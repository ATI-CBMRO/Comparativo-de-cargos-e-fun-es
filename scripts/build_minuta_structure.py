"""
build_minuta_structure.py — Portal CBM

Gera database/minuta_structure.json com estrutura de 5 seções por órgão
(DPO e COT), texto proposto mesclado dos 27 CBMs e lista de fontes.

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
    {"id": "subordinacao",       "title": "Denominação e Subordinação"},
    {"id": "finalidade",         "title": "Finalidade"},
    {"id": "competencias",       "title": "Competências"},
    {"id": "organizacao",        "title": "Organização Interna"},
    {"id": "cargos_atribuicoes", "title": "Atribuições dos Cargos"},
]

ORGAN_LABELS = {
    "dpo": "Diretoria de Planejamento Operacional",
    "cot": "Comando de Operações Técnicas",
}


def normalize(text: str) -> str:
    text = re.sub(r"^\s*[\dIVXivx]+[.)]\s*", "", text.strip())
    return text.strip().lower()


def _ascii_lower(s: str) -> str:
    """Minúsculas sem acentos, para casamento tolerante."""
    return "".join(
        c for c in unicodedata.normalize("NFD", s)
        if unicodedata.category(c) != "Mn"
    ).lower()


# Marcadores de texto VERBATIM de legislação alheia: qualquer dígito (artigo,
# lei, parágrafo, data) ou palavra de citação legal. Itens com esses marcadores
# carregam referências de OUTRO estado e não devem entrar na minuta do CBMRO.
_LEGAL_MARKERS = re.compile(r"\d|§|\bart\b|\blei\b|\blc\b|\bdecreto\b|red\.")


def _other_state_tokens(all_states: list) -> set:
    """Nomes (sem acento, minúsculos) dos estados que NÃO são Rondônia.
    Exclui 'para' (Pará) por colidir com a preposição homônima — itens que
    citam o Pará carregam citação legal e já são barrados por _LEGAL_MARKERS."""
    toks = set()
    for s in all_states:
        if s.get("id") == "ro":
            continue
        nm = _ascii_lower(s.get("name", "")).strip()
        if nm and nm != "para":
            toks.add(nm)
    return toks


def is_generic_competencia(text: str, other_state_names: set) -> bool:
    """True quando a competência é genérica o bastante para qualquer CBM:
    sem citação legal (artigo/lei/§/número), sem fragmento de enumeração
    verbatim (inciso romano, alínea), sem sigla de CBM ou nome de outro estado."""
    low = _ascii_lower(text)
    if _LEGAL_MARKERS.search(low):
        return False
    # Fragmento verbatim de artigo: começa com inciso romano ("I -", "VII -")
    if re.match(r"^[ivxlcdm]+\s*[-–.)]", low):
        return False
    # Citação por alínea ou artigo entre parênteses
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


# ── Extratores por seção ──

def extract_subordinacao(organs: list, state: dict) -> str:
    if not organs:
        return ""
    o = organs[0]
    name  = o.get("name", "")
    abbr  = o.get("abbreviation", "")
    sub   = o.get("subordinadoA", "")
    base  = o.get("baseLegal", "")
    ref   = o.get("legalRef", "")
    parts = []
    if name and abbr:
        parts.append(f"{name} ({abbr})")
    elif name:
        parts.append(f"{name}")
    if sub:
        parts.append(f"é subordinado(a) a {sub}")
    if ref and base:
        parts.append(f"conforme {ref} de {base}")
    elif base:
        parts.append(f"conforme {base}")
    return (", ".join(parts) + ".") if parts else ""


def extract_finalidade(organs: list, _state: dict) -> str:
    # In this dataset the first atribuição is always the organ's purpose statement
    for o in organs:
        for a in (o.get("atribuicoes") or []):
            if a.strip():
                return a.strip()
    return ""


def extract_competencias(organs: list, _state: dict) -> str:
    seen, items = set(), []
    for o in organs:
        for a in (o.get("atribuicoes") or []):
            key = normalize(a)
            if key and key not in seen:
                seen.add(key)
                items.append(a.strip())
    if not items:
        return ""
    return "\n".join(f"{i+1}. {item}" for i, item in enumerate(items))


def extract_organizacao(organs: list, _state: dict) -> str:
    for o in organs:
        desdb = o.get("desdobramentos") or []
        if desdb:
            return "\n".join(f"- {d}" for d in desdb)
    return ""


def extract_cargos_atribuicoes(organs: list, _state: dict) -> str:
    seen_cargos, blocks = set(), []
    for o in organs:
        for c in (o.get("cargos") or []):
            cargo_name = (c.get("cargo") or "").strip()
            if not cargo_name or cargo_name.lower() in seen_cargos:
                continue
            seen_cargos.add(cargo_name.lower())
            atrib = c.get("atribuicoes") or []
            if not atrib:
                continue
            lines = [f"{cargo_name}:"]
            for i, a in enumerate(atrib, 1):
                lines.append(f"  {i}. {a.strip()}")
            blocks.append("\n".join(lines))
    return "\n\n".join(blocks)


EXTRACTORS = {
    "subordinacao":       extract_subordinacao,
    "finalidade":         extract_finalidade,
    "competencias":       extract_competencias,
    "organizacao":        extract_organizacao,
    "cargos_atribuicoes": extract_cargos_atribuicoes,
}


def build_section(section_id: str, all_states: list, group_key: str) -> dict:
    title = next(s["title"] for s in SECTIONS if s["id"] == section_id)
    extractor = EXTRACTORS[section_id]

    # Coleta texto por estado
    state_texts = {}
    for state in all_states:
        org = organs_of(state, group_key)
        if not org:
            continue
        text = extractor(org, state)
        if text.strip():
            state_texts[state["id"]] = text.strip()

    ref_text = state_texts.get("ro", "")
    others   = {k: v for k, v in state_texts.items() if k != "ro"}

    if section_id in ("subordinacao", "finalidade", "organizacao"):
        # Prosa: base é RO; se vazio, maior dos outros
        if ref_text:
            proposed = ref_text
        elif others:
            proposed = max(others.values(), key=len)
        else:
            proposed = ""
        sources = list(state_texts.keys())

    elif section_id == "competencias":
        # Base canônica: CBMRO (verbatim). Enriquecimento: itens de outros
        # estados SÓ quando genéricos — sem citação legal alheia, sem nome de
        # outro estado, sem sigla de CBM de outro estado.
        other_names = _other_state_tokens(all_states)
        items, seen, contributing = [], set(), []

        # 1) CBMRO — todas as atribuições, verbatim
        ro_added = False
        for state in all_states:
            if state["id"] != "ro":
                continue
            for o in organs_of(state, group_key):
                for a in (o.get("atribuicoes") or []):
                    a, key = a.strip(), normalize(a)
                    if a and key not in seen:
                        seen.add(key)
                        items.append(a)
                        ro_added = True
        if ro_added:
            contributing.append("ro")

        # 2) Outros estados — somente competências genéricas
        for state in all_states:
            if state["id"] == "ro":
                continue
            state_added = False
            for o in organs_of(state, group_key):
                for a in (o.get("atribuicoes") or []):
                    a, key = a.strip(), normalize(a)
                    if not a or key in seen:
                        continue
                    if not is_generic_competencia(a, other_names):
                        continue
                    seen.add(key)
                    items.append(a)
                    state_added = True
            if state_added:
                contributing.append(state["id"])

        proposed = "\n".join(f"{i+1}. {item}" for i, item in enumerate(items))
        sources  = contributing

    else:  # cargos_atribuicoes — usa RO como base canônica
        ro_organs = []
        for state in all_states:
            if state["id"] == "ro":
                ro_organs.extend(organs_of(state, group_key))
        proposed = extract_cargos_atribuicoes(ro_organs, {})
        sources  = list(state_texts.keys())
        if not proposed and others:
            # Fallback: primeiro estado com cargos
            for state in all_states:
                if state["id"] == "ro":
                    continue
                org = organs_of(state, group_key)
                candidate = extract_cargos_atribuicoes(org, state)
                if candidate:
                    proposed = candidate
                    sources  = [state["id"]]
                    break

    return {"id": section_id, "title": title, "proposedText": proposed, "sources": sources}


def build_organ(all_states: list, group_key: str) -> dict:
    return {
        "label":    ORGAN_LABELS[group_key],
        "sections": [build_section(s["id"], all_states, group_key) for s in SECTIONS],
    }


def main():
    data       = json.loads(IN_JSON.read_text(encoding="utf-8"))
    all_states = data["states"]
    output = {
        "generated_by": "scripts/build_minuta_structure.py",
        "dpo": build_organ(all_states, "dpo"),
        "cot": build_organ(all_states, "cot"),
    }
    OUT_JSON.write_text(json.dumps(output, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Gerado: {OUT_JSON}")
    for key in ("dpo", "cot"):
        seções = output[key]["sections"]
        filled = sum(1 for s in seções if s["proposedText"])
        print(f"  {key.upper()}: {filled}/{len(seções)} seções com texto")


if __name__ == "__main__":
    main()
