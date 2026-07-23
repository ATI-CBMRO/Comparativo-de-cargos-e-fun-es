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
