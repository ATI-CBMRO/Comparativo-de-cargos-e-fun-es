# Consulta da Minuta do Regulamento de Serviço — pacote para o SEI (2026-09-11)

**Desde 2026-09-14 o pacote é gerado pelo próprio portal**: menu do admin → Regulamento Geral →
"Pacote da consulta (.docx)" (`/regulamento/servico/consulta`). Os quatro botões (minuta em
consulta, relatório das interações, quadro de análise com os pareceres ✅/⛔ e textos finais do
portal, minuta reestruturada) usam a mesma lógica dos scripts abaixo (`src/lib/consultaRelatorios.js`,
`consultaDocx.js`, `regulamentoReestruturado.js`). Os scripts continuam valendo para gerar a pasta
sem navegador (a partir da exportação do Firestore).

Arquivos desta pasta e como regenerá-los (todos os comandos a partir da raiz do repositório).

| Arquivo | O que é | Como gerar |
|---|---|---|
| `Minuta_Regulamento_de_Servico_CBMRO_versao_em_consulta.docx` | A minuta exatamente como o militar com acesso "Só Regulamento de Serviço" a vê no portal (`/regulamento/servico`, cenário LOB vigente): 7 capítulos, 171 artigos, numeração contínua. | `node scripts/gerar_docx_regulamento_servico.mjs [--finals .firestore-export/fs_finalTexts.json]` |
| `Minuta_Regulamento_de_Servico_CBMRO_reestruturada_parte_geral_e_especial.docx` | Os MESMOS 171 artigos reordenados na estrutura sugerida pelo Cel. Luiz Eduardo (o mesmo autor das 271 sugestões): Parte I (Geral, comum aos dois serviços), Parte II (Especial — Título I Serviço Operacional, Título II Serviço Técnico), Parte III (Finais). Anexo I: de-para de numeração. Anexo II: ajustes de redação que a nova ordem exige (não aplicados). | `node scripts/gerar_docx_regulamento_reestruturado.mjs [--finals ...]` |
| `depara_reestruturacao.json` | O de-para do Anexo I em JSON (para a consolidação final da numeração). | idem |
| `Relatorio_Interacoes_Consulta_Regulamento_de_Servico.docx` | Relatório das sugestões recebidas (autor, nome de guerra, unidade, dispositivo, trecho, texto) para anexar ao SEI. | 1) exportar o Firestore: `$env:FB_EMAIL='...'; $env:FB_SENHA='...'; node scripts/exportar_firestore.mjs; Remove-Item Env:FB_SENHA` 2) `node scripts/gerar_sei_interacoes.mjs [--desde AAAA-MM-DD]` |
| `interacoes_consulta.md` / `.json` | Mesmas interações em tabela Markdown / JSON (base da análise de mérito). | idem |
| `Comparativo_Consulta_Regulamento_de_Servico.docx` | Versão em consulta × versão atual, artigo a artigo (curadoria de 14/09: 20 corrigidos nas duas, 7 com texto final, 15 reescritos, 6 novos, 8 suprimidos, 3 propostas pendentes de deliberação). | tela "Comparativo da consulta" ou botão 5 do Pacote |
| `Quadro_Analise_Aplicacao_Regulamento_de_Servico.docx` | Sugestões agrupadas por artigo com o parecer registrado no portal (relevante / descartada / sem parecer) e a situação do texto final (redigido / conferido / suprimido / em aberto). | idem (mesmo comando do relatório) |
| `Analise_Interacoes_e_Proposta_de_Aplicacao.docx` / `.md` | Análise de mérito das 322 interações (14 blocos do Cel. Luiz Eduardo + situação dos registros da equipe), convergência com a estrutura em Parte Geral/Especial sugerida pelo mesmo oficial, e plano de aplicação em 7 passos (decisões do CONDEG, aplicação direta, conferências, redação nova, saneamento dos textos finais). | editar o `.md` e rodar `node scripts/md_para_docx.mjs <md> <docx> "<subtítulo>"` |

Estado da exportação usada (11/09/2026 14h50): 345 sugestões (322 no recorte: 271 do Cel. Luiz
Eduardo, 51 da equipe), 95 textos finais (94 fechados — 53 sem texto, 13 "Excluir"). Nos .docx,
"fechado sem texto" mantém o original e "Excluir" aparece como dispositivo suprimido.

A exportação fica em `.firestore-export/` (ignorada pelo git — contém e-mails dos membros) e
exige credencial de membro do portal; a credencial entra só por variável de ambiente e não é
gravada. As regras do Firestore limitam `members` ao admin: sem admin, o relatório sai sem
nome de guerra/unidade (só o nome gravado na sugestão).

Os artigos são identificados sempre pelo endereço estável `editId#index` (ex.:
`reg:atual:servico-operacional/se-art-24#caput`); o número "Art. N" é o da versão em
consulta e muda a cada reordenação.
