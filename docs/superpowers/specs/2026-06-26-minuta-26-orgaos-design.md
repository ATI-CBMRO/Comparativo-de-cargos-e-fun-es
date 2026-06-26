# Expandir a minuta de RI para os 26 órgãos da LOB — Design

**Data:** 2026-06-26
**Status:** Aprovado no brainstorming, aguardando revisão do spec

## Problema

A minuta de Regimento Interno (`/minuta`, `database/minuta_structure.json`, gerada por
`scripts/build_minuta_structure.py`) hoje cobre só os **11 órgãos operacionais** da LOB do
CBMRO (DPO, DOE, COT, CRBM, BBM, CIBM, CAT, BBS, BIFEA, BOA, GBM) + o capítulo estrutural da
Guarnição de Serviço Operacional. Mas `database/organs_detail/ro.json` já tem **26 órgãos**
curados — toda a estrutura da LOB (Art. 11 a 50), incluindo o lado administrativo: Comando
Geral, CONDEG, DEPDEC, Diretoria de Pessoal, Ensino, Planejamento/Orçamento/Finanças, Saúde,
Logística, Coordenadorias de Inteligência/Comunicação/Informática, Corregedoria-Geral,
Gabinetes, Assessorias e Ajudância-Geral. A minuta de RI deve cobrir a LOB **inteira**, não só
a cadeia operacional.

## Contexto maior

Este é a **Frente 1** de um redesenho em duas frentes:
- **Frente 1 (este spec):** expandir `build_minuta_structure.py` (e, por consequência,
  `/minuta` e `/minuta-diagramas`) para os 26 órgãos.
- **Frente 2 (próxima, spec separado):** reconstruir o comparativo `/comparar` (LOB×LOB) para
  cobrir os mesmos 26 órgãos, reusando a mesma lista/ordem produzida nesta frente, e
  preservando o mapa curado DPO/COT (`build_dpo_cot_comparison.py`) sem alteração — ele
  continua alimentando o enriquecimento da minuta desses dois órgãos.

## Objetivo

`ORGAN_ORDER` em `scripts/build_minuta_structure.py` passa de 11 para **26 entradas**,
cobrindo todos os órgãos de `organs_detail/ro.json`. Os dados (atribuições, cargos,
desdobramentos) já existem nesse JSON — não há nova curadoria de conteúdo, só a inclusão dos
órgãos na lista e o ajuste da árvore de comando para acomodá-los corretamente.

## Arquitetura

### Lista de órgãos (`ORGAN_ORDER`)

Adicionar as 15 entradas que faltam, cada uma com `(organ_key, "DO(A) <TÍTULO DO CAPÍTULO>",
artigo_definido)`, na mesma forma das 11 atuais:

| organ_key | Título do capítulo | art. |
|---|---|---|
| `cg` | DO COMANDO GERAL (CG) | O |
| `condeg` | DO CONSELHO DELIBERATIVO DE ESTRATÉGIA E GESTÃO (CONDEG) | O |
| `depdec` | DA DIRETORIA ESTADUAL DE PROTEÇÃO E DEFESA CIVIL (DEPDEC) | A |
| `dp` | DA DIRETORIA DE PESSOAL (DP) | A |
| `deei` | DA DIRETORIA DE EDUCAÇÃO, ENSINO E INSTRUÇÃO (DEEI) | A |
| `dpof` | DA DIRETORIA DE PLANEJAMENTO, ORÇAMENTO E FINANÇAS (DPOF) | A |
| `dsap` | DA DIRETORIA DE SAÚDE E ASSISTÊNCIA AO PESSOAL (DSAP) | A |
| `dlog` | DA DIRETORIA DE LOGÍSTICA (DLOG) | A |
| `cint` | DA COORDENADORIA DE INTELIGÊNCIA (CINT) | A |
| `ccs` | DA COORDENADORIA DE COMUNICAÇÃO SOCIAL (CCS) | A |
| `cinf` | DA COORDENADORIA DE INFORMÁTICA (CINF) | A |
| `corregedoria` | DA CORREGEDORIA-GERAL | A |
| `assessorias` | DAS ASSESSORIAS | As |
| `gab-cg` | DO GABINETE DO COMANDANTE-GERAL | O |
| `ag` | DA AJUDÂNCIA-GERAL (AG) | A |

A ordem final na lista (e, por consequência, a ordem dos capítulos no documento) segue a
ordem dos artigos da LOB (11→50): `cg, condeg, depdec, dp, deei, dpof, dsap, dlog, dpo, doe,
cot, cat, cint, ccs, cinf, crbm, bbm, cibm, bbs, bifea, boa, gbm, corregedoria, assessorias,
gab-cg, ag` — mantendo a ordem relativa das 11 já existentes intacta entre si.

### Resolução de hierarquia (`build_command_chart` / `find_parent`)

O casamento atual é só por sigla: procura a sigla de outro órgão do conjunto dentro do texto
de `subordinadoA`. Isso funciona para os 11 atuais (ex.: COT → "Diretoria de Planejamento
Operacional (DPO)" casa a sigla DPO). Quebra para 7 dos novos, cujo `subordinadoA` referencia
um **cargo interno do órgão `cg`**, não uma sigla de órgão:

- `dp`, `deei`, `dpof`, `dsap`, `dlog`, `ccs`, `cinf` → `subordinadoA: "Chefe do Estado-Maior
  Geral"` (cargo dentro de `cg`, não um órgão próprio).
- `condeg`, `cint`, `gab-cg` → `subordinadoA: "Comandante-Geral"` (idem).
- `corregedoria`, `ag` → `subordinadoA: "Subcomandante-Geral"` (idem).
- `depdec` → `subordinadoA: "Comandante-Geral (Diretor-Geral nato)"` (idem, com sufixo).
- `assessorias` → `subordinadoA: "Comandante-Geral"` (idem).

**Fix:** adicionar um mapa `ROLE_TO_ORGAN` com esses três papéis (textos normalizados,
prefixo-match para tolerar sufixos como "(Diretor-Geral nato)") apontando para `"cg"`. Em
`find_parent`, se o casamento por sigla não encontrar nada, tentar `ROLE_TO_ORGAN` antes de
declarar raiz.

`cg` em si tem `subordinadoA: "Governador do Estado de Rondônia"` — fora do conjunto, vira
**raiz real**. A raiz sintética hoje hardcoded (`{"label": "Subcomandante-Geral", "synthetic":
True, ...}`) deixa de ser necessária: `cg` passa a ser a única raiz da árvore, com seu próprio
`chapterId` (clicável, como qualquer outro órgão).

**Efeito colateral correto em `dpo`/`doe`** (já existentes, sem mudança de dados): ambos têm
`subordinadoA: "Subcomandante-Geral"` — hoje, sem `cg` no conjunto, isso não casa nenhuma
sigla e os dois entram como filhos diretos da raiz sintética. Com o alias
`"Subcomandante-Geral" → cg`, passam a pendurar corretamente **sob `cg`** — mais correto que
o estado atual, e é a mesma regra aplicada a `corregedoria`/`ag`, sem código especial extra.

`COMMAND_PARENT_OVERRIDE = {"gbm": "crbm"}` continua valendo sem mudança.

### Textos introdutórios

- `TITLE` ("DO REGIMENTO INTERNO DA ESTRUTURA OPERACIONAL DO CBMRO") perde "OPERACIONAL":
  passa a "DO REGIMENTO INTERNO DO CORPO DE BOMBEIROS MILITAR DO ESTADO DE RONDÔNIA (CBMRO)".
- `build_preliminares_chapter()`: o texto que diz "estrutura operacional" e "subordina-se ao
  Comandante-Geral por intermédio do Subcomandante-Geral" passa a descrever a estrutura
  **completa** da LOB, do Comando-Geral à menor fração.

### O que não muda

- `organs_detail/ro.json` — fonte já completa, não é tocado.
- `GUARNICAO_CHAPTER`, `BBM_FRACTION_CHAIN`, `COMMAND_PARENT_OVERRIDE["gbm"]` — sem alteração.
- `minuta_enrichment.py` — `enrich_for`/`enrich_organ_for` já retornam `[]` para qualquer
  `organ_key` sem entrada cadastrada (confirmado por leitura do código); os 15 novos órgãos
  simplesmente não recebem enriquecimento de outros estados, o que é o comportamento correto
  por ora (nenhum dos specs de enrichment cobre esses órgãos administrativos).
- `build_organ_chapter()` — genérico, já funciona para qualquer órgão com a forma
  `atribuicoes`/`cargos`/`desdobramentos` usada em `ro.json`.
- `src/lib/minutaArticles.js`, `MinutaWizard.jsx`, `MinutaOrgChart.jsx`, `MinutaMindMap.jsx` —
  todos consomem a estrutura genericamente a partir do JSON; nenhuma mudança de código
  esperada, só verificação visual com a árvore maior.
- O comparativo `/comparar` — fora de escopo (Frente 2).

## Riscos e mitigação

- **`find_parent` pode lançar `ValueError`** se `subordinadoA` de algum órgão casar mais de
  uma sigla simultaneamente — risco pré-existente, não introduzido por esta mudança; o
  conjunto maior de siglas aumenta a chance marginalmente. Mitigação: rodar o build e observar
  qualquer exceção; se ocorrer, é sinal de ambiguidade real no texto a tratar caso a caso.
- **Árvore mais funda/larga nos diagramas** (`/minuta-diagramas`): mais nós sob `cg`.
  Mitigação: já existe colapsar/expandir por nó; verificação visual cobre isso.
- **Numeração de artigos maior**: o documento da minuta cresce de ~14 para ~29 capítulos.
  Mitigação: `minutaArticles.js` já numera dinamicamente a partir da lista de capítulos —
  sem hardcode de quantidade; suíte `minutaArticles.test.js` cobre a lógica de numeração com
  fixtures que não dependem do nº de capítulos.

## Testes / verificação

- Regenerar `python scripts/build_minuta_structure.py`; conferir que `minuta_structure.json`
  tem 26 capítulos `kind:"organ"` (mais Guarnição) e que `commandChart` tem `cg` como única
  raiz, sem exceção lançada.
- Conferir visualmente em `/minuta-diagramas`: organograma mostra `cg` no topo, os 15 novos
  órgãos pendurados corretamente (a maioria sob `cg`, exceto `dpo`/`doe` que ficam sob
  `cg`→ENTRE si conforme já casam por sigla hoje — confirmar na árvore gerada).
- Conferir `/minuta`: sumário lateral lista os 26 capítulos na ordem correta; abrir 2-3
  capítulos novos (ex.: Diretoria de Pessoal) e confirmar que atribuições/cargos aparecem.
- Rodar `node --test` (suíte `minutaArticles.test.js`) — não deve quebrar.
- Exportar PDF (`window.print()`) de `/minuta-diagramas` para confirmar que a árvore maior
  ainda renderiza em Paisagem sem cortar conteúdo (scroll/paginação aceitável).

## Fora de escopo

- Qualquer mudança em `/comparar` ou `build_minuta_comparison.py` (Frente 2).
- Re-curadoria de conteúdo de `organs_detail/ro.json` — já está completo.
- Enriquecimento verbatim de outros estados para os 15 novos órgãos administrativos (não há
  fonte cadastrada hoje; pode ser um spec futuro separado).
