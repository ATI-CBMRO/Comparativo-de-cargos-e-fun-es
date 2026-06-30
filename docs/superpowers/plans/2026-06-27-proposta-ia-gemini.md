# Proposta com IA (Gemini) — Plano de Implementação

> **For agentic workers:** REQUIRED SUB-SKILL: superpowers:subagent-driven-development ou superpowers:executing-plans. Steps usam checkbox (`- [ ]`).

**Goal:** Botão "✨ Gerar proposta com IA" na janela do dispositivo que, via função serverless segura, pede ao Gemini um texto consolidado (texto atual + sugestões relevantes), exibe a proposta e pré-preenche o campo de texto final; corrige o "Salvar e fechar".

**Architecture:** Frontend chama `POST /api/gerar-proposta`. A lógica de prompt + chamada ao Gemini vive em `api/_gerarProposta.js`, reusada por (a) a função serverless da Vercel `api/gerar-proposta.js` (produção) e (b) um middleware do Vite (dev). A chave fica em `GEMINI_API_KEY` (env do servidor / `.env` local), nunca no frontend.

**Tech Stack:** React 18, Vite 6 (middleware dev), função serverless Vercel (Node 18+, `fetch` nativo), Gemini `generateContent` REST, `node --test`.

## Global Constraints
- UI em PT-BR; sem segredos no frontend (chave só em `process.env`/`.env`, que está no `.gitignore`).
- Sem novas dependências npm (usar `fetch` nativo). Modelo padrão: `gemini-2.0-flash`.
- Proposta da IA é efêmera (não persistir); só `finalTexts` é salvo (já existe).
- Commits pequenos, mensagens `tipo: descrição`.

---

### Task 1: Núcleo compartilhado — prompt + chamada ao Gemini (com testes)

**Files:**
- Create: `api/_gerarProposta.js`
- Test: `api/_gerarProposta.test.js`

**Interfaces:**
- Produces:
  - `buildPrompt(textoAtual: string, sugestoes: string[]) => string`
  - `parseGeminiResposta(json: object) => string` (lança se vazio/inesperado)
  - `gerarPropostaCore({ textoAtual, sugestoes, apiKey, model? }) => Promise<string>`

- [ ] **Step 1: Escrever o teste que falha** — `api/_gerarProposta.test.js`:

```js
import { test } from 'node:test'
import assert from 'node:assert/strict'
import { buildPrompt, parseGeminiResposta } from './_gerarProposta.js'

test('buildPrompt inclui o texto atual e cada sugestão', () => {
  const p = buildPrompt('Art. 5º texto base.', ['trocar X por Y', 'incluir Z'])
  assert.match(p, /Art\. 5º texto base\./)
  assert.match(p, /trocar X por Y/)
  assert.match(p, /incluir Z/)
  assert.match(p, /APENAS/i) // instrução de responder só o texto
})

test('parseGeminiResposta extrai o texto da resposta', () => {
  const json = { candidates: [{ content: { parts: [{ text: '  Art. 5º final.  ' }] } }] }
  assert.equal(parseGeminiResposta(json), 'Art. 5º final.')
})

test('parseGeminiResposta lança quando vazio', () => {
  assert.throws(() => parseGeminiResposta({}), /vazia|inesperado/i)
})
```

- [ ] **Step 2: Rodar e confirmar falha** — Run: `node --test api/_gerarProposta.test.js` → Expected: FALHA (módulo inexistente).

- [ ] **Step 3: Implementar `api/_gerarProposta.js`**

```js
// Lógica compartilhada (sem framework) para gerar a proposta via Gemini.
// Usada pela função serverless (Vercel) e pelo middleware de dev (Vite).
const DEFAULT_MODEL = 'gemini-2.0-flash'

export function buildPrompt(textoAtual, sugestoes) {
  const lista = (sugestoes ?? [])
    .map((s, i) => `${i + 1}. ${String(s).trim()}`)
    .join('\n')
  return [
    'Você é um redator legislativo experiente. Reescreva o dispositivo legal abaixo,',
    'incorporando as sugestões pertinentes e preservando a técnica e o estilo legislativo.',
    'Responda APENAS com o texto final do dispositivo, sem comentários, títulos ou aspas.',
    '',
    'TEXTO ATUAL DO DISPOSITIVO:',
    String(textoAtual ?? '').trim(),
    '',
    'SUGESTÕES RELEVANTES A CONSIDERAR:',
    lista || '(nenhuma)',
  ].join('\n')
}

export function parseGeminiResposta(json) {
  const txt = json?.candidates?.[0]?.content?.parts?.[0]?.text
  if (!txt || !String(txt).trim()) {
    throw new Error('Resposta da IA vazia ou em formato inesperado.')
  }
  return String(txt).trim()
}

export async function gerarPropostaCore({ textoAtual, sugestoes, apiKey, model = DEFAULT_MODEL }) {
  if (!apiKey) throw new Error('Chave do Gemini ausente no servidor (GEMINI_API_KEY).')
  const prompt = buildPrompt(textoAtual, sugestoes)
  const url = `https://generativelanguage.googleapis.com/v1beta/models/${model}:generateContent?key=${apiKey}`
  const resp = await fetch(url, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ contents: [{ parts: [{ text: prompt }] }] }),
  })
  if (!resp.ok) {
    const detalhe = await resp.text().catch(() => '')
    throw new Error(`Gemini respondeu ${resp.status}: ${detalhe.slice(0, 200)}`)
  }
  return parseGeminiResposta(await resp.json())
}
```

- [ ] **Step 4: Rodar e confirmar que passa** — Run: `node --test api/_gerarProposta.test.js` → Expected: PASS (3 testes).

- [ ] **Step 5: Commit**
```bash
git add api/_gerarProposta.js api/_gerarProposta.test.js
git commit -m "feat: núcleo da geração de proposta via Gemini (prompt + chamada) com testes"
```

---

### Task 2: Endpoint (Vercel + dev) e cliente do frontend

**Files:**
- Create: `api/gerar-proposta.js` (função serverless Vercel)
- Create: `src/lib/gerarProposta.js` (cliente do frontend)
- Modify: `vite.config.js` (middleware dev `/api/gerar-proposta` + `loadEnv`)
- Modify: `.env.example` (adicionar `GEMINI_API_KEY`)
- Manual: adicionar `GEMINI_API_KEY=<chave>` ao `.env` local (não versionado)

**Interfaces:**
- Consumes: `gerarPropostaCore` de `api/_gerarProposta.js`.
- Produces: `gerarProposta({ textoAtual, sugestoesRelevantes: string[] }) => Promise<string>` (frontend).
- Contrato HTTP: `POST /api/gerar-proposta` body `{ textoAtual, sugestoes }` → `200 { proposta }` ou `{ error }`.

- [ ] **Step 1: Criar a função serverless `api/gerar-proposta.js`**

```js
import { gerarPropostaCore } from './_gerarProposta.js'

export default async function handler(req, res) {
  if (req.method !== 'POST') {
    res.status(405).json({ error: 'Método não permitido' })
    return
  }
  try {
    const { textoAtual, sugestoes } = req.body ?? {}
    const proposta = await gerarPropostaCore({
      textoAtual, sugestoes, apiKey: process.env.GEMINI_API_KEY,
    })
    res.status(200).json({ proposta })
  } catch (e) {
    res.status(500).json({ error: String(e?.message || e) })
  }
}
```

- [ ] **Step 2: Criar o cliente `src/lib/gerarProposta.js`**

```js
// Chama o endpoint seguro que fala com o Gemini. O frontend nunca vê a chave.
export async function gerarProposta({ textoAtual, sugestoesRelevantes }) {
  const resp = await fetch('/api/gerar-proposta', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ textoAtual, sugestoes: sugestoesRelevantes }),
  })
  const json = await resp.json().catch(() => ({}))
  if (!resp.ok) throw new Error(json.error || 'Falha ao gerar proposta.')
  return json.proposta
}
```

- [ ] **Step 3: Adicionar o middleware de dev ao `vite.config.js`**

Trocar os imports do topo e o `export default` por (mantendo `serveDatabase`/`copyDatabaseOnBuild` como estão):
```js
import { defineConfig, loadEnv } from 'vite'
import react from '@vitejs/plugin-react'
import path from 'path'
import fs from 'fs'
import { gerarPropostaCore } from './api/_gerarProposta.js'
```
Acrescentar o plugin (perto dos outros):
```js
// Em desenvolvimento, atende /api/gerar-proposta com a MESMA lógica da função da Vercel.
function geminiDevApi(apiKey) {
  return {
    name: 'gemini-dev-api',
    configureServer(server) {
      server.middlewares.use('/api/gerar-proposta', async (req, res, next) => {
        if (req.method !== 'POST') return next()
        try {
          let body = ''
          for await (const chunk of req) body += chunk
          const { textoAtual, sugestoes } = JSON.parse(body || '{}')
          const proposta = await gerarPropostaCore({ textoAtual, sugestoes, apiKey })
          res.setHeader('Content-Type', 'application/json; charset=utf-8')
          res.end(JSON.stringify({ proposta }))
        } catch (e) {
          res.statusCode = 500
          res.setHeader('Content-Type', 'application/json; charset=utf-8')
          res.end(JSON.stringify({ error: String(e?.message || e) }))
        }
      })
    },
  }
}
```
Trocar o `export default` por forma de função (para usar `loadEnv`):
```js
export default defineConfig(({ mode }) => {
  const env = loadEnv(mode, process.cwd(), '')
  return {
    plugins: [react(), serveDatabase(), copyDatabaseOnBuild(), geminiDevApi(env.GEMINI_API_KEY)],
    server: { port: 5173 },
  }
})
```

- [ ] **Step 4: Atualizar `.env.example`** — acrescentar ao final:
```
# Chave da API do Gemini (Google AI Studio) — usada SÓ no servidor (função/Vite dev).
GEMINI_API_KEY=
```

- [ ] **Step 5: Build** — Run: `npm run build` → Expected: sem erros (o middleware só roda no dev; o build não quebra).

- [ ] **Step 6: Commit**
```bash
git add api/gerar-proposta.js src/lib/gerarProposta.js vite.config.js .env.example
git commit -m "feat: endpoint seguro /api/gerar-proposta (Vercel + dev) e cliente do front"
```

---

### Task 3: Janela do dispositivo — texto atual, botão gerar e correção do fechar

**Files:**
- Modify: `src/components/RevisaoModal.jsx`
- Modify: `src/pages/Revisao.jsx`
- Modify: `src/index.css`

**Interfaces:**
- Consumes: `gerarProposta` (via prop `onGerarProposta` vinda da página).
- Modal ganha props: `onGerarProposta({ textoAtual, sugestoes }) => Promise<string>`.

- [ ] **Step 1: Editar `src/components/RevisaoModal.jsx`** — adicionar estados e a seção de IA. No topo do componente, junto aos outros `useState`:

```jsx
  const [propostaIA, setPropostaIA] = useState(null)
  const [gerando, setGerando] = useState(false)
  const [erroIA, setErroIA] = useState('')
```
Adicionar (dentro do componente, antes do `return`) a função e o cálculo das relevantes:
```jsx
  const relevantes = suggestions.filter(s => (s.adminStatus ?? 'pendente') === 'relevante')

  const gerar = async () => {
    setErroIA(''); setGerando(true)
    try {
      const proposta = await onGerarProposta({
        textoAtual: dispositivo.trecho,
        sugestoes: relevantes.map(s => s.texto),
      })
      setPropostaIA(proposta)
      setFinal(proposta)
    } catch (e) {
      setErroIA(e.message || 'Não foi possível gerar agora. Tente de novo.')
    } finally {
      setGerando(false)
    }
  }
```
Na seção `{(isAdmin || finalText) && (...)}` do "Texto final", inserir ANTES do textarea (apenas para admin) o bloco de IA:
```jsx
            {isAdmin && (
              <div className="rev-ia">
                <div className="rev-ia-atual">
                  <span className="label">Texto atual</span>
                  {dispositivo.trecho}
                </div>
                <button className="rev-ia-btn" onClick={gerar} disabled={gerando || relevantes.length === 0}
                  title={relevantes.length === 0 ? 'Marque ao menos uma sugestão como relevante' : ''}>
                  {gerando ? 'Gerando…' : '✨ Gerar proposta com IA'}
                </button>
                {relevantes.length === 0 && (
                  <span className="rev-ia-dica">Marque ao menos uma sugestão como relevante para gerar.</span>
                )}
                {erroIA && <div className="login-erro">{erroIA}</div>}
                {propostaIA && (
                  <div className="rev-ia-proposta">
                    <span className="label">✨ Proposta da IA (referência)</span>
                    {propostaIA}
                  </div>
                )}
              </div>
            )}
```
Corrigir o "Salvar e fechar" para fechar a janela após salvar:
```jsx
                  <button className="rev-final-btn fechar"
                    onClick={async () => { await onSaveFinal(final, 'fechado'); onClose() }}>Salvar e fechar</button>
```

- [ ] **Step 2: Editar `src/pages/Revisao.jsx`** — importar e passar a prop:

No bloco de imports do reviewData/gerarProposta, adicionar:
```jsx
import { gerarProposta } from '../lib/gerarProposta.js'
```
No `<RevisaoModal ... />`, adicionar a prop:
```jsx
          onGerarProposta={({ textoAtual, sugestoes }) => gerarProposta({ textoAtual, sugestoesRelevantes: sugestoes })}
```

- [ ] **Step 3: Estilos ao fim de `src/index.css`**
```css
/* ===== Revisão: geração com IA ===== */
.rev-ia { margin-bottom: 12px; }
.rev-ia-atual { font-size: 13px; color: #3a4866; background: #f7f9fc; border: 1px solid #d7deea; border-radius: 8px; padding: 8px 10px; margin-bottom: 8px; }
.rev-ia-atual .label, .rev-ia-proposta .label { display: block; font-size: 11px; text-transform: uppercase; letter-spacing: .04em; margin-bottom: 4px; }
.rev-ia-atual .label { color: #5a667f; }
.rev-ia-btn { background: #6b3fc8; color: #fff; border: none; border-radius: 8px; padding: 8px 16px; font-weight: 700; font-size: 13px; cursor: pointer; }
.rev-ia-btn:disabled { opacity: .5; cursor: default; }
.rev-ia-dica { display: block; font-size: 12px; color: #8a93a8; margin-top: 4px; }
.rev-ia-proposta { margin-top: 10px; font-size: 13.5px; line-height: 1.6; color: #1a1a1a; background: #f6f2fc; border: 1px solid #d6c8f0; border-radius: 8px; padding: 10px 12px; }
.rev-ia-proposta .label { color: #6b3fc8; }
```

- [ ] **Step 4: Build** — Run: `npm run build` → Expected: sem erros.

- [ ] **Step 5: Verificação manual** (com `GEMINI_API_KEY` no `.env` e `npm run dev`):
- Como admin, abrir um dispositivo, marcar 1+ sugestão como **relevante**.
- Clicar **✨ Gerar proposta com IA** → aparece "Gerando…", depois a **Proposta da IA** e o campo **Texto final** já preenchido.
- Editar o texto, clicar **Salvar e fechar** → a janela **fecha** e o dispositivo fica "fechado" (traço verde + progresso sobe).
- Sem nenhuma relevante → botão fica desabilitado com a dica.
- Reabrir o dispositivo → o texto final persiste.

- [ ] **Step 6: Commit**
```bash
git add src/components/RevisaoModal.jsx src/pages/Revisao.jsx src/index.css
git commit -m "feat: botão Gerar proposta com IA na janela + texto atual + corrige Salvar e fechar"
```

---

## Self-Review (preenchido)
- Base = texto atual + relevantes → Task 3 (filtra `adminStatus==='relevante'`, envia `dispositivo.trecho`). ✔
- Botão automático (só admin) + 3 estágios (atual/proposta/final) → Task 3. ✔
- Função segura Vercel + dev, chave server-side → Tasks 1–2. ✔
- Pré-preenche texto final + corrige Salvar e fechar → Task 3. ✔
- Erros (sem relevante, falha da IA, sem chave) → Tasks 1–3. ✔
- Sem persistir proposta crua; sem dependências novas; modelo `gemini-2.0-flash`. ✔
- Nomes consistentes: `gerarPropostaCore`/`buildPrompt`/`parseGeminiResposta` (núcleo); `gerarProposta({textoAtual,sugestoesRelevantes})` (front); prop `onGerarProposta({textoAtual,sugestoes})` (modal). ✔
- Fora de escopo (futuro): diff colorido, proteção do endpoint por token, geração em lote. ✔
```
