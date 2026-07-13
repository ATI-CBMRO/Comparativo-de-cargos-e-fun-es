# Pendências — Comparativo-de-cargos-e-funcoes
> Backlog canônico. Atualizado por qualquer sessão via /handoff. Não apagar histórico de concluídas do mês.

## 🔴 Pendente
- [ ] **Camada 2/3 dos documentos ingeridos em 2026-07-13** (camada 1 concluída):
  - **MA - Portaria 46** (Regimento de Serviços) → candidato à Minuta de Regulamento (`regulamento_enrichment_ma.py`).
  - **PA - Regulamento de serviço** (Regimento de Serviços) → candidato à Minuta de Regulamento (`regulamento_enrichment_pa.py`; PA já tem RI organizacional separado).
  - **MT/SE**: renomeações só corrigiram o rótulo no acervo; já cobertos na trilha de Regulamento (referências de nome de arquivo atualizadas em `regulamento_enrichment.py`/`extrair_regulamentos.py`/`sugerir_equivalencias.py`).
- [ ] `database/documents_index.json` — artefato órfão (não é lido por nenhum código nem gerado pela pipeline); referencia os nomes antigos de MT/SE. Atualizar ou remover numa faxina futura.
- [ ] Organograma — validar a **classificação por natureza** (Direção/Apoio/Execução) dos órgãos: foi inferida, não veio rotulada da LOB. Origem: sessão organograma 10/07/2026.
- [ ] Organograma (aba Projeção territorial) — validar o **mapeamento proposto** GBM→Batalhão, COB→Comando Regional, Subgrupamento→Companhia/Pelotão, +BIFEA (nova). Depende da redação final da nova LOB. Origem: 10/07/2026.
- [ ] Lacuna de dados — extrair **texto verbatim** dos estados que só têm competências (ex.: MT no Comando-Geral). Curadoria por estado/órgão. Origem: reforma Subsídio.
- [ ] Regulamento — Diagramas e abas Estrutura/LOB do Subsídio estão como **"em breve"** (agora visíveis em produção). Dependem de dados a curar (commandChart do Regulamento).

## 🟡 Em andamento
- [ ] Faxina do CLAUDE.md — FEITA (481→225 linhas, ~9k→~3,6k tokens; corrigiu rotas/menu/sidebar defasados pós-reforma, adicionou Organograma/Manual/login). PR aberto, aguardando revisão do Tiago (repo compartilhado). 10/07/2026.

## ✅ Concluído (mês atual)
- [x] **Santa Catarina — LOB corrigida (13/07/2026).** Os PDFs da ALESC vinham escaneados (sem OCR).
  Substituídos pelas versões legíveis: **LC nº 724/2018** (`Santa Catarina - Organização Básica.pdf`,
  a LOB real) + **LC nº 885/2025** (`Santa Catarina - Organização Básica alterações.pdf`, altera a LOB) —
  ambas geradas do texto oficial da ALESC (PDF pesquisável via reportlab), classificadas como LOB. O
  Decreto nº 1.328/2021 (que era o antigo "Organização Básica", rotulado Regimento Interno) foi
  DESCARTADO — é superseded pela LOB real, por decisão do Tiago. Override de SC removido do
  `build_states_data.py`.
- [x] Organograma — página `/organograma` (Geral) com 7 visualizações; EM PRODUÇÃO via PR #10 — 10/07/2026.
- [x] Reforma das minutas (trilhas espelhadas, Subsídio unificado, Manual, menu enxuto) — EM PRODUÇÃO junto do PR #10 — 10/07/2026.
- [x] Login — link "Primeiro acesso? Criar minha senha" → /cadastro; EM PRODUÇÃO via PR #11 — 10/07/2026.
