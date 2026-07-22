"""
triagem_acervo.py — helper READ-ONLY da skill ingestar-acervo.

Não renomeia, move, nem edita nenhum arquivo. Só lê PDFs e imprime um relatório de
triagem: qualidade da extração, tipo proposto por conteúdo e validação do prefixo do
nome contra STATE_META. As 3 funções puras (score_extracao, tipo_por_conteudo,
valida_prefixo) não importam pypdf nem build_states_data.
"""

import re
import unicodedata

GLYPH_RE = re.compile(r'/U[0-9A-Fa-f]{4}')


def score_extracao(texto: str) -> str:
    """Classifica a qualidade da extração em OK / SUSPEITO / RUIM.

    Puro: recebe o texto já extraído (amostra de páginas). Sinaliza os dois modos de
    falha já vistos no projeto: fonte mapeada por glifos (/U00XX, caso RJ DAT) e
    PDF escaneado/garble com baixa densidade alfabética (caso Piauí).
    """
    if not texto:
        return "RUIM"
    total = len(texto)
    glyph_chars = sum(len(m.group()) for m in GLYPH_RE.finditer(texto))
    glyph_ratio = glyph_chars / total
    if glyph_ratio > 0.30:
        return "RUIM"
    non_space = [c for c in texto if not c.isspace()]
    if not non_space:
        return "RUIM"
    alpha_ratio = sum(1 for c in non_space if c.isalpha()) / len(non_space)
    if alpha_ratio < 0.45:
        return "RUIM"
    if glyph_ratio > 0.05 or alpha_ratio < 0.60:
        return "SUSPEITO"
    return "OK"


def _norm(s: str) -> str:
    """Minúsculas + sem acento (NFKD), para casar palavras-chave e prefixos."""
    s = unicodedata.normalize('NFKD', s or '')
    s = ''.join(c for c in s if not unicodedata.combining(c))
    return s.lower()


# (lista de palavras-chave normalizadas, tipo canônico) — ordem: mais específico primeiro.
# Regras de "serviço diário" vêm antes de "regimento interno"/"regulamento" de propósito:
# um regulamento/regimento de SERVIÇO deve ser proposto como Regimento de Serviços, não
# como Regulamento Geral só pela palavra no título (caso PA).
_CONTENT_RULES = [
    (["diretriz operacional", "gestor operacional de dia", "supervisor do ciops",
      "servico operacional de dia", "superior de dia", "escala de servico",
      "servico de dia", "atividades diarias",
      "servicos administrativos, preventivos e operacionais",
      "normas ou procedimentos para os servicos"], "Regimento de Serviços"),
    (["quadro demonstrativo"], "Quadro Demonstrativo de Cargos"),
    (["quadro de organizacao", "quadro de distribuicao"], "Quadro de Organização e Distribuição"),
    (["normas gerais de acao"], "Normas Gerais de Ação"),
    (["regimento interno"], "Regimento Interno"),
    (["regulamento geral", "regulamenta a lei", "aprova o regulamento"], "Regulamento Geral"),
    (["organizacao basica", "lei organica", "reorganiza o corpo de bombeiros",
      "cria o corpo de bombeiros", "organizacao estrutural e funcional"],
     "Lei de Organização Básica"),
]


def tipo_por_conteudo(texto: str) -> str:
    """Propõe o tipo canônico do documento pela ementa/primeiros artigos. Consultivo:
    a decisão final é humana. Devolve 'Indefinido' quando nada casa."""
    n = _norm(texto)
    for termos, tipo in _CONTENT_RULES:
        if any(t in n for t in termos):
            return tipo
    return "Indefinido"


def valida_prefixo(nome: str, state_meta: dict):
    """Valida o prefixo do nome de arquivo (texto antes de ' - ') contra STATE_META.

    Retorna (True, chave) se casa exatamente; (False, chave_canônica) se existe com
    caixa/acento diferentes (sugestão de correção); (False, None) se não há separador
    ou o estado é desconhecido.
    """
    base = nome.rsplit('.', 1)[0]
    if ' - ' not in base:
        return (False, None)
    prefixo = base.split(' - ', 1)[0].strip()
    if prefixo in state_meta:
        return (True, prefixo)
    alvo = _norm(prefixo)
    for chave in state_meta:
        if _norm(chave) == alvo:
            return (False, chave)
    return (False, None)


def ler_amostra(pdf_path, paginas: int = 3):
    """Lê as primeiras `paginas` páginas do PDF e devolve (texto, total_paginas).
    Importa pypdf tardiamente para não exigir a lib nos testes puros."""
    from pypdf import PdfReader
    reader = PdfReader(pdf_path)
    partes = [(reader.pages[i].extract_text() or "") for i in range(min(paginas, len(reader.pages)))]
    return "\n".join(partes), len(reader.pages)


def _carregar_pipeline():
    """Importa STATE_META e parse_doc_type do build do repo (só quando roda como CLI)."""
    import sys
    from pathlib import Path
    repo_root = Path(__file__).resolve().parents[4]
    sys.path.insert(0, str(repo_root / "scripts"))
    from build_states_data import STATE_META, parse_doc_type
    return STATE_META, parse_doc_type


def main():
    import argparse
    import os
    parser = argparse.ArgumentParser(description="Triagem read-only de PDFs para o Acervo.")
    parser.add_argument("pasta", help="Pasta com os PDFs a triar (ex.: a de staging).")
    parser.add_argument("--paginas", type=int, default=3, help="Páginas amostradas por PDF.")
    args = parser.parse_args()

    state_meta, parse_doc_type = _carregar_pipeline()
    pdfs = sorted(f for f in os.listdir(args.pasta) if f.lower().endswith(".pdf"))
    if not pdfs:
        print(f"Nenhum PDF em: {args.pasta}")
        return

    print(f"Triagem de {len(pdfs)} PDF(s) em: {args.pasta}\n")
    for nome in pdfs:
        caminho = os.path.join(args.pasta, nome)
        try:
            texto, npag = ler_amostra(caminho, args.paginas)
        except Exception as e:
            print(f"[ERRO] {nome}: {e!r}")
            continue
        ok_prefixo, sugestao = valida_prefixo(nome, state_meta)
        md_nome = os.path.splitext(nome)[0] + ".md"
        tipo_nome = parse_doc_type(md_nome)
        tipo_conteudo = tipo_por_conteudo(texto)
        score = score_extracao(texto)
        diverge = "DIVERGE" if (tipo_conteudo != "Indefinido" and tipo_conteudo != tipo_nome) else "ok"
        pref = "ok" if ok_prefixo else (f"corrigir->{sugestao}" if sugestao else "ESTADO DESCONHECIDO")
        print(f"• {nome}  ({npag} pág.)")
        print(f"    prefixo/STATE_META : {pref}")
        print(f"    qualidade extração : {score}")
        print(f"    tipo por nome      : {tipo_nome}")
        print(f"    tipo por conteúdo  : {tipo_conteudo}  [{diverge}]")
        print()


if __name__ == "__main__":
    main()
