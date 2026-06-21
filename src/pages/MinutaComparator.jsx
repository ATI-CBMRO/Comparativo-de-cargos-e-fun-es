import { useEffect, useMemo, useState } from 'react'
import { GitCompare, Info, AlertCircle, Search, FileDown, ScrollText } from 'lucide-react'
import { MATRIX_ROWS } from '../lib/comparatorRender.jsx'

function norm(s) {
  return (s || '').normalize('NFKD').replace(/[̀-ͯ]/g, '').toLowerCase()
}

function ProvBadge({ provenance }) {
  const curado = provenance === 'curado'
  return (
    <span style={{
      fontSize: 9, fontWeight: 800, padding: '1px 6px', borderRadius: 99,
      textTransform: 'uppercase', letterSpacing: '0.04em',
      background: curado ? 'rgba(22,163,74,0.12)' : 'rgba(245,166,35,0.16)',
      color: curado ? 'var(--accent-green)' : 'var(--accent-orange)',
    }}>{curado ? 'Curado' : 'Auto'}</span>
  )
}

function Matrix({ organ, states }) {
  const refOrgans = organ.reference ? [organ.reference] : []
  return (
    <div className="cargo-compare-wrapper oc-scroll">
      <table className="cargo-compare-table oc-matrix-table">
        <colgroup>
          <col style={{ width: 150 }} />
          {refOrgans.length === 0 ? <col style={{ minWidth: 240 }} /> : refOrgans.map((_, i) => <col key={i} style={{ minWidth: 240 }} />)}
          {states.map(s => <col key={s.id} style={{ minWidth: 210 }} />)}
        </colgroup>
        <thead>
          <tr>
            <th className="cc-col-label cc-corner">Campo</th>
            <th className="cc-col-ro cc-corner" colSpan={Math.max(refOrgans.length, 1)}>
              <div className="cc-corp-head">
                <span className="cc-corp-abbr ref">RO</span>
                <div>
                  <div className="cc-corp-name">Rondônia</div>
                  <div className="cc-corp-cbm">CBMRO · Referência</div>
                </div>
              </div>
            </th>
            {states.map(s => (
              <th key={s.id}>
                <div className="cc-corp-head" style={{ flexDirection: 'column', alignItems: 'flex-start', gap: 4 }}>
                  <div style={{ display: 'flex', alignItems: 'center', gap: 8 }}>
                    <span className="cc-corp-abbr">{s.abbr}</span>
                    <div>
                      <div className="cc-corp-name">{s.name}</div>
                      <div className="cc-corp-cbm">{s.cbm}</div>
                    </div>
                  </div>
                  <div style={{ display: 'flex', alignItems: 'center', gap: 6 }}>
                    <ProvBadge provenance={s.provenance} />
                    {s.sourceLabel && <span style={{ fontSize: 9.5, color: 'var(--text-muted)' }}>{s.sourceLabel}</span>}
                  </div>
                </div>
              </th>
            ))}
          </tr>
        </thead>
        <tbody>
          {MATRIX_ROWS.map((row, rowIdx) => (
            <tr key={row.key}>
              <td className="cc-col-label">{row.label}</td>
              {refOrgans.length === 0
                ? (rowIdx === 0
                    ? <td className="cc-col-ro cc-ref-cell" rowSpan={MATRIX_ROWS.length} style={{ verticalAlign: 'top' }}>
                        <span style={{ display: 'flex', gap: 5, alignItems: 'flex-start', fontSize: 11.5, fontStyle: 'italic', color: 'var(--text-muted)' }}>
                          <AlertCircle size={13} style={{ flexShrink: 0, marginTop: 2 }} />
                          {organ.referenceNote || 'O CBMRO não discrimina este órgão.'}
                        </span>
                      </td>
                    : null)
                : refOrgans.map((o, i) => <td key={i} className="cc-col-ro cc-ref-cell">{row.render(o)}</td>)
              }
              {states.map(s => (
                <td key={s.id}>
                  {(s.organs || []).length === 0
                    ? <span className="cc-empty">—</span>
                    : s.organs.map((o, i) => <div key={i} style={i > 0 ? { marginTop: 8, paddingTop: 8, borderTop: '1px dashed var(--border-subtle)' } : undefined}>{row.render(o)}</div>)}
                  {row.key === 'organ' && s.note && (
                    <div style={{ marginTop: 6, fontSize: 10.5, color: 'var(--text-muted)', fontStyle: 'italic' }}>{s.note}</div>
                  )}
                </td>
              ))}
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  )
}

export default function MinutaComparator() {
  const [data, setData] = useState(null)
  const [error, setError] = useState(false)
  const [organKey, setOrganKey] = useState(null)
  const [search, setSearch] = useState('')

  useEffect(() => {
    fetch('/database/comparativo_minuta.json')
      .then(r => (r.ok ? r.json() : Promise.reject()))
      .then(d => { setData(d); setOrganKey(d.organs[0]?.key || null) })
      .catch(() => setError(true))
  }, [])

  const organ = useMemo(() => data?.organs.find(o => o.key === organKey) || null, [data, organKey])

  const visibleStates = useMemo(() => {
    if (!organ) return []
    if (!search.trim()) return organ.states
    const q = norm(search)
    return organ.states.filter(s => norm(s.name).includes(q) || norm(s.abbr).includes(q) || norm(s.cbm).includes(q))
  }, [organ, search])

  if (error) {
    return (
      <div className="empty-state" style={{ marginTop: 24 }}>
        <GitCompare size={40} className="empty-state-icon" />
        <h3>Comparativo não encontrado</h3>
        <p>Execute <code>python scripts/build_minuta_comparison.py</code> para gerar os dados.</p>
      </div>
    )
  }
  if (!data) return <div className="empty-state"><div className="spinner" /></div>

  return (
    <>
      <div className="section-bar no-print">
        <div className="section-bar-label">Subsídio à Minuta — CBMRO × demais estados, pela estrutura do Regimento</div>
        <span className="section-bar-badge"><ScrollText size={13} color="var(--cbm-red-700)" />{data.organs.length} órgãos</span>
      </div>

      <div className="page-body">
        <div className="card no-print" style={{ marginBottom: 16 }}>
          <p style={{ fontSize: 13, color: 'var(--text-secondary)', lineHeight: 1.6, margin: 0 }}>
            Compare a legislação do <strong>CBMRO</strong> com a dos demais estados, órgão a órgão, na mesma
            ordem da minuta do Regimento Interno — do topo (DPO/COT) à menor fração (Guarnição de Serviço).
            Colunas marcadas <strong>Curado</strong> trazem texto verbatim atribuído à fonte; <strong>Auto</strong>
            vêm de extração automática e podem ser rasas. Só aparecem estados com dado para o órgão.
          </p>
        </div>

        <div style={{ display: 'flex', gap: 16, alignItems: 'flex-start' }}>
          {/* Sumário de órgãos */}
          <aside className="no-print" style={{ flex: '0 0 230px', position: 'sticky', top: 12 }}>
            <div className="card" style={{ padding: 8 }}>
              <div className="nav-section-label" style={{ padding: '6px 8px' }}>Órgãos da minuta</div>
              {data.organs.map(o => (
                <button
                  key={o.key}
                  onClick={() => setOrganKey(o.key)}
                  className={`nav-item${o.key === organKey ? ' active' : ''}`}
                  style={{ width: '100%', textAlign: 'left', border: 'none', cursor: 'pointer', fontSize: 12.5 }}
                  title={o.title}
                >
                  {o.abbr} <span style={{ opacity: 0.6, fontSize: 10, marginLeft: 4 }}>{o.states.length}</span>
                </button>
              ))}
            </div>
          </aside>

          {/* Conteúdo do órgão */}
          <div style={{ flex: 1, minWidth: 0 }}>
            {organ && (
              <>
                <div className="oc-group-desc no-print" style={{ marginBottom: 12 }}>
                  <Info size={14} style={{ flexShrink: 0, marginTop: 2 }} color="var(--accent-blue)" />
                  <span><strong>{organ.title}</strong></span>
                </div>

                <div className="oc-toolbar no-print" style={{ marginBottom: 12 }}>
                  <div className="search-input-wrap" style={{ maxWidth: 280 }}>
                    <Search size={14} className="search-input-icon" />
                    <input
                      type="text" className="search-input" placeholder="Buscar estado / CBM..."
                      value={search} onChange={e => setSearch(e.target.value)}
                      style={{ height: 36, paddingLeft: 34, fontSize: 13 }}
                    />
                  </div>
                  <button className="btn btn-ghost" onClick={() => window.print()}>
                    <FileDown size={15} /> Exportar PDF
                  </button>
                </div>

                <div className="print-only-title" style={{ display: 'none' }}>{organ.title}</div>

                {visibleStates.length === 0 && organ.reference == null
                  ? <div className="card" style={{ padding: 30, textAlign: 'center', color: 'var(--text-muted)' }}>Nenhum estado com dado para este órgão.</div>
                  : <Matrix organ={organ} states={visibleStates} />}
              </>
            )}
          </div>
        </div>
      </div>
    </>
  )
}
