# Design — Proposta com IA (Gemini) a partir das sugestões relevantes

**Data:** 2026-06-27
**Galho:** `feat/revisao-colaborativa-minuta`
**Status:** aprovado para escrita do plano

## 1. Objetivo

Na janela de curadoria do dispositivo (`/revisao`, visão do admin), permitir gerar — com IA —
uma **nova proposta de texto** do dispositivo, consolidando o **texto atual** com as **sugestões
marcadas como relevantes**. A proposta aparece como referência e **pré-preenche** o campo de
**texto final**, que o admin edita e salva. Inclui correção do botão "Salvar e fechar".

## 2. Decisões (validadas com o usuário)

| Tema | Decisão |
|------|---------|
| Base da geração | **Texto atual + sugestões relevantes** (consolida). |
| Disparo | **Botão automático** "✨ Gerar proposta com IA" na janela do dispositivo (só admin). |
| Apresentação | 3 estágios empilhados: **Texto atual → Proposta da IA (referência) → Texto final (editável)**. |
| Motor | **Gemini** (Google), modelo rápido e gratuito (ex.: `gemini-2.0-flash`). |
| Custo | Plano **gratuito** do Gemini cobre a revisão (R$ 0); paga seria centavos. |
| Segredo | Chave do Gemini só no servidor (Vercel env + `.env` local, no `.gitignore`). Nunca no front. |

## 3. Arquitetura

```
Frontend React (/revisao)
  → POST /api/gerar-proposta   (função serverless — guarda a chave)
     → Gemini API (generateContent)
  ← { proposta: "<texto consolidado>" }
```

Por que a função no meio: a chave do Gemini é **secreta**. Se chamássemos o Gemini direto do
navegador, a chave vazaria. A função serverless roda no servidor (Vercel), guarda a chave e só
devolve o texto.

### Componentes (criar/alterar)
- **`api/_gerarProposta.js`** (lógica compartilhada, sem framework): `buildPrompt(textoAtual, sugestoesRelevantes)`
  e `gerarPropostaCore({ textoAtual, sugestoes, apiKey, model })` — monta o prompt, chama o Gemini via
  `fetch`, extrai e devolve o texto. Sem SDK (usa `fetch` nativo do Node 18+).
- **`api/gerar-proposta.js`** (função serverless Vercel): valida método POST, lê `process.env.GEMINI_API_KEY`,
  chama `gerarPropostaCore`, responde JSON. Trata erros (sem chave → 500 com mensagem; corpo inválido → 400).
- **`vite.config.js`** (dev): novo middleware `configureServer` que atende `POST /api/gerar-proposta`
  localmente chamando a MESMA `gerarPropostaCore`, lendo a chave via `loadEnv(mode, cwd, '')`
  (`GEMINI_API_KEY`). Assim funciona no `npm run dev` sem `vercel dev`.
- **`src/lib/gerarProposta.js`** (front): `gerarProposta({ textoAtual, sugestoesRelevantes }) => Promise<string>`
  — faz `fetch('/api/gerar-proposta', { method:'POST', body: JSON.stringify(...) })` e devolve `proposta`.
- **`src/components/RevisaoModal.jsx`** (alterar): mostra o **Texto atual**; botão "✨ Gerar proposta com IA"
  (só admin, habilitado quando há ≥1 relevante); estados de carregando/erro; caixa **Proposta da IA**;
  pré-preenche o campo **Texto final** com a proposta; **fecha a janela** ao "Salvar e fechar".
- **`src/pages/Revisao.jsx`** (alterar): passa as `sugestoesRelevantes` (adminStatus === 'relevante')
  do dispositivo aberto ao modal; mantém `onSaveFinal` e adiciona o fechar ao salvar-e-fechar.

### Prompt (essência, em PT-BR)
Instrução ao modelo: "Você é um redator legislativo. Reescreva o dispositivo a seguir incorporando
as sugestões pertinentes, preservando a técnica legislativa e o estilo. Responda **apenas** com o
texto final do dispositivo, sem comentários." + `TEXTO ATUAL:` + `SUGESTÕES RELEVANTES:` (lista).

## 4. Dados

Nenhuma coleção nova. A proposta da IA é **efêmera** (pode regenerar). Só o **texto final** continua
sendo persistido em `finalTexts/{dispositivoId}` (já existente). Não gravamos a proposta crua.

## 5. Erros e limites
- Sem sugestões relevantes → botão desabilitado com dica "marque ao menos uma sugestão como relevante".
- Falha de rede/Gemini → mensagem "Não foi possível gerar agora. Tente de novo." (o campo final
  permanece intacto/editável).
- Chave ausente no servidor → função responde erro claro; front mostra a mensagem acima.

## 6. Segurança
- Chave do Gemini **nunca** no frontend (só `process.env`/`.env`).
- O endpoint `/api/gerar-proposta` é público (qualquer um poderia chamá-lo). No plano gratuito o pior
  caso é consumir cota. **Mitigação v2 (fora deste escopo):** exigir e validar o token de login do
  Firebase na função. Documentado como melhoria; aceitável para a v1 por custo/risco baixos.

## 7. Correção acoplada
O botão **"Salvar e fechar"** passará a **fechar a janela** após salvar (hoje só salva o status e a
janela fica aberta — o que parecia "travado").

## 8. Testes
- `api/_gerarProposta.test.js` (`node --test`): `buildPrompt` inclui o texto atual e cada sugestão
  relevante; e o parser extrai o texto de uma resposta simulada do Gemini.
- Verificação manual: marcar relevantes → gerar → conferir proposta + campo preenchido → editar → salvar e fechar.

## 9. Escopo
**Inclui:** função segura (Vercel + dev), botão gerar, 3 estágios na janela, pré-preenchimento, correção
do salvar-e-fechar, tratamento de erro, testes do prompt/parser.
**Fora (futuro):** destaque visual das diferenças (diff) na proposta; proteção do endpoint por token;
geração em lote de vários dispositivos.
