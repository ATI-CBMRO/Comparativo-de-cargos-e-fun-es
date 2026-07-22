# Frente B — Curadoria do RI no Obsidian — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) ou superpowers:executing-plans. Steps use checkbox (`- [ ]`) syntax.

**Goal:** Semear no vault a curadoria do Regimento Interno (LOB futura): índice + fontes + 27 notas de órgão (26 da LOB + Guarnição) + decisões onde os estados divergem de verdade — espelho do formato validado do Regulamento.

**Architecture:** Dados de `database/minuta_structure.json` (capítulos `kind:'organ'` com `sections` de RO e `alternatives` verbatim de até 25 estados — Bloco D) e `database/organs_detail/` quando precisar de contexto. NUNCA os .md crus. Ondas paralelas de órgãos (arquivos disjuntos), revisor por lote.

**Tech Stack:** Markdown Obsidian; Python só para extrair/verificar do JSON (heredoc, scratchpad).

## Global Constraints

- Spec: `docs/superpowers/specs/2026-07-22-ri-curadoria-obsidian-design.md`.
- Pasta nova do vault: `/Users/wandriobandeira/Documents/Obsidian Vault/Codebases/Comparativo-de-cargos-e-funcoes/Regimento Interno — Curadoria/`.
- Formato de referência OBRIGATÓRIO (ler antes de escrever): notas da pasta irmã `Regulamento — Curadoria/` (`_Índice…`, `Tema — servico-operacional.md`, uma nota de decisão).
- Verbatim absoluto nas decisões (citações do JSON com `cf.` exato; OCR defeituoso reproduzido + anotado em itálico FORA da citação); "## Decisão CBMRO" vazia, `decidido: false`.
- Divergência REAL = estrutura/subordinação/competência conflitante entre estados para o MESMO órgão — não redação diferente. Sem divergência → zero decisões + frase explícita.
- Nomes-contrato: `_Índice — Curadoria do Regimento Interno.md` · `Fonte — <slug>.md` (REUSAR as notas de fonte existentes da pasta do Regulamento quando for o MESMO documento — checar por `ls` antes de criar; wikilink resolve vault-wide) · `Órgão — <organKey>.md` · `Decisão — ri — <organKey> — <assunto>.md`.
- pt-BR de gestor; nada de código do repo alterado; nenhuma nota existente de outra pasta editada (exceto: adicionar UMA linha de ligação no `_Índice — Curadoria do Regulamento.md` apontando para o novo índice, na Task final).
- Lacunas conhecidas a registrar: `guarnicao` (matéria de RISD, sem RI equivalente) e `gbm` (homônimo no RS descartado no Bloco D).

---

### Task B1: Infraestrutura — índice + notas de fonte faltantes

- [ ] Extrair do `minuta_structure.json`: lista dos capítulos `kind:'organ'` (organKey, chapterTitle, nº sections, estados em `alternatives` + docLabel de cada) → scratchpad.
- [ ] Levantar o conjunto de documentos-fonte das `alternatives`; comparar com as notas `Fonte — *` já existentes na pasta do Regulamento; criar SOMENTE as faltantes (ex.: LOBs/RIs que não alimentam o Regulamento), no formato padrão de nota de fonte, seção "Papel na minuta" citando os órgãos ([[Órgão — <key>]]).
- [ ] Criar `_Índice — Curadoria do Regimento Interno.md`: tabela de órgãos agrupada pelos blocos da LOB (ordem do JSON), status ⚪ para todos; lista de fontes (mistura de notas novas + reusadas); ligações para `[[_Índice — Curadoria do Regulamento]]` e o Diário.
- [ ] Verificar: nomes exatos, wikilinks, contagens. Relatório em `.superpowers/sdd/frenteB-task1-report.md`.

### Tasks B2..B4 (ondas de órgãos — ~9 por onda, arquivos disjuntos)

Para CADA órgão (uma nota por órgão, padrão da nota de Tema do Regulamento adaptado):

- [ ] Extrair o capítulo do órgão do JSON (sections de RO + alternatives) → scratchpad `<organKey>.json`.
- [ ] `Órgão — <organKey>.md`: frontmatter (`type: orgao`, `organKey`, `status: em-curadoria`); resumo do que RO define (por número de seção/tópico, sem colar tudo); tabela de cobertura (estado × órgão equivalente × o que diz, por Art.); "Decisões a tomar" (divergências REAIS) ; "Lacunas"; "Ligações" (fontes usadas + índice + tema do Regulamento que tangencia, se houver).
- [ ] Notas de decisão conforme padrão, com verificação verbatim python de TODOS os excertos (evidência no relatório).
- [ ] Status ⚪→🟡 desses órgãos NO ÍNDICE fica para a Task final (não mexer aqui).
- Onda B2: cg, depdec, condeg + 6 seguintes na ordem do JSON. Onda B3: próximos 9. Onda B4: restantes + guarnicao (lacuna RISD explícita) + gbm (nota sobre o homônimo RS).

### Task B5: Fechamento

- [ ] Índice do RI: status 🟡 nos órgãos semeados; Índice do Regulamento ganha 1 linha de ligação para o do RI.
- [ ] Diário: nova linha na Linha do tempo (contagens reais) + item de material visual (grafo com os 2 domínios conectados).
- [ ] Verificação global: contagem de arquivos; varredura de TODOS os wikilinks (0 quebrados); frontmatter uniforme; relatório final.
