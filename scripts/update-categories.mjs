/**
 * Script para atualizar o campo positionCategory de todos os cargos
 * As categorias agrupam cargos equivalentes entre diferentes estados para permitir comparação
 *
 * Categorias definidas:
 * CO - Comando Operacional
 *   chefe-co          → Chefe/Diretor/Comandante do órgão operacional (nível 1)
 *   adjunto-co        → Adjunto/Subcomandante do órgão operacional (nível 2)
 *   chefe-depto-co    → Chefe de Departamento/Seção subordinado ao CO
 *   chefe-secao-co    → Chefe de Seção/Divisão subordinado ao CO
 *
 * DAT - Diretoria de Atividades Técnicas
 *   chefe-dat         → Chefe/Diretor/Coordenador/Comandante do órgão técnico (nível 1)
 *   adjunto-dat       → Adjunto/Subchefe do órgão técnico (nível 2)
 *   chefe-depto-dat   → Chefe de Departamento/Divisão subordinado à DAT
 *   chefe-secao-dat   → Chefe de Seção/Subseção subordinado à DAT
 */

import mysql from 'mysql2/promise';

const DB_URL = process.env.DATABASE_URL;
if (!DB_URL) {
  console.error('DATABASE_URL not set');
  process.exit(1);
}

const conn = await mysql.createConnection(DB_URL);

// Mapeamento: título → categoria
// Ordem importa: mais específico primeiro
const categoryMap = [
  // ─── Chefes do CO (nível 1) ───────────────────────────────────────────────
  { pattern: /^Comandante Operacional de Bombeiros$/i,             category: 'chefe-co' },
  { pattern: /^Comandante Operacional Bombeiro Militar$/i,         category: 'chefe-co' },
  { pattern: /^Comandante Operacional$/i,                          category: 'chefe-co' },
  { pattern: /^Diretor de Planejamento Operacional$/i,             category: 'chefe-co' },
  { pattern: /^Diretor de Operações$/i,                            category: 'chefe-co' },
  { pattern: /^Diretor Operacional$/i,                             category: 'chefe-co' },
  { pattern: /^Coordenador Operacional$/i,                         category: 'chefe-co' },
  { pattern: /^Chefe do Departamento de Operações$/i,              category: 'chefe-co' },
  { pattern: /^Comandante do Comando de Operações Técnicas$/i,     category: 'chefe-co' },
  { pattern: /^Comandante Regional Bombeiro Militar$/i,            category: 'chefe-co' },

  // ─── Chefes do CO (nível 1) — variantes adicionais ─────────────────────────
  { pattern: /^Comandante Operacional do Corpo de Bombeiros$/i,     category: 'chefe-co' },
  { pattern: /^Comandante de Comando Regional de Bombeiros Militar$/i, category: 'chefe-co' },
  { pattern: /^Comandante Metropolitano de Bombeiros$/i,            category: 'chefe-co' },
  { pattern: /^Comandante Regional de Bombeiro Militar$/i,          category: 'chefe-co' },
  { pattern: /^Comandante Regional de Bombeiros Militar$/i,         category: 'chefe-co' },
  { pattern: /^Coordenador de Operações$/i,                         category: 'chefe-co' },

  // ─── Adjuntos do CO (nível 2) ─────────────────────────────────────────────
  { pattern: /^Adjunto da Diretoria de Planejamento Operacional$/i, category: 'adjunto-co' },
  { pattern: /^Adjunto do Comando de Operações Técnicas$/i,         category: 'adjunto-co' },
  { pattern: /^Assistente do Comando de Operações$/i,               category: 'adjunto-co' },
  { pattern: /^Subcomandante Operacional$/i,                        category: 'adjunto-co' },
  { pattern: /^Subcomandante Operacional de Bombeiros$/i,            category: 'adjunto-co' },
  { pattern: /^Subcomandante Metropolitano de Bombeiros$/i,          category: 'adjunto-co' },
  { pattern: /^Subcomandante Regional de Bombeiro Militar$/i,        category: 'adjunto-co' },
  { pattern: /^Diretor-Adjunto da Diretoria Operacional$/i,          category: 'adjunto-co' },
  { pattern: /^Coordenador de Doutrina e Pesquisa$/i,                category: 'adjunto-co' },
  { pattern: /^Coordenador de Estudos Estratégicos$/i,               category: 'adjunto-co' },

  // ─── Chefes de Departamento/Seção do CO ───────────────────────────────────
  { pattern: /^Chefe do Centro de Operações e Comunicações$/i,     category: 'chefe-depto-co' },
  { pattern: /^Chefe do CIODES\/CBMES$/i,                          category: 'chefe-depto-co' },
  { pattern: /^Chefe do Departamento de Doutrinas$/i,              category: 'chefe-depto-co' },
  { pattern: /^Chefe de Seção do Comando de Operações$/i,          category: 'chefe-secao-co' },

  // ─── Chefes da DAT (nível 1) ─────────────────────────────────────────────
  { pattern: /^Diretor de Atividades Técnicas$/i,                  category: 'chefe-dat' },
  { pattern: /^Diretor de Serviços Técnicos$/i,                    category: 'chefe-dat' },
  { pattern: /^Diretor da Diretoria de Segurança Contra Incêndio e Pânico$/i, category: 'chefe-dat' },
  { pattern: /^Diretor da Diretoria de Segurança Contra Incêndio$/i, category: 'chefe-dat' },
  { pattern: /^Diretor do Departamento de Segurança Contra Incêndio e Pânico$/i, category: 'chefe-dat' },
  { pattern: /^Chefe do Departamento-Geral de Segurança contra Incêndios e Emergências$/i, category: 'chefe-dat' },
  { pattern: /^Chefe do Centro de Atividades Técnicas$/i,          category: 'chefe-dat' },
  { pattern: /^Coordenador de Atividades Técnicas$/i,              category: 'chefe-dat' },
  { pattern: /^Comandante de Atividades Técnicas$/i,               category: 'chefe-dat' },

  // ─── Adjuntos da DAT (nível 2) ───────────────────────────────────────────
  { pattern: /^Subchefe do Centro de Atividades Técnicas$/i,       category: 'adjunto-dat' },
  { pattern: /^Adjunto da Diretoria de Atividades Técnicas$/i,     category: 'adjunto-dat' },
  { pattern: /^Adjunto da Diretoria de Serviços Técnicos$/i,       category: 'adjunto-dat' },
  { pattern: /^Adjunto do Comando de Atividades Técnicas$/i,       category: 'adjunto-dat' },
  { pattern: /^Vice-Diretor de Atividades Técnicas$/i,              category: 'adjunto-dat' },
  { pattern: /^Subdiretor do Departamento de Segurança Contra Incêndio e Pânico$/i, category: 'adjunto-dat' },
  { pattern: /^Subchefe do Departamento-Geral de Segurança contra Incêndios e Emergências$/i, category: 'adjunto-dat' },
  { pattern: /^Diretor-Adjunto da Diretoria de Atividades Técnicas$/i, category: 'adjunto-dat' },

  // ─── Chefes de Departamento/Seção da DAT ─────────────────────────────────
  { pattern: /^Chefe do Departamento de Vistorias e Pareceres$/i,  category: 'chefe-depto-dat' },
  { pattern: /^Chefe do Departamento de Investigação/i,            category: 'chefe-depto-dat' },
  { pattern: /^Chefe de Seção do DGSCI$/i,                         category: 'chefe-depto-dat' },
  { pattern: /^Chefe da Seção de Análise de Projetos$/i,           category: 'chefe-secao-dat' },
  { pattern: /^Chefe da Seção de Vistorias e Fiscalização$/i,      category: 'chefe-secao-dat' },
  { pattern: /^Gerente de Vistorias$/i,                             category: 'chefe-secao-dat' },
  { pattern: /^Gerente de Normas e Cadastros$/i,                    category: 'chefe-secao-dat' },
  { pattern: /^Chefe do Núcleo de Investigação e Prevenção de Incêndios$/i, category: 'chefe-secao-dat' },
  { pattern: /^Coordenador de Projetos de Arquitetura e Engenharia$/i, category: 'chefe-secao-dat' },
  { pattern: /^Chefe do Estado Maior Regional$/i,                   category: 'chefe-secao-co' },
];

// Buscar todos os cargos
const [rows] = await conn.execute('SELECT id, title FROM positions');

let updated = 0;
let unmatched = [];

for (const row of rows) {
  let matched = null;
  for (const { pattern, category } of categoryMap) {
    if (pattern.test(row.title)) {
      matched = category;
      break;
    }
  }

  if (matched) {
    await conn.execute('UPDATE positions SET positionCategory = ? WHERE id = ?', [matched, row.id]);
    updated++;
  } else {
    unmatched.push(row.title);
  }
}

await conn.end();

console.log(`\n✅ Categorias atualizadas: ${updated} cargos`);
if (unmatched.length > 0) {
  console.log(`\n⚠️  Cargos sem categoria (${unmatched.length}):`);
  unmatched.forEach(t => console.log(`  - ${t}`));
}
