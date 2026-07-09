import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

from equivalencias_terminologicas import expand_terms, all_terms_normalized
from sugerir_equivalencias import normalize, split_articles, score_article
import verificar_verbatim as vv

# expand_terms: sinônimos do mesmo grupo se expandem para o mesmo conjunto
grupo_dia = expand_terms("serviço de dia")
assert "servico de permanencia" in grupo_dia
assert "servico interno" in grupo_dia
assert expand_terms("serviço de permanência") == grupo_dia

# expand_terms: termo fora de qualquer grupo devolve só ele mesmo (normalizado)
assert expand_terms("termo qualquer sem sinonimo") == {"termo qualquer sem sinonimo"}

# all_terms_normalized: inclui termos conhecidos
assert "dgp" in all_terms_normalized()

# normalize: minúsculas + sem acento
assert normalize("Comandante-Geral") == "comandante-geral"
assert normalize("Serviço de Dia") == "servico de dia"

# split_articles: separa por "Art." mantendo cabeçalho+corpo juntos; texto antes do
# 1º "Art." (preâmbulo/título) vira seu próprio segmento inicial.
texto = "Preâmbulo qualquer\nArt. 1º Primeiro artigo.\nContinuação.\nArt. 2º Segundo artigo."
arts = split_articles(texto)
assert len(arts) == 3
assert arts[0] == "Preâmbulo qualquer"
assert arts[1].startswith("Art. 1º")
assert "Continuação" in arts[1]
assert arts[2].startswith("Art. 2º")

# score_article: mais palavras-chave encontradas -> score maior
alto = score_article(normalize("serviço de dia e escala de serviço"), {"servico de dia", "escala de servico"})
baixo = score_article(normalize("texto totalmente não relacionado"), {"servico de dia", "escala de servico"})
assert alto > baixo

# verificar_verbatim.normalize_whitespace: colapsa espaços/quebras e desfaz hifenização
assert vv.normalize_whitespace("texto  com   espaços\ne quebra") == "texto com espaços e quebra"
assert vv.normalize_whitespace("pala-\nvra quebrada") == "palavra quebrada"

# verificar_verbatim.verificar: sem REGULAMENTO_ENRICHMENT, retorna 0 (nada a verificar)
vv.REGULAMENTO_ENRICHMENT = None
assert vv.verificar() == 0

# verificar_verbatim.verificar: dispositivo verbatim presente -> OK (0)
FONTE_FAKE = "Texto de exemplo. Inciso I - exemplo. Palavra que bro tou com artefato."
vv.REGULAMENTO_ENRICHMENT = {
    ("tema-x", "zz"): [{"caput": "Texto de exemplo.", "dispositivos": ["Inciso I - exemplo."]}],
}
vv.REGULAMENTO_DOCS = {"zz": "fonte-fake.md"}
vv.carrega_markdown = lambda state_id: (vv.normalize_whitespace(FONTE_FAKE),
                                        vv.normalize_whitespace(FONTE_FAKE).replace(' ', ''))
assert vv.verificar() == 0

# tolerância a artefato de PDF: fonte tem "bro tou" (espaço espúrio); transcrição
# corrigida "brotou" ainda é aceita (letras verbatim)
vv.REGULAMENTO_ENRICHMENT = {
    ("tema-x", "zz"): [{"caput": None, "dispositivos": ["Palavra que brotou com artefato."]}],
}
assert vv.verificar() == 0

# verificar_verbatim.verificar: dispositivo com paráfrase (não verbatim) -> erro (1)
vv.REGULAMENTO_ENRICHMENT = {
    ("tema-x", "zz"): [{"caput": "Texto de exemplo.", "dispositivos": ["Isto não está na fonte."]}],
}
assert vv.verificar() == 1

print("OK — scripts/test_equivalencias.py")
