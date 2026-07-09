# Design — Bloco C, fatia 1: comissão comenta o Regulamento (multi-documento na Revisão)

**Data:** 2026-07-07
**Status:** aprovado para escrita do plano de implementação

## 1. Objetivo

A aba **Revisão** (Firebase) hoje só serve a **um** documento (a minuta do RI, via
`minuta_structure.json`). Esta fatia estende o mesmo fluxo — balão por dispositivo,
sugestão, curtida, texto final do admin — para o **segundo documento**: a minuta do
**Regulamento** (`database/regulamento_structure.json`, gerada no Bloco B), **sem
misturar os comentários dos dois documentos** e **sem que o Regulamento fique visível
à comissão antes de o Wândrio validar a minuta**.

É deliberadamente a fatia mínima do Bloco C original (ver plano-mestre, seção Bloco C).
As demais 5 fatias — rodadas com versão congelada, convite em massa, exportação .docx do
texto final, relatórios de participação, endurecimento de acesso a arquivos estáticos —
ficam fora de escopo e viram itens futuros (§9).

## 2. Decisões de produto (validadas com o Wândrio)

| Tema | Decisão |
|------|---------|
| Escopo desta rodada | Só multi-documento (RI + Regulamento comentáveis, isolados). Sem rodadas/versões, sem convite em massa, sem .docx, sem relatórios. |
| Navegação entre documentos | **Um seletor no topo** da própria página Revisão (não duas entradas de menu). |
| Quando o Regulamento fica comentável | **Interruptor do admin** (`config/revisao.regulamentoAberto`). Enquanto `false`, participantes veem "em preparação" e não comentam; o admin sempre pode ver e testar. |
| Quem é "a comissão" | O mesmo grupo de `members/` já convidado para o RI — sem convite em massa nesta fatia. |

## 3. Por que dá para reaproveitar quase tudo

`regulamento_structure.json` foi gerado (Bloco B2) **no mesmo formato estrutural** de
`minuta_structure.json` (`{chapters:[{id, kind, articles/sections:[...]}]}`), justamente
para herdar de graça `buildArticles`, `minutaArticles.js`, o wizard e — agora — a Revisão.
A única coisa que falta é a camada de **isolamento por documento** nos comentários e na
tela.

**Confirmado por inspeção dos dois JSONs (evita a suposição de que os endereços não
colidem):**
- Todo `editId` da minuta do RI vem sem prefixo ou com prefixo `organ:` (ex.:
  `preliminares`, `organ:cg/finalidade`).
- Todo `editId` do Regulamento já nasce com prefixo **`reg:`** (ex.:
  `reg:disposicoes-preliminares/mt-art-1`) — foi assim que o B2 rotulou os capítulos por
  tema.
- `chapterIdOf(editId)` (em `minutaTargets.js:8-10`) é `editId.split('/')[0]` — já
  funciona para os dois formatos sem alteração, porque é genérico.

Conclusão: **o próprio `editId` já serve de etiqueta de documento.** Não é preciso
inventar um campo novo nem migrar dado nenhum — só usar o prefixo `reg:` (presença/ausência)
para filtrar. Um comentário de dispositivo do Regulamento sempre tem `dispositivoId`
começando em `reg:`; um do RI, nunca.

*Alternativa descartada:* gravar um campo explícito `{documento: 'ri'|'regulamento'}` em
cada sugestão. Mais "limpo" no papel, mas exigiria migrar as sugestões do RI já existentes
no Firestore (senão ficam sem o campo e quebram um filtro `where`). O prefixo já presente
no `editId` resolve com **zero migração**.

## 4. Arquitetura / fluxo

```
Revisao.jsx
  ├─ Seletor de documento: [ Minuta do RI ] [ Regulamento ]  (estado local: docId 'ri'|'reg')
  ├─ carrega minuta_structure.json OU regulamento_structure.json conforme docId (fetchJson)
  ├─ interruptor "Regulamento aberto p/ comentários" — SÓ renderizado quando user é admin
  │    lido/gravado em config/revisao (Firestore)
  ├─ se docId === 'reg' e !regulamentoAberto e !isAdmin → EmptyState "Em preparação"
  └─ resto IDÊNTICO ao fluxo atual (Rail, RevisaoModal, subscribeSuggestions, finalTexts)
       — só filtrando por prefixo do dispositivoId
```

### Componentes que mudam (todos já existem — nenhum arquivo novo de peso)

- **`src/lib/reviewData.js`**
  - `subscribeSuggestions` e `subscribeFinalTexts` continuam OUVINDO as coleções inteiras
    (mesma leitura de hoje) — o filtro por documento acontece client-side, pelo prefixo do
    `dispositivoId`/`id`. Evita criar índice novo e mantém a assinatura das funções.
  - **Novo:** `subscribeRevisaoConfig(onChange, onError)` — assina `config/revisao` (doc
    único) e `setRegulamentoAberto(bool)` — grava (só chamável pela UI quando `isAdmin`,
    mas a *garantia* real está na regra do Firestore, não na UI).
- **`src/pages/Revisao.jsx`**
  - Estado `docId` ('ri' | 'reg'), seletor no cabeçalho.
  - Troca a URL do `fetchJson` conforme `docId` (`/database/minuta_structure.json` vs
    `/database/regulamento_structure.json`).
  - Filtra `suggestions`/`finals` por `dispositivoId` começar (ou não) com `'reg:'`,
    conforme `docId`.
  - Assina `subscribeRevisaoConfig`; se `docId === 'reg' && !regulamentoAberto && !isAdmin`,
    renderiza `EmptyState` ("O Regulamento ainda está em preparação — em breve estará
    disponível para comentários.") em vez do documento.
  - Interruptor do admin: pequeno toggle no `page-header`, visível só quando
    `user.role === 'admin'` e `docId === 'reg'`.
- **`src/lib/dispositivoId.js`** — nenhuma mudança de assinatura; só um comentário
  documentando que o prefixo `reg:` do `editId` já distingue o documento (evita que
  alguém "arrume" isso no futuro achando que falta).
- **`firestore.rules`**
  - Nova regra para `config/revisao`: qualquer membro lê; só admin escreve.
  - Nenhuma mudança nas regras de `suggestions`/`finalTexts` — o isolamento é por
    convenção de prefixo no aplicativo, não por regra (as regras já exigem `isMember()`
    para tudo; não há necessidade de regra por documento nesta fatia, já que os dois
    documentos são visíveis ao mesmo grupo de convidados).

### O que **não** muda
- `RevisaoModal.jsx`, `RevisaoChapterRail.jsx`, `reviewGroup.js`, `minutaArticles.js`,
  `minutaTargets.js` — reusados tal qual, sem edição.
- Estrutura de dados de `suggestions`/`finalTexts` no Firestore — sem migração.

## 5. Modelo de dados — o que é novo

- **`config/revisao`** (documento único) — `{ regulamentoAberto: boolean }`. Ausência do
  doc é equivalente a `false` (fail-closed: enquanto ninguém ligar o interruptor,
  Regulamento fica fechado por padrão).

Nenhuma coleção nova; nenhum campo novo em `suggestions`/`finalTexts`.

## 6. Segurança

- `config/revisao`: `allow read: if isMember(); allow write: if isAdmin();` — mesma
  função `isAdmin()` já usada em `members`.
- O fail-closed protege contra o cenário "esqueci de configurar": documento ausente ⇒
  tratado como fechado no client.
- Continua valendo a limitação já registrada no A9: arquivos estáticos
  (`/database/*.json`) respondem por link direto independente de login — quem tiver a
  URL exata do `regulamento_structure.json` consegue **ler o texto da minuta**, mesmo
  com o interruptor desligado. O interruptor controla a **interação** (comentar), não a
  leitura do arquivo estático. Isso já era uma limitação conhecida (A9) e o
  endurecimento (middleware de borda) segue sendo item futuro — não é regressão desta
  fatia, mas deve ficar claro para o Wândrio.

## 7. UI (texto, não mockup — mudança pequena e não visual o bastante para justificar o companion)

Cabeçalho da página Revisão passa a ter, à direita do título:

```
[ Minuta do RI ]  [ Regulamento ]      (toggle-group, estilo dos chips .oc-state-chip já usados)
```

Quando `docId === 'reg'` e `user.role === 'admin'`, mais um controle pequeno abaixo:

```
Comissão pode comentar o Regulamento:  ( ○ desligado  ● ligado )
```

Reaproveita o padrão visual já existente (chips, toggle simples) — sem CSS novo além de
1-2 classes `.rev-doc-switch`.

## 8. Testes

- `reviewGroup.js` (ou novo helper) — função pura que decide "este dispositivoId pertence
  ao documento X" a partir do prefixo — testável isoladamente (`node --test`).
- `firestore.rules` — regra de `config/revisao`: membro lê, não-admin não escreve, admin
  escreve. (Padrão dos testes de regra já existentes no projeto, se houver; senão,
  verificação manual documentada como no A1.)
- Verificação manual ponta a ponta (Wândrio, como nas fatias anteriores — não crio contas
  de teste no Firebase de produção): comentar em ambos os documentos sem vazamento
  cruzado; membro comum não vê o Regulamento com interruptor desligado; ligar o
  interruptor libera para todos; comentários antigos do RI continuam intactos.

## 9. Fora de escopo (fatias futuras do Bloco C)

1. Rodadas com versão congelada do Regulamento (parar de aceitar comentários numa data,
   arquivar).
2. Convite em massa (import de e-mails para `members/`).
3. Consolidação + exportação do texto final do Regulamento em `.docx` (reusaria
   `minutaConsolidation.js`/`minutaDocx.js`, mas fica para depois).
4. Relatórios de participação por membro (base: `membersStats.js`/`reviewGroup.js`).
5. Endurecimento do acesso a `/database/*.json` e `/legislacao-pdf/*` (middleware de
   borda validando sessão Firebase) — já registrado como pendência do A9.

## 10. Riscos e mitigação

| Risco | Mitigação |
|-------|-----------|
| Prefixo `reg:` colidir por acidente com algum `editId` futuro do RI | Documentar a convenção no `CLAUDE.md` (editIds do RI nunca devem começar com `reg:`); é dado gerado por script, fácil de garantir. |
| Doc `config/revisao` esquecido (nunca criado) | Ausência tratada como `false` no client — fail-closed por padrão. |
| Confundir "ligar comentários" com "trancar leitura do arquivo" | Documentar explicitamente no CLAUDE.md e avisar o Wândrio (§6) — não é regressão, é limitação preexistente do A9. |
