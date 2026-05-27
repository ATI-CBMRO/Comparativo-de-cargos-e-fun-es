/**
 * SEED DE CARGOS E FUNÇÕES - v2
 * Dados 100% fiéis às legislações originais de cada estado.
 * Reescrito após revisão detalhada dos documentos fonte.
 *
 * Mapeamento de IDs (confirmado via banco):
 * AL=1, CE=2, DF=3, ES=4, MA=5, MT=6, MS=7, MG=8, PA=9, PB=10, PR=11, PE=12, PI=13, RJ=14, RS=15, RO=16, SC=17, SE=18, TO=19
 * operational_commands: id = stateId (1:1)
 * technical_directorates: id = stateId (1:1)
 *
 * Colunas da tabela positions:
 * id, operationalCommandId, technicalDirectorateId, title, acronym, rank, subordinateTo, subordinates, attributions, sortOrder
 */
import mysql from "mysql2/promise";
import dotenv from "dotenv";
dotenv.config();

const DB_URL = process.env.DATABASE_URL;
if (!DB_URL) throw new Error("DATABASE_URL não definida");

const conn = await mysql.createConnection(DB_URL);

// Limpar tabela existente
await conn.execute("DELETE FROM positions");
console.log("Tabela positions limpa.");

// IDs confirmados
const IDS = {
  AL: { state: 1, cop: 1, dat: 1 },
  CE: { state: 2, cop: 2, dat: 2 },
  DF: { state: 3, cop: 3, dat: 3 },
  ES: { state: 4, cop: 4, dat: 4 },
  MA: { state: 5, cop: 5, dat: 5 },
  MT: { state: 6, cop: 6, dat: 6 },
  MS: { state: 7, cop: 7, dat: 7 },
  MG: { state: 8, cop: 8, dat: 8 },
  PA: { state: 9, cop: 9, dat: 9 },
  PB: { state: 10, cop: 10, dat: 10 },
  PR: { state: 11, cop: 11, dat: 11 },
  PI: { state: 13, cop: 13, dat: 13 },
  RO: { state: 16, cop: 16, dat: 16 },
  SE: { state: 18, cop: 18, dat: 18 },
  TO: { state: 19, cop: 19, dat: 19 },
};

// Helper para inserir cargo
async function insert(p) {
  await conn.execute(
    "INSERT INTO positions (operationalCommandId, technicalDirectorateId, title, acronym, `rank`, subordinateTo, subordinates, attributions, sortOrder) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
    [
      p.copId ?? null,
      p.datId ?? null,
      p.title,
      p.acronym ?? null,
      p.rank ?? null,
      p.subordinateTo ?? null,
      p.subordinates ?? null,
      p.attributions ?? null,
      p.order ?? 1,
    ]
  );
}

// ============================================================
// ALAGOAS - CBMAL
// Fonte: Regimento Interno do CBMAL
// ============================================================
const AL = IDS.AL;

// COB - Comando Operacional de Bombeiros
await insert({ copId: AL.cop, title: "Comandante Operacional de Bombeiros", acronym: "Cmt COB", rank: "Coronel", subordinateTo: "Comandante-Geral", subordinates: "Subcomandante Operacional de Bombeiros; Seção de Planejamento e Controle; Seção de Comunicações; Centro de Operações e Comunicações (CEOCOM); Batalhões e Companhias Independentes", attributions: "Planejar, coordenar, supervisionar, controlar e fiscalizar as atividades operacionais dos órgãos de execução subordinados; assessorar o Comandante-Geral nos assuntos operacionais; expedir ordens de operações e normas de serviço operacional.", order: 1 });
await insert({ copId: AL.cop, title: "Subcomandante Operacional de Bombeiros", acronym: "Sub Cmt COB", rank: "Tenente-Coronel", subordinateTo: "Comandante Operacional de Bombeiros", subordinates: "Seção de Planejamento e Controle; Seção de Comunicações; CEOCOM", attributions: "Substituir o Comandante Operacional em seus impedimentos; auxiliar no planejamento e controle das atividades operacionais; supervisionar as seções subordinadas.", order: 2 });
await insert({ copId: AL.cop, title: "Chefe do Centro de Operações e Comunicações", acronym: "Chefe CEOCOM", rank: "Major ou Capitão", subordinateTo: "Comandante Operacional de Bombeiros", subordinates: "Seção de Operações; Seção de Comunicações", attributions: "Planejar, coordenar e controlar as atividades do CEOCOM; gerenciar as comunicações operacionais; coordenar o despacho de viaturas e atendimento de ocorrências.", order: 3 });

// DST - Diretoria de Serviços Técnicos
await insert({ datId: AL.dat, title: "Diretor de Serviços Técnicos", acronym: "Dir DST", rank: "Coronel ou Tenente-Coronel", subordinateTo: "Comandante-Geral", subordinates: "Seção de Análise de Projetos; Seção de Vistorias e Fiscalização; Seção de Perícias", attributions: "Planejar, coordenar, supervisionar e controlar as atividades de prevenção e segurança contra incêndio e pânico; analisar projetos de segurança contra incêndio; realizar vistorias e emitir pareceres técnicos; fiscalizar o cumprimento das normas de segurança.", order: 1 });
await insert({ datId: AL.dat, title: "Chefe da Seção de Análise de Projetos", acronym: "Chefe SAP", rank: "Oficial Superior ou Intermediário", subordinateTo: "Diretor de Serviços Técnicos", subordinates: "Analistas de projetos", attributions: "Analisar e aprovar projetos de segurança contra incêndio e pânico; emitir laudos técnicos sobre projetos; orientar os profissionais sobre as normas aplicáveis.", order: 2 });
await insert({ datId: AL.dat, title: "Chefe da Seção de Vistorias e Fiscalização", acronym: "Chefe SVF", rank: "Oficial Superior ou Intermediário", subordinateTo: "Diretor de Serviços Técnicos", subordinates: "Fiscais e vistoriadores", attributions: "Realizar vistorias em edificações e áreas de risco; fiscalizar o cumprimento das normas de segurança contra incêndio; notificar, embargar e interditar estabelecimentos em desconformidade.", order: 3 });

// ============================================================
// CEARÁ - CBMCE
// Fonte: Lei de Organização Básica do CBMCE
// ============================================================
const CE = IDS.CE;

await insert({ copId: CE.cop, title: "Coordenador Operacional", acronym: "Coord COROP", rank: "Coronel", subordinateTo: "Comandante-Geral", subordinates: "Seção de Planejamento Operacional; Seção de Comunicações; Batalhões e Companhias Independentes", attributions: "Planejar, coordenar, supervisionar e controlar as atividades operacionais; assessorar o Comandante-Geral nos assuntos de emprego operacional; elaborar planos e ordens de operações.", order: 1 });

await insert({ datId: CE.dat, title: "Coordenador de Atividades Técnicas", acronym: "Coord CAT", rank: "Coronel ou Tenente-Coronel", subordinateTo: "Comandante-Geral", subordinates: "Seção de Análise de Projetos; Seção de Vistorias; Seção de Fiscalização; Seção de Perícias", attributions: "Planejar, coordenar e controlar as atividades de prevenção e segurança contra incêndio e pânico; analisar projetos técnicos; realizar vistorias e emitir pareceres; fiscalizar o cumprimento das normas técnicas.", order: 1 });

// ============================================================
// DISTRITO FEDERAL - CBMDF
// Fonte: Regimento Interno do CBMDF
// ============================================================
const DF = IDS.DF;

await insert({ copId: DF.cop, title: "Comandante Operacional", acronym: "Cmt COMOP", rank: "Coronel", subordinateTo: "Comandante-Geral", subordinates: "Subcomandante Operacional; Seção de Planejamento; Seção de Operações; Grupamentos de Bombeiros Militares", attributions: "Planejar, coordenar, supervisionar e controlar as atividades operacionais do CBMDF; assessorar o Comandante-Geral nos assuntos operacionais; expedir normas operacionais; coordenar o emprego dos Grupamentos de Bombeiros.", order: 1 });
await insert({ copId: DF.cop, title: "Subcomandante Operacional", acronym: "Sub Cmt COMOP", rank: "Tenente-Coronel", subordinateTo: "Comandante Operacional", subordinates: "Seção de Planejamento; Seção de Operações", attributions: "Substituir o Comandante Operacional em seus impedimentos; auxiliar no planejamento e controle das atividades operacionais; supervisionar as seções subordinadas.", order: 2 });

await insert({ datId: DF.dat, title: "Diretor do Departamento de Segurança Contra Incêndio e Pânico", acronym: "Dir DESEG", rank: "Coronel", subordinateTo: "Comandante-Geral", subordinates: "Subdiretor do DESEG; Seção de Análise de Projetos; Seção de Vistorias e Fiscalização; Seção de Perícias; Seção de Normas Técnicas", attributions: "Planejar, coordenar, supervisionar e controlar as atividades de segurança contra incêndio e pânico no DF; analisar projetos técnicos; realizar vistorias e emitir pareceres; fiscalizar edificações e áreas de risco; elaborar e atualizar normas técnicas.", order: 1 });
await insert({ datId: DF.dat, title: "Subdiretor do Departamento de Segurança Contra Incêndio e Pânico", acronym: "Sub Dir DESEG", rank: "Tenente-Coronel", subordinateTo: "Diretor do DESEG", subordinates: "Seção de Análise de Projetos; Seção de Vistorias e Fiscalização", attributions: "Substituir o Diretor do DESEG em seus impedimentos; auxiliar no planejamento e controle das atividades técnicas; supervisionar as seções subordinadas.", order: 2 });
await insert({ datId: DF.dat, title: "Chefe da Seção de Análise de Projetos", acronym: "Chefe SAP/DESEG", rank: "Major ou Capitão", subordinateTo: "Diretor do DESEG", subordinates: "Analistas de projetos", attributions: "Analisar e aprovar projetos de segurança contra incêndio e pânico; emitir laudos técnicos; orientar profissionais sobre as normas aplicáveis.", order: 3 });
await insert({ datId: DF.dat, title: "Chefe da Seção de Vistorias e Fiscalização", acronym: "Chefe SVF/DESEG", rank: "Major ou Capitão", subordinateTo: "Diretor do DESEG", subordinates: "Fiscais e vistoriadores", attributions: "Realizar vistorias em edificações e áreas de risco; fiscalizar o cumprimento das normas; notificar, embargar e interditar estabelecimentos em desconformidade.", order: 4 });

// ============================================================
// ESPÍRITO SANTO - CBMES
// Fonte: Normas Gerais de Ação - CBMES 2023
// ============================================================
const ES = IDS.ES;

await insert({ copId: ES.cop, title: "Diretor de Operações", acronym: "Dir DOp", rank: "Coronel", subordinateTo: "Comandante-Geral", subordinates: "Departamento de Operações; Departamento de Doutrinas; CIODES/CBMES", attributions: "Responsável pelo Emprego Operacional e pela Doutrina Institucional voltada à parte operacional. Estabelecer diretrizes para o emprego operacional do CBMES; centralizar a organização da doutrina institucional; supervisionar as atividades operacionais das unidades; gerenciar todos os recursos operacionais do CBMES, inclusive da frota de viaturas; coordenar a atuação dos Comitês de Desenvolvimento de Atividades do CBMES.", order: 1 });
await insert({ copId: ES.cop, title: "Chefe do Departamento de Operações", acronym: "Chefe DepOp", rank: "Tenente-Coronel ou Major", subordinateTo: "Diretor de Operações", subordinates: "Seções do Departamento de Operações", attributions: "Gerenciar, controlar e produzir o Plano de Articulação Operacional do CBMES; apoiar no gerenciamento de grandes desastres; cumprir as diretrizes do Diretor de Operações no que tange ao emprego operacional.", order: 2 });
await insert({ copId: ES.cop, title: "Chefe do Departamento de Doutrinas", acronym: "Chefe DepDout", rank: "Tenente-Coronel ou Major", subordinateTo: "Diretor de Operações", subordinates: "Seções do Departamento de Doutrinas", attributions: "Coordenar a produção descentralizada de conteúdo doutrinário; organizar e atualizar a doutrina institucional do CBMES; levantar necessidades de instrução e treinamentos.", order: 3 });
await insert({ copId: ES.cop, title: "Chefe do CIODES/CBMES", acronym: "Chefe CIODES", rank: "Major ou Capitão", subordinateTo: "Diretor de Operações", subordinates: "Seção de Operações; Seção Expediente", attributions: "Acionar, informar, coordenar e articular, com eficiência, agilidade e segurança, os recursos operacionais do CBMES para o devido socorro à sociedade nas ocorrências específicas de bombeiros e em integração com as demais agências.", order: 4 });

await insert({ datId: ES.dat, title: "Chefe do Centro de Atividades Técnicas", acronym: "Chefe CAT", rank: "Oficial Superior", subordinateTo: "Comandante-Geral (relação funcional direta com DGP, DAL e Corregedoria)", subordinates: "Subchefe do CAT (acumula chefia do DepAP); Secretaria; Departamento de Análise de Projetos (DepAP); Departamento de Investigação, Pesquisa e Prevenção de Incêndio (DepIPPI); Gerência de Normas e Cadastros; Gerência de Vistorias (GV)", attributions: "Planejar, organizar, coordenar e controlar o Quadro de Detalhamento Interno (QDI) do CAT; ser o interlocutor do CAT junto à Corregedoria e DRH; propor ao Comando-Geral designação de Comissão Técnica para revisão e elaboração de Normas Técnicas; convocar Comissão Técnica para avaliar casos omissos ou especiais; apresentar relatório anual das atividades desenvolvidas; buscar junto aos setores competentes meios para o complemento dos recursos humanos do Centro.", order: 1 });
await insert({ datId: ES.dat, title: "Subchefe do Centro de Atividades Técnicas", acronym: "Sub Chefe CAT", rank: "Oficial Superior ou Intermediário", subordinateTo: "Chefe do CAT", subordinates: "Analistas Nível IV; Gerência de Análise Nível III; Gerência de Análise Nível II; Seção de Análise Nível I", attributions: "Substituir ou representar o Chefe do CAT sempre que necessário; cumprir e fazer cumprir as determinações do Chefe do CAT; emitir Pareceres Técnicos conforme solicitação da Chefia; planejar, junto com a Chefia, a implementação de política de pessoal. Acumula a função de Chefe do Departamento de Análise de Projetos (DepAP).", order: 2 });
await insert({ datId: ES.dat, title: "Chefe do Departamento de Investigação, Pesquisa e Prevenção de Incêndio", acronym: "Chefe DepIPPI", rank: "Oficial Superior ou Intermediário", subordinateTo: "Chefe do CAT", subordinates: "Peritos; Gerência de Pesquisa e Prevenção de Incêndios (GPPI)", attributions: "Coordenar as atividades de investigação de incêndios; supervisionar as perícias; coordenar pesquisas e ações de prevenção de incêndios.", order: 3 });
await insert({ datId: ES.dat, title: "Gerente de Vistorias", acronym: "Gerente GV", rank: "Oficial Intermediário ou Subalterno", subordinateTo: "Chefe do CAT", subordinates: "Auxiliar do Gerente de Vistorias; Seção de Fiscalização", attributions: "Coordenar e supervisionar as vistorias em edificações e áreas de risco; gerenciar a Seção de Fiscalização; garantir o cumprimento das normas de segurança contra incêndio e pânico.", order: 4 });
await insert({ datId: ES.dat, title: "Gerente de Normas e Cadastros", acronym: "Gerente GNC", rank: "Oficial Intermediário ou Subalterno", subordinateTo: "Chefe do CAT", subordinates: "Chefe da Seção de Normas; Chefe da Seção de Cadastro", attributions: "Coordenar e supervisionar as atividades de normatização e cadastro de edificações e profissionais habilitados.", order: 5 });

// ============================================================
// MARANHÃO - CBMMA
// Fonte: Lei de Organização Básica do CBMMA
// ============================================================
const MA = IDS.MA;

await insert({ copId: MA.cop, title: "Comandante Operacional do Corpo de Bombeiros", acronym: "Cmt COCB", rank: "Coronel", subordinateTo: "Comandante-Geral", subordinates: "Centro de Operações e Comunicações; Batalhões de Bombeiros Militar; Companhias Independentes de Bombeiros Militar; Postos de Bombeiros Militar", attributions: "Planejar, coordenar, supervisionar e controlar as atividades operacionais dos órgãos de execução subordinados; assessorar o Comandante-Geral nos assuntos operacionais.", order: 1 });
await insert({ copId: MA.cop, title: "Chefe do Centro de Operações e Comunicações", acronym: "Chefe COC", rank: "Major ou Capitão", subordinateTo: "Comandante Operacional do Corpo de Bombeiros", subordinates: "Seção de Operações; Seção de Comunicações", attributions: "Planejar, coordenar, controlar, fiscalizar e executar as atividades operacionais e de comunicações, de pesquisas tecnológicas, de perícias e de prevenção de incêndios, além das atribuições específicas de planejamento em Proteção e Defesa Civil em sua área de circunscrição.", order: 2 });

await insert({ datId: MA.dat, title: "Diretor de Atividades Técnicas", acronym: "Dir DAT", rank: "Coronel ou Tenente-Coronel", subordinateTo: "Comandante-Geral", subordinates: "Seção de Administração; Departamento de Investigação e Prevenção de Incêndio; Departamento de Vistorias e Pareceres", attributions: "Planejar, fiscalizar e controlar as atividades de prevenção em locais de grande concentração humana, vistorias e pareceres técnicos, apoio operacional e auxílio dos serviços e missões específicas no âmbito estadual.", order: 1 });
await insert({ datId: MA.dat, title: "Chefe do Departamento de Investigação e Prevenção de Incêndio", acronym: "Chefe DIPI", rank: "Major ou Capitão", subordinateTo: "Diretor de Atividades Técnicas", subordinates: "Seção de Prevenção e Perícia", attributions: "Coordenar as atividades de investigação e prevenção de incêndios; supervisionar as perícias; elaborar laudos e relatórios técnicos.", order: 2 });
await insert({ datId: MA.dat, title: "Chefe do Departamento de Vistorias e Pareceres", acronym: "Chefe DVP", rank: "Major ou Capitão", subordinateTo: "Diretor de Atividades Técnicas", subordinates: "Seção de Análise de Projetos; Seção de Operações", attributions: "Coordenar as vistorias em edificações e áreas de risco; analisar projetos de segurança contra incêndio; emitir pareceres técnicos.", order: 3 });

// ============================================================
// MATO GROSSO - CBMMT
// Fonte: Lei de Organização Básica do CBMMT
// ============================================================
const MT = IDS.MT;

await insert({ copId: MT.cop, title: "Diretor Operacional", acronym: "Dir DOP", rank: "Coronel do QOBM", subordinateTo: "Comandante-Geral Adjunto", subordinates: "Comandos Regionais de Bombeiros Militar (CRBMs); Unidades de Bombeiros Militar (UBMs); Batalhão de Emergências Ambientais; Grupo de Aviação de Bombeiros Militar", attributions: "Responsável pela supervisão, coordenação e planejamento das políticas relacionadas com a atividade operacional da Corporação. A função de Diretor Operacional é de Coronel do QOBM da ativa, escolhido e nomeado pelo Comandante-Geral.", order: 1 });
await insert({ copId: MT.cop, title: "Comandante de Comando Regional de Bombeiros Militar", acronym: "Cmt CRBM", rank: "Oficial Superior", subordinateTo: "Diretor Operacional", subordinates: "Batalhões de Bombeiros Militar; Companhias Independentes; Pelotões Independentes; Núcleos de Bombeiros Militar", attributions: "Supervisionar, coordenar e planejar o emprego operacional das UBMs subordinadas.", order: 2 });

await insert({ datId: MT.dat, title: "Diretor da Diretoria de Segurança Contra Incêndio e Pânico", acronym: "Dir DSCI", rank: "Coronel do QOBM", subordinateTo: "Comandante-Geral Adjunto", subordinates: "Seções de Segurança Contra Incêndio e Pânico (nas UBMs, com vinculação técnica à DSCI)", attributions: "Responsável pelo planejamento, execução, coordenação e controle de todas as atividades concernentes à segurança contra incêndio e pânico das instalações, edificações e locais de risco, em conformidade com a legislação peculiar. A função de Diretor da DSCI é de Coronel do QOBM da ativa, escolhido e nomeado pelo Comandante-Geral. As Seções de Segurança Contra Incêndio e Pânico serão subordinadas administrativa e operacionalmente às respectivas UBM e terão vinculação técnica com a DSCI.", order: 1 });

// ============================================================
// MATO GROSSO DO SUL - CBMMS
// Fonte: Lei Complementar nº 188/2014 do CBMMS
// ============================================================
const MS = IDS.MS;

await insert({ copId: MS.cop, title: "Comandante Metropolitano de Bombeiros", acronym: "Cmt CMB", rank: "Coronel do QOBM (último posto)", subordinateTo: "Subcomandante-Geral", subordinates: "Subcomandante Metropolitano de Bombeiros; Batalhões e Companhias da capital e regiões subordinadas", attributions: "Responsável pelo planejamento, coordenação, fiscalização, controle, assessoramento e acompanhamento direto de todas as atividades operacionais e de prevenção desenvolvidas na capital e regiões a ela subordinadas. O Comandante do CMB será um Oficial Superior da ativa do último posto do QOBM, nomeado pelo Comandante-Geral.", order: 1 });
await insert({ copId: MS.cop, title: "Subcomandante Metropolitano de Bombeiros", acronym: "Sub Cmt CMB", rank: "Coronel do QOBM (penúltimo posto)", subordinateTo: "Comandante Metropolitano de Bombeiros", subordinates: "Seções e unidades subordinadas ao CMB", attributions: "Substituir o Comandante Metropolitano em seus impedimentos; auxiliar no planejamento e controle das atividades operacionais e de prevenção da capital.", order: 2 });

await insert({ datId: MS.dat, title: "Diretor de Atividades Técnicas", acronym: "Dir DAT", rank: "Coronel ou Tenente-Coronel", subordinateTo: "Comandante-Geral", subordinates: "Seções e departamentos da DAT", attributions: "Órgão de Direção Setorial do sistema de prevenção do CBMMS, competindo-lhe a normatização, o estudo, a análise, o planejamento das atividades preventivas, a orientação técnica, o controle e a fiscalização dos órgãos de execução da Corporação empenhados nas atividades relativas à aplicação das normas de segurança contra incêndio, pânico e outros riscos, e ao cumprimento das disposições legais sobre o assunto no âmbito do Estado de Mato Grosso do Sul.", order: 1 });

// ============================================================
// MINAS GERAIS - CBMMG
// Fonte: Lei Complementar nº 54/1999 do CBMMG
// ============================================================
const MG = IDS.MG;

await insert({ copId: MG.cop, title: "Comandante Operacional de Bombeiros", acronym: "Cmt COp", rank: "Coronel", subordinateTo: "Comandante-Geral", subordinates: "Batalhões de Bombeiros Militar (BBM); Companhias Independentes de Bombeiros Militar (CIA IND BM)", attributions: "Responsável pelo planejamento, coordenação, supervisão e controle das atividades operacionais. Os Batalhões e Companhias Independentes de Bombeiros Militar são subordinados diretamente ao Comando Operacional de Bombeiros e realizam ações de prevenção e combate a incêndio, busca e salvamento, socorros de urgência e defesa civil. A subordinação, competência e responsabilidade territorial das Unidades de Execução Operacional serão definidas pelo Comando-Geral.", order: 1 });

await insert({ datId: MG.dat, title: "Chefe do Centro de Atividades Técnicas", acronym: "Chefe CAT", rank: "Coronel ou Tenente-Coronel", subordinateTo: "Comandante-Geral", subordinates: "Seções e departamentos do CAT", attributions: "Pesquisar, analisar, planejar, normatizar, exigir e fiscalizar o cumprimento das disposições legais próprias dos serviços de segurança contra incêndio e pânico; realizar perícias de incêndio e explosão em locais de sinistro; atuar como segunda instância na análise de projetos de prevenção no Estado. O CAT é unidade subordinada diretamente ao Comando-Geral do CBMMG.", order: 1 });

// ============================================================
// PARÁ - CBMPA
// Fonte: Lei de Organização Básica do CBMPA (2025)
// ============================================================
const PA = IDS.PA;

await insert({ copId: PA.cop, title: "Comandante Operacional", acronym: "Cmt Op", rank: "Coronel do QOBM (último posto)", subordinateTo: "Comandante-Geral", subordinates: "Assistente; Seção de Planejamento de Pessoal; Seção de Planejamento Logístico; Seção de Planejamento de Operações e Estatística; Seção de Planejamento de Eventos; Secretaria; órgãos de direção intermediária e setorial, de apoio e de execução", attributions: "Órgão de direção-geral responsável pela direção e pelo controle dos órgãos de direção intermediária e setorial, de apoio e de execução da atividade-fim da corporação. O Comandante Operacional será um oficial do último posto do QOBM, indicado pelo Comandante-Geral e de livre nomeação do Chefe do Poder Executivo Estadual, com precedência hierárquica e funcional sobre os comandantes dos órgãos subordinados. Na ausência, responderá pelo Comando de Operações o comandante do órgão de direção intermediária mais antigo da Região Metropolitana de Belém.", order: 1 });
await insert({ copId: PA.cop, title: "Assistente do Comando de Operações", acronym: "Assistente Cmt Op", rank: "Tenente-Coronel do QOBM", subordinateTo: "Comandante Operacional", subordinates: "Seções do Comando de Operações", attributions: "Auxiliar o Comandante Operacional no planejamento e controle das atividades; supervisionar as seções do Comando de Operações.", order: 2 });
await insert({ copId: PA.cop, title: "Chefe de Seção do Comando de Operações", acronym: "Chefe Seção Cmt Op", rank: "Major do QOBM", subordinateTo: "Comandante Operacional", subordinates: "Subseções (cada seção pode ser desdobrada em até 2 subseções)", attributions: "Planejar, coordenar e controlar as atividades da respectiva seção: Planejamento de Pessoal, Logístico, de Operações e Estatística, ou de Eventos.", order: 3 });

await insert({ datId: PA.dat, title: "Chefe do Departamento-Geral de Segurança contra Incêndios e Emergências", acronym: "Chefe DGSCI", rank: "Coronel do QOBM (último posto)", subordinateTo: "Comandante-Geral", subordinates: "Subchefe do DGSCI; Seção de Fiscalização e Vistoria Técnica; Seção de Análise de Projetos; Seção de Perícia de Incêndio; Seção de Credenciamento de Empresas e Profissionais; Secretaria; Seções de Atividades Técnicas (SATs) nas Unidades Bombeiro Militar", attributions: "Responsável por estabelecer diretrizes gerais de segurança contra incêndios e emergências, de modo a proteger a vida e reduzir danos ao meio ambiente e ao patrimônio. O Chefe do DGSCI é um oficial do último posto do QOBM, indicado pelo Comandante-Geral e de livre nomeação do Chefe do Poder Executivo Estadual.", order: 1 });
await insert({ datId: PA.dat, title: "Subchefe do Departamento-Geral de Segurança contra Incêndios e Emergências", acronym: "Sub Chefe DGSCI", rank: "Tenente-Coronel do QOBM", subordinateTo: "Chefe do DGSCI", subordinates: "Seções de Atividades Técnicas (SATs) nas Unidades Bombeiro Militar", attributions: "Responder pela chefia do DGSCI na ausência do titular; exercer a supervisão das Seções de Atividades Técnicas (SATs) instaladas nas Unidades Bombeiro Militar.", order: 2 });
await insert({ datId: PA.dat, title: "Chefe de Seção do DGSCI", acronym: "Chefe Seção DGSCI", rank: "Oficial Superior do QOBM (Credenciamento: oficial intermediário)", subordinateTo: "Chefe do DGSCI", subordinates: "Subseções (cada seção pode ser desdobrada em até 3 subseções)", attributions: "Planejar, coordenar e controlar as atividades da respectiva seção: Fiscalização e Vistoria Técnica, Análise de Projetos, Perícia de Incêndio, ou Credenciamento de Empresas e Profissionais.", order: 3 });

// ============================================================
// PARAÍBA - CBMPB
// Fonte: Lei de Organização Básica do CBMPB
// ============================================================
const PB = IDS.PB;

await insert({ copId: PB.cop, title: "Comandante Regional de Bombeiro Militar", acronym: "Cmt CRBM", rank: "Coronel", subordinateTo: "Comandante-Geral", subordinates: "Subcomandante Regional; Estado Maior Regional (EM/R); Centro Regional de Intendência (CRI); Batalhões de Bombeiro Militar (BBM); Companhias Independentes de Bombeiro Militar (CIBM)", attributions: "Responsável pelo planejamento, coordenação, supervisão e controle das atividades operacionais na REISP de sua responsabilidade. Escolhido privativamente entre os coronéis da ativa, nomeado por ato do Governador do Estado. O CRBM tem jurisdição na REISP onde está instalado, podendo apoiar operacionalmente municípios de responsabilidade de outro CRBM.", order: 1 });
await insert({ copId: PB.cop, title: "Subcomandante Regional de Bombeiro Militar", acronym: "Sub Cmt CRBM", rank: "Tenente-Coronel", subordinateTo: "Comandante Regional de Bombeiro Militar", subordinates: "Estado Maior Regional (EM/R); Centro Regional de Intendência (CRI)", attributions: "Substituir o Comandante Regional em seus impedimentos; auxiliar no planejamento e controle das atividades operacionais da regional. Escolhido privativamente entre os tenentes-coronéis da ativa, nomeado por ato do Governador do Estado.", order: 2 });
await insert({ copId: PB.cop, title: "Chefe do Estado Maior Regional", acronym: "Chefe EM/R", rank: "Oficial Superior ou Intermediário", subordinateTo: "Comandante Regional de Bombeiro Militar", subordinates: "B/1 (Gestão de Pessoas e Secretaria); B/2 (Inteligência); B/3 (Articulação Operacional); B/4 (Articulação Logística e Mobilização); B/5 (Comunicação Social e Marketing); B/6 (Compras e Finanças)", attributions: "Coordenar e supervisionar as atividades das seções do Estado Maior Regional; assessorar o Comandante Regional nos assuntos de planejamento e gestão.", order: 3 });

await insert({ datId: PB.dat, title: "Diretor de Atividades Técnicas", acronym: "Dir DAT", rank: "Coronel", subordinateTo: "Subcomandante-Geral", subordinates: "Vice-Diretor de Atividades Técnicas; Conselho Técnico Normativo (CTN); Conselho Técnico Deliberativo (CTD); Comissão Interna de Análise Técnica (CIAT); Seção DAT/1 (Legislação de Prevenção); Seção DAT/2 (Segurança contra Incêndio); Centros de Atividades Técnicas (CATs) - vinculação doutrinária e normativa", attributions: "Unidade gestora, em nível setorial, organizada de forma sistêmica, responsável pelo estudo, análise, planejamento, orientação técnica, normatização, controle e fiscalização das atividades relativas à segurança contra incêndio e controle de pânico, ao cumprimento das disposições legais sobre o assunto e investigação de incêndios e explosões. A DAT tem jurisdição em todo o território do Estado da Paraíba. Cargo de provimento em comissão, nomeado por ato do Governador do Estado.", order: 1 });
await insert({ datId: PB.dat, title: "Vice-Diretor de Atividades Técnicas", acronym: "Vice-Dir DAT", rank: "Tenente-Coronel", subordinateTo: "Diretor de Atividades Técnicas", subordinates: "Seção DAT/1; Seção DAT/2", attributions: "Substituir o Diretor de Atividades Técnicas em seus impedimentos; auxiliar no planejamento e controle das atividades técnicas. Cargo de provimento em comissão, nomeado por ato do Governador do Estado.", order: 2 });

// ============================================================
// PARANÁ - CBMPR
// Fonte: Lei Ordinária nº 22.206/2024 do CBMPR
// ============================================================
const PR = IDS.PR;

await insert({ copId: PR.cop, title: "Comandante Regional Bombeiro Militar", acronym: "Cmt CRBM", rank: "Coronel Combatente", subordinateTo: "Subcomandante-Geral", subordinates: "Batalhões de Bombeiro Militar (BBM); Companhias Independentes de Bombeiro Militar (Cia. Ind. BM); Grupo de Operações de Socorro Tático (GOST); Unidades de Operações Aéreas (UOA)", attributions: "Responsável pelo planejamento, coordenação, supervisão e controle das atividades operacionais na circunscrição regional. O Subcomandante-Geral exerce a função de coordenador operacional da Corporação.", order: 1 });

await insert({ datId: PR.dat, title: "Diretor de Atividades Técnicas", acronym: "Dir DAT", rank: "Coronel ou Tenente-Coronel", subordinateTo: "Subcomandante-Geral", subordinates: "Seções e departamentos da DAT", attributions: "Órgão de direção setorial responsável pela coordenação, controle e assessoramento em assuntos relacionados: à prevenção e combate a incêndios e desastres em edificações, estabelecimentos, áreas de risco e eventos temporários, atuando por meio do gerenciamento normativo, estudos e pesquisa de incêndios; à tecnologia da informação e comunicação, com ações de gestão e desenvolvimento de sistemas informatizados, infraestrutura, segurança, projetos, inovações e governança.", order: 1 });

// ============================================================
// PIAUÍ - CBMPI
// Fonte: Lei de Organização Básica do CBMPI
// ============================================================
const PI = IDS.PI;

await insert({ copId: PI.cop, title: "Comandante Operacional de Bombeiros", acronym: "Cmt COB", rank: "Coronel do QOBM Combatente", subordinateTo: "Órgão de direção geral", subordinates: "Subcomandante Operacional de Bombeiros; Seção Administrativa; Seção de Operações e Comunicações; Seção de Controle e Fiscalização de Hidrantes; Seção de Planejamento, Estatística e Avaliação Operacional; Núcleo de Investigação e Prevenção de Incêndios; Comandos Regionais de Bombeiros Militar", attributions: "Órgão de execução do mais alto escalão do sistema operacional subordinado ao órgão de direção geral, tendo a seu cargo o planejamento estratégico e a fiscalização do emprego dos Comandos Regionais de Bombeiros.", order: 1 });
await insert({ copId: PI.cop, title: "Subcomandante Operacional de Bombeiros", acronym: "Sub Cmt COB", rank: "Tenente-Coronel do QOBM Combatente", subordinateTo: "Comandante Operacional de Bombeiros", subordinates: "Seção Administrativa; Seção de Operações e Comunicações; Seção de Controle e Fiscalização de Hidrantes; Seção de Planejamento, Estatística e Avaliação Operacional; Núcleo de Investigação e Prevenção de Incêndios", attributions: "Substituir o Comandante Operacional em seus impedimentos; auxiliar no planejamento estratégico e na fiscalização do emprego dos Comandos Regionais.", order: 2 });
await insert({ copId: PI.cop, title: "Chefe do Núcleo de Investigação e Prevenção de Incêndios", acronym: "Chefe NIPI", rank: "Oficial Superior ou Intermediário", subordinateTo: "Comandante Operacional de Bombeiros", subordinates: "Subchefe; Seção de Perícias; Seção de Pesquisas; Laboratório", attributions: "Realizar as análises laboratoriais relacionadas à investigação de incêndios e de explosões; emitir conclusões técnicas sobre atividades preventivas.", order: 3 });
await insert({ copId: PI.cop, title: "Comandante Regional de Bombeiros Militar", acronym: "Cmt CRB", rank: "Oficial Superior", subordinateTo: "Comandante Operacional de Bombeiros", subordinates: "Subcomandante; Seção Administrativa; Seção de Planejamento e Avaliação Operacional", attributions: "Efetuar o planejamento operacional, a supervisão, a coordenação, prevenção, o controle, a fiscalização e a execução das atividades de bombeiro no âmbito de suas respectivas responsabilidades e circunscrições.", order: 4 });

await insert({ datId: PI.dat, title: "Diretor da Diretoria de Segurança Contra Incêndio", acronym: "Dir DSCI", rank: "Coronel ou Tenente-Coronel", subordinateTo: "Comandante-Geral", subordinates: "Seção de Análise de Projetos (DSCI-1); Seção de Vistorias e Pareceres (DSCI-2); Seção de Fiscalização (DSCI-3); Seção de Apoio Técnico (DSCI-4); Seção de Estatística e Arquivo (DSCI-5)", attributions: "Unidade administrativa responsável pelo planejamento, análise, controle e fiscalização das atividades atinentes à segurança contra incêndio e pânico no âmbito do Estado do Piauí.", order: 1 });

// ============================================================
// RONDÔNIA - CBMRO
// Fonte: Minuta de Projeto de Lei de Organização Básica do CBMRO
// Art. 22 - DPO subordinada ao Subcomandante-Geral
// Art. 24 - COT subordinado à DPO
// Art. 42 - CATs subordinadas ao COT
// ============================================================
const RO = IDS.RO;

await insert({ copId: RO.cop, title: "Diretor de Planejamento Operacional", acronym: "Dir DPO", rank: "Coronel ou Tenente-Coronel", subordinateTo: "Subcomandante-Geral", subordinates: "Adjunto; Seção Administrativa; Coordenadoria de Operações; Coordenadoria de Doutrina e Pesquisa; Coordenadoria de Estudos Estratégicos", attributions: "Órgão responsável pelo planejamento, direção, coordenação, supervisão, fiscalização e avaliação das atividades operacionais da Corporação, visando a eficiência e a eficácia das ações dos órgãos de execução subordinados. Subordinado ao Subcomandante-Geral.", order: 1 });
await insert({ copId: RO.cop, title: "Adjunto da Diretoria de Planejamento Operacional", acronym: "Adj DPO", rank: "Tenente-Coronel ou Major", subordinateTo: "Diretor de Planejamento Operacional", subordinates: "Seção Administrativa; Coordenadorias", attributions: "Substituir o Diretor de Planejamento Operacional em seus impedimentos; auxiliar no planejamento e controle das atividades operacionais.", order: 2 });
await insert({ copId: RO.cop, title: "Coordenador de Operações", acronym: "Coord Op", rank: "Major ou Capitão", subordinateTo: "Diretor de Planejamento Operacional", subordinates: "Adjunto; Seção Administrativa", attributions: "Planejar, coordenar e controlar as atividades operacionais no âmbito da Coordenadoria de Operações.", order: 3 });
await insert({ copId: RO.cop, title: "Coordenador de Doutrina e Pesquisa", acronym: "Coord Dout", rank: "Major ou Capitão", subordinateTo: "Diretor de Planejamento Operacional", subordinates: "Adjunto; Seção Administrativa", attributions: "Planejar, coordenar e controlar as atividades de doutrina e pesquisa operacional.", order: 4 });
await insert({ copId: RO.cop, title: "Coordenador de Estudos Estratégicos", acronym: "Coord EE", rank: "Major ou Capitão", subordinateTo: "Diretor de Planejamento Operacional", subordinates: "Adjunto; Seção Administrativa", attributions: "Planejar, coordenar e controlar as atividades de estudos estratégicos operacionais.", order: 5 });

await insert({ datId: RO.dat, title: "Comandante do Comando de Operações Técnicas", acronym: "Cmt COT", rank: "Oficial da ativa do último Posto do QOEMBM ou QCOBM", subordinateTo: "Diretoria de Planejamento Operacional", subordinates: "Adjunto; Seção Administrativa; Seção de Estudos Técnicos; Seção de Planejamento, Fiscalização e Suporte Técnico; Coordenadorias de Atividades Técnicas (CATs); Coordenadoria de Projetos de Arquitetura e Engenharia", attributions: "Órgão máximo responsável pelo controle e observância dos requisitos técnicos contra incêndio e pânico das edificações e áreas de risco, competindo-lhe o estudo, a análise, o planejamento, a normatização, a exigência, a fiscalização e a execução das normas que disciplinam a segurança contra incêndio e pânico, bem como a elaboração de projetos de engenharia e arquitetura, acompanhamento e fiscalização de obras no âmbito do CBMRO. Quando a escolha recair sobre oficial do QCOBM, deverá ser possuidor de formação nas áreas de Engenharia ou Arquitetura. Subordinado à Diretoria de Planejamento Operacional.", order: 1 });
await insert({ datId: RO.dat, title: "Adjunto do Comando de Operações Técnicas", acronym: "Adj COT", rank: "Tenente-Coronel ou Major", subordinateTo: "Comandante do COT", subordinates: "Seção Administrativa; Seção de Estudos Técnicos; Seção de Planejamento, Fiscalização e Suporte Técnico", attributions: "Substituir o Comandante do COT em seus impedimentos; auxiliar no planejamento e controle das atividades técnicas.", order: 2 });
await insert({ datId: RO.dat, title: "Coordenador de Atividades Técnicas", acronym: "Coord CAT", rank: "Major ou Capitão", subordinateTo: "Comandante do COT", subordinates: "Adjunto; Seção Administrativa; Seção de Análise de Projetos; Seção de Investigação e Prevenção de Incêndio; Gerência de Atividades Técnicas (Seção de Vistoria; Seção de Hidrantes)", attributions: "Estudar, analisar, exigir e fiscalizar as atividades pertinentes à segurança contra incêndio e pânico; proceder à análise de projetos; realizar investigação de incêndios, testes de materiais, vistorias e emitir pareceres técnicos; com autoridade para notificar, multar, embargar e interditar na forma da lei específica. Subordinado ao Comando de Operações Técnicas (COT).", order: 3 });
await insert({ datId: RO.dat, title: "Coordenador de Projetos de Arquitetura e Engenharia", acronym: "Coord PAE", rank: "Major ou Capitão", subordinateTo: "Comandante do COT", subordinates: "Adjunto; Seção Administrativa; Seção de Fiscalização e Vistorias de Obras; Seção de Projetos, Planejamento e Estudos Técnicos; Seção de Manutenção Predial", attributions: "Planejar, coordenar e controlar as atividades de elaboração de projetos de arquitetura e engenharia, fiscalização e vistoria de obras no âmbito do CBMRO. Classificado como Órgão de Apoio Setorial.", order: 4 });

// ============================================================
// SERGIPE - CBMSE
// Fonte: Lei de Organização Básica do CBMSE
// ============================================================
const SE = IDS.SE;

await insert({ copId: SE.cop, title: "Diretor Operacional", acronym: "Dir DOP", rank: "Coronel", subordinateTo: "Comandante-Geral", subordinates: "Diretor-Adjunto da DOP; Comandos Regionais; Grupamentos Especializados", attributions: "Responsável pela gestão, planejamento, coordenação, execução, fiscalização e controle das atividades operacionais e na execução das atividades de proteção e defesa civil, sendo responsável pela coordenação e emprego dos Comandos Regionais e Unidades Operacionais que lhe são subordinadas.", order: 1 });
await insert({ copId: SE.cop, title: "Diretor-Adjunto da Diretoria Operacional", acronym: "Dir Adj DOP", rank: "Tenente-Coronel", subordinateTo: "Diretor Operacional", subordinates: "Seções e unidades da DOP", attributions: "Atuar como auxiliar direto do Diretor Operacional e substituí-lo em suas ausências.", order: 2 });

await insert({ datId: SE.dat, title: "Diretor de Atividades Técnicas", acronym: "Dir DAT", rank: "Coronel", subordinateTo: "Comandante-Geral", subordinates: "Diretor-Adjunto da DAT; Seções e departamentos da DAT", attributions: "Responsável pela gestão, planejamento, coordenação, execução, fiscalização e controle de todas as atividades concernentes à segurança contra incêndio e pânico das instalações, edificações e locais de risco, no âmbito do Estado de Sergipe.", order: 1 });
await insert({ datId: SE.dat, title: "Diretor-Adjunto da Diretoria de Atividades Técnicas", acronym: "Dir Adj DAT", rank: "Tenente-Coronel", subordinateTo: "Diretor de Atividades Técnicas", subordinates: "Seções da DAT", attributions: "Atuar como auxiliar direto do Diretor de Atividades Técnicas e substituí-lo em suas ausências.", order: 2 });

// ============================================================
// TOCANTINS - CBMTO
// Fonte: Lei de Organização Básica do CBMTO
// ============================================================
const TO = IDS.TO;

await insert({ copId: TO.cop, title: "Comandante Operacional Bombeiro Militar", acronym: "Cmt COBM", rank: "Coronel do QOBM", subordinateTo: "Chefe do Estado-Maior", subordinates: "Regionais (conforme plano de articulação do CBMTO); Unidades operacionais", attributions: "Responsável pelo planejamento dos assuntos relativos à articulação operacional, à administração e ao controle das operações bombeiro militares e pelos estudos, estatísticas, doutrinas, pesquisas e padronização de procedimentos relacionados às atividades operacionais da Corporação. De acordo com a necessidade, poderá o Comando Operacional Bombeiro Militar ser dividido em regionais, conforme plano de articulação do CBMTO.", order: 1 });

await insert({ datId: TO.dat, title: "Comandante de Atividades Técnicas", acronym: "Cmt CAT", rank: "Coronel do QOBM", subordinateTo: "Chefe do Estado-Maior", subordinates: "Diretoria de Serviços Técnicos", attributions: "Encarregado de planejar, controlar e fiscalizar as atividades atinentes à segurança contra incêndio e emergência no Estado.", order: 1 });
await insert({ datId: TO.dat, title: "Diretor de Serviços Técnicos", acronym: "Dir DST", rank: "Tenente-Coronel ou Major", subordinateTo: "Comandante de Atividades Técnicas", subordinates: "Seções e departamentos da DST", attributions: "Responsável pela coordenação da área de prevenção contra incêndio e emergência. Subordinada ao Comando de Atividades Técnicas.", order: 2 });

console.log("✅ Seed v2 concluído com sucesso!");
await conn.end();
