# Taxonomia da Estrutura Organizacional na Minuta do RI — Design

**Data:** 2026-06-21
**Status:** Aprovado para planejamento

## Problema

O Art. 3 (DA ESTRUTURA ORGANIZACIONAL) da minuta do RI apresenta uma **lista
plana de 10 órgãos** (DPO, COT, DOE, CRBM, BBM, CIBM, GBM, BBS, BIFEA, BOA),
enquanto a Lei de Organização Básica (LOB) do CBMRO organiza os mesmos órgãos em
uma **taxonomia de dois níveis**:

- **Órgãos de Direção Operacional** (LOB Art. 6): Direção Setorial (DPO, DOE,
  COT) e Direção Regional (CRBM);
- **Órgãos de Execução** (LOB Art. 9), classificados por **área de atuação**:
  - Atuação Operacional Ordinária: BBM, CAT (e, por coerência interna da LOB,
    CIBM — detalhada na Subseção I, Art. 41);
  - Atuação Operacional Especializada Terrestre: BBS, BIFEA;
  - Atuação Operacional Especializada Aérea: BOA;
  - Atuação Operacional Conveniada Municipal: GBM.

Três descompassos resultam disso:

1. A lista plana mistura órgãos de **direção** com órgãos de **execução** sem
   distinção.
2. As **áreas de atuação** (coração do Art. 9 da LOB) desaparecem.
3. A **CAT** (Coordenadoria de Atividades Técnicas) — que a LOB põe no mesmo
   patamar do BBM como órgão de execução de atuação ordinária (Art. 9 §1º, II;
   Art. 42) — aparece apenas como subdivisão interna do COT, nunca como órgão.

O Art. 60 da LOB determina que o detalhamento orgânico se dê **no respectivo
Regimento Interno** — ou seja, o RI é exatamente onde essa taxonomia deve ser
fielmente reproduzida.

## Decisões tomadas (com o usuário)

1. **CAT vira capítulo próprio** de órgão de execução.
2. **CIBM entra em "Atuação Operacional Ordinária"** (junto a BBM e CAT),
   corrigindo silenciosamente a omissão do Art. 9 §1º da LOB.
3. **CAT como órgão de primeira classe**: adicionada ao `ro.json`, passando a
   aparecer também no organograma do estado (StateDetail) e na página
   "Subsídio à Minuta" (comparador), além da minuta.
4. **Art. 3 articulado em dois artigos**: um para Direção, outro para Execução
   (fiel à separação Art. 6 / Art. 9 da LOB).

## Solução

### 1. Novo órgão `cat` em `database/organs_detail/ro.json`

Adicionar a chave `cat` ao dicionário `organs` com:

- `id`: `"cat"`, `name`: `"Coordenadoria de Atividades Técnicas"`,
  `abbreviation`: `"CAT"`, `category`: `"Execução"`,
  `subordinadoA`: `"Comando de Operações Técnicas (COT)"`, `legalRef`: `"Art. 42"`,
  `baseLegal`: idêntico aos demais órgãos do `ro.json`,
  `artigosDeOrigem`: `["Art. 42 (CAT)"]`.
- `atribuicoes` (finalidade/competência, da LOB Art. 42):
  - "Órgão de execução de atuação operacional ordinária, subordinado ao Comando
    de Operações Técnicas (COT), incumbido de estudar, analisar, exigir e
    fiscalizar as atividades pertinentes à segurança contra incêndio e pânico."
  - "Proceder a análise de projetos, realizar investigação de incêndios, testes
    de materiais, vistorias e emitir pareceres técnicos, com autoridade para
    notificar, multar, embargar e interditar na forma da lei específica."
- `desdobramentos` (composição, da LOB Art. 42 parágrafo único):
  Coordenador; Adjunto; Seção Administrativa; Seção de Análise de Projetos;
  Seção de Investigação e Prevenção de Incêndio; Gerência de Atividades Técnicas
  — Seção Administrativa, Seção de Vistoria, Seção de Hidrantes.
- `cargos`: **mover** o cargo "Coordenador de Atividades Técnicas (CAT)" hoje em
  `cot.cargos` para `cat.cargos` (preservando `requisito`, `subordinadoA`,
  `desdobramentos`, `atribuicoes` verbatim).

No órgão `cot` do `ro.json`:
- **remover** o cargo "Coordenador de Atividades Técnicas (CAT)" de `cot.cargos`;
- **manter** a linha de Organização Interna que cita "Coordenadorias de
  Atividades Técnicas (CATs) — Art. 42: …" (passa a ser cross-reference).

> `ro.json` é arquivo escrito à mão (exceção do pipeline); editar diretamente.

### 2. Reordenar `ORGAN_ORDER` em `scripts/build_minuta_structure.py`

Nova ordem (topo → menor fração, agrupando por categoria/área), 11 órgãos:

```python
ORGAN_ORDER = [
    ("dpo",   "DA DIRETORIA DE PLANEJAMENTO OPERACIONAL (DPO)",          "A"),
    ("doe",   "DA DIRETORIA OPERACIONAL ESPECIALIZADA (DOE)",            "A"),
    ("cot",   "DO COMANDO DE OPERAÇÕES TÉCNICAS (COT)",                  "O"),
    ("crbm",  "DOS COMANDOS REGIONAIS DE BOMBEIRO MILITAR (CRBM)",       "O"),
    ("bbm",   "DO BATALHÃO DE BOMBEIROS MILITAR (BBM)",                  "O"),
    ("cibm",  "DA COMPANHIA INDEPENDENTE DE BOMBEIROS MILITAR (CIBM)",   "A"),
    ("cat",   "DA COORDENADORIA DE ATIVIDADES TÉCNICAS (CAT)",           "A"),
    ("bbs",   "DO BATALHÃO DE BUSCA E SALVAMENTO (BBS)",                 "O"),
    ("bifea", "DO BATALHÃO DE INCÊNDIO FLORESTAL E EMERGÊNCIAS AMBIENTAIS (BIFEA)", "O"),
    ("boa",   "DO BATALHÃO DE OPERAÇÕES AÉREAS (BOA)",                   "O"),
    ("gbm",   "DO GRUPO DE BOMBEIROS MILITAR (GBM)",                     "O"),
]
```

(`dpo, doe, cot` na ordem da LOB Art. 6 §3; `gbm` por último, conveniada.)

### 3. Capítulo da Estrutura em dois artigos — novo tipo `articles`

O modelo de capítulos hoje tem três `kind`: `prose`, `incisos`, `organ`. Um
capítulo `incisos` gera **um** artigo. Para o capítulo da Estrutura gerar **dois**
artigos sob um único título de capítulo, introduzimos um quarto `kind`:
`articles`, que carrega uma lista `articles: [<leaf incisos>, …]`, cada folha
gerando um artigo; o título do capítulo aparece só no primeiro.

`build_estrutura_chapter()` passa a retornar:

```
{
  id: "estrutura", kind: "articles",
  chapterTitle: "DA ESTRUTURA ORGANIZACIONAL",
  articles: [
    { id:"direcao", kind:"incisos", editId:"estrutura/direcao",
      caput:"São Órgãos de Direção Operacional:",
      items:[
        {text:"de Direção Setorial: a Diretoria de Planejamento Operacional (DPO), a Diretoria Operacional Especializada (DOE) e o Comando de Operações Técnicas (COT)", source:"ro"},
        {text:"de Direção Regional: os Comandos Regionais de Bombeiro Militar (CRBM)", source:"ro"},
      ], proposedText:"…" },
    { id:"execucao", kind:"incisos", editId:"estrutura/execucao",
      caput:"Os Órgãos de Execução classificam-se, quanto à área de atuação, em:",
      items:[
        {text:"Atuação Operacional Ordinária: o Batalhão de Bombeiros Militar (BBM), a Companhia Independente de Bombeiros Militar (CIBM) e a Coordenadoria de Atividades Técnicas (CAT)", source:"ro"},
        {text:"Atuação Operacional Especializada Terrestre: o Batalhão de Busca e Salvamento (BBS) e o Batalhão de Incêndio Florestal e Emergências Ambientais (BIFEA)", source:"ro"},
        {text:"Atuação Operacional Especializada Aérea: o Batalhão de Operações Aéreas (BOA)", source:"ro"},
        {text:"Atuação Operacional Conveniada Municipal: o Grupo de Bombeiros Militar (GBM)", source:"ro"},
      ], proposedText:"…" },
  ],
}
```

As listas de órgãos por área são derivadas de `ORGAN_ORDER` filtrando pela
`category` lida do `ro.json` (Direção Setorial / Direção Regional / Execução) e,
para a execução, por uma classificação de área de atuação. Como o `ro.json` não
carrega o campo "área de atuação", o mapeamento órgão→área fica explícito no
script (`AREA_BY_ORGAN = {"bbm":"ordinaria","cibm":"ordinaria","cat":"ordinaria",
"bbs":"terrestre","bifea":"terrestre","boa":"aerea","gbm":"conveniada"}`), de
modo que a ordem/elenco dos artigos siga sempre `ORGAN_ORDER`.

### 4. `buildArticles` e wizard — suportar `kind: "articles"`

`src/lib/minutaArticles.js` — em `buildArticles`, tratar
`chapter.kind === 'articles'`: iterar `chapter.articles` e emitir cada folha como
artigo (`emitLeaf(leaf, false)`), reaproveitando a lógica de `firstOfChapter`
(título do capítulo só no primeiro artigo).

`src/pages/MinutaWizard.jsx` — `indexLeaves` e `indexSources` hoje só leem
`ch.items` para capítulos não-`organ`. Estender ambas para, quando
`ch.kind === 'articles'`, iterar `ch.articles` e indexar cada folha por seu
`editId` (sem `sectionTitle`). O sumário (que lista `ch.chapterTitle`) e o
`chapterIdOf` (que usa `editId.split('/')[0]` → `estrutura`) continuam corretos.

### 5. Comparador "Subsídio à Minuta"

`scripts/build_minuta_comparison.py` importa `ORGAN_ORDER`, logo a CAT entra como
órgão automaticamente. Para a coluna não ficar só com o RO, adicionar uma entrada
`cat` em `AUTO_MATCH_KEYWORDS` de `scripts/minuta_comparison_lib.py`:

```python
"cat": {
    "include": ["atividades tecnicas", "atividade tecnica",
                "seguranca contra incendio", "analise de projetos", "vistoria"],
    "exclude": ["operacoes tecnicas", "comando de operacoes"],
},
```

(Valores exatos a refinar no plano; o objetivo é casar "Coordenadoria/Centro/
Diretoria de Atividades Técnicas" de outros estados, sem casar o próprio COT.)

### 6. Atualizações de contagem e documentação

Trocar "10 órgãos da LOB"/"11 órgãos (10 da LOB + guarnição)" por
"11 órgãos da LOB + Guarnição = 12" em: comentários de
`build_minuta_comparison.py`, `build_minuta_structure.py` e seção pertinente do
`CLAUDE.md`. A badge de contagem em `MinutaComparator.jsx` é dinâmica
(`data.organs.length`) — não requer alteração.

## Pipeline de regeneração (ordem importa)

Após editar `ro.json` e os scripts:

```bash
python scripts/build_organs_detail.py        # regenera (não toca ro.json escrito à mão)
python scripts/build_states_data.py          # organograma + enriquecimento
python scripts/build_minuta_structure.py     # minuta (Art. 3 + capítulo CAT)
python scripts/build_dpo_cot_comparison.py   # pré-requisito do comparador
python scripts/build_minuta_comparison.py    # comparador (coluna CAT)
```

> `cat` é definido à mão em `ro.json`; `build_organs_detail.py` não sobrescreve o
> arquivo escrito à mão. Confirmar isso no plano.

## Testes

- `src/lib/minutaArticles.test.js` (`node --test`): novo caso cobrindo um
  capítulo `kind: "articles"` — dois artigos sob um título de capítulo,
  numeração contínua, título de capítulo só no primeiro artigo.
- Verificação manual: `MinutaWizard` (sumário rola para a Estrutura; os dois
  artigos e o capítulo CAT aparecem; curadoria por inciso e edição por seção
  funcionam nos `editId`s `estrutura/direcao` e `estrutura/execucao`); página
  "Subsídio à Minuta" exibe a CAT.

## Fora de escopo

- Enriquecimento curado de competências da CAT a partir de outros CBMs (mantém-se
  só o texto do RO/LOB Art. 42).
- Reordenação ou reclassificação de órgãos administrativos (não operacionais).
- Alterações no comparador além da entrada da CAT.
