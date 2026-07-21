# Pendências — Comparativo-de-cargos-e-funcoes
> Backlog canônico. Atualizado por qualquer sessão via /handoff. Não apagar histórico de concluídas do mês.

## 🔴 Pendente
- [ ] **Regulamento — Fase 2, Fatia B**: reforçar a Parte II com o RESTO de BA/RR/TO (fora do teledespacho) + as 9 normas de Serviço de AL. Origem: spec 2026-07-21.
- [ ] **Regulamento — Fase 2, Fatia C**: tapar os temas magros da Parte I (uniformes, cerimonial, pessoal) com RISG (Títs. VI/VIII) e RS. Origem: spec 2026-07-21.
- [ ] **Regulamento — Fase 2, Fatia D**: acréscimos cirúrgicos do ES (prontidão, salvamento marítimo, vistorias SCI). Origem: spec 2026-07-21.
- [ ] **Regulamento — Fase 3**: curadoria no Obsidian (notas por tema/artigo com backlinks entre estados). Origem: spec 2026-07-21.
- [ ] **Regulamento — herdar 2 Partes** nas telas Subsídio/Diagramas/Revisão (spec §5.4 — fora da Fase 1). Origem: spec 2026-07-21.
- [ ] **Cenário atual — Subsídio** (`/minuta/subsidio` e `/regulamento/subsidio`): ainda gated no atual. Depende de gerar o `comparativo_minuta` do atual (comparação dispositivo-a-dispositivo com outros estados). Origem: sessão cenários 15-16/07/2026.
- [ ] Organograma — validar a **classificação por natureza** (Direção/Apoio/Execução) dos órgãos: foi inferida, não veio rotulada da LOB. Origem: sessão organograma 10/07/2026.
- [ ] Organograma (aba Projeção territorial) — validar o **mapeamento proposto** GBM→Batalhão, COB→Comando Regional, Subgrupamento→Companhia/Pelotão, +BIFEA (nova). Depende da redação final da nova LOB. Origem: 10/07/2026.
- [ ] Lacuna de dados — extrair **texto verbatim** dos estados que só têm competências (ex.: MT no Comando-Geral). Curadoria por estado/órgão. Origem: reforma Subsídio.
- [ ] Regulamento — Diagramas e abas Estrutura/LOB do Subsídio estão como **"em breve"** (agora visíveis em produção). Dependem de dados a curar (commandChart do Regulamento).

## 🟡 Em andamento
_(nenhum)_

## ✅ Concluído (mês atual)
- [x] **Regulamento — Fase 2A**: 16º tema `central-operacoes-193` preenchido — Bahia (CICOM,
  Art. 8-9 Supervisor + Art. 18 Operador de Teledespacho) como primária, Tocantins (Anexo 2,
  Art. 12-14) como alternativa. Roraima ficou de fora (o 193 está difuso no Art. 54, sem
  recorte limpo). Total do Regulamento: 410 → 413 artigos, todos únicos. Spec e plano em
  `docs/superpowers/specs/` e `docs/superpowers/plans/2026-07-21-fase2a-*` — 21/07/2026.
- [x] **Regulamento Geral em 2 Partes — Fase 1 (estrutura)**: campo `parte` (geral/serviço) em cada capítulo, 16º tema `central-operacoes-193` (pendente), reordenação Parte I → Parte II no JSON, no wizard e no `.docx`; herdado pelo cenário atual. 410 artigos preservados (0 removidos/renomeados). Fontes verificadas por leitura de 7 subagentes (round 2) — ver vault `Codebases/Comparativo-de-cargos-e-funcoes/`. Spec e plano em `docs/superpowers/specs/` e `docs/superpowers/plans/2026-07-21-*` — 21/07/2026.
- [x] Cenários LOB — branch `feat/auditoria-seguranca-e-comparador-regulamento` integrada ao remoto via **PR #15** (aguardando revisão/merge) — 16/07/2026.
- [x] **Cenários LOB atual × futura** — chave no topo isola os dois cenários (nunca misturam); dados em gavetas por cenário (futura na raiz, atual em `database/atual/`); acervo dos 27 estados compartilhado. Fase 1 (chave+contexto+seletor+isolamento) — 15/07/2026.
- [x] **Cenário atual — Regimento Interno vigente** (Lei 2.204/2009): 21 capítulos/órgãos com competências verbatim, estrutura validada pelo organograma oficial. Gerador `build_minuta_structure_atual.py` isolado do da futura — 15/07/2026.
- [x] **Cenário atual — Regulamento temático** (15 temas, 410 artigos dos 9 estados), isolado por `reg:atual:`; reusa a curadoria da futura (serviço não depende da LOB) — 16/07/2026.
- [x] **Cenário atual — Diagramas** (commandChart próprio) e **Revisão** destravados; **isolamento do Firebase por cenário** (marcador no editId: atual com `atual:`/`reg:atual:`, futura sem marcador — preserva comentários existentes). Fecha dívida da Fase 1 — 16/07/2026.
- [x] Organograma — página `/organograma` (Geral) com 7 visualizações; EM PRODUÇÃO via PR #10 — 10/07/2026.
- [x] Reforma das minutas (trilhas espelhadas, Subsídio unificado, Manual, menu enxuto) — EM PRODUÇÃO junto do PR #10 — 10/07/2026.
- [x] Login — link "Primeiro acesso? Criar minha senha" → /cadastro; EM PRODUÇÃO via PR #11 — 10/07/2026.
- [x] Faxina do CLAUDE.md — 481→225 linhas (~9k→~3,6k tokens) + correção de defasagens pós-reforma; mesclada via PR #12 — 10/07/2026.
