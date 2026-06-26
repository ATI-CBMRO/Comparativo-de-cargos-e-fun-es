# Revisão Colaborativa — Etapa 3: Curadoria do admin + texto final — Plano

> **For agentic workers:** REQUIRED SUB-SKILL: superpowers:subagent-driven-development ou superpowers:executing-plans. Steps usam checkbox (`- [ ]`).

**Goal:** Dar ao admin, dentro da janela do dispositivo, os controles para marcar cada sugestão como *relevante* ou *descartada* e escrever/salvar o **texto final** do dispositivo (com status em aberto/fechado); exibir o texto final (somente leitura) aos participantes; e mostrar um painel de progresso (quantos dispositivos fechados).

**Architecture:** A marcação fica no campo `adminStatus` de cada doc em `suggestions`. O texto final fica em `finalTexts/{dispositivoId}` (`{ texto, status, atualizadoPor, atualizadoEm }`), assinado em tempo real. As Security Rules ganham: admin pode alterar `adminStatus`; `finalTexts` é escrito só por admin (já estava).

**Tech Stack:** React 18, Firestore modular, componentes da Etapa 2.

## Global Constraints
- UI em PT-BR; padrões do projeto; sem segredos no código; commits pequenos.
- `adminStatus` ausente é tratado como `'pendente'`.

---

### Task 1: Dados — adminStatus e finalTexts (`reviewData.js`)

**Files:** Modify: `src/lib/reviewData.js`

**Interfaces (produces, somado ao que já existe):**
- `setAdminStatus(suggestionId, status) => Promise<void>` — grava `adminStatus` ('pendente'|'relevante'|'descartada').
- `subscribeFinalTexts(onChange, onError?) => () => void` — assina a coleção `finalTexts`; `onChange(Map<dispositivoId, {texto,status,atualizadoPor,atualizadoEm}>)`.
- `saveFinalText(dispositivoId, { texto, status, autor }) => Promise<void>` — `setDoc` (merge) em `finalTexts/{dispositivoId}`.

- [ ] **Step 1: Editar `src/lib/reviewData.js`**

Adicionar aos imports existentes `getDocs`? Não — usar `setDoc` e `collection`/`onSnapshot` já importados; importar `setDoc`:
```js
// no topo, juntar setDoc à lista de imports de 'firebase/firestore'
```
Acrescentar as funções:
```js
const COL_FINAL = 'finalTexts'

export async function setAdminStatus(suggestionId, status) {
  await updateDoc(doc(db, COL, suggestionId), { adminStatus: status })
}

export function subscribeFinalTexts(onChange, onError) {
  return onSnapshot(collection(db, COL_FINAL),
    (snap) => {
      const map = new Map()
      snap.docs.forEach(d => map.set(d.id, d.data()))
      onChange(map)
    },
    (err) => { if (onError) onError(err) },
  )
}

export async function saveFinalText(dispositivoId, { texto, status, autor }) {
  await setDoc(doc(db, COL_FINAL, dispositivoId), {
    texto: texto.trim(),
    status,
    atualizadoPor: autor.nome,
    atualizadoEm: serverTimestamp(),
  }, { merge: true })
}
```

- [ ] **Step 2: Build** — Run: `npm run build` → Expected: sem erros.
- [ ] **Step 3: Commit**
```bash
git add src/lib/reviewData.js
git commit -m "feat: dados de curadoria (adminStatus) e texto final (finalTexts)"
```

---

### Task 2: Modal com curadoria do admin (`RevisaoModal.jsx`)

**Files:** Modify: `src/components/RevisaoModal.jsx`, `src/index.css`

**Interfaces (novas props):**
- `finalText`: `{ texto, status } | null`
- `onSetStatus(suggestion, status)`
- `onSaveFinal(texto, status)`

- [ ] **Step 1: Editar `src/components/RevisaoModal.jsx`** — substituir o componente por:

```jsx
import { useState, useEffect } from 'react'
import { X, ThumbsUp, Trash2, Check, Ban } from 'lucide-react'

function formataData(criadoEm) {
  if (!criadoEm?.toDate) return ''
  return criadoEm.toDate().toLocaleString('pt-BR', {
    day: '2-digit', month: '2-digit', hour: '2-digit', minute: '2-digit',
  })
}

export default function RevisaoModal({
  dispositivo, suggestions, finalText, user,
  onAdd, onToggleLike, onDelete, onSetStatus, onSaveFinal, onClose,
}) {
  const isAdmin = user.role === 'admin'
  const [texto, setTexto] = useState('')
  const [enviando, setEnviando] = useState(false)
  const [final, setFinal] = useState(finalText?.texto ?? '')

  useEffect(() => { setFinal(finalText?.texto ?? '') }, [finalText, dispositivo.id])

  const enviar = async (e) => {
    e.preventDefault()
    if (!texto.trim()) return
    setEnviando(true)
    try { await onAdd(texto); setTexto('') }
    finally { setEnviando(false) }
  }

  const statusClasse = (s) => {
    const st = s.adminStatus ?? 'pendente'
    if (st === 'relevante') return ' rel'
    if (st === 'descartada') return ' desc'
    return ''
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
            <p className="rev-modal-vazio">Ainda não há sugestões para este dispositivo.</p>
          )}
          {suggestions.map(s => {
            const curtiu = (s.curtidoPor ?? []).includes(user.uid)
            const podeExcluir = s.autorUid === user.uid || isAdmin
            const st = s.adminStatus ?? 'pendente'
            return (
              <div key={s.id} className={`rev-sug${statusClasse(s)}`}>
                <div className="rev-sug-meta">
                  <span className="rev-sug-autor">{s.autorNome}</span>
                  <span className="rev-sug-data">{formataData(s.criadoEm)}</span>
                </div>
                <div className="rev-sug-texto">{s.texto}</div>
                <div className="rev-sug-acoes">
                  <button className={`rev-like${curtiu ? ' on' : ''}`} onClick={() => onToggleLike(s)}>
                    <ThumbsUp size={14} /> {(s.curtidoPor ?? []).length || ''}
                  </button>
                  {st !== 'pendente' && (
                    <span className={`rev-badge ${st}`}>{st === 'relevante' ? 'Relevante' : 'Descartada'}</span>
                  )}
                  {isAdmin && (
                    <span className="rev-admin-acoes">
                      <button className="rev-mini rel" title="Marcar relevante"
                        onClick={() => onSetStatus(s, st === 'relevante' ? 'pendente' : 'relevante')}><Check size={14} /></button>
                      <button className="rev-mini desc" title="Descartar"
                        onClick={() => onSetStatus(s, st === 'descartada' ? 'pendente' : 'descartada')}><Ban size={14} /></button>
                    </span>
                  )}
                  {podeExcluir && (
                    <button className="rev-del" onClick={() => onDelete(s)} title="Excluir"><Trash2 size={14} /></button>
                  )}
                </div>
              </div>
            )
          })}
        </div>

        {/* Texto final */}
        {(isAdmin || finalText) && (
          <div className="rev-final">
            <div className="rev-final-head">
              ✍️ Texto final do dispositivo
              {finalText?.status === 'fechado' && <span className="rev-badge fechado">✔ Fechado</span>}
            </div>
            {isAdmin ? (
              <>
                <textarea className="rev-modal-input" value={final} onChange={e => setFinal(e.target.value)}
                  placeholder="Escreva o texto final consolidado…" rows={3} />
                <div className="rev-final-acoes">
                  <button className="rev-final-btn" onClick={() => onSaveFinal(final, 'em_aberto')}>Salvar rascunho</button>
                  <button className="rev-final-btn fechar" onClick={() => onSaveFinal(final, 'fechado')}>Salvar e fechar</button>
                </div>
              </>
            ) : (
              <p className="rev-final-ro">{finalText.texto}</p>
            )}
          </div>
        )}

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
/* ===== Revisão: curadoria do admin ===== */
.rev-sug.rel { border-color: #abdcbd; background: #f1faf4; }
.rev-sug.desc { opacity: .6; }
.rev-sug.desc .rev-sug-texto { text-decoration: line-through; }
.rev-badge { font-size: 11px; border-radius: 10px; padding: 1px 8px; font-weight: 700; }
.rev-badge.relevante { background: #e9f6ee; color: #1d6b3a; }
.rev-badge.descartada { background: #f3f4f6; color: #6b7280; }
.rev-badge.fechado { background: #e9f6ee; color: #1d6b3a; margin-left: 8px; }
.rev-admin-acoes { display: inline-flex; gap: 4px; }
.rev-mini { border: 1px solid #c5cee0; background: #fff; border-radius: 6px; padding: 2px 6px; cursor: pointer; display: inline-flex; }
.rev-mini.rel:hover { border-color: #1d6b3a; color: #1d6b3a; }
.rev-mini.desc:hover { border-color: #c8102e; color: #c8102e; }
.rev-final { border-top: 1px solid #e3e8f0; padding: 12px 18px; background: #fbfcfe; }
.rev-final-head { font-size: 13px; font-weight: 700; color: #121d3d; margin-bottom: 6px; display: flex; align-items: center; }
.rev-final-acoes { display: flex; gap: 8px; justify-content: flex-end; margin-top: 8px; }
.rev-final-btn { border: 1px solid #c5cee0; background: #fff; border-radius: 8px; padding: 7px 14px; font-size: 13px; cursor: pointer; }
.rev-final-btn.fechar { background: #c8102e; color: #fff; border-color: #c8102e; font-weight: 700; }
.rev-final-ro { font-size: 14px; color: #1a1a1a; background: #f1faf4; border: 1px solid #abdcbd; border-radius: 8px; padding: 8px 10px; margin: 0; }
```

- [ ] **Step 3: Build** → Expected: sem erros.
- [ ] **Step 4: Commit**
```bash
git add src/components/RevisaoModal.jsx src/index.css
git commit -m "feat: curadoria do admin no modal (relevante/descartar + texto final)"
```

---

### Task 3: Página `/revisao` — ligar curadoria + progresso

**Files:** Modify: `src/pages/Revisao.jsx`, `src/index.css`

- [ ] **Step 1: Editar `src/pages/Revisao.jsx`**

Adicionar imports:
```jsx
import {
  subscribeSuggestions, addSuggestion, toggleLike, deleteSuggestion,
  setAdminStatus, subscribeFinalTexts, saveFinalText,
} from '../lib/reviewData.js'
```
Adicionar estado e assinatura dos textos finais (após a assinatura de sugestões):
```jsx
  const [finals, setFinals] = useState(new Map())
  useEffect(() => subscribeFinalTexts(setFinals, (e) => console.error('Erro finalTexts:', e)), [])
```
Calcular progresso (após `articles`):
```jsx
  const fechados = useMemo(() => {
    let n = 0
    finals.forEach(f => { if (f.status === 'fechado') n += 1 })
    return n
  }, [finals])
```
No cabeçalho (`page-subtitle`), abaixo do parágrafo, inserir o painel:
```jsx
          <p className="rev-progresso">{fechados} dispositivo(s) com texto final fechado.</p>
```
No `<Rail>` de cada linha, passar se está fechado. Atualizar a linha do caput e do inciso para marcar `fechado`:
```jsx
                <div className={`rev-line${finals.get(caputId)?.status === 'fechado' ? ' fechado' : ''}`}>
```
(idem para a linha do inciso, usando `finals.get(id)?.status`).

Passar as novas props ao modal:
```jsx
        <RevisaoModal
          dispositivo={aberto}
          suggestions={grupos.get(aberto.id) ?? []}
          finalText={finals.get(aberto.id) ?? null}
          user={user}
          onAdd={handleAdd}
          onToggleLike={(s) => toggleLike(s, user.uid)}
          onDelete={(s) => deleteSuggestion(s.id)}
          onSetStatus={(s, status) => setAdminStatus(s.id, status)}
          onSaveFinal={(texto, status) => saveFinalText(aberto.id, { texto, status, autor: { uid: user.uid, nome: user.nome } })}
          onClose={() => setAberto(null)}
        />
```

- [ ] **Step 2: Estilos** — ao fim de `src/index.css`:
```css
.rev-progresso { font-size: 12.5px; color: #1d6b3a; font-weight: 600; margin-top: 4px; }
.rev-line.fechado { box-shadow: inset 3px 0 0 #2aa05a; }
```

- [ ] **Step 3: Atualizar Security Rules** — em `firestore.rules`, na regra `update` de `suggestions`, permitir o admin alterar `adminStatus`:
```
      allow update: if isMember()
        && (resource.data.autorUid == request.auth.uid
            || request.resource.data.diff(resource.data).affectedKeys().hasOnly(['curtidoPor'])
            || (isAdmin() && request.resource.data.diff(resource.data).affectedKeys().hasOnly(['adminStatus'])));
```
(`finalTexts` já permite escrita só de admin.)

- [ ] **Step 4: Build** → Expected: sem erros.

- [ ] **Step 5: Verificação manual** (republicar rules antes):
- Como admin, abrir um dispositivo: marcar uma sugestão "Relevante" (fica verde) e outra "Descartar" (riscada); escrever o texto final e "Salvar e fechar" → a linha ganha um traço verde à esquerda e o contador de progresso sobe.
- Recarregar → tudo persiste.
- Como participante (outro usuário), abrir o mesmo dispositivo → vê as marcações e o texto final em modo leitura, sem botões de admin.

- [ ] **Step 6: Commit**
```bash
git add src/pages/Revisao.jsx src/index.css firestore.rules
git commit -m "feat: liga curadoria do admin e progresso na página /revisao + rules p/ adminStatus"
```

---

## Self-Review (preenchido)
- Marcar relevante/descartar (Task 2 + 3 + rules); texto final por dispositivo (Tasks 1–3); progresso (Task 3); leitura para participantes (Task 2). ✔
- Nomes consistentes: `setAdminStatus/subscribeFinalTexts/saveFinalText`; `finalText` (objeto) no modal; `finals` (Map) na página. `adminStatus` ausente = 'pendente' em todos os pontos. ✔
- Sem placeholders; passos manuais referenciam `docs/FIREBASE_SETUP.md`.
```
