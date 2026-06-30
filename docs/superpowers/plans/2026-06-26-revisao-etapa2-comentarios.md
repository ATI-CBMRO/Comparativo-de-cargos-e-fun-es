# Revisão Colaborativa — Etapa 2: Documento + Comentários por inciso — Plano

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development ou superpowers:executing-plans. Steps usam checkbox (`- [ ]`).

**Goal:** Na rota protegida `/revisao`, renderizar a minuta como documento (capítulo → artigo → incisos) com a trilha de balões na margem direita; ao clicar num balão, abrir a janela central (modal) com as sugestões daquele dispositivo, onde o participante cria sugestões, vê as de todos e dá 👍 — tudo em tempo real via Firestore.

**Architecture:** A página lê `database/minuta_structure.json` (mesma fonte do wizard) e articula com `buildArticles`. Cada inciso e cada caput vira um "dispositivo" endereçado por `dispositivoId` (Etapa 1). As sugestões ficam na coleção `suggestions` do Firestore, assinadas com `onSnapshot` (tempo real). Contagem por dispositivo é derivada em memória (conjunto pequeno).

**Tech Stack:** React 18, Firestore (modular SDK), `buildArticles`/`dispositivoId` já existentes, `node --test`.

## Global Constraints

- UI em Português (Brasil); seguir padrões do projeto (inline styles como no `MinutaWizard.jsx`, CSS extra em `src/index.css`).
- Nenhum segredo no código; Firestore acessado via `db` de `src/lib/firebase.js`.
- `minuta_structure.json` congelado durante a revisão (não reexecutar a pipeline).
- Commits pequenos, mensagens `tipo: descrição`.

---

### Task 1: Agrupar sugestões por dispositivo (lógica pura + teste)

**Files:**
- Create: `src/lib/reviewGroup.js`
- Test: `src/lib/reviewGroup.test.js`

**Interfaces:**
- Produces:
  - `groupByDispositivo(suggestions: Array<{dispositivoId}>) => Map<string, Array>` — agrupa por `dispositivoId`, preservando a ordem de entrada.
  - `countByDispositivo(suggestions) => Map<string, number>` — contagem por `dispositivoId`.

- [ ] **Step 1: Escrever o teste que falha**

`src/lib/reviewGroup.test.js`:
```js
import { test } from 'node:test'
import assert from 'node:assert/strict'
import { groupByDispositivo, countByDispositivo } from './reviewGroup.js'

const sugs = [
  { id: 'a', dispositivoId: 'cot#0', texto: 'x' },
  { id: 'b', dispositivoId: 'cot#0', texto: 'y' },
  { id: 'c', dispositivoId: 'cot#caput', texto: 'z' },
]

test('groupByDispositivo agrupa por dispositivoId', () => {
  const g = groupByDispositivo(sugs)
  assert.equal(g.get('cot#0').length, 2)
  assert.equal(g.get('cot#caput').length, 1)
  assert.equal(g.get('cot#0')[0].id, 'a')
})

test('countByDispositivo conta por dispositivoId', () => {
  const c = countByDispositivo(sugs)
  assert.equal(c.get('cot#0'), 2)
  assert.equal(c.get('cot#caput'), 1)
  assert.equal(c.get('inexistente'), undefined)
})
```

- [ ] **Step 2: Rodar e confirmar falha**

Run: `node --test src/lib/reviewGroup.test.js`
Expected: FALHA (módulo inexistente).

- [ ] **Step 3: Implementar `src/lib/reviewGroup.js`**

```js
// Agrupamento/contagem de sugestões por dispositivoId (lógica pura, sem React/Firebase).
export function groupByDispositivo(suggestions) {
  const map = new Map()
  for (const s of suggestions) {
    const arr = map.get(s.dispositivoId)
    if (arr) arr.push(s)
    else map.set(s.dispositivoId, [s])
  }
  return map
}

export function countByDispositivo(suggestions) {
  const map = new Map()
  for (const s of suggestions) {
    map.set(s.dispositivoId, (map.get(s.dispositivoId) ?? 0) + 1)
  }
  return map
}
```

- [ ] **Step 4: Rodar e confirmar que passa**

Run: `node --test src/lib/reviewGroup.test.js`
Expected: PASS (2 testes).

- [ ] **Step 5: Commit**

```bash
git add src/lib/reviewGroup.js src/lib/reviewGroup.test.js
git commit -m "feat: agrupamento/contagem de sugestões por dispositivo (lógica pura)"
```

---

### Task 2: Camada de dados do Firestore (`reviewData.js`)

**Files:**
- Create: `src/lib/reviewData.js`

**Interfaces:**
- Consumes: `db` de `src/lib/firebase.js`.
- Produces:
  - `subscribeSuggestions(onChange: (suggestions: Array) => void) => () => void` — assina a coleção `suggestions` ordenada por `criadoEm` asc; retorna função de cancelamento. Cada item: `{ id, dispositivoId, dispositivoLabelSnapshot, trechoSnapshot, autorUid, autorNome, texto, criadoEm, curtidoPor: string[] }`.
  - `addSuggestion({ dispositivoId, dispositivoLabelSnapshot, trechoSnapshot, texto, autor: {uid, nome} }) => Promise<void>`.
  - `toggleLike(suggestion, uid) => Promise<void>` — adiciona/remove `uid` de `curtidoPor`.
  - `deleteSuggestion(id) => Promise<void>`.

- [ ] **Step 1: Implementar `src/lib/reviewData.js`**

```js
import {
  collection, addDoc, deleteDoc, doc, updateDoc,
  onSnapshot, query, orderBy, serverTimestamp,
  arrayUnion, arrayRemove,
} from 'firebase/firestore'
import { db } from './firebase.js'

const COL = 'suggestions'

export function subscribeSuggestions(onChange) {
  const q = query(collection(db, COL), orderBy('criadoEm', 'asc'))
  return onSnapshot(q, (snap) => {
    const list = snap.docs.map(d => ({ id: d.id, ...d.data() }))
    onChange(list)
  })
}

export async function addSuggestion({ dispositivoId, dispositivoLabelSnapshot, trechoSnapshot, texto, autor }) {
  await addDoc(collection(db, COL), {
    dispositivoId,
    dispositivoLabelSnapshot,
    trechoSnapshot,
    texto: texto.trim(),
    autorUid: autor.uid,
    autorNome: autor.nome,
    curtidoPor: [],
    criadoEm: serverTimestamp(),
  })
}

export async function toggleLike(suggestion, uid) {
  const jaCurtiu = (suggestion.curtidoPor ?? []).includes(uid)
  await updateDoc(doc(db, COL, suggestion.id), {
    curtidoPor: jaCurtiu ? arrayRemove(uid) : arrayUnion(uid),
  })
}

export async function deleteSuggestion(id) {
  await deleteDoc(doc(db, COL, id))
}
```

- [ ] **Step 2: Verificar compilação**

Run: `npm run build`
Expected: build sem erros. (Sem uso ainda; validação real na Task 4.)

- [ ] **Step 3: Commit**

```bash
git add src/lib/reviewData.js
git commit -m "feat: camada de dados Firestore para sugestões (assinar/criar/curtir/excluir)"
```

---

### Task 3: Janela do dispositivo (`RevisaoModal.jsx`)

**Files:**
- Create: `src/components/RevisaoModal.jsx`
- Modify: `src/index.css` (estilos `.rev-modal*`)

**Interfaces:**
- Consumes: nenhuma lib externa além de React + `lucide-react`.
- Produces: `<RevisaoModal dispositivo suggestions user onAdd onToggleLike onDelete onClose />` (default export), onde:
  - `dispositivo`: `{ id, label, trecho }`.
  - `suggestions`: `Array` (já filtrada para este dispositivo).
  - `user`: `{ uid, nome, role }`.
  - `onAdd(texto)`, `onToggleLike(suggestion)`, `onDelete(suggestion)`, `onClose()`.

- [ ] **Step 1: Implementar `src/components/RevisaoModal.jsx`**

```jsx
import { useState } from 'react'
import { X, ThumbsUp, Trash2 } from 'lucide-react'

function formataData(criadoEm) {
  if (!criadoEm?.toDate) return ''
  return criadoEm.toDate().toLocaleString('pt-BR', {
    day: '2-digit', month: '2-digit', hour: '2-digit', minute: '2-digit',
  })
}

export default function RevisaoModal({ dispositivo, suggestions, user, onAdd, onToggleLike, onDelete, onClose }) {
  const [texto, setTexto] = useState('')
  const [enviando, setEnviando] = useState(false)

  const enviar = async (e) => {
    e.preventDefault()
    if (!texto.trim()) return
    setEnviando(true)
    try { await onAdd(texto); setTexto('') }
    finally { setEnviando(false) }
  }

  return (
    <div className="rev-modal-backdrop" onClick={onClose}>
      <div className="rev-modal" onClick={e => e.stopPropagation()}>
        <div className="rev-modal-head">
          <div>
            <div className="rev-modal-label">{dispositivo.label}</div>
            <div className="rev-modal-trecho">{dispositivo.trecho}</div>
          </div>
          <button className="rev-modal-x" onClick={onClose} aria-label="Fechar"><X size={18} /></button>
        </div>

        <div className="rev-modal-list">
          {suggestions.length === 0 && (
            <p className="rev-modal-vazio">Ainda não há sugestões para este dispositivo. Seja o primeiro.</p>
          )}
          {suggestions.map(s => {
            const curtiu = (s.curtidoPor ?? []).includes(user.uid)
            const podeExcluir = s.autorUid === user.uid || user.role === 'admin'
            return (
              <div key={s.id} className="rev-sug">
                <div className="rev-sug-meta">
                  <span className="rev-sug-autor">{s.autorNome}</span>
                  <span className="rev-sug-data">{formataData(s.criadoEm)}</span>
                </div>
                <div className="rev-sug-texto">{s.texto}</div>
                <div className="rev-sug-acoes">
                  <button className={`rev-like${curtiu ? ' on' : ''}`} onClick={() => onToggleLike(s)}>
                    <ThumbsUp size={14} /> {(s.curtidoPor ?? []).length || ''}
                  </button>
                  {podeExcluir && (
                    <button className="rev-del" onClick={() => onDelete(s)} title="Excluir">
                      <Trash2 size={14} />
                    </button>
                  )}
                </div>
              </div>
            )
          })}
        </div>

        <form className="rev-modal-form" onSubmit={enviar}>
          <textarea className="rev-modal-input" value={texto} onChange={e => setTexto(e.target.value)}
            placeholder="Escreva sua sugestão para este dispositivo…" rows={3} />
          <button className="rev-modal-enviar" type="submit" disabled={enviando || !texto.trim()}>
            {enviando ? 'Enviando…' : 'Enviar sugestão'}
          </button>
        </form>
      </div>
    </div>
  )
}
```

- [ ] **Step 2: Adicionar estilos ao fim de `src/index.css`**

```css
/* ===== Revisão: janela do dispositivo (modal) ===== */
.rev-modal-backdrop { position: fixed; inset: 0; background: rgba(18,29,61,.45); display: flex;
  align-items: center; justify-content: center; padding: 20px; z-index: 50; }
.rev-modal { width: 100%; max-width: 540px; max-height: 86vh; background: #fff; border-radius: 12px;
  display: flex; flex-direction: column; overflow: hidden; box-shadow: 0 18px 50px rgba(0,0,0,.3); }
.rev-modal-head { display: flex; gap: 12px; padding: 16px 18px; border-bottom: 1px solid #e3e8f0; background: #f7f9fc; }
.rev-modal-label { font-weight: 700; color: #121d3d; font-size: 14px; }
.rev-modal-trecho { color: #5a667f; font-size: 13px; margin-top: 2px; }
.rev-modal-x { margin-left: auto; background: none; border: none; cursor: pointer; color: #5a667f; align-self: flex-start; }
.rev-modal-list { padding: 12px 18px; overflow: auto; flex: 1; display: flex; flex-direction: column; gap: 10px; }
.rev-modal-vazio { color: #8a93a8; font-size: 13px; text-align: center; padding: 16px 0; }
.rev-sug { border: 1px solid #e3e8f0; border-radius: 8px; padding: 10px 12px; }
.rev-sug-meta { display: flex; justify-content: space-between; align-items: baseline; }
.rev-sug-autor { font-weight: 600; color: #121d3d; font-size: 13px; }
.rev-sug-data { color: #8a93a8; font-size: 12px; }
.rev-sug-texto { margin: 4px 0 8px; font-size: 14px; color: #1a1a1a; }
.rev-sug-acoes { display: flex; gap: 8px; align-items: center; }
.rev-like { display: inline-flex; align-items: center; gap: 4px; border: 1px solid #c5cee0; background: #fff;
  border-radius: 14px; padding: 3px 10px; font-size: 12.5px; cursor: pointer; color: #3a4866; }
.rev-like.on { background: #fdecee; border-color: #f3b4bd; color: #c8102e; }
.rev-del { border: none; background: none; cursor: pointer; color: #b0b8c8; }
.rev-del:hover { color: #c8102e; }
.rev-modal-form { border-top: 1px solid #e3e8f0; padding: 12px 18px; display: flex; flex-direction: column; gap: 8px; }
.rev-modal-input { border: 1px solid #c5cee0; border-radius: 8px; padding: 10px; font-size: 14px; resize: vertical; font-family: inherit; }
.rev-modal-enviar { align-self: flex-end; background: #c8102e; color: #fff; border: none; border-radius: 8px;
  padding: 9px 18px; font-weight: 700; font-size: 14px; cursor: pointer; }
.rev-modal-enviar:disabled { opacity: .5; cursor: default; }
```

- [ ] **Step 3: Verificar compilação**

Run: `npm run build` → Expected: sem erros.

- [ ] **Step 4: Commit**

```bash
git add src/components/RevisaoModal.jsx src/index.css
git commit -m "feat: janela (modal) de sugestões do dispositivo com curtir/excluir"
```

---

### Task 4: Página `/revisao` — documento + trilha de balões

**Files:**
- Modify: `src/pages/Revisao.jsx` (substitui o placeholder da Etapa 1)
- Modify: `src/index.css` (estilos `.rev-doc*`, `.rev-line`, `.rev-rail*`)

**Interfaces:**
- Consumes: `useAuth()`, `buildArticles`/`articleLabel`/`romanize` de `minutaArticles.js`, `incisoDispositivoId`/`caputDispositivoId` de `dispositivoId.js`, `groupByDispositivo`/`countByDispositivo` de `reviewGroup.js`, `subscribeSuggestions`/`addSuggestion`/`toggleLike`/`deleteSuggestion` de `reviewData.js`, `RevisaoModal`.
- Produces: a página `/revisao` completa.

- [ ] **Step 1: Implementar `src/pages/Revisao.jsx`**

```jsx
import { useEffect, useMemo, useState } from 'react'
import { MessageSquare } from 'lucide-react'
import { useAuth } from '../lib/auth.jsx'
import { buildArticles, articleLabel, romanize } from '../lib/minutaArticles.js'
import { incisoDispositivoId, caputDispositivoId } from '../lib/dispositivoId.js'
import { groupByDispositivo, countByDispositivo } from '../lib/reviewGroup.js'
import {
  subscribeSuggestions, addSuggestion, toggleLike, deleteSuggestion,
} from '../lib/reviewData.js'
import RevisaoModal from '../components/RevisaoModal.jsx'

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

export default function Revisao() {
  const { user } = useAuth()
  const [data, setData] = useState(null)
  const [erro, setErro] = useState(null)
  const [suggestions, setSuggestions] = useState([])
  const [aberto, setAberto] = useState(null) // { id, label, trecho }

  useEffect(() => {
    fetch('/database/minuta_structure.json')
      .then(r => { if (!r.ok) throw new Error(r.status); return r.json() })
      .then(setData)
      .catch(() => setErro('Não foi possível carregar a minuta.'))
  }, [])

  useEffect(() => subscribeSuggestions(setSuggestions), [])

  const counts = useMemo(() => countByDispositivo(suggestions), [suggestions])
  const grupos = useMemo(() => groupByDispositivo(suggestions), [suggestions])
  const articles = useMemo(() => (data ? buildArticles(data) : []), [data])

  const abrir = (id, label, trecho) => setAberto({ id, label, trecho })

  const handleAdd = (texto) => addSuggestion({
    dispositivoId: aberto.id,
    dispositivoLabelSnapshot: aberto.label,
    trechoSnapshot: aberto.trecho,
    texto,
    autor: { uid: user.uid, nome: user.nome },
  })

  if (erro) return <div style={{ padding: 32, color: '#c8102e' }}>{erro}</div>
  if (!data) return <div style={{ padding: 32 }}>Carregando minuta…</div>

  return (
    <>
      <div className="page-header">
        <div className="page-header-left">
          <h2 className="page-title">Revisão da Minuta</h2>
          <p className="page-subtitle">
            Clique no balão à direita de cada dispositivo para ver e enviar sugestões.
            As sugestões de todos ficam visíveis.
          </p>
        </div>
      </div>

      <div className="page-body">
        <div className="rev-doc">
          {articles.map(art => {
            const caputId = caputDispositivoId(art.editId)
            const caputLabel = `${articleLabel(art.number)}`
            return (
              <div key={art.number} className="rev-art">
                {art.chapterTitle && (
                  <p className="rev-chapter">CAPÍTULO {romanize(art.chapterNumber)}<br />{art.chapterTitle}</p>
                )}
                {art.sectionTitle && (
                  <p className="rev-section">Seção {romanize(art.sectionNumber)} — {art.sectionTitle}</p>
                )}

                <div className="rev-line">
                  <span className="rev-text" style={{ textIndent: art.incisos.length ? 0 : '1.25em' }}>
                    <strong>{articleLabel(art.number)}</strong> {art.caput}
                  </span>
                  <Rail count={counts.get(caputId)} onClick={() => abrir(caputId, caputLabel, art.caput)} />
                </div>

                {art.incisos.map((inc, i) => {
                  const id = incisoDispositivoId(inc.editId, inc.index)
                  const label = `${articleLabel(art.number)}, inciso ${romanize(i + 1)}`
                  return (
                    <div className="rev-line rev-inciso" key={`${id}`}>
                      <span className="rev-text"><strong>{romanize(i + 1)} -</strong> {inc.text}</span>
                      <Rail count={counts.get(id)} onClick={() => abrir(id, label, inc.text)} />
                    </div>
                  )
                })}
              </div>
            )
          })}
        </div>
      </div>

      {aberto && (
        <RevisaoModal
          dispositivo={aberto}
          suggestions={grupos.get(aberto.id) ?? []}
          user={user}
          onAdd={handleAdd}
          onToggleLike={(s) => toggleLike(s, user.uid)}
          onDelete={(s) => deleteSuggestion(s.id)}
          onClose={() => setAberto(null)}
        />
      )}
    </>
  )
}
```

- [ ] **Step 2: Adicionar estilos ao fim de `src/index.css`**

```css
/* ===== Revisão: documento + trilha de balões ===== */
.rev-doc { border: 1px solid var(--border-card); border-radius: 8px; background: #fff; padding: 20px 8px 20px 24px;
  font-family: Georgia, 'Times New Roman', serif; font-size: 14px; line-height: 1.7; color: #1a1a1a; max-width: 900px; }
.rev-art { margin-bottom: 8px; }
.rev-chapter { text-align: center; font-weight: 700; margin: 20px 40px 6px; }
.rev-section { text-align: center; font-weight: 600; font-style: italic; margin: 10px 40px 6px; }
.rev-line { display: flex; align-items: flex-start; gap: 6px; padding: 2px 0; border-radius: 6px; }
.rev-line:hover { background: rgba(18,29,61,.035); }
.rev-inciso { padding-left: 24px; }
.rev-text { flex: 1; text-align: justify; }
.rev-rail { flex: 0 0 34px; display: flex; justify-content: center; border-left: 1px solid #e7ebf3; }
.rev-mark { width: 26px; height: 22px; display: inline-flex; align-items: center; justify-content: center;
  border: none; background: none; border-radius: 11px; cursor: pointer; font-size: 12px; font-weight: 700;
  color: #c3cad8; font-family: Inter, sans-serif; }
.rev-line:hover .rev-mark { color: #8a93a8; }
.rev-mark.has { background: #c8102e; color: #fff; }
```

- [ ] **Step 3: Atualizar as Security Rules para permitir 👍 (curtir sugestão de outro)**

Editar `firestore.rules`: substituir a linha de `update, delete` de `suggestions` por regras que permitam (a) o autor alterar/excluir a própria e (b) qualquer membro alterar **apenas** o campo `curtidoPor`:

```
    match /suggestions/{id} {
      allow read: if isMember();
      allow create: if isMember() && request.resource.data.autorUid == request.auth.uid;
      allow delete: if isMember()
        && (resource.data.autorUid == request.auth.uid
            || isAdmin());
      allow update: if isMember()
        && (resource.data.autorUid == request.auth.uid
            || request.resource.data.diff(resource.data).affectedKeys().hasOnly(['curtidoPor']));
    }
```

> Nota: `hasOnly(['curtidoPor'])` permite a qualquer membro togglar curtidas sem tocar no resto. Para um grupo convidado e pequeno, é aceitável na v1.

- [ ] **Step 4: Verificação manual ponta a ponta**

Pré-requisito: republicar `firestore.rules` no console (ver `docs/FIREBASE_SETUP.md`).
Run: `npm run dev` e no navegador, logado:
- Abrir `/revisao` → Expected: a minuta aparece como documento, com um balão cinza à direita de cada artigo/inciso.
- Clicar num balão → abre a janela central; digitar uma sugestão e **Enviar** → ela aparece na lista e o balão fica vermelho com "1".
- Recarregar a página → a sugestão persiste (veio do Firestore).
- Clicar em 👍 → contador muda; clicar de novo → volta.
- Excluir a própria sugestão → some da lista e o balão zera.
- (Com 2 usuários/2 navegadores) a sugestão de um aparece para o outro em tempo real.

- [ ] **Step 5: Commit**

```bash
git add src/pages/Revisao.jsx src/index.css firestore.rules
git commit -m "feat: página /revisao com documento, trilha de balões e sugestões em tempo real"
```

---

## Self-Review (preenchido)

**Cobertura da spec (Etapa 2):** documento reaproveitando `minuta_structure.json`/`buildArticles` (Task 4); trilha de balões discreta na margem direita (Task 4 + CSS); janela central modal (Task 3); criar/listar/curtir/excluir sugestões em tempo real (Tasks 2 e 4); todos veem todos com autoria (modal + regras de leitura); endereço estável por inciso/caput (`dispositivoId`, Etapa 1). ✔

**Fora de escopo (Etapa 3):** marcar relevante/descartar, texto final, painel de progresso e extensão das regras para `adminStatus`.

**Placeholders:** nenhum. Passos manuais do console são intencionais e referenciam `docs/FIREBASE_SETUP.md`.

**Consistência de nomes:** `reviewData` expõe `subscribeSuggestions/addSuggestion/toggleLike/deleteSuggestion`; `reviewGroup` expõe `groupByDispositivo/countByDispositivo`; `dispositivoId` expõe `incisoDispositivoId/caputDispositivoId` — todos consumidos com esses exatos nomes em `Revisao.jsx`. O objeto de sugestão usa `curtidoPor` (array) de ponta a ponta (data, modal, regras).
```
