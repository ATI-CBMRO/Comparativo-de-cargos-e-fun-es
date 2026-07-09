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

# Regenerar dados (Python 3.10+ — os scripts usam `int | None`; pypdf instalado em
# AppData/Roaming/Python314. Em Mac com só o Python 3.9 do sistema, instalar uma versão
# mais nova, ex.: `brew install python@3.12`, e chamar `python3.12` no lugar de `python`)
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
  `/busca` (Search), `/minuta` (MinutaWizard), `/minuta-diagramas` (MinutaDiagrams),
  `/minuta/comparativo-ri` (RIComparator), `/minuta/revisao` (MinutaRevisao) e
  `/minuta/deliberacao` (MinutaDeliberacao).
- As páginas fazem `fetch('/database/states_data.json')`; `StateDetail` também busca
  `/database/organs_detail/${stateId}.json`. O `stateId` da URL corresponde ao `id` do
  `STATE_META`.
- O **Dashboard** mostra só a Visão Geral (estatísticas); as antigas abas "Comparativo de
  Cargos" e "DPO × COT" foram removidas junto com seus componentes.
### Tabela de cobertura no Acervo Legal (jul/2026)
A página Acervo Legal (`src/pages/Legislations.jsx`) mostra, no topo, uma
tabela-resumo `estado × tipo` (LOB / Regimento Interno / Regulamento de
Serviço) — lógica pura em `src/lib/acervoCoverage.js` (testada), apresentação
em `src/components/AcervoCoverageTable.jsx`. A coluna "Regulamento de Serviço"
funde os tipos `Regulamento Geral` e `Regimento de Serviços`. O selo ✓/⚠ por
célula reusa o campo `typeVerified` dos dados (✓ = conferido por conteúdo, ⚠ =
só por nome de arquivo). A tabela NÃO é filtrada pela busca da página (é
panorama fixo dos 27); a busca continua governando só a lista detalhada abaixo.
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
- `/minuta/comparativo-ri` (`src/pages/RIComparator.jsx`, "Comparativo de RI") compara, capítulo a
  capítulo, a minuta do CBMRO (coluna central, leitura, via `buildTargets` do `minuta_structure.json`)
  com o órgão equivalente no **Regimento Interno** dos 7 estados que de fato possuem RI organizacional
  no acervo (al, df, mt, pr, pa, rs, se; `RI_STATE_IDS`) — UM estado por vez, por pills. NÃO inclui
  am (só LOB+Quadro) nem go (LOB+QOD+"Regimento dos Serviços Interno e Operacional", que é regimento
  de serviço, não RI). Diferente do `/comparar`, esta página mostra **só a camada de RI, sem
  o enriquecimento da LOB**: lê o campo `riOrgans`/`riProvenance`/`riSourceLabel` do
  `comparativo_minuta.json` (snapshot da coluna 3 gravado por `build_minuta_comparison.py` ANTES do
  merge da LOB — camadas DPO/COT curado + `ENRICHMENT_ORGAN` + Guarnição + auto por palavra-chave em
  organs_detail não-LOB). A coluna `organs` (LOB + RI) segue intacta para o `/comparar`. Lógica pura
  em `src/lib/riComparison.js` (testada): `indexComparativo`, `organKeyOfChapter`, `statesWithData`
  (filtra por `riOrgans` não vazio), `pickState`. Capítulos sem `organKey` (Preliminares/Estrutura/
  Finais) e a Guarnição (sem RI mapeado) exibem avisos de "sem equivalente".
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

### Revisão e Deliberação colaborativa do CONDEG (`/minuta/revisao` e `/minuta/deliberacao`) — LEGADO
Fluxo colaborativo do CONDEG sobre a minuta de RI, em duas fases, lendo o mesmo
`minuta_structure.json`. **Protótipo de frontend**, hoje **fora do menu** (retirado do array
`NAV` em `App.jsx`) — o módulo Firebase real (`/revisao`, seção abaixo) é o fluxo oficial de
produção. As rotas continuam respondendo por URL direta e o código não foi apagado: o sumário
de capítulos (`ChapterRail.jsx`) foi replicado/melhorado em `/revisao`, e `minutaTargets.js`,
`minutaConsolidation.js` e `minutaDocx.js` seguem reusados pelo módulo real. Aqui tudo roda
sobre dados simulados, por uma camada de dados ISOLADA e trocável.

- **Camada de dados** (`src/lib/suggestionsStore.js`): `createSuggestionsStore(storage)`, API
  assíncrona (Promise) sobre `localStorage`, com `MOCK_USERS` (coronéis fictícios) e a "sessão"
  simulada. Quando o backend real existir, criar um `apiBackend` com a MESMA assinatura (fetch +
  sessão autenticada) e trocar a instância exportada — as telas não mudam.
- **Fase 1 — `/minuta/revisao`** (`src/pages/MinutaRevisao.jsx`): 3 colunas — trilha de capítulos
  (`ChapterRail.jsx`, filtro + contadores) · documento com marcadores · painel lateral
  (`SuggestionPanel.jsx` + `SuggestionCard.jsx`, "Antes/Depois"). Coronéis propõem incluir/editar/
  remover incisos e seções (o compositor pré-preenche o texto vigente ao editar); todos veem as
  sugestões de todos, com autoria + Apoiar/Comentar. Trilha e painel ficam `sticky` (abaixo do
  header fixo) enquanto só o documento central rola.
- **Fase 2 — `/minuta/deliberacao`** (`src/pages/MinutaDeliberacao.jsx`): lista de pendências
  (itens agrupados por `itemKeyOf` = `editId#incisoIndex`) → fila de revisão guiada (Aceitar/
  Rejeitar, texto final por item, "Aprovar e avançar") → `.docx` consolidado.
- **Alvos/consolidação/export**: `src/lib/minutaTargets.js` (`buildTargets`, deriva
  capítulo→seção→inciso de `buildArticles`), `src/lib/minutaConsolidation.js`
  (`applyResolutionsToEdits` — a minuta final usa o **texto final APROVADO** por item, não só as
  sugestões aceitas) e `src/lib/minutaDocx.js` (`buildMinutaBlob`, extraído do `MinutaWizard` e
  reusado pela Fase 2). Identidade simulada em `src/components/IdentityBar.jsx`.
- **Lógica pura testada** com `node --test`: `suggestionsStore.test.js`, `minutaTargets.test.js`,
  `minutaConsolidation.test.js`. Spec/plano em
  `docs/superpowers/{specs,plans}/2026-06-29-minuta-revisao-colaborativa*`.
- Limites intencionais do protótipo: nova-seção e resoluções de seção/prose não entram no `.docx`
  gerado (embora contem no progresso); a colaboração "em tempo real" é simulada trocando de coronel
  no mesmo navegador (sem sync entre máquinas).

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

## Minuta do Regulamento — curadoria (em andamento)

Evolução em curso: gerar a minuta do Regulamento Interno do CBMRO a partir dos
regulamentos de outros estados já no acervo (MT como esqueleto — a LOB de RO seguiu a
de MT —, RN/SE e demais como complemento), e comparar dispositivo a dispositivo. Como
os textos dos estados NÃO casam perfeitamente entre si, a curadoria segue 4 passos por
estado antes de qualquer transcrição (detalhes no plano de execução):

1. `python3 scripts/sugerir_equivalencias.py <uf>` — garimpo automático de candidatos
   por tema (`docs/curadoria/candidatos-<uf>.md`). Feito para os 9 estados.
2. De-para tema→artigos por estado — `docs/curadoria/de-para-<uf>.md` (FEITOS e
   validados para os 9; visão geral em `docs/curadoria/panorama-cobertura.md`,
   inclusive a matriz de cobertura 15 temas × 9 estados e as fontes primárias por tema).
3. Validação humana dos de-paras (concluída em 2026-07-07).
4. **Extração determinística**: `python3 scripts/extrair_regulamentos.py` corta os
   markdowns por "Art. N" e gera `scripts/regulamento_enrichment_<uf>.py` (850 artigos,
   GERADOS — não editar à mão; o mapa artigo→tema vive no próprio extrator).
   `scripts/regulamento_enrichment.py` (mestre) define os 15 THEMES, PRIMARY_SOURCE por
   tema e ADAPTATIONS (CBMMT→CBMRO etc.) e mescla os arquivos por estado.
5. Verificação: `python3 scripts/verificar_verbatim.py` — todo caput/dispositivo deve
   existir literalmente no markdown de origem (compara também fonte "limpa" com o mesmo
   pipeline do extrator e versão sem espaços/hifens, tolerando artefatos de PDF).
6. **Minuta**: `python3 scripts/build_regulamento_structure.py` →
   `database/regulamento_structure.json` (MESMO formato de minuta_structure.json: 15
   capítulos-temas, artigos da fonte primária adaptados p/ RO com original preservado,
   `alternatives` por tema com o texto original dos demais estados). Validação:
   `python3 scripts/test_regulamento_structure.py`. Páginas: `/regulamento` (wizard) e
   `/regulamento/comparar` (comparador por dispositivo).

`scripts/equivalencias_terminologicas.py` é o glossário de sinônimos entre estados
(ex.: "serviço de dia" ≈ "serviço de permanência") usado pelo garimpo.

**Nota de ambiente**: os scripts de dados (ex.: `build_states_data.py`) usam sintaxe
`int | None`, que exige **Python 3.10+**. Em Mac com só o Python 3.9 do sistema, use
`brew install python@3.12` e chame `python3.12` no lugar de `python`/`python3` para
esses scripts. Os scripts NOVOS de curadoria acima (`sugerir_equivalencias.py`,
`equivalencias_terminologicas.py`, `verificar_verbatim.py`) rodam também no Python 3.9.

**Mecanismos de correção descobertos testando manualmente (2026-07-08):**
- `strip_lines` em `CONFIG[<uf>]` (`extrair_regulamentos.py`) — remove linhas-fragmento
  conhecidas ANTES do parse (mesmo espírito de `fake_art_res`). Criado porque um
  cabeçalho de seção quebrado em 2 linhas na conversão do PDF (`RE_NOISE` só reconhece
  a 1ª linha) fazia uma palavra solta grudar no fim do artigo anterior — achado real no
  Art. 53 do RISD-SE. Use quando achar contaminação parecida em outro estado.
- `hasOwnMarker(text)` em `src/lib/minutaArticles.js` — dispositivos que já começam
  com "Parágrafo único"/"§" são unidades legislativas completas, não incisos
  numerados: `normalizeInciso()` os devolve verbatim (sem strip de marcador, sem
  lowercase, sem sufixo de continuação), e `buildArticles()` marca `ownMarker: true`
  no inciso pra as telas pularem o prefixo `romanize(i+1) -`. Relevante pra qualquer
  novo tema/estado do Regulamento que tenha parágrafos (33 dispositivos afetados só
  na curadoria atual).

## ⚠️ Classificação de tipo de documento — auditoria pendente (achado 2026-07-08)

`parse_doc_type()` em `scripts/build_states_data.py` classifica cada documento **só
pelo nome do arquivo** (procura substrings como "regimento interno", "regulamento"),
NUNCA leu o conteúdo. Isso já causou erro confirmado: `database/states_data.json`
mostra **Mato Grosso** e **Sergipe** como `"Regimento Interno"`, mas a curadoria do
Regulamento (que leu o conteúdo de verdade) descobriu que:
- **MT**: o arquivo chamado "Regimento Interno" é na verdade o **Regulamento Geral**
  do CBMMT (Portaria nº 009/BM-8/2013) — é a fonte primária de boa parte dos temas do
  Regulamento por causa disso.
- **SE**: o arquivo é o **RISD** (Regimento Interno dos Serviços Diários) — apesar do
  nome ter "Regimento", funciona como um regulamento de rotina operacional, não como
  regimento de estrutura organizacional.

Essas descobertas ficaram só dentro de `scripts/regulamento_enrichment.py`
(`REGULAMENTO_DOCS`), **nunca foram propagadas de volta pro `states_data.json`** que
o site mostra em `/estados`. RN e GO já foram corrigidos (Bloco B0); MT e SE **ainda
não**. Além disso, **só 9 dos 27 estados** (os do Regulamento) tiveram o conteúdo
lido de verdade — os outros 18 têm classificação 100% baseada em nome de arquivo,
nunca verificada.

**Antes de confiar nessa classificação para qualquer novo recurso** (ex.: uma tabela
LOB × Regimento Interno × Regulamento por estado, pedida pelo Wândrio em 2026-07-08),
tratar isso como pré-requisito: corrigir MT/SE no mínimo, e decidir se os outros 18
precisam de conferência de conteúdo ou se a UI deve deixar explícito o que foi/não
foi verificado. Ver `docs/curadoria/bloco-d-esboco-comparador-ri.md` (seção
"Pré-requisito descoberto depois") para o contexto completo.

## Menu lateral agrupado por trilha de minuta (`NAV_GROUPS`)

`src/App.jsx` — o array `NAV` virou `NAV_GROUPS`: 3 blocos visuais no menu lateral,
cada um com um `nav-section-label` (reusa o estilo já existente, variante
`.nav-section-label-sub` pros sub-rótulos):
- **Geral** (sem rótulo de seção): Início, Estados, Acervo Legal, Busca Textual,
  Diagramas da Minuta (fica aqui e não na trilha do RI — vem de `commandChart`/
  `organs_detail/ro.json`, ou seja, é a estrutura da PRÓPRIA LOB de Rondônia, não
  conteúdo comparado com outros estados).
- **Regimento Interno**: Subsídio à Minuta, Minuta do Regimento Interno, Subsídio ao
  RI (estrutura), Comparar Regimento Interno (texto).
- **Regulamento Geral**: Minuta do Regulamento Geral, Comparar Regulamento.

**Duas telas de comparação do RI, de propósito (fusão com `master`, 2026-07-09)**:
"Subsídio ao RI" (`/minuta/comparativo-ri`, `RIComparator.jsx`, construído em
paralelo por outra sessão) reusa a MESMA matriz estrutural de "Subsídio à Minuta"
(`comparativo_minuta.json`, campo novo `riOrgans`/`riProvenance`/`riSourceLabel`
por estado), só filtrada aos que têm RI — compara ESTRUTURA/competências.
"Comparar Regimento Interno" (`/minuta/comparar`, Bloco D) compara o TEXTO
verbatim de cada artigo. Rótulos "(estrutura)"/"(texto)" no menu deixam a
diferença óbvia. Ao integrar as duas branches: `master` também tinha corrigido
RN/GO em `parse_doc_type` (regras genéricas por nome de arquivo) — mesclado
sem conflito real com os overrides pontuais de MT/SE (que dependem de
conteúdo, não de nome); `master` NÃO tinha os Blocos A9 (login obrigatório)
nem a reorganização do menu em `NAV_GROUPS` — essas prevaleceram como estavam
nesta branch.

"Revisão da Minuta" e "Acessos" continuam fora dos grupos (o primeiro atende os dois
documentos via seletor interno; o segundo é administrativo). Nomes dos documentos
sempre por extenso agora: "Minuta do Regimento Interno" (não "Minuta RI") e "Minuta
do Regulamento Geral" (não "Minuta do Regulamento").

**Bloco D concluído (2026-07-09)**: comparador "Regimento Interno × outros estados"
em `/minuta/comparar` (`src/pages/MinutaRIComparator.jsx`), análogo ao "Comparar
Regulamento". `minuta_structure.json` ganhou o campo `alternatives` em cada nó
`kind: 'organ'` — 25 dos 27 órgãos têm cobertura (AL, DF, PA, PR, RS; MT/SE saíram
do escopo depois da correção de classificação). Diferente do Regulamento, aqui a
coluna do estado mostra o **ARTIGO COMPLETO** (decisão de produto), não só o
trecho já aproveitado na minuta — decisão que aumenta o valor do comparador mas
também o esforço de extração.
- Curadoria (Fable): `docs/curadoria/bloco-d-classificacao-al-df-pr-pa.md` (20
  órgãos já cobertos por AL/DF/PR/PA, revisão do que já estava em
  `minuta_enrichment.py`) + `docs/curadoria/de-para-ri-rs.md` (RS mapeado pelos
  27 órgãos, nunca lido pra esse fim antes). Achado: das 7 lacunas identificadas,
  5 ganharam fonte válida (bifea←DF GPRAM, cat←RS BESCI, doe←DF COESP,
  assessorias←PA, crbm←RS); só `guarnicao` (matéria de RISD, não de RI) e `gbm`
  (homônimo de natureza diferente no RS) ficam sem correspondência plena.
- Extração: `scripts/extrair_ri_alternativas.py` gera
  `scripts/ri_alternativas_enrichment.py` (reusa as funções de
  `extrair_regulamentos.py`). Achados de leitura tratados: PR tem 2 documentos-
  fonte (LOB × coletânea de RI do portal, roteados por citação); a Portaria nº
  227/2023 do PR (citada pra corregedoria) não existe no acervo — substituída
  pelo Art. 23 da coletânea, mesmo assunto; DF tem "Art. N" embutido no meio da
  linha em alguns pontos; a LOB do PR tem um defeito de conversão que agrupa
  números de artigo no rodapé, desconectados do corpo (resolvido por
  fatiamento de linha verificado manualmente); páginas raspadas de site (não
  PDF) às vezes colam o próximo bloco sem marcador — mecanismo `_STOP_MARKERS`
  no extrator corta no ponto certo (achado ao revisar o Art. 23 do PR).
- `scripts/test_minuta_alternativas.py` valida o schema; entra no `test:py`.
- Ver `docs/curadoria/bloco-d-esboco-comparador-ri.md` e
  `docs/curadoria/bloco-d-pacote-trabalho-fable.md` pro histórico completo.

## Revisão Colaborativa da Minuta (login + comentários + IA)

Módulo NOVO, **independente** do portal estático: permite que pessoas convidadas façam login e
comentem/curem a minuta dispositivo por dispositivo. Backend é **Firebase** (Auth e-mail+senha +
Firestore) consumido direto do frontend; a IA usa uma função serverless. O portal existente não foi
alterado. Specs e planos detalhados em `docs/superpowers/specs/` e `docs/superpowers/plans/`.

### Rotas
- `/login` (pública) — `src/pages/Login.jsx`. Após autenticar, aguarda o `user` ser confirmado via
  `useEffect` antes de navegar (evita corrida com `onAuthStateChanged`).
- `/cadastro` (pública) — `src/pages/Cadastro.jsx`. Autocadastro do convidado: cria a própria senha
  (`cadastrar`); o `AuthProvider` autoriza só se o e-mail estiver na lista de membros e `ativo:true`.
- `/revisao` (protegida) — `src/pages/Revisao.jsx`. Documento da minuta com trilha de balões na margem
  e o popup do dispositivo (`src/components/RevisaoModal.jsx`, duas colunas: sugestões | redação final).
- `/acessos` (protegida, só admin) — `src/pages/Acessos.jsx`. Gestão de convidados/cadastros: convidar
  por e-mail, papel, bloquear/liberar/remover, e acompanhar o último login ("nunca entrou" inclusive).

### Autenticação e autorização
- `src/lib/firebase.js` inicializa Auth + Firestore a partir de `import.meta.env.VITE_FIREBASE_*`.
- `src/lib/auth.jsx` (`AuthProvider`/`useAuth`): autoriza por **e-mail** (`members/{email}` com `ativo:true`);
  no login grava `uid`/`status:'cadastrado'`/`ultimoLogin`. Expõe `entrar`, `cadastrar`, `sair`,
  `recuperarSenha`. E-mails sempre normalizados em minúsculas (`normalizeEmail` em `src/lib/membersStats.js`).
  Papéis `participante`/`admin`.
- `src/lib/membersData.js`: CRUD de membros (`subscribeMembers`/`addMember`/`setMemberRole`/`setMemberAtivo`/
  `removeMember`); `src/lib/membersStats.js`: lógica pura (`contaStatus`/`situacaoMembro`/`normalizeEmail`, com testes).
- `src/components/ProtectedRoute.jsx` bloqueia rotas (e `requireAdmin`).
- Os itens de menu "Revisão" (logado) e "Acessos" (só `role === 'admin'`) aparecem condicionalmente.

### Dados (Firestore) e regras
- Coleções: **`members`** (quem pode entrar; ver nota de indexação), **`suggestions`** (sugestões por
  dispositivo: `dispositivoId`, `autorUid`, `texto`, `curtidoPor[]`, `adminStatus`), **`finalTexts`**
  (`finalTexts/{dispositivoId}`: texto final + status em_aberto/fechado).
- `firestore.rules` define `isMember()`/`isAdmin()` **baseados em `request.auth.token.email`** e as
  permissões; publicar pelo console (passo a passo em `docs/FIREBASE_SETUP.md`). **`members` é indexado
  por E-MAIL** (`members/{email}`, campos `email/nome/role/ativo/status/uid/criadoEm/criadoPor/ultimoLogin`).
  O dono do doc só pode alterar `uid/status/ultimoLogin` (registro de login); o resto é só admin.
- `dispositivoId` (`src/lib/dispositivoId.js`) é o endereço ESTÁVEL do dispositivo (`editId#index` ou
  `editId#caput`), pois o "Art. Nº" é recalculado por `buildArticles`. Premissa: congelar
  `minuta_structure.json` durante a rodada de revisão.
- **Multi-documento na Revisão (Bloco C, fatia 1):** a página `/revisao` comenta DOIS
  documentos — a minuta do RI (`minuta_structure.json`) e a minuta do Regulamento
  (`regulamento_structure.json`) — sem misturar comentários. A separação usa o prefixo
  `reg:` que TODO `editId` do Regulamento já carrega desde o Bloco B2 (`editId` do RI
  nunca deve começar com `reg:` — é a premissa que garante o isolamento; ver
  `src/lib/reviewGroup.js:docOfDispositivo`). Nova coleção **`config/revisao`**
  (doc único, campo `regulamentoAberto: boolean`) controla quando o Regulamento fica
  comentável para quem não é admin; ausência do doc = fechado (fail-closed). Design
  completo em `docs/superpowers/specs/2026-07-07-comissao-comenta-regulamento-design.md`.

### IA — proposta a partir das sugestões relevantes
- `api/_gerarProposta.js` (núcleo: `buildPrompt`/`parseGeminiResposta`/`gerarPropostaCore`, sem framework)
  é reusado por `api/gerar-proposta.js` (função serverless da Vercel) e por um middleware do Vite em
  `vite.config.js` (dev). Endpoint: `POST /api/gerar-proposta` `{textoAtual, sugestoes}` → `{proposta}`.
- Modelo **`gemini-2.5-flash`** (o `gemini-2.0-flash` tinha cota grátis 0 na conta). Chave só no servidor.

### Variáveis de ambiente (NUNCA versionar)
`.env` (copiar de `.env.example`): `VITE_FIREBASE_API_KEY/AUTH_DOMAIN/PROJECT_ID/STORAGE_BUCKET/`
`MESSAGING_SENDER_ID/APP_ID` e `GEMINI_API_KEY`. No deploy (Vercel), cadastrar as MESMAS variáveis em
*Environment Variables*. Projeto Firebase institucional: `revisao-minuta-cbmro-6f248`.

### Rodar e testar
- `npm run dev` sobe o site + o endpoint da IA (middleware). Login exige usuário em `members`.
- Testes de lógica pura: `node --test src/lib/dispositivoId.test.js src/lib/reviewGroup.test.js api/_gerarProposta.test.js`.
- Testar no celular: `cloudflared tunnel --url http://localhost:5173 --protocol http2` (o `--protocol http2`
  evita o flapping do QUIC). `vite.config.js` já tem `server.host:true, allowedHosts:true` para o túnel.

## graphify

This project has a knowledge graph at graphify-out/ with god nodes, community structure, and cross-file relationships.

Rules:
- For codebase questions, first run `graphify query "<question>"` when graphify-out/graph.json exists. Use `graphify path "<A>" "<B>"` for relationships and `graphify explain "<concept>"` for focused concepts. These return a scoped subgraph, usually much smaller than GRAPH_REPORT.md or raw grep output.
- If graphify-out/wiki/index.md exists, use it for broad navigation instead of raw source browsing.
- Read graphify-out/GRAPH_REPORT.md only for broad architecture review or when query/path/explain do not surface enough context.
- After modifying code, run `graphify update .` to keep the graph current (AST-only, no API cost).
