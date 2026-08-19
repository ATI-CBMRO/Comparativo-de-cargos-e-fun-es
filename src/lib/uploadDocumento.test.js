import test from 'node:test'
import assert from 'node:assert/strict'
import {
  TIPOS_DOCUMENTO, LIMITE_TAMANHO_BYTES, LIMITES_UPLOAD,
  validarEnvio, nomeArquivoSeguro, caminhoUpload,
} from './uploadDocumento.js'

// Dublê de File: o validador só olha name/size/type, então um objeto simples basta —
// `node --test` não tem a File API do navegador.
const pdf = (over = {}) => ({ name: 'lob.pdf', size: 1024, type: 'application/pdf', ...over })

// --- constantes ------------------------------------------------------------

test('TIPOS_DOCUMENTO traz os 4 rótulos exatos que o visitante já vê no Acervo', () => {
  assert.deepEqual(TIPOS_DOCUMENTO, [
    'Lei de Organização Básica', 'Regimento Interno', 'Regulamento de Serviço', 'Outro',
  ])
})

test('LIMITE_TAMANHO_BYTES é 20 MB', () => {
  assert.equal(LIMITE_TAMANHO_BYTES, 20 * 1024 * 1024)
})

// --- validação -------------------------------------------------------------

test('validarEnvio apara espaços de estado e observação', () => {
  const r = validarEnvio({
    estado: '  CBMPA  ', tipoDocumento: 'Regimento Interno',
    observacao: '  veio do site oficial  ', arquivo: pdf(),
  })
  assert.equal(r.ok, true)
  assert.deepEqual(r.dados, {
    estado: 'CBMPA', tipoDocumento: 'Regimento Interno', observacao: 'veio do site oficial',
  })
})

test('validarEnvio aceita observação vazia (campo opcional)', () => {
  const r = validarEnvio({ estado: 'CBMPA', tipoDocumento: 'Outro', arquivo: pdf() })
  assert.equal(r.ok, true)
  assert.equal(r.dados.observacao, '')
})

test('validarEnvio exige estado', () => {
  const r = validarEnvio({ estado: '   ', tipoDocumento: 'Outro', arquivo: pdf() })
  assert.equal(r.ok, false)
  assert.match(r.erro, /estado/i)
})

test('validarEnvio exige um tipo da lista — nada inventado', () => {
  assert.equal(validarEnvio({ estado: 'CBMPA', tipoDocumento: '', arquivo: pdf() }).ok, false)
  const r = validarEnvio({ estado: 'CBMPA', tipoDocumento: 'Portaria qualquer', arquivo: pdf() })
  assert.equal(r.ok, false)
  assert.match(r.erro, /tipo/i)
})

test('validarEnvio exige arquivo', () => {
  const r = validarEnvio({ estado: 'CBMPA', tipoDocumento: 'Outro', arquivo: null })
  assert.equal(r.ok, false)
  assert.match(r.erro, /arquivo|PDF/i)
})

test('validarEnvio recusa arquivo que não é PDF', () => {
  const r = validarEnvio({
    estado: 'CBMPA', tipoDocumento: 'Outro',
    arquivo: pdf({ name: 'foto.jpg', type: 'image/jpeg' }),
  })
  assert.equal(r.ok, false)
  assert.match(r.erro, /PDF/i)
})

test('validarEnvio recusa arquivo acima de 20 MB e aceita exatamente no limite', () => {
  const acima = validarEnvio({
    estado: 'CBMPA', tipoDocumento: 'Outro', arquivo: pdf({ size: LIMITE_TAMANHO_BYTES + 1 }),
  })
  assert.equal(acima.ok, false)
  assert.match(acima.erro, /20 MB/)

  // O limite é <= nos DOIS lados (cliente e regra do Storage): exatamente 20 MB passa.
  const noLimite = validarEnvio({
    estado: 'CBMPA', tipoDocumento: 'Outro', arquivo: pdf({ size: LIMITE_TAMANHO_BYTES }),
  })
  assert.equal(noLimite.ok, true)
})

test('validarEnvio recusa estado e observação acima do limite da regra do Firestore', () => {
  const estadoGigante = 'x'.repeat(LIMITES_UPLOAD.estado + 1)
  assert.equal(validarEnvio({ estado: estadoGigante, tipoDocumento: 'Outro', arquivo: pdf() }).ok, false)

  const obsGigante = 'y'.repeat(LIMITES_UPLOAD.observacao + 1)
  assert.equal(
    validarEnvio({ estado: 'CBMPA', tipoDocumento: 'Outro', observacao: obsGigante, arquivo: pdf() }).ok,
    false,
  )
})

// --- nome de arquivo e caminho --------------------------------------------

// SEGURANÇA: uma barra no nome do arquivo criaria uma subpasta e poderia escapar da pasta
// do próprio uid, que é exatamente o que a regra do Storage usa para autorizar a escrita.
test('nomeArquivoSeguro remove barras, "..", e caracteres de caminho', () => {
  assert.equal(nomeArquivoSeguro('../../etc/senha.pdf'), 'etc-senha.pdf')
  assert.equal(nomeArquivoSeguro('pasta/sub/lei.pdf'), 'pasta-sub-lei.pdf')
  assert.equal(nomeArquivoSeguro('lei\\windows.pdf'), 'lei-windows.pdf')
})

test('nomeArquivoSeguro troca espaços e acentos por equivalentes simples', () => {
  assert.equal(nomeArquivoSeguro('Lei de Organização Básica.pdf'), 'Lei-de-Organizacao-Basica.pdf')
})

test('nomeArquivoSeguro trunca nome muito longo preservando a extensão .pdf', () => {
  const longo = `${'a'.repeat(400)}.pdf`
  const saida = nomeArquivoSeguro(longo)
  assert.ok(saida.length <= LIMITES_UPLOAD.nomeArquivo)
  assert.ok(saida.endsWith('.pdf'))
})

test('nomeArquivoSeguro nunca devolve string vazia', () => {
  assert.ok(nomeArquivoSeguro('').length > 0)
  assert.ok(nomeArquivoSeguro('///').length > 0)
})

test('caminhoUpload põe o arquivo dentro da pasta do próprio uid, com carimbo de tempo', () => {
  const caminho = caminhoUpload('uid123', 'lei.pdf', 1700000000000)
  assert.equal(caminho, 'uploads-visitantes/uid123/1700000000000-lei.pdf')
})

test('caminhoUpload sanitiza o nome antes de montar o caminho', () => {
  const caminho = caminhoUpload('uid123', '../fuga.pdf', 1700000000000)
  assert.equal(caminho, 'uploads-visitantes/uid123/1700000000000-fuga.pdf')
  // Nenhum ".." sobrevive: o arquivo não escapa da pasta do uid.
  assert.ok(!caminho.includes('..'))
})
