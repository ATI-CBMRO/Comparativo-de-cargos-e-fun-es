import { useEffect, useMemo, useState } from 'react'
import { MessageSquare } from 'lucide-react'
import { useAuth } from '../lib/auth.jsx'
import { buildArticles, articleLabel, romanize } from '../lib/minutaArticles.js'
import { incisoDispositivoId, caputDispositivoId, parseDispositivoId } from '../lib/dispositivoId.js'
import { chapterIdOf } from '../lib/minutaTargets.js'
import {
  groupByDispositivo, countByDispositivo, countByChapter,
  filterSuggestionsByDoc, filterFinalsByDoc,
  filterSuggestionsByScenario, filterFinalsByScenario,
} from '../lib/reviewGroup.js'
import { useScenario } from '../context/ScenarioContext.jsx'
import { scenarioDbUrl } from '../lib/scenario.js'
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
import { PARTE_HEADERS, parteByChapterTitle } from '../lib/regulamentoPartes.js'
import AvisoSincronizacao from '../components/AvisoSincronizacao.jsx'
import { filtrarEstruturaPorEscopo, resumoForaDoEscopo } from '../lib/escopoServico.js'
import NotaEscopoServico from '../components/NotaEscopoServico.jsx'

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

export default function Revisao({ initialDoc, escopo } = {}) {
  const { user } = useAuth()
  const { cenario } = useScenario()
  // Quando a Revisão é aberta a partir da trilha (menu), o documento já vem
  // fixado (initialDoc) e o seletor RI×Regulamento é escondido.
  const [docId, setDocId] = useState(initialDoc || 'ri') // 'ri' | 'reg'
  const [data, setData] = useState(null)
  const [erro, setErro] = useState(null)
  const [suggestions, setSuggestions] = useState([])
  const [aberto, setAberto] = useState(null) // { id, label, trecho }
  const [regulamentoAberto, setRegulamentoAbertoState] = useState(false)

  // Recorte setorizado (spec 2026-08-13). `data` segue com o documento COMPLETO — é dela
  // que sai a contagem do que ficou de fora, para a nota de escopo. Sem escopo, é no-op.
  const dataEscopo = useMemo(() => filtrarEstruturaPorEscopo(data, escopo), [data, escopo])

  // editIds que existem na estrutura ATUAL (documento COMPLETO, não `dataEscopo`): um
  // artigo removido é removido em qualquer visão, mas um artigo só fora do recorte por
  // escopo/órgão continua existindo no documento e deve continuar contando na visão do
  // admin. Usado por `countByChapter` para não contar sugestões órfãs (Finding 3, revisão
  // final 2026-08-18) — sugestão sobre artigo removido não deve inflar o trilho de
  // capítulos, porque o leitor não consegue abrir o dispositivo.
  const editIdsValidos = useMemo(() => {
    if (!data) return undefined
    const s = new Set()
    for (const c of data.chapters ?? []) for (const a of c.articles ?? []) s.add(a.editId)
    return s
  }, [data])

  const alternativesAberto = useMemo(() => {
    if (!aberto || !dataEscopo) return {}
    const { editId } = parseDispositivoId(aberto.id)
    const chapterId = chapterIdOf(editId)
    const chapter = dataEscopo.chapters.find(c => c.id === chapterId)
    return chapter?.alternatives ?? {}
  }, [aberto, dataEscopo])

  useEffect(() => {
    setData(null)
    setErro(null)
    setAberto(null) // fecha a modal ao trocar de documento — evita comentar no doc errado
    const file = docId === 'reg' ? 'regulamento_structure.json' : 'minuta_structure.json'
    fetchJson(scenarioDbUrl(cenario, file))
      .then(setData)
      .catch(() => setErro('Não foi possível carregar o documento.'))
  }, [docId, cenario])

  const [syncErro, setSyncErro] = useState(false)

  // Ausência do doc config/revisao == fechado (fail-closed) — ver reviewData.js.
  useEffect(() => subscribeRevisaoConfig(
    (cfg) => setRegulamentoAbertoState(cfg.regulamentoAberto === true),
    (e) => { console.error('Erro na config da revisão:', e); setSyncErro(true) },
  ), [])
  // subscribeSuggestions retorna o unsubscribe do onSnapshot — cleanup correto do efeito.
  useEffect(() => subscribeSuggestions(
    (v) => { setSuggestions(v); setSyncErro(false) },
    (e) => { console.error('Erro na assinatura de sugestões:', e); setSyncErro(true) },
  ), [])

  const [finals, setFinals] = useState(new Map())
  // Idem: subscribeFinalTexts também retorna o unsubscribe do onSnapshot.
  useEffect(() => subscribeFinalTexts(
    setFinals,
    (e) => { console.error('Erro finalTexts:', e); setSyncErro(true) },
  ), [])

  // Filtra por documento (RI×Regulamento) E por cenário (atual×futura) — os dois nunca
  // se misturam: comentários de um cenário jamais aparecem no outro.
  const finalsForDoc = useMemo(
    () => filterFinalsByScenario(filterFinalsByDoc(finals, docId), cenario),
    [finals, docId, cenario],
  )

  const suggestionsForDoc = useMemo(
    () => filterSuggestionsByScenario(filterSuggestionsByDoc(suggestions, docId), cenario),
    [suggestions, docId, cenario],
  )
  const counts = useMemo(() => countByDispositivo(suggestionsForDoc), [suggestionsForDoc])
  const grupos = useMemo(() => groupByDispositivo(suggestionsForDoc), [suggestionsForDoc])
  const articles = useMemo(() => (dataEscopo ? buildArticles(dataEscopo) : []), [dataEscopo])
  // No modo escopo o documento NÃO é dividido em Partes — é um documento único de
  // serviço. Mapa vazio faz as faixas "PARTE I/II" virarem no-op (regulamentoPartes.js).
  const parteDe = useMemo(
    () => (docId === 'reg' && !escopo ? parteByChapterTitle(dataEscopo) : {}),
    [docId, dataEscopo, escopo],
  )
  // Números da nota de escopo, calculados dos dados reais — nunca cravados no código.
  // Separa os dois tipos de corte: capítulos inteiros fora do recorte × artigos cortados
  // DENTRO de um capítulo que ficou (capítulo misto) — ver escopoServico.js.
  const foraDoEscopo = useMemo(() => {
    if (!escopo || !data) return null
    return resumoForaDoEscopo(data, dataEscopo, escopo)
  }, [escopo, data, dataEscopo])
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
    () => countByChapter(suggestionsForDoc, finalsForDoc, parseDispositivoId, chapterIdOf, editIdsValidos),
    [suggestionsForDoc, finalsForDoc, editIdsValidos],
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
  const tituloDoc = escopo === 'servico'
    ? 'Minuta do Regulamento de Serviço'
    : (docId === 'reg' ? 'Revisão do Regulamento' : 'Revisão da Minuta')

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
          {!initialDoc && (
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
          )}
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
        <AvisoSincronizacao visivel={syncErro} />
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
          {foraDoEscopo && (
            <NotaEscopoServico
              artigosNoEscopo={articles.length}
              artigosEmCapitulosFora={foraDoEscopo.artigosEmCapitulosFora}
              capitulosFora={foraDoEscopo.capitulosFora}
              artigosCortadosNoEscopo={foraDoEscopo.artigosCortadosNoEscopo}
            />
          )}
          {(() => {
            let ultimaParte = null
            return articles.map(art => {
            const caputId = caputDispositivoId(art.editId)
            const caputLabel = `${articleLabel(art.number)}`
            const parte = art.chapterTitle ? parteDe[art.chapterTitle] : null
            const faixa = parte && parte !== ultimaParte ? PARTE_HEADERS[parte] : null
            if (parte) ultimaParte = parte
            return (
              <div key={art.number} className="rev-art">
                {faixa && (
                  <div style={{
                    textAlign: 'center', fontWeight: 800, fontSize: 15, letterSpacing: 1,
                    color: 'var(--cbm-red-700)', borderTop: '2px solid var(--cbm-red-700)',
                    borderBottom: '2px solid var(--cbm-red-700)', padding: '8px 0', margin: '20px 0 12px',
                  }}>{faixa}</div>
                )}
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
            })
          })()}
          </div>
        </div>
        )}
      </div>

      {aberto && (
        <RevisaoModal
          dispositivo={aberto}
          alternatives={alternativesAberto}
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
