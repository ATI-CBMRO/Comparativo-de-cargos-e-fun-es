import { test } from 'node:test'
import assert from 'node:assert/strict'
import { confKey, mergeStatus, divergentesDe } from './conferenciaStatus.js'

test('confKey é estável por editId+número', () => {
  assert.equal(confKey({ editId: 'reg:tema-a/mt-art-1', number: 7 }), 'reg:tema-a/mt-art-1#art7')
})

test('mergeStatus: remoto vence o local', () => {
  const local = new Map([['a#art1', 'ok'], ['b#art2', 'div']])
  const remoto = new Map([['a#art1', { status: 'div' }]])
  const m = mergeStatus(local, remoto)
  assert.equal(m.get('a#art1'), 'div')
  assert.equal(m.get('b#art2'), 'div')
})

test('divergentesDe filtra por documento e cenário', () => {
  const remoto = new Map([
    ['reg:tema#art1', { status: 'div' }],           // reg, futura
    ['reg:atual:tema#art2', { status: 'div' }],     // reg, atual
    ['organ:cg/x#art3', { status: 'div' }],         // ri, futura
    ['reg:tema#art4', { status: 'ok' }],
  ])
  assert.equal(divergentesDe(remoto, 'reg', 'futura').length, 1)
  assert.equal(divergentesDe(remoto, 'reg', 'atual').length, 1)
  assert.equal(divergentesDe(remoto, 'ri', 'futura').length, 1)
})
