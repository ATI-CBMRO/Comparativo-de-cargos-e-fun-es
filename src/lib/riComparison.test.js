import { test } from 'node:test'
import assert from 'node:assert/strict'
import {
  RI_STATE_IDS, indexComparativo, organKeyOfChapter,
  stateHasData, statesWithData, pickState,
} from './riComparison.js'

test('organKeyOfChapter aceita ids do cenário atual (atual:organ:<key>)', () => {
  assert.equal(organKeyOfChapter('atual:organ:cg'), 'cg')
  assert.equal(organKeyOfChapter('atual:organ:cepdec'), 'cepdec')
})

const COMPARATIVO = {
  organs: [
    {
      key: 'cg', title: 'DO COMANDO GERAL (CG)', abbr: 'CG',
      states: [
        { id: 'al', abbr: 'AL', provenance: 'curado', sourceLabel: 'cf. CBMAL',
          riOrgans: [{ name: 'Comando Geral', abbreviation: 'CG', atribuicoes: ['comandar'] }] },
        { id: 'ac', abbr: 'AC', provenance: 'curado', sourceLabel: 'cf. CBMAC',
          riOrgans: [{ name: 'Comando Geral', abbreviation: 'CG', atribuicoes: ['comandar'] }] },
        { id: 'rs', abbr: 'RS', provenance: 'automatico', sourceLabel: 'cf. CBMRS',
          riOrgans: [{ name: 'CG', abbreviation: 'CG', atribuicoes: [] }] },
      ],
    },
    {
      key: 'dpo', title: 'DA DPO', abbr: 'DPO',
      states: [
        { id: 'mt', abbr: 'MT', provenance: 'curado', sourceLabel: 'cf. CBMMT',
          riOrgans: [{ name: 'Departamento', abbreviation: 'DPO', atribuicoes: ['planejar'] }] },
      ],
    },
  ],
}

test('RI_STATE_IDS tem os 7 estados com Regimento Interno de fato (sem am/go)', () => {
  assert.deepEqual(RI_STATE_IDS, ['al', 'df', 'mt', 'pr', 'pa', 'rs', 'se'])
})

test('indexComparativo indexa por key, ignorando entradas sem key', () => {
  const idx = indexComparativo({ organs: [...COMPARATIVO.organs, { key: null, states: [] }] })
  assert.equal(idx.cg.title, 'DO COMANDO GERAL (CG)')
  assert.equal(idx.dpo.abbr, 'DPO')
  assert.equal(Object.keys(idx).length, 2)
})

test('indexComparativo tolera entrada vazia', () => {
  assert.deepEqual(indexComparativo(null), {})
  assert.deepEqual(indexComparativo({}), {})
})

test('organKeyOfChapter extrai a key só de capítulos de órgão', () => {
  assert.equal(organKeyOfChapter('organ:cg'), 'cg')
  assert.equal(organKeyOfChapter('organ:dpo'), 'dpo')
  assert.equal(organKeyOfChapter('estrutura'), null)
  assert.equal(organKeyOfChapter('preliminares'), null)
  assert.equal(organKeyOfChapter('atual:preliminares'), null)
  assert.equal(organKeyOfChapter(null), null)
})

test('stateHasData exige ao menos uma atribuição não vazia', () => {
  assert.equal(stateHasData({ riOrgans: [{ atribuicoes: ['x'] }] }), true)
  assert.equal(stateHasData({ riOrgans: [{ atribuicoes: [] }] }), false)
  assert.equal(stateHasData({ riOrgans: [] }), false)
  assert.equal(stateHasData(null), false)
})

test('statesWithData filtra por RI + dado e mantém a ordem de RI_STATE_IDS', () => {
  const idx = indexComparativo(COMPARATIVO)
  const withData = statesWithData(idx.cg)
  // 'ac' não é estado-RI; 'rs' é RI mas tem atribuições vazias -> só 'al'
  assert.deepEqual(withData.map(s => s.id), ['al'])
})

test('statesWithData retorna [] para organEntry ausente', () => {
  assert.deepEqual(statesWithData(null), [])
})

test('pickState mantém o estado anterior quando disponível', () => {
  const available = [{ id: 'al' }, { id: 'mt' }]
  assert.equal(pickState('mt', available), 'mt')
})

test('pickState cai no primeiro quando o anterior sumiu', () => {
  const available = [{ id: 'al' }, { id: 'mt' }]
  assert.equal(pickState('rs', available), 'al')
})

test('pickState retorna null quando não há disponíveis', () => {
  assert.equal(pickState('al', []), null)
  assert.equal(pickState(null, []), null)
})
