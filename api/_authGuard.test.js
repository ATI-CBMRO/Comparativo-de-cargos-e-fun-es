import { test } from 'node:test'
import assert from 'node:assert/strict'
import { validarPayload, verificarIdToken, verificarMembro, checarRateLimit } from './_authGuard.js'

test('validarPayload aceita payload dentro dos limites', () => {
  assert.doesNotThrow(() => validarPayload({ textoAtual: 'Art. 5º.', sugestoes: ['ok'] }))
})

test('validarPayload rejeita corpo maior que o limite', () => {
  assert.throws(
    () => validarPayload({ textoAtual: 'x', sugestoes: [], rawSize: 999999 }),
    (e) => e.status === 413,
  )
})

test('validarPayload rejeita textoAtual muito longo', () => {
  assert.throws(
    () => validarPayload({ textoAtual: 'a'.repeat(5000), sugestoes: [] }),
    (e) => e.status === 400,
  )
})

test('validarPayload rejeita mais de 30 sugestões', () => {
  assert.throws(
    () => validarPayload({ textoAtual: 'ok', sugestoes: Array(31).fill('s') }),
    (e) => e.status === 400,
  )
})

test('validarPayload rejeita sugestão individual muito longa', () => {
  assert.throws(
    () => validarPayload({ textoAtual: 'ok', sugestoes: ['a'.repeat(2001)] }),
    (e) => e.status === 400,
  )
})

test('verificarIdToken lança 401 sem token', async () => {
  await assert.rejects(() => verificarIdToken('', 'fake-key'), (e) => e.status === 401)
})

test('verificarIdToken lança 401 quando o Identity Toolkit rejeita', async (t) => {
  const originalFetch = global.fetch
  global.fetch = async () => ({ ok: false })
  t.after(() => { global.fetch = originalFetch })
  await assert.rejects(() => verificarIdToken('token-invalido', 'fake-key'), (e) => e.status === 401)
})

test('verificarIdToken retorna e-mail normalizado quando válido', async (t) => {
  const originalFetch = global.fetch
  global.fetch = async () => ({
    ok: true,
    json: async () => ({ users: [{ email: 'ADMIN@Exemplo.com' }] }),
  })
  t.after(() => { global.fetch = originalFetch })
  const email = await verificarIdToken('token-valido', 'fake-key')
  assert.equal(email, 'admin@exemplo.com')
})

test('verificarMembro lança 403 quando o documento não existe', async (t) => {
  const originalFetch = global.fetch
  global.fetch = async () => ({ ok: false })
  t.after(() => { global.fetch = originalFetch })
  await assert.rejects(
    () => verificarMembro('token', 'proj', 'ninguem@exemplo.com'),
    (e) => e.status === 403,
  )
})

test('verificarMembro lança 403 quando ativo mas não é admin', async (t) => {
  const originalFetch = global.fetch
  global.fetch = async () => ({
    ok: true,
    json: async () => ({ fields: { ativo: { booleanValue: true }, role: { stringValue: 'participante' } } }),
  })
  t.after(() => { global.fetch = originalFetch })
  await assert.rejects(
    () => verificarMembro('token', 'proj', 'participante@exemplo.com'),
    (e) => e.status === 403,
  )
})

test('verificarMembro passa quando ativo e admin', async (t) => {
  const originalFetch = global.fetch
  global.fetch = async () => ({
    ok: true,
    json: async () => ({ fields: { ativo: { booleanValue: true }, role: { stringValue: 'admin' } } }),
  })
  t.after(() => { global.fetch = originalFetch })
  await assert.doesNotReject(() => verificarMembro('token', 'proj', 'admin@exemplo.com'))
})

test('checarRateLimit permite até o limite e bloqueia depois', () => {
  const email = `rate-${Math.floor(Math.random() * 1e9)}@exemplo.com`
  const now = 1000000
  for (let i = 0; i < 8; i++) {
    assert.doesNotThrow(() => checarRateLimit(email, now + i))
  }
  assert.throws(() => checarRateLimit(email, now + 8), (e) => e.status === 429)
})

test('checarRateLimit libera após a janela de tempo', () => {
  const email = `rate-janela-${Math.floor(Math.random() * 1e9)}@exemplo.com`
  const now = 2000000
  for (let i = 0; i < 8; i++) checarRateLimit(email, now + i)
  assert.doesNotThrow(() => checarRateLimit(email, now + 61000))
})
