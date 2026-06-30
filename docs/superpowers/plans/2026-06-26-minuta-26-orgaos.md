# Expandir a minuta de RI para os 26 órgãos da LOB (Frente 1) — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Fazer `database/minuta_structure.json` (e por consequência `/minuta` e
`/minuta-diagramas`) cobrir os 26 órgãos de `database/organs_detail/ro.json` (toda a LOB do
CBMRO), em vez dos 11 órgãos operacionais atuais, com `cg` (Comando Geral) como raiz real da
árvore de comando.

**Architecture:** Tudo em `scripts/build_minuta_structure.py` (script Python sem framework de
teste — projeto não tem suíte Python; verificação é regenerar o JSON e inspecionar via
`python -c` e checagem visual) + um ajuste pontual em `src/components/MinutaOrgChart.jsx`
(preservar "raiz sempre expandida" quando a raiz deixa de ser sintética). Nenhuma mudança em
`organs_detail/ro.json`, `minuta_enrichment.py`, `minutaArticles.js` ou `build_minuta_comparison.py`
(Frente 2, fora de escopo).

**Tech Stack:** Python 3.14 (script standalone, `json`/`re`/`pathlib`), React 18 (componente
funcional), Node `--test` (suíte `src/lib/minutaArticles.test.js`, não tocada mas usada como
regressão).

**Spec:** `docs/superpowers/specs/2026-06-26-minuta-26-orgaos-design.md`

---

### Task 1: Expandir `ORGAN_ORDER` para os 26 órgãos

**Files:**
- Modify: `scripts/build_minuta_structure.py:1-6` (docstring), `scripts/build_minuta_structure.py:35-47` (`ORGAN_ORDER`)

- [ ] **Step 1: Atualizar o docstring do módulo** (linhas 1-6), trocando a menção a "estrutura
OPERACIONAL" por "estrutura completa da LOB":

```python
"""
build_minuta_structure.py — Portal CBM

Gera database/minuta_structure.json: minuta ARTICULADA e HIERÁRQUICA do Regimento
Interno do CBMRO — do Comando Geral (CG) à menor fração (Companhia/GBM), cobrindo
os 26 órgãos da LOB. Um capítulo por órgão; uma seção por função (cargo).

Fontes:
  - database/organs_detail/ro.json        (estrutura + competências RO verbatim)
  - scripts/minuta_enrichment.py          (competências curadas de outros CBMs, rotuladas)

Saída: database/minuta_structure.json
Rodar: python scripts/build_minuta_structure.py
"""
```

- [ ] **Step 2: Substituir `ORGAN_ORDER`** (linhas 35-47) pela lista completa de 26 entradas,
na ordem da taxonomia do Art. 5º da LOB (Direção → Assessoramento → Apoio → Execução →
Correição), preservando a ordem relativa das 11 já existentes:

```python
ORGAN_ORDER = [
    ("cg",           "DO COMANDO GERAL (CG)",                                          "O"),
    ("depdec",       "DA DIRETORIA ESTADUAL DE PROTEÇÃO E DEFESA CIVIL (DEPDEC)",       "A"),
    ("condeg",       "DO CONSELHO DELIBERATIVO DE ESTRATÉGIA E GESTÃO (CONDEG)",        "O"),
    ("dp",           "DA DIRETORIA DE PESSOAL (DP)",                                    "A"),
    ("deei",         "DA DIRETORIA DE EDUCAÇÃO, ENSINO E INSTRUÇÃO (DEEI)",             "A"),
    ("dpof",         "DA DIRETORIA DE PLANEJAMENTO, ORÇAMENTO E FINANÇAS (DPOF)",        "A"),
    ("dsap",         "DA DIRETORIA DE SAÚDE E ASSISTÊNCIA AO PESSOAL (DSAP)",            "A"),
    ("dlog",         "DA DIRETORIA DE LOGÍSTICA (DLOG)",                                "A"),
    ("dpo",          "DA DIRETORIA DE PLANEJAMENTO OPERACIONAL (DPO)",                  "A"),
    ("doe",          "DA DIRETORIA OPERACIONAL ESPECIALIZADA (DOE)",                    "A"),
    ("cot",          "DO COMANDO DE OPERAÇÕES TÉCNICAS (COT)",                          "O"),
    ("cint",         "DA COORDENADORIA DE INTELIGÊNCIA (CINT)",                         "A"),
    ("ccs",          "DA COORDENADORIA DE COMUNICAÇÃO SOCIAL (CCS)",                    "A"),
    ("cinf",         "DA COORDENADORIA DE INFORMÁTICA (CINF)",                          "A"),
    ("crbm",         "DOS COMANDOS REGIONAIS DE BOMBEIRO MILITAR (CRBM)",               "Os"),
    ("assessorias",  "DAS ASSESSORIAS",                                                 "As"),
    ("gab-cg",       "DO GABINETE DO COMANDANTE-GERAL",                                 "O"),
    ("ag",           "DA AJUDÂNCIA-GERAL (AG)",                                         "A"),
    ("bbm",          "DO BATALHÃO DE BOMBEIROS MILITAR (BBM)",                          "O"),
    ("cibm",         "DA COMPANHIA INDEPENDENTE DE BOMBEIROS MILITAR (CIBM)",           "A"),
    ("cat",          "DA COORDENADORIA DE ATIVIDADES TÉCNICAS (CAT)",                   "A"),
    ("bbs",          "DO BATALHÃO DE BUSCA E SALVAMENTO (BBS)",                         "O"),
    ("bifea",        "DO BATALHÃO DE INCÊNDIO FLORESTAL E EMERGÊNCIAS AMBIENTAIS (BIFEA)", "O"),
    ("boa",          "DO BATALHÃO DE OPERAÇÕES AÉREAS (BOA)",                           "O"),
    ("gbm",          "DO GRUPO DE BOMBEIROS MILITAR (GBM)",                             "O"),
    ("corregedoria", "DA CORREGEDORIA-GERAL",                                           "A"),
]
```

- [ ] **Step 3: Verificar que o script ainda roda sem exceção** (a hierarquia ainda não foi
corrigida — os 15 novos órgãos vão cair todos como raízes soltas da árvore sintética; isso é
esperado nesta etapa, será corrigido no Task 2):

Run: `python scripts/build_minuta_structure.py`
Expected: termina sem traceback, imprime `26 órgãos` na última linha (ex.: `27 capítulos · 26
órgãos · N seções de função`).

- [ ] **Step 4: Commit**

```bash
git add scripts/build_minuta_structure.py
git commit -m "feat(minuta): expande ORGAN_ORDER para os 26 orgaos da LOB"
```

---

### Task 2: Resolver hierarquia de cargos com `ROLE_TO_ORGAN`

**Files:**
- Modify: `scripts/build_minuta_structure.py:312-326` (`find_parent`, dentro de `build_command_chart`)

- [ ] **Step 1: Adicionar o mapa `ROLE_TO_ORGAN`** imediatamente antes de
`def build_command_chart(...)` (atualmente linha 290):

```python
# subordinadoA de alguns órgãos referencia um CARGO interno de `cg` (Comandante-Geral,
# Subcomandante-Geral, Chefe do Estado-Maior Geral), não a sigla de um órgão do conjunto.
# Mapa de fallback: texto normalizado do cargo -> organ_key real que o "contém".
ROLE_TO_ORGAN = {
    "comandante-geral": "cg",
    "subcomandante-geral": "cg",
    "chefe do estado-maior geral": "cg",
}
```

- [ ] **Step 2: Alterar `find_parent`** para tentar `ROLE_TO_ORGAN` como fallback quando o
casamento por sigla não encontra nada. Trecho atual (linhas 312-326):

```python
    def find_parent(k):
        if k in COMMAND_PARENT_OVERRIDE:
            return COMMAND_PARENT_OVERRIDE[k]
        sub = (organs.get(k) or {}).get("subordinadoA", "") or ""
        matches = [
            other_k for other_k, sig in siglas.items()
            if other_k != k and re.search(rf"\b{re.escape(sig)}\b", sub)
        ]
        # subordinadoA deve referenciar no máximo uma sigla do conjunto; mais de uma
        # significaria roteamento ambíguo (texto do ro.json mudou) — falha alto.
        if len(matches) > 1:
            raise ValueError(
                f"subordinadoA de '{k}' casa múltiplas siglas {matches}: {sub!r}"
            )
        return matches[0] if matches else None  # None = raiz
```

Substituir por:

```python
    def find_parent(k):
        if k in COMMAND_PARENT_OVERRIDE:
            return COMMAND_PARENT_OVERRIDE[k]
        sub = (organs.get(k) or {}).get("subordinadoA", "") or ""
        matches = [
            other_k for other_k, sig in siglas.items()
            if other_k != k and re.search(rf"\b{re.escape(sig)}\b", sub)
        ]
        # subordinadoA deve referenciar no máximo uma sigla do conjunto; mais de uma
        # significaria roteamento ambíguo (texto do ro.json mudou) — falha alto.
        if len(matches) > 1:
            raise ValueError(
                f"subordinadoA de '{k}' casa múltiplas siglas {matches}: {sub!r}"
            )
        if matches:
            return matches[0]
        # Sem sigla: subordinadoA pode referenciar um CARGO interno de outro órgão
        # (ex.: "Chefe do Estado-Maior Geral", cargo de `cg`) em vez de um órgão próprio.
        sub_norm = normalize(sub)
        for role, target in ROLE_TO_ORGAN.items():
            if sub_norm.startswith(role) and target in nodes and target != k:
                return target
        return None  # raiz
```

- [ ] **Step 3: Verificar via script ad hoc** que todos os 15 novos órgãos (exceto `cg`) agora
têm pai resolvido, e que `cg` é a única raiz remanescente:

Run:
```bash
python -c "
import json, sys
sys.path.insert(0, 'scripts')
from build_minuta_structure import build_command_chart, _min_organ_chapters
organs = json.loads(open('database/organs_detail/ro.json', encoding='utf-8').read())['organs']
chart = build_command_chart(organs, _min_organ_chapters(organs))
print('root organKey:', chart.get('organKey'), '| synthetic:', chart.get('synthetic'))
"
```
Expected: sem traceback. `synthetic` ainda aparece `True` nesta etapa (o unwrap de raiz única é
o Task 3) — o que importa aqui é que NENHUMA exceção `ValueError` é lançada (confirma que
nenhum `subordinadoA` casa siglas ambíguas com o conjunto de 26).

- [ ] **Step 4: Commit**

```bash
git add scripts/build_minuta_structure.py
git commit -m "fix(minuta): resolve subordinadoA por cargo (ROLE_TO_ORGAN) alem de sigla"
```

---

### Task 3: `cg` como raiz real da árvore de comando

**Files:**
- Modify: `scripts/build_minuta_structure.py:290-351` (`build_command_chart`, docstring + `return`)
- Modify: `scripts/build_minuta_structure.py:372-392` (`command_order`, docstring + loop final)

- [ ] **Step 1: Atualizar o docstring de `build_command_chart`** (linhas 290-296):

```python
def build_command_chart(organs, chapters):
    """Árvore dos órgãos (capítulos kind='organ') pela subordinação do ro.json.

    Pai = órgão do conjunto cuja SIGLA aparece em subordinadoA; se nenhuma sigla
    casar, tenta ROLE_TO_ORGAN (subordinadoA referencia um cargo interno de outro
    órgão); senão, raiz. A Guarnição (menor fração) pendura na cadeia
    Cia BM → Pel BM dentro do BBM.
    Retorna `cg` como raiz real (tem chapterId, é clicável) quando há exatamente
    uma raiz; cai para um wrapper sintético só se restarem múltiplas raízes
    desconectadas (não esperado com os 26 órgãos atuais — sinal de dado inesperado).
    """
```

- [ ] **Step 2: Trocar o `return` final** (linha 351) por uma decisão de raiz única vs.
múltipla:

```python
    if len(roots) == 1:
        return roots[0]
    return {"label": "Subcomandante-Geral", "synthetic": True, "children": roots}
```

- [ ] **Step 3: Atualizar o docstring de `command_order`** (linhas 372-377) e o loop final
(linhas 390-391). Trecho atual:

```python
def command_order(organs):
    """Ordem hierárquica (DFS) e profundidade dos órgãos pela cadeia de comando.

    Retorna list[(organKey, depth)] — depth conta só níveis de ÓRGÃO (nós
    estruturais Cia/Pel não incrementam). É a mesma árvore do organograma,
    então a lista de órgãos da minuta espelha o organograma montado.
    """
    chart = build_command_chart(organs, _min_organ_chapters(organs))
    out = []

    def walk(node, depth):
        k = node.get("organKey")
        if k:
            out.append((k, depth))
        nd = depth + 1 if k else depth
        for c in node.get("children", []):
            walk(c, nd)

    for c in chart.get("children", []):
        walk(c, 0)
    return out
```

Substituir por:

```python
def command_order(organs):
    """Ordem hierárquica (DFS) e profundidade dos órgãos pela cadeia de comando.

    Retorna list[(organKey, depth)] — depth conta só níveis de ÓRGÃO (nós
    estruturais Cia/Pel não incrementam). É a mesma árvore do organograma,
    então a lista de órgãos da minuta espelha o organograma montado.
    """
    chart = build_command_chart(organs, _min_organ_chapters(organs))
    out = []

    def walk(node, depth):
        k = node.get("organKey")
        if k:
            out.append((k, depth))
        nd = depth + 1 if k else depth
        for c in node.get("children", []):
            walk(c, nd)

    walk(chart, 0)
    return out
```

(`walk(chart, 0)` funciona nos dois casos: raiz sintética sem `organKey` não emite nada e desce
para os filhos na mesma profundidade 0 — igual ao loop antigo; raiz real `cg` emite `("cg", 0)`
e desce para os filhos em profundidade 1.)

- [ ] **Step 4: Verificar raiz única e ordem completa**

Run:
```bash
python -c "
import json, sys
sys.path.insert(0, 'scripts')
from build_minuta_structure import build_command_chart, command_order, _min_organ_chapters, ORGAN_ORDER
organs = json.loads(open('database/organs_detail/ro.json', encoding='utf-8').read())['organs']
chart = build_command_chart(organs, _min_organ_chapters(organs))
assert chart.get('organKey') == 'cg', chart.get('organKey')
assert not chart.get('synthetic'), 'raiz nao deveria ser sintetica'
order = command_order(organs)
keys = [k for k, _d in order]
assert keys[0] == 'cg', keys[:3]
assert set(keys) == {k for k, _t, _a in ORGAN_ORDER} | {'guarnicao'}, sorted(set(keys))
print('OK: raiz =', chart['organKey'], '| ordem[:5] =', order[:5])
"
```
Expected: imprime `OK: raiz = cg | ordem[:5] = [('cg', 0), ...]` sem `AssertionError`.

- [ ] **Step 5: Commit**

```bash
git add scripts/build_minuta_structure.py
git commit -m "feat(minuta): cg passa a ser raiz real da arvore de comando"
```

---

### Task 4: Capítulo "Da Estrutura Organizacional" — taxonomia completa (Art. 5º-10º)

**Files:**
- Modify: `scripts/build_minuta_structure.py:190-224` (`build_estrutura_chapter`)

- [ ] **Step 1: Substituir `build_estrutura_chapter`** (linhas 190-224) por uma versão que
agrupa genericamente por `category` (sem caso especial por órgão), cobrindo os 5 grupos do
Art. 5º:

```python
CATEGORY_LABELS = [
    ("Direção Geral",     "de Direção Geral"),
    ("Direção Colegiada",  "de Direção Colegiada"),
    ("Direção Setorial",   "de Direção Setorial"),
    ("Direção Regional",   "de Direção Regional"),
]
APOIO_LABELS = [
    ("Apoio ao Comando-Geral",    "ao Comando-Geral"),
    ("Apoio ao Subcomando-Geral", "ao Subcomando-Geral"),
]


def build_estrutura_chapter(organs):
    art_by_key = {k: art for (k, _t, art) in ORGAN_ORDER}
    cat_of = {k: (organs.get(k) or {}).get("category", "") for (k, _t, _a) in ORGAN_ORDER}

    def items_for(labels):
        out = []
        for cat, label in labels:
            keys = [k for (k, _t, _a) in ORGAN_ORDER if cat_of[k] == cat]
            if keys:
                out.append({"text": f"{label}: {_join_orgaos(keys, organs, art_by_key)}", "source": "ro"})
        return out

    direcao_items = items_for(CATEGORY_LABELS)
    apoio_items = items_for(APOIO_LABELS)
    assessoramento_items = items_for([("Assessoramento", "de Assessoramento")])
    correicao_items = items_for([("Correição", "de Correição")])

    execucao_items = []
    for area_key, area_label in AREA_LABELS:
        keys = [k for (k, _t, _a) in ORGAN_ORDER if AREA_BY_ORGAN.get(k) == area_key]
        if not keys:
            continue
        execucao_items.append({"text": f"{area_label}: {_join_orgaos(keys, organs, art_by_key)}", "source": "ro"})

    def make_article(article_id, caput, items):
        return {
            "id": article_id, "kind": "incisos", "editId": f"estrutura/{article_id}",
            "caput": caput, "items": items, "proposedText": proposed_text(items),
        }

    articles = [make_article("direcao", "São Órgãos de Direção:", direcao_items)]
    if assessoramento_items:
        articles.append(make_article("assessoramento", "É Órgão de Assessoramento:", assessoramento_items))
    if apoio_items:
        articles.append(make_article("apoio", "São Órgãos de Apoio:", apoio_items))
    articles.append(make_article(
        "execucao", "Os Órgãos de Execução classificam-se, quanto à área de atuação, em:", execucao_items
    ))
    if correicao_items:
        articles.append(make_article("correicao", "É Órgão de Correição:", correicao_items))

    return {
        "id": "estrutura", "kind": "articles", "chapterTitle": "DA ESTRUTURA ORGANIZACIONAL",
        "editId": "estrutura",
        "articles": articles,
    }
```

- [ ] **Step 2: Verificar os 5 grupos presentes**

Run:
```bash
python -c "
import json, sys
sys.path.insert(0, 'scripts')
from build_minuta_structure import build_estrutura_chapter
organs = json.loads(open('database/organs_detail/ro.json', encoding='utf-8').read())['organs']
ch = build_estrutura_chapter(organs)
ids = [a['id'] for a in ch['articles']]
assert ids == ['direcao', 'assessoramento', 'apoio', 'execucao', 'correicao'], ids
for a in ch['articles']:
    print(a['id'], '->', len(a['items']), 'itens')
"
```
Expected: imprime as 5 linhas (`direcao -> 4 itens`, `assessoramento -> 1 itens`,
`apoio -> 2 itens`, `execucao -> 4 itens`, `correicao -> 1 itens`) sem `AssertionError`.

- [ ] **Step 3: Commit**

```bash
git add scripts/build_minuta_structure.py
git commit -m "feat(minuta): estrutura organizacional cobre os 5 grupos do Art. 5 da LOB"
```

---

### Task 5: Atualizar título e disposições preliminares

**Files:**
- Modify: `scripts/build_minuta_structure.py:31` (`TITLE`)
- Modify: `scripts/build_minuta_structure.py:227-238` (`build_preliminares_chapter`)

- [ ] **Step 1: Trocar `TITLE`** (linha 31):

```python
TITLE = "DO REGIMENTO INTERNO DO CORPO DE BOMBEIROS MILITAR DO ESTADO DE RONDÔNIA (CBMRO)"
```

- [ ] **Step 2: Reescrever `build_preliminares_chapter`** (linhas 227-238):

```python
def build_preliminares_chapter():
    txt = (
        "Este Regimento Interno disciplina a organização, as competências e o funcionamento "
        "da estrutura do Corpo de Bombeiros Militar do Estado de Rondônia (CBMRO), do Comando "
        "Geral às frações de execução.\n"
        "A estrutura do CBMRO observa a Lei de Organização Básica do CBMRO, que define a "
        "subordinação entre seus órgãos."
    )
    return {
        "id": "preliminares", "kind": "prose", "chapterTitle": "DAS DISPOSIÇÕES PRELIMINARES",
        "editId": "preliminares", "proposedText": txt,
    }
```

- [ ] **Step 3: Commit**

```bash
git add scripts/build_minuta_structure.py
git commit -m "docs(minuta): titulo e preliminares descrevem a LOB inteira, nao so a operacional"
```

---

### Task 6: Preservar "raiz sempre expandida" com `cg` como raiz real

**Files:**
- Modify: `src/components/MinutaOrgChart.jsx`

O componente hoje só auto-expande a raiz quando `node.synthetic === true` (linha 18). Como
`cg` passa a ser uma raiz REAL (não sintética, com `chapterId` próprio e clicável), sem este
ajuste o organograma nasceria com a raiz recolhida, regredindo a garantia documentada no
cabeçalho do arquivo ("a raiz fica sempre expandida").

- [ ] **Step 1: Adicionar a prop `isRoot`** em `ChartNode` (linha 13) e usá-la no cálculo do
estado inicial (linha 18):

Trecho atual:
```jsx
function ChartNode({ node, onSelect, selectedId, defaultExpanded }) {
  const kids = node.children || []
  const hasKids = kids.length > 0
  const clickable = !node.synthetic && node.chapterId
  const selected = clickable && node.chapterId === selectedId
  const [open, setOpen] = useState(node.synthetic ? true : defaultExpanded)
```

Substituir por:
```jsx
function ChartNode({ node, onSelect, selectedId, defaultExpanded, isRoot = false }) {
  const kids = node.children || []
  const hasKids = kids.length > 0
  const clickable = !node.synthetic && node.chapterId
  const selected = clickable && node.chapterId === selectedId
  const [open, setOpen] = useState(isRoot || node.synthetic ? true : defaultExpanded)
```

- [ ] **Step 2: Passar `isRoot={true}` apenas na chamada de topo** em `MinutaOrgChart` (linhas
70-83); as chamadas recursivas dentro de `ChartNode` (linhas 55-63) NÃO recebem `isRoot`
(mantém o padrão `false`, raiz real só existe uma vez, no topo):

Trecho atual:
```jsx
export default function MinutaOrgChart({ chart, onSelect, selectedId, defaultExpanded = false }) {
  if (!chart) return null
  return (
    <div className="moc-tree">
      <ul>
        <ChartNode
          node={chart}
          onSelect={onSelect}
          selectedId={selectedId}
          defaultExpanded={defaultExpanded}
        />
      </ul>
    </div>
  )
}
```

Substituir por:
```jsx
export default function MinutaOrgChart({ chart, onSelect, selectedId, defaultExpanded = false }) {
  if (!chart) return null
  return (
    <div className="moc-tree">
      <ul>
        <ChartNode
          node={chart}
          onSelect={onSelect}
          selectedId={selectedId}
          defaultExpanded={defaultExpanded}
          isRoot
        />
      </ul>
    </div>
  )
}
```

Não aplicar a classe `.moc-box-root` (estilo vermelho "não clicável") a `cg`: essa classe
continua condicionada só a `node.synthetic` (linha 19, inalterada) — `cg` é clicável (tem
`chapterId`) e deve manter a aparência normal de caixa clicável, não a aparência de raiz
sintética de fallback.

- [ ] **Step 3: Atualizar o comentário de cabeçalho do arquivo** (linhas 1-9), que hoje só
descreve a raiz sintética como sempre expandida:

Trecho atual (linhas 6-9):
```jsx
// Árvore dinâmica: nós com filhos têm um botão −/+ (moc-toggle) que expande/recolhe
// a subárvore; o clique na CAIXA continua abrindo o painel de detalhe. A raiz fica
// sempre expandida; os demais nós iniciam conforme `defaultExpanded` (recolhidos por
// padrão → só DPO e DOE visíveis). Trocar `defaultExpanded` + remontar (via `key` na
// árvore) reaplica "expandir/recolher tudo".
```

Substituir por:
```jsx
// Árvore dinâmica: nós com filhos têm um botão −/+ (moc-toggle) que expande/recolhe
// a subárvore; o clique na CAIXA continua abrindo o painel de detalhe. A raiz (CG, ou
// o wrapper sintético no caso raro de múltiplas raízes) fica sempre expandida via a
// prop `isRoot`; os demais nós iniciam conforme `defaultExpanded` (recolhidos por
// padrão). Trocar `defaultExpanded` + remontar (via `key` na árvore) reaplica
// "expandir/recolher tudo".
```

- [ ] **Step 4: Commit**

```bash
git add src/components/MinutaOrgChart.jsx
git commit -m "fix(minuta-diagramas): raiz real (cg) comeca expandida, como a sintetica antes"
```

---

### Task 7: Regenerar dados e verificação final

**Files:**
- Modify (gerado, não editar à mão): `database/minuta_structure.json`

- [ ] **Step 1: Regenerar o JSON**

Run: `python scripts/build_minuta_structure.py`
Expected (stdout termina com algo como):
```
Gerado: .../database/minuta_structure.json
  28 capítulos · 27 órgãos · N seções de função
```
(27 = 26 órgãos da LOB + Guarnição; 28 = 27 + preliminares + estrutura + finais.)

- [ ] **Step 2: Verificação estrutural completa via script**

Run:
```bash
python -c "
import json
data = json.loads(open('database/minuta_structure.json', encoding='utf-8').read())
organ_chapters = [c for c in data['chapters'] if c['kind'] == 'organ']
assert len(organ_chapters) == 27, len(organ_chapters)  # 26 LOB + guarnicao
keys = {c['organKey'] for c in organ_chapters}
assert 'cg' in keys and 'guarnicao' in keys, keys
chart = data['commandChart']
assert chart.get('organKey') == 'cg', chart.get('organKey')
assert not chart.get('synthetic'), 'raiz nao deveria ser sintetica'
print('OK:', len(organ_chapters), 'capitulos de orgao; raiz =', chart['organKey'])
"
```
Expected: `OK: 27 capitulos de orgao; raiz = cg` sem `AssertionError` nem traceback.

- [ ] **Step 3: Rodar a suíte JS de regressão**

Run: `node --test src/lib/minutaArticles.test.js`
Expected: todos os testes existentes continuam passando (a suíte usa fixtures próprias, não lê
`minuta_structure.json` — não deve haver `not ok` na saída).

- [ ] **Step 4: Verificação visual manual** (não automatizável — registrar resultado no PR/commit)

1. `npm run dev` (porta 5173).
2. Abrir `http://localhost:5173/minuta-diagramas`: confirmar que o organograma mostra `CG` no
   topo, já expandido, com os 25 demais órgãos pendurados na árvore (a maioria sob `CG`, exceto
   `DPO`/`DOE` que também ficam sob `CG`). Expandir/recolher alguns nós para confirmar que o
   botão −/+ funciona na raiz real. Abrir o mapa mental e confirmar que aparecem ~28 cartões de
   capítulo. Testar "Expandir tudo" / "Recolher tudo" e a exportação por `window.print()`
   (Paisagem, sem cortar conteúdo).
3. Abrir `http://localhost:5173/minuta`: confirmar que o sumário lateral lista os 26 capítulos
   de órgão + Guarnição na ordem correta (CG primeiro). Abrir 2-3 capítulos novos (ex.:
   "Da Diretoria de Pessoal") e confirmar que aparecem Finalidade/Competência/cargos com texto.
   Abrir o capítulo "Da Estrutura Organizacional" e confirmar os 5 incisos (Direção,
   Assessoramento, Apoio, Execução, Correição).

- [ ] **Step 5: Commit final** (só o JSON regenerado; se os Steps 4 não revelarem bugs)

```bash
git add database/minuta_structure.json
git commit -m "data(minuta): regenera minuta_structure.json com os 26 orgaos da LOB"
```

---

## Self-Review (executado antes de entregar o plano)

**Cobertura do spec:**
- Lista de 26 órgãos / `ORGAN_ORDER` → Task 1.
- Resolução de hierarquia (`ROLE_TO_ORGAN`) → Task 2.
- `cg` como raiz real (efeito colateral em `dpo`/`doe`) → Task 3 (a troca de `find_parent` no
  Task 2 já produz o efeito colateral; Task 3 só ajusta o formato do retorno/ordem).
- Capítulo "Da Estrutura Organizacional", 5 grupos → Task 4.
- Textos introdutórios (`TITLE`, preliminares) → Task 5.
- "O que não muda" (ro.json, GUARNICAO_CHAPTER, BBM_FRACTION_CHAIN, enrichment, comparador) →
  nenhuma task toca esses arquivos; confirmado.
- Testes/verificação do spec (regenerar, checar 26 capítulos + raiz única, visual, `node --test`,
  PDF) → Task 7.
- Dois achados arquiteturais que NÃO estavam no spec original (raiz real quebra
  "sempre expandida" no frontend; `command_order` precisava do `walk(chart, 0)`) → cobertos nos
  Tasks 3 e 6, com a justificativa técnica explicada inline (são consequências mecânicas da
  raiz deixar de ser sintética, não escolhas de design novas).

**Placeholders:** nenhum "TBD"/"similar ao Task N" — todo código é completo e específico do
arquivo/linha.

**Consistência de nomes:** `ROLE_TO_ORGAN`, `CATEGORY_LABELS`, `APOIO_LABELS`, `find_parent`,
`build_command_chart`, `command_order`, `build_estrutura_chapter`, `isRoot` — usados de forma
idêntica em todas as tasks que os referenciam.
