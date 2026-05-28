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

// Buscar ID do estado RO
const [stateRows] = await conn.execute("SELECT id FROM states WHERE sigla = 'RO'");
if (!stateRows.length) { console.error('Estado RO não encontrado'); process.exit(1); }
const stateId = stateRows[0].id;

// Atualizar Comando Operacional de RO
// RO tem: DPO (Diretoria de Planejamento Operacional) + DOE (Diretoria Operacional Especializada)
// Os CRBMs são subordinados à DPO
const [opRows] = await conn.execute('SELECT id FROM operational_commands WHERE stateId = ?', [stateId]);
if (opRows.length) {
  await conn.execute(
    'UPDATE operational_commands SET nomenclature = ?, acronym = ?, attributions = ?, subdivisions = ?, detailLevel = ? WHERE id = ?',
    [
      "Diretoria de Planejamento Operacional",
      "DPO",
      "Órgão responsável pelo planejamento, direção, coordenação, supervisão, fiscalização e avaliação das atividades operacionais da Corporação, visando a eficiência e a eficácia das ações dos órgãos de execução subordinados. (Minuta de Lei de Organização Básica – CBMRO)",
      JSON.stringify([
        "Coordenadoria de Operações",
        "Coordenadoria de Doutrina e Pesquisa",
        "Coordenadoria de Estudos Estratégicos",
        "Comandos Regionais de Bombeiro Militar (CRBMs)",
        "Batalhões de Bombeiros Militar (BBM)",
        "Companhias Independentes de Bombeiros Militar (CIBM)",
        "Diretoria Operacional Especializada (DOE) – Batalhão de Busca e Salvamento (BBS)",
        "Batalhão de Incêndio Florestal e Emergências Ambientais (BIFEA)",
        "Batalhão de Operações Aéreas (BOA)"
      ]),
      'detalhado',
      opRows[0].id
    ]
  );
  console.log('✓ RO CO atualizado: Diretoria de Planejamento Operacional (DPO)');
}

// Atualizar Diretoria Técnica de RO
// RO tem: COT (Comando de Operações Técnicas) + CATs (Coordenadorias de Atividades Técnicas)
const [tecRows] = await conn.execute('SELECT id FROM technical_directorates WHERE stateId = ?', [stateId]);
if (tecRows.length) {
  await conn.execute(
    'UPDATE technical_directorates SET nomenclature = ?, acronym = ?, attributions = ?, subdivisions = ?, detailLevel = ? WHERE id = ?',
    [
      "Comando de Operações Técnicas",
      "COT",
      "Órgão máximo responsável pelo controle e observância dos requisitos técnicos contra incêndio e pânico das edificações e áreas de risco, competindo-lhe o estudo, a análise, o planejamento, a normatização, a exigência, a fiscalização e a execução das normas que disciplinam a segurança contra incêndio e pânico. (Minuta de Lei de Organização Básica – CBMRO)",
      JSON.stringify([
        "Comandante",
        "Adjunto",
        "Seção Administrativa",
        "Seção de Estudos Técnicos",
        "Seção de Planejamento, Fiscalização e Suporte Técnico",
        "Coordenadorias de Atividades Técnicas (CATs)",
        "Coordenadoria de Projetos de Arquitetura e Engenharia",
        "CAT – Coordenador, Adjunto, Seção Administrativa, Seção de Análise de Projetos, Seção de Investigação e Prevenção de Incêndio, Gerência de Atividades Técnicas (Seção de Vistoria, Seção de Hidrantes)"
      ]),
      'detalhado',
      tecRows[0].id
    ]
  );
  console.log('✓ RO DT atualizado: Comando de Operações Técnicas (COT)');
}

await conn.end();
console.log('\nRondônia atualizado com sucesso!');
