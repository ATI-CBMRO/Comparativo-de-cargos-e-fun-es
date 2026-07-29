# Registrar decisão em janela separada — Design

## Objetivo

Hoje o formulário de registro de decisão (`RegistroDecisaoModal.jsx`) abre como um overlay
centrado (`.decm-overlay` + `.decm`, 720px) que **cobre o card da decisão**. Quem está
redigindo a decisão perde de vista justamente o material que precisa consultar: a Questão,
os excertos verbatim das candidatas (Mato Grosso, Goiás, RS…) e a Comparação.

Este trabalho move o formulário para uma **janela separada do navegador**, que pode ser
posicionada ao lado da janela principal (ou em outro monitor), deixando a tela de Decisões
visível e navegável enquanto se preenche o registro.

Decidido com o Wândrio/Tiago em 29/07/2026: janela do navegador de verdade (não um modal em
2 colunas nem uma gaveta lateral), com a janela principal livre e a decisão em edição
destacada.

## Contexto técnico confirmado

- `RegistroDecisaoModal` recebe `decisao`, `trilha`, `cenario`, `autor`, `onClose`, `onSaved`
  e é renderizado por `DecisoesCuradoria.jsx` quando o estado `registrando` não é nulo.
- Ele já resolve dados por cenário: `fetchJson(scenarioDbUrl(cenario, ARQ[trilha]))` para
  montar a lista de artigos-alvo, e grava com `registrarDecisao(decisionDocId(d.id, cenario), …)`
  (isolamento por cenário, commit `d8b0405`).
- Ele depende do contexto React do app: `db` do Firestore (`decisionsData.js`, `reviewData.js`).
  `DecisoesCuradoria` também usa `useAuth()` e `useScenario()`. **Manter a árvore React única
  é o que evita ter de refazer login/cenário na janela nova.**
- Os estilos vivem num CSS único (`src/index.css`). Uma janela aberta por `window.open` nasce
  com `<head>` vazio — sem clonar as folhas de estilo, o formulário sai sem CSS nenhum.
- O feed do Firestore em `DecisoesCuradoria` é `onSnapshot` (`subscribeDecisions`), então a
  janela principal reflete o registro sozinha assim que ele é gravado — sem precisar de
  mensagem entre janelas.

## Abordagem escolhida: portal do React para a janela nova

`window.open` cria a janela; `createPortal(children, janela.document.body)` renderiza o
formulário dentro dela mantendo-o na **mesma árvore React** da janela principal. Assim
`useAuth`, `useScenario`, Firestore e todo o estado do formulário continuam funcionando sem
adaptação.

Descartadas:
- **Rota própria aberta como janela** (`/minuta/decisoes/registrar/:id`): recarregaria o
  bundle inteiro, refaria login e rebuscaria a estrutura, e exigiria sincronizar estado entre
  janelas. Peso desproporcional ao ganho.
- **Painel flutuante arrastável** na mesma página: não atende ao pedido (continuaria preso à
  área do navegador).

## Componente novo: `JanelaSeparada`

Novo arquivo `src/components/JanelaSeparada.jsx`. Cuida **só** do ciclo de vida da janela —
não sabe nada sobre decisões e pode ser reusado por qualquer outra tela.

```
JanelaSeparada({ titulo, largura, altura, onFechar, onBloqueada, children })
```

Responsabilidades:

1. **Abrir** a janela no mount (`window.open('', nome, 'width=…,height=…')`), com um `nome`
   fixo por finalidade — reabrir com o mesmo nome reaproveita a janela existente em vez de
   criar outra.
2. **Clonar as folhas de estilo** da janela principal para o `<head>` da nova: percorre
   `document.head` copiando os `<style>` e os `<link rel="stylesheet">`. Cobre tanto o dev
   (Vite injeta `<style>`) quanto a produção (`<link>`). O clone é um **retrato no momento da
   abertura**; estilos injetados depois (HMR no dev) não aparecem até reabrir — aceitável,
   afeta só o desenvolvimento.
3. **Portalizar** `children` em `janela.document.body`.
4. **Detectar o fechamento pelo usuário** (X da janela) e chamar `onFechar()`, para o pai
   limpar o estado e reabilitar o botão. Detecção por `beforeunload` na janela filha, com
   verificação de `janela.closed` como rede de segurança.
5. **Limpar**: fecha a janela ao desmontar; fecha junto se a janela principal for
   fechada/recarregada (`beforeunload` no pai), para não deixar janela órfã.
6. **Sinalizar bloqueio**: se `window.open` devolver `null` (bloqueador de pop-up), chama
   `onBloqueada()` e não renderiza nada.

## Divisão de `RegistroDecisaoModal`

O arquivo atual mistura a moldura (overlay + card) com o formulário. Passa a ser:

- **`RegistroDecisaoForm.jsx`** — todo o conteúdo e a lógica de hoje (tipo redação/estrutural,
  campos, lista de artigos-alvo, gravação, tratamento de erro), **sem** o `.decm-overlay`.
  Nenhuma mudança de comportamento: mesma gravação, mesmo `decisionDocId(d.id, cenario)`,
  mesmas mensagens de erro.
- **`RegistroDecisaoModal.jsx`** — passa a ser só a escolha da moldura: tenta a
  `JanelaSeparada`; se ela sinalizar bloqueio, cai no overlay de hoje envolvendo o mesmo
  `RegistroDecisaoForm`.

## Comportamento da janela principal

- Permanece **totalmente navegável**: rolar a lista, abrir/fechar candidatas e Comparação,
  trocar de filtro.
- O card em edição recebe destaque visual (classe nova `dec-card-editando` em `index.css`,
  seguindo o padrão do `dec-card-ok` já existente).
- O botão daquele card vira **"Editando em outra janela"**, desabilitado — evita abrir duas
  janelas para a mesma decisão.
- Os botões das **demais** decisões seguem ativos. Clicar num deles troca o conteúdo da
  **mesma** janela (nome fixo) e a traz para frente com `janela.focus()`.
- Salvar fecha a janela (o `onSaved` de hoje já limpa `registrando`).

## Fallback de pop-up bloqueado

Se o navegador bloquear a janela, o formulário abre no overlay de hoje com um aviso no topo:
que a janela foi bloqueada e que liberar pop-ups para este site permite abri-la ao lado.
O registro continua possível pelo overlay — nada de caminho morto (mesma diretriz do AR-04
em `docs/superpowers/auditoria-armadilhas.md`).

Observação: `window.open` é disparado a partir do clique em "Registrar decisão", ou seja,
dentro de um gesto do usuário — o caso normal não é bloqueado.

## Fora de escopo

- Não altera o conteúdo das decisões, o filtro por cenário (`filtrarPorCenario`) nem o
  isolamento no Firestore (`decisionDocId`).
- Não altera a lógica interna do formulário — só muda onde ele é renderizado.
- Não move para janela separada nenhum outro popup do portal (Revisão, PDF do Acervo).

## Testes e verificação

- As suítes atuais devem seguir verdes: `npm test` (141) e `npm run test:py`. A divisão do
  modal não introduz lógica pura nova, então não há teste unitário novo a escrever —
  `JanelaSeparada` é plumbing de DOM/janela, que `node --test` (sem DOM) não cobre de forma
  honesta.
- A prova é **visual, com o app real**:
  1. Abrir "Registrar decisão" → a janela abre **com o CSS aplicado** e o card segue visível
     e rolável na janela principal.
  2. Card em edição destacado e botão "Editando em outra janela" desabilitado.
  3. Clicar em "Registrar decisão" de outra decisão → reaproveita a mesma janela, com foco.
  4. Fechar a janela no X → o card volta ao normal e o botão reabilita.
  5. Gravar uma decisão de verdade (admin, cenário ativo) → a janela fecha e o card aparece
     como "Decidida no sistema" na janela principal, via `onSnapshot`.
  6. `npm run build` com exit 0.
