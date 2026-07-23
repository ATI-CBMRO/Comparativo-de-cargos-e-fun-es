// Lógica pura da aba Decisões (cockpit Fase 2). Sem React, sem fetch — testável isolada.

export function decisoesDaTrilha(dados, trilha) {
  return (dados?.decisoes ?? []).filter(d => d.trilha === trilha)
}

// Decidida = registro no sistema/vault (statusDecisao) OU, para dados sem esse campo
// (Fase 2 pura), o antigo `decidido` booleano — mantém compatibilidade retroativa.
function isDecidida(d) {
  return d.statusDecisao ? d.statusDecisao !== 'pendente' : Boolean(d.decidido)
}

export function filtrarDecisoes(lista, filtro) {
  if (filtro === 'pendentes') return lista.filter(d => !isDecidida(d))
  if (filtro === 'decididas') return lista.filter(d => isDecidida(d))
  return lista
}

export function contarDecisoes(lista) {
  const decididas = lista.filter(isDecidida).length
  return { total: lista.length, decididas, pendentes: lista.length - decididas }
}
