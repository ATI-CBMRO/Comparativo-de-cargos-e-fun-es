# Regulamento de Serviço — ambiente setorizado por escopo · Plano de Implementação

> **Para executores agênticos:** SUB-SKILL OBRIGATÓRIA: use `superpowers:subagent-driven-development`
> (recomendado) ou `superpowers:executing-plans` para executar tarefa a tarefa. Os passos usam
> caixas (`- [ ]`) para acompanhamento.

**Spec:** `docs/superpowers/specs/2026-08-13-regulamento-servico-escopo-participante-design.md`
**Branch:** `feat/regulamento-servico-escopo` (já criada, spec já commitada)

**Objetivo:** dar ao participante convidado um ambiente que mostre **apenas** a minuta do
Regulamento de Serviço (7 capítulos, 185 artigos, LOB atual) para ler e comentar, sem
alterar nada para quem já usa o portal.

**Arquitetura:** o recorte é uma **lista de capítulos em lógica pura** aplicada sobre a
estrutura já existente, antes da articulação. Um campo `escopo` no cadastro do participante
liga o recorte. Nenhum documento novo, nenhum dado duplicado: os comentários continuam
ancorados no `editId` do dispositivo e reaparecem intactos no Regulamento completo depois.

**Stack:** React 18 + react-router-dom 6 + Vite 6; Firebase (Auth + Firestore); testes de
lógica pura com `node --test`.

## Restrições globais

- **Idioma de toda a interface: pt-BR.** Nenhum rótulo em inglês.
- **Não tocar** em `RegulamentoWizard.jsx`, `minutaDocx.js`, `ConferenciaLinear.jsx`,
  `RegulamentoComparator.jsx`, `RegSubsidio.jsx`, `firestore.rules`, nem em qualquer
  arquivo de `database/`. Esta entrega é o ambiente, não o conteúdo.
- **Comportamento sem escopo é sagrado:** usuário sem o campo `escopo` (todos os atuais)
  deve ver o portal exatamente como hoje. Toda função nova é no-op nesse caso.
- **Casar capítulo pelo SUFIXO do id** (`id.split(':').pop()`). O id carrega o marcador de
  cenário: `reg:servico-operacional` (futura) × `reg:atual:servico-operacional` (atual).
  Casar pelo id inteiro quebra em um dos cenários.
- **Nenhum número de artigo pode ser digitado à mão no código.** 185 e 228 são resultado da
  contagem no momento; devem ser calculados a partir dos dados, nunca fixados.
- Rodar `npm test` (que é `node --test "src/lib/**/*.test.js" "api/**/*.test.js"`) ao fim de
  cada tarefa que toque `src/lib/`.

---

### Tarefa 1: Lógica pura do recorte (`escopoServico.js`)

**Arquivos:**
- Criar: `src/lib/escopoServico.js`
- Criar: `src/lib/escopoServico.test.js`

**Interfaces:**
- Consome: nada (lógica pura, sem React, sem Firebase).
- Produz, usado pelas Tarefas 3 e 5:
  - `TEMAS_SERVICO: string[]` — os 7 sufixos de tema, **na ordem de leitura**.
  - `temaDoCapitulo(id: string): string` — sufixo do id, sem o marcador de cenário.
  - `filtrarEstruturaPorEscopo(structure: object|null, escopo: string|null|undefined): object|null`
    — devolve `{...structure, chapters}` filtrado e reordenado; devolve `structure`
    **inalterado** quando o escopo é nulo/desconhecido ou não há `chapters`.

- [ ] **Passo 1: Escrever os testes que falham**

Criar `src/lib/escopoServico.test.js`:

```js
import test from 'node:test'
import assert from 'node:assert/strict'
import { TEMAS_SERVICO, temaDoCapitulo, filtrarEstruturaPorEscopo } from './escopoServico.js'

// Estrutura-fake na MESMA ordem do arquivo real: a Parte I inteira antes da Parte II,
// com "disposicoes-finais" na posição 12 — é justamente o que o recorte precisa corrigir.
const estruturaFutura = () => ({
  title: 'Regulamento Geral',
  chapters: [
    { id: 'reg:disposicoes-preliminares', chapterTitle: 'DAS DISPOSIÇÕES PRELIMINARES', parte: 'geral' },
    { id: 'reg:organizacao-geral', chapterTitle: 'DA ORGANIZAÇÃO GERAL', parte: 'geral' },
    { id: 'reg:competencias-direcao', chapterTitle: 'DAS COMPETÊNCIAS DOS ÓRGÃOS DE DIREÇÃO', parte: 'geral' },
    { id: 'reg:ensino-instrucao', chapterTitle: 'DO ENSINO E DA INSTRUÇÃO', parte: 'geral' },
    { id: 'reg:seguranca-contra-incendio', chapterTitle: 'DA SEGURANÇA CONTRA INCÊNDIO E PÂNICO', parte: 'geral' },
    { id: 'reg:disposicoes-finais', chapterTitle: 'DAS DISPOSIÇÕES FINAIS', parte: 'geral' },
    { id: 'reg:servico-operacional', chapterTitle: 'DO SERVIÇO OPERACIONAL', parte: 'servico' },
    { id: 'reg:servico-interno-dia', chapterTitle: 'DO SERVIÇO INTERNO E DE DIA', parte: 'servico' },
    { id: 'reg:atribuicoes-funcoes', chapterTitle: 'DAS ATRIBUIÇÕES DAS FUNÇÕES', parte: 'servico' },
    { id: 'reg:central-operacoes-193', chapterTitle: 'DA CENTRAL DE OPERAÇÕES E DO TELEDESPACHO', parte: 'servico' },
  ],
})

// Mesmos capítulos, ids do cenário ATUAL (marcador 'atual:' no meio do id).
const estruturaAtual = () => ({
  ...estruturaFutura(),
  chapters: estruturaFutura().chapters.map(c => ({
    ...c, id: c.id.replace('reg:', 'reg:atual:'),
  })),
})

test('TEMAS_SERVICO tem os 7 temas do recorte, na ordem de leitura', () => {
  assert.deepEqual(TEMAS_SERVICO, [
    'disposicoes-preliminares',
    'servico-operacional',
    'central-operacoes-193',
    'servico-interno-dia',
    'atribuicoes-funcoes',
    'seguranca-contra-incendio',
    'disposicoes-finais',
  ])
})

test('temaDoCapitulo tira o marcador de cenário dos dois formatos de id', () => {
  assert.equal(temaDoCapitulo('reg:servico-operacional'), 'servico-operacional')
  assert.equal(temaDoCapitulo('reg:atual:servico-operacional'), 'servico-operacional')
  assert.equal(temaDoCapitulo('preliminares'), 'preliminares')
  assert.equal(temaDoCapitulo(null), '')
})

test('filtra para os 7 capítulos do escopo e descarta o resto', () => {
  const r = filtrarEstruturaPorEscopo(estruturaFutura(), 'servico')
  assert.equal(r.chapters.length, 7)
  const ids = r.chapters.map(c => c.id)
  assert.ok(!ids.includes('reg:organizacao-geral'))
  assert.ok(!ids.includes('reg:competencias-direcao'))
  assert.ok(!ids.includes('reg:ensino-instrucao'))
})

test('REORDENA: Preliminares abre e Disposições Finais fecha (não a ordem do arquivo)', () => {
  const r = filtrarEstruturaPorEscopo(estruturaFutura(), 'servico')
  assert.equal(temaDoCapitulo(r.chapters[0].id), 'disposicoes-preliminares')
  assert.equal(temaDoCapitulo(r.chapters.at(-1).id), 'disposicoes-finais')
  assert.deepEqual(r.chapters.map(c => temaDoCapitulo(c.id)), TEMAS_SERVICO)
})

test('funciona igual no cenário atual (ids com marcador atual:)', () => {
  const r = filtrarEstruturaPorEscopo(estruturaAtual(), 'servico')
  assert.deepEqual(r.chapters.map(c => temaDoCapitulo(c.id)), TEMAS_SERVICO)
  assert.equal(r.chapters[0].id, 'reg:atual:disposicoes-preliminares')
})

test('preserva os demais campos da estrutura e não muta a original', () => {
  const original = estruturaFutura()
  const r = filtrarEstruturaPorEscopo(original, 'servico')
  assert.equal(r.title, 'Regulamento Geral')
  assert.equal(original.chapters.length, 10, 'a estrutura original não pode ser alterada')
})

test('NO-OP: sem escopo, escopo desconhecido ou estrutura nula devolve o que veio', () => {
  const original = estruturaFutura()
  assert.equal(filtrarEstruturaPorEscopo(original, null), original)
  assert.equal(filtrarEstruturaPorEscopo(original, undefined), original)
  assert.equal(filtrarEstruturaPorEscopo(original, 'inexistente'), original)
  assert.equal(filtrarEstruturaPorEscopo(null, 'servico'), null)
  assert.equal(filtrarEstruturaPorEscopo({}, 'servico').chapters, undefined)
})

test('tema do escopo ausente na estrutura é ignorado, sem buraco na lista', () => {
  const semIncendio = estruturaFutura()
  semIncendio.chapters = semIncendio.chapters.filter(c => !c.id.includes('seguranca'))
  const r = filtrarEstruturaPorEscopo(semIncendio, 'servico')
  assert.equal(r.chapters.length, 6)
  assert.ok(r.chapters.every(Boolean), 'nenhum undefined pode sobrar na lista')
})
```

- [ ] **Passo 2: Rodar e ver falhar**

```bash
node --test src/lib/escopoServico.test.js
```

Esperado: FALHA com `Cannot find module './escopoServico.js'`.

- [ ] **Passo 3: Escrever a implementação mínima**

Criar `src/lib/escopoServico.js`:

```js
// Recorte setorizado do Regulamento de Serviço (spec 2026-08-13).
// Fonte ÚNICA da lista de capítulos E da ordem de leitura — nenhuma tela repete isto.

// ATENÇÃO: esta lista é a ORDEM do documento recortado, não só o filtro. NÃO é a ordem
// do arquivo: no regulamento_structure.json a Parte I vem inteira antes da Parte II, de
// modo que "DAS DISPOSIÇÕES FINAIS" (posição 12) precede o serviço operacional (13).
// Preservar a ordem do arquivo jogaria o fecho do regulamento para o meio do documento.
// Ordem escolhida: COB primeiro, CAT em bloco próprio, Preliminares e Finais nas pontas.
export const TEMAS_SERVICO = [
  'disposicoes-preliminares',
  'servico-operacional',
  'central-operacoes-193',
  'servico-interno-dia',
  'atribuicoes-funcoes',
  'seguranca-contra-incendio',
  'disposicoes-finais',
]

export const ESCOPOS = { servico: TEMAS_SERVICO }

// O id do capítulo carrega o marcador de cenário ('reg:x' na futura, 'reg:atual:x' no
// atual). Casar pelo id inteiro quebraria em um dos dois cenários.
export function temaDoCapitulo(id) {
  return String(id ?? '').split(':').pop()
}

// Devolve a estrutura com os capítulos do escopo, NA ORDEM de TEMAS_SERVICO.
// Escopo nulo/desconhecido, ou estrutura sem chapters: devolve o que veio, intacto —
// quem não tem escopo não é afetado por nada disto.
export function filtrarEstruturaPorEscopo(structure, escopo) {
  const temas = ESCOPOS[escopo]
  if (!temas || !Array.isArray(structure?.chapters)) return structure
  const porTema = new Map()
  for (const c of structure.chapters) porTema.set(temaDoCapitulo(c.id), c)
  const chapters = temas.map(t => porTema.get(t)).filter(Boolean)
  return { ...structure, chapters }
}
```

- [ ] **Passo 4: Rodar e ver passar**

```bash
node --test src/lib/escopoServico.test.js
npm test
```

Esperado: todos PASS (os 8 novos + os que já existiam).

- [ ] **Passo 5: Commitar**

```bash
git add src/lib/escopoServico.js src/lib/escopoServico.test.js
git commit -m "feat(escopo): recorte do Regulamento de Serviço em lógica pura testada"
```

---

### Tarefa 2: Propagar o escopo do cadastro para o usuário logado

**Arquivos:**
- Modificar: `src/lib/auth.jsx:46-51` (o objeto passado a `setUser`)

**Interfaces:**
- Consome: documento `members/{email}` do Firestore, campo opcional `escopo`.
- Produz, usado pelas Tarefas 3, 4 e 5: `user.escopo` — `'servico'` ou `null`.

**Contexto para quem nunca viu este arquivo:** `AuthProvider` monta o objeto `user` a
partir do documento `members/{email}`. O campo `role` já é normalizado ali com uma
expressão defensiva (qualquer valor diferente de `'admin'` vira `'participante'`). O campo
novo segue exatamente o mesmo padrão: valor desconhecido vira `null`, nunca é confiado cru.

- [ ] **Passo 1: Acrescentar o campo `escopo`**

Em `src/lib/auth.jsx`, no objeto de `setUser`, logo depois da linha do `role`:

```js
        setUser({
          uid: fbUser.uid,
          email,
          nome: m.nome ?? email,
          role: m.role === 'admin' ? 'admin' : 'participante',
          // Escopo restringe o participante a um recorte do portal (ver
          // src/lib/escopoServico.js). Ausente/desconhecido = null = portal completo,
          // que é o caso de TODOS os cadastros existentes.
          escopo: m.escopo === 'servico' ? 'servico' : null,
        })
```

- [ ] **Passo 2: Conferir que nada mais quebrou**

```bash
npm test
```

Esperado: PASS (nenhum teste cobre `auth.jsx`, que depende de Firebase; o comando serve
para garantir que nada foi quebrado por acidente).

- [ ] **Passo 3: Commitar**

```bash
git add src/lib/auth.jsx
git commit -m "feat(escopo): propaga members.escopo para o usuário logado"
```

---

### Tarefa 3: Nota de escopo no topo do documento

**Arquivos:**
- Criar: `src/components/NotaEscopoServico.jsx`
- Modificar: `src/index.css` (acrescentar `.nota-escopo` no fim do arquivo)

**Interfaces:**
- Consome: nada além das props.
- Produz, usado pela Tarefa 4: componente padrão com as props
  `{ artigosNoEscopo: number, artigosFora: number, capitulosFora: string[] }`.

**Por que os números são props e não texto fixo:** a restrição global proíbe cravar 185 e
228 no código. Quem chama calcula a partir dos dados reais, de modo que a nota nunca mente
se a curadoria mudar a minuta.

- [ ] **Passo 1: Criar o componente**

Criar `src/components/NotaEscopoServico.jsx`:

```jsx
import { Info } from 'lucide-react'

// Nota de escopo do recorte setorizado (spec 2026-08-13). Declara na cara do documento
// o que ficou para a 2ª etapa: a análise transversal mostrou que a lacuna do recorte é
// CONCEITUAL (matéria pressuposta), não textual — a minuta tem 1 única remissão a
// "Art. N" em todo o recorte, e ela é externa. Lacuna declarada é escopo.
export default function NotaEscopoServico({ artigosNoEscopo, artigosFora, capitulosFora }) {
  return (
    <aside className="nota-escopo">
      <Info className="nota-escopo-ico" size={18} aria-hidden="true" />
      <div>
        <p className="nota-escopo-titulo">Minuta do Regulamento de Serviço — 1ª etapa</p>
        <p>
          Reúne o serviço operacional (COB), a Central de Operações e o teledespacho, o
          serviço interno e de dia, as atribuições das funções e o serviço técnico de
          segurança contra incêndio e pânico (CAT) — <strong>{artigosNoEscopo} artigos</strong>,
          sobre a Lei nº 2.204/2009, a Lei de Organização Básica vigente.
        </p>
        {capitulosFora.length > 0 && (
          <p>
            Ficam para a 2ª etapa, no Regulamento Geral completo,{' '}
            <strong>{artigosFora} artigos</strong>: {capitulosFora.join('; ')}.
          </p>
        )}
        <p className="nota-escopo-aviso">
          A numeração dos artigos é provisória e será refeita na consolidação final.
        </p>
      </div>
    </aside>
  )
}
```

- [ ] **Passo 2: Acrescentar o estilo**

No fim de `src/index.css`:

```css
/* Nota de escopo do Regulamento de Serviço (recorte setorizado, spec 2026-08-13) */
.nota-escopo {
  display: flex;
  gap: 12px;
  align-items: flex-start;
  max-width: 780px;
  margin: 0 auto 28px;
  padding: 14px 18px;
  border-left: 4px solid var(--cbm-red-700);
  border-radius: 6px;
  background: #fff;
  box-shadow: 0 1px 3px rgba(16, 24, 40, .08);
  font-size: 14px;
  line-height: 1.55;
  color: var(--navy-700, #33415c);
}
.nota-escopo p { margin: 0 0 8px; }
.nota-escopo p:last-child { margin-bottom: 0; }
.nota-escopo-ico { flex: 0 0 auto; margin-top: 2px; color: var(--cbm-red-700); }
.nota-escopo-titulo { font-weight: 700; color: var(--cbm-red-700); }
.nota-escopo-aviso { font-style: italic; opacity: .85; }
```

- [ ] **Passo 3: Conferir que as variáveis CSS usadas existem**

```bash
grep -n -- "--cbm-red-700\|--navy-700" src/index.css | head -5
```

Esperado: pelo menos uma definição de `--cbm-red-700`. Se `--navy-700` não existir, o
`var(--navy-700, #33415c)` já cai no valor reserva — nada a fazer.

- [ ] **Passo 4: Commitar**

```bash
git add src/components/NotaEscopoServico.jsx src/index.css
git commit -m "feat(escopo): nota de escopo declarando o que fica para a 2a etapa"
```

---

### Tarefa 4: Aplicar o recorte na tela de Revisão

**Arquivos:**
- Modificar: `src/pages/Revisao.jsx`

**Interfaces:**
- Consome: `filtrarEstruturaPorEscopo` (Tarefa 1), `NotaEscopoServico` (Tarefa 3).
- Produz, usado pela Tarefa 5: a prop `escopo` de `Revisao` — `'servico'` ou ausente.

**Contexto:** `Revisao` carrega a estrutura em `data`, articula com `buildArticles(data)` e
desenha. O recorte entra **entre** o carregamento e a articulação. Três cuidados:

1. `data` continua sendo a estrutura **completa** — é dela que sai a contagem do que ficou
   de fora, para a nota de escopo.
2. As faixas "PARTE I / PARTE II" precisam sumir no modo escopo. Na ordem de leitura as
   partes se alternam (`geral` → `servico` → `geral`) e a tela imprimiria
   "PARTE I → PARTE II → PARTE I", sugerindo que o documento volta atrás. Como o código já
   trata mapa vazio como no-op, basta não montar o mapa.
3. `alternativesAberto` procura o capítulo do dispositivo aberto — deve procurar na
   estrutura **recortada**, que é a que está na tela.

- [ ] **Passo 1: Acrescentar os imports**

Em `src/pages/Revisao.jsx`, junto dos demais imports:

```js
import { filtrarEstruturaPorEscopo } from '../lib/escopoServico.js'
import NotaEscopoServico from '../components/NotaEscopoServico.jsx'
```

- [ ] **Passo 2: Aceitar a prop e derivar a estrutura recortada**

Trocar a assinatura do componente:

```js
export default function Revisao({ initialDoc, escopo } = {}) {
```

E logo depois de `const [regulamentoAberto, setRegulamentoAbertoState] = useState(false)`,
acrescentar:

```js
  // Recorte setorizado (spec 2026-08-13). `data` segue com o documento COMPLETO — é dela
  // que sai a contagem do que ficou de fora, para a nota de escopo. Sem escopo, é no-op.
  const dataEscopo = useMemo(() => filtrarEstruturaPorEscopo(data, escopo), [data, escopo])
```

- [ ] **Passo 3: Articular a partir da estrutura recortada**

Trocar a linha de `articles` e a de `parteDe`:

```js
  const articles = useMemo(() => (dataEscopo ? buildArticles(dataEscopo) : []), [dataEscopo])
  // No modo escopo o documento NÃO é dividido em Partes — é um documento único de
  // serviço. Mapa vazio faz as faixas "PARTE I/II" virarem no-op (regulamentoPartes.js).
  const parteDe = useMemo(
    () => (docId === 'reg' && !escopo ? parteByChapterTitle(dataEscopo) : {}),
    [docId, dataEscopo, escopo],
  )
```

- [ ] **Passo 4: Corrigir a busca de referências para a estrutura recortada**

No `useMemo` de `alternativesAberto`, trocar as duas ocorrências de `data` por `dataEscopo`:

```js
  const alternativesAberto = useMemo(() => {
    if (!aberto || !dataEscopo) return {}
    const { editId } = parseDispositivoId(aberto.id)
    const chapterId = chapterIdOf(editId)
    const chapter = dataEscopo.chapters.find(c => c.id === chapterId)
    return chapter?.alternatives ?? {}
  }, [aberto, dataEscopo])
```

- [ ] **Passo 5: Calcular os números da nota de escopo**

Logo depois do `useMemo` de `articles`:

```js
  // Números da nota de escopo, calculados dos dados reais — nunca cravados no código.
  const foraDoEscopo = useMemo(() => {
    if (!escopo || !data) return null
    const idsNoEscopo = new Set((dataEscopo?.chapters ?? []).map(c => c.id))
    const capitulos = data.chapters.filter(c => !idsNoEscopo.has(c.id))
    return {
      artigos: buildArticles(data).length - articles.length,
      titulos: capitulos.map(c => c.chapterTitle).filter(Boolean),
    }
  }, [escopo, data, dataEscopo, articles])
```

- [ ] **Passo 6: Ajustar o título da tela**

Trocar a linha de `tituloDoc`:

```js
  const tituloDoc = escopo === 'servico'
    ? 'Minuta do Regulamento de Serviço'
    : (docId === 'reg' ? 'Revisão do Regulamento' : 'Revisão da Minuta')
```

- [ ] **Passo 7: Desenhar a nota acima do documento**

A nota pertence ao documento, não ao sumário lateral — então entra dentro de
`<div className="rev-doc">`, como **primeiro filho**, imediatamente antes do
`{(() => {` que percorre os artigos:

```jsx
          <div className="rev-doc">
          {foraDoEscopo && (
            <NotaEscopoServico
              artigosNoEscopo={articles.length}
              artigosFora={foraDoEscopo.artigos}
              capitulosFora={foraDoEscopo.titulos}
            />
          )}
          {(() => {
```

- [ ] **Passo 8: Conferir que nada quebrou e que o build passa**

```bash
npm test
npm run build
```

Esperado: testes PASS e build sem erro.

- [ ] **Passo 9: Commitar**

```bash
git add src/pages/Revisao.jsx
git commit -m "feat(escopo): Revisão aceita recorte setorizado, sem faixas de Parte"
```

---

### Tarefa 5: Rota, cenário travado e menu enxuto

**Arquivos:**
- Modificar: `src/App.jsx`

**Interfaces:**
- Consome: `user.escopo` (Tarefa 2), prop `escopo` de `Revisao` (Tarefa 4).
- Produz: rota `/regulamento/servico`; menu reduzido.

**Contexto:** `App.jsx` define o array `NAV_GROUPS` (o menu), o componente `Sidebar` (que
percorre esse array) e o bloco `<Routes>`. O cenário vem da URL — `ScenarioProvider`
resolve `?cenario=` e carimba na URL. Para travar em `atual` basta chamar `setCenario`
uma vez ao montar a rota; o provider carimba a URL sozinho.

**Aviso que precisa constar no código:** esconder itens do menu é **simplificação de
interface, não controle de segurança**. Quem digitar `/minuta` na barra de endereço ainda
chega lá. A segurança de dado é do `firestore.rules`, que não muda nesta entrega.

- [ ] **Passo 1: Acrescentar o menu do escopo**

Logo depois do fechamento do array `NAV_GROUPS` em `src/App.jsx`:

```js
// Menu do participante com escopo (spec 2026-08-13): só o que diz respeito a ele.
// ATENÇÃO: isto é simplificação de INTERFACE, não parede — quem digitar /minuta na
// barra de endereço ainda alcança a rota. Segurança de dado é do firestore.rules.
const NAV_ESCOPO = {
  servico: [
    { to: '/regulamento/servico', icon: BookMarked, label: 'Regulamento de Serviço', end: true },
    { to: '/manual', icon: BookOpen, label: 'Manual de uso' },
  ],
}
```

- [ ] **Passo 2: Fazer a Sidebar respeitar o escopo**

Dentro de `function Sidebar(...)`, logo depois de `const { user } = useAuth()`:

```js
  const itensEscopo = NAV_ESCOPO[user?.escopo] ?? null
```

Trocar `<ScenarioSwitcher />` por:

```jsx
      {/* Participante com escopo não escolhe cenário: a rota já o trava em "atual". */}
      {!itensEscopo && <ScenarioSwitcher />}
```

E trocar o bloco `{NAV_GROUPS.map(...)}` inteiro por:

```jsx
        {itensEscopo
          ? (
            <div className="nav-group">
              {itensEscopo.map(({ to, icon: Icon, label, end }) => (
                <NavLink
                  key={to}
                  to={to}
                  end={end}
                  onClick={onNavigate}
                  title={label}
                  className={({ isActive }) => `nav-item${isActive ? ' active' : ''}`}
                >
                  <Icon className="nav-icon" size={18} />
                  <span className="nav-item-label">{label}</span>
                </NavLink>
              ))}
            </div>
          )
          : NAV_GROUPS.map((group, gi) => (
          <div key={group.section ?? `g${gi}`} className="nav-group">
            {group.section && <div className="nav-section-label nav-section-label-sub">{group.section}</div>}
            {group.items
              .filter(it => !it.admin || user?.role === 'admin')
              .map(({ to, icon: Icon, label, end }) => (
                <NavLink
                  key={to}
                  to={to}
                  end={end}
                  onClick={onNavigate}
                  title={label}
                  className={({ isActive }) => `nav-item${isActive ? ' active' : ''}`}
                >
                  <Icon className="nav-icon" size={18} />
                  <span className="nav-item-label">{label}</span>
                </NavLink>
              ))}
          </div>
        ))}
```

- [ ] **Passo 3: Criar a rota que trava o cenário**

Antes do componente que contém o `<Routes>` (por exemplo, logo depois de `FullPageLoading`),
acrescentar:

```jsx
// Rota do Regulamento de Serviço (recorte setorizado). Trava o cenário em "atual": a
// LOB vigente é a que este regulamento regulamenta, e comentário de um cenário NUNCA
// aparece no outro — deixar no padrão "futura" gravaria a manifestação no lugar errado,
// em silêncio.
function RegulamentoServicoRoute() {
  const { cenario, setCenario } = useScenario()
  useEffect(() => {
    if (cenario !== 'atual') setCenario('atual')
  }, [cenario, setCenario])
  return <Revisao initialDoc="reg" escopo="servico" />
}
```

- [ ] **Passo 4: Registrar a rota**

No bloco `<Routes>`, logo depois da linha de `/regulamento/revisao`:

```jsx
          <Route path="/regulamento/servico" element={<ProtectedRoute><RegulamentoServicoRoute /></ProtectedRoute>} />
```

- [ ] **Passo 5: Mandar o participante com escopo para a tela dele**

Trocar a rota raiz, que hoje é `<Route path="/" element={<Navigate to="/legislacoes" replace />} />`:

```jsx
          <Route path="/" element={<InicioPorEscopo />} />
```

E acrescentar o componente junto de `RegulamentoServicoRoute`:

```jsx
// Quem tem escopo não cai no Acervo dos 27 estados: vai direto ao documento dele.
function InicioPorEscopo() {
  const { user } = useAuth()
  const destino = user?.escopo === 'servico' ? '/regulamento/servico' : '/legislacoes'
  return <Navigate to={destino} replace />
}
```

- [ ] **Passo 6: Conferir que `useEffect` está importado**

```bash
grep -n "^import { useState, useEffect } from 'react'" src/App.jsx
```

Esperado: encontra a linha (já existe no topo do arquivo). Se não encontrar, acrescentar
`useEffect` ao import do React.

- [ ] **Passo 7: Build e testes**

```bash
npm test
npm run build
```

Esperado: PASS e build sem erro.

- [ ] **Passo 8: Commitar**

```bash
git add src/App.jsx
git commit -m "feat(escopo): rota /regulamento/servico, cenário travado e menu enxuto"
```

---

### Tarefa 6: Verificação ponta a ponta com evidência

**Arquivos:** nenhum (verificação).

**Contexto:** o repositório não tem testes de componente React — só `node --test` sobre
lógica pura. Portanto a prova desta entrega é **observada no navegador**, com screenshot,
conforme a regra de prova obrigatória do Wândrio. Nada aqui pode ser declarado pronto sem
a imagem correspondente colada na resposta.

- [ ] **Passo 1: Subir o ambiente**

```bash
npm run dev
```

Esperado: servidor em `http://localhost:5173`.

- [ ] **Passo 2: Criar o participante de teste no Firestore**

No console do Firebase (projeto `revisao-minuta-cbmro-6f248`, **perfil Chrome
Institucional**), coleção `members`, criar/editar um documento com o e-mail de teste:

```
ativo:  true          (boolean)
nome:   "Teste Escopo Serviço"
role:   "participante"
escopo: "servico"     (string)
```

- [ ] **Passo 3: Destravar o Regulamento para não-administrador**

Entrar como **administrador**, ir a `/regulamento/revisao` e clicar no botão que diz
"Comissão NÃO pode comentar o Regulamento ainda (clique para abrir)". Confirmar que o
rótulo passa a "Comissão PODE comentar o Regulamento".

Sem isto o participante vê "Regulamento em preparação" e a reunião morre na largada
(`Revisao.jsx:164` — a chave `config/revisao.regulamentoAberto` é *fail-closed*).

- [ ] **Passo 4: Provar a tela do participante (com escopo)**

Entrar com a conta de teste e capturar screenshot mostrando, na mesma imagem:
- menu com **dois** itens apenas (Regulamento de Serviço, Manual de uso);
- **sem** o seletor de cenário;
- a nota de escopo no topo;
- o título "Minuta do Regulamento de Serviço".

- [ ] **Passo 5: Provar a ordem dos capítulos e a ausência das faixas de Parte**

Percorrer o documento e conferir, contra a tabela da spec:
1. Das Disposições Preliminares · 2. Do Serviço Operacional · 3. Da Central de Operações e
do Teledespacho · 4. Do Serviço Interno e de Dia · 5. Das Atribuições das Funções ·
6. Da Segurança Contra Incêndio e Pânico · 7. Das Disposições Finais.

Confirmar que **nenhuma faixa vermelha "PARTE I" ou "PARTE II"** aparece. Screenshot do
sumário lateral com os 7 capítulos e screenshot do último capítulo.

- [ ] **Passo 6: Conferir a contagem de artigos**

O último artigo do documento deve ser o **Art. 185**, e a nota de escopo deve dizer
185 artigos no escopo e 228 fora. Se divergir, **reportar o número real** — nunca ajustar
a nota para bater. Screenshot do último artigo.

- [ ] **Passo 7: Provar o comentário ponta a ponta**

Comentar um artigo qualquer. No console do Firestore, abrir a coleção `suggestions` e
conferir no documento novo:
- `dispositivoId` começa com `reg:atual:` (cenário certo, documento certo);
- `autor.nome` é o participante de teste;
- `criadoEm` preenchido.

Colar o conteúdo do documento como evidência.

- [ ] **Passo 8: Provar que NÃO houve regressão para quem já usa o portal**

Entrar com a conta de **administrador** (sem `escopo`) e capturar screenshot de
`/legislacoes` mostrando o menu completo: os 3 blocos, o seletor de cenário e o Acervo.

Além disso, rodar a varredura de casos análogos exigida pela regra de prova:

```bash
grep -rn "buildArticles" src/ --include=*.jsx --include=*.js | grep -v test
```

Para cada tela que articula o Regulamento (Wizard, docx, Conferência, Subsídio),
confirmar pelo diff que **não foi tocada**:

```bash
git diff master --stat
```

Esperado: apenas `App.jsx`, `Revisao.jsx`, `auth.jsx`, `index.css`, os dois arquivos novos
de `escopoServico` e `NotaEscopoServico.jsx`, e os documentos em `docs/`.

- [ ] **Passo 9: Publicar (exceção autorizada)**

O Wândrio autorizou expressamente, em 2026-08-13, deploy direto por causa do prazo da
reunião — exceção à regra 4 do crachá (este repositório é compartilhado com o Ten. Tiago
e normalmente exige PR com revisão). A exceção fica registrada na mensagem do merge, e o
Ten. Tiago deve ser avisado depois.

```bash
git checkout master
git merge --no-ff feat/regulamento-servico-escopo -m "feat: ambiente setorizado do Regulamento de Serviço

Recorte de 7 capítulos (Parte II + Segurança contra Incêndio, o serviço técnico
da CAT) sobre a LOB atual, para a reunião de apresentação aos responsáveis dos
COB e da CAT em 13/08/2026.

Merge direto no master autorizado expressamente pelo Cel. Wândrio em 13/08/2026,
em caráter excepcional, por causa do prazo da reunião — a regra do repositório é
PR com revisão do Ten. Tiago, que será avisado."
git push origin master
```

- [ ] **Passo 10: Confirmar a produção no ar**

```bash
curl -s -o /dev/null -w "%{http_code}\n" https://portal-comparativo-cbm-aticbmro.vercel.app/regulamento/servico
```

Esperado: `200`. Depois, abrir a URL de produção, entrar com a conta de teste e repetir os
Passos 4 e 6 **em produção** — o que funciona em `localhost` não é prova do que o grupo vai
ver na reunião. Screenshot de produção.

- [ ] **Passo 11: Entregar o link**

Invocar a skill `abrir-app` (`/abrir-app`) para entregar o link verificado ao Wândrio,
com a opção de celular via Tailscale.

---

## Depois da reunião (fora do escopo deste plano)

- Campo `escopo` na tela `/acessos`, para o Wândrio convidar sem depender do console.
- Consolidar as manifestações da reunião via a trilha de Decisões já existente.
- Avaliar gerar o `.docx` autônomo do Regulamento de Serviço a partir deste mesmo recorte.
- Avisar o Ten. Tiago do merge direto.
