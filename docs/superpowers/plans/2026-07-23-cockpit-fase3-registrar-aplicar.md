# Cockpit Fase 3 — registrar e aplicar decisões — Plano de Implementação

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Registrar decisões pelo sistema (Firebase), aplicá-las à minuta (texto final no Wizard/.docx ou ficha estrutural), persistir o "Divergente" da Conferência e devolver as decisões ao vault Obsidian.

**Architecture:** Coleções novas `decisions` e `conferencia` no Firestore (mesma base da Revisão), com encoding de id na fronteira (Task 1 corrige bug latente do `finalTexts`). Overlay de textos finais aplicado PÓS-`buildArticles` por função pura, reusada pelos 2 Wizards e pelo `.docx`. Exportação client-side + script Python local fecha o ciclo com o vault.

**Tech Stack:** React/Vite, Firebase (Auth+Firestore, web SDK), `node --test`, Python 3.10+ (venv `.venv-pipeline/`), lib `docx`.

## Global Constraints

- **Encoding de id Firestore:** `editId` contém `/` (ex.: `organ:cg/finalidade`) e ids de documento Firestore NÃO aceitam `/`. TODA gravação/leitura de doc chaveado por dispositivoId/chave composta passa por `encodeFirestoreId`/`decodeFirestoreId` (Task 1; troca `/`↔`|`; confirmado que nenhum editId contém `|`). Dentro do app os ids circulam SEM encoding.
- **Permissão:** registrar/desfazer decisão e marcar ficha = papel admin (`user.role === 'admin'` via `useAuth()`); conferência persistida = qualquer membro logado; sem login = leitura/estado local com aviso visível (nunca falha silenciosa).
- **Cenário:** o alvo de redação vale no cenário ativo no registro; NENHUM caminho de código faz de-para automático de dispositivo entre cenários (anti-AR-01). Isolamento via marcador já embutido no editId (`atual:`/`reg:atual:`), lido por `docOfDispositivo`/`scenarioOfDispositivo` de `src/lib/reviewGroup.js`.
- **Sem sucesso parcial silencioso:** gravações Firebase com erro → mensagem visível; script do vault: conflito/nota ausente → relatório + saída ≠ 0; idempotente.
- **Fidelidade:** texto final substitui exatamente o que o Wândrio salvou; export JSON carrega o texto verbatim da decisão.
- Python roda via `.venv-pipeline/bin/python` (PEP 668). Vault: mesma constante/env `VAULT_CURADORIA` do `build_decisoes_curadoria.py`.
- `firestore.rules` muda no repo, mas só vale após publicação manual no console (avisar na entrega).
- Suíte JS: `node --test` (hoje 119 + os novos); testes Python novos em `scripts/test_aplicar_decisoes_vault.py`.

---

### Task 1: Encoding de id na fronteira do Firestore (corrige bug latente do finalTexts)

**Files:**
- Modify: `src/lib/dispositivoId.js` (adicionar 2 funções no fim)
- Modify: `src/lib/reviewData.js:56-75` (saveFinalText + subscribeFinalTexts)
- Test: `src/lib/dispositivoId.test.js` (append)

**Interfaces:**
- Produces: `encodeFirestoreId(id: string): string` e `decodeFirestoreId(id: string): string` — usadas por TODAS as tasks que gravam docs chaveados (T2, T4).

**Contexto:** `saveFinalText(dispositivoId, ...)` usa o id cru como id de documento. Como todo editId tem `/` (ex.: `organ:cg/competencia#caput`), `doc(db, 'finalTexts', id)` produz um caminho de 3 segmentos e LANÇA erro — bug latente (nunca gravou; logo, não há migração de dados a fazer).

- [ ] **Step 1: Verificação empírica** (não commitada — evidência para o relatório)

Rode no diretório do projeto:
```bash
node --input-type=module -e "
import { initializeApp } from 'firebase/app'
import { getFirestore, doc } from 'firebase/firestore'
const app = initializeApp({ projectId: 'proj-teste', apiKey: 'x', appId: 'x' })
const db = getFirestore(app)
try { doc(db, 'finalTexts', 'organ:cg/competencia#caput'); console.log('ACEITOU (inesperado)') }
catch (e) { console.log('LANÇOU (bug confirmado):', e.message.slice(0, 120)) }
try { doc(db, 'finalTexts', 'organ:cg|competencia#caput'); console.log('COM PIPE: aceitou') }
catch (e) { console.log('COM PIPE lançou:', e.message.slice(0, 120)) }
"
```
Expected: primeira tentativa LANÇA ("even number of segments"); com `|` aceita. Cole a saída no relatório.

- [ ] **Step 2: Teste que falha** — append em `src/lib/dispositivoId.test.js`:

```javascript
import { encodeFirestoreId, decodeFirestoreId } from './dispositivoId.js'

test('encodeFirestoreId troca / por | e faz round-trip', () => {
  const id = 'atual:organ:cg/competencia#caput'
  const enc = encodeFirestoreId(id)
  assert.ok(!enc.includes('/'))
  assert.equal(enc, 'atual:organ:cg|competencia#caput')
  assert.equal(decodeFirestoreId(enc), id)
})

test('encodeFirestoreId é no-op sem barra', () => {
  assert.equal(encodeFirestoreId('reg:tema#3'), 'reg:tema#3')
})
```
(Se o arquivo de teste usa outro estilo de import de `test`/`assert`, siga o estilo existente do arquivo.)

- [ ] **Step 3: Rodar e ver falhar** — `node --test src/lib/dispositivoId.test.js` → FAIL (função não existe).

- [ ] **Step 4: Implementar** — append em `src/lib/dispositivoId.js`:

```javascript
// Fronteira Firestore: ids de documento não aceitam '/', mas todo editId tem
// (ex.: organ:cg/competencia). Troca por '|' (ausente em todos os editIds — verificado
// nos 4 structure.json em 2026-07-23). Dentro do app os ids circulam SEM encoding.
export function encodeFirestoreId(id) {
  return String(id).replaceAll('/', '|')
}

export function decodeFirestoreId(id) {
  return String(id).replaceAll('|', '/')
}
```

- [ ] **Step 5: Aplicar na fronteira do finalTexts** — em `src/lib/reviewData.js`: importar `{ encodeFirestoreId, decodeFirestoreId } from './dispositivoId.js'`; em `saveFinalText`, trocar `doc(db, COL_FINAL, dispositivoId)` por `doc(db, COL_FINAL, encodeFirestoreId(dispositivoId))`; em `subscribeFinalTexts`, trocar `map.set(d.id, d.data())` por `map.set(decodeFirestoreId(d.id), d.data())`.

- [ ] **Step 6: Rodar** — `node --test` → tudo verde (121). **Step 7: Commit** — `git add src/lib/dispositivoId.js src/lib/dispositivoId.test.js src/lib/reviewData.js && git commit -m "fix(revisao): encoding de dispositivoId na fronteira Firestore (bug latente do finalTexts)"`

---

### Task 2: Dados de decisão — `decisionsData.js` + `decisionsMerge.js` + rules

**Files:**
- Create: `src/lib/decisionsData.js`
- Create: `src/lib/decisionsMerge.js`
- Test: `src/lib/decisionsMerge.test.js`
- Modify: `firestore.rules` (2 blocos novos antes do fechamento)

**Interfaces:**
- Consumes: `encodeFirestoreId` (Task 1).
- Produces: `subscribeDecisions(onChange, onError)` → Map(id→doc); `registrarDecisao(id, dados, autor)`; `marcarFichaAplicada(id)`; `desfazerDecisao(id)`; `mergeDecisoes(decisoesJson, fbMap)` → array com `statusDecisao: 'sistema'|'vault'|'pendente'` e `registro`; `pendenciasDeAplicacao(merged)` → fichas aguardando.

- [ ] **Step 1: Teste que falha** — `src/lib/decisoesMerge.test.js` → use o nome `src/lib/decisionsMerge.test.js`:

```javascript
import { test } from 'node:test'
import assert from 'node:assert/strict'
import { mergeDecisoes, pendenciasDeAplicacao } from './decisionsMerge.js'

const json = [
  { id: 'a', decidido: false },
  { id: 'b', decidido: true },
  { id: 'c', decidido: true },   // vault diz decidida, mas sistema também tem — sistema vence
  { id: 'd', decidido: false },
]
const fb = new Map([
  ['c', { tipo: 'redacao', decisao: 'texto C' }],
  ['d', { tipo: 'estrutural', decisao: 'x', ficha: { oQueMuda: 'fundir', onde: 'dlog', status: 'aguardando' } }],
])

test('mergeDecisoes: sistema > vault > pendente', () => {
  const m = mergeDecisoes(json, fb)
  assert.equal(m[0].statusDecisao, 'pendente')
  assert.equal(m[1].statusDecisao, 'vault')
  assert.equal(m[2].statusDecisao, 'sistema')
  assert.equal(m[2].registro.decisao, 'texto C')
  assert.equal(m[3].statusDecisao, 'sistema')
})

test('mergeDecisoes tolera fbMap null', () => {
  assert.equal(mergeDecisoes(json, null)[1].statusDecisao, 'vault')
})

test('pendenciasDeAplicacao: só ficha estrutural aguardando', () => {
  const p = pendenciasDeAplicacao(mergeDecisoes(json, fb))
  assert.equal(p.length, 1)
  assert.equal(p[0].id, 'd')
})
```

- [ ] **Step 2: Ver falhar** — `node --test src/lib/decisionsMerge.test.js` → FAIL.

- [ ] **Step 3: Implementar `src/lib/decisionsMerge.js`** (puro, sem Firebase):

```javascript
// Funde as decisões do JSON (pipeline da Fase 2) com os registros do Firebase.
// Precedência: registro no sistema > decidida no vault > pendente.
export function mergeDecisoes(decisoesJson, fbMap) {
  return (decisoesJson ?? []).map(d => {
    const registro = fbMap?.get(d.id) ?? null
    if (registro) return { ...d, statusDecisao: 'sistema', registro }
    if (d.decidido) return { ...d, statusDecisao: 'vault', registro: null }
    return { ...d, statusDecisao: 'pendente', registro: null }
  })
}

export function pendenciasDeAplicacao(merged) {
  return merged.filter(d =>
    d.registro?.tipo === 'estrutural' && d.registro?.ficha?.status === 'aguardando')
}
```

- [ ] **Step 4: Implementar `src/lib/decisionsData.js`** (espelha `reviewData.js`):

```javascript
// CRUD da coleção 'decisions' (decisões CBMRO registradas pelo sistema).
// Chave = id da decisão (nome da nota no vault, sem extensão). Encoding na fronteira
// por consistência (ids de decisão não têm '/', mas a regra é uniforme).
import {
  collection, doc, onSnapshot, setDoc, updateDoc, deleteDoc, serverTimestamp,
} from 'firebase/firestore'
import { db } from './firebase.js'
import { encodeFirestoreId, decodeFirestoreId } from './dispositivoId.js'

const COL = 'decisions'

export function subscribeDecisions(onChange, onError) {
  return onSnapshot(collection(db, COL),
    (snap) => {
      const map = new Map()
      snap.docs.forEach(d => map.set(decodeFirestoreId(d.id), d.data()))
      onChange(map)
    },
    (err) => { if (onError) onError(err) },
  )
}

// dados: { tipo, decisao, fonteEscolhida, alvoDispositivoId | null, ficha | null }
export async function registrarDecisao(id, dados, autor) {
  await setDoc(doc(db, COL, encodeFirestoreId(id)), {
    ...dados,
    registradoPor: autor.nome,
    registradoEm: serverTimestamp(),
  })
}

export async function marcarFichaAplicada(id) {
  await updateDoc(doc(db, COL, encodeFirestoreId(id)), { 'ficha.status': 'aplicada' })
}

export async function desfazerDecisao(id) {
  await deleteDoc(doc(db, COL, encodeFirestoreId(id)))
}
```

- [ ] **Step 5: Rules** — em `firestore.rules`, adicionar após o bloco `config/revisao` (mesmo estilo dos existentes):

```
    match /decisions/{id} {
      allow read: if isMember();
      allow write: if isAdmin();
    }

    match /conferencia/{id} {
      allow read: if isMember();
      allow write: if isMember();
    }
```

- [ ] **Step 6: Rodar** — `node --test` → verde. **Step 7: Commit** — `git add src/lib/decisionsData.js src/lib/decisionsMerge.js src/lib/decisionsMerge.test.js firestore.rules && git commit -m "feat(decisoes): coleção decisions (CRUD+merge puro) e rules (decisions admin, conferencia membro)"`

---

### Task 3: Overlay de textos finais no Wizard e no .docx

**Files:**
- Create: `src/lib/minutaFinals.js`
- Test: `src/lib/minutaFinals.test.js`
- Modify: `src/lib/minutaDocx.js:9,42` (novo param `finals`/`skipEditIds`)
- Modify: `src/pages/MinutaWizard.jsx` e `src/pages/RegulamentoWizard.jsx` (assinar finals logado, aplicar, badge/aviso, passar ao docx)

**Interfaces:**
- Consumes: `subscribeFinalTexts` (`reviewData.js`), `filterFinalsByDoc`/`filterFinalsByScenario` (`reviewGroup.js`), `caputDispositivoId`/`incisoDispositivoId` (`dispositivoId.js`), `useAuth`, `useScenario`.
- Produces: `applyFinalsToArticles(articles, finalsMap, { skipEditIds }) -> { articles, appliedCount }` — também usada pelo docx.

**Regras de aplicação (exatas):** só `status === 'fechado'`; final de caput (`editId#caput`) só se aquele editId gera UM artigo (capítulos-prosa que se desdobram em vários artigos ficam de fora — limitação herdada da premissa do dispositivoId); final de inciso casa pelo índice ORIGINAL (`editId#index`); `skipEditIds` = folhas com edição manual viva no modo avançado (a edição manual do usuário vence).

- [ ] **Step 1: Teste que falha** — `src/lib/minutaFinals.test.js`:

```javascript
import { test } from 'node:test'
import assert from 'node:assert/strict'
import { applyFinalsToArticles } from './minutaFinals.js'

const articles = [
  { number: 1, editId: 'organ:cg/competencia', caput: 'Compete ao CG:',
    incisos: [{ text: 'planejar', index: 0 }, { text: 'dirigir', index: 2 }] },
  { number: 2, editId: 'preliminares', caput: 'Linha A', incisos: [] },
  { number: 3, editId: 'preliminares', caput: 'Linha B', incisos: [] },
]

test('aplica final de caput quando editId gera 1 artigo', () => {
  const finals = new Map([['organ:cg/competencia#caput', { texto: 'NOVO CAPUT', status: 'fechado' }]])
  const r = applyFinalsToArticles(articles, finals)
  assert.equal(r.articles[0].caput, 'NOVO CAPUT')
  assert.equal(r.articles[0].hasFinal, true)
  assert.equal(r.appliedCount, 1)
})

test('final de inciso casa pelo índice ORIGINAL', () => {
  const finals = new Map([['organ:cg/competencia#2', { texto: 'coordenar', status: 'fechado' }]])
  const r = applyFinalsToArticles(articles, finals)
  assert.equal(r.articles[0].incisos[1].text, 'coordenar')
  assert.equal(r.articles[0].incisos[0].text, 'planejar')
})

test('não aplica: status aberto, editId ambíguo (prosa), skipEditIds', () => {
  const finals = new Map([
    ['organ:cg/competencia#caput', { texto: 'X', status: 'aberto' }],
    ['preliminares#caput', { texto: 'Y', status: 'fechado' }],       // 2 artigos → ambíguo
  ])
  const r = applyFinalsToArticles(articles, finals)
  assert.equal(r.appliedCount, 0)
  const r2 = applyFinalsToArticles(articles,
    new Map([['organ:cg/competencia#caput', { texto: 'Z', status: 'fechado' }]]),
    { skipEditIds: new Set(['organ:cg/competencia']) })
  assert.equal(r2.appliedCount, 0)
})

test('mapa vazio/null é no-op', () => {
  assert.equal(applyFinalsToArticles(articles, null).appliedCount, 0)
  assert.equal(applyFinalsToArticles(articles, new Map()).articles, articles)
})
```

- [ ] **Step 2: Ver falhar.** `node --test src/lib/minutaFinals.test.js`

- [ ] **Step 3: Implementar `src/lib/minutaFinals.js`:**

```javascript
// Aplica os textos finais (finalTexts, status 'fechado') sobre os artigos JÁ montados
// por buildArticles. Usada pelos Wizards (tela) e pelo minutaDocx (.docx) — a mesma
// função nos dois lugares garante que o documento baixado é o que se vê.
import { caputDispositivoId, incisoDispositivoId } from './dispositivoId.js'

export function applyFinalsToArticles(articles, finalsMap, { skipEditIds = new Set() } = {}) {
  if (!finalsMap || finalsMap.size === 0) return { articles, appliedCount: 0 }
  const artigosPorEditId = new Map()
  for (const a of articles) {
    artigosPorEditId.set(a.editId, (artigosPorEditId.get(a.editId) ?? 0) + 1)
  }
  let appliedCount = 0
  const out = articles.map(a => {
    if (skipEditIds.has(a.editId)) return a
    let art = a
    const capFinal = finalsMap.get(caputDispositivoId(a.editId))
    if (capFinal?.status === 'fechado' && artigosPorEditId.get(a.editId) === 1) {
      art = { ...art, caput: capFinal.texto, hasFinal: true }
      appliedCount += 1
    }
    let mudouInciso = false
    const incisos = (art.incisos ?? []).map(inc => {
      const f = finalsMap.get(incisoDispositivoId(a.editId, inc.index))
      if (f?.status === 'fechado') { mudouInciso = true; appliedCount += 1; return { ...inc, text: f.texto, source: null } }
      return inc
    })
    if (mudouInciso) art = { ...art, incisos, hasFinal: true }
    return art
  })
  return { articles: out, appliedCount }
}
```

- [ ] **Step 4: docx** — em `src/lib/minutaDocx.js`: importar `applyFinalsToArticles`; assinatura vira `buildMinutaBlob({ structure, edits = {}, isExcluded = () => false, subtitle, finals = null, skipEditIds })`; logo após `const articles = buildArticles(structure, edits, isExcluded)` (linha ~42), inserir:

```javascript
  const withFinals = finals
    ? applyFinalsToArticles(articles, finals, { skipEditIds: skipEditIds ?? new Set(Object.keys(edits)) }).articles
    : articles
```
e usar `withFinals` no lugar de `articles` dali em diante (renomear a variável de consumo).

- [ ] **Step 5: Wizards** — em `MinutaWizard.jsx` e `RegulamentoWizard.jsx` (mesma mudança, doc `'ri'` no primeiro e `'reg'` no segundo):
  1. Imports: `useAuth` de `../lib/auth.jsx`, `subscribeFinalTexts` de `../lib/reviewData.js`, `filterFinalsByDoc, filterFinalsByScenario` de `../lib/reviewGroup.js`, `applyFinalsToArticles` de `../lib/minutaFinals.js`, `useScenario` (se ainda não importado).
  2. Estado: `const { user } = useAuth()`; `const [finals, setFinals] = useState(null)`; efeito:
```javascript
  useEffect(() => {
    if (!user) { setFinals(null); return undefined }
    return subscribeFinalTexts(setFinals, (e) => console.error('Erro finalTexts:', e))
  }, [user])
  const finalsDoDoc = useMemo(() => {
    if (!finals) return null
    return filterFinalsByScenario(filterFinalsByDoc(finals, 'ri'), cenario)  // 'reg' no RegulamentoWizard
  }, [finals, cenario])
```
  3. Onde hoje há `const articles = buildArticles(data, edits, isExcluded)`, acrescentar:
```javascript
  const skipEditIds = useMemo(() => new Set(Object.keys(edits)), [edits])
  const { articles: articlesFinais, appliedCount } = useMemo(
    () => applyFinalsToArticles(articles, finalsDoDoc, { skipEditIds }),
    [articles, finalsDoDoc, skipEditIds],
  )
```
  e renderizar a partir de `articlesFinais` (trocar o uso subsequente).
  4. No `buildMinutaBlob({ ... })`, acrescentar `finals: finalsDoDoc, skipEditIds`.
  5. UI: perto do topo do documento, badge quando `appliedCount > 0`: `<span className="section-bar-badge">{appliedCount} texto(s) final(is) aplicado(s)</span>`; quando `!user`: `<span className="wiz-finais-aviso">Entre no sistema para ver os textos finais aplicados.</span>` (classe nova no CSS: `.wiz-finais-aviso { font-size: .78rem; color: var(--text-muted); font-style: italic; }` — append em `src/index.css`).

- [ ] **Step 6: Rodar** — `node --test` e `npm run build` → verdes. **Step 7: Commit** — `git add src/lib/minutaFinals.js src/lib/minutaFinals.test.js src/lib/minutaDocx.js src/pages/MinutaWizard.jsx src/pages/RegulamentoWizard.jsx src/index.css && git commit -m "feat(finais): overlay de textos finais nos Wizards e no .docx (applyFinalsToArticles)"`

---

### Task 4: Conferência persistente

**Files:**
- Create: `src/lib/conferenciaData.js`
- Create: `src/lib/conferenciaStatus.js`
- Test: `src/lib/conferenciaStatus.test.js`
- Modify: `src/pages/ConferenciaLinear.jsx` (status por chave estável + persistência quando logado + aviso)

**Interfaces:**
- Consumes: `encodeFirestoreId`/`decodeFirestoreId` (T1); `useAuth`.
- Produces: `confKey(dispositivo) -> string`; `mergeStatus(localMap, remotoMap) -> Map(key→'ok'|'div')`; `divergentesDe(remotoMap, doc, cenario) -> [{key, status}]` (usada pela T5 no bloco de pendências); `subscribeConferencia(onChange, onError)`; `saveConferenciaStatus(key, status|null, autor)`.

- [ ] **Step 1: Teste que falha** — `src/lib/conferenciaStatus.test.js`:

```javascript
import { test } from 'node:test'
import assert from 'node:assert/strict'
import { confKey, mergeStatus, divergentesDe } from './conferenciaStatus.js'

test('confKey é estável por editId+número', () => {
  assert.equal(confKey({ editId: 'reg:tema-a/mt-art-1', number: 7 }), 'reg:tema-a/mt-art-1#art7')
})

test('mergeStatus: remoto vence o local', () => {
  const local = new Map([['a#art1', 'ok'], ['b#art2', 'div']])
  const remoto = new Map([['a#art1', { status: 'div' }]])
  const m = mergeStatus(local, remoto)
  assert.equal(m.get('a#art1'), 'div')
  assert.equal(m.get('b#art2'), 'div')
})

test('divergentesDe filtra por documento e cenário', () => {
  const remoto = new Map([
    ['reg:tema#art1', { status: 'div' }],           // reg, futura
    ['reg:atual:tema#art2', { status: 'div' }],     // reg, atual
    ['organ:cg/x#art3', { status: 'div' }],         // ri, futura
    ['reg:tema#art4', { status: 'ok' }],
  ])
  assert.equal(divergentesDe(remoto, 'reg', 'futura').length, 1)
  assert.equal(divergentesDe(remoto, 'reg', 'atual').length, 1)
  assert.equal(divergentesDe(remoto, 'ri', 'futura').length, 1)
})
```

- [ ] **Step 2: Ver falhar.** — [ ] **Step 3: Implementar `src/lib/conferenciaStatus.js`:**

```javascript
// Lógica pura da conferência persistente. A chave é estável enquanto a estrutura
// estiver congelada (mesma premissa do dispositivoId da Revisão).
import { docOfDispositivo, scenarioOfDispositivo } from './reviewGroup.js'

export function confKey(dispositivo) {
  return `${dispositivo.editId}#art${dispositivo.number}`
}

export function mergeStatus(localMap, remotoMap) {
  const m = new Map(localMap)
  remotoMap?.forEach((v, k) => { m.set(k, v.status) })
  return m
}

export function divergentesDe(remotoMap, docId, cenario) {
  const out = []
  remotoMap?.forEach((v, k) => {
    if (v.status !== 'div') return
    if (docOfDispositivo(k) !== docId) return
    if (scenarioOfDispositivo(k) !== cenario) return
    out.push({ key: k, status: v.status })
  })
  return out
}
```
(Se `docOfDispositivo`/`scenarioOfDispositivo` tiverem assinaturas de retorno diferentes de `'ri'|'reg'`/`'atual'|'futura'`, ADAPTE as chamadas ao contrato real de `reviewGroup.js` — leia o arquivo — mantendo os testes acima como comportamento.)

- [ ] **Step 4: Implementar `src/lib/conferenciaData.js`:**

```javascript
// Persistência do Confere/Divergente (coleção 'conferencia'), por membro logado.
import { collection, doc, onSnapshot, setDoc, deleteDoc, serverTimestamp } from 'firebase/firestore'
import { db } from './firebase.js'
import { encodeFirestoreId, decodeFirestoreId } from './dispositivoId.js'

const COL = 'conferencia'

export function subscribeConferencia(onChange, onError) {
  return onSnapshot(collection(db, COL),
    (snap) => {
      const map = new Map()
      snap.docs.forEach(d => map.set(decodeFirestoreId(d.id), d.data()))
      onChange(map)
    },
    (err) => { if (onError) onError(err) },
  )
}

export async function saveConferenciaStatus(key, status, autor) {
  const ref = doc(db, COL, encodeFirestoreId(key))
  if (status == null) { await deleteDoc(ref); return }
  await setDoc(ref, { status, por: autor.nome, em: serverTimestamp() })
}
```

- [ ] **Step 5: Integrar em `ConferenciaLinear.jsx`:** trocar o estado por índice (`status[i]`) por chave estável: `const [statusLocal, setStatusLocal] = useState(new Map())`; `const [remoto, setRemoto] = useState(null)`; assinar quando logado (`useAuth`): `useEffect(() => { if (!user) { setRemoto(null); return undefined } return subscribeConferencia(setRemoto, console.error) }, [user])`; `const statusMap = useMemo(() => mergeStatus(statusLocal, remoto), [statusLocal, remoto])`; item recebe `status={statusMap.get(confKey(item.dispositivo))}` e `onStatus` vira:

```javascript
const marcar = (item) => (v) => {
  const key = confKey(item.dispositivo)
  setStatusLocal(m => { const n = new Map(m); if (v == null) n.delete(key); else n.set(key, v); return n })
  if (user) saveConferenciaStatus(key, v, { nome: user.nome ?? user.email }).catch(e => console.error('Erro ao salvar conferência:', e))
}
```
Contador `feitos` passa a contar sobre `statusMap` restrito às chaves da lista atual. Quando `!user`, exibir na `section-bar`: `<span className="wiz-finais-aviso">Entre para salvar a conferência.</span>`.

- [ ] **Step 6: Rodar** — `node --test` e `npm run build`. **Step 7: Commit** — `git add src/lib/conferenciaData.js src/lib/conferenciaStatus.js src/lib/conferenciaStatus.test.js src/pages/ConferenciaLinear.jsx && git commit -m "feat(conferencia): Confere/Divergente persistente por membro logado (chave estável)"`

---

### Task 5: Registro na aba Decisões — modal, selos, pendências, "Como funciona"

**Files:**
- Create: `src/components/RegistroDecisaoModal.jsx`
- Modify: `src/pages/DecisoesCuradoria.jsx` (merge Firebase, selo 3 estados, botão registrar/desfazer, bloco pendências, link Como funciona, botão exportar — o handler de exportar vem na T6)
- Modify: `src/index.css` (append `.decm-*`)

**Interfaces:**
- Consumes: T2 (`subscribeDecisions`, `registrarDecisao`, `marcarFichaAplicada`, `desfazerDecisao`, `mergeDecisoes`, `pendenciasDeAplicacao`); T4 (`subscribeConferencia`, `divergentesDe`); `saveFinalText` (reviewData, já com encoding da T1); `buildConferencia` (`conferencia.js`); `useAuth`, `useScenario`, `scenarioDbUrl`, `caputDispositivoId`.
- Produces: aba completa da Fase 3 (a T6 só liga o handler de exportação).

**Regras exatas do modal:**
- Passo 1: tipo (`redacao`/`estrutural`, radio), textarea `decisao` (obrigatória), select `fonteEscolhida` (opções = `d.candidatas.map(c => c.fonte)` + `'Redação própria'`).
- Passo 2 redação: carrega a estrutura do cenário ativo (`fetchJson(scenarioDbUrl(cenario, ARQ[trilha]))`, `ARQ = { ri: 'minuta_structure.json', reg: 'regulamento_structure.json' }`), monta `buildConferencia(structure)` e filtra `item.chapterId` cujo `semCenario` (replicar: `id.replace(/^reg:atual:/, 'reg:').replace(/^atual:/, '')`) seja igual a `d.chapterId`; lista SÓ artigos cujo editId gera UM artigo (mesma regra da T3 — contar por editId; os demais aparecem desabilitados com nota "indisponível: artigo desdobrado de texto corrido"); radio por artigo com "Art. N — caput (primeiras ~90 chars)". Ao escolher, textarea "Texto final" pré-preenchida com o caput atual. Se NENHUM capítulo casa no cenário ativo: aviso "Este capítulo não existe no cenário ativo — troque o cenário para aplicar a redação." e o salvar fica desabilitado.
- Passo 2 estrutural: inputs `oQueMuda` e `onde` (texto livre, obrigatórios).
- Salvar (redação): 1º `registrarDecisao(d.id, { tipo, decisao, fonteEscolhida, alvoDispositivoId, ficha: null }, autor)`; 2º `saveFinalText(alvoDispositivoId, { texto, status: 'fechado', autor })`. Se o 2º falhar: manter modal aberto com erro "Decisão registrada, mas o texto final falhou: <msg>" + botão "Repetir gravação do texto final".
- Salvar (estrutural): `registrarDecisao(d.id, { tipo, decisao, fonteEscolhida, alvoDispositivoId: null, ficha: { oQueMuda, onde, status: 'aguardando' } }, autor)`.
- `alvoDispositivoId = caputDispositivoId(editIdEscolhido)` — o editId vem do artigo escolhido, JÁ com o marcador de cenário embutido (estrutura do cenário ativo). Nenhum de-para automático.

- [ ] **Step 1: Escrever `src/components/RegistroDecisaoModal.jsx`** (componente completo):

```jsx
import { useEffect, useMemo, useState } from 'react'
import { X } from 'lucide-react'
import { fetchJson } from '../lib/dataCache.js'
import { scenarioDbUrl } from '../lib/scenario.js'
import { buildConferencia } from '../lib/conferencia.js'
import { caputDispositivoId } from '../lib/dispositivoId.js'
import { registrarDecisao } from '../lib/decisionsData.js'
import { saveFinalText } from '../lib/reviewData.js'

const ARQ = { ri: 'minuta_structure.json', reg: 'regulamento_structure.json' }
const semCenario = (id) => String(id ?? '').replace(/^reg:atual:/, 'reg:').replace(/^atual:/, '')

export default function RegistroDecisaoModal({ decisao: d, trilha, cenario, autor, onClose, onSaved }) {
  const [tipo, setTipo] = useState('redacao')
  const [texto, setTexto] = useState('')
  const [fonte, setFonte] = useState('Redação própria')
  const [oQueMuda, setOQueMuda] = useState('')
  const [onde, setOnde] = useState('')
  const [alvo, setAlvo] = useState(null)          // { editId, label, caput }
  const [textoFinal, setTextoFinal] = useState('')
  const [struct, setStruct] = useState(null)
  const [erro, setErro] = useState(null)
  const [salvando, setSalvando] = useState(false)
  const [decisaoGravada, setDecisaoGravada] = useState(false) // p/ repetir só o finalText

  useEffect(() => {
    fetchJson(scenarioDbUrl(cenario, ARQ[trilha])).then(setStruct).catch(() => setStruct(null))
  }, [cenario, trilha])

  const artigos = useMemo(() => {
    if (!struct) return []
    const lista = buildConferencia(struct).filter(it => semCenario(it.chapterId) === d.chapterId)
    const porEditId = new Map()
    lista.forEach(it => porEditId.set(it.dispositivo.editId, (porEditId.get(it.dispositivo.editId) ?? 0) + 1))
    return lista.map(it => ({
      editId: it.dispositivo.editId,
      number: it.dispositivo.number,
      caput: it.dispositivo.caput,
      elegivel: porEditId.get(it.dispositivo.editId) === 1,
    }))
  }, [struct, d.chapterId])

  const escolher = (a) => { setAlvo(a); setTextoFinal(a.caput) }

  const podeSalvar = texto.trim() && !salvando && (
    tipo === 'estrutural' ? (oQueMuda.trim() && onde.trim()) : (alvo && textoFinal.trim()))

  const gravarFinal = async () => {
    await saveFinalText(caputDispositivoId(alvo.editId), { texto: textoFinal, status: 'fechado', autor })
  }

  const salvar = async () => {
    setSalvando(true); setErro(null)
    try {
      if (!decisaoGravada) {
        await registrarDecisao(d.id, {
          tipo, decisao: texto.trim(), fonteEscolhida: fonte,
          alvoDispositivoId: tipo === 'redacao' ? caputDispositivoId(alvo.editId) : null,
          ficha: tipo === 'estrutural' ? { oQueMuda: oQueMuda.trim(), onde: onde.trim(), status: 'aguardando' } : null,
        }, autor)
        setDecisaoGravada(true)
      }
      if (tipo === 'redacao') await gravarFinal()
      onSaved()
    } catch (e) {
      setErro(decisaoGravada
        ? `Decisão registrada, mas o texto final falhou: ${e.message}`
        : `Falha ao registrar: ${e.message}`)
    } finally { setSalvando(false) }
  }

  return (
    <div className="decm-overlay" role="dialog" aria-modal="true">
      <div className="decm card">
        <div className="decm-head">
          <h3>Registrar decisão</h3>
          <button className="btn btn-ghost" onClick={onClose}><X size={16} /></button>
        </div>
        <p className="dec-questao">{d.titulo}</p>

        <div className="decm-field">
          <label>Tipo</label>
          <label><input type="radio" checked={tipo === 'redacao'} onChange={() => setTipo('redacao')} /> Redação (muda o texto de um artigo)</label>
          <label><input type="radio" checked={tipo === 'estrutural'} onChange={() => setTipo('estrutural')} /> Estrutural (muda a estrutura — gera ficha de aplicação)</label>
        </div>

        <div className="decm-field">
          <label>Decisão (o que ficou decidido e por quê)</label>
          <textarea rows={4} value={texto} onChange={e => setTexto(e.target.value)} />
        </div>

        <div className="decm-field">
          <label>Fonte escolhida</label>
          <select value={fonte} onChange={e => setFonte(e.target.value)}>
            {[...d.candidatas.map(c => c.fonte), 'Redação própria'].map(f => <option key={f} value={f}>{f}</option>)}
          </select>
        </div>

        {tipo === 'redacao' && (
          <div className="decm-field">
            <label>Artigo alvo (cenário ativo: {cenario})</label>
            {artigos.length === 0 && (
              <p className="rg-empty">Este capítulo não existe no cenário ativo — troque o cenário para aplicar a redação.</p>
            )}
            <div className="decm-artigos">
              {artigos.map(a => (
                <label key={`${a.editId}#${a.number}`} className={a.elegivel ? '' : 'decm-inelegivel'}>
                  <input type="radio" disabled={!a.elegivel} checked={alvo?.editId === a.editId}
                    onChange={() => escolher(a)} />
                  {' '}Art. {a.number} — {String(a.caput).slice(0, 90)}
                  {!a.elegivel && <em> (indisponível: artigo desdobrado de texto corrido)</em>}
                </label>
              ))}
            </div>
            {alvo && (
              <>
                <label>Texto final do artigo</label>
                <textarea rows={4} value={textoFinal} onChange={e => setTextoFinal(e.target.value)} />
              </>
            )}
          </div>
        )}

        {tipo === 'estrutural' && (
          <div className="decm-field">
            <label>O que muda</label>
            <textarea rows={2} value={oQueMuda} onChange={e => setOQueMuda(e.target.value)} />
            <label>Onde (órgãos/temas/arquivos envolvidos)</label>
            <input type="text" value={onde} onChange={e => setOnde(e.target.value)} />
          </div>
        )}

        {erro && (
          <div className="decm-erro">
            {erro}
            {decisaoGravada && tipo === 'redacao' && (
              <button className="btn btn-ghost" onClick={salvar}>Repetir gravação do texto final</button>
            )}
          </div>
        )}

        <div className="decm-acoes">
          <button className="btn btn-ghost" onClick={onClose}>Cancelar</button>
          <button className="btn" disabled={!podeSalvar} onClick={salvar}>
            {salvando ? 'Salvando…' : 'Registrar decisão'}
          </button>
        </div>
      </div>
    </div>
  )
}
```

- [ ] **Step 2: CSS** — append em `src/index.css`:

```css
/* ===== Modal de registro de decisão (cockpit Fase 3) ===== */
.decm-overlay { position: fixed; inset: 0; background: rgba(15,23,42,.45); display: flex; align-items: center; justify-content: center; z-index: 80; padding: 16px; }
.decm { width: min(720px, 100%); max-height: 90vh; overflow-y: auto; padding: 20px; }
.decm-head { display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px; }
.decm-field { display: flex; flex-direction: column; gap: 6px; margin: 12px 0; }
.decm-field textarea, .decm-field input[type="text"], .decm-field select { font: inherit; padding: 8px; border: 1px solid var(--border, #e2e6ee); border-radius: 8px; }
.decm-artigos { display: flex; flex-direction: column; gap: 6px; max-height: 200px; overflow-y: auto; border: 1px solid var(--border, #e2e6ee); border-radius: 8px; padding: 10px; }
.decm-inelegivel { color: var(--text-muted); }
.decm-erro { background: #fdecea; color: #b3261e; border-radius: 8px; padding: 10px; margin: 10px 0; display: flex; flex-direction: column; gap: 8px; }
.decm-acoes { display: flex; justify-content: flex-end; gap: 8px; margin-top: 12px; }
.dec-selo-sys { background: #d9f0e2; color: #0c6b35; }
.dec-pendencias { margin-bottom: 14px; }
```

- [ ] **Step 3: Integrar em `DecisoesCuradoria.jsx`:**
  1. Imports novos: `useAuth`; `subscribeDecisions, desfazerDecisao, marcarFichaAplicada` (decisionsData); `mergeDecisoes, pendenciasDeAplicacao` (decisionsMerge); `subscribeConferencia` (conferenciaData); `divergentesDe` (conferenciaStatus); `useScenario`; `RegistroDecisaoModal`; ícone `BookOpen` (link Como funciona) e `Download` (T6).
  2. Estado/efeitos: `const { user } = useAuth()`; `const { cenario } = useScenario()`; `fbDecisoes`/`conf` assinados só com `user` (mesmo padrão da T3/T4); `const isAdmin = user?.role === 'admin'`; `const [registrando, setRegistrando] = useState(null)`.
  3. `const daTrilha = ...` passa a: `const merged = useMemo(() => mergeDecisoes(decisoesDaTrilha(dados, trilha), fbDecisoes), [dados, trilha, fbDecisoes])` e filtro/contagem sobre `merged` — **contarDecisoes/filtrarDecisoes continuam funcionando** porque decidem por `d.decidido`; ATUALIZE a semântica: passar a decidir por `d.statusDecisao !== 'pendente'`. Faça isso SEM quebrar a lib da Fase 2: adicione em `src/lib/decisoes.js` um segundo parâmetro opcional `pred = (d) => d.decidido` OU (mais simples e explícito) ajuste `filtrarDecisoes`/`contarDecisoes` para usar `d.statusDecisao ? d.statusDecisao !== 'pendente' : d.decidido` — e ATUALIZE `src/lib/decisoes.test.js` cobrindo os dois formatos (com e sem `statusDecisao`).
  4. Selo no `DecisaoCard`: 3 estados — `statusDecisao === 'sistema'` → `<span className="dec-selo dec-selo-sys"><Check size={13}/> Decidida no sistema</span>`; `'vault'` → selo atual "Decidida"→ renomear rótulo para "Decidida no vault"; `'pendente'` → Pendente (como hoje). Quando `'sistema'`, mostrar o registro (`registro.decisao`, `registro.fonteEscolhida`, `registro.tipo`, e a ficha quando estrutural) no bloco `dec-decisao`.
  5. Botões admin no card: pendente/vault → "Registrar decisão" (`setRegistrando(d)`); sistema → "Desfazer" com `window.confirm('Desfazer o registro? O texto final aplicado (se houver) permanece e pode ser revisto pela Revisão.')` → `desfazerDecisao(d.id)`.
  6. Bloco "Pendências de aplicação" (acima da lista, `className="card dec-pendencias"`, recolhível como as candidatas): fichas de `pendenciasDeAplicacao(merged)` (com botão admin "Marcar aplicada" → `marcarFichaAplicada(d.id)`) + divergentes de `divergentesDe(conf, trilha, cenario)` (linha por chave: `Divergente — {key}`). Vazio → não renderiza o bloco.
  7. Topo: link `<Link to="/manual#cockpit" className="btn btn-ghost"><BookOpen size={15}/> Como funciona</Link>`; botão Exportar (`Download`) já presente mas com handler `null` até a T6 (renderizar SÓ se `isAdmin`; se handler ausente, não renderizar ainda — deixe comentário `{/* Exportar: ligado na task de exportação */}`).
  8. Modal: `{registrando && <RegistroDecisaoModal decisao={registrando} trilha={trilha} cenario={cenario} autor={{ nome: user?.nome ?? user?.email }} onClose={() => setRegistrando(null)} onSaved={() => setRegistrando(null)} />}`.

- [ ] **Step 4: Rodar** — `node --test` (com os testes de `decisoes.test.js` atualizados) e `npm run build`. **Step 5: Commit** — `git add src/components/RegistroDecisaoModal.jsx src/pages/DecisoesCuradoria.jsx src/lib/decisoes.js src/lib/decisoes.test.js src/index.css && git commit -m "feat(decisoes): registro pelo sistema (modal admin), selos 3 estados, pendências de aplicação"`

---

### Task 6: Exportação + script de retorno ao vault

**Files:**
- Modify: `src/pages/DecisoesCuradoria.jsx` (handler do botão Exportar)
- Create: `scripts/aplicar_decisoes_vault.py`
- Test: `scripts/test_aplicar_decisoes_vault.py`

**Interfaces:**
- Consumes: `merged` (T5) — decisões com `statusDecisao === 'sistema'`.
- Produces: arquivo `decisoes_export.json` baixado: `[{ id, tipo, decisao, fonteEscolhida, alvoDispositivoId, registradoPor, registradoEm }]`; script que escreve `## Decisão CBMRO` + `decidido: true` nas notas.

- [ ] **Step 1: Handler de exportação** em `DecisoesCuradoria.jsx` (e renderizar o botão admin `Download` "Exportar decisões" ao lado do link Como funciona):

```javascript
const exportar = () => {
  const registradas = merged.filter(d => d.statusDecisao === 'sistema')
  if (registradas.length === 0) { window.alert('Nenhuma decisão registrada no sistema para exportar.'); return }
  const payload = registradas.map(d => ({
    id: d.id, tipo: d.registro.tipo, decisao: d.registro.decisao,
    fonteEscolhida: d.registro.fonteEscolhida ?? null,
    alvoDispositivoId: d.registro.alvoDispositivoId ?? null,
    registradoPor: d.registro.registradoPor ?? null,
    registradoEm: d.registro.registradoEm?.toDate?.()?.toISOString() ?? null,
  }))
  const blob = new Blob([JSON.stringify(payload, null, 2)], { type: 'application/json' })
  const a = document.createElement('a')
  a.href = URL.createObjectURL(blob)
  a.download = 'decisoes_export.json'
  a.click()
  URL.revokeObjectURL(a.href)
}
```
Nota: exporta as decisões da TRILHA ativa? NÃO — exporta TODAS as registradas (as duas trilhas), porque o script aplica no vault inteiro de uma vez. Use `mergeDecisoes(dados?.decisoes ?? [], fbDecisoes)` (sem filtro de trilha) dentro do handler.

- [ ] **Step 2: Teste Python que falha** — `scripts/test_aplicar_decisoes_vault.py`:

```python
import json
import tempfile
import unittest
from pathlib import Path
from aplicar_decisoes_vault import aplicar

NOTA = """---
tags: [cbmro, curadoria, decisao]
type: decisao
themeKey: servico-operacional
decidido: false
---
# Decisão — servico-operacional — folga

**Questão:** Quanto de folga?

## Decisão CBMRO
_(a preencher pelo Wândrio — redação escolhida e o porquê)_

## Ligações
[[Tema — servico-operacional]]
"""

EXPORT = [{
    "id": "Decisão — servico-operacional — folga",
    "tipo": "redacao", "decisao": "Adotar 12h/36h (critério de exclusividade de AL).",
    "fonteEscolhida": "Alagoas", "alvoDispositivoId": "reg:servico-operacional/x#caput",
    "registradoPor": "Wândrio", "registradoEm": "2026-07-23T12:00:00Z",
}]


class TestAplicar(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.vault = Path(self.tmp.name)
        (self.vault / "Regulamento — Curadoria").mkdir()
        (self.vault / "Regimento Interno — Curadoria").mkdir()
        self.nota = self.vault / "Regulamento — Curadoria" / "Decisão — servico-operacional — folga.md"
        self.nota.write_text(NOTA, encoding="utf-8")
        self.export = self.vault / "decisoes_export.json"
        self.export.write_text(json.dumps(EXPORT), encoding="utf-8")

    def tearDown(self):
        self.tmp.cleanup()

    def test_aplica_e_marca_decidido(self):
        r = aplicar(self.export, self.vault)
        self.assertEqual(r["aplicadas"], 1)
        txt = self.nota.read_text(encoding="utf-8")
        self.assertIn("decidido: true", txt)
        self.assertIn("Adotar 12h/36h", txt)
        self.assertIn("_Registrado no sistema por Wândrio", txt)
        self.assertNotIn("_(a preencher", txt)

    def test_idempotente(self):
        aplicar(self.export, self.vault)
        r2 = aplicar(self.export, self.vault)
        self.assertEqual(r2["aplicadas"], 0)
        self.assertEqual(r2["ja_aplicadas"], 1)
        self.assertEqual(self.nota.read_text(encoding="utf-8").count("_Registrado no sistema"), 1)

    def test_conflito_nao_sobrescreve(self):
        self.nota.write_text(NOTA.replace(
            "_(a preencher pelo Wândrio — redação escolhida e o porquê)_",
            "Decisão manual DIFERENTE tomada no papel."), encoding="utf-8")
        r = aplicar(self.export, self.vault)
        self.assertEqual(r["conflitos"], 1)
        self.assertIn("Decisão manual DIFERENTE", self.nota.read_text(encoding="utf-8"))

    def test_nota_ausente(self):
        self.nota.unlink()
        r = aplicar(self.export, self.vault)
        self.assertEqual(r["nao_encontradas"], 1)


if __name__ == "__main__":
    unittest.main()
```

- [ ] **Step 3: Ver falhar** — `cd scripts && ../.venv-pipeline/bin/python -m unittest test_aplicar_decisoes_vault -v` → erro de import.

- [ ] **Step 4: Implementar `scripts/aplicar_decisoes_vault.py`:**

```python
"""
aplicar_decisoes_vault.py — Portal CBM (cockpit Fase 3)

Aplica no vault Obsidian as decisões registradas no sistema (decisoes_export.json,
baixado da aba Decisões). Preenche '## Decisão CBMRO' + 'decidido: true'.
Regras duras: conflito com decisão manual divergente NÃO sobrescreve (reporta);
idempotente; nota ausente reporta; qualquer anomalia => saída != 0.

Rodar: .venv-pipeline/bin/python scripts/aplicar_decisoes_vault.py <export.json> [--vault <dir>]
"""
import json
import os
import re
import sys
from pathlib import Path

DEFAULT_VAULT = Path.home() / "Documents" / "Obsidian Vault" / "Codebases" / "Comparativo-de-cargos-e-funcoes"
SUBPASTAS = ["Regimento Interno — Curadoria", "Regulamento — Curadoria"]
SECAO_RE = re.compile(r"(## Decisão CBMRO\n)(.*?)(?=\n## |\Z)", re.DOTALL)


def _eh_placeholder(txt):
    t = txt.strip()
    return not t or t.startswith("_(") or t.startswith("<!--")


def _rodape(dec):
    quem = dec.get("registradoPor") or "sistema"
    quando = (dec.get("registradoEm") or "")[:10] or "data não informada"
    return f"_Registrado no sistema por {quem} em {quando}._"


def aplicar(export_path, vault):
    export = json.loads(Path(export_path).read_text(encoding="utf-8"))
    r = {"aplicadas": 0, "ja_aplicadas": 0, "conflitos": 0, "nao_encontradas": 0, "detalhes": []}
    for dec in export:
        nota = None
        for sub in SUBPASTAS:
            p = Path(vault) / sub / f"{dec['id']}.md"
            if p.exists():
                nota = p
                break
        if nota is None:
            r["nao_encontradas"] += 1
            r["detalhes"].append(f"NÃO ENCONTRADA: {dec['id']}")
            continue
        txt = nota.read_text(encoding="utf-8")
        m = SECAO_RE.search(txt)
        atual = m.group(2) if m else ""
        novo_corpo = f"{dec['decisao'].strip()}\n\n{_rodape(dec)}\n"
        if not _eh_placeholder(atual):
            if dec["decisao"].strip() in atual:
                r["ja_aplicadas"] += 1
                continue
            r["conflitos"] += 1
            r["detalhes"].append(f"CONFLITO (decisão manual divergente): {dec['id']}")
            continue
        if m:
            txt = SECAO_RE.sub(lambda mm: mm.group(1) + novo_corpo, txt, count=1)
        else:
            txt = txt.rstrip() + f"\n\n## Decisão CBMRO\n{novo_corpo}"
        txt = re.sub(r"^decidido: false$", "decidido: true", txt, count=1, flags=re.MULTILINE)
        nota.write_text(txt, encoding="utf-8")
        r["aplicadas"] += 1
    return r


def main():
    if len(sys.argv) < 2:
        sys.exit("Uso: aplicar_decisoes_vault.py <decisoes_export.json> [--vault <dir>]")
    export_path = sys.argv[1]
    vault = Path(os.environ.get("VAULT_CURADORIA", str(DEFAULT_VAULT)))
    if "--vault" in sys.argv:
        vault = Path(sys.argv[sys.argv.index("--vault") + 1])
    if not vault.is_dir():
        sys.exit(f"ERRO: vault não encontrado em {vault} (defina VAULT_CURADORIA ou use --vault).")
    r = aplicar(export_path, vault)
    print(f"Aplicadas: {r['aplicadas']} · Já aplicadas: {r['ja_aplicadas']} · "
          f"Conflitos: {r['conflitos']} · Não encontradas: {r['nao_encontradas']}")
    for d in r["detalhes"]:
        print(" -", d)
    if r["conflitos"] or r["nao_encontradas"]:
        sys.exit(1)


if __name__ == "__main__":
    main()
```

- [ ] **Step 5: Rodar testes** — `cd scripts && ../.venv-pipeline/bin/python -m unittest test_aplicar_decisoes_vault -v` → 4/4. `npm run build` ok.
- [ ] **Step 6: Commit** — `git add scripts/aplicar_decisoes_vault.py scripts/test_aplicar_decisoes_vault.py src/pages/DecisoesCuradoria.jsx && git commit -m "feat(decisoes): exportação JSON + script que devolve decisões ao vault (conflito reporta, idempotente)"`

---

### Task 7: Guia da metodologia no Manual (orientação para o Tiago) + docs

**Files:**
- Modify: `src/pages/Manual.jsx` (nova entrada no array `SECTIONS`, id `cockpit`)
- Modify: `CLAUDE.md` (parágrafo curto na seção do cockpit)

- [ ] **Step 1: Seção no Manual** — append ao array `SECTIONS` (mesmo formato dos itens existentes: `{ id, title, body: <>...</> }`):

```jsx
  {
    id: 'cockpit', title: 'Cockpit de curadoria — como decidir',
    body: (
      <>
        <p>
          O <b>cockpit de curadoria</b> é o conjunto de telas onde as minutas são conferidas e
          as <b>Decisões CBMRO</b> são analisadas e registradas. Quem analisa as decisões deve
          seguir esta dinâmica:
        </p>
        <p>
          <b>1. Conferência</b> (menu de cada trilha): percorra a minuta artigo por artigo, com as
          referências dos outros estados ao lado. Marque <b>Confere</b> ou <b>Divergente</b> —
          logado, a marcação fica salva para todos; o Divergente vira pendência na aba Decisões.
        </p>
        <p>
          <b>2. Decisões</b> (menu de cada trilha): cada cartão traz a <b>Questão</b> (o que precisa
          ser decidido), as <b>redações candidatas</b> (texto literal das leis de outros estados,
          com a leitura do curador) e a <b>Comparação</b>. Os selos: <b>Pendente</b> (ninguém
          decidiu), <b>Decidida no vault</b> (decisão anotada no acervo de estudo) e
          <b> Decidida no sistema</b> (registrada aqui — é a que vale).
        </p>
        <p>
          <b>3. Registrar</b> (botão visível para o papel administrador): escolha o tipo —
          <b> Redação</b> (você aponta o artigo alvo e escreve o texto final; ele passa a aparecer
          na Minuta e no arquivo .docx baixado, com o aviso de quantos textos finais estão
          aplicados) ou <b>Estrutural</b> (muda a organização — fusão de órgãos, subordinação;
          gera uma <b>ficha de aplicação</b> que fica pendente até ser aplicada em sessão de
          trabalho). Registre sempre o <b>porquê</b> da decisão.
        </p>
        <p>
          <b>4. Retorno ao acervo</b>: o administrador exporta as decisões registradas
          (botão <b>Exportar decisões</b>) e um passo local atualiza as notas de estudo no
          Obsidian — nada se perde e o histórico fica completo.
        </p>
        <div className="manual-callout">
          <b>Regra de ouro:</b> decida <b>lendo o conteúdo</b> das candidatas, nunca pela
          semelhança de nomes de órgãos ou temas — órgãos com nomes parecidos podem tratar de
          matérias completamente diferentes.
        </div>
      </>
    ),
  },
```

- [ ] **Step 2: CLAUDE.md** — na seção do cockpit (Conferência linear), acrescentar parágrafo curto:

```markdown
**Fase 3 (registrar/aplicar, 2026-07-23):** decisões registradas pelo sistema na coleção
`decisions` (admin), com `finalText` no dispositivo alvo (redação, cenário ativo, alvo
apontado manualmente — nunca de-para automático) ou ficha de aplicação (estrutural);
Conferência persiste em `conferencia` (membro logado); overlay `applyFinalsToArticles`
(`src/lib/minutaFinals.js`) aplica textos finais nos 2 Wizards e no .docx (logado);
`encodeFirestoreId` (dispositivoId.js) na fronteira Firestore (editId tem `/`);
exportar decisões (aba Decisões, admin) + `scripts/aplicar_decisoes_vault.py` devolve ao
vault (conflito reporta, idempotente). Guia p/ analista: Manual seção `#cockpit`.
```

- [ ] **Step 3: Rodar** — `npm run build && node --test` → verdes. **Step 4: Commit** — `git add src/pages/Manual.jsx CLAUDE.md && git commit -m "docs(cockpit): guia da metodologia no Manual (analista) + CLAUDE.md Fase 3"`

---

## Prova real (após as 7 tasks — regra do crachá; feita pelo coordenador, não por subagente)

1. `npm run dev` + Playwright logado (o Wândrio loga uma vez): registrar decisão de redação de teste → ver o selo "Decidida no sistema", o texto no Wizard (badge "1 texto final aplicado") e no .docx baixado; registrar estrutural → ficha em Pendências; marcar Divergente na Conferência → recarregar → persiste e aparece em Pendências; screenshots colados.
2. Exportar → rodar `aplicar_decisoes_vault.py --vault <vault-de-teste>` (cópia) → nota preenchida; rodar 2ª vez → idempotente.
3. Preservação: diff mostra Revisão/Subsídio intocados; desfazer a decisão de teste ao final (e remover o finalText de teste via console/Firestore se necessário — relatar o que ficou).
4. Lembrar o Wândrio: publicar `firestore.rules` no console (docs/FIREBASE_SETUP.md).

## Auditoria AR-01 (fechar a fase)

Reexecutar as 3 varreduras do catálogo + a nova: confirmar por leitura de código que NENHUM caminho faz casamento automático de dispositivo entre cenários ou por semelhança de nome (o alvo é sempre apontado manualmente no modal; `divergentesDe` filtra por marcador, não por nome).

## Self-Review (feito)

- **Cobertura da spec:** C1→T2, C2→T5, C3→T3, C4→T4, C5→T6, C6→T7, risco do encoding→T1. ✓
- **Placeholders:** nenhum; todo passo de código tem código.
- **Consistência:** `encodeFirestoreId/decodeFirestoreId` (T1) usados em T2/T4; `applyFinalsToArticles(articles, finalsMap, {skipEditIds})` idêntico em T3 (lib, docx, wizards); `mergeDecisoes/pendenciasDeAplicacao` (T2) consumidos em T5/T6; `confKey/mergeStatus/divergentesDe` (T4) consumidos em T4/T5; campos do doc `decisions` (T2) idênticos aos gravados no modal (T5) e exportados (T6). ✓
