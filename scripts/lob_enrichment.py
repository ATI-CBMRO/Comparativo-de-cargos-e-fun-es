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
}


def lob_enrich_for(organ_key: str, state_id: str):
    """Entrada curada da LOB para (órgão, estado), ou None."""
    return LOB_ENRICHMENT.get((organ_key, state_id))
