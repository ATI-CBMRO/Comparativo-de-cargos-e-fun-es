# Skill de Ingestão do Acervo Legal — Design

**Data:** 2026-07-13
**Autor:** brainstorming com o Tiago (Ten Tiago)
**Branch:** `master` (a definir branch de trabalho na implementação)

## Objetivo

Criar uma **skill do Claude** (`.claude/skills/ingestar-acervo/`) que padroniza e executa
o processo de **receber, curar e adicionar novos documentos legais ao Acervo** (camada 1
do pipeline), carimbando cada documento com seu destino downstream (minuta de RI, minuta
de Regulamento, ou referência) sem executar a curadoria cara das camadas 2/3. A skill é
autodisparada quando o usuário quer atualizar o acervo, e inclui um **helper Python
read-only de triagem**. O primeiro uso da skill é aplicá-la ao batch de documentos novos
pendentes.

## Motivação

Documentos novos chegam em lotes (hoje, uma pasta de staging dentro de `LEGISLAÇÃO CBMS/`).
A ingestão manual é frágil em três pontos que já causaram erro real no projeto:

1. **Classificação por nome falha.** `parse_doc_type()` só olha o nome do arquivo. Nos
   documentos deste batch: "Maranhão - Portaria" cairia no default "Lei de Organização
   Básica" (é Regimento de Serviços); "Pará - Regulamento de serviço" viraria "Regulamento
   Geral" (é Regimento de Serviços). Precedentes já corrigidos à mão: MT, SE, SC, RN, GO.
2. **Extração ruim passa despercebida.** PDFs escaneados sem OCR (Piauí) ou com fonte
   mapeada por glifos (`/U0044…`, caso do RJ DAT) produzem markdown lixo que contamina tudo
   a jusante. Hoje só se descobre lendo o markdown no olho.
3. **Renomeações quebram overrides silenciosamente.** `CONTENT_TYPE_OVERRIDES` é indexado
   pelo nome do arquivo `.md`. Quando um PDF é renomeado (MT: "Regimento Interno" →
   "Regulamento Geral"; SE: "Regimento Interno" → "Regulamento Interno"), a chave antiga
   fica órfã e a classificação passa a estar errada sem aviso.

Uma skill encapsula o processo correto uma vez, autodisparado, com gates explícitos de
decisão nos pontos frágeis — em vez de re-derivar o passo a passo a cada lote.

## Decisões tomadas no brainstorming

1. **Profundidade = camada 1 (Acervo) primeiro.** A skill leva o documento até aparecer na
   tabela de cobertura, com tipo classificado e verificado. As camadas 2 (comparação
   verbatim) e 3 (enriquecimento da minuta do RO) ficam para etapas seguintes, documento por
   documento. A skill NÃO faz curadoria verbatim.

2. **Entregável = skill reutilizável + aplicar ao batch atual.** A skill é o processo padrão
   para qualquer documento futuro; o primeiro uso é o lote pendente.

3. **Formato = skill do Claude** (não doc solto, não doc+script separado). O helper Python de
   triagem mora DENTRO da pasta da skill.

4. **Helper `.py` read-only, consultivo.** Só triagem: não renomeia, não move, não edita
   overrides, não roda o rebuild. Automatiza apenas os dois gates mecânicos (qualidade da
   extração + validação de nome/`STATE_META`) e propõe o tipo por conteúdo. A decisão final de
   classificação continua sendo do humano/agente.

5. **Rebuild = cadeia completa.** Após adicionar o documento, rodar a cadeia inteira
   documentada no CLAUDE.md (não apenas `build_states_data`), para manter todos os JSON
   derivados consistentes.

6. **RJ DAT fora do batch atual.** Excluído da pasta pelo Tiago (extração ilegível + nível de
   diretoria, não da corporação). O gate de qualidade da extração permanece na skill como
   salvaguarda para documentos futuros.

## Arquitetura

### Estrutura de arquivos

```
.claude/skills/ingestar-acervo/
  SKILL.md                    # frontmatter (name, description/trigger) + checklist do SOP
  scripts/
    triagem_acervo.py         # helper read-only de triagem
    test_triagem_acervo.py    # testes da lógica pura (convenção test_*.py do repo)
```

O helper vive na pasta da skill (não em `scripts/` do repo) para manter a skill
autocontida. Os testes seguem a convenção `test_*.py` do repo; se convier rodá-los no
`test:py`, apontar o caminho da skill no script de teste do `package.json`.

### O helper `triagem_acervo.py` (read-only)

**Entrada:** um caminho de pasta (a pasta de staging, já congelada). **Saída:** uma tabela por
PDF impressa no stdout, sem tocar em nenhum arquivo.

Colunas do relatório, por PDF:
- **Nome do arquivo** e nº de páginas.
- **Prefixo → estado:** valida o prefixo (texto antes de " - ") contra as chaves de
  `STATE_META` (importado de `scripts/build_states_data.py`). Marca ✓ se casa exatamente
  (acentos incluídos), ✗ + sugestão do estado mais próximo se não.
- **Score de qualidade da extração:** heurística sobre o texto extraído (pypdf) das primeiras
  N páginas — proporção de tokens de glifo `/U00XX`, proporção de páginas vazias, densidade de
  caracteres alfabéticos por página. Classifica em `OK` / `SUSPEITO` / `RUIM`. `RUIM` =
  provável escaneado/sem OCR ou fonte por glifos → aciona o gate do passo 3.
- **Tipo por nome:** o que `parse_doc_type()` retornaria para o nome do arquivo.
- **Tipo por conteúdo (proposto):** varredura de palavras-chave na ementa/primeiros artigos
  (ex.: "diretriz operacional", "serviço … diário", "atividades diárias" → Regimento de
  Serviços; "organização básica"/"cria o Corpo" → LOB; etc.). É uma PROPOSTA.
- **Divergência:** sinaliza quando tipo-por-nome ≠ tipo-por-conteúdo (exige override).

Lógica pura testável: as funções de `score_extracao(texto) -> str`,
`tipo_por_conteudo(texto) -> str` e `valida_prefixo(nome, STATE_META) -> (bool, estado|None)`
são puras e têm testes. A leitura de PDF (pypdf) fica isolada numa função fina não-testada.

### O `SKILL.md` — checklist do SOP

Frontmatter:
- `name: ingestar-acervo`
- `description:` gatilho — "Use ao adicionar/atualizar documentos de legislação no Acervo
  Legal do portal (novos PDFs em LEGISLAÇÃO CBMS/, atualizar acervo, classificar tipo de
  documento). Leva o documento à camada 1 (acervo) e carimba seu destino nas minutas."

Corpo = os 9 passos abaixo, cada um como item de checklist (o agente cria um todo por passo).

## Fluxo de dados (os 9 passos)

**0. Congelar o batch.** A pasta de staging sincroniza ao vivo pelo OneDrive (nome e conteúdo
mudaram durante o próprio brainstorming). Listar os PDFs + tamanho, copiar para um local
estável fora do staging, confirmar o conjunto antes de processar.

**1. Normalizar nomenclatura.** Rodar o helper de triagem. Para cada arquivo, garantir
`<Estado por extenso> - <Descrição>.pdf` com o prefixo batendo EXATAMENTE uma chave de
`STATE_META` (é assim que `build_states_data` deriva o estado). Corrigir acento/caixa. Mover o
arquivo normalizado para a **raiz** de `LEGISLAÇÃO CBMS/` (o `convert_to_markdown` só varre o
topo, não subpastas).

**2. Converter.** `python scripts/convert_to_markdown.py`.

**3. Gate de qualidade da extração.** Ler o score do helper. Se `RUIM`: PARAR e decidir —
buscar fonte com OCR, ou registrar "no acervo, extração pendente de OCR" com `typeVerified`
falso e não confiar no markdown a jusante. Não prosseguir no automático para documentos `RUIM`.

**4. Classificar por CONTEÚDO.** Ler ementa/primeiros artigos e escolher o tipo canônico entre:
`Lei de Organização Básica`, `Regimento Interno`, `Regimento de Serviços`, `Regulamento Geral`,
`Normas Gerais de Ação`, `Quadro Demonstrativo de Cargos`, `Quadro de Organização e
Distribuição`. Comparar com `parse_doc_type(nome)`:
- Coincide → adicionar o arquivo `.md` a `CONTENT_VERIFIED_FILES` (selo ✓).
- Diverge → adicionar/ajustar `CONTENT_TYPE_OVERRIDES[<arquivo.md>] = <tipo correto>` e marcar
  verificado.
- Arquivo renomeado → REMOVER a chave de override antiga e criar a nova (corrige MT/SE).

**5. Rebuild completo.** Rodar a cadeia inteira, na ordem do CLAUDE.md:
`convert_to_markdown` → `build_organs_detail` → `build_states_data` → `build_dpo_cot_comparison`
→ `build_minuta_comparison` → `build_minuta_structure` → `build_regulamento_structure`.

**6. Verificar (evidência antes de afirmar).** Diff do `states_data.json`: o documento aparece
no estado + tipo certos, `typeVerified` correto, contadores e célula da tabela de cobertura
atualizados. Rodar `node --test` (lógica de `acervoCoverage` etc.). Opcional: subir o dev
server e conferir a página Acervo.

**7. Handoff para camadas 2/3.** Registrar em `.claude/PENDENCIAS.md`, por documento, se é
candidato à camada de comparação e/ou à minuta, e QUAL minuta, conforme o mapa tipo→minuta.

**8. Limpeza + registro.** Remover os arquivos processados do staging, atualizar a contagem do
acervo no CLAUDE.md se mudou, e propor commit (só commitar se o usuário pedir).

## Mapa tipo → minuta (o carimbo do passo 7)

| Tipo classificado | Alimenta | Script downstream |
|---|---|---|
| Regimento Interno (organizacional, corporação inteira) | Minuta de RI | `ri_alternativas_enrichment.py`, `minuta_enrichment.py` |
| Regulamento Geral **ou** Regimento de Serviços | Minuta de Regulamento | `regulamento_enrichment_<uf>.py` |
| Lei de Organização Básica | camada LOB (comparação) | `lob_enrichment.py` |
| Quadro / Normas Gerais de Ação | referência (não alimenta minuta) | — |
| RI de diretoria ou extração `RUIM` | só acervo, sinalizado | — (decisão manual) |

## Aplicação ao batch atual

Re-snapshot no momento da execução (a pasta sincroniza ao vivo). Conjunto conhecido hoje:

- **Maranhão - Portaria** → conteúdo é Diretriz Operacional (Gestor Operacional de Dia,
  Supervisor do CIOPS) → tipo **Regimento de Serviços** (override; `parse_doc_type` daria LOB).
- **Pará - Regulamento de serviço** → Decreto 1.052/2020, serviços diários → tipo **Regimento
  de Serviços** (override; `parse_doc_type` daria Regulamento Geral). É o 2º documento do PA
  (já há um "Regimento Interno" organizacional).
- **MT / SE (renomeações já em disco)** → atualizar `CONTENT_TYPE_OVERRIDES` para os novos
  nomes: MT "Mato Grosso - Regulamento Geral.md" (parse já dá "Regulamento Geral" → remover a
  chave antiga, sem novo override); SE "Sergipe - Regulamento Interno.md" (parse daria
  "Regulamento Geral", mas conteúdo é RISD → override para "Regimento de Serviços"; remover a
  chave antiga).
- **Santa Catarina - Organização Básica alterações** → verificar conteúdo (provável LOB de
  alteração); confirmar se afeta o override existente de SC.
- **RJ DAT** → fora do batch (excluído pelo Tiago).

## Componentes e responsabilidades (isolamento)

- **`triagem_acervo.py`** — o quê: relatório read-only de triagem; como se usa:
  `python .claude/skills/ingestar-acervo/scripts/triagem_acervo.py <pasta>`; depende de:
  pypdf + `STATE_META`/`parse_doc_type` de `build_states_data.py`.
- **`SKILL.md`** — o quê: o processo de 9 passos que o agente segue; como se usa: autodisparo
  por gatilho; depende de: o helper e os scripts existentes do pipeline.
- **Scripts do pipeline (existentes)** — inalterados; a skill os orquestra, não os reescreve.

## Tratamento de erros / gates de decisão

- **Prefixo não bate `STATE_META`** (passo 1) → parar e normalizar o nome antes de converter.
- **Score `RUIM`** (passo 3) → parar; decidir OCR vs. registrar como pendente; não confiar
  no markdown a jusante.
- **Divergência tipo nome × conteúdo** (passo 4) → exige entrada em `CONTENT_TYPE_OVERRIDES`.
- **Batch instável (OneDrive)** → sempre re-snapshot no início; nunca assumir o conjunto.

## Testes

- Lógica pura do helper (`score_extracao`, `tipo_por_conteudo`, `valida_prefixo`) com testes
  Python, no padrão `test:py` do repo.
- Verificação de ponta a ponta ao aplicar ao batch: diff do `states_data.json` + `node --test`.

## Fora de escopo (YAGNI)

- Camada 2 (extração verbatim / `alternatives`) e camada 3 (enriquecimento da minuta) — a skill
  só registra candidatura no backlog.
- OCR automático de PDFs escaneados — o gate apenas sinaliza; a obtenção de fonte legível é
  manual.
- Qualquer mutação feita pelo helper — ele é estritamente read-only.
- Novos estados — os 27 já estão em `STATE_META`.
