# Curar a LOB dos 8 estados com LOB+RI fundidos — Design

**Data:** 2026-06-26
**Status:** Aprovado no brainstorming, aguardando revisão do spec

## Problema

Vamos adicionar ao comparativo `/comparar` uma **3ª coluna "LOB do estado"** ao lado da
coluna atual "legislação compilada" (Sub-projeto B, separado). Para a coluna LOB nascer
limpa nos 27 estados, falta isolar a LOB de **8 estados cuja curadoria hoje funde LOB + RI
(ou + Quadro de Cargos) sem marca de origem**: AM, DF, GO, MT, PA, PR, RS, SE.

Esses estados têm em `organs_detail/<id>.json` uma árvore de órgãos que mistura dois
documentos, sem o campo `source` que permitiria filtrar só a LOB. Sem isolar isso, a coluna
LOB desses 8 estados sairia impura (mistura RI). Os demais 19 estados já estão prontos:
AL e ES ganharam entradas `source:"lob"` no Sub-projeto 1; os ~17 de doc único de LOB têm
curadoria que já é integralmente LOB.

## Contexto maior

Este é o **Sub-projeto A** da feature "3ª coluna LOB no comparativo":
- **A (este spec):** curar a LOB dos 8 estados mistos, como camada `source:"lob"`.
- **B (próximo):** `build_minuta_comparison.py` produz, por estado, dois conjuntos —
  `lob` (filtrado por `source:"lob"`) e `compilada` (as camadas curadas atuais, intactas);
  `MinutaComparator.jsx` renderiza 3 colunas (CBMRO · LOB do estado · legislação compilada).

Sub-projeto A reusa **exatamente** o padrão do Sub-projeto 1 (spec
`2026-06-26-lob-al-es-design.md`), que cadastrou e curou a LOB de AL e ES.

## Estados, fontes e arquivos

Todos os 8 têm um markdown de LOB disponível em `database/markdown/` (texto utilizável,
verificado). Cada estado vive num par `detail_data_g*.py` / `detail_cargos_g*.py`:

| UF | Lei (baseLegal) | markdown de LOB | g-file |
|----|-----------------|-----------------|--------|
| AM | Lei nº 2.538/1999 (Organização Básica) | `Amazonas - Organização Básica.md` | g1 |
| DF | Lei nº 8.255/1991 (Organização Básica) | `Distrito Federal - Organização Básica.md` | g2 |
| GO | Lei nº 18.305/2013 (Organização Básica) | `Goiás - Organização Básica (Lei 18.305-2013).md` | g3 |
| MT | Lei Complementar nº 775/2023 (Organização Básica) | `Mato Grosso - Organização Básica.md` | g3 |
| PA | Lei nº 11.060/2025 (Organização Básica) | `Pará - Organização Básica.md` | g4 |
| PR | Lei nº 22.206/2020 (Organização Básica) | `Paraná - Organização Básica.md` | g4 |
| RS | Decreto que regulamenta a LC nº 14.920/2016 (Organização Básica) | `Rio Grande do Sul - Organização Básica.md` | g5 |
| SE | Lei nº 8.979/2022 (Organização Básica) | `Sergipe - Organização Básica (Lei 8.979-2022).md` | g5 |

Os números de lei acima saem do `legal_source` atual de cada `organs_detail/<id>.json`; o
texto exato de `baseLegal` deve ser confirmado contra o cabeçalho do markdown de LOB durante
a curadoria (a fonte do RS é o Decreto regulador, não a LC em si — registrar isso fielmente).

## Curadoria (por estado)

Para cada estado, a partir do seu markdown de LOB:

1. **Órgãos.** Adicionar entradas novas em `detail_data_g*.py`, dentro do bloco `"<id>"` →
   `"organs"`, com ids `<sigla>-<uf>-lob` (ex.: `cg-am-lob`, `em-df-lob`). Cada entrada tem
   os mesmos campos das existentes: `name`, `abbreviation`, `category`, **`source: "lob"`**,
   `subordinadoA`, `legalRef`, `baseLegal`, `artigosDeOrigem`, `atribuicoes`,
   `desdobramentos`, `cargos` (vazio aqui; cargos vão no arquivo de cargos).
2. **Cargo(s)-chave.** No `detail_cargos_g*.py`, sob a chave `"<id>"`, adicionar o cargo do
   dirigente máximo (Comandante-Geral) com `id` de órgão `cg-<uf>-lob`, com atribuições
   **verbatim** quando a LOB as enumera por inciso; quando a LOB é em prosa
   (finalidade/competência), transcrever fielmente sem inventar listas — convenção já
   vigente no projeto (CLAUDE.md). Cargos de outros órgãos podem ser adicionados quando a
   lei os enumerar, mas o mínimo é o Comandante-Geral, espelhando AL/ES.
3. **Profundidade.** Equivalente a AL/ES: cobrir os órgãos de direção, apoio e execução
   nomeados na LOB, com a finalidade/competência de cada um. Não precisa descer a cada seção
   interna; `desdobramentos[]` lista as subdivisões nomeadas.

## Regras de isolamento

- **Ids `-lob` nunca colidem** com os existentes (que não têm o sufixo). Verificação
  automática por estado.
- **Entradas mescladas existentes não são tocadas** — elas seguem alimentando a coluna
  "compilada" do Sub-projeto B. O diff de cada `detail_*` deve ser puramente aditivo.
- O campo `source` já sobrevive ao `build_organs_detail.py` sem mudança de código (confirmado
  no Sub-projeto 1: o build grava cada órgão direto, sem lista de campos permitidos).

## Pipeline e verificação

Ordem (documentada no CLAUDE.md): `build_organs_detail.py` → `build_states_data.py`.

- `states_data.json`: os 8 estados **já listam** "Lei de Organização Básica" em `documents`
  (não muda); só a contagem de órgãos no organograma pode variar pelo enriquecimento.
- Por estado, verificar em `organs_detail/<id>.json`: nº de entradas `source:"lob"` > 0,
  ausência de ids duplicados, entradas antigas (sem `source`) preservadas e em mesmo número.
- Conferência visual em `/estados/<id>` de 2–3 estados: organograma curado atual intacto
  (a árvore visual vem de `curated_organs*.py`, não tocada), sem erros de console.

## Fora de escopo

- A 3ª coluna no comparativo e qualquer mudança em `build_minuta_comparison.py` ou frontend
  — isso é o Sub-projeto B.
- O organograma visual (`curated_organs*.py`) e o painel de detalhe — inalterados; os novos
  órgãos `-lob` não aparecem na árvore visual (esperado, sem `detailId` apontando para eles).
- Estados já prontos (AL, ES e os de doc único de LOB) — nada a fazer.

## Execução

Subagentes, **um estado por tarefa** (cada subagente lê o markdown de LOB do estado e cura o
par data/cargos), seguidos de uma tarefa final de rebuild + verificação consolidada. Cada
tarefa é independente das demais (estados não se cruzam), com revisão de spec-compliance e
qualidade entre elas.
