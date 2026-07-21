import test from 'node:test'
import assert from 'node:assert/strict'
import { PARTE_HEADERS, parteByChapterTitle } from './regulamentoPartes.js'

test('PARTE_HEADERS tem os dois rótulos em pt-BR', () => {
  assert.equal(PARTE_HEADERS.geral, 'PARTE I — GERAL')
  assert.equal(PARTE_HEADERS.servico, 'PARTE II — DO SERVIÇO')
})

test('parteByChapterTitle mapeia título→parte e ignora capítulos sem parte (compat RI)', () => {
  const structure = { chapters: [
    { chapterTitle: 'DAS DISPOSIÇÕES PRELIMINARES', parte: 'geral' },
    { chapterTitle: 'DO SERVIÇO OPERACIONAL', parte: 'servico' },
    { chapterTitle: 'CAPÍTULO SEM PARTE' },
  ] }
  assert.deepEqual(parteByChapterTitle(structure), {
    'DAS DISPOSIÇÕES PRELIMINARES': 'geral',
    'DO SERVIÇO OPERACIONAL': 'servico',
  })
})

test('parteByChapterTitle é seguro com estrutura vazia/nula', () => {
  assert.deepEqual(parteByChapterTitle(null), {})
  assert.deepEqual(parteByChapterTitle({}), {})
})
