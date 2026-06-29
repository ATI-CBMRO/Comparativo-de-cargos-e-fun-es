import { test } from 'node:test'
import assert from 'node:assert/strict'
import { applyResolutionsToEdits } from './minutaConsolidation.js'

const STRUCTURE = {
  chapters: [
    {
      id: 'organ:cg', kind: 'organ', chapterTitle: 'DO COMANDO-GERAL (CG)',
      organKey: 'cg', abbr: 'CG',
      sections: [
        {
          id: 'competencia', kind: 'incisos', sectionTitle: 'Da Competência',
          editId: 'organ:cg/competencia', caput: 'Compete ao CG:',
          items: [
            { text: 'planejar as ações', source: 'ro' },
            { text: 'dirigir a Corporação', source: 'ro' },
            { text: 'representar o CBMRO', source: 'ro' },
          ],
        },
      ],
    },
  ],
}

const res = (status, finalText) => ({ status, finalText })

test('usa o texto final aprovado no lugar do inciso original', () => {
  const edits = applyResolutionsToEdits(STRUCTURE, {
    'organ:cg/competencia#0': res('decidido', 'comandar e dirigir a Corporação'),
  })
  assert.equal(edits['organ:cg/competencia'], 'comandar e dirigir a Corporação\ndirigir a Corporação\nrepresentar o CBMRO')
})

test('finalText vazio remove o inciso', () => {
  const edits = applyResolutionsToEdits(STRUCTURE, {
    'organ:cg/competencia#1': res('decidido', ''),
  })
  assert.equal(edits['organ:cg/competencia'], 'planejar as ações\nrepresentar o CBMRO')
})

test('ignora resoluções pendentes e chaves sem item cru', () => {
  const edits = applyResolutionsToEdits(STRUCTURE, {
    'organ:cg/competencia#0': res('pendente', 'X'),
    'preliminares': res('decidido', 'algo'),
  })
  assert.deepEqual(edits, {})
})
