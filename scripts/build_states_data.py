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
    "Mato Grosso - Regimento Interno.md": "Regulamento Geral",
    "Sergipe - Regimento Interno.md": "Regimento de Serviços",
}

# Estados cujo TIPO de documento foi conferido por leitura de conteúdo de verdade —
# a curadoria do Regulamento (Bloco B1-M, scripts/regulamento_enrichment.py
# REGULAMENTO_DOCS) leu o texto integral desses 9 estados pra montar a minuta do
# Regulamento, e por isso também confirmou (ou corrigiu, ver acima) o tipo de cada
# documento. Os demais 18 estados seguem classificados só pelo nome do arquivo,
# nunca conferidos por conteúdo — ver campo "typeVerified" abaixo.
CONTENT_VERIFIED_STATES = {"al", "df", "go", "mt", "pa", "pr", "rn", "rs", "se"}


def parse_doc_type(filename: str) -> str:
    if filename in CONTENT_TYPE_OVERRIDES:
        return CONTENT_TYPE_OVERRIDES[filename]
    name = filename.lower()
    if 'regimento dos serviços' in name: return 'Regimento de Serviços'
    if 'regimento interno' in name: return 'Regimento Interno'
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
            "typeVerified": state_id in CONTENT_VERIFIED_STATES,
            "md_file": md_file.name,
            "char_count": len(text),
            "year": year,
            "laws": laws,
            "has_pdf": md_file.name.replace(".md", ".pdf") in PDF_FILES
        }
        documents.append(doc_entry)

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
        if state not in groups:
            groups[state] = []
        groups[state].append(f)
    return groups


def main():
    print("=" * 60)
    print("Portal CBM — Construtor de states_data.json")
    print("=" * 60)

    md_files = sorted(MD_DIR.glob("*.md"))
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
