import { useState } from 'react'

// Sumário de capítulos da Revisão da Minuta — versão real (Firebase), inspirada na
// trilha do protótipo CONDEG (ChapterRail.jsx), mas com contadores vindos das sugestões
// de verdade, distinguindo abertas × resolvidas, e recolhível no mobile.
// `chapters` vem de buildTargets(); `counts` é um Map chapterId -> { open, resolved }.
export default function RevisaoChapterRail({ chapters, counts, activeChapterId, onSelect }) {
  const [filter, setFilter] = useState('')
  const [onlyWith, setOnlyWith] = useState(false)
  const [openMobile, setOpenMobile] = useState(false)
  const f = filter.trim().toLowerCase()

  const list = chapters.filter(c => {
    if (f && !c.chapterTitle.toLowerCase().includes(f)) return false
    if (onlyWith) {
      const n = counts.get(c.chapterId)
      if (!n || (n.open === 0 && n.resolved === 0)) return false
    }
    return true
  })

  return (
    <nav className={`rc-summary${openMobile ? ' rc-summary-open' : ''}`} aria-label="Sumário de capítulos">
      <button
        type="button"
        className="rc-summary-toggle-mobile"
        onClick={() => setOpenMobile(o => !o)}
        aria-expanded={openMobile}
      >
        Sumário {openMobile ? '▾' : '▸'}
      </button>

      <div className="rc-summary-body">
        <div className="rc-summary-title">Capítulos</div>
        <input
          className="rc-summary-filter"
          value={filter}
          onChange={e => setFilter(e.target.value)}
          placeholder="Filtrar capítulo…"
        />
        <label className="rc-summary-only-toggle">
          <input type="checkbox" checked={onlyWith} onChange={e => setOnlyWith(e.target.checked)} />
          só com sugestões
        </label>

        {list.map(c => {
          const n = counts.get(c.chapterId) ?? { open: 0, resolved: 0 }
          const active = c.chapterId === activeChapterId
          return (
            <button
              key={c.chapterId}
              type="button"
              className={`rc-summary-item${active ? ' active' : ''}`}
              onClick={() => { onSelect(c.chapterId); setOpenMobile(false) }}
            >
              <span className="rc-summary-item-title">{c.chapterTitle}</span>
              {n.open > 0 && <span className="rc-badge rc-badge-open" title={`${n.open} sugestão(ões) em aberto`}>{n.open}</span>}
              {n.resolved > 0 && <span className="rc-badge rc-badge-resolved" title={`${n.resolved} resolvida(s)`}>✔ {n.resolved}</span>}
              {n.open === 0 && n.resolved === 0 && <span className="rc-badge rc-badge-empty">0</span>}
            </button>
          )
        })}
      </div>
    </nav>
  )
}
