// Casca do "Subsídio" — uma página por minuta com sub-abas (Estrutura / Texto /
// LOB) que reusam os comparadores já existentes. Padrão idêntico nas duas
// trilhas; abas ainda não construídas para o Regulamento aparecem como "em breve".
import { useState } from 'react'

export default function SubsidioTabs({ trilha, tabs }) {
  const firstReal = tabs.find(t => !t.soon) || tabs[0]
  const [active, setActive] = useState(firstReal.id)
  const current = tabs.find(t => t.id === active) || firstReal

  return (
    <div className="subsidio">
      <div className="subsidio-bar">
        <span className="subsidio-eyebrow">Subsídio · {trilha}</span>
        <div className="subsidio-tabs" role="tablist">
          {tabs.map(t => (
            <button
              key={t.id} type="button" role="tab" aria-selected={active === t.id}
              className={`subsidio-tab${active === t.id ? ' is-on' : ''}`}
              onClick={() => setActive(t.id)}
            >
              {t.label}
              {t.soon && <span className="subsidio-soon">em breve</span>}
            </button>
          ))}
        </div>
      </div>
      <div className="subsidio-body">
        {current.soon ? (
          <div className="subsidio-empty">
            <b>{current.label} — em breve</b>
            <p>{current.soonNote || 'Esta aba seguirá o mesmo padrão do Regimento Interno quando for construída.'}</p>
          </div>
        ) : current.render()}
      </div>
    </div>
  )
}
