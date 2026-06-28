import { test } from 'node:test'
import assert from 'node:assert/strict'
import { buildPrompt, parseGeminiResposta } from './_gerarProposta.js'

test('buildPrompt inclui o texto atual e cada sugestão', () => {
  const p = buildPrompt('Art. 5º texto base.', ['trocar X por Y', 'incluir Z'])
  assert.match(p, /Art\. 5º texto base\./)
  assert.match(p, /trocar X por Y/)
  assert.match(p, /incluir Z/)
  assert.match(p, /APENAS/i) // instrução de responder só o texto
})

test('parseGeminiResposta extrai o texto da resposta', () => {
  const json = { candidates: [{ content: { parts: [{ text: '  Art. 5º final.  ' }] } }] }
  assert.equal(parseGeminiResposta(json), 'Art. 5º final.')
})

test('parseGeminiResposta lança quando vazio', () => {
  assert.throws(() => parseGeminiResposta({}), /vazia|inesperado/i)
})
