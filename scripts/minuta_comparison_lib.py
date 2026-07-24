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
    # cot = Comando de Operações TÉCNICAS: segurança contra incêndio e pânico, análise
    # de edificações, prevenção (NÃO é socorro/atividade-fim). O include por
    # "operacoes/operacional" casava os Comandos Operacionais de SOCORRO de ~20 estados
    # (mesma armadilha AR-01 do COB×COT); trocado pela MATÉRIA técnica em 2026-07-24
    # (decisão do Wândrio, diff revisado: 24 estados, todos órgãos de seg. contra
    # incêndio/prevenção; 0 comando de socorro). Sobrepõe o `cat` de propósito — no RO
    # o CAT é a execução subordinada ao COT, a mesma matéria; aceitável no fallback
    # automático (selo "sujeito a revisão").
    "cot":   {"include": ["operacoes tecnicas", "operacao tecnica",
                          "seguranca contra incendio", "contra incendio",
                          "prevencao de incendio", "atividades tecnicas",
                          "servicos tecnicos"],
              "exclude": ["assessoria", "aerea", "aereo", "aviacao"]},
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
               # "gabinete": "Gabinete do Comando-Geral" contém "comando-geral" e caía
               # aqui além de em gab-cg (AR-01, auditoria 2026-07-23) — o painel do
               # Comando-Geral mostrava o Gabinete do estado como se fosse o Comando.
               "exclude": ["regional", "operacoes", "setorial", "secao", "gabinete"]},
    "depdec": {"include": ["defesa civil", "protecao e defesa"], "exclude": []},
    "condeg": {"include": ["conselho"],
               # "ensino": Conselho Superior de Ensino/Pesquisa (MT) não é o CONDEG
               # (auditoria 2026-07-23) — já casa em deei pela matéria certa.
               "exclude": ["municipal", "regional", "ensino"]},
    "dp":   {"include": ["diretoria de pessoal", "departamento de pessoal",
                         "gestao de pessoal", "gestao de pessoas", "recursos humanos"],
             "exclude": ["assistencia ao pessoal", "saude"]},
    "deei": {"include": ["ensino", "instrucao", "academia"],
             "exclude": ["defesa civil"]},
    "dpof": {"include": ["financas", "orcamento", "gestao e financas",
                         "administracao financeira"],
             "exclude": ["planejamento operacional"]},
    "dsap": {"include": ["saude", "assistencia ao pessoal", "assistencia social"],
             "exclude": []},
    "dlog": {"include": ["logistica", "apoio logistico", "material e patrimonio",
                         "materiais e servicos", "suprimento"],
             "exclude": []},
    "cint": {"include": ["inteligencia"],                        "exclude": []},
    "ccs":  {"include": ["comunicacao social"],                  "exclude": []},
    "cinf": {"include": ["informatica", "tecnologia da informacao"], "exclude": []},
    "assessorias": {"include": ["assessoria"],
                    # "informatica"/"telecomunicacoes": Assessoria de Telecomunicações e
                    # Informática (TO) pertence ao cinf, não às assessorias genéricas
                    # (auditoria 2026-07-23).
                    "exclude": ["assessoria de comunicacao", "comunicacao social",
                                "inteligencia", "defesa civil",
                                "informatica", "telecomunicacoes"]},
    "gab-cg": {"include": ["gabinete"],
               "exclude": ["subcomando", "subcomandante", "chefia de gabinete"]},
    "ag":     {"include": ["ajudancia", "ajudante-geral", "ajudante geral"],
               "exclude": []},
    "corregedoria": {"include": ["corregedoria", "correicao"], "exclude": []},
}


def auto_match_organ_ids(organ_key: str, organs: dict, keywords: dict | None = None) -> list[str]:
    """`keywords` permite reusar o MESMO matcher com outra tabela (a do cenário
    atual) — antes o builder do atual reimplementava esta função e correções num
    lado não propagavam pro outro (achado da auditoria de 2026-07-23)."""
    spec = (keywords if keywords is not None else AUTO_MATCH_KEYWORDS).get(organ_key)
    if not spec:
        return []
    inc, exc = spec["include"], spec["exclude"]
    out = []
    for oid, o in organs.items():
        n = norm(o.get("name", ""))
        if any(k in n for k in inc) and not any(k in n for k in exc):
            out.append(oid)
    return out
