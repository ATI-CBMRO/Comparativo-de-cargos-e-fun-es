# Acervo público — terceiro perfil de acesso (visitante, sem login)

**Data:** 2026-08-18
**Origem:** pedido do Ten. Tiago — além dos perfis de **administrador** e **participante**,
criar um perfil **público**, sem login e senha, com apenas um cadastro básico, e com acesso
restrito ao Acervo Legal.

**Problema:** hoje o portal inteiro está atrás do login. Sem sessão válida, só `/login` e
`/solicitar-acesso` respondem — qualquer outro endereço é redirecionado
(`LoggedOutRoutes`, `src/App.jsx`). Quem é de fora do CBMRO e só quer consultar o acervo
comparado dos 27 CBMs precisa hoje pedir acesso, esperar aprovação do administrador e
receber, junto, um perfil de participante que não lhe diz respeito.

**Observação que moldou o desenho:** o Acervo Legal **não depende de autenticação
nenhuma**. `Legislations.jsx` lê JSON estático por `fetch` (`src/lib/dataCache.js`) e os
PDFs saem de `/legislacao-pdf/*`. Os dados já são públicos na rede; o login, para essas
telas, é hoje apenas uma porta de interface. Esta entrega não expõe nada novo — ela dá
uma porta legítima e um registro de quem entrou.

## Requisitos fixados com o Ten. Tiago (2026-08-18)

| Decisão | Escolha |
|---|---|
| O que o cadastro produz | **Registro nominal auditável** no Firestore, visível ao administrador |
| Recorte de acesso | Acervo (`/legislacoes`) + ficha do estado (`/estados/:id`) + busca (`/busca`) + PDFs |
| Campos do cadastro | Nome completo, e-mail, instituição/órgão (texto livre — público externo ao CBMRO) |
| Entrada | Imediata, sem aprovação; o navegador lembra; **sem** botão de bloqueio (registro é histórico) |
| Porta de entrada | **Rota própria `/acervo-publico`**, divulgável em ofício/site/QR code; `/login` fica intocado |

## Abordagem escolhida: camada separada (o público nunca vira `user`)

Foram consideradas três:

- **A — terceiro `escopo` dentro do usuário atual** (`escopo: 'publico'`, reusando
  `NAV_ESCOPO`/`ROTAS_LIBERADAS`/`GuardaDeEscopo`). Quase nenhuma casca nova, mas `user`
  deixaria de significar "membro autenticado": toda tela que faz `if (user)` — inclusive
  `ProtectedRoute` sem `requireAdmin` — passaria a aceitar visitante, e as leituras do
  Firestore falhariam em silêncio para ele, porque `isMember()` exige
  `request.auth.token.email`, que sessão anônima não tem. É o padrão **AR-04** (erro
  engolido) do catálogo de armadilhas do projeto. **Descartada.**
- **B — camada separada com sessão anônima do Firebase. ESCOLHIDA.**
- **C — sem auth anônima, gravando por função serverless** (`api/registrar-visitante` com
  credencial de servidor). Evitaria habilitar auth anônima, mas exigiria uma *service
  account* do Firebase como segredo na Vercel — hoje só há `GEMINI_API_KEY` lá — e um
  middleware equivalente no Vite para o ambiente de desenvolvimento. Muita infra e um
  segredo novo para gravar quatro campos. **Descartada.**

Razão de fundo para B: este projeto já pagou o preço de misturar trilhas (o vazamento de
enriquecimento de outros estados entre cenários; o transplante de MT na pauta do
participante). Manter o visitante numa camada que não toca o `user` é a versão barata do
mesmo aprendizado.

## 1. A fronteira é o caminho, não a condição de login

O público vive sob o prefixo **`/acervo-publico/*`**:

| Rota pública | Tela reusada |
|---|---|
| `/acervo-publico` | `Legislations` (tabela de cobertura + PDFs) |
| `/acervo-publico/estados/:id` | `StateDetail` |
| `/acervo-publico/busca` | `Search` |

Reusar `/legislacoes` para os dois públicos daria **dois donos ao mesmo endereço**, e a
guarda voltaria a depender de quem está logado — exatamente o acoplamento que a abordagem
B existe para evitar. Com prefixo próprio, a fronteira é legível na barra de endereço e no
roteador.

As três páginas são **reusadas sem fork**. Elas navegam em apenas cinco lugares, todos com
destino `/estados/...`:

| Arquivo | Linha | Destino |
|---|---|---|
| `src/pages/Legislations.jsx` | 51 | `/estados/<id>` |
| `src/pages/StateDetail.jsx` | 184 | `/estados` |
| `src/pages/StateDetail.jsx` | 202 | `/estados` |
| `src/pages/Search.jsx` | 185 | `/estados/<id>` |

Um contexto pequeno (`AcervoBase`, padrão vazio) e um hook `useAcervoNav()` substituem
essas chamadas por `irParaEstado(id)` e `voltarParaEstados()`. Nenhuma tela ganha
`if (visitante)`.

**Atenção ao destino do "voltar":** `/estados` (a lista `StatesList`) **não** faz parte do
recorte público. `voltarParaEstados()` não é um simples prefixo — no membro leva a
`/estados`, como hoje; no visitante leva a `/acervo-publico`, a tabela do acervo, que é de
onde ele veio. Um prefixo cego produziria `/acervo-publico/estados`, rota que não existe.

`/acervo-publico` também responde a quem **está logado**: membro é levado a `/legislacoes`,
onde já tem tudo — nunca uma tela de erro.

Em `/acervo-publico/estados/:id`, a ficha do estado exibe o organograma **daquele estado**,
que é material de acervo. Nada da estrutura do CBMRO em elaboração entra no recorte.

## 2. Sessão do visitante

`VisitanteProvider` (`src/lib/visitante.jsx`) é **irmão** do `AuthProvider`, nunca aninhado
dentro dele. Guarda `{ uid, nome }`.

- **Primeira visita:** formulário → `signInAnonymously` → grava `visitantes/{uid}` → entra.
- **Retorno:** a sessão anônima do Firebase persiste sozinha no navegador; o `localStorage`
  (chave `cbmro_visitante`) guarda `{ uid, nome }` para a casca renderizar sem esperar a rede.
- **`localStorage` limpo com sessão anônima viva:** o formulário reaparece e a gravação é
  `setDoc(..., { merge: true })` com `ultimoAcesso` novo — **atualiza o registro existente,
  não duplica**.
- **Não há "sair"**: não existe sessão a encerrar. Existe o link discreto
  "Sou membro — entrar", que leva a `/login`.

O `user` do `AuthProvider` **nunca** recebe visitante. `ProtectedRoute`, `GuardaDeEscopo`,
`NAV_ESCOPO` e `src/lib/escopoServico.js` ficam intocados por esta entrega.

## 3. Dados e regras do Firestore

Coleção nova `visitantes/{uid}`:

| Campo | Tipo | Origem |
|---|---|---|
| `uid` | string | uid da sessão anônima |
| `nome` | string (1..200) | formulário |
| `email` | string (≤200, normalizado por `normalizeEmail`) | formulário |
| `instituicao` | string (≤200) | formulário |
| `criadoEm` | timestamp | `serverTimestamp()` na criação |
| `ultimoAcesso` | timestamp | `serverTimestamp()` a cada gravação |

```
match /visitantes/{uid} {
  allow read, delete: if isAdmin();
  allow create, update: if request.auth != null
    && request.auth.uid == uid
    && request.resource.data.uid == uid
    && request.resource.data.keys().hasOnly(
         ['uid','nome','email','instituicao','criadoEm','ultimoAcesso'])
    && request.resource.data.nome is string
    && request.resource.data.nome.size() > 0 && request.resource.data.nome.size() <= 200
    && request.resource.data.email is string && request.resource.data.email.size() <= 200
    && request.resource.data.instituicao is string
    && request.resource.data.instituicao.size() <= 200;
}
```

**Nenhuma regra existente afrouxa.** `isMember()` continua exigindo
`request.auth.token.email`, que sessão anônima não possui — logo `suggestions`,
`decisions`, `finalTexts`, `conferencia`, `config/revisao` e `members` seguem fechados ao
visitante **pelo banco**, não apenas pela interface. O visitante também não lê o próprio
documento: não precisa, e a regra não concede.

A auth anônima é necessária porque o Firestore só aceita escrita com `request.auth != null`.
A alternativa seria `allow create: if true`, um endereço de escrita aberto a qualquer um na
internet.

**Fricção operacional:** exige habilitar o provedor **Anônimo** no console do Firebase, no
projeto institucional `revisao-minuta-cbmro-6f248` — mesma caminhada de publicar as
`firestore.rules` (o CLI local está numa conta pessoal sem acesso ao projeto).

## 4. Telas novas

- **`src/pages/AcervoPublico.jsx`** — casca própria: cabeçalho com brasão e título, selo
  "Consulta pública", navegação de dois itens (Acervo Legal · Busca) e o link
  "Sou membro — entrar". **Sem `ScenarioSwitcher`**: o acervo é compartilhado entre os
  cenários LOB atual e futura (`states_data.json`, `organs_detail/`), então escolher
  cenário não mudaria nada nessas telas.
- **`src/pages/CadastroVisitante.jsx`** — nome completo, e-mail e instituição/órgão, com
  validação simples e uma linha curta informando para que os dados servem e quem os vê
  (registro de acesso, visível ao administrador do portal). Custa uma frase e evita
  coletar dado pessoal em silêncio.

O bloco de marca do cabeçalho sai de `Header` (`src/App.jsx`) para um componente
compartilhado, para as duas cascas não divergirem visualmente com o tempo.

## 5. Administração

`/acessos` ganha a seção **"Visitantes do acervo público"**: lista somente leitura — nome,
e-mail, instituição, primeiro e último acesso — com contador, ordenada pelo acesso mais
recente. **Sem botões de ação**, conforme a decisão de não haver bloqueio.

O feed usa `onSnapshot` **com estado de erro visível** (`AvisoSincronizacao`), nunca um
`catch` que só escreve no console — a armadilha **AR-04** do catálogo
(`docs/superpowers/auditoria-armadilhas.md`).

## 6. Testes e verificação

Lógica pura em `src/lib/visitante.js`, testada com `node --test`, no padrão da casa:

- normalização e validação dos campos do cadastro (trim, `normalizeEmail`, obrigatoriedade,
  limites de tamanho espelhando a regra do Firestore);
- resolução de rota do `AcervoBase`: ficha do estado prefixada no visitante e não no
  membro, e o "voltar" mapeado para `/acervo-publico` no visitante contra `/estados` no
  membro (o caso que um prefixo cego erraria).

Componentes React não têm suíte neste projeto. **Não há navegador no ambiente do agente**,
então a conferência visual das telas e o teste do cadastro ponta a ponta ficam com o
Ten. Tiago, com o dev server em http://localhost:5173.

Verificação manual mínima antes de considerar pronto:
1. Deslogado, `/acervo-publico` mostra o formulário; preenchido, entra no Acervo.
2. Recarregar a página não pede o cadastro de novo.
3. `/acervo-publico/estados/ro` abre a ficha e o botão "voltar" retorna a `/acervo-publico`
   (nunca a `/estados`, que está fora do recorte).
4. Digitar `/minuta` ou `/regulamento` como visitante **não** abre nada da curadoria.
5. Logado como membro, `/acervo-publico` leva a `/legislacoes`.
6. Em `/acessos`, o administrador vê o visitante recém-cadastrado.

## 7. Fora de escopo (de propósito)

Verificação de e-mail, exportação CSV dos visitantes, limite de cadastros por IP, e
qualquer acesso público às minutas (Regimento Interno, Regulamento Geral) ou às telas de
curadoria. Se algum desses importar, é entrega própria.
