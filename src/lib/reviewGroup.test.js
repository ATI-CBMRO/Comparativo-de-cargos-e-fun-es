import { test } from 'node:test'
import assert from 'node:assert/strict'
import {
  groupByDispositivo, countByDispositivo, countByChapter,
  docOfDispositivo, filterSuggestionsByDoc, filterFinalsByDoc,
  scenarioOfDispositivo, filterSuggestionsByScenario, filterFinalsByScenario,
} from './reviewGroup.js'
import { parseDispositivoId } from './dispositivoId.js'
import { chapterIdOf } from './minutaTargets.js'

const sugs = [
  { id: 'a', dispositivoId: 'cot#0', texto: 'x' },
  { id: 'b', dispositivoId: 'cot#0', texto: 'y' },
  { id: 'c', dispositivoId: 'cot#caput', texto: 'z' },
]

test('groupByDispositivo agrupa por dispositivoId', () => {
  const g = groupByDispositivo(sugs)
  assert.equal(g.get('cot#0').length, 2)
  assert.equal(g.get('cot#caput').length, 1)
  assert.equal(g.get('cot#0')[0].id, 'a')
})

test('countByDispositivo conta por dispositivoId', () => {
  const c = countByDispositivo(sugs)
  assert.equal(c.get('cot#0'), 2)
  assert.equal(c.get('cot#caput'), 1)
  assert.equal(c.get('inexistente'), undefined)
})

test('countByChapter agrupa por capítulo e separa abertas de resolvidas', () => {
  const sugestoes = [
    { dispositivoId: 'organ:cg/competencia#0' },
    { dispositivoId: 'organ:cg/competencia#1' },
    { dispositivoId: 'estrutura#caput' },
  ]
  const finals = new Map([
    ['organ:cg/competencia#0', { status: 'fechado' }],
    ['organ:cg/competencia#1', { status: 'em_aberto' }],
  ])
  const counts = countByChapter(sugestoes, finals, parseDispositivoId, chapterIdOf)
  assert.deepEqual(counts.get('organ:cg'), { open: 1, resolved: 1 })
  assert.deepEqual(counts.get('estrutura'), { open: 1, resolved: 0 })
})

test('countByChapter sem sugestões devolve Map vazio', () => {
  const counts = countByChapter([], new Map(), parseDispositivoId, chapterIdOf)
  assert.equal(counts.size, 0)
})

test('docOfDispositivo reconhece prefixo reg: do Regulamento', () => {
  assert.equal(docOfDispositivo('reg:disposicoes-preliminares/mt-art-1#0'), 'reg')
})

test('docOfDispositivo trata qualquer editId sem prefixo reg: como RI', () => {
  assert.equal(docOfDispositivo('organ:cg/competencia#0'), 'ri')
  assert.equal(docOfDispositivo('estrutura#caput'), 'ri')
})

test('filterSuggestionsByDoc separa sugestões do RI e do Regulamento', () => {
  const suggestions = [
    { id: 'a', dispositivoId: 'organ:cg/competencia#0' },
    { id: 'b', dispositivoId: 'reg:disposicoes-preliminares/mt-art-1#0' },
    { id: 'c', dispositivoId: 'estrutura#caput' },
  ]
  const ri = filterSuggestionsByDoc(suggestions, 'ri')
  const reg = filterSuggestionsByDoc(suggestions, 'reg')
  assert.deepEqual(ri.map(s => s.id), ['a', 'c'])
  assert.deepEqual(reg.map(s => s.id), ['b'])
})

test('filterFinalsByDoc separa o Map de textos finais por documento', () => {
  const finals = new Map([
    ['organ:cg/competencia#0', { status: 'fechado' }],
    ['reg:disposicoes-preliminares/mt-art-1#0', { status: 'em_aberto' }],
  ])
  const ri = filterFinalsByDoc(finals, 'ri')
  const reg = filterFinalsByDoc(finals, 'reg')
  assert.equal(ri.size, 1)
  assert.equal(ri.get('organ:cg/competencia#0').status, 'fechado')
  assert.equal(reg.size, 1)
  assert.equal(reg.get('reg:disposicoes-preliminares/mt-art-1#0').status, 'em_aberto')
})

test('filterSuggestionsByDoc/filterFinalsByDoc com listas vazias devolvem vazio', () => {
  assert.deepEqual(filterSuggestionsByDoc([], 'ri'), [])
  assert.equal(filterFinalsByDoc(new Map(), 'reg').size, 0)
})

test('scenarioOfDispositivo: futura (sem marcador) × atual (com marcador)', () => {
  // futura — RI e Regulamento sem 'atual'
  assert.equal(scenarioOfDispositivo('organ:cg/competencia#0'), 'futura')
  assert.equal(scenarioOfDispositivo('reg:disposicoes/mt-art-1#0'), 'futura')
  // atual — RI com prefixo 'atual:' e Regulamento com 'reg:atual:'
  assert.equal(scenarioOfDispositivo('atual:organ:cg/competencia#0'), 'atual')
  assert.equal(scenarioOfDispositivo('reg:atual:cg/cg-caput#0'), 'atual')
})

test('filterSuggestionsByScenario separa os cenários', () => {
  const s = [
    { id: '1', dispositivoId: 'organ:cg/competencia#0' },        // futura
    { id: '2', dispositivoId: 'atual:organ:cg/competencia#0' },  // atual
    { id: '3', dispositivoId: 'reg:atual:cg/cg-caput#0' },       // atual
  ]
  assert.deepEqual(filterSuggestionsByScenario(s, 'futura').map(x => x.id), ['1'])
  assert.deepEqual(filterSuggestionsByScenario(s, 'atual').map(x => x.id), ['2', '3'])
})

test('filterFinalsByScenario separa os textos finais por cenário', () => {
  const finals = new Map([
    ['organ:cg/competencia#0', { status: 'fechado' }],       // futura
    ['atual:organ:cg/competencia#0', { status: 'aberto' }],  // atual
  ])
  assert.equal(filterFinalsByScenario(finals, 'futura').size, 1)
  assert.equal(filterFinalsByScenario(finals, 'atual').size, 1)
  assert.ok(filterFinalsByScenario(finals, 'atual').has('atual:organ:cg/competencia#0'))
})

// Finding 3 (revisão final do branch fix/regulamento-servico-fase2, 2026-08-18):
// se-art-113/se-art-48/se-art-49 foram removidos do documento numa tarefa anterior, mas
// as sugestões sobre eles continuam existindo no Firestore. Sem filtro, `countByChapter`
// as conta pelo chapterId derivado do editId mesmo sem o artigo mais existir na estrutura
// atual — inflando o número do trilho de capítulos com comentários que o leitor nunca vai
// conseguir abrir. `editIdsValidos` (5º parâmetro opcional) resolve isso no código, sem
// tocar o Firestore.
const editIdValido = 'reg:servico-operacional/se-art-30'
const editIdRemovido = 'reg:servico-operacional/se-art-113'
const chapterIdServico = chapterIdOf(editIdValido) // mesmo capítulo para os dois editIds

const sugestoesComOrfa = () => ([
  { dispositivoId: `${editIdValido}#caput` }, // fica aberta (sem final)
  { dispositivoId: `${editIdValido}#0` },     // fica resolvida (final "fechado")
  { dispositivoId: `${editIdRemovido}#0` },   // órfã: editId não existe mais na estrutura
])

test('countByChapter sem editIdsValidos conta todas as sugestões (comportamento de sempre)', () => {
  const map = countByChapter(sugestoesComOrfa(), new Map(), parseDispositivoId, chapterIdOf)
  const entry = map.get(chapterIdServico)
  assert.equal(entry.open, 3)
  assert.equal(entry.resolved, 0)
})

test('countByChapter com editIdsValidos ignora sugestão de editId removido (não conta aberta nem resolvida)', () => {
  const editIdsValidos = new Set([editIdValido]) // se-art-113 NÃO está no set
  // Mesmo com um final "fechado" associado, a sugestão órfã não deve contar em lado
  // nenhum — o filtro descarta ANTES de olhar `finals`.
  const finals = new Map([[`${editIdRemovido}#0`, { status: 'fechado' }]])
  const map = countByChapter(sugestoesComOrfa(), finals, parseDispositivoId, chapterIdOf, editIdsValidos)
  const entry = map.get(chapterIdServico)
  assert.equal(entry.open, 2)     // caput + #0 do editId válido, nenhum tem final aqui
  assert.equal(entry.resolved, 0) // a sugestão órfã (com final "fechado") não conta
})

test('countByChapter com editIdsValidos conta normalmente sugestão de editId válido, respeitando finals', () => {
  const editIdsValidos = new Set([editIdValido]) // se-art-113 continua fora
  const finals = new Map([[`${editIdValido}#0`, { status: 'fechado' }]])
  const map = countByChapter(sugestoesComOrfa(), finals, parseDispositivoId, chapterIdOf, editIdsValidos)
  const entry = map.get(chapterIdServico)
  assert.equal(entry.open, 1)     // caput, sem final
  assert.equal(entry.resolved, 1) // #0, com final "fechado"
})
