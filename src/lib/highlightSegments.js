// Função pura: separa um texto em segmentos { text, bold }, sem produzir HTML.
// Substitui a antiga abordagem via dangerouslySetInnerHTML em comparatorRender.jsx.
const TERM_REGEX = new RegExp(
  '\\b(' + [
    'Oficiais', 'Oficial superior', 'Oficiais superiores', 'Oficial da ativa', 'Oficiais da ativa',
    'último posto', 'último Posto', 'Coronéis', 'Coronel', 'Tenente-Coronel', 'Majores', 'Major',
    'Capitão', 'Tenente', 'Praças', 'QOEMBM', 'QCOBM', 'CCEMBM',
    'Governador do Estado', 'Governador', 'Secretário de Estado', 'Comandante-Geral',
    'Subcomandante-Geral', 'Chefe do Estado-Maior', 'Chefe do EMG', 'Estado-Maior Geral',
    'Subcomandante', 'Comandante', 'Diretor-Geral', 'Diretor', 'Diretora', 'Coordenador', 'Coordenadora',
  ].join('|') + ')\\b',
  'gi',
)

export function highlightSegments(text) {
  if (!text) return []
  // split() com um único grupo de captura intercala: índices pares = texto comum,
  // índices ímpares = o próprio termo casado (calculado ANTES de descartar vazios).
  return String(text)
    .split(TERM_REGEX)
    .map((part, i) => ({ text: part, bold: i % 2 === 1 }))
    .filter((seg) => seg.text !== '')
}
