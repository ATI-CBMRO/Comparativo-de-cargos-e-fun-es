# Configuração do Firebase — Revisão Colaborativa

## Publicar as Security Rules
1. Console do Firebase → **Firestore Database** → aba **Regras**.
2. Cole o conteúdo de `firestore.rules` (na raiz do repositório) e clique em **Publicar**.

## Cadastrar um convidado (v1)
1. **Authentication → Adicionar usuário**: e-mail + senha inicial. Copie o **UID**.
2. **Firestore → coleção `members` → documento com ID = UID** e campos:
   - `nome` (string), `role` (string: `participante` ou `admin`), `ativo` (boolean: `true`).
3. Avise a pessoa do e-mail e da senha inicial (ela troca depois via "Esqueci minha senha").

## Verificar as regras (Rules Playground)
No editor de Regras, use **Simulação/Playground**:
- Leitura de `members/{uid}` autenticado como um UID **fora** da coleção → deve **negar**.
- Leitura autenticado como um UID **com** `ativo:true` → deve **permitir**.
- `create` em `suggestions` com `autorUid` ≠ uid do autenticado → deve **negar**.
- `write` em `finalTexts` autenticado como `participante` → deve **negar**; como `admin` → **permitir**.

## Acervo público (visitante sem login) — 2026-08-18

Dois passos **manuais** no console do projeto `revisao-minuta-cbmro-6f248`, na conta
institucional (o CLI local está numa conta pessoal sem acesso ao projeto):

1. **Authentication → Sign-in method → Anônimo → Ativar.** Sem isso o cadastro do
   visitante falha com `auth/operation-not-allowed`, e a tela mostra
   "O acesso público ainda não foi habilitado no servidor".
2. **Firestore → Regras:** publicar o `firestore.rules` deste repositório, que passou a
   conter o bloco `match /visitantes/{uid}`.

Conferência depois de publicar: abrir `/acervo-publico` numa janela anônima, preencher o
cadastro e verificar se a pessoa aparece em `/acessos`, seção "Visitantes do acervo
público".

## Envio de documentos pelo visitante (upload) — 2026-08-19

**Pré-requisito que pode custar dinheiro:** o Cloud Storage **não estava provisionado**
neste projeto (verificado em 2026-08-19: o bucket
`revisao-minuta-cbmro-6f248.firebasestorage.app` respondia 404). Desde outubro de 2024 o
Firebase exige o **plano Blaze** (pago por uso, com cota gratuita mensal) para criar o
bucket padrão. Sem o bucket, a tela de envio existe mas nenhum arquivo sobe.

Passos manuais no console do projeto `revisao-minuta-cbmro-6f248`, na conta institucional:

1. **Build → Storage → "Começar"**, para provisionar o bucket padrão (exige o plano Blaze).
2. **Firestore → Rules:** republicar o `firestore.rules`, que passou a conter o bloco
   `match /uploadsVisitantes/{id}`. **Publique este passo antes do próximo** — na ordem
   inversa, um envio na janela entre as duas publicações sobe o arquivo no Storage e falha
   ao gravar o metadado (a coleção ainda não seria aceita pelas regras vigentes), deixando
   um arquivo órfão de até 20 MB, invisível pela interface (a caixa de entrada do admin lê
   do Firestore, não do Storage).
3. **Storage → Rules:** publicar o `storage.rules` deste repositório (arquivo novo — antes
   desta entrega o projeto não tinha nenhuma regra de Storage).

Conferência depois de publicar: abrir `/acervo-publico/enviar` como visitante, enviar um PDF
pequeno, e verificar se ele aparece em `/acessos`, seção "Documentos enviados por
visitantes", com o botão **Baixar** funcionando.
