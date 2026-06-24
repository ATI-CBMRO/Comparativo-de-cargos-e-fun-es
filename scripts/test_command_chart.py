"""Teste da forma da árvore commandChart (sem pytest: rodar com python)."""
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import build_minuta_structure as B  # noqa: E402
from build_minuta_structure import build_command_chart  # noqa: E402

RO_JSON = Path(__file__).parent.parent / "database" / "organs_detail" / "ro.json"


def _chapters(organs):
    chapters = [B.build_preliminares_chapter(), B.build_estrutura_chapter(organs)]
    for k, title, _a in B.ORGAN_ORDER:
        o = organs.get(k)
        if o:
            chapters.append(B.build_organ_chapter(k, title, o))
    chapters.append(B.build_guarnicao_chapter())
    chapters.append(B.build_finais_chapter())
    return chapters


def kids(node):
    return {c["organKey"]: c for c in node["children"]}


def main():
    organs = json.loads(RO_JSON.read_text(encoding="utf-8"))["organs"]
    chart = build_command_chart(organs, _chapters(organs))

    assert chart.get("synthetic") is True
    assert chart["label"] == "Subcomandante-Geral"

    top = kids(chart)
    assert set(top) == {"dpo", "doe"}, list(top)
    dpo = kids(top["dpo"])
    assert set(dpo) == {"cot", "crbm"}, list(dpo)
    assert set(kids(dpo["cot"])) == {"cat"}
    crbm = kids(dpo["crbm"])
    assert set(crbm) == {"bbm", "cibm"}, list(crbm)
    bbm = kids(crbm["bbm"])
    assert set(bbm) == {"gbm"}
    assert set(kids(bbm["gbm"])) == {"guarnicao"}
    assert set(kids(top["doe"])) == {"bbs", "bifea", "boa"}, list(kids(top["doe"]))

    def walk(n):
        if not n.get("synthetic"):
            assert n["chapterId"].startswith("organ:"), n
            assert "sigla" in n and "label" in n, n
        for c in n["children"]:
            walk(c)
    walk(chart)

    print("OK: commandChart shape correct")


if __name__ == "__main__":
    main()
