import { createContext, useContext, useCallback, useEffect, useMemo } from 'react'
import { useSearchParams } from 'react-router-dom'
import { resolveScenario, normalizeScenario, DEFAULT_SCENARIO, SCENARIOS } from '../lib/scenario.js'

const STORAGE_KEY = 'portal-cbm.cenario'
const ScenarioContext = createContext(null)

function readStored() {
  try { return localStorage.getItem(STORAGE_KEY) } catch { return null }
}
function writeStored(cenario) {
  try { localStorage.setItem(STORAGE_KEY, cenario) } catch { /* ignora storage indisponível */ }
}

export function ScenarioProvider({ children }) {
  const [searchParams, setSearchParams] = useSearchParams()
  // Cenário ativo é derivado da URL (fonte da verdade), com fallback no armazenamento.
  const cenario = resolveScenario(searchParams.get('cenario'), readStored())

  // Mantém o armazenamento em dia com o cenário efetivo (ex.: primeira visita sem URL).
  useEffect(() => { writeStored(cenario) }, [cenario])

  // Garante que a URL seja sempre autoexplicativa: se faltar `?cenario` (ou vier
  // inválido), carimba o cenário resolvido na URL. Só escreve quando necessário,
  // para não entrar em loop de renderização.
  useEffect(() => {
    const atual = searchParams.get('cenario')
    if (!SCENARIOS.includes(atual)) {
      setSearchParams((prev) => {
        const p = new URLSearchParams(prev)
        p.set('cenario', cenario)
        return p
      }, { replace: true })
    }
  }, [cenario, searchParams, setSearchParams])

  const setCenario = useCallback((next) => {
    const c = normalizeScenario(next)
    writeStored(c)
    setSearchParams((prev) => {
      const p = new URLSearchParams(prev)
      p.set('cenario', c)
      return p
    }, { replace: true })
  }, [setSearchParams])

  const value = useMemo(() => ({ cenario, setCenario }), [cenario, setCenario])
  return <ScenarioContext.Provider value={value}>{children}</ScenarioContext.Provider>
}

export function useScenario() {
  const ctx = useContext(ScenarioContext)
  if (!ctx) throw new Error('useScenario deve ser usado dentro de <ScenarioProvider>')
  return ctx
}

export { DEFAULT_SCENARIO }
