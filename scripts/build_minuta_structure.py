"""
build_minuta_structure.py — Portal CBM

Gera database/minuta_structure.json: minuta ARTICULADA e HIERÁRQUICA do Regimento
Interno do CBMRO — do Comando Geral (CG) à menor fração (Companhia/GBM), cobrindo
os 26 órgãos da LOB. Um capítulo por órgão; uma seção por função (cargo).

Fontes:
  - database/organs_detail/ro.json        (estrutura + competências RO verbatim)
  - scripts/minuta_enrichment.py          (competências curadas de outros CBMs, rotuladas)

Saída: database/minuta_structure.json
Rodar: python scripts/build_minuta_structure.py
"""

import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from minuta_enrichment import enrich_for, enrich_organ_for, GUARNICAO_CHAPTER  # noqa: E402

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

BASE_DIR = Path(__file__).parent.parent
RO_JSON  = BASE_DIR / "database" / "organs_detail" / "ro.json"
OUT_JSON = BASE_DIR / "database" / "minuta_structure.json"

TITLE = "DO REGIMENTO INTERNO DA ESTRUTURA OPERACIONAL DO CBMRO"

# Ordem dos capítulos = ordem de subordinação (topo → menor fração).
# (organ_key, CHAPTER_TITLE, artigo_definido)
ORGAN_ORDER = [
    ("cg",           "DO COMANDO GERAL (CG)",                                          "O"),
    ("depdec",       "DA DIRETORIA ESTADUAL DE PROTEÇÃO E DEFESA CIVIL (DEPDEC)",       "A"),
    ("condeg",       "DO CONSELHO DELIBERATIVO DE ESTRATÉGIA E GESTÃO (CONDEG)",        "O"),
    ("dp",           "DA DIRETORIA DE PESSOAL (DP)",                                    "A"),
    ("deei",         "DA DIRETORIA DE EDUCAÇÃO, ENSINO E INSTRUÇÃO (DEEI)",             "A"),
    ("dpof",         "DA DIRETORIA DE PLANEJAMENTO, ORÇAMENTO E FINANÇAS (DPOF)",        "A"),
    ("dsap",         "DA DIRETORIA DE SAÚDE E ASSISTÊNCIA AO PESSOAL (DSAP)",            "A"),
    ("dlog",         "DA DIRETORIA DE LOGÍSTICA (DLOG)",                                "A"),
    ("dpo",          "DA DIRETORIA DE PLANEJAMENTO OPERACIONAL (DPO)",                  "A"),
    ("doe",          "DA DIRETORIA OPERACIONAL ESPECIALIZADA (DOE)",                    "A"),
    ("cot",          "DO COMANDO DE OPERAÇÕES TÉCNICAS (COT)",                          "O"),
    ("cint",         "DA COORDENADORIA DE INTELIGÊNCIA (CINT)",                         "A"),
    ("ccs",          "DA COORDENADORIA DE COMUNICAÇÃO SOCIAL (CCS)",                    "A"),
    ("cinf",         "DA COORDENADORIA DE INFORMÁTICA (CINF)",                          "A"),
    ("crbm",         "DOS COMANDOS REGIONAIS DE BOMBEIRO MILITAR (CRBM)",               "Os"),
    ("assessorias",  "DAS ASSESSORIAS",                                                 "As"),
    ("gab-cg",       "DO GABINETE DO COMANDANTE-GERAL",                                 "O"),
    ("ag",           "DA AJUDÂNCIA-GERAL (AG)",                                         "A"),
    ("bbm",          "DO BATALHÃO DE BOMBEIROS MILITAR (BBM)",                          "O"),
    ("cibm",         "DA COMPANHIA INDEPENDENTE DE BOMBEIROS MILITAR (CIBM)",           "A"),
    ("cat",          "DA COORDENADORIA DE ATIVIDADES TÉCNICAS (CAT)",                   "A"),
    ("bbs",          "DO BATALHÃO DE BUSCA E SALVAMENTO (BBS)",                         "O"),
    ("bifea",        "DO BATALHÃO DE INCÊNDIO FLORESTAL E EMERGÊNCIAS AMBIENTAIS (BIFEA)", "O"),
    ("boa",          "DO BATALHÃO DE OPERAÇÕES AÉREAS (BOA)",                           "O"),
    ("gbm",          "DO GRUPO DE BOMBEIROS MILITAR (GBM)",                             "O"),
    ("corregedoria", "DA CORREGEDORIA-GERAL",                                           "A"),
]

# Área de atuação dos Órgãos de Execução (LOB Art. 9), para agrupar o Art. 3.
AREA_BY_ORGAN = {
    "bbm": "ordinaria", "cibm": "ordinaria", "cat": "ordinaria",
    "bbs": "terrestre", "bifea": "terrestre",
    "boa": "aerea",
    "gbm": "conveniada",
}
AREA_LABELS = [
    ("ordinaria",  "Atuação Operacional Ordinária"),
    ("terrestre",  "Atuação Operacional Especializada Terrestre"),
    ("aerea",      "Atuação Operacional Especializada Aérea"),
    ("conveniada", "Atuação Operacional Conveniada Municipal"),
]

DISP_FINAIS = (
    "Os casos omissos neste Regimento Interno serão resolvidos pelo Comandante-Geral do CBMRO.\n"
    "Este Regimento Interno entra em vigor na data de sua publicação, revogadas as disposições em contrário."
)


def normalize(text: str) -> str:
    t = re.sub(r"^\s*[\dIVXivx]+[.)]\s*", "", (text or "").strip())
    return t.strip().lower()


def _dedup_keep_order(items):
    """items: list[{text, source}] -> remove duplicatas por texto normalizado, RO primeiro."""
    seen, out = set(), []
    for it in items:
        k = normalize(it["text"])
        if k and k not in seen:
            seen.add(k)
            out.append(it)
    return out


def ro_items(texts, source="ro"):
    return [{"text": t.strip(), "source": source} for t in texts if (t or "").strip()]


def proposed_text(items):
    return "\n".join(it["text"] for it in items)


def build_finalidade_section(organ):
    """Seção 'Da Finalidade' (prose) — usa a 1ª atribuição/finalidade do órgão."""
    fin = ""
    for a in (organ.get("atribuicoes") or []):
        if a.strip():
            fin = a.strip()
            break
    return {
        "id": "finalidade", "kind": "prose", "sectionTitle": "Da Finalidade",
        "editId": None,  # preenchido pelo chamador
        "proposedText": fin,
    }


def build_competencia_section(organ_key, organ, abbr, skip_text=""):
    skip = normalize(skip_text) if skip_text else None
    raw = ro_items(organ.get("atribuicoes") or [])
    if skip:
        raw = [it for it in raw if normalize(it["text"]) != skip]
    # RO primeiro; depois competências/missões verbatim de outras legislações.
    items = _dedup_keep_order(raw + enrich_organ_for(organ_key))
    return {
        "id": "competencia", "kind": "incisos", "sectionTitle": "Da Competência",
        "editId": None, "caput": f"Compete à {abbr}:" if abbr else "Compete:",
        "items": items, "proposedText": proposed_text(items),
    }


def build_organizacao_section(organ, abbr):
    items = ro_items(organ.get("desdobramentos") or [])
    return {
        "id": "organizacao", "kind": "incisos", "sectionTitle": "Da Organização Interna",
        "editId": None, "caput": f"{abbr} tem a seguinte estrutura interna:" if abbr else "Tem a seguinte estrutura interna:",
        "items": items, "proposedText": proposed_text(items),
    }


def build_cargo_sections(organ_key, organ):
    sections = []
    for c in (organ.get("cargos") or []):
        name = (c.get("cargo") or "").strip()
        if not name:
            continue
        ro = ro_items(c.get("atribuicoes") or [])
        enr = enrich_for(organ_key, name)
        items = _dedup_keep_order(ro + enr)
        if not items:
            continue
        sid = "cargo:" + re.sub(r"[^a-z0-9]+", "-", name.lower()).strip("-")
        sections.append({
            "id": sid, "kind": "incisos",
            "sectionTitle": f"Das Atribuições do {name}",
            "editId": None, "caput": f"Ao {name} compete:",
            "items": items, "proposedText": proposed_text(items),
        })
    return sections


def build_organ_chapter(organ_key, chapter_title, organ):
    abbr = organ.get("abbreviation") or organ_key.upper()
    fin_section = build_finalidade_section(organ)
    sections = [fin_section]
    # Competência exclui a 1ª atribuição já usada como Finalidade (evita repetição).
    comp = build_competencia_section(organ_key, organ, abbr, skip_text=fin_section["proposedText"])
    if comp["items"]:
        sections.append(comp)
    org = build_organizacao_section(organ, abbr)
    if org["items"]:
        sections.append(org)
    sections.extend(build_cargo_sections(organ_key, organ))

    chapter_id = f"organ:{organ_key}"
    for s in sections:
        s["editId"] = f"{chapter_id}/{s['id']}"

    return {
        "id": chapter_id, "kind": "organ", "chapterTitle": chapter_title,
        "organKey": organ_key, "label": organ.get("name", ""), "abbr": abbr,
        "sections": sections,
    }


def _join_orgaos(keys, organs, art_by_key):
    """['dpo','doe','cot'] -> 'a Diretoria ... (DPO), a Diretoria ... (DOE) e o Comando ... (COT)'."""
    parts = []
    for k in keys:
        o = organs.get(k)
        if not o:
            continue
        nome = o.get("name", k.upper())
        abbr = o.get("abbreviation") or k.upper()
        parts.append(f"{art_by_key[k].lower()} {nome} ({abbr})")
    if len(parts) <= 1:
        return "".join(parts)
    return ", ".join(parts[:-1]) + " e " + parts[-1]


CATEGORY_LABELS = [
    ("Direção Geral",     "de Direção Geral"),
    ("Direção Colegiada",  "de Direção Colegiada"),
    ("Direção Setorial",   "de Direção Setorial"),
    ("Direção Regional",   "de Direção Regional"),
]
APOIO_LABELS = [
    ("Apoio ao Comando-Geral",    "ao Comando-Geral"),
    ("Apoio ao Subcomando-Geral", "ao Subcomando-Geral"),
]


def build_estrutura_chapter(organs):
    art_by_key = {k: art for (k, _t, art) in ORGAN_ORDER}
    cat_of = {k: (organs.get(k) or {}).get("category", "") for (k, _t, _a) in ORGAN_ORDER}

    def items_for(labels):
        out = []
        for cat, label in labels:
            keys = [k for (k, _t, _a) in ORGAN_ORDER if cat_of[k] == cat]
            if keys:
                out.append({"text": f"{label}: {_join_orgaos(keys, organs, art_by_key)}", "source": "ro"})
        return out

    direcao_items = items_for(CATEGORY_LABELS)
    apoio_items = items_for(APOIO_LABELS)
    assessoramento_items = items_for([("Assessoramento", "de Assessoramento")])
    correicao_items = items_for([("Correição", "de Correição")])

    execucao_items = []
    for area_key, area_label in AREA_LABELS:
        keys = [k for (k, _t, _a) in ORGAN_ORDER if AREA_BY_ORGAN.get(k) == area_key]
        if not keys:
            continue
        execucao_items.append({"text": f"{area_label}: {_join_orgaos(keys, organs, art_by_key)}", "source": "ro"})

    def make_article(article_id, caput, items):
        return {
            "id": article_id, "kind": "incisos", "editId": f"estrutura/{article_id}",
            "caput": caput, "items": items, "proposedText": proposed_text(items),
        }

    articles = [make_article("direcao", "São Órgãos de Direção:", direcao_items)]
    if assessoramento_items:
        articles.append(make_article("assessoramento", "É Órgão de Assessoramento:", assessoramento_items))
    if apoio_items:
        articles.append(make_article("apoio", "São Órgãos de Apoio:", apoio_items))
    articles.append(make_article(
        "execucao", "Os Órgãos de Execução classificam-se, quanto à área de atuação, em:", execucao_items
    ))
    if correicao_items:
        articles.append(make_article("correicao", "É Órgão de Correição:", correicao_items))

    return {
        "id": "estrutura", "kind": "articles", "chapterTitle": "DA ESTRUTURA ORGANIZACIONAL",
        "editId": "estrutura",
        "articles": articles,
    }


def build_preliminares_chapter():
    txt = (
        "Este Regimento Interno disciplina a organização, as competências e o funcionamento "
        "da estrutura operacional do Corpo de Bombeiros Militar do Estado de Rondônia (CBMRO), "
        "do escalão de direção operacional às frações de execução.\n"
        "A estrutura operacional subordina-se ao Comandante-Geral por intermédio do "
        "Subcomandante-Geral, nos termos da Lei de Organização Básica do CBMRO."
    )
    return {
        "id": "preliminares", "kind": "prose", "chapterTitle": "DAS DISPOSIÇÕES PRELIMINARES",
        "editId": "preliminares", "proposedText": txt,
    }


def build_guarnicao_chapter():
    """Capítulo da menor fração operacional — subsídio integral do CBMSE (RISD)."""
    g = GUARNICAO_CHAPTER
    chapter_id = "organ:guarnicao"
    sections = [{
        "id": "finalidade", "kind": "prose", "sectionTitle": "Da Finalidade",
        "editId": None, "proposedText": g["finalidade"],
    }]
    for name, caput, items in g["cargos"]:
        items = _dedup_keep_order(items)
        sid = "cargo:" + re.sub(r"[^a-z0-9]+", "-", name.lower()).strip("-")
        sections.append({
            "id": sid, "kind": "incisos", "sectionTitle": f"Das Atribuições do {name}",
            "editId": None, "caput": caput,
            "items": items, "proposedText": proposed_text(items),
        })
    for s in sections:
        s["editId"] = f"{chapter_id}/{s['id']}"
    return {
        "id": chapter_id, "kind": "organ", "chapterTitle": g["chapterTitle"],
        "organKey": "guarnicao", "label": g["label"], "abbr": g.get("abbr", ""),
        "sections": sections,
    }


def build_finais_chapter():
    return {
        "id": "finais", "kind": "prose", "chapterTitle": "DAS DISPOSIÇÕES FINAIS",
        "editId": "finais", "proposedText": DISP_FINAIS,
    }


# Colocações padrão para nós que não casam pela subordinação textual do ro.json:
#   gbm  -> subordinadoA = "Pelotão…" (fora do conjunto). É unidade de Execução
#           Conveniada Municipal, ramo próprio sob o CRBM (ao lado de BBM e CIBM).
# A Guarnição é tratada à parte (não por override): é a folha da cadeia de frações
# da execução ordinária do BBM — ver BBM_FRACTION_CHAIN.
COMMAND_PARENT_OVERRIDE = {"gbm": "crbm"}

# Cadeia de frações da execução ordinária, do maior ao menor, DENTRO do BBM.
# Companhia e Pelotão não têm capítulo próprio na minuta: entram como nós
# estruturais não-clicáveis (sem chapterId). A Guarnição de Serviço Operacional
# (capítulo organ:guarnicao) compõe o Pelotão e fecha a cadeia como folha.
BBM_FRACTION_CHAIN = [
    {"sigla": "Cia BM",  "label": "Companhia de Bombeiros Militar"},
    {"sigla": "Pel BM",  "label": "Pelotão de Bombeiros Militar"},
]


# subordinadoA de alguns órgãos referencia um CARGO interno de `cg` (Comandante-Geral,
# Subcomandante-Geral, Chefe do Estado-Maior Geral), não a sigla de um órgão do conjunto.
# Mapa de fallback: texto normalizado do cargo -> organ_key real que o "contém".
ROLE_TO_ORGAN = {
    "comandante-geral": "cg",
    "subcomandante-geral": "cg",
    "chefe do estado-maior geral": "cg",
}


def build_command_chart(organs, chapters):
    """Árvore dos órgãos (capítulos kind='organ') pela subordinação do ro.json.

    Pai = órgão do conjunto cuja SIGLA aparece em subordinadoA; se nenhuma sigla
    casar, tenta ROLE_TO_ORGAN (subordinadoA referencia um cargo interno de outro
    órgão); senão, raiz. A Guarnição (menor fração) pendura na cadeia
    Cia BM → Pel BM dentro do BBM.
    Retorna `cg` como raiz real (tem chapterId, é clicável) quando há exatamente
    uma raiz; cai para um wrapper sintético só se restarem múltiplas raízes
    desconectadas (não esperado com os 26 órgãos atuais — sinal de dado inesperado).
    """
    nodes = {}
    for c in chapters:
        if c.get("kind") != "organ":
            continue
        k = c["organKey"]
        nodes[k] = {
            "organKey": k,
            "sigla": c.get("abbr") or "",
            "label": c.get("label") or "",
            "chapterId": c["id"],
            "children": [],
        }

    siglas = {k: n["sigla"] for k, n in nodes.items() if n["sigla"]}

    def find_parent(k):
        if k in COMMAND_PARENT_OVERRIDE:
            return COMMAND_PARENT_OVERRIDE[k]
        sub = (organs.get(k) or {}).get("subordinadoA", "") or ""
        matches = [
            other_k for other_k, sig in siglas.items()
            if other_k != k and re.search(rf"\b{re.escape(sig)}\b", sub)
        ]
        # subordinadoA deve referenciar no máximo uma sigla do conjunto; mais de uma
        # significaria roteamento ambíguo (texto do ro.json mudou) — falha alto.
        if len(matches) > 1:
            raise ValueError(
                f"subordinadoA de '{k}' casa múltiplas siglas {matches}: {sub!r}"
            )
        if matches:
            return matches[0]
        # Sem sigla: subordinadoA pode referenciar um CARGO interno de outro órgão
        # (ex.: "Chefe do Estado-Maior Geral", cargo de `cg`) em vez de um órgão próprio.
        sub_norm = normalize(sub)
        for role, target in ROLE_TO_ORGAN.items():
            if sub_norm.startswith(role) and target in nodes and target != k:
                return target
        return None  # raiz

    # A Guarnição não entra no roteamento por sigla: é a folha da cadeia de frações
    # do BBM, montada à parte com nós estruturais intermediários (Cia BM, Pel BM).
    guarnicao = nodes.pop("guarnicao", None)

    roots = []
    for k, n in nodes.items():
        p = find_parent(k)
        if p and p in nodes:
            nodes[p]["children"].append(n)
        else:
            roots.append(n)

    if guarnicao is not None and "bbm" in nodes:
        leaf = nodes["bbm"]
        for frac in BBM_FRACTION_CHAIN:
            node = {
                "organKey": None, "sigla": frac["sigla"], "label": frac["label"],
                "structural": True, "chapterId": None, "children": [],
            }
            leaf["children"].append(node)
            leaf = node
        leaf["children"].append(guarnicao)

    if len(roots) == 1:
        return roots[0]
    return {"label": "Subcomandante-Geral", "synthetic": True, "children": roots}


def _min_organ_chapters(organs):
    """Capítulos mínimos (só os campos que build_command_chart lê) p/ derivar a ordem."""
    chapters = []
    for k, _title, _a in ORGAN_ORDER:
        o = organs.get(k, {})
        chapters.append({
            "kind": "organ", "organKey": k,
            "abbr": o.get("abbreviation") or k.upper(),
            "label": o.get("name", ""), "id": f"organ:{k}",
        })
    chapters.append({
        "kind": "organ", "organKey": "guarnicao",
        "abbr": GUARNICAO_CHAPTER.get("abbr", ""), "label": GUARNICAO_CHAPTER["label"],
        "id": "organ:guarnicao",
    })
    return chapters


def command_order(organs):
    """Ordem hierárquica (DFS) e profundidade dos órgãos pela cadeia de comando.

    Retorna list[(organKey, depth)] — depth conta só níveis de ÓRGÃO (nós
    estruturais Cia/Pel não incrementam). É a mesma árvore do organograma,
    então a lista de órgãos da minuta espelha o organograma montado.
    """
    chart = build_command_chart(organs, _min_organ_chapters(organs))
    out = []

    def walk(node, depth):
        k = node.get("organKey")
        if k:
            out.append((k, depth))
        nd = depth + 1 if k else depth
        for c in node.get("children", []):
            walk(c, nd)

    walk(chart, 0)
    return out


def main():
    organs = json.loads(RO_JSON.read_text(encoding="utf-8")).get("organs", {})

    chapters = [build_preliminares_chapter(), build_estrutura_chapter(organs)]
    for organ_key, chapter_title, _art in ORGAN_ORDER:
        o = organs.get(organ_key)
        if not o:
            print(f"  ! órgão ausente no ro.json: {organ_key} — pulando")
            continue
        chapters.append(build_organ_chapter(organ_key, chapter_title, o))
    chapters.append(build_guarnicao_chapter())
    chapters.append(build_finais_chapter())

    output = {
        "generated_by": "scripts/build_minuta_structure.py",
        "title": TITLE,
        "chapters": chapters,
        "commandChart": build_command_chart(organs, chapters),
    }
    OUT_JSON.write_text(json.dumps(output, ensure_ascii=False, indent=2), encoding="utf-8")

    n_org = sum(1 for c in chapters if c["kind"] == "organ")
    n_sec = sum(len(c.get("sections", [])) for c in chapters if c["kind"] == "organ")
    print(f"Gerado: {OUT_JSON}")
    print(f"  {len(chapters)} capítulos · {n_org} órgãos · {n_sec} seções de função")


if __name__ == "__main__":
    main()
