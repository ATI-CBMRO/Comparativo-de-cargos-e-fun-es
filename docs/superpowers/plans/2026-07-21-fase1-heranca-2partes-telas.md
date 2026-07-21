# Herdar as 2 Partes no Subsídio e na Revisão do Regulamento — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** `RegulamentoComparator` (aba Regulamento do Subsídio) e `Revisao` (modo Regulamento) passam a mostrar a divisão Parte I — Geral / Parte II — do Serviço, igual ao Wizard e ao `.docx`. `RegDiagramas` fica fora (bloqueado por dado ausente, não relacionado a esta pendência).

**Architecture:** Reusa `src/lib/regulamentoPartes.js` (já existe, criado na Fase 1: `PARTE_HEADERS`, `parteByChapterTitle`). Em `RegulamentoComparator`, a função `groupChapters` passa a agrupar em 2 níveis (Parte → grupo temático). Em `Revisao`, insere a mesma faixa de Parte que o Wizard já usa, calculada uma vez via `useMemo`.

**Tech Stack:** React/Vite, `node --test`.

**Spec:** `docs/superpowers/specs/2026-07-21-fase1-heranca-2partes-telas-design.md`.

## Global Constraints
- Comunicação/UI em pt-BR.
- NÃO tocar no Regimento Interno (`MinutaWizard.jsx`, `MinutaRIComparator.jsx`, modo `ri` de `Revisao.jsx`) — para estruturas sem campo `parte`, a lógica nova deve ser no-op total (mesma garantia já provada na Fase 1).
- NÃO gerar `commandChart` nem tocar em `RegDiagramas.jsx` — fora de escopo.
- `node --test` deve terminar verde em todo commit.
- Caminhos absolutos no Bash, sem `cd ... &&`.

---

### Task 1: `RegulamentoComparator` — agrupamento por Parte

**Files:**
- Modify: `src/pages/RegulamentoComparator.jsx` (`groupChapters` ~linha 18; sidebar de navegação ~linha 129 `filteredGroups.map`)

**Interfaces:**
- Consumes: `ch.parte` (campo já presente em cada capítulo de `regulamento_structure.json` desde a Fase 1).
- Produces: nenhuma exportação nova — mudança interna de UI.

- [ ] **Step 1: Reescrever `groupChapters` para 2 níveis** — substituir a função inteira (linhas 18-31):

```jsx
import { PARTE_HEADERS } from '../lib/regulamentoPartes.js'

function groupChapters(chapters) {
  const porParte = new Map()
  for (const ch of chapters) {
    const parte = ch.parte ?? 'geral' // RI/estruturas antigas sem `parte` caem em 'geral' (no-op visual, já que hoje só o Regulamento usa este componente)
    if (!porParte.has(parte)) porParte.set(parte, { parte, label: PARTE_HEADERS[parte] ?? null, groups: [] })
    const bucket = porParte.get(parte)
    const name = ch.group || 'Outros'
    let g = bucket.groups.find(x => x.name === name)
    if (!g) { g = { name, chapters: [] }; bucket.groups.push(g) }
    g.chapters.push(ch)
  }
  // Ordem: geral antes de servico (mesma ordem já usada no JSON/Wizard).
  return [...porParte.values()].sort((a, b) => (a.parte === 'geral' ? 0 : 1) - (b.parte === 'geral' ? 0 : 1))
}
```

(Import `PARTE_HEADERS` no topo do arquivo, junto aos demais imports de `../lib/`.)

- [ ] **Step 2: Ajustar `filteredGroups`** — o filtro de busca hoje itera `groups` (lista plana de
grupos temáticos); agora `groups` é uma lista de "partes", cada uma com sua lista de `groups`
internos. Substituir o `useMemo` de `filteredGroups` (linhas ~48-53) por:

```jsx
  const filteredGroups = useMemo(() => {
    if (!filter.trim()) return groups
    const q = filter.trim().toLowerCase()
    return groups
      .map(p => ({
        ...p,
        groups: p.groups
          .map(g => ({ ...g, chapters: g.chapters.filter(c => c.chapterTitle.toLowerCase().includes(q)) }))
          .filter(g => g.chapters.length > 0),
      }))
      .filter(p => p.groups.length > 0)
  }, [groups, filter])
```

- [ ] **Step 3: Ajustar o render da sidebar** — substituir o bloco `{filteredGroups.map(g => (...))}`
(dentro do `<aside>`, logo após a busca) por:

```jsx
              {filteredGroups.map(p => (
                <div key={p.parte} style={{ marginBottom: 10 }}>
                  {p.label && (
                    <div style={{ fontWeight: 800, color: 'var(--cbm-red-700)', fontSize: 10.5, letterSpacing: 0.5, padding: '6px 6px 2px' }}>
                      {p.label}
                    </div>
                  )}
                  {p.groups.map(g => (
                    <div key={g.name} style={{ marginBottom: 6 }}>
                      <div className="nav-section-label" style={{ padding: '6px 6px 4px' }}>{g.name}</div>
                      {g.chapters.map(c => (
                        <button
                          key={c.id}
                          onClick={() => setChapterId(c.id)}
                          className={`nav-item rg-nav-item${c.id === chapterId ? ' active' : ''}`}
                          title={c.chapterTitle}
                        >
                          <span className="nav-item-label">{c.chapterTitle}</span>
                        </button>
                      ))}
                    </div>
                  ))}
                </div>
              ))}
              {filteredGroups.every(p => p.groups.length === 0) && (
                <div style={{ padding: 12, fontSize: 12.5, color: 'var(--text-muted)', textAlign: 'center' }}>Nenhum capítulo encontrado.</div>
              )}
```

(A condição do "Nenhum capítulo encontrado" mudou de `filteredGroups.length === 0` para
`filteredGroups.every(p => p.groups.length === 0)`, já que agora `filteredGroups` é a lista de
Partes, não de grupos.)

- [ ] **Step 4: Verificar build e suíte**

Run: `npm run build`
Expected: build verde, sem erro de import/JSX.

Run: `node --test`
Expected: `pass 110 / fail 0` (nenhum teste JS cobre este componente React diretamente — a
suíte não pode regredir).

- [ ] **Step 5: Commit**

```bash
git add src/pages/RegulamentoComparator.jsx
git commit -m "feat(regulamento): Subsídio agrupa capítulos por Parte (I-Geral / II-Serviço)

Co-Authored-By: Claude <noreply@anthropic.com>"
```

---

### Task 2: `Revisao` (modo Regulamento) — faixa de Parte

**Files:**
- Modify: `src/pages/Revisao.jsx` (imports ~linha 1-22; render de artigos ~linha 221 onde insere "CAPÍTULO N")

**Interfaces:**
- Consumes: `PARTE_HEADERS`, `parteByChapterTitle` de `../lib/regulamentoPartes.js` (Fase 1).

- [ ] **Step 1: Importar o helper** — junto aos demais imports de `../lib/`:

```jsx
import { PARTE_HEADERS, parteByChapterTitle } from '../lib/regulamentoPartes.js'
```

- [ ] **Step 2: Calcular o mapa de Partes** — dentro do componente `Revisao`, junto aos outros
`useMemo`/`useEffect` (procurar onde `data` já é usado em outro `useMemo`, ex. próximo à
definição de `articles` — usar Read para localizar o ponto exato antes de editar):

```jsx
  const parteDe = useMemo(() => (docId === 'reg' ? parteByChapterTitle(data) : {}), [docId, data])
```

- [ ] **Step 3: Emitir a faixa de Parte antes da faixa de Capítulo** — o padrão EXATO já existe
em `src/pages/RegulamentoWizard.jsx` (linhas 404-417): uma IIFE que envolve o `.map` dos
artigos, com uma variável `ultimaParte` declarada com `let` (fora do JSX, dentro da IIFE) que
rastreia a última Parte vista, emitindo a faixa só quando `parte !== ultimaParte`:

```jsx
{
  let ultimaParte = null
  return articles.map(art => {
    const parte = art.chapterTitle ? parteDe[art.chapterTitle] : null
    const faixa = parte && parte !== ultimaParte ? PARTE_HEADERS[parte] : null
    if (parte) ultimaParte = parte
    return (
      <div key={art.number}>
        {faixa && (
          <div style={{
            textAlign: 'center', fontWeight: 800, fontSize: 15, letterSpacing: 1,
            color: 'var(--cbm-red-700)', borderTop: '2px solid var(--cbm-red-700)',
            borderBottom: '2px solid var(--cbm-red-700)', padding: '8px 0', margin: '20px 0 12px',
          }}>{faixa}</div>
        )}
        {art.chapterTitle && (
          /* ... o bloco existente de "CAPÍTULO N" continua aqui, sem alteração ... */
        )}
        {/* ... resto da renderização do artigo, sem alteração ... */}
      </div>
    )
  })
}
```

Use Read em `src/pages/Revisao.jsx` para localizar o `.map` real de artigos (pode não estar
envolto em `<div key={art.number}>` hoje — adapte a estrutura ENVOLVENTE existente, só
inserindo a IIFE com `ultimaParte` por fora e o bloco de `faixa` como primeiro filho, sem
mudar o que já é renderizado para cada artigo. Este é o MESMO padrão do Wizard — copie a
lógica de `ultimaParte`/`faixa` literalmente, adaptando só a estrutura de wrapper ao que já
existe em `Revisao.jsx`.

- [ ] **Step 4: Verificar que o modo RI não muda** — para `docId==='ri'`, `parteDe` é `{}` (o
guard do Step 2), logo `parteDe[art.chapterTitle]` é sempre `undefined` e a faixa nunca
aparece — no-op total, igual ao `.docx`.

- [ ] **Step 5: Prova visual** — subir `npm run dev`, logar, navegar a `/regulamento/revisao`,
rolar o documento e CONFIRMAR: a faixa de Parte aparece exatamente 2 vezes no documento inteiro
(uma para cada Parte), não a cada capítulo. Depois, navegar a `/minuta/revisao` (RI) e
confirmar que NADA mudou visualmente ali (prova de não-regressão do Regimento Interno).

Run: `node --test`
Expected: `pass 110 / fail 0`.

- [ ] **Step 6: Commit**

```bash
git add src/pages/Revisao.jsx
git commit -m "feat(regulamento): Revisão do Regulamento exibe as faixas de Parte I/II

Co-Authored-By: Claude <noreply@anthropic.com>"
```

---

### Task 3: Prova final + registro

**Files:**
- Modify: `.claude/PENDENCIAS.md`
- Evidence: screenshots

**Interfaces:**
- Consumes: Tasks 1-2.

- [ ] **Step 1: Prova visual consolidada** — com o dev server no ar e logado: capturar
screenshot de `/regulamento/subsidio` (aba Regulamento) mostrando "PARTE I — GERAL"/"PARTE II —
DO SERVIÇO" no sumário lateral; capturar screenshot de `/regulamento/revisao` mostrando a faixa
de Parte no documento. Abrir ambos no Preview.

- [ ] **Step 2: Registrar no backlog** — em `.claude/PENDENCIAS.md`, mover para "Concluído":
"Regulamento — herdar 2 Partes no Subsídio e na Revisão (RegDiagramas segue fora, bloqueado por
`commandChart` ausente — pendência própria, já existia)". Adicionar/confirmar como pendência
separada: "Regulamento — Diagramas: gerar `commandChart` do Regulamento (bloqueia RegDiagramas
há tempo, não é sobre as 2 Partes)".

- [ ] **Step 3: Commit**

```bash
git add .claude/PENDENCIAS.md
git commit -m "chore(handoff): 2 Partes herdadas no Subsídio e Revisão do Regulamento

Co-Authored-By: Claude <noreply@anthropic.com>"
```

- [ ] **Step 4: Atualizar o Diário de Construção no Obsidian** — acrescentar à nota
`Codebases/Comparativo-de-cargos-e-funcoes/Diário de Construção da Minuta — rumo à
apresentação ao Comando.md`: este marco na linha do tempo.
