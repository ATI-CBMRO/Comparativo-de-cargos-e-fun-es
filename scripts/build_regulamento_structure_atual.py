"""Gera database/atual/regulamento_structure.json — MINUTA do Regulamento do CBMRO
para o cenário LOB ATUAL (vigente, Lei nº 2.204/2009).

Decisão de produto (validada 2026-07-15): o Regulamento do cenário atual NASCE PRÓPRIO,
ancorado na ESTRUTURA VIGENTE (um capítulo por órgão, mesma ordem do RI atual), como
ESQUELETO a ser enriquecido depois com os temas dos regulamentos de outros estados
adaptados à LOB atual. Totalmente isolado do Regulamento da LOB futura — nada se mistura.

Formato de saída compatível com RegulamentoWizard.jsx (chapters com themeKey/group/
status/articles/alternatives; editId com prefixo 'reg:').

Entrada:  database/atual/organs_detail/ro.json
Saída:    database/atual/regulamento_structure.json
"""
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from build_minuta_structure_atual import ATUAL_ORGAN_ORDER  # mesma ordem/lista de órgãos  # noqa: E402

BASE_DIR = Path(__file__).parent.parent
RO_JSON = BASE_DIR / "database" / "atual" / "organs_detail" / "ro.json"
OUT_JSON = BASE_DIR / "database" / "atual" / "regulamento_structure.json"

TITLE = "DO REGULAMENTO DO CORPO DE BOMBEIROS MILITAR DO ESTADO DE RONDÔNIA (CBMRO) — LOB ATUAL"


def _slug(s):
    out = []
    for ch in s.lower():
        out.append(ch if ch.isalnum() else "-")
    return "-".join("".join(out).split("-")).strip("-")


def build_chapter(organ_key, chapter_title, organ):
    """Um capítulo por órgão. Artigos = competências verbatim do próprio CBMRO
    (Lei 2.204/2009), como base a regulamentar. Sem enriquecimento de outros estados
    (entra na curadoria seguinte). editId com prefixo 'reg:' e escopo 'atual-' para
    garantir isolamento de cenário e de documento."""
    theme_key = f"atual-{organ_key}"
    articles = []
    atribs = [a for a in (organ.get("atribuicoes") or []) if a.strip()]
    if atribs:
        articles.append({
            "id": f"atual-{organ_key}-caput",
            "kind": "incisos",
            "editId": f"reg:atual-{theme_key}/{organ_key}-caput",
            "caput": f"O presente Capítulo regula a atuação da {organ.get('name', organ_key)} no âmbito do CBMRO, com base nas competências fixadas na Lei nº 2.204/2009:",
            "items": [{"text": a, "source": "RO"} for a in atribs],
            "source": "RO",
            "match": None,
            "heading": None,
            "adapted": False,
            "original_caput": None,
        })
    return {
        "id": f"organ:{organ_key}",
        "kind": "articles",  # exigido por buildArticles para emitir os artigos do capítulo
        "chapterTitle": chapter_title,
        "group": organ.get("category", ""),
        "themeKey": theme_key,
        "primary": "RO",
        "status": "esqueleto",  # a enriquecer com temas de outros estados
        "articles": articles,
        "alternatives": {},  # cenário atual: sem enriquecimento de outros estados ainda
    }


def main():
    organs = json.loads(RO_JSON.read_text(encoding="utf-8")).get("organs", {})

    chapters = []
    for organ_key, chapter_title, _art in ATUAL_ORGAN_ORDER:
        o = organs.get(organ_key)
        if not o:
            print(f"  ! órgão ausente no ro.json (atual): {organ_key} — pulando")
            continue
        chapters.append(build_chapter(organ_key, chapter_title, o))

    output = {
        "generated_by": "scripts/build_regulamento_structure_atual.py",
        "cenario": "atual",
        "title": TITLE,
        "chapters": chapters,
    }
    OUT_JSON.parent.mkdir(parents=True, exist_ok=True)
    OUT_JSON.write_text(json.dumps(output, ensure_ascii=False, indent=2), encoding="utf-8")

    n_art = sum(len(c["articles"]) for c in chapters)
    print(f"Gerado: {OUT_JSON}")
    print(f"  {len(chapters)} capítulo(s) · {n_art} artigo(s)-base")


if __name__ == "__main__":
    main()
