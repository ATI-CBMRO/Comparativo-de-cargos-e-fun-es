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
