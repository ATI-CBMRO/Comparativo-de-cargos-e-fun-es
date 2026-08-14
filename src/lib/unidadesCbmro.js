// Dados reais das unidades do CBMRO (63 unidades, 17 cidades), copiados do Sistema ATI
// (prisma/seed.ts do projeto sistema-ati-2026) — não inventar/alterar nomes aqui.
// "comando" = coordenadoria (COB I/II, CAT, CEEI, COA, Comando Geral, e os órgãos
// administrativos de sede única). Sistemas sem conexão entre si: esta lista é uma cópia,
// não uma sincronização ao vivo.

export const UNIDADES_CBMRO = [
  // COB I — Coordenadoria Operacional de Bombeiros I
  { unidade: '1º GBM', cidade: 'Porto Velho', comando: 'COB I' },
  { unidade: '1º GBM / 1º SGBM', cidade: 'Porto Velho', comando: 'COB I' },
  { unidade: '1º GBM / 2º SGBM', cidade: 'Guajará-Mirim', comando: 'COB I' },
  { unidade: '1º GBM / 3º SGBM', cidade: 'Candeias do Jamari', comando: 'COB I' },
  { unidade: '2º GBM', cidade: 'Ji-Paraná', comando: 'COB I' },
  { unidade: '2º GBM / 1º SGBM', cidade: 'Ji-Paraná', comando: 'COB I' },
  { unidade: '2º GBM / 2º SGBM', cidade: 'Ouro Preto do Oeste', comando: 'COB I' },
  { unidade: '2º GBM / 3º SGBM', cidade: 'Jaru', comando: 'COB I' },
  { unidade: '5º GBM', cidade: 'Ariquemes', comando: 'COB I' },
  { unidade: '5º GBM / 1º SGBM', cidade: 'Ariquemes', comando: 'COB I' },
  { unidade: '5º GBM / 2º SGBM', cidade: "Machadinho D'Oeste", comando: 'COB I' },
  { unidade: '5º GBM / 3º SGBM', cidade: 'Buritis', comando: 'COB I' },
  { unidade: 'GBS', cidade: 'Porto Velho', comando: 'COB I' },

  // COB II — Coordenadoria Operacional de Bombeiros II
  { unidade: '3º GBM', cidade: 'Vilhena', comando: 'COB II' },
  { unidade: '3º GBM / 1º SGBM', cidade: 'Vilhena', comando: 'COB II' },
  { unidade: '3º GBM / 2º SGBM', cidade: 'Cerejeiras', comando: 'COB II' },
  { unidade: '3º GBM / 3º SGBM', cidade: 'Colorado do Oeste', comando: 'COB II' },
  { unidade: '4º GBM', cidade: 'Cacoal', comando: 'COB II' },
  { unidade: '4º GBM / 1º SGBM', cidade: 'Cacoal', comando: 'COB II' },
  { unidade: '4º GBM / 2º SGBM', cidade: 'Pimenta Bueno', comando: 'COB II' },
  { unidade: '4º GBM / 3º SGBM', cidade: "Espigão D'Oeste", comando: 'COB II' },
  { unidade: '6º GBM', cidade: 'Rolim de Moura', comando: 'COB II' },
  { unidade: '6º GBM / 1º SGBM', cidade: 'Rolim de Moura', comando: 'COB II' },
  { unidade: '6º GBM / 2º SGBM', cidade: 'São Miguel do Guaporé', comando: 'COB II' },

  // CAT — Coordenadoria de Atividades Técnicas
  { unidade: 'CAT', cidade: 'Porto Velho', comando: 'CAT' },
  { unidade: 'DAT - Porto Velho', cidade: 'Porto Velho', comando: 'CAT' },
  { unidade: 'DAT - Porto Velho / SAT - Porto Velho', cidade: 'Porto Velho', comando: 'CAT' },
  { unidade: 'DAT - Porto Velho / SAT - Candeias', cidade: 'Candeias do Jamari', comando: 'CAT' },
  { unidade: 'DAT - Porto Velho / SAT - Guajará-Mirim', cidade: 'Guajará-Mirim', comando: 'CAT' },
  { unidade: 'DAT - Ariquemes', cidade: 'Ariquemes', comando: 'CAT' },
  { unidade: 'DAT - Ariquemes / SAT - Ariquemes', cidade: 'Ariquemes', comando: 'CAT' },
  { unidade: 'DAT - Ariquemes / SAT - Machadinho', cidade: "Machadinho D'Oeste", comando: 'CAT' },
  { unidade: 'DAT - Ariquemes / SAT - Buritis', cidade: 'Buritis', comando: 'CAT' },
  { unidade: 'DAT - Ji-Paraná', cidade: 'Ji-Paraná', comando: 'CAT' },
  { unidade: 'DAT - Ji-Paraná / SAT - Ji-Paraná', cidade: 'Ji-Paraná', comando: 'CAT' },
  { unidade: 'DAT - Ji-Paraná / SAT - Ouro Preto', cidade: 'Ouro Preto do Oeste', comando: 'CAT' },
  { unidade: 'DAT - Ji-Paraná / SAT - Jaru', cidade: 'Jaru', comando: 'CAT' },
  { unidade: 'DAT - Cacoal', cidade: 'Cacoal', comando: 'CAT' },
  { unidade: 'DAT - Cacoal / SAT - Cacoal', cidade: 'Cacoal', comando: 'CAT' },
  { unidade: 'DAT - Cacoal / SAT - Pimenta Bueno', cidade: 'Pimenta Bueno', comando: 'CAT' },
  { unidade: 'DAT - Cacoal / SAT - Rolim', cidade: 'Rolim de Moura', comando: 'CAT' },
  { unidade: 'DAT - Cacoal / SAT - Espigão', cidade: "Espigão D'Oeste", comando: 'CAT' },
  { unidade: 'DAT - Cacoal / SAT - São Miguel', cidade: 'São Miguel do Guaporé', comando: 'CAT' },
  { unidade: 'DAT - Vilhena', cidade: 'Vilhena', comando: 'CAT' },
  { unidade: 'DAT - Vilhena / SAT - Vilhena', cidade: 'Vilhena', comando: 'CAT' },
  { unidade: 'DAT - Vilhena / SAT - Cerejeiras', cidade: 'Cerejeiras', comando: 'CAT' },
  { unidade: 'DAT - Vilhena / SAT - Colorado', cidade: 'Colorado do Oeste', comando: 'CAT' },

  // COA — Coordenadoria Operacional Administrativa
  { unidade: 'COA', cidade: 'Porto Velho', comando: 'COA' },
  { unidade: 'GOA', cidade: 'Porto Velho', comando: 'COA' },

  // CEEI — Centro de Ensino e Instrução
  { unidade: 'CEEI', cidade: 'Porto Velho', comando: 'CEEI' },
  { unidade: 'CEEI / CMDPII-2', cidade: 'Vilhena', comando: 'CEEI' },

  // Unidades administrativas (sede única, todas em Porto Velho)
  { unidade: 'Gabinete do Comando Geral', cidade: 'Porto Velho', comando: 'Comando Geral' },
  { unidade: 'Ajudância Geral', cidade: 'Porto Velho', comando: 'Comando Geral' },
  { unidade: 'CHEM', cidade: 'Porto Velho', comando: 'Comando Geral' },
  { unidade: 'CPOF', cidade: 'Porto Velho', comando: 'CPOF' },
  { unidade: 'DPLAN', cidade: 'Porto Velho', comando: 'DPLAN' },
  { unidade: 'DLOG', cidade: 'Porto Velho', comando: 'DLOG' },
  { unidade: 'DCS', cidade: 'Porto Velho', comando: 'DCS' },
  { unidade: 'DINF', cidade: 'Porto Velho', comando: 'DINF' },
  { unidade: 'Coordenadoria de Pessoal', cidade: 'Porto Velho', comando: 'Coordenadoria de Pessoal' },
  { unidade: 'Corregedoria', cidade: 'Porto Velho', comando: 'Corregedoria' },
  { unidade: 'Defesa Civil', cidade: 'Porto Velho', comando: 'Defesa Civil' },
  { unidade: 'Diretoria de Inteligência', cidade: 'Porto Velho', comando: 'Diretoria de Inteligência' },
]

function unicosOrdenados(valores) {
  return [...new Set(valores)].sort((a, b) => a.localeCompare(b, 'pt-BR'))
}

export function cidadesDisponiveis() {
  return unicosOrdenados(UNIDADES_CBMRO.map(u => u.cidade))
}

export function comandosPorCidade(cidade) {
  return unicosOrdenados(
    UNIDADES_CBMRO.filter(u => u.cidade === cidade).map(u => u.comando),
  )
}

export function unidadesPorCidadeEComando(cidade, comando) {
  return unicosOrdenados(
    UNIDADES_CBMRO.filter(u => u.cidade === cidade && u.comando === comando).map(u => u.unidade),
  )
}
