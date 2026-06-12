import { useEffect, useMemo, useState } from 'react'
import {
  Users, CheckSquare, Square, ListChecks, Eraser, Layers,
  AlertCircle, Award, Search, LayoutGrid, Table, ChevronDown, ChevronUp, Loader
} from 'lucide-react'

/* ────────────────────────────────────────────────────────────
   Normalização e casamento de cargos (tolerante a variações)
   ──────────────────────────────────────────────────────────── */
const STOP = new Set([
  // artigos, preposições e partículas
  'de', 'do', 'da', 'dos', 'das', 'e', 'o', 'a', 'ao', 'geral',
  // títulos estruturais de cargo — presentes em quase todo nome, não distinguem função
  'diretor', 'diretoria', 'diretora',
  'comando', 'comandante', 'subcomandante',
  'coordenador', 'coordenadoria', 'coordenadora',
  'chefe', 'adjunto', 'adjunta',
  'secao', 'nucleo',
  'assessor', 'assessoria',
  'gerente', 'gerencia',
  'supervisor', 'supervisao',
])

function norm(s) {
  return (s || '')
    .normalize('NFKD').replace(/[̀-ͯ]/g, '')
    .toLowerCase().replace(/[^a-z0-9]+/g, ' ').trim()
}

function canon(s) {
  let x = norm(s)
  x = x.replace(/^chefe (d[aeo] )?/, '')
       .replace(/\bsubcomandante\b/g, 'subcomando')
       .replace(/\bcomandante\b/g, 'comando')
       .replace(/\bdiretor(a)?\b/g, 'diretoria')
       .replace(/\bcoordenador(a)?\b/g, 'coordenadoria')
  return x.replace(/\s+/g, ' ').trim()
}

function tokenSet(s) {
  return new Set(norm(s).split(' ').filter(t => t && !STOP.has(t)))
}

/** 
 * Acha o cargo correspondente e calcula o nível de similaridade.
 * Retorna dados detalhados da correspondência.
 */
function findCargoMatch(refName, targetCargos) {
  const rN = norm(refName)
  const rC = canon(refName)
  const rT = tokenSet(refName)
  
  // 1) Match exato (100% de similaridade)
  for (const c of targetCargos) {
    if (norm(c.cargo) === rN) {
      return {
        found: true,
        score: 100,
        type: 'exact',
        label: 'Correspondência Exata',
        match: c
      }
    }
  }
  
  // 2) Match canônico/sinônimo (90% de similaridade)
  for (const c of targetCargos) {
    if (canon(c.cargo) === rC) {
      return {
        found: true,
        score: 90,
        type: 'synonym',
        label: 'Por Sinônimos',
        match: c
      }
    }
  }
  
  // 3) Match parcial (sobreposição de tokens)
  let best = null
  let bestScore = 0
  let bestPercentage = 0
  
  for (const c of targetCargos) {
    const cT = tokenSet(c.cargo)
    let shared = 0
    for (const t of rT) {
      if (cT.has(t)) shared++
    }
    
    if (shared >= 1) {
      const maxTokens = Math.max(rT.size, cT.size) || 1
      const percentage = Math.round((shared / maxTokens) * 100)
      
      const cover = shared / Math.min(rT.size || 1, cT.size || 1)
      const score = shared + cover
      
      if (cover >= 0.5 && score > bestScore) {
        best = c
        bestScore = score
        bestPercentage = Math.min(85, Math.max(50, percentage))
      }
    }
  }
  
  if (best) {
    return {
      found: true,
      score: bestPercentage,
      type: 'partial',
      label: `Similaridade Parcial (${bestPercentage}%)`,
      match: best
    }
  }
  
  // 4) Não encontrado
  return {
    found: false,
    score: 0,
    type: 'none',
    label: 'Não Localizado',
    match: null
  }
}

/* ──────────────────────────────────────────────────────────── */

const REGION_ORDER = ['Norte', 'Nordeste', 'Centro-Oeste', 'Sudeste', 'Sul']
const REF_ID = 'ro'

/**
 * Formata texto verbatim aplicando negrito a postos e termos de subordinação
 */
function renderFriendlyText(text) {
  if (!text) return <span className="cc-empty">—</span>
  
  let html = text
  
  // Postos, quadros, e termos relevantes para negrito
  const patterns = [
    { regex: /\b(Oficiais|Oficial superior|Oficiais superiores|Oficial da ativa|Oficiais da ativa|último posto|último Posto|Coronéis|Coronel|Tenente-Coronel|Majores|Major|Capitão|Tenente|Praças|QOEMBM|QCOBM|CCEMBM)\b/gi, replacement: '<strong>$1</strong>' },
    { regex: /\b(Governador do Estado|Governador|Secretário de Estado|Comandante-Geral|Subcomandante-Geral|Chefe do Estado-Maior|Chefe do EMG|Estado-Maior Geral|Subcomandante|Comandante|Diretor-Geral|Diretor|Diretora|Coordenador|Coordenadora)\b/gi, replacement: '<strong>$1</strong>' }
  ]
  
  patterns.forEach(p => {
    html = html.replace(p.regex, p.replacement)
  })
  
  return <span dangerouslySetInnerHTML={{ __html: html }} />
}

function ListCell({ items }) {
  if (!items || items.length === 0) return <span className="cc-empty">—</span>
  return (
    <ul className="cc-list">
      {items.map((it, i) => <li key={i}>{renderFriendlyText(it)}</li>)}
    </ul>
  )
}

/** Monta os campos comparáveis de um cargo */
function cargoFields(cargo, organName) {
  return {
    found: !!cargo,
    cargoLocal: cargo?.cargo || null,
    organ: organName || null,
    requisito: cargo?.requisito || null,
    subordinadoA: cargo?.subordinadoA || null,
    desdobramentos: cargo?.desdobramentos || [],
    atribuicoes: cargo?.atribuicoes || [],
  }
}

export default function CargoComparator({ states }) {
  const [refOrgans, setRefOrgans] = useState(null)      // órgãos do ro.json
  const [selectedCargoKey, setSelectedCargoKey] = useState('')
  const [loadedDetails, setLoadedDetails] = useState({})    // cache: { id: organs }
  const [isBatchLoading, setIsBatchLoading] = useState(true)
  const [loadProgress, setLoadProgress] = useState(0)
  
  // Controles de Visualização e Filtro
  const [activeView, setActiveView] = useState('table')    // 'table' ou 'cards'
  const [filterRegion, setFilterRegion] = useState('all')
  const [filterSimilarity, setFilterSimilarity] = useState('all')
  const [searchState, setSearchState] = useState('')
  
  // Controle de sanfona (accordion) nos cards
  const [openAccordion, setOpenAccordion] = useState({}) // { 'stateId::sectionKey': boolean }

  // Estados de destino (todos menos RO)
  const targetStates = useMemo(
    () => (states || []).filter(s => s.id !== REF_ID),
    [states]
  )

  // Carrega a referência canônica (ro.json)
  useEffect(() => {
    fetch(`/database/organs_detail/${REF_ID}.json`)
      .then(r => r.ok ? r.json() : null)
      .then(d => { if (d?.organs) setRefOrgans(d.organs) })
      .catch(() => {})
  }, [])

  // Carrega todos os 26 estados automaticamente e assincronamente ao montar o componente
  useEffect(() => {
    if (!targetStates.length) return
    
    setIsBatchLoading(true)
    setLoadProgress(0)
    
    let loadedCount = 0
    // Filtra para carregar apenas quem não está carregado
    const toLoad = targetStates.filter(s => !loadedDetails[s.id])
    
    if (toLoad.length === 0) {
      setIsBatchLoading(false)
      setLoadProgress(100)
      return
    }
    
    const promises = toLoad.map(state => {
      return fetch(`/database/organs_detail/${state.id}.json`)
        .then(r => r.ok ? r.json() : null)
        .then(d => {
          loadedCount++
          setLoadProgress(Math.round((loadedCount / toLoad.length) * 100))
          return { id: state.id, organs: d?.organs || {} }
        })
        .catch(() => {
          loadedCount++
          setLoadProgress(Math.round((loadedCount / toLoad.length) * 100))
          return { id: state.id, organs: {} }
        })
    })
    
    Promise.all(promises).then(results => {
      setLoadedDetails(prev => {
        const next = { ...prev }
        for (const { id, organs } of results) {
          next[id] = organs
        }
        return next
      })
      setIsBatchLoading(false)
    })
  }, [targetStates])

  // Lista achatada de cargos da referência CBMRO
  const refCargoGroups = useMemo(() => {
    if (!refOrgans) return []
    const groups = []
    for (const [oid, o] of Object.entries(refOrgans)) {
      const cargos = (o.cargos || []).map((c, i) => ({
        key: `${oid}::${i}`, cargo: c, organName: o.name, organId: oid,
      }))
      if (cargos.length) groups.push({ organId: oid, organName: o.name, cargos })
    }
    return groups
  }, [refOrgans])

  // Seleciona o primeiro cargo por padrão se não houver um selecionado
  useEffect(() => {
    if (!selectedCargoKey && refCargoGroups.length) {
      setSelectedCargoKey(refCargoGroups[0].cargos[0].key)
    }
  }, [refCargoGroups, selectedCargoKey])

  // Cargo de referência selecionado
  const refSelected = useMemo(() => {
    for (const g of refCargoGroups) {
      const found = g.cargos.find(c => c.key === selectedCargoKey)
      if (found) return found
    }
    return null
  }, [refCargoGroups, selectedCargoKey])

  // Mapeia o cargo de referência contra todos os estados de destino
  const matchesByState = useMemo(() => {
    if (!refSelected) return {}
    const out = {}
    
    for (const s of targetStates) {
      const organs = loadedDetails[s.id]
      if (!organs) {
        out[s.id] = { loading: true }
        continue
      }
      
      const flat = []
      for (const o of Object.values(organs)) {
        for (const c of (o.cargos || [])) {
          flat.push({ ...c, _organName: o.name })
        }
      }
      
      const mInfo = findCargoMatch(refSelected.cargo.cargo, flat)
      if (mInfo.found) {
        out[s.id] = {
          loading: false,
          found: true,
          score: mInfo.score,
          type: mInfo.type,
          label: mInfo.label,
          fields: cargoFields(mInfo.match, mInfo.match._organName)
        }
      } else {
        out[s.id] = {
          loading: false,
          found: false,
          score: 0,
          type: 'none',
          label: 'Não Localizado',
          fields: cargoFields(null)
        }
      }
    }
    return out
  }, [refSelected, targetStates, loadedDetails])

  // Filtra os estados com base nas escolhas de filtro do usuário
  const filteredStates = useMemo(() => {
    return targetStates.filter(s => {
      // 1) Filtro de Busca por Estado
      if (searchState.trim() !== '') {
        const query = norm(searchState)
        const nameMatch = norm(s.name).includes(query)
        const abbrMatch = norm(s.abbreviation).includes(query)
        const cbmMatch = norm(s.cbm_abbreviation).includes(query)
        if (!nameMatch && !abbrMatch && !cbmMatch) return false
      }
      
      // 2) Filtro de Região
      if (filterRegion !== 'all' && s.region !== filterRegion) return false
      
      // 3) Filtro de Similaridade
      const match = matchesByState[s.id]
      if (filterSimilarity !== 'all') {
        if (!match || match.loading) return true // Mantém enquanto carrega
        
        if (filterSimilarity === 'matched' && !match.found) return false
        if (filterSimilarity === 'not_matched' && match.found) return false
        if (filterSimilarity === 'exact' && match.type !== 'exact') return false
        if (filterSimilarity === 'high' && match.score < 90) return false
      }
      
      return true
    })
  }, [targetStates, searchState, filterRegion, filterSimilarity, matchesByState])

  const stateMeta = useMemo(() => {
    const m = {}; for (const s of states || []) m[s.id] = s; return m
  }, [states])

  const refFields = refSelected ? cargoFields(refSelected.cargo, refSelected.organName) : null

  // Rótulos das linhas da tabela sticky
  const ROWS = [
    { label: 'Cargo Local', key: 'cargoLocal', render: f => f.cargoLocal ? <strong>{f.cargoLocal}</strong> : <span className="cc-empty">—</span> },
    { label: 'Órgão Vinculado', key: 'organ', render: f => f.organ || <span className="cc-empty">—</span> },
    { label: 'Requisitos', key: 'requisito', render: f => renderFriendlyText(f.requisito) },
    { label: 'Subordinação', key: 'subordinadoA', render: f => renderFriendlyText(f.subordinadoA) },
    { label: 'Subordinados / Desdobramentos', key: 'desdobramentos', render: f => <ListCell items={f.desdobramentos} /> },
    { label: 'Atribuições (Verbatim)', key: 'atribuicoes', render: f => <ListCell items={f.atribuicoes} /> },
  ]

  // Renderiza a badge de similaridade estilizada
  const renderSimilarityBadge = (match) => {
    if (!match) return null
    if (match.loading) return <span className="similarity-badge similarity-badge-none"><Loader size={10} className="spinner" /> Carregando...</span>
    
    switch (match.type) {
      case 'exact':
        return <span className="similarity-badge similarity-badge-exact">Exata (100%)</span>
      case 'synonym':
        return <span className="similarity-badge similarity-badge-synonym">Sinônimo (90%)</span>
      case 'partial':
        return <span className="similarity-badge similarity-badge-partial">Parcial ({match.score}%)</span>
      default:
        return <span className="similarity-badge similarity-badge-none">Não Localizado</span>
    }
  }

  // Alterna o colapso do acordeão nos cards
  const toggleAccordion = (stateId, sectionKey) => {
    const key = `${stateId}::${sectionKey}`
    setOpenAccordion(prev => ({ ...prev, [key]: !prev[key] }))
  }

  // Verifica se um item do acordeão está aberto
  const isAccordionOpen = (stateId, sectionKey, defaultVal = false) => {
    const key = `${stateId}::${sectionKey}`
    return openAccordion[key] !== undefined ? openAccordion[key] : defaultVal
  }

  return (
    <div>
      {/* Controles de referência */}
      <div className="card" style={{ marginBottom: 20 }}>
        <div className="card-header">
          <span className="card-title" style={{ display: 'flex', alignItems: 'center', gap: 8 }}>
            <Award size={18} color="var(--cbm-red-700)" />
            Cargo de Referência — CBMRO (Rondônia)
          </span>
        </div>

        <div style={{ marginBottom: 10 }}>
          <label className="cc-field-label">Cargo / Função na minuta da LOB do CBMRO</label>
          <div style={{ position: 'relative', maxWidth: 520 }}>
            <select
              className="cc-select"
              value={selectedCargoKey}
              onChange={e => setSelectedCargoKey(e.target.value)}
            >
              {refCargoGroups.map(g => (
                <optgroup key={g.organId} label={g.organName}>
                  {g.cargos.map(c => (
                    <option key={c.key} value={c.key}>{c.cargo.cargo}</option>
                  ))}
                </optgroup>
              ))}
            </select>
          </div>
        </div>
      </div>

      {/* Barra de Progresso do Batch Loading */}
      {isBatchLoading && (
        <div className="batch-load-container">
          <div className="batch-load-title">Sincronizando legislações estaduais para comparação cruzada...</div>
          <div className="batch-load-bar-bg">
            <div className="batch-load-bar-fill" style={{ width: `${loadProgress}%` }} />
          </div>
          <div className="batch-load-status">Carregando dados estruturados: {loadProgress}% completo</div>
        </div>
      )}

      {/* Interface Principal de Filtros e Visualização */}
      {!isBatchLoading && (
        <>
          {/* Painel de Filtros e Layout */}
          <div className="cc-filters-card">
            {/* Visualização */}
            <div className="cc-filter-item">
              <label className="cc-field-label">Visualização</label>
              <div className="cc-view-toggle">
                <button
                  className={`cc-view-btn ${activeView === 'table' ? 'active' : ''}`}
                  onClick={() => setActiveView('table')}
                  title="Visualizar em Tabela Sticky Lado a Lado"
                >
                  <Table size={14} /> Matriz Sticky
                </button>
                <button
                  className={`cc-view-btn ${activeView === 'cards' ? 'active' : ''}`}
                  onClick={() => setActiveView('cards')}
                  title="Visualizar em Grid de Cards Expandíveis"
                >
                  <LayoutGrid size={14} /> Cards dos Estados
                </button>
              </div>
            </div>

            {/* Busca por Estado */}
            <div className="cc-filter-item">
              <label className="cc-field-label">Buscar Estado / CBM</label>
              <div className="search-input-wrap">
                <Search size={14} className="search-input-icon" />
                <input
                  type="text"
                  className="search-input"
                  placeholder="Ex: Acre, CBMDF, RO..."
                  value={searchState}
                  onChange={e => setSearchState(e.target.value)}
                  style={{ height: 38, paddingLeft: 36, fontSize: 13 }}
                />
              </div>
            </div>

            {/* Filtro por Região */}
            <div className="cc-filter-item">
              <label className="cc-field-label">Região</label>
              <select
                className="cc-select"
                value={filterRegion}
                onChange={e => setFilterRegion(e.target.value)}
                style={{ height: 38, padding: '0 12px', fontSize: 13 }}
              >
                <option value="all">Todas as Regiões</option>
                {REGION_ORDER.map(r => (
                  <option key={r} value={r}>{r}</option>
                ))}
              </select>
            </div>

            {/* Filtro de Similaridade */}
            <div className="cc-filter-item">
              <label className="cc-field-label">Nível de Similaridade</label>
              <select
                className="cc-select"
                value={filterSimilarity}
                onChange={e => setFilterSimilarity(e.target.value)}
                style={{ height: 38, padding: '0 12px', fontSize: 13 }}
              >
                <option value="all">Qualquer Similaridade</option>
                <option value="matched">Apenas Correspondentes</option>
                <option value="exact">Apenas Correspondência Exata</option>
                <option value="high">Alta Similaridade (&ge; 90%)</option>
                <option value="not_matched">Apenas Não Localizados</option>
              </select>
            </div>
          </div>

          {/* Feedback de Filtros vazios */}
          {filteredStates.length === 0 ? (
            <div className="card" style={{ padding: 40, textAlign: 'center' }}>
              <Layers size={40} style={{ opacity: 0.3, margin: '0 auto 12px' }} />
              <h3 style={{ fontSize: 16, color: 'var(--text-secondary)' }}>Nenhum CBM atende aos filtros</h3>
              <p style={{ fontSize: 13, color: 'var(--text-muted)' }}>Experimente redefinir os filtros de busca, similaridade ou região.</p>
            </div>
          ) : (
            <>
              {/* VISTA 1: Tabela Sticky Lado a Lado */}
              {activeView === 'table' && (
                <div className="cargo-compare-wrapper">
                  <table className="cargo-compare-table cc-table">
                    <thead>
                      <tr>
                        <th className="cc-col-label cc-corner">Característica</th>
                        <th className="cc-col-ro cc-corner">
                          <div className="cc-corp-head">
                            <span className="cc-corp-abbr ref">RO</span>
                            <div>
                              <div className="cc-corp-name">Rondônia (Minuta)</div>
                              <div className="cc-corp-cbm">CBMRO · Referência</div>
                            </div>
                          </div>
                        </th>
                        {filteredStates.map(s => {
                          const match = matchesByState[s.id]
                          return (
                            <th key={s.id} className="cc-col-state">
                              <div className="cc-corp-head" style={{ flexDirection: 'column', gap: 6, alignItems: 'flex-start' }}>
                                <div style={{ display: 'flex', alignItems: 'center', gap: 8 }}>
                                  <span className="cc-corp-abbr">{s.abbreviation}</span>
                                  <div>
                                    <div className="cc-corp-name">{s.name}</div>
                                    <div className="cc-corp-cbm">{s.cbm_abbreviation}</div>
                                  </div>
                                </div>
                                <div style={{ marginTop: 2 }}>{renderSimilarityBadge(match)}</div>
                              </div>
                            </th>
                          )
                        })}
                      </tr>
                    </thead>
                    <tbody>
                      {ROWS.map(row => (
                        <tr key={row.key}>
                          <td className="cc-col-label">{row.label}</td>
                          <td className="cc-col-ro cc-ref-cell">{row.render(refFields)}</td>
                          {filteredStates.map(s => {
                            const match = matchesByState[s.id]
                            if (!match || match.loading) {
                              return <td key={s.id} className="cc-col-state"><span className="cc-empty">carregando…</span></td>
                            }
                            
                            // Classe de background conforme similaridade
                            let cellClass = 'cc-col-state'
                            if (!match.found) {
                              cellClass += ' cc-col-matched-none'
                            } else if (match.type === 'exact') {
                              cellClass += ' cc-col-matched-exact'
                            } else if (match.type === 'synonym') {
                              cellClass += ' cc-col-matched-synonym'
                            } else {
                              cellClass += ' cc-col-matched-partial'
                            }

                            if (!match.found) {
                              return (
                                <td key={s.id} className={cellClass} style={{ color: 'var(--text-muted)', fontStyle: 'italic' }}>
                                  <div style={{ display: 'flex', gap: 6, alignItems: 'flex-start' }}>
                                    <AlertCircle size={13} style={{ flexShrink: 0, marginTop: 2, color: '#b91c1c' }} />
                                    <span>Não localizado na legislação deste estado.</span>
                                  </div>
                                </td>
                              )
                            }
                            return <td key={s.id} className={cellClass}>{row.render(match.fields)}</td>
                          })}
                        </tr>
                      ))}
                    </tbody>
                  </table>
                </div>
              )}

              {/* VISTA 2: Grid de Cards Expandíveis */}
              {activeView === 'cards' && (
                <div className="cc-cards-grid">
                  {filteredStates.map(s => {
                    const match = matchesByState[s.id]
                    const hasMatch = match && match.found
                    const fields = hasMatch ? match.fields : null
                    
                    let cardClass = 'cc-card-state'
                    if (!match || match.loading) cardClass += ' loading'
                    else if (!hasMatch) cardClass += ' not-matched'
                    else if (match.type === 'exact') cardClass += ' exact-matched'
                    else cardClass += ' matched'

                    return (
                      <div key={s.id} className={cardClass}>
                        <div className="cc-card-header">
                          <div style={{ display: 'flex', alignItems: 'center', gap: 8 }}>
                            <span className="cc-corp-abbr" style={{ background: hasMatch ? 'var(--navy-700)' : 'var(--gray-400)' }}>
                              {s.abbreviation}
                            </span>
                            <div>
                              <div style={{ fontSize: 13, fontWeight: 700, color: 'var(--text-primary)' }}>{s.name}</div>
                              <div style={{ fontSize: 10, color: 'var(--text-muted)', fontWeight: 600 }}>{s.cbm_abbreviation}</div>
                            </div>
                          </div>
                          <div>{renderSimilarityBadge(match)}</div>
                        </div>
                        
                        <div className="cc-card-body">
                          {match && match.loading ? (
                            <div style={{ display: 'flex', justifyContent: 'center', padding: '20px 0' }}>
                              <Loader className="spinner" size={24} color="var(--navy-500)" />
                            </div>
                          ) : !hasMatch ? (
                            <div style={{ padding: '16px 8px', textAlign: 'center', color: 'var(--text-muted)' }}>
                              <AlertCircle size={32} style={{ margin: '0 auto 8px', opacity: 0.4, color: 'var(--text-muted)' }} />
                              <div style={{ fontSize: 13, fontStyle: 'italic' }}>Nenhum cargo correspondente encontrado.</div>
                            </div>
                          ) : (
                            <>
                              <div>
                                <label className="cc-field-label" style={{ marginBottom: 2 }}>Cargo Equivalente Local</label>
                                <div className="cc-card-local-title">{fields.cargoLocal}</div>
                              </div>

                              <div>
                                <label className="cc-field-label" style={{ marginBottom: 2 }}>Órgão Vinculado</label>
                                <div className="cc-card-organ">{fields.organ || 'Não especificado'}</div>
                              </div>

                              <div className="cc-card-accordion">
                                {/* Requisitos */}
                                <div className="cc-card-accordion-item">
                                  <button
                                    className="cc-card-accordion-header"
                                    onClick={() => toggleAccordion(s.id, 'req')}
                                  >
                                    Requisitos
                                    {isAccordionOpen(s.id, 'req') ? <ChevronUp size={12} /> : <ChevronDown size={12} />}
                                  </button>
                                  {isAccordionOpen(s.id, 'req') && (
                                    <div className="cc-card-accordion-content">
                                      {renderFriendlyText(fields.requisito)}
                                    </div>
                                  )}
                                </div>

                                {/* Subordinação */}
                                <div className="cc-card-accordion-item">
                                  <button
                                    className="cc-card-accordion-header"
                                    onClick={() => toggleAccordion(s.id, 'sub')}
                                  >
                                    Subordinação
                                    {isAccordionOpen(s.id, 'sub') ? <ChevronUp size={12} /> : <ChevronDown size={12} />}
                                  </button>
                                  {isAccordionOpen(s.id, 'sub') && (
                                    <div className="cc-card-accordion-content">
                                      {renderFriendlyText(fields.subordinadoA)}
                                    </div>
                                  )}
                                </div>

                                {/* Desdobramentos */}
                                <div className="cc-card-accordion-item">
                                  <button
                                    className="cc-card-accordion-header"
                                    onClick={() => toggleAccordion(s.id, 'desd')}
                                  >
                                    Desdobramentos
                                    {isAccordionOpen(s.id, 'desd') ? <ChevronUp size={12} /> : <ChevronDown size={12} />}
                                  </button>
                                  {isAccordionOpen(s.id, 'desd') && (
                                    <div className="cc-card-accordion-content" style={{ paddingLeft: 6 }}>
                                      <ListCell items={fields.desdobramentos} />
                                    </div>
                                  )}
                                </div>

                                {/* Atribuições */}
                                <div className="cc-card-accordion-item">
                                  <button
                                    className="cc-card-accordion-header"
                                    onClick={() => toggleAccordion(s.id, 'atrib')}
                                  >
                                    Atribuições (Verbatim)
                                    {isAccordionOpen(s.id, 'atrib') ? <ChevronUp size={12} /> : <ChevronDown size={12} />}
                                  </button>
                                  {isAccordionOpen(s.id, 'atrib') && (
                                    <div className="cc-card-accordion-content" style={{ paddingLeft: 6 }}>
                                      <ListCell items={fields.atribuicoes} />
                                    </div>
                                  )}
                                </div>
                              </div>
                            </>
                          )}
                        </div>
                      </div>
                    )
                  })}
                </div>
              )}
            </>
          )}
        </>
      )}
    </div>
  )
}
