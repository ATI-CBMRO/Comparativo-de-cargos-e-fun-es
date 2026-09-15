import test from 'node:test'
import assert from 'node:assert/strict'
import { capitalizarFrases } from './formatacaoTexto.js'

test('capitalizarFrases: início do texto, inclusive após marcador de alínea/parágrafo', () => {
  assert.equal(capitalizarFrases('realizar serviços de prevenção;'), 'Realizar serviços de prevenção;')
  assert.equal(capitalizarFrases('a) em aglomerados urbanos;'), 'a) Em aglomerados urbanos;')
  assert.equal(capitalizarFrases('§ 1º durante o serviço.'), '§ 1º Durante o serviço.')
  assert.equal(capitalizarFrases('a) 6 horas de trabalho;'), 'a) 6 horas de trabalho;')
  assert.equal(capitalizarFrases('Já maiúscula.'), 'Já maiúscula.')
  assert.equal(capitalizarFrases(''), '')
})

test('capitalizarFrases: após ponto final, mas não após abreviatura, número ou letra isolada', () => {
  assert.equal(capitalizarFrases('inclusive nos dias não úteis. porém, o militar deverá informar.'), 'Inclusive nos dias não úteis. Porém, o militar deverá informar.')
  assert.equal(capitalizarFrases('nos termos do art. 35 da Lei nº 2.204/2009. cabendo ao cmt. do socorro'), 'Nos termos do art. 35 da Lei nº 2.204/2009. Cabendo ao cmt. do socorro')
  assert.equal(capitalizarFrases('as informações: a. qual foi o fato; b. quantidade de efetivo'), 'As informações: a. qual foi o fato; b. quantidade de efetivo')
  assert.equal(capitalizarFrases('Decreto nº 8.134, de 18 de dezembro de 1997. observadas as regras'), 'Decreto nº 8.134, de 18 de dezembro de 1997. Observadas as regras')
  assert.equal(capitalizarFrases('pergunta? sim! resposta.'), 'Pergunta? Sim! Resposta.')
})
