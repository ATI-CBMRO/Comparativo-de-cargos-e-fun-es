import { test } from 'node:test'
import assert from 'node:assert/strict'
import {
  decisoesDaTrilha, filtrarDecisoes, contarDecisoes,
  cenariosDaDecisao, filtrarPorCenario, decisionDocId,
} from './decisoes.js'

const dados = {
  decisoes: [
    { trilha: 'ri', decidido: true },
    { trilha: 'ri', decidido: false },
    { trilha: 'reg', decidido: false },
  ],
}

test('decisoesDaTrilha filtra por trilha', () => {
  assert.equal(decisoesDaTrilha(dados, 'ri').length, 2)
  assert.equal(decisoesDaTrilha(dados, 'reg').length, 1)
  assert.deepEqual(decisoesDaTrilha(null, 'ri'), [])
})

test('filtrarDecisoes por status', () => {
  const ri = decisoesDaTrilha(dados, 'ri')
  assert.equal(filtrarDecisoes(ri, 'todas').length, 2)
  assert.equal(filtrarDecisoes(ri, 'pendentes').length, 1)
  assert.equal(filtrarDecisoes(ri, 'decididas').length, 1)
})

test('contarDecisoes soma total/decididas/pendentes', () => {
  assert.deepEqual(contarDecisoes(decisoesDaTrilha(dados, 'ri')),
    { total: 2, decididas: 1, pendentes: 1 })
})

const dadosComStatus = {
  decisoes: [
    { trilha: 'ri', decidido: false, statusDecisao: 'sistema' },
    { trilha: 'ri', decidido: true, statusDecisao: 'vault' },
    { trilha: 'ri', decidido: false, statusDecisao: 'pendente' },
  ],
}

test('com statusDecisao (merge Firebase): decide por statusDecisao, não por decidido', () => {
  const ri = decisoesDaTrilha(dadosComStatus, 'ri')
  assert.equal(filtrarDecisoes(ri, 'decididas').length, 2) // sistema + vault
  assert.equal(filtrarDecisoes(ri, 'pendentes').length, 1)
  assert.deepEqual(contarDecisoes(ri), { total: 3, decididas: 2, pendentes: 1 })
})

// --- Cenário (LOB atual × futura) ---
// A curadoria da Fase 2 (36 notas) foi toda redigida sobre a LOB FUTURA e não traz o
// campo `cenarios`; o padrão por trilha reproduz isso sem precisar reescrever o JSON.

const dadosCenario = {
  decisoes: [
    { id: 'ri-legado', trilha: 'ri', decidido: false },
    { id: 'reg-legado', trilha: 'reg', decidido: false },
    { id: 'ri-atual', trilha: 'ri', decidido: false, cenarios: ['atual'] },
    { id: 'ri-ambos', trilha: 'ri', decidido: false, cenarios: ['atual', 'futura'] },
  ],
}

test('cenariosDaDecisao: sem o campo, RI é da futura e Regulamento vale nos 2', () => {
  assert.deepEqual(cenariosDaDecisao({ trilha: 'ri' }), ['futura'])
  assert.deepEqual(cenariosDaDecisao({ trilha: 'reg' }), ['atual', 'futura'])
})

test('cenariosDaDecisao: campo explícito tem precedência sobre o padrão da trilha', () => {
  assert.deepEqual(cenariosDaDecisao({ trilha: 'ri', cenarios: ['atual'] }), ['atual'])
  assert.deepEqual(cenariosDaDecisao({ trilha: 'reg', cenarios: ['futura'] }), ['futura'])
})

test('filtrarPorCenario: as decisões do RI da futura NÃO aparecem no cenário atual', () => {
  const ri = decisoesDaTrilha(dadosCenario, 'ri')
  assert.deepEqual(filtrarPorCenario(ri, 'atual').map(d => d.id), ['ri-atual', 'ri-ambos'])
  assert.deepEqual(filtrarPorCenario(ri, 'futura').map(d => d.id), ['ri-legado', 'ri-ambos'])
})

test('filtrarPorCenario: Regulamento é temático — aparece nos 2 cenários', () => {
  const reg = decisoesDaTrilha(dadosCenario, 'reg')
  assert.equal(filtrarPorCenario(reg, 'atual').length, 1)
  assert.equal(filtrarPorCenario(reg, 'futura').length, 1)
})

test('decisionDocId: atual carimba marcador; futura fica sem (preserva registros)', () => {
  assert.equal(decisionDocId('Decisão — x', 'atual'), 'atual:Decisão — x')
  assert.equal(decisionDocId('Decisão — x', 'futura'), 'Decisão — x')
})
