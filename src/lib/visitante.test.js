import test from 'node:test'
import assert from 'node:assert/strict'
import {
  BASE_PUBLICA, LIMITES, CHAVE_LOCAL,
  normalizarVisitante, rotaEstado, rotaListaEstados,
  lerVisitanteLocal, gravarVisitanteLocal, limparVisitanteLocal,
} from './visitante.js'

// --- validação do cadastro -------------------------------------------------

test('normalizarVisitante apara espaços e normaliza o e-mail', () => {
  const r = normalizarVisitante({
    nome: '  Maria da Silva  ', email: '  Maria@Exemplo.COM ', instituicao: ' CBMPA ',
  })
  assert.equal(r.ok, true)
  assert.deepEqual(r.dados, { nome: 'Maria da Silva', email: 'maria@exemplo.com', instituicao: 'CBMPA' })
})

test('normalizarVisitante exige nome, e-mail e instituição', () => {
  assert.equal(normalizarVisitante({ nome: '  ', email: 'a@b.com', instituicao: 'X' }).ok, false)
  assert.equal(normalizarVisitante({ nome: 'A', email: '   ', instituicao: 'X' }).ok, false)
  assert.equal(normalizarVisitante({ nome: 'A', email: 'a@b.com', instituicao: '' }).ok, false)
})

test('normalizarVisitante devolve mensagem em português, nunca só ok:false', () => {
  const r = normalizarVisitante({ nome: '', email: '', instituicao: '' })
  assert.equal(r.ok, false)
  assert.equal(typeof r.erro, 'string')
  assert.ok(r.erro.length > 0)
})

test('normalizarVisitante recusa e-mail sem formato mínimo', () => {
  const r = normalizarVisitante({ nome: 'A', email: 'sem-arroba', instituicao: 'X' })
  assert.equal(r.ok, false)
  assert.match(r.erro, /e-mail/i)
})

// Os limites espelham a regra do Firestore (spec, seção 3): campo maior que o limite
// seria RECUSADO pelo banco. Barrar aqui evita uma falha silenciosa na gravação.
test('normalizarVisitante recusa campo acima do limite da regra do Firestore', () => {
  const gigante = 'x'.repeat(LIMITES.nome + 1)
  assert.equal(normalizarVisitante({ nome: gigante, email: 'a@b.com', instituicao: 'X' }).ok, false)
  assert.equal(
    normalizarVisitante({ nome: 'A', email: 'a@b.com', instituicao: 'y'.repeat(LIMITES.instituicao + 1) }).ok,
    false,
  )
})

test('normalizarVisitante aceita exatamente no limite', () => {
  const noLimite = 'x'.repeat(LIMITES.nome)
  assert.equal(normalizarVisitante({ nome: noLimite, email: 'a@b.com', instituicao: 'X' }).ok, true)
})

// --- resolução de rotas ----------------------------------------------------

test('rotaEstado sem base devolve a rota do membro, inalterada', () => {
  assert.equal(rotaEstado('', 'ro'), '/estados/ro')
})

test('rotaEstado com a base pública prefixa', () => {
  assert.equal(rotaEstado(BASE_PUBLICA, 'ro'), '/acervo-publico/estados/ro')
})

// O CASO QUE UM PREFIXO CEGO ERRARIA (spec, seção 1): /estados (a lista StatesList) não
// existe no recorte público. Prefixar daria '/acervo-publico/estados', rota inexistente.
test('rotaListaEstados: membro volta para a lista, visitante volta para o acervo', () => {
  assert.equal(rotaListaEstados(''), '/estados')
  assert.equal(rotaListaEstados(BASE_PUBLICA), '/acervo-publico')
})

// --- persistência local ----------------------------------------------------

function storageFake(inicial = {}) {
  const dados = { ...inicial }
  return {
    getItem: (k) => (k in dados ? dados[k] : null),
    setItem: (k, v) => { dados[k] = String(v) },
    removeItem: (k) => { delete dados[k] },
    _dados: dados,
  }
}

test('gravarVisitanteLocal e lerVisitanteLocal fazem a volta completa', () => {
  const s = storageFake()
  gravarVisitanteLocal(s, { uid: 'abc123', nome: 'Maria da Silva' })
  assert.deepEqual(lerVisitanteLocal(s), { uid: 'abc123', nome: 'Maria da Silva' })
})

test('lerVisitanteLocal devolve null quando não há nada gravado', () => {
  assert.equal(lerVisitanteLocal(storageFake()), null)
})

test('lerVisitanteLocal devolve null (sem lançar) se o conteúdo estiver corrompido', () => {
  assert.equal(lerVisitanteLocal(storageFake({ [CHAVE_LOCAL]: 'isto não é json' })), null)
})

test('lerVisitanteLocal devolve null se faltar uid ou nome', () => {
  assert.equal(lerVisitanteLocal(storageFake({ [CHAVE_LOCAL]: '{"nome":"Maria"}' })), null)
  assert.equal(lerVisitanteLocal(storageFake({ [CHAVE_LOCAL]: '{"uid":"abc"}' })), null)
})

test('lerVisitanteLocal devolve null quando não há storage (ambiente sem localStorage)', () => {
  assert.equal(lerVisitanteLocal(null), null)
})

test('limparVisitanteLocal remove a chave e não lança sem storage', () => {
  const s = storageFake({ [CHAVE_LOCAL]: '{"uid":"a","nome":"b"}' })
  limparVisitanteLocal(s)
  assert.equal(lerVisitanteLocal(s), null)
  assert.doesNotThrow(() => limparVisitanteLocal(null))
})
