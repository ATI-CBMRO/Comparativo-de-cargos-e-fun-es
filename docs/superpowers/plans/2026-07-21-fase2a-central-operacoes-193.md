# Fase 2A — Preencher o 16º tema (Central de Operações 193) — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** O tema `central-operacoes-193` deixa de estar vazio/pendente e passa a exibir texto verbatim de teledespacho, com a Bahia como fonte primária e Tocantins como alternativa.

**Architecture:** Reusa o pipeline de curadoria existente. Adiciona duas entradas ao `CONFIG` do `extrair_regulamentos.py` (Bahia e Tocantins), mapeando SÓ os artigos de teledespacho ao tema; roda o extrator (verbatim por construção) e o verificador; muda a fonte primária do tema para `ba`; regenera os JSONs. Roraima fica de fora (o 193 não é isolável num artigo próprio — está difuso dentro do Art. 54).

**Tech Stack:** Python 3.12 (venv `.venv-pipeline/`), `node --test`.

**Spec:** `docs/superpowers/specs/2026-07-21-fase2a-central-operacoes-193-design.md`.

## Contexto factual (leitura de fonte já feita — 2026-07-21)
- **Bahia** (`Bahia - Regulamento de Serviço.md`, Norma Operacional nº 01/2021): teledespacho em
  **Art. 8º–9º** (Seção II — Supervisor do Teledespacho/CICOM) e **Art. 18** (Seção X — Operador
  do Teledespacho/CICOM). Corpo articulado começa após a linha "R E S O L V E". Ruído de layout
  repetido NO MEIO dos artigos: linhas "NORMA OPERACIONAL ... nº 02" e "Pág. N".
- **Tocantins** (`Tocantins - Regulamento de Serviço.md`): teledespacho em **Art. 12–14 do
  ANEXO 2** (Coordenador de Operações, Despachante, Atendente). ⚠️ O Anexo 2 REINICIA a numeração
  em "Art. 1º", então "Art. 12" existe DUAS vezes no arquivo — é obrigatório fatiar a partir do
  cabeçalho do Anexo 2. Ruído de layout: linha "QUARTEL DO COMANDO GERAL ... SUPLEMENTO AO BG nº
  1128 ...", que aparece no meio do Art. 12.
- **Roraima**: NÃO entra — o teledespacho está difuso dentro do Art. 54 (Oficial de Comunicação,
  misturado com PPE, empenho de UR/SAMU etc.), sem artigo próprio. Risco #7 do spec, confirmado.

## Global Constraints

- Comunicação/UI em pt-BR.
- Python SEMPRE via `.venv-pipeline/bin/python` (PEP 668 bloqueia o pip do sistema).
- Os arquivos `scripts/regulamento_enrichment_<uf>.py` são GERADOS — NÃO editar à mão; sempre
  regenerar via `extrair_regulamentos.py`.
- Verbatim é lei: `verificar_verbatim.py` deve passar. Caput que não existe literal na fonte se
  reporta e corrige (faixa/`strip_lines`), nunca se ajusta à mão no arquivo gerado.
- NÃO tocar em nenhum tema já existente nem nos 410 artigos da Fase 1; não tocar na trilha do RI
  (`minuta_*`), nem em `database/atual/organs_detail/ro.json`.
- `node --test` deve terminar verde em todo commit.
- Caminhos absolutos no Bash, sem `cd ... &&`.

---

### Task 1: Preencher o tema com BA (primária) + TO (alternativa)

**Files:**
- Modify: `scripts/extrair_regulamentos.py` (dict `CONFIG`, após a entrada `'go'`/`'al'` — adicionar `'ba'` e `'to'`)
- Modify: `scripts/regulamento_enrichment.py` (`PRIMARY_SOURCE['central-operacoes-193']`, ~linha 70)
- Generate: `scripts/regulamento_enrichment_ba.py`, `scripts/regulamento_enrichment_to.py` (via extrator)
- Regenerate: `database/regulamento_structure.json`, `database/atual/regulamento_structure.json`
- Modify: `scripts/test_regulamento_structure.py`

**Interfaces:**
- Produces: capítulo `central-operacoes-193` com `articles` não-vazio (3 artigos da BA), `primary.uf == 'ba'`, `parte == 'servico'`, e `alternatives['to']` com 3 excerpts. Total de artigos do Regulamento: 410 → 413.

- [ ] **Step 1: Escrever as asserções que devem falhar** — em `scripts/test_regulamento_structure.py`:

Remover `central-operacoes-193` da allowlist de pendentes (localizar `PENDENTES_OK = {'central-operacoes-193'}` e trocar por conjunto vazio):

```python
PENDENTES_OK = set()  # Fase 2A preencheu central-operacoes-193; nenhum tema pode ficar vazio
```

E adicionar, logo após o loop que percorre `d['chapters']` (perto das outras asserções de capítulo), um bloco específico do tema:

```python
_co = next(c for c in d['chapters'] if c['themeKey'] == 'central-operacoes-193')
assert _co['articles'], 'central-operacoes-193 sem artigos (Fase 2A deveria ter preenchido)'
assert _co['parte'] == 'servico', _co['parte']
assert _co['primary']['uf'] == 'ba', _co['primary']['uf']
assert 'to' in _co['alternatives'], 'faltou a alternativa TO em central-operacoes-193'
```

- [ ] **Step 2: Rodar o teste e confirmar que FALHA**

Run: `"/Users/wandriobandeira/Projetos de dev Sistemas/05. Comparativo-de-cargos-e-funcoes/.venv-pipeline/bin/python" scripts/test_regulamento_structure.py`
Expected: `AssertionError` em "central-operacoes-193 sem artigos ..." (o tema ainda está vazio).

- [ ] **Step 3: Adicionar as entradas de CONFIG (BA e TO)** — em `scripts/extrair_regulamentos.py`, dentro do dict `CONFIG`, após a última entrada existente, inserir:

```python
    'ba': {
        'md': 'Bahia - Regulamento de Serviço.md',
        'src': 'cf. CBMBA, Norma Operacional nº 01/2021, Art. {n}',
        'slice_between': ('R E S O L V E', None),
        # Cabeçalho de página repetido NO MEIO dos artigos (Art. 9º e 18 são longos):
        'strip_lines': [re.compile(r'^\s*NORMA OPERACIONAL\b'), re.compile(r'^\s*Pág\.\s*\d+\s*$')],
        'ranges': [
            (8, 9, 'central-operacoes-193', 'exata', 'NOp 01/2021, Seção II — Supervisor do Teledespacho (CICOM)'),
            (18, 18, 'central-operacoes-193', 'exata', 'NOp 01/2021, Seção X — Operador do Teledespacho (CICOM)'),
        ],
        'overrides': {},
    },
    'to': {
        'md': 'Tocantins - Regulamento de Serviço.md',
        'src': 'cf. CBMTO, NGA do SIOP (Diretriz COB, Portaria nº 003/2019), Art. {n}',
        # Anexo 2 reinicia a numeração em "Art. 1º"; fatiar a partir do cabeçalho do Anexo 2
        # para não colidir com os artigos homônimos do corpo principal. Marcador conferido no Step 4.
        'slice_between': ('ANEXO 2', None),
        'strip_lines': [re.compile(r'^\s*QUARTEL DO COMANDO GERAL\b')],
        'ranges': [
            (12, 14, 'central-operacoes-193', 'exata', 'NGA SIOP (Anexo 2) — Coordenador de Operações, Despachante e Atendente'),
        ],
        'overrides': {},
    },
```

- [ ] **Step 4: Verificar o marcador de fatiamento do Tocantins** — o marcador `'ANEXO 2'` faz match por substring na PRIMEIRA linha que o contém. Confirmar que ele cai no cabeçalho real do Anexo (e não num sumário anterior):

Run: `grep -n "ANEXO 2" "/Users/wandriobandeira/Projetos de dev Sistemas/05. Comparativo-de-cargos-e-funcoes/database/markdown/Tocantins - Regulamento de Serviço.md"`
Expected: idealmente uma única ocorrência (o cabeçalho do Anexo, ~linha 563). Se houver mais de uma (ex.: um sumário citando "ANEXO 2" antes), trocar o `slice_between` do `'to'` por um trecho mais distintivo da MESMA linha do cabeçalho real — ex.: `('ANEXO 2 – NORMA GERAL DE AÇÃO', None)` ou `('SISTEMA INTEGRADO DE OPERAÇÕES E CENTRAIS', None)` — escolhendo o que só aparece no cabeçalho real. A prova final é o Step 6 (caputs corretos + verbatim).

- [ ] **Step 5: Mudar a fonte primária do tema** — em `scripts/regulamento_enrichment.py`, na dict `PRIMARY_SOURCE`, trocar a linha do tema:

```python
    "central-operacoes-193": "ba",  # Fase 2A: Bahia/CICOM (Supervisor e Operador de Teledespacho)
```

- [ ] **Step 6: Extrair, verificar verbatim e conferir a contagem**

Run: `"/Users/wandriobandeira/Projetos de dev Sistemas/05. Comparativo-de-cargos-e-funcoes/.venv-pipeline/bin/python" scripts/extrair_regulamentos.py ba to`
Expected: `ba: 3 artigos -> regulamento_enrichment_ba.py | central-operacoes-193=3` e `to: 3 artigos -> regulamento_enrichment_to.py | central-operacoes-193=3`. Se aparecer "Art. N fora de qualquer range — ignorado" para outros artigos, é esperado (só as faixas de teledespacho entram). Se a contagem da BA ou do TO não for 3, revisar faixas/marcador (Step 3/4) — NÃO prosseguir com contagem errada.

Run: `"/Users/wandriobandeira/Projetos de dev Sistemas/05. Comparativo-de-cargos-e-funcoes/.venv-pipeline/bin/python" scripts/verificar_verbatim.py`
Expected: OK (todo caput/dispositivo de BA e TO existe literal na fonte). Se acusar erro, ajustar `strip_lines`/faixa e reextrair — nunca editar o arquivo gerado à mão.

- [ ] **Step 7: Regenerar os JSONs (futura + atual)**

Run: `"/Users/wandriobandeira/Projetos de dev Sistemas/05. Comparativo-de-cargos-e-funcoes/.venv-pipeline/bin/python" scripts/build_regulamento_structure.py`
Expected: `Capítulos: 16 | artigos propostos: 413 | ...` e NÃO deve mais listar `central-operacoes-193` em "Capítulos pendentes".

Run: `"/Users/wandriobandeira/Projetos de dev Sistemas/05. Comparativo-de-cargos-e-funcoes/.venv-pipeline/bin/python" scripts/build_regulamento_structure_atual.py`
Expected: `16 temas · 413 artigos (isolados como reg:atual:)`.

- [ ] **Step 8: Rodar o teste e confirmar que PASSA (Python + JS)**

Run: `"/Users/wandriobandeira/Projetos de dev Sistemas/05. Comparativo-de-cargos-e-funcoes/.venv-pipeline/bin/python" scripts/test_regulamento_structure.py`
Expected: `OK — ... (16 capítulos, 413 artigos, ...)`.

Run: `node --test`
Expected: `tests 110 / pass 110 / fail 0` (nenhuma mudança JS; só não pode regredir).

- [ ] **Step 9: Commit**

```bash
git add scripts/extrair_regulamentos.py scripts/regulamento_enrichment.py scripts/regulamento_enrichment_ba.py scripts/regulamento_enrichment_to.py scripts/test_regulamento_structure.py database/regulamento_structure.json database/atual/regulamento_structure.json
git commit -m "feat(regulamento): preenche central-operacoes-193 (teledespacho verbatim BA+TO)

Bahia (CICOM) primária: Art. 8-9 (Supervisor) e 18 (Operador de Teledespacho);
Tocantins alternativa: Art. 12-14 do Anexo 2 (Coordenador/Despachante/Atendente).
Roraima fora — 193 difuso no Art. 54, não isolável. Fase 2A.

Co-Authored-By: Claude <noreply@anthropic.com>"
```

---

### Task 2: Prova visual + registro

**Files:**
- Modify: `.claude/PENDENCIAS.md`
- Evidence: screenshot Playwright do tema preenchido

**Interfaces:**
- Consumes: Task 1.

- [ ] **Step 1: Prova visual (regra dura do crachá)** — subir `npm run dev`, logar (conta do Wândrio), navegar a `http://localhost:5173/regulamento?cenario=futura`, avançar para "Revisar e curar a minuta", rolar até a Parte II e capturar screenshot do capítulo "DA CENTRAL DE OPERAÇÕES E DO TELEDESPACHO" — agora COM artigos (fonte Bahia; alternativa TO) e SEM o `⏳` no sumário. Abrir o screenshot no Preview.
Expected: o tema mostra o texto do Supervisor/Operador de Teledespacho; o `⏳` sumiu do sumário.

- [ ] **Step 2: Prova de contagem**

Run: `"/Users/wandriobandeira/Projetos de dev Sistemas/05. Comparativo-de-cargos-e-funcoes/.venv-pipeline/bin/python" -c "import json; d=json.load(open('database/regulamento_structure.json')); co=[c for c in d['chapters'] if c['themeKey']=='central-operacoes-193'][0]; print('artigos no tema:', len(co['articles']), '| alternativas:', list(co['alternatives'].keys())); ids=[a['editId'] for c in d['chapters'] for a in c['articles']]; print('total:', len(ids), '| únicos:', len(set(ids)))"`
Expected: `artigos no tema: 3 | alternativas: ['to']` e `total: 413 | únicos: 413`. Colar a saída na entrega.

- [ ] **Step 3: Registrar no backlog** — em `.claude/PENDENCIAS.md`, mover para "Concluído (mês atual)" um item "Regulamento — Fase 2A: 16º tema (Central de Operações 193) preenchido — BA primária + TO alternativa; RR fora (193 difuso)"; e ajustar a pendência da Fase 2 para deixar claro que restam as Fatias B (reforço da Parte II com o resto de BA/RR/TO + normas de AL), C (temas magros da Parte I) e D (ES cirúrgico).

- [ ] **Step 4: Commit**

```bash
git add .claude/PENDENCIAS.md
git commit -m "chore(handoff): Fase 2A concluída (16º tema preenchido); restam Fatias B/C/D

Co-Authored-By: Claude <noreply@anthropic.com>"
```

- [ ] **Step 5: Entregar** — invocar a skill `abrir-app` para entregar o link verificado ao Wândrio, com o screenshot do tema preenchido.
