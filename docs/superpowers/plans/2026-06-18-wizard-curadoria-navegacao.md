# Wizard — Curadoria e Navegação — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Transformar a etapa de revisão do `MinutaWizard` num documento único rolável com curadoria por inciso (checkbox incluir/excluir), filtro por fonte em lote, sidebar de navegação e edição livre por seção (modo avançado), refletindo tudo no `.docx`.

**Architecture:** A lib pura `buildArticles` ganha um predicado `isExcluded(editId, index)` e passa a carimbar cada inciso com `editId`/`index` e cada artigo com `editId`. O wizard mantém um único estado de verdade — `excluded: Set<"editId#index">` — onde o filtro por fonte é apenas uma operação em lote. A etapa 1 vira documento único (sidebar + barra de fontes + checkboxes inline); o `.docx` usa a mesma articulação curada.

**Tech Stack:** React 18 + Vite, `docx` (npm), `node:test` para a lib pura.

**Spec:** `docs/superpowers/specs/2026-06-18-wizard-curadoria-navegacao-design.md`

---

## File Structure

- **Modify** `src/lib/minutaArticles.js` — `buildArticles(structure, edits, isExcluded)`: 3º parâmetro predicado; incisos passam a `{text, source, editId, index}`; artigos ganham `editId`.
- **Modify** `src/lib/minutaArticles.test.js` — atualizar asserts de incisos e adicionar casos de exclusão.
- **Modify** `src/pages/MinutaWizard.jsx` — reescrita da etapa 1 (documento único, sidebar, barra de fontes, checkboxes inline, expansor de removidos, modo avançado por seção) e `.docx` com `isExcluded`.

**Nota de simplificação (vs. spec):** seção totalmente esvaziada por remoção manual é recuperável pelo botão global **"restaurar removidos (N)"** na barra de fontes (em vez de um stub por seção). Satisfaz a intenção do spec ("continuar alcançável/readicionável") com menos complexidade de render.

---

## Task 1: `buildArticles` com exclusão e identidade de inciso

**Files:**
- Modify: `src/lib/minutaArticles.js`
- Test: `src/lib/minutaArticles.test.js`

- [ ] **Step 1: Atualizar/Adicionar testes**

No `src/lib/minutaArticles.test.js`, substituir TODO o bloco a partir de `import { buildArticles } from './minutaArticles.js'` (linha ~30) até o fim do arquivo por:

```js
import { buildArticles } from './minutaArticles.js'

const STRUCTURE = {
  chapters: [
    {
      id: 'preliminares', kind: 'prose', chapterTitle: 'DAS DISPOSIÇÕES PRELIMINARES',
      editId: 'preliminares',
      proposedText: 'Primeiro artigo do objeto.\nSegundo artigo da base legal.',
    },
    {
      id: 'estrutura', kind: 'incisos', chapterTitle: 'DA ESTRUTURA ORGANIZACIONAL',
      editId: 'estrutura', caput: 'A estrutura operacional compõe-se dos órgãos:',
      items: [{ text: 'a DPO', source: 'ro' }, { text: 'o COT', source: 'ro' }],
    },
    {
      id: 'organ:dpo', kind: 'organ', chapterTitle: 'DA DIRETORIA DE PLANEJAMENTO OPERACIONAL (DPO)',
      organKey: 'dpo', label: 'Diretoria de Planejamento Operacional', abbr: 'DPO',
      sections: [
        {
          id: 'competencia', kind: 'incisos', sectionTitle: 'Da Competência',
          editId: 'organ:dpo/competencia', caput: 'Compete à DPO:',
          items: [
            { text: 'planejar as operações', source: 'ro' },
            { text: 'fiscalizar a instrução', source: 'cf. CBMAL, RI, Art. 115, VII' },
          ],
        },
        {
          id: 'cargo:diretor', kind: 'incisos', sectionTitle: 'Das Atribuições do Diretor',
          editId: 'organ:dpo/cargo:diretor', caput: 'Ao Diretor compete:',
          items: [{ text: 'dirigir a DPO', source: 'ro' }],
        },
      ],
    },
  ],
}

test('buildArticles numera artigos continuamente atravessando capítulos', () => {
  const arts = buildArticles(STRUCTURE, {})
  assert.deepEqual(arts.map(a => a.number), [1, 2, 3, 4, 5])
})

test('buildArticles marca capítulo no 1º artigo e numera capítulos em sequência', () => {
  const arts = buildArticles(STRUCTURE, {})
  assert.equal(arts[0].chapterTitle, 'DAS DISPOSIÇÕES PRELIMINARES')
  assert.equal(arts[0].chapterNumber, 1)
  assert.equal(arts[1].chapterTitle, null)
  assert.equal(arts[2].chapterTitle, 'DA ESTRUTURA ORGANIZACIONAL')
  assert.equal(arts[2].chapterNumber, 2)
  assert.equal(arts[3].chapterNumber, 3)
})

test('buildArticles numera seções por capítulo e marca no 1º artigo da seção', () => {
  const arts = buildArticles(STRUCTURE, {})
  assert.equal(arts[3].sectionNumber, 1)
  assert.equal(arts[3].sectionTitle, 'Da Competência')
})

test('cada artigo carrega o editId da sua folha de origem', () => {
  const arts = buildArticles(STRUCTURE, {})
  assert.equal(arts[0].editId, 'preliminares')
  assert.equal(arts[2].editId, 'estrutura')
  assert.equal(arts[3].editId, 'organ:dpo/competencia')
  assert.equal(arts[4].editId, 'organ:dpo/cargo:diretor')
})

test('incisos carregam texto normalizado, fonte, editId e index original', () => {
  const arts = buildArticles(STRUCTURE, {})
  assert.deepEqual(arts[3].incisos, [
    { text: 'planejar as operações; e', source: 'ro', editId: 'organ:dpo/competencia', index: 0 },
    { text: 'fiscalizar a instrução.', source: 'cf. CBMAL, RI, Art. 115, VII', editId: 'organ:dpo/competencia', index: 1 },
  ])
})

test('buildArticles articula prose como um artigo por linha', () => {
  const arts = buildArticles(STRUCTURE, {})
  assert.equal(arts[0].caput, 'Primeiro artigo do objeto.')
  assert.deepEqual(arts[0].incisos, [])
  assert.equal(arts[1].caput, 'Segundo artigo da base legal.')
})

test('buildArticles usa edits (texto) no lugar dos itens, com source nulo', () => {
  const arts = buildArticles(STRUCTURE, { 'organ:dpo/cargo:diretor': 'item editado\noutro item' })
  const diretor = arts.find(a => a.caput === 'Ao Diretor compete:')
  assert.deepEqual(diretor.incisos, [
    { text: 'item editado; e', source: null, editId: 'organ:dpo/cargo:diretor', index: 0 },
    { text: 'outro item.', source: null, editId: 'organ:dpo/cargo:diretor', index: 1 },
  ])
})

test('isExcluded pula o inciso e renumera os restantes (sufixo recalculado)', () => {
  const isExcluded = (editId, i) => editId === 'organ:dpo/competencia' && i === 0
  const arts = buildArticles(STRUCTURE, {}, isExcluded)
  const comp = arts.find(a => a.caput === 'Compete à DPO:')
  assert.deepEqual(comp.incisos, [
    { text: 'fiscalizar a instrução.', source: 'cf. CBMAL, RI, Art. 115, VII', editId: 'organ:dpo/competencia', index: 1 },
  ])
})

test('seção com todos os incisos excluídos é omitida e a numeração permanece contígua', () => {
  const isExcluded = (editId) => editId === 'organ:dpo/cargo:diretor'
  const arts = buildArticles(STRUCTURE, {}, isExcluded)
  assert.equal(arts.find(a => a.caput === 'Ao Diretor compete:'), undefined)
  assert.deepEqual(arts.map(a => a.number), [1, 2, 3, 4])
})
```

(Manter intactos os testes de `articleLabel`, `romanize`, `normalizeInciso` nas linhas 1–28.)

- [ ] **Step 2: Rodar os testes para confirmar que falham**

Run: `node --test src/lib/minutaArticles.test.js`
Expected: FAIL — incisos sem `editId`/`index`, artigos sem `editId`, e `isExcluded` ignorado.

- [ ] **Step 3: Reescrever `buildArticles` em `src/lib/minutaArticles.js`**

Substituir a função `buildArticles` (linhas 38–105) por:

```js
// Articula a estrutura hierárquica: chapters[] (prose | incisos | organ).
// Numeração de artigos contínua; capítulos e seções em romano (seção reseta por capítulo).
// edits[editId] (string) sobrepõe o texto de um nó-folha; ao editar, a fonte vira null.
// isExcluded(editId, index) remove incisos específicos (curadoria); a numeração ignora os removidos.
// Cada artigo carrega editId; cada inciso carrega { text, source, editId, index (original) }.
export function buildArticles(structure, edits = {}, isExcluded = () => false) {
  const articles = []
  let articleCounter = 0
  let chapterCounter = 0

  for (const chapter of structure.chapters) {
    let firstOfChapter = true
    let sectionCounter = 0

    const emitLeaf = (leaf, isSection) => {
      let firstOfSection = true

      const pushArticle = (caput, incisos) => {
        articleCounter += 1
        const art = {
          number: articleCounter, caput, incisos, editId: leaf.editId,
          chapterNumber: null, chapterTitle: null,
          sectionNumber: null, sectionTitle: null,
        }
        if (firstOfChapter) {
          chapterCounter += 1
          art.chapterNumber = chapterCounter
          art.chapterTitle = chapter.chapterTitle ?? null
          firstOfChapter = false
        }
        if (isSection && firstOfSection) {
          sectionCounter += 1
          art.sectionNumber = sectionCounter
          art.sectionTitle = leaf.sectionTitle ?? null
          firstOfSection = false
        }
        articles.push(art)
      }

      if (leaf.kind === 'prose') {
        const text = edits[leaf.editId] ?? leaf.proposedText ?? ''
        for (const line of text.split('\n')) {
          const c = line.trim()
          if (c) pushArticle(c, [])
        }
      } else if (leaf.kind === 'incisos') {
        const edited = edits[leaf.editId]
        let incisos
        if (edited != null) {
          const raw = edited.split('\n').map(l => l.trim()).filter(Boolean)
          incisos = raw.map((t, i) => ({
            text: normalizeInciso(t, i, raw.length),
            source: null, editId: leaf.editId, index: i,
          }))
        } else {
          // preserva o índice ORIGINAL em leaf.items para a chave de exclusão
          const kept = []
          ;(leaf.items ?? []).forEach((it, i) => {
            if (!(it.text ?? '').trim()) return
            if (isExcluded(leaf.editId, i)) return
            kept.push({ it, i })
          })
          incisos = kept.map((k, pos) => ({
            text: normalizeInciso(k.it.text, pos, kept.length),
            source: k.it.source ?? null, editId: leaf.editId, index: k.i,
          }))
        }
        if (incisos.length || !isSection) {
          pushArticle(leaf.caput ?? '', incisos)
        }
      }
    }

    if (chapter.kind === 'organ') {
      for (const section of chapter.sections) emitLeaf(section, true)
    } else {
      emitLeaf(chapter, false)
    }
  }

  return articles
}
```

- [ ] **Step 4: Rodar os testes para confirmar que passam**

Run: `node --test src/lib/minutaArticles.test.js`
Expected: PASS — `# pass 11 / # fail 0` (3 de articleLabel/romanize/normalizeInciso + 8 de buildArticles).

- [ ] **Step 5: Commit**

```bash
git add src/lib/minutaArticles.js src/lib/minutaArticles.test.js
git commit -m "feat: buildArticles com predicado isExcluded e identidade editId/index nos incisos"
```

---

## Task 2: Reescrever a etapa de revisão do wizard (documento único + curadoria)

**Files:**
- Modify: `src/pages/MinutaWizard.jsx` (substituição total)

- [ ] **Step 1: Substituir `src/pages/MinutaWizard.jsx` inteiro por:**

```jsx
import { useState, useEffect, useMemo } from 'react'
import { ChevronRight, Download, ArrowLeft, Pencil, Check, RotateCcw } from 'lucide-react'
import {
  Document, Packer, Paragraph, TextRun,
  Footer, AlignmentType, ImageRun,
} from 'docx'
import { buildArticles, articleLabel, romanize } from '../lib/minutaArticles.js'

const STEP_LABELS = ['Visão geral', 'Revisão & curadoria', 'Download']

const slug = s => String(s).replace(/[^a-z0-9]+/gi, '-').replace(/^-|-$/g, '')
const chapterIdOf = editId => `cap-${slug(String(editId).split('/')[0])}`
const sectionIdOf = editId => `sec-${slug(editId)}`
const itemKey = (editId, index) => `${editId}#${index}`

// 'ro' -> 'RO'; 'cf. CBMPR, Lei ...' -> 'CBMPR'
function sourceKey(source) {
  if (!source || source === 'ro') return 'RO'
  const m = source.match(/^cf\.\s*([^,]+)/)
  return (m ? m[1] : source).trim()
}

// Índice editId -> { items, sectionTitle, chapterTitle, proposedText, kind }
function indexLeaves(structure) {
  const idx = {}
  for (const ch of structure.chapters) {
    if (ch.kind === 'organ') {
      for (const s of ch.sections) {
        idx[s.editId] = {
          items: s.items ?? [], proposedText: s.proposedText ?? '',
          sectionTitle: s.sectionTitle, chapterTitle: ch.chapterTitle, kind: s.kind,
        }
      }
    } else {
      idx[ch.editId] = {
        items: ch.items ?? [], proposedText: ch.proposedText ?? '',
        sectionTitle: null, chapterTitle: ch.chapterTitle, kind: ch.kind,
      }
    }
  }
  return idx
}

// Mapa sourceKey -> [itemKey] (todos os itens estruturados da minuta)
function indexSources(structure) {
  const map = {}
  const add = (editId, items) => {
    ;(items ?? []).forEach((it, i) => {
      if (!(it.text ?? '').trim()) return
      const k = sourceKey(it.source)
      ;(map[k] ||= []).push(itemKey(editId, i))
    })
  }
  for (const ch of structure.chapters) {
    if (ch.kind === 'organ') ch.sections.forEach(s => add(s.editId, s.items))
    else add(ch.editId, ch.items)
  }
  return map
}

function srcBadge(source) {
  if (!source || source === 'ro') return null
  return (
    <span style={{
      marginLeft: 6, fontSize: 11, fontFamily: 'Inter, sans-serif',
      color: '#fff', background: '#c8102e', borderRadius: 4, padding: '1px 6px',
    }}>{source}</span>
  )
}

export default function MinutaWizard() {
  const [step, setStep] = useState(0)
  const [data, setData] = useState(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)
  const [edits, setEdits] = useState({})            // editId -> texto (modo avançado)
  const [advanced, setAdvanced] = useState(new Set())  // editIds em modo avançado
  const [excluded, setExcluded] = useState(new Set()) // "editId#index" removidos
  const [generating, setGenerating] = useState(false)

  useEffect(() => {
    fetch('/database/minuta_structure.json')
      .then(r => { if (!r.ok) throw new Error(r.status); return r.json() })
      .then(setData)
      .catch(() => setError('Erro ao carregar minuta_structure.json. Execute build_minuta_structure.py.'))
      .finally(() => setLoading(false))
  }, [])

  const leafIndex = useMemo(() => (data ? indexLeaves(data) : {}), [data])
  const sourceMap = useMemo(() => (data ? indexSources(data) : {}), [data])
  const sourceKeys = useMemo(() => {
    const keys = Object.keys(sourceMap)
    return ['RO', ...keys.filter(k => k !== 'RO').sort()]
  }, [sourceMap])

  const isExcluded = (editId, index) => excluded.has(itemKey(editId, index))

  function toggleItem(editId, index) {
    setExcluded(prev => {
      const next = new Set(prev)
      const k = itemKey(editId, index)
      if (next.has(k)) next.delete(k); else next.add(k)
      return next
    })
  }

  function sourceChecked(key) {
    const keys = sourceMap[key] ?? []
    return keys.some(k => !excluded.has(k))   // marcado se ao menos 1 incluso
  }

  function toggleSource(key) {
    const keys = sourceMap[key] ?? []
    const turnOff = sourceChecked(key)
    setExcluded(prev => {
      const next = new Set(prev)
      keys.forEach(k => { if (turnOff) next.add(k); else next.delete(k) })
      return next
    })
  }

  function setAllSources(on) {
    setExcluded(prev => {
      const next = new Set(prev)
      sourceKeys.forEach(key => {
        if (key === 'RO') return
        ;(sourceMap[key] ?? []).forEach(k => { if (on) next.delete(k); else next.add(k) })
      })
      return next
    })
  }

  function openAdvanced(editId) {
    setEdits(prev => prev[editId] != null ? prev : { ...prev, [editId]: leafIndex[editId]?.proposedText ?? '' })
    setAdvanced(prev => new Set(prev).add(editId))
  }
  function closeAdvanced(editId) {
    setAdvanced(prev => { const n = new Set(prev); n.delete(editId); return n })
    setEdits(prev => { const n = { ...prev }; delete n[editId]; return n })
  }

  function startReview() { setStep(1) }

  // Itens removidos por editId (para o expansor "N removidos")
  const removedByEditId = useMemo(() => {
    const map = {}
    Object.entries(leafIndex).forEach(([editId, leaf]) => {
      ;(leaf.items ?? []).forEach((it, i) => {
        if (excluded.has(itemKey(editId, i)) && (it.text ?? '').trim()) {
          ;(map[editId] ||= []).push({ ...it, index: i })
        }
      })
    })
    return map
  }, [leafIndex, excluded])

  const removedCount = excluded.size

  async function handleDownload() {
    setGenerating(true)
    try {
      const dateStr = new Date().toLocaleDateString('pt-BR', { day: '2-digit', month: 'long', year: 'numeric' })
      let imageData = null
      try {
        const resp = await fetch('/BrasaoCBMRO2D-COMPLETO.png')
        if (resp.ok) imageData = await resp.arrayBuffer()
      } catch (_) { /* segue sem imagem */ }

      const children = []
      if (imageData) {
        children.push(new Paragraph({
          alignment: AlignmentType.CENTER,
          children: [new ImageRun({ data: imageData, transformation: { width: 65, height: 65 }, type: 'png' })],
        }))
      }
      children.push(
        new Paragraph({
          alignment: AlignmentType.CENTER, spacing: { before: 120 },
          children: [new TextRun({ text: 'CORPO DE BOMBEIROS MILITAR DO ESTADO DE RONDÔNIA', bold: true, size: 28, font: 'Times New Roman' })],
        }),
        new Paragraph({
          alignment: AlignmentType.CENTER,
          children: [new TextRun({ text: `Minuta de Regimento Interno — ${data.title}`, size: 24, font: 'Times New Roman' })],
        }),
        new Paragraph({
          alignment: AlignmentType.CENTER, spacing: { after: 480 },
          children: [new TextRun({ text: dateStr, size: 22, font: 'Times New Roman', italics: true })],
        }),
      )

      const articles = buildArticles(data, edits, isExcluded)
      let chapterSeen = false
      articles.forEach(art => {
        if (art.chapterTitle) {
          children.push(
            new Paragraph({
              alignment: AlignmentType.CENTER, pageBreakBefore: chapterSeen,
              spacing: { before: 240, after: 0 },
              children: [new TextRun({ text: `CAPÍTULO ${romanize(art.chapterNumber)}`, bold: true, font: 'Times New Roman', size: 26 })],
            }),
            new Paragraph({
              alignment: AlignmentType.CENTER, spacing: { after: 120 },
              children: [new TextRun({ text: art.chapterTitle, bold: true, font: 'Times New Roman', size: 26 })],
            }),
          )
          chapterSeen = true
        }
        if (art.sectionTitle) {
          children.push(new Paragraph({
            alignment: AlignmentType.CENTER, spacing: { before: 120, after: 80 },
            children: [new TextRun({ text: `Seção ${romanize(art.sectionNumber)} — ${art.sectionTitle}`, bold: true, italics: true, font: 'Times New Roman', size: 24 })],
          }))
        }
        children.push(new Paragraph({
          alignment: AlignmentType.JUSTIFIED,
          spacing: { line: 360, after: art.incisos.length ? 60 : 120 },
          indent: art.incisos.length ? undefined : { firstLine: 708 },
          children: [
            new TextRun({ text: `${articleLabel(art.number)} `, bold: true, font: 'Times New Roman', size: 24 }),
            new TextRun({ text: art.caput, font: 'Times New Roman', size: 24 }),
          ],
        }))
        art.incisos.forEach((inc, i) => {
          const runs = [new TextRun({ text: `${romanize(i + 1)} - ${inc.text}`, font: 'Times New Roman', size: 24 })]
          if (inc.source && inc.source !== 'ro') {
            runs.push(new TextRun({ text: ` (${inc.source})`, font: 'Times New Roman', size: 20, italics: true, color: '888888' }))
          }
          children.push(new Paragraph({
            alignment: AlignmentType.JUSTIFIED, spacing: { line: 360, after: 60 },
            indent: { left: 708, hanging: 340 }, children: runs,
          }))
        })
      })

      const doc = new Document({
        sections: [{
          properties: { page: { margin: { top: 1701, right: 1134, bottom: 1134, left: 1701 } } },
          footers: {
            default: new Footer({
              children: [new Paragraph({
                alignment: AlignmentType.CENTER,
                children: [new TextRun({ text: `Documento gerado pelo Portal de Legislação CBM — CBMRO · ${dateStr}`, size: 18, font: 'Times New Roman', italics: true })],
              })],
            }),
          },
          children,
        }],
      })

      const blob = await Packer.toBlob(doc)
      const url = URL.createObjectURL(blob)
      const a = document.createElement('a')
      a.href = url
      a.download = 'Minuta_RI_Operacional_CBMRO.docx'
      document.body.appendChild(a)
      a.click()
      document.body.removeChild(a)
      URL.revokeObjectURL(url)
    } finally {
      setGenerating(false)
    }
  }

  if (loading) {
    return (
      <>
        <div className="page-header"><div className="page-header-left"><h2 className="page-title">Minuta de Regimento Interno</h2></div></div>
        <div className="page-body" style={{ padding: 32 }}><p style={{ color: 'var(--text-muted)' }}>Carregando dados…</p></div>
      </>
    )
  }
  if (error) {
    return (
      <>
        <div className="page-header"><div className="page-header-left"><h2 className="page-title">Minuta de Regimento Interno</h2></div></div>
        <div className="page-body" style={{ padding: 32 }}><p style={{ color: '#c8102e' }}>{error}</p></div>
      </>
    )
  }

  const articles = buildArticles(data, edits, isExcluded)
  const renderedAdvanced = new Set()

  function scrollTo(id) {
    const el = document.getElementById(id)
    if (el) el.scrollIntoView({ behavior: 'smooth', block: 'start' })
  }

  // ── Render de um artigo no modo curadoria ──
  function renderArticle(art) {
    const blocks = []
    if (art.chapterTitle) {
      blocks.push(
        <p key={`c-${art.number}`} id={chapterIdOf(art.editId)}
          style={{ textAlign: 'center', fontWeight: 700, margin: '20px 0 6px', scrollMarginTop: 70 }}>
          CAPÍTULO {romanize(art.chapterNumber)}<br />{art.chapterTitle}
        </p>,
      )
    }
    if (art.sectionTitle) {
      blocks.push(
        <p key={`s-${art.number}`} id={sectionIdOf(art.editId)}
          style={{ textAlign: 'center', fontWeight: 600, fontStyle: 'italic', margin: '10px 0 6px', scrollMarginTop: 70 }}>
          Seção {romanize(art.sectionNumber)} — {art.sectionTitle}
        </p>,
      )
    }

    const inAdvanced = advanced.has(art.editId)
    if (inAdvanced) {
      if (!renderedAdvanced.has(art.editId)) {
        renderedAdvanced.add(art.editId)
        blocks.push(
          <div key={`adv-${art.number}`} style={{ margin: '6px 0 14px' }}>
            <textarea
              value={edits[art.editId] ?? ''}
              onChange={e => setEdits(prev => ({ ...prev, [art.editId]: e.target.value }))}
              style={{
                width: '100%', minHeight: 160, padding: 12, border: '1.5px solid var(--border-card)',
                borderRadius: 8, fontSize: 13.5, lineHeight: 1.6, fontFamily: 'Inter, sans-serif',
                resize: 'vertical', boxSizing: 'border-box', outline: 'none',
              }}
            />
            <button onClick={() => closeAdvanced(art.editId)} style={{
              marginTop: 6, display: 'inline-flex', alignItems: 'center', gap: 6, padding: '5px 12px',
              border: '1.5px solid var(--border-card)', borderRadius: 6, background: '#fff', cursor: 'pointer', fontSize: 13,
            }}><Check size={14} /> Concluir edição</button>
          </div>,
        )
      }
      return blocks
    }

    // Caput + botão "editar texto"
    blocks.push(
      <div key={`cap-${art.number}`} style={{ display: 'flex', alignItems: 'baseline', gap: 8, margin: '0 0 4px' }}>
        <p style={{ textAlign: 'justify', margin: 0, flex: 1, textIndent: art.incisos.length ? 0 : '1.25em' }}>
          <strong>{articleLabel(art.number)}</strong> {art.caput}
        </p>
        <button onClick={() => openAdvanced(art.editId)} title="Editar texto desta seção" style={{
          flexShrink: 0, display: 'inline-flex', alignItems: 'center', gap: 4, padding: '2px 8px',
          border: '1px solid var(--border-card)', borderRadius: 5, background: '#fff', cursor: 'pointer',
          fontSize: 12, color: 'var(--text-muted)',
        }}><Pencil size={12} /> editar</button>
      </div>,
    )

    art.incisos.forEach((inc, i) => {
      blocks.push(
        <label key={`i-${art.number}-${i}`} style={{
          display: 'flex', gap: 8, alignItems: 'flex-start', padding: '2px 0 2px 24px',
          cursor: 'pointer', textAlign: 'justify',
        }}>
          <input type="checkbox" checked readOnly={false}
            onChange={() => toggleItem(inc.editId, inc.index)}
            style={{ marginTop: 5, flexShrink: 0, cursor: 'pointer' }} />
          <span><strong>{romanize(i + 1)} -</strong> {inc.text}{srcBadge(inc.source)}</span>
        </label>,
      )
    })

    const removed = removedByEditId[art.editId] ?? []
    if (removed.length) {
      blocks.push(<RemovedBlock key={`rm-${art.number}`} removed={removed} onRestore={toggleItem} editId={art.editId} />)
    }
    return blocks
  }

  return (
    <>
      <div className="page-header">
        <div className="page-header-left">
          <h2 className="page-title">Minuta de Regimento Interno</h2>
          <p className="page-subtitle">
            Minuta articulada da estrutura operacional do CBMRO — do topo (DPO/COT/DOE)
            à menor fração — com competências do CBMRO e subsídios de outras legislações.
          </p>
        </div>
      </div>

      <div className="page-body">
        <div style={{ display: 'flex', alignItems: 'center', gap: 8, marginBottom: 24 }}>
          {STEP_LABELS.map((label, i) => (
            <div key={i} style={{ display: 'flex', alignItems: 'center', gap: 8 }}>
              <div style={{
                width: 28, height: 28, borderRadius: '50%', display: 'flex', alignItems: 'center', justifyContent: 'center',
                background: i <= step ? '#c8102e' : '#d1d5db', color: '#fff', fontWeight: 700, fontSize: 13, flexShrink: 0,
              }}>{i + 1}</div>
              <span style={{ fontSize: 13, color: i === step ? '#c8102e' : 'var(--text-muted)', fontWeight: i === step ? 600 : 400 }}>{label}</span>
              {i < 2 && <ChevronRight size={16} color="#d1d5db" style={{ flexShrink: 0 }} />}
            </div>
          ))}
        </div>

        {/* Etapa 0: visão geral */}
        {step === 0 && (
          <div>
            <div style={{ border: '1px solid var(--border-card)', borderRadius: 8, background: '#fff', padding: 24, marginBottom: 20, maxHeight: 520, overflow: 'auto' }}>
              <PlainPreview articles={buildArticles(data, {})} />
            </div>
            <button onClick={startReview} style={{
              display: 'flex', alignItems: 'center', gap: 8, padding: '11px 26px', border: 'none', borderRadius: 7,
              background: '#c8102e', color: '#fff', fontWeight: 600, cursor: 'pointer', fontSize: 15,
            }}>Revisar e curar a minuta <ChevronRight size={18} /></button>
          </div>
        )}

        {/* Etapa 1: documento único + curadoria */}
        {step === 1 && (
          <div style={{ display: 'flex', gap: 18, alignItems: 'flex-start' }}>
            {/* Sidebar de navegação */}
            <nav style={{
              flex: '0 0 230px', position: 'sticky', top: 16, maxHeight: '82vh', overflow: 'auto',
              border: '1px solid var(--border-card)', borderRadius: 8, background: '#fff', padding: 12, fontSize: 13,
            }}>
              <div style={{ fontWeight: 700, color: 'var(--text-muted)', textTransform: 'uppercase', fontSize: 11, marginBottom: 8 }}>Sumário</div>
              {data.chapters.map(ch => (
                <div key={ch.id} style={{ marginBottom: 4 }}>
                  <button onClick={() => scrollTo(chapterIdOf(ch.id))} style={{
                    border: 'none', background: 'none', padding: '2px 0', textAlign: 'left', cursor: 'pointer',
                    color: '#121d3d', fontWeight: 600, fontSize: 12.5,
                  }}>{ch.chapterTitle}</button>
                  {ch.kind === 'organ' && ch.sections.map(s => {
                    const rm = (removedByEditId[s.editId] ?? []).length
                    return (
                      <button key={s.editId} onClick={() => scrollTo(sectionIdOf(s.editId))} style={{
                        display: 'block', border: 'none', background: 'none', padding: '1px 0 1px 12px', textAlign: 'left',
                        cursor: 'pointer', color: 'var(--text-muted)', fontSize: 12,
                      }}>{s.sectionTitle}{rm > 0 && <span style={{ color: '#c8102e', fontWeight: 700 }}> ·{rm}</span>}</button>
                    )
                  })}
                </div>
              ))}
            </nav>

            {/* Documento */}
            <div style={{ flex: 1, minWidth: 0 }}>
              {/* Barra de fontes (fixa) */}
              <div style={{
                position: 'sticky', top: 0, zIndex: 5, background: '#eef1f6', borderBottom: '1px solid var(--border-card)',
                padding: '10px 4px', marginBottom: 12, display: 'flex', flexWrap: 'wrap', gap: 10, alignItems: 'center',
              }}>
                <span style={{ fontSize: 12, fontWeight: 700, color: 'var(--text-muted)' }}>Fontes:</span>
                {sourceKeys.map(key => (
                  <label key={key} style={{ display: 'inline-flex', alignItems: 'center', gap: 4, fontSize: 12.5, cursor: key === 'RO' ? 'default' : 'pointer', opacity: key === 'RO' ? 0.7 : 1 }}>
                    <input type="checkbox" checked={key === 'RO' ? true : sourceChecked(key)} disabled={key === 'RO'}
                      onChange={() => toggleSource(key)} style={{ cursor: key === 'RO' ? 'default' : 'pointer' }} />
                    {key}
                  </label>
                ))}
                <span style={{ marginLeft: 'auto', display: 'inline-flex', gap: 8 }}>
                  <button onClick={() => setAllSources(true)} style={chipBtn}>marcar todas</button>
                  <button onClick={() => setAllSources(false)} style={chipBtn}>desmarcar todas</button>
                  {removedCount > 0 && (
                    <button onClick={() => setExcluded(new Set())} style={{ ...chipBtn, color: '#c8102e', borderColor: '#c8102e' }}>
                      <RotateCcw size={12} style={{ verticalAlign: -2, marginRight: 3 }} />restaurar removidos ({removedCount})
                    </button>
                  )}
                </span>
              </div>

              <div style={{
                border: '1px solid var(--border-card)', borderRadius: 8, background: '#fff', padding: '20px 24px',
                fontFamily: 'Georgia, "Times New Roman", serif', fontSize: 14, lineHeight: 1.7, color: '#1a1a1a',
              }}>
                {articles.map(art => <div key={art.number} style={{ marginBottom: 8 }}>{renderArticle(art)}</div>)}
              </div>

              <div style={{ display: 'flex', justifyContent: 'space-between', marginTop: 18 }}>
                <button onClick={() => setStep(0)} style={{
                  display: 'flex', alignItems: 'center', gap: 6, padding: '9px 20px', border: '1.5px solid var(--border-card)',
                  borderRadius: 7, background: '#fff', cursor: 'pointer', fontSize: 14,
                }}><ArrowLeft size={16} /> Voltar</button>
                <button onClick={() => setStep(2)} style={{
                  display: 'flex', alignItems: 'center', gap: 6, padding: '9px 24px', border: 'none', borderRadius: 7,
                  background: '#c8102e', color: '#fff', fontWeight: 600, cursor: 'pointer', fontSize: 14,
                }}>Ir para download <ChevronRight size={16} /></button>
              </div>
            </div>
          </div>
        )}

        {/* Etapa 2: download */}
        {step === 2 && (
          <div style={{ maxWidth: 820 }}>
            <h3 style={{ color: '#121d3d', marginBottom: 16, fontSize: 17 }}>Resumo da minuta — {data.title}</h3>
            <div style={{ border: '1px solid var(--border-card)', borderRadius: 8, background: '#fff', padding: 24, marginBottom: 4, maxHeight: 520, overflow: 'auto' }}>
              <PlainPreview articles={articles} />
            </div>
            <div style={{ display: 'flex', gap: 12, marginTop: 24, flexWrap: 'wrap' }}>
              <button onClick={() => setStep(1)} style={{
                display: 'flex', alignItems: 'center', gap: 6, padding: '10px 20px', border: '1.5px solid var(--border-card)', borderRadius: 7,
                background: '#fff', cursor: 'pointer', fontSize: 14,
              }}><ArrowLeft size={16} /> Voltar e curar</button>
              <button onClick={handleDownload} disabled={generating} style={{
                display: 'flex', alignItems: 'center', gap: 8, padding: '10px 24px', border: 'none', borderRadius: 7,
                background: generating ? '#9ca3af' : '#c8102e', color: '#fff', fontWeight: 600, cursor: generating ? 'wait' : 'pointer', fontSize: 14,
              }}><Download size={16} />{generating ? 'Gerando…' : 'Baixar Minuta_RI_Operacional_CBMRO.docx'}</button>
            </div>
          </div>
        )}
      </div>
    </>
  )
}

const chipBtn = {
  border: '1px solid var(--border-card)', borderRadius: 5, background: '#fff',
  padding: '3px 9px', fontSize: 12, cursor: 'pointer', color: '#121d3d',
}

// Expansor "N removidos" por seção
function RemovedBlock({ removed, onRestore, editId }) {
  const [open, setOpen] = useState(false)
  return (
    <div style={{ paddingLeft: 24, margin: '4px 0 8px' }}>
      <button onClick={() => setOpen(o => !o)} style={{
        border: 'none', background: 'none', cursor: 'pointer', color: 'var(--text-muted)', fontSize: 12.5, padding: 0,
      }}>{open ? '▾' : '▸'} {removed.length} removido{removed.length > 1 ? 's' : ''}</button>
      {open && removed.map(it => (
        <label key={it.index} style={{ display: 'flex', gap: 8, alignItems: 'flex-start', padding: '2px 0', cursor: 'pointer', color: '#9ca3af' }}>
          <input type="checkbox" checked={false} onChange={() => onRestore(editId, it.index)} style={{ marginTop: 4, cursor: 'pointer' }} />
          <span style={{ textDecoration: 'line-through' }}>{it.text}{it.source && it.source !== 'ro' ? ` (${it.source})` : ''}</span>
        </label>
      ))}
    </div>
  )
}

// Prévia somente-leitura (etapas 0 e 2)
function PlainPreview({ articles }) {
  if (!articles.length) return <p style={{ color: 'var(--text-muted)', fontSize: 13 }}>(sem conteúdo)</p>
  return (
    <div style={{ fontFamily: 'Georgia, "Times New Roman", serif', fontSize: 14, lineHeight: 1.7, color: '#1a1a1a' }}>
      {articles.map(art => (
        <div key={art.number} style={{ marginBottom: 10 }}>
          {art.chapterTitle && (
            <p style={{ textAlign: 'center', fontWeight: 700, margin: '18px 0 6px' }}>
              CAPÍTULO {romanize(art.chapterNumber)}<br />{art.chapterTitle}
            </p>
          )}
          {art.sectionTitle && (
            <p style={{ textAlign: 'center', fontWeight: 600, fontStyle: 'italic', margin: '8px 0 8px' }}>
              Seção {romanize(art.sectionNumber)} — {art.sectionTitle}
            </p>
          )}
          <p style={{ textAlign: 'justify', margin: '0 0 6px', textIndent: art.incisos.length ? 0 : '1.25em' }}>
            <strong>{articleLabel(art.number)}</strong> {art.caput}
          </p>
          {art.incisos.map((inc, i) => (
            <p key={i} style={{ textAlign: 'justify', margin: '0 0 4px', paddingLeft: '2em', textIndent: '-1em' }}>
              {romanize(i + 1)} - {inc.text}{srcBadge(inc.source)}
            </p>
          ))}
        </div>
      ))}
    </div>
  )
}
```

- [ ] **Step 2: Conferir o build de produção**

Run: `npm run build`
Expected: build conclui sem erros. (Se algum import de ícone do lucide-react não existir, ajustar; `Pencil`, `Check`, `RotateCcw`, `ArrowLeft`, `Download`, `ChevronRight` existem no lucide-react.)

- [ ] **Step 3: Commit**

```bash
git add src/pages/MinutaWizard.jsx
git commit -m "feat: wizard com curadoria por inciso, filtro por fonte e navegação"
```

---

## Task 3: Verificação manual e checkpoint

**Files:** nenhuma alteração de código (verificação).

- [ ] **Step 1: Garantir o dev server**

Run (se ainda não estiver no ar): `npm run dev -- --port 5173 --strictPort`
Expected: `Local: http://localhost:5173/`.

- [ ] **Step 2: Conferir o fluxo de curadoria no navegador**

Abrir http://localhost:5173 → "Minuta de Regimento Interno". Verificar:
- Etapa 0 mostra a prévia completa; botão "Revisar e curar a minuta" leva à etapa 1.
- Etapa 1: sidebar lista capítulos e seções; clicar rola até a seção.
- Barra de fontes mostra RO (fixo) + CBMAL/CBMPR/CBMMT/CBMSC/CBMBA/CBMPE/CBMES/CBMPA. Desmarcar **CBMAL** remove em lote todos os incisos `cf. CBMAL` e a numeração se ajusta ao vivo; marcar de novo os restaura.
- Desmarcar o checkbox de um inciso o remove e renumera; aparece "▸ N removidos" naquela seção; expandir e remarcar restaura o inciso.
- "restaurar removidos (N)" no topo zera todas as remoções.
- Em uma seção, "editar" abre a textarea (modo avançado); "Concluir edição" volta aos checkboxes preservando as remoções anteriores.
- Etapa 2: a prévia bate com a curadoria; baixar o `.docx` e conferir que os incisos removidos NÃO aparecem e que as citações `(cf. …)` constam dos incisos enriquecidos mantidos.

- [ ] **Step 3: Confirmar que o Comparador de Cargos segue intacto**

Dashboard → aba "Comparativo de Cargos" carrega normalmente (`ro.json` não foi tocado).

- [ ] **Step 4: Checkpoint final**

```bash
git add -A
git commit -m "chore: checkpoint — curadoria e navegação do wizard"
```

---

## Self-Review (autor do plano)

- **Cobertura do spec:** modelo de estado único (`excluded` Set, filtro em lote) → Task 2 (`toggleSource`/`setAllSources`/`excluded`); `buildArticles` com `isExcluded` + `editId`/`index` → Task 1; documento único + sidebar + barra de fontes + checkboxes inline + expansor de removidos + modo avançado → Task 2 (`renderArticle`, `RemovedBlock`, `NavSidebar` inline, barra de fontes); `.docx` usa o mesmo `isExcluded` → Task 2 `handleDownload`; seção totalmente removida recuperável → botão global "restaurar removidos" (simplificação anotada); testes → Task 1; verificação → Task 3. ✔
- **Consistência de tipos:** incisos `{text, source, editId, index}` e artigos `{…, editId}` definidos em Task 1 e consumidos em Task 2 (`inc.editId`, `inc.index`, `art.editId`). Chave de exclusão `editId#index` consistente em `itemKey`, `buildArticles` e `indexSources`. `sourceKey` idêntico em `indexSources` e nos badges. ✔
- **Sem placeholders:** todo o código presente; comandos com saída esperada. ✔
- **YAGNI:** sem persistência (localStorage), sem dedup semântico, sem reordenação — anotados como fora de escopo.
