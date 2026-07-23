"""
aplicar_decisoes_vault.py — Portal CBM (cockpit Fase 3)

Aplica no vault Obsidian as decisões registradas no sistema (decisoes_export.json,
baixado da aba Decisões). Preenche '## Decisão CBMRO' + 'decidido: true'.
Regras duras: conflito com decisão manual divergente NÃO sobrescreve (reporta);
idempotente; nota ausente reporta; qualquer anomalia => saída != 0.

Rodar: .venv-pipeline/bin/python scripts/aplicar_decisoes_vault.py <export.json> [--vault <dir>]
"""
import json
import os
import re
import sys
from pathlib import Path

DEFAULT_VAULT = Path.home() / "Documents" / "Obsidian Vault" / "Codebases" / "Comparativo-de-cargos-e-funcoes"
SUBPASTAS = ["Regimento Interno — Curadoria", "Regulamento — Curadoria"]
SECAO_RE = re.compile(r"(## Decisão CBMRO\n)(.*?)(?=\n## |\Z)", re.DOTALL)


def _eh_placeholder(txt):
    t = txt.strip()
    return not t or t.startswith("_(") or t.startswith("<!--")


def _rodape(dec):
    quem = dec.get("registradoPor") or "sistema"
    quando = (dec.get("registradoEm") or "")[:10] or "data não informada"
    return f"_Registrado no sistema por {quem} em {quando}._"


def aplicar(export_path, vault):
    export = json.loads(Path(export_path).read_text(encoding="utf-8"))
    r = {"aplicadas": 0, "ja_aplicadas": 0, "conflitos": 0, "nao_encontradas": 0, "detalhes": []}
    for dec in export:
        nota = None
        for sub in SUBPASTAS:
            p = Path(vault) / sub / f"{dec['id']}.md"
            if p.exists():
                nota = p
                break
        if nota is None:
            r["nao_encontradas"] += 1
            r["detalhes"].append(f"NÃO ENCONTRADA: {dec['id']}")
            continue
        txt = nota.read_text(encoding="utf-8")
        m = SECAO_RE.search(txt)
        atual = m.group(2) if m else ""
        novo_corpo = f"{dec['decisao'].strip()}\n\n{_rodape(dec)}\n"
        if not _eh_placeholder(atual):
            # Idempotência pelo BLOCO inteiro (decisão + rodapé determinístico), não só
            # pelo texto da decisão — evita falso "já aplicada" quando o texto da decisão
            # coincide por acaso com um trecho de uma nota manual não relacionada.
            if novo_corpo.strip() in atual:
                r["ja_aplicadas"] += 1
                continue
            r["conflitos"] += 1
            r["detalhes"].append(f"CONFLITO (decisão manual divergente): {dec['id']}")
            continue
        if m:
            txt = SECAO_RE.sub(lambda mm: mm.group(1) + novo_corpo, txt, count=1)
        else:
            txt = txt.rstrip() + f"\n\n## Decisão CBMRO\n{novo_corpo}"
        txt = re.sub(r"^decidido: false$", "decidido: true", txt, count=1, flags=re.MULTILINE)
        nota.write_text(txt, encoding="utf-8")
        r["aplicadas"] += 1
    return r


def main():
    if len(sys.argv) < 2:
        sys.exit("Uso: aplicar_decisoes_vault.py <decisoes_export.json> [--vault <dir>]")
    export_path = sys.argv[1]
    vault = Path(os.environ.get("VAULT_CURADORIA", str(DEFAULT_VAULT)))
    if "--vault" in sys.argv:
        vault = Path(sys.argv[sys.argv.index("--vault") + 1])
    if not vault.is_dir():
        sys.exit(f"ERRO: vault não encontrado em {vault} (defina VAULT_CURADORIA ou use --vault).")
    r = aplicar(export_path, vault)
    print(f"Aplicadas: {r['aplicadas']} · Já aplicadas: {r['ja_aplicadas']} · "
          f"Conflitos: {r['conflitos']} · Não encontradas: {r['nao_encontradas']}")
    for d in r["detalhes"]:
        print(" -", d)
    if r["conflitos"] or r["nao_encontradas"]:
        sys.exit(1)


if __name__ == "__main__":
    main()
