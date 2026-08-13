"""Curadoria dos regulamentos estaduais para a minuta do Regulamento do CBMRO.

ARQUIVO-MESTRE: define a taxonomia de temas, o inventário de fontes, a fonte primária
por tema e a tabela de adaptações para RO, e MESCLA as transcrições por estado
(scripts/regulamento_enrichment_<uf>.py — um arquivo por estado, escritos na
transcrição das rodadas T1–T7; ver docs/curadoria/panorama-cobertura.md).

Disciplina (B1-M): só entra dispositivo VERBATIM do markdown de origem, com rótulo de
fonte e nível de correspondência (`match`). scripts/verificar_verbatim.py confere tudo.
"""

import re

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
    "mt": {"label": "Regulamento Geral (Portaria nº 009/BM-8/2013)", "md": "Mato Grosso - Regulamento Geral.md"},
    "pa": {"label": "MINUTA de RI (Decreto em tramitação, 2026)", "md": "Pará - Regimento Interno.md"},
    "pr": {"label": "Atribuições institucionais (portal oficial)", "md": "Paraná - Regimento Interno.md"},
    "rn": {"label": "Regulamento Geral (Decreto nº 31.139/2021)", "md": "Rio Grande do Norte - Regulamento Geral (Decreto 31.139-2021).md"},
    "rs": {"label": "RI (Portaria nº 001/2025)", "md": "Rio Grande do Sul - Regimento Interno.md"},
    "se": {"label": "RISD (atual. 2022)", "md": "Sergipe - Regulamento Interno.md"},
    "ba": {"label": "Norma Operacional nº 01/2021 (CBMBA)", "md": "Bahia - Regulamento de Serviço.md"},
    "rr": {"label": "INOp do Serviço Diário dos Oficiais (CBMRR)", "md": "Roraíma - Regulamento de Serviço.md"},
    "to": {"label": "Diretriz Geral do Comando Operacional (Portaria nº 003/2019/COB)", "md": "Tocantins - Regulamento de Serviço.md"},
    "to_corpo": {"label": "Diretriz Geral do Comando Operacional, Anexo 1 (Portaria nº 003/2019/COB)", "md": "Tocantins - Regulamento de Serviço.md"},
    "al_no03": {"label": "Norma Operacional nº 03 (CBMAL)", "md": "Alagoas - Norma Operacional 03.md"},
    "al_no04": {"label": "Norma Operacional nº 04 (CBMAL)", "md": "Alagoas - Norma Operacional 04.md"},
    "es": {"label": "Normas Gerais de Ação (2023)", "md": "Espírito Santo - Normas Gerais de Ação.md"},
    "al_no06": {"label": "Norma Operacional nº 06 (CBMAL)", "md": "Alagoas - Norma Operacional 06.md"},
    "al_no07": {"label": "Norma Operacional nº 07 (CBMAL)", "md": "Alagoas - Norma Operacional 07.md"},
    "al_no11": {"label": "Norma Operacional nº 11 — Canil (CBMAL)", "md": "Alagoas - Norma Operacional 11.md"},
    "risg": {"label": "RISG — R-1 do Exército Brasileiro (Portaria SGEx nº 51/2003)", "md": "RISG.md"},
    "al_dob05": {"label": "DOB nº 05 — Rotina Diária dos Postos de Bombeiros (CBMAL, rev. 2013)", "md": "Alagoas - Diretriz Operacional 05.md"},
    "al_dob06": {"label": "DOB nº 06 — Acionamento e Controle do Serviço (CBMAL, rev. 2019)", "md": "Alagoas - Diretriz Operacional 06.md"},
    "al_dob07": {"label": "DOB nº 07 — Serviço com Cães (CBMAL, 2016)", "md": "Alagoas - Diretriz Operacional 07.md"},
    "al_dob08": {"label": "DOB nº 08 — Serviço de Salvamento Aquático e Mergulho (CBMAL, 2022)", "md": "Alagoas - Diretriz Operacional 08.md"},
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
#
# AUDITORIA 2026-08-13: a tabela cobria 9 estados (MT, RN, RS, SE, AL, GO, PA, PR, DF) e
# NÃO cobria a BAHIA — que é a fonte primária de 'central-operacoes-193' (ver
# PRIMARY_SOURCE acima). Resultado: aquele capítulo saía com ZERO adaptações e vazava
# "CBMBA" para dentro da minuta de RO. Regras da Bahia acrescentadas abaixo. Ao eleger uma
# nova fonte primária em PRIMARY_SOURCE, confira se o estado tem regra AQUI.
ADAPTATIONS = [
    # Pares específicos primeiro (a ordem importa); genéricos por último.
    ("região metropolitana de Cuiabá/Várzea Grande", "região metropolitana de Porto Velho"),
    ("Corpo de Bombeiros Militar do Estado de Mato Grosso", "Corpo de Bombeiros Militar do Estado de Rondônia"),
    ("Corpo de Bombeiros Militar do Estado do Rio Grande do Norte", "Corpo de Bombeiros Militar do Estado de Rondônia"),
    ("Corpo de Bombeiros Militar do Estado do Rio Grande do Sul", "Corpo de Bombeiros Militar do Estado de Rondônia"),
    ("Corpo de Bombeiros Militar do Estado do Sergipe", "Corpo de Bombeiros Militar do Estado de Rondônia"),
    ("Corpo de Bombeiros Militar do Estado de Alagoas", "Corpo de Bombeiros Militar do Estado de Rondônia"),
    ("Corpo de Bombeiros Militar do Estado da Bahia", "Corpo de Bombeiros Militar do Estado de Rondônia"),
    ("Estado de Mato Grosso", "Estado de Rondônia"),
    ("Estado da Bahia", "Estado de Rondônia"),
    ("Estado do Rio Grande do Norte", "Estado de Rondônia"),
    ("Estado do Rio Grande do Sul", "Estado de Rondônia"),
    ("Estado de Alagoas", "Estado de Rondônia"),
    ("Estado de Sergipe", "Estado de Rondônia"),
    ("Estado de SERGIPE", "Estado de Rondônia"),
    ("mato-grossense", "rondoniense"),
    ("sergipano", "rondoniense"),
    ("sergipana", "rondoniense"),
    ("baiano", "rondoniense"),
    ("baiana", "rondoniense"),
    # Genéricos (depois dos específicos): pegam "…Corpo de Bombeiros Militar de Mato
    # Grosso", "…de Sergipe" etc. sem o "do Estado".
    ("Mato Grosso", "Rondônia"),
    ("Sergipe", "Rondônia"),
    ("Bahia", "Rondônia"),
    # Polícia Militar do estado de origem: o RISD do CBMSE manda acionar a "PMSE" em
    # ocorrência com vítima de crime — no texto de RO isso mandava chamar a PM de outro
    # estado. A LOB de RO (Art. 61) não usa sigla; escreve por extenso. Auditoria 2026-08-13.
    ("PMSE", "Polícia Militar do Estado de Rondônia"),
    # A minuta importada do CBMMT vincula o Corpo de Bombeiros à "Secretaria de Estado de
    # Segurança Pública" (a pasta do Mato Grosso). Em Rondônia é a SESDEC — Secretaria de
    # Estado de Segurança, Defesa e Cidadania (LOB Art. 1º, parágrafo único). Resíduo T1
    # do handoff 2026-08-13, marcado como seguro por não depender de decisão de mérito.
    ("Secretaria de Estado de Segurança Pública", "SESDEC"),
    # Resíduos T1 do handoff 2026-08-13, respondidos pelo Ten. Tiago (conhecimento
    # institucional do CBMRO, não deduzido): a minuta importada do CBMSE cita o órgão
    # ambiental de Sergipe e o sistema de processo eletrônico do CBMSE.
    ("ADEMA", "SEDAM"),
    ("e-doc", "SEI"),
    # "CICOM" é o centro de comunicações da Bahia (fonte primária do capítulo 193).
    # Confirmado pelo Ten. Tiago: o CBMRO opera dois CIOP (Centro Integrado de
    # Operações) — um em Porto Velho (ocorrências do COB I) e outro em Ji-Paraná
    # (COB II). Troca só o NOME do centro; a divisão operacional por COB não está
    # codificada texto a texto (pendência de redação — ver handoff 2026-08-13).
    # "CICOM" só ocorre no arquivo da Bahia, então não vaza para outros capítulos.
    ("CICOM", "CIOP"),
    # ── ESTRUTURA ORGANIZACIONAL (2026-08-13) ────────────────────────────────────────
    # Até aqui a tabela só trocava NOME DE ESTADO. A curadoria, porém, importou junto a
    # ESTRUTURA de MT/SE/BA: a minuta descrevia o organograma daqueles CBMs com o nome do
    # CBMRO. As regras abaixo corrigem os órgãos cuja correspondência em Rondônia é
    # INEQUÍVOCA na lei — conferidas contra a Lei 2.204/2009, o Decreto 21.425/2016 e o
    # organograma oficial do CBMRO, validadas pelo Ten. Tiago.
    # O que depende de decisão de mérito (Pelotão, capítulo da CAT, CIOP/COB, funções da
    # NOp da Bahia) fica DE FORA de propósito — ver .claude/PENDENCIAS.md.
    #
    # ⚠️ NÃO acrescentar aqui uma regra para a palavra solta "Companhia": em
    # servico-operacional as 4 ocorrências são CONCESSIONÁRIAS (energia, água, elevador,
    # seguradora) e "Companhia de Comando e Serviços" EXISTE em RO (LOB Art. 25). Só
    # entram as formas que trazem "Bombeiro Militar" ou a sigla. Armadilha AR-01.
    #
    # Comando operacional — RO NÃO tem Comando Regional/CRBM (nome do MT). Tem COB I
    # (Porto Velho) e COB II (Ji-Paraná), subordinados operacionalmente ao
    # Subcomandante-Geral (LOB Art. 35 + organograma). "Diretoria Operacional" é o nome
    # do MT para o mesmo órgão. Plurais e variantes antes das formas curtas.
    ("Comandantes Regionais Adjuntos", "Comandantes Operacionais de Bombeiros Adjuntos"),
    ("Comandante Regional Adjunto", "Comandante Operacional de Bombeiros Adjunto"),
    ("Comandantes Regionais", "Comandantes Operacionais de Bombeiros"),
    ("Comandante Regional", "Comandante Operacional de Bombeiros"),
    ("Comandos Regionais Bombeiro Militar", "Comandos Operacionais de Bombeiros"),
    ("Comando Regionais Bombeiro Militar", "Comandos Operacionais de Bombeiros"),
    ("Comandos Regionais de Bombeiros Militares", "Comandos Operacionais de Bombeiros"),
    ("Comandos Regionais do Corpo de Bombeiros", "Comandos Operacionais de Bombeiros"),
    ("Comandos Regionais", "Comandos Operacionais de Bombeiros"),
    ("Comando de Regional", "Comando Operacional de Bombeiros"),
    ("Comando Regional", "Comando Operacional de Bombeiros"),
    ("CRBM", "COB"),
    ("Diretoria de Operacional", "Comando Operacional de Bombeiros"),
    ("Diretoria Operacional", "Comando Operacional de Bombeiros"),
    ("Diretor Operacional", "Comandante Operacional de Bombeiros"),
    ("Diretoria de Operações", "Comando Operacional de Bombeiros"),
    ("Diretor de Operações", "Comandante Operacional de Bombeiros"),
    # Unidades — a cadeia do CBMRO é COB → GBM → SGBM (LOB Art. 47 e §1º; organograma).
    # "Batalhão"/"Companhia BM" são os degraus do MT. O degrau abaixo do SGBM na lei é
    # "Seção de Bombeiros" (Art. 47, V), mas "Pelotão" NÃO é convertido aqui: a cadeia
    # confirmada pelo Ten. Tiago para o CBMRO para no SGBM, e inventar o 4º nível seria
    # repetir o erro que esta rodada corrige. Pendência registrada.
    ("Batalhão Bombeiro Militar (BBM)", "Grupamento de Bombeiro Militar (GBM)"),
    ("Companhias Independente Bombeiro Militar - CIBM", "Subgrupamentos de Bombeiros Militar - SGBM"),
    ("Companhia Independente Bombeiro Militar (CIBM)", "Subgrupamento de Bombeiros Militar (SGBM)"),
    ("Companhias de Bombeiro Militar – CiaBM", "Subgrupamentos de Bombeiros Militar – SGBM"),
    ("Companhias Bombeiro Militar- CiaBM", "Subgrupamentos de Bombeiros Militar - SGBM"),
    ("CiaBM", "SGBM"),
    ("Batalhão", "Grupamento"),
    # A lei de RO diz OBM (Organização Bombeiro Militar, Art. 3º e Art. 60); "UBM"
    # (Unidade Bombeiro Militar) é o termo do MT. Conferido: "UBM" nunca aparece dentro
    # de outra palavra, então a troca não colide (a forma plural "UBMs" segue junto).
    ("UBM", "OBM"),
    # RO não tem "Comandante-Geral Adjunto": tem SUBCOMANDANTE-GERAL (LOB Art. 12),
    # que é o substituto eventual do Comandante-Geral — exatamente a função que o texto
    # do MT descreve. Confirmado no organograma oficial.
    # As duas grafias aparecem na fonte (com e sem hífen) — a segunda escapou na
    # primeira rodada desta correção.
    ("Comandante-Geral Adjunto", "Subcomandante-Geral"),
    ("Comandante Geral Adjunto", "Subcomandante-Geral"),
    # Vazamento clássico: a adaptação trocou "Mato Grosso"→"Rondônia" mas deixou a SIGLA
    # do estado de origem, produzindo "Secretaria ... do Estado de Rondônia (SSP/MT)".
    # A pasta em RO é a SESDEC (LOB Art. 1º, par. único).
    ("SSP/MT", "SESDEC"),
    ("CBMMT", "CBMRO"),
    ("CBMBA", "CBMRO"),
    ("CBMRN", "CBMRO"),
    ("CBMRS", "CBMRO"),
    ("CBMSE", "CBMRO"),
    ("CBMAL", "CBMRO"),
    ("CBMGO", "CBMRO"),
    ("CBMPA", "CBMRO"),
    ("CBMPR", "CBMRO"),
    ("CBMDF", "CBMRO"),
]


# Siglas de corporação de OUTROS estados, tolerando o separador que aparecer entre "CBM"
# e a UF: "CBMMT", "CBM-MT", "CBM- MT", "CBM.MT", "CBM/MT". A tabela ADAPTATIONS acima
# casa texto literal e, por isso, deixava passar toda variante com separador — foi assim
# que "CBM-MT" sobreviveu em 6 dispositivos (inclusive no híbrido "Corpo de Bombeiros
# Militar do Estado de Rondônia/CBM-MT"). "RO" fica FORA da lista de propósito: a sigla
# do próprio CBMRO nunca pode ser reescrita. Auditoria 2026-08-13.
_UF_OUTRAS = ('MT|SE|BA|RN|RS|AL|GO|PA|PR|DF|ES|RR|TO|AC|AM|AP|MA|PI|CE|PB|PE|MG|SP|RJ|MS|SC')
RE_SIGLA_OUTRA_UF = re.compile(r'\bCBM[\s.\-–—/]*(?:' + _UF_OUTRAS + r')\b')


# ── Ruído de página (não é norma; é mobília do PDF de origem) ────────────────────────
# O RISD do CBMSE foi extraído com o rodapé de cada página embutido NO MEIO das frases,
# ex.: "…mediante autorização por escrito 14/28 BGO Nº 060 Publicado em 30/03/2022
# CBMSE/RISD – Regulamento Interno dos Serviços Diários. do Diretor Operacional…".
# Dois estragos: (1) parte a frase ao meio; (2) a adaptação trocava "CBMSE" por "CBMRO"
# ali dentro e passava a AFIRMAR, na minuta de RO, a existência de um Boletim Geral nº 060
# de 30/03/2022 do CBMRO e de um "RISD" — atos que não existem. Citação fabricada dentro
# de texto normativo.
#
# A limpeza é feita AQUI, no build, e NÃO na transcrição: o rodapé está mesmo no markdown
# de origem, e scripts/verificar_verbatim.py compara a transcrição com ele. Tirar da
# transcrição quebraria essa conferência; tirar no build mantém as duas coisas certas —
# a transcrição fiel à fonte e a minuta livre do lixo. Auditoria 2026-08-13.
RUIDO_DE_PAGINA = [
    re.compile(
        r'\s*\d{1,3}\s*/\s*28\s+BGO\s+N[ºo°]\s*060\s+Publicado\s+em\s+30/03/2022\s+'
        r'CBM\w{2}\s*/\s*RISD\s*[–—-]\s*Regulamento\s+Interno\s+dos\s+Servi[çc]os\s+Di[áa]rios\.\s*'
    ),
]


def limpar_ruido_de_pagina(text):
    """Remove rodapé/cabeçalho de página que a extração do PDF deixou no meio do texto."""
    out = text or ''
    for rx in RUIDO_DE_PAGINA:
        out = rx.sub(' ', out)
    return re.sub(r'[ \t]{2,}', ' ', out).strip()


def adapt_text(text):
    """Aplica ADAPTATIONS; retorna (texto_adaptado, houve_mudanca)."""
    out = limpar_ruido_de_pagina(text)
    for de, para in ADAPTATIONS:
        out = out.replace(de, para)
    out = RE_SIGLA_OUTRA_UF.sub('CBMRO', out)
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
