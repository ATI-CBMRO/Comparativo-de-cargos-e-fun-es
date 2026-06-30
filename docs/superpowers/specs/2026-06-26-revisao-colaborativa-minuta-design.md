# Design — Revisão Colaborativa da Minuta (login + comentários por dispositivo)

**Data:** 2026-06-26
**Galho:** `feat/revisao-colaborativa-minuta`
**Status:** aprovado para escrita do plano de implementação

## 1. Objetivo

Permitir que pessoas convidadas façam login na plataforma e, para cada **dispositivo legal
da minuta** (no nível de **inciso/parágrafo**), deixem sugestões de alteração. A plataforma
armazena as sugestões de todos; o **administrador** marca cada uma como *relevante* ou
*descartada* e escreve o **texto final** consolidado daquele dispositivo.

## 2. Decisões de produto (validadas com o usuário)

| Tema | Decisão |
|------|---------|
| Quem acessa | **Só convidados** (lista controlada pelo admin). Sem cadastro aberto. |
| Granularidade do comentário | **Por inciso/parágrafo** (nível mais fino). |
| Visibilidade entre participantes | **Todos veem todos** (debate aberto), com autoria + 👍. |
| Texto final | **Admin marca relevante/descarta e reescreve** o texto final na própria plataforma. |
| Login | **E-mail + senha** (+ "esqueci a senha"). |
| Base técnica | **Firebase** (Authentication + Firestore). Frontend segue na Vercel. |

## 3. UX validada (mockups aprovados no companion visual)

- **Marcador de comentário discreto:** trilha de balões na **margem direita** de cada inciso
  (estilo "Revisão" do Word). Balão cinza-claro quando não há sugestões; vermelho com contador
  quando há. Escolhido para não poluir a tela diante de muitos incisos.
- **Página de interação:** documento largo e confortável; ao clicar no balão, abre uma
  **janela central (modal)** com as sugestões daquele inciso.
- **Janela do participante:** lista de sugestões (autor, data, 👍) + campo "escrever sugestão".
- **Janela do admin:** mesma janela + por sugestão os botões **✅ Relevante / ❌ Descartar**,
  um campo **"Texto final do inciso"**, botão **Salvar texto final** e um selo de **status**
  (`em aberto` / `fechado`). Painel do admin com progresso (nº de incisos fechados).

## 4. Arquitetura

```
SITE React/Vite (Vercel) — intacto + nova rota /revisao
        │  (SDK do Firebase, sem servidor próprio)
        ▼
FIREBASE
  ├─ Authentication (e-mail + senha)
  └─ Firestore (comentários, decisões, textos finais, membros)
      └─ Security Rules (porteiro: só convidado; papéis participante/admin)
```

- **Nada do site atual é reformado.** A minuta, o wizard `/minuta`, organogramas e a pipeline
  Python continuam iguais. Acrescenta-se a área **/revisão**.
- A área **/revisão reaproveita `minuta_structure.json`** (mesma fonte do wizard) para renderizar
  capítulos → artigos → incisos. A numeração de artigos continua via `src/lib/minutaArticles.js`
  (`buildArticles`), apenas para **exibição**.

### Componentes (frontend)
- `src/lib/firebase.js` — inicialização do app Firebase (config via variáveis de ambiente Vite,
  `import.meta.env.VITE_FIREBASE_*`). Nenhuma chave hardcoded no código versionado.
- `src/lib/auth.jsx` — contexto de autenticação (usuário atual, papel, login, logout, reset de senha).
- `src/lib/reviewData.js` — funções de leitura/escrita no Firestore (sugestões, decisões, textos finais).
- `src/lib/dispositivoId.js` — gera o **endereço fixo** do inciso (ver §6).
- `src/pages/Login.jsx` — tela de login + "esqueci a senha".
- `src/pages/Revisao.jsx` — página protegida; renderiza o documento + trilha de balões.
- `src/components/RevisaoModal.jsx` — a janela central do inciso (alterna visão participante/admin).
- `src/components/ProtectedRoute.jsx` — bloqueia rotas para quem não está logado/convidado.
- `src/pages/AdminMembros.jsx` (mínimo) — visão do admin com progresso. Cadastro de pessoas na v1
  é feito pelo painel do Firebase (ver §8).

Cada arquivo tem uma responsabilidade única e pode ser entendido/testado isoladamente.

## 5. Modelo de dados (Firestore)

> Coleções no topo. IDs entre `{}`.

- **`members/{uid}`** — `{ nome, email, role: 'participante' | 'admin', ativo: bool, criadoEm }`.
  A existência do doc (com `ativo: true`) é o que autoriza o acesso.
- **`suggestions/{suggestionId}`** —
  `{ dispositivoId, dispositivoLabelSnapshot, trechoSnapshot, autorUid, autorNome, texto,
     criadoEm, curtidas: number, curtidoPor: string[], adminStatus: 'pendente'|'relevante'|'descartada' }`.
- **`finalTexts/{dispositivoId}`** —
  `{ texto, status: 'em_aberto' | 'fechado', atualizadoPor, atualizadoEm }`.

`dispositivoLabelSnapshot` (ex.: "Art. 7º, II") e `trechoSnapshot` (o texto do inciso no momento)
são gravados junto à sugestão para preservar o contexto mesmo que a minuta mude depois.

## 6. Endereço fixo do inciso (`dispositivoId`)

O rótulo "Art. 7º" **não** serve como identificador: a numeração de artigos é recalculada por
`buildArticles` conforme o texto é editado/excluído. O `dispositivoId` é derivado de identificadores
**estáveis** já existentes na estrutura da minuta:

```
dispositivoId = `${editId}#${indiceDoInciso}`
```

onde `editId` é o id estável da seção em `minuta_structure.json` (o mesmo usado hoje pelo conjunto
`excluded: Set<"editId#index">` no wizard) e `indiceDoInciso` é a posição do inciso dentro da seção.
Isso garante que cada sugestão permaneça ancorada ao inciso correto.

**Premissa:** durante a rodada de revisão, a estrutura da minuta (`minuta_structure.json`) é
**congelada** (não se reexecuta a pipeline que altera `editId`). Documentado como regra operacional.

## 7. Segurança (Firestore Security Rules)

- Acesso negado a qualquer pessoa sem `members/{uid}` com `ativo == true` (mesmo conhecendo a URL).
- **Participante:** lê a minuta e todas as sugestões; cria sugestões com `autorUid == seu uid`;
  edita/apaga **apenas as próprias**; pode dar/remover o próprio 👍.
- **Admin:** tudo acima + escreve `adminStatus` nas sugestões, escreve `finalTexts`, gerencia `members`.
- Identidade sempre verificada pelo login (sem se passar por outro). Regras versionadas em
  `firestore.rules`; testadas localmente com o emulador do Firebase.

## 8. Provisionamento de acesso (v1)

O admin cadastra cada convidado no **painel do Firebase Authentication** (e-mail + senha inicial) e
cria o doc correspondente em `members/`. Um botão "Convidar pessoa" dentro do app fica para a v2
(exige Admin SDK/Cloud Function). O primeiro `admin` (Wândrio) é marcado manualmente.

## 9. Escopo da 1ª versão (MVP)

**Inclui:** login e-mail+senha + reset de senha; rota `/revisao` protegida; documento com trilha de
balões (margem direita) + modal central; participante cria/vê sugestões e dá 👍; admin marca
relevante/descarta e grava o texto final por inciso; painel de progresso do admin; segurança por
convite + papéis.

**Fica para v2:** botão "Convidar pessoa" no app; respostas em fio (thread) às sugestões; exportar
relatório de decisões e gerar a minuta final consolidada em `.docx`; notificações por e-mail.

## 10. Custo

Plano gratuito (Spark) do Firebase: cotas de leitura/escrita/armazenamento muito acima do uso de uma
comissão de revisão. Estimativa: **R$ 0/mês**. Sem cartão obrigatório enquanto não usar Cloud Functions.

## 11. Testes

- `dispositivoId.js` — testes unitários (`node --test`, padrão já usado em `minutaArticles.test.js`)
  garantindo geração e estabilidade do endereço do inciso.
- `firestore.rules` — testes de regras no emulador (convidado vê / estranho não vê / participante não
  escreve decisão / admin escreve).
- Verificação manual do fluxo ponta a ponta (login → sugerir → curar → texto final) antes do merge.

## 12. Riscos e mitigação

| Risco | Mitigação |
|-------|-----------|
| `editId` mudar e "soltar" comentários | Congelar `minuta_structure.json` na rodada; snapshots de contexto na sugestão. |
| Vazar chave do Firebase | Config por `.env` (no `.gitignore`); regras de segurança restritivas (a config pública do Firebase é segura quando as Rules existem). |
| Acesso indevido | `members.ativo` + Security Rules como única fonte de autorização. |
| Custo inesperado | Manter Spark; sem Cloud Functions na v1. |
```
