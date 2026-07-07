import { useEffect, useMemo, useState } from 'react'
import { MessageSquare } from 'lucide-react'
import { useAuth } from '../lib/auth.jsx'
import { buildArticles, articleLabel, romanize } from '../lib/minutaArticles.js'
import { incisoDispositivoId, caputDispositivoId, parseDispositivoId } from '../lib/dispositivoId.js'
import { chapterIdOf } from '../lib/minutaTargets.js'
import { groupByDispositivo, countByDispositivo, countByChapter } from '../lib/reviewGroup.js'
import {
  subscribeSuggestions, addSuggestion, toggleLike, deleteSuggestion,
  setAdminStatus, subscribeFinalTexts, saveFinalText,
} from '../lib/reviewData.js'
import { gerarProposta } from '../lib/gerarProposta.js'
import RevisaoModal from '../components/RevisaoModal.jsx'
import RevisaoChapterRail from '../components/RevisaoChapterRail.jsx'
import { fetchJson } from '../lib/dataCache.js'
import { LoadingState, ErrorState } from '../components/Status.jsx'

const chapterAnchorId = (chapterId) => `rc-cap-${chapterId}`

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
    fetchJson('/database/minuta_structure.json')
      .then(setData)
      .catch(() => setErro('Não foi possível carregar a minuta.'))
  }, [])

  // subscribeSuggestions retorna o unsubscribe do onSnapshot — cleanup correto do efeito.
  useEffect(() => subscribeSuggestions(
    setSuggestions,
    (e) => console.error('Erro na assinatura de sugestões:', e),
  ), [])

  const [finals, setFinals] = useState(new Map())
  // Idem: subscribeFinalTexts também retorna o unsubscribe do onSnapshot.
  useEffect(() => subscribeFinalTexts(setFinals, (e) => console.error('Erro finalTexts:', e)), [])

  const counts = useMemo(() => countByDispositivo(suggestions), [suggestions])
  const grupos = useMemo(() => groupByDispositivo(suggestions), [suggestions])
  const articles = useMemo(() => (data ? buildArticles(data) : []), [data])
  const fechados = useMemo(() => {
    let n = 0
    finals.forEach(f => { if (f.status === 'fechado') n += 1 })
    return n
  }, [finals])

  // Sumário de capítulos (a partir dos mesmos `articles`, sem recomputar buildArticles).
  const chapters = useMemo(() => {
    const list = []
    for (const a of articles) {
      if (a.chapterNumber) list.push({ chapterId: chapterIdOf(a.editId), chapterTitle: a.chapterTitle })
    }
    return list
  }, [articles])

  // Sugestões por capítulo, separadas em abertas × resolvidas (pelo status do texto final).
  const chapterCounts = useMemo(
    () => countByChapter(suggestions, finals, parseDispositivoId, chapterIdOf),
    [suggestions, finals],
  )

  const [activeChapterId, setActiveChapterId] = useState(null)

  // Destaca no sumário o capítulo visível enquanto o documento rola.
  useEffect(() => {
    if (!chapters.length) return
    const alvos = chapters
      .map(c => ({ id: c.chapterId, el: document.getElementById(chapterAnchorId(c.chapterId)) }))
      .filter(x => x.el)
    if (!alvos.length) return
    const observer = new IntersectionObserver(
      (entries) => {
        const visiveis = entries.filter(e => e.isIntersecting)
        if (!visiveis.length) return
        const topo = visiveis.reduce((a, b) => (a.boundingClientRect.top < b.boundingClientRect.top ? a : b))
        const achado = alvos.find(x => x.el === topo.target)
        if (achado) setActiveChapterId(achado.id)
      },
      { rootMargin: '-96px 0px -70% 0px', threshold: 0 },
    )
    alvos.forEach(x => observer.observe(x.el))
    return () => observer.disconnect()
  }, [chapters])

  const scrollToChapter = (chapterId) => {
    const el = document.getElementById(chapterAnchorId(chapterId))
    if (el) el.scrollIntoView({ behavior: 'smooth', block: 'start' })
  }

  const abrir = (id, label, trecho) => setAberto({ id, label, trecho })

  const handleAdd = (texto) => addSuggestion({
    dispositivoId: aberto.id,
    dispositivoLabelSnapshot: aberto.label,
    trechoSnapshot: aberto.trecho,
    texto,
    autor: { uid: user.uid, nome: user.nome },
  })

  if (erro) return <ErrorState title="Erro ao carregar" hint={erro} />
  if (!data) return <LoadingState label="Carregando minuta…" />

  return (
    <>
      <div className="page-header">
        <div className="page-header-left">
          <h2 className="page-title">Revisão da Minuta</h2>
          <p className="page-subtitle">
            Clique no balão à direita de cada dispositivo para ver e enviar sugestões.
            As sugestões de todos ficam visíveis.
          </p>
          <p className="rev-progresso">{fechados} dispositivo(s) com texto final fechado.</p>
        </div>
      </div>

      <div className="page-body">
        <div className="rc-layout">
          <RevisaoChapterRail
            chapters={chapters}
            counts={chapterCounts}
            activeChapterId={activeChapterId}
            onSelect={scrollToChapter}
          />
          <div className="rev-doc">
          {articles.map(art => {
            const caputId = caputDispositivoId(art.editId)
            const caputLabel = `${articleLabel(art.number)}`
            return (
              <div key={art.number} className="rev-art">
                {art.chapterTitle && (
                  <p
                    className="rev-chapter"
                    id={chapterAnchorId(chapterIdOf(art.editId))}
                    style={{ scrollMarginTop: 'calc(var(--header-h) + 12px)' }}
                  >
                    CAPÍTULO {romanize(art.chapterNumber)}<br />{art.chapterTitle}
                  </p>
                )}
                {art.sectionTitle && (
                  <p className="rev-section">Seção {romanize(art.sectionNumber)} — {art.sectionTitle}</p>
                )}

                <div className={`rev-line${finals.get(caputId)?.status === 'fechado' ? ' fechado' : ''}`}>
                  <span className="rev-text" style={{ textIndent: art.incisos.length ? 0 : '1.25em' }}>
                    <strong>{articleLabel(art.number)}</strong> {art.caput}
                  </span>
                  <Rail count={counts.get(caputId)} onClick={() => abrir(caputId, caputLabel, art.caput)} />
                </div>

                {art.incisos.map((inc, i) => {
                  const id = incisoDispositivoId(inc.editId, inc.index)
                  const label = `${articleLabel(art.number)}, inciso ${romanize(i + 1)}`
                  return (
                    <div className={`rev-line rev-inciso${finals.get(id)?.status === 'fechado' ? ' fechado' : ''}`} key={`${id}`}>
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
      </div>

      {aberto && (
        <RevisaoModal
          dispositivo={aberto}
          suggestions={grupos.get(aberto.id) ?? []}
          finalText={finals.get(aberto.id) ?? null}
          user={user}
          onAdd={handleAdd}
          onToggleLike={(s) => toggleLike(s, user.uid)}
          onDelete={(s) => deleteSuggestion(s.id)}
          onSetStatus={(s, status) => setAdminStatus(s.id, status)}
          onSaveFinal={(texto, status) => saveFinalText(aberto.id, { texto, status, autor: { uid: user.uid, nome: user.nome } })}
          onGerarProposta={({ textoAtual, sugestoes }) => gerarProposta({ textoAtual, sugestoesRelevantes: sugestoes })}
          onClose={() => setAberto(null)}
        />
      )}
    </>
  )
}
