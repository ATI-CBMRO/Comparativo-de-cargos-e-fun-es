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
    """Mapeia filhos por organKey — só serve para nós com capítulo próprio
    (estruturais como Cia BM/Pel BM têm organKey None e não entram aqui)."""
    return {c["organKey"]: c for c in node["children"] if c.get("organKey")}


def only_child(node):
    assert len(node["children"]) == 1, node["children"]
    return node["children"][0]


def main():
    organs = json.loads(RO_JSON.read_text(encoding="utf-8"))["organs"]
    chart = build_command_chart(organs, _chapters(organs))

    # Desde bfc9ef6, cg é raiz real da árvore (não sintética) — os 26 órgãos da
    # LOB formam uma única árvore conectada sob o Comando-Geral.
    assert not chart.get("synthetic")
    assert chart["organKey"] == "cg"
    assert chart["label"] == "Comando Geral"

    top = kids(chart)
    assert set(top) == {
        "depdec", "condeg", "dp", "deei", "dpof", "dsap", "dlog",
        "dpo", "doe", "cint", "ccs", "cinf", "assessorias", "gab-cg", "ag",
        "corregedoria",
    }, list(top)
    dpo = kids(top["dpo"])
    assert set(dpo) == {"cot", "crbm"}, list(dpo)
    assert set(kids(dpo["cot"])) == {"cat"}
    crbm = kids(dpo["crbm"])
    assert set(crbm) == {"bbm", "cibm", "gbm"}, list(crbm)
    assert set(kids(top["doe"])) == {"bbs", "bifea", "boa"}, list(kids(top["doe"]))

    # BBM -> Cia BM (estrutural) -> Pel BM (estrutural) -> Guarnição (capítulo).
    cia = only_child(crbm["bbm"])
    assert cia["structural"] is True and cia["sigla"] == "Cia BM", cia
    pel = only_child(cia)
    assert pel["structural"] is True and pel["sigla"] == "Pel BM", pel
    guarnicao = only_child(pel)
    assert guarnicao["organKey"] == "guarnicao" and guarnicao["chapterId"] == "organ:guarnicao", guarnicao

    def walk(n):
        if n.get("synthetic") or n.get("structural"):
            pass  # raiz sintética e nós estruturais (Cia/Pel) não têm capítulo
        else:
            assert n["chapterId"].startswith("organ:"), n
            assert "sigla" in n and "label" in n, n
        for c in n["children"]:
            walk(c)
    walk(chart)

    print("OK: commandChart shape correct")


if __name__ == "__main__":
    main()
