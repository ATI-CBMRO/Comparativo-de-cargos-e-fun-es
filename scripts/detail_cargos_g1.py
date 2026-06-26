# detail_cargos_g1.py — Cargos detalhados (subordinação, desdobramentos, atribuições)
# Estados: AL, AP, AM. Chaveado por id de órgão existente em detail_data_g1.
# Extraído fielmente das legislações.

CARGOS = {

# ── ALAGOAS (Decreto nº 408/2001 — Regimento Interno) ──
"al": {
  "cg-al": [
    {"cargo": "Comandante Geral", "subordinadoA": "Governador do Estado / Secretário de Defesa Social", "requisito": "Oficial Superior do último posto (Coronel QOBM/COMB)",
     "desdobramentos": ["Subcomandante Geral", "Conselho de Políticas Estratégicas", "Gabinete do Comandante Geral", "Corregedoria Geral", "Diretorias", "Comando Operacional de Bombeiros"],
     "atribuicoes": [
       "Assessorar o Governador do Estado nos assuntos relacionados com as atividades bombeiro militar e ações de defesa civil (Art. 8º, I)",
       "Assessorar o Secretário de Defesa Social nos assuntos de Segurança Pública relacionados com a competência da Corporação (II)",
       "Dirigir as atividades técnicas, operacionais e administrativas da Corporação (III)",
       "Fazer cumprir as leis, normas e regulamentos da Corporação (IV)",
       "Baixar portarias e ordens de serviços (V)",
       "Aplicar penas disciplinares de sua alçada (VI)",
       "Autorizar despesas, nos limites de sua competência (VII)",
       "Submeter ao Governador e ao Secretário de Defesa Social os planos, estudos, programas, projetos e propostas para organização, funcionamento e atuação do CBM (VIII)",
       "Exercer a supervisão superior dos órgãos de direção, de apoio e de execução, orientando e controlando seu funcionamento (IX)",
       "Desempenhar as funções de Coordenador Estadual de Defesa Civil (X)",
       "Desempenhar outras atribuições correlatas (XI)"
     ]},
  ],
  "scg-al": [
    {"cargo": "Subcomandante Geral", "subordinadoA": "Comandante Geral", "requisito": "Oficial Superior (Coronel/Tenente-Coronel QOBM/COMB)",
     "desdobramentos": ["Órgãos de direção, de apoio e de execução"],
     "atribuicoes": [
       "Responder pelo Comandante Geral em seus impedimentos eventuais (Art. 9º, I)",
       "Assegurar-se que as ordens específicas estão sendo cumpridas, de acordo com os objetivos da Corporação (II)",
       "Exercer o controle disciplinar dos integrantes da Corporação (III)",
       "Apresentar propostas ou emitir pareceres sobre os assuntos administrativos e operacionais que devam ser apreciados pelo Comandante Geral (IV)",
       "Determinar os implementos ao cumprimento das decisões do Conselho de Políticas Estratégicas (V)",
       "Coordenar e elaborar o relatório anual de atividades do CBM/AL (VI)",
       "Secundar o Comandante Geral na fiscalização das atividades da Corporação (VII)",
       "Dar conhecimento aos órgãos de direção, de apoio e de execução das decisões tomadas pelo Comandante Geral (VIII)",
       "Exercer outros encargos previstos em leis e regulamentos ou atribuídos pelo Comandante Geral (IX)",
       "Dar conhecimento ao Comandante Geral dos fatos e atos a respeito dos quais tenha providenciado por iniciativa própria (X)",
       "Coordenar as atividades, tarefas e trabalhos dos órgãos que integram o Conselho de Políticas Estratégicas (XI)"
     ]},
  ],
  "gabinete-al": [
    {"cargo": "Chefe do Gabinete do Comando Geral", "subordinadoA": "Comandante-Geral", "requisito": "Tenente-Coronel QOBM/COMB", "desdobramentos": ["Ajudância de Ordens", "Assessoria de Inteligência e Contra-Inteligência", "Assessoria de Relações Públicas e Comunicação Social", "Secretaria Administrativa"], "atribuicoes": ["Assistência e assessoramento direto ao Comandante Geral"]},
    {"cargo": "Ajudante de Ordens do Comandante Geral", "subordinadoA": "Comandante-Geral", "requisito": "Capitão QOBM/COMB", "desdobramentos": [], "atribuicoes": []},
    {"cargo": "Chefe da Assessoria de Inteligência e Contra-Inteligência", "subordinadoA": "Comandante-Geral", "requisito": "Major QOBM/COMB", "desdobramentos": [], "atribuicoes": []},
    {"cargo": "Chefe da Assessoria de Relações Públicas e Comunicação Social", "subordinadoA": "Comandante-Geral", "requisito": "Tenente-Coronel QOBM/COMB", "desdobramentos": ["Subseção de Imprensa e Marketing", "Subseção de Relações Públicas, Publicidade e Propaganda"], "atribuicoes": ["Direção das atividades de comunicação social"]},
  ],
  "corregedoria-al": [
    {"cargo": "Corregedor Geral", "subordinadoA": "Comandante-Geral", "requisito": "Coronel QOBM/COMB", "desdobramentos": ["Subcorregedoria", "Ouvidoria", "Seção de Polícia Disciplinar", "Seção de Polícia Judiciária Militar", "Seção de Apoio Administrativo", "Seção de Inteligência"], "atribuicoes": ["Fiscalização disciplinar e apuração de desvios de conduta"]},
    {"cargo": "Subcorregedor Geral", "subordinadoA": "Corregedor Geral", "requisito": "Tenente-Coronel QOBM/COMB", "desdobramentos": [], "atribuicoes": []},
    {"cargo": "Ouvidor Geral", "subordinadoA": "Corregedor Geral", "requisito": "Tenente-Coronel QOBM/COMB", "desdobramentos": ["Sub-Ouvidor Geral", "Assistente da Ouvidoria"], "atribuicoes": ["Ouvidoria da Corporação"]},
    {"cargo": "Chefe da Seção de Polícia Disciplinar", "subordinadoA": "Corregedor Geral", "requisito": "1º Tenente QOBM/COMB", "desdobramentos": [], "atribuicoes": []},
    {"cargo": "Chefe da Seção de Polícia Judiciária Militar", "subordinadoA": "Corregedor Geral", "requisito": "1º Tenente QOBM/COMB", "desdobramentos": [], "atribuicoes": []},
    {"cargo": "Chefe da Seção de Inteligência", "subordinadoA": "Corregedor Geral", "requisito": "Major QOBM/COMB", "desdobramentos": [], "atribuicoes": []},
  ],
  "drh-al": [
    {"cargo": "Diretor de Recursos Humanos", "subordinadoA": "Comando Geral", "requisito": "Coronel QOBM/COMB", "desdobramentos": ["Seção de Seleção e Ingresso", "Seção de Cadastro, Avaliação, Controle e Movimentação", "Seção de Desenvolvimento de RH", "Seção de Promoções", "Seção de Pagamento de Pessoal", "Seção de Inativos e Pensionistas", "Seção de Identificação", "Seção de Expediente e Arquivo", "Seção de Legislação"], "atribuicoes": ["Planejamento, controle e fiscalização das atividades de pessoal"]},
    {"cargo": "Chefe da Seção de Seleção e Ingresso de RH", "subordinadoA": "Diretor de Recursos Humanos", "requisito": "Tenente-Coronel QOBM/COMB", "desdobramentos": [], "atribuicoes": []},
    {"cargo": "Chefe da Seção de Cadastro, Avaliação, Controle e Movimentação", "subordinadoA": "Diretor de Recursos Humanos", "requisito": "Tenente-Coronel QOBM/COMB", "desdobramentos": [], "atribuicoes": []},
    {"cargo": "Chefe da Seção de Desenvolvimento de RH", "subordinadoA": "Diretor de Recursos Humanos", "requisito": "Major QOBM/COMB", "desdobramentos": [], "atribuicoes": []},
    {"cargo": "Chefe da Seção de Promoções", "subordinadoA": "Diretor de Recursos Humanos", "requisito": "Capitão QOBM/COMB", "desdobramentos": [], "atribuicoes": []},
    {"cargo": "Chefe da Seção de Pagamento de Pessoal", "subordinadoA": "Diretor de Recursos Humanos", "requisito": "Major QOBM/ADM", "desdobramentos": [], "atribuicoes": []},
    {"cargo": "Chefe da Seção de Inativos e Pensionistas", "subordinadoA": "Diretor de Recursos Humanos", "requisito": "Major QOBM/ADM", "desdobramentos": [], "atribuicoes": []},
    {"cargo": "Chefe da Seção de Identificação", "subordinadoA": "Diretor de Recursos Humanos", "requisito": "Capitão QOBM/COMB", "desdobramentos": [], "atribuicoes": []},
  ],
  "dmp-al": [
    {"cargo": "Diretor de Material e Patrimônio", "subordinadoA": "Comando Geral", "requisito": "Coronel QOBM/COMB", "desdobramentos": ["Seção de Aquisições e Gestão de Contratos e Convênios", "Seção de Apoio a CPL", "Seção de Administração da Frota", "Seção de Cadastro, Controle e Alienação", "Seção de Administração, Expediente e Arquivo", "Seção de Estatística"], "atribuicoes": ["Controle de material e patrimônio; planejamento logístico"]},
    {"cargo": "Chefe da Seção de Aquisições e Gestão de Contratos e Convênios", "subordinadoA": "Diretor de Material e Patrimônio", "requisito": "Tenente-Coronel QOBM/COMB", "desdobramentos": ["Subseção de Gestão de Contratos e Convênios", "Subseção de Aquisições"], "atribuicoes": []},
    {"cargo": "Chefe da Seção de Cadastro, Controle e Alienação", "subordinadoA": "Diretor de Material e Patrimônio", "requisito": "Major QOBM/ADM", "desdobramentos": ["Subseção de Cadastro de Patrimônio", "Subseção de Cadastro e Controle de Material Bélico"], "atribuicoes": []},
  ],
  "df-al": [
    {"cargo": "Diretor de Finanças", "subordinadoA": "Comando Geral", "requisito": "Tenente-Coronel QOBM/COMB", "desdobramentos": ["Seção de Administração Financeira", "Seção de Contabilidade e Auditoria", "Seção de Expediente e Arquivo", "Tesouraria Geral"], "atribuicoes": ["Gestão orçamentária e financeira"]},
    {"cargo": "Chefe da Seção de Administração Financeira", "subordinadoA": "Diretor de Finanças", "requisito": "Major QOBM/COMB", "desdobramentos": ["Subseção de Controle e Execução Orçamentária"], "atribuicoes": []},
    {"cargo": "Chefe da Seção de Contabilidade e Auditoria", "subordinadoA": "Diretor de Finanças", "requisito": "Major QOBM/ADM", "desdobramentos": [], "atribuicoes": []},
    {"cargo": "Tesoureiro Geral", "subordinadoA": "Diretor de Finanças", "requisito": "1º Tenente QOBM/ADM", "desdobramentos": [], "atribuicoes": []},
  ],
  "dst-al": [
    {"cargo": "Diretor de Atividades Técnicas", "subordinadoA": "Comando Geral", "requisito": "Coronel QOBM/COMB", "desdobramentos": ["Seção de Estudos e Análises de Projetos", "Seção de Testes, Vistorias e Pareceres", "Seção de Perícias e Pesquisas", "Seção de Hidrantes", "Seção de Expediente e Arquivo"], "atribuicoes": ["Prevenção e segurança contra incêndio"]},
    {"cargo": "Chefe da Seção de Estudos e Análises de Projetos", "subordinadoA": "Diretor de Atividades Técnicas", "requisito": "Tenente-Coronel QOBM/COMB", "desdobramentos": [], "atribuicoes": []},
    {"cargo": "Chefe da Seção de Testes, Vistorias e Pareceres", "subordinadoA": "Diretor de Atividades Técnicas", "requisito": "Major QOBM/COMB", "desdobramentos": [], "atribuicoes": []},
    {"cargo": "Chefe da Seção de Perícias e Pesquisas", "subordinadoA": "Diretor de Atividades Técnicas", "requisito": "Major QOBM/COMB", "desdobramentos": [], "atribuicoes": []},
    {"cargo": "Chefe da Seção de Hidrantes", "subordinadoA": "Diretor de Atividades Técnicas", "requisito": "1º Tenente QOBM/ADM", "desdobramentos": [], "atribuicoes": []},
  ],
  "policlinica-al": [
    {"cargo": "Diretor (Centro de Assistência)", "subordinadoA": "Comando Geral", "requisito": "Coronel QOBM/S", "desdobramentos": ["Subdiretor", "Junta de Inspeção de Saúde", "Serviço de Clínica Médica", "Serviço Odontológico", "Serviço de Enfermaria", "Serviço de Farmácia", "Serviço de Capelania", "Serviço de Assistência Psicossocial"], "atribuicoes": ["Assistência e saúde do pessoal"]},
    {"cargo": "Subdiretor", "subordinadoA": "Diretor (Centro de Assistência)", "requisito": "Tenente-Coronel QOBM/S", "desdobramentos": [], "atribuicoes": []},
    {"cargo": "Presidente da Junta de Inspeção de Saúde", "subordinadoA": "Diretor (Centro de Assistência)", "requisito": "Tenente-Coronel QOBM/S", "desdobramentos": [], "atribuicoes": []},
    {"cargo": "Chefe do Serviço de Clínica Médica e Atendimento Ambulatorial", "subordinadoA": "Diretor (Centro de Assistência)", "requisito": "Major QOBM/S", "desdobramentos": [], "atribuicoes": []},
    {"cargo": "Chefe do Serviço Odontológico", "subordinadoA": "Diretor (Centro de Assistência)", "requisito": "Major QOBM/S", "desdobramentos": [], "atribuicoes": []},
    {"cargo": "Chefe do Serviço de Enfermaria", "subordinadoA": "Diretor (Centro de Assistência)", "requisito": "Tenente-Coronel QOBM/S", "desdobramentos": [], "atribuicoes": []},
    {"cargo": "Chefe do Serviço de Capelania", "subordinadoA": "Diretor (Centro de Assistência)", "requisito": "Capitão QOBM/CAP", "desdobramentos": [], "atribuicoes": []},
  ],
  "ag-al": [
    {"cargo": "Ajudante Geral", "subordinadoA": "Comando Geral", "requisito": "Tenente-Coronel ou Capitão QOBM/COMB", "desdobramentos": ["Secretaria Geral", "Seção Administrativa", "Seção de Comando e Serviço", "Protocolo Geral", "Arquivo Geral", "Biblioteca Geral", "Banda de Música"], "atribuicoes": ["Funções administrativas do Comando Geral"]},
    {"cargo": "Secretário Geral", "subordinadoA": "Ajudante Geral", "requisito": "Major QOBM/COMB", "desdobramentos": [], "atribuicoes": []},
    {"cargo": "Chefe da Seção de Comando e Serviço", "subordinadoA": "Ajudante Geral", "requisito": "Capitão QOBM/COMB", "desdobramentos": ["Sargenteação", "Subseção de Segurança do QCG"], "atribuicoes": []},
    {"cargo": "Regente da Banda de Música", "subordinadoA": "Ajudante Geral", "requisito": "Major QOBM/MUS", "desdobramentos": ["Seção de Administração", "Seção de Editoração e Arranjo", "Seção de Bens e Patrimônio"], "atribuicoes": []},
  ],
  "cpet-al": [
    {"cargo": "Conselho de Políticas Estratégicas", "subordinadoA": "Comandante-Geral", "requisito": "Colegiado (CG, SCG, Chefe de Gabinete, Diretores, Corregedor, Ajudante Geral e Cmt. Operacional)", "desdobramentos": [], "atribuicoes": ["Assessoramento no planejamento, coordenação e fiscalização", "Propor medidas de aperfeiçoamento das atividades técnicas especializadas"]},
  ],
  "cob-al": [
    {"cargo": "Comandante Operacional de Bombeiros", "subordinadoA": "Subcomandante Geral", "requisito": "Tenente-Coronel QOBM/COMB", "desdobramentos": ["Seção de Planejamento e Avaliação Operacional", "Seção de Administração", "Centro de Operações e Comunicações"], "atribuicoes": ["Coordenação operacional e execução das atividades-fins"]},
    {"cargo": "Chefe do Centro de Operações e Comunicações", "subordinadoA": "Comandante Operacional de Bombeiros", "requisito": "Major QOBM/COMB", "desdobramentos": ["Subseção de Rádio Operador e Despacho", "Subseção de Operadores de Tele Atendimento"], "atribuicoes": []},
  ],
  "cg-al-lob": [
    {"cargo": "Comandante Geral", "subordinadoA": "Governador do Estado", "requisito": "Oficial da ativa, do último posto do Quadro de Combatentes, com o Curso Superior de Bombeiro Militar ou equivalente (Art. 7º)",
     "desdobramentos": ["Gabinete do Comandante Geral", "Subcomando Geral", "Conselho de Políticas Estratégicas", "Coordenadoria Estadual de Defesa Civil", "Corregedoria Geral", "Diretorias", "Secretaria Geral", "Comissões"],
     "atribuicoes": [
       "Assessorar ao Governador do Estado nos assuntos relacionados com as atividades bombeiro-militar e ações de defesa civil (Art. 8º, I)",
       "Assessorar ao Secretário de Defesa Social nos assuntos de Segurança Pública, relacionados com a competência da Corporação (II)",
       "Dirigir as atividades técnicas, operacionais e administrativas da corporação (III)",
       "Fazer cumprir as leis, normas e regulamentos da Corporação (IV)",
       "Baixar portarias e ordens de serviços (V)",
       "Aplicar penas disciplinares de sua alçada (VI)",
       "Autorizar despesas, nos limites de sua competência (VII)",
       "Submeter ao Governador do Estado os planos, estudos, programas, projetos e propostas para a organização, funcionamento e atuação do Corpo de Bombeiros Militar (VIII)",
       "Exercer a supervisão superior dos órgãos de direção, de apoio e de execução, orientando e controlando o respectivo funcionamento (IX)",
       "Desempenhar as funções de Secretário Estadual de Defesa Civil (X)",
       "Desempenhar outras atribuições correlatas (XI)"
     ]},
  ],
},

# ── AMAPÁ (LC nº 180/2026) — sem detalhamento de cargos individuais na lei;
#    registrados os dirigentes e atribuições gerais por órgão. ──
"ap": {
  "cg-ap": [
    {"cargo": "Comandante-Geral", "subordinadoA": "Governador do Estado", "requisito": "Coronel do Quadro de Oficiais de Estado-Maior; honras de Secretário de Estado", "desdobramentos": ["Subcomandante-Geral", "Órgãos de Direção, Assessoramento, Apoio, Execução e Correição"], "atribuicoes": ["Comando e administração geral da Corporação"]},
  ],
  "scg-ap": [
    {"cargo": "Subcomandante-Geral", "subordinadoA": "Comandante-Geral", "requisito": "Coronel do Quadro de Oficiais de Estado-Maior; honras de Secretário de Estado Adjunto", "desdobramentos": [], "atribuicoes": ["Substituição do Comandante-Geral em impedimentos", "Assessoramento ao Comandante-Geral"]},
  ],
  "diretorias-ap": [
    {"cargo": "Diretor de Inteligência", "subordinadoA": "Subcomandante-Geral", "requisito": "", "desdobramentos": [], "atribuicoes": ["Gestão de inteligência"]},
    {"cargo": "Diretor de Recursos Humanos", "subordinadoA": "Subcomandante-Geral", "requisito": "", "desdobramentos": [], "atribuicoes": ["Gestão de recursos humanos"]},
    {"cargo": "Diretor de Pesquisa e Desenvolvimento", "subordinadoA": "Subcomandante-Geral", "requisito": "", "desdobramentos": [], "atribuicoes": ["Pesquisa e desenvolvimento"]},
    {"cargo": "Diretor de Gestão Orçamentária e Financeira", "subordinadoA": "Subcomandante-Geral", "requisito": "", "desdobramentos": [], "atribuicoes": ["Gestão orçamentária e financeira"]},
    {"cargo": "Diretor Ambiental", "subordinadoA": "Subcomandante-Geral", "requisito": "", "desdobramentos": [], "atribuicoes": ["Gestão ambiental"]},
  ],
  "corregedoria-ap": [
    {"cargo": "Corregedor-Geral", "subordinadoA": "Comandante-Geral", "requisito": "", "desdobramentos": [], "atribuicoes": ["Órgão de correição com atuação desconcentrada, destinado a exercer as funções de Corregedoria-Geral, mediante regulamentação de procedimentos internos, para a prevenção, fiscalização e apuração dos desvios de conduta em atos disciplinares e penais militares, a promoção da qualidade e eficiência do serviço de segurança pública e a instrumentalização da Justiça Militar (LC nº 180/2026, Art. 6º, §5º)"]},
  ],
  "gabinete-ap": [
    {"cargo": "Chefe do Gabinete do Comandante-Geral", "subordinadoA": "Comandante-Geral", "requisito": "Oficial Superior do CBMAP", "desdobramentos": ["Gabinete do Subcomandante-Geral"], "atribuicoes": ["Órgão de direção-geral, responsável pelo assessoramento direto ao Comandante-Geral e pelo apoio à direção superior, planejamento estratégico e administração geral da Instituição (LC nº 180/2026, Art. 6º, §1º, I)"]},
  ],
  "cdoem-ap": [
    {"cargo": "Presidente do Comitê de Desenvolvimento Organizacional", "subordinadoA": "Comandante-Geral", "requisito": "Oficial Superior do CBMAP", "desdobramentos": [], "atribuicoes": ["Órgão de direção-geral, responsável pelo planejamento e gestão do desenvolvimento organizacional da Corporação, integrando os órgãos incumbidos da direção superior, planejamento estratégico e administração geral da Instituição (LC nº 180/2026, Art. 6º, §1º, I)"]},
  ],
  "comando-operacional-ap": [
    {"cargo": "Comandante Operacional", "subordinadoA": "Comandante-Geral", "requisito": "Oficial Superior do CBMAP", "desdobramentos": [], "atribuicoes": ["Órgão de direção-geral, responsável pela coordenação das atividades operacionais de bombeiro militar do Estado do Amapá, integrando os órgãos incumbidos da direção superior, planejamento estratégico e administração geral da Instituição (LC nº 180/2026, Art. 6º, §1º, I)"]},
  ],
  "frcb-ap": [
    {"cargo": "Gestor do Fundo de Reequipamento do Corpo de Bombeiros", "subordinadoA": "Comandante-Geral", "requisito": "Oficial Superior do CBMAP", "desdobramentos": [], "atribuicoes": ["Órgão de direção-geral, responsável pela gestão do Fundo de Reequipamento do Corpo de Bombeiros, integrando os órgãos incumbidos da direção superior, planejamento estratégico e administração geral da Instituição (LC nº 180/2026, Art. 6º, §1º, I)"]},
  ],
  "aci-ap": [
    {"cargo": "Assessor de Controle Interno", "subordinadoA": "Comandante-Geral", "requisito": "Oficial do CBMAP", "desdobramentos": [], "atribuicoes": ["Órgão de assessoramento destinado a prestar assessoria, consultoria, recomendação e orientação técnica e política e a expedir nota técnica para auxiliar as decisões dos órgãos de direção em assuntos especializados de controle interno (LC nº 180/2026, Art. 6º, §2º)"]},
  ],
  "aj-ap": [
    {"cargo": "Assessor Jurídico", "subordinadoA": "Comandante-Geral", "requisito": "Oficial do CBMAP (preferencialmente bacharel em Direito)", "desdobramentos": [], "atribuicoes": ["Órgão de assessoramento destinado a prestar assessoria, consultoria, recomendação e orientação técnica e política e a expedir nota técnica para auxiliar as decisões dos órgãos de direção em assuntos jurídicos especializados (LC nº 180/2026, Art. 6º, §2º)"]},
  ],
  "at-ap": [
    {"cargo": "Assessor Técnico", "subordinadoA": "Comandante-Geral", "requisito": "Oficial do CBMAP", "desdobramentos": [], "atribuicoes": ["Órgão de assessoramento destinado a prestar assessoria, consultoria, recomendação e orientação técnica e política e a expedir nota técnica para auxiliar as decisões dos órgãos de direção em assuntos técnicos especializados (LC nº 180/2026, Art. 6º, §2º)"]},
  ],
  "centros-ap": [
    {"cargo": "Diretores/Comandantes dos Centros, Academia e Coordenadorias", "subordinadoA": "Comando Geral", "requisito": "Oficial do CBMAP", "desdobramentos": ["Centros", "Academia Bombeiro Militar", "Coordenadorias"], "atribuicoes": ["Órgãos de apoio destinados, entre outras atribuições, ao atendimento das necessidades de recursos humanos, saúde, ensino, pesquisa e logística, responsáveis pela realização das atividades-meio da instituição (LC nº 180/2026, Art. 6º, §3º)"]},
  ],
  "gbm-ap": [
    {"cargo": "Comandante de Grupamento de Bombeiro Militar", "subordinadoA": "Comando Geral", "requisito": "Oficial do CBMAP", "desdobramentos": ["Grupamentos Especializados"], "atribuicoes": ["Órgãos de execução destinados à realização das atividades-fim da instituição, compreendendo os Grupamentos de Bombeiro Militar e os Grupamentos Especializados (LC nº 180/2026, Art. 6º, §4º)"]},
  ],
  "em-ap": [
    {"cargo": "Diretor da Escola Militar", "subordinadoA": "Comandante-Geral", "requisito": "Oficial do CBMAP", "desdobramentos": ["Projetos Sociais e demais atividades previstas no decreto regulamentador"], "atribuicoes": ["Órgão vinculado ao CBMAP com regulamentação, organização e estruturação próprias, por meio do desenvolvimento de atividades inerentes à atividade militar e à Defesa Civil (LC nº 180/2026, Art. 6º, §6º)"]},
  ],
},

# ── AMAZONAS (Lei nº 2.538/1999) ──
"am": {
  "cg-am": [
    {"cargo": "Comandante Geral", "subordinadoA": "Governador do Estado", "requisito": "Oficial superior combatente, da ativa, possuidor do Curso Superior de Bombeiro Militar (CSBM), do último posto da própria Corporação; livre nomeação e exoneração do Governador (Art. 10)",
     "desdobramentos": ["Subcomandante Geral", "Coordenadoria Estadual de Defesa Civil", "Conselho Superior de Políticas Estratégicas", "Gabinete do Comando-Geral", "Ajudância Geral", "Comissões"],
     "atribuicoes": [
       "É responsável pelo comando, administração e emprego da Corporação (Art. 9º)",
       "No âmbito do Estado do Amazonas, tem honras e prerrogativas de Secretário de Estado (Art. 9º, parágrafo único)",
       "Será assessorado por oficiais superiores na função de assistentes e por oficial intermediário ou subalterno combatente, na função de ajudante-de-ordens, todos da Corporação (Art. 10, § 3º)"
     ]},
  ],
  "scg-am": [
    {"cargo": "Subcomandante Geral", "subordinadoA": "Comandante Geral", "requisito": "Oficial superior combatente da ativa do último posto da própria Corporação, indicado pelo Comandante Geral e nomeado pelo Governador (Art. 12); honras e prerrogativas de Subsecretário de Estado (Art. 13, parágrafo único)",
     "desdobramentos": ["Órgãos de Direção Setorial (Diretorias)"],
     "atribuicoes": [
       "É o substituto automático do Comandante Geral nas suas faltas e impedimentos (Art. 11)",
       "É o principal assessor do Comandante Geral, competindo-lhe dirigir, orientar, coordenar e fiscalizar todos os trabalhos internos da Corporação (Art. 13)",
       "Coordena as Diretorias (órgãos de direção setorial), às quais compete também: produzir informações; realizar estudos de situação; apresentar propostas e sugestões; elaborar planos e ordens para aprovação do Comandante-Geral; e supervisionar a execução dos planos e ordens (Art. 20, parágrafo único)"
     ]},
  ],
  "gabinete-am": [
    {"cargo": "Chefe de Gabinete", "subordinadoA": "Comandante Geral", "requisito": "Tenente-Coronel QOBM/COMB", "desdobramentos": ["Secretário", "Assessor de Comunicações e Imprensa", "Assessor Jurídico", "Ajudante-de-Ordens"], "atribuicoes": ["Assistência e assessoramento direto ao Comandante Geral", "Controle e supervisão do expediente pessoal do Comandante Geral"]},
    {"cargo": "Assessor de Comunicações e Imprensa (ACI)", "subordinadoA": "Comandante Geral", "requisito": "Oficial", "desdobramentos": [], "atribuicoes": []},
    {"cargo": "Assessor Jurídico (AJ)", "subordinadoA": "Comandante Geral", "requisito": "Oficial", "desdobramentos": [], "atribuicoes": []},
  ],
  "ag-am": [
    {"cargo": "Ajudante Geral", "subordinadoA": "Comandante Geral", "requisito": "Coronel QOBM", "desdobramentos": ["Secretaria Geral", "Seção Administrativa (AG-1)", "Seção de Protocolo e Distribuição (AG-2)", "Seção de Transporte e Embarque (AG-3)", "Seção de Comando e Serviço (AG-4)", "Banda de Música"], "atribuicoes": [
       "A Ajudância Geral é o órgão responsável pelas funções administrativas do Comando Geral (Art. 18)",
       "Trabalhos de secretaria, inclusive correspondências, correios, protocolo geral, arquivo geral e boletim geral (Art. 18, § 1º, a)",
       "Serviço de embarque da Corporação (b)",
       "Apoio de pessoal auxiliar (militar e civil) aos órgãos do Comando Geral (c)",
       "Serviços gerais (d)",
       "Segurança do Quartel do Comando Geral (e)"
     ]},
  ],
  "drh-am": [
    {"cargo": "Diretor de Recursos Humanos", "subordinadoA": "Subcomandante Geral", "requisito": "Oficial Superior", "desdobramentos": ["Seção de Controle de Pessoal Ativo, Inativo e Civil (DRH-1)", "Seção de Recrutamento, Seleção e Serviço Reservado (DRH-2)", "Seção de Cadastro, Identificação, Avaliação, Classificação, Movimentação e Promoções (DRH-3)", "Seção de Desenvolvimento Humano (DRH-4)", "Seção de Expediente e Mobilização (DRH-5)", "Seção de Pagadoria de Pessoal (DRH-6)", "Centro de Assistência Social e Religiosa (CASR)"], "atribuicoes": ["Planejamento, controle e fiscalização das políticas de pessoal", "Capacitação técnica; assistência psicológica, social, jurídica e religiosa"]},
  ],
  "df-am": [
    {"cargo": "Diretor de Finanças", "subordinadoA": "Subcomandante Geral", "requisito": "Oficial Superior", "desdobramentos": ["Seção de Administração Financeira (DF-1)", "Seção de Contabilidade (DF-2)", "Seção de Auditoria (DF-3)", "Seção de Expediente (DF-4)"], "atribuicoes": ["Gestão orçamentária e financeira", "Controle de repasse de recursos; captação de recursos financeiros"]},
  ],
  "dl-am": [
    {"cargo": "Diretor de Logística", "subordinadoA": "Subcomandante Geral", "requisito": "Oficial Superior", "desdobramentos": ["Seção de Suprimento (DL-1)", "Seção de Manutenção (DL-2)", "Seção de Patrimônio e Expediente (DL-3)", "Centro de Suprimento e Manutenção de Materiais e Serviços (CSM/MS)"], "atribuicoes": ["Planejamento, coordenação, fiscalização e controle das atividades de suprimento e material", "Elaboração de convênios"]},
  ],
  "deipo-am": [
    {"cargo": "Diretor de Ensino, Instrução, Pesquisa e Operações", "subordinadoA": "Subcomandante Geral", "requisito": "Oficial Superior", "desdobramentos": ["Seção de Ensino, Instrução e Pesquisa (DEIPO-1)", "Seção de Projetos e Programas Especiais (DEIPO-2)", "Seção de Planejamento, Expediente e Meios Auxiliares (DEIPO-3)", "Escola de Bombeiros Militar (ESBOM)", "Centro de Informática (CInf)"], "atribuicoes": ["Coordenação, fiscalização e controle de ensino, instrução e pesquisa", "Planejamento operacional da Corporação"]},
  ],
  "dst-am": [
    {"cargo": "Diretor de Serviços Técnicos", "subordinadoA": "Subcomandante Geral", "requisito": "Oficial Superior", "desdobramentos": ["Seção de Exames de Projetos (DST-1)", "Seção de Vistorias e Pareceres (DST-2)", "Seção de Hidrante, Expediente e Apoio (DST-3)", "Centro de Perícia de Incêndio (CPI)"], "atribuicoes": ["Estudo, análise, planejamento, exigência e fiscalização da prevenção e segurança contra incêndios e pânico", "Perícias de incêndio e explosão; vistorias e pareceres"]},
  ],
  "esbom-am": [
    {"cargo": "Comandante da Escola de Bombeiros Militar (ESBOM)", "subordinadoA": "Diretor de Ensino, Instrução, Pesquisa e Operações", "requisito": "Oficial", "desdobramentos": ["Subcomandante", "Secretaria", "Divisão de Ensino", "Divisão Administrativa", "Corpo de Alunos"], "atribuicoes": ["Formação, aperfeiçoamento e especialização de bombeiros", "Estudos e pesquisas técnico-científicas"]},
  ],
  "cbc-am": [
    {"cargo": "Comandante de Bombeiros da Capital", "subordinadoA": "Subcomandante Geral", "requisito": "Tenente-Coronel QOBM", "desdobramentos": ["Seção de Administração e Apoio", "Seção de Planejamento Operacional", "Batalhões de Incêndio", "Batalhão de Bombeiro Especial", "Batalhão de Incêndio Florestal e Meio Ambiente"], "atribuicoes": ["Planejamento estratégico, coordenação, fiscalização e emprego das unidades operacionais da capital"]},
  ],
  "cbi-am": [
    {"cargo": "Comandante de Bombeiros do Interior", "subordinadoA": "Subcomandante Geral", "requisito": "Tenente-Coronel QOBM", "desdobramentos": ["Companhias Independentes BM (Itacoatiara, Manacapuru, Parintins)", "Pelotões Independentes BM (Tefé, Tabatinga)"], "atribuicoes": ["Planejamento estratégico, coordenação e fiscalização das unidades do interior"]},
  ],
},

}
