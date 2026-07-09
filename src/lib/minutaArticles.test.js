import { test } from 'node:test'
import assert from 'node:assert/strict'
import { articleLabel, romanize, normalizeInciso, hasOwnMarker } from './minutaArticles.js'

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

test('hasOwnMarker reconhece Parágrafo único e § como marcador próprio', () => {
  assert.equal(hasOwnMarker('Parágrafo único. Em casos excepcionais...'), true)
  assert.equal(hasOwnMarker('§ 1º Nos casos previstos...'), true)
  assert.equal(hasOwnMarker('Coordenação operacional'), false)
  assert.equal(hasOwnMarker('I - fiscalizar;'), false)
})

test('normalizeInciso preserva verbatim dispositivos com marcador próprio', () => {
  const texto = 'Parágrafo único. Em casos excepcionais, devidamente autoriz ado pelo DOp.'
  assert.equal(normalizeInciso(texto, 0, 1), texto)
  assert.equal(normalizeInciso('§ 2º Não se aplica ao pessoal civil.', 1, 3), '§ 2º Não se aplica ao pessoal civil.')
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
  assert.deepEqual(arts.map(a => a.number), [1, 2, 3, 4, 5])
})

test('buildArticles marca capítulo no 1º artigo e numera capítulos em sequência', () => {
  const arts = buildArticles(STRUCTURE, {})
  assert.equal(arts[0].chapterTitle, 'DAS DISPOSIÇÕES PRELIMINARES')
  assert.equal(arts[0].chapterNumber, 1)
  assert.equal(arts[1].chapterTitle, null)
  assert.equal(arts[2].chapterTitle, 'DA ESTRUTURA ORGANIZACIONAL')
  assert.equal(arts[2].chapterNumber, 2)
  assert.equal(arts[3].chapterNumber, 3)
})

test('buildArticles numera seções por capítulo e marca no 1º artigo da seção', () => {
  const arts = buildArticles(STRUCTURE, {})
  assert.equal(arts[3].sectionNumber, 1)
  assert.equal(arts[3].sectionTitle, 'Da Competência')
})

test('cada artigo carrega o editId da sua folha de origem', () => {
  const arts = buildArticles(STRUCTURE, {})
  assert.equal(arts[0].editId, 'preliminares')
  assert.equal(arts[2].editId, 'estrutura')
  assert.equal(arts[3].editId, 'organ:dpo/competencia')
  assert.equal(arts[4].editId, 'organ:dpo/cargo:diretor')
})

test('incisos carregam texto normalizado, fonte, editId e index original', () => {
  const arts = buildArticles(STRUCTURE, {})
  assert.deepEqual(arts[3].incisos, [
    { text: 'planejar as operações; e', ownMarker: false, source: 'ro', editId: 'organ:dpo/competencia', index: 0 },
    { text: 'fiscalizar a instrução.', ownMarker: false, source: 'cf. CBMAL, RI, Art. 115, VII', editId: 'organ:dpo/competencia', index: 1 },
  ])
})

test('incisos com marcador próprio (Parágrafo único/§) ganham ownMarker:true e texto verbatim', () => {
  const structure = {
    chapters: [{
      id: 'estrutura', kind: 'incisos', chapterTitle: 'DA ESTRUTURA',
      editId: 'estrutura', caput: 'Compete ao órgão:',
      items: [
        { text: 'planejar as ações', source: 'ro' },
        { text: 'Parágrafo único. Em casos excepcionais, o chefe decide.', source: 'ro' },
      ],
    }],
  }
  const arts = buildArticles(structure, {})
  assert.equal(arts[0].incisos[0].ownMarker, false)
  assert.equal(arts[0].incisos[1].ownMarker, true)
  assert.equal(arts[0].incisos[1].text, 'Parágrafo único. Em casos excepcionais, o chefe decide.')
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
    { text: 'item editado; e', ownMarker: false, source: null, editId: 'organ:dpo/cargo:diretor', index: 0 },
    { text: 'outro item.', ownMarker: false, source: null, editId: 'organ:dpo/cargo:diretor', index: 1 },
  ])
})

test('isExcluded pula o inciso e renumera os restantes (sufixo recalculado)', () => {
  const isExcluded = (editId, i) => editId === 'organ:dpo/competencia' && i === 0
  const arts = buildArticles(STRUCTURE, {}, isExcluded)
  const comp = arts.find(a => a.caput === 'Compete à DPO:')
  assert.deepEqual(comp.incisos, [
    { text: 'fiscalizar a instrução.', ownMarker: false, source: 'cf. CBMAL, RI, Art. 115, VII', editId: 'organ:dpo/competencia', index: 1 },
  ])
})

test('seção com todos os incisos excluídos é omitida e a numeração permanece contígua', () => {
  const isExcluded = (editId) => editId === 'organ:dpo/cargo:diretor'
  const arts = buildArticles(STRUCTURE, {}, isExcluded)
  assert.equal(arts.find(a => a.caput === 'Ao Diretor compete:'), undefined)
  assert.deepEqual(arts.map(a => a.number), [1, 2, 3, 4])
})

test('buildArticles: capítulo kind "articles" gera um artigo por folha sob um único título de capítulo', () => {
  const structure = {
    chapters: [
      {
        id: 'estrutura', kind: 'articles', chapterTitle: 'DA ESTRUTURA ORGANIZACIONAL',
        editId: 'estrutura',
        articles: [
          { id: 'direcao', kind: 'incisos', editId: 'estrutura/direcao',
            caput: 'São Órgãos de Direção Operacional:',
            items: [
              { text: 'de Direção Setorial: a DPO, a DOE e o COT', source: 'ro' },
              { text: 'de Direção Regional: o CRBM', source: 'ro' },
            ] },
          { id: 'execucao', kind: 'incisos', editId: 'estrutura/execucao',
            caput: 'Os Órgãos de Execução classificam-se em:',
            items: [{ text: 'Atuação Operacional Ordinária: o BBM', source: 'ro' }] },
        ],
      },
    ],
  }
  const arts = buildArticles(structure, {})
  assert.equal(arts.length, 2)
  assert.equal(arts[0].number, 1)
  assert.equal(arts[0].chapterNumber, 1)
  assert.equal(arts[0].chapterTitle, 'DA ESTRUTURA ORGANIZACIONAL')
  assert.equal(arts[0].editId, 'estrutura/direcao')
  assert.equal(arts[0].sectionNumber, null)
  assert.equal(arts[1].number, 2)
  assert.equal(arts[1].chapterTitle, null)
  assert.equal(arts[1].editId, 'estrutura/execucao')
})
