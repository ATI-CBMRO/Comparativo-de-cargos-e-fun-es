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

// Sugestões por capítulo, separadas em abertas × resolvidas (usada pelo sumário de
// capítulos da Revisão da Minuta). `parseDispositivoId`/`chapterIdOf` e `finals` (Map
// dispositivoId -> {status}) vêm de fora — função pura, sem depender de React/Firebase.
export function countByChapter(suggestions, finals, parseDispositivoId, chapterIdOf) {
  const map = new Map()
  for (const s of suggestions) {
    const { editId } = parseDispositivoId(s.dispositivoId)
    const chapterId = chapterIdOf(editId)
    const entry = map.get(chapterId) ?? { open: 0, resolved: 0 }
    const resolvida = finals.get(s.dispositivoId)?.status === 'fechado'
    if (resolvida) entry.resolved += 1; else entry.open += 1
    map.set(chapterId, entry)
  }
  return map
}
