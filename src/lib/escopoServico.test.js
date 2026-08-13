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
