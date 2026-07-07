import { useEffect, useState, useMemo } from 'react'
import { useNavigate } from 'react-router-dom'
import { Search, FileText, ChevronRight, AlertCircle } from 'lucide-react'
import { fetchJson } from '../lib/dataCache.js'

function highlightText(text, query) {
  if (!query || !text) return text
  const escaped = query.replace(/[.*+?^${}()|[\]\\]/g, '\\$&')
  const parts = text.split(new RegExp(`(${escaped})`, 'gi'))
  return parts.map((part, i) =>
    part.toLowerCase() === query.toLowerCase()
      ? <mark key={i}>{part}</mark>
      : part
  )
}

function getSnippet(text, query, maxLen = 200) {
  if (!text || !query) return ''
  const idx = text.toLowerCase().indexOf(query.toLowerCase())
  if (idx === -1) return text.slice(0, maxLen) + '...'
  const start = Math.max(0, idx - 60)
  const end = Math.min(text.length, idx + query.length + 140)
  return (start > 0 ? '...' : '') + text.slice(start, end) + (end < text.length ? '...' : '')
}

export default function SearchPage() {
  const [data, setData] = useState(null)
  const [dataError, setDataError] = useState(null)
  const [markdownCache, setMarkdownCache] = useState({})
  const [query, setQuery] = useState('')
  const [debouncedQuery, setDebouncedQuery] = useState('')
  const [loading, setLoading] = useState(false)
  const navigate = useNavigate()

  // Carrega dados dos estados
  useEffect(() => {
    fetchJson('/database/states_data.json')
      .then(setData)
      .catch(() => setDataError('Não foi possível carregar a base de dados. Recarregue a página.'))
  }, [])

  // Debounce da query
  useEffect(() => {
    const t = setTimeout(() => setDebouncedQuery(query), 350)
    return () => clearTimeout(t)
  }, [query])

  // Busca nos dados estruturados (organograma, documentos, base legal)
  const structuralResults = useMemo(() => {
    if (!data || !debouncedQuery || debouncedQuery.length < 2) return []
    const q = debouncedQuery.toLowerCase()

    const results = []

    data.states.forEach(state => {
      const matches = []

      // Busca no nome
      if (state.name.toLowerCase().includes(q)) {
        matches.push({ type: 'nome', text: state.name, field: 'Estado' })
      }

      // Busca na base legal
      if (state.legal_basis?.toLowerCase().includes(q)) {
        matches.push({ type: 'legal', text: state.legal_basis, field: 'Base Legal' })
      }

      // Busca nos órgãos (recursivo)
      function searchOrgans(organs) {
        if (!organs) return
        organs.forEach(organ => {
          if (organ.name?.toLowerCase().includes(q)) {
            matches.push({ type: 'organ', text: organ.name, field: 'Órgão / Seção' })
          }
          if (organ.description?.toLowerCase().includes(q)) {
            matches.push({ type: 'organ', text: getSnippet(organ.description, debouncedQuery), field: 'Descrição de Órgão' })
          }
          if (organ.children?.length) searchOrgans(organ.children)
        })
      }
      searchOrgans(state.organs)

      // Busca nos títulos dos documentos e tipos
      state.documents?.forEach(doc => {
        if (doc.type?.toLowerCase().includes(q)) {
          matches.push({ type: 'doc', text: doc.type, field: 'Tipo de Documento' })
        }
        doc.laws?.forEach(l => {
          const lawStr = `${l.tipo} nº ${l.numero}`
          if (lawStr.toLowerCase().includes(q)) {
            matches.push({ type: 'law', text: lawStr, field: 'Número de Lei' })
          }
        })
      })

      // Busca nos capítulos
      state.chapters_summary?.forEach(ch => {
        if (ch.title?.toLowerCase().includes(q)) {
          matches.push({ type: 'chapter', text: ch.title, field: `Capítulo ${ch.number}` })
        }
      })

      if (matches.length > 0) {
        results.push({
          state,
          matches: matches.slice(0, 6),
          totalMatches: matches.length
        })
      }
    })

    return results.slice(0, 30)
  }, [data, debouncedQuery])

  const totalResults = structuralResults.reduce((acc, r) => acc + r.totalMatches, 0)

  return (
    <>
      <div className="page-header">
        <div className="page-header-left">
          <h1 className="page-title">Busca Textual Avançada</h1>
          <p className="page-subtitle">Pesquise em toda a base de dados estruturada — órgãos, leis, atribuições e capítulos</p>
        </div>
      </div>

      <div className="page-body">
        {dataError && (
          <div className="empty-state">
            <AlertCircle size={40} className="empty-state-icon" />
            <h3>Erro ao carregar</h3>
            <p>{dataError}</p>
          </div>
        )}

        {/* Campo de busca principal */}
        <div style={{ marginBottom: 16 }}>
          <div className="search-input-wrap" style={{ maxWidth: 640 }}>
            <Search size={18} className="search-input-icon" />
            <input
              className="search-input"
              style={{ fontSize: 15, padding: '12px 14px 12px 44px' }}
              placeholder="Buscar órgãos, leis, artigos, atribuições..."
              value={query}
              onChange={e => setQuery(e.target.value)}
              autoFocus
            />
          </div>
        </div>

        {/* Resultados */}
        {debouncedQuery.length >= 2 && (
          <div style={{ marginBottom: 12, fontSize: 13, color: 'var(--text-muted)' }}>
            {structuralResults.length > 0
              ? <>{totalResults} ocorrência{totalResults !== 1 ? 's' : ''} em <strong style={{ color: 'var(--text-primary)' }}>{structuralResults.length}</strong> estado{structuralResults.length !== 1 ? 's' : ''}</>
              : 'Nenhum resultado encontrado nos dados estruturados.'}
          </div>
        )}

        {debouncedQuery.length >= 2 && structuralResults.length === 0 && (
          <div className="empty-state">
            <Search size={36} className="empty-state-icon" />
            <h3>Nenhum resultado</h3>
            <p>A busca por "<strong>{debouncedQuery}</strong>" não encontrou correspondências nos dados estruturados.</p>
            <div style={{ marginTop: 12, fontSize: 13, color: 'var(--text-muted)', maxWidth: 420, textAlign: 'center' }}>
              Dica: tente termos como "Diretoria", "Estado-Maior", "Corregedoria", "Batalhão" ou número de lei como "8.255".
            </div>
          </div>
        )}

        {debouncedQuery.length < 2 && !debouncedQuery && (
          <div className="empty-state">
            <Search size={40} className="empty-state-icon" />
            <h3>Pronto para buscar</h3>
            <p>Digite pelo menos 2 caracteres para iniciar a pesquisa nos dados estruturados de todos os estados.</p>
          </div>
        )}

        {/* Cards de resultado */}
        <div style={{ display: 'flex', flexDirection: 'column', gap: 12 }}>
          {structuralResults.map(({ state, matches, totalMatches }) => (
            <div
              key={state.id}
              className="card"
              style={{ cursor: 'pointer', transition: 'all 0.15s' }}
              onClick={() => navigate(`/estados/${state.id}`)}
              onMouseEnter={e => { e.currentTarget.style.borderColor = 'var(--cbm-red-800)'; e.currentTarget.style.transform = 'translateY(-1px)' }}
              onMouseLeave={e => { e.currentTarget.style.borderColor = ''; e.currentTarget.style.transform = '' }}
            >
              <div style={{ display: 'flex', alignItems: 'flex-start', gap: 14, marginBottom: 12 }}>
                <div style={{
                  width: 42, height: 42, background: 'var(--cbm-red-800)',
                  borderRadius: 'var(--radius-md)',
                  display: 'flex', alignItems: 'center', justifyContent: 'center',
                  fontFamily: 'Outfit', fontWeight: 900, fontSize: 14, color: '#fff',
                  flexShrink: 0
                }}>
                  {state.abbreviation}
                </div>
                <div style={{ flex: 1 }}>
                  <div style={{ display: 'flex', alignItems: 'center', gap: 8, flexWrap: 'wrap' }}>
                    <span style={{ fontFamily: 'Outfit', fontSize: 15, fontWeight: 700 }}>{state.name}</span>
                    <span style={{ fontSize: 12, color: 'var(--cbm-red-400)', fontWeight: 700 }}>{state.cbm_abbreviation}</span>
                    <span className="badge badge-gray" style={{ fontSize: 10 }}>
                      {totalMatches} ocorrência{totalMatches !== 1 ? 's' : ''}
                    </span>
                  </div>
                </div>
                <ChevronRight size={18} color="var(--cbm-gray-400)" />
              </div>

              <div style={{ display: 'flex', flexDirection: 'column', gap: 6 }}>
                {matches.map((match, i) => (
                  <div key={i} style={{
                    display: 'flex', gap: 10, padding: '7px 10px',
                    background: 'var(--bg-surface)', borderRadius: 'var(--radius-sm)',
                    alignItems: 'flex-start'
                  }}>
                    <span style={{ fontSize: 10, fontWeight: 700, textTransform: 'uppercase', letterSpacing: '0.6px', color: 'var(--cbm-gold-400)', minWidth: 120, flexShrink: 0, paddingTop: 1 }}>
                      {match.field}
                    </span>
                    <span style={{ fontSize: 12.5, color: 'var(--text-secondary)', lineHeight: 1.5 }}>
                      {highlightText(match.text, debouncedQuery)}
                    </span>
                  </div>
                ))}
              </div>
            </div>
          ))}
        </div>

        {/* Nota sobre busca full-text */}
        {debouncedQuery.length >= 2 && (
          <div style={{ marginTop: 20, display: 'flex', gap: 8, padding: '10px 14px', background: 'var(--bg-surface)', borderRadius: 'var(--radius-md)', border: '1px solid var(--border-subtle)' }}>
            <AlertCircle size={14} color="var(--cbm-gray-400)" style={{ flexShrink: 0, marginTop: 1 }} />
            <span style={{ fontSize: 12, color: 'var(--text-muted)' }}>
              A busca atua sobre os dados estruturados extraídos (organograma, base legal, capítulos). Para busca nos textos completos das legislações,
              acesse cada estado individualmente e utilize Ctrl+F no documento.
            </span>
          </div>
        )}
      </div>
    </>
  )
}
