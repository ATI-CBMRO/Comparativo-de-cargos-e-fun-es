# Aba "Acessos" — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Dar ao administrador uma aba `/acessos` para convidar pessoas por e-mail, controlar papéis, bloquear/liberar/remover acesso e acompanhar o último login; e uma página pública `/cadastro` para o convidado criar a própria senha.

**Architecture:** A coleção `members` deixa de ser indexada por UID e passa a ser indexada por **e-mail em minúsculas** (`members/{email}`), o que permite listar até quem foi convidado mas ainda não entrou. O `AuthProvider` passa a autorizar por `request.auth.token.email`, registra `ultimoLogin` a cada entrada e ganha `cadastrar(email, senha)`. A lógica de contagem fica num módulo puro testável; o resto é integração com Firebase, verificada manualmente ponta a ponta.

**Tech Stack:** React 18 + Vite 6, react-router-dom 6, Firebase Auth + Firestore (SDK modular v11), lucide-react, CSS único em `src/index.css`, testes com `node --test`.

## Global Constraints

- Todo texto de interface em **Português (Brasil)**; tom para não-desenvolvedor.
- E-mails sempre normalizados em **minúsculas** antes de virar id de documento ou comparação.
- Galho de trabalho: `feat/revisao-colaborativa-minuta` (já existe; não criar galho novo).
- `members/{email}` tem os campos: `email`, `nome`, `role` (`'participante'|'admin'`), `ativo` (bool), `status` (`'convidado'|'cadastrado'`), `uid` (string|null), `criadoEm`, `criadoPor`, `ultimoLogin` (timestamp|null).
- **Ao bloquear/remover uma pessoa, as sugestões dela PERMANECEM** (não apagar nada em `suggestions`).
- Testes rodam com `node --test <arquivo>` (não há script `test` no package.json). Módulos testados não podem importar `firebase.js` (que usa `import.meta.env`).
- Admin atual: `bmwandrio@gmail.com`, UID `KCqK1IloqwPRQkyPglks6nXkdF82`.

---

### Task 1: Lógica pura de membros (`membersStats.js`)

**Files:**
- Create: `src/lib/membersStats.js`
- Test: `src/lib/membersStats.test.js`

**Interfaces:**
- Produces:
  - `normalizeEmail(email: string): string` — trim + lowercase, tolerante a `null`/`undefined`.
  - `situacaoMembro(member: {ativo?: boolean, status?: string}): 'bloqueado'|'cadastrado'|'convidado'`
  - `contaStatus(members: Array<member>): {total:number, cadastrados:number, convidados:number, bloqueados:number}`

- [ ] **Step 1: Write the failing test**

Create `src/lib/membersStats.test.js`:

```js
import { test } from 'node:test'
import assert from 'node:assert/strict'
import { normalizeEmail, situacaoMembro, contaStatus } from './membersStats.js'

test('normalizeEmail apara espaços e baixa a caixa', () => {
  assert.equal(normalizeEmail('  Fulano@CBM.RO.gov.BR '), 'fulano@cbm.ro.gov.br')
  assert.equal(normalizeEmail(undefined), '')
  assert.equal(normalizeEmail(null), '')
})

test('situacaoMembro: ativo=false sempre é bloqueado', () => {
  assert.equal(situacaoMembro({ ativo: false, status: 'cadastrado' }), 'bloqueado')
  assert.equal(situacaoMembro({ ativo: false, status: 'convidado' }), 'bloqueado')
})

test('situacaoMembro: ativo segue o status', () => {
  assert.equal(situacaoMembro({ ativo: true, status: 'cadastrado' }), 'cadastrado')
  assert.equal(situacaoMembro({ ativo: true, status: 'convidado' }), 'convidado')
})

test('contaStatus soma por situação', () => {
  const members = [
    { ativo: true, status: 'cadastrado' },
    { ativo: true, status: 'cadastrado' },
    { ativo: true, status: 'convidado' },
    { ativo: false, status: 'cadastrado' },
  ]
  assert.deepEqual(contaStatus(members), { total: 4, cadastrados: 2, convidados: 1, bloqueados: 1 })
})
```

- [ ] **Step 2: Run test to verify it fails**

Run: `node --test src/lib/membersStats.test.js`
Expected: FAIL — `Cannot find module './membersStats.js'`.

- [ ] **Step 3: Write minimal implementation**

Create `src/lib/membersStats.js`:

```js
// Helpers puros (sem Firebase) sobre a lista de membros: normalização de e-mail,
// situação de acesso exibida e contagem para os cartões da aba Acessos.

export function normalizeEmail(email) {
  return (email ?? '').trim().toLowerCase()
}

// Situação exibida: bloqueado vence tudo (ativo:false); senão o próprio status.
export function situacaoMembro(member) {
  if (member.ativo === false) return 'bloqueado'
  return member.status === 'cadastrado' ? 'cadastrado' : 'convidado'
}

export function contaStatus(members) {
  const c = { total: 0, cadastrados: 0, convidados: 0, bloqueados: 0 }
  for (const m of members) {
    c.total += 1
    const s = situacaoMembro(m)
    if (s === 'bloqueado') c.bloqueados += 1
    else if (s === 'cadastrado') c.cadastrados += 1
    else c.convidados += 1
  }
  return c
}
```

- [ ] **Step 4: Run test to verify it passes**

Run: `node --test src/lib/membersStats.test.js`
Expected: PASS — 4 testes ok.

- [ ] **Step 5: Commit**

```bash
git add src/lib/membersStats.js src/lib/membersStats.test.js
git commit -m "feat: lógica pura de status de membros (Acessos)"
```

---

### Task 2: Migração para e-mail — regras + auth + doc do admin

> Esta é a virada de chave. As três coisas mudam juntas porque dependem uma da outra: as regras passam a olhar `members/{token.email}`, o `AuthProvider` passa a ler/gravar por e-mail, e o documento do admin precisa existir no novo formato. A ordem dos passos evita qualquer janela em que o admin fique trancado para fora.

**Files:**
- Modify: `firestore.rules` (reescrever para basear em `request.auth.token.email`)
- Modify: `src/lib/auth.jsx` (ler/gravar por e-mail; registrar `ultimoLogin`; expor `cadastrar`)
- Manual: console do Firebase (criar `members/bmwandrio@gmail.com`, depois apagar o doc por UID)

**Interfaces:**
- Consumes: `normalizeEmail` de `src/lib/membersStats.js` (Task 1).
- Produces: contexto `useAuth()` agora expõe também `cadastrar(email, senha): Promise<void>` (cria a conta no Firebase Auth; a autorização/registro de login acontece no `onAuthStateChanged`). `user` continua `{uid, email, nome, role}` com `email` em minúsculas.

- [ ] **Step 1: Criar o documento do admin no novo formato (console — NÃO apagar o antigo ainda)**

No console do Firebase → Firestore → coleção `members` → **Add document**, com **Document ID = `bmwandrio@gmail.com`** e os campos:

| campo | tipo | valor |
|---|---|---|
| `email` | string | `bmwandrio@gmail.com` |
| `nome` | string | `Wândrio` |
| `role` | string | `admin` |
| `ativo` | boolean | `true` |
| `status` | string | `cadastrado` |
| `uid` | string | `KCqK1IloqwPRQkyPglks6nXkdF82` |
| `criadoPor` | string | `sistema` |
| `ultimoLogin` | (deixe vazio / null) | — |
| `criadoEm` | timestamp | (data/hora de agora) |

Deixe **intacto** o documento antigo `members/KCqK1IloqwPRQkyPglks6nXkdF82` por enquanto (os dois coexistem nesta fase).

- [ ] **Step 2: Reescrever `firestore.rules` para basear em e-mail**

Substituir TODO o conteúdo de `firestore.rules` por:

```
rules_version = '2';
service cloud.firestore {
  match /databases/{database}/documents {

    function memberRef() {
      return /databases/$(database)/documents/members/$(request.auth.token.email);
    }
    function isMember() {
      return request.auth != null
        && exists(memberRef())
        && get(memberRef()).data.ativo == true;
    }
    function isAdmin() {
      return isMember() && get(memberRef()).data.role == 'admin';
    }

    match /members/{email} {
      allow read: if isAdmin()
        || (request.auth != null && request.auth.token.email == email);
      allow create, delete: if isAdmin();
      // O próprio dono só pode mexer em uid/status/ultimoLogin (registro de login).
      allow update: if isAdmin()
        || (request.auth != null && request.auth.token.email == email
            && request.resource.data.diff(resource.data).affectedKeys().hasOnly(['uid','status','ultimoLogin']));
    }

    match /suggestions/{id} {
      allow read: if isMember();
      allow create: if isMember() && request.resource.data.autorUid == request.auth.uid;
      allow delete: if isMember()
        && (resource.data.autorUid == request.auth.uid || isAdmin());
      allow update: if isMember()
        && (resource.data.autorUid == request.auth.uid
            || request.resource.data.diff(resource.data).affectedKeys().hasOnly(['curtidoPor'])
            || (isAdmin() && request.resource.data.diff(resource.data).affectedKeys().hasOnly(['adminStatus'])));
    }

    match /finalTexts/{id} {
      allow read: if isMember();
      allow write: if isAdmin();
    }
  }
}
```

- [ ] **Step 3: Publicar as regras no console**

Copiar o conteúdo de `firestore.rules` para Firebase → Firestore → **Rules** → **Publish**.
Observação: como o doc por UID e o doc por e-mail coexistem (Step 1), o admin continua autorizado mesmo antes da troca do código.

- [ ] **Step 4: Refatorar `src/lib/auth.jsx`**

Substituir TODO o conteúdo de `src/lib/auth.jsx` por:

```jsx
import { createContext, useContext, useEffect, useState } from 'react'
import {
  signInWithEmailAndPassword, createUserWithEmailAndPassword,
  signOut, onAuthStateChanged, sendPasswordResetEmail,
} from 'firebase/auth'
import { doc, getDoc, updateDoc, serverTimestamp } from 'firebase/firestore'
import { auth, db } from './firebase.js'
import { normalizeEmail } from './membersStats.js'

const AuthContext = createContext(null)

export function AuthProvider({ children }) {
  const [user, setUser] = useState(null)
  const [loading, setLoading] = useState(true)
  const [naoAutorizado, setNaoAutorizado] = useState(false)

  useEffect(() => {
    const unsub = onAuthStateChanged(auth, async (fbUser) => {
      if (!fbUser) {
        setUser(null); setNaoAutorizado(false); setLoading(false)
        return
      }
      try {
        // Autorização = existir members/{email} com ativo == true.
        const email = normalizeEmail(fbUser.email)
        const ref = doc(db, 'members', email)
        const snap = await getDoc(ref)
        if (!snap.exists() || snap.data().ativo !== true) {
          setUser(null); setNaoAutorizado(true)
          await signOut(auth)
          return
        }
        const m = snap.data()
        // Marca presença: vincula o uid, confirma o cadastro e registra o login.
        try {
          await updateDoc(ref, {
            uid: fbUser.uid,
            status: 'cadastrado',
            ultimoLogin: serverTimestamp(),
          })
        } catch (e) {
          console.error('Não foi possível registrar o último login:', e)
        }
        setUser({
          uid: fbUser.uid,
          email,
          nome: m.nome ?? email,
          role: m.role === 'admin' ? 'admin' : 'participante',
        })
        setNaoAutorizado(false)
      } catch (e) {
        // Falha ao verificar o cadastro (ex.: rede): não trava a tela.
        console.error('Erro ao verificar acesso:', e)
        setUser(null)
      } finally {
        setLoading(false)
      }
    })
    return unsub
  }, [])

  const entrar = async (email, senha) => {
    await signInWithEmailAndPassword(auth, normalizeEmail(email), senha)
  }
  const cadastrar = async (email, senha) => {
    await createUserWithEmailAndPassword(auth, normalizeEmail(email), senha)
  }
  const sair = () => signOut(auth)
  const recuperarSenha = (email) => sendPasswordResetEmail(auth, normalizeEmail(email))

  return (
    <AuthContext.Provider value={{ user, loading, naoAutorizado, entrar, cadastrar, sair, recuperarSenha }}>
      {children}
    </AuthContext.Provider>
  )
}

export function useAuth() {
  const ctx = useContext(AuthContext)
  if (ctx === null) throw new Error('useAuth precisa estar dentro de <AuthProvider>')
  return ctx
}
```

- [ ] **Step 5: Verificar build e login do admin (manual, ponta a ponta)**

```bash
npm run dev
```

No navegador: abra `/login`, entre com `bmwandrio@gmail.com`. Esperado: entra e cai em `/revisao` (sem ficar travado em "Carregando…"). No console do Firestore, confira que `members/bmwandrio@gmail.com` ganhou `ultimoLogin` preenchido e `status: 'cadastrado'`.
Expected: login ok + `ultimoLogin` gravado.

- [ ] **Step 6: Apagar o documento antigo por UID (console)**

Confirmado o login pelo e-mail, apagar `members/KCqK1IloqwPRQkyPglks6nXkdF82` no console (Firestore → coleção `members` → delete document). Recarregue `/revisao` logado e confirme que continua funcionando.

- [ ] **Step 7: Commit**

```bash
git add firestore.rules src/lib/auth.jsx
git commit -m "feat: autorização e regras por e-mail + registro de último login"
```

---

### Task 3: Aba `/acessos` (camada de dados + tela + nav)

**Files:**
- Create: `src/lib/membersData.js`
- Create: `src/pages/Acessos.jsx`
- Modify: `src/App.jsx` (importes, rota `/acessos`, item de menu "Acessos" e "Revisão")
- Modify: `src/index.css` (estilos `.acc-*` ao final do arquivo)

**Interfaces:**
- Consumes: `contaStatus`, `situacaoMembro`, `normalizeEmail` de `src/lib/membersStats.js` (Task 1); `useAuth()` de `src/lib/auth.jsx` (Task 2).
- Produces (`membersData.js`):
  - `subscribeMembers(onChange: (list)=>void, onError?: (e)=>void): () => void`
  - `addMember({email, nome, role}: object, criadoPor: string): Promise<void>`
  - `setMemberRole(email: string, role: 'admin'|'participante'): Promise<void>`
  - `setMemberAtivo(email: string, ativo: boolean): Promise<void>`
  - `removeMember(email: string): Promise<void>`

- [ ] **Step 1: Criar a camada de dados `membersData.js`**

Create `src/lib/membersData.js`:

```js
import {
  collection, doc, setDoc, updateDoc, deleteDoc,
  onSnapshot, query, orderBy, serverTimestamp,
} from 'firebase/firestore'
import { db } from './firebase.js'
import { normalizeEmail } from './membersStats.js'

const COL = 'members'

export function subscribeMembers(onChange, onError) {
  const q = query(collection(db, COL), orderBy('criadoEm', 'asc'))
  return onSnapshot(q,
    (snap) => onChange(snap.docs.map(d => ({ id: d.id, ...d.data() }))),
    (err) => { if (onError) onError(err) },
  )
}

export async function addMember({ email, nome, role }, criadoPor) {
  const id = normalizeEmail(email)
  await setDoc(doc(db, COL, id), {
    email: id,
    nome: (nome ?? '').trim() || id,
    role: role === 'admin' ? 'admin' : 'participante',
    ativo: true,
    status: 'convidado',
    uid: null,
    criadoEm: serverTimestamp(),
    criadoPor: criadoPor ?? null,
    ultimoLogin: null,
  })
}

export async function setMemberRole(email, role) {
  await updateDoc(doc(db, COL, normalizeEmail(email)), {
    role: role === 'admin' ? 'admin' : 'participante',
  })
}

export async function setMemberAtivo(email, ativo) {
  await updateDoc(doc(db, COL, normalizeEmail(email)), { ativo: !!ativo })
}

export async function removeMember(email) {
  await deleteDoc(doc(db, COL, normalizeEmail(email)))
}
```

- [ ] **Step 2: Criar a página `Acessos.jsx`**

Create `src/pages/Acessos.jsx`:

```jsx
import { useEffect, useMemo, useState } from 'react'
import { useAuth } from '../lib/auth.jsx'
import { contaStatus, situacaoMembro } from '../lib/membersStats.js'
import {
  subscribeMembers, addMember, setMemberRole, setMemberAtivo, removeMember,
} from '../lib/membersData.js'

function formatLogin(ts) {
  if (!ts || typeof ts.toDate !== 'function') return null
  return ts.toDate().toLocaleString('pt-BR', {
    day: '2-digit', month: '2-digit', hour: '2-digit', minute: '2-digit',
  })
}

const BADGE = {
  cadastrado: { cls: 'b-cad', txt: '🟢 Cadastrado' },
  convidado: { cls: 'b-conv', txt: '🟡 Convidado' },
  bloqueado: { cls: 'b-bloq', txt: '🔴 Bloqueado' },
}

export default function Acessos() {
  const { user } = useAuth()
  const [members, setMembers] = useState([])
  const [erro, setErro] = useState(null)
  const [abrindo, setAbrindo] = useState(false)
  const [email, setEmail] = useState('')
  const [nome, setNome] = useState('')
  const [role, setRole] = useState('participante')

  useEffect(() => subscribeMembers(
    setMembers,
    (e) => { console.error('Erro ao carregar membros:', e); setErro('Não foi possível carregar a lista de acessos.') },
  ), [])

  const stats = useMemo(() => contaStatus(members), [members])

  const convidar = async (e) => {
    e.preventDefault()
    if (!email.trim()) return
    try {
      await addMember({ email, nome, role }, user.email)
      setEmail(''); setNome(''); setRole('participante'); setAbrindo(false)
    } catch (err) {
      console.error(err); setErro('Não foi possível adicionar a pessoa.')
    }
  }

  const alternarPapel = (m) => setMemberRole(m.email, m.role === 'admin' ? 'participante' : 'admin')
  const alternarAtivo = (m) => setMemberAtivo(m.email, !m.ativo)
  const remover = (m) => {
    if (window.confirm(`Remover ${m.email}? As sugestões já enviadas permanecem.`)) removeMember(m.email)
  }

  return (
    <div className="acc-wrap">
      <h2 className="acc-title">Acessos</h2>
      <p className="acc-sub">Convide pessoas pelo e-mail, controle papéis e acompanhe quem se cadastrou e quando entrou.</p>

      {erro && <div className="login-erro" style={{ marginBottom: 12 }}>{erro}</div>}

      <div className="acc-cards">
        <div className="acc-stat"><div className="acc-n">{stats.total}</div><div className="acc-l">Pessoas no total</div></div>
        <div className="acc-stat"><div className="acc-n"><span className="acc-dot" style={{ background: '#2aa05a' }} />{stats.cadastrados}</div><div className="acc-l">Cadastradas</div></div>
        <div className="acc-stat"><div className="acc-n"><span className="acc-dot" style={{ background: '#e0a106' }} />{stats.convidados}</div><div className="acc-l">Convidadas (sem entrar)</div></div>
        <div className="acc-stat"><div className="acc-n"><span className="acc-dot" style={{ background: '#c8102e' }} />{stats.bloqueados}</div><div className="acc-l">Bloqueadas</div></div>
      </div>

      <div className="acc-bar">
        <strong>Pessoas</strong>
        <button type="button" className="acc-add" onClick={() => setAbrindo(o => !o)}>＋ Convidar pessoa</button>
      </div>

      {abrindo && (
        <form className="acc-addform" onSubmit={convidar}>
          <div className="acc-fld" style={{ flex: 2, minWidth: 220 }}>
            <label>E-mail</label>
            <input value={email} onChange={e => setEmail(e.target.value)} type="email" placeholder="pessoa@exemplo.com" required />
          </div>
          <div className="acc-fld" style={{ flex: 2, minWidth: 180 }}>
            <label>Nome</label>
            <input value={nome} onChange={e => setNome(e.target.value)} placeholder="Posto e nome" />
          </div>
          <div className="acc-fld">
            <label>Papel</label>
            <select value={role} onChange={e => setRole(e.target.value)}>
              <option value="participante">Participante</option>
              <option value="admin">Administrador</option>
            </select>
          </div>
          <button type="submit" className="acc-add">Adicionar à lista</button>
        </form>
      )}

      <div className="acc-panel">
        <table className="acc-table">
          <thead>
            <tr><th>Pessoa</th><th>Papel</th><th>Status</th><th>Último login</th><th style={{ textAlign: 'right' }}>Ações</th></tr>
          </thead>
          <tbody>
            {members.map(m => {
              const sit = situacaoMembro(m)
              const badge = BADGE[sit]
              const login = formatLogin(m.ultimoLogin)
              const ehEu = m.email === user.email
              return (
                <tr key={m.email} style={sit === 'bloqueado' ? { opacity: .65 } : undefined}>
                  <td>
                    <div className="acc-nome">{m.nome}{m.role === 'admin' ? ' (administrador)' : ''}</div>
                    <div className="acc-mail">{m.email}</div>
                  </td>
                  <td><span className={`acc-papel${m.role === 'admin' ? ' adm' : ''}`}>{m.role === 'admin' ? 'Administrador' : 'Participante'}</span></td>
                  <td><span className={`acc-badge ${badge.cls}`}>{badge.txt}</span></td>
                  <td className={login ? 'acc-quando' : 'acc-nunca'}>{login ?? 'nunca entrou'}</td>
                  <td>
                    {ehEu ? (
                      <div className="acc-acts"><span className="acc-eu">você</span></div>
                    ) : (
                      <div className="acc-acts">
                        <button type="button" className="acc-ic" onClick={() => alternarPapel(m)}>papel</button>
                        <button type="button" className="acc-ic" onClick={() => alternarAtivo(m)}>{m.ativo ? 'bloquear' : 'liberar'}</button>
                        <button type="button" className="acc-ic danger" onClick={() => remover(m)}>remover</button>
                      </div>
                    )}
                  </td>
                </tr>
              )
            })}
          </tbody>
        </table>
      </div>
    </div>
  )
}
```

- [ ] **Step 3: Adicionar estilos `.acc-*` ao final de `src/index.css`**

Acrescentar ao FINAL de `src/index.css`:

```css
/* ===== Aba Acessos ===== */
.acc-wrap { max-width: 1040px; margin: 0 auto; }
.acc-title { font-size: 22px; color: #121d3d; margin: 0 0 2px; }
.acc-sub { color: #5a667f; font-size: 13.5px; margin: 0 0 16px; }
.acc-cards { display: flex; gap: 12px; flex-wrap: wrap; margin-bottom: 18px; }
.acc-stat { flex: 1; min-width: 120px; background: #fff; border: 1px solid #e3e8f0; border-radius: 10px; padding: 12px 14px; }
.acc-n { font-size: 24px; font-weight: 800; color: #121d3d; }
.acc-l { font-size: 12px; color: #5a667f; }
.acc-dot { display: inline-block; width: 9px; height: 9px; border-radius: 50%; margin-right: 5px; vertical-align: 1px; }
.acc-bar { display: flex; justify-content: space-between; align-items: center; margin-bottom: 10px; }
.acc-add { background: #c8102e; color: #fff; border: none; border-radius: 9px; padding: 10px 16px; font-weight: 700; font-size: 13.5px; cursor: pointer; }
.acc-addform { background: #fbfcff; border: 1px dashed #c5cee0; border-radius: 10px; padding: 14px; margin-bottom: 14px; display: flex; gap: 10px; align-items: end; flex-wrap: wrap; }
.acc-fld { display: flex; flex-direction: column; gap: 4px; }
.acc-fld label { font-size: 11px; text-transform: uppercase; letter-spacing: .04em; color: #5a667f; font-weight: 700; }
.acc-fld input, .acc-fld select { border: 1px solid #c5cee0; border-radius: 8px; padding: 9px 10px; font-size: 13.5px; font-family: inherit; }
.acc-panel { background: #fff; border: 1px solid #e3e8f0; border-radius: 11px; overflow: hidden; }
.acc-table { width: 100%; border-collapse: collapse; font-size: 13.5px; }
.acc-table th { text-align: left; background: #f7f9fc; color: #5a667f; font-size: 11px; text-transform: uppercase; letter-spacing: .04em; padding: 11px 14px; border-bottom: 1px solid #e3e8f0; }
.acc-table td { padding: 12px 14px; border-bottom: 1px solid #eef1f6; vertical-align: middle; }
.acc-table tr:last-child td { border-bottom: none; }
.acc-nome { font-weight: 600; color: #121d3d; }
.acc-mail { font-size: 12px; color: #5a667f; }
.acc-badge { font-size: 11.5px; border-radius: 12px; padding: 2px 10px; font-weight: 700; display: inline-flex; align-items: center; gap: 5px; }
.acc-badge.b-conv { background: #fff6e6; color: #9a6700; }
.acc-badge.b-cad { background: #e9f6ee; color: #1d6b3a; }
.acc-badge.b-bloq { background: #fdecee; color: #9b1c2c; }
.acc-papel { font-size: 12.5px; color: #3a4866; }
.acc-papel.adm { font-weight: 700; color: #c8102e; }
.acc-quando { color: #5a667f; }
.acc-nunca { color: #b08900; font-style: italic; }
.acc-acts { display: flex; gap: 6px; justify-content: flex-end; }
.acc-eu { font-size: 12px; color: #9aa4ba; font-style: italic; }
.acc-ic { border: 1px solid #d7deea; background: #fff; border-radius: 7px; padding: 5px 8px; font-size: 12.5px; cursor: pointer; color: #3a4866; }
.acc-ic.danger:hover { border-color: #c8102e; color: #c8102e; }
```

- [ ] **Step 4: Ligar rota e itens de menu em `src/App.jsx`**

Em `src/App.jsx`, no bloco de importes de páginas (logo após a linha que importa `Revisao`), acrescentar:

```jsx
import Acessos from './pages/Acessos.jsx'
```

Na linha de importe de ícones do lucide-react, acrescentar `MessageSquare, ShieldCheck`:

```jsx
import {
  Flame, LayoutDashboard, BookOpen, GitCompare,
  Search, Library, ScrollText, Menu, X, Network, LogOut,
  MessageSquare, ShieldCheck
} from 'lucide-react'
```

No componente `Sidebar`, ler o usuário e renderizar os itens condicionais. Trocar a assinatura e o `<nav>` por:

```jsx
function Sidebar({ open, collapsed, onNavigate, onToggleCollapse }) {
  const { user } = useAuth()
  return (
    <aside id="sidebar-nav" className={`sidebar${open ? ' open' : ''}`}>
      <button
        type="button"
        className="sidebar-logo"
        onClick={onToggleCollapse}
        aria-expanded={!collapsed}
        title={collapsed ? 'Expandir navegação' : 'Recolher navegação'}
      >
        <div className="sidebar-logo-icon">
          <Flame size={20} color="#fff" strokeWidth={2.5} />
        </div>
        <div className="sidebar-logo-text">
          <strong>Portal CBM</strong>
          <span>Legislação Comparada</span>
        </div>
      </button>

      <nav className="sidebar-nav">
        <div className="nav-section-label">Navegação</div>
        {NAV.map(({ to, icon: Icon, label, end }) => (
          <NavLink
            key={to}
            to={to}
            end={end}
            onClick={onNavigate}
            title={label}
            className={({ isActive }) => `nav-item${isActive ? ' active' : ''}`}
          >
            <Icon className="nav-icon" size={18} />
            <span className="nav-item-label">{label}</span>
          </NavLink>
        ))}

        {user && (
          <NavLink to="/revisao" onClick={onNavigate} title="Revisão"
            className={({ isActive }) => `nav-item${isActive ? ' active' : ''}`}>
            <MessageSquare className="nav-icon" size={18} />
            <span className="nav-item-label">Revisão</span>
          </NavLink>
        )}
        {user?.role === 'admin' && (
          <NavLink to="/acessos" onClick={onNavigate} title="Acessos"
            className={({ isActive }) => `nav-item${isActive ? ' active' : ''}`}>
            <ShieldCheck className="nav-icon" size={18} />
            <span className="nav-item-label">Acessos</span>
          </NavLink>
        )}
      </nav>

      <div className="sidebar-footer">
        <p className="sidebar-footer-text">
          Dados das legislações oficiais<br />
          <span style={{ color: '#4a5680' }}>Atualizado em junho/2026</span>
        </p>
      </div>
    </aside>
  )
}
```

No bloco `<Routes>`, logo após a rota `/revisao`, acrescentar:

```jsx
<Route path="/acessos" element={<ProtectedRoute requireAdmin><Acessos /></ProtectedRoute>} />
```

- [ ] **Step 5: Verificar manualmente (admin)**

```bash
npm run dev
```

Logado como `bmwandrio@gmail.com`: o menu mostra **Acessos**. Abra `/acessos`:
- os cartões mostram contagens (ao menos 1 cadastrado: você);
- clique **Convidar pessoa**, preencha um e-mail de teste (ex.: `teste@exemplo.com`) + nome + papel Participante → **Adicionar à lista** → a linha aparece com 🟡 Convidado e "nunca entrou";
- na sua própria linha aparece "você" (sem ações destrutivas);
- na linha do convidado, **bloquear** muda para 🔴 Bloqueado e o cartão "Bloqueadas" sobe; **liberar** volta;
- **remover** (com confirmação) tira a linha.

Expected: todas as ações refletem na hora (tempo real) e nos cartões.

- [ ] **Step 6: Commit**

```bash
git add src/lib/membersData.js src/pages/Acessos.jsx src/App.jsx src/index.css
git commit -m "feat: aba Acessos (convidar, papéis, bloquear/remover, último login)"
```

---

### Task 4: Página pública de autocadastro (`/cadastro`)

**Files:**
- Create: `src/pages/Cadastro.jsx`
- Modify: `src/App.jsx` (importe + rota pública `/cadastro`)

**Interfaces:**
- Consumes: `cadastrar`, `naoAutorizado`, `user` de `useAuth()` (Task 2); classes CSS `.login-*` já existentes em `src/index.css`.

- [ ] **Step 1: Criar a página `Cadastro.jsx`**

Create `src/pages/Cadastro.jsx`:

```jsx
import { useState, useEffect } from 'react'
import { useNavigate, Link } from 'react-router-dom'
import { useAuth } from '../lib/auth.jsx'

const MENSAGENS = {
  'auth/email-already-in-use': 'Este e-mail já tem cadastro. Use a tela de login.',
  'auth/invalid-email': 'E-mail inválido.',
  'auth/weak-password': 'A senha precisa ter ao menos 6 caracteres.',
}

export default function Cadastro() {
  const { cadastrar, naoAutorizado, user } = useAuth()
  const navigate = useNavigate()
  const [email, setEmail] = useState('')
  const [senha, setSenha] = useState('')
  const [confirma, setConfirma] = useState('')
  const [erro, setErro] = useState('')
  const [enviando, setEnviando] = useState(false)

  // Cadastrou e foi autorizado: o AuthProvider seta `user`; então navegamos.
  useEffect(() => { if (user) navigate('/revisao', { replace: true }) }, [user, navigate])
  // Conta criada, mas e-mail não está na lista de convidados: para o "Criando…".
  useEffect(() => { if (naoAutorizado) setEnviando(false) }, [naoAutorizado])

  const submeter = async (e) => {
    e.preventDefault()
    setErro('')
    if (senha.length < 6) { setErro('A senha precisa ter ao menos 6 caracteres.'); return }
    if (senha !== confirma) { setErro('As senhas não conferem.'); return }
    setEnviando(true)
    try {
      await cadastrar(email, senha)
      // Autorização/navegação acontecem via AuthProvider (useEffect acima / naoAutorizado).
    } catch (err) {
      setErro(MENSAGENS[err.code] ?? 'Não foi possível criar o cadastro. Tente novamente.')
      setEnviando(false)
    }
  }

  return (
    <div className="login-wrap">
      <form className="login-card" onSubmit={submeter}>
        <h2 className="login-title">Criar acesso</h2>
        <p className="login-sub">Use o e-mail que foi liberado pelo administrador</p>

        {naoAutorizado && (
          <div className="login-erro">Este e-mail ainda não foi liberado pelo administrador.</div>
        )}
        {erro && <div className="login-erro">{erro}</div>}

        <label className="login-label">E-mail
          <input className="login-input" type="email" value={email}
            onChange={e => setEmail(e.target.value)} autoComplete="email" required />
        </label>
        <label className="login-label">Senha
          <input className="login-input" type="password" value={senha}
            onChange={e => setSenha(e.target.value)} autoComplete="new-password" required />
        </label>
        <label className="login-label">Confirmar senha
          <input className="login-input" type="password" value={confirma}
            onChange={e => setConfirma(e.target.value)} autoComplete="new-password" required />
        </label>

        <button className="login-btn" type="submit" disabled={enviando}>
          {enviando ? 'Criando…' : 'Criar acesso'}
        </button>
        <Link className="login-link" to="/login">Já tenho acesso — entrar</Link>
      </form>
    </div>
  )
}
```

- [ ] **Step 2: Registrar a rota pública em `src/App.jsx`**

No bloco de importes de páginas, acrescentar:

```jsx
import Cadastro from './pages/Cadastro.jsx'
```

No `<Routes>`, logo após a rota `/login`, acrescentar:

```jsx
<Route path="/cadastro" element={<Cadastro />} />
```

- [ ] **Step 3: Verificar autocadastro ponta a ponta (manual)**

Pré-requisito: na aba `/acessos` (logado como admin), convide um e-mail de teste que você controle (ou use um já convidado).
Depois, em uma janela anônima, abra `/cadastro`:
- e-mail NÃO convidado → cria a conta mas cai em "Este e-mail ainda não foi liberado" (o AuthProvider faz signOut). Esperado.
- e-mail convidado + senha (≥6) + confirmação igual → entra e vai para `/revisao`. No `/acessos` (admin), a linha desse e-mail passa para 🟢 Cadastrado e mostra "Último login" preenchido.
- senhas diferentes → "As senhas não conferem." sem chamar o Firebase.

Expected: convidado vira cadastrado; último login aparece.

- [ ] **Step 4: Commit**

```bash
git add src/pages/Cadastro.jsx src/App.jsx
git commit -m "feat: página pública de autocadastro (/cadastro)"
```

---

### Task 5: Verificação final, documentação e publicação

**Files:**
- Modify: `CLAUDE.md` (ajustar a seção de Revisão Colaborativa para refletir members por e-mail + Acessos)
- Modify: `~/.claude/projects/.../memory/revisao-minuta-feature.md` (marcar Acessos como CONCLUÍDO)

- [ ] **Step 1: Rodar a suíte de testes pura**

Run: `node --test src/lib/membersStats.test.js src/lib/dispositivoId.test.js src/lib/reviewGroup.test.js`
Expected: todos PASS (nenhuma regressão).

- [ ] **Step 2: Teste manual ponta a ponta (cenário completo)**

Com `npm run dev`: convidar (admin) → autocadastrar (janela anônima) → confirmar status 🟢 Cadastrado + último login → bloquear → confirmar que o bloqueado não entra mais (`/login` → "acesso não liberado") → confirmar que as sugestões dele continuam visíveis em `/revisao` → remover.
Expected: fluxo inteiro coerente; sugestões preservadas.

- [ ] **Step 3: Atualizar a documentação**

Em `CLAUDE.md`, na seção "Revisão Colaborativa da Minuta", confirmar/ajustar que `members` é indexado por **e-mail**, que existem as rotas `/cadastro` (pública) e `/acessos` (admin), e que o login grava `ultimoLogin`.

Na memória `revisao-minuta-feature.md`, mover a feature "Acessos" de EM ANDAMENTO para CONCLUÍDO (login por e-mail, autocadastro, aba admin, último login, migração do doc do admin feita).

- [ ] **Step 4: Commit e push**

```bash
git add CLAUDE.md
git commit -m "docs: atualiza documentação para acesso por e-mail + aba Acessos"
git push
```

- [ ] **Step 5: Lembrete de publicação (Vercel) — NÃO bloqueia o merge**

Quando for publicar o site, cadastrar nas Environment Variables da Vercel: `VITE_FIREBASE_*` (6 chaves) + `GEMINI_API_KEY`. Sem isso, o site publicado não conecta ao Firebase nem à IA. (Tarefa separada, fora deste plano de código.)

---

## Self-Review

**Cobertura do spec:**
- Modelo de acesso (admin libera e-mail, pessoa se cadastra) → Task 4 + Task 3 (convite). ✓
- Sem verificação de e-mail → `cadastrar` só faz `createUserWithEmailAndPassword`. ✓
- Sugestões permanecem ao cortar acesso → não há delete em `suggestions`; confirmado em Task 5 Step 2. ✓
- `members/{email}` com todos os campos → Task 3 `addMember` + migração Task 2 Step 1. ✓
- auth por e-mail + `ultimoLogin` + `cadastrar` → Task 2 Step 4. ✓
- `membersData.js` (5 funções) → Task 3 Step 1. ✓
- `membersStats.js` `contaStatus` → Task 1. ✓
- `Cadastro.jsx` / `Acessos.jsx` → Tasks 4 / 3. ✓
- Rotas `/cadastro` (pública) e `/acessos` (requireAdmin) + menu admin + menu Revisão → Tasks 4 / 3. ✓
- Security Rules por e-mail → Task 2 Step 2. ✓
- E-mails em minúsculas → `normalizeEmail` em todos os pontos. ✓
- Migração do doc do admin → Task 2 Steps 1 e 6. ✓
- Testes (`membersStats.test.js`, rules no console, manual ponta a ponta) → Tasks 1 e 5. ✓

**Itens fora de escopo do spec mantidos fora:** reenvio de convite por e-mail, verificação de e-mail, contagem de sugestões por pessoa, exportar lista. ✓

**Consistência de tipos:** `normalizeEmail` (membersStats) usado igual em auth/membersData; `situacaoMembro` retorna exatamente as chaves de `BADGE`; `contaStatus` retorna `{total,cadastrados,convidados,bloqueados}` consumidas nos 4 cartões; `addMember(obj, criadoPor)` chamado com `(/* obj */, user.email)`. ✓
