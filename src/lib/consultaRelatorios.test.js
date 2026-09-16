import test from 'node:test'
import assert from 'node:assert/strict'
import {
  articular, textoFinalDe, aplicarFinais, indexarRecorte, localizar, autorDe,
  selecionarInteracoes, resumoParticipacao, quadroAnalise, mapaFinais, paraData, aplicacaoPorArtigo,
} from './consultaRelatorios.js'
import { montarReestruturada, ESTRUTURA } from './regulamentoReestruturado.js'
import { filtrarEstruturaPorEscopo } from './escopoServico.js'
import fs from 'node:fs'
import path from 'node:path'

const recorteFake = () => ({
  chapters: [
    { id: 'reg:atual:disposicoes-preliminares', chapterTitle: 'DAS DISPOSIÇÕES PRELIMINARES', articles: [
      { id: 'mt-art-1', editId: 'reg:atual:disposicoes-preliminares/mt-art-1', caput: 'Caput um.', items: [] },
      { id: 'mt-art-3', editId: 'reg:atual:disposicoes-preliminares/mt-art-3', caput: 'Compete:', items: [{ text: 'I - alfa;' }, { text: '' }, { text: '§ 1º Beta.' }] },
    ] },
    { id: 'reg:atual:servico-operacional', chapterTitle: 'DO SERVIÇO OPERACIONAL', articles: [
      { id: 'se-art-24', editId: 'reg:atual:servico-operacional/se-art-24', caput: 'Superior de Dia.', items: [{ text: '§1.º Visto.' }] },
    ] },
  ],
})

test('articular preserva o índice original dos incisos e pula vazios', () => {
  const art = articular(recorteFake().chapters[0].articles[1])
  assert.equal(art.incisos.length, 2)
  assert.deepEqual(art.incisos.map(i => i.index), [0, 2])
  assert.equal(art.incisos[1].ownMarker, true)
})

test('textoFinalDe distingue vazio, Excluir e texto', () => {
  assert.equal(textoFinalDe(null), null)
  assert.equal(textoFinalDe({ status: 'em_aberto', texto: 'x' }), null)
  assert.deepEqual(textoFinalDe({ status: 'fechado', texto: '  ' }), { vazio: true })
  assert.deepEqual(textoFinalDe({ status: 'fechado', texto: 'Excluir.' }), { suprimido: true })
  assert.deepEqual(textoFinalDe({ status: 'fechado', texto: 'Novo' }), { texto: 'Novo' })
})

test('aplicarFinais: vazio mantém, Excluir suprime, texto substitui', () => {
  const art = articular(recorteFake().chapters[0].articles[1])
  const finals = new Map([
    ['reg:atual:disposicoes-preliminares/mt-art-3#caput', { status: 'fechado', texto: '' }],
    ['reg:atual:disposicoes-preliminares/mt-art-3#0', { status: 'fechado', texto: 'I - novo;' }],
  ])
  const out = aplicarFinais(art, finals)
  assert.equal(out.caput, 'Compete:')
  assert.equal(out.conferido, true)
  assert.equal(out.incisos[0].text, 'I - novo;')
  const sup = aplicarFinais(art, new Map([['reg:atual:disposicoes-preliminares/mt-art-3#caput', { status: 'fechado', texto: 'Excluir' }]]))
  assert.equal(sup.suprimido, true)
  assert.equal(sup.incisos.length, 0)
})

test('indexarRecorte numera continuamente e localizar acha caput/inciso/parágrafo', () => {
  const idx = indexarRecorte(recorteFake())
  assert.equal(idx.get('reg:atual:servico-operacional/se-art-24').numero, 3)
  assert.equal(localizar(idx, 'reg:atual:disposicoes-preliminares/mt-art-3#caput').rotulo, 'Art. 2º, caput')
  assert.equal(localizar(idx, 'reg:atual:disposicoes-preliminares/mt-art-3#0').rotulo, 'Art. 2º, inciso I')
  assert.equal(localizar(idx, 'reg:atual:disposicoes-preliminares/mt-art-3#2').rotulo, 'Art. 2º, parágrafo')
  assert.equal(localizar(idx, 'reg:atual:disposicoes-preliminares/mt-art-3#1').rotulo, 'Art. 2º, item 1 (não localizado)')
  assert.equal(localizar(idx, 'reg:atual:organizacao-geral/ro-art-2#7').noRecorte, false)
})

test('autorDe casa por uid, cai para o nome e nunca expõe e-mail', () => {
  const membros = [{ uid: 'u1', nome: 'Fulano', nomeGuerra: 'Ful', unidade: '1º GBM', comando: 'COB', cidade: 'PVH', escopo: 'servico', email: 'x@y' }]
  const a = autorDe({ autorUid: 'u1', autorNome: 'Outro' }, membros)
  assert.equal(a.nome, 'Fulano')
  assert.equal(a.unidade, '1º GBM — COB — PVH')
  assert.equal(a.consultado, true)
  assert.equal('email' in a, false)
  const b = autorDe({ autorUid: 'zz', autorNome: 'fulano' }, membros)
  assert.equal(b.nomeGuerra, 'Ful')
  const c = autorDe({ autorUid: 'zz', autorNome: 'Ninguém' }, membros)
  assert.equal(c.alcance, '(não cadastrado)')
})

test('selecionarInteracoes filtra recorte/cenário, ordena caput antes dos incisos e lê parecer/final', () => {
  const idx = indexarRecorte(recorteFake())
  const membros = [{ uid: 'u1', nome: 'Fulano', escopo: 'servico' }, { uid: 'u2', nome: 'Admin', role: 'admin' }]
  const sugestoes = [
    { id: 'a', dispositivoId: 'reg:atual:servico-operacional/se-art-24#0', texto: 'inciso', autorUid: 'u1', criadoEm: '2026-09-01T12:00:00Z', adminStatus: 'relevante' },
    { id: 'b', dispositivoId: 'reg:atual:servico-operacional/se-art-24#caput', texto: 'caput', autorUid: 'u2', criadoEm: '2026-09-02T12:00:00Z' },
    { id: 'c', dispositivoId: 'reg:atual:organizacao-geral/ro-art-2#7', texto: 'fora', autorUid: 'u1', criadoEm: '2026-09-02T12:00:00Z' },
    { id: 'd', dispositivoId: 'organ:cg/competencia#0', texto: 'RI', autorUid: 'u1', criadoEm: '2026-09-02T12:00:00Z' },
    { id: 'e', dispositivoId: 'reg:servico-operacional/se-art-24#caput', texto: 'futura', autorUid: 'u1', criadoEm: '2026-09-02T12:00:00Z' },
  ]
  const finals = mapaFinais([{ id: 'reg:atual:servico-operacional|se-art-24#caput', status: 'fechado', texto: 'Redigido.' }])
  // padrão: só quem tem escopo 'servico' — a sugestão 'b' é da administração do portal e fica de fora
  const soConsultados = selecionarInteracoes({ sugestoes, membros, indice: idx, finals })
  assert.deepEqual(soConsultados.map(r => r.firestoreId), ['a'])
  const out = selecionarInteracoes({ sugestoes, membros, indice: idx, finals, somenteConsultados: false })
  assert.deepEqual(out.map(r => r.firestoreId), ['b', 'a'])
  assert.equal(out[0].aplicacao.como, 'nenhuma')
  assert.equal(out[0].textoFinal, 'Redigido.')
  assert.equal(out[0].parecer, 'pendente')
  assert.equal(out[1].parecer, 'relevante')
  assert.equal(out[1].dispositivo, 'Art. 3º, parágrafo')
  const desde = selecionarInteracoes({ sugestoes, membros, indice: idx, finals, desde: new Date('2026-09-02T00:00:00Z'), somenteConsultados: false })
  assert.deepEqual(desde.map(r => r.firestoreId), ['b'])
  const resumo = resumoParticipacao(membros, out)
  assert.equal(resumo.cadastradosEscopo, 1)
  assert.equal(resumo.contribuintes, 1)
  assert.equal(resumo.dosConsultados, 1)
  assert.equal(resumo.daEquipe, 1)
  assert.deepEqual(resumo.pareceres, { relevante: 1, descartada: 0, pendente: 1 })
  assert.equal(resumo.aplicadas, 0)
  const quadro = quadroAnalise(out)
  assert.equal(quadro.length, 1)
  assert.equal(quadro[0].situacaoFinal, 'redigido')
  assert.equal(quadro[0].itens.length, 2)
})

test('selecionarInteracoes: aplicação deduzida por artigo, com registro explícito vencendo', () => {
  const idx = indexarRecorte(recorteFake())
  const atual = { curadoria: { atendimentos_artigos: { 'reg:atual:disposicoes-preliminares/mt-art-1': { como: 'incluido', nota: 'virou artigos novos' } } }, chapters: [
    { id: 'reg:atual:disposicoes-preliminares', suprimidos: [{ id: 'mt-art-1', motivo: 'dup' }], articles: [
      { id: 'mt-art-3-r1', editId: 'reg:atual:disposicoes-preliminares/mt-art-3-r1', substitui: 'mt-art-3', nota: 'LOB', caput: 'x', items: [] },
    ] },
    { id: 'reg:atual:servico-operacional', articles: [
      { id: 'se-art-24', editId: 'reg:atual:servico-operacional/se-art-24', alterado: 'redação', caput: 'y', items: [] },
    ] },
  ] }
  const porArtigo = aplicacaoPorArtigo(atual)
  assert.equal(porArtigo.get('reg:atual:disposicoes-preliminares/mt-art-3').como, 'reescrito')
  assert.equal(porArtigo.get('reg:atual:disposicoes-preliminares/mt-art-1').como, 'incluido') // registro explícito vence a dedução (suprimido)
  assert.equal(porArtigo.get('reg:atual:servico-operacional/se-art-24').como, 'redacao')
  const membros = [{ uid: 'u1', nome: 'Fulano', escopo: 'servico' }, { uid: 'u2', nome: 'Admin', role: 'admin' }]
  const sugestoes = [
    { id: 'cel', dispositivoId: 'reg:atual:disposicoes-preliminares/mt-art-3#caput', texto: '25 incisos', autorUid: 'u1', criadoEm: '2026-08-19T12:00:00Z' },
    { id: 'red', dispositivoId: 'reg:atual:servico-operacional/se-art-24#0', texto: 'x', autorUid: 'u1', criadoEm: '2026-08-19T12:00:00Z' },
    { id: 'sem', dispositivoId: 'reg:atual:disposicoes-preliminares/mt-art-1#caput', texto: 'y', autorUid: 'u1', criadoEm: '2026-08-19T12:00:00Z' },
    { id: 'adm', dispositivoId: 'reg:atual:disposicoes-preliminares/mt-art-1#caput', texto: 'interno', autorUid: 'u2', criadoEm: '2026-08-13T12:00:00Z' },
    { id: 'fora', dispositivoId: 'reg:atual:organizacao-geral/ro-art-2#1', texto: 'fora do recorte', autorUid: 'u1', criadoEm: '2026-08-19T12:00:00Z' },
  ]
  const out = selecionarInteracoes({ sugestoes, membros, indice: idx, finals: new Map(), aplicacaoArtigos: porArtigo })
  assert.deepEqual(out.map(r => r.firestoreId), ['sem', 'cel', 'red'])   // admin e fora do recorte ficam de fora
  assert.equal(out[0].aplicacao.como, 'incluido')             // registro explícito
  assert.equal(out[1].aplicacao.como, 'reescrito')            // deduzido por artigo
  assert.equal(out[2].aplicacao.como, 'redacao')
  const resumo = resumoParticipacao(membros, out)
  assert.equal(resumo.daEquipe, 0)
  assert.equal(resumo.aplicadas, 3)
  assert.deepEqual(resumo.aplicacoes, { incluido: 1, reescrito: 1, redacao: 1 })
})

test('resumoParticipacao conta pessoas, não contas: duas contas com o mesmo nome são um militar', () => {
  const idx = indexarRecorte(recorteFake())
  const membros = [
    { uid: 'a1', nome: 'LUIZ EDUARDO OLIVEIRA FIRMINO', escopo: 'servico' },
    { uid: 'a2', nome: 'Luiz Eduardo Oliveira  Firmino', escopo: 'servico' },
    { uid: 'b1', nome: 'Outro Militar', escopo: 'servico' },
  ]
  const sugestoes = [
    { id: 'x', dispositivoId: 'reg:atual:servico-operacional/se-art-24#caput', texto: 'a', autorUid: 'a1', criadoEm: '2026-08-19T12:00:00Z' },
    { id: 'y', dispositivoId: 'reg:atual:servico-operacional/se-art-24#0', texto: 'b', autorUid: 'a2', criadoEm: '2026-08-25T12:00:00Z' },
  ]
  const out = selecionarInteracoes({ sugestoes, membros, indice: idx, finals: new Map() })
  const resumo = resumoParticipacao(membros, out)
  assert.equal(resumo.cadastradosEscopo, 2)
  assert.equal(resumo.contasEscopo, 3)
  assert.equal(resumo.contribuintes, 1)
  assert.equal(resumo.porAutor.length, 1)
  assert.equal(resumo.porAutor[0].qtd, 2)
})

test('paraData aceita Timestamp do Firestore, ISO e nulo', () => {
  assert.equal(paraData(null), null)
  assert.equal(paraData({ toDate: () => new Date('2026-01-01') }).getUTCFullYear(), 2026)
  assert.equal(paraData('2026-09-11T10:00:00Z').getUTCHours(), 10)
  assert.equal(paraData('lixo'), null)
})

test('ESTRUTURA cobre 100% do recorte real, sem repetição, e mantém os 171 artigos', () => {
  // A ESTRUTURA mapeia os ids da versão EM CONSULTA (a atual tem ids novos '-r'/'-c').
  const p = path.resolve('database/atual/regulamento_structure_consulta.json')
  if (!fs.existsSync(p)) return
  const completa = JSON.parse(fs.readFileSync(p, 'utf8'))
  const recorte = filtrarEstruturaPorEscopo(completa, 'servico')
  const r = montarReestruturada(recorte)
  const totalRecorte = recorte.chapters.reduce((n, c) => n + c.articles.length, 0)
  assert.equal(r.totalArtigos, totalRecorte)
  assert.equal(r.depara.length, totalRecorte)
  assert.equal(r.blocos.filter(b => b.tipo === 'parte').length, ESTRUTURA.length)
  assert.ok(r.notas.every(n => n.artigo !== '—'), 'toda nota aponta para um artigo da proposta')
  // capítulo cujo único artigo é um incluído da atual não aparece na consulta
  assert.ok(!r.blocos.some(b => b.tipo === 'capitulo' && /POLÍTICA DO SERVIÇO TÉCNICO/.test(b.texto)))
})

test('ESTRUTURA cobre a versão ATUAL: substitutos no lugar do antigo, incluídos após a âncora, suprimidos fora', () => {
  const p = path.resolve('database/atual/regulamento_structure.json')
  if (!fs.existsSync(p)) return
  const recorte = filtrarEstruturaPorEscopo(JSON.parse(fs.readFileSync(p, 'utf8')), 'servico')
  const r = montarReestruturada(recorte)
  const total = recorte.chapters.reduce((n, c) => n + c.articles.length, 0)
  assert.equal(r.totalArtigos, total)
  const ids = r.blocos.filter(b => b.tipo === 'artigo').map(b => b.leaf.id)
  assert.ok(ids.includes('mt-art-3-r1') && !ids.includes('mt-art-3'))
  assert.ok(ids.includes('se-art-31-c1') && !ids.includes('se-art-31'), 'âncora suprimida nas duas versões (16/09) não impede o incluído')
  assert.equal(ids.indexOf('se-art-31-c2'), ids.indexOf('se-art-31-c1') + 1, 'incluídos na ordem da âncora')
  assert.ok(ids.includes('se-art-38-c1') && !ids.includes('se-art-38'), 'âncora suprimida não impede o incluído')
  assert.ok(!ids.includes('se-art-43-c1') && !ids.includes('se-art-43') && !ids.includes('se-art-43-c2'), 'competências operacionais do Oficial de Dia suprimidas em 16/09')
  assert.ok(!r.blocos.some(b => b.tipo === 'capitulo' && /DEMAIS FUNÇÕES DE SERVIÇO/.test(b.texto)))
  assert.ok(r.blocos.some(b => b.tipo === 'capitulo' && b.texto === 'DA PASSAGEM DE SERVIÇO'))
  assert.equal(ids[ids.indexOf('ro-art-2-c1') - 1], 'ro-art-2')
  assert.ok(!ids.includes('se-art-46'))
  // capítulo da RTO (se-art-95..99) foi todo suprimido: some da minuta e a numeração dos capítulos não pula
  assert.ok(!r.blocos.some(b => b.tipo === 'capitulo' && /RESERVA TÉCNICA/.test(b.texto)))
  const caps = r.blocos.filter(b => b.tipo === 'capitulo').map(b => b.rotulo)
  assert.equal(new Set(caps.slice(0, 5)).size, 5, 'Parte I: 5 capítulos numerados sem repetição')
  // 15/09: política do serviço operacional abre o Título I; política do serviço técnico (artigo novo,
  // posicionado pelo próprio id) abre o Título II, antes do ro-art-13 do SSCIP
  const textos = r.blocos.map(b => b.tipo === 'artigo' ? b.leaf.id : b.texto ?? b.rotulo)
  assert.equal(textos[textos.indexOf('TÍTULO I — DO SERVIÇO OPERACIONAL') + 1], 'DA POLÍTICA DO SERVIÇO OPERACIONAL')
  assert.equal(textos[textos.indexOf('DA POLÍTICA DO SERVIÇO OPERACIONAL') + 1], 'se-art-3-r1')
  assert.equal(textos[textos.indexOf('TÍTULO II — DO SERVIÇO TÉCNICO') + 1], 'DA POLÍTICA DO SERVIÇO TÉCNICO')
  assert.equal(textos[textos.indexOf('DA POLÍTICA DO SERVIÇO TÉCNICO') + 1], 'ro-art-13-c1')
  assert.equal(ids.filter(i => i === 'ro-art-13-c1').length, 1, 'incluído explícito não repete após a âncora')
})

test('montarReestruturada falha alto se sobrar artigo', () => {
  const recorte = recorteFake()
  assert.throws(() => montarReestruturada(recorte), /Folha não encontrada|sem posição/)
})
