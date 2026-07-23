import unittest
from build_decisoes_curadoria import parse_decisao

NOTA_RI = """---
type: decisao
organKey: dlog
decidido: false
---
# Decisão — ri — dlog — fusao-logistica-financas
**Questão:** A minuta trata Logística e Finanças como dois órgãos.

## Redações candidatas

### Paraná — Lei nº 22.206/2024 (fusão)
> A Diretoria de Apoio Logístico e Finanças é o órgão de direção responsável por:
> I - coordenação das atividades de logística;
`cf. CBMPR, Lei nº 22.206/2024, Art. 29`
**Leitura:** os incisos do PR misturam logística e finanças.

### Distrito Federal — RI (Portaria nº 24/2020)
> Art. 218. À Diretoria de Materiais e Serviços, além das atri buições, compete:
`cf. CBMDF, RI (Portaria nº 24/2020), Art. 218`
*(OCR do documento-fonte quebra "atribuições" em "atri buições".)*
**Leitura:** o DF trata só de logística.

## Comparação
- DF e PA convergem entre si.
- PR diverge dos dois.

## Decisão CBMRO
_(a preencher pelo Wândrio — manter separados ou fundir)_

## Ligações
[[Órgão — dlog]] · [[Órgão — dpof]] · [[Fonte — RI-PR]]
"""

NOTA_REG_DECIDIDA = """---
type: decisao
themeKey: servico-operacional
decidido: true
---
# Decisão — servico-operacional — folga
**Questão:** Quanto de folga após 12h?

## Redações candidatas

### Sergipe (primária) — RISD
> O serviço será em regime de 12 horas.
`cf. CBMSE, RISD, Art. 48`
**Leitura:** SE fixa só a jornada.

## Comparação
- TO e AL divergem.

## Decisão CBMRO
Adotar o critério de exclusividade de AL: 12h/36h para militar exclusivo.

## Ligações
[[Tema — servico-operacional]]
"""


class TestParseDecisao(unittest.TestCase):
    def test_ri_estrutura_completa(self):
        d = parse_decisao(NOTA_RI, "Decisão — ri — dlog — fusao-logistica-financas.md", "ri")
        self.assertEqual(d["trilha"], "ri")
        self.assertEqual(d["key"], "dlog")
        self.assertEqual(d["chapterId"], "organ:dlog")
        self.assertEqual(d["titulo"], "Decisão — ri — dlog — fusao-logistica-financas")
        self.assertTrue(d["questao"].startswith("A minuta trata Logística"))
        self.assertEqual(len(d["candidatas"]), 2)
        self.assertEqual(d["candidatas"][0]["fonte"], "Paraná — Lei nº 22.206/2024 (fusão)")
        self.assertEqual(d["candidatas"][0]["verbatim"][0],
                         "A Diretoria de Apoio Logístico e Finanças é o órgão de direção responsável por:")
        self.assertEqual(len(d["candidatas"][0]["verbatim"]), 2)
        self.assertEqual(d["candidatas"][0]["citacao"], "cf. CBMPR, Lei nº 22.206/2024, Art. 29")
        self.assertIsNone(d["candidatas"][0]["ocr"])
        self.assertTrue(d["candidatas"][0]["leitura"].startswith("os incisos do PR"))
        # OCR preservado na 2ª candidata
        self.assertIn("atri buições", d["candidatas"][1]["verbatim"][0])
        self.assertIsNotNone(d["candidatas"][1]["ocr"])
        self.assertEqual(len(d["comparacao"]), 2)
        self.assertEqual(d["ligadas"], ["Órgão — dlog", "Órgão — dpof", "Fonte — RI-PR"])
        # placeholder itálico → decisao None
        self.assertFalse(d["decidido"])
        self.assertIsNone(d["decisao"])

    def test_reg_decidida(self):
        d = parse_decisao(NOTA_REG_DECIDIDA, "Decisão — servico-operacional — folga.md", "reg")
        self.assertEqual(d["key"], "servico-operacional")
        self.assertEqual(d["chapterId"], "reg:servico-operacional")
        self.assertTrue(d["decidido"])
        self.assertTrue(d["decisao"].startswith("Adotar o critério"))

    def test_sem_questao_falha(self):
        ruim = "---\ntype: decisao\nthemeKey: x\ndecidido: false\n---\n# Título\n## Comparação\n- a\n"
        with self.assertRaises(ValueError):
            parse_decisao(ruim, "Decisão — x.md", "reg")


NOTA_LEGADO_TABELA = """---
type: decisao
organKey: assessorias
decidido: false
---
# Decisão — RI — Assessorias — Subordinação das assessorias

**Órgão:** [[Órgão — assessorias]]

## O problema

A minuta do RO organiza Assessorias como órgão autônomo. As alternativas divergem entre si.

## Excertos verbatim

**[[Fonte — Minuta-RI-PA]] — Art. 69, §1º:**

> "As assessorias técnicas são voltadas a assuntos especializados da Corporação , mediante
> indicação do Chefe."

*(nota: espaço antes da vírgula em "Corporação , mediante" reproduz OCR do PDF de origem —
mantido tal como está no JSON.)*

**[[Fonte — RI-RS]] — Art. 31 (caput):**

> "Art. 31. Ao Gabinete do Comandante-Geral, compete:"

## Os três modelos, lado a lado

| Ente | Onde ficam | Subordinadas a |
|---|---|---|
| RO (minuta) | Órgão próprio | Direto ao Comandante-Geral |
| PA | Capítulo próprio | Chefe do DGA |

## Decisão CBMRO

"""

NOTA_LEGADO_DIVERGENCIA = """---
type: decisao
organKey: corregedoria
decidido: false
---
# Decisão — RI — corregedoria — requisito

## Contexto

O RO e o PR divergem sobre quem pode ser Corregedor-Geral.

## Excertos verbatim

**RO** (`Órgão — corregedoria`, `cf. ro`):

> Corregedor-Geral (Oficial da ativa do último Posto).

**Paraná** (cf. CBMPR, RI (coletânea do portal), Art. 23):

> Art. 23 A Corregedoria-Geral é o órgão técnico.

## Divergência

O RO exige apenas quadro geral. O PR exige linha combatente.

## Decisão CBMRO

<!-- Preencher com a decisão do Wândrio/Comando -->
"""


class TestParseDecisaoLegado(unittest.TestCase):
    def test_legado_com_tabela(self):
        d = parse_decisao(NOTA_LEGADO_TABELA, "Decisão — ri — assessorias — x.md", "ri")
        self.assertEqual(d["key"], "assessorias")
        self.assertTrue(d["questao"].startswith("A minuta do RO organiza"))
        self.assertEqual(len(d["candidatas"]), 2)
        self.assertIn("Fonte — Minuta-RI-PA", d["candidatas"][0]["fonte"])
        self.assertTrue(d["candidatas"][0]["verbatim"][0].startswith("As assessorias"))
        # nota OCR multi-linha: não pode sumir, tem que vir concatenada e completa
        self.assertIsNotNone(d["candidatas"][0]["ocr"])
        self.assertIn("Corporação , mediante", d["candidatas"][0]["ocr"])
        self.assertIn("mantido tal como está no JSON", d["candidatas"][0]["ocr"])
        self.assertTrue(len(d["comparacao"]) >= 1)
        self.assertIn("Órgão — assessorias", d["ligadas"])
        self.assertIsNone(d["decisao"])

    def test_legado_com_divergencia_e_comentario_html(self):
        d = parse_decisao(NOTA_LEGADO_DIVERGENCIA, "Decisão — ri — corregedoria — y.md", "ri")
        self.assertEqual(len(d["candidatas"]), 2)
        self.assertEqual(d["candidatas"][0]["citacao"], "cf. ro")
        # citação com parêntese aninhado não pode ser truncada antes de "Art. 23"
        self.assertEqual(d["candidatas"][1]["citacao"],
                          "cf. CBMPR, RI (coletânea do portal), Art. 23")
        self.assertTrue(len(d["comparacao"]) >= 1)
        self.assertIsNone(d["decisao"])  # comentário HTML placeholder -> None

    def test_legado_sem_problema_nem_contexto_falha(self):
        ruim = (
            "---\ntype: decisao\norganKey: x\ndecidido: false\n---\n"
            "# Título\n## Excertos verbatim\n**A** (cf. x):\n> texto\n"
        )
        with self.assertRaises(ValueError):
            parse_decisao(ruim, "Decisão — x.md", "ri")


if __name__ == "__main__":
    unittest.main()
