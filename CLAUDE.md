# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Visão geral

Portal de Legislação dos Corpos de Bombeiros Militares — SPA React/Vite que compara
legislações (organização básica, regimentos internos, organogramas, quadros de efetivo)
dos CBMs estaduais do Brasil, com identidade visual do CBMRO. 27 CBMs mapeados,
37 documentos legais.

## Comandos

```bash
npm install              # instalar dependências
npm run dev              # servidor de desenvolvimento em http://localhost:5173
npm run build            # build de produção (Vite/Rollup -> dist/)
npm run preview          # pré-visualizar o build

# Regenerar dados (Python; pypdf instalado em AppData/Roaming/Python314)
python scripts/convert_to_markdown.py      # PDFs em "LEGISLAÇÃO CBMS/" -> database/markdown/*.md
python scripts/build_organs_detail.py      # detail_data_g*.py + detail_cargos_g*.py -> database/organs_detail/<id>.json
python scripts/build_states_data.py        # database/markdown/*.md + organs_detail/*.json -> database/states_data.json
python scripts/build_dpo_cot_comparison.py # organs_detail/*.json -> database/comparativo_dpo_cot.json (aba "DPO × COT")
python scripts/build_minuta_comparison.py    # organs_detail/*.json + comparativo_dpo_cot.json + minuta_enrichment.py + lob_enrichment.py -> database/comparativo_minuta.json (página /comparar "Subsídio à Minuta")
python scripts/build_minuta_structure.py   # organs_detail/ro.json + minuta_enrichment.py -> database/minuta_structure.json (wizard /minuta + commandChart p/ /minuta-diagramas)
```

> ORDEM IMPORTA: `build_organs_detail.py` deve rodar ANTES de `build_states_data.py`, pois
> este último enriquece a árvore do organograma com as subdivisões (desdobramentos) gravadas
> nos JSON de detalhamento. `build_minuta_comparison.py` depende de `build_dpo_cot_comparison.py`
> e de `build_organs_detail.py` (lê `comparativo_dpo_cot.json` e os `organs_detail/*.json`).

Não há suíte de testes nem linter configurados.

## Arquitetura

### Camada de dados (pipeline Python, executado offline)
O frontend nunca lê PDFs diretamente. Os dados passam por uma pipeline de geração:

1. **PDFs** em `LEGISLAÇÃO CBMS/` (originais, nomes com acento — ex.: `Roraíma - ...pdf`).
2. `convert_to_markdown.py` extrai texto via pypdf para `database/markdown/*.md`.
3. `build_states_data.py` faz parsing dos `.md` e produz **`database/states_data.json`**,
   a fonte única consumida por quase todas as páginas. O dicionário `STATE_META` no topo
   desse script é o mapa canônico estado→{id, abbr, region, cbm}; o `id` minúsculo
   (ex.: `ro`, `df`) é a chave usada em rotas e nomes de arquivo.
4. `build_organs_detail.py` agrega os dicts Python em `scripts/detail_data_g1.py`…`g5.py`
   (estrutura/órgãos) e **mescla** os cargos de `scripts/detail_cargos_g1.py`…`g5.py`
   (cada órgão recebe `cargos[]`: cargo, subordinadoA, requisito/posto, desdobramentos,
   atribuições — via `merge_cargos()`, casando por id de órgão ou por "Nome | SIGLA").
   Gera um **`database/organs_detail/<id>.json`** por estado.
5. `build_states_data.py` também ENRIQUECE a árvore do organograma: a função
   `enrich_tree_from_detail()` lê os JSON de detalhamento e (a) adiciona as subdivisões
   (campo `desdobramentos`) como nós-filhos (marcados com `_reg: true`), surfando a
   estrutura do Regimento no próprio organograma; (b) **carimba cada nó com `detailId`**
   — o id do órgão de detalhamento correspondente, resolvido por nome canônico/sigla/tokens
   (sinônimos Comandante↔Comando, Diretor↔Diretoria etc.) — para o frontend abrir o painel
   de detalhe certo mesmo quando o nome na árvore difere do nome no detalhamento. Por isso
   a ordem de execução importa.

Curadoria manual vs. automática:
- Organogramas curados à mão vivem em `scripts/curated_organs*.py` (`curated_organs.py` +
  `_p2` + `_p3`) — hoje cobrem **os 27 estados**, mas a PROFUNDIDADE varia muito
  (ex.: RO ~194 nós, MT ~161; SP ~7 nós, RN ~12 são stubs rasos). O flag `stats.curated`
  fica `true` para todos por terem árvore ali; não significa curadoria profunda. Ver
  `docs/BACKLOG_CURADORIA.md` para o ranking de qualidade por estado.
- `ro.json` e `ac.json` de detalhamento são escritos à mão; os demais 24 são gerados.
- Estados sem curadoria profunda têm extração automática e podem conter imprecisões.
- Estados com LOB + Regimento Interno (AL, AM, DF, GO, MT, PR, PA, RS, SE) têm lógica de
  unificação dos dois documentos.
- Atribuições de comando transcritas VERBATIM (texto integral dos artigos, com inciso) nos
  estados cujas leis ENUMERAM atribuições por cargo: AL, AM, DF, ES, MT, PA, PR (nos
  `detail_cargos_g*.py`). Os demais têm leis em prosa/finalidade ou regulamento de serviço
  diário (GO, SE) — sem listas enumeráveis; mantêm-se fiéis ao texto, sem invenção.

Ao editar dados de um estado, altere os `detail_data_g*.py` / `curated_organs*.py` e
**reexecute o script** correspondente — não edite os JSON gerados diretamente (serão
sobrescritos). Os arquivos escritos à mão (`ro.json`, `ac.json`) são a exceção.

### Frontend (React)
- Entrada: `src/main.jsx` (BrowserRouter) → `src/App.jsx` define o layout (Header + Sidebar
  + main) e as rotas. O array `NAV` em `App.jsx` controla a navegação. No desktop (≥901px)
  a sidebar recolhe em trilha de ícones (264px→76px) ao clicar em qualquer aba (estado
  `collapsed`, separado do `navOpen` da gaveta mobile); o logo "Portal CBM" alterna de volta.
  Regras em `@media (min-width: 901px) .app-shell.nav-collapsed` no `index.css`.
- Rotas: `/` (Dashboard), `/estados` (StatesList), `/estados/:stateId` (StateDetail),
  `/legislacoes` (Legislations), `/comparar` (MinutaComparator, "Subsídio à Minuta"),
  `/busca` (Search), `/minuta` (MinutaWizard), `/minuta-diagramas` (MinutaDiagrams).
- As páginas fazem `fetch('/database/states_data.json')`; `StateDetail` também busca
  `/database/organs_detail/${stateId}.json`. O `stateId` da URL corresponde ao `id` do
  `STATE_META`.
- O **Dashboard** mostra só a Visão Geral (estatísticas); as antigas abas "Comparativo de
  Cargos" e "DPO × COT" foram removidas junto com seus componentes.
- `/comparar` (`src/pages/MinutaComparator.jsx`, "Subsídio à Minuta") lê
  `database/comparativo_minuta.json` (gerado por `scripts/build_minuta_comparison.py`) e
  espelha os 26 órgãos da LOB + Guarnição (27 no total), comparando RO × estados em **3 colunas**:
  CBMRO (referência), **LOB do estado** (`state.lobOrgans`/`lobProvenance`) e **LOB + RI**
  (`state.organs`/`provenance`, a estrutura enriquecida com as demais fontes), com proveniência
  curado/automático por coluna (badge). A coluna LOB pura é alimentada por `scripts/lob_enrichment.py`
  (`LOB_ENRICHMENT[(organ_key, state_id)]`, curadoria verbatim — finalidade/caput de 1 frase +
  incisos — das 27 Leis de Organização Básica; cobre os 26 órgãos × 26 estados não-RO; documentada
  em `docs/ENRIQUECIMENTO_MINUTA.md`, seção "Camada LOB"). A coluna LOB + RI é a UNIÃO dessa camada
  LOB com a camada curada de `comparativo_dpo_cot.json` (DPO/COT) + as competências verbatim de
  `minuta_enrichment.py` (`ENRICHMENT_ORGAN`, pivotadas por fonte; a curadoria dos 15 órgãos da
  Frente 2 — Direção Geral/Setorial/Colegiada, Assessoramento/Apoio e Correição — segue documentada
  em `docs/ENRIQUECIMENTO_MINUTA.md`) + a Guarnição (CBMSE); a camada automática casa por
  palavra-chave (`AUTO_MATCH_KEYWORDS` em `minuta_comparison_lib.py`) quando não há curadoria. A
  lista "Órgãos da minuta" na barra lateral segue a ORDEM e a PROFUNDIDADE hierárquica do
  organograma (DFS da cadeia de comando), indentada por `depth` — esse campo é gravado no JSON
  por `build_minuta_comparison.py` via `build_minuta_structure.command_order`, mantendo a lista
  em sincronia com o `commandChart`. Só entram estados com dado correspondente; busca filtra a
  matriz. Substitui o antigo `Compare.jsx` (removido), que comparava por região/similaridade.
- Componentes-chave: `Organogram.jsx` (árvore expansível/colapsável) e `OrgDetail.jsx`
  (painel lateral de detalhamento). `CargoComparator.jsx` e `OrgaosOperacionaisComparator.jsx`
  foram removidos junto com as abas do Dashboard.
- `StateDetail.handleSelectOrgan` resolve o detalhe pelo `detailId` carimbado no build
  (prioritário) e só então recorre a id/nome/sigla — por isso os painéis de cargos e
  atribuições aparecem mesmo quando o nome do nó da árvore difere do detalhamento.
- Exportação PDF (`MinutaComparator.jsx` + `@media print` no `index.css`): `window.print()`
  com título centralizado (`.print-only-title`), a barra de controles e o sumário ocultos na
  impressão (`.page-body` em modo bloco) e a matriz (`.oc-matrix-table`) em fonte reduzida
  para caber em Paisagem.
- Estilo: CSS único em `src/index.css`. Identidade CBMRO (tema claro): cabeçalho vermelho
  `#c8102e`, sidebar navy `#121d3d`, conteúdo `#eef1f6`. Tipografia Outfit (títulos) + Inter.
- Ícones: `lucide-react`.

### Wizard de Minuta de Regimento Interno (`/minuta`)
Gera, em `.docx` client-side, uma minuta hierárquica única de RI do CBMRO cobrindo toda a
estrutura da LOB (do Comando-Geral à menor fração), em vez de apenas comparar o que outros
estados fizeram.

- `scripts/build_minuta_structure.py` lê **diretamente** `database/organs_detail/ro.json`
  (não mais o `comparativo_dpo_cot.json`) e percorre os órgãos na ordem de subordinação do
  RO: Preliminares + Estrutura + os **26 órgãos da LOB** (Direção Geral/Colegiada/Setorial/
  Regional, Assessoramento, Apoio ao Comando-Geral/Subcomando-Geral, Execução Ordinária/
  Especializada Terrestre/Aérea/Conveniada Municipal, Correição — agrupados em
  `build_estrutura_chapter()` via `CATEGORY_LABELS`/`APOIO_LABELS`) + capítulo da
  **Guarnição de Serviço Operacional** (menor fração) + Finais — gerando
  `database/minuta_structure.json` (`{title, chapters:[{kind: prose|incisos|organ, sections:[...]}]}`).
  `cg` (Comando-Geral) é a raiz real da árvore de comando (`commandChart`); `find_parent`
  resolve `subordinadoA` por sigla de órgão ou, via `ROLE_TO_ORGAN`, por nome de cargo
  (ex.: "Subcomandante-Geral" → órgão `cg`).
- `scripts/minuta_enrichment.py` traz o enriquecimento curado VERBATIM de outros CBMs,
  rotulado por fonte: `ENRICHMENT` (por cargo/função — hoje só CBMAL) e `ENRICHMENT_ORGAN`
  (por órgão/competência — AL, MT, PR, SC, DF, SP, BA, CE, PE, ES, PA) mais
  `GUARNICAO_CHAPTER` (nó estrutural novo, sem equivalente no `ro.json`, subsidiado
  integralmente pelo RISD do CBMSE). Critério, fontes e descartes (com motivo) em
  **`docs/ENRIQUECIMENTO_MINUTA.md`** — só entra competência **enumerada e verbatim**;
  ao ampliar o enriquecimento, editar esse script e reexecutar `build_minuta_structure.py`.
  `ro.json` nunca é tocado por esse enriquecimento (preserva o Comparador de Cargos).
- `src/lib/minutaArticles.js` — `buildArticles(structure, edits, isExcluded)` faz a
  numeração contínua de artigos e capítulos/seções em algarismos romanos a partir do JSON
  gerado; testado em `minutaArticles.test.js` (`node --test`).
- `src/pages/MinutaWizard.jsx` — documento único rolável com sidebar de sumário (scroll
  para capítulo/seção), curadoria por inciso (`excluded: Set<"editId#index">`, com filtro em
  lote por fonte) e edição de texto por seção em modo avançado; exporta o mesmo resultado
  filtrado para `.docx` via `docx`.

### Diagramas da Minuta (`/minuta-diagramas`)
Página que apresenta dois diagramas da minuta, lendo o mesmo `minuta_structure.json`:
- **Organograma** (`src/components/MinutaOrgChart.jsx`) — cadeia de comando dos 26 órgãos da
  LOB + Guarnição, caixas-e-linhas em CSS puro (sem lib), a partir do campo `commandChart`
  gerado por `build_minuta_structure.py` (árvore derivada de `subordinadoA` no `ro.json`, com
  `cg` — Comando-Geral — como raiz REAL, não mais sintética, quando há uma única raiz na
  cadeia; só cai numa raiz sintética/placeholder para 0 ou 2+ raízes desconexas; GBM como
  ramo próprio sob o CRBM — Execução Conveniada Municipal — via `COMMAND_PARENT_OVERRIDE`, e a
  Guarnição de Serviço Operacional como folha da cadeia de frações do BBM: BBM → Companhia
  (Cia BM) → Pelotão (Pel BM) → Guarnição, via `BBM_FRACTION_CHAIN`, com Cia/Pel como nós
  estruturais não-clicáveis). A árvore é **dinâmica**: cada nó com filhos tem botão −/+
  (`.moc-toggle`) que expande/recolhe a subárvore (estado local por nó; a raiz — real ou
  sintética — sempre aberta via a prop `isRoot`; demais nós iniciam recolhidos no 1º nível).
  Controles "Expandir/Recolher tudo" remontam a árvore via `key`+`defaultExpanded`; a
  impressão expande tudo antes do `window.print()`.
- **Mapa mental** (`src/components/MinutaMindMap.jsx`) — grade de cartões, um por capítulo.
Ambos clicáveis: abrem um painel lateral com as seções/competências do capítulo. Exporta via
`window.print()` (`@media print`, Paisagem), ocultando navegação/controles/painel.

A lista "Órgãos da minuta" do `/comparar` reusa o mesmo padrão: `MinutaComparator.jsx`
reconstrói a árvore a partir do `depth` (`buildOrganTree`) e renderiza `OrgTreeNode` com
botão −/+ (`.oc-org-toggle`), iniciando recolhida no 1º nível; clicar no item seleciona o órgão.

### Servir dados: middleware (dev) + cópia no build (produção)
`vite.config.js` registra DOIS plugins customizados:
- `serveDatabase` (via `configureServer`, só no **dev server**): expõe
  `/database/*` → pasta `database/` (JSON/MD) e `/legislacao-pdf/*` → `LEGISLAÇÃO CBMS/` (PDFs).
- `copyDatabaseOnBuild` (via `closeBundle`, no **build de produção**): copia `database/`
  → `dist/database/` e `LEGISLAÇÃO CBMS/` → `dist/legislacao-pdf/`, para que os
  `fetch('/database/...')` e os links de PDF funcionem no `dist/` servido estaticamente.

Essas pastas ficam FORA de `public/` (são grandes e regeneradas pela pipeline), por isso
o tratamento é feito pelos plugins acima — não pelo mecanismo padrão de assets do Vite.

### Assets estáticos
`public/` é servida na raiz (ex.: brasão referenciado como `/BrasaoCBMRO2D-COMPLETO.png`
em `App.jsx`, com fallback para `/brasao-cbmro.svg`).
