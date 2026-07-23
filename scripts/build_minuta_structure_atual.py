"""Gera database/atual/minuta_structure.json — MINUTA do Regimento Interno do CBMRO
para o cenário LOB ATUAL (vigente, Lei nº 2.204/2009 consolidada).

Isolado do gerador da LOB futura (build_minuta_structure.py): reaproveita APENAS as
funções de montagem de seção (que definem o formato consumido por buildArticles no
frontend), mas NÃO importa o enriquecimento da futura (RI_ALTERNATIVES, guarnição,
command chart, capítulos de estrutura) — assim os cenários nunca se misturam.

Entrada:  database/atual/organs_detail/ro.json  (estrutura vigente, curada à mão)
Saída:    database/atual/minuta_structure.json

Fase 2A: cobre o Comando-Geral (prova de ponta a ponta). Demais órgãos entram na 2B,
acrescentando entradas em ATUAL_ORGAN_ORDER e no ro.json do atual.
"""
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
# Reaproveitamos APENAS helpers NEUTROS de build_minuta_structure (ro_items,
# _dedup_keep_order, proposed_text, normalize, build_finalidade_section,
# build_organizacao_section). NÃO usamos build_competencia_section nem
# build_cargo_sections: essas chamam enrich_organ_for/enrich_for (enriquecimento
# de OUTROS estados da LOB futura) e contaminariam o cenário atual. As seções de
# Competência e de Cargos abaixo são reescritas SEM enriquecimento.
import build_minuta_structure as B  # noqa: E402

BASE_DIR = Path(__file__).parent.parent
RO_JSON = BASE_DIR / "database" / "atual" / "organs_detail" / "ro.json"
OUT_JSON = BASE_DIR / "database" / "atual" / "minuta_structure.json"

TITLE = "DO REGIMENTO INTERNO DO CORPO DE BOMBEIROS MILITAR DO ESTADO DE RONDÔNIA (CBMRO) — LOB ATUAL"

# --- Enriquecimento de conferência: reaproveita o Bloco D verbatim da futura ---
# (as referências de outros estados independem do cenário do RO). Só o campo
# 'alternatives'; NUNCA as competências do RO. de-para a validar pelo Wândrio.
DEPARA_BLOCO_D = {
    "cg":"cg","condeg":"condeg","assessorias":"assessorias","corregedoria":"corregedoria",
    "dp":"dp","deei":"deei","cat":"cat","dlog":"dlog",
    "ajudancia":"ag","gabinete":"gab-cg","cepdec":"depdec","dint":"cint","cpof":"dpof",
    "dcs":"ccs","dinf":"cinf","cob1":"crbm","cob2":"crbm","coa":"boa","gbs":"bbs",
}
def _bloco_d_futura():
    fut = json.loads((BASE_DIR / "database" / "minuta_structure.json").read_text(encoding="utf-8"))
    return {c.get("organKey"): (c.get("alternatives") or {})
            for c in fut["chapters"] if c.get("kind") == "organ"}

# Ordem dos capítulos do cenário atual (topo → menor fração), conforme o organograma
# oficial do CBMRO. Fase 2A: Comando-Geral. Fase 2B — lote 1: demais Órgãos de Direção.
# (organ_key, CHAPTER_TITLE, artigo_definido)
ATUAL_ORGAN_ORDER = [
    ("cg",           "DO COMANDO-GERAL (CG)",                                          "O"),
    ("cepdec",       "DA COORDENADORIA ESTADUAL DE PROTEÇÃO E DEFESA CIVIL (CEPDEC)",   "A"),
    ("condeg",       "DO CONSELHO DELIBERATIVO DE ESTRATÉGIA E GESTÃO (CONDEG)",        "O"),
    ("gabinete",     "DO GABINETE DO COMANDANTE-GERAL",                                 "O"),
    ("assessorias",  "DAS ASSESSORIAS",                                                 "AS"),
    ("dint",         "DA DIRETORIA DE INTELIGÊNCIA (DINT)",                             "A"),
    ("cpof",         "DA COORDENADORIA DE PLANEJAMENTO, ORÇAMENTO E FINANÇAS (CPOF)",   "A"),
    ("comissoes",    "DAS COMISSÕES",                                                   "AS"),
    ("corregedoria", "DA CORREGEDORIA-GERAL",                                           "A"),
    ("ajudancia",    "DA AJUDÂNCIA-GERAL",                                              "A"),
    ("emg",          "DO ESTADO-MAIOR-GERAL (EMG)",                                     "O"),
    ("dp",           "DA COORDENADORIA DE PESSOAL (CP)",                               "A"),
    ("deei",         "DA COORDENADORIA DE EDUCAÇÃO, ENSINO E INSTRUÇÃO (CEEI)",         "A"),
    ("cat",          "DA COORDENADORIA DE ATIVIDADES TÉCNICAS (CAT)",                  "A"),
    ("dlog",         "DA DIRETORIA DE LOGÍSTICA (DLOG)",                               "A"),
    ("dcs",          "DA DIRETORIA DE COMUNICAÇÃO SOCIAL (DCS)",                       "A"),
    ("dinf",         "DA DIRETORIA DE INFORMÁTICA (DINF)",                             "A"),
    ("cob1",         "DO COMANDO OPERACIONAL DE BOMBEIROS I (COB I)",                  "O"),
    ("cob2",         "DO COMANDO OPERACIONAL DE BOMBEIROS II (COB II)",               "O"),
    ("coa",          "DO COMANDO DE OPERAÇÕES AÉREAS (COA)",                           "O"),
    ("gbs",          "DO GRUPAMENTO DE BUSCA E SALVAMENTO (GBS)",                      "O"),
]


def _competencia_atual(organ, abbr, skip_text=""):
    """Seção 'Da Competência' SEM enriquecimento — só as competências verbatim
    do próprio CBMRO (Lei 2.204/2009). Espelha B.build_competencia_section, mas
    remove a chamada a enrich_organ_for()."""
    skip = B.normalize(skip_text) if skip_text else None
    raw = B.ro_items(organ.get("atribuicoes") or [])
    if skip:
        raw = [it for it in raw if B.normalize(it["text"]) != skip]
    items = B._dedup_keep_order(raw)  # sem enrich_organ_for()
    return {
        "id": "competencia", "kind": "incisos", "sectionTitle": "Da Competência",
        "editId": None, "caput": f"Compete à {abbr}:" if abbr else "Compete:",
        "items": items, "proposedText": B.proposed_text(items),
    }


def _cargos_atual(organ):
    """Seções de cargo SEM enriquecimento. Espelha B.build_cargo_sections, mas
    remove a chamada a enrich_for()."""
    sections = []
    for c in (organ.get("cargos") or []):
        name = (c.get("cargo") or "").strip()
        if not name:
            continue
        items = B._dedup_keep_order(B.ro_items(c.get("atribuicoes") or []))  # sem enrich_for()
        if not items:
            continue
        sid = "cargo:" + re.sub(r"[^a-z0-9]+", "-", name.lower()).strip("-")
        sections.append({
            "id": sid, "kind": "incisos",
            "sectionTitle": f"Das Atribuições do {name}",
            "editId": None, "caput": f"Ao {name} compete:",
            "items": items, "proposedText": B.proposed_text(items),
        })
    return sections


def build_organ_chapter_atual(organ_key, chapter_title, organ, bloco_d=None):
    """Monta o capítulo do órgão usando SÓ dados do próprio CBMRO — sem
    enriquecimento de competências, mas com alternatives do Bloco D da futura se houver."""
    abbr = organ.get("abbreviation") or organ_key.upper()
    fin_section = B.build_finalidade_section(organ)
    sections = [fin_section]
    comp = _competencia_atual(organ, abbr, skip_text=fin_section["proposedText"])
    if comp["items"]:
        sections.append(comp)
    org = B.build_organizacao_section(organ, abbr)
    if org["items"]:
        sections.append(org)
    sections.extend(_cargos_atual(organ))

    # Marcador de cenário 'atual:' no id — isola os endereços de dispositivo (comentários
    # e textos finais no Firebase) dos do cenário futuro, que compartilham chaves como
    # 'organ:cg'. A futura permanece sem marcador (preserva os comentários existentes).
    chapter_id = f"atual:organ:{organ_key}"
    for s in sections:
        s["editId"] = f"{chapter_id}/{s['id']}"

    # Enriquecimento de Bloco D: reaproveita o campo alternatives verbatim da futura
    alternatives = {}
    if bloco_d:
        fk = DEPARA_BLOCO_D.get(organ_key)
        alt = bloco_d.get(fk) if fk else None
        if alt:
            alternatives = alt  # cópia verbatim; NÃO tocar em sections

    return {
        "id": chapter_id, "kind": "organ", "chapterTitle": chapter_title,
        "organKey": organ_key, "label": organ.get("name", ""), "abbr": abbr,
        "sections": sections,
        "alternatives": alternatives,
    }


# Cadeia de comando do cenário atual: pai de cada órgão conforme a estrutura vigente
# validada (organograma oficial). `cg` (Comando-Geral) é a raiz. Comandante-Geral e
# Subcomandante-Geral são cargos internos de `cg`, por isso os órgãos que lhes respondem
# pendem de `cg`; os do Estado-Maior pendem de `emg`; o GBS pende do Comando Operacional.
COMMAND_PARENT = {
    "cepdec": "cg", "condeg": "cg", "comissoes": "cg", "gabinete": "cg",
    "assessorias": "cg", "dint": "cg", "cpof": "cg",
    "corregedoria": "cg", "ajudancia": "cg", "emg": "cg",
    "dp": "emg", "deei": "emg", "cat": "emg", "dlog": "emg", "dcs": "emg", "dinf": "emg",
    "cob1": "cg", "cob2": "cg", "coa": "cg", "gbs": "cob1",
}


def build_command_chart_atual(chapters):
    """Árvore da cadeia de comando (mesmo formato de build_command_chart da futura:
    nós {organKey, sigla, label, chapterId, children}), montada pelo COMMAND_PARENT
    da estrutura vigente. Retorna o nó raiz `cg`."""
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
    for k, node in nodes.items():
        parent = COMMAND_PARENT.get(k)
        if parent and parent in nodes:
            nodes[parent]["children"].append(node)
    return nodes.get("cg")


def main():
    organs = json.loads(RO_JSON.read_text(encoding="utf-8")).get("organs", {})
    bloco_d = _bloco_d_futura()  # carrega uma vez; as alternativas independem do cenário do RO

    chapters = []
    for organ_key, chapter_title, _art in ATUAL_ORGAN_ORDER:
        o = organs.get(organ_key)
        if not o:
            print(f"  ! órgão ausente no ro.json (atual): {organ_key} — pulando")
            continue
        chapters.append(build_organ_chapter_atual(organ_key, chapter_title, o, bloco_d))

    output = {
        "generated_by": "scripts/build_minuta_structure_atual.py",
        "cenario": "atual",
        "title": TITLE,
        "chapters": chapters,
        "commandChart": build_command_chart_atual(chapters),
    }
    OUT_JSON.parent.mkdir(parents=True, exist_ok=True)
    OUT_JSON.write_text(json.dumps(output, ensure_ascii=False, indent=2), encoding="utf-8")

    n_sec = sum(len(c.get("sections", [])) for c in chapters)
    print(f"Gerado: {OUT_JSON}")
    print(f"  {len(chapters)} capítulo(s) · {n_sec} seções de função")


if __name__ == "__main__":
    main()
