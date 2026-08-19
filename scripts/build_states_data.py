"""
build_states_data.py — Portal CBM
Lê os arquivos .md em database/markdown/ e extrai dados estruturados
para gerar database/states_data.json. Idempotente.
"""

import re
import json
import sys
from pathlib import Path

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')

BASE_DIR = Path(__file__).parent.parent
MD_DIR = BASE_DIR / "database" / "markdown"
DATA_DIR = BASE_DIR / "database"
PDF_DIR = BASE_DIR / "LEGISLAÇÃO CBMS"
PDF_FILES = {p.name for p in PDF_DIR.glob("*.pdf")} if PDF_DIR.exists() else set()

# Pseudo-fontes que vivem em database/markdown/ mas NÃO são estado/CBM — não devem
# virar um "estado" em states_data.json. Hoje só o RISG (Exército Brasileiro), usado
# EXCLUSIVAMENTE como alternativa verbatim do Regulamento (regulamento_enrichment.py);
# nunca deve aparecer como fonte primária nem como estado no acervo comparativo.
NON_STATE_MD_STEMS = {"RISG"}

# ────────────────────────────────────────────
# Mapeamento estático de metadados por estado
# ────────────────────────────────────────────
STATE_META = {
    "Acre":              {"id": "ac", "abbr": "AC", "region": "Norte",       "cbm": "CBMAC"},
    "Alagoas":           {"id": "al", "abbr": "AL", "region": "Nordeste",    "cbm": "CBMAL"},
    "Amapá":             {"id": "ap", "abbr": "AP", "region": "Norte",       "cbm": "CBMAP"},
    "Amazonas":          {"id": "am", "abbr": "AM", "region": "Norte",       "cbm": "CBMAM"},
    "Bahia":             {"id": "ba", "abbr": "BA", "region": "Nordeste",    "cbm": "CBMBA"},
    "Ceará":             {"id": "ce", "abbr": "CE", "region": "Nordeste",    "cbm": "CBMCE"},
    "Distrito Federal":  {"id": "df", "abbr": "DF", "region": "Centro-Oeste","cbm": "CBMDF"},
    "Espírito Santo":    {"id": "es", "abbr": "ES", "region": "Sudeste",     "cbm": "CBMES"},
    "Goiás":             {"id": "go", "abbr": "GO", "region": "Centro-Oeste","cbm": "CBMGO"},
    "Maranhão":          {"id": "ma", "abbr": "MA", "region": "Nordeste",    "cbm": "CBMMA"},
    "Mato Grosso":       {"id": "mt", "abbr": "MT", "region": "Centro-Oeste","cbm": "CBMMT"},
    "Mato Grosso do Sul":{"id": "ms", "abbr": "MS", "region": "Centro-Oeste","cbm": "CBMMS"},
    "Minas Gerais":      {"id": "mg", "abbr": "MG", "region": "Sudeste",     "cbm": "CBMMG"},
    "Paraná":            {"id": "pr", "abbr": "PR", "region": "Sul",         "cbm": "CBMPR"},
    "Paraíba":           {"id": "pb", "abbr": "PB", "region": "Nordeste",    "cbm": "CBMPB"},
    "Pará":              {"id": "pa", "abbr": "PA", "region": "Norte",       "cbm": "CBMPA"},
    "Pernambuco":        {"id": "pe", "abbr": "PE", "region": "Nordeste",    "cbm": "CBMPE"},
    "Piauí":             {"id": "pi", "abbr": "PI", "region": "Nordeste",    "cbm": "CBMPI"},
    "Rio Grande do Norte":{"id":"rn", "abbr": "RN", "region": "Nordeste",    "cbm": "CBMRN"},
    "Rio Grande do Sul": {"id": "rs", "abbr": "RS", "region": "Sul",         "cbm": "CBMRS"},
    "Rio de Janeiro":    {"id": "rj", "abbr": "RJ", "region": "Sudeste",     "cbm": "CBMERJ"},
    "Rondônia":          {"id": "ro", "abbr": "RO", "region": "Norte",       "cbm": "CBMRO"},
    "Roraíma":           {"id": "rr", "abbr": "RR", "region": "Norte",       "cbm": "CBMRR"},
    "Roraima":           {"id": "rr", "abbr": "RR", "region": "Norte",       "cbm": "CBMRR"},
    "Santa Catarina":    {"id": "sc", "abbr": "SC", "region": "Sul",         "cbm": "CBMSC"},
    "Sergipe":           {"id": "se", "abbr": "SE", "region": "Nordeste",    "cbm": "CBMSE"},
    "São Paulo":         {"id": "sp", "abbr": "SP", "region": "Sudeste",     "cbm": "CBPMESP"},
    "Tocantins":         {"id": "to", "abbr": "TO", "region": "Norte",       "cbm": "CBMTO"},
}

CBM_FULL_NAMES = {
    "ac": "Corpo de Bombeiros Militar do Estado do Acre",
    "al": "Corpo de Bombeiros Militar de Alagoas",
    "ap": "Corpo de Bombeiros Militar do Amapá",
    "am": "Corpo de Bombeiros Militar do Amazonas",
    "ba": "Corpo de Bombeiros Militar da Bahia",
    "ce": "Corpo de Bombeiros Militar do Ceará",
    "df": "Corpo de Bombeiros Militar do Distrito Federal",
    "es": "Corpo de Bombeiros Militar do Espírito Santo",
    "go": "Corpo de Bombeiros Militar do Estado de Goiás",
    "ma": "Corpo de Bombeiros Militar do Maranhão",
    "mt": "Corpo de Bombeiros Militar do Mato Grosso",
    "ms": "Corpo de Bombeiros Militar do Mato Grosso do Sul",
    "mg": "Corpo de Bombeiros Militar de Minas Gerais",
    "pr": "Corpo de Bombeiros Militar do Paraná",
    "pb": "Corpo de Bombeiros Militar da Paraíba",
    "pa": "Corpo de Bombeiros Militar do Pará",
    "pe": "Corpo de Bombeiros Militar de Pernambuco",
    "pi": "Corpo de Bombeiros Militar do Piauí",
    "rn": "Corpo de Bombeiros Militar do Rio Grande do Norte",
    "rs": "Corpo de Bombeiros Militar do Rio Grande do Sul",
    "rj": "Corpo de Bombeiros Militar do Estado do Rio de Janeiro",
    "ro": "Corpo de Bombeiros Militar do Estado de Rondônia",
    "rr": "Corpo de Bombeiros Militar do Estado de Roraima",
    "sc": "Corpo de Bombeiros Militar de Santa Catarina",
    "se": "Corpo de Bombeiros Militar de Sergipe",
    "sp": "Corpo de Bombeiros Militar do Estado de São Paulo",
    "to": "Corpo de Bombeiros Militar do Tocantins",
}


# ────────────────────────────────────────────
# Helpers de extração por Regex
# ────────────────────────────────────────────

ROMAN_RE = r'(?:M{0,3})(?:CM|CD|D?C{0,3})(?:XC|XL|L?X{0,3})(?:IX|IV|V?I{0,3})'

def extract_law_numbers(text: str) -> list[dict]:
    """Extrai números de leis, decretos e portarias do texto."""
    patterns = [
        (r'LEI\s+(?:COMPLEMENTAR\s+)?N[º°\.]\s*([\d\.]+)[,\s]+DE\s+(\d+\s+\w+\s+\w+(?:\s+\w+)?)', 'Lei'),
        (r'DECRETO\s+N[º°\.]\s*([\d\.]+)[,\s]+DE\s+(\d+\s+\w+\s+\w+(?:\s+\w+)?)', 'Decreto'),
        (r'PORTARIA\s+N[º°\.]\s*([\d\.]+)[,\s]+DE\s+(\d+\s+\w+\s+\w+(?:\s+\w+)?)', 'Portaria'),
        (r'RESOLUÇÃO\s+N[º°\.]\s*([\d\.]+)[,\s]+DE\s+(\d+\s+\w+\s+\w+(?:\s+\w+)?)', 'Resolução'),
        (r'PROJETO\s+DE\s+LEI\s+DE\s+(\w+)\s+DE\s+(\w+\s+\w+\s+\w+)', 'Projeto de Lei'),
    ]
    found = []
    for pattern, kind in patterns:
        for m in re.finditer(pattern, text[:3000], re.IGNORECASE):
            found.append({"tipo": kind, "numero": m.group(1), "data": m.group(2)})
    return found[:3]


def extract_year(text: str) -> int | None:
    """Extrai o ano de vigência do documento."""
    m = re.search(r'\b(19[89]\d|20[012]\d)\b', text[:2000])
    return int(m.group(1)) if m else None


def extract_articles_about_structure(text: str) -> list[str]:
    """Extrai artigos que descrevem a estrutura organizacional."""
    # Padrão: Art. X ... será estruturado em / compreende / compõe
    art_pattern = re.compile(
        r'Art\.\s*\d+[º°]?\s*[–\-]?\s*(.{20,600}?)'
        r'(?=Art\.\s*\d+[º°]|§\s*\d+|CAPÍTULO|Seção|$)',
        re.DOTALL
    )
    structure_keywords = ['estrutur', 'compreend', 'compõe', 'organiz', 'constitui', 'composta']
    results = []
    for m in art_pattern.finditer(text):
        art_text = m.group(0)
        if any(kw in art_text.lower() for kw in structure_keywords):
            results.append(art_text.strip()[:600])
    return results[:8]


def extract_organ_names(text: str) -> list[dict]:
    """
    Extrai nomes de órgãos listados em artigos estruturais.
    Retorna lista de { name, abbreviation, category }.
    """
    organs = []
    seen = set()

    # Padrão: "I - Nome do Órgão (SIGLA)" ou "I – Nome – SIGLA"
    roman_list = re.compile(
        r'(?:^|\n)\s*(?:' + ROMAN_RE + r'|[a-z])\s*[-–]\s*'
        r'(.{5,120}?)(?=\n|;|$)',
        re.MULTILINE
    )

    for m in roman_list.finditer(text):
        item = m.group(1).strip()
        item = re.sub(r'\s+', ' ', item)
        if not item or len(item) < 4:
            continue

        # Extrai sigla entre parênteses
        abbr_match = re.search(r'\(([A-Z]{2,10}(?:\/[A-Z]+)?)\)', item)
        abbr = abbr_match.group(1) if abbr_match else None

        # Limpa o nome
        name = re.sub(r'\s*\([^)]+\)\s*', ' ', item).strip()
        name = re.sub(r'\s*[-–]\s*[A-Z]{2,10}$', '', name).strip()
        name = name.rstrip(';,.')

        if name and name not in seen and len(name) > 3:
            seen.add(name)
            organs.append({
                "id": slugify(name),
                "name": name,
                "abbreviation": abbr,
                "children": []
            })

    return organs[:60]


def slugify(text: str) -> str:
    text = text.lower()
    text = re.sub(r'[àáâãä]', 'a', text)
    text = re.sub(r'[èéêë]', 'e', text)
    text = re.sub(r'[ìíîï]', 'i', text)
    text = re.sub(r'[òóôõö]', 'o', text)
    text = re.sub(r'[ùúûü]', 'u', text)
    text = re.sub(r'[ç]', 'c', text)
    text = re.sub(r'[^a-z0-9]+', '-', text)
    return text.strip('-')


def classify_organ(name: str, _text_context: str = "") -> str:
    """Classifica o tipo de órgão com base no nome."""
    nl = name.lower()
    if any(k in nl for k in ['comando-geral', 'comando geral', 'comandante-geral']):
        return 'direcao_geral'
    if any(k in nl for k in ['estado-maior', 'estado maior']):
        return 'direcao_geral'
    if any(k in nl for k in ['subcomando', 'subcomandante']):
        return 'direcao_geral'
    if any(k in nl for k in ['diretoria']):
        return 'direcao_setorial'
    if any(k in nl for k in ['assessoria', 'assessor']):
        return 'assessoramento'
    if any(k in nl for k in ['corregedoria', 'corregedor']):
        return 'correcao'
    if any(k in nl for k in ['batalhão', 'companhia', 'pelotão', 'grupamento']):
        return 'execucao'
    if any(k in nl for k in ['gabinete', 'ajudância']):
        return 'apoio'
    if any(k in nl for k in ['conselho', 'comissão']):
        return 'colegiado'
    return 'outro'


def extract_chapters(text: str) -> list[dict]:
    """Extrai capítulos e seções como estrutura hierárquica."""
    chapter_re = re.compile(
        r'CAPÍTULO\s+(' + ROMAN_RE + r')\s*\n(.+?)(?=\nCAPÍTULO|\Z)',
        re.DOTALL | re.IGNORECASE
    )
    chapters = []
    for m in chapter_re.finditer(text[:50000]):
        title = m.group(2).strip().split('\n')[0].strip()
        chapters.append({
            "number": m.group(1),
            "title": title,
            "text_preview": m.group(0)[:400]
        })
    return chapters[:20]


# ────────────────────────────────────────────
# Estruturas organizacionais curadas manualmente
# (complementam extração automática)
# ────────────────────────────────────────────

import sys as _sys, os as _os
_sys.path.insert(0, _os.path.dirname(__file__))
from curated_organs import CURATED_ORGANS as _CO1
from curated_organs_p2 import CURATED_ORGANS_P2 as _CO2
from curated_organs_p3 import CURATED_ORGANS_P3 as _CO3

CURATED_ORGANS = {**_CO1, **_CO2, **_CO3}



# ────────────────────────────────────────────
# Enriquecimento da árvore com subdivisões do Regimento
# (puxa os "desdobramentos" do detalhamento para dentro do organograma)
# ────────────────────────────────────────────

import copy as _copy
ORGANS_DETAIL_DIR = DATA_DIR / "organs_detail"


def _norm2(s: str) -> str:
    s = (s or "").lower()
    for a, b in [("á","a"),("à","a"),("â","a"),("ã","a"),("é","e"),("ê","e"),
                 ("í","i"),("ó","o"),("ô","o"),("õ","o"),("ú","u"),("ç","c")]:
        s = s.replace(a, b)
    return re.sub(r'[^a-z0-9]+', ' ', s).strip()


def _canon(s: str) -> str:
    """Normalização canônica tolerante a variações de cargo↔órgão, para casar
    nós da árvore curada com chaves do detalhamento (ex.: 'Comandante Geral'
    ↔ 'Comando Geral', 'Diretor de RH' ↔ 'Diretoria de RH')."""
    s = _norm2(s)
    s = re.sub(r'^(chefe d[aeo] |chefe )', '', s)
    s = re.sub(r'\bsubcomandante\b', 'subcomando', s)
    s = re.sub(r'\bcomandante\b', 'comando', s)
    s = re.sub(r'\bdiretor(?:a)?(?: d[aeo])?\b', 'diretoria', s)
    s = re.sub(r'\bcoordenador(?:a)?(?: d[aeo])?\b', 'coordenadoria', s)
    s = re.sub(r'\s+', ' ', s).strip()
    return s


def count_nodes(nodes: list) -> int:
    total = 0
    for n in nodes:
        total += 1
        total += count_nodes(n.get("children", []))
    return total


def enrich_tree_from_detail(state_id: str, organs: list) -> list:
    """Adiciona, como nós-filhos, as subdivisões (desdobramentos) descritas no
    detalhamento de cada órgão — surfando a estrutura do Regimento na árvore."""
    path = ORGANS_DETAIL_DIR / f"{state_id}.json"
    if not path.exists():
        return organs
    try:
        detail = json.loads(path.read_text(encoding='utf-8')).get("organs", {})
    except Exception:
        return detail_fail(organs)
    if not detail:
        return organs

    by_abbr, by_name, by_canon = {}, {}, {}
    for oid, o in detail.items():
        ab = (o.get("abbreviation") or "").strip().lower()
        if ab:
            by_abbr.setdefault(ab, oid)
        by_name.setdefault(_norm2(o.get("name", "")), oid)
        by_canon.setdefault(_canon(o.get("name", "")), oid)

    def match(node):
        """Retorna (oid, organ_detail) ou (None, None). Tolera variações comuns
        de nomenclatura entre a árvore curada e o detalhamento."""
        nid = node.get("id")
        if nid and nid in detail:
            return nid, detail[nid]
        ab = (node.get("abbreviation") or "").strip().lower()
        if ab and ab in by_abbr:
            oid = by_abbr[ab]; return oid, detail[oid]
        nm = _norm2(node.get("name", ""))
        if nm in by_name:
            oid = by_name[nm]; return oid, detail[oid]
        cn = _canon(node.get("name", ""))
        if cn and cn in by_canon:
            oid = by_canon[cn]; return oid, detail[oid]
        # sobreposição de tokens (tolera "/" vs "e", ordem das palavras, núcleos
        # compostos): escolhe o candidato com mais tokens em comum, exigindo
        # cobertura forte do menor conjunto para evitar falsos positivos.
        STOP = {"e", "de", "do", "da", "dos", "das", "o", "a", "ao", "geral"}
        # qualificadores que distinguem órgãos homônimos — se um lado tem e o
        # outro não (ou difere), NÃO casar (ex.: Estado-Maior Operacional ≠ Geral)
        QUALIF = {"operacional", "setorial", "administrativo", "administrativa",
                  "regional", "metropolitano", "metropolitana", "especializado",
                  "especializada", "interior", "capital", "adjunto", "operacoes",
                  "atuacao", "terrestre", "aerea", "aereo"}
        ntok = {t for t in cn.split() if t not in STOP}
        if len(ntok) >= 2:
            best_oid, best_score = None, 0.0
            for ck, oid in by_canon.items():
                ctok = {t for t in ck.split() if t not in STOP}
                if not ctok:
                    continue
                shared = len(ntok & ctok)
                if shared < 2:
                    continue
                if (ntok ^ ctok) & QUALIF:   # qualificador conflitante
                    continue
                cover = shared / min(len(ntok), len(ctok))
                if cover < 0.6:
                    continue
                score = shared + cover  # prioriza mais tokens casados
                if score > best_score:
                    best_oid, best_score = oid, score
            if best_oid:
                return best_oid, detail[best_oid]
        return None, None

    organs = _copy.deepcopy(organs)

    def walk(node):
        children = node.setdefault("children", [])
        for c in list(children):
            if not c.get("_reg"):
                walk(c)
        oid, d = match(node)
        if not d:
            return
        node["detailId"] = oid   # carimbo p/ o frontend resolver direto
        existing = {_norm2(c.get("name", "")) for c in children}
        for sub in d.get("desdobramentos", []):
            raw = (sub or "").strip()
            if not raw:
                continue
            base = re.sub(r'\s*\([^)]*\)\s*$', '', raw).strip()
            base = re.sub(r'\s*[–-]\s*[A-Z0-9/]{2,12}$', '', base).strip()
            key = _norm2(base)
            if not key or key in existing:
                continue
            m = re.search(r'\(([^)]+)\)\s*$', raw) or re.search(r'[–-]\s*([A-Z0-9/]{2,12})$', raw)
            leaf = {"id": slugify(base)[:48] or "no", "name": base, "children": [], "_reg": True}
            if m:
                leaf["abbreviation"] = m.group(1).strip()
            children.append(leaf)
            existing.add(key)

    for n in organs:
        walk(n)
    return organs


def detail_fail(organs):
    return organs


# ────────────────────────────────────────────
# Processamento principal
# ────────────────────────────────────────────

# Correções descobertas pela curadoria do Regulamento (Bloco B1-M, achado 2026-07-08):
# o NOME do arquivo diz uma coisa, o CONTEÚDO real (de-para lido pelo Fable) diz
# outra. parse_doc_type() só olha o nome do arquivo, então não tem como acertar
# esses dois sozinho. RN e GO já tinham sido corrigidos direto no parse_doc_type
# (Bloco B0, porque o nome do arquivo deles já indicava a categoria certa); MT e SE
# só foram identificados depois, na leitura de conteúdo. Ver CLAUDE.md
# "Classificação de tipo de documento".
CONTENT_TYPE_OVERRIDES = {
    # SE: PDF renomeado para "Regulamento Interno" (2026-07-13), mas o conteúdo é o
    # RISD — Regulamento Interno dos Serviços Diários (regimento de serviço).
    # parse_doc_type daria "Regulamento Geral" pela palavra "regulamento" no nome.
    "Sergipe - Regulamento Interno.md": "Regimento de Serviços",
    # NOTA SC (ingestão 2026-07-13): o antigo override de SC ("Organização Básica"
    # → Regimento Interno) foi REMOVIDO. O arquivo era o Decreto nº 1.328/2021
    # (regulamenta a LOB), obtido escaneado; foi SUBSTITUÍDO pela LOB real —
    # Lei Complementar nº 724/2018 ("Santa Catarina - Organização Básica.md") e sua
    # alteração, a LC nº 885/2025 ("Santa Catarina - Organização Básica alterações.md").
    # Ambas são LOB e parse_doc_type já retorna "Lei de Organização Básica" pelos nomes.
    # MA: a "Portaria 46/2020" é a Diretriz Operacional do serviço diário (Gestor
    # Operacional de Dia, Supervisor do CIOPS, Superior de Dia) — regimento de
    # serviço; parse_doc_type cairia no default "Lei de Organização Básica"
    # (ingestão 2026-07-13).
    "Maranhão - Portaria 46.md": "Regimento de Serviços",
    # PA: "Regulamento de serviço" é o Decreto nº 1.052/2020 sobre os serviços
    # administrativos, preventivos e operacionais diários — regimento de serviço;
    # parse_doc_type daria "Regulamento Geral" pela palavra "regulamento"
    # (ingestão 2026-07-13). PA já tem um "Regimento Interno" organizacional à parte.
    "Pará - Regulamento de serviço.md": "Regimento de Serviços",
    # NOTA MT (2026-07-13): o antigo override "Mato Grosso - Regimento Interno.md"
    # foi removido — o PDF foi renomeado para "Mato Grosso - Regulamento Geral.md",
    # e parse_doc_type já retorna "Regulamento Geral" para esse nome. MT segue em
    # CONTENT_VERIFIED_STATES, então permanece verificado.
    # Alagoas (ingestão 2026-07-20): as Diretrizes Operacionais de Bombeiros (DOB)
    # e as Normas Operacionais NÃO são leis de organização básica — regulam o
    # SERVIÇO operacional (terminologia, estrutura operacional, atividade diária,
    # postos de bombeiros). Matéria de Regulamento Geral. Conteúdo conferido pelo
    # cabeçalho/ementa de cada arquivo. Classificação validada pelo Wândrio.
    "Alagoas - Diretriz Operacional 01.md": "Regulamento Geral",
    "Alagoas - Diretriz Operacional 03.md": "Regulamento Geral",
    "Alagoas - Diretriz Operacional 04.md": "Regulamento Geral",
    "Alagoas - Diretriz Operacional 05.md": "Regulamento Geral",
    "Alagoas - Diretriz Operacional 06.md": "Regulamento Geral",
    "Alagoas - Diretriz Operacional 07.md": "Regulamento Geral",
    "Alagoas - Diretriz Operacional 08.md": "Regulamento Geral",
    "Alagoas - Norma Operacional 01.md": "Regulamento Geral",
    "Alagoas - Norma Operacional 02.md": "Regulamento Geral",
    "Alagoas - Norma Operacional 03.md": "Regulamento Geral",
    "Alagoas - Norma Operacional 04.md": "Regulamento Geral",
    "Alagoas - Norma Operacional 05.md": "Regulamento Geral",
    "Alagoas - Norma Operacional 06.md": "Regulamento Geral",
    "Alagoas - Norma Operacional 07.md": "Regulamento Geral",
    "Alagoas - Norma Operacional 08.md": "Regulamento Geral",
    "Alagoas - Norma Operacional 09.md": "Regulamento Geral",
    "Alagoas - Norma Operacional 11.md": "Regulamento Geral",
}

# Rótulo de EXIBIÇÃO por documento, quando difere do `type` (classificação
# funcional usada na tabela de cobertura e não deve mudar). Sem isso, o rótulo
# cai para o `type` e vários documentos DISTINTOS aparecem com o mesmo nome —
# em Alagoas eram 17 linhas "Regulamento Geral" idênticas, impossíveis de
# distinguir na lista. Cada título abaixo foi conferido no cabeçalho da 1ª
# página do markdown extraído; os PDFs fonte NÃO são renomeados nem movidos.
# Formato curto (o nome pelo qual o documento circula), porque a lista precisa
# caber na tela do celular — o número da lei já aparece em separado (lawText).
DOCUMENT_TITLE_OVERRIDES = {
    # CBMBA batiza os próprios instrumentos: o classificado como "Regimento
    # Interno" se autodenomina "NORMA ADMINISTRATIVA" no cabeçalho de todas as
    # páginas; o "Regulamento de Serviço", "NORMA OPERACIONAL".
    "Bahia - Regimento Interno.md": "Norma Administrativa",
    "Bahia - Regulamento de Serviço.md": "Norma Operacional",
    # CBMAL: 17 documentos operacionais distintos, todos classificados como
    # "Regulamento Geral". Cabeçalhos: "DIRETRIZ OPERACIONAL DE BOMBEIROS (DOB)
    # Nº xx" e "NORMA OPERACIONAL DE BOMBEIRO N.º xx". As DOB 03 e NOB 09 vêm
    # como transcrição em Boletim Geral (sem cabeçalho próprio na 1ª página),
    # mas são citadas nominalmente pelas NOB 01-03, que "dispõem sobre" itens da
    # DOB 03.
    "Alagoas - Diretriz Operacional 01.md": "Diretriz Operacional 01",
    "Alagoas - Diretriz Operacional 03.md": "Diretriz Operacional 03",
    "Alagoas - Diretriz Operacional 04.md": "Diretriz Operacional 04",
    "Alagoas - Diretriz Operacional 05.md": "Diretriz Operacional 05",
    "Alagoas - Diretriz Operacional 06.md": "Diretriz Operacional 06",
    "Alagoas - Diretriz Operacional 07.md": "Diretriz Operacional 07",
    "Alagoas - Diretriz Operacional 08.md": "Diretriz Operacional 08",
    "Alagoas - Norma Operacional 01.md": "Norma Operacional 01",
    "Alagoas - Norma Operacional 02.md": "Norma Operacional 02",
    "Alagoas - Norma Operacional 03.md": "Norma Operacional 03",
    "Alagoas - Norma Operacional 04.md": "Norma Operacional 04",
    "Alagoas - Norma Operacional 05.md": "Norma Operacional 05",
    "Alagoas - Norma Operacional 06.md": "Norma Operacional 06",
    "Alagoas - Norma Operacional 07.md": "Norma Operacional 07",
    "Alagoas - Norma Operacional 08.md": "Norma Operacional 08",
    "Alagoas - Norma Operacional 09.md": "Norma Operacional 09",
    "Alagoas - Norma Operacional 11.md": "Norma Operacional 11",
    # Demais estados cujo documento de serviço tem nome próprio, diferente do
    # tipo funcional pelo qual foi classificado.
    "Goiás - Regimento dos Serviços Interno e Operacional.md": "Regimento dos Serviços Interno e Operacional",
    # Portaria que APROVA a diretriz; sem lei registrada, por isso o número entra
    # no título (é como o documento é identificado no CBMMA).
    "Maranhão - Portaria 46.md": "Diretriz Operacional do Serviço (Portaria 46/2020)",
    "Pará - Regulamento de serviço.md": "Regulamento de Serviço",
    "Sergipe - Regulamento Interno.md": "Regulamento Interno dos Serviços Diários (RISD)",
    # "INSTRUÇÃO NORMATIVA OPERACIONAL Nº 01/2024 (INOp 01) — Serviços Diários
    # dos Oficiais". Arquivo com a grafia antiga do estado ("Roraíma"), ver
    # STATE_NAME_ALIASES.
    "Roraíma - Regulamento de Serviço.md": "Instrução Normativa Operacional 01/2024",
    # Portaria nº 003/2019/COB: "Atualiza a Diretriz Geral do Comando Operacional".
    "Tocantins - Regulamento de Serviço.md": "Diretriz Geral do Comando Operacional",
    # Decreto 21.425/2016 — classificado como Regulamento Geral, mas é o RSCIP,
    # matéria de segurança contra incêndio, não de serviço.
    "Rondônia - Regulamento de Segurança Contra Incêndio e Pânico (Decreto 21.425-2016).md":
        "Regulamento de Segurança Contra Incêndio e Pânico",
    # PROJETO de lei ("* MINUTA DE DOCUMENTO" na 1ª página): sem o rótulo, se
    # exibia igual à LOB vigente, como se já valesse.
    "Rondônia - Minuta de Lei de Organização Básica.md": "Minuta de Lei de Organização Básica",
    # LC 885/2025 ALTERA a LC 724/2018 (a LOB do CBMSC). As duas se exibiam como
    # "Lei de Organização Básica", indistinguíveis.
    "Santa Catarina - Organização Básica alterações.md": "Lei de Organização Básica (alterações)",
}

# Ordem de EXIBIÇÃO dos documentos dentro de cada estado: LOB, depois Regimento
# Interno, depois os documentos de serviço, e por último o que não entra nas 3
# colunas de cobertura (Quadros de efetivo). Ordenar aqui, no gerador, e não em
# cada tela: a ordem vira propriedade do dado, então o Acervo Legal e a ficha do
# estado herdam a mesma sequência sem duplicar lógica. Espelha o bucketOf() de
# src/lib/acervoCoverage.js — se um tipo entrar lá, entra aqui também.
DOC_TYPE_DISPLAY_ORDER = (
    "Lei de Organização Básica",
    "Regimento Interno",
    "Regulamento Geral",
    "Regimento de Serviços",
    "Normas Gerais de Ação",
)


def doc_sort_key(doc: dict) -> tuple:
    """Posição do documento na ordem de exibição do estado.

    Tipo desconhecido cai para o fim (len da tupla). Desempate pelo nome do
    arquivo, para a ordem ficar estável entre execuções — sem isso, dois
    documentos do mesmo tipo poderiam trocar de lugar a cada regeneração e
    sujar o diff do JSON.
    """
    try:
        rank = DOC_TYPE_DISPLAY_ORDER.index(doc.get("type"))
    except ValueError:
        rank = len(DOC_TYPE_DISPLAY_ORDER)
    return (rank, doc.get("md_file", ""))

# Grafias alternativas do MESMO estado no nome dos arquivos → nome canônico único.
# Sem isso, "Roraíma" (grafia herdada do acervo antigo) e "Roraima" (grafia correta
# dos arquivos novos) seriam agrupados como DOIS estados distintos. Canônico = a
# grafia correta. Ingestão 2026-07-20.
STATE_NAME_ALIASES = {
    "Roraíma": "Roraima",
}

# Estados cujo TIPO de documento foi conferido por leitura de conteúdo de verdade —
# a curadoria do Regulamento (Bloco B1-M, scripts/regulamento_enrichment.py
# REGULAMENTO_DOCS) leu o texto integral desses estados pra montar a minuta do
# Regulamento, e por isso também confirmou (ou corrigiu, ver acima) o tipo de cada
# documento.
# NOTA MT/RN (2026-07-30): os documentos têm título formal "Regulamento Geral" (MT:
# Portaria nº 009/BM-8/2013; RN: Decreto nº 31.139/2021), mas o CONTEÚDO funciona como o
# Regimento Interno de cada estado — confirmado pelo Wândrio e corroborado por
# scripts/minuta_enrichment.py, que já citava 9+ órgãos como "cf. CBMMT, RI, Art. N"
# (ex.: Art. 152 = Ajudância-Geral, 12 itens; Art. 129 = cinf, 9 itens) extraídos VERBATIM
# deste mesmo documento antes mesmo do acervo reconhecer o tipo certo. Igual a SE/MA/PA/GO
# acima: o nome que o próprio estado dá ao instrumento não corresponde à função —
# parse_doc_type já acerta pelo nome do arquivo (renomeado), sem precisar de override. Os
# dois continuam também PRIMARY_SOURCE de temas do Regulamento Geral da minuta (o mesmo
# documento cobre estrutura organizacional E competências temáticas). Resolve a pendência
# "falta o RI de MT" (Art. 152/129) — ver ✅ Concluído em .claude/PENDENCIAS.md.
CONTENT_VERIFIED_STATES = {"al", "df", "go", "mt", "pa", "pr", "rn", "rs", "se"}

# Auditoria de 2026-07-09 (achado 2026-07-09): leitura do início (ementa/título) de
# cada documento dos 18 estados fora do B1-M, um a um, pra confirmar ou corrigir a
# classificação por nome de arquivo. Arquivos abaixo tiveram o conteúdo lido e
# CONFIRMADO batendo com o tipo (ou corrigido, caso de SC acima). É por ARQUIVO,
# não por estado inteiro — os 2 arquivos de São Paulo e 1 do Piauí ficaram de fora
# de propósito, ver notas abaixo.
CONTENT_VERIFIED_FILES = {
    "Acre - Organização Básica (Lei 2.009-2008 att Lei 4.428-2024).md",
    "Acre - Organização Básica.md",
    "Amapá - Organização Básica.md",
    "Amazonas - Organização Básica.md",
    "Amazonas - Quadro Demonstrativo de Cargos e Funções.md",
    "Bahia - Organização Básica.md",
    "Ceará - Organização Básica (Lei 13.438-2004).md",
    "Ceará - Organização Básica.md",
    "Espírito Santo - Lei de Organização Básica.md",
    "Espírito Santo - Normas Gerais de Ação.md",
    "Maranhão - Organização Básica.md",
    "Maranhão - Quadro de Organização e Distribuição.md",
    # Diretriz Operacional (Portaria 46/2020) — conteúdo lido e confirmado como
    # regimento de serviço na ingestão de 2026-07-13 (MA não está em
    # CONTENT_VERIFIED_STATES, por isso entra por arquivo).
    "Maranhão - Portaria 46.md",
    "Mato Grosso do Sul - Organização Básica.md",
    "Minas Gerais - Organização Básica.md",
    # Ementa diz "organização estrutural e funcional" (não "organização básica"
    # literalmente), mas cumpre a mesma função de LOB — revoga as leis antigas de
    # organização básica do CBMPB.
    "Paraíba - Organização Básica.md",
    "Pernambuco - Organização Básica (Lei 15.187-2013).md",
    "Pernambuco - Organização Básica.md",
    # A Lei nº 5.949/2009 original (no OUTRO arquivo do Piauí) veio de PDF
    # escaneado sem OCR legível — só cabeçalho de jornal, nenhum texto de lei.
    # Este arquivo é a Lei nº 7.772/2022, que ALTERA a original com redação
    # substitutiva completa dos artigos — legível e confirmado.
    "Piauí - Organização Básica.md",
    "Rio de Janeiro - Organização Básica.md",
    # O próprio texto se identifica como "MINUTA DE DOCUMENTO"/projeto de lei em
    # tramitação (marca d'água, processo SEI) — condição já conhecida e refletida
    # no nome do arquivo, não é uma anomalia.
    "Rondônia - Minuta de Lei de Organização Básica.md",
    # Decreto nº 21.425/2016 (alt. Decreto nº 24.357/2019), regulamenta a Lei estadual
    # nº 3.924/2016 sobre segurança contra incêndio e evacuação de edificações — o
    # próprio Art. 1º se autodenomina "Regulamento de Segurança Contra Incêndio e
    # Pânico do Estado", confirmando o tipo. Ingerido em 2026-08-13 e já usado como
    # fundamento na reescrita do capítulo "Da Segurança Contra Incêndio e Pânico" da
    # minuta do Regulamento Geral (ver scripts/regulamento_reescrita.py).
    "Rondônia - Regulamento de Segurança Contra Incêndio e Pânico (Decreto 21.425-2016).md",
    # Ementa usa "Lei Orgânica" em vez de "organização básica", mas mesma função.
    "Roraíma - Organização Básica.md",
    "Santa Catarina - Organização Básica.md",
    # LC nº 885/2025 que altera a LOB (LC 724/2018) do CBMSC — texto oficial da ALESC,
    # transcrito para PDF pesquisável na ingestão de 2026-07-13.
    "Santa Catarina - Organização Básica alterações.md",
    "Tocantins - Organização Básica.md",
}

# NÃO entram em CONTENT_VERIFIED_FILES (achados da auditoria de 2026-07-09, cada um
# com motivo diferente — ver CLAUDE.md "Classificação de tipo de documento"):
# - "Piauí - Organização Básica (Lei 5.949-2009 alt. Lei 7.772-2022).md": PDF
#   escaneado sem OCR legível (só cabeçalho de jornal) — impossível confirmar ou
#   negar o tipo pelo conteúdo.
# - "São Paulo - Organização Básica (Lei 616-1974).md" e
#   "São Paulo - Organização Básica.md": os 2 documentos organizam a POLÍCIA
#   MILITAR de SP inteira (o Corpo de Bombeiros aparece só como seção/comando
#   subordinado, Art. 38-43 da Lei 616/1974), não uma LOB exclusiva do CBM. Pode
#   refletir a realidade de SP (CBM integrado à PM, sem lei própria separada) ou
#   pode faltar buscar o documento certo — o Wândrio ainda não confirmou qual dos
#   dois casos é (2026-07-09).


def parse_doc_type(filename: str) -> str:
    if filename in CONTENT_TYPE_OVERRIDES:
        return CONTENT_TYPE_OVERRIDES[filename]
    name = filename.lower()
    if 'regimento dos serviços' in name: return 'Regimento de Serviços'
    if 'regimento interno' in name: return 'Regimento Interno'
    # Regimento de serviço/escala (ex.: GO "Regimento dos Serviços Interno e
    # Operacional") — NÃO é um Regimento Interno organizacional; rótulo distinto
    # para não confundir no acervo nem virar has_regimento.
    if 'regimento' in name and 'serviç' in name: return 'Regimento de Serviços'
    # Regulamento Geral por Decreto (ex.: RN Decreto 31.139/2021) — não é uma Lei
    # de Organização Básica; rótulo próprio.
    if 'regulamento' in name: return 'Regulamento Geral'
    if 'normas gerais de ação' in name or 'nga' in name: return 'Normas Gerais de Ação'
    if 'quadro demonstrativo' in name: return 'Quadro Demonstrativo de Cargos'
    if 'quadro de organização' in name: return 'Quadro de Organização e Distribuição'
    return 'Lei de Organização Básica'


def process_state(state_name: str, md_files: list[Path]) -> dict:
    meta = STATE_META.get(state_name, {})
    state_id = meta.get("id", slugify(state_name))

    documents = []
    all_text = ""

    for md_file in sorted(md_files):
        text = md_file.read_text(encoding='utf-8', errors='replace')
        all_text += "\n\n" + text

        doc_type = parse_doc_type(md_file.name)
        laws = extract_law_numbers(text)
        year = extract_year(text)

        doc_entry = {
            "type": doc_type,
            "title": DOCUMENT_TITLE_OVERRIDES.get(md_file.name, doc_type),
            "typeVerified": state_id in CONTENT_VERIFIED_STATES or md_file.name in CONTENT_VERIFIED_FILES,
            "md_file": md_file.name,
            "char_count": len(text),
            "year": year,
            "laws": laws,
            "has_pdf": md_file.name.replace(".md", ".pdf") in PDF_FILES
        }
        documents.append(doc_entry)

    # LOB -> Regimento Interno -> documentos de serviço -> demais (ver
    # DOC_TYPE_DISPLAY_ORDER). Feito uma vez aqui: todo consumidor do JSON
    # herda a mesma ordem.
    documents.sort(key=doc_sort_key)

    # Monta base legal
    law_strings = []
    for doc in documents:
        for law in doc.get("laws", []):
            law_strings.append(f"{law['tipo']} nº {law['numero']} ({law['data']})")
    legal_basis = "; ".join(law_strings) if law_strings else "Consultar documento fonte"

    # Extrai capítulos
    chapters = extract_chapters(all_text)

    # Extrai órgãos (fallback automático)
    auto_organs = extract_organ_names(all_text)

    # Usa órgãos curados se disponíveis
    organs = CURATED_ORGANS.get(state_id, auto_organs[:30])
    # Enriquece a árvore com as subdivisões descritas no detalhamento (Regimento)
    organs = enrich_tree_from_detail(state_id, organs)

    # Estatísticas de documentos
    has_regimento = any(d["type"] == "Regimento Interno" for d in documents)
    has_regulamento = any(d["type"] in ("Regulamento Geral", "Regimento de Serviços") for d in documents)
    has_nga = any(d["type"] == "Normas Gerais de Ação" for d in documents)
    total_chars = sum(d["char_count"] for d in documents)

    return {
        "id": state_id,
        "name": state_name,
        "abbreviation": meta.get("abbr", ""),
        "region": meta.get("region", ""),
        "cbm_name": CBM_FULL_NAMES.get(state_id, f"Corpo de Bombeiros Militar — {state_name}"),
        "cbm_abbreviation": meta.get("cbm", "CBM"),
        "documents": documents,
        "legal_basis": legal_basis,
        "chapters_summary": chapters[:5],
        "organs": organs,
        "stats": {
            "total_documents": len(documents),
            "has_regimento": has_regimento,
            "has_regulamento": has_regulamento,
            "has_nga": has_nga,
            "total_chars": total_chars,
            "organs_mapped": count_nodes(organs),
            "curated": state_id in CURATED_ORGANS
        }
    }


def group_files_by_state(md_files: list[Path]) -> dict[str, list[Path]]:
    groups: dict[str, list[Path]] = {}
    for f in md_files:
        state = f.stem.split(' - ')[0].strip()
        state = STATE_NAME_ALIASES.get(state, state)
        if state not in groups:
            groups[state] = []
        groups[state].append(f)
    return groups


def main():
    print("=" * 60)
    print("Portal CBM — Construtor de states_data.json")
    print("=" * 60)

    md_files = sorted(
        f for f in MD_DIR.glob("*.md") if f.stem not in NON_STATE_MD_STEMS
    )
    if not md_files:
        print(f"Nenhum arquivo .md encontrado em {MD_DIR}")
        print("Execute primeiro: python scripts/convert_to_markdown.py")
        return

    groups = group_files_by_state(md_files)
    print(f"Estados identificados: {len(groups)}")

    states = []
    for state_name, files in sorted(groups.items()):
        print(f"  Processando: {state_name} ({len(files)} doc(s))")
        state_data = process_state(state_name, files)
        states.append(state_data)

    # Ordena puramente por ordem alfabética do nome do estado
    states.sort(key=lambda s: s["name"])

    # Estatísticas globais
    total_docs = sum(s["stats"]["total_documents"] for s in states)
    curated_count = sum(1 for s in states if s["stats"]["curated"])
    regions = {}
    for s in states:
        r = s["region"]
        regions[r] = regions.get(r, 0) + 1

    output = {
        "metadata": {
            "version": "1.0",
            "generated_at": "2026-06-01",
            "total_states": len(states),
            "total_documents": total_docs,
            "curated_states": curated_count,
            "regions": regions
        },
        "states": states
    }

    out_path = DATA_DIR / "states_data.json"
    out_path.write_text(json.dumps(output, ensure_ascii=False, indent=2), encoding='utf-8')

    print(f"\n{'='*60}")
    print(f"Gerado: {out_path}")
    print(f"Estados: {len(states)} | Documentos: {total_docs} | Curados: {curated_count}")
    print("Concluído.")


if __name__ == "__main__":
    main()
