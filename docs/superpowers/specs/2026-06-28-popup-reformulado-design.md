# Design — Reformulação do popup do dispositivo (layout B)

**Data:** 2026-06-28
**Galho:** `feat/revisao-colaborativa-minuta`
**Status:** aprovado (mockup validado)

## Objetivo
Reorganizar a janela (`RevisaoModal`) em **duas colunas**, com o texto em discussão em destaque
no cabeçalho, interações ao lado do participante e a redação (IA + texto final) separada das sugestões.

## Decisões (mockup aprovado)
1. **Cabeçalho com destaque** para o texto em discussão: rótulo "● Em discussão" (vermelho), a
   referência do dispositivo (`dispositivo.label`) e o `dispositivo.trecho` numa caixa com **barra
   vermelha à esquerda, fonte serifada maior**.
2. **Corpo em duas colunas:**
   - **Esquerda — Sugestões (N):** cada cartão tem, na **mesma linha do participante**, os emojis de
     interação **👍** (curtir + contador) · **✅** (relevante) · **⛔** (descartar) · **🗑️** (excluir),
     com o selo *Relevante/Descartada* à direita; o texto da sugestão abaixo. No rodapé da coluna, a
     caixa **"Sua sugestão"** (volta a existir).
   - **Direita — Redação final:** botão **✨ Gerar proposta com IA** → caixa **Proposta da IA** (quando
     gerada) → **Texto final (editável)** → **Salvar rascunho / Salvar e fechar**. **Sem** a caixa
     "Texto atual" (já está no cabeçalho).
3. **Emojis** substituem os ícones lucide nas interações da sugestão (curtir/relevante/descartar/excluir).

## Papéis
- **Admin:** vê os emojis ✅/⛔ (curadoria), a coluna de redação editável e o botão de IA.
- **Participante:** vê 👍 (e 🗑️ só na própria); a coluna direita mostra o **texto final em leitura**
  (ou "ainda sem texto final"); a caixa "Sua sugestão" disponível para todos.

## Layout/responsivo
- `.rev-modal` mais larga (~máx. 920px) para acomodar 2 colunas; em telas estreitas (≤720px) as
  colunas **empilham** (CSS `flex-wrap`/media query).

## Fora de escopo
Sem mudança de dados, regras ou fluxo de IA — é só reorganização visual de `RevisaoModal.jsx` + CSS.
Diff colorido da proposta e proteção de endpoint seguem fora (como já registrado).

## Teste
Verificação manual: abrir um dispositivo como admin (2 colunas, header em destaque, emojis na linha do
autor, redação à direita, sem caixa "texto atual"); como participante (sem ✅/⛔, redação só leitura).
