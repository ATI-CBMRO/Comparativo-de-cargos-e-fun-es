"""
minuta_comparison_lib.py — Portal CBM

Helpers puros do build do comparativo da minuta:
- normalização tolerante (sem acento, minúsculas);
- extração do estado de origem a partir do rótulo de fonte ("cf. CBMxx, ...");
- casamento automático de órgão por palavra-chave (camada "automatico").
"""

import re
import unicodedata


def norm(s: str) -> str:
    s = unicodedata.normalize("NFKD", s or "")
    s = "".join(c for c in s if not unicodedata.combining(c))
    return re.sub(r"\s+", " ", s).strip().lower()


def state_from_source_label(label: str) -> str | None:
    """'cf. CBMMT, RI, Art. 236' -> 'mt'. None se não houver CBMxx."""
    m = re.search(r"\bCBM([A-Za-z]{2})\b", label or "")
    return m.group(1).lower() if m else None


# Camada "automatico": por organ_key, palavras-chave de inclusão/exclusão (já normalizadas).
AUTO_MATCH_KEYWORDS = {
    "dpo":   {"include": ["planejamento"],                     "exclude": []},
    "cot":   {"include": ["operacoes", "operacional"],
              "exclude": ["aerea", "aereo", "aviacao", "atividades tecnicas"]},
    "doe":   {"include": ["especializ"],                       "exclude": []},
    "crbm":  {"include": ["regional", "regiao de bombeiro"],   "exclude": []},
    "bbm":   {"include": ["batalhao"],
              "exclude": ["busca", "salvamento", "florestal", "ambiental",
                          "aerea", "aereo", "aviacao", "maritimo"]},
    "cibm":  {"include": ["companhia independente", "cia independente"], "exclude": []},
    "gbm":   {"include": ["grupo", "grupamento"],              "exclude": []},
    "bbs":   {"include": ["busca", "salvamento"],              "exclude": []},
    "bifea": {"include": ["florestal", "ambiental"],           "exclude": []},
    "boa":   {"include": ["aerea", "aereo", "aviacao", "operacoes aereas"], "exclude": []},
    "cat":   {"include": ["atividades tecnicas", "atividade tecnica"],
              "exclude": ["operacoes tecnicas", "comando de operacoes"]},
    "cg":     {"include": ["comando geral", "comando-geral", "estado maior", "estado-maior"],
               "exclude": ["regional", "operacoes", "setorial", "secao"]},
    "depdec": {"include": ["defesa civil", "protecao e defesa"], "exclude": []},
    "condeg": {"include": ["conselho"],
               "exclude": ["municipal", "regional"]},
}


def auto_match_organ_ids(organ_key: str, organs: dict) -> list[str]:
    spec = AUTO_MATCH_KEYWORDS.get(organ_key)
    if not spec:
        return []
    inc, exc = spec["include"], spec["exclude"]
    out = []
    for oid, o in organs.items():
        n = norm(o.get("name", ""))
        if any(k in n for k in inc) and not any(k in n for k in exc):
            out.append(oid)
    return out
