# Regulamento de Serviço — 2ª rodada de curadoria: Plano de Implementação

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Corrigir 6 problemas de conteúdo da minuta do Regulamento de Serviço (terminologia de escala de serviço, ordem de capítulos, resíduos de CIOP, remissões a normas próprias do CBMRO e o escopo do Capítulo V), valendo nos perfis admin e participante.

**Architecture:** Toda mudança de CONTEÚDO passa pela camada de reescrita autoral já existente (`scripts/regulamento_reescrita.py`), consumida por `scripts/build_regulamento_structure.py`. O JSON do cenário atual é derivação pura da futura (`build_regulamento_structure_atual.py` só re-carimba ids), então **basta rodar os dois builders na ordem** para propagar. A única mudança de FRONTEND é o filtro de escopo (`src/lib/escopoServico.js`), que ganha capacidade de filtrar artigos dentro de um capítulo.

**Tech Stack:** Python 3.10+ (scripts do pipeline, sem dependências novas), JavaScript ES modules + `node:test` (lógica de frontend), React 18 (telas).

**Spec:** `docs/superpowers/specs/2026-08-18-regulamento-servico-correcoes-fase2-design.md`

## Global Constraints

Valores copiados literalmente da spec — valem para **todas** as tarefas:

- **Ordem obrigatória dos builders:** `python scripts/build_regulamento_structure.py` **antes** de `python scripts/build_regulamento_structure_atual.py`. O segundo lê o JSON gerado pelo primeiro; inverter propaga conteúdo defasado em silêncio.
- **Python**: usar `python` direto (Windows). No Mac seria `.venv-pipeline/bin/python`.
- **`scripts/test_regulamento_structure.py` linha 90:** `assert len(autorais) == 40` é contagem **exata**. Toda tarefa que acrescenta artigo autoral DEVE atualizar esse número **e** o comentário de aritmética das linhas 72-87.
- **`fundamento` de artigo autoral** passa por allowlist (linhas 38-44). Normas aceitas hoje: `Lei nº 2.204/2009`, `LOB`, `Decreto nº 21.425/2016`, `Lei estadual nº 3.924/2016`, `organograma oficial`, `NGA-CIOP-001/2026`.
- **`leaf['source'] == leaf['fundamento']`** para artigo autoral — o builder já faz isso; não duplicar manualmente.
- **`caput` nunca começa com "Art."** — a numeração da minuta é contínua e própria.
- **`atribuicoes-funcoes` NÃO entra em `SUBSTITUI_INTEGRALMENTE`** — é capítulo misto por decisão de escopo (COB/CAT reescritos + demais órgãos preservados).
- **Nunca editar JSON gerado à mão.** Editar `regulamento_reescrita.py` / `escopoServico.js` e reexecutar.
- **`database/atual/organs_detail/ro.json` é fonte da verdade** da estrutura vigente; não é tocado por este plano.
- **Documentos de apoio:** `LEGISLAÇÃO CBMS/Manuais/` (pasta não versionada, fora do Acervo Legal de propósito).
- **Idioma:** todo texto de norma, comentário de código e mensagem de commit em português do Brasil.

---

## Estrutura de arquivos

| Arquivo | Responsabilidade | Tarefas |
|---|---|---|
| `src/lib/escopoServico.js` | Lista/ordem dos capítulos do recorte + filtro (ganha filtro por artigo) | 1, 2 |
| `src/lib/escopoServico.test.js` | Testes do recorte | 1, 2 |
| `docs/curadoria/depara-supervisor-de-dia.md` | **Criar** — de-para artigo a artigo, para aprovação do Ten. Tiago | 3 |
| `scripts/regulamento_reescrita.py` | Camada de reescrita: remoções e artigos autorais | 4, 5, 6, 7, 8 |
| `scripts/test_regulamento_structure.py` | Contagens e invariantes da estrutura | 5, 6, 7, 8 |
| `src/components/NotaEscopoServico.jsx` | Nota de escopo do recorte | 9 |

---

### Task 1: Reordenar o Capítulo V no recorte

Move `atribuicoes-funcoes` para logo após `disposicoes-preliminares` na ordem de leitura do recorte. Mudança isolada de uma lista — nenhum builder roda nesta tarefa.

**Files:**
- Modify: `src/lib/escopoServico.js:9-17`
- Test: `src/lib/escopoServico.test.js:31-41`

**Interfaces:**
- Consumes: nada.
- Produces: `TEMAS_SERVICO` na nova ordem — Task 2 depende dela para os testes de filtro.

- [ ] **Step 1: Atualizar o teste de ordem para a ordem nova**

Em `src/lib/escopoServico.test.js`, substituir o corpo do teste `'TEMAS_SERVICO tem os 7 temas do recorte, na ordem de leitura'`:

```javascript
test('TEMAS_SERVICO tem os 7 temas do recorte, na ordem de leitura', () => {
  assert.deepEqual(TEMAS_SERVICO, [
    'disposicoes-preliminares',
    'atribuicoes-funcoes',
    'servico-operacional',
    'central-operacoes-193',
    'servico-interno-dia',
    'seguranca-contra-incendio',
    'disposicoes-finais',
  ])
})
```

- [ ] **Step 2: Rodar o teste e confirmar que falha**

```bash
npm test
```

Esperado: FALHA no teste de ordem, com diff mostrando `atribuicoes-funcoes` na posição 5 em vez da 2.

- [ ] **Step 3: Aplicar a nova ordem**

Em `src/lib/escopoServico.js`, substituir o array `TEMAS_SERVICO` e o comentário acima dele:

```javascript
// ATENÇÃO: esta lista é a ORDEM do documento recortado, não só o filtro. NÃO é a ordem
// do arquivo: no regulamento_structure.json a Parte I vem inteira antes da Parte II, de
// modo que "DAS DISPOSIÇÕES FINAIS" (posição 12) precede o serviço operacional (13).
// Preservar a ordem do arquivo jogaria o fecho do regulamento para o meio do documento.
// Ordem escolhida: Preliminares e Finais nas pontas; as ATRIBUIÇÕES DAS FUNÇÕES logo
// após as Preliminares (determinação do Ten. Tiago, 2026-08-18 — quem lê o regulamento de
// serviço precisa saber QUEM faz o quê antes de ler o serviço em si); depois o serviço
// operacional do COB, a Central de Operações, o serviço interno e o serviço técnico da CAT.
// O documento COMPLETO não é reordenado nesta rodada: lá as Preliminares abrem a Parte I e
// este capítulo é Parte II — a posição dele entra na reordenação geral da 2ª etapa.
export const TEMAS_SERVICO = [
  'disposicoes-preliminares',
  'atribuicoes-funcoes',
  'servico-operacional',
  'central-operacoes-193',
  'servico-interno-dia',
  'seguranca-contra-incendio',
  'disposicoes-finais',
]
```

- [ ] **Step 4: Rodar os testes e confirmar que passam**

```bash
npm test
```

Esperado: PASSA — inclusive `'REORDENA: Preliminares abre e Disposições Finais fecha'`, que compara contra `TEMAS_SERVICO` e portanto acompanha a mudança automaticamente.

- [ ] **Step 5: Commit**

```bash
git add src/lib/escopoServico.js src/lib/escopoServico.test.js
git commit -m "feat(regulamento): move as Atribuicoes das Funcoes para o inicio do recorte

Determinacao do Ten. Tiago (2026-08-18): quem le o Regulamento de Servico
precisa saber QUEM faz o que antes de ler o servico em si. O documento
completo nao e reordenado nesta rodada — la o capitulo e Parte II e a
posicao dele entra na reordenacao geral da 2a etapa.

Co-Authored-By: Claude Opus 5 <noreply@anthropic.com>"
```

---

### Task 2: Filtro por artigo dentro do capítulo

Hoje `filtrarEstruturaPorEscopo` só corta capítulos inteiros. O Capítulo V passa a ser misto (COB/CAT no recorte; demais órgãos só no documento completo), então o filtro precisa saber cortar artigos. Tarefa de lógica pura — nenhum dado real muda ainda.

**Files:**
- Modify: `src/lib/escopoServico.js`
- Test: `src/lib/escopoServico.test.js`

**Interfaces:**
- Consumes: `TEMAS_SERVICO` (Task 1), `temaDoCapitulo(id)`.
- Produces: constante `ORGAOS_NO_ESCOPO = { servico: ['cob', 'cat'] }` e o comportamento novo de `filtrarEstruturaPorEscopo`: em capítulos listados em `TEMAS_COM_FILTRO_DE_ORGAO`, mantém só artigos cujo campo `orgao` esteja no escopo. Task 8 grava esse campo `orgao` nos artigos.

- [ ] **Step 1: Escrever os testes que falham**

Acrescentar em `src/lib/escopoServico.test.js`, ao final do arquivo:

```javascript
// --- Filtro por ARTIGO dentro do capítulo (Capítulo V misto, 2026-08-18) ---
// O capítulo das Atribuições das Funções passa a conter dois níveis de curadoria: os
// artigos de COB/CAT (reescritos sobre a LOB de RO) e os demais órgãos (ainda transplante
// de MT, que só o documento completo mostra).
const comCapituloMisto = () => ({
  title: 'Regulamento Geral',
  chapters: [
    { id: 'reg:atual:disposicoes-preliminares', parte: 'geral', articles: [{ editId: 'a1' }] },
    {
      id: 'reg:atual:atribuicoes-funcoes',
      parte: 'servico',
      articles: [
        { editId: 'cob-1', orgao: 'cob' },
        { editId: 'mt-art-62' },              // sem tag: órgão fora do escopo
        { editId: 'cat-1', orgao: 'cat' },
        { editId: 'mt-art-63', orgao: 'emg' }, // tag de órgão fora do escopo
      ],
    },
    { id: 'reg:atual:disposicoes-finais', parte: 'geral', articles: [{ editId: 'z1' }] },
  ],
})

test('no capítulo misto, mantém só os artigos de COB e CAT', () => {
  const r = filtrarEstruturaPorEscopo(comCapituloMisto(), 'servico')
  const cap = r.chapters.find(c => temaDoCapitulo(c.id) === 'atribuicoes-funcoes')
  assert.deepEqual(cap.articles.map(a => a.editId), ['cob-1', 'cat-1'])
})

test('capítulo NÃO listado para filtro de órgão mantém todos os artigos', () => {
  const r = filtrarEstruturaPorEscopo(comCapituloMisto(), 'servico')
  const prelim = r.chapters.find(c => temaDoCapitulo(c.id) === 'disposicoes-preliminares')
  assert.equal(prelim.articles.length, 1, 'Preliminares não sofre filtro por órgão')
})

test('filtro por artigo não muta a estrutura original', () => {
  const original = comCapituloMisto()
  filtrarEstruturaPorEscopo(original, 'servico')
  const cap = original.chapters.find(c => temaDoCapitulo(c.id) === 'atribuicoes-funcoes')
  assert.equal(cap.articles.length, 4, 'a estrutura original não pode ser alterada')
})

test('sem escopo, o capítulo misto sai inteiro (visão do documento completo)', () => {
  const original = comCapituloMisto()
  assert.equal(filtrarEstruturaPorEscopo(original, null), original)
})

test('capítulo misto sem o campo articles não quebra o filtro', () => {
  const semArtigos = comCapituloMisto()
  const cap = semArtigos.chapters.find(c => temaDoCapitulo(c.id) === 'atribuicoes-funcoes')
  delete cap.articles
  const r = filtrarEstruturaPorEscopo(semArtigos, 'servico')
  const capFiltrado = r.chapters.find(c => temaDoCapitulo(c.id) === 'atribuicoes-funcoes')
  assert.equal(capFiltrado.articles, undefined)
})
```

- [ ] **Step 2: Rodar os testes e confirmar que falham**

```bash
npm test
```

Esperado: FALHA nos 2 primeiros testes novos — hoje o capítulo sai com os 4 artigos, porque o filtro só corta capítulos.

- [ ] **Step 3: Implementar o filtro por artigo**

Em `src/lib/escopoServico.js`, logo após `export const ESCOPOS = { servico: TEMAS_SERVICO }`, acrescentar:

```javascript
// Capítulos MISTOS: contêm artigos de vários órgãos e, no recorte, só os do escopo devem
// aparecer. Hoje só o das Atribuições das Funções — nele os artigos de COB/CAT foram
// reescritos sobre a LOB de RO, e os dos demais órgãos seguem sendo o transplante de MT,
// que pertence ao Regulamento Geral completo (decisão do Ten. Tiago, 2026-08-18).
const TEMAS_COM_FILTRO_DE_ORGAO = new Set(['atribuicoes-funcoes'])

// Órgãos que o recorte de serviço cobre: o serviço operacional é do COB, o serviço técnico
// de segurança contra incêndio é da CAT.
export const ORGAOS_NO_ESCOPO = { servico: ['cob', 'cat'] }

// Artigo sem o campo `orgao` NÃO entra no recorte: a ausência de tag significa "órgão que
// esta rodada de curadoria não cobriu". Fail-closed de propósito — deixar passar o que não
// foi classificado é como o transplante de MT vazou para a pauta do participante.
function filtrarArtigosPorOrgao(capitulo, orgaos) {
  if (!Array.isArray(capitulo.articles)) return capitulo
  return { ...capitulo, articles: capitulo.articles.filter(a => orgaos.includes(a?.orgao)) }
}
```

Depois substituir a função `filtrarEstruturaPorEscopo` inteira por:

```javascript
// Devolve a estrutura com os capítulos do escopo, NA ORDEM de TEMAS_SERVICO, e — nos
// capítulos mistos — só com os artigos dos órgãos do escopo.
// Escopo nulo/desconhecido, ou estrutura sem chapters: devolve o que veio, intacto —
// quem não tem escopo não é afetado por nada disto.
export function filtrarEstruturaPorEscopo(structure, escopo) {
  const temas = ESCOPOS[escopo]
  if (!temas || !Array.isArray(structure?.chapters)) return structure
  const orgaos = ORGAOS_NO_ESCOPO[escopo] ?? []
  const porTema = new Map()
  for (const c of structure.chapters) porTema.set(temaDoCapitulo(c.id), c)
  const chapters = temas
    .map(t => {
      const capitulo = porTema.get(t)
      if (!capitulo) return null
      return TEMAS_COM_FILTRO_DE_ORGAO.has(t)
        ? filtrarArtigosPorOrgao(capitulo, orgaos)
        : capitulo
    })
    .filter(Boolean)
  return { ...structure, chapters }
}
```

- [ ] **Step 4: Rodar os testes e confirmar que passam**

```bash
npm test
```

Esperado: PASSA, todos — inclusive os antigos, porque estruturas-fake sem campo `articles` continuam devolvidas intactas.

- [ ] **Step 5: Commit**

```bash
git add src/lib/escopoServico.js src/lib/escopoServico.test.js
git commit -m "feat(regulamento): filtra artigos por orgao dentro do capitulo misto

O capitulo das Atribuicoes das Funcoes passa a ter dois niveis de curadoria
convivendo: COB/CAT reescritos sobre a LOB de RO (visiveis no recorte) e os
demais orgaos ainda em transplante de MT (so no Regulamento Geral completo).
O filtro de escopo, que so sabia cortar capitulos inteiros, ganha corte por
artigo. Artigo sem tag de orgao nao entra no recorte — fail-closed, porque
foi justamente o nao-classificado que vazou para a pauta do participante.

Co-Authored-By: Claude Opus 5 <noreply@anthropic.com>"
```

---

### Task 3: Análise do de-para "Supervisor de Dia" (sem mudar código)

Produz o documento de curadoria que o Ten. Tiago vai aprovar antes de qualquer edição de norma. **Não altera dados nem código** — é a tarefa que impede a Task 4 de virar find-replace cego.

**Files:**
- Create: `docs/curadoria/depara-supervisor-de-dia.md`

**Interfaces:**
- Consumes: nada.
- Produces: para cada um dos 12 artigos, a decisão `Oficial de Dia` | `Superior de Dia` | `suprimir` | `reescrever cadeia`, que a Task 4 aplica literalmente.

- [ ] **Step 1: Extrair os 12 artigos com o termo**

```bash
node -e "
const fs=require('fs');
const j=JSON.parse(fs.readFileSync('database/atual/regulamento_structure.json','utf8'));
const c=j.chapters.find(x=>x.themeKey==='servico-operacional');
for (const a of c.articles) {
  const itens=(a.items||[]).map(i=>typeof i==='string'?i:(i.text||''));
  const blob=[a.caput||'', ...itens].join(' ');
  if (/Supervisor de Dia/i.test(blob)) {
    console.log('=== '+a.id+' ===');
    console.log('CAPUT: '+(a.caput||'').replace(/\s+/g,' '));
    itens.forEach((t,ix)=>{ if(/Supervisor de Dia/i.test(t)) console.log('  ['+ix+'] '+t.replace(/\s+/g,' ')); });
  }
}
"
```

Esperado: os 12 artigos `se-art-4, 24, 32, 33, 34, 35, 38, 113, 114, 116, 132, 145`.

- [ ] **Step 2: Escrever o documento de de-para**

Criar `docs/curadoria/depara-supervisor-de-dia.md` com este cabeçalho e uma linha por artigo:

```markdown
# De-para: "Supervisor de Dia" → figuras reais do CBMRO

**Data:** 2026-08-18
**Spec:** `docs/superpowers/specs/2026-08-18-regulamento-servico-correcoes-fase2-design.md`
**Status:** aguardando aprovação do Ten. Tiago

## O problema

A fonte do capítulo `servico-operacional` é o RISD do CBM de Sergipe, que tem **três**
figuras de escala: Superior de Dia, Supervisor de Dia e Oficial de Dia. O CBMRO tem
**duas**. A prova está em `se-art-4`, a lista-mestra das 15 funções do serviço diário,
que traz as três lado a lado (incisos I, II e V) — por isso renomear
"Supervisor"→"Oficial" criaria duplicata dentro da própria lista.

## As duas figuras reais (definição do Ten. Tiago, 2026-08-18)

| Figura | Posto | Escala | Área |
|---|---|---|---|
| **Oficial de Dia** | subalterno ou intermediário | serviço operacional no 1º GBM, só oficiais lotados na capital | local (Porto Velho) |
| **Superior de Dia** | oficial superior lotado na capital | sobreaviso | **todo o território estadual**, ocorrências de grande vulto |

Cadeia de acionamento do Superior de Dia:
Comandante de SGBM → Comandante de GBM → Comandante de COB → Superior de Dia.

## Critério

Decide-se pela **área de atuação e natureza da escala**, nunca pelo nome:
presencial e local → Oficial de Dia; sobreaviso e estadual → Superior de Dia.

## Decisões artigo a artigo

| Artigo | Trecho (resumo) | Decisão | Justificativa |
|---|---|---|---|
| `se-art-4` | inciso II da lista de funções | **suprimir o inciso** | a lista já tem Superior de Dia (I) e Oficial de Dia (V); a figura intermediária não existe no CBMRO |
| `se-art-24` | Superior de Dia informa meio de contato "ao Supervisor de Dia"; visto no livro de registro | **Oficial de Dia** | é o militar presente no quartel que recebe a informação e mantém o livro |
| `se-art-32` | "regime adequado de 24 horas, podendo em casos excepcionais ser de 12" | **Oficial de Dia** | escala presencial de 24h é a do Oficial de Dia; o Superior é sobreaviso (`se-art-24`) |
| `se-art-33` | permuta de escala mediante autorização escrita | **Oficial de Dia** | acompanha `se-art-32` |
| `se-art-34` | serviço "coordenado pelo COB, através da sua Seção de Recursos Humanos" | **Oficial de Dia**, conferir o órgão | o COB não tem "Seção de Recursos Humanos" na LOB Art. 35, §1º — tem **Seção de Pessoal**; corrigir junto |
| `se-art-35` | publicação da escala com titular e reserva | **Oficial de Dia** | acompanha `se-art-32` |
| `se-art-38` | "área de atuação abrange todo o território estadual" | **Superior de Dia** | área estadual é, por definição, do Superior de Dia — atribuir ao Oficial de Dia contradiria `se-art-32`/`34`. **Corrigir também o resíduo de extração**: o caput termina com o título de seção "Oficial de Dia" grudado nele |
| `se-art-113` | entrevista "pelo Comandante de Socorro ou Superior ou Supervisor de Dia"; casos omissos | **reescrever cadeia** | ver Task 6 (mídia): o artigo inteiro passa a remeter à Resolução 121/2022 |
| `se-art-114` | casos omissos: "Cmt do SOS em conjunto com o Supervisor de Dia... acionar o Superior de Dia" | **reescrever cadeia** | trocar pelo escalonamento real: Cmt SGBM → Cmt GBM → Cmt COB → Superior de Dia |
| `se-art-116` | idem, pacientes com distúrbios mentais | **reescrever cadeia** | idem `se-art-114` |
| `se-art-132` | presença obrigatória em ocorrência com duas ou mais Unidades Operacionais | **Oficial de Dia** | ocorrência local com múltiplas unidades; grande vulto aciona o Superior por `se-art-38` |
| `se-art-145` | decide emprego de recurso humano extraordinário | **Oficial de Dia** | decisão operacional imediata, do militar de serviço presente |
```

- [ ] **Step 3: Commit do documento**

```bash
git add docs/curadoria/depara-supervisor-de-dia.md
git commit -m "docs(curadoria): de-para do Supervisor de Dia para as figuras reais do CBMRO

A fonte (RISD de Sergipe) tem tres figuras de escala e o CBMRO tem duas —
se-art-4 traz as tres lado a lado, o que descarta renomeacao global. Documenta
a decisao artigo a artigo pelo criterio de area de atuacao (local/presencial =
Oficial de Dia; estadual/sobreaviso = Superior de Dia), para aprovacao antes
de qualquer edicao de norma.

Co-Authored-By: Claude Opus 5 <noreply@anthropic.com>"
```

- [ ] **Step 4: PARAR e pedir aprovação**

Apresentar a tabela ao Ten. Tiago e **aguardar aprovação explícita**. Registrar no documento (trocando o `Status:` para `aprovado em <data>`) antes de seguir para a Task 4. Alterações pedidas viram edição do documento e nova conferência.

---

### Task 4: Aplicar o de-para de terminologia

Aplica as decisões aprovadas na Task 3. Só entra depois do aval.

**Files:**
- Modify: `scripts/regulamento_reescrita.py`
- Verify: `database/atual/regulamento_structure.json` (gerado)

**Interfaces:**
- Consumes: decisões aprovadas em `docs/curadoria/depara-supervisor-de-dia.md`.
- Produces: capítulo `servico-operacional` sem nenhuma ocorrência de "Supervisor de Dia".

- [ ] **Step 1: Acrescentar o mecanismo de substituição de termo por artigo**

`REMOVER_INCISOS` e `SUBSTITUI_INTEGRALMENTE` não servem: aqui o artigo continua válido e só o termo muda. Acrescentar em `scripts/regulamento_reescrita.py`, ao final do arquivo:

```python
# ── (d) SUBSTITUIÇÃO DE TERMO POR ARTIGO ─────────────────────────────────────────────
# Diferente da tabela ADAPTATIONS (regulamento_enrichment.py), que troca um termo em TODO
# o documento: aqui a mesma expressão vira coisas diferentes conforme o artigo, porque a
# fonte (RISD de Sergipe) tem TRÊS figuras de escala e o CBMRO tem duas. Ver o de-para
# aprovado em docs/curadoria/depara-supervisor-de-dia.md.
#
# O casamento é por TEXTO, não por índice — mesma razão de REMOVER_INCISOS (armadilha
# AR-03 do catálogo: índice posicional dessincroniza em silêncio quando a lista muda).
SUBSTITUIR_TERMOS = {
    'servico-operacional': {
        'se-art-24': [('Supervisor de Dia', 'Oficial de Dia')],
        'se-art-32': [('Supervisor de Dia', 'Oficial de Dia')],
        'se-art-33': [('Supervisor de Dia', 'Oficial de Dia')],
        'se-art-34': [('Supervisor de Dia', 'Oficial de Dia'),
                      ('Seção de Recursos Humanos', 'Seção de Pessoal')],
        'se-art-35': [('Supervisor de Dia', 'Oficial de Dia')],
        'se-art-38': [('Supervisor de Dia', 'Superior de Dia')],
        'se-art-132': [('Supervisor de Dia', 'Oficial de Dia')],
        'se-art-145': [('Supervisor de Dia', 'Oficial de Dia')],
    },
}
```

- [ ] **Step 2: Acrescentar a supressão do inciso da lista-mestra e a reescrita das cadeias**

No mesmo arquivo, acrescentar a `REMOVER_INCISOS` a entrada de `servico-operacional`:

```python
    'servico-operacional': {
        # A figura do Supervisor de Dia não existe no CBMRO: a lista-mestra das funções do
        # serviço diário já traz Superior de Dia (inciso I) e Oficial de Dia (inciso V).
        'se-art-4': ['Supervisor de Dia'],
    },
```

E às cadeias de escalonamento (`se-art-114` e `se-art-116`), que citam a figura como elo
intermediário, aplicar substituição pela cadeia real:

```python
# acrescentar dentro de SUBSTITUIR_TERMOS['servico-operacional']:
        'se-art-114': [
            ('Cmt do SOS em conjunto com o Supervisor de Dia, devendo se necessário, '
             'acionar o Superior de Dia e ou o Comando Operacional',
             'Comandante do socorro, que os submeterá, sucessivamente, ao Comandante do '
             'Subgrupamento, ao Comandante do Grupamento e ao Comandante Operacional de '
             'Bombeiros, acionando-se o Superior de Dia quando a ocorrência for de grande vulto'),
        ],
        'se-art-116': [
            ('Cmt do SOS em conjunto com o Supervisor de Dia, devendo se necessário, '
             'acionar o Superior de Dia ou o Comandante da OB M e/ou o Comandante '
             'Operacional de Bombeiros',
             'Comandante do socorro, que os submeterá, sucessivamente, ao Comandante do '
             'Subgrupamento, ao Comandante do Grupamento e ao Comandante Operacional de '
             'Bombeiros, acionando-se o Superior de Dia quando a ocorrência for de grande vulto'),
        ],
```

- [ ] **Step 3: Ligar `SUBSTITUIR_TERMOS` ao builder**

Em `scripts/build_regulamento_structure.py`, acrescentar `SUBSTITUIR_TERMOS` ao import da
linha 22-23, e aplicá-lo ao `caput` e aos `items` de cada artigo primário, **depois** da
adaptação de termos e **antes** de gravar o artigo. O texto original preservado em
`original_caput` não é tocado.

- [ ] **Step 4: Regerar os dois JSONs**

```bash
python scripts/build_regulamento_structure.py && python scripts/build_regulamento_structure_atual.py
```

- [ ] **Step 5: Conferir que o termo sumiu**

```bash
node -e "
const fs=require('fs');
for (const f of ['database/regulamento_structure.json','database/atual/regulamento_structure.json']) {
  const j=JSON.parse(fs.readFileSync(f,'utf8'));
  let n=0;
  for (const c of j.chapters) for (const a of (c.articles||[])) {
    const blob=[a.caput||'',...(a.items||[]).map(i=>i.text||'')].join(' ');
    if (/Supervisor de Dia/i.test(blob)) { n++; console.log(f+' ainda tem: '+a.editId); }
  }
  console.log(f+' -> '+n+' ocorrencias de \"Supervisor de Dia\"');
}
"
```

Esperado: `0 ocorrencias` nos dois arquivos.

- [ ] **Step 6: Rodar as suítes**

```bash
python scripts/test_regulamento_structure.py && python scripts/verificar_verbatim.py && npm test
```

Esperado: as três passam. `verificar_verbatim.py` **vai acusar** os artigos alterados se
eles ainda forem tratados como transcrição — se acusar, marcar os artigos de
`SUBSTITUIR_TERMOS` como adaptados (mesmo tratamento de `ADAPTATIONS`, que já convive com
o verificador), nunca afrouxar o verificador.

- [ ] **Step 7: Commit**

```bash
git add scripts/regulamento_reescrita.py scripts/build_regulamento_structure.py database/regulamento_structure.json database/atual/regulamento_structure.json docs/curadoria/depara-supervisor-de-dia.md
git commit -m "fix(curadoria): suprime a figura do Supervisor de Dia, inexistente no CBMRO

Aplica o de-para aprovado pelo Ten. Tiago: a fonte (RISD de Sergipe) tem tres
figuras de escala e o CBMRO tem duas. O inciso II da lista-mestra de funcoes
sai (a lista ja traz Superior de Dia e Oficial de Dia), e as 11 demais
ocorrencias sao redistribuidas pelo criterio de area de atuacao — presencial e
local vira Oficial de Dia, estadual e de sobreaviso vira Superior de Dia
(se-art-38). As cadeias de escalonamento passam a seguir a cadeia real: Cmt
SGBM, Cmt GBM, Cmt COB, Superior de Dia. Corrige junto a Secao de Recursos
Humanos do COB, que na LOB Art. 35 e Secao de Pessoal.

Co-Authored-By: Claude Opus 5 <noreply@anthropic.com>"
```

---

### Task 5: Purgar os resíduos de CIOP fora do capítulo próprio

O capítulo `central-operacoes-193` já reflete a NGA-CIOP-001/2026 (reescrito em 14/08). Esta tarefa tira as menções a CIOP espalhadas pelos outros capítulos — matéria que a NGA regula e o Regulamento não deve duplicar.

**Files:**
- Modify: `scripts/regulamento_reescrita.py`
- Modify: `scripts/test_regulamento_structure.py`

**Interfaces:**
- Consumes: `REMOVER_ARTIGOS` / `REMOVER_INCISOS` (já existentes).
- Produces: menções a CIOP concentradas só em `central-operacoes-193`.

- [ ] **Step 1: Levantar as ocorrências exatas**

```bash
node -e "
const fs=require('fs');
const j=JSON.parse(fs.readFileSync('database/atual/regulamento_structure.json','utf8'));
for (const c of j.chapters) {
  if (c.themeKey==='central-operacoes-193') continue;
  for (const a of (c.articles||[])) {
    const re=/CIOP|Central Integrada|Centro Integrado/i;
    if (re.test(a.caput||'')) console.log(c.themeKey+' | '+a.id+' | CAPUT: '+(a.caput||'').replace(/\s+/g,' ').slice(0,160));
    (a.items||[]).forEach((it,ix)=>{ const t=it.text||''; if(re.test(t)) console.log(c.themeKey+' | '+a.id+' | ['+ix+'] '+t.replace(/\s+/g,' ').slice(0,160)); });
  }
}
"
```

Esperado: 12 ocorrências fora do capítulo próprio, distribuídas em `organizacao-geral` (1),
`competencias-apoio-assessoramento` (3), `competencias-execucao` (1), `servico-operacional`
(4), `servico-interno-dia` (2), `atribuicoes-funcoes` (1).

- [ ] **Step 2: Classificar cada ocorrência**

Para cada uma, decidir entre:
- **artigo inteiro sai** (o CIOP é o sujeito do artigo) → `REMOVER_ARTIGOS`;
- **só o inciso sai** (o artigo continua válido) → `REMOVER_INCISOS`;
- **fica** (menção incidental legítima, ex.: o §2º autoral de `organizacao-geral`, que
  descreve as 2 CIOP como apoio ao COB e é fundado na LOB + organograma).

Registrar a classificação como comentário ao lado de cada entrada nova, no padrão do
arquivo (cada chave traz a razão em texto).

**Atenção:** a ocorrência em `organizacao-geral` está num artigo **autoral** — artigos
autorais não passam por `REMOVER_ARTIGOS`/`REMOVER_INCISOS`, que agem sobre o material
importado. Se precisar sair, edita-se o texto em `ARTIGOS_PROPRIOS` diretamente.

- [ ] **Step 3: Aplicar as remoções**

Acrescentar as entradas classificadas a `REMOVER_ARTIGOS` e `REMOVER_INCISOS` em
`scripts/regulamento_reescrita.py`. Exemplo do inciso da lista-mestra de funções, que é
resíduo certo (o despachante é função do CIOP, regulada pela NGA):

```python
# dentro de REMOVER_INCISOS['servico-operacional'], junto com a entrada da Task 4:
        'se-art-4': ['Supervisor de Dia', 'Despachante ao Central Integrada de Operações'],
```

- [ ] **Step 4: Regerar e conferir**

```bash
python scripts/build_regulamento_structure.py && python scripts/build_regulamento_structure_atual.py
```

Repetir o comando do Step 1 e confirmar que só sobraram as menções deliberadamente
mantidas.

- [ ] **Step 5: Atualizar o piso de artigos do teste**

Contar os artigos após a purga:

```bash
node -e "
const j=require('./database/regulamento_structure.json');
console.log('artigos:', j.chapters.reduce((n,c)=>n+(c.articles||[]).length,0));
"
```

Em `scripts/test_regulamento_structure.py`, atualizar o `assert len(edit_ids) >= 416` para
o número novo e acrescentar ao comentário de aritmética (linhas 72-87) uma linha por
remoção, no padrão já usado:

```python
#     -N artigos com residuo de CIOP fora do capitulo proprio (materia da NGA-CIOP-001/2026,
#        que o Regulamento remete em vez de duplicar — ver regulamento_reescrita.py)
```

- [ ] **Step 6: Rodar as suítes**

```bash
python scripts/test_regulamento_structure.py && python scripts/verificar_verbatim.py && npm test
```

Esperado: as três passam.

- [ ] **Step 7: Commit**

```bash
git add scripts/regulamento_reescrita.py scripts/test_regulamento_structure.py database/regulamento_structure.json database/atual/regulamento_structure.json
git commit -m "fix(curadoria): tira os residuos de CIOP dos capitulos que nao sao dele

O capitulo Da Central de Operacoes ja foi reescrito sobre a NGA-CIOP-001/2026
em 14/08; as mencoes espalhadas pelos demais capitulos sao materia da mesma
NGA, que o Regulamento remete em vez de duplicar. Sai tambem o Despachante ao
CIOP da lista-mestra de funcoes do servico diario, que e funcao do CIOP e nao
do servico diario da Corporacao.

Co-Authored-By: Claude Opus 5 <noreply@anthropic.com>"
```

---

### Task 6: Remissão à Resolução 121/2022 (imprensa e mídia)

Substitui o texto genérico importado de Sergipe/MT sobre entrevistas por remissão à norma própria do CBMRO.

**Files:**
- Modify: `scripts/regulamento_reescrita.py`
- Modify: `scripts/test_regulamento_structure.py:38-44` (allowlist de fundamento) e `:90` (contagem)

**Interfaces:**
- Consumes: `ARTIGOS_PROPRIOS`, `REMOVER_ARTIGOS`.
- Produces: 1 artigo autoral em `servico-operacional` com `fundamento` citando a Resolução nº 121/2022/CBM-CP.

- [ ] **Step 1: Liberar a Resolução na allowlist de fundamento**

Em `scripts/test_regulamento_structure.py`, acrescentar a alternativa na cadeia das linhas 38-44:

```python
            assert ('Lei nº 2.204/2009' in leaf['fundamento']
                    or 'LOB' in leaf['fundamento']
                    or 'Decreto nº 21.425/2016' in leaf['fundamento']
                    or 'Lei estadual nº 3.924/2016' in leaf['fundamento']
                    or 'organograma oficial' in leaf['fundamento']
                    or 'NGA-CIOP-001/2026' in leaf['fundamento']
                    or 'Resolução nº 121/2022/CBM-CP' in leaf['fundamento']), \
                f'fundamento não cita norma de RO: {leaf["fundamento"]}'
```

- [ ] **Step 2: Escrever o artigo autoral**

Em `scripts/regulamento_reescrita.py`, acrescentar a constante da norma junto de `_LOB`/`_DEC`/`_NGA`:

```python
_RES121 = 'CBMRO, Resolução nº 121/2022/CBM-CP (Diretriz Geral de Comunicação Social — ' \
          'D-05-BM), de 09 de dezembro de 2022'
```

E acrescentar a entrada de `servico-operacional` em `ARTIGOS_PROPRIOS`:

```python
    # ── servico-operacional (2026-08-18) ─────────────────────────────────────────────
    # O texto importado de Sergipe regulava entrevistas com regras próprias (quem concede,
    # o que é vedado, uniforme), matéria que em Rondônia já tem norma: a Resolução nº
    # 121/2022/CBM-CP aprova a Diretriz Geral de Comunicação Social (D-05-BM), fundada no
    # art. 11 da própria Lei 2.204/2009. O Regulamento remete a ela em vez de concorrer
    # com ela. O Manual de Relacionamento com a Mídia da DCS é citado como instrumento de
    # aplicação, NÃO como fundamento: não tem número de ato nem data de aprovação.
    'servico-operacional': [
        {
            'heading': 'Da prestação de informações à imprensa',
            'caput': 'A prestação de informações à imprensa e o relacionamento com os '
                     'meios de comunicação observarão a Diretriz Geral de Comunicação '
                     'Social do Corpo de Bombeiros Militar do Estado de Rondônia e as '
                     'orientações do Manual de Relacionamento com a Mídia editado pela '
                     'Diretoria de Comunicação Social, publicados no sítio oficial da '
                     'Corporação.',
            'dispositivos': [
                '§ 1º Compete à Diretoria de Comunicação Social coordenar o atendimento '
                'à imprensa, podendo a informação sobre ocorrência em curso ser prestada '
                'pelo militar que a comande, restrita aos aspectos técnicos do fato, '
                'vedada a manifestação de caráter pessoal.',
                '§ 2º As ocorrências de grande vulto ou de repercussão estadual terão o '
                'atendimento à imprensa articulado com a Diretoria de Comunicação Social '
                'e com o Superior de Dia.',
            ],
            'fundamento': f'{_RES121}; LOB, Art. 22',
        },
    ],
```

- [ ] **Step 3: Remover os artigos importados que a remissão substitui**

Acrescentar a `REMOVER_ARTIGOS` a entrada de `servico-operacional` com os artigos de
imprensa identificados no levantamento (no mínimo `se-art-113`), cada um com a razão:

```python
    'servico-operacional': {
        'se-art-113': 'regras próprias de entrevista importadas de Sergipe — matéria da '
                      'Resolução nº 121/2022/CBM-CP (Diretriz Geral de Comunicação Social), '
                      'para a qual o Regulamento agora remete',
    },
```

- [ ] **Step 4: Atualizar a contagem de autorais**

Em `scripts/test_regulamento_structure.py:90`, subir a contagem em 1 e completar a
descrição:

```python
assert len(autorais) == 41, \
    f'artigos autorais: {len(autorais)} (esperado 15 SCI + 21 org.-geral + 4 CIOP + 1 mídia = 41)'
```

Acrescentar ao comentário de aritmética a linha correspondente.

- [ ] **Step 5: Regerar e rodar as suítes**

```bash
python scripts/build_regulamento_structure.py && python scripts/build_regulamento_structure_atual.py && python scripts/test_regulamento_structure.py && python scripts/verificar_verbatim.py && npm test
```

Esperado: todas passam.

- [ ] **Step 6: Commit**

```bash
git add scripts/regulamento_reescrita.py scripts/test_regulamento_structure.py database/regulamento_structure.json database/atual/regulamento_structure.json
git commit -m "feat(regulamento): remete a prestacao de informacoes a imprensa a norma propria

O texto importado de Sergipe regulava entrevistas com regras proprias, materia
que em Rondonia ja tem norma: a Resolucao 121/2022/CBM-CP aprova a Diretriz
Geral de Comunicacao Social (D-05-BM), fundada no art. 11 da propria Lei
2.204/2009. O Regulamento remete a ela em vez de concorrer com ela. O Manual
de Relacionamento com a Midia da DCS entra como instrumento de aplicacao, nao
como fundamento — nao e ato normativo (sem numero nem data de aprovacao).

Co-Authored-By: Claude Opus 5 <noreply@anthropic.com>"
```

---

### Task 7: Artigo de remissão ao protocolo ATTS

Matéria hoje ausente da minuta (0 ocorrências de "suicídio"). Remissão genérica à doutrina, conforme decisão do Ten. Tiago — sem transcrever as fases e sem citar norma inexistente.

**Files:**
- Modify: `scripts/regulamento_reescrita.py`
- Modify: `scripts/test_regulamento_structure.py:90`

**Interfaces:**
- Consumes: entrada `'servico-operacional'` de `ARTIGOS_PROPRIOS` criada na Task 6.
- Produces: +1 artigo autoral.

- [ ] **Step 1: Acrescentar o artigo**

Em `scripts/regulamento_reescrita.py`, acrescentar ao final da lista
`ARTIGOS_PROPRIOS['servico-operacional']`:

```python
        {
            'heading': 'Do atendimento a tentativas de suicídio',
            'caput': 'O atendimento às ocorrências de tentativa de suicídio observará o '
                     'protocolo de Abordagem Técnica nas Tentativas de Suicídio e a '
                     'doutrina nacional correspondente, adotados pela Corporação em seus '
                     'cursos de formação, habilitação e aperfeiçoamento.',
            'dispositivos': [
                '§ 1º A abordagem será conduzida por militar habilitado no protocolo, '
                'privilegiando a técnica de aproximação e diálogo sobre a intervenção '
                'física, que se reserva às situações de risco iminente à vida.',
                '§ 2º Compete à Coordenadoria de Educação, Ensino e Instrução manter a '
                'capacitação do efetivo operacional no protocolo de que trata este artigo.',
            ],
            'fundamento': 'LOB, Art. 2º, IV e VII (socorro e salvamento), e Art. 15 '
                          '(Coordenadoria de Educação, Ensino e Instrução)',
        },
```

Nota de curadoria a incluir como comentário acima do artigo:

```python
            # A remissão é DELIBERADAMENTE genérica (determinação do Ten. Tiago,
            # 2026-08-18): o material disponível do ATTS é slide de instrução do CHOABM,
            # sem portaria ou resolução que o adote no CBMRO. Transcrever as 4 fases
            # (Aproximação, Silêncio Inicial, Apresentação Pessoal, Início do Diálogo)
            # elevaria material didático a norma e congelaria doutrina de curso dentro do
            # Regulamento. Se surgir ato que adote o protocolo, este artigo passa a citá-lo,
            # no padrão da Resolução nº 121/2022/CBM-CP.
```

- [ ] **Step 2: Atualizar a contagem de autorais**

```python
assert len(autorais) == 42, \
    f'artigos autorais: {len(autorais)} (esperado 15 SCI + 21 org.-geral + 4 CIOP + 1 mídia + 1 ATTS = 42)'
```

Acrescentar a linha correspondente ao comentário de aritmética.

- [ ] **Step 3: Regerar e conferir que a matéria entrou**

```bash
python scripts/build_regulamento_structure.py && python scripts/build_regulamento_structure_atual.py
node -e "
const j=require('./database/atual/regulamento_structure.json');
let n=0;
for (const c of j.chapters) for (const a of (c.articles||[]))
  if (/suic[ií]d/i.test([a.caput||'',...(a.items||[]).map(i=>i.text||'')].join(' '))) { n++; console.log(a.editId); }
console.log('artigos sobre tentativa de suicidio:', n);
"
```

Esperado: 1 artigo, em `servico-operacional`.

- [ ] **Step 4: Rodar as suítes**

```bash
python scripts/test_regulamento_structure.py && python scripts/verificar_verbatim.py && npm test
```

- [ ] **Step 5: Commit**

```bash
git add scripts/regulamento_reescrita.py scripts/test_regulamento_structure.py database/regulamento_structure.json database/atual/regulamento_structure.json
git commit -m "feat(regulamento): remete o atendimento a tentativas de suicidio ao protocolo ATTS

Materia ausente da minuta ate agora. A remissao e deliberadamente generica
(determinacao do Ten. Tiago): o material disponivel do ATTS e slide de
instrucao do CHOABM, sem portaria que o adote no CBMRO — transcrever as 4
fases elevaria material didatico a norma. O fundamento cita a LOB (competencia
de socorro e a Coordenadoria de Educacao, Ensino e Instrucao).

Co-Authored-By: Claude Opus 5 <noreply@anthropic.com>"
```

---

### Task 8: Capítulo V — atribuições das funções do COB e da CAT

A tarefa mais pesada. Escreve as atribuições por FUNÇÃO (pessoa) do COB e da CAT e marca todos os artigos do capítulo com o órgão, para o filtro da Task 2 operar.

**Files:**
- Modify: `scripts/regulamento_reescrita.py`
- Modify: `scripts/build_regulamento_structure.py` (propagar o campo `orgao` para o artigo gerado)
- Modify: `scripts/test_regulamento_structure.py`

**Interfaces:**
- Consumes: `ORGAOS_NO_ESCOPO = { servico: ['cob', 'cat'] }` (Task 2) — os valores de tag são exatamente `'cob'` e `'cat'`.
- Produces: artigos de `atribuicoes-funcoes` com campo `orgao`; os de COB/CAT autorais, os demais preservados e marcados com o órgão a que pertencem.

**Distinção que evita duplicata:** este capítulo trata de **funções** ("Compete ao
Coordenador…"), enquanto `seguranca-contra-incendio` e `organizacao-geral` tratam de
**órgãos** ("Compete à Seção…"). Escrever aqui competência de unidade duplicaria aqueles
capítulos.

- [ ] **Step 1: Permitir a tag `orgao` nos artigos autorais e importados**

Em `scripts/regulamento_reescrita.py`, acrescentar a tabela que classifica os artigos
importados do capítulo (os 27 de MT, que continuam no documento completo):

```python
# ── (e) TAG DE ÓRGÃO NO CAPÍTULO DAS ATRIBUIÇÕES DAS FUNÇÕES ────────────────────────
# O capítulo é MISTO por decisão de escopo (Ten. Tiago, 2026-08-18): as funções de COB e
# CAT foram reescritas sobre a LOB de RO e entram no recorte do Regulamento de Serviço; as
# dos demais órgãos seguem sendo o transplante de MT e só aparecem no Regulamento Geral
# completo, até a curadoria da 2ª etapa. A tag é o que o filtro de escopo do frontend lê
# (src/lib/escopoServico.js) — artigo SEM tag não entra no recorte, de propósito.
ORGAO_DO_ARTIGO = {
    'atribuicoes-funcoes': {
        'mt-art-62': 'emg', 'mt-art-63': 'emg', 'mt-art-67': 'dp',
        'mt-art-111': 'dcs', 'mt-art-123': 'cpof', 'mt-art-137': 'assessorias',
        'mt-art-144': 'cpof', 'mt-art-153': 'ajudancia',
        'mt-art-163': 'deei', 'mt-art-164': 'deei', 'mt-art-170': 'deei',
        'mt-art-190': 'deei', 'mt-art-191': 'deei',
        'mt-art-200': 'cat', 'mt-art-201': 'cat',
        'mt-art-221': 'gabinete', 'mt-art-222': 'gabinete', 'mt-art-225': 'gabinete',
        'mt-art-230': 'ciop',
        'mt-art-238': 'cob', 'mt-art-239': 'cob', 'mt-art-250': 'cob',
        'mt-art-251': 'cob', 'mt-art-255': 'cob', 'mt-art-256': 'cob',
        'mt-art-262': 'cob', 'mt-art-263': 'cob',
    },
}
```

**Atenção (AR-01):** os ids acima vieram do dump do capítulo, mas a classificação deve ser
conferida pelo CONTEÚDO de cada artigo, não pelo nome do cargo. `mt-art-200`/`201` falam do
Diretor de Segurança Contra Incêndio do MT — em RO a matéria é da CAT, mas o cargo não
existe com esse nome; conferir se o artigo deve ser reescrito (vira autoral, tag `cat`) ou
removido. `mt-art-230` é o Chefe do CIOP: matéria da NGA — provavelmente sai pela Task 5.

- [ ] **Step 2: Propagar a tag no builder**

Em `scripts/build_regulamento_structure.py`, importar `ORGAO_DO_ARTIGO` e, ao montar cada
artigo primário, gravar `'orgao': ORGAO_DO_ARTIGO.get(theme_key, {}).get(art_id)` quando
houver valor. Para os artigos autorais, aceitar uma chave `'orgao'` no dicionário de
`ARTIGOS_PROPRIOS` e copiá-la para o artigo gerado.

- [ ] **Step 3: Escrever as funções do COB**

Acrescentar a `ARTIGOS_PROPRIOS` a entrada `'atribuicoes-funcoes'`, com um artigo por
função, todos com `'orgao': 'cob'`. As funções vêm da estrutura já validada em
`organizacao-geral` (LOB Art. 35, §1º) e da cadeia do Art. 47:

1. Comandante Operacional de Bombeiros
2. Adjunto do Comando Operacional de Bombeiros
3. Chefe da Seção de Pessoal
4. Chefe da Seção Administrativa
5. Chefe da Seção de Informática
6. Chefe da Seção de Correição
7. Chefe da Seção de Planejamento Operacional e Controle de Resultados
8. Chefe da Agência Regional de Inteligência
9. Comandante de Grupamento de Bombeiro Militar
10. Comandante de Subgrupamento de Bombeiro Militar

Exemplo COMPLETO do primeiro artigo, que fixa o padrão dos demais — cada inciso derivado de
dispositivo da LOB, nunca inventado (mesma disciplina das reescritas de 13-14/08):

```python
        {
            'heading': 'Cap. I — Das funções do Comando Operacional de Bombeiros',
            'orgao': 'cob',
            'caput': 'Compete ao Comandante Operacional de Bombeiros:',
            'dispositivos': [
                'I - comandar as atividades-fins da Corporação e de proteção e defesa civil '
                'na área de abrangência do respectivo Comando Operacional, traduzindo em '
                'objetivos e metas as políticas e diretrizes do Comando-Geral e do '
                'Estado-Maior-Geral;',
                'II - exercer o comando dos Grupamentos de Bombeiro Militar a ele '
                'subordinados e das demais unidades operacionais de sua área;',
                'III - coordenar o emprego dos meios operacionais disponíveis, determinando '
                'o deslocamento de recursos entre as unidades subordinadas conforme a '
                'natureza e a magnitude da ocorrência;',
                'IV - fiscalizar e controlar a execução das atividades operacionais na sua '
                'área, respondendo pelos resultados perante o Subcomandante-Geral;',
                'V - autorizar, por escrito, a permuta de escala do serviço de Oficial de '
                'Dia, com posterior publicação em Boletim Geral Ostensivo;',
                'VI - acionar o Superior de Dia nas ocorrências de grande vulto, na forma '
                'deste Regulamento;',
                'VII - propor ao Comando-Geral a criação, a extinção ou a alteração de '
                'unidades operacionais de sua área, para constar do Quadro de Organização '
                'da Corporação;',
                'VIII - submeter-se, no que respeita à administração, ao Chefe do '
                'Estado-Maior-Geral, e, no que respeita às operações, ao Subcomandante-Geral.',
            ],
            'fundamento': 'LOB, Art. 34, Art. 35 e Art. 47 (red. Lei nº 4.303/2018) e '
                          'Art. 59, parágrafo único; organograma oficial do CBMRO',
        },
```

Para os 9 artigos restantes do COB, seguir exatamente esse padrão: `caput` sempre na forma
"Compete ao/à \<função\>:", incisos com lastro em dispositivo citado no `fundamento`, e a
subordinação declarada no último inciso quando a LOB a define. Onde a LOB não descrever a
função (caso dos Chefes de Seção, que a lei apenas enumera no Art. 35, §1º), derivar a
competência da finalidade da Seção já escrita em `organizacao-geral` — e **não** escrever o
artigo se nem isso houver, registrando a lacuna no commit em vez de preenchê-la por
analogia com outro estado.

- [ ] **Step 4: Escrever as funções da CAT**

Mesma entrada, `'orgao': 'cat'`, funções derivadas da LOB Art. 18, §1º e do Decreto nº
21.425/2016 (estrutura já validada em `seguranca-contra-incendio`):

1. Coordenador de Atividades Técnicas
2. Adjunto da Coordenadoria
3. Chefe da Seção Administrativa da Coordenadoria
4. Chefe da Seção de Estudos Técnicos
5. Chefe da Seção de Planejamento, Fiscalização e Suporte Técnico
6. Diretor de Atividades Técnicas
7. Adjunto da Diretoria de Atividades Técnicas
8. Chefes das Seções da Diretoria (Vistoria; Análise de Projetos; Investigação e Prevenção de Incêndio; Hidrantes)
9. Chefe da Seção de Atividades Técnicas (SAT)

Fundamento no padrão: `'LOB, Art. 18, § 1º (red. Lei nº 4.488/2019); Decreto nº 21.425/2016, Art. 7º'`.

- [ ] **Step 5: Atualizar as contagens do teste**

Contar os autorais e o total após a regeração:

```bash
python scripts/build_regulamento_structure.py && python scripts/build_regulamento_structure_atual.py
node -e "
const j=require('./database/regulamento_structure.json');
const arts=j.chapters.flatMap(c=>c.articles||[]);
console.log('total:', arts.length, '| autorais:', arts.filter(a=>a.autoral).length);
const cap=j.chapters.find(c=>c.themeKey==='atribuicoes-funcoes');
const porOrgao={};
cap.articles.forEach(a=>{ const k=a.orgao||'(sem tag)'; porOrgao[k]=(porOrgao[k]||0)+1; });
console.log('capitulo V por orgao:', porOrgao);
"
```

Atualizar em `scripts/test_regulamento_structure.py` o `>= N` de artigos e o
`len(autorais) == N`, completando o comentário de aritmética com as linhas do COB e da CAT.

- [ ] **Step 6: Acrescentar teste de invariante do capítulo misto**

Ao final de `scripts/test_regulamento_structure.py`, antes do `print` final:

```python
# Capítulo misto (2026-08-18): todo artigo precisa de tag de órgão, senão some do recorte
# do participante em silêncio — o filtro de escopo é fail-closed (src/lib/escopoServico.js).
_af = next(c for c in d['chapters'] if c['themeKey'] == 'atribuicoes-funcoes')
_sem_tag = [a['editId'] for a in _af['articles'] if not a.get('orgao')]
assert not _sem_tag, f'artigos sem tag de órgão no capítulo misto: {_sem_tag}'
_no_escopo = [a for a in _af['articles'] if a.get('orgao') in ('cob', 'cat')]
assert _no_escopo, 'nenhum artigo de COB/CAT — o recorte ficaria com o capítulo vazio'
assert all(a.get('autoral') for a in _no_escopo), \
    'artigo de COB/CAT no capítulo misto precisa ser redação própria sobre a LOB de RO'
```

- [ ] **Step 7: Rodar as suítes**

```bash
python scripts/test_regulamento_structure.py && python scripts/verificar_verbatim.py && npm test
```

- [ ] **Step 8: Commit**

```bash
git add scripts/regulamento_reescrita.py scripts/build_regulamento_structure.py scripts/test_regulamento_structure.py database/regulamento_structure.json database/atual/regulamento_structure.json
git commit -m "feat(curadoria): reescreve as atribuicoes das funcoes do COB e da CAT

O capitulo apresentava as funcoes de TODOS os orgaos da corporacao, importadas
em bloco do Regulamento do CBMMT — para o Regulamento de Servico so importam as
funcoes do COB (servico operacional) e da CAT (servico tecnico de seguranca
contra incendio), do comandante ate a menor funcao. As duas familias sao
reescritas sobre a LOB de RO e o organograma oficial; as demais recebem tag de
orgao e seguem visiveis so no Regulamento Geral completo, ate a curadoria da 2a
etapa. Escreve competencia de FUNCAO (Compete ao Coordenador...), nunca de
unidade, que ja e materia dos capitulos da organizacao geral e da SCI.

Co-Authored-By: Claude Opus 5 <noreply@anthropic.com>"
```

---

### Task 9: Ajustar a nota de escopo à filtragem por artigo

Com o filtro por artigo, a nota do recorte passa a contar como "fora" artigos de um capítulo que ela lista como "dentro" — inconsistência visível ao participante.

**Files:**
- Modify: `src/components/NotaEscopoServico.jsx`
- Modify: `src/pages/Revisao.jsx:117-125`

**Interfaces:**
- Consumes: `foraDoEscopo` (`Revisao.jsx`), hoje `{ artigos, titulos }`.
- Produces: a nota distingue capítulos inteiros fora do recorte de artigos cortados dentro de um capítulo que ficou.

- [ ] **Step 1: Escrever o teste da contagem**

Como `Revisao.jsx` é componente React sem suíte, mover a aritmética para lógica pura
testável. Primeiro acrescentar `resumoForaDoEscopo` ao import do topo de
`src/lib/escopoServico.test.js` (linha 3), que hoje traz só quatro nomes:

```javascript
import {
  TEMAS_SERVICO, temaDoCapitulo, filtrarEstruturaPorEscopo, rotaLiberadaNoEscopo,
  resumoForaDoEscopo,
} from './escopoServico.js'
```

Depois acrescentar o teste (reusa `comCapituloMisto()`, criada na Task 2):

```javascript
test('resumoForaDoEscopo separa capítulos inteiros de artigos cortados', () => {
  const completa = comCapituloMisto()
  const r = resumoForaDoEscopo(completa, filtrarEstruturaPorEscopo(completa, 'servico'), 'servico')
  assert.equal(r.artigosCortadosNoEscopo, 2, 'mt-art-62 e mt-art-63 saíram do capítulo misto')
  assert.deepEqual(r.capitulosFora, [], 'a estrutura-fake só tem capítulos do escopo')
})
```

- [ ] **Step 2: Rodar e confirmar que falha**

```bash
npm test
```

Esperado: FALHA — `resumoForaDoEscopo` não existe.

- [ ] **Step 3: Implementar a função**

Em `src/lib/escopoServico.js`:

```javascript
// Resumo honesto do que ficou de fora, para a nota de escopo: capítulos inteiros que não
// entram no recorte e artigos cortados DENTRO de um capítulo que entrou (capítulo misto).
// Contar os dois juntos, como antes, faria a nota dizer "N artigos ficaram de fora" e
// listar capítulos que não somam N — o leitor não fecharia a conta.
export function resumoForaDoEscopo(completa, recortada, escopo) {
  const temas = ESCOPOS[escopo]
  if (!temas || !Array.isArray(completa?.chapters)) {
    return { capitulosFora: [], artigosEmCapitulosFora: 0, artigosCortadosNoEscopo: 0 }
  }
  const noEscopo = new Set(temas)
  const capitulosFora = []
  let artigosEmCapitulosFora = 0
  for (const c of completa.chapters) {
    if (noEscopo.has(temaDoCapitulo(c.id))) continue
    if (c.chapterTitle) capitulosFora.push(c.chapterTitle)
    artigosEmCapitulosFora += (c.articles?.length ?? 0)
  }
  const contarArtigos = (e) => (e?.chapters ?? []).reduce((n, c) => n + (c.articles?.length ?? 0), 0)
  const totalNoEscopo = completa.chapters
    .filter(c => noEscopo.has(temaDoCapitulo(c.id)))
    .reduce((n, c) => n + (c.articles?.length ?? 0), 0)
  return {
    capitulosFora,
    artigosEmCapitulosFora,
    artigosCortadosNoEscopo: totalNoEscopo - contarArtigos(recortada),
  }
}
```

- [ ] **Step 4: Rodar e confirmar que passa**

```bash
npm test
```

- [ ] **Step 5: Usar a função na tela**

Em `src/pages/Revisao.jsx`, trocar o `useMemo` de `foraDoEscopo` (linhas 117-125) por
chamada a `resumoForaDoEscopo(data, dataEscopo, escopo)`, e passar os campos novos para
`NotaEscopoServico`. Em `src/components/NotaEscopoServico.jsx`, acrescentar a frase sobre
os artigos cortados dentro do capítulo, exibida só quando `artigosCortadosNoEscopo > 0`:

```jsx
{artigosCortadosNoEscopo > 0 && (
  <p>
    No capítulo das Atribuições das Funções constam apenas as funções do Comando
    Operacional de Bombeiros e da Coordenadoria de Atividades Técnicas —{' '}
    <strong>{artigosCortadosNoEscopo} artigos</strong> das funções dos demais órgãos
    ficam para o Regulamento Geral completo.
  </p>
)}
```

- [ ] **Step 6: Conferir no navegador**

```bash
npm run dev -- --port 5173 --strictPort
```

Abrir http://localhost:5173/regulamento/servico e conferir: o Capítulo II é "DAS
ATRIBUIÇÕES DAS FUNÇÕES", só com funções de COB e CAT, e a nota de escopo fecha a conta.
**Esta conferência visual depende do Ten. Tiago** — o ambiente do agente não tem navegador.

- [ ] **Step 7: Commit**

```bash
git add src/lib/escopoServico.js src/lib/escopoServico.test.js src/pages/Revisao.jsx src/components/NotaEscopoServico.jsx
git commit -m "fix(regulamento): nota de escopo distingue capitulo fora de artigo cortado

Com o filtro por artigo, a nota passava a contar como fora artigos de um
capitulo que ela mesma listava como dentro — o leitor nao fechava a conta. A
aritmetica sai do componente React e vira funcao pura testada.

Co-Authored-By: Claude Opus 5 <noreply@anthropic.com>"
```

---

### Task 10: Conferência das 71 sugestões

Feita por último, de propósito: muitas das sugestões apontam exatamente os defeitos que as Tasks 1-9 eliminam.

**Files:**
- Create: `docs/curadoria/conferencia-71-sugestoes.md`

**Interfaces:**
- Consumes: o documento já corrigido; a coleção `suggestions` do Firestore.
- Produces: classificação de cada sugestão em `resolvida pela rodada` | `ortografia/formatação a aplicar` | `pauta do CONDEG`.

- [ ] **Step 1: Exportar as sugestões**

Requer credencial de membro. O acesso é via API REST do Firebase Auth + Firestore (o
ambiente do agente não tem navegador). Pedir ao Ten. Tiago as credenciais no momento da
execução — **não guardar em arquivo nem em commit**.

- [ ] **Step 2: Classificar cada sugestão**

Para cada uma das 71, verificar se o dispositivo alvo ainda existe e se o defeito apontado
persiste após as Tasks 1-9. Registrar em `docs/curadoria/conferencia-71-sugestoes.md` com
uma linha por sugestão: id, dispositivo, texto, classificação e justificativa.

Atenção ao rótulo defasado: `dispositivoLabelSnapshot` guarda o número do artigo no
momento em que a sugestão foi feita ("Art. 262"). A reordenação da Task 1 e as remoções das
Tasks 4-8 mudam a numeração exibida. O **endereço** (`editId#index`) não muda — conferido
em 18/08: `editId` é `reg:atual:<tema>/<artigo>`, sem índice posicional. Usar o `editId`,
nunca o rótulo.

- [ ] **Step 3: Aplicar as correções de ortografia e formatação**

As que sobrarem na categoria mecânica entram em `scripts/regulamento_reescrita.py`
(`SUBSTITUIR_TERMOS`, se for troca de texto) e regeram-se os JSONs. Defeitos de extração já
identificados que provavelmente aparecem aqui:
- `se-art-4`: caput começa com "º Visando a otimização…" — sobra da quebra de "Art. 4º".
- `se-art-38` e `se-art-113`: título de seção grudado no fim do caput ("Oficial de Dia",
  "Folga em Ocorrência").

- [ ] **Step 4: Rodar as suítes e commitar**

```bash
python scripts/test_regulamento_structure.py && python scripts/verificar_verbatim.py && npm test
git add -A
git commit -m "fix(curadoria): aplica as correcoes mecanicas das 71 sugestoes

Classifica as sugestoes recebidas no Firestore apos as correcoes de conteudo
desta rodada: as resolvidas pela propria reescrita, as de ortografia e
formatacao (aplicadas aqui) e as que dependem de deliberacao do CONDEG, que
seguem abertas.

Co-Authored-By: Claude Opus 5 <noreply@anthropic.com>"
```

- [ ] **Step 5: Atualizar o backlog**

Em `.claude/PENDENCIAS.md`, mover para ✅ Concluído o que esta rodada fechou e deixar
explícito o que continua aberto (as sugestões de pauta do CONDEG, a Parte I do Regulamento
Geral completo e a reordenação geral de capítulos).

---

## Verificação final

Antes de considerar a rodada concluída:

```bash
python scripts/build_regulamento_structure.py && python scripts/build_regulamento_structure_atual.py
python scripts/test_regulamento_structure.py
python scripts/verificar_verbatim.py
npm test
npm run build
```

Conferências que **dependem do Ten. Tiago** (o ambiente do agente não tem navegador):
1. `/regulamento/servico` no perfil **participante**: Capítulo II é "DAS ATRIBUIÇÕES DAS FUNÇÕES", com funções só de COB e CAT.
2. `/regulamento` no perfil **admin**: o capítulo continua com as funções de todos os órgãos.
3. Nenhuma menção a "Supervisor de Dia" em qualquer tela.
4. Os comentários existentes continuam ancorados nos dispositivos certos.
