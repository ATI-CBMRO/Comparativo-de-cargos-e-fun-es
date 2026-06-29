import { useEffect, useState, useCallback } from 'react'
import { articleLabel, romanize } from '../lib/minutaArticles.js'
import { buildTargets } from '../lib/minutaTargets.js'
import { suggestionsStore as store } from '../lib/suggestionsStore.js'
import IdentityBar from '../components/IdentityBar.jsx'
import ChapterRail from '../components/ChapterRail.jsx'
import SuggestionPanel from '../components/SuggestionPanel.jsx'

const incisoKey = (editId, index) => `${editId}#${index}`

// Semeia 2 sugestões de exemplo no 1º inciso do 1º capítulo que tiver incisos.
async function seedExampleIfEmpty(chapters) {
  if ((await store.listSuggestions()).length > 0) return
  let target = null
  for (const c of chapters) {
    const art = c.articles.find(a => a.incisos.length > 0)
    if (art) { target = { chapterId: c.chapterId, editId: art.editId, inc: art.incisos[0] }; break }
  }
  if (!target) return
  await store.addSuggestion({
    chapterId: target.chapterId, targetId: target.editId, targetKind: 'inciso',
    incisoIndex: target.inc.index, type: 'editar',
    originalText: target.inc.text, proposedText: target.inc.text.replace(/[.;]\s*$/, '') + ' (texto revisado);',
    justification: 'Ajuste de redação para clareza.', authorId: 'u-lima',
  })
  await store.addSuggestion({
    chapterId: target.chapterId, targetId: target.editId, targetKind: 'inciso',
    incisoIndex: target.inc.index, type: 'remover',
    originalText: target.inc.text, justification: 'Conteúdo redundante.', authorId: 'u-souza',
  })
}

export default function MinutaRevisao() {
  const [chapters, setChapters] = useState(null)
  const [users, setUsers] = useState([])
  const [currentUser, setCurrentUser] = useState(null)
  const [counts, setCounts] = useState({})
  const [selectedChapterId, setSelectedChapterId] = useState(null)
  const [chapterSugs, setChapterSugs] = useState([])
  const [selectedTarget, setSelectedTarget] = useState(null)
  const [error, setError] = useState(null)

  // Carga inicial.
  useEffect(() => {
    let alive = true
    ;(async () => {
      try {
        const r = await fetch('/database/minuta_structure.json')
        if (!r.ok) throw new Error(r.status)
        const structure = await r.json()
        const chs = buildTargets(structure)
        await seedExampleIfEmpty(chs)
        const [us, cu, ct] = [await store.listUsers(), await store.getCurrentUser(), await store.getChapterCounts()]
        if (!alive) return
        setChapters(chs); setUsers(us); setCurrentUser(cu); setCounts(ct)
        setSelectedChapterId(chs.find(c => c.articles.some(a => a.incisos.length))?.chapterId ?? chs[0]?.chapterId ?? null)
      } catch {
        if (alive) setError('Erro ao carregar minuta_structure.json. Execute build_minuta_structure.py.')
      }
    })()
    return () => { alive = false }
  }, [])

  const reloadChapter = useCallback(async (chapterId) => {
    if (!chapterId) return
    setChapterSugs(await store.listSuggestions({ chapterId }))
    setCounts(await store.getChapterCounts())
  }, [])

  useEffect(() => { reloadChapter(selectedChapterId) }, [selectedChapterId, reloadChapter])

  async function handleChangeUser(id) { setCurrentUser(await store.setCurrentUser(id)) }
  function selectChapter(id) { setSelectedChapterId(id); setSelectedTarget(null) }

  async function addSuggestion(payload) {
    await store.addSuggestion(payload)
    await reloadChapter(selectedChapterId)
    refreshSelectedTarget()
  }
  async function support(s) {
    if (s.supporters.includes(currentUser?.id)) await store.unsupportSuggestion(s.id, currentUser.id)
    else await store.supportSuggestion(s.id, currentUser.id)
    await reloadChapter(selectedChapterId)
    refreshSelectedTarget()
  }
  async function comment(s, text) {
    await store.addComment(s.id, { authorId: currentUser?.id, text })
    await reloadChapter(selectedChapterId)
    refreshSelectedTarget()
  }
  function refreshSelectedTarget() { setSelectedTarget(t => (t ? { ...t } : t)) }

  if (error) {
    return (
      <>
        <div className="page-header"><div className="page-header-left"><h2 className="page-title">Revisão da Minuta</h2></div></div>
        <div className="page-body" style={{ padding: 32 }}><p style={{ color: '#c8102e' }}>{error}</p></div>
      </>
    )
  }
  if (!chapters) {
    return (
      <>
        <div className="page-header"><div className="page-header-left"><h2 className="page-title">Revisão da Minuta</h2></div></div>
        <div className="page-body" style={{ padding: 32 }}><p style={{ color: 'var(--text-muted)' }}>Carregando…</p></div>
      </>
    )
  }

  const chapter = chapters.find(c => c.chapterId === selectedChapterId)
  const sugsForTarget = selectedTarget
    ? chapterSugs.filter(s => s.targetId === selectedTarget.editId
        && (selectedTarget.kind === 'novaSecao' ? s.targetKind === 'secao' : s.incisoIndex === selectedTarget.incisoIndex))
    : []
  const incisoCount = {}
  for (const s of chapterSugs) {
    if (s.incisoIndex != null) { const k = incisoKey(s.targetId, s.incisoIndex); incisoCount[k] = (incisoCount[k] ?? 0) + 1 }
  }

  function selectInciso(art, inc) {
    setSelectedTarget({ kind: 'inciso', chapterId: chapter.chapterId, editId: art.editId, incisoIndex: inc.index, originalText: inc.text, label: `Inciso ${romanize(inc.index + 1)}` })
  }
  function selectNovaSecao() {
    setSelectedTarget({ kind: 'novaSecao', chapterId: chapter.chapterId, editId: chapter.chapterId, label: 'Nova seção neste capítulo' })
  }

  return (
    <>
      <div className="page-header">
        <div className="page-header-left">
          <h2 className="page-title">Revisão da Minuta — Sugestões do CONDEG</h2>
          <p className="page-subtitle">Selecione um capítulo, clique num inciso e proponha incluir, editar ou remover. Todos os coronéis veem as sugestões uns dos outros.</p>
        </div>
      </div>
      <div className="page-body">
        <IdentityBar users={users} currentUser={currentUser} onChangeUser={handleChangeUser} phaseLabel="Fase: Sugestões abertas" />
        <div style={{ display: 'flex', gap: 16, alignItems: 'flex-start' }}>
          <ChapterRail chapters={chapters} counts={counts} selectedId={selectedChapterId} onSelect={selectChapter} />

          <div style={{ flex: 1.25, minWidth: 0, border: '1px solid var(--border-card)', borderRadius: 8, background: '#fff', padding: '16px 20px', fontFamily: 'Georgia, "Times New Roman", serif', color: '#1a1a1a' }}>
            <div style={{ display: 'flex', alignItems: 'center', marginBottom: 8 }}>
              <p style={{ textAlign: 'center', fontWeight: 700, color: '#121d3d', margin: 0, flex: 1 }}>
                CAPÍTULO {romanize(chapter.chapterNumber)} — {chapter.chapterTitle}
              </p>
              <button onClick={selectNovaSecao} style={{ font: '700 10px Inter, sans-serif', color: '#c8102e', border: '1px dashed #e3a3ac', borderRadius: 5, padding: '3px 8px', background: '#fff', cursor: 'pointer' }}>+ nova seção</button>
            </div>
            {chapter.articles.map(art => (
              <div key={art.number} style={{ marginBottom: 10 }}>
                {art.sectionTitle && (
                  <p style={{ textAlign: 'center', fontWeight: 600, fontStyle: 'italic', fontSize: 13, color: '#444', margin: '10px 0 6px' }}>
                    Seção {romanize(art.sectionNumber)} — {art.sectionTitle}
                  </p>
                )}
                <p style={{ textAlign: 'justify', margin: '0 0 4px', textIndent: art.incisos.length ? 0 : '1.25em' }}>
                  <strong>{articleLabel(art.number)}</strong> {art.caput}
                </p>
                {art.incisos.map(inc => {
                  const n = incisoCount[incisoKey(art.editId, inc.index)] ?? 0
                  const sel = selectedTarget?.kind === 'inciso' && selectedTarget.editId === art.editId && selectedTarget.incisoIndex === inc.index
                  return (
                    <div key={inc.index} onClick={() => selectInciso(art, inc)} style={{
                      display: 'flex', gap: 6, padding: '3px 6px', borderRadius: 5, cursor: 'pointer',
                      background: sel ? '#fff7d6' : 'transparent', outline: sel ? '1px solid #f0d98a' : 'none',
                    }}>
                      <span><strong>{romanize(inc.index + 1)} -</strong> {inc.text}</span>
                      {n > 0 && (
                        <span style={{ marginLeft: 'auto', alignSelf: 'center', minWidth: 16, height: 15, padding: '0 4px', background: '#c8102e', color: '#fff', borderRadius: 8, font: '700 9px Inter, sans-serif', display: 'inline-flex', alignItems: 'center', justifyContent: 'center' }}>{n}</span>
                      )}
                    </div>
                  )
                })}
              </div>
            ))}
          </div>

          <SuggestionPanel
            target={selectedTarget}
            suggestions={sugsForTarget}
            users={users}
            currentUser={currentUser}
            onAddSuggestion={addSuggestion}
            onSupport={support}
            onComment={comment}
            onClose={() => setSelectedTarget(null)}
          />
        </div>
      </div>
    </>
  )
}
