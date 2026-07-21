---
name: ingerir-legislacao
description: Use quando o Wândrio colocar PDFs de legislação de CBMs (LOBs, regimentos, regulamentos, quadros de cargos, normas/diretrizes operacionais) na pasta "LEGISLAÇÃO CBMS/" e quiser que sejam lidos e inseridos no portal. Gatilhos "ingira as legislações da pasta", "inseri novos PDFs, processa", "atualize o acervo com esses documentos", "/ingerir-legislacao". Roda o pipeline determinístico (PDF→markdown→builders) na ordem certa, evita as armadilhas conhecidas e reconcilia antes de dizer "pronto".
---

<!--
INSTALAÇÃO:
Skill de PROJETO — versionada no próprio repositório (Comparativo-de-cargos-e-funcoes)
em .claude/skills/ingerir-legislacao/. Fica disponível automaticamente neste repo, sem
copiar para ~/.claude/skills. Uso:  /ingerir-legislacao  (ou "processa os PDFs novos").
Criada 2026-07-20 a partir da ingestão real de 21 documentos novos (17 normas de AL, RI+
Regulamento da BA, Regulamentos de RR e TO, LOB atual de RO).
-->

# Ingerir legislação → inserir no portal (pipeline determinístico)

Você NÃO reescreve dados à mão. Você orquestra o pipeline Python que já existe, na ORDEM
certa, desviando das armadilhas conhecidas, e **reconcilia os números antes de afirmar que
está pronto**. O acervo compartilhado dos 27 estados alimenta quase todas as telas — um
erro aqui se espalha.

## Contexto de execução
Tudo é relativo à RAIZ do repositório (pasta com `scripts/build_states_data.py` e a pasta
`LEGISLAÇÃO CBMS/`). Sessão fora do repo → localize a raiz; não achou → pergunte. Use
sempre caminhos absolutos no Bash, sem `cd ... &&`.

## Princípio inegociável: PROVA antes de "pronto"
É PROIBIDO dizer "ingerido/atualizado" sem colar, na mesma mensagem:
- contagem antes × depois (estados, documentos, markdowns);
- a saída real de `node --test` (deve continuar 107/107, ou o número vigente);
- a lista de documentos NOVOS com o `type` que receberam e se foram classificados por
  conteúdo ou só pelo nome.
Divergência se REPORTA, nunca se ajusta em silêncio.

---

## Armadilhas conhecidas (já morderam — leia antes de rodar)

1. **Python: use o venv isolado do pipeline.** Os scripts exigem 3.10+ (`int | None`). O
   macOS bloqueia `pip install` no Python do sistema (PEP 668) e o 3.12 do Homebrew também.
   Solução validada: um venv dedicado na raiz.
   ```
   python3.12 -m venv .venv-pipeline          # só na primeira vez
   .venv-pipeline/bin/pip install pypdf        # só na primeira vez
   ```
   Depois, SEMPRE chame os scripts com `.venv-pipeline/bin/python scripts/<x>.py`. O
   `.venv-pipeline/` está no `.gitignore` — não versionar.

2. **Grafia divergente do MESMO estado vira dois estados.** O agrupamento usa o texto antes
   do " - " no nome do arquivo. Ex.: acervo antigo usa "Roraíma" (errado), PDF novo veio
   "Roraima". Resultado: 28 estados. NÃO renomeie arquivos para "resolver" — a grafia
   canônica mora em `STATE_NAME_ALIASES` no topo de `build_states_data.py`. Novo conflito
   de grafia → adicione a alias lá (`{"grafiaErrada": "GrafiaCorreta"}`) e reconstrua.

3. **Classificação por NOME de arquivo erra em documentos atípicos.** `parse_doc_type()`
   classifica pelo nome; um "Norma Operacional" ou "Diretriz Operacional" cai no default de
   LOB. Documentos cujo nome não revela o tipo entram em `CONTENT_TYPE_OVERRIDES` (dict no
   topo de `build_states_data.py`), com o tipo correto e um comentário do porquê.
   **Regra de produto validada:** Diretrizes/Normas Operacionais e Regulamentos de Serviço
   regulam o SERVIÇO (não a estrutura) → tipo **"Regulamento Geral"**. LOB só a lei de
   criação/organização. Na dúvida, ABRA o cabeçalho/ementa do markdown e pergunte ao Wândrio
   antes de carimbar — nunca invente o tipo.

4. **Ordem dos builders importa.** `build_organs_detail` antes de `build_states_data` (este
   enriquece a árvore). `build_minuta_comparison` depende de `build_dpo_cot_comparison`.

5. **Escaneados sem OCR.** Se um markdown tiver "Página sem texto digital", o PDF é imagem
   sem OCR — sinalize ao Wândrio (o texto não entrou), não finja que ingeriu.

---

## Passo a passo

**0. Diagnóstico (antes de tocar em nada).** Liste os PDFs em `LEGISLAÇÃO CBMS/` e os
markdowns já em `database/markdown/`. Compare: quais PDFs são NOVOS (sem markdown
correspondente)? Se houver PDFs fora da raiz (ex.: numa subpasta "novos/"), confirme com o
Wândrio se devem ir para a raiz — o portal serve os PDFs a partir da raiz de
`LEGISLAÇÃO CBMS/`, então subpasta = link quebrado no Acervo. Anote contagens ANTES.

**1. Converter.** `.venv-pipeline/bin/python scripts/convert_to_markdown.py` — varre a raiz
de `LEGISLAÇÃO CBMS/` e (re)gera `database/markdown/*.md`. Confira `N/N convertidos`. Note
que uma versão nova do pypdf pode reescrever markdowns antigos com diffs cosméticos
(`autoriz ado`→`autorizado`) — é melhoria, não regressão; mencione mas não reverta.

**2. Classificar os novos.** Para CADA documento novo, leia o cabeçalho/ementa do markdown
(`sed -n '1,30p'`). Decida o tipo pela regra de produto (passo 3 acima). Se o nome do
arquivo não bate com o conteúdo, adicione a `CONTENT_TYPE_OVERRIDES`. Documentos de tipo
ambíguo → pergunte ao Wândrio, não chute.

**3. Reconstruir na ordem.** Rode, checando a saída de cada um:
```
.venv-pipeline/bin/python scripts/build_organs_detail.py
.venv-pipeline/bin/python scripts/build_states_data.py           # confira: N estados | N docs
.venv-pipeline/bin/python scripts/build_dpo_cot_comparison.py
.venv-pipeline/bin/python scripts/build_minuta_comparison.py
.venv-pipeline/bin/python scripts/build_minuta_structure.py
.venv-pipeline/bin/python scripts/build_regulamento_structure.py
.venv-pipeline/bin/python scripts/build_minuta_structure_atual.py
.venv-pipeline/bin/python scripts/build_regulamento_structure_atual.py
```
`build_states_data` deve fechar em **27 estados** (não 28+ — se passar, é grafia, armadilha 2).

**4. Reconciliar.** Abra `database/states_data.json` e confirme: total de estados = 27; os
documentos novos aparecem no estado certo com o `type` esperado; nenhum estado duplicado por
grafia. Cole essa conferência.

**5. Testar.** `node --test` — deve manter 107/107 (ou o número vigente). Cole a saída.

**6. Entregar.** Tabela dos documentos novos (arquivo → estado → tipo → verificado por
conteúdo?), contagens antes×depois, e a saída dos testes. Nada de commit sem o Wândrio pedir.
Ofereça `/abrir-app` para ele conferir na tela do Acervo Legal, e `/handoff` para registrar.

## Quando NÃO usar esta skill
- Curadoria PROFUNDA de órgãos/cargos de um estado (isso é editar `detail_data_g*.py` /
  `curated_organs*.py` à mão — outro fluxo).
- Curadoria do enriquecimento verbatim do Regulamento/RI (fluxo `extrair_*` + `*_enrichment`).
Esta skill é só a PORTA DE ENTRADA: PDF → markdown → JSONs do acervo.
