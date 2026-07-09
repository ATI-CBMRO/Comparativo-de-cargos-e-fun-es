import { test } from 'node:test'
import assert from 'node:assert/strict'
import { buildCoverageRows, REGULAMENTO_SERVICO_TYPES } from './acervoCoverage.js'

const doc = (type, typeVerified) => ({ type, typeVerified })

const STATES = [
  {
    id: 'se', name: 'Sergipe', abbreviation: 'SE',
    documents: [
      doc('Lei de Organização Básica', undefined),
      doc('Lei de Organização Básica', undefined),
      doc('Regimento de Serviços', true),
    ],
  },
  {
    id: 'al', name: 'Alagoas', abbreviation: 'AL',
    documents: [
      doc('Lei de Organização Básica', undefined),
      doc('Regimento Interno', false),
    ],
  },
  {
    id: 'mt', name: 'Mato Grosso', abbreviation: 'MT',
    documents: [
      doc('Lei de Organização Básica', undefined),
      doc('Regulamento Geral', true),
    ],
  },
  {
    id: 'ro', name: 'Rondônia', abbreviation: 'RO',
    documents: [doc('Lei de Organização Básica', undefined)],
  },
]

test('funde Regulamento Geral e Regimento de Serviços na coluna regulamento', () => {
  assert.deepEqual(REGULAMENTO_SERVICO_TYPES, ['Regulamento Geral', 'Regimento de Serviços'])
  const rows = buildCoverageRows(STATES)
  const mt = rows.find(r => r.stateId === 'mt')
  const se = rows.find(r => r.stateId === 'se')
  assert.equal(mt.columns.regulamento.present, true)   // Regulamento Geral
  assert.equal(se.columns.regulamento.present, true)   // Regimento de Serviços
})

test('LOB conta múltiplos documentos e nunca tem selo (verified null)', () => {
  const se = buildCoverageRows(STATES).find(r => r.stateId === 'se')
  assert.equal(se.columns.lob.count, 2)
  assert.equal(se.columns.lob.present, true)
  assert.equal(se.columns.lob.verified, null)
})

test('coluna ausente: present false e verified null', () => {
  const ro = buildCoverageRows(STATES).find(r => r.stateId === 'ro')
  assert.equal(ro.columns.regimento.present, false)
  assert.equal(ro.columns.regimento.count, 0)
  assert.equal(ro.columns.regimento.verified, null)
})

test('regulamento todo verificado => verified true', () => {
  const mt = buildCoverageRows(STATES).find(r => r.stateId === 'mt')
  assert.equal(mt.columns.regulamento.verified, true)
})

test('documento com typeVerified falso => verified false', () => {
  const al = buildCoverageRows(STATES).find(r => r.stateId === 'al')
  assert.equal(al.columns.regimento.present, true)
  assert.equal(al.columns.regimento.verified, false)
})

test('linhas ordenadas por nome (pt-BR)', () => {
  const names = buildCoverageRows(STATES).map(r => r.stateName)
  assert.deepEqual(names, ['Alagoas', 'Mato Grosso', 'Rondônia', 'Sergipe'])
})

test('states nulo/vazio não quebra', () => {
  assert.deepEqual(buildCoverageRows(undefined), [])
  assert.deepEqual(buildCoverageRows([]), [])
})
