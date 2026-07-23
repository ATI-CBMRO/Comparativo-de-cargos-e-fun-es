import { useState, useEffect, useMemo } from 'react'
import { ChevronRight, Download, ArrowLeft, Pencil, Check, RotateCcw, AlertTriangle } from 'lucide-react'
import { buildArticles, articleLabel, romanize } from '../lib/minutaArticles.js'
import { buildMinutaBlob } from '../lib/minutaDocx.js'
import { fetchJson } from '../lib/dataCache.js'
import { LoadingState, ErrorState } from '../components/Status.jsx'
import { useScenario } from '../context/ScenarioContext.jsx'
import { scenarioDbUrl } from '../lib/scenario.js'
import { PARTE_HEADERS, parteByChapterTitle } from '../lib/regulamentoPartes.js'
import { useAuth } from '../lib/auth.jsx'
import { subscribeFinalTexts } from '../lib/reviewData.js'
import { filterFinalsByDoc, filterFinalsByScenario } from '../lib/reviewGroup.js'
import { applyFinalsToArticles } from '../lib/minutaFinals.js'
import AvisoSincronizacao from '../components/AvisoSincronizacao.jsx'

const STEP_LABELS = ['Visão geral', 'Revisão & curadoria', 'Download']

const slug = s => String(s).replace(/[^a-z0-9]+/gi, '-').replace(/^-|-$/g, '')
const chapterIdOf = editId => `cap-${slug(String(editId).split('/')[0])}`
const itemKey = (editId, index) => `${editId}#${index}`

// 'cf. CBMMT, Regulamento Geral ...' -> 'MT'; sem "cf." (fonte primária) -> 'RO'
function sourceKey(source) {
  if (!source) return 'RO'
  const m = source.match(/^cf\.\s*CBM([A-Z]{2})/)
  return m ? m[1] : (source.match(/^cf\.\s*([^,]+)/)?.[1] ?? source).trim()
}

// Índice editId -> { items, chapterTitle, proposedText, kind }
function indexLeaves(structure) {
  const idx = {}
  for (const ch of structure.chapters) {
    for (const a of ch.articles) {
      idx[a.editId] = {
        items: a.items ?? [], proposedText: a.proposedText ?? a.caput ?? '',
        chapterTitle: ch.chapterTitle, kind: a.kind,
      }
    }
  }
  return idx
}

// Mapa sourceKey -> [itemKey] (todos os itens estruturados)
function indexSources(structure) {
  const map = {}
  const add = (editId, items) => {
    ;(items ?? []).forEach((it, i) => {
      if (!(it.text ?? '').trim()) return
      const k = sourceKey(it.source)
      ;(map[k] ||= []).push(itemKey(editId, i))
    })
  }
  for (const ch of structure.chapters) ch.articles.forEach(a => add(a.editId, a.items))
  return map
}

// Mapa chapterId -> { primary, hasParcial }
function indexChapterMeta(structure) {
  const map = {}
  for (const ch of structure.chapters) {
    map[ch.id] = {
      primary: ch.primary ?? null,
      hasParcial: (ch.articles ?? []).some(a => a.match === 'parcial'),
    }
  }
  return map
}

function srcBadge(source) {
  if (!source) return null
  return (
    <span style={{
      marginLeft: 6, fontSize: 11, fontFamily: 'Inter, sans-serif',
      color: '#fff', background: 'var(--cbm-red-700)', borderRadius: 4, padding: '1px 6px',
    }}>{source}</span>
  )
}

export default function RegulamentoWizard() {
  const [step, setStep] = useState(0)
  const [data, setData] = useState(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)
  const [edits, setEdits] = useState({})            // editId -> texto (modo avançado)
  const [advanced, setAdvanced] = useState(new Set())  // editIds em modo avançado
  const [excluded, setExcluded] = useState(new Set()) // "editId#index" removidos
  const [generating, setGenerating] = useState(false)

  const { cenario } = useScenario()
  const { user } = useAuth()
  const [finals, setFinals] = useState(null)

  const [finalsErro, setFinalsErro] = useState(false)
  useEffect(() => {
    if (!user) { setFinals(null); return undefined }
    return subscribeFinalTexts(
      (v) => { setFinals(v); setFinalsErro(false) },
      (e) => { console.error('Erro finalTexts:', e); setFinalsErro(true) },
    )
  }, [user])
  const finalsDoDoc = useMemo(() => {
    if (!finals) return null
    return filterFinalsByScenario(filterFinalsByDoc(finals, 'reg'), cenario)
  }, [finals, cenario])

  useEffect(() => {
    setLoading(true)
    setError(null)
    fetchJson(scenarioDbUrl(cenario, 'regulamento_structure.json'))
      .then(setData)
      .catch(() => setError('Erro ao carregar regulamento_structure.json. Execute o script que gera a minuta do Regulamento Geral.'))
      .finally(() => setLoading(false))
  }, [cenario])

  const leafIndex = useMemo(() => (data ? indexLeaves(data) : {}), [data])
  const sourceMap = useMemo(() => (data ? indexSources(data) : {}), [data])
  const chapterMeta = useMemo(() => (data ? indexChapterMeta(data) : {}), [data])
  const sourceKeys = useMemo(() => {
    const keys = Object.keys(sourceMap)
    return ['RO', ...keys.filter(k => k !== 'RO').sort()]
  }, [sourceMap])

  const isExcluded = (editId, index) => excluded.has(itemKey(editId, index))

  function toggleItem(editId, index) {
    setExcluded(prev => {
      const next = new Set(prev)
      const k = itemKey(editId, index)
      if (next.has(k)) next.delete(k); else next.add(k)
      return next
    })
  }

  function sourceChecked(key) {
    const keys = sourceMap[key] ?? []
    return keys.some(k => !excluded.has(k))   // marcado se ao menos 1 incluso
  }

  function toggleSource(key) {
    const keys = sourceMap[key] ?? []
    const turnOff = sourceChecked(key)
    setExcluded(prev => {
      const next = new Set(prev)
      keys.forEach(k => { if (turnOff) next.add(k); else next.delete(k) })
      return next
    })
  }

  function setAllSources(on) {
    setExcluded(prev => {
      const next = new Set(prev)
      sourceKeys.forEach(key => {
        if (key === 'RO') return
        ;(sourceMap[key] ?? []).forEach(k => { if (on) next.delete(k); else next.add(k) })
      })
      return next
    })
  }

  function openAdvanced(editId) {
    setEdits(prev => prev[editId] != null ? prev : { ...prev, [editId]: leafIndex[editId]?.proposedText ?? '' })
    setAdvanced(prev => new Set(prev).add(editId))
  }
  function closeAdvanced(editId) {
    setAdvanced(prev => { const n = new Set(prev); n.delete(editId); return n })
    setEdits(prev => { const n = { ...prev }; delete n[editId]; return n })
  }

  function startReview() { setStep(1) }

  // Itens removidos por editId (para o expansor "N removidos")
  const removedByEditId = useMemo(() => {
    const map = {}
    Object.entries(leafIndex).forEach(([editId, leaf]) => {
      ;(leaf.items ?? []).forEach((it, i) => {
        if (excluded.has(itemKey(editId, i)) && (it.text ?? '').trim()) {
          ;(map[editId] ||= []).push({ ...it, index: i })
        }
      })
    })
    return map
  }, [leafIndex, excluded])

  const removedCount = excluded.size

  async function handleDownload() {
    setGenerating(true)
    try {
      const blob = await buildMinutaBlob({
        structure: data,
        edits,
        isExcluded,
        subtitle: 'Minuta de Regulamento Geral — gerada a partir dos regulamentos de 9 CBMs',
        finals: finalsDoDoc,
        skipEditIds,
      })
      const url = URL.createObjectURL(blob)
      const a = document.createElement('a')
      a.href = url
      a.download = 'Minuta_Regulamento_Geral_CBMRO.docx'
      document.body.appendChild(a)
      a.click()
      document.body.removeChild(a)
      URL.revokeObjectURL(url)
    } finally {
      setGenerating(false)
    }
  }

  if (loading) {
    return (
      <>
        <div className="page-header"><div className="page-header-left"><h2 className="page-title">Minuta do Regulamento Geral</h2></div></div>
        <LoadingState label="Carregando minuta do regulamento…" />
      </>
    )
  }
  if (error) {
    return (
      <>
        <div className="page-header"><div className="page-header-left"><h2 className="page-title">Minuta do Regulamento Geral</h2></div></div>
        <ErrorState title="Não foi possível carregar a minuta" hint={error} />
      </>
    )
  }

  const articles = buildArticles(data, edits, isExcluded)
  const skipEditIds = new Set(Object.keys(edits))
  const { articles: articlesFinais, appliedCount } = applyFinalsToArticles(articles, finalsDoDoc, { skipEditIds })
  const renderedAdvanced = new Set()
  const parteDe = parteByChapterTitle(data)

  function scrollTo(id) {
    const el = document.getElementById(id)
    if (el) el.scrollIntoView({ behavior: 'smooth', block: 'start' })
  }

  // ── Render de um artigo no modo curadoria ──
  function renderArticle(art) {
    const blocks = []
    if (art.chapterTitle) {
      const meta = chapterMeta[art.editId.split('/')[0]] ?? {}
      blocks.push(
        <div key={`c-${art.number}`} id={chapterIdOf(art.editId)} style={{ margin: '20px 0 6px', scrollMarginTop: 70 }}>
          <p style={{ textAlign: 'center', fontWeight: 700, margin: 0 }}>
            CAPÍTULO {romanize(art.chapterNumber)}<br />{art.chapterTitle}
          </p>
          <div style={{ display: 'flex', justifyContent: 'center', gap: 8, marginTop: 6, flexWrap: 'wrap' }}>
            {meta.primary && (
              <span style={{
                fontSize: 11, fontFamily: 'Inter, sans-serif', color: 'var(--navy-850)',
                background: 'var(--gray-100)', border: '1px solid var(--border-card)',
                borderRadius: 99, padding: '2px 10px', fontWeight: 600,
              }}>Fonte primária: {meta.primary.name} — {meta.primary.docLabel}</span>
            )}
            {meta.hasParcial && (
              <span style={{
                display: 'inline-flex', alignItems: 'center', gap: 4, fontSize: 11,
                fontFamily: 'Inter, sans-serif', color: 'var(--cbm-gold-500, #e69500)',
                background: 'rgba(230,149,0,0.1)', border: '1px solid rgba(230,149,0,0.3)',
                borderRadius: 99, padding: '2px 10px', fontWeight: 600,
              }}><AlertTriangle size={11} /> contém artigo(s) com correspondência parcial</span>
            )}
          </div>
        </div>,
      )
    }

    const inAdvanced = advanced.has(art.editId)
    if (inAdvanced) {
      if (!renderedAdvanced.has(art.editId)) {
        renderedAdvanced.add(art.editId)
        blocks.push(
          <div key={`adv-${art.number}`} style={{ margin: '6px 0 14px' }}>
            <textarea
              value={edits[art.editId] ?? ''}
              onChange={e => setEdits(prev => ({ ...prev, [art.editId]: e.target.value }))}
              style={{
                width: '100%', minHeight: 160, padding: 12, border: '1.5px solid var(--border-card)',
                borderRadius: 8, fontSize: 13.5, lineHeight: 1.6, fontFamily: 'Inter, sans-serif',
                resize: 'vertical', boxSizing: 'border-box', outline: 'none',
              }}
            />
            <button onClick={() => closeAdvanced(art.editId)} style={{
              marginTop: 6, display: 'inline-flex', alignItems: 'center', gap: 6, padding: '5px 12px',
              border: '1.5px solid var(--border-card)', borderRadius: 6, background: '#fff', cursor: 'pointer', fontSize: 13,
            }}><Check size={14} /> Concluir edição</button>
          </div>,
        )
      }
      return blocks
    }

    // Caput + botão "editar texto"
    blocks.push(
      <div key={`cap-${art.number}`} style={{ display: 'flex', alignItems: 'baseline', gap: 8, margin: '0 0 4px' }}>
        <p style={{ textAlign: 'justify', margin: 0, flex: 1, textIndent: art.incisos.length ? 0 : '1.25em' }}>
          <strong>{articleLabel(art.number)}</strong> {art.caput}
        </p>
        {art.hasFinal && (
          <span title="Texto final aplicado (decisão registrada no sistema)" style={{
            flexShrink: 0, display: 'inline-flex', alignItems: 'center', gap: 3, padding: '2px 7px',
            borderRadius: 5, background: '#d9f0e2', color: '#0c6b35', fontSize: 11, fontWeight: 600,
          }}><Check size={11} /> final aplicado</span>
        )}
        <button onClick={() => openAdvanced(art.editId)} title="Editar texto desta seção" style={{
          flexShrink: 0, display: 'inline-flex', alignItems: 'center', gap: 4, padding: '2px 8px',
          border: '1px solid var(--border-card)', borderRadius: 5, background: '#fff', cursor: 'pointer',
          fontSize: 12, color: 'var(--text-muted)',
        }}><Pencil size={12} /> editar</button>
      </div>,
    )

    art.incisos.forEach((inc, i) => {
      blocks.push(
        <label key={`i-${art.number}-${i}`} style={{
          display: 'flex', gap: 8, alignItems: 'flex-start', padding: '2px 0 2px 24px',
          cursor: 'pointer', textAlign: 'justify',
        }}>
          <input type="checkbox" checked
            onChange={() => toggleItem(inc.editId, inc.index)}
            style={{ marginTop: 5, flexShrink: 0, cursor: 'pointer' }} />
          <span>{inc.ownMarker ? '' : <strong>{romanize(i + 1)} -</strong>} {inc.text}{srcBadge(inc.source)}</span>
        </label>,
      )
    })

    const removed = removedByEditId[art.editId] ?? []
    if (removed.length) {
      blocks.push(<RemovedBlock key={`rm-${art.number}`} removed={removed} onRestore={toggleItem} editId={art.editId} />)
    }
    return blocks
  }

  return (
    <>
      <div className="page-header">
        <div className="page-header-left">
          <h2 className="page-title">Minuta do Regulamento Geral</h2>
          <p className="page-subtitle">
            {cenario === 'atual'
              ? `Minuta do Regulamento do CBMRO (LOB atual) — ${data?.chapters?.length ?? 0} capítulos-tema (serviço, disciplina, uniformes, ensino e demais matérias), a partir dos regulamentos de outros Corpos de Bombeiros Militares; isolada do cenário futuro.`
              : 'Minuta articulada do Regulamento Geral do CBMRO — 15 capítulos-tema, com competências, serviço operacional, disciplina e demais matérias, a partir dos regulamentos de 9 Corpos de Bombeiros Militares.'}
          </p>
        </div>
      </div>

      <div className="page-body">
        <AvisoSincronizacao visivel={finalsErro} />
        <div style={{ display: 'flex', alignItems: 'center', gap: 8, marginBottom: 24 }}>
          {STEP_LABELS.map((label, i) => (
            <div key={i} style={{ display: 'flex', alignItems: 'center', gap: 8 }}>
              <div style={{
                width: 28, height: 28, borderRadius: '50%', display: 'flex', alignItems: 'center', justifyContent: 'center',
                background: i <= step ? 'var(--cbm-red-700)' : '#d1d5db', color: '#fff', fontWeight: 700, fontSize: 13, flexShrink: 0,
              }}>{i + 1}</div>
              <span style={{ fontSize: 13, color: i === step ? 'var(--cbm-red-700)' : 'var(--text-muted)', fontWeight: i === step ? 600 : 400 }}>{label}</span>
              {i < 2 && <ChevronRight size={16} color="#d1d5db" style={{ flexShrink: 0 }} />}
            </div>
          ))}
        </div>

        {/* Etapa 0: visão geral */}
        {step === 0 && (
          <div>
            <div style={{ border: '1px solid var(--border-card)', borderRadius: 8, background: '#fff', padding: 24, marginBottom: 20, maxHeight: 520, overflow: 'auto' }}>
              <PlainPreview articles={buildArticles(data, {})} />
            </div>
            <button onClick={startReview} style={{
              display: 'flex', alignItems: 'center', gap: 8, padding: '11px 26px', border: 'none', borderRadius: 7,
              background: 'var(--cbm-red-700)', color: '#fff', fontWeight: 600, cursor: 'pointer', fontSize: 15,
            }}>Revisar e curar a minuta <ChevronRight size={18} /></button>
          </div>
        )}

        {/* Etapa 1: documento único + curadoria */}
        {step === 1 && (
          <div style={{ display: 'flex', gap: 18, alignItems: 'flex-start' }}>
            {/* Sidebar de navegação */}
            <nav style={{
              flex: '0 0 230px', position: 'sticky', top: 16, maxHeight: '82vh', overflow: 'auto',
              border: '1px solid var(--border-card)', borderRadius: 8, background: '#fff', padding: 12, fontSize: 13,
            }}>
              <div style={{ fontWeight: 700, color: 'var(--text-muted)', textTransform: 'uppercase', fontSize: 11, marginBottom: 8 }}>Sumário</div>
              {['geral', 'servico'].map(parte => {
                const caps = data.chapters.filter(ch => ch.parte === parte)
                if (!caps.length) return null
                return (
                  <div key={parte} style={{ marginBottom: 10 }}>
                    <div style={{ fontWeight: 800, color: 'var(--cbm-red-700)', fontSize: 10.5, letterSpacing: 0.5, margin: '6px 0 4px' }}>
                      {PARTE_HEADERS[parte]}
                    </div>
                    {caps.map(ch => (
                      <div key={ch.id} style={{ marginBottom: 4 }}>
                        <button onClick={() => scrollTo(chapterIdOf(ch.articles[0]?.editId ?? ch.id))} style={{
                          border: 'none', background: 'none', padding: '2px 0', textAlign: 'left', cursor: 'pointer',
                          color: 'var(--navy-850)', fontWeight: 600, fontSize: 12.5,
                        }}>{ch.chapterTitle}{ch.status === 'pendente' ? ' ⏳' : ''}</button>
                      </div>
                    ))}
                  </div>
                )
              })}
            </nav>

            {/* Documento */}
            <div style={{ flex: 1, minWidth: 0 }}>
              {/* Barra de fontes (fixa) */}
              <div style={{
                position: 'sticky', top: 0, zIndex: 5, background: 'var(--bg-app)', borderBottom: '1px solid var(--border-card)',
                padding: '10px 4px', marginBottom: 12, display: 'flex', flexWrap: 'wrap', gap: 10, alignItems: 'center',
              }}>
                <span style={{ fontSize: 12, fontWeight: 700, color: 'var(--text-muted)' }}>Fontes:</span>
                {sourceKeys.map(key => (
                  <label key={key} style={{ display: 'inline-flex', alignItems: 'center', gap: 4, fontSize: 12.5, cursor: key === 'RO' ? 'default' : 'pointer', opacity: key === 'RO' ? 0.7 : 1 }}>
                    <input type="checkbox" checked={key === 'RO' ? true : sourceChecked(key)} disabled={key === 'RO'}
                      onChange={() => toggleSource(key)} style={{ cursor: key === 'RO' ? 'default' : 'pointer' }} />
                    {key}
                  </label>
                ))}
                {appliedCount > 0 && <span className="section-bar-badge">{appliedCount} texto(s) final(is) aplicado(s)</span>}
                {!user && <span className="wiz-finais-aviso">Entre no sistema para ver os textos finais aplicados.</span>}
                <span style={{ marginLeft: 'auto', display: 'inline-flex', gap: 8 }}>
                  <button onClick={() => setAllSources(true)} style={chipBtn}>marcar todas</button>
                  <button onClick={() => setAllSources(false)} style={chipBtn}>desmarcar todas</button>
                  {removedCount > 0 && (
                    <button onClick={() => setExcluded(new Set())} style={{ ...chipBtn, color: 'var(--cbm-red-700)', borderColor: 'var(--cbm-red-700)' }}>
                      <RotateCcw size={12} style={{ verticalAlign: -2, marginRight: 3 }} />restaurar removidos ({removedCount})
                    </button>
                  )}
                </span>
              </div>

              <div style={{
                border: '1px solid var(--border-card)', borderRadius: 8, background: '#fff', padding: '20px 24px',
                fontFamily: 'Georgia, "Times New Roman", serif', fontSize: 14, lineHeight: 1.7, color: 'var(--doc-ink)',
              }}>
                {(() => {
                  let ultimaParte = null
                  return articlesFinais.map(art => {
                    const parte = art.chapterTitle ? parteDe[art.chapterTitle] : null
                    const faixa = parte && parte !== ultimaParte ? PARTE_HEADERS[parte] : null
                    if (parte) ultimaParte = parte
                    return (
                      <div key={art.number} style={{ marginBottom: 8 }}>
                        {faixa && (
                          <div style={{
                            textAlign: 'center', fontWeight: 800, fontSize: 16, letterSpacing: 1,
                            color: 'var(--cbm-red-700)', borderTop: '2px solid var(--cbm-red-700)',
                            borderBottom: '2px solid var(--cbm-red-700)', padding: '10px 0', margin: '26px 0 18px',
                          }}>{faixa}</div>
                        )}
                        {renderArticle(art)}
                      </div>
                    )
                  })
                })()}
              </div>

              <div style={{ display: 'flex', justifyContent: 'space-between', marginTop: 18 }}>
                <button onClick={() => setStep(0)} style={{
                  display: 'flex', alignItems: 'center', gap: 6, padding: '9px 20px', border: '1.5px solid var(--border-card)',
                  borderRadius: 7, background: '#fff', cursor: 'pointer', fontSize: 14,
                }}><ArrowLeft size={16} /> Voltar</button>
                <button onClick={() => setStep(2)} style={{
                  display: 'flex', alignItems: 'center', gap: 6, padding: '9px 24px', border: 'none', borderRadius: 7,
                  background: 'var(--cbm-red-700)', color: '#fff', fontWeight: 600, cursor: 'pointer', fontSize: 14,
                }}>Ir para download <ChevronRight size={16} /></button>
              </div>
            </div>
          </div>
        )}

        {/* Etapa 2: download */}
        {step === 2 && (
          <div style={{ maxWidth: 820 }}>
            <h3 style={{ color: 'var(--navy-850)', marginBottom: 16, fontSize: 17 }}>Resumo da minuta — {data.title}</h3>
            <div style={{ border: '1px solid var(--border-card)', borderRadius: 8, background: '#fff', padding: 24, marginBottom: 4, maxHeight: 520, overflow: 'auto' }}>
              <PlainPreview articles={articlesFinais} />
            </div>
            <div style={{ display: 'flex', gap: 12, marginTop: 24, flexWrap: 'wrap' }}>
              <button onClick={() => setStep(1)} style={{
                display: 'flex', alignItems: 'center', gap: 6, padding: '10px 20px', border: '1.5px solid var(--border-card)', borderRadius: 7,
                background: '#fff', cursor: 'pointer', fontSize: 14,
              }}><ArrowLeft size={16} /> Voltar e curar</button>
              <button onClick={handleDownload} disabled={generating} style={{
                display: 'flex', alignItems: 'center', gap: 8, padding: '10px 24px', border: 'none', borderRadius: 7,
                background: generating ? '#9ca3af' : 'var(--cbm-red-700)', color: '#fff', fontWeight: 600, cursor: generating ? 'wait' : 'pointer', fontSize: 14,
              }}><Download size={16} />{generating ? 'Gerando…' : 'Baixar Minuta_Regulamento_Geral_CBMRO.docx'}</button>
            </div>
          </div>
        )}
      </div>
    </>
  )
}

const chipBtn = {
  border: '1px solid var(--border-card)', borderRadius: 5, background: '#fff',
  padding: '3px 9px', fontSize: 12, cursor: 'pointer', color: 'var(--navy-850)',
}

// Expansor "N removidos" por seção
function RemovedBlock({ removed, onRestore, editId }) {
  const [open, setOpen] = useState(false)
  return (
    <div style={{ paddingLeft: 24, margin: '4px 0 8px' }}>
      <button onClick={() => setOpen(o => !o)} style={{
        border: 'none', background: 'none', cursor: 'pointer', color: 'var(--text-muted)', fontSize: 12.5, padding: 0,
      }}>{open ? '▾' : '▸'} {removed.length} removido{removed.length > 1 ? 's' : ''}</button>
      {open && removed.map(it => (
        <label key={it.index} style={{ display: 'flex', gap: 8, alignItems: 'flex-start', padding: '2px 0', cursor: 'pointer', color: '#9ca3af' }}>
          <input type="checkbox" checked={false} onChange={() => onRestore(editId, it.index)} style={{ marginTop: 4, cursor: 'pointer' }} />
          <span style={{ textDecoration: 'line-through' }}>{it.text}{it.source ? ` (${it.source})` : ''}</span>
        </label>
      ))}
    </div>
  )
}

// Prévia somente-leitura (etapas 0 e 2)
function PlainPreview({ articles }) {
  if (!articles.length) return <p style={{ color: 'var(--text-muted)', fontSize: 13 }}>(sem conteúdo)</p>
  return (
    <div style={{ fontFamily: 'Georgia, "Times New Roman", serif', fontSize: 14, lineHeight: 1.7, color: 'var(--doc-ink)' }}>
      {articles.map(art => (
        <div key={art.number} style={{ marginBottom: 10 }}>
          {art.chapterTitle && (
            <p style={{ textAlign: 'center', fontWeight: 700, margin: '18px 0 6px' }}>
              CAPÍTULO {romanize(art.chapterNumber)}<br />{art.chapterTitle}
            </p>
          )}
          <p style={{ textAlign: 'justify', margin: '0 0 6px', textIndent: art.incisos.length ? 0 : '1.25em' }}>
            <strong>{articleLabel(art.number)}</strong> {art.caput}
          </p>
          {art.incisos.map((inc, i) => (
            <p key={i} style={{ textAlign: 'justify', margin: '0 0 4px', paddingLeft: '2em', textIndent: '-1em' }}>
              {inc.ownMarker ? '' : `${romanize(i + 1)} - `}{inc.text}{srcBadge(inc.source)}
            </p>
          ))}
        </div>
      ))}
    </div>
  )
}
