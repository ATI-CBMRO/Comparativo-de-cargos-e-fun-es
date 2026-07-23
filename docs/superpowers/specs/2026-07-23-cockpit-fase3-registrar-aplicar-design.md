# Cockpit de curadoria — Fase 3: registrar e aplicar decisões — Design

**Data:** 2026-07-23
**Status:** aprovado (brainstorming com o Wândrio, 2026-07-23)
**Fases anteriores:** Fase 1 — Conferência linear (PR #19); Fase 2 — aba Decisões, leitura
(PR #20). Ambas mescladas.
**Spec-mãe:** `2026-07-22-cockpit-curadoria-conferencia-decisoes-design.md` (seção Fase 3).

## Objetivo

Fechar o ciclo da curadoria: o Wândrio **registra** a decisão pelo próprio sistema (não mais
só no Obsidian), a decisão **se aplica** à minuta (texto final no dispositivo, visível no
documento e no .docx) ou vira **ficha de aplicação** (estrutural), o "Divergente" da
Conferência **persiste** como pendência, e o **Obsidian recebe de volta** o que foi decidido.

## Decisões de produto (aprovadas no brainstorming)

1. **Firebase é a fonte oficial** da decisão registrada pelo sistema; o vault Obsidian é
   atualizado DE VOLTA via exportação + script local (bloco 5). A aba distingue
   **"Decidida no sistema"** (Firebase) de **"Decidida no vault"** (frontmatter da nota).
2. **Só admin** registra/edita/desfaz decisão (ato de comando). Convidados seguem lendo.
   **Quem analisa as decisões é o Tiago** (definição do Wândrio, 2026-07-23): para delegar,
   o Wândrio concede papel admin ao Tiago pela tela `/acessos` (mecanismo existente — sem
   código novo). O sistema precisa ORIENTÁ-LO sobre a dinâmica — ver C6.
3. Decisão de **redação**: o Wândrio **aponta o dispositivo alvo na hora** (lista do
   capítulo, numeração contínua), com o texto pré-preenchido pela redação atual. Nada de
   casamento automático por nome (anti-AR-01).
4. O texto final vale **no cenário ativo no momento do registro** (o marcador de cenário do
   `dispositivoId` cuida do isolamento). Aplicar no outro cenário = registrar a aplicação lá
   também, explicitamente.
5. **Obsidian recebe atualização** do que for decidido no sistema (exigência do Wândrio):
   exportação JSON pelo navegador + script local que escreve nas notas, com regra dura de
   conflito (nunca sobrescrever decisão manual divergente em silêncio).

## Arquitetura (6 componentes)

### C1 — Dados de decisão: `src/lib/decisionsData.js` (+ regra no `firestore.rules`)

Coleção nova `decisions` no Firestore (mesma base da Revisão). Documento chaveado pelo
**id da decisão** (o mesmo `id` do `decisoes_curadoria.json` — nome do arquivo da nota sem
extensão; aplicar a MESMA convenção de encoding de id que a Revisão já usa nos
`finalTexts` — ver Riscos). Campos:

```
{
  tipo: 'redacao' | 'estrutural',
  decisao: string,            // o que ficou decidido + porquê (texto do Wândrio)
  fonteEscolhida: string,     // rótulo da candidata vencedora ou 'redação própria'
  // só redação:
  alvoDispositivoId: string | null,  // dispositivoId (com marcador de cenário) que recebeu o finalText
  // só estrutural (ficha de aplicação):
  ficha: { oQueMuda: string, onde: string, status: 'aguardando' | 'aplicada' } | null,
  registradoPor: string, registradoEm: serverTimestamp,
}
```

API (espelha `reviewData.js`): `subscribeDecisions(onChange, onError)` (mapa id→doc),
`registrarDecisao(id, dados, autor)`, `marcarFichaAplicada(id, autor)`,
`desfazerDecisao(id)` (delete). Lógica pura separada e testável em
`src/lib/decisionsMerge.js`: `mergeDecisoes(decisoesJson, decisoesFirebase)` → cada decisão
ganha `statusDecisao: 'sistema' | 'vault' | 'pendente'` (Firebase vence sobre vault) e os
campos registrados; `pendenciasDeAplicacao(merged)` → fichas `aguardando`.

`firestore.rules`: `match /decisions/{id}` — `read: if isMember(); write: if isAdmin();`
(mesmo padrão de `finalTexts`). `match /conferencia/{id}` — `read: if isMember();
write: if isMember();` (qualquer membro confere; ver C4).

### C2 — Registro na aba Decisões: modal + selo

`DecisoesCuradoria.jsx` assina `subscribeDecisions` **quando logado** (`useAuth`; sem login
a aba continua 100% leitura, como hoje) e funde via `mergeDecisoes`. Card:

- Selo passa a 3 estados: **Decidida no sistema** (verde, ícone distinto) /
  **Decidida no vault** (verde claro, como hoje) / **Pendente**.
- Botão **"Registrar decisão"** (só admin, cartões não decididos no sistema) abre
  `RegistroDecisaoModal.jsx`:
  - passo 1: tipo (`redacao`/`estrutural`) + texto da decisão + fonte escolhida (select com
    as candidatas do cartão + "redação própria");
  - passo 2 (só redação): lista dos dispositivos do capítulo da decisão no **cenário
    ativo** (reusa `buildConferencia`/`buildArticles` filtrado pelo `chapterId` da decisão,
    com rótulo "Art. N"), o Wândrio marca UM alvo; textarea do texto final pré-preenchida
    com a redação atual do dispositivo;
  - passo 2 (só estrutural): campos da ficha (`oQueMuda`, `onde` — texto livre);
  - salvar: grava `decisions/{id}` e, se redação, também `saveFinalText(alvoDispositivoId,
    { texto, status: 'fechado', autor })` (API existente de `reviewData.js`). Falha em
    qualquer gravação → erro visível, nada de sucesso parcial silencioso (gravar decisão
    primeiro, finalText depois; se o finalText falhar, mostrar aviso claro com botão
    de repetir).
  - Decisão já registrada: admin vê "Desfazer" (delete do doc; o finalText associado NÃO é
    apagado automaticamente — aviso no confirm dizendo que o texto final permanece e pode
    ser revisto pela Revisão; simplicidade > cascata mágica).
- Bloco **"Pendências de aplicação"** no topo da página (recolhível): fichas `aguardando`
  (com botão "Marcar aplicada", só admin) + Divergentes persistidos da Conferência do
  documento/cenário ativo (C4). Vazio honesto quando não houver.

### C3 — Texto final chega ao documento e ao .docx (overlay no Wizard)

Hoje só a tela de Revisão aplica `finalTexts`. Passa a valer também nos dois Wizards:

- Lógica pura nova `applyFinals(articles, finalsMap)` em `src/lib/minutaFinals.js`
  (testada): para cada artigo de `buildArticles`, se houver `finalTexts` com status
  `fechado` para o `caputDispositivoId`/`incisoDispositivoId` correspondente, substitui o
  texto exibido e marca `hasFinal: true`.
- `MinutaWizard.jsx` e `RegulamentoWizard.jsx`: quando logado, assinam
  `subscribeFinalTexts` (filtrado por documento/cenário via `reviewGroup.js` —
  `filterFinalsByScenario`/`docOfDispositivo`, já existentes e testados) e aplicam
  `applyFinals` antes de renderizar e antes de gerar o .docx (`minutaDocx.js` recebe os
  artigos já com overlay — sem mudança de assinatura além dos textos). Badge no topo:
  "N textos finais aplicados". **Sem login: documento base, com aviso discreto** "entre
  para ver os textos finais aplicados" — ausência sinalizada, não silenciosa.

### C4 — Conferência persistente

`ConferenciaLinear.jsx`: o estado Confere/Divergente, hoje local, passa a persistir na
coleção `conferencia` quando logado (documento por dispositivo: id = mesma convenção de
encoding dos `finalTexts`, contendo o marcador de cenário; campos
`{ status: 'ok'|'div', por, em }`). Sem login, continua local com aviso "entre para
salvar a conferência". Lógica pura `src/lib/conferenciaStatus.js`:
`mergeStatus(local, remoto)` (remoto vence), `contarDivergentes(mapa, doc, cenario)`.
Os Divergentes aparecem no bloco de pendências da aba Decisões (C2).

### C5 — Obsidian recebe as decisões: exportação + script local

- Botão **"Exportar decisões"** (admin, na aba Decisões): baixa `decisoes_export.json`
  (client-side, Blob) com as decisões registradas no sistema:
  `[{ id, tipo, decisao, fonteEscolhida, alvoDispositivoId, registradoPor, registradoEm }]`.
- `scripts/aplicar_decisoes_vault.py` (roda local, mesmo venv do pipeline): lê o export,
  localiza cada nota no vault (`VAULT_CURADORIA`, mesma constante/env do
  `build_decisoes_curadoria.py`), e:
  - preenche a seção `## Decisão CBMRO` com o texto (+ rodapé
    `_Registrado no sistema por <quem> em <data>._`) e troca `decidido: false → true`
    no frontmatter;
  - **conflito** (nota já tem decisão manual diferente de placeholder e diferente do
    sistema): NÃO sobrescreve; lista no relatório final ("N aplicadas, M conflitos, K não
    encontradas") e sai com código ≠ 0 se houver conflito — anomalia se sinaliza;
  - idempotente: rodar duas vezes não duplica rodapé nem texto.
- Depois de aplicar no vault, rodar `build_decisoes_curadoria.py` faz a aba passar a
  mostrar essas decisões também como "vault" — o ciclo fecha.

### C6 — Guia da metodologia (orientação para o analista — Tiago)

Exigência do Wândrio: quem vai analisar as decisões é o **Tiago**, e ele precisa ser
orientado pelo próprio sistema sobre a dinâmica/metodologia. Dois entregáveis:

- **Seção nova no Manual de uso** (`/manual`, `Manual.jsx`): "Cockpit de curadoria — como
  decidir", em linguagem simples e SEM jargão, cobrindo: o papel de cada tela (Conferência
  = conferir dispositivo a dispositivo; Decisões = ler o material comparado e registrar o
  veredito); os 3 selos (Pendente / Decidida no vault / Decidida no sistema); a diferença
  entre decisão de **redação** (aponta um artigo e o texto final passa a valer no documento
  e no .docx) e **estrutural** (gera ficha de aplicação, aplicada depois em sessão de
  trabalho); o que é o Divergente e onde ele aparece; o ciclo com o Obsidian (exportar →
  script → nota atualizada); e quem pode o quê (leitura para todos os membros; registro
  para papel admin). Passo a passo numerado de "como registrar uma decisão" com o
  vocabulário exato dos botões.
- **Link "Como funciona"** no topo da aba Decisões, levando à seção do Manual — o Tiago
  não precisa saber de antemão onde a orientação mora.

## Fora de escopo (YAGNI)

- Aplicação automática de decisão estrutural (deliberadamente manual, via ficha).
- Apagar/propagar finalText em cascata ao desfazer decisão.
- De-para automático de dispositivo entre cenários (anti-AR-01).
- Edição livre da minuta fora do fluxo de decisão (Revisão já cobre comentários).
- Sincronização contínua com o vault (é exportação sob demanda, não daemon).

## Tratamento de erro

- Gravações Firebase: erro → mensagem visível no modal, sem fechar; nunca sucesso parcial
  silencioso.
- Export: se não houver decisão registrada, botão gera aviso, não arquivo vazio.
- Script do vault: vault ausente → erro e saída ≠ 0 (mesma regra do pipeline da Fase 2);
  conflito e nota-não-encontrada → relatório explícito + saída ≠ 0.

## Testes e prova

- Puro JS (`node --test`): `mergeDecisoes`/`pendenciasDeAplicacao`, `applyFinals`,
  `mergeStatus`/`contarDivergentes`.
- Python: `aplicar_decisoes_vault.py` contra vault-fixture (aplicação, conflito,
  idempotência, nota ausente).
- Prova real (Playwright, login do Wândrio ou conta admin de teste): registrar decisão de
  redação → texto no Wizard e no .docx baixado; registrar estrutural → ficha em pendências;
  Divergente persiste após recarregar; exportar + rodar o script num vault de teste →
  nota preenchida; seção do Manual visível e link "Como funciona" funcionando;
  preservação: Revisão e Subsídio intocados (diff).

## Riscos

- **Encoding de id no Firestore:** `editId` contém `/` (ex.: `organ:cg/competencia`), e
  ids de documento Firestore tratam `/` como separador de caminho. A Revisão JÁ grava
  `finalTexts` com esses ids em produção — a primeira task do plano deve VERIFICAR
  empiricamente qual convenção/encoding ela usa e replicá-la nas coleções novas
  (`decisions`, `conferencia`). Não inventar encoding novo.
- **Congelamento da estrutura** durante a rodada (premissa herdada da Revisão): o
  `dispositivoId` só é estável se `minuta_structure`/`regulamento_structure` não mudarem.
- **Regras do Firestore publicam pelo console** (processo manual documentado em
  `docs/FIREBASE_SETUP.md`) — a mudança de rules entra no repo, mas o Wândrio/sessão
  precisa publicá-la para valer.
- Varreduras AR-01 da auditoria: reexecutar; ponto novo desta fase = o
  `alvoDispositivoId` é escolhido MANUALMENTE (por desenho), então a varredura vira
  conferência de que nenhum caminho de código faz casamento automático de dispositivo.
