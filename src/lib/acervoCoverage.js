// Lógica pura do Acervo Legal: agrega os documentos de cada estado nas 3
// colunas da tabela de cobertura (LOB / Regimento Interno / Regulamento de
// Serviço). Sem React. A coluna "Regulamento de Serviço" funde dois tipos
// reais do acervo (Regulamento Geral e Regimento de Serviços).

export const REGULAMENTO_SERVICO_TYPES = ['Regulamento Geral', 'Regimento de Serviços']

const LOB_TYPE = 'Lei de Organização Básica'
const REGIMENTO_TYPE = 'Regimento Interno'

// Rótulo curto do documento para a etiqueta da tabela: "Lei 7.444/2012",
// "Portaria 24/2020"… Cai para o nome do arquivo (sem o prefixo do estado)
// quando não há número de lei registrado.
function docLabel(doc) {
  const laws = doc.laws || []
  const yr = doc.year
  if (laws.length && laws[0].numero) {
    const tipo = laws[0].tipo || 'Lei'
    return `${tipo} ${laws[0].numero}${yr ? `/${yr}` : ''}`
  }
  const mf = doc.md_file || ''
  const base = mf.includes(' - ')
    ? mf.split(' - ').slice(1).join(' - ').replace(/\.md$/, '')
    : mf.replace(/\.md$/, '')
  return base || (yr ? String(yr) : doc.type)
}

// URL pública do PDF servido estaticamente (mesmo padrão de StateDetail).
function docPdf(doc) {
  return doc.md_file && doc.has_pdf
    ? `/legislacao-pdf/${encodeURIComponent(doc.md_file.replace('.md', '.pdf'))}`
    : null
}

// Em qual das 3 colunas o documento se encaixa (ou "outros" para tipos que não
// entram na tabela de cobertura, ex.: Normas Gerais de Ação).
function bucketOf(type) {
  if (type === LOB_TYPE) return 'lob'
  if (type === REGIMENTO_TYPE) return 'regimento'
  if (REGULAMENTO_SERVICO_TYPES.includes(type)) return 'regulamento'
  return 'outros'
}

// Detalhes de um documento usados pela etiqueta e pela aba "Documentos por estado".
function docInfo(doc) {
  const laws = doc.laws || []
  return {
    type: doc.type,
    bucket: bucketOf(doc.type),
    label: docLabel(doc),
    lawText: laws.length ? laws.map(l => `${l.tipo} nº ${l.numero}`).join(' · ') : null,
    year: doc.year ?? null,
    charCount: doc.char_count || 0,
    verified: doc.typeVerified === true,
    pdf: docPdf(doc),
  }
}

// Monta uma célula a partir dos documentos de um tipo. `withSeal` = false para a
// LOB (nunca exibe selo), então verified fica sempre null.
function buildCell(docs, withSeal) {
  const present = docs.length > 0
  let verified = null
  if (present && withSeal) {
    verified = docs.every(d => d.typeVerified === true)
  }
  return { count: docs.length, present, verified, docs: docs.map(docInfo) }
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
      cbmName: s.cbm_name,
      cbmAbbr: s.cbm_abbreviation,
      columns: {
        lob: buildCell(lobDocs, false),
        regimento: buildCell(riDocs, true),
        regulamento: buildCell(regDocs, true),
      },
      // Todos os documentos do estado (inclui tipos fora das 3 colunas) para a
      // relação detalhada da aba "Documentos por estado".
      documents: docs.map(docInfo),
    }
  })
  return rows.sort((a, b) => a.stateName.localeCompare(b.stateName, 'pt-BR'))
}
