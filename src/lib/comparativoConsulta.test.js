import test from 'node:test'
import assert from 'node:assert/strict'
import fs from 'node:fs'
import path from 'node:path'
import { compararVersoes, resumoComparativo } from './comparativoConsulta.js'
import { filtrarEstruturaPorEscopo } from './escopoServico.js'

const cap = (id, articles, suprimidos) => ({ id, chapterTitle: id.toUpperCase(), articles, ...(suprimidos ? { suprimidos } : {}) })
const art = (id, caput, extra = {}) => ({ id, editId: `reg:atual:t/${id}`, caput, items: [], ...extra })

test('compararVersoes classifica igual, corrigido, alterado, reescrito, incluído e suprimido na ordem certa', () => {
  const consulta = { chapters: [cap('reg:atual:t', [
    art('a-1', 'um'), art('a-2', 'dois'), art('a-3', 'três'), art('a-4', 'quatro'), art('a-5', 'cinco'),
  ])] }
  const atual = { chapters: [cap('reg:atual:t', [
    art('a-1', 'um', { corrigido: true }),
    art('a-2-r1', 'dois novo', { substitui: 'a-2', proposta: true, nota: 'PROPOSTA' }),
    art('a-2-r2', 'dois novo b', { substitui: 'a-2' }),
    art('a-4', 'quatro alterado', { alterado: 'texto final' }),
    art('a-4-c1', 'novo', { incluido: true }),
    art('a-5', 'cinco'),
  ], [{ id: 'a-3', motivo: 'Excluir' }])] }
  const out = compararVersoes(consulta, atual)
  const tipos = out[0].entradas.map(e => `${e.tipo}:${e.antes?.id ?? '-'}>${e.depois?.id ?? '-'}`)
  assert.deepEqual(tipos, [
    'corrigido:a-1>a-1', 'reescrito:a-2>a-2-r1', 'reescrito:->a-2-r2', 'suprimido:a-3>-',
    'alterado:a-4>a-4', 'incluido:->a-4-c1', 'igual:a-5>a-5',
  ])
  assert.equal(out[0].entradas[1].proposta, true)
  assert.equal(out[0].entradas[3].motivo, 'Excluir')
  assert.deepEqual(out[0].entradas.map(e => e.numDepois), [1, 2, 3, null, 4, 5, 6])
  assert.deepEqual(out[0].entradas.map(e => e.numAntes), [1, 2, null, 3, 4, null, 5])
  const r = resumoComparativo(out)
  assert.deepEqual(r, { igual: 1, corrigido: 1, alterado: 1, reescrito: 2, incluido: 1, suprimido: 1, propostas: 1 })
})

test('recorte real: toda entrada da atual e da consulta aparece uma vez', () => {
  const pc = path.resolve('database/atual/regulamento_structure_consulta.json')
  const pa = path.resolve('database/atual/regulamento_structure.json')
  if (!fs.existsSync(pc) || !fs.existsSync(pa)) return
  const rc = filtrarEstruturaPorEscopo(JSON.parse(fs.readFileSync(pc, 'utf8')), 'servico')
  const ra = filtrarEstruturaPorEscopo(JSON.parse(fs.readFileSync(pa, 'utf8')), 'servico')
  const out = compararVersoes(rc, ra)
  const nAtual = ra.chapters.reduce((n, c) => n + c.articles.length, 0)
  const nConsulta = rc.chapters.reduce((n, c) => n + c.articles.length, 0)
  const entradas = out.flatMap(c => c.entradas)
  assert.equal(entradas.filter(e => e.depois).length, nAtual)
  assert.equal(entradas.filter(e => e.antes).length, nConsulta)
  const r = resumoComparativo(out)
  assert.ok(r.reescrito >= 13 && r.incluido >= 5 && r.suprimido >= 8 && r.propostas === 1, JSON.stringify(r))
})
