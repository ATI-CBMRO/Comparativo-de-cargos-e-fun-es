"""
minuta_enrichment.py — Portal CBM

Enriquecimento CURADO de competências por função operacional, extraído VERBATIM
de regimentos internos de outros CBMs, para níveis onde o detalhamento do CBMRO
(ro.json) é raso. Cada item carrega a citação da fonte.

Consumido apenas por build_minuta_structure.py. NÃO altera ro.json.

Dois níveis de enriquecimento:
  1. ENRICHMENT — por CARGO/função, chave (organ_key, token_da_funcao):
     atribuições pessoais do comando, a partir do RI do CBMAL (Arts. 107/114/115).
     token_da_funcao normaliza o nome do cargo ('comandante', 'adjunto', etc.).
  2. ENRICHMENT_ORGAN — por ÓRGÃO, chave organ_key: competências/missões da
     unidade, a partir das leis/RIs de PR, MT, ES, PA, SC, BA, PE, CE, SP e DF.

Cada item carrega a citação da fonte. Expansível adicionando novas entradas.
"""

# ── CBMAL, RI, Art. 107 — Comandante Operacional de Bombeiro (≈ Comandante Regional) ──
_AL_ART_107 = [
    "planejar, coordenar e fiscalizar as ações operacionais e administrativas no âmbito de sua competência",
    "manter o registro dos principais pontos de riscos existentes nas áreas de atuação, desenvolvendo planos setoriais para protegê-las",
    "controlar e fiscalizar as condições e nível de adestramento da tropa sob sua responsabilidade, elaborando e fiscalizando o fiel cumprimento das notas de serviço, notas de instrução e planos operacionais",
    "planejar, coordenar e fiscalizar a manutenção do material e equipamento, e manter registros dos bens móveis que estiverem sob sua responsabilidade",
    "manter o registro estatístico das ocorrências verificadas nas áreas de atuação das Unidades Operacionais (UOp) e Subunidades subordinadas, e realizar estudos para o aperfeiçoamento da prevenção e eficácia do atendimento nas ocorrências",
    "planejar, coordenar e fiscalizar o cumprimento da legislação referente à prevenção de incêndio",
    "manter, em perfeito funcionamento, o serviço de comunicações das respectivas Unidades e Subunidades, através do Centro de Operações e Comunicações (COC)",
    "planejar, coordenar, fiscalizar e executar a movimentação do pessoal lotado no Comando Operacional de Bombeiros",
    "adotar medidas que visem a informatização e a agilização das ações administrativas e operacionais das diversas UOp e Subunidades sob seu comando",
    "controlar e fiscalizar a carga de bens patrimoniais que estiverem sob sua responsabilidade",
    "elaborar o Regimento Interno do Comando Operacional de Bombeiros, remetendo-o ao Comandante Geral para aprovação",
    "analisar, aprovar e ou modificar, em comum acordo com os Comandantes das Unidades Operacionais e o Subcomandante Geral, as Normas Gerais de Ações das diversas UOp e Subunidades, remetendo as propostas ao Comandante Geral para aprovação",
    "encaminhar ao Comandante Geral os Regimentos Internos das UOp e Subunidades subordinadas",
    "cumprir e fazer cumprir as normas regulamentares de prevenção e proteção contra incêndio, pânico, salvamento e resgate",
    "controlar, fiscalizar e exigir o cumprimento das atividades de instrução das UOp e Subunidades subordinadas",
    "praticar atos administrativos necessários ao perfeito funcionamento das atividades operacionais",
    "comunicar, de imediato, ao Comandante Geral fatos graves que ocorram nas áreas de suas UOp e Subunidades subordinadas",
    "presidir solenidades de passagem de comando de suas UOp e Subunidades, quando não presentes o Comandante ou o Subcomandante Gerais",
    "controlar e zelar pela conservação dos bens móveis e imóveis sob sua responsabilidade",
    "delegar competência aos comandantes de UOp e Subunidades",
    "manter contato com as demais organizações da Corporação ou com autoridades e ou órgãos externos, visando um melhor desempenho de suas atividades",
    "movimentar oficiais e praças entre as UOp e Subunidades, com prévio conhecimento do Comandante Geral",
    "designar comissões para inventariar bens de bombeiros militares desertores, falecidos ou desaparecidos nas áreas de competência das respectivas UOp e Subunidades",
    "exercer outras atribuições que lhe forem determinadas pelo Comandante Geral",
    "propor ao Conselho de Políticas Estratégicas normas, instruções técnicas e procedimentos operacionais para o aprimoramento das atividades da Corporação",
]

# ── CBMAL, RI, Art. 114 — Comandante de Grupamento (≈ Comandante de Batalhão) ──
_AL_ART_114 = [
    "dirigir, cumprir e fazer cumprir as atividades relacionadas à prevenção, combate a incêndios e salvamento em altura e terrestre na sua área de atuação",
    "praticar os atos administrativos necessários ao perfeito funcionamento da Unidade e de suas subunidades",
    "manter a tropa permanentemente adestrada e pronta para o emprego",
    "comandar diretamente as atividades operacionais que envolvam mais de uma operação de socorro bombeiro militar na área de atuação das subunidades",
    "desenvolver o espírito de iniciativa e camaradagem de seus subordinados",
    "comunicar imediatamente à autoridade superior qualquer fato grave ocorrido em sua área de atuação, solicitando intervenção nos casos que exijam a participação de outros órgãos",
    "controlar e zelar pela conservação e manutenção dos bens móveis e imóveis sob sua responsabilidade",
    "providenciar a manutenção dos bens patrimoniais sob sua guarda",
    "elaborar e submeter à aprovação do escalão superior as Normas Gerais de Ação dos órgãos da Unidade",
    "movimentar os oficiais e praças no âmbito das respectivas subunidades",
    "controlar e fiscalizar a execução, no âmbito das respectivas subunidades operacionais, dos planos e ordens superiores",
    "elaborar e manter atualizado o quadro estatístico de ocorrências operacionais de suas subunidades",
    "executar atos administrativos que lhe competirem, como integrante do sistema de administração de pessoal e material",
    "instaurar sindicância",
    "exercer outros encargos que lhe forem atribuídos pelo Comandante Geral ou previstos em leis e regulamentos vigentes",
]

# ── CBMAL, RI, Art. 115 — Subcomandante de Unidade Operacional (≈ Adjunto de unidade) ──
_AL_ART_115 = [
    "assessorar o seu Comandante em todas as suas atribuições",
    "tomar as providências necessárias ao fiel cumprimento das ordens do seu Comandante",
    "fiscalizar e orientar os trabalhos dos órgãos da Unidade",
    "fiscalizar os serviços de escala da Unidade",
    "responder pelo Comandante nos seus impedimentos",
    "assinar, por delegação do respectivo comandante, os atos administrativos que não forem de exclusividade daquela autoridade e sejam compatíveis com as normas vigentes",
    "fiscalizar e controlar a instrução da Unidade",
    "responsabilizar-se pela carga da Unidade",
    "exercer o controle disciplinar dos integrantes da Unidade",
]


def _tag(items, source):
    return [{"text": t, "source": source} for t in items]


# Mapeamento (organ_key, token) -> itens enriquecidos rotulados.
ENRICHMENT = {
    ("crbm", "comandante"):  _tag(_AL_ART_107, "cf. CBMAL, RI, Art. 107"),
    ("crbm", "adjunto"):     _tag(_AL_ART_115, "cf. CBMAL, RI, Art. 115"),
    ("bbm",  "comandante"):  _tag(_AL_ART_114, "cf. CBMAL, RI, Art. 114"),
    ("cibm", "comandante"):  _tag(_AL_ART_114, "cf. CBMAL, RI, Art. 114"),
    ("bbs",  "comandante"):  _tag(_AL_ART_114, "cf. CBMAL, RI, Art. 114"),
    ("bifea","comandante"):  _tag(_AL_ART_114, "cf. CBMAL, RI, Art. 114"),
    ("boa",  "comandante"):  _tag(_AL_ART_114, "cf. CBMAL, RI, Art. 114"),
}


def function_token(cargo_name: str) -> str:
    """Reduz o nome de um cargo a um token de função para casar com ENRICHMENT."""
    n = (cargo_name or "").lower()
    if "companhia" in n:
        return "comandante-de-companhia"
    if "subcomandante" in n:
        return "subcomandante"
    if "adjunto" in n:
        return "adjunto"
    if "coordenador" in n:
        return "coordenador"
    if "diretor" in n:
        return "diretor"
    if "comandante" in n:
        return "comandante"
    if "chefe" in n:
        return "chefe"
    return n.strip()


def enrich_for(organ_key: str, cargo_name: str):
    """Itens de enriquecimento [{text, source}] para uma função; [] se não houver."""
    return list(ENRICHMENT.get((organ_key, function_token(cargo_name)), []))


# ─────────────────────────────────────────────────────────────────────────────
# Enriquecimento em NÍVEL DE ÓRGÃO (competência do órgão), com missões/competências
# verbatim das leis e regimentos de PR, MT, ES e PA. Diferente do enriquecimento
# por cargo (CBMAL acima): aqui as leis descrevem a MISSÃO/competência da unidade
# (não as atribuições pessoais do comandante), o que casa com a competência do órgão.
# ─────────────────────────────────────────────────────────────────────────────

# ── CBMPR, Lei nº 22.206/2024, Art. 35, I — missões do Batalhão (BBM) ──
_PR_BBM = [
    "coordenar e executar as atividades de defesa civil",
    "exercer o poder de polícia administrativa referente à prevenção a incêndios e desastres",
    "combater incêndios e desastres",
    "prevenir acidentes na orla marítima e fluvial",
    "realizar buscas, salvamentos, socorros públicos e atendimento pré-hospitalar",
]

# ── CBMPR, Lei nº 22.206/2024, Art. 35, II — Companhia Independente (Cia. Ind. BM) ──
_PR_CIBM = [
    "exercer, em áreas de menores dimensões não incluídas na circunscrição de um Batalhão, "
    "as mesmas atribuições do Batalhão de Bombeiro Militar",
]

# ── CBMPR, Lei nº 22.206/2024, Art. 35, III — Grupo de Operações de Socorro Tático (GOST) ──
_PR_GOST = [
    "executar a missão especializada de socorro tático em todas as atividades de bombeiro-militar",
    "realizar ações de atendimento às emergências ambientais e a sinistros decorrentes de "
    "desastres naturais e antropogênicos",
    "organizar forças-tarefas",
    "desempenhar atividades de busca e salvamento, inclusive com a utilização de cães",
]

# ── CBMPR, Lei nº 22.206/2024, Art. 35, IV — Unidade de Operações Aéreas (UOA) ──
_PR_UOA = [
    "atender e apoiar ações de busca, resgate e salvamento a vítimas de acidentes e/ou traumas "
    "em áreas urbanas, rurais e rodovias",
    "atender e apoiar ações de busca e resgate de vítimas em matas, florestas, montanhas, rios, "
    "lagos e mar",
    "atuar em missões de apoio à defesa civil",
    "apoiar órgãos federais, estaduais e municipais que necessitem do emprego de aeronaves",
]

# ── CBMMT, RI, Art. 236 — competências da Diretoria Operacional ──
_MT_DOP = [
    "planejar e coordenar o emprego operacional da instituição",
    "manter registro das atividades operacionais da instituição",
    "manter estreito relacionamento com outros órgãos de segurança para a realização de "
    "operações conjuntas",
    "coordenar e controlar todos os serviços de comunicações e ações operacionais",
    "elaborar o planejamento operacional da instituição em grandes eventos",
    "interagir com demais órgãos administrativos e operacionais, visando obter subsídios para o "
    "planejamento operacional",
    "estabelecer unidade de doutrina entre os Comandos Regionais e Unidades Operacionais "
    "subordinadas",
    "planejar a instalação e viabilizar a construção de novas Unidades Operacionais no Estado",
]

# ── CBMMT, RI, Art. 198 — competências da Diretoria de Segurança Contra Incêndio e Pânico ──
_MT_DSCI = [
    "regulamentar as medidas de segurança contra incêndio e pânico no âmbito do Estado",
    "realizar pesquisa e perícia de incêndio, relacionadas com sua competência",
    "analisar os documentos que compõem os Processos de Segurança Contra Incêndio e Pânico "
    "com o fim de verificar a conformidade destes com a legislação",
    "realizar a vistoria nas edificações, instalações e locais de risco permanentes ou temporários",
    "expedir os Alvarás de Prevenção Contra Incêndio e Pânico e de Aprovação do Processo de "
    "Segurança Contra Incêndio e Pânico",
    "cassar os Alvarás de Prevenção Contra Incêndio e Pânico e os de Aprovação do Processo de "
    "Segurança Contra Incêndio e Pânico",
    "notificar, multar, interditar ou embargar as edificações, instalações e locais de risco que não "
    "estiverem em conformidade com as exigências da legislação e normas técnicas",
    "capacitar, fiscalizar e controlar as atividades dos órgãos e das entidades civis que atuam em "
    "sua área de competência",
]

# ── CBMES, NGA — Centro de Atividades Técnicas ──
_ES_CAT = [
    "planejar, executar, controlar e fiscalizar as atividades de proteção contra incêndio",
    "realizar perícias de incêndio e vistorias",
]

# ── CBMPA, Lei nº 11.060/2025, Art. 16 — Comando de Operações ──
_PA_COP = [
    "exercer a direção e o controle dos órgãos de direção intermediária e setorial",
    "exercer a direção e o controle do apoio e da execução da atividade-fim",
]

# ── CBMSC, Dec. nº 1.328/2021, Art. 39 — Região Bombeiro Militar (comando regional) ──
_SC_RBM = [
    "inspecionar periodicamente as Organizações Bombeiro Militar subordinadas",
    "coordenar, controlar, fiscalizar e apoiar as ações operacionais que ultrapassem a "
    "circunscrição ou a esfera de competência do comando da unidade operacional subordinada",
    "supervisionar a gestão de convênios, fundos municipais e instrumentos congêneres no âmbito "
    "da circunscrição",
    "orientar e acompanhar o desempenho administrativo e operacional dos elementos subordinados "
    "por meio de ações de comando e de ferramentas sistêmicas, visando o aprimoramento de resultados",
    "fiscalizar, na circunscrição da Região, a gestão das Centrais de Emergências e congêneres",
    "emitir ordens administrativas e operacionais visando regular as ações de coordenação, controle "
    "e fiscalização sobre os órgãos de execução de sua circunscrição",
    "instaurar inquéritos, sindicâncias e outros procedimentos administrativos pertinentes à "
    "manutenção da disciplina no âmbito dos Comandos Regionais",
    "definir o emprego de Força-Tarefa, de acordo com as diretrizes do Comando-Geral, no âmbito "
    "de sua respectiva circunscrição",
    "autorizar deslocamentos dos seus subordinados a serviço e dentro do território estadual",
]

# ── CBMSC, Dec. nº 1.328/2021, Art. 38 — Diretoria de Segurança Contra Incêndio ──
_SC_DSCI = [
    "a normatização em segurança contra incêndio, pânico e desastre",
    "a análise de projetos e vistorias",
    "o exercício do Poder de Polícia Administrativa",
    "a investigação de incêndio e explosão",
    "a pesquisa e desenvolvimento em segurança contra incêndio, pânico e desastre",
]

# ── CBMBA, Lei nº 14.572/2023, Art. 49, III — Comando de Operações de Bombeiros (COBM) ──
_BA_COBM = [
    "planejar, organizar, supervisionar, coordenar e controlar as atividades de prevenção e combate "
    "a incêndios, busca, salvamento e defesa civil, com atuação nas regiões do Estado",
]

# ── CBMBA, Lei nº 14.572/2023, Art. 49, IV — Comando de Segurança Contra Incêndio (CSCI) ──
_BA_CSCI = [
    "planejar, executar, controlar e fiscalizar as atividades de proteção contra incêndio",
    "planejar, executar e controlar as ações de perícia de incêndio",
    "promover ações de prevenção contra incêndio",
    "propor estudos e pesquisas que viabilizem a melhoria das atividades de segurança contra "
    "incêndio, elaborando diretrizes da política institucional relativas à sua área de atuação",
]

# ── CBMPE, Lei nº 15.187/2013, Art. 97 — competências operacionais distintivas dos CATs ──
_PE_CAT = [
    "planejar, comandar e fiscalizar as ações operacionais da unidade",
    "comunicar imediatamente ao escalão superior qualquer fato ou situação em sua área de atuação, "
    "solicitando-lhe intervenção, se não for de sua competência providenciar a respeito",
    "comandar diretamente as ações que, pela gravidade, vulto, importância e complexidade assim o "
    "exigirem",
]

# ── CBMCE, Lei nº 13.438/2004, Art. 17 — Coordenadoria de Atividades Técnicas ──
_CE_CAT = [
    "gerenciar o sistema de informações no que diz respeito à análise, cadastro e controle de dados",
    "desenvolver pesquisa científica e avaliar o desempenho operacional da Corporação",
    "analisar projetos de edificações, vistorias e pareceres técnicos",
    "controlar, manter e manobrar hidrantes",
]

# ── CBMSP, Lei nº 616/1974, Art. 40, §2º, 7 — Seção de Serviço Técnico (B/6) ──
_SP_TEC = [
    "executar e supervisionar o disposto na legislação do Estado quanto à instalação de equipamentos "
    "e às medidas preventivas contra incêndios",
    "proceder a exames de plantas e a perícias",
    "realizar testes de incombustibilidade",
    "realizar vistorias e emitir pareceres",
    "supervisionar a instalação da rede de hidrantes públicos",
]

# ── CBMDF, RI (Portaria nº 24/2020), Art. 454 — Comando Operacional (COMOP) ──
_DF_COMOP = [
    "realizar o planejamento estratégico setorial, a coordenação e o emprego das unidades subordinadas",
    "manter a tropa permanentemente treinada para pronto emprego",
    "planejar, controlar e executar atividades de prevenção e combate a incêndio, busca, salvamento e "
    "resgate, atendimento pré-hospitalar, proteção civil, proteção ambiental, operações aéreas e guarda "
    "e segurança em suas unidades operacionais",
    "expedir Instrução Normativa a fim de orientar o público interno quanto à padronização de "
    "procedimentos operacionais e administrativos relacionados com a sua área de competência",
    "planejar, coordenar e executar a movimentação dos bombeiros militares e dos recursos materiais "
    "destinados ao Comando Operacional",
    "elaborar os pedidos de aquisição de material e execução de serviços necessários à execução das "
    "suas atividades",
]

# ── CBMDF, RI (Portaria nº 24/2020), Art. 54 — Departamento de Segurança Contra Incêndio (DESEG) ──
_DF_DESEG = [
    "realizar atividades de segurança contra incêndio e pânico, com vistas à proteção das pessoas e "
    "dos bens públicos e privados",
    "realizar perícias em incêndio e explosões",
    "planejar, orientar, coordenar e controlar as atividades de segurança contra incêndio e pânico "
    "relacionadas a credenciamento e fiscalização; serviço de hidrante urbano; proposição de normas, "
    "programas e diretrizes; análise de projetos de instalações de proteção contra incêndio e pânico e "
    "de arquitetura; prevenção e proteção contra incêndio e pânico; e investigação de incêndios",
    "promover e participar de campanhas educativas direcionadas à comunidade em sua área de atuação",
    "realizar pesquisas técnico-científicas, com vistas à obtenção de produtos e processos, que "
    "permitam o desenvolvimento de sistemas de segurança contra incêndio e pânico",
    "fiscalizar, na área de sua competência, o cumprimento da legislação referente à prevenção contra "
    "incêndio e pânico",
    "realizar vistorias e emitir pareceres técnicos com possíveis consequências de penalidades por "
    "infração, na forma da legislação específica",
    "credenciar os agentes fiscalizadores para realizar as vistorias técnicas",
]


# ── CBMMT, RI, Art. 14 — Estado Maior-Geral (cg) ──
_MT_EMG = [
    "assessorar o Comandante-Geral nos níveis mais elevados das atividades desenvolvidas pela "
    "Instituição",
    "realizar estudos e planejamentos, coordenando, fiscalizando e controlando todas as atividades "
    "da Instituição, para assegurar o seu mais eficiente emprego como um todo",
    "elaborar diretrizes e legislações internas, planos e ordens a serem baixadas pelo "
    "Comandante-Geral, que acionam os órgãos de direção setorial, de apoio e de execução, no "
    "cumprimento de suas missões",
    "supervisionar a execução dos planos e das ordens baixadas pelo Comandante-Geral, e tomar as "
    "providências necessárias à consecução dos objetivos da Instituição",
    "supervisionar a parte disciplinar dos Bombeiros Militares",
    "acompanhar o desenvolvimento das políticas salariais estabelecidos pelo Comandante-Geral, a "
    "fim de mantê-lo informado dos objetivos alcançados e de sua evolução",
]

# ── CBMPA, RI, Art. 6 — Comando-Geral (cg), órgão de assessoramento ao Comandante-Geral ──
_PA_CG = [
    "assessorar o Comandante-Geral na adoção de decisões técnicas e administrativas",
    "auxiliar o Comandante-Geral na elaboração e cumprimento do plano de comando",
    "acompanhar os programas, projetos e atividades da Corporação, mantendo o Comandante-Geral "
    "informado sobre o andamento das ações",
]

# ── CBMDF, RI (Portaria nº 24/2020), Art. 58 — Estado-Maior-Geral (cg) ──
_DF_EMG = [
    "elaborar a política militar, o planejamento estratégico e a orientação do preparo e emprego "
    "da Corporação, em conformidade com as diretrizes do Comando-Geral",
    "realizar estudos e elaborar o planejamento geral das atividades da Corporação",
    "elaborar diretrizes e ordens do comando",
    "elaborar e controlar a programação orçamentária e financeira da Corporação",
    "formular diretrizes para as áreas de: recursos humanos; logística, orçamento e finanças; "
    "ensino, pesquisa, ciência e tecnologia; segurança contra incêndio e emprego operacional; "
    "estatística e geoprocessamento; governança, gestão estratégica, gestão de riscos, "
    "gerenciamento de projetos e de processos",
    "analisar e encaminhar propostas de regulamentos, normas, planos, ordens, manuais e outras "
    "diretrizes para apreciação do Comandante-Geral",
    "desenvolver, coordenar, controlar e revisar a gestão estratégica do CBMDF",
    "estabelecer indicadores de qualidade e produtividade",
    "sugerir temas de pesquisa aos cursos de carreira da Corporação",
    "consolidar o processo de tomadas de contas anual dos ordenadores de despesas da Corporação",
    "indicar os projetos estratégicos e de captação de recursos não contemplados no PARF, que "
    "serão validados pelo Alto Comando e aprovados pelo Comandante-Geral",
    "validar o Plano de Contratações Anual - PCA do CBMDF elaborado pelo DEALF",
]

# ── CBMAL, RI, Art. 13 — Coordenadoria Estadual de Defesa Civil (depdec) ──
_AL_CEDEC = [
    "promover, coordenar e supervisionar, no âmbito estadual, as ações de defesa civil",
    "elaborar e encaminhar à deliberação do Conselho Estadual de Defesa Civil os planos, programas "
    "e projetos com vistas à defesa permanente contra os desastres naturais ou provocados pelo "
    "homem, especialmente contra as secas e inundações",
    "mobilizar recursos humanos e materiais necessários às ações de defesa civil",
    "elaborar e encaminhar à deliberação do Conselho Estadual de Defesa Civil as políticas e "
    "diretrizes da ação governamental de defesa civil e promover a sua implementação",
    "promover estudos referentes às causas e possibilidades de ocorrência de desastres de qualquer "
    "origem, sua incidência, extensão e conseqüências",
    "consolidar e compatibilizar planos e programas globais, regionais e setoriais, observadas as "
    "políticas e as diretrizes da ação governamental de defesa civil",
    "incentivar a criação e a implementação de Coordenadorias Municipais de Defesa Civil - COMDEC",
    "sistematizar e integrar informações no âmbito do Sistema Estadual de Defesa Civil",
    "definir e encaminhar à deliberação do Conselho Estadual de Defesa Civil as áreas e as ações "
    "prioritárias para investimentos que contribuam para minimizar a vulnerabilidade das cidades ou "
    "regiões do Estado",
    "propor ao Governador do Estado a homologação de situação de emergência ou de estado de "
    "calamidade pública, obedecidos os critérios estabelecidos pelos Conselhos Nacional e Estadual "
    "de Defesa Civil",
    "promover a capacitação de recursos humanos para as ações de defesa civil, em articulação com "
    "os órgãos estaduais e municipais especializados",
    "propor ao Conselho Estadual de Defesa Civil a criação de comissões técnicas "
    "interinstitucionais para a realização de estudos, pesquisas e trabalhos especializados de "
    "interesse da defesa civil",
    "coordenar e controlar a distribuição de suprimentos às populações atingidas por desastres, em "
    "articulação com as Coordenadorias Regionais e Municipais de Defesa Civil e órgãos "
    "assistenciais integrantes do Sistema Estadual de Defesa Civil",
    "criar grupos de trabalho com o objetivo de prestar o apoio técnico necessário à atuação dos "
    "órgãos e entidades na área de defesa civil",
    "receber, analisar e opinar sobre relatórios e pleitos relativos à declaração de situação de "
    "emergência e estado de calamidade pública",
    "manter o órgão central do Sistema Nacional de Defesa Civil - SINDEC informado sobre a "
    "ocorrência de desastre e atividades de defesa civil",
    "prestar apoio técnico e administrativo ao Conselho Estadual de Defesa Civil e à Junta "
    "Administrativa do Fundo Estadual de Defesa Civil - FUNDEC, criado na forma da lei",
    "coordenar e promover, em articulação com os municípios, a execução das ações conjuntas dos "
    "órgãos integrantes do Sistema Estadual de Defesa Civil",
    "elaborar e apresentar ao órgão competente a proposta orçamentária destinada às atividades de "
    "defesa civil, na forma de legislação vigente",
    "manter intercâmbio com os órgãos federais, estaduais e municipais de defesa civil",
    "acompanhar e avaliar o desempenho do Sistema Estadual de Defesa Civil",
    "apresentar o relatório anual de suas atividades",
    "exercer outras ações, atividades e funções estabelecidas em lei, regulamento ou decisão do "
    "Conselho Estadual de Defesa Civil",
]

# ── CBMGO, Lei nº 18.305/2013, Art. 27 — Comando de Operações de Defesa Civil (depdec) ──
_GO_CODEC = [
    "elaborar planos de gestão operacional nos assuntos relacionados a defesa civil",
    "coordenar as atividades de planejamento, contingência, socorro e reconstrução relacionadas a "
    "defesa civil",
    "realizar ações de prevenção contra incêndio e pânico e de defesa civil por meio dos órgãos de "
    "execução",
    "planejar, controlar e fiscalizar as atividades relacionadas à análise de projetos e inspeções "
    "nas edificações e áreas de risco",
    "elaborar projetos e coordenar programas relacionados à política estadual de Defesa Civil, "
    "além de outras definidas em regulamento",
]

# ── CBMES, NGA, Art. 3 — Coordenadoria Estadual de Proteção e Defesa Civil (depdec) ──
_ES_CEPDEC = [
    "articular e coordenar as ações de proteção e defesa civil no Estado do Espírito Santo, "
    "compreendendo: prevenção e preparação para desastres; assistência e socorro às vítimas das "
    "calamidades; restabelecimento de serviços essenciais; reconstrução; e realizar estudos e "
    "pesquisas sobre riscos e desastres",
    "elaborar e implementar diretrizes, planos, programas e projetos para prevenção, preparação, "
    "mitigação, recuperação e respostas a desastres causados por ação da natureza e/ou do homem no "
    "âmbito do Estado",
    "coordenar a elaboração do plano de contingência estadual de Proteção e Defesa Civil e fomentar "
    "a elaboração dos planos de contingência municipais",
    "mobilizar recursos para prevenção, preparação, mitigação, resposta e recuperação dos desastres",
    "disseminar a cultura de prevenção por meio da inclusão dos princípios de proteção e defesa "
    "civil na sociedade e do fomento, nos municípios",
    "prestar informações à Secretaria Nacional de Proteção e Defesa Civil - SEPDEC ou órgão "
    "correspondente sobre as ocorrências de desastres e atividades de proteção e defesa civil no "
    "Estado",
    "propor à autoridade competente a decretação ou a homologação de situação de emergência e de "
    "estado de calamidade pública",
    "apoiar a União quando solicitado, no reconhecimento de situação de emergência e estado de "
    "calamidade pública",
    "providenciar e gerenciar a distribuição e o abastecimento de suprimentos necessários nas ações "
    "de proteção e defesa civil",
    "articular-se com as demais Secretarias de Estado para promoção das ações de proteção e defesa "
    "civil na região atingida",
    "coordenar as ações estaduais de ajuda humanitária nacional e internacional",
    "coordenar e promover, em articulação com os municípios, a implementação de ações conjuntas dos "
    "órgãos integrantes do SIEPDEC-ES",
    "promover o intercâmbio técnico entre instituições e organizações nacionais e internacionais de "
    "proteção e defesa civil",
    "promover a capacitação de pessoas para as ações de proteção civil, em articulação com órgãos "
    "do SIEPDEC-ES",
    "fomentar o fortalecimento da estrutura de proteção e defesa civil municipal e regional",
    "determinar a interdição de edificações, construções e áreas em situação considerada por "
    "profissional competente como sendo de risco para a vida humana",
    "identificar e mapear as áreas de risco e realizar estudos de identificação de ameaças, "
    "suscetibilidades e vulnerabilidades, em articulação com a União e os Municípios",
    "realizar o monitoramento meteorológico, hidrológico e geológico das áreas de risco, em "
    "articulação com a União e os Municípios",
    "apoiar, sempre que necessário, os municípios no levantamento das áreas de risco, na elaboração "
    "dos Planos de Contingência de Proteção e Defesa Civil e na divulgação de protocolos de "
    "prevenção e alerta e de ações emergenciais",
]

# ── CBMAL, RI, Art. 11 — Conselho de Políticas Estratégicas (condeg) ──
_AL_CPE = [
    "planejar e executar as atividades de administração do pessoal Bombeiro Militar e Civil da "
    "Corporação",
    "estudar, emitir parecer e elaborar expediente relativo aos assuntos que lhe foram atribuídos",
    "assessorar nos assuntos referentes ao planejamento, coordenação e fiscalização das atividades "
    "operacionais e de administração da corporação",
    "propor, com base nos estudos realizados, as medidas necessárias ao aperfeiçoamento das "
    "atividades técnicas especializadas de bombeiros",
    "obter informações e fazer levantamento das rotinas e procedimentos operacionais, objetivando a "
    "melhor eficácia na execução do serviço e tarefas especializadas a cargo da Corporação",
    "acompanhar a evolução doutrinária dos assuntos de sua competência, bem como realizar estudos "
    "para definir, consolidar e aprimorar a doutrina de informações de interesse da instituição",
    "solucionar processos administrativos e submetê-los à decisão do Comandante Geral, devidamente "
    "instruídos, os que lhe escapem à competência",
    "regular as rotinas e procedimentos relacionados com direitos e deveres e incentivos de pessoal",
    "supervisionar, dirigir e coordenar os trabalhos da Corporação, tendo em vista a unidade de "
    "ação no cumprimento de diretrizes",
    "cuidar do emprego de pessoal de acordo com as normas existentes",
]

# ── CBMMT, LC nº 775/2023, Art. 15 — Conselho Superior de Bombeiros Militar (condeg) ──
_MT_CSBM = [
    "apresentar propostas sobre matérias de cunho estratégico que promovam o aperfeiçoamento da "
    "instituição",
    "sugerir propostas que alterem a estrutura organizacional da instituição",
    "avaliar o emprego da instituição orientando a racionalização na aplicação de recursos e a "
    "maximização dos resultados em benefício da sociedade",
    "examinar a Política Estadual de Segurança Pública, em particular na parcela constitucional que "
    "compete ao Corpo de Bombeiros Militar e apresentar soluções para o aperfeiçoamento do sistema",
    "avaliar mudanças na política de emprego tático e técnico das diversas Unidades Bombeiro "
    "Militar que integram a Corporação, inclusive a articulação e desdobramento das mesmas, visando "
    "ao cumprimento das missões constitucionais",
    "analisar matérias de relevância, relativas à Corporação, dependentes de decisão governamental",
    "propor a criação de comissões técnicas e grupos de trabalho para a realização de pesquisas e "
    "estudos estratégicos e sistêmicos sobre assuntos de ordem técnica de interesse do Corpo de "
    "Bombeiros Militar",
    "aprovar proposta de denominação histórica de Unidades Bombeiro Militar",
    "apreciar outros assuntos do interesse da Corporação colocados em pauta pelo Comandante-Geral",
]


# Mapeamento organ_key -> competências verbatim de outras legislações (rotuladas).
ENRICHMENT_ORGAN = {
    "dpo":  _tag(_MT_DOP,   "cf. CBMMT, RI, Art. 236")
          + _tag(_PA_COP,   "cf. CBMPA, Lei nº 11.060/2025, Art. 16")
          + _tag(_BA_COBM,  "cf. CBMBA, Lei nº 14.572/2023, Art. 49, III")
          + _tag(_DF_COMOP, "cf. CBMDF, RI (Portaria nº 24/2020), Art. 454"),
    "cot":  _tag(_MT_DSCI,  "cf. CBMMT, RI, Art. 198")
          + _tag(_ES_CAT,   "cf. CBMES, NGA — Centro de Atividades Técnicas")
          + _tag(_SC_DSCI,  "cf. CBMSC, Dec. nº 1.328/2021, Art. 38")
          + _tag(_BA_CSCI,  "cf. CBMBA, Lei nº 14.572/2023, Art. 49, IV")
          + _tag(_PE_CAT,   "cf. CBMPE, Lei nº 15.187/2013, Art. 97")
          + _tag(_CE_CAT,   "cf. CBMCE, Lei nº 13.438/2004, Art. 17")
          + _tag(_SP_TEC,   "cf. CBMSP, Lei nº 616/1974, Art. 40, §2º, 7")
          + _tag(_DF_DESEG, "cf. CBMDF, RI (Portaria nº 24/2020), Art. 54"),
    "crbm": _tag(_SC_RBM,  "cf. CBMSC, Dec. nº 1.328/2021, Art. 39"),
    "bbm":  _tag(_PR_BBM,  "cf. CBMPR, Lei nº 22.206/2024, Art. 35, I"),
    "cibm": _tag(_PR_CIBM, "cf. CBMPR, Lei nº 22.206/2024, Art. 35, II"),
    "bbs":  _tag(_PR_GOST, "cf. CBMPR, Lei nº 22.206/2024, Art. 35, III"),
    "boa":  _tag(_PR_UOA,  "cf. CBMPR, Lei nº 22.206/2024, Art. 35, IV"),
    "cg":   _tag(_MT_EMG,    "cf. CBMMT, RI, Art. 14")
          + _tag(_PA_CG,     "cf. CBMPA, RI, Art. 6")
          + _tag(_DF_EMG,    "cf. CBMDF, RI (Portaria nº 24/2020), Art. 58"),
    "depdec": _tag(_AL_CEDEC, "cf. CBMAL, RI, Art. 13")
          + _tag(_GO_CODEC,  "cf. CBMGO, Lei nº 18.305/2013, Art. 27")
          + _tag(_ES_CEPDEC, "cf. CBMES, NGA, Art. 3"),
    "condeg": _tag(_AL_CPE,  "cf. CBMAL, RI, Art. 11")
          + _tag(_MT_CSBM,   "cf. CBMMT, LC nº 775/2023, Art. 15"),
}


def enrich_organ_for(organ_key: str):
    """Itens de enriquecimento de competência do órgão [{text, source}]; [] se não houver."""
    return list(ENRICHMENT_ORGAN.get(organ_key, []))


# ── CBMSE, RISD (Regulamento Interno dos Serviços Diários), Art. 14 — Comandante de Guarnição ──
_SE_CMT_GUARNICAO = [
    "cumprir e fazer cumprir todas as normas relativas ao serviço diário de sua competência",
    "apresentar-se ao Comandante de Socorro no início do serviço, transmitindo-lhe as condições "
    "dos equipamentos na viatura, depois de minuciosa conferência do material",
    "sair da base mediante exclusiva autorização dos superiores de serviço",
    "exercer o comando dos integrantes da guarnição com vista ao emprego tático da equipe",
    "controlar, no local da ocorrência, os materiais e equipamentos da viatura utilizados por sua "
    "guarnição",
    "estar atento à segurança do seu pessoal, do patrimônio e do meio ambiente no setor de sua "
    "responsabilidade",
    "responder pelo Comandante de Socorro por ocasião de atendimento a socorro isolado",
    "auxiliar o Comandante de Socorro a manter o moral e a disciplina da guarnição sob sua chefia, "
    "tanto dentro quanto fora da OBM",
    "providenciar a coleta de todos os dados da ocorrência exigidos pelo Centro de Operações para a "
    "execução dos procedimentos administrativos necessários",
    "informar ao Centro de Operações o momento exato de sua saída do quartel, de sua chegada e "
    "saída do local da ocorrência e de sua chegada ao quartel",
    "solicitar apoio ao Supervisor de Dia quando julgar necessário, se o Comandante de Socorro não "
    "estiver presente",
    "ministrar instrução para sua guarnição mediante orientação do Comandante de Socorro",
    "manter o Comandante de Socorro informado sobre o andamento da ocorrência, quando este não "
    "estiver presente no local",
    "informar ao Centro de Operações o desfecho final da ocorrência",
    "utilizar e exigir de todos da guarnição, obrigatoriamente, os Equipamentos de Proteção "
    "Individual (EPIs) disponíveis nas ocorrências em que for empregado",
    "coordenar e participar da conferência de materiais operacionais ao assumir o serviço e ao "
    "término de ocorrência",
]

# ── CBMSE, RISD, Art. 15 — Condutor e Operador de Viaturas ──
_SE_CONDUTOR = [
    "cumprir e fazer cumprir o disposto no Regimento",
    "conduzir a viatura com segurança até o local das ocorrências",
    "operar o corpo de bombas de modo a suprir de água, com vazão e pressão adequadas para as "
    "linhas de combate a incêndio armadas para tal finalidade",
    "se condutor e operador de plataforma mecânica ou escada mecânica, calçar e operar os engenhos "
    "destas viaturas de forma que possam ser utilizadas convenientemente e com segurança, para o "
    "combate e extinção de incêndios, salvamentos ou outros serviços para que forem designados",
    "se condutor e operador de viaturas de porte leve e/ou pesado sem corpo de bomba, conduzir a "
    "viatura de forma que possibilite condições favoráveis de segurança e trabalho para os militares "
    "de serviço, bem como a segurança e o bem-estar de pacientes transportados",
    "conduzir a viatura com prudência de modo que a guarnição, materiais e equipamentos "
    "transportados cheguem ao local das ocorrências e retornem ao quartel com segurança",
    "manter as viaturas em plenas condições de uso, executando os procedimentos de manutenção de "
    "1º escalão",
    "cumprir rigorosamente as ordens dadas pelo Comandante de Socorro durante todo o período em "
    "que estiver de prontidão",
    "comunicar ao Auxiliar de Manutenção e Transporte e/ou ao Comandante de Socorro as alterações "
    "encontradas na viatura ao assumir o serviço ou ocorridas durante a execução de missões de socorro",
    "passar a viatura ao seu sucessor, dando-lhe todas as informações necessárias sobre o estado "
    "geral da mesma, bem como das alterações existentes e ordens de serviço em vigor",
    "abastecer a viatura de combustível sempre que houver necessidade",
    "manter sempre abastecidos os tanques de água das viaturas de combate a incêndio",
    "cumprir normas e determinações específicas colocadas em vigor pelo Comando, pela Diretoria "
    "Operacional, pelo Departamento de Manutenção e pelo Comando do Batalhão",
    "utilizar, obrigatoriamente, os Equipamentos de Proteção Individual (EPIs) disponíveis e "
    "necessários nas ocorrências em que for empregado",
    "manter sua habilitação em dia, conforme exigência para ingresso no quadro de condutor",
]

# Capítulo da Guarnição de Serviço Operacional — a MENOR fração operacional.
# O CBMRO não a define na LOB/minuta (é matéria de regulamento de serviço); subsídio
# integral do CBMSE (RISD), rotulado. A finalidade é enquadramento institucional.
GUARNICAO_CHAPTER = {
    "chapterTitle": "DA GUARNIÇÃO DE SERVIÇO OPERACIONAL",
    "label": "Guarnição de Serviço Operacional",
    "abbr": "GuSv",
    "finalidade": (
        "A guarnição de serviço operacional é a menor fração empregada nas atividades operacionais "
        "do Corpo de Bombeiros Militar do Estado de Rondônia, constituída pela equipe da viatura em "
        "serviço, chefiada pelo militar mais antigo ou designado."
    ),
    "cargos": [
        ("Comandante de Guarnição",
         "Ao Comandante de Guarnição de serviço operacional compete:",
         _tag(_SE_CMT_GUARNICAO, "cf. CBMSE, RISD, Art. 14")),
        ("Condutor e Operador de Viatura",
         "Ao Condutor e Operador de Viatura compete:",
         _tag(_SE_CONDUTOR, "cf. CBMSE, RISD, Art. 15")),
    ],
}
