// Agrupamento/contagem de sugestões por dispositivoId (lógica pura, sem React/Firebase).
export function groupByDispositivo(suggestions) {
  const map = new Map()
  for (const s of suggestions) {
    const arr = map.get(s.dispositivoId)
    if (arr) arr.push(s)
    else map.set(s.dispositivoId, [s])
  }
  return map
}

export function countByDispositivo(suggestions) {
  const map = new Map()
  for (const s of suggestions) {
    map.set(s.dispositivoId, (map.get(s.dispositivoId) ?? 0) + 1)
  }
  return map
}
