# Ver referências no popup de Revisão — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** No popup de Revisão, mostrar um botão retrátil "Ver referências (N)" que exibe os
excertos de outros estados (Bloco D / `alternatives`) do capítulo ao qual o dispositivo aberto
pertence.

**Architecture:** Extrai a UI de chips-por-estado + excertos que já existe inline em
`ConferenciaLinear.jsx` para um componente compartilhado `AlternativesPanel.jsx`. `Revisao.jsx`
calcula o `chapterId` do dispositivo aberto e busca `alternatives` no JSON já carregado.
`RevisaoModal.jsx` recebe essa prop e mostra o botão + painel.

**Tech Stack:** React (Vite SPA), sem estado novo em Firebase — tudo client-side a partir do
JSON já buscado.

## Global Constraints

- `alternatives` é sempre por CAPÍTULO (órgão/tema), nunca por dispositivo individual — não
  inventar granularidade mais fina.
- A extração de `ConferenciaLinear.jsx` NÃO pode mudar o comportamento visual/funcional dessa
  tela — é refatoração pura, não feature nova ali.
- `N === 0` (capítulo sem `alternatives`): botão desabilitado, nunca escondido.
- Sem teste unitário novo para `AlternativesPanel.jsx` (apresentação pura) — a suíte
  `node --test` deve continuar em 132/132 depois de cada task.

---

### Task 1: Extrair `AlternativesPanel`/`MatchBadge` para componente compartilhado

**Files:**
- Create: `src/components/AlternativesPanel.jsx`
- Modify: `src/pages/ConferenciaLinear.jsx:1-25` (imports + remoção do `MatchBadge` local) e
  `src/pages/ConferenciaLinear.jsx:157-192` (bloco de chips+excertos substituído pela chamada
  ao componente)

**Interfaces:**
- Produces: `export function MatchBadge({ match })` e
  `export function AlternativesPanel({ alternatives, selectedUf, onSelectUf })` em
  `src/components/AlternativesPanel.jsx`. `alternatives` é o objeto
  `{ [uf]: { name, abbr, docLabel, excerpts: [{ heading, caput, dispositivos, source, match }] } }`
  (mesmo shape de `minuta_structure.json`/`regulamento_structure.json`). `selectedUf` é a uf
  atualmente selecionada (`string|null|undefined` — se `undefined`/`null`, o componente usa a
  primeira uf disponível). `onSelectUf(uf: string)` é chamado quando o usuário clica num chip.

- [ ] **Step 1: Criar `src/components/AlternativesPanel.jsx`**

```jsx
import { useMemo } from 'react'
import { renderFriendlyText, List } from '../lib/comparatorRender.jsx'

export function MatchBadge({ match }) {
  const cfg = {
    exata: { cls: 'rg-badge-exata', label: 'exata' },
    parcial: { cls: 'rg-badge-parcial', label: 'parcial' },
    tematica: { cls: 'rg-badge-tematica', label: 'temática' },
    auto: { cls: 'rg-badge-tematica', label: 'auto' },
  }[match] ?? { cls: 'rg-badge-tematica', label: match || '—' }
  return <span className={`rg-badge ${cfg.cls}`}>{cfg.label}</span>
}

export function AlternativesPanel({ alternatives, selectedUf, onSelectUf }) {
  const altStates = useMemo(() => (
    Object.entries(alternatives ?? {})
      .map(([uf, alt]) => ({ uf, ...alt }))
      .sort((a, b) => a.name.localeCompare(b.name, 'pt'))
  ), [alternatives])

  if (altStates.length === 0) {
    return (
      <div className="card" style={{ padding: 16, textAlign: 'center', color: 'var(--text-muted)' }}>
        Nenhuma referência disponível.
      </div>
    )
  }

  const effectiveUf = selectedUf ?? altStates[0].uf
  const selectedAlt = altStates.find(s => s.uf === effectiveUf) || altStates[0]

  return (
    <>
      <div className="oc-state-chips" style={{ position: 'static', padding: '0 0 10px' }}>
        <span className="oc-state-chips-label">Estado:</span>
        {altStates.map(s => (
          <button
            key={s.uf}
            className={`oc-state-chip${s.uf === effectiveUf ? ' active' : ''}`}
            onClick={() => onSelectUf(s.uf)}
            title={`${s.name} · ${s.docLabel}`}
          >
            {s.abbr}
          </button>
        ))}
      </div>
      {selectedAlt.excerpts.length > 0
        ? selectedAlt.excerpts.map((ex, i) => (
            <div className="rg-article" key={i}>
              {ex.heading && <div className="rg-heading">{ex.heading}</div>}
              <p className="rg-caput">{renderFriendlyText(ex.caput)}</p>
              {ex.dispositivos?.length > 0 && <List items={ex.dispositivos} />}
              <div className="rg-article-foot">
                {ex.source ? <span className="rg-source">{ex.source}</span> : <span />}
                {ex.match && <MatchBadge match={ex.match} />}
              </div>
            </div>
          ))
        : <p className="rg-empty">Sem trechos para este estado.</p>}
    </>
  )
}
```

- [ ] **Step 2: Atualizar `ConferenciaLinear.jsx` para usar o componente extraído**

Substituir o import no topo do arquivo (linhas 1-12):

```jsx
import { useEffect, useMemo, useState } from 'react'
import { ListChecks, Check, AlertTriangle } from 'lucide-react'
import { useScenario } from '../context/ScenarioContext.jsx'
import { useAuth } from '../lib/auth.jsx'
import { scenarioDbUrl } from '../lib/scenario.js'
import { fetchJson } from '../lib/dataCache.js'
import { LoadingState, ErrorState } from '../components/Status.jsx'
import { renderFriendlyText } from '../lib/comparatorRender.jsx'
import { buildConferencia } from '../lib/conferencia.js'
import { confKey, mergeStatus } from '../lib/conferenciaStatus.js'
import { subscribeConferencia, saveConferenciaStatus } from '../lib/conferenciaData.js'
import { articleLabel, romanize } from '../lib/minutaArticles.js'
import { AlternativesPanel } from '../components/AlternativesPanel.jsx'
```

(`List` sai — só era usado dentro do bloco de excertos que agora vive em `AlternativesPanel`;
`MatchBadge` sai também, já que a função local some no próximo passo.)

Remover a função `MatchBadge` local (linhas 17-25 do arquivo original — o bloco
`function MatchBadge({ match }) { ... }` inteiro, incluindo a linha em branco antes de
`export default function ConferenciaLinear`).

Substituir o corpo de `ConferenciaItem` (o `<div className="rg-col no-print" ...>` inteiro,
que hoje calcula `altStates`/`selectedAlt` e renderiza chips+excertos manualmente) por:

```jsx
function ConferenciaItem({ item, idx, status, onStatus, ufSel, setUfSel }) {
  const { dispositivo, chapterTitle, chapterId, alternatives } = item

  return (
    <div className={`card conf-item${status === 'ok' ? ' conf-item-ok' : status === 'div' ? ' conf-item-div' : ''}`} style={{ marginBottom: 14, padding: 16 }}>
      {chapterTitle && <div className="rg-heading">{chapterTitle}</div>}
      <div className="rg-columns" style={{ display: 'flex', gap: 16, alignItems: 'flex-start' }}>
        <div className="rg-col" style={{ flex: 1, minWidth: 0 }}>
          <div className="rg-article">
            <p className="rg-caput">
              <strong>{articleLabel(dispositivo.number)}</strong> {renderFriendlyText(dispositivo.caput)}
            </p>
            {dispositivo.incisos?.length > 0 && (
              <ul className="cc-list rg-incisos">
                {dispositivo.incisos.map((inc, i) => (
                  <li key={i}>{inc.ownMarker ? '' : `${romanize(i + 1)} - `}{renderFriendlyText(inc.text)}</li>
                ))}
              </ul>
            )}
          </div>
          <div className="conf-controls no-print">
            <button
              type="button"
              className={`btn btn-ghost${status === 'ok' ? ' active' : ''}`}
              onClick={() => onStatus(status === 'ok' ? null : 'ok')}
            >
              <Check size={15} /> Confere
            </button>
            <button
              type="button"
              className={`btn btn-ghost${status === 'div' ? ' active' : ''}`}
              onClick={() => onStatus(status === 'div' ? null : 'div')}
            >
              <AlertTriangle size={15} /> Divergente
            </button>
          </div>
        </div>

        <div className="rg-col no-print" style={{ flex: 1, minWidth: 0 }}>
          <AlternativesPanel
            alternatives={alternatives}
            selectedUf={ufSel[chapterId]}
            onSelectUf={(uf) => setUfSel(u => ({ ...u, [chapterId]: uf }))}
          />
        </div>
      </div>
    </div>
  )
}
```

- [ ] **Step 3: Rodar a suíte completa**

Run: `node --test`
Expected: `tests 132`, `pass 132`, `fail 0` (nenhum teste novo, nenhuma regressão).

- [ ] **Step 4: Prova visual da tela de Conferência (sem regressão)**

Abra `/minuta/conferencia` (RI) e `/regulamento/conferencia` (Regulamento) no navegador,
logado. Confirme visualmente: chips de estado aparecem, clicar num chip troca o trecho
mostrado, itens sem `alternatives` mostram "Nenhuma referência disponível" — comportamento
idêntico ao de antes da extração (compare com o que já está em produção, se precisar).

- [ ] **Step 5: Commit**

```bash
git add src/components/AlternativesPanel.jsx src/pages/ConferenciaLinear.jsx
git commit -m "refactor(revisao): extrai AlternativesPanel/MatchBadge de ConferenciaLinear pra componente compartilhado"
```

---

### Task 2: `Revisao.jsx` calcula e passa `alternatives` do dispositivo aberto

**Files:**
- Modify: `src/pages/Revisao.jsx` (adicionar cálculo de `alternativesAberto` e passar como
  prop pro `RevisaoModal`)

**Interfaces:**
- Consumes: `AlternativesPanel`/`MatchBadge` de `src/components/AlternativesPanel.jsx`
  (Task 1) — não usados diretamente aqui, mas confirma que o arquivo existe antes de seguir.
  `chapterIdOf` (já importado de `../lib/minutaTargets.js`), `parseDispositivoId` (já
  importado de `../lib/dispositivoId.js`). `data.chapters` é um array de objetos com `id`
  (string) e `alternatives` (objeto, pode ser `undefined`).
- Produces: prop `alternatives` (objeto `{ [uf]: {...} }`, nunca `undefined` — sempre `{}` no
  mínimo) passada pro `<RevisaoModal>`, consumida na Task 3.

- [ ] **Step 1: Adicionar o cálculo de `alternativesAberto` em `Revisao.jsx`**

Logo após a declaração de `const [regulamentoAberto, setRegulamentoAbertoState] = useState(false)`
(linha 49 do arquivo atual), adicionar:

```jsx
const alternativesAberto = useMemo(() => {
  if (!aberto || !data) return {}
  const { editId } = parseDispositivoId(aberto.id)
  const chapterId = chapterIdOf(editId)
  const chapter = data.chapters.find(c => c.id === chapterId)
  return chapter?.alternatives ?? {}
}, [aberto, data])
```

(`useMemo` já está importado no topo do arquivo, linha 1.)

- [ ] **Step 2: Passar a prop pro `RevisaoModal`**

No JSX que renderiza `<RevisaoModal ...>` (perto do final do arquivo, onde hoje tem
`dispositivo={aberto}`, `suggestions={...}`, etc.), adicionar a nova prop:

```jsx
<RevisaoModal
  dispositivo={aberto}
  alternatives={alternativesAberto}
  suggestions={grupos.get(aberto.id) ?? []}
  finalText={finalsForDoc.get(aberto.id) ?? null}
  user={user}
  onAdd={handleAdd}
  onToggleLike={(s) => toggleLike(s, user.uid)}
  onDelete={(s) => deleteSuggestion(s.id)}
  onSetStatus={(s, status) => setAdminStatus(s.id, status)}
  onSaveFinal={(texto, status) => saveFinalText(aberto.id, { texto, status, autor: { uid: user.uid, nome: user.nome } })}
  onGerarProposta={({ textoAtual, sugestoes }) => gerarProposta({ textoAtual, sugestoesRelevantes: sugestoes })}
  onClose={() => setAberto(null)}
/>
```

- [ ] **Step 3: Verificar manualmente que o cálculo aponta pro capítulo certo**

Sem teste automatizado dedicado (é fiação de props, coberta pela prova visual da Task 3).
Abra o DevTools do navegador, adicione um `console.log(chapterId, chapter?.alternatives)`
temporário dentro do `useMemo` acima, abra um dispositivo do órgão `dpo` no popup de Revisão
e confirme no console que aparece `organ:dpo` com as chaves `df`/`pa`. Remova o
`console.log` antes de seguir.

- [ ] **Step 4: Rodar a suíte completa**

Run: `node --test`
Expected: `tests 132`, `pass 132`, `fail 0`.

- [ ] **Step 5: Commit**

```bash
git add src/pages/Revisao.jsx
git commit -m "feat(revisao): calcula alternatives do capítulo do dispositivo aberto"
```

---

### Task 3: `RevisaoModal.jsx` — botão "Ver referências (N)" retrátil

**Files:**
- Modify: `src/components/RevisaoModal.jsx` (nova prop, novo estado local, novo bloco de UI)
- Modify: `src/index.css` (2 classes novas: `.rev-refs-toggle` e `.rev-refs-panel`)

**Interfaces:**
- Consumes: prop `alternatives` (objeto `{ [uf]: {...} }`, produzida na Task 2 — sempre
  presente, nunca `undefined`). `AlternativesPanel` de `src/components/AlternativesPanel.jsx`
  (Task 1), com a assinatura `AlternativesPanel({ alternatives, selectedUf, onSelectUf })`.

- [ ] **Step 1: Adicionar import e novos estados locais**

No topo de `src/components/RevisaoModal.jsx`, adicionar o import (junto aos existentes):

```jsx
import { AlternativesPanel } from './AlternativesPanel.jsx'
```

Dentro de `export default function RevisaoModal({ dispositivo, alternatives, suggestions, finalText, user, ... })`
(adicionar `alternatives` à lista de props desestruturadas), adicionar os 2 estados novos
logo após `const [erroIA, setErroIA] = useState('')` (linha 20 do arquivo atual):

```jsx
const [mostrarRefs, setMostrarRefs] = useState(false)
const [ufRef, setUfRef] = useState(null)
const numRefs = Object.keys(alternatives ?? {}).length
```

- [ ] **Step 2: Fechar/resetar o painel de referências ao trocar de dispositivo**

O `useEffect` existente (linha 22 do arquivo atual) já reresta `final` quando o dispositivo
muda:

```jsx
useEffect(() => { setFinal(finalText?.texto ?? '') }, [finalText, dispositivo.id])
```

Adicionar um segundo `useEffect` logo abaixo, para resetar o painel de referências:

```jsx
useEffect(() => { setMostrarRefs(false); setUfRef(null) }, [dispositivo.id])
```

- [ ] **Step 3: Adicionar o botão e o painel no cabeçalho do modal**

No JSX do `rev-mhead` (linhas 54-61 do arquivo atual), o bloco hoje é:

```jsx
<div className="rev-mhead">
  <div style={{ flex: 1, minWidth: 0 }}>
    <div className="rev-mhead-lbl">● Em discussão</div>
    <div className="rev-mhead-ref">{dispositivo.label}</div>
    <div className="rev-discussao">{dispositivo.trecho}</div>
  </div>
  <button className="rev-modal-x" onClick={onClose} aria-label="Fechar">✕</button>
</div>
```

Substituir por:

```jsx
<div className="rev-mhead">
  <div style={{ flex: 1, minWidth: 0 }}>
    <div className="rev-mhead-lbl">● Em discussão</div>
    <div className="rev-mhead-ref">{dispositivo.label}</div>
    <div className="rev-discussao">{dispositivo.trecho}</div>
    <button
      type="button"
      className="rev-refs-toggle"
      disabled={numRefs === 0}
      title={numRefs === 0 ? 'Nenhuma referência de outro estado capturada para este órgão/tema ainda' : ''}
      onClick={() => setMostrarRefs(v => !v)}
    >
      {mostrarRefs ? 'Ocultar referências' : `Ver referências (${numRefs})`}
    </button>
  </div>
  <button className="rev-modal-x" onClick={onClose} aria-label="Fechar">✕</button>
</div>
{mostrarRefs && numRefs > 0 && (
  <div className="rev-refs-panel">
    <AlternativesPanel alternatives={alternatives} selectedUf={ufRef} onSelectUf={setUfRef} />
  </div>
)}
```

- [ ] **Step 4: Adicionar as 2 classes CSS novas**

Em `src/index.css`, logo após a linha `.rev-modal-x { ... }` (linha 2417 do arquivo atual),
adicionar:

```css
.rev-refs-toggle {
  margin-top: 8px; padding: 5px 12px; border-radius: 6px; border: 1px solid #c8102e;
  background: #fff; color: #c8102e; font-size: 12px; font-weight: 700; cursor: pointer;
}
.rev-refs-toggle:hover:not(:disabled) { background: #fdeceb; }
.rev-refs-toggle:disabled { border-color: #c7cede; color: #9aa3ba; cursor: not-allowed; }
.rev-refs-panel { padding: 14px 20px; border-bottom: 1px solid #e3e8f0; background: #fbfcfe; }
```

- [ ] **Step 5: Rodar a suíte completa**

Run: `node --test`
Expected: `tests 132`, `pass 132`, `fail 0`.

- [ ] **Step 6: Prova visual (Playwright ou navegador manual)**

Logado em `/minuta/revisao`, abrir um dispositivo do órgão `dpo` (que tem `alternatives.df`
e `alternatives.pa` desde a correção de hoje) — o botão deve aparecer como
"Ver referências (2)", clicável; ao clicar, mostra os chips DF/PA e o texto do estado
selecionado; clicar em "Ocultar referências" fecha o painel. Abrir um dispositivo de um
órgão/tema SEM `alternatives` (ex.: qualquer capítulo listado como "0 alternatives" na
auditoria de hoje) — o botão aparece cinza/desabilitado com o tooltip. Trocar de dispositivo
(fechar o popup e abrir outro) — o painel deve fechar automaticamente. Screenshot dos 2 casos
(com e sem referência) pra registrar a prova.

- [ ] **Step 7: Commit**

```bash
git add src/components/RevisaoModal.jsx src/index.css
git commit -m "feat(revisao): botão 'Ver referências' retrátil no popup, mostra o Bloco D do capítulo"
```
