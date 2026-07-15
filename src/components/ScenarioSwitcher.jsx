import { useScenario } from '../context/ScenarioContext.jsx'

const OPCOES = [
  { id: 'atual', label: 'LOB atual', hint: 'Vigente' },
  { id: 'futura', label: 'LOB futura', hint: 'Em aprovação' },
]

export default function ScenarioSwitcher() {
  const { cenario, setCenario } = useScenario()
  return (
    <div className={`scenario-switcher scenario-${cenario}`} role="group" aria-label="Cenário de LOB">
      <div className="scenario-switcher-label">Cenário</div>
      <div className="scenario-switcher-tabs">
        {OPCOES.map((o) => (
          <button
            key={o.id}
            type="button"
            className={`scenario-tab${cenario === o.id ? ' is-active' : ''}`}
            aria-pressed={cenario === o.id}
            onClick={() => setCenario(o.id)}
            title={`${o.label} — ${o.hint}`}
          >
            <strong>{o.label}</strong>
            <span>{o.hint}</span>
          </button>
        ))}
      </div>
    </div>
  )
}
