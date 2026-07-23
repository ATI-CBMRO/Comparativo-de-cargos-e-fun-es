import { test } from 'node:test'
import assert from 'node:assert/strict'
import { applyFinalsToArticles } from './minutaFinals.js'

const articles = [
  { number: 1, editId: 'organ:cg/competencia', caput: 'Compete ao CG:',
    incisos: [{ text: 'planejar', index: 0 }, { text: 'dirigir', index: 2 }] },
  { number: 2, editId: 'preliminares', caput: 'Linha A', incisos: [] },
  { number: 3, editId: 'preliminares', caput: 'Linha B', incisos: [] },
]

test('aplica final de caput quando editId gera 1 artigo', () => {
  const finals = new Map([['organ:cg/competencia#caput', { texto: 'NOVO CAPUT', status: 'fechado' }]])
  const r = applyFinalsToArticles(articles, finals)
  assert.equal(r.articles[0].caput, 'NOVO CAPUT')
  assert.equal(r.articles[0].hasFinal, true)
  assert.equal(r.appliedCount, 1)
})

test('final de inciso casa pelo índice ORIGINAL', () => {
  const finals = new Map([['organ:cg/competencia#2', { texto: 'coordenar', status: 'fechado' }]])
  const r = applyFinalsToArticles(articles, finals)
  assert.equal(r.articles[0].incisos[1].text, 'coordenar')
  assert.equal(r.articles[0].incisos[0].text, 'planejar')
})

test('não aplica: status aberto, editId ambíguo (prosa), skipEditIds', () => {
  const finals = new Map([
    ['organ:cg/competencia#caput', { texto: 'X', status: 'aberto' }],
    ['preliminares#caput', { texto: 'Y', status: 'fechado' }],       // 2 artigos → ambíguo
  ])
  const r = applyFinalsToArticles(articles, finals)
  assert.equal(r.appliedCount, 0)
  const r2 = applyFinalsToArticles(articles,
    new Map([['organ:cg/competencia#caput', { texto: 'Z', status: 'fechado' }]]),
    { skipEditIds: new Set(['organ:cg/competencia']) })
  assert.equal(r2.appliedCount, 0)
})

test('mapa vazio/null é no-op', () => {
  assert.equal(applyFinalsToArticles(articles, null).appliedCount, 0)
  assert.equal(applyFinalsToArticles(articles, new Map()).articles, articles)
})

test('NÃO aplica final em inciso re-indexado (seção editada) — auditoria 2026-07-23', () => {
  // Cenário do bug: relator editou a seção removendo o 1º inciso; a linha que hoje
  // ocupa o índice 2 NÃO é o inciso original organ:cg/competencia#2. Antes do fix,
  // o final "coordenar" era aplicado nela em silêncio.
  const editados = articles.map(a => ({
    ...a,
    incisos: (a.incisos ?? []).map((inc, i) => ({ ...inc, index: i, reindexed: true })),
  }))
  const finals = new Map([['organ:cg/competencia#2', { texto: 'coordenar', status: 'fechado' }]])
  const r = applyFinalsToArticles(editados, finals)
  assert.equal(r.appliedCount, 0)
  assert.ok(r.articles[0].incisos.every(inc => inc.text !== 'coordenar'))
})
