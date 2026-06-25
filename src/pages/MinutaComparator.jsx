import { useEffect, useMemo, useState } from 'react'
import { GitCompare, Info, AlertCircle, FileDown, ScrollText, PanelLeftClose, PanelLeftOpen } from 'lucide-react'
import { MATRIX_ROWS } from '../lib/comparatorRender.jsx'

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

/* Pilha de órgãos de um estado dentro de uma célula (alguns estados têm 2+) */
function StateCell({ state, row }) {
  if (!state || (state.organs || []).length === 0) return <span className="cc-empty">—</span>
  return (
    <>
      {state.organs.map((o, i) => (
        <div key={i} style={i > 0 ? { marginTop: 8, paddingTop: 8, borderTop: '1px dashed var(--border-subtle)' } : undefined}>
          {row.render(o)}
        </div>
      ))}
      {row.key === 'organ' && state.note && (
        <div style={{ marginTop: 6, fontSize: 10.5, color: 'var(--text-muted)', fontStyle: 'italic' }}>{state.note}</div>
      )}
    </>
  )
}

/* Tabela pareada: Campo | CBMRO | estado selecionado */
function PairTable({ organ, state }) {
  const refOrgans = organ.reference ? [organ.reference] : []
  return (
    <div className="oc-pair-wrapper" style={{ border: '1px solid var(--border-card)', borderRadius: 'var(--radius-lg)', overflow: 'hidden' }}>
      <table className="oc-pair-table">
        <colgroup>
          <col className="oc-pair-col-label" />
          <col className="oc-pair-col-ro" />
          <col className="oc-pair-col-st" />
        </colgroup>
        <thead>
          <tr>
            <th className="oc-pair-th-label">Campo</th>
            <th className="oc-pair-th-ro">
              <div className="cc-corp-head">
                <span className="cc-corp-abbr ref">RO</span>
                <div>
                  <div className="cc-corp-name">Rondônia</div>
                  <div className="cc-corp-cbm">CBMRO · Referência</div>
                </div>
              </div>
            </th>
            <th className="oc-pair-th-st">
              {state ? (
                <div className="cc-corp-head">
                  <span className="cc-corp-abbr">{state.abbr}</span>
                  <div>
                    <div className="cc-corp-name">{state.name}</div>
                    <div className="cc-corp-cbm" style={{ display: 'flex', alignItems: 'center', gap: 6, flexWrap: 'wrap' }}>
                      {state.cbm}
                      <ProvBadge provenance={state.provenance} />
                      {state.sourceLabel && <span style={{ fontWeight: 600 }}>{state.sourceLabel}</span>}
                    </div>
                  </div>
                </div>
              ) : <span className="cc-empty">Selecione um estado</span>}
            </th>
          </tr>
        </thead>
        <tbody>
          {MATRIX_ROWS.map((row, rowIdx) => (
            <tr key={row.key}>
              <td className="oc-pair-td-label">{row.label}</td>
              {refOrgans.length === 0
                ? (rowIdx === 0
                    ? <td className="oc-pair-td-ro" rowSpan={MATRIX_ROWS.length} style={{ verticalAlign: 'top' }}>
                        <span style={{ display: 'flex', gap: 5, alignItems: 'flex-start', fontStyle: 'italic', color: 'var(--text-muted)' }}>
                          <AlertCircle size={13} style={{ flexShrink: 0, marginTop: 2 }} />
                          {organ.referenceNote || 'O CBMRO não discrimina este órgão.'}
                        </span>
                      </td>
                    : null)
                : <td className="oc-pair-td-ro">{row.render(refOrgans[0])}</td>
              }
              <td className="oc-pair-td-st"><StateCell state={state} row={row} /></td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  )
}

/* Reconstrói a árvore (DPO › COT › CAT …) a partir da lista plana de órgãos com `depth`. */
function buildOrganTree(organs) {
  const roots = []
  const stack = [] // [{ node, depth }]
  for (const o of organs) {
    const node = { ...o, children: [] }
    while (stack.length && stack[stack.length - 1].depth >= (o.depth || 0)) stack.pop()
    if (stack.length) stack[stack.length - 1].node.children.push(node)
    else roots.push(node)
    stack.push({ node, depth: o.depth || 0 })
  }
  return roots
}

/* Nó da árvore de órgãos: botão −/+ recolhe a subárvore; clicar no item seleciona o órgão.
   Inicia recolhido (só o 1º nível visível), espelhando o organograma da minuta. */
function OrgTreeNode({ node, depth, organKey, setOrganKey }) {
  const hasChildren = node.children.length > 0
  const [open, setOpen] = useState(false)
  return (
    <>
      <div className="oc-org-row" style={{ paddingLeft: depth * 14 }}>
        {hasChildren ? (
          <button
            type="button"
            className="oc-org-toggle"
            onClick={() => setOpen(v => !v)}
            aria-expanded={open}
            aria-label={`${open ? 'Recolher' : 'Expandir'} ${node.abbr}`}
            title={open ? 'Recolher' : `Expandir (${node.children.length})`}
          >
            {open ? '−' : '+'}
          </button>
        ) : (
          <span className="oc-org-leaf" aria-hidden="true">└</span>
        )}
        <button
          type="button"
          onClick={() => setOrganKey(node.key)}
          className={`nav-item oc-org-select${node.key === organKey ? ' active' : ''}`}
          title={node.title}
        >
          {node.abbr}<span className="oc-org-count">{node.states.length}</span>
        </button>
      </div>
      {hasChildren && open && node.children.map(c => (
        <OrgTreeNode key={c.key} node={c} depth={depth + 1} organKey={organKey} setOrganKey={setOrganKey} />
      ))}
    </>
  )
}

export default function MinutaComparator() {
  const [data, setData] = useState(null)
  const [error, setError] = useState(false)
  const [organKey, setOrganKey] = useState(null)
  const [selectedStateId, setSelectedStateId] = useState(null)
  const [navOpen, setNavOpen] = useState(true)

  useEffect(() => {
    fetch('/database/comparativo_minuta.json')
      .then(r => (r.ok ? r.json() : Promise.reject()))
      .then(d => { setData(d); setOrganKey(d.organs[0]?.key || null) })
      .catch(() => setError(true))
  }, [])

  const organ = useMemo(() => data?.organs.find(o => o.key === organKey) || null, [data, organKey])
  const organTree = useMemo(() => (data ? buildOrganTree(data.organs) : []), [data])

  // Chips em ordem alfabética
  const chips = useMemo(() => {
    if (!organ) return []
    return [...organ.states].sort((a, b) => a.abbr.localeCompare(b.abbr, 'pt'))
  }, [organ])

  // Ao trocar de órgão, garante um estado válido selecionado (primeiro do órgão)
  useEffect(() => {
    if (!organ) return
    const ids = organ.states.map(s => s.id)
    if (!selectedStateId || !ids.includes(selectedStateId)) {
      const first = [...organ.states].sort((a, b) => a.abbr.localeCompare(b.abbr, 'pt'))[0]
      setSelectedStateId(first ? first.id : null)
    }
  }, [organ]) // eslint-disable-line react-hooks/exhaustive-deps

  const selectedState = useMemo(
    () => organ?.states.find(s => s.id === selectedStateId) || null,
    [organ, selectedStateId]
  )

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
            Compare a legislação do <strong>CBMRO</strong> com a de <strong>um estado por vez</strong>, órgão a
            órgão, na mesma ordem da minuta do Regimento Interno — do topo (DPO/COT) à menor fração (Guarnição
            de Serviço). Escolha o órgão à esquerda e clique na <strong>sigla de um estado</strong> para trocar a
            legislação comparada. Colunas marcadas <strong>Curado</strong> trazem texto verbatim atribuído à
            fonte; <strong>Auto</strong> vêm de extração automática e podem ser rasas.
          </p>
        </div>

        <div className="oc-compare-layout" style={{ display: 'flex', gap: 16, alignItems: 'flex-start' }}>
          {/* Sumário de órgãos (colapsável) */}
          <aside className="no-print oc-compare-aside" style={{ flex: navOpen ? '0 0 220px' : '0 0 52px', position: 'sticky', top: 'calc(var(--header-h) + 12px)', maxHeight: 'calc(100vh - var(--header-h) - 24px)', overflowY: 'auto', transition: 'flex-basis 0.15s ease' }}>
            <div className="card" style={{ padding: navOpen ? 8 : 6 }}>
              <div style={{ display: 'flex', alignItems: 'center', justifyContent: navOpen ? 'space-between' : 'center', gap: 6, padding: navOpen ? '2px 4px 6px' : '2px 0 6px' }}>
                {navOpen && <span className="nav-section-label" style={{ padding: '4px 6px' }}>Órgãos da minuta</span>}
                <button
                  onClick={() => setNavOpen(v => !v)}
                  className="btn btn-ghost"
                  title={navOpen ? 'Recolher lista de órgãos' : 'Expandir lista de órgãos'}
                  style={{ padding: 5, height: 28, minWidth: 28 }}
                >
                  {navOpen ? <PanelLeftClose size={15} /> : <PanelLeftOpen size={15} />}
                </button>
              </div>
              {navOpen
                ? organTree.map(root => (
                    <OrgTreeNode key={root.key} node={root} depth={0} organKey={organKey} setOrganKey={setOrganKey} />
                  ))
                : data.organs.map(o => (
                    <button
                      key={o.key}
                      onClick={() => setOrganKey(o.key)}
                      className={`nav-item${o.key === organKey ? ' active' : ''}`}
                      style={{
                        width: '100%', border: 'none', cursor: 'pointer', fontSize: 12.5,
                        textAlign: 'center', justifyContent: 'center', padding: '8px 2px',
                      }}
                      title={`${o.title} — ${o.states.length} estado(s)`}
                    >
                      {o.abbr}
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

                <div className="oc-toolbar no-print" style={{ marginBottom: 12, justifyContent: 'flex-end' }}>
                  <button className="btn btn-ghost" onClick={() => window.print()}>
                    <FileDown size={15} /> Exportar PDF
                  </button>
                </div>

                {organ.states.length > 0 && (
                  <div className="oc-state-chips no-print">
                    <span className="oc-state-chips-label">Estado:</span>
                    {chips.map(s => (
                      <button
                        key={s.id}
                        className={`oc-state-chip${s.id === selectedStateId ? ' active' : ''}`}
                        onClick={() => setSelectedStateId(s.id)}
                        title={`${s.name} · ${s.cbm}${s.provenance === 'curado' ? ' · curado' : ' · automático'}`}
                      >
                        {s.abbr}
                      </button>
                    ))}
                  </div>
                )}

                <div className="print-only-title" style={{ display: 'none' }}>
                  {organ.title}{selectedState ? ` — CBMRO × ${selectedState.abbr} (${selectedState.cbm})` : ''}
                </div>

                {organ.states.length === 0 && organ.reference == null
                  ? <div className="card" style={{ padding: 30, textAlign: 'center', color: 'var(--text-muted)' }}>Nenhum estado com dado para este órgão.</div>
                  : <PairTable organ={organ} state={selectedState} />}
              </>
            )}
          </div>
        </div>
      </div>
    </>
  )
}
