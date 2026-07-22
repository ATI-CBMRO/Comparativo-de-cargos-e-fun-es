import test from 'node:test'
import assert from 'node:assert/strict'
import { buildRegulamentoTree } from './regulamentoTree.js'

const CHAPTERS = [
  { id: 'reg:disposicoes-preliminares', chapterTitle: 'DAS DISPOSIÇÕES PRELIMINARES', parte: 'geral', articles: [{ caput: 'Art. 1º ...' }, { caput: 'Art. 2º ...' }] },
  { id: 'reg:pessoal-quadros', chapterTitle: 'DO PESSOAL', parte: 'geral', articles: [{ caput: 'Art. 3º ...' }] },
  { id: 'reg:servico-operacional', chapterTitle: 'DO SERVIÇO OPERACIONAL', parte: 'servico', articles: [{ caput: 'Art. 4º ...' }] },
]

test('raiz sintética com as 2 Partes na ordem geral → servico', () => {
  const root = buildRegulamentoTree(CHAPTERS)
  assert.equal(root.synthetic, true)
  assert.equal(root.label, 'Regulamento Geral do CBMRO')
  assert.deepEqual(root.children.map(p => p.label), ['PARTE I — GERAL', 'PARTE II — DO SERVIÇO'])
  assert.ok(root.children.every(p => p.synthetic === true && !p.chapterId))
})

test('temas na ordem do documento, clicáveis, com contagem de artigos', () => {
  const [pI, pII] = buildRegulamentoTree(CHAPTERS).children
  assert.deepEqual(pI.children.map(t => t.chapterId), ['reg:disposicoes-preliminares', 'reg:pessoal-quadros'])
  assert.equal(pI.children[0].label, 'DAS DISPOSIÇÕES PRELIMINARES')
  assert.equal(pI.children[0].sigla, '2 art.')
  assert.equal(pI.children[1].sigla, '1 art.')
  assert.deepEqual(pII.children.map(t => t.chapterId), ['reg:servico-operacional'])
  assert.deepEqual(pI.children[0].children, [])
})

test('capítulo sem parte reconhecida cai em "Outros"; sem esse caso, "Outros" não existe', () => {
  const comOrfao = buildRegulamentoTree([...CHAPTERS, { id: 'reg:x', chapterTitle: 'X', articles: [] }])
  assert.deepEqual(comOrfao.children.map(p => p.label), ['PARTE I — GERAL', 'PARTE II — DO SERVIÇO', 'Outros'])
  assert.equal(comOrfao.children[2].children[0].sigla, '0 art.')
  assert.equal(buildRegulamentoTree(CHAPTERS).children.length, 2)
})

test('entrada vazia/nula devolve raiz sem filhos', () => {
  assert.deepEqual(buildRegulamentoTree([]).children, [])
  assert.deepEqual(buildRegulamentoTree(null).children, [])
})
