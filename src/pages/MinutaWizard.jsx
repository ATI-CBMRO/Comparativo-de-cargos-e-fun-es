import { useState, useEffect, useMemo } from 'react'
import { ChevronRight, Download, ArrowLeft, Pencil, Check, RotateCcw } from 'lucide-react'
import {
  Document, Packer, Paragraph, TextRun,
  Footer, AlignmentType, ImageRun,
} from 'docx'
import { buildArticles, articleLabel, romanize } from '../lib/minutaArticles.js'

const STEP_LABELS = ['Visão geral', 'Revisão & curadoria', 'Download']

const slug = s => String(s).replace(/[^a-z0-9]+/gi, '-').replace(/^-|-$/g, '')
const chapterIdOf = editId => `cap-${slug(String(editId).split('/')[0])}`
const sectionIdOf = editId => `sec-${slug(editId)}`
const itemKey = (editId, index) => `${editId}#${index}`

// 'ro' -> 'RO'; 'cf. CBMPR, Lei ...' -> 'CBMPR'
function sourceKey(source) {
  if (!source || source === 'ro') return 'RO'
  const m = source.match(/^cf\.\s*([^,]+)/)
  return (m ? m[1] : source).trim()
}

// Índice editId -> { items, sectionTitle, chapterTitle, proposedText, kind }
function indexLeaves(structure) {
  const idx = {}
  for (const ch of structure.chapters) {
    if (ch.kind === 'organ') {
      for (const s of ch.sections) {
        idx[s.editId] = {
          items: s.items ?? [], proposedText: s.proposedText ?? '',
          sectionTitle: s.sectionTitle, chapterTitle: ch.chapterTitle, kind: s.kind,
        }
      }
    } else if (ch.kind === 'articles') {
      for (const a of ch.articles) {
        idx[a.editId] = {
          items: a.items ?? [], proposedText: a.proposedText ?? '',
          sectionTitle: null, chapterTitle: ch.chapterTitle, kind: a.kind,
        }
      }
    } else {
      idx[ch.editId] = {
        items: ch.items ?? [], proposedText: ch.proposedText ?? '',
        sectionTitle: null, chapterTitle: ch.chapterTitle, kind: ch.kind,
      }
    }
  }
  return idx
}

// Mapa sourceKey -> [itemKey] (todos os itens estruturados da minuta)
function indexSources(structure) {
  const map = {}
  const add = (editId, items) => {
    ;(items ?? []).forEach((it, i) => {
      if (!(it.text ?? '').trim()) return
      const k = sourceKey(it.source)
      ;(map[k] ||= []).push(itemKey(editId, i))
    })
  }
  for (const ch of structure.chapters) {
    if (ch.kind === 'organ') ch.sections.forEach(s => add(s.editId, s.items))
    else if (ch.kind === 'articles') ch.articles.forEach(a => add(a.editId, a.items))
    else add(ch.editId, ch.items)
  }
  return map
}

function srcBadge(source) {
  if (!source || source === 'ro') return null
  return (
    <span style={{
      marginLeft: 6, fontSize: 11, fontFamily: 'Inter, sans-serif',
      color: '#fff', background: '#c8102e', borderRadius: 4, padding: '1px 6px',
    }}>{source}</span>
  )
}

export default function MinutaWizard() {
  const [step, setStep] = useState(0)
  const [data, setData] = useState(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)
  const [edits, setEdits] = useState({})            // editId -> texto (modo avançado)
  const [advanced, setAdvanced] = useState(new Set())  // editIds em modo avançado
  const [excluded, setExcluded] = useState(new Set()) // "editId#index" removidos
  const [generating, setGenerating] = useState(false)

  useEffect(() => {
    fetch('/database/minuta_structure.json')
      .then(r => { if (!r.ok) throw new Error(r.status); return r.json() })
      .then(setData)
      .catch(() => setError('Erro ao carregar minuta_structure.json. Execute build_minuta_structure.py.'))
      .finally(() => setLoading(false))
  }, [])

  const leafIndex = useMemo(() => (data ? indexLeaves(data) : {}), [data])
  const sourceMap = useMemo(() => (data ? indexSources(data) : {}), [data])
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
      const dateStr = new Date().toLocaleDateString('pt-BR', { day: '2-digit', month: 'long', year: 'numeric' })
      let imageData = null
      try {
        const resp = await fetch('/BrasaoCBMRO2D-COMPLETO.png')
        if (resp.ok) imageData = await resp.arrayBuffer()
      } catch (_) { /* segue sem imagem */ }

      const children = []
      if (imageData) {
        children.push(new Paragraph({
          alignment: AlignmentType.CENTER,
          children: [new ImageRun({ data: imageData, transformation: { width: 65, height: 65 }, type: 'png' })],
        }))
      }
      children.push(
        new Paragraph({
          alignment: AlignmentType.CENTER, spacing: { before: 120 },
          children: [new TextRun({ text: 'CORPO DE BOMBEIROS MILITAR DO ESTADO DE RONDÔNIA', bold: true, size: 28, font: 'Times New Roman' })],
        }),
        new Paragraph({
          alignment: AlignmentType.CENTER,
          children: [new TextRun({ text: `Minuta de Regimento Interno — ${data.title}`, size: 24, font: 'Times New Roman' })],
        }),
        new Paragraph({
          alignment: AlignmentType.CENTER, spacing: { after: 480 },
          children: [new TextRun({ text: dateStr, size: 22, font: 'Times New Roman', italics: true })],
        }),
      )

      const articles = buildArticles(data, edits, isExcluded)
      let chapterSeen = false
      articles.forEach(art => {
        if (art.chapterTitle) {
          children.push(
            new Paragraph({
              alignment: AlignmentType.CENTER, pageBreakBefore: chapterSeen,
              spacing: { before: 240, after: 0 },
              children: [new TextRun({ text: `CAPÍTULO ${romanize(art.chapterNumber)}`, bold: true, font: 'Times New Roman', size: 26 })],
            }),
            new Paragraph({
              alignment: AlignmentType.CENTER, spacing: { after: 120 },
              children: [new TextRun({ text: art.chapterTitle, bold: true, font: 'Times New Roman', size: 26 })],
            }),
          )
          chapterSeen = true
        }
        if (art.sectionTitle) {
          children.push(new Paragraph({
            alignment: AlignmentType.CENTER, spacing: { before: 120, after: 80 },
            children: [new TextRun({ text: `Seção ${romanize(art.sectionNumber)} — ${art.sectionTitle}`, bold: true, italics: true, font: 'Times New Roman', size: 24 })],
          }))
        }
        children.push(new Paragraph({
          alignment: AlignmentType.JUSTIFIED,
          spacing: { line: 360, after: art.incisos.length ? 60 : 120 },
          indent: art.incisos.length ? undefined : { firstLine: 708 },
          children: [
            new TextRun({ text: `${articleLabel(art.number)} `, bold: true, font: 'Times New Roman', size: 24 }),
            new TextRun({ text: art.caput, font: 'Times New Roman', size: 24 }),
          ],
        }))
        art.incisos.forEach((inc, i) => {
          const runs = [new TextRun({ text: `${romanize(i + 1)} - ${inc.text}`, font: 'Times New Roman', size: 24 })]
          if (inc.source && inc.source !== 'ro') {
            runs.push(new TextRun({ text: ` (${inc.source})`, font: 'Times New Roman', size: 20, italics: true, color: '888888' }))
          }
          children.push(new Paragraph({
            alignment: AlignmentType.JUSTIFIED, spacing: { line: 360, after: 60 },
            indent: { left: 708, hanging: 340 }, children: runs,
          }))
        })
      })

      const doc = new Document({
        sections: [{
          properties: { page: { margin: { top: 1701, right: 1134, bottom: 1134, left: 1701 } } },
          footers: {
            default: new Footer({
              children: [new Paragraph({
                alignment: AlignmentType.CENTER,
                children: [new TextRun({ text: `Documento gerado pelo Portal de Legislação CBM — CBMRO · ${dateStr}`, size: 18, font: 'Times New Roman', italics: true })],
              })],
            }),
          },
          children,
        }],
      })

      const blob = await Packer.toBlob(doc)
      const url = URL.createObjectURL(blob)
      const a = document.createElement('a')
      a.href = url
      a.download = 'Minuta_RI_Operacional_CBMRO.docx'
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
        <div className="page-header"><div className="page-header-left"><h2 className="page-title">Minuta de Regimento Interno</h2></div></div>
        <div className="page-body" style={{ padding: 32 }}><p style={{ color: 'var(--text-muted)' }}>Carregando dados…</p></div>
      </>
    )
  }
  if (error) {
    return (
      <>
        <div className="page-header"><div className="page-header-left"><h2 className="page-title">Minuta de Regimento Interno</h2></div></div>
        <div className="page-body" style={{ padding: 32 }}><p style={{ color: '#c8102e' }}>{error}</p></div>
      </>
    )
  }

  const articles = buildArticles(data, edits, isExcluded)
  const renderedAdvanced = new Set()

  function scrollTo(id) {
    const el = document.getElementById(id)
    if (el) el.scrollIntoView({ behavior: 'smooth', block: 'start' })
  }

  // ── Render de um artigo no modo curadoria ──
  function renderArticle(art) {
    const blocks = []
    if (art.chapterTitle) {
      blocks.push(
        <p key={`c-${art.number}`} id={chapterIdOf(art.editId)}
          style={{ textAlign: 'center', fontWeight: 700, margin: '20px 0 6px', scrollMarginTop: 70 }}>
          CAPÍTULO {romanize(art.chapterNumber)}<br />{art.chapterTitle}
        </p>,
      )
    }
    if (art.sectionTitle) {
      blocks.push(
        <p key={`s-${art.number}`} id={sectionIdOf(art.editId)}
          style={{ textAlign: 'center', fontWeight: 600, fontStyle: 'italic', margin: '10px 0 6px', scrollMarginTop: 70 }}>
          Seção {romanize(art.sectionNumber)} — {art.sectionTitle}
        </p>,
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
          <span><strong>{romanize(i + 1)} -</strong> {inc.text}{srcBadge(inc.source)}</span>
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
          <h2 className="page-title">Minuta de Regimento Interno</h2>
          <p className="page-subtitle">
            Minuta articulada da estrutura operacional do CBMRO — do topo (DPO/COT/DOE)
            à menor fração — com competências do CBMRO e subsídios de outras legislações.
          </p>
        </div>
      </div>

      <div className="page-body">
        <div style={{ display: 'flex', alignItems: 'center', gap: 8, marginBottom: 24 }}>
          {STEP_LABELS.map((label, i) => (
            <div key={i} style={{ display: 'flex', alignItems: 'center', gap: 8 }}>
              <div style={{
                width: 28, height: 28, borderRadius: '50%', display: 'flex', alignItems: 'center', justifyContent: 'center',
                background: i <= step ? '#c8102e' : '#d1d5db', color: '#fff', fontWeight: 700, fontSize: 13, flexShrink: 0,
              }}>{i + 1}</div>
              <span style={{ fontSize: 13, color: i === step ? '#c8102e' : 'var(--text-muted)', fontWeight: i === step ? 600 : 400 }}>{label}</span>
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
              background: '#c8102e', color: '#fff', fontWeight: 600, cursor: 'pointer', fontSize: 15,
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
              {data.chapters.map(ch => (
                <div key={ch.id} style={{ marginBottom: 4 }}>
                  <button onClick={() => scrollTo(chapterIdOf(ch.id))} style={{
                    border: 'none', background: 'none', padding: '2px 0', textAlign: 'left', cursor: 'pointer',
                    color: '#121d3d', fontWeight: 600, fontSize: 12.5,
                  }}>{ch.chapterTitle}</button>
                  {ch.kind === 'organ' && ch.sections.map(s => {
                    const rm = (removedByEditId[s.editId] ?? []).length
                    return (
                      <button key={s.editId} onClick={() => scrollTo(sectionIdOf(s.editId))} style={{
                        display: 'block', border: 'none', background: 'none', padding: '1px 0 1px 12px', textAlign: 'left',
                        cursor: 'pointer', color: 'var(--text-muted)', fontSize: 12,
                      }}>{s.sectionTitle}{rm > 0 && <span style={{ color: '#c8102e', fontWeight: 700 }}> ·{rm}</span>}</button>
                    )
                  })}
                </div>
              ))}
            </nav>

            {/* Documento */}
            <div style={{ flex: 1, minWidth: 0 }}>
              {/* Barra de fontes (fixa) */}
              <div style={{
                position: 'sticky', top: 0, zIndex: 5, background: '#eef1f6', borderBottom: '1px solid var(--border-card)',
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
                <span style={{ marginLeft: 'auto', display: 'inline-flex', gap: 8 }}>
                  <button onClick={() => setAllSources(true)} style={chipBtn}>marcar todas</button>
                  <button onClick={() => setAllSources(false)} style={chipBtn}>desmarcar todas</button>
                  {removedCount > 0 && (
                    <button onClick={() => setExcluded(new Set())} style={{ ...chipBtn, color: '#c8102e', borderColor: '#c8102e' }}>
                      <RotateCcw size={12} style={{ verticalAlign: -2, marginRight: 3 }} />restaurar removidos ({removedCount})
                    </button>
                  )}
                </span>
              </div>

              <div style={{
                border: '1px solid var(--border-card)', borderRadius: 8, background: '#fff', padding: '20px 24px',
                fontFamily: 'Georgia, "Times New Roman", serif', fontSize: 14, lineHeight: 1.7, color: '#1a1a1a',
              }}>
                {articles.map(art => <div key={art.number} style={{ marginBottom: 8 }}>{renderArticle(art)}</div>)}
              </div>

              <div style={{ display: 'flex', justifyContent: 'space-between', marginTop: 18 }}>
                <button onClick={() => setStep(0)} style={{
                  display: 'flex', alignItems: 'center', gap: 6, padding: '9px 20px', border: '1.5px solid var(--border-card)',
                  borderRadius: 7, background: '#fff', cursor: 'pointer', fontSize: 14,
                }}><ArrowLeft size={16} /> Voltar</button>
                <button onClick={() => setStep(2)} style={{
                  display: 'flex', alignItems: 'center', gap: 6, padding: '9px 24px', border: 'none', borderRadius: 7,
                  background: '#c8102e', color: '#fff', fontWeight: 600, cursor: 'pointer', fontSize: 14,
                }}>Ir para download <ChevronRight size={16} /></button>
              </div>
            </div>
          </div>
        )}

        {/* Etapa 2: download */}
        {step === 2 && (
          <div style={{ maxWidth: 820 }}>
            <h3 style={{ color: '#121d3d', marginBottom: 16, fontSize: 17 }}>Resumo da minuta — {data.title}</h3>
            <div style={{ border: '1px solid var(--border-card)', borderRadius: 8, background: '#fff', padding: 24, marginBottom: 4, maxHeight: 520, overflow: 'auto' }}>
              <PlainPreview articles={articles} />
            </div>
            <div style={{ display: 'flex', gap: 12, marginTop: 24, flexWrap: 'wrap' }}>
              <button onClick={() => setStep(1)} style={{
                display: 'flex', alignItems: 'center', gap: 6, padding: '10px 20px', border: '1.5px solid var(--border-card)', borderRadius: 7,
                background: '#fff', cursor: 'pointer', fontSize: 14,
              }}><ArrowLeft size={16} /> Voltar e curar</button>
              <button onClick={handleDownload} disabled={generating} style={{
                display: 'flex', alignItems: 'center', gap: 8, padding: '10px 24px', border: 'none', borderRadius: 7,
                background: generating ? '#9ca3af' : '#c8102e', color: '#fff', fontWeight: 600, cursor: generating ? 'wait' : 'pointer', fontSize: 14,
              }}><Download size={16} />{generating ? 'Gerando…' : 'Baixar Minuta_RI_Operacional_CBMRO.docx'}</button>
            </div>
          </div>
        )}
      </div>
    </>
  )
}

const chipBtn = {
  border: '1px solid var(--border-card)', borderRadius: 5, background: '#fff',
  padding: '3px 9px', fontSize: 12, cursor: 'pointer', color: '#121d3d',
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
          <span style={{ textDecoration: 'line-through' }}>{it.text}{it.source && it.source !== 'ro' ? ` (${it.source})` : ''}</span>
        </label>
      ))}
    </div>
  )
}

// Prévia somente-leitura (etapas 0 e 2)
function PlainPreview({ articles }) {
  if (!articles.length) return <p style={{ color: 'var(--text-muted)', fontSize: 13 }}>(sem conteúdo)</p>
  return (
    <div style={{ fontFamily: 'Georgia, "Times New Roman", serif', fontSize: 14, lineHeight: 1.7, color: '#1a1a1a' }}>
      {articles.map(art => (
        <div key={art.number} style={{ marginBottom: 10 }}>
          {art.chapterTitle && (
            <p style={{ textAlign: 'center', fontWeight: 700, margin: '18px 0 6px' }}>
              CAPÍTULO {romanize(art.chapterNumber)}<br />{art.chapterTitle}
            </p>
          )}
          {art.sectionTitle && (
            <p style={{ textAlign: 'center', fontWeight: 600, fontStyle: 'italic', margin: '8px 0 8px' }}>
              Seção {romanize(art.sectionNumber)} — {art.sectionTitle}
            </p>
          )}
          <p style={{ textAlign: 'justify', margin: '0 0 6px', textIndent: art.incisos.length ? 0 : '1.25em' }}>
            <strong>{articleLabel(art.number)}</strong> {art.caput}
          </p>
          {art.incisos.map((inc, i) => (
            <p key={i} style={{ textAlign: 'justify', margin: '0 0 4px', paddingLeft: '2em', textIndent: '-1em' }}>
              {romanize(i + 1)} - {inc.text}{srcBadge(inc.source)}
            </p>
          ))}
        </div>
      ))}
    </div>
  )
}
