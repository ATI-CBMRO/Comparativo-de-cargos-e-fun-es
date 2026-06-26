# Cadastrar e curar a LOB de Alagoas e Espírito Santo — Design

**Data:** 2026-06-26
**Status:** Aprovado no brainstorming, aguardando revisão do spec

## Problema

O comparativo "Subsídio à Minuta" (`/comparar`) vai passar a comparar **apenas LOB do
CBMRO × LOB do estado selecionado** (mudança maior, tratada em sub-projetos separados —
ver "Contexto maior" abaixo). Isso expôs uma lacuna: **Alagoas (AL) e Espírito Santo (ES)
não têm Lei de Organização Básica cadastrada na base** — hoje só têm Regimento Interno e
Quadro Demonstrativo de Cargos (AL) ou Normas Gerais de Ação (ES). Sem a LOB desses dois
estados, eles ficariam fora do comparativo LOB×LOB.

Investigação dos dados (`organs_detail/<id>.json`) também revelou que **não há rastro de
qual documento originou cada órgão/cargo** — tudo é mesclado sem marca de proveniência em
`build_organs_detail.py`. Isso precisa ser corrigido pelo menos para os dados novos que
este sub-projeto introduz.

## Contexto maior

Este é o **sub-projeto 1 de 3** da mudança "comparar só LOB×LOB":
1. **(este spec)** Cadastrar e curar a LOB de AL e ES.
2. Re-curar os 9 estados onde LOB+RI já estão fundidos sem marca de origem (AL\*, AM, DF,
   GO, MT, PR, PA, RS, SE) — separar o que vem de cada documento.
3. Ajustar `build_minuta_comparison.py` e o frontend para comparar só LOB×LOB.

\* Alagoas aparece nas duas listas: aqui ganha curadoria de LOB nova (não existia);
no sub-projeto 2, sua curadoria de RI existente continua intocada — não há fusão a
desfazer em AL, já que RI e LOB sempre foram entradas separadas para esse estado.

## Fontes confirmadas

| Estado | Lei | Fonte | Formato |
|---|---|---|---|
| AL | Lei nº 7.444, de 28/12/2012 ("DISPÕE SOBRE A ORGANIZAÇÃO BÁSICA DO CORPO DE BOMBEIROS MILITAR DO ESTADO DE ALAGOAS") | PDF oficial, intranet do CBMAL | PDF, 14 páginas |
| ES | Lei Complementar nº 101, de 22/09/1997 ("Dispõe sobre a organização básica do Corpo de Bombeiro Militar do Estado do Espírito Santo"), texto consolidado com notas de alterações até a LC nº 1.075/2024 | Portal da ALEPES (legislação compilada) | HTML |

## Armazenamento dos documentos

- **AL:** PDF salvo em `LEGISLAÇÃO CBMS/Alagoas - Lei de Organização Básica.pdf`, processado
  pelo `convert_to_markdown.py` normalmente → gera
  `database/markdown/Alagoas - Lei de Organização Básica.md`.
- **ES:** sem PDF de origem (fonte é HTML). Texto já extraído e limpo é gravado **direto**
  em `database/markdown/Espírito Santo - Lei de Organização Básica.md`, no mesmo formato
  de cabeçalho usado pelo `convert_to_markdown.py` (título + linha `*Documento extraído
  de:*`), citando a URL da ALEPES como fonte — mesmo tratamento de exceção manual que
  `ro.json`/`ac.json` já recebem no projeto.
- `parse_doc_type()` em `build_states_data.py` já classifica qualquer `.md` sem "regimento
  interno"/"nga"/"quadro..." no nome como `"Lei de Organização Básica"` por padrão — **nenhuma
  mudança de código necessária** aí. Após rodar `build_states_data.py`, os dois estados
  passam a listar a LOB em `documents[]`.

## Curadoria da estrutura organizacional

Novas entradas, a partir do texto das leis acima:

- **AL:** novos dicts em `scripts/detail_data_g1.py` (estrutura/órgãos) e
  `scripts/detail_cargos_g1.py` (cargos), onde a curadoria atual de AL já vive.
- **ES:** novos dicts em `scripts/detail_data_g2.py` e `scripts/detail_cargos_g2.py`.
- **IDs novos e distintos** dos já existentes (que vieram do RI/NGA) — sufixo `-lob`
  (ex.: `cg-al-lob`, `dpo-es-lob`) — para não colidir nem se misturar com a curadoria atual
  de RI/NGA desses estados via `merge_cargos()` (que casa por id/sigla/nome).
- Cada órgão e cada cargo novo ganha um campo **`"source": "lob"`**. Esse campo não existe
  hoje em nenhum lugar do pipeline; é introduzido por este sub-projeto e é o que permitirá,
  no sub-projeto 3, filtrar "só LOB" no comparativo sem retrabalho.
- Nível de profundidade da curadoria: equivalente ao já praticado para os demais estados
  com LOB enumerada por artigo/inciso (AL já está nessa categoria hoje, conforme
  CLAUDE.md — atribuições verbatim por cargo). Mesmo padrão para ambos.
- `baseLegal` de cada entrada nova aponta para a lei correta (Lei nº 7.444/2012 para AL;
  LC nº 101/1997 para ES), distinguindo-as das entradas antigas (que apontam para o
  Decreto/RI).

## Mudança de pipeline necessária

- `scripts/build_organs_detail.py`: hoje monta o dict de cada órgão (`extract_organ`-like
  lógica, ver `build_minuta_comparison.py:extract_organ` para função análoga) listando
  campos fixos. Precisa **passar adiante o campo `source`** quando presente no dict de
  origem (passthrough simples) — sem alterar a lógica de matching/merge de
  `merge_cargos()`, que continua funcionando por id/sigla/nome como hoje.
- Nenhuma mudança em `build_states_data.py`, `build_minuta_comparison.py`,
  `curated_organs*.py` ou no frontend.

## Fora de escopo (deste sub-projeto)

- Organograma visual de AL/ES em `StateDetail` (`curated_organs.py`) — continua mostrando a
  árvore atual (derivada do RI), sem mudança.
- `build_minuta_comparison.py` e a UI de `/comparar` — continuam funcionando exatamente como
  hoje; os dados novos ficam "prontos e marcados" dentro de `organs_detail/al.json` e
  `es.json`, mas não são consumidos por nada ainda. A filtragem por `source: "lob"` é
  trabalho do sub-projeto 3.
- Re-curadoria dos 9 estados LOB+RI fundidos — sub-projeto 2.

## Testes / verificação

- Rodar a pipeline na ordem: `convert_to_markdown.py` → `build_organs_detail.py` →
  `build_states_data.py` (ordem já documentada no CLAUDE.md).
- Verificar manualmente `database/organs_detail/al.json` e `es.json`: novas chaves de
  órgão presentes, com `"source": "lob"` e `baseLegal` corretos, coexistindo com as
  entradas antigas (RI/NGA) sem colisão de id.
- Verificar `database/states_data.json`: AL e ES agora listam um documento do tipo
  `"Lei de Organização Básica"`.
- Conferir visualmente em `/estados/al` e `/estados/es` que nada quebrou no organograma
  existente (árvore RI intocada) e que os novos órgãos LOB não aparecem ali (esperado —
  não há `detailId` da árvore apontando pra eles ainda).
