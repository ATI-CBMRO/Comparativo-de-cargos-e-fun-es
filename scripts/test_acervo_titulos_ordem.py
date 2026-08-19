"""Títulos de exibição e ordem dos documentos do acervo (sem pytest: rodar com python).

Cobre as duas garantias da entrega de 20/08/2026:

1. Toda chave de DOCUMENT_TITLE_OVERRIDES aponta para um markdown que existe.
   É o modo de falha silencioso deste mecanismo: um nome de arquivo com typo faz
   o .get() cair no `type` sem erro nenhum, e o documento continua exibido com o
   rótulo errado — exatamente o problema que o override existia para corrigir.

2. Os documentos de cada estado saem na ordem de exibição (LOB → Regimento
   Interno → documentos de serviço → demais).
"""
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from build_states_data import (  # noqa: E402
    DOC_TYPE_DISPLAY_ORDER,
    DOCUMENT_TITLE_OVERRIDES,
    doc_sort_key,
)

RAIZ = Path(__file__).parent.parent
MARKDOWN_DIR = RAIZ / "database" / "markdown"
STATES_JSON = RAIZ / "database" / "states_data.json"


def test_overrides_apontam_para_arquivos_reais():
    faltando = [nome for nome in DOCUMENT_TITLE_OVERRIDES if not (MARKDOWN_DIR / nome).exists()]
    assert not faltando, f"DOCUMENT_TITLE_OVERRIDES aponta para arquivos inexistentes: {faltando}"
    print(f"OK: {len(DOCUMENT_TITLE_OVERRIDES)} overrides de título, todos com markdown correspondente")


def test_override_nao_repete_o_type():
    """Override igual ao `type` é ruído: não muda nada e sugere uma correção que não houve."""
    dados = json.loads(STATES_JSON.read_text(encoding="utf-8"))
    redundantes = [
        doc["md_file"]
        for estado in dados["states"]
        for doc in estado.get("documents", [])
        if doc["md_file"] in DOCUMENT_TITLE_OVERRIDES and doc.get("title") == doc.get("type")
    ]
    assert not redundantes, f"override idêntico ao type (remova): {redundantes}"
    print("OK: nenhum override redundante")


def test_doc_sort_key_ordena_por_tipo():
    docs = [
        {"type": "Quadro Demonstrativo de Cargos", "md_file": "z.md"},
        {"type": "Regimento de Serviços", "md_file": "b.md"},
        {"type": "Lei de Organização Básica", "md_file": "a.md"},
        {"type": "Regimento Interno", "md_file": "c.md"},
    ]
    ordenado = [d["type"] for d in sorted(docs, key=doc_sort_key)]
    assert ordenado == [
        "Lei de Organização Básica",
        "Regimento Interno",
        "Regimento de Serviços",
        "Quadro Demonstrativo de Cargos",
    ], ordenado

    # Mesmo tipo desempata pelo nome do arquivo, para a ordem não oscilar entre
    # execuções e sujar o diff do JSON gerado.
    mesmos = [
        {"type": "Regulamento Geral", "md_file": "Alagoas - Norma Operacional 02.md"},
        {"type": "Regulamento Geral", "md_file": "Alagoas - Diretriz Operacional 01.md"},
    ]
    assert [d["md_file"] for d in sorted(mesmos, key=doc_sort_key)] == [
        "Alagoas - Diretriz Operacional 01.md",
        "Alagoas - Norma Operacional 02.md",
    ]
    print("OK: doc_sort_key ordena por tipo e desempata pelo arquivo")


def test_json_gerado_esta_na_ordem():
    dados = json.loads(STATES_JSON.read_text(encoding="utf-8"))
    fora = []
    for estado in dados["states"]:
        docs = estado.get("documents", [])
        postos = [
            DOC_TYPE_DISPLAY_ORDER.index(d["type"])
            if d["type"] in DOC_TYPE_DISPLAY_ORDER
            else len(DOC_TYPE_DISPLAY_ORDER)
            for d in docs
        ]
        if postos != sorted(postos):
            fora.append(estado["name"])
    assert not fora, f"estados com documentos fora da ordem de exibição: {fora}"
    print(f"OK: {len(dados['states'])} estados com documentos na ordem LOB → RI → serviço → demais")


def main():
    test_overrides_apontam_para_arquivos_reais()
    test_override_nao_repete_o_type()
    test_doc_sort_key_ordena_por_tipo()
    test_json_gerado_esta_na_ordem()


if __name__ == "__main__":
    main()
