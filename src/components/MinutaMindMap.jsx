// Mapa mental: grade de cartões, um por capítulo da minuta.
// `chapters` é data.chapters; cada cartão lista suas seções (organ) ou caputs (articles).

function chapterSubitems(ch) {
  if (ch.kind === 'organ') return (ch.sections || []).map(s => s.sectionTitle).filter(Boolean)
  if (ch.kind === 'articles') return (ch.articles || []).map(a => a.caput).filter(Boolean)
  return []
}

export default function MinutaMindMap({ chapters, onSelect, selectedId }) {
  if (!chapters || !chapters.length) return null
  return (
    <div className="mmm-grid">
      {chapters.map(ch => {
        const sub = chapterSubitems(ch)
        const selected = ch.id === selectedId
        return (
          <button
            key={ch.id}
            type="button"
            className={`mmm-card${selected ? ' mmm-card-sel' : ''}`}
            onClick={() => onSelect(ch.id)}
          >
            <div className="mmm-card-head">{ch.chapterTitle}</div>
            {sub.length ? (
              <ul className="mmm-card-list">
                {sub.map((t, i) => <li key={i}>{t}</li>)}
              </ul>
            ) : (
              <div className="mmm-empty">Texto corrido</div>
            )}
          </button>
        )
      })}
    </div>
  )
}
