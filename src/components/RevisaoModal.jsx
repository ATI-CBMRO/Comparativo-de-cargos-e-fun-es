import { useState, useEffect } from 'react'

function formataData(criadoEm) {
  if (!criadoEm?.toDate) return ''
  return criadoEm.toDate().toLocaleString('pt-BR', {
    day: '2-digit', month: '2-digit', hour: '2-digit', minute: '2-digit',
  })
}

export default function RevisaoModal({
  dispositivo, suggestions, finalText, user,
  onAdd, onToggleLike, onDelete, onSetStatus, onSaveFinal, onGerarProposta, onClose,
}) {
  const isAdmin = user.role === 'admin'
  const [texto, setTexto] = useState('')
  const [enviando, setEnviando] = useState(false)
  const [final, setFinal] = useState(finalText?.texto ?? '')
  const [propostaIA, setPropostaIA] = useState(null)
  const [gerando, setGerando] = useState(false)
  const [erroIA, setErroIA] = useState('')

  useEffect(() => { setFinal(finalText?.texto ?? '') }, [finalText, dispositivo.id])

  const enviar = async (e) => {
    e.preventDefault()
    if (!texto.trim()) return
    setEnviando(true)
    try { await onAdd(texto); setTexto('') }
    finally { setEnviando(false) }
  }

  const relevantes = suggestions.filter(s => (s.adminStatus ?? 'pendente') === 'relevante')

  const gerar = async () => {
    setErroIA(''); setGerando(true)
    try {
      const proposta = await onGerarProposta({
        textoAtual: dispositivo.trecho,
        sugestoes: relevantes.map(s => s.texto),
      })
      setPropostaIA(proposta)
      setFinal(proposta)
    } catch (e) {
      setErroIA(e.message || 'Não foi possível gerar agora. Tente de novo.')
    } finally {
      setGerando(false)
    }
  }

  return (
    <div className="rev-modal-backdrop" onClick={onClose}>
      <div className="rev-modal" onClick={e => e.stopPropagation()}>
        {/* Cabeçalho: texto em discussão em destaque */}
        <div className="rev-mhead">
          <div style={{ flex: 1, minWidth: 0 }}>
            <div className="rev-mhead-lbl">● Em discussão</div>
            <div className="rev-mhead-ref">{dispositivo.label}</div>
            <div className="rev-discussao">{dispositivo.trecho}</div>
          </div>
          <button className="rev-modal-x" onClick={onClose} aria-label="Fechar">✕</button>
        </div>

        <div className="rev-cols">
          {/* Coluna esquerda: sugestões */}
          <div className="rev-col">
            <div className="rev-col-title">Sugestões ({suggestions.length})</div>
            {suggestions.length === 0 && (
              <p className="rev-col-vazio">Ainda não há sugestões para este dispositivo.</p>
            )}
            {suggestions.map(s => {
              const curtiu = (s.curtidoPor ?? []).includes(user.uid)
              const podeExcluir = s.autorUid === user.uid || isAdmin
              const st = s.adminStatus ?? 'pendente'
              return (
                <div key={s.id} className={`rev-sug${st === 'relevante' ? ' rel' : st === 'descartada' ? ' desc' : ''}`}>
                  <div className="rev-whorow">
                    <span className="rev-who">{s.autorNome}</span>
                    <span className="rev-when">{formataData(s.criadoEm)}</span>
                    <button className={`rev-ic count${curtiu ? ' on' : ''}`} onClick={() => onToggleLike(s)} title="Curtir">
                      👍 {(s.curtidoPor ?? []).length || ''}
                    </button>
                    {isAdmin && (
                      <>
                        <span className="rev-sep" />
                        <button className="rev-ic" onClick={() => onSetStatus(s, st === 'relevante' ? 'pendente' : 'relevante')} title="Marcar relevante">✅</button>
                        <button className="rev-ic" onClick={() => onSetStatus(s, st === 'descartada' ? 'pendente' : 'descartada')} title="Descartar">⛔</button>
                      </>
                    )}
                    {podeExcluir && (
                      <button className="rev-ic" onClick={() => onDelete(s)} title="Excluir">🗑️</button>
                    )}
                    {st !== 'pendente' && (
                      <span className={`rev-tag ${st === 'relevante' ? 'r' : 'd'}`}>{st === 'relevante' ? 'Relevante' : 'Descartada'}</span>
                    )}
                  </div>
                  <div className="rev-sug-texto">{s.texto}</div>
                </div>
              )
            })}

            <form className="rev-addbox" onSubmit={enviar}>
              <div className="rev-col-title">Sua sugestão</div>
              <textarea className="rev-editor" value={texto} onChange={e => setTexto(e.target.value)}
                placeholder="Escreva sua sugestão para este dispositivo…" rows={2} />
              <div className="rev-save">
                <button className="rev-btn r" type="submit" disabled={enviando || !texto.trim()}>
                  {enviando ? 'Enviando…' : 'Enviar sugestão'}
                </button>
              </div>
            </form>
          </div>

          {/* Coluna direita: redação final */}
          <div className="rev-col red">
            <div className="rev-col-title">
              Redação final
              {finalText?.status === 'fechado' && <span className="rev-fechado-selo">✔ Fechado</span>}
            </div>
            {isAdmin ? (
              <>
                <button className="rev-ia-btn" onClick={gerar} disabled={gerando || relevantes.length === 0}
                  title={relevantes.length === 0 ? 'Marque ao menos uma sugestão como relevante' : ''}>
                  {gerando ? 'Gerando…' : '✨ Gerar proposta com IA'}
                </button>
                {relevantes.length === 0 && (
                  <span className="rev-ia-dica">Marque ao menos uma sugestão como relevante para gerar.</span>
                )}
                {erroIA && <div className="login-erro" style={{ marginTop: 8 }}>{erroIA}</div>}
                {propostaIA && (
                  <div className="rev-ia-proposta">
                    <span className="label">✨ Proposta da IA (referência)</span>
                    {propostaIA}
                  </div>
                )}
                <div className="rev-col-title" style={{ marginTop: 14 }}>Texto final (editável)</div>
                <textarea className="rev-editor" value={final} onChange={e => setFinal(e.target.value)}
                  placeholder="Escreva o texto final consolidado…" rows={5} />
                <div className="rev-save">
                  <button className="rev-btn" onClick={() => onSaveFinal(final, 'em_aberto')}>Salvar rascunho</button>
                  <button className="rev-btn r" onClick={async () => { await onSaveFinal(final, 'fechado'); onClose() }}>Salvar e fechar</button>
                </div>
              </>
            ) : (
              finalText
                ? <p className="rev-final-ro">{finalText.texto}</p>
                : <p className="rev-col-vazio">Ainda não há texto final definido para este dispositivo.</p>
            )}
          </div>
        </div>
      </div>
    </div>
  )
}
