import test from 'node:test'
import assert from 'node:assert/strict'
import { tokens, jaccard, agruparSemelhantes, unidadesDoArtigo } from './dispositivosSemelhantes.js'

test('tokens: remove marcador, acento, pontuação e palavras curtas/vazias', () => {
  assert.deepEqual(tokens('I - Solicitar o comparecimento da perícia de trânsito;'), ['solicitar', 'comparecimento', 'pericia', 'transito'])
  assert.deepEqual(tokens('§ 1º Ao final do serviço.'), ['final', 'servico'])
})

test('jaccard e agrupamento: idênticos, quase idênticos e distintos', () => {
  const u = [
    { artigo: 1, rotulo: 'Art. 1º, caput', texto: 'Os casos omissos serão resolvidos em conjunto pelo Comandante Operacional de Bombeiros e pelo Comandante da OBM.' },
    { artigo: 2, rotulo: 'Art. 2º, caput', texto: 'Os casos omissos serão resolvidos em conjunto pelo Comandante Operacional de Bombeiros e pelo Comandante da OBM.' },
    { artigo: 3, rotulo: 'Art. 3º, caput', texto: 'Esses serviços serão realizados no Quartel de cada OBM com abrangência em toda sua área de jurisdição.' },
    { artigo: 4, rotulo: 'Art. 4º, caput', texto: 'Esses serviços serão realizados no Quartel de cada OBM com abrangência em toda a área de jurisdição da Unidade.' },
    { artigo: 5, rotulo: 'Art. 5º, inciso I', texto: 'Diretor;' },
    { artigo: 6, rotulo: 'Art. 6º, inciso I', texto: 'Diretor;' },
    { artigo: 7, rotulo: 'Art. 7º, caput', texto: 'As viaturas operacionais somente poderão ser empregadas em atividades exclusivas de prevenção e combate a incêndio.' },
  ]
  assert.equal(jaccard(tokens(u[0].texto), tokens(u[1].texto)), 1)
  const grupos = agruparSemelhantes(u)
  assert.equal(grupos.length, 2)
  assert.equal(grupos[0].identicos, true)
  assert.deepEqual(grupos[0].itens.map(i => i.artigo), [1, 2])
  assert.match(grupos[0].recomendacao, /idêntico/)
  assert.equal(grupos[1].identicos, false)
  assert.deepEqual(grupos[1].itens.map(i => i.artigo), [3, 4])
  assert.ok(!grupos.some(g => g.itens.some(i => i.artigo === 5)), 'unidades curtas nunca entram')
})

test('competências paralelas (Compete ao X × Compete ao Y) recebem recomendação de manter as duas', () => {
  const u = [
    { artigo: 1, rotulo: 'Art. 1º, inciso I', texto: 'cumprir fielmente as determinações dos escalões superiores, no âmbito de suas atribuições.', caputArtigo: 'Compete ao Comandante de Grupamento de Bombeiro Militar:' },
    { artigo: 2, rotulo: 'Art. 2º, inciso I', texto: 'cumprir fielmente as determinações dos escalões superiores, no âmbito de suas atribuições.', caputArtigo: 'Compete ao Comandante de Subgrupamento de Bombeiro Militar:' },
  ]
  assert.equal(agruparSemelhantes(u).length, 0, 'paralelas ficam fora do quadro por padrão')
  assert.equal(agruparSemelhantes(u).paralelosDescartados, 1)
  const [g] = agruparSemelhantes(u, { incluirParalelas: true })
  assert.equal(g.paralelas, true)
  assert.match(g.recomendacao, /Comandante de Grupamento de Bombeiro Militar × Comandante de Subgrupamento de Bombeiro Militar/)
})

test('unidadesDoArtigo rotula caput, incisos (só os numerados), alíneas e parágrafos', () => {
  const art = { caput: 'Caput.', incisos: [
    { text: 'um;', ownMarker: false }, { text: 'a) alínea;', ownMarker: true, alinea: true },
    { text: 'dois.', ownMarker: false }, { text: '§ 1º Parágrafo.', ownMarker: true },
  ] }
  assert.deepEqual(unidadesDoArtigo(12, art, 'CAP').map(u => u.rotulo), ['Art. 12, caput', 'Art. 12, inciso I', 'Art. 12, alínea a)', 'Art. 12, inciso II', 'Art. 12, § 1º'])
})
