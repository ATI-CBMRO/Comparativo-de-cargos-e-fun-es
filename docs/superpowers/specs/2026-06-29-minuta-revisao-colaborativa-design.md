# Revisão Colaborativa da Minuta de RI — Design

- **Data:** 2026-06-29
- **Status:** Aprovado (desenho); aguardando plano de implementação
- **Área do produto:** Aba de Minuta de Regimento Interno (`/minuta`)

## Contexto

O Portal de Legislação dos CBMs gera hoje, no wizard `/minuta`
(`src/pages/MinutaWizard.jsx`), uma **minuta articulada única** do Regimento Interno
do CBMRO a partir de `database/minuta_structure.json` (produzido por
`scripts/build_minuta_structure.py`). A curadoria atual é individual e efêmera:
remove incisos por checkbox, reescreve o texto de uma seção em "modo avançado" e o
resultado só é materializado no `.docx` no download. Não há contas, autoria, nem
estado compartilhado — o portal é uma SPA 100% estática que lê JSONs prontos.

A demanda é transformar essa etapa em um **fluxo colaborativo de deliberação**: a
minuta gerada é apresentada ao CONDEG; cada coronel, logado, propõe
inclusões/edições/remoções de trechos (com registro de autoria); as sugestões são
reunidas e deliberadas em conjunto até a edição final e aprovação.

## Decomposição em sub-projetos

O escopo total é grande e atravessa subsistemas independentes. Ele se divide em:

- **Fase 0 — Fundação (FORA DESTE SPEC):** backend, banco de dados e autenticação
  (login/senha dos coronéis, papéis). **Já está sendo desenvolvida em projeto
  apartado.**
- **Fase 1 — Sugestões com autoria (ESTE SPEC):** tela colaborativa por
  capítulo/seção onde cada coronel propõe incluir/editar/remover seções e incisos;
  cada sugestão carimba autor + data + tipo; todos veem as sugestões de todos.
- **Fase 2 — Deliberação & consolidação (ESTE SPEC):** tela onde o CONDEG vê as
  sugestões por item, decide, edita o texto final, aprova e gera a minuta final.

Este documento cobre **Fases 1 e 2 como protótipo de frontend**, rodando contra
**dados simulados**, com o objetivo de **visualizar o funcionamento** antes de o
backend real existir. A integração com a Fase 0 é tratada como contrato futuro
(ver "Integração futura com o backend").

## Objetivo

Construir, dentro do portal, as duas telas do fluxo colaborativo (sugestão e
deliberação), operando sobre uma **camada de dados isolada e trocável**, de modo que:

1. O usuário consiga ver e demonstrar o fluxo ponta a ponta (sugerir → deliberar →
   minuta final) sem backend.
2. Quando o backend real chegar, **apenas a implementação interna da camada de
   dados** seja trocada — sem alterar as telas.

## Não-objetivos (fora de escopo)

- Autenticação real, backend ou banco de dados (Fase 0, projeto apartado).
- Sincronização em tempo real entre máquinas. A colaboração é **simulada** trocando
  de identidade no mesmo navegador (`localStorage`).
- Aplicação real de permissões/papéis (apenas representados nos dados simulados).
- O ato administrativo de aprovação/publicação além de gerar o documento final.
- Alterar a estrutura de capítulos da minuta (os 26 órgãos da LOB + Guarnição
  permanecem fixos). A edição atua em **seções** (incluir/renomear/remover) e
  **incisos** (incluir/editar/remover) dentro de cada capítulo.

## Decisões de UX (validadas em mockups)

- **Layout da fase de sugestão:** três colunas — **trilha de capítulos** ·
  **documento** · **painel lateral de sugestões**.
- **Filtro por capítulo:** trilha à esquerda (padrão do "Sumário" atual) com campo
  de filtro de texto, alternador "só com sugestões" e **badge por capítulo** com o
  total de sugestões (cinza quando 0). Selecionar um capítulo foca o documento nele.
- **Janela de sugestão:** **painel lateral à direita** (não modal, não inline) —
  mostra o texto e a *thread* coletiva lado a lado.
- **Representação de uma edição:** **Antes/Depois** (bloco do texto atual riscado +
  bloco do proposto), por dar clareza ao colegiado mesmo em reescritas grandes.
- **Colaboração:** todos veem as sugestões de todos, com **autoria visível**
  (nome/posto + data) e ações **Apoiar** e **Comentar**.
- **Compositor:** no rodapé do painel, seletor de tipo (Editar / Incluir / Remover)
  + campo de texto + justificativa opcional + "Enviar sugestão". "+ nova seção"
  cria uma seção proposta no capítulo.
- **Identidade simulada:** barra superior com "Você está como Cel. X ▾" (troca de
  coronel) + indicador de fase.
- **Tela de deliberação (Fase 2):** **lista de pendências como entrada** (tabela só
  com itens que receberam sugestões: nº de sugestões, localização, status
  pendente/decidido) → ao clicar, **fila de revisão guiada** (item a item: texto
  vigente, sugestões com Aceitar/Rejeitar, campo de texto final, "Aprovar item e
  avançar", com barra de progresso).

## Arquitetura

### Onde mora no app

Duas rotas novas sob o guarda-chuva da minuta, com entrada no array `NAV` de
`src/App.jsx`. O `/minuta` (gerador) e `/minuta-diagramas` permanecem inalterados.

- **`/minuta/revisao`** — Fase 1 (sugestões colaborativas).
- **`/minuta/deliberacao`** — Fase 2 (deliberação do CONDEG).

Ambas leem `database/minuta_structure.json` como documento-base.

### Camada de dados isolada (peça-chave)

Módulo único `src/lib/suggestionsStore.js` com **API assíncrona** (sempre retorna
`Promise`) modelada no formato de um backend REST. Internamente delega a um objeto
`backend` com duas implementações: `localBackend` (hoje, sobre `localStorage`) e um
stub `apiBackend` (futuro). Só `localBackend` é ligado neste protótipo. A "sessão"
do coronel também é simulada aqui.

Chave de persistência em `localStorage`: namespace único (ex.: `cbm.minuta.revisao`).
Inclui um *seed* de demonstração e `resetDemo()`.

API:

- `listUsers()` → `User[]`
- `getCurrentUser()` / `setCurrentUser(userId)`
- `listSuggestions({ chapterId?, targetId? })` → `Suggestion[]`
- `addSuggestion(payload)` → `Suggestion`
- `supportSuggestion(id, userId)` / `unsupportSuggestion(id, userId)`
- `addComment(id, { authorId, text })` → `Comment`
- `decideSuggestion(id, status, userId)` — `status: 'aceita' | 'rejeitada'`
- `getItemResolution(targetId)` / `setFinalText(targetId, text, userId)`
- `getChapterCounts()` → `{ [chapterId]: number }` (para os badges)
- `resetDemo()`

### Modelo de dados (simulado, espelhando o backend futuro)

```
Suggestion {
  id: string
  chapterId: string          // ch.id de minuta_structure.json, ex.: "organ:cg"
  targetId: string           // editId da seção/artigo-alvo
  targetKind: 'inciso' | 'secao'
  incisoIndex?: number       // quando targetKind === 'inciso'
  type: 'editar' | 'incluir' | 'remover'
      | 'incluir-secao' | 'renomear-secao' | 'remover-secao'
  originalText: string       // snapshot p/ contexto/diff (editar/remover)
  proposedText: string       // para editar/incluir
  justification?: string
  authorId: string
  createdAt: string          // ISO
  supporters: string[]       // userIds
  comments: Comment[]
  status: 'pendente' | 'aceita' | 'rejeitada'
  decidedBy?: string
  decidedAt?: string         // ISO
}

Comment { id: string, authorId: string, text: string, createdAt: string }

ItemResolution {
  targetId: string
  finalText: string
  status: 'pendente' | 'decidido'
  resolvedBy?: string
  resolvedAt?: string
}

User { id: string, name: string, posto: string, role: 'condeg' | 'relator' }
```

### Componentes

Novos:

- `src/pages/MinutaRevisao.jsx` — página da Fase 1 (3 colunas).
- `src/pages/MinutaDeliberacao.jsx` — página da Fase 2 (lista → fila de revisão).
- `src/components/ChapterRail.jsx` — trilha de capítulos filtrável com contadores
  (compartilhada pelas duas fases).
- `src/components/SuggestionPanel.jsx` — painel lateral (thread + compositor).
- `src/components/SuggestionCard.jsx` — uma sugestão (Antes/Depois + autoria +
  apoiar/comentar; em modo deliberação, ganha Aceitar/Rejeitar).
- `src/components/IdentityBar.jsx` — login simulado + indicador de fase.
- `src/lib/suggestionsStore.js` — camada de dados.
- `src/lib/minutaTargets.js` — helper que percorre `minuta_structure.json` em alvos
  endereçáveis (capítulo → seção → inciso), reaproveitando a numeração de
  `buildArticles`.

Reúso: `src/lib/minutaArticles.js` (`buildArticles`, `articleLabel`, `romanize`);
`database/minuta_structure.json`; CSS de `src/index.css` (tema CBMRO); padrão de
exportação `.docx` do `MinutaWizard` para a "minuta final".

## Plano de implementação (etapas)

1. **Camada de dados:** `suggestionsStore` + coronéis fictícios + *seed*, com o seam
   de troca para backend. Teste `node --test` (padrão de `minutaArticles.test.js`).
2. **Peças compartilhadas:** `ChapterRail`, `IdentityBar`, `minutaTargets`.
3. **Fase 1** (`MinutaRevisao`): documento + marcadores + painel + compositor +
   ações colaborativas (apoiar/comentar), ligados ao store.
4. **Fase 2** (`MinutaDeliberacao`): lista de pendências → fila de revisão →
   decidir → texto final → "minuta final" (`.docx`, reusando o exportador atual).
5. **Integração:** rotas + entrada no `NAV` (`App.jsx`) + CSS em `index.css`.

## Testes

- `suggestionsStore` e `minutaTargets`: testes unitários `node --test` (sem
  dependência de DOM), cobrindo persistência, autoria, contagem por capítulo e a
  derivação de alvos a partir de `minuta_structure.json`.
- Não há suíte de testes de UI configurada no projeto; validação das telas é manual
  via `npm run dev` (localhost:5173).

## Integração futura com o backend (contrato)

Quando a Fase 0 estiver pronta, criar `apiBackend` implementando a mesma assinatura
de `suggestionsStore` (chamadas `fetch` à API real, com o usuário vindo da sessão
autenticada em vez de `setCurrentUser`). Trocar o `backend` ativo no módulo. As telas
não mudam. O modelo de dados acima deve ser usado como referência ao definir os
endpoints/tabelas do backend para minimizar atrito na troca.
