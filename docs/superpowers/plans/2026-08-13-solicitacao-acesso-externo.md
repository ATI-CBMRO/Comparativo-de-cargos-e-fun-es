# Solicitação de Acesso Externo — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Substituir o convite-primeiro por um formulário público de solicitação de acesso
(nome completo, nome de guerra, cidade → comando → unidade em cascata, e-mail, senha),
com aprovação manual do admin antes de liberar o acesso.

**Architecture:** Nova tela pública `/solicitar-acesso` cria a conta no Firebase Auth e, na
sequência, grava `members/{email}` com `ativo:false, status:'pendente'` (nova regra do
Firestore permite esse self-create restrito). O admin vê uma seção nova em `/acessos` e
aprova (`ativo:true`) ou recusa (`status:'recusado'`). O fluxo de convite manual existente
não é alterado — é um caminho adicional, lado a lado.

**Tech Stack:** React 18 + Vite, React Router, Firebase (Auth e-mail/senha + Firestore),
testes com `node --test` (`npm test`).

**Spec:** `docs/superpowers/specs/2026-08-13-solicitacao-acesso-externo-design.md`

## Global Constraints

- Não alterar o comportamento de `/cadastro` (convite manual do admin) — é caminho
  intocado, ao lado do novo.
- A lista de cidades/unidades vem dos dados reais do Sistema ATI (`prisma/seed.ts`), sem
  inventar nomes.
- Nenhum e-mail automático — aviso de aprovação é manual (fora do sistema).
- Reaproveitar as classes CSS `.login-*` e `.acc-*` já existentes; só adicionar o que
  faltar, nunca redefinir uma classe existente.
- `npm test` deve continuar passando a cada task.

---

## Task 1: Dados e cascata Cidade → Comando → Unidade

**Files:**
- Create: `src/lib/unidadesCbmro.js`
- Test: `src/lib/unidadesCbmro.test.js`

**Interfaces:**
- Produces: `UNIDADES_CBMRO` (array), `cidadesDisponiveis(): string[]`,
  `comandosPorCidade(cidade: string): string[]`,
  `unidadesPorCidadeEComando(cidade: string, comando: string): string[]`
  — usados pela Task 6 (`SolicitarAcesso.jsx`).

- [ ] **Step 1: Write the failing test**

```js
// src/lib/unidadesCbmro.test.js
import { test } from 'node:test'
import assert from 'node:assert/strict'
import { cidadesDisponiveis, comandosPorCidade, unidadesPorCidadeEComando } from './unidadesCbmro.js'

test('cidadesDisponiveis: 17 cidades reais, ordenadas, sem repetição', () => {
  const cidades = cidadesDisponiveis()
  assert.equal(cidades.length, 17)
  assert.ok(cidades.includes('Porto Velho'))
  assert.ok(cidades.includes('Buritis'))
  assert.deepEqual(cidades, [...cidades].sort((a, b) => a.localeCompare(b, 'pt-BR')))
})

test('comandosPorCidade: cidade-satélite tem COB e CAT', () => {
  assert.deepEqual(comandosPorCidade('Buritis'), ['CAT', 'COB I'])
})

test('comandosPorCidade: Vilhena também tem CEEI (CMDPII-2)', () => {
  assert.deepEqual(comandosPorCidade('Vilhena'), ['CAT', 'CEEI', 'COB II'])
})

test('comandosPorCidade: Porto Velho concentra os comandos administrativos', () => {
  const comandos = comandosPorCidade('Porto Velho')
  assert.equal(comandos.length, 14)
  assert.ok(comandos.includes('COB I'))
  assert.ok(comandos.includes('CAT'))
  assert.ok(comandos.includes('Corregedoria'))
})

test('comandosPorCidade: cidade inexistente retorna lista vazia', () => {
  assert.deepEqual(comandosPorCidade('Cidade Que Não Existe'), [])
})

test('unidadesPorCidadeEComando: Buritis/CAT tem só o SAT local', () => {
  assert.deepEqual(unidadesPorCidadeEComando('Buritis', 'CAT'), ['DAT - Ariquemes / SAT - Buritis'])
})

test('unidadesPorCidadeEComando: Buritis/COB I tem só o SGBM local', () => {
  assert.deepEqual(unidadesPorCidadeEComando('Buritis', 'COB I'), ['5º GBM / 3º SGBM'])
})

test('unidadesPorCidadeEComando: Porto Velho/COB I tem 3 unidades, ordenadas', () => {
  assert.deepEqual(
    unidadesPorCidadeEComando('Porto Velho', 'COB I'),
    ['1º GBM', '1º GBM / 1º SGBM', 'GBS'],
  )
})
```

- [ ] **Step 2: Run test to verify it fails**

Run: `npm test`
Expected: FAIL — `Cannot find module './unidadesCbmro.js'`

- [ ] **Step 3: Write the implementation**

```js
// src/lib/unidadesCbmro.js
// Dados reais das unidades do CBMRO (63 unidades, 17 cidades), copiados do Sistema ATI
// (prisma/seed.ts do projeto sistema-ati-2026) — não inventar/alterar nomes aqui.
// "comando" = coordenadoria (COB I/II, CAT, CEEI, COA, Comando Geral, e os órgãos
// administrativos de sede única). Sistemas sem conexão entre si: esta lista é uma cópia,
// não uma sincronização ao vivo.

export const UNIDADES_CBMRO = [
  // COB I — Coordenadoria Operacional de Bombeiros I
  { unidade: '1º GBM', cidade: 'Porto Velho', comando: 'COB I' },
  { unidade: '1º GBM / 1º SGBM', cidade: 'Porto Velho', comando: 'COB I' },
  { unidade: '1º GBM / 2º SGBM', cidade: 'Guajará-Mirim', comando: 'COB I' },
  { unidade: '1º GBM / 3º SGBM', cidade: 'Candeias do Jamari', comando: 'COB I' },
  { unidade: '2º GBM', cidade: 'Ji-Paraná', comando: 'COB I' },
  { unidade: '2º GBM / 1º SGBM', cidade: 'Ji-Paraná', comando: 'COB I' },
  { unidade: '2º GBM / 2º SGBM', cidade: 'Ouro Preto do Oeste', comando: 'COB I' },
  { unidade: '2º GBM / 3º SGBM', cidade: 'Jaru', comando: 'COB I' },
  { unidade: '5º GBM', cidade: 'Ariquemes', comando: 'COB I' },
  { unidade: '5º GBM / 1º SGBM', cidade: 'Ariquemes', comando: 'COB I' },
  { unidade: '5º GBM / 2º SGBM', cidade: "Machadinho D'Oeste", comando: 'COB I' },
  { unidade: '5º GBM / 3º SGBM', cidade: 'Buritis', comando: 'COB I' },
  { unidade: 'GBS', cidade: 'Porto Velho', comando: 'COB I' },

  // COB II — Coordenadoria Operacional de Bombeiros II
  { unidade: '3º GBM', cidade: 'Vilhena', comando: 'COB II' },
  { unidade: '3º GBM / 1º SGBM', cidade: 'Vilhena', comando: 'COB II' },
  { unidade: '3º GBM / 2º SGBM', cidade: 'Cerejeiras', comando: 'COB II' },
  { unidade: '3º GBM / 3º SGBM', cidade: 'Colorado do Oeste', comando: 'COB II' },
  { unidade: '4º GBM', cidade: 'Cacoal', comando: 'COB II' },
  { unidade: '4º GBM / 1º SGBM', cidade: 'Cacoal', comando: 'COB II' },
  { unidade: '4º GBM / 2º SGBM', cidade: 'Pimenta Bueno', comando: 'COB II' },
  { unidade: '4º GBM / 3º SGBM', cidade: "Espigão D'Oeste", comando: 'COB II' },
  { unidade: '6º GBM', cidade: 'Rolim de Moura', comando: 'COB II' },
  { unidade: '6º GBM / 1º SGBM', cidade: 'Rolim de Moura', comando: 'COB II' },
  { unidade: '6º GBM / 2º SGBM', cidade: 'São Miguel do Guaporé', comando: 'COB II' },

  // CAT — Coordenadoria de Atividades Técnicas
  { unidade: 'CAT', cidade: 'Porto Velho', comando: 'CAT' },
  { unidade: 'DAT - Porto Velho', cidade: 'Porto Velho', comando: 'CAT' },
  { unidade: 'DAT - Porto Velho / SAT - Porto Velho', cidade: 'Porto Velho', comando: 'CAT' },
  { unidade: 'DAT - Porto Velho / SAT - Candeias', cidade: 'Candeias do Jamari', comando: 'CAT' },
  { unidade: 'DAT - Porto Velho / SAT - Guajará-Mirim', cidade: 'Guajará-Mirim', comando: 'CAT' },
  { unidade: 'DAT - Ariquemes', cidade: 'Ariquemes', comando: 'CAT' },
  { unidade: 'DAT - Ariquemes / SAT - Ariquemes', cidade: 'Ariquemes', comando: 'CAT' },
  { unidade: 'DAT - Ariquemes / SAT - Machadinho', cidade: "Machadinho D'Oeste", comando: 'CAT' },
  { unidade: 'DAT - Ariquemes / SAT - Buritis', cidade: 'Buritis', comando: 'CAT' },
  { unidade: 'DAT - Ji-Paraná', cidade: 'Ji-Paraná', comando: 'CAT' },
  { unidade: 'DAT - Ji-Paraná / SAT - Ji-Paraná', cidade: 'Ji-Paraná', comando: 'CAT' },
  { unidade: 'DAT - Ji-Paraná / SAT - Ouro Preto', cidade: 'Ouro Preto do Oeste', comando: 'CAT' },
  { unidade: 'DAT - Ji-Paraná / SAT - Jaru', cidade: 'Jaru', comando: 'CAT' },
  { unidade: 'DAT - Cacoal', cidade: 'Cacoal', comando: 'CAT' },
  { unidade: 'DAT - Cacoal / SAT - Cacoal', cidade: 'Cacoal', comando: 'CAT' },
  { unidade: 'DAT - Cacoal / SAT - Pimenta Bueno', cidade: 'Pimenta Bueno', comando: 'CAT' },
  { unidade: 'DAT - Cacoal / SAT - Rolim', cidade: 'Rolim de Moura', comando: 'CAT' },
  { unidade: 'DAT - Cacoal / SAT - Espigão', cidade: "Espigão D'Oeste", comando: 'CAT' },
  { unidade: 'DAT - Cacoal / SAT - São Miguel', cidade: 'São Miguel do Guaporé', comando: 'CAT' },
  { unidade: 'DAT - Vilhena', cidade: 'Vilhena', comando: 'CAT' },
  { unidade: 'DAT - Vilhena / SAT - Vilhena', cidade: 'Vilhena', comando: 'CAT' },
  { unidade: 'DAT - Vilhena / SAT - Cerejeiras', cidade: 'Cerejeiras', comando: 'CAT' },
  { unidade: 'DAT - Vilhena / SAT - Colorado', cidade: 'Colorado do Oeste', comando: 'CAT' },

  // COA — Coordenadoria Operacional Administrativa
  { unidade: 'COA', cidade: 'Porto Velho', comando: 'COA' },
  { unidade: 'GOA', cidade: 'Porto Velho', comando: 'COA' },

  // CEEI — Centro de Ensino e Instrução
  { unidade: 'CEEI', cidade: 'Porto Velho', comando: 'CEEI' },
  { unidade: 'CEEI / CMDPII-2', cidade: 'Vilhena', comando: 'CEEI' },

  // Unidades administrativas (sede única, todas em Porto Velho)
  { unidade: 'Gabinete do Comando Geral', cidade: 'Porto Velho', comando: 'Comando Geral' },
  { unidade: 'Ajudância Geral', cidade: 'Porto Velho', comando: 'Comando Geral' },
  { unidade: 'CHEM', cidade: 'Porto Velho', comando: 'Comando Geral' },
  { unidade: 'CPOF', cidade: 'Porto Velho', comando: 'CPOF' },
  { unidade: 'DPLAN', cidade: 'Porto Velho', comando: 'DPLAN' },
  { unidade: 'DLOG', cidade: 'Porto Velho', comando: 'DLOG' },
  { unidade: 'DCS', cidade: 'Porto Velho', comando: 'DCS' },
  { unidade: 'DINF', cidade: 'Porto Velho', comando: 'DINF' },
  { unidade: 'Coordenadoria de Pessoal', cidade: 'Porto Velho', comando: 'Coordenadoria de Pessoal' },
  { unidade: 'Corregedoria', cidade: 'Porto Velho', comando: 'Corregedoria' },
  { unidade: 'Defesa Civil', cidade: 'Porto Velho', comando: 'Defesa Civil' },
  { unidade: 'Diretoria de Inteligência', cidade: 'Porto Velho', comando: 'Diretoria de Inteligência' },
]

function unicosOrdenados(valores) {
  return [...new Set(valores)].sort((a, b) => a.localeCompare(b, 'pt-BR'))
}

export function cidadesDisponiveis() {
  return unicosOrdenados(UNIDADES_CBMRO.map(u => u.cidade))
}

export function comandosPorCidade(cidade) {
  return unicosOrdenados(
    UNIDADES_CBMRO.filter(u => u.cidade === cidade).map(u => u.comando),
  )
}

export function unidadesPorCidadeEComando(cidade, comando) {
  return unicosOrdenados(
    UNIDADES_CBMRO.filter(u => u.cidade === cidade && u.comando === comando).map(u => u.unidade),
  )
}
```

- [ ] **Step 4: Run test to verify it passes**

Run: `npm test`
Expected: PASS (todos os testes de `unidadesCbmro.test.js`)

- [ ] **Step 5: Commit**

```bash
git add src/lib/unidadesCbmro.js src/lib/unidadesCbmro.test.js
git commit -m "feat(acesso): dados reais de cidade/comando/unidade do CBMRO (Sistema ATI)"
```

---

## Task 2: Status "pendente" em `membersStats.js`

**Files:**
- Modify: `src/lib/membersStats.js:9-12` (função `situacaoMembro`), `src/lib/membersStats.js:14-24` (função `contaStatus`)
- Test: `src/lib/membersStats.test.js`

**Interfaces:**
- Consumes: nada novo.
- Produces: `situacaoMembro(member)` agora pode retornar `'pendente'`; `contaStatus(members)`
  agora inclui a chave `pendentes` — usados pela Task 8 (`Acessos.jsx`).

- [ ] **Step 1: Write the failing tests**

Adicionar ao final de `src/lib/membersStats.test.js`:

```js
test('situacaoMembro: ativo=false com status pendente é "pendente", não "bloqueado"', () => {
  assert.equal(situacaoMembro({ ativo: false, status: 'pendente' }), 'pendente')
})

test('situacaoMembro: ativo=false com status recusado continua "bloqueado"', () => {
  assert.equal(situacaoMembro({ ativo: false, status: 'recusado' }), 'bloqueado')
})

test('contaStatus soma pendentes separado de bloqueados', () => {
  const members = [
    { ativo: false, status: 'pendente' },
    { ativo: false, status: 'pendente' },
    { ativo: false, status: 'recusado' },
    { ativo: true, status: 'cadastrado' },
  ]
  assert.deepEqual(contaStatus(members), { total: 4, cadastrados: 1, convidados: 0, bloqueados: 1, pendentes: 2 })
})
```

Também ajustar o teste já existente `contaStatus soma por situação` (linha 21-29), porque
`contaStatus` vai passar a devolver sempre a chave `pendentes` — o `assert.deepEqual`
compara o objeto inteiro:

```js
test('contaStatus soma por situação', () => {
  const members = [
    { ativo: true, status: 'cadastrado' },
    { ativo: true, status: 'cadastrado' },
    { ativo: true, status: 'convidado' },
    { ativo: false, status: 'cadastrado' },
  ]
  assert.deepEqual(contaStatus(members), { total: 4, cadastrados: 2, convidados: 1, bloqueados: 1, pendentes: 0 })
})
```

- [ ] **Step 2: Run test to verify it fails**

Run: `npm test`
Expected: FAIL — `situacaoMembro` ainda devolve `'bloqueado'` para `status: 'pendente'`, e
`contaStatus` ainda não tem a chave `pendentes`.

- [ ] **Step 3: Write the implementation**

Substituir em `src/lib/membersStats.js`:

```js
// Situação exibida: bloqueado vence tudo (ativo:false), exceto quando ainda está
// aguardando aprovação (status "pendente" — não é o admin bloqueando, é a pessoa que
// nunca teve o acesso liberado ainda); senão o próprio status.
export function situacaoMembro(member) {
  if (member.ativo === false) {
    return member.status === 'pendente' ? 'pendente' : 'bloqueado'
  }
  return member.status === 'cadastrado' ? 'cadastrado' : 'convidado'
}

export function contaStatus(members) {
  const c = { total: 0, cadastrados: 0, convidados: 0, bloqueados: 0, pendentes: 0 }
  for (const m of members) {
    c.total += 1
    const s = situacaoMembro(m)
    if (s === 'pendente') c.pendentes += 1
    else if (s === 'bloqueado') c.bloqueados += 1
    else if (s === 'cadastrado') c.cadastrados += 1
    else c.convidados += 1
  }
  return c
}
```

- [ ] **Step 4: Run test to verify it passes**

Run: `npm test`
Expected: PASS (todos os testes de `membersStats.test.js`)

- [ ] **Step 5: Commit**

```bash
git add src/lib/membersStats.js src/lib/membersStats.test.js
git commit -m "feat(acesso): distinguir situação 'pendente' de 'bloqueado' nas estatísticas"
```

---

## Task 3: Escrita no Firestore — `solicitarAcesso` e `recusarSolicitacao`

**Files:**
- Modify: `src/lib/membersData.js` (adicionar duas funções; nenhuma linha existente muda)

**Interfaces:**
- Consumes: `db` (`./firebase.js`), `normalizeEmail` (`./membersStats.js`) — já importados
  no topo do arquivo.
- Produces: `solicitarAcesso({ email, nome, nomeGuerra, cidade, comando, unidade, uid }): Promise<void>`
  e `recusarSolicitacao(email): Promise<void>` — usados pela Task 6 (`SolicitarAcesso.jsx`)
  e Task 8 (`Acessos.jsx`) respectivamente.

Sem teste automatizado dedicado (o arquivo `membersData.js` não tem testes hoje — é uma
casca fina sobre chamadas do Firestore; a verificação real acontece no teste manual
ponta a ponta da Task 9). Este passo é só implementação.

- [ ] **Step 1: Adicionar as duas funções ao final de `src/lib/membersData.js`**

```js
// Autocadastro público (tela /solicitar-acesso): grava sempre travado em
// ativo:false/status:'pendente'/role:'participante' — a regra do Firestore também trava
// isso do lado do servidor; aqui é só o formato que o admin vai aprovar depois.
export async function solicitarAcesso({ email, nome, nomeGuerra, cidade, comando, unidade, uid }) {
  const id = normalizeEmail(email)
  await setDoc(doc(db, COL, id), {
    email: id,
    nome: (nome ?? '').trim() || id,
    nomeGuerra: (nomeGuerra ?? '').trim(),
    cidade,
    comando,
    unidade,
    role: 'participante',
    ativo: false,
    status: 'pendente',
    uid,
    criadoEm: serverTimestamp(),
    criadoPor: null,
    ultimoLogin: null,
  })
}

export async function recusarSolicitacao(email) {
  await updateDoc(doc(db, COL, normalizeEmail(email)), { status: 'recusado' })
}
```

- [ ] **Step 2: Rodar a suíte para garantir que nada quebrou**

Run: `npm test`
Expected: PASS (mesmos testes de antes — este arquivo não tem teste próprio)

- [ ] **Step 3: Commit**

```bash
git add src/lib/membersData.js
git commit -m "feat(acesso): solicitarAcesso e recusarSolicitacao no Firestore"
```

---

## Task 4: `auth.jsx` — `cadastrar()` devolve o usuário + estado `pendente`

**Files:**
- Modify: `src/lib/auth.jsx`

**Interfaces:**
- Consumes: nada novo.
- Produces: `cadastrar(email, senha)` agora retorna o `User` do Firebase (antes não
  retornava nada); novo campo `pendente: boolean` no contexto (`useAuth()`) — usados pela
  Task 6 (`SolicitarAcesso.jsx`) e Task 7 (`Login.jsx`).

Sem teste automatizado dedicado (arquivo depende do SDK do Firebase; não há
`auth.test.jsx` hoje). Verificação real na Task 9.

- [ ] **Step 1: Adicionar o estado `pendente`**

Em `src/lib/auth.jsx:16`, logo abaixo de `naoAutorizado`:

```js
  const [naoAutorizado, setNaoAutorizado] = useState(false)
  const [pendente, setPendente] = useState(false)
```

- [ ] **Step 2: Resetar `pendente` em todos os pontos de saída do `onAuthStateChanged`**

Em `src/lib/auth.jsx:21-23` (ninguém logado):

```js
      if (!fbUser) {
        setUser(null); setNaoAutorizado(false); setPendente(false); setLoading(false)
        return
      }
```

Em `src/lib/auth.jsx:30-34` (doc não existe ou está inativo) — aqui é onde detectamos o
"pendente":

```js
        if (!snap.exists() || snap.data().ativo !== true) {
          setUser(null)
          setNaoAutorizado(true)
          setPendente(snap.exists() && snap.data().status === 'pendente')
          await signOut(auth)
          return
        }
```

Em `src/lib/auth.jsx:56` (sucesso), logo após `setNaoAutorizado(false)`:

```js
        setNaoAutorizado(false)
        setPendente(false)
        setErroVerificacao(null)
```

Em `src/lib/auth.jsx:63` (falha de verificação/rede), logo após `setUser(null); setNaoAutorizado(false)`:

```js
        setUser(null); setNaoAutorizado(false); setPendente(false)
```

- [ ] **Step 3: `cadastrar()` devolve o usuário criado**

Em `src/lib/auth.jsx:75-77`, substituir:

```js
  const cadastrar = async (email, senha) => {
    const cred = await createUserWithEmailAndPassword(auth, normalizeEmail(email), senha)
    return cred.user
  }
```

- [ ] **Step 4: Expor `pendente` no contexto**

Em `src/lib/auth.jsx:87`, adicionar `pendente` ao value do provider:

```js
    <AuthContext.Provider value={{ user, loading, naoAutorizado, pendente, erroVerificacao, entrar, cadastrar, sair, recuperarSenha }}>
```

- [ ] **Step 5: Rodar a suíte para garantir que nada quebrou**

Run: `npm test`
Expected: PASS

- [ ] **Step 6: Commit**

```bash
git add src/lib/auth.jsx
git commit -m "feat(acesso): cadastrar() devolve o usuário; contexto expõe status 'pendente'"
```

---

## Task 5: Regra do Firestore — autocadastro restrito

**Files:**
- Modify: `firestore.rules:29-37`

**Interfaces:** nenhuma (arquivo de configuração, não código consumido por outros arquivos).

- [ ] **Step 1: Substituir o bloco `match /members/{email}`**

Trocar:

```
    match /members/{email} {
      allow read: if isAdmin()
        || (request.auth != null && request.auth.token.email == email);
      allow create, delete: if isAdmin();
      // O próprio dono só pode mexer em uid/status/ultimoLogin (registro de login).
      allow update: if isAdmin()
        || (request.auth != null && request.auth.token.email == email
            && request.resource.data.diff(resource.data).affectedKeys().hasOnly(['uid','status','ultimoLogin']));
    }
```

por:

```
    match /members/{email} {
      allow read: if isAdmin()
        || (request.auth != null && request.auth.token.email == email);
      // Admin cria por convite OU a própria pessoa cria o PRÓPRIO pedido — sempre travado
      // em pendente/sem privilégio; só o admin (via update) libera (ativo:true).
      allow create: if isAdmin()
        || (request.auth != null && request.auth.token.email == email
            && request.resource.data.uid == request.auth.uid
            && request.resource.data.email == email
            && request.resource.data.ativo == false
            && request.resource.data.status == 'pendente'
            && request.resource.data.role == 'participante'
            && request.resource.data.nome is string && request.resource.data.nome.size() > 0 && request.resource.data.nome.size() <= 200
            && request.resource.data.nomeGuerra is string && request.resource.data.nomeGuerra.size() <= 100
            && request.resource.data.cidade is string && request.resource.data.cidade.size() <= 100
            && request.resource.data.comando is string && request.resource.data.comando.size() <= 100
            && request.resource.data.unidade is string && request.resource.data.unidade.size() <= 200
            && request.resource.data.keys().hasOnly(
                 ['email','nome','nomeGuerra','cidade','comando','unidade',
                  'role','ativo','status','uid','criadoEm','criadoPor','ultimoLogin']));
      allow delete: if isAdmin();
      // O próprio dono pode mexer em uid/status/ultimoLogin (registro de login) — inclui a
      // transição pendente→cadastrado quando a solicitação já foi aprovada.
      allow update: if isAdmin()
        || (request.auth != null && request.auth.token.email == email
            && request.resource.data.diff(resource.data).affectedKeys().hasOnly(['uid','status','ultimoLogin']));
    }
```

- [ ] **Step 2: Commit**

```bash
git add firestore.rules
git commit -m "feat(acesso): regra do Firestore permite autocadastro restrito a pendente"
```

- [ ] **Step 3: Publicar a regra (fora do git)**

Este arquivo **não é publicado automaticamente** — precisa colar no console do Firebase
(projeto `revisao-minuta-cbmro-6f248`, aba Firestore → Regras) e clicar em Publicar, ou
usar a skill `deploy-firebase`. **Isso é manual, avisar o Wândrio antes de fazer** (regra 4
do crachá: publicar regra em produção não é uma ação reversível trivial). Sem essa
publicação, a Task 9 (teste ponta a ponta) não vai passar — o `solicitarAcesso()` vai
falhar com `permission-denied`.

---

## Task 6: Tela pública `/solicitar-acesso`

**Files:**
- Create: `src/pages/SolicitarAcesso.jsx`
- Modify: `src/index.css` (uma única regra nova, aditiva)

**Interfaces:**
- Consumes: `useAuth()` → `{ cadastrar, pendente }` (Task 4); `solicitarAcesso` (Task 3,
  `../lib/membersData.js`); `cidadesDisponiveis`, `comandosPorCidade`,
  `unidadesPorCidadeEComando` (Task 1, `../lib/unidadesCbmro.js`).
- Produces: componente `SolicitarAcesso` (default export) — usado pela Task 7 (`App.jsx`).

Tela não tem teste automatizado próprio (é UI de formulário; o projeto não usa
testing-library — os testes existentes são todos de funções puras). Verificação visual e
funcional na Task 9.

- [ ] **Step 1: Adicionar a classe CSS nova**

Em `src/index.css`, logo após a linha 2318 (`.login-card { ... }`):

```css
.login-card--wide { max-width: 420px; }
```

- [ ] **Step 2: Criar o componente**

```jsx
// src/pages/SolicitarAcesso.jsx
import { useMemo, useState, useEffect } from 'react'
import { Link } from 'react-router-dom'
import { useAuth } from '../lib/auth.jsx'
import { solicitarAcesso } from '../lib/membersData.js'
import { cidadesDisponiveis, comandosPorCidade, unidadesPorCidadeEComando } from '../lib/unidadesCbmro.js'

const MENSAGENS = {
  'auth/email-already-in-use': 'Este e-mail já tem cadastro. Use a tela de login.',
  'auth/invalid-email': 'E-mail inválido.',
  'auth/weak-password': 'A senha precisa ter ao menos 6 caracteres.',
}

export default function SolicitarAcesso() {
  const { cadastrar, pendente } = useAuth()
  const [nomeCompleto, setNomeCompleto] = useState('')
  const [nomeGuerra, setNomeGuerra] = useState('')
  const [cidade, setCidade] = useState('')
  const [comando, setComando] = useState('')
  const [unidade, setUnidade] = useState('')
  const [email, setEmail] = useState('')
  const [senha, setSenha] = useState('')
  const [confirma, setConfirma] = useState('')
  const [erro, setErro] = useState('')
  const [enviando, setEnviando] = useState(false)

  const cidades = useMemo(() => cidadesDisponiveis(), [])
  const comandos = useMemo(() => (cidade ? comandosPorCidade(cidade) : []), [cidade])
  const unidades = useMemo(
    () => (cidade && comando ? unidadesPorCidadeEComando(cidade, comando) : []),
    [cidade, comando],
  )

  // Pedido gravado: o AuthProvider detecta ativo:false/status:'pendente' e desloga
  // sozinho — este efeito só tira o "Enviando…"; a confirmação é o `if (pendente)` abaixo.
  useEffect(() => { if (pendente) setEnviando(false) }, [pendente])

  const mudarCidade = (novaCidade) => {
    setCidade(novaCidade); setComando(''); setUnidade('')
  }
  const mudarComando = (novoComando) => {
    setComando(novoComando); setUnidade('')
  }

  const submeter = async (e) => {
    e.preventDefault()
    setErro('')
    if (!nomeCompleto.trim() || !nomeGuerra.trim()) { setErro('Preencha nome completo e nome de guerra.'); return }
    if (!cidade || !comando || !unidade) { setErro('Escolha cidade, comando e unidade.'); return }
    if (senha.length < 6) { setErro('A senha precisa ter ao menos 6 caracteres.'); return }
    if (senha !== confirma) { setErro('As senhas não conferem.'); return }
    setEnviando(true)
    try {
      const fbUser = await cadastrar(email, senha)
      await solicitarAcesso({ email, nome: nomeCompleto, nomeGuerra, cidade, comando, unidade, uid: fbUser.uid })
    } catch (err) {
      setErro(MENSAGENS[err.code] ?? 'Não foi possível enviar o pedido. Tente novamente.')
      setEnviando(false)
    }
  }

  if (pendente) {
    return (
      <div className="login-wrap">
        <div className="login-card login-card--wide">
          <h2 className="login-title">Pedido enviado</h2>
          <p className="login-sub">Seu pedido de acesso foi enviado para análise. Você será avisado quando for aprovado.</p>
          <Link className="login-link" to="/login">Voltar para o login</Link>
        </div>
      </div>
    )
  }

  return (
    <div className="login-wrap">
      <form className="login-card login-card--wide" onSubmit={submeter}>
        <h2 className="login-title">Solicitar acesso</h2>
        <p className="login-sub">Preencha seus dados para pedir acesso à Revisão da Minuta</p>

        {erro && <div className="form-error">{erro}</div>}

        <label className="login-label">Nome completo
          <input className="login-input" value={nomeCompleto}
            onChange={e => setNomeCompleto(e.target.value)} required />
        </label>
        <label className="login-label">Nome de guerra
          <input className="login-input" value={nomeGuerra}
            onChange={e => setNomeGuerra(e.target.value)} required />
        </label>
        <label className="login-label">Cidade
          <select className="login-input" value={cidade}
            onChange={e => mudarCidade(e.target.value)} required>
            <option value="">Selecione...</option>
            {cidades.map(c => <option key={c} value={c}>{c}</option>)}
          </select>
        </label>
        <label className="login-label">Comando
          <select className="login-input" value={comando}
            onChange={e => mudarComando(e.target.value)} required disabled={!cidade}>
            <option value="">{cidade ? 'Selecione...' : 'Escolha a cidade primeiro'}</option>
            {comandos.map(c => <option key={c} value={c}>{c}</option>)}
          </select>
        </label>
        <label className="login-label">Unidade
          <select className="login-input" value={unidade}
            onChange={e => setUnidade(e.target.value)} required disabled={!comando}>
            <option value="">{comando ? 'Selecione...' : 'Escolha o comando primeiro'}</option>
            {unidades.map(u => <option key={u} value={u}>{u}</option>)}
          </select>
        </label>
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
          {enviando ? 'Enviando…' : 'Enviar pedido de acesso'}
        </button>
        <Link className="login-link" to="/login">Já tenho acesso — entrar</Link>
      </form>
    </div>
  )
}
```

- [ ] **Step 3: Rodar a suíte para garantir que nada quebrou**

Run: `npm test`
Expected: PASS

- [ ] **Step 4: Commit**

```bash
git add src/pages/SolicitarAcesso.jsx src/index.css
git commit -m "feat(acesso): tela pública /solicitar-acesso com cascata cidade/comando/unidade"
```

---

## Task 7: Rotas e link no login

**Files:**
- Modify: `src/App.jsx:30` (import), `src/App.jsx:301` (rota deslogada), `src/App.jsx:374` (rota logada)
- Modify: `src/pages/Login.jsx`

**Interfaces:**
- Consumes: `SolicitarAcesso` (Task 6, default export de `./pages/SolicitarAcesso.jsx`);
  `pendente` do `useAuth()` (Task 4).

- [ ] **Step 1: Importar o componente em `App.jsx`**

Em `src/App.jsx:30`, logo após `import Cadastro from './pages/Cadastro.jsx'`:

```js
import SolicitarAcesso from './pages/SolicitarAcesso.jsx'
```

- [ ] **Step 2: Rota pública (deslogado)**

Em `src/App.jsx:301`, dentro de `LoggedOutRoutes`, logo após a rota `/cadastro`:

```jsx
      <Route path="/cadastro" element={<Cadastro />} />
      <Route path="/solicitar-acesso" element={<SolicitarAcesso />} />
```

- [ ] **Step 3: Rota redirecionada (já logado)**

Em `src/App.jsx:374`, logo após a rota `/cadastro` da árvore autenticada:

```jsx
          <Route path="/cadastro" element={<AlreadyLoggedInRedirect />} />
          <Route path="/solicitar-acesso" element={<AlreadyLoggedInRedirect />} />
```

- [ ] **Step 4: Link e aviso de "pendente" em `Login.jsx`**

Em `src/pages/Login.jsx:13`, incluir `pendente` na desestruturação:

```js
  const { entrar, recuperarSenha, naoAutorizado, erroVerificacao, pendente } = useAuth()
```

Em `src/pages/Login.jsx:57-59`, substituir o bloco do aviso de não-autorizado:

```jsx
        {pendente && (
          <div className="login-aviso">Seu pedido de acesso está em análise. Você será avisado quando for aprovado.</div>
        )}
        {!pendente && naoAutorizado && (
          <div className="form-error">Seu acesso ainda não foi liberado pelo administrador.</div>
        )}
```

Em `src/pages/Login.jsx:77-80`, adicionar um segundo bloco de rodapé, logo depois do
existente ("Primeiro acesso? Criar minha senha"):

```jsx
        <div className="login-foot">
          <span className="login-foot-txt">Primeiro acesso?</span>
          <Link className="login-link" to="/cadastro">Criar minha senha</Link>
        </div>
        <div className="login-foot">
          <span className="login-foot-txt">Ainda não tem acesso?</span>
          <Link className="login-link" to="/solicitar-acesso">Solicitar acesso</Link>
        </div>
```

- [ ] **Step 5: Rodar a suíte para garantir que nada quebrou**

Run: `npm test`
Expected: PASS

- [ ] **Step 6: Commit**

```bash
git add src/App.jsx src/pages/Login.jsx
git commit -m "feat(acesso): rotas de /solicitar-acesso e link na tela de login"
```

---

## Task 8: Seção "Solicitações pendentes" em `Acessos.jsx`

**Files:**
- Modify: `src/pages/Acessos.jsx`
- Modify: `src/index.css` (uma regra nova, aditiva)

**Interfaces:**
- Consumes: `situacaoMembro` (já importado, Task 2 muda seu comportamento);
  `recusarSolicitacao` (Task 3, `../lib/membersData.js`); `setMemberAtivo` (já existe, usado
  como "aprovar").

- [ ] **Step 1: Badge de "pendente" no CSS**

Em `src/index.css`, logo após a linha 2499 (`.acc-badge.b-bloq { ... }`):

```css
.acc-badge.b-pend { background: #fff0e0; color: #b45500; }
```

- [ ] **Step 2: Importar `recusarSolicitacao` em `Acessos.jsx`**

Em `src/pages/Acessos.jsx:4-6`, adicionar à lista de imports de `membersData.js`:

```js
import {
  subscribeMembers, addMember, setMemberRole, setMemberAtivo, removeMember, recusarSolicitacao,
} from '../lib/membersData.js'
```

- [ ] **Step 3: Badge "pendente" no mapa `BADGE`**

Em `src/pages/Acessos.jsx:15-19`, adicionar a entrada nova:

```js
const BADGE = {
  cadastrado: { cls: 'b-cad', txt: '🟢 Cadastrado' },
  convidado: { cls: 'b-conv', txt: '🟡 Convidado' },
  pendente: { cls: 'b-pend', txt: '🟠 Pendente' },
  bloqueado: { cls: 'b-bloq', txt: '🔴 Bloqueado' },
}
```

- [ ] **Step 4: Derivar a lista de pendentes e os handlers de aprovar/recusar**

Em `src/pages/Acessos.jsx:35`, logo após `const stats = useMemo(...)`:

```js
  const pendentes = useMemo(() => members.filter(m => situacaoMembro(m) === 'pendente'), [members])
```

Em `src/pages/Acessos.jsx:61` (logo após a função `remover`), adicionar:

```js
  const aprovar = async (m) => {
    try { await setMemberAtivo(m.email, true) }
    catch (err) { console.error(err); setErro('Não foi possível aprovar o pedido.') }
  }
  const recusar = async (m) => {
    if (!window.confirm(`Recusar o pedido de ${m.nome}?`)) return
    try { await recusarSolicitacao(m.email) }
    catch (err) { console.error(err); setErro('Não foi possível recusar o pedido.') }
  }
```

- [ ] **Step 5: Cartão de estatística "Pedidos pendentes"**

Em `src/pages/Acessos.jsx:75-80`, dentro de `.acc-cards`, adicionar um cartão antes do de
"Bloqueadas":

```jsx
        <div className="acc-stat"><div className="acc-n"><span className="acc-dot" style={{ background: '#b45500' }} />{stats.pendentes}</div><div className="acc-l">Pedidos pendentes</div></div>
        <div className="acc-stat"><div className="acc-n"><span className="acc-dot" style={{ background: 'var(--cbm-red-700)' }} />{stats.bloqueados}</div><div className="acc-l">Bloqueadas</div></div>
```

- [ ] **Step 6: Seção de solicitações pendentes**

Em `src/pages/Acessos.jsx:81` (logo antes de `.acc-bar`), adicionar:

```jsx
      {pendentes.length > 0 && (
        <>
          <div className="acc-bar">
            <strong>Solicitações pendentes</strong>
          </div>
          <div className="acc-panel" style={{ marginBottom: 18 }}>
            <table className="acc-table">
              <thead>
                <tr><th>Pessoa</th><th>Cidade / Comando / Unidade</th><th style={{ textAlign: 'right' }}>Ações</th></tr>
              </thead>
              <tbody>
                {pendentes.map(m => (
                  <tr key={m.email}>
                    <td>
                      <div className="acc-nome">{m.nome}{m.nomeGuerra ? ` (${m.nomeGuerra})` : ''}</div>
                      <div className="acc-mail">{m.email}</div>
                    </td>
                    <td>{m.cidade} — {m.comando} — {m.unidade}</td>
                    <td>
                      <div className="acc-acts">
                        <button type="button" className="acc-ic" onClick={() => aprovar(m)}>aprovar</button>
                        <button type="button" className="acc-ic danger" onClick={() => recusar(m)}>recusar</button>
                      </div>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </>
      )}
```

- [ ] **Step 7: Rodar a suíte para garantir que nada quebrou**

Run: `npm test`
Expected: PASS

- [ ] **Step 8: Commit**

```bash
git add src/pages/Acessos.jsx src/index.css
git commit -m "feat(acesso): seção 'Solicitações pendentes' com aprovar/recusar em Acessos.jsx"
```

---

## Task 9: Teste ponta a ponta e limpeza

**Files:** nenhum (validação manual/Playwright do fluxo já implementado)

**Pré-requisito:** Task 5 (regra do Firestore) precisa estar **publicada** no console antes
deste teste — sem isso, `solicitarAcesso()` falha com `permission-denied`.

- [ ] **Step 1: Rodar o app localmente**

Run: `npm run dev`

- [ ] **Step 2: Fluxo de solicitação (Playwright ou manual)**

1. Abrir `/login`, clicar em "Solicitar acesso".
2. Preencher: Nome completo = "Teste Solicitação", Nome de guerra = "TesteSol", Cidade =
   "Buritis" (confere que só aparecem 2 comandos: CAT e COB I), Comando = "CAT" (confere
   que só aparece 1 unidade: "DAT - Ariquemes / SAT - Buritis"), E-mail =
   `teste.solicitacao.lob@gmail.com`, Senha = `teste123`, Confirmar = `teste123`.
3. Enviar. Esperado: tela "Pedido enviado".
4. Conferir no console do Firebase (Firestore → `members` → o doc do e-mail de teste):
   `ativo: false`, `status: 'pendente'`, `cidade: 'Buritis'`, `comando: 'CAT'`,
   `unidade: 'DAT - Ariquemes / SAT - Buritis'`, `nomeGuerra: 'TesteSol'`.

- [ ] **Step 3: Fluxo de aprovação**

1. Logar como admin, ir em `/acessos`.
2. Conferir que a seção "Solicitações pendentes" mostra o pedido de teste com cidade,
   comando e unidade corretos, e que o cartão "Pedidos pendentes" mostra 1.
3. Clicar em "aprovar".
4. Conferir no Firestore que o doc virou `ativo: true`.
5. Deslogar, ir em `/login`, entrar com `teste.solicitacao.lob@gmail.com` / `teste123`.
   Esperado: login bem-sucedido, badge do membro em `/acessos` agora "🟢 Cadastrado".

- [ ] **Step 4: Fluxo de recusa (segundo pedido de teste)**

1. Repetir o Step 2 com um segundo e-mail de teste (`teste.solicitacao2.lob@gmail.com`).
2. Em `/acessos`, clicar em "recusar".
3. Conferir no Firestore: `status: 'recusado'`, `ativo` continua `false`.
4. Tentar logar com esse e-mail: esperado, tela genérica "Seu acesso ainda não foi
   liberado pelo administrador." (não a mensagem de "pedido em análise", já que o status
   não é mais `'pendente'`).

- [ ] **Step 5: Confirmar que o convite manual antigo não regrediu**

Em `/acessos`, usar o formulário "＋ Convidar pessoa" já existente para convidar um
terceiro e-mail de teste; conferir que ele aparece como "🟡 Convidado" e que `/cadastro`
(não `/solicitar-acesso`) continua funcionando para essa pessoa definir a senha.

- [ ] **Step 6: Limpar os dados de teste**

No console do Firebase: apagar os documentos `members/teste.solicitacao.lob@gmail.com`,
`members/teste.solicitacao2.lob@gmail.com` e o terceiro e-mail de convite manual. As
contas correspondentes no Firebase **Auth** não são apagadas automaticamente (mesma
ressalva já registrada para `teste.claude.lob@gmail.com`) — apagar manualmente no console
se quiser estado 100% limpo.

- [ ] **Step 7: Commit final (se sobrou algum ajuste do teste manual)**

```bash
git add -A
git commit -m "test(acesso): valida fluxo ponta a ponta de solicitação/aprovação/recusa"
```

Se nada precisou de ajuste, este commit não existe — os commits das Tasks 1-8 já são o
resultado final.
