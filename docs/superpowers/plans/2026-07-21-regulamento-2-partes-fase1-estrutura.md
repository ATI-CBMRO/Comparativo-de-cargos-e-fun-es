# Regulamento Geral em 2 Partes — Fase 1 (estrutura) — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** O Regulamento Geral passa a ser um documento único em 2 Partes (Parte I — Geral; Parte II — do Serviço), com o 16º tema `central-operacoes-193` criado (ainda sem conteúdo, sinalizado "pendente"), visível no wizard `/regulamento` e no `.docx`.

**Architecture:** Um mapa `TEMA_PARTE` no gerador Python carimba cada capítulo com `parte: "geral"|"servico"` e reordena os capítulos (Parte I antes da Parte II). O frontend lê o campo e insere cabeçalhos de Parte no sumário, no corpo do documento e no `.docx`. Nenhuma migração: `editId`s não mudam (comentários do Firebase preservados); o cenário atual herda o campo automaticamente (seu gerador re-carimba o arquivo da futura).

**Tech Stack:** Python 3.12 (venv `.venv-pipeline/`), React/Vite, `node --test`, lib `docx`.

**Spec:** `docs/superpowers/specs/2026-07-21-regulamento-geral-2-partes-design.md`. Fases 2 (conteúdo verbatim por UF) e 3 (curadoria Obsidian) terão planos próprios.

## Global Constraints

- Comunicação e textos de UI em pt-BR.
- Python SEMPRE via `.venv-pipeline/bin/python` (PEP 668 bloqueia o pip do sistema).
- NÃO tocar em `database/atual/organs_detail/ro.json` nem em arquivos da trilha do RI.
- Preservar os 410 artigos e todos os `editId`s existentes do Regulamento (comentários Firebase dependem deles). Reordenar capítulos é permitido; renomear `editId`, não.
- Arquivos da LOB futura ficam na RAIZ de `database/` (não mover).
- `node --test` deve terminar verde em todo commit.
- Bash com caminhos absolutos, sem `cd ... &&` encadeado quando evitável.

---

### Task 1: Camada de dados — 16º tema + campo `parte` + ordenação por Parte

**Files:**
- Modify: `scripts/regulamento_enrichment.py` (THEMES ~linha 14, REGULAMENTO_DOCS ~linha 35, PRIMARY_SOURCE ~linha 50)
- Modify: `scripts/build_regulamento_structure.py` (STATE_NAMES ~linha 26, `build()` ~linha 97 e ~linha 113)
- Modify: `scripts/test_regulamento_structure.py`
- Regenerate: `database/regulamento_structure.json`

**Interfaces:**
- Produces: `regulamento_structure.json` com `chapters[i].parte ∈ {"geral","servico"}`, 16 capítulos ordenados (todos `geral` antes de todos `servico`), 16º tema `central-operacoes-193` com `status: "pendente"` e `articles: []`. Tasks 3–5 dependem do campo `parte` e da ordenação.

- [ ] **Step 1: Escrever as asserções que devem falhar** — em `scripts/test_regulamento_structure.py`, após a linha `assert len(d['chapters']) == len(THEME_KEYS)`, adicionar:

```python
# 2 Partes (spec 2026-07-21): todo capítulo tem parte válida e a ordem é Parte I → Parte II.
for c in d['chapters']:
    assert c.get('parte') in ('geral', 'servico'), f"capítulo sem parte: {c['themeKey']}"
ordem = [c['parte'] for c in d['chapters']]
assert ordem == sorted(ordem, key=lambda p: {'geral': 0, 'servico': 1}[p]), \
    f'capítulo geral depois de servico: {ordem}'
assert 'central-operacoes-193' in [c['themeKey'] for c in d['chapters']]
```

E trocar o bloco final de capítulos vazios por (allowlist explícita — o 16º tema nasce pendente até a Fase 2):

```python
# Nenhum capítulo sem conteúdo primário — exceto os explicitamente pendentes (Fase 2).
PENDENTES_OK = {'central-operacoes-193'}
vazios = [c['themeKey'] for c in d['chapters']
          if not c['articles'] and c['themeKey'] not in PENDENTES_OK]
assert not vazios, f'capítulos sem artigos: {vazios}'
```

E, no fim do arquivo, antes do `print`, adicionar a prova de preservação:

```python
assert len(edit_ids) >= 410, f'regressão: {len(edit_ids)} artigos (esperado >= 410)'
```

- [ ] **Step 2: Rodar o teste e confirmar que FALHA**

Run: `"/Users/wandriobandeira/Projetos de dev Sistemas/05. Comparativo-de-cargos-e-funcoes/.venv-pipeline/bin/python" scripts/test_regulamento_structure.py`
Expected: `AssertionError: capítulo sem parte: disposicoes-preliminares` (o JSON atual não tem o campo).

- [ ] **Step 3: Adicionar o 16º tema e as fontes novas** — em `scripts/regulamento_enrichment.py`:

Em `THEMES`, adicionar como último item da lista:

```python
    ("central-operacoes-193", "Da Central de Operações e do Teledespacho", "Serviços"),
```

Em `REGULAMENTO_DOCS`, adicionar (mesmo formato das entradas existentes; fontes verificadas no round 2 — vault):

```python
    "ba": {"label": "Norma Operacional nº 01/2021 (CBMBA)", "md": "Bahia - Regulamento de Serviço.md"},
    "rr": {"label": "INOp do Serviço Diário dos Oficiais (CBMRR)", "md": "Roraíma - Regulamento de Serviço.md"},
    "to": {"label": "Diretriz Geral do Comando Operacional (Portaria nº 003/2019/COB)", "md": "Tocantins - Regulamento de Serviço.md"},
```

⚠️ O arquivo de RR usa a grafia "Roraíma" (herdada do acervo) — conferir com `ls` antes de fixar.

Em `PRIMARY_SOURCE`, adicionar:

```python
    "central-operacoes-193": "to",  # SIOP/COCB (Anexo 2 da Diretriz) — fonte mais dedicada ao 193; conteúdo entra na Fase 2
```

- [ ] **Step 4: Carimbar `parte` e reordenar no gerador** — em `scripts/build_regulamento_structure.py`:

Após o dicionário `STATE_NAMES`, adicionar os 3 estados novos dentro dele (`'ba': 'Bahia', 'rr': 'Roraima', 'to': 'Tocantins'`) e criar o mapa (12 geral / 4 servico, decisão do Wândrio no spec §3):

```python
# 2 Partes do Regulamento (spec 2026-07-21): Parte I — Geral | Parte II — do Serviço.
TEMA_PARTE = {
    'disposicoes-preliminares': 'geral', 'organizacao-geral': 'geral',
    'competencias-direcao': 'geral', 'competencias-apoio-assessoramento': 'geral',
    'competencias-execucao': 'geral', 'pessoal-quadros': 'geral',
    'ensino-instrucao': 'geral', 'cerimonial-honras': 'geral',
    'disciplina-correicao': 'geral', 'uniformes-apresentacao': 'geral',
    'seguranca-contra-incendio': 'geral', 'disposicoes-finais': 'geral',
    'servico-operacional': 'servico', 'servico-interno-dia': 'servico',
    'atribuicoes-funcoes': 'servico', 'central-operacoes-193': 'servico',
}
```

No `chapters.append({...})`, adicionar a chave (logo após `'themeKey': theme_key,`):

```python
            'parte': TEMA_PARTE[theme_key],
```

Após o loop `for theme_key, ... in THEMES:` (antes de montar `structure`), reordenar:

```python
    # Parte I (geral) antes da Parte II (servico); dentro de cada Parte, ordem dos THEMES.
    _ordem_parte = {'geral': 0, 'servico': 1}
    chapters.sort(key=lambda c: (_ordem_parte[c['parte']], THEME_KEYS.index(c['themeKey'])))
```

Nota de curadoria (não é ação): `disposicoes-finais` fica na Parte I por decisão do spec; se o Wândrio preferir "Disposições Finais" fechando o documento inteiro, é um ajuste de 1 linha na chave de ordenação — sinalizar na entrega, não decidir sozinho.

- [ ] **Step 5: Regenerar e validar**

Run: `"/Users/wandriobandeira/Projetos de dev Sistemas/05. Comparativo-de-cargos-e-funcoes/.venv-pipeline/bin/python" scripts/build_regulamento_structure.py`
Expected: `Capítulos: 16 | artigos propostos: 410 | ...` e `Capítulos pendentes (sem fonte primária): ['central-operacoes-193']`.

Run: `"/Users/wandriobandeira/Projetos de dev Sistemas/05. Comparativo-de-cargos-e-funcoes/.venv-pipeline/bin/python" scripts/test_regulamento_structure.py`
Expected: `OK — scripts/test_regulamento_structure.py (16 capítulos, 410 artigos, ...)`.

- [ ] **Step 6: Commit**

```bash
git add scripts/regulamento_enrichment.py scripts/build_regulamento_structure.py scripts/test_regulamento_structure.py database/regulamento_structure.json
git commit -m "feat(regulamento): 2 Partes (geral × serviço) + 16º tema central-operacoes-193 na camada de dados

Co-Authored-By: Claude <noreply@anthropic.com>"
```

---

### Task 2: Espelho do cenário atual herda o campo `parte`

**Files:**
- Regenerate: `database/atual/regulamento_structure.json` (via `scripts/build_regulamento_structure_atual.py` — NÃO editar o script; ele re-carimba o arquivo da futura e deve herdar `parte` sem mudanças)

**Interfaces:**
- Consumes: `database/regulamento_structure.json` da Task 1 (com `parte`).
- Produces: espelho do atual com os mesmos 16 capítulos/`parte`, ids `reg:atual:`.

- [ ] **Step 1: Regenerar o espelho do atual**

Run: `"/Users/wandriobandeira/Projetos de dev Sistemas/05. Comparativo-de-cargos-e-funcoes/.venv-pipeline/bin/python" scripts/build_regulamento_structure_atual.py`
Expected: `16 temas · 410 artigos (isolados como reg:atual:)` (era 15 — se imprimir 15, o script filtra por lista fixa de temas: investigar antes de prosseguir e reportar, não contornar).

- [ ] **Step 2: Verificar a herança do campo**

Run: `"/Users/wandriobandeira/Projetos de dev Sistemas/05. Comparativo-de-cargos-e-funcoes/.venv-pipeline/bin/python" -c "import json; d=json.load(open('database/atual/regulamento_structure.json')); partes=[c.get('parte') for c in d['chapters']]; assert all(p in ('geral','servico') for p in partes), partes; assert len(d['chapters'])==16; print('OK atual:', len(d['chapters']), 'capítulos com parte')"`
Expected: `OK atual: 16 capítulos com parte`

- [ ] **Step 3: Rodar a suíte completa**

Run: `node --test`
Expected: `tests 107 / pass 107 / fail 0` (nenhum teste JS lê o número de capítulos; se algo quebrar, reportar antes de mexer).

- [ ] **Step 4: Commit**

```bash
git add database/atual/regulamento_structure.json
git commit -m "chore(cenario-atual): regenera espelho do Regulamento com 2 Partes herdadas

Co-Authored-By: Claude <noreply@anthropic.com>"
```

---

### Task 3: Helper puro `regulamentoPartes.js` (TDD)

**Files:**
- Create: `src/lib/regulamentoPartes.js`
- Test: `src/lib/regulamentoPartes.test.js`

**Interfaces:**
- Produces: `PARTE_HEADERS = { geral: 'PARTE I — GERAL', servico: 'PARTE II — DO SERVIÇO' }` e `parteByChapterTitle(structure) -> { [chapterTitle]: 'geral'|'servico' }`. Tasks 4 e 5 importam exatamente esses nomes.

- [ ] **Step 1: Escrever o teste que falha** — criar `src/lib/regulamentoPartes.test.js`:

```js
import test from 'node:test'
import assert from 'node:assert/strict'
import { PARTE_HEADERS, parteByChapterTitle } from './regulamentoPartes.js'

test('PARTE_HEADERS tem os dois rótulos em pt-BR', () => {
  assert.equal(PARTE_HEADERS.geral, 'PARTE I — GERAL')
  assert.equal(PARTE_HEADERS.servico, 'PARTE II — DO SERVIÇO')
})

test('parteByChapterTitle mapeia título→parte e ignora capítulos sem parte (compat RI)', () => {
  const structure = { chapters: [
    { chapterTitle: 'DAS DISPOSIÇÕES PRELIMINARES', parte: 'geral' },
    { chapterTitle: 'DO SERVIÇO OPERACIONAL', parte: 'servico' },
    { chapterTitle: 'CAPÍTULO SEM PARTE' },
  ] }
  assert.deepEqual(parteByChapterTitle(structure), {
    'DAS DISPOSIÇÕES PRELIMINARES': 'geral',
    'DO SERVIÇO OPERACIONAL': 'servico',
  })
})

test('parteByChapterTitle é seguro com estrutura vazia/nula', () => {
  assert.deepEqual(parteByChapterTitle(null), {})
  assert.deepEqual(parteByChapterTitle({}), {})
})
```

- [ ] **Step 2: Rodar e confirmar que FALHA**

Run: `node --test src/lib/regulamentoPartes.test.js`
Expected: FAIL — `Cannot find module ... regulamentoPartes.js`.

- [ ] **Step 3: Implementar o helper** — criar `src/lib/regulamentoPartes.js`:

```js
// 2 Partes do Regulamento (spec 2026-07-21). Compartilhado por RegulamentoWizard e
// minutaDocx; estruturas SEM o campo `parte` (ex.: RI) resultam em mapa vazio → no-op.
export const PARTE_HEADERS = {
  geral: 'PARTE I — GERAL',
  servico: 'PARTE II — DO SERVIÇO',
}

export function parteByChapterTitle(structure) {
  const map = {}
  for (const ch of structure?.chapters ?? []) {
    if (ch.parte) map[ch.chapterTitle] = ch.parte
  }
  return map
}
```

- [ ] **Step 4: Rodar e confirmar que PASSA (e a suíte inteira)**

Run: `node --test`
Expected: `tests 110 / pass 110 / fail 0` (107 + 3 novos).

- [ ] **Step 5: Commit**

```bash
git add src/lib/regulamentoPartes.js src/lib/regulamentoPartes.test.js
git commit -m "feat(regulamento): helper regulamentoPartes (título→parte + rótulos das 2 Partes)

Co-Authored-By: Claude <noreply@anthropic.com>"
```

---

### Task 4: Wizard — sumário agrupado por Parte + faixas no corpo do documento

**Files:**
- Modify: `src/pages/RegulamentoWizard.jsx` (imports ~linha 3; sumário ~linha 352 `data.chapters.map`; corpo ~linha 393 `articles.map`)

**Interfaces:**
- Consumes: `PARTE_HEADERS`, `parteByChapterTitle` (Task 3); `chapters[i].parte` (Task 1).
- Produces: UI — nada exportado.

- [ ] **Step 1: Importar o helper** — junto aos imports de `../lib/`:

```js
import { PARTE_HEADERS, parteByChapterTitle } from '../lib/regulamentoPartes.js'
```

- [ ] **Step 2: Sumário agrupado** — substituir o bloco `{data.chapters.map(ch => (...))}` do `<nav>` por:

```jsx
              {['geral', 'servico'].map(parte => {
                const caps = data.chapters.filter(ch => ch.parte === parte)
                if (!caps.length) return null
                return (
                  <div key={parte} style={{ marginBottom: 10 }}>
                    <div style={{ fontWeight: 800, color: 'var(--cbm-red-700)', fontSize: 10.5, letterSpacing: 0.5, margin: '6px 0 4px' }}>
                      {PARTE_HEADERS[parte]}
                    </div>
                    {caps.map(ch => (
                      <div key={ch.id} style={{ marginBottom: 4 }}>
                        <button onClick={() => scrollTo(chapterIdOf(ch.articles[0]?.editId ?? ch.id))} style={{
                          border: 'none', background: 'none', padding: '2px 0', textAlign: 'left', cursor: 'pointer',
                          color: 'var(--navy-850)', fontWeight: 600, fontSize: 12.5,
                        }}>{ch.chapterTitle}{ch.status === 'pendente' ? ' ⏳' : ''}</button>
                      </div>
                    ))}
                  </div>
                )
              })}
```

(Fallback implícito: se nenhum capítulo tiver `parte`, os dois filtros voltam vazios — nesse caso restaurar o map plano é desnecessário porque o JSON da Task 1 sempre tem `parte`; capítulos sem `parte` não existem mais no Regulamento.)

- [ ] **Step 3: Faixas de Parte no corpo** — antes do `return` do componente (junto aos outros `useMemo`), criar:

```js
  const parteDe = useMemo(() => parteByChapterTitle(data), [data])
```

E substituir `{articles.map(art => <div key={art.number} style={{ marginBottom: 8 }}>{renderArticle(art)}</div>)}` por:

```jsx
                {(() => {
                  let ultimaParte = null
                  return articles.map(art => {
                    const parte = art.chapterTitle ? parteDe[art.chapterTitle] : null
                    const faixa = parte && parte !== ultimaParte ? PARTE_HEADERS[parte] : null
                    if (parte) ultimaParte = parte
                    return (
                      <div key={art.number} style={{ marginBottom: 8 }}>
                        {faixa && (
                          <div style={{
                            textAlign: 'center', fontWeight: 800, fontSize: 16, letterSpacing: 1,
                            color: 'var(--cbm-red-700)', borderTop: '2px solid var(--cbm-red-700)',
                            borderBottom: '2px solid var(--cbm-red-700)', padding: '10px 0', margin: '26px 0 18px',
                          }}>{faixa}</div>
                        )}
                        {renderArticle(art)}
                      </div>
                    )
                  })
                })()}
```

- [ ] **Step 4: Verificar build e suíte**

Run: `npm run build`
Expected: build verde, sem erro de import/JSX.
Run: `node --test`
Expected: `pass 110 / fail 0`.

- [ ] **Step 5: Commit**

```bash
git add src/pages/RegulamentoWizard.jsx
git commit -m "feat(regulamento): wizard exibe as 2 Partes (sumário agrupado + faixas no documento)

Co-Authored-By: Claude <noreply@anthropic.com>"
```

---

### Task 5: `.docx` com as faixas de Parte

**Files:**
- Modify: `src/lib/minutaDocx.js` (imports ~linha 6; loop `articles.forEach` ~linha 41)

**Interfaces:**
- Consumes: `PARTE_HEADERS`, `parteByChapterTitle` (Task 3). Guardado: estruturas sem `parte` (RI) geram docx idêntico ao de hoje.

- [ ] **Step 1: Importar e indexar** — junto ao import de `minutaArticles.js`:

```js
import { PARTE_HEADERS, parteByChapterTitle } from './regulamentoPartes.js'
```

Dentro de `buildMinutaBlob`, antes de `const articles = buildArticles(...)`:

```js
  const parteDe = parteByChapterTitle(structure)
  let ultimaParte = null
```

- [ ] **Step 2: Emitir a faixa no loop** — dentro de `articles.forEach(art => {`, como PRIMEIRA coisa do `if (art.chapterTitle) {` (a faixa abre a página; o CAPÍTULO logo abaixo NÃO deve quebrar de novo — daí o `!novaParte`):

```js
      const parte = parteDe[art.chapterTitle]
      const novaParte = Boolean(parte) && parte !== ultimaParte
      if (novaParte) {
        children.push(new Paragraph({
          alignment: AlignmentType.CENTER, pageBreakBefore: chapterSeen,
          spacing: { before: 240, after: 240 },
          children: [new TextRun({ text: PARTE_HEADERS[parte], bold: true, font: 'Times New Roman', size: 30 })],
        }))
        ultimaParte = parte
      }
```

E, no parágrafo já existente do `CAPÍTULO ${romanize(...)}` (linha ~46), trocar `pageBreakBefore: chapterSeen` por:

```js
          pageBreakBefore: chapterSeen && !novaParte,
```

- [ ] **Step 3: Verificar que o RI não muda** — o guard `if (parte ...)` é falso para o RI (sem campo `parte`). Prova rápida:

Run: `node --test`
Expected: `pass 110 / fail 0`.
Run: `npm run build`
Expected: verde.

- [ ] **Step 4: Commit**

```bash
git add src/lib/minutaDocx.js
git commit -m "feat(regulamento): .docx sai com as faixas PARTE I/PARTE II (no-op para o RI)

Co-Authored-By: Claude <noreply@anthropic.com>"
```

---

### Task 6: Prova visual + preservação + registro

**Files:**
- Modify: `.claude/PENDENCIAS.md` (registrar Fase 1 concluída + Fases 2/3 pendentes)
- Evidence: screenshots Playwright de `/regulamento` (cenários futura E atual)

**Interfaces:**
- Consumes: tudo das Tasks 1–5.

- [ ] **Step 1: Subir o dev server e capturar evidência (regra dura do crachá: prova antes de "pronto")**

Run: `npm run dev` (porta 5173) e, via Playwright MCP: navegar até `http://localhost:5173/regulamento?cenario=futura`, avançar para "Revisar e curar a minuta", capturar screenshot mostrando a faixa **PARTE I — GERAL** no topo e (rolando) a faixa **PARTE II — DO SERVIÇO**; repetir com `?cenario=atual`. Guardar os 2 screenshots e ABRI-los no Preview.
Expected: as duas faixas visíveis nos dois cenários; sumário agrupado; tema "Da Central de Operações e do Teledespacho" listado com ⏳.

- [ ] **Step 2: Prova de preservação (números ao centavo)**

Run: `"/Users/wandriobandeira/Projetos de dev Sistemas/05. Comparativo-de-cargos-e-funcoes/.venv-pipeline/bin/python" -c "import json; d=json.load(open('database/regulamento_structure.json')); ids=[a['editId'] for c in d['chapters'] for a in c['articles']]; print('artigos:', len(ids), '| únicos:', len(set(ids)))"`
Expected: `artigos: 410 | únicos: 410` — colar a saída na mensagem de entrega, junto do `git diff --stat` mostrando que nenhum arquivo do RI foi tocado.

- [ ] **Step 3: Registrar no backlog** — em `.claude/PENDENCIAS.md`, mover para "Concluído (mês atual)": `Regulamento em 2 Partes — Fase 1 (estrutura)`; adicionar em "Pendente": `Fase 2 — conteúdo verbatim das fontes novas (BA, RR, TO, AL, RS Cap VI, ES, RISG caserna) + preencher central-operacoes-193`, `Fase 3 — curadoria no Obsidian (notas por tema/artigo com backlinks)` e `Herdar a divisão em 2 Partes nas telas Subsídio/Diagramas/Revisão do Regulamento (spec §5.4 — fora da Fase 1)`.

- [ ] **Step 4: Commit final**

```bash
git add .claude/PENDENCIAS.md
git commit -m "chore(handoff): registra Regulamento 2 Partes Fase 1 concluída; Fases 2-3 pendentes

Co-Authored-By: Claude <noreply@anthropic.com>"
```

- [ ] **Step 5: Entregar com /abrir-app** — invocar a skill `abrir-app` para entregar o link verificado ao Wândrio, com os screenshots lado a lado.
