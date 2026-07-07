"""Glossário de sinônimos terminológicos entre os regulamentos dos diferentes CBMs.

Alimentado incrementalmente durante a curadoria do Bloco B1-M ("os textos não casam
perfeitamente entre estados") — cada grupo é um conjunto de termos que estados
diferentes usam para o MESMO conceito. Usado por scripts/sugerir_equivalencias.py
(garimpo de candidatos) e, no futuro, pela busca do comparador de regulamentos.

É DADO reutilizável: crescer este glossário melhora automaticamente o garimpo de
candidatos em TODOS os estados, sem tocar em código.
"""
import unicodedata

# Cada grupo: variações (como aparecem no texto, com acento normal) que devem ser
# tratadas como equivalentes ao comparar/ranquear trechos entre estados.
SYNONYM_GROUPS = [
    # Serviço operacional / regime de serviço
    ["serviço de dia", "serviço de permanência", "serviço interno", "serviço de escala"],
    ["escala de serviço", "escala de plantão", "quadro de serviço"],
    ["guarnição de serviço", "guarnição operacional", "guarnição de plantão"],
    ["oficial de dia", "fiscal de dia", "oficial de serviço"],
    # Órgãos de gestão de pessoal
    ["diretoria de gestão de pessoas", "diretoria de pessoal", "dgp"],
    ["diretoria de ensino", "diretoria de ensino e instrução", "de"],
    # Frações / unidades
    ["grupamento", "gbm", "grupamento de bombeiros militar"],
    ["companhia", "cia bm", "cia"],
    ["pelotão", "pel bm", "pel"],
    ["batalhão", "bbm", "batalhão de bombeiros militar"],
    # Disciplina/correição
    ["corregedoria", "corregedoria geral", "corregedoria-geral"],
    ["conselho de disciplina", "conselho disciplinar"],
    # Cerimonial
    ["honras militares", "honras e continências", "continência"],
]


def _norm(s):
    """Minúsculas + remove acentos (mantém números/pontuação simples)."""
    s = unicodedata.normalize('NFKD', s.lower())
    return ''.join(c for c in s if not unicodedata.combining(c))


def expand_terms(term):
    """Dado um termo, devolve o conjunto de termos equivalentes (normalizados,
    incluindo ele mesmo). Se o termo não estiver em nenhum grupo, devolve só ele
    mesmo normalizado."""
    t = _norm(term)
    for group in SYNONYM_GROUPS:
        normalized_group = {_norm(g) for g in group}
        if t in normalized_group:
            return normalized_group
    return {t}


def all_terms_normalized():
    """Todos os termos conhecidos do glossário, já normalizados."""
    out = set()
    for group in SYNONYM_GROUPS:
        out.update(_norm(g) for g in group)
    return out
