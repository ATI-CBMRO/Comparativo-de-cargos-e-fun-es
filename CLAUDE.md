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
python scripts/build_minuta_structure.py   # organs_detail/ro.json + minuta_enrichment.py -> database/minuta_structure.json (wizard /minuta)
```

> ORDEM IMPORTA: `build_organs_detail.py` deve rodar ANTES de `build_states_data.py`, pois
> este último enriquece a árvore do organograma com as subdivisões (desdobramentos) gravadas
> nos JSON de detalhamento.

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
  + main) e as rotas. O array `NAV` em `App.jsx` controla a navegação.
- Rotas: `/` (Dashboard), `/estados` (StatesList), `/estados/:stateId` (StateDetail),
  `/legislacoes` (Legislations), `/comparar` (Compare), `/busca` (Search), `/minuta`
  (MinutaWizard).
- As páginas fazem `fetch('/database/states_data.json')`; `StateDetail` também busca
  `/database/organs_detail/${stateId}.json`. O `stateId` da URL corresponde ao `id` do
  `STATE_META`.
- O **Dashboard** tem abas: "Visão Geral" (estatísticas), "Comparativo de Cargos"
  (`CargoComparator.jsx`) e "DPO × COT" (`OrgaosOperacionaisComparator.jsx`).
  - "Comparativo de Cargos": confronta um cargo do CBMRO (`ro.json` é a referência canônica)
    com vários estados ao mesmo tempo, em tabela de larga escala com coluna do RO e cabeçalho
    fixos (sticky). O casamento de cargos usa normalização tolerante (mesma lógica de sinônimos
    do `detailId`); sem correspondência, exibe "não localizado". Fetches em paralelo + cache.
  - "DPO × COT": compara, nos 27 CBMs, os órgãos equivalentes à DPO (Diretoria de Planejamento
    Operacional) e ao COT (Comando de Operações Técnicas) da minuta de LOB do CBMRO — casamento
    por FUNÇÃO (a nomenclatura varia: COB/Comando Operacional/Diretoria Operacional ≈ DPO;
    CAT/DAT/DST/DSCI/CSCI ≈ COT). Consome `database/comparativo_dpo_cot.json` (gerado por
    `scripts/build_dpo_cot_comparison.py`, que encoda o MAPEAMENTO curado de ids de órgão por
    estado e extrai os textos VERBATIM dos `organs_detail/*.json`). Tabela com estados nas linhas,
    coluna do CBM e cabeçalho sticky; alterna DPO/COT; estados sem órgão discriminado (ex.: DF no
    COT) exibem nota explicativa. Reexecutar o script se editar o mapeamento ou os detalhamentos.
- Componentes-chave: `Organogram.jsx` (árvore expansível/colapsável), `OrgDetail.jsx`
  (painel lateral de detalhamento) e `CargoComparator.jsx` (comparador de cargos no Dashboard).
- `StateDetail.handleSelectOrgan` resolve o detalhe pelo `detailId` carimbado no build
  (prioritário) e só então recorre a id/nome/sigla — por isso os painéis de cargos e
  atribuições aparecem mesmo quando o nome do nó da árvore difere do detalhamento.
- Exportação PDF (`Compare.jsx` + `@media print` no `index.css`): `window.print()` com
  cabeçalho institucional, moldura vermelha repetida por folha (`.print-frame` em `inset:0`,
  com respiro interno para não cortar texto) e a tabela de estatísticas em página própria.
  Imprimir em Paisagem, margens "Padrão".
- Estilo: CSS único em `src/index.css`. Identidade CBMRO (tema claro): cabeçalho vermelho
  `#c8102e`, sidebar navy `#121d3d`, conteúdo `#eef1f6`. Tipografia Outfit (títulos) + Inter.
- Ícones: `lucide-react`.

### Wizard de Minuta de Regimento Interno (`/minuta`)
Gera, em `.docx` client-side, uma minuta hierárquica única de RI operacional do CBMRO
(do Comando-Geral à menor fração), em vez de apenas comparar o que outros estados fizeram.

- `scripts/build_minuta_structure.py` lê **diretamente** `database/organs_detail/ro.json`
  (não mais o `comparativo_dpo_cot.json`) e percorre os órgãos na ordem de subordinação do
  RO: Preliminares + Estrutura + 10 órgãos (dpo, cot, doe, crbm, bbm, cibm, gbm, bbs, bifea,
  boa) + capítulo da **Guarnição de Serviço Operacional** (menor fração) + Finais — gerando
  `database/minuta_structure.json` (`{title, chapters:[{kind: prose|incisos|organ, sections:[...]}]}`).
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
