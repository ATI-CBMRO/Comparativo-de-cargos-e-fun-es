// Etiqueta de documento embutida no próprio editId: todo dispositivo do Regulamento
// nasce com prefixo "reg:" (Bloco B2); RI nunca usa esse prefixo. Sem campo novo,
// sem migração — ver docs/superpowers/specs/2026-07-07-comissao-comenta-regulamento-design.md.
export function docOfDispositivo(dispositivoId) {
  return String(dispositivoId).startsWith('reg:') ? 'reg' : 'ri'
}

export function filterSuggestionsByDoc(suggestions, docId) {
  return suggestions.filter(s => docOfDispositivo(s.dispositivoId) === docId)
}

export function filterFinalsByDoc(finals, docId) {
  const map = new Map()
  finals.forEach((v, k) => { if (docOfDispositivo(k) === docId) map.set(k, v) })
  return map
}

// Cenário embutido no próprio editId, na mesma filosofia do "reg:" (sem campo novo, sem
// migração): o cenário ATUAL carrega o marcador "atual:" (no RI, prefixo "atual:"; no
// Regulamento, "reg:atual:"); a LOB FUTURA nasce SEM marcador, preservando os comentários
// e textos finais já existentes. Assim endereços como "organ:cg" não colidem entre cenários.
export function scenarioOfDispositivo(dispositivoId) {
  const id = String(dispositivoId)
  return (id.startsWith('atual:') || id.startsWith('reg:atual:')) ? 'atual' : 'futura'
}

export function filterSuggestionsByScenario(suggestions, cenario) {
  return suggestions.filter(s => scenarioOfDispositivo(s.dispositivoId) === cenario)
}

export function filterFinalsByScenario(finals, cenario) {
  const map = new Map()
  finals.forEach((v, k) => { if (scenarioOfDispositivo(k) === cenario) map.set(k, v) })
  return map
}

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
