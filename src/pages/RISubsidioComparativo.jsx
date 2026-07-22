// Subsídio do RI — visão UNIFICADA (Opção A). A navegação é o eixo: escolhe-se
// "Organização (capítulos)" OU "Órgãos (organograma)"; o painel do estado é
// sempre o mesmo — competências (camada só-RI, de comparativo_minuta) E redação
// (texto verbatim das alternativas, do minuta_structure). Estado controlado por
// cima (chapterId + stateAbbr) para o filtro valer entre as abas do Subsídio.
import { useEffect, useMemo, useState } from 'react'
import { fetchJson } from '../lib/dataCache.js'
import { LoadingState, ErrorState } from '../components/Status.jsx'
import { useScenario } from '../context/ScenarioContext'
import { scenarioDbUrl } from '../lib/scenario.js'
import { buildTargets, chapterIdOf } from '../lib/minutaTargets.js'
import { indexComparativo, organKeyOfChapter, statesWithData } from '../lib/riComparison.js'
import { buildArticles, articleLabel, romanize } from '../lib/minutaArticles.js'
import { renderFriendlyText, List } from '../lib/comparatorRender.jsx'
import ChapterRail from '../components/ChapterRail.jsx'
import { Scale, Network, ListTree } from 'lucide-react'

function MatchBadge({ match }) {
  const cfg = {
    exata: { cls: 'rg-badge-exata', label: 'exata' },
    parcial: { cls: 'rg-badge-parcial', label: 'parcial' },
    tematica: { cls: 'rg-badge-tematica', label: 'temática' },
  }[match] ?? { cls: 'rg-badge-tematica', label: match || '—' }
  return <span className={`rg-badge ${cfg.cls}`}>{cfg.label}</span>
}

// Árvore de órgãos da minuta (commandChart). Clicar seleciona o chapterId.
function OrgTreeNode({ node, depth, chapterId, setChapterId }) {
  const hasChildren = (node.children ?? []).length > 0
  const [open, setOpen] = useState(depth === 0)
  const clickable = Boolean(node.chapterId)
  return (
    <>
      <div className="oc-org-row" style={{ paddingLeft: depth * 14 }}>
        {hasChildren ? (
          <button type="button" className="oc-org-toggle" onClick={() => setOpen(v => !v)} aria-expanded={open} title={open ? 'Recolher' : `Expandir (${node.children.length})`}>
            {open ? '−' : '+'}
          </button>
        ) : <span className="oc-org-leaf" aria-hidden="true">└</span>}
        {clickable ? (
          <button type="button" onClick={() => setChapterId(node.chapterId)} className={`nav-item oc-org-select${node.chapterId === chapterId ? ' active' : ''}`} title={node.label}>
            {node.sigla || node.label}
          </button>
        ) : (
          <span className="nav-item oc-org-select" style={{ cursor: 'default', opacity: 0.65 }} title={node.label}>{node.sigla || node.label}</span>
        )}
      </div>
      {hasChildren && open && node.children.map((c, i) => (
        <OrgTreeNode key={c.organKey ?? `${node.organKey ?? 'root'}-s${i}`} node={c} depth={depth + 1} chapterId={chapterId} setChapterId={setChapterId} />
      ))}
    </>
  )
}

function RIArticle({ art }) {
  return (
    <div className="rg-article">
      <p className="rg-caput"><strong>{articleLabel(art.number)}</strong> {renderFriendlyText(art.caput)}</p>
      {art.incisos.length > 0 && (
        <ul className="cc-list rg-incisos">
          {art.incisos.map((inc, i) => <li key={i}>{inc.ownMarker ? '' : `${romanize(i + 1)} - `}{renderFriendlyText(inc.text)}</li>)}
        </ul>
      )}
      {(art.incisos[0]?.source || art.match) && (
        <div className="rg-article-foot">
          {art.incisos[0]?.source ? <span className="rg-source">{art.incisos[0].source}</span> : <span />}
          {art.match && <MatchBadge match={art.match} />}
        </div>
      )}
    </div>
  )
}

function AltExcerpt({ excerpt }) {
  return (
    <div className="rg-article">
      {excerpt.heading && <div className="rg-heading">{excerpt.heading}</div>}
      <p className="rg-caput">{renderFriendlyText(excerpt.caput)}</p>
      {excerpt.dispositivos?.length > 0 && <List items={excerpt.dispositivos} />}
      <div className="rg-article-foot">
        {excerpt.source ? <span className="rg-source">{excerpt.source}</span> : <span />}
        {excerpt.match && <MatchBadge match={excerpt.match} />}
      </div>
    </div>
  )
}

export default function RISubsidioComparativo({ chapterId, setChapterId, stateAbbr, setStateAbbr }) {
  const { cenario } = useScenario()
  const [structure, setStructure] = useState(null)
  const [comparativo, setComparativo] = useState(null)
  const [error, setError] = useState(false)
  const [navMode, setNavMode] = useState('org') // 'org' (capítulos) | 'orgaos'

  useEffect(() => {
    setStructure(null)
    setComparativo(null)
    Promise.all([
      fetchJson(scenarioDbUrl(cenario, 'minuta_structure.json')),
      fetchJson(scenarioDbUrl(cenario, 'comparativo_minuta.json')),
    ]).then(([s, c]) => {
      setStructure(s); setComparativo(c)
      if (!chapterId) setChapterId(s.commandChart?.chapterId ?? s.chapters?.[0]?.id ?? null)
    }).catch(() => setError(true))
  }, [cenario]) // eslint-disable-line react-hooks/exhaustive-deps

  const targets = useMemo(() => (structure ? buildTargets(structure) : []), [structure])
  const compByKey = useMemo(() => (comparativo ? indexComparativo(comparativo) : {}), [comparativo])
  const rawChapter = useMemo(() => structure?.chapters.find(c => c.id === chapterId) ?? null, [structure, chapterId])
  // Numeração CONTÍNUA da minuta: calcula os artigos da minuta inteira uma vez e
  // filtra só os do capítulo/órgão selecionado — sem reiniciar em Art. 1º.
  const allArticles = useMemo(() => (structure ? buildArticles(structure) : []), [structure])
  const articles = useMemo(() => allArticles.filter(a => chapterIdOf(a.editId) === chapterId), [allArticles, chapterId])

  const organKey = organKeyOfChapter(chapterId)
  const organEntry = organKey ? compByKey[organKey] : null
  const compStates = useMemo(() => statesWithData(organEntry), [organEntry])
  const altStates = useMemo(() => (
    rawChapter?.alternatives
      ? Object.entries(rawChapter.alternatives).map(([uf, alt]) => ({ uf, ...alt }))
      : []
  ), [rawChapter])

  // União dos estados que têm competências e/ou redação, por sigla.
  const ufs = useMemo(() => {
    const byAbbr = new Map()
    compStates.forEach(s => byAbbr.set(s.abbr, { abbr: s.abbr, comp: s, alt: null }))
    altStates.forEach(s => {
      const e = byAbbr.get(s.abbr) ?? { abbr: s.abbr, comp: null, alt: null }
      e.alt = s; byAbbr.set(s.abbr, e)
    })
    return [...byAbbr.values()].sort((a, b) => a.abbr.localeCompare(b.abbr, 'pt'))
  }, [compStates, altStates])

  const activeAbbr = ufs.some(u => u.abbr === stateAbbr) ? stateAbbr : (ufs[0]?.abbr ?? null)
  const active = ufs.find(u => u.abbr === activeAbbr) ?? null

  // Mantém a sigla compartilhada válida ao trocar de órgão.
  useEffect(() => {
    if (activeAbbr && activeAbbr !== stateAbbr) setStateAbbr(activeAbbr)
  }, [activeAbbr]) // eslint-disable-line react-hooks/exhaustive-deps

  if (error) return <ErrorState icon={Scale} title="Dados do subsídio não encontrados" hint={<>Execute <code>build_minuta_structure.py</code> e <code>build_minuta_comparison.py</code>.</>} />
  if (!structure || !comparativo) return <LoadingState label="" />

  return (
    <div className="page-body" style={{ paddingTop: 0 }}>
      <div className="subA-toolbar">
        <div className="subA-navpick">
          <span className="lbl">Navegar por:</span>
          <div className="subA-seg">
            <button className={navMode === 'org' ? 'on' : ''} onClick={() => setNavMode('org')}><ListTree size={14} /> Organização</button>
            <button className={navMode === 'orgaos' ? 'on' : ''} onClick={() => setNavMode('orgaos')}><Network size={14} /> Órgãos</button>
          </div>
        </div>
      </div>

      <div className="subA-layout">
        <aside className="subA-rail no-print">
          {navMode === 'org' ? (
            <ChapterRail chapters={targets} counts={{}} selectedId={chapterId} onSelect={setChapterId} />
          ) : (
            <div className="card" style={{ padding: 8 }}>
              <div className="nav-section-label" style={{ padding: '6px 6px 8px' }}>Órgãos da minuta</div>
              {structure.commandChart && (
                <OrgTreeNode node={structure.commandChart} depth={0} chapterId={chapterId} setChapterId={setChapterId} />
              )}
            </div>
          )}
        </aside>

        <div className="subA-mid">
          {rawChapter && (
            <>
              <p className="rev-chapter" style={{ color: 'var(--text-primary)' }}>{rawChapter.chapterTitle || rawChapter.title}</p>
              <div className="card rg-doc">
                {articles.length === 0 ? <p className="rg-empty">Nenhum artigo neste item.</p> : articles.map(a => <RIArticle key={a.number} art={a} />)}
              </div>
            </>
          )}
        </div>

        <aside className="subA-state">
          <div className="rg-col-head">
            {organKey ? `Regimento Interno de outros estados` : 'Regimento Interno equivalente'}
          </div>
          {cenario === 'atual' && (
            <p className="muted-note" style={{ margin: '4px 0 10px', fontStyle: 'italic' }}>
              Correspondência automática — sujeita a revisão.
            </p>
          )}

          {ufs.length === 0 ? (
            <p className="subA-miss" style={{ marginTop: 10 }}>Nenhum estado com RI cobre este item.</p>
          ) : (
            <>
              <div className="oc-state-chips" style={{ position: 'static', padding: '10px 0' }}>
                <span className="oc-state-chips-label">Estado:</span>
                {ufs.map(u => (
                  <button key={u.abbr} className={`oc-state-chip${u.abbr === activeAbbr ? ' active' : ''}`} onClick={() => setStateAbbr(u.abbr)}>{u.abbr}</button>
                ))}
              </div>

              {/* Uma seção só, o melhor disponível: prefere o TEXTO ORIGINAL (com
                  dispositivos); na falta dele, cai para as COMPETÊNCIAS (resumo). */}
              {active?.alt?.excerpts?.length ? (
                <>
                  <div className="subA-secttl"><span className="subA-pill red">Texto original</span> artigo completo, com os dispositivos</div>
                  <div className="rg-doc">{active.alt.excerpts.map((ex, i) => <AltExcerpt key={i} excerpt={ex} />)}</div>
                </>
              ) : active?.comp ? (
                <>
                  <div className="subA-secttl"><span className="subA-pill comp">Competências</span> resumo — texto integral ainda não extraído</div>
                  <div>
                    {(active.comp.riOrgans ?? []).map((o, i) => (
                      <div key={i} style={{ marginBottom: 12 }}>
                        <p className="subA-comp-org">{o.name}{o.abbreviation ? ` (${o.abbreviation})` : ''}</p>
                        {(o.atribuicoes ?? []).map((a, j) => <p key={j} className="subA-comp-atr">• {a}</p>)}
                      </div>
                    ))}
                    <div className="subA-provfoot">
                      <span className={`subA-prov ${active.comp.riProvenance === 'curado' ? 'curado' : 'auto'}`}>
                        {active.comp.riProvenance === 'curado' ? 'curado (RI)' : 'automático (RI)'}
                      </span>
                      {active.comp.riSourceLabel}
                    </div>
                  </div>
                </>
              ) : (
                <p className="subA-miss">Nenhum dado de {activeAbbr} para este item.</p>
              )}
            </>
          )}
        </aside>
      </div>
    </div>
  )
}
