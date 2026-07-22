# Pendências — Comparativo-de-cargos-e-funcoes
> Backlog canônico. Atualizado por qualquer sessão via /handoff. Não apagar histórico de concluídas do mês.

## 🔴 Pendente
- [ ] **Regulamento — resíduos da Fase 2 (sinalizados, não resolvidos)**: corpo principal de
  Tocantins (Art. 1-13,16 — colide numeração com o Anexo 2 em `atribuicoes-funcoes`); os 4 DOBs
  de Alagoas 05-08 (sem "Art. N", estruturados por seção numerada — extrator atual incompatível);
  tema `uniformes-apresentacao` (sem achado forte no RISG nas faixas lidas, segue com 1 artigo
  só de SE). Origem: spec 2026-07-21 (Fatias B/C/D).
- [ ] **Regulamento — Fase 3 (próximo)**: Wândrio preencher as 27 "Decisões CBMRO" no vault
  ("Regulamento — Curadoria/", 16 temas 🟡); depois, sessão de "aplicar Decisões" nos dados
  do portal (mecanismo a desenhar). Minors registrados p/ rodada futura: padronizar os 2
  estilos de citação do MT adaptado (ambos transparentes); ruído de cabeçalho de PDF em 2
  citações de SE (corrigir no JSON se incomodar); notas de Fonte magras de propósito.
- [ ] **Cenário atual — Subsídio** (`/minuta/subsidio` e `/regulamento/subsidio`): ainda gated no atual. Depende de gerar o `comparativo_minuta` do atual (comparação dispositivo-a-dispositivo com outros estados). Origem: sessão cenários 15-16/07/2026.
- [ ] Organograma — validar a **classificação por natureza** (Direção/Apoio/Execução) dos órgãos: foi inferida, não veio rotulada da LOB. Origem: sessão organograma 10/07/2026.
- [ ] Organograma (aba Projeção territorial) — validar o **mapeamento proposto** GBM→Batalhão, COB→Comando Regional, Subgrupamento→Companhia/Pelotão, +BIFEA (nova). Depende da redação final da nova LOB. Origem: 10/07/2026.
- [ ] Lacuna de dados — extrair **texto verbatim** dos estados que só têm competências (ex.: MT no Comando-Geral). Curadoria por estado/órgão. Origem: reforma Subsídio.
- [ ] Subsídio — abas Estrutura/LOB seguem **"em breve"** (visíveis em produção); dependem de dados a curar. (Diagramas do Regulamento já destravados em 21/07/2026.)

## 🟡 Em andamento
_(nenhum)_

## ✅ Concluído (mês atual)
- [x] **Regulamento — Diagramas destravados** (`/regulamento/diagramas`): decisão de produto —
  o Regulamento é TEMÁTICO, não tem cadeia de comando; em vez de gerar um `commandChart`
  artificial, a tela mostra a **árvore do DOCUMENTO** (Regulamento → 2 Partes → 16 temas,
  montada na tela por `src/lib/regulamentoTree.js`, testada) + mapa mental com faixas por
  Parte; painel lateral extraído para componente compartilhado (`MinutaDetailPanel`), RI
  intocado (prova por screenshot). Funciona nos DOIS cenários (gate `TrilhaRoute` removido
  da rota — achado da revisão final). Spec/plano `docs/superpowers/*/2026-07-21-regulamento-diagramas*` — 21/07/2026.
- [x] **Regulamento — 2 Partes herdadas no Subsídio e na Revisão**: `RegulamentoComparator`
  (aba Regulamento do Subsídio) agrupa capítulos por Parte antes do agrupamento temático
  existente; `Revisao` (modo Regulamento) exibe as faixas "PARTE I — GERAL"/"PARTE II — DO
  SERVIÇO" na troca de Parte. Regimento Interno confirmado intocado visualmente (prova por
  screenshot). `RegDiagramas` segue fora — bloqueado por `commandChart` ausente, pendência
  própria não relacionada. Spec e plano em `docs/superpowers/specs/` e
  `docs/superpowers/plans/2026-07-21-fase1-heranca-2partes-telas.md` — 21/07/2026.
- [x] **Regulamento — Fase 2, Fatias B+C+D** (reforço verbatim, sem mudar fonte primária de
  nenhum tema): Fatia B — resto de Bahia (35 art.), Roraima inteiro (97 art.), resto do Anexo 2
  de Tocantins (15 art.), 5 normas de Alagoas (42 art.) reforçando a Parte II. Fatia C — RISG do
  Exército (67 art.) reforça `cerimonial-honras` e `pessoal-quadros`, entrando como pseudo-fonte
  "Exército Brasileiro", só como alternativa (nunca primária — testado). Fatia D — 9 artigos
  cirúrgicos do CBMES (CAT, 1º BBM, CERD) reforçam `servico-operacional` e
  `seguranca-contra-incendio`. Um vazamento de conteúdo (organograma colado ao Art. 31 do ES)
  foi encontrado na revisão e corrigido antes do merge. 413 artigos primários preservados;
  ganho de ~700 excertos alternativos no total. Spec e plano em
  `docs/superpowers/specs/` e `docs/superpowers/plans/2026-07-21-fase2bcd-*` — 21/07/2026.
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
