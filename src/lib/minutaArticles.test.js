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

import { buildArticles } from './minutaArticles.js'

const ORGAN = {
  sections: [
    { id: 'preliminares', chapterTitle: 'DAS DISPOSIÇÕES PRELIMINARES', kind: 'prose', caput: null,
      proposedText: 'Primeiro artigo do objeto.\nSegundo artigo da base legal.' },
    { id: 'competencias', chapterTitle: 'DA COMPETÊNCIA', kind: 'incisos', caput: 'Compete à DPO:',
      proposedText: 'Coordenação operacional\nExecução das ações\nProteção civil' },
    { id: 'cargos_atribuicoes', chapterTitle: 'DAS ATRIBUIÇÕES DOS CARGOS', kind: 'cargos', caput: null,
      proposedText: 'Diretor:\n  planejar\n  coordenar\n\nAdjunto:\n  substituir o Diretor' },
  ],
}

test('buildArticles numera artigos continuamente e marca o 1º de cada capítulo', () => {
  const arts = buildArticles(ORGAN, {})
  assert.equal(arts.length, 5) // 2 prose + 1 incisos + 2 cargos
  assert.deepEqual(arts.map(a => a.number), [1, 2, 3, 4, 5])
  assert.equal(arts[0].chapterTitle, 'DAS DISPOSIÇÕES PRELIMINARES')
  assert.equal(arts[0].chapterNumber, 1)
  assert.equal(arts[1].chapterTitle, null) // 2º artigo do mesmo capítulo
  assert.equal(arts[2].chapterTitle, 'DA COMPETÊNCIA')
  assert.equal(arts[2].chapterNumber, 2)
  assert.equal(arts[3].chapterTitle, 'DAS ATRIBUIÇÕES DOS CARGOS')
  assert.equal(arts[3].chapterNumber, 3)
  assert.equal(arts[4].chapterTitle, null)
})

test('buildArticles articula incisos normalizados', () => {
  const arts = buildArticles(ORGAN, {})
  assert.equal(arts[2].caput, 'Compete à DPO:')
  assert.deepEqual(arts[2].incisos, [
    'coordenação operacional;',
    'execução das ações; e',
    'proteção civil.',
  ])
})

test('buildArticles monta artigo por cargo com caput "Ao ... compete:"', () => {
  const arts = buildArticles(ORGAN, {})
  assert.equal(arts[3].caput, 'Ao Diretor compete:')
  assert.deepEqual(arts[3].incisos, ['planejar;', 'coordenar.'])
  assert.equal(arts[4].caput, 'Ao Adjunto compete:')
  assert.deepEqual(arts[4].incisos, ['substituir o Diretor.'])
})

test('buildArticles usa edits no lugar do proposedText', () => {
  const arts = buildArticles(ORGAN, { competencias: 'Único item' })
  assert.deepEqual(arts[2].incisos, ['único item.'])
})
