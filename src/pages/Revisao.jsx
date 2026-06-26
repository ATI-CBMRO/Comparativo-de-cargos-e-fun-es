import { useEffect, useMemo, useState } from 'react'
import { MessageSquare } from 'lucide-react'
import { useAuth } from '../lib/auth.jsx'
import { buildArticles, articleLabel, romanize } from '../lib/minutaArticles.js'
import { incisoDispositivoId, caputDispositivoId } from '../lib/dispositivoId.js'
import { groupByDispositivo, countByDispositivo } from '../lib/reviewGroup.js'
import {
  subscribeSuggestions, addSuggestion, toggleLike, deleteSuggestion,
} from '../lib/reviewData.js'
import RevisaoModal from '../components/RevisaoModal.jsx'

function Rail({ count, onClick }) {
  return (
    <span className="rev-rail">
      <button type="button" className={`rev-mark${count ? ' has' : ''}`} onClick={onClick}
        title={count ? `${count} sugestão(ões)` : 'Comentar'}>
        {count ? count : <MessageSquare size={13} />}
      </button>
    </span>
  )
}

export default function Revisao() {
  const { user } = useAuth()
  const [data, setData] = useState(null)
  const [erro, setErro] = useState(null)
  const [suggestions, setSuggestions] = useState([])
  const [aberto, setAberto] = useState(null) // { id, label, trecho }

  useEffect(() => {
    fetch('/database/minuta_structure.json')
      .then(r => { if (!r.ok) throw new Error(r.status); return r.json() })
      .then(setData)
      .catch(() => setErro('Não foi possível carregar a minuta.'))
  }, [])

  useEffect(() => subscribeSuggestions(setSuggestions), [])

  const counts = useMemo(() => countByDispositivo(suggestions), [suggestions])
  const grupos = useMemo(() => groupByDispositivo(suggestions), [suggestions])
  const articles = useMemo(() => (data ? buildArticles(data) : []), [data])

  const abrir = (id, label, trecho) => setAberto({ id, label, trecho })

  const handleAdd = (texto) => addSuggestion({
    dispositivoId: aberto.id,
    dispositivoLabelSnapshot: aberto.label,
    trechoSnapshot: aberto.trecho,
    texto,
    autor: { uid: user.uid, nome: user.nome },
  })

  if (erro) return <div style={{ padding: 32, color: '#c8102e' }}>{erro}</div>
  if (!data) return <div style={{ padding: 32 }}>Carregando minuta…</div>

  return (
    <>
      <div className="page-header">
        <div className="page-header-left">
          <h2 className="page-title">Revisão da Minuta</h2>
          <p className="page-subtitle">
            Clique no balão à direita de cada dispositivo para ver e enviar sugestões.
            As sugestões de todos ficam visíveis.
          </p>
        </div>
      </div>

      <div className="page-body">
        <div className="rev-doc">
          {articles.map(art => {
            const caputId = caputDispositivoId(art.editId)
            const caputLabel = `${articleLabel(art.number)}`
            return (
              <div key={art.number} className="rev-art">
                {art.chapterTitle && (
                  <p className="rev-chapter">CAPÍTULO {romanize(art.chapterNumber)}<br />{art.chapterTitle}</p>
                )}
                {art.sectionTitle && (
                  <p className="rev-section">Seção {romanize(art.sectionNumber)} — {art.sectionTitle}</p>
                )}

                <div className="rev-line">
                  <span className="rev-text" style={{ textIndent: art.incisos.length ? 0 : '1.25em' }}>
                    <strong>{articleLabel(art.number)}</strong> {art.caput}
                  </span>
                  <Rail count={counts.get(caputId)} onClick={() => abrir(caputId, caputLabel, art.caput)} />
                </div>

                {art.incisos.map((inc, i) => {
                  const id = incisoDispositivoId(inc.editId, inc.index)
                  const label = `${articleLabel(art.number)}, inciso ${romanize(i + 1)}`
                  return (
                    <div className="rev-line rev-inciso" key={`${id}`}>
                      <span className="rev-text"><strong>{romanize(i + 1)} -</strong> {inc.text}</span>
                      <Rail count={counts.get(id)} onClick={() => abrir(id, label, inc.text)} />
                    </div>
                  )
                })}
              </div>
            )
          })}
        </div>
      </div>

      {aberto && (
        <RevisaoModal
          dispositivo={aberto}
          suggestions={grupos.get(aberto.id) ?? []}
          user={user}
          onAdd={handleAdd}
          onToggleLike={(s) => toggleLike(s, user.uid)}
          onDelete={(s) => deleteSuggestion(s.id)}
          onClose={() => setAberto(null)}
        />
      )}
    </>
  )
}
