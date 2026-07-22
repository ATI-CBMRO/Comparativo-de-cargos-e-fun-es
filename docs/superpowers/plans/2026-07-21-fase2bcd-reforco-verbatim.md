# Fase 2, Fatias B+C+D — Reforço verbatim do Regulamento — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Reforçar com texto verbatim novo: (B) a Parte II com o resto de BA/RR/TO e 5 normas de AL; (C) os temas `cerimonial-honras` e `pessoal-quadros` da Parte I com o RISG do Exército; (D) `servico-operacional` e `seguranca-contra-incendio` com 3 trechos cirúrgicos do ES.

**Architecture:** Reusa o extrator determinístico (`extrair_regulamentos.py`) já maduro. B e C usam o modo padrão `extract_ranges` (faixa de "Art. N" dentro de um `slice_between`). D usa o modo `extract_line_slices` (faixas por linha absoluta do arquivo) — necessário porque o ES reinicia a numeração "Art. N" a cada órgão. C exige um passo extra: converter `RISG.pdf` para `database/markdown/RISG.md` via o conversor oficial antes de extrair, e registrar o RISG como pseudo-fonte (`risg`, rotulado "Exército Brasileiro") — só como alternativa, nunca primária.

**Tech Stack:** Python 3.12 (venv `.venv-pipeline/`), `node --test`.

**Spec:** `docs/superpowers/specs/2026-07-21-fase2bcd-reforco-verbatim-design.md`.

## Contexto factual (leitura de fonte já feita — 2026-07-21)
Ver spec §3-5 para a tabela completa de faixas por fonte. Resumo:
- **Bahia**: +17 artigos (Art. 1-7, 10-17, 19-35 — os únicos já usados são 8-9 e 18).
- **Roraima**: 97 artigos (documento inteiro; nenhum usado ainda).
- **Tocantins**: +7 artigos do Anexo 2 (Art. 1-2, 3-5, 6, 7, 8, 9-11, 15 — os já usados são 12-14).
- **Alagoas**: 5 documentos com corpo articulado (NO 03, 04, 06, 07, 11); 4 DOBs (05-08) ficam de fora (sem "Art. N").
- **RISG**: Art. 321-327, 337-343, 344-348(parcial), 461-462(parcial) → `cerimonial-honras`; Art. 364-375, 376-385, 391-410, 411-414 → `pessoal-quadros`.
- **ES**: linhas 11053-11136 (CAT, SCI), 12424-12454 e 13573-13701 (1º BBM, servico-operacional), 32072-32246 (CERD, servico-operacional).

## Global Constraints
- Comunicação/UI em pt-BR.
- Python SEMPRE via `.venv-pipeline/bin/python`.
- `scripts/regulamento_enrichment_<uf>.py` são GERADOS — nunca editar à mão.
- Nomes de módulo Python NÃO podem ter hífen — usar underscore (`al_no03`, não `al-no03`).
- Verbatim é lei: `verificar_verbatim.py` deve passar; caput que não bate se corrige na
  faixa/`strip_lines` e reextrai, nunca se ajusta à mão.
- NÃO tocar no 16º tema (`central-operacoes-193`, já fechado na Fatia A), nem na divisão 12
  Geral/4 Serviço, nem na trilha do RI, nem em `database/atual/organs_detail/ro.json`.
- `node --test` deve terminar verde em todo commit.
- Caminhos absolutos no Bash, sem `cd ... &&`.

---

### Task 1: Fatia B — reforço da Parte II (BA, RR, TO, 5×AL)

**Files:**
- Modify: `scripts/extrair_regulamentos.py` (estender `CONFIG['ba']` e `CONFIG['to']`; adicionar `CONFIG['rr']`, `CONFIG['al_no03']`, `CONFIG['al_no04']`, `CONFIG['al_no06']`, `CONFIG['al_no07']`, `CONFIG['al_no11']`)
- Modify: `scripts/regulamento_enrichment.py` (adicionar as 5 chaves `al_no0X` a `REGULAMENTO_DOCS`)
- Modify: `scripts/build_regulamento_structure.py` (adicionar as 5 chaves a `STATE_NAMES`)
- Generate: `regulamento_enrichment_ba.py`, `_to.py` (regenerados), `_rr.py`, `_al_no03.py`, `_al_no04.py`, `_al_no06.py`, `_al_no07.py`, `_al_no11.py`
- Regenerate: `database/regulamento_structure.json`, `database/atual/regulamento_structure.json`

**Interfaces:**
- Produces: os temas de Serviço (e alguns de Geral, via as bordas de disposições) ganham `alternatives` novas de BA/RR/TO/AL. Nenhum `primary` muda nesta task.

- [ ] **Step 1: Estender `CONFIG['ba']`** — em `scripts/extrair_regulamentos.py`, no `ranges` de `CONFIG['ba']` (já existe com Art. 8-9 e 18), ACRESCENTAR (mantendo as 2 faixas existentes):

```python
            (1, 1, 'disposicoes-preliminares', 'exata', 'NOp 01/2021 — objeto da Portaria'),
            (2, 2, 'disposicoes-preliminares', 'exata', 'NOp 01/2021, Cap. I — Da Finalidade'),
            (3, 3, 'disposicoes-preliminares', 'exata', 'NOp 01/2021, Cap. II — Dos Objetivos'),
            (4, 4, 'servico-operacional', 'exata', 'NOp 01/2021, Cap. III — Objetivos Básicos do Serviço Operacional'),
            (5, 5, 'organizacao-geral', 'exata', 'NOp 01/2021, Cap. IV — Das Funções Operacionais'),
            (6, 7, 'atribuicoes-funcoes', 'exata', 'NOp 01/2021, Cap. V, Seções I-II — Superior de Dia'),
            (10, 17, 'atribuicoes-funcoes', 'exata', 'NOp 01/2021, Cap. V, Seções III-IX — Supervisor a Integrantes da Guarnição'),
            (19, 19, 'disciplina-correicao', 'exata', 'NOp 01/2021, Cap. VI — Das Medidas Disciplinares'),
            (20, 25, 'servico-interno-dia', 'exata', 'NOp 01/2021, Cap. VII — Da Passagem de Serviço'),
            (26, 35, 'disposicoes-finais', 'exata', 'NOp 01/2021 — Disposições Finais'),
```

- [ ] **Step 2: Estender `CONFIG['to']`** — no `ranges` de `CONFIG['to']` (já existe com Art. 12-14 do Anexo 2), ACRESCENTAR (mesmo `slice_between=('ANEXO 2', None)`):

```python
            (1, 2, 'disposicoes-preliminares', 'exata', 'NGA SIOP (Anexo 2) — Finalidade e Missão'),
            (3, 5, 'organizacao-geral', 'exata', 'NGA SIOP (Anexo 2) — Estrutura do SIOP/BM'),
            (6, 6, 'competencias-direcao', 'exata', 'NGA SIOP (Anexo 2) — Do Gerente'),
            (7, 7, 'servico-interno-dia', 'exata', 'NGA SIOP (Anexo 2) — Regime do Serviço Administrativo'),
            (8, 8, 'atribuicoes-funcoes', 'exata', 'NGA SIOP (Anexo 2) — Atribuições do Serviço Administrativo'),
            (9, 11, 'servico-operacional', 'exata', 'NGA SIOP (Anexo 2) — Escalas do Serviço Operacional'),
            (15, 15, 'disposicoes-finais', 'exata', 'NGA SIOP (Anexo 2) — Disposição Geral'),
```

⚠️ NÃO adicionar faixas do CORPO PRINCIPAL de Tocantins (Art. 1-13, 16) — fica de fora por
decisão do spec §2 (colisão de numeração com o Anexo 2 no tema `atribuicoes-funcoes`, Art. 8
existe nos dois blocos).

- [ ] **Step 3: Adicionar `CONFIG['rr']`** — nova entrada em `scripts/extrair_regulamentos.py`:

```python
    'rr': {
        'md': 'Roraíma - Regulamento de Serviço.md',
        'src': 'cf. CBMRR, INOp 01/2024 (Serviço Diário dos Oficiais), Art. {n}',
        'slice_between': ('CONCEITUAÇÃO BÁSICA', 'ANEXO ÚNICO'),
        'ranges': [
            (1, 1, 'disposicoes-preliminares', 'exata', 'Cap. I — Conceituação Básica'),
            (2, 2, 'atribuicoes-funcoes', 'exata', 'Cap. II, Seção I — Superior de Dia'),
            (3, 6, 'pessoal-quadros', 'exata', 'Cap. II, Seção II — Escalas (Superior de Dia)'),
            (7, 9, 'servico-interno-dia', 'exata', 'Cap. II, Seção III — Passagem de Serviço (Superior de Dia)'),
            (10, 11, 'atribuicoes-funcoes', 'exata', 'Cap. II, Seção IV — Prescrições Gerais (Superior de Dia)'),
            (12, 12, 'atribuicoes-funcoes', 'exata', 'Cap. III, Seção I — Coordenador de Dia'),
            (13, 18, 'servico-operacional', 'exata', 'Cap. III, Seção II — Poder de Pronto Emprego'),
            (19, 22, 'servico-operacional', 'exata', 'Cap. III, Seção III — Ocorrências de Defesa Civil'),
            (23, 24, 'pessoal-quadros', 'exata', 'Cap. III, Seção IV — Escalas (Coordenador de Dia)'),
            (25, 28, 'servico-interno-dia', 'exata', 'Cap. III, Seção V — Passagem de Serviço (Coordenador de Dia)'),
            (29, 33, 'atribuicoes-funcoes', 'exata', 'Cap. III, Seção VI — Prescrições Gerais (Coordenador de Dia)'),
            (34, 34, 'atribuicoes-funcoes', 'exata', 'Cap. IV, Seção I — Oficial de Dia/Comandante do Socorro'),
            (35, 35, 'servico-operacional', 'exata', 'Cap. IV, Seção II — Emprego'),
            (36, 37, 'pessoal-quadros', 'exata', 'Cap. IV, Seção III — Escalas (Oficial de Dia)'),
            (38, 40, 'servico-interno-dia', 'exata', 'Cap. IV, Seção IV — Passagem de Serviço'),
            (41, 44, 'atribuicoes-funcoes', 'exata', 'Cap. IV, Seção V — Prescrições Gerais'),
            (45, 45, 'atribuicoes-funcoes', 'exata', 'Cap. V, Seção I — Oficial de Incêndio/Salvamento/EPH'),
            (46, 47, 'pessoal-quadros', 'exata', 'Cap. V, Seção II — Escalas'),
            (48, 50, 'servico-interno-dia', 'exata', 'Cap. V, Seção III — Passagem de Serviço'),
            (51, 53, 'atribuicoes-funcoes', 'exata', 'Cap. V, Seção IV — Prescrições Gerais'),
            (54, 54, 'atribuicoes-funcoes', 'exata', 'Cap. VI, Seção I — Oficial de Comunicação'),
            (55, 56, 'pessoal-quadros', 'exata', 'Cap. VI, Seção II — Escalas'),
            (57, 59, 'servico-interno-dia', 'exata', 'Cap. VI, Seção III — Passagem de Serviço'),
            (60, 62, 'atribuicoes-funcoes', 'exata', 'Cap. VI, Seção IV — Prescrições Gerais'),
            (63, 63, 'atribuicoes-funcoes', 'exata', 'Cap. VII, Seção I — Oficial de Saúde'),
            (64, 66, 'pessoal-quadros', 'exata', 'Cap. VII, Seção II — Escalas'),
            (67, 69, 'servico-interno-dia', 'exata', 'Cap. VII, Seção III — Passagem de Serviço'),
            (70, 71, 'atribuicoes-funcoes', 'exata', 'Cap. VII, Seção IV — Prescrições Gerais'),
            (72, 72, 'disciplina-correicao', 'exata', 'Cap. VIII, Seção I — Oficial de Correições e Disciplina'),
            (73, 74, 'pessoal-quadros', 'exata', 'Cap. VIII, Seção II — Escalas'),
            (75, 76, 'servico-interno-dia', 'exata', 'Cap. VIII, Seção III — Passagem de Serviço'),
            (77, 78, 'disciplina-correicao', 'exata', 'Cap. VIII, Seção IV — Prescrições Gerais'),
            (79, 79, 'atribuicoes-funcoes', 'exata', 'Cap. IX, Seção I — Oficial de Sobreaviso'),
            (80, 82, 'pessoal-quadros', 'exata', 'Cap. IX, Seção II — Escalas'),
            (83, 84, 'servico-interno-dia', 'exata', 'Cap. IX, Seção III — Passagem de Serviço'),
            (85, 88, 'atribuicoes-funcoes', 'exata', 'Cap. IX, Seção IV — Prescrições Gerais'),
            (89, 93, 'disposicoes-finais', 'exata', 'Cap. X — Disposições Finais (deveres, competência do COCI)'),
            (94, 97, 'disposicoes-finais', 'exata', 'Casos omissos, revogação, vigência'),
        ],
        'overrides': {},
    },
```

- [ ] **Step 4: Adicionar as 5 entradas de Alagoas** — novas entradas em `CONFIG`:

```python
    'al_no03': {
        'md': 'Alagoas - Norma Operacional 03.md',
        'src': 'cf. CBMAL, Norma Operacional nº 03, Art. {n}',
        'slice_between': (None, None),
        'ranges': [
            (1, 5, 'servico-operacional', 'exata', 'NO 03 — Escalas operacionais por função'),
            (5, 6, 'disposicoes-finais', 'exata', 'NO 03 — Vigência e revogação'),
        ],
        'overrides': {},
    },
    'al_no04': {
        'md': 'Alagoas - Norma Operacional 04.md',
        'src': 'cf. CBMAL, Norma Operacional nº 04, Art. {n}',
        'slice_between': (None, None),
        'ranges': [
            (1, 2, 'servico-interno-dia', 'exata', 'NO 04 — Cronograma diário e flexibilização'),
            (3, 4, 'disposicoes-finais', 'exata', 'NO 04 — Vigência e revogação'),
        ],
        'overrides': {},
    },
    'al_no06': {
        'md': 'Alagoas - Norma Operacional 06.md',
        'src': 'cf. CBMAL, Norma Operacional nº 06, Art. {n}',
        'slice_between': (None, None),
        'ranges': [
            (1, 3, 'servico-interno-dia', 'exata', 'NO 06 — Relatório de Serviço Diário e Mensal'),
            (4, 5, 'disposicoes-finais', 'exata', 'NO 06 — Vigência e revogação'),
        ],
        'overrides': {},
    },
    'al_no07': {
        'md': 'Alagoas - Norma Operacional 07.md',
        'src': 'cf. CBMAL, Norma Operacional nº 07, Art. {n}',
        'slice_between': (None, None),
        'ranges': [
            (1, 2, 'servico-interno-dia', 'exata', 'NO 07 — Relatório Mensal de Serviços do Posto'),
            (3, 4, 'disposicoes-finais', 'exata', 'NO 07 — Vigência e revogação'),
        ],
        'overrides': {},
    },
    'al_no11': {
        'md': 'Alagoas - Norma Operacional 11.md',
        'src': 'cf. CBMAL, Norma Operacional nº 11, Art. {n}',
        'slice_between': (None, None),
        'ranges': [
            (1, 1, 'disposicoes-preliminares', 'exata', 'NO 11, Cap. I — Finalidade e objeto'),
            (2, 8, 'servico-interno-dia', 'exata', 'NO 11, Cap. II — Condições do serviço diário do Canil'),
            (9, 10, 'atribuicoes-funcoes', 'exata', 'NO 11, Cap. III — Rotina de cinotécnicos e SVR'),
            (11, 12, 'servico-interno-dia', 'exata', 'NO 11, Cap. IV — Canal de comunicação interna'),
            (13, 15, 'ensino-instrucao', 'exata', 'NO 11, Cap. V — Treinamento operacional'),
            (16, 20, 'servico-operacional', 'exata', 'NO 11, Cap. VI — Emprego e prazos de acionamento'),
            (21, 23, 'disposicoes-finais', 'exata', 'NO 11, Cap. VII — Casos omissos, revogação e vigência'),
        ],
        'overrides': {},
    },
```

- [ ] **Step 5: Registrar as novas chaves** — em `scripts/regulamento_enrichment.py`, no dict `REGULAMENTO_DOCS`, ACRESCENTAR:

```python
    "al_no03": {"label": "Norma Operacional nº 03 (CBMAL)", "md": "Alagoas - Norma Operacional 03.md"},
    "al_no04": {"label": "Norma Operacional nº 04 (CBMAL)", "md": "Alagoas - Norma Operacional 04.md"},
    "al_no06": {"label": "Norma Operacional nº 06 (CBMAL)", "md": "Alagoas - Norma Operacional 06.md"},
    "al_no07": {"label": "Norma Operacional nº 07 (CBMAL)", "md": "Alagoas - Norma Operacional 07.md"},
    "al_no11": {"label": "Norma Operacional nº 11 — Canil (CBMAL)", "md": "Alagoas - Norma Operacional 11.md"},
```

`'rr'` já existe em `REGULAMENTO_DOCS` desde a Fase 1 — não duplicar.

Em `scripts/build_regulamento_structure.py`, no dict `STATE_NAMES`, ACRESCENTAR:

```python
    'al_no03': 'Alagoas', 'al_no04': 'Alagoas', 'al_no06': 'Alagoas',
    'al_no07': 'Alagoas', 'al_no11': 'Alagoas',
```

- [ ] **Step 6: Extrair, verificar, rebuild**

Run: `"/Users/wandriobandeira/Projetos de dev Sistemas/05. Comparativo-de-cargos-e-funcoes/.venv-pipeline/bin/python" scripts/extrair_regulamentos.py ba to rr al_no03 al_no04 al_no06 al_no07 al_no11`
Expected: cada UF imprime `<uf>: N artigos -> regulamento_enrichment_<uf>.py | ...`. Conferir que `ba` soma **35** (3 já existentes + 32 novos = TODOS os 35 artigos de Bahia usados — bom sinal de completude) e `to` soma **15** (3+12 = TODO o Anexo 2 de Tocantins usado). `rr` deve somar 97 (documento inteiro). Se algum número não bater, investigar a faixa/slice antes de prosseguir — não prosseguir com contagem inconsistente.

⚠️ **Nota sobre `al_no03`**: o subagente que leu a fonte reportou que o documento tem **"Art. 5º" duplicado** no original (um sobre área de atuação dos oficiais, outro que deveria ser "Art. 6º" mas veio numerado errado como "Art. 5º" de novo, tratando de vigência). O extrator deduplica por número de artigo (mantém só a PRIMEIRA ocorrência de cada "Art. N"), então a segunda ocorrência do "Art. 5º" será DESCARTADA com um aviso `AVISO al_no03: Art. 5 repetido...` — isso é esperado e correto (é um defeito do documento-fonte, não do extrator). Conferir no output qual conteúdo do Art. 5 foi mantido (deve ser o de "área de atuação dos oficiais") e ajustar o `ranges` de `al_no03` se necessário para refletir só o que foi realmente capturado — não force as duas faixas com o mesmo número.

Run: `"/Users/wandriobandeira/Projetos de dev Sistemas/05. Comparativo-de-cargos-e-funcoes/.venv-pipeline/bin/python" scripts/verificar_verbatim.py`
Expected: OK, sem erros. Ajustar `strip_lines`/faixa e reextrair se necessário — nunca editar o arquivo gerado à mão.

Run: `"/Users/wandriobandeira/Projetos de dev Sistemas/05. Comparativo-de-cargos-e-funcoes/.venv-pipeline/bin/python" scripts/build_regulamento_structure.py && "/Users/wandriobandeira/Projetos de dev Sistemas/05. Comparativo-de-cargos-e-funcoes/.venv-pipeline/bin/python" scripts/build_regulamento_structure_atual.py`
Expected: capítulos continuam 16; total de artigos sobe (registrar o número exato impresso — será usado no teste do Step 7).

- [ ] **Step 7: Atualizar o teste e confirmar verde**

Em `scripts/test_regulamento_structure.py`, localizar a asserção `assert len(edit_ids) >= 410` e mantê-la (é `>=`, continua válida — não precisa mudar o valor).

Run: `"/Users/wandriobandeira/Projetos de dev Sistemas/05. Comparativo-de-cargos-e-funcoes/.venv-pipeline/bin/python" scripts/test_regulamento_structure.py`
Expected: `OK — ... capítulos, N artigos ...` (N = 413 + novos desta task).

Run: `node --test`
Expected: `pass 110 / fail 0`.

- [ ] **Step 8: Commit**

```bash
git add scripts/extrair_regulamentos.py scripts/regulamento_enrichment.py scripts/build_regulamento_structure.py scripts/regulamento_enrichment_ba.py scripts/regulamento_enrichment_to.py scripts/regulamento_enrichment_rr.py scripts/regulamento_enrichment_al_no03.py scripts/regulamento_enrichment_al_no04.py scripts/regulamento_enrichment_al_no06.py scripts/regulamento_enrichment_al_no07.py scripts/regulamento_enrichment_al_no11.py database/regulamento_structure.json database/atual/regulamento_structure.json
git commit -m "feat(regulamento): Fatia B — reforça Parte II (resto de BA/TO, RR inteiro, 5 normas AL)

Co-Authored-By: Claude <noreply@anthropic.com>"
```

---

### Task 2: Fatia C — RISG reforça cerimonial-honras e pessoal-quadros

**Files:**
- Create: `database/markdown/RISG.md` (via conversor oficial)
- Modify: `scripts/extrair_regulamentos.py` (adicionar `CONFIG['risg']`)
- Modify: `scripts/regulamento_enrichment.py` (adicionar `risg` a `REGULAMENTO_DOCS`)
- Modify: `scripts/build_regulamento_structure.py` (adicionar `risg` a `STATE_NAMES`)
- Generate: `regulamento_enrichment_risg.py`
- Regenerate: `database/regulamento_structure.json`, `database/atual/regulamento_structure.json`
- Modify: `scripts/test_regulamento_structure.py`

**Interfaces:**
- Produces: `risg` aparece SÓ em `alternatives` de `cerimonial-honras` e `pessoal-quadros` — nunca em `primary`.

- [ ] **Step 1: Converter o RISG para o pipeline oficial** — o RISG ainda não foi convertido pelo conversor padrão (só existe um `.txt` avulso de uma sessão anterior). Rodar:

Run: `"/Users/wandriobandeira/Projetos de dev Sistemas/05. Comparativo-de-cargos-e-funcoes/.venv-pipeline/bin/python" scripts/convert_to_markdown.py`
Expected: entre as linhas de saída, `Successfully converted: RISG.pdf -> RISG.md` (o conversor roda para TODOS os PDFs da pasta — os demais já convertidos ficam idênticos, sem risco). Confirmar: `ls "/Users/wandriobandeira/Projetos de dev Sistemas/05. Comparativo-de-cargos-e-funcoes/database/markdown/RISG.md"`.

- [ ] **Step 2: Adicionar `CONFIG['risg']`** — em `scripts/extrair_regulamentos.py`:

```python
    'risg': {
        'md': 'RISG.md',
        'src': 'cf. Exército Brasileiro, RISG — R-1 (Portaria SGEx nº 51/2003), Art. {n}',
        'slice_between': ('TÍTULO I', None),
        'ranges': [
            (321, 327, 'cerimonial-honras', 'exata', 'Tít. VI, Cap. I — Dos Símbolos Nacionais'),
            (337, 343, 'cerimonial-honras', 'exata', 'Tít. VI, Cap. IV — Das Festas Nacionais e Militares'),
            (344, 348, 'cerimonial-honras', 'parcial', 'Tít. VI, Cap. IV — Datas específicas do Exército (estrutura reaproveitável)'),
            (461, 462, 'cerimonial-honras', 'parcial', 'Tít. IX, Cap. VIII — Das Honras Militares (remete a outro regulamento)'),
            (364, 375, 'pessoal-quadros', 'exata', 'Tít. VIII, Cap. I — Do Cargo e da Função Militar'),
            (376, 385, 'pessoal-quadros', 'exata', 'Tít. VIII, Cap. II, Seções I-II — Substituições (normas gerais e guarnições)'),
            (391, 410, 'pessoal-quadros', 'exata', 'Tít. VIII, Cap. II, Seções IV-V — Substituições entre oficiais e praças'),
            (411, 414, 'pessoal-quadros', 'exata', 'Tít. VIII, Cap. III — Da Qualificação das Praças'),
        ],
        'overrides': {},
    },
```

⚠️ NÃO incluir art. 328-336 (símbolos do Exército, sem paralelo em CBM) nem 386-390
(substituição entre oficiais-generais, cargo inexistente em CBM estadual) — ficam de fora por
decisão do spec §2.

- [ ] **Step 3: Registrar a chave `risg`** — em `scripts/regulamento_enrichment.py`, `REGULAMENTO_DOCS`:

```python
    "risg": {"label": "RISG — R-1 do Exército Brasileiro (Portaria SGEx nº 51/2003)", "md": "RISG.md"},
```

Em `scripts/build_regulamento_structure.py`, `STATE_NAMES`:

```python
    'risg': 'Exército Brasileiro',
```

- [ ] **Step 4: Extrair, verificar, rebuild**

Run: `"/Users/wandriobandeira/Projetos de dev Sistemas/05. Comparativo-de-cargos-e-funcoes/.venv-pipeline/bin/python" scripts/extrair_regulamentos.py risg`
Expected: `risg: 33 artigos -> regulamento_enrichment_risg.py | cerimonial-honras=17, pessoal-quadros=44` aproximadamente (7+7+5+2=21 artigos-linha para cerimonial mas alguns são faixas de vários artigos cada — conferir a contagem real impressa; o que importa é que NENHUM artigo fora das faixas configuradas apareça, e que a soma bata com (327-321+1)+(343-337+1)+(348-344+1)+(462-461+1)+(375-364+1)+(385-376+1)+(410-391+1)+(414-411+1) = 7+7+5+2+12+10+20+4 = 67 artigos).

Run: `"/Users/wandriobandeira/Projetos de dev Sistemas/05. Comparativo-de-cargos-e-funcoes/.venv-pipeline/bin/python" scripts/verificar_verbatim.py`
Expected: OK.

Run: `"/Users/wandriobandeira/Projetos de dev Sistemas/05. Comparativo-de-cargos-e-funcoes/.venv-pipeline/bin/python" scripts/build_regulamento_structure.py && "/Users/wandriobandeira/Projetos de dev Sistemas/05. Comparativo-de-cargos-e-funcoes/.venv-pipeline/bin/python" scripts/build_regulamento_structure_atual.py`
Expected: capítulos continuam 16; total de artigos sobe mais ~67.

- [ ] **Step 5: Adicionar teste que `risg` nunca é primária**

Em `scripts/test_regulamento_structure.py`, após as asserções de capítulo existentes, adicionar:

```python
for c in d['chapters']:
    assert c['primary']['uf'] != 'risg', f"RISG não pode ser fonte primária: {c['themeKey']}"
```

Run: `"/Users/wandriobandeira/Projetos de dev Sistemas/05. Comparativo-de-cargos-e-funcoes/.venv-pipeline/bin/python" scripts/test_regulamento_structure.py`
Expected: OK.

Run: `node --test`
Expected: `pass 110 / fail 0`.

- [ ] **Step 6: Commit**

```bash
git add database/markdown/RISG.md scripts/extrair_regulamentos.py scripts/regulamento_enrichment.py scripts/build_regulamento_structure.py scripts/regulamento_enrichment_risg.py scripts/test_regulamento_structure.py database/regulamento_structure.json database/atual/regulamento_structure.json
git commit -m "feat(regulamento): Fatia C — RISG reforça cerimonial-honras e pessoal-quadros

RISG entra como pseudo-fonte 'Exército Brasileiro', só como alternativa
(nunca primária). Uniformes-apresentacao ficou de fora (sem achado forte
nas faixas lidas do RISG).

Co-Authored-By: Claude <noreply@anthropic.com>"
```

---

### Task 3: Fatia D — ES reforça servico-operacional e seguranca-contra-incendio

**Files:**
- Modify: `scripts/extrair_regulamentos.py` (adicionar `CONFIG['es']`, usando `extract_line_slices`)
- Modify: `scripts/regulamento_enrichment.py` (adicionar `es` a `REGULAMENTO_DOCS`)
- Modify: `scripts/build_regulamento_structure.py` (adicionar `es` a `STATE_NAMES`)
- Generate: `regulamento_enrichment_es.py`
- Regenerate: `database/regulamento_structure.json`, `database/atual/regulamento_structure.json`

**Interfaces:**
- Consumes: modo `extract_line_slices` já existente em `extrair_regulamentos.py` (chave `line_slices` no CONFIG, em vez de `ranges`+`slice_between`).

- [ ] **Step 1: Adicionar `CONFIG['es']`** — em `scripts/extrair_regulamentos.py`, usando `line_slices` (faixas por LINHA ABSOLUTA do arquivo — necessário porque "Art. N" se repete a cada órgão neste documento):

```python
    'es': {
        'md': 'Espírito Santo - Normas Gerais de Ação.md',
        'src': 'cf. CBMES, Normas Gerais de Ação (2023), Art. {n}',
        'line_slices': [
            (11053, 11136, 'seguranca-contra-incendio', 'exata', 'CAT — Gerência de Vistorias e Seção de Fiscalização'),
            (12424, 12454, 'servico-operacional', 'exata', '1º BBM — Prontidão Operacional e Seção de Operações de Salvamento (SOS)'),
            (13573, 13701, 'servico-operacional', 'exata', '1º BBM — Chefe da SOS e Fiscal do Salvamar'),
            (32072, 32246, 'servico-operacional', 'exata', 'CERD — Finalidade, composição e atribuições gerais'),
        ],
    },
```

⚠️ Usar SÓ o 1º BBM como representante — os outros 5 batalhões repetem o mesmo texto-base
(boilerplate copiado, confirmado na leitura de fonte). Extrair os 6 seria redundância, não
reforço. NÃO incluir as atribuições internas do CERD (Chefe do CERD, GERD, Logística) — fora
do recorte cirúrgico, por decisão do spec §2.

- [ ] **Step 2: Registrar a chave `es`** — em `scripts/regulamento_enrichment.py`, `REGULAMENTO_DOCS`:

```python
    "es": {"label": "Normas Gerais de Ação (2023)", "md": "Espírito Santo - Normas Gerais de Ação.md"},
```

Em `scripts/build_regulamento_structure.py`, `STATE_NAMES`:

```python
    'es': 'Espírito Santo',
```

- [ ] **Step 3: Extrair, verificar, rebuild**

Run: `"/Users/wandriobandeira/Projetos de dev Sistemas/05. Comparativo-de-cargos-e-funcoes/.venv-pipeline/bin/python" scripts/extrair_regulamentos.py es`
Expected: `es: 9 artigos -> regulamento_enrichment_es.py | seguranca-contra-incendio=2, servico-operacional=7` (CAT Art.16-17 = 2; 1º BBM Art.9-10 + Art.30-31 = 4; CERD Art.1-3 = 3; total servico-operacional = 4+3 = 7; total geral 2+7=9). Conferir a soma real impressa — o que importa é que bata exatamente com os 4 blocos configurados, sem artigo extra vazando de outro órgão (o risco real deste documento, já que "Art. N" se repete a cada unidade).

Run: `"/Users/wandriobandeira/Projetos de dev Sistemas/05. Comparativo-de-cargos-e-funcoes/.venv-pipeline/bin/python" scripts/verificar_verbatim.py`
Expected: OK.

Run: `"/Users/wandriobandeira/Projetos de dev Sistemas/05. Comparativo-de-cargos-e-funcoes/.venv-pipeline/bin/python" scripts/build_regulamento_structure.py && "/Users/wandriobandeira/Projetos de dev Sistemas/05. Comparativo-de-cargos-e-funcoes/.venv-pipeline/bin/python" scripts/build_regulamento_structure_atual.py`
Expected: capítulos continuam 16.

Run: `"/Users/wandriobandeira/Projetos de dev Sistemas/05. Comparativo-de-cargos-e-funcoes/.venv-pipeline/bin/python" scripts/test_regulamento_structure.py`
Expected: OK.

Run: `node --test`
Expected: `pass 110 / fail 0`.

- [ ] **Step 4: Commit**

```bash
git add scripts/extrair_regulamentos.py scripts/regulamento_enrichment.py scripts/build_regulamento_structure.py scripts/regulamento_enrichment_es.py database/regulamento_structure.json database/atual/regulamento_structure.json
git commit -m "feat(regulamento): Fatia D — ES reforça servico-operacional e SCI (CAT, 1º BBM, CERD)

Co-Authored-By: Claude <noreply@anthropic.com>"
```

---

### Task 4: Prova visual + preservação + registro final

**Files:**
- Modify: `.claude/PENDENCIAS.md`
- Evidence: screenshot Playwright

**Interfaces:**
- Consumes: Tasks 1-3.

- [ ] **Step 1: Prova de preservação (números ao centavo)**

Run: `"/Users/wandriobandeira/Projetos de dev Sistemas/05. Comparativo-de-cargos-e-funcoes/.venv-pipeline/bin/python" -c "
import json
d=json.load(open('database/regulamento_structure.json'))
ids=[a['editId'] for c in d['chapters'] for a in c['articles']]
print('total:', len(ids), '| únicos:', len(set(ids)))
for c in d['chapters']:
    if c['themeKey'] in ('cerimonial-honras','pessoal-quadros'):
        print(c['themeKey'], '| primary:', c['primary']['uf'], '| alternativas:', sorted(c['alternatives'].keys()))
"`
Expected: total = únicos (sem duplicata); `risg` aparece em `alternatives` de `cerimonial-honras` e `pessoal-quadros`, e NUNCA em `primary`. Colar a saída na entrega.

- [ ] **Step 2: Prova visual (regra dura do crachá)** — subir `npm run dev`, logar, navegar a `/regulamento?cenario=futura`, avançar para "Revisar e curar a minuta", conferir: (a) o tema `cerimonial-honras` ou `pessoal-quadros` mostra "Exército Brasileiro" na lista de fontes/alternativas; (b) um dos temas de Serviço reforçados (ex.: `atribuicoes-funcoes` ou `servico-operacional`) mostra Roraima entre as fontes. Capturar screenshot. Abrir no Preview.

- [ ] **Step 3: Registrar no backlog** — em `.claude/PENDENCIAS.md`, mover para "Concluído": "Regulamento — Fase 2, Fatias B+C+D: reforço verbatim (Serviço: resto de BA/TO, RR inteiro, 5 normas AL; Geral: RISG em cerimonial-honras e pessoal-quadros; ES cirúrgico em servico-operacional/SCI)". Manter como pendente: corpo principal de Tocantins, os 4 DOBs de Alagoas (05-08, sem "Art. N"), e `uniformes-apresentacao` (sem achado forte no RISG) — todos sinalizados, não resolvidos nesta rodada.

- [ ] **Step 4: Commit**

```bash
git add .claude/PENDENCIAS.md
git commit -m "chore(handoff): Fase 2 (Fatias B+C+D) concluída; pendências residuais sinalizadas

Co-Authored-By: Claude <noreply@anthropic.com>"
```

- [ ] **Step 5: Atualizar o Diário de Construção no Obsidian** — acrescentar (não reescrever) à
nota `Codebases/Comparativo-de-cargos-e-funcoes/Diário de Construção da Minuta — rumo à
apresentação ao Comando.md`: o marco desta entrega na linha do tempo, e pelo menos 1 lição
nova (ex.: "nem todo documento é articulado por 'Art. N' — alguns usam seção numerada; nem
toda fonte serve para extração determinística sem adaptação do mecanismo").
