import { useState, useEffect, useMemo } from 'react'
import { ChevronRight, ChevronLeft, Download, ArrowLeft } from 'lucide-react'
import {
  Document, Packer, Paragraph, TextRun,
  Footer, AlignmentType, ImageRun,
} from 'docx'
import { buildArticles, articleLabel, romanize } from '../lib/minutaArticles.js'

const STEP_LABELS = ['Visão geral', 'Revisão das seções', 'Download']

// Achata a estrutura em nós-folha editáveis (cada um com editId, título e contexto).
function flattenLeaves(structure) {
  const leaves = []
  for (const ch of structure.chapters) {
    if (ch.kind === 'organ') {
      for (const s of ch.sections) {
        leaves.push({
          editId: s.editId, kind: s.kind,
          title: `${ch.abbr} — ${s.sectionTitle}`,
          chapter: ch.chapterTitle,
          proposedText: s.proposedText ?? '',
          items: s.items ?? null,
        })
      }
    } else {
      leaves.push({
        editId: ch.editId, kind: ch.kind,
        title: ch.chapterTitle,
        chapter: ch.chapterTitle,
        proposedText: ch.proposedText ?? '',
        items: ch.items ?? null,
      })
    }
  }
  return leaves
}

function ArticlePreview({ articles }) {
  if (!articles.length) {
    return <p style={{ color: 'var(--text-muted)', fontSize: 13 }}>(sem conteúdo)</p>
  }
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
              {romanize(i + 1)} - {inc.text}
              {inc.source && inc.source !== 'ro' && (
                <span style={{
                  marginLeft: 6, fontSize: 11, fontFamily: 'Inter, sans-serif',
                  color: '#fff', background: '#c8102e', borderRadius: 4, padding: '1px 6px',
                }}>{inc.source}</span>
              )}
            </p>
          ))}
        </div>
      ))}
    </div>
  )
}

export default function MinutaWizard() {
  const [step, setStep] = useState(0)
  const [data, setData] = useState(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)
  const [leafIdx, setLeafIdx] = useState(0)
  const [edits, setEdits] = useState({})
  const [generating, setGenerating] = useState(false)

  useEffect(() => {
    fetch('/database/minuta_structure.json')
      .then(r => { if (!r.ok) throw new Error(r.status); return r.json() })
      .then(setData)
      .catch(() => setError('Erro ao carregar minuta_structure.json. Execute build_minuta_structure.py.'))
      .finally(() => setLoading(false))
  }, [])

  const leaves = useMemo(() => (data ? flattenLeaves(data) : []), [data])

  function startReview() {
    // Não pré-semear edits: seções intocadas mantêm seus itens estruturados
    // (com a fonte). edits[editId] só passa a existir quando o usuário edita,
    // e aí aquela seção articula com source: null.
    setLeafIdx(0)
    setStep(1)
  }

  function handleNext() {
    if (leafIdx < leaves.length - 1) setLeafIdx(i => i + 1)
    else setStep(2)
  }
  function handlePrev() {
    if (leafIdx > 0) setLeafIdx(i => i - 1)
  }

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

      const articles = buildArticles(data, edits)
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

  const leaf = leaves[leafIdx] ?? null
  const allArticles = buildArticles(data, edits)

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
        <div style={{ display: 'flex', alignItems: 'center', gap: 8, marginBottom: 32 }}>
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

        {/* Etapa 0: visão geral + prévia completa */}
        {step === 0 && (
          <div>
            <div style={{ border: '1px solid var(--border-card)', borderRadius: 8, background: '#fff', padding: 24, marginBottom: 20, maxHeight: 520, overflow: 'auto' }}>
              <ArticlePreview articles={buildArticles(data, {})} />
            </div>
            <button onClick={startReview} style={{
              display: 'flex', alignItems: 'center', gap: 8, padding: '11px 26px', border: 'none', borderRadius: 7,
              background: '#c8102e', color: '#fff', fontWeight: 600, cursor: 'pointer', fontSize: 15,
            }}>Revisar e editar seções <ChevronRight size={18} /></button>
          </div>
        )}

        {/* Etapa 1: revisão folha a folha */}
        {step === 1 && leaf && (
          <div style={{ display: 'flex', gap: 24, flexWrap: 'wrap', alignItems: 'flex-start' }}>
            <div style={{ flex: '1 1 420px', minWidth: 0 }}>
              <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'baseline', marginBottom: 6 }}>
                <span style={{ fontWeight: 700, color: '#121d3d', fontSize: 16 }}>{leaf.title}</span>
                <span style={{ color: 'var(--text-muted)', fontSize: 13 }}>Seção {leafIdx + 1} de {leaves.length}</span>
              </div>
              <textarea
                value={edits[leaf.editId] ?? leaf.proposedText}
                onChange={e => setEdits(prev => ({ ...prev, [leaf.editId]: e.target.value }))}
                style={{
                  width: '100%', minHeight: 320, padding: 14, border: '1.5px solid var(--border-card)', borderRadius: 8,
                  fontSize: 14, lineHeight: 1.7, fontFamily: 'Inter, sans-serif', resize: 'vertical', boxSizing: 'border-box', outline: 'none',
                }}
              />
              <div style={{ display: 'flex', justifyContent: 'space-between', marginTop: 18 }}>
                <button onClick={handlePrev} disabled={leafIdx === 0} style={{
                  display: 'flex', alignItems: 'center', gap: 6, padding: '9px 20px', border: '1.5px solid var(--border-card)', borderRadius: 7,
                  background: '#fff', cursor: leafIdx === 0 ? 'not-allowed' : 'pointer', opacity: leafIdx === 0 ? 0.4 : 1, fontSize: 14,
                }}><ChevronLeft size={16} /> Anterior</button>
                <button onClick={handleNext} style={{
                  display: 'flex', alignItems: 'center', gap: 6, padding: '9px 24px', border: 'none', borderRadius: 7,
                  background: '#c8102e', color: '#fff', fontWeight: 600, cursor: 'pointer', fontSize: 14,
                }}>{leafIdx < leaves.length - 1 ? 'Próxima' : 'Finalizar'} <ChevronRight size={16} /></button>
              </div>
            </div>
            <div style={{ flex: '1 1 360px', minWidth: 0, border: '1px solid var(--border-card)', borderRadius: 8, background: '#fff', padding: 20, position: 'sticky', top: 16, maxHeight: '80vh', overflow: 'auto' }}>
              <div style={{ fontSize: 12, fontWeight: 700, color: 'var(--text-muted)', textTransform: 'uppercase', marginBottom: 8 }}>Prévia ao vivo</div>
              <ArticlePreview articles={allArticles} />
            </div>
          </div>
        )}

        {/* Etapa 2: download */}
        {step === 2 && (
          <div style={{ maxWidth: 820 }}>
            <h3 style={{ color: '#121d3d', marginBottom: 16, fontSize: 17 }}>Resumo da minuta — {data.title}</h3>
            <div style={{ border: '1px solid var(--border-card)', borderRadius: 8, background: '#fff', padding: 24, marginBottom: 4, maxHeight: 520, overflow: 'auto' }}>
              <ArticlePreview articles={allArticles} />
            </div>
            <div style={{ display: 'flex', gap: 12, marginTop: 24, flexWrap: 'wrap' }}>
              <button onClick={() => { setLeafIdx(leaves.length - 1); setStep(1) }} style={{
                display: 'flex', alignItems: 'center', gap: 6, padding: '10px 20px', border: '1.5px solid var(--border-card)', borderRadius: 7,
                background: '#fff', cursor: 'pointer', fontSize: 14,
              }}><ArrowLeft size={16} /> Voltar e editar</button>
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
