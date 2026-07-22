// Painel lateral de detalhe de capítulo, compartilhado por MinutaDiagrams (RI) e
// RegDiagramas (Regulamento). Extraído verbatim de MinutaDiagrams.jsx (2026-07-21).
import { X } from 'lucide-react'

// Badge de fonte (RO não recebe badge); espelha o padrão do MinutaWizard.
// whiteSpace:nowrap + inline-block mantêm a citação inteira numa linha só
// (quebra como um bloco, em vez de partir "cf." do resto).
function srcBadge(source) {
  if (!source || source === 'ro') return null
  return (
    <span style={{
      marginLeft: 6, fontSize: 11, fontFamily: 'Inter, sans-serif', fontWeight: 600,
      color: '#fff', background: 'var(--cbm-red-700)', borderRadius: 4, padding: '1px 6px',
      whiteSpace: 'nowrap', display: 'inline-block', verticalAlign: 'baseline',
    }}>{source}</span>
  )
}

// Inicial maiúscula para exibição (itens verbatim começam em minúscula).
function capitalizeFirst(text) {
  const t = (text || '').trim()
  return t ? t.charAt(0).toUpperCase() + t.slice(1) : t
}

function panelSections(ch) {
  if (ch.kind === 'organ') return ch.sections || []
  if (ch.kind === 'articles') return ch.articles || []
  return [{ sectionTitle: null, caput: null, items: [], proposedText: ch.proposedText }]
}

export default function MinutaDetailPanel({ chapter, onClose }) {
  const sections = panelSections(chapter)
  return (
    <aside className="md-panel no-print">
      <div className="md-panel-head">
        <span>{chapter.chapterTitle}</span>
        <button type="button" className="md-panel-close" onClick={onClose} aria-label="Fechar">
          <X size={16} />
        </button>
      </div>
      <div className="md-panel-body">
        {sections.map((s, i) => {
          const items = (s.items || []).filter(it => (it.text || '').trim())
          return (
            <div key={i} className="md-panel-sec">
              {s.sectionTitle && <h4>{s.sectionTitle}</h4>}
              {s.caput && <p className="md-caput">{s.caput}</p>}
              {items.length ? (
                <ul>
                  {items.map((it, j) => <li key={j}>{capitalizeFirst(it.text)}{srcBadge(it.source)}</li>)}
                </ul>
              ) : s.proposedText ? (
                <p className="md-prose">{s.proposedText}</p>
              ) : null}
            </div>
          )
        })}
      </div>
    </aside>
  )
}
