# detail_cargos_g5.py — Cargos detalhados: RN, RS, RJ, SC, SE, TO
# (RR já possui cargos em detail_data_g5; SP é raso na legislação.)
# Chaveado por id de órgão existente em detail_data_g5.

CARGOS = {

# ── RIO GRANDE DO NORTE (LC nº 230/2002) ──
"rn": {
  "comando-geral-rn": [
    {"cargo": "Comandante-Geral", "subordinadoA": "Governador do Estado", "requisito": "Oficial da ativa do último posto (Coronel BM)", "desdobramentos": ["Conselho Superior", "Comandos/Diretorias"], "atribuicoes": ["Administração geral e coordenação das atividades da Instituição", "Presidência da Comissão de Avaliação e Mérito", "Direção do Conselho Superior"]},
    {"cargo": "Subcomandante-Geral", "subordinadoA": "Comandante-Geral", "requisito": "Coronel BM", "desdobramentos": [], "atribuicoes": ["Substituir o Comandante-Geral em impedimentos eventuais", "Funções de assessoramento e funções delegadas"]},
  ],
  "conselho-superior": [{"cargo": "Conselho Superior (CSup)", "subordinadoA": "Comandante-Geral", "requisito": "Coronéis BM da ativa do último posto", "desdobramentos": [], "atribuicoes": ["Acompanhamento de assuntos relevantes da Instituição", "Fornecimento de subsídios para a tomada de decisão; assessoramento direto"]}],
  "dir-setorial-rn": [{"cargo": "Diretores Setoriais (DP, DE, DF, DAL, DST)", "subordinadoA": "Comandante-Geral", "requisito": "Coronéis ou Tenentes-Coronéis", "desdobramentos": ["Diretoria de Pessoal", "Diretoria de Ensino", "Diretoria de Finanças", "Diretoria de Apoio Logístico", "Diretoria de Serviços Técnicos"], "atribuicoes": ["Direção setorial de sistemas específicos", "Planejamento, execução e controle das atividades afetas"]}],
},

# ── RIO GRANDE DO SUL (LC nº 14.920/2016 + Regimento) ──
"rs": {
  "comando-geral": [
    {"cargo": "Comandante-Geral", "subordinadoA": "Secretaria da Segurança Pública", "requisito": "Oficial da ativa do último posto do QOEM", "desdobramentos": ["Gabinete do Comando-Geral", "Departamento Administrativo", "DSPCI", "Academia de Bombeiro Militar", "Comandos Regionais"], "atribuicoes": ["Administração e coordenação geral da Instituição", "Presidência da Comissão de Avaliação e Mérito", "Direção do Conselho Superior"]},
    {"cargo": "Subcomandante-Geral", "subordinadoA": "Comandante-Geral", "requisito": "Oficial da ativa do último posto do QOEM", "desdobramentos": [], "atribuicoes": ["Assessoramento ao Comandante-Geral e funções delegadas", "Substituição em ausências e impedimentos", "Coordenação e supervisão dos órgãos de direção operacional e execução"]},
    {"cargo": "Chefe do Estado-Maior Geral (CHEM)", "subordinadoA": "Comandante-Geral", "requisito": "Coronel QOEM", "desdobramentos": ["Estado-Maior Geral (7 Seções)"], "atribuicoes": ["Estudo, planejamento, coordenação, fiscalização e controle", "Órgão central do sistema de planejamento administrativo e orçamento", "Acúmulo das funções de Subcomandante (substituto eventual)"]},
    {"cargo": "Conselho Superior (CSup)", "subordinadoA": "Comandante-Geral", "requisito": "Coronéis da ativa em exercício", "desdobramentos": [], "atribuicoes": ["Acompanhamento e manifestação em assuntos relevantes; subsídios para decisão"]},
  ],
  "corregedoria-geral": [{"cargo": "Corregedor-Geral", "subordinadoA": "Comandante-Geral", "requisito": "", "desdobramentos": ["Divisão Administrativa", "Divisão de Justiça e Disciplina", "Divisão de Controle Interno Correcional", "Divisão de Feitos Especiais", "Ouvidoria", "Cartório"], "atribuicoes": ["Órgão de disciplina, orientação e fiscalização das atividades funcionais", "Fiscalização da conduta dos militares e servidores civis"]}],
  "departamento-administrativo": [{"cargo": "Diretor do Departamento Administrativo", "subordinadoA": "Comando-Geral", "requisito": "", "desdobramentos": ["Divisão Administrativa", "Divisão de Logística e Patrimônio", "Divisão de Orçamento e Finanças", "Divisão de Recursos Humanos", "Divisão de Tecnologia da Informação e Comunicações"], "atribuicoes": ["Planejamento, direção, controle e execução de logística, patrimônio, finanças, pessoal e TIC"]}],
  "dspci": [{"cargo": "Diretor do Departamento de Segurança, Prevenção e Proteção Contra Incêndios", "subordinadoA": "Comando-Geral", "requisito": "", "desdobramentos": ["Divisão Administrativa", "Divisão de Gestão e Normatização", "Divisão de Pesquisa e Investigação de Sinistros"], "atribuicoes": ["Planejamento, controle e fiscalização da segurança contra incêndios e investigação de sinistros"]}],
  "abm": [{"cargo": "Diretor da Academia de Bombeiro Militar", "subordinadoA": "Comando-Geral", "requisito": "", "desdobramentos": ["Divisão Administrativa", "Divisão de Ensino", "Órgão de Pesquisa, Ensino, Treinamento e Avaliação (OPETA)"], "atribuicoes": ["Planejamento, controle e fiscalização de ensino, saúde física e pesquisa científica", "Capacitação continuada de servidores e profissionais civis auxiliares"]}],
  "aodc": [{"cargo": "Assessor de Operações, Defesa Civil e Serviços Civis Auxiliares (AODC)", "subordinadoA": "Comando-Geral", "requisito": "", "desdobramentos": ["Divisão de Operações e Defesa Civil", "Divisão de Serviços Civis e Auxiliares", "Divisão de Monitoramento Operacional", "Divisão de Operações Aéreas"], "atribuicoes": ["Gestão tática de planejamento, direção, organização e controle de operações"]}],
  "1crbm": [{"cargo": "Comandante de Comando Regional de Bombeiro Militar (CRBM)", "subordinadoA": "Subcomandante-Geral (mobilização)", "requisito": "Oficial Superior QOEM", "desdobramentos": ["Batalhões de Bombeiro Militar", "Batalhão de Busca e Salvamento"], "atribuicoes": ["Supervisão, coordenação e planejamento operacional das unidades subordinadas"]}],
  "besci": [{"cargo": "Comandante do Batalhão Especial de Segurança Contra Incêndio (BESCI)", "subordinadoA": "DSPCI (operacional) / Comando-Geral (administrativo)", "requisito": "Oficial Superior QOEM", "desdobramentos": ["Divisão de Análise de Planos", "Divisão de Vistoria e Fiscalização de Edificações"], "atribuicoes": ["Análise de planos de prevenção contra incêndio", "Vistoria e fiscalização de edificações (abrangência estadual)"]}],
  "cg-rs-lob": [
    {"cargo": "Comandante-Geral", "subordinadoA": "Secretaria da Segurança Pública", "requisito": "", "desdobramentos": ["Gabinete do Comando-Geral", "Corregedoria-Geral", "Comissão de Avaliação e Mérito", "Conselho Superior", "Departamento Administrativo", "Departamento de Segurança, Prevenção e Proteção Contra Incêndios", "Academia de Bombeiro Militar", "Comandos Regionais"],
     "atribuicoes": [
       "Ao Comando-Geral, órgão de direção-geral do CBMRS, compete a administração da Instituição, que será exercida diretamente pelo Comandante-Geral (Art. 4º).",
       "Compete ao Comandante-Geral: I - a coordenação geral das atividades da Instituição; II - a presidência da Comissão de Avaliação e Mérito; e III - a direção do Conselho Superior (Art. 5º)."
     ]},
  ],
},

# ── RIO DE JANEIRO (Lei nº 250/1979) ──
"rj": {
  "comando-geral": [{"cargo": "Comandante-Geral", "subordinadoA": "Secretário de Estado de Segurança Pública", "requisito": "Coronel ou Tenente-Coronel do serviço ativo do Exército", "desdobramentos": ["Estado-Maior-Geral", "Diretorias", "Ajudância-Geral", "Assessorias"], "atribuicoes": ["Responsabilidade pelo comando e administração da Corporação"]}],
  "emg": [
    {"cargo": "Chefe do Estado-Maior-Geral", "subordinadoA": "Comandante-Geral", "requisito": "Coronel BM", "desdobramentos": ["Subchefia", "Seções BM/1 a BM/7"], "atribuicoes": ["Direção, orientação, coordenação e fiscalização do EMG", "Acúmulo das funções de Subcomandante; substituto eventual do Comandante-Geral"]},
    {"cargo": "Subchefe do Estado-Maior-Geral", "subordinadoA": "Chefe do Estado-Maior-Geral", "requisito": "Oficial Superior BM", "desdobramentos": [], "atribuicoes": ["Auxílio direto ao Chefe do EMG; substituto eventual (coordenação do EMG)"]},
  ],
  "diretoria-pessoal": [{"cargo": "Diretor de Pessoal", "subordinadoA": "Comandante-Geral", "requisito": "Oficial", "desdobramentos": ["Seções DP/1 a DP/6", "Capelania"], "atribuicoes": ["Planejamento, execução, controle e fiscalização de pessoal ativo, inativo, pensionistas e civil"]}],
  "diretoria-ensino": [{"cargo": "Diretor de Ensino", "subordinadoA": "Comandante-Geral", "requisito": "Oficial", "desdobramentos": ["Seções DE/1 a DE/4"], "atribuicoes": ["Planejamento, coordenação, fiscalização e controle de formação, aperfeiçoamento e especialização"]}],
  "diretoria-financas": [{"cargo": "Diretor de Finanças", "subordinadoA": "Comandante-Geral", "requisito": "Oficial", "desdobramentos": ["Seções DF/1 a DF/4"], "atribuicoes": ["Atividades financeiras; assessoramento na supervisão e distribuição de recursos"]}],
  "diretoria-apoio-logistico": [{"cargo": "Diretor de Apoio Logístico", "subordinadoA": "Comandante-Geral", "requisito": "Oficial", "desdobramentos": ["Seções DAL/1 a DAL/5"], "atribuicoes": ["Planejamento, coordenação e controle de saúde, suprimento, manutenção e obras"]}],
  "diretoria-servicos-tecnicos": [{"cargo": "Diretor de Serviços Técnicos", "subordinadoA": "Comandante-Geral", "requisito": "Oficial", "desdobramentos": ["Seções DST/1 a DST/5", "Laboratório Químico"], "atribuicoes": ["Estudar, analisar, planejar, exigir e fiscalizar a segurança contra incêndio", "Vistorias, perícias, testes e laudos"]}],
  "ajudancia-geral": [{"cargo": "Ajudante-Geral", "subordinadoA": "Comandante-Geral", "requisito": "Oficial", "desdobramentos": ["Secretaria (AG/1)", "Seção Administrativa (AG/2)", "Seção de Embarque (AG/3)", "Grupamento de Comando"], "atribuicoes": ["Funções administrativas do Comando-Geral; secretaria, protocolo e arquivo", "Segurança do quartel, banda de música e embarque"]}],
  "exec-rj": [
    {"cargo": "Comandante de Bombeiros de Área (CBA)", "subordinadoA": "Comandante-Geral", "requisito": "Coronel ou Tenente-Coronel BM", "desdobramentos": ["Estado-Maior (5 Seções)", "Centro de Operações"], "atribuicoes": ["Planejamento, supervisão e execução de missões de bombeiro-militar na respectiva área"]},
    {"cargo": "Comandante de Unidade de Bombeiros-Militares (UBM)", "subordinadoA": "Comando de Bombeiros de Área", "requisito": "", "desdobramentos": ["Grupamento de Incêndio", "Grupamento de Busca e Salvamento", "Grupamento Marítimo"], "atribuicoes": ["Cumprimento de missões específicas no respectivo território de jurisdição"]},
  ],
},

# ── SANTA CATARINA (LC nº 724/2018 + Dec. nº 1.328/2021) ──
"sc": {
  "comando-geral": [
    {"cargo": "Comandante-Geral", "subordinadoA": "Governador do Estado", "requisito": "Nível estratégico de direção geral", "desdobramentos": ["Subcomando-Geral", "Estado-Maior Geral", "Gabinete do Comando-Geral", "Corregedoria-Geral"], "atribuicoes": ["Concessão de medalha, condecoração e comenda; movimentação de Oficial", "Desenvolvimento funcional das Praças; assinatura de convênios com municípios", "Agregação, reversão e exclusão do serviço ativo"]},
    {"cargo": "Subcomandante-Geral", "subordinadoA": "Comandante-Geral", "requisito": "Oficial do último posto QOBM", "desdobramentos": ["Centro de Monitoramento Operacional e Gestão de Crises"], "atribuicoes": ["Assessoramento ao Comandante-Geral; planejamento de operações estaduais e multi-RBM", "Coordenação e supervisão dos órgãos de direção operacional e execução", "Definição de emprego de Força-Tarefa"]},
  ],
  "emg-sc": [
    {"cargo": "Chefe do Estado-Maior Geral", "subordinadoA": "Comandante-Geral", "requisito": "Coronel QOBM", "desdobramentos": ["Subchefia", "8 Seções de planejamento", "Secretaria"], "atribuicoes": ["Assessoramento ao Comandante-Geral no nível estratégico", "Supervisão da elaboração e execução de normas, instruções e planos"]},
    {"cargo": "Subchefe do Estado-Maior Geral", "subordinadoA": "Chefe do Estado-Maior Geral", "requisito": "Oficial designado (QOBM)", "desdobramentos": [], "atribuicoes": ["Recepção, elaboração, controle e arquivo de documentação", "Desenvolvimento e acompanhamento de projetos"]},
  ],
  "gabinete-cg-sc": [{"cargo": "Chefe do Gabinete do Comando-Geral", "subordinadoA": "Comandante-Geral", "requisito": "", "desdobramentos": ["Ajudância-Geral", "Ouvidoria-Geral", "Centro de Comunicação Social", "Controladoria Interna", "Assessoria Jurídica"], "atribuicoes": ["Assistência e assessoramento direto ao Comandante-Geral"]}],
  "corregedoria-geral-sc": [{"cargo": "Corregedor-Geral", "subordinadoA": "Comandante-Geral", "requisito": "Coronel QOBM", "desdobramentos": ["Corregedor-Adjunto", "Divisão de Eficiência Processual", "Divisão de Supervisão Disciplinar"], "atribuicoes": ["Sistematização e controle de correição funcional, disciplinar e de polícia judiciária militar"]}],
  "diretoria-pessoal-sc": [{"cargo": "Diretor de Pessoal", "subordinadoA": "Chefe do Estado-Maior Geral", "requisito": "Diretor e Subdiretor (direção setorial)", "desdobramentos": ["Divisão de Recursos Humanos", "Divisão de Seleção, Inclusão e Estudo de Pessoal", "Divisão de Saúde Ocupacional e Promoção Social", "Divisão de Educação Física", "Divisão de Segurança do Trabalho"], "atribuicoes": ["Planejamento, coordenação, fiscalização e controle da política de pessoal", "Saúde ocupacional, segurança do trabalho, assistência médica e psicológica"]}],
  "die-sc": [{"cargo": "Diretor de Instrução e Ensino", "subordinadoA": "Chefe do Estado-Maior Geral", "requisito": "Diretor e Subdiretor (direção setorial)", "desdobramentos": ["Divisão de Ensino Básico e Complementar", "Divisão de Controle e Avaliação de Ensino", "Divisão de Educação a Distância", "Centro de Educação e Formação de Condutores"], "atribuicoes": ["Planejamento, coordenação, fiscalização e controle de formação, aperfeiçoamento, especialização, pesquisa e extensão"]}],
  "due-sc": [{"cargo": "Diretor de Urgência e Emergência", "subordinadoA": "Chefe do Estado-Maior Geral", "requisito": "Diretor e Subdiretor (direção setorial)", "desdobramentos": ["Divisão de Normatização e Protocolos", "Divisão de Educação Permanente", "Divisão de Apoio Operacional"], "atribuicoes": ["Estudo, planejamento e execução de atendimento pré-hospitalar; integração com o sistema de saúde"]}],
  "dlf-sc": [{"cargo": "Diretor de Logística e Finanças", "subordinadoA": "Chefe do Estado-Maior Geral", "requisito": "Diretor e Subdiretor (direção setorial)", "desdobramentos": ["Divisão de Finanças", "Divisão de Logística", "Divisão de Tecnologia da Informação e Comunicação"], "atribuicoes": ["Planejamento, coordenação, fiscalização e controle de logística, patrimônio e TIC"]}],
  "dsci-sc": [{"cargo": "Diretor de Segurança Contra Incêndio", "subordinadoA": "Chefe do Estado-Maior Geral", "requisito": "Diretor e Subdiretor (direção setorial)", "desdobramentos": ["Divisão de Normatização", "Divisão de Investigação de Incêndio e Explosão", "Divisão de Pesquisa e Inovação", "Divisão de Engenharia Contra Incêndio", "Divisão de Fiscalização, Auditoria e Coordenação"], "atribuicoes": ["Planejamento, coordenação, fiscalização e controle da segurança contra incêndio"]}],
  "1rbm": [{"cargo": "Comandante da Região Bombeiro Militar (RBM)", "subordinadoA": "Subcomandante-Geral", "requisito": "Oficial do último posto QOBM", "desdobramentos": ["Batalhões Bombeiro Militar", "Companhias", "Pelotões", "Grupos"], "atribuicoes": ["Gestão, planejamento, supervisão, coordenação, controle e fiscalização de missões finalísticas"]}],
  "cebm": [{"cargo": "Comandante do Centro de Ensino Bombeiro Militar (CEBM)", "subordinadoA": "Subcomandante-Geral / DIE", "requisito": "Coronel QOBM", "desdobramentos": ["Academia de Bombeiro Militar", "Centro de Formação e Aperfeiçoamento de Praças", "Centro de Estudos Superiores"], "atribuicoes": ["Formação e aperfeiçoamento de praças; estudos superiores e formação especializada"]}],
},

# ── SERGIPE (Lei nº 8.979/2022 + Regimento) ──
"se": {
  "comando-geral": [{"cargo": "Comandante-Geral", "subordinadoA": "Governador do Estado", "requisito": "Coronel do Quadro de Oficiais Combatentes (CFO, CAO e CSBM)", "desdobramentos": ["Subcomandante-Geral", "Estado-Maior-Geral", "Gabinete", "Corregedoria-Geral", "Controladoria Interna", "Ouvidoria-Geral"], "atribuicoes": ["Comando, administração e emprego da Corporação", "Aprovação do Regimento Interno e de planos e estudos", "Autorização de processos licitatórios; expedição de portarias", "Presidência do Alto-Comando e da Comissão de Promoção de Oficiais"]}],
  "subcomandante-geral": [{"cargo": "Subcomandante-Geral", "subordinadoA": "Comandante-Geral", "requisito": "Coronel do Quadro de Oficiais Combatentes (CFO, CAO e CSBM)", "desdobramentos": ["Chefe do Estado-Maior-Geral (função cumulativa)"], "atribuicoes": ["Substituto do Comandante-Geral em impedimentos", "Presidência da Comissão de Promoção de Praças", "Fiscalização da conduta civil e militar; instauração de procedimentos disciplinares"]}],
  "emg-se": [{"cargo": "Estado-Maior-Geral", "subordinadoA": "Comandante-Geral", "requisito": "Órgão de direção estratégica", "desdobramentos": ["Chefe do EMG", "Corregedor-Geral", "Titulares de diretorias de nível de direção-geral"], "atribuicoes": ["Planejamento, orientação, coordenação, fiscalização e execução de atividades administrativas"]}],
  "gabinete-se": [{"cargo": "Chefe de Gabinete", "subordinadoA": "Comandante-Geral", "requisito": "Oficial Superior QOBM", "desdobramentos": ["Ajudância de Ordens", "Ajudância-Geral"], "atribuicoes": ["Assessoramento direto ao Comandante-Geral e Subcomandante-Geral", "Administração do Quartel do Comando-Geral; expediente, secretaria, protocolo e arquivo"]}],
  "corregedoria-geral-se": [{"cargo": "Corregedor-Geral", "subordinadoA": "Comandante-Geral", "requisito": "Coronel QOBM", "desdobramentos": [], "atribuicoes": ["Sistematização e controle de correição funcional", "Atividades de caráter disciplinar e polícia judiciária militar"]}],
  "controladoria-interna-se": [{"cargo": "Chefe da Controladoria Interna", "subordinadoA": "Comandante-Geral", "requisito": "Oficial Superior QOBM", "desdobramentos": [], "atribuicoes": ["Controle financeiro, contábil, orçamentário, patrimonial e operacional"]}],
  "ouvidoria-geral-se": [{"cargo": "Ouvidor-Geral", "subordinadoA": "Comandante-Geral", "requisito": "Oficial Superior QOBM", "desdobramentos": [], "atribuicoes": ["Prestação de informações e transparência das ações executadas"]}],
  "dlog-se": [{"cargo": "Diretor de Logística", "subordinadoA": "Subcomandante-Geral", "requisito": "Oficial do último posto QOBM", "desdobramentos": [], "atribuicoes": ["Gestão, planejamento, coordenação, execução, fiscalização e controle de logística e patrimônio"]}],
  "dfin-se": [{"cargo": "Diretor de Finanças", "subordinadoA": "Subcomandante-Geral", "requisito": "Oficial do último posto QOBM", "desdobramentos": [], "atribuicoes": ["Gestão e controle de administração financeira e contábil"]}],
  "dgp-se": [{"cargo": "Diretor de Gestão de Pessoal", "subordinadoA": "Subcomandante-Geral", "requisito": "Oficial do último posto QOBM", "desdobramentos": [], "atribuicoes": ["Gestão de pessoal e desenvolvimento de recursos humanos"]}],
  "dep-se": [{"cargo": "Diretor de Ensino e Pesquisa", "subordinadoA": "Subcomandante-Geral", "requisito": "Oficial do último posto QOBM", "desdobramentos": [], "atribuicoes": ["Gestão de ensino e pesquisa; instrução continuada dos quadros"]}],
  "dplan-se": [{"cargo": "Diretor de Planejamento", "subordinadoA": "Subcomandante-Geral", "requisito": "Oficial do último posto QOBM", "desdobramentos": [], "atribuicoes": ["Gestão de políticas públicas e estratégias institucionais", "Orientação e execução da programação orçamentária"]}],
  "dat-se": [{"cargo": "Diretor de Atividades Técnicas", "subordinadoA": "Subcomandante-Geral", "requisito": "Diretor e Diretor-Adjunto (Tenente-Coronel)", "desdobramentos": [], "atribuicoes": ["Gestão e controle de segurança contra incêndio e pânico"]}],
  "dop-se": [
    {"cargo": "Diretor Operacional", "subordinadoA": "Subcomandante-Geral", "requisito": "Diretor e Diretor-Adjunto (Tenente-Coronel)", "desdobramentos": ["Comandos Regionais (CRM, CRAS, CRMS, CRCS, CRS, CRL, CRA, CRBSF)", "Grupamentos"], "atribuicoes": ["Gestão e controle de atividades operacionais e de proteção e defesa civil", "Coordenação e emprego dos Comandos Regionais e Unidades"]},
    {"cargo": "Superior de Dia ao CBMSE", "subordinadoA": "Diretoria Operacional", "requisito": "Oficiais Superiores (escala)", "desdobramentos": [], "atribuicoes": ["Fiscalização e decisões operacionais; comparecimento a sinistros de médio/grande porte", "Acionamento do Plano de Chamada em grandes sinistros"]},
    {"cargo": "Supervisor de Dia ao CBMSE", "subordinadoA": "Diretoria Operacional / Superior de Dia", "requisito": "Oficiais Intermediários (excepcionalmente Subalternos)", "desdobramentos": ["Centro de Operações"], "atribuicoes": ["Serviço de nível tático; triagem de solicitações e despacho de guarnições", "Supervisão e distribuição de ocorrências; remanejamento de recursos"]},
  ],
  "crm-se": [{"cargo": "Comandante de Comando Regional Bombeiro Militar (CRBM)", "subordinadoA": "Diretoria Operacional", "requisito": "Oficial Superior QOBM", "desdobramentos": ["Grupamentos Bombeiro Militar (1º ao 8º GBM)"], "atribuicoes": ["Supervisão, coordenação e planejamento operacional das unidades subordinadas (por AISP)"]}],
  "cg-se-lob": [
    {"cargo": "Comandante-Geral", "subordinadoA": "Governador do Estado", "requisito": "Coronel do Quadro de Oficiais Combatentes da ativa, possuidor dos Cursos de Formação de Oficiais, Aperfeiçoamento de Oficiais e Superior de Bombeiro Militar - CSBM, concomitantemente, ou equivalentes reconhecidos legalmente, observado o disposto no §4º do art. 126 da Constituição Estadual (Art. 6º)",
     "desdobramentos": ["Subcomandante-Geral", "Estado-Maior-Geral", "Gabinete", "Corregedoria-Geral", "Controladoria Interna", "Ouvidoria-Geral", "Assessorias", "Comissões Técnicas"],
     "atribuicoes": [
       "Exercer a representação política e institucional do CBMSE, promovendo contatos e relações com autoridades e organizações de diferentes níveis governamentais (Art. 7º, I)",
       "Promover a administração geral do CBMSE, em estrita observância às disposições normativas da Administração Pública Estadual (II)",
       "Aprovar o Regimento Interno do CBMSE, submetendo-o à homologação por decreto do Governador do Estado (III)",
       "Assessorar o Governador do Estado e o Secretário de Estado da Segurança Pública nos assuntos de competência do CBMSE (IV)",
       "Fazer cumprir as leis, normas e regulamentos da Corporação (V)",
       "Proferir despachos finais em processos administrativos e operacionais que envolvam o efetivo sob seu comando (VI)",
       "Autorizar a abertura de processos licitatórios, homologando-os dentro dos limites de sua competência, e ratificar as dispensas ou declarações de inexigibilidade referentes às contratações diretas, nos termos da legislação específica (VII)",
       "Aprovar a programação orçamentário-financeira a ser executada pelo CBMSE e pelos órgãos a ele subordinados, a proposta orçamentária anual e as alterações e ajustes que se fizerem necessários (VIII)",
       "Expedir portarias, instruções normativas, ordens de serviço, diretrizes e planos que promovam a eficácia da gestão administrativa e operacional da instituição, em consonância com a legislação em vigor (IX)",
       "Instaurar procedimentos de polícia judiciária militar e de polícia administrativa, bem como aplicar as sanções previstas na legislação em vigor (X)",
       "Autorizar despesas nos limites de sua competência (XI)",
       "Delegar atribuições de sua competência que não sejam vedadas por lei (XII)",
       "Aprovar os planos, estudos, programas, projetos e propostas para organização funcional e de atuação do CBMSE (XIII)",
       "Exercer a função de presidente do Alto-Comando do CBMSE (XIV)",
       "Promover o controle e a supervisão dos órgãos subordinados (XV)",
       "Presidir a Comissão de Promoção de Oficiais - CPO e os respectivos processos e encaminhá-los para o Governador do Estado, a quem compete o ato da promoção (XVI)",
       "Atribuir outras atividades aos integrantes da corporação, além daquelas estabelecidas em leis ou regulamentos (XVII)",
       "Coordenar e executar ações de defesa civil no âmbito de suas competências (XVIII)",
       "Designar ocupantes dos órgãos integrantes da estrutura organizacional, ressalvada a competência do Governador do Estado (XIX)",
       "Desempenhar outras atribuições que lhe forem delegadas pelo Governador do Estado ou pelo Secretário de Estado da Segurança Pública ou ainda por aquelas previstas em lei (XX)"
     ]},
  ],
},

# ── TOCANTINS (LC nº 131/2021) ──
"to": {
  "cg-to": [{"cargo": "Comandante-Geral", "subordinadoA": "Chefe do Poder Executivo", "requisito": "Secretário de Estado; Coronel da ativa do QOBM, diplomado em CSBM", "desdobramentos": ["Chefe do Estado-Maior", "Estado-Maior (6 Comandos de Seção)", "Unidades de Direção Setorial, Assessoramento, Apoio e Execução"], "atribuicoes": ["Comando, administração e emprego da Corporação", "Responsabilidade pelo Comando de Ações de Defesa Civil"]}],
  "chefe-estado-maior": [{"cargo": "Chefe do Estado-Maior (CHEM)", "subordinadoA": "Comandante-Geral", "requisito": "Coronel QOBM, diplomado em Curso Superior", "desdobramentos": [], "atribuicoes": ["Principal assessor do Comandante-Geral", "Direção, orientação e fiscalização dos trabalhos do Estado-Maior", "Acúmulo das funções de Subcomandante-Geral; substituto do Comandante-Geral"]}],
  "subchefe-estado-maior": [{"cargo": "Subchefe do Estado-Maior (SUBCHEM)", "subordinadoA": "Chefe do Estado-Maior", "requisito": "Coronel QOBM, diplomado em Curso Superior", "desdobramentos": [], "atribuicoes": ["Coordenação das Seções do Estado-Maior", "Substituto do CHEM em afastamentos e impedimentos"]}],
  "comando-correicao-disciplina": [{"cargo": "Comando de Correição e Disciplina", "subordinadoA": "Chefe do Estado-Maior", "requisito": "Seção do Estado-Maior", "desdobramentos": [], "atribuicoes": ["Garantia da hierarquia e disciplina; padronização de processos administrativos disciplinares", "Apuração de transgressões disciplinares e infrações penais"]}],
  "comando-defesa-civil": [{"cargo": "Comando de Ações de Defesa Civil", "subordinadoA": "Chefe do Estado-Maior", "requisito": "Seção do Estado-Maior", "desdobramentos": [], "atribuicoes": ["Planejamento e coordenação de ações de prevenção, preparação e resposta"]}],
  "comando-gestao-pessoas": [{"cargo": "Comando de Gestão de Pessoas", "subordinadoA": "Chefe do Estado-Maior", "requisito": "Seção do Estado-Maior", "desdobramentos": ["Diretoria de Administração e Gestão de Pessoas", "Diretoria de Ensino e Pesquisa", "Diretoria de Saúde e Assistência Social"], "atribuicoes": ["Planejamento de gestão profissional, legislação, pessoal, saúde e ensino"]}],
  "comando-gestao-recursos": [{"cargo": "Comando de Gestão de Recursos Financeiros e Patrimoniais", "subordinadoA": "Chefe do Estado-Maior", "requisito": "Seção do Estado-Maior", "desdobramentos": ["Diretoria de Logística e Patrimônio", "Diretoria de Orçamento e Finanças"], "atribuicoes": ["Planejamento de orçamento, finanças, logística e infraestrutura"]}],
  "comando-atividades-tecnicas": [{"cargo": "Comando de Atividades Técnicas", "subordinadoA": "Chefe do Estado-Maior", "requisito": "Seção do Estado-Maior", "desdobramentos": ["Diretoria de Serviços Técnicos"], "atribuicoes": ["Planejamento, controle e fiscalização de segurança contra incêndio e emergência"]}],
  "comando-operacional-bm": [{"cargo": "Comando Operacional Bombeiro Militar", "subordinadoA": "Chefe do Estado-Maior", "requisito": "Seção do Estado-Maior", "desdobramentos": ["Unidades Bombeiro Militares (Batalhões, Companhias, Pelotões, Grupos)"], "atribuicoes": ["Planejamento de articulação operacional, administração e controle das operações", "Estudos, estatísticas, doutrina e padronização de procedimentos operacionais"]}],
  "diretoria-administracao-gestao-pessoas": [{"cargo": "Diretor de Administração e Gestão de Pessoas", "subordinadoA": "Comando de Gestão de Pessoas", "requisito": "Direção Setorial", "desdobramentos": [], "atribuicoes": ["Coordenação e execução de gestão de pessoal, recrutamento e folha de pagamento"]}],
  "diretoria-ensino-pesquisa-to": [{"cargo": "Diretor de Ensino e Pesquisa", "subordinadoA": "Comando de Gestão de Pessoas", "requisito": "Direção Setorial", "desdobramentos": ["Academia de Formação de Bombeiros", "Colégios Militares"], "atribuicoes": ["Coordenação e execução de ensino, instrução e pesquisa"]}],
  "diretoria-logistica-patrimonio": [{"cargo": "Diretor de Logística e Patrimônio", "subordinadoA": "Comando de Gestão de Recursos", "requisito": "Direção Setorial", "desdobramentos": [], "atribuicoes": ["Aquisição de material e serviços; logística geral; controle de patrimônio e estoque"]}],
  "diretoria-orcamento-financas": [{"cargo": "Diretor de Orçamento e Finanças", "subordinadoA": "Comando de Gestão de Recursos", "requisito": "Direção Setorial", "desdobramentos": [], "atribuicoes": ["Coordenação, acompanhamento e avaliação da execução orçamentária e financeira"]}],
  "diretoria-saude-assistencia": [{"cargo": "Diretor de Saúde e Assistência Social", "subordinadoA": "Comando de Gestão de Pessoas", "requisito": "Direção Setorial", "desdobramentos": ["Policlínica", "Junta Médica", "Capelania Militar"], "atribuicoes": ["Coordenação, execução e acompanhamento de serviços de saúde e promoção social"]}],
  "diretoria-servicos-tecnicos-to": [{"cargo": "Diretor de Serviços Técnicos", "subordinadoA": "Comando de Atividades Técnicas", "requisito": "Direção Setorial", "desdobramentos": [], "atribuicoes": ["Coordenação da área de prevenção contra incêndio e emergência"]}],
},

}
