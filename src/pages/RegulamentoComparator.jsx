import { useState, useEffect, useMemo } from 'react'
import { Scale, FileDown, Search } from 'lucide-react'
import { fetchJson } from '../lib/dataCache.js'
import { LoadingState, ErrorState } from '../components/Status.jsx'
import { renderFriendlyText, List } from '../lib/comparatorRender.jsx'
import { buildArticles, articleLabel, romanize } from '../lib/minutaArticles.js'
import { chapterIdOf } from '../lib/minutaTargets.js'
import { PARTE_HEADERS } from '../lib/regulamentoPartes.js'
import { filtrarEstruturaPorEscopo } from '../lib/escopoServico.js'
import { useScenario } from '../context/ScenarioContext'
import { scenarioDbUrl } from '../lib/scenario.js'

function MatchBadge({ match }) {
  const cfg = {
    exata: { cls: 'rg-badge-exata', label: 'exata' },
    parcial: { cls: 'rg-badge-parcial', label: 'parcial' },
    tematica: { cls: 'rg-badge-tematica', label: 'temática' },
  }[match] ?? { cls: 'rg-badge-tematica', label: match || '—' }
  return <span className={`rg-badge ${cfg.cls}`}>{cfg.label}</span>
}

// Agrupa capítulos em 2 níveis: Parte (Geral/Serviço) e, dentro dela, `group` temático —
// preservando a ordem de primeira aparição.
function groupChapters(chapters) {
  const porParte = new Map()
  for (const ch of chapters) {
    const parte = ch.parte ?? 'geral' // RI/estruturas antigas sem `parte` caem em 'geral' (no-op visual, já que hoje só o Regulamento usa este componente)
    if (!porParte.has(parte)) porParte.set(parte, { parte, label: PARTE_HEADERS[parte] ?? null, groups: [] })
    const bucket = porParte.get(parte)
    const name = ch.group || 'Outros'
    let g = bucket.groups.find(x => x.name === name)
    if (!g) { g = { name, chapters: [] }; bucket.groups.push(g) }
    g.chapters.push(ch)
  }
  // Ordem: geral antes de servico (mesma ordem já usada no JSON/Wizard).
  return [...porParte.values()].sort((a, b) => (a.parte === 'geral' ? 0 : 1) - (b.parte === 'geral' ? 0 : 1))
}

export default function RegulamentoComparator({ escopo } = {}) {
  const { cenario } = useScenario()
  const [data, setData] = useState(null)
  const [error, setError] = useState(false)
  const [chapterId, setChapterId] = useState(null)
  const [selectedUf, setSelectedUf] = useState(null)
  const [filter, setFilter] = useState('')

  useEffect(() => {
    setData(null)
    fetchJson(scenarioDbUrl(cenario, 'regulamento_structure.json'))
      .then(d => setData(d))
      .catch(() => setError(true))
  }, [cenario])

  // Recorte por escopo (participante restrito ao Regulamento de Serviço) — mesmo filtro
  // usado no documento principal (Revisao.jsx). Sem escopo, é no-op: devolve `data` intacto.
  const dataEscopo = useMemo(() => filtrarEstruturaPorEscopo(data, escopo), [data, escopo])

  // Seleciona o primeiro capítulo do recorte ao carregar/trocar de cenário, e também se
  // o capítulo atual não pertencer mais ao recorte (troca de escopo).
  useEffect(() => {
    if (!dataEscopo) return
    if (!chapterId || !dataEscopo.chapters.some(c => c.id === chapterId)) {
      setChapterId(dataEscopo.chapters[0]?.id ?? null)
    }
  }, [dataEscopo]) // eslint-disable-line react-hooks/exhaustive-deps

  const groups = useMemo(() => (dataEscopo ? groupChapters(dataEscopo.chapters) : []), [dataEscopo])
  const chapter = useMemo(() => dataEscopo?.chapters.find(c => c.id === chapterId) || null, [dataEscopo, chapterId])

  const filteredGroups = useMemo(() => {
    if (!filter.trim()) return groups
    const q = filter.trim().toLowerCase()
    return groups
      .map(p => ({
        ...p,
        groups: p.groups
          .map(g => ({ ...g, chapters: g.chapters.filter(c => c.chapterTitle.toLowerCase().includes(q)) }))
          .filter(g => g.chapters.length > 0),
      }))
      .filter(p => p.groups.length > 0)
  }, [groups, filter])

  // Artigos do capítulo com a numeração CONTÍNUA do documento (Parte I → Parte II),
  // igual ao Wizard: numera a estrutura inteira e filtra o capítulo — o "Art. 37"
  // exibido aqui é o mesmo "Art. 37" da minuta. Como buildArticles não propaga os
  // campos extras da folha (match/source/adapted), reanexamos por editId.
  const allArticles = useMemo(() => (dataEscopo ? buildArticles(dataEscopo) : []), [dataEscopo])
  const articles = useMemo(() => {
    if (!chapter) return []
    const metaPorEditId = new Map(
      (chapter.articles ?? []).map(l => [l.editId, { match: l.match, source: l.source, adapted: l.adapted }]),
    )
    // No cenário atual o marcador vive só no editId ("reg:atual:<tema>/..."), enquanto
    // o id do capítulo segue "reg:<tema>" — normaliza antes de comparar.
    const semMarcador = (id) => String(id).replace(/^reg:atual:/, 'reg:')
    return allArticles
      .filter(a => semMarcador(chapterIdOf(a.editId)) === semMarcador(chapter.id))
      .map(a => ({ ...a, ...(metaPorEditId.get(a.editId) ?? {}) }))
  }, [allArticles, chapter])

  // Estados disponíveis em alternatives, em ordem alfabética pelo nome.
  const altStates = useMemo(() => {
    if (!chapter?.alternatives) return []
    return Object.entries(chapter.alternatives)
      .map(([uf, alt]) => ({ uf, ...alt }))
      .sort((a, b) => a.name.localeCompare(b.name, 'pt'))
  }, [chapter])

  // Ao trocar de capítulo, garante um estado válido selecionado (primeiro disponível).
  useEffect(() => {
    if (!chapter) return
    const ufs = altStates.map(s => s.uf)
    if (!selectedUf || !ufs.includes(selectedUf)) {
      setSelectedUf(ufs[0] ?? null)
    }
  }, [chapter, altStates]) // eslint-disable-line react-hooks/exhaustive-deps

  const selectedAlt = altStates.find(s => s.uf === selectedUf) || null

  if (error) {
    return (
      <ErrorState
        icon={Scale}
        title="Minuta do Regulamento Geral não encontrada"
        hint={<>Execute o script que gera <code>database/regulamento_structure.json</code>.</>}
      />
    )
  }
  if (!data) return <LoadingState label="" />

  return (
    <>
      <div className="section-bar no-print">
        <div className="section-bar-label">Comparar Regulamento — CBMRO × demais estados</div>
        <span className="section-bar-badge"><Scale size={13} color="var(--cbm-red-700)" />{dataEscopo.chapters.length} capítulos</span>
      </div>

      <div className="page-body">
        <div className="card no-print" style={{ marginBottom: 16 }}>
          <p style={{ fontSize: 13, color: 'var(--text-secondary)', lineHeight: 1.6, margin: 0 }}>
            Compare, capítulo a capítulo, a <strong>minuta do Regulamento Geral do CBMRO</strong>
            (em construção, à esquerda) com os trechos equivalentes de outros estados
            (à direita). Escolha um capítulo no sumário e clique num estado para ver o texto
            <strong> original</strong> dele — os trechos de outros estados nunca são adaptados,
            é proposital.
          </p>
        </div>

        <div className="rg-layout" style={{ display: 'flex', gap: 16, alignItems: 'flex-start' }}>
          {/* Sumário de capítulos, agrupados */}
          <aside className="no-print rg-aside" style={{ flex: '0 0 250px', position: 'sticky', top: 'calc(var(--header-h) + 12px)', maxHeight: 'calc(100vh - var(--header-h) - 24px)', overflowY: 'auto' }}>
            <div className="card" style={{ padding: 8 }}>
              <div style={{ padding: '2px 6px 8px' }}>
                <div className="rg-search">
                  <Search size={13} className="rg-search-icon" />
                  <input
                    type="text"
                    value={filter}
                    onChange={e => setFilter(e.target.value)}
                    placeholder="Buscar capítulo…"
                    className="rg-search-input"
                  />
                </div>
              </div>
              {filteredGroups.map(p => (
                <div key={p.parte} style={{ marginBottom: 10 }}>
                  {p.label && (
                    <div style={{ fontWeight: 800, color: 'var(--cbm-red-700)', fontSize: 10.5, letterSpacing: 0.5, padding: '6px 6px 2px' }}>
                      {p.label}
                    </div>
                  )}
                  {p.groups.map(g => (
                    <div key={g.name} style={{ marginBottom: 6 }}>
                      <div className="nav-section-label" style={{ padding: '6px 6px 4px' }}>{g.name}</div>
                      {g.chapters.map(c => (
                        <button
                          key={c.id}
                          onClick={() => setChapterId(c.id)}
                          className={`nav-item rg-nav-item${c.id === chapterId ? ' active' : ''}`}
                          title={c.chapterTitle}
                        >
                          <span className="nav-item-label">{c.chapterTitle}</span>
                        </button>
                      ))}
                    </div>
                  ))}
                </div>
              ))}
              {filteredGroups.every(p => p.groups.length === 0) && (
                <div style={{ padding: 12, fontSize: 12.5, color: 'var(--text-muted)', textAlign: 'center' }}>Nenhum capítulo encontrado.</div>
              )}
            </div>
          </aside>

          {/* Conteúdo do capítulo */}
          <div style={{ flex: 1, minWidth: 0 }}>
            {chapter && (
              <>
                <div className="oc-toolbar no-print" style={{ marginBottom: 12, justifyContent: 'space-between' }}>
                  <div className="oc-toolbar-info">
                    <span>{chapter.chapterTitle}</span>
                    {chapter.primary && (
                      <span className="rg-primary-chip">Fonte primária: {chapter.primary.name} — {chapter.primary.docLabel}</span>
                    )}
                  </div>
                  <button className="btn btn-ghost" onClick={() => window.print()}>
                    <FileDown size={15} /> Imprimir
                  </button>
                </div>

                <div className="print-only-title" style={{ display: 'none' }}>
                  {chapter.chapterTitle}{selectedAlt ? ` — CBMRO × ${selectedAlt.abbr} (${selectedAlt.name})` : ''}
                </div>

                <div className="rg-columns" style={{ display: 'flex', gap: 16, alignItems: 'flex-start' }}>
                  {/* Coluna esquerda: minuta CBMRO */}
                  <div className="rg-col" style={{ flex: 1, minWidth: 0 }}>
                    <div className="rg-col-head">CBMRO — minuta (em construção)</div>
                    <div className="card rg-doc">
                      {articles.length === 0
                        ? <p className="rg-empty">Nenhum artigo neste capítulo.</p>
                        : articles.map(art => <RegArticle key={art.number} art={art} />)}
                    </div>
                  </div>

                  {/* Coluna direita: alternativas de outros estados */}
                  <div className="rg-col no-print" style={{ flex: 1, minWidth: 0 }}>
                    <div className="rg-col-head">Outros estados — texto original</div>
                    {altStates.length === 0 ? (
                      <div className="card" style={{ padding: 24, textAlign: 'center', color: 'var(--text-muted)' }}>
                        Nenhuma alternativa disponível para este capítulo.
                      </div>
                    ) : (
                      <>
                        <div className="oc-state-chips" style={{ position: 'static', padding: '0 0 10px' }}>
                          <span className="oc-state-chips-label">Estado:</span>
                          {altStates.map(s => (
                            <button
                              key={s.uf}
                              className={`oc-state-chip${s.uf === selectedUf ? ' active' : ''}`}
                              onClick={() => setSelectedUf(s.uf)}
                              title={`${s.name} · ${s.docLabel}`}
                            >
                              {s.abbr}
                            </button>
                          ))}
                        </div>
                        <div className="card rg-doc">
                          {selectedAlt && selectedAlt.excerpts.length > 0
                            ? selectedAlt.excerpts.map((ex, i) => <AltExcerpt key={i} excerpt={ex} />)
                            : <p className="rg-empty">Sem trechos para este estado.</p>}
                        </div>
                      </>
                    )}
                  </div>

                  {/* Versão para impressão da coluna direita (mostra o estado selecionado) */}
                  {selectedAlt && (
                    <div className="rg-col rg-print-only" style={{ flex: 1, minWidth: 0, display: 'none' }}>
                      <div className="rg-col-head">{selectedAlt.name} — {selectedAlt.docLabel}</div>
                      <div className="card rg-doc">
                        {selectedAlt.excerpts.map((ex, i) => <AltExcerpt key={i} excerpt={ex} />)}
                      </div>
                    </div>
                  )}
                </div>
              </>
            )}
          </div>
        </div>
      </div>
    </>
  )
}

// Artigo da minuta CBMRO: caput + incisos + fonte + selo de match.
function RegArticle({ art }) {
  return (
    <div className="rg-article">
      <p className="rg-caput">
        <strong>{articleLabel(art.number)}</strong> {renderFriendlyText(art.caput)}
      </p>
      {art.incisos.length > 0 && (
        <ul className="cc-list rg-incisos">
          {art.incisos.map((inc, i) => (
            <li key={i}>{inc.ownMarker ? '' : `${romanize(i + 1)} - `}{renderFriendlyText(inc.text)}</li>
          ))}
        </ul>
      )}
      <div className="rg-article-foot">
        {art.incisos[0]?.source || art.source
          ? <span className="rg-source">{art.incisos[0]?.source || art.source}</span>
          : <span />}
        {art.match && <MatchBadge match={art.match} />}
      </div>
    </div>
  )
}

// Trecho de um estado alternativo (heading + caput + dispositivos + fonte + selo).
function AltExcerpt({ excerpt }) {
  return (
    <div className="rg-article">
      {excerpt.heading && <div className="rg-heading">{excerpt.heading}</div>}
      <p className="rg-caput">{renderFriendlyText(excerpt.caput)}</p>
      {excerpt.dispositivos && excerpt.dispositivos.length > 0 && (
        <List items={excerpt.dispositivos} />
      )}
      <div className="rg-article-foot">
        {excerpt.source ? <span className="rg-source">{excerpt.source}</span> : <span />}
        {excerpt.match && <MatchBadge match={excerpt.match} />}
      </div>
    </div>
  )
}
