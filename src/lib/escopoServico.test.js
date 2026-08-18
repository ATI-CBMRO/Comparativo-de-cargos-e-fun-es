import test from 'node:test'
import assert from 'node:assert/strict'
import {
  TEMAS_SERVICO, temaDoCapitulo, filtrarEstruturaPorEscopo, rotaLiberadaNoEscopo,
  resumoForaDoEscopo,
} from './escopoServico.js'

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
    'atribuicoes-funcoes',
    'servico-operacional',
    'central-operacoes-193',
    'servico-interno-dia',
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

test('sem escopo, toda rota é liberada (comportamento de hoje, intocado)', () => {
  assert.equal(rotaLiberadaNoEscopo('/minuta', null), true)
  assert.equal(rotaLiberadaNoEscopo('/regulamento/conferencia', undefined), true)
  assert.equal(rotaLiberadaNoEscopo('/legislacoes', 'inexistente'), true)
})

test('escopo de serviço libera só o documento, o subsídio, o manual e as telas de entrada', () => {
  for (const p of ['/', '/regulamento/servico', '/regulamento/servico/subsidio', '/manual', '/login', '/solicitar-acesso']) {
    assert.equal(rotaLiberadaNoEscopo(p, 'servico'), true, `deveria liberar ${p}`)
  }
})

test('escopo de serviço fecha as trilhas, o acervo e o organograma', () => {
  for (const p of [
    '/minuta', '/minuta/conferencia', '/minuta/decisoes', '/minuta/revisao',
    '/regulamento', '/regulamento/conferencia', '/regulamento/decisoes',
    '/regulamento/revisao', '/regulamento/subsidio',
    '/legislacoes', '/organograma', '/acessos', '/comparar', '/estados/ro',
  ]) {
    assert.equal(rotaLiberadaNoEscopo(p, 'servico'), false, `deveria fechar ${p}`)
  }
})

test('barra final e maiúsculas não furam a guarda', () => {
  assert.equal(rotaLiberadaNoEscopo('/regulamento/servico/', 'servico'), true)
  assert.equal(rotaLiberadaNoEscopo('/MINUTA', 'servico'), false)
  assert.equal(rotaLiberadaNoEscopo('/Manual', 'servico'), true)
})

test('prefixo parecido não libera por engano', () => {
  // "/manualzinho" não pode passar só por começar com "/manual".
  assert.equal(rotaLiberadaNoEscopo('/manualzinho', 'servico'), false)
  assert.equal(rotaLiberadaNoEscopo('/regulamento/servicos', 'servico'), false)
})

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

test('resumoForaDoEscopo separa capítulos inteiros de artigos cortados', () => {
  const completa = comCapituloMisto()
  const r = resumoForaDoEscopo(completa, filtrarEstruturaPorEscopo(completa, 'servico'), 'servico')
  assert.equal(r.artigosCortadosNoEscopo, 2, 'mt-art-62 e mt-art-63 saíram do capítulo misto')
  assert.deepEqual(r.capitulosFora, [], 'a estrutura-fake só tem capítulos do escopo')
})
