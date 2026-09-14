// Estrutura da Minuta do Regulamento de Serviço em PARTE GERAL (comum ao serviço operacional
// e ao serviço técnico) + PARTE ESPECIAL (Título I — Serviço Operacional; Título II — Serviço
// Técnico) + Disposições Finais, conforme sugestão do Cel. Luiz Eduardo (2026-09-11).
// Fonte ÚNICA da estrutura: usada pela tela do admin (download .docx) e pelo script
// scripts/gerar_docx_regulamento_reestruturado.mjs. Cada folha é "tema/id" do
// regulamento_structure.json (cenário atual). NÃO reescreve artigo: só reordena.
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
          { titulo: 'DOS OBJETIVOS E DA POLÍTICA DO SERVIÇO', itens: se(T.op, 2, 3) },
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
          { titulo: 'DAS FUNÇÕES DO COMANDO OPERACIONAL DE BOMBEIROS', itens: ro(T.fun, ...faixa(1, 10)) },
          { titulo: 'DAS FUNÇÕES DO SERVIÇO OPERACIONAL DIÁRIO', itens: se(T.op, 4) },
          { titulo: 'DO SUPERIOR DE DIA', itens: se(T.op, ...faixa(24, 31)) },
          { titulo: 'DO OFICIAL DE DIA', itens: se(T.op, ...faixa(32, 38)) },
          { titulo: 'DO COMANDANTE DE SOCORRO E DO OFICIAL DE DIA NAS UNIDADES', itens: se(T.op, ...faixa(39, 43)) },
          { titulo: 'DAS DEMAIS FUNÇÕES DE SERVIÇO NAS UNIDADES', itens: se(T.op, ...faixa(44, 47)) },
          { titulo: 'DO QUADRO DE ATIVIDADES E DA PASSAGEM DE SERVIÇO', itens: se(T.dia, ...faixa(54, 61)) },
          { titulo: 'DA CONFERÊNCIA E DO EMPREGO DO MATERIAL OPERACIONAL', itens: se(T.dia, ...faixa(62, 68)) },
          { titulo: 'DA PREPARAÇÃO DA PRONTIDÃO, DA INSTRUÇÃO E DOS ALOJAMENTOS', itens: se(T.dia, ...faixa(69, 81)) },
          { titulo: 'DO ACIONAMENTO, DO DESLOCAMENTO E DO REGRESSO DO SOCORRO', itens: se(T.dia, ...faixa(82, 91)) },
          { titulo: 'DA RESERVA TÉCNICA OPERACIONAL', itens: se(T.dia, ...faixa(95, 99)) },
          { titulo: 'DO ATENDIMENTO E DO COMANDO DAS OCORRÊNCIAS', itens: se(T.op, ...faixa(129, 133)) },
          { titulo: 'DO BOMBEIRO MILITAR DE FOLGA EM OCORRÊNCIA', itens: se(T.op, 114, 115) },
          { titulo: 'DAS OCORRÊNCIAS DE GRANDE PORTE E DO APOIO EXTERNO', itens: se(T.op, ...faixa(134, 147)) },
          { titulo: 'DOS PROTOCOLOS ESPECIAIS DE ATENDIMENTO', itens: [...se(T.op, 116), ...ro(T.op, 2)] },
          { titulo: 'DA CENTRAL INTEGRADA DE OPERAÇÕES E DO TELEDESPACHO', itens: ro(T.ciop, 1, 2, 3, 4) },
        ],
      },
      {
        titulo: 'TÍTULO II — DO SERVIÇO TÉCNICO',
        capitulos: [
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
  ['servico-operacional/se-art-43', 'Caput traz resíduo de título de seção da fonte ("Comandante de Guarnição – Do Condutor…"): cortar após "Comandante da OBM."'],
  ['servico-operacional/se-art-47', 'Caput traz resíduo "Operações" no fim: cortar. Repete se-art-43 (casos omissos): na nova estrutura, um único artigo de casos omissos do Título I basta.'],
  ['servico-operacional/se-art-112', 'Caput traz resíduo "durante Ocorrências" no fim: cortar. Passa à Parte Geral (permutas), junto de se-art-111.'],
  ['servico-operacional/se-art-115', 'Caput traz resíduo "com Distúrbios Mentais" no fim: cortar.'],
  ['servico-operacional/se-art-135', 'Inciso XIII traz resíduo "Grande Porte" no fim: cortar.'],
  ['servico-operacional/se-art-147', 'Caput traz resíduo "Disposições Gerais" no fim: cortar.'],
  ['servico-interno-dia/se-art-107', 'Caput traz resíduo "Operacional" no fim: cortar.'],
  ['servico-operacional/se-art-36', 'Repete se-art-29 (apresentação ao COB ao sair/retornar da escala). Com Superior de Dia e Oficial de Dia em capítulos próprios, fundir num único artigo da Parte Geral ou manter um em cada capítulo — decidir.'],
  ['servico-operacional/se-art-37', 'Repete se-art-30 (permuta com 48h de antecedência). Mesma decisão de se-art-36.'],
  ['servico-operacional/se-art-38', 'Repete se-art-31 (área de atuação estadual do Superior de Dia) e está no bloco do Oficial de Dia — provável erro de transplante; no capítulo do Oficial de Dia a área é a da OBM (se-art-42/46). Suprimir ou corrigir.'],
  ['servico-operacional/se-art-46', 'Repete se-art-42 (serviço no quartel de cada OBM). Fundir.'],
  ['servico-interno-dia/se-art-85', 'Concordância: "ao Central Integrada de Operações" → "à Central Integrada de Operações". Idem se-art-91.'],
  ['disposicoes-finais/mt-art-264', 'Fala em "Batalhões Bombeiro Militar" (CBMMT); na LOB de RO as unidades são Grupamentos (GBM). Ajustar.'],
  ['disposicoes-finais/mt-art-266', 'Caput traz rodapé de publicação de MT ("Este texto não substitui o publicado no Boletim Geral Eletrônico – BGE"): cortar.'],
  ['disposicoes-preliminares/mt-art-1', '"Art. 82 da Constituição Estadual" é a referência de Mato Grosso; conferir o artigo correspondente na Constituição de Rondônia (sugestão do Wândrio: art. 148).'],
]

// Monta a lista linear de blocos para renderização (tela ou .docx) a partir do RECORTE em
// consulta (filtrarEstruturaPorEscopo(structure,'servico')). Lança erro se algum artigo do
// recorte ficou sem posição ou foi usado duas vezes — a estrutura tem de cobrir 100%.
// Retorna { blocos, depara, notas, totalArtigos, aplicados }.
export function montarReestruturada(recorte, finals = null) {
  const folhas = new Map()
  const numeroAntigo = new Map()
  let n = 0
  for (const cap of recorte.chapters) {
    const tema = cap.id.split(':').pop()
    for (const leaf of cap.articles) {
      n += 1
      const chave = `${tema}/${leaf.id}`
      folhas.set(chave, { leaf, tema, capituloAntigo: cap.chapterTitle })
      numeroAntigo.set(chave, n)
    }
  }
  const usados = new Set()
  const blocos = []
  const depara = []
  const novoPorChave = new Map()
  let numero = 0
  let aplicados = 0
  ESTRUTURA.forEach((parte, pi) => {
    blocos.push({ tipo: 'parte', texto: parte.parte, subtitulo: parte.subtitulo ?? null, quebraAntes: pi > 0 })
    for (const tit of parte.titulos) {
      if (tit.titulo) blocos.push({ tipo: 'titulo', texto: tit.titulo })
      tit.capitulos.forEach((cap, ci) => {
        const rotuloCap = `CAPÍTULO ${romanize(ci + 1)}`
        blocos.push({ tipo: 'capitulo', rotulo: rotuloCap, texto: cap.titulo })
        for (const chave of cap.itens) {
          const f = folhas.get(chave)
          if (!f) throw new Error(`Folha não encontrada no recorte: ${chave}`)
          if (usados.has(chave)) throw new Error(`Folha usada duas vezes: ${chave}`)
          usados.add(chave)
          let art = articular(f.leaf)
          art = aplicarFinais(art, finals)
          if (art.temFinal) aplicados += 1
          numero += 1
          blocos.push({ tipo: 'artigo', numero, art })
          novoPorChave.set(chave, numero)
          const posicao = [parte.parte.split(' — ')[0], tit.titulo?.split(' — ')[0], `${rotuloCap} — ${cap.titulo}`].filter(Boolean).join(' · ')
          depara.push({ novo: articleLabel(numero), antigo: articleLabel(numeroAntigo.get(chave)), origem: `${f.capituloAntigo} / ${f.leaf.id}`, posicao })
        }
      })
    }
  })
  const sobras = [...folhas.keys()].filter(k => !usados.has(k))
  if (sobras.length) throw new Error(`Artigos do recorte sem posição na nova estrutura: ${sobras.join(', ')}`)
  const notas = NOTAS.map(([chave, nota]) => ({ artigo: novoPorChave.has(chave) ? articleLabel(novoPorChave.get(chave)) : '—', chave, nota }))
  return { blocos, depara, notas, totalArtigos: numero, aplicados }
}
