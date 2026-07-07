import { test } from 'node:test'
import assert from 'node:assert/strict'
import { groupByDispositivo, countByDispositivo, countByChapter } from './reviewGroup.js'
import { parseDispositivoId } from './dispositivoId.js'
import { chapterIdOf } from './minutaTargets.js'

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

test('countByChapter agrupa por capítulo e separa abertas de resolvidas', () => {
  const sugestoes = [
    { dispositivoId: 'organ:cg/competencia#0' },
    { dispositivoId: 'organ:cg/competencia#1' },
    { dispositivoId: 'estrutura#caput' },
  ]
  const finals = new Map([
    ['organ:cg/competencia#0', { status: 'fechado' }],
    ['organ:cg/competencia#1', { status: 'em_aberto' }],
  ])
  const counts = countByChapter(sugestoes, finals, parseDispositivoId, chapterIdOf)
  assert.deepEqual(counts.get('organ:cg'), { open: 1, resolved: 1 })
  assert.deepEqual(counts.get('estrutura'), { open: 1, resolved: 0 })
})

test('countByChapter sem sugestões devolve Map vazio', () => {
  const counts = countByChapter([], new Map(), parseDispositivoId, chapterIdOf)
  assert.equal(counts.size, 0)
})
