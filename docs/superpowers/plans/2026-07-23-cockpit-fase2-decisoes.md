# Cockpit Fase 2 — aba "Decisões" (leitura) — Plano de Implementação

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Trazer as 36 Decisões CBMRO do vault Obsidian para uma página de LEITURA no portal (uma por trilha), consumindo um JSON gerado por pipeline Python.

**Architecture:** Script Python offline parseia as 36 notas `.md` do vault (fora do repo) → `database/decisoes_curadoria.json` (commitado, compartilhado entre cenários) → página React `DecisoesCuradoria.jsx` com cartões recolhíveis. Lógica pura isolada em `src/lib/decisoes.js`.

**Tech Stack:** Python 3.10+ (venv `.venv-pipeline/`), React/Vite, `node --test`, `lucide-react`.

## Global Constraints

- Python roda pelo venv isolado: `.venv-pipeline/bin/python scripts/<x>.py` (PEP 668).
- Caminho do vault: constante `VAULT_CURADORIA` com default `~/Documents/Obsidian Vault/Codebases/Comparativo-de-cargos-e-funcoes`, sobreponível por env `VAULT_CURADORIA`. Vault/subpasta ausente → erro e saída não-zero; nunca gravar JSON vazio.
- Reconciliação: `notas em disco == parseadas` por trilha; divergência falha o script. Nota sem `organKey`/`themeKey` ou sem `**Questão:**` → falha nomeando o arquivo.
- Verbatim fiel: blockquotes reproduzidos exatamente; defeito de OCR preservado no campo `ocr`.
- `chapterId` derivado: `organ:<organKey>` (ri) / `reg:<themeKey>` (reg) — casamento exato (todas as chaves já conferidas contra os chapter ids reais).
- JSON lido da RAIZ `database/` (compartilhado), via `fetchJson('/database/decisoes_curadoria.json')` — **não** `scenarioDbUrl`.
- Rotas sem `TrilhaRoute` (padrão da Conferência). Menu: label "Decisões" após "Conferência" em cada trilha.
- Só leitura: nenhuma persistência, nenhum join ativo com dispositivo, nenhum tipo redação×estrutural (Fase 3).

---

### Task 1: Pipeline Python — parser + gerador + JSON

**Files:**
- Create: `scripts/build_decisoes_curadoria.py`
- Create: `scripts/test_decisoes_curadoria.py`
- Gera (commitar): `database/decisoes_curadoria.json`

**Interfaces:**
- Produces: `parse_decisao(texto: str, arquivo: str, trilha: str) -> dict` com as chaves
  `id, trilha, key, chapterId, titulo, questao, candidatas[{fonte, verbatim[list[str]], citacao, ocr, leitura}], comparacao[list[str]], ligadas[list[str]], decidido[bool], decisao[str|None]`.
- Produces (arquivo): `database/decisoes_curadoria.json` com `{generated_by, reconciliacao, decisoes[]}`.

- [ ] **Step 1: Escrever o teste que falha** — `scripts/test_decisoes_curadoria.py`

```python
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


if __name__ == "__main__":
    unittest.main()
```

- [ ] **Step 2: Rodar e ver falhar**

Run: `.venv-pipeline/bin/python -m pytest scripts/test_decisoes_curadoria.py -q` (rodar de dentro de `scripts/` OU com `PYTHONPATH=scripts`)
Expected: FAIL — `ModuleNotFoundError: No module named 'build_decisoes_curadoria'`.

- [ ] **Step 3: Escrever `scripts/build_decisoes_curadoria.py`**

```python
"""
build_decisoes_curadoria.py — Portal CBM (cockpit de curadoria, Fase 2)

Lê as 36 notas de Decisão do vault Obsidian (fora do repo) e gera
database/decisoes_curadoria.json (compartilhado entre cenários) — material de LEITURA
para a aba Decisões. Só leitura: não decide nada, não toca a estrutura da minuta.

Rodar: .venv-pipeline/bin/python scripts/build_decisoes_curadoria.py
Valida: cd scripts && ../.venv-pipeline/bin/python -m pytest test_decisoes_curadoria.py -q
"""
import json
import os
import re
import sys
from pathlib import Path

BASE_DIR = Path(__file__).parent.parent
OUT_JSON = BASE_DIR / "database" / "decisoes_curadoria.json"

DEFAULT_VAULT = Path.home() / "Documents" / "Obsidian Vault" / "Codebases" / "Comparativo-de-cargos-e-funcoes"
VAULT_CURADORIA = Path(os.environ.get("VAULT_CURADORIA", str(DEFAULT_VAULT)))

SUBPASTAS = {
    "ri":  "Regimento Interno — Curadoria",
    "reg": "Regulamento — Curadoria",
}

FRONT_RE = re.compile(r"^---\n(.*?)\n---\n", re.DOTALL)


def _frontmatter(texto):
    m = FRONT_RE.match(texto)
    fm = {}
    if m:
        for linha in m.group(1).splitlines():
            if ":" in linha:
                k, v = linha.split(":", 1)
                fm[k.strip()] = v.strip()
    return fm


def _secoes(corpo):
    """Divide o corpo (sem frontmatter) em {titulo_h2: texto} + o texto antes do 1º H2."""
    partes = re.split(r"^## +", corpo, flags=re.MULTILINE)
    intro = partes[0]
    secs = {}
    for p in partes[1:]:
        nome, _, resto = p.partition("\n")
        secs[nome.strip()] = resto
    return intro, secs


def _parse_candidatas(texto):
    """Cada '### Fonte' vira {fonte, verbatim[], citacao, ocr, leitura}."""
    out = []
    for bloco in re.split(r"^### +", texto, flags=re.MULTILINE)[1:]:
        fonte, _, corpo = bloco.partition("\n")
        verbatim, citacao, ocr, leitura = [], None, None, None
        for linha in corpo.splitlines():
            s = linha.rstrip()
            if s.startswith("> "):
                verbatim.append(s[2:])
            elif s.startswith("`cf.") and s.endswith("`"):
                citacao = s.strip("`")
            elif s.startswith("*(") and s.endswith(")*"):
                ocr = s[2:-2]
            elif s.startswith("**Leitura:**"):
                leitura = s[len("**Leitura:**"):].strip()
        out.append({
            "fonte": fonte.strip(), "verbatim": verbatim,
            "citacao": citacao, "ocr": ocr, "leitura": leitura,
        })
    return out


def _bullets(texto):
    return [l[2:].strip() for l in texto.splitlines() if l.startswith("- ")]


def _wikilinks(texto):
    return re.findall(r"\[\[([^\]]+)\]\]", texto)


def parse_decisao(texto, arquivo, trilha):
    fm = _frontmatter(texto)
    key = fm.get("organKey") or fm.get("themeKey")
    if not key:
        raise ValueError(f"{arquivo}: sem organKey/themeKey no frontmatter")
    corpo = FRONT_RE.sub("", texto, count=1)
    intro, secs = _secoes(corpo)

    mtit = re.search(r"^# +(.*)$", intro, flags=re.MULTILINE)
    titulo = mtit.group(1).strip() if mtit else Path(arquivo).stem
    mq = re.search(r"\*\*Questão:\*\*\s*(.+?)(?:\n\n|\Z)", intro, flags=re.DOTALL)
    if not mq:
        raise ValueError(f"{arquivo}: sem **Questão:**")
    questao = " ".join(mq.group(1).split())

    dec_txt = (secs.get("Decisão CBMRO") or "").strip()
    is_placeholder = dec_txt.startswith("_(") or not dec_txt
    decidido = fm.get("decidido", "false").lower() == "true"
    decisao = None if is_placeholder else dec_txt

    return {
        "id": Path(arquivo).stem,
        "trilha": trilha,
        "key": key,
        "chapterId": ("organ:" if trilha == "ri" else "reg:") + key,
        "titulo": titulo,
        "questao": questao,
        "candidatas": _parse_candidatas(secs.get("Redações candidatas", "")),
        "comparacao": _bullets(secs.get("Comparação", "")),
        "ligadas": _wikilinks(secs.get("Ligações", "")),
        "decidido": decidido,
        "decisao": decisao,
    }


def build():
    if not VAULT_CURADORIA.is_dir():
        sys.exit(f"ERRO: vault não encontrado em {VAULT_CURADORIA} (defina VAULT_CURADORIA).")
    decisoes, recon = [], {}
    for trilha, sub in SUBPASTAS.items():
        pasta = VAULT_CURADORIA / sub
        if not pasta.is_dir():
            sys.exit(f"ERRO: subpasta ausente: {pasta}")
        arquivos = sorted(pasta.glob("Decisão — *.md"))
        for p in arquivos:
            decisoes.append(parse_decisao(p.read_text(encoding="utf-8"), p.name, trilha))
        recon[trilha] = {"disco": len(arquivos), "parseadas": len(arquivos)}
        print(f"  ✓ {trilha}: {len(arquivos)} decisões")

    out = {
        "generated_by": "scripts/build_decisoes_curadoria.py",
        "reconciliacao": recon,
        "decisoes": decisoes,
    }
    OUT_JSON.write_text(json.dumps(out, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Gerado: {OUT_JSON} ({len(decisoes)} decisões)")


if __name__ == "__main__":
    build()
```

- [ ] **Step 4: Rodar o teste e ver passar**

Run: `cd scripts && ../.venv-pipeline/bin/python -m pytest test_decisoes_curadoria.py -q`
Expected: `3 passed`.

- [ ] **Step 5: Gerar o JSON real e reconciliar**

Run: `.venv-pipeline/bin/python scripts/build_decisoes_curadoria.py`
Expected: imprime `ri: 9 decisões` e `reg: 27 decisões`, e `Gerado: …/decisoes_curadoria.json (36 decisões)`.
Conferir contagem: `.venv-pipeline/bin/python -c "import json;d=json.load(open('database/decisoes_curadoria.json'));print(len(d['decisoes']), d['reconciliacao'])"` → `36 {'ri': {'disco': 9, 'parseadas': 9}, 'reg': {'disco': 27, 'parseadas': 27}}`.

- [ ] **Step 6: Commit**

```bash
git add scripts/build_decisoes_curadoria.py scripts/test_decisoes_curadoria.py database/decisoes_curadoria.json
git commit -m "feat(decisoes): pipeline lê 36 Decisões do vault -> decisoes_curadoria.json"
```

---

### Task 2: Lógica pura — `src/lib/decisoes.js`

**Files:**
- Create: `src/lib/decisoes.js`
- Create: `src/lib/decisoes.test.js`

**Interfaces:**
- Consumes: o JSON `{decisoes: [{trilha, decidido, ...}]}` da Task 1.
- Produces: `decisoesDaTrilha(dados, trilha) -> array`; `filtrarDecisoes(lista, filtro) -> array` (`filtro` ∈ `'todas'|'pendentes'|'decididas'`); `contarDecisoes(lista) -> {total, decididas, pendentes}`.

- [ ] **Step 1: Escrever o teste que falha** — `src/lib/decisoes.test.js`

```javascript
import { test } from 'node:test'
import assert from 'node:assert/strict'
import { decisoesDaTrilha, filtrarDecisoes, contarDecisoes } from './decisoes.js'

const dados = {
  decisoes: [
    { trilha: 'ri', decidido: true },
    { trilha: 'ri', decidido: false },
    { trilha: 'reg', decidido: false },
  ],
}

test('decisoesDaTrilha filtra por trilha', () => {
  assert.equal(decisoesDaTrilha(dados, 'ri').length, 2)
  assert.equal(decisoesDaTrilha(dados, 'reg').length, 1)
  assert.deepEqual(decisoesDaTrilha(null, 'ri'), [])
})

test('filtrarDecisoes por status', () => {
  const ri = decisoesDaTrilha(dados, 'ri')
  assert.equal(filtrarDecisoes(ri, 'todas').length, 2)
  assert.equal(filtrarDecisoes(ri, 'pendentes').length, 1)
  assert.equal(filtrarDecisoes(ri, 'decididas').length, 1)
})

test('contarDecisoes soma total/decididas/pendentes', () => {
  assert.deepEqual(contarDecisoes(decisoesDaTrilha(dados, 'ri')),
    { total: 2, decididas: 1, pendentes: 1 })
})
```

- [ ] **Step 2: Rodar e ver falhar**

Run: `node --test src/lib/decisoes.test.js`
Expected: FAIL — `Cannot find module './decisoes.js'`.

- [ ] **Step 3: Escrever `src/lib/decisoes.js`**

```javascript
// Lógica pura da aba Decisões (cockpit Fase 2). Sem React, sem fetch — testável isolada.

export function decisoesDaTrilha(dados, trilha) {
  return (dados?.decisoes ?? []).filter(d => d.trilha === trilha)
}

export function filtrarDecisoes(lista, filtro) {
  if (filtro === 'pendentes') return lista.filter(d => !d.decidido)
  if (filtro === 'decididas') return lista.filter(d => d.decidido)
  return lista
}

export function contarDecisoes(lista) {
  const decididas = lista.filter(d => d.decidido).length
  return { total: lista.length, decididas, pendentes: lista.length - decididas }
}
```

- [ ] **Step 4: Rodar o teste e ver passar**

Run: `node --test src/lib/decisoes.test.js`
Expected: `pass 3`.

- [ ] **Step 5: Commit**

```bash
git add src/lib/decisoes.js src/lib/decisoes.test.js
git commit -m "feat(decisoes): lib pura (filtro por trilha/status + contagem)"
```

---

### Task 3: Página — `src/pages/DecisoesCuradoria.jsx` + CSS

**Files:**
- Create: `src/pages/DecisoesCuradoria.jsx`
- Modify: `src/index.css` (append: bloco `.dec-*`)

**Interfaces:**
- Consumes: `decisoesDaTrilha`, `filtrarDecisoes`, `contarDecisoes` (Task 2); `fetchJson` de `src/lib/dataCache.js`; `LoadingState`/`ErrorState` de `src/components/Status.jsx`; `renderFriendlyText` de `src/lib/comparatorRender.jsx`.
- Produces: `export default function DecisoesCuradoria({ trilha })` — usado pela Task 4.

Padrões reais do repo (não inventar): `fetchJson(url)` retorna Promise (lança em erro); `ErrorState({icon, title, hint})`; `LoadingState({label})`; a Conferência usa classes `section-bar`, `section-bar-label`, `section-bar-badge`, `page-body`, `card`, `rg-caput`, `rg-heading`, `rg-source`.

- [ ] **Step 1: Escrever a página** — `src/pages/DecisoesCuradoria.jsx`

```jsx
import { useEffect, useMemo, useState } from 'react'
import { ClipboardList, Check, AlertTriangle, ChevronRight } from 'lucide-react'
import { fetchJson } from '../lib/dataCache.js'
import { LoadingState, ErrorState } from '../components/Status.jsx'
import { renderFriendlyText } from '../lib/comparatorRender.jsx'
import { decisoesDaTrilha, filtrarDecisoes, contarDecisoes } from '../lib/decisoes.js'

const TITULO = { ri: 'Regimento Interno', reg: 'Regulamento Geral' }
const FILTROS = [
  { id: 'todas', label: 'Todas' },
  { id: 'pendentes', label: 'Pendentes' },
  { id: 'decididas', label: 'Decididas' },
]

export default function DecisoesCuradoria({ trilha = 'ri' }) {
  const [dados, setDados] = useState(null)
  const [error, setError] = useState(false)
  const [filtro, setFiltro] = useState('todas')

  useEffect(() => {
    setDados(null); setError(false)
    fetchJson('/database/decisoes_curadoria.json').then(setDados).catch(() => setError(true))
  }, [])

  const daTrilha = useMemo(() => decisoesDaTrilha(dados, trilha), [dados, trilha])
  const contagem = useMemo(() => contarDecisoes(daTrilha), [daTrilha])
  const lista = useMemo(() => filtrarDecisoes(daTrilha, filtro), [daTrilha, filtro])

  if (error) {
    return (
      <ErrorState
        icon={ClipboardList}
        title="Decisões não encontradas"
        hint={<>Execute <code>scripts/build_decisoes_curadoria.py</code>.</>}
      />
    )
  }
  if (!dados) return <LoadingState label="" />

  return (
    <div className="dec">
      <div className="section-bar no-print">
        <div className="section-bar-label">Decisões — {TITULO[trilha]}</div>
        <span className="section-bar-badge">
          <ClipboardList size={13} color="var(--cbm-red-700)" />
          {contagem.decididas} / {contagem.total} decididas
        </span>
      </div>

      <div className="page-body">
        <div className="dec-filtros no-print">
          {FILTROS.map(f => (
            <button
              key={f.id}
              className={`btn btn-ghost${filtro === f.id ? ' active' : ''}`}
              onClick={() => setFiltro(f.id)}
            >
              {f.label}
            </button>
          ))}
        </div>

        {lista.length === 0 ? (
          <div className="card" style={{ padding: 24, textAlign: 'center', color: 'var(--text-muted)' }}>
            Nenhuma decisão neste filtro.
          </div>
        ) : (
          lista.map(d => <DecisaoCard key={d.id} d={d} />)
        )}
      </div>
    </div>
  )
}

function DecisaoCard({ d }) {
  const [abertas, setAbertas] = useState({}) // índice da candidata -> aberta
  const [cmpAberta, setCmpAberta] = useState(false)
  const decidida = d.decidido

  return (
    <div className={`card dec-card${decidida ? ' dec-card-ok' : ''}`} style={{ marginBottom: 14, padding: 16 }}>
      <div className="dec-card-head">
        <h3 className="dec-titulo">{d.titulo}</h3>
        <span className={`dec-selo ${decidida ? 'dec-selo-ok' : 'dec-selo-pend'}`}>
          {decidida ? <><Check size={13} /> Decidida</> : <><AlertTriangle size={13} /> Pendente</>}
        </span>
      </div>
      <p className="dec-questao">{d.questao}</p>

      <div className="dec-candidatas">
        {d.candidatas.map((c, i) => (
          <div className="dec-candidata" key={i}>
            <button className="dec-cand-head" onClick={() => setAbertas(a => ({ ...a, [i]: !a[i] }))}>
              <ChevronRight size={14} className={`dec-chevron${abertas[i] ? ' aberta' : ''}`} />
              <span className="dec-cand-fonte">{c.fonte}</span>
              {c.citacao && <span className="rg-source">{c.citacao}</span>}
            </button>
            {abertas[i] && (
              <div className="dec-cand-corpo">
                {c.verbatim.map((linha, j) => (
                  <p className="rg-caput" key={j}>{renderFriendlyText(linha)}</p>
                ))}
                {c.ocr && <p className="dec-ocr">{c.ocr}</p>}
                {c.leitura && <p className="dec-leitura"><strong>Leitura:</strong> {c.leitura}</p>}
              </div>
            )}
          </div>
        ))}
      </div>

      {d.comparacao.length > 0 && (
        <div className="dec-comparacao">
          <button className="dec-cand-head" onClick={() => setCmpAberta(v => !v)}>
            <ChevronRight size={14} className={`dec-chevron${cmpAberta ? ' aberta' : ''}`} />
            <span className="dec-cand-fonte">Comparação</span>
          </button>
          {cmpAberta && (
            <ul className="dec-cmp-list">
              {d.comparacao.map((b, i) => <li key={i}>{b}</li>)}
            </ul>
          )}
        </div>
      )}

      {decidida && d.decisao && (
        <div className="dec-decisao">
          <div className="rg-heading">Decisão CBMRO</div>
          <p className="rg-caput">{d.decisao}</p>
        </div>
      )}
    </div>
  )
}
```

- [ ] **Step 2: Adicionar o CSS** — append ao fim de `src/index.css`

```css
/* ===== Aba Decisões (cockpit Fase 2) ===== */
.dec-filtros { display: flex; gap: 8px; margin-bottom: 14px; }
.dec-card-head { display: flex; align-items: center; justify-content: space-between; gap: 12px; }
.dec-titulo { font-size: .98rem; margin: 0; color: var(--text); }
.dec-selo { display: inline-flex; align-items: center; gap: 5px; font-size: .74rem; font-weight: 600; padding: 3px 9px; border-radius: 999px; white-space: nowrap; }
.dec-selo-ok { background: #e6f4ea; color: #1b7a3d; }
.dec-selo-pend { background: #fdf1e3; color: #b3600d; }
.dec-card-ok { border-left: 3px solid #1b7a3d; }
.dec-questao { margin: 10px 0 14px; color: var(--text); }
.dec-candidata, .dec-comparacao { border-top: 1px solid var(--border, #e2e6ee); }
.dec-cand-head { display: flex; align-items: center; gap: 8px; width: 100%; background: none; border: 0; padding: 10px 0; cursor: pointer; text-align: left; font: inherit; color: var(--text); }
.dec-cand-fonte { font-weight: 600; }
.dec-chevron { transition: transform .15s; flex: none; }
.dec-chevron.aberta { transform: rotate(90deg); }
.dec-cand-corpo { padding: 0 0 12px 22px; }
.dec-ocr { font-size: .8rem; font-style: italic; color: var(--text-muted); }
.dec-leitura { color: var(--text-muted); }
.dec-cmp-list { margin: 0 0 12px; padding-left: 40px; color: var(--text-muted); }
.dec-decisao { margin-top: 12px; padding-top: 10px; border-top: 1px solid var(--border, #e2e6ee); }
```

- [ ] **Step 3: Build sanity (a página compila; sem teste de render nesta base)**

Run: `npm run build`
Expected: build conclui sem erro (Rollup gera `dist/`), sem referência quebrada a `DecisoesCuradoria` (ainda não roteada — importada na Task 4).

- [ ] **Step 4: Commit**

```bash
git add src/pages/DecisoesCuradoria.jsx src/index.css
git commit -m "feat(decisoes): página de leitura das Decisões (cartões recolhíveis)"
```

---

### Task 4: Rotas + menu — `src/App.jsx`

**Files:**
- Modify: `src/App.jsx` (import; 2 rotas; 2 entradas de menu)

**Interfaces:**
- Consumes: `DecisoesCuradoria` (Task 3).

- [ ] **Step 1: Import** — após a linha `import ConferenciaLinear from './pages/ConferenciaLinear.jsx'` (linha ~25)

```jsx
import DecisoesCuradoria from './pages/DecisoesCuradoria.jsx'
```

- [ ] **Step 2: Entradas de menu** — em `NAV_GROUPS`, logo após cada linha `Conferência`

No bloco Regimento (após `{ to: '/minuta/conferencia', ... }`):
```jsx
      { to: '/minuta/decisoes', icon: ClipboardList, label: 'Decisões' },
```
No bloco Regulamento (após `{ to: '/regulamento/conferencia', ... }`):
```jsx
      { to: '/regulamento/decisoes', icon: ClipboardList, label: 'Decisões' },
```

- [ ] **Step 3: Garantir o ícone importado** — no import de `lucide-react` no topo de `App.jsx`, incluir `ClipboardList` na lista (se ainda não estiver).

Run: `grep -n "ClipboardList" src/App.jsx`
Expected: aparece no import do lucide-react e nas 2 entradas de menu.

- [ ] **Step 4: Rotas** — junto das rotas da Conferência (após `<Route path="/minuta/conferencia" ... />` e `<Route path="/regulamento/conferencia" ... />`), SEM `TrilhaRoute`

```jsx
          <Route path="/minuta/decisoes" element={<DecisoesCuradoria trilha="ri" />} />
          <Route path="/regulamento/decisoes" element={<DecisoesCuradoria trilha="reg" />} />
```

- [ ] **Step 5: Build + suíte completa**

Run: `npm run build && node --test`
Expected: build ok; testes JS todos passam (inclui `decisoes.test.js`).

- [ ] **Step 6: Commit**

```bash
git add src/App.jsx
git commit -m "feat(decisoes): rotas /minuta/decisoes e /regulamento/decisoes + menu"
```

---

## Prova visual (após as 4 tasks — regra do crachá)

Servidor `npm run dev` (5173), Playwright pelo Claude: abrir `/minuta/decisoes` e `/regulamento/decisoes` nos dois cenários (`?cenario=atual` e `?cenario=futura`); screenshot mostrando contador, filtros, um cartão expandido com verbatim, e o selo Decidida/Pendente. Comparar com o protótipo aprovado `scratchpad/proto-conferencia.html`. Entregar link verificado via skill `abrir-app`.

## Auditoria AR-01 (fechar a fase)

Reexecutar as 3 varreduras de `docs/superpowers/auditoria-armadilhas.md`. Específico desta fase: confirmar que cada `organKey`/`themeKey` das 36 notas casa com um chapter id real (`organ:*`/`reg:*`) — já conferido no brainstorming (8 organKeys + 12 themeKeys, todos presentes), reconfirmar após gerar o JSON.

## Self-Review (feito)

- **Cobertura da spec:** pipeline+parser+reconciliação (Task 1), lib pura (Task 2), página com cartões recolhíveis+cenário-independente+verbatim/OCR (Task 3), rotas sem TrilhaRoute + menu (Task 4), prova visual + AR-01 (seções finais). ✓
- **Placeholders:** nenhum — todo passo tem código/comando reais.
- **Consistência de tipos:** `decisoesDaTrilha/filtrarDecisoes/contarDecisoes` idênticos entre Task 2 e Task 3; chaves do dict do parser (Task 1) idênticas às lidas na página (Task 3: `titulo, questao, candidatas{fonte,verbatim,citacao,ocr,leitura}, comparacao, decidido, decisao`). ✓
