// 2 Partes do Regulamento (spec 2026-07-21). Compartilhado por RegulamentoWizard e
// minutaDocx; estruturas SEM o campo `parte` (ex.: RI) resultam em mapa vazio → no-op.
export const PARTE_HEADERS = {
  geral: 'PARTE I — GERAL',
  servico: 'PARTE II — DO SERVIÇO',
}

export function parteByChapterTitle(structure) {
  const map = {}
  for (const ch of structure?.chapters ?? []) {
    if (ch.parte) map[ch.chapterTitle] = ch.parte
  }
  return map
}
