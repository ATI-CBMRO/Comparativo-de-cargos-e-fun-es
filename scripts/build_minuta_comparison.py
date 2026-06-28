"""
build_minuta_comparison.py — Portal CBM

Gera database/comparativo_minuta.json: comparativo RO × demais estados, órgão a
órgão, na MESMA estrutura da minuta (12 órgãos (11 da LOB + guarnição), incl. a Guarnição de Serviço).
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
from build_minuta_structure import ORGAN_ORDER, command_order  # noqa: E402
from minuta_enrichment import enrich_organ_for, GUARNICAO_CHAPTER  # noqa: E402

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

BASE_DIR = Path(__file__).parent.parent
DET_DIR = BASE_DIR / "database" / "organs_detail"
STATES_JSON = BASE_DIR / "database" / "states_data.json"
DPO_COT_JSON = BASE_DIR / "database" / "comparativo_dpo_cot.json"
OUT_JSON = BASE_DIR / "database" / "comparativo_minuta.json"

REF_ID = "ro"

# Títulos dos 12 órgãos (11 da LOB + guarnição). A ORDEM e a PROFUNDIDADE são
# derivadas da cadeia de comando (command_order) em build(), para espelhar o
# organograma da minuta — ver build_minuta_structure.command_order.
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

    # 2) Competências curadas (ENRICHMENT_ORGAN) pivotadas por fonte.
    # Acumula os rótulos DISTINTOS por estado (preservando a ordem) para creditar
    # todos os artigos quando um estado contribui com mais de uma fonte ao órgão.
    by_state = {}
    for it in enrich_organ_for(organ_key):
        sid = state_from_source_label(it["source"])
        if not sid or sid == REF_ID:
            continue
        bucket = by_state.setdefault(sid, {"items": [], "sources": []})
        bucket["items"].append(it["text"])
        if it["source"] not in bucket["sources"]:
            bucket["sources"].append(it["source"])
    for sid, info in by_state.items():
        label = "; ".join(info["sources"])
        if sid in out:  # já tem estrutura curada -> anexa competências como órgão extra
            out[sid]["organs"].append(competencia_organ(info["items"]))
            if not out[sid].get("sourceLabel"):
                out[sid]["sourceLabel"] = label
        else:
            out[sid] = {
                **meta.get(sid, _fallback_meta(sid)),
                "provenance": "curado", "sourceLabel": label, "note": None,
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
        # A coluna compilada exclui a camada LOB nova (source:lob), que vai só em lobOrgans;
        # mantém a visão mesclada histórica (RI/NGA/etc.) intacta.
        non_lob = {oid: o for oid, o in organs.items() if o.get("source") != "lob"}
        ids = auto_match_organ_ids(organ_key, non_lob)
        matched = [extract_organ(non_lob, oid) for oid in ids]
        matched = [m for m in matched if m]
        if not matched:
            continue
        out[sid] = {
            **meta[sid], "provenance": "automatico", "sourceLabel": None, "note": None,
            "organs": matched,
        }
    return out


def lob_organs(organs):
    """Subconjunto LOB do organs_detail de um estado: se houver algum órgão com
    source=='lob' (estados com legislação mista, já tagueados), retorna só esses;
    senão retorna todos (estados de doc único de LOB, cuja curadoria já é LOB)."""
    lobbed = {oid: o for oid, o in organs.items() if o.get("source") == "lob"}
    return lobbed if lobbed else organs


def attach_lob_organs(organ_key, state_records):
    """Para cada estado já presente no comparativo, anexa:
      - lobOrgans: órgãos da LOB casados (organs_detail filtrado a LOB + auto-match);
      - lobProvenance: 'curado' se algum órgão casado tem source=='lob', senão 'automatico'.
    Não altera a coluna compilada (rec['organs'])."""
    for rec in state_records:
        sid = rec["id"]
        if sid == REF_ID:
            continue
        organs = load_organs(sid)
        lobbed = lob_organs(organs)
        ids = auto_match_organ_ids(organ_key, lobbed)
        matched = [extract_organ(lobbed, oid) for oid in ids]
        rec["lobOrgans"] = [m for m in matched if m]
        rec["lobProvenance"] = (
            "curado" if any(lobbed.get(oid, {}).get("source") == "lob" for oid in ids)
            else "automatico"
        )


def sort_states(records):
    """Curado primeiro, depois automático; cada grupo alfabético por sigla."""
    return sorted(records, key=lambda r: (r["provenance"] != "curado", r["abbr"]))


def build():
    meta = load_state_meta()
    ro_organs = load_organs(REF_ID)
    dpo_cot = json.loads(DPO_COT_JSON.read_text(encoding="utf-8"))

    # Ordem + profundidade hierárquica (DFS da cadeia de comando do organograma).
    order = command_order(ro_organs)

    organs_out = []
    for organ_key, depth in order:
        reference, ref_note = build_reference(organ_key, ro_organs)
        curated = curated_states_for(organ_key, dpo_cot, meta)
        auto = auto_states_for(organ_key, set(curated.keys()), meta)
        states = sort_states(list(curated.values()) + list(auto.values()))
        attach_lob_organs(organ_key, states)
        ref_abbr = ((reference or {}).get("abbreviation")
                    or (GUARNICAO_CHAPTER.get("abbr") if organ_key == "guarnicao" else "")
                    or organ_key.upper())
        organs_out.append({
            "key": organ_key, "title": ORGAN_TITLES.get(organ_key, organ_key.upper()),
            "abbr": ref_abbr, "depth": depth, "reference": reference, "referenceNote": ref_note,
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
    print("Gerando comparativo da minuta (RO × estados, 12 órgãos (11 da LOB + guarnição))")
    print("=" * 60)
    build()
