# Minuta Operacional Hierárquica — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Reformular a geração da minuta do Regimento Interno do CBMRO para produzir um regimento único e hierárquico cobrindo toda a cadeia operacional (do topo — DPO/COT/DOE — até a menor fração — Companhia/GBM), com atribuições por função, RO verbatim + enriquecimento curado do CBMAL rotulado por fonte.

**Architecture:** Pipeline Python offline gera `database/minuta_structure.json` no novo formato hierárquico (capítulos por órgão, seções por função, itens `{text, source}`). Um módulo curado `scripts/minuta_enrichment.py` fornece competências verbatim do RI do CBMAL para os níveis onde o RO é raso. A lib pura `src/lib/minutaArticles.js` articula a hierarquia (Título → Capítulo → Seção → artigos/incisos) e o `MinutaWizard.jsx` navega a árvore e exporta `.docx`.

**Tech Stack:** Python 3 (pypdf-era scripts, stdlib only), React 18 + Vite, `docx` (npm), `node:test` para testes unitários da lib pura.

**Spec:** `docs/superpowers/specs/2026-06-18-minuta-operacional-hierarquica-design.md`

---

## File Structure

- **Modify** `src/lib/minutaArticles.js` — `buildArticles` passa a consumir `{chapters:[...]}` com capítulos `prose` | `incisos` | `organ` (com `sections[]`); incisos viram `{text, source}`; numeração de artigos contínua + numeração romana de capítulos e de seções (reset por capítulo).
- **Modify** `src/lib/minutaArticles.test.js` — novos casos para a articulação hierárquica.
- **Create** `scripts/minuta_enrichment.py` — seed curado do CBMAL (Arts. 107, 114, 115) + mapeamento `(organ_key, token) → [{text, source}]`.
- **Modify** `scripts/build_minuta_structure.py` — reescrita: percorre a cadeia operacional do `ro.json` na ordem de subordinação e emite o JSON hierárquico, mesclando enriquecimento.
- **Modify** `src/pages/MinutaWizard.jsx` — navegação pela árvore de órgãos, prévia ao vivo, badges de fonte, exportação `.docx` com Título/Capítulo/Seção.
- **Regenerate** `database/minuta_structure.json` (saída do script; não editar à mão).

---

## Task 1: Lib pura — articulação hierárquica (`minutaArticles.js`)

**Files:**
- Modify: `src/lib/minutaArticles.js`
- Test: `src/lib/minutaArticles.test.js`

- [ ] **Step 1: Reescrever os testes para o modelo hierárquico**

Substituir o bloco de `buildArticles` em `src/lib/minutaArticles.test.js` (linhas 30–79, a partir de `import { buildArticles }`) por:

```js
import { buildArticles } from './minutaArticles.js'

const STRUCTURE = {
  chapters: [
    {
      id: 'preliminares', kind: 'prose', chapterTitle: 'DAS DISPOSIÇÕES PRELIMINARES',
      editId: 'preliminares',
      proposedText: 'Primeiro artigo do objeto.\nSegundo artigo da base legal.',
    },
    {
      id: 'estrutura', kind: 'incisos', chapterTitle: 'DA ESTRUTURA ORGANIZACIONAL',
      editId: 'estrutura', caput: 'A estrutura operacional compõe-se dos órgãos:',
      items: [{ text: 'a DPO', source: 'ro' }, { text: 'o COT', source: 'ro' }],
    },
    {
      id: 'organ:dpo', kind: 'organ', chapterTitle: 'DA DIRETORIA DE PLANEJAMENTO OPERACIONAL (DPO)',
      organKey: 'dpo', label: 'Diretoria de Planejamento Operacional', abbr: 'DPO',
      sections: [
        {
          id: 'competencia', kind: 'incisos', sectionTitle: 'Da Competência',
          editId: 'organ:dpo/competencia', caput: 'Compete à DPO:',
          items: [
            { text: 'planejar as operações', source: 'ro' },
            { text: 'fiscalizar a instrução', source: 'cf. CBMAL, RI, Art. 115, VII' },
          ],
        },
        {
          id: 'cargo:diretor', kind: 'incisos', sectionTitle: 'Das Atribuições do Diretor',
          editId: 'organ:dpo/cargo:diretor', caput: 'Ao Diretor compete:',
          items: [{ text: 'dirigir a DPO', source: 'ro' }],
        },
      ],
    },
  ],
}

test('buildArticles numera artigos continuamente atravessando capítulos', () => {
  const arts = buildArticles(STRUCTURE, {})
  assert.deepEqual(arts.map(a => a.number), [1, 2, 3, 4])
})

test('buildArticles marca capítulo no 1º artigo e numera capítulos em sequência', () => {
  const arts = buildArticles(STRUCTURE, {})
  assert.equal(arts[0].chapterTitle, 'DAS DISPOSIÇÕES PRELIMINARES')
  assert.equal(arts[0].chapterNumber, 1)
  assert.equal(arts[1].chapterTitle, null)            // mesmo capítulo
  assert.equal(arts[2].chapterTitle, 'DA ESTRUTURA ORGANIZACIONAL')
  assert.equal(arts[2].chapterNumber, 2)
  assert.equal(arts[3].chapterNumber, 3)              // capítulo do órgão DPO
})

test('buildArticles numera seções por capítulo e marca no 1º artigo da seção', () => {
  const arts = buildArticles(STRUCTURE, {})
  // arts[3] = 1º artigo do capítulo do órgão = 1ª seção (Competência)
  assert.equal(arts[3].sectionNumber, 1)
  assert.equal(arts[3].sectionTitle, 'Da Competência')
})

test('buildArticles preserva a fonte de cada inciso e normaliza o texto', () => {
  const arts = buildArticles(STRUCTURE, {})
  assert.deepEqual(arts[3].incisos, [
    { text: 'planejar as operações; e', source: 'ro' },
    { text: 'fiscalizar a instrução.', source: 'cf. CBMAL, RI, Art. 115, VII' },
  ])
})

test('buildArticles articula prose como um artigo por linha', () => {
  const arts = buildArticles(STRUCTURE, {})
  assert.equal(arts[0].caput, 'Primeiro artigo do objeto.')
  assert.deepEqual(arts[0].incisos, [])
  assert.equal(arts[1].caput, 'Segundo artigo da base legal.')
})

test('buildArticles usa edits (texto) no lugar dos itens, com source nulo', () => {
  const arts = buildArticles(STRUCTURE, { 'organ:dpo/cargo:diretor': 'item editado\noutro item' })
  const diretor = arts.find(a => a.caput === 'Ao Diretor compete:')
  assert.deepEqual(diretor.incisos, [
    { text: 'item editado; e', source: null },
    { text: 'outro item.', source: null },
  ])
})
```

- [ ] **Step 2: Rodar os testes para confirmar que falham**

Run: `node --test src/lib/minutaArticles.test.js`
Expected: FAIL — os novos testes quebram porque `buildArticles` ainda usa o modelo antigo de `organData.sections`.

- [ ] **Step 3: Reescrever `buildArticles` em `src/lib/minutaArticles.js`**

Manter `articleLabel`, `ROMAN_MAP`, `romanize`, `normalizeInciso` exatamente como estão (linhas 1–33). Substituir a função `buildArticles` (linhas 35–91) por:

```js
// Articula a estrutura hierárquica: chapters[] (prose | incisos | organ).
// Numeração de artigos contínua; capítulos e seções em romano (seção reseta por capítulo).
// edits[editId] (string) sobrepõe o texto de um nó-folha; ao editar, a fonte vira null.
export function buildArticles(structure, edits = {}) {
  const articles = []
  let articleCounter = 0
  let chapterCounter = 0

  for (const chapter of structure.chapters) {
    let firstOfChapter = true
    let sectionCounter = 0

    const emitLeaf = (leaf, isSection) => {
      let firstOfSection = true

      const pushArticle = (caput, incisos) => {
        articleCounter += 1
        const art = {
          number: articleCounter, caput, incisos,
          chapterNumber: null, chapterTitle: null,
          sectionNumber: null, sectionTitle: null,
        }
        if (firstOfChapter) {
          chapterCounter += 1
          art.chapterNumber = chapterCounter
          art.chapterTitle = chapter.chapterTitle ?? null
          firstOfChapter = false
        }
        if (isSection && firstOfSection) {
          sectionCounter += 1
          art.sectionNumber = sectionCounter
          art.sectionTitle = leaf.sectionTitle ?? null
          firstOfSection = false
        }
        articles.push(art)
      }

      if (leaf.kind === 'prose') {
        const text = edits[leaf.editId] ?? leaf.proposedText ?? ''
        for (const line of text.split('\n')) {
          const c = line.trim()
          if (c) pushArticle(c, [])
        }
      } else if (leaf.kind === 'incisos') {
        const edited = edits[leaf.editId]
        let items
        if (edited != null) {
          items = edited.split('\n').map(l => l.trim()).filter(Boolean)
            .map(t => ({ text: t, source: null }))
        } else {
          items = (leaf.items ?? []).filter(it => (it.text ?? '').trim())
        }
        const incisos = items.map((it, i) => ({
          text: normalizeInciso(it.text, i, items.length),
          source: it.source ?? null,
        }))
        if (incisos.length || !isSection) {
          pushArticle(leaf.caput ?? '', incisos)
        }
      }
    }

    if (chapter.kind === 'organ') {
      for (const section of chapter.sections) emitLeaf(section, true)
    } else {
      emitLeaf(chapter, false)
    }
  }

  return articles
}
```

- [ ] **Step 4: Rodar os testes para confirmar que passam**

Run: `node --test src/lib/minutaArticles.test.js`
Expected: PASS — todos os testes (incluindo `articleLabel`/`romanize`/`normalizeInciso`, intocados).

- [ ] **Step 5: Commit**

```bash
git add src/lib/minutaArticles.js src/lib/minutaArticles.test.js
git commit -m "feat: articulação hierárquica (capítulo/seção) com itens {text,source}"
```

---

## Task 2: Módulo de enriquecimento curado (`minuta_enrichment.py`)

**Files:**
- Create: `scripts/minuta_enrichment.py`

- [ ] **Step 1: Criar o módulo com o seed verbatim do CBMAL**

Criar `scripts/minuta_enrichment.py` com o conteúdo abaixo. Os textos são transcritos VERBATIM do RI do CBMAL (`database/markdown/Alagoas - Regimento Interno.md`): Art. 107 (linhas 3332–3425), Art. 114 (linhas 3650–3696), Art. 115 (linhas 3701–3722).

```python
"""
minuta_enrichment.py — Portal CBM

Enriquecimento CURADO de competências por função operacional, extraído VERBATIM
de regimentos internos de outros CBMs, para níveis onde o detalhamento do CBMRO
(ro.json) é raso. Cada item carrega a citação da fonte.

Consumido apenas por build_minuta_structure.py. NÃO altera ro.json.

Chave: (organ_key, token_da_funcao) -> list[{"text", "source"}]
  token_da_funcao normaliza o nome do cargo: 'comandante', 'adjunto',
  'subcomandante', 'diretor', 'coordenador', 'comandante-de-companhia'.

Seed atual: cadeia de comando operacional a partir do CBMAL. Expansível
(PR/PA/MT/ES) adicionando novas entradas.
"""

# ── CBMAL, RI, Art. 107 — Comandante Operacional de Bombeiro (≈ Comandante Regional) ──
_AL_ART_107 = [
    "planejar, coordenar e fiscalizar as ações operacionais e administrativas no âmbito de sua competência",
    "manter o registro dos principais pontos de riscos existentes nas áreas de atuação, desenvolvendo planos setoriais para protegê-las",
    "controlar e fiscalizar as condições e nível de adestramento da tropa sob sua responsabilidade, elaborando e fiscalizando o fiel cumprimento das notas de serviço, notas de instrução e planos operacionais",
    "planejar, coordenar e fiscalizar a manutenção do material e equipamento, e manter registros dos bens móveis que estiverem sob sua responsabilidade",
    "manter o registro estatístico das ocorrências verificadas nas áreas de atuação das Unidades Operacionais (UOp) e Subunidades subordinadas, e realizar estudos para o aperfeiçoamento da prevenção e eficácia do atendimento nas ocorrências",
    "planejar, coordenar e fiscalizar o cumprimento da legislação referente à prevenção de incêndio",
    "manter, em perfeito funcionamento, o serviço de comunicações das respectivas Unidades e Subunidades, através do Centro de Operações e Comunicações (COC)",
    "planejar, coordenar, fiscalizar e executar a movimentação do pessoal lotado no Comando Operacional de Bombeiros",
    "adotar medidas que visem a informatização e a agilização das ações administrativas e operacionais das diversas UOp e Subunidades sob seu comando",
    "controlar e fiscalizar a carga de bens patrimoniais que estiverem sob sua responsabilidade",
    "elaborar o Regimento Interno do Comando Operacional de Bombeiros, remetendo-o ao Comandante Geral para aprovação",
    "analisar, aprovar e ou modificar, em comum acordo com os Comandantes das Unidades Operacionais e o Subcomandante Geral, as Normas Gerais de Ações das diversas UOp e Subunidades, remetendo as propostas ao Comandante Geral para aprovação",
    "encaminhar ao Comandante Geral os Regimentos Internos das UOp e Subunidades subordinadas",
    "cumprir e fazer cumprir as normas regulamentares de prevenção e proteção contra incêndio, pânico, salvamento e resgate",
    "controlar, fiscalizar e exigir o cumprimento das atividades de instrução das UOp e Subunidades subordinadas",
    "praticar atos administrativos necessários ao perfeito funcionamento das atividades operacionais",
    "comunicar, de imediato, ao Comandante Geral fatos graves que ocorram nas áreas de suas UOp e Subunidades subordinadas",
    "presidir solenidades de passagem de comando de suas UOp e Subunidades, quando não presentes o Comandante ou o Subcomandante Gerais",
    "controlar e zelar pela conservação dos bens móveis e imóveis sob sua responsabilidade",
    "delegar competência aos comandantes de UOp e Subunidades",
    "manter contato com as demais organizações da Corporação ou com autoridades e ou órgãos externos, visando um melhor desempenho de suas atividades",
    "movimentar oficiais e praças entre as UOp e Subunidades, com prévio conhecimento do Comandante Geral",
    "designar comissões para inventariar bens de bombeiros militares desertores, falecidos ou desaparecidos nas áreas de competência das respectivas UOp e Subunidades",
    "exercer outras atribuições que lhe forem determinadas pelo Comandante Geral",
    "propor ao Conselho de Políticas Estratégicas normas, instruções técnicas e procedimentos operacionais para o aprimoramento das atividades da Corporação",
]

# ── CBMAL, RI, Art. 114 — Comandante de Grupamento (≈ Comandante de Batalhão) ──
_AL_ART_114 = [
    "dirigir, cumprir e fazer cumprir as atividades relacionadas à prevenção, combate a incêndios e salvamento em altura e terrestre na sua área de atuação",
    "praticar os atos administrativos necessários ao perfeito funcionamento da Unidade e de suas subunidades",
    "manter a tropa permanentemente adestrada e pronta para o emprego",
    "comandar diretamente as atividades operacionais que envolvam mais de uma operação de socorro bombeiro militar na área de atuação das subunidades",
    "desenvolver o espírito de iniciativa e camaradagem de seus subordinados",
    "comunicar imediatamente à autoridade superior qualquer fato grave ocorrido em sua área de atuação, solicitando intervenção nos casos que exijam a participação de outros órgãos",
    "controlar e zelar pela conservação e manutenção dos bens móveis e imóveis sob sua responsabilidade",
    "providenciar a manutenção dos bens patrimoniais sob sua guarda",
    "elaborar e submeter à aprovação do escalão superior as Normas Gerais de Ação dos órgãos da Unidade",
    "movimentar os oficiais e praças no âmbito das respectivas subunidades",
    "controlar e fiscalizar a execução, no âmbito das respectivas subunidades operacionais, dos planos e ordens superiores",
    "elaborar e manter atualizado o quadro estatístico de ocorrências operacionais de suas subunidades",
    "executar atos administrativos que lhe competirem, como integrante do sistema de administração de pessoal e material",
    "instaurar sindicância",
    "exercer outros encargos que lhe forem atribuídos pelo Comandante Geral ou previstos em leis e regulamentos vigentes",
]

# ── CBMAL, RI, Art. 115 — Subcomandante de Unidade Operacional (≈ Adjunto de unidade) ──
_AL_ART_115 = [
    "assessorar o seu Comandante em todas as suas atribuições",
    "tomar as providências necessárias ao fiel cumprimento das ordens do seu Comandante",
    "fiscalizar e orientar os trabalhos dos órgãos da Unidade",
    "fiscalizar os serviços de escala da Unidade",
    "responder pelo Comandante nos seus impedimentos",
    "assinar, por delegação do respectivo comandante, os atos administrativos que não forem de exclusividade daquela autoridade e sejam compatíveis com as normas vigentes",
    "fiscalizar e controlar a instrução da Unidade",
    "responsabilizar-se pela carga da Unidade",
    "exercer o controle disciplinar dos integrantes da Unidade",
]


def _tag(items, source):
    return [{"text": t, "source": source} for t in items]


# Mapeamento (organ_key, token) -> itens enriquecidos rotulados.
ENRICHMENT = {
    ("crbm", "comandante"):  _tag(_AL_ART_107, "cf. CBMAL, RI, Art. 107"),
    ("crbm", "adjunto"):     _tag(_AL_ART_115, "cf. CBMAL, RI, Art. 115"),
    ("bbm",  "comandante"):  _tag(_AL_ART_114, "cf. CBMAL, RI, Art. 114"),
    ("cibm", "comandante"):  _tag(_AL_ART_114, "cf. CBMAL, RI, Art. 114"),
    ("bbs",  "comandante"):  _tag(_AL_ART_114, "cf. CBMAL, RI, Art. 114"),
    ("bifea","comandante"):  _tag(_AL_ART_114, "cf. CBMAL, RI, Art. 114"),
    ("boa",  "comandante"):  _tag(_AL_ART_114, "cf. CBMAL, RI, Art. 114"),
}


def function_token(cargo_name: str) -> str:
    """Reduz o nome de um cargo a um token de função para casar com ENRICHMENT."""
    n = (cargo_name or "").lower()
    if "companhia" in n:
        return "comandante-de-companhia"
    if "subcomandante" in n:
        return "subcomandante"
    if "adjunto" in n:
        return "adjunto"
    if "coordenador" in n:
        return "coordenador"
    if "diretor" in n:
        return "diretor"
    if "comandante" in n:
        return "comandante"
    if "chefe" in n:
        return "chefe"
    return n.strip()


def enrich_for(organ_key: str, cargo_name: str):
    """Itens de enriquecimento [{text, source}] para uma função; [] se não houver."""
    return list(ENRICHMENT.get((organ_key, function_token(cargo_name)), []))
```

- [ ] **Step 2: Verificar que o módulo importa e o mapeamento responde**

Run:
```bash
python -c "import sys; sys.path.insert(0,'scripts'); import minuta_enrichment as m; print(len(m.enrich_for('bbm','Comandante do BBM')), m.function_token('Comandante de Companhia de Bombeiros Militar'), len(m.enrich_for('dpo','Diretor de Planejamento Operacional')))"
```
Expected: `15 comandante-de-companhia 0` (BBM-comandante tem 15 itens do Art. 114; Companhia tem token próprio sem seed; DPO-Diretor sem enriquecimento).

- [ ] **Step 3: Commit**

```bash
git add scripts/minuta_enrichment.py
git commit -m "feat: módulo de enriquecimento curado (seed CBMAL Arts. 107/114/115)"
```

---

## Task 3: Reescrever o gerador (`build_minuta_structure.py`)

**Files:**
- Modify: `scripts/build_minuta_structure.py` (reescrita completa)
- Input: `database/organs_detail/ro.json`, `database/comparativo_dpo_cot.json`, `scripts/minuta_enrichment.py`
- Output: `database/minuta_structure.json`

- [ ] **Step 1: Substituir o conteúdo de `scripts/build_minuta_structure.py`**

Substituir o arquivo inteiro por:

```python
"""
build_minuta_structure.py — Portal CBM

Gera database/minuta_structure.json: minuta ARTICULADA e HIERÁRQUICA do Regimento
Interno da estrutura OPERACIONAL do CBMRO — do topo (DPO/COT/DOE) à menor fração
(Companhia/GBM). Um capítulo por órgão; uma seção por função (cargo).

Fontes:
  - database/organs_detail/ro.json        (estrutura + competências RO verbatim)
  - scripts/minuta_enrichment.py          (competências curadas de outros CBMs, rotuladas)

Saída: database/minuta_structure.json
Rodar: python scripts/build_minuta_structure.py
"""

import json
import re
import sys
import unicodedata
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from minuta_enrichment import enrich_for  # noqa: E402

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

BASE_DIR = Path(__file__).parent.parent
RO_JSON  = BASE_DIR / "database" / "organs_detail" / "ro.json"
OUT_JSON = BASE_DIR / "database" / "minuta_structure.json"

TITLE = "DO REGIMENTO INTERNO DA ESTRUTURA OPERACIONAL DO CBMRO"

# Ordem dos capítulos = ordem de subordinação (topo → menor fração).
# (organ_key, CHAPTER_TITLE, artigo_definido, "de"-contração)
ORGAN_ORDER = [
    ("dpo",   "DA DIRETORIA DE PLANEJAMENTO OPERACIONAL (DPO)",          "A",  "da"),
    ("cot",   "DO COMANDO DE OPERAÇÕES TÉCNICAS (COT)",                  "O",  "do"),
    ("doe",   "DA DIRETORIA OPERACIONAL ESPECIALIZADA (DOE)",            "A",  "da"),
    ("crbm",  "DOS COMANDOS REGIONAIS DE BOMBEIRO MILITAR (CRBM)",       "O",  "do"),
    ("bbm",   "DO BATALHÃO DE BOMBEIROS MILITAR (BBM)",                  "O",  "do"),
    ("cibm",  "DA COMPANHIA INDEPENDENTE DE BOMBEIROS MILITAR (CIBM)",   "A",  "da"),
    ("gbm",   "DO GRUPO DE BOMBEIROS MILITAR (GBM)",                     "O",  "do"),
    ("bbs",   "DO BATALHÃO DE BUSCA E SALVAMENTO (BBS)",                 "O",  "do"),
    ("bifea", "DO BATALHÃO DE INCÊNDIO FLORESTAL E EMERGÊNCIAS AMBIENTAIS (BIFEA)", "O", "do"),
    ("boa",   "DO BATALHÃO DE OPERAÇÕES AÉREAS (BOA)",                   "O",  "do"),
]

DISP_FINAIS = (
    "Os casos omissos neste Regimento Interno serão resolvidos pelo Comandante-Geral do CBMRO.\n"
    "Este Regimento Interno entra em vigor na data de sua publicação, revogadas as disposições em contrário."
)


def normalize(text: str) -> str:
    t = re.sub(r"^\s*[\dIVXivx]+[.)]\s*", "", (text or "").strip())
    return t.strip().lower()


def _dedup_keep_order(items):
    """items: list[{text, source}] -> remove duplicatas por texto normalizado, RO primeiro."""
    seen, out = set(), []
    for it in items:
        k = normalize(it["text"])
        if k and k not in seen:
            seen.add(k)
            out.append(it)
    return out


def ro_items(texts, source="ro"):
    return [{"text": t.strip(), "source": source} for t in texts if (t or "").strip()]


def proposed_text(items):
    return "\n".join(it["text"] for it in items)


def build_finalidade_section(organ):
    """Seção 'Da Finalidade' (prose) — usa a 1ª atribuição/finalidade do órgão."""
    fin = ""
    for a in (organ.get("atribuicoes") or []):
        if a.strip():
            fin = a.strip()
            break
    return {
        "id": "finalidade", "kind": "prose", "sectionTitle": "Da Finalidade",
        "editId": None,  # preenchido pelo chamador
        "proposedText": fin,
    }


def build_competencia_section(organ_key, organ, abbr):
    items = _dedup_keep_order(ro_items(organ.get("atribuicoes") or []))
    return {
        "id": "competencia", "kind": "incisos", "sectionTitle": "Da Competência",
        "editId": None, "caput": f"Compete à {abbr}:" if abbr else "Compete:",
        "items": items, "proposedText": proposed_text(items),
    }


def build_organizacao_section(organ, abbr):
    items = ro_items(organ.get("desdobramentos") or [])
    return {
        "id": "organizacao", "kind": "incisos", "sectionTitle": "Da Organização Interna",
        "editId": None, "caput": f"{abbr} tem a seguinte estrutura interna:" if abbr else "Tem a seguinte estrutura interna:",
        "items": items, "proposedText": proposed_text(items),
    }


def build_cargo_sections(organ_key, organ):
    sections = []
    for c in (organ.get("cargos") or []):
        name = (c.get("cargo") or "").strip()
        if not name:
            continue
        ro = ro_items(c.get("atribuicoes") or [])
        enr = enrich_for(organ_key, name)
        items = _dedup_keep_order(ro + enr)
        if not items:
            continue
        sid = "cargo:" + re.sub(r"[^a-z0-9]+", "-", name.lower()).strip("-")
        sections.append({
            "id": sid, "kind": "incisos",
            "sectionTitle": f"Das Atribuições do {name}",
            "editId": None, "caput": f"Ao {name} compete:",
            "items": items, "proposedText": proposed_text(items),
        })
    return sections


def build_organ_chapter(organ_key, chapter_title, art, de, organ):
    abbr = organ.get("abbreviation") or organ_key.upper()
    sections = []
    sections.append(build_finalidade_section(organ))
    comp = build_competencia_section(organ_key, organ, abbr)
    if comp["items"]:
        sections.append(comp)
    org = build_organizacao_section(organ, abbr)
    if org["items"]:
        sections.append(org)
    sections.extend(build_cargo_sections(organ_key, organ))

    chapter_id = f"organ:{organ_key}"
    for s in sections:
        s["editId"] = f"{chapter_id}/{s['id']}"

    return {
        "id": chapter_id, "kind": "organ", "chapterTitle": chapter_title,
        "organKey": organ_key, "label": organ.get("name", ""), "abbr": abbr,
        "sections": sections,
    }


def build_estrutura_chapter(organs):
    items = []
    for organ_key, _title, art, de, _ in [(k, t, a, d, None) for (k, t, a, d) in ORGAN_ORDER]:
        o = organs.get(organ_key)
        if not o:
            continue
        nome = o.get("name", organ_key.upper())
        abbr = o.get("abbreviation") or organ_key.upper()
        items.append({"text": f"{art.lower()} {nome} ({abbr})", "source": "ro"})
    return {
        "id": "estrutura", "kind": "incisos", "chapterTitle": "DA ESTRUTURA ORGANIZACIONAL",
        "editId": "estrutura",
        "caput": "A estrutura operacional do Corpo de Bombeiros Militar do Estado de Rondônia compõe-se dos seguintes órgãos:",
        "items": items, "proposedText": proposed_text(items),
    }


def build_preliminares_chapter():
    txt = (
        "Este Regimento Interno disciplina a organização, as competências e o funcionamento "
        "da estrutura operacional do Corpo de Bombeiros Militar do Estado de Rondônia (CBMRO), "
        "do escalão de direção operacional às frações de execução.\n"
        "A estrutura operacional subordina-se ao Comandante-Geral por intermédio do "
        "Subcomandante-Geral, nos termos da Lei de Organização Básica do CBMRO."
    )
    return {
        "id": "preliminares", "kind": "prose", "chapterTitle": "DAS DISPOSIÇÕES PRELIMINARES",
        "editId": "preliminares", "proposedText": txt,
    }


def build_finais_chapter():
    return {
        "id": "finais", "kind": "prose", "chapterTitle": "DAS DISPOSIÇÕES FINAIS",
        "editId": "finais", "proposedText": DISP_FINAIS,
    }


def main():
    organs = json.loads(RO_JSON.read_text(encoding="utf-8")).get("organs", {})

    chapters = [build_preliminares_chapter(), build_estrutura_chapter(organs)]
    for organ_key, chapter_title, art, de in ORGAN_ORDER:
        o = organs.get(organ_key)
        if not o:
            print(f"  ! órgão ausente no ro.json: {organ_key} — pulando")
            continue
        chapters.append(build_organ_chapter(organ_key, chapter_title, art, de, o))
    chapters.append(build_finais_chapter())

    output = {
        "generated_by": "scripts/build_minuta_structure.py",
        "title": TITLE,
        "chapters": chapters,
    }
    OUT_JSON.write_text(json.dumps(output, ensure_ascii=False, indent=2), encoding="utf-8")

    n_org = sum(1 for c in chapters if c["kind"] == "organ")
    n_sec = sum(len(c.get("sections", [])) for c in chapters if c["kind"] == "organ")
    print(f"Gerado: {OUT_JSON}")
    print(f"  {len(chapters)} capítulos · {n_org} órgãos · {n_sec} seções de função")


if __name__ == "__main__":
    main()
```

- [ ] **Step 2: Rodar o gerador**

Run: `python scripts/build_minuta_structure.py`
Expected: imprime `Gerado: ...minuta_structure.json` e uma linha tipo `13 capítulos · 10 órgãos · NN seções de função` (sem `! órgão ausente`).

- [ ] **Step 3: Commit**

```bash
git add scripts/build_minuta_structure.py database/minuta_structure.json
git commit -m "feat: gerador hierárquico da minuta operacional (RO + enriquecimento)"
```

---

## Task 4: Validar a forma do JSON gerado

**Files:**
- Read-only: `database/minuta_structure.json`

- [ ] **Step 1: Conferir invariantes estruturais do JSON**

Run:
```bash
python -c "
import json
d=json.load(open('database/minuta_structure.json',encoding='utf-8'))
assert d['title']
chaps=d['chapters']
assert chaps[0]['id']=='preliminares' and chaps[0]['kind']=='prose'
assert chaps[1]['id']=='estrutura' and chaps[1]['kind']=='incisos'
assert chaps[-1]['id']=='finais'
organs=[c for c in chaps if c['kind']=='organ']
assert [c['organKey'] for c in organs][:3]==['dpo','cot','doe'], [c['organKey'] for c in organs]
# toda seção incisos tem items {text,source} e editId
for c in organs:
    for s in c['sections']:
        assert s['editId'].startswith('organ:')
        if s['kind']=='incisos':
            for it in s['items']:
                assert 'text' in it and 'source' in it
# há ao menos uma fonte de enriquecimento CBMAL presente
blob=json.dumps(d,ensure_ascii=False)
assert 'cf. CBMAL' in blob, 'sem enriquecimento'
print('OK:', len(organs),'órgãos; enriquecimento presente')
"
```
Expected: `OK: 10 órgãos; enriquecimento presente` (sem AssertionError).

- [ ] **Step 2: (sem commit — etapa de verificação apenas)**

Nenhuma alteração de arquivo nesta task.

---

## Task 5: Reescrever o wizard (`MinutaWizard.jsx`)

**Files:**
- Modify: `src/pages/MinutaWizard.jsx`

O modelo de dados mudou de `data[organKey].sections` para `data.chapters[]`. O wizard passa a: (1) carregar a minuta inteira; (2) etapa de revisão navega TODOS os nós-folha editáveis em sequência (cada folha tem `editId`); (3) prévia ao vivo do articulado completo; (4) `.docx` com Título/Capítulo/Seção e citações.

- [ ] **Step 1: Substituir `MinutaWizard.jsx` pelo modelo hierárquico**

Substituir o arquivo inteiro por:

```jsx
import { useState, useEffect, useMemo } from 'react'
import { ChevronRight, ChevronLeft, Download, ArrowLeft } from 'lucide-react'
import {
  Document, Packer, Paragraph, TextRun,
  Footer, AlignmentType, ImageRun,
} from 'docx'
import { buildArticles, articleLabel, romanize } from '../lib/minutaArticles.js'

const STEP_LABELS = ['Visão geral', 'Revisão das seções', 'Download']

// Achata a estrutura em nós-folha editáveis (cada um com editId, título e contexto).
function flattenLeaves(structure) {
  const leaves = []
  for (const ch of structure.chapters) {
    if (ch.kind === 'organ') {
      for (const s of ch.sections) {
        leaves.push({
          editId: s.editId, kind: s.kind,
          title: `${ch.abbr} — ${s.sectionTitle}`,
          chapter: ch.chapterTitle,
          proposedText: s.proposedText ?? '',
          items: s.items ?? null,
        })
      }
    } else {
      leaves.push({
        editId: ch.editId, kind: ch.kind,
        title: ch.chapterTitle,
        chapter: ch.chapterTitle,
        proposedText: ch.proposedText ?? '',
        items: ch.items ?? null,
      })
    }
  }
  return leaves
}

function ArticlePreview({ articles }) {
  if (!articles.length) {
    return <p style={{ color: 'var(--text-muted)', fontSize: 13 }}>(sem conteúdo)</p>
  }
  return (
    <div style={{ fontFamily: 'Georgia, "Times New Roman", serif', fontSize: 14, lineHeight: 1.7, color: '#1a1a1a' }}>
      {articles.map(art => (
        <div key={art.number} style={{ marginBottom: 10 }}>
          {art.chapterTitle && (
            <p style={{ textAlign: 'center', fontWeight: 700, margin: '18px 0 6px' }}>
              CAPÍTULO {romanize(art.chapterNumber)}<br />{art.chapterTitle}
            </p>
          )}
          {art.sectionTitle && (
            <p style={{ textAlign: 'center', fontWeight: 600, fontStyle: 'italic', margin: '8px 0 8px' }}>
              Seção {romanize(art.sectionNumber)} — {art.sectionTitle}
            </p>
          )}
          <p style={{ textAlign: 'justify', margin: '0 0 6px', textIndent: art.incisos.length ? 0 : '1.25em' }}>
            <strong>{articleLabel(art.number)}</strong> {art.caput}
          </p>
          {art.incisos.map((inc, i) => (
            <p key={i} style={{ textAlign: 'justify', margin: '0 0 4px', paddingLeft: '2em', textIndent: '-1em' }}>
              {romanize(i + 1)} - {inc.text}
              {inc.source && inc.source !== 'ro' && (
                <span style={{
                  marginLeft: 6, fontSize: 11, fontFamily: 'Inter, sans-serif',
                  color: '#fff', background: '#c8102e', borderRadius: 4, padding: '1px 6px',
                }}>{inc.source}</span>
              )}
            </p>
          ))}
        </div>
      ))}
    </div>
  )
}

export default function MinutaWizard() {
  const [step, setStep] = useState(0)
  const [data, setData] = useState(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)
  const [leafIdx, setLeafIdx] = useState(0)
  const [edits, setEdits] = useState({})
  const [generating, setGenerating] = useState(false)

  useEffect(() => {
    fetch('/database/minuta_structure.json')
      .then(r => { if (!r.ok) throw new Error(r.status); return r.json() })
      .then(setData)
      .catch(() => setError('Erro ao carregar minuta_structure.json. Execute build_minuta_structure.py.'))
      .finally(() => setLoading(false))
  }, [])

  const leaves = useMemo(() => (data ? flattenLeaves(data) : []), [data])

  function startReview() {
    const initial = {}
    leaves.forEach(l => { initial[l.editId] = l.proposedText })
    setEdits(initial)
    setLeafIdx(0)
    setStep(1)
  }

  function handleNext() {
    if (leafIdx < leaves.length - 1) setLeafIdx(i => i + 1)
    else setStep(2)
  }
  function handlePrev() {
    if (leafIdx > 0) setLeafIdx(i => i - 1)
  }

  async function handleDownload() {
    setGenerating(true)
    try {
      const dateStr = new Date().toLocaleDateString('pt-BR', { day: '2-digit', month: 'long', year: 'numeric' })

      let imageData = null
      try {
        const resp = await fetch('/BrasaoCBMRO2D-COMPLETO.png')
        if (resp.ok) imageData = await resp.arrayBuffer()
      } catch (_) { /* segue sem imagem */ }

      const children = []
      if (imageData) {
        children.push(new Paragraph({
          alignment: AlignmentType.CENTER,
          children: [new ImageRun({ data: imageData, transformation: { width: 65, height: 65 }, type: 'png' })],
        }))
      }
      children.push(
        new Paragraph({
          alignment: AlignmentType.CENTER, spacing: { before: 120 },
          children: [new TextRun({ text: 'CORPO DE BOMBEIROS MILITAR DO ESTADO DE RONDÔNIA', bold: true, size: 28, font: 'Times New Roman' })],
        }),
        new Paragraph({
          alignment: AlignmentType.CENTER,
          children: [new TextRun({ text: `Minuta de Regimento Interno — ${data.title}`, size: 24, font: 'Times New Roman' })],
        }),
        new Paragraph({
          alignment: AlignmentType.CENTER, spacing: { after: 480 },
          children: [new TextRun({ text: dateStr, size: 22, font: 'Times New Roman', italics: true })],
        }),
      )

      const articles = buildArticles(data, edits)
      let chapterSeen = false
      articles.forEach(art => {
        if (art.chapterTitle) {
          children.push(
            new Paragraph({
              alignment: AlignmentType.CENTER, pageBreakBefore: chapterSeen,
              spacing: { before: 240, after: 0 },
              children: [new TextRun({ text: `CAPÍTULO ${romanize(art.chapterNumber)}`, bold: true, font: 'Times New Roman', size: 26 })],
            }),
            new Paragraph({
              alignment: AlignmentType.CENTER, spacing: { after: 120 },
              children: [new TextRun({ text: art.chapterTitle, bold: true, font: 'Times New Roman', size: 26 })],
            }),
          )
          chapterSeen = true
        }
        if (art.sectionTitle) {
          children.push(new Paragraph({
            alignment: AlignmentType.CENTER, spacing: { before: 120, after: 80 },
            children: [new TextRun({ text: `Seção ${romanize(art.sectionNumber)} — ${art.sectionTitle}`, bold: true, italics: true, font: 'Times New Roman', size: 24 })],
          }))
        }
        children.push(new Paragraph({
          alignment: AlignmentType.JUSTIFIED,
          spacing: { line: 360, after: art.incisos.length ? 60 : 120 },
          indent: art.incisos.length ? undefined : { firstLine: 708 },
          children: [
            new TextRun({ text: `${articleLabel(art.number)} `, bold: true, font: 'Times New Roman', size: 24 }),
            new TextRun({ text: art.caput, font: 'Times New Roman', size: 24 }),
          ],
        }))
        art.incisos.forEach((inc, i) => {
          const runs = [new TextRun({ text: `${romanize(i + 1)} - ${inc.text}`, font: 'Times New Roman', size: 24 })]
          if (inc.source && inc.source !== 'ro') {
            runs.push(new TextRun({ text: ` (${inc.source})`, font: 'Times New Roman', size: 20, italics: true, color: '888888' }))
          }
          children.push(new Paragraph({
            alignment: AlignmentType.JUSTIFIED, spacing: { line: 360, after: 60 },
            indent: { left: 708, hanging: 340 }, children: runs,
          }))
        })
      })

      const doc = new Document({
        sections: [{
          properties: { page: { margin: { top: 1701, right: 1134, bottom: 1134, left: 1701 } } },
          footers: {
            default: new Footer({
              children: [new Paragraph({
                alignment: AlignmentType.CENTER,
                children: [new TextRun({ text: `Documento gerado pelo Portal de Legislação CBM — CBMRO · ${dateStr}`, size: 18, font: 'Times New Roman', italics: true })],
              })],
            }),
          },
          children,
        }],
      })

      const blob = await Packer.toBlob(doc)
      const url = URL.createObjectURL(blob)
      const a = document.createElement('a')
      a.href = url
      a.download = 'Minuta_RI_Operacional_CBMRO.docx'
      document.body.appendChild(a)
      a.click()
      document.body.removeChild(a)
      URL.revokeObjectURL(url)
    } finally {
      setGenerating(false)
    }
  }

  if (loading) {
    return (
      <>
        <div className="page-header"><div className="page-header-left"><h2 className="page-title">Minuta de Regimento Interno</h2></div></div>
        <div className="page-body" style={{ padding: 32 }}><p style={{ color: 'var(--text-muted)' }}>Carregando dados…</p></div>
      </>
    )
  }
  if (error) {
    return (
      <>
        <div className="page-header"><div className="page-header-left"><h2 className="page-title">Minuta de Regimento Interno</h2></div></div>
        <div className="page-body" style={{ padding: 32 }}><p style={{ color: '#c8102e' }}>{error}</p></div>
      </>
    )
  }

  const leaf = leaves[leafIdx] ?? null
  const allArticles = buildArticles(data, edits)

  return (
    <>
      <div className="page-header">
        <div className="page-header-left">
          <h2 className="page-title">Minuta de Regimento Interno</h2>
          <p className="page-subtitle">
            Minuta articulada da estrutura operacional do CBMRO — do topo (DPO/COT/DOE)
            à menor fração — com competências do CBMRO e subsídios de outras legislações.
          </p>
        </div>
      </div>

      <div className="page-body">
        <div style={{ display: 'flex', alignItems: 'center', gap: 8, marginBottom: 32 }}>
          {STEP_LABELS.map((label, i) => (
            <div key={i} style={{ display: 'flex', alignItems: 'center', gap: 8 }}>
              <div style={{
                width: 28, height: 28, borderRadius: '50%', display: 'flex', alignItems: 'center', justifyContent: 'center',
                background: i <= step ? '#c8102e' : '#d1d5db', color: '#fff', fontWeight: 700, fontSize: 13, flexShrink: 0,
              }}>{i + 1}</div>
              <span style={{ fontSize: 13, color: i === step ? '#c8102e' : 'var(--text-muted)', fontWeight: i === step ? 600 : 400 }}>{label}</span>
              {i < 2 && <ChevronRight size={16} color="#d1d5db" style={{ flexShrink: 0 }} />}
            </div>
          ))}
        </div>

        {/* Etapa 0: visão geral + prévia completa */}
        {step === 0 && (
          <div>
            <div style={{ border: '1px solid var(--border-card)', borderRadius: 8, background: '#fff', padding: 24, marginBottom: 20, maxHeight: 520, overflow: 'auto' }}>
              <ArticlePreview articles={buildArticles(data, {})} />
            </div>
            <button onClick={startReview} style={{
              display: 'flex', alignItems: 'center', gap: 8, padding: '11px 26px', border: 'none', borderRadius: 7,
              background: '#c8102e', color: '#fff', fontWeight: 600, cursor: 'pointer', fontSize: 15,
            }}>Revisar e editar seções <ChevronRight size={18} /></button>
          </div>
        )}

        {/* Etapa 1: revisão folha a folha */}
        {step === 1 && leaf && (
          <div style={{ display: 'flex', gap: 24, flexWrap: 'wrap', alignItems: 'flex-start' }}>
            <div style={{ flex: '1 1 420px', minWidth: 0 }}>
              <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'baseline', marginBottom: 6 }}>
                <span style={{ fontWeight: 700, color: '#121d3d', fontSize: 16 }}>{leaf.title}</span>
                <span style={{ color: 'var(--text-muted)', fontSize: 13 }}>Seção {leafIdx + 1} de {leaves.length}</span>
              </div>
              <textarea
                value={edits[leaf.editId] ?? ''}
                onChange={e => setEdits(prev => ({ ...prev, [leaf.editId]: e.target.value }))}
                style={{
                  width: '100%', minHeight: 320, padding: 14, border: '1.5px solid var(--border-card)', borderRadius: 8,
                  fontSize: 14, lineHeight: 1.7, fontFamily: 'Inter, sans-serif', resize: 'vertical', boxSizing: 'border-box', outline: 'none',
                }}
              />
              <div style={{ display: 'flex', justifyContent: 'space-between', marginTop: 18 }}>
                <button onClick={handlePrev} disabled={leafIdx === 0} style={{
                  display: 'flex', alignItems: 'center', gap: 6, padding: '9px 20px', border: '1.5px solid var(--border-card)', borderRadius: 7,
                  background: '#fff', cursor: leafIdx === 0 ? 'not-allowed' : 'pointer', opacity: leafIdx === 0 ? 0.4 : 1, fontSize: 14,
                }}><ChevronLeft size={16} /> Anterior</button>
                <button onClick={handleNext} style={{
                  display: 'flex', alignItems: 'center', gap: 6, padding: '9px 24px', border: 'none', borderRadius: 7,
                  background: '#c8102e', color: '#fff', fontWeight: 600, cursor: 'pointer', fontSize: 14,
                }}>{leafIdx < leaves.length - 1 ? 'Próxima' : 'Finalizar'} <ChevronRight size={16} /></button>
              </div>
            </div>
            <div style={{ flex: '1 1 360px', minWidth: 0, border: '1px solid var(--border-card)', borderRadius: 8, background: '#fff', padding: 20, position: 'sticky', top: 16, maxHeight: '80vh', overflow: 'auto' }}>
              <div style={{ fontSize: 12, fontWeight: 700, color: 'var(--text-muted)', textTransform: 'uppercase', marginBottom: 8 }}>Prévia ao vivo</div>
              <ArticlePreview articles={allArticles} />
            </div>
          </div>
        )}

        {/* Etapa 2: download */}
        {step === 2 && (
          <div style={{ maxWidth: 820 }}>
            <h3 style={{ color: '#121d3d', marginBottom: 16, fontSize: 17 }}>Resumo da minuta — {data.title}</h3>
            <div style={{ border: '1px solid var(--border-card)', borderRadius: 8, background: '#fff', padding: 24, marginBottom: 4, maxHeight: 520, overflow: 'auto' }}>
              <ArticlePreview articles={allArticles} />
            </div>
            <div style={{ display: 'flex', gap: 12, marginTop: 24, flexWrap: 'wrap' }}>
              <button onClick={() => { setLeafIdx(leaves.length - 1); setStep(1) }} style={{
                display: 'flex', alignItems: 'center', gap: 6, padding: '10px 20px', border: '1.5px solid var(--border-card)', borderRadius: 7,
                background: '#fff', cursor: 'pointer', fontSize: 14,
              }}><ArrowLeft size={16} /> Voltar e editar</button>
              <button onClick={handleDownload} disabled={generating} style={{
                display: 'flex', alignItems: 'center', gap: 8, padding: '10px 24px', border: 'none', borderRadius: 7,
                background: generating ? '#9ca3af' : '#c8102e', color: '#fff', fontWeight: 600, cursor: generating ? 'wait' : 'pointer', fontSize: 14,
              }}><Download size={16} />{generating ? 'Gerando…' : 'Baixar Minuta_RI_Operacional_CBMRO.docx'}</button>
            </div>
          </div>
        )}
      </div>
    </>
  )
}
```

- [ ] **Step 2: Garantir o dev server e checar o build de produção**

Run: `npm run build`
Expected: build conclui sem erros (sem referências a `data[selectedOrgan]` ou `ORGAN_OPTIONS`).

- [ ] **Step 3: Commit**

```bash
git add src/pages/MinutaWizard.jsx
git commit -m "feat: wizard hierárquico (árvore operacional, prévia completa, badges de fonte)"
```

---

## Task 6: Verificação manual e checkpoint

**Files:** nenhuma alteração de código (verificação).

- [ ] **Step 1: Subir o dev server**

Run (background): `npm run dev -- --port 5173 --strictPort`
Expected: `Local: http://localhost:5173/`.

- [ ] **Step 2: Conferir o wizard no navegador**

Abrir http://localhost:5173 → página "Minuta de Regimento Interno". Verificar:
- Etapa 0 mostra a prévia completa com CAPÍTULOS (Preliminares, Estrutura, DPO, COT, DOE, CRBM, BBM, CIBM, GBM, BBS, BIFEA, BOA, Disposições Finais) e Seções por função.
- Incisos enriquecidos exibem o badge vermelho `cf. CBMAL, RI, Art. NNN` (ex.: no capítulo do CRBM/BBM).
- Numeração de artigos é contínua e crescente atravessando capítulos.
- Etapa 1 navega folha a folha; editar um textarea atualiza a prévia ao vivo.
- Etapa 2 baixa `Minuta_RI_Operacional_CBMRO.docx`; abrir e conferir Título/Capítulos/Seções e as citações entre parênteses.

- [ ] **Step 3: Confirmar que o Comparador de Cargos segue intacto**

Abrir o Dashboard → aba "Comparativo de Cargos". Confirmar que carrega normalmente (o `ro.json` não foi alterado).

- [ ] **Step 4: Checkpoint final**

```bash
git add -A
git commit -m "chore: checkpoint — minuta operacional hierárquica completa"
```

---

## Self-Review (preenchido pelo autor do plano)

- **Cobertura do spec:** escopo completo (Task 3 ORGAN_ORDER cobre DPO/COT/DOE/CRBM/BBM/CIBM/GBM/BBS/BIFEA/BOA); RO verbatim + enriquecimento rotulado (Task 2 + `_dedup_keep_order` RO-first em Task 3); estrutura hierárquica Título→Capítulo→Seção (Task 1); ro.json intocado (Task 3 lê, não escreve; Task 6 Step 3 valida); frontend wizard + .docx (Task 5); testes (Task 1). ✔
- **Consistência de tipos:** itens são sempre `{text, source}`; `editId` em todo nó-folha; `buildArticles` consome `{chapters:[...]}` em lib (Task 1), build (Task 3) e wizard (Task 5). Incisos no artigo são `{text, source}` e o wizard lê `inc.text`/`inc.source`. ✔
- **Sem placeholders:** todo código e texto verbatim presentes; comandos com saída esperada. ✔
- **YAGNI:** enriquecimento só para funções com correspondência clara (comandante/adjunto de unidade); Companhia/Coordenador/Diretor ficam RO verbatim nesta entrega.
