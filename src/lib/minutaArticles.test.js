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
  assert.equal(normalizeInciso('I - fiscalizar;', 0, 2), 'fiscalizar; e')
})

import { buildArticles } from './minutaArticles.js'

const STRUCTURE = {
  chapters: [
    {
      id: 'preliminares', kind: 'prose', chapterTitle: 'DAS DISPOSIÇÕES PRELIMINARES',
      editId: 'preliminares',
      proposedText: 'Primeiro artigo do objeto.\nSegundo artigo da base legal.',
    },
    {
      id: 'estrutura', kind: 'incisos', chapterTitle: 'DA ESTRUTURA ORGANIZACIONAL',
      editId: 'estrutura', caput: 'A estrutura operacional compõe-se dos órgãos:',
      items: [{ text: 'a DPO', source: 'ro' }, { text: 'o COT', source: 'ro' }],
    },
    {
      id: 'organ:dpo', kind: 'organ', chapterTitle: 'DA DIRETORIA DE PLANEJAMENTO OPERACIONAL (DPO)',
      organKey: 'dpo', label: 'Diretoria de Planejamento Operacional', abbr: 'DPO',
      sections: [
        {
          id: 'competencia', kind: 'incisos', sectionTitle: 'Da Competência',
          editId: 'organ:dpo/competencia', caput: 'Compete à DPO:',
          items: [
            { text: 'planejar as operações', source: 'ro' },
            { text: 'fiscalizar a instrução', source: 'cf. CBMAL, RI, Art. 115, VII' },
          ],
        },
        {
          id: 'cargo:diretor', kind: 'incisos', sectionTitle: 'Das Atribuições do Diretor',
          editId: 'organ:dpo/cargo:diretor', caput: 'Ao Diretor compete:',
          items: [{ text: 'dirigir a DPO', source: 'ro' }],
        },
      ],
    },
  ],
}

test('buildArticles numera artigos continuamente atravessando capítulos', () => {
  const arts = buildArticles(STRUCTURE, {})
  // 2 prose (preliminares) + 1 incisos (estrutura) + 2 seções do órgão DPO (competência, cargo:diretor)
  assert.deepEqual(arts.map(a => a.number), [1, 2, 3, 4, 5])
})

test('buildArticles marca capítulo no 1º artigo e numera capítulos em sequência', () => {
  const arts = buildArticles(STRUCTURE, {})
  assert.equal(arts[0].chapterTitle, 'DAS DISPOSIÇÕES PRELIMINARES')
  assert.equal(arts[0].chapterNumber, 1)
  assert.equal(arts[1].chapterTitle, null)            // mesmo capítulo
  assert.equal(arts[2].chapterTitle, 'DA ESTRUTURA ORGANIZACIONAL')
  assert.equal(arts[2].chapterNumber, 2)
  assert.equal(arts[3].chapterNumber, 3)              // capítulo do órgão DPO
})

test('buildArticles numera seções por capítulo e marca no 1º artigo da seção', () => {
  const arts = buildArticles(STRUCTURE, {})
  // arts[3] = 1º artigo do capítulo do órgão = 1ª seção (Competência)
  assert.equal(arts[3].sectionNumber, 1)
  assert.equal(arts[3].sectionTitle, 'Da Competência')
})

test('buildArticles preserva a fonte de cada inciso e normaliza o texto', () => {
  const arts = buildArticles(STRUCTURE, {})
  assert.deepEqual(arts[3].incisos, [
    { text: 'planejar as operações; e', source: 'ro' },
    { text: 'fiscalizar a instrução.', source: 'cf. CBMAL, RI, Art. 115, VII' },
  ])
})

test('buildArticles articula prose como um artigo por linha', () => {
  const arts = buildArticles(STRUCTURE, {})
  assert.equal(arts[0].caput, 'Primeiro artigo do objeto.')
  assert.deepEqual(arts[0].incisos, [])
  assert.equal(arts[1].caput, 'Segundo artigo da base legal.')
})

test('buildArticles usa edits (texto) no lugar dos itens, com source nulo', () => {
  const arts = buildArticles(STRUCTURE, { 'organ:dpo/cargo:diretor': 'item editado\noutro item' })
  const diretor = arts.find(a => a.caput === 'Ao Diretor compete:')
  assert.deepEqual(diretor.incisos, [
    { text: 'item editado; e', source: null },
    { text: 'outro item.', source: null },
  ])
})
