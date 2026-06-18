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
     unidade, a partir das leis/RIs de PR, MT, ES, PA, SC, BA e PE.

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


# Mapeamento organ_key -> competências verbatim de outras legislações (rotuladas).
ENRICHMENT_ORGAN = {
    "dpo":  _tag(_MT_DOP,  "cf. CBMMT, RI, Art. 236")
          + _tag(_PA_COP,  "cf. CBMPA, Lei nº 11.060/2025, Art. 16")
          + _tag(_BA_COBM, "cf. CBMBA, Lei nº 14.572/2023, Art. 49, III"),
    "cot":  _tag(_MT_DSCI, "cf. CBMMT, RI, Art. 198")
          + _tag(_ES_CAT,  "cf. CBMES, NGA — Centro de Atividades Técnicas")
          + _tag(_SC_DSCI, "cf. CBMSC, Dec. nº 1.328/2021, Art. 38")
          + _tag(_BA_CSCI, "cf. CBMBA, Lei nº 14.572/2023, Art. 49, IV")
          + _tag(_PE_CAT,  "cf. CBMPE, Lei nº 15.187/2013, Art. 97"),
    "crbm": _tag(_SC_RBM,  "cf. CBMSC, Dec. nº 1.328/2021, Art. 39"),
    "bbm":  _tag(_PR_BBM,  "cf. CBMPR, Lei nº 22.206/2024, Art. 35, I"),
    "cibm": _tag(_PR_CIBM, "cf. CBMPR, Lei nº 22.206/2024, Art. 35, II"),
    "bbs":  _tag(_PR_GOST, "cf. CBMPR, Lei nº 22.206/2024, Art. 35, III"),
    "boa":  _tag(_PR_UOA,  "cf. CBMPR, Lei nº 22.206/2024, Art. 35, IV"),
}


def enrich_organ_for(organ_key: str):
    """Itens de enriquecimento de competência do órgão [{text, source}]; [] se não houver."""
    return list(ENRICHMENT_ORGAN.get(organ_key, []))
