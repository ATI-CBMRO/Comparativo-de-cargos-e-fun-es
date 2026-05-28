import mysql from "mysql2/promise";

const db = await mysql.createConnection(process.env.DATABASE_URL);

// Dados completos extraídos dos arquivos de legislação
// Formato: [sigla, legalBasis completo para CO, legalBasis completo para DAT]
// Quando CO e DAT têm a mesma base legal, usamos o mesmo valor para ambos
const legalBasisData = [
  // AL - Decreto 408/2001 regulamenta Lei 6.212/2000
  ["AL", "Lei n.º 6.212, de 26 de dezembro de 2000 (regulamentada pelo Decreto n.º 408, de 08 de novembro de 2001) — Organização Básica do CBMAL"],
  // CE - Lei 13.438/2004
  ["CE", "Lei n.º 13.438, de 07 de janeiro de 2004 — Organização Básica do CBMCE"],
  // DF - Portaria 24/2020 (Regimento Interno)
  ["DF", "Portaria n.º 24, de 25 de novembro de 2020 — Regimento Interno do CBMDF"],
  // ES - Lei Estadual 9.220/2009 (referenciada nas Normas Gerais de Ação)
  ["ES", "Lei Estadual n.º 9.220, de 17 de junho de 2009 — Organização Básica do CBMES"],
  // MA - Lei 8.508/2006
  ["MA", "Lei n.º 8.508, de 27 de novembro de 2006 — Organização Básica do CBMMA"],
  // MG - Lei Complementar 54/1999
  ["MG", "Lei Complementar n.º 54, de 13 de dezembro de 1999 — Organização Básica do CBMMG"],
  // MS - Lei Complementar 188/2014
  ["MS", "Lei Complementar n.º 188, de 3 de abril de 2014 — Organização Básica do CBMMS"],
  // MT - Lei Complementar 775/2023
  ["MT", "Lei Complementar n.º 775, de 27 de setembro de 2023 — Organização Básica do CBMMT"],
  // PA - Lei 11.060/2025
  ["PA", "Lei n.º 11.060, de 1.º de julho de 2025 — Organização Básica e Efetivo do CBMPA"],
  // PB - Lei Complementar 191/2024
  ["PB", "Lei Complementar n.º 191, de 26 de abril de 2024 — Organização Básica do CBMPB"],
  // PE - Lei 15.187/2013
  ["PE", "Lei n.º 15.187, de 12 de dezembro de 2013 — Organização Básica do CBMPE"],
  // PI - Lei 7.772/2022
  ["PI", "Lei n.º 7.772, de 04 de abril de 2022 — Organização Básica do CBMPI"],
  // PR - Lei 22.206/2024
  ["PR", "Lei n.º 22.206, de 29 de novembro de 2024 — Organização Básica do CBMPR"],
  // RJ - Lei 250/1979
  ["RJ", "Lei n.º 250, de 02 de julho de 1979 — Organização Básica do CBMERJ"],
  // RO - Minuta de Projeto de Lei (2025) — ainda não promulgada
  ["RO", "Minuta de Projeto de Lei n.º 0059262482 (abril de 2025) — Organização Básica do CBMRO (em tramitação)"],
  // RS - Decreto 53.897/2018 (regulamenta LC 14.920/2016)
  ["RS", "Decreto n.º 53.897, de 25 de janeiro de 2018 (regulamenta a Lei Complementar n.º 14.920, de 1.º de agosto de 2016) — Organização Básica do CBMRS"],
  // SC - Lei Complementar 724/2018
  ["SC", "Lei Complementar n.º 724, de 18 de julho de 2018 — Organização Básica do CBMSC"],
  // SE - Lei 8.979/2022
  ["SE", "Lei n.º 8.979, de 03 de fevereiro de 2022 — Estrutura Organizacional do CBMSE"],
  // TO - Lei Complementar 131/2021
  ["TO", "Lei Complementar n.º 131, de 30 de setembro de 2021 — Organização Básica do CBMTO"],
];

let updated = 0;
let errors = 0;

for (const [sigla, legalBasis] of legalBasisData) {
  try {
    // Buscar o state_id
    const [rows] = await db.execute("SELECT id FROM states WHERE sigla = ?", [sigla]);
    if (!rows.length) {
      console.log(`AVISO: Estado ${sigla} não encontrado`);
      continue;
    }
    const stateId = rows[0].id;

    // Atualizar operational_commands
    const [ocResult] = await db.execute(
      "UPDATE operational_commands SET legalBasis = ? WHERE stateId = ?",
      [legalBasis, stateId]
    );

    // Atualizar technical_directorates
    const [tdResult] = await db.execute(
      "UPDATE technical_directorates SET legalBasis = ? WHERE stateId = ?",
      [legalBasis, stateId]
    );

    console.log(`✓ ${sigla}: CO(${ocResult.affectedRows}) TD(${tdResult.affectedRows}) — ${legalBasis.substring(0, 60)}...`);
    updated++;
  } catch (err) {
    console.error(`✗ ${sigla}: ${err.message}`);
    errors++;
  }
}

await db.end();
console.log(`\nConcluído: ${updated} estados atualizados, ${errors} erros.`);
