# Comparador "Subsídio à Minuta" — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Substituir os dois comparadores (Cargos e DPO×COT, abas do Dashboard) e a página `Compare.jsx` por uma única página `/comparar` ("Subsídio à Minuta") que compara o CBMRO contra os demais estados, organizada pela estrutura da minuta (12 órgãos, incl. Guarnição), para subsidiar o Regimento Interno.

**Architecture:** Um novo script Python (`build_minuta_comparison.py`) gera um artefato único `database/comparativo_minuta.json` combinando, por órgão, a referência do RO (de `ro.json` puro) com cada estado em duas camadas — **curado** (mapa DPO/COT de `comparativo_dpo_cot.json`, competências de `minuta_enrichment.py` pivotadas por fonte, e a Guarnição do CBMSE) e **automático** (casamento por palavra-chave em `organs_detail/<id>.json`). O frontend só faz fetch desse JSON e renderiza uma matriz (campos nas linhas, RO + estados nas colunas), com navegação por órgão, busca de estado e exportação PDF.

**Tech Stack:** Python 3 (pipeline offline, sem libs externas além da stdlib), React 18 + Vite, `lucide-react`, CSS único em `src/index.css`.

## Global Constraints

- O frontend nunca lê PDFs nem faz casamento pesado: lê `database/comparativo_minuta.json` gerado offline.
- Textos de outros estados são **verbatim**; nada é inventado. A referência do RO vem de `database/organs_detail/ro.json` **puro** (nunca o texto enriquecido da minuta — evita circularidade).
- Proveniência sempre marcada por estado: `"curado"` ou `"automatico"`.
- Os 12 órgãos, na ordem de subordinação: `dpo, cot, doe, crbm, bbm, cibm, gbm, bbs, bifea, boa, guarnicao` (os 10 primeiros vêm de `ORGAN_ORDER` em `build_minuta_structure.py`; `guarnicao` é acrescentado).
- Rota da nova página: `/comparar`. Item de sidebar: **"Subsídio à Minuta"**.
- Sem filtros de região e de nível de similaridade. Mantém busca textual de estado.
- Encoding de saída UTF-8 (`ensure_ascii=False`). No Windows, `sys.stdout.reconfigure(encoding="utf-8")`.
- Commits frequentes, mensagens em pt-BR, trailer `Co-Authored-By: Claude Opus 4.8 <noreply@anthropic.com>`.

---

### Task 1: Helpers puros do build (parse de fonte + casamento por palavra-chave)

**Files:**
- Create: `scripts/minuta_comparison_lib.py`
- Test: `scripts/test_minuta_comparison_lib.py`

**Interfaces:**
- Produces:
  - `norm(s: str) -> str` — minúsculas, sem acento, espaços colapsados.
  - `state_from_source_label(label: str) -> str | None` — extrai o id do estado (minúsculo) de um rótulo `"cf. CBMXX, ..."`; `None` se não houver `CBMxx`.
  - `AUTO_MATCH_KEYWORDS: dict[str, dict]` — por organ_key, `{"include": [...], "exclude": [...]}`.
  - `auto_match_organ_ids(organ_key: str, organs: dict) -> list[str]` — ids de órgãos do dict `organs` (de `organs_detail`) cujo `name` normalizado contém algum `include` e nenhum `exclude`.

- [ ] **Step 1: Write the failing test**

Create `scripts/test_minuta_comparison_lib.py`:

```python
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from minuta_comparison_lib import (
    norm, state_from_source_label, auto_match_organ_ids, AUTO_MATCH_KEYWORDS,
)

# norm
assert norm("Comando Regional") == "comando regional"
assert norm("Operações  Aéreas") == "operacoes aereas"

# state_from_source_label
assert state_from_source_label("cf. CBMMT, RI, Art. 236") == "mt"
assert state_from_source_label("cf. CBMSE, RISD, Art. 14") == "se"
assert state_from_source_label("cf. CBMDF, RI (Portaria nº 24/2020), Art. 454") == "df"
assert state_from_source_label("cf. CBMSP, Lei nº 616/1974, Art. 40, §2º, 7") == "sp"
assert state_from_source_label("texto sem fonte") is None

# auto_match_organ_ids — crbm casa "regional"
organs = {
    "reg-1": {"name": "1ª Região de Bombeiro Militar"},
    "bat-1": {"name": "Batalhão de Bombeiros Militar"},
    "bbs-x": {"name": "Batalhão de Busca e Salvamento"},
    "grp-1": {"name": "Grupamento de Bombeiros"},
}
assert auto_match_organ_ids("crbm", organs) == ["reg-1"]
# bbm casa "batalhao" mas EXCLUI busca/salvamento
assert auto_match_organ_ids("bbm", organs) == ["bat-1"]
# bbs casa busca/salvamento
assert auto_match_organ_ids("bbs", organs) == ["bbs-x"]
# gbm casa grupo/grupamento
assert auto_match_organ_ids("gbm", organs) == ["grp-1"]
# dpo não tem auto (curado-only)
assert "dpo" not in AUTO_MATCH_KEYWORDS

print("OK")
```

- [ ] **Step 2: Run test to verify it fails**

Run: `python scripts/test_minuta_comparison_lib.py`
Expected: FAIL — `ModuleNotFoundError: No module named 'minuta_comparison_lib'`

- [ ] **Step 3: Write minimal implementation**

Create `scripts/minuta_comparison_lib.py`:

```python
"""
minuta_comparison_lib.py — Portal CBM

Helpers puros do build do comparativo da minuta:
- normalização tolerante (sem acento, minúsculas);
- extração do estado de origem a partir do rótulo de fonte ("cf. CBMxx, ...");
- casamento automático de órgão por palavra-chave (camada "automatico").
"""

import re
import unicodedata


def norm(s: str) -> str:
    s = unicodedata.normalize("NFKD", s or "")
    s = "".join(c for c in s if not unicodedata.combining(c))
    return re.sub(r"\s+", " ", s).strip().lower()


def state_from_source_label(label: str) -> str | None:
    """'cf. CBMMT, RI, Art. 236' -> 'mt'. None se não houver CBMxx."""
    m = re.search(r"\bCBM([A-Za-z]{2})\b", label or "")
    return m.group(1).lower() if m else None


# Camada "automatico": por organ_key, palavras-chave de inclusão/exclusão (já normalizadas).
AUTO_MATCH_KEYWORDS = {
    "doe":   {"include": ["especializ"],                       "exclude": []},
    "crbm":  {"include": ["regional", "regiao de bombeiro"],   "exclude": []},
    "bbm":   {"include": ["batalhao"],
              "exclude": ["busca", "salvamento", "florestal", "ambiental",
                          "aerea", "aereo", "aviacao", "maritimo"]},
    "cibm":  {"include": ["companhia independente", "cia independente"], "exclude": []},
    "gbm":   {"include": ["grupo", "grupamento"],              "exclude": []},
    "bbs":   {"include": ["busca", "salvamento"],              "exclude": []},
    "bifea": {"include": ["florestal", "ambiental"],           "exclude": []},
    "boa":   {"include": ["aerea", "aereo", "aviacao", "operacoes aereas"], "exclude": []},
}


def auto_match_organ_ids(organ_key: str, organs: dict) -> list[str]:
    spec = AUTO_MATCH_KEYWORDS.get(organ_key)
    if not spec:
        return []
    inc, exc = spec["include"], spec["exclude"]
    out = []
    for oid, o in organs.items():
        n = norm(o.get("name", ""))
        if any(k in n for k in inc) and not any(k in n for k in exc):
            out.append(oid)
    return out
```

- [ ] **Step 4: Run test to verify it passes**

Run: `python scripts/test_minuta_comparison_lib.py`
Expected: `OK`

- [ ] **Step 5: Commit**

```bash
git add scripts/minuta_comparison_lib.py scripts/test_minuta_comparison_lib.py
git commit -m "feat: helpers puros do build do comparativo da minuta (parse de fonte + auto-match)

Co-Authored-By: Claude Opus 4.8 <noreply@anthropic.com>"
```

---

### Task 2: Script de build — gera `comparativo_minuta.json`

**Files:**
- Create: `scripts/build_minuta_comparison.py`
- Create (gerado): `database/comparativo_minuta.json`

**Interfaces:**
- Consumes: `norm`, `state_from_source_label`, `auto_match_organ_ids` (Task 1); `ORGAN_ORDER` de `build_minuta_structure.py`; `enrich_organ_for`, `GUARNICAO_CHAPTER` de `minuta_enrichment.py`.
- Produces: `database/comparativo_minuta.json` com o formato:

```jsonc
{
  "generated_by": "scripts/build_minuta_comparison.py",
  "reference": { "id": "ro", "name": "Rondônia", "abbr": "RO", "cbm": "CBMRO" },
  "organs": [
    {
      "key": "cot",
      "title": "DO COMANDO DE OPERAÇÕES TÉCNICAS (COT)",
      "abbr": "COT",
      "reference": { /* organ do RO ou null */ },
      "referenceNote": null,            /* texto quando reference é null (guarnição) */
      "states": [
        {
          "id": "mt", "name": "Mato Grosso", "abbr": "MT", "cbm": "CBMMT", "region": "Centro-Oeste",
          "provenance": "curado",       /* "curado" | "automatico" */
          "sourceLabel": "cf. CBMMT, RI, Art. 236",   /* ou null */
          "note": null,                 /* nota explicativa (DPO/COT) ou null */
          "organs": [ { "name": "...", "abbreviation": "...", "subordinadoA": "...",
                        "cargos": [ { "cargo": "...", "requisito": "...", "subordinadoA": "...",
                                      "atribuicoes": ["..."], "desdobramentos": ["..."] } ],
                        "atribuicoes": ["..."], "desdobramentos": ["..."] } ]
        }
      ]
    }
  ]
}
```

- [ ] **Step 1: Write the build script**

Create `scripts/build_minuta_comparison.py`:

```python
"""
build_minuta_comparison.py — Portal CBM

Gera database/comparativo_minuta.json: comparativo RO × demais estados, órgão a
órgão, na MESMA estrutura da minuta (12 órgãos, incl. a Guarnição de Serviço).
Para cada órgão, a referência é o RO (de organs_detail/ro.json puro) e cada
estado entra em uma de duas camadas:

  - curado:     mapa DPO/COT (comparativo_dpo_cot.json) + competências verbatim
                de minuta_enrichment (pivotadas por fonte) + Guarnição (CBMSE).
  - automatico: casamento por palavra-chave em organs_detail/<id>.json.

Depende de (rode antes): build_dpo_cot_comparison.py, build_organs_detail.py.
Rodar: python scripts/build_minuta_comparison.py
"""

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from minuta_comparison_lib import norm, state_from_source_label, auto_match_organ_ids  # noqa: E402
from build_minuta_structure import ORGAN_ORDER  # noqa: E402
from minuta_enrichment import enrich_organ_for, GUARNICAO_CHAPTER  # noqa: E402

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

BASE_DIR = Path(__file__).parent.parent
DET_DIR = BASE_DIR / "database" / "organs_detail"
STATES_JSON = BASE_DIR / "database" / "states_data.json"
DPO_COT_JSON = BASE_DIR / "database" / "comparativo_dpo_cot.json"
OUT_JSON = BASE_DIR / "database" / "comparativo_minuta.json"

REF_ID = "ro"

# Ordem dos 12 órgãos: 10 da LOB (ORGAN_ORDER) + guarnição.
ORGAN_KEYS = [k for (k, _t, _a) in ORGAN_ORDER] + ["guarnicao"]
ORGAN_TITLES = {k: t for (k, t, _a) in ORGAN_ORDER}
ORGAN_TITLES["guarnicao"] = GUARNICAO_CHAPTER["chapterTitle"]


def load_state_meta():
    data = json.loads(STATES_JSON.read_text(encoding="utf-8"))
    meta = {}
    for s in data.get("states", []):
        meta[s["id"]] = {
            "id": s["id"],
            "name": s.get("name", s["id"]),
            "abbr": s.get("abbreviation", s["id"].upper()),
            "cbm": s.get("cbm_abbreviation", ""),
            "region": s.get("region", ""),
        }
    return meta


def load_organs(sid):
    p = DET_DIR / f"{sid}.json"
    if not p.exists():
        return {}
    return json.loads(p.read_text(encoding="utf-8")).get("organs", {})


def extract_organ(organs, oid):
    o = organs.get(oid)
    if not o:
        return None
    cargos = [{
        "cargo": c.get("cargo", ""), "requisito": c.get("requisito", ""),
        "subordinadoA": c.get("subordinadoA", ""),
        "atribuicoes": list(c.get("atribuicoes", [])),
        "desdobramentos": list(c.get("desdobramentos", [])),
    } for c in o.get("cargos", [])]
    return {
        "name": o.get("name", ""), "abbreviation": o.get("abbreviation", ""),
        "subordinadoA": o.get("subordinadoA", ""),
        "atribuicoes": list(o.get("atribuicoes", [])),
        "desdobramentos": list(o.get("desdobramentos", [])),
        "cargos": cargos,
    }


def competencia_organ(items):
    """Sintetiza um 'órgão' a partir de competências verbatim (sem estrutura)."""
    return {
        "name": "", "abbreviation": "", "subordinadoA": "",
        "atribuicoes": list(items), "desdobramentos": [], "cargos": [],
    }


def build_reference(organ_key, ro_organs):
    """Coluna RO. Guarnição: RO não disciplina -> reference None + nota."""
    if organ_key == "guarnicao":
        return None, ("O CBMRO não disciplina a Guarnição de Serviço Operacional na "
                      "LOB/minuta; a proposta baseia-se no CBMSE (RISD).")
    return extract_organ(ro_organs, organ_key), None


def curated_states_for(organ_key, dpo_cot, meta):
    """{state_id: record} da camada curada para um órgão."""
    out = {}

    # 1) DPO/COT: mapa estrutural curado de comparativo_dpo_cot.json
    if organ_key in ("dpo", "cot"):
        for s in dpo_cot["states"]:
            if s["id"] == REF_ID:
                continue
            organs = s.get(organ_key) or []
            note = (s.get("notes") or {}).get(organ_key)
            if not organs and not note:
                continue
            out[s["id"]] = {
                **meta.get(s["id"], _fallback_meta(s["id"])),
                "provenance": "curado", "sourceLabel": None, "note": note,
                "organs": [_strip_organ(o) for o in organs],
            }

    # 2) Competências curadas (ENRICHMENT_ORGAN) pivotadas por fonte
    by_state = {}
    for it in enrich_organ_for(organ_key):
        sid = state_from_source_label(it["source"])
        if not sid or sid == REF_ID:
            continue
        by_state.setdefault(sid, {"items": [], "source": it["source"]})
        by_state[sid]["items"].append(it["text"])
    for sid, info in by_state.items():
        if sid in out:  # já tem estrutura curada -> anexa competências como órgão extra
            out[sid]["organs"].append(competencia_organ(info["items"]))
            if not out[sid].get("sourceLabel"):
                out[sid]["sourceLabel"] = info["source"]
        else:
            out[sid] = {
                **meta.get(sid, _fallback_meta(sid)),
                "provenance": "curado", "sourceLabel": info["source"], "note": None,
                "organs": [competencia_organ(info["items"])],
            }

    # 3) Guarnição: CBMSE (RISD)
    if organ_key == "guarnicao":
        cargos = [{
            "cargo": name, "requisito": "", "subordinadoA": "",
            "atribuicoes": [i["text"] for i in items], "desdobramentos": [],
        } for (name, _caput, items) in GUARNICAO_CHAPTER["cargos"]]
        src = GUARNICAO_CHAPTER["cargos"][0][2][0]["source"] if GUARNICAO_CHAPTER["cargos"] else "cf. CBMSE, RISD"
        out["se"] = {
            **meta.get("se", _fallback_meta("se")),
            "provenance": "curado", "sourceLabel": src, "note": None,
            "organs": [{"name": GUARNICAO_CHAPTER["label"], "abbreviation": "",
                        "subordinadoA": "", "atribuicoes": [], "desdobramentos": [],
                        "cargos": cargos}],
        }

    return out


def _strip_organ(o):
    """Remove campos extras do organ vindo de comparativo_dpo_cot.json."""
    return {
        "name": o.get("name", ""), "abbreviation": o.get("abbreviation", ""),
        "subordinadoA": o.get("subordinadoA", ""),
        "atribuicoes": list(o.get("atribuicoes", [])),
        "desdobramentos": list(o.get("desdobramentos", [])),
        "cargos": [{
            "cargo": c.get("cargo", ""), "requisito": c.get("requisito", ""),
            "subordinadoA": c.get("subordinadoA", ""),
            "atribuicoes": list(c.get("atribuicoes", [])),
            "desdobramentos": list(c.get("desdobramentos", [])),
        } for c in o.get("cargos", [])],
    }


def _fallback_meta(sid):
    return {"id": sid, "name": sid, "abbr": sid.upper(), "cbm": "", "region": ""}


def auto_states_for(organ_key, curated_ids, meta):
    """Camada automática: casa por palavra-chave em organs_detail dos estados não curados."""
    out = {}
    for sid in meta:
        if sid == REF_ID or sid in curated_ids:
            continue
        organs = load_organs(sid)
        ids = auto_match_organ_ids(organ_key, organs)
        matched = [extract_organ(organs, oid) for oid in ids]
        matched = [m for m in matched if m]
        if not matched:
            continue
        out[sid] = {
            **meta[sid], "provenance": "automatico", "sourceLabel": None, "note": None,
            "organs": matched,
        }
    return out


def sort_states(records):
    """Curado primeiro, depois automático; cada grupo alfabético por sigla."""
    return sorted(records, key=lambda r: (r["provenance"] != "curado", r["abbr"]))


def build():
    meta = load_state_meta()
    ro_organs = load_organs(REF_ID)
    dpo_cot = json.loads(DPO_COT_JSON.read_text(encoding="utf-8"))

    organs_out = []
    for organ_key in ORGAN_KEYS:
        reference, ref_note = build_reference(organ_key, ro_organs)
        curated = curated_states_for(organ_key, dpo_cot, meta)
        auto = auto_states_for(organ_key, set(curated.keys()), meta)
        states = sort_states(list(curated.values()) + list(auto.values()))
        ref_abbr = (reference or {}).get("abbreviation") or organ_key.upper()
        organs_out.append({
            "key": organ_key, "title": ORGAN_TITLES.get(organ_key, organ_key.upper()),
            "abbr": ref_abbr, "reference": reference, "referenceNote": ref_note,
            "states": states,
        })
        n_cur = sum(1 for s in states if s["provenance"] == "curado")
        print(f"  ✓ {organ_key:9s}: {len(states):2d} estados ({n_cur} curado, {len(states)-n_cur} auto)")

    rmeta = meta.get(REF_ID, _fallback_meta(REF_ID))
    out = {
        "generated_by": "scripts/build_minuta_comparison.py",
        "reference": {"id": REF_ID, "name": rmeta["name"], "abbr": rmeta["abbr"], "cbm": rmeta["cbm"]},
        "organs": organs_out,
    }
    OUT_JSON.write_text(json.dumps(out, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"\n→ {OUT_JSON.relative_to(BASE_DIR)} ({len(organs_out)} órgãos)")


if __name__ == "__main__":
    print("=" * 60)
    print("Gerando comparativo da minuta (RO × estados, 12 órgãos)")
    print("=" * 60)
    build()
```

- [ ] **Step 2: Run the build script**

Run: `python scripts/build_minuta_comparison.py`
Expected: 12 linhas `✓ <organ>: N estados (...)`; `dpo` e `cot` com ~26 estados; `guarnicao` com 1 (se, curado); termina com `→ database/comparativo_minuta.json (12 órgãos)`.

- [ ] **Step 3: Sanity-check do artefato gerado**

Run:
```bash
node -e "const d=require('./database/comparativo_minuta.json'); console.log('organs', d.organs.length); const g=d.organs.find(o=>o.key==='guarnicao'); const se=g.states.find(s=>s.id==='se'); console.log('guarnicao se cargos', se.organs[0].cargos.map(c=>c.cargo)); const cot=d.organs.find(o=>o.key==='cot'); console.log('cot states', cot.states.length, '| mt curado?', (cot.states.find(s=>s.id==='mt')||{}).provenance);"
```
Expected: `organs 12`; `guarnicao se cargos [ 'Comandante de Guarnição', 'Condutor e Operador de Viatura' ]`; `cot states` ~26 e `mt curado? curado`.

- [ ] **Step 4: Commit**

```bash
git add scripts/build_minuta_comparison.py database/comparativo_minuta.json
git commit -m "feat: build do comparativo da minuta (RO x estados, 12 orgaos, curado+auto)

Co-Authored-By: Claude Opus 4.8 <noreply@anthropic.com>"
```

---

### Task 3: Helpers de render compartilhados (frontend)

**Files:**
- Create: `src/lib/comparatorRender.jsx`

**Interfaces:**
- Produces:
  - `renderFriendlyText(text) -> JSX` — negrita postos/cargos; `—` se vazio.
  - `List({ items }) -> JSX` — `<ul>` ou `—`.
  - `MATRIX_ROWS: Array<{ key, label, render(organ) }>` — 6 linhas (Órgão/Sigla, Subordinação, Cargo/Função, Requisito/Posto, Atribuições, Desdobramentos).

- [ ] **Step 1: Create the module**

Create `src/lib/comparatorRender.jsx`:

```jsx
/* Helpers de render compartilhados pela matriz de comparação (verbatim). */

export function renderFriendlyText(text) {
  if (!text) return <span className="cc-empty">—</span>
  let html = text
  const patterns = [
    { regex: /\b(Oficiais|Oficial superior|Oficiais superiores|Oficial da ativa|Oficiais da ativa|último posto|último Posto|Coronéis|Coronel|Tenente-Coronel|Majores|Major|Capitão|Tenente|Praças|QOEMBM|QCOBM|CCEMBM)\b/gi, replacement: '<strong>$1</strong>' },
    { regex: /\b(Governador do Estado|Governador|Secretário de Estado|Comandante-Geral|Subcomandante-Geral|Chefe do Estado-Maior|Chefe do EMG|Estado-Maior Geral|Subcomandante|Comandante|Diretor-Geral|Diretor|Diretora|Coordenador|Coordenadora)\b/gi, replacement: '<strong>$1</strong>' },
  ]
  patterns.forEach(p => { html = html.replace(p.regex, p.replacement) })
  return <span dangerouslySetInnerHTML={{ __html: html }} />
}

export function List({ items }) {
  if (!items || items.length === 0) return <span className="cc-empty">—</span>
  return <ul className="cc-list">{items.map((it, i) => <li key={i}>{renderFriendlyText(it)}</li>)}</ul>
}

function organAtribuicoes(organ) {
  if (organ.atribuicoes && organ.atribuicoes.length) return organ.atribuicoes
  const out = []
  for (const c of organ.cargos || []) for (const a of c.atribuicoes || []) out.push(a)
  return out
}

export const MATRIX_ROWS = [
  { key: 'organ', label: 'Órgão / Sigla', render: o => (
      <div>
        <div className="oc-organ-name">{renderFriendlyText(o.name || '—')}</div>
        {o.abbreviation && <div className="oc-organ-sub"><span className="oc-organ-abbr">{o.abbreviation}</span></div>}
      </div>
    ) },
  { key: 'subord', label: 'Subordinação', render: o => o.subordinadoA
      ? <span className="oc-sub">{renderFriendlyText(o.subordinadoA)}</span>
      : <span className="cc-empty">—</span> },
  { key: 'cargos', label: 'Cargo / Função', render: o => {
      const names = (o.cargos || []).map(c => c.cargo).filter(Boolean)
      return names.length
        ? <ul className="cc-list">{names.map((n, i) => <li key={i}>{renderFriendlyText(n)}</li>)}</ul>
        : <span className="cc-empty">—</span>
    } },
  { key: 'req', label: 'Requisito / Posto', render: o => {
      const reqs = [...new Set((o.cargos || []).map(c => c.requisito).filter(Boolean))]
      return reqs.length
        ? <ul className="cc-list">{reqs.map((r, i) => <li key={i}>{renderFriendlyText(r)}</li>)}</ul>
        : <span className="cc-empty">—</span>
    } },
  { key: 'atrib', label: 'Atribuições / Competências', render: o => {
      const items = organAtribuicoes(o)
      // inclui atribuições por cargo quando o órgão tem cargos detalhados
      const cargoAtribs = []
      for (const c of o.cargos || []) for (const a of c.atribuicoes || []) cargoAtribs.push(a)
      const all = items.length ? items : cargoAtribs
      return <List items={all} />
    } },
  { key: 'desd', label: 'Desdobramentos', render: o => <List items={o.desdobramentos} /> },
]
```

- [ ] **Step 2: Verify it imports (build)**

Run: `npm run build`
Expected: build conclui sem erro (módulo válido; ainda não importado por ninguém).

- [ ] **Step 3: Commit**

```bash
git add src/lib/comparatorRender.jsx
git commit -m "feat: helpers de render compartilhados da matriz de comparacao

Co-Authored-By: Claude Opus 4.8 <noreply@anthropic.com>"
```

---

### Task 4: Página `MinutaComparator.jsx` + rota `/comparar` + sidebar; remove `Compare.jsx`

**Files:**
- Create: `src/pages/MinutaComparator.jsx`
- Modify: `src/App.jsx`
- Delete: `src/pages/Compare.jsx`

**Interfaces:**
- Consumes: `renderFriendlyText`, `MATRIX_ROWS` de `src/lib/comparatorRender.jsx`; fetch de `/database/comparativo_minuta.json` (Task 2).

- [ ] **Step 1: Create the page**

Create `src/pages/MinutaComparator.jsx`:

```jsx
import { useEffect, useMemo, useState } from 'react'
import { GitCompare, Info, AlertCircle, Search, FileDown, ScrollText } from 'lucide-react'
import { renderFriendlyText, MATRIX_ROWS } from '../lib/comparatorRender.jsx'

function norm(s) {
  return (s || '').normalize('NFKD').replace(/[̀-ͯ]/g, '').toLowerCase()
}

function ProvBadge({ provenance }) {
  const curado = provenance === 'curado'
  return (
    <span style={{
      fontSize: 9, fontWeight: 800, padding: '1px 6px', borderRadius: 99,
      textTransform: 'uppercase', letterSpacing: '0.04em',
      background: curado ? 'rgba(22,163,74,0.12)' : 'rgba(245,166,35,0.16)',
      color: curado ? 'var(--accent-green)' : 'var(--accent-orange)',
    }}>{curado ? 'Curado' : 'Auto'}</span>
  )
}

function Matrix({ organ, states }) {
  const refOrgans = organ.reference ? [organ.reference] : []
  return (
    <div className="cargo-compare-wrapper oc-scroll">
      <table className="cargo-compare-table oc-matrix-table">
        <colgroup>
          <col style={{ width: 150 }} />
          {refOrgans.length === 0 ? <col style={{ minWidth: 240 }} /> : refOrgans.map((_, i) => <col key={i} style={{ minWidth: 240 }} />)}
          {states.map(s => <col key={s.id} style={{ minWidth: 210 }} />)}
        </colgroup>
        <thead>
          <tr>
            <th className="cc-col-label cc-corner">Campo</th>
            <th className="cc-col-ro cc-corner" colSpan={Math.max(refOrgans.length, 1)}>
              <div className="cc-corp-head">
                <span className="cc-corp-abbr ref">RO</span>
                <div>
                  <div className="cc-corp-name">Rondônia</div>
                  <div className="cc-corp-cbm">CBMRO · Referência</div>
                </div>
              </div>
            </th>
            {states.map(s => (
              <th key={s.id}>
                <div className="cc-corp-head" style={{ flexDirection: 'column', alignItems: 'flex-start', gap: 4 }}>
                  <div style={{ display: 'flex', alignItems: 'center', gap: 8 }}>
                    <span className="cc-corp-abbr">{s.abbr}</span>
                    <div>
                      <div className="cc-corp-name">{s.name}</div>
                      <div className="cc-corp-cbm">{s.cbm}</div>
                    </div>
                  </div>
                  <div style={{ display: 'flex', alignItems: 'center', gap: 6 }}>
                    <ProvBadge provenance={s.provenance} />
                    {s.sourceLabel && <span style={{ fontSize: 9.5, color: 'var(--text-muted)' }}>{s.sourceLabel}</span>}
                  </div>
                </div>
              </th>
            ))}
          </tr>
        </thead>
        <tbody>
          {MATRIX_ROWS.map((row, rowIdx) => (
            <tr key={row.key}>
              <td className="cc-col-label">{row.label}</td>
              {refOrgans.length === 0
                ? (rowIdx === 0
                    ? <td className="cc-col-ro cc-ref-cell" rowSpan={MATRIX_ROWS.length} style={{ verticalAlign: 'top' }}>
                        <span style={{ display: 'flex', gap: 5, alignItems: 'flex-start', fontSize: 11.5, fontStyle: 'italic', color: 'var(--text-muted)' }}>
                          <AlertCircle size={13} style={{ flexShrink: 0, marginTop: 2 }} />
                          {organ.referenceNote || 'O CBMRO não discrimina este órgão.'}
                        </span>
                      </td>
                    : null)
                : refOrgans.map((o, i) => <td key={i} className="cc-col-ro cc-ref-cell">{row.render(o)}</td>)
              }
              {states.map(s => (
                <td key={s.id}>
                  {(s.organs || []).length === 0
                    ? <span className="cc-empty">—</span>
                    : s.organs.map((o, i) => <div key={i} style={i > 0 ? { marginTop: 8, paddingTop: 8, borderTop: '1px dashed var(--border-subtle)' } : undefined}>{row.render(o)}</div>)}
                  {row.key === 'organ' && s.note && (
                    <div style={{ marginTop: 6, fontSize: 10.5, color: 'var(--text-muted)', fontStyle: 'italic' }}>{s.note}</div>
                  )}
                </td>
              ))}
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  )
}

export default function MinutaComparator() {
  const [data, setData] = useState(null)
  const [error, setError] = useState(false)
  const [organKey, setOrganKey] = useState(null)
  const [search, setSearch] = useState('')

  useEffect(() => {
    fetch('/database/comparativo_minuta.json')
      .then(r => (r.ok ? r.json() : Promise.reject()))
      .then(d => { setData(d); setOrganKey(d.organs[0]?.key || null) })
      .catch(() => setError(true))
  }, [])

  const organ = useMemo(() => data?.organs.find(o => o.key === organKey) || null, [data, organKey])

  const visibleStates = useMemo(() => {
    if (!organ) return []
    if (!search.trim()) return organ.states
    const q = norm(search)
    return organ.states.filter(s => norm(s.name).includes(q) || norm(s.abbr).includes(q) || norm(s.cbm).includes(q))
  }, [organ, search])

  if (error) {
    return (
      <div className="empty-state" style={{ marginTop: 24 }}>
        <GitCompare size={40} className="empty-state-icon" />
        <h3>Comparativo não encontrado</h3>
        <p>Execute <code>python scripts/build_minuta_comparison.py</code> para gerar os dados.</p>
      </div>
    )
  }
  if (!data) return <div className="empty-state"><div className="spinner" /></div>

  return (
    <>
      <div className="section-bar no-print">
        <div className="section-bar-label">Subsídio à Minuta — CBMRO × demais estados, pela estrutura do Regimento</div>
        <span className="section-bar-badge"><ScrollText size={13} color="var(--cbm-red-700)" />{data.organs.length} órgãos</span>
      </div>

      <div className="page-body">
        <div className="card no-print" style={{ marginBottom: 16 }}>
          <p style={{ fontSize: 13, color: 'var(--text-secondary)', lineHeight: 1.6, margin: 0 }}>
            Compare a legislação do <strong>CBMRO</strong> com a dos demais estados, órgão a órgão, na mesma
            ordem da minuta do Regimento Interno — do topo (DPO/COT) à menor fração (Guarnição de Serviço).
            Colunas marcadas <strong>Curado</strong> trazem texto verbatim atribuído à fonte; <strong>Auto</strong>
            vêm de extração automática e podem ser rasas. Só aparecem estados com dado para o órgão.
          </p>
        </div>

        <div style={{ display: 'flex', gap: 16, alignItems: 'flex-start' }}>
          {/* Sumário de órgãos */}
          <aside className="no-print" style={{ flex: '0 0 230px', position: 'sticky', top: 12 }}>
            <div className="card" style={{ padding: 8 }}>
              <div className="nav-section-label" style={{ padding: '6px 8px' }}>Órgãos da minuta</div>
              {data.organs.map(o => (
                <button
                  key={o.key}
                  onClick={() => setOrganKey(o.key)}
                  className={`nav-item${o.key === organKey ? ' active' : ''}`}
                  style={{ width: '100%', textAlign: 'left', border: 'none', cursor: 'pointer', fontSize: 12.5 }}
                  title={o.title}
                >
                  {o.abbr} <span style={{ opacity: 0.6, fontSize: 10, marginLeft: 4 }}>{o.states.length}</span>
                </button>
              ))}
            </div>
          </aside>

          {/* Conteúdo do órgão */}
          <div style={{ flex: 1, minWidth: 0 }}>
            {organ && (
              <>
                <div className="oc-group-desc no-print" style={{ marginBottom: 12 }}>
                  <Info size={14} style={{ flexShrink: 0, marginTop: 2 }} color="var(--accent-blue)" />
                  <span><strong>{organ.title}</strong></span>
                </div>

                <div className="oc-toolbar no-print" style={{ marginBottom: 12 }}>
                  <div className="search-input-wrap" style={{ maxWidth: 280 }}>
                    <Search size={14} className="search-input-icon" />
                    <input
                      type="text" className="search-input" placeholder="Buscar estado / CBM..."
                      value={search} onChange={e => setSearch(e.target.value)}
                      style={{ height: 36, paddingLeft: 34, fontSize: 13 }}
                    />
                  </div>
                  <button className="btn btn-ghost" onClick={() => window.print()}>
                    <FileDown size={15} /> Exportar PDF
                  </button>
                </div>

                <div className="print-only-title" style={{ display: 'none' }}>{organ.title}</div>

                {visibleStates.length === 0 && organ.reference == null
                  ? <div className="card" style={{ padding: 30, textAlign: 'center', color: 'var(--text-muted)' }}>Nenhum estado com dado para este órgão.</div>
                  : <Matrix organ={organ} states={visibleStates} />}
              </>
            )}
          </div>
        </div>
      </div>
    </>
  )
}
```

- [ ] **Step 2: Wire route + sidebar in `App.jsx`, remove Compare**

In `src/App.jsx`: replace the `Compare` import with the new page, and update the NAV label.

Replace line `import Compare from './pages/Compare.jsx'` with:
```jsx
import MinutaComparator from './pages/MinutaComparator.jsx'
```

Replace the NAV entry
```jsx
  { to: '/comparar', icon: GitCompare, label: 'Comparativo' },
```
with
```jsx
  { to: '/comparar', icon: GitCompare, label: 'Subsídio à Minuta' },
```

Replace the route
```jsx
          <Route path="/comparar" element={<Compare />} />
```
with
```jsx
          <Route path="/comparar" element={<MinutaComparator />} />
```

- [ ] **Step 3: Delete the old page**

```bash
git rm src/pages/Compare.jsx
```

- [ ] **Step 4: Verify build + dev server**

Run: `npm run build`
Expected: build sem erros, sem referências a `Compare.jsx`.

Then run the dev server and open the page:
Run: `npm run dev -- --port 5173 --strictPort`
Open: http://localhost:5173/comparar
Expected: sumário de órgãos à esquerda; DPO selecionado por padrão com matriz RO + estados; trocar para "guarnicao" mostra coluna RO com a nota e a coluna SE com Comandante de Guarnição (atribuições verbatim); busca filtra colunas; badges Curado/Auto aparecem.

- [ ] **Step 5: Commit**

```bash
git add src/pages/MinutaComparator.jsx src/App.jsx
git commit -m "feat: pagina Subsidio a Minuta em /comparar; remove Compare.jsx

Co-Authored-By: Claude Opus 4.8 <noreply@anthropic.com>"
```

---

### Task 5: Limpa Dashboard (remove abas) e componentes mortos; PDF; docs

**Files:**
- Modify: `src/pages/Dashboard.jsx`
- Modify: `src/index.css` (regras `@media print` da nova página)
- Delete: `src/components/CargoComparator.jsx`, `src/components/OrgaosOperacionaisComparator.jsx`
- Modify: `CLAUDE.md`

**Interfaces:**
- Consumes: nada novo. Remove consumidores de `CargoComparator`/`OrgaosOperacionaisComparator`.

- [ ] **Step 1: Remove as abas do Dashboard**

In `src/pages/Dashboard.jsx`:

Remove os imports:
```jsx
import CargoComparator from '../components/CargoComparator.jsx'
import OrgaosOperacionaisComparator from '../components/OrgaosOperacionaisComparator.jsx'
```

Remove o estado `const [activeTab, setActiveTab] = useState('overview')` e o bloco inteiro `<div className="tabs">…</div>` (as três abas), além das renderizações condicionais `{activeTab === 'cargos' && …}` e `{activeTab === 'orgaos' && …}`.

Desembrulhe o conteúdo de `{activeTab === 'overview' && (<>…</>)}` para ficar sempre visível (remova o wrapper condicional, mantendo o conteúdo interno e o fechamento `</div>` do `page-body`).

Remova de `lucide-react` os ícones que ficaram sem uso (`Users`, `Building2`, `LayoutDashboard`) — confira se não são usados em outro ponto do arquivo antes de remover.

- [ ] **Step 2: Verify Dashboard build**

Run: `npm run build`
Expected: build sem erros; nenhuma referência a `CargoComparator`/`OrgaosOperacionaisComparator`.

- [ ] **Step 3: Delete dead components**

```bash
git rm src/components/CargoComparator.jsx src/components/OrgaosOperacionaisComparator.jsx
```

Run: `npm run build`
Expected: build sem erros (confirma que nada mais importa os componentes removidos).

- [ ] **Step 4: Add print rules para a nova página**

In `src/index.css`, ao final do arquivo, adicione:

```css
/* ── Impressão do comparador "Subsídio à Minuta" ── */
@media print {
  .print-only-title { display: block !important; font-family: 'Outfit', sans-serif;
    font-size: 16pt; font-weight: 800; text-align: center; margin: 0 0 12px; color: #000; }
  .oc-matrix-table { font-size: 8.5pt; }
  .page-body { display: block !important; }
}
```

- [ ] **Step 5: Verify PDF (impressão)**

Run dev server (se não estiver no ar): `npm run dev -- --port 5173 --strictPort`
Open: http://localhost:5173/comparar — selecione um órgão, clique **Exportar PDF** (ou Ctrl+P).
Expected: a barra de controles e o sumário somem na pré-visualização de impressão; aparece o título do órgão centralizado e a matriz; imprimir em Paisagem.

- [ ] **Step 6: Update CLAUDE.md**

In `CLAUDE.md`, na seção de comandos de regeneração de dados, adicione após a linha do `build_dpo_cot_comparison.py`:

```bash
python scripts/build_minuta_comparison.py    # organs_detail/*.json + comparativo_dpo_cot.json + minuta_enrichment.py -> database/comparativo_minuta.json (página /comparar "Subsídio à Minuta")
```

Na seção do **Frontend**, atualize a descrição das rotas e do Dashboard: remova a menção às abas "Comparativo de Cargos" e "DPO × COT" do Dashboard; registre que `/comparar` agora é a página **"Subsídio à Minuta"** (`MinutaComparator.jsx`), que lê `database/comparativo_minuta.json`, espelha os 12 órgãos da minuta e compara RO × estados em matriz, com proveniência curado/automático; observe que `Compare.jsx`, `CargoComparator.jsx` e `OrgaosOperacionaisComparator.jsx` foram removidos. Mantenha a nota de ORDEM IMPORTA: `build_minuta_comparison.py` depende de `build_dpo_cot_comparison.py` e `build_organs_detail.py`.

- [ ] **Step 7: Commit**

```bash
git add src/pages/Dashboard.jsx src/index.css CLAUDE.md
git commit -m "refactor: remove abas do Dashboard e componentes antigos; PDF + docs do novo comparador

Co-Authored-By: Claude Opus 4.8 <noreply@anthropic.com>"
```

---

## Self-Review

**Spec coverage:**
- Página única espelhando a minuta → Task 4 (sumário dos 12 órgãos).
- Só onde há dado → Task 2 (estados sem match não entram) + Task 4 (busca filtra).
- Matriz campos×estados, RO sticky → Task 3 (MATRIX_ROWS) + Task 4 (Matrix).
- Fonte híbrida (curado + automático) com proveniência → Task 2 (camadas) + Task 4 (ProvBadge).
- RO puro de ro.json → Task 2 (`extract_organ(ro_organs, ...)`).
- Guarnição (CBMSE) até Comandante de Guarnição → Task 2 (`curated_states_for` guarnicao) + Task 4 (nota na coluna RO).
- DPO/COT curados → Task 2 (mapa de comparativo_dpo_cot.json).
- Remove região/similaridade, mantém busca → Task 4 (só busca).
- Remove Compare.jsx + abas do Dashboard → Task 4 + Task 5.
- PDF preservado → Task 5 (print rules + window.print).
- Novo artefato/pipeline → Task 2; docs → Task 5.

**Placeholder scan:** sem TBD/TODO; todo passo de código traz o código completo.

**Type consistency:** `comparativo_minuta.json` (Task 2) define `organs[].{key,title,abbr,reference,referenceNote,states}` e `states[].{id,name,abbr,cbm,region,provenance,sourceLabel,note,organs}`; consumido exatamente assim em Task 4. `MATRIX_ROWS[].render(organ)` recebe um objeto com `name/abbreviation/subordinadoA/cargos/atribuicoes/desdobramentos` — o mesmo shape produzido por `extract_organ`/`competencia_organ`/`_strip_organ` em Task 2. Helpers `renderFriendlyText`/`MATRIX_ROWS` exportados em Task 3, importados em Task 4.
