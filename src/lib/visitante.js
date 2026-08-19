// Lógica pura do visitante público (spec 2026-08-18): validação do cadastro básico,
// resolução das rotas do acervo e persistência local. Sem React e sem Firebase de
// propósito — é o núcleo que dá para testar com `node --test`.
import { normalizeEmail } from './membersStats.js'

export const BASE_PUBLICA = '/acervo-publico'
export const CHAVE_LOCAL = 'cbmro_visitante'

// Espelham os tamanhos da regra do Firestore (firestore.rules, match /visitantes/{uid}).
// Se um deles mudar lá, mude aqui: passar do limite faz o banco RECUSAR a gravação, e o
// visitante veria um erro genérico depois de preencher o formulário inteiro.
export const LIMITES = { nome: 200, email: 200, instituicao: 200 }

export function normalizarVisitante({ nome, email, instituicao } = {}) {
  const n = (nome ?? '').trim()
  const e = normalizeEmail(email)
  const i = (instituicao ?? '').trim()

  if (!n || !e || !i) {
    return { ok: false, erro: 'Preencha nome completo, e-mail e instituição.' }
  }
  // Validação deliberadamente frouxa: não confirmamos o e-mail (spec, seção 7), então
  // exigir formato rígido só barraria endereço institucional incomum sem nada em troca.
  if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(e)) {
    return { ok: false, erro: 'Digite um e-mail válido.' }
  }
  if (n.length > LIMITES.nome) return { ok: false, erro: `O nome deve ter até ${LIMITES.nome} caracteres.` }
  if (e.length > LIMITES.email) return { ok: false, erro: `O e-mail deve ter até ${LIMITES.email} caracteres.` }
  if (i.length > LIMITES.instituicao) return { ok: false, erro: `A instituição deve ter até ${LIMITES.instituicao} caracteres.` }

  return { ok: true, dados: { nome: n, email: e, instituicao: i } }
}

// `base` vazia = membro logado (rotas de sempre); BASE_PUBLICA = visitante.
export function rotaEstado(base, id) {
  return `${base ?? ''}/estados/${id}`
}

// ATENÇÃO: não é prefixo cego. A lista de estados (/estados, StatesList) NÃO faz parte do
// recorte público — prefixar daria '/acervo-publico/estados', rota que não existe. O
// visitante volta para a tabela do acervo, que é de onde ele veio.
export function rotaListaEstados(base) {
  return base ? base : '/estados'
}

export function lerVisitanteLocal(storage) {
  try {
    const cru = storage?.getItem(CHAVE_LOCAL)
    if (!cru) return null
    const v = JSON.parse(cru)
    if (!v || typeof v.uid !== 'string' || typeof v.nome !== 'string') return null
    return { uid: v.uid, nome: v.nome }
  } catch {
    return null   // conteúdo corrompido ou ambiente sem localStorage: trate como "não há visitante"
  }
}

export function gravarVisitanteLocal(storage, { uid, nome }) {
  try { storage?.setItem(CHAVE_LOCAL, JSON.stringify({ uid, nome })) } catch { /* ambiente sem localStorage */ }
}

export function limparVisitanteLocal(storage) {
  try { storage?.removeItem(CHAVE_LOCAL) } catch { /* ambiente sem localStorage */ }
}
