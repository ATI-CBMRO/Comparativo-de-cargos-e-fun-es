# Revisão Colaborativa — Etapa 1: Fundação (Firebase + Auth) — Plano de Implementação

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Habilitar login por e-mail+senha com acesso restrito a convidados (papéis participante/admin) e deixar a rota `/revisao` protegida pronta para receber o conteúdo da Etapa 2.

**Architecture:** Frontend React/Vite (na Vercel) conversa direto com o Firebase (Authentication + Firestore) via SDK modular v9+, sem servidor próprio. A autorização é decidida pela existência de `members/{uid}` com `ativo: true` no Firestore, espelhada nas Security Rules. Um `AuthProvider` (Context) carrega o usuário e seu papel; `ProtectedRoute` bloqueia rotas.

**Tech Stack:** React 18, react-router-dom 6, Vite 6, Firebase JS SDK (`firebase` ^11), `node --test` para lógica pura.

## Global Constraints

- Idioma de toda a UI e mensagens: **Português (Brasil)**.
- **Nenhuma chave/segredo no código versionado.** Config do Firebase vem de `import.meta.env.VITE_FIREBASE_*` (arquivo `.env`, já no `.gitignore`).
- Seguir os padrões do projeto: componentes em `src/pages/` e `src/components/`, libs sem React em `src/lib/`, CSS único em `src/index.css`. Sem TypeScript (projeto é JSX).
- Não alterar a pipeline Python nem páginas existentes além do necessário para registrar rotas/provider.
- Durante a rodada de revisão, `database/minuta_structure.json` é **congelado** (não reexecutar a pipeline que altera `editId`).
- Commits pequenos e frequentes, mensagens em português no padrão `tipo: descrição`.

---

### Task 1: Projeto Firebase + inicialização do SDK

**Files:**
- Create: `src/lib/firebase.js`
- Create: `.env.example`
- Modify: `package.json` (dependência `firebase`)
- Manual: console do Firebase (passos abaixo) + arquivo local `.env` (não versionado)

**Interfaces:**
- Produces: `app`, `auth`, `db` exportados de `src/lib/firebase.js` (instâncias de `FirebaseApp`, `Auth`, `Firestore`).

- [ ] **Step 1: Criar o projeto no Firebase (manual — feito pelo Wândrio/admin)**

No navegador, em https://console.firebase.google.com:
1. "Adicionar projeto" → nome `revisao-minuta-cbmro` → desativar Google Analytics (não é necessário) → criar.
2. Menu **Authentication** → "Vamos começar" → aba **Sign-in method** → habilitar **E-mail/senha** → salvar.
3. Menu **Firestore Database** → "Criar banco de dados" → modo **produção** → local `southamerica-east1` (São Paulo) → ativar.
4. Engrenagem **Configurações do projeto** → aba "Geral" → seção "Seus apps" → ícone **</>** (Web) → apelido `portal-revisao` → registrar app. **Copiar o objeto `firebaseConfig`** mostrado (apiKey, authDomain, projectId, etc.).

> Nota de segurança: a `apiKey` do Firebase Web é pública por natureza — ela identifica o projeto, não autoriza acesso. Quem autoriza são as Security Rules (Task 6). Mesmo assim, mantemos a config em `.env` para facilitar troca de ambiente.

- [ ] **Step 2: Instalar a dependência `firebase`**

Run:
```bash
cd "/Users/wandriobandeira/Projetos de dev Sistemas/Comparativo-de-cargos-e-funcoes"
npm install firebase@^11
```
Expected: `package.json` passa a listar `"firebase"` em `dependencies`; `package-lock.json` atualizado; sem erros.

- [ ] **Step 3: Criar o `.env` local (não versionado) com os valores copiados no Step 1**

Criar o arquivo `.env` na raiz do projeto (NÃO commitar — já está no `.gitignore`) com:
```
VITE_FIREBASE_API_KEY=cole_aqui
VITE_FIREBASE_AUTH_DOMAIN=cole_aqui
VITE_FIREBASE_PROJECT_ID=cole_aqui
VITE_FIREBASE_STORAGE_BUCKET=cole_aqui
VITE_FIREBASE_MESSAGING_SENDER_ID=cole_aqui
VITE_FIREBASE_APP_ID=cole_aqui
```

- [ ] **Step 4: Criar `.env.example` (versionado, sem segredos)**

```
# Configuração do Firebase (Web). Copie para .env e preencha com os valores do
# console do Firebase → Configurações do projeto → Seus apps → SDK.
VITE_FIREBASE_API_KEY=
VITE_FIREBASE_AUTH_DOMAIN=
VITE_FIREBASE_PROJECT_ID=
VITE_FIREBASE_STORAGE_BUCKET=
VITE_FIREBASE_MESSAGING_SENDER_ID=
VITE_FIREBASE_APP_ID=
```

- [ ] **Step 5: Criar `src/lib/firebase.js`**

```js
// Inicialização única do Firebase (Authentication + Firestore).
// A config vem de variáveis de ambiente Vite (.env) — nada de segredo no código.
import { initializeApp } from 'firebase/app'
import { getAuth } from 'firebase/auth'
import { getFirestore } from 'firebase/firestore'

const firebaseConfig = {
  apiKey: import.meta.env.VITE_FIREBASE_API_KEY,
  authDomain: import.meta.env.VITE_FIREBASE_AUTH_DOMAIN,
  projectId: import.meta.env.VITE_FIREBASE_PROJECT_ID,
  storageBucket: import.meta.env.VITE_FIREBASE_STORAGE_BUCKET,
  messagingSenderId: import.meta.env.VITE_FIREBASE_MESSAGING_SENDER_ID,
  appId: import.meta.env.VITE_FIREBASE_APP_ID,
}

export const app = initializeApp(firebaseConfig)
export const auth = getAuth(app)
export const db = getFirestore(app)
```

- [ ] **Step 6: Verificar que o app sobe sem erros**

Run:
```bash
npm run dev
```
Expected: servidor inicia em http://localhost:5173 sem erros no terminal nem no console do navegador relacionados ao Firebase. Encerrar com Ctrl+C.

- [ ] **Step 7: Commit**

```bash
git add package.json package-lock.json .env.example src/lib/firebase.js
git commit -m "feat: inicializa Firebase (Auth + Firestore) via variáveis de ambiente"
```

---

### Task 2: Endereço fixo do inciso (`dispositivoId`) — lógica pura com teste

**Files:**
- Create: `src/lib/dispositivoId.js`
- Test: `src/lib/dispositivoId.test.js`

**Interfaces:**
- Produces:
  - `incisoDispositivoId(editId: string, index: number) => string` — retorna `` `${editId}#${index}` ``.
  - `caputDispositivoId(editId: string) => string` — retorna `` `${editId}#caput` ``.
  - `parseDispositivoId(id: string) => { editId: string, parte: 'caput' | number }`.

- [ ] **Step 1: Escrever o teste que falha**

`src/lib/dispositivoId.test.js`:
```js
import { test } from 'node:test'
import assert from 'node:assert/strict'
import { incisoDispositivoId, caputDispositivoId, parseDispositivoId } from './dispositivoId.js'

test('incisoDispositivoId monta editId#index', () => {
  assert.equal(incisoDispositivoId('cot-comp', 2), 'cot-comp#2')
})

test('caputDispositivoId monta editId#caput', () => {
  assert.equal(caputDispositivoId('cot-comp'), 'cot-comp#caput')
})

test('parseDispositivoId lê inciso numérico', () => {
  assert.deepEqual(parseDispositivoId('cot-comp#2'), { editId: 'cot-comp', parte: 2 })
})

test('parseDispositivoId lê caput', () => {
  assert.deepEqual(parseDispositivoId('cot-comp#caput'), { editId: 'cot-comp', parte: 'caput' })
})

test('parseDispositivoId aceita editId com hífen e ignora apenas o último #', () => {
  assert.deepEqual(parseDispositivoId('bbm-frac-3#0'), { editId: 'bbm-frac-3', parte: 0 })
})
```

- [ ] **Step 2: Rodar o teste e confirmar que falha**

Run: `node --test src/lib/dispositivoId.test.js`
Expected: FALHA com erro de módulo não encontrado / export indefinido.

- [ ] **Step 3: Implementar `src/lib/dispositivoId.js`**

```js
// Endereço ESTÁVEL de um dispositivo da minuta para ancorar comentários.
// Não use o rótulo "Art. 7º" (a numeração muda quando o texto é editado).
// Use o editId estável da seção + o índice original do inciso (mesmos que
// buildArticles expõe em cada inciso: { editId, index }).

export function incisoDispositivoId(editId, index) {
  return `${editId}#${index}`
}

export function caputDispositivoId(editId) {
  return `${editId}#caput`
}

export function parseDispositivoId(id) {
  const i = id.lastIndexOf('#')
  const editId = id.slice(0, i)
  const tail = id.slice(i + 1)
  return { editId, parte: tail === 'caput' ? 'caput' : Number(tail) }
}
```

- [ ] **Step 4: Rodar o teste e confirmar que passa**

Run: `node --test src/lib/dispositivoId.test.js`
Expected: PASS (5 testes).

- [ ] **Step 5: Commit**

```bash
git add src/lib/dispositivoId.js src/lib/dispositivoId.test.js
git commit -m "feat: dispositivoId — endereço estável de inciso/caput para ancorar comentários"
```

---

### Task 3: Contexto de autenticação (`AuthProvider`)

**Files:**
- Create: `src/lib/auth.jsx`

**Interfaces:**
- Consumes: `auth`, `db` de `src/lib/firebase.js`.
- Produces:
  - `<AuthProvider>{children}</AuthProvider>` — provê o contexto.
  - `useAuth() => { user, loading, naoAutorizado, entrar, sair, recuperarSenha }`
    - `user`: `null` ou `{ uid, email, nome, role: 'participante' | 'admin' }`.
    - `loading`: `boolean` (true enquanto resolve o estado inicial).
    - `naoAutorizado`: `boolean` (logou no Firebase mas não está em `members` ou `ativo == false`).
    - `entrar(email, senha) => Promise<void>` (lança em credencial inválida).
    - `sair() => Promise<void>`.
    - `recuperarSenha(email) => Promise<void>`.

- [ ] **Step 1: Implementar `src/lib/auth.jsx`**

```jsx
import { createContext, useContext, useEffect, useState } from 'react'
import {
  signInWithEmailAndPassword, signOut, onAuthStateChanged,
  sendPasswordResetEmail,
} from 'firebase/auth'
import { doc, getDoc } from 'firebase/firestore'
import { auth, db } from './firebase.js'

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
      // Autorização = existir members/{uid} com ativo == true.
      const snap = await getDoc(doc(db, 'members', fbUser.uid))
      if (!snap.exists() || snap.data().ativo !== true) {
        setUser(null); setNaoAutorizado(true)
        await signOut(auth)
        setLoading(false)
        return
      }
      const m = snap.data()
      setUser({
        uid: fbUser.uid,
        email: fbUser.email,
        nome: m.nome ?? fbUser.email,
        role: m.role === 'admin' ? 'admin' : 'participante',
      })
      setNaoAutorizado(false)
      setLoading(false)
    })
    return unsub
  }, [])

  const entrar = async (email, senha) => {
    await signInWithEmailAndPassword(auth, email.trim(), senha)
  }
  const sair = () => signOut(auth)
  const recuperarSenha = (email) => sendPasswordResetEmail(auth, email.trim())

  return (
    <AuthContext.Provider value={{ user, loading, naoAutorizado, entrar, sair, recuperarSenha }}>
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

- [ ] **Step 2: Verificar build (lint de import) subindo o dev server**

Run: `npm run dev`
Expected: sem erro de compilação. (Ainda sem UI que use o contexto — validação real na Task 5.) Encerrar com Ctrl+C.

- [ ] **Step 3: Commit**

```bash
git add src/lib/auth.jsx
git commit -m "feat: AuthProvider/useAuth com autorização por members/{uid}"
```

---

### Task 4: Tela de login + recuperação de senha

**Files:**
- Create: `src/pages/Login.jsx`
- Modify: `src/index.css` (estilos `.login-*`)

**Interfaces:**
- Consumes: `useAuth()` (`entrar`, `recuperarSenha`, `user`, `naoAutorizado`).
- Produces: componente `Login` (default export) usado na rota `/login`. Ao logar com sucesso, redireciona para `/revisao` via `useNavigate`.

- [ ] **Step 1: Implementar `src/pages/Login.jsx`**

```jsx
import { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { useAuth } from '../lib/auth.jsx'

const MENSAGENS = {
  'auth/invalid-credential': 'E-mail ou senha incorretos.',
  'auth/invalid-email': 'E-mail inválido.',
  'auth/missing-password': 'Digite a senha.',
  'auth/too-many-requests': 'Muitas tentativas. Aguarde alguns minutos e tente de novo.',
}

export default function Login() {
  const { entrar, recuperarSenha, naoAutorizado } = useAuth()
  const navigate = useNavigate()
  const [email, setEmail] = useState('')
  const [senha, setSenha] = useState('')
  const [erro, setErro] = useState('')
  const [aviso, setAviso] = useState('')
  const [enviando, setEnviando] = useState(false)

  const submeter = async (e) => {
    e.preventDefault()
    setErro(''); setAviso(''); setEnviando(true)
    try {
      await entrar(email, senha)
      navigate('/revisao')
    } catch (err) {
      setErro(MENSAGENS[err.code] ?? 'Não foi possível entrar. Tente novamente.')
    } finally {
      setEnviando(false)
    }
  }

  const esqueci = async () => {
    setErro(''); setAviso('')
    if (!email.trim()) { setErro('Digite seu e-mail acima para receber o link de redefinição.'); return }
    try {
      await recuperarSenha(email)
      setAviso('Enviamos um link de redefinição de senha para o seu e-mail.')
    } catch {
      setErro('Não foi possível enviar o e-mail de redefinição.')
    }
  }

  return (
    <div className="login-wrap">
      <form className="login-card" onSubmit={submeter}>
        <h2 className="login-title">Revisão da Minuta</h2>
        <p className="login-sub">Acesso restrito a convidados</p>

        {naoAutorizado && (
          <div className="login-erro">Seu acesso ainda não foi liberado pelo administrador.</div>
        )}
        {erro && <div className="login-erro">{erro}</div>}
        {aviso && <div className="login-aviso">{aviso}</div>}

        <label className="login-label">E-mail
          <input className="login-input" type="email" value={email}
            onChange={e => setEmail(e.target.value)} autoComplete="email" required />
        </label>
        <label className="login-label">Senha
          <input className="login-input" type="password" value={senha}
            onChange={e => setSenha(e.target.value)} autoComplete="current-password" required />
        </label>

        <button className="login-btn" type="submit" disabled={enviando}>
          {enviando ? 'Entrando…' : 'Entrar'}
        </button>
        <button className="login-link" type="button" onClick={esqueci}>Esqueci minha senha</button>
      </form>
    </div>
  )
}
```

- [ ] **Step 2: Adicionar estilos ao final de `src/index.css`**

```css
/* ===== Tela de login (Revisão) ===== */
.login-wrap { min-height: 70vh; display: flex; align-items: center; justify-content: center; padding: 24px; }
.login-card { width: 100%; max-width: 360px; background: #fff; border: 1px solid #d7deea;
  border-radius: 12px; padding: 28px 24px; box-shadow: 0 6px 24px rgba(18,29,61,.08); display: flex; flex-direction: column; gap: 12px; }
.login-title { margin: 0; color: #121d3d; font-family: 'Outfit', sans-serif; }
.login-sub { margin: 0 0 8px; color: #5a667f; font-size: 14px; }
.login-label { display: flex; flex-direction: column; gap: 4px; font-size: 13px; color: #3a4866; font-weight: 600; }
.login-input { padding: 10px 12px; border: 1px solid #c5cee0; border-radius: 8px; font-size: 15px; }
.login-input:focus { outline: 2px solid #c8102e; border-color: #c8102e; }
.login-btn { margin-top: 6px; padding: 11px; background: #c8102e; color: #fff; border: none;
  border-radius: 8px; font-size: 15px; font-weight: 700; cursor: pointer; }
.login-btn:disabled { opacity: .6; cursor: default; }
.login-link { background: none; border: none; color: #c8102e; cursor: pointer; font-size: 13px; }
.login-erro { background: #fdecee; border: 1px solid #f3b4bd; color: #9b1c2c; padding: 8px 10px; border-radius: 8px; font-size: 13px; }
.login-aviso { background: #e9f6ee; border: 1px solid #abdcbd; color: #1d6b3a; padding: 8px 10px; border-radius: 8px; font-size: 13px; }
```

- [ ] **Step 3: Verificação manual (após Task 5 ligar a rota)**

A verificação visual da tela ocorre no fim da Task 5 (quando `/login` estiver roteada). Aqui, apenas confirmar que `npm run dev` compila sem erro.
Run: `npm run dev` → Expected: sem erro de compilação. Ctrl+C.

- [ ] **Step 4: Commit**

```bash
git add src/pages/Login.jsx src/index.css
git commit -m "feat: tela de login com e-mail/senha e recuperação de senha"
```

---

### Task 5: Rota protegida, provider no app e placeholder `/revisao`

**Files:**
- Create: `src/components/ProtectedRoute.jsx`
- Create: `src/pages/Revisao.jsx` (placeholder desta etapa)
- Modify: `src/main.jsx` (envolver com `<AuthProvider>`)
- Modify: `src/App.jsx` (rotas `/login` e `/revisao`; botão "Sair"/identidade quando logado)

**Interfaces:**
- Consumes: `useAuth()`, `AuthProvider`.
- Produces:
  - `<ProtectedRoute requireAdmin?={boolean}>{children}</ProtectedRoute>` — redireciona para `/login` se não logado; mostra aviso se `requireAdmin` e papel ≠ admin.
  - `Revisao` (default export) — placeholder com saudação ao usuário (será substituído na Etapa 2).

- [ ] **Step 1: Implementar `src/components/ProtectedRoute.jsx`**

```jsx
import { Navigate } from 'react-router-dom'
import { useAuth } from '../lib/auth.jsx'

export default function ProtectedRoute({ children, requireAdmin = false }) {
  const { user, loading } = useAuth()
  if (loading) return <div style={{ padding: 32 }}>Carregando…</div>
  if (!user) return <Navigate to="/login" replace />
  if (requireAdmin && user.role !== 'admin') {
    return <div style={{ padding: 32 }}>Acesso restrito ao administrador.</div>
  }
  return children
}
```

- [ ] **Step 2: Implementar placeholder `src/pages/Revisao.jsx`**

```jsx
import { useAuth } from '../lib/auth.jsx'

export default function Revisao() {
  const { user } = useAuth()
  return (
    <div style={{ padding: 32 }}>
      <h2 style={{ color: '#121d3d' }}>Revisão da Minuta</h2>
      <p>Olá, {user?.nome}. Seu papel: <strong>{user?.role}</strong>.</p>
      <p style={{ color: '#5a667f' }}>
        Esta área receberá o documento com os comentários por inciso na Etapa 2.
      </p>
    </div>
  )
}
```

- [ ] **Step 3: Envolver o app com `<AuthProvider>` em `src/main.jsx`**

```jsx
import React from 'react'
import ReactDOM from 'react-dom/client'
import { BrowserRouter } from 'react-router-dom'
import App from './App.jsx'
import { AuthProvider } from './lib/auth.jsx'
import './index.css'

ReactDOM.createRoot(document.getElementById('root')).render(
  <React.StrictMode>
    <BrowserRouter>
      <AuthProvider>
        <App />
      </AuthProvider>
    </BrowserRouter>
  </React.StrictMode>
)
```

- [ ] **Step 4: Registrar rotas e botão "Sair" em `src/App.jsx`**

No topo, adicionar os imports:
```jsx
import Login from './pages/Login.jsx'
import Revisao from './pages/Revisao.jsx'
import ProtectedRoute from './components/ProtectedRoute.jsx'
import { useAuth } from './lib/auth.jsx'
import { LogOut } from 'lucide-react'
```

Dentro do `<Routes>` (em `src/App.jsx:130-139`), adicionar:
```jsx
          <Route path="/login" element={<Login />} />
          <Route path="/revisao" element={<ProtectedRoute><Revisao /></ProtectedRoute>} />
```

No componente `Header`, exibir identidade + sair quando logado. Substituir a assinatura/escopo do `Header` para receber a auth e renderizar um rodapé de usuário ao fim do `<header>`:
```jsx
function HeaderUserBox() {
  const { user, sair } = useAuth()
  if (!user) return null
  return (
    <div className="app-header-user">
      <span className="app-header-user-name">{user.nome}</span>
      <button type="button" className="app-header-user-exit" onClick={sair} title="Sair">
        <LogOut size={16} /> Sair
      </button>
    </div>
  )
}
```
E inserir `<HeaderUserBox />` como último filho dentro de `<header className="app-header"> … </header>` (logo após `app-header-text`).

Adicionar ao fim de `src/index.css`:
```css
.app-header-user { margin-left: auto; display: flex; align-items: center; gap: 10px; color: #fff; }
.app-header-user-name { font-size: 13px; opacity: .9; }
.app-header-user-exit { display: inline-flex; align-items: center; gap: 4px; background: rgba(255,255,255,.15);
  color: #fff; border: none; border-radius: 6px; padding: 6px 10px; cursor: pointer; font-size: 13px; }
```

- [ ] **Step 5: Verificação manual ponta a ponta da Etapa 1**

Pré-requisito: criar 1 usuário de teste no console do Firebase e o respectivo `members/{uid}`:
1. Firebase → Authentication → "Adicionar usuário" → e-mail `teste@exemplo.com` + senha `teste123`. Copiar o **UID** gerado.
2. Firebase → Firestore → "Iniciar coleção" `members` → ID do documento = **o UID copiado** → campos: `nome` (string) "Usuário Teste", `role` (string) "admin", `ativo` (boolean) true.

Run: `npm run dev` e no navegador:
- Abrir `http://localhost:5173/revisao` deslogado → Expected: redireciona para `/login`.
- Entrar com `teste@exemplo.com` / `teste123` → Expected: vai para `/revisao` e mostra "Olá, Usuário Teste. Seu papel: admin".
- Conferir no cabeçalho o nome + botão "Sair"; clicar "Sair" → Expected: ao tentar `/revisao` volta para `/login`.
- Entrar com e-mail/senha errados → Expected: mensagem "E-mail ou senha incorretos.".
- (Opcional) Criar um usuário no Auth SEM doc em `members` e tentar logar → Expected: mensagem "Seu acesso ainda não foi liberado pelo administrador.".

- [ ] **Step 6: Commit**

```bash
git add src/components/ProtectedRoute.jsx src/pages/Revisao.jsx src/main.jsx src/App.jsx src/index.css
git commit -m "feat: rota protegida /revisao, AuthProvider no app e botão sair"
```

---

### Task 6: Security Rules base (trava por convite)

**Files:**
- Create: `firestore.rules`
- Create: `docs/FIREBASE_SETUP.md` (instruções de publicação das regras)

**Interfaces:**
- Produces: regras publicadas no projeto Firebase que só permitem acesso a membros ativos; só admin escreve `members` e `finalTexts`; sugestões só pelo próprio autor. (As permissões de `adminStatus` em `suggestions` serão estendidas na Etapa 3.)

- [ ] **Step 1: Criar `firestore.rules`**

```
rules_version = '2';
service cloud.firestore {
  match /databases/{database}/documents {

    function isMember() {
      return request.auth != null
        && exists(/databases/$(database)/documents/members/$(request.auth.uid))
        && get(/databases/$(database)/documents/members/$(request.auth.uid)).data.ativo == true;
    }
    function isAdmin() {
      return isMember()
        && get(/databases/$(database)/documents/members/$(request.auth.uid)).data.role == 'admin';
    }

    match /members/{uid} {
      allow read: if isMember();
      allow write: if isAdmin();
    }

    match /suggestions/{id} {
      allow read: if isMember();
      allow create: if isMember() && request.resource.data.autorUid == request.auth.uid;
      allow update, delete: if isMember() && resource.data.autorUid == request.auth.uid;
    }

    match /finalTexts/{id} {
      allow read: if isMember();
      allow write: if isAdmin();
    }
  }
}
```

- [ ] **Step 2: Criar `docs/FIREBASE_SETUP.md`**

````markdown
# Configuração do Firebase — Revisão Colaborativa

## Publicar as Security Rules
1. Console do Firebase → **Firestore Database** → aba **Regras**.
2. Cole o conteúdo de `firestore.rules` (na raiz do repositório) e clique em **Publicar**.

## Cadastrar um convidado (v1)
1. **Authentication → Adicionar usuário**: e-mail + senha inicial. Copie o **UID**.
2. **Firestore → coleção `members` → documento com ID = UID** e campos:
   - `nome` (string), `role` (string: `participante` ou `admin`), `ativo` (boolean: `true`).
3. Avise a pessoa do e-mail e da senha inicial (ela troca depois via "Esqueci minha senha").

## Verificar as regras (Rules Playground)
No editor de Regras, use **Simulação/Playground**:
- Leitura de `members/{uid}` autenticado como um UID **fora** da coleção → deve **negar**.
- Leitura autenticado como um UID **com** `ativo:true` → deve **permitir**.
- `create` em `suggestions` com `autorUid` ≠ uid do autenticado → deve **negar**.
- `write` em `finalTexts` autenticado como `participante` → deve **negar**; como `admin` → **permitir**.
````

- [ ] **Step 3: Publicar e verificar (manual, no console)**

Seguir `docs/FIREBASE_SETUP.md`: publicar as regras e rodar os 4 cenários do Rules Playground.
Expected: os 4 cenários se comportam como descrito (negar/permitir).

- [ ] **Step 4: Commit**

```bash
git add firestore.rules docs/FIREBASE_SETUP.md
git commit -m "feat: Security Rules base (acesso por convite) + doc de setup do Firebase"
```

---

## Self-Review (preenchido)

**Cobertura da spec (Etapa 1):**
- Login e-mail+senha + reset → Tasks 4 (UI) + 3 (lógica). ✔
- Acesso só por convite + papéis → Tasks 3 (autorização por `members`) + 6 (Rules). ✔
- Rota protegida `/revisao` → Task 5. ✔
- Segredos fora do código → Task 1 (`.env`/`.env.example`, `.gitignore` já ajustado na spec). ✔
- Endereço estável do inciso (necessário à Etapa 2, definido já) → Task 2. ✔
- Modelo de dados `members`/`suggestions`/`finalTexts` → criado sob demanda; regras já cobrem as 3 coleções (Task 6). ✔

**Itens da spec que ficam para Etapas 2/3 (fora deste plano):** render do documento com trilha de balões e modal; CRUD de sugestões + 👍 (Etapa 2); marcação relevante/descartada, texto final, painel de progresso e extensão das Rules para `adminStatus` (Etapa 3).

**Placeholders:** nenhum "TODO/TBD" com lógica pendente; passos manuais do console são intencionais e detalhados.

**Consistência de tipos/nomes:** `useAuth()` expõe `entrar/sair/recuperarSenha/user/loading/naoAutorizado` e são exatamente esses os nomes consumidos em `Login.jsx`, `ProtectedRoute.jsx`, `Revisao.jsx` e no `Header`. `dispositivoId` expõe `incisoDispositivoId/caputDispositivoId/parseDispositivoId`, usados na Etapa 2.
```
