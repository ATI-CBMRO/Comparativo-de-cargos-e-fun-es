import { test } from 'node:test'
import assert from 'node:assert/strict'
import { mergeDecisoes, pendenciasDeAplicacao } from './decisionsMerge.js'

const json = [
  { id: 'a', decidido: false },
  { id: 'b', decidido: true },
  { id: 'c', decidido: true },   // vault diz decidida, mas sistema também tem — sistema vence
  { id: 'd', decidido: false },
]
const fb = new Map([
  ['c', { tipo: 'redacao', decisao: 'texto C' }],
  ['d', { tipo: 'estrutural', decisao: 'x', ficha: { oQueMuda: 'fundir', onde: 'dlog', status: 'aguardando' } }],
])

test('mergeDecisoes: sistema > vault > pendente', () => {
  const m = mergeDecisoes(json, fb)
  assert.equal(m[0].statusDecisao, 'pendente')
  assert.equal(m[1].statusDecisao, 'vault')
  assert.equal(m[2].statusDecisao, 'sistema')
  assert.equal(m[2].registro.decisao, 'texto C')
  assert.equal(m[3].statusDecisao, 'sistema')
})

test('mergeDecisoes tolera fbMap null', () => {
  assert.equal(mergeDecisoes(json, null)[1].statusDecisao, 'vault')
})

test('pendenciasDeAplicacao: só ficha estrutural aguardando', () => {
  const p = pendenciasDeAplicacao(mergeDecisoes(json, fb))
  assert.equal(p.length, 1)
  assert.equal(p[0].id, 'd')
})

// Isolamento por cenário: o registro gravado no ATUAL vive sob a chave "atual:<id>".
// Sem isso, decidir no atual marcaria a mesma decisão como decidida na futura, onde o
// texto final nunca foi aplicado (falso verde — AR-04).
const fbCenarios = new Map([
  ['b', { tipo: 'redacao', decisao: 'B na futura' }],
  ['atual:c', { tipo: 'redacao', decisao: 'C no atual' }],
])

test('mergeDecisoes: no cenário atual só enxerga registros com o marcador', () => {
  const m = mergeDecisoes(json, fbCenarios, 'atual')
  assert.equal(m.find(d => d.id === 'c').statusDecisao, 'sistema')
  assert.equal(m.find(d => d.id === 'c').registro.decisao, 'C no atual')
  // 'b' foi registrada na futura: no atual continua valendo só o vault
  assert.equal(m.find(d => d.id === 'b').statusDecisao, 'vault')
})

test('mergeDecisoes: na futura ignora o registro do atual', () => {
  const m = mergeDecisoes(json, fbCenarios, 'futura')
  assert.equal(m.find(d => d.id === 'b').statusDecisao, 'sistema')
  assert.equal(m.find(d => d.id === 'c').statusDecisao, 'vault') // registro do atual não vaza
})

test('mergeDecisoes sem cenário mantém o comportamento antigo (futura)', () => {
  assert.equal(mergeDecisoes(json, fbCenarios).find(d => d.id === 'b').statusDecisao, 'sistema')
})
