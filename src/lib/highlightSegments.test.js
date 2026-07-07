import { test } from 'node:test'
import assert from 'node:assert/strict'
import { highlightSegments } from './highlightSegments.js'

test('texto vazio devolve lista vazia', () => {
  assert.deepEqual(highlightSegments(''), [])
  assert.deepEqual(highlightSegments(null), [])
})

test('texto sem termo devolve um único segmento não-negrito', () => {
  assert.deepEqual(highlightSegments('texto qualquer sem termos'), [
    { text: 'texto qualquer sem termos', bold: false },
  ])
})

test('destaca um termo no meio do texto', () => {
  const segs = highlightSegments('nomeado pelo Governador do Estado para o cargo')
  assert.deepEqual(segs, [
    { text: 'nomeado pelo ', bold: false },
    { text: 'Governador do Estado', bold: true },
    { text: ' para o cargo', bold: false },
  ])
})

test('destaca dois termos distintos preservando o texto entre eles', () => {
  const segs = highlightSegments('O Comandante-Geral é Coronel da ativa.')
  assert.deepEqual(segs, [
    { text: 'O ', bold: false },
    { text: 'Comandante-Geral', bold: true },
    { text: ' é ', bold: false },
    { text: 'Coronel', bold: true },
    { text: ' da ativa.', bold: false },
  ])
})

test('é insensível a maiúsculas/minúsculas', () => {
  const segs = highlightSegments('o governador assinou')
  assert.deepEqual(segs, [
    { text: 'o ', bold: false },
    { text: 'governador', bold: true },
    { text: ' assinou', bold: false },
  ])
})
