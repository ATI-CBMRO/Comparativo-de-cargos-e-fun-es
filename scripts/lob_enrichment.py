"""
lob_enrichment.py — Portal CBM

Camada CURADA da LOB para o comparativo /comparar (coluna "LOB do estado" e
parte "LOB" da coluna compilada). Para cada (organ_key, estado), a finalidade
e/ou os incisos VERBATIM que a Lei de Organização Básica do estado dá ao órgão,
com citação da fonte. Diferente de minuta_enrichment.ENRICHMENT_ORGAN (que é RI):
aqui é só LOB, e admite a finalidade/caput (1 frase) além de incisos.

Consumido por build_minuta_comparison.py. NÃO altera organs_detail nem ENRICHMENT_ORGAN.
"""

# LOB_ENRICHMENT[(organ_key, state_id)] -> entrada verbatim da LOB.
LOB_ENRICHMENT = {
    ("dp", "sc"): {
        "finalidade": (
            "A Diretoria de Pessoal, órgão de direção setorial, incumbe-se de planejar, "
            "coordenar, fiscalizar, controlar e executar a política de pessoal da Instituição"
        ),
        "competencias": [
            "controlar todas as atividades relacionadas com a vida funcional do pessoal "
            "militar e civil da Corporação, mantendo registros individuais",
            "promover a seleção para o ingresso no CBMSC e para admissão de pessoal civil, "
            "bem como o serviço de identificação",
            "executar as atividades relativas ao pagamento, alterações e demais encargos "
            "relativos ao pessoal ativo, inativo, pensionista e civil",
            "executar as atividades pertinentes à documentação do pessoal do CBMSC",
            "desenvolver os planos e baixar as ordens decorrentes das diretrizes da política "
            "de pessoal da Corporação",
            "propor a movimentação de Oficiais ao Comandante-Geral, e a de Praças ao "
            "Subcomandante-Geral",
            "preparar os atos de movimentação, classificação e nomeação de Oficiais",
            "preparar os atos de movimentação, classificação e designação de Praças e Civis",
            "manter ligação através do Comandante-Geral com os órgãos do Exército Brasileiro, "
            "relacionados com o controle do pessoal bombeiro militar",
            "estudar e instruir os processos administrativos e submetê-los à consideração do "
            "Chefe do Estado-Maior Geral em que lhe extrapolarem à competência",
            "manter o controle do pessoal agregado, excluído e licenciado",
            "atualizar a cada promoção os Almanaques de Oficiais, Subtenentes, Sargentos, "
            "Cabos e Soldados",
            "elaborar a documentação da Comissão de Promoção de Oficiais e Comissão de "
            "Promoção de Praças",
            "elaborar os processos de concessão de medalhas",
            "coordenar e controlar a execução do plano de férias da Corporação",
            "coletar dados e realizar inspeção de caráter setorial, visando à elaboração de "
            "estudos e propostas de medidas a serem submetidas ao Chefe do Estado-Maior Geral, "
            "para a melhoria e aperfeiçoamento do sistema de administração de pessoal",
            "elaborar estatísticas e relatórios das atividades da Diretoria",
            "manter e operacionalizar o funcionamento das comissões permanentes e de mérito",
            "planejar, orientar, coordenar, controlar e fiscalizar as atividades de saúde "
            "ocupacional, segurança do trabalho, assistência médica, odontológica e psicológica "
            "do pessoal do CBMSC e de seus dependentes",
        ],
        "source": "cf. CBMSC, LOB (Dec. nº 1.328/2021), Art. 34",
        "organName": "Diretoria de Pessoal", "abbr": "DP",
    },
    ("cg", "sc"): {
        "finalidade": "",
        "competencias": [
            "concessão de medalha, condecoração e comenda",
            "movimentação de Oficial",
            "desenvolvimento funcional das Praças pela progressão por antiguidade e por merecimento",
            "assinatura de convênios com municípios, relativos à prestação de serviços de "
            "bombeiro militar e outras atividades consideradas por LEI de competência do CBMSC",
            "agregação e reversão de Praças e Oficiais do CBMSC",
            "exclusão do serviço ativo das Praças",
            "convocação e dispensa de Oficial da Reserva Remunerada do CBMSC para compor "
            "Conselho Especial de Justiça ou Conselho de Justificação, ambos encarregados de "
            "inquérito policial-militar, ou para outros procedimentos administrativos na falta "
            "de oficial da ativa em situação hierárquica compatível com a do oficial envolvido",
            "assinatura de termos de cooperação técnica e convênios com órgãos cujo objeto "
            "seja de interesse da Corporação",
            "designação e respectiva dispensa dos servidores inativos ao Corpo Temporário de "
            "Inativos da Segurança Pública (CTISP), após autorização do Grupo Gestor de Governo (GGG)",
        ],
        "source": "cf. CBMSC, LOB (Dec. nº 1.328/2021), Art. 14",
        "organName": "Comando-Geral", "abbr": "CmdoG",
    },
    ("dp", "go"): {
        "finalidade": "",
        "competencias": [
            "planejar, controlar e executar as atividades relacionadas com pessoal",
            "promover as atividades inerentes ao pagamento de militares, civis e fornecedores",
            "praticar atos inerentes à execução financeira e contábil",
            "elaborar normas internas sobre gestão de pessoal e financeira",
            "planejar e fiscalizar as atividades relacionadas a segurança e medicina do trabalho",
            "elaborar boletins gerais",
        ],
        "source": "cf. CBMGO, LOB (Lei nº 18.305/2013), Art. 26",
        "organName": "Comando de Gestão e Finanças", "abbr": "",
    },
    ("cg", "go"): {
        "finalidade": (
            "O órgão de direção geral, representado pelo Comando Geral, é encarregado do "
            "planejamento e organização geral da Corporação, visando ao emprego estratégico "
            "de pessoal e material no âmbito da Instituição, cabendo-lhe ainda a fiscalização "
            "e o controle dos órgãos de direção setorial, de apoio e execução"
        ),
        "competencias": [],
        "source": "cf. CBMGO, LOB (Lei nº 18.305/2013), Art. 9",
        "organName": "Comando Geral", "abbr": "",
    },

    # =====================================================================
    # Lote 1 — AC, AL, AM, AP, BA (camada LOB /comparar, 2026-06-28)
    # =====================================================================

    # --- Acre (CBMAC) — Lei nº 2.009/2008 (alt. Lei nº 4.428/2024) ---
    # LOB enxuta/estrutural: descreve poucos órgãos por finalidade; Art. 22 (red.
    # Lei 3.105/2015) remete competências/atribuições dos demais órgãos a instruções
    # normativas do comandante-geral. (cg) usa a atribuição do comandante-geral (cargo).
    ("cg", "ac"): {
        "finalidade": (
            "Compete ao comandante-geral da corporação, dentre outras atribuições, "
            "planejar, coordenar, fiscalizar, controlar e orientar todas as atividades do "
            "CBMAC e centralizar o planejamento administrativo e a programação orçamentária, "
            "podendo delegar estas últimas"
        ),
        "competencias": [],
        "source": "cf. CBMAC, LOB (Lei nº 2.009/2008), Art. 6º",
        "organName": "Comando Geral", "abbr": "",
    },
    ("assessorias", "ac"): {
        "finalidade": (
            "As assessorias do comando geral destinam-se a apoiar o comandante-geral da "
            "corporação em assuntos especializados, podendo ser preenchidas por pessoal civil"
        ),
        "competencias": [],
        "source": "cf. CBMAC, LOB (Lei nº 2.009/2008), Art. 10",
        "organName": "Assessorias do Comando Geral", "abbr": "",
    },
    ("ag", "ac"): {
        "finalidade": (
            "À ajudância geral compete, dentre outras atribuições, a administração, a "
            "segurança e os serviços gerais, dando suporte e apoio em efetivo aos órgãos "
            "sediados no quartel do comando geral"
        ),
        "competencias": [],
        "source": "cf. CBMAC, LOB (Lei nº 2.009/2008), Art. 11",
        "organName": "Ajudância Geral", "abbr": "",
    },
    ("corregedoria", "ac"): {
        "finalidade": (
            "A corregedoria do CBMAC é o órgão responsável pelo sistema administrativo "
            "disciplinar do CBMAC e dos procedimentos de polícia judiciária militar e todos "
            "os seus atos serão validados pelo subcomandante da corporação"
        ),
        "competencias": [],
        "source": "cf. CBMAC, LOB (Lei nº 2.009/2008), Art. 8º",
        "organName": "Corregedoria do CBMAC", "abbr": "",
    },

    # --- Alagoas (CBMAL) — Lei nº 7.444/2012 ---
    ("cg", "al"): {
        "finalidade": (
            "O Comando Geral da Corporação compete ao Comandante Geral do Corpo de Bombeiros "
            "Militar do Estado de Alagoas, responsável pelo comando e a administração da "
            "instituição, bem como a coordenação geral das ações de Defesa Civil no Estado de "
            "Alagoas"
        ),
        "competencias": [],
        "source": "cf. CBMAL, LOB (Lei nº 7.444/2012), Art. 6º",
        "organName": "Comando Geral", "abbr": "",
    },
    ("gab-cg", "al"): {
        "finalidade": (
            "Ao Gabinete do Comandante Geral compete as funções de assistência e "
            "assessoramento direto ao Comandante Geral na prática de atos de gestão e nos "
            "assuntos que escapem às atribuições normais e específicas dos demais órgãos de "
            "direção"
        ),
        "competencias": [],
        "source": "cf. CBMAL, LOB (Lei nº 7.444/2012), Art. 9º",
        "organName": "Gabinete do Comando Geral", "abbr": "",
    },
    ("condeg", "al"): {
        "finalidade": (
            "O Conselho de Políticas Estratégicas é um colegiado encarregado de assessorar ao "
            "Comandante Geral na formulação e avaliação de políticas estratégicas e na fixação "
            "de diretrizes de gerenciamento administrativo e de emprego do Corpo de Bombeiros "
            "Militar para o cumprimento de suas missões"
        ),
        "competencias": [],
        "source": "cf. CBMAL, LOB (Lei nº 7.444/2012), Art. 11",
        "organName": "Conselho de Políticas Estratégicas", "abbr": "",
    },
    ("depdec", "al"): {
        "finalidade": (
            "A Coordenadoria Estadual de Defesa Civil é órgão de coordenação central do "
            "Sistema Estadual de Defesa Civil, competindo-lhe o estudo, o planejamento, a "
            "orientação técnica, a coordenação, a supervisão, a execução, o controle e a "
            "avaliação das ações de defesa civil no Estado de Alagoas, observando o disposto "
            "na Lei nº 6.171, de 31 de julho de 2000"
        ),
        "competencias": [],
        "source": "cf. CBMAL, LOB (Lei nº 7.444/2012), Art. 12",
        "organName": "Coordenadoria Estadual de Defesa Civil", "abbr": "",
    },
    ("corregedoria", "al"): {
        "finalidade": (
            "A Corregedoria Geral do Corpo de Bombeiros Militar é o órgão de direção "
            "encarregado da orientação, fiscalização e correção dos procedimentos relativos à "
            "apuração das transgressões disciplinares e das infrações penais militares dos "
            "Bombeiros Militares, promovendo-lhes, ainda, a responsabilidade funcional e "
            "disciplinar"
        ),
        "competencias": [],
        "source": "cf. CBMAL, LOB (Lei nº 7.444/2012), Art. 13",
        "organName": "Corregedoria Geral", "abbr": "",
    },
    ("dp", "al"): {
        "finalidade": (
            "A Diretoria de Recursos Humanos é o órgão central do sistema de recursos humanos "
            "do Corpo de Bombeiros Militar, competindo-lhe o estudo, o planejamento, a "
            "orientação normativa, a coordenação, a supervisão, o controle e a execução das "
            "atividades relativas à gestão de pessoal e desenvolvimento de recursos humanos da "
            "Corporação, de acordo com as diretrizes da Secretaria de Estado da Gestão "
            "Pública - SEGESP"
        ),
        "competencias": [],
        "source": "cf. CBMAL, LOB (Lei nº 7.444/2012), Art. 15",
        "organName": "Diretoria de Recursos Humanos", "abbr": "DRH",
    },
    ("dlog", "al"): {
        "finalidade": (
            "A Diretoria de Material e Patrimônio é o órgão central do sistema logístico do "
            "Corpo de Bombeiros Militar, competindo-lhe o estudo, o planejamento, a orientação "
            "normativa, a coordenação, a supervisão, o controle e a execução das atividades "
            "relativas à gestão do material e patrimônio da Corporação"
        ),
        "competencias": [],
        "source": "cf. CBMAL, LOB (Lei nº 7.444/2012), Art. 16",
        "organName": "Diretoria de Material e Patrimônio", "abbr": "",
    },
    ("dpof", "al"): {
        "finalidade": (
            "A Diretoria de Finanças é o órgão central do sistema de administração financeira "
            "do Corpo de Bombeiros Militar, competindo-lhe o estudo, o planejamento, a "
            "orientação normativa, a coordenação, a supervisão, o controle e a execução das "
            "atividades relativas à gestão financeira, ao planejamento e execução "
            "orçamentária, à contabilidade e auditoria"
        ),
        "competencias": [],
        "source": "cf. CBMAL, LOB (Lei nº 7.444/2012), Art. 17",
        "organName": "Diretoria de Finanças", "abbr": "",
    },
    ("cot", "al"): {
        "finalidade": (
            "A Diretoria de Atividades Técnicas é o órgão central do sistema de engenharia e "
            "segurança do Corpo de Bombeiros Militar, competindo-lhe o estudo, a análise, o "
            "planejamento, a orientação técnica, a execução, o controle e a fiscalização das "
            "atividades relativas à segurança contra incêndio e pânico e ao cumprimento das "
            "disposições legais sobre o assunto, no âmbito do Estado de Alagoas"
        ),
        "competencias": [],
        "source": "cf. CBMAL, LOB (Lei nº 7.444/2012), Art. 18",
        "organName": "Diretoria de Atividades Técnicas", "abbr": "",
    },
    ("dpo", "al"): {
        "finalidade": (
            "A Diretoria de Planejamento e Orçamento é o órgão central do sistema de "
            "Planejamento Estratégico e Orçamentário do Corpo de Bombeiros Militar, "
            "competindo-lhe a coordenação do planejamento, a orientação técnica, o "
            "monitoramento, o controle e a fiscalização das atividades relativas ao "
            "planejamento estratégico, bem como a elaboração e execução do orçamento da "
            "Corporação"
        ),
        "competencias": [],
        "source": "cf. CBMAL, LOB (Lei nº 7.444/2012), Art. 19",
        "organName": "Diretoria de Planejamento e Orçamento", "abbr": "",
    },
    ("deei", "al"): {
        "finalidade": (
            "A Diretoria de Ensino é o órgão de apoio do sistema de ensino da Corporação, "
            "incumbindo-lhe, o estudo, o planejamento, a supervisão e o controle das "
            "atividades de ensino e capacitação profissional da Instituição"
        ),
        "competencias": [],
        "source": "cf. CBMAL, LOB (Lei nº 7.444/2012), Art. 20",
        "organName": "Diretoria de Ensino", "abbr": "",
    },
    ("ag", "al"): {
        "finalidade": (
            "A Secretaria Geral é o órgão de direção encarregado da administração do Quartel "
            "do Comando Geral, considerado como Organização Bombeiro Militar, bem como do "
            "expediente, da execução dos trabalhos de secretaria, incluindo a correspondência, "
            "correio, redação e impressão do boletim diário, do protocolo e arquivo geral e "
            "biblioteca, do apoio em pessoal aos órgãos que compõem o Comando Geral, dos "
            "serviços gerais, da banda de música e da segurança do Quartel do Comando Geral"
        ),
        "competencias": [],
        "source": "cf. CBMAL, LOB (Lei nº 7.444/2012), Art. 21",
        "organName": "Secretaria Geral", "abbr": "",
    },
    ("cinf", "al"): {
        "finalidade": (
            "O Centro de Tecnologia em Informática e Informação é o órgão que gerencia e "
            "administra os recursos tecnológicos e computacionais de geração e uso da "
            "informação como também todo o parque de informática do Corpo de Bombeiros "
            "Militar, subordinado ao Subcomandante Geral, encarregado de desenvolver e manter "
            "sistemas informatizados, para as áreas administrativa, operacional, internet e "
            "intranet da Corporação, dar suporte tecnológico e apoio ao usuário, provendo "
            "informações de planejamento e avaliação da gestão pública"
        ),
        "competencias": [],
        "source": "cf. CBMAL, LOB (Lei nº 7.444/2012), Art. 25",
        "organName": "Centro de Tecnologia de Informática e Informação", "abbr": "",
    },
    ("dsap", "al"): {
        "finalidade": (
            "O Centro de Assistência é o órgão de apoio do sistema de recursos humanos, "
            "subordinado ao Subcomandante Geral, incumbido do suporte ao sistema de "
            "atendimento pré-hospitalar, do estudo, planejamento, a supervisão, a execução e o "
            "controle das atividades de assistência médica, odontológica, farmacêutica, "
            "sanitária, religiosa e de assistência social aos Bombeiros Militares e seus "
            "dependentes, na forma da legislação em vigor"
        ),
        "competencias": [],
        "source": "cf. CBMAL, LOB (Lei nº 7.444/2012), Art. 26",
        "organName": "Centro de Assistência", "abbr": "",
    },
    ("crbm", "al"): {
        "finalidade": (
            "Comando Operacional de Bombeiros é a denominação genérica dada a Organização "
            "Bombeiro-Militar de mais alto escalão do sistema operacional, subordinado ao "
            "Subcomandante Geral, que tem a seu cargo o planejamento estratégico, a "
            "coordenação e o emprego das Unidades Operacionais da Corporação que lhe forem "
            "subordinadas, com a finalidade de executar as missões de prevenção e extinção de "
            "incêndios, de resgate, busca e salvamento, de atendimento aos traumas e "
            "emergências pré-hospitalares e de defesa civil, além de outras, em uma "
            "determinada área operacional"
        ),
        "competencias": [],
        "source": "cf. CBMAL, LOB (Lei nº 7.444/2012), Art. 30",
        "organName": "Comando Operacional de Bombeiros", "abbr": "",
    },
    ("gbm", "al"): {
        "finalidade": (
            "Os Grupamentos de Bombeiros Militar, subordinados aos Comandos Operacionais de "
            "Área, têm a seu cargo, dentro de sua área de atuação operacional, as missões de "
            "prevenção e extinção de incêndios, busca e salvamento, atendimento "
            "pré-hospitalar, emergências com produtos perigosos, bem como disporão de uma "
            "Seção de Atividades Técnicas para a execução dos trabalhos de análise de "
            "projetos, vistorias e pareceres técnicos em edificações e locais de risco, além "
            "de contar com uma Seção de Defesa Civil"
        ),
        "competencias": [],
        "source": "cf. CBMAL, LOB (Lei nº 7.444/2012), Art. 34",
        "organName": "Grupamento de Bombeiros Militar", "abbr": "GBM",
    },
    ("bbs", "al"): {
        "finalidade": (
            "O Grupamento de Busca e Salvamento tem a seu cargo, dentro de uma determinada "
            "área de atuação operacional, as missões de busca, salvamento em altura e "
            "terrestre, resgate e outras voltadas para as missões de salvamento terrestre"
        ),
        "competencias": [],
        "source": "cf. CBMAL, LOB (Lei nº 7.444/2012), Art. 38",
        "organName": "Grupamento de Busca e Salvamento", "abbr": "GBS",
    },
    ("bifea", "al"): {
        "finalidade": (
            "O Grupamento de Proteção Ambiental tem a seu cargo, dentro de uma determinada "
            "área de atuação operacional, as missões de prevenção, combate a incêndios "
            "florestais, preservação de áreas ambientais, seus recursos hídricos, salvamento "
            "de animais silvestres, dentre outras voltadas para a proteção e preservação da "
            "fauna e da flora"
        ),
        "competencias": [],
        "source": "cf. CBMAL, LOB (Lei nº 7.444/2012), Art. 39",
        "organName": "Grupamento de Proteção Ambiental", "abbr": "GPA",
    },
    ("boa", "al"): {
        "finalidade": (
            "O Grupamento de Operações Aéreas tem a seu cargo, dentro de uma determinada área "
            "de atuação operacional, as missões, por meio aéreo, de socorro de urgência, "
            "extricação de presos em ferragens, combate a incêndios florestais, salvamentos e "
            "resgate, dentre outras atividades aéreas correlatas, além de dispor de uma "
            "assessoria de segurança de voo"
        ),
        "competencias": [],
        "source": "cf. CBMAL, LOB (Lei nº 7.444/2012), Art. 40",
        "organName": "Grupamento de Operações Aéreas", "abbr": "GOA",
    },

    # --- Amazonas (CBMAM) — Lei nº 2.538/1999 ---
    ("cg", "am"): {
        "finalidade": (
            "O Comandante Geral do Corpo de Bombeiros Militar do Estado do Amazonas é "
            "responsável pelo comando, administração e emprego da Corporação"
        ),
        "competencias": [],
        "source": "cf. CBMAM, LOB (Lei nº 2.538/1999), Art. 9º",
        "organName": "Comando Geral", "abbr": "",
    },
    ("gab-cg", "am"): {
        "finalidade": (
            "O Gabinete do Comando-Geral tem a seu cargo as funções de assistência e "
            "assessoramento direto ao Comandante Geral nos assuntos que refogem às atribuições "
            "normais e específicas dos demais órgãos de direção"
        ),
        "competencias": [],
        "source": "cf. CBMAM, LOB (Lei nº 2.538/1999), Art. 16",
        "organName": "Gabinete do Comando-Geral", "abbr": "",
    },
    ("depdec", "am"): {
        "finalidade": (
            "A Coordenadoria Estadual de Defesa Civil (CEDEC) órgão de direção geral, "
            "centraliza o Sistema Estadual de Defesa Civil e tem por finalidade estabelecer "
            "normas e o exercício das atividades de integrar, planejar, organizar, coordenar e "
            "supervisionar a execução das medidas preventivas de socorro, de assistência e de "
            "recuperação, considerando os efeitos produzidos por fatos adversos de qualquer "
            "natureza e nas situações de emergência ou estado de calamidade pública"
        ),
        "competencias": [],
        "source": "cf. CBMAM, LOB (Lei nº 2.538/1999), Art. 14",
        "organName": "Coordenadoria Estadual de Defesa Civil", "abbr": "CEDEC",
    },
    ("condeg", "am"): {
        "finalidade": (
            "O Conselho Superior de Políticas Estratégicas (CSPE), constituído pelo Comandante "
            "Geral, Subcomandante Geral, Comandantes de Bombeiros da Capital e do Interior e "
            "Diretores Setoriais, reunir-se-á, eventualmente, por convocação do Comandante "
            "Geral, ou em datas por ele prefixadas e, terá suas atribuições definidas no "
            "Regimento Interno da Corporação"
        ),
        "competencias": [],
        "source": "cf. CBMAM, LOB (Lei nº 2.538/1999), Art. 15",
        "organName": "Conselho Superior de Políticas Estratégicas", "abbr": "CSPE",
    },
    ("ag", "am"): {
        "finalidade": (
            "A Ajudância Geral (AG) é o órgão responsável pelas funções administrativas do "
            "Comando Geral"
        ),
        "competencias": [
            "trabalhos de secretaria, inclusive correspondências, correios, protocolo geral, "
            "arquivo geral e boletim geral",
            "serviço de embarque da Corporação",
            "apoio de pessoal auxiliar (militar e civil) aos órgãos do Comando Geral",
            "serviços gerais",
            "segurança do Quartel do Comando Geral",
        ],
        "source": "cf. CBMAM, LOB (Lei nº 2.538/1999), Art. 18",
        "organName": "Ajudância Geral", "abbr": "AG",
    },
    ("dp", "am"): {
        "finalidade": (
            "A Diretoria de Recursos Humanos (DRH) é o órgão de direção setorial responsável "
            "pelo planejamento, controle e fiscalização das atividades relacionadas com "
            "políticas de pessoal, da admissão, da capacitação técnica, da assistência "
            "psicológica, social, jurídica e religiosa, pela remuneração do pessoal e pela "
            "prevenção de acidentes no trabalho"
        ),
        "competencias": [],
        "source": "cf. CBMAM, LOB (Lei nº 2.538/1999), Art. 21",
        "organName": "Diretoria de Recursos Humanos", "abbr": "DRH",
    },
    ("dpof", "am"): {
        "finalidade": (
            "A Diretoria de Finanças (DF) é o órgão de direção setorial responsável pelas "
            "atividades específicas da gestão orçamentária e financeira, supervisão destas "
            "junto aos demais órgãos da Corporação, controle de repasse de recursos "
            "orçamentários e captação de recursos financeiros, de acordo com o planejamento "
            "estabelecido"
        ),
        "competencias": [],
        "source": "cf. CBMAM, LOB (Lei nº 2.538/1999), Art. 23",
        "organName": "Diretoria de Finanças", "abbr": "DF",
    },
    ("dlog", "am"): {
        "finalidade": (
            "A Diretoria de Logística (DL) é o órgão de direção setorial responsável pelo "
            "planejamento, coordenação, fiscalização e controle das atividades de suprimento e "
            "material da Corporação, além da elaboração de convênios e atividades de saúde"
        ),
        "competencias": [],
        "source": "cf. CBMAM, LOB (Lei nº 2.538/1999), Art. 25",
        "organName": "Diretoria de Logística", "abbr": "DL",
    },
    ("deei", "am"): {
        "finalidade": (
            "A Diretoria de Ensino, Instrução, Pesquisa e Operações (DEIPO) é o órgão de "
            "direção setorial responsável pela coordenação, fiscalização, controle das "
            "atividades de ensino, instrução, pesquisa e pelo planejamento operacional da "
            "Corporação"
        ),
        "competencias": [],
        "source": "cf. CBMAM, LOB (Lei nº 2.538/1999), Art. 27",
        "organName": "Diretoria de Ensino, Instrução, Pesquisa e Operações", "abbr": "DEIPO",
    },
    ("cot", "am"): {
        "finalidade": (
            "A Diretoria de Serviços Técnicos (DST) é o órgão de direção setorial incumbido de "
            "estudar, analisar, planejar, exigir, fiscalizar as atividades atinentes à "
            "prevenção e segurança contra incêndios e pânico, além de proceder testes, exames "
            "de plantas, perícias de incêndio e explosão, a realizar vistorias e emitir "
            "pareceres e supervisionar a instalação de hidrantes na rede pública"
        ),
        "competencias": [],
        "source": "cf. CBMAM, LOB (Lei nº 2.538/1999), Art. 29",
        "organName": "Diretoria de Serviços Técnicos", "abbr": "DST",
    },
    ("cinf", "am"): {
        "finalidade": (
            "O Centro de Informática (CInf), órgão de apoio, subordinado diretamente à "
            "Diretoria de Ensino, Instrução, Pesquisa e Operações (DEIPO), destina-se a "
            "realizar programas e sistemas para a otimização das áreas administrativas e "
            "operacionais da Corporação"
        ),
        "competencias": [],
        "source": "cf. CBMAM, LOB (Lei nº 2.538/1999), Art. 37",
        "organName": "Centro de Informática", "abbr": "CInf",
    },
    ("crbm", "am"): {
        "finalidade": (
            "O Comando de Bombeiros da Capital (CBC) e o Comando de Bombeiros do Interior "
            "(CBI), órgãos de execução, subordinados ao Subcomandante Geral, destinam-se ao "
            "planejamento estratégico, à coordenação, à fiscalização e ao emprego das Unidades "
            "e Sub-unidades que lhe forem subordinadas, com a finalidade de executar "
            "atividades de prevenção, combate a incêndio, busca e salvamento, atendimento de "
            "socorros de emergência e defesa civil, além de outras atividades previstas em lei"
        ),
        "competencias": [],
        "source": "cf. CBMAM, LOB (Lei nº 2.538/1999), Art. 45",
        "organName": "Comando de Bombeiros da Capital e do Interior", "abbr": "CBC/CBI",
    },
    ("bbm", "am"): {
        "finalidade": (
            "O Batalhão de Incêndio (BI), unidade operacional, órgão de execução, subordinado "
            "ao Comando de Bombeiros da Capital (CBC) ou Comando de Bombeiros do Interior "
            "(CBI), destina-se à coordenação, ao controle, à fiscalização e à execução de "
            "atividade operacional e administrativa em sua área de atuação"
        ),
        "competencias": [],
        "source": "cf. CBMAM, LOB (Lei nº 2.538/1999), Art. 48",
        "organName": "Batalhão de Incêndio", "abbr": "BI",
    },
    ("bifea", "am"): {
        "finalidade": (
            "O Batalhão de Incêndio Florestal e Meio Ambiente (BIF/MA), unidade operacional, "
            "órgão de execução, subordinado ao Comando Operacional do Interior, destina-se à "
            "prevenção e combate a incêndio florestal e queimadas e socorro ao meio ambiente, "
            "em conformidade com a lei"
        ),
        "competencias": [],
        "source": "cf. CBMAM, LOB (Lei nº 2.538/1999), Art. 52",
        "organName": "Batalhão de Incêndio Florestal e Meio Ambiente", "abbr": "BIF/MA",
    },

    # --- Amapá (CBMAP) — Lei Complementar nº 180/2026 ---
    # LOB nova e enxuta: Art. 6º remete a estrutura/atribuições de cada órgão a decreto
    # ("definidas por ato do Governador"). Só descreve órgãos por CATEGORIA (§§ do Art. 6º);
    # as Diretorias/Centros não têm finalidade individual. (cg) usa a finalidade da
    # direção-geral; (corregedoria) usa a finalidade dos órgãos de correição (§5º).
    ("cg", "ap"): {
        "finalidade": (
            "os órgãos de direção-geral, responsáveis pela direção superior, planejamento "
            "estratégico e administração geral da Instituição, compostos pelo Gabinete do "
            "Comandante-Geral, Gabinete do Subcomandante-Geral, Comitê de Desenvolvimento "
            "Organizacional, Comando Operacional e Fundo de Reequipamento do Corpo de Bombeiros"
        ),
        "competencias": [],
        "source": "cf. CBMAP, LOB (LC nº 180/2026), Art. 6º, § 1º, I",
        "organName": "Órgãos de Direção-Geral", "abbr": "",
    },
    ("corregedoria", "ap"): {
        "finalidade": (
            "Os órgãos de correição, com atuação desconcentrada, destinam-se a exercer as "
            "funções de Corregedoria-Geral, mediante regulamentação de procedimentos internos, "
            "para a prevenção, fiscalização e apuração dos desvios de conduta em atos "
            "disciplinares e penais militares, a promoção da qualidade e eficiência do serviço "
            "de segurança pública e a instrumentalização da Justiça Militar, bem como a "
            "acompanhar o cumprimento de quaisquer medidas cautelares restritivas de direitos "
            "e mandados de prisão judicialmente deferidos em desfavor de militares dentro da "
            "instituição, sem suprimir a responsabilidade do poder hierárquico e disciplinar "
            "de outras autoridades"
        ),
        "competencias": [],
        "source": "cf. CBMAP, LOB (LC nº 180/2026), Art. 6º, § 5º",
        "organName": "Órgãos de Correição (Corregedoria-Geral)", "abbr": "",
    },

    # --- Bahia (CBMBA) — Lei nº 14.572/2023 ---
    # LOB moderna que dá finalidade ("tem por finalidade") a quase todos os órgãos; Art. 7º
    # §2º remete a estrutura interna e competências de detalhe a Regimento (Decreto).
    ("cg", "ba"): {
        "finalidade": (
            "O Comando-Geral é o órgão diretivo superior e estratégico que tem por finalidade "
            "planejar, dirigir, executar, avaliar, deliberar e controlar as atividades do CBMBA"
        ),
        "competencias": [],
        "source": "cf. CBMBA, LOB (Lei nº 14.572/2023), Art. 11",
        "organName": "Comando-Geral", "abbr": "",
    },
    ("gab-cg", "ba"): {
        "finalidade": (
            "O Gabinete do Comando Geral, integrante do Comando-Geral, tem por finalidade "
            "prestar assistência ao Comandante-Geral em suas atribuições técnicas e "
            "administrativas e nas relações de interesse do CBMBA com órgãos e instituições "
            "dos Poderes Executivo, Legislativo e Judiciário, em âmbito Federal, Estadual e "
            "Municipal, do Ministério Público, dos Tribunais de Contas e de Organismos "
            "Internacionais"
        ),
        "competencias": [],
        "source": "cf. CBMBA, LOB (Lei nº 14.572/2023), Art. 12",
        "organName": "Gabinete do Comando Geral", "abbr": "",
    },
    ("condeg", "ba"): {
        "finalidade": (
            "O Conselho do Corpo de Bombeiros Militar, órgão consultivo e propositivo, "
            "convocado e presidido pelo Comandante-Geral, é constituído pelos Coronéis da "
            "ativa, quando no exercício dos cargos privativos do posto de coronel previstos no "
            "quadro de organização do CBMBA, tendo como finalidade a análise e discussão sobre "
            "assuntos de relevante interesse da Corporação, ressalvada a competência do Alto "
            "Comando"
        ),
        "competencias": [],
        "source": "cf. CBMBA, LOB (Lei nº 14.572/2023), Art. 10",
        "organName": "Conselho do Corpo de Bombeiros Militar", "abbr": "",
    },
    ("dpo", "ba"): {
        "finalidade": (
            "O Comando de Operações de Bombeiros Militar tem por finalidade assessorar o "
            "Comandante-Geral e o Subcomandante-Geral, planejar, coordenar, executar, avaliar "
            "e controlar as atividades operacionais de bombeiros militares, de proteção e "
            "defesa civil, executadas pelos Comandos Regionais e pelas Unidades Operacionais, "
            "no que concerne à proteção das pessoas e dos bens públicos e privados"
        ),
        "competencias": [],
        "source": "cf. CBMBA, LOB (Lei nº 14.572/2023), Art. 16",
        "organName": "Comando de Operações de Bombeiros Militar", "abbr": "COBM",
    },
    ("boa", "ba"): {
        "finalidade": (
            "O Centro de Gestão do Vetor Aéreo, integrante do Comando de Operações de "
            "Bombeiros Militar, tem por finalidade a gestão e execução do apoio do vetor aéreo "
            "às atividades de bombeiros militares e defesa civil"
        ),
        "competencias": [],
        "source": "cf. CBMBA, LOB (Lei nº 14.572/2023), Art. 17",
        "organName": "Centro de Gestão do Vetor Aéreo", "abbr": "",
    },
    ("cot", "ba"): {
        "finalidade": (
            "O Comando de Segurança Contra Incêndio tem por finalidade planejar, avaliar e "
            "efetuar pesquisas, perícias de incêndios, vistorias, análises de projetos de "
            "proteção contra incêndios e pânico na sua área específica de atuação, emitindo os "
            "respectivos laudos, pareceres e autos de vistorias técnicas"
        ),
        "competencias": [],
        "source": "cf. CBMBA, LOB (Lei nº 14.572/2023), Art. 18",
        "organName": "Comando de Segurança Contra Incêndio", "abbr": "",
    },
    ("cint", "ba"): {
        "finalidade": (
            "A Coordenadoria de Inteligência tem por finalidade planejar, coordenar, executar, "
            "fiscalizar, controlar, articular, supervisionar e gerenciar as atividades de "
            "inteligência bombeiro militar, no âmbito do Sistema de Inteligência do Corpo de "
            "Bombeiros Militar - SINBOM, dentro do território baiano, e assessorar o Alto "
            "Comando da Corporação nos assuntos de cunho estratégico, tático e operacional que "
            "lhes forem confiados, além de se inter-relacionar com os demais órgãos estaduais "
            "de inteligência e do Sistema Brasileiro de Inteligência - SISBIN"
        ),
        "competencias": [],
        "source": "cf. CBMBA, LOB (Lei nº 14.572/2023), Art. 19",
        "organName": "Coordenadoria de Inteligência", "abbr": "",
    },
    ("corregedoria", "ba"): {
        "finalidade": (
            "A Corregedoria do Corpo de Bombeiros Militar da Bahia tem por finalidade assistir "
            "o Comandante-Geral e o Subcomandante-Geral do Corpo de Bombeiros Militar da Bahia "
            "no desempenho de suas atribuições constitucionais, políticas e administrativas, "
            "realizar a atividade correcional, zelando pela justiça e disciplina dos "
            "integrantes da Corporação e gerenciar as atividades dos segmentos de correição "
            "descentralizados do CBMBA"
        ),
        "competencias": [],
        "source": "cf. CBMBA, LOB (Lei nº 14.572/2023), Art. 20",
        "organName": "Corregedoria do Corpo de Bombeiros Militar da Bahia", "abbr": "",
    },
    ("dpof", "ba"): {
        "finalidade": (
            "O Departamento de Planejamento tem por finalidade elaborar o planejamento das "
            "políticas públicas e estratégias institucionais, orientar e executar a "
            "programação orçamentária, consolidar os planos, programas e projetos e realizar o "
            "acompanhamento e a avaliação das ações governamentais, no âmbito do CBMBA"
        ),
        "competencias": [],
        "source": "cf. CBMBA, LOB (Lei nº 14.572/2023), Art. 21",
        "organName": "Departamento de Planejamento", "abbr": "",
    },
    ("dp", "ba"): {
        "finalidade": (
            "O Departamento de Pessoal tem por finalidade planejar, organizar, coordenar e "
            "controlar as atividades de pessoal do CBMBA"
        ),
        "competencias": [],
        "source": "cf. CBMBA, LOB (Lei nº 14.572/2023), Art. 22",
        "organName": "Departamento de Pessoal", "abbr": "",
    },
    ("dlog", "ba"): {
        "finalidade": (
            "O Departamento de Apoio Logístico tem por finalidade planejar, coordenar, "
            "controlar e executar as atividades de logística e de patrimônio do CBMBA"
        ),
        "competencias": [],
        "source": "cf. CBMBA, LOB (Lei nº 14.572/2023), Art. 23",
        "organName": "Departamento de Apoio Logístico", "abbr": "",
    },
    ("cinf", "ba"): {
        "finalidade": (
            "O Departamento de Modernização e Tecnologia tem por finalidade planejar, "
            "coordenar, executar e controlar as atividades de tecnologia da informação e "
            "telecomunicações, promovendo a elevação da qualidade dos serviços e das "
            "atividades do CBMBA, em estreita articulação com os órgãos estaduais de "
            "tecnologia da informação e telecomunicações, e, por intermédio de convênios, com "
            "as demais esferas de governo"
        ),
        "competencias": [],
        "source": "cf. CBMBA, LOB (Lei nº 14.572/2023), Art. 25",
        "organName": "Departamento de Modernização e Tecnologia", "abbr": "",
    },
    ("deei", "ba"): {
        "finalidade": (
            "O Instituto Militar de Ensino Superior de Bombeiros - IMESB, instituição de "
            "ensino superior do CBMBA, tem por finalidade planejar, organizar, dirigir, "
            "controlar, avaliar e fiscalizar as atividades de ensino, instrução, extensão e "
            "pesquisa do CBMBA, emitindo diretrizes educacionais para as organizações "
            "tecnicamente subordinadas"
        ),
        "competencias": [],
        "source": "cf. CBMBA, LOB (Lei nº 14.572/2023), Art. 28",
        "organName": "Instituto Militar de Ensino Superior de Bombeiros", "abbr": "IMESB",
    },
    ("dsap", "ba"): {
        "finalidade": (
            "A Coordenadoria de Saúde tem por finalidade planejar, coordenar, controlar e "
            "executar as atividades de promoção, prevenção, tratamentos médico, psicológico e "
            "odontológico, reabilitação e recuperação dos agravos à saúde dos integrantes do "
            "CBMBA e dos seus dependentes"
        ),
        "competencias": [],
        "source": "cf. CBMBA, LOB (Lei nº 14.572/2023), Art. 32",
        "organName": "Coordenadoria de Saúde", "abbr": "",
    },
    ("crbm", "ba"): {
        "finalidade": (
            "Os Comandos Regionais de Bombeiros Militar, subordinados ao COBM, têm por "
            "finalidade planejar, coordenar, controlar, executar e avaliar as atividades "
            "operacionais de bombeiros militares de proteção e defesa civil nas regiões sob "
            "sua responsabilidade, bem como supervisionar as atividades realizadas pelas "
            "unidades operacionais respectivas, no que concerne à eficiência nas missões de "
            "bombeiro militar"
        ),
        "competencias": [],
        "source": "cf. CBMBA, LOB (Lei nº 14.572/2023), Art. 33",
        "organName": "Comandos Regionais de Bombeiros Militar", "abbr": "",
    },
    ("bbm", "ba"): {
        "finalidade": (
            "Os Batalhões de Bombeiros Militar subordinados aos seus respectivos Comandos "
            "Regionais têm por finalidade a execução das missões de bombeiro militar, e terão "
            "atuação em todo o Estado da Bahia ou em região definida em regulamento"
        ),
        "competencias": [],
        "source": "cf. CBMBA, LOB (Lei nº 14.572/2023), Art. 34",
        "organName": "Batalhões de Bombeiros Militar", "abbr": "",
    },

    # =====================================================================
    # Lote 2 — CE, DF, ES, MA, MG + completa GO (camada LOB /comparar, 2026-06-28)
    # =====================================================================

    # --- Ceará (CBMCE) — Lei nº 13.438/2004 ---
    # LOB por "competência": dá finalidade (caput) e, em vários órgãos, incisos. (cg) usa a
    # atribuição do Comandante Geral (cargo); a LOB não dá finalidade ao Comando como órgão.
    ("cg", "ce"): {
        "finalidade": (
            "O Comandante Geral, responsável pelo comando e administração da Corporação, é "
            "cargo privativo de Oficial da ativa, do quadro de Oficiais Combatentes do Corpo "
            "de Bombeiros, dentre os Oficiais no Posto de Coronel, nomeado pelo Governador do "
            "Estado"
        ),
        "competencias": [],
        "source": "cf. CBMCE, LOB (Lei nº 13.438/2004), Art. 8º",
        "organName": "Comandante Geral", "abbr": "",
    },
    ("condeg", "ce"): {
        "finalidade": (
            "O Conselho Consultivo é o Órgão Colegiado de natureza consultiva com a finalidade "
            "de assessorar o Comandante Geral em assuntos de alta relevância no cumprimento de "
            "suas missões"
        ),
        "competencias": [],
        "source": "cf. CBMCE, LOB (Lei nº 13.438/2004), Art. 6º",
        "organName": "Conselho Consultivo", "abbr": "",
    },
    ("ag", "ce"): {
        "finalidade": (
            "A Secretaria Executiva tem por finalidade coordenar e supervisionar as atividades "
            "do Gabinete, bem como acompanhar os trabalhos das Comissões e Assessorias, "
            "competindo-lhe"
        ),
        "competencias": [
            "assessorar o Comandante Geral nos assuntos de controle interno, identificação e "
            "avaliação dos pontos críticos que possam ameaçar a comunidade cearense",
            "produzir informações estratégicas com vistas ao preparo e emprego do Corpo de "
            "Bombeiros Militar",
            "dar suporte ao Comando Geral nos assuntos de relações públicas envolvendo o "
            "público interno e externo",
            "coordenar e supervisionar assuntos relacionados com a imprensa em geral",
            "assessorar o Comando Geral na doutrina e legislação da Corporação",
            "coordenar as atividades relacionadas com a elaboração de leis, regulamentos e "
            "instruções normativas da Corporação",
            "desempenhar as funções de apoio administrativo, comando de serviços, expediente e "
            "trabalho de secretaria do Comando Geral, incluindo correspondência, protocolo "
            "geral e boletim diário",
        ],
        "source": "cf. CBMCE, LOB (Lei nº 13.438/2004), Art. 12",
        "organName": "Secretaria Executiva", "abbr": "",
    },
    ("assessorias", "ce"): {
        "finalidade": (
            "A Assessoria Jurídica é o órgão incumbido de assessorar o Comandante Geral nos "
            "diversos aspectos jurídicos da Corporação"
        ),
        "competencias": [],
        "source": "cf. CBMCE, LOB (Lei nº 13.438/2004), Art. 13",
        "organName": "Assessoria Jurídica", "abbr": "",
    },
    ("cat", "ce"): {
        "finalidade": (
            "A Coordenadoria de Atividades Técnicas é o Órgão de Execução Programática "
            "responsável pelo controle da observância dos requisitos técnicos contra incêndios "
            "e de projetos de edificações antes ou depois de sua liberação ao uso, "
            "competindo-lhe"
        ),
        "competencias": [
            "gerenciar o sistema de informações no que diz respeito à análise, cadastro e "
            "controle de dados",
            "desenvolver pesquisa científica e avaliar o desempenho operacional da Corporação",
            "analisar projetos de edificações, vistorias e pareceres técnicos",
            "controlar, manter e manobrar hidrantes",
        ],
        "source": "cf. CBMCE, LOB (Lei nº 13.438/2004), Art. 17",
        "organName": "Coordenadoria de Atividades Técnicas", "abbr": "",
    },
    ("dpo", "ce"): {
        "finalidade": "A Coordenadoria Operacional é responsável pela execução das operações bombeirísticas",
        "competencias": [],
        "source": "cf. CBMCE, LOB (Lei nº 13.438/2004), Art. 18",
        "organName": "Coordenadoria Operacional", "abbr": "",
    },
    ("crbm", "ce"): {
        "finalidade": (
            "O Núcleo de Bombeiro Metropolitano é responsável pela execução das operações de "
            "bombeiro militar na região metropolitana, competindo-lhe ainda o comando, controle "
            "e fiscalização das missões que lhe são atribuídas pelo Comandante Geral da "
            "Corporação"
        ),
        "competencias": [],
        "source": "cf. CBMCE, LOB (Lei nº 13.438/2004), Art. 19",
        "organName": "Núcleo de Bombeiro Metropolitano (e do Interior)", "abbr": "",
    },
    ("depdec", "ce"): {
        "finalidade": (
            "O Núcleo de Defesa Civil do Corpo de Bombeiros é responsável, na fase de socorro, "
            "pelo planejamento, fiscalização, controle e execução e atividades de Defesa Civil, "
            "competindo-lhe"
        ),
        "competencias": [
            "realizar a integração com a Secretaria da Ação Social e a Comunidade a fim de "
            "avaliar as situações de risco e aspectos preventivos",
            "planejar as atividades operacionais de Defesa Civil em parceria com a Secretaria "
            "da Ação Social",
        ],
        "source": "cf. CBMCE, LOB (Lei nº 13.438/2004), Art. 21",
        "organName": "Núcleo de Defesa Civil", "abbr": "",
    },
    ("bbs", "ce"): {
        "finalidade": (
            "O Núcleo de Busca e Salvamento é a unidade operacional responsável pelo serviço "
            "de busca, salvamento e proteção"
        ),
        "competencias": [],
        "source": "cf. CBMCE, LOB (Lei nº 13.438/2004), Art. 22",
        "organName": "Núcleo de Busca e Salvamento", "abbr": "",
    },
    ("dlog", "ce"): {
        "finalidade": (
            "A Célula de Logística é o órgão incumbido da administração e do suprimento de "
            "material de todas as classes, sendo responsável também pela manutenção do "
            "patrimônio móvel e imóvel, manutenção de transportes e equipamentos pesados, "
            "competindo-lhe"
        ),
        "competencias": [
            "gerir a conservação, reforma, ampliação e construção do patrimônio móvel e imóvel "
            "da Corporação",
            "fiscalizar, acompanhar, solicitar e distribuir o material necessário a todas as "
            "unidades da Corporação",
            "supervisionar a manutenção de toda a frota operacional e administrativa da "
            "Corporação",
            "gerenciar as atividades de arquivo, protocolo e controle de pessoal",
        ],
        "source": "cf. CBMCE, LOB (Lei nº 13.438/2004), Art. 26",
        "organName": "Célula de Logística", "abbr": "",
    },
    ("dpof", "ce"): {
        "finalidade": (
            "O Núcleo Financeiro é responsável pelas atividades financeiras e de contabilidade "
            "da Corporação, competindo-lhe"
        ),
        "competencias": [
            "gerenciar as contas da Corporação, utilizando instrumentos adequados de "
            "acompanhamento e execução orçamentária, objetivando controle financeiro",
            "assegurar o cumprimento dos compromissos decorrentes da execução orçamentária "
            "financeira",
            "intermediar contatos para liberação de recursos e para implantação das alterações "
            "orçamentárias, bem como, pelos pagamentos de contas e do pessoal do Corpo de "
            "Bombeiros",
            "controlar toda captação de recursos da Corporação, e atribuições de planejar, "
            "lançar, acompanhar, fiscalizar, coordenar e controlar as receitas das taxas de "
            "serviços",
            "gerenciar o acompanhamento e planejamento orçamentário e financeiro",
        ],
        "source": "cf. CBMCE, LOB (Lei nº 13.438/2004), Art. 27",
        "organName": "Núcleo Financeiro", "abbr": "",
    },
    ("dp", "ce"): {
        "finalidade": (
            "A Célula de Gestão e Formação de Pessoas é incumbida do planejamento, controle, "
            "ensino, execução, capacitação e fiscalização das atividades relacionadas ao "
            "pessoal do Corpo de Bombeiros, competindo-lhe"
        ),
        "competencias": [
            "coordenar as atividades de recrutamento, seleção, acompanhamento, controle do "
            "pessoal ativo, inativo e servidores civis, bem como acompanhar as promoções, "
            "classificação e movimentação do pessoal",
            "acompanhar o trabalho do pessoal nos serviços de assistência religiosa e "
            "psicosocial",
            "planejar assuntos pertinentes à instrução e às operações do Corpo de Bombeiros",
            "consolidar projetos, através da coleta de informações, pesquisas e experiências "
            "operacionais, marketing de serviços e recursos humanos",
            "propor as implantações e modificações administrativas, para todos os níveis da "
            "Corporação, de acordo com os preceitos de qualidade total, reengenharia, "
            "racionalização de meios e espaço, no sentido de modernizar, aumentar a "
            "produtividade e a qualidade administrativa operacional",
        ],
        "source": "cf. CBMCE, LOB (Lei nº 13.438/2004), Art. 28",
        "organName": "Célula de Gestão e Formação de Pessoas", "abbr": "",
    },
    ("deei", "ce"): {
        "finalidade": (
            "O Colégio Militar do Corpo de Bombeiros – CMCB, é responsável pelo sistema de "
            "ensino da Corporação, desempenhando-as pelas seguintes atribuições"
        ),
        "competencias": [
            "orientar a formação integral dos alunos",
            "realizar o enquadramento militar compatível com a idade e a condição de aluno, em "
            "consonância com a Orientação Educacional do Colégio",
            "supervisionar, coordenar e controlar as atividades do Corpo Discente",
            "planejar, programar, executar, controlar, supervisionar e orientar os serviços "
            "administrativos do Colégio",
            "direcionar os objetivos para os métodos e aprendizagem aplicada pelo corpo docente "
            "e acompanhamento do processo ensino-aprendizagem",
            "planejar os assuntos relativos à comunicação social",
            "acompanhar os trabalhos educativos desenvolvidos e os projetos técnicos para o "
            "aprimoramento educacional",
        ],
        "source": "cf. CBMCE, LOB (Lei nº 13.438/2004), Art. 30",
        "organName": "Colégio Militar do Corpo de Bombeiros", "abbr": "CMCB",
    },

    # --- Goiás (CBMGO) — Lei nº 18.305/2013 (completa o Lote inicial; cg/go e dp/go já existem) ---
    # LOB por competências enumeradas (incisos); a finalidade dos Comandos Regionais vem do
    # Art. 21 e seus incisos do Art. 22.
    ("crbm", "go"): {
        "finalidade": (
            "Os órgãos de direção regional, representados pelos Comandos Regionais, são "
            "organizados para a consecução de atividades de gestão operacional, cabendo-lhes a "
            "otimização na aplicação dos recursos operacionais disponíveis nas respectivas "
            "atribuições, conforme diretrizes e ordens definidas pelo órgão de direção geral"
        ),
        "competencias": [
            "exercer a gestão operacional nas respectivas regiões",
            "planejar, controlar e fiscalizar as atividades operacionais desenvolvidas pelas "
            "respectivas unidades de execução, bem como exercer outras missões correlatas",
        ],
        "source": "cf. CBMGO, LOB (Lei nº 18.305/2013), Art. 21-22",
        "organName": "Comandos Regionais", "abbr": "",
    },
    ("corregedoria", "go"): {
        "finalidade": "",
        "competencias": [
            "assegurar a disciplina funcional, os princípios hierárquicos estruturais "
            "fundamentais e a apuração das infrações penais militares e transgressões "
            "disciplinares",
            "exercer diretamente ou por meio das Organizações Bombeiro Militares as funções de "
            "Polícia Judiciária Militar e de Polícia Administrativa, observada a legislação "
            "vigente",
            "acompanhar a apuração de ilícitos penais e transgressões disciplinares",
            "promover execução, controle, coordenação, orientação e fiscalização de atividade "
            "pertinente à disciplina e execução judiciária",
            "controlar a instauração de inquéritos policiais, sindicâncias, conselhos de "
            "justificação, conselhos de disciplina, autos de prisão em flagrante, inquéritos "
            "técnicos e outros procedimentos administrativos",
            "exercer fiscalização ostensiva quanto ao desempenho funcional, operacional e "
            "administrativo dos integrantes da Corporação",
            "exercer as atividades de ouvidoria no âmbito da Corporação",
        ],
        "source": "cf. CBMGO, LOB (Lei nº 18.305/2013), Art. 24",
        "organName": "Comando de Correições e Disciplina", "abbr": "",
    },
    ("dlog", "go"): {
        "finalidade": "",
        "competencias": [
            "planejar e controlar as atividades relacionadas às necessidades de suprimento e "
            "manutenção da Corporação, bem como o controle patrimonial, de acordo com premissas "
            "definidas pelo Comando Geral",
            "elaborar normas internas sobre especificações e solicitações de materiais e "
            "serviços, bem como aquisição, recebimento, armazenamento, distribuição, "
            "manutenção, fiscalização e controle dos materiais, equipamentos, viaturas e "
            "instalações no âmbito da Corporação e submeter à apreciação do Comando Geral para "
            "aprovação",
            "executar atos pertinentes a licitações e contratos, excetuando-se aqueles de "
            "competência exclusiva do ordenador de despesas, quando tratar-se de recursos do "
            "Fundo Especial de Reaparelhamento e Modernização do Corpo de Bombeiros Militar do "
            "Estado de Goiás – FUNEBOM–, bem como acompanhar processos até o cumprimento "
            "integral das obrigações contratuais",
            "realizar gestão junto aos órgãos competentes visando celeridade no andamento "
            "processual de licitações e contratos",
        ],
        "source": "cf. CBMGO, LOB (Lei nº 18.305/2013), Art. 25",
        "organName": "Comando de Apoio Logístico", "abbr": "",
    },
    ("depdec", "go"): {
        "finalidade": "",
        "competencias": [
            "elaborar planos de gestão operacional nos assuntos relacionados a defesa civil",
            "coordenar as atividades de planejamento, contingência, socorro e reconstrução "
            "relacionadas a defesa civil",
            "realizar ações de prevenção contra incêndio e pânico e de defesa civil por meio "
            "dos órgãos de execução",
            "planejar, controlar e fiscalizar as atividades relacionadas à análise de projetos "
            "e inspeções nas edificações e áreas de risco",
            "elaborar projetos e coordenar programas relacionados à política estadual de Defesa "
            "Civil, além de outras definidas em regulamento",
        ],
        "source": "cf. CBMGO, LOB (Lei nº 18.305/2013), Art. 27",
        "organName": "Comando de Operações de Defesa Civil", "abbr": "",
    },
    ("deei", "go"): {
        "finalidade": "",
        "competencias": [
            "elaborar o planejamento institucional inerente a formação, especialização, "
            "aperfeiçoamento, habilitação e aprimoramento técnico-profissional dos bombeiros "
            "militares, bem como o controle e fiscalização das atividades correlatas",
            "elaborar normas e manuais operacionais relacionados à doutrina institucional de "
            "ensino",
        ],
        "source": "cf. CBMGO, LOB (Lei nº 18.305/2013), Art. 28",
        "organName": "Comando de Ensino Bombeiro Militar", "abbr": "",
    },
    ("cint", "go"): {
        "finalidade": "",
        "competencias": [
            "produzir conhecimentos e informações que subsidiem ações para prevenir, "
            "neutralizar, coibir e reprimir atos de qualquer natureza que venham prejudicar a "
            "Corporação no cumprimento de suas atribuições legais, tendo como fundamentos "
            "básicos a defesa do Estado Democrático de Direito e a dignidade da pessoa humana",
            "exercer atividades de inteligência de interesse institucional com o intuito de "
            "subsidiar tomadas de decisão do Comandante-Geral e do Subcomandante-Geral, com "
            "vistas ao aprimoramento dos serviços prestados pela Instituição",
            "identificar, monitorar e avaliar ameaças reais ou potenciais à segurança e "
            "manutenção das atividades do Corpo de Bombeiros Militar",
            "realizar investigações sociais relativas à seleção de candidatos ao ingresso nas "
            "fileiras da Corporação",
            "produzir conhecimentos e informações que subsidiem tomadas de decisão e ações "
            "relacionadas ao exercício das atribuições previstas nesta Lei",
        ],
        "source": "cf. CBMGO, LOB (Lei nº 18.305/2013), Art. 29",
        "organName": "Comando de Operações de Inteligência", "abbr": "",
    },
    ("dsap", "go"): {
        "finalidade": "",
        "competencias": [
            "planejar, coordenar, orientar, controlar e avaliar as atividades realizadas pelos "
            "serviços médico e odontológico",
            "executar as ações relacionadas à saúde física e mental dos militares da Corporação",
            "apoiar a execução de atividades preventivas e operacionais realizadas diretamente "
            "pela Corporação ou em que ela esteja envolvida",
        ],
        "source": "cf. CBMGO, LOB (Lei nº 18.305/2013), Art. 32",
        "organName": "Comando de Saúde", "abbr": "",
    },
    ("boa", "go"): {
        "finalidade": (
            "O Centro de Operações Aéreas é responsável pela execução de operações aéreas "
            "relacionadas à missão constitucional da Corporação"
        ),
        "competencias": [],
        "source": "cf. CBMGO, LOB (Lei nº 18.305/2013), Art. 34, § 2º",
        "organName": "Centro de Operações Aéreas", "abbr": "",
    },
    ("gab-cg", "go"): {
        "finalidade": (
            "À Chefia de Gabinete compete o exercício das funções de assistência e "
            "assessoramento direto ao Comandante-Geral e ao Subcomandante-Geral, inerentes ao "
            "controle, coordenação e fiscalização das atividades administrativas desenvolvidas "
            "por militares e civis no âmbito dos Gabinetes do Comandante-Geral e do "
            "Subcomandante-Geral, da Ajudância de Ordens, da Assessoria Jurídica e da "
            "Secretaria-Geral"
        ),
        "competencias": [],
        "source": "cf. CBMGO, LOB (Lei nº 18.305/2013), Art. 15",
        "organName": "Chefia de Gabinete", "abbr": "",
    },
    ("assessorias", "go"): {
        "finalidade": (
            "À Assessoria Jurídica compete assessorar o Comando Geral em matérias de natureza "
            "jurídica já pacificadas no âmbito da Procuradoria-Geral do Estado"
        ),
        "competencias": [
            "analisar normas, diretrizes, portarias, determinações, informações e demais "
            "documentos emanados do Comando Geral",
            "orientar o Comando Geral quanto ao exato cumprimento de decisões e sentenças "
            "judiciais, de acordo com as orientações emanadas da Procuradoria-Geral do Estado",
            "coligir elementos de fato e de direito para preparar as informações que devem ser "
            "prestadas à Procuradoria-Geral do Estado, para a defesa dos interesses do Estado "
            "de Goiás em ações judiciais",
        ],
        "source": "cf. CBMGO, LOB (Lei nº 18.305/2013), Art. 17",
        "organName": "Assessoria Jurídica", "abbr": "",
    },
    ("ag", "go"): {
        "finalidade": (
            "À Secretaria-Geral competem a recepção, o protocolo, a elaboração e o controle de "
            "toda a documentação pertinente ao Comando Geral"
        ),
        "competencias": [],
        "source": "cf. CBMGO, LOB (Lei nº 18.305/2013), Art. 20",
        "organName": "Secretaria-Geral", "abbr": "",
    },
    ("bbm", "go"): {
        "finalidade": (
            "Batalhão Bombeiro Militar, cujo comando é prerrogativa de Oficial Superior do "
            "Quadro de Oficiais de Comando - QOC, é unidade operacional responsável pela "
            "execução de atividades-fim das respectivas áreas de atuação, conforme diretrizes e "
            "ordens emanadas dos órgãos de direção geral, regional e setorial"
        ),
        "competencias": [],
        "source": "cf. CBMGO, LOB (Lei nº 18.305/2013), Art. 34, § 5º, I",
        "organName": "Batalhão Bombeiro Militar", "abbr": "",
    },
    ("cibm", "go"): {
        "finalidade": (
            "Companhia Independente Bombeiro Militar, cujo comando é prerrogativa de Oficial "
            "Superior do QOC, é unidade operacional responsável pela execução de atividades-fim "
            "das respectivas áreas de atuação, conforme diretrizes e ordens emanadas dos órgãos "
            "de direção geral, regional e setorial"
        ),
        "competencias": [],
        "source": "cf. CBMGO, LOB (Lei nº 18.305/2013), Art. 34, § 5º, II",
        "organName": "Companhia Independente Bombeiro Militar", "abbr": "",
    },

    # --- Distrito Federal (CBMDF) — Lei nº 8.255/1991 ---
    # LOB por finalidade/atribuição; (cg) usa a atribuição do Comandante-Geral (cargo).
    ("cg", "df"): {
        "finalidade": (
            "O Comandante-Geral do Corpo de Bombeiros Militar do Distrito Federal é o "
            "responsável pela administração, comando e emprego da corporação"
        ),
        "competencias": [],
        "source": "cf. CBMDF, LOB (Lei nº 8.255/1991), Art. 9º",
        "organName": "Comandante-Geral", "abbr": "",
    },
    ("condeg", "df"): {
        "finalidade": (
            "O Alto Comando, órgão consultivo do Comandante-Geral, é constituído dos seguintes "
            "membros: Comandante-Geral, na qualidade de Presidente; Subcomandante-Geral, na "
            "qualidade de Vice-Presidente; Chefe do Estado-Maior-Geral; Controlador; Chefe de "
            "Gabinete do Comandante-Geral; Chefes de Departamento; Diretores; "
            "Comandante-Operacional; Ajudante-Geral; os Ex-Comandantes-Gerais e "
            "Ex-Subcomandantes-Gerais da Corporação, enquanto não passarem para a inatividade"
        ),
        "competencias": [],
        "source": "cf. CBMDF, LOB (Lei nº 8.255/1991), Art. 8º-A",
        "organName": "Alto Comando", "abbr": "",
    },
    ("corregedoria", "df"): {
        "finalidade": (
            "A Controladoria é o órgão de assessoramento direto e imediato ao Comandante-Geral "
            "quanto aos assuntos e providências relacionados com a defesa do patrimônio "
            "público, auditoria, correição, ouvidoria, orientação e fiscalização, e averiguação "
            "e análise das atividades de administração orçamentária, financeira, patrimonial e "
            "de gestão de pessoas"
        ),
        "competencias": [],
        "source": "cf. CBMDF, LOB (Lei nº 8.255/1991), Art. 22",
        "organName": "Controladoria", "abbr": "",
    },
    ("ag", "df"): {
        "finalidade": (
            "A Ajudância Geral, subordinada diretamente ao Comandante-Geral, é o órgão de "
            "direção encarregado de auxiliar nas funções de administração do Quartel do Comando "
            "Geral, considerado como Organização de Bombeiro Militar"
        ),
        "competencias": [],
        "source": "cf. CBMDF, LOB (Lei nº 8.255/1991), Art. 21",
        "organName": "Ajudância Geral", "abbr": "",
    },
    ("gab-cg", "df"): {
        "finalidade": (
            "O Gabinete do Comandante-Geral tem a seu cargo as funções de assistência e "
            "assessoramento direto ao Comandante-Geral, nos assuntos que escapem às atribuições "
            "normais e específicas dos demais órgãos de direção e destina-se a dar "
            "flexibilidade à estrutura do Comando Geral da Corporação, particularmente em "
            "assuntos técnicos especializados"
        ),
        "competencias": [],
        "source": "cf. CBMDF, LOB (Lei nº 8.255/1991), Art. 23",
        "organName": "Gabinete do Comandante-Geral", "abbr": "",
    },
    ("deei", "df"): {
        "finalidade": (
            "A Academia de Bombeiro Militar (ABM) é o órgão de apoio do sistema de ensino, "
            "subordinado à Diretoria de Ensino e Instrução, incumbida da formação, do "
            "aperfeiçoamento, do treinamento e da instrução especializada dos oficiais e dos "
            "cadetes do Corpo de Bombeiros Militar do Distrito Federal e, eventualmente, de "
            "oficiais e de alunos de outras corporações"
        ),
        "competencias": [],
        "source": "cf. CBMDF, LOB (Lei nº 8.255/1991), Art. 25",
        "organName": "Academia de Bombeiro Militar", "abbr": "ABM",
    },
    ("dsap", "df"): {
        "finalidade": (
            "As Policlínicas são órgãos de apoio ao sistema de saúde, incumbidas da assistência "
            "médica, odontológica, farmacêutica e sanitária à família bombeiro-militar, "
            "conforme dispuser a lei"
        ),
        "competencias": [],
        "source": "cf. CBMDF, LOB (Lei nº 8.255/1991), Art. 26",
        "organName": "Policlínicas", "abbr": "",
    },
    ("dpo", "df"): {
        "finalidade": (
            "Comando Operacional é a denominação genérica dada a Organização Bombeiro-Militar "
            "de mais alto escalão, dotada de Estado-Maior próprio e subordinada ao "
            "Comandante-Geral, que tem a seu cargo o planejamento estratégico, a coordenação e "
            "o emprego das unidades e subunidades que lhes forem subordinadas, com a finalidade "
            "de executar atividades de prevenção, guarda e segurança, combate a incêndio, busca "
            "e salvamento, atendimento pré-hospitalar e defesa civil, além de outras, em uma "
            "determinada área operacional"
        ),
        "competencias": [],
        "source": "cf. CBMDF, LOB (Lei nº 8.255/1991), Art. 28, § 1º",
        "organName": "Comando Operacional", "abbr": "",
    },

    # --- Espírito Santo (CBMES) — Lei Complementar nº 101/1997 (texto consolidado) ---
    # LOB que dá finalidade/competência (caput e §§ acrescidos por LC 705/2013 — texto de Lei,
    # não NGA) a vários órgãos. (cg) usa a atribuição do Comandante-Geral.
    ("cg", "es"): {
        "finalidade": (
            "O Comandante-Geral é o responsável pelo comando, administração e emprego da "
            "Corporação. Será um Oficial da Ativa do último posto do Quadro de Oficiais "
            "Combatentes BM"
        ),
        "competencias": [],
        "source": "cf. CBMES, LOB (LC nº 101/1997), Art. 10",
        "organName": "Comandante-Geral", "abbr": "",
    },
    ("depdec", "es"): {
        "finalidade": (
            "À Coordenadoria Estadual de Proteção e Defesa Civil, órgão central do Sistema "
            "Estadual de Defesa Civil, compete, além de outras atribuições que lhe forem "
            "conferidas por lei, articular e coordenar as ações de proteção e defesa civil no "
            "Estado, compreendendo a prevenção e a preparação para desastres, a assistência e "
            "socorro às vítimas das calamidades, o restabelecimento de serviços essenciais e a "
            "reconstrução de comunidades"
        ),
        "competencias": [],
        "source": "cf. CBMES, LOB (LC nº 101/1997), Art. 9º, § 1º",
        "organName": "Coordenadoria Estadual de Proteção e Defesa Civil", "abbr": "",
    },
    ("corregedoria", "es"): {
        "finalidade": (
            "A Corregedoria é responsável por planejar, coordenar, instaurar, executar, "
            "fiscalizar e controlar os trabalhos dos processos e procedimentos administrativos "
            "de qualquer natureza, das atividades de investigação, bem como das apurações das "
            "infrações penais militares, referentes aos atos e fatos envolvendo a participação "
            "de militares estaduais da Corporação, competindo-lhe também a auditagem nos "
            "processos administrativos e operacionais da Corporação"
        ),
        "competencias": [],
        "source": "cf. CBMES, LOB (LC nº 101/1997), Art. 9º, § 2º",
        "organName": "Corregedoria", "abbr": "",
    },
    ("cot", "es"): {
        "finalidade": (
            "A Diretoria de Atividades Técnicas (DAT), órgão subordinado diretamente ao Comando "
            "Geral do Corpo de Bombeiros, tem como competência: estudar, analisar, planejar, "
            "normatizar, exigir e fiscalizar o cumprimento das disposições legais, assim como "
            "todos os serviços de segurança contra incêndio e pânico, dirigindo também todas as "
            "atividades que envolvem as perícias de incêndio e explosão em locais de sinistro "
            "no Estado do Espírito Santo"
        ),
        "competencias": [],
        "source": "cf. CBMES, LOB (LC nº 101/1997), Art. 13, § 2º",
        "organName": "Diretoria de Atividades Técnicas", "abbr": "DAT",
    },
    ("dpo", "es"): {
        "finalidade": (
            "A Diretoria de Operações (DOp), órgão subordinado diretamente ao Comando Geral do "
            "Corpo de Bombeiros, tem como competência: disciplinar, coordenar e controlar todas "
            "as atividades envolvendo as missões constitucionais do CBMES especificamente no "
            "que se refere a combate a incêndios e busca e salvamento, bem como apurar dados a "
            "fim de fundamentar estatísticas para um melhor emprego e uso de técnicas e táticas "
            "adequadas nas ações referentes aos procedimentos operacionais"
        ),
        "competencias": [],
        "source": "cf. CBMES, LOB (LC nº 101/1997), Art. 13, § 3º",
        "organName": "Diretoria de Operações", "abbr": "DOp",
    },
    ("dlog", "es"): {
        "finalidade": (
            "A Diretoria de Apoio Logístico (DAL), órgão subordinado diretamente ao Comando "
            "Geral do Corpo de Bombeiros, tem como competência: planejar, supervisionar, "
            "coordenar, controlar, fiscalizar e executar as ações da aquisição, do "
            "armazenamento e da manutenção dos materiais, dos equipamentos, dos armamentos, das "
            "munições, das viaturas, dos bens móveis e imóveis, obras e instalações "
            "patrimoniais, convênios e contratos administrativos e de telecomunicações"
        ),
        "competencias": [],
        "source": "cf. CBMES, LOB (LC nº 101/1997), Art. 13, § 4º",
        "organName": "Diretoria de Apoio Logístico", "abbr": "DAL",
    },
    ("dpof", "es"): {
        "finalidade": (
            "A Diretoria de Finanças (DF), órgão subordinado diretamente ao Comando Geral do "
            "Corpo de Bombeiros, tem como competência: planejar, supervisionar, coordenar, "
            "controlar, fiscalizar e executar a administração financeira e patrimonial da "
            "Corporação"
        ),
        "competencias": [],
        "source": "cf. CBMES, LOB (LC nº 101/1997), Art. 13, § 5º",
        "organName": "Diretoria de Finanças", "abbr": "DF",
    },
    ("ag", "es"): {
        "finalidade": (
            "A Ajudância-Geral tem como competência o desenvolvimento das atividades "
            "administrativas do Comando Geral e suas principais atribuições são: secretaria do "
            "Comando Geral, incluindo correspondência, protocolo geral, arquivo geral e serviço "
            "de embarque da corporação"
        ),
        "competencias": [],
        "source": "cf. CBMES, LOB (LC nº 101/1997), Art. 14",
        "organName": "Ajudância-Geral", "abbr": "",
    },
    ("assessorias", "es"): {
        "finalidade": (
            "As assessorias, constituídas eventualmente para determinados estudos que escapem "
            "às atribuições normais e específicas dos órgãos de direção, destinam-se a dar "
            "flexibilidade a estrutura do Comando da Corporação, particularmente em assuntos "
            "especializados"
        ),
        "competencias": [],
        "source": "cf. CBMES, LOB (LC nº 101/1997), Art. 16",
        "organName": "Assessorias", "abbr": "",
    },
    ("deei", "es"): {
        "finalidade": (
            "O Centro de Ensino e Instrução de Bombeiros (CEIB), é o órgão responsável pela "
            "formação, aperfeiçoamento e especialização de bombeiros, bem como, ao "
            "desenvolvimento de estudos e pesquisas"
        ),
        "competencias": [],
        "source": "cf. CBMES, LOB (LC nº 101/1997), Art. 17, § 1º",
        "organName": "Centro de Ensino e Instrução de Bombeiros", "abbr": "CEIB",
    },
    ("dsap", "es"): {
        "finalidade": (
            "O Centro de Serviço Social (CSS), é o órgão de apoio de pessoal, destinando-se, a "
            "prestação de serviços assistenciais"
        ),
        "competencias": [],
        "source": "cf. CBMES, LOB (LC nº 101/1997), Art. 17, § 2º",
        "organName": "Centro de Serviço Social", "abbr": "CSS",
    },
    ("cat", "es"): {
        "finalidade": (
            "O Centro de Atividades Técnicas (CAT), órgão subordinado diretamente ao Comando do "
            "Corpo de Bombeiros, tem como competência: estudar, analisar, planejar, normatizar, "
            "exigir e fiscalizar o cumprimento das disposições legais, assim como todos os "
            "serviços de segurança contra incêndio e pânico, bem como realizar perícias de "
            "incêndio e explosões em locais de sinistro no Estado do Espírito Santo"
        ),
        "competencias": [],
        "source": "cf. CBMES, LOB (LC nº 101/1997), Art. 19",
        "organName": "Centro de Atividades Técnicas", "abbr": "CAT",
    },
    ("bbm", "es"): {
        "finalidade": (
            "O Batalhão de Bombeiros Militares, órgão subordinado diretamente ao Comando do "
            "Corpo de Bombeiros, tem como competência: a prevenção e o combate a incêndios, "
            "busca e salvamento, realizar socorros de urgências, controlar o tráfego de "
            "embarcações próximo às praias, rios e lagos e ações de defesa civil"
        ),
        "competencias": [],
        "source": "cf. CBMES, LOB (LC nº 101/1997), Art. 20",
        "organName": "Batalhão de Bombeiros Militares", "abbr": "BBM",
    },

    # --- Maranhão (CBMMA) — Lei nº 10.230/2015 ---
    # LOB que dá finalidade/competência aos órgãos (caput dos artigos e §§ do Art. 13).
    # (cg) usa a atribuição do Comandante-Geral.
    ("cg", "ma"): {
        "finalidade": "A administração e o comando da Corporação são de competência do Comandante-Geral",
        "competencias": [],
        "source": "cf. CBMMA, LOB (Lei nº 10.230/2015), Art. 6º",
        "organName": "Comandante-Geral", "abbr": "",
    },
    ("condeg", "ma"): {
        "finalidade": "O Alto-Comando tem por finalidade opinar, propor e estudar sobre",
        "competencias": [
            "políticas de gestão e estratégia da Corporação",
            "gestão de planos e programas oriundos do plano diretor da Corporação",
            "outras matérias que sejam propostas pelo Comandante-Geral",
        ],
        "source": "cf. CBMMA, LOB (Lei nº 10.230/2015), Art. 9º",
        "organName": "Alto-Comando", "abbr": "",
    },
    ("dp", "ma"): {
        "finalidade": (
            "À Diretoria de Pessoal compete o planejamento, coordenação, execução, controle e "
            "fiscalização relacionados a pessoal, além da assistência social e religiosa ao "
            "bombeiro militar"
        ),
        "competencias": [],
        "source": "cf. CBMMA, LOB (Lei nº 10.230/2015), Art. 13, § 1º",
        "organName": "Diretoria de Pessoal", "abbr": "",
    },
    ("dpof", "ma"): {
        "finalidade": (
            "À Diretoria de Finanças compete o funcionamento do sistema de administração "
            "financeira, programação, orçamento e contabilidade"
        ),
        "competencias": [],
        "source": "cf. CBMMA, LOB (Lei nº 10.230/2015), Art. 13, § 2º",
        "organName": "Diretoria de Finanças", "abbr": "",
    },
    ("deei", "ma"): {
        "finalidade": (
            "À Diretoria de Ensino e Pesquisa compete o planejamento, coordenação, controle e "
            "fiscalização das atividades de formação, aperfeiçoamento e especialização nos "
            "diferentes níveis de ensino, do adestramento e da instrução"
        ),
        "competencias": [],
        "source": "cf. CBMMA, LOB (Lei nº 10.230/2015), Art. 13, § 3º",
        "organName": "Diretoria de Ensino e Pesquisa", "abbr": "",
    },
    ("dlog", "ma"): {
        "finalidade": (
            "À Diretoria de Apoio Logístico compete o planejamento, aquisição, coordenação, "
            "fiscalização e controle de suprimento, material, equipamentos e viaturas, bem "
            "como, das atividades de manutenção de material e das instalações físicas"
        ),
        "competencias": [],
        "source": "cf. CBMMA, LOB (Lei nº 10.230/2015), Art. 13, § 4º",
        "organName": "Diretoria de Apoio Logístico", "abbr": "",
    },
    ("cat", "ma"): {
        "finalidade": (
            "À Diretoria de Atividades Técnicas compete o planejamento, fiscalização e controle "
            "das atividades de prevenção em locais de grande concentração humana, vistorias e "
            "pareceres técnicos, apoio operacional e auxílio dos serviços e missões específicas "
            "no âmbito estadual"
        ),
        "competencias": [],
        "source": "cf. CBMMA, LOB (Lei nº 10.230/2015), Art. 13, § 5º",
        "organName": "Diretoria de Atividades Técnicas", "abbr": "",
    },
    ("cint", "ma"): {
        "finalidade": (
            "A Diretoria de Inteligência compete o assessoramento direto ao Comandante-Geral "
            "nos assuntos pertinentes à informação, à inteligência e à contra-inteligência"
        ),
        "competencias": [],
        "source": "cf. CBMMA, LOB (Lei nº 10.230/2015), Art. 13, § 6º",
        "organName": "Diretoria de Inteligência", "abbr": "",
    },
    ("cinf", "ma"): {
        "finalidade": (
            "À Diretoria de Planejamento e Modernização compete o planejamento orçamentário, a "
            "gestão de projetos, elaboração de planos de modernização da Institucional e a "
            "implementação de sistemas de tecnologia da informação"
        ),
        "competencias": [],
        "source": "cf. CBMMA, LOB (Lei nº 10.230/2015), Art. 13, § 7º",
        "organName": "Diretoria de Planejamento e Modernização", "abbr": "",
    },
    ("ag", "ma"): {
        "finalidade": (
            "A Ajudância-Geral, subordinada ao Comandante Adjunto, em nível de Centro, compete "
            "a publicação dos atos administrativos e auxiliar nas funções de administração e "
            "conservação das instalações físicas do Quartel do Comando Geral"
        ),
        "competencias": [],
        "source": "cf. CBMMA, LOB (Lei nº 10.230/2015), Art. 14",
        "organName": "Ajudância-Geral", "abbr": "",
    },
    ("gab-cg", "ma"): {
        "finalidade": (
            "O Gabinete do Comandante-Geral, subordinado diretamente ao Comandante-Geral, em "
            "nível de Centro, tem a seu cargo as funções de assistência geral e assessoramento "
            "nos assuntos que não sejam às atribuições normais e específicas dos demais órgãos "
            "de direção e destina-se a dar flexibilidade à estrutura do Comando Geral da "
            "corporação"
        ),
        "competencias": [],
        "source": "cf. CBMMA, LOB (Lei nº 10.230/2015), Art. 17",
        "organName": "Gabinete do Comandante-Geral", "abbr": "",
    },
    ("assessorias", "ma"): {
        "finalidade": (
            "As Assessorias compete dar suporte à estrutura do Comando da Corporação, "
            "particularmente em assuntos de natureza técnica ou especializada, podendo ser "
            "constituídas por bombeiros militar ou por civis, de acordo legislação específica"
        ),
        "competencias": [],
        "source": "cf. CBMMA, LOB (Lei nº 10.230/2015), Art. 19",
        "organName": "Assessorias", "abbr": "",
    },
    ("dsap", "ma"): {
        "finalidade": (
            "A Coordenadoria Médica de Saúde, órgão subordinado ao Comandante Adjunto, compete "
            "a assistência médica, farmacêutica e sanitária da família bombeiro militar"
        ),
        "competencias": [],
        "source": "cf. CBMMA, LOB (Lei nº 10.230/2015), Art. 22",
        "organName": "Coordenadoria Médica de Saúde", "abbr": "",
    },
    ("crbm", "ma"): {
        "finalidade": (
            "Aos Comandos Operacionais, denominação genérica dada às organizações bombeiros "
            "militar operacionais de mais alto escalão, subordinados ao Comandante Adjunto, "
            "compete à aplicação da disciplina, o planejamento estratégico, a coordenação e o "
            "emprego de unidade e subunidade operacionais, com a finalidade de executar as "
            "atividades de prevenção, guarda e segurança, combate a incêndio, busca e "
            "salvamento, atendimento pré-hospitalar e proteção e defesa civil, engenharia de "
            "segurança contra incêndio e pânico, além de outras conexas"
        ),
        "competencias": [],
        "source": "cf. CBMMA, LOB (Lei nº 10.230/2015), Art. 29",
        "organName": "Comandos Operacionais", "abbr": "",
    },
    ("bbm", "ma"): {
        "finalidade": (
            "Ao Batalhão de Bombeiros Militar e ao Batalhão de Bombeiros Militar Especializado "
            "compete o planejamento estratégico, coordenação e o emprego de unidade e "
            "subunidade operacionais, com a finalidade de executar as atividades de prevenção, "
            "guarda e segurança, combate a incêndio, busca e salvamento, atendimento "
            "pré-hospitalar e proteção e defesa civil, engenharia de segurança contra incêndio "
            "e pânico, além de outras conexas"
        ),
        "competencias": [],
        "source": "cf. CBMMA, LOB (Lei nº 10.230/2015), Art. 28, § 4º",
        "organName": "Batalhão de Bombeiros Militar", "abbr": "BBM",
    },
    ("bbs", "ma"): {
        "finalidade": (
            "Ao Batalhão de Bombeiros de Busca e Salvamento compete as missões de resgate, "
            "busca, salvamento terrestre e em altura e as demais que lhes sejam conexas"
        ),
        "competencias": [],
        "source": "cf. CBMMA, LOB (Lei nº 10.230/2015), Art. 28, § 7º",
        "organName": "Batalhão de Bombeiros de Busca e Salvamento", "abbr": "BBS",
    },
    ("bifea", "ma"): {
        "finalidade": (
            "Ao Batalhão de Bombeiros Ambiental compete as missões de prevenção e combate a "
            "incêndios florestais, as relacionadas ao meio-ambiente e as demais que lhes sejam "
            "conexas"
        ),
        "competencias": [],
        "source": "cf. CBMMA, LOB (Lei nº 10.230/2015), Art. 28, § 8º",
        "organName": "Batalhão de Bombeiros Ambiental", "abbr": "BBA",
    },
    ("cibm", "ma"): {
        "finalidade": (
            "A Companhia Independente de Bombeiros Militar e a Companhia Independente "
            "Especializada de Bombeiros Militar compete o planejamento estratégico, coordenação "
            "e o emprego de unidade e subunidade operacionais, em área de menor abrangência que "
            "um Batalhão de Bombeiros Militar, com a finalidade de executar as atividades de "
            "prevenção, guarda e segurança, combate a incêndio, busca e salvamento, atendimento "
            "pré-hospitalar e defesa civil, engenharia de segurança contra incêndio e pânico, "
            "além de outras conexas"
        ),
        "competencias": [],
        "source": "cf. CBMMA, LOB (Lei nº 10.230/2015), Art. 28, § 9º",
        "organName": "Companhia Independente de Bombeiros Militar", "abbr": "CIBM",
    },

    # --- Minas Gerais (CBMMG) — Lei Complementar nº 54/1999 ---
    # LOB que dá finalidade/competência (caput e incisos) a parte dos órgãos. As Diretorias
    # (Art. 17-19) só são mencionadas, sem finalidade individual → sem entrada (dp/dpof).
    ("cg", "mg"): {
        "finalidade": "O Comandante-Geral é responsável pelo comando e pela administração geral da Corporação",
        "competencias": [],
        "source": "cf. CBMMG, LOB (LC nº 54/1999), Art. 12, § 1º",
        "organName": "Comandante-Geral", "abbr": "",
    },
    ("cat", "mg"): {
        "finalidade": (
            "Compete ao Centro de Atividades Técnicas - CAT -, unidade subordinada diretamente "
            "ao Comando-Geral do Corpo de Bombeiros Militar"
        ),
        "competencias": [
            "pesquisar, analisar, planejar, normatizar, exigir e fiscalizar o cumprimento das "
            "disposições legais próprias dos serviços de segurança contra incêndio e pânico",
            "realizar perícias de incêndio e explosão em locais de sinistro",
            "atuar como segunda instância na análise de projetos de prevenção no Estado",
        ],
        "source": "cf. CBMMG, LOB (LC nº 54/1999), Art. 24",
        "organName": "Centro de Atividades Técnicas", "abbr": "CAT",
    },
    ("dlog", "mg"): {
        "finalidade": (
            "O Centro de Suprimento e Manutenção - CSM -, unidade responsável pelo suprimento "
            "logístico da corporação, vincula-se à diretoria de Apoio Logístico, cabendo-lhe as "
            "atividades de recebimento, estocagem, distribuição de materiais, manutenção de "
            "viaturas e equipamentos especializados e intendência"
        ),
        "competencias": [],
        "source": "cf. CBMMG, LOB (LC nº 54/1999), Art. 23",
        "organName": "Centro de Suprimento e Manutenção", "abbr": "CSM",
    },
    ("deei", "mg"): {
        "finalidade": (
            "A Academia de Bombeiros Militar – ABM – é unidade responsável pela formação, pelo "
            "aperfeiçoamento e pela especialização de Bombeiros"
        ),
        "competencias": [],
        "source": "cf. CBMMG, LOB (LC nº 54/1999), Art. 22",
        "organName": "Academia de Bombeiros Militar", "abbr": "ABM",
    },
    ("ag", "mg"): {
        "finalidade": (
            "A Ajudância-Geral, unidade responsável pelas funções administrativas do "
            "Comando-Geral, é subordinada diretamente a esse Comando, cabendo-lhe"
        ),
        "competencias": [
            "o trabalho de secretaria, correspondência, correio, protocolo geral, arquivo "
            "geral, boletim geral e outros",
            "o apoio ao quartel do Comando-Geral no que se refere a pessoal e material, "
            "administração financeira e contábil, almoxarifado e aprovisionamento",
            "a segurança do quartel do Comando-Geral",
        ],
        "source": "cf. CBMMG, LOB (LC nº 54/1999), Art. 25",
        "organName": "Ajudância-Geral", "abbr": "",
    },
    ("crbm", "mg"): {
        "finalidade": (
            "Os Comandos Operacionais de Bombeiros, Unidades de Direção Intermediária, são "
            "responsáveis perante o Comando-Geral pela coordenação das atividades operacionais "
            "de competência do Corpo de Bombeiros Militar, em sua respectiva área de atuação, "
            "de acordo com as diretrizes e ordens emanadas do Comando-Geral"
        ),
        "competencias": [],
        "source": "cf. CBMMG, LOB (LC nº 54/1999), Art. 20, § 1º",
        "organName": "Comandos Operacionais de Bombeiros", "abbr": "",
    },
    ("bbm", "mg"): {
        "finalidade": (
            "Compete ao Batalhão e à Companhia Independente de Bombeiros Militar, unidades "
            "subordinadas diretamente ao Comando Operacional de Bombeiros, realizar ações de "
            "prevenção e combate a incêndio, busca e salvamento, socorros de urgência e defesa "
            "civil"
        ),
        "competencias": [],
        "source": "cf. CBMMG, LOB (LC nº 54/1999), Art. 27",
        "organName": "Batalhão de Bombeiros Militar", "abbr": "BBM",
    },
    ("cibm", "mg"): {
        "finalidade": (
            "Compete ao Batalhão e à Companhia Independente de Bombeiros Militar, unidades "
            "subordinadas diretamente ao Comando Operacional de Bombeiros, realizar ações de "
            "prevenção e combate a incêndio, busca e salvamento, socorros de urgência e defesa "
            "civil"
        ),
        "competencias": [],
        "source": "cf. CBMMG, LOB (LC nº 54/1999), Art. 27",
        "organName": "Companhia Independente de Bombeiros Militar", "abbr": "CIA IND BM",
    },
}


def lob_enrich_for(organ_key: str, state_id: str):
    """Entrada curada da LOB para (órgão, estado), ou None."""
    return LOB_ENRICHMENT.get((organ_key, state_id))
