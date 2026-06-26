# 3ª coluna "LOB do estado" no comparativo — Design

**Data:** 2026-06-26
**Status:** Aprovado no brainstorming, aguardando revisão do spec

## Problema

O comparativo `/comparar` ("Subsídio à Minuta") hoje compara, por órgão, a minuta da LOB do
CBMRO (coluna referência) contra **uma** coluna do estado selecionado, cujos dados vêm de
quatro camadas misturadas (mapa curado DPO/COT + enrichment verbatim + Guarnição + casamento
automático no `organs_detail`). O usuário quer ver, lado a lado, **o que a LOB daquele estado
diz** vs. **o que a legislação compilada (atual) daquele estado diz**, sem perder nenhuma das
camadas curadas já construídas.

## Objetivo

Adicionar uma **3ª coluna "LOB do estado"** ao lado da coluna atual, que passa a se chamar
"Legislação compilada". A tabela fica: **Campo · CBMRO · LOB do estado · Legislação
compilada**. A coluna compilada permanece **100% intacta**; a coluna LOB é uma camada nova,
de proveniência uniforme (só LOB).

Pré-requisitos já concluídos: todos os 27 estados têm a camada LOB limpa em `organs_detail`
(`source:"lob"` nos 10 estados com legislação mista — AL, ES, AM, DF, GO, MT, PA, PR, RS, SE;
curadoria integralmente LOB nos ~17 de doc único de LOB). Specs
`2026-06-26-lob-al-es-design.md` e `2026-06-26-lob-8-estados-design.md`.

## Arquitetura

### Dados — `scripts/build_minuta_comparison.py`

- A produção atual de `states[].organs` (camada compilada: curado + enrichment + auto +
  Guarnição) fica **inalterada**.
- ADICIONA, por estado, um conjunto paralelo **`states[].lobOrgans`**: uma passagem
  independente que, para cada órgão do RO, casa contra o `organs_detail` do estado
  **filtrado a LOB** e devolve os órgãos LOB correspondentes (mesmo shape de `organs`).
- **Filtro LOB** (helper novo `lob_organs(organs)`): se o estado tem algum órgão com
  `source=="lob"`, retorna só esses; senão retorna todos (os ~17 puros). Reusa exatamente a
  regra já validada nos sub-projetos anteriores.
- **Casamento** da coluna LOB: reusa `auto_match_organ_ids` (de `minuta_comparison_lib.py`),
  que hoje cobre doe, crbm, bbm, cibm, gbm, bbs, bifea, boa, cat. **Estende
  `AUTO_MATCH_KEYWORDS`** com regras para `dpo` e `cot` (que antes só vinham do mapa curado):
  - `dpo`: include `["planejamento", "plan. operacional", "planejamento operacional"]`
  - `cot`: include `["operacoes", "operacional"]`, exclude `["aerea", "aereo"]`
  Esses keywords são aproximados; a coluna LOB pode ficar vazia ("—") para órgãos/estados sem
  casamento — aceitável, pois a coluna compilada continua ao lado.
- `lobOrgans` por estado: lista de órgãos (mesmo `_strip_organ`/`extract_organ` shape já
  usado), mais um campo `lobProvenance`: `"curado"` se ALGUM órgão casado tem `source=="lob"`
  (os 10 estados tagueados), senão `"automatico"` (os ~17 puros). Reaproveita o `ProvBadge`.
- Estados sem nenhum órgão LOB casado para o órgão corrente: `lobOrgans: []` → célula "—".
- A ordem/estrutura (`organs[].depth`, `command_order`) e a coluna referência RO ficam
  inalteradas.

### Frontend — `src/pages/MinutaComparator.jsx` + `PairTable`

- O `PairTable` passa de 3 para **4 colunas**: `colgroup` ganha `oc-pair-col-lob`; o `thead`
  ganha uma 3ª coluna de cabeçalho ("LOB do estado", com o `ProvBadge` da `lobProvenance`),
  empurrando a atual para "Legislação compilada". Cada linha (`MATRIX_ROWS`) ganha uma célula
  `oc-pair-td-lob` que renderiza `StateCell` com `state.lobOrgans` (reusa `StateCell`,
  passando os órgãos LOB no lugar de `organs`).
- O cabeçalho do estado (sigla, nome, CBM) é compartilhado pelas duas colunas do estado, ou
  repetido em ambas com rótulos distintos ("LOB" / "Compilada"). Decisão: cabeçalho do estado
  em cada uma das 2 colunas, com um sub-rótulo distinguindo "LOB" vs "Compilada" e o
  respectivo `ProvBadge`.
- Os **chips de UF** (seleção de estado) e a barra lateral de órgãos ficam inalterados —
  trocam o estado nas duas colunas ao mesmo tempo.
- Texto introdutório da página atualizado para descrever a comparação de 3 vias (CBMRO × LOB
  do estado × legislação compilada).

### Estilo — `src/index.css`

- `colgroup`: `.oc-pair-col-label` (170px) + três colunas de conteúdo a
  `calc((100% - 170px) / 3)` cada (RO, LOB, compilada).
- `.oc-pair-table` ganha `min-width` maior (ex.: 820px) para que o `oc-pair-wrapper`
  (que já tem `overflow-x:auto`) ative scroll horizontal em telas estreitas, em vez de
  espremer as 4 colunas.
- Bloco `@media print` (`.oc-pair-table` em 9pt, Paisagem) já existe; ajustar larguras para 4
  colunas caberem (fonte um pouco menor se necessário).
- Bloco `@media (max-width: 900px)` já trata `oc-pair-*`; estender para a coluna LOB
  (largura, scroll).

## Não-objetivos / fora de escopo

- Não alterar a coluna compilada nem as camadas que a alimentam (curado/enrichment/Guarnição).
- Não mudar a estrutura de órgãos (linhas/ordem), a barra lateral, os chips de UF, nem o RO.
- Não re-curar dados (os 27 estados já têm a camada LOB).
- Não mexer no wizard `/minuta` nem nos diagramas.

## Riscos e mitigação

- **Casamento dpo/cot fraco:** os keywords novos são aproximados; alguns estados mostrarão
  "—" na coluna LOB para dpo/cot. Mitigação: aceitável — a coluna compilada (com o mapa
  curado DPO/COT) continua ao lado, então nenhuma informação é perdida; a coluna LOB só
  acrescenta. Pode ser refinada depois ampliando os keywords.
- **Largura da tabela:** 4 colunas ficam largas. Mitigação: scroll horizontal já existente no
  wrapper; em telas pequenas o usuário rola. PDF em Paisagem com fonte reduzida.
- **Sobreposição visual LOB×compilada para estados puros:** nos ~17 estados de doc único, as
  duas colunas mostrarão dados parecidos (a compilada é quase a LOB). Mitigação: é esperado e
  informativo (mostra consistência); a distinção fica clara nos estados com legislação mista.

## Testes / verificação

- Regenerar `python scripts/build_minuta_comparison.py`; conferir no
  `comparativo_minuta.json` que cada estado tem `lobOrgans` e `lobProvenance`, e que os 10
  estados tagueados puxam órgãos `source:lob` (ex.: AL, ES, MT).
- Conferência visual em `/comparar`: selecionar um estado misto (ex.: MT, SE) e ver as 3
  colunas distintas; selecionar um estado puro (ex.: BA) e ver LOB ≈ compilada; órgão sem
  casamento LOB mostra "—" na coluna LOB sem quebrar a compilada. Sem erros de console.
- Conferir export PDF (`window.print()`) com 4 colunas em Paisagem.
- Rodar `node --test` (suíte existente não deve quebrar; nenhuma lógica de `minutaArticles`
  é tocada).
