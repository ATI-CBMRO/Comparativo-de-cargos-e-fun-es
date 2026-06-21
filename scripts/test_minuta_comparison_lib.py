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
