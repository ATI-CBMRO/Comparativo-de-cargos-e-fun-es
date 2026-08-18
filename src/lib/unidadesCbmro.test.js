import { test } from 'node:test'
import assert from 'node:assert/strict'
import { cidadesDisponiveis, comandosPorCidade, unidadesPorCidadeEComando } from './unidadesCbmro.js'

test('cidadesDisponiveis: 17 cidades reais, ordenadas, sem repetição', () => {
  const cidades = cidadesDisponiveis()
  assert.equal(cidades.length, 17)
  assert.ok(cidades.includes('Porto Velho'))
  assert.ok(cidades.includes('Buritis'))
  assert.deepEqual(cidades, [...cidades].sort((a, b) => a.localeCompare(b, 'pt-BR')))
})

test('comandosPorCidade: cidade-satélite tem COB e CAT', () => {
  assert.deepEqual(comandosPorCidade('Buritis'), ['CAT', 'COB I'])
})

test('comandosPorCidade: Vilhena também tem CEEI (CMDPII-2)', () => {
  assert.deepEqual(comandosPorCidade('Vilhena'), ['CAT', 'CEEI', 'COB II'])
})

test('comandosPorCidade: Porto Velho concentra os comandos administrativos', () => {
  const comandos = comandosPorCidade('Porto Velho')
  assert.equal(comandos.length, 14)
  assert.ok(comandos.includes('COB I'))
  assert.ok(comandos.includes('CAT'))
  assert.ok(comandos.includes('Corregedoria'))
})

test('comandosPorCidade: cidade inexistente retorna lista vazia', () => {
  assert.deepEqual(comandosPorCidade('Cidade Que Não Existe'), [])
})

test('unidadesPorCidadeEComando: Buritis/CAT tem só o SAT local', () => {
  assert.deepEqual(unidadesPorCidadeEComando('Buritis', 'CAT'), ['DAT - Ariquemes / SAT - Buritis'])
})

test('unidadesPorCidadeEComando: Buritis/COB I tem só o SGBM local', () => {
  assert.deepEqual(unidadesPorCidadeEComando('Buritis', 'COB I'), ['5º GBM / 3º SGBM'])
})

test('unidadesPorCidadeEComando: Porto Velho/COB I tem 3 unidades, ordenadas', () => {
  assert.deepEqual(
    unidadesPorCidadeEComando('Porto Velho', 'COB I'),
    ['1º GBM', '1º GBM / 1º SGBM', 'GBS'],
  )
})
