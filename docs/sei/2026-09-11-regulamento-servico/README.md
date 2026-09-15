# Consulta da Minuta do Regulamento de Serviço — pacote para o SEI (2026-09-11)

**Desde 2026-09-14 o pacote é gerado pelo próprio portal**: menu do admin → Regulamento Geral →
"Pacote da consulta (.docx)" (`/regulamento/servico/consulta`). Os cinco botões (minuta em
consulta, relatório das interações, quadro de análise com os pareceres ✅/⛔ e textos finais do
portal, minuta publicável em Parte Geral/Especial, comparativo) usam a mesma lógica dos scripts
abaixo (`src/lib/consultaRelatorios.js`, `consultaDocx.js`, `regulamentoReestruturado.js`,
`formatacaoTexto.js`). O quadro de dispositivos semelhantes (15/09) foi eliminado por decisão:
dos 6 grupos, 1 foi aplicado (casos omissos, `DELIBERACOES_SEMELHANTES`) e 5 ficam como estão. Os scripts continuam valendo para gerar a pasta
sem navegador (a partir da exportação do Firestore).

Arquivos desta pasta e como regenerá-los (todos os comandos a partir da raiz do repositório).

| Arquivo | O que é | Como gerar |
|---|---|---|
| `Minuta_Regulamento_de_Servico_CBMRO_versao_em_consulta.docx` | A minuta exatamente como o militar com acesso "Só Regulamento de Serviço" a leu no portal (`/regulamento/servico`, cenário LOB vigente): 7 capítulos, 171 artigos, numeração contínua, sem as correções posteriores (estas ficam na versão atual e no Comparativo). | `node scripts/gerar_docx_regulamento_servico.mjs [--finals .firestore-export/fs_finalTexts.json]` |
| `Minuta_Regulamento_de_Servico_CBMRO_parte_geral_e_especial.docx` | **Minuta publicável** (15/09): a versão ATUAL (169 artigos) na estrutura Parte I (Geral, comum aos dois serviços), Parte II (Especial — Título I Serviço Operacional, Título II Serviço Técnico), Parte III (Finais). Sem autoria da estrutura, sem texto introdutório, sem anexos, sem selos de curadoria; primeira letra de cada frase em maiúscula (`capitalizarFrases`). Artigos reescritos entram no lugar dos antigos, os novos após a âncora, os suprimidos não aparecem. | `node scripts/gerar_docx_regulamento_reestruturado.mjs` |
| `depara_reestruturacao.json` | De-para de numeração (minuta publicável ↔ versão em consulta) em JSON, para a consolidação final. | idem |
| `Relatorio_Interacoes_Consulta_Regulamento_de_Servico.docx` | Relatório das sugestões recebidas dos **militares consultados** (autor, nome de guerra, unidade, dispositivo, trecho, texto) para anexar ao SEI, com a coluna **Aplicação** — o que a versão atual da minuta fez com o artigo comentado (reescrito / artigo novo / alterado / suprimido / mantido). Registros das contas de administração do portal são revisão interna, incorporada à versão atual, e não constam. | 1) exportar o Firestore: `$env:FB_EMAIL='...'; $env:FB_SENHA='...'; node scripts/exportar_firestore.mjs; Remove-Item Env:FB_SENHA` 2) `node scripts/gerar_sei_interacoes.mjs [--desde AAAA-MM-DD]` |
| `interacoes_consulta.md` / `.json` | Mesmas interações em tabela Markdown / JSON, com a aplicação de cada uma (base da análise de mérito). | idem |
| `Comparativo_Consulta_Regulamento_de_Servico.docx` | Versão em consulta (o texto lido) × versão atual, artigo a artigo (19 com correção de texto, 11 com texto alterado, 15 reescritos, 7 novos, 11 suprimidos, 3 propostas pendentes de deliberação). | `node scripts/gerar_docx_regulamento_servico.mjs` (sai junto com a minuta), tela "Comparativo da consulta" ou botão 5 do Pacote |
| `Quadro_Analise_Aplicacao_Regulamento_de_Servico.docx` | Sugestões agrupadas por artigo com a aplicação na versão atual, o parecer registrado no portal (relevante / descartada / sem parecer) e a situação do texto final (redigido / conferido / suprimido / em aberto). | idem (mesmo comando do relatório) |
| `Analise_Interacoes_e_Proposta_de_Aplicacao.docx` / `.md` | Análise de mérito das 271 interações (14 blocos do Cel. Luiz Eduardo), a revisão de texto incorporada à versão atual, convergência com a estrutura em Parte Geral/Especial sugerida pelo mesmo oficial, e plano de aplicação em 7 passos (decisões do CONDEG, aplicação direta, conferências, redação nova, saneamento dos textos finais). | editar o `.md` e rodar `node scripts/md_para_docx.mjs <md> <docx> "<subtítulo>"` |

Estado da exportação usada (11/09/2026 14h50): 345 registros na coleção `suggestions`, dos
quais 271 são sugestões dos militares consultados sobre o recorte (todas do Cel. Luiz Eduardo);
os demais são registros das contas de administração do portal (revisão interna, incorporada à
versão atual, fora do relatório) e do Regimento Interno. 95 textos finais (94 fechados — 53 sem
texto, 13 "Excluir"). Nos .docx, "fechado sem texto" mantém o original e "Excluir" aparece como
dispositivo suprimido.

Aplicação na versão atual (14/09/2026): as 271 sugestões recaem sobre artigos alterados — 197
sobre artigos reescritos (competências do CBMRO, COB, GBM, SGBM, objetivos e política) e 74
sobre o Bloco 14, que entrou como 6 artigos novos (3 deles propostas pendentes de deliberação
do CONDEG). A revisão de texto da administração (correções, textos finais, supressões) está
descrita na seção 3 da análise e aparece no Comparativo, sem autoria.

A exportação fica em `.firestore-export/` (ignorada pelo git — contém e-mails dos membros) e
exige credencial de membro do portal; a credencial entra só por variável de ambiente e não é
gravada. As regras do Firestore limitam `members` ao admin: sem admin, o relatório sai sem
nome de guerra/unidade (só o nome gravado na sugestão).

Os artigos são identificados sempre pelo endereço estável `editId#index` (ex.:
`reg:atual:servico-operacional/se-art-24#caput`); o número "Art. N" é o da versão em
consulta e muda a cada reordenação.
