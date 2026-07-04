// Lógica pura do Comparativo de RI: indexa comparativo_minuta.json por órgão,
// mapeia capítulo->órgão e seleciona os estados com RI que têm dado. Sem React.

// Os 9 estados com LOB + Regimento Interno (ordem de exibição fixa).
export const RI_STATE_IDS = ['al', 'am', 'df', 'go', 'mt', 'pr', 'pa', 'rs', 'se']

const ORGAN_PREFIX = 'organ:'

// comparativo.organs[] -> { [key]: organEntry }. Ignora entradas sem key.
export function indexComparativo(comparativo) {
  const map = {}
  for (const o of comparativo?.organs ?? []) {
    if (o && o.key) map[o.key] = o
  }
  return map
}

// "organ:cg" -> "cg"; "estrutura"/"preliminares"/"finais" -> null.
export function organKeyOfChapter(chapterId) {
  const id = String(chapterId ?? '')
  return id.startsWith(ORGAN_PREFIX) ? id.slice(ORGAN_PREFIX.length) : null
}

// Verdadeiro se o estado tem ao menos uma atribuição não vazia na camada SÓ-RI
// (riOrgans) — sem o enriquecimento da LOB, que fica na coluna `organs`.
export function stateHasData(stateEntry) {
  return (stateEntry?.riOrgans ?? []).some(o => (o?.atribuicoes ?? []).length > 0)
}

// Estados de RI_STATE_IDS (nessa ordem) que existem no órgão e têm dado.
export function statesWithData(organEntry, stateIds = RI_STATE_IDS) {
  if (!organEntry) return []
  const byId = {}
  for (const s of organEntry.states ?? []) byId[s.id] = s
  const out = []
  for (const id of stateIds) {
    const s = byId[id]
    if (s && stateHasData(s)) out.push(s)
  }
  return out
}

// Mantém prevStateId se ainda disponível; senão o primeiro; senão null.
export function pickState(prevStateId, available) {
  if (!available || available.length === 0) return null
  if (prevStateId && available.some(s => s.id === prevStateId)) return prevStateId
  return available[0].id
}
