# Skill de Ingestão do Acervo Legal — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Criar a skill `ingestar-acervo` (checklist do SOP de 9 passos + helper Python read-only de triagem) e aplicá-la ao batch de documentos novos pendentes, levando-os à camada 1 (Acervo).

**Architecture:** Uma skill autocontida em `.claude/skills/ingestar-acervo/` com `SKILL.md` (processo) e `scripts/triagem_acervo.py` (triagem read-only). O helper tem 3 funções puras (`score_extracao`, `tipo_por_conteudo`, `valida_prefixo`) testadas via `assert`, mais uma camada fina de I/O (pypdf + CLI) que orquestra o relatório. A aplicação ao batch usa os scripts de pipeline existentes e edita `CONTENT_TYPE_OVERRIDES`/`CONTENT_VERIFIED_FILES` em `build_states_data.py`.

**Tech Stack:** Python 3.10+ (pypdf, unicodedata, re, argparse), convenção de teste `test_*.py` com `assert` (padrão do repo), Markdown para o `SKILL.md`.

---

## File Structure

- **Create** `.claude/skills/ingestar-acervo/SKILL.md` — frontmatter (name/description-gatilho) + os 9 passos do SOP como checklist.
- **Create** `.claude/skills/ingestar-acervo/scripts/triagem_acervo.py` — helper read-only: 3 funções puras + camada fina de I/O (pypdf) + CLI.
- **Create** `.claude/skills/ingestar-acervo/scripts/test_triagem_acervo.py` — testes das 3 funções puras (não importa pypdf nem `build_states_data`).
- **Modify** `package.json` — anexar o teste do helper ao script `test:py`.
- **Modify** `scripts/build_states_data.py` — atualizar `CONTENT_TYPE_OVERRIDES` e `CONTENT_VERIFIED_FILES` para o batch (Task 8).
- **Modify** `.claude/PENDENCIAS.md` — registrar handoff das camadas 2/3 por documento (Task 8).

Princípio de isolamento do helper: as 3 funções puras não dependem de pypdf nem de `build_states_data` no import (pypdf é importado tardiamente dentro da função de I/O; `STATE_META`/`parse_doc_type` são importados só dentro de `main()`). Assim `test_triagem_acervo.py` roda sem pypdf instalado e sem disparar o glob de `build_states_data.py`.

---

## Task 1: Scaffold da skill — SKILL.md

**Files:**
- Create: `.claude/skills/ingestar-acervo/SKILL.md`

- [ ] **Step 1: Criar o SKILL.md com frontmatter e os 9 passos**

Conteúdo exato do arquivo:

```markdown
---
name: ingestar-acervo
description: "Use ao adicionar ou atualizar documentos de legislação no Acervo Legal do portal CBM (novos PDFs em 'LEGISLAÇÃO CBMS/', atualizar acervo, reclassificar tipo de documento). Leva o documento à camada 1 (acervo) e carimba seu destino nas minutas (RI/Regulamento). NÃO faz curadoria verbatim das camadas 2/3."
---

# Ingestão de documento ao Acervo Legal (camada 1)

Processo padrão para receber, curar e adicionar novos documentos legais ao acervo do
portal. Leva cada documento até aparecer na tabela de cobertura, com tipo classificado e
verificado, e registra seu destino downstream (minuta de RI, minuta de Regulamento ou
referência) sem executar a curadoria cara das camadas 2/3.

Crie um todo por passo e execute na ordem. Os passos 1 e 3 usam o helper de triagem:
`python scripts/triagem_acervo.py "<pasta>"` (a partir da pasta desta skill), que é
READ-ONLY (não renomeia, move, nem edita nada).

## Passo 0 — Congelar o batch
A pasta de staging dentro de `LEGISLAÇÃO CBMS/` sincroniza ao vivo pelo OneDrive (nome e
conteúdo podem mudar durante o trabalho). Liste os PDFs com tamanho, copie para um local
estável fora do staging e confirme o conjunto ANTES de processar. Nunca assuma o conjunto.

## Passo 1 — Normalizar nomenclatura
Rode o helper de triagem sobre a pasta congelada. Para cada arquivo, garanta o nome
`<Estado por extenso> - <Descrição>.pdf`, com o prefixo (texto antes de " - ") batendo
EXATAMENTE uma chave de `STATE_META` em `scripts/build_states_data.py` (acentos e caixa
incluídos) — é assim que o build deriva o estado. Corrija acento/caixa se o helper acusar
divergência. Mova o arquivo normalizado para a RAIZ de `LEGISLAÇÃO CBMS/` (o
`convert_to_markdown.py` só varre o topo, não subpastas).

## Passo 2 — Converter
`python scripts/convert_to_markdown.py` (na raiz do repo).

## Passo 3 — Gate de qualidade da extração
Leia o score do helper. Se `RUIM` (PDF escaneado sem OCR ou fonte por glifos `/U00XX`):
PARE e decida — buscar fonte com OCR, ou registrar "no acervo, extração pendente de OCR"
com `typeVerified` falso. Não prossiga no automático para documentos `RUIM`.

## Passo 4 — Classificar por CONTEÚDO
Leia ementa/primeiros artigos e escolha o tipo canônico entre: `Lei de Organização
Básica`, `Regimento Interno`, `Regimento de Serviços`, `Regulamento Geral`, `Normas Gerais
de Ação`, `Quadro Demonstrativo de Cargos`, `Quadro de Organização e Distribuição`.
Compare com `parse_doc_type(nome)`:
- Coincide → adicione o `.md` a `CONTENT_VERIFIED_FILES` (selo ✓).
- Diverge → adicione/ajuste `CONTENT_TYPE_OVERRIDES[<arquivo.md>] = <tipo correto>` e
  marque verificado.
- Arquivo renomeado → REMOVA a chave de override antiga e crie a nova; apague o `.md`
  antigo em `database/markdown/`.

## Passo 5 — Rebuild completo (ordem importa)
```
python scripts/convert_to_markdown.py
python scripts/build_organs_detail.py
python scripts/build_states_data.py
python scripts/build_dpo_cot_comparison.py
python scripts/build_minuta_comparison.py
python scripts/build_minuta_structure.py
python scripts/build_regulamento_structure.py
```

## Passo 6 — Verificar (evidência antes de afirmar)
Diff de `database/states_data.json`: o documento aparece no estado + tipo certos,
`typeVerified` correto, contadores e célula da tabela de cobertura atualizados. Rode
`npm test` (lógica de `acervoCoverage` etc.). Opcional: `npm run dev` e conferir a página
Acervo em http://localhost:5173/legislacoes.

## Passo 7 — Handoff para camadas 2/3
Registre em `.claude/PENDENCIAS.md`, por documento, se é candidato à camada de comparação
e/ou à minuta, e QUAL minuta, pelo mapa:

| Tipo | Alimenta | Script downstream |
|---|---|---|
| Regimento Interno (organizacional) | Minuta de RI | ri_alternativas_enrichment.py, minuta_enrichment.py |
| Regulamento Geral ou Regimento de Serviços | Minuta de Regulamento | regulamento_enrichment_<uf>.py |
| Lei de Organização Básica | camada LOB | lob_enrichment.py |
| Quadro / Normas Gerais de Ação | referência (não alimenta minuta) | — |
| RI de diretoria ou extração RUIM | só acervo, sinalizado | — |

## Passo 8 — Limpeza + registro
Remova os arquivos processados do staging, atualize a contagem do acervo no CLAUDE.md se
mudou e proponha commit (só commite se o usuário pedir).
```

- [ ] **Step 2: Verificar que o arquivo existe e tem frontmatter**

Run: `head -4 ".claude/skills/ingestar-acervo/SKILL.md"`
Expected: mostra as linhas `---`, `name: ingestar-acervo`, `description: ...`, `---`.

- [ ] **Step 3: Commit**

```bash
git add ".claude/skills/ingestar-acervo/SKILL.md"
git commit -m "feat(skill): SKILL.md da ingestao-acervo (SOP de 9 passos)"
```

---

## Task 2: Helper — função pura `score_extracao` (TDD)

**Files:**
- Create: `.claude/skills/ingestar-acervo/scripts/triagem_acervo.py`
- Test: `.claude/skills/ingestar-acervo/scripts/test_triagem_acervo.py`

- [ ] **Step 1: Escrever o teste que falha**

Criar `.claude/skills/ingestar-acervo/scripts/test_triagem_acervo.py`:

```python
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

from triagem_acervo import score_extracao

# Texto legal em português bem extraído -> OK
bom = ("Art. 1º Fica aprovado o Regulamento Geral do Corpo de Bombeiros Militar, "
       "que dispõe sobre a organização e o funcionamento da corporação. "
       "Parágrafo único. As disposições desta lei aplicam-se a todos os órgãos.")
assert score_extracao(bom) == "OK", score_extracao(bom)

# Fonte mapeada por glifos (caso RJ DAT) -> RUIM
glifos = "/U0044/U0049/U0052/U0049/U004F /U0050/U004F/U0044/U0045/U0052 /U0045/U0058"
assert score_extracao(glifos) == "RUIM", score_extracao(glifos)

# Texto vazio -> RUIM
assert score_extracao("") == "RUIM"
assert score_extracao(None) == "RUIM"

# Garble de símbolos/dígitos com pouca letra -> RUIM
lixo = "12 34 %% ## @@ 55 || 77 && (( )) ** ++ == 99 :: ;;"
assert score_extracao(lixo) == "RUIM", score_extracao(lixo)

print("score_extracao OK")
```

- [ ] **Step 2: Rodar o teste para ver falhar**

Run: `python3 ".claude/skills/ingestar-acervo/scripts/test_triagem_acervo.py"`
Expected: FAIL com `ModuleNotFoundError: No module named 'triagem_acervo'` (o helper ainda não existe).

- [ ] **Step 3: Implementar `score_extracao`**

Criar `.claude/skills/ingestar-acervo/scripts/triagem_acervo.py`:

```python
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
```

- [ ] **Step 4: Rodar o teste para ver passar**

Run: `python3 ".claude/skills/ingestar-acervo/scripts/test_triagem_acervo.py"`
Expected: imprime `score_extracao OK` e sai com código 0.

- [ ] **Step 5: Commit**

```bash
git add ".claude/skills/ingestar-acervo/scripts/triagem_acervo.py" ".claude/skills/ingestar-acervo/scripts/test_triagem_acervo.py"
git commit -m "feat(skill): score_extracao (gate de qualidade da extracao)"
```

---

## Task 3: Helper — função pura `tipo_por_conteudo` (TDD)

**Files:**
- Modify: `.claude/skills/ingestar-acervo/scripts/triagem_acervo.py`
- Test: `.claude/skills/ingestar-acervo/scripts/test_triagem_acervo.py`

- [ ] **Step 1: Adicionar o teste que falha**

Anexar ao final de `test_triagem_acervo.py` (antes de nada — adicione a importação no topo junto da existente):

No topo, trocar a linha de import por:
```python
from triagem_acervo import score_extracao, tipo_por_conteudo
```

Acrescentar ao FINAL do arquivo (depois de `print("score_extracao OK")`):
```python
# tipo_por_conteudo: Portaria/Diretriz Operacional (caso MA) -> Regimento de Serviços
ma = ("PORTARIA Nº 46/2020 Aprova Diretriz Operacional para o Serviço de Gestor "
      "Operacional de Dia, Supervisor do CIOPS e Superior de Dia.")
assert tipo_por_conteudo(ma) == "Regimento de Serviços", tipo_por_conteudo(ma)

# Decreto de serviços diários (caso PA) -> Regimento de Serviços
pa = ("Dispõe sobre as normas ou procedimentos para os serviços administrativos, "
      "preventivos e operacionais a serem adotados nas atividades diárias.")
assert tipo_por_conteudo(pa) == "Regimento de Serviços", tipo_por_conteudo(pa)

# LOB -> Lei de Organização Básica
lob = "Dispõe sobre a organização básica do Corpo de Bombeiros Militar e dá providências."
assert tipo_por_conteudo(lob) == "Lei de Organização Básica", tipo_por_conteudo(lob)

# Quadro demonstrativo -> Quadro Demonstrativo de Cargos
assert tipo_por_conteudo("Quadro Demonstrativo de Cargos e Funções") == "Quadro Demonstrativo de Cargos"

# Texto sem pista reconhecível -> Indefinido
assert tipo_por_conteudo("Bom dia a todos, segue o comunicado.") == "Indefinido"

print("tipo_por_conteudo OK")
```

- [ ] **Step 2: Rodar o teste para ver falhar**

Run: `python3 ".claude/skills/ingestar-acervo/scripts/test_triagem_acervo.py"`
Expected: FAIL com `ImportError: cannot import name 'tipo_por_conteudo'`.

- [ ] **Step 3: Implementar `tipo_por_conteudo` e o helper `_norm`**

Adicionar em `triagem_acervo.py` (após `score_extracao`):

```python
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
```

- [ ] **Step 4: Rodar o teste para ver passar**

Run: `python3 ".claude/skills/ingestar-acervo/scripts/test_triagem_acervo.py"`
Expected: imprime `score_extracao OK`, `tipo_por_conteudo OK`, sai com 0.

- [ ] **Step 5: Commit**

```bash
git add ".claude/skills/ingestar-acervo/scripts/triagem_acervo.py" ".claude/skills/ingestar-acervo/scripts/test_triagem_acervo.py"
git commit -m "feat(skill): tipo_por_conteudo (classificacao por conteudo, consultiva)"
```

---

## Task 4: Helper — função pura `valida_prefixo` (TDD)

**Files:**
- Modify: `.claude/skills/ingestar-acervo/scripts/triagem_acervo.py`
- Test: `.claude/skills/ingestar-acervo/scripts/test_triagem_acervo.py`

- [ ] **Step 1: Adicionar o teste que falha**

No topo do teste, trocar a linha de import por:
```python
from triagem_acervo import score_extracao, tipo_por_conteudo, valida_prefixo
```

Acrescentar ao FINAL do arquivo (depois de `print("tipo_por_conteudo OK")`):
```python
# valida_prefixo: usa um STATE_META falso pequeno (teste puro, sem importar o real)
FAKE_META = {"Maranhão": {"id": "ma"}, "Pará": {"id": "pa"}, "Mato Grosso": {"id": "mt"}}

# prefixo exato -> (True, prefixo)
assert valida_prefixo("Maranhão - Portaria.pdf", FAKE_META) == (True, "Maranhão")

# caixa/acento diferentes -> (False, forma canônica sugerida)
assert valida_prefixo("maranhao - Portaria.pdf", FAKE_META) == (False, "Maranhão")

# estado inexistente -> (False, None)
assert valida_prefixo("Xingu - Foo.pdf", FAKE_META) == (False, None)

# sem separador " - " -> (False, None)
assert valida_prefixo("SemSeparador.pdf", FAKE_META) == (False, None)

print("valida_prefixo OK")
```

- [ ] **Step 2: Rodar o teste para ver falhar**

Run: `python3 ".claude/skills/ingestar-acervo/scripts/test_triagem_acervo.py"`
Expected: FAIL com `ImportError: cannot import name 'valida_prefixo'`.

- [ ] **Step 3: Implementar `valida_prefixo`**

Adicionar em `triagem_acervo.py` (após `tipo_por_conteudo`):

```python
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
```

- [ ] **Step 4: Rodar o teste para ver passar**

Run: `python3 ".claude/skills/ingestar-acervo/scripts/test_triagem_acervo.py"`
Expected: imprime as 3 linhas `... OK` e sai com 0.

- [ ] **Step 5: Commit**

```bash
git add ".claude/skills/ingestar-acervo/scripts/triagem_acervo.py" ".claude/skills/ingestar-acervo/scripts/test_triagem_acervo.py"
git commit -m "feat(skill): valida_prefixo (nome de arquivo x STATE_META)"
```

---

## Task 5: Helper — camada de I/O (pypdf) + CLI do relatório

**Files:**
- Modify: `.claude/skills/ingestar-acervo/scripts/triagem_acervo.py`

Sem teste automatizado (é I/O sobre PDFs); a verificação é rodar contra a pasta real do batch no Step 3.

- [ ] **Step 1: Adicionar a leitura de PDF e a CLI**

Adicionar ao final de `triagem_acervo.py`:

```python
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
        md_nome = nome[:-4] + ".md"
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
```

- [ ] **Step 2: Sanidade — importar o módulo não deve exigir pypdf nem rodar o build**

Run: `python3 -c "import sys; sys.path.insert(0, '.claude/skills/ingestar-acervo/scripts'); import triagem_acervo; print('import OK')"`
Expected: imprime `import OK` sem erro (as funções puras carregam; pypdf e build_states_data só entram em runtime da CLI).

- [ ] **Step 3: Rodar a CLI contra a pasta de staging real e conferir o relatório**

Primeiro descubra o nome atual da pasta de staging (o OneDrive pode tê-la renomeado):
Run: `ls "LEGISLAÇÃO CBMS/" | grep -iE "novo|regulament.*intern" || ls "LEGISLAÇÃO CBMS/"`

Depois rode (ajuste o nome da pasta ao que apareceu):
Run: `python3 ".claude/skills/ingestar-acervo/scripts/triagem_acervo.py" "LEGISLAÇÃO CBMS/NOVOS DOCUMENTOS"`
Expected: uma ficha por PDF. Para "Maranhão - Portaria.pdf": `tipo por nome: Lei de Organização Básica`, `tipo por conteúdo: Regimento de Serviços [DIVERGE]`. Para "Pará - Regulamento de serviço.pdf": `tipo por nome: Regulamento Geral`, `tipo por conteúdo: Regimento de Serviços [DIVERGE]`. Prefixos "Maranhão"/"Pará" → `ok`.

- [ ] **Step 4: Commit**

```bash
git add ".claude/skills/ingestar-acervo/scripts/triagem_acervo.py"
git commit -m "feat(skill): camada de I/O (pypdf) + CLI do relatorio de triagem"
```

---

## Task 6: Wire do teste no `test:py`

**Files:**
- Modify: `package.json`

- [ ] **Step 1: Anexar o teste do helper ao script `test:py`**

Em `package.json`, localizar a linha do `test:py` (termina em `... && python3 scripts/test_minuta_alternativas.py`) e acrescentar ao final, ainda dentro das aspas:

```
 && python3 ".claude/skills/ingestar-acervo/scripts/test_triagem_acervo.py"
```

O valor final de `test:py` deve terminar com:
`... && python3 scripts/test_minuta_alternativas.py && python3 ".claude/skills/ingestar-acervo/scripts/test_triagem_acervo.py"`

- [ ] **Step 2: Rodar a cadeia de testes Python inteira**

Run: `npm run test:py`
Expected: todos os testes anteriores passam e, ao final, aparecem `score_extracao OK`, `tipo_por_conteudo OK`, `valida_prefixo OK`; o comando sai com código 0.

- [ ] **Step 3: Commit**

```bash
git add package.json
git commit -m "test(skill): inclui test_triagem_acervo no test:py"
```

---

## Task 7: Ponto de checagem — a skill está completa

- [ ] **Step 1: Revisar a skill de ponta a ponta**

Confirme:
- `SKILL.md` tem frontmatter válido e os 9 passos.
- `python3 -c "..."` de import passa (Task 5 Step 2).
- `npm run test:py` verde (Task 6 Step 2).
- A CLI produz relatório coerente (Task 5 Step 3).

Se algo falhar, corrija antes de aplicar ao batch. **A partir daqui, os passos são a
APLICAÇÃO da skill ao batch atual — envolvem arquivos sincronizados ao vivo (OneDrive) e
decisões de conteúdo; re-snapshot antes de agir.**

---

## Task 8: Aplicar a skill ao batch atual (camada 1)

**Files:**
- Modify: `scripts/build_states_data.py` (dicts `CONTENT_TYPE_OVERRIDES` e `CONTENT_VERIFIED_FILES`)
- Modify: `.claude/PENDENCIAS.md`
- Filesystem: renomear/mover PDFs em `LEGISLAÇÃO CBMS/`, apagar `.md` órfãos em `database/markdown/`

> Segue o Passo 0→8 do `SKILL.md`. As decisões abaixo foram apuradas por leitura de
> conteúdo no brainstorming (2026-07-13); **re-verifique** porque a pasta sincroniza ao vivo.

- [ ] **Step 1: Passo 0 — congelar e listar o batch**

Run: `git status --short -- "LEGISLAÇÃO CBMS/" ; ls "LEGISLAÇÃO CBMS/"`
Anote: (a) PDFs de staging (pasta "NOVOS DOCUMENTOS" ou nome atual), (b) renomeações já em
disco (MT: "Regimento Interno"→"Regulamento Geral"; SE: "Regimento Interno"→"Regulamento
Interno"), (c) SC ("Organização Básica alterações"). Se o conjunto mudou vs. o esperado,
rode o helper de triagem de novo e reavalie antes de prosseguir.

- [ ] **Step 2: Passos 1–3 — normalizar nomes e triar staging**

Mova cada PDF de staging para a RAIZ de `LEGISLAÇÃO CBMS/` com nome canônico
`<Estado> - <Descrição>.pdf` (prefixo exato de `STATE_META`). Para o batch conhecido:
- `Maranhão - Portaria.pdf` → manter nome (prefixo "Maranhão" ok).
- `Pará - Regulamento de serviço.pdf` → manter nome (prefixo "Pará" ok).

Run (triagem final na raiz, confirme score ≠ RUIM para os dois):
`python3 ".claude/skills/ingestar-acervo/scripts/triagem_acervo.py" "LEGISLAÇÃO CBMS"`
Expected: MA e PA com score `OK`/`SUSPEITO` (não `RUIM`) e `[DIVERGE]` no tipo.

- [ ] **Step 3: Passo 2 — converter para markdown**

Run: `python scripts/convert_to_markdown.py`
Expected: `Successfully converted` para "Maranhão - Portaria.pdf", "Pará - Regulamento de serviço.pdf", "Mato Grosso - Regulamento Geral.pdf", "Sergipe - Regulamento Interno.pdf", "Santa Catarina - Organização Básica alterações.pdf".

- [ ] **Step 4: Passo 4 — apagar `.md` órfãos das renomeações**

Os PDFs antigos de MT/SE foram renomeados; seus `.md` antigos ficam órfãos em
`database/markdown/`. Remova-os:

Run: `rm -f "database/markdown/Mato Grosso - Regimento Interno.md" "database/markdown/Sergipe - Regimento Interno.md"`
Expected: sem erro; confirme com `ls "database/markdown/" | grep -iE "mato grosso|sergipe"` que sobraram só os nomes novos.

- [ ] **Step 5: Passo 4 — atualizar `CONTENT_TYPE_OVERRIDES` em `scripts/build_states_data.py`**

Substituir o bloco atual (linhas ~396–405) do dict `CONTENT_TYPE_OVERRIDES`. Estado atual:

```python
CONTENT_TYPE_OVERRIDES = {
    "Mato Grosso - Regimento Interno.md": "Regulamento Geral",
    "Sergipe - Regimento Interno.md": "Regimento de Serviços",
    "Santa Catarina - Organização Básica.md": "Regimento Interno",
}
```

Novo conteúdo (remove chaves órfãs de MT/SE; MT some porque o novo nome já classifica
certo por `parse_doc_type`; SE migra para o novo nome; adiciona MA e PA):

```python
CONTENT_TYPE_OVERRIDES = {
    # SE: arquivo renomeado para "Regulamento Interno", mas o conteúdo é o RISD
    # (regimento de serviços) — parse_doc_type daria "Regulamento Geral" pelo nome.
    "Sergipe - Regulamento Interno.md": "Regimento de Serviços",
    # SC: "Organização Básica" é o Decreto 1.328/2021 que REGULAMENTA a LOB — perfil
    # de Regimento Interno (ver CLAUDE.md "Classificação de tipo de documento").
    "Santa Catarina - Organização Básica.md": "Regimento Interno",
    # MA: "Portaria" é a Diretriz Operacional do serviço diário (Gestor Operacional de
    # Dia, CIOPS) — regimento de serviço; parse_doc_type cairia no default LOB.
    "Maranhão - Portaria.md": "Regimento de Serviços",
    # PA: "Regulamento de serviço" é o Decreto 1.052/2020 de serviços diários — regimento
    # de serviço; parse_doc_type daria "Regulamento Geral" pela palavra "regulamento".
    "Pará - Regulamento de serviço.md": "Regimento de Serviços",
}
```

> Nota MT: o novo arquivo "Mato Grosso - Regulamento Geral.md" faz `parse_doc_type`
> retornar "Regulamento Geral" sozinho, então NÃO precisa de override. MT já está em
> `CONTENT_VERIFIED_STATES`, então segue verificado.

- [ ] **Step 6: Passo 4 — marcar MA e PA como verificados por conteúdo**

MA não está em `CONTENT_VERIFIED_STATES`; adicionar o arquivo a `CONTENT_VERIFIED_FILES`.
PA já está em `CONTENT_VERIFIED_STATES` (cobre todos os arquivos do PA), então não precisa.

Em `scripts/build_states_data.py`, dentro do set `CONTENT_VERIFIED_FILES` (após a linha
`"Maranhão - Quadro de Organização e Distribuição.md",`), inserir:

```python
    # Diretriz Operacional (Portaria 46/2020) — conteúdo lido e confirmado como
    # regimento de serviço (2026-07-13).
    "Maranhão - Portaria.md",
```

Para o SC: leia o conteúdo de `database/markdown/Santa Catarina - Organização Básica alterações.md`
(ementa/primeiros artigos). Se for de fato uma lei que ALTERA a LOB do CBMSC (perfil de
Lei de Organização Básica, o default de `parse_doc_type`), adicione também
`"Santa Catarina - Organização Básica alterações.md",` a `CONTENT_VERIFIED_FILES`
(SC não está em `CONTENT_VERIFIED_STATES`). Se o conteúdo divergir do default, trate como
divergência (override) conforme o Passo 4 do SKILL.md.

- [ ] **Step 7: Passo 5 — rebuild completo (ordem importa)**

Run:
```bash
python scripts/convert_to_markdown.py && \
python scripts/build_organs_detail.py && \
python scripts/build_states_data.py && \
python scripts/build_dpo_cot_comparison.py && \
python scripts/build_minuta_comparison.py && \
python scripts/build_minuta_structure.py && \
python scripts/build_regulamento_structure.py
```
Expected: todos concluem sem exceção; `build_states_data.py` reporta os estados processados.

- [ ] **Step 8: Passo 6 — verificar o `states_data.json`**

Run:
```bash
python3 -c "import json; d=json.load(open('database/states_data.json', encoding='utf-8')); \
docs=[(s['id'], doc['md_file'], doc['type'], doc['typeVerified']) \
for s in d['states'] for doc in s.get('documents', []) \
if s['id'] in ('ma','pa','mt','se','sc')]; \
[print(x) for x in sorted(docs)]"
```
(As chaves reais do objeto documento são `type`, `typeVerified`, `md_file`, `char_count`,
`year`, `laws`, `has_pdf`; as de estado incluem `id`. Confirmado no build atual.)

Expected (confira cada linha):
- `('ma', 'Maranhão - Portaria.md', 'Regimento de Serviços', True)`
- `('pa', 'Pará - Regulamento de serviço.md', 'Regimento de Serviços', True)`
- `('mt', 'Mato Grosso - Regulamento Geral.md', 'Regulamento Geral', True)`
- `('se', 'Sergipe - Regulamento Interno.md', 'Regimento de Serviços', True)`
- `('sc', 'Santa Catarina - Organização Básica alterações.md', 'Lei de Organização Básica', <True se adicionado a CONTENT_VERIFIED_FILES no passo de verificação de conteúdo do SC; caso contrário False>)`
- não deve existir nenhuma linha com `'Mato Grosso - Regimento Interno.md'` ou `'Sergipe - Regimento Interno.md'`.

- [ ] **Step 9: Passo 6 — rodar os testes de lógica**

Run: `npm test && npm run test:py`
Expected: ambos verdes (nenhuma regressão em `acervoCoverage`, comparadores etc.).

- [ ] **Step 10: Passo 7 — handoff das camadas 2/3 no `.claude/PENDENCIAS.md`**

Na seção `## 🔴 Pendente` de `.claude/PENDENCIAS.md`, adicionar:

```markdown
- [ ] Camada 2/3 dos documentos ingeridos em 2026-07-13 (camada 1 concluída):
  - **MA - Portaria** (Regimento de Serviços) → candidato à Minuta de Regulamento (regulamento_enrichment_ma.py).
  - **PA - Regulamento de serviço** (Regimento de Serviços) → candidato à Minuta de Regulamento (regulamento_enrichment_pa.py; PA já tem RI organizacional separado).
  - **SC - Organização Básica alterações** (LOB) → candidato à camada LOB (lob_enrichment.py).
  - **MT/SE** já cobertos na trilha de Regulamento; renomeações só corrigiram o rótulo no acervo.
```

- [ ] **Step 11: Passo 8 — commit da ingestão**

```bash
git add scripts/build_states_data.py database/ .claude/PENDENCIAS.md "LEGISLAÇÃO CBMS/"
git status --short
git commit -m "feat(acervo): ingere MA/PA e reclassifica MT/SE/SC (camada 1)"
```
> Antes de commitar, revise `git status --short` para não incluir a pasta de staging
> "NOVOS DOCUMENTOS/" nem arquivos indesejados; se ela ainda existir, remova-a do staging
> (`git reset` no path) ou apague-a do disco após confirmar que os PDFs já estão na raiz.

---

## Notas de execução

- **Branch:** o Tiago autorizou commits em `master` para o spec. Confirme com ele se a
  implementação também vai direto em `master` ou numa branch `feat/skill-ingestao-acervo`
  antes de começar (repo compartilhado).
- **`python` vs `python3`:** no Windows do Tiago o comando é `python`; os scripts de teste
  do repo usam `python3` (via `test:py`). Use o que estiver disponível no ambiente de
  execução — a lógica é idêntica.
- **Push:** não fazer `git push` sem pedido explícito.
