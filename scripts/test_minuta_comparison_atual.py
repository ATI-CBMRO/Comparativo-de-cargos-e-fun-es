"""Valida database/atual/comparativo_minuta.json (gerado por build_minuta_comparison_atual)."""
import json
import re
import sys
from pathlib import Path

BASE = Path(__file__).parent.parent
OUT = BASE / "database" / "atual" / "comparativo_minuta.json"
STRUCT = BASE / "database" / "atual" / "minuta_structure.json"

# Rótulos que só existem na camada CURADA da futura — presença aqui = vazamento.
# Genérico: qualquer "cf. " denota rótulo curado, não só as siglas conhecidas hoje.
FORBIDDEN = re.compile(r'"cf\. ')

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
