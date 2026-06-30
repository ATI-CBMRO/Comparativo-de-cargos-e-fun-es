# Estrutura interna dos órgãos-folha no organograma da minuta — Plano de Implementação

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Fazer os órgãos-folha do `commandChart` da minuta (DP, DEEI, DPOF, DSAP,
DLOG, CINT, CCS, CINF, CONDEG, DEPDEC, CORREGEDORIA, CAT, CIBM, GBM, GAB-CG, AG,
ASSESSORIAS) exibirem sua estrutura interna (`desdobramentos` do `ro.json`) como
nós filhos expansíveis no organograma de `/minuta-diagramas`, sem alterar
DPO/DOE/COT/CRBM/BBM/BBS/BIFEA/BOA.

**Architecture:** `build_command_chart()` em `scripts/build_minuta_structure.py`
injeta, após montar a árvore por subordinação e antes da cadeia Cia BM/Pel BM, os
`desdobramentos` de cada nó **sem filhos de órgão** como nós estruturais
`isInternal: true` (label truncado no separador " — "/" – " fora de parênteses).
`MinutaOrgChart.jsx` ganha uma classe CSS condicional `moc-box-internal` para esses
nós; o toggle −/+ já existe e funciona automaticamente para qualquer nó com filhos.

**Tech Stack:** Python (pipeline offline), JSON, React/Vite (frontend), CSS puro.

**Spec:** `docs/superpowers/specs/2026-06-30-minuta-organograma-estrutura-interna-design.md`

## Global Constraints

- Não alterar `DPO`, `DOE`, `COT`, `CRBM`, `BBM`, `BBS`, `BIFEA`, `BOA` — só recebem
  nós internos os órgãos que ficaram **sem filhos de órgão** após o roteamento por
  subordinação.
- A injeção deve rodar **antes** do bloco que monta a cadeia Cia BM → Pel BM →
  Guarnição dentro de `bbm` (linha ~400 de `build_minuta_structure.py`), senão
  `bbm` seria marcado como "sem filhos" e ganharia nós internos espúrios antes de
  receber a cadeia de frações real.
- Truncamento de label deve ignorar dash dentro de parênteses (ver função
  `truncate_desdobramento_label` na spec) — testado contra os 107 desdobramentos
  reais antes de codificar.
- Não tocar `MinutaMindMap.jsx`, `/comparar` (`OrgTreeNode`/`buildOrganTree`), nem
  trazer os 11 órgãos novos do RO (`ai, ae, al, ap, apge, af, aci, comissoes,
  conselhos, gab-scg, gab-emg`) para o `ORGAN_ORDER` da minuta.

---

## File Structure

- **Modify:** `scripts/build_minuta_structure.py` — função `build_command_chart()`
  (linhas 338-413): adiciona `truncate_desdobramento_label()` e o loop de injeção.
- **Regenerate (não editar):** `database/minuta_structure.json` via
  `python scripts/build_minuta_structure.py`.
- **Modify:** `src/components/MinutaOrgChart.jsx` — linha 21 (`cls`), adiciona
  classe condicional `moc-box-internal`.
- **Modify:** `src/index.css` — nova regra `.moc-box-internal` próxima às regras
  `.moc-box*` existentes (linhas 2171-2183).

---

### Task 1: Injetar `desdobramentos` como nós internos no `commandChart`

**Files:**
- Modify: `scripts/build_minuta_structure.py:338-413` (função `build_command_chart`)

**Interfaces:**
- Consumes: `organs: dict` (já é parâmetro de `build_command_chart`, contém
  `desdobramentos: list[str]` por órgão — vem de `ro.json`); `nodes: dict[str, dict]`
  já construído pelo loop de roteamento existente (linhas 392-398).
- Produces: cada nó-folha em `nodes` ganha `children: list[dict]` com itens
  `{"organKey": None, "sigla": "", "label": str, "structural": True,
  "isInternal": True, "chapterId": None, "children": []}`. Consumido pela Task 2
  (`MinutaOrgChart.jsx` lê `node.isInternal`).

- [ ] **Step 1: Escrever a função de truncamento e o loop de injeção**

Abrir `scripts/build_minuta_structure.py` e localizar o trecho (linhas ~392-400):

```python
    roots = []
    for k, n in nodes.items():
        p = find_parent(k)
        if p and p in nodes:
            nodes[p]["children"].append(n)
        else:
            roots.append(n)

    if guarnicao is not None and "bbm" in nodes:
```

Substituir por (insere a função antes de `build_command_chart` e o loop de injeção
entre o roteamento e o bloco da Guarnição):

```python
def truncate_desdobramento_label(desd: str) -> str:
    """Corta no separador ' — '/' – ' de topo, ignorando dash DENTRO de
    parênteses (ex.: 'Diretor (QCOBM — formação em Medicina...)' fica intacto —
    o dash ali qualifica o requisito do cargo, não separa nome de unidade da
    sua composição interna)."""
    depth = 0
    for i, ch in enumerate(desd):
        if ch == "(":
            depth += 1
        elif ch == ")":
            depth -= 1
        elif ch in "—–" and depth == 0:
            return desd[:i].strip()
    return desd.strip()


def build_command_chart(organs, chapters):
```

(a função fica em nível de módulo, logo antes de `build_command_chart` — não
dentro dela). Depois, dentro de `build_command_chart`, trocar:

```python
    roots = []
    for k, n in nodes.items():
        p = find_parent(k)
        if p and p in nodes:
            nodes[p]["children"].append(n)
        else:
            roots.append(n)

    if guarnicao is not None and "bbm" in nodes:
```

por:

```python
    roots = []
    for k, n in nodes.items():
        p = find_parent(k)
        if p and p in nodes:
            nodes[p]["children"].append(n)
        else:
            roots.append(n)

    # Órgãos sem filhos de órgão (folhas do commandChart) ganham sua estrutura
    # interna (desdobramentos do ro.json) como nós estruturais isInternal=True.
    # Roda ANTES da cadeia Cia BM/Pel BM abaixo, para não marcar "bbm" como folha
    # indevidamente (ele só fica "sem filhos" até a Guarnição ser anexada a seguir).
    for k, n in nodes.items():
        if n["children"]:
            continue
        for desd in (organs.get(k) or {}).get("desdobramentos") or []:
            label = truncate_desdobramento_label(desd)
            n["children"].append({
                "organKey": None, "sigla": "", "label": label,
                "structural": True, "isInternal": True,
                "chapterId": None, "children": [],
            })

    if guarnicao is not None and "bbm" in nodes:
```

- [ ] **Step 2: Regenerar `minuta_structure.json`**

Run:
```bash
cd "c:/Users/tiago/OneDrive/Documentos/Comparativo de legislações CBM" && python scripts/build_minuta_structure.py
```
Expected: conclui sem erro (sem traceback).

- [ ] **Step 3: Asserção — órgãos-folha ganharam nós `isInternal`, órgãos com filhos de órgão não**

Run:
```bash
cd "c:/Users/tiago/OneDrive/Documentos/Comparativo de legislações CBM" && python - <<'PY'
import json, sys

LEAF_EXPECTED = {"dp","deei","dpof","dsap","dlog","cint","ccs","cinf","condeg",
                 "depdec","corregedoria","cat","cibm","gbm","gab-cg","ag","assessorias"}
NO_INTERNAL_EXPECTED = {"dpo","doe","cot","crbm","bbm","bbs","bifea","boa"}

d = json.load(open("database/minuta_structure.json", encoding="utf-8"))
chart = d["commandChart"]

by_key = {}
def walk(n):
    k = n.get("organKey")
    if k:
        by_key[k] = n
    for c in n.get("children", []):
        walk(c)
walk(chart)

fail = []
for k in LEAF_EXPECTED:
    n = by_key.get(k)
    if not n:
        fail.append(f"{k}: nó não encontrado no commandChart")
        continue
    internal_kids = [c for c in n["children"] if c.get("isInternal")]
    if not internal_kids:
        fail.append(f"{k}: esperava filhos isInternal, encontrou {len(n['children'])} filhos (nenhum interno)")

for k in NO_INTERNAL_EXPECTED:
    n = by_key.get(k)
    if not n:
        fail.append(f"{k}: nó não encontrado no commandChart")
        continue
    internal_kids = [c for c in n["children"] if c.get("isInternal")]
    if internal_kids:
        fail.append(f"{k}: NÃO deveria ter filhos isInternal, encontrou {len(internal_kids)}")

if fail:
    print("FALHAS:")
    for f in fail:
        print(" -", f)
    sys.exit(1)
print("OK: todos os órgãos-folha esperados têm nós internos; DPO/DOE/COT/CRBM/BBM/BBS/BIFEA/BOA não têm.")
PY
echo "exit=$?"
```
Expected: `OK: ...` e `exit=0`.

- [ ] **Step 4: Conferir um label truncado com parênteses (regressão do bug encontrado no design)**

Run:
```bash
cd "c:/Users/tiago/OneDrive/Documentos/Comparativo de legislações CBM" && python -c "
import json
d = json.load(open('database/minuta_structure.json', encoding='utf-8'))
chart = d['commandChart']
def walk(n):
    if n.get('organKey') == 'dpof':
        return n
    for c in n.get('children', []):
        r = walk(c)
        if r:
            return r
    return None
dpof = walk(chart)
labels = [c['label'] for c in dpof['children']]
print(labels)
assert 'Diretor (Oficial da ativa do último Posto — QOEMBM)' in labels, labels
print('OK: parêntese com dash interno preservado intacto')
"
```
Expected: imprime a lista de labels de DPOF e `OK: parêntese com dash interno preservado intacto`.

- [ ] **Step 5: Commit**

```bash
cd "c:/Users/tiago/OneDrive/Documentos/Comparativo de legislações CBM" && git add scripts/build_minuta_structure.py database/minuta_structure.json && git commit -m "$(cat <<'EOF'
feat(minuta-diagramas): injeta estrutura interna nos órgãos-folha do commandChart

build_command_chart() agora anexa os desdobramentos do ro.json (Diretor,
Adjunto, Coordenadorias, Seções...) como nós isInternal=true nos órgãos
sem filhos de órgão (DP, DEEI, DPOF, DSAP, DLOG, CINT, CCS, CINF, CONDEG,
DEPDEC, CORREGEDORIA, CAT, CIBM, GBM, GAB-CG, AG, ASSESSORIAS). DPO/DOE/
COT/CRBM/BBM/BBS/BIFEA/BOA, que já têm filhos de órgão reais, ficam
inalterados. Labels truncados no separador " — "/" – " de topo, ignorando
dash dentro de parênteses (requisitos de cargo).

Co-Authored-By: Claude Sonnet 4.6 <noreply@anthropic.com>
EOF
)"
```
Expected: commit criado com os 2 arquivos.

---

### Task 2: Estilo visual dos nós internos no `MinutaOrgChart.jsx`

**Files:**
- Modify: `src/components/MinutaOrgChart.jsx:21`
- Modify: `src/index.css` (após a regra `.moc-label`, linha 2183)

**Interfaces:**
- Consumes: `node.isInternal` (produzido pela Task 1, presente em
  `database/minuta_structure.json` → `commandChart`).
- Produces: classe CSS `moc-box-internal` aplicada à `<div>`/`<button>` do nó —
  não consumida por nenhuma outra task.

- [ ] **Step 1: Adicionar a classe condicional em `MinutaOrgChart.jsx`**

Em `src/components/MinutaOrgChart.jsx:21`, trocar:

```jsx
  const cls = `moc-box${node.synthetic ? ' moc-box-root' : ''}${selected ? ' moc-box-sel' : ''}`
```

por:

```jsx
  const cls = `moc-box${node.synthetic ? ' moc-box-root' : ''}${node.isInternal ? ' moc-box-internal' : ''}${selected ? ' moc-box-sel' : ''}`
```

- [ ] **Step 2: Adicionar o estilo `.moc-box-internal` em `src/index.css`**

Em `src/index.css`, logo após a linha `.moc-label { font-size: 10.5px; color: var(--text-muted); }`
(linha 2183), adicionar:

```css
.moc-box-internal {
  border-style: dashed; background: #f4f6fa; cursor: default; min-width: 84px;
  padding: 6px 10px;
}
.moc-box-internal .moc-label { font-size: 9.5px; }
```

- [ ] **Step 3: Subir o dev server**

Run:
```bash
cd "c:/Users/tiago/OneDrive/Documentos/Comparativo de legislações CBM" && npm run dev -- --port 5173 --strictPort
```
Expected: Vite sobe em http://localhost:5173

- [ ] **Step 4: Conferir visualmente em http://localhost:5173/minuta-diagramas**

1. Abrir o organograma. Localizar "DP" (Diretoria de Pessoal) — antes uma caixa
   plana sem botão −/+. Confirmar que agora tem o botão "+".
2. Clicar para expandir: devem aparecer "Diretor", "Adjunto", "Seção
   Administrativa", "Coordenadoria de Gestão de Pessoal Ativo", "Coordenadoria de
   Gestão de Pessoal Inativo e Pensionistas", "Coordenadoria de Legislação,
   Controle e Análise de Processos" — em caixas com borda tracejada (estilo
   `.moc-box-internal`), visualmente mais leves que os órgãos normais.
3. Confirmar que **DPO** e **DOE** continuam mostrando só seus filhos de órgão
   (COT/CRBM para DPO; BBS/BIFEA/BOA para DOE) — sem nós internos adicionais
   misturados.
4. Clicar em "Expandir tudo" e depois usar a pré-visualização de impressão do
   navegador (ou `window.print()` via DevTools) — confirmar que os nós internos
   aparecem na visualização impressa sem quebrar o layout.

- [ ] **Step 5: Commit**

```bash
cd "c:/Users/tiago/OneDrive/Documentos/Comparativo de legislações CBM" && git add src/components/MinutaOrgChart.jsx src/index.css && git commit -m "$(cat <<'EOF'
feat(minuta-diagramas): estiliza nós de estrutura interna no organograma

Nós isInternal (desdobramentos injetados na Task 1) recebem a classe
moc-box-internal: borda tracejada, fundo neutro, fonte menor — visualmente
mais leves que os órgãos reais (que abrem painel ao clicar). O toggle
−/+ já funciona automaticamente para qualquer nó com children.

Co-Authored-By: Claude Sonnet 4.6 <noreply@anthropic.com>
EOF
)"
```
Expected: commit criado com os 2 arquivos.

---

## Self-Review (preenchido pelo autor do plano)

- **Cobertura da spec:** injeção em órgãos-folha (Task 1, Step 1) ✓ · ordem
  antes da cadeia BBM (Task 1, Step 1, comentário no código) ✓ · truncamento
  ciente de parênteses, validado contra dados reais (Task 1, Step 4) ✓ · não
  afeta DPO/DOE/COT/CRBM/BBM/BBS/BIFEA/BOA (Task 1, Step 3) ✓ · estilo visual
  distinto (Task 2, Step 2) ✓ · toggle automático (nenhuma mudança extra
  necessária — `MinutaOrgChart.jsx` já trata `hasKids` genericamente) ✓ ·
  impressão (Task 2, Step 4.4) ✓ · não tocar MindMap/`/comparar`/`ORGAN_ORDER`
  (nenhuma task toca esses arquivos) ✓.
- **Placeholders:** nenhum — código completo em cada step.
- **Consistência de tipos:** `isInternal` é o mesmo nome em
  `build_minuta_structure.py` (Task 1) e `MinutaOrgChart.jsx` (Task 2, lê
  `node.isInternal`). `truncate_desdobramento_label` definida e usada na mesma
  task.
