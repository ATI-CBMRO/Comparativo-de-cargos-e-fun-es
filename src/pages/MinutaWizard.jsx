import { useState, useEffect } from 'react'
import { ChevronRight, ChevronLeft, Download, ArrowLeft } from 'lucide-react'
import {
  Document, Packer, Paragraph, TextRun, HeadingLevel,
  Footer, AlignmentType, ImageRun,
} from 'docx'

const ORGAN_OPTIONS = [
  {
    key: 'dpo',
    label: 'DPO',
    fullName: 'Diretoria de Planejamento Operacional',
    description:
      'Órgão responsável pelo planejamento, direção, coordenação, supervisão, ' +
      'fiscalização e avaliação das atividades operacionais da Corporação.',
  },
  {
    key: 'cot',
    label: 'COT',
    fullName: 'Comando de Operações Técnicas',
    description:
      'Órgão responsável pelo controle e observância dos requisitos técnicos contra ' +
      'incêndio e pânico — análise de projetos, vistorias, fiscalização e perícia.',
  },
]

export default function MinutaWizard() {
  const [step, setStep] = useState(0)            // 0 escolha | 1 revisão | 2 download
  const [selectedOrgan, setSelectedOrgan] = useState(null)
  const [data, setData] = useState(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)
  const [sectionIdx, setSectionIdx] = useState(0)
  const [edits, setEdits] = useState({})
  const [generating, setGenerating] = useState(false)

  useEffect(() => {
    fetch('/database/minuta_structure.json')
      .then(r => { if (!r.ok) throw new Error(r.status); return r.json() })
      .then(setData)
      .catch(() => setError('Erro ao carregar minuta_structure.json. Execute build_minuta_structure.py.'))
      .finally(() => setLoading(false))
  }, [])

  function handleSelectOrgan(key) {
    const sections = data[key].sections
    const initial = {}
    sections.forEach(s => { initial[s.id] = s.proposedText })
    setEdits(initial)
    setSelectedOrgan(key)
    setSectionIdx(0)
    setStep(1)
  }

  function handleNext() {
    const sections = data[selectedOrgan].sections
    if (sectionIdx < sections.length - 1) {
      setSectionIdx(i => i + 1)
    } else {
      setStep(2)
    }
  }

  function handlePrev() {
    if (sectionIdx > 0) setSectionIdx(i => i - 1)
  }

  async function handleDownload() {
    setGenerating(true)
    try {
      const organInfo = ORGAN_OPTIONS.find(o => o.key === selectedOrgan)
      const sections  = data[selectedOrgan].sections
      const dateStr   = new Date().toLocaleDateString('pt-BR', {
        day: '2-digit', month: 'long', year: 'numeric',
      })

      // Carrega brasão como ArrayBuffer
      let imageData = null
      try {
        const resp = await fetch('/BrasaoCBMRO2D-COMPLETO.png')
        if (resp.ok) imageData = await resp.arrayBuffer()
      } catch (_) { /* continua sem imagem */ }

      const children = []

      // Cabeçalho do documento
      if (imageData) {
        children.push(
          new Paragraph({
            alignment: AlignmentType.CENTER,
            children: [
              new ImageRun({
                data: imageData,
                transformation: { width: 65, height: 65 },
                type: 'png',
              }),
            ],
          })
        )
      }
      children.push(
        new Paragraph({
          alignment: AlignmentType.CENTER,
          spacing: { before: 120 },
          children: [
            new TextRun({
              text: 'CORPO DE BOMBEIROS MILITAR DO ESTADO DE RONDÔNIA',
              bold: true, size: 28, font: 'Times New Roman',
            }),
          ],
        }),
        new Paragraph({
          alignment: AlignmentType.CENTER,
          children: [
            new TextRun({
              text: `Minuta de Regimento Interno — ${organInfo.fullName} (${organInfo.label})`,
              size: 24, font: 'Times New Roman',
            }),
          ],
        }),
        new Paragraph({
          alignment: AlignmentType.CENTER,
          spacing: { after: 480 },
          children: [
            new TextRun({
              text: dateStr,
              size: 22, font: 'Times New Roman', italics: true,
            }),
          ],
        })
      )

      // Capítulos
      sections.forEach((section, idx) => {
        children.push(
          new Paragraph({
            heading: HeadingLevel.HEADING_1,
            pageBreakBefore: idx > 0,
            children: [
              new TextRun({
                text: section.title,
                font: 'Times New Roman', size: 28, bold: true,
              }),
            ],
          }),
          new Paragraph({
            spacing: { line: 360, after: 120 },
            children: [
              new TextRun({
                text: edits[section.id] || '',
                font: 'Times New Roman', size: 24,
              }),
            ],
          })
        )
      })

      const doc = new Document({
        sections: [{
          properties: {
            page: {
              margin: { top: 1701, right: 1134, bottom: 1134, left: 1701 },
            },
          },
          footers: {
            default: new Footer({
              children: [
                new Paragraph({
                  alignment: AlignmentType.CENTER,
                  children: [
                    new TextRun({
                      text: `Documento gerado pelo Portal de Legislação CBM — CBMRO · ${dateStr}`,
                      size: 18, font: 'Times New Roman', italics: true,
                    }),
                  ],
                }),
              ],
            }),
          },
          children,
        }],
      })

      const blob = await Packer.toBlob(doc)
      const url  = URL.createObjectURL(blob)
      const a    = document.createElement('a')
      a.href     = url
      a.download = `Minuta_RI_${organInfo.label}_CBMRO.docx`
      document.body.appendChild(a)
      a.click()
      document.body.removeChild(a)
      URL.revokeObjectURL(url)
    } finally {
      setGenerating(false)
    }
  }

  // ── Render guards ──
  if (loading) {
    return (
      <>
        <div className="page-header">
          <div className="page-header-left">
            <h2 className="page-title">Minuta de Regimento Interno</h2>
          </div>
        </div>
        <div className="page-body" style={{ padding: 32 }}>
          <p style={{ color: 'var(--text-muted)' }}>Carregando dados…</p>
        </div>
      </>
    )
  }

  if (error) {
    return (
      <>
        <div className="page-header">
          <div className="page-header-left">
            <h2 className="page-title">Minuta de Regimento Interno</h2>
          </div>
        </div>
        <div className="page-body" style={{ padding: 32 }}>
          <p style={{ color: '#c8102e' }}>{error}</p>
        </div>
      </>
    )
  }

  const STEP_LABELS = ['Escolha do órgão', 'Revisão das seções', 'Download']

  return (
    <>
      {/* Cabeçalho da página */}
      <div className="page-header">
        <div className="page-header-left">
          <h2 className="page-title">Minuta de Regimento Interno</h2>
          <p className="page-subtitle">
            Gere uma minuta editável em .docx para a DPO ou o COT do CBMRO,
            baseada na legislação dos 27 CBMs.
          </p>
        </div>
      </div>

      <div className="page-body">
        {/* Stepper */}
        <div style={{ display: 'flex', alignItems: 'center', gap: 8, marginBottom: 32 }}>
          {STEP_LABELS.map((label, i) => (
            <div key={i} style={{ display: 'flex', alignItems: 'center', gap: 8 }}>
              <div style={{
                width: 28, height: 28, borderRadius: '50%',
                display: 'flex', alignItems: 'center', justifyContent: 'center',
                background: i <= step ? '#c8102e' : '#d1d5db',
                color: '#fff', fontWeight: 700, fontSize: 13, flexShrink: 0,
              }}>
                {i + 1}
              </div>
              <span style={{
                fontSize: 13,
                color: i === step ? '#c8102e' : 'var(--text-muted)',
                fontWeight: i === step ? 600 : 400,
              }}>
                {label}
              </span>
              {i < 2 && <ChevronRight size={16} color="#d1d5db" style={{ flexShrink: 0 }} />}
            </div>
          ))}
        </div>

        {/* ── Etapa 0: escolha do órgão ── */}
        {step === 0 && (
          <div style={{ display: 'flex', gap: 24, flexWrap: 'wrap' }}>
            {ORGAN_OPTIONS.map(organ => (
              <button
                key={organ.key}
                onClick={() => handleSelectOrgan(organ.key)}
                style={{
                  flex: '1 1 280px', padding: 28,
                  border: '2px solid var(--border-card)', borderRadius: 12,
                  background: '#fff', cursor: 'pointer', textAlign: 'left',
                  transition: 'border-color 0.15s, box-shadow 0.15s',
                }}
                onMouseEnter={e => {
                  e.currentTarget.style.borderColor = '#c8102e'
                  e.currentTarget.style.boxShadow = '0 4px 16px rgba(200,16,46,0.10)'
                }}
                onMouseLeave={e => {
                  e.currentTarget.style.borderColor = 'var(--border-card)'
                  e.currentTarget.style.boxShadow = 'none'
                }}
              >
                <div style={{ fontWeight: 800, fontSize: 24, color: '#c8102e', marginBottom: 4 }}>
                  {organ.label}
                </div>
                <div style={{ fontWeight: 600, color: '#121d3d', marginBottom: 10, fontSize: 15 }}>
                  {organ.fullName}
                </div>
                <div style={{ color: 'var(--text-muted)', fontSize: 14, lineHeight: 1.55 }}>
                  {organ.description}
                </div>
              </button>
            ))}
          </div>
        )}

        {/* ── Etapa 1: revisão seção a seção ── */}
        {step === 1 && selectedOrgan && (() => {
          const sections = data[selectedOrgan].sections
          const section  = sections[sectionIdx]
          return (
            <div style={{ maxWidth: 760 }}>
              <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'baseline', marginBottom: 6 }}>
                <span style={{ fontWeight: 700, color: '#121d3d', fontSize: 17 }}>
                  {section.title}
                </span>
                <span style={{ color: 'var(--text-muted)', fontSize: 13 }}>
                  Seção {sectionIdx + 1} de {sections.length}
                </span>
              </div>

              {section.sources.length > 0 && (
                <div style={{ display: 'flex', gap: 6, flexWrap: 'wrap', alignItems: 'center', marginBottom: 12 }}>
                  <span style={{ fontSize: 12, color: 'var(--text-muted)' }}>Baseado em:</span>
                  {section.sources.map(s => (
                    <span key={s} style={{
                      background: '#eef1f6', border: '1px solid var(--border-card)',
                      borderRadius: 4, padding: '1px 7px',
                      fontSize: 12, fontWeight: 700, color: '#121d3d', textTransform: 'uppercase',
                    }}>
                      {s}
                    </span>
                  ))}
                </div>
              )}

              <textarea
                value={edits[section.id] ?? ''}
                onChange={e => setEdits(prev => ({ ...prev, [section.id]: e.target.value }))}
                style={{
                  width: '100%', minHeight: 280, padding: 14,
                  border: '1.5px solid var(--border-card)', borderRadius: 8,
                  fontSize: 14, lineHeight: 1.7,
                  fontFamily: 'Inter, sans-serif',
                  resize: 'vertical', boxSizing: 'border-box',
                  outline: 'none',
                }}
                onFocus={e => { e.target.style.borderColor = '#c8102e' }}
                onBlur={e => { e.target.style.borderColor = 'var(--border-card)' }}
              />

              <div style={{ display: 'flex', justifyContent: 'space-between', marginTop: 18 }}>
                <button
                  onClick={handlePrev}
                  disabled={sectionIdx === 0}
                  style={{
                    display: 'flex', alignItems: 'center', gap: 6,
                    padding: '9px 20px',
                    border: '1.5px solid var(--border-card)', borderRadius: 7,
                    background: '#fff', cursor: sectionIdx === 0 ? 'not-allowed' : 'pointer',
                    opacity: sectionIdx === 0 ? 0.4 : 1, fontSize: 14,
                  }}
                >
                  <ChevronLeft size={16} /> Anterior
                </button>
                <button
                  onClick={handleNext}
                  style={{
                    display: 'flex', alignItems: 'center', gap: 6,
                    padding: '9px 24px',
                    border: 'none', borderRadius: 7,
                    background: '#c8102e', color: '#fff',
                    fontWeight: 600, cursor: 'pointer', fontSize: 14,
                  }}
                >
                  {sectionIdx < sections.length - 1 ? 'Próxima' : 'Finalizar'}
                  <ChevronRight size={16} />
                </button>
              </div>
            </div>
          )
        })()}

        {/* ── Etapa 2: download ── */}
        {step === 2 && selectedOrgan && (() => {
          const organInfo = ORGAN_OPTIONS.find(o => o.key === selectedOrgan)
          const sections  = data[selectedOrgan].sections
          return (
            <div style={{ maxWidth: 760 }}>
              <h3 style={{ color: '#121d3d', marginBottom: 16, fontSize: 17 }}>
                Resumo da minuta — {organInfo.fullName}
              </h3>

              {sections.map(section => (
                <details
                  key={section.id}
                  style={{
                    marginBottom: 10,
                    border: '1px solid var(--border-card)',
                    borderRadius: 8, overflow: 'hidden',
                  }}
                >
                  <summary style={{
                    padding: '10px 14px', fontWeight: 600, cursor: 'pointer',
                    background: 'var(--gray-50)', color: '#121d3d', fontSize: 14,
                    listStyle: 'none', display: 'flex', alignItems: 'center', gap: 8,
                  }}>
                    {section.title}
                  </summary>
                  <pre style={{
                    padding: 14, margin: 0,
                    fontSize: 13, whiteSpace: 'pre-wrap',
                    lineHeight: 1.65, color: 'var(--text-secondary)',
                    fontFamily: 'Inter, sans-serif',
                  }}>
                    {edits[section.id] || '(vazio)'}
                  </pre>
                </details>
              ))}

              <div style={{ display: 'flex', gap: 12, marginTop: 24, flexWrap: 'wrap' }}>
                <button
                  onClick={() => { setSectionIdx(data[selectedOrgan].sections.length - 1); setStep(1) }}
                  style={{
                    display: 'flex', alignItems: 'center', gap: 6,
                    padding: '10px 20px',
                    border: '1.5px solid var(--border-card)', borderRadius: 7,
                    background: '#fff', cursor: 'pointer', fontSize: 14,
                  }}
                >
                  <ArrowLeft size={16} /> Voltar e editar
                </button>
                <button
                  onClick={handleDownload}
                  disabled={generating}
                  style={{
                    display: 'flex', alignItems: 'center', gap: 8,
                    padding: '10px 24px',
                    border: 'none', borderRadius: 7,
                    background: generating ? '#9ca3af' : '#c8102e',
                    color: '#fff', fontWeight: 600,
                    cursor: generating ? 'wait' : 'pointer', fontSize: 14,
                  }}
                >
                  <Download size={16} />
                  {generating
                    ? 'Gerando…'
                    : `Baixar Minuta_RI_${organInfo.label}_CBMRO.docx`}
                </button>
              </div>
            </div>
          )
        })()}
      </div>
    </>
  )
}
