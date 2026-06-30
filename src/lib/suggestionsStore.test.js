import { test } from 'node:test'
import assert from 'node:assert/strict'
import { createSuggestionsStore, MOCK_USERS } from './suggestionsStore.js'

function fakeStorage() {
  const m = new Map()
  return {
    getItem: k => (m.has(k) ? m.get(k) : null),
    setItem: (k, v) => m.set(k, String(v)),
    removeItem: k => m.delete(k),
  }
}

const base = {
  chapterId: 'organ:cg', targetId: 'organ:cg/competencia', targetKind: 'inciso',
  incisoIndex: 2, type: 'editar', originalText: 'dirigir', proposedText: 'comandar',
  authorId: 'u-costa',
}

test('addSuggestion grava autoria, status pendente e defaults', async () => {
  const store = createSuggestionsStore(fakeStorage())
  const s = await store.addSuggestion(base)
  assert.equal(s.authorId, 'u-costa')
  assert.equal(s.status, 'pendente')
  assert.deepEqual(s.supporters, [])
  assert.deepEqual(s.comments, [])
  assert.ok(s.id && s.createdAt)
})

test('listSuggestions filtra por chapterId e por targetId', async () => {
  const store = createSuggestionsStore(fakeStorage())
  await store.addSuggestion(base)
  await store.addSuggestion({ ...base, chapterId: 'organ:dp', targetId: 'organ:dp/competencia' })
  assert.equal((await store.listSuggestions()).length, 2)
  assert.equal((await store.listSuggestions({ chapterId: 'organ:cg' })).length, 1)
  assert.equal((await store.listSuggestions({ targetId: 'organ:dp/competencia' })).length, 1)
})

test('apoiar é idempotente e desapoiar remove', async () => {
  const store = createSuggestionsStore(fakeStorage())
  const s = await store.addSuggestion(base)
  await store.supportSuggestion(s.id, 'u-lima')
  await store.supportSuggestion(s.id, 'u-lima')
  let got = (await store.listSuggestions())[0]
  assert.deepEqual(got.supporters, ['u-lima'])
  await store.unsupportSuggestion(s.id, 'u-lima')
  got = (await store.listSuggestions())[0]
  assert.deepEqual(got.supporters, [])
})

test('decideSuggestion grava status e autor da decisão', async () => {
  const store = createSuggestionsStore(fakeStorage())
  const s = await store.addSuggestion(base)
  await store.decideSuggestion(s.id, 'aceita', 'u-costa')
  const got = (await store.listSuggestions())[0]
  assert.equal(got.status, 'aceita')
  assert.equal(got.decidedBy, 'u-costa')
  assert.ok(got.decidedAt)
})

test('getChapterCounts conta sugestões por capítulo', async () => {
  const store = createSuggestionsStore(fakeStorage())
  await store.addSuggestion(base)
  await store.addSuggestion({ ...base, type: 'remover' })
  await store.addSuggestion({ ...base, chapterId: 'organ:dp', targetId: 'organ:dp/competencia' })
  assert.deepEqual(await store.getChapterCounts(), { 'organ:cg': 2, 'organ:dp': 1 })
})

test('setFinalText/getItemResolution faz upsert e marca decidido', async () => {
  const store = createSuggestionsStore(fakeStorage())
  assert.equal((await store.getItemResolution('k1')).status, 'pendente')
  await store.setFinalText('k1', 'texto final', 'u-costa')
  const r = await store.getItemResolution('k1')
  assert.equal(r.finalText, 'texto final')
  assert.equal(r.status, 'decidido')
  assert.equal(r.resolvedBy, 'u-costa')
})

test('persiste entre instâncias que compartilham o mesmo storage', async () => {
  const storage = fakeStorage()
  const a = createSuggestionsStore(storage)
  await a.setCurrentUser('u-lima')
  await a.addSuggestion(base)
  const b = createSuggestionsStore(storage)
  assert.equal((await b.getCurrentUser()).id, 'u-lima')
  assert.equal((await b.listSuggestions()).length, 1)
})

test('getCurrentUser default = primeiro usuário; setCurrentUser troca', async () => {
  const store = createSuggestionsStore(fakeStorage())
  assert.equal((await store.getCurrentUser()).id, MOCK_USERS[0].id)
  await store.setCurrentUser('u-rocha')
  assert.equal((await store.getCurrentUser()).id, 'u-rocha')
})

test('resetDemo limpa tudo', async () => {
  const store = createSuggestionsStore(fakeStorage())
  await store.addSuggestion(base)
  await store.resetDemo()
  assert.equal((await store.listSuggestions()).length, 0)
})
