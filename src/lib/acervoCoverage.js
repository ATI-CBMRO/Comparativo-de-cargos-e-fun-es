// Lógica pura do Acervo Legal: agrega os documentos de cada estado nas 3
// colunas da tabela de cobertura (LOB / Regimento Interno / Regulamento de
// Serviço). Sem React. A coluna "Regulamento de Serviço" funde dois tipos
// reais do acervo (Regulamento Geral e Regimento de Serviços).

export const REGULAMENTO_SERVICO_TYPES = ['Regulamento Geral', 'Regimento de Serviços']

const LOB_TYPE = 'Lei de Organização Básica'
const REGIMENTO_TYPE = 'Regimento Interno'

// Monta uma célula a partir dos documentos de um tipo. `withSeal` = false para a
// LOB (nunca exibe selo), então verified fica sempre null.
function buildCell(docs, withSeal) {
  const present = docs.length > 0
  let verified = null
  if (present && withSeal) {
    verified = docs.every(d => d.typeVerified === true)
  }
  return { count: docs.length, present, verified }
}

// data.states -> uma linha por estado, ordenada por nome (pt-BR).
export function buildCoverageRows(states) {
  if (!Array.isArray(states)) return []
  const rows = states.map(s => {
    const docs = s.documents || []
    const lobDocs = docs.filter(d => d.type === LOB_TYPE)
    const riDocs = docs.filter(d => d.type === REGIMENTO_TYPE)
    const regDocs = docs.filter(d => REGULAMENTO_SERVICO_TYPES.includes(d.type))
    return {
      stateId: s.id,
      stateName: s.name,
      abbreviation: s.abbreviation,
      columns: {
        lob: buildCell(lobDocs, false),
        regimento: buildCell(riDocs, true),
        regulamento: buildCell(regDocs, true),
      },
    }
  })
  return rows.sort((a, b) => a.stateName.localeCompare(b.stateName, 'pt-BR'))
}
