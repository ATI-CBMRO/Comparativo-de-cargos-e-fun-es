// Lógica pura do cenário (LOB atual × LOB futura). Sem React — testável com node --test.
// 'futura' = LOB em aprovação (arquivos de dados de hoje). 'atual' = LOB vigente (Fase 2).
export const SCENARIOS = Object.freeze(['futura', 'atual'])
export const DEFAULT_SCENARIO = 'futura'

export function normalizeScenario(value) {
  return SCENARIOS.includes(value) ? value : DEFAULT_SCENARIO
}

// Prioridade: valor válido na URL > valor armazenado (localStorage) > padrão.
export function resolveScenario(urlValue, storedValue) {
  if (SCENARIOS.includes(urlValue)) return urlValue
  return normalizeScenario(storedValue)
}

// Caminho do arquivo de dados por cenário. A LOB futura permanece na raiz de
// /database (arquivos de hoje, intocados); a LOB atual vive em /database/atual/.
// `file` é o nome do arquivo específico de cenário (ex.: 'minuta_structure.json').
export function scenarioDbUrl(cenario, file) {
  return normalizeScenario(cenario) === 'atual'
    ? `/database/atual/${file}`
    : `/database/${file}`
}

// Duas VERSÕES do Regulamento no cenário atual (curadoria da consulta, 2026-09-14):
// 'consulta' = a minuta exatamente como foi lida pelos militares, onde os
// comentários ficam ancorados; 'atual' = a versão produzida após as sugestões. A futura
// não tem versão em consulta — cai sempre no arquivo único.
export const VERSOES_REGULAMENTO = Object.freeze(['atual', 'consulta'])
export function regulamentoFile(versao) {
  return versao === 'consulta' ? 'regulamento_structure_consulta.json' : 'regulamento_structure.json'
}
export function regulamentoDbUrl(cenario, versao) {
  const c = normalizeScenario(cenario)
  return scenarioDbUrl(c, c === 'atual' ? regulamentoFile(versao) : 'regulamento_structure.json')
}
