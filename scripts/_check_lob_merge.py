"""Verificação da camada LOB no comparativo (asserções; sem pytest no repo)."""
import json, sys
from pathlib import Path
BASE = Path(__file__).parent.parent
d = json.loads((BASE / "database" / "comparativo_minuta.json").read_text(encoding="utf-8"))
by = {o["key"]: o for o in d["organs"]}

def state(organ_key, sid):
    o = by[organ_key]
    return next((s for s in o["states"] if s["id"] == sid), None)

sc_dp = state("dp", "sc"); assert sc_dp, "SC ausente em dp"
assert sc_dp["lobProvenance"] == "curado", f"esperava lobProvenance curado, veio {sc_dp['lobProvenance']}"
lob_atrib = [a for g in (sc_dp.get("lobOrgans") or []) for a in (g.get("atribuicoes") or [])]
assert lob_atrib, "coluna LOB de (dp,sc) vazia"

go_cg = state("cg", "go"); assert go_cg, "GO não foi adicionado em cg via camada LOB"
assert go_cg["provenance"] == "curado"

col3_atrib = [a for g in (go_cg.get("organs") or []) for a in (g.get("atribuicoes") or [])]
assert col3_atrib, "coluna 3 de (cg,go) vazia"

print("OK: camada LOB integrada (col2 curada, estado só-LOB adicionado, col3 com LOB).")
