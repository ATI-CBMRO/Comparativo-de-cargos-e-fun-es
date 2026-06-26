import { useState, useEffect } from 'react'
import { X, ThumbsUp, Trash2, Check, Ban } from 'lucide-react'

function formataData(criadoEm) {
  if (!criadoEm?.toDate) return ''
  return criadoEm.toDate().toLocaleString('pt-BR', {
    day: '2-digit', month: '2-digit', hour: '2-digit', minute: '2-digit',
  })
}

export default function RevisaoModal({
  dispositivo, suggestions, finalText, user,
  onAdd, onToggleLike, onDelete, onSetStatus, onSaveFinal, onClose,
}) {
  const isAdmin = user.role === 'admin'
  const [texto, setTexto] = useState('')
  const [enviando, setEnviando] = useState(false)
  const [final, setFinal] = useState(finalText?.texto ?? '')

  useEffect(() => { setFinal(finalText?.texto ?? '') }, [finalText, dispositivo.id])

  const enviar = async (e) => {
    e.preventDefault()
    if (!texto.trim()) return
    setEnviando(true)
    try { await onAdd(texto); setTexto('') }
    finally { setEnviando(false) }
  }

  const statusClasse = (s) => {
    const st = s.adminStatus ?? 'pendente'
    if (st === 'relevante') return ' rel'
    if (st === 'descartada') return ' desc'
    return ''
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
            <p className="rev-modal-vazio">Ainda não há sugestões para este dispositivo.</p>
          )}
          {suggestions.map(s => {
            const curtiu = (s.curtidoPor ?? []).includes(user.uid)
            const podeExcluir = s.autorUid === user.uid || isAdmin
            const st = s.adminStatus ?? 'pendente'
            return (
              <div key={s.id} className={`rev-sug${statusClasse(s)}`}>
                <div className="rev-sug-meta">
                  <span className="rev-sug-autor">{s.autorNome}</span>
                  <span className="rev-sug-data">{formataData(s.criadoEm)}</span>
                </div>
                <div className="rev-sug-texto">{s.texto}</div>
                <div className="rev-sug-acoes">
                  <button className={`rev-like${curtiu ? ' on' : ''}`} onClick={() => onToggleLike(s)}>
                    <ThumbsUp size={14} /> {(s.curtidoPor ?? []).length || ''}
                  </button>
                  {st !== 'pendente' && (
                    <span className={`rev-badge ${st}`}>{st === 'relevante' ? 'Relevante' : 'Descartada'}</span>
                  )}
                  {isAdmin && (
                    <span className="rev-admin-acoes">
                      <button className="rev-mini rel" title="Marcar relevante"
                        onClick={() => onSetStatus(s, st === 'relevante' ? 'pendente' : 'relevante')}><Check size={14} /></button>
                      <button className="rev-mini desc" title="Descartar"
                        onClick={() => onSetStatus(s, st === 'descartada' ? 'pendente' : 'descartada')}><Ban size={14} /></button>
                    </span>
                  )}
                  {podeExcluir && (
                    <button className="rev-del" onClick={() => onDelete(s)} title="Excluir"><Trash2 size={14} /></button>
                  )}
                </div>
              </div>
            )
          })}
        </div>

        {/* Texto final */}
        {(isAdmin || finalText) && (
          <div className="rev-final">
            <div className="rev-final-head">
              ✍️ Texto final do dispositivo
              {finalText?.status === 'fechado' && <span className="rev-badge fechado">✔ Fechado</span>}
            </div>
            {isAdmin ? (
              <>
                <textarea className="rev-modal-input" value={final} onChange={e => setFinal(e.target.value)}
                  placeholder="Escreva o texto final consolidado…" rows={3} />
                <div className="rev-final-acoes">
                  <button className="rev-final-btn" onClick={() => onSaveFinal(final, 'em_aberto')}>Salvar rascunho</button>
                  <button className="rev-final-btn fechar" onClick={() => onSaveFinal(final, 'fechado')}>Salvar e fechar</button>
                </div>
              </>
            ) : (
              <p className="rev-final-ro">{finalText.texto}</p>
            )}
          </div>
        )}

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
