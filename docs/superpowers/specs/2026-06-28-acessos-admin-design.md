# Design — Aba "Acessos" (gestão de convidados, cadastro e logins)

**Data:** 2026-06-28
**Galho:** `feat/revisao-colaborativa-minuta`
**Status:** aprovado (mockup validado)

## Objetivo
Dar ao administrador uma aba **/acessos** para: convidar pessoas por e-mail, ver quem se cadastrou
(ou só foi convidado), controlar papéis, bloquear/liberar/remover acesso e acompanhar o **último login**
(inclusive "nunca entrou"). Inclui página de **autocadastro** para o convidado criar a própria senha.

## Decisões (validadas)
- **Modelo de acesso:** admin **libera o e-mail** (convite); a pessoa **se cadastra sozinha** criando a
  própria senha (sem servidor pago).
- **Sem verificação de e-mail** no cadastro (confia na lista de autorizados).
- **Ao cortar acesso, as sugestões da pessoa permanecem** (histórico preservado).
- **Identificação por e-mail:** a coleção de membros passa a ser indexada por e-mail (não mais por UID),
  para permitir listar convidados que ainda não entraram.

## Mudança de modelo de dados (refator pequeno)
Coleção **`members/{email}`** (id = e-mail em minúsculas):
- `email` (string), `nome` (string)
- `role`: `'participante' | 'admin'`
- `ativo`: bool (bloquear/liberar)
- `status`: `'convidado' | 'cadastrado'`
- `uid`: string | null (preenchido quando a pessoa cria a conta)
- `criadoEm`, `criadoPor`
- `ultimoLogin`: timestamp | null (`null` = nunca entrou)

> Hoje há só 1 doc (admin, indexado por UID). Migração: recriar como `members/<email-do-admin>`
> (passo manual no console / extensão; o doc antigo por UID pode ser apagado).

## Fluxo
1. **Convite:** admin adiciona `members/{email}` com `status:'convidado'`, `ativo:true`, `uid:null`.
2. **Autocadastro (`/cadastro`):** convidado informa e-mail + senha → `createUserWithEmailAndPassword`.
   Se o e-mail não estiver na lista (ou inativo) → mensagem "acesso não liberado" + `signOut`.
3. **Login (`/login`) e cadastro:** o `AuthProvider` lê `members/{email}`; se existe e `ativo`, autoriza e
   **atualiza** `uid`, `status:'cadastrado'`, `ultimoLogin: serverTimestamp()`.

## Componentes
- **`src/lib/auth.jsx`** (refator): autorização por e-mail; registra `ultimoLogin`/`uid`/`status` no login;
  expõe `cadastrar(email, senha)`.
- **`src/lib/membersData.js`**: `subscribeMembers(cb)`, `addMember({email,nome,role})`,
  `setMemberRole(email,role)`, `setMemberAtivo(email,ativo)`, `removeMember(email)`.
- **`src/lib/membersStats.js`** (lógica pura, testável): `contaStatus(members)` → `{total, cadastrados, convidados, bloqueados}`.
- **`src/pages/Cadastro.jsx`**: página pública de autocadastro (e-mail + senha + confirmar).
- **`src/pages/Acessos.jsx`**: aba admin — cartões-resumo, "Convidar pessoa" (e-mail, nome, papel) e tabela
  (Pessoa, Papel, Status, Último login, Ações: papel / bloquear-liberar / remover).
- **`src/App.jsx`**: rotas `/cadastro` (pública) e `/acessos` (protegida, `requireAdmin`); item de menu
  **"Acessos"** visível só para admin (e item **"Revisão"** para quem está logado, p/ navegação).
- **`firestore.rules`**: regras por e-mail (abaixo).

## Security Rules (essência)
```
function memberDoc() { return get(/databases/$(database)/documents/members/$(request.auth.token.email)); }
function isMember() {
  return request.auth != null
    && exists(/databases/$(database)/documents/members/$(request.auth.token.email))
    && memberDoc().data.ativo == true;
}
function isAdmin() { return isMember() && memberDoc().data.role == 'admin'; }

match /members/{email} {
  allow read:   if isAdmin() || (request.auth != null && request.auth.token.email == email);
  allow create, delete: if isAdmin();
  allow update: if isAdmin()
    || (request.auth != null && request.auth.token.email == email
        && request.resource.data.diff(resource.data).affectedKeys().hasOnly(['uid','status','ultimoLogin']));
}
// suggestions/finalTexts: mantêm as regras atuais (isMember/isAdmin agora baseados em e-mail).
```

## Erros e limites
- E-mails tratados em **minúsculas** (entrada do admin normalizada; `request.auth.token.email` deve bater).
  Limitação conhecida: se o provedor preservar maiúsculas no token, pode haver divergência — orientar uso
  de e-mails minúsculos (Firebase normalmente já normaliza).
- Autocadastro com e-mail não convidado: conta órfã sem acesso (inofensiva; rules bloqueiam tudo).
- Senha fraca / e-mail já em uso: mensagens claras na página de cadastro.

## Fora de escopo (futuro)
Reenvio de "convite por e-mail" automático; verificação de e-mail; contagem de sugestões por pessoa na
tabela; exportar lista.

## Testes
- `membersStats.test.js` (`node --test`): contagem por status.
- Rules: verificação no console (admin lê tudo; membro lê só o próprio; participante não escreve members).
- Manual ponta a ponta: convidar → autocadastrar → ver status/último login → bloquear → remover.
