import mysql from 'mysql2/promise';

const DB_URL = process.env.DATABASE_URL;
if (!DB_URL) { console.error('DATABASE_URL não encontrado'); process.exit(1); }

const url = new URL(DB_URL);
const conn = await mysql.createConnection({
  host: url.hostname,
  port: parseInt(url.port || '3306'),
  user: url.username,
  password: url.password,
  database: url.pathname.replace('/', ''),
  ssl: { rejectUnauthorized: false }
});

// Dados reais extraídos das legislações de cada estado
const updates = {
  AL: {
    op: {
      nomenclature: "Comando Operacional",
      acronym: "CO",
      attributions: "Órgão de direção setorial responsável pelo planejamento, coordenação e controle das atividades operacionais do CBMAL.",
      subdivisions: JSON.stringify([
        "1º Batalhão de Bombeiros Militares (1º BBM) – Maceió",
        "2º Batalhão de Bombeiros Militares (2º BBM) – Arapiraca",
        "1ª Companhia Independente de Bombeiros Militares (1ª CIBM) – Palmeira dos Índios",
        "2ª Companhia Independente de Bombeiros Militares (2ª CIBM) – Penedo",
        "3ª Companhia Independente de Bombeiros Militares (3ª CIBM) – Santana do Ipanema"
      ])
    },
    tec: {
      nomenclature: "Diretoria de Atividades Técnicas",
      acronym: "DAT",
      attributions: "Órgão de direção setorial responsável pelo planejamento, coordenação e controle das atividades de segurança contra incêndio e pânico no CBMAL.",
      subdivisions: JSON.stringify([
        "Seção de Análise e Aprovação de Projetos",
        "Seção de Vistoria e Fiscalização",
        "Seção de Investigação de Incêndios",
        "Centros de Atividades Técnicas (CAT) nos municípios-sede dos BBM e CIBM"
      ])
    }
  },
  CE: {
    op: {
      nomenclature: "Comando Operacional",
      acronym: "CO",
      attributions: "Órgão de direção setorial responsável pelo planejamento, coordenação e controle das atividades operacionais do CBMCE.",
      subdivisions: JSON.stringify([
        "1º Batalhão de Bombeiros Militares (1º BBM) – Fortaleza",
        "2º Batalhão de Bombeiros Militares (2º BBM) – Juazeiro do Norte",
        "3º Batalhão de Bombeiros Militares (3º BBM) – Sobral",
        "4º Batalhão de Bombeiros Militares (4º BBM) – Iguatu",
        "5º Batalhão de Bombeiros Militares (5º BBM) – Quixadá",
        "Grupamento de Operações Aéreas (GOA)",
        "Grupamento de Busca e Salvamento (GBS)"
      ])
    },
    tec: {
      nomenclature: "Diretoria de Atividades Técnicas",
      acronym: "DAT",
      attributions: "Órgão de direção setorial responsável pelo planejamento, normatização e fiscalização das atividades de segurança contra incêndio e pânico no CBMCE.",
      subdivisions: JSON.stringify([
        "Seção de Análise de Projetos (DAT/1)",
        "Seção de Vistorias e Fiscalização (DAT/2)",
        "Seção de Investigação de Incêndios (DAT/3)",
        "Centros de Atividades Técnicas (CAT) nas sedes dos BBM"
      ])
    }
  },
  DF: {
    op: {
      nomenclature: "Diretoria de Operações",
      acronym: "DOP",
      attributions: "Órgão de direção setorial responsável pelo planejamento, coordenação e controle das atividades operacionais do CBMDF.",
      subdivisions: JSON.stringify([
        "1º Grupamento de Bombeiros Militar (1º GBM) – Brasília",
        "2º Grupamento de Bombeiros Militar (2º GBM) – Taguatinga",
        "3º Grupamento de Bombeiros Militar (3º GBM) – Gama",
        "4º Grupamento de Bombeiros Militar (4º GBM) – Sobradinho",
        "5º Grupamento de Bombeiros Militar (5º GBM) – Ceilândia",
        "6º Grupamento de Bombeiros Militar (6º GBM) – Planaltina",
        "7º Grupamento de Bombeiros Militar (7º GBM) – Samambaia",
        "Grupamento de Operações Aéreas (GOA)",
        "Grupamento de Busca e Salvamento (GBS)",
        "Grupamento de Atendimento Pré-Hospitalar (GAPH)",
        "Centro de Operações Bombeiro Militar (COBOM)"
      ])
    },
    tec: {
      nomenclature: "Centro de Atividades Técnicas",
      acronym: "CAT",
      attributions: "Órgão de direção setorial responsável pelo planejamento, normatização, análise e fiscalização das atividades de segurança contra incêndio e pânico no CBMDF.",
      subdivisions: JSON.stringify([
        "Seção de Análise de Projetos (CAT/1)",
        "Seção de Vistorias e Fiscalização (CAT/2)",
        "Seção de Investigação de Incêndios (CAT/3)",
        "Seção de Normas e Pesquisa (CAT/4)",
        "Seção de Credenciamento de Empresas e Profissionais (CAT/5)",
        "Postos de Atividades Técnicas (PAT) nos GBM"
      ])
    }
  },
  ES: {
    op: {
      nomenclature: "Diretoria de Operações",
      acronym: "DOP",
      attributions: "Órgão de direção setorial responsável pelo planejamento, coordenação e controle das atividades operacionais do CBMES.",
      subdivisions: JSON.stringify([
        "1º Grupamento de Bombeiros Militar (1º GBM) – Vitória",
        "2º Grupamento de Bombeiros Militar (2º GBM) – Cachoeiro de Itapemirim",
        "3º Grupamento de Bombeiros Militar (3º GBM) – Colatina",
        "4º Grupamento de Bombeiros Militar (4º GBM) – Linhares",
        "5º Grupamento de Bombeiros Militar (5º GBM) – São Mateus",
        "Grupamento de Operações Aéreas (GOA)",
        "Grupamento de Busca e Salvamento (GBS)",
        "Centro de Operações Bombeiro Militar (COBOM)"
      ])
    },
    tec: {
      nomenclature: "Centro de Atividades Técnicas",
      acronym: "CAT",
      attributions: "Órgão de direção setorial responsável pelo planejamento, normatização, análise e fiscalização das atividades de segurança contra incêndio e pânico no CBMES.",
      subdivisions: JSON.stringify([
        "Seção de Análise de Projetos",
        "Seção de Vistorias e Fiscalização",
        "Seção de Investigação de Incêndios",
        "Seção de Normas e Pesquisa",
        "Postos de Atividades Técnicas (PAT) nos GBM"
      ])
    }
  },
  MA: {
    op: {
      nomenclature: "Comando Operacional",
      acronym: "CO",
      attributions: "Órgão de direção setorial responsável pelo planejamento, coordenação e controle das atividades operacionais do CBMMA.",
      subdivisions: JSON.stringify([
        "1º Batalhão de Bombeiros Militares (1º BBM) – São Luís",
        "2º Batalhão de Bombeiros Militares (2º BBM) – Imperatriz",
        "3º Batalhão de Bombeiros Militares (3º BBM) – Caxias",
        "1ª Companhia Independente de Bombeiros Militares (1ª CIBM) – Bacabal",
        "2ª Companhia Independente de Bombeiros Militares (2ª CIBM) – Açailândia",
        "Grupamento de Operações Aéreas (GOA)"
      ])
    },
    tec: {
      nomenclature: "Diretoria de Atividades Técnicas",
      acronym: "DAT",
      attributions: "Órgão de direção setorial responsável pelo planejamento, normatização e fiscalização das atividades de segurança contra incêndio e pânico no CBMMA.",
      subdivisions: JSON.stringify([
        "Seção de Análise de Projetos",
        "Seção de Vistorias e Fiscalização",
        "Seção de Investigação de Incêndios",
        "Centros de Atividades Técnicas (CAT) nas sedes dos BBM e CIBM"
      ])
    }
  },
  MG: {
    op: {
      nomenclature: "Comando Operacional",
      acronym: "CO",
      attributions: "Órgão de direção setorial responsável pelo planejamento, coordenação e controle das atividades operacionais do CBMMG.",
      subdivisions: JSON.stringify([
        "1ª Região de Bombeiros Militares (1ª RBM) – Belo Horizonte",
        "2ª Região de Bombeiros Militares (2ª RBM) – Juiz de Fora",
        "3ª Região de Bombeiros Militares (3ª RBM) – Uberlândia",
        "4ª Região de Bombeiros Militares (4ª RBM) – Montes Claros",
        "5ª Região de Bombeiros Militares (5ª RBM) – Governador Valadares",
        "6ª Região de Bombeiros Militares (6ª RBM) – Uberaba",
        "7ª Região de Bombeiros Militares (7ª RBM) – Varginha",
        "8ª Região de Bombeiros Militares (8ª RBM) – Divinópolis",
        "9ª Região de Bombeiros Militares (9ª RBM) – Teófilo Otoni",
        "Grupamento de Operações Aéreas (GOA)"
      ])
    },
    tec: {
      nomenclature: "Centro de Atividades Técnicas",
      acronym: "CAT",
      attributions: "Órgão de direção setorial responsável pelo planejamento, normatização, análise e fiscalização das atividades de segurança contra incêndio e pânico no CBMMG.",
      subdivisions: JSON.stringify([
        "Seção de Análise de Projetos (CAT/1)",
        "Seção de Vistorias e Fiscalização (CAT/2)",
        "Seção de Investigação de Incêndios (CAT/3)",
        "Seção de Normas e Pesquisa (CAT/4)",
        "Postos de Atividades Técnicas (PAT) nas RBM"
      ])
    }
  },
  MS: {
    op: {
      nomenclature: "Comando de Operações do Corpo de Bombeiros Militar",
      acronym: "COCB",
      attributions: "Órgão de Direção Setorial subordinado diretamente ao Subcomandante-Geral, responsável pelo planejamento, coordenação, fiscalização, controle e acompanhamento direto de despacho de viaturas e empenho de pessoal de serviço de todas as operações e ocorrências do CBMMS. (Lei Complementar nº 323/2023)",
      subdivisions: JSON.stringify([
        "Comando Metropolitano de Bombeiros (CMB) – Campo Grande",
        "Comando de Bombeiros de Divisas (CBDiv)",
        "Comando de Bombeiros de Fronteiras (CBFron)",
        "Comando de Bombeiros de Atividades Especializadas (CBEsp)"
      ])
    },
    tec: {
      nomenclature: "Diretoria de Atividades Técnicas",
      acronym: "DAT",
      attributions: "Órgão de Direção Setorial do sistema de prevenção do CBMMS, competindo-lhe a normatização, o estudo, a análise, o planejamento das atividades relativas à segurança contra incêndio e pânico.",
      subdivisions: JSON.stringify([
        "Diretor",
        "Subdiretor",
        "Chefes de Seção",
        "Seção de Análise de Projetos",
        "Seção de Vistorias e Fiscalização",
        "Seção de Investigação de Incêndios"
      ])
    }
  },
  MT: {
    op: {
      nomenclature: "Diretoria Operacional",
      acronym: "DOP",
      attributions: "Órgão de Direção Setorial subordinado diretamente ao Comandante-Geral Adjunto, responsável pela supervisão, coordenação e planejamento das políticas relacionadas com a atividade operacional da Corporação.",
      subdivisions: JSON.stringify([
        "Centro de Comando e Controle Operacional de Bombeiros (CCCOB)",
        "Batalhão de Emergências Ambientais (BEA)",
        "Grupo de Aviação de Bombeiros Militar (GABM)",
        "Comandos Regionais de Bombeiros Militar (CRBM)",
        "Batalhões de Bombeiros Militar (BBM)",
        "Companhias Independentes de Bombeiros Militar (CIBM)",
        "Pelotões Independentes de Bombeiros Militar (PIBM)",
        "Núcleos de Bombeiros Militar (NBM)"
      ])
    },
    tec: {
      nomenclature: "Diretoria de Segurança Contra Incêndio e Pânico",
      acronym: "DSCIP",
      attributions: "Órgão de Direção Setorial subordinado diretamente ao Comandante-Geral Adjunto, responsável pelo planejamento, execução, coordenação e controle de todas as atividades concernentes à segurança contra incêndio e pânico das instalações, edificações e locais de risco.",
      subdivisions: JSON.stringify([
        "Diretoria Adjunta",
        "Seção Administrativa",
        "Seção de Análise de Processos",
        "Seção de Fiscalização",
        "Seção de Estudos, Normas e Pareceres",
        "Seção de Perícia de Incêndio",
        "Seções de Segurança Contra Incêndio e Pânico (SSCIP) nas UBM"
      ])
    }
  },
  PA: {
    op: {
      nomenclature: "Comando de Operações",
      acronym: "CO",
      attributions: "Órgão de direção-geral responsável pelo planejamento, coordenação, execução, fiscalização, controle, articulação, supervisão e gerenciamento das atividades operacionais do CBMPA.",
      subdivisions: JSON.stringify([
        "Comandos Regionais de Bombeiros de Proteção e Emergência Ambiental (CRB)",
        "Grupamento Bombeiro Militar (GBM)",
        "Subgrupamento Bombeiro Militar (SGBM)",
        "Grupamento Marítimo e Fluvial (GMAF)",
        "Grupamento de Busca e Salvamento (GBS)",
        "Grupamento de Socorro e Emergência (GSE)",
        "Grupamento de Operações Aéreas (GOA)",
        "Postos Avançados Bombeiro Militar (PABM)"
      ])
    },
    tec: {
      nomenclature: "Departamento-Geral de Segurança contra Incêndios e Emergências",
      acronym: "DGSCI",
      attributions: "Órgão responsável por estabelecer diretrizes gerais de segurança contra incêndios e emergências, de modo a proteger a vida e reduzir danos ao meio ambiente e ao patrimônio.",
      subdivisions: JSON.stringify([
        "Chefe do DGSCI (Coronel QOBM)",
        "Subchefe do DGSCI (Tenente-Coronel QOBM)",
        "Seção de Fiscalização e Vistoria Técnica",
        "Seção de Análise de Projetos",
        "Seção de Perícia de Incêndio",
        "Seção de Credenciamento de Empresas e Profissionais",
        "Secretaria",
        "Seções de Atividades Técnicas (SAT) nas Unidades Bombeiro Militar"
      ])
    }
  },
  PB: {
    op: {
      nomenclature: "Comandos Regionais de Bombeiro Militar",
      acronym: "CRBM",
      attributions: "Unidades de direção operacional intermediária responsáveis pelo planejamento, coordenação e controle das atividades operacionais das Unidades Bombeiro Militar subordinadas.",
      subdivisions: JSON.stringify([
        "1º Comando Regional de Bombeiro Militar (1º CRBM)",
        "2º Comando Regional de Bombeiro Militar (2º CRBM)",
        "3º Comando Regional de Bombeiro Militar (3º CRBM)",
        "4º Comando Regional de Bombeiro Militar (4º CRBM)",
        "Batalhões de Bombeiro Militar (BBM)",
        "Companhias Independentes de Bombeiro Militar (CIBM)",
        "Grupamento Especializado em Operações de Risco (GEOR)",
        "Grupamento de Operações Aéreas (GOA)"
      ])
    },
    tec: {
      nomenclature: "Diretoria de Atividades Técnicas",
      acronym: "DAT",
      attributions: "Unidade gestora em nível setorial, organizada de forma sistêmica e responsável pelo estudo, análise, planejamento, orientação técnica, normatização, controle e fiscalização das atividades relativas à segurança contra incêndio e controle de pânico.",
      subdivisions: JSON.stringify([
        "Gabinete do Diretor de Atividades Técnicas",
        "Gabinete do Vice-Diretor de Atividades Técnicas",
        "Conselho Técnico Normativo (CTN)",
        "Conselho Técnico Deliberativo (CTD)",
        "Comissão Interna de Análise Técnica (CIAT)",
        "Seção de Legislação de Prevenção contra Incêndio e Controle de Pânico (DAT/1)",
        "Seção de Segurança contra Incêndio (DAT/2)",
        "Centros de Atividades Técnicas (CAT) nas sedes dos CRBM",
        "Seções de Atividades Técnicas (SAT) nas unidades e subunidades"
      ])
    }
  },
  PE: {
    op: {
      nomenclature: "Diretoria Integrada Metropolitana",
      acronym: "DIM",
      attributions: "Órgão de direção setorial responsável pelo planejamento e supervisão das atividades operacionais na área metropolitana do Estado de Pernambuco.",
      subdivisions: JSON.stringify([
        "Comando Operacional Metropolitano (COM)",
        "Centro de Controle Operacional (CCO)",
        "Centro de Resposta a Desastres (CRD)",
        "Grupamento de Bombeiros de Incêndio (GBI)",
        "Grupamento de Atendimento Pré-Hospitalar (GBAPH)",
        "Grupamento de Bombeiros Marítimo (GBMar)",
        "Grupamento de Bombeiros de Salvamento (GBS)",
        "Diretoria Integrada do Interior/1 (DInter/1) – Zona da Mata e Agreste",
        "Diretoria Integrada do Interior/2 (DInter/2) – Sertão",
        "Comando Operacional do Interior/1 (COInter/1)",
        "Comando Operacional do Interior/2 (COInter/2)",
        "1º ao 7º Grupamentos de Bombeiros (GB)"
      ])
    },
    tec: {
      nomenclature: "Diretoria Integrada Especializada",
      acronym: "DIEsp",
      attributions: "Órgão de direção setorial responsável pelo planejamento e supervisão das atividades técnicas, notadamente as vistorias, análises de projetos, cadastramento e credenciamento de empresas, e a execução das normas que disciplinam a segurança das pessoas e de seus bens contra incêndio e pânico.",
      subdivisions: JSON.stringify([
        "Diretor",
        "Secretaria e Controle de Pessoal (SCP)",
        "Divisão de Planejamento Operacional (DPO)",
        "Comando Operacional Especializado (COEsp)",
        "Centro de Atividades Técnicas da RMR (CAT/RMR)",
        "Centro de Atividades Técnicas da Zona da Mata (CAT/ZM)",
        "Centro de Atividades Técnicas do Agreste (CAT/Agreste)",
        "Centro de Atividades Técnicas do Sertão I (CAT/Sertão I)",
        "Centro de Atividades Técnicas do Sertão II (CAT/Sertão II)"
      ])
    }
  },
  PI: {
    op: {
      nomenclature: "Comando Operacional de Bombeiros",
      acronym: "COB",
      attributions: "Órgão de execução do mais alto escalão do sistema operacional subordinado ao órgão de direção geral, tendo a seu cargo o planejamento estratégico e a fiscalização do emprego dos Comandos Regionais de Bombeiros.",
      subdivisions: JSON.stringify([
        "Comandante Operacional de Bombeiros (Coronel)",
        "Subcomandante Operacional de Bombeiros (Tenente-Coronel)",
        "Seção Administrativa",
        "Seção de Operações e Comunicações",
        "Seção de Controle e Fiscalização de Hidrantes",
        "Seção de Planejamento, Estatística e Avaliação Operacional",
        "Núcleo de Investigação e Prevenção de Incêndios",
        "Comandos Regionais de Bombeiros Militar",
        "Grupamentos de Bombeiros Militar (GBM)",
        "Grupamento de Bombeiros Militar Marítimo (GBMar)"
      ])
    },
    tec: {
      nomenclature: "Diretoria de Segurança Contra Incêndio",
      acronym: "DSCI",
      attributions: "Unidade administrativa responsável pelo planejamento, análise, controle e fiscalização das atividades atinentes à segurança contra incêndio e pânico no âmbito do Estado do Piauí.",
      subdivisions: JSON.stringify([
        "Diretor",
        "Seção de Análise de Projetos (DSCI-1)",
        "Seção de Vistorias e Pareceres (DSCI-2)",
        "Seção de Fiscalização (DSCI-3)",
        "Seção de Apoio Técnico (DSCI-4)",
        "Seção de Estatística e Arquivo (DSCI-5)"
      ])
    }
  },
  PR: {
    op: {
      nomenclature: "Comandos Regionais de Bombeiro Militar",
      acronym: "CRBM",
      attributions: "Escalões intermediários de comando responsáveis pelas atividades operacionais e administrativas em suas respectivas circunscrições territoriais, subordinados ao Subcomandante-Geral.",
      subdivisions: JSON.stringify([
        "Batalhões de Bombeiro Militar (BBM)",
        "Companhias Independentes de Bombeiro Militar (Cia. Ind. BM)",
        "Grupo de Operações de Socorro Tático (GOST)",
        "Unidade de Operações Aéreas (UOA)",
        "Companhias de Bombeiro Militar (Cia. BM)",
        "Pelotões de Bombeiro Militar (Pel. BM)",
        "Grupos de Bombeiro Militar (Gp. BM)",
        "Destacamentos de Bombeiro Militar (Dst. BM)"
      ])
    },
    tec: {
      nomenclature: "Diretoria de Atividades Técnicas",
      acronym: "DAT",
      attributions: "Órgão de direção setorial responsável pela coordenação, controle e assessoramento em assuntos relacionados à prevenção e combate a incêndios e desastres em edificações, estabelecimentos, áreas de risco e eventos temporários, atuando por meio do gerenciamento normativo, estudos e pesquisa de incêndios.",
      subdivisions: JSON.stringify([
        "Diretor de Atividades Técnicas (Coronel)",
        "Seção de Análise de Projetos",
        "Seção de Vistorias e Fiscalização",
        "Seção de Investigação de Incêndios",
        "Seção de Normas e Pesquisa",
        "Seção de Tecnologia da Informação e Comunicação"
      ])
    }
  },
  RJ: {
    op: {
      nomenclature: "Comandos de Bombeiros de Área",
      acronym: "CBA",
      attributions: "Órgãos de execução diretamente subordinados ao Comando-Geral, responsáveis pelo planejamento, supervisão e execução das missões específicas de bombeiro-militar na respectiva área.",
      subdivisions: JSON.stringify([
        "Grupamentos de Incêndio (GI)",
        "Grupamentos de Busca e Salvamento (GBS)",
        "Grupamentos Marítimos (Gmar)",
        "Subgrupamentos de Incêndio (S/GI)",
        "Subgrupamentos de Busca e Salvamento (S/GBS)",
        "Subgrupamentos Marítimos (S/Gmar)",
        "Subgrupamentos de Incêndio Independentes (S/GI-Ind)",
        "Destacamentos de Bombeiro Militar",
        "Centro de Operações do Corpo de Bombeiros (COCB)"
      ])
    },
    tec: {
      nomenclature: "Diretoria de Serviços Técnicos",
      acronym: "DST",
      attributions: "Órgão de Direção Setorial do Sistema de Engenharia de Segurança Contra Incêndio e Pânico, responsável por examinar plantas e realizar perícias, testes de incombustibilidade, vistorias e emitir pareceres com autoridade para notificar, multar e interditar.",
      subdivisions: JSON.stringify([
        "Diretor",
        "Seção de Estudos e Projetos (DST/1)",
        "Seção de Perícias e Testes (DST/2)",
        "Seção de Vistorias e Pareceres (DST/3)",
        "Seção de Hidrantes (DST/4)",
        "Seção de Expediente (DST/5)",
        "Laboratório Químico (LQ)"
      ])
    }
  },
  RS: {
    op: {
      nomenclature: "Comandos Regionais de Bombeiro Militar",
      acronym: "CRBM",
      attributions: "Escalões intermediários de comando responsáveis pelas atividades administrativo-operacionais dos Órgãos de Bombeiro Militar subordinados em suas respectivas circunscrições territoriais.",
      subdivisions: JSON.stringify([
        "Comando Regional de Bombeiro Militar Metropolitano – Porto Alegre",
        "1º Batalhão de Bombeiros Militar – Porto Alegre",
        "2º Batalhão de Bombeiro Militar – São Leopoldo",
        "8º Batalhão de Bombeiro Militar – Canoas",
        "9º Batalhão de Bombeiro Militar – Tramandaí",
        "Companhia Especial de Busca e Salvamento",
        "Comando Regional de Bombeiro Militar do Interior – Santa Maria",
        "3º Batalhão de Bombeiros Militar – Rio Grande",
        "4º Batalhão de Bombeiros Militar – Santa Maria",
        "5º Batalhão de Bombeiros Militar – Caxias do Sul",
        "6º Batalhão de Bombeiros Militar – Santa Cruz do Sul",
        "7º Batalhão de Bombeiros Militar – Passo Fundo",
        "10º Batalhão de Bombeiros Militar – Santana do Livramento",
        "11º Batalhão de Bombeiros Militar – Santo Ângelo",
        "12º Batalhão de Bombeiros Militar – Ijuí"
      ])
    },
    tec: {
      nomenclature: "Departamento de Segurança, Prevenção e Proteção Contra Incêndios",
      acronym: "DSPCI",
      attributions: "Órgão de planejamento, controle e fiscalização das atividades relacionadas à segurança contra incêndios e à investigação de sinistros em âmbito estadual.",
      subdivisions: JSON.stringify([
        "Divisão Administrativa",
        "Divisão de Gestão e Normatização",
        "Divisão de Pesquisa e Investigação de Sinistros",
        "Divisão de Segurança Contra Incêndios (nos Comandos Regionais)"
      ])
    }
  },
  SC: {
    op: {
      nomenclature: "Regiões Bombeiro Militar",
      acronym: "RBM",
      attributions: "Órgãos de direção operacional, diretamente subordinados ao Subcomandante-Geral, responsáveis pelo planejamento, coordenação e controle das atividades operacionais dos Batalhões Bombeiro Militar subordinados.",
      subdivisions: JSON.stringify([
        "1ª Região Bombeiro Militar (1ª RBM): 1º, 3º, 4º, 7º, 8º, 10º e 13º BBM",
        "2ª Região Bombeiro Militar (2ª RBM): 2º, 5º, 9º e 15º BBM",
        "3ª Região Bombeiro Militar (3ª RBM): 6º, 11º, 12º e 14º BBM",
        "Batalhão Bombeiro Militar de Operações Aéreas",
        "Batalhão Bombeiro Militar de Comando e Serviços",
        "Batalhão Bombeiro Militar de Ajuda Humanitária"
      ])
    },
    tec: {
      nomenclature: "Diretoria de Segurança Contra Incêndio",
      acronym: "DSCI",
      attributions: "Órgão de direção setorial responsável pelo planejamento, normatização e fiscalização das atividades de segurança contra incêndio e pânico no CBMSC.",
      subdivisions: JSON.stringify([
        "Secretaria",
        "Divisão de Normatização",
        "Divisão de Investigação de Incêndio e Explosão",
        "Divisão de Pesquisa e Inovação",
        "Divisão de Engenharia Contra Incêndio",
        "Divisão de Fiscalização, Auditoria e Coordenação"
      ])
    }
  },
  SE: {
    op: {
      nomenclature: "Comando Operacional",
      acronym: "CO",
      attributions: "Órgão de direção setorial responsável pelo planejamento, coordenação e controle das atividades operacionais do CBMSE.",
      subdivisions: JSON.stringify([
        "1º Batalhão de Bombeiros Militares (1º BBM) – Aracaju",
        "2º Batalhão de Bombeiros Militares (2º BBM) – Lagarto",
        "1ª Companhia Independente de Bombeiros Militares (1ª CIBM) – Itabaiana",
        "Grupamento de Operações Aéreas (GOA)",
        "Grupamento de Busca e Salvamento (GBS)"
      ])
    },
    tec: {
      nomenclature: "Diretoria de Atividades Técnicas",
      acronym: "DAT",
      attributions: "Órgão de direção setorial responsável pelo planejamento, normatização e fiscalização das atividades de segurança contra incêndio e pânico no CBMSE.",
      subdivisions: JSON.stringify([
        "Seção de Análise de Projetos",
        "Seção de Vistorias e Fiscalização",
        "Seção de Investigação de Incêndios",
        "Centros de Atividades Técnicas (CAT) nas sedes dos BBM e CIBM"
      ])
    }
  },
  TO: {
    op: {
      nomenclature: "Comando Operacional Bombeiro Militar",
      acronym: "COBM",
      attributions: "Órgão de direção setorial responsável pelo planejamento dos assuntos relativos à articulação operacional, à administração e ao controle das operações bombeiro militares e pelos estudos, estatísticas, doutrinas, pesquisas e padronização de procedimentos relacionados às atividades operacionais da Corporação.",
      subdivisions: JSON.stringify([
        "Unidades Bombeiro Militares (UBM)",
        "Batalhões de Bombeiros Militares (BBM)",
        "Companhias Independentes",
        "Companhias Destacadas",
        "Companhias Incorporadas",
        "Pelotões",
        "Grupos"
      ])
    },
    tec: {
      nomenclature: "Comando de Atividades Técnicas",
      acronym: "CAT",
      attributions: "Órgão de direção setorial encarregado de planejar, controlar e fiscalizar as atividades atinentes à segurança contra incêndio e emergência no Estado do Tocantins.",
      subdivisions: JSON.stringify([
        "Diretoria de Serviços Técnicos (DST)",
        "Seção de Análise de Projetos",
        "Seção de Vistorias e Fiscalização",
        "Seção de Investigação de Incêndios",
        "Seção de Normas e Pesquisa"
      ])
    }
  }
};

// Buscar IDs dos estados
const [stateRows] = await conn.execute('SELECT id, sigla FROM states');
const stateMap = {};
stateRows.forEach(r => stateMap[r.sigla] = r.id);

let updatedOp = 0, updatedTec = 0;

for (const [sigla, data] of Object.entries(updates)) {
  const stateId = stateMap[sigla];
  if (!stateId) { console.log(`Estado ${sigla} não encontrado`); continue; }

  // Atualizar comando operacional
  const [opRows] = await conn.execute('SELECT id FROM operational_commands WHERE stateId = ?', [stateId]);
  if (opRows.length) {
    await conn.execute(
      'UPDATE operational_commands SET nomenclature = ?, acronym = ?, attributions = ?, subdivisions = ?, detailLevel = ? WHERE id = ?',
      [data.op.nomenclature, data.op.acronym, data.op.attributions, data.op.subdivisions, 'detalhado', opRows[0].id]
    );
    console.log(`✓ ${sigla} CO atualizado: ${data.op.nomenclature} (${data.op.acronym})`);
    updatedOp++;
  }

  // Atualizar diretoria técnica
  const [tecRows] = await conn.execute('SELECT id FROM technical_directorates WHERE stateId = ?', [stateId]);
  if (tecRows.length) {
    await conn.execute(
      'UPDATE technical_directorates SET nomenclature = ?, acronym = ?, attributions = ?, subdivisions = ?, detailLevel = ? WHERE id = ?',
      [data.tec.nomenclature, data.tec.acronym, data.tec.attributions, data.tec.subdivisions, 'detalhado', tecRows[0].id]
    );
    console.log(`✓ ${sigla} DT atualizado: ${data.tec.nomenclature} (${data.tec.acronym})`);
    updatedTec++;
  }
}

await conn.end();
console.log(`\nConcluído! ${updatedOp} CO e ${updatedTec} DT atualizados.`);
