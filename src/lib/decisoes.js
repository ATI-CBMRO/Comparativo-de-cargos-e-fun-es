// Lógica pura da aba Decisões (cockpit Fase 2). Sem React, sem fetch — testável isolada.

export function decisoesDaTrilha(dados, trilha) {
  return (dados?.decisoes ?? []).filter(d => d.trilha === trilha)
}

export function filtrarDecisoes(lista, filtro) {
  if (filtro === 'pendentes') return lista.filter(d => !d.decidido)
  if (filtro === 'decididas') return lista.filter(d => d.decidido)
  return lista
}

export function contarDecisoes(lista) {
  const decididas = lista.filter(d => d.decidido).length
  return { total: lista.length, decididas, pendentes: lista.length - decididas }
}
