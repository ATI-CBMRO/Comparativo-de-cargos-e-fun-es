# Upload de documentos pelo visitante público — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Permitir que militares de outros CBMs, já identificados como visitantes públicos, enviem PDFs de legislação ainda ausentes do acervo, e dar ao administrador uma caixa de entrada para baixar e remover esses envios.

**Architecture:** O arquivo vai para o **Firebase Storage** (`uploads-visitantes/{uid}/…`) e os metadados para uma coleção nova do Firestore (`uploadsVisitantes`). Nada do pipeline de ingestão muda: o app só recebe e guarda; a curadoria de cada arquivo continua manual, fora do app. A identidade usada é a sessão anônima que o visitante já tem — nenhum login novo, nenhum provider novo.

**Tech Stack:** React 18 + Vite, react-router-dom v6, Firebase Auth (anônimo) + Firestore + **Storage** (primeiro uso no projeto), `node --test` para lógica pura, CSS único em `src/index.css`.

**Spec:** `docs/superpowers/specs/2026-08-18-acervo-publico-upload-documentos-design.md` — leia antes de começar.

---

## ⚠️ Pré-requisito operacional que BLOQUEIA a verificação ponta a ponta

**O bucket do Storage NÃO existe neste projeto ainda.** Verificado em 2026-08-19:

```
GET https://firebasestorage.googleapis.com/v0/b/revisao-minuta-cbmro-6f248.firebasestorage.app/o  → 404
GET https://firebasestorage.googleapis.com/v0/b/revisao-minuta-cbmro-6f248.appspot.com/o          → 404
```

Alguém com acesso ao console precisa **provisionar o Cloud Storage** no projeto
`revisao-minuta-cbmro-6f248` (Console → Build → Storage → "Começar"). Desde outubro de 2024
o Firebase exige o **plano Blaze** (pago por uso, com cota gratuita) para criar o bucket
padrão — se o projeto estiver no plano Spark, isso é uma decisão de contratação que precisa
ser tomada antes.

**Impacto no trabalho deste plano:** o código pode ser escrito, revisado e mesclado sem o
bucket — todos os testes desta entrega são de lógica pura e não tocam a rede. O que **não**
pode acontecer sem o bucket é o teste real de enviar um arquivo. Nenhuma tarefa deve ser
declarada "verificada em produção" enquanto o bucket não existir. Se o bucket não puder ser
criado, pare e reporte: a arquitetura inteira desta entrega depende dele.

---

## Global Constraints

- **Idioma:** todo texto de interface, comentário de código e mensagem de commit em **português do Brasil**.
- **Dev server:** porta fixa **5173** (`npm run dev`).
- **Testes:** `node --test` na raiz roda a suíte inteira (190 testes hoje, todos passando). Arquivos de teste ao lado do módulo, sufixo `.test.js` (padrão: `src/lib/visitante.test.js`).
- **Ramo de trabalho:** `feat/acervo-publico-upload-documentos` (já criado, já contém o commit da spec).
- **Não tocar:** `src/lib/escopoServico.js`, `src/components/ProtectedRoute.jsx`, `GuardaDeEscopo`/`NAV_ESCOPO` em `src/App.jsx`, e **nenhum bloco existente** do `firestore.rules`. Esta entrega só acrescenta.
- **Erro nunca fica só no console:** todo `catch`/`onError` precisa mudar algum pixel na tela (armadilha **AR-04**, `docs/superpowers/auditoria-armadilhas.md`).
- **Não há navegador no ambiente do agente.** Nenhuma tarefa pode ser declarada "verificada visualmente".
- **Nome da coleção do Firestore:** `uploadsVisitantes` (exato).
- **Prefixo do caminho no Storage:** `uploads-visitantes/{uid}/` (exato — a regra do Storage autoriza por esse prefixo).
- **Limite de arquivo:** somente `application/pdf`, **até 20 MB** (`20 * 1024 * 1024` bytes, comparação `<=` nos DOIS lados — cliente e regra).
- **Tipos de documento** (strings exatas, iguais aos rótulos que o visitante já vê na tabela de cobertura do Acervo): `Lei de Organização Básica`, `Regimento Interno`, `Regulamento de Serviço`, `Outro`.

---

### Task 1: Lógica pura do envio (`src/lib/uploadDocumento.js`)

Validação do formulário e geração do caminho no Storage. Sem React, sem Firebase — é o núcleo testável, no mesmo espírito de `src/lib/visitante.js` (entrega anterior).

**Files:**
- Create: `src/lib/uploadDocumento.js`
- Test: `src/lib/uploadDocumento.test.js`

**Interfaces:**
- Consumes: nada de tarefas anteriores.
- Produces:
  - `TIPOS_DOCUMENTO: string[]` — os 4 rótulos exatos
  - `LIMITE_TAMANHO_BYTES: number` = `20 * 1024 * 1024`
  - `LIMITES_UPLOAD: { estado: 120, observacao: 1000, nomeArquivo: 260 }`
  - `validarEnvio({ estado, tipoDocumento, observacao, arquivo }) -> { ok: true, dados: { estado, tipoDocumento, observacao } } | { ok: false, erro: string }`
  - `nomeArquivoSeguro(nome) -> string`
  - `caminhoUpload(uid, nomeArquivo, agoraMs) -> string`

- [ ] **Step 1: Escreva o teste que falha**

Crie `src/lib/uploadDocumento.test.js`:

```js
import test from 'node:test'
import assert from 'node:assert/strict'
import {
  TIPOS_DOCUMENTO, LIMITE_TAMANHO_BYTES, LIMITES_UPLOAD,
  validarEnvio, nomeArquivoSeguro, caminhoUpload,
} from './uploadDocumento.js'

// Dublê de File: o validador só olha name/size/type, então um objeto simples basta —
// `node --test` não tem a File API do navegador.
const pdf = (over = {}) => ({ name: 'lob.pdf', size: 1024, type: 'application/pdf', ...over })

// --- constantes ------------------------------------------------------------

test('TIPOS_DOCUMENTO traz os 4 rótulos exatos que o visitante já vê no Acervo', () => {
  assert.deepEqual(TIPOS_DOCUMENTO, [
    'Lei de Organização Básica', 'Regimento Interno', 'Regulamento de Serviço', 'Outro',
  ])
})

test('LIMITE_TAMANHO_BYTES é 20 MB', () => {
  assert.equal(LIMITE_TAMANHO_BYTES, 20 * 1024 * 1024)
})

// --- validação -------------------------------------------------------------

test('validarEnvio apara espaços de estado e observação', () => {
  const r = validarEnvio({
    estado: '  CBMPA  ', tipoDocumento: 'Regimento Interno',
    observacao: '  veio do site oficial  ', arquivo: pdf(),
  })
  assert.equal(r.ok, true)
  assert.deepEqual(r.dados, {
    estado: 'CBMPA', tipoDocumento: 'Regimento Interno', observacao: 'veio do site oficial',
  })
})

test('validarEnvio aceita observação vazia (campo opcional)', () => {
  const r = validarEnvio({ estado: 'CBMPA', tipoDocumento: 'Outro', arquivo: pdf() })
  assert.equal(r.ok, true)
  assert.equal(r.dados.observacao, '')
})

test('validarEnvio exige estado', () => {
  const r = validarEnvio({ estado: '   ', tipoDocumento: 'Outro', arquivo: pdf() })
  assert.equal(r.ok, false)
  assert.match(r.erro, /estado/i)
})

test('validarEnvio exige um tipo da lista — nada inventado', () => {
  assert.equal(validarEnvio({ estado: 'CBMPA', tipoDocumento: '', arquivo: pdf() }).ok, false)
  const r = validarEnvio({ estado: 'CBMPA', tipoDocumento: 'Portaria qualquer', arquivo: pdf() })
  assert.equal(r.ok, false)
  assert.match(r.erro, /tipo/i)
})

test('validarEnvio exige arquivo', () => {
  const r = validarEnvio({ estado: 'CBMPA', tipoDocumento: 'Outro', arquivo: null })
  assert.equal(r.ok, false)
  assert.match(r.erro, /arquivo|PDF/i)
})

test('validarEnvio recusa arquivo que não é PDF', () => {
  const r = validarEnvio({
    estado: 'CBMPA', tipoDocumento: 'Outro',
    arquivo: pdf({ name: 'foto.jpg', type: 'image/jpeg' }),
  })
  assert.equal(r.ok, false)
  assert.match(r.erro, /PDF/i)
})

test('validarEnvio recusa arquivo acima de 20 MB e aceita exatamente no limite', () => {
  const acima = validarEnvio({
    estado: 'CBMPA', tipoDocumento: 'Outro', arquivo: pdf({ size: LIMITE_TAMANHO_BYTES + 1 }),
  })
  assert.equal(acima.ok, false)
  assert.match(acima.erro, /20 MB/)

  // O limite é <= nos DOIS lados (cliente e regra do Storage): exatamente 20 MB passa.
  const noLimite = validarEnvio({
    estado: 'CBMPA', tipoDocumento: 'Outro', arquivo: pdf({ size: LIMITE_TAMANHO_BYTES }),
  })
  assert.equal(noLimite.ok, true)
})

test('validarEnvio recusa estado e observação acima do limite da regra do Firestore', () => {
  const estadoGigante = 'x'.repeat(LIMITES_UPLOAD.estado + 1)
  assert.equal(validarEnvio({ estado: estadoGigante, tipoDocumento: 'Outro', arquivo: pdf() }).ok, false)

  const obsGigante = 'y'.repeat(LIMITES_UPLOAD.observacao + 1)
  assert.equal(
    validarEnvio({ estado: 'CBMPA', tipoDocumento: 'Outro', observacao: obsGigante, arquivo: pdf() }).ok,
    false,
  )
})

// --- nome de arquivo e caminho --------------------------------------------

// SEGURANÇA: uma barra no nome do arquivo criaria uma subpasta e poderia escapar da pasta
// do próprio uid, que é exatamente o que a regra do Storage usa para autorizar a escrita.
test('nomeArquivoSeguro remove barras, "..", e caracteres de caminho', () => {
  assert.equal(nomeArquivoSeguro('../../etc/senha.pdf'), 'etc-senha.pdf')
  assert.equal(nomeArquivoSeguro('pasta/sub/lei.pdf'), 'pasta-sub-lei.pdf')
  assert.equal(nomeArquivoSeguro('lei\\windows.pdf'), 'lei-windows.pdf')
})

test('nomeArquivoSeguro troca espaços e acentos por equivalentes simples', () => {
  assert.equal(nomeArquivoSeguro('Lei de Organização Básica.pdf'), 'Lei-de-Organizacao-Basica.pdf')
})

test('nomeArquivoSeguro trunca nome muito longo preservando a extensão .pdf', () => {
  const longo = `${'a'.repeat(400)}.pdf`
  const saida = nomeArquivoSeguro(longo)
  assert.ok(saida.length <= LIMITES_UPLOAD.nomeArquivo)
  assert.ok(saida.endsWith('.pdf'))
})

test('nomeArquivoSeguro nunca devolve string vazia', () => {
  assert.ok(nomeArquivoSeguro('').length > 0)
  assert.ok(nomeArquivoSeguro('///').length > 0)
})

test('caminhoUpload põe o arquivo dentro da pasta do próprio uid, com carimbo de tempo', () => {
  const caminho = caminhoUpload('uid123', 'lei.pdf', 1700000000000)
  assert.equal(caminho, 'uploads-visitantes/uid123/1700000000000-lei.pdf')
})

test('caminhoUpload sanitiza o nome antes de montar o caminho', () => {
  const caminho = caminhoUpload('uid123', '../fuga.pdf', 1700000000000)
  assert.equal(caminho, 'uploads-visitantes/uid123/1700000000000-fuga.pdf')
  // Nenhum ".." sobrevive: o arquivo não escapa da pasta do uid.
  assert.ok(!caminho.includes('..'))
})
```

- [ ] **Step 2: Rode o teste e confirme que falha**

```bash
node --test src/lib/uploadDocumento.test.js
```
Esperado: FALHA com `ERR_MODULE_NOT_FOUND` para `./uploadDocumento.js`.

- [ ] **Step 3: Implemente o mínimo**

Crie `src/lib/uploadDocumento.js`:

```js
// Lógica pura do envio de documentos pelo visitante público (spec 2026-08-18):
// validação do formulário e montagem do caminho no Storage. Sem React e sem Firebase —
// é o núcleo que dá para testar com `node --test`, no mesmo espírito de visitante.js.

// Os mesmos rótulos que o visitante já lê na tabela de cobertura do Acervo Legal. Manter
// o vocabulário igual evita que ele tenha que traduzir o que está vendo para o que o
// formulário pede.
export const TIPOS_DOCUMENTO = [
  'Lei de Organização Básica', 'Regimento Interno', 'Regulamento de Serviço', 'Outro',
]

// 20 MB. A comparação é `<=` aqui E na regra do Storage — se um lado usar `<` e o outro
// `<=`, um arquivo de exatamente 20 MB passa no formulário e é recusado pelo servidor,
// depois do upload inteiro já ter subido.
export const LIMITE_TAMANHO_BYTES = 20 * 1024 * 1024

// Espelham os tamanhos da regra do Firestore (firestore.rules, match /uploadsVisitantes).
// Se um deles mudar lá, mude aqui — senão o banco recusa a gravação depois do upload.
export const LIMITES_UPLOAD = { estado: 120, observacao: 1000, nomeArquivo: 260 }

export function validarEnvio({ estado, tipoDocumento, observacao, arquivo } = {}) {
  const e = (estado ?? '').trim()
  const o = (observacao ?? '').trim()

  if (!e) return { ok: false, erro: 'Informe o estado / CBM de origem do documento.' }
  if (e.length > LIMITES_UPLOAD.estado) {
    return { ok: false, erro: `O estado deve ter até ${LIMITES_UPLOAD.estado} caracteres.` }
  }
  if (!TIPOS_DOCUMENTO.includes(tipoDocumento)) {
    return { ok: false, erro: 'Escolha o tipo de documento.' }
  }
  if (o.length > LIMITES_UPLOAD.observacao) {
    return { ok: false, erro: `A observação deve ter até ${LIMITES_UPLOAD.observacao} caracteres.` }
  }
  if (!arquivo) return { ok: false, erro: 'Anexe o arquivo em PDF.' }
  if (arquivo.type !== 'application/pdf') {
    return { ok: false, erro: 'O arquivo precisa ser um PDF.' }
  }
  if (arquivo.size > LIMITE_TAMANHO_BYTES) {
    return { ok: false, erro: 'O arquivo passa de 20 MB. Envie um PDF menor.' }
  }

  return { ok: true, dados: { estado: e, tipoDocumento, observacao: o } }
}

// SEGURANÇA, não estética: barra no nome viraria subpasta e poderia escapar da pasta do
// próprio uid — que é justamente o que a regra do Storage usa para autorizar a escrita.
// Acentos saem porque nome de objeto no Storage com acento complica a URL de download.
export function nomeArquivoSeguro(nome) {
  const semAcento = (nome ?? '')
    .normalize('NFD')
    .replace(/[\u0300-\u036f]/g, '')   // tira os diacriticos separados pelo NFD
  const limpo = semAcento
    .replace(/[^a-zA-Z0-9._-]+/g, '-')     // tudo que não é seguro vira hífen (inclui / e \)
    .replace(/\.{2,}/g, '.')               // ".." não sobrevive
    .replace(/^[-.]+/, '')                 // não começa com hífen nem ponto
    .replace(/-{2,}/g, '-')
  const base = limpo || 'documento.pdf'
  if (base.length <= LIMITES_UPLOAD.nomeArquivo) return base

  // Trunca preservando a extensão: o admin precisa reconhecer que é PDF pela lista.
  const ext = base.toLowerCase().endsWith('.pdf') ? '.pdf' : ''
  return base.slice(0, LIMITES_UPLOAD.nomeArquivo - ext.length) + ext
}

export function caminhoUpload(uid, nomeArquivo, agoraMs) {
  return `uploads-visitantes/${uid}/${agoraMs}-${nomeArquivoSeguro(nomeArquivo)}`
}
```

- [ ] **Step 4: Rode o teste e confirme que passa**

```bash
node --test src/lib/uploadDocumento.test.js
```
Esperado: PASSA, todos os testes do arquivo.

- [ ] **Step 5: Rode a suíte inteira**

```bash
node --test
```
Esperado: PASSA. Eram 190 testes antes desta tarefa.

- [ ] **Step 6: Commit**

```bash
git add src/lib/uploadDocumento.js src/lib/uploadDocumento.test.js
git commit -m "feat(upload): lógica pura de validação e caminho do envio"
```

---

### Task 2: Reter o e-mail do visitante no estado local

O upload precisa gravar `emailVisitante`, mas hoje `useVisitante()` só expõe `{ uid, nome }` — e a regra do Firestore **não** permite o visitante reler o próprio documento em `visitantes/{uid}` (só o admin lê). A solução é reter no estado local o e-mail que a pessoa acabou de digitar no cadastro, sem leitura nova ao banco e sem afrouxar regra nenhuma.

**Files:**
- Modify: `src/lib/visitante.js` (`lerVisitanteLocal`, `gravarVisitanteLocal`)
- Modify: `src/lib/visitante.test.js` (acrescentar testes ao final)
- Modify: `src/lib/visitante.jsx` (`entrar`, para passar o e-mail adiante)

**Interfaces:**
- Consumes: nada de tarefas anteriores.
- Produces:
  - `lerVisitanteLocal(storage) -> { uid, nome, email } | null` — `email` é `''` quando ausente
  - `gravarVisitanteLocal(storage, { uid, nome, email })`
  - `useVisitante().visitante` passa a ser `{ uid, nome, email }`

- [ ] **Step 1: Escreva os testes que falham**

Acrescente ao FINAL de `src/lib/visitante.test.js` (não mexa nos testes existentes):

```js
// --- e-mail retido no estado local (entrega de upload, 2026-08-19) ----------

test('gravarVisitanteLocal e lerVisitanteLocal preservam o e-mail', () => {
  const s = storageFake()
  gravarVisitanteLocal(s, { uid: 'abc123', nome: 'Maria da Silva', email: 'maria@cbmpa.gov.br' })
  assert.deepEqual(lerVisitanteLocal(s), {
    uid: 'abc123', nome: 'Maria da Silva', email: 'maria@cbmpa.gov.br',
  })
})

// COMPATIBILIDADE: quem já era visitante antes desta mudança tem {uid,nome} gravado, sem
// email. Exigir o campo aqui deslogaria todos eles e pediria cadastro de novo — regressão
// gratuita. O e-mail ausente vira string vazia e a sessão continua válida.
test('lerVisitanteLocal aceita cadastro antigo sem e-mail (email vira "")', () => {
  const s = storageFake({ [CHAVE_LOCAL]: '{"uid":"abc","nome":"Maria"}' })
  assert.deepEqual(lerVisitanteLocal(s), { uid: 'abc', nome: 'Maria', email: '' })
})

test('lerVisitanteLocal ignora e-mail de tipo errado em vez de invalidar a sessão', () => {
  const s = storageFake({ [CHAVE_LOCAL]: '{"uid":"abc","nome":"Maria","email":42}' })
  assert.deepEqual(lerVisitanteLocal(s), { uid: 'abc', nome: 'Maria', email: '' })
})
```

- [ ] **Step 2: Rode o teste e confirme que falha**

```bash
node --test src/lib/visitante.test.js
```
Esperado: FALHA nos três testes novos — `lerVisitanteLocal` ainda devolve `{ uid, nome }` sem `email`, então o `deepEqual` acusa a diferença.

- [ ] **Step 3: Implemente**

Em `src/lib/visitante.js`, substitua as duas funções:

```js
export function lerVisitanteLocal(storage) {
  try {
    const cru = storage?.getItem(CHAVE_LOCAL)
    if (!cru) return null
    const v = JSON.parse(cru)
    if (!v || typeof v.uid !== 'string' || typeof v.nome !== 'string') return null
    // `email` entrou depois (entrega de upload): quem se cadastrou antes não tem o campo.
    // Ausente ou de tipo errado vira '' — nunca invalida a sessão, senão todo visitante
    // antigo seria deslogado e teria que se cadastrar de novo sem motivo.
    return { uid: v.uid, nome: v.nome, email: typeof v.email === 'string' ? v.email : '' }
  } catch {
    return null   // conteúdo corrompido ou ambiente sem localStorage: trate como "não há visitante"
  }
}

export function gravarVisitanteLocal(storage, { uid, nome, email }) {
  try {
    storage?.setItem(CHAVE_LOCAL, JSON.stringify({ uid, nome, email: email ?? '' }))
  } catch { /* ambiente sem localStorage */ }
}
```

Em `src/lib/visitante.jsx`, dentro de `entrar()`, passe o e-mail adiante nas duas linhas que hoje só levam `nome`:

```js
      gravarVisitanteLocal(globalThis.localStorage, { uid, nome: v.dados.nome, email: v.dados.email })
      setVisitante({ uid, nome: v.dados.nome, email: v.dados.email })
```

O `useEffect` que reconhece o visitante que volta **não muda**: ele já usa o objeto inteiro devolvido por `lerVisitanteLocal`, que agora traz o `email` junto.

- [ ] **Step 4: Corrija o teste existente que esta mudança quebra**

**Um teste que já existe VAI falhar, e isso é esperado** — ele afirma a forma antiga do
retorno. Em `src/lib/visitante.test.js`, o teste
`'gravarVisitanteLocal e lerVisitanteLocal fazem a volta completa'` hoje diz:

```js
test('gravarVisitanteLocal e lerVisitanteLocal fazem a volta completa', () => {
  const s = storageFake()
  gravarVisitanteLocal(s, { uid: 'abc123', nome: 'Maria da Silva' })
  assert.deepEqual(lerVisitanteLocal(s), { uid: 'abc123', nome: 'Maria da Silva' })
})
```

Passe a expectativa a incluir o campo novo (a gravação sem e-mail agora persiste `email: ''`):

```js
test('gravarVisitanteLocal e lerVisitanteLocal fazem a volta completa', () => {
  const s = storageFake()
  gravarVisitanteLocal(s, { uid: 'abc123', nome: 'Maria da Silva' })
  assert.deepEqual(lerVisitanteLocal(s), { uid: 'abc123', nome: 'Maria da Silva', email: '' })
})
```

Ajuste a **expectativa**, nunca o comportamento: o campo `email` passa a existir sempre, e é
isso que o teste deve afirmar. Não mexa em nenhum outro teste do arquivo.

- [ ] **Step 5: Rode os testes e confirme que passam**

```bash
node --test src/lib/visitante.test.js
```
Esperado: PASSA — os 15 testes antigos (um deles com a expectativa ajustada no passo acima) mais os 3 novos.

- [ ] **Step 6: Rode a suíte inteira e o build**

```bash
node --test && npm run build
```
Esperado: ambos passam.

- [ ] **Step 7: Commit**

```bash
git add src/lib/visitante.js src/lib/visitante.test.js src/lib/visitante.jsx
git commit -m "feat(upload): retém o e-mail do visitante no estado local"
```

---

### Task 3: Storage no projeto e camada de dados do upload

**Files:**
- Modify: `src/lib/firebase.js`
- Create: `src/lib/uploadsData.js`

**Interfaces:**
- Consumes: `caminhoUpload(uid, nomeArquivo, agoraMs)`, `nomeArquivoSeguro(nome)` de `src/lib/uploadDocumento.js` (Task 1).
- Produces:
  - `storage` (export de `src/lib/firebase.js`)
  - `enviarDocumento({ uid, nomeVisitante, emailVisitante, estado, tipoDocumento, observacao, arquivo }) -> Promise<void>`
  - `subscribeUploads(onChange, onError) -> () => void`
  - `urlDeDownload(storagePath) -> Promise<string>`
  - `removerUpload({ id, storagePath }) -> Promise<void>`

- [ ] **Step 1: Exporte o Storage em `src/lib/firebase.js`**

Duas linhas novas (import no topo, export no fim). `storageBucket` já está na config, vindo do `.env`:

```js
import { getStorage } from 'firebase/storage'
```

```js
export const storage = getStorage(app)
```

- [ ] **Step 2: Escreva a camada de dados**

Crie `src/lib/uploadsData.js`:

```js
// Envios de documentos pelos visitantes do acervo público (spec 2026-08-18).
// O ARQUIVO vai para o Storage (uploads-visitantes/{uid}/...) e os METADADOS para a
// coleção `uploadsVisitantes` do Firestore. Os dois lados são apagados juntos —
// ver removerUpload.
import {
  collection, addDoc, deleteDoc, doc, onSnapshot, query, orderBy, serverTimestamp,
} from 'firebase/firestore'
import { ref, uploadBytes, getDownloadURL, deleteObject } from 'firebase/storage'
import { db, storage } from './firebase.js'
import { caminhoUpload, nomeArquivoSeguro } from './uploadDocumento.js'

const COL = 'uploadsVisitantes'

// Ordem importa: sobe o arquivo PRIMEIRO, grava o metadado DEPOIS. Se o metadado falhar,
// apaga o arquivo recém-enviado — senão fica um objeto órfão no Storage, consumindo cota,
// sem nenhum registro que aponte para ele (ninguém jamais saberia que existe).
// A ordem inversa (metadado primeiro) deixaria uma linha na caixa de entrada do admin
// cujo botão "Baixar" quebra — pior, porque é visível e confunde.
export async function enviarDocumento({
  uid, nomeVisitante, emailVisitante, estado, tipoDocumento, observacao, arquivo,
}) {
  const storagePath = caminhoUpload(uid, arquivo.name, Date.now())
  const objeto = ref(storage, storagePath)
  await uploadBytes(objeto, arquivo, { contentType: 'application/pdf' })

  try {
    await addDoc(collection(db, COL), {
      uid,
      nomeVisitante,
      emailVisitante,
      estado,
      tipoDocumento,
      observacao,
      storagePath,
      nomeArquivo: nomeArquivoSeguro(arquivo.name),
      tamanho: arquivo.size,
      criadoEm: serverTimestamp(),
    })
  } catch (e) {
    await deleteObject(objeto).catch(() => { /* melhor esforço: o erro que importa é o de baixo */ })
    throw e
  }
}

export function subscribeUploads(onChange, onError) {
  const q = query(collection(db, COL), orderBy('criadoEm', 'desc'))
  return onSnapshot(q,
    (snap) => onChange(snap.docs.map(d => ({ id: d.id, ...d.data() }))),
    (err) => { if (onError) onError(err) },
  )
}

// URL gerada sob demanda (no clique), não na renderização da lista: uma chamada de rede
// por linha só para desenhar a tabela seria desperdício, e a URL tem validade própria.
export function urlDeDownload(storagePath) {
  return getDownloadURL(ref(storage, storagePath))
}

// Apaga os DOIS lados. O arquivo primeiro: se o Storage falhar, o metadado continua lá e
// o admin pode tentar de novo. Se fosse o contrário e o Storage falhasse, o arquivo
// ficaria órfão, invisível e impossível de achar pela interface.
export async function removerUpload({ id, storagePath }) {
  await deleteObject(ref(storage, storagePath))
  await deleteDoc(doc(db, COL, id))
}
```

- [ ] **Step 3: Verifique build e suíte**

```bash
npm run build && node --test
```
Esperado: build sem erro (confirma que o import de `firebase/storage` resolve); testes passando. Não há teste novo nesta tarefa — tudo aqui é I/O de rede, que este projeto não tem como testar sem Firebase ao vivo (mesma limitação das entregas anteriores).

- [ ] **Step 4: Commit**

```bash
git add src/lib/firebase.js src/lib/uploadsData.js
git commit -m "feat(upload): Storage no projeto e camada de dados dos envios"
```

---

### Task 4: Tela de envio e a terceira aba do acervo público

**Files:**
- Create: `src/pages/EnviarDocumento.jsx`
- Modify: `src/pages/AcervoPublico.jsx`
- Modify: `src/index.css` (ao final, junto do bloco `.pub-*`)

**Interfaces:**
- Consumes: `useVisitante()` → `{ visitante: { uid, nome, email } }` (Task 2); `TIPOS_DOCUMENTO`, `LIMITE_TAMANHO_BYTES`, `validarEnvio` (Task 1); `enviarDocumento(...)` (Task 3); `BASE_PUBLICA` de `src/lib/visitante.js`.
- Produces: rota `/acervo-publico/enviar`.

- [ ] **Step 1: Escreva a tela de envio**

Crie `src/pages/EnviarDocumento.jsx`:

```jsx
import { useState } from 'react'
import { UploadCloud } from 'lucide-react'
import { useVisitante } from '../lib/visitante.jsx'
import { TIPOS_DOCUMENTO, validarEnvio } from '../lib/uploadDocumento.js'
import { enviarDocumento } from '../lib/uploadsData.js'

// Envio de documentos pelo visitante (spec 2026-08-18): um campo único, compartilhado por
// todos os CBMs — a curadoria de cada arquivo é feita depois pelo administrador, fora do
// app. A tela não sabe nada de Storage: quem cuida disso é uploadsData.js.
export default function EnviarDocumento() {
  const { visitante } = useVisitante()
  const [estado, setEstado] = useState('')
  const [tipoDocumento, setTipoDocumento] = useState('')
  const [observacao, setObservacao] = useState('')
  const [arquivo, setArquivo] = useState(null)
  const [erro, setErro] = useState('')
  const [enviado, setEnviado] = useState(false)
  const [enviando, setEnviando] = useState(false)

  const submeter = async (e) => {
    e.preventDefault()
    setErro(''); setEnviado(false)

    const v = validarEnvio({ estado, tipoDocumento, observacao, arquivo })
    if (!v.ok) { setErro(v.erro); return }

    setEnviando(true)
    try {
      await enviarDocumento({
        uid: visitante.uid,
        nomeVisitante: visitante.nome,
        emailVisitante: visitante.email ?? '',
        ...v.dados,
        arquivo,
      })
      // Limpa para permitir outro envio na mesma visita — quem tem um documento costuma
      // ter dois.
      setEstado(''); setTipoDocumento(''); setObservacao(''); setArquivo(null)
      e.target.reset()
      setEnviado(true)
    } catch (err) {
      console.error('Falha ao enviar documento:', err)
      setErro(
        err?.code === 'storage/unauthorized'
          ? 'O envio de arquivos ainda não foi liberado no servidor. Avise o administrador do portal.'
          : 'Não foi possível enviar o documento agora. Tente novamente.',
      )
    } finally {
      setEnviando(false)
    }
  }

  return (
    <div className="pub-envio">
      <h2 className="pub-envio-titulo">Enviar documento ao acervo</h2>
      <p className="pub-envio-sub">
        Falta a legislação do seu estado aqui? Envie o PDF e ele entra na fila de análise da
        equipe do CBMRO. Um documento por envio.
      </p>

      <form className="pub-envio-form" onSubmit={submeter}>
        {erro && <div className="form-error">{erro}</div>}
        {enviado && (
          <div className="pub-envio-ok">
            Recebido, obrigado! O documento entra na fila de análise. Pode enviar outro, se quiser.
          </div>
        )}

        <label className="login-label">Estado / CBM de origem
          <input className="login-input" type="text" value={estado}
            onChange={ev => setEstado(ev.target.value)} maxLength={120} required
            placeholder="Ex.: CBMPA, CBMSC, CBMDF" />
        </label>

        <label className="login-label">Tipo de documento
          <select className="login-input" value={tipoDocumento}
            onChange={ev => setTipoDocumento(ev.target.value)} required>
            <option value="">Escolha…</option>
            {TIPOS_DOCUMENTO.map(t => <option key={t} value={t}>{t}</option>)}
          </select>
        </label>

        <label className="login-label">Observação (opcional)
          <textarea className="login-input pub-envio-obs" value={observacao}
            onChange={ev => setObservacao(ev.target.value)} maxLength={1000} rows={3}
            placeholder="Ex.: publicado no Diário Oficial de 03/2025; substitui a lei anterior" />
        </label>

        <label className="login-label">Arquivo (PDF, até 20 MB)
          <input className="login-input" type="file" accept="application/pdf"
            onChange={ev => setArquivo(ev.target.files?.[0] ?? null)} required />
        </label>

        <button className="login-btn" type="submit" disabled={enviando}>
          <UploadCloud size={16} /> {enviando ? 'Enviando…' : 'Enviar documento'}
        </button>

        <p className="pub-lgpd">
          Seu nome, e-mail e instituição acompanham o envio, para o administrador saber a
          origem do documento. O arquivo é analisado antes de qualquer publicação no acervo.
        </p>
      </form>
    </div>
  )
}
```

- [ ] **Step 2: Acrescente a aba e a rota em `src/pages/AcervoPublico.jsx`**

Três edições, todas pequenas. No topo, o import do ícone e da página:

```jsx
import { Library, Search as SearchIcon, LogIn, UploadCloud } from 'lucide-react'
```
```jsx
import EnviarDocumento from './EnviarDocumento.jsx'
```

Na `<nav className="pub-nav">`, um terceiro `NavLink`, **depois** do de Busca e **antes** do `<span className="pub-nav-quem">`:

```jsx
        <NavLink to={`${BASE_PUBLICA}/enviar`} className={({ isActive }) => `pub-nav-item${isActive ? ' active' : ''}`}>
          <UploadCloud size={16} /> Enviar documento
        </NavLink>
```

E, dentro do `<Routes>`, uma rota nova **antes** da rota curinga `path="*"`:

```jsx
            <Route path="enviar" element={<EnviarDocumento />} />
```

- [ ] **Step 3: Acrescente o CSS ao final de `src/index.css`**

```css
/* ===== Envio de documentos pelo visitante — spec 2026-08-18 ===== */
.pub-envio { max-width: 640px; margin: 0 auto; }
.pub-envio-titulo { font-size: 20px; color: #121d3d; margin: 0 0 4px; }
.pub-envio-sub { color: #5a667f; font-size: 13.5px; line-height: 1.5; margin: 0 0 18px; }
.pub-envio-form { background: #fff; border: 1px solid #d7deea; border-radius: 12px;
  padding: 20px; display: flex; flex-direction: column; }
.pub-envio-obs { resize: vertical; font-family: inherit; }
.pub-envio-ok { background: #e9f6ee; border: 1px solid #b7e0c6; color: #1d6b3a;
  border-radius: 8px; padding: 10px 12px; font-size: 13.5px; font-weight: 600;
  margin-bottom: 12px; }
```

- [ ] **Step 4: Verifique build e suíte**

```bash
npm run build && node --test
```
Esperado: build sem erro; testes passando.

- [ ] **Step 5: Suba o dev server e entregue o link**

```bash
npm run dev -- --port 5173 --strictPort
```
Confirme que o servidor sobe limpo (sem erro nos primeiros segundos) e informe ao Ten. Tiago: http://localhost:5173/acervo-publico/enviar. **Você não tem navegador** — não declare nada como verificado visualmente. E note: enquanto o bucket do Storage não existir (ver o bloco de pré-requisito no topo deste plano), o envio vai falhar — isso é esperado, não é defeito desta tarefa.

- [ ] **Step 6: Commit**

```bash
git add src/pages/EnviarDocumento.jsx src/pages/AcervoPublico.jsx src/index.css
git commit -m "feat(upload): tela de envio de documentos e aba no acervo público"
```

---

### Task 5: Regras de segurança — Firestore e Storage

**Files:**
- Modify: `firestore.rules`
- Create: `storage.rules`
- Modify: `docs/FIREBASE_SETUP.md`

**Interfaces:**
- Consumes: a função `isAdmin()` que já existe no topo do `firestore.rules`; os campos gravados por `enviarDocumento` (Task 3) e o caminho de `caminhoUpload` (Task 1).
- Produces: coleção `uploadsVisitantes` e prefixo `uploads-visitantes/` protegidos.

- [ ] **Step 1: Acrescente o bloco ao `firestore.rules`**

Dentro de `match /databases/{database}/documents {`, **depois** do bloco `match /visitantes/{uid}` (que é hoje o último):

```
    // Envios de documentos pelos visitantes (spec 2026-08-18). O visitante só CRIA, com o
    // próprio uid; nunca lê nem edita a fila — a caixa de entrada é do admin. O arquivo em
    // si mora no Storage (storage.rules, prefixo uploads-visitantes/); aqui ficam só os
    // metadados que a tela de /acessos mostra.
    match /uploadsVisitantes/{id} {
      allow read, delete: if isAdmin();
      allow create: if request.auth != null
        && request.resource.data.uid == request.auth.uid
        && request.resource.data.keys().hasOnly(
             ['uid','nomeVisitante','emailVisitante','estado','tipoDocumento','observacao',
              'storagePath','nomeArquivo','tamanho','criadoEm'])
        && request.resource.data.estado is string
        && request.resource.data.estado.size() > 0
        && request.resource.data.estado.size() <= 120
        && request.resource.data.tipoDocumento in
             ['Lei de Organização Básica','Regimento Interno','Regulamento de Serviço','Outro']
        && request.resource.data.observacao is string
        && request.resource.data.observacao.size() <= 1000
        && request.resource.data.nomeVisitante is string
        && request.resource.data.nomeVisitante.size() <= 200
        && request.resource.data.emailVisitante is string
        && request.resource.data.emailVisitante.size() <= 200
        && request.resource.data.nomeArquivo is string
        && request.resource.data.nomeArquivo.size() <= 260
        // `is number`, nao `is int`: File.size e inteiro, mas se o SDK serializar como
        // double a regra recusaria o metadado DEPOIS do upload inteiro ja ter subido.
        // O teto abaixo e o que realmente importa aqui.
        && request.resource.data.tamanho is number
        && request.resource.data.tamanho <= 20 * 1024 * 1024
        // O caminho declarado tem que ser dentro da pasta do próprio uid: sem isto, um
        // cliente adulterado apontaria o metadado para o arquivo de outra pessoa.
        && request.resource.data.storagePath is string
        && request.resource.data.storagePath.matches('^uploads-visitantes/' + request.auth.uid + '/.*');
    }
```

- [ ] **Step 2: Confirme que nenhuma regra existente mudou**

```bash
git diff firestore.rules
```
Esperado: **apenas adição**. Se alguma linha de `members`, `suggestions`, `finalTexts`, `config`, `decisions`, `conferencia` ou `visitantes` aparecer como removida (`-`), desfaça — esta entrega não afrouxa nada existente.

- [ ] **Step 3: Crie o `storage.rules`**

Arquivo NOVO na raiz do repositório (o projeto nunca usou Storage até aqui):

```
rules_version = '2';
service firebase.storage {
  match /b/{bucket}/o {

    // Mesmo critério de admin do firestore.rules: membro ativo com role 'admin'. Regras do
    // Storage podem consultar o Firestore — é assim que os dois lados falam a mesma língua
    // sem duplicar a lista de administradores.
    function memberRef() {
      return /databases/(default)/documents/members/$(request.auth.token.email);
    }
    function isAdmin() {
      return request.auth != null
        && request.auth.token.email != null
        && firestore.exists(memberRef())
        && firestore.get(memberRef()).data.ativo == true
        && firestore.get(memberRef()).data.role == 'admin';
    }

    // Envios do acervo público. Cada visitante escreve SÓ dentro da pasta do próprio uid.
    // Tamanho e tipo são reforçados AQUI, não só no formulário: um cliente adulterado não
    // pode subir um executável de 500 MB só porque o JavaScript da página foi contornado.
    match /uploads-visitantes/{uid}/{arquivo} {
      allow read: if isAdmin();
      allow delete: if isAdmin();
      allow create: if request.auth != null
        && request.auth.uid == uid
        && request.resource.size <= 20 * 1024 * 1024
        && request.resource.contentType == 'application/pdf';
    }

    // Nada mais no bucket é acessível pelo cliente.
    match /{caminho=**} {
      allow read, write: if false;
    }
  }
}
```

**Confira a sintaxe de `firestore.get()` em regra de Storage contra a documentação atual do Firebase antes de publicar** — é o primeiro uso deste recurso no projeto e não há como testá-lo sem um projeto ao vivo. Se a sintaxe divergir, corrija aqui e anote no relatório.

- [ ] **Step 4: Documente os passos manuais em `docs/FIREBASE_SETUP.md`**

Acrescente ao final do arquivo:

```markdown
## Envio de documentos pelo visitante (upload) — 2026-08-19

**Pré-requisito que pode custar dinheiro:** o Cloud Storage **não estava provisionado**
neste projeto (verificado em 2026-08-19: o bucket
`revisao-minuta-cbmro-6f248.firebasestorage.app` respondia 404). Desde outubro de 2024 o
Firebase exige o **plano Blaze** (pago por uso, com cota gratuita mensal) para criar o
bucket padrão. Sem o bucket, a tela de envio existe mas nenhum arquivo sobe.

Passos manuais no console do projeto `revisao-minuta-cbmro-6f248`, na conta institucional:

1. **Build → Storage → "Começar"**, para provisionar o bucket padrão (exige o plano Blaze).
2. **Storage → Rules:** publicar o `storage.rules` deste repositório (arquivo novo — antes
   desta entrega o projeto não tinha nenhuma regra de Storage).
3. **Firestore → Rules:** republicar o `firestore.rules`, que passou a conter o bloco
   `match /uploadsVisitantes/{id}`.

Conferência depois de publicar: abrir `/acervo-publico/enviar` como visitante, enviar um PDF
pequeno, e verificar se ele aparece em `/acessos`, seção "Documentos enviados por
visitantes", com o botão **Baixar** funcionando.
```

- [ ] **Step 5: Commit**

```bash
git add firestore.rules storage.rules docs/FIREBASE_SETUP.md
git commit -m "feat(upload): regras de Firestore e Storage para os envios"
```

---

### Task 6: Caixa de entrada do administrador em `/acessos`

**Files:**
- Modify: `src/pages/Acessos.jsx`
- Modify: `src/index.css` (uma regra, junto do bloco `.pub-envio-*`)

**Interfaces:**
- Consumes: `subscribeUploads(onChange, onError)`, `urlDeDownload(storagePath)`, `removerUpload({ id, storagePath })` de `src/lib/uploadsData.js` (Task 3); `AvisoSincronizacao` de `src/components/AvisoSincronizacao.jsx`; o helper `formatLogin` já definido no topo de `Acessos.jsx`.

- [ ] **Step 1: Assine o feed e escreva as ações**

Em `src/pages/Acessos.jsx`, acrescente os imports:

```jsx
import { subscribeUploads, urlDeDownload, removerUpload } from '../lib/uploadsData.js'
```

Dentro do componente `Acessos()`, junto dos outros `useState`/`useEffect` (logo depois do bloco de `visitantes`):

```jsx
  const [uploads, setUploads] = useState([])
  const [erroUploads, setErroUploads] = useState(false)

  // Erro visível na tela, nunca só no console (AR-04): sem isto, uma queda do feed deixaria
  // a seção mostrando "nenhum envio", que é indistinguível de "ninguém enviou nada" e mente
  // para o administrador — que poderia perder um documento enviado.
  useEffect(() => subscribeUploads(
    (lista) => { setUploads(lista); setErroUploads(false) },
    (e) => { console.error('Erro ao carregar envios:', e); setErroUploads(true) },
  ), [])

  const baixar = async (u) => {
    try {
      const url = await urlDeDownload(u.storagePath)
      window.open(url, '_blank', 'noopener')
    } catch (err) {
      console.error(err); setErro('Não foi possível abrir o arquivo enviado.')
    }
  }
  const removerEnvio = async (u) => {
    if (!window.confirm(`Remover o envio "${u.nomeArquivo}"? O arquivo é apagado junto e não há como desfazer.`)) return
    try { await removerUpload({ id: u.id, storagePath: u.storagePath }) }
    catch (err) { console.error(err); setErro('Não foi possível remover o envio.') }
  }
```

- [ ] **Step 2: Escreva um formatador de tamanho, ao lado de `formatLogin`**

No topo de `src/pages/Acessos.jsx`, logo depois da função `formatLogin`:

```jsx
function formatTamanho(bytes) {
  if (typeof bytes !== 'number' || bytes < 0) return '—'
  const mb = bytes / (1024 * 1024)
  return mb >= 1 ? `${mb.toFixed(1)} MB` : `${Math.max(1, Math.round(bytes / 1024))} KB`
}
```

- [ ] **Step 3: Renderize a seção**

Antes do `</div>` que fecha `.acc-wrap`, ao FINAL do JSX (depois da seção "Visitantes do acervo público"):

```jsx
      <h3 className="acc-sec-title">Documentos enviados por visitantes ({uploads.length})</h3>
      <p className="acc-sub">
        Legislações que militares de outros CBMs enviaram pela página pública. Baixe, avalie e
        — se aproveitar — ingira no acervo pelo processo de sempre. Remover apaga o arquivo junto.
      </p>

      <AvisoSincronizacao visivel={erroUploads}>
        Não foi possível carregar os envios agora — a lista abaixo pode estar incompleta ou
        desatualizada.
      </AvisoSincronizacao>

      <div className="acc-panel">
        <table className="acc-table">
          <thead>
            <tr>
              <th>Documento</th><th>Enviado por</th><th>Observação</th><th>Quando</th><th></th>
            </tr>
          </thead>
          <tbody>
            {uploads.length === 0 && !erroUploads && (
              <tr><td colSpan={5} className="acc-mail">Nenhum documento enviado até agora.</td></tr>
            )}
            {uploads.map(u => (
              <tr key={u.id}>
                <td>
                  <div className="acc-nome">{u.estado} · {u.tipoDocumento}</div>
                  <div className="acc-mail">{u.nomeArquivo} · {formatTamanho(u.tamanho)}</div>
                </td>
                <td>
                  <div className="acc-nome">{u.nomeVisitante}</div>
                  {/* E-mail pode faltar em envio de visitante cadastrado ANTES desta entrega
                      (o campo só passou a ser retido agora): cai para a lista de visitantes,
                      que o admin já tem carregada nesta mesma tela. */}
                  <div className="acc-mail">
                    {u.emailVisitante || visitantes.find(v => v.id === u.uid)?.email || '—'}
                  </div>
                </td>
                <td className="acc-papel">{u.observacao || '—'}</td>
                <td className={formatLogin(u.criadoEm) ? 'acc-quando' : 'acc-nunca'}>
                  {formatLogin(u.criadoEm) ?? '—'}
                </td>
                <td>
                  <div className="acc-acts">
                    <button type="button" className="acc-ic" onClick={() => baixar(u)}>baixar</button>
                    <button type="button" className="acc-ic danger" onClick={() => removerEnvio(u)}>remover</button>
                  </div>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
```

`formatLogin` e `visitantes` já existem neste arquivo — reuse, não duplique.

- [ ] **Step 4: Verifique build e suíte**

```bash
npm run build && node --test
```
Esperado: build sem erro; testes passando.

- [ ] **Step 5: Commit**

```bash
git add src/pages/Acessos.jsx src/index.css
git commit -m "feat(upload): caixa de entrada dos envios em /acessos"
```

---

### Task 7: Documentação do repositório

**Files:**
- Modify: `CLAUDE.md`
- Modify: `.claude/PENDENCIAS.md`
- Modify: `src/pages/Manual.jsx`

- [ ] **Step 1: Registre a arquitetura no `CLAUDE.md`**

Na seção "Revisão Colaborativa da Minuta", logo **depois** do parágrafo "**Terceiro perfil — acervo público**" (que a entrega anterior acrescentou), insira:

```markdown
**Envio de documentos pelo visitante (2026-08-19, spec `2026-08-18-acervo-publico-upload-documentos-design.md`):**
a finalidade do perfil público não é só consulta — militares de outros CBMs contribuem com
legislações ausentes do acervo por `/acervo-publico/enviar`. **Primeiro uso de Firebase
Storage no projeto** (`uploads-visitantes/{uid}/…`, regras em `storage.rules`, arquivo novo
que precisa ser publicado à parte do `firestore.rules`); metadados na coleção
`uploadsVisitantes` (só o admin lê e apaga). Lógica pura em `src/lib/uploadDocumento.js`
(validação, `nomeArquivoSeguro` — barra no nome escaparia da pasta do uid, que é o que a
regra do Storage usa para autorizar); I/O em `src/lib/uploadsData.js` (sobe o arquivo antes
do metadado e apaga o arquivo se o metadado falhar, para não deixar órfão). Caixa de
entrada do admin em `/acessos`; a curadoria em si continua MANUAL, fora do app. O
`VisitanteProvider` passou a reter o `email` no estado local — a regra de `visitantes/{uid}`
não deixa o visitante reler o próprio cadastro, e cadastro antigo sem o campo continua
válido (`email: ''`), sem deslogar ninguém.
```

- [ ] **Step 2: Atualize o backlog**

Em `.claude/PENDENCIAS.md`, no topo da seção `## 🔴 Pendente`:

```markdown
- [ ] **Acervo público / upload — provisionar o Cloud Storage (pode exigir plano Blaze)**
  (entrega de 19/08/2026). Verificado em 19/08: o bucket
  `revisao-minuta-cbmro-6f248.firebasestorage.app` responde **404** — o Storage nunca foi
  provisionado neste projeto. Desde out/2024 o Firebase exige o **plano Blaze** para criar o
  bucket padrão. Enquanto isso não for resolvido, a tela `/acervo-publico/enviar` existe mas
  nenhum arquivo sobe. Depois de provisionar: publicar o `storage.rules` (arquivo novo) e
  republicar o `firestore.rules`. Ver `docs/FIREBASE_SETUP.md`, seção "Envio de documentos".
- [ ] **Acervo público / upload — conferência visual** (o agente não tem navegador): enviar
  um PDF por `/acervo-publico/enviar` e conferir que aparece em `/acessos` com "baixar"
  funcionando.
```

E na seção de concluídas do mês:

```markdown
- [x] **Upload de documentos pelo visitante público** — 19/08/2026. Militares de outros CBMs
  enviam PDFs (até 20 MB) de legislações ausentes do acervo; admin vê a caixa de entrada em
  `/acessos`, baixa e remove. Firebase Storage + coleção `uploadsVisitantes`. Curadoria
  segue manual. Spec e plano em `docs/superpowers/`.
```

- [ ] **Step 3: Documente no Manual de uso**

Em `src/pages/Manual.jsx`, no array `SECTIONS`, logo **depois** da seção `id: 'acervo-publico'` (acrescentada na entrega anterior), insira:

```jsx
  {
    id: 'acervo-publico-envio', title: 'Acervo público — recebendo documentos',
    body: (
      <>
        <p>
          Quem entra pela página pública (<b>/acervo-publico</b>) também pode <b>contribuir</b>:
          a aba <b>Enviar documento</b> aceita um PDF de até 20 MB, com o estado de origem, o
          tipo de documento e uma observação.
        </p>
        <ul>
          <li>Os envios aparecem em <b>Acessos</b>, seção <b>Documentos enviados por visitantes</b>.</li>
          <li>Clique em <b>baixar</b> para abrir o PDF e avaliar.</li>
          <li>Se o documento for aproveitado, ele entra no acervo pelo <b>processo de ingestão de
              sempre</b> — o envio não publica nada sozinho.</li>
          <li><b>remover</b> tira da lista e apaga o arquivo junto; use depois de já ter baixado
              ou decidido descartar.</li>
        </ul>
        <div className="manual-callout">
          <b>Nada entra no acervo automaticamente.</b> A tela de envio é uma caixa de entrada:
          todo arquivo passa pela curadoria antes de virar parte do acervo comparado.
        </div>
      </>
    ),
  },
```

- [ ] **Step 4: Verifique build e suíte**

```bash
npm run build && node --test
```
Esperado: build sem erro (confirma que o JSX novo do Manual é válido); testes passando.

- [ ] **Step 5: Commit**

```bash
git add CLAUDE.md .claude/PENDENCIAS.md src/pages/Manual.jsx
git commit -m "docs: registra o envio de documentos pelo visitante público"
```

---

## Conferência final (humana, não do agente)

**Só é possível depois de provisionar o Storage** (ver o bloco de pré-requisito no topo).
Com o bucket criado e as duas regras publicadas, o Ten. Tiago verifica:

1. Como visitante, `/acervo-publico/enviar` mostra o formulário com as três abas na barra.
2. Tentar enviar um arquivo que não é PDF → mensagem clara, sem subir nada.
3. Tentar enviar um PDF acima de 20 MB → mensagem clara sobre o limite.
4. Enviar um PDF válido → mensagem de confirmação, formulário limpo.
5. Em `/acessos`, o envio aparece na seção nova, com estado, tipo, quem enviou e tamanho.
6. **baixar** abre o PDF correto.
7. **remover** tira da lista; conferir no console do Firebase que o arquivo saiu do Storage também.
8. Como participante comum (não admin), `/acessos` continua inacessível.
