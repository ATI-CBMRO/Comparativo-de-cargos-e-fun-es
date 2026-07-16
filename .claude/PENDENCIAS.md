# Pendências — Comparativo-de-cargos-e-funcoes
> Backlog canônico. Atualizado por qualquer sessão via /handoff. Não apagar histórico de concluídas do mês.

## 🔴 Pendente
- [ ] **Cenário atual — Subsídio** (`/minuta/subsidio` e `/regulamento/subsidio`): ainda gated no atual. Depende de gerar o `comparativo_minuta` do atual (comparação dispositivo-a-dispositivo com outros estados). Origem: sessão cenários 15-16/07/2026.
- [ ] **Integrar a branch `feat/auditoria-seguranca-e-comparador-regulamento` ao remoto**: 18 commits locais (Fase 1 + Fase 2 dos cenários) só na máquina — envio ao GitHub pendente por segurança (repo institucional ATI-CBMRO). Decidir com o Wândrio: abrir PR ou enviar a branch.
- [ ] Organograma — validar a **classificação por natureza** (Direção/Apoio/Execução) dos órgãos: foi inferida, não veio rotulada da LOB. Origem: sessão organograma 10/07/2026.
- [ ] Organograma (aba Projeção territorial) — validar o **mapeamento proposto** GBM→Batalhão, COB→Comando Regional, Subgrupamento→Companhia/Pelotão, +BIFEA (nova). Depende da redação final da nova LOB. Origem: 10/07/2026.
- [ ] Lacuna de dados — extrair **texto verbatim** dos estados que só têm competências (ex.: MT no Comando-Geral). Curadoria por estado/órgão. Origem: reforma Subsídio.
- [ ] Regulamento — Diagramas e abas Estrutura/LOB do Subsídio estão como **"em breve"** (agora visíveis em produção). Dependem de dados a curar (commandChart do Regulamento).

## 🟡 Em andamento
_(nenhum)_

## ✅ Concluído (mês atual)
- [x] **Cenários LOB atual × futura** — chave no topo isola os dois cenários (nunca misturam); dados em gavetas por cenário (futura na raiz, atual em `database/atual/`); acervo dos 27 estados compartilhado. Fase 1 (chave+contexto+seletor+isolamento) — 15/07/2026.
- [x] **Cenário atual — Regimento Interno vigente** (Lei 2.204/2009): 21 capítulos/órgãos com competências verbatim, estrutura validada pelo organograma oficial. Gerador `build_minuta_structure_atual.py` isolado do da futura — 15/07/2026.
- [x] **Cenário atual — Regulamento temático** (15 temas, 410 artigos dos 9 estados), isolado por `reg:atual:`; reusa a curadoria da futura (serviço não depende da LOB) — 16/07/2026.
- [x] **Cenário atual — Diagramas** (commandChart próprio) e **Revisão** destravados; **isolamento do Firebase por cenário** (marcador no editId: atual com `atual:`/`reg:atual:`, futura sem marcador — preserva comentários existentes). Fecha dívida da Fase 1 — 16/07/2026.
- [x] Organograma — página `/organograma` (Geral) com 7 visualizações; EM PRODUÇÃO via PR #10 — 10/07/2026.
- [x] Reforma das minutas (trilhas espelhadas, Subsídio unificado, Manual, menu enxuto) — EM PRODUÇÃO junto do PR #10 — 10/07/2026.
- [x] Login — link "Primeiro acesso? Criar minha senha" → /cadastro; EM PRODUÇÃO via PR #11 — 10/07/2026.
- [x] Faxina do CLAUDE.md — 481→225 linhas (~9k→~3,6k tokens) + correção de defasagens pós-reforma; mesclada via PR #12 — 10/07/2026.
