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
