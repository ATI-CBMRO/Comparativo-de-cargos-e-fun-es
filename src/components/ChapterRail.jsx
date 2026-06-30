import { useState } from 'react'

// Trilha lateral de capítulos: filtro por texto, alternador "só com sugestões" e
// badge de contagem (vermelho > 0, cinza quando 0). `chapters` vem de buildTargets.
export default function ChapterRail({ chapters, counts, selectedId, onSelect }) {
  const [filter, setFilter] = useState('')
  const [onlyWith, setOnlyWith] = useState(false)
  const f = filter.trim().toLowerCase()

  const list = chapters.filter(c => {
    if (f && !c.chapterTitle.toLowerCase().includes(f)) return false
    if (onlyWith && !((counts[c.chapterId] ?? 0) > 0)) return false
    return true
  })

  return (
    <nav className="rev-rail" style={{
      flex: '0 0 210px', alignSelf: 'flex-start', position: 'sticky', top: 'calc(var(--header-h) + 8px)',
      maxHeight: 'calc(100vh - var(--header-h) - 24px)', overflow: 'auto',
      border: '1px solid var(--border-card)', borderRadius: 8, background: '#fff', padding: 12,
    }}>
      <div style={{ fontWeight: 700, color: 'var(--text-muted)', textTransform: 'uppercase', fontSize: 11, marginBottom: 8 }}>
        Capítulos
      </div>
      <input
        value={filter}
        onChange={e => setFilter(e.target.value)}
        placeholder="filtrar capítulo…"
        style={{ width: '100%', boxSizing: 'border-box', padding: '5px 8px', border: '1px solid var(--border-card)', borderRadius: 6, fontSize: 13, marginBottom: 6 }}
      />
      <label style={{ display: 'flex', alignItems: 'center', gap: 6, fontSize: 12, color: 'var(--text-muted)', marginBottom: 8, cursor: 'pointer' }}>
        <input type="checkbox" checked={onlyWith} onChange={e => setOnlyWith(e.target.checked)} /> só com sugestões
      </label>
      {list.map(c => {
        const n = counts[c.chapterId] ?? 0
        const active = c.chapterId === selectedId
        return (
          <button
            key={c.chapterId}
            onClick={() => onSelect(c.chapterId)}
            style={{
              display: 'flex', alignItems: 'center', gap: 6, width: '100%', textAlign: 'left',
              border: 'none', background: active ? '#fdeaec' : 'none',
              color: active ? '#c8102e' : '#444', fontWeight: active ? 700 : 500,
              padding: '5px 6px', borderRadius: 6, cursor: 'pointer', fontSize: 12.5, marginBottom: 2,
            }}
          >
            <span style={{ flex: 1 }}>{c.chapterTitle}</span>
            <span style={{
              minWidth: 18, textAlign: 'center', padding: '0 5px', height: 16, lineHeight: '16px',
              borderRadius: 8, fontSize: 10, fontWeight: 700,
              background: n > 0 ? '#c8102e' : '#d6deea', color: n > 0 ? '#fff' : '#5a6377',
            }}>{n}</span>
          </button>
        )
      })}
    </nav>
  )
}
