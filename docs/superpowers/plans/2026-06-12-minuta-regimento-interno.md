# Minuta de Regimento Interno Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Adicionar ao portal um wizard de 3 etapas que gera uma minuta de Regimento Interno em `.docx` para a DPO ou o COT do CBMRO, com texto proposto mesclado dos 26 outros CBMs e editável pelo usuário seção a seção.

**Architecture:** Um script Python (`build_minuta_structure.py`) lê `comparativo_dpo_cot.json` e gera `database/minuta_structure.json` com 5 seções por órgão e texto mesclado. O componente React `MinutaWizard.jsx` consome esse JSON via fetch e usa a biblioteca `docx` (npm) para gerar e baixar o `.docx` client-side. Nenhuma mudança na infraestrutura Vite — o plugin `serveDatabase` já serve `database/` automaticamente.

**Tech Stack:** Python stdlib (json, re) · React · `docx` npm (v8) · Lucide React

---

## Mapa de arquivos

| Ação | Arquivo |
|------|---------|
| Criar | `scripts/build_minuta_structure.py` |
| Criar | `database/minuta_structure.json` (gerado pelo script) |
| Criar | `src/pages/MinutaWizard.jsx` |
| Modificar | `src/App.jsx` (nova rota + item NAV) |
| Modificar | `CLAUDE.md` (novo comando de build) |

---

## Task 1: Instalar biblioteca `docx`

**Files:**
- Modify: `package.json` (dependência adicionada pelo npm)

- [ ] **Step 1: Instalar o pacote**

```bash
npm install docx
```

- [ ] **Step 2: Verificar instalação**

```bash
node -e "const { Document } = require('docx'); console.log('ok')"
```

Esperado: `ok`

- [ ] **Step 3: Commit**

```bash
git add package.json package-lock.json
git commit -m "chore: adiciona biblioteca docx para geração de .docx client-side"
```

---

## Task 2: Script Python `build_minuta_structure.py`

**Files:**
- Create: `scripts/build_minuta_structure.py`
- Create: `database/minuta_structure.json` (gerado)

- [ ] **Step 1: Criar o script**

Criar `scripts/build_minuta_structure.py` com o conteúdo abaixo:

```python
"""
build_minuta_structure.py — Portal CBM

Gera database/minuta_structure.json com estrutura de 5 seções por órgão
(DPO e COT), texto proposto mesclado dos 27 CBMs e lista de fontes.

Entrada: database/comparativo_dpo_cot.json
Saída:   database/minuta_structure.json

Rodar: python scripts/build_minuta_structure.py
"""

import json
import re
import sys
from pathlib import Path

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

BASE_DIR = Path(__file__).parent.parent
IN_JSON  = BASE_DIR / "database" / "comparativo_dpo_cot.json"
OUT_JSON = BASE_DIR / "database" / "minuta_structure.json"

SECTIONS = [
    {"id": "subordinacao",       "title": "Denominação e Subordinação"},
    {"id": "finalidade",         "title": "Finalidade"},
    {"id": "competencias",       "title": "Competências"},
    {"id": "organizacao",        "title": "Organização Interna"},
    {"id": "cargos_atribuicoes", "title": "Atribuições dos Cargos"},
]

ORGAN_LABELS = {
    "dpo": "Diretoria de Planejamento Operacional",
    "cot": "Comando de Operações Técnicas",
}


def normalize(text: str) -> str:
    text = re.sub(r"^\s*[\dIVXivx]+[.)]\s*", "", text.strip())
    return text.strip().lower()


def organs_of(state: dict, group_key: str) -> list:
    v = state.get(group_key)
    return v if isinstance(v, list) else []


# ── Extratores por seção ──

def extract_subordinacao(organs: list, state: dict) -> str:
    if not organs:
        return ""
    o = organs[0]
    name  = o.get("name", "")
    abbr  = o.get("abbreviation", "")
    sub   = o.get("subordinadoA", "")
    base  = o.get("baseLegal", "")
    ref   = o.get("legalRef", "")
    parts = []
    if name and abbr:
        parts.append(f"A {name} ({abbr})")
    elif name:
        parts.append(f"A {name}")
    if sub:
        parts.append(f"é subordinada a {sub}")
    if ref and base:
        parts.append(f"conforme {ref} de {base}")
    elif base:
        parts.append(f"conforme {base}")
    return (", ".join(parts) + ".") if parts else ""


def extract_finalidade(organs: list, _state: dict) -> str:
    for o in organs:
        for a in (o.get("atribuicoes") or []):
            if a.strip():
                return a.strip()
    return ""


def extract_competencias(organs: list, _state: dict) -> str:
    seen, items = set(), []
    for o in organs:
        for a in (o.get("atribuicoes") or []):
            key = normalize(a)
            if key and key not in seen:
                seen.add(key)
                items.append(a.strip())
    if not items:
        return ""
    return "\n".join(f"{i+1}. {item}" for i, item in enumerate(items))


def extract_organizacao(organs: list, _state: dict) -> str:
    for o in organs:
        desdb = o.get("desdobramentos") or []
        if desdb:
            return "\n".join(f"- {d}" for d in desdb)
    return ""


def extract_cargos_atribuicoes(organs: list, _state: dict) -> str:
    seen_cargos, blocks = set(), []
    for o in organs:
        for c in (o.get("cargos") or []):
            cargo_name = (c.get("cargo") or "").strip()
            if not cargo_name or cargo_name.lower() in seen_cargos:
                continue
            seen_cargos.add(cargo_name.lower())
            atrib = c.get("atribuicoes") or []
            if not atrib:
                continue
            lines = [f"{cargo_name}:"]
            for i, a in enumerate(atrib, 1):
                lines.append(f"  {i}. {a.strip()}")
            blocks.append("\n".join(lines))
    return "\n\n".join(blocks)


EXTRACTORS = {
    "subordinacao":       extract_subordinacao,
    "finalidade":         extract_finalidade,
    "competencias":       extract_competencias,
    "organizacao":        extract_organizacao,
    "cargos_atribuicoes": extract_cargos_atribuicoes,
}


def build_section(section_id: str, all_states: list, group_key: str) -> dict:
    title = next(s["title"] for s in SECTIONS if s["id"] == section_id)
    extractor = EXTRACTORS[section_id]

    # Coleta texto por estado
    state_texts = {}
    for state in all_states:
        org = organs_of(state, group_key)
        if not org:
            continue
        text = extractor(org, state)
        if text.strip():
            state_texts[state["id"]] = text.strip()

    ref_text = state_texts.get("ro", "")
    others   = {k: v for k, v in state_texts.items() if k != "ro"}

    if section_id in ("subordinacao", "finalidade", "organizacao"):
        # Prosa: base é RO; se vazio, maior dos outros
        if ref_text:
            proposed = ref_text
        elif others:
            proposed = max(others.values(), key=len)
        else:
            proposed = ""
        sources = list(state_texts.keys())

    elif section_id == "competencias":
        # Mescla todos os estados (RO primeiro), deduplicando
        merged_organs = []
        for state in all_states:
            if state["id"] == "ro":
                merged_organs.extend(organs_of(state, group_key))
        for state in all_states:
            if state["id"] != "ro":
                merged_organs.extend(organs_of(state, group_key))
        proposed = extract_competencias(merged_organs, {})
        sources  = list(state_texts.keys())

    else:  # cargos_atribuicoes — usa RO como base canônica
        ro_organs = []
        for state in all_states:
            if state["id"] == "ro":
                ro_organs.extend(organs_of(state, group_key))
        proposed = extract_cargos_atribuicoes(ro_organs, {})
        sources  = ["ro"] if ref_text else []
        if not proposed and others:
            # Fallback: primeiro estado com cargos
            for state in all_states:
                if state["id"] == "ro":
                    continue
                org = organs_of(state, group_key)
                candidate = extract_cargos_atribuicoes(org, state)
                if candidate:
                    proposed = candidate
                    sources  = [state["id"]]
                    break

    return {"id": section_id, "title": title, "proposedText": proposed, "sources": sources}


def build_organ(all_states: list, group_key: str) -> dict:
    return {
        "label":    ORGAN_LABELS[group_key],
        "sections": [build_section(s["id"], all_states, group_key) for s in SECTIONS],
    }


def main():
    data       = json.loads(IN_JSON.read_text(encoding="utf-8"))
    all_states = data["states"]
    output = {
        "generated_by": "scripts/build_minuta_structure.py",
        "dpo": build_organ(all_states, "dpo"),
        "cot": build_organ(all_states, "cot"),
    }
    OUT_JSON.write_text(json.dumps(output, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Gerado: {OUT_JSON}")
    for key in ("dpo", "cot"):
        seções = output[key]["sections"]
        filled = sum(1 for s in seções if s["proposedText"])
        print(f"  {key.upper()}: {filled}/{len(seções)} seções com texto")


if __name__ == "__main__":
    main()
```

- [ ] **Step 2: Executar o script**

```bash
python scripts/build_minuta_structure.py
```

Esperado (exemplo):
```
Gerado: .../database/minuta_structure.json
  DPO: 5/5 seções com texto
  COT: 5/5 seções com texto
```

- [ ] **Step 3: Inspecionar o JSON gerado**

```bash
python -c "
import json; d = json.load(open('database/minuta_structure.json', encoding='utf-8'))
for key in ('dpo','cot'):
    print(key.upper())
    for s in d[key]['sections']:
        preview = (s['proposedText'] or '')[:60].replace('\n',' ')
        print(f'  {s[\"id\"]}: {len(s[\"sources\"])} fontes | {preview!r}')
"
```

Verificar: todas as 5 seções de cada órgão têm `proposedText` não-vazio e ao menos 1 fonte.

- [ ] **Step 4: Commit**

```bash
git add scripts/build_minuta_structure.py database/minuta_structure.json
git commit -m "feat: script Python que gera minuta_structure.json para o wizard de minuta RI"
```

---

## Task 3: Rota e item de navegação em `App.jsx`

**Files:**
- Modify: `src/App.jsx:1-19` (imports e array NAV)
- Modify: `src/App.jsx:100-111` (Routes)

- [ ] **Step 1: Adicionar import do MinutaWizard e ícone**

No topo de `src/App.jsx`, adicionar `ScrollText` nos imports de lucide e o import do componente:

```jsx
import {
  Flame, LayoutDashboard, BookOpen, GitCompare,
  Search, Shield, FileText, Award, Library, ScrollText
} from 'lucide-react'
import Dashboard from './pages/Dashboard.jsx'
import StatesList from './pages/StatesList.jsx'
import StateDetail from './pages/StateDetail.jsx'
import Compare from './pages/Compare.jsx'
import SearchPage from './pages/Search.jsx'
import Legislations from './pages/Legislations.jsx'
import MinutaWizard from './pages/MinutaWizard.jsx'
```

- [ ] **Step 2: Adicionar item ao array NAV**

```jsx
const NAV = [
  { to: '/', icon: LayoutDashboard, label: 'Início', end: true },
  { to: '/estados', icon: BookOpen, label: 'Estados' },
  { to: '/legislacoes', icon: Library, label: 'Acervo Legal' },
  { to: '/comparar', icon: GitCompare, label: 'Comparativo' },
  { to: '/busca', icon: Search, label: 'Busca Textual' },
  { to: '/minuta', icon: ScrollText, label: 'Minuta RI' },
]
```

- [ ] **Step 3: Adicionar a rota dentro de `<Routes>`**

```jsx
<Routes>
  <Route path="/" element={<Dashboard />} />
  <Route path="/estados" element={<StatesList />} />
  <Route path="/estados/:stateId" element={<StateDetail />} />
  <Route path="/legislacoes" element={<Legislations />} />
  <Route path="/comparar" element={<Compare />} />
  <Route path="/busca" element={<SearchPage />} />
  <Route path="/minuta" element={<MinutaWizard />} />
</Routes>
```

- [ ] **Step 4: Verificar no browser**

Iniciar `npm run dev` (se não estiver rodando) e abrir http://localhost:5173. O item "Minuta RI" deve aparecer na sidebar. Clicar nele deve exibir tela em branco ou erro "MinutaWizard não encontrado" (ainda não criado) — isso é esperado.

- [ ] **Step 5: Commit**

```bash
git add src/App.jsx
git commit -m "feat: adiciona rota /minuta e item de nav para o wizard de minuta RI"
```

---

## Task 4: Componente `MinutaWizard.jsx`

**Files:**
- Create: `src/pages/MinutaWizard.jsx`

- [ ] **Step 1: Criar o componente**

Criar `src/pages/MinutaWizard.jsx` com o conteúdo abaixo:

```jsx
import { useState, useEffect } from 'react'
import { ChevronRight, ChevronLeft, Download, ArrowLeft } from 'lucide-react'
import {
  Document, Packer, Paragraph, TextRun, HeadingLevel,
  Footer, AlignmentType, ImageRun,
} from 'docx'

const ORGAN_OPTIONS = [
  {
    key: 'dpo',
    label: 'DPO',
    fullName: 'Diretoria de Planejamento Operacional',
    description:
      'Órgão responsável pelo planejamento, direção, coordenação, supervisão, ' +
      'fiscalização e avaliação das atividades operacionais da Corporação.',
  },
  {
    key: 'cot',
    label: 'COT',
    fullName: 'Comando de Operações Técnicas',
    description:
      'Órgão responsável pelo controle e observância dos requisitos técnicos contra ' +
      'incêndio e pânico — análise de projetos, vistorias, fiscalização e perícia.',
  },
]

export default function MinutaWizard() {
  const [step, setStep] = useState(0)            // 0 escolha | 1 revisão | 2 download
  const [selectedOrgan, setSelectedOrgan] = useState(null)
  const [data, setData] = useState(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)
  const [sectionIdx, setSectionIdx] = useState(0)
  const [edits, setEdits] = useState({})
  const [generating, setGenerating] = useState(false)

  useEffect(() => {
    fetch('/database/minuta_structure.json')
      .then(r => { if (!r.ok) throw new Error(r.status); return r.json() })
      .then(setData)
      .catch(() => setError('Erro ao carregar minuta_structure.json. Execute build_minuta_structure.py.'))
      .finally(() => setLoading(false))
  }, [])

  function handleSelectOrgan(key) {
    const sections = data[key].sections
    const initial = {}
    sections.forEach(s => { initial[s.id] = s.proposedText })
    setEdits(initial)
    setSelectedOrgan(key)
    setSectionIdx(0)
    setStep(1)
  }

  function handleNext() {
    const sections = data[selectedOrgan].sections
    if (sectionIdx < sections.length - 1) {
      setSectionIdx(i => i + 1)
    } else {
      setStep(2)
    }
  }

  function handlePrev() {
    if (sectionIdx > 0) setSectionIdx(i => i - 1)
  }

  async function handleDownload() {
    setGenerating(true)
    try {
      const organInfo = ORGAN_OPTIONS.find(o => o.key === selectedOrgan)
      const sections  = data[selectedOrgan].sections
      const dateStr   = new Date().toLocaleDateString('pt-BR', {
        day: '2-digit', month: 'long', year: 'numeric',
      })

      // Carrega brasão como ArrayBuffer
      let imageData = null
      try {
        const resp = await fetch('/BrasaoCBMRO2D-COMPLETO.png')
        if (resp.ok) imageData = await resp.arrayBuffer()
      } catch (_) { /* continua sem imagem */ }

      const children = []

      // Cabeçalho do documento
      if (imageData) {
        children.push(
          new Paragraph({
            alignment: AlignmentType.CENTER,
            children: [
              new ImageRun({
                data: imageData,
                transformation: { width: 65, height: 65 },
                type: 'png',
              }),
            ],
          })
        )
      }
      children.push(
        new Paragraph({
          alignment: AlignmentType.CENTER,
          spacing: { before: 120 },
          children: [
            new TextRun({
              text: 'CORPO DE BOMBEIROS MILITAR DO ESTADO DE RONDÔNIA',
              bold: true, size: 28, font: 'Times New Roman',
            }),
          ],
        }),
        new Paragraph({
          alignment: AlignmentType.CENTER,
          children: [
            new TextRun({
              text: `Minuta de Regimento Interno — ${organInfo.fullName} (${organInfo.label})`,
              size: 24, font: 'Times New Roman',
            }),
          ],
        }),
        new Paragraph({
          alignment: AlignmentType.CENTER,
          spacing: { after: 480 },
          children: [
            new TextRun({
              text: dateStr,
              size: 22, font: 'Times New Roman', italics: true,
            }),
          ],
        })
      )

      // Capítulos
      sections.forEach((section, idx) => {
        children.push(
          new Paragraph({
            heading: HeadingLevel.HEADING_1,
            pageBreakBefore: idx > 0,
            children: [
              new TextRun({
                text: section.title,
                font: 'Times New Roman', size: 28, bold: true,
              }),
            ],
          }),
          new Paragraph({
            spacing: { line: 360, after: 120 },
            children: [
              new TextRun({
                text: edits[section.id] || '',
                font: 'Times New Roman', size: 24,
              }),
            ],
          })
        )
      })

      const doc = new Document({
        sections: [{
          properties: {
            page: {
              margin: { top: 1701, right: 1134, bottom: 1134, left: 1701 },
            },
          },
          footers: {
            default: new Footer({
              children: [
                new Paragraph({
                  alignment: AlignmentType.CENTER,
                  children: [
                    new TextRun({
                      text: `Documento gerado pelo Portal de Legislação CBM — CBMRO · ${dateStr}`,
                      size: 18, font: 'Times New Roman', italics: true,
                    }),
                  ],
                }),
              ],
            }),
          },
          children,
        }],
      })

      const blob = await Packer.toBlob(doc)
      const url  = URL.createObjectURL(blob)
      const a    = document.createElement('a')
      a.href     = url
      a.download = `Minuta_RI_${organInfo.label}_CBMRO.docx`
      document.body.appendChild(a)
      a.click()
      document.body.removeChild(a)
      URL.revokeObjectURL(url)
    } finally {
      setGenerating(false)
    }
  }

  // ── Render guards ──
  if (loading) {
    return (
      <>
        <div className="page-header">
          <div className="page-header-left">
            <h2 className="page-title">Minuta de Regimento Interno</h2>
          </div>
        </div>
        <div className="page-body" style={{ padding: 32 }}>
          <p style={{ color: 'var(--text-muted)' }}>Carregando dados…</p>
        </div>
      </>
    )
  }

  if (error) {
    return (
      <>
        <div className="page-header">
          <div className="page-header-left">
            <h2 className="page-title">Minuta de Regimento Interno</h2>
          </div>
        </div>
        <div className="page-body" style={{ padding: 32 }}>
          <p style={{ color: '#c8102e' }}>{error}</p>
        </div>
      </>
    )
  }

  const STEP_LABELS = ['Escolha do órgão', 'Revisão das seções', 'Download']

  return (
    <>
      {/* Cabeçalho da página */}
      <div className="page-header">
        <div className="page-header-left">
          <h2 className="page-title">Minuta de Regimento Interno</h2>
          <p className="page-subtitle">
            Gere uma minuta editável em .docx para a DPO ou o COT do CBMRO,
            baseada na legislação dos 27 CBMs.
          </p>
        </div>
      </div>

      <div className="page-body">
        {/* Stepper */}
        <div style={{ display: 'flex', alignItems: 'center', gap: 8, marginBottom: 32 }}>
          {STEP_LABELS.map((label, i) => (
            <div key={i} style={{ display: 'flex', alignItems: 'center', gap: 8 }}>
              <div style={{
                width: 28, height: 28, borderRadius: '50%',
                display: 'flex', alignItems: 'center', justifyContent: 'center',
                background: i <= step ? '#c8102e' : '#d1d5db',
                color: '#fff', fontWeight: 700, fontSize: 13, flexShrink: 0,
              }}>
                {i + 1}
              </div>
              <span style={{
                fontSize: 13,
                color: i === step ? '#c8102e' : 'var(--text-muted)',
                fontWeight: i === step ? 600 : 400,
              }}>
                {label}
              </span>
              {i < 2 && <ChevronRight size={16} color="#d1d5db" style={{ flexShrink: 0 }} />}
            </div>
          ))}
        </div>

        {/* ── Etapa 0: escolha do órgão ── */}
        {step === 0 && (
          <div style={{ display: 'flex', gap: 24, flexWrap: 'wrap' }}>
            {ORGAN_OPTIONS.map(organ => (
              <button
                key={organ.key}
                onClick={() => handleSelectOrgan(organ.key)}
                style={{
                  flex: '1 1 280px', padding: 28,
                  border: '2px solid var(--border-card)', borderRadius: 12,
                  background: '#fff', cursor: 'pointer', textAlign: 'left',
                  transition: 'border-color 0.15s, box-shadow 0.15s',
                }}
                onMouseEnter={e => {
                  e.currentTarget.style.borderColor = '#c8102e'
                  e.currentTarget.style.boxShadow = '0 4px 16px rgba(200,16,46,0.10)'
                }}
                onMouseLeave={e => {
                  e.currentTarget.style.borderColor = 'var(--border-card)'
                  e.currentTarget.style.boxShadow = 'none'
                }}
              >
                <div style={{ fontWeight: 800, fontSize: 24, color: '#c8102e', marginBottom: 4 }}>
                  {organ.label}
                </div>
                <div style={{ fontWeight: 600, color: '#121d3d', marginBottom: 10, fontSize: 15 }}>
                  {organ.fullName}
                </div>
                <div style={{ color: 'var(--text-muted)', fontSize: 14, lineHeight: 1.55 }}>
                  {organ.description}
                </div>
              </button>
            ))}
          </div>
        )}

        {/* ── Etapa 1: revisão seção a seção ── */}
        {step === 1 && selectedOrgan && (() => {
          const sections = data[selectedOrgan].sections
          const section  = sections[sectionIdx]
          return (
            <div style={{ maxWidth: 760 }}>
              <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'baseline', marginBottom: 6 }}>
                <span style={{ fontWeight: 700, color: '#121d3d', fontSize: 17 }}>
                  {section.title}
                </span>
                <span style={{ color: 'var(--text-muted)', fontSize: 13 }}>
                  Seção {sectionIdx + 1} de {sections.length}
                </span>
              </div>

              {section.sources.length > 0 && (
                <div style={{ display: 'flex', gap: 6, flexWrap: 'wrap', alignItems: 'center', marginBottom: 12 }}>
                  <span style={{ fontSize: 12, color: 'var(--text-muted)' }}>Baseado em:</span>
                  {section.sources.map(s => (
                    <span key={s} style={{
                      background: '#eef1f6', border: '1px solid var(--border-card)',
                      borderRadius: 4, padding: '1px 7px',
                      fontSize: 12, fontWeight: 700, color: '#121d3d', textTransform: 'uppercase',
                    }}>
                      {s}
                    </span>
                  ))}
                </div>
              )}

              <textarea
                value={edits[section.id] ?? ''}
                onChange={e => setEdits(prev => ({ ...prev, [section.id]: e.target.value }))}
                style={{
                  width: '100%', minHeight: 280, padding: 14,
                  border: '1.5px solid var(--border-card)', borderRadius: 8,
                  fontSize: 14, lineHeight: 1.7,
                  fontFamily: 'Inter, sans-serif',
                  resize: 'vertical', boxSizing: 'border-box',
                  outline: 'none',
                }}
                onFocus={e => { e.target.style.borderColor = '#c8102e' }}
                onBlur={e => { e.target.style.borderColor = 'var(--border-card)' }}
              />

              <div style={{ display: 'flex', justifyContent: 'space-between', marginTop: 18 }}>
                <button
                  onClick={handlePrev}
                  disabled={sectionIdx === 0}
                  style={{
                    display: 'flex', alignItems: 'center', gap: 6,
                    padding: '9px 20px',
                    border: '1.5px solid var(--border-card)', borderRadius: 7,
                    background: '#fff', cursor: sectionIdx === 0 ? 'not-allowed' : 'pointer',
                    opacity: sectionIdx === 0 ? 0.4 : 1, fontSize: 14,
                  }}
                >
                  <ChevronLeft size={16} /> Anterior
                </button>
                <button
                  onClick={handleNext}
                  style={{
                    display: 'flex', alignItems: 'center', gap: 6,
                    padding: '9px 24px',
                    border: 'none', borderRadius: 7,
                    background: '#c8102e', color: '#fff',
                    fontWeight: 600, cursor: 'pointer', fontSize: 14,
                  }}
                >
                  {sectionIdx < sections.length - 1 ? 'Próxima' : 'Finalizar'}
                  <ChevronRight size={16} />
                </button>
              </div>
            </div>
          )
        })()}

        {/* ── Etapa 2: download ── */}
        {step === 2 && selectedOrgan && (() => {
          const organInfo = ORGAN_OPTIONS.find(o => o.key === selectedOrgan)
          const sections  = data[selectedOrgan].sections
          return (
            <div style={{ maxWidth: 760 }}>
              <h3 style={{ color: '#121d3d', marginBottom: 16, fontSize: 17 }}>
                Resumo da minuta — {organInfo.fullName}
              </h3>

              {sections.map(section => (
                <details
                  key={section.id}
                  style={{
                    marginBottom: 10,
                    border: '1px solid var(--border-card)',
                    borderRadius: 8, overflow: 'hidden',
                  }}
                >
                  <summary style={{
                    padding: '10px 14px', fontWeight: 600, cursor: 'pointer',
                    background: 'var(--gray-50)', color: '#121d3d', fontSize: 14,
                    listStyle: 'none', display: 'flex', alignItems: 'center', gap: 8,
                  }}>
                    {section.title}
                  </summary>
                  <pre style={{
                    padding: 14, margin: 0,
                    fontSize: 13, whiteSpace: 'pre-wrap',
                    lineHeight: 1.65, color: 'var(--text-secondary)',
                    fontFamily: 'Inter, sans-serif',
                  }}>
                    {edits[section.id] || '(vazio)'}
                  </pre>
                </details>
              ))}

              <div style={{ display: 'flex', gap: 12, marginTop: 24, flexWrap: 'wrap' }}>
                <button
                  onClick={() => { setSectionIdx(data[selectedOrgan].sections.length - 1); setStep(1) }}
                  style={{
                    display: 'flex', alignItems: 'center', gap: 6,
                    padding: '10px 20px',
                    border: '1.5px solid var(--border-card)', borderRadius: 7,
                    background: '#fff', cursor: 'pointer', fontSize: 14,
                  }}
                >
                  <ArrowLeft size={16} /> Voltar e editar
                </button>
                <button
                  onClick={handleDownload}
                  disabled={generating}
                  style={{
                    display: 'flex', alignItems: 'center', gap: 8,
                    padding: '10px 24px',
                    border: 'none', borderRadius: 7,
                    background: generating ? '#9ca3af' : '#c8102e',
                    color: '#fff', fontWeight: 600,
                    cursor: generating ? 'wait' : 'pointer', fontSize: 14,
                  }}
                >
                  <Download size={16} />
                  {generating
                    ? 'Gerando…'
                    : `Baixar Minuta_RI_${organInfo.label}_CBMRO.docx`}
                </button>
              </div>
            </div>
          )
        })()}
      </div>
    </>
  )
}
```

- [ ] **Step 2: Verificar no browser — Etapa 0**

Abrir http://localhost:5173/minuta. Deve exibir:
- Stepper com 3 etapas, etapa 1 ativa em vermelho
- Dois cartões clicáveis: DPO e COT

- [ ] **Step 3: Verificar no browser — Etapa 1**

Clicar em "DPO". Deve exibir:
- Título da seção "Denominação e Subordinação"
- Chips com siglas dos estados que contribuíram
- Textarea pré-preenchida com o texto proposto
- Botão "Anterior" desabilitado, botão "Próxima" ativo
- Clicar "Próxima" avança para "Finalidade", e assim por diante
- Na 5ª seção, botão muda para "Finalizar"

- [ ] **Step 4: Verificar no browser — Etapa 2**

Após "Finalizar", deve exibir:
- Resumo colapsável com as 5 seções
- Botão "Voltar e editar" e botão "Baixar Minuta_RI_DPO_CBMRO.docx"

- [ ] **Step 5: Verificar download**

Clicar "Baixar". O arquivo `Minuta_RI_DPO_CBMRO.docx` deve ser baixado. Abrir no Word/LibreOffice e verificar:
- Brasão do CBMRO no topo (ou linha de título se imagem falhou)
- 5 capítulos com Heading 1 + texto, cada um numa página
- Rodapé com texto institucional
- Margens ABNT (sup/esq 3 cm, inf/dir 2 cm)

Repetir o fluxo para "COT" e verificar que o arquivo baixado é `Minuta_RI_COT_CBMRO.docx`.

- [ ] **Step 6: Commit**

```bash
git add src/pages/MinutaWizard.jsx
git commit -m "feat: wizard MinutaWizard.jsx — 3 etapas com edição inline e download .docx"
```

---

## Task 5: Atualizar `CLAUDE.md`

**Files:**
- Modify: `CLAUDE.md` (seção Comandos)

- [ ] **Step 1: Adicionar linha do novo script**

Na seção `## Comandos` do `CLAUDE.md`, adicionar após a linha `build_dpo_cot_comparison.py`:

```bash
python scripts/build_minuta_structure.py # comparativo_dpo_cot.json -> database/minuta_structure.json
```

Ficará assim no bloco de comandos:

```bash
python scripts/build_organs_detail.py      # detail_data_g*.py + detail_cargos_g*.py -> database/organs_detail/<id>.json
python scripts/build_states_data.py        # database/markdown/*.md + organs_detail/*.json -> database/states_data.json
python scripts/build_dpo_cot_comparison.py # organs_detail/*.json -> database/comparativo_dpo_cot.json (aba "DPO × COT")
python scripts/build_minuta_structure.py   # comparativo_dpo_cot.json -> database/minuta_structure.json (wizard minuta RI)
```

- [ ] **Step 2: Commit**

```bash
git add CLAUDE.md
git commit -m "docs: registra build_minuta_structure.py nos comandos do CLAUDE.md"
```

---

## Verificação final

- [ ] Navegar por todo o fluxo DPO: escolha → 5 seções editadas → download → abrir `.docx`
- [ ] Navegar por todo o fluxo COT: idem
- [ ] Confirmar que editar texto numa seção e voltar (Anterior/Próxima) preserva o texto editado
- [ ] Confirmar que "Voltar e editar" na etapa 3 abre a etapa 2 na última seção com o texto preservado
- [ ] Confirmar que `npm run build` conclui sem erros e que `dist/database/minuta_structure.json` existe
