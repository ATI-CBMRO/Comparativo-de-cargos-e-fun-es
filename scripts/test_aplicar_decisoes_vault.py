import json
import tempfile
import unittest
from pathlib import Path
from aplicar_decisoes_vault import aplicar

NOTA = """---
tags: [cbmro, curadoria, decisao]
type: decisao
themeKey: servico-operacional
decidido: false
---
# Decisão — servico-operacional — folga

**Questão:** Quanto de folga?

## Decisão CBMRO
_(a preencher pelo Wândrio — redação escolhida e o porquê)_

## Ligações
[[Tema — servico-operacional]]
"""

EXPORT = [{
    "id": "Decisão — servico-operacional — folga",
    "tipo": "redacao", "decisao": "Adotar 12h/36h (critério de exclusividade de AL).",
    "fonteEscolhida": "Alagoas", "alvoDispositivoId": "reg:servico-operacional/x#caput",
    "registradoPor": "Wândrio", "registradoEm": "2026-07-23T12:00:00Z",
}]


class TestAplicar(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.vault = Path(self.tmp.name)
        (self.vault / "Regulamento — Curadoria").mkdir()
        (self.vault / "Regimento Interno — Curadoria").mkdir()
        self.nota = self.vault / "Regulamento — Curadoria" / "Decisão — servico-operacional — folga.md"
        self.nota.write_text(NOTA, encoding="utf-8")
        self.export = self.vault / "decisoes_export.json"
        self.export.write_text(json.dumps(EXPORT), encoding="utf-8")

    def tearDown(self):
        self.tmp.cleanup()

    def test_aplica_e_marca_decidido(self):
        r = aplicar(self.export, self.vault)
        self.assertEqual(r["aplicadas"], 1)
        txt = self.nota.read_text(encoding="utf-8")
        self.assertIn("decidido: true", txt)
        self.assertIn("Adotar 12h/36h", txt)
        self.assertIn("_Registrado no sistema por Wândrio", txt)
        self.assertNotIn("_(a preencher", txt)

    def test_idempotente(self):
        aplicar(self.export, self.vault)
        r2 = aplicar(self.export, self.vault)
        self.assertEqual(r2["aplicadas"], 0)
        self.assertEqual(r2["ja_aplicadas"], 1)
        self.assertEqual(self.nota.read_text(encoding="utf-8").count("_Registrado no sistema"), 1)

    def test_conflito_nao_sobrescreve(self):
        self.nota.write_text(NOTA.replace(
            "_(a preencher pelo Wândrio — redação escolhida e o porquê)_",
            "Decisão manual DIFERENTE tomada no papel."), encoding="utf-8")
        r = aplicar(self.export, self.vault)
        self.assertEqual(r["conflitos"], 1)
        self.assertIn("Decisão manual DIFERENTE", self.nota.read_text(encoding="utf-8"))

    def test_nota_ausente(self):
        self.nota.unlink()
        r = aplicar(self.export, self.vault)
        self.assertEqual(r["nao_encontradas"], 1)

    def test_texto_coincidente_por_acaso_e_conflito_nao_ja_aplicada(self):
        # A decisão manual contém, por coincidência, o MESMO texto da decisão do sistema —
        # mas SEM o rodapé "_Registrado no sistema..._" que só o próprio script escreve.
        # Idempotência deve exigir o bloco inteiro (decisão + rodapé), não só o texto.
        self.nota.write_text(NOTA.replace(
            "_(a preencher pelo Wândrio — redação escolhida e o porquê)_",
            "Adotar 12h/36h (critério de exclusividade de AL). Decidido em reunião presencial."),
            encoding="utf-8")
        r = aplicar(self.export, self.vault)
        self.assertEqual(r["conflitos"], 1)
        self.assertEqual(r["ja_aplicadas"], 0)
        self.assertNotIn("_Registrado no sistema", self.nota.read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()
