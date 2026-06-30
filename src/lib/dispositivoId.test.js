import { test } from 'node:test'
import assert from 'node:assert/strict'
import { incisoDispositivoId, caputDispositivoId, parseDispositivoId } from './dispositivoId.js'

test('incisoDispositivoId monta editId#index', () => {
  assert.equal(incisoDispositivoId('cot-comp', 2), 'cot-comp#2')
})

test('caputDispositivoId monta editId#caput', () => {
  assert.equal(caputDispositivoId('cot-comp'), 'cot-comp#caput')
})

test('parseDispositivoId lê inciso numérico', () => {
  assert.deepEqual(parseDispositivoId('cot-comp#2'), { editId: 'cot-comp', parte: 2 })
})

test('parseDispositivoId lê caput', () => {
  assert.deepEqual(parseDispositivoId('cot-comp#caput'), { editId: 'cot-comp', parte: 'caput' })
})

test('parseDispositivoId aceita editId com hífen e ignora apenas o último #', () => {
  assert.deepEqual(parseDispositivoId('bbm-frac-3#0'), { editId: 'bbm-frac-3', parte: 0 })
})
