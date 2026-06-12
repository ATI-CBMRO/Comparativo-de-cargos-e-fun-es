# detail_data_g5.py — RN, RR, RS, RJ, SC, SE, SP, TO

DATA = {

"rr": {
  "legal_source": "Lei Complementar nº 52, de 28 de dezembro de 2001 (alt. até LC nº 275/2018)",
  "organs": {
    "cg-rr": {
      "name": "Comando Geral", "abbreviation": "CG", "category": "Administração Superior",
      "subordinadoA": "Governador do Estado", "legalRef": "Art. 11",
      "baseLegal": "Lei Complementar nº 52, de 28 de dezembro de 2001",
      "artigosDeOrigem": ["Art. 11 (Comando Geral)", "Art. 12 (Comandante Geral)", "Art. 13 (Subcomandante Geral)"],
      "atribuicoes": ["Órgão máximo executivo do Corpo de Bombeiros Militar de Roraima, incumbido da administração da instituição"],
      "desdobramentos": ["Comandante Geral", "Subcomandante Geral", "Gabinete", "Corregedoria Geral", "Estado Maior Geral", "Comissão de Avaliação e Mérito", "Ajudância Geral", "Centro Cultural", "Coordenadoria Estadual de Proteção e Defesa Civil", "Comissões", "Diretoria de Inteligência"],
      "cargos": [
        {"cargo": "Comandante Geral", "subordinadoA": "Governador do Estado", "requisito": "Oficial da ativa do último posto do quadro de combatentes (QOCBM); honras e prerrogativas de Secretário de Estado", "desdobramentos": [], "atribuicoes": ["Responsável pela administração geral da instituição", "Acumula o cargo de Coordenador Estadual de Proteção e Defesa Civil"]},
        {"cargo": "Subcomandante Geral", "subordinadoA": "Comandante Geral", "requisito": "Oficial da ativa do quadro de combatentes; honras de Secretário de Estado Adjunto", "desdobramentos": ["Chefe do Estado Maior Geral Bombeiro Militar"], "atribuicoes": ["Substituto eventual do Comandante Geral", "Chefe do Estado Maior Geral Bombeiro Militar"]}
      ]
    },
    "gab-rr": {
      "name": "Gabinete do Comandante Geral", "abbreviation": "GAB", "category": "Assessoramento",
      "subordinadoA": "Comando Geral", "legalRef": "Art. 14-19",
      "baseLegal": "Lei Complementar nº 52, de 28 de dezembro de 2001",
      "artigosDeOrigem": ["Art. 14 (Gabinete)", "Art. 15-19 (Estrutura)"],
      "atribuicoes": ["Supervisão e execução das atividades administrativas de apoio e assessoramento direto, imediato e pessoal do Comandante Geral"],
      "desdobramentos": ["Chefia de Gabinete", "Secretaria", "Assessoria de Comunicação e Imprensa (ACI)", "Comissão de Justiça (CJ)", "Ajudância de Ordens"],
      "cargos": [
        {"cargo": "Chefe de Gabinete", "subordinadoA": "Comandante Geral", "requisito": "Oficial", "desdobramentos": ["Secretaria", "ACI", "Comissão de Justiça", "Ajudância de Ordens"], "atribuicoes": ["Funções de assistência e assessoramento direto ao Comandante Geral nos assuntos que fogem às atribuições normais dos demais órgãos de direção"]},
        {"cargo": "Presidente da Comissão de Justiça", "subordinadoA": "Comandante Geral", "requisito": "Oficial; obrigatório um advogado civil; pode ser dirigida por um procurador", "desdobramentos": [], "atribuicoes": ["Execução das atividades de assessoria jurídica à instituição"]}
      ]
    },
    "correg-rr": {
      "name": "Corregedoria Geral", "abbreviation": "Correg", "category": "Administração Superior",
      "subordinadoA": "Comandante Geral", "legalRef": "Art. 20",
      "baseLegal": "Lei Complementar nº 52, de 28 de dezembro de 2001",
      "artigosDeOrigem": ["Art. 20 (Corregedoria Geral)"],
      "atribuicoes": ["Órgão de disciplina, orientação e fiscalização das atividades funcionais e da conduta dos servidores da instituição", "Apuração de responsabilidade criminal, administrativa e disciplinar"],
      "desdobramentos": ["Chefia da Corregedoria", "Seção Administrativa", "Cartório", "Seção de Investigação", "Ouvidoria"],
      "cargos": [{"cargo": "Chefe da Corregedoria", "subordinadoA": "Comandante Geral", "requisito": "Oficial", "desdobramentos": ["Seção Administrativa", "Cartório", "Seção de Investigação", "Ouvidoria"], "atribuicoes": ["Disciplina, orientação e fiscalização das atividades funcionais"]}]
    },
    "cam-rr": {
      "name": "Comissão de Avaliação e Mérito", "abbreviation": "CAM", "category": "Assessoramento",
      "subordinadoA": "Comandante Geral", "legalRef": "Art. 22",
      "baseLegal": "Lei Complementar nº 52, de 28 de dezembro de 2001",
      "artigosDeOrigem": ["Art. 22 (Comissão de Avaliação e Mérito)"],
      "atribuicoes": ["Órgão de assessoramento permanente do Comandante Geral", "Controle, avaliação e processamento das promoções de oficiais e de praças"],
      "desdobramentos": [],
      "cargos": [{"cargo": "Presidente da Comissão de Avaliação e Mérito", "subordinadoA": "Comandante Geral", "requisito": "Oficial do QOCBM", "desdobramentos": [], "atribuicoes": ["À Comissão de Avaliação e Mérito, órgão de assessoramento permanente do Comandante Geral, compete o controle, avaliação e processamento das promoções de oficiais e de praças (LC nº 52/2001, Art. 22)"]}]
    },
    "ag-rr": {
      "name": "Ajudância Geral", "abbreviation": "AG", "category": "Suporte",
      "subordinadoA": "Subcomandante Geral", "legalRef": "Art. 21",
      "baseLegal": "Lei Complementar nº 52, de 28 de dezembro de 2001",
      "artigosDeOrigem": ["Art. 21 (Ajudância Geral)"],
      "atribuicoes": ["OBM de suporte com as funções administrativas do Quartel do Comando Geral, inclusive o controle de todo o seu pessoal"],
      "desdobramentos": ["Secretaria Geral", "Seção Administrativa", "Seção de Protocolo e Distribuição", "Seção de Transporte e Embarque", "Companhia de Comando e Serviços", "Centro de Saúde"],
      "cargos": [{"cargo": "Ajudante Geral", "subordinadoA": "Subcomandante Geral", "requisito": "Oficial", "desdobramentos": ["Companhia de Comando e Serviços", "Centro de Saúde"], "atribuicoes": ["Funções administrativas do Quartel do Comando Geral"]}]
    },
    "ccult-rr": {
      "name": "Centro Cultural", "abbreviation": "CCult", "category": "Administração Superior",
      "subordinadoA": "Comandante Geral", "legalRef": "Art. 23",
      "baseLegal": "Lei Complementar nº 52, de 28 de dezembro de 2001",
      "artigosDeOrigem": ["Art. 23 (Centro Cultural)"],
      "atribuicoes": ["Administração das atividades socioculturais, particularmente as relacionadas à banda de música e à preservação da memória institucional"],
      "desdobramentos": ["Seção Administrativa", "Museu do Corpo de Bombeiro Militar", "Banda de Música"],
      "cargos": [{"cargo": "Comandante do Centro Cultural", "subordinadoA": "Comandante Geral", "requisito": "Oficial do QOCBM", "desdobramentos": ["Seção Administrativa", "Museu do Corpo de Bombeiro Militar", "Banda de Música"], "atribuicoes": ["O Centro Cultural, subordinado diretamente ao Comandante Geral, é o órgão encarregado da administração das atividades socioculturais, particularmente as relacionadas à banda de música e à preservação da memória institucional (LC nº 52/2001, Art. 23)"]}]
    },
    "cepdec-rr": {
      "name": "Coordenadoria Estadual de Proteção e Defesa Civil", "abbreviation": "CEPDEC", "category": "Administração Superior",
      "subordinadoA": "Comandante Geral (Coordenador Estadual)", "legalRef": "Art. 24",
      "baseLegal": "Lei Complementar nº 52, de 28 de dezembro de 2001 (alt. LC nº 257/2017 e LC nº 265/2018)",
      "artigosDeOrigem": ["Art. 24 (CEPDEC)"],
      "atribuicoes": ["Órgão de direção geral que centraliza o sistema Estadual de Proteção e Defesa Civil de Roraima", "Estabelecer normas e exercer atividades de integrar, planejar, organizar, coordenar e supervisionar as medidas preventivas, de socorro, assistência e recuperação nas situações de emergência ou calamidade pública"],
      "desdobramentos": ["Coordenador Estadual de Proteção e Defesa Civil", "Diretor Executivo de Proteção e Defesa Civil", "Coordenadores Regionais (Capital, Centro Sul, Sul, Norte e Leste)", "Divisão de Prevenção, Mitigação e Preparação", "Divisão de Resposta ao Desastre", "Divisão de Recuperação de Cenário de Desastre", "Divisão Administrativa", "Gerências (Ação Comunitária, Minimização de Desastre, Monitoramento, Logística, Engenharia, Hidrologia, Meteorologia, entre outras)"],
      "cargos": [
        {"cargo": "Coordenador Estadual de Proteção e Defesa Civil", "subordinadoA": "Governador do Estado", "requisito": "Comandante Geral do CBMRR (acumulação ex officio)", "desdobramentos": ["Diretor Executivo de Proteção e Defesa Civil"], "atribuicoes": ["A Coordenadoria Estadual de Defesa Civil — CEDEC, é o órgão de direção geral, que centraliza o sistema estadual de defesa civil de Roraima e tem por finalidade estabelecer normas e o exercício das atividades de integrar, planejar, organizar, coordenar e supervisionar as execuções das medidas preventivas, de socorro, de assistência e de recuperação, considerando os efeitos produzidos por fatores adversos de qualquer natureza e origens nas situações de emergência ou estado de calamidade pública (LC nº 52/2001, Art. 24)"]},
        {"cargo": "Diretor Executivo de Proteção e Defesa Civil", "subordinadoA": "Coordenador Estadual de Proteção e Defesa Civil", "requisito": "Oficial do CBMRR", "desdobramentos": ["Coordenadores Regionais", "Divisões de Prevenção, Resposta e Recuperação", "Divisão Administrativa"], "atribuicoes": ["Direção executiva da Coordenadoria Estadual de Proteção e Defesa Civil (CEPDEC), coordenando as atividades de prevenção, mitigação, preparação, resposta e recuperação em situações de emergência ou calamidade pública (LC nº 52/2001, Art. 24 §1°)"]}
      ]
    },
    "dint-rr": {
      "name": "Diretoria de Inteligência", "abbreviation": "DINT", "category": "Administração Superior",
      "subordinadoA": "Comandante Geral", "legalRef": "Art. 25-A",
      "baseLegal": "Lei Complementar nº 52/2001 (incl. LC nº 257/2017)",
      "artigosDeOrigem": ["Art. 25-A (Diretoria de Inteligência)"],
      "atribuicoes": ["Exercício sistemático de ações especializadas voltadas para a obtenção, produção de dados e conhecimentos e salvaguarda destes", "Assessorar o Comandante Geral no planejamento, acompanhamento e execução de políticas e atos decisórios", "Identificação, avaliação e neutralização de atividades de inteligência adversas"],
      "desdobramentos": ["Subdiretoria de Inteligência", "Subdiretoria de Contra Inteligência e Segurança Institucional", "Subdiretoria de Operações de Inteligência", "Subdiretoria de Registro e Porte de Arma de Fogo", "Subdiretoria de Expediente"],
      "cargos": [{"cargo": "Diretor de Inteligência", "subordinadoA": "Comandante Geral", "requisito": "Oficial Superior do QOCBM", "desdobramentos": ["Subdiretoria de Inteligência", "Subdiretoria de Contra Inteligência e Segurança Institucional", "Subdiretoria de Operações de Inteligência", "Subdiretoria de Registro e Porte de Arma de Fogo", "Subdiretoria de Expediente"], "atribuicoes": ["Exercício sistemático de ações especializadas voltadas para a obtenção, produção de dados e conhecimentos e salvaguarda destes, assessorando o Comandante Geral no planejamento, acompanhamento e execução de políticas e atos decisórios, bem como na identificação, avaliação e neutralização de atividades de inteligência adversas (LC nº 52/2001, Art. 25-A, incl. LC nº 257/2017)"]}]
    },
    "emg-rr": {
      "name": "Estado Maior Geral Bombeiro Militar", "abbreviation": "EMG", "category": "Administração Superior",
      "subordinadoA": "Comandante Geral", "legalRef": "Art. 26-27",
      "baseLegal": "Lei Complementar nº 52, de 28 de dezembro de 2001",
      "artigosDeOrigem": ["Art. 26 (EMG)", "Art. 27 (Estrutura)", "Arts. 29-35 (Diretorias)"],
      "atribuicoes": ["OBM de Atuação Colegiada, de caráter permanente", "Definição das políticas, estabelecimento das diretrizes e ordens do Comando Geral em nível estratégico", "Elaboração dos planos gerais da corporação"],
      "desdobramentos": ["Chefe (Subcomandante Geral)", "Diretoria de Pessoal e Legislação (DPL)", "Diretoria de Informática e Estatísticas (DIE)", "Diretoria de Ensino, Instrução e Pesquisa (DEIP)", "Diretoria de Logística (DLOG)", "Diretoria de Prevenção e Serviços Técnicos (DPST)", "Diretoria de Assuntos Civis e Relações Públicas (DACRP)", "Diretoria de Gestão Orçamentária e Financeira (DGOF)", "Diretoria de Controle Interno (DCI)"],
      "cargos": [{"cargo": "Chefe do Estado Maior Geral", "subordinadoA": "Comandante Geral", "requisito": "Subcomandante Geral (Coronel QOCBM)", "desdobramentos": ["Diretorias do EMG (DPL, DIE, DEIP, DLOG, DPST, DACRP, DGOF, DCI)"], "atribuicoes": ["Direção do Estado Maior Geral"]}]
    },
    "dpl-rr": {
      "name": "Diretoria de Pessoal e Legislação", "abbreviation": "DPL", "category": "Administração Superior (EMG)",
      "subordinadoA": "Estado Maior Geral Bombeiro Militar", "legalRef": "Art. 29",
      "baseLegal": "Lei Complementar nº 52, de 28 de dezembro de 2001",
      "artigosDeOrigem": ["Art. 29 (DPL)"],
      "atribuicoes": ["Gestão de pessoal ativo, inativo e pensionista, identificação, folha de pagamento e legislação"],
      "desdobramentos": ["Subdiretoria de Pessoal Ativo", "Subdiretoria de Pessoal Inativo e Pensionista", "Subdiretoria de Identificação", "Subdiretoria de Expediente", "Subdiretoria de Folha de Pagamento", "Subdiretoria de Legislação"],
      "cargos": [{"cargo": "Diretor de Pessoal e Legislação", "subordinadoA": "Chefe do Estado Maior Geral", "requisito": "Oficial Superior do QOCBM", "desdobramentos": ["Subdiretoria de Pessoal Ativo", "Subdiretoria de Pessoal Inativo e Pensionista", "Subdiretoria de Identificação", "Subdiretoria de Expediente", "Subdiretoria de Folha de Pagamento", "Subdiretoria de Legislação"], "atribuicoes": ["A Diretoria de Pessoal e Legislação tem por competência a gestão de pessoal ativo, inativo e pensionista, identificação, folha de pagamento e legislação da corporação (LC nº 52/2001, Art. 29)"]}]
    },
    "die-rr": {
      "name": "Diretoria de Informática e Estatísticas", "abbreviation": "DIE", "category": "Administração Superior (EMG)",
      "subordinadoA": "Estado Maior Geral Bombeiro Militar", "legalRef": "Art. 30",
      "baseLegal": "Lei Complementar nº 52/2001 (alt. LC nº 257/2017)",
      "artigosDeOrigem": ["Art. 30 (DIE)"],
      "atribuicoes": ["Gestão das atividades de informática e estatística da corporação"],
      "desdobramentos": ["Subdiretoria de Expediente", "Centro de Estatística (CEST)", "Centro de Informática (CINFOR)"],
      "cargos": [{"cargo": "Diretor de Informática e Estatísticas", "subordinadoA": "Chefe do Estado Maior Geral", "requisito": "Oficial Superior do QOCBM", "desdobramentos": ["Subdiretoria de Expediente", "Centro de Estatística (CEST)", "Centro de Informática (CINFOR)"], "atribuicoes": ["A Diretoria de Informática e Estatísticas tem por competência a gestão das atividades de informática e estatística da corporação (LC nº 52/2001, Art. 30, alt. LC nº 257/2017)"]}]
    },
    "deip-rr": {
      "name": "Diretoria de Ensino, Instrução e Pesquisa", "abbreviation": "DEIP", "category": "Administração Superior (EMG)",
      "subordinadoA": "Estado Maior Geral Bombeiro Militar", "legalRef": "Art. 31",
      "baseLegal": "Lei Complementar nº 52/2001 (alt. LC nº 257/2017)",
      "artigosDeOrigem": ["Art. 31 (DEIP)"],
      "atribuicoes": ["Planejamento e organização do ensino, instrução, operação e pesquisa"],
      "desdobramentos": ["Subdiretoria de Expediente", "Subdiretoria de Planejamento e Organização Operacional", "Centro de Operações e Comunicações de Bombeiros (COCB)", "Centro de Ensino e Instrução de Bombeiros (CEIB)", "Centro de Educação Física e Desportos (CEFID)"],
      "cargos": [{"cargo": "Diretor de Ensino, Instrução e Pesquisa", "subordinadoA": "Chefe do Estado Maior Geral", "requisito": "Oficial Superior do QOCBM", "desdobramentos": ["Subdiretoria de Expediente", "Subdiretoria de Planejamento e Organização Operacional", "Centro de Operações e Comunicações de Bombeiros (COCB)", "Centro de Ensino e Instrução de Bombeiros (CEIB)", "Centro de Educação Física e Desportos (CEFID)"], "atribuicoes": ["A Diretoria de Ensino, Instrução e Pesquisa tem por competência o planejamento e organização do ensino, instrução, operação e pesquisa da corporação (LC nº 52/2001, Art. 31, alt. LC nº 257/2017)"]}]
    },
    "dlog-rr": {
      "name": "Diretoria de Logística", "abbreviation": "DLOG", "category": "Administração Superior (EMG)",
      "subordinadoA": "Estado Maior Geral Bombeiro Militar", "legalRef": "Art. 32",
      "baseLegal": "Lei Complementar nº 52/2001 (alt. LC nº 265/2018)",
      "artigosDeOrigem": ["Art. 32 (DLOG)"],
      "atribuicoes": ["Gestão das atividades de suprimento, material e manutenção da corporação"],
      "desdobramentos": ["Subdiretoria de Expediente", "Centro de Suprimento e Material (CSM)", "Centro de Manutenção (CEMAN)"],
      "cargos": [{"cargo": "Diretor de Logística", "subordinadoA": "Chefe do Estado Maior Geral", "requisito": "Oficial Superior do QOCBM", "desdobramentos": ["Subdiretoria de Expediente", "Centro de Suprimento e Material (CSM)", "Centro de Manutenção (CEMAN)"], "atribuicoes": ["A Diretoria de Logística tem por competência a gestão das atividades de suprimento, material e manutenção da corporação (LC nº 52/2001, Art. 32, alt. LC nº 265/2018)"]}]
    },
    "dpst-rr": {
      "name": "Diretoria de Prevenção e Serviços Técnicos", "abbreviation": "DPST", "category": "Administração Superior (EMG)",
      "subordinadoA": "Estado Maior Geral Bombeiro Militar", "legalRef": "Art. 33",
      "baseLegal": "Lei Complementar nº 52, de 28 de dezembro de 2001",
      "artigosDeOrigem": ["Art. 33 (DPST)"],
      "atribuicoes": ["Gestão das atividades de prevenção, vistoria, análise de projetos e investigação de incêndio"],
      "desdobramentos": ["Subdiretoria de Hidrantes", "Centro de Vistoria e Análise de Projeto (CVAP)", "Centro de Investigação e Prevenção de Incêndio (CIPI)", "Subdiretoria de Expediente"],
      "cargos": [{"cargo": "Diretor de Prevenção e Serviços Técnicos", "subordinadoA": "Chefe do Estado Maior Geral", "requisito": "Oficial Superior do QOCBM", "desdobramentos": ["Subdiretoria de Hidrantes", "Centro de Vistoria e Análise de Projeto (CVAP)", "Centro de Investigação e Prevenção de Incêndio (CIPI)", "Subdiretoria de Expediente"], "atribuicoes": ["A Diretoria de Prevenção e Serviços Técnicos tem por competência a gestão das atividades de prevenção, vistoria, análise de projetos e investigação de incêndio da corporação (LC nº 52/2001, Art. 33)"]}]
    },
    "dacrp-rr": {
      "name": "Diretoria de Assuntos Civis e Relações Públicas", "abbreviation": "DACRP", "category": "Administração Superior (EMG)",
      "subordinadoA": "Estado Maior Geral Bombeiro Militar", "legalRef": "Art. 34",
      "baseLegal": "Lei Complementar nº 52/2001 (alt. LC nº 257/2017)",
      "artigosDeOrigem": ["Art. 34 (DACRP)"],
      "atribuicoes": ["Gestão dos assuntos civis, relações públicas e cerimonial da corporação"],
      "desdobramentos": ["Subdiretoria de Expediente", "Subdiretoria de Assuntos Civis", "Subdiretoria de Relações Públicas", "Centro de Cerimonial"],
      "cargos": [{"cargo": "Diretor de Assuntos Civis e Relações Públicas", "subordinadoA": "Chefe do Estado Maior Geral", "requisito": "Oficial Superior do QOCBM", "desdobramentos": ["Subdiretoria de Expediente", "Subdiretoria de Assuntos Civis", "Subdiretoria de Relações Públicas", "Centro de Cerimonial"], "atribuicoes": ["A Diretoria de Assuntos Civis e Relações Públicas tem por competência a gestão dos assuntos civis, relações públicas e cerimonial da corporação (LC nº 52/2001, Art. 34, alt. LC nº 257/2017)"]}]
    },
    "dgof-rr": {
      "name": "Diretoria de Gestão Orçamentária e Financeira", "abbreviation": "DGOF", "category": "Administração Superior (EMG)",
      "subordinadoA": "Estado Maior Geral Bombeiro Militar", "legalRef": "Art. 35",
      "baseLegal": "Lei Complementar nº 52/2001 (alt. LC nº 257/2017)",
      "artigosDeOrigem": ["Art. 35 (DGOF)"],
      "atribuicoes": ["Planejamento administrativo, orçamentário, execução financeira, gestão de projetos estratégicos, licitação, contratos e convênios", "Gestão do Fundo de Reequipamento e de Saúde do CBM"],
      "desdobramentos": ["Subdiretoria de Expediente", "Subdiretoria de Planejamento Administrativo", "Subdiretoria de Planejamento Orçamentário", "Subdiretoria de Execução Financeira", "Subdiretoria de Gestão de Projetos Estratégicos", "Subdiretoria de Licitação, Contratos e Convênios", "Subdiretoria de Gestão do Fundo de Reequipamento e de Saúde do CBM"],
      "cargos": [{"cargo": "Diretor de Gestão Orçamentária e Financeira", "subordinadoA": "Chefe do Estado Maior Geral", "requisito": "Oficial Superior do QOCBM", "desdobramentos": ["Subdiretoria de Expediente", "Subdiretoria de Planejamento Administrativo", "Subdiretoria de Planejamento Orçamentário", "Subdiretoria de Execução Financeira", "Subdiretoria de Gestão de Projetos Estratégicos", "Subdiretoria de Licitação, Contratos e Convênios", "Subdiretoria de Gestão do Fundo de Reequipamento e de Saúde do CBM"], "atribuicoes": ["A Diretoria de Gestão Orçamentária e Financeira tem por competência o planejamento administrativo, orçamentário, execução financeira, gestão de projetos estratégicos, licitação, contratos e convênios, e gestão do Fundo de Reequipamento e de Saúde do CBM (LC nº 52/2001, Art. 35, alt. LC nº 257/2017)"]}]
    },
    "dci-rr": {
      "name": "Diretoria de Controle Interno", "abbreviation": "DCI", "category": "Administração Superior (EMG)",
      "subordinadoA": "Estado Maior Geral Bombeiro Militar", "legalRef": "Art. 35-A",
      "baseLegal": "Lei Complementar nº 52/2001 (incl. LC nº 257/2017)",
      "artigosDeOrigem": ["Art. 35-A (DCI)"],
      "atribuicoes": ["Controle interno da corporação"],
      "desdobramentos": ["Comissão de Controle Interno", "Subdiretoria Administrativa"],
      "cargos": [{"cargo": "Diretor de Controle Interno", "subordinadoA": "Chefe do Estado Maior Geral", "requisito": "Oficial Superior do QOCBM", "desdobramentos": ["Comissão de Controle Interno", "Subdiretoria Administrativa"], "atribuicoes": ["A Diretoria de Controle Interno tem por competência o exercício do controle interno da corporação (LC nº 52/2001, Art. 35-A, incl. LC nº 257/2017)"]}]
    },
    "cmd-op-rr": {
      "name": "Comando Operacional (Capital e Interior)", "abbreviation": "CmdOp", "category": "Administração Setorial",
      "subordinadoA": "Subcomandante Geral", "legalRef": "Art. 37-40",
      "baseLegal": "Lei Complementar nº 52/2001 (alt. LC nº 257/2017)",
      "artigosDeOrigem": ["Art. 37 (Comando Operacional)", "Art. 40 (Estado Maior Operacional)"],
      "atribuicoes": ["Coordenação, controle e fiscalização das atividades operacionais (área setorial)"],
      "desdobramentos": ["Comandante Operacional da Capital", "Comandante Operacional do Interior", "Subcomandantes Operacionais (substitutos e Chefes do Estado Maior Operacional)", "Estado Maior Operacional da Capital", "Estado Maior Operacional do Interior"],
      "cargos": [
        {"cargo": "Comandante Operacional da Capital", "subordinadoA": "Subcomandante Geral", "requisito": "Oficial Superior", "desdobramentos": ["Subcomandante Operacional da Capital", "Estado Maior Operacional da Capital"], "atribuicoes": ["Coordenação, controle e fiscalização das atividades operacionais da Capital"]},
        {"cargo": "Comandante Operacional do Interior", "subordinadoA": "Subcomandante Geral", "requisito": "Oficial Superior", "desdobramentos": ["Subcomandante Operacional do Interior", "Estado Maior Operacional do Interior"], "atribuicoes": ["Coordenação, controle e fiscalização das atividades operacionais do Interior"]}
      ]
    },
    "ceib-rr": {
      "name": "Centro de Ensino e Instrução de Bombeiros", "abbreviation": "CEIB", "category": "Administração Setorial",
      "subordinadoA": "Comando Geral / DEIP", "legalRef": "Art. 36, III; Art. 42",
      "baseLegal": "Lei Complementar nº 52, de 28 de dezembro de 2001",
      "artigosDeOrigem": ["Art. 42 (CEIB)"],
      "atribuicoes": ["Administração das atividades de formação, especialização, aperfeiçoamento e educação continuada dos recursos humanos, bem como a pesquisa e a doutrina da instituição"],
      "desdobramentos": ["Comando", "Subcomando", "Secretaria", "Seção Administrativa", "Seção de Ensino", "Seção de Pesquisa e Doutrina", "Corpo de Alunos"],
      "cargos": [{"cargo": "Comandante do CEIB", "subordinadoA": "Comando Geral / DEIP", "requisito": "", "desdobramentos": [], "atribuicoes": ["Direção do Centro de Ensino e Instrução de Bombeiros (CEIB); dirigido por um Comandante (LC nº 52/2001, Art. 42)"]}]
    },
    "csm-rr": {
      "name": "Centro de Suprimento e Material", "abbreviation": "CSM", "category": "Administração Setorial",
      "subordinadoA": "Diretoria de Logística (DLOG)", "legalRef": "Art. 36, IV; Art. 43",
      "baseLegal": "Lei Complementar nº 52, de 28 de dezembro de 2001",
      "artigosDeOrigem": ["Art. 43 (CSM)"],
      "atribuicoes": ["Planejamento, execução, coordenação, fiscalização e controle das atividades de suprimento e material da corporação"],
      "desdobramentos": ["Seção Administrativa", "Seção de Contabilidade e Auditoria", "Seção de Licitação Permanente", "Almoxarifado Geral", "Aprovisionamento"],
      "cargos": [{"cargo": "Comandante do CSM", "subordinadoA": "Diretoria de Logística (DLOG)", "requisito": "", "desdobramentos": [], "atribuicoes": ["Direção do Centro de Suprimento e Material (CSM); dirigido por um Comandante (LC nº 52/2001, Art. 43)"]}]
    },
    "ceman-rr": {
      "name": "Centro de Manutenção", "abbreviation": "CEMAN", "category": "Administração Setorial",
      "subordinadoA": "Diretoria de Logística (DLOG)", "legalRef": "Art. 36, V; Art. 44",
      "baseLegal": "Lei Complementar nº 52, de 28 de dezembro de 2001",
      "artigosDeOrigem": ["Art. 44 (CEMAN)"],
      "atribuicoes": ["Manutenção de viaturas, equipamento motorizado, materiais em geral e instalações"],
      "desdobramentos": ["Seção Administrativa", "Seção de Manutenção de Viaturas e Equipamentos Motorizados", "Seção de Obras, Serviços Gerais e Manutenção de Instalações Prediais"],
      "cargos": [{"cargo": "Comandante do CEMAN", "subordinadoA": "Diretoria de Logística (DLOG)", "requisito": "", "desdobramentos": [], "atribuicoes": ["Direção do Centro de Manutenção (CEMAN); dirigido por um Comandante (LC nº 52/2001, Art. 44)"]}]
    },
    "cinfor-rr": {
      "name": "Centro de Informática", "abbreviation": "CINFOR", "category": "Administração Setorial",
      "subordinadoA": "Diretoria de Informática e Estatística (DIE)", "legalRef": "Art. 36, VI; Art. 45",
      "baseLegal": "Lei Complementar nº 52/2001 (alt. LC nº 257/2017)",
      "artigosDeOrigem": ["Art. 45 (CINFOR)"],
      "atribuicoes": ["Realizar programas e sistemas para otimização das áreas administrativas e operacionais da corporação"],
      "desdobramentos": ["Seção de Suporte Técnico e Manutenção (Cinf-I)", "Seção de Desenvolvimento e Manutenção de Sistemas (Cinf-II)", "Seção de Suporte de Rede/Intranet (Cinf-III)"],
      "cargos": [{"cargo": "Comandante do CINFOR", "subordinadoA": "Diretoria de Informática e Estatística (DIE)", "requisito": "", "desdobramentos": [], "atribuicoes": ["Direção do Centro de Informática (CINFOR); dirigido por um Comandante (LC nº 52/2001, Art. 45)"]}]
    },
    "cipi-rr": {
      "name": "Centro de Investigação e Prevenção de Incêndios", "abbreviation": "CIPI", "category": "Administração Setorial",
      "subordinadoA": "Diretoria de Prevenção e Serviços Técnicos (DPST)", "legalRef": "Art. 36, VII; Art. 46",
      "baseLegal": "Lei Complementar nº 52, de 28 de dezembro de 2001",
      "artigosDeOrigem": ["Art. 46 (CIPI)"],
      "atribuicoes": ["Serviços de prevenção, investigação, perícias de incêndios e explosões", "Emitir conclusões e laudos técnicos periciais"],
      "desdobramentos": ["Seção Administrativa (CIPI-I)", "Seção de Perícias (CIPI-II)", "Seção de Análises Laboratoriais (CIPI-III)"],
      "cargos": [{"cargo": "Comandante do CIPI", "subordinadoA": "Diretoria de Prevenção e Serviços Técnicos (DPST)", "requisito": "", "desdobramentos": [], "atribuicoes": ["Direção do Centro de Investigação e Prevenção de Incêndios (CIPI); dirigido por um Comandante (LC nº 52/2001, Art. 46)"]}]
    },
    "cesau-rr": {
      "name": "Centro de Saúde", "abbreviation": "CESAU", "category": "Administração Setorial",
      "subordinadoA": "Ajudância Geral", "legalRef": "Art. 36, VIII; Art. 47",
      "baseLegal": "Lei Complementar nº 52/2001 (alt. LC nº 257/2017)",
      "artigosDeOrigem": ["Art. 47 (CESAU)"],
      "atribuicoes": ["Órgão de apoio de saúde e assistência social", "Prestação de serviços de saúde e assistência social aos bombeiros militares e dependentes"],
      "desdobramentos": ["Seção Administrativa", "Seção Médica", "Seção Odontológica", "Seção de Laboratório", "Seção de Ortopedia e Fisioterapia", "Enfermarias", "Seção de Assistência Social", "Seção de Psicologia", "Seção de Farmácia", "Seção de Veterinária"],
      "cargos": [{"cargo": "Comandante do CESAU", "subordinadoA": "Ajudância Geral", "requisito": "", "desdobramentos": [], "atribuicoes": ["Direção do Centro de Saúde (CESAU); dirigido por um Comandante (LC nº 52/2001, Art. 47)"]}]
    },
    "cest-rr": {
      "name": "Centro de Estatística", "abbreviation": "CEST", "category": "Administração Setorial",
      "subordinadoA": "Diretoria de Informática e Estatística (DIE)", "legalRef": "Art. 47-A",
      "baseLegal": "Lei Complementar nº 52/2001 (incl. LC nº 257/2017)",
      "artigosDeOrigem": ["Art. 47-A (CEST)"],
      "atribuicoes": ["Coleta de dados e fornecimento de dados estatísticos"],
      "desdobramentos": ["Seção de Coleta de Dados (CEST-I)", "Seção de Análise e Produção de Estatística (CEST-II)"],
      "cargos": [{"cargo": "Comandante do CEST", "subordinadoA": "Diretoria de Informática e Estatística (DIE)", "requisito": "", "desdobramentos": [], "atribuicoes": ["Direção do Centro de Estatística (CEST); dirigido por um Comandante (LC nº 52/2001, Art. 47-A)"]}]
    },
    "cecer-rr": {
      "name": "Centro de Cerimonial", "abbreviation": "CECER", "category": "Administração Setorial",
      "subordinadoA": "Diretoria de Assuntos Civis e Relações Públicas (DACRP)", "legalRef": "Art. 47-B",
      "baseLegal": "Lei Complementar nº 52/2001 (incl. LC nº 257/2017)",
      "artigosDeOrigem": ["Art. 47-B (CECER)"],
      "atribuicoes": ["Organizar todas as atividades cerimoniais desenvolvidas pela Instituição"],
      "desdobramentos": ["Seção de Cerimonial"],
      "cargos": [{"cargo": "Comandante do CECER", "subordinadoA": "Diretoria de Assuntos Civis e Relações Públicas (DACRP)", "requisito": "", "desdobramentos": [], "atribuicoes": ["Direção do Centro de Cerimonial (CECER); dirigido por um Comandante (LC nº 52/2001, Art. 47-B)"]}]
    },
    "cvap-rr": {
      "name": "Centro de Vistoria e Análise de Projeto", "abbreviation": "CVAP", "category": "Administração Setorial",
      "subordinadoA": "Diretoria de Prevenção e Serviços Técnicos (DPST)", "legalRef": "Art. 47-C",
      "baseLegal": "Lei Complementar nº 52/2001 (incl. LC nº 257/2017)",
      "artigosDeOrigem": ["Art. 47-C (CVAP)"],
      "atribuicoes": ["Prestação de serviços de vistoria e análise de projetos técnicos"],
      "desdobramentos": ["Seção Administrativa (CVAP-I)", "Seção de Análise de Projetos (CVAP-II)", "Seção de Vistorias e Pareceres (CVAP-III)", "Seção de Estudos e Pesquisas de Normas Técnicas (CVAP-IV)", "Seção de Fiscalização (CVAP-V)"],
      "cargos": [{"cargo": "Comandante do CVAP", "subordinadoA": "Diretoria de Prevenção e Serviços Técnicos (DPST)", "requisito": "", "desdobramentos": [], "atribuicoes": ["Direção do Centro de Vistoria e Análise de Projeto (CVAP); dirigido por um Comandante (LC nº 52/2001, Art. 47-C)"]}]
    },
    "exec-op-rr": {
      "name": "Órgãos de Execução Operacional", "abbreviation": "OEO", "category": "Execução",
      "subordinadoA": "Comando Operacional", "legalRef": "Art. 49-52",
      "baseLegal": "Lei Complementar nº 52, de 28 de dezembro de 2001",
      "artigosDeOrigem": ["Art. 49 (OBMs de Atuação Direta Operacionais)", "Art. 50 (Tipos)"],
      "atribuicoes": ["OBMs de Atuação Direta Operacionais", "Classificam-se em Ordinárias, Especializadas, Particulares e Voluntárias"],
      "desdobramentos": ["Batalhão de Bombeiros", "Companhia Independente de Bombeiros", "Companhia de Bombeiros", "Companhia de Comando e Serviço", "Pelotão de Bombeiros", "Pelotão de Comando e Serviço", "Destacamento de Bombeiros"],
      "cargos": []
    },
    "exec-prev-rr": {
      "name": "Órgãos de Execução Prevencional", "abbreviation": "OEP", "category": "Execução",
      "subordinadoA": "Diretoria de Prevenção e Serviços Técnicos (DPST)", "legalRef": "Art. 53",
      "baseLegal": "Lei Complementar nº 52, de 28 de dezembro de 2001",
      "artigosDeOrigem": ["Art. 53 (Órgãos de Execução Prevencional)"],
      "atribuicoes": ["OBMs de Atuação Direta Prevencionais", "Perícia técnica, prevenção, vistoria e análise de projetos"],
      "desdobramentos": ["Subdiretoria de Hidrantes", "Centro de Investigação e Prevenção de Incêndios (CIPI)", "Centro de Vistoria e Análise de Projetos (CVAP)"],
      "cargos": []
    },
    "exec-estr-rr": {
      "name": "Órgãos de Execução Estratégica", "abbreviation": "OEE", "category": "Execução",
      "subordinadoA": "Comando Geral / EMG", "legalRef": "Art. 54",
      "baseLegal": "Lei Complementar nº 52, de 28 de dezembro de 2001",
      "artigosDeOrigem": ["Art. 54 (Órgãos de Execução Estratégica)"],
      "atribuicoes": ["OBMs de Atuação Direta Estratégicas (ensino, saúde, informática, cerimonial e estatística)"],
      "desdobramentos": ["Centro de Ensino e Instrução de Bombeiros (CEIB)", "Centro de Saúde (CESAU)", "Centro de Informática (CINFOR)", "Centro de Cerimonial (CECER)", "Centro de Estatísticas (CEST)"],
      "cargos": []
    },
    "exec-log-rr": {
      "name": "Órgãos de Execução Logística", "abbreviation": "OEL", "category": "Execução",
      "subordinadoA": "Diretoria de Logística (DLOG)", "legalRef": "Art. 55",
      "baseLegal": "Lei Complementar nº 52, de 28 de dezembro de 2001",
      "artigosDeOrigem": ["Art. 55 (Órgãos de Execução Logística)"],
      "atribuicoes": ["OBMs de Suporte: suprimento, material e manutenção"],
      "desdobramentos": ["Centro de Suprimento e Material (CSM)", "Centro de Manutenção (CEMAN)"],
      "cargos": []
    }
  }
},

"rn": {
  "legal_source": "Decreto nº 31.139, de 1º de dezembro de 2021 (Regulamento Geral do CBMRN); LC nº 230/2002 (alt. até LC nº 791/2025)",
  "organs": {
    "cmt-rn": {
      "name": "Comandante-Geral", "abbreviation": "CG", "category": "Direção Superior",
      "subordinadoA": "Governador do Estado (por intermédio da SESED)", "legalRef": "Art. 12; Art. 13",
      "baseLegal": "Decreto nº 31.139/2021 (Regulamento Geral do CBMRN)",
      "artigosDeOrigem": ["Art. 12 (caput)", "Art. 13 (competências, I-XIX)", "Art. 14 (requisito do cargo)"],
      "atribuicoes": [
        "O Comandante Geral do Corpo de Bombeiros Militar do Estado do Rio Grande do Norte é o responsável pelo comando, coordenação, supervisão e orientação da execução das atividades da Corporação (Art. 12)",
        "I - assessorar o Governador do Estado e o Secretário de Estado da Segurança Pública e da Defesa Social nos assuntos relacionados às atividades de bombeiro militar, defesa civil e guarda militar do meio ambiente;",
        "II - dirigir, coordenar, supervisionar e orientar as atividades técnicas, operacionais e administrativas da Corporação;",
        "III - fazer cumprir as leis, normas e regulamentos da Corporação;",
        "IV - editar portarias e demais normas e diretrizes de serviço;",
        "V - submeter ao Secretário de Estado da Segurança Pública e da Defesa Social, no início de cada exercício, o relatório das atividades desenvolvidas pelo Corpo de Bombeiros Militar durante o ano anterior, sugerindo a adoção de medidas legislativas e as providências adequadas ao seu aperfeiçoamento, como estudos, projetos, programas e propostas para a organização, o funcionamento e a atuação da Instituição, com vista ao desenvolvimento da segurança;",
        "VI - determinar a instauração de sindicância e de processo administrativo disciplinar, bem como aplicar as penalidades de sua competência;",
        "VII - convocar e presidir as reuniões do Conselho Superior do Corpo de Bombeiros Militar;",
        "VIII - celebrar convênios e ajustes com entidades públicas e privadas visando formar parcerias com vistas à otimização das funções institucionais do Corpo de Bombeiros Militar;",
        "IX - presidir a elaboração da proposta orçamentária do Corpo de Bombeiros Militar, bem como praticar os atos necessários de gestão orçamentária e financeira;",
        "X - determinar a realização de licitações, inexigi-las, dispensá-las, aprová-las, anulá-las ou revogá-las;",
        "XI - presidir e designar os demais membros da Comissão Organizadora e Examinadora dos concursos para ingresso na carreira de oficiais e praças, bem como as condições necessárias à inscrição de candidato, atendendo previamente às normas estabelecidas pelo Conselho Superior do Corpo de Bombeiros Militar;",
        "XII - antecipar ou prorrogar a jornada normal de trabalho, bem como definir normas e critérios para o cumprimento do expediente regular do Corpo de Bombeiros Militar;",
        "XIII - propor e conceder gratificações, na forma da legislação vigente;",
        "XIV - designar ou dispensar os ocupantes de comando, diretorias, chefias, funções gratificadas ou de confiança, bem como os seus eventuais substitutos;",
        "XV - disciplinar o uso dos uniformes militares, nos termos da legislação em vigor;",
        "XVI - decidir nos processos relativos aos interesses do Corpo de Bombeiro Militar, inclusive os referentes a direitos e deveres dos oficiais e praças e dos servidores civis da Instituição;",
        "XVII - determinar a publicação semestral da relação de antiguidade dos Oficiais e Praças da Corporação em Boletim Geral, até 31 de janeiro e 31 de julho;",
        "XVIII - determinar a realização de exame de sanidade para a verificação da incapacidade física ou mental de Praças e Oficiais, temporária ou definitiva, por intermédio da Junta Médica da Instituição;",
        "XIX - desempenhar outras atividades definidas em lei."
      ],
      "desdobramentos": [],
      "cargos": [{
        "cargo": "Comandante-Geral",
        "subordinadoA": "Governador do Estado (via SESED)",
        "requisito": "Oficial superior da ativa, do último posto do QOCBM, com Curso Superior de Bombeiro Militar ou equivalente, nomeado e exonerado por ato do Governador (Art. 14)",
        "desdobramentos": [],
        "atribuicoes": [
          "I - assessorar o Governador do Estado e o Secretário de Estado da Segurança Pública e da Defesa Social nos assuntos relacionados às atividades de bombeiro militar, defesa civil e guarda militar do meio ambiente;",
          "II - dirigir, coordenar, supervisionar e orientar as atividades técnicas, operacionais e administrativas da Corporação;",
          "III - fazer cumprir as leis, normas e regulamentos da Corporação;",
          "IV - editar portarias e demais normas e diretrizes de serviço;",
          "IX - presidir a elaboração da proposta orçamentária do Corpo de Bombeiros Militar, bem como praticar os atos necessários de gestão orçamentária e financeira;"
        ]
      }]
    },
    "scmt-rn": {
      "name": "Subcomandante-Geral", "abbreviation": "SCG", "category": "Direção Superior",
      "subordinadoA": "Comandante-Geral", "legalRef": "Art. 15",
      "baseLegal": "Decreto nº 31.139/2021 (Regulamento Geral do CBMRN)",
      "artigosDeOrigem": ["Art. 15 (competências, I-XIII)", "Art. 16 (requisito do cargo)"],
      "atribuicoes": [
        "O Subcomandante Geral é o auxiliar direto do Comandante Geral da Corporação, substituindo-o em seus eventuais impedimentos, desempenhando as atribuições previstas em Lei e regulamentos, competindo-lhe: (Art. 15, caput)",
        "I - substituir o Comandante Geral nas suas ausências ou impedimentos legais;",
        "II - assessorar o Comandante Geral na gestão administrativa, técnica e operacional da corporação, por meio do controle das atividades dos órgãos de direção geral e assessoramento;",
        "III - coordenar a elaboração do planejamento estratégico da corporação, assim como aplicá-lo;",
        "IV - assessorar o Comandante Geral na formulação da doutrina de preparo e emprego da tropa e na definição das políticas de comando;",
        "V - assegurar a atuação convergente e dinâmica dos órgãos de direção geral, assessoramento e execução;",
        "VI - elaborar e estabelecer ordens, instruções, diretrizes, planos e orientações pertinentes à implementação das políticas do Comandante Geral, visando à consecução dos objetivos e metas estabelecidas no planejamento estratégico ou planos de ação;",
        "VII - supervisionar a execução das diretrizes, planos e ordens;",
        "VIII - realizar inspeção periódica nas Organizações Bombeiro Militar (OBM);",
        "IX - desempenhar outras atribuições delegadas pelo Comandante Geral;",
        "X - presidir a Comissão de Promoção de Praças (CPP);",
        "XI - encarregar-se pelo nível de disciplina dos militares da Corporação;",
        "XII - presidir, como membro nato, as atividades desenvolvidas na Comissão Permanente de Ética e Disciplina (CPED);",
        "XIII - exercer demais atribuições definidas na legislação em vigor."
      ],
      "desdobramentos": [],
      "cargos": [{
        "cargo": "Subcomandante-Geral",
        "subordinadoA": "Comandante-Geral",
        "requisito": "Oficial superior da ativa, do último posto do QOCBM, com Curso Superior de Bombeiro Militar ou equivalente, nomeado e exonerado por ato do Governador (Art. 16)",
        "desdobramentos": [],
        "atribuicoes": [
          "I - substituir o Comandante Geral nas suas ausências ou impedimentos legais;",
          "II - assessorar o Comandante Geral na gestão administrativa, técnica e operacional da corporação;",
          "X - presidir a Comissão de Promoção de Praças (CPP);",
          "XII - presidir, como membro nato, as atividades desenvolvidas na Comissão Permanente de Ética e Disciplina (CPED);"
        ]
      }]
    },
    "csup-rn": {
      "name": "Conselho Superior", "abbreviation": "CS", "category": "Deliberação Coletiva",
      "subordinadoA": "Comandante-Geral", "legalRef": "Art. 17",
      "baseLegal": "Decreto nº 31.139/2021 (Regulamento Geral do CBMRN)",
      "artigosDeOrigem": ["Art. 17 (atribuições, I-IX)", "Art. 18 (composição)"],
      "atribuicoes": [
        "Órgão de deliberação coletiva que assessora o Comandante Geral na formulação e avaliação de políticas estratégicas e na fixação de diretrizes de gerenciamento administrativo e operacional do Corpo de Bombeiros Militar (Art. 17, caput)",
        "I - aprovar a proposta orçamentária do Corpo de Bombeiros Militar;",
        "II - aprovar o relatório geral e anual do Corpo de Bombeiros Militar;",
        "III - deliberar sobre qualquer matéria de interesse do Corpo de Bombeiros Militar, que lhe seja submetida por quaisquer de seus membros, com anuência do Comandante Geral;",
        "IV - dirimir quaisquer dúvidas ou omissões atinentes à competência dos órgãos que integram o Corpo de Bombeiros Militar;",
        "V - analisar regras, critérios e princípios para a realização de concurso público para ingresso nas carreiras de Oficiais e Praças da Instituição, propostas pelo Comandante Geral, observado o disposto em lei;",
        "VI - estabelecer o padrão dos símbolos do Corpo de Bombeiros Militar;",
        "VII - deliberar sobre os processos de promoção de Oficiais e Praças da Corporação;",
        "VIII - estabelecer as diretrizes do Fundo de Reaparelhamento do Corpo de Bombeiros Militar (FUNREBOM);",
        "IX - elaborar o seu regimento interno."
      ],
      "desdobramentos": [],
      "cargos": [{
        "cargo": "Presidente do Conselho Superior (Comandante-Geral)",
        "subordinadoA": "—",
        "requisito": "Presidido pelo Comandante-Geral; membros natos: SCG, Cmdo Op BM, Diretores de DLOF/DGPEI/DAT e Ajudante Geral (Art. 18)",
        "desdobramentos": [],
        "atribuicoes": ["Presidência do órgão de deliberação coletiva de assessoramento estratégico do CBMRN (Art. 17)"]
      }]
    },
    "gab-rn": {
      "name": "Gabinete do Comando Geral", "abbreviation": "Gab.CG", "category": "Assessoramento",
      "subordinadoA": "Comandante-Geral", "legalRef": "Art. 19",
      "baseLegal": "Decreto nº 31.139/2021 (Regulamento Geral do CBMRN)",
      "artigosDeOrigem": ["Art. 19 (competências, I-V)"],
      "atribuicoes": [
        "O Gabinete do Comando Geral é o seu órgão de apoio administrativo e de representação social, competindo-lhe: (Art. 19, caput)",
        "I - redigir e preparar o expediente pessoal do Comandante Geral e do Subcomandante Geral e organizar suas agendas de despachos e de compromissos, assim como fornecer informações administrativas aos demais órgãos do Corpo de Bombeiros Militar;",
        "II - coordenar a recepção e o atendimento ao público;",
        "III - assistir ao Comandante Geral e ao Subcomandante Geral nas suas atividades de relações internas e externas;",
        "IV - promover, junto aos órgãos de imprensa, a divulgação de informações sobre a atuação e as atividades do Corpo de Bombeiros Militar;",
        "V - exercer outras atividades que lhe forem cometidas pelo Comandante Geral e Subcomandante Geral."
      ],
      "desdobramentos": [],
      "cargos": [{
        "cargo": "Chefe do Gabinete do Comando Geral",
        "subordinadoA": "Comandante-Geral",
        "requisito": "Oficial BM de livre escolha do Comandante Geral; acumula com a função de Ajudante Geral (Art. 22, parágrafo único)",
        "desdobramentos": [],
        "atribuicoes": ["Apoio administrativo e representação social do Comando Geral; redação do expediente pessoal do CG e SCG; coordenação do atendimento ao público (Art. 19)"]
      }]
    },
    "aj-rn": {
      "name": "Assessoria Jurídica", "abbreviation": "AJ", "category": "Assessoramento",
      "subordinadoA": "Comandante-Geral", "legalRef": "Art. 20",
      "baseLegal": "Decreto nº 31.139/2021 (Regulamento Geral do CBMRN)",
      "artigosDeOrigem": ["Art. 20 (caput)"],
      "atribuicoes": [
        "A Assessoria Jurídica é o órgão que presta assessoramento direto ao Comandante Geral do Corpo de Bombeiros Militar, competindo-lhe o estudo de questões de direito compreendidas na política de administração geral da corporação, o exame dos aspectos de legalidade dos atos e normas que lhe forem submetidas à apreciação e demais atribuições que venham a ser previstas em regulamento (Art. 20)."
      ],
      "desdobramentos": [],
      "cargos": [{
        "cargo": "Assessor Jurídico",
        "subordinadoA": "Comandante-Geral",
        "requisito": "Oficial BM com formação jurídica, designado pelo Comandante Geral",
        "desdobramentos": [],
        "atribuicoes": ["Assessoramento jurídico direto ao Comandante Geral; estudo de questões de direito e exame da legalidade dos atos e normas (Art. 20)"]
      }]
    },
    "ajg-rn": {
      "name": "Ajudância Geral", "abbreviation": "AjG", "category": "Assessoramento",
      "subordinadoA": "Comandante-Geral", "legalRef": "Art. 22",
      "baseLegal": "Decreto nº 31.139/2021 (Regulamento Geral do CBMRN)",
      "artigosDeOrigem": ["Art. 22 (caput e parágrafo único)"],
      "atribuicoes": [
        "A Ajudância Geral é o órgão encarregado do expediente, da execução dos trabalhos de secretaria geral, incluindo a expedição e recebimento de correspondência, correios, redação e impressão do boletim diário do Comando Geral, do protocolo, do apoio em pessoal aos órgãos que compõem o Comando Geral, dos serviços gerais e da segurança do Quartel do Comando do Corpo de Bombeiros Militar do Rio Grande do Norte, competindo-lhe ainda, elaborar e redigir as 'Ordens do Dia' e discursos do Comandante Geral e preparar os processos de seleção e agraciamento das diversas comendas institucionais (Art. 22)."
      ],
      "desdobramentos": ["Secretaria Geral", "Seção de Administração", "Seção de Comando e Serviço", "Protocolo Geral"],
      "cargos": [{
        "cargo": "Ajudante Geral",
        "subordinadoA": "Comandante-Geral",
        "requisito": "Oficial Superior Bombeiro Militar, de livre escolha do Comandante Geral; acumula com a função de Chefe de Gabinete do Comando Geral (Art. 22, parágrafo único)",
        "desdobramentos": [],
        "atribuicoes": ["Expediente geral, secretaria, protocolo e segurança do Quartel-General do CBMRN; redação das 'Ordens do Dia' e discursos do CG; processos de agraciamento (Art. 22)"]
      }]
    },
    "uci-rn": {
      "name": "Unidade de Controle Interno", "abbreviation": "UCI", "category": "Assessoramento",
      "subordinadoA": "Comandante-Geral", "legalRef": "Art. 24",
      "baseLegal": "Decreto nº 31.139/2021 (Regulamento Geral do CBMRN)",
      "artigosDeOrigem": ["Art. 24 (competências, I-IX)"],
      "atribuicoes": [
        "A Unidade de Controle Interno (UCI) é o órgão responsável pela análise dos processos de aquisição de materiais e equipamentos de qualquer natureza, contratação de serviços e despesas com pessoal no âmbito do CBMRN, competindo-lhe: (Art. 24, caput)",
        "I - controlar e fiscalizar todas as atividades relativas à compra e pagamento do CBMRN;",
        "II - conferir cálculos e planilhas de toda compra do CBMRN;",
        "III - conferir índices de reajustes ou de atualização aplicados nos contratos do CBMRN;",
        "IV - exercer o controle contábil, financeiro, orçamentário, operacional e patrimonial, quanto à legalidade, legitimidade, economicidade e razoabilidade;",
        "V - exercer o Controle Interno das operações de créditos, bem como da execução de convênios, contratos e licitações, relativos aos direitos e haveres do CBMRN;",
        "VI - avaliar a correta aplicação das disposições contidas na legislação em vigor quanto aos limites de gastos e outras decorrentes, apresentando informações que auxiliem neste processo;",
        "VII - monitorar e colaborar na implementação e no cumprimento de todas as disposições contidas nas deliberações expedidas pelos Órgãos de Controle Externos;",
        "VIII - supervisionar os processos de controles internos;",
        "IX - outras atribuições definidas em lei."
      ],
      "desdobramentos": [],
      "cargos": [{
        "cargo": "Chefe da Unidade de Controle Interno",
        "subordinadoA": "Comandante-Geral",
        "requisito": "Oficial BM designado por ato do Comandante Geral; pode acumular com outra função (Art. 46)",
        "desdobramentos": [],
        "atribuicoes": [
          "I - controlar e fiscalizar todas as atividades relativas à compra e pagamento do CBMRN;",
          "IV - exercer o controle contábil, financeiro, orçamentário, operacional e patrimonial, quanto à legalidade, legitimidade, economicidade e razoabilidade;",
          "V - exercer o Controle Interno das operações de créditos, bem como da execução de convênios, contratos e licitações;"
        ]
      }]
    },
    "cpp-rn": {
      "name": "Comissão de Promoção de Praças", "abbreviation": "CPP", "category": "Assessoramento",
      "subordinadoA": "Subcomandante-Geral (presidente)", "legalRef": "Art. 26",
      "baseLegal": "Decreto nº 31.139/2021 (Regulamento Geral do CBMRN)",
      "artigosDeOrigem": ["Art. 26 (competências, I-III)"],
      "atribuicoes": [
        "A Comissão de Promoção de Praças do Corpo de Bombeiros Militar do Rio Grande do Norte (CPP/CBMRN) é um órgão consultivo e deliberativo integrante da estrutura administrativa do CBMRN, competindo-lhe: (Art. 26, caput)",
        "I - assessorar, estudar e propor ao Comandante Geral as diretrizes que visem a garantir às Praças do CBMRN o direito à promoção de forma seletiva, gradual e sucessiva;",
        "II - deliberar, no âmbito da sua competência, acerca da existência ou não do preenchimento dos requisitos objetivos ou subjetivos ensejadores da promoção das Praças do CBMRN;",
        "III - desempenhar atividades correlatas determinadas pelo Comandante Geral, bem como outras funções definidas na legislação em vigor."
      ],
      "desdobramentos": [],
      "cargos": [{
        "cargo": "Presidente da CPP (Subcomandante-Geral)",
        "subordinadoA": "Comandante-Geral",
        "requisito": "Presidida pelo Subcomandante-Geral (Art. 15, X); membros designados por ato do CG",
        "desdobramentos": [],
        "atribuicoes": [
          "I - assessorar, estudar e propor ao Comandante Geral as diretrizes que visem a garantir às Praças do CBMRN o direito à promoção de forma seletiva, gradual e sucessiva;",
          "II - deliberar acerca da existência ou não do preenchimento dos requisitos ensejadores da promoção das Praças do CBMRN;"
        ]
      }]
    },
    "cped-rn": {
      "name": "Comissão Permanente de Ética e Disciplina", "abbreviation": "CPED", "category": "Assessoramento",
      "subordinadoA": "Subcomandante-Geral (presidente)", "legalRef": "Art. 23",
      "baseLegal": "Decreto nº 31.139/2021 (Regulamento Geral do CBMRN)",
      "artigosDeOrigem": ["Art. 23 (caput)"],
      "atribuicoes": [
        "A Comissão Permanente de Ética e Disciplina será nomeada anualmente por ato do Comandante Geral do CBMRN, podendo ser reconduzida por iguais e sucessivos períodos, limitado até 60 (sessenta) meses, e será presidida pelo Subcomandante Geral, competindo-lhe analisar o nível disciplinar da tropa, propor medidas de correção, acompanhamento e fiscalização dos processos e procedimentos administrativos disciplinares, examinar fatos, circunstâncias e consequências de atos que afetem o bom desempenho da atividade Bombeiro Militar ou decoro da Corporação (Art. 23)."
      ],
      "desdobramentos": [],
      "cargos": [{
        "cargo": "Presidente da CPED (Subcomandante-Geral)",
        "subordinadoA": "Comandante-Geral",
        "requisito": "Presidida pelo Subcomandante-Geral como membro nato (Art. 15, XII)",
        "desdobramentos": [],
        "atribuicoes": ["Presidência da comissão responsável por analisar o nível disciplinar da tropa e propor medidas de correção (Art. 23)"]
      }]
    },
    "assint-rn": {
      "name": "Assessoria de Inteligência", "abbreviation": "ASSINT", "category": "Assessoramento",
      "subordinadoA": "Comandante-Geral", "legalRef": "Art. 30",
      "baseLegal": "Decreto nº 31.139/2021 (Regulamento Geral do CBMRN)",
      "artigosDeOrigem": ["Art. 30 (caput e parágrafo único)"],
      "atribuicoes": [
        "A Assessoria de Inteligência é o Órgão de Assessoramento Superior incumbido de assessorar o Comandante Geral nos assuntos de controle interno, identificação e avaliação dos pontos críticos que possam ameaçar a comunidade potiguar. O Assessor de Inteligência tem a competência de produzir informações estratégicas com vistas ao preparo e emprego do Corpo de Bombeiros Militar (Art. 30)."
      ],
      "desdobramentos": [],
      "cargos": [{
        "cargo": "Assessor de Inteligência",
        "subordinadoA": "Comandante-Geral",
        "requisito": "Oficial Superior do QOCBM (Art. 30, parágrafo único)",
        "desdobramentos": [],
        "atribuicoes": ["Assessorar o Comandante Geral nos assuntos de controle interno e identificação de pontos críticos; produzir informações estratégicas com vistas ao preparo e emprego do CBMRN (Art. 30)"]
      }]
    },
    "cmdoop-rn": {
      "name": "Comando Operacional Bombeiro Militar", "abbreviation": "CmdoOpBM", "category": "Execução",
      "subordinadoA": "Conselho Superior (membro)", "legalRef": "Art. 32",
      "baseLegal": "Decreto nº 31.139/2021 (Regulamento Geral do CBMRN)",
      "artigosDeOrigem": ["Art. 32 (caput e parágrafo único)"],
      "atribuicoes": [
        "O Comando Operacional Bombeiro Militar (Cmdo Op BM) é o órgão responsável pelo planejamento, orientação normativa, coordenação, fiscalização, controle e execução das atividades operacionais no campo de atuação da Corporação (Art. 32)."
      ],
      "desdobramentos": ["Estado-Maior Operacional (EM Op)", "Centro de Operações do CBMRN (COCBM)", "Comissão de Defesa Civil (CODEC)", "1º Grupamento de Bombeiros Militar", "2º Grupamento de Bombeiros Militar", "Grupamento de Bombeiros Marítimo (GBMAR)", "Subgrupamento Independente de APH (SIBM-APH)", "1º Subgrupamento Independente de Bombeiros Militar", "2º Subgrupamento Independente de Bombeiros Militar"],
      "cargos": [{
        "cargo": "Comandante Operacional Bombeiro Militar",
        "subordinadoA": "Comandante-Geral",
        "requisito": "Coronel ou Tenente-Coronel do QOCBM (Art. 45)",
        "desdobramentos": [],
        "atribuicoes": ["Planejamento, orientação normativa, coordenação, fiscalização, controle e execução das atividades operacionais no campo de atuação da Corporação (Art. 32)"]
      }]
    },
    "emop-rn": {
      "name": "Estado-Maior Operacional", "abbreviation": "EM Op", "category": "Execução",
      "subordinadoA": "Comando Operacional Bombeiro Militar", "legalRef": "Art. 33",
      "baseLegal": "Decreto nº 31.139/2021 (Regulamento Geral do CBMRN)",
      "artigosDeOrigem": ["Art. 33 (caput; §1º I-VI; §§2º-5º)"],
      "atribuicoes": [
        "O Estado-Maior Operacional (EM Op), subordinado ao Comandante Operacional, é a estrutura de assessoramento responsável pela coordenação setorial do Comando Operacional, atuando na supervisão das atividades de proteção e defesa civil, proteção do meio ambiente, combate a incêndio, resgate, busca e salvamento de vidas e bens em todo o Estado (Art. 33, caput)",
        "Composição: 1ª Seção (B/1) — supervisão de organização e emprego de pessoal e controle de efetivo (Art. 33 §2º)",
        "2ª Seção (B/2) — responsável pela coleta de dados, produção de informes e estudos de inteligência e contrainteligência (Art. 33 §3º)",
        "3ª Seção (B/3) — planejamento de operações, organização, instrução, mobilização e desmobilização e planos de operações futuras (Art. 33 §4º)",
        "4ª Seção (B/4) — orientação das prioridades de apoio logístico operacional e distribuição de equipamentos e suprimentos (Art. 33 §5º)"
      ],
      "desdobramentos": ["1ª Seção (B/1)", "2ª Seção (B/2)", "3ª Seção (B/3)", "4ª Seção (B/4)"],
      "cargos": [{
        "cargo": "Subcomandante Operacional / Chefe do EM Op",
        "subordinadoA": "Comandante Operacional Bombeiro Militar",
        "requisito": "Oficial do QOCBM; substituto do Comandante Operacional",
        "desdobramentos": [],
        "atribuicoes": [
          "I - realizar estudos de situação;",
          "II - apresentar propostas;",
          "III - elaborar planos e ordens;",
          "IV - supervisionar a execução dos planos e ordens previstos no inciso anterior;",
          "V - substituir o Comandante Operacional;",
          "VI - desempenhar as atribuições previstas em lei e regulamentos."
        ]
      }]
    },
    "cocbm-rn": {
      "name": "Centro de Operações do CBMRN", "abbreviation": "COCBM", "category": "Execução",
      "subordinadoA": "Comando Operacional Bombeiro Militar", "legalRef": "Art. 33 §7º",
      "baseLegal": "Decreto nº 31.139/2021 (Regulamento Geral do CBMRN)",
      "artigosDeOrigem": ["Art. 33 §7º (competências)"],
      "atribuicoes": [
        "O Centro de Operações do Corpo de Bombeiros (COCBM) tem por competência coordenar o atendimento e despachos de ocorrências bombeiro-militar e de proteção e defesa civil, bem como coordenar, orientar e disciplinar as telecomunicações operacionais no âmbito do CBMRN (Art. 33 §7º)."
      ],
      "desdobramentos": ["Seção de Operações", "Seção de Comunicações", "Seção de Apoio"],
      "cargos": [{
        "cargo": "Chefe do Centro de Operações",
        "subordinadoA": "Comando Operacional BM",
        "requisito": "Oficial BM designado pelo Comandante Geral",
        "desdobramentos": [],
        "atribuicoes": ["Coordenação do atendimento e despachos de ocorrências BM e de proteção e defesa civil; coordenação e disciplina das telecomunicações operacionais do CBMRN (Art. 33 §7º)"]
      }]
    },
    "codec-rn": {
      "name": "Comissão de Defesa Civil", "abbreviation": "CODEC", "category": "Execução",
      "subordinadoA": "Comando Operacional Bombeiro Militar", "legalRef": "Art. 33 §8º",
      "baseLegal": "Decreto nº 31.139/2021 (Regulamento Geral do CBMRN)",
      "artigosDeOrigem": ["Art. 33 §8º (competências)"],
      "atribuicoes": [
        "A Comissão de Defesa Civil (CODEC) tem por competência a coordenação de ações preventivas e de socorro emergencial, com vistas a evitar ou minimizar os efeitos desastrosos de situações adversas que possam causar danos à sociedade, promovendo estudo em áreas de risco, organizando banco de dados em mapeamento de áreas críticas relacionadas com as ameaças e vulnerabilidade aos riscos naturais de maior prevalência no Estado (Art. 33 §8º)."
      ],
      "desdobramentos": ["Subcomissão de ações preventivas", "Subcomissão de ações de emergência", "Subcomissão de ações de apoio"],
      "cargos": [{
        "cargo": "Presidente da CODEC",
        "subordinadoA": "Comando Operacional BM",
        "requisito": "Oficial BM designado pelo Comandante Geral",
        "desdobramentos": [],
        "atribuicoes": ["Coordenação de ações preventivas e de socorro emergencial de defesa civil; mapeamento de áreas críticas e vulnerabilidade aos riscos naturais (Art. 33 §8º)"]
      }]
    },
    "gbm1-rn": {
      "name": "1º Grupamento de Bombeiros Militar", "abbreviation": "1º GBM", "category": "Execução",
      "subordinadoA": "Comando Operacional Bombeiro Militar", "legalRef": "Art. 32 §9º",
      "baseLegal": "Decreto nº 31.139/2021 (Regulamento Geral do CBMRN)",
      "artigosDeOrigem": ["Art. 32 §9º (missão e composição)"],
      "atribuicoes": [
        "O Primeiro Grupamento de Bombeiros Militar (1º GBM) é a unidade operacional do Corpo de Bombeiros Militar, responsável pela operacionalização das atividades de prevenção e combate a incêndio, busca e resgate de pessoas e bens, compreendendo as atividades de salvamento terrestre e em altura, bem como a defesa do meio ambiente, atuando como órgão estadual encarregado da guarda militar do patrimônio ambiental do Estado, na capital e região metropolitana do Estado (Art. 32 §9º)."
      ],
      "desdobramentos": ["Divisão Administrativa", "Divisão de Operações", "1º Subgrupamento de Bombeiros", "2º Subgrupamento de Bombeiros", "3º Subgrupamento de Bombeiros"],
      "cargos": [{
        "cargo": "Comandante do 1º GBM",
        "subordinadoA": "Comandante Operacional BM",
        "requisito": "Major ou Tenente-Coronel do QOCBM",
        "desdobramentos": [],
        "atribuicoes": ["Comandar a unidade operacional responsável pelas atividades de prevenção, combate a incêndio, busca e resgate na capital e região metropolitana do Estado (Art. 32 §9º)"]
      }]
    },
    "gbm2-rn": {
      "name": "2º Grupamento de Bombeiros Militar", "abbreviation": "2º GBM", "category": "Execução",
      "subordinadoA": "Comando Operacional Bombeiro Militar", "legalRef": "Art. 32 §10º",
      "baseLegal": "Decreto nº 31.139/2021 (Regulamento Geral do CBMRN)",
      "artigosDeOrigem": ["Art. 32 §10º (missão e composição)"],
      "atribuicoes": [
        "O Segundo Grupamento de Bombeiros Militar (2º GBM) é a unidade operacional do Corpo de Bombeiros Militar, responsável pela operacionalização das atividades de prevenção e combate a incêndio, de busca e resgate de pessoas e bens, compreendendo as atividades de salvamento terrestre, em altura e aquático, e atendimento pré-hospitalar de urgência, nos municípios localizados no interior do Estado do Rio Grande do Norte (Art. 32 §10º)."
      ],
      "desdobramentos": ["Divisão Administrativa", "Divisão de Operações", "1º Subgrupamento de Bombeiros (Mossoró/RN)", "2º Subgrupamento de Bombeiros (Caicó/RN)", "3º Subgrupamento de Bombeiros (Pau dos Ferros/RN)"],
      "cargos": [{
        "cargo": "Comandante do 2º GBM",
        "subordinadoA": "Comandante Operacional BM",
        "requisito": "Major ou Tenente-Coronel do QOCBM",
        "desdobramentos": [],
        "atribuicoes": ["Comandar a unidade operacional responsável por incêndio, busca, resgate e APH nos municípios do interior do Estado do RN (Art. 32 §10º)"]
      }]
    },
    "gbmar-rn": {
      "name": "Grupamento de Bombeiros Marítimo", "abbreviation": "GBMAR", "category": "Execução",
      "subordinadoA": "Comando Operacional Bombeiro Militar", "legalRef": "Art. 32 §11º",
      "baseLegal": "Decreto nº 31.139/2021 (Regulamento Geral do CBMRN)",
      "artigosDeOrigem": ["Art. 32 §11º (missão e composição)"],
      "atribuicoes": [
        "O Grupamento de Bombeiros Marítimo (GBMAR) é a unidade operacional do Corpo de Bombeiros Militar, responsável pela operacionalização das diretrizes e procedimentos referentes aos serviços e técnicas de salvamento aquático, procedimentos de primeiros socorros e noções básicas de marinharia, visando a busca e resgate de pessoas e bens, compreendendo as atividades de salvamento aquático, a prevenção contra afogamentos e a normalização e fiscalização de atividades esportivas e recreativas em áreas de risco em seu campo de atuação (Art. 32 §11º)."
      ],
      "desdobramentos": ["Divisão Administrativa", "Divisão de Operações", "1º SBMSA", "2º SBMSA", "3º SBMSA"],
      "cargos": [{
        "cargo": "Comandante do GBMAR",
        "subordinadoA": "Comandante Operacional BM",
        "requisito": "Oficial do QOCBM",
        "desdobramentos": [],
        "atribuicoes": ["Comandar a unidade responsável pelo salvamento aquático, prevenção contra afogamentos e fiscalização de atividades esportivas e recreativas em áreas de risco (Art. 32 §11º)"]
      }]
    },
    "sibm-aph-rn": {
      "name": "Subgrupamento Independente de Bombeiros Militar de APH", "abbreviation": "SIBM-APH", "category": "Execução",
      "subordinadoA": "Comando Operacional Bombeiro Militar", "legalRef": "Art. 32 §12º",
      "baseLegal": "Decreto nº 31.139/2021 (Regulamento Geral do CBMRN)",
      "artigosDeOrigem": ["Art. 32 §12º (missão e composição)"],
      "atribuicoes": [
        "O Subgrupamento Independente de Bombeiros Militar de Atendimento Pré-hospitalar (S.I.B.M-APH) é a unidade operacional do Corpo de Bombeiros Militar do Estado responsável pelo serviço de atendimento pré-hospitalar de urgência, compreendendo as ações de manutenção do suporte básico e avançado de vida, prestadas nos acidentes em via pública e rodovias, capaz de reduzir os casos de mortalidade por afecções causadas pelo trauma, na capital e região metropolitana do Estado (Art. 32 §12º)."
      ],
      "desdobramentos": [],
      "cargos": [{
        "cargo": "Comandante do SIBM-APH",
        "subordinadoA": "Comandante Operacional BM",
        "requisito": "Oficial do QOCBM",
        "desdobramentos": [],
        "atribuicoes": ["Comandar o subgrupamento responsável pelo APH de urgência na capital e região metropolitana (Art. 32 §12º)"]
      }]
    },
    "dlof-rn": {
      "name": "Diretoria de Logística, Orçamento e Finanças", "abbreviation": "DLOF", "category": "Execução",
      "subordinadoA": "Conselho Superior (membro)", "legalRef": "Art. 34",
      "baseLegal": "Decreto nº 31.139/2021 (Regulamento Geral do CBMRN)",
      "artigosDeOrigem": ["Art. 34 (caput e §§1º-2º)"],
      "atribuicoes": [
        "A Diretoria de Logística, Orçamento e Finanças é responsável pela gestão das finanças da corporação, bem como pela gestão de logística da corporação, de modo a supervisionar, coordenar, controlar, fiscalizar e executar as atividades financeiras, contábeis e orçamentárias e a aquisição, o suprimento, o armazenamento e a manutenção dos equipamentos, viaturas, bens móveis e imóveis, obras, instalações, transportes de materiais e pessoas, sendo ainda responsável por planejar, coordenar, executar e avaliar projetos e atividades relacionadas a investimentos, desenvolvimento, manutenção, inovação e segurança em tecnologia da informação, além de outras atividades correlatas (Art. 34)."
      ],
      "desdobramentos": ["Secretaria Executiva", "Comissão Permanente de Licitação (CPL)", "Centro de Logística (CLOG)", "Centro de Tecnologia da Informação e Comunicações (CTIC)", "Centro de Administração Financeira e Orçamentária (CAFO)"],
      "cargos": [{
        "cargo": "Diretor de Logística, Orçamento e Finanças",
        "subordinadoA": "Comandante-Geral",
        "requisito": "Coronel ou Tenente-Coronel do QOCBM (Art. 45)",
        "desdobramentos": [],
        "atribuicoes": ["Gestão das finanças e logística da Corporação; supervisão, coordenação, controle e fiscalização das atividades financeiras, contábeis, orçamentárias, aquisição, suprimento e tecnologia da informação (Art. 34)"]
      }]
    },
    "cafo-rn": {
      "name": "Centro de Administração Financeira e Orçamentária", "abbreviation": "CAFO", "category": "Execução",
      "subordinadoA": "Diretoria de Logística, Orçamento e Finanças", "legalRef": "Art. 39",
      "baseLegal": "Decreto nº 31.139/2021 (Regulamento Geral do CBMRN)",
      "artigosDeOrigem": ["Art. 39 (competências, I-XVI)"],
      "atribuicoes": [
        "O Centro de Administração Financeira e Orçamentária é o órgão responsável pelas atividades específicas da gestão orçamentário-financeira, pela supervisão destas atividades junto aos demais órgãos da Corporação e pelo repasse de recursos orçamentários, de acordo com o planejamento estabelecido, competindo-lhe: (Art. 39, caput)",
        "I - elaborar programa de planejamento, controle e fiscalização das atividades relacionadas com a política de pessoal, de admissão, de capacitação técnica, de remuneração do pessoal e de prevenção de acidentes do trabalho;",
        "II - alocar recursos orçamentários e financeiros para os diferentes setores de atividade do CBMRN;",
        "III - controlar os custos com pessoal e manter atualizado o cadastro central de recursos humanos;",
        "IV - realizar atividades específicas da gestão financeira, supervisão destas junto aos demais órgãos da corporação e o repasse de recursos orçamentários, de acordo com o planejamento estabelecido;",
        "VI - elaborar o planejamento orçamentário do CBMRN, da programação financeira, da captação de recursos financeiros e a confecção de convênios com órgãos e entidades públicas e privadas;",
        "VII - acompanhar, controlar e fiscalizar a execução orçamentária-financeira do CBMRN;",
        "VIII - apropriar, analisar e controlar custos;",
        "IX - empenhar, liquidar e pagar as despesas da respectiva unidade orçamentária;",
        "X - promover o registro de atos orçamentários e financeiros, consignações e depósitos;",
        "XI - manter atualizadas as informações sobre a posição dos saldos orçamentários e financeiros;",
        "XII - elaborar balancetes e prestações de contas a serem encaminhados aos órgãos internos e externos;",
        "XIII - manter registrados e arquivados contratos e obrigações de responsabilidade do CBMRN;",
        "XIV - assessorar na elaboração da proposta de Lei Orçamentária Anual (LOA), na Lei de Diretrizes Orçamentárias (LDO) e acompanhar a execução do Plano Plurianual (PPA);",
        "XV - realizar auditorias em todas as repartições do CBMRN nas passagens de comando ou por solicitação do Comandante Geral da Corporação;",
        "XVI - desempenhar outras atividades correlatas."
      ],
      "desdobramentos": ["Tesouraria Geral", "Seção de Processos, Contabilidade e Auditoria"],
      "cargos": [{
        "cargo": "Chefe do CAFO",
        "subordinadoA": "Diretor da DLOF",
        "requisito": "Oficial BM designado pelo Comandante Geral",
        "desdobramentos": [],
        "atribuicoes": [
          "II - alocar recursos orçamentários e financeiros para os diferentes setores de atividade do CBMRN;",
          "VII - acompanhar, controlar e fiscalizar a execução orçamentária-financeira do CBMRN;",
          "IX - empenhar, liquidar e pagar as despesas da respectiva unidade orçamentária;"
        ]
      }]
    },
    "dgpei-rn": {
      "name": "Diretoria de Gestão de Pessoas, Ensino e Instrução", "abbreviation": "DGPEI", "category": "Execução",
      "subordinadoA": "Conselho Superior (membro)", "legalRef": "Art. 40",
      "baseLegal": "Decreto nº 31.139/2021 (Regulamento Geral do CBMRN)",
      "artigosDeOrigem": ["Art. 40 (competências, I-VI)"],
      "atribuicoes": [
        "A Diretoria de Gestão de Pessoas, Ensino e Instrução é responsável pelo gerenciamento de pessoas da Corporação, incumbindo-se: (Art. 40, caput)",
        "I - da supervisão, coordenação, controle, fiscalização e execução das atividades relacionadas com o ingresso, identificação, classificação, movimentação, cadastros, avaliações, promoções, direitos e deveres;",
        "II - do acompanhamento e controle de inativos e pensionistas;",
        "III - das orientações e acompanhamento quanto à saúde do efetivo;",
        "IV - pela gestão do ensino e instrução da corporação;",
        "V - pela política de ensino, atuando na supervisão, na coordenação, na fiscalização, no controle e na execução das atividades de ensino, instrução e pesquisa relacionadas com a formação, o aperfeiçoamento e a especialização de oficiais e praças;",
        "VI - desempenhar outras atividades correlatas."
      ],
      "desdobramentos": ["Centro de Recursos Humanos (CRH)", "Centro Superior de Formação e Aperfeiçoamento (CSFA)", "Serviço de Saúde"],
      "cargos": [{
        "cargo": "Diretor de Gestão de Pessoas, Ensino e Instrução",
        "subordinadoA": "Comandante-Geral",
        "requisito": "Coronel ou Tenente-Coronel do QOCBM (Art. 45)",
        "desdobramentos": [],
        "atribuicoes": [
          "I - supervisão, coordenação, controle, fiscalização e execução das atividades relacionadas com o ingresso, identificação, classificação, movimentação, cadastros, avaliações, promoções, direitos e deveres;",
          "IV - gestão do ensino e instrução da corporação;",
          "V - política de ensino, atuando na supervisão, coordenação, fiscalização, controle e execução das atividades de ensino, instrução e pesquisa de formação, aperfeiçoamento e especialização de oficiais e praças;"
        ]
      }]
    },
    "crh-rn": {
      "name": "Centro de Recursos Humanos", "abbreviation": "CRH", "category": "Execução",
      "subordinadoA": "Diretoria de Gestão de Pessoas, Ensino e Instrução", "legalRef": "Art. 41",
      "baseLegal": "Decreto nº 31.139/2021 (Regulamento Geral do CBMRN)",
      "artigosDeOrigem": ["Art. 41 (competências, I-VIII)"],
      "atribuicoes": [
        "O Centro de Recursos Humanos é o órgão responsável pelo planejamento, controle e fiscalização das atividades relacionadas com a política de pessoal, competindo-lhe: (Art. 41, caput)",
        "I - manter atualizados os registros relativos aos direitos e deveres dos militares do CBMRN;",
        "II - manter atualizadas as anotações devidas na ficha funcional dos militares do CBMRN;",
        "III - planejar, coordenar e controlar todos os assuntos relacionados com o pessoal pensionistas e inativos;",
        "IV - assessorar às Comissões de Promoção;",
        "V - assessorar todo o recrutamento e seleção para ingresso ao CBMRN;",
        "VI - coordenar e controlar todos os assuntos relacionados com a identificação do pessoal da corporação;",
        "VII - coordenar e controlar o arquivo de toda documentação inerente ao efetivo ativo, inativo e de pensionistas do CBMRN;",
        "VIII - desempenhar outras atividades correlatas."
      ],
      "desdobramentos": ["Seção de Identificação e Processo de Pessoal", "Seção de Pensionistas e Inativos", "Seção de Arquivo Geral"],
      "cargos": [{
        "cargo": "Chefe do CRH",
        "subordinadoA": "Diretor da DGPEI",
        "requisito": "Oficial BM designado pelo Comandante Geral",
        "desdobramentos": [],
        "atribuicoes": [
          "I - manter atualizados os registros relativos aos direitos e deveres dos militares do CBMRN;",
          "III - planejar, coordenar e controlar todos os assuntos relacionados com o pessoal pensionistas e inativos;",
          "V - assessorar todo o recrutamento e seleção para ingresso ao CBMRN;"
        ]
      }]
    },
    "csfa-rn": {
      "name": "Centro Superior de Formação e Aperfeiçoamento", "abbreviation": "CSFA", "category": "Execução",
      "subordinadoA": "Diretoria de Gestão de Pessoas, Ensino e Instrução", "legalRef": "Art. 42",
      "baseLegal": "Decreto nº 31.139/2021 (Regulamento Geral do CBMRN)",
      "artigosDeOrigem": ["Art. 42 (competências, I-V)"],
      "atribuicoes": [
        "O Centro Superior de Formação e Aperfeiçoamento é o órgão responsável pelas atividades de formação, especialização e aperfeiçoamento de Oficiais e Praças da Corporação, competindo-lhe: (Art. 42, caput)",
        "I - realizar estudos para o planejamento do ensino do CBMRN;",
        "II - realizar ações de planejamento no desenvolvimento das atividades físicas e de desportos no âmbito da corporação;",
        "III - realizar ações inerentes à formação, especialização e aperfeiçoamento do pessoal do CBMRN;",
        "IV - planejar e promover eventos de artes e culturas do CBMRN;",
        "V - desempenhar outras atividades correlatas."
      ],
      "desdobramentos": ["Comissão de Estudos Superiores", "Corpo de Alunos", "Divisão de Ensino", "Divisão Administrativa"],
      "cargos": [{
        "cargo": "Chefe do CSFA",
        "subordinadoA": "Diretor da DGPEI",
        "requisito": "Oficial BM designado pelo Comandante Geral; pode ser o próprio Subdiretor da DGPEI (Art. 40 §2º)",
        "desdobramentos": [],
        "atribuicoes": [
          "I - realizar estudos para o planejamento do ensino do CBMRN;",
          "III - realizar ações inerentes à formação, especialização e aperfeiçoamento do pessoal do CBMRN;"
        ]
      }]
    },
    "dat-rn": {
      "name": "Diretoria de Atividades Técnicas", "abbreviation": "DAT", "category": "Execução",
      "subordinadoA": "Conselho Superior (membro)", "legalRef": "Art. 44",
      "baseLegal": "Decreto nº 31.139/2021 (Regulamento Geral do CBMRN); LC nº 601/2017",
      "artigosDeOrigem": ["Art. 44 (caput e §§3º-9º)"],
      "atribuicoes": [
        "A Diretoria de Atividades Técnicas (DAT) é o órgão da Corporação que tem por finalidade desenvolver as atividades relacionadas à prevenção contra incêndio e controle de pânico nas edificações e áreas de risco em todo Estado, conforme previsto na Lei Complementar Estadual nº 601, de 07 de agosto de 2017, e demais normas e instruções técnicas (Art. 44)."
      ],
      "desdobramentos": ["Centro de Análise de Risco de Incêndio e Pânico (CARIP)", "Centro de Apoio Técnico Administrativo (CATA)", "Seção de Tecnologia da Informação", "Centro de Vistorias", "Centro de Fiscalização", "1º Centro de Atividades Técnicas — Mossoró", "2º Centro de Atividades Técnicas — Caicó"],
      "cargos": [{
        "cargo": "Diretor de Atividades Técnicas",
        "subordinadoA": "Comandante-Geral",
        "requisito": "Coronel ou Tenente-Coronel do QOCBM (Art. 45)",
        "desdobramentos": [],
        "atribuicoes": ["Desenvolvimento das atividades de prevenção contra incêndio e controle de pânico nas edificações e áreas de risco em todo o Estado, conforme LC 601/2017 e normas técnicas (Art. 44)"]
      }]
    },
    "carip-rn": {
      "name": "Centro de Análise de Risco de Incêndio e Pânico", "abbreviation": "CARIP", "category": "Execução",
      "subordinadoA": "Diretoria de Atividades Técnicas", "legalRef": "Art. 44 §3º",
      "baseLegal": "Decreto nº 31.139/2021 (Regulamento Geral do CBMRN)",
      "artigosDeOrigem": ["Art. 44 §3º (competência)"],
      "atribuicoes": [
        "O Centro de Análise de Risco de Incêndio e Pânico tem por competência a análise técnica dos projetos de prevenção contra incêndio e pânico das edificações e áreas de risco, verificando o cumprimento das normas de segurança previstas no Código Estadual de Segurança Contra Incêndio e Pânico do Rio Grande do Norte (CESIP), bem como a realização de pesquisas sobre a atualização tecnológica dos materiais, dos equipamentos e das normas nacionais e estrangeiras relacionadas à proteção contra incêndio (Art. 44 §3º)."
      ],
      "desdobramentos": [],
      "cargos": [{
        "cargo": "Chefe do CARIP",
        "subordinadoA": "Diretor da DAT",
        "requisito": "Oficial BM com conhecimento técnico em prevenção de incêndios",
        "desdobramentos": [],
        "atribuicoes": ["Análise técnica dos projetos de prevenção contra incêndio e pânico; verificação do cumprimento das normas do CESIP; pesquisas sobre atualização tecnológica de materiais e normas (Art. 44 §3º)"]
      }]
    },
    "cf-rn": {
      "name": "Centro de Fiscalização", "abbreviation": "CF", "category": "Execução",
      "subordinadoA": "Diretoria de Atividades Técnicas", "legalRef": "Art. 44 §7º",
      "baseLegal": "Decreto nº 31.139/2021 (Regulamento Geral do CBMRN)",
      "artigosDeOrigem": ["Art. 44 §7º (competência)"],
      "atribuicoes": [
        "O Centro de Fiscalização tem por competência fiscalizar toda e qualquer edificação e área de risco existente no Estado e, quando necessário, expedir notificações e auto de infração, aplicar multas, proceder embargos e interdições e apreensão de bens e produtos, com o intuito de sanar as irregularidades verificadas (Art. 44 §7º)."
      ],
      "desdobramentos": [],
      "cargos": [{
        "cargo": "Chefe do Centro de Fiscalização",
        "subordinadoA": "Diretor da DAT",
        "requisito": "Oficial BM com competência de fiscalização e poder de polícia administrativa",
        "desdobramentos": [],
        "atribuicoes": ["Fiscalização de edificações e áreas de risco; expedição de notificações, autos de infração, multas, embargos e interdições (Art. 44 §7º)"]
      }]
    },
    "cat1-rn": {
      "name": "1º Centro de Atividades Técnicas — Mossoró", "abbreviation": "1º CAT", "category": "Execução",
      "subordinadoA": "Diretoria de Atividades Técnicas", "legalRef": "Art. 44 §8º",
      "baseLegal": "Decreto nº 31.139/2021 (Regulamento Geral do CBMRN)",
      "artigosDeOrigem": ["Art. 44 §8º (competência)"],
      "atribuicoes": [
        "O Primeiro Centro de Atividades Técnicas (1º CAT) é a unidade da Diretoria de Atividades Técnicas, sediada em Mossoró/RN, responsável pelas atividades relacionadas à prevenção contra incêndio e controle de pânico nas edificações e áreas de risco nos municípios localizados no interior do Estado do Rio Grande do Norte (Art. 44 §8º)."
      ],
      "desdobramentos": ["Seção de Atividades Técnicas — Pau dos Ferros/RN (Art. 44 §10)"],
      "cargos": [{
        "cargo": "Chefe do 1º CAT",
        "subordinadoA": "Diretor da DAT",
        "requisito": "Oficial BM designado pelo Comandante Geral",
        "desdobramentos": [],
        "atribuicoes": ["Prevenção contra incêndio e controle de pânico nas edificações e áreas de risco nos municípios do interior do Estado do RN (sede em Mossoró) (Art. 44 §8º)"]
      }]
    },
    "cat2-rn": {
      "name": "2º Centro de Atividades Técnicas — Caicó", "abbreviation": "2º CAT", "category": "Execução",
      "subordinadoA": "Diretoria de Atividades Técnicas", "legalRef": "Art. 44 §9º",
      "baseLegal": "Decreto nº 31.139/2021 (Regulamento Geral do CBMRN)",
      "artigosDeOrigem": ["Art. 44 §9º (competência)"],
      "atribuicoes": [
        "O Segundo Centro de Atividades Técnicas (2º CAT) é a unidade da Diretoria de Atividades Técnicas, sediada em Caicó/RN, responsável pelas atividades relacionadas à prevenção contra incêndio e controle de pânico nas edificações e áreas de risco nos municípios localizados no interior do Estado do Rio Grande do Norte (Art. 44 §9º)."
      ],
      "desdobramentos": [],
      "cargos": [{
        "cargo": "Chefe do 2º CAT",
        "subordinadoA": "Diretor da DAT",
        "requisito": "Oficial BM designado pelo Comandante Geral",
        "desdobramentos": [],
        "atribuicoes": ["Prevenção contra incêndio e controle de pânico nas edificações e áreas de risco nos municípios do interior do Estado do RN (sede em Caicó) (Art. 44 §9º)"]
      }]
    }
  }
},

"rs": {
  "legal_source": "Lei Complementar nº 14.920/2016; Decreto nº 53.897/2018; Regimento Interno (Portaria CBMRS nº 001/2025)",
  "organs": {
    "comando-geral": {
      "name": "Comando-Geral", "abbreviation": "Cmt-G", "category": "Direção Estratégica",
      "subordinadoA": "Secretaria da Segurança Pública", "legalRef": "Art. 4º Dec. 53.897/2018; Art. 3º do RI",
      "baseLegal": "Lei Complementar nº 14.920/2016; Decreto nº 53.897/2018",
      "artigosDeOrigem": ["Art. 4º (Comando-Geral)"],
      "atribuicoes": ["Coordenação geral das atividades da Instituição", "Presidência da Comissão de Avaliação e Mérito", "Direção do Conselho Superior", "Competência institucional do Corpo de Bombeiros Militar (Regimento Interno, Art. 1º): I - exercer as atividades de polícia judiciária militar no âmbito de sua competência", "II - realizar a segurança, a prevenção, a proteção e o combate a incêndios", "III - realizar os serviços de busca, salvamento e resgates aéreo, aquático e terrestre no Estado", "IV - planejar e implementar as ações de proteção e defesa civil no Estado", "V - planejar, estudar, analisar, vistoriar, controlar, fiscalizar, aprovar, notificar e interditar atividades, equipamentos, projetos e planos de proteção e prevenção contra incêndios, pânicos, desastres e catástrofes em todas as edificações, instalações, veículos, embarcações e outras atividades que ponham em risco a vida, o meio ambiente e o patrimônio, aplicando a legislação específica, respeitada a competência de outros órgãos", "VI - realizar a investigação de incêndios e de sinistros, respeitadas as competências de outros órgãos", "VII - elaborar, emitir e homologar instruções, resoluções, relatórios, pareceres e normas técnicas para disciplinar a segurança, a proteção e a prevenção contra incêndios e sinistros e a proteção e defesa civil", "VIII - realizar o suporte básico de vida, respeitadas as competências de outros órgãos", "IX - credenciar e fiscalizar as escolas, as empresas e os cursos de formação de bombeiros civis e aplicar as penalidades previstas em lei", "X - desempenhar outras atribuições previstas em lei e exercer o poder de polícia administrativa no âmbito de suas atribuições"],
      "desdobramentos": ["Subcomandante-Geral", "Conselho Superior", "Corregedoria-Geral", "Gabinete do Comando-Geral", "Comissão de Avaliação e Mérito", "Departamento Administrativo", "Departamento de Segurança, Prevenção e Proteção Contra Incêndios", "Academia de Bombeiro Militar", "Assessoria de Operações, Defesa Civil e Serviços Civis Auxiliares", "Comandos Regionais (1º ao 4º CRBM)", "Batalhão Especial de Segurança Contra Incêndio"],
      "cargos": [
        {"cargo": "Comandante-Geral", "subordinadoA": "Secretaria da Segurança Pública", "requisito": "Oficial da ativa do último posto da carreira do Quadro de Oficiais de Estado-Maior (QOEM), autoridade primeira da Instituição (Regimento Interno, Art. 27)", "desdobramentos": [], "atribuicoes": ["Compete-lhe a administração da Instituição, com os poderes, inclusive hierárquicos sobre os demais Oficiais do mesmo posto, e deveres inerentes ao cargo e à função (Regimento Interno, Art. 27)", "I - a coordenação geral das atividades da Instituição; II - a presidência da Comissão de Avaliação e Mérito; III - a direção do Conselho Superior (Art. 27)"]},
        {"cargo": "Subcomandante-Geral", "subordinadoA": "Comandante-Geral", "requisito": "Oficial da ativa do último posto da carreira do Quadro de Oficiais de Estado-Maior (QOEM); indicado pelo Comandante-Geral e nomeado pelo Governador do Estado; possui precedência hierárquica sobre os demais Oficiais do mesmo posto (Art. 28)", "desdobramentos": [], "atribuicoes": ["Substituto do Comandante-Geral nas suas ausências e impedimentos eventuais; competem-lhe as funções de assessoramento ao Comandante-Geral no cumprimento das competências atribuídas ao CBMRS, além de outras que lhe forem delegadas (Regimento Interno, Art. 28)"]}
      ]
    },
    "corregedoria-geral": {
      "name": "Corregedoria-Geral", "abbreviation": "Corr-G", "category": "Disciplina e Fiscalização",
      "subordinadoA": "Comandante-Geral", "legalRef": "Art. 9º Dec. 53.897/2018; Art. 7º RI",
      "baseLegal": "Lei Complementar nº 14.920/2016; Decreto nº 53.897/2018",
      "artigosDeOrigem": ["Art. 9º (Corregedoria-Geral)"],
      "atribuicoes": ["Órgão de disciplina, orientação e fiscalização das atividades funcionais e da conduta dos Bombeiros Militares e dos Servidores Civis da Instituição, diretamente subordinada ao Comandante-Geral (Regimento Interno, Art. 30)"],
      "desdobramentos": ["Divisão Administrativa (DAdm/Corr-G)", "Divisão de Justiça e Disciplina (DJD/Corr-G)", "Divisão de Controle Interno Correcional (DCIC/Corr-G)", "Divisão de Feitos Especiais (DFE/Corr-G)", "Ouvidoria (Ouv/Corr-G)", "Cartório (Cart/Corr-G)"],
      "cargos": [{"cargo": "Corregedor-Geral", "subordinadoA": "Comandante-Geral", "requisito": "Oficial da ativa do último posto da carreira do Quadro de Oficiais de Estado-Maior (QOEM)", "desdobramentos": [], "atribuicoes": ["Responsabilidade pela disciplina e pela hierarquia institucional, bem como assessoramento direto ao Comando-Geral (Regimento Interno, Art. 46)"]}]
    },
    "gabinete-cmt-g": {
      "name": "Gabinete do Comandante-Geral", "abbreviation": "GCG", "category": "Assessoramento",
      "subordinadoA": "Comandante-Geral", "legalRef": "Art. 6º Dec. 53.897/2018; Art. 8º RI",
      "baseLegal": "Lei Complementar nº 14.920/2016; Decreto nº 53.897/2018",
      "artigosDeOrigem": ["Art. 6º (Gabinete)"],
      "atribuicoes": ["Órgão de assistência, de assessoramento, suporte administrativo, de transmissão e fiscalização das ordens do Comandante-Geral (Cmt-G) e do Subcomandante-Geral (SCmt-G) (Regimento Interno, Art. 31)"],
      "desdobramentos": ["Secretaria-Executiva do Comandante-Geral (SecExec/GCG)", "Assessoria de Controle Interno (CI/GCG)", "Assessoria Jurídica, Convênios e Contratos (AJCC/GCG)", "Assessoria de Comunicação Social (ACS/GCG)", "Agência Central de Inteligência (ACI/GCG)", "Assessoria de Planejamento Estratégico e Relações Institucionais (APERI/GCG)"],
      "cargos": [{"cargo": "Chefe de Gabinete do Comandante-Geral", "subordinadoA": "Comandante-Geral", "requisito": "Oficial, com assessoramento direto do Secretário-Executivo e das suas Seções", "desdobramentos": [], "atribuicoes": ["Chefiar, orientar e supervisionar os trabalhos do Gabinete do Comandante-Geral; prestar assessoramento direto ao Comando-Geral; coordenar as atividades administrativas (Regimento Interno, Art. 47)"]}]
    },
    "departamento-administrativo": {
      "name": "Departamento Administrativo", "abbreviation": "DA", "category": "Apoio Tático",
      "subordinadoA": "Comando-Geral", "legalRef": "Art. 12º Dec. 53.897/2018; Art. 10º RI",
      "baseLegal": "Lei Complementar nº 14.920/2016; Decreto nº 53.897/2018",
      "artigosDeOrigem": ["Art. 12º (Departamento Administrativo)"],
      "atribuicoes": ["Órgão de planejamento, controle, fiscalização, auditoria e execução das atividades relacionadas ao fluxo de registros, movimentações e processos de recursos humanos, orçamento e finanças, logística, patrimônio e tecnologia da informação e comunicações (Regimento Interno, Art. 34)"],
      "desdobramentos": ["Divisão Administrativa (DAdm)", "Divisão de Logística e Patrimônio (DLP)", "Divisão de Orçamento e Finanças (DOF)", "Divisão de Recursos Humanos (DRH)", "Divisão de Tecnologia da Informação e Comunicações (DTIC)"],
      "cargos": [{"cargo": "Diretor do Departamento Administrativo", "subordinadoA": "Comando-Geral", "requisito": "Oficial da ativa do último posto da carreira do Quadro de Oficiais de Estado-Maior (QOEM)", "desdobramentos": [], "atribuicoes": ["Coordenar, em Nível Departamental de Apoio, a gestão das atividades administrativas da Corporação (Regimento Interno, Art. 49)"]}]
    },
    "dspci": {
      "name": "Departamento de Segurança, Prevenção e Proteção Contra Incêndios", "abbreviation": "DSPCI", "category": "Apoio Tático",
      "subordinadoA": "Comando-Geral", "legalRef": "Art. 13º Dec. 53.897/2018; Art. 11º RI",
      "baseLegal": "Lei Complementar nº 14.920/2016; Decreto nº 53.897/2018",
      "artigosDeOrigem": ["Art. 13º (DSPCI)"],
      "atribuicoes": ["Órgão de planejamento, controle e fiscalização das atividades relacionadas à segurança contra incêndio e à pesquisa e investigação de sinistros em âmbito estadual (Regimento Interno, Art. 35)"],
      "desdobramentos": ["Divisão Administrativa (DAdm)", "Divisão de Gestão e Normatização (DGN)", "Divisão de Pesquisa e Investigação de Sinistros (DPIS)"],
      "cargos": [{"cargo": "Diretor do Departamento de Segurança, Prevenção e Proteção Contra Incêndios", "subordinadoA": "Comando-Geral", "requisito": "Oficial da ativa do último posto da carreira do Quadro de Oficiais de Estado-Maior (QOEM)", "desdobramentos": [], "atribuicoes": ["Definir as estratégias para a segurança, prevenção e proteção contra incêndios (Regimento Interno, Art. 50)"]}]
    },
    "abm": {
      "name": "Academia de Bombeiro Militar", "abbreviation": "ABM", "category": "Apoio Tático",
      "subordinadoA": "Comando-Geral", "legalRef": "Art. 14º Dec. 53.897/2018; Art. 12º RI",
      "baseLegal": "Lei Complementar nº 14.920/2016; Decreto nº 53.897/2018",
      "artigosDeOrigem": ["Art. 14º (Academia de Bombeiro Militar)"],
      "atribuicoes": ["Nível Departamental de Ensino do CBMRS, responsável pelo planejamento, controle e fiscalização das atividades relacionadas ao ensino, à saúde física do efetivo e à pesquisa científica da Instituição, bem como pela capacitação continuada dos servidores militares e dos profissionais civis que exerçam atividade auxiliar de bombeiro em âmbito estadual (Regimento Interno, Art. 36)"],
      "desdobramentos": ["Divisão Administrativa (DAdm/ABM)", "Divisão de Ensino (DEns/ABM)", "Órgão de Pesquisa, Ensino, Treinamento e Avaliação (OPETA)", "Escola de Educação Física (EsEF)", "Escola Superior de Segurança Contra Incêndio e Desastres (ESSCID)", "Escola de Bombeiro Militar (EsBo)", "Escola de Serviços Civis Auxiliares de Bombeiro (ESCAB)"],
      "cargos": [{"cargo": "Comandante da Academia de Bombeiro Militar", "subordinadoA": "Comando-Geral", "requisito": "Oficial, com assessoramento direto do Secretário-Executivo e das suas divisões", "desdobramentos": [], "atribuicoes": ["Comandar, chefiar, supervisionar, planejar, dirigir, orientar, coordenar e acompanhar as atividades da Academia de Bombeiro Militar (Regimento Interno, Art. 51)"]}]
    },
    "aodc": {
      "name": "Assessoria de Operações, Defesa Civil e Serviços Civis Auxiliares de Bombeiro", "abbreviation": "AODC", "category": "Apoio Tático",
      "subordinadoA": "Comando-Geral", "legalRef": "Dec. 53.897/2018; Art. 13º RI",
      "baseLegal": "Lei Complementar nº 14.920/2016; Decreto nº 53.897/2018",
      "artigosDeOrigem": ["Art. 3º, VII (AODC)"],
      "atribuicoes": ["Órgão de planejamento, direção, controle e execução das atividades relacionadas a operações, defesa civil e serviços civis e auxiliares de bombeiro (Regimento Interno, Art. 37)"],
      "desdobramentos": ["Divisão Administrativa (DAdm/AODC)", "Divisão de Operações e Defesa Civil (DODC/AODC)", "Divisão de Serviços Civis Auxiliares (DSCAB/AODC)", "Divisão de Monitoramento Operacional (DMO/AODC)", "Divisão de Operações Aéreas (DOA/AODC)"],
      "cargos": [{"cargo": "Diretor da Assessoria de Operações e Defesa Civil", "subordinadoA": "Comando-Geral", "requisito": "Oficial, com assessoramento direto do Secretário-Executivo e das suas divisões", "desdobramentos": [], "atribuicoes": ["Coordenar a gestão das atividades operacionais da Corporação; realizar a interlocução para a participação do Corpo de Bombeiros Militar em ações de defesa civil (Regimento Interno, Art. 52)"]}]
    },
    "1crbm": {
      "name": "1º Comando Regional de Bombeiro Militar", "abbreviation": "1ºCRBM", "category": "Execução",
      "subordinadoA": "Comando-Geral", "legalRef": "Art. 15º Dec. 53.897/2018; Art. 14º RI",
      "baseLegal": "Lei Complementar nº 14.920/2016; Decreto nº 53.897/2018",
      "artigosDeOrigem": ["Art. 3º, VIII (Comando Regional Metropolitano)"],
      "atribuicoes": ["Escalão intermediário de comando, responsável, em sua circunscrição territorial, pelas atividades administrativo-operacionais internas e dos Órgãos do CBM (OCBM) que lhe são subordinados (Regimento Interno, Art. 38)"],
      "desdobramentos": ["1º Batalhão BM (Porto Alegre)", "8º Batalhão BM (Canoas)", "9º Batalhão BM (Tramandaí)", "Batalhão de Busca e Salvamento (BBS) — Porto Alegre"],
      "cargos": [{"cargo": "Comandante do 1º CRBM", "subordinadoA": "Comando-Geral", "requisito": "Oficial da ativa do último ou penúltimo posto da carreira do Quadro de Oficiais de Estado-Maior (QOEM)", "desdobramentos": [], "atribuicoes": ["Comandar, chefiar, supervisionar, planejar, dirigir, orientar, coordenar e acompanhar as atividades da respectiva unidade organizacional (Regimento Interno, Art. 54)"]}]
    },
    "crbm-rs": {
      "name": "Comandos Regionais (2º, 3º e 4º CRBM)", "abbreviation": "CRBM", "category": "Execução",
      "subordinadoA": "Comando-Geral", "legalRef": "Dec. 53.897/2018",
      "baseLegal": "Lei Complementar nº 14.920/2016; Decreto nº 53.897/2018",
      "artigosDeOrigem": ["Dec. 53.897/2018"],
      "atribuicoes": ["Escalões intermediários de comando, responsáveis, em suas respectivas circunscrições territoriais, pelas atividades administrativo-operacionais internas e dos Órgãos do CBM (OCBM) que lhes são subordinados (Regimento Interno, Art. 38)"],
      "desdobramentos": ["2º CRBM (Caxias do Sul): 2º, 5º, 7º BBM", "3º CRBM (Pelotas): 3º, 10º, 13º BBM", "4º CRBM (Santa Maria): 4º, 6º, 11º, 12º BBM"],
      "cargos": [{"cargo": "Comandante Regional", "subordinadoA": "Comando-Geral", "requisito": "Oficial da ativa do último ou penúltimo posto da carreira do Quadro de Oficiais de Estado-Maior (QOEM)", "desdobramentos": [], "atribuicoes": ["Comandar, chefiar, supervisionar, planejar, dirigir, orientar, coordenar e acompanhar as atividades da respectiva unidade organizacional (Regimento Interno, Art. 54)"]}]
    },
    "besci": {
      "name": "Batalhão Especial de Segurança Contra Incêndio", "abbreviation": "BESCI", "category": "Execução Especial",
      "subordinadoA": "DSPCI (operacionalmente) e Comandante-Geral (administrativamente)", "legalRef": "Art. 16º RI",
      "baseLegal": "Lei Complementar nº 14.920/2016; Decreto nº 53.897/2018",
      "artigosDeOrigem": ["Art. 3º, VIII e Art. 5º"],
      "atribuicoes": ["Órgão de Nível Departamental de Apoio e Execução, com abrangência estadual na sua área temática, subordinado operacionalmente ao Departamento de Segurança, Prevenção e Proteção Contra Incêndios (DSPCI) e, enquanto órgão de Apoio, subordinado ao Comandante-Geral, de autonomia administrativa (Regimento Interno, Art. 39)"],
      "desdobramentos": ["Divisão Administrativa e Correição (DAdmC/BESCI)", "Divisão de Análise de Planos (DAPPCI/BESCI)", "Divisão de Vistoria e Fiscalização de Edificações (DVFE/BESCI)"],
      "cargos": [{"cargo": "Comandante do BESCI", "subordinadoA": "DSPCI (operacionalmente) / Comandante-Geral (administrativamente)", "requisito": "Oficial Superior", "desdobramentos": [], "atribuicoes": ["Comandar, chefiar, supervisionar, planejar, dirigir, orientar, coordenar e acompanhar as atividades do Batalhão Especial de Segurança Contra Incêndio (Regimento Interno, Art. 55)"]}]
    }
  }
},

"rj": {
  "legal_source": "Lei nº 250, de 02 de julho de 1979",
  "organs": {
    "cg-rj": {
      "name": "Comando-Geral", "abbreviation": "CmtG", "category": "Direção Geral",
      "subordinadoA": "Secretaria de Estado de Segurança Pública", "legalRef": "Arts. 2, 4, 10",
      "baseLegal": "Lei nº 250, de 02 de julho de 1979",
      "artigosDeOrigem": ["Art. 2 (competências institucionais)", "Art. 4 (Comandante-Geral)", "Art. 10 (responsabilidade)"],
      "atribuicoes": [
        "Art. 2, I — realizar serviços de prevenção e extinção de incêndios;",
        "Art. 2, II — realizar serviços de busca e salvamento;",
        "Art. 2, III — realizar perícias de incêndio;",
        "Art. 2, IV — prestar socorros nos casos de inundações, desabamentos ou catástrofes, sempre que haja ameaça de destruição de haveres, vítima ou pessoa em iminente perigo de vida;",
        "Art. 2, V — estudar, analisar, planejar, exigir e fiscalizar todo o serviço de segurança contra incêndio do Estado;",
        "Art. 2, VI — em caso de mobilização do Exército, com ele cooperar no serviço de Defesa Civil.",
        "Art. 4 — A administração, o comando e o emprego da Corporação são da competência e responsabilidade do Comandante-Geral, assessorado e auxiliado pelos órgãos de direção.",
        "Art. 10 — O Comandante-Geral é responsável pelo Comando e pela Administração da Corporação."
      ],
      "desdobramentos": ["Estado-Maior-Geral (EMG)", "Diretorias", "Ajudância-Geral (AjG)", "Comissões e Secretarias", "Assessorias"],
      "cargos": [
        {"cargo": "Comandante-Geral", "subordinadoA": "Governador do Estado", "requisito": "Coronel ou Tenente-Coronel do serviço ativo do Exército, proposto ao Ministro do Exército pelo Governador (Art. 11)", "desdobramentos": [], "atribuicoes": []},
        {"cargo": "Oficial Ajudante-de-Ordens", "subordinadoA": "Comandante-Geral", "requisito": "Oficial BM (Art. 13)", "desdobramentos": [], "atribuicoes": []}
      ]
    },
    "emg-rj": {
      "name": "Estado-Maior-Geral", "abbreviation": "EMG", "category": "Direção Geral",
      "subordinadoA": "Comandante-Geral", "legalRef": "Arts. 14-18",
      "baseLegal": "Lei nº 250, de 02 de julho de 1979",
      "artigosDeOrigem": ["Art. 14 (EMG)", "Art. 16 (Chefe do EMG)"],
      "atribuicoes": [
        "Art. 14 — O Estado-Maior-Geral é o órgão de direção geral, responsável, perante o Comandante-Geral, pelo estudo, planejamento, coordenação, fiscalização e controle de todas as atividades da Corporação, inclusive dos órgãos de direção setorial. É, ainda, o órgão central do sistema de planejamento administrativo, programação e orçamento. Elabora as diretrizes e ordens do comando que acionam os órgãos de direção setorial e os de execução no cumprimento de suas missões.",
        "Art. 16, caput — O Chefe do Estado-Maior-Geral acumula as funções de Subcomandante da Corporação, sendo, pois, substituto eventual do Comandante-Geral nos impedimentos deste."
      ],
      "desdobramentos": ["Chefe do EMG (acumula função de Subcomandante)", "Subchefe do EMG", "1ª Seção (BM/1) — pessoal e legislação", "2ª Seção (BM/2) — assuntos civis", "3ª Seção (BM/3) — instrução, operações e ensino", "4ª Seção (BM/4) — logística", "5ª Seção (BM/5) — assuntos civis", "6ª Seção (BM/6) — planejamento administrativo e orçamentação", "7ª Seção (BM/7) — serviço técnico"],
      "cargos": [
        {"cargo": "Chefe do Estado-Maior-Geral (Subcomandante da Corporação)", "subordinadoA": "Comandante-Geral", "requisito": "Coronel BM, da escolha do Comandante-Geral e nomeado pelo Governador do Estado (Art. 17)", "desdobramentos": [], "atribuicoes": []},
        {"cargo": "Subchefe do Estado-Maior-Geral", "subordinadoA": "Chefe do EMG", "requisito": "Oficial Superior BM do mesmo posto ou imediatamente abaixo ao do Chefe do EMG, nomeado pelo Comandante-Geral (Art. 18)", "desdobramentos": [], "atribuicoes": []}
      ]
    },
    "ag-rj": {
      "name": "Ajudância-Geral", "abbreviation": "AjG", "category": "Apoio",
      "subordinadoA": "Comando-Geral", "legalRef": "Arts. 30-31",
      "baseLegal": "Lei nº 250, de 02 de julho de 1979",
      "artigosDeOrigem": ["Art. 30 (Ajudância-Geral)", "Art. 30 parágrafo único (atribuições)"],
      "atribuicoes": [
        "Art. 30, caput — A Ajudância-Geral tem a seu cargo as funções administrativas do Comando-Geral, considerada como uma Organização de Bombeiros-Militares (OBM), bem como algumas atividades de pessoal para a Corporação como um todo.",
        "Art. 30, pú — trabalhos de secretaria incluindo correspondência, correio, protocolo-geral, arquivo-geral, boletim diário e outros;",
        "Art. 30, pú — apoio de pessoal auxiliar (praças) a todos os órgãos do Comando-Geral;",
        "Art. 30, pú — segurança do Quartel do Comando-Geral;",
        "Art. 30, pú — supervisão e emprego da Banda de Música e Banda Marcial;",
        "Art. 30, pú — serviços gerais do Quartel do Comando-Geral;",
        "Art. 30, pú — serviço de embarque da Corporação."
      ],
      "desdobramentos": ["Secretaria (AG/1)", "Seção Administrativa (AG/2)", "Seção de Embarque (AG/3)", "Grupamento de Comando (GC)"],
      "cargos": [
        {"cargo": "Ajudante-Geral", "subordinadoA": "Comandante-Geral", "requisito": "Oficial BM", "desdobramentos": [], "atribuicoes": []}
      ]
    },
    "dp-rj": {
      "name": "Diretoria de Pessoal", "abbreviation": "DP", "category": "Direção Setorial",
      "subordinadoA": "Comando-Geral", "legalRef": "Art. 20",
      "baseLegal": "Lei nº 250, de 02 de julho de 1979",
      "artigosDeOrigem": ["Art. 20 (Diretoria de Pessoal)"],
      "atribuicoes": [
        "Art. 20 — A Diretoria de Pessoal é o órgão de Direção Setorial do Sistema de Pessoal, incumbido do planejamento, execução, controle e fiscalização das atividades relacionadas com a classificação e movimentação de pessoal da ativa, cadastro e avaliação, direitos, deveres e incentivos, pessoal inativo e pensionistas, pessoal civil, seleção e ingresso e assistência social e religiosa."
      ],
      "desdobramentos": ["Seção de Cadastro, Avaliação e Movimentação (DP/1)", "Seção de Recrutamento (DP/2)", "Seção de Identificação (DP/3)", "Seção de Justiça e Disciplina (DP/4)", "Seção de Inativos e Pensionistas (DP/5)", "Seção de Expediente (DP/6)", "Capelania (Cpl)"],
      "cargos": [
        {"cargo": "Diretor de Pessoal", "subordinadoA": "Comando-Geral", "requisito": "Oficial Superior BM", "desdobramentos": [], "atribuicoes": []}
      ]
    },
    "de-rj": {
      "name": "Diretoria de Ensino", "abbreviation": "DE", "category": "Direção Setorial",
      "subordinadoA": "Comando-Geral", "legalRef": "Art. 22",
      "baseLegal": "Lei nº 250, de 02 de julho de 1979",
      "artigosDeOrigem": ["Art. 22 (Diretoria de Ensino)"],
      "atribuicoes": [
        "Art. 22 — A Diretoria de Ensino é o órgão de Direção Setorial do sistema de Ensino, incumbido de planejamento, coordenação, fiscalização e controle das atividades de formação, aperfeiçoamento e especialização de oficiais e praças BM do Corpo e, eventualmente, de civis ou oficiais e praças de outras Corporações."
      ],
      "desdobramentos": ["Seção Técnica de Ensino (DE/1)", "Seção de Formação (DE/2)", "Seção de Especialização e Aperfeiçoamento (DE/3)", "Seção de Administração (DE/4)"],
      "cargos": [
        {"cargo": "Diretor de Ensino", "subordinadoA": "Comando-Geral", "requisito": "Oficial Superior BM", "desdobramentos": [], "atribuicoes": []}
      ]
    },
    "df-rj": {
      "name": "Diretoria de Finanças", "abbreviation": "DF", "category": "Direção Setorial",
      "subordinadoA": "Comando-Geral", "legalRef": "Art. 24",
      "baseLegal": "Lei nº 250, de 02 de julho de 1979",
      "artigosDeOrigem": ["Art. 24 (Diretoria de Finanças)"],
      "atribuicoes": [
        "Art. 24 — A Diretoria de Finanças é o órgão de Direção Setorial do sistema Financeiro, incumbido de realizar as atividades específicas e assessorar o Comandante-Geral na supervisão das atividades financeiras dos órgãos da Corporação e na distribuição de recursos orçamentários, de acordo com o planejamento estabelecido."
      ],
      "desdobramentos": ["Seção de Administração Financeira (DF/1)", "Seção de Contabilidade (DF/2)", "Seção de Auditoria (DF/3)", "Seção de Expediente (DF/4)"],
      "cargos": [
        {"cargo": "Diretor de Finanças", "subordinadoA": "Comando-Geral", "requisito": "Oficial Superior BM", "desdobramentos": [], "atribuicoes": []}
      ]
    },
    "dal-rj": {
      "name": "Diretoria de Apoio Logístico", "abbreviation": "DAL", "category": "Direção Setorial",
      "subordinadoA": "Comando-Geral", "legalRef": "Art. 26",
      "baseLegal": "Lei nº 250, de 02 de julho de 1979",
      "artigosDeOrigem": ["Art. 26 (Diretoria de Apoio Logístico)"],
      "atribuicoes": [
        "Art. 26 — A Diretoria de Apoio Logístico é o órgão de Direção Setorial do Sistema Logístico, incumbido do planejamento, coordenação, fiscalização e controle das necessidades de apoio de saúde, de suprimento e de manutenção; realizará essas mesmas atividades no que se refere a obras."
      ],
      "desdobramentos": ["Seção de Suprimento (DAL/1)", "Seção de Manutenção (DAL/2)", "Seção de Saúde (DAL/3)", "Seção de Patrimônio (DAL/4)", "Seção de Expediente (DAL/5)"],
      "cargos": [
        {"cargo": "Diretor de Apoio Logístico", "subordinadoA": "Comando-Geral", "requisito": "Oficial Superior BM", "desdobramentos": [], "atribuicoes": []}
      ]
    },
    "dst-rj": {
      "name": "Diretoria de Serviços Técnicos", "abbreviation": "DST", "category": "Direção Setorial",
      "subordinadoA": "Comando-Geral", "legalRef": "Art. 28",
      "baseLegal": "Lei nº 250, de 02 de julho de 1979",
      "artigosDeOrigem": ["Art. 28 (Diretoria de Serviços Técnicos)"],
      "atribuicoes": [
        "Art. 28 — A Diretoria de Serviços Técnicos é o órgão de Direção Setorial do Sistema de Engenharia de Segurança, incumbido de estudar, analisar, planejar, exigir e fiscalizar as atividades atinentes à segurança contra incêndio e pânico, proceder a exame de plantas e a perícias; realizar testes de incombustibilidade; realizar vistorias e emitir pareceres, com autoridade para notificar, multar e interditar, na forma da legislação específica."
      ],
      "desdobramentos": ["Seção de Estudos e Projetos (DST/1)", "Seção de Perícias e Testes (DST/2)", "Seção de Vistorias e Pareceres (DST/3)", "Seção de Hidrantes (DST/4)", "Seção de Expediente (DST/5)", "Laboratório Químico (LQ)"],
      "cargos": [
        {"cargo": "Diretor de Serviços Técnicos", "subordinadoA": "Comando-Geral", "requisito": "Oficial Superior BM", "desdobramentos": [], "atribuicoes": []}
      ]
    },
    "css-rj": {
      "name": "Centro de Serviço Social", "abbreviation": "CSS", "category": "Apoio",
      "subordinadoA": "Diretoria de Pessoal", "legalRef": "Art. 37",
      "baseLegal": "Lei nº 250, de 02 de julho de 1979",
      "artigosDeOrigem": ["Art. 37 (Centro de Serviço Social)"],
      "atribuicoes": [
        "Art. 37, pú — O Centro de Serviço Social destina-se a prestar assistência social aos integrantes da Corporação, especialmente no que diz respeito a moradia, educação, empréstimos, transportes, recreações, justiça, pensões e seguros."
      ],
      "desdobramentos": [],
      "cargos": [
        {"cargo": "Chefe do Centro de Serviço Social", "subordinadoA": "Diretor de Pessoal", "requisito": "Oficial BM", "desdobramentos": [], "atribuicoes": []}
      ]
    },
    "csbm": {
      "name": "Curso Superior de Bombeiro-Militar", "abbreviation": "CSBM", "category": "Apoio",
      "subordinadoA": "Diretoria de Ensino", "legalRef": "Art. 39 § 1º",
      "baseLegal": "Lei nº 250, de 02 de julho de 1979",
      "artigosDeOrigem": ["Art. 39 § 1º (CSBM)"],
      "atribuicoes": [
        "Art. 39, § 1º — O Curso Superior de Bombeiro-Militar destina-se a aprimorar os conhecimentos técnico-profissionais e culturais dos oficiais superiores da Corporação, desenvolvendo a aptidão em trabalhos de Estado-Maior, acrescer conhecimentos relativos ao exercício de chefia, de forma a habilitá-los ao desempenho das funções mais elevadas do Corpo."
      ],
      "desdobramentos": [],
      "cargos": [
        {"cargo": "Diretor do CSBM", "subordinadoA": "Diretor de Ensino", "requisito": "Oficial Superior BM", "desdobramentos": [], "atribuicoes": []}
      ]
    },
    "esfao": {
      "name": "Escola de Formação e Aperfeiçoamento de Oficiais", "abbreviation": "EsFAO", "category": "Apoio",
      "subordinadoA": "Diretoria de Ensino", "legalRef": "Art. 39 § 2º",
      "baseLegal": "Lei nº 250, de 02 de julho de 1979",
      "artigosDeOrigem": ["Art. 39 § 2º (EsFAO)"],
      "atribuicoes": [
        "Art. 39, § 2º — A Escola de Formação e Aperfeiçoamento de Oficiais destina-se à formação, ao aperfeiçoamento e à especialização dos oficiais do Corpo e, eventualmente, de oficiais de outras Corporações.",
        "Art. 39, § 2º, a — Curso de Aperfeiçoamento de Oficiais (CAO);",
        "Art. 39, § 2º, b — Curso de Especialização em Prevenção de Incêndio (CEPrevI);",
        "Art. 39, § 2º, c — Curso de Formação de Oficiais (CFO)."
      ],
      "desdobramentos": ["Curso de Aperfeiçoamento de Oficiais (CAO)", "Curso de Especialização em Prevenção de Incêndio (CEPrevI)", "Curso de Formação de Oficiais (CFO)"],
      "cargos": [
        {"cargo": "Diretor da EsFAO", "subordinadoA": "Diretor de Ensino", "requisito": "Oficial Superior BM", "desdobramentos": [], "atribuicoes": []}
      ]
    },
    "cfap-rj": {
      "name": "Centro de Formação e Aperfeiçoamento de Praças", "abbreviation": "CFAP", "category": "Apoio",
      "subordinadoA": "Diretoria de Ensino", "legalRef": "Art. 39 § 3º",
      "baseLegal": "Lei nº 250, de 02 de julho de 1979",
      "artigosDeOrigem": ["Art. 39 § 3º (CFAP)"],
      "atribuicoes": [
        "Art. 39, § 3º — O Centro de Formação e Aperfeiçoamento de Praças destina-se à formação, ao adestramento, ao aperfeiçoamento e à especialização das praças do Corpo e, eventualmente, de praças de outras Corporações.",
        "Art. 39, § 3º, a — Curso de Habilitação do Oficialato Administrativo e Especialista (CHOAE);",
        "Art. 39, § 3º, b — Curso de Aperfeiçoamento de Sargentos (CAS);",
        "Art. 39, § 3º, c — Curso de Formação de Sargentos (CFS);",
        "Art. 39, § 3º, d — Curso de Formação de Cabos (CFC);",
        "Art. 39, § 3º, e — Curso de Formação de Soldados (CFSd)."
      ],
      "desdobramentos": ["Curso de Habilitação do Oficialato Administrativo e Especialista (CHOAE)", "Curso de Aperfeiçoamento de Sargentos (CAS)", "Curso de Formação de Sargentos (CFS)", "Curso de Formação de Cabos (CFC)", "Curso de Formação de Soldados (CFSd)"],
      "cargos": [
        {"cargo": "Diretor do CFAP", "subordinadoA": "Diretor de Ensino", "requisito": "Oficial Superior BM", "desdobramentos": [], "atribuicoes": []}
      ]
    },
    "pagc": {
      "name": "Pagadoria Central", "abbreviation": "PagC", "category": "Apoio",
      "subordinadoA": "Diretoria de Finanças", "legalRef": "Art. 41",
      "baseLegal": "Lei nº 250, de 02 de julho de 1979",
      "artigosDeOrigem": ["Art. 41 (Pagadoria Central)"],
      "atribuicoes": [
        "Art. 41, pú — A Pagadoria Central é o órgão de Apoio incumbido de proceder aos recebimentos e pagamentos relativos ao movimento financeiro da Corporação, efetuando, ainda, o controle de suas contas bancárias."
      ],
      "desdobramentos": [],
      "cargos": [
        {"cargo": "Chefe da Pagadoria Central", "subordinadoA": "Diretor de Finanças", "requisito": "Oficial BM", "desdobramentos": [], "atribuicoes": []}
      ]
    },
    "csm-mop": {
      "name": "Centro de Suprimento e Manutenção — Material Operacional", "abbreviation": "CSM/MOp", "category": "Apoio",
      "subordinadoA": "Diretoria de Apoio Logístico", "legalRef": "Art. 43 § 1º",
      "baseLegal": "Lei nº 250, de 02 de julho de 1979",
      "artigosDeOrigem": ["Art. 43 § 1º (CSM/MOp)"],
      "atribuicoes": [
        "Art. 43, § 1º — O Centro de Suprimento e Manutenção de Material Operacional é o órgão de Apoio incumbido da obtenção, da estocagem e da distribuição dos suprimentos específicos e da execução da manutenção do armamento e do material especializado de bombeiro."
      ],
      "desdobramentos": [],
      "cargos": [
        {"cargo": "Chefe do CSM/MOp", "subordinadoA": "Diretor de Apoio Logístico", "requisito": "Oficial BM", "desdobramentos": [], "atribuicoes": []}
      ]
    },
    "csm-mmoto": {
      "name": "Centro de Suprimento e Manutenção — Material Motorizado", "abbreviation": "CSM/MMoto", "category": "Apoio",
      "subordinadoA": "Diretoria de Apoio Logístico", "legalRef": "Art. 43 § 2º",
      "baseLegal": "Lei nº 250, de 02 de julho de 1979",
      "artigosDeOrigem": ["Art. 43 § 2º (CSM/MMoto)"],
      "atribuicoes": [
        "Art. 43, § 2º — O Centro de Suprimento e Manutenção de Material Motorizado é o órgão de Apoio incumbido do suprimento e da manutenção das viaturas e de todo o equipamento motorizado da Corporação, bem como da obtenção e da estocagem de todo material necessário a esse fim."
      ],
      "desdobramentos": [],
      "cargos": [
        {"cargo": "Chefe do CSM/MMoto", "subordinadoA": "Diretor de Apoio Logístico", "requisito": "Oficial BM", "desdobramentos": [], "atribuicoes": []}
      ]
    },
    "csm-int": {
      "name": "Centro de Suprimento e Manutenção — Intendência", "abbreviation": "CSM/Int", "category": "Apoio",
      "subordinadoA": "Diretoria de Apoio Logístico", "legalRef": "Art. 43 § 3º",
      "baseLegal": "Lei nº 250, de 02 de julho de 1979",
      "artigosDeOrigem": ["Art. 43 § 3º (CSM/Int)"],
      "atribuicoes": [
        "Art. 43, § 3º — O Centro de Suprimento e Manutenção de Intendência é o órgão de Apoio incumbido da obtenção, do armazenamento e da distribuição dos suprimentos específicos e da execução da manutenção do material de intendência; tem, igualmente, a seu cargo o apoio de subsistência à Corporação."
      ],
      "desdobramentos": [],
      "cargos": [
        {"cargo": "Chefe do CSM/Int", "subordinadoA": "Diretor de Apoio Logístico", "requisito": "Oficial BM", "desdobramentos": [], "atribuicoes": []}
      ]
    },
    "csm-o": {
      "name": "Centro de Suprimento e Manutenção — Obras", "abbreviation": "CSM/O", "category": "Apoio",
      "subordinadoA": "Diretoria de Apoio Logístico", "legalRef": "Art. 43 § 4º",
      "baseLegal": "Lei nº 250, de 02 de julho de 1979",
      "artigosDeOrigem": ["Art. 43 § 4º (CSM/O)"],
      "atribuicoes": [
        "Art. 43, § 4º — O Centro de Suprimento e Manutenção de Obras é o órgão de Apoio incumbido de atender às necessidades de obras e reparos nos aquartelamentos e edifícios da Corporação."
      ],
      "desdobramentos": [],
      "cargos": [
        {"cargo": "Chefe do CSM/O", "subordinadoA": "Diretor de Apoio Logístico", "requisito": "Oficial BM", "desdobramentos": [], "atribuicoes": []}
      ]
    },
    "csm-mtel": {
      "name": "Centro de Suprimento e Manutenção — Telecomunicações", "abbreviation": "CSM/MTel", "category": "Apoio",
      "subordinadoA": "Diretoria de Apoio Logístico", "legalRef": "Art. 43 § 5º",
      "baseLegal": "Lei nº 250, de 02 de julho de 1979",
      "artigosDeOrigem": ["Art. 43 § 5º (CSM/MTel)"],
      "atribuicoes": [
        "Art. 43, § 5º — O Centro de Suprimento e Manutenção de Material de Telecomunicações é o órgão de Apoio incumbido da obtenção, da estocagem, da distribuição e da execução da manutenção do material de comunicações."
      ],
      "desdobramentos": [],
      "cargos": [
        {"cargo": "Chefe do CSM/MTel", "subordinadoA": "Diretor de Apoio Logístico", "requisito": "Oficial BM", "desdobramentos": [], "atribuicoes": []}
      ]
    },
    "hcb": {
      "name": "Hospitais do Corpo de Bombeiros", "abbreviation": "HCB", "category": "Apoio",
      "subordinadoA": "Diretoria de Apoio Logístico", "legalRef": "Art. 43 § 6º",
      "baseLegal": "Lei nº 250, de 02 de julho de 1979",
      "artigosDeOrigem": ["Art. 43 § 6º (Hospitais e Policlínicas)"],
      "atribuicoes": [
        "Art. 43, § 6º — Os Hospitais e as Policlínicas são os órgãos de Apoio incumbidos de prestar assistência médica, odontológica, farmacêutica e laboratorial ao pessoal da Corporação, da ativa e inativas, seus dependentes e pensionistas, assim como efetuar as inspeções de saúde e demais procedimentos de perícia médica que se tornem necessários."
      ],
      "desdobramentos": [],
      "cargos": [
        {"cargo": "Diretor do Hospital do CB", "subordinadoA": "Diretor de Apoio Logístico", "requisito": "Oficial BM de Saúde (QOS)", "desdobramentos": [], "atribuicoes": []}
      ]
    },
    "polcb": {
      "name": "Policlínicas do Corpo de Bombeiros", "abbreviation": "PolCB", "category": "Apoio",
      "subordinadoA": "Diretoria de Apoio Logístico", "legalRef": "Art. 43 § 6º",
      "baseLegal": "Lei nº 250, de 02 de julho de 1979",
      "artigosDeOrigem": ["Art. 43 § 6º (Hospitais e Policlínicas)"],
      "atribuicoes": [
        "Art. 43, § 6º — Os Hospitais e as Policlínicas são os órgãos de Apoio incumbidos de prestar assistência médica, odontológica, farmacêutica e laboratorial ao pessoal da Corporação, da ativa e inativas, seus dependentes e pensionistas, assim como efetuar as inspeções de saúde e demais procedimentos de perícia médica que se tornem necessários."
      ],
      "desdobramentos": [],
      "cargos": [
        {"cargo": "Chefe da Policlínica do CB", "subordinadoA": "Diretor de Apoio Logístico", "requisito": "Oficial BM de Saúde (QOS)", "desdobramentos": [], "atribuicoes": []}
      ]
    },
    "cba": {
      "name": "Comando de Bombeiros de Área", "abbreviation": "CBA", "category": "Execução",
      "subordinadoA": "Comandante-Geral", "legalRef": "Art. 44 § 1º",
      "baseLegal": "Lei nº 250, de 02 de julho de 1979",
      "artigosDeOrigem": ["Art. 44 § 1º (Comando de Bombeiros de Área)"],
      "atribuicoes": [
        "Art. 44, § 1º — Os Comandos de Bombeiros da Área, diretamente subordinados ao Comando-Geral, são responsáveis pelo planejamento, supervisão e execução das missões específicas de bombeiro-militar, na respectiva área, de acordo com as diretrizes e ordens do Comando-Geral."
      ],
      "desdobramentos": ["Comandante", "Estado-Maior (B/1 a B/5)", "Centro de Operações"],
      "cargos": [
        {"cargo": "Comandante de Bombeiros de Área", "subordinadoA": "Comandante-Geral", "requisito": "Oficial Superior BM", "desdobramentos": [], "atribuicoes": []}
      ]
    },
    "cocb-rj": {
      "name": "Centro de Operações do Corpo de Bombeiros", "abbreviation": "COCB", "category": "Execução",
      "subordinadoA": "Comandante-Geral", "legalRef": "Art. 44 § 3º",
      "baseLegal": "Lei nº 250, de 02 de julho de 1979",
      "artigosDeOrigem": ["Art. 44 § 3º (COCB)"],
      "atribuicoes": [
        "Art. 44, § 3º — O Centro de Operações do Corpo de Bombeiros é um órgão de Execução, subordinado ao Comandante-Geral, equipado com meios variados de comunicações, destinado a controlar e coordenar a atuação das Unidades Operacionais da Corporação e será organizado de forma a possibilitar ligações eficientes com todas as Unidades Operacionais da Corporação, e com os órgãos responsáveis pela segurança do Estado do Rio de Janeiro."
      ],
      "desdobramentos": [],
      "cargos": [
        {"cargo": "Chefe do COCB", "subordinadoA": "Comandante-Geral", "requisito": "Oficial Superior BM", "desdobramentos": [], "atribuicoes": []}
      ]
    },
    "gi": {
      "name": "Grupamento de Incêndio", "abbreviation": "GI", "category": "Execução",
      "subordinadoA": "Comando de Bombeiros de Área", "legalRef": "Art. 45 § 1º",
      "baseLegal": "Lei nº 250, de 02 de julho de 1979",
      "artigosDeOrigem": ["Art. 45 § 1º (Grupamento de Incêndio)"],
      "atribuicoes": [
        "Art. 45, § 1º — Unidade de Extinção de Incêndio Terrestre é a que tem a seu cargo, dentro do território de sua responsabilidade, as missões de extinção de incêndios e suas decorrências."
      ],
      "desdobramentos": ["Subgrupamentos de Incêndio (S/GI)", "Subgrupamentos de Incêndio Independentes (S/GI-Ind)", "Destacamentos de Bombeiros"],
      "cargos": [
        {"cargo": "Comandante do Grupamento de Incêndio", "subordinadoA": "Comando de Bombeiros de Área", "requisito": "Oficial BM", "desdobramentos": [], "atribuicoes": []}
      ]
    },
    "gbs-rj": {
      "name": "Grupamento de Busca e Salvamento", "abbreviation": "GBS", "category": "Execução",
      "subordinadoA": "Comando de Bombeiros de Área", "legalRef": "Art. 45 § 2º",
      "baseLegal": "Lei nº 250, de 02 de julho de 1979",
      "artigosDeOrigem": ["Art. 45 § 2º (Grupamento de Busca e Salvamento)"],
      "atribuicoes": [
        "Art. 45, § 2º — Unidades de Busca e Salvamento é a que tem a seu cargo, dentro da área do Estado do Rio de Janeiro, as missões de busca e salvamento, tanto terrestre, como aquática."
      ],
      "desdobramentos": ["Subgrupamentos de Busca e Salvamento (S/GBS)"],
      "cargos": [
        {"cargo": "Comandante do Grupamento de Busca e Salvamento", "subordinadoA": "Comando de Bombeiros de Área", "requisito": "Oficial BM", "desdobramentos": [], "atribuicoes": []}
      ]
    },
    "gmar": {
      "name": "Grupamento Marítimo", "abbreviation": "Gmar", "category": "Execução",
      "subordinadoA": "Comando de Bombeiros de Área", "legalRef": "Art. 45 § 3º",
      "baseLegal": "Lei nº 250, de 02 de julho de 1979",
      "artigosDeOrigem": ["Art. 45 § 3º (Grupamento Marítimo)"],
      "atribuicoes": [
        "Art. 45, § 3º — Unidade de Extinção de Incêndio e Salvamento Marítimo é a que tem a seu cargo as missões de extinção de incêndios, buscas e salvamento em embarcações, ilhas e orla marítima do Estado do Rio de Janeiro."
      ],
      "desdobramentos": ["Subgrupamentos Marítimos (S/Gmar)"],
      "cargos": [
        {"cargo": "Comandante do Grupamento Marítimo", "subordinadoA": "Comando de Bombeiros de Área", "requisito": "Oficial BM", "desdobramentos": [], "atribuicoes": []}
      ]
    }
  }
},

"sc": {
  "legal_source": "Lei Complementar nº 724, de 18 de julho de 2018; Decreto nº 1.328, de 14 de junho de 2021",
  "organs": {
    "cg-sc": {
      "name": "Comando-Geral", "abbreviation": "CG", "category": "Direção Geral",
      "subordinadoA": "Governador do Estado", "legalRef": "Art. 8º, I; Art. 14 Dec. 1.328/2021",
      "baseLegal": "Lei Complementar nº 724, de 18 de julho de 2018",
      "artigosDeOrigem": ["Art. 14 (Atribuições exclusivas do Comandante-Geral)"],
      "atribuicoes": [
        "I - concessão de medalha, condecoração e comenda;",
        "II - movimentação de Oficial;",
        "III - desenvolvimento funcional das Praças pela progressão por antiguidade e por merecimento;",
        "IV - assinatura de convênios com municípios, relativos à prestação de serviços de bombeiro militar e outras atividades consideradas por LEI de competência do CBMSC;",
        "V - agregação e reversão de Praças e Oficiais do CBMSC;",
        "VI - exclusão do serviço ativo das Praças;",
        "VII - convocação e dispensa de Oficial da Reserva Remunerada do CBMSC para compor Conselho Especial de Justiça ou Conselho de Justificação, ambos encarregados de inquérito policial-militar, ou para outros procedimentos administrativos na falta de oficial da ativa em situação hierárquica compatível com a do oficial envolvido;",
        "VIII - assinatura de termos de cooperação técnica e convênios com órgãos cujo objeto seja de interesse da Corporação; e",
        "IX - designação e respectiva dispensa dos servidores inativos ao Corpo Temporário de Inativos da Segurança Pública (CTISP), após autorização do Grupo Gestor de Governo (GGG)."
      ],
      "desdobramentos": [],
      "cargos": [{"cargo": "Comandante-Geral", "subordinadoA": "Governador do Estado", "requisito": "Coronel QOBM", "desdobramentos": [], "atribuicoes": ["Atribuições exclusivas previstas no Art. 14 I-IX do Dec. nº 1.328/2021; atribuições delegáveis do Art. 15 I-VI."]}]
    },
    "scmt-sc": {
      "name": "Subcomando-Geral", "abbreviation": "SCG", "category": "Direção Geral",
      "subordinadoA": "Comandante-Geral", "legalRef": "Art. 8º, I, b; Art. 16 Dec. 1.328/2021",
      "baseLegal": "Lei Complementar nº 724, de 18 de julho de 2018",
      "artigosDeOrigem": ["Art. 16 (Atribuições do Subcomandante-Geral)"],
      "atribuicoes": [
        "I - assessorar o Comandante-Geral no desempenho de suas atribuições;",
        "II - planejar as operações que importem em uma coordenação ao nível estadual ou que envolvam mais de uma RBM, bem como as relativas à participação do CBMSC em solenidades, paradas e desfiles militares;",
        "III - coordenar, controlar e supervisionar as atividades desenvolvidas pelos órgãos de direção operacional e pelos órgãos de execução da Corporação;",
        "IV - coordenar toda a execução do atendimento a eventos críticos; e",
        "V - definir o emprego de Força-Tarefa, de acordo com as diretrizes do Comando-Geral do CBMSC, que extrapole os limites da circunscrição de uma RBM."
      ],
      "desdobramentos": [],
      "cargos": [{"cargo": "Subcomandante-Geral", "subordinadoA": "Comandante-Geral", "requisito": "Coronel QOBM", "desdobramentos": [], "atribuicoes": ["I a V – atribuições do Art. 16 Dec. nº 1.328/2021."]}]
    },
    "emg-sc": {
      "name": "Estado-Maior Geral", "abbreviation": "EMG", "category": "Direção Estratégica",
      "subordinadoA": "Comandante-Geral", "legalRef": "Art. 8º, I, c; Art. 17 Dec. 1.328/2021",
      "baseLegal": "Lei Complementar nº 724, de 18 de julho de 2018",
      "artigosDeOrigem": ["Art. 17 (Atribuições do Chefe do Estado-Maior Geral)"],
      "atribuicoes": [
        "I - assessorar o Comandante-Geral no nível estratégico do CBMSC;",
        "II - prestar assistência ao Comandante-Geral no desempenho de suas atividades, elaborando estudos e projetos e planejando, controlando e gerindo planos institucionais;",
        "III - supervisionar a elaboração e execução de normas, instruções, diretrizes, planos e ordens do CBMSC;",
        "IV - orientar, controlar e supervisionar os órgãos de direção, apoio e execução no cumprimento de suas atribuições; e",
        "V - desenvolver outras atividades relacionadas à direção geral do CBMSC."
      ],
      "desdobramentos": [],
      "cargos": [{"cargo": "Chefe do Estado-Maior Geral", "subordinadoA": "Comandante-Geral", "requisito": "Coronel QOBM", "desdobramentos": [], "atribuicoes": ["I a V – atribuições do Art. 17 Dec. nº 1.328/2021."]}]
    },
    "gab-sc": {
      "name": "Gabinete do Comando-Geral", "abbreviation": "Gab", "category": "Assessoramento",
      "subordinadoA": "Comandante-Geral", "legalRef": "Art. 8º, I, d; Art. 26 Dec. 1.328/2021",
      "baseLegal": "Lei Complementar nº 724, de 18 de julho de 2018",
      "artigosDeOrigem": ["Art. 26 (Atribuições do Gabinete do Comando-Geral)"],
      "atribuicoes": [
        "I - atuar de forma sistêmica e integrada com os demais órgãos do CBMSC; e",
        "II - exercer, por meio da Ajudância-Geral, a articulação institucional e a coordenação das atividades administrativas do Gabinete do Comando-Geral."
      ],
      "desdobramentos": [],
      "cargos": [{"cargo": "Ajudante-Geral", "subordinadoA": "Comandante-Geral", "requisito": "Coronel QOBM, designado por ATO do Comandante-Geral (Art. 27 §3º)", "desdobramentos": [], "atribuicoes": ["Chefia do Gabinete do Comando-Geral, exercida pelo Ajudante-Geral (Art. 26 §único)."]}]
    },
    "ag-sc": {
      "name": "Ajudância-Geral", "abbreviation": "AG", "category": "Assessoramento",
      "subordinadoA": "Gabinete do Comando-Geral", "legalRef": "Art. 27 Dec. 1.328/2021",
      "baseLegal": "Lei Complementar nº 724, de 18 de julho de 2018",
      "artigosDeOrigem": ["Art. 27 §1º (Atribuições da Ajudância-Geral)", "Art. 27 §2º (Atribuições do Ajudante-Geral)"],
      "atribuicoes": [
        "I - desenvolver os trabalhos de secretaria e de documentações inerentes ao Comandante-Geral;",
        "II - administrar e executar a atividade de protocolo geral da Corporação e propor a normatização do serviço para os demais órgãos;",
        "III - receber e registrar a correspondência oficial, petições, processos, documentos e quaisquer expedientes endereçados ao Comando-Geral;",
        "IV - promover o controle dos atos administrativos assinados pelo Comandante-Geral;",
        "V - administrar o arquivo geral da Corporação e propor a normatização do serviço para os demais órgãos;",
        "VI - planejar, organizar e dirigir os serviços de segurança interna e externa do Quartel do Comando-Geral;",
        "VII - administrar o serviço geral do Quartel do Comando-Geral; e",
        "VIII - publicar e distribuir o Boletim do CBMSC."
      ],
      "desdobramentos": [],
      "cargos": [{"cargo": "Ajudante-Geral", "subordinadoA": "Comandante-Geral", "requisito": "Coronel QOBM, designado por ATO do Comandante-Geral (Art. 27 §3º)", "desdobramentos": [], "atribuicoes": [
        "I - dirigir, supervisionar e coordenar os trabalhos da Ajudância-Geral;",
        "II - elaborar e expedir as normas de funcionamento da Ajudância-Geral;",
        "III - redigir toda a correspondência, cuja natureza assim o exigir;",
        "IV - subscrever certidões e papéis análogos;",
        "V - conferir e autenticar as cópias de documentos existentes no arquivo, mandadas extrair por autoridade competente, bem como conferir e assinar as cópias autênticas de documentos da Corporação;",
        "VI - manter em dia e em ordem, o arquivo da documentação da Ajudância-Geral, de acordo com as normas em vigor;",
        "VII - despachar e distribuir correspondência oficial, petições, processos, documentos ou quaisquer expedientes endereçados ao Comandante-Geral e que não necessitem intervenção direta deste, bem como aqueles que para serem decididos necessitem de parecer ou manifestação prévia do correspondente órgão de direção, apoio ou execução;",
        "VIII - fiscalizar pessoalmente a expedição da correspondência, fazendo registrá-la no protocolo em que será passado o competente recibo;",
        "IX - estabelecer a ligação com os comandos dos elementos subordinados da Corporação e demais órgãos públicos, no trato das atividades relacionadas com a sua área de competência;",
        "X - emitir conceitos e elogios, conceder recompensas, férias, licenças e dispensas do serviço, bem como aplicar punições ao pessoal que servir sob as suas ordens, na forma da legislação em vigor;",
        "XI - organizar e manter em dia o livro ou fichário de apresentação de oficiais no Quartel do Comando-Geral, providenciando a devida publicação em Boletim do CBMSC;",
        "XII - providenciar a publicação dos atos, ordens e despachos do Comandante-Geral, bem como dos demais atos de interesse da Corporação;",
        "XIII - colaborar na organização da pauta de audiência do Comandante-Geral, em articulação com o Ajudante de Ordens;",
        "XIV - dirigir a escrituração referente à correspondência, ao arquivo e ao registro das alterações dos Oficiais lotados no Comando-Geral, Subcomando-Geral, Estado-Maior Geral, Comunicação Social e Assessoria Jurídica;",
        "XV - publicar e distribuir o Boletim do CBMSC; e",
        "XVI - exercer outras atividades correlatas ou desempenhar missões especiais temporárias, de caráter relevante, conforme for definido por ATO do Comandante-Geral."
      ]}]
    },
    "ccs-sc": {
      "name": "Centro de Comunicação Social", "abbreviation": "CCS", "category": "Assessoramento",
      "subordinadoA": "Gabinete do Comando-Geral", "legalRef": "Art. 8º §4º; Art. 28 Dec. 1.328/2021",
      "baseLegal": "Lei Complementar nº 724, de 18 de julho de 2018",
      "artigosDeOrigem": ["Art. 28 (Atribuições do Centro de Comunicação Social)"],
      "atribuicoes": [
        "I - planejar, desenvolver, coordenar e executar as atividades de comunicação social do CBMSC;",
        "II - assessorar o Comandante-Geral nos aspectos relacionados à imprensa, divulgação institucional e conscientização social;",
        "III - elaborar, de acordo com a orientação do Comando-Geral: a) as diretrizes referentes à comunicação social, com base nas instruções do Comando-Geral e Governo do Estado; e b) o Plano Institucional de Comunicação Social.",
        "IV - desenvolver e propor políticas de relacionamento da Corporação com órgãos e entidades públicas e privadas, com profissionais da Corporação e com a população;",
        "V - divulgar as atividades desenvolvidas pelo CBMSC por meio dos diversos veículos de comunicação social;",
        "VI - manter o Comandante-Geral informado sobre fatos de interesse do CBMSC, quando veiculados pela imprensa;",
        "VII - regular, planejar, coordenar e executar o cerimonial militar e o cerimonial das atividades sociais de interesse do Comando-Geral frequentes e aqueles extraordinários determinados pelo Comandante-Geral;",
        "VIII - promover a imagem institucional e mercadológica do CBMSC nos ambientes sociais e de segurança pública;",
        "IX - possibilitar a elaboração de respostas coordenadas, articuladas, adequadas e oportunas, aos questionamentos da sociedade e do cidadão, sobre assuntos de interesse da Instituição;",
        "X - coordenar as ações dos elementos subordinados em seus relacionamentos com outros órgãos de comunicação, que exijam, pela natureza da pauta, articulação interna e participação coordenada;",
        "XI - assessorar e supervisionar o conteúdo de comunicação social no âmbito da Corporação;",
        "XII - administrar os canais de comunicação oficiais da Corporação e monitorar os canais de comunicação em nível dos elementos subordinados; e",
        "XIII - acompanhar, analisar e informar o Comando-Geral a repercussão na sociedade das mídias utilizadas pela Corporação."
      ],
      "desdobramentos": [],
      "cargos": [{"cargo": "Chefe do Centro de Comunicação Social", "subordinadoA": "Gabinete do Comando-Geral", "requisito": "Oficial QOBM", "desdobramentos": [], "atribuicoes": ["Chefia do Centro de Comunicação Social (Art. 8º, I, d, 3 e §4º Dec. nº 1.328/2021)."]}]
    },
    "ce-sc": {
      "name": "Conselho Estratégico", "abbreviation": "CE", "category": "Assessoramento",
      "subordinadoA": "Comandante-Geral", "legalRef": "Art. 8º, I, e; Art. 30 Dec. 1.328/2021",
      "baseLegal": "Lei Complementar nº 724, de 18 de julho de 2018",
      "artigosDeOrigem": ["Art. 30 (Atribuições do Conselho Estratégico)"],
      "atribuicoes": [
        "I - prestar assistência ao Comando-Geral no desempenho das atividades relacionadas com a execução do planejamento estratégico da Corporação, auxiliando no processo de tomada de decisão;",
        "II - colaborar na elaboração de planos e ordens do Comando-Geral relacionados com pessoal, informações, instrução, operações, ensino, assuntos administrativos, assuntos civis, planejamento administrativo, programação e orçamento; e",
        "III - desenvolver outras atividades de interesse ou determinadas pelo Comando-Geral da Corporação."
      ],
      "desdobramentos": [],
      "cargos": []
    },
    "ass-jur-sc": {
      "name": "Assessoria Jurídica", "abbreviation": "AJ", "category": "Assessoramento",
      "subordinadoA": "Comandante-Geral", "legalRef": "Art. 8º, I, f; Art. 32 Dec. 1.328/2021",
      "baseLegal": "Lei Complementar nº 724, de 18 de julho de 2018",
      "artigosDeOrigem": ["Art. 32 (Atribuições da Assessoria Jurídica)"],
      "atribuicoes": [
        "I - programar, organizar, orientar, coordenar, executar e controlar as atividades relacionadas com os serviços jurídicos, no âmbito do CBMSC, vinculando-se tecnicamente à Consultoria Jurídica da SSP e à Procuradoria-Geral do Estado (PGE);",
        "II - examinar a legalidade dos atos administrativos que lhe forem submetidos à apreciação pelo Comandante-Geral, Subcomandante-Geral e Chefe do Estado-Maior Geral;",
        "III - participar do processo legislativo de elaboração de anteprojetos de LEI e DECRETO relacionados às atividades do CBMSC;",
        "IV - coordenar a elaboração de informações em mandados de segurança e habeas corpus do Comandante-Geral, do Subcomandante-Geral e do Chefe do Estado-Maior Geral, sendo as informações inerentes às demais autoridades coatoras a cargo de suas assessorias ou corregedorias setoriais;",
        "V - requisitar de quaisquer órgãos ou entidades da Corporação, documentos ou informações necessários ao exame de matéria jurídica a ele submetida, devendo os consultados atender no prazo estipulado pela Assessoria Jurídica; e",
        "VI - apreciar editais de concurso e processos seletivos de pessoal."
      ],
      "desdobramentos": [],
      "cargos": [{"cargo": "Chefe da Assessoria Jurídica", "subordinadoA": "Comandante-Geral", "requisito": "Oficial superior da ativa com formação em Direito (Art. 32)", "desdobramentos": [], "atribuicoes": ["I a VI – atribuições previstas no Art. 32 do Dec. nº 1.328/2021."]}]
    },
    "correg-sc": {
      "name": "Corregedoria-Geral", "abbreviation": "Corr-G", "category": "Correição",
      "subordinadoA": "Comandante-Geral", "legalRef": "Art. 8º, II; Art. 33 Dec. 1.328/2021",
      "baseLegal": "Lei Complementar nº 724, de 18 de julho de 2018",
      "artigosDeOrigem": ["Art. 33 (Atribuições da Corregedoria-Geral)"],
      "atribuicoes": [
        "I - promover o acompanhamento das apurações de transgressões disciplinares e ilícitos penais atribuídos a bombeiros militares, realizadas pelos órgãos de direção, de apoio, e de execução do CBMSC, avocando-as quando necessário;",
        "II - promover integração com os órgãos do Poder Judiciário, Ministério Público, Defensoria Pública e corregedorias de outros órgãos, nos temas relacionados a suas atribuições;",
        "III - baixar normas técnicas em conjunto com Estado-Maior Geral, relativas às atividades de sua competência e controlar a sua aplicação;",
        "IV - gerenciar o sistema de corregedoria do CBMSC;",
        "V - manter cópia digitalizada dos procedimentos disciplinares e penais que forem instaurados no CBMSC;",
        "VI - efetuar investigações, levantamentos externos ou diligências em conjunto com a Agência Central de Inteligência, para proveito das apurações das infrações penais militares e transgressões disciplinares e sua autoria, imputada a bombeiros militares;",
        "VII - elaborar estatísticas relativas às suas atividades; e",
        "VIII - remeter, com exclusividade, à Justiça Militar, os Inquéritos Policiais Militares, Sindicâncias e outros processos que tenham relação com a apuração no âmbito criminal, concernentes a atos praticados por integrantes do CBMSC."
      ],
      "desdobramentos": [],
      "cargos": [{"cargo": "Corregedor-Geral", "subordinadoA": "Comandante-Geral", "requisito": "Coronel QOBM", "desdobramentos": [], "atribuicoes": ["I a VIII – atribuições previstas no Art. 33 do Dec. nº 1.328/2021."]}]
    },
    "dp-sc": {
      "name": "Diretoria de Pessoal", "abbreviation": "DP", "category": "Direção Setorial",
      "subordinadoA": "Chefe do Estado-Maior Geral", "legalRef": "Art. 9º, I; Art. 34 Dec. 1.328/2021",
      "baseLegal": "Lei Complementar nº 724, de 18 de julho de 2018",
      "artigosDeOrigem": ["Art. 34 (Atribuições da Diretoria de Pessoal)"],
      "atribuicoes": [
        "I - controlar todas as atividades relacionadas com a vida funcional do pessoal militar e civil da Corporação, mantendo registros individuais;",
        "II - promover a seleção para o ingresso no CBMSC e para admissão de pessoal civil, bem como o serviço de identificação;",
        "III - executar as atividades relativas ao pagamento, alterações e demais encargos relativos ao pessoal ativo, inativo, pensionista e civil;",
        "IV - executar as atividades pertinentes à documentação do pessoal do CBMSC;",
        "V - desenvolver os planos e baixar as ordens decorrentes das diretrizes da política de pessoal da Corporação;",
        "VI - propor a movimentação de Oficiais ao Comandante-Geral, e a de Praças ao Subcomandante-Geral;",
        "VII - preparar os atos de movimentação, classificação e nomeação de Oficiais;",
        "VIII - preparar os atos de movimentação, classificação e designação de Praças e Civis;",
        "IX - manter ligação através do Comandante-Geral com os órgãos do Exército Brasileiro, relacionados com o controle do pessoal bombeiro militar;",
        "X - estudar e instruir os processos administrativos e submetê-los à consideração do Chefe do Estado-Maior Geral em que lhe extrapolarem à competência;",
        "XI - manter o controle do pessoal agregado, excluído e licenciado;",
        "XII - atualizar a cada promoção os Almanaques de Oficiais, Subtenentes, Sargentos, Cabos e Soldados;",
        "XIII - elaborar a documentação da Comissão de Promoção de Oficiais e Comissão de Promoção de Praças;",
        "XIV - elaborar os processos de concessão de medalhas;",
        "XV - coordenar e controlar a execução do plano de férias da Corporação;",
        "XVI - coletar dados e realizar inspeção de caráter setorial, visando à elaboração de estudos e propostas de medidas a serem submetidas ao Chefe do Estado-Maior Geral, para a melhoria e aperfeiçoamento do sistema de administração de pessoal;",
        "XVII - elaborar estatísticas e relatórios das atividades da Diretoria;",
        "XVIII - manter e operacionalizar o funcionamento das comissões permanentes e de mérito;",
        "XIX - planejar, orientar, coordenar, controlar e fiscalizar as atividades de saúde ocupacional, segurança do trabalho, assistência médica, odontológica e psicológica do pessoal do CBMSC e de seus dependentes;",
        "XX - proceder o controle médico-sanitário do pessoal;",
        "XXI - atender, no que lhe couber, a seleção do pessoal do CBMSC;",
        "XXII - elaborar e executar programas de medicina preventiva e saúde comunitária;",
        "XXIII - promover a realização de estudos, análises, e pesquisas, visando ao aperfeiçoamento do Sistema de Saúde e Assistência Social;",
        "XXIV - baixar normas técnicas relativas às atividades de sua competência e controlar a sua aplicação;",
        "XXV - tratar dos assuntos de estatística e modernização administrativa, na esfera de suas atribuições;",
        "XXVI - tratar da coordenação, controle, e fiscalização, por meio de inspeções técnico-administrativas dos órgãos do Sistema de Saúde e Assistência Social;",
        "XXVII - propor ao Estado-Maior Geral medidas que visem aprimorar as diretrizes gerais e aperfeiçoar a legislação e a Política de Saúde Ocupacional e Segurança do Trabalho e Assistência Social;",
        "XXVIII - estabelecer e manter intercâmbio técnico-científico com entidades afins;",
        "XXIX - propor a realização de convênios e contratos com entidades médicas ou técnico-profissionais, do direito público ou privado, visando à complementação e à racionalização dos serviços que lhe são afetos;",
        "XXX - colaborar na especificação, padronização, catalogação e distribuição do material necessário às suas atividades e instruir a sua utilização e manutenção;",
        "XXXI - elaborar normas, planos, programas, ordens e instruções relacionadas com o Sistema de Saúde e Assistência Social;",
        "XXXII - elaborar e propor ao Estado-Maior Geral os manuais e instruções técnicas;",
        "XXXIII - realizar as perícias médicas ou médico-legais, psicológicas e físicas, através do corpo técnico disponível;",
        "XXXIV - prover, controlar e fiscalizar as atividades relacionadas à promoção da saúde e qualidade de vida, assistência social e religiosa do CBMSC;",
        "XXXV - acompanhar a vida laboral do BM, avaliando-os sob os parâmetros de saúde, condicionamento físico e mental, anualmente;",
        "XXXVI - avaliar os riscos ocupacionais das atividades laborais do bombeiro militar (administrativas e operacionais) definindo ações para mitigá-los;",
        "XXXVII - realizar as investigações dos acidentes no trabalho definindo as ações necessárias à sua prevenção;",
        "XXXVIII - promover estudos voltados ao desempenho humano, gerando estatísticas;",
        "XXXIX - planejar, coordenar e supervisionar a educação física no CBMSC, com foco na atividade operacional e desempenho humano;",
        "XL - elaborar normas relativas à educação física corporativa;",
        "XLI - coordenar eventos de natureza desportiva de interesse institucional;",
        "XLII - encaminhar os inaptos no TAF anual para a atividade-fim, ao devido tratamento e acompanhamento de saúde; e",
        "XLIII - planejar e operacionalizar os testes de aptidão física para inclusões, promoções, seleções de cursos internos e externos, e anuais para acompanhamento da saúde dos militares."
      ],
      "desdobramentos": [],
      "cargos": [{"cargo": "Diretor de Pessoal", "subordinadoA": "Chefe do EMG", "requisito": "Coronel QOBM (Art. 9º §2º)", "desdobramentos": [], "atribuicoes": ["I a XLIII – atribuições previstas no Art. 34 do Dec. nº 1.328/2021."]}]
    },
    "die-sc": {
      "name": "Diretoria de Instrução e Ensino", "abbreviation": "DIE", "category": "Direção Setorial",
      "subordinadoA": "Chefe do Estado-Maior Geral", "legalRef": "Art. 9º, II; Art. 35 Dec. 1.328/2021",
      "baseLegal": "Lei Complementar nº 724, de 18 de julho de 2018",
      "artigosDeOrigem": ["Art. 35 (Atribuições da Diretoria de Instrução e Ensino)"],
      "atribuicoes": [
        "I - planejar, elaborar, desenvolver, supervisionar, avaliar e revisar as normas das atividades de ensino na Corporação;",
        "II - elaborar, aprovar, regularizar e revisar os cursos e currículos da educação básica e complementar no CBMSC;",
        "III - fomentar o desenvolvimento de novas metodologias e processos de ensino e aprendizagem adequados a cada atividade de ensino;",
        "IV - elaborar, revisar e registrar os materiais didáticos utilizados no CBMSC;",
        "V - desenvolver projetos de ensino, bem como promover o fomento de convênios entre sistemas de ensino congêneres;",
        "VI - criar e executar processos de aprovação, acompanhamento, controle, encerramento, avaliação, auditoria, registro e emissão de certificados das atividades de ensino;",
        "VII - manter o controle, análise, homologação, inserção e arquivo da formação acadêmica, da educação básica e da educação complementar do efetivo da Corporação, desde a inclusão até a passagem para a inatividade;",
        "VIII - organizar os objetivos, metodologias, estratégias, atividades e avaliação da aprendizagem da atividade de ensino realizada por meio do ambiente virtual de aprendizagem;",
        "IX - executar, planejar e gerir os cursos ofertados pelo Centro de Educação e Formação de Condutores, bem como outros assuntos ligados à legislação de trânsito;",
        "X - manter o controle, análise, homologação e inserção das pontuações dos cursos civis e militares, bem como de estágios, treinamentos e ciclos de instrução de manutenção, para registro nos assentamentos dos militares, desde a inclusão até a passagem para inatividade; e",
        "XI - o Plano Geral de Ensino."
      ],
      "desdobramentos": [],
      "cargos": [{"cargo": "Diretor de Instrução e Ensino", "subordinadoA": "Chefe do EMG", "requisito": "Coronel QOBM (Art. 9º §2º)", "desdobramentos": [], "atribuicoes": ["I a XI – atribuições previstas no Art. 35 do Dec. nº 1.328/2021."]}]
    },
    "due-sc": {
      "name": "Diretoria de Urgência e Emergência", "abbreviation": "DUE", "category": "Direção Setorial",
      "subordinadoA": "Chefe do Estado-Maior Geral", "legalRef": "Art. 9º, III; Art. 36 Dec. 1.328/2021",
      "baseLegal": "Lei Complementar nº 724, de 18 de julho de 2018",
      "artigosDeOrigem": ["Art. 36 (Atribuições da Diretoria de Urgência e Emergência)"],
      "atribuicoes": [
        "I - planejar, orientar, coordenar, controlar e supervisionar as atividades de atendimento pré-hospitalar executadas pelo CBMSC em todo território catarinense;",
        "II - promover a integração com os demais órgãos de Estados que possuem atividades relacionadas e interligadas ao serviço de atendimento pré-hospitalar do CBMSC;",
        "III - promover o intercâmbio com demais estados da Federação e outros países, referentes a assuntos correlacionados com as atividades de atendimento pré-hospitalar;",
        "IV - elaborar e executar programas de controle de qualidade para as atividades de atendimento pré-hospitalar do CBMSC;",
        "V - promover a realização de estudos, análises e pesquisas, visando ao aperfeiçoamento do serviço de atendimento pré-hospitalar do CBMSC;",
        "VI - propor normas técnicas relativas às atividades de sua competência e controlar a sua aplicação;",
        "VII - elaborar estatística com foco na governança e modernização administrativa, na esfera de suas atribuições;",
        "VIII - coordenar, controlar e fiscalizar a execução de contratos ligados a sua esfera de atuação;",
        "IX - propor ao Estado-Maior Geral medidas que visem o aprimoramento das diretrizes gerais, manuais e instruções técnicas de atendimento pré-hospitalar;",
        "X - estabelecer e manter intercâmbio técnico-científico com entidades afins;",
        "XI - propor a realização de convênios e contratos com entidades afins às atividades da Diretoria;",
        "XII - colaborar na especificação, padronização, catalogação e elaboração de normas, planos, programas, ordens e instruções relacionadas com o serviço de atendimento pré-hospitalar e demais integrações em curso;",
        "XIII - coordenar a integração do atendimento pré-hospitalar do CBMSC com o SAMU catarinense, estadual e municipais."
      ],
      "desdobramentos": [],
      "cargos": [{"cargo": "Diretor de Urgência e Emergência", "subordinadoA": "Chefe do EMG", "requisito": "Coronel QOBM (Art. 9º §2º)", "desdobramentos": [], "atribuicoes": ["I a XIII – atribuições previstas no Art. 36 do Dec. nº 1.328/2021."]}]
    },
    "dlf-sc": {
      "name": "Diretoria de Logística e Finanças", "abbreviation": "DLF", "category": "Direção Setorial",
      "subordinadoA": "Chefe do Estado-Maior Geral", "legalRef": "Art. 9º, IV; Art. 37 Dec. 1.328/2021",
      "baseLegal": "Lei Complementar nº 724, de 18 de julho de 2018",
      "artigosDeOrigem": ["Art. 37 (Atribuições da Diretoria de Logística e Finanças)"],
      "atribuicoes": [
        "I - adquirir, transportar, armazenar e distribuir os diversos materiais e suprimentos, bem como contratar serviços essenciais;",
        "II - executar os processos licitatórios da Corporação para a aquisição de produtos e contratação de obras e serviços;",
        "III - nomear as comissões de licitação, pregoeiros e equipes de apoio para atuarem nos processos licitatórios;",
        "IV - elaborar, analisar, acompanhar e arquivar os processos relativos à celebração de convênios;",
        "V - propor, acompanhar e gerir os contratos administrativos, termos aditivos e apostilamentos;",
        "VI - assinar, rescindir e aplicar as penalidades administrativas relacionados aos contratos administrativos;",
        "VII - instaurar processos ostensivos a fim de apurar irregularidades verificadas em processos licitatórios e contratos administrativos;",
        "VIII - aplicar sanções administrativas a licitantes e fornecedores inadimplentes;",
        "IX - contatar os órgãos centrais da administração financeira do Estado, visando a liberação de recursos para a execução do programa de trabalho e/ou plano de aplicação;",
        "X - executar a contabilidade da Corporação;",
        "XI - confeccionar a prestação de contas concernentes aos processos licitatórios, contratos administrativos e convênios executados pela Diretoria;",
        "XII - cumprir o cronograma de desembolso de recursos financeiros;",
        "XIII - realizar levantamentos estatísticos das atividades financeiras;",
        "XIV - representar a Corporação perante as instituições financeiras e congêneres, bem como perante os órgãos centrais do governo no que tange à execução orçamentária e gestão financeira dos referidos órgãos;",
        "XV - aplicar e executar os recursos orçamentários e extraorçamentários;",
        "XVI - auditar os documentos comprobatórios de despesas da Corporação, liquidar e pagar fornecedores e prestadores de serviços contratados;",
        "XVII - realizar inspeções de caráter setorial na área financeira, logística e patrimonial;",
        "XVIII - emitir normativas internas que visem a padronização de procedimentos administrativos para a gestão logística e financeira da Corporação;",
        "XIX - identificar e manter o controle patrimonial da Corporação;",
        "XX - regularizar perante os órgãos constituídos os bens imóveis da Corporação;",
        "XXI - fazer a gestão do material bélico da Corporação, bem como realizar os processos de autorização para a aquisição, transferência, porte e demais providências afetas ao armamento particular dos militares integrantes da Instituição;",
        "XXII - realizar a gestão e identificação da frota, marítima, aérea e rodoviária;",
        "XXIII - executar o Plano Diretor de Tecnologia da Informação e Comunicação da Corporação, bem como propor atualizações quando necessário;",
        "XXIV - propor e fiscalizar a política de segurança da informação da Corporação;",
        "XXV - homologar as soluções de tecnologia da informação e comunicação a serem utilizadas pela Corporação;",
        "XXVI - coordenar atividades relacionadas com análise, programação e administração da base de dados da Corporação;",
        "XXVII - planejar, padronizar e controlar a instalação e manutenção preventiva, corretiva e evolutiva de soluções de tecnologia da informação e comunicação;",
        "XXVIII - efetuar, extraordinariamente, em caso de emergência, a manutenção das soluções de tecnologia da informação e comunicação; e",
        "XXIX - executar atividades relacionadas à pesquisa e desenvolvimento de novas tecnologias voltadas às atividades institucionais."
      ],
      "desdobramentos": [],
      "cargos": [{"cargo": "Diretor de Logística e Finanças", "subordinadoA": "Chefe do EMG", "requisito": "Coronel QOBM (Art. 9º §2º)", "desdobramentos": [], "atribuicoes": ["I a XXIX – atribuições previstas no Art. 37 do Dec. nº 1.328/2021."]}]
    },
    "dsci-sc": {
      "name": "Diretoria de Segurança Contra Incêndio", "abbreviation": "DSCI", "category": "Direção Setorial",
      "subordinadoA": "Chefe do Estado-Maior Geral", "legalRef": "Art. 9º, V; Art. 38 Dec. 1.328/2021",
      "baseLegal": "Lei Complementar nº 724, de 18 de julho de 2018",
      "artigosDeOrigem": ["Art. 38 (Atribuições da Diretoria de Segurança Contra Incêndio)"],
      "atribuicoes": [
        "I - a normatização em segurança contra incêndio, pânico e desastre;",
        "II - a análise de projetos e vistorias;",
        "III - o exercício do Poder de Polícia Administrativa;",
        "IV - a investigação de incêndio e explosão; e",
        "V - a pesquisa e desenvolvimento em segurança contra incêndio, pânico e desastre."
      ],
      "desdobramentos": [],
      "cargos": [{"cargo": "Diretor de Segurança Contra Incêndio", "subordinadoA": "Chefe do EMG", "requisito": "Coronel QOBM (Art. 9º §2º)", "desdobramentos": [], "atribuicoes": ["I a V – responsabilidades previstas no Art. 38 do Dec. nº 1.328/2021."]}]
    },
    "1rbm": {
      "name": "1ª Região Bombeiro Militar", "abbreviation": "1ª RBM", "category": "Direção Operacional",
      "subordinadoA": "Subcomandante-Geral", "legalRef": "Art. 10, I; Art. 39 Dec. 1.328/2021",
      "baseLegal": "Lei Complementar nº 724, de 18 de julho de 2018",
      "artigosDeOrigem": ["Art. 10, I (composição)", "Art. 39 (Atribuições dos Comandos Regionais)"],
      "atribuicoes": [
        "I - inspecionar periodicamente as Organizações Bombeiro Militar subordinadas;",
        "II - coordenar, controlar, fiscalizar e apoiar as ações operacionais que ultrapassem a circunscrição ou a esfera de competência do comando da unidade operacional subordinada;",
        "III - supervisionar a gestão de convênios, fundos municipais e instrumentos congêneres no âmbito da circunscrição;",
        "IV - orientar e acompanhar o desempenho administrativo e operacional dos elementos subordinados por meio de ações de comando e de ferramentas sistêmicas, visando o aprimoramento de resultados, em consonância com o Plano Estratégico do CBMSC;",
        "V - fiscalizar, na circunscrição da RBM, a gestão das Centrais de Emergências e congêneres;",
        "VI - emitir ordens administrativas e operacionais visando regular as ações de coordenação, controle e fiscalização sobre os órgãos de execução de sua circunscrição;",
        "VII - instaurar inquéritos, sindicâncias e outros procedimentos administrativos pertinentes à manutenção da disciplina no âmbito dos Comandos Regionais;",
        "VIII - definir o emprego de Força-Tarefa, de acordo com as diretrizes do Comando-Geral do CBMSC, no âmbito de sua respectiva circunscrição; e",
        "IX - autorizar deslocamentos dos seus subordinados a serviço e dentro do território estadual."
      ],
      "desdobramentos": ["1º BBM - Florianópolis", "3º BBM - Blumenau", "4º BBM - Criciúma", "7º BBM - Itajaí", "8º BBM - Tubarão", "10º BBM - São José", "13º BBM - Balneário Camboriú"],
      "cargos": [{"cargo": "Comandante da 1ª RBM", "subordinadoA": "Subcomandante-Geral", "requisito": "Oficial do último posto do QOBM (Coronel), nos termos do Art. 11 Dec. nº 1.328/2021", "desdobramentos": [], "atribuicoes": ["I a IX – atribuições previstas no Art. 39 do Dec. nº 1.328/2021."]}]
    },
    "2rbm": {
      "name": "2ª Região Bombeiro Militar", "abbreviation": "2ª RBM", "category": "Direção Operacional",
      "subordinadoA": "Subcomandante-Geral", "legalRef": "Art. 10, II; Art. 39 Dec. 1.328/2021",
      "baseLegal": "Lei Complementar nº 724, de 18 de julho de 2018",
      "artigosDeOrigem": ["Art. 10, II (composição)", "Art. 39 (Atribuições dos Comandos Regionais)"],
      "atribuicoes": [
        "I - inspecionar periodicamente as Organizações Bombeiro Militar subordinadas;",
        "II - coordenar, controlar, fiscalizar e apoiar as ações operacionais que ultrapassem a circunscrição ou a esfera de competência do comando da unidade operacional subordinada;",
        "III - supervisionar a gestão de convênios, fundos municipais e instrumentos congêneres no âmbito da circunscrição;",
        "IV - orientar e acompanhar o desempenho administrativo e operacional dos elementos subordinados por meio de ações de comando e de ferramentas sistêmicas, visando o aprimoramento de resultados, em consonância com o Plano Estratégico do CBMSC;",
        "V - fiscalizar, na circunscrição da RBM, a gestão das Centrais de Emergências e congêneres;",
        "VI - emitir ordens administrativas e operacionais visando regular as ações de coordenação, controle e fiscalização sobre os órgãos de execução de sua circunscrição;",
        "VII - instaurar inquéritos, sindicâncias e outros procedimentos administrativos pertinentes à manutenção da disciplina no âmbito dos Comandos Regionais;",
        "VIII - definir o emprego de Força-Tarefa, de acordo com as diretrizes do Comando-Geral do CBMSC, no âmbito de sua respectiva circunscrição; e",
        "IX - autorizar deslocamentos dos seus subordinados a serviço e dentro do território estadual."
      ],
      "desdobramentos": ["2º BBM - Curitibanos", "5º BBM - Lages", "9º BBM - Canoinhas", "15º BBM - Rio do Sul"],
      "cargos": [{"cargo": "Comandante da 2ª RBM", "subordinadoA": "Subcomandante-Geral", "requisito": "Oficial do último posto do QOBM (Coronel), nos termos do Art. 11 Dec. nº 1.328/2021", "desdobramentos": [], "atribuicoes": ["I a IX – atribuições previstas no Art. 39 do Dec. nº 1.328/2021."]}]
    },
    "3rbm": {
      "name": "3ª Região Bombeiro Militar", "abbreviation": "3ª RBM", "category": "Direção Operacional",
      "subordinadoA": "Subcomandante-Geral", "legalRef": "Art. 10, III; Art. 39 Dec. 1.328/2021",
      "baseLegal": "Lei Complementar nº 724, de 18 de julho de 2018",
      "artigosDeOrigem": ["Art. 10, III (composição)", "Art. 39 (Atribuições dos Comandos Regionais)"],
      "atribuicoes": [
        "I - inspecionar periodicamente as Organizações Bombeiro Militar subordinadas;",
        "II - coordenar, controlar, fiscalizar e apoiar as ações operacionais que ultrapassem a circunscrição ou a esfera de competência do comando da unidade operacional subordinada;",
        "III - supervisionar a gestão de convênios, fundos municipais e instrumentos congêneres no âmbito da circunscrição;",
        "IV - orientar e acompanhar o desempenho administrativo e operacional dos elementos subordinados por meio de ações de comando e de ferramentas sistêmicas, visando o aprimoramento de resultados, em consonância com o Plano Estratégico do CBMSC;",
        "V - fiscalizar, na circunscrição da RBM, a gestão das Centrais de Emergências e congêneres;",
        "VI - emitir ordens administrativas e operacionais visando regular as ações de coordenação, controle e fiscalização sobre os órgãos de execução de sua circunscrição;",
        "VII - instaurar inquéritos, sindicâncias e outros procedimentos administrativos pertinentes à manutenção da disciplina no âmbito dos Comandos Regionais;",
        "VIII - definir o emprego de Força-Tarefa, de acordo com as diretrizes do Comando-Geral do CBMSC, no âmbito de sua respectiva circunscrição; e",
        "IX - autorizar deslocamentos dos seus subordinados a serviço e dentro do território estadual."
      ],
      "desdobramentos": ["6º BBM - Chapecó", "11º BBM - Joaçaba", "12º BBM - São Miguel do Oeste", "14º BBM - Xanxerê"],
      "cargos": [{"cargo": "Comandante da 3ª RBM", "subordinadoA": "Subcomandante-Geral", "requisito": "Oficial do último posto do QOBM (Coronel), nos termos do Art. 11 Dec. nº 1.328/2021", "desdobramentos": [], "atribuicoes": ["I a IX – atribuições previstas no Art. 39 do Dec. nº 1.328/2021."]}]
    },
    "cebm": {
      "name": "Centro de Ensino Bombeiro Militar", "abbreviation": "CEBM", "category": "Apoio",
      "subordinadoA": "Subcomandante-Geral (mobilização); DIE (técnico-administrativamente)", "legalRef": "Art. 12, I; Art. 40 Dec. 1.328/2021",
      "baseLegal": "Lei Complementar nº 724, de 18 de julho de 2018",
      "artigosDeOrigem": ["Art. 40 (Atribuições do CEBM)"],
      "atribuicoes": [
        "I - orientar, coordenar e executar as atividades de Ensino Básico do CBMSC;",
        "II - atender, no que lhe couber, a formação de Ensino Complementar do CBMSC, incluindo a capacitação do corpo docente;",
        "III - baixar normas técnicas relativas às atividades de sua competência e controlar sua aplicação;",
        "IV - estabelecer e manter, por intermédio da Diretoria de Ensino e Instrução, o intercâmbio técnico-científico com as Academias Militares, Universidades e Escolas de Governo;",
        "V - propor ao Estado-Maior Geral, através da Diretoria de Instrução e Ensino, medidas que visem aprimorar as diretrizes gerais e aperfeiçoar a legislação e a política de instrução e ensino;",
        "VI - ofertar, no âmbito da Escola de Governo, cursos com currículos aprovados pela Diretoria de Ensino e Instrução que visem o aprimoramento profissional dos militares estaduais, bem como para servidores públicos e profissionais que se relacionam com as atividades de bombeiro;",
        "VII - promover as atividades de ensino, pesquisa e extensão no âmbito da Corporação e em parceria com outras instituições em conformidade com a legislação em vigor;",
        "VIII - atender às exigências emanadas pelo Conselho Estadual de Educação no que tange à Escola de Governo;",
        "IX - promover e incentivar as pesquisas técnico-científicas nas áreas de conhecimento presentes no Plano de Desenvolvimento Institucional da Escola de Governo; e",
        "X - apoiar o Comando-Geral da Corporação na condição de reserva tática de pronto emprego operacional."
      ],
      "desdobramentos": ["Academia de Bombeiro Militar (1ª Companhia)", "Centro de Formação e Aperfeiçoamento de Praças (2ª Companhia)", "Centro de Estudos Superiores (3ª Companhia)", "Centro de Formação de Corpo Temporário (4ª Companhia)", "Centros Descentralizados de Formação Especializada"],
      "cargos": [{"cargo": "Comandante do CEBM", "subordinadoA": "Subcomandante-Geral", "requisito": "Coronel QOBM (Art. 12 §8º)", "desdobramentos": [], "atribuicoes": ["I a X – atribuições previstas no Art. 40 do Dec. nº 1.328/2021."]}]
    },
    "aci-sc": {
      "name": "Agência Central de Inteligência", "abbreviation": "ACI", "category": "Apoio",
      "subordinadoA": "Gabinete do Comando-Geral", "legalRef": "Art. 12, III; Art. 42 Dec. 1.328/2021",
      "baseLegal": "Lei Complementar nº 724, de 18 de julho de 2018",
      "artigosDeOrigem": ["Art. 42 (Atribuições da Agência Central de Inteligência)"],
      "atribuicoes": [
        "I - supervisionar e coordenar, em todo o território do Estado, a atividade de inteligência;",
        "II - definir bases para o estabelecimento da doutrina da atividade de inteligência;",
        "III - elaborar os planos de inteligência e de busca;",
        "IV - produzir conhecimentos necessários às decisões do Comandante-Geral, bem como aos estudos e planejamentos em nível de Estado-Maior Geral;",
        "V - promover e coordenar o intercâmbio de informações entre as Agências Setoriais de Inteligência do CBMSC;",
        "VI - estabelecer o relacionamento e ligações com os órgãos federais e estaduais de inteligência, assegurando o intercâmbio de conhecimentos;",
        "VII - coordenar operações de inteligência em todo território do Estado;",
        "VIII - promover a formação de uma correta mentalidade de inteligência;",
        "IX - organizar e manter em dia os arquivos sigilosos, bem como controlar o fluxo de documentos sigilosos do CBMSC;",
        "X - elaborar e controlar a expedição dos boletins reservados do Comando-Geral; e",
        "XI - outras atribuições correlatas ou que vierem a ser cometidas à Agência Central de Inteligência."
      ],
      "desdobramentos": [],
      "cargos": [{"cargo": "Chefe da Agência Central de Inteligência", "subordinadoA": "Gabinete do Comando-Geral", "requisito": "Oficial intermediário ou superior do QOBM (Art. 12 §7º)", "desdobramentos": [], "atribuicoes": ["I a XI – atribuições previstas no Art. 42 do Dec. nº 1.328/2021."]}]
    },
    "aeis": {
      "name": "Assessoria Especial de Integração de Serviços Auxiliares", "abbreviation": "AEISA", "category": "Apoio",
      "subordinadoA": "Subcomandante-Geral", "legalRef": "Art. 12, IV, a; Art. 44 Dec. 1.328/2021",
      "baseLegal": "Lei Complementar nº 724, de 18 de julho de 2018",
      "artigosDeOrigem": ["Art. 44 (Atribuições da Assessoria Especial de Integração de Serviços Auxiliares)"],
      "atribuicoes": [
        "I - articular a integração dos órgãos de direção setorial, apoio e execução, necessária para a formação, aperfeiçoamento e atuação dos integrantes dos serviços auxiliares do CBMSC;",
        "II - planejar, monitorar, controlar e avaliar todos os processos de formação e treinamento dos integrantes dos serviços auxiliares do CBMSC;",
        "III - monitorar o controle realizado pelos órgãos de execução, de todas as atividades relacionadas com o exercício do serviço voluntário na Corporação;",
        "IV - planejar e controlar, de forma integrada com demais órgãos, o emprego operacional e concessão de benefícios aos integrantes dos serviços auxiliares do CBMSC;",
        "V - planejar, monitorar, controlar e avaliar todos os processos desenvolvidos pelos demais órgãos relacionados com os programas comunitários;",
        "VI - auxiliar os órgãos de execução na implementação dos programas, projetos e ações comunitárias;",
        "VII - manter biblioteca atualizada com normas e regulamentos referentes aos programas comunitários;",
        "VIII - manter acessível toda documentação padronizada referente à implementação dos programas comunitários;",
        "IX - controlar a aplicação das normas e regulamentos afetos aos serviços auxiliares e programas comunitários;",
        "X - gerenciar processos para aprovação de editais e planos de ensino dos programas de sua responsabilidade, bem como os processos de registro e emissão de certificados das atividades de capacitação;",
        "XI - fazer levantamentos de necessidade de formação do efetivo para gestão e execução das atividades relacionadas aos programas comunitários, mantendo atualizada a relação dos gestores dos programas comunitários;",
        "XII - analisar as propostas de projetos institucionais, emitindo parecer para Coordenadoria de Programas Comunitários para análise final;",
        "XIII - coletar e consolidar dados para fins estatísticos;",
        "XIV - fiscalizar as atividades desenvolvidas pelas OBM na execução dos programas comunitários, por meio de inspeções técnico-administrativas;",
        "XV - identificar necessidade de alteração e/ou ajuste de programas, projetos e ações, de modo a promover o alinhamento com os objetivos estratégicos da Corporação;",
        "XVI - acompanhar os indicadores de desempenho das atividades relacionadas aos programas comunitários;",
        "XVII - divulgar os resultados operacionais e impactos sociais das atividades relacionadas aos programas comunitários;",
        "XVIII - estabelecer a integração com os demais órgãos públicos, no trato das atividades relacionadas com a área de competência;",
        "XIX - manter atualizado e divulgado o portfólio de programas comunitários da Corporação; e",
        "XX - outras definidas por ATO do Comandante-Geral."
      ],
      "desdobramentos": [],
      "cargos": [{"cargo": "Chefe da AEISA", "subordinadoA": "Subcomandante-Geral", "requisito": "Oficial QOBM (Art. 12 §4º)", "desdobramentos": [], "atribuicoes": ["I a XX – atribuições previstas no Art. 44 do Dec. nº 1.328/2021."]}]
    },
    "aeai": {
      "name": "Assessoria Especial de Assuntos Institucionais", "abbreviation": "AEAI", "category": "Apoio",
      "subordinadoA": "Gabinete do Comandante-Geral", "legalRef": "Art. 12, IV, b; Art. 45 Dec. 1.328/2021",
      "baseLegal": "Lei Complementar nº 724, de 18 de julho de 2018",
      "artigosDeOrigem": ["Art. 45 (Assessoria Especial de Assuntos Institucionais)"],
      "atribuicoes": [
        "A Assessoria Especial de Assuntos Institucionais é órgão de apoio, prestando assessoria técnica, coordenação, controle e acompanhamento dos assuntos institucionais em nível federal, estadual e municipal que sejam de interesse do Comando-Geral do CBMSC, cabendo a este editar ATO que discipline as atividades, as atribuições e a organização (Art. 45).",
        "Parágrafo único. A Assessoria Especial de Assuntos Institucionais poderá exercer atividades na capital federal atuando na articulação junto aos ministérios para captação de recursos e acompanhamento de matérias que sejam de interesse da Corporação."
      ],
      "desdobramentos": [],
      "cargos": [{"cargo": "Chefe da AEAI", "subordinadoA": "Gabinete do Comandante-Geral", "requisito": "Oficial QOBM (Art. 12 §5º)", "desdobramentos": [], "atribuicoes": ["Atribuições disciplinadas por ATO do Comandante-Geral (Art. 45)."]}]
    },
    "aei-sc": {
      "name": "Assessoria Especial de Inovação", "abbreviation": "AEI", "category": "Apoio",
      "subordinadoA": "Gabinete do Comandante-Geral", "legalRef": "Art. 12, IV, c; Art. 46 Dec. 1.328/2021",
      "baseLegal": "Lei Complementar nº 724, de 18 de julho de 2018",
      "artigosDeOrigem": ["Art. 46 (Assessoria Especial de Inovação)"],
      "atribuicoes": [
        "A Assessoria Especial de Inovação do CBMSC tem como finalidade a pesquisa de novas tecnologias, novos procedimentos e equipamentos que possam trazer melhorias nas atividades da Corporação no Estado (Art. 46)."
      ],
      "desdobramentos": [],
      "cargos": [{"cargo": "Chefe da AEI", "subordinadoA": "Gabinete do Comandante-Geral", "requisito": "Oficial QOBM (Art. 12 §6º)", "desdobramentos": [], "atribuicoes": ["Pesquisa de novas tecnologias, procedimentos e equipamentos para as atividades da Corporação (Art. 46)."]}]
    },
    "bbm-sc": {
      "name": "Batalhões Bombeiro Militar", "abbreviation": "BBM", "category": "Execução",
      "subordinadoA": "Regiões Bombeiro Militar (RBMs)", "legalRef": "Art. 13; Art. 51 Dec. 1.328/2021",
      "baseLegal": "Lei Complementar nº 724, de 18 de julho de 2018",
      "artigosDeOrigem": ["Art. 51 (Atribuições dos BBMs)"],
      "atribuicoes": [
        "I - realizar os serviços de segurança, prevenção, proteção e combate a incêndios;",
        "II - realizar os serviços de busca e salvamento de pessoas e bens, por meio de resgates aéreo, aquático e terrestre;",
        "III - realizar o atendimento pré-hospitalar, respeitadas as competências de outros órgãos;",
        "IV - executar a prevenção balneária por guarda-vidas e a prevenção de acidentes e incêndios na orla marítima e fluvial;",
        "V - analisar previamente os projetos preventivos, acompanhar e fiscalizar sua execução e impor sanções administrativas estabelecidas em LEI em: a) segurança contra incêndio e pânico em imóveis; e b) áreas de risco e de armazenagem, manipulação e transporte de produtos perigosos;",
        "VI - credenciar e fiscalizar o funcionamento dos serviços civis auxiliares de bombeiros;",
        "VII - desenvolver atividades relacionadas à educação pública, com foco na criação de uma cultura preventiva e reativa na comunidade, abrangendo o rol de atendimentos prestados pela Corporação e em conformidade com a política de capacitação do público externo;",
        "VIII - realizar investigação de incêndio e explosão de áreas sinistradas no limite de sua competência;",
        "IX - atuar de forma integrada com os órgãos de defesa civil; e",
        "X - outras atividades regularmente previstas, bem como outras necessárias para a consecução das atividades da Corporação."
      ],
      "desdobramentos": [],
      "cargos": [{"cargo": "Comandante de BBM", "subordinadoA": "Comandante da RBM", "requisito": "Oficial QOBM", "desdobramentos": [], "atribuicoes": ["I a X – atribuições previstas no Art. 51 do Dec. nº 1.328/2021."]}]
    }
  }
},

"se": {
  "legal_source": "Lei nº 8.979, de 03 de fevereiro de 2022",
  "organs": {
    "comando-geral": {
      "name": "Comando-Geral", "abbreviation": "CG", "category": "Direção Estratégica",
      "subordinadoA": "Governador do Estado", "legalRef": "Art. 5º",
      "baseLegal": "Lei nº 8.979, de 03 de fevereiro de 2022",
      "artigosDeOrigem": ["Art. 5º (Comando-Geral)", "Art. 7º (Atribuições do Comandante-Geral)"],
      "atribuicoes": [
        "I - exercer a representação política e institucional do CBMSE, promovendo contatos e relações com autoridades e organizações de diferentes níveis governamentais;",
        "II - promover a administração geral do CBMSE, em estrita observância às disposições normativas da Administração Pública Estadual;",
        "III - aprovar o Regimento Interno do CBMSE, submetendo-o à homologação por decreto do Governador do Estado;",
        "IV - assessorar o Governador do Estado e o Secretário de Estado da Segurança Pública nos assuntos de competência do CBMSE;",
        "V - fazer cumprir as leis, normas e regulamentos da Corporação;",
        "VI - proferir despachos finais em processos administrativos e operacionais que envolvam o efetivo sob seu comando;",
        "VII - autorizar a abertura de processos licitatórios, homologando-os dentro dos limites de sua competência, e ratificar as dispensas ou declarações de inexigibilidade referentes às contratações diretas, nos termos da legislação específica;",
        "VIII - aprovar a programação orçamentário-financeira a ser executada pelo CBMSE e pelos órgãos a ele subordinados, a proposta orçamentária anual e as alterações e ajustes que se fizerem necessários;",
        "IX - expedir portarias, instruções normativas, ordens de serviço, diretrizes e planos que promovam a eficácia da gestão administrativa e operacional da instituição, em consonância com a legislação em vigor;",
        "X - instaurar procedimentos de polícia judiciária militar e de polícia administrativa, bem como aplicar as sanções previstas na legislação em vigor;",
        "XI - autorizar despesas nos limites de sua competência;",
        "XII - delegar atribuições de sua competência que não sejam vedadas por lei;",
        "XIII - aprovar os planos, estudos, programas, projetos e propostas para organização funcional e de atuação do CBMSE;",
        "XIV - exercer a função de presidente do Alto-Comando do CBMSE;",
        "XV - promover o controle e a supervisão dos órgãos subordinados;",
        "XVI - presidir a Comissão de Promoção de Oficiais (CPO) e os respectivos processos e encaminhá-los para o Governador do Estado, a quem compete o ato da promoção;",
        "XVII - atribuir outras atividades aos integrantes da corporação, além daquelas estabelecidas em leis ou regulamentos;",
        "XVIII - coordenar e executar ações de defesa civil no âmbito de suas competências;",
        "XIX - designar ocupantes dos órgãos integrantes da estrutura organizacional, ressalvada a competência do Governador do Estado;",
        "XX - desempenhar outras atribuições que lhe forem delegadas pelo Governador do Estado ou pelo Secretário de Estado da Segurança Pública ou ainda por aquelas previstas em lei."
      ],
      "desdobramentos": ["Comandante-Geral", "Subcomandante-Geral (acumula Chefe do EMG)", "Estado-Maior-Geral", "Gabinete", "Corregedoria-Geral", "Controladoria Interna", "Ouvidoria-Geral", "Assessorias", "Comissões Técnicas"],
      "cargos": [{"cargo": "Comandante-Geral", "subordinadoA": "Governador do Estado", "requisito": "Coronel QOBM com Cursos de Formação de Oficiais, Aperfeiçoamento de Oficiais e Superior de Bombeiro Militar (CSBM), ou equivalentes reconhecidos legalmente (Art. 6º)", "desdobramentos": [], "atribuicoes": [
        "I - exercer a representação política e institucional do CBMSE;",
        "II - promover a administração geral do CBMSE;",
        "III - aprovar o Regimento Interno do CBMSE;",
        "IV - assessorar o Governador do Estado e o Secretário de Estado da Segurança Pública;",
        "V - fazer cumprir as leis, normas e regulamentos da Corporação;",
        "VI–XX - demais atribuições previstas no Art. 7º da Lei nº 8.979/2022."
      ]}]
    },
    "subcomandante-geral": {
      "name": "Subcomandante-Geral", "abbreviation": "SCG", "category": "Direção Estratégica",
      "subordinadoA": "Comandante-Geral", "legalRef": "Art. 8º, 9º",
      "baseLegal": "Lei nº 8.979, de 03 de fevereiro de 2022",
      "artigosDeOrigem": ["Art. 8º (Subcomandante-Geral)", "Art. 9º (Atribuições)"],
      "atribuicoes": [
        "I - exercer a função de Presidente da Comissão de Promoção de Praças (CPP);",
        "II - substituir o Comandante-Geral em seus impedimentos;",
        "III - fiscalizar a conduta civil e militar dos oficiais e praças do Corpo de Bombeiros Militar, respeitados os princípios da disciplina, hierarquia e ética do bombeiro militar;",
        "IV - instaurar procedimentos investigatórios e processos administrativos disciplinares, bem como aplicar sanções disciplinares previstas na legislação em vigor a todos os que lhe estiverem subordinados;",
        "V - promover e coordenar estudos estratégicos e sistêmicos sobre assuntos de ordem técnica, pertinentes à instituição;",
        "VI - exercer outras atribuições que lhe forem delegadas pelo Comandante-Geral."
      ],
      "desdobramentos": ["Acumula função de Chefe do Estado-Maior-Geral (Art. 8º §3º)"],
      "cargos": [{"cargo": "Subcomandante-Geral", "subordinadoA": "Comandante-Geral", "requisito": "Coronel QOBM com Cursos de Formação de Oficiais, Aperfeiçoamento de Oficiais e Superior de Bombeiro Militar (CSBM), ou equivalentes, indicado pelo Comandante-Geral e nomeado pelo Governador do Estado (Art. 8º)", "desdobramentos": [], "atribuicoes": [
        "I - exercer a função de Presidente da Comissão de Promoção de Praças (CPP);",
        "II - substituir o Comandante-Geral em seus impedimentos;",
        "III - fiscalizar a conduta civil e militar dos oficiais e praças do Corpo de Bombeiros Militar;",
        "IV - instaurar procedimentos investigatórios e processos administrativos disciplinares;",
        "V - promover e coordenar estudos estratégicos e sistêmicos;",
        "VI - exercer outras atribuições delegadas pelo Comandante-Geral. (Art. 9º I–VI)"
      ]}]
    },
    "emg-se": {
      "name": "Estado-Maior-Geral", "abbreviation": "EMG", "category": "Direção Estratégica",
      "subordinadoA": "Comandante-Geral", "legalRef": "Art. 10",
      "baseLegal": "Lei nº 8.979, de 03 de fevereiro de 2022",
      "artigosDeOrigem": ["Art. 10 (Estado-Maior-Geral)"],
      "atribuicoes": ["O Estado-Maior-Geral é o órgão de direção estratégica, responsável perante o Comandante-Geral, pelo planejamento, orientação, coordenação, fiscalização e execução das atividades relacionadas à gestão administrativa, visando à eficácia da instituição no cumprimento de suas atribuições (Art. 10)"],
      "desdobramentos": ["Chefe do Estado-Maior-Geral (acumulado pelo Subcomandante-Geral)", "Corregedor-Geral", "Titulares de Diretorias"],
      "cargos": [{"cargo": "Chefe do Estado-Maior-Geral", "subordinadoA": "Comandante-Geral", "requisito": "Subcomandante-Geral (acumulação obrigatória, Art. 8º §3º)", "desdobramentos": [], "atribuicoes": ["Chefia do Estado-Maior-Geral, acumulada com a função de Subcomandante-Geral (Art. 8º §3º)"]}]
    },
    "gabinete-se": {
      "name": "Gabinete do Comandante-Geral", "abbreviation": "Gab", "category": "Assessoramento",
      "subordinadoA": "Comandante-Geral", "legalRef": "Art. 11, 12",
      "baseLegal": "Lei nº 8.979, de 03 de fevereiro de 2022",
      "artigosDeOrigem": ["Art. 11 (Gabinete)", "Art. 12 (Chefia de Gabinete)"],
      "atribuicoes": ["O Gabinete do Comandante-Geral compete o assessoramento direto ao Comandante-Geral (Art. 11)"],
      "desdobramentos": ["Chefia de Gabinete", "Ajudância de Ordens", "Ajudância-Geral"],
      "cargos": [{"cargo": "Chefe de Gabinete", "subordinadoA": "Comandante-Geral", "requisito": "Oficial Superior QOBM (Art. 12 parágrafo único)", "desdobramentos": [], "atribuicoes": ["À Chefia de Gabinete compete o exercício das funções de assistência e assessoramento direto ao Comandante-Geral e ao Subcomandante-Geral, inerentes ao controle, coordenação e fiscalização das atividades administrativas desenvolvidas por militares e civis no âmbito dos Gabinetes do Comandante-Geral e do Subcomandante-Geral, da Ajudância de Ordens (Art. 12)"]}]
    },
    "ajudancia-geral-se": {
      "name": "Ajudância-Geral", "abbreviation": "AjG", "category": "Assessoramento",
      "subordinadoA": "Comandante-Geral", "legalRef": "Art. 14",
      "baseLegal": "Lei nº 8.979, de 03 de fevereiro de 2022",
      "artigosDeOrigem": ["Art. 14 (Ajudância-Geral)"],
      "atribuicoes": ["À Ajudância-Geral compete a administração do Quartel do Comando-Geral, considerado como Organização Bombeiro Militar, bem como do expediente, da execução dos trabalhos de secretaria, incluindo a correspondência, correio, redação do boletim diário, do protocolo e arquivo geral e biblioteca, do apoio em pessoal aos órgãos que compõem o Comando-Geral, dos serviços gerais, do Centro de Memória e da segurança do Quartel do Comando-Geral (Art. 14)"],
      "desdobramentos": [],
      "cargos": [{"cargo": "Chefe da Ajudância-Geral", "subordinadoA": "Comandante-Geral", "requisito": "Oficial Superior QOBM (Art. 14 parágrafo único)", "desdobramentos": [], "atribuicoes": ["Chefia da Ajudância-Geral (Art. 14)"]}]
    },
    "corregedoria-geral-se": {
      "name": "Corregedoria-Geral", "abbreviation": "Corr-G", "category": "Disciplina",
      "subordinadoA": "Comandante-Geral", "legalRef": "Art. 15",
      "baseLegal": "Lei nº 8.979, de 03 de fevereiro de 2022",
      "artigosDeOrigem": ["Art. 15 (Corregedoria-Geral)"],
      "atribuicoes": ["A Corregedoria-Geral do Corpo de Bombeiros Militar é o órgão responsável pela sistematização e controle das atividades de correição funcional, de caráter disciplinar, administrativo ou de polícia judiciária militar (Art. 15)"],
      "desdobramentos": [],
      "cargos": [{"cargo": "Corregedor-Geral", "subordinadoA": "Comandante-Geral", "requisito": "Coronel QOBM (função privativa, Art. 15 parágrafo único)", "desdobramentos": [], "atribuicoes": ["Chefia da Corregedoria-Geral, com função privativa de Oficial do posto de Coronel do QOBM (Art. 15 parágrafo único)"]}]
    },
    "controladoria-interna-se": {
      "name": "Controladoria Interna", "abbreviation": "CI", "category": "Assessoramento",
      "subordinadoA": "Comandante-Geral", "legalRef": "Art. 16",
      "baseLegal": "Lei nº 8.979, de 03 de fevereiro de 2022",
      "artigosDeOrigem": ["Art. 16 (Controladoria Interna)"],
      "atribuicoes": ["A Controladoria Interna é o órgão de assessoramento e consultoria que tem como finalidade a efetivação do controle financeiro, contábil, orçamentário, patrimonial e operacional da instituição, com foco na gestão das políticas públicas (Art. 16)"],
      "desdobramentos": [],
      "cargos": [{"cargo": "Chefe da Controladoria Interna", "subordinadoA": "Comandante-Geral", "requisito": "Oficial Superior da ativa pertencente ao QOBM (Art. 16 §2º)", "desdobramentos": [], "atribuicoes": ["Chefia da Controladoria Interna (Art. 16)"]}]
    },
    "ouvidoria-geral-se": {
      "name": "Ouvidoria-Geral", "abbreviation": "Ouv-G", "category": "Transparência",
      "subordinadoA": "Comandante-Geral", "legalRef": "Art. 17",
      "baseLegal": "Lei nº 8.979, de 03 de fevereiro de 2022",
      "artigosDeOrigem": ["Art. 17 (Ouvidoria-Geral)"],
      "atribuicoes": ["A Ouvidoria-Geral é o órgão que tem como finalidade prestar informações e dar transparência às ações e atividades executadas pela instituição, competindo-lhe planejar, controlar e executar as atividades relacionadas ao Sistema Administrativo de Ouvidoria do Estado, sem prejuízo de outras atribuições previstas em lei (Art. 17)"],
      "desdobramentos": [],
      "cargos": [{"cargo": "Chefe da Ouvidoria-Geral", "subordinadoA": "Comandante-Geral", "requisito": "Oficial Superior pertencente ao QOBM (Art. 17 §2º)", "desdobramentos": [], "atribuicoes": ["Chefia da Ouvidoria-Geral (Art. 17)"]}]
    },
    "dlog-se": {
      "name": "Diretoria de Logística", "abbreviation": "DLOG", "category": "Direção Geral",
      "subordinadoA": "Subcomandante-Geral", "legalRef": "Art. 22, 23",
      "baseLegal": "Lei nº 8.979, de 03 de fevereiro de 2022",
      "artigosDeOrigem": ["Art. 22 (Órgãos de Direção-Geral)", "Art. 23 (DLOG)"],
      "atribuicoes": ["A Diretoria de Logística — DLOG é responsável pela gestão, planejamento, coordenação, execução, fiscalização e controle das atividades relacionadas à logística e patrimônio do CBMSE (Art. 23)"],
      "desdobramentos": [],
      "cargos": [{"cargo": "Diretor de Logística", "subordinadoA": "Subcomandante-Geral", "requisito": "Oficial da ativa do último posto do QOBM (Art. 22 §2º)", "desdobramentos": [], "atribuicoes": ["Direção da DLOG (Art. 23)"]}]
    },
    "dfin-se": {
      "name": "Diretoria de Finanças", "abbreviation": "DFIN", "category": "Direção Geral",
      "subordinadoA": "Subcomandante-Geral", "legalRef": "Art. 24",
      "baseLegal": "Lei nº 8.979, de 03 de fevereiro de 2022",
      "artigosDeOrigem": ["Art. 24 (DFIN)"],
      "atribuicoes": ["A Diretoria Financeira — DFIN é responsável pela gestão, planejamento, coordenação, execução, fiscalização e controle das atividades do sistema de administração financeira e contábil do CBMSE (Art. 24)"],
      "desdobramentos": [],
      "cargos": [{"cargo": "Diretor de Finanças", "subordinadoA": "Subcomandante-Geral", "requisito": "Oficial da ativa do último posto do QOBM (Art. 22 §2º)", "desdobramentos": [], "atribuicoes": ["Direção da DFIN (Art. 24)"]}]
    },
    "dgp-se": {
      "name": "Diretoria de Gestão de Pessoal", "abbreviation": "DGP", "category": "Direção Geral",
      "subordinadoA": "Subcomandante-Geral", "legalRef": "Art. 25",
      "baseLegal": "Lei nº 8.979, de 03 de fevereiro de 2022",
      "artigosDeOrigem": ["Art. 25 (DGP)"],
      "atribuicoes": ["A Diretoria de Gestão de Pessoal — DGP é responsável pela gestão, planejamento, coordenação, execução, fiscalização e controle das atividades relativas à gestão de pessoal e desenvolvimento de recursos humanos do CBMSE (Art. 25)"],
      "desdobramentos": [],
      "cargos": [{"cargo": "Diretor de Gestão de Pessoal", "subordinadoA": "Subcomandante-Geral", "requisito": "Oficial da ativa do último posto do QOBM (Art. 22 §2º)", "desdobramentos": [], "atribuicoes": ["Direção da DGP (Art. 25)"]}]
    },
    "dep-se": {
      "name": "Diretoria de Ensino e Pesquisa", "abbreviation": "DEP", "category": "Direção Geral",
      "subordinadoA": "Subcomandante-Geral", "legalRef": "Art. 26",
      "baseLegal": "Lei nº 8.979, de 03 de fevereiro de 2022",
      "artigosDeOrigem": ["Art. 26 (DEP)"],
      "atribuicoes": ["A Diretoria de Ensino e Pesquisa — DEP é responsável pela gestão, planejamento, coordenação, execução, fiscalização e controle das atividades referentes ao ensino, fomentando a pesquisa e viabilizando a instrução continuada dos quadros no âmbito do CBMSE (Art. 26)"],
      "desdobramentos": [],
      "cargos": [{"cargo": "Diretor de Ensino e Pesquisa", "subordinadoA": "Subcomandante-Geral", "requisito": "Oficial da ativa do último posto do QOBM (Art. 22 §2º)", "desdobramentos": [], "atribuicoes": ["Direção da DEP (Art. 26)"]}]
    },
    "dplan-se": {
      "name": "Diretoria de Planejamento", "abbreviation": "DPLAN", "category": "Direção Geral",
      "subordinadoA": "Subcomandante-Geral", "legalRef": "Art. 27",
      "baseLegal": "Lei nº 8.979, de 03 de fevereiro de 2022",
      "artigosDeOrigem": ["Art. 27 (DPLAN)"],
      "atribuicoes": ["A Diretoria de Planejamento — DPLAN é responsável pela gestão, planejamento das políticas públicas e estratégias institucionais, orientação e execução da programação orçamentária, consolidação dos planos, programas e projetos e acompanhamento e avaliação das ações governamentais, no âmbito do CBMSE (Art. 27)"],
      "desdobramentos": [],
      "cargos": [{"cargo": "Diretor de Planejamento", "subordinadoA": "Subcomandante-Geral", "requisito": "Oficial da ativa do último posto do QOBM (Art. 22 §2º)", "desdobramentos": [], "atribuicoes": ["Direção da DPLAN (Art. 27)"]}]
    },
    "dat-se": {
      "name": "Diretoria de Atividades Técnicas", "abbreviation": "DAT", "category": "Direção Operacional",
      "subordinadoA": "Comandante-Geral", "legalRef": "Art. 28, 29",
      "baseLegal": "Lei nº 8.979, de 03 de fevereiro de 2022",
      "artigosDeOrigem": ["Art. 28 (Órgãos de Direção Operacional)", "Art. 29 (DAT)"],
      "atribuicoes": ["A Diretoria de Atividades Técnicas — DAT é responsável pela gestão, planejamento, coordenação, execução, fiscalização e controle de todas as atividades concernentes à segurança contra incêndio e pânico das instalações, edificações e locais de risco, no âmbito do Estado de Sergipe (Art. 29)"],
      "desdobramentos": [],
      "cargos": [{"cargo": "Diretor de Atividades Técnicas", "subordinadoA": "Comandante-Geral", "requisito": "Oficial da ativa do último posto do QOBM (Art. 28 caput)", "desdobramentos": [], "atribuicoes": ["Direção da DAT (Art. 29)"]}]
    },
    "dop-se": {
      "name": "Diretoria Operacional", "abbreviation": "DOP", "category": "Direção Operacional",
      "subordinadoA": "Comandante-Geral", "legalRef": "Art. 30",
      "baseLegal": "Lei nº 8.979, de 03 de fevereiro de 2022",
      "artigosDeOrigem": ["Art. 30 (DOP)"],
      "atribuicoes": ["A Diretoria Operacional — DOP é responsável pela gestão, planejamento, coordenação, execução, fiscalização e controle das atividades operacionais e na execução das atividades de proteção e defesa civil, sendo responsável pela coordenação e emprego dos Comandos Regionais e Unidades Operacionais, que lhes são subordinadas (Art. 30)"],
      "desdobramentos": ["Comandos Regionais Bombeiro Militar (CRBM)", "Grupamentos Bombeiro Militar (GBM)", "Grupamentos Especializados (GBS, GOA)"],
      "cargos": [{"cargo": "Diretor Operacional", "subordinadoA": "Comandante-Geral", "requisito": "Oficial da ativa do último posto do QOBM (Art. 28 caput)", "desdobramentos": [], "atribuicoes": ["Direção da DOP, coordenação e emprego dos Comandos Regionais e Unidades Operacionais subordinadas (Art. 30)"]}]
    },
    "crm-se": {
      "name": "Comando Regional Metropolitano", "abbreviation": "CRM", "category": "Execução",
      "subordinadoA": "Diretoria Operacional", "legalRef": "Art. 35, I",
      "baseLegal": "Lei nº 8.979, de 03 de fevereiro de 2022",
      "artigosDeOrigem": ["Art. 35 (Comandos Regionais)", "Art. 35 §2º I"],
      "atribuicoes": ["Os Comandos Regionais Bombeiro Militar — CRBM subordinam-se à DOP e são órgãos de supervisão, coordenação e planejamento operacional das unidades subordinadas (Art. 35)"],
      "desdobramentos": ["1º GBM — Aracaju", "4º GBM — Nossa Senhora do Socorro (CRM/CRL)", "8º GBM — Barra dos Coqueiros"],
      "cargos": [{"cargo": "Chefe do Comando Regional Metropolitano", "subordinadoA": "Diretoria Operacional", "requisito": "Oficial Superior QOBM (Art. 35 §2º); acumula função de Comandante de Grupamento da AISP (Art. 35 §4º)", "desdobramentos": [], "atribuicoes": ["Supervisão, coordenação e planejamento operacional das unidades subordinadas na AISP correspondente (Art. 35)"]}]
    },
    "cras-se": {
      "name": "Comando Regional do Alto Sertão", "abbreviation": "CRAS", "category": "Execução",
      "subordinadoA": "Diretoria Operacional", "legalRef": "Art. 35, II",
      "baseLegal": "Lei nº 8.979, de 03 de fevereiro de 2022",
      "artigosDeOrigem": ["Art. 35 §2º II"],
      "atribuicoes": ["Os Comandos Regionais Bombeiro Militar — CRBM subordinam-se à DOP e são órgãos de supervisão, coordenação e planejamento operacional das unidades subordinadas (Art. 35)"],
      "desdobramentos": ["7º GBM — Nossa Senhora da Glória (CRAS/CRMS)"],
      "cargos": [{"cargo": "Chefe do Comando Regional do Alto Sertão", "subordinadoA": "Diretoria Operacional", "requisito": "Oficial Superior QOBM (Art. 35 §2º)", "desdobramentos": [], "atribuicoes": ["Supervisão, coordenação e planejamento operacional das unidades subordinadas na AISP correspondente (Art. 35)"]}]
    },
    "crms-se": {
      "name": "Comando Regional do Médio Sertão", "abbreviation": "CRMS", "category": "Execução",
      "subordinadoA": "Diretoria Operacional", "legalRef": "Art. 35, III",
      "baseLegal": "Lei nº 8.979, de 03 de fevereiro de 2022",
      "artigosDeOrigem": ["Art. 35 §2º III"],
      "atribuicoes": ["Os Comandos Regionais Bombeiro Militar — CRBM subordinam-se à DOP e são órgãos de supervisão, coordenação e planejamento operacional das unidades subordinadas (Art. 35)"],
      "desdobramentos": ["7º GBM — Nossa Senhora da Glória (CRAS/CRMS)"],
      "cargos": [{"cargo": "Chefe do Comando Regional do Médio Sertão", "subordinadoA": "Diretoria Operacional", "requisito": "Oficial Superior QOBM (Art. 35 §2º)", "desdobramentos": [], "atribuicoes": ["Supervisão, coordenação e planejamento operacional das unidades subordinadas na AISP correspondente (Art. 35)"]}]
    },
    "crcs-se": {
      "name": "Comando Regional do Centro Sul", "abbreviation": "CRCS", "category": "Execução",
      "subordinadoA": "Diretoria Operacional", "legalRef": "Art. 35, IV",
      "baseLegal": "Lei nº 8.979, de 03 de fevereiro de 2022",
      "artigosDeOrigem": ["Art. 35 §2º IV"],
      "atribuicoes": ["Os Comandos Regionais Bombeiro Militar — CRBM subordinam-se à DOP e são órgãos de supervisão, coordenação e planejamento operacional das unidades subordinadas (Art. 35)"],
      "desdobramentos": ["5º GBM — Lagarto"],
      "cargos": [{"cargo": "Chefe do Comando Regional do Centro Sul", "subordinadoA": "Diretoria Operacional", "requisito": "Oficial Superior QOBM (Art. 35 §2º)", "desdobramentos": [], "atribuicoes": ["Supervisão, coordenação e planejamento operacional das unidades subordinadas na AISP correspondente (Art. 35)"]}]
    },
    "crs-se": {
      "name": "Comando Regional do Sul", "abbreviation": "CRS", "category": "Execução",
      "subordinadoA": "Diretoria Operacional", "legalRef": "Art. 35, V",
      "baseLegal": "Lei nº 8.979, de 03 de fevereiro de 2022",
      "artigosDeOrigem": ["Art. 35 §2º V"],
      "atribuicoes": ["Os Comandos Regionais Bombeiro Militar — CRBM subordinam-se à DOP e são órgãos de supervisão, coordenação e planejamento operacional das unidades subordinadas (Art. 35)"],
      "desdobramentos": ["2º GBM — Estância"],
      "cargos": [{"cargo": "Chefe do Comando Regional do Sul", "subordinadoA": "Diretoria Operacional", "requisito": "Oficial Superior QOBM (Art. 35 §2º)", "desdobramentos": [], "atribuicoes": ["Supervisão, coordenação e planejamento operacional das unidades subordinadas na AISP correspondente (Art. 35)"]}]
    },
    "crl-se": {
      "name": "Comando Regional do Leste", "abbreviation": "CRL", "category": "Execução",
      "subordinadoA": "Diretoria Operacional", "legalRef": "Art. 35, VI",
      "baseLegal": "Lei nº 8.979, de 03 de fevereiro de 2022",
      "artigosDeOrigem": ["Art. 35 §2º VI"],
      "atribuicoes": ["Os Comandos Regionais Bombeiro Militar — CRBM subordinam-se à DOP e são órgãos de supervisão, coordenação e planejamento operacional das unidades subordinadas (Art. 35)"],
      "desdobramentos": ["4º GBM — Nossa Senhora do Socorro (CRM/CRL)"],
      "cargos": [{"cargo": "Chefe do Comando Regional do Leste", "subordinadoA": "Diretoria Operacional", "requisito": "Oficial Superior QOBM (Art. 35 §2º)", "desdobramentos": [], "atribuicoes": ["Supervisão, coordenação e planejamento operacional das unidades subordinadas na AISP correspondente (Art. 35)"]}]
    },
    "cra-se": {
      "name": "Comando Regional do Agreste", "abbreviation": "CRA", "category": "Execução",
      "subordinadoA": "Diretoria Operacional", "legalRef": "Art. 35, VII",
      "baseLegal": "Lei nº 8.979, de 03 de fevereiro de 2022",
      "artigosDeOrigem": ["Art. 35 §2º VII"],
      "atribuicoes": ["Os Comandos Regionais Bombeiro Militar — CRBM subordinam-se à DOP e são órgãos de supervisão, coordenação e planejamento operacional das unidades subordinadas (Art. 35)"],
      "desdobramentos": ["3º GBM — Itabaiana"],
      "cargos": [{"cargo": "Chefe do Comando Regional do Agreste", "subordinadoA": "Diretoria Operacional", "requisito": "Oficial Superior QOBM (Art. 35 §2º)", "desdobramentos": [], "atribuicoes": ["Supervisão, coordenação e planejamento operacional das unidades subordinadas na AISP correspondente (Art. 35)"]}]
    },
    "crbsf-se": {
      "name": "Comando Regional do Baixo São Francisco", "abbreviation": "CRBSF", "category": "Execução",
      "subordinadoA": "Diretoria Operacional", "legalRef": "Art. 35, VIII",
      "baseLegal": "Lei nº 8.979, de 03 de fevereiro de 2022",
      "artigosDeOrigem": ["Art. 35 §2º VIII"],
      "atribuicoes": ["Os Comandos Regionais Bombeiro Militar — CRBM subordinam-se à DOP e são órgãos de supervisão, coordenação e planejamento operacional das unidades subordinadas (Art. 35)"],
      "desdobramentos": ["6º GBM — Propriá"],
      "cargos": [{"cargo": "Chefe do Comando Regional do Baixo São Francisco", "subordinadoA": "Diretoria Operacional", "requisito": "Oficial Superior QOBM (Art. 35 §2º)", "desdobramentos": [], "atribuicoes": ["Supervisão, coordenação e planejamento operacional das unidades subordinadas na AISP correspondente (Art. 35)"]}]
    },
    "gbm-se": {
      "name": "Grupamentos Bombeiro Militar", "abbreviation": "GBM", "category": "Execução",
      "subordinadoA": "Comandos Regionais Bombeiro Militar", "legalRef": "Art. 36, 37",
      "baseLegal": "Lei nº 8.979, de 03 de fevereiro de 2022",
      "artigosDeOrigem": ["Art. 36 (Unidades)", "Art. 37 (GBMs)"],
      "atribuicoes": ["As Unidades, também denominadas de Grupamentos, realizam a execução das atividades operacionais e de apoio da Corporação (Art. 36)"],
      "desdobramentos": ["1º GBM — Aracaju (CRM)", "2º GBM — Estância (CRS)", "3º GBM — Itabaiana (CRA)", "4º GBM — Nossa Senhora do Socorro (CRM/CRL)", "5º GBM — Lagarto (CRCS)", "6º GBM — Propriá (CRBSF)", "7º GBM — Nossa Senhora da Glória (CRAS/CRMS)", "8º GBM — Barra dos Coqueiros (CRM)"],
      "cargos": [{"cargo": "Comandante de GBM", "subordinadoA": "Comando Regional Bombeiro Militar", "requisito": "Oficial Superior QOBM (Art. 37 parágrafo único)", "desdobramentos": [], "atribuicoes": ["Execução das atividades operacionais e de apoio da Corporação na área do Grupamento (Art. 36, 37)"]}]
    },
    "gbs-se": {
      "name": "Grupamento de Busca e Salvamento", "abbreviation": "GBS", "category": "Execução Especializada",
      "subordinadoA": "Diretoria Operacional", "legalRef": "Art. 39, I",
      "baseLegal": "Lei nº 8.979, de 03 de fevereiro de 2022",
      "artigosDeOrigem": ["Art. 38 (Grupamentos Especializados)", "Art. 39 I (GBS)"],
      "atribuicoes": ["Os Grupamentos Especializados têm a seu encargo o planejamento e controle das atividades a eles correlatas e realizam missões específicas de cada área (Art. 38)"],
      "desdobramentos": [],
      "cargos": [{"cargo": "Comandante do GBS", "subordinadoA": "Diretoria Operacional", "requisito": "Oficial Superior QOBM (Art. 38)", "desdobramentos": [], "atribuicoes": ["Comando do Grupamento de Busca e Salvamento (Art. 38, 39 I)"]}]
    },
    "goa-se": {
      "name": "Grupamento de Operações Aéreas", "abbreviation": "GOA", "category": "Execução Especializada",
      "subordinadoA": "Diretoria Operacional", "legalRef": "Art. 39, II",
      "baseLegal": "Lei nº 8.979, de 03 de fevereiro de 2022",
      "artigosDeOrigem": ["Art. 38 (Grupamentos Especializados)", "Art. 39 II (GOA)"],
      "atribuicoes": ["Os Grupamentos Especializados têm a seu encargo o planejamento e controle das atividades a eles correlatas e realizam missões específicas de cada área (Art. 38)"],
      "desdobramentos": [],
      "cargos": [{"cargo": "Comandante do GOA", "subordinadoA": "Diretoria Operacional", "requisito": "Oficial Superior QOBM (Art. 38)", "desdobramentos": [], "atribuicoes": ["Comando do Grupamento de Operações Aéreas (Art. 38, 39 II)"]}]
    }
  }
},

"sp": {
  "legal_source": "Lei nº 616, de 17/12/1974 (organização básica da PMESP, atualizada até a Lei nº 735/1975) — Seção II, Corpo de Bombeiros (Arts. 38 a 43); complementada pelo Decreto nº 65.096, de 28/07/2020 (estrutura operacional vigente)",
  "organs": {
    "comando-corpo-bombeiros": {
      "name": "Comando do Corpo de Bombeiros", "abbreviation": "CCB", "category": "Direção Geral",
      "subordinadoA": "Comando-Geral da Polícia Militar", "legalRef": "Lei 616/1974, Arts. 38 a 40",
      "baseLegal": "Lei nº 616, de 17/12/1974 (atualizada até a Lei nº 735/1975)",
      "artigosDeOrigem": ["Art. 38 (organização do Corpo de Bombeiros)", "Art. 39 (Comando do Corpo de Bombeiros)", "Art. 40 (estrutura do Comando)"],
      "atribuicoes": ["Órgão responsável perante o Comando Geral pelo planejamento, comando, execução, coordenação, fiscalização e controle de todas as atividades de prevenção, extinção de incêndios e de buscas e salvamentos, bem como das atividades técnicas a elas relacionadas no território estadual (Art. 39)"],
      "desdobramentos": ["Comandante", "Estado Maior", "Secretaria", "Seção de Comando", "Centro de Comunicações do Corpo de Bombeiros (CC/CB)"],
      "cargos": [{"cargo": "Comandante do Corpo de Bombeiros", "subordinadoA": "Comando-Geral da Polícia Militar", "requisito": "Coronel PM, designado pelo Governador do Estado mediante indicação do Comandante-Geral da PM (Art. 40, §1º, red. Lei nº 663/1975)", "desdobramentos": [], "atribuicoes": ["Comando do Corpo de Bombeiros (Art. 39)", "Responsável, perante o Comando Geral, pelo planejamento, coordenação, fiscalização e controle dos suprimentos e manutenção dos materiais tipicamente operacionais das unidades subordinadas (Art. 39, parágrafo único)"]}]
    },
    "estado-maior-cb": {
      "name": "Estado Maior do Corpo de Bombeiros", "abbreviation": "EM/CB", "category": "Assessoramento",
      "subordinadoA": "Comando do Corpo de Bombeiros", "legalRef": "Lei 616/1974, Art. 40, II e §2º",
      "baseLegal": "Lei nº 616, de 17/12/1974 (atualizada até a Lei nº 735/1975)",
      "artigosDeOrigem": ["Art. 40, II (Estado Maior)", "Art. 40, §2º (organização do Estado Maior)"],
      "atribuicoes": ["Assessoria e planejamento ao Comandante do Corpo de Bombeiros nas áreas de pessoal (B/1), informações (B/2), organização, instrução e operações (B/3), fiscalização administrativa e logística (B/4), assuntos civis (B/5) e serviço técnico (B/6) (Lei nº 616/1974, Art. 40, II e §2º)"],
      "desdobramentos": ["Chefe do Estado Maior", "1ª Seção (B/1): pessoal", "2ª Seção (B/2): informações", "3ª Seção (B/3): organização, instrução e operações", "4ª Seção (B/4): fiscalização administrativa e logística", "5ª Seção (B/5): assuntos civis", "6ª Seção (B/6): Seção de Serviço Técnico"],
      "cargos": [{"cargo": "Chefe do Estado Maior", "subordinadoA": "Comandante do Corpo de Bombeiros", "requisito": "", "desdobramentos": [], "atribuicoes": ["Chefia do Estado Maior do Corpo de Bombeiros (Art. 40, §2º, 1)"]}]
    },
    "secao-servico-tecnico": {
      "name": "Seção de Serviço Técnico (B/6)", "abbreviation": "B/6", "category": "Seção do Estado Maior",
      "subordinadoA": "Estado Maior do Corpo de Bombeiros", "legalRef": "Lei 616/1974, Art. 40, §2º, 7",
      "baseLegal": "Lei nº 616, de 17/12/1974 (atualizada até a Lei nº 735/1975)",
      "artigosDeOrigem": ["Art. 40, §2º, item 7 (Seção de Serviço Técnico, B/6)"],
      "atribuicoes": ["Executar e supervisionar o disposto na legislação do Estado quanto à instalação de equipamentos e às medidas preventivas contra incêndios (alínea a)", "Proceder a exames de plantas e a perícias (alínea b)", "Realizar testes de incombustibilidade (alínea c)", "Realizar vistorias e emitir pareceres (alínea d)", "Supervisionar a instalação da rede de hidrantes públicos (alínea e)"],
      "desdobramentos": [],
      "cargos": [{"cargo": "Chefe da 6ª Seção — Serviço Técnico (B/6)", "subordinadoA": "Chefe do Estado Maior do Corpo de Bombeiros", "requisito": "Oficial PM (Lei nº 616/1974, Art. 40)", "desdobramentos": [], "atribuicoes": ["Executar e supervisionar o disposto na legislação do Estado quanto à instalação de equipamentos e às medidas preventivas contra incêndios (Lei nº 616/1974, Art. 40, §2º, 7, a)", "Proceder a exames de plantas e a perícias (Lei nº 616/1974, Art. 40, §2º, 7, b)", "Realizar testes de incombustibilidade (Lei nº 616/1974, Art. 40, §2º, 7, c)", "Realizar vistorias e emitir pareceres (Lei nº 616/1974, Art. 40, §2º, 7, d)", "Supervisionar a instalação da rede de hidrantes públicos (Lei nº 616/1974, Art. 40, §2º, 7, e)"]}]
    },
    "secretaria-cb": {
      "name": "Secretaria do Corpo de Bombeiros", "abbreviation": "Sec", "category": "Apoio",
      "subordinadoA": "Comando do Corpo de Bombeiros", "legalRef": "Lei 616/1974, Art. 40, III e §3º",
      "baseLegal": "Lei nº 616, de 17/12/1974 (atualizada até a Lei nº 735/1975)",
      "artigosDeOrigem": ["Art. 40, III (Secretaria)", "Art. 40, §3º"],
      "atribuicoes": ["Trabalhos relativos a correspondência, protocolo, arquivo, boletim diário e outros (Art. 40, §3º)"],
      "desdobramentos": [],
      "cargos": [{"cargo": "Secretário do Corpo de Bombeiros", "subordinadoA": "Comandante do Corpo de Bombeiros", "requisito": "Oficial PM (Lei nº 616/1974, Art. 40)", "desdobramentos": [], "atribuicoes": ["Responsável pelos trabalhos relativos a correspondência, protocolo, arquivo, boletim diário e outros (Lei nº 616/1974, Art. 40, §3º)"]}]
    },
    "secao-comando-cb": {
      "name": "Seção de Comando", "abbreviation": "SC", "category": "Apoio",
      "subordinadoA": "Comando do Corpo de Bombeiros", "legalRef": "Lei 616/1974, Art. 40, IV e §4º",
      "baseLegal": "Lei nº 616, de 17/12/1974 (atualizada até a Lei nº 735/1975)",
      "artigosDeOrigem": ["Art. 40, IV (Seção de Comando)", "Art. 40, §4º"],
      "atribuicoes": ["Apoio de pessoal auxiliar (praças) necessário aos trabalhos burocráticos do Comando (Art. 40, §4º, 1)", "Serviços gerais e segurança do aquartelamento (Art. 40, §4º, 2)"],
      "desdobramentos": [],
      "cargos": [{"cargo": "Chefe da Seção de Comando", "subordinadoA": "Comandante do Corpo de Bombeiros", "requisito": "Oficial PM (Lei nº 616/1974, Art. 40)", "desdobramentos": [], "atribuicoes": ["Providenciar o apoio de pessoal auxiliar (praças) necessário aos trabalhos burocráticos do Comando (Lei nº 616/1974, Art. 40, §4º, 1)", "Supervisionar os serviços gerais e segurança do aquartelamento (Lei nº 616/1974, Art. 40, §4º, 2)"]}]
    },
    "cc-cb": {
      "name": "Centro de Comunicações do Corpo de Bombeiros", "abbreviation": "CC/CB", "category": "Apoio",
      "subordinadoA": "Comando do Corpo de Bombeiros", "legalRef": "Lei 616/1974, Art. 40, V",
      "baseLegal": "Lei nº 616/1974 (inciso V acrescentado pela Lei nº 663/1975)",
      "artigosDeOrigem": ["Art. 40, V (Centro de Comunicações, acrescido pela Lei nº 663/1975)"],
      "atribuicoes": ["Órgão de comunicações do Corpo de Bombeiros (Art. 40, V, acrescido pela Lei nº 663/1975)"],
      "desdobramentos": [],
      "cargos": [{"cargo": "Comandante do Centro de Comunicações do Corpo de Bombeiros", "subordinadoA": "Comandante do Corpo de Bombeiros", "requisito": "Oficial PM (Lei nº 616/1974, Art. 40, V)", "desdobramentos": [], "atribuicoes": ["Direção do Centro de Comunicações do Corpo de Bombeiros, órgão responsável pelas atividades de comunicações da tropa (Lei nº 616/1974, Art. 40, V, red. Lei nº 663/1975)"]}]
    },
    "grupamento-incendio": {
      "name": "Grupamentos de Incêndio", "abbreviation": "GI", "category": "Execução",
      "subordinadoA": "Comando do Corpo de Bombeiros", "legalRef": "Lei 616/1974, Art. 41, I; Art. 42",
      "baseLegal": "Lei nº 616, de 17/12/1974 (atualizada até a Lei nº 735/1975)",
      "artigosDeOrigem": ["Art. 41, I (Grupamentos de Incêndio)", "Art. 42 (organização interna)"],
      "atribuicoes": ["Unidades diretamente subordinadas ao Comando do Corpo de Bombeiros, incumbidas da missão de extinção de incêndios, podendo integrar missões de busca e salvamento (Art. 41, I)"],
      "desdobramentos": ["Comando", "Estado Maior (Art. 42, §4º, acrescido pela Lei nº 663/1975)", "Seção de Comando e Serviços", "Seção de Incêndio ou de Busca e Salvamento", "Sub-Grupamentos de Incêndio (S/GI)"],
      "cargos": [{"cargo": "Comandante de Grupamento de Incêndio", "subordinadoA": "Comando do Corpo de Bombeiros", "requisito": "", "desdobramentos": [], "atribuicoes": ["Comando do Grupamento de Incêndio (Art. 42, I)"]}]
    },
    "subgrupamento-incendio": {
      "name": "Sub-Grupamentos de Incêndio", "abbreviation": "S/GI", "category": "Execução",
      "subordinadoA": "Grupamento de Incêndio (GI)", "legalRef": "Lei 616/1974, Art. 41, II; Art. 42",
      "baseLegal": "Lei nº 616, de 17/12/1974 (atualizada até a Lei nº 735/1975)",
      "artigosDeOrigem": ["Art. 41, II (Sub-Grupamentos de Incêndio)", "Art. 42 (organização interna)"],
      "atribuicoes": ["Unidades incumbidas da missão de extinção de incêndios, subordinadas a um Grupamento de Incêndio, podendo integrar eventualmente missões de busca e salvamento (Art. 41, II)"],
      "desdobramentos": ["Comando", "Seção de Comando e Serviços", "Seção de Incêndio ou de Busca e Salvamento"],
      "cargos": [{"cargo": "Comandante de Sub-Grupamento de Incêndio", "subordinadoA": "Grupamento de Incêndio (GI)", "requisito": "", "desdobramentos": [], "atribuicoes": ["Comando do Sub-Grupamento de Incêndio (Art. 42)"]}]
    },
    "grupamento-busca-salvamento": {
      "name": "Grupamentos de Busca e Salvamento", "abbreviation": "GBS", "category": "Execução",
      "subordinadoA": "Comando do Corpo de Bombeiros", "legalRef": "Lei 616/1974, Art. 41, III; Art. 42",
      "baseLegal": "Lei nº 616, de 17/12/1974 (atualizada até a Lei nº 735/1975)",
      "artigosDeOrigem": ["Art. 41, III (Grupamentos de Busca e Salvamento)", "Art. 42 (organização interna)"],
      "atribuicoes": ["Unidades diretamente subordinadas ao Comando do Corpo de Bombeiros, incumbidas da missão de busca e salvamento, de modo especial em razão da extensão da missão (Art. 41, III)"],
      "desdobramentos": ["Comando", "Seção de Comando e Serviços", "Seção de Busca e Salvamento", "Sub-Seções de Busca e Salvamento (Art. 42, §3º)"],
      "cargos": [{"cargo": "Comandante de Grupamento de Busca e Salvamento", "subordinadoA": "Comando do Corpo de Bombeiros", "requisito": "", "desdobramentos": [], "atribuicoes": ["Comando do Grupamento de Busca e Salvamento (Art. 42)"]}]
    },
    "ciad": {
      "name": "Centro de Instruções e Adestramento", "abbreviation": "CIAd", "category": "Apoio",
      "subordinadoA": "Corpo de Bombeiros", "legalRef": "Lei 616/1974, Art. 43, I",
      "baseLegal": "Lei nº 616/1974 (Art. 43 com redação da Lei nº 663/1975)",
      "artigosDeOrigem": ["Art. 43, I (Centro de Instruções e Adestramento, red. Lei nº 663/1975)"],
      "atribuicoes": ["Destinado a possibilitar o adestramento e a instrução da tropa do Corpo, bem como a preparação de bombeiros civis de entidades privadas (Art. 43, I)"],
      "desdobramentos": [],
      "cargos": [{"cargo": "Comandante do Centro de Instruções e Adestramento", "subordinadoA": "Comandante do Corpo de Bombeiros", "requisito": "Oficial PM (Lei nº 616/1974, Art. 43)", "desdobramentos": [], "atribuicoes": ["Direção do Centro de Instruções e Adestramento, destinado a possibilitar o adestramento e a instrução da tropa do Corpo, bem como a preparação de bombeiros civis de entidades privadas (Lei nº 616/1974, Art. 43, I, red. Lei nº 663/1975)"]}]
    },
    "csm-mop": {
      "name": "Centro de Suprimento e Manutenção do Material Operacional", "abbreviation": "CSM/MOp", "category": "Apoio",
      "subordinadoA": "Corpo de Bombeiros", "legalRef": "Lei 616/1974, Art. 43, II e parágrafo único",
      "baseLegal": "Lei nº 616/1974 (Art. 43 com redação da Lei nº 663/1975)",
      "artigosDeOrigem": ["Art. 43, II (CSM/MOp)", "Art. 43, parágrafo único"],
      "atribuicoes": ["Incumbido do recebimento, da estocagem e da distribuição dos suprimentos e da execução da manutenção no que concerne ao material especializado (Art. 43, II)", "As demais necessidades de suprimentos e manutenção são asseguradas pela Diretoria de Apoio Logístico da Corporação (Art. 43, parágrafo único)"],
      "desdobramentos": [],
      "cargos": [{"cargo": "Comandante do Centro de Suprimento e Manutenção do Material Operacional", "subordinadoA": "Comandante do Corpo de Bombeiros", "requisito": "Oficial PM (Lei nº 616/1974, Art. 43)", "desdobramentos": [], "atribuicoes": ["Direção do Centro de Suprimento e Manutenção do Material Operacional, incumbido do recebimento, da estocagem e da distribuição dos suprimentos e da execução da manutenção no que concerne ao material especializado do Corpo de Bombeiros (Lei nº 616/1974, Art. 43, II, red. Lei nº 663/1975)", "As demais necessidades de suprimentos e manutenção são asseguradas pela Diretoria de Apoio Logístico da Corporação (Lei nº 616/1974, Art. 43, parágrafo único)"]}]
    },
    "cbm-metropolitano": {
      "name": "Comando de Bombeiros Metropolitano", "abbreviation": "CBM", "category": "Execução",
      "subordinadoA": "Comando do Corpo de Bombeiros", "legalRef": "Decreto 65.096/2020, Art. 25, I",
      "baseLegal": "Decreto nº 65.096, de 28 de julho de 2020 (estrutura operacional vigente)",
      "artigosDeOrigem": ["Art. 25, I (Comando de Bombeiros Metropolitano)"],
      "atribuicoes": ["Planejamento, coordenação, controle e apoio de atividades técnicas, logísticas, operacionais e administrativas", "Responsabilidade pelos Grupamentos subordinados em sua área (Região Metropolitana)"],
      "desdobramentos": ["1º a 4º Grupamento de Bombeiros (Capital)", "5º GB (Guarulhos)", "8º GB (Santo André)", "17º GB (Mogi das Cruzes)", "18º GB (Barueri)"],
      "cargos": [{"cargo": "Comandante de Bombeiros Metropolitano", "subordinadoA": "Comandante do Corpo de Bombeiros", "requisito": "Coronel PM (Decreto nº 65.096/2020, Art. 25)", "desdobramentos": ["1º ao 4º Grupamento de Bombeiros (Capital)", "5º GB (Guarulhos)", "8º GB (Santo André)", "17º GB (Mogi das Cruzes)", "18º GB (Barueri)"], "atribuicoes": ["Responsável pelo planejamento, coordenação, controle e apoio de atividades técnicas, logísticas, operacionais e administrativas dos Grupamentos subordinados na Região Metropolitana de São Paulo (Decreto nº 65.096/2020, Art. 25, I)"]}]
    },
    "cbi-interior": {
      "name": "Comando de Bombeiros do Interior", "abbreviation": "CBI", "category": "Execução",
      "subordinadoA": "Comando do Corpo de Bombeiros", "legalRef": "Decreto 65.096/2020, Art. 25, II",
      "baseLegal": "Decreto nº 65.096, de 28 de julho de 2020 (estrutura operacional vigente)",
      "artigosDeOrigem": ["Art. 25, II (Comando de Bombeiros do Interior)"],
      "atribuicoes": ["Planejamento, coordenação, controle e apoio de atividades técnicas, logísticas, operacionais e administrativas", "Responsabilidade pelos Grupamentos subordinados em sua área (Interior)"],
      "desdobramentos": ["6º GB (Santos)", "7º GB (Campinas)", "9º GB (Ribeirão Preto)", "10º GB (Marília)", "11º GB (São José dos Campos)", "12º GB (Bauru)", "13º GB (São José do Rio Preto)", "14º GB (Presidente Prudente)", "15º GB (Sorocaba)", "16º GB (Piracicaba)", "19º GB (Jundiaí)", "20º GB (Araçatuba)", "Grupamento de Bombeiros Marítimo (GBMar) - Guarujá"],
      "cargos": [{"cargo": "Comandante de Bombeiros do Interior", "subordinadoA": "Comandante do Corpo de Bombeiros", "requisito": "Coronel PM (Decreto nº 65.096/2020, Art. 25)", "desdobramentos": ["6º ao 20º Grupamentos de Bombeiros do Interior", "Grupamento de Bombeiros Marítimo (GBMar)"], "atribuicoes": ["Responsável pelo planejamento, coordenação, controle e apoio de atividades técnicas, logísticas, operacionais e administrativas dos Grupamentos subordinados no Interior do Estado de São Paulo (Decreto nº 65.096/2020, Art. 25, II)"]}]
    }
  }
},

"to": {
  "legal_source": "Lei Complementar nº 131, de 30 de setembro de 2021",
  "organs": {
    "cg-to": {
      "name": "Comando-Geral", "abbreviation": "CG", "category": "Direção Superior",
      "subordinadoA": "Chefe do Poder Executivo", "legalRef": "Art. 2º; Art. 5º; Art. 7º LC 131/2021",
      "baseLegal": "Lei Complementar nº 131, de 30 de setembro de 2021",
      "artigosDeOrigem": ["Art. 2º (Competências do CBMTO)", "Art. 5º (Direção Superior)", "Art. 7º (Comandante-Geral)"],
      "atribuicoes": [
        "O Comandante-Geral, Secretário de Estado, nomeado por ato do Chefe do Poder Executivo, é responsável pelo comando, administração e emprego da Corporação e do Comando de Ações de Defesa Civil, assessorado pelas demais unidades administrativas, que lhe são subordinadas. (Art. 7º)",
        "I - o planejamento estratégico; (Art. 5º, I)",
        "II - o estabelecimento das diretrizes, ordens e normas técnicas ou gerais. (Art. 5º, II)",
        "I - planejar, coordenar e executar ações preventivas, emergenciais, de socorro, assistenciais e recuperativas no âmbito da defesa civil; (Art. 2º, I)",
        "II - planejar, editar atos normativos, coordenar, dirigir e executar as ações de prevenção e extinção de incêndios, emergência, busca e salvamento, resgate e atendimento pré-hospitalar; (Art. 2º, II)",
        "III - exercer, privativamente, a prevenção contra incêndio e emergência no Estado do Tocantins, mediante: a) o planejamento de ações; b) o estabelecimento de normas; c) a análise de projetos de sistemas de prevenção contra incêndio e emergência; d) a vistoria, certificação e fiscalização de edificações e áreas de riscos. (Art. 2º, III)",
        "IV - fiscalizar e fazer cumprir a legislação de prevenção contra incêndio e emergência, podendo, interditar, embargar e aplicar outras sanções previstas na legislação específica, quanto às edificações, obras, serviços, atividades e locais de concentração de público que não ofereçam condições de segurança e de funcionamento; (Art. 2º, IV)",
        "V - realizar a perícia de incêndios e de locais de sinistros ou com risco de colapso; (Art. 2º, V)",
        "VI - exercer a polícia judiciária militar e a apuração das infrações penais militares praticadas pelos seus membros, nos termos da legislação federal; (Art. 2º, VI)",
        "VII - proteger o meio ambiente mediante a realização de atividades de prevenção, fiscalização e extinção de incêndio florestal; (Art. 2º, VII)",
        "VIII - regular, credenciar e fiscalizar empresas de fabricação e comercialização de produtos, bem como as escolas formadoras, na prestação de serviços relativos à segurança contra incêndio, emergência e os demais serviços civis públicos e privados auxiliares de bombeiros e congêneres; (Art. 2º, VIII)",
        "IX - fiscalizar, no âmbito de sua competência, os serviços de armazenamento e transporte de produtos especiais e perigosos, visando à proteção das pessoas, do patrimônio público e privado, e do meio ambiente; (Art. 2º, IX)",
        "X - exercer o poder de polícia no âmbito de sua competência; (Art. 2º, X)",
        "XI - realizar pesquisas técnico-científicas, testes e exames técnicos relacionados com as suas atividades. (Art. 2º, XI)"
      ],
      "desdobramentos": [],
      "cargos": [{"cargo": "Comandante-Geral", "subordinadoA": "Chefe do Poder Executivo", "requisito": "Coronel da ativa do QOBM, diplomado no Curso Superior de Bombeiro Militar ou equivalente (Art. 7º §único)", "desdobramentos": [], "atribuicoes": ["Comando, administração e emprego da Corporação e do Comando de Ações de Defesa Civil (Art. 7º)."]}]
    },
    "chem": {
      "name": "Chefe do Estado-Maior / Subcomandante-Geral", "abbreviation": "CHEM", "category": "Direção Superior",
      "subordinadoA": "Comandante-Geral", "legalRef": "Art. 8º LC 131/2021",
      "baseLegal": "Lei Complementar nº 131, de 30 de setembro de 2021",
      "artigosDeOrigem": ["Art. 8º (Chefe do Estado-Maior)"],
      "atribuicoes": [
        "O Chefe do Estado-Maior, designado por ato do Chefe do Poder Executivo, é o principal assessor do Comandante-Geral, competindo-lhe a direção, orientação e fiscalização dos trabalhos do Estado-Maior. (Art. 8º caput)",
        "§1º O Chefe do Estado-Maior acumula a função de Subcomandante-Geral e substitui o Comandante-Geral em seus eventuais afastamentos e impedimentos."
      ],
      "desdobramentos": [],
      "cargos": [{"cargo": "Chefe do Estado-Maior", "subordinadoA": "Comandante-Geral", "requisito": "Coronel da ativa do QOBM, diplomado no Curso Superior de Bombeiro Militar ou equivalente (Art. 8º §2º)", "desdobramentos": [], "atribuicoes": ["Direção, orientação e fiscalização dos trabalhos do Estado-Maior; acumula função de Subcomandante-Geral (Art. 8º)."]}]
    },
    "subchem": {
      "name": "Subchefe do Estado-Maior", "abbreviation": "SUBCHEM", "category": "Direção Superior",
      "subordinadoA": "Chefe do Estado-Maior", "legalRef": "Art. 9º LC 131/2021",
      "baseLegal": "Lei Complementar nº 131, de 30 de setembro de 2021",
      "artigosDeOrigem": ["Art. 9º (Subchefe do Estado-Maior)"],
      "atribuicoes": [
        "§3º Compete ao Subchefe do Estado-Maior coordenar as Seções do Estado-Maior, bem como substituir o Chefe do Estado-Maior em seus eventuais afastamentos e impedimentos legais. (Art. 9º §3º)"
      ],
      "desdobramentos": [],
      "cargos": [{"cargo": "Subchefe do Estado-Maior", "subordinadoA": "Chefe do Estado-Maior", "requisito": "Coronel da ativa do QOBM, diplomado no Curso Superior de Bombeiro Militar ou equivalente (Art. 9º)", "desdobramentos": [], "atribuicoes": ["Coordenação das Seções do Estado-Maior e substituição do Chefe do Estado-Maior (Art. 9º §3º)."]}]
    },
    "em-to": {
      "name": "Estado-Maior", "abbreviation": "EM", "category": "Direção Superior",
      "subordinadoA": "Chefe do Estado-Maior", "legalRef": "Art. 10; Art. 11 LC 131/2021",
      "baseLegal": "Lei Complementar nº 131, de 30 de setembro de 2021",
      "artigosDeOrigem": ["Art. 10 (Estado-Maior)", "Art. 11 (Estrutura e seções)"],
      "atribuicoes": [
        "O Estado-Maior é responsável pelas ações de planejamento, estudo, orientação, coordenação, fiscalização e controle das atividades do CBMTO, cabendo-lhe a formulação de diretrizes, ordens e normas gerais de ação do Comandante-Geral no acionamento das unidades da Corporação. (Art. 10)",
        "O Estado-Maior é comandado pelo Chefe do Estado-Maior, coordenado pelo Subchefe do Estado-Maior e estruturado em: Comando de Correição e Disciplina; Comando de Ações de Defesa Civil; Comando de Gestão de Pessoas; Comando de Gestão de Recursos Financeiros e Patrimoniais; Comando de Atividades Técnicas; Comando Operacional Bombeiro Militar. (Art. 11)"
      ],
      "desdobramentos": [],
      "cargos": [{"cargo": "Chefe do Estado-Maior", "subordinadoA": "Comandante-Geral", "requisito": "Coronel QOBM (Art. 8º §2º)", "desdobramentos": [], "atribuicoes": ["Comando do Estado-Maior (Art. 11)."]}]
    },
    "ccd-to": {
      "name": "Comando de Correição e Disciplina", "abbreviation": "CCorD", "category": "Seção do Estado-Maior",
      "subordinadoA": "Chefe do Estado-Maior", "legalRef": "Art. 12 LC 131/2021",
      "baseLegal": "Lei Complementar nº 131, de 30 de setembro de 2021",
      "artigosDeOrigem": ["Art. 12 (Comando de Correição e Disciplina)"],
      "atribuicoes": [
        "I - garantir a preservação dos princípios da hierarquia e disciplina da Corporação;",
        "II - controlar, orientar e padronizar processos administrativos disciplinares e Inquéritos Policiais Militares;",
        "III - apurar transgressões disciplinares e infrações penais de natureza militar envolvendo seus membros;",
        "IV - acompanhar pessoal submetido a processo penal e processo penal militar."
      ],
      "desdobramentos": [],
      "cargos": [{"cargo": "Comandante de Correição e Disciplina", "subordinadoA": "Chefe do Estado-Maior", "requisito": "Coronel da ativa do QOBM, diplomado no Curso Superior de Bombeiro Militar ou equivalente (Art. 11 §único)", "desdobramentos": [], "atribuicoes": ["I a IV – atribuições previstas no Art. 12 da LC nº 131/2021."]}]
    },
    "cadc-to": {
      "name": "Comando de Ações de Defesa Civil", "abbreviation": "CADC", "category": "Seção do Estado-Maior",
      "subordinadoA": "Chefe do Estado-Maior", "legalRef": "Art. 13 LC 131/2021",
      "baseLegal": "Lei Complementar nº 131, de 30 de setembro de 2021",
      "artigosDeOrigem": ["Art. 13 (Comando de Ações de Defesa Civil)"],
      "atribuicoes": [
        "O Comando de Ações de Defesa Civil é responsável pelo planejamento e coordenação das ações de prevenção, preparação e resposta no âmbito da defesa civil. (Art. 13)"
      ],
      "desdobramentos": [],
      "cargos": [{"cargo": "Comandante de Ações de Defesa Civil", "subordinadoA": "Chefe do Estado-Maior", "requisito": "Coronel da ativa do QOBM (Art. 11 §único)", "desdobramentos": [], "atribuicoes": ["Planejamento e coordenação das ações de defesa civil (Art. 13)."]}]
    },
    "cgp-to": {
      "name": "Comando de Gestão de Pessoas", "abbreviation": "CGP", "category": "Seção do Estado-Maior",
      "subordinadoA": "Chefe do Estado-Maior", "legalRef": "Art. 14 LC 131/2021",
      "baseLegal": "Lei Complementar nº 131, de 30 de setembro de 2021",
      "artigosDeOrigem": ["Art. 14 (Comando de Gestão de Pessoas)"],
      "atribuicoes": [
        "O Comando de Gestão de Pessoas é encarregado do planejamento e dos assuntos estratégicos referentes à gestão profissional, à legislação, ao pessoal, à saúde e ao ensino na Corporação. (Art. 14)"
      ],
      "desdobramentos": [],
      "cargos": [{"cargo": "Comandante de Gestão de Pessoas", "subordinadoA": "Chefe do Estado-Maior", "requisito": "Coronel da ativa do QOBM (Art. 11 §único)", "desdobramentos": [], "atribuicoes": ["Planejamento dos assuntos de gestão profissional, legislação, pessoal, saúde e ensino (Art. 14)."]}]
    },
    "cgrf-to": {
      "name": "Comando de Gestão de Recursos Financeiros e Patrimoniais", "abbreviation": "CGRF", "category": "Seção do Estado-Maior",
      "subordinadoA": "Chefe do Estado-Maior", "legalRef": "Art. 15 LC 131/2021",
      "baseLegal": "Lei Complementar nº 131, de 30 de setembro de 2021",
      "artigosDeOrigem": ["Art. 15 (Comando de Gestão de Recursos Financeiros e Patrimoniais)"],
      "atribuicoes": [
        "O Comando de Gestão de Recursos Financeiros e Patrimoniais é responsável pelo planejamento dos assuntos referentes ao orçamento, finanças, logística e infraestrutura da Corporação. (Art. 15)"
      ],
      "desdobramentos": [],
      "cargos": [{"cargo": "Comandante de Gestão de Recursos", "subordinadoA": "Chefe do Estado-Maior", "requisito": "Coronel da ativa do QOBM (Art. 11 §único)", "desdobramentos": [], "atribuicoes": ["Planejamento dos assuntos de orçamento, finanças, logística e infraestrutura (Art. 15)."]}]
    },
    "cat-to": {
      "name": "Comando de Atividades Técnicas", "abbreviation": "CAT", "category": "Seção do Estado-Maior",
      "subordinadoA": "Chefe do Estado-Maior", "legalRef": "Art. 16 LC 131/2021",
      "baseLegal": "Lei Complementar nº 131, de 30 de setembro de 2021",
      "artigosDeOrigem": ["Art. 16 (Comando de Atividades Técnicas)"],
      "atribuicoes": [
        "O Comando de Atividades Técnicas é encarregado de planejar, controlar e fiscalizar as atividades atinentes à segurança contra incêndio e emergência no Estado. (Art. 16)"
      ],
      "desdobramentos": [],
      "cargos": [{"cargo": "Comandante de Atividades Técnicas", "subordinadoA": "Chefe do Estado-Maior", "requisito": "Coronel da ativa do QOBM (Art. 11 §único)", "desdobramentos": [], "atribuicoes": ["Planejamento, controle e fiscalização das atividades de SCI e emergência (Art. 16)."]}]
    },
    "cobm-to": {
      "name": "Comando Operacional Bombeiro Militar", "abbreviation": "COBM", "category": "Seção do Estado-Maior",
      "subordinadoA": "Chefe do Estado-Maior", "legalRef": "Art. 17 LC 131/2021",
      "baseLegal": "Lei Complementar nº 131, de 30 de setembro de 2021",
      "artigosDeOrigem": ["Art. 17 (Comando Operacional Bombeiro Militar)"],
      "atribuicoes": [
        "O Comando Operacional Bombeiro Militar é responsável pelo planejamento dos assuntos relativos à articulação operacional, à administração e ao controle das operações bombeiro militares e pelos estudos, estatísticas, doutrinas, pesquisas e padronização de procedimentos relacionados às atividades operacionais da Corporação. (Art. 17)",
        "§único. De acordo com a necessidade, poderá o Comando Operacional Bombeiro Militar ser dividido em regionais, conforme plano de articulação do CBMTO."
      ],
      "desdobramentos": [],
      "cargos": [{"cargo": "Comandante Operacional Bombeiro Militar", "subordinadoA": "Chefe do Estado-Maior", "requisito": "Coronel da ativa do QOBM (Art. 11 §único)", "desdobramentos": [], "atribuicoes": ["Planejamento da articulação operacional e padronização de procedimentos operacionais (Art. 17)."]}]
    },
    "gab-to": {
      "name": "Gabinete do Comandante-Geral", "abbreviation": "Gab", "category": "Assessoramento",
      "subordinadoA": "Comandante-Geral", "legalRef": "Art. 19, VI LC 131/2021",
      "baseLegal": "Lei Complementar nº 131, de 30 de setembro de 2021",
      "artigosDeOrigem": ["Art. 19, VI (Gabinete do Comandante-Geral)"],
      "atribuicoes": [
        "a) transmissão e controle da execução das ordens emanadas do Comandante-Geral;",
        "b) organização da correspondência e despacho da documentação do Gabinete;",
        "c) ajudância de ordens;",
        "d) secretariado geral do Comandante-Geral e do Chefe do Estado-Maior;",
        "e) publicação do Boletim Geral."
      ],
      "desdobramentos": [],
      "cargos": [{"cargo": "Chefe do Gabinete", "subordinadoA": "Comandante-Geral", "requisito": "Oficial QOBM", "desdobramentos": [], "atribuicoes": ["a a e – atribuições previstas no Art. 19, VI da LC nº 131/2021."]}]
    },
    "ai-to": {
      "name": "Assessoria de Inteligência", "abbreviation": "AI", "category": "Assessoramento",
      "subordinadoA": "Comandante-Geral", "legalRef": "Art. 19, I LC 131/2021",
      "baseLegal": "Lei Complementar nº 131, de 30 de setembro de 2021",
      "artigosDeOrigem": ["Art. 19, I (Assessoria de Inteligência)"],
      "atribuicoes": [
        "a) a inteligência e contrainteligência;",
        "b) a guarda e manutenção de documentos e arquivos sigilosos;",
        "c) ao controle de armamento dos integrantes da Corporação;",
        "d) a confecção do boletim reservado da Corporação;",
        "e) ao secretariado da Comissão de Promoções de Oficiais - CPO e Comissão de Promoção de Praças – CPP."
      ],
      "desdobramentos": [],
      "cargos": [{"cargo": "Chefe da Assessoria de Inteligência", "subordinadoA": "Comandante-Geral", "requisito": "Oficial QOBM", "desdobramentos": [], "atribuicoes": ["a a e – atribuições previstas no Art. 19, I da LC nº 131/2021."]}]
    },
    "aj-to": {
      "name": "Assessoria Jurídica", "abbreviation": "AJ", "category": "Assessoramento",
      "subordinadoA": "Comandante-Geral", "legalRef": "Art. 19, II LC 131/2021",
      "baseLegal": "Lei Complementar nº 131, de 30 de setembro de 2021",
      "artigosDeOrigem": ["Art. 19, II (Assessoria Jurídica)"],
      "atribuicoes": [
        "Assessoria Jurídica, com atribuições de consultoria, análise e emissão de pareceres jurídicos nos processos e assuntos de interesse da Corporação. (Art. 19, II)"
      ],
      "desdobramentos": [],
      "cargos": [{"cargo": "Chefe da Assessoria Jurídica", "subordinadoA": "Comandante-Geral", "requisito": "Oficial QOBM com formação em Direito", "desdobramentos": [], "atribuicoes": ["Consultoria, análise e emissão de pareceres jurídicos (Art. 19, II)."]}]
    },
    "acs-to": {
      "name": "Assessoria de Comunicação Social", "abbreviation": "ACS", "category": "Assessoramento",
      "subordinadoA": "Comandante-Geral", "legalRef": "Art. 19, III LC 131/2021",
      "baseLegal": "Lei Complementar nº 131, de 30 de setembro de 2021",
      "artigosDeOrigem": ["Art. 19, III (Assessoria de Comunicação Social)"],
      "atribuicoes": [
        "encarregada das atividades de comunicação social, publicidade, relacionamento com a mídia, cerimonial, eventos e marketing institucional. (Art. 19, III)"
      ],
      "desdobramentos": [],
      "cargos": [{"cargo": "Chefe da Assessoria de Comunicação Social", "subordinadoA": "Comandante-Geral", "requisito": "Oficial QOBM", "desdobramentos": [], "atribuicoes": ["Comunicação social, publicidade, cerimonial e marketing institucional (Art. 19, III)."]}]
    },
    "age-to": {
      "name": "Assessoria de Gestão Estratégica", "abbreviation": "AGE", "category": "Assessoramento",
      "subordinadoA": "Comandante-Geral", "legalRef": "Art. 19, IV LC 131/2021",
      "baseLegal": "Lei Complementar nº 131, de 30 de setembro de 2021",
      "artigosDeOrigem": ["Art. 19, IV (Assessoria de Gestão Estratégica)"],
      "atribuicoes": [
        "responsável por acompanhar a gestão estratégica e desenvolver os projetos da Corporação, em conjunto com as outras seções pertinentes. (Art. 19, IV)"
      ],
      "desdobramentos": [],
      "cargos": [{"cargo": "Chefe da Assessoria de Gestão Estratégica", "subordinadoA": "Comandante-Geral", "requisito": "Oficial QOBM", "desdobramentos": [], "atribuicoes": ["Acompanhamento da gestão estratégica e projetos da Corporação (Art. 19, IV)."]}]
    },
    "ati-to": {
      "name": "Assessoria de Telecomunicações e Informática", "abbreviation": "ATI", "category": "Assessoramento",
      "subordinadoA": "Comandante-Geral", "legalRef": "Art. 19, V LC 131/2021",
      "baseLegal": "Lei Complementar nº 131, de 30 de setembro de 2021",
      "artigosDeOrigem": ["Art. 19, V (Assessoria de Telecomunicações e Informática)"],
      "atribuicoes": [
        "responsável pela coordenação e execução das matérias relativas à informática, telecomunicações e tecnologia da informação. (Art. 19, V)"
      ],
      "desdobramentos": [],
      "cargos": [{"cargo": "Chefe da Assessoria de Telecomunicações e Informática", "subordinadoA": "Comandante-Geral", "requisito": "Oficial QOBM", "desdobramentos": [], "atribuicoes": ["Coordenação e execução de informática, telecomunicações e TI (Art. 19, V)."]}]
    },
    "dagp-to": {
      "name": "Diretoria de Administração e Gestão de Pessoas", "abbreviation": "DAGP", "category": "Direção Setorial",
      "subordinadoA": "Comando de Gestão de Pessoas", "legalRef": "Art. 18, I LC 131/2021",
      "baseLegal": "Lei Complementar nº 131, de 30 de setembro de 2021",
      "artigosDeOrigem": ["Art. 18, I (Diretoria de Administração e Gestão de Pessoas)"],
      "atribuicoes": [
        "encarregada da coordenação e execução dos assuntos inerentes à gestão de pessoal, pelos civis e militares ativos, inativos e pensionistas, pelo recrutamento e seleção e pela folha de pagamento. (Art. 18, I)"
      ],
      "desdobramentos": [],
      "cargos": [{"cargo": "Diretor de Administração e Gestão de Pessoas", "subordinadoA": "Comando de Gestão de Pessoas", "requisito": "Oficial QOBM", "desdobramentos": [], "atribuicoes": ["Gestão de pessoal, recrutamento e seleção e folha de pagamento (Art. 18, I)."]}]
    },
    "dep-to": {
      "name": "Diretoria de Ensino e Pesquisa", "abbreviation": "DEP", "category": "Direção Setorial",
      "subordinadoA": "Comando de Gestão de Pessoas", "legalRef": "Art. 18, II LC 131/2021",
      "baseLegal": "Lei Complementar nº 131, de 30 de setembro de 2021",
      "artigosDeOrigem": ["Art. 18, II (Diretoria de Ensino e Pesquisa)"],
      "atribuicoes": [
        "encarregada de assuntos relativos à coordenação e execução do ensino, instrução e pesquisa, inerentes às atividades de bombeiro militar. (Art. 18, II)"
      ],
      "desdobramentos": ["Academia de Formação de Bombeiros", "Colégios Militares do CBM-TO"],
      "cargos": [{"cargo": "Diretor de Ensino e Pesquisa", "subordinadoA": "Comando de Gestão de Pessoas", "requisito": "Oficial QOBM", "desdobramentos": [], "atribuicoes": ["Coordenação e execução do ensino, instrução e pesquisa de bombeiro militar (Art. 18, II)."]}]
    },
    "dlp-to": {
      "name": "Diretoria de Logística e Patrimônio", "abbreviation": "DLP", "category": "Direção Setorial",
      "subordinadoA": "Comando de Gestão de Recursos Financeiros e Patrimoniais", "legalRef": "Art. 18, III LC 131/2021",
      "baseLegal": "Lei Complementar nº 131, de 30 de setembro de 2021",
      "artigosDeOrigem": ["Art. 18, III (Diretoria de Logística e Patrimônio)"],
      "atribuicoes": [
        "responsável pelos assuntos relativos à aquisição de material e serviços, logística geral, e ao controle e fiscalização do patrimônio e estoque. (Art. 18, III)"
      ],
      "desdobramentos": [],
      "cargos": [{"cargo": "Diretor de Logística e Patrimônio", "subordinadoA": "Comando de Gestão de Recursos", "requisito": "Oficial QOBM", "desdobramentos": [], "atribuicoes": ["Aquisição de material e serviços, logística geral e controle de patrimônio (Art. 18, III)."]}]
    },
    "dof-to": {
      "name": "Diretoria de Orçamento e Finanças", "abbreviation": "DOF", "category": "Direção Setorial",
      "subordinadoA": "Comando de Gestão de Recursos Financeiros e Patrimoniais", "legalRef": "Art. 18, IV LC 131/2021",
      "baseLegal": "Lei Complementar nº 131, de 30 de setembro de 2021",
      "artigosDeOrigem": ["Art. 18, IV (Diretoria de Orçamento e Finanças)"],
      "atribuicoes": [
        "encarregada dos assuntos relativos à coordenação, acompanhamento e avaliação, e à execução orçamentária e financeira da corporação. (Art. 18, IV)"
      ],
      "desdobramentos": [],
      "cargos": [{"cargo": "Diretor de Orçamento e Finanças", "subordinadoA": "Comando de Gestão de Recursos", "requisito": "Oficial QOBM", "desdobramentos": [], "atribuicoes": ["Coordenação e execução orçamentária e financeira (Art. 18, IV)."]}]
    },
    "dsas-to": {
      "name": "Diretoria de Saúde e Assistência Social", "abbreviation": "DSAS", "category": "Direção Setorial",
      "subordinadoA": "Comando de Gestão de Pessoas", "legalRef": "Art. 18, V LC 131/2021",
      "baseLegal": "Lei Complementar nº 131, de 30 de setembro de 2021",
      "artigosDeOrigem": ["Art. 18, V (Diretoria de Saúde e Assistência Social)"],
      "atribuicoes": [
        "responsável pela coordenação, execução e acompanhamento dos assuntos relativos aos serviços de saúde e à promoção social dos bombeiros militares, seus dependentes e pensionistas, compreendendo: policlínica; consultórios médicos, odontológicos, psicológicos e de assistência social das unidades; fisioterapia; junta médica; educação física; Capelania Militar. (Art. 18, V)"
      ],
      "desdobramentos": ["Policlínica", "Consultórios médicos, odontológicos, psicológicos e de assistência social", "Fisioterapia", "Junta médica", "Educação física", "Capelania Militar"],
      "cargos": [{"cargo": "Diretor de Saúde e Assistência Social", "subordinadoA": "Comando de Gestão de Pessoas", "requisito": "Oficial QOBM/S", "desdobramentos": [], "atribuicoes": ["Coordenação dos serviços de saúde e promoção social dos BMs e dependentes (Art. 18, V)."]}]
    },
    "dst-to": {
      "name": "Diretoria de Serviços Técnicos", "abbreviation": "DST", "category": "Direção Setorial",
      "subordinadoA": "Comando de Atividades Técnicas", "legalRef": "Art. 18, VI LC 131/2021",
      "baseLegal": "Lei Complementar nº 131, de 30 de setembro de 2021",
      "artigosDeOrigem": ["Art. 18, VI (Diretoria de Serviços Técnicos)"],
      "atribuicoes": [
        "responsável pela coordenação da área de prevenção contra incêndio e emergência. (Art. 18, VI)"
      ],
      "desdobramentos": [],
      "cargos": [{"cargo": "Diretor de Serviços Técnicos", "subordinadoA": "Comando de Atividades Técnicas", "requisito": "Oficial QOBM", "desdobramentos": [], "atribuicoes": ["Coordenação da área de prevenção contra incêndio e emergência (Art. 18, VI)."]}]
    },
    "ag-to": {
      "name": "Ajudância Geral", "abbreviation": "AjG", "category": "Apoio",
      "subordinadoA": "Comandante-Geral", "legalRef": "Art. 21, I LC 131/2021",
      "baseLegal": "Lei Complementar nº 131, de 30 de setembro de 2021",
      "artigosDeOrigem": ["Art. 21, I (Ajudância Geral)"],
      "atribuicoes": [
        "subordinada ao Comandante-Geral, encarregada dos assuntos administrativos de segurança e manutenção das instalações físicas do Quartel do Comando Geral, considerado como Organização Bombeiro Militar - OBM e de apoio às unidades do Comando-Geral com pessoal auxiliar. (Art. 21, I)"
      ],
      "desdobramentos": [],
      "cargos": [{"cargo": "Ajudante-Geral", "subordinadoA": "Comandante-Geral", "requisito": "Oficial QOBM", "desdobramentos": [], "atribuicoes": ["Assuntos administrativos de segurança e manutenção das instalações do Quartel do CG (Art. 21, I)."]}]
    },
    "acad-to": {
      "name": "Academia de Formação de Bombeiros", "abbreviation": "AFBM", "category": "Apoio",
      "subordinadoA": "Diretoria de Ensino e Pesquisa", "legalRef": "Art. 21, II LC 131/2021",
      "baseLegal": "Lei Complementar nº 131, de 30 de setembro de 2021",
      "artigosDeOrigem": ["Art. 21, II (Academia de Formação de Bombeiros)"],
      "atribuicoes": [
        "subordinada à Diretoria de Ensino e Pesquisa, responsável pela formação, aperfeiçoamento, habilitação e especialização dos militares da Corporação e de coirmãs. (Art. 21, II)"
      ],
      "desdobramentos": [],
      "cargos": [{"cargo": "Comandante da Academia", "subordinadoA": "Diretoria de Ensino e Pesquisa", "requisito": "Oficial QOBM", "desdobramentos": [], "atribuicoes": ["Formação, aperfeiçoamento, habilitação e especialização dos militares do CBMTO (Art. 21, II)."]}]
    },
    "ap-to": {
      "name": "Assessoria Parlamentar", "abbreviation": "AP", "category": "Apoio",
      "subordinadoA": "Comandante-Geral", "legalRef": "Art. 21, IV LC 131/2021",
      "baseLegal": "Lei Complementar nº 131, de 30 de setembro de 2021",
      "artigosDeOrigem": ["Art. 21, IV (Assessoria Parlamentar)"],
      "atribuicoes": [
        "Assessoria Parlamentar, subordinada ao Comandante-Geral. (Art. 21, IV)"
      ],
      "desdobramentos": [],
      "cargos": [{"cargo": "Chefe da Assessoria Parlamentar", "subordinadoA": "Comandante-Geral", "requisito": "Oficial QOBM", "desdobramentos": [], "atribuicoes": ["Assessoramento parlamentar ao Comandante-Geral (Art. 21, IV)."]}]
    },
    "ubm-to": {
      "name": "Unidades Bombeiro Militares", "abbreviation": "UBM", "category": "Execução",
      "subordinadoA": "Comando Operacional Bombeiro Militar", "legalRef": "Art. 23; Art. 24 LC 131/2021",
      "baseLegal": "Lei Complementar nº 131, de 30 de setembro de 2021",
      "artigosDeOrigem": ["Art. 23 (Órgãos de Execução)", "Art. 24 (UBMs)"],
      "atribuicoes": [
        "As Unidades Administrativas de Execução são constituídas pelas unidades operacionais e realizam as atividades-fim do CBMTO, executando as diretrizes e ordens emanadas das unidades de Direção, amparadas pelas Unidades de Apoio. (Art. 23)",
        "As Unidades Administrativas de Execução, subordinadas ao Comando Operacional, são constituídas por Unidades Bombeiro Militares - UBM, encarregadas de executar as atividades-fim da Corporação em determinada área, conforme Plano de Articulação do CBMTO, podendo ser divididas em subunidades. (Art. 24)"
      ],
      "desdobramentos": ["Batalhões", "Companhias Independentes", "Companhias Destacadas", "Companhias Incorporadas", "Pelotões", "Grupos"],
      "cargos": [{"cargo": "Comandante de UBM", "subordinadoA": "Comando Operacional Bombeiro Militar", "requisito": "Oficial QOBM", "desdobramentos": [], "atribuicoes": ["Execução das atividades-fim da Corporação em determinada área (Art. 24)."]}]
    }
  }
},

}
