import { useState } from 'react'

const TYPE_LABEL = {
  editar: 'Editar', incluir: 'Incluir inciso', remover: 'Remover',
  'incluir-secao': 'Nova seção', 'renomear-secao': 'Renomear seção', 'remover-secao': 'Remover seção',
}
const TYPE_COLOR = {
  editar: ['#fff4d6', '#9a6b00'], incluir: ['#e8f5ec', '#1a7f37'], remover: ['#fbeaec', '#c8102e'],
  'incluir-secao': ['#e8f5ec', '#1a7f37'], 'renomear-secao': ['#fff4d6', '#9a6b00'], 'remover-secao': ['#fbeaec', '#c8102e'],
}
const initialsOf = name => (name ?? '?').split(' ').filter(Boolean).map(w => w[0]).slice(0, 2).join('').toUpperCase()
const fmtDate = iso => { try { return new Date(iso).toLocaleDateString('pt-BR') } catch { return '' } }

// mode: 'review' (apoiar/comentar) | 'deliberate' (aceitar/rejeitar).
export default function SuggestionCard({ suggestion: s, users, currentUser, mode = 'review', onSupport, onComment, onDecide }) {
  const [commenting, setCommenting] = useState(false)
  const [draft, setDraft] = useState('')
  const author = users.find(u => u.id === s.authorId)
  const [bg, fg] = TYPE_COLOR[s.type] ?? ['#eef1f6', '#444']
  const supported = s.supporters.includes(currentUser?.id)
  const showOld = s.type === 'editar' || s.type === 'remover' || s.type === 'renomear-secao'
  const showNew = s.type === 'editar' || s.type === 'incluir' || s.type === 'incluir-secao' || s.type === 'renomear-secao'
  const decided = s.status !== 'pendente'

  return (
    <div style={{
      background: '#fff', border: '1px solid #e1e7f0', borderRadius: 8, padding: '9px 10px', marginBottom: 8,
      opacity: decided && mode === 'review' ? 0.85 : 1,
    }}>
      <div style={{ display: 'flex', alignItems: 'center', gap: 6, marginBottom: 5 }}>
        <span style={{ width: 18, height: 18, borderRadius: '50%', background: '#c8102e', color: '#fff', font: '700 9px Inter, sans-serif', display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
          {initialsOf(author?.name)}
        </span>
        <span style={{ font: '700 11px Inter, sans-serif', color: '#121d3d' }}>{author?.posto} {author?.name}</span>
        <span style={{ font: '11px Inter, sans-serif', color: '#8a93a6' }}>· {fmtDate(s.createdAt)}</span>
        <span style={{ marginLeft: 'auto', font: '700 9px Inter, sans-serif', textTransform: 'uppercase', padding: '2px 6px', borderRadius: 4, background: bg, color: fg }}>
          {TYPE_LABEL[s.type] ?? s.type}
        </span>
      </div>

      {s.type === 'incluir-secao' && s.sectionTitle && (
        <div style={{ font: '700 12px Georgia, serif', color: '#121d3d', marginBottom: 3 }}>{s.sectionTitle}</div>
      )}
      {showOld && (
        <>
          <div style={{ font: '700 8px Inter, sans-serif', textTransform: 'uppercase', color: '#9aa3b5', margin: '2px 0 1px' }}>Atual</div>
          <div style={{ borderRadius: 4, padding: '3px 6px', font: '12px/1.35 Georgia, serif', background: '#fbeaec', color: '#9b3b46', textDecoration: 'line-through' }}>{s.originalText}</div>
        </>
      )}
      {showNew && (
        <>
          <div style={{ font: '700 8px Inter, sans-serif', textTransform: 'uppercase', color: '#9aa3b5', margin: '4px 0 1px' }}>Proposto</div>
          <div style={{ borderRadius: 4, padding: '3px 6px', font: '12px/1.35 Georgia, serif', background: '#e8f5ec', color: '#1a5e30' }}>{s.proposedText}</div>
        </>
      )}
      {s.justification && (
        <div style={{ font: '11px Inter, sans-serif', color: '#5a6377', marginTop: 4 }}>"{s.justification}"</div>
      )}

      {mode === 'review' && (
        <div style={{ display: 'flex', gap: 12, marginTop: 8, font: '11px Inter, sans-serif', color: '#5a6377', borderTop: '1px solid #eef1f6', paddingTop: 6 }}>
          <button onClick={() => onSupport(s)} style={{ border: 'none', background: 'none', cursor: 'pointer', color: supported ? '#c8102e' : '#5a6377', fontWeight: supported ? 700 : 400 }}>
            👍 Apoiar · {s.supporters.length}
          </button>
          <button onClick={() => setCommenting(v => !v)} style={{ border: 'none', background: 'none', cursor: 'pointer', color: '#5a6377' }}>
            💬 Comentar · {s.comments.length}
          </button>
        </div>
      )}

      {mode === 'review' && commenting && (
        <div style={{ marginTop: 6 }}>
          {s.comments.map(c => (
            <div key={c.id} style={{ font: '11px Inter, sans-serif', color: '#444', padding: '2px 0' }}>
              <strong>{users.find(u => u.id === c.authorId)?.name ?? '?'}:</strong> {c.text}
            </div>
          ))}
          <textarea value={draft} onChange={e => setDraft(e.target.value)} placeholder="escreva um comentário…"
            style={{ width: '100%', boxSizing: 'border-box', minHeight: 44, border: '1px solid #d6deea', borderRadius: 5, fontSize: 12, padding: 6, marginTop: 4 }} />
          <button
            onClick={() => { if (draft.trim()) { onComment(s, draft.trim()); setDraft('') } }}
            style={{ marginTop: 4, border: 'none', background: '#121d3d', color: '#fff', font: '700 10px Inter, sans-serif', padding: '5px 11px', borderRadius: 5, cursor: 'pointer' }}
          >Enviar comentário</button>
        </div>
      )}

      {mode === 'deliberate' && (
        <div style={{ display: 'flex', gap: 6, marginTop: 8, alignItems: 'center', borderTop: '1px solid #eef1f6', paddingTop: 7 }}>
          <button onClick={() => onDecide(s, 'aceita')} style={{ font: '700 10px Inter, sans-serif', padding: '4px 10px', borderRadius: 5, cursor: 'pointer', background: s.status === 'aceita' ? '#1a7f37' : '#e8f5ec', color: s.status === 'aceita' ? '#fff' : '#1a7f37', border: '1px solid #b6dcc1' }}>✓ Aceitar</button>
          <button onClick={() => onDecide(s, 'rejeitada')} style={{ font: '700 10px Inter, sans-serif', padding: '4px 10px', borderRadius: 5, cursor: 'pointer', background: s.status === 'rejeitada' ? '#c8102e' : '#fbeaec', color: s.status === 'rejeitada' ? '#fff' : '#c8102e', border: '1px solid #eebcc2' }}>✗ Rejeitar</button>
          <span style={{ marginLeft: 'auto', font: '10px Inter, sans-serif', color: '#8a93a6' }}>👍 {s.supporters.length}</span>
        </div>
      )}
    </div>
  )
}
