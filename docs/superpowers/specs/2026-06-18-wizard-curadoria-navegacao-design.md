# Wizard da minuta — curadoria por inciso, filtro por fonte e navegação

**Data:** 2026-06-18
**Status:** Aprovado para planejamento
**Contexto:** evolução do `MinutaWizard.jsx` após a minuta operacional hierárquica
(`2026-06-18-minuta-operacional-hierarquica-design.md`) e o enriquecimento de 8
legislações (`minuta_enrichment.py`).

## Problema

A minuta ficou densa: 13 capítulos, 10 órgãos, ~48 seções por função, com
competências de DPO/COT/CRBM agregando 5+ legislações. O wizard atual obriga a
revisar **folha a folha** as 48 seções em sequência, sem visão da árvore e sem
forma de filtrar/remover incisos. Os badges de fonte são só rótulo. Para a minuta
virar um rascunho curável, é preciso tornar a curadoria fácil.

## Decisões (definidas com o usuário)

1. **Curadoria estruturada por inciso** (checkbox incluir/excluir); a edição livre
   de texto vira "modo avançado" por seção.
2. **Filtro por fonte = checkboxes por legislação** (RO sempre ligado), com atalhos
   marcar/desmarcar todas.
3. **Superfície principal = documento único rolável** com checkboxes inline, barra
   de filtro fixa no topo e sidebar com a árvore de capítulos/seções.

## Modelo de estado (fonte única de verdade)

- **`excluded: Set<string>`** — incisos removidos. Chave estável
  `` `${editId}#${index}` `` (índice no `items[]` original da folha).
- **Filtro por fonte NÃO é camada independente:** ligar/desligar uma legislação é
  uma operação em lote sobre `excluded` (desligar CBMPR ⇒ adiciona todos os itens
  com `source` iniciando em `cf. CBMPR`; ligar ⇒ remove). Uma só fonte de verdade,
  sem ambiguidade entre "filtrado" e "removido manualmente".
- **`edits: { editId → string }`** — modo avançado: texto livre que substitui a
  seção (esconde os checkboxes dela; incisos viram `source: null`, como hoje).
- RO não tem toggle de fonte (é a base); incisos individuais de qualquer fonte
  podem ser removidos pelo checkbox.
- Estado vive em React (perdido ao recarregar, como o `edits` atual). Persistência
  em localStorage fica **fora de escopo**.

### Chave de fonte (para o filtro em lote)

`sourceKey(source)`: `"ro"` → `RO`; senão, extrai o token após `cf. ` até a
primeira vírgula (`"cf. CBMPR, Lei…"` → `CBMPR`). Usado para agrupar checkboxes e
para a operação em lote.

## Núcleo de articulação (`src/lib/minutaArticles.js`)

`buildArticles(structure, edits = {}, isExcluded = () => false)` — novo 3º
parâmetro predicado (default = nada excluído, mantém retrocompatibilidade):

- Em cada folha `incisos`, itera os itens com o índice original; **pula** os que
  `isExcluded(editId, index)`; numera só os incluídos (numeração correta).
- Cada inciso de saída carrega `{ text, source, editId, index }` (antes só
  `{text, source}`).
- Seção sem incisos incluídos continua omitida pela regra atual
  (`if (incisos.length || !isSection)`).
- Modo avançado (`edits[editId]` presente) ignora `isExcluded` (texto livre manda).

Função pura; testável.

## Interface — etapa "Revisão & curadoria" (documento único)

Três zonas:

1. **Sidebar (esquerda):** árvore Capítulos → Seções (derivada da estrutura),
   clicável → `scrollIntoView` da seção. Marca seções que têm itens removidos
   (ex.: ponto/contador). Largura fixa, rolagem própria.
2. **Barra fixa (topo do documento):** um checkbox por legislação presente
   (`RO, CBMAL, CBMPR, CBMMT, CBMSC, CBMBA, CBMPE, CBMES, CBMPA`) + botões
   "marcar todas" / "desmarcar todas" (RO permanece). Toggle = operação em lote
   sobre `excluded`.
3. **Documento (centro, rolável):** regimento articulado por
   `buildArticles(structure, edits, isExcluded)`. Para cada inciso, um **checkbox
   inline** (marcado = incluso); desmarcar adiciona a `excluded` e **renumera ao
   vivo**. Por seção com itens removidos, um expansor "*▸ N removidos*" mostra os
   incisos retirados (cinza/tachado) com checkbox para readicionar. Cada seção tem
   botão "**editar texto**" → abre a `textarea` daquela seção (modo avançado);
   fechar volta para os checkboxes.

Âncoras: cada seção (e capítulo) recebe um `id` para o `scrollIntoView` da sidebar.

**Seção totalmente removida:** `buildArticles` a omite (sem artigo numerado), mas
o documento ainda renderiza um **stub cinza** daquela seção (título + expansor
"*▸ N removidos*"), lido da estrutura, para que continue alcançável pela sidebar e
os incisos possam ser readicionados. Não recebe número de artigo enquanto vazia.

## `.docx` e fluxo

- O download usa **o mesmo** `buildArticles(structure, edits, isExcluded)` — o
  arquivo baixado é exatamente o documento curado na tela. Incisos `source: null`
  ou `RO` não recebem citação; demais recebem `(cf. …)` como hoje.
- Etapas: **Visão geral → Revisão & curadoria → Download** (mantém o stepper de 3).

## Componentes / arquivos

- `src/lib/minutaArticles.js` — `buildArticles` ganha `isExcluded`; incisos com
  `editId`/`index`.
- `src/lib/minutaArticles.test.js` — novos casos.
- `src/pages/MinutaWizard.jsx` — reescrita da etapa 1 (documento único + sidebar +
  barra de fontes + checkboxes inline + expansor de removidos + modo avançado);
  estado `excluded` e helpers `sourceKey`, `isExcluded`, `toggleSource`. O `.docx`
  passa `isExcluded`. Como o arquivo cresce, extrair subcomponentes no mesmo
  arquivo: `SourceFilterBar`, `NavSidebar`, `IncisoRow`, `SectionBlock`.

## Testes e verificação

- **Unit (`minutaArticles.test.js`):** exclusão por predicado (numeração pula
  removidos; seção esvaziada some; incisos trazem `editId`/`index`);
  retrocompatibilidade sem predicado (comportamento atual).
- **Manual:** filtrar por fonte (lote), remover/readicionar inciso, editar texto de
  uma seção, navegar pela sidebar, gerar `.docx` e conferir que bate com a tela;
  Comparador de Cargos intacto; `npm run build` ok.

## Fora de escopo (YAGNI)

- Persistência (localStorage) do estado de curadoria.
- Dedup semântico automático entre legislações.
- Reordenar incisos; editar item a item fora do modo avançado.
