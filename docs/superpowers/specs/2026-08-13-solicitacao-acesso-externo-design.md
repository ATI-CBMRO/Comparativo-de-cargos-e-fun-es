# Solicitação de acesso externo com aprovação do admin

**Data:** 2026-08-13
**Origem:** hoje o acesso à Revisão Colaborativa da Minuta só é liberado se o admin
convidar a pessoa primeiro (por e-mail, na tela `/acessos`). O Wândrio quer inverter esse
fluxo para pessoas externas: elas recebem o link do sistema, se autocadastram preenchendo
um formulário (com cidade/unidade em cascata usando o vocabulário real do CBMRO), e só
depois de aprovadas pelo admin ganham acesso de fato.

---

## Decisões tomadas (com o Wândrio, 2026-08-13)

| Questão | Decisão |
|---|---|
| Quando a senha é definida | **Junto com o pedido** (uma visita só). A conta fica criada mas bloqueada até aprovação |
| Aviso de aprovação | **Manual** — o admin avisa a pessoa por fora (WhatsApp etc.); nenhum e-mail automático |
| Cascata de unidade | **3 passos:** Cidade → Comando (COB I/II, CAT, Comando Geral, CEEI, COA, DPLAN...) → Unidade |
| Fonte da lista de cidades/unidades | Dados reais do **Sistema ATI** (`sistema-ati-2026`, tabelas `unidades`/`users`), copiados para este repositório — os dois sistemas não têm conexão entre si |
| Fluxo de convite manual do admin (`Acessos.jsx`) | **Mantido**, sem alteração — a nova solicitação pública é um caminho adicional, não substitui o convite |

---

## Estado atual (levantado por exploração do código)

- `src/pages/Cadastro.jsx` (rota `/cadastro`): formulário só com e-mail + senha. Não
  grava nada no Firestore — só cria a conta no Firebase Auth
  (`cadastrar()` em `src/lib/auth.jsx:75-77`).
- O documento `members/{email}` só é criado hoje pelo admin, em `Acessos.jsx`, **antes**
  de a pessoa se autocadastrar (fluxo de convite). Estrutura atual do documento
  (`src/lib/membersData.js:18-31`):
  ```js
  { email, nome, role: 'admin'|'participante', ativo, status: 'convidado'|'cadastrado',
    uid, criadoEm, criadoPor, ultimoLogin }
  ```
- `firestore.rules:29-37` permite `create` em `members/{email}` **só para admin**.
  `update` do próprio usuário é restrito a `uid`, `status`, `ultimoLogin`.
- O gate de acesso real é o campo **`ativo`** (`auth.jsx`: se o doc não existe ou
  `ativo !== true`, força logout e marca `naoAutorizado`). O campo `status` é só rótulo
  de exibição.
- Não existe hoje nenhuma tela de "cidade → unidade" em cascata no sistema. O
  `Organograma.jsx` tem uma modelagem territorial, mas usa a **nomenclatura da proposta
  de nova LOB** (CRBM, BBM) — não serve para este formulário, que precisa da nomenclatura
  **vigente**, a mesma que as pessoas reconhecem hoje.

### Dados reais do Sistema ATI (fonte da cascata)

18 cidades com unidade do CBMRO: Ariquemes, Buritis, Cacoal, Candeias do Jamari,
Cerejeiras, Colorado do Oeste, Espigão D'Oeste, Guajará-Mirim, Jaru, Ji-Paraná,
Machadinho D'Oeste, Ouro Preto do Oeste, Pimenta Bueno, Porto Velho, Presidente Médici,
Rolim de Moura, São Miguel do Guaporé, Vilhena.

63 unidades, agrupadas por "coordenadoria" (o **Comando**, 2º passo da cascata):
CAT (23), COB I (13), COB II (11), Comando Geral (3), COA (2), CEEI (2), e mais 9
comandos com 1 unidade cada (DPLAN, DLOG, DINF, DCS, Corregedoria, Coordenadoria de
Pessoal, Defesa Civil, Diretoria de Inteligência, CPOF). Exemplos de unidade (3º passo):
"1º GBM", "1º GBM / 1º SGBM" (Guajará-Mirim, subordinado ao 1º GBM de Porto Velho),
"DAT - Ariquemes / SAT - Buritis".

Vocabulário confirmado: GBM = Grupamento de Bombeiros Militar; SGBM = Subgrupamento;
COB I/II = Coordenadoria Operacional de Bombeiros; CAT = Coordenadoria de Atividades
Técnicas; DAT = Divisão de Atividades Técnicas; SAT = Seção de Atividades Técnicas.

---

## Desenho da solução

### 1. Dados de cidade/unidade

Novo módulo `src/lib/unidadesCbmro.js`, com a lista das 63 unidades reais (copiadas do
seed do Sistema ATI) estruturada como:

```js
export const UNIDADES_CBMRO = [
  { cidade: 'Porto Velho', comando: 'COB I', unidade: '1º GBM' },
  { cidade: 'Guajará-Mirim', comando: 'COB I', unidade: '1º GBM / 1º SGBM' },
  { cidade: 'Buritis', comando: 'CAT', unidade: 'DAT - Ariquemes / SAT - Buritis' },
  // ... 63 no total
]
```

Funções puras derivadas (testáveis sem Firebase):
- `cidadesDisponiveis()` → lista de cidades únicas, ordenadas
- `comandosPorCidade(cidade)` → comandos únicos existentes naquela cidade
- `unidadesPorCidadeEComando(cidade, comando)` → unidades da combinação

Se `comandosPorCidade(cidade)` retornar só 1 item, a tela pula o passo do Comando
automaticamente (evita clique desnecessário).

### 2. Nova tela pública `/solicitar-acesso`

Novo arquivo `src/pages/SolicitarAcesso.jsx`. Campos: Nome completo, Nome de guerra,
Cidade (select), Comando (select, populado a partir da cidade), Unidade (select, populado
a partir de cidade+comando), E-mail, Senha, Confirmar senha. Todos obrigatórios.

Ao enviar:
1. `createUserWithEmailAndPassword(auth, email, senha)` — igual ao `Cadastro.jsx` de hoje.
2. Grava `members/{email}` com:
   ```js
   { email, nome, nomeGuerra, cidade, comando, unidade, role: 'participante',
     ativo: false, status: 'pendente', uid, criadoEm: serverTimestamp(),
     criadoPor: null, ultimoLogin: null }
   ```
3. Mostra confirmação: "Pedido enviado. Você será avisado quando for aprovado."

Se a pessoa tentar logar antes da aprovação, `auth.jsx` já força logout por `ativo !==
true` — só ajusto a mensagem exibida para diferenciar "pedido em análise" (doc existe,
`status === 'pendente'`) de "e-mail não cadastrado" (doc não existe).

`Cadastro.jsx` (fluxo de convite do admin) **não muda** — continua servindo quem já foi
convidado manualmente.

### 3. Regra do Firestore (`firestore.rules`)

Novo ramo em `allow create` de `members/{email}`, além do já existente `isAdmin()`:

```
allow create: if isAdmin()
  || (request.auth.token.email == email
      && request.resource.data.ativo == false
      && request.resource.data.status == 'pendente'
      && request.resource.data.role == 'participante'
      && request.resource.data.uid == request.auth.uid
      && request.resource.data.keys().hasOnly(
           ['email','nome','nomeGuerra','cidade','comando','unidade',
            'role','ativo','status','uid','criadoEm','criadoPor','ultimoLogin']));
```

A pessoa só consegue criar o **próprio** documento (e-mail do token = chave do doc),
sempre travado em `ativo: false` / `role: participante` — não há caminho para
autoaprovação ou virar admin por essa via. Os ramos de `update`/`delete` já existentes
(só admin) não mudam.

### 4. Painel do admin (`Acessos.jsx`)

Nova seção **"Solicitações pendentes"** (membros com `status === 'pendente'`), acima ou ao
lado da tabela atual. Cada linha mostra nome, nome de guerra, cidade, unidade, e-mail, com
dois botões:
- **Aprovar** → `update` de `ativo: true` (o campo `status` vira `cadastrado` sozinho no
  próximo login, como já acontece hoje).
- **Recusar** → `update` de `status: 'recusado'`, mantém `ativo: false`. O registro fica
  para auditoria; a conta do Firebase Auth em si não é apagada (a exclusão de conta de
  outro usuário exige Admin SDK/Cloud Function, fora do escopo — mesma limitação já
  registrada para a conta de teste `teste.claude.lob@gmail.com`).

O formulário "Convidar pessoa" e a tabela de membros existentes continuam exatamente como
estão.

### 5. Tela de login (`Login.jsx`)

Ajuste de texto/link: além do link atual para quem já foi convidado (`/cadastro`),
adicionar "Ainda não tem acesso? Solicitar acesso" apontando para `/solicitar-acesso`.

---

## Testes

- Testes puros (Vitest, sem Firebase) para `unidadesCbmro.js`: `cidadesDisponiveis`,
  `comandosPorCidade`, `unidadesPorCidadeEComando` — cobrindo cidade com 1 único comando
  (pula passo) e cidade com vários (Porto Velho).
- Teste manual ponta a ponta (Playwright, como já foi feito para o fluxo de convite):
  preencher `/solicitar-acesso` com e-mail de teste → conferir doc `pendente` no Firestore
  → aprovar em `/acessos` → logar com sucesso → limpar dados de teste ao final.
- Conferir que o convite manual antigo (`Acessos.jsx` → `/cadastro`) continua funcionando
  sem regressão.

## Fora de escopo (YAGNI)

- E-mail automático de aprovação/recusa (decisão: aviso manual).
- Apagar a conta do Firebase Auth ao recusar um pedido (exige Admin SDK).
- Conectar ao banco do Sistema ATI ao vivo (são projetos sem integração; a lista é
  copiada, não sincronizada).
