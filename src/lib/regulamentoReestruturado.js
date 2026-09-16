// Estrutura da Minuta do Regulamento de Serviço em PARTE GERAL (comum ao serviço operacional
// e ao serviço técnico) + PARTE ESPECIAL (Título I — Serviço Operacional; Título II — Serviço
// Técnico) + Disposições Finais (estrutura adotada em 2026-09-11).
// Fonte ÚNICA da estrutura: usada pela tela do admin (download .docx) e pelo script
// scripts/gerar_docx_regulamento_reestruturado.mjs. Cada folha é "tema/id" da VERSÃO EM
// CONSULTA do regulamento_structure (cenário atual). NÃO reescreve artigo: só reordena.
// Funciona com as DUAS versões: na atual, o artigo com `substitui` entra no lugar do id
// antigo, o `incluido` (`<ancora>-cN`) entra logo após a âncora — salvo quando a ESTRUTURA o
// cita pelo próprio id (`tema/<ancora>-cN`), caso em que entra ali (e o capítulo some na versão
// em consulta, onde ele não existe) —, e os `suprimidos` do capítulo não aparecem (2026-09-15).
import { articular, aplicarFinais } from './consultaRelatorios.js'
import { articleLabel, romanize } from './minutaArticles.js'

const T = {
  pre: 'disposicoes-preliminares', fun: 'atribuicoes-funcoes', op: 'servico-operacional',
  ciop: 'central-operacoes-193', dia: 'servico-interno-dia', sci: 'seguranca-contra-incendio',
  fim: 'disposicoes-finais',
}
const se = (tema, ...ns) => ns.map(n => `${tema}/se-art-${n}`)
const ro = (tema, ...ns) => ns.map(n => `${tema}/ro-art-${n}`)
const mt = (tema, ...ns) => ns.map(n => `${tema}/mt-art-${n}`)
const faixa = (a, b) => Array.from({ length: b - a + 1 }, (_, i) => a + i)

export const ESTRUTURA = [
  {
    parte: 'PARTE I — DISPOSIÇÕES GERAIS',
    subtitulo: 'Normas comuns ao serviço operacional e ao serviço técnico',
    titulos: [
      {
        capitulos: [
          { titulo: 'DA FINALIDADE, DA ABRANGÊNCIA E DA COMPETÊNCIA', itens: [...mt(T.pre, 1, 2, 3), ...se(T.op, 1)] },
          { titulo: 'DOS OBJETIVOS DO REGULAMENTO', itens: se(T.op, 2) },
          { titulo: 'DO REGIME DE TRABALHO, DAS ESCALAS, DAS PERMUTAS E DAS DISPENSAS', itens: [...se(T.op, 23), ...se(T.dia, 109, 111), ...se(T.op, 112, 50, 51, 52), ...se(T.dia, 110)] },
          { titulo: 'DAS VIATURAS', itens: [...se(T.op, ...faixa(117, 128)), ...se(T.dia, 105, 106, 107, 108)] },
          { titulo: 'DO MATERIAL, DO EMPRÉSTIMO E DA RESPONSABILIDADE POR DANOS', itens: se(T.dia, 100, 101, 102, 103, 104, 92, 93, 94) },
          { titulo: 'DA COMUNICAÇÃO SOCIAL E DAS RELAÇÕES COM A IMPRENSA', itens: ro(T.op, 1) },
        ],
      },
    ],
  },
  {
    parte: 'PARTE II — DISPOSIÇÕES ESPECIAIS',
    subtitulo: 'Capítulos específicos do Serviço Operacional e do Serviço Técnico',
    titulos: [
      {
        titulo: 'TÍTULO I — DO SERVIÇO OPERACIONAL',
        capitulos: [
          { titulo: 'DA POLÍTICA DO SERVIÇO OPERACIONAL', itens: se(T.op, 3) },
          { titulo: 'DAS FUNÇÕES DO COMANDO OPERACIONAL DE BOMBEIROS', itens: ro(T.fun, ...faixa(1, 10)) },
          { titulo: 'DAS FUNÇÕES DO SERVIÇO OPERACIONAL DIÁRIO', itens: se(T.op, 4) },
          { titulo: 'DO SUPERIOR DE DIA', itens: se(T.op, ...faixa(24, 31)) },
          { titulo: 'DO OFICIAL DE DIA E DO COMANDANTE DE GUARNIÇÃO', itens: se(T.op, ...faixa(32, 43)) },
          { titulo: 'DAS DEMAIS FUNÇÕES DE SERVIÇO NAS UNIDADES', itens: se(T.op, ...faixa(44, 47)) },
          { titulo: 'DA PASSAGEM DE SERVIÇO', itens: se(T.dia, ...faixa(54, 61)) },   // se-art-54 (quadro) suprimido em 16/09
          { titulo: 'DA CONFERÊNCIA E DO EMPREGO DO MATERIAL OPERACIONAL', itens: se(T.dia, ...faixa(62, 68)) },
          { titulo: 'DA PREPARAÇÃO DA PRONTIDÃO E DOS ALOJAMENTOS', itens: se(T.dia, ...faixa(69, 81)) },   // instrução (se-art-71..77) suprimida em 16/09
          { titulo: 'DO ACIONAMENTO, DO DESLOCAMENTO E DO REGRESSO DO SOCORRO', itens: se(T.dia, ...faixa(82, 91)) },
          { titulo: 'DA RESERVA TÉCNICA OPERACIONAL', itens: se(T.dia, ...faixa(95, 99)) },
          { titulo: 'DO ATENDIMENTO E DO COMANDO DAS OCORRÊNCIAS', itens: se(T.op, ...faixa(129, 133)) },
          { titulo: 'DO BOMBEIRO MILITAR DE FOLGA EM OCORRÊNCIA', itens: se(T.op, 114, 115) },
          { titulo: 'DAS OCORRÊNCIAS DE GRANDE PORTE E DO APOIO EXTERNO', itens: se(T.op, ...faixa(134, 147)) },
          { titulo: 'DOS PROTOCOLOS ESPECIAIS DE ATENDIMENTO', itens: [...se(T.op, 116), ...ro(T.op, 2)] },
          { titulo: 'DO CENTRO INTEGRADO DE OPERAÇÕES E DO TELEDESPACHO', itens: ro(T.ciop, 1, 2, 3, 4) },
        ],
      },
      {
        titulo: 'TÍTULO II — DO SERVIÇO TÉCNICO',
        capitulos: [
          // artigo novo da versão atual, posicionado explicitamente (só existe na atual; na consulta o capítulo some)
          { titulo: 'DA POLÍTICA DO SERVIÇO TÉCNICO', itens: [`${T.sci}/ro-art-13-c1`] },
          { titulo: 'DO SISTEMA DE SEGURANÇA CONTRA INCÊNDIO E PÂNICO', itens: ro(T.sci, 13) },
          { titulo: 'DA COORDENADORIA DE ATIVIDADES TÉCNICAS', itens: ro(T.sci, 1, 2, 3, 4, 5) },
          { titulo: 'DAS DIRETORIAS E DAS SEÇÕES DE ATIVIDADES TÉCNICAS', itens: ro(T.sci, ...faixa(6, 12)) },
          { titulo: 'DAS FUNÇÕES DO SERVIÇO TÉCNICO', itens: ro(T.fun, ...faixa(11, 19)) },
          { titulo: 'DAS PENALIDADES, DAS COMISSÕES E DO DIREITO DE DEFESA', itens: ro(T.sci, 14, 15) },
        ],
      },
    ],
  },
  {
    parte: 'PARTE III — DISPOSIÇÕES FINAIS',
    titulos: [{ capitulos: [{ titulo: 'DAS DISPOSIÇÕES FINAIS', itens: mt(T.fim, 264, 265, 266) }] }],
  },
]

// Ajustes de redação que a reestruturação passa a exigir (não aplicados — pauta do CONDEG).
export const NOTAS = [
  ['servico-operacional/se-art-1', 'O caput fala em "serviço operacional diário"; na Parte Geral passa a abranger também o serviço técnico. Sugestão: "dispor sobre o serviço operacional e o serviço técnico no âmbito do CBMRO".'],
  ['servico-operacional/se-art-2', 'Inciso I cita "Funções integrantes do Serviço Operacional"; na Parte Geral, ampliar para "do Serviço Operacional e do Serviço Técnico".'],
  ['servico-operacional/se-art-3', '"Política do serviço operacional" — avaliar se os objetivos IV a VIII (socorros, viaturas, reserva operacional) valem também para o serviço técnico ou se o artigo deve descer ao Título I da Parte Especial.'],
  ['servico-operacional/se-art-23', 'Caput já abrange "serviço administrativo e operacional"; os incisos tratam só de escalas operacionais. Manter na Parte Geral e acrescentar inciso para o expediente do serviço técnico, ou remeter à NGA da CAT.'],
  ['servico-operacional/se-art-115', 'Caput traz resíduo "com Distúrbios Mentais" no fim: cortar.'],
  ['servico-operacional/se-art-135', 'Inciso XIII traz resíduo "Grande Porte" no fim: cortar.'],
  ['servico-interno-dia/se-art-107', 'Caput traz resíduo "Operacional" no fim: cortar.'],
  ['servico-interno-dia/se-art-85', 'Nomenclatura: "Central Integrada de Operações" → "Centro Integrado de Operações – CIOP" (nome da NGA-CIOP-001/2026), em todo o texto.'],
  ['disposicoes-finais/mt-art-264', 'Fala em "Batalhões Bombeiro Militar" (CBMMT); na LOB de RO as unidades são Grupamentos (GBM). Ajustar.'],
  ['disposicoes-finais/mt-art-266', 'Caput traz rodapé de publicação de MT ("Este texto não substitui o publicado no Boletim Geral Eletrônico – BGE"): cortar.'],
  ['disposicoes-preliminares/mt-art-1', '"Art. 82 da Constituição Estadual" é a referência de Mato Grosso; conferir o artigo correspondente na Constituição de Rondônia (art. 148, já corrigido na versão atual).'],
]

// Monta a lista linear de blocos para renderização (tela ou .docx) a partir do RECORTE em
// consulta (filtrarEstruturaPorEscopo(structure,'servico')). Lança erro se algum artigo do
// recorte ficou sem posição ou foi usado duas vezes — a estrutura tem de cobrir 100%.
// Retorna { blocos, depara, notas, totalArtigos, aplicados }.
export function montarReestruturada(recorte, finals = null) {
  const folhas = new Map()        // chave da consulta → [{leaf}] (o próprio ou seus substitutos)
  const incluidos = new Map()     // chave da âncora → [{leaf}] (artigos novos, após a âncora)
  const incluidosPorId = new Map() // chave do próprio incluído → {leaf} (posição explícita na ESTRUTURA)
  const suprimidos = new Set()
  const numeroAntigo = new Map()
  let n = 0
  for (const cap of recorte.chapters) {
    const tema = cap.id.split(':').pop()
    for (const s of cap.suprimidos ?? []) suprimidos.add(`${tema}/${s.id}`)
    for (const leaf of cap.articles) {
      n += 1
      const entrada = { leaf, tema, capituloAntigo: cap.chapterTitle }
      if (leaf.substitui) {
        const chave = `${tema}/${leaf.substitui}`
        if (!folhas.has(chave)) folhas.set(chave, [])
        folhas.get(chave).push(entrada)
      } else if (leaf.incluido) {
        const chave = `${tema}/${leaf.id.replace(/-c\d+$/, '')}`
        if (!incluidos.has(chave)) incluidos.set(chave, [])
        incluidos.get(chave).push(entrada)
        incluidosPorId.set(`${tema}/${leaf.id}`, entrada)
      } else {
        folhas.set(`${tema}/${leaf.id}`, [entrada])
      }
      numeroAntigo.set(`${tema}/${leaf.id}`, n)
    }
  }
  const usados = new Set()
  const explicitos = new Set(ESTRUTURA.flatMap(p => p.titulos.flatMap(t => t.capitulos.flatMap(c => c.itens))).filter(k => /-c\d+$/.test(k)))
  const aposAncora = chave => (incluidos.get(chave) ?? []).filter(f => !explicitos.has(`${f.tema}/${f.leaf.id}`))
  const blocos = []
  const depara = []
  const novoPorChave = new Map()
  let numero = 0
  let aplicados = 0
  const emitir = (f, chave, posicao) => {
    let art = articular(f.leaf)
    art = aplicarFinais(art, finals)
    if (art.temFinal) aplicados += 1
    numero += 1
    blocos.push({ tipo: 'artigo', numero, art, leaf: f.leaf })
    if (!novoPorChave.has(chave)) novoPorChave.set(chave, numero)
    const antigo = numeroAntigo.get(`${f.tema}/${f.leaf.id}`)
    depara.push({ novo: articleLabel(numero), antigo: antigo ? articleLabel(antigo) : '—', origem: `${f.capituloAntigo} / ${f.leaf.id}`, posicao })
  }
  ESTRUTURA.forEach((parte, pi) => {
    blocos.push({ tipo: 'parte', texto: parte.parte, subtitulo: parte.subtitulo ?? null, quebraAntes: pi > 0 })
    for (const tit of parte.titulos) {
      if (tit.titulo) blocos.push({ tipo: 'titulo', texto: tit.titulo })
      let numCap = 0
      for (const cap of tit.capitulos) {
        // capítulo cujos artigos foram todos suprimidos na versão atual não aparece (nem conta)
        const temArtigo = cap.itens.some(chave => folhas.has(chave) || incluidosPorId.has(chave) || aposAncora(chave).length)
        if (!temArtigo) { cap.itens.forEach(chave => usados.add(chave)); continue }
        numCap += 1
        const rotuloCap = `CAPÍTULO ${romanize(numCap)}`
        blocos.push({ tipo: 'capitulo', rotulo: rotuloCap, texto: cap.titulo })
        const posicao = [parte.parte.split(' — ')[0], tit.titulo?.split(' — ')[0], `${rotuloCap} — ${cap.titulo}`].filter(Boolean).join(' · ')
        for (const chave of cap.itens) {
          if (usados.has(chave)) throw new Error(`Folha usada duas vezes: ${chave}`)
          usados.add(chave)
          if (explicitos.has(chave)) {   // incluído citado pelo próprio id: só existe na versão atual
            const f = incluidosPorId.get(chave)
            if (f) emitir(f, chave, posicao)
            continue
          }
          const fs = folhas.get(chave)
          if (!fs && !suprimidos.has(chave) && !incluidos.has(chave)) throw new Error(`Folha não encontrada no recorte: ${chave}`)
          for (const f of fs ?? []) emitir(f, chave, posicao)
          for (const f of aposAncora(chave)) emitir(f, chave, posicao)
        }
      }
    }
  })
  const sobras = [...folhas.keys(), ...incluidos.keys()].filter(k => !usados.has(k))
  if (sobras.length) throw new Error(`Artigos do recorte sem posição na nova estrutura: ${sobras.join(', ')}`)
  const notas = NOTAS.map(([chave, nota]) => ({ artigo: novoPorChave.has(chave) ? articleLabel(novoPorChave.get(chave)) : '—', chave, nota }))
  return { blocos, depara, notas, totalArtigos: numero, aplicados }
}
