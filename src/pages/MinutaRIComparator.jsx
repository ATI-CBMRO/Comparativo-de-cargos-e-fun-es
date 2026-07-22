import { useState, useEffect, useMemo } from 'react'
import { Scale, FileDown } from 'lucide-react'
import { fetchJson } from '../lib/dataCache.js'
import { LoadingState, ErrorState, EmptyState } from '../components/Status.jsx'
import { renderFriendlyText, List } from '../lib/comparatorRender.jsx'
import { buildArticles, articleLabel, romanize } from '../lib/minutaArticles.js'
import { chapterIdOf } from '../lib/minutaTargets.js'

function MatchBadge({ match }) {
  const cfg = {
    exata: { cls: 'rg-badge-exata', label: 'exata' },
    parcial: { cls: 'rg-badge-parcial', label: 'parcial' },
    tematica: { cls: 'rg-badge-tematica', label: 'temática' },
  }[match] ?? { cls: 'rg-badge-tematica', label: match || '—' }
  return <span className={`rg-badge ${cfg.cls}`}>{cfg.label}</span>
}

// Nó da árvore de órgãos (commandChart já vem aninhado — organKey/sigla/label/
// chapterId/children). Espelha OrgTreeNode de MinutaComparator.jsx: botão −/+
// recolhe a subárvore; clicar no item seleciona o capítulo. Inicia recolhido (só
// o 1º nível visível), espelhando o organograma da minuta. Nós estruturais sem
// chapterId (ex.: Cia BM/Pel BM dentro do BBM) não são clicáveis.
function OrgTreeNode({ node, depth, chapterId, setChapterId, altCountByChapter }) {
  const hasChildren = (node.children ?? []).length > 0
  const [open, setOpen] = useState(false)
  const clickable = Boolean(node.chapterId)
  const count = node.chapterId ? (altCountByChapter.get(node.chapterId) ?? 0) : 0
  return (
    <>
      <div className="oc-org-row" style={{ paddingLeft: depth * 14 }}>
        {hasChildren ? (
          <button
            type="button"
            className="oc-org-toggle"
            onClick={() => setOpen(v => !v)}
            aria-expanded={open}
            aria-label={`${open ? 'Recolher' : 'Expandir'} ${node.sigla}`}
            title={open ? 'Recolher' : `Expandir (${node.children.length})`}
          >
            {open ? '−' : '+'}
          </button>
        ) : (
          <span className="oc-org-leaf" aria-hidden="true">└</span>
        )}
        {clickable ? (
          <button
            type="button"
            onClick={() => setChapterId(node.chapterId)}
            className={`nav-item oc-org-select${node.chapterId === chapterId ? ' active' : ''}`}
            title={node.label}
          >
            {node.sigla || node.label}<span className="oc-org-count">{count}</span>
          </button>
        ) : (
          <span className="nav-item oc-org-select" style={{ cursor: 'default', opacity: 0.65 }} title={node.label}>
            {node.sigla || node.label}
          </span>
        )}
      </div>
      {hasChildren && open && node.children.map((c, i) => (
        <OrgTreeNode
          key={c.organKey ?? `${node.organKey ?? 'root'}-struct-${i}`}
          node={c} depth={depth + 1} chapterId={chapterId} setChapterId={setChapterId}
          altCountByChapter={altCountByChapter}
        />
      ))}
    </>
  )
}

export default function MinutaRIComparator() {
  const [data, setData] = useState(null)
  const [error, setError] = useState(false)
  const [chapterId, setChapterId] = useState(null)
  const [selectedUf, setSelectedUf] = useState(null)

  useEffect(() => {
    fetchJson('/database/minuta_structure.json')
      .then(d => { setData(d); setChapterId(d.commandChart?.chapterId ?? null) })
      .catch(() => setError(true))
  }, [])

  const chapter = useMemo(
    () => data?.chapters.find(c => c.id === chapterId) || null,
    [data, chapterId],
  )

  // Quantidade de estados-alternativa por capítulo (organ), para o contador na
  // árvore de navegação — mesmo papel do o.states.length em MinutaComparator.jsx.
  const altCountByChapter = useMemo(() => {
    const m = new Map()
    if (data) {
      for (const c of data.chapters) {
        if (c.kind === 'organ') m.set(c.id, Object.keys(c.alternatives ?? {}).length)
      }
    }
    return m
  }, [data])

  // Artigos do capítulo com a numeração CONTÍNUA da minuta (decisão do Wândrio,
  // 22/07/2026, mesma regra do RegulamentoComparator): numera a estrutura inteira
  // e filtra o capítulo — o "Art. Nº" exibido é o mesmo do documento no Wizard.
  const allArticles = useMemo(() => (data ? buildArticles(data) : []), [data])
  const articles = useMemo(() => {
    if (!chapter) return []
    return allArticles.filter(a => chapterIdOf(a.editId) === chapter.id)
  }, [allArticles, chapter])

  // Estados disponíveis em alternatives, em ordem alfabética pelo nome.
  const altStates = useMemo(() => {
    if (!chapter?.alternatives) return []
    return Object.entries(chapter.alternatives)
      .map(([uf, alt]) => ({ uf, ...alt }))
      .sort((a, b) => a.name.localeCompare(b.name, 'pt'))
  }, [chapter])

  // Ao trocar de órgão, garante um estado válido selecionado (primeiro disponível).
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
        title="Minuta do Regimento Interno não encontrada"
        hint={<>Execute o script que gera <code>database/minuta_structure.json</code>.</>}
      />
    )
  }
  if (!data) return <LoadingState label="" />

  const totalOrganChapters = data.chapters.filter(c => c.kind === 'organ').length

  return (
    <>
      <div className="section-bar no-print">
        <div className="section-bar-label">Comparar Regimento Interno — CBMRO × demais estados</div>
        <span className="section-bar-badge"><Scale size={13} color="var(--cbm-red-700)" />{totalOrganChapters} órgãos</span>
      </div>

      <div className="page-body">
        <div className="card no-print" style={{ marginBottom: 16 }}>
          <p style={{ fontSize: 13, color: 'var(--text-secondary)', lineHeight: 1.6, margin: 0 }}>
            Compare, órgão a órgão, a <strong>minuta do Regimento Interno do CBMRO</strong>
            (em construção, à esquerda) com o <strong>artigo completo</strong> equivalente de
            outros estados (à direita) — sempre o dispositivo inteiro (caput e todos os
            incisos), não só o trecho já aproveitado na minuta. Escolha um órgão no sumário
            e clique num estado para ver o texto <strong>original</strong> dele — os trechos
            de outros estados nunca são adaptados, é proposital.
          </p>
        </div>

        <div className="rg-layout" style={{ display: 'flex', gap: 16, alignItems: 'flex-start' }}>
          {/* Sumário de órgãos (árvore pela cadeia de comando, igual ao Subsídio à Minuta) */}
          <aside className="no-print rg-aside" style={{ flex: '0 0 250px', position: 'sticky', top: 'calc(var(--header-h) + 12px)', maxHeight: 'calc(100vh - var(--header-h) - 24px)', overflowY: 'auto' }}>
            <div className="card" style={{ padding: 8 }}>
              <div className="nav-section-label" style={{ padding: '6px 6px 8px' }}>Órgãos da minuta</div>
              {data.commandChart && (
                <OrgTreeNode
                  node={data.commandChart} depth={0}
                  chapterId={chapterId} setChapterId={setChapterId}
                  altCountByChapter={altCountByChapter}
                />
              )}
            </div>
          </aside>

          {/* Conteúdo do órgão */}
          <div style={{ flex: 1, minWidth: 0 }}>
            {chapter && (
              <>
                <div className="oc-toolbar no-print" style={{ marginBottom: 12, justifyContent: 'space-between' }}>
                  <div className="oc-toolbar-info">
                    <span>{chapter.chapterTitle}</span>
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
                        ? <p className="rg-empty">Nenhum artigo neste órgão.</p>
                        : articles.map(art => <RIArticle key={art.number} art={art} />)}
                    </div>
                  </div>

                  {/* Coluna direita: alternativas de outros estados */}
                  <div className="rg-col no-print" style={{ flex: 1, minWidth: 0 }}>
                    <div className="rg-col-head">Outros estados — Regimento Interno (texto original)</div>
                    {altStates.length === 0 ? (
                      <EmptyState
                        icon={Scale}
                        title="Sem correspondência mapeada"
                        text="Nenhum estado com Regimento Interno já curado cobre este órgão ainda."
                      />
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

// Artigo da minuta CBMRO: caput + incisos + fonte + selo de match (quando o
// leaf.kind='incisos' carregar match/source diretamente — mesmo formato usado
// pelo Regulamento; na minuta do RI a maioria dos incisos traz o source por item).
function RIArticle({ art }) {
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
      {(art.incisos[0]?.source || art.match) && (
        <div className="rg-article-foot">
          {art.incisos[0]?.source
            ? <span className="rg-source">{art.incisos[0].source}</span>
            : <span />}
          {art.match && <MatchBadge match={art.match} />}
        </div>
      )}
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
