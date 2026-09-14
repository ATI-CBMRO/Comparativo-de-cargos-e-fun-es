// Comparativo entre a versão EM CONSULTA (lida pelos militares, + correções) e a versão
// ATUAL (após as sugestões) do Regulamento de Serviço — lógica pura, usada pela tela
// /regulamento/servico/comparativo e pelo .docx. Casamento por id: artigo da atual com
// `substitui` casa com o id antigo; `incluido` é novo; id da consulta ausente na atual é
// suprimido; mesmo id nas duas → compara o texto (texto final do admin) ou é igual.
import { articular } from './consultaRelatorios.js'
import { articleLabel } from './minutaArticles.js'

export const ROTULO_TIPO = {
  igual: 'Sem alteração',
  corrigido: 'Corrigido nas duas versões',
  alterado: 'Texto alterado na versão atual',
  reescrito: 'Reescrito na versão atual',
  incluido: 'Incluído na versão atual',
  suprimido: 'Suprimido na versão atual',
}

function textoDe(art) {
  const a = articular(art)
  return [a.caput, ...a.incisos.map(i => i.text)].join('\n')
}

// Devolve [{ capitulo, entradas: [{ tipo, antes, depois, numAntes, numDepois, nota, proposta, motivo }] }]
// com numeração contínua de cada versão (a que cada tela mostra).
export function compararVersoes(recorteConsulta, recorteAtual) {
  const numA = new Map()
  let n = 0
  for (const c of recorteAtual.chapters) for (const a of c.articles) { n += 1; numA.set(a.id, n) }
  const numC = new Map()
  n = 0
  for (const c of recorteConsulta.chapters) for (const a of c.articles) { n += 1; numC.set(a.id, n) }

  const atualPorTema = new Map(recorteAtual.chapters.map(c => [c.id, c]))
  const saida = []
  for (const capC of recorteConsulta.chapters) {
    const capA = atualPorTema.get(capC.id)
    const artsA = capA?.articles ?? []
    const suprimidos = new Map((capA?.suprimidos ?? []).map(s => [s.id, s.motivo]))
    const substitutos = new Map()
    for (const a of artsA) if (a.substitui) (substitutos.get(a.substitui) ?? substitutos.set(a.substitui, []).get(a.substitui)).push(a)
    const idsA = new Map(artsA.map(a => [a.id, a]))
    const entradas = []
    // Percorre a ATUAL na ordem dela, para as inclusões caírem no lugar certo; artigos da
    // consulta que sumiram (suprimidos) entram na posição em que estavam.
    const emitidosC = new Set()
    const artsC = capC.articles
    const posC = new Map(artsC.map((a, i) => [a.id, i]))
    function emitirSuprimidosAntesDe(idC) {
      const alvo = idC == null ? artsC.length : posC.get(idC)
      for (let i = 0; i < alvo; i += 1) {
        const c = artsC[i]
        if (emitidosC.has(c.id)) continue
        if (!idsA.has(c.id) && !substitutos.has(c.id)) {
          emitidosC.add(c.id)
          entradas.push({ tipo: 'suprimido', antes: c, depois: null, numAntes: numC.get(c.id), numDepois: null, motivo: suprimidos.get(c.id) ?? 'suprimido' })
        }
      }
    }
    for (const a of artsA) {
      if (a.substitui) {
        emitirSuprimidosAntesDe(a.substitui)
        const c = artsC[posC.get(a.substitui)]
        const primeira = !emitidosC.has(a.substitui)
        emitidosC.add(a.substitui)
        entradas.push({ tipo: 'reescrito', antes: primeira ? c : null, depois: a, numAntes: primeira ? numC.get(c?.id) : null, numDepois: numA.get(a.id), nota: a.nota ?? null, proposta: Boolean(a.proposta) })
      } else if (a.incluido) {
        entradas.push({ tipo: 'incluido', antes: null, depois: a, numAntes: null, numDepois: numA.get(a.id), nota: a.nota ?? null, proposta: Boolean(a.proposta) })
      } else {
        emitirSuprimidosAntesDe(a.id)
        const c = artsC[posC.get(a.id)]
        emitidosC.add(a.id)
        let tipo = 'igual'
        if (c && textoDe(c) !== textoDe(a)) tipo = 'alterado'
        else if (a.corrigido) tipo = 'corrigido'
        entradas.push({ tipo, antes: c ?? null, depois: a, numAntes: c ? numC.get(c.id) : null, numDepois: numA.get(a.id), nota: a.alterado ? `${a.alterado} (${a.fundamento_alteracao ?? ''})` : null })
      }
    }
    emitirSuprimidosAntesDe(null)
    saida.push({ capitulo: capC.chapterTitle, entradas })
  }
  return saida
}

export function resumoComparativo(comparacao) {
  const r = { igual: 0, corrigido: 0, alterado: 0, reescrito: 0, incluido: 0, suprimido: 0, propostas: 0 }
  for (const c of comparacao) for (const e of c.entradas) { r[e.tipo] += 1; if (e.proposta) r.propostas += 1 }
  return r
}

export function rotuloArtigo(num) {
  return num ? articleLabel(num) : '—'
}
