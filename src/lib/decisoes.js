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

// --- Cenário (LOB atual × futura) ---
// Regra de produto (CLAUDE.md): o RI é por ÓRGÃO, logo é ESPECÍFICO da LOB de cada
// cenário; o Regulamento é TEMÁTICO (serviço/disciplina/ensino) e não depende da LOB,
// valendo nos 2. As 36 notas da Fase 2 foram redigidas sobre a LOB FUTURA e não trazem
// o campo `cenarios` — o padrão por trilha reproduz isso sem reescrever o JSON gerado,
// mesma compatibilidade retroativa do `decidido` legado acima. Curadoria nova declara
// `cenarios:` no frontmatter da nota e passa a mandar.
export function cenariosDaDecisao(d) {
  const declarado = d?.cenarios
  if (Array.isArray(declarado) && declarado.length > 0) return declarado
  return d?.trilha === 'reg' ? ['atual', 'futura'] : ['futura']
}

export function filtrarPorCenario(lista, cenario) {
  return (lista ?? []).filter(d => cenariosDaDecisao(d).includes(cenario))
}

// Id do registro no Firestore com o cenário embutido — mesma filosofia do editId
// (reviewGroup.js): o ATUAL carrega o marcador "atual:"; a FUTURA nasce SEM marcador,
// preservando os registros já gravados. Sem isso, registrar uma decisão do Regulamento
// (que aparece nos 2 cenários) marcaria a outra como "Decidida no sistema" sem que o
// texto final tivesse sido aplicado lá — falso verde da classe AR-04.
export function decisionDocId(id, cenario) {
  return cenario === 'atual' ? `atual:${id}` : String(id)
}
