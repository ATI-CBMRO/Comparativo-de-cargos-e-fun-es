# Pendências — Comparativo-de-cargos-e-funcoes
> Backlog canônico. Atualizado por qualquer sessão via /handoff. Não apagar histórico de concluídas do mês.

## 🔴 Pendente
- [ ] **Curadoria — preencher as 36 "Decisões CBMRO" (com o Wândrio/Tiago)**: 27 do
  Regulamento ("Regulamento — Curadoria/", 16 temas 🟡) + 9 do Regimento Interno
  ("Regimento Interno — Curadoria/", 27 órgãos 🟡). O mecanismo de REGISTRAR e APLICAR a
  decisão já está pronto (cockpit Fase 3, 23/07/2026 — aba Decisões, papel admin) — falta só
  a análise/decisão em si. Delegar papel admin ao Tiago em `/acessos` quando ele começar.
  Orientação de uso em `/manual#cockpit`. Minors registrados p/ rodada futura: padronizar os 2
  estilos de citação do MT adaptado; ruído de cabeçalho de PDF em 2 citações de SE; notas de
  Fonte magras de propósito; elisões sem "[...]" em 2 notas de decisão (cada linha é verbatim).
- [ ] **Ajudância-Geral (ag) — falta o RI do Mato Grosso**: 12 de 25 itens da competência citam
  `cf. CBMMT, RI, Art. 152`, mas o Regimento Interno de MT nunca foi ingerido no acervo (só há
  a LOB e o Regulamento Geral). Sem o PDF não dá pra confirmar nem capturar o excerto. Origem:
  revisões da Frente B, 22/07/2026; investigado e resolvido em parte (dpo/assessorias) em
  23/07/2026 — ver ✅ Concluído.
- [ ] Regulamento — tema `uniformes-apresentacao` segue magro (1 artigo, só SE); DOB-01 de AL
  ("Terminologia Operacional") citada pela DOB-08 mas não ingerida; dimensionamento técnico do
  193 (nº de PAs/troncos) só na DOB-06-AL (lacuna registrada no vault).
- [ ] Cenário atual — Subsídio: **curadoria fina do comparativo** (rodada futura, sob demanda):
  o comparativo do atual usa SÓ casamento automático por palavra-chave (decisão de produto
  22/07/2026, selo na tela); se o Wândrio sentir falta, curar de-para manual dos órgãos
  principais. Origem: fatia Subsídio atual 22/07/2026.
- [ ] **Camada 2/3 dos documentos ingeridos em 2026-07-13** (camada 1 concluída):
  - **MA - Portaria 46** (Regimento de Serviços) → candidato à Minuta de Regulamento (`regulamento_enrichment_ma.py`).
  - **PA - Regulamento de serviço** (Regimento de Serviços) → candidato à Minuta de Regulamento (`regulamento_enrichment_pa.py`; PA já tem RI organizacional separado).
  - **MT/SE**: renomeações só corrigiram o rótulo no acervo; já cobertos na trilha de Regulamento (referências de nome de arquivo atualizadas em `regulamento_enrichment.py`/`extrair_regulamentos.py`/`sugerir_equivalencias.py`).
- [ ] `database/documents_index.json` — artefato órfão (não é lido por nenhum código nem gerado pela pipeline); referencia os nomes antigos de MT/SE. Atualizar ou remover numa faxina futura.
- [ ] Organograma — **alinhar a classificação por natureza à LEI** (achado 22/07/2026): a
  premissa de que "a LOB não rotula natureza" caiu — a minuta da nova LOB (Art. 5º-10) traz
  5 naturezas expressas (Direção Geral/Setorial/Regional, Assessoramento, Apoio, Execução,
  Correição) e a página usa só 3, com **16 divergências** mapeadas (ex.: DP/DEEI/DPOF/DLOG
  são Direção Setorial na lei, não "apoio"; DPO/DOE/COT/CRBM são Direção, não "execução";
  GAB-CG/Ajudância são Apoio na lei). Relatório completo em
  `.superpowers/sdd/verificacao-natureza-organograma.md`. Decidir com o Wândrio: realinhar
  a página à lei (fatia própria) ou manter a leitura didática atual com nota explicativa.
- [ ] Lacuna de dados — extrair **texto verbatim** dos estados que só têm competências (ex.: MT no Comando-Geral). Curadoria por estado/órgão. Origem: reforma Subsídio.
- [ ] Subsídio — abas Estrutura/LOB seguem **"em breve"** (visíveis em produção); dependem de dados a curar. (Diagramas do Regulamento já destravados em 21/07/2026.)

## 🟡 Em andamento
_(nenhum)_

## ✅ Concluído (mês atual)
- [x] **Curadoria RI — 2 das 3 inconsistências de dados resolvidas** (23/07/2026): dpo/PA tinha
  excerto extraído do documento errado (RI em vez da LOB) — corrigido, `match` virou `exata`;
  assessorias/GO citado na competência sem excerto capturado — adicionado (conferido no PDF
  oficial, Art. 17-18). Ajudância-Geral/MT segue pendente (RI de MT nunca ingerido — ver
  🔴 Pendente). `scripts/ri_alternativas_enrichment.py` + `database/minuta_structure.json`
  regenerado; notas do vault atualizadas.
- [x] **Faxina — 4 PNGs soltos + checkpoint descartados** (23/07/2026): screenshots de prova
  de sessões passadas (15/07) e o checkpoint automático pré-compactação — nenhum era
  versionado nem lido por código; descartados a pedido do Wândrio.
- [x] **Cockpit — erros de gravação deixaram de ser silenciosos** (23/07/2026): `saveConferenciaStatus`/
  `marcarFichaAplicada`/`desfazerDecisao` agora mostram um alerta visível na tela quando a
  gravação falha (antes só iam pro `console.error`). Achado não-bloqueante da revisão final da
  Fase 3.
- [x] **Cockpit de curadoria — Fase 1: Conferência linear** (`/minuta/conferencia`,
  `/regulamento/conferencia`): tela de percorrer a minuta dispositivo a dispositivo com as
  referências de outros estados, nos 2 cenários. O Regimento atual reaproveita o Bloco D
  verbatim da futura (de-para validado pelo Wândrio, inclui a correção `cob1/cob2→crbm` —
  AR-01). Prova visual nos 2 cenários; bug de chave duplicada (futura) achado na prova e
  corrigido. Spec/plano `docs/superpowers/*/2026-07-22-cockpit-*`. Registro de armadilhas em
  `docs/superpowers/auditoria-armadilhas.md` (AR-01). — 22/07/2026.
- [x] **Cockpit de curadoria — Fase 2: aba Decisões** (`/minuta/decisoes`,
  `/regulamento/decisoes`): as 36 Decisões CBMRO do vault Obsidian passam a ser lidas dentro
  do portal (Questão + candidatas verbatim + Comparação), filtro Pendentes/Decididas, nos 2
  cenários. Parser reconhece 2 formatos de nota (2/9 notas do Regimento usavam template mais
  antigo) sem editar o vault. Wikilinks crus limpos na revisão final. PR #20. — 23/07/2026.
- [x] **Cockpit de curadoria — Fase 3: registrar e aplicar decisão**: Firebase (`decisions`)
  vira fonte oficial, só admin registra; decisão de REDAÇÃO aponta o artigo alvo manualmente
  (nunca de-para automático — anti-AR-01) e o texto final passa a valer no Wizard e no
  `.docx` (provado baixando o arquivo de verdade); decisão ESTRUTURAL vira ficha de
  aplicação; Conferência persiste por usuário logado; exportação + script devolvem as
  decisões ao vault sem sobrescrever decisão manual divergente; badge visual "final aplicado"
  nos Wizards. Bug real corrigido no caminho: `finalTexts` nunca conseguia gravar (Firestore
  rejeita `/` no id — ver memória `firestore-encoding-dispositivoid`). Guia de metodologia em
  `/manual#cockpit`. Prova real com login (não só testes). PR #21. — 23/07/2026.
- [x] **Cenário atual — Subsídio destravado** (`/minuta/subsidio` e `/regulamento/subsidio`):
  gerador isolado `build_minuta_comparison_atual.py` (21 órgãos da Lei 2.204/2009 × estados,
  SÓ camada automática, teste anti-vazamento da futura), telas resolvendo dados por
  `scenarioDbUrl`, selo "Correspondência automática — sujeita a revisão", gate removido só
  das 2 rotas; futura intocada (diff: só `database/atual/`). Suíte 115/115 — 22/07/2026.
- [x] **Organograma — Projeção territorial VALIDADA pelo Wândrio** (22/07/2026): o de-para
  GBM→Batalhão, COB→Comando Regional, Subgrupamento→Companhia/Pelotão, +BIFEA (nova) está
  aprovado como proposta de projeção (sujeito só à redação final da nova LOB).
- [x] **Organograma oficial da LOB atual inserido no portal** (22/07/2026): no cenário
  "LOB atual", a página `/organograma` mostra o organograma oficial vigente (imagem +
  PDF, mesmo arquivo validado em `docs/curadoria/lob-atual-ro/`); cenário futura intocado.
- [x] **Frente A — resíduos TO/AL/PI resolvidos**: corpo principal de Tocantins (Art. 1-13,16,
  14 art., corte por linha absoluta) e os 4 DOBs de Alagoas 05-08 (37 seções, novo extrator por
  seção numerada) incorporados como ALTERNATIVAS (fonte primária de nenhum tema mudou; 413
  artigos primários intactos; 1166 excertos 100% verbatim); NO-02 de AL confirmada curta (1
  página); LOB do Piauí destravada por OCR (604 bytes → 27,8KB legíveis, PDF `[OCR]` ao lado do
  original); fix: RISG não aparece mais como 28º "estado". Revisão final: pronto p/ entrega,
  0 Critical/Important — 22/07/2026.
- [x] **Frente B — curadoria do Regimento Interno no Obsidian**: pasta "Regimento Interno —
  Curadoria/" com 40 notas (1 índice, 3 fontes novas + 4 reusadas, 27 órgãos da minuta LOB
  futura, 9 decisões RI com candidatas verbatim); vault total 107 notas, 859 wikilinks, 0
  quebrados; Diário atualizado (linha 22/07). Espelho do formato validado do Regulamento;
  revisão independente por lote + revisão final — 22/07/2026.
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
- [x] Faxina do CLAUDE.md — 481→225 linhas (~9k→~3,6k tokens) + correção de defasagens pós-reforma; mesclada via PR #12 — 10/07/2026.
