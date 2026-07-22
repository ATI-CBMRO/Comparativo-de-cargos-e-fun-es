# Cenários LOB (Fase 1: chave + isolamento) — Plano de Implementação

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Adicionar uma chave no topo que alterna o portal entre "LOB atual" e "LOB futura", sem os cenários se misturarem, mantendo a LOB futura idêntica a hoje.

**Architecture:** Um contexto React (`ScenarioProvider`/`useScenario`) guarda o cenário ativo, persistido em `localStorage` e refletido na URL (`?cenario=atual`). A LOB futura continua lendo os arquivos de dados de hoje (nada movido). No cenário "atual", as páginas das duas trilhas (Regimento Interno e Regulamento Geral) exibem um placeholder "Em construção" em vez de carregar dados — logo, nenhum dado se mistura. A separação de dados real (pasta `database/atual/`) e o conteúdo entram na Fase 2.

**Tech Stack:** React 18, react-router-dom v6, Vite. Testes de lógica pura com `node --test` (ESM, `node:test` + `node:assert/strict`). Validação visual/e2e com Playwright.

## Global Constraints

- **Não mover nenhum arquivo de dados nem alterar scripts Python nesta fase.** A LOB futura deve permanecer byte-a-byte como hoje (decisão do Wândrio: "futura fica onde está").
- **Cenário na URL como parâmetro** (`?cenario=atual` | `?cenario=futura`), nunca como prefixo de rota.
- **Cenários válidos:** exatamente `'futura'` e `'atual'`. Padrão: `'futura'`.
- **Rótulos de menu inalterados:** as trilhas continuam "Regimento Interno" e "Regulamento Geral" nos dois cenários.
- **Isolamento do Firebase/comentários fica FORA da Fase 1** (a revisão da LOB atual nasce vazia; sem risco de mistura). Registrado na Fase 2.
- **Idioma:** todo texto de UI em pt-BR.
- Testes rodam com `npm test` (= `node --test "src/lib/**/*.test.js" "api/**/*.test.js"`).

---

## Estrutura de arquivos

- **Criar** `src/lib/scenario.js` — lógica pura do cenário: constantes e resolução (URL/armazenamento → cenário). Sem React. Testável.
- **Criar** `src/lib/scenario.test.js` — testes da lógica pura.
- **Criar** `src/context/ScenarioContext.jsx` — `ScenarioProvider` + `useScenario` (estado + sync `localStorage` + sync URL via `useSearchParams`).
- **Criar** `src/components/ScenarioSwitcher.jsx` — o seletor visual no topo da barra lateral.
- **Criar** `src/components/EmConstrucao.jsx` — placeholder das páginas de trilha no cenário "atual".
- **Modificar** `src/main.jsx` — envolver `<App/>` com `<ScenarioProvider>` (dentro de `BrowserRouter`).
- **Modificar** `src/App.jsx` — renderizar `<ScenarioSwitcher/>` na `Sidebar`; envolver as rotas específicas de cenário com o portão `<TrilhaRoute>`.
- **Modificar** `src/index.css` — estilos do seletor e do placeholder (escopo próprio).

---

## Task 1: Lógica pura do cenário (`scenario.js`)

**Files:**
- Create: `src/lib/scenario.js`
- Test: `src/lib/scenario.test.js`

**Interfaces:**
- Consumes: nada.
- Produces:
  - `SCENARIOS: readonly ['futura','atual']`
  - `DEFAULT_SCENARIO: 'futura'`
  - `normalizeScenario(value: string|null|undefined) => 'futura'|'atual'` (qualquer valor inválido vira `DEFAULT_SCENARIO`)
  - `resolveScenario(urlValue: string|null, storedValue: string|null) => 'futura'|'atual'` (prioridade: URL válida → armazenamento → padrão)

- [ ] **Step 1: Escrever os testes que falham**

Criar `src/lib/scenario.test.js`:

```js
import { test } from 'node:test'
import assert from 'node:assert/strict'
import { SCENARIOS, DEFAULT_SCENARIO, normalizeScenario, resolveScenario } from './scenario.js'

test('SCENARIOS e padrão', () => {
  assert.deepEqual([...SCENARIOS], ['futura', 'atual'])
  assert.equal(DEFAULT_SCENARIO, 'futura')
})

test('normalizeScenario aceita válidos e cai no padrão nos inválidos', () => {
  assert.equal(normalizeScenario('atual'), 'atual')
  assert.equal(normalizeScenario('futura'), 'futura')
  assert.equal(normalizeScenario('xpto'), 'futura')
  assert.equal(normalizeScenario(null), 'futura')
  assert.equal(normalizeScenario(undefined), 'futura')
})

test('resolveScenario prioriza a URL quando válida', () => {
  assert.equal(resolveScenario('atual', 'futura'), 'atual')
  assert.equal(resolveScenario('futura', 'atual'), 'futura')
})

test('resolveScenario usa o armazenamento quando a URL é inválida/ausente', () => {
  assert.equal(resolveScenario(null, 'atual'), 'atual')
  assert.equal(resolveScenario('lixo', 'atual'), 'atual')
})

test('resolveScenario cai no padrão quando URL e armazenamento são inválidos', () => {
  assert.equal(resolveScenario(null, null), 'futura')
  assert.equal(resolveScenario('', 'nada'), 'futura')
})
```

- [ ] **Step 2: Rodar e ver falhar**

Run: `npm test`
Expected: FAIL — `Cannot find module './scenario.js'` (ou similar).

- [ ] **Step 3: Implementar o mínimo**

Criar `src/lib/scenario.js`:

```js
// Lógica pura do cenário (LOB atual × LOB futura). Sem React — testável com node --test.
// 'futura' = LOB em aprovação (arquivos de dados de hoje). 'atual' = LOB vigente (Fase 2).
export const SCENARIOS = Object.freeze(['futura', 'atual'])
export const DEFAULT_SCENARIO = 'futura'

export function normalizeScenario(value) {
  return SCENARIOS.includes(value) ? value : DEFAULT_SCENARIO
}

// Prioridade: valor válido na URL > valor armazenado (localStorage) > padrão.
export function resolveScenario(urlValue, storedValue) {
  if (SCENARIOS.includes(urlValue)) return urlValue
  return normalizeScenario(storedValue)
}
```

- [ ] **Step 4: Rodar e ver passar**

Run: `npm test`
Expected: PASS (todos os testes de `scenario.test.js` verdes; os demais continuam passando).

- [ ] **Step 5: Commit**

```bash
git add src/lib/scenario.js src/lib/scenario.test.js
git commit -m "feat(cenario): lógica pura de resolução de cenário LOB (atual/futura)"
```

---

## Task 2: Contexto React do cenário (`ScenarioContext`)

**Files:**
- Create: `src/context/ScenarioContext.jsx`
- Modify: `src/main.jsx`

**Interfaces:**
- Consumes: `resolveScenario`, `normalizeScenario`, `SCENARIOS`, `DEFAULT_SCENARIO` de `src/lib/scenario.js`.
- Produces:
  - `<ScenarioProvider>{children}</ScenarioProvider>` — deve estar dentro de `BrowserRouter`.
  - `useScenario() => { cenario: 'futura'|'atual', setCenario: (c) => void }`
  - Chave de armazenamento: `localStorage['portal-cbm.cenario']`.

- [ ] **Step 1: Implementar o provider e o hook**

Criar `src/context/ScenarioContext.jsx`:

```jsx
import { createContext, useContext, useCallback, useEffect, useMemo } from 'react'
import { useSearchParams } from 'react-router-dom'
import { resolveScenario, normalizeScenario, DEFAULT_SCENARIO } from '../lib/scenario.js'

const STORAGE_KEY = 'portal-cbm.cenario'
const ScenarioContext = createContext(null)

function readStored() {
  try { return localStorage.getItem(STORAGE_KEY) } catch { return null }
}
function writeStored(cenario) {
  try { localStorage.setItem(STORAGE_KEY, cenario) } catch { /* ignora storage indisponível */ }
}

export function ScenarioProvider({ children }) {
  const [searchParams, setSearchParams] = useSearchParams()
  // Cenário ativo é derivado da URL (fonte da verdade), com fallback no armazenamento.
  const cenario = resolveScenario(searchParams.get('cenario'), readStored())

  // Mantém o armazenamento em dia com o cenário efetivo (ex.: primeira visita sem URL).
  useEffect(() => { writeStored(cenario) }, [cenario])

  const setCenario = useCallback((next) => {
    const c = normalizeScenario(next)
    writeStored(c)
    setSearchParams((prev) => {
      const p = new URLSearchParams(prev)
      p.set('cenario', c)
      return p
    }, { replace: false })
  }, [setSearchParams])

  const value = useMemo(() => ({ cenario, setCenario }), [cenario, setCenario])
  return <ScenarioContext.Provider value={value}>{children}</ScenarioContext.Provider>
}

export function useScenario() {
  const ctx = useContext(ScenarioContext)
  if (!ctx) throw new Error('useScenario deve ser usado dentro de <ScenarioProvider>')
  return ctx
}

export { DEFAULT_SCENARIO }
```

- [ ] **Step 2: Envolver o App com o provider**

Modificar `src/main.jsx` — adicionar o import e inserir `<ScenarioProvider>` entre `<AuthProvider>` e `<App/>`:

```jsx
import React from 'react'
import ReactDOM from 'react-dom/client'
import { BrowserRouter } from 'react-router-dom'
import App from './App.jsx'
import { AuthProvider } from './lib/auth.jsx'
import { ScenarioProvider } from './context/ScenarioContext.jsx'
import './index.css'

ReactDOM.createRoot(document.getElementById('root')).render(
  <React.StrictMode>
    <BrowserRouter>
      <AuthProvider>
        <ScenarioProvider>
          <App />
        </ScenarioProvider>
      </AuthProvider>
    </BrowserRouter>
  </React.StrictMode>
)
```

- [ ] **Step 3: Validar que o app sobe sem erro**

Run: `npm run dev` (em background) e abrir `http://localhost:5173` com Playwright.
Expected: a aplicação carrega normalmente (sem tela branca, sem erro no console do navegador). O comportamento visível ainda é idêntico a hoje (nenhuma UI de cenário ainda).

- [ ] **Step 4: Commit**

```bash
git add src/context/ScenarioContext.jsx src/main.jsx
git commit -m "feat(cenario): contexto React (provider/useScenario) com sync URL+localStorage"
```

---

## Task 3: Seletor de cenário no topo da barra lateral

**Files:**
- Create: `src/components/ScenarioSwitcher.jsx`
- Modify: `src/App.jsx` (renderizar o seletor na `Sidebar`, logo abaixo do logo)
- Modify: `src/index.css` (estilos com escopo `.scenario-switcher`)

**Interfaces:**
- Consumes: `useScenario()` de `src/context/ScenarioContext.jsx`.
- Produces: `<ScenarioSwitcher />` (sem props).

- [ ] **Step 1: Criar o componente**

Criar `src/components/ScenarioSwitcher.jsx`:

```jsx
import { useScenario } from '../context/ScenarioContext.jsx'

const OPCOES = [
  { id: 'atual', label: 'LOB atual', hint: 'Vigente' },
  { id: 'futura', label: 'LOB futura', hint: 'Em aprovação' },
]

export default function ScenarioSwitcher() {
  const { cenario, setCenario } = useScenario()
  return (
    <div className={`scenario-switcher scenario-${cenario}`} role="group" aria-label="Cenário de LOB">
      <div className="scenario-switcher-label">Cenário</div>
      <div className="scenario-switcher-tabs">
        {OPCOES.map((o) => (
          <button
            key={o.id}
            type="button"
            className={`scenario-tab${cenario === o.id ? ' is-active' : ''}`}
            aria-pressed={cenario === o.id}
            onClick={() => setCenario(o.id)}
            title={`${o.label} — ${o.hint}`}
          >
            <strong>{o.label}</strong>
            <span>{o.hint}</span>
          </button>
        ))}
      </div>
    </div>
  )
}
```

- [ ] **Step 2: Renderizar na Sidebar**

Em `src/App.jsx`: adicionar o import no topo (junto dos outros de componentes):

```jsx
import ScenarioSwitcher from './components/ScenarioSwitcher.jsx'
```

E na função `Sidebar`, inserir `<ScenarioSwitcher />` logo após o botão `.sidebar-logo` (entre a linha que fecha o `</button>` do logo e a abertura de `<nav className="sidebar-nav">`):

```jsx
      </button>

      <ScenarioSwitcher />

      <nav className="sidebar-nav">
```

- [ ] **Step 3: Estilos**

Acrescentar ao final de `src/index.css`:

```css
/* Seletor de cenário LOB (topo da barra lateral) */
.scenario-switcher { padding: 10px 12px 4px; }
.scenario-switcher-label {
  font-size: 11px; text-transform: uppercase; letter-spacing: .06em;
  color: var(--navy-500); margin-bottom: 6px;
}
.scenario-switcher-tabs { display: flex; gap: 6px; }
.scenario-tab {
  flex: 1; display: flex; flex-direction: column; align-items: flex-start;
  padding: 6px 8px; border: 1px solid var(--navy-200, #d9dee7); border-radius: 8px;
  background: #fff; cursor: pointer; line-height: 1.15; text-align: left;
}
.scenario-tab strong { font-size: 12px; color: var(--navy-700, #2a3a55); }
.scenario-tab span { font-size: 10px; color: var(--navy-500, #6b7793); }
.scenario-tab.is-active { border-color: transparent; color: #fff; }
/* Cor por cenário: atual = navy; futura = vermelho CBMRO */
.scenario-atual .scenario-tab.is-active { background: #26324a; }
.scenario-atual .scenario-tab.is-active strong,
.scenario-atual .scenario-tab.is-active span { color: #fff; }
.scenario-futura .scenario-tab.is-active { background: #c8102e; }
.scenario-futura .scenario-tab.is-active strong,
.scenario-futura .scenario-tab.is-active span { color: #fff; }
```

- [ ] **Step 4: Validar visualmente (Playwright)**

Com `npm run dev` no ar, abrir `http://localhost:5173` no Playwright e:
1. Tirar screenshot do topo da barra lateral com "LOB futura" ativo (chip vermelho).
2. Clicar em "LOB atual" e conferir: chip navy ativo **e** a URL passou a conter `?cenario=atual`.
3. Recarregar a página e conferir que "LOB atual" continua selecionado (persistência).

Expected: os três pontos confirmados, com screenshot colado na mensagem.

- [ ] **Step 5: Commit**

```bash
git add src/components/ScenarioSwitcher.jsx src/App.jsx src/index.css
git commit -m "feat(cenario): seletor de cenário no topo da sidebar (cor por cenário, URL+persistência)"
```

---

## Task 4: Portão "Em construção" nas trilhas do cenário atual

**Files:**
- Create: `src/components/EmConstrucao.jsx`
- Modify: `src/App.jsx` (definir `TrilhaRoute` e envolver as rotas específicas de cenário)
- Modify: `src/index.css` (estilo do placeholder)

**Interfaces:**
- Consumes: `useScenario()` de `src/context/ScenarioContext.jsx`.
- Produces:
  - `<EmConstrucao />` — placeholder de página.
  - `TrilhaRoute` (helper local em `App.jsx`): renderiza `children` quando `cenario==='futura'`; senão `<EmConstrucao/>`.

Rotas a envolver (todas as que consomem dados específicos de cenário — minuta/regulamento):
`/minuta/subsidio`, `/minuta`, `/minuta/diagramas`, `/minuta/revisao`,
`/regulamento/subsidio`, `/regulamento`, `/regulamento/diagramas`, `/regulamento/revisao`,
e as de compatibilidade: `/comparar`, `/minuta-diagramas`, `/minuta/deliberacao`,
`/minuta/comparar`, `/minuta/comparativo-ri`, `/regulamento/comparar`, `/revisao`.
(NÃO envolver as páginas do bloco "Geral": `/legislacoes`, `/organograma`, `/manual`,
`/acessos`, `/estados`, `/estados/:id`, `/busca` — são compartilhadas.)

- [ ] **Step 1: Criar o placeholder**

Criar `src/components/EmConstrucao.jsx`:

```jsx
export default function EmConstrucao() {
  return (
    <div className="em-construcao">
      <h1>Em construção</h1>
      <p>
        Este documento ainda não foi elaborado para a <strong>LOB atual</strong> (vigente).
        A estrutura e as minutas do cenário atual serão montadas nas próximas etapas.
      </p>
      <p className="em-construcao-dica">
        Para ver o trabalho já pronto, troque o cenário para <strong>LOB futura</strong> no
        topo da barra lateral.
      </p>
    </div>
  )
}
```

- [ ] **Step 2: Definir o portão `TrilhaRoute` em App.jsx**

Em `src/App.jsx`, adicionar o import:

```jsx
import EmConstrucao from './components/EmConstrucao.jsx'
import { useScenario } from './context/ScenarioContext.jsx'
```

E definir o helper (perto dos outros componentes utilitários de rota, ex.: acima de `AlreadyLoggedInRedirect`):

```jsx
// Páginas das trilhas (Regimento Interno / Regulamento Geral) só têm conteúdo na LOB
// futura por enquanto. No cenário "atual", mostram o placeholder — nada de dados se mistura.
function TrilhaRoute({ children }) {
  const { cenario } = useScenario()
  return cenario === 'atual' ? <EmConstrucao /> : children
}
```

- [ ] **Step 3: Envolver as rotas específicas de cenário**

Em `src/App.jsx`, no bloco `<Routes>`, trocar cada rota de trilha para envolver o elemento com `<TrilhaRoute>`. Exemplos (aplicar o mesmo padrão a TODAS as rotas listadas nas Interfaces):

```jsx
          <Route path="/minuta/subsidio" element={<TrilhaRoute><RISubsidio /></TrilhaRoute>} />
          <Route path="/minuta" element={<TrilhaRoute><MinutaWizard /></TrilhaRoute>} />
          <Route path="/minuta/diagramas" element={<TrilhaRoute><MinutaDiagrams /></TrilhaRoute>} />
          <Route path="/minuta/revisao" element={<TrilhaRoute><ProtectedRoute><Revisao initialDoc="ri" /></ProtectedRoute></TrilhaRoute>} />

          <Route path="/regulamento/subsidio" element={<TrilhaRoute><RegSubsidio /></TrilhaRoute>} />
          <Route path="/regulamento" element={<TrilhaRoute><RegulamentoWizard /></TrilhaRoute>} />
          <Route path="/regulamento/diagramas" element={<TrilhaRoute><RegDiagramas /></TrilhaRoute>} />
          <Route path="/regulamento/revisao" element={<TrilhaRoute><ProtectedRoute><Revisao initialDoc="reg" /></ProtectedRoute></TrilhaRoute>} />

          <Route path="/comparar" element={<TrilhaRoute><MinutaComparator /></TrilhaRoute>} />
          <Route path="/minuta-diagramas" element={<TrilhaRoute><MinutaDiagrams /></TrilhaRoute>} />
          <Route path="/minuta/deliberacao" element={<TrilhaRoute><MinutaDeliberacao /></TrilhaRoute>} />
          <Route path="/minuta/comparar" element={<TrilhaRoute><MinutaRIComparator /></TrilhaRoute>} />
          <Route path="/minuta/comparativo-ri" element={<TrilhaRoute><RIComparator /></TrilhaRoute>} />
          <Route path="/regulamento/comparar" element={<TrilhaRoute><RegulamentoComparator /></TrilhaRoute>} />
          <Route path="/revisao" element={<TrilhaRoute><ProtectedRoute><Revisao /></ProtectedRoute></TrilhaRoute>} />
```

(As rotas do bloco "Geral" e `/login`, `/cadastro`, `/acessos` permanecem exatamente como estão.)

- [ ] **Step 4: Estilo do placeholder**

Acrescentar ao final de `src/index.css`:

```css
/* Placeholder "Em construção" (trilhas no cenário LOB atual) */
.em-construcao { max-width: 640px; margin: 48px auto; padding: 0 24px; text-align: center; }
.em-construcao h1 { color: var(--navy-700, #2a3a55); margin-bottom: 12px; }
.em-construcao p { color: var(--navy-600, #45526e); line-height: 1.6; }
.em-construcao-dica { margin-top: 16px; font-size: 14px; color: var(--navy-500, #6b7793); }
```

- [ ] **Step 5: Validar o isolamento ponta a ponta (Playwright)**

Com `npm run dev` no ar, abrir `http://localhost:5173` no Playwright e comprovar:
1. Cenário **futura** + navegar em `/minuta`: a minuta real carrega normalmente (screenshot).
2. Trocar para **atual** (seletor): a mesma tela `/minuta` passa a mostrar "Em construção" (screenshot); a URL contém `?cenario=atual`.
3. Ainda em **atual**, abrir `/legislacoes` (bloco Geral): o Acervo carrega normalmente — prova de que o compartilhado não foi afetado.
4. Voltar para **futura**: `/minuta` volta a mostrar a minuta real, idêntica ao passo 1.

Expected: os quatro pontos confirmados, com screenshots colados lado a lado (futura real × atual placeholder).

- [ ] **Step 6: Rodar a suíte e commitar**

Run: `npm test`
Expected: PASS (nenhuma regressão nos testes de lógica pura).

```bash
git add src/components/EmConstrucao.jsx src/App.jsx src/index.css
git commit -m "feat(cenario): trilhas mostram 'Em construção' no cenário atual (isolamento sem misturar dados)"
```

---

## Self-Review (cobertura do spec)

- **Chave no topo que troca todo o sistema** → Tasks 2, 3, 4. ✅
- **Cenário na URL + persistência** → Task 2 (sync) + validado na Task 3. ✅
- **Menu com rótulos idênticos** → inalterado (constraint). ✅
- **LOB futura idêntica a hoje** → nenhum dado movido; futura renderiza as páginas reais sem mudança de fetch (Task 4). ✅
- **LOB atual isolada / não mistura** → `TrilhaRoute` mostra placeholder; nenhum fetch de dados no cenário atual (Task 4). ✅
- **Acervo dos estados compartilhado** → páginas do bloco "Geral" não são envolvidas (Task 4). ✅
- **Firebase/dispositivoId por cenário** → explicitamente FORA da Fase 1 (constraint); Fase 2. ✅
- **Estrutura/dados da LOB atual** → Fase 2 (fora do escopo). ✅

Sem placeholders de plano; tipos e nomes (`cenario`, `setCenario`, `useScenario`, `TrilhaRoute`, `normalizeScenario`, `resolveScenario`, `SCENARIOS`, `DEFAULT_SCENARIO`) consistentes entre tarefas.
