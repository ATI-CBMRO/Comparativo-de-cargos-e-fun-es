"""
triagem_acervo.py — helper READ-ONLY da skill ingestar-acervo.

Não renomeia, move, nem edita nenhum arquivo. Só lê PDFs e imprime um relatório de
triagem: qualidade da extração, tipo proposto por conteúdo e validação do prefixo do
nome contra STATE_META. As 3 funções puras (score_extracao, tipo_por_conteudo,
valida_prefixo) não importam pypdf nem build_states_data.
"""

import re
import unicodedata

GLYPH_RE = re.compile(r'/U[0-9A-Fa-f]{4}')


def score_extracao(texto: str) -> str:
    """Classifica a qualidade da extração em OK / SUSPEITO / RUIM.

    Puro: recebe o texto já extraído (amostra de páginas). Sinaliza os dois modos de
    falha já vistos no projeto: fonte mapeada por glifos (/U00XX, caso RJ DAT) e
    PDF escaneado/garble com baixa densidade alfabética (caso Piauí).
    """
    if not texto:
        return "RUIM"
    total = len(texto)
    glyph_chars = sum(len(m.group()) for m in GLYPH_RE.finditer(texto))
    glyph_ratio = glyph_chars / total
    if glyph_ratio > 0.30:
        return "RUIM"
    non_space = [c for c in texto if not c.isspace()]
    if not non_space:
        return "RUIM"
    alpha_ratio = sum(1 for c in non_space if c.isalpha()) / len(non_space)
    if alpha_ratio < 0.45:
        return "RUIM"
    if glyph_ratio > 0.05 or alpha_ratio < 0.60:
        return "SUSPEITO"
    return "OK"
