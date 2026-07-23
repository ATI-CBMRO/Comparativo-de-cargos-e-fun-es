# CLAUDE.md

Guia para o Claude Code neste repositório.

## Visão geral

Portal de Legislação dos Corpos de Bombeiros Militares — SPA React/Vite que compara
legislações (LOB, regimentos internos, organogramas, quadros de efetivo) dos 27 CBMs
estaduais, com identidade visual do CBMRO (50 documentos legais). Além de comparar, o
portal ELABORA as minutas do CBMRO (Regimento Interno e Regulamento Geral) a partir
desse acervo.

**LEIA PRIMEIRO — o portal tem DOIS CENÁRIOS que nunca se misturam** (ver seção
"Cenários LOB"): **LOB atual** (Lei 2.204/2009, vigente) e **LOB futura** (nova LOB, em
aprovação). Quase tudo neste guia descreve a trilha da FUTURA; o cenário ATUAL tem
geradores e dados próprios. Antes de mexer em qualquer minuta/gerador, saiba em qual
cenário está.

## Comandos

```bash
npm install              # dependências
npm run dev              # dev server em http://localhost:5173 (+ endpoint de IA via middleware)
npm run build            # build de produção (Vite/Rollup -> dist/)
npm run preview          # pré-visualizar o build
node --test              # testes de lógica pura (96 testes; ver arquivos *.test.js em src/lib e api/)
```

**Ingestão de novos PDFs de legislação → use a skill `/ingerir-legislacao`** (em
`.claude/skills/`): orquestra o pipeline abaixo na ordem certa, desvia das armadilhas
(venv isolado, grafia divergente de estado, classificação por conteúdo) e reconcilia.

**Pipeline de dados (Python 3.10+ — os scripts usam `int | None`). No Mac, o `pip` é
bloqueado no Python do sistema e no 3.12 do Homebrew (PEP 668): use o venv isolado
`.venv-pipeline/` — `.venv-pipeline/bin/python scripts/<x>.py` (fora do git).** ORDEM IMPORTA:

```bash
python scripts/convert_to_markdown.py      # PDFs em "LEGISLAÇÃO CBMS/" -> database/markdown/*.md
python scripts/build_organs_detail.py      # detail_data_g*.py + detail_cargos_g*.py -> database/organs_detail/<id>.json
python scripts/build_states_data.py        # markdown/*.md + organs_detail/*.json -> database/states_data.json (fonte única)
python scripts/build_dpo_cot_comparison.py # organs_detail/*.json -> database/comparativo_dpo_cot.json
python scripts/build_minuta_comparison.py  # + minuta_enrichment.py + lob_enrichment.py -> database/comparativo_minuta.json
python scripts/build_minuta_structure.py   # organs_detail/ro.json + minuta_enrichment.py -> database/minuta_structure.json
python scripts/build_regulamento_structure.py # -> database/regulamento_structure.json
```

`build_organs_detail` antes de `build_states_data` (este enriquece a árvore com os
desdobramentos do detalhamento). `build_minuta_comparison` depende de
`build_dpo_cot_comparison` + `build_organs_detail`.

## Arquitetura

### Camada de dados (pipeline Python, offline)

O frontend nunca lê PDFs; consome JSON gerado. Fluxo: **PDFs** (`LEGISLAÇÃO CBMS/`) →
`convert_to_markdown` (pypdf) → `build_states_data` faz parsing e produz
**`states_data.json`** (fonte única de quase todas as páginas). O dict `STATE_META` no
topo de `build_states_data.py` é o mapa canônico estado→{id, abbr, region, cbm}; o `id`
minúsculo (`ro`, `df`) é a chave de rotas e arquivos.

- `build_organs_detail` agrega `scripts/detail_data_g1..g5.py` (órgãos) e mescla
  `scripts/detail_cargos_g1..g5.py` (cargos: cargo, subordinadoA, requisito, desdobramentos,
  atribuições — via `merge_cargos()`) → um `organs_detail/<id>.json` por estado.
- `build_states_data` também ENRIQUECE o organograma: `enrich_tree_from_detail()` adiciona
  os `desdobramentos` como nós-filhos (`_reg: true`) e **carimba cada nó com `detailId`**
  (resolvido por nome canônico/sigla/tokens) — por isso `StateDetail` abre o painel certo
  mesmo quando o nome na árvore difere do detalhamento. Daí a ordem de execução importar.

Curadoria de dados:
- Organogramas curados à mão em `scripts/curated_organs*.py` (cobrem os 27 estados, mas a
  PROFUNDIDADE varia muito: RO ~194 nós, SP ~7 stub). `stats.curated=true` só significa que
  há árvore, não curadoria profunda. Ranking em `docs/BACKLOG_CURADORIA.md`.
- `ro.json` e `ac.json` são escritos à mão (exceção — os demais 24 são gerados; não editar
  JSON gerado, edite os `detail_data_g*.py`/`curated_organs*.py` e reexecute o script).
- Atribuições VERBATIM (texto integral com inciso) nos estados cujas leis enumeram por
  cargo: AL, AM, DF, ES, MT, PA, PR. Demais (GO, SE) têm prosa/finalidade — sem invenção.

### Frontend (React)

Entrada `src/main.jsx` (BrowserRouter) → `src/App.jsx` (layout Header+Sidebar+main, rotas e
o array **`NAV_GROUPS`**). Páginas fazem `fetch('/database/...')`. Estilo: CSS único em
`src/index.css`; tema claro CBMRO (cabeçalho `#c8102e`, sidebar navy, conteúdo `#eef1f6`);
tipografia Outfit+Inter; ícones `lucide-react`.

**Barra lateral**: começa EXPANDIDA e NÃO recolhe ao clicar num item — só pelo botão
"Recolher menu" (rodapé) ou pelo ☰. Estado `collapsed` (default `false`), separado do
`navOpen` da gaveta mobile.

**Menu (`NAV_GROUPS`, 3 blocos):**
- **Geral**: Acervo Legal (`/legislacoes`), Organograma (`/organograma`), Manual de uso
  (`/manual`), Acessos (`/acessos`, só admin).
- **Regimento Interno** (trilha): Subsídio (`/minuta/subsidio`) · Minuta do Regimento
  Interno (`/minuta`) · Diagramas (`/minuta/diagramas`) · Revisão (`/minuta/revisao`).
- **Regulamento Geral** (trilha espelhada): `/regulamento/subsidio` · `/regulamento` ·
  `/regulamento/diagramas` · `/regulamento/revisao`.

`/` redireciona para `/legislacoes`. Rotas mantidas por compat (fora do menu): `/estados`,
`/estados/:id`, `/busca`, `/comparar`, `/minuta-diagramas`, `/minuta/comparar`,
`/minuta/comparativo-ri`, `/minuta/deliberacao`, `/regulamento/comparar`, `/revisao`.

### Páginas principais

- **Acervo Legal** (`Legislations.jsx`): tabela-resumo `estado × tipo` no topo — lógica pura
  em `src/lib/acervoCoverage.js` (testada), apresentação em `AcervoCoverageTable.jsx` (3
  sub-abas: Tabela / Por documento / Documentos por estado; nomes de documento clicáveis
  abrem o PDF em popup). Coluna "Regulamento de Serviço" funde `Regulamento Geral` +
  `Regimento de Serviços`. Selo ✓/⚠ = `typeVerified` (conteúdo vs. só nome). A tabela é
  panorama fixo dos 27 (não filtrada pela busca da página).

- **Organograma** (`/organograma`, `Organograma.jsx`): página institucional com 7
  visualizações da MESMA estrutura do CBMRO (clássico, faixas por natureza, cartões, árvore
  interativa, blueprint, unificado com linhas de subordinação, e projeção territorial da
  nova LOB sobre as 17 cidades reais). Dados curados no TOPO do componente
  (`ORGAOS`/`TREE`/`OPTREE`/`TECTREE`/`ESPTREE`) para edição fácil; CSS escopado sob `.orgv`
  no index.css. A classificação por natureza (direção/apoio/execução) e o mapeamento
  territorial são PROPOSTA a validar (a LOB não rotula natureza nem nomeia unidades
  municipais).

- **Subsídio unificado** (`/minuta/subsidio`, `RISubsidio.jsx` + `RISubsidioComparativo.jsx`;
  espelho `RegSubsidio.jsx`): compara a minuta do RO com outros estados, dispositivo a
  dispositivo. Eixo = navegação ("Navegar por: Organização/capítulos ou Órgãos/organograma"
  — trocar a navegação NÃO muda a comparação). Abas Regimento Interno | LOB com seleção
  (órgão + estado) COMPARTILHADA entre abas via `organKey` (`MinutaComparator` aceita props
  controladas). Numeração CONTÍNUA da minuta (`buildArticles(structure)` filtrado por
  `chapterIdOf`, não reinicia por órgão). Painel do estado = UMA seção adaptativa: prefere
  TEXTO ORIGINAL verbatim (das `alternatives`/Bloco D); na falta, cai para COMPETÊNCIAS
  rotulado "texto integral ainda não extraído". `SubsidioTabs.jsx` é a casca reutilizável.
  As telas antigas `/comparar`, `/minuta/comparativo-ri`, `/minuta/comparar` continuam por
  compat (dados em `comparativo_minuta.json`: colunas `lobOrgans`, `organs` (LOB+RI),
  `riOrgans`; lógica em `riComparison.js`, testada).

- **Wizard de Minuta** (`/minuta`, `MinutaWizard.jsx`; espelho `RegulamentoWizard`): documento
  único rolável que gera `.docx` client-side (lib `docx`). Estrutura vem de
  `build_minuta_structure.py` (lê `organs_detail/ro.json`, percorre os 26 órgãos da LOB na
  ordem de subordinação + Guarnição; `cg` é a raiz do `commandChart`). Enriquecimento
  VERBATIM de outros CBMs em `scripts/minuta_enrichment.py` (`ENRICHMENT_ORGAN` por órgão +
  `GUARNICAO_CHAPTER` do RISD-SE), rotulado por fonte — critério/descartes em
  `docs/ENRIQUECIMENTO_MINUTA.md`; só entra competência enumerada e verbatim; `ro.json`
  nunca é tocado. Numeração em `src/lib/minutaArticles.js` (`buildArticles`, testado);
  curadoria por inciso via `excluded: Set<"editId#index">`.

- **Diagramas** (`/minuta/diagramas`, `MinutaDiagrams.jsx`): duas visões do
  `minuta_structure.json` — Organograma (`MinutaOrgChart.jsx`, cadeia de comando em CSS puro
  a partir de `commandChart`; nós expansíveis) e Mapa mental (`MinutaMindMap.jsx`). Ambos
  abrem painel lateral do capítulo; export via `window.print()`. `/regulamento/diagramas`
  (`RegDiagramas.jsx`) está "em breve" (falta `commandChart` no `regulamento_structure.json`).

- **Manual de uso** (`/manual`, `Manual.jsx`): guia interno tela por tela.

### Servir dados

`vite.config.js` tem 2 plugins: `serveDatabase` (dev: expõe `/database/*` e
`/legislacao-pdf/*`) e `copyDatabaseOnBuild` (build: copia `database/` → `dist/database/` e
`LEGISLAÇÃO CBMS/` → `dist/legislacao-pdf/`). Essas pastas ficam FORA de `public/` (grandes,
regeneradas). `public/` é servida na raiz (brasão `/BrasaoCBMRO2D-COMPLETO.png`).

## Cenários LOB — atual × futura (Fases 1 e 2, 15-16/07/2026)

O portal separa **dois cenários que NUNCA se misturam**:
- **LOB futura** — nova LOB (em aprovação). É o trabalho antigo; **curadoria PAUSADA**.
- **LOB atual** — Lei nº 2.204/2009 vigente (red. até Lei 5.697/2023). Foco atual.

**A chave:** `ScenarioSwitcher` no topo da sidebar; `src/context/ScenarioContext.jsx`
(`ScenarioProvider`/`useScenario` → `{ cenario, setCenario }`, dentro do `BrowserRouter`,
ver `main.jsx`). Lógica pura em `src/lib/scenario.js` (`SCENARIOS`, `DEFAULT_SCENARIO='futura'`,
`normalizeScenario`, `resolveScenario`, `scenarioDbUrl`), testada. Cenário na URL
(`?cenario=atual|futura`, carimbado no mount) + `localStorage`.

**Gavetas de dados:** a **futura fica na RAIZ de `database/`** (arquivos de sempre —
NÃO mover); o **atual em `database/atual/`**. Resolva SEMPRE com
`scenarioDbUrl(cenario, 'minuta_structure.json')`. Compartilhados entre cenários (não
mexer): `states_data.json`, `organs_detail/` (acervo dos 27), `markdown/`.

**Geradores do ATUAL são separados** (os da futura estão colados à LOB futura via
`ORGAN_ORDER` hardcoded + enriquecimento):
```bash
python scripts/build_minuta_structure_atual.py       # RI do atual (por ÓRGÃO) + commandChart
python scripts/build_regulamento_structure_atual.py  # Regulamento do atual (TEMÁTICO)
python scripts/build_minuta_comparison_atual.py      # comparativo do atual (SÓ camada automática)
```
- `database/atual/organs_detail/ro.json` — 21 órgãos do CBMRO vigente, curados à mão,
  competências VERBATIM da Lei 2.204/2009. Estrutura **validada pelo organograma oficial**
  (`docs/curadoria/lob-atual-ro/` — PDF + `estrutura-vigente-validada.md`). É a fonte da verdade.
- `build_regulamento_structure_atual.py` **lê o `regulamento_structure.json` da futura** e
  re-carimba os ids (não chama o builder da futura, que reescreveria o arquivo dela).

**⚠️ ARMADILHA (já mordeu):** `build_competencia_section` e `build_cargo_sections` de
`build_minuta_structure.py` chamam `enrich_organ_for`/`enrich_for` — enriquecimento de
OUTROS ESTADOS da futura. Reusá-las no atual **vaza CBMMT/PA/DF** na competência do CBMRO.
Por isso o gerador do atual reescreve essas duas seções SEM enriquecimento (só
`build_finalidade_section`/`build_organizacao_section` são neutras e reusáveis).

**Regra de produto:** o **RI é por ÓRGÃO** (estrutura → LOB-específica); o **Regulamento é
TEMÁTICO** (serviço/disciplina/uniformes/ensino → NÃO depende da LOB), por isso o atual
reusa os 16 temas / 413 artigos primários já curados (ver seção "Regulamento Geral em 2
Partes" abaixo), só isolando os ids.

**Isolamento no Firebase** (comentários e textos finais) — marcador embutido no `editId`,
mesma filosofia do `reg:` (sem campo novo, sem migração):
- atual: `atual:organ:...` (RI) e `reg:atual:...` (Regulamento);
- futura: **SEM marcador** (preserva os comentários existentes).
`reviewGroup.js`: `scenarioOfDispositivo` + `filterSuggestionsByScenario`/`filterFinalsByScenario`
(testados). Sem isso, ids como `organ:cg` colidiriam entre cenários.

**Conferência linear** (`/minuta/conferencia`, `/regulamento/conferencia` — `ConferenciaLinear.jsx`,
Fase 1 do cockpit de curadoria, 22/07/2026): percorre a minuta dispositivo a dispositivo
(numeração contínua via `buildConferencia` em `src/lib/conferencia.js`) com as referências de
outros estados ao lado (badge exata/auto). Funciona nos 2 cenários; SEM `TrilhaRoute`. O
**Regimento atual** reaproveita o **Bloco D verbatim da futura** casando órgão a órgão — de-para
`DEPARA_BLOCO_D` em `build_minuta_structure_atual.py` (só o campo `alternatives`, nunca as
competências do RO; 19 dos 21 órgãos; `emg`/`comissoes` sem equivalente = estado vazio honesto).
Spec `2026-07-22-cockpit-curadoria-conferencia-decisoes-design.md` (Fases 2/3 pendentes:
decisões do Obsidian no sistema + registrar/aplicar).

**Telas do atual prontas:** `/minuta` (RI, 21 capítulos), `/regulamento` (16 temas),
`/minuta/diagramas`, `/minuta/revisao`, `/regulamento/revisao`, e **Subsídio**
(`/minuta/subsidio`, `/regulamento/subsidio` — destravados 22/07/2026; o comparativo do
atual vem de `build_minuta_comparison_atual.py`, SÓ casamento automático por palavra-chave,
selo "Correspondência automática — sujeita a revisão" na tela; NÃO importa os módulos de
enriquecimento da futura — ver spec `2026-07-22-subsidio-cenario-atual-design.md`). Rotas de
compat (`/comparar`, `/minuta/comparar` etc.) seguem gated via `TrilhaRoute`. Specs/planos em
`docs/superpowers/specs/2026-07-15-cenarios-lob-atual-futura-design.md` e
`docs/superpowers/plans/2026-07-15-cenarios-lob-fase1.md`.

## Regulamento Geral em 2 Partes (Geral × Serviço) — 21/07/2026

O Regulamento Geral deixou de ser uma sequência única de temas: agora é **um documento com
2 Partes** — Parte I (Geral/institucional, 12 temas) e Parte II (de Serviço/operacional, 4
temas). Cada capítulo de `regulamento_structure.json` tem o campo `parte: 'geral'|'servico'`;
o gerador (`build_regulamento_structure.py`, dict `TEMA_PARTE`) ordena Parte I antes da Parte
II. Helper compartilhado: `src/lib/regulamentoPartes.js` (`PARTE_HEADERS`,
`parteByChapterTitle`) — usado por `RegulamentoWizard.jsx`, `minutaDocx.js`,
`RegulamentoComparator.jsx` e `Revisao.jsx` (modo Regulamento). Para o RI, que não tem campo
`parte`, o helper retorna `{}` e vira no-op automático — não confundir os dois documentos.

**16º tema**: `central-operacoes-193` ("Da Central de Operações e do Teledespacho") — matéria
recorrente (achada em 4 fontes: BA/RR/TO/ES) sem tema próprio na base original de 15. Primária:
Bahia (Art. 8-9 Supervisor + 18 Operador de Teledespacho/CICOM); alternativa: Tocantins (Anexo
2, Art. 12-14). **413 artigos primários** ao todo (410 da curadoria original + 3 do 16º tema).

**RISG do Exército** (`database/markdown/RISG.md`, convertido de `LEGISLAÇÃO CBMS/RISG.pdf`)
entra como pseudo-fonte `risg` (rotulada "Exército Brasileiro") — **só como alternativa, nunca
como fonte primária de nenhum tema** (testado em `test_regulamento_structure.py`). Reforça
`cerimonial-honras` e `pessoal-quadros`. Fontes verificadas por leitura de subagentes antes de
qualquer decisão de estrutura — ver vault Obsidian `Codebases/Comparativo-de-cargos-e-funcoes/`
(notas "Comparativo RISG × Regulamentos — Round 1/Round 2").

**Pendências sinalizadas (não forçadas)**: corpo principal de Tocantins (Art. 1-13,16 — colide
numeração de "Art. N" com o Anexo 2 já usado); 4 Diretrizes/Normas de Alagoas sem "Art. N"
formal (seção numerada, incompatível com o extrator atual); tema `uniformes-apresentacao`
segue magro (1 artigo, sem achado forte no RISG). `RegDiagramas.jsx` foi destravado em
21/07/2026 (árvore do documento — ver seção Diagramas), sem `commandChart` artificial.

Specs/planos: `docs/superpowers/specs/2026-07-21-regulamento-geral-2-partes-design.md` (Fase 1
— estrutura), `2026-07-21-fase2a-central-operacoes-193-design.md` (16º tema),
`2026-07-21-fase2bcd-reforco-verbatim-design.md` (reforço verbatim), `2026-07-21-fase1-heranca-2partes-telas-design.md`
(herança nas telas) — e os planos irmãos em `docs/superpowers/plans/`.

## Curadoria — Minuta do Regulamento (em andamento)

Gerar a minuta do Regulamento a partir dos regulamentos de outros estados (MT como
esqueleto — a LOB de RO seguiu a de MT). 4 passos por estado antes de transcrever:
1. `scripts/sugerir_equivalencias.py <uf>` — candidatos por tema (feito p/ 9 estados).
2. De-para tema→artigos: `docs/curadoria/de-para-<uf>.md` (validados; matriz em
   `panorama-cobertura.md`).
3. Validação humana (concluída 2026-07-07).
4. Extração determinística: `extrair_regulamentos.py` corta os markdowns por "Art. N" →
   `regulamento_enrichment_<uf>.py` (850 artigos, GERADOS). Mestre
   `regulamento_enrichment.py` (15 THEMES, PRIMARY_SOURCE, ADAPTATIONS CBMMT→CBMRO).
5. Verificação verbatim: `verificar_verbatim.py` (todo caput deve existir literalmente na
   fonte). `equivalencias_terminologicas.py` = glossário de sinônimos.
6. `build_regulamento_structure.py` → `regulamento_structure.json` (mesmo formato do
   minuta_structure, com `alternatives` por tema). Valida: `test_regulamento_structure.py`.

Mecanismos descobertos testando (2026-07-08): `strip_lines` em `CONFIG[<uf>]` (remove
linhas-fragmento antes do parse — achado no Art. 53 do RISD-SE); `hasOwnMarker()` em
`minutaArticles.js` (dispositivos que começam com "Parágrafo único"/"§" são unidades
completas → verbatim, `ownMarker: true`, telas pulam o prefixo romano).

## Bloco D — comparador de RI verbatim (concluído 2026-07-09)

`/minuta/comparar` (`MinutaRIComparator.jsx`) compara o TEXTO verbatim de cada artigo.
`minuta_structure.json` tem `alternatives` em cada nó `kind:'organ'` — 25 dos 27 órgãos
cobertos (AL, DF, PA, PR, RS). A coluna do estado mostra o ARTIGO COMPLETO (decisão de
produto). Extração: `extrair_ri_alternativas.py` → `ri_alternativas_enrichment.py`; valida
`test_minuta_alternativas.py`. Curadoria (Fable) em `docs/curadoria/bloco-d-*.md`.
Lacunas sem correspondência plena: `guarnicao` (matéria de RISD) e `gbm` (homônimo no RS).

## Classificação de tipo de documento (fechado 2026-07-08/09; atualizado 2026-07-13)

`parse_doc_type()` (`build_states_data.py`) classifica pelo NOME do arquivo; erros
confirmados corrigidos via `CONTENT_TYPE_OVERRIDES`. Estado atual dos overrides: **SE**
("Regulamento Interno") é o **RISD** → Regimento de Serviços; **MA** ("Portaria 46",
Diretriz Operacional do serviço diário) e **PA** ("Regulamento de serviço", Decreto
1.052/2020) → **Regimento de Serviços**. **MT** teve o PDF renomeado "Regimento Interno" →
"Regulamento Geral" (rename puro), então parse_doc_type já acerta e o override foi removido.
**SC** deixou de ser Regimento Interno: o antigo "Organização Básica" era o Decreto
1.328/2021 (regulamenta a LOB), obtido escaneado; foi substituído pela LOB real — **LC nº
724/2018** (`Organização Básica`) + **LC nº 885/2025** (`Organização Básica alterações`),
ambas **LOB**, geradas do texto oficial da ALESC (PDF pesquisável). O decreto foi descartado
e o override de SC removido.

Campo `typeVerified` por documento (✓ conteúdo / ⚠ só nome): **47 de 50** verificados por
conteúdo. Fora, de propósito: **PI** (PDF escaneado sem OCR) e **SP** (2 arquivos organizam
a PM inteira, CBM só como seção — aguardando confirmação do Wândrio). Decisão: não bloquear
recursos numa auditoria completa; a UI já sinaliza o que foi verificado.

Para ADICIONAR documentos ao acervo use a skill **`ingestar-acervo`** (`.claude/skills/`),
que padroniza o processo (camada 1): triagem read-only (`scripts/triagem_acervo.py` — gate
de qualidade da extração + tipo por conteúdo + validação de nome contra `STATE_META`),
classificação por conteúdo, rebuild completo e handoff das camadas 2/3.

## Revisão Colaborativa da Minuta (Firebase: login + comentários + IA)

Módulo independente: convidados fazem login e comentam a minuta dispositivo por dispositivo.
Backend **Firebase** (Auth e-mail+senha + Firestore) consumido do frontend; IA por função
serverless. Specs em `docs/superpowers/specs/` e `plans/`.

**Rotas/telas:** `/login` (`Login.jsx`, com link "Primeiro acesso? Criar minha senha" →
`/cadastro`) · `/cadastro` (`Cadastro.jsx`, autocadastro: o convidado cria a própria senha;
autorizado só se o e-mail estiver em `members` com `ativo:true`) · `/revisao` (protegida,
`Revisao.jsx` — aceita prop `initialDoc` 'ri'|'reg'; balões na margem + `RevisaoModal.jsx`)
· `/acessos` (protegida, admin — `Acessos.jsx`: convidar por e-mail, papel, bloquear/liberar/
remover, acompanhar último login).

**Auth:** `src/lib/firebase.js` (Auth+Firestore de `import.meta.env.VITE_FIREBASE_*`);
`src/lib/auth.jsx` (`AuthProvider`/`useAuth`) autoriza por **e-mail** (`members/{email}`,
`ativo:true`); expõe `entrar`/`cadastrar`/`sair`/`recuperarSenha` (e-mails normalizados por
`normalizeEmail`). `ProtectedRoute.jsx` (com `requireAdmin`).

**Firestore:** coleções `members` (indexada por E-MAIL), `suggestions`, `finalTexts`.
`firestore.rules` usa `request.auth.token.email` (publicar pelo console — `docs/FIREBASE_SETUP.md`).
`dispositivoId` (`src/lib/dispositivoId.js`) = endereço ESTÁVEL (`editId#index`); premissa:
congelar `minuta_structure.json` durante a rodada. **Multi-documento**: `/revisao` comenta RI
e Regulamento sem misturar, via prefixo `reg:` no `editId` (`reviewGroup.js:docOfDispositivo`);
`config/revisao.regulamentoAberto` (boolean, fail-closed) libera o Regulamento a não-admin.

**IA:** `api/_gerarProposta.js` (núcleo, testado) reusado por `api/gerar-proposta.js`
(serverless Vercel) e por um middleware do Vite (dev). Modelo `gemini-2.5-flash`; chave só no
servidor.

**Env (NUNCA versionar):** `.env` (de `.env.example`): `VITE_FIREBASE_*` + `GEMINI_API_KEY`.
Cadastrar as MESMAS na Vercel. Projeto Firebase institucional: `revisao-minuta-cbmro-6f248`.
Testar no celular: `cloudflared tunnel --url http://localhost:5173 --protocol http2`.

## graphify

Grafo de conhecimento em `graphify-out/`. Para perguntas sobre o código, rode
`graphify query "<pergunta>"` (ou `path`/`explain`) antes de grep amplo; use
`graphify-out/wiki/index.md` para navegação e `GRAPH_REPORT.md` só para visão de
arquitetura. Após alterar código, `graphify update .` (AST, sem custo de API).
