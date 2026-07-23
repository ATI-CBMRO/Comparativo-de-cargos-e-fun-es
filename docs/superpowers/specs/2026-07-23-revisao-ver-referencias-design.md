# Ver referências no popup de Revisão — Design

## Objetivo

No popup de Revisão (`RevisaoModal.jsx`), quem está analisando um dispositivo específico
hoje só vê o texto em discussão, as sugestões e a redação final — sem link para as
referências de outros estados ("Bloco D"/`alternatives`) que embasaram a construção daquele
capítulo/órgão. Este trabalho adiciona essa visibilidade, reaproveitando um componente que
já existe na tela de Conferência linear.

## Contexto técnico confirmado

- `alternatives` é uma propriedade de **capítulo inteiro** (órgão do RI / tema do
  Regulamento) em `minuta_structure.json`/`regulamento_structure.json` — não existe por
  dispositivo individual. A referência mostrada será sempre a do capítulo ao qual o
  dispositivo pertence, igual ao que a tela de Conferência já faz.
- `Revisao.jsx` já carrega o JSON completo (`data`, via `fetchJson`) e cada dispositivo
  aberto no popup carrega um `id` no formato `<editId>#caput` ou `<editId>#<index>`.
  `chapterIdOf(parseDispositivoId(id).editId)` (já existe em `minutaTargets.js`/
  `dispositivoId.js`) devolve o id do capítulo (ex.: `organ:dpo`, `reg:uniformes-apresentacao`).
- A UI de referências (chips por estado + trecho + fonte + selo de match) já existe, inline,
  dentro de `ConferenciaItem` em `ConferenciaLinear.jsx` (linhas ~111-196). Será extraída
  para um componente compartilhado.

## Componente compartilhado: `AlternativesPanel`

Novo arquivo `src/components/AlternativesPanel.jsx`, extraído do bloco de renderização de
`ConferenciaItem` (chips de estado + lista de excertos + `MatchBadge`). Props:

```
AlternativesPanel({ alternatives, selectedUf, onSelectUf })
```

- `alternatives`: o objeto `{ [uf]: { name, abbr, docLabel, excerpts: [...] } }` (mesmo shape
  de hoje).
- `selectedUf`/`onSelectUf`: estado do chip ativo, controlado pelo componente pai (mesmo
  padrão de `ufSel`/`setUfSel` que `ConferenciaLinear.jsx` já usa por `chapterId`).
- Renderiza exatamente o que `ConferenciaItem` renderiza hoje na coluna direita (chips +
  excertos), sem lógica de negócio nova.
- `MatchBadge` também migra para este arquivo (hoje é local a `ConferenciaLinear.jsx`) e é
  exportado para reuso.

`ConferenciaLinear.jsx` passa a importar `AlternativesPanel`/`MatchBadge` de
`AlternativesPanel.jsx` em vez de definir/renderizar inline — comportamento visual idêntico
ao de hoje (nenhuma mudança para quem já usa a tela de Conferência).

## Mudança no popup de Revisão

**`Revisao.jsx`:**
- Ao abrir o popup (`abrir(id, label, trecho)`), também calcula e guarda o `chapterId`:
  `chapterIdOf(parseDispositivoId(id).editId)`.
- Busca o capítulo em `data.chapters` (mesmo array já carregado) por esse `chapterId` e
  extrai `.alternatives` (objeto vazio `{}` se o capítulo não tiver).
- Passa `alternatives` como nova prop pro `RevisaoModal`.

**`RevisaoModal.jsx`:**
- Recebe prop `alternatives` (objeto `{ [uf]: {...} }`, pode ser `{}`).
- No cabeçalho (`rev-mhead`), ao lado do rótulo "● Em discussão", um botão
  `Ver referências (N)` onde `N = Object.keys(alternatives).length`.
  - `N === 0`: botão desabilitado (`disabled`), estilo acinzentado, tooltip "Nenhuma
    referência de outro estado capturada para este órgão/tema ainda".
  - `N > 0`: botão clicável, alterna um estado local `mostrarRefs` (boolean).
- Quando `mostrarRefs` é `true`, renderiza `<AlternativesPanel alternatives={alternatives}
  selectedUf={ufRef} onSelectUf={setUfRef} />` logo abaixo do cabeçalho, antes das duas
  colunas de sugestões/redação final (ocupa a largura toda do popup).
- Fecha automaticamente (`mostrarRefs` volta a `false`) quando o popup troca de dispositivo
  (mesmo padrão que já existe pro `useEffect` de `final`/`finalText`).

## Fora de escopo

- Não altera o cálculo/estrutura de `alternatives` nos scripts Python nem nos JSONs.
- Não adiciona referência por dispositivo específico (granularidade fica em capítulo,
  como já é hoje em todo o resto do sistema).
- Não altera a tela de Conferência linear visualmente — só extrai o componente que já existe.

## Testes

- `AlternativesPanel.jsx` é apresentação pura (sem lógica de dados nova) — sem teste unitário
  dedicado, mas prova visual (Playwright) cobre: capítulo com 1 estado, capítulo com múltiplos
  estados (troca de chip), capítulo sem `alternatives` (botão desabilitado).
- `node --test` completo deve seguir em 132/132 depois da extração (nenhuma lógica pura nova
  além da já testada em `dispositivoId.js`/`minutaTargets.js`).
