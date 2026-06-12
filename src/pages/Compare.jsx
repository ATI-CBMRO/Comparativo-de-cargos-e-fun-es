import { useEffect, useState } from 'react'
import { GitCompare, ChevronDown, X, Layers, AlertCircle, FileDown } from 'lucide-react'
import Organogram from '../components/Organogram.jsx'

function StateSelector({ states, selected, onChange, placeholder }) {
  return (
    <div style={{ position: 'relative' }}>
      <select
        style={{
          width: '100%',
          background: 'var(--bg-input)',
          border: '1px solid var(--border-card)',
          borderRadius: 'var(--radius-md)',
          color: selected ? 'var(--text-primary)' : 'var(--cbm-gray-400)',
          fontSize: 14,
          padding: '10px 36px 10px 12px',
          outline: 'none',
          cursor: 'pointer',
          appearance: 'none',
          fontFamily: 'inherit',
        }}
        value={selected?.id || ''}
        onChange={e => {
          const found = states.find(s => s.id === e.target.value)
          onChange(found || null)
        }}
      >
        <option value="">{placeholder}</option>
        {states.map(s => (
          <option key={s.id} value={s.id}>
            {s.abbreviation} — {s.name} ({s.cbm_abbreviation})
          </option>
        ))}
      </select>
      <ChevronDown size={16} style={{ position: 'absolute', right: 12, top: '50%', transform: 'translateY(-50%)', color: 'var(--cbm-gray-400)', pointerEvents: 'none' }} />
    </div>
  )
}

function CompareDocCard({ doc, idxColor }) {
  const [hovered, setHovered] = useState(false)
  const pdfUrl = doc.md_file ? `/legislacao-pdf/${encodeURIComponent(doc.md_file.replace('.md', '.pdf'))}` : null

  return (
    <div
      style={{
        padding: '8px 10px',
        background: hovered ? 'var(--bg-card-hover)' : 'var(--bg-surface)',
        borderRadius: 'var(--radius-md)',
        border: hovered ? `1px solid ${idxColor.text}` : '1px solid var(--border-subtle)',
        cursor: pdfUrl ? 'pointer' : 'default',
        transition: 'all 0.15s ease',
        transform: hovered ? 'translateY(-1px)' : 'none',
        boxShadow: hovered ? 'var(--shadow-card)' : 'none',
      }}
      onMouseEnter={() => setHovered(true)}
      onMouseLeave={() => setHovered(false)}
      onClick={() => {
        if (pdfUrl) {
          window.open(pdfUrl, '_blank')
        }
      }}
      title={pdfUrl ? "Clique para abrir o arquivo PDF oficial da legislação" : ""}
    >
      <div style={{ fontSize: 11, fontWeight: 700, color: idxColor.text, marginBottom: 3, display: 'flex', alignItems: 'center', gap: 4 }}>
        {doc.type === 'Lei de Organização Básica' ? 'LOB' : doc.type}
        {pdfUrl && <span style={{ fontSize: 8, color: 'var(--text-muted)' }}>↗</span>}
      </div>
      {doc.laws?.map((l, j) => (
        <div key={j} style={{ fontSize: 11, color: 'var(--text-secondary)', lineHeight: 1.4 }}>
          {l.tipo} nº {l.numero} · {l.data}
        </div>
      ))}
      {doc.year && <div style={{ fontSize: 10, color: 'var(--text-muted)', marginTop: 2 }}>Ano: {doc.year}</div>}
    </div>
  )
}

function ComparePanel({ state, idx }) {
  const [activeTab, setActiveTab] = useState('organograma')

  const colors = [
    { border: 'var(--cbm-red-800)', accent: 'var(--cbm-red-700)', text: 'var(--cbm-red-400)' },
    { border: 'var(--cbm-gold-500)', accent: 'var(--cbm-gold-500)', text: 'var(--cbm-gold-400)' },
    { border: 'var(--navy-700)', accent: 'var(--navy-600)', text: 'var(--navy-500)' },
    { border: 'var(--cbm-red-900)', accent: 'var(--cbm-red-800)', text: 'var(--cbm-red-500)' },
    { border: 'var(--gray-600)', accent: 'var(--gray-500)', text: 'var(--gray-400)' },
  ]
  const idxColor = colors[idx % colors.length]

  if (!state) return (
    <div style={{
      background: 'var(--bg-card)',
      border: `1px dashed var(--border-card)`,
      borderRadius: 'var(--radius-lg)',
      display: 'flex',
      alignItems: 'center',
      justifyContent: 'center',
      minHeight: 400,
      flexDirection: 'column',
      gap: 12,
      padding: 24
    }}>
      <Layers size={32} style={{ opacity: 0.3 }} />
      <p style={{ color: 'var(--text-muted)', fontSize: 14 }}>Selecione um estado acima</p>
    </div>
  )

  return (
    <div className="compare-panel" style={{
      background: 'var(--bg-card)',
      border: `1px solid ${idxColor.border}`,
      borderRadius: 'var(--radius-lg)',
      overflow: 'hidden',
      display: 'flex',
      flexDirection: 'column',
      height: '100%'
    }}>
      {/* Header do painel */}
      <div style={{
        background: 'var(--bg-surface)',
        borderBottom: `3px solid ${idxColor.border}`,
        padding: '14px 18px',
        display: 'flex',
        alignItems: 'center',
        gap: 12
      }}>
        <div style={{
          width: 38, height: 38,
          background: idxColor.border,
          borderRadius: 'var(--radius-md)',
          display: 'flex', alignItems: 'center', justifyContent: 'center',
          fontFamily: 'Outfit', fontWeight: 900, fontSize: 14, color: '#fff',
          flexShrink: 0
        }}>
          {state.abbreviation}
        </div>
        <div style={{ minWidth: 0 }}>
          <div style={{ fontFamily: 'Outfit', fontSize: 15, fontWeight: 700, color: 'var(--text-primary)', whiteSpace: 'nowrap', overflow: 'hidden', textOverflow: 'ellipsis' }}>{state.name}</div>
          <div style={{ fontSize: 11, color: idxColor.text, fontWeight: 700 }}>{state.cbm_abbreviation}</div>
        </div>
      </div>

      {/* Tabs */}
      <div className="no-print" style={{ display: 'flex', gap: 2, padding: '10px 12px 0', borderBottom: '1px solid var(--border-subtle)', background: 'var(--bg-card)' }}>
        {['organograma', 'documentos', 'base-legal'].map(tab => (
          <button
            key={tab}
            onClick={() => setActiveTab(tab)}
            style={{
              padding: '6px 10px',
              borderRadius: 'var(--radius-md) var(--radius-md) 0 0',
              fontSize: 11,
              fontWeight: 600,
              cursor: 'pointer',
              border: 'none',
              background: activeTab === tab ? 'var(--bg-surface)' : 'transparent',
              color: activeTab === tab ? idxColor.text : 'var(--text-muted)',
              borderBottom: activeTab === tab ? `2px solid ${idxColor.text}` : '2px solid transparent',
              transition: 'all 0.15s',
              textTransform: 'capitalize'
            }}
          >
            {tab === 'base-legal' ? 'Base Legal' : tab.charAt(0).toUpperCase() + tab.slice(1)}
          </button>
        ))}
      </div>

      <div style={{ padding: 14, flex: 1, overflowY: 'auto' }}>
        {(activeTab === 'organograma' || window.matchMedia('print').matches) && (
          <div>
            {!state.stats?.curated && (
              <div className="no-print" style={{ display: 'flex', gap: 8, marginBottom: 12, padding: '8px 12px', background: 'rgba(245,124,0,0.06)', borderRadius: 'var(--radius-md)', border: '1px solid rgba(245,124,0,0.15)' }}>
                <AlertCircle size={14} color="var(--cbm-gold-500)" style={{ flexShrink: 0, marginTop: 1 }} />
                <span style={{ fontSize: 11, color: 'var(--cbm-gold-500)' }}>Extração automática — contém revisões simplificadas</span>
              </div>
            )}
            <Organogram data={state.organs} />
          </div>
        )}

        {(activeTab === 'documentos' && !window.matchMedia('print').matches) && (
          <div style={{ display: 'flex', flexDirection: 'column', gap: 8 }}>
            {state.documents?.map((doc, i) => (
              <CompareDocCard key={i} doc={doc} idxColor={idxColor} />
            ))}
          </div>
        )}

        {(activeTab === 'base-legal' && !window.matchMedia('print').matches) && (
          <div>
            <div style={{ fontSize: 12, color: 'var(--text-secondary)', lineHeight: 1.6, marginBottom: 12 }}>
              <span style={{ fontWeight: 700, color: 'var(--text-primary)' }}>Fundamentação:</span>{' '}
              {state.legal_basis || 'Não identificada automaticamente.'}
            </div>
            {state.stats?.has_regimento && (
              <div style={{ padding: '8px 10px', background: 'rgba(255,179,0,0.05)', borderRadius: 'var(--radius-md)', border: '1px solid rgba(255,179,0,0.12)', fontSize: 11, color: 'var(--cbm-gold-300)', marginBottom: 8 }}>
                Este estado possui LOB + Regimento Interno unificados.
              </div>
            )}
            {state.stats?.has_nga && (
              <div style={{ padding: '8px 10px', background: 'rgba(255,179,0,0.05)', borderRadius: 'var(--radius-md)', border: '1px solid rgba(255,179,0,0.12)', fontSize: 11, color: 'var(--cbm-gold-300)' }}>
                As Normas Gerais de Ação (NGA) foram unificadas.
              </div>
            )}
          </div>
        )}
      </div>
    </div>
  )
}

export default function Compare() {
  const [data, setData] = useState(null)
  const [selectedStates, setSelectedStates] = useState([])

  useEffect(() => {
    fetch('/database/states_data.json')
      .then(r => r.json())
      .then(res => {
        setData(res)
        if (res.states && res.states.length > 0) {
          // Inicializa com Rondônia (RO) e Distrito Federal (DF) por padrão
          const ro = res.states.find(s => s.id === 'ro')
          const df = res.states.find(s => s.id === 'df')
          const initial = []
          if (ro) initial.push(ro)
          if (df) initial.push(df)
          if (initial.length < 2 && res.states[0]) initial.push(res.states[0])
          if (initial.length < 2 && res.states[1]) initial.push(res.states[1])
          setSelectedStates(initial)
        }
      })
  }, [])

  if (!data) return (
    <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'center', height: '60vh' }}>
      <div className="spinner" />
    </div>
  )

  const handleStateChange = (idx, newState) => {
    const updated = [...selectedStates]
    if (newState) {
      updated[idx] = newState
    } else {
      updated.splice(idx, 1)
    }
    setSelectedStates(updated)
  }

  const handleRemoveState = (idx) => {
    const updated = [...selectedStates]
    updated.splice(idx, 1)
    setSelectedStates(updated)
  }

  const printDate = new Date().toLocaleDateString('pt-BR', { day: '2-digit', month: 'long', year: 'numeric' })

  return (
    <>
      {/* Cabeçalho exclusivo da impressão / PDF */}
      <div className="print-header print-only">
        <img
          className="print-header-emblem"
          src="/BrasaoCBMRO2D-COMPLETO.png"
          onError={e => { if (!e.currentTarget.dataset.fb) { e.currentTarget.dataset.fb = '1'; e.currentTarget.src = '/brasao-cbmro.svg' } }}
          alt="Brasão CBMRO"
        />
        <div className="print-header-text">
          <div className="print-header-title">Comparativo de Estruturas Organizacionais</div>
          <div className="print-header-subtitle">Corpos de Bombeiros Militares — Portal de Legislação · CBMRO</div>
          {selectedStates.length > 0 && (
            <div className="print-header-states">
              {selectedStates.map(s => `${s.name} (${s.cbm_abbreviation})`).join('   ·   ')}
            </div>
          )}
        </div>
        <div className="print-header-meta">
          <span>Emitido em</span>
          <strong>{printDate}</strong>
        </div>
      </div>

      <div className="page-header">
        <div className="page-header-left">
          <h1 className="page-title">Comparador de Legislações</h1>
          <p className="page-subtitle">Compare de forma fiel a estrutura e competências de até 5 corporações simultaneamente</p>
        </div>
        <div style={{ display: 'flex', gap: 10 }} className="no-print">
          <button
            className="btn btn-primary"
            onClick={() => window.print()}
            disabled={selectedStates.length === 0}
            style={{ display: 'flex', alignItems: 'center', gap: 8 }}
          >
            <FileDown size={16} />
            Exportar Comparativo (PDF)
          </button>
        </div>
      </div>

      <div className="page-body">
        {/* Seletores */}
        <div style={{
          display: 'grid',
          gridTemplateColumns: `repeat(auto-fit, minmax(200px, 1fr))`,
          gap: 16,
          marginBottom: 24,
          alignItems: 'end'
        }} className="no-print">
          {selectedStates.map((state, idx) => (
            <div key={idx} style={{ position: 'relative' }}>
              <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 6 }}>
                <span style={{ fontSize: 11, fontWeight: 700, color: idx % 2 === 0 ? 'var(--cbm-red-400)' : 'var(--cbm-gold-400)', textTransform: 'uppercase', letterSpacing: '0.8px' }}>
                  Corporação {idx + 1}
                </span>
                {selectedStates.length > 1 && (
                  <button
                    onClick={() => handleRemoveState(idx)}
                    style={{ color: 'var(--text-muted)', cursor: 'pointer', display: 'flex', alignItems: 'center', padding: '2px' }}
                    title="Remover corporação"
                  >
                    <X size={14} />
                  </button>
                )}
              </div>
              <StateSelector
                states={data.states.filter(s => !selectedStates.some((sel, sIdx) => sel && sel.id === s.id && sIdx !== idx))}
                selected={state}
                onChange={newState => handleStateChange(idx, newState)}
                placeholder="Selecione um estado..."
              />
            </div>
          ))}

          {selectedStates.length < 5 && (
            <div>
              <div style={{ fontSize: 11, fontWeight: 700, color: 'var(--text-muted)', marginBottom: 6, textTransform: 'uppercase', letterSpacing: '0.8px' }}>
                Adicionar Corporação
              </div>
              <StateSelector
                states={data.states.filter(s => !selectedStates.some(sel => sel && sel.id === s.id))}
                selected={null}
                onChange={newState => {
                  if (newState) {
                    setSelectedStates([...selectedStates, newState])
                  }
                }}
                placeholder="+ Adicionar corporação..."
              />
            </div>
          )}
        </div>

        {/* Sugestões rápidas de comparação */}
        {selectedStates.length <= 1 && (
          <div className="card no-print" style={{ marginBottom: 24 }}>
            <div style={{ fontSize: 12, color: 'var(--text-muted)', marginBottom: 8 }}>Sugestões rápidas de comparação:</div>
            <div style={{ display: 'flex', gap: 8, flexWrap: 'wrap' }}>
              {[
                { label: 'Rondônia vs Acre', ids: ['ro', 'ac'] },
                { label: 'Rondônia vs Distrito Federal', ids: ['ro', 'df'] },
                { label: 'Região Norte (RO, AC, AM, AP)', ids: ['ro', 'ac', 'am', 'ap'] },
                { label: 'LOB + Regimento (DF, RS, ES)', ids: ['df', 'rs', 'es'] }
              ].map((sug, i) => (
                <button
                  key={i}
                  className="btn btn-ghost btn-sm"
                  onClick={() => {
                    const statesList = sug.ids
                      .map(id => data.states.find(s => s.id === id))
                      .filter(Boolean)
                    setSelectedStates(statesList)
                  }}
                >
                  {sug.label}
                </button>
              ))}
            </div>
          </div>
        )}

        {/* Comparação lado a lado */}
        {selectedStates.length > 0 ? (
          <div
            className="compare-grid-scroll"
            style={{
              display: 'grid',
              gridTemplateColumns: `repeat(${selectedStates.length}, minmax(280px, 1fr))`,
              gap: 20,
              overflowX: 'auto',
              paddingBottom: 16,
              alignItems: 'stretch'
            }}
          >
            {selectedStates.map((state, idx) => (
              <ComparePanel key={state ? state.id : `empty-${idx}`} state={state} idx={idx} />
            ))}
          </div>
        ) : (
          <div className="empty-state">
            <Layers size={40} className="empty-state-icon" />
            <h3>Nenhuma corporação selecionada</h3>
            <p>Selecione pelo menos um Corpo de Bombeiros Militar para analisar.</p>
          </div>
        )}

        {/* Tabela de Comparação Rápida */}
        {selectedStates.length > 1 && (
          <div className="card compare-stats" style={{ marginTop: 24, overflow: 'hidden' }}>
            <div className="card-header">
              <span className="card-title" style={{ display: 'flex', alignItems: 'center', gap: 8 }}>
                <GitCompare size={18} color="var(--cbm-red-700)" />
                Análise Comparativa Rápida (Estatísticas da Legislação)
              </span>
            </div>
            <div style={{ overflowX: 'auto' }}>
              <table style={{ width: '100%', borderCollapse: 'collapse', fontSize: 13, minWidth: 600 }}>
                <thead>
                  <tr style={{ borderBottom: '2px solid var(--border-card)', background: 'var(--bg-surface)' }}>
                    <th style={{ textAlign: 'left', padding: '12px 16px', color: 'var(--text-primary)', fontWeight: 700 }}>Métrica / Parâmetro</th>
                    {selectedStates.map((s, idx) => {
                      const colors = ['var(--cbm-red-700)', 'var(--cbm-gold-500)', 'var(--navy-600)', 'var(--cbm-red-900)', 'var(--gray-500)']
                      const color = colors[idx % colors.length]
                      return (
                        <th key={s.id} style={{ textAlign: 'center', padding: '12px 16px', color: color, fontWeight: 800 }}>
                          {s.abbreviation}
                        </th>
                      )
                    })}
                  </tr>
                </thead>
                <tbody>
                  {[
                    { label: 'Qtd. de Documentos no Acervo', getValue: s => `${s.stats?.total_documents || 0} doc(s)` },
                    { label: 'Volume Textual (Qtd. de Caracteres)', getValue: s => `${((s.stats?.total_chars || 0) / 1000).toFixed(0)}k caracteres` },
                    { label: 'Total de Órgãos Catalogados', getValue: s => `${s.stats?.organs_mapped || 0} órgãos` },
                    { label: 'Possui Regimento Interno unificado?', getValue: s => s.stats?.has_regimento ? '🟢 Sim' : '❌ Não' },
                    { label: 'Possui Normas Gerais (NGA) unificadas?', getValue: s => s.stats?.has_nga ? '🟢 Sim' : '❌ Não' },
                    { label: 'Região do País', getValue: s => s.region },
                  ].map((row, idx) => (
                    <tr key={idx} style={{ borderBottom: '1px solid var(--border-subtle)', background: idx % 2 === 0 ? 'rgba(0,0,0,0.01)' : 'transparent' }}>
                      <td style={{ padding: '12px 16px', fontWeight: 600, color: 'var(--text-secondary)' }}>{row.label}</td>
                      {selectedStates.map(s => (
                        <td key={s.id} style={{ textAlign: 'center', padding: '12px 16px', fontWeight: 700, color: 'var(--text-primary)' }}>
                          {row.getValue(s)}
                        </td>
                      ))}
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>
        )}
      </div>
    </>
  )
}

