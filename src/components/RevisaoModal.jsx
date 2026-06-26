import { useState } from 'react'
import { X, ThumbsUp, Trash2 } from 'lucide-react'

function formataData(criadoEm) {
  if (!criadoEm?.toDate) return ''
  return criadoEm.toDate().toLocaleString('pt-BR', {
    day: '2-digit', month: '2-digit', hour: '2-digit', minute: '2-digit',
  })
}

export default function RevisaoModal({ dispositivo, suggestions, user, onAdd, onToggleLike, onDelete, onClose }) {
  const [texto, setTexto] = useState('')
  const [enviando, setEnviando] = useState(false)

  const enviar = async (e) => {
    e.preventDefault()
    if (!texto.trim()) return
    setEnviando(true)
    try { await onAdd(texto); setTexto('') }
    finally { setEnviando(false) }
  }

  return (
    <div className="rev-modal-backdrop" onClick={onClose}>
      <div className="rev-modal" onClick={e => e.stopPropagation()}>
        <div className="rev-modal-head">
          <div>
            <div className="rev-modal-label">{dispositivo.label}</div>
            <div className="rev-modal-trecho">{dispositivo.trecho}</div>
          </div>
          <button className="rev-modal-x" onClick={onClose} aria-label="Fechar"><X size={18} /></button>
        </div>

        <div className="rev-modal-list">
          {suggestions.length === 0 && (
            <p className="rev-modal-vazio">Ainda não há sugestões para este dispositivo. Seja o primeiro.</p>
          )}
          {suggestions.map(s => {
            const curtiu = (s.curtidoPor ?? []).includes(user.uid)
            const podeExcluir = s.autorUid === user.uid || user.role === 'admin'
            return (
              <div key={s.id} className="rev-sug">
                <div className="rev-sug-meta">
                  <span className="rev-sug-autor">{s.autorNome}</span>
                  <span className="rev-sug-data">{formataData(s.criadoEm)}</span>
                </div>
                <div className="rev-sug-texto">{s.texto}</div>
                <div className="rev-sug-acoes">
                  <button className={`rev-like${curtiu ? ' on' : ''}`} onClick={() => onToggleLike(s)}>
                    <ThumbsUp size={14} /> {(s.curtidoPor ?? []).length || ''}
                  </button>
                  {podeExcluir && (
                    <button className="rev-del" onClick={() => onDelete(s)} title="Excluir">
                      <Trash2 size={14} />
                    </button>
                  )}
                </div>
              </div>
            )
          })}
        </div>

        <form className="rev-modal-form" onSubmit={enviar}>
          <textarea className="rev-modal-input" value={texto} onChange={e => setTexto(e.target.value)}
            placeholder="Escreva sua sugestão para este dispositivo…" rows={3} />
          <button className="rev-modal-enviar" type="submit" disabled={enviando || !texto.trim()}>
            {enviando ? 'Enviando…' : 'Enviar sugestão'}
          </button>
        </form>
      </div>
    </div>
  )
}
