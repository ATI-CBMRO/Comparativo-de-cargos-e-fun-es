import { useEffect, useState, useCallback } from 'react'
import { Download } from 'lucide-react'
import { romanize } from '../lib/minutaArticles.js'
import { buildTargets, itemKeyOf } from '../lib/minutaTargets.js'
import { applyDecisionsToEdits } from '../lib/minutaConsolidation.js'
import { buildMinutaBlob } from '../lib/minutaDocx.js'
import { suggestionsStore as store } from '../lib/suggestionsStore.js'
import IdentityBar from '../components/IdentityBar.jsx'
import SuggestionCard from '../components/SuggestionCard.jsx'

// Agrupa sugestões em "itens" deliberáveis por (editId, incisoIndex).
function groupItems(chapters, suggestions) {
  const byChapterTitle = {}
  const incisoText = {}
  for (const c of chapters) {
    byChapterTitle[c.chapterId] = c.chapterTitle
    for (const a of c.articles) for (const inc of a.incisos) incisoText[itemKeyOf(a.editId, inc.index)] = { chapterId: c.chapterId, caput: a.caput, romano: romanize(inc.index + 1), text: inc.text }
  }
  const map = new Map()
  for (const s of suggestions) {
    const key = itemKeyOf(s.targetId, s.incisoIndex)
    if (!map.has(key)) {
      const meta = incisoText[key]
      map.set(key, {
        key, chapterId: s.chapterId, chapterTitle: byChapterTitle[s.chapterId] ?? s.chapterId,
        location: meta ? `${meta.caput} — inciso ${meta.romano}` : (s.targetKind === 'secao' ? 'Nova seção proposta' : s.targetId),
        originalText: meta?.text ?? s.originalText ?? '', suggestions: [],
      })
    }
    map.get(key).suggestions.push(s)
  }
  return [...map.values()]
}

export default function MinutaDeliberacao() {
  const [structure, setStructure] = useState(null)
  const [chapters, setChapters] = useState([])
  const [users, setUsers] = useState([])
  const [currentUser, setCurrentUser] = useState(null)
  const [items, setItems] = useState([])
  const [resolutions, setResolutions] = useState({})
  const [activeKey, setActiveKey] = useState(null)
  const [finalDraft, setFinalDraft] = useState('')
  const [error, setError] = useState(null)
  const [generating, setGenerating] = useState(false)

  const reload = useCallback(async (chs) => {
    const all = await store.listSuggestions()
    const grouped = groupItems(chs, all)
    setItems(grouped)
    const res = {}
    for (const it of grouped) res[it.key] = await store.getItemResolution(it.key)
    setResolutions(res)
  }, [])

  useEffect(() => {
    let alive = true
    ;(async () => {
      try {
        const r = await fetch('/database/minuta_structure.json')
        if (!r.ok) throw new Error(r.status)
        const struct = await r.json()
        const chs = buildTargets(struct)
        const [us, cu] = [await store.listUsers(), await store.getCurrentUser()]
        if (!alive) return
        setStructure(struct); setChapters(chs); setUsers(us); setCurrentUser(cu)
        await reload(chs)
      } catch {
        if (alive) setError('Erro ao carregar minuta_structure.json. Execute build_minuta_structure.py.')
      }
    })()
    return () => { alive = false }
  }, [reload])

  async function handleChangeUser(id) { setCurrentUser(await store.setCurrentUser(id)) }

  function openItem(it) {
    setActiveKey(it.key)
    const accepted = it.suggestions.find(s => s.status === 'aceita')
    setFinalDraft(resolutions[it.key]?.finalText || accepted?.proposedText || it.originalText || '')
  }

  async function decide(s, status) {
    await store.decideSuggestion(s.id, status, currentUser?.id)
    await reload(chapters)
    const it = groupItems(chapters, await store.listSuggestions()).find(i => i.key === activeKey)
    if (it) { const acc = it.suggestions.find(x => x.status === 'aceita'); if (acc) setFinalDraft(acc.proposedText) }
  }

  async function approveItem() {
    await store.setFinalText(activeKey, finalDraft, currentUser?.id)
    await reload(chapters)
    const next = items.find(it => it.key !== activeKey && resolutions[it.key]?.status !== 'decidido')
    setActiveKey(next ? next.key : null)
    if (next) openItem(next)
  }

  async function generateFinal() {
    setGenerating(true)
    try {
      const all = await store.listSuggestions()
      const edits = applyDecisionsToEdits(structure, all)
      const blob = await buildMinutaBlob({ structure, edits, subtitle: 'Minuta de Regimento Interno — consolidada pela deliberação do CONDEG' })
      const url = URL.createObjectURL(blob)
      const a = document.createElement('a')
      a.href = url; a.download = 'Minuta_RI_CBMRO_consolidada.docx'
      document.body.appendChild(a); a.click(); document.body.removeChild(a)
      URL.revokeObjectURL(url)
    } finally { setGenerating(false) }
  }

  if (error) {
    return (<><div className="page-header"><div className="page-header-left"><h2 className="page-title">Deliberação do CONDEG</h2></div></div><div className="page-body" style={{ padding: 32 }}><p style={{ color: '#c8102e' }}>{error}</p></div></>)
  }
  if (!structure) {
    return (<><div className="page-header"><div className="page-header-left"><h2 className="page-title">Deliberação do CONDEG</h2></div></div><div className="page-body" style={{ padding: 32 }}><p style={{ color: 'var(--text-muted)' }}>Carregando…</p></div></>)
  }

  const decidedCount = items.filter(it => resolutions[it.key]?.status === 'decidido').length
  const active = items.find(it => it.key === activeKey)
  const pct = items.length ? Math.round((decidedCount / items.length) * 100) : 0

  return (
    <>
      <div className="page-header">
        <div className="page-header-left">
          <h2 className="page-title">Deliberação do CONDEG</h2>
          <p className="page-subtitle">Itens que receberam sugestões. Decida cada uma, escreva o texto final e aprove. Ao fim, gere a minuta consolidada.</p>
        </div>
      </div>
      <div className="page-body">
        <IdentityBar users={users} currentUser={currentUser} onChangeUser={handleChangeUser} phaseLabel="Fase: Deliberação" />

        {items.length === 0 && <p style={{ color: 'var(--text-muted)' }}>Nenhuma sugestão registrada ainda. Use a tela de Revisão para criar sugestões.</p>}

        {items.length > 0 && (
          <>
            <div style={{ display: 'flex', alignItems: 'center', gap: 12, marginBottom: 14 }}>
              <div style={{ flex: 1, height: 8, background: '#dde3ec', borderRadius: 4, overflow: 'hidden' }}>
                <div style={{ height: '100%', width: `${pct}%`, background: '#1a7f37' }} />
              </div>
              <span style={{ fontSize: 12, color: 'var(--text-muted)', fontWeight: 600 }}>{decidedCount}/{items.length} itens decididos</span>
              <button onClick={generateFinal} disabled={generating} style={{ display: 'inline-flex', alignItems: 'center', gap: 6, border: 'none', borderRadius: 7, background: generating ? '#9ca3af' : '#1a7f37', color: '#fff', fontWeight: 600, padding: '8px 16px', cursor: generating ? 'wait' : 'pointer', fontSize: 13 }}>
                <Download size={15} />{generating ? 'Gerando…' : 'Gerar minuta final (.docx)'}
              </button>
            </div>

            <div style={{ display: 'flex', gap: 16, alignItems: 'flex-start' }}>
              {/* Lista de pendências (entrada) */}
              <div style={{ flex: '0 0 320px', border: '1px solid var(--border-card)', borderRadius: 8, background: '#fff', overflow: 'hidden' }}>
                <div style={{ font: '700 11px Inter, sans-serif', color: '#121d3d', textTransform: 'uppercase', padding: '10px 12px', borderBottom: '1px solid var(--border-card)' }}>Itens com sugestões</div>
                {items.map(it => {
                  const decided = resolutions[it.key]?.status === 'decidido'
                  const isActive = it.key === activeKey
                  return (
                    <button key={it.key} onClick={() => openItem(it)} style={{ display: 'flex', alignItems: 'center', gap: 8, width: '100%', textAlign: 'left', border: 'none', borderBottom: '1px solid #eef1f6', background: isActive ? '#fdeaec' : '#fff', padding: '8px 12px', cursor: 'pointer', fontSize: 12 }}>
                      <span style={{ width: 20, height: 20, borderRadius: '50%', background: '#c8102e', color: '#fff', font: '700 10px Inter, sans-serif', display: 'flex', alignItems: 'center', justifyContent: 'center', flexShrink: 0 }}>{it.suggestions.length}</span>
                      <span style={{ flex: 1, color: '#444', lineHeight: 1.3 }}>{it.chapterTitle}<br /><span style={{ color: '#8a93a6' }}>{it.location}</span></span>
                      <span style={{ font: '700 8px Inter, sans-serif', padding: '2px 7px', borderRadius: 10, background: decided ? '#e8f5ec' : '#fff4d6', color: decided ? '#1a7f37' : '#9a6b00', flexShrink: 0 }}>{decided ? 'decidido' : 'pendente'}</span>
                    </button>
                  )
                })}
              </div>

              {/* Fila de revisão (decidir) */}
              <div style={{ flex: 1, minWidth: 0 }}>
                {!active && <div style={{ border: '1px solid var(--border-card)', borderRadius: 8, background: '#fff', padding: 24, color: 'var(--text-muted)', fontSize: 13 }}>Selecione um item à esquerda para deliberar.</div>}
                {active && (
                  <div style={{ border: '1px solid var(--border-card)', borderRadius: 8, background: '#fff', padding: '16px 18px' }}>
                    <div style={{ font: '700 11px Inter, sans-serif', color: '#8a93a6', textTransform: 'uppercase', marginBottom: 4 }}>{active.chapterTitle} · {active.location}</div>
                    <div style={{ fontFamily: 'Georgia, serif', fontSize: 13.5, color: '#1a1a1a', background: '#f7f9fc', borderRadius: 6, padding: '8px 10px', marginBottom: 12 }}>
                      <span style={{ font: '700 8px Inter, sans-serif', textTransform: 'uppercase', color: '#9aa3b5', display: 'block', marginBottom: 2 }}>Texto vigente</span>
                      {active.originalText || '(item sem texto-base)'}
                    </div>
                    {active.suggestions.map(s => (
                      <SuggestionCard key={s.id} suggestion={s} users={users} currentUser={currentUser} mode="deliberate" onDecide={decide} />
                    ))}
                    <div style={{ background: '#fffdf3', border: '1px dashed #d8c98f', borderRadius: 6, padding: 10, marginTop: 8 }}>
                      <div style={{ font: '700 9px Inter, sans-serif', textTransform: 'uppercase', color: '#9a6b00', marginBottom: 4 }}>Texto final aprovado</div>
                      <textarea value={finalDraft} onChange={e => setFinalDraft(e.target.value)} style={{ width: '100%', boxSizing: 'border-box', minHeight: 56, border: '1px solid #d8c98f', borderRadius: 5, fontSize: 13, padding: 8, fontFamily: 'Georgia, serif' }} />
                      <button onClick={approveItem} style={{ marginTop: 8, border: 'none', background: '#1a7f37', color: '#fff', font: '700 11px Inter, sans-serif', padding: '7px 14px', borderRadius: 6, cursor: 'pointer' }}>Aprovar item e avançar ▸</button>
                    </div>
                  </div>
                )}
              </div>
            </div>
          </>
        )}
      </div>
    </>
  )
}
