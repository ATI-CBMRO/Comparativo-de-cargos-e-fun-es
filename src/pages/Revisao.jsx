import { useEffect, useMemo, useState } from 'react'
import { MessageSquare } from 'lucide-react'
import { useAuth } from '../lib/auth.jsx'
import { buildArticles, articleLabel, romanize } from '../lib/minutaArticles.js'
import { incisoDispositivoId, caputDispositivoId, parseDispositivoId } from '../lib/dispositivoId.js'
import { chapterIdOf } from '../lib/minutaTargets.js'
import {
  groupByDispositivo, countByDispositivo, countByChapter,
  filterSuggestionsByDoc, filterFinalsByDoc,
} from '../lib/reviewGroup.js'
import {
  subscribeSuggestions, addSuggestion, toggleLike, deleteSuggestion,
  setAdminStatus, subscribeFinalTexts, saveFinalText,
  subscribeRevisaoConfig, setRegulamentoAberto,
} from '../lib/reviewData.js'
import { gerarProposta } from '../lib/gerarProposta.js'
import RevisaoModal from '../components/RevisaoModal.jsx'
import RevisaoChapterRail from '../components/RevisaoChapterRail.jsx'
import { fetchJson } from '../lib/dataCache.js'
import { LoadingState, ErrorState, EmptyState } from '../components/Status.jsx'

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
  const [docId, setDocId] = useState('ri') // 'ri' | 'reg'
  const [data, setData] = useState(null)
  const [erro, setErro] = useState(null)
  const [suggestions, setSuggestions] = useState([])
  const [aberto, setAberto] = useState(null) // { id, label, trecho }
  const [regulamentoAberto, setRegulamentoAbertoState] = useState(false)

  useEffect(() => {
    setData(null)
    setErro(null)
    setAberto(null) // fecha a modal ao trocar de documento — evita comentar no doc errado
    const url = docId === 'reg' ? '/database/regulamento_structure.json' : '/database/minuta_structure.json'
    fetchJson(url)
      .then(setData)
      .catch(() => setErro('Não foi possível carregar o documento.'))
  }, [docId])

  // Ausência do doc config/revisao == fechado (fail-closed) — ver reviewData.js.
  useEffect(() => subscribeRevisaoConfig(
    (cfg) => setRegulamentoAbertoState(cfg.regulamentoAberto === true),
    (e) => console.error('Erro na config da revisão:', e),
  ), [])

  // subscribeSuggestions retorna o unsubscribe do onSnapshot — cleanup correto do efeito.
  useEffect(() => subscribeSuggestions(
    setSuggestions,
    (e) => console.error('Erro na assinatura de sugestões:', e),
  ), [])

  const [finals, setFinals] = useState(new Map())
  // Idem: subscribeFinalTexts também retorna o unsubscribe do onSnapshot.
  useEffect(() => subscribeFinalTexts(setFinals, (e) => console.error('Erro finalTexts:', e)), [])

  const finalsForDoc = useMemo(() => filterFinalsByDoc(finals, docId), [finals, docId])

  const suggestionsForDoc = useMemo(() => filterSuggestionsByDoc(suggestions, docId), [suggestions, docId])
  const counts = useMemo(() => countByDispositivo(suggestionsForDoc), [suggestionsForDoc])
  const grupos = useMemo(() => groupByDispositivo(suggestionsForDoc), [suggestionsForDoc])
  const articles = useMemo(() => (data ? buildArticles(data) : []), [data])
  const fechados = useMemo(() => {
    let n = 0
    finalsForDoc.forEach(f => { if (f.status === 'fechado') n += 1 })
    return n
  }, [finalsForDoc])

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
    () => countByChapter(suggestionsForDoc, finalsForDoc, parseDispositivoId, chapterIdOf),
    [suggestionsForDoc, finalsForDoc],
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

  const bloqueadoParaComissao = docId === 'reg' && !regulamentoAberto && user.role !== 'admin'
  const tituloDoc = docId === 'reg' ? 'Revisão do Regulamento' : 'Revisão da Minuta'

  if (erro) return <ErrorState title="Erro ao carregar" hint={erro} />
  if (!data) return <LoadingState label="Carregando…" />

  return (
    <>
      <div className="page-header">
        <div className="page-header-left">
          <h2 className="page-title">{tituloDoc}</h2>
          {!bloqueadoParaComissao && (
            <>
              <p className="page-subtitle">
                Clique no balão à direita de cada dispositivo para ver e enviar sugestões.
                As sugestões de todos ficam visíveis.
              </p>
              <p className="rev-progresso">{fechados} dispositivo(s) com texto final fechado.</p>
            </>
          )}
          <div className="rev-doc-switch">
            <button
              type="button"
              className={`oc-state-chip${docId === 'ri' ? ' active' : ''}`}
              onClick={() => setDocId('ri')}
            >
              Minuta do Regimento Interno
            </button>
            <button
              type="button"
              className={`oc-state-chip${docId === 'reg' ? ' active' : ''}`}
              onClick={() => setDocId('reg')}
            >
              Minuta do Regulamento Geral
            </button>
          </div>
          {user.role === 'admin' && docId === 'reg' && (
            <button
              type="button"
              className="btn btn-ghost rev-doc-toggle"
              onClick={() => setRegulamentoAberto(!regulamentoAberto)}
            >
              {regulamentoAberto
                ? 'Comissão PODE comentar o Regulamento (clique para fechar)'
                : 'Comissão NÃO pode comentar o Regulamento ainda (clique para abrir)'}
            </button>
          )}
        </div>
      </div>

      <div className="page-body">
        {bloqueadoParaComissao ? (
          <EmptyState
            title="Regulamento em preparação"
            text="Este documento ainda não foi liberado para comentários. Volte em breve."
          />
        ) : (
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

                <div className={`rev-line${finalsForDoc.get(caputId)?.status === 'fechado' ? ' fechado' : ''}`}>
                  <span className="rev-text" style={{ textIndent: art.incisos.length ? 0 : '1.25em' }}>
                    <strong>{articleLabel(art.number)}</strong> {art.caput}
                  </span>
                  <Rail count={counts.get(caputId)} onClick={() => abrir(caputId, caputLabel, art.caput)} />
                </div>

                {art.incisos.map((inc, i) => {
                  const id = incisoDispositivoId(inc.editId, inc.index)
                  const label = inc.ownMarker
                    ? `${articleLabel(art.number)}, parágrafo`
                    : `${articleLabel(art.number)}, inciso ${romanize(i + 1)}`
                  return (
                    <div className={`rev-line rev-inciso${finalsForDoc.get(id)?.status === 'fechado' ? ' fechado' : ''}`} key={`${id}`}>
                      <span className="rev-text">{inc.ownMarker ? '' : <strong>{romanize(i + 1)} -</strong>} {inc.text}</span>
                      <Rail count={counts.get(id)} onClick={() => abrir(id, label, inc.text)} />
                    </div>
                  )
                })}
              </div>
            )
          })}
          </div>
        </div>
        )}
      </div>

      {aberto && (
        <RevisaoModal
          dispositivo={aberto}
          suggestions={grupos.get(aberto.id) ?? []}
          finalText={finalsForDoc.get(aberto.id) ?? null}
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
