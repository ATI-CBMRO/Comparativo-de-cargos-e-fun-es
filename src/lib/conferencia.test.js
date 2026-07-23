import { test } from 'node:test'
import assert from 'node:assert/strict'
import { buildConferencia } from './conferencia.js'

const struct = {
  chapters: [
    {
      id: 'reg:tema-a', kind: 'organ', chapterTitle: 'TEMA A',
      alternatives: { se: { name: 'Sergipe', excerpts: [{ caput: 'Art. 1 SE' }] } },
      sections: [
        {
          kind: 'incisos', editId: 'reg:tema-a/mt-art-1', caput: 'Caput A',
          items: [{ text: 'item A', source: 'ro' }],
        },
      ],
    },
    {
      id: 'reg:tema-b', kind: 'organ', chapterTitle: 'TEMA B',
      sections: [
        {
          kind: 'incisos', editId: 'reg:tema-b/mt-art-2', caput: 'Caput B',
          items: [{ text: 'item B', source: 'ro' }],
        },
      ],
    },
  ],
}

test('buildConferencia numera contínuo e anexa alternatives do capítulo', () => {
  const lista = buildConferencia(struct)
  assert.equal(lista.length, 2)
  assert.equal(lista[0].dispositivo.number, 1)
  assert.equal(lista[1].dispositivo.number, 2)                 // contínuo, não reinicia
  assert.equal(lista[0].chapterId, 'reg:tema-a')
  assert.ok(lista[0].alternatives.se)                          // alternatives do capítulo A
  assert.deepEqual(lista[1].alternatives, {})                  // capítulo B sem alternatives
})
