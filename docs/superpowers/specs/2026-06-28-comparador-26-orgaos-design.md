# Frente 2 — Curadoria verbatim dos 15 órgãos novos no comparador (design)

## Contexto

A Frente 1 (mesclada em `master`) expandiu `scripts/build_minuta_structure.py` e o
`/minuta-diagramas` para os 26 órgãos da LOB do CBMRO (`ORGAN_ORDER`), com `cg`
(Comando Geral) como raiz real da árvore de comando. O comparador `/comparar`
(`scripts/build_minuta_comparison.py`, página `src/pages/MinutaComparator.jsx`)
importa o mesmo `ORGAN_ORDER` e por isso já lista os 26 órgãos + Guarnição (27
linhas), mas **15 deles aparecem com "0 estados"**, pois as camadas de dados que
alimentam o comparativo não foram estendidas:

- **Curada:** mapa DPO/COT (`database/comparativo_dpo_cot.json`, só cobre `dpo`/`cot`)
  + competências verbatim de `ENRICHMENT_ORGAN` em `scripts/minuta_enrichment.py`
  (hoje só cobre `dpo`, `cot`, `crbm`, `bbm`, `cibm`, `bbs`, `bifea`, `boa`, `cat`).
- **Automática:** casamento por palavra-chave (`AUTO_MATCH_KEYWORDS` em
  `scripts/minuta_comparison_lib.py`), também restrito aos mesmos órgãos.

Os 15 órgãos sem nenhuma cobertura, confirmados rodando
`python scripts/build_minuta_comparison.py`:

```
cg, depdec, condeg, dp, deei, dpof, dsap, dlog, cint, ccs, cinf,
assessorias, gab-cg, ag, corregedoria
```

**Restrição padrão do projeto** (já registrada em memória de longo prazo): não
substituir as camadas curadas existentes por extração automática pura — o usuário
já abortou essa abordagem em 2026-06-26. Este trabalho é **aditivo**: preenche o
gap dos 15 órgãos novos sem tocar nas chaves já curadas.

## Objetivo

Pesquisa comparativa profunda: curar, **verbatim** (como já é feito hoje para os
11 órgãos originais), as competências dos 15 órgãos novos a partir da legislação
de **todos os 27 estados** (varredura do zero — não reaproveitar cegamente os
descartes já documentados, pois um estado pode não enumerar COT mas enumerar
Diretoria de Pessoal, por exemplo).

## Categorias reais (campo `category` em `database/organs_detail/ro.json`)

Os 15 órgãos se agrupam em 4 blocos de pesquisa, cada um uma tarefa do plano:

| Bloco | Órgãos | Categoria (`ro.json`) |
|---|---|---|
| 1 — Direção Geral/Colegiada | `cg`, `depdec`, `condeg` | Direção Geral / Direção Colegiada |
| 2 — Direção Setorial | `dp`, `deei`, `dpof`, `dsap`, `dlog`, `cint`, `ccs`, `cinf` | Direção Setorial |
| 3 — Assessoramento/Apoio | `assessorias`, `gab-cg`, `ag` | Assessoramento / Apoio ao Comando-Geral / Apoio ao Subcomando-Geral |
| 4 — Correição | `corregedoria` | Correição |

## Arquitetura

Nenhuma mudança estrutural em código de build ou frontend: `build_minuta_comparison.py`,
`build_minuta_structure.py` e `MinutaComparator.jsx` já operam genericamente sobre
qualquer chave presente em `ORGAN_ORDER` + `ENRICHMENT_ORGAN` + `AUTO_MATCH_KEYWORDS`.
O trabalho é puramente de **dados**, em 3 arquivos:

1. **`scripts/minuta_enrichment.py`** — para cada item verbatim encontrado, uma lista
   `_XX_ORGAO` de strings + `_tag(lista, "cf. CBMxx, Lei/RI, Art. N")`, adicionada a
   uma entrada nova em `ENRICHMENT_ORGAN[organ_key]` (mesmo padrão das entradas
   existentes, ex.: `ENRICHMENT_ORGAN["dpo"]`). Como esse dict já é importado tanto
   por `build_minuta_structure.py` (`/minuta`) quanto por `build_minuta_comparison.py`
   (`/comparar`), cada entrada nova beneficia as duas páginas automaticamente.
2. **`scripts/minuta_comparison_lib.py`** — extensão de `AUTO_MATCH_KEYWORDS` com
   `include`/`exclude` para as 15 chaves novas, dando ao `/comparar` uma camada
   "automático" de fallback nos estados não curados verbatim (mesmo padrão dos
   11 órgãos atuais).
3. **`docs/ENRIQUECIMENTO_MINUTA.md`** — nova seção por bloco, documentando fontes
   aproveitadas e descartadas (com motivo), seguindo a tabela já existente.

`database/organs_detail/ro.json` **nunca é tocado** (todas as 26 chaves já existem
lá desde a Frente 1).

## Fluxo de trabalho (por bloco — 4 tarefas)

1. Dispatch de um subagente de pesquisa, somente leitura, que varre
   `database/markdown/*.md` dos 26 estados (exceto RO) procurando, para cada órgão
   do bloco, um órgão equivalente (por nome/função — nomes variam entre estados,
   ex. "Diretoria de Pessoal" → `dp`, "Corregedoria" → `corregedoria`) que **enumere
   competências verbatim** (incisos limpos transcritos da fonte). Mesmo critério já
   documentado em `docs/ENRIQUECIMENTO_MINUTA.md`: descarta texto
   condensado/parafraseado ou narrativo por subdivisão.
2. O subagente reporta, por órgão do bloco: lista de `{estado, citação (Lei/Art.),
   itens verbatim}` encontrados + descartes com motivo.
3. Controller (eu) revisa o achado e integra manualmente nos 3 arquivos listados
   acima.
4. Regera `database/minuta_structure.json` e `database/comparativo_minuta.json`
   (`python scripts/build_minuta_structure.py && python scripts/build_minuta_comparison.py`).
5. Roda a suíte JS (`node --test`, hoje 14/14 passando) e confirma, por diff, que
   nenhuma chave pré-existente de `ENRICHMENT_ORGAN`/`AUTO_MATCH_KEYWORDS` foi
   alterada e que `ro.json` segue intocado.
6. Revisão de spec-compliance + revisão de qualidade de código (subagent-driven-development).

## Critério de aceite por tarefa

- Todo item novo tem citação de fonte (`cf. CBMxx, Lei/RI/Decreto, Art. N`).
- Nenhum item é paráfrase/condensado — só verbatim enumerado.
- Nenhuma chave pré-existente do `ENRICHMENT_ORGAN`/`AUTO_MATCH_KEYWORDS` foi alterada
  (mudança puramente aditiva).
- `database/organs_detail/ro.json` intocado.
- `docs/ENRIQUECIMENTO_MINUTA.md` atualizado com a nova seção do bloco (fontes
  aproveitadas + descartadas com motivo).
- Build reproduzível: rodar os scripts duas vezes produz o mesmo JSON.

## Casos de borda esperados (aceitáveis, não são falhas)

Alguns órgãos (ex.: `condeg` — conselho deliberativo, `ag` — ajudância-geral) são
estruturas pouco comuns fora do RO; é esperado que tenham poucos ou nenhum match,
assim como `cibm`/`guarnicao` hoje têm só 1 estado curado cada. Isso é documentado
como descarte avaliado (mesmo padrão da seção "Avaliadas e descartadas" já
existente), não tratado como tarefa incompleta.

## Fora de escopo

- Nenhuma mudança em `build_minuta_comparison.py`, `build_minuta_structure.py`,
  `MinutaComparator.jsx`, `MinutaWizard.jsx` ou `MinutaOrgChart.jsx` — a estrutura
  genérica já suporta os 26 órgãos.
- Nenhuma alteração nas chaves já curadas (`dpo`, `cot`, `crbm`, `bbm`, `cibm`,
  `bbs`, `bifea`, `boa`, `cat`, `gbm`, `guarnicao`).
- Nenhuma alteração em `database/organs_detail/ro.json` ou em
  `database/comparativo_dpo_cot.json`.

## Testes

- Suíte JS existente (`node --test`, `src/lib/minutaArticles.test.js`) — deve
  continuar 14/14 após cada bloco.
- Verificação manual de reprodutibilidade dos builds Python (sem suíte automatizada
  no pipeline de dados, conforme já documentado em `CLAUDE.md`).
- Diff dirigido por chave (`git diff` em `minuta_enrichment.py` e
  `minuta_comparison_lib.py`) para confirmar natureza aditiva de cada mudança.
