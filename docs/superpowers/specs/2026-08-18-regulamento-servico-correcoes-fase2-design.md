# Regulamento de Serviço — 2ª rodada de curadoria (correções de conteúdo)

**Data:** 2026-08-18
**Origem:** o Ten. Tiago analisou o recorte "Regulamento de Serviço" (`/regulamento/servico`,
spec `2026-08-13-regulamento-servico-escopo-participante-design.md`) já em produção — com
os dois perfis (admin e participante) — e apontou 6 problemas de conteúdo, herdados do
transplante bruto de MT que ainda não passou pela camada de reescrita autoral
(`scripts/regulamento_reescrita.py`).

**Contexto que já existe e este spec reaproveita:**
- O recorte filtra por **capítulo inteiro** via `TEMAS_SERVICO`
  (`src/lib/escopoServico.js`) — 7 dos 16 capítulos do `regulamento_structure.json`.
- A camada de reescrita autoral (`scripts/regulamento_reescrita.py`) já corrigiu 2 dos 16
  temas (`organizacao-geral`, `seguranca-contra-incendio`) e um 3º parcialmente
  (`central-operacoes-193`, com a NGA-CIOP-001/2026) em 13-14/08/2026. Este spec estende
  o mesmo mecanismo — não cria um novo.
- As mudanças valem para os **dois perfis** (admin e participante): ambos leem o mesmo
  `regulamento_structure.json`; o recorte só filtra o que é exibido.

---

## Escopo desta rodada

### Frente A — correções mecânicas (sem documento novo)

1. **Terminologia "Supervisor de Dia" → "Oficial de Dia" / "Superior de Dia".**
   12 artigos em `servico-operacional` citam "Supervisor de Dia" (herança do
   RISG/Exército via MT); a minuta já usa "Oficial de Dia" (8x) e "Superior de Dia" (11x)
   em outros pontos. Reler os 12 e decidir, artigo a artigo, qual figura real se aplica:
   - **Oficial de Dia** — oficial subalterno/intermediário, concorre à escala de serviço
     operacional no 1º GBM (Porto Velho), só oficiais lotados na capital.
   - **Superior de Dia** — oficial superior lotado na capital, escala de sobreaviso,
     ocorrências de grande vulto em todo o Estado; acionamento pela cadeia
     Comandante de SGBM → Comandante de GBM → Comandante de COB → Superior de Dia.
   Reconciliar com os 19 usos já corretos (não duplicar/contradizer). Resultado
   (de-para artigo a artigo) apresentado ao Ten. Tiago antes de aplicar — é conteúdo
   substantivo, não find-replace.

2. **Reordenar capítulos**: mover `atribuicoes-funcoes` para logo após
   `disposicoes-preliminares` — no recorte (`TEMAS_SERVICO`) **e** no Regulamento Geral
   completo (os 16 capítulos), já que não há razão para a ordem divergir entre as duas
   apresentações do mesmo documento.

### Frente B — depende de documentos que o Ten. Tiago vai fornecer (caminho de pasta)

3. **CIOP** — a NGA-CIOP-001/2026 já usada em 14/08 é a mesma; não é reescrita nova.
   Trabalho: **purgar** os resíduos de CIOP fora do capítulo `central-operacoes-193`
   (que já reflete a NGA): 4 artigos em `servico-operacional`, 2 em
   `servico-interno-dia`, 1 em `atribuicoes-funcoes` (dentro do recorte); 1 em
   `organizacao-geral`, 3 em `competencias-apoio-assessoramento`, 1 em
   `competencias-execucao` (fora do recorte, mas no Regulamento Geral completo — corrigir
   também, já que são resíduos do mesmo problema).

4. **Imprensa/mídia** — os 12 artigos que tratam do tema passam a remeter ao Manual de
   Relacionamento com a Mídia (DCS) e à Diretriz Geral de Comunicação Social, em vez do
   texto genérico importado de MT. Ler os 2 documentos para decidir entre remissão simples
   (padrão do artigo de fechamento da NGA-CIOP) ou transcrição de competências específicas.

5. **Protocolo de tentativa de suicídio (ATTS)** — conteúdo novo (hoje 0 artigos).
   Um dispositivo de remissão ao protocolo de Abordagem Técnica nas Tentativas de
   Suicídio, provavelmente em `servico-operacional`. Precisa do manual para o nome
   oficial/norma a citar como `fundamento`.

### Frente C — Capítulo V (`atribuicoes-funcoes`), a mais delicada

6. **Reescrever, escopado a COB (I e II) + CAT** e seus desdobramentos até a menor
   função, usando como base factual o que já foi validado em `organizacao-geral`
   (estrutura do COB: Comandante → Adjunto → Seções → GBM → SGBM → Pelotão) e
   `seguranca-contra-incendio` (estrutura do CAT: Coordenador → DAT → SAT). Citar
   LOB/organograma como `fundamento`, mesmo padrão das reescritas anteriores.

   **Decisão de escopo (2026-08-18):** o Regulamento Geral completo mantém, por ora, as
   funções dos outros 19 órgãos (ainda transplante de MT — corrigidas pontualmente pelas
   Frentes A/B onde citarem CIOP/mídia, mas sem reescrita completa nesta rodada). Ou
   seja: o capítulo passa a ter conteúdo de **dois níveis de curadoria coexistindo** —
   COB/CAT reescritos, demais órgãos como estão.

   **Peça técnica nova:** cada artigo do capítulo precisa de uma tag de órgão
   (`orgao: 'cob' | 'cat' | outro`, ou equivalente) para que:
   - `filtrarEstruturaPorEscopo` (`escopoServico.js`) filtre **por artigo dentro do
     capítulo**, não só por capítulo inteiro (hoje só sabe cortar capítulos completos) —
     o recorte do participante deve mostrar só os artigos de COB/CAT dentro de
     `atribuicoes-funcoes`.
   - O Regulamento Geral completo (admin) continue mostrando todos os artigos do
     capítulo, sem filtro.

---

## Fora de escopo — registrado como pendência de 2ª etapa

**Achado nesta rodada, não tratado agora** (determinação do Ten. Tiago: "fica para um
segundo plano"): o Regulamento Geral completo (visão admin, 16 capítulos) tem sua
**Parte I inteira** (temas 1-12, artigos 1-257) ainda baseada no transplante bruto de MT
— alinhado à estrutura que o Regulamento de MT usa, não à LOB atual de Rondônia. Só 2 dos
12 temas de Parte I já passaram pela reescrita autoral (`organizacao-geral` e
`seguranca-contra-incendio`); os outros 10 (`competencias-direcao`,
`competencias-apoio-assessoramento`, `competencias-execucao`, `disciplina-correicao`,
`uniformes-apresentacao`, `cerimonial-honras`, `ensino-instrucao`, `pessoal-quadros`,
mais `disposicoes-preliminares`/`disposicoes-finais`, já ok) seguem pendentes. A "Parte
II" (artigos 258+) que aparece no documento completo é o mesmo recorte de serviço tratado
aqui.

Este spec **não ataca** essa correção de Parte I nem a reordenação de capítulos dentro
dela — registrar em `.claude/PENDENCIAS.md` como item novo de 🔴 Pendente ao final desta
rodada.

---

## Verificação

- `scripts/test_regulamento_structure.py` (contagem de capítulos/artigos, cobertura do
  `REMOVER_ARTIGOS`/`SUBSTITUI_INTEGRALMENTE`).
- `scripts/verificar_verbatim.py` — só cobre o que é transcrito de outro estado; o texto
  autoral (Frentes B/C) não entra, mesmo padrão das reescritas de 13-14/08.
- `node --test` (154 testes atuais + os que cobrirem o filtro por artigo em
  `escopoServico.test.js`).
- Rebuild dos dois JSONs (`regulamento_structure.json` e
  `database/atual/regulamento_structure.json`) e checagem manual do recorte.

## Sequenciamento das 71 sugestões do Firestore

Feito **por último**, depois de A/B/C: muitas das 71 sugestões apontam exatamente os
problemas corrigidos nesta rodada (Supervisor de Dia, CIOP fora de lugar, Capítulo V) —
corrigir a causa resolve a sugestão. Ao final, reclassificar o que sobrar em (i)
ortografia/formatação → aplicar direto no `regulamento_enrichment_*.py`/
`regulamento_reescrita.py` e rebuild; (ii) depende de decisão do CONDEG → deixar em
aberto no Firestore, sem tocar.
