import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

from triagem_acervo import score_extracao, tipo_por_conteudo, valida_prefixo

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

# tipo_por_conteudo: Portaria/Diretriz Operacional (caso MA) -> Regimento de Serviços
ma = ("PORTARIA Nº 46/2020 Aprova Diretriz Operacional para o Serviço de Gestor "
      "Operacional de Dia, Supervisor do CIOPS e Superior de Dia.")
assert tipo_por_conteudo(ma) == "Regimento de Serviços", tipo_por_conteudo(ma)

# Decreto de serviços diários (caso PA) -> Regimento de Serviços
pa = ("Dispõe sobre as normas ou procedimentos para os serviços administrativos, "
      "preventivos e operacionais a serem adotados nas atividades diárias.")
assert tipo_por_conteudo(pa) == "Regimento de Serviços", tipo_por_conteudo(pa)

# LOB -> Lei de Organização Básica
lob = "Dispõe sobre a organização básica do Corpo de Bombeiros Militar e dá providências."
assert tipo_por_conteudo(lob) == "Lei de Organização Básica", tipo_por_conteudo(lob)

# Quadro demonstrativo -> Quadro Demonstrativo de Cargos
assert tipo_por_conteudo("Quadro Demonstrativo de Cargos e Funções") == "Quadro Demonstrativo de Cargos"

# Texto sem pista reconhecível -> Indefinido
assert tipo_por_conteudo("Bom dia a todos, segue o comunicado.") == "Indefinido"

print("tipo_por_conteudo OK")

# valida_prefixo: usa um STATE_META falso pequeno (teste puro, sem importar o real)
FAKE_META = {"Maranhão": {"id": "ma"}, "Pará": {"id": "pa"}, "Mato Grosso": {"id": "mt"}}

# prefixo exato -> (True, prefixo)
assert valida_prefixo("Maranhão - Portaria.pdf", FAKE_META) == (True, "Maranhão")

# caixa/acento diferentes -> (False, forma canônica sugerida)
assert valida_prefixo("maranhao - Portaria.pdf", FAKE_META) == (False, "Maranhão")

# estado inexistente -> (False, None)
assert valida_prefixo("Xingu - Foo.pdf", FAKE_META) == (False, None)

# sem separador " - " -> (False, None)
assert valida_prefixo("SemSeparador.pdf", FAKE_META) == (False, None)

print("valida_prefixo OK")
