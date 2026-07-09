import { test } from 'node:test'
import assert from 'node:assert/strict'
import {
  groupByDispositivo, countByDispositivo, countByChapter,
  docOfDispositivo, filterSuggestionsByDoc, filterFinalsByDoc,
} from './reviewGroup.js'
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

test('docOfDispositivo reconhece prefixo reg: do Regulamento', () => {
  assert.equal(docOfDispositivo('reg:disposicoes-preliminares/mt-art-1#0'), 'reg')
})

test('docOfDispositivo trata qualquer editId sem prefixo reg: como RI', () => {
  assert.equal(docOfDispositivo('organ:cg/competencia#0'), 'ri')
  assert.equal(docOfDispositivo('estrutura#caput'), 'ri')
})

test('filterSuggestionsByDoc separa sugestões do RI e do Regulamento', () => {
  const suggestions = [
    { id: 'a', dispositivoId: 'organ:cg/competencia#0' },
    { id: 'b', dispositivoId: 'reg:disposicoes-preliminares/mt-art-1#0' },
    { id: 'c', dispositivoId: 'estrutura#caput' },
  ]
  const ri = filterSuggestionsByDoc(suggestions, 'ri')
  const reg = filterSuggestionsByDoc(suggestions, 'reg')
  assert.deepEqual(ri.map(s => s.id), ['a', 'c'])
  assert.deepEqual(reg.map(s => s.id), ['b'])
})

test('filterFinalsByDoc separa o Map de textos finais por documento', () => {
  const finals = new Map([
    ['organ:cg/competencia#0', { status: 'fechado' }],
    ['reg:disposicoes-preliminares/mt-art-1#0', { status: 'em_aberto' }],
  ])
  const ri = filterFinalsByDoc(finals, 'ri')
  const reg = filterFinalsByDoc(finals, 'reg')
  assert.equal(ri.size, 1)
  assert.equal(ri.get('organ:cg/competencia#0').status, 'fechado')
  assert.equal(reg.size, 1)
  assert.equal(reg.get('reg:disposicoes-preliminares/mt-art-1#0').status, 'em_aberto')
})

test('filterSuggestionsByDoc/filterFinalsByDoc com listas vazias devolvem vazio', () => {
  assert.deepEqual(filterSuggestionsByDoc([], 'ri'), [])
  assert.equal(filterFinalsByDoc(new Map(), 'reg').size, 0)
})
