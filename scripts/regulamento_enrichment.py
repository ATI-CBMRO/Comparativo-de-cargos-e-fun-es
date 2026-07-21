"""Curadoria dos regulamentos estaduais para a minuta do Regulamento do CBMRO.

ARQUIVO-MESTRE: define a taxonomia de temas, o inventário de fontes, a fonte primária
por tema e a tabela de adaptações para RO, e MESCLA as transcrições por estado
(scripts/regulamento_enrichment_<uf>.py — um arquivo por estado, escritos na
transcrição das rodadas T1–T7; ver docs/curadoria/panorama-cobertura.md).

Disciplina (B1-M): só entra dispositivo VERBATIM do markdown de origem, com rótulo de
fonte e nível de correspondência (`match`). scripts/verificar_verbatim.py confere tudo.
"""

# ── Taxonomia (15 temas; é DADO — cresce com a curadoria) ────────────────────────────
# (key, título p/ a minuta, grupo de exibição)
THEMES = [
    ("disposicoes-preliminares", "Das Disposições Preliminares", "Fundamentos"),
    ("organizacao-geral", "Da Organização Geral", "Fundamentos"),
    ("competencias-direcao", "Das Competências dos Órgãos de Direção", "Competências"),
    ("competencias-apoio-assessoramento", "Das Competências dos Órgãos de Apoio e Assessoramento", "Competências"),
    ("competencias-execucao", "Das Competências dos Órgãos de Execução", "Competências"),
    ("servico-operacional", "Do Serviço Operacional", "Serviços"),
    ("servico-interno-dia", "Do Serviço Interno e de Dia", "Serviços"),
    ("atribuicoes-funcoes", "Das Atribuições das Funções", "Competências"),
    ("disciplina-correicao", "Da Disciplina e da Correição", "Correição e Conduta"),
    ("uniformes-apresentacao", "Dos Uniformes e da Apresentação Pessoal", "Correição e Conduta"),
    ("cerimonial-honras", "Do Cerimonial e das Honras", "Correição e Conduta"),
    ("ensino-instrucao", "Do Ensino e da Instrução", "Atividades Especializadas"),
    ("seguranca-contra-incendio", "Da Segurança Contra Incêndio e Pânico", "Atividades Especializadas"),
    ("pessoal-quadros", "Do Pessoal e dos Quadros", "Pessoal"),
    ("disposicoes-finais", "Das Disposições Finais", "Fundamentos"),
    ("central-operacoes-193", "Da Central de Operações e do Teledespacho", "Serviços"),
]

THEME_KEYS = [t[0] for t in THEMES]

# ── Inventário de fontes (arquivo .md por UF em database/markdown/) ──────────────────
REGULAMENTO_DOCS = {
    "al": {"label": "RI (Decreto nº 408/2001)", "md": "Alagoas - Regimento Interno.md"},
    "df": {"label": "RI (Portaria nº 24/2020)", "md": "Distrito Federal - Regimento Interno.md"},
    "go": {"label": "Regimento dos Serviços Interno e Operacional", "md": "Goiás - Regimento dos Serviços Interno e Operacional.md"},
    "mt": {"label": "Regulamento Geral (Portaria nº 009/BM-8/2013)", "md": "Mato Grosso - Regimento Interno.md"},
    "pa": {"label": "MINUTA de RI (Decreto em tramitação, 2026)", "md": "Pará - Regimento Interno.md"},
    "pr": {"label": "Atribuições institucionais (portal oficial)", "md": "Paraná - Regimento Interno.md"},
    "rn": {"label": "Regulamento Geral (Decreto nº 31.139/2021)", "md": "Rio Grande do Norte - Regulamento Geral (Decreto 31.139-2021).md"},
    "rs": {"label": "RI (Portaria nº 001/2025)", "md": "Rio Grande do Sul - Regimento Interno.md"},
    "se": {"label": "RISD (atual. 2022)", "md": "Sergipe - Regimento Interno.md"},
    "ba": {"label": "Norma Operacional nº 01/2021 (CBMBA)", "md": "Bahia - Regulamento de Serviço.md"},
    "rr": {"label": "INOp do Serviço Diário dos Oficiais (CBMRR)", "md": "Roraíma - Regulamento de Serviço.md"},
    "to": {"label": "Diretriz Geral do Comando Operacional (Portaria nº 003/2019/COB)", "md": "Tocantins - Regulamento de Serviço.md"},
    "al_no03": {"label": "Norma Operacional nº 03 (CBMAL)", "md": "Alagoas - Norma Operacional 03.md"},
    "al_no04": {"label": "Norma Operacional nº 04 (CBMAL)", "md": "Alagoas - Norma Operacional 04.md"},
    "al_no06": {"label": "Norma Operacional nº 06 (CBMAL)", "md": "Alagoas - Norma Operacional 06.md"},
    "al_no07": {"label": "Norma Operacional nº 07 (CBMAL)", "md": "Alagoas - Norma Operacional 07.md"},
    "al_no11": {"label": "Norma Operacional nº 11 — Canil (CBMAL)", "md": "Alagoas - Norma Operacional 11.md"},
}

# ── Fonte primária POR TEMA (decisão do panorama: nunca "MT por padrão") ─────────────
# O texto proposto da minuta parte da fonte primária; os demais estados entram como
# alternativas no comparador. Temas sem fonte adequada ficam "pendente".
PRIMARY_SOURCE = {
    "disposicoes-preliminares": "mt",
    "organizacao-geral": "mt",
    "competencias-direcao": "mt",
    "competencias-apoio-assessoramento": "mt",
    "competencias-execucao": "mt",
    "servico-operacional": "se",
    "servico-interno-dia": "se",
    "atribuicoes-funcoes": "mt",
    "disciplina-correicao": "mt",
    "uniformes-apresentacao": "se",   # parcial (Art. 53 RISD) — capítulo nasce quase todo pendente
    "cerimonial-honras": "rs",
    "ensino-instrucao": "mt",
    "seguranca-contra-incendio": "mt",
    "pessoal-quadros": "rn",
    "disposicoes-finais": "mt",
    "central-operacoes-193": "ba",  # Fase 2A: Bahia/CICOM (Supervisor e Operador de Teledespacho)
}

# ── Adaptações p/ RO (aplicadas NO BUILD apenas ao texto proposto da minuta; o
#    original fica preservado em original_text e é o que o comparador exibe) ──────────
# Pares (de, para), aplicados na ordem. Revisáveis pelo Wândrio.
ADAPTATIONS = [
    # Pares específicos primeiro (a ordem importa); genéricos por último.
    ("região metropolitana de Cuiabá/Várzea Grande", "região metropolitana de Porto Velho"),
    ("Corpo de Bombeiros Militar do Estado de Mato Grosso", "Corpo de Bombeiros Militar do Estado de Rondônia"),
    ("Corpo de Bombeiros Militar do Estado do Rio Grande do Norte", "Corpo de Bombeiros Militar do Estado de Rondônia"),
    ("Corpo de Bombeiros Militar do Estado do Rio Grande do Sul", "Corpo de Bombeiros Militar do Estado de Rondônia"),
    ("Corpo de Bombeiros Militar do Estado do Sergipe", "Corpo de Bombeiros Militar do Estado de Rondônia"),
    ("Corpo de Bombeiros Militar do Estado de Alagoas", "Corpo de Bombeiros Militar do Estado de Rondônia"),
    ("Estado de Mato Grosso", "Estado de Rondônia"),
    ("Estado do Rio Grande do Norte", "Estado de Rondônia"),
    ("Estado do Rio Grande do Sul", "Estado de Rondônia"),
    ("Estado de Alagoas", "Estado de Rondônia"),
    ("Estado de Sergipe", "Estado de Rondônia"),
    ("Estado de SERGIPE", "Estado de Rondônia"),
    ("mato-grossense", "rondoniense"),
    ("sergipano", "rondoniense"),
    ("sergipana", "rondoniense"),
    # Genéricos (depois dos específicos): pegam "…Corpo de Bombeiros Militar de Mato
    # Grosso", "…de Sergipe" etc. sem o "do Estado".
    ("Mato Grosso", "Rondônia"),
    ("Sergipe", "Rondônia"),
    ("CBMMT", "CBMRO"),
    ("CBMRN", "CBMRO"),
    ("CBMRS", "CBMRO"),
    ("CBMSE", "CBMRO"),
    ("CBMAL", "CBMRO"),
    ("CBMGO", "CBMRO"),
    ("CBMPA", "CBMRO"),
    ("CBMPR", "CBMRO"),
    ("CBMDF", "CBMRO"),
]


def adapt_text(text):
    """Aplica ADAPTATIONS; retorna (texto_adaptado, houve_mudanca)."""
    out = text
    for de, para in ADAPTATIONS:
        out = out.replace(de, para)
    return out, out != text


# ── Mescla das transcrições por estado ───────────────────────────────────────────────
# Cada scripts/regulamento_enrichment_<uf>.py define ENRICHMENT:
#   {(theme_key, state_id): [excerpt, ...]}
# excerpt = {"heading": str|None, "caput": str|None, "dispositivos": [str, ...],
#            "source": "cf. <CBM>, <label>, Art. NN", "match": "exata"|"parcial"|"tematica"}
REGULAMENTO_ENRICHMENT = {}

import importlib  # noqa: E402

for _uf in REGULAMENTO_DOCS:
    try:
        _mod = importlib.import_module(f"regulamento_enrichment_{_uf}")
    except ImportError:
        continue
    except SyntaxError as _e:
        # Arquivo em edição por outro processo/agente: avisa e segue com os demais.
        import sys as _sys
        print(f"AVISO: regulamento_enrichment_{_uf}.py com erro de sintaxe — ignorado nesta rodada ({_e})",
              file=_sys.stderr)
        continue
    for _key, _excerpts in getattr(_mod, "ENRICHMENT", {}).items():
        _theme, _state = _key
        assert _theme in THEME_KEYS, f"tema desconhecido em {_uf}: {_theme}"
        assert _state == _uf, f"state_id divergente em regulamento_enrichment_{_uf}: {_state}"
        REGULAMENTO_ENRICHMENT.setdefault(_key, []).extend(_excerpts)
