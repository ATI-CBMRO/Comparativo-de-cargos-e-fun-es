import { useState, useEffect } from 'react'
import SuggestionCard from './SuggestionCard.jsx'

// target: para inciso = { kind:'inciso', chapterId, editId, incisoIndex, originalText, label }
//         para nova seção = { kind:'novaSecao', chapterId, editId(=chapterId), label }
// onAddSuggestion(payload) cria a sugestão; onSupport/onComment refrescam.
export default function SuggestionPanel({ target, suggestions, users, currentUser, onAddSuggestion, onSupport, onComment, onClose }) {
  const incisoTypes = [
    { v: 'editar', label: 'Editar' },
    { v: 'incluir', label: 'Incluir' },
    { v: 'remover', label: 'Remover' },
  ]
  const isNovaSecao = target?.kind === 'novaSecao'
  const [type, setType] = useState(isNovaSecao ? 'incluir-secao' : 'editar')
  const [proposed, setProposed] = useState('')
  const [sectionTitle, setSectionTitle] = useState('')
  const [justification, setJustification] = useState('')

  // Reseta o compositor quando muda o alvo selecionado.
  useEffect(() => {
    setType(isNovaSecao ? 'incluir-secao' : 'editar')
    // Pré-preenche o texto proposto com o inciso atual (a edição parte do texto vigente).
    setProposed(isNovaSecao ? '' : (target?.originalText ?? ''))
    setSectionTitle(''); setJustification('')
  }, [target?.editId, target?.incisoIndex, isNovaSecao])

  if (!target) {
    return (
      <div style={{ flex: 1, alignSelf: 'flex-start', position: 'sticky', top: 'calc(var(--header-h) + 8px)', background: '#f7f9fc', borderRadius: 8, padding: 16, color: 'var(--text-muted)', fontSize: 13 }}>
        Selecione um inciso (ou "+ nova seção") para ver e propor sugestões.
      </div>
    )
  }

  const needsProposed = type !== 'remover'

  // Trocar o tipo ajusta o texto proposto: Editar parte do texto vigente; Incluir começa vazio.
  function chooseType(t) {
    setType(t)
    if (t === 'editar') setProposed(target?.originalText ?? '')
    else if (t === 'incluir') setProposed('')
  }

  function submit() {
    if (needsProposed && !proposed.trim()) return
    if (type === 'incluir-secao' && !sectionTitle.trim()) return
    onAddSuggestion({
      chapterId: target.chapterId,
      targetId: target.editId,
      targetKind: isNovaSecao ? 'secao' : 'inciso',
      incisoIndex: isNovaSecao ? null : target.incisoIndex,
      type,
      originalText: target.originalText ?? '',
      proposedText: needsProposed ? proposed.trim() : '',
      sectionTitle: sectionTitle.trim(),
      justification: justification.trim(),
      authorId: currentUser?.id,
    })
    setProposed(''); setSectionTitle(''); setJustification('')
  }

  return (
    <div style={{ flex: 1, minWidth: 0, alignSelf: 'flex-start', position: 'sticky', top: 'calc(var(--header-h) + 8px)', background: '#f7f9fc', borderRadius: 8, padding: 12, display: 'flex', flexDirection: 'column', maxHeight: 'calc(100vh - var(--header-h) - 24px)' }}>
      <div style={{ display: 'flex', alignItems: 'baseline', marginBottom: 8 }}>
        <div style={{ font: '700 11px Inter, sans-serif', color: '#121d3d', textTransform: 'uppercase', letterSpacing: .3 }}>
          {target.label}
          <span style={{ display: 'block', fontWeight: 500, textTransform: 'none', color: '#8a93a6', fontSize: 10.5 }}>
            {suggestions.length} sugestão(ões)
          </span>
        </div>
        <button onClick={onClose} style={{ marginLeft: 'auto', border: 'none', background: 'none', cursor: 'pointer', color: '#8a93a6', fontSize: 16 }} title="Fechar">×</button>
      </div>

      <div style={{ overflow: 'auto', flex: 1 }}>
        {suggestions.length === 0 && (
          <p style={{ color: 'var(--text-muted)', fontSize: 12.5 }}>Ainda sem sugestões neste item. Seja o primeiro.</p>
        )}
        {suggestions.map(s => (
          <SuggestionCard key={s.id} suggestion={s} users={users} currentUser={currentUser} mode="review" onSupport={onSupport} onComment={onComment} />
        ))}
      </div>

      <div style={{ marginTop: 10, background: '#fff', border: '1px solid #e1e7f0', borderRadius: 8, padding: 9 }}>
        {!isNovaSecao && (
          <div style={{ display: 'flex', gap: 4, marginBottom: 6 }}>
            {incisoTypes.map(t => (
              <button key={t.v} onClick={() => chooseType(t.v)} style={{
                font: '700 9px Inter, sans-serif', padding: '4px 9px', borderRadius: 5, cursor: 'pointer',
                border: '1px solid', borderColor: type === t.v ? '#c8102e' : '#d6deea',
                background: type === t.v ? '#c8102e' : '#fff', color: type === t.v ? '#fff' : '#5a6377',
              }}>{t.label}</button>
            ))}
          </div>
        )}
        {isNovaSecao && (
          <input value={sectionTitle} onChange={e => setSectionTitle(e.target.value)} placeholder="Título da nova seção (ex.: Das Atribuições do Chefe)"
            style={{ width: '100%', boxSizing: 'border-box', border: '1px solid #d6deea', borderRadius: 5, fontSize: 12.5, padding: 6, marginBottom: 6 }} />
        )}
        {needsProposed && (
          <textarea value={proposed} onChange={e => setProposed(e.target.value)}
            placeholder={type === 'incluir' || type === 'incluir-secao' ? 'Texto do novo inciso/seção…' : 'Texto proposto…'}
            style={{ width: '100%', boxSizing: 'border-box', minHeight: 50, border: '1px solid #d6deea', borderRadius: 5, fontSize: 12.5, padding: 6, background: '#fbfcfe' }} />
        )}
        {type === 'remover' && (
          <p style={{ font: '11px Inter, sans-serif', color: '#5a6377', margin: '0 0 4px' }}>Propondo a remoção deste item.</p>
        )}
        <input value={justification} onChange={e => setJustification(e.target.value)} placeholder="Justificativa (opcional)"
          style={{ width: '100%', boxSizing: 'border-box', border: '1px solid #d6deea', borderRadius: 5, fontSize: 12, padding: 6, marginTop: 6 }} />
        <button onClick={submit} style={{ marginTop: 6, border: 'none', background: '#c8102e', color: '#fff', font: '700 10px Inter, sans-serif', padding: '6px 12px', borderRadius: 5, cursor: 'pointer' }}>
          Enviar sugestão
        </button>
      </div>
    </div>
  )
}
