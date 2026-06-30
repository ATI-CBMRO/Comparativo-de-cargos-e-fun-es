# Desdobramento dos órgãos administrativos do RO no organograma — Plano de Implementação

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Fazer todos os órgãos administrativos do RO (7 assessorias, Correição, Comissões, Conselhos, Gabinetes SCG/EMG) abrirem painel de detalhe no `/estados/ro`, com competências verbatim da Minuta da LOB do RO.

**Architecture:** Editar o `database/organs_detail/ro.json` (escrito à mão; nenhum script o regenera) adicionando os órgãos administrativos faltantes com texto verbatim da LOB; alinhar o id de um nó da árvore em `scripts/curated_organs.py`; reexecutar `build_states_data.py`, que re-carimba `detailId` em cada nó casando por id. O `OrgDetail.jsx` já renderiza qualquer órgão com `atribuicoes`/`cargos`/`desdobramentos` — nenhuma mudança de frontend.

**Tech Stack:** Python (pipeline de dados offline, sem libs externas), JSON, React/Vite (frontend de visualização).

**Spec:** `docs/superpowers/specs/2026-06-30-organograma-ro-orgaos-administrativos-design.md`

---

## File Structure

- **Modify:** `database/organs_detail/ro.json` — adicionar 7 órgãos de assessoria (`ai, ae, al, ap, apge, af, aci`) + 4 de apoio (`comissoes, conselhos, gab-scg, gab-emg`). **Manter** o órgão combinado `assessorias` (consumido por id exato pela coluna RO do `/comparar`).
- **Modify:** `scripts/curated_organs.py` — trocar o id do nó de Correição do RO de `correg` → `corregedoria`.
- **Regenerate (não editar):** `database/states_data.json` via `scripts/build_states_data.py`.
- **Verify only (não editar):** `database/comparativo_dpo_cot.json`, `database/comparativo_minuta.json` (guarda de regressão).

**baseLegal padrão** (string idêntica à já usada nos demais órgãos do RO, copiar exatamente):
`Minuta de Projeto de Lei n.º 0059262482 (abril de 2025) — Organização Básica do CBMRO (em tramitação)`

---

### Task 1: Guarda de verificação (asserção que falha hoje)

Confirma o estado atual (12 nós-alvo sem `detailId`) e servirá de critério de pronto. É um comando reexecutável — não cria arquivo no repo.

**Files:** nenhum (comando inline).

- [ ] **Step 1: Rodar a asserção e confirmar que FALHA agora**

Run:
```bash
cd "c:/Users/tiago/OneDrive/Documentos/Comparativo de legislações CBM" && python - <<'PY'
import json, sys
TARGETS = {"ai","ae","al","ap","apge","af","aci",
           "comissoes","conselhos","gab-scg","gab-emg","corregedoria"}
d = json.load(open("database/states_data.json", encoding="utf-8"))
ro = next(s for s in d["states"] if s["id"] == "ro")
found = {}
def walk(n):
    if isinstance(n, list):
        for x in n: walk(x)
        return
    if n.get("id") in TARGETS:
        found[n["id"]] = n.get("detailId")
    for c in (n.get("children") or []): walk(c)
walk(ro["organs"])
missing = sorted(t for t in TARGETS if not found.get(t))
print("encontrados c/ detailId:", {k:v for k,v in found.items() if v})
print("FALTANDO (sem nó ou sem detailId):", missing)
sys.exit(0 if not missing else 1)
PY
echo "exit=$?"
```
Expected: `exit=1` e `FALTANDO` listando os 12 ids (`corregedoria` aparece faltando porque o nó ainda se chama `correg`; os demais existem mas sem `detailId`).

---

### Task 2: Baseline do `/comparar` (guarda de regressão)

Snapshot dos dois JSON do comparador, para diff ao final.

**Files:** snapshots em pasta temporária (fora do repo).

- [ ] **Step 1: Copiar os JSON atuais para baseline**

Run:
```bash
cd "c:/Users/tiago/OneDrive/Documentos/Comparativo de legislações CBM" && mkdir -p /tmp/cbm_baseline && cp database/comparativo_dpo_cot.json database/comparativo_minuta.json /tmp/cbm_baseline/ && ls -la /tmp/cbm_baseline/
```
Expected: os dois arquivos copiados.

---

### Task 3: Adicionar as 7 assessorias individuais ao `ro.json`

Mantém o órgão combinado `assessorias` e adiciona 7 órgãos com ids casando os nós da árvore. Texto verbatim do Art. 30 §1º.

**Files:**
- Modify: `database/organs_detail/ro.json` (objeto `organs`)

- [ ] **Step 1: Inserir os 7 órgãos no objeto `organs`** (logo após a entrada `"assessorias"`, que NÃO deve ser removida)

```json
"ai": {
  "id": "ai",
  "name": "Assessoria Institucional",
  "category": "Assessoramento",
  "subordinadoA": "Comandante-Geral",
  "legalRef": "Art. 30, §1º, I",
  "baseLegal": "Minuta de Projeto de Lei n.º 0059262482 (abril de 2025) — Organização Básica do CBMRO (em tramitação)",
  "artigosDeOrigem": ["Art. 7º (Assessoramento)", "Art. 30 (Assessorias)"],
  "atribuicoes": [
    "Responsável pela ligação do Comandante-Geral junto aos Poderes, Entes e Instituições Permanentes, prestando assessoramento nas questões voltadas à Corporação. (Art. 30, §1º, I)"
  ],
  "cargos": [
    {"cargo": "Assessor Institucional", "subordinadoA": "Comandante-Geral"}
  ]
},
"ae": {
  "id": "ae",
  "name": "Assessoria Especial",
  "category": "Assessoramento",
  "subordinadoA": "Comandante-Geral",
  "legalRef": "Art. 30, §1º, II",
  "baseLegal": "Minuta de Projeto de Lei n.º 0059262482 (abril de 2025) — Organização Básica do CBMRO (em tramitação)",
  "artigosDeOrigem": ["Art. 7º (Assessoramento)", "Art. 30 (Assessorias)"],
  "atribuicoes": [
    "Responsável por prestar assessoramento técnico, elaborar estudos e pareceres de questões de direito, de questões relacionadas à política de administração geral da Corporação, de exames de aspectos de legalidade dos atos que lhe forem submetidos, além de auxiliar a tomada de decisão de outros órgãos da Corporação, quando previamente autorizado pelo Comandante-Geral. (Art. 30, §1º, II)"
  ],
  "cargos": [
    {"cargo": "Assessor Especial", "subordinadoA": "Comandante-Geral"}
  ]
},
"al": {
  "id": "al",
  "name": "Assessoria Legislativa",
  "category": "Assessoramento",
  "subordinadoA": "Comandante-Geral",
  "legalRef": "Art. 30, §1º, III",
  "baseLegal": "Minuta de Projeto de Lei n.º 0059262482 (abril de 2025) — Organização Básica do CBMRO (em tramitação)",
  "artigosDeOrigem": ["Art. 7º (Assessoramento)", "Art. 30 (Assessorias)"],
  "atribuicoes": [
    "Responsável por assessorar o Comandante-Geral quanto à análise de normas, diretrizes, portarias, determinações e demais documentos emanados pelo Comando-Geral, além de realizar os estudos e elaborar projetos de leis de interesse da Corporação e orientar ao Comandante-Geral quanto ao exato cumprimento de decisões judiciais, bem como preparar as informações que devem ser prestadas à Procuradoria-Geral do Estado, para a defesa dos interesses do Estado em ações judiciais demandadas ao CBMRO. (Art. 30, §1º, III)"
  ],
  "cargos": [
    {"cargo": "Assessor Legislativo", "subordinadoA": "Comandante-Geral"}
  ]
},
"ap": {
  "id": "ap",
  "name": "Assessoria Parlamentar",
  "category": "Assessoramento",
  "subordinadoA": "Comandante-Geral",
  "legalRef": "Art. 30, §1º, IV",
  "baseLegal": "Minuta de Projeto de Lei n.º 0059262482 (abril de 2025) — Organização Básica do CBMRO (em tramitação)",
  "artigosDeOrigem": ["Art. 7º (Assessoramento)", "Art. 30 (Assessorias)"],
  "atribuicoes": [
    "Responsável por assessorar o Comandante-Geral na Assembleia Legislativa, Congresso Nacional e demais órgãos e autoridades, no acompanhamento de matérias legislativas de interesse da Corporação. (Art. 30, §1º, IV)"
  ],
  "cargos": [
    {"cargo": "Assessor Parlamentar", "subordinadoA": "Comandante-Geral"}
  ]
},
"apge": {
  "id": "apge",
  "name": "Assessoria de Projetos e Gestão Estratégica",
  "category": "Assessoramento",
  "subordinadoA": "Comandante-Geral",
  "legalRef": "Art. 30, §1º, V",
  "baseLegal": "Minuta de Projeto de Lei n.º 0059262482 (abril de 2025) — Organização Básica do CBMRO (em tramitação)",
  "artigosDeOrigem": ["Art. 7º (Assessoramento)", "Art. 30 (Assessorias)"],
  "atribuicoes": [
    "Responsável por prestar assessoramento técnico nos assuntos relacionados à Gestão Estratégica da Corporação, bem como elaborar, gerir, acompanhar e fiscalizar a execução do Plano Estratégico, dos Projetos e Convênios firmados entre o CBMRO e outros órgãos e Poderes. (Art. 30, §1º, V)"
  ],
  "cargos": [
    {"cargo": "Assessor de Projetos e Gestão Estratégica", "subordinadoA": "Comandante-Geral"}
  ]
},
"af": {
  "id": "af",
  "name": "Assessoria Fundacional",
  "category": "Assessoramento",
  "subordinadoA": "Comandante-Geral",
  "legalRef": "Art. 30, §1º, VI",
  "baseLegal": "Minuta de Projeto de Lei n.º 0059262482 (abril de 2025) — Organização Básica do CBMRO (em tramitação)",
  "artigosDeOrigem": ["Art. 7º (Assessoramento)", "Art. 30 (Assessorias)"],
  "atribuicoes": [
    "A LOB (Art. 30, §1º, VI) cita a Assessoria Fundacional sem enumerar competências específicas. Aplica-se o caput do Art. 30: órgão subordinado ao Comandante-Geral que presta assessoramento administrativo e técnico, responsável pela realização de estudos, pesquisas e elaboração e controle de pareceres, mantendo o relacionamento entre o CBMRO e outros Poderes e Órgãos."
  ],
  "cargos": [
    {"cargo": "Assessor Fundacional", "subordinadoA": "Comandante-Geral"}
  ]
},
"aci": {
  "id": "aci",
  "name": "Assessoria de Controle Interno",
  "category": "Assessoramento",
  "subordinadoA": "Comandante-Geral (sujeita-se tecnicamente à Controladoria Geral do Estado)",
  "legalRef": "Art. 30, §1º, VII",
  "baseLegal": "Minuta de Projeto de Lei n.º 0059262482 (abril de 2025) — Organização Básica do CBMRO (em tramitação)",
  "artigosDeOrigem": ["Art. 7º (Assessoramento)", "Art. 30 (Assessorias)"],
  "atribuicoes": [
    "Assegurar o alcance dos objetivos e metas estabelecidas pela instituição, otimizando os resultados de aplicação dos recursos públicos e dos serviços prestados à sociedade.",
    "Atenuar os índices de intervenção dos sistemas de controles externos existentes, buscando a adequação legislativa e a melhoria contínua dos processos administrativos.",
    "Assegurar a conformidade dos atos de gestão através do gerenciamento de riscos, promoção da integridade, da governança pública e da transparência ativa e passiva, com foco na eficiência, eficácia e efetividade da administração dos recursos públicos e na proteção do erário.",
    "Adotar as medidas necessárias para prevenir, corrigir e combater a corrupção e fomentar a transparência na gestão.",
    "Realizar atividades de ouvidoria do CBMRO. (Art. 30, §1º, VII)"
  ],
  "cargos": [
    {
      "cargo": "Assessor de Controle Interno",
      "subordinadoA": "Comandante-Geral",
      "requisito": "Oficial Superior da ativa do último posto da Corporação (QOEMBM). (Art. 30, §1º, VII)"
    }
  ]
},
```

- [ ] **Step 2: Validar JSON**

Run:
```bash
cd "c:/Users/tiago/OneDrive/Documentos/Comparativo de legislações CBM" && python -c "import json; d=json.load(open('database/organs_detail/ro.json',encoding='utf-8')); o=d['organs']; print('assessorias combinado presente:', 'assessorias' in o); print('novos:', [k for k in ['ai','ae','al','ap','apge','af','aci'] if k in o])"
```
Expected: `assessorias combinado presente: True` e `novos: ['ai', 'ae', 'al', 'ap', 'apge', 'af', 'aci']`.

---

### Task 4: Adicionar os 4 órgãos de apoio ao `ro.json`

Ids casam os nós `comissoes, conselhos, gab-scg, gab-emg` da árvore. Verbatim Arts. 32, 33-35, 36, 38.

**Files:**
- Modify: `database/organs_detail/ro.json` (objeto `organs`)

- [ ] **Step 1: Inserir os 4 órgãos no objeto `organs`**

```json
"comissoes": {
  "id": "comissoes",
  "name": "Comissões",
  "category": "Apoio ao Comando-Geral",
  "subordinadoA": "Comandante-Geral",
  "legalRef": "Art. 32",
  "baseLegal": "Minuta de Projeto de Lei n.º 0059262482 (abril de 2025) — Organização Básica do CBMRO (em tramitação)",
  "artigosDeOrigem": ["Art. 8º, §1º, II (Apoio ao Comando-Geral)", "Art. 32 (Comissões)"],
  "atribuicoes": [
    "Órgãos constituídos para a realização de atividades periódicas e temporárias previstas em regulamento da Corporação ou determinadas pelo Comandante-Geral, subordinadas a ele, para deliberarem sobre os assuntos de interesse institucional.",
    "São comissões permanentes a Comissão de Promoção de Oficiais e a Comissão de Promoção de Praças, cuja composição e atribuições serão fixadas em regulamento próprio.",
    "Poderão ser constituídas outras comissões, de caráter temporário e destinadas a estudos específicos, a critério do Comandante-Geral."
  ],
  "desdobramentos": ["Presidente", "Secretário", "Membros"],
  "cargos": []
},
"conselhos": {
  "id": "conselhos",
  "name": "Conselhos",
  "category": "Apoio ao Comando-Geral",
  "subordinadoA": "Comandante-Geral",
  "legalRef": "Arts. 33 a 35",
  "baseLegal": "Minuta de Projeto de Lei n.º 0059262482 (abril de 2025) — Organização Básica do CBMRO (em tramitação)",
  "artigosDeOrigem": ["Art. 8º, §1º, III (Apoio ao Comando-Geral)", "Arts. 33 a 35 (Conselhos)"],
  "atribuicoes": [
    "Conselhos de Justificação e Disciplina — órgãos constituídos para processar e julgar, no âmbito administrativo, os assuntos de interesse institucional, com composição e atribuições fixadas em legislação específica, subordinados ao Comandante-Geral. (Art. 33)",
    "Conselhos de Ética e Disciplina Militares — composição, atribuições e funcionamento fixados em legislação específica, subordinados ao Comandante-Geral. (Art. 34)",
    "Conselhos de Condecorações — órgãos constituídos com a competência de analisar e processar as propostas de concessão e cassação das condecorações submetidas à sua apreciação, realizando a propositura da concessão ou cassação ao Comandante-Geral, de acordo com a legislação específica. (Art. 35)"
  ],
  "desdobramentos": [
    "Conselhos de Justificação e Disciplina",
    "Conselhos de Ética e Disciplina Militares",
    "Conselhos de Condecorações"
  ],
  "cargos": []
},
"gab-scg": {
  "id": "gab-scg",
  "name": "Gabinete do Subcomando-Geral",
  "abbreviation": "GAB/SCG",
  "category": "Apoio ao Subcomando-Geral",
  "subordinadoA": "Subcomandante-Geral",
  "legalRef": "Art. 36",
  "baseLegal": "Minuta de Projeto de Lei n.º 0059262482 (abril de 2025) — Organização Básica do CBMRO (em tramitação)",
  "artigosDeOrigem": ["Art. 8º, §2º, I (Apoio ao Subcomando-Geral)", "Art. 36 (Gabinete do Subcomando-Geral)"],
  "atribuicoes": [
    "Supervisão e execução das atividades administrativas de apoio e assessoramento direto, imediato e pessoal do Subcomandante-Geral."
  ],
  "desdobramentos": ["Chefia de Gabinete", "Secretaria", "Ajudância de Ordens"],
  "cargos": [
    {
      "cargo": "Chefe de Gabinete do Subcomando-Geral",
      "subordinadoA": "Subcomandante-Geral",
      "atribuicoes": [
        "Supervisionar e executar as atividades administrativas de apoio e assessoramento direto, imediato e pessoal do Subcomandante-Geral."
      ]
    }
  ]
},
"gab-emg": {
  "id": "gab-emg",
  "name": "Gabinete do Estado-Maior Geral",
  "abbreviation": "GAB/EMG",
  "category": "Apoio ao Estado-Maior Geral",
  "subordinadoA": "Chefe do Estado-Maior Geral",
  "legalRef": "Art. 38",
  "baseLegal": "Minuta de Projeto de Lei n.º 0059262482 (abril de 2025) — Organização Básica do CBMRO (em tramitação)",
  "artigosDeOrigem": ["Art. 8º, §3º, I (Apoio ao Estado-Maior Geral)", "Art. 38 (Gabinete do Estado-Maior Geral)"],
  "atribuicoes": [
    "Supervisão e execução das atividades administrativas de apoio e assessoramento direto, imediato e pessoal do Chefe do Estado-Maior Geral."
  ],
  "desdobramentos": ["Chefia de Gabinete", "Secretaria", "Ajudante de Ordens"],
  "cargos": [
    {
      "cargo": "Chefe de Gabinete do Estado-Maior Geral",
      "subordinadoA": "Chefe do Estado-Maior Geral",
      "atribuicoes": [
        "Supervisionar e executar as atividades administrativas de apoio e assessoramento direto, imediato e pessoal do Chefe do Estado-Maior Geral."
      ]
    }
  ]
},
```

- [ ] **Step 2: Validar JSON e contagem de órgãos**

Run:
```bash
cd "c:/Users/tiago/OneDrive/Documentos/Comparativo de legislações CBM" && python -c "import json; o=json.load(open('database/organs_detail/ro.json',encoding='utf-8'))['organs']; print('total organs:', len(o)); print('apoio novos:', [k for k in ['comissoes','conselhos','gab-scg','gab-emg'] if k in o])"
```
Expected: `total organs: 37` (26 originais + 7 assessorias + 4 apoio) e `apoio novos: ['comissoes', 'conselhos', 'gab-scg', 'gab-emg']`.

---

### Task 5: Alinhar o id do nó de Correição na árvore curada

**Files:**
- Modify: `scripts/curated_organs.py` (bloco `"ro"`, ~linha 89)

- [ ] **Step 1: Trocar o id `correg` → `corregedoria`**

De:
```python
    _n("correg","Órgãos de Correição", cat="Correição",
       desc="Exercem as funções de Corregedoria-Geral.",
       ref="Art. 10 — Minuta LOB 2025"),
```
Para:
```python
    _n("corregedoria","Órgãos de Correição", cat="Correição",
       desc="Exercem as funções de Corregedoria-Geral.",
       ref="Art. 10 — Minuta LOB 2025"),
```

> Apenas o 1º argumento (id) muda. O nome exibido continua "Órgãos de Correição". Atenção: alterar **somente** a ocorrência dentro do bloco `"ro"` (não as de outros estados).

- [ ] **Step 2: Confirmar a alteração no bloco do RO**

Run:
```bash
cd "c:/Users/tiago/OneDrive/Documentos/Comparativo de legislações CBM" && python -c "from scripts import curated_organs as c" 2>/dev/null; grep -n 'corregedoria\",\"Órgãos de Correição' scripts/curated_organs.py
```
Expected: uma linha encontrada (o nó do RO agora com id `corregedoria`).

---

### Task 6: Regenerar `states_data.json` e passar a guarda da Task 1

**Files:**
- Regenerate: `database/states_data.json`

- [ ] **Step 1: Reexecutar o build (NÃO rodar `build_organs_detail.py`)**

Run:
```bash
cd "c:/Users/tiago/OneDrive/Documentos/Comparativo de legislações CBM" && python scripts/build_states_data.py
```
Expected: build conclui sem erro; menciona o RO entre os estados processados.

- [ ] **Step 2: Rodar a guarda da Task 1 — agora deve PASSAR**

Run: (mesmo comando da Task 1, Step 1)
```bash
cd "c:/Users/tiago/OneDrive/Documentos/Comparativo de legislações CBM" && python - <<'PY'
import json, sys
TARGETS = {"ai","ae","al","ap","apge","af","aci",
           "comissoes","conselhos","gab-scg","gab-emg","corregedoria"}
d = json.load(open("database/states_data.json", encoding="utf-8"))
ro = next(s for s in d["states"] if s["id"] == "ro")
found = {}
def walk(n):
    if isinstance(n, list):
        for x in n: walk(x)
        return
    if n.get("id") in TARGETS:
        found[n["id"]] = n.get("detailId")
    for c in (n.get("children") or []): walk(c)
walk(ro["organs"])
missing = sorted(t for t in TARGETS if not found.get(t))
print("com detailId:", {k:v for k,v in found.items() if v})
print("FALTANDO:", missing)
sys.exit(0 if not missing else 1)
PY
echo "exit=$?"
```
Expected: `exit=0`; `FALTANDO: []`; cada id-alvo com seu `detailId` (ex.: `ai -> ai`, `corregedoria -> corregedoria`, `comissoes -> comissoes`).

---

### Task 7: Guarda de regressão do `/comparar`

**Files:**
- Regenerate: `database/comparativo_dpo_cot.json`, `database/comparativo_minuta.json`

- [ ] **Step 1: Regenerar os comparativos (ordem importa: dpo_cot antes de minuta)**

Run:
```bash
cd "c:/Users/tiago/OneDrive/Documentos/Comparativo de legislações CBM" && python scripts/build_dpo_cot_comparison.py && python scripts/build_minuta_comparison.py
```
Expected: ambos concluem sem erro.

- [ ] **Step 2: Diff contra o baseline — deve ser VAZIO**

Run:
```bash
cd "c:/Users/tiago/OneDrive/Documentos/Comparativo de legislações CBM" && diff /tmp/cbm_baseline/comparativo_dpo_cot.json database/comparativo_dpo_cot.json && diff /tmp/cbm_baseline/comparativo_minuta.json database/comparativo_minuta.json && echo "SEM REGRESSAO"
```
Expected: `SEM REGRESSAO` (nenhuma diferença). Se houver diff, PARAR: investigar antes de prosseguir (o esperado é zero — a coluna RO usa id exato `assessorias`, que foi mantido).

---

### Task 8: Verificação visual e commit

**Files:**
- Commit: `database/organs_detail/ro.json`, `scripts/curated_organs.py`, `database/states_data.json`

- [ ] **Step 1: Subir o dev server**

Run:
```bash
cd "c:/Users/tiago/OneDrive/Documentos/Comparativo de legislações CBM" && npm run dev -- --port 5173 --strictPort
```
Expected: Vite sobe em http://localhost:5173

- [ ] **Step 2: Conferir no navegador**

Abrir http://localhost:5173/estados/ro e clicar no ícone ⓘ de cada órgão antes mudo: as **7 Assessorias**, **Órgãos de Correição**, **Comissões**, **Conselhos**, **Gabinete do Subcomando-Geral** e **Gabinete do Estado-Maior Geral**. Cada um deve abrir o painel lateral com o texto da LOB (atribuições/competências). Conferir também que DPO/COT e as diretorias seguem abrindo normalmente.

- [ ] **Step 3: Commit**

```bash
cd "c:/Users/tiago/OneDrive/Documentos/Comparativo de legislações CBM" && git add database/organs_detail/ro.json scripts/curated_organs.py database/states_data.json && git commit -m "$(cat <<'EOF'
feat(organograma-ro): desdobra órgãos administrativos pela LOB

Adiciona ao ro.json os 7 órgãos de assessoria (Art. 30) e 4 de apoio
(Comissões/Conselhos/Gabinetes SCG e EMG — Arts. 32-38) e religa a
Correição à Corregedoria-Geral (id correg->corregedoria em curated_organs).
Agora todos os órgãos administrativos do RO abrem painel de detalhe no
/estados/ro, com texto verbatim da Minuta da LOB. O órgão combinado
'assessorias' é mantido (coluna RO do /comparar); comparativos inalterados.

Co-Authored-By: Claude Opus 4.8 <noreply@anthropic.com>
EOF
)"
```
Expected: commit criado com os 3 arquivos.

---

## Self-Review (preenchido pelo autor do plano)

- **Cobertura da spec:** 7 assessorias (Task 3) ✓ · 4 apoio (Task 4) ✓ · Correição religada (Task 5) ✓ · manter `assessorias` combinado (Task 3) ✓ · regenerar só `build_states_data` (Task 6) ✓ · Assessoria Fundacional sem invenção (Task 3, `af`) ✓ · guarda de regressão `/comparar` (Tasks 2, 7) ✓ · asserção de `detailId` dos 12 nós (Tasks 1, 6) ✓ · verificação visual (Task 8) ✓.
- **Categorias permanecem sem `detailId`** (`assess`, `apoio`, `exec`, `ap-cg`, `ap-scg`, `ap-emg`, `ap-set`): esperado, não são alvo.
- **Placeholders:** nenhum — todo texto verbatim incluído.
- **Consistência de ids:** ids do `ro.json` (Tasks 3-4) = ids dos nós da árvore em `curated_organs.py` (`ai,ae,al,ap,apge,af,aci,comissoes,conselhos,gab-scg,gab-emg`) e `corregedoria` após a Task 5 — casam por id em `enrich_tree_from_detail`.
