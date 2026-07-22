# Fase 3 — Rodada 2: replicar a curadoria aos 15 temas restantes — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) ou superpowers:executing-plans. Steps use checkbox (`- [ ]`) syntax.

**Goal:** Criar no vault as 15 notas de Tema restantes + notas de Decisão (onde houver divergência real), no formato validado pelo Wândrio no piloto `servico-operacional` (2026-07-21/22).

**Architecture:** Repetição, POR TEMA, das Tasks 2 e 3 do plano do piloto (`docs/superpowers/plans/2026-07-21-regulamento-fase3-curadoria-obsidian.md`) — os templates de nota de Tema (Task 2, Step 3) e de nota de Decisão (Task 3, Step 1) valem VERBATIM, trocando o themeKey. Temas independentes entre si → execução em ondas paralelas (arquivos disjuntos), revisão por tema.

**Tech Stack:** idem piloto (Markdown Obsidian, Python só para extrair/verificar do JSON).

## Global Constraints

- Herda TODAS as Global Constraints do plano do piloto (mesma pasta do vault, dados só do `database/regulamento_structure.json`, verbatim absoluto com `cf.`, pt-BR de gestor, nada de mudança de código no repo, wikilinks exatos).
- Nomes: `Tema — <themeKey>.md` e `Decisão — <themeKey> — <assunto-slug>.md`.
- Divergência REAL (regras/números/conceitos conflitantes) — não redação diferente da mesma regra. Tema sem divergência = zero notas de decisão (legítimo; registrar "nenhuma divergência real" na seção "Decisões a tomar").
- NÃO tocar nas 24 notas existentes, EXCETO o Índice (troca de status ⚪→🟡 na Task final) — e no Índice, só a coluna Status.
- Frontmatter da nota de tema: `parte:` conforme o campo `parte` do capítulo no JSON (geral|servico); `status: em-curadoria`.
- Extração por tema: mesmo comando do piloto (Task 2, Step 1) trocando o themeKey; gravar `<themeKey>.json` no scratchpad da sessão.

## Os 15 temas (ordem de execução; parte; primária conforme JSON)

Parte I: `disposicoes-preliminares`, `organizacao-geral`, `competencias-direcao`,
`competencias-apoio-assessoramento`, `competencias-execucao`, `disciplina-correicao`,
`uniformes-apresentacao`, `cerimonial-honras`, `ensino-instrucao`,
`seguranca-contra-incendio`, `pessoal-quadros`, `disposicoes-finais`.
Parte II: `servico-interno-dia`, `atribuicoes-funcoes`, `central-operacoes-193`.

---

### Task N (uma por tema, N=1..15): Tema + Decisões de `<themeKey>`

**Files:** Create no vault: `Tema — <themeKey>.md` + `Decisão — <themeKey> — *.md` (0..k).

**Interfaces:** Consome os nomes `Fonte — <slug>` já existentes (mapa slug↔jsonKey na Task 1 do plano do piloto). Produz notas autocontidas; nenhuma task depende de outra.

- [ ] Step 1: Extrair o tema do JSON para o scratchpad (comando do piloto Task 2 Step 1, themeKey trocado).
- [ ] Step 2: Ler TODO o material (artigos primários + alternatives); analisar assuntos, cobertura, divergências reais, lacunas.
- [ ] Step 3: Escrever `Tema — <themeKey>.md` (template do piloto Task 2 Step 3; cabeçalho com primária/alternativas e contagens reais do JSON).
- [ ] Step 4: Para cada divergência real, escrever a nota de Decisão (template do piloto Task 3 Step 1) com excertos verbatim (incluindo `dispositivos`), `cf.` exato e "## Decisão CBMRO" vazia.
- [ ] Step 5: Verificar — verbatim caractere a caractere de TODOS os excertos citados (colar evidência no relatório); simetria tema↔decisões; wikilinks exatos.

### Task 16: Índice, Diário e fechamento

- [ ] Step 1: No `_Índice — Curadoria do Regulamento.md`, trocar o Status dos 15 temas para 🟡 (nada mais muda; `servico-operacional` mantém 🟡).
- [ ] Step 2: Acrescentar linha à Linha do tempo do Diário: data 2026-07-22, "Fase 3 rodada 2 — 15 temas restantes semeados (X notas de decisão no total); curadoria completa aguardando as Decisões CBMRO do Wândrio", fonte técnica: este plano.
- [ ] Step 3: Verificação global — contagem final de arquivos na pasta; varredura de wikilinks quebrados (typos) em todas as notas novas; reportar contagens por tema.
