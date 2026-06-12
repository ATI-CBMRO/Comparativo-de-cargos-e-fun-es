"""
build_organs_detail.py — Portal CBM
Gera os arquivos database/organs_detail/<id>.json a partir dos módulos de dados
detail_data_g1..g5. Cada órgão traz subordinação, desdobramentos, atribuições e
cargos extraídos fielmente das legislações. Idempotente.
"""

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')

from detail_data_g1 import DATA as D1
from detail_data_g2 import DATA as D2
from detail_data_g3 import DATA as D3
from detail_data_g4 import DATA as D4
from detail_data_g5 import DATA as D5

# Cargos detalhados (subordinação, desdobramentos, atribuições) por estado.
# Chaveados por id de órgão existente; mesclados nos órgãos abaixo.
import unicodedata, re as _re
try:
    from detail_cargos_g1 import CARGOS as C1
except Exception:
    C1 = {}
try:
    from detail_cargos_g2 import CARGOS as C2
except Exception:
    C2 = {}
try:
    from detail_cargos_g3 import CARGOS as C3
except Exception:
    C3 = {}
try:
    from detail_cargos_g4 import CARGOS as C4
except Exception:
    C4 = {}
try:
    from detail_cargos_g5 import CARGOS as C5
except Exception:
    C5 = {}

ALL_CARGOS = {}
for c in (C1, C2, C3, C4, C5):
    ALL_CARGOS.update(c)


def _norm(s):
    s = unicodedata.normalize("NFKD", s or "").encode("ascii", "ignore").decode().lower()
    return _re.sub(r"[^a-z0-9]+", " ", s).strip()


def merge_cargos(state_id, organs):
    """Mescla os cargos detalhados nos órgãos. Aceita chaves por id de órgão
    ou por 'Nome | SIGLA' (correspondência por sigla/nome)."""
    data = ALL_CARGOS.get(state_id)
    if not data:
        return 0
    by_abbr, by_name = {}, {}
    for oid, o in organs.items():
        ab = (o.get("abbreviation") or "").strip().lower()
        if ab:
            by_abbr.setdefault(ab, oid)
        by_name[_norm(o.get("name", ""))] = oid
    merged = 0
    for key, cargos in data.items():
        oid = None
        if key in organs:
            oid = key
        else:
            name, _, sigla = key.partition("|")
            sigla = sigla.strip().lower()
            nn = _norm(name)
            if sigla and sigla in by_abbr:
                oid = by_abbr[sigla]
            elif nn in by_name:
                oid = by_name[nn]
            else:
                for k, v in by_name.items():
                    if nn and k and (nn == k or nn in k or k in nn):
                        oid = v
                        break
        if oid and oid in organs:
            organs[oid]["cargos"] = cargos
            merged += 1
    return merged


BASE_DIR = Path(__file__).parent.parent
OUT_DIR = BASE_DIR / "database" / "organs_detail"
OUT_DIR.mkdir(parents=True, exist_ok=True)

# Metadados por estado: nome, denominação completa e sigla da corporação
META = {
    "ac": ("Acre", "Corpo de Bombeiros Militar do Estado do Acre", "CBMAC"),
    "al": ("Alagoas", "Corpo de Bombeiros Militar de Alagoas", "CBMAL"),
    "ap": ("Amapá", "Corpo de Bombeiros Militar do Amapá", "CBMAP"),
    "am": ("Amazonas", "Corpo de Bombeiros Militar do Amazonas", "CBMAM"),
    "ba": ("Bahia", "Corpo de Bombeiros Militar da Bahia", "CBMBA"),
    "ce": ("Ceará", "Corpo de Bombeiros Militar do Ceará", "CBMCE"),
    "df": ("Distrito Federal", "Corpo de Bombeiros Militar do Distrito Federal", "CBMDF"),
    "es": ("Espírito Santo", "Corpo de Bombeiros Militar do Espírito Santo", "CBMES"),
    "go": ("Goiás", "Corpo de Bombeiros Militar do Estado de Goiás", "CBMGO"),
    "ma": ("Maranhão", "Corpo de Bombeiros Militar do Maranhão", "CBMMA"),
    "mt": ("Mato Grosso", "Corpo de Bombeiros Militar do Mato Grosso", "CBMMT"),
    "ms": ("Mato Grosso do Sul", "Corpo de Bombeiros Militar do Mato Grosso do Sul", "CBMMS"),
    "mg": ("Minas Gerais", "Corpo de Bombeiros Militar de Minas Gerais", "CBMMG"),
    "pr": ("Paraná", "Corpo de Bombeiros Militar do Paraná", "CBMPR"),
    "pb": ("Paraíba", "Corpo de Bombeiros Militar da Paraíba", "CBMPB"),
    "pa": ("Pará", "Corpo de Bombeiros Militar do Pará", "CBMPA"),
    "pe": ("Pernambuco", "Corpo de Bombeiros Militar de Pernambuco", "CBMPE"),
    "pi": ("Piauí", "Corpo de Bombeiros Militar do Piauí", "CBMPI"),
    "rn": ("Rio Grande do Norte", "Corpo de Bombeiros Militar do Rio Grande do Norte", "CBMRN"),
    "rs": ("Rio Grande do Sul", "Corpo de Bombeiros Militar do Rio Grande do Sul", "CBMRS"),
    "rj": ("Rio de Janeiro", "Corpo de Bombeiros Militar do Estado do Rio de Janeiro", "CBMERJ"),
    "rr": ("Roraima", "Corpo de Bombeiros Militar do Estado de Roraima", "CBMRR"),
    "sc": ("Santa Catarina", "Corpo de Bombeiros Militar de Santa Catarina", "CBMSC"),
    "se": ("Sergipe", "Corpo de Bombeiros Militar de Sergipe", "CBMSE"),
    "sp": ("São Paulo", "Corpo de Bombeiros Militar do Estado de São Paulo", "CBPMESP"),
    "to": ("Tocantins", "Corpo de Bombeiros Militar do Tocantins", "CBMTO"),
}

ALL_DATA = {}
for d in (D1, D2, D3, D4, D5):
    ALL_DATA.update(d)


def main():
    print("=" * 60)
    print("Portal CBM — Construtor de organs_detail/*.json")
    print("=" * 60)
    count = 0
    for state_id, payload in sorted(ALL_DATA.items()):
        name, cbm_name, cbm_abbr = META.get(state_id, (state_id.upper(), "Corpo de Bombeiros Militar", "CBM"))
        organs = payload["organs"]
        # injeta o campo id em cada órgão (garante consistência)
        for oid, organ in organs.items():
            organ.setdefault("id", oid)
        # mescla cargos detalhados (hierarquia/atribuições) quando disponíveis
        merge_cargos(state_id, organs)
        out = {
            "state_id": state_id,
            "state_name": name,
            "cbm_name": cbm_name,
            "cbm_abbreviation": cbm_abbr,
            "legal_source": payload.get("legal_source", ""),
            "organs": organs,
        }
        path = OUT_DIR / f"{state_id}.json"
        path.write_text(json.dumps(out, ensure_ascii=False, indent=2), encoding="utf-8")
        n = len(organs)
        count += 1
        print(f"  ✓ {state_id}.json — {n} órgãos detalhados")

    print(f"\n{'='*60}")
    print(f"Gerados: {count} arquivos de detalhamento em {OUT_DIR}")
    print("Concluído.")


if __name__ == "__main__":
    main()
