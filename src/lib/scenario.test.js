import { test } from 'node:test'
import assert from 'node:assert/strict'
import { SCENARIOS, DEFAULT_SCENARIO, normalizeScenario, resolveScenario, scenarioDbUrl } from './scenario.js'

test('SCENARIOS e padrão', () => {
  assert.deepEqual([...SCENARIOS], ['futura', 'atual'])
  assert.equal(DEFAULT_SCENARIO, 'futura')
})

test('normalizeScenario aceita válidos e cai no padrão nos inválidos', () => {
  assert.equal(normalizeScenario('atual'), 'atual')
  assert.equal(normalizeScenario('futura'), 'futura')
  assert.equal(normalizeScenario('xpto'), 'futura')
  assert.equal(normalizeScenario(null), 'futura')
  assert.equal(normalizeScenario(undefined), 'futura')
})

test('resolveScenario prioriza a URL quando válida', () => {
  assert.equal(resolveScenario('atual', 'futura'), 'atual')
  assert.equal(resolveScenario('futura', 'atual'), 'futura')
})

test('resolveScenario usa o armazenamento quando a URL é inválida/ausente', () => {
  assert.equal(resolveScenario(null, 'atual'), 'atual')
  assert.equal(resolveScenario('lixo', 'atual'), 'atual')
})

test('resolveScenario cai no padrão quando URL e armazenamento são inválidos', () => {
  assert.equal(resolveScenario(null, null), 'futura')
  assert.equal(resolveScenario('', 'nada'), 'futura')
})

test('scenarioDbUrl: futura usa a raiz de /database (caminho de hoje)', () => {
  assert.equal(scenarioDbUrl('futura', 'minuta_structure.json'), '/database/minuta_structure.json')
})

test('scenarioDbUrl: atual usa a subpasta /database/atual', () => {
  assert.equal(scenarioDbUrl('atual', 'minuta_structure.json'), '/database/atual/minuta_structure.json')
})

test('scenarioDbUrl: cenário inválido cai no padrão (futura/raiz)', () => {
  assert.equal(scenarioDbUrl('xpto', 'regulamento_structure.json'), '/database/regulamento_structure.json')
})
