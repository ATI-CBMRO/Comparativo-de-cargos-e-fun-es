// Lógica pura do envio de documentos pelo visitante público (spec 2026-08-18):
// validação do formulário e montagem do caminho no Storage. Sem React e sem Firebase —
// é o núcleo que dá para testar com `node --test`, no mesmo espírito de visitante.js.

// Os mesmos rótulos que o visitante já lê na tabela de cobertura do Acervo Legal. Manter
// o vocabulário igual evita que ele tenha que traduzir o que está vendo para o que o
// formulário pede.
export const TIPOS_DOCUMENTO = [
  'Lei de Organização Básica', 'Regimento Interno', 'Regulamento de Serviço', 'Outro',
]

// 20 MB. A comparação é `<=` aqui E na regra do Storage — se um lado usar `<` e o outro
// `<=`, um arquivo de exatamente 20 MB passa no formulário e é recusado pelo servidor,
// depois do upload inteiro já ter subido.
export const LIMITE_TAMANHO_BYTES = 20 * 1024 * 1024

// Espelham os tamanhos da regra do Firestore (firestore.rules, match /uploadsVisitantes).
// Se um deles mudar lá, mude aqui — senão o banco recusa a gravação depois do upload.
export const LIMITES_UPLOAD = { estado: 120, observacao: 1000, nomeArquivo: 260 }

export function validarEnvio({ estado, tipoDocumento, observacao, arquivo } = {}) {
  const e = (estado ?? '').trim()
  const o = (observacao ?? '').trim()

  if (!e) return { ok: false, erro: 'Informe o estado / CBM de origem do documento.' }
  if (e.length > LIMITES_UPLOAD.estado) {
    return { ok: false, erro: `O estado deve ter até ${LIMITES_UPLOAD.estado} caracteres.` }
  }
  if (!TIPOS_DOCUMENTO.includes(tipoDocumento)) {
    return { ok: false, erro: 'Escolha o tipo de documento.' }
  }
  if (o.length > LIMITES_UPLOAD.observacao) {
    return { ok: false, erro: `A observação deve ter até ${LIMITES_UPLOAD.observacao} caracteres.` }
  }
  if (!arquivo) return { ok: false, erro: 'Anexe o arquivo em PDF.' }
  if (arquivo.type !== 'application/pdf') {
    return { ok: false, erro: 'O arquivo precisa ser um PDF.' }
  }
  if (arquivo.size > LIMITE_TAMANHO_BYTES) {
    return { ok: false, erro: 'O arquivo passa de 20 MB. Envie um PDF menor.' }
  }

  return { ok: true, dados: { estado: e, tipoDocumento, observacao: o } }
}

// SEGURANÇA, não estética: barra no nome viraria subpasta e poderia escapar da pasta do
// próprio uid — que é justamente o que a regra do Storage usa para autorizar a escrita.
// Acentos saem porque nome de objeto no Storage com acento complica a URL de download.
export function nomeArquivoSeguro(nome) {
  const semAcento = (nome ?? '')
    .normalize('NFD')
    .replace(/[\u0300-\u036f]/g, '')   // tira os diacriticos separados pelo NFD
  const limpo = semAcento
    .replace(/[^a-zA-Z0-9._-]+/g, '-')     // tudo que não é seguro vira hífen (inclui / e \)
    .replace(/\.{2,}/g, '.')               // ".." não sobrevive
    .replace(/^[-.]+/, '')                 // não começa com hífen nem ponto
    .replace(/-{2,}/g, '-')
  const base = limpo || 'documento.pdf'
  if (base.length <= LIMITES_UPLOAD.nomeArquivo) return base

  // Trunca preservando a extensão: o admin precisa reconhecer que é PDF pela lista.
  const ext = base.toLowerCase().endsWith('.pdf') ? '.pdf' : ''
  return base.slice(0, LIMITES_UPLOAD.nomeArquivo - ext.length) + ext
}

export function caminhoUpload(uid, nomeArquivo, agoraMs) {
  return `uploads-visitantes/${uid}/${agoraMs}-${nomeArquivoSeguro(nomeArquivo)}`
}
