# Cockpit de Curadoria — Fase 1: Conferência linear — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) ou superpowers:executing-plans. Steps use checkbox (`- [ ]`) syntax.

**Goal:** Entregar a tela de **conferência linear** — percorrer a minuta (Regimento e Regulamento) dispositivo a dispositivo com as referências dos outros estados ao lado — incluindo o **enriquecimento verbatim do Regimento atual** (reaproveitando o Bloco D da futura via de-para). Sem decisões ainda (Fases 2/3).

**Architecture:** Uma tela `ConferenciaLinear` reusável, parametrizada por trilha (RI/Regulamento), lê a estrutura do cenário via `scenarioDbUrl`, monta a lista linear com `buildArticles` (numeração contínua) e mostra as `alternatives` de cada capítulo/órgão. O Regimento atual ganha `alternatives` por um passo no gerador do atual que copia o Bloco D da futura casando órgão a órgão (de-para), SEM tocar nas competências do RO.

**Tech Stack:** Python 3 (`.venv-pipeline/bin/python`), React/Vite, `node --test`.

## Global Constraints

- Spec: `docs/superpowers/specs/2026-07-22-cockpit-curadoria-conferencia-decisoes-design.md`.
- **Isolamento (armadilha do CLAUDE.md):** ao enriquecer o Regimento atual, escrever SOMENTE o campo `alternatives` de cada órgão. É PROIBIDO tocar `sections`/competências do RO — `alternatives` é campo separado (outros estados, verbatim, rotulado por fonte), como já é na futura.
- **Verbatim absoluto:** os excertos de `alternatives` são copiados como estão da futura (que já é verbatim verificado); defeitos de OCR preservados. Nenhum texto novo inventado.
- Cenário futura intocado: `git diff master -- database/` só pode tocar `database/atual/`.
- `node --test` verde ao final de cada task (115 atuais + novos).
- Rotas de conferência NÃO passam por `TrilhaRoute` (funcionam nos dois cenários).
- Branch nova: `feat/cockpit-fase1-conferencia`.
- De-para do Regimento é PROPOSTA — validada pelo Wândrio em 2026-07-22 (inclui a correção `cob1/cob2 → crbm`, ver AR-01); onde não há equivalente (`emg`, `comissoes`), o órgão fica sem `alternatives` (a tela cai para o automático/estado vazio honesto).
- **Registro de armadilhas:** `docs/superpowers/auditoria-armadilhas.md` (classe AR-01 = casamento semântico errado por semelhança de nome). A REVISÃO de cada task e a auditoria final DEVEM consultar esse arquivo e caçar cada classe listada; toda correção termina com varredura de análogos.

---

### Task 1: Enriquecer o Regimento atual com `alternatives` (Bloco D via de-para)

**Files:**
- Modify: `scripts/build_minuta_structure_atual.py`
- Create: `scripts/test_conferencia_alternatives_atual.py`
- Regenera: `database/atual/minuta_structure.json`

**Interfaces:**
- Consome: `database/minuta_structure.json` (futura — órgãos com `alternatives`), `database/atual/minuta_structure.json` (atual — órgãos com `organKey`).
- Produz: cada capítulo `kind:'organ'` do atual passa a ter `alternatives` (mesma forma da futura: `{uf: {name, abbr, docLabel, excerpts:[{heading,caput,dispositivos,source,match}]}}`) quando houver equivalente no de-para.

- [ ] **Step 1: Escrever o teste (falhando)** — `scripts/test_conferencia_alternatives_atual.py`:

```python
"""Valida o enriquecimento de alternatives no Regimento atual (de-para Bloco D)."""
import json, sys
from pathlib import Path
BASE = Path(__file__).parent.parent
ATU = BASE / "database" / "atual" / "minuta_structure.json"
FUT = BASE / "database" / "minuta_structure.json"

# de-para proposto (atual -> futura); 8 diretos + 11 mapeados; emg/comissoes sem equivalente
DEPARA = {
    "cg":"cg","condeg":"condeg","assessorias":"assessorias","corregedoria":"corregedoria",
    "dp":"dp","deei":"deei","cat":"cat","dlog":"dlog",
    "ajudancia":"ag","gabinete":"gab-cg","cepdec":"depdec","dint":"cint","cpof":"dpof",
    "dcs":"ccs","dinf":"cinf","cob1":"crbm","cob2":"crbm","coa":"boa","gbs":"bbs",
}
def main():
    errs=[]
    atu=json.loads(ATU.read_text(encoding="utf-8"))
    fut=json.loads(FUT.read_text(encoding="utf-8"))
    fut_alt={c.get("organKey"):(c.get("alternatives") or {}) for c in fut["chapters"] if c.get("kind")=="organ"}
    for c in atu["chapters"]:
        if c.get("kind")!="organ": continue
        k=c.get("organKey")
        alt=c.get("alternatives") or {}
        # órgãos com equivalente que TEM Bloco D na futura devem receber alternatives
        fk=DEPARA.get(k)
        if fk and fut_alt.get(fk):
            if not alt:
                errs.append(f"{k}: esperava alternatives (de-para -> {fk}), veio vazio")
            else:
                # verbatim: os excerpts devem ser idênticos aos da futura para a mesma fonte
                for uf, a in alt.items():
                    fa=fut_alt[fk].get(uf)
                    if fa and a.get("excerpts")!=fa.get("excerpts"):
                        errs.append(f"{k}/{uf}: excerpts divergem do Bloco D da futura (deve ser cópia verbatim)")
        # emg/comissoes não podem ganhar alternatives (sem equivalente)
        if k in ("emg","comissoes") and alt:
            errs.append(f"{k}: não deveria ter alternatives (sem equivalente no de-para)")
        # ISOLAMENTO: nenhuma competência do RO pode citar CBM de outro estado
        for s in c.get("sections") or []:
            txt=json.dumps(s, ensure_ascii=False)
            import re
            m=re.search(r"cf\. CBM(?!RO)", txt)
            if m: errs.append(f"{k}: seção do RO cita fonte de outro estado ({m.group(0)}) — vazamento")
    if errs:
        print("FALHOU:"); [print(" -",e) for e in errs[:30]]; sys.exit(1)
    n=sum(1 for c in atu["chapters"] if c.get("kind")=="organ" and (c.get("alternatives") or {}))
    print(f"OK — {n} órgãos do Regimento atual com alternatives (Bloco D reaproveitado), sem vazamento.")
if __name__=="__main__": main()
```

- [ ] **Step 2: Rodar e ver falhar** — `.venv-pipeline/bin/python scripts/test_conferencia_alternatives_atual.py` → FAIL (órgãos sem alternatives).

- [ ] **Step 3: Implementar no gerador** — em `scripts/build_minuta_structure_atual.py`, ao final do build de cada capítulo `organ` (antes de gravar o JSON), acrescentar o enriquecimento. Adicionar perto do topo o de-para e uma função que lê o Bloco D da futura UMA vez:

```python
# --- Enriquecimento de conferência: reaproveita o Bloco D verbatim da futura ---
# (as referências de outros estados independem do cenário do RO). Só o campo
# 'alternatives'; NUNCA as competências do RO. de-para a validar pelo Wândrio.
DEPARA_BLOCO_D = {
    "cg":"cg","condeg":"condeg","assessorias":"assessorias","corregedoria":"corregedoria",
    "dp":"dp","deei":"deei","cat":"cat","dlog":"dlog",
    "ajudancia":"ag","gabinete":"gab-cg","cepdec":"depdec","dint":"cint","cpof":"dpof",
    "dcs":"ccs","dinf":"cinf","cob1":"crbm","cob2":"crbm","coa":"boa","gbs":"bbs",
}
def _bloco_d_futura():
    fut = json.loads((BASE_DIR / "database" / "minuta_structure.json").read_text(encoding="utf-8"))
    return {c.get("organKey"): (c.get("alternatives") or {})
            for c in fut["chapters"] if c.get("kind") == "organ"}
```

E no laço que monta cada capítulo `organ` (após montar `sections`), antes de anexar o capítulo à lista:

```python
    fk = DEPARA_BLOCO_D.get(organ_key)
    alt = bloco_d.get(fk) if fk else None
    if alt:
        chapter["alternatives"] = alt   # cópia verbatim; NÃO tocar em chapter["sections"]
```
(onde `bloco_d = _bloco_d_futura()` é obtido uma vez no início de `build()`.)

- [ ] **Step 4: Regenerar e validar**

```bash
.venv-pipeline/bin/python scripts/build_minuta_structure_atual.py
.venv-pipeline/bin/python scripts/test_conferencia_alternatives_atual.py
git diff master --name-only -- database/ | grep -v "^database/atual/" ; echo "exit=$? (1 = só o atual mudou)"
node --test 2>&1 | grep -E "^ℹ (tests|pass|fail)"
```
Expected: teste OK; nada fora de `database/atual/`; 115/115.

- [ ] **Step 5: Commit**

```bash
git add scripts/build_minuta_structure_atual.py scripts/test_conferencia_alternatives_atual.py database/atual/minuta_structure.json
git commit -m "feat(atual): enriquece o Regimento atual com Bloco D verbatim da futura (de-para, campo alternatives)"
```

### Task 2: Lib pura — lista linear de conferência

**Files:**
- Create: `src/lib/conferencia.js`
- Create: `src/lib/conferencia.test.js`

**Interfaces:**
- Consome: `buildArticles(structure)` de `src/lib/minutaArticles.js`; `chapterIdOf(editId)` de `src/lib/minutaTargets.js`.
- Produz: `buildConferencia(structure)` → `Array<{ dispositivo, chapterId, chapterTitle, alternatives }>` onde `dispositivo` é o item de `buildArticles` (com `number`, `caput`, `incisos`, `editId`) e `alternatives` é o objeto de alternativas do capítulo daquele dispositivo (ou `{}`).

- [ ] **Step 1: Escrever o teste (falhando)** — `src/lib/conferencia.test.js`:

```js
import { test } from 'node:test'
import assert from 'node:assert/strict'
import { buildConferencia } from './conferencia.js'

const struct = {
  chapters: [
    { id: 'reg:tema-a', kind: 'organ', chapterTitle: 'TEMA A',
      alternatives: { se: { name: 'Sergipe', excerpts: [{ caput: 'Art. 1 SE' }] } },
      articles: [{ kind: 'incisos', editId: 'reg:tema-a/mt-art-1', caput: 'Caput A', items: [] }] },
    { id: 'reg:tema-b', kind: 'organ', chapterTitle: 'TEMA B',
      articles: [{ kind: 'incisos', editId: 'reg:tema-b/mt-art-2', caput: 'Caput B', items: [] }] },
  ],
}

test('buildConferencia numera contínuo e anexa alternatives do capítulo', () => {
  const lista = buildConferencia(struct)
  assert.equal(lista.length, 2)
  assert.equal(lista[0].dispositivo.number, 1)
  assert.equal(lista[1].dispositivo.number, 2)                 // contínuo, não reinicia
  assert.equal(lista[0].chapterId, 'reg:tema-a')
  assert.ok(lista[0].alternatives.se)                          // alternatives do capítulo A
  assert.deepEqual(lista[1].alternatives, {})                  // capítulo B sem alternatives
})
```

- [ ] **Step 2: Rodar e ver falhar** — `node --test src/lib/conferencia.test.js` → FAIL (módulo inexistente).

- [ ] **Step 3: Implementar** — `src/lib/conferencia.js`:

```js
import { buildArticles } from './minutaArticles.js'
import { chapterIdOf } from './minutaTargets.js'

// Normaliza o marcador de cenário para casar dispositivo (editId) com capítulo (id).
const semCenario = (id) => String(id ?? '').replace(/^reg:atual:/, 'reg:').replace(/^atual:/, '')

// Lista linear de conferência: cada dispositivo da minuta (numeração contínua) com as
// alternativas (referências de outros estados) do seu capítulo/órgão anexadas.
export function buildConferencia(structure) {
  if (!structure?.chapters) return []
  const altPorCap = new Map(
    structure.chapters.map(c => [semCenario(c.id), c.alternatives ?? {}]),
  )
  return buildArticles(structure).map(dispositivo => {
    const chapterId = chapterIdOf(dispositivo.editId)
    const cap = structure.chapters.find(c => semCenario(c.id) === semCenario(chapterId))
    return {
      dispositivo,
      chapterId,
      chapterTitle: cap?.chapterTitle ?? null,
      alternatives: altPorCap.get(semCenario(chapterId)) ?? {},
    }
  })
}
```

- [ ] **Step 4: Rodar e ver passar** — `node --test src/lib/conferencia.test.js` → PASS.

- [ ] **Step 5: Commit**

```bash
git add src/lib/conferencia.js src/lib/conferencia.test.js
git commit -m "feat(conferencia): lib pura buildConferencia (lista linear + alternatives por capítulo)"
```

### Task 3: Tela ConferenciaLinear + rotas + menu

**Files:**
- Create: `src/pages/ConferenciaLinear.jsx`
- Modify: `src/App.jsx` (import, 2 rotas, 2 entradas de menu em NAV_GROUPS)

**Interfaces:**
- Consome: `buildConferencia(structure)` (Task 2); `useScenario()` → `{ cenario }`; `scenarioDbUrl(cenario, arquivo)`; `fetchJson`; `LoadingState/ErrorState`.
- Produz: rotas `/minuta/conferencia` e `/regulamento/conferencia`; a tela aceita prop `trilha` `'ri'|'reg'` que define o arquivo de estrutura (`minuta_structure.json` | `regulamento_structure.json`).

- [ ] **Step 1: Criar o componente** — `src/pages/ConferenciaLinear.jsx`. Seguir o PADRÃO visual e de carregamento de `src/pages/RegulamentoComparator.jsx` (mesmo esqueleto: `useScenario`, `fetchJson(scenarioDbUrl(...))` com `cenario` nas dependências e `setData(null)` no início; `LoadingState/ErrorState`). Estrutura do componente:

```jsx
import { useEffect, useMemo, useState } from 'react'
import { useScenario } from '../context/ScenarioContext'
import { scenarioDbUrl } from '../lib/scenario.js'
import { fetchJson } from '../lib/dataCache.js'
import { LoadingState, ErrorState } from '../components/Status.jsx'
import { buildConferencia } from '../lib/conferencia.js'
import { articleLabel, romanize } from '../lib/minutaArticles.js'

const ARQ = { ri: 'minuta_structure.json', reg: 'regulamento_structure.json' }

export default function ConferenciaLinear({ trilha = 'ri' }) {
  const { cenario } = useScenario()
  const [data, setData] = useState(null)
  const [error, setError] = useState(false)
  const [status, setStatus] = useState({})   // editId+idx -> 'ok'|'div' (local, Fase 1)
  const [ufSel, setUfSel] = useState({})      // chapterId -> uf selecionada

  useEffect(() => {
    setData(null); setError(false)
    fetchJson(scenarioDbUrl(cenario, ARQ[trilha])).then(setData).catch(() => setError(true))
  }, [cenario, trilha])

  const lista = useMemo(() => (data ? buildConferencia(data) : []), [data])
  const feitos = useMemo(() => lista.filter((l, i) => status[i]).length, [status, lista])

  if (error) return <ErrorState label="Não foi possível carregar a estrutura." />
  if (!data) return <LoadingState label="" />

  return (
    <div className="conf">
      {/* cabeçalho + barra de progresso (feitos / lista.length) */}
      {/* para cada item de `lista`: cartão 2 colunas:
          esquerda = dispositivo (articleLabel(l.dispositivo) + caput + incisos)
          direita  = chips das UFs de l.alternatives + trechos da UF selecionada,
                     com etiqueta 'exata'/'auto' vinda de cada excerpt.match
          controles locais: ✓ Confere / ⚠ Divergente (setStatus por índice) */}
    </div>
  )
}
```
Detalhes de renderização (rótulo do dispositivo, incisos, chips, etiquetas exata/auto) devem seguir os componentes existentes `RegulamentoComparator.jsx` (função de rótulo `articleLabel`, badges) — reusar as classes CSS existentes; no máximo 1-2 classes novas sob prefixo `.conf` em `src/index.css` se necessário. NÃO persistir status (Fase 3 fará isso).

- [ ] **Step 2: Registrar rotas e menu** — em `src/App.jsx`:

Import junto dos outros imports de página:
```jsx
import ConferenciaLinear from './pages/ConferenciaLinear.jsx'
```
Rotas (junto das outras de cada trilha; SEM TrilhaRoute):
```jsx
<Route path="/minuta/conferencia" element={<ConferenciaLinear trilha="ri" />} />
<Route path="/regulamento/conferencia" element={<ConferenciaLinear trilha="reg" />} />
```
Menu — em `NAV_GROUPS`, no grupo do Regimento (após `/minuta/subsidio`) e no do Regulamento (após `/regulamento/subsidio`):
```jsx
{ to: '/minuta/conferencia', icon: GitCompare, label: 'Conferência' },
```
```jsx
{ to: '/regulamento/conferencia', icon: GitCompare, label: 'Conferência' },
```
(usar um ícone já importado de `lucide-react`; se preferir distinguir do Subsídio, importar `ListChecks` e usá-lo.)

- [ ] **Step 3: Suíte + smoke** — `node --test` completo (116, 0 fail). Subir `npm run dev`; `curl` 200 em `/minuta/conferencia` e `/regulamento/conferencia`; conferir no console 0 erros.

- [ ] **Step 4: Commit**

```bash
git add src/pages/ConferenciaLinear.jsx src/App.jsx src/index.css
git commit -m "feat(conferencia): tela de conferência linear no menu (Regimento e Regulamento, 2 cenários)"
```

### Task 4: Prova visual + documentação

**Files:**
- Modify: `CLAUDE.md` (citar a tela de Conferência e o de-para do Bloco D no atual)
- Modify: `.claude/PENDENCIAS.md` (Fase 1 concluída; registrar "validar de-para" e "Fases 2/3 pendentes")

- [ ] **Step 1: Prova visual (Playwright, login real do Wândrio).** Com `npm run dev` no ar e sessão logada:
  - `/minuta/conferencia?cenario=atual` — Regimento com referências **verbatim** (etiqueta `exata`) nos órgãos do de-para; screenshot.
  - `/regulamento/conferencia?cenario=atual` — Regulamento com referências verbatim; screenshot.
  - `/minuta/conferencia?cenario=futura` — Regimento futura (referências do Bloco D original); screenshot.
  - Abrir os screenshots no Preview (`open`).
- [ ] **Step 2: Preservação.** `git diff master --stat -- database/ | grep -v atual` vazio; colar no relatório.
- [ ] **Step 3: Docs + commit.** Atualizar CLAUDE.md (seção Cenários LOB: nova tela de Conferência; o Regimento atual reaproveita o Bloco D da futura via de-para em `build_minuta_structure_atual.py`) e PENDENCIAS. Commit:
```bash
git add CLAUDE.md .claude/PENDENCIAS.md
git commit -m "docs: tela de Conferência linear (Fase 1 do cockpit de curadoria)"
```
