# Pendências — Comparativo-de-cargos-e-funcoes
> Backlog canônico. Atualizado por qualquer sessão via /handoff. Não apagar histórico de concluídas do mês.

## 🔴 Pendente
- [ ] **Curadoria — Decisões do REGIMENTO INTERNO para a LOB ATUAL (não existem ainda)**:
  as 9 decisões de RI do vault foram todas redigidas sobre a **LOB futura** (discutem BBS,
  CRBM, DEPDEC, DOE, COT, dpof, gab-cg — sem equivalente na Lei 2.204/2009). Desde
  29/07/2026 elas aparecem SÓ no cenário futura, e o cenário atual mostra estado vazio
  explicativo. Para o atual é preciso curar decisões novas sobre os **21 órgãos da Lei
  2.204/2009** (pasta "Regimento Interno — Curadoria/" do vault), marcando `cenarios: atual`
  no frontmatter da nota. As 27 do Regulamento são temáticas e seguem valendo nos 2 cenários.
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
  23/07/2026 — ver ✅ Concluído. **Ampliado pela auditoria (23/07/2026):** `cinf` também
  cita o RI de MT (`cf. CBMMT, RI, Art. 129`) sem fonte no acervo — mesma solução (ingerir
  o RI de MT) resolve os dois.
- [ ] Regulamento — tema `uniformes-apresentacao` segue magro (1 artigo, só SE) — matéria que
  pede um regulamento próprio de uniformes (RUMBM) no médio prazo, não uma lacuna a forçar
  agora. DOB-01 de AL investigada e descartada (23/07/2026 — ver ✅ Concluído): é glossário
  técnico, sem termos de uniforme/apresentação aproveitáveis. Dimensionamento técnico do 193
  (nº de PAs/troncos), só na DOB-06-AL, segue lacuna registrada no vault.
- [ ] Cenário atual — Subsídio: **curadoria fina do comparativo** (rodada futura, sob demanda):
  o comparativo do atual usa SÓ casamento automático por palavra-chave (decisão de produto
  22/07/2026, selo na tela); se o Wândrio sentir falta, curar de-para manual dos órgãos
  principais. Origem: fatia Subsídio atual 22/07/2026.
- [ ] **Camada 2/3 dos documentos ingeridos em 2026-07-13** (camada 1 concluída):
  - **MA - Portaria 46** (Regimento de Serviços) → candidato à Minuta de Regulamento (`regulamento_enrichment_ma.py`).
  - **PA - Regulamento de serviço** (Regimento de Serviços) → candidato à Minuta de Regulamento (`regulamento_enrichment_pa.py`; PA já tem RI organizacional separado).
  - **MT/SE**: renomeações só corrigiram o rótulo no acervo; já cobertos na trilha de Regulamento (referências de nome de arquivo atualizadas em `regulamento_enrichment.py`/`extrair_regulamentos.py`/`sugerir_equivalencias.py`).
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

- [ ] **Guard-rail para `editId#index` entre rodadas (AR-03)**: a estabilidade do endereço
  dos comentários/textos finais depende da CONVENÇÃO de congelar `minuta_structure.json`
  durante a rodada — regenerar o JSON inserindo inciso no meio desloca todos os comentários
  posteriores em silêncio. Proposta a decidir: gravar um hash/versão do structure junto de
  cada sugestão/final e avisar na tela quando divergir. Achado da auditoria 23/07/2026.

## 🟡 Em andamento
- [ ] **Curadoria do Regulamento à luz da LOB vigente — handoff Wândrio→Tiago (2026-08-13,
  branch `fix/curadoria-lob-atual`, ainda não mesclada)**: a minuta importada de MT/SE/BA/RN/RS
  só trocou nome de estado, nunca estrutura organizacional — 32 nomes de órgão sem lastro em
  nenhuma LOB de RO. Relatório completo em
  `docs/superpowers/specs/2026-08-13-revisao-curadoria-lob-atual.md`, plano de tarefas T1-T7 em
  `docs/superpowers/plans/2026-08-13-handoff-tiago-correcao-curadoria.md`.
  **Decidido com o Tiago (2026-08-13):**
  - **Instrumento: Portaria do Comandante-Geral** (não Decreto). Consequência: os capítulos que
    criam/renomeiam órgão (`atribuicoes-funcoes`, `seguranca-contra-incendio`,
    `central-operacoes-193`) são inválidos como texto próprio na forma atual — precisam virar
    remissão a Decreto do Governador (LOB Art. 59), não descrição direta de estrutura. Ainda não
    reescritos nessa forma.
  - **Central 193**: o CBMRO opera **2 CIOP** (Centro Integrado de Operações) — Porto Velho
    (ocorrências do COB I) e Ji-Paraná (COB II). Aplicado só o NOME (`CICOM`→`CIOP`); a divisão
    operacional por COB **não** foi codificada nos 3 artigos/65 incisos do capítulo — pendência
    de redação.
  - **ADEMA→SEDAM, e-doc→SEI**: aplicados (resíduos de 1 ocorrência cada, fonte Sergipe).
  **Feito nesta branch (9 commits)**: 4 do Wândrio (resíduos mecânicos — Bahia sem adaptação,
  variantes "CBM-MT", rodapé do RISD/CBMSE fabricando um "Boletim Geral" do CBMRO, "PMSE") + 5
  meus (SESDEC; ADEMA/e-doc/CIOP; **correção da ESTRUTURA organizacional**; nome baiano do
  comando operacional). `verificar_verbatim.py` OK (1166 excerpts) +
  `test_regulamento_structure.py` OK (16 capítulos, 413 artigos) + `npm test` 154/154 em cada
  commit.

  **⚠️ Correção de ESTRUTURA aplicada em 2026-08-13** (o Tiago forneceu 3 documentos —
  organograma oficial do CBMRO, Decreto 21.425/2016 de SCI e a LOB consolidada — e a estrutura
  real da corporação). Até então a `ADAPTATIONS` só trocava NOME DE ESTADO; a curadoria havia
  importado junto o ORGANOGRAMA de MT/SE/BA. Corrigido, com correspondência inequívoca na lei:
  - `Comando/Comandante Regional`, `CRBM` (25x) → **Comando/Comandante Operacional de
    Bombeiros**. RO **não tem Comando Regional**: tem **COB I** (Porto Velho) e **COB II**
    (Ji-Paraná), subordinados operacionalmente ao Subcomandante-Geral (LOB Art. 35 + organograma).
  - `Diretoria/Diretor Operacional` e `de Operações` (44x) e a forma baiana `Comando de Operações
    de Bombeiros Militares` (4x) → **Comando/Comandante Operacional de Bombeiros**.
  - `Batalhão`→**Grupamento**; `CiaBM`/`CIBM` (33x)→**SGBM**. Cadeia do CBMRO: **COB → GBM →
    SGBM** (LOB Art. 47 e §1º; organograma).
  - `UBM` (18x) → **OBM** (termo da lei de RO). `Comandante-Geral Adjunto` (10x, 2 grafias) →
    **Subcomandante-Geral** (LOB Art. 12). `SSP/MT` → **SESDEC**.
  - **ANTI-AR-01 verificado ANTES de escrever a regra**: NÃO há regra para a palavra solta
    "Companhia" — em `servico-operacional` as 4 ocorrências são **concessionárias** (energia,
    água, elevador, seguradora) e **"Companhia de Comando e Serviços" EXISTE em RO** (LOB
    Art. 25). As 5 seguem intactas, conferidas no JSON pós-rebuild.

  **✅ REVERTE conclusão anterior — "multar" TEM base legal em RO.** O relatório de 13/08 dizia
  que a palavra "não existe na LOB" e que sanção pecuniária exigiria lei. Existe: a **Lei estadual
  nº 3.924/2016** e o **Decreto nº 21.425/2016** (regulamento de SCI, alterado pelo Decreto
  24.357/2019) preveem multa expressamente — Art. 34, II (rol de penalidades) e Art. 40 (gradação
  de 10 a 2.000 UPF, com destino ao FUNESBOM no §11). Os 4 dispositivos com "notificar, multar,
  interditar ou embargar" **podem ficar**; o que falta é **citar essa base** no texto, hoje ausente.

  **Ainda em aberto, todos exigindo decisão de mérito de quem conhece o CBMRO (não corrigir por
  semelhança/palpite — repetiria o erro que esta rodada está consertando):**
  - `seguranca-contra-incendio` (19 art/184 incisos) — **o capítulo inteiro é o regimento interno
    da DSCIP do Mato Grosso**: descreve CCIP 1 a CCIP 5, Tesouraria, Subseção de Protocolo,
    Subseção de Arrecadação e Estatística. **Nenhuma existe em RO.** A estrutura real é taxativa
    (LOB Art. 18, §1º + Decreto 21.425/2016, Arts. 2º e 5º): **CAT → DAT (uma por GBM) → SAT (uma
    por SGBM)**, com Seção de Estudos Técnicos, Seção de Planejamento/Fiscalização/Suporte Técnico
    e, nas DAT, Seções de Vistoria, Análise de Projetos, Investigação e Prevenção de Incêndio,
    Hidrantes e Atividades Técnicas. **Decisão consciente: NÃO renomear só a cabeça DSCIP→CAT** —
    isso daria falsa legitimidade (um "CAT" com sub-unidades do MT pareceria validado). O capítulo
    precisa ser **reescrito** sobre a estrutura legal; enquanto não for, permanecer visivelmente
    estrangeiro é mais honesto. Nomenclatura de RO já disponível no Decreto para a reescrita:
    SSCIP, PPCIP, AVCIP, ACPS, Instrução Técnica (IT), Comissão Técnica/CTE/CEA.
  - `seguranca-contra-incendio`, art. 182: afirma **vinculação automática** das Seções de
    Atividades Técnicas às unidades operacionais; a lei (Art. 18, §2º, red. Lei 4.488/2019) a
    trata como **facultativa, por ato do Comandante-Geral**. Contraria a lei.
  - `central-operacoes-193`: resíduos baianos que **não citam nome de estado** (por isso escapam
    da varredura automática) — Supervisor do Teledespacho "sediado na **Secretaria de Segurança
    Pública (SSP)**" (em RO os 2 CIOP ficam em Porto Velho e Ji-Paraná: **onde exatamente?**),
    `Superior de Dia` (3x), `Coordenadores de Área`, `Coordenadoria de Saúde` (RO não tem órgão de
    saúde — Art. 62 revogado pela Lei 2.244/2010), `GD (Grupo de Despacho)`, `SGTO`, `Supervisor
    de Operações`, `Adjunto ao Oficial de Dia`, remissão a "**ANEXO A desta Portaria**" (anexo
    baiano inexistente) e "código fonético previsto no âmbito do CBMRO" (o da Bahia). Falta ainda
    **codificar a divisão CIOP-Porto Velho/COB I × CIOP-Ji-Paraná/COB II** nos 3 artigos.
  - `atribuicoes-funcoes` (29 art/345 incisos): é o Título III do Regulamento do CBMMT. Os nomes
    de unidade já foram corrigidos acima, mas **restam os órgãos de direção**: DEIP, CEIB, Escola
    Dom Pedro II, Centro de Capacitação Física (19x no total) — sem equivalente direto. E o alerta
    permanece: **cargo de Coordenador é privativo de Oficial do último posto (LOB Art. 19)**, logo
    cada "Coordenadoria" que o texto criar implica um cargo de **Coronel** — correção de nome vira
    decisão de desenho de efetivo.
  - **`Pelotão` (5x) — 4º nível da cadeia não confirmado.** A cadeia validada pelo Tiago vai até o
    SGBM. A LOB (Art. 47, V e VI, e §1º) põe **Seção de Bombeiros** abaixo do Subgrupamento e
    **Grupo de Bombeiros** abaixo dela — nenhum dos dois aparece no texto (0x). Não convertido de
    propósito: inventar o nível repetiria o erro que esta rodada corrige.
  - `servico-operacional`+`servico-interno-dia` (128 art, fonte SE): nomes de órgão já corrigidos;
    **resta a matéria** — escalas desenhadas para estado compacto (Superior de Dia em sobreaviso
    preso à área da residência mas responsável pelo estado inteiro), a regionalizar por GBM;
    doutrina de comando contraditória (antiguidade × Sistema de Comando de Incidentes); 5 regras
    de "casos omissos" conflitantes.
  - Fundamento legal: **nenhum dos 185 artigos cita a Lei 2.204/2009** (sem cláusula de vigência/
    revogatória); o Art. 3º da minuta tem **11 competências**, a LOB (Art. 2º) tem **25** —
    suprime atendimento pré-hospitalar, guarda-vidas, socorro a embarcações, perícia técnica,
    vistorias, embargo/interdição, polícia judiciária militar, bombeiro civil e orçamento; e o
    inciso X condiciona **a convênio** uma fiscalização que a lei dá como poder próprio.
  - **"Art. 82 da Constituição Estadual"** (art. 1º da minuta) é o artigo da Constituição **do Mato
    Grosso**. Pista forte para o correspondente em RO: o Decreto 21.425/2016 fundamenta-se no
    **art. 148, § 3º, da Constituição Estadual** de Rondônia (e o poder de decreto do Governador
    no art. 65, V) — **confirmar antes de aplicar**, não foi alterado.
  - RI do cenário **futuro** (`minuta_structure.json`) tem 21 siglas de outros estados (CBMDF
    10x, CBMMT 7x, CBM-MT 2x, CBMPA 2x) — pendência separada, não afeta a reunião de 14/08; RI
    do cenário atual está limpo (0).
  Recomendação do relatório para a reunião de 14/08: apresentar como material-base a mapear
  (não como "a minuta do CBMRO"), com os comentários ancorados no `editId` — sobrevivem a
  qualquer reescrita/renumeração posterior dos capítulos.

## ✅ Concluído (mês atual)
- [x] **Registro de decisão em janela separada** (29/07/2026, pedido do Tiago): o
  formulário abria como overlay e cobria o card, escondendo a Questão e os excertos
  verbatim das candidatas — justamente o material de consulta para redigir a decisão.
  Agora abre em janela do navegador (`JanelaSeparada.jsx`, reutilizável), com a tela de
  Decisões livre, card em edição destacado, janela reaproveitada ao trocar de decisão e
  fallback para o overlay se o pop-up for bloqueado. node 141/141 + python OK + build limpo.
  **Prova manual em navegador (login real, gravação real no Firestore) ainda PENDENTE
  com o Tiago** — nenhum subagente deste projeto tem acesso a navegador gráfico neste
  ambiente; a verificação automatizada (testes + build) passou, mas o fluxo completo
  (abrir → trocar de decisão → gravar) só foi confirmado por leitura de código, não em
  uso real.
- [x] **Decisões passam a ser POR CENÁRIO** (29/07/2026, achado do Tiago): a aba Decisões
  mostrava as 9 decisões do RI da **LOB futura** também no cenário **atual** — `DecisoesCuradoria.jsx`
  buscava o JSON num caminho fixo, sem `scenarioDbUrl`, e o gerador declarava o arquivo
  "compartilhado entre cenários". Evidência: 4 das 9 citam órgãos que não existem na Lei
  2.204/2009 (bbs, crbm, depdec, doe) e outras 4 discutem COT/dpof/gab-cg no texto. Correção:
  campo `cenarios` por decisão (padrão por trilha — RI é específico da LOB, Regulamento é
  temático), filtro puro testado (`cenariosDaDecisao`/`filtrarPorCenario`), estado vazio
  explicativo no atual (nada de de-para por nome — seria AR-01) e isolamento do registro no
  Firestore por `decisionDocId` (antes, decidir num cenário marcava o outro como decidido sem
  ter aplicado texto final — falso verde AR-04). node 141/141 + python OK + build limpo.
- [x] **Lote de pendências técnicas da auditoria** (24/07/2026, aprovado pelo Wândrio):
  - **BA, NOp 01/2021, Art. 35**: novo truncador por-artigo no extrator (`art_stop` no
    `CONFIG['ba']` de `extrair_regulamentos.py`) corta o ANEXO A (mapa de força) que o
    último artigo engolia; excerto agora é só o caput. Exceção saiu da whitelist da
    `auditoria_citacoes.py`; 0 falhas.
  - **`chapter.id` do Regulamento atual re-carimbado** (`reg:atual:`): além de fechar a
    fragilidade de colisão, CONSERTOU um bug latente — o `Revisao.jsx` casa
    `c.id === chapterId` sem `semCenario`, então no cenário atual o painel "Ver
    referências" do Regulamento vinha VAZIO. Agora casa nos 2 cenários; futura intacta
    (0 vazamento de `reg:atual:`).
  - **`cot` (camada automática)**: include trocado de "operacoes/operacional" (casava
    Comandos de SOCORRO de ~20 estados — armadilha AR-01) pela MATÉRIA técnica (segurança
    contra incêndio/prevenção/atividades técnicas). Diff provado: 8 estados tiveram o
    `lobOrgans` do cot corrigido de socorro→técnico; matcher unificado reusado (lib).
  - **`documents_index.json`** removido (órfão; backup no scratchpad da sessão).
- [x] **Firestore rules endurecidas — PUBLICADAS e TESTADAS** (25-26/07/2026): `curtidoPor`
  só permite toggle do próprio uid (antes qualquer membro reescrevia o array e apagava
  curtidas alheias); `conferencia` validada por shape (status ∈ {ok,div}, sem campos-lixo),
  mantida COLABORATIVA de propósito. Publicadas pelo Wândrio no console (conta institucional
  `institucional_bsb_cbmro@cloud.sesdec.ro.gov.br`, projeto `revisao-minuta-cbmro-6f248`; o
  CLI da máquina está na conta pessoal, que não vê o projeto — publicação manual). Prova
  ponta a ponta no app OK: marcar conferência persiste após F5; curtir/descurtir funciona,
  sem travar nada legítimo nem erro. Encerra também o item antigo "teste REAL de escrita/
  leitura no Firestore".
  - Firestore rules endurecidas (ver 🔴 — falta só PUBLICAR). node 133/133 + python OK.
- [x] **"Ver referências" no popup de Revisão** (23/07/2026): botão retrátil "Ver
  referências (N)" no cabeçalho do popup (`RevisaoModal.jsx`) mostra o Bloco D (excertos de
  outros estados) do capítulo/órgão do dispositivo aberto — desabilitado quando N=0. UI
  extraída de `ConferenciaLinear.jsx` pro componente compartilhado
  `AlternativesPanel.jsx` (sem mudar aquela tela). Prova visual real: DPO Art. 57 → 2
  referências (DF/PA, já com o texto correto pós-fix da manhã); tema `uniformes-apresentacao`
  → 0 referências, botão cinza. 3 tasks via subagent-driven-development, todas Approved.
  Spec/plano em `docs/superpowers/*/2026-07-23-revisao-ver-referencias*`.
- [x] **Auditoria Rodada 3 — falsos verdes e falhas silenciosas** (23/07/2026): (a) classe
  do MyFOP encontrada de verdade — incisos de seção EDITADA são re-indexados 0..n e o
  texto final `editId#N` era aplicado no inciso ERRADO em silêncio; corrigido
  (`reindexed: true` + skip no overlay, teste de regressão novo); (b) 14 erros engolidos
  mapeados (4 altas) e corrigidos: banner `AvisoSincronizacao` nos feeds Firestore
  (Wizards/Revisão/Conferência/Decisões), falha de rede no login distinta de "não
  autorizado", telas que confundiam erro de carga com dado inexistente; (c) fronteira
  `encodeFirestoreId` conferida (simétrica nas 3 coleções por dispositivoId);
  (d) `npm run build` exit 0 com dist/ conferida; (e) rules locais auditadas coleção a
  coleção; (f) API gerar-proposta com auth+rate-limit reais nos 2 caminhos. AR-03 e
  AR-04 registradas no catálogo de armadilhas. node 133/133.
- [x] **Auditoria Rodada 2 — cenários atual×futura / geradores paralelos** (23/07/2026):
  3 comparações lado a lado (minuta, regulamento, comparativo) + teste mecânico nos JSONs.
  Vazamento futura→atual: **0** (competências do RO limpas; editIds todos com marcador;
  DEPARA_BLOCO_D 19/19 validado por conteúdo). Corrigidos 3 casamentos AR-01 reais na
  camada automática dos 2 cenários (cg×Gabinete em 10 estados; cob1×Comandos de Defesa
  Civil/Inteligência de GO; cot×Suprimento/Estado-Maior/Especializado) + condeg×Conselho
  de Ensino e assessorias×Telecom/Informática — **39 casamentos errados removidos, 0
  legítimos perdidos** (diff antes/depois). Matcher unificado na lib (era função duplicada
  — correções não propagavam). Avisos de frescor nos 2 geradores do atual (herança de JSON
  velho da futura era silenciosa) e órfão do commandChart do atual não some mais em
  silêncio. Comparativos regenerados; suítes verdes.
- [x] **Auditoria Rodada 1 — integridade das citações verbatim** (23/07/2026): verificador
  novo `scripts/auditoria_citacoes.py` confere os 1.605 excertos dos 4 JSONs de estrutura
  contra o DOCUMENTO reivindicado (LOB × RI × Regulamento do mesmo estado). Resultado:
  1.569 verbatim estritos, 24 com ruído de página embutido (minor), 12 exceções
  documentadas em whitelist, 0 falhas. Causa raiz do bug dpo/PA achada e corrigida no
  CÓDIGO: `md_for()` ignorava o `doc` e caía no RI em silêncio (**AR-02** em
  `docs/superpowers/auditoria-armadilhas.md`); correção da manhã (cabf7fb) refeita no
  GERADOR (extrator recaptura verbatim com as minúsculas do OCR do PA preservadas; GO
  idem). Teste inverso (citação→excerto) achou e fechou 2 lacunas com fonte disponível:
  `cot`→CE (Lei 13.438/2004, Art. 17) e `dpof`→GO (Lei 18.305/2013, Art. 26) capturados
  no Bloco D. Drift MT/SE (enrichments desatualizados após renomeação dos markdowns)
  regenerado. Suítes: node 132/132 + python OK + verificar_verbatim 1.166 OK.
- [x] **DOB-01 de Alagoas (glossário de terminologia) — investigada e descartada** (23/07/2026):
  1.686 verbetes extraídos e revisados (pelo Claude e pelo Wândrio); é glossário técnico de
  combate a incêndio, sem termos de uniforme/apresentação pessoal e só 2 termos fracos
  ligados a `central-operacoes-193`. Fechado sem incorporação nem extrator novo — nota do
  tema `uniformes-apresentacao` atualizada no vault.
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
