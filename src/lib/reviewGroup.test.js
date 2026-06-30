import { test } from 'node:test'
import assert from 'node:assert/strict'
import { groupByDispositivo, countByDispositivo } from './reviewGroup.js'

const sugs = [
  { id: 'a', dispositivoId: 'cot#0', texto: 'x' },
  { id: 'b', dispositivoId: 'cot#0', texto: 'y' },
  { id: 'c', dispositivoId: 'cot#caput', texto: 'z' },
]

test('groupByDispositivo agrupa por dispositivoId', () => {
  const g = groupByDispositivo(sugs)
  assert.equal(g.get('cot#0').length, 2)
  assert.equal(g.get('cot#caput').length, 1)
  assert.equal(g.get('cot#0')[0].id, 'a')
})

test('countByDispositivo conta por dispositivoId', () => {
  const c = countByDispositivo(sugs)
  assert.equal(c.get('cot#0'), 2)
  assert.equal(c.get('cot#caput'), 1)
  assert.equal(c.get('inexistente'), undefined)
})
