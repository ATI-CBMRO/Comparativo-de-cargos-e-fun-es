import json
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
# dpo: AUTO_MATCH_KEYWORDS pode ter uma entrada de fallback (desde 43c5c28), mas o
# invariante que importa de verdade é o COMPORTAMENTO: build_minuta_comparison.py
# só chama a camada automática para estados sem curadoria (linha ~205), e o DPO tem
# curadoria para os 26 estados desde o início — então nenhum estado deve sair como
# "automatico" para o DPO na saída final, curada ou não.
_comparativo_path = Path(__file__).parent.parent / "database" / "comparativo_minuta.json"
if _comparativo_path.exists():
    _dpo = next(o for o in json.loads(_comparativo_path.read_text(encoding="utf-8"))["organs"] if o["key"] == "dpo")
    assert all(s.get("provenance") == "curado" for s in _dpo["states"]), \
        "DPO deveria ser 100% curado — auto-match nunca deveria vencer aqui"


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

print("OK")
