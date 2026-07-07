import { test } from 'node:test'
import assert from 'node:assert/strict'
import { fetchJson, clearJsonCache } from './dataCache.js'

test('fetchJson resolve o JSON quando a resposta é ok', async (t) => {
  const originalFetch = global.fetch
  let calls = 0
  global.fetch = async () => { calls += 1; return { ok: true, status: 200, json: async () => ({ a: 1 }) } }
  t.after(() => { global.fetch = originalFetch; clearJsonCache() })

  const data = await fetchJson('/x/ok.json')
  assert.deepEqual(data, { a: 1 })
  assert.equal(calls, 1)
})

test('fetchJson deduplica chamadas simultâneas para a mesma URL', async (t) => {
  const originalFetch = global.fetch
  let calls = 0
  global.fetch = async () => { calls += 1; return { ok: true, status: 200, json: async () => ({ ok: true }) } }
  t.after(() => { global.fetch = originalFetch; clearJsonCache() })

  const [a, b] = await Promise.all([fetchJson('/x/dedupe.json'), fetchJson('/x/dedupe.json')])
  assert.deepEqual(a, { ok: true })
  assert.deepEqual(b, { ok: true })
  assert.equal(calls, 1)
})

test('fetchJson rejeita e não cacheia falha (HTTP não-2xx)', async (t) => {
  const originalFetch = global.fetch
  let calls = 0
  global.fetch = async () => { calls += 1; return { ok: false, status: 500, json: async () => ({}) } }
  t.after(() => { global.fetch = originalFetch; clearJsonCache() })

  await assert.rejects(() => fetchJson('/x/erro.json'), /HTTP 500/)
  await assert.rejects(() => fetchJson('/x/erro.json'))
  assert.equal(calls, 2, 'uma falha não deve ficar em cache — a próxima chamada tenta de novo')
})

test('fetchJson com optional:true resolve null em 404', async (t) => {
  const originalFetch = global.fetch
  global.fetch = async () => ({ ok: false, status: 404, json: async () => ({}) })
  t.after(() => { global.fetch = originalFetch; clearJsonCache() })

  const data = await fetchJson('/x/talvez.json', { optional: true })
  assert.equal(data, null)
})

test('clearJsonCache(url) força um novo fetch só para aquela URL', async (t) => {
  const originalFetch = global.fetch
  let calls = 0
  global.fetch = async () => { calls += 1; return { ok: true, status: 200, json: async () => ({ n: calls }) } }
  t.after(() => { global.fetch = originalFetch; clearJsonCache() })

  const first = await fetchJson('/x/limpa.json')
  clearJsonCache('/x/limpa.json')
  const second = await fetchJson('/x/limpa.json')
  assert.equal(first.n, 1)
  assert.equal(second.n, 2)
})
