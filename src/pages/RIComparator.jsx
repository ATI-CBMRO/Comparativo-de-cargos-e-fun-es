import { useEffect, useMemo, useState } from 'react'
import { articleLabel, romanize } from '../lib/minutaArticles.js'
import { buildTargets } from '../lib/minutaTargets.js'
import { indexComparativo, organKeyOfChapter, statesWithData, pickState } from '../lib/riComparison.js'
import ChapterRail from '../components/ChapterRail.jsx'

const EMPTY_COUNTS = {}

export default function RIComparator() {
  const [chapters, setChapters] = useState(null)
  const [compByKey, setCompByKey] = useState({})
  const [selectedChapterId, setSelectedChapterId] = useState(null)
  const [selectedStateId, setSelectedStateId] = useState(null)
  const [error, setError] = useState(null)

  // Carga inicial: minuta articulada + comparativo, em paralelo.
  useEffect(() => {
    let alive = true
    ;(async () => {
      try {
        const [rs, rc] = await Promise.all([
          fetch('/database/minuta_structure.json'),
          fetch('/database/comparativo_minuta.json'),
        ])
        if (!rs.ok || !rc.ok) throw new Error('fetch')
        const [structure, comparativo] = [await rs.json(), await rc.json()]
        if (!alive) return
        const chs = buildTargets(structure)
        setChapters(chs)
        setCompByKey(indexComparativo(comparativo))
        // Primeiro capítulo de órgão como padrão (fallback: primeiro capítulo).
        const firstOrgan = chs.find(c => organKeyOfChapter(c.chapterId))
        setSelectedChapterId((firstOrgan ?? chs[0])?.chapterId ?? null)
      } catch {
        if (alive) setError('Erro ao carregar os dados. Execute build_minuta_structure.py e build_minuta_comparison.py.')
      }
    })()
    return () => { alive = false }
  }, [])

  const chapter = chapters?.find(c => c.chapterId === selectedChapterId) ?? null
  const organKey = chapter ? organKeyOfChapter(chapter.chapterId) : null
  const organEntry = organKey ? compByKey[organKey] : null
  const available = useMemo(() => statesWithData(organEntry), [organEntry])

  // Estado efetivo derivado no render (sem effect): mantém o escolhido se ainda
  // tem dado no capítulo atual, senão cai no primeiro disponível.
  const activeStateId = pickState(selectedStateId, available)
  const stateEntry = available.find(s => s.id === activeStateId) ?? null

  if (error) {
    return (
      <>
        <div className="page-header"><div className="page-header-left"><h2 className="page-title">Comparativo de RI</h2></div></div>
        <div className="page-body" style={{ padding: 32 }}><p style={{ color: '#c8102e' }}>{error}</p></div>
      </>
    )
  }
  if (!chapters) {
    return (
      <>
        <div className="page-header"><div className="page-header-left"><h2 className="page-title">Comparativo de RI</h2></div></div>
        <div className="page-body" style={{ padding: 32 }}><p style={{ color: 'var(--text-muted)' }}>Carregando…</p></div>
      </>
    )
  }

  return (
    <>
      <div className="page-header">
        <div className="page-header-left">
          <h2 className="page-title">Comparativo de RI — Minuta CBMRO × demais estados</h2>
          <p className="page-subtitle">Selecione um capítulo e um estado para ver, lado a lado, o texto da minuta do CBMRO e as competências do órgão equivalente no Regimento Interno do estado.</p>
        </div>
      </div>
      <div className="page-body">
        <div className="rev-layout" style={{ display: 'flex', gap: 16, alignItems: 'flex-start' }}>
          <ChapterRail chapters={chapters} counts={EMPTY_COUNTS} selectedId={selectedChapterId} onSelect={setSelectedChapterId} />

          <div className="rev-doc" style={{ flex: 1.25, minWidth: 0 }}>
            {chapter && (
              <>
                <p className="rev-chapter" style={{ color: '#121d3d' }}>
                  CAPÍTULO {romanize(chapter.chapterNumber)} — {chapter.chapterTitle}
                </p>
                {chapter.articles.map(art => (
                  <div key={art.number} style={{ marginBottom: 10 }}>
                    {art.sectionTitle && (
                      <p className="rev-section">Seção {romanize(art.sectionNumber)} — {art.sectionTitle}</p>
                    )}
                    <p style={{ textAlign: 'justify', margin: '0 0 4px', textIndent: art.incisos.length ? 0 : '1.25em' }}>
                      <strong>{articleLabel(art.number)}</strong> {art.caput}
                    </p>
                    {art.incisos.map(inc => (
                      <p key={inc.index} style={{ textAlign: 'justify', margin: '2px 0 2px 1.25em' }}>
                        <strong>{romanize(inc.index + 1)} -</strong> {inc.text}
                      </p>
                    ))}
                  </div>
                ))}
              </>
            )}
          </div>

          <aside className="ri-state-col">
            <div style={{ fontWeight: 700, color: 'var(--text-muted)', textTransform: 'uppercase', fontSize: 11, marginBottom: 8 }}>
              Regimento Interno equivalente
            </div>
            {!organKey ? (
              <p style={{ color: 'var(--text-muted)', fontSize: 13 }}>Sem equivalente direto nos RIs analisados.</p>
            ) : available.length === 0 ? (
              <p style={{ color: 'var(--text-muted)', fontSize: 13 }}>Nenhum RI analisado trata deste órgão.</p>
            ) : (
              <>
                <div style={{ display: 'flex', flexWrap: 'wrap', gap: 6, marginBottom: 12 }}>
                  {available.map(s => {
                    const on = s.id === activeStateId
                    return (
                      <button key={s.id} onClick={() => setSelectedStateId(s.id)} style={{
                        font: '700 11px Inter, sans-serif', padding: '4px 9px', borderRadius: 20, cursor: 'pointer',
                        border: on ? '1px solid #c8102e' : '1px solid var(--border-card)',
                        background: on ? '#c8102e' : '#fff', color: on ? '#fff' : '#444',
                      }}>{s.abbr}</button>
                    )
                  })}
                </div>
                {stateEntry ? (
                  <div>
                    {(stateEntry.riOrgans ?? []).map((o, i) => (
                      <div key={i} style={{ marginBottom: 12 }}>
                        <p style={{ fontWeight: 700, fontSize: 13, color: '#121d3d', margin: '0 0 4px' }}>
                          {o.name}{o.abbreviation ? ` (${o.abbreviation})` : ''}
                        </p>
                        {(o.atribuicoes ?? []).map((a, j) => (
                          <p key={j} style={{ fontSize: 12.5, textAlign: 'justify', margin: '0 0 5px', color: '#333' }}>• {a}</p>
                        ))}
                      </div>
                    ))}
                    <div style={{ marginTop: 10, paddingTop: 8, borderTop: '1px solid var(--border-card)', fontSize: 11, color: 'var(--text-muted)' }}>
                      <span style={{
                        display: 'inline-block', padding: '1px 7px', borderRadius: 10, fontWeight: 700, fontSize: 10, marginRight: 6,
                        background: stateEntry.riProvenance === 'curado' ? '#e6f4ea' : '#fdeaea',
                        color: stateEntry.riProvenance === 'curado' ? '#1e7d40' : '#c8102e',
                      }}>{stateEntry.riProvenance === 'curado' ? 'curado (RI)' : 'automático (RI)'}</span>
                      {stateEntry.riSourceLabel}
                    </div>
                  </div>
                ) : (
                  <p style={{ color: 'var(--text-muted)', fontSize: 13 }}>Nenhum dado disponível para este órgão neste RI.</p>
                )}
              </>
            )}
          </aside>
        </div>
      </div>
    </>
  )
}
