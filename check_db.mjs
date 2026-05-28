import mysql from 'mysql2/promise';

const DB_URL = process.env.DATABASE_URL;
if (!DB_URL) {
  console.error('DATABASE_URL não encontrado');
  process.exit(1);
}

const url = new URL(DB_URL);
const conn = await mysql.createConnection({
  host: url.hostname,
  port: parseInt(url.port || '3306'),
  user: url.username,
  password: url.password,
  database: url.pathname.replace('/', ''),
  ssl: { rejectUnauthorized: false }
});

const [rows] = await conn.execute(
  'SELECT oc.id, s.sigla, oc.nomenclature, oc.acronym, oc.subdivisions FROM operational_commands oc JOIN states s ON s.id = oc.stateId ORDER BY s.sigla'
);
console.log('=== COMANDOS OPERACIONAIS ===');
rows.forEach(r => console.log(r.sigla, r.acronym, '|', r.nomenclature, '| subs:', r.subdivisions ? 'SIM' : 'NAO'));

const [rows2] = await conn.execute(
  'SELECT td.id, s.sigla, td.nomenclature, td.acronym, td.subdivisions FROM technical_directorates td JOIN states s ON s.id = td.stateId ORDER BY s.sigla'
);
console.log('\n=== DIRETORIAS TÉCNICAS ===');
rows2.forEach(r => console.log(r.sigla, r.acronym, '|', r.nomenclature, '| subs:', r.subdivisions ? 'SIM' : 'NAO'));

await conn.end();
console.log('\nTotal CO:', rows.length, '| Total DT:', rows2.length);
