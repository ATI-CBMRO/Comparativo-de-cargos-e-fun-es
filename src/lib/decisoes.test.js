import { test } from 'node:test'
import assert from 'node:assert/strict'
import { decisoesDaTrilha, filtrarDecisoes, contarDecisoes } from './decisoes.js'

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
