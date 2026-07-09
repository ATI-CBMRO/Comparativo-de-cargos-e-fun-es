import { useEffect, useMemo, useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { Search, FileText, Library, ChevronRight, ExternalLink } from 'lucide-react'
import { fetchJson } from '../lib/dataCache.js'

const DOC_TYPE_SHORT = {
  'Lei de Organização Básica': 'LOB',
  'Regimento Interno': 'Regimento',
  'Regimento de Serviços': 'Reg. Serviços',
  'Regulamento Geral': 'Regulamento',
  'Normas Gerais de Ação': 'NGA',
  'Quadro Demonstrativo de Cargos': 'QDC',
  'Quadro de Organização e Distribuição': 'QOD',
}

export default function Legislations() {
  const [data, setData] = useState(null)
  const [error, setError] = useState(null)
  const [query, setQuery] = useState('')
  const navigate = useNavigate()

  useEffect(() => {
    fetchJson('/database/states_data.json')
      .then(setData)
      .catch(() => setError('Não foi possível carregar a base de dados. Recarregue a página.'))
  }, [])

  // Achata todos os documentos de todos os estados em uma única lista (ordem alfabética por estado)
  const allDocs = useMemo(() => {
    if (!data) return []
    const docs = []
    for (const s of data.states) {
      for (const doc of (s.documents || [])) {
        docs.push({
          ...doc,
          stateId: s.id,
          stateName: s.name,
          abbreviation: s.abbreviation,
          cbm_name: s.cbm_name,
          cbm_abbreviation: s.cbm_abbreviation,
        })
      }
    }
    return docs.sort((a, b) => a.stateName.localeCompare(b.stateName, 'pt-BR'))
  }, [data])

  const q = query.trim().toLowerCase()
  const filtered = useMemo(() => allDocs.filter(d => (
    !q
    || d.stateName.toLowerCase().includes(q)
    || d.cbm_abbreviation?.toLowerCase().includes(q)
    || d.cbm_name?.toLowerCase().includes(q)
    || d.type?.toLowerCase().includes(q)
    || d.laws?.some(l => `${l.tipo} ${l.numero}`.toLowerCase().includes(q))
  )), [allDocs, q])

  // Agrupa os documentos filtrados por estado (preserva a ordem alfabética)
  const groups = useMemo(() => {
    const byState = new Map()
    for (const d of filtered) {
      if (!byState.has(d.stateId)) {
        byState.set(d.stateId, {
          stateId: d.stateId, stateName: d.stateName, abbreviation: d.abbreviation,
          cbm_name: d.cbm_name, cbm_abbreviation: d.cbm_abbreviation, docs: [],
        })
      }
      byState.get(d.stateId).docs.push(d)
    }
    return [...byState.values()]
  }, [filtered])

  if (error) return (
    <div className="empty-state" style={{ marginTop: 80 }}>
      <h3>Erro ao carregar</h3>
      <p>{error}</p>
    </div>
  )

  if (!data) return (
    <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'center', height: '60vh' }}>
      <div className="spinner" />
    </div>
  )

  const totalChars = filtered.reduce((acc, d) => acc + (d.char_count || 0), 0)

  return (
    <>
      <div className="page-header">
        <div className="page-header-left">
          <h1 className="page-title">Acervo Legal</h1>
          <p className="page-subtitle">
            {allDocs.length} legislações de {data.states.length} Corpos de Bombeiros Militares, organizadas por estado
          </p>
        </div>
      </div>

      <div className="page-body">
        {/* Busca */}
        <div className="search-input-wrap" style={{ marginBottom: 12 }}>
          <Search size={16} className="search-input-icon" />
          <input
            className="search-input"
            placeholder="Buscar por estado, sigla, tipo de documento ou número da lei..."
            value={query}
            onChange={e => setQuery(e.target.value)}
          />
        </div>

        <p style={{ fontSize: 12, color: 'var(--text-muted)', marginBottom: 16 }}>
          Exibindo {filtered.length} de {allDocs.length} legislações em {groups.length} estado{groups.length !== 1 ? 's' : ''} · {(totalChars / 1000).toFixed(0)}k caracteres
        </p>

        {/* Legislações agrupadas por estado */}
        <div style={{ display: 'flex', flexDirection: 'column', gap: 20 }}>
          {groups.map(g => (
            <div key={g.stateId}>
              {/* Cabeçalho do estado (clicável) */}
              <button
                className="leg-state-head"
                onClick={() => navigate(`/estados/${g.stateId}`)}
                title={`Abrir a página de ${g.stateName}`}
              >
                <span className="leg-state-abbr">{g.abbreviation}</span>
                <span className="leg-state-meta">
                  <span className="leg-state-name">{g.stateName}</span>
                  <span className="leg-state-cbm">{g.cbm_abbreviation} · {g.cbm_name}</span>
                </span>
                <span className="badge badge-gray" style={{ fontSize: 10 }}>
                  {g.docs.length} doc{g.docs.length !== 1 ? 's' : ''}
                </span>
                <ChevronRight size={16} color="var(--gray-400)" style={{ marginLeft: 'auto' }} />
              </button>

              {/* Documentos do estado */}
              <div style={{ display: 'flex', flexDirection: 'column', gap: 8, marginTop: 8 }}>
                {g.docs.map((d, idx) => {
                  const short = DOC_TYPE_SHORT[d.type] || d.type
                  const isLob = d.type === 'Lei de Organização Básica'
                  const pdfUrl = d.md_file && d.has_pdf
                    ? `/legislacao-pdf/${encodeURIComponent(d.md_file.replace('.md', '.pdf'))}`
                    : null
                  return (
                    <div
                      key={`${d.stateId}-${idx}`}
                      className="leg-row"
                      style={{
                        display: 'flex', alignItems: 'center', gap: 14,
                        background: 'var(--bg-surface)', border: '1px solid var(--border-card)',
                        borderRadius: 'var(--radius-md)', padding: '12px 16px',
                      }}
                    >
                      <div style={{
                        width: 40, height: 40, borderRadius: 'var(--radius-md)', flexShrink: 0,
                        background: isLob ? 'rgba(183,28,28,0.2)' : 'rgba(255,179,0,0.12)',
                        display: 'flex', alignItems: 'center', justifyContent: 'center',
                      }}>
                        <FileText size={18} color={isLob ? 'var(--cbm-red-400)' : 'var(--cbm-gold-400)'} />
                      </div>

                      <div style={{ flex: 1, minWidth: 0 }}>
                        <div style={{ fontSize: 13, fontWeight: 700, color: 'var(--text-primary)', display: 'flex', alignItems: 'center', gap: 8, flexWrap: 'wrap' }}>
                          {d.type}
                          {d.laws?.length > 0 && (
                            <span style={{ fontSize: 12, color: 'var(--cbm-gold-400)', fontWeight: 600 }}>
                              {d.laws.map(l => `${l.tipo} nº ${l.numero}`).join(' · ')}
                            </span>
                          )}
                        </div>
                        <div style={{ fontSize: 12, color: 'var(--text-muted)', marginTop: 2 }}>
                          {d.year ? `${d.year}` : ''}
                          {d.year && d.char_count ? ' · ' : ''}
                          {d.char_count ? `${Math.round(d.char_count / 1000)}k car.` : ''}
                        </div>
                        {d.type !== 'Lei de Organização Básica' && (
                          <div
                            style={{ fontSize: 11, marginTop: 2, color: d.typeVerified ? 'var(--success-text, #2e7d32)' : 'var(--text-muted)' }}
                            title={d.typeVerified
                              ? 'O tipo deste documento foi conferido lendo o conteúdo de verdade, não só o nome do arquivo.'
                              : 'Este tipo de documento ainda não foi conferido por conteúdo — a classificação é só pelo nome do arquivo, pode estar incorreta.'}
                          >
                            {d.typeVerified ? '✓ tipo conferido por conteúdo' : '⚠ tipo só por nome de arquivo'}
                          </div>
                        )}
                      </div>

                      <span className={`badge ${isLob ? 'badge-red' : 'badge-gold'}`} style={{ fontSize: 10, flexShrink: 0 }}>
                        {short}
                      </span>

                      {pdfUrl && (
                        <button
                          className="btn btn-sm btn-ghost"
                          style={{ flexShrink: 0 }}
                          onClick={() => window.open(pdfUrl, '_blank')}
                          title="Abrir o PDF oficial da legislação"
                        >
                          <ExternalLink size={14} /> PDF
                        </button>
                      )}
                    </div>
                  )
                })}
              </div>
            </div>
          ))}
        </div>

        {filtered.length === 0 && (
          <div className="empty-state">
            <Library size={40} className="empty-state-icon" />
            <h3>Nenhuma legislação encontrada</h3>
            <p>Tente ajustar a busca.</p>
          </div>
        )}
      </div>
    </>
  )
}
