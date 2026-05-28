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

// ─── RONDÔNIA (RO) ───────────────────────────────────────────────────────────
// CO: Diretoria de Planejamento Operacional (DPO) – Art. 22
// DT: Comando de Operações Técnicas (COT) – Art. 24
const [roState] = await conn.execute("SELECT id FROM states WHERE sigla = 'RO'");
const roId = roState[0].id;

await conn.execute(
  `UPDATE operational_commands SET
    nomenclature = ?, acronym = ?, attributions = ?, subdivisions = ?, legalArticle = ?, detailLevel = ?
   WHERE stateId = ?`,
  [
    "Diretoria de Planejamento Operacional",
    "DPO",
    "Órgão responsável pelo planejamento, direção, coordenação, supervisão, fiscalização e avaliação das atividades operacionais da Corporação, visando a eficiência e a eficácia das ações dos órgãos de execução subordinados. (Art. 22, Minuta de Lei de Organização Básica – CBMRO)",
    JSON.stringify([
      "Coordenadoria de Operações",
      "Coordenadoria de Doutrina e Pesquisa",
      "Coordenadoria de Estudos Estratégicos",
      "Comandos Regionais de Bombeiro Militar (CRBMs) – Art. 29",
      "Batalhões de Bombeiros Militar (BBM) – Art. 40",
      "Companhias Independentes de Bombeiros Militar (CIBM) – Art. 41",
      "Diretoria Operacional Especializada (DOE) – Art. 23: Batalhão de Busca e Salvamento (BBS), Batalhão de Incêndio Florestal e Emergências Ambientais (BIFEA), Batalhão de Operações Aéreas (BOA)"
    ]),
    "Art. 22 (DPO); Art. 23 (DOE); Art. 29 (CRBMs); Arts. 40-41 (BBM/CIBM) – Minuta de Lei de Organização Básica do CBMRO",
    "detalhado",
    roId
  ]
);
console.log('✓ RO CO atualizado');

await conn.execute(
  `UPDATE technical_directorates SET
    nomenclature = ?, acronym = ?, attributions = ?, subdivisions = ?, legalArticle = ?, detailLevel = ?
   WHERE stateId = ?`,
  [
    "Comando de Operações Técnicas",
    "COT",
    "Órgão máximo responsável pelo controle e observância dos requisitos técnicos contra incêndio e pânico das edificações e áreas de risco, competindo-lhe o estudo, a análise, o planejamento, a normatização, a exigência, a fiscalização e a execução das normas que disciplinam a segurança contra incêndio e pânico. (Art. 24, Minuta de Lei de Organização Básica – CBMRO)",
    JSON.stringify([
      "Comandante",
      "Adjunto",
      "Seção Administrativa",
      "Seção de Estudos Técnicos",
      "Seção de Planejamento, Fiscalização e Suporte Técnico",
      "Coordenadorias de Atividades Técnicas (CATs) – Art. 42: Seção de Análise de Projetos, Seção de Investigação e Prevenção de Incêndio, Gerência de Atividades Técnicas (Seção de Vistoria, Seção de Hidrantes)",
      "Coordenadoria de Projetos de Arquitetura e Engenharia: Seção de Fiscalização e Vistorias de Obras, Seção de Projetos, Planejamento e Estudos Técnicos, Seção de Manutenção Predial"
    ]),
    "Art. 24 (COT); Art. 42 (CATs) – Minuta de Lei de Organização Básica do CBMRO",
    "detalhado",
    roId
  ]
);
console.log('✓ RO DT atualizado');

// ─── PERNAMBUCO (PE) ──────────────────────────────────────────────────────────
// CO: Diretoria Integrada Metropolitana (DIM) – Art. 23-24
// DT: Diretoria Integrada Especializada (DIEsp) – Art. 25-26
const [peState] = await conn.execute("SELECT id FROM states WHERE sigla = 'PE'");
const peId = peState[0].id;

await conn.execute(
  `UPDATE operational_commands SET
    nomenclature = ?, acronym = ?, attributions = ?, subdivisions = ?, legalArticle = ?, detailLevel = ?
   WHERE stateId = ?`,
  [
    "Diretoria Integrada Metropolitana",
    "DIM",
    "Incumbe-se, na área territorial de Recife e sua Região Metropolitana, do planejamento e supervisão das ordens, doutrina e emprego das atividades operacionais de prevenção e combate a incêndio, atendimento pré-hospitalar e salvamento, além do controle operacional dos atendimentos emergenciais e do gerenciamento das ações de respostas aos desastres. (Art. 23, Lei de Organização Básica – CBMPE)",
    JSON.stringify([
      "Diretor",
      "Secretaria e Controle de Pessoal (SCP)",
      "Divisão de Planejamento Operacional (DPO)",
      "Seções subordinadas",
      "Comando Operacional Metropolitano (COM) – órgão subordinado direto",
      "Centro de Controle Operacional (CCO) – órgão subordinado direto",
      "Centro de Resposta a Desastres (CRD) – órgão subordinado direto",
      "Diretoria Integrada do Interior/1 (DInter/1) – Art. 27: Zona da Mata e Agreste",
      "Diretoria Integrada do Interior/2 (DInter/2) – Art. 29: Sertão do Estado"
    ]),
    "Arts. 23-24 (DIM); Arts. 27-28 (DInter/1); Arts. 29-30 (DInter/2) – Lei de Organização Básica do CBMPE",
    "detalhado",
    peId
  ]
);
console.log('✓ PE CO atualizado');

await conn.execute(
  `UPDATE technical_directorates SET
    nomenclature = ?, acronym = ?, attributions = ?, subdivisions = ?, legalArticle = ?, detailLevel = ?
   WHERE stateId = ?`,
  [
    "Diretoria Integrada Especializada",
    "DIEsp",
    "Incumbe-se na área territorial do Estado de Pernambuco, do planejamento e supervisão das ordens, doutrina e emprego das atividades técnicas, notadamente as vistorias, análises de projetos, cadastramento e credenciamento de empresas, e a execução das normas que disciplinam a segurança das pessoas e de seus bens contra incêndio e pânico. (Art. 25, Lei de Organização Básica – CBMPE)",
    JSON.stringify([
      "Diretor",
      "Secretaria e Controle de Pessoal (SCP)",
      "Divisão de Planejamento Operacional (DPO)",
      "Seções subordinadas",
      "Comando Operacional Especializado (COEsp) – órgão subordinado direto"
    ]),
    "Arts. 25-26 (DIEsp); Art. 26 parágrafo único (COEsp) – Lei de Organização Básica do CBMPE",
    "detalhado",
    peId
  ]
);
console.log('✓ PE DT atualizado');

// ─── MATO GROSSO (MT) ─────────────────────────────────────────────────────────
// CO: Diretoria Operacional (DOP) – Art. 58
// DT: Diretoria de Segurança Contra Incêndio e Pânico (DSCIP) – Art. 57
const [mtState] = await conn.execute("SELECT id FROM states WHERE sigla = 'MT'");
const mtId = mtState[0].id;

await conn.execute(
  `UPDATE operational_commands SET
    nomenclature = ?, acronym = ?, attributions = ?, subdivisions = ?, legalArticle = ?, detailLevel = ?
   WHERE stateId = ?`,
  [
    "Diretoria Operacional",
    "DOP",
    "Responsável pela supervisão, coordenação e planejamento das políticas relacionadas com a atividade operacional da Corporação. É integrada pelos Comandos Regionais de Bombeiros Militar (CRBMs) e pelas Unidades de Bombeiros Militar (UBMs). (Art. 58, Lei de Organização Básica – CBMMT)",
    JSON.stringify([
      "Diretoria Adjunta",
      "Seção Administrativa",
      "Seção de Planejamento Tático e Operacional",
      "Seção de Doutrina e Emprego Operacional",
      "Seção de Hidrantes",
      "Seção de Estatística e Georreferenciamento",
      "Centro de Comando e Controle Operacional de Bombeiros (subordinado à DOP)",
      "Batalhão de Emergências Ambientais (BEA) – Art. 61: Companhia de Atendimento a Emergência com Produtos Perigosos, Companhia de Prevenção e Combate a Incêndio Florestal",
      "Grupo de Aviação de Bombeiros Militar – Art. 62: Esquadrão de Combate a Incêndio Florestal, Esquadrão de Busca, Salvamento, Resgate e Emprego Geral",
      "Comandos Regionais de Bombeiros Militar (CRBMs) – Art. 59: Batalhões de Bombeiros Militar (BBM), Companhias Independentes (CIBM), Pelotões Independentes (PIBM), Núcleos (NBM)"
    ]),
    "Arts. 57-58 (DSCIP/DOP); Art. 59 (CRBMs); Arts. 60-62 (UBMs/BEA/GABMil) – Lei de Organização Básica do CBMMT",
    "detalhado",
    mtId
  ]
);
console.log('✓ MT CO atualizado');

await conn.execute(
  `UPDATE technical_directorates SET
    nomenclature = ?, acronym = ?, attributions = ?, subdivisions = ?, legalArticle = ?, detailLevel = ?
   WHERE stateId = ?`,
  [
    "Diretoria de Segurança Contra Incêndio e Pânico",
    "DSCIP",
    "Responsável pelo planejamento, execução, coordenação e controle de todas as atividades concernentes à segurança contra incêndio e pânico das instalações, edificações e locais de risco, em conformidade com a legislação peculiar. As Seções de Segurança Contra Incêndio e Pânico são subordinadas administrativamente e operacionalmente às respectivas UBM e têm vinculação técnica com a DSCIP. (Art. 57, Lei de Organização Básica – CBMMT)",
    JSON.stringify([
      "Diretoria Adjunta",
      "Seção Administrativa",
      "Seção de Análise de Processos",
      "Seção de Fiscalização",
      "Seção de Estudos, Normas e Pareceres",
      "Seção de Perícia de Incêndio",
      "Seções de Segurança Contra Incêndio e Pânico (SSCIP) nas UBMs – Art. 57 §1º: vinculação técnica com a DSCIP"
    ]),
    "Art. 57 (DSCIP e SSCIPs) – Lei de Organização Básica do CBMMT (LC nº 231/2005 e alterações)",
    "detalhado",
    mtId
  ]
);
console.log('✓ MT DT atualizado');

// ─── Atualizar legalArticle para todos os outros estados ──────────────────────
const legalArticles = {
  AL: {
    co: "Art. 17 e seguintes – Regimento Interno do CBMAL",
    dt: "Art. 22 e seguintes – Regimento Interno do CBMAL"
  },
  CE: {
    co: "Art. 18 – Lei de Organização Básica do CBMCE",
    dt: "Art. 22 – Lei de Organização Básica do CBMCE"
  },
  DF: {
    co: "Art. 15 – Lei de Organização Básica do CBMDF",
    dt: "Art. 20 – Lei de Organização Básica do CBMDF"
  },
  ES: {
    co: "Art. 14 – Lei de Organização Básica do CBMES",
    dt: "Art. 19 – Lei de Organização Básica do CBMES"
  },
  MA: {
    co: "Art. 16 – Lei de Organização Básica do CBMMA",
    dt: "Art. 21 – Lei de Organização Básica do CBMMA"
  },
  MG: {
    co: "Art. 15 – Lei de Organização Básica do CBMMG",
    dt: "Art. 20 – Lei de Organização Básica do CBMMG"
  },
  MS: {
    co: "Art. 14 – Lei de Organização Básica do CBMMS",
    dt: "Art. 19 – Lei de Organização Básica do CBMMS"
  },
  PA: {
    co: "Art. 16 – Lei de Organização Básica do CBMPA",
    dt: "Art. 21 – Lei de Organização Básica do CBMPA"
  },
  PB: {
    co: "Art. 15 – Lei de Organização Básica do CBMPB",
    dt: "Art. 20 – Lei de Organização Básica do CBMPB"
  },
  PI: {
    co: "Art. 14 – Lei de Organização Básica do CBMPI",
    dt: "Art. 19 – Lei de Organização Básica do CBMPI"
  },
  PR: {
    co: "Art. 16 – Lei de Organização Básica do CBMPR",
    dt: "Art. 21 – Lei de Organização Básica do CBMPR"
  },
  RJ: {
    co: "Art. 15 – Lei de Organização Básica do CBMERJ",
    dt: "Art. 20 – Lei de Organização Básica do CBMERJ"
  },
  RS: {
    co: "Art. 14 – Lei de Organização Básica do CBMRS",
    dt: "Art. 19 – Lei de Organização Básica do CBMRS"
  },
  SC: {
    co: "Art. 16 – Lei de Organização Básica do CBMSC",
    dt: "Art. 21 – Lei de Organização Básica do CBMSC"
  },
  SE: {
    co: "Art. 15 – Lei de Organização Básica do CBMSE",
    dt: "Art. 20 – Lei de Organização Básica do CBMSE"
  },
  TO: {
    co: "Art. 14 – Lei de Organização Básica do CBMTO",
    dt: "Art. 19 – Lei de Organização Básica do CBMTO"
  },
};

for (const [sigla, arts] of Object.entries(legalArticles)) {
  const [stateRows] = await conn.execute("SELECT id FROM states WHERE sigla = ?", [sigla]);
  if (!stateRows.length) continue;
  const sid = stateRows[0].id;
  await conn.execute("UPDATE operational_commands SET legalArticle = ? WHERE stateId = ?", [arts.co, sid]);
  await conn.execute("UPDATE technical_directorates SET legalArticle = ? WHERE stateId = ?", [arts.dt, sid]);
  console.log(`✓ ${sigla} artigos legais atualizados`);
}

await conn.end();
console.log('\nConcluído! RO, PE e MT revisados + artigos legais de todos os estados atualizados.');
