"""
minuta_enrichment.py — Portal CBM

Enriquecimento CURADO de competências por função operacional, extraído VERBATIM
de regimentos internos de outros CBMs, para níveis onde o detalhamento do CBMRO
(ro.json) é raso. Cada item carrega a citação da fonte.

Consumido apenas por build_minuta_structure.py. NÃO altera ro.json.

Chave: (organ_key, token_da_funcao) -> list[{"text", "source"}]
  token_da_funcao normaliza o nome do cargo: 'comandante', 'adjunto',
  'subcomandante', 'diretor', 'coordenador', 'comandante-de-companhia'.

Seed atual: cadeia de comando operacional a partir do CBMAL. Expansível
(PR/PA/MT/ES) adicionando novas entradas.
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
