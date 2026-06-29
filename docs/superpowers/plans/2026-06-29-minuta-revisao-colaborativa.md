# Revisão Colaborativa da Minuta de RI — Plano de Implementação

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Construir o protótipo de frontend do fluxo colaborativo de sugestão + deliberação do CONDEG sobre a minuta de RI, rodando contra dados simulados (localStorage) por uma camada de dados isolada e trocável por backend.

**Architecture:** Duas páginas novas (`/minuta/revisao` e `/minuta/deliberacao`) leem `database/minuta_structure.json` e operam sobre `src/lib/suggestionsStore.js` (API assíncrona sobre localStorage, coronéis fictícios, swap-seam para backend). Lógica pura (alvos endereçáveis, consolidação de decisões, geração do .docx) fica em módulos `src/lib/*` testados com `node --test`; as telas reusam `buildArticles` e o tema CBMRO via classes/estilos inline existentes.

**Tech Stack:** React 18 + react-router-dom 6 (SPA Vite), `docx` para exportação, `node:test` para testes de lógica pura, `lucide-react` para ícones. Sem backend.

---

## Contexto para quem implementa (leia antes da Task 1)

- O frontend é uma SPA estática; páginas fazem `fetch('/database/minuta_structure.json')`. Não há backend.
- `src/lib/minutaArticles.js` já existe e exporta `buildArticles(structure, edits, isExcluded)`, `articleLabel(n)`, `romanize(n)`, `normalizeInciso(text, i, total)`. NÃO altere esse arquivo.
  - `buildArticles` devolve uma lista de artigos `{ number, caput, incisos, editId, chapterNumber, chapterTitle, sectionNumber, sectionTitle }`. `chapterNumber` só vem preenchido no **primeiro artigo de cada capítulo** (senão `null`); cada inciso é `{ text, source, editId, index }` (`index` = posição original na seção).
  - `edits[editId]` (string com incisos separados por `\n`) substitui o texto de uma folha; `isExcluded(editId, index)` remove um inciso.
- Testes de lógica rodam com `node --test` (não há script npm; use o comando direto mostrado em cada task). Não há suíte de testes de UI: páginas/componentes são verificados manualmente com `npm run dev` (http://localhost:5173).
- Estilo do projeto: componentes com **estilos inline** (ver `src/pages/MinutaWizard.jsx`) e variáveis CSS já existentes (`var(--border-card)`, `var(--text-muted)`); tema CBMRO (vermelho `#c8102e`, navy `#121d3d`). Reuse as classes `page-header`, `page-header-left`, `page-title`, `page-subtitle`, `page-body`.
- Há arquivos `database/markdown/*.md` modificados no working tree por trabalho ANTERIOR a este plano. **Nunca** use `git add -A`/`git add .`; sempre adicione caminhos explícitos nos commits.

---

## Task 1: Camada de dados `suggestionsStore`

**Files:**
- Create: `src/lib/suggestionsStore.js`
- Test: `src/lib/suggestionsStore.test.js`

- [ ] **Step 1: Escrever o store**

Create `src/lib/suggestionsStore.js`:

```js
// Camada de dados ISOLADA do fluxo de revisão colaborativa da minuta de RI.
// API assíncrona (Promise) no formato de um backend REST. Hoje persiste em
// localStorage; quando o backend real existir, basta criar outra implementação com
// a MESMA assinatura (via createSuggestionsStore) e trocar a instância exportada —
// as telas não mudam.

const STORAGE_KEY = 'cbm.minuta.revisao.v1'

// "Sessão" simulada: coronéis fictícios do CONDEG (1 relator + membros).
export const MOCK_USERS = [
  { id: 'u-costa', name: 'João Costa',   posto: 'Cel. BM', role: 'relator' },
  { id: 'u-lima',  name: 'Pedro Lima',   posto: 'Cel. BM', role: 'condeg' },
  { id: 'u-souza', name: 'Ana Souza',    posto: 'Cel. BM', role: 'condeg' },
  { id: 'u-rocha', name: 'Marcos Rocha', posto: 'Cel. BM', role: 'condeg' },
]

function genId(prefix) {
  return `${prefix}-${Date.now().toString(36)}-${Math.random().toString(36).slice(2, 7)}`
}

const EMPTY = () => ({ currentUserId: null, suggestions: [], resolutions: {} })

// `storage` deve ter getItem/setItem/removeItem (igual ao localStorage).
export function createSuggestionsStore(storage) {
  function read() {
    try {
      const raw = storage.getItem(STORAGE_KEY)
      if (!raw) return EMPTY()
      const s = JSON.parse(raw)
      return {
        currentUserId: s.currentUserId ?? null,
        suggestions: Array.isArray(s.suggestions) ? s.suggestions : [],
        resolutions: s.resolutions && typeof s.resolutions === 'object' ? s.resolutions : {},
      }
    } catch {
      return EMPTY()
    }
  }
  function write(state) { storage.setItem(STORAGE_KEY, JSON.stringify(state)); return state }

  return {
    listUsers() { return Promise.resolve(MOCK_USERS) },

    getCurrentUser() {
      const { currentUserId } = read()
      return Promise.resolve(MOCK_USERS.find(u => u.id === currentUserId) ?? MOCK_USERS[0])
    },

    setCurrentUser(userId) {
      const state = read()
      state.currentUserId = userId
      write(state)
      return Promise.resolve(MOCK_USERS.find(u => u.id === userId) ?? MOCK_USERS[0])
    },

    listSuggestions({ chapterId, targetId } = {}) {
      let out = read().suggestions
      if (chapterId) out = out.filter(s => s.chapterId === chapterId)
      if (targetId) out = out.filter(s => s.targetId === targetId)
      return Promise.resolve(out)
    },

    addSuggestion(p) {
      const state = read()
      const sug = {
        id: genId('sug'),
        chapterId: p.chapterId,
        targetId: p.targetId,
        targetKind: p.targetKind,                 // 'inciso' | 'secao'
        incisoIndex: p.incisoIndex ?? null,
        type: p.type,                             // 'editar'|'incluir'|'remover'|'incluir-secao'|'renomear-secao'|'remover-secao'
        originalText: p.originalText ?? '',
        proposedText: p.proposedText ?? '',
        sectionTitle: p.sectionTitle ?? '',       // usado por incluir-secao/renomear-secao
        justification: p.justification ?? '',
        authorId: p.authorId,
        createdAt: new Date().toISOString(),
        supporters: [],
        comments: [],
        status: 'pendente',
        decidedBy: null,
        decidedAt: null,
      }
      state.suggestions.push(sug)
      write(state)
      return Promise.resolve(sug)
    },

    supportSuggestion(id, userId) {
      const state = read()
      const s = state.suggestions.find(x => x.id === id)
      if (s && !s.supporters.includes(userId)) s.supporters.push(userId)
      write(state)
      return Promise.resolve(s ?? null)
    },

    unsupportSuggestion(id, userId) {
      const state = read()
      const s = state.suggestions.find(x => x.id === id)
      if (s) s.supporters = s.supporters.filter(u => u !== userId)
      write(state)
      return Promise.resolve(s ?? null)
    },

    addComment(id, { authorId, text }) {
      const state = read()
      const s = state.suggestions.find(x => x.id === id)
      const comment = { id: genId('cmt'), authorId, text, createdAt: new Date().toISOString() }
      if (s) s.comments.push(comment)
      write(state)
      return Promise.resolve(comment)
    },

    decideSuggestion(id, status, userId) {
      const state = read()
      const s = state.suggestions.find(x => x.id === id)
      if (s) { s.status = status; s.decidedBy = userId; s.decidedAt = new Date().toISOString() }
      write(state)
      return Promise.resolve(s ?? null)
    },

    getItemResolution(itemKey) {
      const { resolutions } = read()
      return Promise.resolve(resolutions[itemKey] ?? {
        targetId: itemKey, finalText: '', status: 'pendente', resolvedBy: null, resolvedAt: null,
      })
    },

    setFinalText(itemKey, text, userId) {
      const state = read()
      state.resolutions[itemKey] = {
        targetId: itemKey, finalText: text, status: 'decidido',
        resolvedBy: userId, resolvedAt: new Date().toISOString(),
      }
      write(state)
      return Promise.resolve(state.resolutions[itemKey])
    },

    getChapterCounts() {
      const counts = {}
      for (const s of read().suggestions) counts[s.chapterId] = (counts[s.chapterId] ?? 0) + 1
      return Promise.resolve(counts)
    },

    resetDemo() { storage.removeItem(STORAGE_KEY); return Promise.resolve() },
  }
}

function memoryStorage() {
  const m = new Map()
  return {
    getItem: k => (m.has(k) ? m.get(k) : null),
    setItem: (k, v) => { m.set(k, String(v)) },
    removeItem: k => { m.delete(k) },
  }
}

const defaultStorage =
  (typeof globalThis !== 'undefined' && globalThis.localStorage) ? globalThis.localStorage : memoryStorage()

export const suggestionsStore = createSuggestionsStore(defaultStorage)
```

- [ ] **Step 2: Escrever os testes**

Create `src/lib/suggestionsStore.test.js`:

```js
import { test } from 'node:test'
import assert from 'node:assert/strict'
import { createSuggestionsStore, MOCK_USERS } from './suggestionsStore.js'

function fakeStorage() {
  const m = new Map()
  return {
    getItem: k => (m.has(k) ? m.get(k) : null),
    setItem: (k, v) => m.set(k, String(v)),
    removeItem: k => m.delete(k),
  }
}

const base = {
  chapterId: 'organ:cg', targetId: 'organ:cg/competencia', targetKind: 'inciso',
  incisoIndex: 2, type: 'editar', originalText: 'dirigir', proposedText: 'comandar',
  authorId: 'u-costa',
}

test('addSuggestion grava autoria, status pendente e defaults', async () => {
  const store = createSuggestionsStore(fakeStorage())
  const s = await store.addSuggestion(base)
  assert.equal(s.authorId, 'u-costa')
  assert.equal(s.status, 'pendente')
  assert.deepEqual(s.supporters, [])
  assert.deepEqual(s.comments, [])
  assert.ok(s.id && s.createdAt)
})

test('listSuggestions filtra por chapterId e por targetId', async () => {
  const store = createSuggestionsStore(fakeStorage())
  await store.addSuggestion(base)
  await store.addSuggestion({ ...base, chapterId: 'organ:dp', targetId: 'organ:dp/competencia' })
  assert.equal((await store.listSuggestions()).length, 2)
  assert.equal((await store.listSuggestions({ chapterId: 'organ:cg' })).length, 1)
  assert.equal((await store.listSuggestions({ targetId: 'organ:dp/competencia' })).length, 1)
})

test('apoiar é idempotente e desapoiar remove', async () => {
  const store = createSuggestionsStore(fakeStorage())
  const s = await store.addSuggestion(base)
  await store.supportSuggestion(s.id, 'u-lima')
  await store.supportSuggestion(s.id, 'u-lima')
  let got = (await store.listSuggestions())[0]
  assert.deepEqual(got.supporters, ['u-lima'])
  await store.unsupportSuggestion(s.id, 'u-lima')
  got = (await store.listSuggestions())[0]
  assert.deepEqual(got.supporters, [])
})

test('decideSuggestion grava status e autor da decisão', async () => {
  const store = createSuggestionsStore(fakeStorage())
  const s = await store.addSuggestion(base)
  await store.decideSuggestion(s.id, 'aceita', 'u-costa')
  const got = (await store.listSuggestions())[0]
  assert.equal(got.status, 'aceita')
  assert.equal(got.decidedBy, 'u-costa')
  assert.ok(got.decidedAt)
})

test('getChapterCounts conta sugestões por capítulo', async () => {
  const store = createSuggestionsStore(fakeStorage())
  await store.addSuggestion(base)
  await store.addSuggestion({ ...base, type: 'remover' })
  await store.addSuggestion({ ...base, chapterId: 'organ:dp', targetId: 'organ:dp/competencia' })
  assert.deepEqual(await store.getChapterCounts(), { 'organ:cg': 2, 'organ:dp': 1 })
})

test('setFinalText/getItemResolution faz upsert e marca decidido', async () => {
  const store = createSuggestionsStore(fakeStorage())
  assert.equal((await store.getItemResolution('k1')).status, 'pendente')
  await store.setFinalText('k1', 'texto final', 'u-costa')
  const r = await store.getItemResolution('k1')
  assert.equal(r.finalText, 'texto final')
  assert.equal(r.status, 'decidido')
  assert.equal(r.resolvedBy, 'u-costa')
})

test('persiste entre instâncias que compartilham o mesmo storage', async () => {
  const storage = fakeStorage()
  const a = createSuggestionsStore(storage)
  await a.setCurrentUser('u-lima')
  await a.addSuggestion(base)
  const b = createSuggestionsStore(storage)
  assert.equal((await b.getCurrentUser()).id, 'u-lima')
  assert.equal((await b.listSuggestions()).length, 1)
})

test('getCurrentUser default = primeiro usuário; setCurrentUser troca', async () => {
  const store = createSuggestionsStore(fakeStorage())
  assert.equal((await store.getCurrentUser()).id, MOCK_USERS[0].id)
  await store.setCurrentUser('u-rocha')
  assert.equal((await store.getCurrentUser()).id, 'u-rocha')
})

test('resetDemo limpa tudo', async () => {
  const store = createSuggestionsStore(fakeStorage())
  await store.addSuggestion(base)
  await store.resetDemo()
  assert.equal((await store.listSuggestions()).length, 0)
})
```

- [ ] **Step 3: Rodar os testes e ver passar**

Run: `node --test src/lib/suggestionsStore.test.js`
Expected: todos os testes PASS (9 passos de teste).

- [ ] **Step 4: Commit**

```bash
git add src/lib/suggestionsStore.js src/lib/suggestionsStore.test.js
git commit -m "feat(minuta): camada de dados isolada de sugestões (localStorage + mock)"
```

---

## Task 2: Alvos endereçáveis `minutaTargets`

**Files:**
- Create: `src/lib/minutaTargets.js`
- Test: `src/lib/minutaTargets.test.js`

- [ ] **Step 1: Escrever o módulo**

Create `src/lib/minutaTargets.js`:

```js
// Deriva, do minuta_structure.json articulado, a lista de capítulos com seus
// artigos/incisos endereçáveis para a UI de revisão. Reusa buildArticles para
// herdar numeração e normalização — não reimplementa nada disso.
import { buildArticles } from './minutaArticles.js'

// chapterId = prefixo do editId antes da primeira "/" (ex.: "organ:cg/competencia"
// -> "organ:cg"; "estrutura/direcao" -> "estrutura"; "preliminares" -> "preliminares").
export function chapterIdOf(editId) {
  return String(editId).split('/')[0]
}

// Chave única de um "item" deliberável: inciso = "<editId>#<index>"; seção/prose = editId.
export function itemKeyOf(editId, incisoIndex) {
  return incisoIndex == null ? editId : `${editId}#${incisoIndex}`
}

// -> [{ chapterId, chapterTitle, chapterNumber,
//        articles: [{ editId, number, caput, sectionTitle, sectionNumber,
//                     incisos: [{ index, text, source }] }] }]
export function buildTargets(structure) {
  const arts = buildArticles(structure)
  const chapters = []
  let current = null
  for (const a of arts) {
    if (a.chapterNumber) {
      current = {
        chapterId: chapterIdOf(a.editId),
        chapterTitle: a.chapterTitle,
        chapterNumber: a.chapterNumber,
        articles: [],
      }
      chapters.push(current)
    }
    current.articles.push({
      editId: a.editId,
      number: a.number,
      caput: a.caput,
      sectionTitle: a.sectionTitle,
      sectionNumber: a.sectionNumber,
      incisos: a.incisos.map(inc => ({ index: inc.index, text: inc.text, source: inc.source })),
    })
  }
  return chapters
}
```

- [ ] **Step 2: Escrever os testes**

Create `src/lib/minutaTargets.test.js`:

```js
import { test } from 'node:test'
import assert from 'node:assert/strict'
import { buildTargets, chapterIdOf, itemKeyOf } from './minutaTargets.js'

test('chapterIdOf extrai o prefixo do editId', () => {
  assert.equal(chapterIdOf('organ:cg/competencia'), 'organ:cg')
  assert.equal(chapterIdOf('estrutura/direcao'), 'estrutura')
  assert.equal(chapterIdOf('preliminares'), 'preliminares')
})

test('itemKeyOf compõe a chave do item', () => {
  assert.equal(itemKeyOf('organ:cg/competencia', 2), 'organ:cg/competencia#2')
  assert.equal(itemKeyOf('preliminares', null), 'preliminares')
})

const STRUCTURE = {
  chapters: [
    {
      id: 'preliminares', kind: 'prose', chapterTitle: 'DAS DISPOSIÇÕES PRELIMINARES',
      editId: 'preliminares', proposedText: 'Primeiro artigo.\nSegundo artigo.',
    },
    {
      id: 'organ:cg', kind: 'organ', chapterTitle: 'DO COMANDO-GERAL (CG)',
      organKey: 'cg', label: 'Comando-Geral', abbr: 'CG',
      sections: [
        {
          id: 'competencia', kind: 'incisos', sectionTitle: 'Da Competência',
          editId: 'organ:cg/competencia', caput: 'Compete ao CG:',
          items: [
            { text: 'planejar as ações', source: 'ro' },
            { text: 'dirigir a Corporação', source: 'ro' },
          ],
        },
      ],
    },
  ],
}

test('buildTargets agrupa por capítulo com chapterId/título/número', () => {
  const chs = buildTargets(STRUCTURE)
  assert.equal(chs.length, 2)
  assert.equal(chs[0].chapterId, 'preliminares')
  assert.equal(chs[0].chapterTitle, 'DAS DISPOSIÇÕES PRELIMINARES')
  assert.equal(chs[1].chapterId, 'organ:cg')
  assert.equal(chs[1].chapterNumber, 2)
})

test('buildTargets expõe incisos com index original e editId da seção', () => {
  const chs = buildTargets(STRUCTURE)
  const comp = chs[1].articles.find(a => a.caput === 'Compete ao CG:')
  assert.equal(comp.editId, 'organ:cg/competencia')
  assert.equal(comp.sectionTitle, 'Da Competência')
  assert.deepEqual(comp.incisos.map(i => i.index), [0, 1])
  assert.equal(comp.incisos[0].text, 'planejar as ações; e')
})
```

- [ ] **Step 3: Rodar os testes e ver passar**

Run: `node --test src/lib/minutaTargets.test.js`
Expected: 4 testes PASS.

- [ ] **Step 4: Commit**

```bash
git add src/lib/minutaTargets.js src/lib/minutaTargets.test.js
git commit -m "feat(minuta): deriva alvos endereçáveis (capítulo/seção/inciso) do structure"
```

---

## Task 3: Consolidação de decisões `minutaConsolidation`

Transforma as sugestões ACEITAS num objeto `edits` (editId → incisos por linha) consumível por `buildArticles`, para gerar a minuta final na Fase 2.

**Files:**
- Create: `src/lib/minutaConsolidation.js`
- Test: `src/lib/minutaConsolidation.test.js`

- [ ] **Step 1: Escrever o módulo**

Create `src/lib/minutaConsolidation.js`:

```js
// A partir das sugestões ACEITAS, produz `edits` (editId -> texto multilinha de
// incisos crus) para alimentar buildArticles e gerar a minuta consolidada.
// Aplica, por seção: remover (descarta o inciso), editar (troca o texto) e incluir
// (anexa novo inciso ao fim). Seções totalmente novas (incluir-secao) ficam fora do
// protótipo de geração (registradas como sugestão, não inseridas no .docx).

// Indexa os textos CRUS (não normalizados) de cada folha "incisos" da estrutura.
function indexRawItems(structure) {
  const idx = {}
  const addLeaf = leaf => {
    if (leaf && leaf.kind === 'incisos') idx[leaf.editId] = (leaf.items ?? []).map(it => it.text ?? '')
  }
  for (const ch of structure.chapters) {
    if (ch.kind === 'organ') (ch.sections ?? []).forEach(addLeaf)
    else if (ch.kind === 'articles') (ch.articles ?? []).forEach(addLeaf)
  }
  return idx
}

export function applyDecisionsToEdits(structure, suggestions) {
  const raw = indexRawItems(structure)
  const byEdit = {}
  for (const s of suggestions) {
    if (s.status !== 'aceita') continue
    ;(byEdit[s.targetId] ||= []).push(s)
  }

  const edits = {}
  for (const [editId, list] of Object.entries(byEdit)) {
    const base = raw[editId]
    if (!base) continue // sem incisos crus (prose ou seção nova) — fora do protótipo
    const items = base.map((text, index) => ({ text, index, removed: false }))
    const appended = []
    for (const s of list) {
      if (s.type === 'remover' && s.incisoIndex != null) {
        const t = items.find(i => i.index === s.incisoIndex)
        if (t) t.removed = true
      } else if (s.type === 'editar' && s.incisoIndex != null) {
        const t = items.find(i => i.index === s.incisoIndex)
        if (t && (s.proposedText ?? '').trim()) t.text = s.proposedText.trim()
      } else if (s.type === 'incluir' && (s.proposedText ?? '').trim()) {
        appended.push(s.proposedText.trim())
      }
    }
    const finalTexts = items.filter(i => !i.removed).map(i => i.text).concat(appended)
    edits[editId] = finalTexts.join('\n')
  }
  return edits
}
```

- [ ] **Step 2: Escrever os testes**

Create `src/lib/minutaConsolidation.test.js`:

```js
import { test } from 'node:test'
import assert from 'node:assert/strict'
import { applyDecisionsToEdits } from './minutaConsolidation.js'

const STRUCTURE = {
  chapters: [
    {
      id: 'organ:cg', kind: 'organ', chapterTitle: 'DO COMANDO-GERAL (CG)',
      organKey: 'cg', abbr: 'CG',
      sections: [
        {
          id: 'competencia', kind: 'incisos', sectionTitle: 'Da Competência',
          editId: 'organ:cg/competencia', caput: 'Compete ao CG:',
          items: [
            { text: 'planejar as ações', source: 'ro' },
            { text: 'dirigir a Corporação', source: 'ro' },
          ],
        },
      ],
    },
  ],
}

const sug = (p) => ({
  id: 'x', chapterId: 'organ:cg', targetId: 'organ:cg/competencia', targetKind: 'inciso',
  status: 'aceita', proposedText: '', incisoIndex: null, type: 'editar', ...p,
})

test('editar troca o texto do inciso pelo índice', () => {
  const edits = applyDecisionsToEdits(STRUCTURE, [
    sug({ type: 'editar', incisoIndex: 0, proposedText: 'comandar a Corporação' }),
  ])
  assert.equal(edits['organ:cg/competencia'], 'comandar a Corporação\ndirigir a Corporação')
})

test('remover descarta o inciso e incluir anexa ao fim', () => {
  const edits = applyDecisionsToEdits(STRUCTURE, [
    sug({ type: 'remover', incisoIndex: 1 }),
    sug({ type: 'incluir', proposedText: 'fiscalizar o serviço' }),
  ])
  assert.equal(edits['organ:cg/competencia'], 'planejar as ações\nfiscalizar o serviço')
})

test('ignora sugestões não aceitas', () => {
  const edits = applyDecisionsToEdits(STRUCTURE, [
    sug({ type: 'editar', incisoIndex: 0, proposedText: 'X', status: 'pendente' }),
    sug({ type: 'editar', incisoIndex: 0, proposedText: 'Y', status: 'rejeitada' }),
  ])
  assert.deepEqual(edits, {})
})
```

- [ ] **Step 3: Rodar os testes e ver passar**

Run: `node --test src/lib/minutaConsolidation.test.js`
Expected: 3 testes PASS.

- [ ] **Step 4: Commit**

```bash
git add src/lib/minutaConsolidation.js src/lib/minutaConsolidation.test.js
git commit -m "feat(minuta): consolida decisões aceitas em edits para a minuta final"
```

---

## Task 4: Extrair gerador de `.docx` para `minutaDocx` e refatorar o wizard

Hoje a geração do `.docx` está embutida em `MinutaWizard.handleDownload`. Extraia-a para um módulo reutilizável (será usado também pela Fase 2). Saída deve ser idêntica.

**Files:**
- Create: `src/lib/minutaDocx.js`
- Modify: `src/pages/MinutaWizard.jsx`

- [ ] **Step 1: Criar `src/lib/minutaDocx.js`**

Create `src/lib/minutaDocx.js`:

```js
// Gera o Blob .docx da minuta a partir da estrutura articulada. Extraído de
// MinutaWizard para reuso pela Fase 2 (deliberação). Mantém a formatação original.
import {
  Document, Packer, Paragraph, TextRun, Footer, AlignmentType, ImageRun,
} from 'docx'
import { buildArticles, articleLabel, romanize } from './minutaArticles.js'

export async function buildMinutaBlob({ structure, edits = {}, isExcluded = () => false, subtitle }) {
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
      children: [new TextRun({ text: subtitle, size: 24, font: 'Times New Roman' })],
    }),
    new Paragraph({
      alignment: AlignmentType.CENTER, spacing: { after: 480 },
      children: [new TextRun({ text: dateStr, size: 22, font: 'Times New Roman', italics: true })],
    }),
  )

  const articles = buildArticles(structure, edits, isExcluded)
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

  return await Packer.toBlob(doc)
}
```

- [ ] **Step 2: Refatorar `MinutaWizard.jsx` para usar o módulo**

In `src/pages/MinutaWizard.jsx`, remove the `docx` import block (lines 3-6, the `import { Document, Packer, ... } from 'docx'`) and add an import of the new helper. Change the import area near the top so it reads:

```js
import { buildArticles, articleLabel, romanize } from '../lib/minutaArticles.js'
import { buildMinutaBlob } from '../lib/minutaDocx.js'
```

(Keep the existing `import { useState, useEffect, useMemo } from 'react'` and the `lucide-react` import. Remove only the `docx` import.)

Then replace the entire body of `handleDownload` (everything between `setGenerating(true)` and the matching `finally`) so the function becomes:

```js
  async function handleDownload() {
    setGenerating(true)
    try {
      const blob = await buildMinutaBlob({
        structure: data,
        edits,
        isExcluded,
        subtitle: `Minuta de Regimento Interno — ${data.title}`,
      })
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
```

- [ ] **Step 3: Verificar manualmente (saída idêntica)**

Run: `npm run dev -- --port 5173 --strictPort`
Open http://localhost:5173/minuta → avance até "Download" → clique em "Baixar Minuta...". Confirme que o `.docx` baixa e abre com o mesmo cabeçalho/numeração de antes (capítulos em romano, artigos contínuos). Pare o servidor (Ctrl+C).

- [ ] **Step 4: Commit**

```bash
git add src/lib/minutaDocx.js src/pages/MinutaWizard.jsx
git commit -m "refactor(minuta): extrai gerador de .docx para minutaDocx (reuso na Fase 2)"
```

---

## Task 5: Componente `IdentityBar`

Barra de identidade simulada (troca de coronel) + indicador de fase.

**Files:**
- Create: `src/components/IdentityBar.jsx`

- [ ] **Step 1: Criar o componente**

Create `src/components/IdentityBar.jsx`:

```jsx
// Barra de "login simulado": escolhe qual coronel você é (autoria das ações) +
// rótulo da fase. No protótipo, a sessão vem do suggestionsStore (não há auth real).
export default function IdentityBar({ users, currentUser, onChangeUser, phaseLabel }) {
  return (
    <div style={{
      display: 'flex', alignItems: 'center', gap: 10, flexWrap: 'wrap',
      background: '#121d3d', color: '#fff', padding: '8px 14px', borderRadius: 8,
      fontSize: 13, marginBottom: 16,
    }}>
      <span style={{ background: 'rgba(255,255,255,.14)', padding: '3px 10px', borderRadius: 20, fontWeight: 600 }}>
        {phaseLabel}
      </span>
      <span style={{ opacity: .7 }}>Minuta de RI · CBMRO</span>
      <label style={{ marginLeft: 'auto', display: 'inline-flex', alignItems: 'center', gap: 8 }}>
        <span style={{ opacity: .7 }}>Você está como</span>
        <select
          value={currentUser?.id ?? ''}
          onChange={e => onChangeUser(e.target.value)}
          style={{
            background: '#0d1730', color: '#fff', border: '1px solid #2a3a63',
            borderRadius: 6, padding: '5px 8px', fontSize: 13, fontWeight: 600,
          }}
        >
          {users.map(u => (
            <option key={u.id} value={u.id}>
              {u.posto} {u.name}{u.role === 'relator' ? ' (relator)' : ''}
            </option>
          ))}
        </select>
      </label>
    </div>
  )
}
```

- [ ] **Step 2: Commit**

```bash
git add src/components/IdentityBar.jsx
git commit -m "feat(minuta): componente IdentityBar (sessão simulada do coronel)"
```

---

## Task 6: Componente `ChapterRail`

Trilha de capítulos filtrável, com badge de contagem por capítulo. Usada nas duas fases.

**Files:**
- Create: `src/components/ChapterRail.jsx`

- [ ] **Step 1: Criar o componente**

Create `src/components/ChapterRail.jsx`:

```jsx
import { useState } from 'react'

// Trilha lateral de capítulos: filtro por texto, alternador "só com sugestões" e
// badge de contagem (vermelho > 0, cinza quando 0). `chapters` vem de buildTargets.
export default function ChapterRail({ chapters, counts, selectedId, onSelect }) {
  const [filter, setFilter] = useState('')
  const [onlyWith, setOnlyWith] = useState(false)
  const f = filter.trim().toLowerCase()

  const list = chapters.filter(c => {
    if (f && !c.chapterTitle.toLowerCase().includes(f)) return false
    if (onlyWith && !((counts[c.chapterId] ?? 0) > 0)) return false
    return true
  })

  return (
    <nav style={{
      flex: '0 0 210px', position: 'sticky', top: 16, maxHeight: '82vh', overflow: 'auto',
      border: '1px solid var(--border-card)', borderRadius: 8, background: '#fff', padding: 12,
    }}>
      <div style={{ fontWeight: 700, color: 'var(--text-muted)', textTransform: 'uppercase', fontSize: 11, marginBottom: 8 }}>
        Capítulos
      </div>
      <input
        value={filter}
        onChange={e => setFilter(e.target.value)}
        placeholder="filtrar capítulo…"
        style={{ width: '100%', boxSizing: 'border-box', padding: '5px 8px', border: '1px solid var(--border-card)', borderRadius: 6, fontSize: 13, marginBottom: 6 }}
      />
      <label style={{ display: 'flex', alignItems: 'center', gap: 6, fontSize: 12, color: 'var(--text-muted)', marginBottom: 8, cursor: 'pointer' }}>
        <input type="checkbox" checked={onlyWith} onChange={e => setOnlyWith(e.target.checked)} /> só com sugestões
      </label>
      {list.map(c => {
        const n = counts[c.chapterId] ?? 0
        const active = c.chapterId === selectedId
        return (
          <button
            key={c.chapterId}
            onClick={() => onSelect(c.chapterId)}
            style={{
              display: 'flex', alignItems: 'center', gap: 6, width: '100%', textAlign: 'left',
              border: 'none', background: active ? '#fdeaec' : 'none',
              color: active ? '#c8102e' : '#444', fontWeight: active ? 700 : 500,
              padding: '5px 6px', borderRadius: 6, cursor: 'pointer', fontSize: 12.5, marginBottom: 2,
            }}
          >
            <span style={{ flex: 1 }}>{c.chapterTitle}</span>
            <span style={{
              minWidth: 18, textAlign: 'center', padding: '0 5px', height: 16, lineHeight: '16px',
              borderRadius: 8, fontSize: 10, fontWeight: 700,
              background: n > 0 ? '#c8102e' : '#d6deea', color: n > 0 ? '#fff' : '#5a6377',
            }}>{n}</span>
          </button>
        )
      })}
    </nav>
  )
}
```

- [ ] **Step 2: Commit**

```bash
git add src/components/ChapterRail.jsx
git commit -m "feat(minuta): componente ChapterRail (filtro por capítulo + contadores)"
```

---

## Task 7: Componente `SuggestionCard`

Uma sugestão na thread: autoria, etiqueta de tipo, Antes/Depois, apoiar/comentar e (modo deliberação) Aceitar/Rejeitar.

**Files:**
- Create: `src/components/SuggestionCard.jsx`

- [ ] **Step 1: Criar o componente**

Create `src/components/SuggestionCard.jsx`:

```jsx
import { useState } from 'react'

const TYPE_LABEL = {
  editar: 'Editar', incluir: 'Incluir inciso', remover: 'Remover',
  'incluir-secao': 'Nova seção', 'renomear-secao': 'Renomear seção', 'remover-secao': 'Remover seção',
}
const TYPE_COLOR = {
  editar: ['#fff4d6', '#9a6b00'], incluir: ['#e8f5ec', '#1a7f37'], remover: ['#fbeaec', '#c8102e'],
  'incluir-secao': ['#e8f5ec', '#1a7f37'], 'renomear-secao': ['#fff4d6', '#9a6b00'], 'remover-secao': ['#fbeaec', '#c8102e'],
}
const initialsOf = name => (name ?? '?').split(' ').filter(Boolean).map(w => w[0]).slice(0, 2).join('').toUpperCase()
const fmtDate = iso => { try { return new Date(iso).toLocaleDateString('pt-BR') } catch { return '' } }

// mode: 'review' (apoiar/comentar) | 'deliberate' (aceitar/rejeitar).
export default function SuggestionCard({ suggestion: s, users, currentUser, mode = 'review', onSupport, onComment, onDecide }) {
  const [commenting, setCommenting] = useState(false)
  const [draft, setDraft] = useState('')
  const author = users.find(u => u.id === s.authorId)
  const [bg, fg] = TYPE_COLOR[s.type] ?? ['#eef1f6', '#444']
  const supported = s.supporters.includes(currentUser?.id)
  const showOld = s.type === 'editar' || s.type === 'remover' || s.type === 'renomear-secao'
  const showNew = s.type === 'editar' || s.type === 'incluir' || s.type === 'incluir-secao' || s.type === 'renomear-secao'
  const decided = s.status !== 'pendente'

  return (
    <div style={{
      background: '#fff', border: '1px solid #e1e7f0', borderRadius: 8, padding: '9px 10px', marginBottom: 8,
      opacity: decided && mode === 'review' ? 0.85 : 1,
    }}>
      <div style={{ display: 'flex', alignItems: 'center', gap: 6, marginBottom: 5 }}>
        <span style={{ width: 18, height: 18, borderRadius: '50%', background: '#c8102e', color: '#fff', font: '700 9px Inter, sans-serif', display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
          {initialsOf(author?.name)}
        </span>
        <span style={{ font: '700 11px Inter, sans-serif', color: '#121d3d' }}>{author?.posto} {author?.name}</span>
        <span style={{ font: '11px Inter, sans-serif', color: '#8a93a6' }}>· {fmtDate(s.createdAt)}</span>
        <span style={{ marginLeft: 'auto', font: '700 9px Inter, sans-serif', textTransform: 'uppercase', padding: '2px 6px', borderRadius: 4, background: bg, color: fg }}>
          {TYPE_LABEL[s.type] ?? s.type}
        </span>
      </div>

      {s.type === 'incluir-secao' && s.sectionTitle && (
        <div style={{ font: '700 12px Georgia, serif', color: '#121d3d', marginBottom: 3 }}>{s.sectionTitle}</div>
      )}
      {showOld && (
        <>
          <div style={{ font: '700 8px Inter, sans-serif', textTransform: 'uppercase', color: '#9aa3b5', margin: '2px 0 1px' }}>Atual</div>
          <div style={{ borderRadius: 4, padding: '3px 6px', font: '12px/1.35 Georgia, serif', background: '#fbeaec', color: '#9b3b46', textDecoration: 'line-through' }}>{s.originalText}</div>
        </>
      )}
      {showNew && (
        <>
          <div style={{ font: '700 8px Inter, sans-serif', textTransform: 'uppercase', color: '#9aa3b5', margin: '4px 0 1px' }}>Proposto</div>
          <div style={{ borderRadius: 4, padding: '3px 6px', font: '12px/1.35 Georgia, serif', background: '#e8f5ec', color: '#1a5e30' }}>{s.proposedText}</div>
        </>
      )}
      {s.justification && (
        <div style={{ font: '11px Inter, sans-serif', color: '#5a6377', marginTop: 4 }}>"{s.justification}"</div>
      )}

      {mode === 'review' && (
        <div style={{ display: 'flex', gap: 12, marginTop: 8, font: '11px Inter, sans-serif', color: '#5a6377', borderTop: '1px solid #eef1f6', paddingTop: 6 }}>
          <button onClick={() => onSupport(s)} style={{ border: 'none', background: 'none', cursor: 'pointer', color: supported ? '#c8102e' : '#5a6377', fontWeight: supported ? 700 : 400 }}>
            👍 Apoiar · {s.supporters.length}
          </button>
          <button onClick={() => setCommenting(v => !v)} style={{ border: 'none', background: 'none', cursor: 'pointer', color: '#5a6377' }}>
            💬 Comentar · {s.comments.length}
          </button>
        </div>
      )}

      {mode === 'review' && commenting && (
        <div style={{ marginTop: 6 }}>
          {s.comments.map(c => (
            <div key={c.id} style={{ font: '11px Inter, sans-serif', color: '#444', padding: '2px 0' }}>
              <strong>{users.find(u => u.id === c.authorId)?.name ?? '?'}:</strong> {c.text}
            </div>
          ))}
          <textarea value={draft} onChange={e => setDraft(e.target.value)} placeholder="escreva um comentário…"
            style={{ width: '100%', boxSizing: 'border-box', minHeight: 44, border: '1px solid #d6deea', borderRadius: 5, fontSize: 12, padding: 6, marginTop: 4 }} />
          <button
            onClick={() => { if (draft.trim()) { onComment(s, draft.trim()); setDraft('') } }}
            style={{ marginTop: 4, border: 'none', background: '#121d3d', color: '#fff', font: '700 10px Inter, sans-serif', padding: '5px 11px', borderRadius: 5, cursor: 'pointer' }}
          >Enviar comentário</button>
        </div>
      )}

      {mode === 'deliberate' && (
        <div style={{ display: 'flex', gap: 6, marginTop: 8, alignItems: 'center', borderTop: '1px solid #eef1f6', paddingTop: 7 }}>
          <button onClick={() => onDecide(s, 'aceita')} style={{ font: '700 10px Inter, sans-serif', padding: '4px 10px', borderRadius: 5, cursor: 'pointer', background: s.status === 'aceita' ? '#1a7f37' : '#e8f5ec', color: s.status === 'aceita' ? '#fff' : '#1a7f37', border: '1px solid #b6dcc1' }}>✓ Aceitar</button>
          <button onClick={() => onDecide(s, 'rejeitada')} style={{ font: '700 10px Inter, sans-serif', padding: '4px 10px', borderRadius: 5, cursor: 'pointer', background: s.status === 'rejeitada' ? '#c8102e' : '#fbeaec', color: s.status === 'rejeitada' ? '#fff' : '#c8102e', border: '1px solid #eebcc2' }}>✗ Rejeitar</button>
          <span style={{ marginLeft: 'auto', font: '10px Inter, sans-serif', color: '#8a93a6' }}>👍 {s.supporters.length}</span>
        </div>
      )}
    </div>
  )
}
```

- [ ] **Step 2: Commit**

```bash
git add src/components/SuggestionCard.jsx
git commit -m "feat(minuta): componente SuggestionCard (Antes/Depois + apoiar/decidir)"
```

---

## Task 8: Componente `SuggestionPanel`

Painel lateral: thread de sugestões do alvo selecionado + compositor para nova sugestão.

**Files:**
- Create: `src/components/SuggestionPanel.jsx`

- [ ] **Step 1: Criar o componente**

Create `src/components/SuggestionPanel.jsx`:

```jsx
import { useState, useEffect } from 'react'
import SuggestionCard from './SuggestionCard.jsx'

// target: para inciso = { kind:'inciso', chapterId, editId, incisoIndex, originalText, label }
//         para nova seção = { kind:'novaSecao', chapterId, editId(=chapterId), label }
// onAddSuggestion(payload) cria a sugestão; onSupport/onComment refrescam.
export default function SuggestionPanel({ target, suggestions, users, currentUser, onAddSuggestion, onSupport, onComment, onClose }) {
  const incisoTypes = [
    { v: 'editar', label: 'Editar' },
    { v: 'incluir', label: 'Incluir' },
    { v: 'remover', label: 'Remover' },
  ]
  const isNovaSecao = target?.kind === 'novaSecao'
  const [type, setType] = useState(isNovaSecao ? 'incluir-secao' : 'editar')
  const [proposed, setProposed] = useState('')
  const [sectionTitle, setSectionTitle] = useState('')
  const [justification, setJustification] = useState('')

  // Reseta o compositor quando muda o alvo selecionado.
  useEffect(() => {
    setType(isNovaSecao ? 'incluir-secao' : 'editar')
    setProposed(''); setSectionTitle(''); setJustification('')
  }, [target?.editId, target?.incisoIndex, isNovaSecao])

  if (!target) {
    return (
      <div style={{ flex: 1, background: '#f7f9fc', borderRadius: 8, padding: 16, color: 'var(--text-muted)', fontSize: 13 }}>
        Selecione um inciso (ou "+ nova seção") para ver e propor sugestões.
      </div>
    )
  }

  const needsProposed = type !== 'remover'

  function submit() {
    if (needsProposed && !proposed.trim()) return
    if (type === 'incluir-secao' && !sectionTitle.trim()) return
    onAddSuggestion({
      chapterId: target.chapterId,
      targetId: target.editId,
      targetKind: isNovaSecao ? 'secao' : 'inciso',
      incisoIndex: isNovaSecao ? null : target.incisoIndex,
      type,
      originalText: target.originalText ?? '',
      proposedText: needsProposed ? proposed.trim() : '',
      sectionTitle: sectionTitle.trim(),
      justification: justification.trim(),
      authorId: currentUser?.id,
    })
    setProposed(''); setSectionTitle(''); setJustification('')
  }

  return (
    <div style={{ flex: 1, minWidth: 0, background: '#f7f9fc', borderRadius: 8, padding: 12, display: 'flex', flexDirection: 'column', maxHeight: '82vh' }}>
      <div style={{ display: 'flex', alignItems: 'baseline', marginBottom: 8 }}>
        <div style={{ font: '700 11px Inter, sans-serif', color: '#121d3d', textTransform: 'uppercase', letterSpacing: .3 }}>
          {target.label}
          <span style={{ display: 'block', fontWeight: 500, textTransform: 'none', color: '#8a93a6', fontSize: 10.5 }}>
            {suggestions.length} sugestão(ões)
          </span>
        </div>
        <button onClick={onClose} style={{ marginLeft: 'auto', border: 'none', background: 'none', cursor: 'pointer', color: '#8a93a6', fontSize: 16 }} title="Fechar">×</button>
      </div>

      <div style={{ overflow: 'auto', flex: 1 }}>
        {suggestions.length === 0 && (
          <p style={{ color: 'var(--text-muted)', fontSize: 12.5 }}>Ainda sem sugestões neste item. Seja o primeiro.</p>
        )}
        {suggestions.map(s => (
          <SuggestionCard key={s.id} suggestion={s} users={users} currentUser={currentUser} mode="review" onSupport={onSupport} onComment={onComment} />
        ))}
      </div>

      <div style={{ marginTop: 10, background: '#fff', border: '1px solid #e1e7f0', borderRadius: 8, padding: 9 }}>
        {!isNovaSecao && (
          <div style={{ display: 'flex', gap: 4, marginBottom: 6 }}>
            {incisoTypes.map(t => (
              <button key={t.v} onClick={() => setType(t.v)} style={{
                font: '700 9px Inter, sans-serif', padding: '4px 9px', borderRadius: 5, cursor: 'pointer',
                border: '1px solid', borderColor: type === t.v ? '#c8102e' : '#d6deea',
                background: type === t.v ? '#c8102e' : '#fff', color: type === t.v ? '#fff' : '#5a6377',
              }}>{t.label}</button>
            ))}
          </div>
        )}
        {isNovaSecao && (
          <input value={sectionTitle} onChange={e => setSectionTitle(e.target.value)} placeholder="Título da nova seção (ex.: Das Atribuições do Chefe)"
            style={{ width: '100%', boxSizing: 'border-box', border: '1px solid #d6deea', borderRadius: 5, fontSize: 12.5, padding: 6, marginBottom: 6 }} />
        )}
        {needsProposed && (
          <textarea value={proposed} onChange={e => setProposed(e.target.value)}
            placeholder={type === 'incluir' || type === 'incluir-secao' ? 'Texto do novo inciso/seção…' : 'Texto proposto…'}
            style={{ width: '100%', boxSizing: 'border-box', minHeight: 50, border: '1px solid #d6deea', borderRadius: 5, fontSize: 12.5, padding: 6, background: '#fbfcfe' }} />
        )}
        {type === 'remover' && (
          <p style={{ font: '11px Inter, sans-serif', color: '#5a6377', margin: '0 0 4px' }}>Propondo a remoção deste item.</p>
        )}
        <input value={justification} onChange={e => setJustification(e.target.value)} placeholder="Justificativa (opcional)"
          style={{ width: '100%', boxSizing: 'border-box', border: '1px solid #d6deea', borderRadius: 5, fontSize: 12, padding: 6, marginTop: 6 }} />
        <button onClick={submit} style={{ marginTop: 6, border: 'none', background: '#c8102e', color: '#fff', font: '700 10px Inter, sans-serif', padding: '6px 12px', borderRadius: 5, cursor: 'pointer' }}>
          Enviar sugestão
        </button>
      </div>
    </div>
  )
}
```

- [ ] **Step 2: Commit**

```bash
git add src/components/SuggestionPanel.jsx
git commit -m "feat(minuta): componente SuggestionPanel (thread + compositor)"
```

---

## Task 9: Página Fase 1 `MinutaRevisao` (`/minuta/revisao`)

Três colunas: trilha de capítulos · documento (com marcadores) · painel de sugestões. Semeia dois exemplos na primeira carga vazia para a demonstração.

**Files:**
- Create: `src/pages/MinutaRevisao.jsx`

- [ ] **Step 1: Criar a página**

Create `src/pages/MinutaRevisao.jsx`:

```jsx
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
```

- [ ] **Step 2: Registrar a rota temporariamente para teste**

Para verificar antes da Task 11, adicione provisoriamente em `src/App.jsx`: o import `import MinutaRevisao from './pages/MinutaRevisao.jsx'` e a rota `<Route path="/minuta/revisao" element={<MinutaRevisao />} />` dentro de `<Routes>`. (A Task 11 consolida isso com a entrada de menu — não commite o App.jsx aqui ainda.)

- [ ] **Step 3: Verificar manualmente**

Run: `npm run dev -- --port 5173 --strictPort`
Open http://localhost:5173/minuta/revisao. Confirme:
- Trilha de capítulos à esquerda com filtro e badges; um capítulo já vem com badge ≥ 1 (exemplo semeado).
- Clicar num inciso abre o painel à direita com as sugestões (uma "Editar", uma "Remover") e o compositor.
- Trocar de coronel na barra superior e enviar uma sugestão "Editar" → ela aparece na thread com a autoria do coronel selecionado; o badge do inciso/capítulo incrementa.
- "Apoiar" alterna a contagem; "Comentar" adiciona comentário.
- "+ nova seção" abre o compositor de seção (título + texto).
Pare o servidor (Ctrl+C). Reverta a edição provisória do App.jsx (`git checkout src/App.jsx`).

- [ ] **Step 4: Commit**

```bash
git add src/pages/MinutaRevisao.jsx
git commit -m "feat(minuta): página Fase 1 — revisão colaborativa (3 colunas)"
```

---

## Task 10: Página Fase 2 `MinutaDeliberacao` (`/minuta/deliberacao`)

Lista de pendências (itens com sugestões) → fila de revisão guiada (decidir cada sugestão, escrever texto final, aprovar) → gerar `.docx` consolidado.

**Files:**
- Create: `src/pages/MinutaDeliberacao.jsx`

- [ ] **Step 1: Criar a página**

Create `src/pages/MinutaDeliberacao.jsx`:

```jsx
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
```

- [ ] **Step 2: Registrar a rota temporariamente para teste**

Adicione provisoriamente em `src/App.jsx` o import `import MinutaDeliberacao from './pages/MinutaDeliberacao.jsx'` e a rota `<Route path="/minuta/deliberacao" element={<MinutaDeliberacao />} />`. (Não commite o App.jsx aqui; a Task 11 consolida.)

- [ ] **Step 3: Verificar manualmente**

Run: `npm run dev -- --port 5173 --strictPort`
Primeiro abra http://localhost:5173/minuta/revisao e crie 1-2 sugestões (para haver pendências). Depois abra http://localhost:5173/minuta/deliberacao e confirme:
- A lista de pendências mostra os itens com nº de sugestões e status "pendente".
- Clicar num item abre a fila: texto vigente, cada sugestão com Aceitar/Rejeitar, e o campo "Texto final".
- Aceitar uma sugestão de edição preenche o texto final; "Aprovar item e avançar" marca como "decidido", avança a barra de progresso e pula ao próximo pendente.
- "Gerar minuta final (.docx)" baixa um `.docx` que reflete as edições aceitas.
Pare o servidor. Reverta a edição provisória do App.jsx (`git checkout src/App.jsx`).

- [ ] **Step 4: Commit**

```bash
git add src/pages/MinutaDeliberacao.jsx
git commit -m "feat(minuta): página Fase 2 — deliberação do CONDEG (lista → fila → .docx)"
```

---

## Task 11: Rotas e navegação em `App.jsx`

**Files:**
- Modify: `src/App.jsx`

- [ ] **Step 1: Importar ícones e páginas**

In `src/App.jsx`, na linha de import do `lucide-react`, acrescente `MessagesSquare` e `Gavel` à lista de ícones importados:

```js
import {
  Flame, LayoutDashboard, BookOpen, GitCompare,
  Search, Library, ScrollText, Menu, X, Network, MessagesSquare, Gavel
} from 'lucide-react'
```

Logo abaixo do `import MinutaDiagrams from './pages/MinutaDiagrams.jsx'`, adicione:

```js
import MinutaRevisao from './pages/MinutaRevisao.jsx'
import MinutaDeliberacao from './pages/MinutaDeliberacao.jsx'
```

- [ ] **Step 2: Acrescentar itens ao `NAV`**

No array `NAV`, logo após a linha do item `/minuta-diagramas`, insira:

```js
  { to: '/minuta/revisao', icon: MessagesSquare, label: 'Revisão CONDEG' },
  { to: '/minuta/deliberacao', icon: Gavel, label: 'Deliberação CONDEG' },
```

- [ ] **Step 3: Acrescentar as rotas**

Dentro de `<Routes>`, logo após `<Route path="/minuta-diagramas" element={<MinutaDiagrams />} />`, adicione:

```jsx
          <Route path="/minuta/revisao" element={<MinutaRevisao />} />
          <Route path="/minuta/deliberacao" element={<MinutaDeliberacao />} />
```

- [ ] **Step 4: Verificar manualmente**

Run: `npm run dev -- --port 5173 --strictPort`
Open http://localhost:5173 e confirme no menu lateral as novas abas "Revisão CONDEG" e "Deliberação CONDEG"; clique em cada uma e confirme que carregam as telas das Tasks 9 e 10. Pare o servidor.

- [ ] **Step 5: Commit**

```bash
git add src/App.jsx
git commit -m "feat(minuta): rotas e navegação da revisão/deliberação do CONDEG"
```

---

## Self-review do plano (já aplicado)

- **Cobertura da spec:** camada de dados isolada (Task 1) · alvos/filtro por capítulo (Task 2, 6, 9) · janela de sugestão = painel lateral (Task 8, 9) · Antes/Depois (Task 7) · colaboração com autoria/apoiar/comentar (Task 1, 7, 9) · seções/incisos incluir/editar/remover (Task 8) · deliberação lista→fila + texto final + aprovar (Task 10) · minuta final .docx (Task 3, 4, 10) · identidade simulada (Task 5, 9, 10) · rotas/nav (Task 11). ✔
- **Sem placeholders:** todo passo de código traz o código completo. ✔
- **Consistência de tipos:** `suggestionsStore` (Task 1) usa `targetId`, `incisoIndex`, `status` consumidos igualmente em `minutaConsolidation` (Task 3), `MinutaRevisao` (Task 9) e `MinutaDeliberacao` (Task 10); `buildTargets` (Task 2) e `itemKeyOf` reusados nas Tasks 9 e 10; `buildMinutaBlob` (Task 4) com a mesma assinatura usada nas Tasks 4 e 10. ✔

## Notas de integração futura (backend — fora deste plano)

Quando o backend (projeto apartado) existir, criar `apiBackend` com a mesma assinatura de `createSuggestionsStore` (chamadas `fetch`, usuário vindo da sessão autenticada) e trocar a instância exportada em `suggestionsStore.js`. Nenhuma tela muda. O modelo da Task 1 é a referência para os endpoints/tabelas.
