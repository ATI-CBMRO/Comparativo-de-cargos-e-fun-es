# Acervo Público (visitante sem login) — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Criar um terceiro perfil de acesso — visitante público, sem login e senha, com cadastro básico (nome, e-mail, instituição) — que enxerga apenas o Acervo Legal, a ficha de estado e a busca, sob a rota própria `/acervo-publico`.

**Architecture:** Camada separada do `AuthProvider`. O visitante **nunca** vira `user`: um `VisitanteProvider` independente guarda `{ uid, nome }`, obtidos por sessão anônima do Firebase, e as telas do acervo são reusadas sem fork através de um contexto de prefixo de rota (`AcervoBase`). A fronteira entre público e membro é o **caminho da URL**, não uma condição de login.

**Tech Stack:** React 18 + Vite, react-router-dom v6, Firebase Auth (anônimo) + Firestore, `node --test` para lógica pura, CSS único em `src/index.css`.

**Spec:** `docs/superpowers/specs/2026-08-18-acervo-publico-visitante-design.md` — leia antes de começar.

## Global Constraints

- **Idioma:** todo texto de interface, comentário de código e mensagem de commit em **português do Brasil**.
- **Dev server:** porta fixa **5173** (`npm run dev`). Ao terminar uma tarefa que mexe em tela, informar o link http://localhost:5173.
- **Testes:** `node --test` na raiz do projeto roda toda a suíte (96 testes hoje). Arquivos de teste ficam ao lado do módulo, com sufixo `.test.js` (padrão: `src/lib/escopoServico.test.js`).
- **Não tocar:** `src/lib/escopoServico.js`, `src/components/ProtectedRoute.jsx`, `GuardaDeEscopo`/`NAV_ESCOPO` em `src/App.jsx`, e qualquer regra existente do `firestore.rules`. Esta entrega só **acrescenta**.
- **Não há navegador no ambiente do agente.** Nenhuma tarefa pode ser declarada "verificada visualmente". A conferência de tela é do Ten. Tiago.
- **Erro nunca fica só no console:** todo `catch`/`onError` de Firestore precisa mudar algum pixel na tela (armadilha **AR-04**, `docs/superpowers/auditoria-armadilhas.md`).
- **Ramo de trabalho:** `feat/acervo-publico-visitante` (já criado, já contém o commit da spec).
- **Nome da chave de localStorage:** `cbmro_visitante` (exato).
- **Nome da coleção do Firestore:** `visitantes` (exato), documento identificado pelo `uid` anônimo.

---

### Task 1: Lógica pura do visitante (`src/lib/visitante.js`)

Módulo sem React e sem Firebase: validação dos campos do cadastro, resolução de rotas do acervo e leitura/gravação do localStorage. É o núcleo testável de tudo que vem depois.

**Files:**
- Create: `src/lib/visitante.js`
- Test: `src/lib/visitante.test.js`

**Interfaces:**
- Consumes: `normalizeEmail(email)` de `src/lib/membersStats.js` (já existe: `(email ?? '').trim().toLowerCase()`).
- Produces:
  - `BASE_PUBLICA: string` = `'/acervo-publico'`
  - `LIMITES: { nome: 200, email: 200, instituicao: 200 }`
  - `CHAVE_LOCAL: string` = `'cbmro_visitante'`
  - `normalizarVisitante({ nome, email, instituicao }) -> { ok: true, dados: { nome, email, instituicao } } | { ok: false, erro: string }`
  - `rotaEstado(base, id) -> string`
  - `rotaListaEstados(base) -> string`
  - `lerVisitanteLocal(storage) -> { uid, nome } | null`
  - `gravarVisitanteLocal(storage, { uid, nome }) -> void`
  - `limparVisitanteLocal(storage) -> void`

- [ ] **Step 1: Escreva o teste que falha**

Crie `src/lib/visitante.test.js`:

```js
import test from 'node:test'
import assert from 'node:assert/strict'
import {
  BASE_PUBLICA, LIMITES, CHAVE_LOCAL,
  normalizarVisitante, rotaEstado, rotaListaEstados,
  lerVisitanteLocal, gravarVisitanteLocal, limparVisitanteLocal,
} from './visitante.js'

// --- validação do cadastro -------------------------------------------------

test('normalizarVisitante apara espaços e normaliza o e-mail', () => {
  const r = normalizarVisitante({
    nome: '  Maria da Silva  ', email: '  Maria@Exemplo.COM ', instituicao: ' CBMPA ',
  })
  assert.equal(r.ok, true)
  assert.deepEqual(r.dados, { nome: 'Maria da Silva', email: 'maria@exemplo.com', instituicao: 'CBMPA' })
})

test('normalizarVisitante exige nome, e-mail e instituição', () => {
  assert.equal(normalizarVisitante({ nome: '  ', email: 'a@b.com', instituicao: 'X' }).ok, false)
  assert.equal(normalizarVisitante({ nome: 'A', email: '   ', instituicao: 'X' }).ok, false)
  assert.equal(normalizarVisitante({ nome: 'A', email: 'a@b.com', instituicao: '' }).ok, false)
})

test('normalizarVisitante devolve mensagem em português, nunca só ok:false', () => {
  const r = normalizarVisitante({ nome: '', email: '', instituicao: '' })
  assert.equal(r.ok, false)
  assert.equal(typeof r.erro, 'string')
  assert.ok(r.erro.length > 0)
})

test('normalizarVisitante recusa e-mail sem formato mínimo', () => {
  const r = normalizarVisitante({ nome: 'A', email: 'sem-arroba', instituicao: 'X' })
  assert.equal(r.ok, false)
  assert.match(r.erro, /e-mail/i)
})

// Os limites espelham a regra do Firestore (spec, seção 3): campo maior que o limite
// seria RECUSADO pelo banco. Barrar aqui evita uma falha silenciosa na gravação.
test('normalizarVisitante recusa campo acima do limite da regra do Firestore', () => {
  const gigante = 'x'.repeat(LIMITES.nome + 1)
  assert.equal(normalizarVisitante({ nome: gigante, email: 'a@b.com', instituicao: 'X' }).ok, false)
  assert.equal(
    normalizarVisitante({ nome: 'A', email: 'a@b.com', instituicao: 'y'.repeat(LIMITES.instituicao + 1) }).ok,
    false,
  )
})

test('normalizarVisitante aceita exatamente no limite', () => {
  const noLimite = 'x'.repeat(LIMITES.nome)
  assert.equal(normalizarVisitante({ nome: noLimite, email: 'a@b.com', instituicao: 'X' }).ok, true)
})

// --- resolução de rotas ----------------------------------------------------

test('rotaEstado sem base devolve a rota do membro, inalterada', () => {
  assert.equal(rotaEstado('', 'ro'), '/estados/ro')
})

test('rotaEstado com a base pública prefixa', () => {
  assert.equal(rotaEstado(BASE_PUBLICA, 'ro'), '/acervo-publico/estados/ro')
})

// O CASO QUE UM PREFIXO CEGO ERRARIA (spec, seção 1): /estados (a lista StatesList) não
// existe no recorte público. Prefixar daria '/acervo-publico/estados', rota inexistente.
test('rotaListaEstados: membro volta para a lista, visitante volta para o acervo', () => {
  assert.equal(rotaListaEstados(''), '/estados')
  assert.equal(rotaListaEstados(BASE_PUBLICA), '/acervo-publico')
})

// --- persistência local ----------------------------------------------------

function storageFake(inicial = {}) {
  const dados = { ...inicial }
  return {
    getItem: (k) => (k in dados ? dados[k] : null),
    setItem: (k, v) => { dados[k] = String(v) },
    removeItem: (k) => { delete dados[k] },
    _dados: dados,
  }
}

test('gravarVisitanteLocal e lerVisitanteLocal fazem a volta completa', () => {
  const s = storageFake()
  gravarVisitanteLocal(s, { uid: 'abc123', nome: 'Maria da Silva' })
  assert.deepEqual(lerVisitanteLocal(s), { uid: 'abc123', nome: 'Maria da Silva' })
})

test('lerVisitanteLocal devolve null quando não há nada gravado', () => {
  assert.equal(lerVisitanteLocal(storageFake()), null)
})

test('lerVisitanteLocal devolve null (sem lançar) se o conteúdo estiver corrompido', () => {
  assert.equal(lerVisitanteLocal(storageFake({ [CHAVE_LOCAL]: 'isto não é json' })), null)
})

test('lerVisitanteLocal devolve null se faltar uid ou nome', () => {
  assert.equal(lerVisitanteLocal(storageFake({ [CHAVE_LOCAL]: '{"nome":"Maria"}' })), null)
  assert.equal(lerVisitanteLocal(storageFake({ [CHAVE_LOCAL]: '{"uid":"abc"}' })), null)
})

test('lerVisitanteLocal devolve null quando não há storage (ambiente sem localStorage)', () => {
  assert.equal(lerVisitanteLocal(null), null)
})

test('limparVisitanteLocal remove a chave e não lança sem storage', () => {
  const s = storageFake({ [CHAVE_LOCAL]: '{"uid":"a","nome":"b"}' })
  limparVisitanteLocal(s)
  assert.equal(lerVisitanteLocal(s), null)
  assert.doesNotThrow(() => limparVisitanteLocal(null))
})
```

- [ ] **Step 2: Rode o teste e confirme que falha**

```bash
node --test src/lib/visitante.test.js
```
Esperado: FALHA com `Cannot find module` / `ERR_MODULE_NOT_FOUND` para `./visitante.js`.

- [ ] **Step 3: Implemente o mínimo**

Crie `src/lib/visitante.js`:

```js
// Lógica pura do visitante público (spec 2026-08-18): validação do cadastro básico,
// resolução das rotas do acervo e persistência local. Sem React e sem Firebase de
// propósito — é o núcleo que dá para testar com `node --test`.
import { normalizeEmail } from './membersStats.js'

export const BASE_PUBLICA = '/acervo-publico'
export const CHAVE_LOCAL = 'cbmro_visitante'

// Espelham os tamanhos da regra do Firestore (firestore.rules, match /visitantes/{uid}).
// Se um deles mudar lá, mude aqui: passar do limite faz o banco RECUSAR a gravação, e o
// visitante veria um erro genérico depois de preencher o formulário inteiro.
export const LIMITES = { nome: 200, email: 200, instituicao: 200 }

export function normalizarVisitante({ nome, email, instituicao } = {}) {
  const n = (nome ?? '').trim()
  const e = normalizeEmail(email)
  const i = (instituicao ?? '').trim()

  if (!n || !e || !i) {
    return { ok: false, erro: 'Preencha nome completo, e-mail e instituição.' }
  }
  // Validação deliberadamente frouxa: não confirmamos o e-mail (spec, seção 7), então
  // exigir formato rígido só barraria endereço institucional incomum sem nada em troca.
  if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(e)) {
    return { ok: false, erro: 'Digite um e-mail válido.' }
  }
  if (n.length > LIMITES.nome) return { ok: false, erro: `O nome deve ter até ${LIMITES.nome} caracteres.` }
  if (e.length > LIMITES.email) return { ok: false, erro: `O e-mail deve ter até ${LIMITES.email} caracteres.` }
  if (i.length > LIMITES.instituicao) return { ok: false, erro: `A instituição deve ter até ${LIMITES.instituicao} caracteres.` }

  return { ok: true, dados: { nome: n, email: e, instituicao: i } }
}

// `base` vazia = membro logado (rotas de sempre); BASE_PUBLICA = visitante.
export function rotaEstado(base, id) {
  return `${base ?? ''}/estados/${id}`
}

// ATENÇÃO: não é prefixo cego. A lista de estados (/estados, StatesList) NÃO faz parte do
// recorte público — prefixar daria '/acervo-publico/estados', rota que não existe. O
// visitante volta para a tabela do acervo, que é de onde ele veio.
export function rotaListaEstados(base) {
  return base ? base : '/estados'
}

export function lerVisitanteLocal(storage) {
  try {
    const cru = storage?.getItem(CHAVE_LOCAL)
    if (!cru) return null
    const v = JSON.parse(cru)
    if (!v || typeof v.uid !== 'string' || typeof v.nome !== 'string') return null
    return { uid: v.uid, nome: v.nome }
  } catch {
    return null   // conteúdo corrompido ou ambiente sem localStorage: trate como "não há visitante"
  }
}

export function gravarVisitanteLocal(storage, { uid, nome }) {
  try { storage?.setItem(CHAVE_LOCAL, JSON.stringify({ uid, nome })) } catch { /* ambiente sem localStorage */ }
}

export function limparVisitanteLocal(storage) {
  try { storage?.removeItem(CHAVE_LOCAL) } catch { /* ambiente sem localStorage */ }
}
```

- [ ] **Step 4: Rode o teste e confirme que passa**

```bash
node --test src/lib/visitante.test.js
```
Esperado: PASSA, todos os testes do arquivo.

- [ ] **Step 5: Rode a suíte inteira (nada quebrou)**

```bash
node --test
```
Esperado: PASSA. Antes desta tarefa eram 96 testes; agora são 96 + os novos.

- [ ] **Step 6: Commit**

```bash
git add src/lib/visitante.js src/lib/visitante.test.js
git commit -m "feat(publico): lógica pura do visitante (validação, rotas, storage)"
```

---

### Task 2: Contexto de prefixo do acervo (`AcervoBase`) e os 5 `navigate()`

Faz as três telas do acervo funcionarem nos dois endereços sem nenhum `if (visitante)` dentro delas.

**Files:**
- Create: `src/context/AcervoBaseContext.jsx`
- Modify: `src/pages/Legislations.jsx` (linha 51)
- Modify: `src/pages/StateDetail.jsx` (linhas 184 e 202)
- Modify: `src/pages/Search.jsx` (linha 185)

**Interfaces:**
- Consumes: `rotaEstado(base, id)`, `rotaListaEstados(base)`, `BASE_PUBLICA` de `src/lib/visitante.js` (Task 1).
- Produces:
  - `AcervoBaseProvider({ base, children })` — componente
  - `useAcervoNav() -> { irParaEstado(id: string): void, voltarParaEstados(): void }`

- [ ] **Step 1: Crie o contexto**

Crie `src/context/AcervoBaseContext.jsx`:

```jsx
// Prefixo de rota do acervo. Padrão '' = portal do membro (rotas de sempre); o visitante
// público monta as mesmas telas com base '/acervo-publico'. Existe para que Legislations,
// StateDetail e Search sejam REUSADAS sem fork e sem nenhum `if (visitante)` dentro delas.
import { createContext, useContext, useMemo } from 'react'
import { useNavigate } from 'react-router-dom'
import { rotaEstado, rotaListaEstados } from '../lib/visitante.js'

const AcervoBaseContext = createContext('')

export function AcervoBaseProvider({ base, children }) {
  return <AcervoBaseContext.Provider value={base ?? ''}>{children}</AcervoBaseContext.Provider>
}

export function useAcervoNav() {
  const base = useContext(AcervoBaseContext)
  const navigate = useNavigate()
  return useMemo(() => ({
    irParaEstado: (id) => navigate(rotaEstado(base, id)),
    voltarParaEstados: () => navigate(rotaListaEstados(base)),
  }), [base, navigate])
}
```

- [ ] **Step 2: Troque a navegação em `Legislations.jsx`**

Em `src/pages/Legislations.jsx`, troque o import de `useNavigate` pelo hook e o uso na linha 51:

```jsx
// antes:  import { useNavigate } from 'react-router-dom'
import { useAcervoNav } from '../context/AcervoBaseContext.jsx'

// antes:  const navigate = useNavigate()
const { irParaEstado } = useAcervoNav()

// antes:  onSelectState={id => navigate(`/estados/${id}`)}
onSelectState={id => irParaEstado(id)}
```

- [ ] **Step 3: Troque a navegação em `StateDetail.jsx`**

Em `src/pages/StateDetail.jsx`, mantenha `useParams` e remova `useNavigate`:

```jsx
// antes:  import { useParams, useNavigate } from 'react-router-dom'
import { useParams } from 'react-router-dom'
import { useAcervoNav } from '../context/AcervoBaseContext.jsx'

// antes:  const navigate = useNavigate()
const { voltarParaEstados } = useAcervoNav()

// linhas 184 e 202 — antes:  onClick={() => navigate('/estados')}
onClick={voltarParaEstados}
```

- [ ] **Step 4: Troque a navegação em `Search.jsx`**

```jsx
// antes:  import { useNavigate } from 'react-router-dom'
import { useAcervoNav } from '../context/AcervoBaseContext.jsx'

// antes:  const navigate = useNavigate()
const { irParaEstado } = useAcervoNav()

// antes:  onClick={() => navigate(`/estados/${state.id}`)}
onClick={() => irParaEstado(state.id)}
```

- [ ] **Step 5: Confirme que nenhuma navegação para `/estados` sobrou nessas telas**

```bash
grep -n "navigate(" src/pages/Legislations.jsx src/pages/StateDetail.jsx src/pages/Search.jsx
```
Esperado: **nenhuma linha**. Se sobrar alguma, ela escaparia do prefixo e levaria o visitante para fora do recorte.

- [ ] **Step 6: Confirme que o build passa e a suíte segue verde**

```bash
npm run build && node --test
```
Esperado: build sem erro; testes passando. (O membro ainda não vê diferença nenhuma — `base` é `''` por padrão, então as rotas de hoje continuam idênticas.)

- [ ] **Step 7: Commit**

```bash
git add src/context/AcervoBaseContext.jsx src/pages/Legislations.jsx src/pages/StateDetail.jsx src/pages/Search.jsx
git commit -m "refactor(acervo): navegação do acervo via contexto de prefixo (AcervoBase)"
```

---

### Task 3: Sessão do visitante — `AuthProvider` blindado, gravação e `VisitanteProvider`

**Files:**
- Modify: `src/lib/auth.jsx` (bloco `onAuthStateChanged`, linhas 19-24)
- Create: `src/lib/visitantesData.js`
- Create: `src/lib/visitante.jsx`
- Modify: `src/main.jsx`

**Interfaces:**
- Consumes: `normalizarVisitante`, `lerVisitanteLocal`, `gravarVisitanteLocal`, `limparVisitanteLocal` de `src/lib/visitante.js` (Task 1); `auth`, `db` de `src/lib/firebase.js`.
- Produces:
  - `registrarVisitante({ uid, nome, email, instituicao }) -> Promise<void>` (`visitantesData.js`)
  - `subscribeVisitantes(onChange, onError) -> () => void` (`visitantesData.js`)
  - `VisitanteProvider({ children })` e `useVisitante() -> { visitante, carregando, erro, entrar(campos) }` onde `visitante` é `{ uid, nome } | null` e `entrar` é `(campos) => Promise<boolean>` (`visitante.jsx`)

- [ ] **Step 1: Blinde o `AuthProvider` contra a sessão anônima — FAÇA ISTO PRIMEIRO**

Sem este passo o resto quebra de forma difícil de diagnosticar. Hoje, `onAuthStateChanged` (`src/lib/auth.jsx`) roda para **qualquer** sessão do Firebase, inclusive a anônima. Um usuário anônimo não tem e-mail, então o código atual faria `normalizeEmail(null)` → `''` → `doc(db, 'members', '')`, que é **caminho de documento vazio** (erro do Firestore), e no ramo seguinte chamaria `signOut(auth)` — **matando a sessão do visitante** que a Task 3 acabou de criar.

Em `src/lib/auth.jsx`, troque a guarda inicial:

```js
    const unsub = onAuthStateChanged(auth, async (fbUser) => {
      // Sessão ANÔNIMA é do visitante do acervo público (src/lib/visitante.jsx) e não
      // pertence a este provedor: ela não tem e-mail, então a checagem de members faria
      // doc(db,'members','') — caminho vazio — e o signOut abaixo derrubaria o visitante.
      // `user` continua significando "membro autorizado", e só isso.
      if (!fbUser || fbUser.isAnonymous) {
        setUser(null); setNaoAutorizado(false); setPendente(false); setLoading(false)
        return
      }
```

- [ ] **Step 2: Escreva o acesso ao Firestore**

Crie `src/lib/visitantesData.js`:

```js
// Registro dos visitantes do acervo público (spec 2026-08-18). Coleção `visitantes`,
// documento identificado pelo uid da sessão ANÔNIMA — não há e-mail autenticado aqui, e
// por isso este registro nunca se confunde com `members`.
import {
  collection, doc, setDoc, onSnapshot, query, orderBy, serverTimestamp,
} from 'firebase/firestore'
import { db } from './firebase.js'

const COL = 'visitantes'

// merge:true de propósito: se a pessoa limpar o localStorage e preencher de novo com a
// MESMA sessão anônima viva, isto ATUALIZA o registro (ultimoAcesso) em vez de duplicar.
// `criadoEm` só é escrito quando ainda não existe, preservando o primeiro acesso.
export async function registrarVisitante({ uid, nome, email, instituicao, primeiraVez = true }) {
  await setDoc(doc(db, COL, uid), {
    uid, nome, email, instituicao,
    ...(primeiraVez ? { criadoEm: serverTimestamp() } : {}),
    ultimoAcesso: serverTimestamp(),
  }, { merge: true })
}

export function subscribeVisitantes(onChange, onError) {
  const q = query(collection(db, COL), orderBy('ultimoAcesso', 'desc'))
  return onSnapshot(q,
    (snap) => onChange(snap.docs.map(d => ({ id: d.id, ...d.data() }))),
    (err) => { if (onError) onError(err) },
  )
}
```

- [ ] **Step 3: Escreva o provedor do visitante**

Crie `src/lib/visitante.jsx`:

```jsx
// Sessão do visitante do acervo público. Independente do AuthProvider: nenhum dado passa
// de um para o outro. No React a aninhagem de provedores é inevitável, mas a
// INDEPENDÊNCIA é real — este módulo não importa auth.jsx, e auth.jsx ignora sessões
// anônimas (ver a guarda `fbUser.isAnonymous` lá).
import { createContext, useContext, useEffect, useState } from 'react'
import { signInAnonymously, onAuthStateChanged } from 'firebase/auth'
import { auth } from './firebase.js'
import { registrarVisitante } from './visitantesData.js'
import {
  normalizarVisitante, lerVisitanteLocal, gravarVisitanteLocal, limparVisitanteLocal,
} from './visitante.js'

const VisitanteContext = createContext(null)

export function VisitanteProvider({ children }) {
  const [visitante, setVisitante] = useState(null)
  const [carregando, setCarregando] = useState(true)
  const [erro, setErro] = useState('')

  // Só considera visitante conhecido quando o localStorage E a sessão anônima do Firebase
  // concordam. Caso real que isto resolve: a pessoa entrou como visitante, depois logou
  // como membro (o login SUBSTITUI a sessão anônima) e saiu — o localStorage ficaria
  // apontando para um uid que não existe mais, e a gravação seria recusada pela regra
  // `request.auth.uid == uid`. Melhor pedir o cadastro de novo do que falhar depois.
  useEffect(() => {
    const unsub = onAuthStateChanged(auth, (fbUser) => {
      const local = lerVisitanteLocal(globalThis.localStorage)
      if (fbUser?.isAnonymous && local && local.uid === fbUser.uid) {
        setVisitante(local)
      } else {
        if (local) limparVisitanteLocal(globalThis.localStorage)
        setVisitante(null)
      }
      setCarregando(false)
    })
    return unsub
  }, [])

  // Devolve true quando entrou. Erro fica em `erro` — e a tela MOSTRA (nunca só console).
  const entrar = async (campos) => {
    setErro('')
    const v = normalizarVisitante(campos)
    if (!v.ok) { setErro(v.erro); return false }
    try {
      // Já existe sessão anônima? Então este cadastro é REPETIÇÃO (a pessoa limpou o
      // localStorage) e `criadoEm` não pode ser reescrito — senão o "primeiro acesso" da
      // lista do admin viraria a data de hoje, todas as vezes. signInAnonymously reaproveita
      // a sessão existente em vez de criar outra, então precisamos olhar ANTES de chamar.
      const jaTinhaSessao = Boolean(auth.currentUser?.isAnonymous)
      const cred = await signInAnonymously(auth)
      const uid = cred.user.uid
      await registrarVisitante({ uid, ...v.dados, primeiraVez: !jaTinhaSessao })
      gravarVisitanteLocal(globalThis.localStorage, { uid, nome: v.dados.nome })
      setVisitante({ uid, nome: v.dados.nome })
      return true
    } catch (e) {
      console.error('Falha ao registrar visitante:', e)
      setErro(
        e?.code === 'auth/operation-not-allowed'
          ? 'O acesso público ainda não foi habilitado no servidor. Avise o administrador do portal.'
          : 'Não foi possível concluir o cadastro agora. Tente novamente.',
      )
      return false
    }
  }

  return (
    <VisitanteContext.Provider value={{ visitante, carregando, erro, entrar }}>
      {children}
    </VisitanteContext.Provider>
  )
}

export function useVisitante() {
  const ctx = useContext(VisitanteContext)
  if (ctx === null) throw new Error('useVisitante precisa estar dentro de <VisitanteProvider>')
  return ctx
}
```

A mensagem de `auth/operation-not-allowed` existe porque é **exatamente** o erro que aparece enquanto o provedor Anônimo não estiver habilitado no console do Firebase (Task 5). Sem ela, o sintoma seria "não funciona" sem pista nenhuma.

- [ ] **Step 4: Ligue o provedor em `src/main.jsx`**

```jsx
import { VisitanteProvider } from './lib/visitante.jsx'

// ...
    <BrowserRouter>
      <AuthProvider>
        <ScenarioProvider>
          <VisitanteProvider>
            <App />
          </VisitanteProvider>
        </ScenarioProvider>
      </AuthProvider>
    </BrowserRouter>
```

- [ ] **Step 5: Verifique o build e a suíte**

```bash
npm run build && node --test
```
Esperado: build sem erro; testes passando (nenhum teste novo nesta tarefa — o que dava para testar puro já está na Task 1; o resto é integração com Firebase, que este projeto não tem como testar sem rede).

- [ ] **Step 6: Commit**

```bash
git add src/lib/auth.jsx src/lib/visitantesData.js src/lib/visitante.jsx src/main.jsx
git commit -m "feat(publico): sessão anônima do visitante e registro no Firestore"
```

---

### Task 4: Telas do acervo público e as rotas

**Files:**
- Create: `src/components/MarcaPortal.jsx`
- Create: `src/pages/CadastroVisitante.jsx`
- Create: `src/pages/AcervoPublico.jsx`
- Modify: `src/App.jsx` (`Header`, `LoggedOutRoutes`, bloco de rotas do portal logado)
- Modify: `src/index.css` (bloco novo `.pub-*`, ao final do arquivo)

**Interfaces:**
- Consumes: `useVisitante()` (Task 3), `AcervoBaseProvider` (Task 2), `BASE_PUBLICA` (Task 1), páginas `Legislations`, `StateDetail`, `Search`.
- Produces: `MarcaPortal()` — bloco de marca reutilizável; `AcervoPublico()` — casca pública com rotas aninhadas.

- [ ] **Step 1: Extraia o bloco de marca do cabeçalho**

Crie `src/components/MarcaPortal.jsx` com o conteúdo que hoje está dentro de `Header` em `src/App.jsx` (brasão + título + régua + subtítulo):

```jsx
// Bloco de marca do cabeçalho, compartilhado entre a casca do portal (App.jsx) e a casca
// do acervo público (AcervoPublico.jsx) — para as duas não divergirem visualmente.
export default function MarcaPortal() {
  return (
    <>
      <img
        className="app-header-emblem"
        src="/BrasaoCBMRO2D-COMPLETO.png"
        onError={e => { if (!e.currentTarget.dataset.fb) { e.currentTarget.dataset.fb = '1'; e.currentTarget.src = '/brasao-cbmro.svg' } }}
        alt="Brasão do Corpo de Bombeiros Militar de Rondônia"
      />
      <div className="app-header-text">
        <h1 className="app-header-title">
          Portal de Legislação dos Corpos de Bombeiros Militares
        </h1>
        <div className="app-header-rule" />
        <div className="app-header-sub">
          Corpo de Bombeiros Militar de Rondônia · CBMRO
        </div>
      </div>
    </>
  )
}
```

Em `src/App.jsx`, no `Header`, substitua esse mesmo trecho por `<MarcaPortal />` e adicione o import. O `Header` continua com o botão ☰ e o `HeaderUserBox` — só o miolo de marca sai.

- [ ] **Step 2: Escreva o formulário de cadastro**

Crie `src/pages/CadastroVisitante.jsx` (reusa as classes `.login-*` já existentes no `index.css`, linhas 2317+):

```jsx
import { useState } from 'react'
import { Link } from 'react-router-dom'
import { useVisitante } from '../lib/visitante.jsx'

export default function CadastroVisitante() {
  const { entrar, erro } = useVisitante()
  const [nome, setNome] = useState('')
  const [email, setEmail] = useState('')
  const [instituicao, setInstituicao] = useState('')
  const [enviando, setEnviando] = useState(false)

  const submeter = async (e) => {
    e.preventDefault()
    setEnviando(true)
    const ok = await entrar({ nome, email, instituicao })
    // Deu certo: o VisitanteProvider troca a tela sozinho. Deu errado: `erro` aparece
    // abaixo e o botão volta a ficar clicável.
    if (!ok) setEnviando(false)
  }

  return (
    <div className="login-wrap">
      <form className="login-card login-card--wide" onSubmit={submeter}>
        <h2 className="login-title">Acervo Legal — consulta pública</h2>
        <p className="login-sub">
          Legislação comparada dos 27 Corpos de Bombeiros Militares. Informe seus dados para consultar.
        </p>

        {erro && <div className="form-error">{erro}</div>}

        <label className="login-label">Nome completo
          <input className="login-input" type="text" value={nome}
            onChange={e => setNome(e.target.value)} autoComplete="name" maxLength={200} required />
        </label>
        <label className="login-label">E-mail
          <input className="login-input" type="email" value={email}
            onChange={e => setEmail(e.target.value)} autoComplete="email" maxLength={200} required />
        </label>
        <label className="login-label">Instituição ou órgão
          <input className="login-input" type="text" value={instituicao}
            onChange={e => setInstituicao(e.target.value)} maxLength={200} required
            placeholder="Ex.: CBMPA, Prefeitura de Porto Velho, autônomo" />
        </label>

        <button className="login-btn" type="submit" disabled={enviando}>
          {enviando ? 'Entrando…' : 'Consultar o acervo'}
        </button>

        <p className="pub-lgpd">
          Estes dados ficam registrados como controle de acesso ao acervo e são vistos
          apenas pelo administrador do portal. Não há envio de mensagens.
        </p>

        <div className="login-foot">
          <span className="login-foot-txt">É membro do grupo de trabalho?</span>
          <Link className="login-link" to="/login">Entrar</Link>
        </div>
      </form>
    </div>
  )
}
```

- [ ] **Step 3: Escreva a casca pública**

Crie `src/pages/AcervoPublico.jsx`:

```jsx
// Casca do acervo público: cabeçalho próprio, navegação de dois itens e as MESMAS telas
// do acervo do portal, montadas sob o prefixo /acervo-publico (AcervoBaseProvider).
// Ela vive FORA do portal logado de propósito — a fronteira entre visitante e membro é o
// caminho da URL, não uma condição de login (spec, seção 1).
import { Routes, Route, NavLink, Navigate, Link } from 'react-router-dom'
import { Library, Search as SearchIcon, LogIn } from 'lucide-react'
import MarcaPortal from '../components/MarcaPortal.jsx'
import Legislations from './Legislations.jsx'
import StateDetail from './StateDetail.jsx'
import SearchPage from './Search.jsx'
import CadastroVisitante from './CadastroVisitante.jsx'
import { useVisitante } from '../lib/visitante.jsx'
import { AcervoBaseProvider } from '../context/AcervoBaseContext.jsx'
import { BASE_PUBLICA } from '../lib/visitante.js'

export default function AcervoPublico() {
  const { visitante, carregando } = useVisitante()

  if (carregando) return <div style={{ padding: 32 }}>Carregando…</div>
  if (!visitante) return <CadastroVisitante />

  return (
    <div className="pub-shell">
      <header className="app-header">
        <MarcaPortal />
        <div className="app-header-user">
          <span className="pub-selo">Consulta pública</span>
          <Link className="app-header-user-exit" to="/login" title="Entrar como membro">
            <LogIn size={16} /> Sou membro
          </Link>
        </div>
      </header>

      <nav className="pub-nav">
        <NavLink end to="/acervo-publico" className={({ isActive }) => `pub-nav-item${isActive ? ' active' : ''}`}>
          <Library size={16} /> Acervo Legal
        </NavLink>
        <NavLink to="/acervo-publico/busca" className={({ isActive }) => `pub-nav-item${isActive ? ' active' : ''}`}>
          <SearchIcon size={16} /> Busca
        </NavLink>
        <span className="pub-nav-quem">Olá, {visitante.nome}</span>
      </nav>

      <main className="pub-main">
        {/* Sem ScenarioSwitcher: o acervo é o mesmo nos cenários LOB atual e futura
            (states_data.json e organs_detail/ são compartilhados), então escolher
            cenário não mudaria nada nestas telas. */}
        <AcervoBaseProvider base={BASE_PUBLICA}>
          <Routes>
            <Route index element={<Legislations />} />
            <Route path="estados/:stateId" element={<StateDetail />} />
            <Route path="busca" element={<SearchPage />} />
            {/* Endereço fora do recorte dentro do prefixo: devolve ao acervo. */}
            <Route path="*" element={<Navigate to="/acervo-publico" replace />} />
          </Routes>
        </AcervoBaseProvider>
      </main>
    </div>
  )
}
```

- [ ] **Step 4: Ligue as rotas nos DOIS ramos do `App.jsx`**

Em `LoggedOutRoutes` (visitante deslogado — a rota precisa vir **antes** do `path="*"`, que hoje manda tudo para `/login`):

```jsx
    <Routes>
      <Route path="/login" element={<Login />} />
      <Route path="/solicitar-acesso" element={<SolicitarAcesso />} />
      {/* Acervo público: única porta que responde sem login (spec 2026-08-18). Precisa
          vir antes do catch-all abaixo, senão cai no redirecionamento para /login. */}
      <Route path="/acervo-publico/*" element={<AcervoPublico />} />
      <Route path="*" element={<Navigate to="/login" replace state={{ from }} />} />
    </Routes>
```

E no bloco de rotas do portal logado, junto das outras rotas de compatibilidade:

```jsx
          {/* Membro que abre o link público vai para o acervo completo — ele já tem tudo. */}
          <Route path="/acervo-publico/*" element={<Navigate to="/legislacoes" replace />} />
```

Adicione o import: `import AcervoPublico from './pages/AcervoPublico.jsx'`.

- [ ] **Step 5: Acrescente o CSS ao final de `src/index.css`**

`.app-header` é `position: fixed` (linha 141) porque o portal logado tem sidebar fixa e conteúdo deslocado. A casca pública não tem sidebar, então o cabeçalho volta a fluir normalmente — é o que a primeira regra abaixo faz.

```css
/* ===== Acervo público (visitante sem login) — spec 2026-08-18 ===== */
.pub-shell { min-height: 100vh; background: #eef1f6; }
/* O cabeçalho do portal é `position: fixed` (layout com sidebar). Aqui não há sidebar:
   ele volta a ocupar espaço no fluxo, senão a navegação abaixo ficaria por baixo dele. */
.pub-shell .app-header { position: static; }
.pub-selo { font-size: 11.5px; font-weight: 700; letter-spacing: .04em; text-transform: uppercase;
  background: rgba(255,255,255,.16); color: #fff; border-radius: 12px; padding: 4px 10px; margin-right: 10px; }
.pub-nav { display: flex; align-items: center; gap: 6px; flex-wrap: wrap;
  background: #121d3d; padding: 8px 20px; }
.pub-nav-item { display: inline-flex; align-items: center; gap: 7px; text-decoration: none;
  color: #c3cbdd; font-size: 13.5px; font-weight: 600; padding: 7px 13px; border-radius: 8px; }
.pub-nav-item:hover { background: rgba(255,255,255,.08); color: #fff; }
.pub-nav-item.active { background: #c8102e; color: #fff; }
.pub-nav-quem { margin-left: auto; color: #8e99b4; font-size: 12.5px; }
.pub-main { padding: 22px 20px 40px; max-width: 1240px; margin: 0 auto; }
.pub-lgpd { font-size: 11.5px; color: #5a667f; line-height: 1.5; margin: 12px 0 0; }
@media (max-width: 700px) {
  .pub-nav { padding: 8px 12px; }
  .pub-nav-quem { width: 100%; margin: 4px 0 0; }
  .pub-main { padding: 16px 12px 32px; }
}
```

- [ ] **Step 6: Verifique build e suíte**

```bash
npm run build && node --test
```
Esperado: build sem erro; testes passando.

- [ ] **Step 7: Suba o dev server e entregue o link para conferência humana**

```bash
npm run dev -- --port 5173 --strictPort
```
Informe ao Ten. Tiago: http://localhost:5173/acervo-publico — **o agente não tem navegador**; a conferência visual é dele. Note que o cadastro só grava depois da Task 5 (provedor Anônimo habilitado); antes disso a tela deve mostrar a mensagem "O acesso público ainda não foi habilitado no servidor", e isso é o comportamento correto, não um defeito.

- [ ] **Step 8: Commit**

```bash
git add src/components/MarcaPortal.jsx src/pages/CadastroVisitante.jsx src/pages/AcervoPublico.jsx src/App.jsx src/index.css
git commit -m "feat(publico): casca do acervo público, cadastro do visitante e rotas"
```

---

### Task 5: Regra do Firestore e instruções de configuração

**Files:**
- Modify: `firestore.rules`
- Modify: `docs/FIREBASE_SETUP.md`

**Interfaces:**
- Consumes: a função `isAdmin()` que já existe no topo do `firestore.rules`.
- Produces: coleção `visitantes` legível pelo admin e gravável pelo próprio dono anônimo.

- [ ] **Step 1: Acrescente o bloco ao `firestore.rules`**

Dentro de `match /databases/{database}/documents {`, depois do bloco `match /conferencia/{id}`:

```
    // Visitantes do acervo público (spec 2026-08-18). Sessão ANÔNIMA: não há e-mail, logo
    // isMember() é falso para eles e todas as coleções da curadoria seguem fechadas pelo
    // BANCO, não só pela interface. Aqui cada visitante só escreve o PRÓPRIO documento.
    match /visitantes/{uid} {
      allow read, delete: if isAdmin();
      allow create, update: if request.auth != null
        && request.auth.uid == uid
        && request.resource.data.uid == uid
        && request.resource.data.keys().hasOnly(
             ['uid','nome','email','instituicao','criadoEm','ultimoAcesso'])
        && request.resource.data.nome is string
        && request.resource.data.nome.size() > 0
        && request.resource.data.nome.size() <= 200
        && request.resource.data.email is string
        && request.resource.data.email.size() <= 200
        && request.resource.data.instituicao is string
        && request.resource.data.instituicao.size() <= 200;
    }
```

- [ ] **Step 2: Confirme que nenhuma regra existente mudou**

```bash
git diff firestore.rules
```
Esperado: **apenas adição** do bloco acima. Se alguma linha de `members`, `suggestions`, `finalTexts`, `config`, `decisions` ou `conferencia` aparecer no diff, desfaça — esta entrega não afrouxa nada existente.

- [ ] **Step 3: Documente os dois passos manuais no console**

Acrescente ao final de `docs/FIREBASE_SETUP.md`:

```markdown
## Acervo público (visitante sem login) — 2026-08-18

Dois passos **manuais** no console do projeto `revisao-minuta-cbmro-6f248`, na conta
institucional (o CLI local está numa conta pessoal sem acesso ao projeto):

1. **Authentication → Sign-in method → Anônimo → Ativar.** Sem isso o cadastro do
   visitante falha com `auth/operation-not-allowed`, e a tela mostra
   "O acesso público ainda não foi habilitado no servidor".
2. **Firestore → Regras:** publicar o `firestore.rules` deste repositório, que passou a
   conter o bloco `match /visitantes/{uid}`.

Conferência depois de publicar: abrir `/acervo-publico` numa janela anônima, preencher o
cadastro e verificar se a pessoa aparece em `/acessos`, seção "Visitantes do acervo
público".
```

- [ ] **Step 4: Commit**

```bash
git add firestore.rules docs/FIREBASE_SETUP.md
git commit -m "feat(publico): regra do Firestore para a coleção visitantes"
```

---

### Task 6: Seção "Visitantes do acervo público" em `/acessos`

**Files:**
- Modify: `src/pages/Acessos.jsx`
- Modify: `src/index.css` (uma regra, junto do bloco `.pub-*`)

**Interfaces:**
- Consumes: `subscribeVisitantes(onChange, onError)` de `src/lib/visitantesData.js` (Task 3); `AvisoSincronizacao` de `src/components/AvisoSincronizacao.jsx`.

- [ ] **Step 1: Assine o feed com estado de erro visível**

Em `src/pages/Acessos.jsx`, junto dos outros `useState`/`useEffect` do topo do componente:

```jsx
import { subscribeVisitantes } from '../lib/visitantesData.js'
import AvisoSincronizacao from '../components/AvisoSincronizacao.jsx'

// ... dentro de Acessos():
  const [visitantes, setVisitantes] = useState([])
  const [erroVisitantes, setErroVisitantes] = useState(false)

  // Erro visível na tela, nunca só no console (AR-04): sem isto, uma queda do feed
  // deixaria a seção mostrando "nenhum visitante" — que é indistinguível de "ninguém
  // acessou ainda" e mente para o administrador.
  useEffect(() => subscribeVisitantes(
    (lista) => { setVisitantes(lista); setErroVisitantes(false) },
    (e) => { console.error('Erro ao carregar visitantes:', e); setErroVisitantes(true) },
  ), [])
```

- [ ] **Step 2: Renderize a seção, somente leitura**

Antes do `</div>` que fecha `.acc-wrap`, ao final do JSX de `Acessos`:

```jsx
      <h3 className="acc-sec-title">Visitantes do acervo público</h3>
      <p className="acc-sub">
        Quem consultou o acervo pela página pública, sem login. Registro de histórico — não há
        aprovação nem bloqueio: o acervo é público por decisão do comando.
      </p>

      <AvisoSincronizacao visivel={erroVisitantes}>
        Não foi possível carregar a lista de visitantes agora — o que aparece abaixo pode estar
        incompleto ou desatualizado.
      </AvisoSincronizacao>

      <div className="acc-panel">
        <table className="acc-table">
          <thead>
            <tr>
              <th>Visitante</th><th>Instituição</th><th>Primeiro acesso</th><th>Último acesso</th>
            </tr>
          </thead>
          <tbody>
            {visitantes.length === 0 && !erroVisitantes && (
              <tr><td colSpan={4} className="acc-mail">Nenhum visitante registrado até agora.</td></tr>
            )}
            {visitantes.map(v => (
              <tr key={v.id}>
                <td>
                  <div className="acc-nome">{v.nome}</div>
                  <div className="acc-mail">{v.email}</div>
                </td>
                <td className="acc-papel">{v.instituicao}</td>
                <td className={formatLogin(v.criadoEm) ? 'acc-quando' : 'acc-nunca'}>
                  {formatLogin(v.criadoEm) ?? '—'}
                </td>
                <td className={formatLogin(v.ultimoAcesso) ? 'acc-quando' : 'acc-nunca'}>
                  {formatLogin(v.ultimoAcesso) ?? '—'}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
```

`formatLogin` já existe no topo do arquivo (linha 9) e trata timestamp do Firestore — reuse, não duplique.

- [ ] **Step 3: Acrescente a classe do título de seção ao `src/index.css`**

```css
.acc-sec-title { font-size: 17px; color: #121d3d; margin: 28px 0 2px; }
```

- [ ] **Step 4: Verifique build e suíte**

```bash
npm run build && node --test
```
Esperado: build sem erro; testes passando.

- [ ] **Step 5: Commit**

```bash
git add src/pages/Acessos.jsx src/index.css
git commit -m "feat(publico): lista de visitantes do acervo em /acessos"
```

---

### Task 7: Documentação do repositório

**Files:**
- Modify: `CLAUDE.md`
- Modify: `.claude/PENDENCIAS.md`
- Modify: `src/pages/Manual.jsx`

- [ ] **Step 1: Registre a arquitetura no `CLAUDE.md`**

Na seção "Revisão Colaborativa da Minuta (Firebase…)", depois do parágrafo de **Rotas/telas**, acrescente:

```markdown
**Terceiro perfil — acervo público (2026-08-18, spec `2026-08-18-acervo-publico-visitante-design.md`):**
`/acervo-publico` responde **sem login**, fora do portal autenticado. O visitante preenche um
cadastro básico (nome, e-mail, instituição), entra por **sessão anônima do Firebase** e enxerga
só o Acervo (`Legislations`), a ficha do estado e a busca — montadas sob o prefixo pelo
`AcervoBaseProvider` (`src/context/AcervoBaseContext.jsx`), sem fork das telas.
**O visitante NUNCA vira `user`**: `VisitanteProvider` (`src/lib/visitante.jsx`) é independente
do `AuthProvider`, que agora ignora sessões anônimas (`fbUser.isAnonymous`) — sem essa guarda
a checagem de membro faria `doc(db,'members','')` e o `signOut` derrubaria o visitante.
Registro em `visitantes/{uid}` (só o admin lê; `isMember()` continua exigindo `token.email`,
então a curadoria segue fechada ao visitante pelo BANCO). Lógica pura testada em
`src/lib/visitante.js`. Atenção ao `voltarParaEstados()`: no visitante vai para
`/acervo-publico` e **não** para `/estados`, que está fora do recorte.
Exige o provedor **Anônimo** habilitado no console do Firebase (ver `docs/FIREBASE_SETUP.md`).
```

- [ ] **Step 2: Atualize o backlog**

Em `.claude/PENDENCIAS.md`, no topo da seção `## 🔴 Pendente`:

```markdown
- [ ] **Acervo público — dois passos manuais no console do Firebase** (entrega de
  18/08/2026). Na conta institucional (`revisao-minuta-cbmro-6f248`): (1) Authentication →
  Sign-in method → **Anônimo** → Ativar; (2) publicar o `firestore.rules`, que ganhou o
  bloco `match /visitantes/{uid}`. Sem o passo 1 o cadastro do visitante falha com
  `auth/operation-not-allowed` (a tela avisa isso em português). Ver
  `docs/FIREBASE_SETUP.md`, seção "Acervo público".
- [ ] **Acervo público — conferência visual das telas** (o agente não tem navegador). Roteiro
  de 7 itens no fim de `docs/superpowers/plans/2026-08-18-acervo-publico-visitante.md`.
```

E na seção de concluídas do mês:

```markdown
- [x] **Acervo público (terceiro perfil — visitante sem login)** — 18/08/2026. Rota própria
  `/acervo-publico` fora do portal autenticado, cadastro básico (nome, e-mail, instituição),
  sessão anônima do Firebase, coleção `visitantes` (só o admin lê) e lista somente leitura em
  `/acessos`. O visitante nunca vira `user`. Spec e plano em `docs/superpowers/`.
```

- [ ] **Step 3: Documente no Manual de uso**

Em `src/pages/Manual.jsx`, no array `SECTIONS`, logo **depois** da seção `id: 'acervo'` (linha 62), acrescente:

```jsx
  {
    id: 'acervo-publico', title: 'Acervo Legal — consulta pública',
    body: (
      <>
        <p>
          Existe um endereço <b>público</b> do Acervo, para divulgar a quem só precisa
          consultar a legislação e não participa da elaboração das minutas:
          <b> /acervo-publico</b>. Serve para ofício, site institucional ou QR code.
        </p>
        <ul>
          <li>Não exige login e senha: a pessoa informa <b>nome, e-mail e instituição</b> e já entra.</li>
          <li>Ela enxerga <b>apenas</b> o Acervo, a ficha de cada estado e a Busca. Nenhuma minuta,
              nenhum subsídio, nenhuma tela de curadoria.</li>
          <li>O navegador lembra o cadastro: quem volta não preenche de novo.</li>
          <li>Quem entrou aparece em <b>Acessos</b>, na seção <b>Visitantes do acervo público</b> —
              é registro de histórico, sem aprovação e sem bloqueio.</li>
        </ul>
        <div className="manual-callout">
          <b>Por que não tem senha.</b> Os documentos do acervo são legislação pública de outros
          Corpos de Bombeiros. O cadastro existe para o comando saber quem consulta, não para
          restringir o acesso.
        </div>
      </>
    ),
  },
```

- [ ] **Step 4: Verifique build e suíte**

```bash
npm run build && node --test
```
Esperado: build sem erro; testes passando.

- [ ] **Step 5: Commit**

```bash
git add CLAUDE.md .claude/PENDENCIAS.md src/pages/Manual.jsx
git commit -m "docs: registra o perfil público do acervo (CLAUDE, backlog e manual)"
```

---

## Conferência final (humana, não do agente)

Com o provedor Anônimo já habilitado e as regras publicadas, o Ten. Tiago verifica em http://localhost:5173:

1. Janela anônima em `/acervo-publico` → aparece o formulário; preenchido, entra no Acervo.
2. Recarregar a página **não** pede o cadastro de novo.
3. `/acervo-publico/estados/ro` abre a ficha; "voltar" retorna a `/acervo-publico` (nunca a `/estados`).
4. Como visitante, digitar `/minuta`, `/regulamento` ou `/acessos` na barra de endereço **não** abre nada da curadoria (cai no `/login`, porque essas rotas vivem no portal autenticado).
5. Logado como membro, abrir `/acervo-publico` leva a `/legislacoes`.
6. Em `/acessos`, o visitante recém-cadastrado aparece na seção "Visitantes do acervo público".
7. Como participante com escopo `servico`, nada mudou: o recorte do Regulamento de Serviço continua igual.
