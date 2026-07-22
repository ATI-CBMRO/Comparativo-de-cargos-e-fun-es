"""Extrator determinístico da curadoria dos regulamentos (rodadas T1–T7).

Em vez de um modelo "digitar" ~800 artigos, este script CORTA o markdown-fonte por
"Art. N" e monta os arquivos scripts/regulamento_enrichment_<uf>.py mecanicamente —
extração é verbatim por construção. O MAPA artigo→tema abaixo é o dado curado
(de-paras validados em docs/curadoria/de-para-<uf>.md + panorama-cobertura.md).

Uso:  python3 scripts/extrair_regulamentos.py [uf ...]   (sem args = todos)

Regenerável e idempotente: os arquivos gerados trazem aviso de NÃO editar à mão.
Depois de rodar, conferir com: python3 scripts/verificar_verbatim.py
"""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
MD = ROOT / 'database' / 'markdown'
OUT = ROOT / 'scripts'

# ── Limpeza e parsing ────────────────────────────────────────────────────────────────

RE_NOISE = re.compile(
    r'^(## Página|\*Documento extraído|\*Total de páginas|---\s*$|\s*Página \d+ de \d+'
    r'|\s*[Pp]ágina\s+\d+\s*/\s*\d+'                 # "página 2 /18" (GO)
    r'|\s*CBMGO\s*/?\s*RESIOBOM'                     # cabeçalho corrente do PDF de GO
    r'|\s*(T[ÍI]TULO|CAP[ÍI]TULO|Cap[íi]tulo|Se[çc][ãa]o|SE[ÇC][ÃA]O|Subse[çc][ãa]o|SUBSE[ÇC][ÃA]O)\s+[IVXLC\d])'
)
# Linhas-título/cabeçalho corrente todas em maiúsculas (ex.: "DA DESTINAÇÃO, SUBORDINAÇÃO
# E COMPETÊNCIA", "REGULAMENTO GERAL DO CORPO DE BOMBEIROS MILITAR DO ESTADO DO RIO
# GRANDE DO NORTE" — este último tem 80 caracteres).
RE_TITLE_CAPS = re.compile(r'^[^a-zá-ü0-9]{8,90}$')
# Tolerante a artefatos de PDF no próprio número ("Art. 3 2."); exige "Art" maiúsculo —
# referências no corpo do texto usam "art." minúsculo.
RE_ART = re.compile(r'^\s*Art\s*\.?\s*(\d[\d\s]{0,3})\s*[ºo°\.]?')
# Marcadores de dispositivo (inciso/parágrafo/alínea/item numerado):
RE_ITEM = re.compile(
    r'^\s*(§\s*\d|Parágrafo\s+único|[IVXLCDM]{1,8}\s*[-–—\.\)]|[a-z]\s*\)|\d{1,2}(\.\d{1,2}){0,3}\s*[-–])',
)


def load_lines(filename, inline_split=False, fake_art_res=(), strip_lines=()):
    text = (MD / filename).read_text(encoding='utf-8', errors='replace')
    lines = text.splitlines()
    if inline_split:
        # Páginas extraídas em linha única (GO): quebra antes de cada "Art. N" e "Capítulo".
        quebradas = []
        for ln in lines:
            ln = re.sub(r'(?<!^)\s(?=Art\.\s*\d)', '\n', ln)
            ln = re.sub(r'(?<!^)\s(?=Cap[íi]tulo\s+[IVXLC])', '\n', ln)
            quebradas.extend(ln.split('\n'))
        lines = quebradas
    if fake_art_res:
        # Citações a artigos de OUTRAS normas que começam a linha (falsos cabeçalhos).
        lines = [re.sub(r'^(\s*)Art', r'\1art', ln)
                 if any(rx.match(ln) for rx in fake_art_res) else ln
                 for ln in lines]
    if strip_lines:
        # Continuação de cabeçalho (TÍTULO/CAPÍTULO/SEÇÃO) quebrado em 2 linhas na
        # conversão do PDF: RE_NOISE só reconhece a 1ª linha ("Capítulo VII: Da Rotina
        # Diária das Unidades"), a 2ª ("Operacionais") sobra e gruda no artigo seguinte.
        lines = [ln for ln in lines if not any(rx.match(ln.strip()) for rx in strip_lines)]
    return lines


def clean(s):
    return re.sub(r'\s+', ' ', s).strip()


def art_number(line):
    m = RE_ART.match(line)
    if not m:
        return None
    return int(m.group(1).replace(' ', ''))


# Cabeçalho de SEÇÃO NUMERADA (DOBs de AL: "1 FINALIDADE", "2. OBJETIVO" — sem "Art. N").
# Distingue de subseções ("3.1 Acesso ao sistema:", "5.1.1 Incêndios") porque estas usam
# Title Case/minúsculas, enquanto o título de 1º nível vem em CAIXA ALTA a linha inteira.
RE_SECTION = re.compile(r'^\s*(\d{1,2})\.?\s+([A-ZÀ-Ü][A-ZÀ-Ü0-9À-Ü ,/\-]{1,80})\s*$')


def split_sections(lines):
    """[(numero, titulo, [linhas do corpo])] a partir de cabeçalhos 'N TÍTULO' (maiúsculas).
    O corpo NÃO inclui a linha do cabeçalho — vira o campo 'heading' à parte."""
    out, cur_num, cur_title, cur = [], None, None, []
    for ln in lines:
        stripped = ln.strip()
        # Mesmo filtro de ruído/título do split_articles() — paridade com o
        # _fonte_limpa() de verificar_verbatim.py (senão o verbatim nunca bate).
        if RE_NOISE.match(ln) or (stripped and RE_TITLE_CAPS.match(stripped)):
            continue
        m = RE_SECTION.match(stripped) if stripped else None
        if m:
            if cur_num is not None:
                out.append((cur_num, cur_title, cur))
            cur_num, cur_title, cur = int(m.group(1)), clean(m.group(2)), []
        elif cur_num is not None:
            cur.append(ln)
    if cur_num is not None:
        out.append((cur_num, cur_title, cur))
    return out


def split_articles(lines):
    """[(numero, [linhas do artigo]), ...] — do 'Art. N' até o próximo."""
    out, cur_num, cur = [], None, []
    for ln in lines:
        if RE_NOISE.match(ln) or (ln.strip() and RE_TITLE_CAPS.match(ln.strip())):
            continue
        n = art_number(ln)
        if n is not None:
            if cur_num is not None:
                out.append((cur_num, cur))
            cur_num, cur = n, [ln]
        elif cur_num is not None:
            cur.append(ln)
    if cur_num is not None:
        out.append((cur_num, cur))
    return out


def caput_e_dispositivos(art_lines):
    """Separa caput (até o 1º marcador) dos dispositivos (um por marcador)."""
    caput_parts, dispositivos, current = [], [], None
    for ln in art_lines:
        if not ln.strip():
            continue
        if RE_ITEM.match(ln):
            if current is not None:
                dispositivos.append(clean(current))
            current = ln
        elif current is not None:
            current += ' ' + ln
        else:
            caput_parts.append(ln)
    if current is not None:
        dispositivos.append(clean(current))
    return clean(' '.join(caput_parts)), [d for d in dispositivos if d]


# ── Mapa curado: UF → {label, fonte, fatia, ranges, overrides} ───────────────────────
# ranges: lista (art_ini, art_fim, tema, match, heading). overrides: {art: (tema, match)}.
# slice_between: (marcador_inicio, marcador_fim|None) por CONTEÚDO de linha.
# line_slices (PA/DF): [(linha_ini, linha_fim, tema, match, heading)] — 1-indexado.

CONFIG = {
    'mt': {
        'md': 'Mato Grosso - Regimento Interno.md',
        'src': 'cf. CBMMT, Regulamento Geral (Portaria nº 009/BM-8/2013), Art. {n}',
        'slice_between': ('TÍTULO I', None),
        'ranges': [
            (1, 3, 'disposicoes-preliminares', 'exata', 'TÍT. I — Das Generalidades'),
            (4, 4, 'organizacao-geral', 'exata', 'TÍT. II — Da Estrutura Organizacional'),
            (5, 5, 'organizacao-geral', 'parcial', 'TÍT. II — Da Estrutura Organizacional (estrutura é a de MT; a da minuta de RO vem da LOB de RO)'),
            (6, 14, 'competencias-direcao', 'exata', 'TÍT. III, Caps. I–III — Direção Geral, Colegiada e Superior'),
            (15, 33, 'disciplina-correicao', 'exata', 'TÍT. III, Cap. III, Seção II — Corregedoria Geral'),
            (34, 59, 'competencias-apoio-assessoramento', 'exata', 'TÍT. III, Cap. IV — Assessoramento Superior'),
            (60, 159, 'competencias-direcao', 'exata', 'TÍT. III, Cap. V — Direção Setorial / EMG (DAI e Coordenadorias BM/1–BM/10)'),
            (160, 196, 'ensino-instrucao', 'exata', 'TÍT. III, Cap. V, Seção II — DEIP (Ensino, Instrução e Pesquisa)'),
            (197, 217, 'seguranca-contra-incendio', 'exata', 'TÍT. III, Cap. V, Seção III — DSCIP'),
            (218, 233, 'competencias-apoio-assessoramento', 'exata', 'TÍT. III, Cap. VI — Nível de Apoio (Gabinetes e COB)'),
            (234, 263, 'competencias-execucao', 'exata', 'TÍT. III, Cap. VII — Nível de Execução (DOp, CRBM, UBM)'),
            (264, 266, 'disposicoes-finais', 'exata', 'Disposições Finais'),
        ],
        'overrides': {
            72: ('disciplina-correicao', 'exata'), 73: ('disciplina-correicao', 'exata'),
            158: ('servico-interno-dia', 'parcial'),
            # Funções de chefia/comando dispersas → tema 8 (de-para MT, tema 8):
            **{n: ('atribuicoes-funcoes', 'exata') for n in
               [62, 63, 67, 111, 123, 137, 144, 153, 163, 164, 170, 181, 182, 190, 191,
                200, 201, 221, 222, 225, 230, 238, 239, 250, 251, 255, 256, 262, 263]},
        },
    },
    'rn': {
        'md': 'Rio Grande do Norte - Regulamento Geral (Decreto 31.139-2021).md',
        'src': 'cf. CBMRN, Regulamento Geral (Decreto nº 31.139/2021), Art. {n}',
        # Fim em 'ANEXO I' (siglas): o Regulamento em si termina no Art. 56 —
        # os anexos e o Decreto 31.140 (orçamento) que vêm depois NÃO entram.
        'slice_between': ('REGULAMENTO GERAL DO CORPO DE BOMBEIROS MILITAR DO', 'ANEXO I'),
        'ranges': [
            (1, 4, 'disposicoes-preliminares', 'exata', 'TÍT. I, Cap. I — Disposições Gerais'),
            (5, 11, 'organizacao-geral', 'exata', 'TÍT. I, Cap. II — Estrutura Organizacional'),
            (12, 18, 'competencias-direcao', 'exata', 'TÍT. II, Cap. I — Direção Superior'),
            (19, 31, 'competencias-apoio-assessoramento', 'exata', 'TÍT. II, Cap. II — Assessoramento'),
            (32, 39, 'competencias-execucao', 'exata', 'TÍT. II, Cap. III — Execução (Cmdo Op BM, DLOF)'),
            (40, 43, 'ensino-instrucao', 'parcial', 'TÍT. II, Cap. III — DGPEI (pessoas + ensino)'),
            (44, 44, 'seguranca-contra-incendio', 'exata', 'TÍT. II, Cap. III — DAT'),
            (45, 49, 'disposicoes-finais', 'exata', 'TÍT. II, Cap. IV — Prescrições Diversas'),
            (50, 56, 'pessoal-quadros', 'exata', 'TÍT. III — Do Pessoal (quadros e QOD)'),
        ],
        'overrides': {23: ('disciplina-correicao', 'parcial')},
    },
    'se': {
        'md': 'Sergipe - Regimento Interno.md',
        'src': 'cf. CBMSE, RISD (atual. 2022), Art. {n}',
        'slice_between': (None, None),
        # "Capítulo VII: Da Rotina Diária das Unidades" quebra em 2 linhas na conversão
        # do PDF; RE_NOISE só reconhece a 1ª ("Capítulo VII..."), a palavra solta
        # "Operacionais" da 2ª linha sobrava colada ao fim do Art. 53 (parág. único).
        'strip_lines': [re.compile(r'^Operacionais$')],
        'ranges': [
            (1, 4, 'servico-operacional', 'exata', 'RISD, Caps. I–IV — Finalidade, Objetivos, Políticas e Funções Operacionais'),
            (5, 22, 'atribuicoes-funcoes', 'exata', 'RISD, Cap. V — Atribuições das Funções de Serviço'),
            (23, 52, 'servico-operacional', 'exata', 'RISD, Cap. VI — Regime e Escalas de Serviço'),
            (53, 53, 'uniformes-apresentacao', 'parcial', 'RISD, Cap. VI — Uniforme destinado ao serviço'),
            (54, 111, 'servico-interno-dia', 'exata', 'RISD, Cap. VII — Rotina Diária das Unidades'),
            (112, 147, 'servico-operacional', 'exata', 'RISD, Caps. VIII–XI — Situações Extraordinárias, Viaturas, Apoio e Ocorrências'),
            (148, 150, 'disposicoes-finais', 'exata', 'RISD, Cap. XII — Disposições Gerais'),
        ],
        'overrides': {},
    },
    'go': {
        'md': 'Goiás - Regimento dos Serviços Interno e Operacional.md',
        'src': 'cf. CBMGO, Regimento dos Serviços Interno e Operacional, Art. {n}',
        'slice_between': (None, None),
        'inline_split': True,  # páginas extraídas em linha única
        'ranges': [
            (1, 1, 'disposicoes-preliminares', 'parcial', 'Cap. I — Considerações Gerais (finalidade do regimento de serviço)'),
            (2, 3, 'servico-interno-dia', 'exata', 'Cap. II — Serviços de Dia'),
            (4, 15, 'servico-operacional', 'exata', 'Cap. III — Jornada de Trabalho e Escala de Serviço'),
            (16, 21, 'atribuicoes-funcoes', 'exata', 'Cap. IV — Funções e Atribuições'),
            (22, 26, 'disposicoes-finais', 'exata', 'Cap. V — Disposições Finais'),
        ],
        'overrides': {},
    },
    'al': {
        'md': 'Alagoas - Regimento Interno.md',
        'src': 'cf. CBMAL, RI (Decreto nº 408/2001), Art. {n}',
        'slice_between': ('TÍTULO I', 'PALÁCIO MARECHAL'),
        'ranges': [
            (1, 2, 'disposicoes-preliminares', 'exata', 'TÍT. I — Finalidade, Objetivos e Competências'),
            (3, 7, 'organizacao-geral', 'exata', 'TÍT. II — Organização Geral e Estruturação'),
            (8, 11, 'competencias-direcao', 'exata', 'TÍT. III, Cap. I — Direção Geral'),
            (12, 27, 'competencias-apoio-assessoramento', 'exata', 'TÍT. III, Cap. I — Defesa Civil e Gabinete'),
            (28, 31, 'disciplina-correicao', 'exata', 'TÍT. III, Cap. I, Seção VI — Corregedoria Geral'),
            (32, 57, 'competencias-direcao', 'exata', 'TÍT. III, Cap. II — Diretorias (direção setorial)'),
            (58, 64, 'seguranca-contra-incendio', 'exata', 'TÍT. III, Cap. II, Seção IV — Diretoria de Serviços Técnicos'),
            (65, 74, 'competencias-apoio-assessoramento', 'exata', 'TÍT. III, Cap. II — Ajudância Geral e Comissões'),
            (75, 80, 'competencias-apoio-assessoramento', 'exata', 'TÍT. III, Cap. III — Órgãos de Apoio'),
            (81, 87, 'ensino-instrucao', 'exata', 'TÍT. III, Cap. III, Seção II — CFAE'),
            (88, 103, 'competencias-apoio-assessoramento', 'exata', 'TÍT. III, Cap. III — Órgãos de Apoio'),
            (104, 124, 'competencias-execucao', 'exata', 'TÍT. III, Cap. IV — Órgãos de Execução'),
            (125, 125, 'competencias-apoio-assessoramento', 'exata', 'TÍT. III, Cap. V — Órgãos Especiais'),
            (126, 127, 'disposicoes-finais', 'exata', 'Disposições Finais'),
        ],
        'overrides': {},
    },
    'rs': {
        'md': 'Rio Grande do Sul - Regimento Interno.md',
        'src': 'cf. CBMRS, RI (Portaria nº 001/2025), Art. {n}',
        'slice_between': (None, None),
        # Citação ao Decreto nº 53.897/2018 que começa a linha como "Art. 3º Inciso XIII…"
        'fake_art_res': [re.compile(r'^\s*Art\.?\s*3º?\s+Inciso XIII')],
        'ranges': [
            (1, 1, 'disposicoes-preliminares', 'exata', 'Cap. I — Competência da Corporação'),
            (2, 16, 'organizacao-geral', 'exata', 'Cap. II — Estruturação'),
            (17, 26, 'organizacao-geral', 'parcial', 'Cap. III — Estratégia Organizacional'),
            (27, 29, 'competencias-direcao', 'exata', 'Cap. IV — Cmt-G, SCmt-G e Conselho Superior'),
            (30, 30, 'disciplina-correicao', 'exata', 'Cap. IV — Corregedoria-Geral'),
            (31, 34, 'competencias-apoio-assessoramento', 'exata', 'Cap. IV — Gabinete, CAM e Departamentos de Apoio'),
            (35, 35, 'seguranca-contra-incendio', 'exata', 'Cap. IV — DSPCI'),
            (36, 36, 'ensino-instrucao', 'exata', 'Cap. IV — Academia de Bombeiro Militar'),
            (37, 37, 'competencias-apoio-assessoramento', 'exata', 'Cap. IV — AODC'),
            (38, 39, 'competencias-execucao', 'exata', 'Cap. IV — CRBM e BESCI'),
            (40, 40, 'atribuicoes-funcoes', 'exata', 'Cap. IV — Funções de direção/chefia'),
            (41, 41, 'organizacao-geral', 'parcial', 'Cap. IV — Seções e Setores'),
            (42, 42, 'seguranca-contra-incendio', 'exata', 'Cap. IV — Órgãos de SCIP'),
            (43, 44, 'competencias-execucao', 'exata', 'Cap. IV — Órgãos operacionais e Especiais'),
            (45, 45, 'ensino-instrucao', 'exata', 'Cap. IV — Órgãos de Ensino e Treinamento'),
            (46, 46, 'disciplina-correicao', 'exata', 'Cap. V — Corregedor-Geral'),
            (47, 57, 'atribuicoes-funcoes', 'exata', 'Cap. V — Atribuições das Funções'),
            (58, 65, 'disposicoes-finais', 'parcial', 'Cap. VI, Seções I–II — Regimentos Internos e Boletins'),
            (66, 72, 'servico-interno-dia', 'parcial', 'Cap. VI, Seção III — Escalas de serviços internos e externos'),
            (73, 81, 'cerimonial-honras', 'exata', 'Cap. VI, Seções IV–VIII — Formaturas, Bandeiras, Festas, Parada Diária, Galeria e Recepção/Despedida'),
            (82, 89, 'disposicoes-finais', 'parcial', 'Cap. VI, Seção IX — Sistema normativo e correspondência'),
            (90, 90, 'disposicoes-finais', 'exata', 'Disposições Finais'),
            (91, 93, 'pessoal-quadros', 'parcial', 'Disposições Finais — quadros, saúde e civis'),
            (94, 96, 'disposicoes-finais', 'exata', 'Disposições Finais'),
        ],
        'overrides': {},
    },
    # PA e DF: uso SELETIVO por fatias de linha (de-paras respectivos).
    'pa': {
        'md': 'Pará - Regimento Interno.md',
        'src': 'cf. CBMPA, MINUTA de RI (Decreto em tramitação, 2026), Art. {n}',
        'line_slices': [
            (66, 79, 'disposicoes-preliminares', 'exata', 'TÍT. I, Cap. I — Natureza e Finalidade'),
            (80, 190, 'organizacao-geral', 'exata', 'TÍT. I, Cap. II — Competência e Estrutura Organizacional'),
            (191, 706, 'competencias-direcao', 'exata', 'TÍT. I — Direção Geral (Comando-Geral, Alto Comando, EMG)'),
            (707, 730, 'competencias-apoio-assessoramento', 'exata', 'TÍT. I, Cap. V — Coordenadoria Estadual de Proteção e Defesa Civil'),
            (731, 1009, 'disciplina-correicao', 'exata', 'TÍT. I, Cap. VI — Corregedoria-Geral'),
            (1714, 1840, 'ensino-instrucao', 'exata', 'Cap. XI — Departamento-Geral de Cultura, Educação e Pesquisa'),
            (1841, 2069, 'seguranca-contra-incendio', 'exata', 'Cap. XII — Departamento-Geral de Segurança Contra Incêndios e Emergências'),
            (6204, 6220, 'disposicoes-finais', 'exata', 'Disposições Finais'),
        ],
    },
    'df': {
        'md': 'Distrito Federal - Regimento Interno.md',
        'src': 'cf. CBMDF, RI (Portaria nº 24/2020), Art. {n}',
        'line_slices': [
            (1541, 1615, 'ensino-instrucao', 'exata', 'TÍT. I, Cap. VII — Departamento de Ensino, Pesquisa, Ciência e Tecnologia'),
            (1616, 1685, 'seguranca-contra-incendio', 'exata', 'TÍT. I, Cap. VIII — Departamento de Segurança Contra Incêndio'),
            (2501, 2739, 'disciplina-correicao', 'exata', 'TÍT. I, Cap. XIV — Corregedoria'),
            (3445, 3651, 'pessoal-quadros', 'parcial', 'TÍT. II, Cap. III — Diretoria de Inativos e Pensionistas'),
        ],
    },
    # ES: Normas Gerais de Ação — "Art. N" REINICIA a cada órgão/unidade; recorte cirúrgico
    # por linha absoluta (CAT, 1º BBM como representante dos 6 batalhões, núcleo do CERD).
    'es': {
        'md': 'Espírito Santo - Normas Gerais de Ação.md',
        'src': 'cf. CBMES, Normas Gerais de Ação (2023), Art. {n}',
        'line_slices': [
            (11053, 11136, 'seguranca-contra-incendio', 'exata', 'CAT — Gerência de Vistorias e Seção de Fiscalização'),
            (12424, 12454, 'servico-operacional', 'exata', '1º BBM — Prontidão Operacional e Seção de Operações de Salvamento (SOS)'),
            # Fim ajustado para 13663 (achado da revisão): a linha 13701 original incluía um
            # trecho de organograma não numerado (§2º-§4º: Administração, SOS, 1ª Companhia)
            # colado ao fim do Art. 31 — não é dispositivo do Fiscal do Salvamar.
            (13573, 13663, 'servico-operacional', 'exata', '1º BBM — Chefe da SOS e Fiscal do Salvamar'),
            (32072, 32246, 'servico-operacional', 'exata', 'CERD — Finalidade, composição e atribuições gerais'),
        ],
    },
    # PR: coletânea do portal — blocos "Atribuições …" com numeração que REINICIA.
    'pr': {
        'md': 'Paraná - Regimento Interno.md',
        'src': 'cf. CBMPR, Atribuições institucionais (portal oficial), bloco "{bloco}", Art. {n}',
        'blocks': True,
    },
    'ba': {
        'md': 'Bahia - Regulamento de Serviço.md',
        'src': 'cf. CBMBA, Norma Operacional nº 01/2021, Art. {n}',
        'slice_between': ('R E S O L V E', None),
        # Cabeçalho de página repetido NO MEIO dos artigos (Art. 9º e 18 são longos):
        'strip_lines': [re.compile(r'^\s*NORMA OPERACIONAL\b'), re.compile(r'^\s*Pág\.\s*\d+\s*$')],
        'ranges': [
            (8, 9, 'central-operacoes-193', 'exata', 'NOp 01/2021, Seção II — Supervisor do Teledespacho (CICOM)'),
            (18, 18, 'central-operacoes-193', 'exata', 'NOp 01/2021, Seção X — Operador do Teledespacho (CICOM)'),
            (1, 1, 'disposicoes-preliminares', 'exata', 'NOp 01/2021 — objeto da Portaria'),
            (2, 2, 'disposicoes-preliminares', 'exata', 'NOp 01/2021, Cap. I — Da Finalidade'),
            (3, 3, 'disposicoes-preliminares', 'exata', 'NOp 01/2021, Cap. II — Dos Objetivos'),
            (4, 4, 'servico-operacional', 'exata', 'NOp 01/2021, Cap. III — Objetivos Básicos do Serviço Operacional'),
            (5, 5, 'organizacao-geral', 'exata', 'NOp 01/2021, Cap. IV — Das Funções Operacionais'),
            (6, 7, 'atribuicoes-funcoes', 'exata', 'NOp 01/2021, Cap. V, Seções I-II — Superior de Dia'),
            (10, 17, 'atribuicoes-funcoes', 'exata', 'NOp 01/2021, Cap. V, Seções III-IX — Supervisor a Integrantes da Guarnição'),
            (19, 19, 'disciplina-correicao', 'exata', 'NOp 01/2021, Cap. VI — Das Medidas Disciplinares'),
            (20, 25, 'servico-interno-dia', 'exata', 'NOp 01/2021, Cap. VII — Da Passagem de Serviço'),
            (26, 35, 'disposicoes-finais', 'exata', 'NOp 01/2021 — Disposições Finais'),
        ],
        'overrides': {},
    },
    'to': {
        'md': 'Tocantins - Regulamento de Serviço.md',
        'src': 'cf. CBMTO, NGA do SIOP (Diretriz COB, Portaria nº 003/2019), Art. {n}',
        # Anexo 2 reinicia a numeração em "Art. 1º"; fatiar a partir do cabeçalho do Anexo 2
        # para não colidir com os artigos homônimos do corpo principal. Marcador conferido no Step 4.
        'slice_between': ('ANEXO 2', None),
        'strip_lines': [re.compile(r'^\s*QUARTEL DO COMANDO GERAL\b')],
        'ranges': [
            (12, 14, 'central-operacoes-193', 'exata', 'NGA SIOP (Anexo 2) — Coordenador de Operações, Despachante e Atendente'),
            (1, 2, 'disposicoes-preliminares', 'exata', 'NGA SIOP (Anexo 2) — Finalidade e Missão'),
            (3, 5, 'organizacao-geral', 'exata', 'NGA SIOP (Anexo 2) — Estrutura do SIOP/BM'),
            (6, 6, 'competencias-direcao', 'exata', 'NGA SIOP (Anexo 2) — Do Gerente'),
            (7, 7, 'servico-interno-dia', 'exata', 'NGA SIOP (Anexo 2) — Regime do Serviço Administrativo'),
            (8, 8, 'atribuicoes-funcoes', 'exata', 'NGA SIOP (Anexo 2) — Atribuições do Serviço Administrativo'),
            (9, 11, 'servico-operacional', 'exata', 'NGA SIOP (Anexo 2) — Escalas do Serviço Operacional'),
            (15, 15, 'disposicoes-finais', 'exata', 'NGA SIOP (Anexo 2) — Disposição Geral'),
        ],
        'overrides': {},
    },
    # TO (corpo principal): "Art. N" do corpo principal (Anexo 1) e do Anexo 2 usam a
    # MESMA numeração (ambos começam em "Art. 1º") — colisão resolvida por corte de
    # LINHA ABSOLUTA (precedente do ES), isolando o corpo principal (Art. 1-13, 16; não
    # há Art. 14-15 aqui — só reaparecem, homônimos, dentro do Anexo 2 já extraído acima).
    'to_corpo': {
        'md': 'Tocantins - Regulamento de Serviço.md',
        'src': 'cf. CBMTO, Diretriz Geral do Comando Operacional (Portaria nº 003/2019/COB), Anexo 1, Art. {n}',
        'line_slices': [
            (204, 217, 'organizacao-geral', 'exata', 'Anexo 1, Cap. I — Comando Operacional e UBMs (Art. 1º)'),
            (218, 225, 'servico-operacional', 'exata', 'Anexo 1, Cap. I — Execução do Serviço Operacional em escalas (Art. 2º)'),
            (226, 495, 'atribuicoes-funcoes', 'exata', 'Anexo 1, Seção I e funções — Superior de Dia a Apoio Logístico (Art. 3º-11)'),
            (496, 502, 'central-operacoes-193', 'exata', 'Anexo 1 — Central de Operações do CBM/COCB (Art. 12)'),
            (503, 553, 'atribuicoes-funcoes', 'exata', 'Anexo 1 — Plantão/Comunicante/Sentinela (Art. 13)'),
            (554, 562, 'organizacao-geral', 'exata', 'Anexo 1 — Sistema Integrado de Operações, SIOP/BM (Art. 16)'),
        ],
    },
    'rr': {
        'md': 'Roraíma - Regulamento de Serviço.md',
        'src': 'cf. CBMRR, INOp 01/2024 (Serviço Diário dos Oficiais), Art. {n}',
        # 'CONCEITUAÇÃO BÁSICA' também aparece no Sumário (TOC) como substring de
        # "CAPÍTULO I – CONCEITUAÇÃO BÁSICA (art. 1º) 2"; usar o início real do Art. 1º
        # para não fatiar a partir do sumário (que não tem corpo articulado).
        'slice_between': ('Art. 1º Para fins de normatização', 'ANEXO ÚNICO'),
        'ranges': [
            (1, 1, 'disposicoes-preliminares', 'exata', 'Cap. I — Conceituação Básica'),
            (2, 2, 'atribuicoes-funcoes', 'exata', 'Cap. II, Seção I — Superior de Dia'),
            (3, 6, 'pessoal-quadros', 'exata', 'Cap. II, Seção II — Escalas (Superior de Dia)'),
            (7, 9, 'servico-interno-dia', 'exata', 'Cap. II, Seção III — Passagem de Serviço (Superior de Dia)'),
            (10, 11, 'atribuicoes-funcoes', 'exata', 'Cap. II, Seção IV — Prescrições Gerais (Superior de Dia)'),
            (12, 12, 'atribuicoes-funcoes', 'exata', 'Cap. III, Seção I — Coordenador de Dia'),
            (13, 18, 'servico-operacional', 'exata', 'Cap. III, Seção II — Poder de Pronto Emprego'),
            (19, 22, 'servico-operacional', 'exata', 'Cap. III, Seção III — Ocorrências de Defesa Civil'),
            (23, 24, 'pessoal-quadros', 'exata', 'Cap. III, Seção IV — Escalas (Coordenador de Dia)'),
            (25, 28, 'servico-interno-dia', 'exata', 'Cap. III, Seção V — Passagem de Serviço (Coordenador de Dia)'),
            (29, 33, 'atribuicoes-funcoes', 'exata', 'Cap. III, Seção VI — Prescrições Gerais (Coordenador de Dia)'),
            (34, 34, 'atribuicoes-funcoes', 'exata', 'Cap. IV, Seção I — Oficial de Dia/Comandante do Socorro'),
            (35, 35, 'servico-operacional', 'exata', 'Cap. IV, Seção II — Emprego'),
            (36, 37, 'pessoal-quadros', 'exata', 'Cap. IV, Seção III — Escalas (Oficial de Dia)'),
            (38, 40, 'servico-interno-dia', 'exata', 'Cap. IV, Seção IV — Passagem de Serviço'),
            (41, 44, 'atribuicoes-funcoes', 'exata', 'Cap. IV, Seção V — Prescrições Gerais'),
            (45, 45, 'atribuicoes-funcoes', 'exata', 'Cap. V, Seção I — Oficial de Incêndio/Salvamento/EPH'),
            (46, 47, 'pessoal-quadros', 'exata', 'Cap. V, Seção II — Escalas'),
            (48, 50, 'servico-interno-dia', 'exata', 'Cap. V, Seção III — Passagem de Serviço'),
            (51, 53, 'atribuicoes-funcoes', 'exata', 'Cap. V, Seção IV — Prescrições Gerais'),
            (54, 54, 'atribuicoes-funcoes', 'exata', 'Cap. VI, Seção I — Oficial de Comunicação'),
            (55, 56, 'pessoal-quadros', 'exata', 'Cap. VI, Seção II — Escalas'),
            (57, 59, 'servico-interno-dia', 'exata', 'Cap. VI, Seção III — Passagem de Serviço'),
            (60, 62, 'atribuicoes-funcoes', 'exata', 'Cap. VI, Seção IV — Prescrições Gerais'),
            (63, 63, 'atribuicoes-funcoes', 'exata', 'Cap. VII, Seção I — Oficial de Saúde'),
            (64, 66, 'pessoal-quadros', 'exata', 'Cap. VII, Seção II — Escalas'),
            (67, 69, 'servico-interno-dia', 'exata', 'Cap. VII, Seção III — Passagem de Serviço'),
            (70, 71, 'atribuicoes-funcoes', 'exata', 'Cap. VII, Seção IV — Prescrições Gerais'),
            (72, 72, 'disciplina-correicao', 'exata', 'Cap. VIII, Seção I — Oficial de Correições e Disciplina'),
            (73, 74, 'pessoal-quadros', 'exata', 'Cap. VIII, Seção II — Escalas'),
            (75, 76, 'servico-interno-dia', 'exata', 'Cap. VIII, Seção III — Passagem de Serviço'),
            (77, 78, 'disciplina-correicao', 'exata', 'Cap. VIII, Seção IV — Prescrições Gerais'),
            (79, 79, 'atribuicoes-funcoes', 'exata', 'Cap. IX, Seção I — Oficial de Sobreaviso'),
            (80, 82, 'pessoal-quadros', 'exata', 'Cap. IX, Seção II — Escalas'),
            (83, 84, 'servico-interno-dia', 'exata', 'Cap. IX, Seção III — Passagem de Serviço'),
            (85, 88, 'atribuicoes-funcoes', 'exata', 'Cap. IX, Seção IV — Prescrições Gerais'),
            (89, 93, 'disposicoes-finais', 'exata', 'Cap. X — Disposições Finais (deveres, competência do COCI)'),
            (94, 97, 'disposicoes-finais', 'exata', 'Casos omissos, revogação, vigência'),
        ],
        'overrides': {},
    },
    'al_no03': {
        'md': 'Alagoas - Norma Operacional 03.md',
        'src': 'cf. CBMAL, Norma Operacional nº 03, Art. {n}',
        'slice_between': (None, None),
        # Defeito do documento original: "Art. 5º" aparece duplicado (área de atuação dos
        # oficiais + depois vigência, que deveria ser "Art. 6º"). O extrator dedupe por número
        # e mantém só a 1ª ocorrência — a de vigência é descartada com aviso; Art. 6
        # (revogação) segue normalmente para disposicoes-finais.
        'ranges': [
            (1, 5, 'servico-operacional', 'exata', 'NO 03 — Escalas operacionais por função'),
            (5, 6, 'disposicoes-finais', 'exata', 'NO 03 — Vigência e revogação'),
        ],
        'overrides': {},
    },
    'al_no04': {
        'md': 'Alagoas - Norma Operacional 04.md',
        'src': 'cf. CBMAL, Norma Operacional nº 04, Art. {n}',
        'slice_between': (None, None),
        'ranges': [
            (1, 2, 'servico-interno-dia', 'exata', 'NO 04 — Cronograma diário e flexibilização'),
            (3, 4, 'disposicoes-finais', 'exata', 'NO 04 — Vigência e revogação'),
        ],
        'overrides': {},
    },
    'al_no06': {
        'md': 'Alagoas - Norma Operacional 06.md',
        'src': 'cf. CBMAL, Norma Operacional nº 06, Art. {n}',
        'slice_between': (None, None),
        'ranges': [
            (1, 3, 'servico-interno-dia', 'exata', 'NO 06 — Relatório de Serviço Diário e Mensal'),
            (4, 5, 'disposicoes-finais', 'exata', 'NO 06 — Vigência e revogação'),
        ],
        'overrides': {},
    },
    'al_no07': {
        'md': 'Alagoas - Norma Operacional 07.md',
        'src': 'cf. CBMAL, Norma Operacional nº 07, Art. {n}',
        'slice_between': (None, None),
        'ranges': [
            (1, 2, 'servico-interno-dia', 'exata', 'NO 07 — Relatório Mensal de Serviços do Posto'),
            (3, 4, 'disposicoes-finais', 'exata', 'NO 07 — Vigência e revogação'),
        ],
        'overrides': {},
    },
    'al_no11': {
        'md': 'Alagoas - Norma Operacional 11.md',
        'src': 'cf. CBMAL, Norma Operacional nº 11, Art. {n}',
        'slice_between': (None, None),
        # Cabeçalho de página repetido GRUDADO na mesma linha do "Art. N" seguinte
        # (ex.: "...Corpo de Bombeiros Militar de Alagoas    Art.  6º  A formatura..."),
        # sem quebra de linha própria — strip_lines não resolve pois não há linha
        # isolada para remover; inline_split quebra ANTES de cada "Art. N" no meio da linha.
        'inline_split': True,
        'ranges': [
            (1, 1, 'disposicoes-preliminares', 'exata', 'NO 11, Cap. I — Finalidade e objeto'),
            (2, 8, 'servico-interno-dia', 'exata', 'NO 11, Cap. II — Condições do serviço diário do Canil'),
            (9, 10, 'atribuicoes-funcoes', 'exata', 'NO 11, Cap. III — Rotina de cinotécnicos e SVR'),
            (11, 12, 'servico-interno-dia', 'exata', 'NO 11, Cap. IV — Canal de comunicação interna'),
            (13, 15, 'ensino-instrucao', 'exata', 'NO 11, Cap. V — Treinamento operacional'),
            (16, 20, 'servico-operacional', 'exata', 'NO 11, Cap. VI — Emprego e prazos de acionamento'),
            (21, 23, 'disposicoes-finais', 'exata', 'NO 11, Cap. VII — Casos omissos, revogação e vigência'),
        ],
        'overrides': {},
    },
    # DOBs de AL (sem "Art. N"): estrutura por SEÇÃO NUMERADA "1 FINALIDADE / 2 APLICAÇÃO
    # ...". Classificação por leitura integral de cada documento (2026-07-22).
    'al_dob05': {
        'md': 'Alagoas - Diretriz Operacional 05.md',
        'src': 'cf. CBMAL, DOB nº 05 (Rotina Diária dos Postos de Bombeiros, rev. 2013), seção {n}',
        'sections': True,
        'ranges': [
            (1, 1, 'disposicoes-preliminares', 'exata', 'DOB 05 — Finalidade'),
            (2, 2, 'disposicoes-preliminares', 'exata', 'DOB 05 — Aplicação'),
            (3, 3, 'servico-interno-dia', 'exata', 'DOB 05 — Condições Gerais (rotina diária do posto)'),
            (4, 4, 'servico-interno-dia', 'exata', 'DOB 05 — Atividade Diária do Serviço Operacional'),
            (5, 5, 'atribuicoes-funcoes', 'exata', 'DOB 05 — Recursos Humanos (Cmt PB, Cmt Pront, Cmt SGBM)'),
            (6, 6, 'servico-interno-dia', 'exata', 'DOB 05 — Viaturas (manutenção e conferência)'),
            (7, 7, 'servico-interno-dia', 'exata', 'DOB 05 — Equipamentos de Proteção e Segurança'),
            (8, 8, 'central-operacoes-193', 'exata', 'DOB 05 — Acionamento do Socorro'),
            (9, 9, 'servico-operacional', 'exata', 'DOB 05 — Tempo Resposta'),
            (10, 10, 'servico-operacional', 'exata', 'DOB 05 — Apoio Operacional'),
            (11, 11, 'servico-interno-dia', 'exata', 'DOB 05 — Controle (Relatório de Serviço Diário)'),
            # Seção 12 (Referências Normativas e Bibliográficas) fica de fora — bibliografia,
            # sem conteúdo normativo.
        ],
        'overrides': {},
    },
    'al_dob06': {
        'md': 'Alagoas - Diretriz Operacional 06.md',
        'src': 'cf. CBMAL, DOB nº 06 (Acionamento e Controle do Serviço, rev. 2019), seção {n}',
        'sections': True,
        # Cabeçalho de página repetido (ESTADO/SECRETARIA/CBMAL + nº da página solto), sem
        # marcador de fim de linha — sem isto, gruda NO MEIO de frases quebradas por página.
        'strip_lines': [
            re.compile(r'^ESTADO DE ALAGOAS$'),
            re.compile(r'^SECRETARIA DE ESTADO DA SEGURAN[ÇC]A P[ÚU]BLIC[OA]?$'),
            re.compile(r'^CORPO DE BOMBEIROS MILITAR( DE ALAGOAS)?$'),
            re.compile(r'^\d{1,3}$'),
        ],
        'ranges': [
            (1, 1, 'disposicoes-preliminares', 'exata', 'DOB 06 — Finalidade'),
            (2, 2, 'disposicoes-preliminares', 'exata', 'DOB 06 — Objetivo'),
            (3, 3, 'central-operacoes-193', 'exata', 'DOB 06 — Definições (glossário do 193/CIODS)'),
            (4, 4, 'central-operacoes-193', 'exata', 'DOB 06 — Aplicação (CIODS e Centros de Operações)'),
            (5, 5, 'central-operacoes-193', 'exata', 'DOB 06 — Condições Gerais (triagem, indicadores, infraestrutura)'),
            (6, 6, 'central-operacoes-193', 'exata', 'DOB 06 — Condições Específicas'),
            (7, 7, 'ensino-instrucao', 'exata', 'DOB 06 — Capacitação Específica (CIODS/COC)'),
            (8, 8, 'central-operacoes-193', 'exata', 'DOB 06 — Execução da Atividade'),
            # Seção 9 (Referências) e Anexos A-D (fluxograma, grade, órgãos de apoio, tabela
            # de despacho) ficam de fora — bibliografia/tabelas sem "Art."/dispositivo textual.
        ],
        'overrides': {},
    },
    'al_dob07': {
        'md': 'Alagoas - Diretriz Operacional 07.md',
        'src': 'cf. CBMAL, DOB nº 07 (Serviço com Cães, 2016), seção {n}',
        'sections': True,
        'ranges': [
            (1, 1, 'disposicoes-preliminares', 'exata', 'DOB 07 — Finalidade'),
            (2, 2, 'disposicoes-preliminares', 'exata', 'DOB 07 — Objetivos'),
            (3, 3, 'servico-operacional', 'exata', 'DOB 07 — Definições (serviço com cães)'),
            (4, 4, 'servico-operacional', 'exata', 'DOB 07 — Condições Gerais (funcionamento dos canis)'),
            (5, 5, 'atribuicoes-funcoes', 'exata', 'DOB 07 — Coordenações (CGSEC e COSEC)'),
            (6, 6, 'servico-operacional', 'exata', 'DOB 07 — Serviço de Busca, Resgate e Salvamento com Cães'),
            (7, 7, 'servico-operacional', 'parcial', 'DOB 07 — Desenvolvimento dos Cães (inclusão, aquisição, baixa)'),
            (8, 8, 'ensino-instrucao', 'exata', 'DOB 07 — Avaliação, Certificação e Recertificação'),
            (9, 9, 'disposicoes-finais', 'exata', 'DOB 07 — Prescrições Diversas'),
            # Seção 10 (Referências) fica de fora — bibliografia, sem conteúdo normativo.
        ],
        'overrides': {},
    },
    'al_dob08': {
        'md': 'Alagoas - Diretriz Operacional 08.md',
        'src': 'cf. CBMAL, DOB nº 08 (Serviço de Salvamento Aquático e Mergulho, 2022), seção {n}',
        'sections': True,
        # Cabeçalho de página repetido (nº solto + CBMAL + Boletim + local/data), sem
        # marcador de fim de linha — gruda no meio de frases quebradas por página.
        'strip_lines': [
            re.compile(r'^\d{1,3}$'),
            re.compile(r'^CORPO DE BOMBEIROS MILITAR DE ALAGOAS$'),
            re.compile(r'^BOLETIM GERAL OSTENSIVO'),
            re.compile(r'^MACEI[ÓO]-AL'),
        ],
        'ranges': [
            (1, 1, 'disposicoes-preliminares', 'exata', 'DOB 08 — Finalidade'),
            (2, 2, 'disposicoes-preliminares', 'exata', 'DOB 08 — Aplicação'),
            (3, 3, 'atribuicoes-funcoes', 'exata', 'DOB 08 — Definições e Atribuições (Cmt Prontidão a Fiel)'),
            (4, 4, 'servico-operacional', 'exata', 'DOB 08 — Condições Gerais (subsistemas de salvamento aquático)'),
            (5, 5, 'servico-operacional', 'exata', 'DOB 08 — Condições Específicas'),
            (6, 6, 'pessoal-quadros', 'exata', 'DOB 08 — Recursos Humanos (guarda-vidas e mergulhadores)'),
            (7, 7, 'servico-operacional', 'exata', 'DOB 08 — Recursos Materiais (viaturas e equipamentos)'),
            (8, 8, 'servico-operacional', 'exata', 'DOB 08 — Serviço de Salvamento Aquático'),
            (9, 9, 'servico-operacional', 'exata', 'DOB 08 — Serviço de Mergulho'),
            # "REFERÊNCIAS" ao final não tem numeral próprio — cai fora naturalmente.
        ],
        'overrides': {},
    },
    'risg': {
        'md': 'RISG.md',
        'src': 'cf. Exército Brasileiro, RISG — R-1 (Portaria SGEx nº 51/2003), Art. {n}',
        'slice_between': ('TÍTULO I', None),
        'ranges': [
            (321, 327, 'cerimonial-honras', 'exata', 'Tít. VI, Cap. I — Dos Símbolos Nacionais'),
            (337, 343, 'cerimonial-honras', 'exata', 'Tít. VI, Cap. IV — Das Festas Nacionais e Militares'),
            (344, 348, 'cerimonial-honras', 'parcial', 'Tít. VI, Cap. IV — Datas específicas do Exército (estrutura reaproveitável)'),
            (461, 462, 'cerimonial-honras', 'parcial', 'Tít. IX, Cap. VIII — Das Honras Militares (remete a outro regulamento)'),
            (364, 375, 'pessoal-quadros', 'exata', 'Tít. VIII, Cap. I — Do Cargo e da Função Militar'),
            (376, 385, 'pessoal-quadros', 'exata', 'Tít. VIII, Cap. II, Seções I-II — Substituições (normas gerais e guarnições)'),
            (391, 410, 'pessoal-quadros', 'exata', 'Tít. VIII, Cap. II, Seções IV-V — Substituições entre oficiais e praças'),
            (411, 414, 'pessoal-quadros', 'exata', 'Tít. VIII, Cap. III — Da Qualificação das Praças'),
        ],
        'overrides': {},
    },
}

PR_BLOCK_THEME = [
    (re.compile(r'corregedoria', re.I), 'disciplina-correicao', 'exata'),
    (re.compile(r'funcionais', re.I), 'atribuicoes-funcoes', 'exata'),
]
PR_DEFAULT = ('competencias-apoio-assessoramento', 'exata')
PR_TAIL = ('competencias-execucao', 'parcial', 'Organização operacional (trechos: CRBM, BBM, Cia Ind.)')


def theme_for(cfg, n):
    if n in cfg.get('overrides', {}):
        t, m = cfg['overrides'][n]
        heading = next((h for a, b, _, _, h in cfg['ranges'] if a <= n <= b), None)
        return t, m, heading
    for a, b, t, m, h in cfg['ranges']:
        if a <= n <= b:
            return t, m, h
    return None


def slice_lines(lines, cfg):
    start_marker, end_marker = cfg.get('slice_between', (None, None))
    ini, fim = 0, len(lines)
    if start_marker:
        for i, ln in enumerate(lines):
            if start_marker in ln:
                ini = i
                break
    if end_marker:
        for i in range(ini, len(lines)):
            if end_marker in lines[i]:
                fim = i
                break
    return lines[ini:fim]


def build_excerpt(n, art_lines, src_tpl, match, heading, bloco=None):
    caput, dispositivos = caput_e_dispositivos(art_lines)
    src = src_tpl.format(n=n, bloco=bloco or '')
    return {'heading': heading, 'caput': caput, 'dispositivos': dispositivos,
            'source': src, 'match': match}


def load_for(cfg):
    return load_lines(cfg['md'], inline_split=cfg.get('inline_split', False),
                      fake_art_res=cfg.get('fake_art_res', ()),
                      strip_lines=cfg.get('strip_lines', ()))


def extract_ranges(uf, cfg):
    lines = slice_lines(load_for(cfg), cfg)
    enrichment, vistos = {}, set()
    for n, art_lines in split_articles(lines):
        if n in vistos:
            print(f'  AVISO {uf}: Art. {n} repetido na fatia — mantido só o primeiro')
            continue
        info = theme_for(cfg, n)
        if info is None:
            print(f'  AVISO {uf}: Art. {n} fora de qualquer range — ignorado')
            continue
        vistos.add(n)
        tema, match, heading = info
        enrichment.setdefault((tema, uf), []).append(
            build_excerpt(n, art_lines, cfg['src'], match, heading))
    return enrichment, len(vistos)


def extract_line_slices(uf, cfg):
    lines = load_for(cfg)
    enrichment, total = {}, 0
    for ini, fim, tema, match, heading in cfg['line_slices']:
        for n, art_lines in split_articles(lines[ini - 1:fim]):
            enrichment.setdefault((tema, uf), []).append(
                build_excerpt(n, art_lines, cfg['src'], match, heading))
            total += 1
    return enrichment, total


def extract_sections(uf, cfg):
    """DOBs de AL (sem 'Art. N'): unidade = SEÇÃO NUMERADA de 1º nível. 'heading' vem do
    próprio título da seção (fonte: '{titulo} — Seção {n}'); caput/dispositivos reaproveitam
    caput_e_dispositivos() (mesma separação por marcador de item usada nos "Art. N")."""
    lines = slice_lines(load_for(cfg), cfg)
    enrichment, total = {}, 0
    for n, titulo, body in split_sections(lines):
        info = theme_for(cfg, n)
        if info is None:
            print(f'  AVISO {uf}: seção {n} ({titulo}) fora de qualquer range — ignorada')
            continue
        tema, match, heading = info
        caput, dispositivos = caput_e_dispositivos(body)
        if not caput and not dispositivos:
            print(f'  AVISO {uf}: seção {n} ({titulo}) sem conteúdo — ignorada')
            continue
        src = cfg['src'].format(n=n)
        enrichment.setdefault((tema, uf), []).append(
            {'heading': heading or f'Seção {n} — {titulo}', 'caput': caput,
             'dispositivos': dispositivos, 'source': src, 'match': match})
        total += 1
    return enrichment, total


def extract_pr(uf, cfg):
    lines = load_for(cfg)
    enrichment, total = {}, 0
    bloco, buf = None, []

    def flush():
        nonlocal total
        if not buf:
            return
        if bloco is None:
            tema, match, heading = PR_TAIL
            nome = heading
        else:
            nome = bloco
            tema, match = PR_DEFAULT
            for rx, t, m in PR_BLOCK_THEME:
                if rx.search(bloco):
                    tema, match = t, m
                    break
            heading = bloco
        for n, art_lines in split_articles(buf):
            enrichment.setdefault((tema, uf), []).append(
                build_excerpt(n, art_lines, cfg['src'], match, heading, bloco=nome))
            total += 1

    for ln in lines:
        if re.match(r'^\s*Atribuições\b', ln):
            flush()
            bloco, buf = clean(ln), []
        else:
            buf.append(ln)
    flush()
    return enrichment, total


def emit(uf, enrichment):
    path = OUT / f'regulamento_enrichment_{uf}.py'
    parts = [
        f'# GERADO por scripts/extrair_regulamentos.py — NÃO editar à mão.',
        f'# Fonte: {CONFIG[uf]["md"]} (extração determinística; mapa nos de-paras).',
        'ENRICHMENT = {',
    ]
    for key in sorted(enrichment):
        parts.append(f'    {key!r}: [')
        for ex in enrichment[key]:
            parts.append('        {')
            for campo in ('heading', 'caput', 'dispositivos', 'source', 'match'):
                parts.append(f'            {campo!r}: {ex[campo]!r},')
            parts.append('        },')
        parts.append('    ],')
    parts.append('}')
    path.write_text('\n'.join(parts) + '\n', encoding='utf-8')
    return path


def main(ufs):
    for uf in ufs:
        cfg = CONFIG[uf]
        if cfg.get('blocks'):
            enrichment, total = extract_pr(uf, cfg)
        elif 'line_slices' in cfg:
            enrichment, total = extract_line_slices(uf, cfg)
        elif cfg.get('sections'):
            enrichment, total = extract_sections(uf, cfg)
        else:
            enrichment, total = extract_ranges(uf, cfg)
        path = emit(uf, enrichment)
        temas = {k[0]: len(v) for k, v in sorted(enrichment.items())}
        print(f'{uf}: {total} artigos -> {path.name} | ' +
              ', '.join(f'{t}={c}' for t, c in temas.items()))


if __name__ == '__main__':
    alvo = [a.lower() for a in sys.argv[1:]] or list(CONFIG)
    main(alvo)
