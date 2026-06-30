# Camada LOB do /comparar — curadoria verbatim das LOBs (plano)

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Enriquecer as colunas 2 (LOB pura) e 3 (LOB + RI) do `/comparar` com a finalidade/competências verbatim que cada LOB estadual dá a cada um dos 26 órgãos, via uma camada de dados curada e isolada.

**Architecture:** Novo `scripts/lob_enrichment.py` (`LOB_ENRICHMENT[(organ_key, state_id)]`). `scripts/build_minuta_comparison.py` passa a (a) montar a coluna 2 a partir dessa camada quando houver entrada, (b) unir a entrada da LOB na coluna 3 junto do RI da Frente 2, e (c) **adicionar** ao comparativo estados que só têm LOB. `organs_detail/*.json`, `comparativo_dpo_cot.json` e `ENRICHMENT_ORGAN` nunca são tocados.

**Tech Stack:** Python 3 (build, sem pytest no pipeline — verificação por script de asserção `python`), Node `--test` (suíte JS existente), Git.

---

## Contexto compartilhado (ler antes de qualquer tarefa)

**As 3 colunas do `/comparar`** (já existem em `src/pages/MinutaComparator.jsx`, `PairTable`):
1. **CBMRO** — referência (LOB do RO).
2. **LOB do estado** — `state.lobOrgans` / `state.lobProvenance`.
3. **LOB + RI (compilada)** — `state.organs` / `state.provenance`.

**Matriz de campos** (`src/lib/comparatorRender.jsx`, `MATRIX_ROWS`): Órgão/Sigla,
Subordinação, Cargo/Função, Requisito/Posto, **Atribuições/Competências**, Desdobramentos.
A finalidade + incisos da LOB entram no campo **Atribuições/Competências** (`atribuicoes`).

**Critério (camada LOB, relaxado vs Frente 2):** entra a **finalidade/caput verbatim**
(1 frase) E/OU os **incisos verbatim** que a LOB enumera para o órgão. Sempre transcrição
fiel, com correção de OCR óbvio (ex.: "as as" → "as"); **nunca** parafrasear/condensar/
inventar. Itens de **RI não entram** nesta camada (são da Frente 2). Citação obrigatória:
`cf. CBMxx, LOB (Lei nº …/ano), Art. N`.

**Os 26 órgãos** (organ_keys, de `ORGAN_ORDER` em `scripts/build_minuta_structure.py`):
`cg, depdec, condeg, dp, deei, dpof, dsap, dlog, dpo, doe, cot, cat, cint, ccs, cinf, crbm,
bbm, cibm, bbs, bifea, boa, gbm, corregedoria, assessorias, gab-cg, ag`. (A `guarnicao` fica
fora — não há LOB estadual equivalente.)

**Mapa nome→organ_key (sinônimos comuns; o estado nomeia diferente):**
- `cg` Comando-Geral / Estado-Maior-Geral (como unidade)
- `depdec` Proteção e Defesa Civil / Coordenadoria Estadual de Defesa Civil
- `condeg` Conselho (Deliberativo / Superior / de Administração)
- `dp` Pessoal / Gestão de Pessoas / Recursos Humanos
- `deei` Ensino / Instrução / Educação / Academia
- `dpof` Finanças / Orçamento / Planejamento administrativo / Gestão e Finanças
- `dsap` Saúde / Assistência (ao Pessoal/Social)
- `dlog` Logística / Apoio Logístico / Material e Patrimônio / Suprimento
- `dpo` Planejamento Operacional / Operações (planejamento)
- `doe` Operacional Especializada
- `cot` Operações Técnicas / Atividades Técnicas / Segurança contra Incêndio
- `cat` Atividades Técnicas (coordenadoria)
- `cint` Inteligência
- `ccs` Comunicação Social
- `cinf` Informática / Tecnologia da Informação
- `crbm` Comando(s) Regional(is)
- `bbm` Batalhão
- `cibm` Companhia Independente
- `bbs` Busca e Salvamento
- `bifea` Incêndio Florestal / Emergências Ambientais
- `boa` Operações Aéreas / Aviação
- `gbm` Grupamento / Grupo
- `corregedoria` Corregedoria
- `assessorias` Assessoria(s)
- `gab-cg` Gabinete do Comandante-Geral
- `ag` Ajudância-Geral / Secretaria-Geral

**Arquivos de LOB** em `database/markdown/` (um por estado; quando houver duas variantes,
usar a CONSOLIDADA/mais recente e registrar a Lei no rótulo):
`Acre - Organização Básica (Lei 2.009-2008 att Lei 4.428-2024).md`, `Alagoas - Lei de
Organização Básica.md`, `Amazonas - Organização Básica.md`, `Amapá - Organização Básica.md`,
`Bahia - Organização Básica.md`, `Ceará - Organização Básica (Lei 13.438-2004).md`,
`Distrito Federal - Organização Básica.md`, `Espírito Santo - Lei de Organização Básica.md`,
`Goiás - Organização Básica (Lei 18.305-2013).md`, `Maranhão - Organização Básica.md`,
`Minas Gerais - Organização Básica.md`, `Mato Grosso do Sul - Organização Básica.md`,
`Mato Grosso - Organização Básica.md`, `Pará - Organização Básica.md`, `Paraíba - Organização
Básica.md`, `Pernambuco - Organização Básica (Lei 15.187-2013).md`, `Piauí - Organização
Básica (Lei 5.949-2009 alt. Lei 7.772-2022).md`, `Paraná - Organização Básica.md`, `Rio de
Janeiro - Organização Básica.md`, `Rio Grande do Norte - Organização Básica.md`, `Roraíma -
Organização Básica.md`, `Rio Grande do Sul - Organização Básica.md`, `Santa Catarina -
Organização Básica.md`, `Sergipe - Organização Básica (Lei 8.979-2022).md`, `São Paulo -
Organização Básica (Lei 616-1974).md`, `Tocantins - Organização Básica.md`.

**Formato de entrada em `LOB_ENRICHMENT`** (uma por par órgão×estado com conteúdo):
```python
("dp", "sc"): {
    "finalidade": "<caput verbatim, 1 frase — ou '' se a LOB só enumera incisos>",
    "competencias": ["<inciso verbatim>", "<inciso verbatim>"],  # [] se só finalidade
    "source": "cf. CBMSC, LOB (Lei nº 1.058/2024), Art. N",
    "organName": "Diretoria de Pessoal",   # nome do órgão na LOB do estado
    "abbr": "DP",                            # sigla na LOB (ou "")
},
```

**Comandos:**
- Regenerar: `python scripts/build_minuta_comparison.py`
- Testes JS: `node --test src/lib/minutaArticles.test.js` (espera `# fail 0`)

---

### Task 0: Modelo de dados + merge no build (validado com SC e GO)

**Files:**
- Create: `scripts/lob_enrichment.py`
- Modify: `scripts/build_minuta_comparison.py`
- Create (verificação): `scripts/_check_lob_merge.py`

- [ ] **Step 1: Criar `scripts/lob_enrichment.py` com a camada e 2 estados de amostra**

Crie o arquivo com o dict e o acessor. Inclua entradas REAIS de SC e GO (extraídas das
LOBs `Santa Catarina - Organização Básica.md` e `Goiás - Organização Básica (Lei
18.305-2013).md`) para `dp` e `cg` (SC é rico; GO hoje some da coluna LOB de `dp` — valida o
caminho "adicionar estado que só tem LOB"). Transcreva verbatim os trechos reais dessas LOBs
(abra os arquivos e copie fielmente — os textos abaixo são a ESTRUTURA, substitua pelo
verbatim real ao implementar):

```python
"""
lob_enrichment.py — Portal CBM

Camada CURADA da LOB para o comparativo /comparar (coluna "LOB do estado" e
parte "LOB" da coluna compilada). Para cada (organ_key, estado), a finalidade
e/ou os incisos VERBATIM que a Lei de Organização Básica do estado dá ao órgão,
com citação da fonte. Diferente de minuta_enrichment.ENRICHMENT_ORGAN (que é RI):
aqui é só LOB, e admite a finalidade/caput (1 frase) além de incisos.

Consumido por build_minuta_comparison.py. NÃO altera organs_detail nem ENRICHMENT_ORGAN.
"""

# LOB_ENRICHMENT[(organ_key, state_id)] -> entrada verbatim da LOB.
LOB_ENRICHMENT = {
    ("dp", "sc"): {
        "finalidade": "",
        "competencias": [
            # <incisos verbatim do Art. da LOB de SC que trata da Diretoria de Pessoal>
        ],
        "source": "cf. CBMSC, LOB (Lei nº 1.058/2024), Art. N",
        "organName": "Diretoria de Pessoal", "abbr": "DP",
    },
    ("cg", "sc"): {
        "finalidade": "<finalidade verbatim do Comando-Geral/Estado-Maior na LOB de SC>",
        "competencias": [],
        "source": "cf. CBMSC, LOB (Lei nº 1.058/2024), Art. N",
        "organName": "Comando-Geral", "abbr": "CmdoG",
    },
    ("dp", "go"): {
        "finalidade": "<finalidade verbatim da Diretoria/órgão de pessoal na LOB de GO>",
        "competencias": [
            # <incisos verbatim, se a LOB de GO os enumerar>
        ],
        "source": "cf. CBMGO, LOB (Lei nº 18.305/2013), Art. N",
        "organName": "<nome na LOB de GO>", "abbr": "",
    },
    ("cg", "go"): {
        "finalidade": "<finalidade verbatim do Comando-Geral na LOB de GO>",
        "competencias": [],
        "source": "cf. CBMGO, LOB (Lei nº 18.305/2013), Art. N",
        "organName": "Comando-Geral", "abbr": "",
    },
}


def lob_enrich_for(organ_key: str, state_id: str):
    """Entrada curada da LOB para (órgão, estado), ou None."""
    return LOB_ENRICHMENT.get((organ_key, state_id))
```

- [ ] **Step 2: Escrever o script de verificação do merge (falha antes da Task)**

Crie `scripts/_check_lob_merge.py`. Ele importa o build e checa o comportamento do merge
sobre o JSON gerado. Roda DEPOIS do build:

```python
"""Verificação da camada LOB no comparativo (asserções; sem pytest no repo)."""
import json, sys
from pathlib import Path
BASE = Path(__file__).parent.parent
d = json.loads((BASE / "database" / "comparativo_minuta.json").read_text(encoding="utf-8"))
by = {o["key"]: o for o in d["organs"]}

def state(organ_key, sid):
    o = by[organ_key]
    return next((s for s in o["states"] if s["id"] == sid), None)

# 1) Coluna 2 (LOB) de (dp, sc) é curada e não-vazia.
sc_dp = state("dp", "sc"); assert sc_dp, "SC ausente em dp"
assert sc_dp["lobProvenance"] == "curado", f"esperava lobProvenance curado, veio {sc_dp['lobProvenance']}"
lob_atrib = [a for g in (sc_dp.get("lobOrgans") or []) for a in (g.get("atribuicoes") or [])]
assert lob_atrib, "coluna LOB de (dp,sc) vazia"

# 2) GO entra em (cg, go) mesmo sem RI/auto (estado só-LOB).
go_cg = state("cg", "go"); assert go_cg, "GO não foi adicionado em cg via camada LOB"
assert go_cg["provenance"] == "curado"

# 3) Coluna 3 (organs) de um estado que tem LOB+RI inclui itens da LOB.
#    (após os lotes haverá casos claros; aqui ao menos garante que a coluna 3 de (cg,go)
#     traz a finalidade da LOB.)
col3_atrib = [a for g in (go_cg.get("organs") or []) for a in (g.get("atribuicoes") or [])]
assert col3_atrib, "coluna 3 de (cg,go) vazia"

print("OK: camada LOB integrada (col2 curada, estado só-LOB adicionado, col3 com LOB).")
```

Run (antes de implementar o merge): `python scripts/build_minuta_comparison.py && python scripts/_check_lob_merge.py`
Expected: FALHA (AssertionError em SC/GO — a camada ainda não é lida pelo build).

- [ ] **Step 3: Implementar os helpers no build**

Em `scripts/build_minuta_comparison.py`, logo após os imports existentes, adicione o import:

```python
from lob_enrichment import lob_enrich_for, LOB_ENRICHMENT  # noqa: E402
```

E adicione estes helpers (perto de `competencia_organ`, ~linha 84):

```python
def lob_organ_from_entry(entry):
    """Objeto de órgão (formato da matriz) a partir de uma entrada de LOB_ENRICHMENT."""
    items = ([entry["finalidade"]] if entry.get("finalidade") else []) \
            + list(entry.get("competencias") or [])
    return {
        "name": entry.get("organName", ""), "abbreviation": entry.get("abbr", ""),
        "subordinadoA": "", "atribuicoes": items, "desdobramentos": [], "cargos": [],
    }


def _merge_lob_into_organs(organs, lob_org):
    """Anexa o órgão da LOB à coluna 3 sem repetir atribuições idênticas (por texto)."""
    seen = {a for o in organs for a in (o.get("atribuicoes") or [])}
    extra = [a for a in lob_org["atribuicoes"] if a not in seen]
    if extra or not organs:
        organs.append({**lob_org, "atribuicoes": extra or lob_org["atribuicoes"]})
```

- [ ] **Step 4: Implementar `lob_curated_states_for` e o merge em `build()`**

Adicione a função (perto de `auto_states_for`):

```python
def lob_curated_states_for(organ_key, meta):
    """{state_id: {organ, source}} da camada LOB curada para um órgão."""
    out = {}
    for sid in meta:
        if sid == REF_ID:
            continue
        entry = lob_enrich_for(organ_key, sid)
        if entry:
            out[sid] = {"organ": lob_organ_from_entry(entry), "source": entry["source"]}
    return out
```

Em `build()`, substitua o trecho do laço (atualmente):

```python
        curated = curated_states_for(organ_key, dpo_cot, meta)
        auto = auto_states_for(organ_key, set(curated.keys()), meta)
        states = sort_states(list(curated.values()) + list(auto.values()))
        attach_lob_organs(organ_key, states)
```

por:

```python
        curated = curated_states_for(organ_key, dpo_cot, meta)
        auto = auto_states_for(organ_key, set(curated.keys()), meta)
        lob_cur = lob_curated_states_for(organ_key, meta)
        records = {r["id"]: r for r in (list(curated.values()) + list(auto.values()))}
        # Mescla a camada LOB na coluna 3 e garante presença de estados só-LOB.
        for sid, info in lob_cur.items():
            if sid in records:
                _merge_lob_into_organs(records[sid]["organs"], info["organ"])
                if not records[sid].get("sourceLabel"):
                    records[sid]["sourceLabel"] = info["source"]
            else:
                records[sid] = {
                    **meta.get(sid, _fallback_meta(sid)),
                    "provenance": "curado", "sourceLabel": info["source"], "note": None,
                    "organs": [info["organ"]],
                }
        states = sort_states(list(records.values()))
        attach_lob_organs(organ_key, states, lob_cur)
```

- [ ] **Step 5: Atualizar `attach_lob_organs` para usar a camada LOB na coluna 2**

Substitua a assinatura e o corpo atuais de `attach_lob_organs` por:

```python
def attach_lob_organs(organ_key, state_records, lob_cur):
    """Coluna 2 (LOB) de cada estado: usa a camada curada lob_enrichment quando houver;
    senão, mantém o auto-match histórico em organs_detail filtrado a LOB."""
    for rec in state_records:
        sid = rec["id"]
        if sid == REF_ID:
            continue
        if sid in lob_cur:
            rec["lobOrgans"] = [lob_cur[sid]["organ"]]
            rec["lobProvenance"] = "curado"
            continue
        organs = load_organs(sid)
        lobbed = lob_organs(organs)
        ids = auto_match_organ_ids(organ_key, lobbed)
        matched = [extract_organ(lobbed, oid) for oid in ids]
        rec["lobOrgans"] = [m for m in matched if m]
        rec["lobProvenance"] = (
            "curado" if any(lobbed.get(oid, {}).get("source") == "lob" for oid in ids)
            else "automatico"
        )
```

- [ ] **Step 6: Preencher o verbatim real de SC e GO e regenerar**

Abra `Santa Catarina - Organização Básica.md` e `Goiás - Organização Básica (Lei
18.305-2013).md`, localize os artigos do Comando-Geral e da Diretoria de Pessoal (ou
equivalente), e substitua os placeholders `<...>` nas 4 entradas de `lob_enrichment.py` pelo
texto VERBATIM, com o número do artigo correto no `source`. Então:

Run: `python scripts/build_minuta_comparison.py && python scripts/_check_lob_merge.py`
Expected: `OK: camada LOB integrada (...)`.

- [ ] **Step 7: Não-regressão + testes**

Run:
```bash
git status --short database/organs_detail database/comparativo_dpo_cot.json
node --test src/lib/minutaArticles.test.js
```
Expected: primeiro VAZIO (intocados); segundo `# fail 0`.

- [ ] **Step 8: Validação visual (3 colunas)**

Suba o dev server e confira o `/comparar` para o órgão `dp` (estado SC) e `cg` (estado GO):
a coluna 2 deve mostrar o texto da LOB com badge "Curado"; a coluna 3 deve incluir os itens
da LOB. Run: `npm run dev -- --port 5173 --strictPort` e abra http://localhost:5173/comparar.
(Se não puder validar visualmente, registre isso explicitamente.)

- [ ] **Step 9: Commit**

```bash
git add scripts/lob_enrichment.py scripts/build_minuta_comparison.py scripts/_check_lob_merge.py database/comparativo_minuta.json
git commit -m "$(cat <<'EOF'
feat(comparador): camada LOB curada (col 2 LOB pura + col 3 LOB+RI), amostra SC/GO

Nova scripts/lob_enrichment.py + merge no build: coluna 2 usa a LOB curada quando
houver; coluna 3 une LOB + RI; estados so-LOB passam a entrar. organs_detail,
comparativo_dpo_cot e ENRICHMENT_ORGAN intocados.

Co-Authored-By: Claude Opus 4.8 <noreply@anthropic.com>
EOF
)"
```

---

## Prompt de pesquisa (reusar nos lotes 1–5, trocando a lista de estados)

> Pesquisa SOMENTE LEITURA. Para cada estado da lista, abra a LOB correspondente em
> `database/markdown/` (use a variante CONSOLIDADA/mais recente quando houver duas) e extraia,
> para CADA um dos 26 órgãos do RO que a LOB descreva, o conteúdo VERBATIM: a **finalidade/
> caput** (1 frase, transcrita fiel) e/ou os **incisos** enumerados. Mapeie o nome do órgão no
> estado ao `organ_key` do RO pelo mapa de sinônimos do plano (ex.: "Diretoria de Gestão de
> Pessoas" → `dp`). Para cada par (organ_key, estado) com conteúdo, reporte: `organName` (nome
> na LOB), `abbr` (sigla na LOB ou ""), `finalidade` (ou ""), `competencias` (lista verbatim,
> cada item em minúscula inicial, sem o marcador do inciso, sem ponto final), e `source`
> (`cf. CBMxx, LOB (Lei nº …/ano), Art. N`). Critério: só LOB; admite finalidade; nada de RI,
> paráfrase ou invenção; correção de OCR óbvio permitida. Órgão que a LOB não descreve → sem
> entrada (registre "sem equivalente" com o motivo). NÃO edite arquivos; só reporte.
>
> Estados deste lote: <LISTA>

Cada lote, após a pesquisa: o controller integra as entradas em `scripts/lob_enrichment.py`
(aditivo, ordenadas por organ_key depois state_id), regenera, verifica não-regressão e testes,
e commita. Revisão spec + qualidade entre lotes (subagent-driven-development).

---

### Task 1: Lote 1 — LOBs de ac, al, am, ap, ba

**Files:** Modify `scripts/lob_enrichment.py`; Regenera `database/comparativo_minuta.json`; Modify `docs/ENRIQUECIMENTO_MINUTA.md`.

- [ ] **Step 1: Pesquisa** — dispatch subagente com o "Prompt de pesquisa", `<LISTA>` =
  `ac` (Acre - Organização Básica (Lei 2.009-2008 att Lei 4.428-2024).md),
  `al` (Alagoas - Lei de Organização Básica.md),
  `am` (Amazonas - Organização Básica.md),
  `ap` (Amapá - Organização Básica.md),
  `ba` (Bahia - Organização Básica.md).
- [ ] **Step 2: Integrar** — adicione as entradas reportadas a `LOB_ENRICHMENT` em
  `scripts/lob_enrichment.py`, no formato do Contexto compartilhado. Aditivo; não altere
  entradas existentes (SC/GO da Task 0).
- [ ] **Step 3: Documentar** — em `docs/ENRIQUECIMENTO_MINUTA.md`, na seção "Camada LOB —
  /comparar" (criada na Task 6 se ainda não existir; senão append), registre, por estado: Lei,
  nº de órgãos com entrada, e os pares "sem equivalente" com motivo.
- [ ] **Step 4: Regenerar** — `python scripts/build_minuta_comparison.py && python scripts/_check_lob_merge.py`. Expected: `OK`.
- [ ] **Step 5: Não-regressão** —
  ```bash
  git status --short database/organs_detail database/comparativo_dpo_cot.json
  ```
  Expected: VAZIO. E confirme que `git diff scripts/lob_enrichment.py` é puramente aditivo.
- [ ] **Step 6: Testes** — `node --test src/lib/minutaArticles.test.js`. Expected: `# fail 0`.
- [ ] **Step 7: Commit**
  ```bash
  git add scripts/lob_enrichment.py docs/ENRIQUECIMENTO_MINUTA.md database/comparativo_minuta.json
  git commit -m "data(comparador): camada LOB lote 1 (AC, AL, AM, AP, BA)"
  ```
  (última linha `Co-Authored-By: Claude Opus 4.8 <noreply@anthropic.com>`, via heredoc.)

---

### Task 2: Lote 2 — LOBs de ce, df, es, ma, mg

**Files:** Modify `scripts/lob_enrichment.py`; Regenera `database/comparativo_minuta.json`; Modify `docs/ENRIQUECIMENTO_MINUTA.md`.

- [ ] **Step 1: Pesquisa** — `<LISTA>` =
  `ce` (Ceará - Organização Básica (Lei 13.438-2004).md),
  `df` (Distrito Federal - Organização Básica.md),
  `es` (Espírito Santo - Lei de Organização Básica.md),
  `ma` (Maranhão - Organização Básica.md),
  `mg` (Minas Gerais - Organização Básica.md).
- [ ] **Step 2: Integrar** — entradas em `LOB_ENRICHMENT` (aditivo).
- [ ] **Step 3: Documentar** — append na seção "Camada LOB" de `docs/ENRIQUECIMENTO_MINUTA.md`.
- [ ] **Step 4: Regenerar** — `python scripts/build_minuta_comparison.py && python scripts/_check_lob_merge.py`. Expected: `OK`.
- [ ] **Step 5: Não-regressão** — `git status --short database/organs_detail database/comparativo_dpo_cot.json` VAZIO; diff aditivo.
- [ ] **Step 6: Testes** — `node --test src/lib/minutaArticles.test.js` → `# fail 0`.
- [ ] **Step 7: Commit** — `data(comparador): camada LOB lote 2 (CE, DF, ES, MA, MG)` (+ Co-Authored-By).

---

### Task 3: Lote 3 — LOBs de ms, mt, pa, pb, pe

**Files:** Modify `scripts/lob_enrichment.py`; Regenera `database/comparativo_minuta.json`; Modify `docs/ENRIQUECIMENTO_MINUTA.md`.

- [ ] **Step 1: Pesquisa** — `<LISTA>` =
  `ms` (Mato Grosso do Sul - Organização Básica.md),
  `mt` (Mato Grosso - Organização Básica.md),
  `pa` (Pará - Organização Básica.md),
  `pb` (Paraíba - Organização Básica.md),
  `pe` (Pernambuco - Organização Básica (Lei 15.187-2013).md).
- [ ] **Step 2: Integrar** — entradas em `LOB_ENRICHMENT` (aditivo).
- [ ] **Step 3: Documentar** — append em `docs/ENRIQUECIMENTO_MINUTA.md`.
- [ ] **Step 4: Regenerar** — `python scripts/build_minuta_comparison.py && python scripts/_check_lob_merge.py`. Expected: `OK`.
- [ ] **Step 5: Não-regressão** — VAZIO; diff aditivo.
- [ ] **Step 6: Testes** — `# fail 0`.
- [ ] **Step 7: Commit** — `data(comparador): camada LOB lote 3 (MS, MT, PA, PB, PE)` (+ Co-Authored-By).

---

### Task 4: Lote 4 — LOBs de pi, pr, rj, rn, rr

**Files:** Modify `scripts/lob_enrichment.py`; Regenera `database/comparativo_minuta.json`; Modify `docs/ENRIQUECIMENTO_MINUTA.md`.

- [ ] **Step 1: Pesquisa** — `<LISTA>` =
  `pi` (Piauí - Organização Básica (Lei 5.949-2009 alt. Lei 7.772-2022).md),
  `pr` (Paraná - Organização Básica.md),
  `rj` (Rio de Janeiro - Organização Básica.md),
  `rn` (Rio Grande do Norte - Organização Básica.md),
  `rr` (Roraíma - Organização Básica.md).
- [ ] **Step 2: Integrar** — entradas em `LOB_ENRICHMENT` (aditivo).
- [ ] **Step 3: Documentar** — append em `docs/ENRIQUECIMENTO_MINUTA.md`.
- [ ] **Step 4: Regenerar** — `python scripts/build_minuta_comparison.py && python scripts/_check_lob_merge.py`. Expected: `OK`.
- [ ] **Step 5: Não-regressão** — VAZIO; diff aditivo.
- [ ] **Step 6: Testes** — `# fail 0`.
- [ ] **Step 7: Commit** — `data(comparador): camada LOB lote 4 (PI, PR, RJ, RN, RR)` (+ Co-Authored-By).

---

### Task 5: Lote 5 — LOBs de rs, se, sp, to

**Files:** Modify `scripts/lob_enrichment.py`; Regenera `database/comparativo_minuta.json`; Modify `docs/ENRIQUECIMENTO_MINUTA.md`.

- [ ] **Step 1: Pesquisa** — `<LISTA>` =
  `rs` (Rio Grande do Sul - Organização Básica.md),
  `se` (Sergipe - Organização Básica (Lei 8.979-2022).md),
  `sp` (São Paulo - Organização Básica (Lei 616-1974).md),
  `to` (Tocantins - Organização Básica.md).
- [ ] **Step 2: Integrar** — entradas em `LOB_ENRICHMENT` (aditivo).
- [ ] **Step 3: Documentar** — append em `docs/ENRIQUECIMENTO_MINUTA.md`.
- [ ] **Step 4: Regenerar** — `python scripts/build_minuta_comparison.py && python scripts/_check_lob_merge.py`. Expected: `OK`.
- [ ] **Step 5: Não-regressão** — VAZIO; diff aditivo.
- [ ] **Step 6: Testes** — `# fail 0`.
- [ ] **Step 7: Commit** — `data(comparador): camada LOB lote 5 (RS, SE, SP, TO)` (+ Co-Authored-By).

---

### Task 6: Verificação final, frontend e docs

**Files:** Modify `src/pages/MinutaComparator.jsx` (texto), `CLAUDE.md`, `docs/ENRIQUECIMENTO_MINUTA.md`.

- [ ] **Step 1: Cobertura final** — rode:
  ```bash
  python scripts/build_minuta_comparison.py
  python -c "import json; d=json.load(open('database/comparativo_minuta.json',encoding='utf-8')); \
  print('orgaos:', len(d['organs'])); \
  print('estados com col2 curada por orgao:'); \
  [print(' ', o['key'], sum(1 for s in o['states'] if s.get('lobProvenance')=='curado')) for o in d['organs']]"
  ```
  Anote a cobertura curada da coluna LOB por órgão. Órgãos/estados sem LOB equivalente devem
  ter o motivo registrado em `docs/ENRIQUECIMENTO_MINUTA.md`.

- [ ] **Step 2: Reprodutibilidade** — rode o build duas vezes:
  ```bash
  python scripts/build_minuta_comparison.py
  git status --short database/comparativo_minuta.json
  ```
  Expected: VAZIO na 2ª vez.

- [ ] **Step 3: Invariantes globais** —
  ```bash
  git diff master --stat -- database/organs_detail database/comparativo_dpo_cot.json scripts/minuta_enrichment.py
  ```
  Expected: VAZIO (camadas da Frente 2 e detalhamento intocadas).

- [ ] **Step 4: Ajuste textual do frontend** — em `src/pages/MinutaComparator.jsx`, no
  parágrafo de ajuda (linhas ~217-225) e no `StateColHead` (rótulo da coluna compilada,
  ~linha 46), troque "Compilada / todas as fontes curadas" por "LOB + RI" para casar com a
  nova semântica. Exemplo no `StateColHead`:
  ```jsx
  <span className="oc-col-kind">{isLob ? 'LOB' : 'LOB + RI'}</span>
  ```
  E no parágrafo, ajuste a descrição da 3ª visão para "a estrutura enriquecida (LOB + RI)".
  Sem mudança de lógica.

- [ ] **Step 5: Testes pós-frontend** — `node --test src/lib/minutaArticles.test.js` → `# fail 0`.

- [ ] **Step 6: Atualizar `CLAUDE.md`** — na seção do `/comparar`, descreva a nova camada
  `scripts/lob_enrichment.py` (LOB curada por órgão×estado, admite finalidade), que a coluna 2
  passa a ser curada quando há entrada e a coluna 3 é "LOB + RI". Adicione `lob_enrichment.py`
  ao comando de geração se pertinente.

- [ ] **Step 7: Commit**
  ```bash
  git add src/pages/MinutaComparator.jsx CLAUDE.md docs/ENRIQUECIMENTO_MINUTA.md database/comparativo_minuta.json
  git commit -m "docs+ui(comparador): rotulo LOB+RI e doc da camada lob_enrichment"
  ```
  (+ Co-Authored-By via heredoc.)

---

## Self-Review (autor do plano)

**Spec coverage:**
- Camada de dados nova (`lob_enrichment.py`) → Task 0. ✓
- Merge col 2 (LOB curada > auto) → Task 0 Step 5. ✓
- Merge col 3 (LOB + RI, união) + estados só-LOB adicionados → Task 0 Step 4. ✓
- Critério relaxado (finalidade verbatim) → Contexto compartilhado + prompt de pesquisa. ✓
- 26 órgãos × 27 estados → Tasks 1–5 (24 estados) + Task 0 (SC, GO). ✓ (26 estados não-RO
  no total: 2 na Task 0 + 24 nos lotes.)
- organs_detail / dpo_cot / ENRICHMENT_ORGAN intocados → Steps de não-regressão + Task 6 Step 3. ✓
- Frontend "LOB + RI" → Task 6 Step 4. ✓
- Docs (ENRIQUECIMENTO_MINUTA + CLAUDE) → Tasks 1–6. ✓
- Build reproduzível + testes → todos os lotes + Task 6. ✓

**Placeholder scan:** os `<...>` em Task 0 e no formato de entrada são marcadores de dado
verbatim (preenchidos da fonte real ao implementar, como na Frente 2) — não há TODO/TBD de
lógica. O código de build (helpers, merge, attach_lob_organs) está completo e literal.

**Type consistency:** `lob_enrich_for(organ_key, state_id)` e `LOB_ENRICHMENT[(organ_key,
state_id)]` consistentes; `lob_organ_from_entry` produz `{name, abbreviation, subordinadoA,
atribuicoes, desdobramentos, cargos}` (compatível com `extract_organ`/`MATRIX_ROWS`);
`lob_curated_states_for` retorna `{sid: {"organ", "source"}}`, consumido igual em `build()` e
`attach_lob_organs(organ_key, state_records, lob_cur)`. Campos da entrada (`finalidade`,
`competencias`, `source`, `organName`, `abbr`) idênticos no formato, no `lob_enrichment.py` e
no prompt de pesquisa.
