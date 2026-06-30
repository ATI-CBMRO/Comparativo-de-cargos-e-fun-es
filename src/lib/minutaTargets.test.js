import { test } from 'node:test'
import assert from 'node:assert/strict'
import { buildTargets, chapterIdOf, itemKeyOf } from './minutaTargets.js'

test('chapterIdOf extrai o prefixo do editId', () => {
  assert.equal(chapterIdOf('organ:cg/competencia'), 'organ:cg')
  assert.equal(chapterIdOf('estrutura/direcao'), 'estrutura')
  assert.equal(chapterIdOf('preliminares'), 'preliminares')
})

test('itemKeyOf compõe a chave do item', () => {
  assert.equal(itemKeyOf('organ:cg/competencia', 2), 'organ:cg/competencia#2')
  assert.equal(itemKeyOf('preliminares', null), 'preliminares')
})

const STRUCTURE = {
  chapters: [
    {
      id: 'preliminares', kind: 'prose', chapterTitle: 'DAS DISPOSIÇÕES PRELIMINARES',
      editId: 'preliminares', proposedText: 'Primeiro artigo.\nSegundo artigo.',
    },
    {
      id: 'organ:cg', kind: 'organ', chapterTitle: 'DO COMANDO-GERAL (CG)',
      organKey: 'cg', label: 'Comando-Geral', abbr: 'CG',
      sections: [
        {
          id: 'competencia', kind: 'incisos', sectionTitle: 'Da Competência',
          editId: 'organ:cg/competencia', caput: 'Compete ao CG:',
          items: [
            { text: 'planejar as ações', source: 'ro' },
            { text: 'dirigir a Corporação', source: 'ro' },
          ],
        },
      ],
    },
  ],
}

test('buildTargets agrupa por capítulo com chapterId/título/número', () => {
  const chs = buildTargets(STRUCTURE)
  assert.equal(chs.length, 2)
  assert.equal(chs[0].chapterId, 'preliminares')
  assert.equal(chs[0].chapterTitle, 'DAS DISPOSIÇÕES PRELIMINARES')
  assert.equal(chs[1].chapterId, 'organ:cg')
  assert.equal(chs[1].chapterNumber, 2)
})

test('buildTargets expõe incisos com index original e editId da seção', () => {
  const chs = buildTargets(STRUCTURE)
  const comp = chs[1].articles.find(a => a.caput === 'Compete ao CG:')
  assert.equal(comp.editId, 'organ:cg/competencia')
  assert.equal(comp.sectionTitle, 'Da Competência')
  assert.deepEqual(comp.incisos.map(i => i.index), [0, 1])
  assert.equal(comp.incisos[0].text, 'planejar as ações; e')
})
