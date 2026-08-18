// Recorte setorizado do Regulamento de Serviço (spec 2026-08-13).
// Fonte ÚNICA da lista de capítulos E da ordem de leitura — nenhuma tela repete isto.

// ATENÇÃO: esta lista é a ORDEM do documento recortado, não só o filtro. NÃO é a ordem
// do arquivo: no regulamento_structure.json a Parte I vem inteira antes da Parte II, de
// modo que "DAS DISPOSIÇÕES FINAIS" (posição 12) precede o serviço operacional (13).
// Preservar a ordem do arquivo jogaria o fecho do regulamento para o meio do documento.
// Ordem escolhida: Preliminares e Finais nas pontas; as ATRIBUIÇÕES DAS FUNÇÕES logo
// após as Preliminares (determinação do Ten. Tiago, 2026-08-18 — quem lê o regulamento de
// serviço precisa saber QUEM faz o quê antes de ler o serviço em si); depois o serviço
// operacional do COB, a Central de Operações, o serviço interno e o serviço técnico da CAT.
// O documento COMPLETO não é reordenado nesta rodada: lá as Preliminares abrem a Parte I e
// este capítulo é Parte II — a posição dele entra na reordenação geral da 2ª etapa.
export const TEMAS_SERVICO = [
  'disposicoes-preliminares',
  'atribuicoes-funcoes',
  'servico-operacional',
  'central-operacoes-193',
  'servico-interno-dia',
  'seguranca-contra-incendio',
  'disposicoes-finais',
]

export const ESCOPOS = { servico: TEMAS_SERVICO }

// Capítulos MISTOS: contêm artigos de vários órgãos e, no recorte, só os do escopo devem
// aparecer. Hoje só o das Atribuições das Funções — nele os artigos de COB/CAT foram
// reescritos sobre a LOB de RO, e os dos demais órgãos seguem sendo o transplante de MT,
// que pertence ao Regulamento Geral completo (decisão do Ten. Tiago, 2026-08-18).
const TEMAS_COM_FILTRO_DE_ORGAO = new Set(['atribuicoes-funcoes'])

// Órgãos que o recorte de serviço cobre: o serviço operacional é do COB, o serviço técnico
// de segurança contra incêndio é da CAT.
export const ORGAOS_NO_ESCOPO = { servico: ['cob', 'cat'] }

// Artigo sem o campo `orgao` NÃO entra no recorte: a ausência de tag significa "órgão que
// esta rodada de curadoria não cobriu". Fail-closed de propósito — deixar passar o que não
// foi classificado é como o transplante de MT vazou para a pauta do participante.
function filtrarArtigosPorOrgao(capitulo, orgaos) {
  if (!Array.isArray(capitulo.articles)) return capitulo
  return { ...capitulo, articles: capitulo.articles.filter(a => orgaos.includes(a?.orgao)) }
}

// O id do capítulo carrega o marcador de cenário ('reg:x' na futura, 'reg:atual:x' no
// atual). Casar pelo id inteiro quebraria em um dos dois cenários.
export function temaDoCapitulo(id) {
  return String(id ?? '').split(':').pop()
}

// Devolve a estrutura com os capítulos do escopo, NA ORDEM de TEMAS_SERVICO, e — nos
// capítulos mistos — só com os artigos dos órgãos do escopo.
// Escopo nulo/desconhecido, ou estrutura sem chapters: devolve o que veio, intacto —
// quem não tem escopo não é afetado por nada disto.
export function filtrarEstruturaPorEscopo(structure, escopo) {
  const temas = ESCOPOS[escopo]
  if (!temas || !Array.isArray(structure?.chapters)) return structure
  const orgaos = ORGAOS_NO_ESCOPO[escopo] ?? []
  const porTema = new Map()
  for (const c of structure.chapters) porTema.set(temaDoCapitulo(c.id), c)
  const chapters = temas
    .map(t => {
      const capitulo = porTema.get(t)
      if (!capitulo) return null
      return TEMAS_COM_FILTRO_DE_ORGAO.has(t)
        ? filtrarArtigosPorOrgao(capitulo, orgaos)
        : capitulo
    })
    .filter(Boolean)
  return { ...structure, chapters }
}

// Rotas que o participante com escopo pode abrir. Lista fechada (allowlist): endereço
// que não estiver aqui é devolvido ao documento dele. Esconder o link do menu não basta —
// quem digita /minuta na barra de endereço chega lá.
// ATENÇÃO: isto é camada de INTERFACE. A tranca de banco é o firestore.rules, que não
// muda nesta entrega (ver spec, seção 3c).
const ROTAS_LIBERADAS = {
  servico: ['/', '/regulamento/servico', '/manual', '/login', '/cadastro'],
}

// Resumo honesto do que ficou de fora, para a nota de escopo: capítulos inteiros que não
// entram no recorte e artigos cortados DENTRO de um capítulo que entrou (capítulo misto).
// Contar os dois juntos, como antes, faria a nota dizer "N artigos ficaram de fora" e
// listar capítulos que não somam N — o leitor não fecharia a conta.
export function resumoForaDoEscopo(completa, recortada, escopo) {
  const temas = ESCOPOS[escopo]
  if (!temas || !Array.isArray(completa?.chapters)) {
    return { capitulosFora: [], artigosEmCapitulosFora: 0, artigosCortadosNoEscopo: 0 }
  }
  const noEscopo = new Set(temas)
  const capitulosFora = []
  let artigosEmCapitulosFora = 0
  for (const c of completa.chapters) {
    if (noEscopo.has(temaDoCapitulo(c.id))) continue
    if (c.chapterTitle) capitulosFora.push(c.chapterTitle)
    artigosEmCapitulosFora += (c.articles?.length ?? 0)
  }
  const contarArtigos = (e) => (e?.chapters ?? []).reduce((n, c) => n + (c.articles?.length ?? 0), 0)
  const totalNoEscopo = completa.chapters
    .filter(c => noEscopo.has(temaDoCapitulo(c.id)))
    .reduce((n, c) => n + (c.articles?.length ?? 0), 0)
  return {
    capitulosFora,
    artigosEmCapitulosFora,
    artigosCortadosNoEscopo: totalNoEscopo - contarArtigos(recortada),
  }
}

export function rotaLiberadaNoEscopo(pathname, escopo) {
  const liberadas = ROTAS_LIBERADAS[escopo]
  if (!liberadas) return true            // sem escopo: portal completo, como sempre
  // Compara o caminho inteiro, nunca por prefixo: "/manualzinho" não pode passar por
  // começar com "/manual". Barra final é ignorada e a comparação é insensível a
  // maiúsculas — a barra de endereço aceita "/Manual" ou "/MINUTA" e o navegador não
  // normaliza isso sozinho antes de chegar aqui.
  const p = String(pathname ?? '').toLowerCase().replace(/\/+$/, '') || '/'
  return liberadas.includes(p)
}
