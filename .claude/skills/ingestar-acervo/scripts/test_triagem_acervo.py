import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

from triagem_acervo import score_extracao

# Texto legal em português bem extraído -> OK
bom = ("Art. 1º Fica aprovado o Regulamento Geral do Corpo de Bombeiros Militar, "
       "que dispõe sobre a organização e o funcionamento da corporação. "
       "Parágrafo único. As disposições desta lei aplicam-se a todos os órgãos.")
assert score_extracao(bom) == "OK", score_extracao(bom)

# Fonte mapeada por glifos (caso RJ DAT) -> RUIM
glifos = "/U0044/U0049/U0052/U0049/U004F /U0050/U004F/U0044/U0045/U0052 /U0045/U0058"
assert score_extracao(glifos) == "RUIM", score_extracao(glifos)

# Texto vazio -> RUIM
assert score_extracao("") == "RUIM"
assert score_extracao(None) == "RUIM"

# Garble de símbolos/dígitos com pouca letra -> RUIM
lixo = "12 34 %% ## @@ 55 || 77 && (( )) ** ++ == 99 :: ;;"
assert score_extracao(lixo) == "RUIM", score_extracao(lixo)

print("score_extracao OK")
