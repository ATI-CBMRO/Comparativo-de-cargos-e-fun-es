import { test } from 'node:test'
import assert from 'node:assert/strict'
import { applyDecisionsToEdits } from './minutaConsolidation.js'

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
          ],
        },
      ],
    },
  ],
}

const sug = (p) => ({
  id: 'x', chapterId: 'organ:cg', targetId: 'organ:cg/competencia', targetKind: 'inciso',
  status: 'aceita', proposedText: '', incisoIndex: null, type: 'editar', ...p,
})

test('editar troca o texto do inciso pelo índice', () => {
  const edits = applyDecisionsToEdits(STRUCTURE, [
    sug({ type: 'editar', incisoIndex: 0, proposedText: 'comandar a Corporação' }),
  ])
  assert.equal(edits['organ:cg/competencia'], 'comandar a Corporação\ndirigir a Corporação')
})

test('remover descarta o inciso e incluir anexa ao fim', () => {
  const edits = applyDecisionsToEdits(STRUCTURE, [
    sug({ type: 'remover', incisoIndex: 1 }),
    sug({ type: 'incluir', proposedText: 'fiscalizar o serviço' }),
  ])
  assert.equal(edits['organ:cg/competencia'], 'planejar as ações\nfiscalizar o serviço')
})

test('ignora sugestões não aceitas', () => {
  const edits = applyDecisionsToEdits(STRUCTURE, [
    sug({ type: 'editar', incisoIndex: 0, proposedText: 'X', status: 'pendente' }),
    sug({ type: 'editar', incisoIndex: 0, proposedText: 'Y', status: 'rejeitada' }),
  ])
  assert.deepEqual(edits, {})
})
