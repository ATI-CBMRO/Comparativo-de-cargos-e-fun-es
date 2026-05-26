import mysql from "mysql2/promise";

// Mapeamento de IDs (oc_id = operational_command_id, td_id = technical_directorate_id)
const IDS = {
  AL: { oc: 1, td: 1 },
  CE: { oc: 2, td: 2 },
  DF: { oc: 3, td: 3 },
  ES: { oc: 4, td: 4 },
  MA: { oc: 5, td: 5 },
  MT: { oc: 6, td: 6 },
  MS: { oc: 7, td: 7 },
  MG: { oc: 8, td: 8 },
  PA: { oc: 9, td: 9 },
  PB: { oc: 10, td: 10 },
  PR: { oc: 11, td: 11 },
  PE: { oc: 12, td: 12 },
  PI: { oc: 13, td: 13 },
  RJ: { oc: 14, td: 14 },
  RS: { oc: 15, td: 15 },
  RO: { oc: 16, td: 16 },
  SC: { oc: 17, td: 17 },
  SE: { oc: 18, td: 18 },
  TO: { oc: 19, td: 19 },
};

// Dados de cargos e funções por estado
// Formato: { oc: [...], td: [...] }
// Cada cargo: { title, acronym, rank, subordinateTo, subordinates, attributions, sortOrder }
const POSITIONS_DATA = {

  // ── ALAGOAS ──────────────────────────────────────────────────────────────────
  AL: {
    oc: [
      {
        title: "Comandante Operacional de Bombeiros",
        acronym: "COB",
        rank: "Coronel BM",
        subordinateTo: "Comandante-Geral",
        subordinates: "Subcomandante Operacional; Seção de Planejamento Operacional; Seção de Operações; Seção de Comunicações; Grupamentos de Bombeiros",
        attributions: "Planejar, dirigir, coordenar e controlar as atividades operacionais do CBMAL; Supervisionar os Grupamentos de Bombeiros; Propor normas e procedimentos operacionais; Representar o Comando Operacional junto ao Comando-Geral",
        sortOrder: 1,
      },
      {
        title: "Subcomandante Operacional de Bombeiros",
        acronym: "SCOB",
        rank: "Tenente-Coronel BM",
        subordinateTo: "Comandante Operacional de Bombeiros",
        subordinates: "Seção de Planejamento Operacional; Seção de Operações",
        attributions: "Auxiliar o Comandante Operacional; Substituir o Comandante Operacional em suas ausências; Coordenar as seções subordinadas; Supervisionar o cumprimento das normas operacionais",
        sortOrder: 2,
      },
      {
        title: "Chefe da Seção de Planejamento Operacional",
        acronym: "S/PO",
        rank: "Major BM",
        subordinateTo: "Subcomandante Operacional de Bombeiros",
        subordinates: null,
        attributions: "Elaborar planos e programas operacionais; Analisar dados estatísticos de ocorrências; Propor melhorias nos procedimentos operacionais; Elaborar relatórios de atividades operacionais",
        sortOrder: 3,
      },
      {
        title: "Chefe da Seção de Operações",
        acronym: "S/OP",
        rank: "Major BM",
        subordinateTo: "Subcomandante Operacional de Bombeiros",
        subordinates: null,
        attributions: "Coordenar as operações em andamento; Manter o controle das ocorrências; Elaborar escalas de serviço operacional; Supervisionar o emprego dos meios operacionais",
        sortOrder: 4,
      },
    ],
    td: [
      {
        title: "Diretor de Serviços Técnicos",
        acronym: "DST",
        rank: "Coronel BM",
        subordinateTo: "Comandante-Geral",
        subordinates: "Subdiretor de Serviços Técnicos; Seção de Análise de Projetos; Seção de Fiscalização; Seção de Normas Técnicas",
        attributions: "Planejar, dirigir e controlar as atividades de segurança contra incêndio e pânico; Supervisionar a análise de projetos de SPCI; Coordenar as atividades de fiscalização de edificações; Propor normas técnicas de prevenção",
        sortOrder: 1,
      },
      {
        title: "Subdiretor de Serviços Técnicos",
        acronym: "SDST",
        rank: "Tenente-Coronel BM",
        subordinateTo: "Diretor de Serviços Técnicos",
        subordinates: "Seção de Análise de Projetos; Seção de Fiscalização",
        attributions: "Auxiliar o Diretor de Serviços Técnicos; Substituir o Diretor em suas ausências; Coordenar as atividades das seções subordinadas",
        sortOrder: 2,
      },
      {
        title: "Chefe da Seção de Análise de Projetos",
        acronym: "SAP",
        rank: "Major BM",
        subordinateTo: "Subdiretor de Serviços Técnicos",
        subordinates: null,
        attributions: "Analisar e aprovar projetos de sistemas de prevenção e combate a incêndio; Emitir pareceres técnicos sobre projetos; Controlar o arquivo de projetos aprovados; Orientar projetistas sobre as normas técnicas aplicáveis",
        sortOrder: 3,
      },
      {
        title: "Chefe da Seção de Fiscalização",
        acronym: "SF",
        rank: "Major BM",
        subordinateTo: "Subdiretor de Serviços Técnicos",
        subordinates: null,
        attributions: "Coordenar as vistorias em edificações; Emitir laudos de vistoria; Autuar estabelecimentos em situação irregular; Controlar os prazos de regularização das edificações vistoriadas",
        sortOrder: 4,
      },
    ],
  },

  // ── CEARÁ ────────────────────────────────────────────────────────────────────
  CE: {
    oc: [
      {
        title: "Coordenador Operacional",
        acronym: "COORD-OP",
        rank: "Coronel BM",
        subordinateTo: "Comandante-Geral",
        subordinates: "Subcoordernador Operacional; Seção de Operações; Seção de Planejamento; Batalhões de Bombeiros",
        attributions: "Coordenar e supervisionar todas as atividades operacionais do CBMCE; Planejar e controlar o emprego dos meios operacionais; Propor políticas operacionais ao Comando-Geral; Supervisionar os Batalhões de Bombeiros",
        sortOrder: 1,
      },
      {
        title: "Subcoordernador Operacional",
        acronym: "SCOORD-OP",
        rank: "Tenente-Coronel BM",
        subordinateTo: "Coordenador Operacional",
        subordinates: "Seção de Operações; Seção de Planejamento",
        attributions: "Auxiliar o Coordenador Operacional; Substituir o Coordenador em suas ausências e impedimentos; Coordenar as seções da Coordenadoria Operacional",
        sortOrder: 2,
      },
      {
        title: "Chefe da Seção de Operações",
        acronym: "S/OP",
        rank: "Major BM",
        subordinateTo: "Subcoordernador Operacional",
        subordinates: null,
        attributions: "Controlar e registrar as ocorrências operacionais; Elaborar escalas de serviço; Manter atualizado o banco de dados operacionais; Coordenar o Centro de Operações de Bombeiros",
        sortOrder: 3,
      },
      {
        title: "Chefe da Seção de Planejamento",
        acronym: "S/PL",
        rank: "Major BM",
        subordinateTo: "Subcoordernador Operacional",
        subordinates: null,
        attributions: "Elaborar planos operacionais; Analisar estatísticas de ocorrências; Propor melhorias nos procedimentos operacionais; Elaborar o Plano Anual de Atividades Operacionais",
        sortOrder: 4,
      },
    ],
    td: [
      {
        title: "Coordenador de Atividades Técnicas",
        acronym: "COORD-AT",
        rank: "Coronel BM",
        subordinateTo: "Comandante-Geral",
        subordinates: "Subcoordernador de Atividades Técnicas; Seção de Análise e Aprovação de Projetos; Seção de Fiscalização e Vistoria; Seção de Normas e Pesquisa",
        attributions: "Coordenar e supervisionar as atividades de segurança contra incêndio e pânico; Propor normas técnicas de prevenção; Supervisionar a análise de projetos e fiscalização de edificações; Representar o CBMCE em comissões técnicas",
        sortOrder: 1,
      },
      {
        title: "Subcoordernador de Atividades Técnicas",
        acronym: "SCOORD-AT",
        rank: "Tenente-Coronel BM",
        subordinateTo: "Coordenador de Atividades Técnicas",
        subordinates: "Seção de Análise e Aprovação de Projetos; Seção de Fiscalização e Vistoria",
        attributions: "Auxiliar o Coordenador de Atividades Técnicas; Substituir o Coordenador em suas ausências; Coordenar as atividades das seções subordinadas",
        sortOrder: 2,
      },
      {
        title: "Chefe da Seção de Análise e Aprovação de Projetos",
        acronym: "SAAP",
        rank: "Major BM",
        subordinateTo: "Subcoordernador de Atividades Técnicas",
        subordinates: null,
        attributions: "Analisar projetos de SPCI; Emitir pareceres técnicos; Controlar o arquivo de projetos; Orientar projetistas e responsáveis técnicos",
        sortOrder: 3,
      },
      {
        title: "Chefe da Seção de Fiscalização e Vistoria",
        acronym: "SFV",
        rank: "Major BM",
        subordinateTo: "Subcoordernador de Atividades Técnicas",
        subordinates: null,
        attributions: "Coordenar as vistorias em edificações e áreas de risco; Emitir laudos de vistoria; Autuar estabelecimentos irregulares; Controlar os prazos de regularização",
        sortOrder: 4,
      },
    ],
  },

  // ── DISTRITO FEDERAL ─────────────────────────────────────────────────────────
  DF: {
    oc: [
      {
        title: "Comandante Operacional",
        acronym: "COMOP",
        rank: "Coronel BM",
        subordinateTo: "Comandante-Geral do CBMDF",
        subordinates: "Subcomandante Operacional; Centro de Operações de Bombeiros Militar; Grupamentos de Bombeiros Militares; Grupamentos Especializados",
        attributions: "Planejar, coordenar, controlar e supervisionar as atividades operacionais do CBMDF; Propor ao Comandante-Geral políticas e diretrizes operacionais; Supervisionar o Centro de Operações de Bombeiros Militar; Coordenar as ações de resposta a emergências de grande porte",
        sortOrder: 1,
      },
      {
        title: "Subcomandante Operacional",
        acronym: "SCOMOP",
        rank: "Tenente-Coronel BM",
        subordinateTo: "Comandante Operacional",
        subordinates: "Centro de Operações de Bombeiros Militar; Seção de Planejamento Operacional",
        attributions: "Auxiliar o Comandante Operacional no planejamento e controle das atividades; Substituir o Comandante Operacional em suas ausências; Supervisionar as atividades do Centro de Operações",
        sortOrder: 2,
      },
      {
        title: "Chefe do Centro de Operações de Bombeiros Militar",
        acronym: "COBOM",
        rank: "Major BM",
        subordinateTo: "Subcomandante Operacional",
        subordinates: "Seção de Despacho; Seção de Comunicações; Seção de Estatística Operacional",
        attributions: "Coordenar o atendimento e despacho de ocorrências; Manter o controle das viaturas e equipes em serviço; Elaborar relatórios de ocorrências; Gerenciar o sistema de comunicações operacionais",
        sortOrder: 3,
      },
      {
        title: "Comandante de Grupamento de Bombeiros Militar",
        acronym: "CGBM",
        rank: "Major BM / Capitão BM",
        subordinateTo: "Comandante Operacional",
        subordinates: "Subcomandante de Grupamento; Seções de Bombeiros; Postos Avançados",
        attributions: "Comandar e administrar o Grupamento de Bombeiros Militar; Garantir a prontidão operacional da unidade; Supervisionar o treinamento e a manutenção dos meios; Responder pelas atividades operacionais na área de atuação",
        sortOrder: 4,
      },
    ],
    td: [
      {
        title: "Diretor do Departamento de Segurança Contra Incêndio",
        acronym: "DSCI",
        rank: "Coronel BM",
        subordinateTo: "Comandante-Geral do CBMDF",
        subordinates: "Subdiretor do DSCI; Seção de Análise de Projetos; Seção de Fiscalização; Seção de Normas e Pesquisa; Seção de Investigação de Incêndios",
        attributions: "Dirigir, planejar e controlar as atividades de segurança contra incêndio e pânico no DF; Propor normas técnicas de prevenção; Supervisionar a análise de projetos e fiscalização; Coordenar as investigações de incêndio; Representar o CBMDF em comissões técnicas e normativas",
        sortOrder: 1,
      },
      {
        title: "Subdiretor do Departamento de Segurança Contra Incêndio",
        acronym: "SDSCI",
        rank: "Tenente-Coronel BM",
        subordinateTo: "Diretor do DSCI",
        subordinates: "Seção de Análise de Projetos; Seção de Fiscalização; Seção de Normas e Pesquisa",
        attributions: "Auxiliar o Diretor do DSCI; Substituir o Diretor em suas ausências; Coordenar as atividades das seções subordinadas; Supervisionar a execução dos planos e programas de prevenção",
        sortOrder: 2,
      },
      {
        title: "Chefe da Seção de Análise de Projetos",
        acronym: "SAP",
        rank: "Major BM",
        subordinateTo: "Subdiretor do DSCI",
        subordinates: null,
        attributions: "Analisar e aprovar projetos de sistemas de prevenção e combate a incêndio; Emitir Certificados de Conformidade de Projetos; Controlar o arquivo de projetos aprovados; Orientar projetistas e responsáveis técnicos sobre as normas aplicáveis",
        sortOrder: 3,
      },
      {
        title: "Chefe da Seção de Fiscalização",
        acronym: "SF",
        rank: "Major BM",
        subordinateTo: "Subdiretor do DSCI",
        subordinates: null,
        attributions: "Coordenar as vistorias em edificações e áreas de risco; Emitir Certificados de Vistoria do Corpo de Bombeiros; Autuar estabelecimentos em situação irregular; Controlar os prazos de regularização",
        sortOrder: 4,
      },
      {
        title: "Chefe da Seção de Normas e Pesquisa",
        acronym: "SNP",
        rank: "Major BM",
        subordinateTo: "Subdiretor do DSCI",
        subordinates: null,
        attributions: "Elaborar e revisar normas técnicas de prevenção contra incêndio; Realizar pesquisas sobre novas tecnologias de SPCI; Representar o CBMDF em comissões de normatização; Manter atualizado o acervo técnico-normativo",
        sortOrder: 5,
      },
    ],
  },

  // ── ESPÍRITO SANTO ───────────────────────────────────────────────────────────
  ES: {
    oc: [
      {
        title: "Diretor de Operações",
        acronym: "DO",
        rank: "Coronel BM",
        subordinateTo: "Comandante-Geral do CBMES",
        subordinates: "Subdiretor de Operações; Seção de Operações; Seção de Planejamento Operacional; Batalhões de Bombeiros Militares",
        attributions: "Planejar, dirigir, coordenar e controlar as atividades operacionais do CBMES; Propor políticas e diretrizes operacionais; Supervisionar os Batalhões de Bombeiros Militares; Coordenar as ações de resposta a grandes emergências",
        sortOrder: 1,
      },
      {
        title: "Subdiretor de Operações",
        acronym: "SDO",
        rank: "Tenente-Coronel BM",
        subordinateTo: "Diretor de Operações",
        subordinates: "Seção de Operações; Seção de Planejamento Operacional",
        attributions: "Auxiliar o Diretor de Operações; Substituir o Diretor em suas ausências; Coordenar as seções subordinadas; Supervisionar o cumprimento das normas operacionais",
        sortOrder: 2,
      },
      {
        title: "Chefe da Seção de Operações",
        acronym: "S/OP",
        rank: "Major BM",
        subordinateTo: "Subdiretor de Operações",
        subordinates: null,
        attributions: "Controlar e registrar as ocorrências operacionais; Elaborar escalas de serviço; Coordenar o Centro de Operações de Bombeiros; Manter atualizado o banco de dados operacionais",
        sortOrder: 3,
      },
    ],
    td: [
      {
        title: "Diretor do Centro de Atividades Técnicas",
        acronym: "CAT",
        rank: "Coronel BM",
        subordinateTo: "Comandante-Geral do CBMES",
        subordinates: "Subdiretor do CAT; Seção de Análise de Projetos; Seção de Fiscalização; Seção de Normas Técnicas; Seção de Investigação de Incêndios",
        attributions: "Planejar, dirigir e controlar as atividades de segurança contra incêndio e pânico no ES; Propor normas técnicas de prevenção; Supervisionar a análise de projetos e fiscalização; Coordenar as investigações de incêndio; Representar o CBMES em fóruns técnicos",
        sortOrder: 1,
      },
      {
        title: "Subdiretor do Centro de Atividades Técnicas",
        acronym: "SCAT",
        rank: "Tenente-Coronel BM",
        subordinateTo: "Diretor do CAT",
        subordinates: "Seção de Análise de Projetos; Seção de Fiscalização; Seção de Normas Técnicas",
        attributions: "Auxiliar o Diretor do CAT; Substituir o Diretor em suas ausências; Coordenar as atividades das seções subordinadas",
        sortOrder: 2,
      },
      {
        title: "Chefe da Seção de Análise de Projetos",
        acronym: "SAP",
        rank: "Major BM",
        subordinateTo: "Subdiretor do CAT",
        subordinates: null,
        attributions: "Analisar e aprovar projetos de SPCI; Emitir pareceres técnicos; Controlar o arquivo de projetos aprovados; Orientar projetistas sobre as normas técnicas aplicáveis",
        sortOrder: 3,
      },
      {
        title: "Chefe da Seção de Fiscalização",
        acronym: "SF",
        rank: "Major BM",
        subordinateTo: "Subdiretor do CAT",
        subordinates: null,
        attributions: "Coordenar as vistorias em edificações; Emitir laudos e certificados de vistoria; Autuar estabelecimentos irregulares; Controlar os prazos de regularização",
        sortOrder: 4,
      },
      {
        title: "Chefe da Seção de Investigação de Incêndios",
        acronym: "SII",
        rank: "Capitão BM",
        subordinateTo: "Subdiretor do CAT",
        subordinates: null,
        attributions: "Coordenar as investigações de causas e circunstâncias de incêndios; Elaborar laudos de investigação; Manter banco de dados de incêndios investigados; Propor medidas preventivas baseadas nos resultados das investigações",
        sortOrder: 5,
      },
    ],
  },

  // ── MARANHÃO ─────────────────────────────────────────────────────────────────
  MA: {
    oc: [
      {
        title: "Comandante Operacional",
        acronym: "COMOP",
        rank: "Coronel BM",
        subordinateTo: "Comandante-Geral do CBMMA",
        subordinates: "Subcomandante Operacional; Centro de Operações de Bombeiros; Grupamentos de Bombeiros; Grupamentos Especializados",
        attributions: "Planejar, coordenar e controlar as atividades operacionais do CBMMA; Propor ao Comandante-Geral políticas operacionais; Supervisionar o Centro de Operações de Bombeiros; Coordenar as ações de resposta a emergências",
        sortOrder: 1,
      },
      {
        title: "Subcomandante Operacional",
        acronym: "SCOMOP",
        rank: "Tenente-Coronel BM",
        subordinateTo: "Comandante Operacional",
        subordinates: "Centro de Operações de Bombeiros; Seção de Planejamento Operacional",
        attributions: "Auxiliar o Comandante Operacional; Substituir o Comandante em suas ausências; Coordenar as atividades do Centro de Operações de Bombeiros",
        sortOrder: 2,
      },
      {
        title: "Chefe do Centro de Operações de Bombeiros",
        acronym: "COB",
        rank: "Major BM",
        subordinateTo: "Subcomandante Operacional",
        subordinates: null,
        attributions: "Coordenar o atendimento e despacho de ocorrências; Manter o controle das viaturas e equipes em serviço; Elaborar relatórios de ocorrências; Gerenciar o sistema de comunicações operacionais",
        sortOrder: 3,
      },
    ],
    td: [
      {
        title: "Diretor de Atividades Técnicas",
        acronym: "DAT",
        rank: "Coronel BM",
        subordinateTo: "Comandante-Geral do CBMMA",
        subordinates: "Subdiretor de Atividades Técnicas; Seção de Análise de Projetos; Seção de Fiscalização; Seção de Normas e Pesquisa",
        attributions: "Planejar, dirigir e controlar as atividades de segurança contra incêndio e pânico no MA; Propor normas técnicas de prevenção; Supervisionar a análise de projetos e fiscalização de edificações; Representar o CBMMA em comissões técnicas",
        sortOrder: 1,
      },
      {
        title: "Subdiretor de Atividades Técnicas",
        acronym: "SDAT",
        rank: "Tenente-Coronel BM",
        subordinateTo: "Diretor de Atividades Técnicas",
        subordinates: "Seção de Análise de Projetos; Seção de Fiscalização",
        attributions: "Auxiliar o Diretor de Atividades Técnicas; Substituir o Diretor em suas ausências; Coordenar as atividades das seções subordinadas",
        sortOrder: 2,
      },
      {
        title: "Chefe da Seção de Análise de Projetos",
        acronym: "SAP",
        rank: "Major BM",
        subordinateTo: "Subdiretor de Atividades Técnicas",
        subordinates: null,
        attributions: "Analisar e aprovar projetos de SPCI; Emitir pareceres técnicos; Controlar o arquivo de projetos aprovados; Orientar projetistas sobre as normas técnicas aplicáveis",
        sortOrder: 3,
      },
      {
        title: "Chefe da Seção de Fiscalização",
        acronym: "SF",
        rank: "Major BM",
        subordinateTo: "Subdiretor de Atividades Técnicas",
        subordinates: null,
        attributions: "Coordenar as vistorias em edificações; Emitir laudos de vistoria; Autuar estabelecimentos irregulares; Controlar os prazos de regularização",
        sortOrder: 4,
      },
    ],
  },

  // ── MATO GROSSO ──────────────────────────────────────────────────────────────
  MT: {
    oc: [
      {
        title: "Diretor Operacional",
        acronym: "DOP",
        rank: "Coronel BM",
        subordinateTo: "Comandante-Geral do CBMMT",
        subordinates: "Subdiretor Operacional; Seção de Operações; Seção de Planejamento Operacional; Batalhões de Bombeiros",
        attributions: "Planejar, dirigir e controlar as atividades operacionais do CBMMT; Propor políticas e diretrizes operacionais; Supervisionar os Batalhões de Bombeiros; Coordenar as ações de resposta a grandes emergências",
        sortOrder: 1,
      },
      {
        title: "Subdiretor Operacional",
        acronym: "SDOP",
        rank: "Tenente-Coronel BM",
        subordinateTo: "Diretor Operacional",
        subordinates: "Seção de Operações; Seção de Planejamento Operacional",
        attributions: "Auxiliar o Diretor Operacional; Substituir o Diretor em suas ausências; Coordenar as seções subordinadas",
        sortOrder: 2,
      },
    ],
    td: [
      {
        title: "Diretor de Segurança Contra Incêndio e Pânico",
        acronym: "DSCIP",
        rank: "Coronel BM",
        subordinateTo: "Comandante-Geral do CBMMT",
        subordinates: "Subdiretor de SCIP; Seção de Análise de Projetos; Seção de Fiscalização; Seção de Normas Técnicas",
        attributions: "Planejar, dirigir e controlar as atividades de segurança contra incêndio e pânico no MT; Propor normas técnicas de prevenção; Supervisionar a análise de projetos e fiscalização; Representar o CBMMT em comissões técnicas",
        sortOrder: 1,
      },
      {
        title: "Subdiretor de Segurança Contra Incêndio e Pânico",
        acronym: "SDSCIP",
        rank: "Tenente-Coronel BM",
        subordinateTo: "Diretor de SCIP",
        subordinates: "Seção de Análise de Projetos; Seção de Fiscalização",
        attributions: "Auxiliar o Diretor de SCIP; Substituir o Diretor em suas ausências; Coordenar as atividades das seções subordinadas",
        sortOrder: 2,
      },
      {
        title: "Chefe da Seção de Análise de Projetos",
        acronym: "SAP",
        rank: "Major BM",
        subordinateTo: "Subdiretor de SCIP",
        subordinates: null,
        attributions: "Analisar e aprovar projetos de SPCI; Emitir pareceres técnicos; Controlar o arquivo de projetos aprovados",
        sortOrder: 3,
      },
    ],
  },

  // ── MATO GROSSO DO SUL ───────────────────────────────────────────────────────
  MS: {
    oc: [
      {
        title: "Comandante Operacional",
        acronym: "COMOP",
        rank: "Coronel BM",
        subordinateTo: "Comandante-Geral do CBMMS",
        subordinates: "Subcomandante Operacional; Centro de Operações de Bombeiros; Grupamentos de Bombeiros; Grupamentos Especializados",
        attributions: "Planejar, coordenar e controlar as atividades operacionais do CBMMS; Supervisionar os Grupamentos de Bombeiros; Propor políticas operacionais ao Comando-Geral; Coordenar as ações de resposta a emergências",
        sortOrder: 1,
      },
      {
        title: "Subcomandante Operacional",
        acronym: "SCOMOP",
        rank: "Tenente-Coronel BM",
        subordinateTo: "Comandante Operacional",
        subordinates: "Centro de Operações de Bombeiros; Seção de Planejamento Operacional",
        attributions: "Auxiliar o Comandante Operacional; Substituir o Comandante em suas ausências; Coordenar as atividades do Centro de Operações",
        sortOrder: 2,
      },
    ],
    td: [
      {
        title: "Diretor de Atividades Técnicas",
        acronym: "DAT",
        rank: "Coronel BM",
        subordinateTo: "Comandante-Geral do CBMMS",
        subordinates: "Subdiretor de Atividades Técnicas; Seção de Análise de Projetos; Seção de Fiscalização; Seção de Normas Técnicas",
        attributions: "Planejar, dirigir e controlar as atividades de segurança contra incêndio e pânico no MS; Propor normas técnicas; Supervisionar análise de projetos e fiscalização; Representar o CBMMS em comissões técnicas",
        sortOrder: 1,
      },
      {
        title: "Subdiretor de Atividades Técnicas",
        acronym: "SDAT",
        rank: "Tenente-Coronel BM",
        subordinateTo: "Diretor de Atividades Técnicas",
        subordinates: "Seção de Análise de Projetos; Seção de Fiscalização",
        attributions: "Auxiliar o Diretor de Atividades Técnicas; Substituir o Diretor em suas ausências; Coordenar as seções subordinadas",
        sortOrder: 2,
      },
    ],
  },

  // ── MINAS GERAIS ─────────────────────────────────────────────────────────────
  MG: {
    oc: [
      {
        title: "Comandante Operacional",
        acronym: "COMOP",
        rank: "Coronel BM",
        subordinateTo: "Comandante-Geral do CBMMG",
        subordinates: "Subcomandante Operacional; Centro de Operações de Bombeiros Militares; Batalhões de Bombeiros Militares; Grupamentos Especializados",
        attributions: "Planejar, coordenar, controlar e supervisionar as atividades operacionais do CBMMG; Propor ao Comandante-Geral políticas e diretrizes operacionais; Supervisionar o COBOM; Coordenar as ações de resposta a emergências de grande porte",
        sortOrder: 1,
      },
      {
        title: "Subcomandante Operacional",
        acronym: "SCOMOP",
        rank: "Tenente-Coronel BM",
        subordinateTo: "Comandante Operacional",
        subordinates: "Centro de Operações de Bombeiros Militares; Seção de Planejamento Operacional",
        attributions: "Auxiliar o Comandante Operacional; Substituir o Comandante em suas ausências; Supervisionar as atividades do COBOM",
        sortOrder: 2,
      },
      {
        title: "Chefe do Centro de Operações de Bombeiros Militares",
        acronym: "COBOM",
        rank: "Major BM",
        subordinateTo: "Subcomandante Operacional",
        subordinates: "Seção de Despacho; Seção de Comunicações; Seção de Estatística Operacional",
        attributions: "Coordenar o atendimento e despacho de ocorrências; Manter o controle das viaturas e equipes em serviço; Elaborar relatórios de ocorrências; Gerenciar o sistema de comunicações operacionais",
        sortOrder: 3,
      },
    ],
    td: [
      {
        title: "Diretor do Centro de Atividades Técnicas",
        acronym: "CAT",
        rank: "Coronel BM",
        subordinateTo: "Comandante-Geral do CBMMG",
        subordinates: "Subdiretor do CAT; Seção de Análise de Projetos; Seção de Fiscalização; Seção de Normas e Pesquisa; Seção de Investigação de Incêndios",
        attributions: "Planejar, dirigir e controlar as atividades de segurança contra incêndio e pânico em MG; Propor normas técnicas de prevenção; Supervisionar a análise de projetos e fiscalização; Coordenar investigações de incêndio; Representar o CBMMG em comissões técnicas",
        sortOrder: 1,
      },
      {
        title: "Subdiretor do Centro de Atividades Técnicas",
        acronym: "SCAT",
        rank: "Tenente-Coronel BM",
        subordinateTo: "Diretor do CAT",
        subordinates: "Seção de Análise de Projetos; Seção de Fiscalização; Seção de Normas e Pesquisa",
        attributions: "Auxiliar o Diretor do CAT; Substituir o Diretor em suas ausências; Coordenar as atividades das seções subordinadas",
        sortOrder: 2,
      },
      {
        title: "Chefe da Seção de Análise de Projetos",
        acronym: "SAP",
        rank: "Major BM",
        subordinateTo: "Subdiretor do CAT",
        subordinates: null,
        attributions: "Analisar e aprovar projetos de SPCI; Emitir pareceres técnicos; Controlar o arquivo de projetos aprovados; Orientar projetistas sobre as normas técnicas aplicáveis",
        sortOrder: 3,
      },
      {
        title: "Chefe da Seção de Fiscalização",
        acronym: "SF",
        rank: "Major BM",
        subordinateTo: "Subdiretor do CAT",
        subordinates: null,
        attributions: "Coordenar as vistorias em edificações; Emitir laudos de vistoria; Autuar estabelecimentos irregulares; Controlar os prazos de regularização",
        sortOrder: 4,
      },
    ],
  },

  // ── PARÁ ─────────────────────────────────────────────────────────────────────
  PA: {
    oc: [
      {
        title: "Diretor-Geral de Operações",
        acronym: "DGO",
        rank: "Coronel BM",
        subordinateTo: "Comandante-Geral do CBMPA",
        subordinates: "Subdiretor-Geral de Operações; Batalhões de Bombeiros Militares; Grupamentos de Bombeiros Militares",
        attributions: "Planejar, dirigir e controlar as atividades operacionais do CBMPA; Propor políticas e diretrizes operacionais; Supervisionar os Batalhões e Grupamentos de Bombeiros; Coordenar as ações de resposta a grandes emergências",
        sortOrder: 1,
      },
      {
        title: "Subdiretor-Geral de Operações",
        acronym: "SDGO",
        rank: "Tenente-Coronel BM",
        subordinateTo: "Diretor-Geral de Operações",
        subordinates: "Seção de Operações; Seção de Planejamento Operacional",
        attributions: "Auxiliar o Diretor-Geral de Operações; Substituir o Diretor em suas ausências; Coordenar as seções subordinadas",
        sortOrder: 2,
      },
    ],
    td: [
      {
        title: "Diretor-Geral de Segurança Contra Incêndios",
        acronym: "DGSCI",
        rank: "Coronel BM",
        subordinateTo: "Comandante-Geral do CBMPA",
        subordinates: "Subdiretor-Geral de SCI; Seção de Análise de Projetos; Seção de Fiscalização; Seção de Normas e Pesquisa; Seção de Investigação de Incêndios",
        attributions: "Planejar, dirigir e controlar as atividades de segurança contra incêndio e pânico no PA; Propor normas técnicas de prevenção; Supervisionar a análise de projetos e fiscalização; Coordenar investigações de incêndio",
        sortOrder: 1,
      },
      {
        title: "Subdiretor-Geral de Segurança Contra Incêndios",
        acronym: "SDGSCI",
        rank: "Tenente-Coronel BM",
        subordinateTo: "Diretor-Geral de SCI",
        subordinates: "Seção de Análise de Projetos; Seção de Fiscalização",
        attributions: "Auxiliar o Diretor-Geral de SCI; Substituir o Diretor em suas ausências; Coordenar as atividades das seções subordinadas",
        sortOrder: 2,
      },
      {
        title: "Chefe da Seção de Análise de Projetos",
        acronym: "SAP",
        rank: "Major BM",
        subordinateTo: "Subdiretor-Geral de SCI",
        subordinates: null,
        attributions: "Analisar e aprovar projetos de SPCI; Emitir pareceres técnicos; Controlar o arquivo de projetos aprovados",
        sortOrder: 3,
      },
    ],
  },

  // ── PARAÍBA ──────────────────────────────────────────────────────────────────
  PB: {
    oc: [
      {
        title: "Diretor de Atividades Operacionais",
        acronym: "DAO",
        rank: "Coronel BM",
        subordinateTo: "Comandante-Geral do CBMPB",
        subordinates: "Subdiretor de Atividades Operacionais; Seção de Operações; Seção de Planejamento Operacional; Comandos Regionais de Bombeiros",
        attributions: "Planejar, dirigir e controlar as atividades operacionais do CBMPB; Propor políticas operacionais; Supervisionar os Comandos Regionais; Coordenar as ações de resposta a emergências",
        sortOrder: 1,
      },
      {
        title: "Subdiretor de Atividades Operacionais",
        acronym: "SDAO",
        rank: "Tenente-Coronel BM",
        subordinateTo: "Diretor de Atividades Operacionais",
        subordinates: "Seção de Operações; Seção de Planejamento Operacional",
        attributions: "Auxiliar o Diretor de Atividades Operacionais; Substituir o Diretor em suas ausências; Coordenar as seções subordinadas",
        sortOrder: 2,
      },
    ],
    td: [
      {
        title: "Diretor de Atividades Técnicas",
        acronym: "DAT",
        rank: "Coronel BM",
        subordinateTo: "Comandante-Geral do CBMPB",
        subordinates: "Subdiretor de Atividades Técnicas; Seção de Análise de Projetos; Seção de Fiscalização; Seção de Normas Técnicas",
        attributions: "Planejar, dirigir e controlar as atividades de segurança contra incêndio e pânico na PB; Propor normas técnicas; Supervisionar análise de projetos e fiscalização; Representar o CBMPB em comissões técnicas",
        sortOrder: 1,
      },
      {
        title: "Subdiretor de Atividades Técnicas",
        acronym: "SDAT",
        rank: "Tenente-Coronel BM",
        subordinateTo: "Diretor de Atividades Técnicas",
        subordinates: "Seção de Análise de Projetos; Seção de Fiscalização",
        attributions: "Auxiliar o Diretor de Atividades Técnicas; Substituir o Diretor em suas ausências; Coordenar as seções subordinadas",
        sortOrder: 2,
      },
    ],
  },

  // ── PARANÁ ───────────────────────────────────────────────────────────────────
  PR: {
    oc: [
      {
        title: "Diretor de Operações",
        acronym: "DO",
        rank: "Coronel BM",
        subordinateTo: "Comandante-Geral do CBMPR",
        subordinates: "Subdiretor de Operações; Seção de Operações; Seção de Planejamento Operacional; Comandos Regionais de Bombeiros",
        attributions: "Planejar, dirigir e controlar as atividades operacionais do CBMPR; Propor políticas e diretrizes operacionais; Supervisionar os Comandos Regionais; Coordenar as ações de resposta a grandes emergências",
        sortOrder: 1,
      },
      {
        title: "Subdiretor de Operações",
        acronym: "SDO",
        rank: "Tenente-Coronel BM",
        subordinateTo: "Diretor de Operações",
        subordinates: "Seção de Operações; Seção de Planejamento Operacional",
        attributions: "Auxiliar o Diretor de Operações; Substituir o Diretor em suas ausências; Coordenar as seções subordinadas",
        sortOrder: 2,
      },
      {
        title: "Chefe da Seção de Operações",
        acronym: "S/OP",
        rank: "Major BM",
        subordinateTo: "Subdiretor de Operações",
        subordinates: null,
        attributions: "Controlar e registrar as ocorrências operacionais; Elaborar escalas de serviço; Coordenar o Centro de Operações de Bombeiros; Manter atualizado o banco de dados operacionais",
        sortOrder: 3,
      },
    ],
    td: [
      {
        title: "Diretor de Atividades Técnicas",
        acronym: "DAT",
        rank: "Coronel BM",
        subordinateTo: "Comandante-Geral do CBMPR",
        subordinates: "Subdiretor de Atividades Técnicas; Seção de Análise de Projetos; Seção de Fiscalização; Seção de Normas e Pesquisa; Seção de Investigação de Incêndios",
        attributions: "Planejar, dirigir e controlar as atividades de segurança contra incêndio e pânico no PR; Propor normas técnicas; Supervisionar análise de projetos e fiscalização; Coordenar investigações de incêndio; Representar o CBMPR em comissões técnicas",
        sortOrder: 1,
      },
      {
        title: "Subdiretor de Atividades Técnicas",
        acronym: "SDAT",
        rank: "Tenente-Coronel BM",
        subordinateTo: "Diretor de Atividades Técnicas",
        subordinates: "Seção de Análise de Projetos; Seção de Fiscalização; Seção de Normas e Pesquisa",
        attributions: "Auxiliar o Diretor de Atividades Técnicas; Substituir o Diretor em suas ausências; Coordenar as atividades das seções subordinadas",
        sortOrder: 2,
      },
      {
        title: "Chefe da Seção de Análise de Projetos",
        acronym: "SAP",
        rank: "Major BM",
        subordinateTo: "Subdiretor de Atividades Técnicas",
        subordinates: null,
        attributions: "Analisar e aprovar projetos de SPCI; Emitir pareceres técnicos; Controlar o arquivo de projetos aprovados; Orientar projetistas sobre as normas técnicas aplicáveis",
        sortOrder: 3,
      },
    ],
  },

  // ── PERNAMBUCO ───────────────────────────────────────────────────────────────
  PE: {
    oc: [
      {
        title: "Diretor de Operações",
        acronym: "DO",
        rank: "Coronel BM",
        subordinateTo: "Comandante-Geral do CBMPE",
        subordinates: "Subdiretor de Operações; Seção de Operações; Seção de Planejamento; Batalhões de Bombeiros",
        attributions: "Planejar, dirigir e controlar as atividades operacionais do CBMPE; Propor políticas operacionais; Supervisionar os Batalhões de Bombeiros; Coordenar as ações de resposta a emergências",
        sortOrder: 1,
      },
      {
        title: "Subdiretor de Operações",
        acronym: "SDO",
        rank: "Tenente-Coronel BM",
        subordinateTo: "Diretor de Operações",
        subordinates: "Seção de Operações; Seção de Planejamento",
        attributions: "Auxiliar o Diretor de Operações; Substituir o Diretor em suas ausências; Coordenar as seções subordinadas",
        sortOrder: 2,
      },
    ],
    td: [
      {
        title: "Diretor de Atividades Técnicas",
        acronym: "DAT",
        rank: "Coronel BM",
        subordinateTo: "Comandante-Geral do CBMPE",
        subordinates: "Subdiretor de Atividades Técnicas; Seção de Análise de Projetos; Seção de Fiscalização",
        attributions: "Planejar, dirigir e controlar as atividades de segurança contra incêndio e pânico em PE; Propor normas técnicas; Supervisionar análise de projetos e fiscalização",
        sortOrder: 1,
      },
      {
        title: "Subdiretor de Atividades Técnicas",
        acronym: "SDAT",
        rank: "Tenente-Coronel BM",
        subordinateTo: "Diretor de Atividades Técnicas",
        subordinates: "Seção de Análise de Projetos; Seção de Fiscalização",
        attributions: "Auxiliar o Diretor de Atividades Técnicas; Substituir o Diretor em suas ausências; Coordenar as seções subordinadas",
        sortOrder: 2,
      },
    ],
  },

  // ── PIAUÍ ────────────────────────────────────────────────────────────────────
  PI: {
    oc: [
      {
        title: "Comandante Operacional",
        acronym: "COMOP",
        rank: "Coronel BM",
        subordinateTo: "Comandante-Geral do CBMPI",
        subordinates: "Subcomandante Operacional; Centro de Operações de Bombeiros; Grupamentos de Bombeiros; Grupamentos Especializados",
        attributions: "Planejar, coordenar e controlar as atividades operacionais do CBMPI; Supervisionar os Grupamentos de Bombeiros; Propor políticas operacionais ao Comando-Geral; Coordenar as ações de resposta a emergências",
        sortOrder: 1,
      },
      {
        title: "Subcomandante Operacional",
        acronym: "SCOMOP",
        rank: "Tenente-Coronel BM",
        subordinateTo: "Comandante Operacional",
        subordinates: "Centro de Operações de Bombeiros; Seção de Planejamento Operacional",
        attributions: "Auxiliar o Comandante Operacional; Substituir o Comandante em suas ausências; Coordenar as atividades do Centro de Operações",
        sortOrder: 2,
      },
    ],
    td: [
      {
        title: "Diretor de Segurança Contra Incêndio e Pânico",
        acronym: "DSCIP",
        rank: "Coronel BM",
        subordinateTo: "Comandante-Geral do CBMPI",
        subordinates: "Subdiretor de SCIP; Seção de Análise de Projetos; Seção de Fiscalização; Seção de Normas Técnicas",
        attributions: "Planejar, dirigir e controlar as atividades de segurança contra incêndio e pânico no PI; Propor normas técnicas; Supervisionar análise de projetos e fiscalização; Representar o CBMPI em comissões técnicas",
        sortOrder: 1,
      },
      {
        title: "Subdiretor de Segurança Contra Incêndio e Pânico",
        acronym: "SDSCIP",
        rank: "Tenente-Coronel BM",
        subordinateTo: "Diretor de SCIP",
        subordinates: "Seção de Análise de Projetos; Seção de Fiscalização",
        attributions: "Auxiliar o Diretor de SCIP; Substituir o Diretor em suas ausências; Coordenar as seções subordinadas",
        sortOrder: 2,
      },
    ],
  },

  // ── RIO DE JANEIRO ───────────────────────────────────────────────────────────
  RJ: {
    oc: [
      {
        title: "Diretor de Operações",
        acronym: "DO",
        rank: "Coronel BM",
        subordinateTo: "Comandante-Geral do CBMERJ",
        subordinates: "Subdiretor de Operações; Centro de Operações de Bombeiros; Batalhões de Bombeiros; Grupamentos Especializados",
        attributions: "Planejar, dirigir e controlar as atividades operacionais do CBMERJ; Propor políticas e diretrizes operacionais; Supervisionar o Centro de Operações de Bombeiros; Coordenar as ações de resposta a grandes emergências",
        sortOrder: 1,
      },
      {
        title: "Subdiretor de Operações",
        acronym: "SDO",
        rank: "Tenente-Coronel BM",
        subordinateTo: "Diretor de Operações",
        subordinates: "Centro de Operações de Bombeiros; Seção de Planejamento Operacional",
        attributions: "Auxiliar o Diretor de Operações; Substituir o Diretor em suas ausências; Supervisionar as atividades do Centro de Operações",
        sortOrder: 2,
      },
    ],
    td: [
      {
        title: "Diretor de Serviços Técnicos",
        acronym: "DST",
        rank: "Coronel BM",
        subordinateTo: "Comandante-Geral do CBMERJ",
        subordinates: "Subdiretor de Serviços Técnicos; Seção de Análise de Projetos; Seção de Fiscalização; Seção de Normas e Pesquisa; Seção de Investigação de Incêndios",
        attributions: "Planejar, dirigir e controlar as atividades de segurança contra incêndio e pânico no RJ; Propor normas técnicas de prevenção; Supervisionar análise de projetos e fiscalização; Coordenar investigações de incêndio; Representar o CBMERJ em comissões técnicas",
        sortOrder: 1,
      },
      {
        title: "Subdiretor de Serviços Técnicos",
        acronym: "SDST",
        rank: "Tenente-Coronel BM",
        subordinateTo: "Diretor de Serviços Técnicos",
        subordinates: "Seção de Análise de Projetos; Seção de Fiscalização; Seção de Normas e Pesquisa",
        attributions: "Auxiliar o Diretor de Serviços Técnicos; Substituir o Diretor em suas ausências; Coordenar as atividades das seções subordinadas",
        sortOrder: 2,
      },
      {
        title: "Chefe da Seção de Análise de Projetos",
        acronym: "SAP",
        rank: "Major BM",
        subordinateTo: "Subdiretor de Serviços Técnicos",
        subordinates: null,
        attributions: "Analisar e aprovar projetos de SPCI; Emitir pareceres técnicos; Controlar o arquivo de projetos aprovados; Orientar projetistas sobre as normas técnicas aplicáveis",
        sortOrder: 3,
      },
    ],
  },

  // ── RIO GRANDE DO SUL ────────────────────────────────────────────────────────
  RS: {
    oc: [
      {
        title: "Diretor de Operações",
        acronym: "DO",
        rank: "Coronel BM",
        subordinateTo: "Comandante-Geral do CBMRS",
        subordinates: "Subdiretor de Operações; Seção de Operações; Seção de Planejamento Operacional; Batalhões de Bombeiros; Grupamentos Especializados",
        attributions: "Planejar, dirigir e controlar as atividades operacionais do CBMRS; Propor políticas e diretrizes operacionais; Supervisionar os Batalhões de Bombeiros; Coordenar as ações de resposta a grandes emergências",
        sortOrder: 1,
      },
      {
        title: "Subdiretor de Operações",
        acronym: "SDO",
        rank: "Tenente-Coronel BM",
        subordinateTo: "Diretor de Operações",
        subordinates: "Seção de Operações; Seção de Planejamento Operacional",
        attributions: "Auxiliar o Diretor de Operações; Substituir o Diretor em suas ausências; Coordenar as seções subordinadas",
        sortOrder: 2,
      },
    ],
    td: [
      {
        title: "Diretor de Atividades Técnicas",
        acronym: "DAT",
        rank: "Coronel BM",
        subordinateTo: "Comandante-Geral do CBMRS",
        subordinates: "Subdiretor de Atividades Técnicas; Seção de Análise de Projetos; Seção de Fiscalização; Seção de Normas e Pesquisa",
        attributions: "Planejar, dirigir e controlar as atividades de segurança contra incêndio e pânico no RS; Propor normas técnicas; Supervisionar análise de projetos e fiscalização; Representar o CBMRS em comissões técnicas",
        sortOrder: 1,
      },
      {
        title: "Subdiretor de Atividades Técnicas",
        acronym: "SDAT",
        rank: "Tenente-Coronel BM",
        subordinateTo: "Diretor de Atividades Técnicas",
        subordinates: "Seção de Análise de Projetos; Seção de Fiscalização",
        attributions: "Auxiliar o Diretor de Atividades Técnicas; Substituir o Diretor em suas ausências; Coordenar as seções subordinadas",
        sortOrder: 2,
      },
    ],
  },

  // ── RONDÔNIA ─────────────────────────────────────────────────────────────────
  RO: {
    oc: [
      {
        title: "Diretor de Planejamento Operacional",
        acronym: "DPO",
        rank: "Coronel BM",
        subordinateTo: "Comandante-Geral do CBMRO",
        subordinates: "Subdiretor de Planejamento Operacional; Seção de Planejamento; Seção de Operações; Seção de Instrução Operacional",
        attributions: "Planejar, coordenar e controlar as atividades de planejamento operacional do CBMRO; Elaborar e revisar os planos operacionais; Propor políticas e diretrizes operacionais ao Comando-Geral; Supervisionar a instrução operacional",
        sortOrder: 1,
      },
      {
        title: "Subdiretor de Planejamento Operacional",
        acronym: "SDPO",
        rank: "Tenente-Coronel BM",
        subordinateTo: "Diretor de Planejamento Operacional",
        subordinates: "Seção de Planejamento; Seção de Operações; Seção de Instrução Operacional",
        attributions: "Auxiliar o Diretor de Planejamento Operacional; Substituir o Diretor em suas ausências; Coordenar as seções subordinadas; Supervisionar a elaboração dos planos operacionais",
        sortOrder: 2,
      },
      {
        title: "Diretor Operacional Especializado",
        acronym: "DOE",
        rank: "Coronel BM",
        subordinateTo: "Comandante-Geral do CBMRO",
        subordinates: "Subdiretor Operacional Especializado; Grupamentos Especializados (GMAR, GRAS, GRAU, GCAP)",
        attributions: "Planejar, coordenar e controlar as atividades operacionais especializadas do CBMRO; Supervisionar os Grupamentos Especializados; Propor políticas para as atividades especializadas; Coordenar as ações de resposta a emergências especializadas",
        sortOrder: 3,
      },
      {
        title: "Subdiretor Operacional Especializado",
        acronym: "SDOE",
        rank: "Tenente-Coronel BM",
        subordinateTo: "Diretor Operacional Especializado",
        subordinates: "Grupamentos Especializados",
        attributions: "Auxiliar o Diretor Operacional Especializado; Substituir o Diretor em suas ausências; Coordenar as atividades dos Grupamentos Especializados",
        sortOrder: 4,
      },
      {
        title: "Comandante do Grupamento de Mergulho e Aquático de Rondônia",
        acronym: "GMAR",
        rank: "Major BM / Capitão BM",
        subordinateTo: "Diretor Operacional Especializado",
        subordinates: "Seção de Mergulho; Seção de Operações Aquáticas",
        attributions: "Comandar e administrar o GMAR; Garantir a prontidão operacional para operações aquáticas e de mergulho; Supervisionar o treinamento especializado; Coordenar as operações de busca e salvamento aquático",
        sortOrder: 5,
      },
    ],
    td: [
      {
        title: "Comandante de Operações Técnicas",
        acronym: "COT",
        rank: "Coronel BM",
        subordinateTo: "Comandante-Geral do CBMRO",
        subordinates: "Subcomandante de Operações Técnicas; Coordenadorias de Atividades Técnicas (CAT); Seção de Normas e Pesquisa; Seção de Investigação de Incêndios",
        attributions: "Planejar, coordenar e controlar as atividades de segurança contra incêndio e pânico em RO; Propor normas técnicas de prevenção; Supervisionar as Coordenadorias de Atividades Técnicas; Coordenar investigações de incêndio; Representar o CBMRO em comissões técnicas e normativas",
        sortOrder: 1,
      },
      {
        title: "Subcomandante de Operações Técnicas",
        acronym: "SCOT",
        rank: "Tenente-Coronel BM",
        subordinateTo: "Comandante de Operações Técnicas",
        subordinates: "Coordenadorias de Atividades Técnicas; Seção de Normas e Pesquisa",
        attributions: "Auxiliar o Comandante de Operações Técnicas; Substituir o Comandante em suas ausências; Coordenar as atividades das Coordenadorias de Atividades Técnicas",
        sortOrder: 2,
      },
      {
        title: "Coordenador de Atividades Técnicas",
        acronym: "CAT",
        rank: "Major BM",
        subordinateTo: "Subcomandante de Operações Técnicas",
        subordinates: "Seção de Análise de Projetos; Seção de Fiscalização e Vistoria",
        attributions: "Coordenar as atividades de análise de projetos e fiscalização de edificações na área de atuação; Emitir pareceres técnicos; Supervisionar as vistorias em edificações; Controlar os prazos de regularização",
        sortOrder: 3,
      },
      {
        title: "Chefe da Seção de Análise de Projetos",
        acronym: "SAP",
        rank: "Capitão BM",
        subordinateTo: "Coordenador de Atividades Técnicas",
        subordinates: null,
        attributions: "Analisar e aprovar projetos de SPCI; Emitir pareceres técnicos; Controlar o arquivo de projetos aprovados; Orientar projetistas sobre as normas técnicas aplicáveis",
        sortOrder: 4,
      },
      {
        title: "Chefe da Seção de Fiscalização e Vistoria",
        acronym: "SFV",
        rank: "Capitão BM",
        subordinateTo: "Coordenador de Atividades Técnicas",
        subordinates: null,
        attributions: "Coordenar as vistorias em edificações e áreas de risco; Emitir laudos e certificados de vistoria; Autuar estabelecimentos irregulares; Controlar os prazos de regularização",
        sortOrder: 5,
      },
      {
        title: "Chefe da Seção de Normas e Pesquisa",
        acronym: "SNP",
        rank: "Major BM",
        subordinateTo: "Subcomandante de Operações Técnicas",
        subordinates: null,
        attributions: "Elaborar e revisar normas técnicas de prevenção contra incêndio; Realizar pesquisas sobre novas tecnologias de SPCI; Representar o CBMRO em comissões de normatização; Manter atualizado o acervo técnico-normativo",
        sortOrder: 6,
      },
    ],
  },

  // ── SANTA CATARINA ───────────────────────────────────────────────────────────
  SC: {
    oc: [
      {
        title: "Diretor de Operações",
        acronym: "DO",
        rank: "Coronel BM",
        subordinateTo: "Comandante-Geral do CBMSC",
        subordinates: "Subdiretor de Operações; Seção de Operações; Seção de Planejamento Operacional; Batalhões de Bombeiros; Grupamentos Especializados",
        attributions: "Planejar, dirigir e controlar as atividades operacionais do CBMSC; Propor políticas e diretrizes operacionais; Supervisionar os Batalhões de Bombeiros; Coordenar as ações de resposta a grandes emergências",
        sortOrder: 1,
      },
      {
        title: "Subdiretor de Operações",
        acronym: "SDO",
        rank: "Tenente-Coronel BM",
        subordinateTo: "Diretor de Operações",
        subordinates: "Seção de Operações; Seção de Planejamento Operacional",
        attributions: "Auxiliar o Diretor de Operações; Substituir o Diretor em suas ausências; Coordenar as seções subordinadas",
        sortOrder: 2,
      },
    ],
    td: [
      {
        title: "Diretor de Segurança Contra Incêndio e Pânico",
        acronym: "DSCIP",
        rank: "Coronel BM",
        subordinateTo: "Comandante-Geral do CBMSC",
        subordinates: "Subdiretor de SCIP; Seção de Análise de Projetos; Seção de Fiscalização; Seção de Normas e Pesquisa; Seção de Investigação de Incêndios",
        attributions: "Planejar, dirigir e controlar as atividades de segurança contra incêndio e pânico em SC; Propor normas técnicas de prevenção; Supervisionar análise de projetos e fiscalização; Coordenar investigações de incêndio; Representar o CBMSC em comissões técnicas",
        sortOrder: 1,
      },
      {
        title: "Subdiretor de Segurança Contra Incêndio e Pânico",
        acronym: "SDSCIP",
        rank: "Tenente-Coronel BM",
        subordinateTo: "Diretor de SCIP",
        subordinates: "Seção de Análise de Projetos; Seção de Fiscalização; Seção de Normas e Pesquisa",
        attributions: "Auxiliar o Diretor de SCIP; Substituir o Diretor em suas ausências; Coordenar as atividades das seções subordinadas",
        sortOrder: 2,
      },
      {
        title: "Chefe da Seção de Análise de Projetos",
        acronym: "SAP",
        rank: "Major BM",
        subordinateTo: "Subdiretor de SCIP",
        subordinates: null,
        attributions: "Analisar e aprovar projetos de SPCI; Emitir pareceres técnicos; Controlar o arquivo de projetos aprovados; Orientar projetistas sobre as normas técnicas aplicáveis",
        sortOrder: 3,
      },
    ],
  },

  // ── SERGIPE ──────────────────────────────────────────────────────────────────
  SE: {
    oc: [
      {
        title: "Diretor Operacional",
        acronym: "DOP",
        rank: "Coronel BM",
        subordinateTo: "Comandante-Geral do CBMSE",
        subordinates: "Subdiretor Operacional; Seção de Operações; Seção de Planejamento Operacional; Grupamentos de Bombeiros",
        attributions: "Planejar, dirigir e controlar as atividades operacionais do CBMSE; Propor políticas e diretrizes operacionais; Supervisionar os Grupamentos de Bombeiros; Coordenar as ações de resposta a emergências",
        sortOrder: 1,
      },
      {
        title: "Subdiretor Operacional",
        acronym: "SDOP",
        rank: "Tenente-Coronel BM",
        subordinateTo: "Diretor Operacional",
        subordinates: "Seção de Operações; Seção de Planejamento Operacional",
        attributions: "Auxiliar o Diretor Operacional; Substituir o Diretor em suas ausências; Coordenar as seções subordinadas",
        sortOrder: 2,
      },
    ],
    td: [
      {
        title: "Diretor de Atividades Técnicas",
        acronym: "DAT",
        rank: "Coronel BM",
        subordinateTo: "Comandante-Geral do CBMSE",
        subordinates: "Subdiretor de Atividades Técnicas; Seção de Análise de Projetos; Seção de Fiscalização; Seção de Normas Técnicas",
        attributions: "Planejar, dirigir e controlar as atividades de segurança contra incêndio e pânico em SE; Propor normas técnicas; Supervisionar análise de projetos e fiscalização; Representar o CBMSE em comissões técnicas",
        sortOrder: 1,
      },
      {
        title: "Subdiretor de Atividades Técnicas",
        acronym: "SDAT",
        rank: "Tenente-Coronel BM",
        subordinateTo: "Diretor de Atividades Técnicas",
        subordinates: "Seção de Análise de Projetos; Seção de Fiscalização",
        attributions: "Auxiliar o Diretor de Atividades Técnicas; Substituir o Diretor em suas ausências; Coordenar as seções subordinadas",
        sortOrder: 2,
      },
    ],
  },

  // ── TOCANTINS ────────────────────────────────────────────────────────────────
  TO: {
    oc: [
      {
        title: "Comandante Operacional",
        acronym: "COMOP",
        rank: "Coronel BM",
        subordinateTo: "Comandante-Geral do CBMTO",
        subordinates: "Subcomandante Operacional; Centro de Operações de Bombeiros; Grupamentos de Bombeiros; Grupamentos Especializados",
        attributions: "Planejar, coordenar e controlar as atividades operacionais do CBMTO; Supervisionar os Grupamentos de Bombeiros; Propor políticas operacionais ao Comando-Geral; Coordenar as ações de resposta a emergências",
        sortOrder: 1,
      },
      {
        title: "Subcomandante Operacional",
        acronym: "SCOMOP",
        rank: "Tenente-Coronel BM",
        subordinateTo: "Comandante Operacional",
        subordinates: "Centro de Operações de Bombeiros; Seção de Planejamento Operacional",
        attributions: "Auxiliar o Comandante Operacional; Substituir o Comandante em suas ausências; Coordenar as atividades do Centro de Operações",
        sortOrder: 2,
      },
    ],
    td: [
      {
        title: "Comandante de Atividades Técnicas",
        acronym: "CAT",
        rank: "Coronel BM",
        subordinateTo: "Comandante-Geral do CBMTO",
        subordinates: "Subcomandante de Atividades Técnicas; Seção de Análise de Projetos; Seção de Fiscalização; Seção de Normas Técnicas",
        attributions: "Planejar, coordenar e controlar as atividades de segurança contra incêndio e pânico no TO; Propor normas técnicas; Supervisionar análise de projetos e fiscalização; Representar o CBMTO em comissões técnicas",
        sortOrder: 1,
      },
      {
        title: "Subcomandante de Atividades Técnicas",
        acronym: "SCAT",
        rank: "Tenente-Coronel BM",
        subordinateTo: "Comandante de Atividades Técnicas",
        subordinates: "Seção de Análise de Projetos; Seção de Fiscalização",
        attributions: "Auxiliar o Comandante de Atividades Técnicas; Substituir o Comandante em suas ausências; Coordenar as seções subordinadas",
        sortOrder: 2,
      },
    ],
  },
};

async function main() {
  const conn = await mysql.createConnection(process.env.DATABASE_URL);

  let totalInserted = 0;

  for (const [sigla, data] of Object.entries(POSITIONS_DATA)) {
    const ids = IDS[sigla];
    if (!ids) {
      console.warn(`Skipping ${sigla}: no IDs found`);
      continue;
    }

    // Insert operational command positions
    for (const pos of data.oc) {
      await conn.execute(
        `INSERT INTO positions (operationalCommandId, technicalDirectorateId, title, acronym, \`rank\`, subordinateTo, subordinates, attributions, sortOrder)
         VALUES (?, NULL, ?, ?, ?, ?, ?, ?, ?)`,
        [ids.oc, pos.title, pos.acronym ?? null, pos.rank ?? null, pos.subordinateTo ?? null, pos.subordinates ?? null, pos.attributions ?? null, pos.sortOrder ?? 0]
      );
      totalInserted++;
    }

    // Insert technical directorate positions
    for (const pos of data.td) {
      await conn.execute(
        `INSERT INTO positions (operationalCommandId, technicalDirectorateId, title, acronym, \`rank\`, subordinateTo, subordinates, attributions, sortOrder)
         VALUES (NULL, ?, ?, ?, ?, ?, ?, ?, ?)`,
        [ids.td, pos.title, pos.acronym ?? null, pos.rank ?? null, pos.subordinateTo ?? null, pos.subordinates ?? null, pos.attributions ?? null, pos.sortOrder ?? 0]
      );
      totalInserted++;
    }

    console.log(`✓ ${sigla}: ${data.oc.length} cargos OC + ${data.td.length} cargos DAT inseridos`);
  }

  console.log(`\nTotal: ${totalInserted} cargos/funções inseridos`);
  await conn.end();
}

main().catch(console.error);
