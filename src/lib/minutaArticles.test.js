import { test } from 'node:test'
import assert from 'node:assert/strict'
import { articleLabel, romanize, normalizeInciso } from './minutaArticles.js'

test('articleLabel usa ordinal até 9 e cardinal a partir de 10', () => {
  assert.equal(articleLabel(1), 'Art. 1º')
  assert.equal(articleLabel(9), 'Art. 9º')
  assert.equal(articleLabel(10), 'Art. 10')
  assert.equal(articleLabel(12), 'Art. 12')
})

test('romanize converte inteiros em algarismos romanos', () => {
  assert.equal(romanize(1), 'I')
  assert.equal(romanize(4), 'IV')
  assert.equal(romanize(9), 'IX')
  assert.equal(romanize(14), 'XIV')
})

test('normalizeInciso minusculiza inicial e pontua por posição', () => {
  assert.equal(normalizeInciso('Coordenação operacional', 0, 3), 'coordenação operacional;')
  assert.equal(normalizeInciso('Execução das ações', 1, 3), 'execução das ações; e')
  assert.equal(normalizeInciso('Proteção e defesa civil', 2, 3), 'proteção e defesa civil.')
})

test('normalizeInciso remove marcador de lista e pontuação preexistente', () => {
  assert.equal(normalizeInciso('1. planejar as ações.', 0, 1), 'planejar as ações.')
  assert.equal(normalizeInciso('I - fiscalizar;', 0, 2), 'fiscalizar;')
})
