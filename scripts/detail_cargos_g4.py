# detail_cargos_g4.py — Cargos detalhados: PR, PB, PA, PE, PI
# Chaveado por id de órgão existente em detail_data_g4.

CARGOS = {

# ── PARANÁ (Lei nº 22.206/2024) ──
"pr": {
  "comandante_geral": [{"cargo": "Comandante-Geral", "subordinadoA": "Governador do Estado", "requisito": "Coronel Combatente da ativa", "desdobramentos": ["Subcomandante-Geral", "Estado-Maior", "Gabinete do Comando-Geral", "Consultoria Institucional", "Corregedoria-Geral"], "atribuicoes": ["Comando, administração e emprego geral da Corporação", "Planejamento visando à organização da Corporação", "Nomeação de bombeiros militares em funções de direção, comando e assessoramento", "Precedência hierárquica e funcional sobre todos os Oficiais e Praças"]}],
  "subcomandante_geral": [{"cargo": "Subcomandante-Geral", "subordinadoA": "Comandante-Geral", "requisito": "Coronel Combatente da ativa", "desdobramentos": [], "atribuicoes": ["Substituto imediato do Comandante-Geral", "Coordenador operacional da Corporação"]}],
  "estado_maior": [
    {"cargo": "Chefe do Estado-Maior", "subordinadoA": "Comandante-Geral", "requisito": "Coronel Combatente da ativa", "desdobramentos": ["1ª a 4ª Seção (BM/1 a BM/4)"], "atribuicoes": ["Planejamento estratégico da Corporação", "Elaboração de diretrizes e ordens do Comando-Geral", "Precedência sobre demais, exceto CG e SCG"]},
    {"cargo": "1ª Seção (BM/1)", "subordinadoA": "Chefe do Estado-Maior", "requisito": "Oficial Superior", "desdobramentos": [], "atribuicoes": ["Pessoal e legislação"]},
    {"cargo": "2ª Seção (BM/2)", "subordinadoA": "Chefe do Estado-Maior", "requisito": "Oficial Superior", "desdobramentos": [], "atribuicoes": [
       "Assessorar e manter o Comandante-Geral, o Subcomandante-Geral e o Chefe do Estado-Maior constantemente informados dos fatos, informes e informações que digam respeito ao Corpo de Bombeiros Militar do Paraná e às responsabilidades de inteligência e contrainteligência atribuídas à Corporação pelo Sistema Estadual de Inteligência de Segurança Pública, Sistema de Inteligência de Segurança Pública e pelo Sistema Brasileiro de Inteligência (Art. 3º, I)",
       "Produzir conhecimento útil e oportuno necessários às decisões do Comandante-Geral, do Subcomandante-Geral e o Chefe do Estado-Maior, bem como aos estudos e planejamentos do Estado-Maior (II)"
     ]},
    {"cargo": "3ª Seção (BM/3)", "subordinadoA": "Chefe do Estado-Maior", "requisito": "Oficial Superior", "desdobramentos": [], "atribuicoes": ["Planejamento, operações e estatística"]},
    {"cargo": "4ª Seção (BM/4)", "subordinadoA": "Chefe do Estado-Maior", "requisito": "Oficial Superior", "desdobramentos": [], "atribuicoes": ["Logística da Corporação"]},
  ],
  "gabinete_cg": [
    {"cargo": "Chefe de Gabinete", "subordinadoA": "Comandante-Geral", "requisito": "Oficial Superior Combatente da ativa", "desdobramentos": ["Ajudância-Geral", "Assessoria Estratégica", "Assessoria de Comunicação Organizacional", "Secretaria do Comando-Geral"], "atribuicoes": ["Assistência direta ao Comandante-Geral", "Recepção, estudo e triagem de expedientes", "Transmissão e controle da execução de ordens"]},
  ],
  "ajudancia_geral": [{"cargo": "Ajudante-Geral", "subordinadoA": "Chefe de Gabinete", "requisito": "Oficial", "desdobramentos": ["Banda de Música", "Protocolo Geral", "Arquivo Geral", "Centro Histórico"], "atribuicoes": [
       "A Ajudância-Geral, subordinada ao Chefe de Gabinete, exercerá o apoio administrativo ao Comando-Geral (Art. 16)",
       "A organização, a direção e a supervisão do pessoal auxiliar de todos os órgãos do Comando-Geral e do efetivo da Banda de Música do CBMPR (Art. 16, I, a e b)",
       "A coordenação dos trabalhos de protocolo geral da Corporação (II)",
       "O controle da entrada e retirada de processos e documentos do arquivo geral (III)",
       "A elaboração dos boletins-gerais (IV)",
       "O desenvolvimento das demais tarefas relacionadas com a segurança do aquartelamento e dos serviços gerais do Comando-Geral (V)",
       "A promoção das atividades necessárias para a manutenção e desenvolvimento do centro histórico (VI)",
       "Executar os trabalhos de protocolo, boletim geral, registro geral e outros (Portaria CG nº 022/2024, Art. 4º, I)",
       "Manter atualizada a situação do efetivo do CCB, com base no QO em vigor, coordenando a coleta dos dados necessários (II)",
       "Executar a administração financeira e o aprovisionamento do Quartel do Comando-Geral (QCG) (III)",
       "Executar o apoio de pessoal aos órgãos do Comando-Geral (IV)",
       "Preparar e distribuir o Boletim-Geral, providenciando para que um exemplar permaneça em arquivo (V)",
       "Organizar e administrar o Arquivo Geral (VI)",
       "Organizar e administrar o Centro Histórico (VII)",
       "Organizar e manter atualizado nos sistemas os dados dos militares estaduais integrantes da Ajudância-Geral e daqueles que servem no QCG, para fins de acionamento e outros (VIII)",
       "Executar a segurança e serviços gerais do QCG/CBMPR, bem como elaborar escalas de serviço para tal finalidade (IX)"
     ]}],
  "assessoria_estrategica": [{"cargo": "Assessor Estratégico", "subordinadoA": "Comandante-Geral", "requisito": "Oficial", "desdobramentos": [], "atribuicoes": ["Planejamento, implementação e monitoramento de projetos institucionais", "Gestão e controle da captação de recursos", "Assessoramento em defesa civil; coordenação do SIATE"]}],
  "assessoria_comunicacao": [{"cargo": "Assessor de Comunicação Organizacional", "subordinadoA": "Comandante-Geral", "requisito": "Oficial", "desdobramentos": [], "atribuicoes": ["Comunicação social, campanhas de educação preventiva e assessoria de imprensa", "Organização de solenidades e eventos"]}],
  "consultoria_institucional": [{"cargo": "Consultor Institucional", "subordinadoA": "Comandante-Geral e Subcomandante-Geral", "requisito": "Oficial com formação jurídica", "desdobramentos": [], "atribuicoes": ["Estudo de questões de direito da administração geral", "Exame de legalidade dos atos e normas", "Orientação quanto ao cumprimento de decisões judiciais", "Análise de minutas e convênios"]}],
  "corregedoria_geral": [{"cargo": "Corregedor-Geral", "subordinadoA": "Comandante-Geral", "requisito": "Coronel Combatente da ativa", "desdobramentos": ["Comissão Disciplinar Geral", "Comissão de Recurso"], "atribuicoes": ["Assegurar a correta aplicação da lei; padronizar a Polícia Judiciária Militar", "Realizar correições, inspeções e fiscalizações", "Apuração de crimes militares, fatos administrativos e faltas disciplinares"]}],
  "comissoes": [
    {"cargo": "Comissão de Promoções de Oficiais (CPO)", "subordinadoA": "Comandante-Geral", "requisito": "Coronéis e Oficiais", "desdobramentos": [], "atribuicoes": ["Controle, avaliação e processamento das promoções de oficiais"]},
    {"cargo": "Comissão de Promoções de Praças (CPP)", "subordinadoA": "Comandante-Geral", "requisito": "Oficiais e Praças", "desdobramentos": [], "atribuicoes": ["Controle, avaliação e processamento das promoções de praças"]},
    {"cargo": "Comissão de Mérito (CM)", "subordinadoA": "Comandante-Geral", "requisito": "Oficiais", "desdobramentos": [], "atribuicoes": ["Apreciação do mérito; proposta de outorga de medalhas e condecorações"]},
  ],
  "diretoria_pessoal": [{"cargo": "Diretor de Pessoal", "subordinadoA": "Comando-Geral", "requisito": "Coronel Combatente da ativa", "desdobramentos": ["Centro de Recrutamento e Seleção", "Centro de Saúde", "Centro de Educação Física e Desporto"], "atribuicoes": ["Desenvolvimento, coordenação, fiscalização e controle das atividades de pessoal", "Acompanhamento de saúde física e mental"]}],
  "diretoria_apoio_logistico": [{"cargo": "Diretor de Apoio Logístico e Finanças", "subordinadoA": "Comando-Geral", "requisito": "Coronel Combatente da ativa", "desdobramentos": ["Centro de Planejamento e Compras", "Centro de Administração Logística", "Centro de Orçamento e Finanças", "Centro de Suprimento e Manutenção"], "atribuicoes": ["Coordenação, controle e execução de logística, suprimento e patrimônio", "Execução orçamentária e financeira; controladoria e auditoria"]}],
  "diretoria_atividades_tecnicas": [{"cargo": "Diretor de Atividades Técnicas", "subordinadoA": "Comando-Geral", "requisito": "Coronel Combatente da ativa", "desdobramentos": [], "atribuicoes": ["Coordenação e assessoramento em prevenção e combate a incêndios e desastres", "Gerenciamento normativo e estudos de incêndios", "Tecnologia da informação e comunicação"]}],
  "escola_superior": [{"cargo": "Diretor da Escola Superior de Bombeiro Militar", "subordinadoA": "Comando-Geral", "requisito": "Coronel Combatente da ativa", "desdobramentos": [], "atribuicoes": ["Planejamento, coordenação, fiscalização e execução das atividades de ensino"]}],
  "comando_regional": [{"cargo": "Comandante Regional de Bombeiro Militar (CRBM)", "subordinadoA": "Subcomandante-Geral", "requisito": "Coronel Combatente da ativa", "desdobramentos": ["Batalhões", "Companhias Independentes"], "atribuicoes": ["Escalão intermediário de comando", "Ações operacionais estratégicas; distribuição de efetivo", "Auxílio, fiscalização e gestão logística das unidades subordinadas"]}],
  "batalhao": [{"cargo": "Comandante de Batalhão de Bombeiro Militar (BBM)", "subordinadoA": "Comando Regional", "requisito": "Oficial Superior", "desdobramentos": ["Companhias", "Pelotões", "Grupos"], "atribuicoes": ["Coordenação e execução de defesa civil", "Combate a incêndios e desastres; buscas, salvamentos, socorros e atendimento pré-hospitalar"]}],
  "gost": [{"cargo": "Grupo de Operações de Socorro Tático (GOST)", "subordinadoA": "Comandante-Geral", "requisito": "Equivalente a Companhia Independente", "desdobramentos": [], "atribuicoes": ["Missão especializada de socorro tático", "Emergências ambientais e defesa civil; busca e salvamento com cães"]}],
  "uoa": [{"cargo": "Unidade de Operações Aéreas (UOA)", "subordinadoA": "Subcomandante-Geral", "requisito": "Oficial Superior", "desdobramentos": [], "atribuicoes": ["Busca, resgate e salvamento aéreo", "Missões de apoio à defesa civil e a órgãos públicos"]}],
  "cg-pr-lob": [
    {"cargo": "Comandante-Geral", "subordinadoA": "Governador do Estado", "requisito": "Coronel Combatente da ativa do Corpo de Bombeiros Militar do Paraná - CBMPR (Art. 10)",
     "desdobramentos": ["Subcomandante-Geral - SCG", "Estado-Maior - EM", "Gabinete do Comando-Geral - Gab.CmtG", "Consultoria Institucional - CI", "Comissão de Promoções de Oficiais - CPO", "Comissão de Promoções de Praças - CPP", "Comissão de Mérito - CM", "Corregedoria-Geral - Coger"],
     "atribuicoes": [
       "O Comandante-Geral, responsável superior pelo comando e pela administração geral do Corpo de Bombeiros Militar do Paraná - CBMPR, será nomeado pelo Governador do Estado, dentre os Coronéis Combatentes da ativa da Corporação. (Art. 10)",
       "Parágrafo único. O Comandante-Geral tem precedência hierárquica e funcional sobre todos os Oficiais e Praças do Corpo de Bombeiros Militar do Paraná - CBMPR que estejam no exercício de funções bombeiros-militares, de natureza ou interesse bombeiro-militar, dentro ou fora da Corporação, com exceção da precedência funcional em relação ao Coordenador Estadual da Defesa Civil. (Art. 10, parágrafo único)"
     ]},
  ],
},

# ── PARAÍBA (LC nº 191/2024) ──
"pb": {
  "comandante_geral": [{"cargo": "Comandante Geral", "subordinadoA": "Governador do Estado", "requisito": "Coronel da ativa do QOEM; honras de Secretário de Estado", "desdobramentos": ["Gabinete do Comando Geral", "Estado Maior Geral", "Controladoria Interna", "Corregedoria", "Comandos Regionais", "Diretorias"], "atribuicoes": ["Comando, gestão, emprego, supervisão e coordenação geral", "Aprovar diretrizes e planos de emprego, ensino, orçamento e regimentos", "Aprovar normas técnicas de segurança contra incêndio e controle de pânico", "Exercer a competência disciplinar e a polícia judiciária militar", "Declarar aspirantes-a-oficial e promover praças"]}],
  "subcomandante_geral": [{"cargo": "Subcomandante Geral", "subordinadoA": "Comandante Geral", "requisito": "Coronel da ativa do QOEM; honras de Secretário Executivo de Estado", "desdobramentos": [], "atribuicoes": ["Garantia da hierarquia e disciplina; principal assessor do CMTG", "Substituto legal do Comandante Geral", "Supervisionar os órgãos de direção setorial e de execução (nível estratégico)"]}],
  "estado_maior_geral": [{"cargo": "Chefe do Estado Maior Geral", "subordinadoA": "Comandante Geral", "requisito": "Coronel da ativa da Corporação (cargo em comissão)", "desdobramentos": ["1ª a 8ª Coordenadoria (EMG)"], "atribuicoes": ["Elaborar o Planejamento Estratégico da Corporação", "Elaborar diretrizes, planos e ordens", "Realizar estudos, planejamentos, coordenar e fiscalizar as atividades", "Elaborar o Plano de Contratações Anual"]}],
  "controladoria_interna": [{"cargo": "Controlador Interno", "subordinadoA": "Comando Geral", "requisito": "", "desdobramentos": ["Seção de Auditoria e Fiscalização", "Seção de Gestão de Contratos", "Seção de Controle de Gastos", "Seção de Controle Patrimonial"], "atribuicoes": ["Auditoria, fiscalização, gestão de contratos e controle de gastos e patrimônio"]}],
  "corregedoria_pb": [{"cargo": "Corregedor", "subordinadoA": "Comando Geral", "requisito": "", "desdobramentos": ["Corregedor Adjunto"], "atribuicoes": ["Atividade correcional, disciplinar e de polícia judiciária militar"]}],
  "crbm_pb": [{"cargo": "Comandante Regional de Bombeiro Militar (CRBM)", "subordinadoA": "Comando Geral", "requisito": "", "desdobramentos": ["Estado Maior Regional (B/1 a B/6)", "Centro Regional de Intendência"], "atribuicoes": ["Direção, controle e planejamento das atividades operacionais das unidades em sua região"]}],
  "dal_pb": [{"cargo": "Diretor de Apoio Logístico", "subordinadoA": "Subcomandante Geral", "requisito": "Oficial Superior", "desdobramentos": ["Centro de Suprimento Logístico", "Centro de Arquitetura, Engenharia e Obras", "Centro de Controle e Manutenção de Viaturas"], "atribuicoes": ["Aquisições, especificações e registros; gestão patrimonial e apoio à administração logística"]}],
  "dat_pb": [{"cargo": "Diretor de Atividades Técnicas", "subordinadoA": "Subcomandante Geral", "requisito": "Oficial Superior", "desdobramentos": ["Conselho Técnico Normativo", "Conselho Técnico Deliberativo"], "atribuicoes": ["Legislação de prevenção contra incêndio e controle de pânico", "Segurança contra incêndio"]}],
  "dep_pb": [{"cargo": "Diretor de Educação e Pesquisa", "subordinadoA": "Subcomandante Geral", "requisito": "Oficial Superior", "desdobramentos": ["Academia de Bombeiro Militar (ABMAP)", "Colégios Militares", "Corpo Musical"], "atribuicoes": ["Planejamento pedagógico; ensino, pesquisa e extensão", "Tecnologia da informação e ensino a distância"]}],
  "df_pb": [{"cargo": "Diretor de Finanças", "subordinadoA": "Subcomandante Geral", "requisito": "Oficial Superior", "desdobramentos": ["Seções DF/1 a DF/5"], "atribuicoes": ["Administração financeira, orçamento, contabilidade, auditoria e captação de recursos"]}],
  "dgp_pb": [{"cargo": "Diretor de Gestão de Pessoas", "subordinadoA": "Subcomandante Geral", "requisito": "Oficial Superior", "desdobramentos": ["Centro de Recrutamento e Seleção de Pessoal", "Seções DGP/1 a DGP/8"], "atribuicoes": ["Recrutamento e seleção; cadastro, avaliação e identificação", "Movimentação, promoções, justiça e disciplina, folha de pagamento"]}],
  "ds_pb": [{"cargo": "Diretor de Saúde", "subordinadoA": "Subcomandante Geral", "requisito": "Oficial Superior", "desdobramentos": ["Centro de Perícia Médica de Saúde Militar", "Centro de Saúde Biopsicossocial", "Clínica Veterinária"], "atribuicoes": ["Perícia médica de saúde militar; gestão de pessoal de saúde e do fundo de saúde"]}],
  "dti_pb": [{"cargo": "Diretor de Tecnologia da Informação", "subordinadoA": "Subcomandante Geral", "requisito": "Oficial Superior", "desdobramentos": ["Seções DTI/1 a DTI/8"], "atribuicoes": ["Administração de redes e segurança da informação; bancos de dados", "Desenvolvimento de sistemas corporativos e suporte"]}],
  "exec_pb": [{"cargo": "Comandantes das Unidades de Execução (BBM, CIBM, GEOR, GOA)", "subordinadoA": "Comandos Regionais de Bombeiro Militar", "requisito": "", "desdobramentos": ["Batalhões BM", "Companhias e Companhias Independentes", "Grupamento Especializado em Operações de Risco", "Grupamento de Operações Aéreas"], "atribuicoes": ["Execução das atividades operacionais e técnicas de bombeiro militar"]}],
},

# ── PARÁ (Lei nº 11.060/2025) ──
"pa": {
  "comandante_geral": [{"cargo": "Comandante-Geral", "subordinadoA": "Chefe do Poder Executivo Estadual", "requisito": "Oficial da ativa do último posto (QOBM)", "desdobramentos": ["Alto Comando", "Estado-Maior Geral", "CEDEC", "Corregedoria-Geral", "Comando de Operações", "Departamentos-Gerais"], "atribuicoes": [
       "Comandar, gerir, empregar, supervisionar e coordenar de forma geral as atividades da Corporação, assessorado pelos órgãos de direção, apoio e de execução (Art. 7º, I)",
       "Presidir o Alto Comando do Corpo de Bombeiros Militar do Pará (CBMPA), a Comissão de Promoção de Oficiais e o Conselho do Mérito Bombeiro Militar (II)",
       "Encaminhar ao órgão competente o projeto de orçamento anual referente ao CBMPA e participar, no que couber, da elaboração do Plano Plurianual (III)",
       "Celebrar convênios e contratos de interesse do CBMPA com entidades de direito público ou privado, nos termos da lei (IV)",
       "Nomear e exonerar bombeiros militares no exercício das funções de direção, comando e assessoramento, nos termos desta Lei (V)",
       "Autorizar bombeiros militares e servidores civis da Corporação a se afastarem do Estado (VI)",
       "Ordenar o emprego de verbas orçamentárias ou de créditos abertos em favor do CBMPA e de outros recursos que este venha a receber, oriundos de quaisquer fontes de receitas (VII)",
       "Expedir os atos necessários para a administração do CBMPA (VIII)",
       "Incorporar praças e praças especiais (IX)",
       "Promover praças e declarar aspirantes-a-oficial (X)",
       "Conceder férias, licenças ou afastamentos de qualquer natureza (XI)",
       "Instaurar e solucionar procedimentos e processos administrativos, disciplinares ou não, aplicando as penalidades previstas na legislação vigente (XII)",
       "Criar, desenvolver e gerenciar programas de prevenção e proteção nas atividades bombeiro militar que visem à melhoria da qualidade de vida do cidadão (XIII)",
       "Certificar o atendimento do direito ao porte de arma de seus militares, bem como as hipóteses excepcionais de suspensão e cassação de porte de arma (XIV)",
       "Encaminhar ao Chefe do Poder Executivo a lista de promoção dos oficiais, nos termos da lei que estabelece as regras de promoção (XV)",
       "Poderá delegar competência para a expedição de atos administrativos, visando à agilização da gestão da Corporação (Art. 7º, § 1º)"
     ]}],
  "chefe_estado_maior_geral": [
    {"cargo": "Chefe do Estado-Maior Geral", "subordinadoA": "Comandante-Geral", "requisito": "Oficial do último posto (QOBM)", "desdobramentos": ["Subchefe", "Seções BM/1 a BM/6", "Escritório de Projetos e Convênios"], "atribuicoes": ["Substituição do Comandante-Geral em impedimentos", "Direção, coordenação e controle de pessoal, legislação, operações, logística, qualidade e orçamento", "Execução do planejamento aprovado pelo Comandante-Geral"]},
    {"cargo": "1ª Seção (BM/1) — Pessoal e Legislação", "subordinadoA": "Chefe do Estado-Maior Geral", "requisito": "Oficial Superior", "desdobramentos": ["SEEP", "SEEL"], "atribuicoes": ["Efetivo militar e civil; ingresso, ciclos e carreira", "Política de efetivos; normatização sobre inclusão, seleção e movimentações"]},
    {"cargo": "2ª Seção (BM/2) — Gestão do Conhecimento, Cultura e Inovação", "subordinadoA": "Chefe do Estado-Maior Geral", "requisito": "Oficial Superior", "desdobramentos": ["SPBG", "STCI"], "atribuicoes": ["Gestão do conhecimento; mapeamento por competências", "Patrimônio histórico-cultural; projetos de inovação tecnológica"]},
    {"cargo": "3ª Seção (BM/3) — Operações, Doutrina e Estatística", "subordinadoA": "Chefe do Estado-Maior Geral", "requisito": "Oficial Superior", "desdobramentos": ["SOGE", "SEED"], "atribuicoes": ["Planejamento de operações e grandes eventos", "Plano de Emprego Operacional; doutrina e dados estatísticos"]},
    {"cargo": "4ª Seção (BM/4) — Logística", "subordinadoA": "Chefe do Estado-Maior Geral", "requisito": "Oficial Superior", "desdobramentos": ["SPL", "SAC"], "atribuicoes": ["Diagnóstico e planejamento logístico", "Banco de especificações; controle e supervisão de logística e patrimônio"]},
    {"cargo": "5ª Seção (BM/5) — Gestão pela Qualidade", "subordinadoA": "Chefe do Estado-Maior Geral", "requisito": "Oficial Superior", "desdobramentos": ["SGAR", "SPQ"], "atribuicoes": ["Gestão por processos e avaliação de resultados", "Planos baseados em normas ISO; ciclo PDCA"]},
    {"cargo": "6ª Seção (BM/6) — Planejamento e Orçamento Institucional", "subordinadoA": "Chefe do Estado-Maior Geral", "requisito": "Oficial Superior", "desdobramentos": ["SPPOGR", "SAP"], "atribuicoes": ["Planejamento e orçamento institucional (PPA, LDO, LOA)", "Controle da execução orçamentária e relatórios gerenciais"]},
  ],
  "alto_comando": [{"cargo": "Alto Comando", "subordinadoA": "Comandante-Geral", "requisito": "Órgão colegiado deliberativo e consultivo", "desdobramentos": ["Membros natos e 3 membros efetivos do último posto"], "atribuicoes": ["Deliberação e consulta em assuntos de direção-geral"]}],
  "cedec": [
    {"cargo": "Coordenador Estadual de Proteção e Defesa Civil", "subordinadoA": "Chefe do Poder Executivo Estadual", "requisito": "Comandante-Geral do CBMPA", "desdobramentos": ["Coordenador-Adjunto", "Divisão de Gestão de Risco", "Divisão de Gerenciamento de Desastres"], "atribuicoes": ["Integração, planejamento, coordenação e supervisão das medidas preventivas", "Elaboração do Plano Estadual de Proteção e Defesa Civil"]},
    {"cargo": "Coordenador-Adjunto Estadual de Proteção e Defesa Civil", "subordinadoA": "Comandante-Geral", "requisito": "Oficial da ativa do último posto (QOBM)", "desdobramentos": [], "atribuicoes": ["Substituição do Comandante-Geral em impedimentos", "Coordenação das unidades da CEDEC"]},
  ],
  "corregedoria_geral": [
    {"cargo": "Corregedor-Geral", "subordinadoA": "Comandante-Geral", "requisito": "Oficial do último posto (QOBM), preferencialmente bacharel em Direito", "desdobramentos": ["Subcorregedor-Geral", "Comissões Disciplinares", "Seção de Inteligência Correcional"], "atribuicoes": ["Direção superior da Corregedoria-Geral", "Determinar instauração de sindicâncias e processos administrativos", "Decisões disciplinares em 1ª instância e recursos hierárquicos"]},
    {"cargo": "Subcorregedor-Geral", "subordinadoA": "Corregedor-Geral", "requisito": "Tenente-Coronel (QOBM)", "desdobramentos": ["Comissão Disciplinar Geral"], "atribuicoes": ["Auxílio ao Corregedor-Geral; presidência da Comissão Disciplinar Geral", "Coordenação das Comissões Disciplinares Regionais"]},
  ],
  "comando_operacoes": [{"cargo": "Comandante Operacional", "subordinadoA": "Comandante-Geral", "requisito": "Oficial do último posto (QOBM)", "desdobramentos": ["Assistente", "Seções de Planejamento", "Comandos Regionais"], "atribuicoes": ["Direção e controle dos órgãos de direção intermediária e setorial", "Direção e controle de apoio e execução da atividade-fim"]}],
  "departamento_administracao": [{"cargo": "Chefe do Departamento-Geral de Administração (DGA)", "subordinadoA": "Comandante-Geral", "requisito": "Oficial do último posto (QOBM)", "desdobramentos": ["Diretoria de Apoio Logístico", "Diretoria de Finanças", "Diretoria de Contratações e Aquisições", "Diretoria de TIC"], "atribuicoes": ["Direção e controle dos órgãos de apoio logístico, finanças, contratações e TIC"]}],
  "departamento_pessoal": [{"cargo": "Chefe do Departamento-Geral de Pessoal (DGP)", "subordinadoA": "Comandante-Geral", "requisito": "Oficial do último posto (QOBM)", "desdobramentos": ["Seção de Controle de Pessoal", "Seção de Pagamento", "Seção de Recrutamento, Seleção e Inclusão", "Seção de Identificação"], "atribuicoes": ["Direção e controle das atividades de pessoal (ingresso, identificação, movimentação)", "Assistência psicológica, social e religiosa; saúde"]}],
  "departamento_cultura": [{"cargo": "Chefe do Departamento-Geral de Cultura, Educação e Pesquisa (DGCEP)", "subordinadoA": "Comandante-Geral", "requisito": "Oficial do último posto (QOBM)", "desdobramentos": ["Seção de Planejamento de Ensino e Pesquisa", "Academia Bombeiro Militar"], "atribuicoes": ["Gestão do sistema de ensino bombeiro militar e das atividades de pesquisa", "Formação, capacitação e especialização; promoção da cultura"]}],
  "departamento_seguranca_incendio": [{"cargo": "Chefe do Departamento-Geral de Segurança contra Incêndios e Emergências (DGSCI)", "subordinadoA": "Comandante-Geral", "requisito": "Oficial do último posto (QOBM)", "desdobramentos": ["Seção de Fiscalização e Vistoria Técnica", "Seção de Análise de Projetos", "Seção de Perícia de Incêndio", "Seção de Credenciamento"], "atribuicoes": ["Diretrizes gerais de segurança contra incêndios e emergências", "Proteção da vida e redução de danos ao meio ambiente e ao patrimônio"]}],
  "comando_regional_bombeiros": [{"cargo": "Comandante Regional de Bombeiros (CRB)", "subordinadoA": "Comando de Operações", "requisito": "Oficial do último posto (QOBM)", "desdobramentos": ["Subcomandante (Tenente-Coronel)", "Seção de Administração", "Seção de Planejamento, Instrução e Operações", "Núcleo de Corregedoria"], "atribuicoes": ["Direção, controle e planejamento das atividades operacionais das UBMs subordinadas"]}],
  "exec_pa": [{"cargo": "Comandantes das Unidades de Execução (GBM, GMAF, GBS, GSE, GOA)", "subordinadoA": "Comandos Regionais de Bombeiros", "requisito": "", "desdobramentos": ["Grupamento Marítimo e Fluvial", "Grupamento de Busca e Salvamento", "Grupamento de Operações Aéreas", "Núcleo de Ações com Cães"], "atribuicoes": ["Execução das atividades-fim de bombeiro militar"]}],
  "cg-pa-lob": [
    {"cargo": "Comandante-Geral", "subordinadoA": "Governador do Estado", "requisito": "Oficial da ativa, último posto do Quadro de Oficiais Bombeiro Militar Combatente (QOBM), não convocado da reserva, possuidor do curso superior de bombeiros; equiparado a Secretário de Estado (Art. 7º)",
     "desdobramentos": ["Alto Comando", "Estado-Maior Geral", "Coordenadoria Estadual de Proteção e Defesa Civil do Pará (CEDEC)", "Corregedoria-Geral", "Comando de Operações", "Departamentos-Gerais", "Comissões", "Gabinete do Comandante-Geral", "Ajudância-Geral", "Controladoria Interna", "Consultoria Jurídica (CONJUR)", "Centro de Inteligência (CEINT)"],
     "atribuicoes": [
       "O comando, a gestão, o emprego, a supervisão e a coordenação geral das atividades da corporação, assessorado pelos órgãos de direção, apoio e de execução (Art. 8º, I)",
       "A presidência do Alto Comando do Corpo de Bombeiros Militar do Pará (CBMPA), da Comissão de Promoção de Oficiais e do Conselho do Mérito Bombeiro Militar (II)",
       "Encaminhar ao órgão competente o projeto de orçamento anual referente ao Corpo de Bombeiros Militar do Pará (CBMPA) e participar, no que couber, da elaboração do Plano Plurianual (III)",
       "Celebrar convênios e contratos de interesse do Corpo de Bombeiros Militar do Pará (CBMPA) com entidades de direito público ou privado, nos termos da lei (IV)",
       "Nomear e exonerar bombeiros militares no exercício das funções de direção, comando e assessoramento, nos termos desta lei (V)",
       "Autorizar bombeiros militares e servidores civis da corporação a se afastarem do estado (VI)",
       "Ordenar o emprego de verbas orçamentárias ou de créditos abertos em favor do Corpo de Bombeiros Militar do Pará (CBMPA) e de outros recursos que este venha a receber, oriundos de quaisquer fontes de receitas (VII)",
       "Expedir os atos necessários para a administração do Corpo de Bombeiros Militar do Pará (CBMPA) (VIII)",
       "Incorporar praças e praças especiais (IX)",
       "Promover praças e declarar aspirantes-a-oficial (X)",
       "Conceder férias, licenças ou afastamentos de qualquer natureza (XI)",
       "Instaurar e solucionar procedimentos e processos administrativos, disciplinares ou não, aplicando as penalidades previstas na legislação vigente (XII)",
       "Criar, desenvolver e gerenciar programas de prevenção e proteção nas atividades bombeiro militar que visem à melhoria da qualidade de vida do cidadão (XIII)",
       "Certificar o atendimento do direito ao porte de arma de seus militares, bem como as hipóteses excepcionais de suspensão e cassação de porte de arma (XIV)",
       "Encaminhar ao Chefe do Poder Executivo a lista de promoção dos oficiais, nos termos da lei que estabelece as regras de promoção (XV) (Art. 8º, I a XV)",
       "Poderá delegar competência para a expedição de atos administrativos, visando à agilização da gestão da corporação (Art. 8º, § 1º)",
       "Nos impedimentos ou ausências do Comandante-Geral, responderá pelo comando-geral o chefe do Estado-Maior Geral e, no impedimento ou ausência deste, seguirá a seguinte ordem de prioridade: o Coordenador-Adjunto Estadual de Proteção e Defesa Civil, o Corregedor-Geral, o Comandante Operacional e o chefe do Departamento-Geral mais antigo (Art. 8º, § 2º)"
     ]},
  ],
},

# ── PERNAMBUCO (Lei nº 15.187/2013) ──
"pe": {
  "comandante_geral": [{"cargo": "Comandante Geral", "subordinadoA": "Secretaria de Defesa Social", "requisito": "Oficial do Quadro de Combatentes (QOC) da ativa, do último posto", "desdobramentos": ["Subcomandante Geral", "Conselho de Políticas e Estratégias"], "atribuicoes": ["Responsável pelo comando, administração e emprego da Corporação", "Precedência hierárquica e funcional sobre demais coronéis"]}],
  "subcomandante_geral": [{"cargo": "Subcomandante Geral", "subordinadoA": "Comandante Geral", "requisito": "Oficial combatente da ativa do último posto", "desdobramentos": [], "atribuicoes": ["Substituto imediato do Comandante Geral", "Precedência funcional e hierárquica sobre demais oficiais"]}],
  "conselho_politicas": [{"cargo": "Presidente do Conselho de Políticas e Estratégias (CPE)", "subordinadoA": "Comandante Geral", "requisito": "Comandante Geral", "desdobramentos": ["Membros natos (SCG, Diretores)", "Secretaria"], "atribuicoes": ["Formulação da doutrina geral de emprego", "Viabilização de políticas, estratégias, diretrizes e ordens do Comandante Geral"]}],
  "diretoria_gestao_pessoal": [{"cargo": "Diretor de Gestão de Pessoal", "subordinadoA": "Comando Geral", "requisito": "Oficial", "desdobramentos": ["Divisão de Controle de Pessoal", "Divisão de Formação, Especialização e Aperfeiçoamento", "Divisão de Inativos e Pensionistas", "Divisão de Planejamento e Desenvolvimento"], "atribuicoes": ["Planejamento, normatização, controle e fiscalização de pessoal", "Formação, especialização e aperfeiçoamento; assistência social"]}],
  "diretoria_logistica": [{"cargo": "Diretor de Logística", "subordinadoA": "Comando Geral", "requisito": "Oficial", "desdobramentos": ["Divisão de Planejamento Logístico", "Divisão de Controle de Contratos", "Divisão de Controle de Patrimônio", "Divisão de Controle de Transporte", "Divisão de Compras e Serviços"], "atribuicoes": ["Aquisição, contratação e gestão de frota e patrimônio", "Manutenção de materiais; engenharia, arquitetura e obras"]}],
  "diretoria_financas": [{"cargo": "Diretor de Finanças", "subordinadoA": "Comando Geral", "requisito": "Oficial", "desdobramentos": ["Divisão de Controle Orçamentário e Financeiro", "Divisão Administrativa e Financeira"], "atribuicoes": ["Planejamento, normatização, execução e controle financeiro"]}],
  "diretoria_planejamento": [{"cargo": "Diretor de Planejamento e Gestão", "subordinadoA": "Comando Geral", "requisito": "Oficial", "desdobramentos": ["Divisão de Planejamento e Gestão", "Divisão de Projetos", "Divisão de Convênios", "Divisão de Arrecadação Tributária"], "atribuicoes": ["Elaboração e gestão do planejamento institucional", "Monitoramento do orçamento e do plano estratégico; gestão de projetos e convênios"]}],
  "diretoria_integrada_metropolitana": [{"cargo": "Diretor Integrado Metropolitano", "subordinadoA": "Comando Geral", "requisito": "Oficial", "desdobramentos": ["Comando Operacional Metropolitano", "Centro de Controle Operacional", "Centro de Resposta a Desastres"], "atribuicoes": ["Planejamento e supervisão das operações em Recife e Região Metropolitana", "Controle operacional dos atendimentos emergenciais e resposta a desastres"]}],
  "comando_operacional_metropolitano": [{"cargo": "Comandante Operacional Metropolitano (COM)", "subordinadoA": "Diretoria Integrada Metropolitana", "requisito": "Oficial", "desdobramentos": ["Divisão de Articulação Operacional", "Divisão de Monitoramento e Controle", "Divisão de Coordenação Tática e Operacional"], "atribuicoes": ["Direção executiva na área de Recife e Região Metropolitana", "Combate a incêndio, salvamento e atendimento pré-hospitalar"]}],
  "diretorias_integradas_pe": [
    {"cargo": "Diretor Integrado Especializado (DIEsp)", "subordinadoA": "Comando Geral", "requisito": "Oficial", "desdobramentos": ["Comando Operacional Especializado"], "atribuicoes": ["Atividades técnicas: vistorias, análise de projetos e credenciamento", "Execução de normas de segurança contra incêndio e pânico"]},
    {"cargo": "Diretor Integrado do Interior/1 (DInter/1)", "subordinadoA": "Comando Geral", "requisito": "Oficial", "desdobramentos": ["Comando Operacional do Interior/1"], "atribuicoes": ["Operações na Zona da Mata e Agreste"]},
    {"cargo": "Diretor Integrado do Interior/2 (DInter/2)", "subordinadoA": "Comando Geral", "requisito": "Oficial", "desdobramentos": ["Comando Operacional do Interior/2"], "atribuicoes": ["Operações no Sertão"]},
  ],
},

# ── PIAUÍ (Lei nº 7.772/2022) ──
"pi": {
  "comando_geral": [
    {"cargo": "Comandante-Geral", "subordinadoA": "Governador do Estado", "requisito": "Oficial do último posto da Corporação (QOBMC)", "desdobramentos": ["Subcomandante-Geral", "Alto Comando", "Gabinete", "Assessorias"], "atribuicoes": ["Comando, gestão, emprego, supervisão e coordenação das atividades", "Presidência do Alto Comando e da Comissão de Promoção de Oficiais"]},
    {"cargo": "Subcomandante-Geral", "subordinadoA": "Comandante-Geral", "requisito": "Oficial do último posto (QOBMC)", "desdobramentos": ["Chefe do Estado-Maior-Geral"], "atribuicoes": ["Substituto imediato do Comandante-Geral", "Acúmulo da função de Chefe do Estado-Maior-Geral"]},
  ],
  "alto_comando": [{"cargo": "Alto Comando (Órgão Colegiado Deliberativo)", "subordinadoA": "Comandante-Geral", "requisito": "Coronéis da ativa", "desdobramentos": ["Membros natos (SCG, Diretores, Cmt. Operacional)", "Secretaria"], "atribuicoes": ["Colaboração no processo decisório em assuntos de relevância", "Decisões sobre pessoal, ensino, disciplina, legislação, projetos e promoções em grau de recurso"]}],
  "diretoria_gestao_pessoas": [{"cargo": "Diretor de Gestão de Pessoas", "subordinadoA": "Alto Comando", "requisito": "Oficial", "desdobramentos": ["Seções DGP-1 a DGP-6", "Núcleo de Voluntários da Reserva Remunerada"], "atribuicoes": ["Planejamento, coordenação, execução, controle e fiscalização de pessoal"]}],
  "diretoria_administrativa_financeira": [{"cargo": "Diretor Administrativo e Financeiro", "subordinadoA": "Alto Comando", "requisito": "Oficial", "desdobramentos": ["Seções DAF-1 a DAF-5"], "atribuicoes": ["Administração financeira, programação e orçamento", "Gestão de material e patrimônio; armas e munições"]}],
  "diretoria_ensino": [{"cargo": "Diretor de Ensino, Instrução e Pesquisa", "subordinadoA": "Alto Comando", "requisito": "Oficial", "desdobramentos": ["Seções DEIP-1 a DEIP-3", "Banda de Música"], "atribuicoes": ["Planejamento, coordenação e fiscalização de formação, aperfeiçoamento e especialização", "Adestramento e instrução"]}],
  "diretoria_seguranca_incendio": [{"cargo": "Diretor de Segurança Contra Incêndio", "subordinadoA": "Alto Comando", "requisito": "Oficial", "desdobramentos": ["Seções DSCI-1 a DSCI-5"], "atribuicoes": ["Planejamento, análise, controle e fiscalização de segurança contra incêndio e pânico"]}],
  "comando_operacional": [{"cargo": "Comandante Operacional de Bombeiros (COB)", "subordinadoA": "Direção Geral", "requisito": "Coronel ou Tenente-Coronel", "desdobramentos": ["Subcomandante Operacional", "Seções de Operações, Hidrantes e Planejamento", "Comandos Regionais"], "atribuicoes": ["Planejamento estratégico e fiscalização do emprego dos Comandos Regionais"]}],
  "crbm_i": [{"cargo": "Comandante Regional de Bombeiros Militar (CRBM)", "subordinadoA": "Comando Operacional de Bombeiros", "requisito": "Penúltimo posto (QOBMC)", "desdobramentos": ["Subcomandante", "Seções de Planejamento, Comunicações e Estatística", "Grupamentos"], "atribuicoes": ["Planejamento operacional, supervisão, coordenação e controle das atividades em sua circunscrição"]}],
  "grupamento_bombeiros": [{"cargo": "Comandante de Grupamento de Bombeiros Militar (GBM)", "subordinadoA": "Comando Regional", "requisito": "Oficial Superior (QOBMC)", "desdobramentos": ["Subcomandante", "Seções de Planejamento, Logística, Estatística e Serviços Técnicos", "Subgrupamentos"], "atribuicoes": ["Prevenção e extinção de incêndios; busca, salvamento e atendimento pré-hospitalar", "Auxílio em atividades de defesa civil"]}],
  "grupamento_maritimo": [{"cargo": "Comandante do Grupamento de Bombeiros Militar Marítimo (GBMar)", "subordinadoA": "Comando Regional", "requisito": "Major (QOBMC)", "desdobramentos": ["Subgrupamentos Marítimos"], "atribuicoes": ["Operações aquáticas; prevenção em eventos náuticos", "Busca e salvamento; combate a incêndio em embarcações"]}],
},

}
