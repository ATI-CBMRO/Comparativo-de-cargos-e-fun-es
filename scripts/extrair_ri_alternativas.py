"""Extrator determinístico da curadoria do Bloco D (comparador do Regimento Interno).

Mesmo espírito de scripts/extrair_regulamentos.py: em vez de digitar os excertos à
mão, este script CORTA o markdown-fonte por "Art. N" e monta
scripts/ri_alternativas_enrichment.py mecanicamente — extração é verbatim por
construção. A diferença de propósito: aqui o mapa curado é ÓRGÃO (organKey de
minuta_structure.json) -> {uf -> [artigos citados]}, não tema; e por decisão de
produto o excerto é sempre o ARTIGO COMPLETO (caput + todos os dispositivos), nunca
só o inciso aproveitado na minuta.

Fontes da curadoria (leitura obrigatória, ver docstrings de cada CITATION abaixo):
  - docs/curadoria/bloco-d-classificacao-al-df-pr-pa.md  (AL/DF/PR/PA, Tarefas 1 e 3)
  - docs/curadoria/de-para-ri-rs.md                       (RS, Tarefa 2)

Reusa load_lines/split_articles/caput_e_dispositivos/clean/art_number de
extrair_regulamentos.py — não duplica a lógica de parsing.

Uso:  python3.12 scripts/extrair_ri_alternativas.py
Gera: scripts/ri_alternativas_enrichment.py (aviso de NÃO editar à mão no topo).
"""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
MD = ROOT / 'database' / 'markdown'
OUT = ROOT / 'scripts'

sys.path.insert(0, str(Path(__file__).resolve().parent))
from extrair_regulamentos import load_lines, split_articles, caput_e_dispositivos, clean, art_number  # noqa: E402

# ── Metadados por estado (name/abbr fixos; docLabel varia por CITATION pois um   ──
# ── mesmo estado pode ter mais de uma fonte documental, ex. PR: LOB × RI-portal) ──
STATE_META = {
    'al': {'name': 'Alagoas', 'abbr': 'AL'},
    'df': {'name': 'Distrito Federal', 'abbr': 'DF'},
    'pr': {'name': 'Paraná', 'abbr': 'PR'},
    'pa': {'name': 'Pará', 'abbr': 'PA'},
    'rs': {'name': 'Rio Grande do Sul', 'abbr': 'RS'},
}

MD_FILE = {
    'al': 'Alagoas - Regimento Interno.md',
    'df': 'Distrito Federal - Regimento Interno.md',
    'pa': 'Pará - Regimento Interno.md',
    'rs': 'Rio Grande do Sul - Regimento Interno.md',
    # PR tem 2 documentos-fonte (achado nº 1 do briefing) — resolvido por CITATION,
    # não por uf: cada CITATION do pr aponta pro arquivo certo em '_md'.
}

PR_LOB_MD = 'Paraná - Organização Básica.md'
PR_RI_MD = 'Paraná - Regimento Interno.md'

DOC_LABEL = {
    ('al', 'ri'): 'RI (Decreto nº 408/2001)',
    ('df', 'ri'): 'RI (Portaria nº 24/2020)',
    ('pa', 'ri'): 'MINUTA de RI (Decreto em tramitação, 2026)',
    ('pa', 'lob'): 'Lei nº 11.060/2025',
    ('rs', 'ri'): 'RI (Portaria nº 001/2025)',
    ('pr', 'lob'): 'Organização Básica (Lei nº 22.206/2024)',
    ('pr', 'ri'): 'RI (coletânea do portal)',
}


def clean_lines_generic(filename):
    """Lê e limpa ruído de PDF (cabeçalhos correntes, rodapés de página, títulos em
    caixa alta) reusando as mesmas regras de RE_NOISE/RE_TITLE_CAPS do extrator do
    Regulamento, sem aplicar nenhum slice — aqui cada CITATION já sabe seu artigo."""
    from extrair_regulamentos import RE_NOISE, RE_TITLE_CAPS
    lines = load_lines(filename)
    return [ln for ln in lines
            if not (RE_NOISE.match(ln) or (ln.strip() and RE_TITLE_CAPS.match(ln.strip())))]


_CACHE = {}


def articles_of(filename):
    if filename not in _CACHE:
        lines = clean_lines_generic(filename)
        arts = {}
        vistos_dup = set()
        for n, art_lines in split_articles(lines):
            if n in arts and n not in vistos_dup:
                vistos_dup.add(n)
                print(f'  AVISO {filename}: Art. {n} repetido — mantido só o primeiro')
                continue
            arts.setdefault(n, art_lines)
        _CACHE[filename] = arts
    return _CACHE[filename]


# ── Correção manual: "Paraná - Organização Básica.md" tem um defeito sistemático de
# conversão de PDF — os números "Art. N." saem AGRUPADOS no rodapé de cada página,
# desconectados do corpo do artigo (ex.: linhas 348-351 têm só "Art. 25."···"Art. 28."
# em sequência, sem texto; o texto de cada artigo aparece ANTES/DEPOIS do cluster,
# sem marcador). split_articles() não consegue reconstruir a correspondência
# núm.->texto nessa região; confirmado por leitura manual do markdown (linhas
# 340-403). Os 3 artigos citados pela curadoria que caem nessa região (28, 29, 35)
# são então fatiados aqui por INTERVALO DE LINHA, verificado manualmente contra o
# texto (os itens batem com _PR_DP/_PR_BBM/_PR_CIBM/_PR_GOST/_PR_UOA já existentes
# em scripts/minuta_enrichment.py, extraídos à mão na mesma leitura anterior).
# Ranges começam DEPOIS do título da Subseção/Seção (que vira o `heading` do
# excerpt, não faz parte do caput) e excluem o rodapé de página específico deste
# PDF ("DD/MM/AAAA, HH:MM Lei Ordinária..." + URL), que RE_NOISE não reconhece.
# Caso especial do Art. 35: o caput ("Em razão dos diferentes objetivos...") começa
# quebrado por um bug de espaçamento bem no fim da página 9 (linhas 454-455:
# "empregadosparaocumprimentodessamissão..." — palavras grudadas), e o próprio
# extrator de PDF RE-IMPRIME a mesma frase de forma limpa como 1ª linha da página
# seguinte (linhas 468-469: "empregados para o cumprimento dessa missão...",
# confirmado por leitura manual) — por isso o range começa em 468, pulando o
# fragmento quebrado em vez de tentar consertá-lo.
_PR_LOB_LINE_OVERRIDES = {
    28: (343, 362),  # Subseção I — Da Diretoria de Pessoal (caput + incisos I-V)
    29: (365, 369),  # Subseção II — Da Diretoria de Apoio Logístico e Finanças (caput + incisos I-IV)
    35: (468, 509),  # Seção Única — Das Unidades e Subunidades de Bombeiro Militar (caput + I-IV + §§1-2)
}
_RE_PR_LOB_FOOTER = re.compile(r'^\s*\d{2}/\d{2}/\d{4},\s*\d{2}:\d{2}\s|^\s*https://leisestaduais\.com\.br')


# Abertura verbatim do caput do Art. 35, tomada da linha 454 (o fragmento quebrado
# antes do bug de espaçamento) — usada só para PREPOR ao texto limpo que recomeça
# na linha 468, sem duplicar nem reescrever nada.
_PR_ART35_CAPUT_PREFIX = 'Em razão dos diferentes objetivos da missão bombeiro-militar, da diversidade de processos a serem'


def get_article(filename, n):
    if filename == PR_LOB_MD and n in _PR_LOB_LINE_OVERRIDES:
        ini, fim = _PR_LOB_LINE_OVERRIDES[n]
        raw_lines = load_lines(filename)
        from extrair_regulamentos import RE_NOISE, RE_TITLE_CAPS
        art_lines = [ln for ln in raw_lines[ini - 1:fim]
                     if not (RE_NOISE.match(ln) or _RE_PR_LOB_FOOTER.match(ln)
                             or (ln.strip() and RE_TITLE_CAPS.match(ln.strip())))
                     and not re.match(r'^\s*Art\s*\.?\s*\d', ln)]
        if n == 35 and art_lines:
            art_lines[0] = _PR_ART35_CAPUT_PREFIX + ' ' + art_lines[0].strip()
        return art_lines
    arts = articles_of(filename)
    return arts.get(n)


# ── Mapa curado: organKey -> lista de CITATION ───────────────────────────────────
# CITATION = (uf, doc('ri'|'lob'), arts:list[int], match, source_label, heading|None)
# `source_label` é o rótulo completo já pronto (após "cf. CBM..."), pois em 2 casos
# (corregedoria/pr e cat/df) o rótulo não é um espelho mecânico de doc+art.
#
# Nota geral sobre PR (achado nº 1 do briefing, confirmado em grep no markdown-fonte):
#   - Citações "CBMPR, Lei nº 22.206/2024, Art. NN" (bbm/cibm/bbs/boa Art. 35;
#     dp Art. 28; dlog Art. 29) vêm de PR_LOB_MD.
#   - Citação "CBMPR, Atribuições institucionais (portal oficial)" (a antiga
#     ENRICHMENT_ORGAN['corregedoria'] via Portaria 227/2023) vem de PR_RI_MD.
#
# Nota sobre a Portaria nº 227/2023 do PR (achado nº 2 do briefing): o arquivo dessa
# portaria NÃO existe no acervo (só o markdown da LOB e o da coletânea do portal).
# A citação original em bloco-d-classificacao-al-df-pr-pa.md ("CBMPR, Portaria nº
# 227/2023, Art. 3º") foi SUBSTITUÍDA aqui pelo Art. 23 de `Paraná - Regimento
# Interno.md` (seção "Corregedoria-Geral - COGER", confirmado nas linhas ~346-390 do
# markdown) — mesmo assunto (competências da Corregedoria), fonte que de fato existe
# no acervo. Rótulo ajustado de acordo (RI coletânea do portal, não a portaria).

CITATIONS = {
    'dpo': [
        ('pa', 'lob', [16], 'parcial',
         'cf. CBMPA, Lei nº 11.060/2025, Art. 16', 'Comando de Operações (COP)'),
        ('df', 'ri', [454], 'parcial',
         'cf. CBMDF, RI (Portaria nº 24/2020), Art. 454', 'COMOP'),
    ],
    'cot': [
        ('df', 'ri', [54], 'exata',
         'cf. CBMDF, RI (Portaria nº 24/2020), Art. 54', 'DESEG'),
    ],
    'bbm': [
        ('pr', 'lob', [35], 'exata',
         'cf. CBMPR, Lei nº 22.206/2024, Art. 35, I', 'Das Unidades e Subunidades de Bombeiro Militar'),
    ],
    'cibm': [
        ('pr', 'lob', [35], 'exata',
         'cf. CBMPR, Lei nº 22.206/2024, Art. 35, II', 'Das Unidades e Subunidades de Bombeiro Militar'),
    ],
    'bbs': [
        ('pr', 'lob', [35], 'parcial',
         'cf. CBMPR, Lei nº 22.206/2024, Art. 35, III', 'Das Unidades e Subunidades de Bombeiro Militar (GOST)'),
    ],
    'boa': [
        ('pr', 'lob', [35], 'exata',
         'cf. CBMPR, Lei nº 22.206/2024, Art. 35, IV', 'Das Unidades e Subunidades de Bombeiro Militar (UOA)'),
    ],
    'cg': [
        ('pa', 'ri', [6], 'parcial',
         'cf. CBMPA, RI, Art. 6', 'Comando-Geral (assessoramento)'),
        ('df', 'ri', [58], 'parcial',
         'cf. CBMDF, RI (Portaria nº 24/2020), Art. 58', 'Estado-Maior-Geral (EMG)'),
    ],
    'depdec': [
        ('al', 'ri', [13], 'exata',
         'cf. CBMAL, RI, Art. 13', 'Coordenadoria Estadual de Defesa Civil (CEDEC)'),
    ],
    'condeg': [
        ('al', 'ri', [11], 'parcial',
         'cf. CBMAL, RI, Art. 11', 'Conselho de Políticas Estratégicas'),
    ],
    'dp': [
        ('df', 'ri', [127], 'exata',
         'cf. CBMDF, RI (Portaria nº 24/2020), Art. 127', 'Diretoria de Gestão de Pessoal (DIGEP)'),
        ('pr', 'lob', [28], 'exata',
         'cf. CBMPR, Lei nº 22.206/2024, Art. 28', 'Diretoria de Pessoal'),
    ],
    'deei': [
        ('df', 'ri', [227], 'exata',
         'cf. CBMDF, RI (Portaria nº 24/2020), Art. 227', 'Diretoria de Ensino (DIREN)'),
    ],
    'dpof': [
        ('df', 'ri', [187], 'parcial',
         'cf. CBMDF, RI (Portaria nº 24/2020), Art. 187', 'Diretoria de Orçamento e Finanças (DIOFI)'),
        ('pa', 'ri', [170], 'exata',
         'cf. CBMPA, RI, Art. 170', 'Diretoria de Finanças'),
        ('al', 'ri', [52], 'parcial',
         'cf. CBMAL, RI, Art. 52', 'Diretoria de Finanças'),
    ],
    'dsap': [
        ('df', 'ri', [154], 'exata',
         'cf. CBMDF, RI (Portaria nº 24/2020), Art. 154', 'Diretoria de Saúde (DISAU)'),
    ],
    'dlog': [
        ('pr', 'lob', [29], 'parcial',
         'cf. CBMPR, Lei nº 22.206/2024, Art. 29', 'Diretoria de Apoio Logístico e Finanças (DALF)'),
        ('df', 'ri', [218], 'exata',
         'cf. CBMDF, RI (Portaria nº 24/2020), Art. 218', 'Diretoria de Materiais e Serviços (DIMAT)'),
        ('pa', 'ri', [163], 'exata',
         'cf. CBMPA, RI, Art. 163', 'Diretoria de Administração e Logística (DAL)'),
    ],
    'cint': [
        ('df', 'ri', [304], 'exata',
         'cf. CBMDF, RI (Portaria nº 24/2020), Art. 304', 'Centro de Inteligência (CEINT)'),
        ('pa', 'ri', [140], 'exata',
         'cf. CBMPA, RI, Art. 140', 'Centro de Inteligência (CEINT)'),
        ('al', 'ri', [25], 'exata',
         'cf. CBMAL, RI, Art. 25', 'Assessoria de Inteligência e Contra-Inteligência (AICI)'),
    ],
    'ccs': [
        ('df', 'ri', [291], 'exata',
         'cf. CBMDF, RI (Portaria nº 24/2020), Art. 291', 'Centro de Comunicação Social (CECOM)'),
        ('al', 'ri', [26], 'parcial',
         'cf. CBMAL, RI, Art. 26', 'Assessoria de Relações Públicas e Comunicação Social (ARPCS)'),
    ],
    'cinf': [
        ('df', 'ri', [241], 'exata',
         'cf. CBMDF, RI (Portaria nº 24/2020), Art. 241', 'Diretoria de Tecnologia da Informação e Comunicação (DITIC)'),
    ],
    'gab-cg': [
        ('df', 'ri', [6], 'exata',
         'cf. CBMDF, RI (Portaria nº 24/2020), Art. 6', 'Gabinete do Comandante-Geral'),
        ('pa', 'ri', [107], 'exata',
         'cf. CBMPA, RI, Art. 107', 'Gabinete do Comandante-Geral'),
    ],
    'ag': [
        ('df', 'ri', [110], 'exata',
         'cf. CBMDF, RI (Portaria nº 24/2020), Art. 110', 'Ajudância Geral'),
        ('pa', 'ri', [119], 'exata',
         'cf. CBMPA, RI, Art. 119', 'Ajudância Geral'),
    ],
    'corregedoria': [
        ('df', 'ri', [96], 'exata',
         'cf. CBMDF, RI (Portaria nº 24/2020), Art. 96', 'Corregedoria'),
        ('al', 'ri', [29], 'tematica',
         'cf. CBMAL, RI, Art. 29', 'Corregedoria Geral (assistência judiciária ao militar)'),
        # Substitui a Portaria nº 227/2023 (indisponível no acervo) pelo Art. 23 do RI
        # coletânea do portal — ver nota do achado nº 2 acima.
        ('pr', 'ri', [23], 'exata',
         'cf. CBMPR, RI (coletânea do portal), Art. 23', 'Corregedoria-Geral - COGER'),
    ],
    'bifea': [
        ('df', 'ri', [530], 'exata',
         'cf. CBMDF, RI (Portaria nº 24/2020), Art. 530', 'Grupamento de Proteção Ambiental (GPRAM)'),
    ],
    'cat': [
        ('rs', 'ri', [16, 39, 55], 'exata',
         'cf. CBMRS, RI (Portaria nº 001/2025), Art. {n}', 'Batalhão Especial Segurança Contra Incêndio (BESCI)'),
        # ◐ complementar: DF fatia a execução técnica em 2 diretorias; usamos as
        # competências (não a estrutura pura de 263/265-267) como o 2º melhor par.
        ('df', 'ri', [251], 'parcial',
         'cf. CBMDF, RI (Portaria nº 24/2020), Art. 251', 'Diretoria de Vistorias (DIVIS)'),
        ('df', 'ri', [264], 'parcial',
         'cf. CBMDF, RI (Portaria nº 24/2020), Art. 264', 'Diretoria de Estudos e Análise de Projetos (DIEAP)'),
    ],
    'doe': [
        ('df', 'ri', [488, 489], 'exata',
         'cf. CBMDF, RI (Portaria nº 24/2020), Art. {n}', 'Comando Especializado (COESP)'),
    ],
    'assessorias': [
        ('pa', 'ri', [69], 'exata',
         'cf. CBMPA, RI, Art. 69', 'Assessorias Técnicas'),
        ('rs', 'ri', [31, 37, 47], 'parcial',
         'cf. CBMRS, RI (Portaria nº 001/2025), Art. {n}', 'Assessorias do GCG (Controle Interno, Jurídica/Convênios, APERI etc.)'),
    ],
    'crbm': [
        ('rs', 'ri', [14, 38, 54], 'exata',
         'cf. CBMRS, RI (Portaria nº 001/2025), Art. {n}', 'Comandos Regionais de Bombeiro Militar (CRBM)'),
    ],
}

# organKey -> md_file por CITATION (resolve a ambiguidade do PR: 'lob' -> LOB do PR;
# 'ri' do PR -> coletânea do portal; os demais estados têm 1 único arquivo de RI).
def md_for(uf, doc):
    if uf == 'pr':
        return PR_LOB_MD if doc == 'lob' else PR_RI_MD
    return MD_FILE[uf]


_TRAILING_SUBHEADINGS = [
    'Da Organização', 'Das Competências Orgânicas Comuns', 'Das Competências Orgânicas',
    'Das Atribuições dos Dirigentes Do Chefe do Departamento-Geral de Administração',
    'Das Atribuições dos Dirigentes',
    'Da Secretaria Administrativa', 'Do Corregedor Geral',
    'Da Coordenadoria Estadual de Defesa Civil', 'Do Coordenador Estadual de Defesa Civil',
    'Da Assessoria de Relações Públicas e Comunicação Social',
    'Da Assessoria de Inteligência e Contra-Inteligência',
    'Do Diretor de Finanças',
]
_TRAILING_SUBHEADINGS.sort(key=len, reverse=True)


def _strip_trailing_subheading(text):
    """Remove sub-título de seção (título-caso, não pego por RE_TITLE_CAPS) que fica
    GRUDADO ao fim do último dispositivo de um artigo — no markdown-fonte esse
    subtítulo introduz o PRÓXIMO bloco/artigo, não faz parte do atual (mesma classe
    de bug de extrair_regulamentos.py CONFIG['se']['strip_lines'], mas aqui colado
    na mesma linha em vez de em linha própria). Lista construída por leitura manual
    dos documentos afetados (AL, PA RI)."""
    t = text.rstrip()
    for sub in _TRAILING_SUBHEADINGS:
        if t.endswith(' ' + sub):
            return t[: -(len(sub) + 1)].rstrip()
        if t == sub:
            return ''
    return text


_RE_ART_EMBUTIDO = re.compile(r'(?<!^)\bArt\.?\s*\d[\dº°\s]{0,3}\.\s')


def _truncar_no_proximo_artigo(art_lines):
    """O próximo "Art. N" às vezes vem GRUDADO no fim da última linha do artigo
    atual (ex.: DF Art. 227/228: "...ensino da Corporação. Art. 228. À Seção..."
    numa única linha física) — RE_ART só reconhece marcador no INÍCIO da linha,
    então split_articles()/o corte por line_slices não separam os dois artigos.
    Detecta o marcador embutido (não no início da linha) e trunca ali."""
    out = []
    for ln in art_lines:
        m = _RE_ART_EMBUTIDO.search(ln)
        if m and m.start() > 0:
            out.append(ln[:m.start()].rstrip())
            break
        out.append(ln)
    return out


# (uf, doc, n) -> substring onde a extração deve PARAR (achado por leitura manual):
# páginas raspadas de site (não PDF) às vezes não têm nenhum marcador de "próximo
# artigo" entre o fim do dispositivo e o começo do bloco seguinte — só um subtítulo
# solto + rodapé de página + frase de introdução do bloco seguinte, tudo sem
# marcador reconhecível por RE_ITEM, então caput_e_dispositivos() gruda tudo no
# último dispositivo. Ex.: PR/RI Art. 23 (Corregedoria-Geral): depois do Parágrafo
# único, a página segue com "Atribuições Funcionais da Corregedoria-Geral" + rodapé
# de data/URL do site oficial + a intro do bloco de atribuições DA PORTARIA
# 227/2023 (que não faz parte do Art. 23 nem está disponível no acervo — ver nota
# do achado nº 2 no topo do arquivo).
_STOP_MARKERS = {
    ('pr', 'ri', 23): 'Atribuições Funcionais da Corregedoria-Geral',
}


def _truncar_em_marcador(art_lines, marker):
    out = []
    for ln in art_lines:
        idx = ln.find(marker)
        if idx != -1:
            out.append(ln[:idx].rstrip())
            break
        out.append(ln)
    return out


def build_excerpt(uf, doc, n, source_label, match, heading):
    filename = md_for(uf, doc)
    art_lines = get_article(filename, n)
    if art_lines is None:
        print(f'  BLOQUEADO: {uf}/{doc} Art. {n} não encontrado em {filename} — pulando (heading: {heading})')
        return None
    art_lines = _truncar_no_proximo_artigo(art_lines)
    stop_marker = _STOP_MARKERS.get((uf, doc, n))
    if stop_marker:
        art_lines = _truncar_em_marcador(art_lines, stop_marker)
    caput, dispositivos = caput_e_dispositivos(art_lines)
    if dispositivos:
        dispositivos = list(dispositivos)
        dispositivos[-1] = _strip_trailing_subheading(dispositivos[-1])
        dispositivos = [d for d in dispositivos if d]
    else:
        caput = _strip_trailing_subheading(caput)
    if not caput and not dispositivos:
        print(f'  AVISO: {uf}/{doc} Art. {n} encontrado mas vazio em {filename} — pulando')
        return None
    source = source_label.format(n=n) if '{n}' in source_label else source_label
    return {'heading': heading, 'caput': caput, 'dispositivos': dispositivos,
            'source': source, 'match': match}


def build_ri_alternatives():
    result = {}
    pulados = []
    for organ_key, citations in CITATIONS.items():
        by_uf = {}
        for uf, doc, arts, match, source_label, heading in citations:
            excerpts = []
            for n in arts:
                ex = build_excerpt(uf, doc, n, source_label, match, heading)
                if ex is None:
                    pulados.append((organ_key, uf, doc, n))
                    continue
                excerpts.append(ex)
            if not excerpts:
                continue
            entry = by_uf.setdefault(uf, {
                'name': STATE_META[uf]['name'], 'abbr': STATE_META[uf]['abbr'],
                'docLabel': DOC_LABEL[(uf, doc)], 'excerpts': [],
            })
            entry['excerpts'].extend(excerpts)
        if by_uf:
            result[organ_key] = by_uf
    return result, pulados


def emit(alternatives):
    path = OUT / 'ri_alternativas_enrichment.py'
    parts = [
        '# GERADO por scripts/extrair_ri_alternativas.py — NAO editar a mao.',
        '# Fonte: docs/curadoria/bloco-d-classificacao-al-df-pr-pa.md +',
        '#        docs/curadoria/de-para-ri-rs.md (extracao deterministica; mapa CITATIONS',
        '#        no proprio script gerador).',
        'RI_ALTERNATIVES = {',
    ]
    for organ_key in sorted(alternatives):
        parts.append(f'    {organ_key!r}: {{')
        for uf in sorted(alternatives[organ_key]):
            entry = alternatives[organ_key][uf]
            parts.append(f'        {uf!r}: {{')
            parts.append(f'            "name": {entry["name"]!r}, "abbr": {entry["abbr"]!r},')
            parts.append(f'            "docLabel": {entry["docLabel"]!r},')
            parts.append('            "excerpts": [')
            for ex in entry['excerpts']:
                parts.append('                {')
                for campo in ('heading', 'caput', 'dispositivos', 'source', 'match'):
                    parts.append(f'                    {campo!r}: {ex[campo]!r},')
                parts.append('                },')
            parts.append('            ],')
            parts.append('        },')
        parts.append('    },')
    parts.append('}')
    path.write_text('\n'.join(parts) + '\n', encoding='utf-8')
    return path


def main():
    alternatives, pulados = build_ri_alternatives()
    path = emit(alternatives)
    n_organs = len(alternatives)
    n_excerpts = sum(len(ex['excerpts']) for organ in alternatives.values() for ex in organ.values())
    n_states_total = sum(len(organ) for organ in alternatives.values())
    print(f'Gerado: {path}')
    print(f'{n_organs} órgãos com alternatives | {n_states_total} pares órgão×estado | {n_excerpts} excertos')
    if pulados:
        print(f'Citações puladas por falta de artigo no acervo ({len(pulados)}):')
        for organ_key, uf, doc, n in pulados:
            print(f'  - {organ_key} / {uf}/{doc} Art. {n}')


if __name__ == '__main__':
    main()
