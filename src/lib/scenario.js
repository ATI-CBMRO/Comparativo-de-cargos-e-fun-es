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
