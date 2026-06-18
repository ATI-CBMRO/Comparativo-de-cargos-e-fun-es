# Minuta de Regimento Articulada Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Transformar a minuta gerada de blocos de texto em um regimento articulado (Art. 1º, 2º…, incisos), com pré-visualização ao vivo e fontes por seção no wizard.

**Architecture:** Um módulo puro `src/lib/minutaArticles.js` (`buildArticles`) converte os dados do órgão + edições do usuário num array de artigos numerados. Dois renderizadores consomem esse array: a pré-visualização HTML (na tela) e o gerador `.docx` (no download), garantindo saída idêntica. O script Python passa a emitir JSON articulado (6 capítulos, `kind`, `caput`, `sourceExcerpts`).

**Tech Stack:** React 18 · Vite (ESM, `"type": "module"`) · `docx` v9 · Python stdlib · testes com `node:test` nativo (sem dependências novas).

## Global Constraints

- Projeto ESM: arquivos `.js`/`.jsx` usam `import`/`export`.
- Sem libs de teste novas — usar `node:test` + `node:assert/strict`, rodando `node --test <arquivo>`.
- Identidade visual: vermelho `#c8102e`, navy `#121d3d`; CSS vars `--text-muted`, `--border-card`, `--gray-50`, `--text-secondary`.
- `.docx`: Times New Roman, espaçamento 1,5 (`line: 360`), margens ABNT (`top/left: 1701`, `bottom/right: 1134` twips). Tamanhos docx em half-points (24 = 12pt).
- Gera-se um documento por órgão (DPO/COT separados). Nome: `Minuta_RI_<LABEL>_CBMRO.docx`.
- Não editar `database/minuta_structure.json` à mão — é gerado por `scripts/build_minuta_structure.py`.

---

## Mapa de arquivos

| Ação | Arquivo | Responsabilidade |
|---|---|---|
| Criar | `src/lib/minutaArticles.js` | `articleLabel`, `romanize`, `normalizeInciso`, `buildArticles` — lógica pura de articulação |
| Criar | `src/lib/minutaArticles.test.js` | Testes do módulo acima |
| Modificar | `scripts/build_minuta_structure.py` | JSON articulado (6 capítulos, `kind`, `caput`, `sourceExcerpts`) |
| Regerar | `database/minuta_structure.json` | Saída do script |
| Modificar | `src/pages/MinutaWizard.jsx` | Prévia ao vivo, fontes clicáveis, `.docx` via `buildArticles` |

---

## Task 1: Helpers puros em `minutaArticles.js`

**Files:**
- Create: `src/lib/minutaArticles.js`
- Test: `src/lib/minutaArticles.test.js`

**Interfaces:**
- Produces:
  - `articleLabel(n: number) -> string` — "Art. 1º"…"Art. 9º" (ordinal até 9), "Art. 10"+ (cardinal)
  - `romanize(n: number) -> string` — algarismo romano maiúsculo
  - `normalizeInciso(text: string, index: number, total: number) -> string` — remove marcador de lista inicial e pontuação final, minúscula na 1ª letra, sufixo ";" / "; e" (penúltimo) / "." (último)

- [ ] **Step 1: Escrever os testes (falhando)**

Criar `src/lib/minutaArticles.test.js`:

```js
import { test } from 'node:test'
import assert from 'node:assert/strict'
import { articleLabel, romanize, normalizeInciso } from './minutaArticles.js'

test('articleLabel usa ordinal até 9 e cardinal a partir de 10', () => {
  assert.equal(articleLabel(1), 'Art. 1º')
  assert.equal(articleLabel(9), 'Art. 9º')
  assert.equal(articleLabel(10), 'Art. 10')
  assert.equal(articleLabel(12), 'Art. 12')
})

test('romanize converte inteiros em algarismos romanos', () => {
  assert.equal(romanize(1), 'I')
  assert.equal(romanize(4), 'IV')
  assert.equal(romanize(9), 'IX')
  assert.equal(romanize(14), 'XIV')
})

test('normalizeInciso minusculiza inicial e pontua por posição', () => {
  assert.equal(normalizeInciso('Coordenação operacional', 0, 3), 'coordenação operacional;')
  assert.equal(normalizeInciso('Execução das ações', 1, 3), 'execução das ações; e')
  assert.equal(normalizeInciso('Proteção e defesa civil', 2, 3), 'proteção e defesa civil.')
})

test('normalizeInciso remove marcador de lista e pontuação preexistente', () => {
  assert.equal(normalizeInciso('1. planejar as ações.', 0, 1), 'planejar as ações.')
  assert.equal(normalizeInciso('I - fiscalizar;', 0, 2), 'fiscalizar;')
})
```

- [ ] **Step 2: Rodar os testes e confirmar que falham**

Run: `node --test src/lib/minutaArticles.test.js`
Expected: FAIL — `Cannot find module './minutaArticles.js'` (arquivo ainda não existe).

- [ ] **Step 3: Implementar os helpers**

Criar `src/lib/minutaArticles.js`:

```js
// Lógica pura de articulação da minuta de regimento (sem React, sem docx).

export function articleLabel(n) {
  return n <= 9 ? `Art. ${n}º` : `Art. ${n}`
}

const ROMAN_MAP = [
  [1000, 'M'], [900, 'CM'], [500, 'D'], [400, 'CD'],
  [100, 'C'], [90, 'XC'], [50, 'L'], [40, 'XL'],
  [10, 'X'], [9, 'IX'], [5, 'V'], [4, 'IV'], [1, 'I'],
]

export function romanize(n) {
  let out = ''
  let val = n
  for (const [v, sym] of ROMAN_MAP) {
    while (val >= v) { out += sym; val -= v }
  }
  return out
}

// Remove marcador de lista inicial ("1.", "1)", "I -", "- ", "a)") e pontuação
// final, minúscula a 1ª letra e aplica o sufixo conforme a posição no rol.
export function normalizeInciso(text, index, total) {
  let t = (text ?? '').trim()
  t = t.replace(/^(\d+[.)]|[ivxlcdm]+\s*[-–.)]|[a-z][).]|[-–•])\s*/i, '')
  t = t.replace(/[;.]\s*$/, '')
  if (t) t = t[0].toLowerCase() + t.slice(1)
  let suffix = ';'
  if (index === total - 1) suffix = '.'
  else if (index === total - 2) suffix = '; e'
  return t + suffix
}
```

- [ ] **Step 4: Rodar os testes e confirmar que passam**

Run: `node --test src/lib/minutaArticles.test.js`
Expected: PASS — 4 testes ok.

- [ ] **Step 5: Commit**

```bash
git add src/lib/minutaArticles.js src/lib/minutaArticles.test.js
git commit -m "feat: helpers puros de articulação (articleLabel, romanize, normalizeInciso)"
```

---

## Task 2: `buildArticles` em `minutaArticles.js`

**Files:**
- Modify: `src/lib/minutaArticles.js`
- Test: `src/lib/minutaArticles.test.js`

**Interfaces:**
- Consumes (de Task 1): `romanize`, `normalizeInciso` (uso interno).
- Produces:
  - `buildArticles(organData, edits) -> Article[]`
  - `organData` = `{ sections: [{ id, chapterTitle, kind, caput, proposedText }] }`
  - `edits` = `{ [sectionId]: string }` (texto editado; cai para `proposedText` se ausente)
  - `Article` = `{ number, chapterNumber, chapterTitle, caput, incisos }`
    - `number`: inteiro sequencial contínuo no documento
    - `chapterNumber`: inteiro só no 1º artigo de cada capítulo, senão `null`
    - `chapterTitle`: string só no 1º artigo de cada capítulo, senão `null`
    - `caput`: string
    - `incisos`: `string[]` já normalizados (sem o prefixo romano)
  - Regras por `kind`: `prose` = cada linha não-vazia vira um artigo (caput = linha, sem incisos); `incisos` = um artigo (caput = `section.caput`, incisos = linhas não-vazias normalizadas); `cargos` = linha terminada em ":" abre artigo (caput = "Ao {nome} compete:"), linhas seguintes não-vazias viram incisos; linhas em branco ignoradas; incisos antes do 1º "Cargo:" descartados.

- [ ] **Step 1: Escrever os testes (falhando)**

Adicionar ao final de `src/lib/minutaArticles.test.js`:

```js
import { buildArticles } from './minutaArticles.js'

const ORGAN = {
  sections: [
    { id: 'preliminares', chapterTitle: 'DAS DISPOSIÇÕES PRELIMINARES', kind: 'prose', caput: null,
      proposedText: 'Primeiro artigo do objeto.\nSegundo artigo da base legal.' },
    { id: 'competencias', chapterTitle: 'DA COMPETÊNCIA', kind: 'incisos', caput: 'Compete à DPO:',
      proposedText: 'Coordenação operacional\nExecução das ações\nProteção civil' },
    { id: 'cargos_atribuicoes', chapterTitle: 'DAS ATRIBUIÇÕES DOS CARGOS', kind: 'cargos', caput: null,
      proposedText: 'Diretor:\n  planejar\n  coordenar\n\nAdjunto:\n  substituir o Diretor' },
  ],
}

test('buildArticles numera artigos continuamente e marca o 1º de cada capítulo', () => {
  const arts = buildArticles(ORGAN, {})
  assert.equal(arts.length, 5) // 2 prose + 1 incisos + 2 cargos
  assert.deepEqual(arts.map(a => a.number), [1, 2, 3, 4, 5])
  assert.equal(arts[0].chapterTitle, 'DAS DISPOSIÇÕES PRELIMINARES')
  assert.equal(arts[0].chapterNumber, 1)
  assert.equal(arts[1].chapterTitle, null) // 2º artigo do mesmo capítulo
  assert.equal(arts[2].chapterTitle, 'DA COMPETÊNCIA')
  assert.equal(arts[2].chapterNumber, 2)
  assert.equal(arts[3].chapterTitle, 'DAS ATRIBUIÇÕES DOS CARGOS')
  assert.equal(arts[3].chapterNumber, 3)
  assert.equal(arts[4].chapterTitle, null)
})

test('buildArticles articula incisos normalizados', () => {
  const arts = buildArticles(ORGAN, {})
  assert.equal(arts[2].caput, 'Compete à DPO:')
  assert.deepEqual(arts[2].incisos, [
    'coordenação operacional;',
    'execução das ações; e',
    'proteção civil.',
  ])
})

test('buildArticles monta artigo por cargo com caput "Ao ... compete:"', () => {
  const arts = buildArticles(ORGAN, {})
  assert.equal(arts[3].caput, 'Ao Diretor compete:')
  assert.deepEqual(arts[3].incisos, ['planejar;', 'coordenar.'])
  assert.equal(arts[4].caput, 'Ao Adjunto compete:')
  assert.deepEqual(arts[4].incisos, ['substituir o Diretor.'])
})

test('buildArticles usa edits no lugar do proposedText', () => {
  const arts = buildArticles(ORGAN, { competencias: 'Único item' })
  assert.deepEqual(arts[2].incisos, ['único item.'])
})
```

- [ ] **Step 2: Rodar os testes e confirmar que falham**

Run: `node --test src/lib/minutaArticles.test.js`
Expected: FAIL — `buildArticles is not a function` / `is not exported`.

- [ ] **Step 3: Implementar `buildArticles`**

Adicionar ao final de `src/lib/minutaArticles.js`:

```js
export function buildArticles(organData, edits = {}) {
  const articles = []
  let articleCounter = 0
  let chapterCounter = 0

  for (const section of organData.sections) {
    const text = edits[section.id] ?? section.proposedText ?? ''
    const lines = text.split('\n')
    let firstOfSection = true

    const push = (caput, incisos) => {
      articleCounter += 1
      let chapterTitle = null
      let chapterNumber = null
      if (firstOfSection && section.chapterTitle) {
        chapterCounter += 1
        chapterTitle = section.chapterTitle
        chapterNumber = chapterCounter
      }
      firstOfSection = false
      articles.push({ number: articleCounter, chapterNumber, chapterTitle, caput, incisos })
    }

    if (section.kind === 'prose') {
      for (const line of lines) {
        const c = line.trim()
        if (c) push(c, [])
      }
    } else if (section.kind === 'incisos') {
      const raw = lines.map(l => l.trim()).filter(Boolean)
      const incisos = raw.map((t, i) => normalizeInciso(t, i, raw.length))
      push(section.caput ?? '', incisos)
    } else if (section.kind === 'cargos') {
      let current = null
      const flush = () => {
        if (current) {
          const incisos = current.raw.map((t, i) => normalizeInciso(t, i, current.raw.length))
          push(current.caput, incisos)
          current = null
        }
      }
      for (const line of lines) {
        const c = line.trim()
        if (!c) continue
        if (c.endsWith(':')) {
          flush()
          current = { caput: `Ao ${c.slice(0, -1).trim()} compete:`, raw: [] }
        } else if (current) {
          current.raw.push(c)
        }
      }
      flush()
    }
  }

  return articles
}
```

- [ ] **Step 4: Rodar os testes e confirmar que passam**

Run: `node --test src/lib/minutaArticles.test.js`
Expected: PASS — 8 testes ok.

- [ ] **Step 5: Commit**

```bash
git add src/lib/minutaArticles.js src/lib/minutaArticles.test.js
git commit -m "feat: buildArticles converte seções editadas em artigos numerados"
```

---

## Task 3: Script Python — JSON articulado

**Files:**
- Modify: `scripts/build_minuta_structure.py`
- Regerar: `database/minuta_structure.json`

**Interfaces:**
- Produces: `database/minuta_structure.json` no formato `{ generated_by, dpo, cot }`, cada órgão `{ label, abbr, artigoCaput, sections: [...] }`, cada seção `{ id, title, chapterTitle, kind, caput, proposedText, sources, sourceExcerpts }`. Consumido por `MinutaWizard.jsx` (Tasks 4–5).

- [ ] **Step 1: Substituir o conteúdo do script**

Sobrescrever `scripts/build_minuta_structure.py` com:

```python
"""
build_minuta_structure.py — Portal CBM

Gera database/minuta_structure.json: estrutura ARTICULADA do regimento interno
(6 capítulos por órgão), texto proposto, fontes e trechos por estado.

Entrada: database/comparativo_dpo_cot.json
Saída:   database/minuta_structure.json

Rodar: python scripts/build_minuta_structure.py
"""

import json
import re
import sys
import unicodedata
from pathlib import Path

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

BASE_DIR = Path(__file__).parent.parent
IN_JSON  = BASE_DIR / "database" / "comparativo_dpo_cot.json"
OUT_JSON = BASE_DIR / "database" / "minuta_structure.json"

SECTIONS = [
    {"id": "preliminares",       "title": "Disposições Preliminares", "chapterTitle": "DAS DISPOSIÇÕES PRELIMINARES", "kind": "prose"},
    {"id": "finalidade",         "title": "Finalidade",               "chapterTitle": "DA FINALIDADE",                 "kind": "prose"},
    {"id": "competencias",       "title": "Competências",             "chapterTitle": "DA COMPETÊNCIA",                "kind": "incisos"},
    {"id": "organizacao",        "title": "Organização Interna",      "chapterTitle": "DA ORGANIZAÇÃO",                "kind": "incisos"},
    {"id": "cargos_atribuicoes", "title": "Atribuições dos Cargos",   "chapterTitle": "DAS ATRIBUIÇÕES DOS CARGOS",    "kind": "cargos"},
    {"id": "disposicoes_finais", "title": "Disposições Finais",       "chapterTitle": "DAS DISPOSIÇÕES FINAIS",        "kind": "prose"},
]

ORGAN_LABELS = {"dpo": "Diretoria de Planejamento Operacional", "cot": "Comando de Operações Técnicas"}
ORGAN_ABBR   = {"dpo": "DPO", "cot": "COT"}
ORGAN_ART    = {"dpo": "A",  "cot": "O"}           # artigo definido
ORGAN_DE     = {"dpo": "da", "cot": "do"}          # contração de "de"
ORGAN_GEN    = {"dpo": "a",  "cot": "o"}           # sufixo de gênero (subordinad-a/o)
ORGAN_CAPUT  = {"dpo": "à DPO", "cot": "ao COT"}   # complemento do caput de competência

DISP_FINAIS = "\n".join([
    "Os casos omissos neste Regimento Interno serão resolvidos pelo Comandante-Geral do CBMRO.",
    "Este Regimento Interno entra em vigor na data de sua publicação, revogadas as disposições em contrário.",
])


def normalize(text: str) -> str:
    text = re.sub(r"^\s*[\dIVXivx]+[.)]\s*", "", text.strip())
    return text.strip().lower()


def _ascii_lower(s: str) -> str:
    return "".join(c for c in unicodedata.normalize("NFD", s) if unicodedata.category(c) != "Mn").lower()


def _first_lower(s: str) -> str:
    return (s[:1].lower() + s[1:]) if s else s


_LEGAL_MARKERS = re.compile(r"\d|§|\bart\b|\blei\b|\blc\b|\bdecreto\b|red\.")


def _other_state_tokens(all_states: list) -> set:
    toks = set()
    for s in all_states:
        if s.get("id") == "ro":
            continue
        nm = _ascii_lower(s.get("name", "")).strip()
        if nm and nm != "para":
            toks.add(nm)
    return toks


def is_generic_competencia(text: str, other_state_names: set) -> bool:
    low = _ascii_lower(text)
    if _LEGAL_MARKERS.search(low):
        return False
    if re.match(r"^[ivxlcdm]+\s*[-–.)]", low):
        return False
    if re.search(r"\(\s*al[ií]nea|\(\s*art|\(\s*lei", low):
        return False
    for m in re.finditer(r"cbm([a-z]{2})", low):
        if m.group(1) != "ro":
            return False
    for name in other_state_names:
        if re.search(r"\b" + re.escape(name) + r"\b", low):
            return False
    return True


def organs_of(state: dict, group_key: str) -> list:
    v = state.get(group_key)
    return v if isinstance(v, list) else []


def _state_by_id(all_states: list, sid: str) -> dict:
    for s in all_states:
        if s.get("id") == sid:
            return s
    return {}


def _ro_first_organ(all_states: list, key: str) -> dict:
    orgs = organs_of(_state_by_id(all_states, "ro"), key)
    return orgs[0] if orgs else {}


# ── Extratores por estado (alimentam proposedText fallback e sourceExcerpts) ──

def extract_finalidade(organs: list) -> str:
    for o in organs:
        for a in (o.get("atribuicoes") or []):
            if a.strip():
                return a.strip()
    return ""


def extract_competencias(organs: list) -> str:
    seen, items = set(), []
    for o in organs:
        for a in (o.get("atribuicoes") or []):
            key = normalize(a)
            if key and key not in seen:
                seen.add(key)
                items.append(a.strip())
    return "\n".join(items)


def extract_organizacao(organs: list) -> str:
    for o in organs:
        desdb = o.get("desdobramentos") or []
        if desdb:
            return "\n".join(desdb)
    return ""


def extract_cargos(organs: list) -> str:
    seen, blocks = set(), []
    for o in organs:
        for c in (o.get("cargos") or []):
            name = (c.get("cargo") or "").strip()
            if not name or name.lower() in seen:
                continue
            seen.add(name.lower())
            atrib = c.get("atribuicoes") or []
            if not atrib:
                continue
            lines = [f"{name}:"] + [f"  {a.strip()}" for a in atrib]
            blocks.append("\n".join(lines))
    return "\n\n".join(blocks)


# ── Construtores de seção ──

def build_preliminares(key: str, ro: dict) -> str:
    label, abbr = ORGAN_LABELS[key], ORGAN_ABBR[key]
    sub  = ro.get("subordinadoA", "")
    base = ro.get("baseLegal", "")
    objeto = (f"Este Regimento Interno disciplina a organização, as competências e o "
              f"funcionamento {ORGAN_DE[key]} {label} ({abbr}), no âmbito do Corpo de "
              f"Bombeiros Militar do Estado de Rondônia.")
    legal = f"{ORGAN_ART[key]} {label} ({abbr}) é subordinad{ORGAN_GEN[key]} a {sub}" if sub \
        else f"{ORGAN_ART[key]} {label} ({abbr}) integra a estrutura do CBMRO"
    if base:
        legal += f", nos termos da {base}"
    legal += "."
    return "\n".join([objeto, legal])


def build_finalidade(key: str, ro: dict) -> str:
    fin = extract_finalidade([ro]) if ro else ""
    if not fin:
        return ""
    return f"{ORGAN_ART[key]} {ORGAN_LABELS[key]} ({ORGAN_ABBR[key]}) é o {_first_lower(fin)}"


def build_competencias(key: str, all_states: list):
    other = _other_state_tokens(all_states)
    items, seen, sources, excerpts = [], set(), [], {}
    ro_added = False
    for o in organs_of(_state_by_id(all_states, "ro"), key):
        for a in (o.get("atribuicoes") or []):
            a, kk = a.strip(), normalize(a)
            if a and kk not in seen:
                seen.add(kk); items.append(a); ro_added = True
    if ro_added:
        sources.append("ro")
        excerpts["ro"] = extract_competencias(organs_of(_state_by_id(all_states, "ro"), key))
    for s in all_states:
        if s["id"] == "ro":
            continue
        added = False
        for o in organs_of(s, key):
            for a in (o.get("atribuicoes") or []):
                a, kk = a.strip(), normalize(a)
                if not a or kk in seen:
                    continue
                if not is_generic_competencia(a, other):
                    continue
                seen.add(kk); items.append(a); added = True
        if added:
            sources.append(s["id"])
            excerpts[s["id"]] = extract_competencias(organs_of(s, key))
    return "\n".join(items), sources, excerpts


def _sources_and_excerpts(all_states: list, key: str, extractor):
    sources, excerpts = [], {}
    for s in all_states:
        txt = extractor(organs_of(s, key))
        if txt.strip():
            sources.append(s["id"])
            excerpts[s["id"]] = txt
    return sources, excerpts


def build_organ(all_states: list, key: str) -> dict:
    ro = _ro_first_organ(all_states, key)

    comp_text, comp_src, comp_exc = build_competencias(key, all_states)
    org_proposed = "\n".join(ro.get("desdobramentos") or [])
    org_src, org_exc = _sources_and_excerpts(all_states, key, extract_organizacao)
    car_proposed = extract_cargos(organs_of(_state_by_id(all_states, "ro"), key))
    car_src, car_exc = _sources_and_excerpts(all_states, key, extract_cargos)
    fin_src, fin_exc = _sources_and_excerpts(all_states, key, extract_finalidade)

    by_id = {
        "preliminares":       (build_preliminares(key, ro), [],       {},       None),
        "finalidade":         (build_finalidade(key, ro),   fin_src,  fin_exc,  None),
        "competencias":       (comp_text,                   comp_src, comp_exc, f"Compete {ORGAN_CAPUT[key]}:"),
        "organizacao":        (org_proposed,                org_src,  org_exc,  f"{ORGAN_ART[key]} {ORGAN_ABBR[key]} tem a seguinte estrutura:"),
        "cargos_atribuicoes": (car_proposed,                car_src,  car_exc,  None),
        "disposicoes_finais": (DISP_FINAIS,                 [],       {},       None),
    }

    sections = []
    for meta in SECTIONS:
        text, src, exc, caput = by_id[meta["id"]]
        sections.append({
            "id": meta["id"],
            "title": meta["title"],
            "chapterTitle": meta["chapterTitle"],
            "kind": meta["kind"],
            "caput": caput,
            "proposedText": text,
            "sources": src,
            "sourceExcerpts": exc,
        })

    return {
        "label": ORGAN_LABELS[key],
        "abbr": ORGAN_ABBR[key],
        "artigoCaput": ORGAN_CAPUT[key],
        "sections": sections,
    }


def main():
    data = json.loads(IN_JSON.read_text(encoding="utf-8"))
    all_states = data["states"]
    output = {
        "generated_by": "scripts/build_minuta_structure.py",
        "dpo": build_organ(all_states, "dpo"),
        "cot": build_organ(all_states, "cot"),
    }
    OUT_JSON.write_text(json.dumps(output, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Gerado: {OUT_JSON}")
    for key in ("dpo", "cot"):
        secs = output[key]["sections"]
        filled = sum(1 for s in secs if s["proposedText"])
        print(f"  {key.upper()}: {filled}/{len(secs)} seções com texto")


if __name__ == "__main__":
    main()
```

- [ ] **Step 2: Rodar o script**

Run: `python scripts/build_minuta_structure.py`
Expected:
```
Gerado: ...database/minuta_structure.json
  DPO: 6/6 seções com texto
  COT: 6/6 seções com texto
```

- [ ] **Step 3: Inspecionar a estrutura gerada**

Run:
```bash
python -c "
import json
d = json.load(open('database/minuta_structure.json', encoding='utf-8'))
for key in ('dpo','cot'):
    o = d[key]
    print(key.upper(), '| abbr', o['abbr'], '| artigoCaput', repr(o['artigoCaput']))
    for s in o['sections']:
        print('  ', s['id'], '| kind', s['kind'], '| caput', repr(s['caput']), '| sources', len(s['sources']))
"
```
Verificar: 6 seções por órgão na ordem `preliminares, finalidade, competencias, organizacao, cargos_atribuicoes, disposicoes_finais`; `kind` correto; `competencias`/`organizacao` com `caput` preenchido; demais com `caput: None`.

- [ ] **Step 4: Confirmar que competências seguem limpas (sem citação alheia)**

Run:
```bash
python -c "
import json
d = json.load(open('database/minuta_structure.json', encoding='utf-8'))
sec = next(s for s in d['dpo']['sections'] if s['id']=='competencias')
txt = sec['proposedText']
print('itens:', len(txt.split(chr(10))))
print('poluído?', any(t in txt for t in ('CBMSC','CBMAC','Lei ','§','(Art')))
print('1ª linha:', txt.split(chr(10))[0][:60])
"
```
Expected: `poluído? False` e nenhuma linha começando com "1.".

- [ ] **Step 5: Commit**

```bash
git add scripts/build_minuta_structure.py database/minuta_structure.json
git commit -m "feat: script gera minuta articulada (6 capítulos, kind, caput, sourceExcerpts)"
```

---

## Task 4: Wizard — prévia ao vivo e fontes clicáveis (Etapa de revisão)

**Files:**
- Modify: `src/pages/MinutaWizard.jsx`

**Interfaces:**
- Consumes: `buildArticles`, `articleLabel`, `romanize` de `../lib/minutaArticles.js`; JSON da Task 3 (`section.title`, `section.chapterTitle`, `section.kind`, `section.caput`, `section.sources`, `section.sourceExcerpts`).
- Produces: componente `ArticlePreview({ articles })` (usado também na Task 5).

- [ ] **Step 1: Atualizar imports**

Em `src/pages/MinutaWizard.jsx`, trocar o import do lucide e adicionar o do módulo de artigos. Substituir:

```jsx
import { ChevronRight, ChevronLeft, Download, ArrowLeft } from 'lucide-react'
import {
  Document, Packer, Paragraph, TextRun,
  Footer, AlignmentType, ImageRun,
} from 'docx'
```

por:

```jsx
import { ChevronRight, ChevronLeft, Download, ArrowLeft } from 'lucide-react'
import {
  Document, Packer, Paragraph, TextRun,
  Footer, AlignmentType, ImageRun,
} from 'docx'
import { buildArticles, articleLabel, romanize } from '../lib/minutaArticles.js'
```

- [ ] **Step 2: Adicionar o componente `ArticlePreview` e estado dos chips**

Adicionar o componente `ArticlePreview` no escopo do módulo (após `const STEP_LABELS = [...]`), antes de `export default function MinutaWizard()`:

```jsx
function ArticlePreview({ articles }) {
  if (!articles.length) {
    return <p style={{ color: 'var(--text-muted)', fontSize: 13 }}>(sem conteúdo nesta seção)</p>
  }
  return (
    <div style={{ fontFamily: 'Georgia, "Times New Roman", serif', fontSize: 14, lineHeight: 1.7, color: '#1a1a1a' }}>
      {articles.map(art => (
        <div key={art.number} style={{ marginBottom: 10 }}>
          {art.chapterTitle && (
            <p style={{ textAlign: 'center', fontWeight: 700, margin: '18px 0 10px' }}>
              CAPÍTULO {romanize(art.chapterNumber)}<br />{art.chapterTitle}
            </p>
          )}
          <p style={{ textAlign: 'justify', margin: '0 0 6px', textIndent: art.incisos.length ? 0 : '1.25em' }}>
            <strong>{articleLabel(art.number)}</strong> {art.caput}
          </p>
          {art.incisos.map((inc, i) => (
            <p key={i} style={{ textAlign: 'justify', margin: '0 0 4px', paddingLeft: '2em', textIndent: '-1em' }}>
              {romanize(i + 1)} - {inc}
            </p>
          ))}
        </div>
      ))}
    </div>
  )
}
```

E no corpo de `MinutaWizard`, junto aos outros `useState`, adicionar o estado da fonte expandida:

```jsx
  const [openSource, setOpenSource] = useState(null)
```

- [ ] **Step 3: Reescrever a Etapa de revisão (step === 1) em duas colunas**

Substituir todo o bloco `{step === 1 && section && ( ... )}` por:

```jsx
        {/* ── Etapa 1: revisão seção a seção (duas colunas) ── */}
        {step === 1 && section && (
          <div style={{ display: 'flex', gap: 24, flexWrap: 'wrap', alignItems: 'flex-start' }}>
            {/* Coluna de edição */}
            <div style={{ flex: '1 1 420px', minWidth: 0 }}>
              <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'baseline', marginBottom: 6 }}>
                <span style={{ fontWeight: 700, color: '#121d3d', fontSize: 17 }}>{section.title}</span>
                <span style={{ color: 'var(--text-muted)', fontSize: 13 }}>
                  Seção {sectionIdx + 1} de {sections.length}
                </span>
              </div>

              {section.sources.length > 0 && (
                <div style={{ marginBottom: 12 }}>
                  <div style={{ display: 'flex', gap: 6, flexWrap: 'wrap', alignItems: 'center' }}>
                    <span style={{ fontSize: 12, color: 'var(--text-muted)' }}>Baseado em:</span>
                    {section.sources.map(s => (
                      <button
                        key={s}
                        onClick={() => setOpenSource(openSource === s ? null : s)}
                        style={{
                          background: openSource === s ? '#c8102e' : '#eef1f6',
                          color: openSource === s ? '#fff' : '#121d3d',
                          border: '1px solid var(--border-card)', borderRadius: 4,
                          padding: '1px 7px', fontSize: 12, fontWeight: 700,
                          textTransform: 'uppercase', cursor: 'pointer',
                        }}
                      >
                        {s}
                      </button>
                    ))}
                  </div>
                  {openSource && section.sourceExcerpts[openSource] && (
                    <pre style={{
                      marginTop: 8, padding: 12, background: 'var(--gray-50)',
                      border: '1px solid var(--border-card)', borderRadius: 6,
                      fontSize: 12.5, whiteSpace: 'pre-wrap', lineHeight: 1.6,
                      color: 'var(--text-secondary)', fontFamily: 'Inter, sans-serif',
                      maxHeight: 220, overflow: 'auto',
                    }}>
                      {section.sourceExcerpts[openSource]}
                    </pre>
                  )}
                </div>
              )}

              <textarea
                value={edits[section.id] ?? ''}
                onChange={e => setEdits(prev => ({ ...prev, [section.id]: e.target.value }))}
                style={{
                  width: '100%', minHeight: 300, padding: 14,
                  border: '1.5px solid var(--border-card)', borderRadius: 8,
                  fontSize: 14, lineHeight: 1.7, fontFamily: 'Inter, sans-serif',
                  resize: 'vertical', boxSizing: 'border-box', outline: 'none',
                }}
              />

              <div style={{ display: 'flex', justifyContent: 'space-between', marginTop: 18 }}>
                <button
                  onClick={handlePrev}
                  disabled={sectionIdx === 0}
                  style={{
                    display: 'flex', alignItems: 'center', gap: 6, padding: '9px 20px',
                    border: '1.5px solid var(--border-card)', borderRadius: 7,
                    background: '#fff', cursor: sectionIdx === 0 ? 'not-allowed' : 'pointer',
                    opacity: sectionIdx === 0 ? 0.4 : 1, fontSize: 14,
                  }}
                >
                  <ChevronLeft size={16} /> Anterior
                </button>
                <button
                  onClick={handleNext}
                  style={{
                    display: 'flex', alignItems: 'center', gap: 6, padding: '9px 24px',
                    border: 'none', borderRadius: 7, background: '#c8102e', color: '#fff',
                    fontWeight: 600, cursor: 'pointer', fontSize: 14,
                  }}
                >
                  {sectionIdx < sections.length - 1 ? 'Próxima' : 'Finalizar'}
                  <ChevronRight size={16} />
                </button>
              </div>
            </div>

            {/* Coluna de prévia ao vivo (capítulo atual) */}
            <div style={{
              flex: '1 1 360px', minWidth: 0,
              border: '1px solid var(--border-card)', borderRadius: 8,
              background: '#fff', padding: 20, position: 'sticky', top: 16,
            }}>
              <div style={{ fontSize: 12, fontWeight: 700, color: 'var(--text-muted)', textTransform: 'uppercase', marginBottom: 8 }}>
                Prévia do capítulo
              </div>
              <ArticlePreview articles={buildArticles({ sections: [section] }, edits)} />
            </div>
          </div>
        )}
```

- [ ] **Step 4: Verificar no browser — prévia ao vivo e fontes**

Garantir dev server rodando (`npm run dev -- --port 5173 --strictPort`) e abrir http://localhost:5173/minuta. Escolher "DPO" e verificar:
- Layout em duas colunas; à direita a prévia "CAPÍTULO …" + "Art. Nº …" + incisos numerados (I, II, III).
- Editar a textarea altera a prévia em tempo real (numeração e pontuação dos incisos atualizam).
- Na seção Competências, clicar num chip de estado (ex.: AM) expande o trecho daquele estado; clicar de novo fecha.
- Navegar Anterior/Próxima percorre os 6 capítulos; a numeração do artigo na prévia do capítulo começa em "Art. 1º" para cada capítulo isolado (esperado — a prévia da Etapa 1 mostra só o capítulo atual).

- [ ] **Step 5: Verificar o build**

Run: `npm run build 2>&1 | tail -5`
Expected: build conclui sem erros.

- [ ] **Step 6: Commit**

```bash
git add src/pages/MinutaWizard.jsx
git commit -m "feat: wizard com prévia articulada ao vivo e fontes por seção clicáveis"
```

---

## Task 5: Wizard — `.docx` articulado e prévia completa (Etapa de download)

**Files:**
- Modify: `src/pages/MinutaWizard.jsx`

**Interfaces:**
- Consumes: `buildArticles`, `articleLabel`, `romanize`; componente `ArticlePreview` (Task 4).

- [ ] **Step 1: Reescrever o loop de capítulos em `handleDownload`**

Em `handleDownload`, substituir o bloco que começa em `// Capítulos` e vai até o fechamento do `sections.forEach(...)` por:

```jsx
      // Documento articulado (mesma fonte da prévia)
      const articles = buildArticles(data[selectedOrgan], edits)
      let chapterSeen = false
      articles.forEach(art => {
        if (art.chapterTitle) {
          children.push(
            new Paragraph({
              alignment: AlignmentType.CENTER,
              pageBreakBefore: chapterSeen,
              spacing: { before: 240, after: 0 },
              children: [new TextRun({ text: `CAPÍTULO ${romanize(art.chapterNumber)}`, bold: true, font: 'Times New Roman', size: 26 })],
            }),
            new Paragraph({
              alignment: AlignmentType.CENTER,
              spacing: { after: 240 },
              children: [new TextRun({ text: art.chapterTitle, bold: true, font: 'Times New Roman', size: 26 })],
            })
          )
          chapterSeen = true
        }
        // Caput do artigo
        children.push(
          new Paragraph({
            alignment: AlignmentType.JUSTIFIED,
            spacing: { line: 360, after: art.incisos.length ? 60 : 120 },
            indent: art.incisos.length ? undefined : { firstLine: 708 },
            children: [
              new TextRun({ text: `${articleLabel(art.number)} `, bold: true, font: 'Times New Roman', size: 24 }),
              new TextRun({ text: art.caput, font: 'Times New Roman', size: 24 }),
            ],
          })
        )
        // Incisos
        art.incisos.forEach((inc, i) => {
          children.push(
            new Paragraph({
              alignment: AlignmentType.JUSTIFIED,
              spacing: { line: 360, after: 60 },
              indent: { left: 708, hanging: 340 },
              children: [new TextRun({ text: `${romanize(i + 1)} - ${inc}`, font: 'Times New Roman', size: 24 })],
            })
          )
        })
      })
```

(O cabeçalho institucional — brasão, título, subtítulo, data — e o `Document`/rodapé permanecem inalterados, antes e depois deste bloco.)

- [ ] **Step 2: Substituir o resumo da Etapa de download (step === 2) pela prévia completa**

Substituir o bloco que renderiza os `<details>` por seção (de `{sections.map(sec => (` até o `))}` que o fecha) por:

```jsx
            <div style={{
              border: '1px solid var(--border-card)', borderRadius: 8,
              background: '#fff', padding: 24, marginBottom: 4, maxHeight: 460, overflow: 'auto',
            }}>
              <ArticlePreview articles={buildArticles(data[selectedOrgan], edits)} />
            </div>
```

- [ ] **Step 3: Verificar a prévia completa no browser**

Abrir http://localhost:5173/minuta, escolher DPO, avançar até a Etapa de download. Verificar:
- A prévia mostra o documento inteiro com numeração de artigos **contínua** (Art. 1º, 2º… seguindo entre capítulos) e capítulos I–VI.
- "Voltar e editar" retorna à última seção; "Baixar .docx" presente.

- [ ] **Step 4: Verificar o `.docx` gerado (XML)**

Criar script temporário no projeto e inspecionar o XML:
```bash
cat > _gen_check.mjs <<'EOF'
import fs from 'fs'
import { Document, Packer, Paragraph, TextRun, AlignmentType } from 'docx'
import { buildArticles, articleLabel, romanize } from './src/lib/minutaArticles.js'
const data = JSON.parse(fs.readFileSync('database/minuta_structure.json','utf-8'))
const children = []
let chapterSeen = false
for (const art of buildArticles(data.dpo, {})) {
  if (art.chapterTitle) {
    children.push(new Paragraph({ alignment: AlignmentType.CENTER, pageBreakBefore: chapterSeen, children:[new TextRun({text:`CAPÍTULO ${romanize(art.chapterNumber)}`, bold:true, font:'Times New Roman', size:26})]}))
    children.push(new Paragraph({ alignment: AlignmentType.CENTER, children:[new TextRun({text:art.chapterTitle, bold:true, font:'Times New Roman', size:26})]}))
    chapterSeen = true
  }
  children.push(new Paragraph({ alignment: AlignmentType.JUSTIFIED, children:[ new TextRun({text:`${articleLabel(art.number)} `, bold:true, font:'Times New Roman', size:24}), new TextRun({text:art.caput, font:'Times New Roman', size:24}) ]}))
  art.incisos.forEach((inc,i)=> children.push(new Paragraph({ alignment: AlignmentType.JUSTIFIED, indent:{left:708,hanging:340}, children:[new TextRun({text:`${romanize(i+1)} - ${inc}`, font:'Times New Roman', size:24})]})))
}
const doc = new Document({ sections:[{ children }] })
fs.writeFileSync('_check.docx', await Packer.toBuffer(doc))
console.log('ok bytes', fs.statSync('_check.docx').size)
EOF
node _gen_check.mjs && python -c "
import zipfile
xml = zipfile.ZipFile('_check.docx').read('word/document.xml').decode('utf-8')
print('justified:', xml.count('w:val=\"both\"'))
print('center:', xml.count('w:val=\"center\"'))
print('page breaks:', xml.count('pageBreakBefore'))
print('Art. 1º presente:', 'Art. 1' in xml)
print('CAPÍTULO presente:', 'CAP' in xml)
"
rm -f _gen_check.mjs _check.docx
```
Expected: bytes > 0; `justified` > 0; `center` ≥ 12 (2 linhas × 6 capítulos); `page breaks` = 5 (capítulos II–VI); `Art. 1º presente: True`; `CAPÍTULO presente: True`.

- [ ] **Step 5: Verificar o build**

Run: `npm run build 2>&1 | tail -5`
Expected: build conclui sem erros.

- [ ] **Step 6: Commit**

```bash
git add src/pages/MinutaWizard.jsx
git commit -m "feat: .docx articulado (artigos/incisos) e prévia completa na etapa de download"
```

---

## Verificação final

- [ ] `node --test src/lib/minutaArticles.test.js` — todos os testes passam
- [ ] Fluxo DPO completo: editar capítulos → prévia ao vivo coerente → baixar `.docx` → abrir no Word: capítulos I–VI centralizados/negrito, artigos numerados contínuos, incisos I, II, III com recuo deslocado, corpo justificado, "; e" no penúltimo inciso e "." no último
- [ ] Fluxo COT completo: idem, com concordância "ao COT" no caput de competência
- [ ] Competências sem citações de outros estados (verificado na Task 3)
- [ ] Fontes por seção: clicar chip expande trecho do estado; seções de disposições (preliminares/finais) não exibem chips
- [ ] `npm run build` conclui sem erros e `dist/database/minuta_structure.json` existe
