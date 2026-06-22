# Taxonomia da Estrutura (Art. 3) + CAT como órgão próprio — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Reestruturar o Art. 3 da minuta do RI na taxonomia da LOB (Direção × Execução por área de atuação) e promover a CAT a órgão próprio, refletindo na minuta (`/minuta`), no organograma do estado e no comparador (`/comparar`).

**Architecture:** A minuta é gerada offline por scripts Python a partir de `database/organs_detail/ro.json` (escrito à mão) e consumida pelo front (React) via JSON. Introduz-se um quarto `kind` de capítulo (`articles`) para o Art. 3 gerar dois artigos sob um único título; adiciona-se o órgão `cat` ao `ro.json`; reordena-se `ORGAN_ORDER`; o comparador (que importa `ORGAN_ORDER`) ganha a coluna CAT.

**Tech Stack:** Python 3 (pypdf não é tocado aqui), React 18 + Vite, testes `node --test` (JS) e asserts (Python). Ambiente Windows; shell Git Bash disponível.

## Global Constraints

- **Contagem:** após esta mudança são **11 órgãos da LOB + Guarnição = 12** capítulos de órgão na minuta e 12 colunas no comparador. Toda menção a "10 órgãos da LOB" / "11 órgãos (10 da LOB + guarnição)" deve passar a refletir 11/12.
- **`ro.json` e `ac.json`** são os ÚNICOS detail JSON escritos à mão — podem ser editados diretamente. Os demais JSON gerados (`minuta_structure.json`, `comparativo_minuta.json`, `states_data.json`, `comparativo_dpo_cot.json`, demais `organs_detail/*.json`) NUNCA são editados à mão; só regenerados pelos scripts.
- **Coluna RO no comparador é pura do `ro.json`** — não derivar de enriquecimento.
- **Ordem dos órgãos** (em `ORGAN_ORDER`, fonte única para minuta e comparador):
  `dpo, doe, cot` (Direção Setorial) · `crbm` (Direção Regional) · `bbm, cibm, cat` (Ordinária) · `bbs, bifea` (Esp. Terrestre) · `boa` (Esp. Aérea) · `gbm` (Conveniada).
- **CAT:** classificada como Execução de Atuação Ordinária, mas `subordinadoA` = "Comando de Operações Técnicas (COT)" (LOB Art. 42).
- **Servidor de dev:** porta fixa 5173 (`npm run dev -- --port 5173 --strictPort`).
- Não há linter; o "test suite" JS é `node --test src/lib/minutaArticles.test.js`.

## File Structure

- `src/lib/minutaArticles.js` — numeração/articulação pura. Ganha suporte ao `kind: "articles"`.
- `src/lib/minutaArticles.test.js` — testes `node --test`. Ganha caso do `kind: "articles"`.
- `database/organs_detail/ro.json` — estrutura RO (à mão). Ganha o órgão `cat`; perde o cargo CAT de dentro do `cot`.
- `scripts/build_minuta_structure.py` — gera `minuta_structure.json`. Reordena `ORGAN_ORDER`, adiciona `AREA_BY_ORGAN`/`AREA_LABELS`/`_join_orgaos`, reescreve `build_estrutura_chapter` para `kind: "articles"`.
- `src/pages/MinutaWizard.jsx` — wizard. `indexLeaves`/`indexSources` passam a tratar `kind: "articles"`.
- `scripts/minuta_comparison_lib.py` — helpers do comparador. Ganha entrada `cat` em `AUTO_MATCH_KEYWORDS`.
- `scripts/test_minuta_comparison_lib.py` — teste do lib. Ganha caso do auto-match `cat`.
- `scripts/build_minuta_comparison.py` — comentários/contagem.
- `CLAUDE.md` — contagens e lista de órgãos.

---

### Task 1: `buildArticles` suporta `kind: "articles"`

**Files:**
- Modify: `src/lib/minutaArticles.js:108-112`
- Test: `src/lib/minutaArticles.test.js` (append)

- [ ] **Step 1: Escrever o teste que falha**

Anexar ao final de `src/lib/minutaArticles.test.js`:

```js
test('buildArticles: capítulo kind "articles" gera um artigo por folha sob um único título de capítulo', () => {
  const structure = {
    chapters: [
      {
        id: 'estrutura', kind: 'articles', chapterTitle: 'DA ESTRUTURA ORGANIZACIONAL',
        editId: 'estrutura',
        articles: [
          { id: 'direcao', kind: 'incisos', editId: 'estrutura/direcao',
            caput: 'São Órgãos de Direção Operacional:',
            items: [
              { text: 'de Direção Setorial: a DPO, a DOE e o COT', source: 'ro' },
              { text: 'de Direção Regional: o CRBM', source: 'ro' },
            ] },
          { id: 'execucao', kind: 'incisos', editId: 'estrutura/execucao',
            caput: 'Os Órgãos de Execução classificam-se em:',
            items: [{ text: 'Atuação Operacional Ordinária: o BBM', source: 'ro' }] },
        ],
      },
    ],
  }
  const arts = buildArticles(structure, {})
  assert.equal(arts.length, 2)
  assert.equal(arts[0].number, 1)
  assert.equal(arts[0].chapterNumber, 1)
  assert.equal(arts[0].chapterTitle, 'DA ESTRUTURA ORGANIZACIONAL')
  assert.equal(arts[0].editId, 'estrutura/direcao')
  assert.equal(arts[0].sectionNumber, null)
  assert.equal(arts[1].number, 2)
  assert.equal(arts[1].chapterTitle, null)
  assert.equal(arts[1].editId, 'estrutura/execucao')
})
```

- [ ] **Step 2: Rodar o teste e ver falhar**

Run: `node --test src/lib/minutaArticles.test.js`
Expected: FAIL — o capítulo `articles` cai no ramo `else` (`emitLeaf(chapter, false)`), e como `chapter.kind` não é `prose`/`incisos`, nenhum artigo é emitido → `arts.length` 0, não 2.

- [ ] **Step 3: Implementar o suporte ao `kind: "articles"`**

Em `src/lib/minutaArticles.js`, substituir o bloco final do loop de capítulos:

```js
    if (chapter.kind === 'organ') {
      for (const section of chapter.sections) emitLeaf(section, true)
    } else {
      emitLeaf(chapter, false)
    }
```

por:

```js
    if (chapter.kind === 'organ') {
      for (const section of chapter.sections) emitLeaf(section, true)
    } else if (chapter.kind === 'articles') {
      for (const leaf of chapter.articles) emitLeaf(leaf, false)
    } else {
      emitLeaf(chapter, false)
    }
```

- [ ] **Step 4: Rodar o teste e ver passar (suíte inteira)**

Run: `node --test src/lib/minutaArticles.test.js`
Expected: PASS — todos os casos (os 13 existentes + o novo) passam.

- [ ] **Step 5: Commit**

```bash
git add src/lib/minutaArticles.js src/lib/minutaArticles.test.js
git commit -m "feat(minuta): buildArticles suporta capítulo kind 'articles' (multi-artigo)"
```

---

### Task 2: Adicionar órgão `cat` ao `ro.json` e remover o cargo CAT do `cot`

**Files:**
- Modify: `database/organs_detail/ro.json` (órgão `cot` ~486-537; inserir `cat` após `cot`)

- [ ] **Step 1: Remover o cargo "Coordenador de Atividades Técnicas (CAT)" de `cot.cargos`**

No órgão `cot`, localizar o array `cargos`. Remover o objeto do cargo CAT (o 3º), de modo que o `Adjunto do COT` seja seguido diretamente pelo `Coordenador de Projetos de Arquitetura e Engenharia`. Substituir:

```json
        {
          "cargo": "Adjunto do COT",
          "subordinadoA": "Comandante do COT",
          "desdobramentos": ["Seção Administrativa", "Seção de Estudos Técnicos", "Seção de Planejamento, Fiscalização e Suporte Técnico"],
          "atribuicoes": ["Substituir o Comandante do COT em seus impedimentos.", "Auxiliar no planejamento e controle das atividades técnicas."]
        },
        {
          "cargo": "Coordenador de Atividades Técnicas (CAT)",
          "subordinadoA": "Comandante do COT",
          "requisito": "Oficial Superior da ativa — QOEMBM ou QCOBM. (Art. 25 §2º)",
          "desdobramentos": ["Adjunto", "Seção Administrativa", "Seção de Análise de Projetos", "Seção de Investigação e Prevenção de Incêndio", "Gerência de Atividades Técnicas (Seção de Vistoria, Seção de Hidrantes)"],
          "atribuicoes": ["Estudar, analisar, exigir e fiscalizar as atividades pertinentes à segurança contra incêndio e pânico.", "Proceder a análise de projetos, realizar investigação de incêndios, testes de materiais, vistorias e emitir pareceres técnicos.", "Com autoridade para notificar, multar, embargar e interditar na forma da lei específica. Subordinado ao Comando de Operações Técnicas (COT)."]
        },
        {
          "cargo": "Coordenador de Projetos de Arquitetura e Engenharia",
```

por:

```json
        {
          "cargo": "Adjunto do COT",
          "subordinadoA": "Comandante do COT",
          "desdobramentos": ["Seção Administrativa", "Seção de Estudos Técnicos", "Seção de Planejamento, Fiscalização e Suporte Técnico"],
          "atribuicoes": ["Substituir o Comandante do COT em seus impedimentos.", "Auxiliar no planejamento e controle das atividades técnicas."]
        },
        {
          "cargo": "Coordenador de Projetos de Arquitetura e Engenharia",
```

> Manter intacta a linha de `desdobramentos` do `cot` que cita "Coordenadorias de Atividades Técnicas (CATs) — Art. 42: …" (passa a ser cross-reference).

- [ ] **Step 2: Inserir o órgão `cat` logo após o órgão `cot`**

Localizar o fechamento do órgão `cot` (a linha `},` imediatamente antes de `"cint": {`) e inserir o bloco abaixo entre eles:

```json
    "cat": {
      "id": "cat",
      "name": "Coordenadoria de Atividades Técnicas",
      "abbreviation": "CAT",
      "category": "Execução",
      "subordinadoA": "Comando de Operações Técnicas (COT)",
      "legalRef": "Art. 42",
      "baseLegal": "Minuta de Projeto de Lei n.º 0059262482 (abril de 2025) — Organização Básica do CBMRO (em tramitação)",
      "artigosDeOrigem": ["Art. 42 (CAT)"],
      "atribuicoes": [
        "Órgão de execução de atuação operacional ordinária, subordinado ao Comando de Operações Técnicas (COT), incumbido de estudar, analisar, exigir e fiscalizar as atividades pertinentes à segurança contra incêndio e pânico.",
        "Proceder a análise de projetos, realizar investigação de incêndios, testes de materiais, vistorias e emitir pareceres técnicos, com autoridade para notificar, multar, embargar e interditar na forma da lei específica."
      ],
      "desdobramentos": [
        "Coordenador",
        "Adjunto",
        "Seção Administrativa",
        "Seção de Análise de Projetos",
        "Seção de Investigação e Prevenção de Incêndio",
        "Gerência de Atividades Técnicas — Seção Administrativa, Seção de Vistoria, Seção de Hidrantes"
      ],
      "cargos": [
        {
          "cargo": "Coordenador de Atividades Técnicas (CAT)",
          "subordinadoA": "Comandante do COT",
          "requisito": "Oficial Superior da ativa — QOEMBM ou QCOBM. (Art. 25 §2º)",
          "desdobramentos": ["Adjunto", "Seção Administrativa", "Seção de Análise de Projetos", "Seção de Investigação e Prevenção de Incêndio", "Gerência de Atividades Técnicas (Seção de Vistoria, Seção de Hidrantes)"],
          "atribuicoes": ["Estudar, analisar, exigir e fiscalizar as atividades pertinentes à segurança contra incêndio e pânico.", "Proceder a análise de projetos, realizar investigação de incêndios, testes de materiais, vistorias e emitir pareceres técnicos.", "Com autoridade para notificar, multar, embargar e interditar na forma da lei específica. Subordinado ao Comando de Operações Técnicas (COT)."]
        }
      ]
    },
```

- [ ] **Step 3: Validar o JSON e a edição**

Run:
```bash
python -c "import json; d=json.load(open('database/organs_detail/ro.json',encoding='utf-8')); o=d['organs']; assert 'cat' in o; assert o['cat']['category']=='Execução'; assert o['cat']['subordinadoA'].startswith('Comando de Operações Técnicas'); assert len(o['cat']['cargos'])==1; assert all(c['cargo']!='Coordenador de Atividades Técnicas (CAT)' for c in o['cot']['cargos']); assert any('Coordenadorias de Atividades Técnicas' in d for d in o['cot']['desdobramentos']); print('OK')"
```
Expected: imprime `OK` (JSON válido; `cat` presente e correto; COT sem o cargo CAT mas com a cross-reference).

- [ ] **Step 4: Regenerar `states_data.json` (organograma reflete a CAT)**

Run:
```bash
python scripts/build_organs_detail.py && python scripts/build_states_data.py
```
Então confirmar que o `ro.json` à mão não foi sobrescrito (a CAT continua lá):
```bash
python -c "import json; assert 'cat' in json.load(open('database/organs_detail/ro.json',encoding='utf-8'))['organs']; print('ro.json preservado')"
```
Expected: scripts concluem sem erro; imprime `ro.json preservado`. Se a CAT sumir do `ro.json`, PARAR — `build_organs_detail.py` não deveria tocar o arquivo escrito à mão; investigar antes de prosseguir.

- [ ] **Step 5: Commit**

```bash
git add database/organs_detail/ro.json database/states_data.json database/organs_detail
git commit -m "feat(dados): CAT vira órgão de execução próprio no ro.json (cargo movido do COT)"
```

---

### Task 3: Reordenar `ORGAN_ORDER` e reescrever o Art. 3 (`build_minuta_structure.py`)

**Files:**
- Modify: `scripts/build_minuta_structure.py:35-46` (ORGAN_ORDER), `:160-174` (build_estrutura_chapter)
- Regenerate: `database/minuta_structure.json`

- [ ] **Step 1: Substituir `ORGAN_ORDER` pela nova ordem (com `cat`)**

Substituir o bloco `ORGAN_ORDER = [ ... ]` por:

```python
ORGAN_ORDER = [
    ("dpo",   "DA DIRETORIA DE PLANEJAMENTO OPERACIONAL (DPO)",          "A"),
    ("doe",   "DA DIRETORIA OPERACIONAL ESPECIALIZADA (DOE)",            "A"),
    ("cot",   "DO COMANDO DE OPERAÇÕES TÉCNICAS (COT)",                  "O"),
    ("crbm",  "DOS COMANDOS REGIONAIS DE BOMBEIRO MILITAR (CRBM)",       "O"),
    ("bbm",   "DO BATALHÃO DE BOMBEIROS MILITAR (BBM)",                  "O"),
    ("cibm",  "DA COMPANHIA INDEPENDENTE DE BOMBEIROS MILITAR (CIBM)",   "A"),
    ("cat",   "DA COORDENADORIA DE ATIVIDADES TÉCNICAS (CAT)",           "A"),
    ("bbs",   "DO BATALHÃO DE BUSCA E SALVAMENTO (BBS)",                 "O"),
    ("bifea", "DO BATALHÃO DE INCÊNDIO FLORESTAL E EMERGÊNCIAS AMBIENTAIS (BIFEA)", "O"),
    ("boa",   "DO BATALHÃO DE OPERAÇÕES AÉREAS (BOA)",                   "O"),
    ("gbm",   "DO GRUPO DE BOMBEIROS MILITAR (GBM)",                     "O"),
]

# Área de atuação dos Órgãos de Execução (LOB Art. 9), para agrupar o Art. 3.
AREA_BY_ORGAN = {
    "bbm": "ordinaria", "cibm": "ordinaria", "cat": "ordinaria",
    "bbs": "terrestre", "bifea": "terrestre",
    "boa": "aerea",
    "gbm": "conveniada",
}
AREA_LABELS = [
    ("ordinaria",  "Atuação Operacional Ordinária"),
    ("terrestre",  "Atuação Operacional Especializada Terrestre"),
    ("aerea",      "Atuação Operacional Especializada Aérea"),
    ("conveniada", "Atuação Operacional Conveniada Municipal"),
]
```

- [ ] **Step 2: Adicionar o helper `_join_orgaos` e reescrever `build_estrutura_chapter`**

Substituir a função `build_estrutura_chapter` inteira por:

```python
def _join_orgaos(keys, organs, art_by_key):
    """['dpo','doe','cot'] -> 'a Diretoria ... (DPO), a Diretoria ... (DOE) e o Comando ... (COT)'."""
    parts = []
    for k in keys:
        o = organs.get(k)
        if not o:
            continue
        nome = o.get("name", k.upper())
        abbr = o.get("abbreviation") or k.upper()
        parts.append(f"{art_by_key[k].lower()} {nome} ({abbr})")
    if len(parts) <= 1:
        return "".join(parts)
    return ", ".join(parts[:-1]) + " e " + parts[-1]


def build_estrutura_chapter(organs):
    art_by_key = {k: art for (k, _t, art) in ORGAN_ORDER}
    cat_of = {k: (organs.get(k) or {}).get("category", "") for (k, _t, _a) in ORGAN_ORDER}

    setorial = [k for (k, _t, _a) in ORGAN_ORDER if cat_of[k] == "Direção Setorial"]
    regional = [k for (k, _t, _a) in ORGAN_ORDER if cat_of[k] == "Direção Regional"]

    direcao_items = []
    if setorial:
        direcao_items.append({"text": f"de Direção Setorial: {_join_orgaos(setorial, organs, art_by_key)}", "source": "ro"})
    if regional:
        direcao_items.append({"text": f"de Direção Regional: {_join_orgaos(regional, organs, art_by_key)}", "source": "ro"})

    execucao_items = []
    for area_key, area_label in AREA_LABELS:
        keys = [k for (k, _t, _a) in ORGAN_ORDER if AREA_BY_ORGAN.get(k) == area_key]
        if not keys:
            continue
        execucao_items.append({"text": f"{area_label}: {_join_orgaos(keys, organs, art_by_key)}", "source": "ro"})

    direcao = {
        "id": "direcao", "kind": "incisos", "editId": "estrutura/direcao",
        "caput": "São Órgãos de Direção Operacional:",
        "items": direcao_items, "proposedText": proposed_text(direcao_items),
    }
    execucao = {
        "id": "execucao", "kind": "incisos", "editId": "estrutura/execucao",
        "caput": "Os Órgãos de Execução classificam-se, quanto à área de atuação, em:",
        "items": execucao_items, "proposedText": proposed_text(execucao_items),
    }
    return {
        "id": "estrutura", "kind": "articles", "chapterTitle": "DA ESTRUTURA ORGANIZACIONAL",
        "editId": "estrutura",
        "articles": [direcao, execucao],
    }
```

- [ ] **Step 3: Regenerar `minuta_structure.json`**

Run: `python scripts/build_minuta_structure.py`
Expected: imprime "Gerado: …minuta_structure.json" e a contagem (12 órgãos).

- [ ] **Step 4: Validar a estrutura gerada**

Run:
```bash
python -c "
import json
d=json.load(open('database/minuta_structure.json',encoding='utf-8'))
chs={c['id']:c for c in d['chapters']}
est=chs['estrutura']
assert est['kind']=='articles', est['kind']
assert [a['editId'] for a in est['articles']]==['estrutura/direcao','estrutura/execucao']
dir_txt=est['articles'][0]['items']
assert 'de Direção Setorial' in dir_txt[0]['text'] and '(DPO)' in dir_txt[0]['text'] and '(COT)' in dir_txt[0]['text']
assert 'de Direção Regional' in dir_txt[1]['text'] and '(CRBM)' in dir_txt[1]['text']
exe_txt=[i['text'] for i in est['articles'][1]['items']]
assert any('Atuação Operacional Ordinária' in t and '(CAT)' in t and '(CIBM)' in t for t in exe_txt)
assert any(c.get('organKey')=='cat' for c in d['chapters']), 'capítulo CAT ausente'
order=[c['organKey'] for c in d['chapters'] if c.get('kind')=='organ']
assert order==['dpo','doe','cot','crbm','bbm','cibm','cat','bbs','bifea','boa','gbm','guarnicao'], order
print('OK')
"
```
Expected: imprime `OK`.

- [ ] **Step 5: Commit**

```bash
git add scripts/build_minuta_structure.py database/minuta_structure.json
git commit -m "feat(minuta): Art. 3 em dois artigos (Direção/Execução por área) + capítulo CAT"
```

---

### Task 4: Wizard indexa o `kind: "articles"` (`MinutaWizard.jsx`)

**Files:**
- Modify: `src/pages/MinutaWizard.jsx:24-42` (`indexLeaves`), `:45-59` (`indexSources`)

- [ ] **Step 1: Estender `indexLeaves` para o `kind: "articles"`**

Substituir a função `indexLeaves` por:

```js
// Índice editId -> { items, sectionTitle, chapterTitle, proposedText, kind }
function indexLeaves(structure) {
  const idx = {}
  for (const ch of structure.chapters) {
    if (ch.kind === 'organ') {
      for (const s of ch.sections) {
        idx[s.editId] = {
          items: s.items ?? [], proposedText: s.proposedText ?? '',
          sectionTitle: s.sectionTitle, chapterTitle: ch.chapterTitle, kind: s.kind,
        }
      }
    } else if (ch.kind === 'articles') {
      for (const a of ch.articles) {
        idx[a.editId] = {
          items: a.items ?? [], proposedText: a.proposedText ?? '',
          sectionTitle: null, chapterTitle: ch.chapterTitle, kind: a.kind,
        }
      }
    } else {
      idx[ch.editId] = {
        items: ch.items ?? [], proposedText: ch.proposedText ?? '',
        sectionTitle: null, chapterTitle: ch.chapterTitle, kind: ch.kind,
      }
    }
  }
  return idx
}
```

- [ ] **Step 2: Estender `indexSources` para o `kind: "articles"`**

Na função `indexSources`, substituir o loop:

```js
  for (const ch of structure.chapters) {
    if (ch.kind === 'organ') ch.sections.forEach(s => add(s.editId, s.items))
    else add(ch.editId, ch.items)
  }
```

por:

```js
  for (const ch of structure.chapters) {
    if (ch.kind === 'organ') ch.sections.forEach(s => add(s.editId, s.items))
    else if (ch.kind === 'articles') ch.articles.forEach(a => add(a.editId, a.items))
    else add(ch.editId, ch.items)
  }
```

- [ ] **Step 3: Verificar build de produção**

Run: `npm run build`
Expected: build conclui sem erros (Vite/Rollup → `dist/`).

- [ ] **Step 4: Verificação manual no dev server**

Run: `npm run dev -- --port 5173 --strictPort`
Abrir http://localhost:5173/minuta e confirmar:
- O capítulo "DA ESTRUTURA ORGANIZACIONAL" aparece com **dois artigos** (Direção / Execução); a Execução Ordinária lista BBM, CIBM e CAT.
- Existe um capítulo "DA COORDENADORIA DE ATIVIDADES TÉCNICAS (CAT)".
- Na etapa "Revisão & curadoria": a barra "Fontes" e os checkboxes por inciso funcionam nos dois artigos da Estrutura; o botão "editar" abre o textarea em `estrutura/direcao` e `estrutura/execucao` sem erro no console.
- O sumário rola até a Estrutura ao clicar.

- [ ] **Step 5: Commit**

```bash
git add src/pages/MinutaWizard.jsx
git commit -m "feat(minuta): wizard indexa capítulo kind 'articles' (Art. 3 multi-artigo)"
```

---

### Task 5: Comparador ganha a CAT + atualizar contagens/docs

**Files:**
- Modify: `scripts/minuta_comparison_lib.py:27-38` (AUTO_MATCH_KEYWORDS)
- Modify: `scripts/test_minuta_comparison_lib.py` (append)
- Modify: `scripts/build_minuta_comparison.py:5,37,232` (comentários/contagem)
- Modify: `CLAUDE.md` (contagens e lista de órgãos)
- Regenerate: `database/comparativo_dpo_cot.json`, `database/comparativo_minuta.json`

- [ ] **Step 1: Escrever o teste do auto-match `cat` (falha)**

Anexar ao final de `scripts/test_minuta_comparison_lib.py` (antes de um eventual `print("OK")` final — se houver, mover o print para depois):

```python
def test_auto_match_cat():
    organs = {
        "x1": {"name": "Coordenadoria de Atividades Técnicas"},
        "x2": {"name": "Centro de Atividades Técnicas"},
        "x3": {"name": "Comando de Operações Técnicas"},  # não deve casar
        "x4": {"name": "Batalhão de Bombeiros"},          # não deve casar
    }
    ids = set(auto_match_organ_ids("cat", organs))
    assert ids == {"x1", "x2"}, ids


test_auto_match_cat()
```

Garantir que `auto_match_organ_ids` está importado no topo do arquivo de teste (junto aos demais imports de `minuta_comparison_lib`).

- [ ] **Step 2: Rodar o teste e ver falhar**

Run: `python scripts/test_minuta_comparison_lib.py`
Expected: FAIL (AssertionError) — sem a chave `cat`, `auto_match_organ_ids` retorna `[]`, logo `ids == set()`.

- [ ] **Step 3: Adicionar a entrada `cat` em `AUTO_MATCH_KEYWORDS`**

Em `scripts/minuta_comparison_lib.py`, dentro do dict `AUTO_MATCH_KEYWORDS`, acrescentar a entrada (após `"boa"`):

```python
    "cat":   {"include": ["atividades tecnicas", "atividade tecnica"],
              "exclude": ["operacoes tecnicas", "comando de operacoes"]},
```

- [ ] **Step 4: Rodar o teste e ver passar**

Run: `python scripts/test_minuta_comparison_lib.py`
Expected: PASS (imprime `OK`, se o arquivo terminar com esse print).

- [ ] **Step 5: Regenerar o comparador**

Run:
```bash
python scripts/build_dpo_cot_comparison.py && python scripts/build_minuta_comparison.py
```
Expected: concluem sem erro; o segundo lista 12 órgãos, incluindo `cat`.

- [ ] **Step 6: Validar o comparador gerado**

Run:
```bash
python -c "
import json
d=json.load(open('database/comparativo_minuta.json',encoding='utf-8'))
keys=[o['key'] for o in d['organs']]
assert 'cat' in keys, keys
cat=[o for o in d['organs'] if o['key']=='cat'][0]
assert cat['reference'] is not None and cat['reference']['abbreviation']=='CAT'
print('cat states:', len(cat['states'])); print('OK')
"
```
Expected: imprime a contagem de estados da CAT e `OK`.

- [ ] **Step 7: Atualizar contagens em `build_minuta_comparison.py`**

Substituir as três menções de contagem:
- Docstring (linha ~5): `11 órgãos (10 da LOB + guarnição)` → `12 órgãos (11 da LOB + guarnição)`.
- Comentário do `ORGAN_KEYS` (linha ~37): `Ordem dos 11 órgãos (10 da LOB + guarnição)` → `Ordem dos 12 órgãos (11 da LOB + guarnição)`.
- `print(...)` do bloco `__main__` (linha ~232): `11 órgãos (10 da LOB + guarnição)` → `12 órgãos (11 da LOB + guarnição)`.

- [ ] **Step 8: Atualizar `CLAUDE.md`**

Aplicar as substituições exatas:

`espelha os 11 órgãos da minuta (10 da LOB + Guarnição)` →
`espelha os 12 órgãos da minuta (11 da LOB + Guarnição)`

`Estrutura + 10 órgãos (dpo, cot, doe, crbm, bbm, cibm, gbm, bbs, bifea, boa) + capítulo da **Guarnição de Serviço Operacional**` →
`Estrutura + 11 órgãos (dpo, doe, cot, crbm, bbm, cibm, cat, bbs, bifea, boa, gbm) + capítulo da **Guarnição de Serviço Operacional**`

> Se houver outras ocorrências de "10 da LOB"/"11 órgãos" no `CLAUDE.md`, ajustá-las para 11/12 de modo consistente.

- [ ] **Step 9: Commit**

```bash
git add scripts/minuta_comparison_lib.py scripts/test_minuta_comparison_lib.py scripts/build_minuta_comparison.py database/comparativo_dpo_cot.json database/comparativo_minuta.json CLAUDE.md
git commit -m "feat(comparador): coluna CAT no Subsídio à Minuta + contagens (12 órgãos)"
```

---

## Self-Review

**Spec coverage:**
- CAT como órgão próprio no `ro.json` (cargo movido do COT) → Task 2. ✓
- `ORGAN_ORDER` reordenado + `cat` → Task 3 Step 1. ✓
- Art. 3 em dois artigos via `kind: "articles"` → Task 1 (motor) + Task 3 (geração) + Task 4 (wizard). ✓
- CAT no organograma do estado → Task 2 Step 4 (regen `states_data.json`). ✓
- CAT no comparador + auto-match → Task 5. ✓
- Contagens/docs (11 LOB + Guarnição = 12) → Task 5 Steps 7-8. ✓
- Testes: `kind articles` (Task 1), auto-match `cat` (Task 5). ✓
- Fora de escopo (enriquecimento de competências da CAT; órgãos administrativos) — não há tarefa, correto. ✓

**Placeholder scan:** sem TBD/TODO; todo passo de código traz o código completo; comandos com saída esperada. ✓

**Type consistency:** `kind: "articles"` carrega `articles: [<incisos leaf>]`; cada folha tem `{id, kind:'incisos', editId, caput, items, proposedText}`, igual ao que `buildArticles`/`indexLeaves`/`indexSources` consomem. `editId`s `estrutura/direcao` e `estrutura/execucao` usados de forma idêntica nos três arquivos. `cat` keyado igual em `ro.json`, `ORGAN_ORDER`, `AREA_BY_ORGAN` e `AUTO_MATCH_KEYWORDS`. ✓
