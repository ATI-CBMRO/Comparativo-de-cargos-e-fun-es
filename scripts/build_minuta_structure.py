"""
build_minuta_structure.py — Portal CBM

Gera database/minuta_structure.json: minuta ARTICULADA e HIERÁRQUICA do Regimento
Interno da estrutura OPERACIONAL do CBMRO — do topo (DPO/COT/DOE) à menor fração
(Companhia/GBM). Um capítulo por órgão; uma seção por função (cargo).

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
from minuta_enrichment import enrich_for, enrich_organ_for  # noqa: E402

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

BASE_DIR = Path(__file__).parent.parent
RO_JSON  = BASE_DIR / "database" / "organs_detail" / "ro.json"
OUT_JSON = BASE_DIR / "database" / "minuta_structure.json"

TITLE = "DO REGIMENTO INTERNO DA ESTRUTURA OPERACIONAL DO CBMRO"

# Ordem dos capítulos = ordem de subordinação (topo → menor fração).
# (organ_key, CHAPTER_TITLE, artigo_definido)
ORGAN_ORDER = [
    ("dpo",   "DA DIRETORIA DE PLANEJAMENTO OPERACIONAL (DPO)",          "A"),
    ("cot",   "DO COMANDO DE OPERAÇÕES TÉCNICAS (COT)",                  "O"),
    ("doe",   "DA DIRETORIA OPERACIONAL ESPECIALIZADA (DOE)",            "A"),
    ("crbm",  "DOS COMANDOS REGIONAIS DE BOMBEIRO MILITAR (CRBM)",       "O"),
    ("bbm",   "DO BATALHÃO DE BOMBEIROS MILITAR (BBM)",                  "O"),
    ("cibm",  "DA COMPANHIA INDEPENDENTE DE BOMBEIROS MILITAR (CIBM)",   "A"),
    ("gbm",   "DO GRUPO DE BOMBEIROS MILITAR (GBM)",                     "O"),
    ("bbs",   "DO BATALHÃO DE BUSCA E SALVAMENTO (BBS)",                 "O"),
    ("bifea", "DO BATALHÃO DE INCÊNDIO FLORESTAL E EMERGÊNCIAS AMBIENTAIS (BIFEA)", "O"),
    ("boa",   "DO BATALHÃO DE OPERAÇÕES AÉREAS (BOA)",                   "O"),
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


def build_estrutura_chapter(organs):
    items = []
    for (organ_key, _title, art) in ORGAN_ORDER:
        o = organs.get(organ_key)
        if not o:
            continue
        nome = o.get("name", organ_key.upper())
        abbr = o.get("abbreviation") or organ_key.upper()
        items.append({"text": f"{art.lower()} {nome} ({abbr})", "source": "ro"})
    return {
        "id": "estrutura", "kind": "incisos", "chapterTitle": "DA ESTRUTURA ORGANIZACIONAL",
        "editId": "estrutura",
        "caput": "A estrutura operacional do Corpo de Bombeiros Militar do Estado de Rondônia compõe-se dos seguintes órgãos:",
        "items": items, "proposedText": proposed_text(items),
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


def build_finais_chapter():
    return {
        "id": "finais", "kind": "prose", "chapterTitle": "DAS DISPOSIÇÕES FINAIS",
        "editId": "finais", "proposedText": DISP_FINAIS,
    }


def main():
    organs = json.loads(RO_JSON.read_text(encoding="utf-8")).get("organs", {})

    chapters = [build_preliminares_chapter(), build_estrutura_chapter(organs)]
    for organ_key, chapter_title, _art in ORGAN_ORDER:
        o = organs.get(organ_key)
        if not o:
            print(f"  ! órgão ausente no ro.json: {organ_key} — pulando")
            continue
        chapters.append(build_organ_chapter(organ_key, chapter_title, o))
    chapters.append(build_finais_chapter())

    output = {
        "generated_by": "scripts/build_minuta_structure.py",
        "title": TITLE,
        "chapters": chapters,
    }
    OUT_JSON.write_text(json.dumps(output, ensure_ascii=False, indent=2), encoding="utf-8")

    n_org = sum(1 for c in chapters if c["kind"] == "organ")
    n_sec = sum(len(c.get("sections", [])) for c in chapters if c["kind"] == "organ")
    print(f"Gerado: {OUT_JSON}")
    print(f"  {len(chapters)} capítulos · {n_org} órgãos · {n_sec} seções de função")


if __name__ == "__main__":
    main()
