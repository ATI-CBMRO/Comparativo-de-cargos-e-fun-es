import { useEffect, useMemo, useState } from 'react'
import { ListChecks, Check, AlertTriangle } from 'lucide-react'
import { useScenario } from '../context/ScenarioContext.jsx'
import { scenarioDbUrl } from '../lib/scenario.js'
import { fetchJson } from '../lib/dataCache.js'
import { LoadingState, ErrorState } from '../components/Status.jsx'
import { renderFriendlyText, List } from '../lib/comparatorRender.jsx'
import { buildConferencia } from '../lib/conferencia.js'
import { articleLabel, romanize } from '../lib/minutaArticles.js'

const ARQ = { ri: 'minuta_structure.json', reg: 'regulamento_structure.json' }
const TITULO = { ri: 'Regimento Interno', reg: 'Regulamento Geral' }

function MatchBadge({ match }) {
  const cfg = {
    exata: { cls: 'rg-badge-exata', label: 'exata' },
    parcial: { cls: 'rg-badge-parcial', label: 'parcial' },
    tematica: { cls: 'rg-badge-tematica', label: 'temática' },
    auto: { cls: 'rg-badge-tematica', label: 'auto' },
  }[match] ?? { cls: 'rg-badge-tematica', label: match || '—' }
  return <span className={`rg-badge ${cfg.cls}`}>{cfg.label}</span>
}

export default function ConferenciaLinear({ trilha = 'ri' }) {
  const { cenario } = useScenario()
  const [data, setData] = useState(null)
  const [error, setError] = useState(false)
  const [status, setStatus] = useState({}) // índice -> 'ok'|'div' (local, Fase 1 — não persiste)
  const [ufSel, setUfSel] = useState({}) // chapterId -> uf selecionada

  useEffect(() => {
    setData(null); setError(false)
    fetchJson(scenarioDbUrl(cenario, ARQ[trilha])).then(setData).catch(() => setError(true))
  }, [cenario, trilha])

  const lista = useMemo(() => (data ? buildConferencia(data) : []), [data])
  const feitos = useMemo(() => lista.filter((_, i) => status[i]).length, [status, lista])

  if (error) {
    return (
      <ErrorState
        icon={ListChecks}
        title="Estrutura não encontrada"
        hint={<>Execute o script que gera <code>database/{ARQ[trilha]}</code>.</>}
      />
    )
  }
  if (!data) return <LoadingState label="" />

  return (
    <div className="conf">
      <div className="section-bar no-print">
        <div className="section-bar-label">Conferência — {TITULO[trilha]}</div>
        <span className="section-bar-badge">
          <ListChecks size={13} color="var(--cbm-red-700)" />
          {feitos} / {lista.length} conferidos
        </span>
      </div>

      <div className="page-body">
        <div className="conf-progress">
          <div className="conf-progress-bar" style={{ width: `${lista.length ? (feitos / lista.length) * 100 : 0}%` }} />
        </div>

        {lista.length === 0 ? (
          <div className="card" style={{ padding: 24, textAlign: 'center', color: 'var(--text-muted)' }}>
            Nenhum dispositivo encontrado.
          </div>
        ) : (
          lista.map((item, i) => (
            <ConferenciaItem
              key={item.dispositivo.number ?? i}
              item={item}
              idx={i}
              status={status[i]}
              onStatus={(v) => setStatus(s => ({ ...s, [i]: v }))}
              ufSel={ufSel}
              setUfSel={setUfSel}
            />
          ))
        )}
      </div>
    </div>
  )
}

function ConferenciaItem({ item, idx, status, onStatus, ufSel, setUfSel }) {
  const { dispositivo, chapterTitle, chapterId, alternatives } = item
  const altStates = useMemo(() => (
    Object.entries(alternatives ?? {})
      .map(([uf, alt]) => ({ uf, ...alt }))
      .sort((a, b) => a.name.localeCompare(b.name, 'pt'))
  ), [alternatives])

  const selectedUf = ufSel[chapterId] ?? altStates[0]?.uf ?? null
  const selectedAlt = altStates.find(s => s.uf === selectedUf) || null

  return (
    <div className={`card conf-item${status === 'ok' ? ' conf-item-ok' : status === 'div' ? ' conf-item-div' : ''}`} style={{ marginBottom: 14, padding: 16 }}>
      {chapterTitle && <div className="rg-heading">{chapterTitle}</div>}
      <div className="rg-columns" style={{ display: 'flex', gap: 16, alignItems: 'flex-start' }}>
        <div className="rg-col" style={{ flex: 1, minWidth: 0 }}>
          <div className="rg-article">
            <p className="rg-caput">
              <strong>{articleLabel(dispositivo.number)}</strong> {renderFriendlyText(dispositivo.caput)}
            </p>
            {dispositivo.incisos?.length > 0 && (
              <ul className="cc-list rg-incisos">
                {dispositivo.incisos.map((inc, i) => (
                  <li key={i}>{inc.ownMarker ? '' : `${romanize(i + 1)} - `}{renderFriendlyText(inc.text)}</li>
                ))}
              </ul>
            )}
          </div>
          <div className="conf-controls no-print">
            <button
              type="button"
              className={`btn btn-ghost${status === 'ok' ? ' active' : ''}`}
              onClick={() => onStatus(status === 'ok' ? null : 'ok')}
            >
              <Check size={15} /> Confere
            </button>
            <button
              type="button"
              className={`btn btn-ghost${status === 'div' ? ' active' : ''}`}
              onClick={() => onStatus(status === 'div' ? null : 'div')}
            >
              <AlertTriangle size={15} /> Divergente
            </button>
          </div>
        </div>

        <div className="rg-col no-print" style={{ flex: 1, minWidth: 0 }}>
          {altStates.length === 0 ? (
            <div className="card" style={{ padding: 16, textAlign: 'center', color: 'var(--text-muted)' }}>
              Nenhuma referência disponível.
            </div>
          ) : (
            <>
              <div className="oc-state-chips" style={{ position: 'static', padding: '0 0 10px' }}>
                <span className="oc-state-chips-label">Estado:</span>
                {altStates.map(s => (
                  <button
                    key={s.uf}
                    className={`oc-state-chip${s.uf === selectedUf ? ' active' : ''}`}
                    onClick={() => setUfSel(u => ({ ...u, [chapterId]: s.uf }))}
                    title={`${s.name} · ${s.docLabel}`}
                  >
                    {s.abbr}
                  </button>
                ))}
              </div>
              {selectedAlt && selectedAlt.excerpts.length > 0
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
          )}
        </div>
      </div>
    </div>
  )
}
