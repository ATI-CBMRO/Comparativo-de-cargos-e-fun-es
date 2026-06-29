import { test } from 'node:test'
import assert from 'node:assert/strict'
import { normalizeEmail, situacaoMembro, contaStatus } from './membersStats.js'

test('normalizeEmail apara espaços e baixa a caixa', () => {
  assert.equal(normalizeEmail('  Fulano@CBM.RO.gov.BR '), 'fulano@cbm.ro.gov.br')
  assert.equal(normalizeEmail(undefined), '')
  assert.equal(normalizeEmail(null), '')
})

test('situacaoMembro: ativo=false sempre é bloqueado', () => {
  assert.equal(situacaoMembro({ ativo: false, status: 'cadastrado' }), 'bloqueado')
  assert.equal(situacaoMembro({ ativo: false, status: 'convidado' }), 'bloqueado')
})

test('situacaoMembro: ativo segue o status', () => {
  assert.equal(situacaoMembro({ ativo: true, status: 'cadastrado' }), 'cadastrado')
  assert.equal(situacaoMembro({ ativo: true, status: 'convidado' }), 'convidado')
})

test('contaStatus soma por situação', () => {
  const members = [
    { ativo: true, status: 'cadastrado' },
    { ativo: true, status: 'cadastrado' },
    { ativo: true, status: 'convidado' },
    { ativo: false, status: 'cadastrado' },
  ]
  assert.deepEqual(contaStatus(members), { total: 4, cadastrados: 2, convidados: 1, bloqueados: 1 })
})
