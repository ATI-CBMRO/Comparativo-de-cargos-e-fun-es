# Registrar decisão em janela separada — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Mover o formulário de registro de decisão para uma janela separada do navegador, deixando a tela de Decisões visível e navegável enquanto se preenche o registro.

**Architecture:** `window.open` cria a janela e `createPortal` renderiza o formulário dentro dela, mantendo-o na MESMA árvore React da janela principal — assim `useAuth`, `useScenario`, Firestore e o estado do formulário continuam funcionando sem adaptação. O `RegistroDecisaoModal` atual se divide em formulário (conteúdo/lógica) e moldura (janela separada, com fallback para o overlay de hoje se o pop-up for bloqueado).

**Tech Stack:** React 18.3.1 (`createPortal` de `react-dom`), Vite 6, CSS único em `src/index.css`, `lucide-react` para ícones.

Spec: `docs/superpowers/specs/2026-07-29-registro-decisao-janela-separada-design.md`

## Global Constraints

- Português do Brasil em toda a UI e nos comentários de código (padrão do repositório).
- Nenhuma mudança de comportamento no registro em si: mesmos tipos (redação/estrutural), mesma gravação, mesmo `decisionDocId(d.id, cenario)` (isolamento por cenário, commit `d8b0405`).
- Não editar JSON gerado em `database/`.
- Suítes que devem seguir verdes ao fim de cada task: `npm test` = **141 passando**, `npm run test:py` = exit 0, `npm run build` = exit 0.
- **Não há teste unitário novo neste plano.** O repositório roda `node --test` sem DOM (não há jsdom nas devDependencies), então `window.open`/`createPortal` não são cobríveis honestamente por teste de nó. A verificação de cada task é: suítes existentes verdes + prova visual no app real, com o resultado esperado escrito em cada passo. Não escrever teste de fachada que não prova nada.
- Servidor de dev na porta fixa 5173 (`npm run dev -- --port 5173 --strictPort`).
- Para provar visualmente é preciso estar logado como **admin** (o botão "Registrar decisão" só aparece para admin) e ter `.env` preenchido (já existe nesta máquina, via `vercel env pull`).

## File Structure

| Arquivo | Responsabilidade |
|---|---|
| `src/components/JanelaSeparada.jsx` (**criar**) | Só o ciclo de vida da janela: abrir, clonar estilos, portalizar, avisar fechamento, limpar. Não sabe nada de decisões. |
| `src/components/RegistroDecisaoForm.jsx` (**criar**) | O formulário: campos, lista de artigos-alvo, gravação, erros. Sem moldura. |
| `src/components/RegistroDecisaoModal.jsx` (**modificar**) | Passa a ser só a escolha da moldura: janela separada ou, se bloqueada, overlay. |
| `src/pages/DecisoesCuradoria.jsx` (**modificar**) | Destaque do card em edição e botão "Editando em outra janela". |
| `src/index.css` (**modificar**) | `.dec-card-editando`, `.janela-sep-body`, `.decm-aviso` e ajuste do `.decm` dentro da janela. |

---

### Task 1: Extrair o formulário para `RegistroDecisaoForm` (refatoração pura)

Separa conteúdo de moldura **sem mudar nada visível**. Ao fim desta task o app se comporta exatamente como hoje (overlay centrado). Isso isola o risco: se algo quebrar nas tasks seguintes, sabemos que não foi a extração.

**Files:**
- Create: `src/components/RegistroDecisaoForm.jsx`
- Modify: `src/components/RegistroDecisaoModal.jsx` (167 linhas hoje)

**Interfaces:**
- Produces: `RegistroDecisaoForm({ decisao, trilha, cenario, autor, onClose, onSaved, aviso })` — default export. `aviso` é uma string opcional exibida no topo do formulário (usada só pelo fallback da Task 2); quando ausente, nada é renderizado no lugar.
- Consumes: nada de tasks anteriores.

- [ ] **Step 1: Criar `RegistroDecisaoForm.jsx` com o conteúdo movido**

Criar o arquivo novo copiando **verbatim** de `RegistroDecisaoModal.jsx` as linhas 1-12 (imports + constantes `ARQ` e `semCenario`) e todo o corpo da função (linhas 15-81: estados, os dois `useEffect`, `artigos`, `escolher`, `podeSalvar`, `gravarFinal`, `salvar`). Muda apenas a assinatura, o JSX externo e a inclusão do `aviso`.

Assinatura (substitui a linha 14 do arquivo original):

```jsx
export default function RegistroDecisaoForm({ decisao: d, trilha, cenario, autor, onClose, onSaved, aviso }) {
```

O `return` deixa de ter o `.decm-overlay` (que vira responsabilidade da moldura) e ganha o `aviso`. Trocar o bloco que hoje começa em `return (` / `<div className="decm-overlay" …>` por:

```jsx
  return (
    <div className="decm card">
      <div className="decm-head">
        <h3>Registrar decisão</h3>
        <button className="btn btn-ghost" onClick={onClose}><X size={16} /></button>
      </div>
      {aviso && <p className="decm-aviso">{aviso}</p>}
      <p className="dec-questao">{d.titulo}</p>
```

O restante do JSX (campos Tipo, Decisão, Fonte escolhida, bloco `tipo === 'redacao'`, bloco `tipo === 'estrutural'`, bloco `erro` e `.decm-acoes`) é copiado **sem alteração**. Fechar com:

```jsx
    </div>
  )
}
```

ou seja: some uma camada de `</div>` em relação ao original (a do overlay).

- [ ] **Step 2: Reduzir `RegistroDecisaoModal.jsx` a moldura**

Substituir o arquivo inteiro por:

```jsx
import RegistroDecisaoForm from './RegistroDecisaoForm.jsx'

// Moldura do registro de decisão. Nesta task ainda é o overlay de sempre; a Task 2
// troca por janela separada, mantendo este overlay como fallback de pop-up bloqueado.
export default function RegistroDecisaoModal(props) {
  return (
    <div className="decm-overlay" role="dialog" aria-modal="true">
      <RegistroDecisaoForm {...props} />
    </div>
  )
}
```

- [ ] **Step 3: Rodar as suítes e o build**

```bash
npm test
npm run build
```

Esperado: `pass 141`, `fail 0`; build exit 0. (A extração não toca lógica pura, então a contagem não muda.)

- [ ] **Step 4: Prova visual de que NADA mudou**

Com o dev server em `http://localhost:5173`, logado como admin, ir em Decisões (Regulamento), clicar em "Registrar decisão".

Esperado: o overlay abre igual a antes — mesmo tamanho, mesmos campos, X e Cancelar fecham, e trocar Tipo para "Estrutural" ainda troca os campos ("O que muda"/"Onde"). Nenhuma diferença visual.

- [ ] **Step 5: Commit**

```bash
git add src/components/RegistroDecisaoForm.jsx src/components/RegistroDecisaoModal.jsx
git commit -m "refactor(decisoes): extrai RegistroDecisaoForm da moldura do modal"
```

---

### Task 2: `JanelaSeparada` + abrir o formulário na janela nova

Cria o componente de janela e passa a usá-lo, com fallback para o overlay se o navegador bloquear.

**Files:**
- Create: `src/components/JanelaSeparada.jsx`
- Modify: `src/components/RegistroDecisaoModal.jsx`
- Modify: `src/index.css` (bloco novo ao lado das regras `.decm-*`, hoje em ~3111-3119)

**Interfaces:**
- Consumes: `RegistroDecisaoForm({ decisao, trilha, cenario, autor, onClose, onSaved, aviso })` da Task 1.
- Produces: `JanelaSeparada({ titulo, nome, largura, altura, onFechar, onBloqueada, children })` — default export. Chama `onBloqueada()` e não renderiza nada se `window.open` devolver `null`; chama `onFechar()` uma única vez quando o usuário fecha a janela.

- [ ] **Step 1: Criar `src/components/JanelaSeparada.jsx`**

```jsx
import { useEffect, useRef, useState } from 'react'
import { createPortal } from 'react-dom'

// Uma janela aberta por window.open nasce com <head> vazio — sem clonar as folhas de
// estilo, o conteúdo sai sem CSS nenhum. Cobre o dev (Vite injeta <style>) e a produção
// (<link rel="stylesheet">). É um retrato do momento da abertura: estilos injetados
// depois (HMR no dev) só aparecem ao reabrir a janela.
function clonarEstilos(origem, destino) {
  origem.querySelectorAll('style, link[rel="stylesheet"]')
    .forEach(no => destino.head.appendChild(no.cloneNode(true)))
}

// Renderiza `children` numa janela separada do navegador, mantendo-os na MESMA árvore
// React da janela principal (createPortal) — é isso que preserva login, cenário,
// Firestore e o estado do formulário sem nenhuma sincronização entre janelas.
export default function JanelaSeparada({
  titulo, nome = 'janela-portal', largura = 560, altura = 780,
  onFechar, onBloqueada, children,
}) {
  const [corpo, setCorpo] = useState(null)
  const janelaRef = useRef(null)
  // Callbacks em ref: mudam de identidade a cada render do pai e não podem
  // reabrir a janela.
  const onFecharRef = useRef(onFechar)
  const onBloqueadaRef = useRef(onBloqueada)
  useEffect(() => { onFecharRef.current = onFechar }, [onFechar])
  useEffect(() => { onBloqueadaRef.current = onBloqueada }, [onBloqueada])

  useEffect(() => {
    const janela = window.open('', nome, `width=${largura},height=${altura}`)
    if (!janela) { onBloqueadaRef.current?.(); return undefined }
    janelaRef.current = janela

    // Reabrir com o mesmo nome devolve a janela JÁ existente, que pode trazer o
    // conteúdo anterior — limpar antes de portalizar.
    janela.document.body.innerHTML = ''
    clonarEstilos(document, janela.document)
    janela.document.body.className = 'janela-sep-body'
    setCorpo(janela.document.body)

    // Avisa o pai uma única vez, venha o fechamento do evento ou do polling.
    let avisado = false
    const avisarFechamento = () => {
      if (avisado) return
      avisado = true
      onFecharRef.current?.()
    }
    janela.addEventListener('beforeunload', avisarFechamento)
    // Rede de segurança: nem todo navegador dispara beforeunload em janela
    // about:blank aberta por script.
    const vigia = setInterval(() => {
      if (janela.closed) { clearInterval(vigia); avisarFechamento() }
    }, 500)
    // Janela principal fechada/recarregada não pode deixar a filha órfã.
    const fecharFilha = () => janela.close()
    window.addEventListener('beforeunload', fecharFilha)

    return () => {
      clearInterval(vigia)
      janela.removeEventListener('beforeunload', avisarFechamento)
      window.removeEventListener('beforeunload', fecharFilha)
      janela.close()
    }
  }, [nome, largura, altura])

  // Trocar de decisão não reabre a janela: só atualiza o título e a traz para frente.
  useEffect(() => {
    const janela = janelaRef.current
    if (janela && !janela.closed) {
      janela.document.title = titulo
      janela.focus()
    }
  }, [titulo])

  if (!corpo) return null
  return createPortal(children, corpo)
}
```

- [ ] **Step 2: Ligar a moldura à janela, com fallback**

Substituir `src/components/RegistroDecisaoModal.jsx` inteiro por:

```jsx
import { useState } from 'react'
import JanelaSeparada from './JanelaSeparada.jsx'
import RegistroDecisaoForm from './RegistroDecisaoForm.jsx'

const AVISO_BLOQUEIO = 'O navegador bloqueou a janela separada. Libere pop-ups para este '
  + 'site se quiser preencher a decisão ao lado da tela de Decisões.'

// Escolhe a moldura do formulário: janela separada do navegador (para consultar a
// Questão e os excertos das candidatas enquanto se redige) e, se o pop-up for
// bloqueado, o overlay de sempre com um aviso — nunca um caminho morto.
export default function RegistroDecisaoModal(props) {
  const [bloqueada, setBloqueada] = useState(false)

  if (bloqueada) {
    return (
      <div className="decm-overlay" role="dialog" aria-modal="true">
        <RegistroDecisaoForm {...props} aviso={AVISO_BLOQUEIO} />
      </div>
    )
  }
  return (
    <JanelaSeparada
      titulo={`Registrar decisão — ${props.decisao.titulo}`}
      nome="registro-decisao"
      onFechar={props.onClose}
      onBloqueada={() => setBloqueada(true)}
    >
      <RegistroDecisaoForm {...props} />
    </JanelaSeparada>
  )
}
```

- [ ] **Step 3: CSS da janela e do aviso**

Acrescentar em `src/index.css`, logo depois da última regra `.decm-*` (hoje `.decm-acoes`, ~linha 3119):

```css
/* Formulário de registro dentro da janela separada: o body da janela nova não herda
   nada do layout do portal, e o .decm perde os limites que só fazem sentido no overlay. */
.janela-sep-body { margin: 0; padding: 16px; background: #eef1f6; }
.janela-sep-body .decm { width: 100%; max-height: none; overflow: visible; }
.decm-aviso { background: #fdf1e3; color: #b3600d; border-radius: 8px; padding: 10px; margin: 0 0 10px; }
```

- [ ] **Step 4: Rodar as suítes e o build**

```bash
npm test
npm run build
```

Esperado: `pass 141`, `fail 0`; build exit 0.

- [ ] **Step 5: Prova visual da janela**

Com o dev server rodando e logado como admin, em Decisões (Regulamento) clicar em "Registrar decisão".

Esperado:
1. Abre uma **janela separada** do navegador com o título "Registrar decisão — …".
2. O formulário aparece **com o CSS aplicado** (campos com borda arredondada, botões vermelhos do tema) — se sair sem estilo, `clonarEstilos` falhou.
3. A janela principal continua **navegável**: dá para rolar a lista e abrir/fechar as candidatas e a Comparação enquanto a janela está aberta.
4. Fechar a janela no X → o formulário some do estado do pai (clicar de novo em "Registrar decisão" reabre normalmente).

- [ ] **Step 6: Prova do fallback de bloqueio**

Bloquear pop-ups para `localhost:5173` nas configurações do navegador e clicar em "Registrar decisão".

Esperado: o formulário abre no overlay de sempre, com a tarja de aviso laranja no topo dizendo que a janela foi bloqueada. Registrar continua funcionando por ali. Depois, liberar os pop-ups de novo.

- [ ] **Step 7: Commit**

```bash
git add src/components/JanelaSeparada.jsx src/components/RegistroDecisaoModal.jsx src/index.css
git commit -m "feat(decisoes): registra decisão em janela separada do navegador"
```

---

### Task 3: Destaque na janela principal e botão "Editando em outra janela"

**Files:**
- Modify: `src/pages/DecisoesCuradoria.jsx`
- Modify: `src/index.css`

**Interfaces:**
- Consumes: o estado `registrando` já existente em `DecisoesCuradoria` (o objeto da decisão em edição, ou `null`).
- Produces: prop nova `emEdicao` (boolean) em `DecisaoCard`.

- [ ] **Step 1: Passar `emEdicao` para o card**

Em `src/pages/DecisoesCuradoria.jsx`, na renderização da lista, acrescentar a prop ao `<DecisaoCard>` (as demais props ficam como estão):

```jsx
              emEdicao={registrando?.id === d.id}
```

- [ ] **Step 2: Usar a prop no `DecisaoCard`**

Trocar a assinatura:

```jsx
function DecisaoCard({ d, isAdmin, emEdicao, onRegistrar, onDesfazer }) {
```

Acrescentar a classe de destaque no card (a `className` hoje é `card dec-card${status !== 'pendente' ? ' dec-card-ok' : ''}`):

```jsx
    <div className={`card dec-card${status !== 'pendente' ? ' dec-card-ok' : ''}${emEdicao ? ' dec-card-editando' : ''}`} style={{ marginBottom: 14, padding: 16 }}>
```

E trocar o bloco de ações do admin (hoje um ternário `status === 'sistema' ? Desfazer : Registrar decisão`) por:

```jsx
          {status === 'sistema' ? (
            <button className="btn btn-ghost" onClick={onDesfazer}>Desfazer</button>
          ) : emEdicao ? (
            <button className="btn btn-ghost" disabled>Editando em outra janela</button>
          ) : (
            <button className="btn btn-ghost" onClick={onRegistrar}>Registrar decisão</button>
          )}
```

- [ ] **Step 3: CSS do destaque**

Acrescentar em `src/index.css`, junto das regras `.dec-*` (depois de `.dec-card-ok`, ~linha 3094):

```css
.dec-card-editando { border-left: 3px solid #c8102e; box-shadow: 0 0 0 2px rgba(200,16,45,.14); }
```

- [ ] **Step 4: Rodar as suítes e o build**

```bash
npm test
npm run build
```

Esperado: `pass 141`, `fail 0`; build exit 0.

- [ ] **Step 5: Prova visual do destaque e do reaproveitamento da janela**

Logado como admin, em Decisões:
1. Clicar em "Registrar decisão" na 1ª decisão → o card ganha borda vermelha à esquerda e o botão vira "Editando em outra janela", desabilitado.
2. Com a janela ainda aberta, clicar em "Registrar decisão" de **outra** decisão → a **mesma** janela é reaproveitada (não abre uma segunda), vem para frente e mostra o título da nova decisão; o destaque muda de card.
3. Fechar a janela no X → o destaque some e o botão volta a "Registrar decisão".

- [ ] **Step 6: Commit**

```bash
git add src/pages/DecisoesCuradoria.jsx src/index.css
git commit -m "feat(decisoes): destaca o card em edição e reaproveita a janela aberta"
```

---

### Task 4: Prova ponta a ponta com gravação real e documentação

Fecha o trabalho provando que o caminho completo funciona **de verdade** (não só visualmente) e registra a mudança nos documentos do projeto.

**Files:**
- Modify: `CLAUDE.md` (seção "Fase 3 (registrar/aplicar…)", que descreve o cockpit)
- Modify: `.claude/PENDENCIAS.md` (bloco `## ✅ Concluído (mês atual)`)

**Interfaces:**
- Consumes: tudo das Tasks 1-3.
- Produces: nada de código.

- [ ] **Step 1: Gravar uma decisão de verdade pela janela separada**

Logado como admin, no cenário **LOB atual**, trilha Regulamento (que tem 27 decisões nos 2 cenários): abrir "Registrar decisão", escolher tipo **Redação**, preencher a decisão, escolher um artigo alvo, ajustar o texto final e salvar.

Esperado:
1. A janela separada fecha sozinha ao salvar.
2. Na janela principal, o card passa a "Decidida no sistema" **sem recarregar a página** (o `onSnapshot` de `subscribeDecisions` atualiza sozinho).
3. Trocar para o cenário **LOB futura** → a MESMA decisão continua **Pendente** (isolamento por `decisionDocId`, commit `d8b0405`, segue intacto).
4. Desfazer o registro no cenário atual devolve o card a "Pendente".

- [ ] **Step 2: Rodar a verificação completa**

```bash
npm test
npm run test:py
npm run build
```

Esperado: `pass 141` / `fail 0`; test:py exit 0; build exit 0.

- [ ] **Step 3: Atualizar o CLAUDE.md**

Na seção que descreve a Fase 3 do cockpit, acrescentar ao fim do parágrafo:

```
O formulário de registro abre em **janela separada do navegador** (`JanelaSeparada.jsx`
— `window.open` + `createPortal`, mantendo a árvore React única para preservar login,
cenário e Firestore), para consultar a Questão e os excertos das candidatas enquanto se
redige; o card em edição fica destacado e a janela é reaproveitada ao trocar de decisão.
Pop-up bloqueado cai no overlay de antes, com aviso. Spec
`2026-07-29-registro-decisao-janela-separada-design.md`.
```

- [ ] **Step 4: Registrar no PENDENCIAS**

Acrescentar como primeiro item de `## ✅ Concluído (mês atual)`:

```
- [x] **Registro de decisão em janela separada** (29/07/2026, pedido do Tiago): o
  formulário abria como overlay e cobria o card, escondendo a Questão e os excertos
  verbatim das candidatas — justamente o material de consulta para redigir a decisão.
  Agora abre em janela do navegador (`JanelaSeparada.jsx`, reutilizável), com a tela de
  Decisões livre, card em edição destacado, janela reaproveitada ao trocar de decisão e
  fallback para o overlay se o pop-up for bloqueado. node 141/141 + python OK + build limpo.
```

- [ ] **Step 5: Commit**

```bash
git add CLAUDE.md .claude/PENDENCIAS.md
git commit -m "docs: registra a janela separada do formulário de decisão"
```

---

## Self-Review

**Cobertura da spec:**

| Requisito da spec | Task |
|---|---|
| Componente `JanelaSeparada` (abrir, clonar estilos, portalizar, detectar fechamento, limpar, sinalizar bloqueio) | 2, Step 1 |
| Divisão em `RegistroDecisaoForm` + moldura | 1 |
| Fallback de pop-up bloqueado com aviso | 2, Steps 2-3 e 6 |
| Janela principal livre | 2, Step 5 (item 3) |
| Card em edição destacado | 3 |
| Botão "Editando em outra janela" desabilitado | 3 |
| Reaproveitar a mesma janela ao trocar de decisão | 2 (nome fixo + efeito de `titulo`), provado na 3, Step 5 |
| Salvar fecha a janela | 4, Step 1 |
| Não deixar janela órfã ao fechar a principal | 2, Step 1 (`fecharFilha`) |
| Suítes verdes + build | todas as tasks |
| Prova visual dos 6 pontos da spec | 2, Steps 5-6; 3, Step 5; 4, Step 1 |

**Placeholders:** nenhum "TBD"/"TODO"/"implementar depois". Todo passo de código traz o código.

**Consistência de tipos/nomes:** `RegistroDecisaoForm` é criado na Task 1 com a prop `aviso` e consumido com esse nome na Task 2. `JanelaSeparada` expõe `titulo`/`nome`/`largura`/`altura`/`onFechar`/`onBloqueada`/`children` na Task 2 e é usado com exatamente esses nomes. `emEdicao` é criado e consumido na Task 3. `decisionDocId` e `filtrarPorCenario` não são tocados — só referenciados na prova da Task 4.

**Escopo:** um único subsistema (a moldura do registro de decisão). Não decompõe.
