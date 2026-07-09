// Camada de dados ISOLADA do fluxo de revisão colaborativa da minuta de RI.
// API assíncrona (Promise) no formato de um backend REST. Hoje persiste em
// localStorage; quando o backend real existir, basta criar outra implementação com
// a MESMA assinatura (via createSuggestionsStore) e trocar a instância exportada —
// as telas não mudam.

const STORAGE_KEY = 'cbm.minuta.revisao.v1'
// Exportada para o logout (auth.jsx) limpar só as chaves do protótipo, nunca localStorage.clear().
export const PROTOTYPE_STORAGE_KEY = STORAGE_KEY

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
