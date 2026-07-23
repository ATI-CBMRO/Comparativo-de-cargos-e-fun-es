import { useMemo } from 'react'
import { renderFriendlyText, List } from '../lib/comparatorRender.jsx'

export function MatchBadge({ match }) {
  const cfg = {
    exata: { cls: 'rg-badge-exata', label: 'exata' },
    parcial: { cls: 'rg-badge-parcial', label: 'parcial' },
    tematica: { cls: 'rg-badge-tematica', label: 'temática' },
    auto: { cls: 'rg-badge-tematica', label: 'auto' },
  }[match] ?? { cls: 'rg-badge-tematica', label: match || '—' }
  return <span className={`rg-badge ${cfg.cls}`}>{cfg.label}</span>
}

export function AlternativesPanel({ alternatives, selectedUf, onSelectUf }) {
  const altStates = useMemo(() => (
    Object.entries(alternatives ?? {})
      .map(([uf, alt]) => ({ uf, ...alt }))
      .sort((a, b) => a.name.localeCompare(b.name, 'pt'))
  ), [alternatives])

  if (altStates.length === 0) {
    return (
      <div className="card" style={{ padding: 16, textAlign: 'center', color: 'var(--text-muted)' }}>
        Nenhuma referência disponível.
      </div>
    )
  }

  const effectiveUf = selectedUf ?? altStates[0].uf
  const selectedAlt = altStates.find(s => s.uf === effectiveUf) || altStates[0]

  return (
    <>
      <div className="oc-state-chips" style={{ position: 'static', padding: '0 0 10px' }}>
        <span className="oc-state-chips-label">Estado:</span>
        {altStates.map(s => (
          <button
            key={s.uf}
            className={`oc-state-chip${s.uf === effectiveUf ? ' active' : ''}`}
            onClick={() => onSelectUf(s.uf)}
            title={`${s.name} · ${s.docLabel}`}
          >
            {s.abbr}
          </button>
        ))}
      </div>
      {selectedAlt.excerpts.length > 0
        ? selectedAlt.excerpts.map((ex, i) => (
            <div className="rg-article" key={i}>
              {ex.heading && <div className="rg-heading">{ex.heading}</div>}
              <p className="rg-caput">{renderFriendlyText(ex.caput)}</p>
              {ex.dispositivos?.length > 0 && <List items={ex.dispositivos} />}
              <div className="rg-article-foot">
                {ex.source ? <span className="rg-source">{ex.source}</span> : <span />}
                {ex.match && <MatchBadge match={ex.match} />}
              </div>
            </div>
          ))
        : <p className="rg-empty">Sem trechos para este estado.</p>}
    </>
  )
}
