# Comissão Comenta o Regulamento (Bloco C, fatia 1) — Plano de Implementação

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Estender a página `/revisao` (Firebase) para que a comissão comente também a
minuta do **Regulamento** (`database/regulamento_structure.json`), isolada dos comentários
do **RI** (`database/minuta_structure.json`), com um seletor de documento no topo e um
interruptor de admin que controla quando o Regulamento fica aberto para comentários.

**Architecture:** O prefixo `reg:` já presente em todo `editId` do Regulamento (gerado no
Bloco B2) serve, sozinho, de etiqueta de documento — nenhum campo novo, nenhuma migração.
Um novo documento único `config/revisao` no Firestore guarda o interruptor
`regulamentoAberto`; a UI filtra `suggestions`/`finalTexts` client-side pelo prefixo do
`dispositivoId`. Todo o resto do fluxo (balão por dispositivo, modal de sugestão, curtida,
texto final do admin) é reusado sem alteração.

**Tech Stack:** React 18 + Vite, Firebase (Auth + Firestore, SDK client-side via
`onSnapshot`), `node --test` para testes de lógica pura.

## Global Constraints

- Nenhum arquivo novo "pesado" (componente/página) — só extensão de arquivos existentes
  (design §4).
- Nenhuma migração de dados no Firestore: comentários já gravados no RI continuam válidos
  sem alteração (design §3, §4).
- `editId` do RI nunca pode começar com `reg:` — é a premissa que garante a separação;
  deve ficar documentada, não só implícita (design §10, risco 1).
- Ausência do doc `config/revisao` deve ser tratada como `regulamentoAberto: false`
  (fail-closed) — nunca abrir por omissão (design §5, §10, risco 2).
- Participante comum nunca vê o Regulamento como comentável enquanto o interruptor
  estiver desligado; o admin sempre vê e pode testar (design §2, §4).
- Reusar classes/padrões visuais existentes (`.oc-state-chip`, `.btn.btn-ghost`,
  `EmptyState`) — no máximo 1-2 classes CSS novas (design §7).
- Sem contas de teste no Firebase de produção `revisao-minuta-cbmro-6f248` — verificação
  ponta a ponta com login real fica com o Wândrio, como nas fatias anteriores.

---

### Task 1: Helpers puros de separação por documento (`reviewGroup.js`)

**Files:**
- Modify: `src/lib/reviewGroup.js`
- Test: `src/lib/reviewGroup.test.js`

**Interfaces:**
- Consumes: nada de novo (função pura sobre strings/arrays/Map já usados no arquivo).
- Produces:
  - `docOfDispositivo(dispositivoId: string): 'ri' | 'reg'`
  - `filterSuggestionsByDoc(suggestions: Array<{dispositivoId: string, ...}>, docId: 'ri'|'reg'): Array<...>`
  - `filterFinalsByDoc(finals: Map<string, object>, docId: 'ri'|'reg'): Map<string, object>`
  — usadas pela Task 4 (`Revisao.jsx`) para filtrar `suggestions`/`finals` antes de
  `groupByDispositivo`/`countByDispositivo`/`countByChapter`.

- [ ] **Step 1: Escrever os testes que falham**

Em `src/lib/reviewGroup.test.js` (arquivo já existe), primeiro TROQUE o import existente
do topo:

```js
import { groupByDispositivo, countByDispositivo, countByChapter } from './reviewGroup.js'
```

por:

```js
import {
  groupByDispositivo, countByDispositivo, countByChapter,
  docOfDispositivo, filterSuggestionsByDoc, filterFinalsByDoc,
} from './reviewGroup.js'
```

Depois acrescente estes testes ao final do arquivo (sem remover os atuais):

```js
test('docOfDispositivo reconhece prefixo reg: do Regulamento', () => {
  assert.equal(docOfDispositivo('reg:disposicoes-preliminares/mt-art-1#0'), 'reg')
})

test('docOfDispositivo trata qualquer editId sem prefixo reg: como RI', () => {
  assert.equal(docOfDispositivo('organ:cg/competencia#0'), 'ri')
  assert.equal(docOfDispositivo('estrutura#caput'), 'ri')
})

test('filterSuggestionsByDoc separa sugestões do RI e do Regulamento', () => {
  const suggestions = [
    { id: 'a', dispositivoId: 'organ:cg/competencia#0' },
    { id: 'b', dispositivoId: 'reg:disposicoes-preliminares/mt-art-1#0' },
    { id: 'c', dispositivoId: 'estrutura#caput' },
  ]
  const ri = filterSuggestionsByDoc(suggestions, 'ri')
  const reg = filterSuggestionsByDoc(suggestions, 'reg')
  assert.deepEqual(ri.map(s => s.id), ['a', 'c'])
  assert.deepEqual(reg.map(s => s.id), ['b'])
})

test('filterFinalsByDoc separa o Map de textos finais por documento', () => {
  const finals = new Map([
    ['organ:cg/competencia#0', { status: 'fechado' }],
    ['reg:disposicoes-preliminares/mt-art-1#0', { status: 'em_aberto' }],
  ])
  const ri = filterFinalsByDoc(finals, 'ri')
  const reg = filterFinalsByDoc(finals, 'reg')
  assert.equal(ri.size, 1)
  assert.equal(ri.get('organ:cg/competencia#0').status, 'fechado')
  assert.equal(reg.size, 1)
  assert.equal(reg.get('reg:disposicoes-preliminares/mt-art-1#0').status, 'em_aberto')
})

test('filterSuggestionsByDoc/filterFinalsByDoc com listas vazias devolvem vazio', () => {
  assert.deepEqual(filterSuggestionsByDoc([], 'ri'), [])
  assert.equal(filterFinalsByDoc(new Map(), 'reg').size, 0)
})
```

- [ ] **Step 2: Rodar os testes e confirmar que falham**

Run: `node --test src/lib/reviewGroup.test.js`
Expected: FAIL — `docOfDispositivo is not a function` (ou erro de import equivalente).

- [ ] **Step 3: Implementar as três funções**

No topo de `src/lib/reviewGroup.js`, antes de `groupByDispositivo`, acrescente:

```js
// Etiqueta de documento embutida no próprio editId: todo dispositivo do Regulamento
// nasce com prefixo "reg:" (Bloco B2); RI nunca usa esse prefixo. Sem campo novo,
// sem migração — ver docs/superpowers/specs/2026-07-07-comissao-comenta-regulamento-design.md.
export function docOfDispositivo(dispositivoId) {
  return String(dispositivoId).startsWith('reg:') ? 'reg' : 'ri'
}

export function filterSuggestionsByDoc(suggestions, docId) {
  return suggestions.filter(s => docOfDispositivo(s.dispositivoId) === docId)
}

export function filterFinalsByDoc(finals, docId) {
  const map = new Map()
  finals.forEach((v, k) => { if (docOfDispositivo(k) === docId) map.set(k, v) })
  return map
}
```

- [ ] **Step 4: Rodar os testes e confirmar que passam**

Run: `node --test src/lib/reviewGroup.test.js`
Expected: PASS — todos os testes (os antigos + os 5 novos).

- [ ] **Step 5: Commit**

```bash
cd "/Users/wandriobandeira/Projetos de dev Sistemas/Comparativo-de-cargos-e-funcoes"
git add src/lib/reviewGroup.js src/lib/reviewGroup.test.js
git commit -m "$(cat <<'EOF'
feat(revisao): separar sugestões/finais por documento via prefixo reg:

Helpers puros (docOfDispositivo/filterSuggestionsByDoc/filterFinalsByDoc)
usam o prefixo reg: já presente nos editIds do Regulamento (Bloco B2)
para isolar RI e Regulamento sem precisar de campo novo nem migração.
EOF
)"
```

---

### Task 2: Interruptor de admin no Firestore (`reviewData.js`)

**Files:**
- Modify: `src/lib/reviewData.js`

**Interfaces:**
- Consumes: `db` de `src/lib/firebase.js` (já importado no arquivo); `doc`, `onSnapshot`,
  `setDoc` de `firebase/firestore` (já importados no arquivo).
- Produces:
  - `subscribeRevisaoConfig(onChange: (cfg: {regulamentoAberto: boolean}) => void, onError?: (e) => void): () => void`
    — mesmo padrão de `subscribeFinalTexts`/`subscribeSuggestions` (retorna o
    `unsubscribe` do `onSnapshot`); usada pela Task 4.
  - `setRegulamentoAberto(aberto: boolean): Promise<void>` — usada pela Task 4 (botão do
    admin).

Não há teste automatizado aqui (o arquivo `reviewData.js` já não tem
`reviewData.test.js` hoje — é uma camada fina sobre o SDK do Firebase, sem lógica pura
para isolar; o padrão do projeto é verificar manualmente, como no A1/A8.7). A
verificação manual está descrita no Step 3.

- [ ] **Step 1: Acrescentar a constante do documento de config**

Em `src/lib/reviewData.js`, logo abaixo de `const COL_FINAL = 'finalTexts'` (linha 9),
adicione:

```js
const DOC_CONFIG = doc(db, 'config', 'revisao')
```

- [ ] **Step 2: Acrescentar as duas funções**

No final do arquivo (depois de `saveFinalText`), adicione:

```js
// Ausência do doc == regulamentoAberto:false (fail-closed) — nunca abrir por omissão.
export function subscribeRevisaoConfig(onChange, onError) {
  return onSnapshot(DOC_CONFIG,
    (snap) => onChange(snap.exists() ? snap.data() : { regulamentoAberto: false }),
    (err) => { if (onError) onError(err) },
  )
}

export async function setRegulamentoAberto(aberto) {
  await setDoc(DOC_CONFIG, { regulamentoAberto: aberto }, { merge: true })
}
```

- [ ] **Step 3: Endurecer `addSuggestion` — truncar snapshots ao limite das rules**

**Motivo (achado da revisão do plano, verificado empiricamente):** as rules do A8.7
(pendentes de publicação) limitam `trechoSnapshot` e `dispositivoLabelSnapshot` a
**1000 chars**, mas a tela grava o texto COMPLETO do dispositivo como snapshot — e o
Regulamento tem incisos de até **1792 chars** (o RI tem 25 textos acima de 1000,
chegando a 7737). Sem este passo, comentar nesses dispositivos passaria a falhar assim
que as rules forem publicadas. O snapshot é só um retrato de contexto — truncar não
perde nada essencial.

Em `src/lib/reviewData.js`, troque o corpo de `addSuggestion`:

```js
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
```

por:

```js
// As rules limitam os snapshots a 1000 chars (A8.7); dispositivos longos (há incisos
// de 1792 chars no Regulamento e textos de até 7737 no RI) são truncados — o snapshot
// é só contexto, o dispositivoId continua apontando para o texto íntegro.
const SNAPSHOT_MAX = 1000

export async function addSuggestion({ dispositivoId, dispositivoLabelSnapshot, trechoSnapshot, texto, autor }) {
  await addDoc(collection(db, COL), {
    dispositivoId,
    dispositivoLabelSnapshot: String(dispositivoLabelSnapshot ?? '').slice(0, SNAPSHOT_MAX),
    trechoSnapshot: String(trechoSnapshot ?? '').slice(0, SNAPSHOT_MAX),
    texto: texto.trim(),
    autorUid: autor.uid,
    autorNome: autor.nome,
    curtidoPor: [],
    criadoEm: serverTimestamp(),
  })
}
```

- [ ] **Step 3b: Verificação manual (documentar no commit, executar quando possível)**

Sem emulador do Firestore configurado neste projeto, a verificação real depende de rodar
`npm run dev` com um usuário admin logado (fica com o Wândrio, como nas fatias
anteriores). Passos a documentar/testar:
1. Sem o doc `config/revisao` existir: `subscribeRevisaoConfig` deve entregar
   `{ regulamentoAberto: false }` (não deve travar nem lançar erro).
2. Chamar `setRegulamentoAberto(true)` (via UI da Task 4) deve criar/atualizar o doc e o
   `onSnapshot` deve refletir a mudança em tempo real, sem recarregar a página.
3. Comentar num dispositivo de texto longo (> 1000 chars) grava a sugestão com snapshot
   truncado, sem erro.

- [ ] **Step 4: Rodar a suíte de testes JS para garantir que nada quebrou**

Run: `npm test`
Expected: PASS — mesma contagem de antes + os 5 testes novos da Task 1 (nenhum teste
novo nesta task, pois não há lógica pura a isolar).

- [ ] **Step 5: Commit**

```bash
cd "/Users/wandriobandeira/Projetos de dev Sistemas/Comparativo-de-cargos-e-funcoes"
git add src/lib/reviewData.js
git commit -m "$(cat <<'EOF'
feat(revisao): interruptor de admin + snapshots truncados ao limite das rules

subscribeRevisaoConfig/setRegulamentoAberto leem/gravam config/revisao
(Firestore). Ausência do doc é tratada como fechado (fail-closed) —
o Regulamento só fica comentável quando um admin liga o interruptor.
addSuggestion trunca trechoSnapshot/dispositivoLabelSnapshot em 1000
chars: corrige bug latente em que comentar dispositivos longos
(incisos de até 1792 chars no Regulamento, 7737 no RI) falharia assim
que as rules do A8.7 fossem publicadas.
EOF
)"
```

---

### Task 3: Regra do Firestore para `config/revisao`

**Files:**
- Modify: `firestore.rules`

**Interfaces:**
- Consumes: `isMember()`/`isAdmin()` (funções já definidas no topo do arquivo, linhas
  6-14).
- Produces: nada consumido por outra task — é a barreira de segurança do interruptor
  criado na Task 2.

- [ ] **Step 1: Adicionar o bloco de regra**

Em `firestore.rules`, depois do bloco `match /finalTexts/{id} { ... }` (última regra do
arquivo) e antes do `}` de fechamento do `match /databases/{database}/documents`,
adicione:

```
    match /config/revisao {
      allow read: if isMember();
      allow write: if isAdmin();
    }
```

- [ ] **Step 2: Conferir a sintaxe do arquivo inteiro**

Não há Firebase CLI logado neste ambiente (e o projeto não usa emulador), então a
conferência é visual + estrutural: chaves balanceadas e a regra nova DENTRO do escopo
`match /databases/{database}/documents`, no mesmo padrão dos blocos vizinhos
(`members`, `suggestions`, `finalTexts`). Checagem mecânica de balanceamento:

Run: `python3 -c "s=open('firestore.rules').read(); assert s.count('{')==s.count('}'), 'chaves desbalanceadas'; print('chaves OK:', s.count('{'))"`
Expected: `chaves OK: <n>` sem AssertionError. A validação REAL de sintaxe acontece no
console do Firebase na hora de publicar (o editor de rules do console acusa erro antes
de aceitar) — que já é a pendência registrada do Wândrio.

- [ ] **Step 3: Commit**

```bash
cd "/Users/wandriobandeira/Projetos de dev Sistemas/Comparativo-de-cargos-e-funcoes"
git add firestore.rules
git commit -m "$(cat <<'EOF'
feat(rules): config/revisao só admin escreve, qualquer membro lê

Protege o interruptor "Regulamento aberto para comentários" — a garantia
real de que só admin liga/desliga está na regra, não só na UI.
EOF
)"
```

**Nota para a próxima etapa (fora deste plano):** esta regra só passa a valer em
produção quando publicada pelo console do Firebase — mesma pendência já registrada para
os limites de tamanho do A8.7 (`docs/FIREBASE_SETUP.md`). Publicar as duas juntas.

---

### Task 4: Seletor de documento + interruptor + filtro na página (`Revisao.jsx`)

**Files:**
- Modify: `src/pages/Revisao.jsx`
- Modify: `src/index.css` (2 classes novas)

**Interfaces:**
- Consumes:
  - `filterSuggestionsByDoc(suggestions, docId)`, `filterFinalsByDoc(finals, docId)` da
    Task 1 (`src/lib/reviewGroup.js`).
  - `subscribeRevisaoConfig(onChange, onError)`, `setRegulamentoAberto(aberto)` da
    Task 2 (`src/lib/reviewData.js`).
  - `EmptyState` de `src/components/Status.jsx` (já existe: `{icon, title, text}`).
  - `user.role` de `useAuth()` (já existe: `'admin' | 'participante'`, ver
    `src/lib/auth.jsx:45-50`).
- Produces: nada consumido por outra task — é a página final.

- [ ] **Step 1: Atualizar os imports do arquivo**

Em `src/pages/Revisao.jsx`, troque a linha de import de `reviewGroup.js`:

```js
import { groupByDispositivo, countByDispositivo, countByChapter } from '../lib/reviewGroup.js'
```

por:

```js
import {
  groupByDispositivo, countByDispositivo, countByChapter,
  filterSuggestionsByDoc, filterFinalsByDoc,
} from '../lib/reviewGroup.js'
```

E a linha de import de `reviewData.js`:

```js
import {
  subscribeSuggestions, addSuggestion, toggleLike, deleteSuggestion,
  setAdminStatus, subscribeFinalTexts, saveFinalText,
} from '../lib/reviewData.js'
```

por:

```js
import {
  subscribeSuggestions, addSuggestion, toggleLike, deleteSuggestion,
  setAdminStatus, subscribeFinalTexts, saveFinalText,
  subscribeRevisaoConfig, setRegulamentoAberto,
} from '../lib/reviewData.js'
```

E a linha de import de `Status.jsx`:

```js
import { LoadingState, ErrorState } from '../components/Status.jsx'
```

por:

```js
import { LoadingState, ErrorState, EmptyState } from '../components/Status.jsx'
```

- [ ] **Step 2: Trocar o carregamento de dados para depender do documento escolhido**

Troque este bloco (linhas 33-42 do arquivo original):

```js
  const [data, setData] = useState(null)
  const [erro, setErro] = useState(null)
  const [suggestions, setSuggestions] = useState([])
  const [aberto, setAberto] = useState(null) // { id, label, trecho }

  useEffect(() => {
    fetchJson('/database/minuta_structure.json')
      .then(setData)
      .catch(() => setErro('Não foi possível carregar a minuta.'))
  }, [])
```

por:

```js
  const [docId, setDocId] = useState('ri') // 'ri' | 'reg'
  const [data, setData] = useState(null)
  const [erro, setErro] = useState(null)
  const [suggestions, setSuggestions] = useState([])
  const [aberto, setAberto] = useState(null) // { id, label, trecho }
  const [regulamentoAberto, setRegulamentoAbertoState] = useState(false)

  useEffect(() => {
    setData(null)
    setErro(null)
    setAberto(null) // fecha a modal ao trocar de documento — evita comentar no doc errado
    const url = docId === 'reg' ? '/database/regulamento_structure.json' : '/database/minuta_structure.json'
    fetchJson(url)
      .then(setData)
      .catch(() => setErro('Não foi possível carregar o documento.'))
  }, [docId])

  // Ausência do doc config/revisao == fechado (fail-closed) — ver reviewData.js.
  useEffect(() => subscribeRevisaoConfig(
    (cfg) => setRegulamentoAbertoState(cfg.regulamentoAberto === true),
    (e) => console.error('Erro na config da revisão:', e),
  ), [])
```

- [ ] **Step 3: Filtrar sugestões/finais pelo documento escolhido antes de agrupar**

Troque este bloco (linhas 54-56 do arquivo original):

```js
  const counts = useMemo(() => countByDispositivo(suggestions), [suggestions])
  const grupos = useMemo(() => groupByDispositivo(suggestions), [suggestions])
  const articles = useMemo(() => (data ? buildArticles(data) : []), [data])
```

por:

```js
  const suggestionsForDoc = useMemo(() => filterSuggestionsByDoc(suggestions, docId), [suggestions, docId])
  const counts = useMemo(() => countByDispositivo(suggestionsForDoc), [suggestionsForDoc])
  const grupos = useMemo(() => groupByDispositivo(suggestionsForDoc), [suggestionsForDoc])
  const articles = useMemo(() => (data ? buildArticles(data) : []), [data])
```

Troque este bloco (linhas 50-52 e 57-61 do arquivo original):

```js
  const [finals, setFinals] = useState(new Map())
  // Idem: subscribeFinalTexts também retorna o unsubscribe do onSnapshot.
  useEffect(() => subscribeFinalTexts(setFinals, (e) => console.error('Erro finalTexts:', e)), [])
```

e

```js
  const fechados = useMemo(() => {
    let n = 0
    finals.forEach(f => { if (f.status === 'fechado') n += 1 })
    return n
  }, [finals])
```

por:

```js
  const [finals, setFinals] = useState(new Map())
  // Idem: subscribeFinalTexts também retorna o unsubscribe do onSnapshot.
  useEffect(() => subscribeFinalTexts(setFinals, (e) => console.error('Erro finalTexts:', e)), [])

  const finalsForDoc = useMemo(() => filterFinalsByDoc(finals, docId), [finals, docId])

  const fechados = useMemo(() => {
    let n = 0
    finalsForDoc.forEach(f => { if (f.status === 'fechado') n += 1 })
    return n
  }, [finalsForDoc])
```

- [ ] **Step 4: Trocar `countByChapter` e os usos de `finals` no corpo do documento para as versões filtradas**

Troque (linhas 73-76 do arquivo original):

```js
  const chapterCounts = useMemo(
    () => countByChapter(suggestions, finals, parseDispositivoId, chapterIdOf),
    [suggestions, finals],
  )
```

por:

```js
  const chapterCounts = useMemo(
    () => countByChapter(suggestionsForDoc, finalsForDoc, parseDispositivoId, chapterIdOf),
    [suggestionsForDoc, finalsForDoc],
  )
```

Troque, no JSX de renderização dos artigos, as duas ocorrências de `finals.get(...)` por
`finalsForDoc.get(...)`:

```js
                <div className={`rev-line${finals.get(caputId)?.status === 'fechado' ? ' fechado' : ''}`}>
```
→
```js
                <div className={`rev-line${finalsForDoc.get(caputId)?.status === 'fechado' ? ' fechado' : ''}`}>
```

```js
                    <div className={`rev-line rev-inciso${finals.get(id)?.status === 'fechado' ? ' fechado' : ''}`} key={`${id}`}>
```
→
```js
                    <div className={`rev-line rev-inciso${finalsForDoc.get(id)?.status === 'fechado' ? ' fechado' : ''}`} key={`${id}`}>
```

E no `RevisaoModal`, troque `finalText={finals.get(aberto.id) ?? null}` por
`finalText={finalsForDoc.get(aberto.id) ?? null}`.

- [ ] **Step 5: Cabeçalho — título dinâmico, seletor de documento e interruptor de admin**

Troque o bloco do cabeçalho (linhas 119-130 do arquivo original):

```js
  if (erro) return <ErrorState title="Erro ao carregar" hint={erro} />
  if (!data) return <LoadingState label="Carregando minuta…" />

  return (
    <>
      <div className="page-header">
        <div className="page-header-left">
          <h2 className="page-title">Revisão da Minuta</h2>
          <p className="page-subtitle">
            Clique no balão à direita de cada dispositivo para ver e enviar sugestões.
            As sugestões de todos ficam visíveis.
          </p>
          <p className="rev-progresso">{fechados} dispositivo(s) com texto final fechado.</p>
        </div>
      </div>
```

por:

```js
  const bloqueadoParaComissao = docId === 'reg' && !regulamentoAberto && user.role !== 'admin'
  const tituloDoc = docId === 'reg' ? 'Revisão do Regulamento' : 'Revisão da Minuta'

  if (erro) return <ErrorState title="Erro ao carregar" hint={erro} />
  if (!data) return <LoadingState label="Carregando…" />

  return (
    <>
      <div className="page-header">
        <div className="page-header-left">
          <h2 className="page-title">{tituloDoc}</h2>
          {!bloqueadoParaComissao && (
            <>
              <p className="page-subtitle">
                Clique no balão à direita de cada dispositivo para ver e enviar sugestões.
                As sugestões de todos ficam visíveis.
              </p>
              <p className="rev-progresso">{fechados} dispositivo(s) com texto final fechado.</p>
            </>
          )}
          <div className="rev-doc-switch">
            <button
              type="button"
              className={`oc-state-chip${docId === 'ri' ? ' active' : ''}`}
              onClick={() => setDocId('ri')}
            >
              Minuta do RI
            </button>
            <button
              type="button"
              className={`oc-state-chip${docId === 'reg' ? ' active' : ''}`}
              onClick={() => setDocId('reg')}
            >
              Regulamento
            </button>
          </div>
          {user.role === 'admin' && docId === 'reg' && (
            <button
              type="button"
              className="btn btn-ghost rev-doc-toggle"
              onClick={() => setRegulamentoAberto(!regulamentoAberto)}
            >
              {regulamentoAberto
                ? 'Comissão PODE comentar o Regulamento (clique para fechar)'
                : 'Comissão NÃO pode comentar o Regulamento ainda (clique para abrir)'}
            </button>
          )}
        </div>
      </div>
```

- [ ] **Step 6: Bloquear o corpo do documento quando fechado para a comissão**

Troque o início de `<div className="page-body">` (linha 132 do arquivo original):

```js
      <div className="page-body">
        <div className="rc-layout">
```

por:

```js
      <div className="page-body">
        {bloqueadoParaComissao ? (
          <EmptyState
            title="Regulamento em preparação"
            text="Este documento ainda não foi liberado para comentários. Volte em breve."
          />
        ) : (
        <div className="rc-layout">
```

E, no fechamento correspondente (linha 180-181 do arquivo original):

```js
          </div>
        </div>
      </div>
```

por:

```js
          </div>
        </div>
        )}
      </div>
```

- [ ] **Step 7: Adicionar as classes CSS novas**

Em `src/index.css`, logo depois do bloco `.rev-rail { ... }` (linha 2322), adicione:

```css
.rev-doc-switch { display: flex; gap: 6px; margin: 6px 0 4px; }
.rev-doc-toggle { margin-top: 4px; font-size: 12.5px; }
```

- [ ] **Step 8: Rodar a suíte de testes JS**

Run: `npm test`
Expected: PASS — mesma contagem de antes (nenhum teste novo nesta task; a lógica pura
já foi testada na Task 1).

- [ ] **Step 9: Rodar o build de produção**

Run: `npm run build`
Expected: build limpo, sem erros (confirma que o JSX está sintaticamente correto e sem
imports quebrados).

- [ ] **Step 10: Verificação manual no navegador (checklist para quem executa a task)**

Com `npm run dev` rodando e logado como participante comum:
1. Abrir `/revisao` → vê "Minuta do RI" ativo por padrão, documento do RI carregado
   normalmente (igual a antes desta mudança).
2. Clicar em "Regulamento" → se o interruptor estiver desligado, vê o `EmptyState`
   "Regulamento em preparação" (não vê o documento, não vê balões).
3. Voltar para "Minuta do RI" → sugestões e textos finais do RI continuam exatamente
   como antes (nenhum comentário antigo sumiu).

Logado como admin:
4. Ver o botão de interruptor abaixo do seletor quando "Regulamento" está selecionado.
5. Clicar para abrir → o documento do Regulamento aparece com os balões, comentar
   funciona, o comentário fica só nesse documento (voltar para "Minuta do RI" não mostra
   esse comentário).
6. Deslogar e logar como participante comum (ou pedir a outra pessoa) → confirma que
   agora consegue ver e comentar o Regulamento também.

- [ ] **Step 11: Commit**

```bash
cd "/Users/wandriobandeira/Projetos de dev Sistemas/Comparativo-de-cargos-e-funcoes"
git add src/pages/Revisao.jsx src/index.css
git commit -m "$(cat <<'EOF'
feat(revisao): seletor RI/Regulamento + gate de comentários por admin

Revisao.jsx passa a carregar minuta_structure.json ou
regulamento_structure.json conforme o documento escolhido no seletor do
topo, filtrando sugestões/textos finais pelo prefixo reg: (Task 1) e
respeitando o interruptor de admin (Task 2/3) — participante comum só
comenta o Regulamento depois que um admin abrir.
EOF
)"
```

---

### Task 5: Documentação (`CLAUDE.md`)

**Files:**
- Modify: `CLAUDE.md`

**Interfaces:**
- Consumes: nada (documentação).
- Produces: nada consumido por código — referência para sessões futuras.

- [ ] **Step 1: Atualizar a seção "Dados (Firestore) e regras"**

Em `CLAUDE.md`, no bloco que começa em `### Dados (Firestore) e regras` (linha ~300),
depois da linha:

```
- `dispositivoId` (`src/lib/dispositivoId.js`) é o endereço ESTÁVEL do dispositivo (`editId#index` ou
  `editId#caput`), pois o "Art. Nº" é recalculado por `buildArticles`. Premissa: congelar
  `minuta_structure.json` durante a rodada de revisão.
```

adicione:

```
- **Multi-documento na Revisão (Bloco C, fatia 1):** a página `/revisao` comenta DOIS
  documentos — a minuta do RI (`minuta_structure.json`) e a minuta do Regulamento
  (`regulamento_structure.json`) — sem misturar comentários. A separação usa o prefixo
  `reg:` que TODO `editId` do Regulamento já carrega desde o Bloco B2 (`editId` do RI
  nunca deve começar com `reg:` — é a premissa que garante o isolamento; ver
  `src/lib/reviewGroup.js:docOfDispositivo`). Nova coleção **`config/revisao`**
  (doc único, campo `regulamentoAberto: boolean`) controla quando o Regulamento fica
  comentável para quem não é admin; ausência do doc = fechado (fail-closed). Design
  completo em `docs/superpowers/specs/2026-07-07-comissao-comenta-regulamento-design.md`.
```

- [ ] **Step 2: Commit**

```bash
cd "/Users/wandriobandeira/Projetos de dev Sistemas/Comparativo-de-cargos-e-funcoes"
git add CLAUDE.md
git commit -m "docs: documentar multi-documento na Revisão (RI + Regulamento)"
```

---

### Task 6: Verificação final e push

**Files:** nenhum (task de fechamento — roda os gates e sincroniza com o remoto).

- [ ] **Step 1: Rodar toda a suíte JS**

Run: `npm test`
Expected: PASS — todos os testes (os já existentes + os 5 novos da Task 1).

- [ ] **Step 2: Rodar o build de produção**

Run: `npm run build`
Expected: build limpo, sem erros.

- [ ] **Step 3: Conferir working tree limpo**

Run: `git status --short`
Expected: sem saída (tudo commitado nas Tasks 1-5).

- [ ] **Step 4: Sincronizar com o remoto**

```bash
cd "/Users/wandriobandeira/Projetos de dev Sistemas/Comparativo-de-cargos-e-funcoes"
git fetch origin
git push origin feat/auditoria-seguranca-e-comparador-regulamento
git rev-parse HEAD
git rev-parse origin/feat/auditoria-seguranca-e-comparador-regulamento
```

Expected: os dois SHAs finais são idênticos.

- [ ] **Step 5: Relatar ao Wândrio as pendências que exigem ele**

Ao final, avisar explicitamente (nenhuma destas é testável sem acesso real):
1. Publicar as regras atualizadas de `firestore.rules` (bloco `config/revisao` desta
   fatia + os limites de tamanho pendentes do A8.7) pelo console do Firebase.
2. Testar o fluxo com login real de dois usuários (um admin, um participante comum) —
   nenhuma conta de teste foi criada no projeto de produção
   `revisao-minuta-cbmro-6f248`.
3. Só ligar o interruptor "Regulamento aberto para comentários" depois de validar a
   minuta gerada no Bloco B2 — a fatia 1 dá o controle, mas a decisão de quando abrir é
   dele.
4. Transparência (não é bug): comentários de TESTE que o admin fizer no Regulamento
   antes de abrir ficam tecnicamente legíveis para qualquer membro que consultar o
   Firestore diretamente (as rules de `suggestions` dão leitura a todo membro; a UI é
   que esconde). Mesmo grupo de confiança, risco aceito — mas o admin deve apagar
   comentários de teste antes de abrir, por higiene.
