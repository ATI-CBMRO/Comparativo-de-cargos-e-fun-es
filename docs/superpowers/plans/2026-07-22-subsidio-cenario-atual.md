# Subsídio no cenário LOB atual — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) ou superpowers:executing-plans. Steps use checkbox (`- [ ]`) syntax.

**Goal:** Destravar `/minuta/subsidio` e `/regulamento/subsidio` no cenário LOB atual: gerador isolado `build_minuta_comparison_atual.py` (camada automática rotulada) + telas resolvendo dados por `scenarioDbUrl` + selo "correspondência automática".

**Architecture:** Gerador novo que NÃO importa nada da trilha da futura (isolamento por arquivo); telas trocam caminhos fixos `/database/...` por `scenarioDbUrl(cenario, ...)`; gate `TrilhaRoute` sai só das 2 rotas de Subsídio. Cenário futura fica byte a byte intocado.

**Tech Stack:** Python 3 (`.venv-pipeline/bin/python`), React/Vite, `node --test`.

## Global Constraints

- Spec: `docs/superpowers/specs/2026-07-22-subsidio-cenario-atual-design.md` (ler antes).
- **PROIBIDO** no gerador do atual: `import` de `minuta_enrichment`, `lob_enrichment`, `build_minuta_structure`, `build_minuta_comparison`. Permitido: `minuta_comparison_lib` (só `norm`).
- JSON do atual: toda `provenance` == `"automatico"`; nenhum rótulo `cf. CBM..` de camada curada; 21 órgãos na ordem dos capítulos de `database/atual/minuta_structure.json`.
- Cenário futura intocado: `database/comparativo_minuta.json` e telas no cenário futura sem mudança de comportamento; diff não toca `database/` da raiz.
- Selo no cenário atual (RI): texto exato **"Correspondência automática — sujeita a revisão."**
- `node --test` completo verde ao final de cada task (114 pré-existentes + novos).
- Nada de pip no Python do sistema; usar `.venv-pipeline/bin/python`.
- Trabalhar na branch `feat/subsidio-cenario-atual` (já criada).

---

### Task 1: Gerador `build_minuta_comparison_atual.py` + teste

**Files:**
- Create: `scripts/build_minuta_comparison_atual.py`
- Create: `scripts/test_minuta_comparison_atual.py`
- Gera: `database/atual/comparativo_minuta.json`

**Interfaces:**
- Consome: `database/atual/organs_detail/ro.json` (21 órgãos), `database/atual/minuta_structure.json` (ordem/títulos/commandChart), `database/organs_detail/<id>.json` (27 estados, compartilhado), `database/states_data.json` (metadados), `scripts/minuta_comparison_lib.py` (`norm`).
- Produz: `database/atual/comparativo_minuta.json` no MESMO shape do da futura: topo `{generated_by, scenario:"atual", reference:{id,name,abbr,cbm}, organs:[...]}`; cada organ `{key,title,abbr,depth,reference,referenceNote:null,states:[...]}`; cada state `{id,name,abbr,cbm,region,provenance:"automatico",sourceLabel:null,note:null,organs,riOrgans,riProvenance:"automatico",riSourceLabel:null,lobOrgans,lobProvenance:"automatico"|null}`.

- [ ] **Step 1: Escrever o teste (falhando)** — `scripts/test_minuta_comparison_atual.py`:

```python
"""Valida database/atual/comparativo_minuta.json (gerado por build_minuta_comparison_atual)."""
import json
import re
import sys
from pathlib import Path

BASE = Path(__file__).parent.parent
OUT = BASE / "database" / "atual" / "comparativo_minuta.json"
STRUCT = BASE / "database" / "atual" / "minuta_structure.json"

# Rótulos que só existem na camada CURADA da futura — presença aqui = vazamento.
FORBIDDEN = re.compile(r"cf\. CBM(MT|PA|DF|AL|GO|SE)\b")

def main():
    errors = []
    data = json.loads(OUT.read_text(encoding="utf-8"))
    struct = json.loads(STRUCT.read_text(encoding="utf-8"))
    expected_keys = [c["id"].split(":")[-1] for c in struct["chapters"]]

    if data.get("scenario") != "atual":
        errors.append("topo: scenario != 'atual'")
    got_keys = [o["key"] for o in data.get("organs", [])]
    if got_keys != expected_keys:
        errors.append(f"ordem/chaves != capítulos do atual: {got_keys} vs {expected_keys}")
    if len(got_keys) != 21:
        errors.append(f"esperava 21 órgãos, veio {len(got_keys)}")

    raw = OUT.read_text(encoding="utf-8")
    m = FORBIDDEN.search(raw)
    if m:
        errors.append(f"vazamento de fonte curada da futura: '{m.group(0)}' presente no JSON do atual")

    for o in data.get("organs", []):
        if not o.get("reference"):
            errors.append(f"{o['key']}: reference (coluna RO) vazio")
        for s in o.get("states", []):
            if s.get("provenance") != "automatico":
                errors.append(f"{o['key']}/{s.get('id')}: provenance '{s.get('provenance')}' != automatico")
            if s.get("id") == "ro":
                errors.append(f"{o['key']}: RO não pode aparecer como estado comparado")
            for col in ("organs", "riOrgans", "lobOrgans"):
                if col not in s:
                    errors.append(f"{o['key']}/{s.get('id')}: coluna '{col}' ausente")

    if errors:
        print("FALHOU:")
        for e in errors[:30]:
            print(" -", e)
        sys.exit(1)
    n_states = sum(len(o["states"]) for o in data["organs"])
    print(f"OK — 21 órgãos na ordem do atual, {n_states} registros de estado, tudo 'automatico', sem vazamento.")

if __name__ == "__main__":
    main()
```

- [ ] **Step 2: Rodar e ver falhar** — `.venv-pipeline/bin/python scripts/test_minuta_comparison_atual.py` → FAIL (FileNotFoundError: comparativo do atual não existe).

- [ ] **Step 3: Implementar o gerador** — `scripts/build_minuta_comparison_atual.py`:

```python
"""
build_minuta_comparison_atual.py — Portal CBM (cenário LOB ATUAL, Lei nº 2.204/2009)

Gera database/atual/comparativo_minuta.json: os 21 órgãos do CBMRO vigente × demais
estados, SÓ com a camada 'automatico' (casamento por palavra-chave no organs_detail
compartilhado). Decisão de produto 2026-07-22: sem curadoria manual nesta fatia; a
tela rotula tudo como correspondência automática.

ISOLAMENTO (armadilha documentada no CLAUDE.md): este script NÃO importa
minuta_enrichment, lob_enrichment, build_minuta_structure nem build_minuta_comparison
— qualquer um deles traria conteúdo da LOB futura para o cenário atual.

Rodar: .venv-pipeline/bin/python scripts/build_minuta_comparison_atual.py
Valida: .venv-pipeline/bin/python scripts/test_minuta_comparison_atual.py
"""
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from minuta_comparison_lib import norm  # noqa: E402  (única importação permitida da lib)

BASE_DIR = Path(__file__).parent.parent
ATUAL_DIR = BASE_DIR / "database" / "atual"
DET_DIR = BASE_DIR / "database" / "organs_detail"          # acervo dos 27 (compartilhado)
RO_ATUAL_JSON = ATUAL_DIR / "organs_detail" / "ro.json"     # 21 órgãos vigentes
STRUCT_JSON = ATUAL_DIR / "minuta_structure.json"
STATES_JSON = BASE_DIR / "database" / "states_data.json"
OUT_JSON = ATUAL_DIR / "comparativo_minuta.json"

REF_ID = "ro"

# Palavras-chave POR ÓRGÃO DO ATUAL (chaves da Lei 2.204/2009 — a tabela da lib usa as
# chaves da futura e não serve aqui). include/exclude já normalizados (sem acento).
AUTO_MATCH_KEYWORDS_ATUAL = {
    "cg":           {"include": ["comando geral", "comando-geral"],
                     "exclude": ["regional", "operacoes", "setorial", "secao"]},
    "emg":          {"include": ["estado maior", "estado-maior"], "exclude": ["regional"]},
    "corregedoria": {"include": ["corregedoria", "correicao"], "exclude": []},
    "ajudancia":    {"include": ["ajudancia", "ajudante-geral", "ajudante geral"], "exclude": []},
    "gabinete":     {"include": ["gabinete"],
                     "exclude": ["subcomando", "subcomandante", "chefia de gabinete"]},
    "cepdec":       {"include": ["defesa civil", "protecao e defesa"], "exclude": []},
    "condeg":       {"include": ["conselho"], "exclude": ["municipal", "regional"]},
    "dint":         {"include": ["inteligencia"], "exclude": []},
    "cpof":         {"include": ["financas", "orcamento", "administracao financeira"],
                     "exclude": ["planejamento operacional"]},
    "assessorias":  {"include": ["assessoria"],
                     "exclude": ["assessoria de comunicacao", "comunicacao social",
                                 "inteligencia", "defesa civil"]},
    "comissoes":    {"include": ["comissao"], "exclude": ["promocao"]},
    "dp":           {"include": ["diretoria de pessoal", "departamento de pessoal",
                                 "gestao de pessoal", "gestao de pessoas", "recursos humanos"],
                     "exclude": ["assistencia ao pessoal", "saude"]},
    "deei":         {"include": ["ensino", "instrucao", "academia"], "exclude": ["defesa civil"]},
    "cat":          {"include": ["atividades tecnicas", "atividade tecnica"],
                     "exclude": ["operacoes tecnicas", "comando de operacoes"]},
    "dlog":         {"include": ["logistica", "apoio logistico", "material e patrimonio",
                                 "materiais e servicos", "suprimento"], "exclude": []},
    "dcs":          {"include": ["comunicacao social"], "exclude": []},
    "dinf":         {"include": ["informatica", "tecnologia da informacao"], "exclude": []},
    "cob1":         {"include": ["comando operacional", "comando de operacoes",
                                 "coordenadoria operacional"],
                     "exclude": ["aerea", "aereo", "aviacao", "atividades tecnicas"]},
    "cob2":         {"include": ["regional", "regiao de bombeiro"], "exclude": []},
    "coa":          {"include": ["aerea", "aereo", "aviacao", "operacoes aereas"], "exclude": []},
    "gbs":          {"include": ["busca", "salvamento"], "exclude": []},
}


def match_ids(organ_key, organs):
    spec = AUTO_MATCH_KEYWORDS_ATUAL.get(organ_key)
    if not spec:
        return []
    inc, exc = spec["include"], spec["exclude"]
    return [oid for oid, o in organs.items()
            if any(k in norm(o.get("name", "")) for k in inc)
            and not any(k in norm(o.get("name", "")) for k in exc)]


def extract_organ(organs, oid):
    o = organs.get(oid)
    if not o:
        return None
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


def load_state_meta():
    data = json.loads(STATES_JSON.read_text(encoding="utf-8"))
    return {s["id"]: {
        "id": s["id"], "name": s.get("name", s["id"]),
        "abbr": s.get("abbreviation", s["id"].upper()),
        "cbm": s.get("cbm_abbreviation", ""), "region": s.get("region", ""),
    } for s in data.get("states", [])}


def depth_map(chart):
    """{organKey: profundidade} a partir do commandChart do atual (dict raiz)."""
    out = {}
    def walk(node, d):
        out[node.get("organKey")] = d
        for ch in node.get("children", []) or []:
            walk(ch, d + 1)
    walk(chart, 0)
    return out


def build():
    struct = json.loads(STRUCT_JSON.read_text(encoding="utf-8"))
    ro_organs = json.loads(RO_ATUAL_JSON.read_text(encoding="utf-8")).get("organs", {})
    meta = load_state_meta()
    depths = depth_map(struct.get("commandChart") or {})

    organs_out = []
    for ch in struct["chapters"]:
        key = ch["id"].split(":")[-1]
        reference = extract_organ(ro_organs, key)
        states = []
        for sid in sorted(meta):
            if sid == REF_ID:
                continue
            p = DET_DIR / f"{sid}.json"
            if not p.exists():
                continue
            all_organs = json.loads(p.read_text(encoding="utf-8")).get("organs", {})
            lobbed = {oid: o for oid, o in all_organs.items() if o.get("source") == "lob"}
            non_lob = {oid: o for oid, o in all_organs.items() if o.get("source") != "lob"}
            lob_pool = lobbed if lobbed else all_organs  # regra da futura, copiada (não importada)
            ri = [extract_organ(non_lob, oid) for oid in match_ids(key, non_lob)]
            ri = [m for m in ri if m]
            lob = [extract_organ(lob_pool, oid) for oid in match_ids(key, lob_pool)]
            lob = [m for m in lob if m]
            if not ri and not lob:
                continue
            states.append({
                **meta[sid],
                "provenance": "automatico", "sourceLabel": None, "note": None,
                "organs": ri, "riOrgans": ri,
                "riProvenance": "automatico" if ri else None, "riSourceLabel": None,
                "lobOrgans": lob, "lobProvenance": "automatico" if lob else None,
            })
        states.sort(key=lambda s: s["name"])
        organs_out.append({
            "key": key,
            "title": ch.get("chapterTitle", key.upper()),
            "abbr": (reference or {}).get("abbreviation") or key.upper(),
            "depth": depths.get(key, 1),
            "reference": reference, "referenceNote": None,
            "states": states,
        })
        print(f"  ✓ {key:12s}: {len(states):2d} estados (automatico)")

    rmeta = meta.get(REF_ID, {"name": "Rondônia", "abbr": "RO", "cbm": "CBMRO"})
    out = {
        "generated_by": "scripts/build_minuta_comparison_atual.py",
        "scenario": "atual",
        "reference": {"id": REF_ID, "name": rmeta["name"], "abbr": rmeta["abbr"], "cbm": rmeta["cbm"]},
        "organs": organs_out,
    }
    OUT_JSON.write_text(json.dumps(out, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Gerado: {OUT_JSON} ({len(organs_out)} órgãos)")


if __name__ == "__main__":
    build()
```

- [ ] **Step 4: Gerar e validar** — rodar o gerador e depois o teste:

```bash
.venv-pipeline/bin/python scripts/build_minuta_comparison_atual.py
.venv-pipeline/bin/python scripts/test_minuta_comparison_atual.py
```
Expected: `OK — 21 órgãos na ordem do atual, ... registros de estado, tudo 'automatico', sem vazamento.`

- [ ] **Step 5: Prova de isolamento e não-regressão** — conferir imports proibidos e diff:

```bash
grep -nE "import (minuta_enrichment|lob_enrichment|build_minuta_structure|build_minuta_comparison)|from (minuta_enrichment|lob_enrichment|build_minuta_structure|build_minuta_comparison)" scripts/build_minuta_comparison_atual.py; echo "exit=$? (1 = nenhum import proibido)"
git status --porcelain database/ | grep -v "^?? database/atual/" ; echo "exit=$? (1 = nada da futura tocado)"
node --test 2>&1 | grep -E "^ℹ (tests|pass|fail)"
```
Expected: nenhum import proibido; nada fora de `database/atual/` alterado; 114/114.

- [ ] **Step 6: Commit**

```bash
git add scripts/build_minuta_comparison_atual.py scripts/test_minuta_comparison_atual.py database/atual/comparativo_minuta.json
git commit -m "feat(atual): gera comparativo_minuta do cenário atual (camada automática, isolado da futura)"
```

### Task 2: Telas por cenário + selo + gate

**Files:**
- Modify: `src/lib/riComparison.js:24-27` (organKeyOfChapter aceita prefixo `atual:`)
- Modify: `src/lib/riComparison.test.js` (2 casos novos)
- Modify: `src/pages/MinutaComparator.jsx:~175` (fetch por cenário + selo)
- Modify: `src/pages/RISubsidioComparativo.jsx:~94-95` (fetches por cenário + selo)
- Modify: `src/pages/RegulamentoComparator.jsx:~43` (fetch por cenário; sem selo)
- Modify: `src/App.jsx:283,288` (remover TrilhaRoute só dessas 2 rotas)

**Interfaces:**
- Consumes: `scenarioDbUrl(cenario, name)` de `src/lib/scenario.js`; `useScenario()` de `src/context/ScenarioContext.jsx` → `{ cenario }`; `database/atual/comparativo_minuta.json` da Task 1.
- Produces: telas funcionais nos 2 cenários; contrato do selo: texto exato "Correspondência automática — sujeita a revisão." renderizado apenas quando `cenario === 'atual'`.

- [ ] **Step 1: Teste da lib (falhando)** — em `src/lib/riComparison.test.js`, adicionar:

```js
test('organKeyOfChapter aceita ids do cenário atual (atual:organ:<key>)', () => {
  assert.equal(organKeyOfChapter('atual:organ:cg'), 'cg')
  assert.equal(organKeyOfChapter('atual:organ:cepdec'), 'cepdec')
})
```

- [ ] **Step 2: Rodar e ver falhar** — `node --test src/lib/riComparison.test.js` → FAIL (retorna null).

- [ ] **Step 3: Corrigir `organKeyOfChapter`** em `src/lib/riComparison.js`:

```js
export function organKeyOfChapter(chapterId) {
  // Ids do cenário atual vêm prefixados ("atual:organ:cg") — remove o marcador de
  // cenário antes de extrair a chave, sem afetar os ids da futura ("organ:cg").
  const id = String(chapterId ?? '').replace(/^atual:/, '')
  return id.startsWith(ORGAN_PREFIX) ? id.slice(ORGAN_PREFIX.length) : null
}
```

- [ ] **Step 4: Rodar e ver passar** — `node --test src/lib/riComparison.test.js` → PASS.

- [ ] **Step 5: Ligar as 3 telas ao cenário.** Em cada arquivo, importar
`import { useScenario } from '../context/ScenarioContext'` e
`import { scenarioDbUrl } from '../lib/scenario.js'`, obter `const { cenario } = useScenario()` no componente e trocar:
  - `MinutaComparator.jsx`: `fetchJson('/database/comparativo_minuta.json')` → `` fetchJson(`/${scenarioDbUrl(cenario, 'comparativo_minuta.json')}`) `` — CONFERIR a assinatura real de `scenarioDbUrl` em `src/lib/scenario.js` (se já devolve o caminho completo com `/database/...`, usar direto, sem remontar); incluir `cenario` no array de dependências do efeito que faz o fetch, para trocar de dados ao virar a chave.
  - `RISubsidioComparativo.jsx`: os dois `fetchJson('/database/minuta_structure.json')` e `fetchJson('/database/comparativo_minuta.json')` idem, com `cenario` nas dependências.
  - `RegulamentoComparator.jsx`: `fetchJson('/database/regulamento_structure.json')` idem.

- [ ] **Step 6: Selo do automático.** Em `MinutaComparator.jsx` e `RISubsidioComparativo.jsx`, logo acima do painel/coluna de estados, renderizar apenas quando `cenario === 'atual'`:

```jsx
{cenario === 'atual' && (
  <p className="muted-note" style={{ margin: '4px 0 10px', fontStyle: 'italic' }}>
    ⚠ Correspondência automática — sujeita a revisão.
  </p>
)}
```
(Se a classe `muted-note` não existir no index.css, usar apenas o style inline — não criar classe nova.)

- [ ] **Step 7: Destravar as 2 rotas** em `src/App.jsx` (linhas 283 e 288):

```jsx
<Route path="/minuta/subsidio" element={<RISubsidio />} />
...
<Route path="/regulamento/subsidio" element={<RegSubsidio />} />
```
As DEMAIS rotas com `TrilhaRoute` (293-298) ficam como estão.

- [ ] **Step 8: Suíte + smoke.** `node --test` completo (114 + 1 novo = 115, 0 fail). Subir `npm run dev` e conferir com curl que `/database/atual/comparativo_minuta.json` responde 200.

- [ ] **Step 9: Commit**

```bash
git add src/lib/riComparison.js src/lib/riComparison.test.js src/pages/MinutaComparator.jsx src/pages/RISubsidioComparativo.jsx src/pages/RegulamentoComparator.jsx src/App.jsx
git commit -m "feat(atual): destrava Subsídio no cenário atual (dados por cenário + selo de correspondência automática)"
```

### Task 3: Prova real nos 2 cenários + documentação

**Files:**
- Modify: `CLAUDE.md` (seção "Cenários LOB": Subsídio sai da lista "ainda gated"; citar o gerador novo no bloco de geradores do atual)
- Modify: `.claude/PENDENCIAS.md` (item "Cenário atual — Subsídio" → Concluído)

- [ ] **Step 1: Prova visual.** Com `npm run dev` no ar e sessão logada (o portal exige login real — sem conta de teste; se a sessão do navegador Playwright não estiver logada, PARAR e pedir ao Wândrio para logar uma vez na janela aberta):
  - Screenshot A: `/minuta/subsidio?cenario=atual` (21 capítulos + selo visível).
  - Screenshot B: `/regulamento/subsidio?cenario=atual` (16 temas, sem "Em construção").
  - Screenshot C: `/minuta/subsidio?cenario=futura` — comparar com o comportamento atual de produção (dados curados, SEM selo).
  - Abrir os screenshots no Preview (`open`).
- [ ] **Step 2: Prova de preservação.** `git diff master --stat -- database/ | grep -v atual` vazio (nada da futura mudou) e colar a saída no relatório.
- [ ] **Step 3: Atualizar CLAUDE.md e PENDENCIAS conforme acima; commit.**

```bash
git add CLAUDE.md .claude/PENDENCIAS.md
git commit -m "docs: Subsídio destravado no cenário atual (CLAUDE.md + pendências)"
```
