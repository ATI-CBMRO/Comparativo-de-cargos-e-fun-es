"""Curadoria das sugestões da CONSULTA da Minuta do Regulamento de Serviço (ago/2026).

Regra definida pelo Ten. Tiago em 2026-09-14, para que a minuta que os militares leram
possa ser COMPARADA com a que resultou da consulta:

  CORRECOES  — correções ortográficas, de concordância, de citação e resíduos de extração:
               entram nas DUAS versões (a "em consulta" e a "atual"). O texto lido pelos
               militares só ganha o que era erro objetivo.
  ALTERACOES — reescritas de artigo, artigos/incisos novos e supressões: entram SÓ na
               versão ATUAL. Cada artigo reescrito ganha id NOVO com o campo `substitui`,
               de modo que os comentários dos militares (ancorados em editId#index) sigam
               apontando para o texto que eles leram, na versão em consulta, e nunca caiam
               no dispositivo errado na atual (armadilha AR-03).

Fonte das sugestões: coleção `suggestions` do portal (exportada em 11/09/2026) — 271
registros do Cel. BM Luiz Eduardo Oliveira Firmino (19 e 25/08/2026), 51 da equipe
(Ten. Tiago e Wândrio, 17-18/08) e os textos finais fechados pelo Ten. Tiago. Análise de
mérito em docs/sei/2026-09-11-regulamento-servico/Analise_Interacoes_e_Proposta_de_Aplicacao.md.

Decisões (Ten. Tiago, 2026-09-14): reescritas do Cel. só na atual; os três blocos que mudam
regra de mérito (Superior de Dia só na Capital; Comandante de Socorro só no 1º GBM; Oficial
de Dia como serviço interno do QCG) ENTRAM na atual marcados `proposta: True` com a nota
"pendente de deliberação do CONDEG".

Este módulo só descreve; quem aplica é `build_regulamento_structure_atual.py` (gera
database/atual/regulamento_structure_consulta.json e regulamento_structure.json).
"""
import copy

# ── Fundamentos ──────────────────────────────────────────────────────────────────────
_CEL = ('Sugestão do Cel. BM Luiz Eduardo Oliveira Firmino na consulta ao Regulamento de '
        'Serviço (19-25/08/2026)')
_F_LOB2 = f'{_CEL} — transcrição do Art. 2º da Lei nº 2.204/2009 (red. Lei nº 3.413/2014)'
_F_COB = f'{_CEL} — Lei nº 2.204/2009 (LOB), Art. 35 e parágrafo único (red. Lei nº 4.303/2018)'
_F_GBM = f'{_CEL} — Lei nº 2.204/2009 (LOB), Art. 47, § 1º (red. Lei nº 4.303/2018)'
_F_SGBM = f'{_CEL} — Lei nº 2.204/2009 (LOB), Art. 47 (red. Lei nº 4.303/2018)'
_F_SERV = f'{_CEL} — Lei nº 2.204/2009 (LOB), Art. 2º e Art. 35; RISD/CBMSE como texto de partida'
_F_FINAL = 'Texto final fechado pelo Ten. Tiago no Portal de Legislação CBM (17-18/08/2026) sobre a LOB, Lei nº 2.204/2009'

NOTA_PROPOSTA = ('PROPOSTA PENDENTE DE DELIBERAÇÃO DO CONDEG — muda regra de mérito em '
                 'relação à versão em consulta')

# ── CORREÇÕES (nas duas versões) ─────────────────────────────────────────────────────
# {tema: {id: {'caput': [(velho, novo), ...], 'items': [(velho, novo), ...]}}}
# Casamento por TEXTO (substring), nunca por índice. Todo `velho` PRECISA existir — o
# builder aborta se não achar (correção silenciosa que não aplica é pior que nenhuma).
CORRECOES = {
    'disposicoes-preliminares': {
        # Wândrio (17/08): a citação era a de Mato Grosso; em RO o CBM está no art. 148 da
        # Constituição Estadual. Texto final fechado pelo Ten. Tiago em 18/08.
        'mt-art-1': {'caput': [('Art. 82 da Constituição Estadual', 'Art. 148 da Constituição Estadual')]},
        # Wândrio (17/08): nome atual do sistema. Texto final fechado em 17/08.
        'mt-art-3': {'items': [('Sistema Estadual de Defesa Civil', 'Sistema Estadual de Proteção e Defesa Civil')]},
    },
    'servico-operacional': {
        # Sobra da quebra "Art. Nº" na extração do RISD de Sergipe.
        'se-art-1': {'caput': [('º O presente Regulamento', 'O presente Regulamento')]},
        'se-art-2': {'caput': [('º São objetivos', 'São objetivos')]},
        'se-art-3': {'caput': [('º Chama-se política', 'Chama-se política')]},
        'se-art-4': {'caput': [('º Visando a otimização', 'Visando a otimização')]},
        # Ten. Tiago (17/08, texto final): "para que concorre" → "para quem concorre".
        'se-art-23': {'items': [('As escalas para que concorre exclusivamente', 'As escalas para quem concorre exclusivamente')]},
        # Resíduos de título de seção da fonte grudados no fim do caput.
        'se-art-43': {'caput': [(' Comandante de Guarnição – Do Condutor e Operador de Viaturas – Dos Auxiliares da Guarnição e do Operador de Rádio', '')]},
        'se-art-44': {'caput': [('excepcion ais', 'excepcionais')]},
        'se-art-47': {'caput': [('pelo Comandante da OBM. Operações', 'pelo Comandante da OBM.')]},
        'se-art-112': {'caput': [('análise do comandante da OBM. durante Ocorrências', 'análise do comandante da OBM.')]},
        'se-art-115': {'caput': [('Comandante do incidente. com Distúrbios Mentais', 'Comandante do incidente.')]},
        'se-art-135': {'items': [('nos acidentes contra o meio ambiente. Grande Porte', 'nos acidentes contra o meio ambiente.')]},
        'se-art-147': {'caput': [('emprego desnecessário de bombeiros militares. Disposições Gerais', 'emprego desnecessário de bombeiros militares.')]},
    },
    'servico-interno-dia': {
        'se-art-78': {'caput': [('O acesso aos alojamento deve obedecer', 'O acesso aos alojamentos deve obedecer')]},
        'se-art-81': {'caput': [('ficando proibido a prática', 'ficando proibida a prática')]},
        'se-art-83': {'caput': [('deverá está consciente', 'deverá estar consciente')]},
        # Concordância: Central Integrada de Operações é feminino (achado 18/08).
        'se-art-85': {'caput': [('solicitar ao Central Integrada de Operações', 'solicitar à Central Integrada de Operações')]},
        'se-art-90': {'caput': [('lubrific ado', 'lubrificado')]},
        'se-art-91': {'caput': [('informar ao Central Integrada de Operações', 'informar à Central Integrada de Operações')]},
        'se-art-98': {'caput': [('o mlitar deverá trajar', 'o militar deverá trajar')]},
        'se-art-107': {'caput': [('condições de conserto no local. Operacional', 'condições de conserto no local.')]},
    },
    'disposicoes-finais': {
        # Resíduo da adaptação CBMMT→CBMRO: em RO as unidades são Grupamentos (LOB, Art. 47).
        'mt-art-264': {'caput': [('estabelecidas aos Batalhões Bombeiro Militar', 'estabelecidas aos Grupamentos de Bombeiro Militar')]},
        # Rodapé de publicação do Boletim de MT colado no caput do artigo de fecho.
        'mt-art-266': {'caput': [(' ** Este texto não substitui o publicado no Boletim Geral Eletrônico – BGE', '')]},
    },
}

# ── ALTERAÇÕES (só na versão atual) ───────────────────────────────────────────────────

# (1) Textos finais SUBSTANTIVOS fechados pelo Ten. Tiago no portal: mudam regra (a quem se
# reporta, quem autoriza, base legal), então só na atual. O id NÃO muda (é o mesmo artigo,
# com decisão do admin) — o artigo ganha `alterado: 'texto final'`.
TEXTOS_FINAIS_ATUAL = {
    'servico-operacional': {
        'se-art-24': {
            'caput': 'O serviço de Superior de Dia será realizado em regime de sobreaviso de 24 (vinte e quatro) horas, devendo o Oficial escalado não se ausentar da área de sua residência e permanecer com o telefone celular funcional ligado durante todo o dia de serviço ou outro meio de comunicação o qual deverá ser informado ao Subcomandante-Geral.',
            'items': {0: '§ 1º Ao final do serviço deverá assinar, via SEI, juntamente com o Oficial de Dia a Parte Diária.',
                      1: '§ 2º O regime do serviço poderá sofrer alterações mediante publicação em BG por determinação do Comandante-Geral ou pelo Subcomandante-Geral em virtude das necessidades do momento.'},
        },
        'se-art-25': {'caput': 'A permuta de serviço do Superior de Dia, só será permitida mediante autorização por escrito do Subcomandante-Geral do CBMRO, após publicação em Boletim Geral.'},
        'se-art-26': {'caput': 'O serviço diário de Superior de Dia ao CBMRO será coordenado pelo Subcomandante-Geral, através do gabinete do Subcomando-Geral.'},
        'se-art-27': {'caput': 'O regime da escala de serviços diários de Superior de Dia obedecerá ao critério de dias corridos, podendo, a critério do Subcomandante-Geral ser alterado.'},
        'se-art-29': {'caput': 'O militar que concorre à escala aqui tratada quando tiver que se ausentar ou retornar às suas atividades normais em decorrência de férias, dispensas, licenças ou que comporão as mesmas deverá se apresentar ao Subcomandante-Geral a fim de ser reinserido ou inserido na respectiva escala.'},
        'se-art-41': {'caput': 'Todos os aspectos relacionados ao serviço de Comandante de socorro e de Oficial de dia deverão observar às regras internas da OBM a que o Oficial estiver subordinado, além daquelas previstas neste Regulamento de Serviço.'},
        'se-art-45': {'caput': 'Todos os aspectos relacionados a esses serviços deverão observar às regras internas da OBM a que as praças estiverem subordinadas além daquelas previstas neste Regulamento de Serviço.'},
    },
}

# (2) Supressões — "Excluir" fechado pelo Ten. Tiago (18/08) + duplicidades apontadas na
# análise (se-art-36/37/38 repetem 29/30/31; 46/47 repetem 42/43). O bloco do Oficial de
# Dia (32-38) é substituído pelos artigos novos do Cel. (ver INCLUIR abaixo).
SUPRIMIR = {
    'servico-operacional': {
        'se-art-32': 'Excluir (Ten. Tiago, 18/08) — regime do Oficial de Dia refeito pelos artigos novos',
        'se-art-34': 'Excluir (Ten. Tiago, 18/08) — idem',
        'se-art-35': 'Excluir (Ten. Tiago, 18/08) — idem',
        'se-art-36': 'Excluir (Ten. Tiago, 18/08) — duplica se-art-29',
        'se-art-37': 'Excluir (Ten. Tiago, 18/08) — duplica se-art-30',
        'se-art-38': 'Excluir (Ten. Tiago, 18/08) — duplica se-art-31 e está no bloco errado',
        'se-art-46': 'Excluir (Ten. Tiago, 18/08) — duplica se-art-42',
        'se-art-47': 'Excluir (Ten. Tiago, 18/08) — duplica se-art-43',
    },
}


def _art(caput, dispositivos, fundamento, heading=None, orgao=None, proposta=False, nota=None):
    a = {'caput': caput, 'dispositivos': list(dispositivos), 'fundamento': fundamento}
    if heading:
        a['heading'] = heading
    if orgao:
        a['orgao'] = orgao
    if proposta:
        a['proposta'] = True
        a['nota'] = nota or NOTA_PROPOSTA
    elif nota:
        a['nota'] = nota
    return a


_H_COB = 'Cap. I — Das funções do Comando Operacional de Bombeiros'

# (3) Reescritas — o artigo antigo SAI da atual e entra(m) o(s) novo(s), com `substitui`.
# {tema: {id_antigo: [artigo_novo, ...]}}
SUBSTITUIR = {
    'disposicoes-preliminares': {
        'mt-art-3': [_art(
            'Compete ao Corpo de Bombeiros Militar, nos termos do art. 2º da Lei nº 2.204/2009, a execução das seguintes atividades:',
            [
                'I - realizar serviços de prevenção e extinção de incêndios, especialmente:',
                'a) em aglomerados urbanos;',
                'b) em florestas, particularmente em unidades de conservação, proteção e preservação ambiental;',
                'c) em veículos automotores ou não de qualquer natureza e porte; e',
                'd) em áreas de interesse estratégico e econômico.',
                'II - realizar serviços de busca e resgate de pessoas, animais, bens e haveres;',
                'III - realizar serviços de salvamentos de pessoas e animais;',
                'IV - realizar serviços de atendimento pré-hospitalar de pessoas em situação de emergência, oferecendo condições de suporte básico de vida até uma unidade de saúde;',
                'V - realizar serviços de proteção por guarda-vidas na orla fluvial e balneários públicos;',
                'VI - realizar serviços de socorro e apoio às embarcações;',
                'VII - exercer o poder de polícia na área de sua competência, especialmente:',
                'a) nos locais de sinistros ou de risco;',
                'b) na fiscalização de empresas especializadas na produção e comercialização de produtos destinados à prevenção de desastres e sinistros, à segurança contra incêndio e pânico em edificações, particularmente quanto à recarga de extintores de incêndio;',
                'c) na fiscalização do armazenamento, estocagem e transporte de cargas e produtos perigosos no território do Estado de Rondônia;',
                'd) na fiscalização de atividades que representem risco potencial de desastres e sinistros;',
                'e) na fiscalização das instalações e medidas de segurança contra incêndio e pânico das edificações residenciais multifamiliares, comerciais, industriais e de serviços em geral, inclusive, nos conjuntos residenciais, condomínios fechados e loteamentos urbanizados, quando da construção, reforma, ampliação e mudança de ocupação;',
                'f) na fiscalização das instalações e medidas de segurança contra incêndio dos veículos automotores;',
                'g) na fiscalização das instalações e medidas de segurança contra incêndio e acidentes em estruturas temporárias, tais como, arquibancadas e parques de diversões.',
                'VIII - realizar Perícia Técnica:',
                'a) preventiva, quanto a perigo potencial de incêndios e acidentes em edificações e estruturas temporárias;',
                'b) nos locais de sinistros e explosão relacionadas com sua competência.',
                'IX - realizar serviços de vistorias em edificações;',
                'X - estudar, analisar, planejar, exigir e fiscalizar todo o serviço de segurança contra incêndio e pânico no Estado de Rondônia;',
                'XI - embargar, interditar obras, serviços, habitações e locais de diversões públicas que não ofereçam condições de segurança para funcionamento;',
                'XII - emitir normas e laudos de exigências e aprovação de medidas contra incêndios;',
                'XIII - agir em cooperação com instituições similares em todo o território nacional;',
                'XIV - prestar assessoramento técnico, na área de sua competência, aos demais órgãos dos Poderes Executivo, Legislativo e Judiciário do Estado de Rondônia;',
                'XV - atender às demandas policiais ou judiciárias na investigação de responsabilidades por acidentes ou sinistros;',
                'XVI - planejar, coordenar, controlar e executar as atividades de Defesa Civil do Estado de Rondônia dentro de sua área de competência;',
                'XVII - capacitar pessoas para o enfrentamento de desastres, sinistros e acidentes;',
                'XVIII - exercer atividades que lhe forem delegadas pelo Governador do Estado;',
                'XIX - exercer a polícia judiciária militar, relativamente aos crimes militares praticados por seus integrantes ou contra a instituição Corpo de Bombeiros Militar ou sob sua administração, nos termos da legislação federal específica;',
                'XX - realizar atividades educativas de prevenção a incêndios, pânico coletivo e proteção ao meio ambiente, bem como ações de proteção e promoção do bem-estar da coletividade e dos direitos, garantias e liberdades do cidadão;',
                'XXI - estimular o respeito à cidadania, através de ações de natureza preventiva e educacional;',
                'XXII - realizar pesquisas técnico-científicas em seu campo de atuação funcional, com vistas à obtenção de produtos e processos que permitam o desenvolvimento de sistemas de segurança contra incêndio e pânico;',
                'XXIII - realizar atividades de formação e normatização das atividades de bombeiro civil e congêneres, no âmbito do Estado de Rondônia;',
                'XXIV - planejar, elaborar, gerenciar e executar o orçamento; e',
                'XXV - exercer outras atividades correlatas.',
            ],
            _F_LOB2, heading='TÍT. I — Das Generalidades',
        )],
    },
    'atribuicoes-funcoes': {
        'ro-art-1': [
            _art(
                'O Comando Operacional de Bombeiros é o órgão responsável pela execução das atividades-fins da Corporação e de Defesa Civil, subordinado operacionalmente ao Subcomandante-Geral e administrativamente ao Chefe do Estado-Maior-Geral, nos termos do art. 35 da Lei nº 2.204/2009, e tem a seguinte estrutura:',
                ['I - Comandante;', 'II - Adjunto;', 'III - Seção de Pessoal;', 'IV - Seção Administrativa;',
                 'V - Seção de Informática;', 'VI - Seção de Correição;',
                 'VII - Seção de Planejamento Operacional e Controle de Resultados;',
                 'VIII - Agência Regional de Inteligência; e', 'IX - Órgãos de Execução Operacional.'],
                _F_COB, heading=_H_COB, orgao='cob',
            ),
            _art(
                'Compete ao Comandante Operacional de Bombeiros:',
                [
                    'I - planejar, coordenar, supervisionar e fiscalizar, em nível regional, as atividades operacionais e de proteção e defesa civil desenvolvidas pelas unidades subordinadas, observadas as políticas, diretrizes e determinações do Comando-Geral e do Estado-Maior-Geral;',
                    'II - exercer o comando sobre os Grupamentos de Bombeiro Militar e demais unidades operacionais subordinadas, respeitadas as atribuições e competências próprias de seus respectivos comandantes;',
                    'III - planejar e coordenar as operações de âmbito regional, promovendo a integração operacional entre as unidades subordinadas e propondo ao Subcomandante-Geral a homologação dos planejamentos cuja execução implique despesa ou repercussão financeira para a Corporação;',
                    'IV - coordenar o emprego dos recursos humanos, viaturas, equipamentos e demais meios operacionais disponíveis na respectiva área, podendo determinar ou autorizar o deslocamento de recursos entre as unidades subordinadas, conforme a necessidade do serviço, a natureza e a magnitude da ocorrência, dando ciência ao escalão superior quando a medida, por sua relevância, duração ou repercussão, assim exigir;',
                    'V - atuar como elo de comando e promover a interlocução das Organizações Bombeiro Militar operacionais subordinadas com os escalões superiores da Corporação e com as Seções do Estado-Maior-Geral, encaminhando, coordenando e acompanhando as demandas de natureza operacional, administrativa e logística que ultrapassem a competência das respectivas unidades;',
                    'VI - aprovar as Ordens de Serviço e os demais planejamentos operacionais elaborados pelas unidades subordinadas, ressalvados aqueles sujeitos à homologação ou aprovação de autoridade superior;',
                    'VII - expedir diretrizes, orientações e determinações de natureza operacional às unidades subordinadas, visando à padronização, à eficiência e à integração dos serviços na área do respectivo Comando Operacional;',
                    'VIII - coordenar e fiscalizar as escalas de serviço de âmbito regional, podendo autorizar alterações e permutas cuja competência não esteja atribuída a outra autoridade;',
                    'IX - autorizar, por escrito, a permuta de escala do serviço de Oficial de Dia, com posterior publicação em Boletim Geral Ostensivo;',
                    'X - acionar o Superior de Dia nas ocorrências de grande vulto, na forma deste Regulamento;',
                    'XI - fiscalizar e acompanhar a execução das atividades operacionais desenvolvidas pelas unidades subordinadas, avaliando o emprego dos recursos e os resultados alcançados;',
                    'XII - efetuar, nos termos do art. 13, inciso V, do Regulamento de Movimentação aprovado pelo Decreto nº 8.134, de 18 de dezembro de 1997, a movimentação de praças entre as Organizações Bombeiro Militar subordinadas ao respectivo Comando Operacional, quando não implicar ônus para a Corporação, observados, sempre que possível, os pareceres dos respectivos Comandantes de Unidade;',
                    'XIII - propor ao Coordenador de Pessoal a movimentação de praças entre Organizações Bombeiro Militar pertencentes a Comandos Operacionais distintos, quando não implicar ônus para a Corporação, observadas as competências estabelecidas no art. 13 do Regulamento de Movimentação aprovado pelo Decreto nº 8.134, de 18 de dezembro de 1997;',
                    'XIV - propor ao Subcomandante-Geral a movimentação de praças quando dela decorrer ônus para a Corporação, observadas as competências estabelecidas no art. 13 do Regulamento de Movimentação aprovado pelo Decreto nº 8.134, de 18 de dezembro de 1997;',
                    'XV - propor ao Subcomandante-Geral, nos termos do art. 13, inciso II, alínea "a", do Regulamento de Movimentação aprovado pelo Decreto nº 8.134, de 18 de dezembro de 1997, a movimentação de oficiais das Organizações Bombeiro Militar subordinadas ao respectivo Comando Operacional, observadas a necessidade do serviço e as demais disposições regulamentares aplicáveis;',
                    'XVI - coordenar o apoio operacional entre as unidades subordinadas, especialmente nas ocorrências de maior vulto, operações extraordinárias, eventos especiais e demais situações que excedam a capacidade operacional de determinada unidade;',
                    'XVII - acionar ou solicitar o acionamento dos escalões superiores da cadeia de comando nas ocorrências cuja natureza, magnitude ou repercussão ultrapasse a capacidade de resposta das unidades sob sua responsabilidade;',
                    'XVIII - acompanhar e consolidar os dados estatísticos, relatórios e informações operacionais produzidos pelas unidades subordinadas, promovendo seu encaminhamento aos órgãos competentes e mantendo os escalões superiores informados acerca da situação operacional de sua área;',
                    'XIX - propor ao Comando-Geral medidas destinadas ao aperfeiçoamento da estrutura operacional, inclusive a criação, transformação, extinção, instalação ou alteração da área de atuação das unidades subordinadas;',
                    'XX - promover a integração entre os Grupamentos de Bombeiro Militar e demais unidades subordinadas, buscando a uniformidade de procedimentos, a racionalização do emprego dos recursos e a melhoria da resposta operacional;',
                    'XXI - presidir as solenidades de passagem de comando dos Grupamentos de Bombeiro Militar subordinados ao respectivo Comando Operacional;',
                    'XXII - representar o Comandante-Geral em solenidades, reuniões, eventos e demais atos institucionais, quando devidamente designado ou determinado; e',
                    'XXIII - cumprir fielmente as determinações emanadas dos escalões superiores, observadas as competências e atribuições estabelecidas na legislação e nos regulamentos vigentes.',
                ],
                _F_COB, heading=_H_COB, orgao='cob',
                nota='Incisos XII a XV citam o Decreto nº 8.134/1997 (Regulamento de Movimentação) — conferir vigência e teor do art. 13 antes da consolidação. Incisos IX e X mantidos da versão em consulta.',
            ),
        ],
        'ro-art-2': [_art(
            'Compete ao Adjunto do Comando Operacional de Bombeiros:',
            [
                'I - assessorar o Comandante Operacional de Bombeiros no planejamento, na coordenação, na supervisão e na fiscalização das atividades desenvolvidas no âmbito do respectivo Comando Operacional;',
                'II - acompanhar o cumprimento das diretrizes, determinações e ordens emanadas pelo Comandante Operacional, mantendo-o informado acerca de sua execução pelas unidades subordinadas;',
                'III - coordenar, por determinação do Comandante Operacional, a consolidação dos planejamentos, Ordens de Serviço, escalas, relatórios, dados estatísticos e demais informações encaminhadas pelas unidades subordinadas;',
                'IV - acompanhar a tramitação das demandas das Organizações Bombeiro Militar subordinadas junto aos escalões superiores e às Seções do Estado-Maior-Geral, mantendo o Comandante Operacional informado quanto ao seu andamento;',
                'V - promover a integração e o fluxo de informações entre o Comando Operacional e as unidades subordinadas, zelando pelo cumprimento dos prazos, determinações e providências estabelecidas;',
                'VI - auxiliar o Comandante Operacional na elaboração e no acompanhamento dos planejamentos e operações de âmbito regional;',
                'VII - acompanhar a situação do efetivo, dos meios operacionais, das viaturas e dos equipamentos das unidades subordinadas, consolidando as informações necessárias ao planejamento e à tomada de decisão do Comandante Operacional;',
                'VIII - elaborar estudos, informações, relatórios e propostas destinados a subsidiar as decisões do Comandante Operacional;',
                'IX - substituir o Comandante Operacional de Bombeiros em seus impedimentos e afastamentos eventuais; e',
                'X - exercer as demais atribuições que lhe forem delegadas pelo Comandante Operacional de Bombeiros.',
            ],
            _F_COB, heading=_H_COB, orgao='cob',
            nota='Incisos IX e X mantidos da versão em consulta (substituição eventual do titular).',
        )],
        'ro-art-3': [_art(
            'Compete ao Chefe da Seção de Pessoal do Comando Operacional de Bombeiros:',
            [
                'I - dirigir, coordenar e distribuir os trabalhos da Seção de Pessoal, mantendo atualizado o controle da situação funcional, da lotação e da distribuição do efetivo do Comando Operacional;',
                'II - instruir os processos relativos à movimentação de oficiais e praças, elaborando as informações e manifestações necessárias à decisão ou proposição do Comandante Operacional, observadas as competências estabelecidas no Regulamento de Movimentação aprovado pelo Decreto nº 8.134, de 18 de dezembro de 1997;',
                'III - acompanhar a distribuição do efetivo das Organizações Bombeiro Militar subordinadas, identificando déficits, excedentes e necessidades de recompletamento, para subsidiar as decisões do Comandante Operacional;',
                'IV - acompanhar e manter registro das apresentações, inclusões, exclusões, transferências, afastamentos, férias, licenças e demais alterações funcionais dos militares pertencentes ao efetivo do Comando Operacional;',
                'V - elaborar estudos e levantamentos relativos à distribuição do efetivo das unidades subordinadas, submetendo ao Comandante Operacional informações destinadas a subsidiar as decisões relativas à movimentação e ao emprego de pessoal;',
                'VI - acompanhar as demandas de pessoal encaminhadas pelas Organizações Bombeiro Militar subordinadas, submetendo ao Comandante Operacional aquelas que dependam de providências dos escalões superiores ou da Coordenadoria de Pessoal;',
                'VII - elaborar e manter atualizados os mapas, quadros e relatórios relativos ao efetivo do Comando Operacional, bem como consolidar, quando necessário, informações de pessoal provenientes das unidades subordinadas; e',
                'VIII - exercer outras atribuições de pessoal que lhe forem determinadas pelo Comandante Operacional de Bombeiros.',
            ],
            _F_COB, heading=_H_COB, orgao='cob',
            nota='O inciso II da sugestão original não foi enviado (a numeração pulou de I para III); renumerado. Inciso II cita o Decreto nº 8.134/1997 — conferir.',
        )],
        'ro-art-4': [_art(
            'Compete ao Chefe da Seção Administrativa do Comando Operacional de Bombeiros:',
            [
                'I - dirigir, coordenar e distribuir os trabalhos da Seção Administrativa, promovendo a execução das atividades administrativas necessárias ao funcionamento do Comando Operacional;',
                'II - instruir e acompanhar os processos administrativos de interesse do Comando Operacional e acompanhar, quando necessário, aqueles oriundos das Organizações Bombeiro Militar subordinadas que dependam de providências do Comando Operacional ou dos escalões superiores;',
                'III - controlar e acompanhar os bens patrimoniais, materiais permanentes e de consumo sob responsabilidade do Comando Operacional, mantendo atualizados os respectivos registros e controles;',
                'IV - acompanhar as necessidades administrativas, logísticas e de infraestrutura do Comando Operacional, adotando as providências de sua competência e submetendo ao Comandante Operacional aquelas que dependam de atuação dos escalões superiores;',
                'V - receber, consolidar e encaminhar, quando determinado pelo Comandante Operacional, as demandas administrativas e logísticas apresentadas pelas Organizações Bombeiro Militar subordinadas, preservadas as competências próprias de cada unidade;',
                'VI - acompanhar, junto às Seções do Estado-Maior-Geral e demais órgãos competentes, a tramitação das demandas administrativas e logísticas encaminhadas pelo Comando Operacional;',
                'VII - organizar e manter o controle da documentação administrativa de responsabilidade do Comando Operacional, observadas as normas de gestão documental vigentes;',
                'VIII - elaborar levantamentos, informações e relatórios de natureza administrativa e logística destinados a subsidiar as decisões do Comandante Operacional; e',
                'IX - exercer outras atribuições administrativas que lhe forem determinadas pelo Comandante Operacional de Bombeiros.',
            ],
            _F_COB, heading=_H_COB, orgao='cob',
        )],
        'ro-art-5': [_art(
            'Compete ao Chefe da Seção de Informática do Comando Operacional de Bombeiros:',
            [
                'I - receber e acompanhar as demandas relacionadas à tecnologia da informação oriundas do Comando Operacional e das Organizações Bombeiro Militar subordinadas, quando dependerem de providências dos órgãos técnicos da Corporação;',
                'II - encaminhar à Diretoria de Informática as demandas de tecnologia da informação que excedam a capacidade ou a competência das Organizações Bombeiro Militar subordinadas, acompanhando as providências adotadas; e',
                'III - manter o Comandante Operacional informado acerca das demandas de tecnologia da informação que possam afetar o funcionamento administrativo ou operacional das unidades subordinadas.',
            ],
            _F_COB, heading=_H_COB, orgao='cob',
        )],
        'ro-art-6': [_art(
            'Compete ao Chefe da Seção de Correição do Comando Operacional de Bombeiros:',
            [
                'I - assessorar o Comandante Operacional nos assuntos de natureza disciplinar e correcional de sua competência;',
                'II - instruir e acompanhar, no âmbito do Comando Operacional, os procedimentos disciplinares e correcionais cuja instauração ou instrução lhe seja regularmente determinada pela autoridade competente;',
                'III - acompanhar, para fins de controle, os procedimentos disciplinares e correcionais instaurados no âmbito das Organizações Bombeiro Militar subordinadas, sem prejuízo das competências próprias de seus respectivos comandantes;',
                'IV - manter controle dos prazos e da tramitação dos procedimentos disciplinares e correcionais de responsabilidade do Comando Operacional;',
                'V - receber e encaminhar à Corregedoria-Geral as demandas de natureza correcional oriundas do Comando Operacional ou das Organizações Bombeiro Militar subordinadas que dependam de providências daquele órgão;',
                'VI - prestar, quando solicitado, informações ao Comandante Operacional acerca da situação dos procedimentos disciplinares e correcionais em tramitação na área do respectivo Comando, respeitados o sigilo e as restrições de acesso aplicáveis;',
                'VII - promover a interlocução entre o Comando Operacional, as Organizações Bombeiro Militar subordinadas e a Corregedoria-Geral nos assuntos de natureza disciplinar e correcional; e',
                'VIII - exercer outras atribuições de natureza correcional que lhe forem determinadas pelo Comandante Operacional, observadas as competências da Corregedoria-Geral e das demais autoridades disciplinares.',
            ],
            _F_COB, heading=_H_COB, orgao='cob',
        )],
        'ro-art-7': [_art(
            'Compete ao Chefe da Seção de Planejamento Operacional e Controle de Resultados do Comando Operacional de Bombeiros:',
            [
                'I - dirigir e coordenar a elaboração do planejamento operacional de âmbito regional do Comando Operacional de Bombeiros, observadas as diretrizes estabelecidas pelo Comando-Geral, pelo Subcomandante-Geral e pelo Estado-Maior-Geral;',
                'II - analisar e consolidar os planejamentos operacionais encaminhados pelas Organizações Bombeiro Militar subordinadas, quando envolverem emprego integrado de unidades, repercussão regional ou dependerem de aprovação ou homologação de escalão superior;',
                'III - elaborar, em conjunto com as Organizações Bombeiro Militar subordinadas, planos e propostas para operações que envolvam o emprego integrado de recursos de mais de uma unidade;',
                'IV - consolidar e analisar os dados estatísticos, indicadores e resultados operacionais das Organizações Bombeiro Militar subordinadas, identificando tendências e necessidades relacionadas à capacidade de resposta operacional;',
                'V - acompanhar a execução dos planejamentos e operações de âmbito regional, avaliando os resultados alcançados e propondo, quando necessário, medidas destinadas ao aperfeiçoamento do emprego operacional;',
                'VI - elaborar estudos, levantamentos, relatórios e informações de natureza operacional destinados a subsidiar a tomada de decisão do Comandante Operacional;',
                'VII - subsidiar o Comandante Operacional na prestação de informações e de resultados operacionais aos escalões superiores;',
                'VIII - manter e consolidar informações relativas aos recursos e às capacidades operacionais das unidades subordinadas necessárias ao planejamento de operações de âmbito regional; e',
                'IX - exercer outras atribuições de planejamento operacional e controle de resultados que lhe forem determinadas pelo Comandante Operacional de Bombeiros.',
            ],
            _F_COB, heading=_H_COB, orgao='cob',
        )],
        'ro-art-8': [_art(
            'Compete ao Chefe da Agência Regional de Inteligência do Comando Operacional de Bombeiros:',
            [
                'I - atuar como elo entre o Comando Operacional, as Organizações Bombeiro Militar subordinadas e a Diretoria de Inteligência do CBMRO nos assuntos de competência desta;',
                'II - receber, instruir, conferir e encaminhar à Diretoria de Inteligência as demandas dos militares pertencentes ao Comando Operacional relativas à aquisição, transferência, venda e demais procedimentos relacionados a armamento, bem como receber e encaminhar à referida Diretoria as demandas devidamente instruídas pelas Organizações Bombeiro Militar subordinadas, observadas as normas e competências específicas;',
                'III - acompanhar, junto à Diretoria de Inteligência, a tramitação das demandas encaminhadas pelo Comando Operacional e pelas Organizações Bombeiro Militar subordinadas, promovendo a interlocução necessária até a conclusão das providências de competência daquele órgão;',
                'IV - orientar as Organizações Bombeiro Militar subordinadas quanto aos procedimentos, à documentação e aos fluxos estabelecidos pela Diretoria de Inteligência para o processamento das matérias de sua competência;',
                'V - encaminhar à Diretoria de Inteligência as matérias que, por sua natureza, grau de sigilo ou competência, dependam de análise ou providência daquele órgão;',
                'VI - receber, instruir e prestar as informações relativas aos militares pertencentes ao Comando Operacional, bem como receber e encaminhar as informações devidamente instruídas pelas Organizações Bombeiro Militar subordinadas, referentes às demandas de restrição de porte e posse de arma de fogo, quando solicitadas pela Diretoria de Logística, promovendo o respectivo encaminhamento ao órgão competente; e',
                'VII - exercer outras atividades de interlocução e apoio relacionadas às matérias de competência da Diretoria de Inteligência que lhe forem determinadas pelo Comandante Operacional.',
            ],
            _F_COB, heading=_H_COB, orgao='cob',
            nota='Incisos II e VI atribuem à ARI o trâmite de armamento (aquisição, transferência, restrição de porte) — confirmar com a Diretoria de Inteligência e a Diretoria de Logística.',
        )],
        'ro-art-9': [
            _art(
                'O Grupamento de Bombeiro Militar, subordinado diretamente ao Comando Operacional de Bombeiros, é organizado em Subgrupamentos de Bombeiro Militar, destacados ou não, que por sua vez se estruturam em Seções de Bombeiros, destacadas ou não, e possui a seguinte estrutura, nos termos do art. 47, § 1º, da Lei nº 2.204/2009:',
                ['I - Comando:', 'a) Comandante;', 'b) Subcomandante; e', 'c) Auxiliares;',
                 'II - Estado-Maior:', 'a) B1 (Pessoal);', 'b) B2 (Inteligência);', 'c) B3 (Operações);',
                 'd) B4 (Logística);', 'e) B5 (Relações Externas); e', 'f) B6 (Justiça e Disciplina).'],
                _F_GBM, heading=_H_COB, orgao='cob',
                nota='O Cel. propõe regulamentar também Subcomandante, Auxiliares e as seções B1 a B6 do GBM; a redação desses artigos ainda não existe (coincide com a pendência "cadeia de comando abaixo do SGBM").',
            ),
            _art(
                'Compete ao Comandante de Grupamento de Bombeiro Militar:',
                [
                    'I - comandar, coordenar, supervisionar e fiscalizar as atividades operacionais e administrativas do Grupamento e das Subunidades a ele subordinadas, observadas as diretrizes e determinações dos escalões superiores;',
                    'II - planejar, coordenar e executar as atividades operacionais no âmbito de sua área de responsabilidade, observadas as diretrizes estabelecidas pelo respectivo Comando Operacional;',
                    'III - elaborar e aprovar as Ordens de Serviço e os planejamentos operacionais de âmbito do Grupamento, submetendo ao Comando Operacional aqueles que envolvam emprego de meios de outras unidades, repercussão regional ou dependam de aprovação ou homologação de escalão superior;',
                    'IV - administrar o efetivo, os materiais, as viaturas, os equipamentos e demais recursos colocados à disposição do Grupamento, observadas as competências dos órgãos responsáveis e a legislação vigente;',
                    'V - coordenar o emprego dos recursos humanos e materiais das Subunidades subordinadas, podendo determinar seu emprego dentro da área de responsabilidade do Grupamento, conforme a necessidade do serviço;',
                    'VI - manter o Comando Operacional informado acerca das ocorrências de maior vulto, situações extraordinárias ou fatos relevantes que possam exigir apoio, coordenação ou providências do escalão superior;',
                    'VII - solicitar ao Comando Operacional, quando necessário, apoio de efetivo, viaturas, equipamentos ou outros recursos de unidades não subordinadas ao respectivo Grupamento;',
                    'VIII - exercer a gestão do efetivo do Grupamento e de suas Subunidades, promovendo os atos de sua competência e encaminhando ao Comando Operacional as demandas de pessoal que dependam de providências daquele Comando ou dos escalões superiores;',
                    'IX - fiscalizar o cumprimento das normas, ordens, diretrizes e procedimentos operacionais e administrativos no âmbito das unidades subordinadas;',
                    'X - acompanhar e avaliar os resultados operacionais do Grupamento e de suas Subunidades, mantendo atualizados os dados e informações necessários ao controle e ao planejamento operacional;',
                    'XI - promover a instrução e o aperfeiçoamento profissional do efetivo sob seu comando, observadas as diretrizes e normas estabelecidas pelos órgãos competentes;',
                    'XII - zelar pela disciplina, hierarquia, apresentação, eficiência e regularidade dos serviços no âmbito do Grupamento e de suas Subunidades;',
                    'XIII - promover a articulação institucional do Grupamento com os órgãos públicos e demais instituições existentes em sua área de responsabilidade, nos assuntos relacionados às atribuições da Corporação, observadas as diretrizes dos escalões superiores;',
                    'XIV - propor ao Comando Operacional medidas destinadas ao aperfeiçoamento da estrutura, da distribuição do efetivo, dos recursos e da capacidade operacional das unidades sob seu comando;',
                    'XV - presidir as solenidades de passagem de comando dos Subgrupamentos de Bombeiro Militar subordinados ao respectivo Grupamento;',
                    'XVI - representar o Comandante-Geral em solenidades, reuniões, eventos e demais atos institucionais realizados em sua área de responsabilidade, quando devidamente designado ou determinado;',
                    'XVII - prestar ao Comando Operacional as informações, dados, relatórios e demais elementos necessários ao acompanhamento das atividades e dos resultados do Grupamento;',
                    'XVIII - propor à autoridade competente a instauração de Inquérito Sanitário de Origem e de Atestado de Origem relativos aos militares sob seu comando, quando presentes os pressupostos regulamentares, promovendo o encaminhamento da documentação pertinente; e',
                    'XIX - cumprir fielmente as determinações dos escalões superiores, no âmbito de suas atribuições.',
                ],
                _F_GBM, heading=_H_COB, orgao='cob',
            ),
        ],
        'ro-art-10': [_art(
            'Compete ao Comandante de Subgrupamento de Bombeiro Militar:',
            [
                'I - comandar, coordenar, supervisionar e fiscalizar as atividades operacionais e administrativas do Subgrupamento e das frações a ele subordinadas, observadas as diretrizes e determinações dos escalões superiores;',
                'II - planejar, coordenar e executar as atividades operacionais no âmbito de sua área de responsabilidade, observadas as diretrizes estabelecidas pelo Grupamento de Bombeiro Militar ao qual estiver subordinado;',
                'III - elaborar as Ordens de Serviço e os planejamentos operacionais de âmbito do Subgrupamento, submetendo ao Comandante do Grupamento aqueles que dependam de aprovação superior, envolvam emprego de recursos externos à Subunidade ou produzam repercussão além de sua área de responsabilidade;',
                'IV - administrar o efetivo, os materiais, as viaturas, os equipamentos, as instalações e os demais recursos colocados à disposição do Subgrupamento, observadas as competências dos órgãos responsáveis e a legislação vigente;',
                'V - coordenar o emprego dos recursos humanos e materiais disponíveis no Subgrupamento e nas frações subordinadas, de acordo com as necessidades do serviço;',
                'VI - organizar, coordenar e fiscalizar as escalas de serviço no âmbito do Subgrupamento, observadas as normas e diretrizes estabelecidas pelos escalões superiores;',
                'VII - manter o Comandante do Grupamento informado acerca das ocorrências de maior vulto, situações extraordinárias e demais fatos relevantes que possam exigir apoio ou providências do escalão superior;',
                'VIII - solicitar ao Comandante do Grupamento, quando necessário, apoio de efetivo, viaturas, equipamentos ou outros recursos que excedam a capacidade operacional do Subgrupamento;',
                'IX - exercer a gestão do efetivo pertencente ao Subgrupamento, adotando as providências de sua competência e encaminhando ao Grupamento as demandas de pessoal que dependam de atuação do escalão superior;',
                'X - fiscalizar o cumprimento das normas, ordens, diretrizes e procedimentos operacionais e administrativos no âmbito do Subgrupamento e de suas frações subordinadas;',
                'XI - acompanhar e avaliar os resultados das atividades operacionais desenvolvidas pelo Subgrupamento, mantendo atualizados os dados e informações necessários ao planejamento e ao controle das atividades;',
                'XII - promover e fiscalizar a instrução e o aperfeiçoamento profissional do efetivo sob seu comando, observadas as diretrizes estabelecidas pelos órgãos competentes;',
                'XIII - zelar pela hierarquia, disciplina, apresentação, eficiência e regularidade dos serviços no âmbito do Subgrupamento;',
                'XIV - manter o Comandante do Grupamento informado acerca das necessidades administrativas, logísticas, operacionais e de pessoal do Subgrupamento, propondo as providências que excedam sua competência;',
                'XV - promover a articulação institucional do Subgrupamento com órgãos públicos e demais instituições existentes em sua área de responsabilidade, nos assuntos relacionados às atribuições da Corporação, observadas as diretrizes dos escalões superiores;',
                'XVI - prestar ao Grupamento de Bombeiro Militar as informações, dados, relatórios e demais elementos necessários ao acompanhamento das atividades e dos resultados do Subgrupamento;',
                'XVII - propor à autoridade competente a instauração de Inquérito Sanitário de Origem e de Atestado de Origem relativos aos militares sob seu comando, quando presentes os pressupostos regulamentares, promovendo o encaminhamento da documentação pertinente; e',
                'XVIII - cumprir fielmente as determinações dos escalões superiores, no âmbito de suas atribuições.',
            ],
            _F_SGBM, heading=_H_COB, orgao='cob',
            nota='O Cel. propõe regulamentar também Subcomandante e Auxiliares do SGBM (LOB, Art. 47); redação ainda não existe.',
        )],
    },
    'servico-operacional': {
        'se-art-2': [_art(
            'São objetivos do presente Regulamento:',
            [
                'I - estabelecer as competências, atribuições e responsabilidades das funções integrantes do Serviço Operacional do Corpo de Bombeiros Militar, definindo os procedimentos funcionais correspondentes às respectivas esferas de atuação;',
                'II - delimitar as competências dos diferentes níveis de comando e das funções integrantes da estrutura operacional da Corporação, estabelecendo os respectivos limites de atuação e prevenindo conflitos, sobreposições ou lacunas de atribuições;',
                'III - estabelecer os níveis de planejamento, coordenação, supervisão, execução e controle das atividades operacionais, observada a estrutura organizacional e a cadeia de comando da Corporação;',
                'IV - assegurar a integração e a adequada articulação entre os diferentes escalões, Organizações Bombeiro Militar, Subunidades e demais frações operacionais da Corporação;',
                'V - adequar a atuação operacional das Organizações Bombeiro Militar às políticas, diretrizes e determinações emanadas do Comando-Geral e dos demais escalões competentes;',
                'VI - promover a padronização dos procedimentos operacionais e administrativos diretamente relacionados à execução do serviço operacional;',
                'VII - promover a eficiência, a eficácia e a efetividade na execução das atividades operacionais, buscando o adequado emprego dos recursos humanos, materiais e operacionais disponíveis;',
                'VIII - estabelecer fluxos de comunicação, encaminhamento e decisão entre as Organizações Bombeiro Militar e os diferentes níveis da cadeia de comando, respeitadas as competências legalmente estabelecidas; e',
                'IX - proporcionar aos oficiais e praças orientações funcionais que subsidiem a tomada de decisão e a solução de situações decorrentes da execução das atividades operacionais, observados os limites de competência de cada função.',
            ],
            _F_SERV, heading='RISD, Caps. I–IV — Finalidade, Objetivos, Políticas e Funções Operacionais',
        )],
        'se-art-3': [_art(
            'Entende-se por política do serviço operacional o conjunto de princípios, objetivos e diretrizes destinados a orientar o planejamento, a organização, a execução e o aperfeiçoamento das atividades operacionais do Corpo de Bombeiros Militar.',
            [
                'Parágrafo único. Constituem objetivos básicos da política do serviço operacional:',
                'I - promover a valorização do bombeiro militar como elemento essencial à qualidade, à segurança e à eficiência das atividades operacionais;',
                'II - incentivar o aperfeiçoamento técnico-profissional e a capacitação continuada do efetivo, visando à manutenção das competências necessárias ao adequado desempenho das missões institucionais;',
                'III - fortalecer os valores profissionais, a hierarquia, a disciplina, o espírito de corpo e os princípios institucionais da Corporação;',
                'IV - promover a melhoria contínua da capacidade de resposta operacional, buscando a redução do tempo de resposta e o aumento da eficiência e da segurança nos atendimentos;',
                'V - aprimorar continuamente a qualidade dos serviços prestados, buscando maior efetividade das ações e satisfação da sociedade;',
                'VI - promover o adequado emprego e a disponibilidade dos recursos humanos, viaturas, equipamentos e demais meios necessários à execução das atividades operacionais;',
                'VII - manter recursos e meios operacionais em condições de pronto emprego, de acordo com as necessidades e peculiaridades de cada área de atuação;',
                'VIII - promover o planejamento e a preparação para ocorrências de maior vulto, desastres, eventos extraordinários e demais situações que demandem emprego ampliado ou integrado dos recursos da Corporação;',
                'IX - manter atualizadas as informações relativas aos recursos, pontos de apoio, áreas de risco e demais elementos necessários ao planejamento e à execução das operações;',
                'X - fomentar a integração operacional entre as Organizações Bombeiro Militar, permitindo o emprego coordenado dos recursos disponíveis quando a situação assim exigir;',
                'XI - promover a padronização e o aperfeiçoamento contínuo dos procedimentos empregados nas atividades operacionais; e',
                'XII - orientar o planejamento e o emprego dos recursos operacionais segundo critérios de necessidade, eficiência, segurança e capacidade de resposta.',
            ],
            _F_SERV, heading='RISD, Caps. I–IV — Finalidade, Objetivos, Políticas e Funções Operacionais',
        )],
    },
}

_H_SD = 'RISD, Cap. VI — Regime e Escalas de Serviço · Do Superior de Dia'
_H_OD = 'RISD, Cap. VI — Regime e Escalas de Serviço · Do Oficial de Dia'
_H_CS = 'RISD, Cap. VI — Regime e Escalas de Serviço · Do Comandante de Socorro'

# (4) Inclusões — artigos NOVOS, inseridos APÓS o id indicado (id da versão em consulta).
# {tema: [{'apos': id, 'artigos': [...]}, ...]}
INCLUIR = {
    'servico-operacional': [
        {   # Seção do Superior de Dia — depois do bloco de regime/escala (se-art-24..31)
            'apos': 'se-art-31',
            'artigos': [
                _art(
                    'O serviço de Superior de Dia será estabelecido exclusivamente na Capital do Estado, em regime de sobreaviso de 24 (vinte e quatro) horas, concorrendo à respectiva escala os oficiais dos postos de Major BM e Tenente-Coronel BM.',
                    ['§ 1º Durante o período de serviço, o Superior de Dia deverá permanecer em condições de pronto acionamento, mantendo disponível meio de comunicação que permita seu imediato contato e comparecimento quando necessário.',
                     '§ 2º A atuação do Superior de Dia ficará circunscrita à Capital do Estado, observadas as competências próprias do Comando Operacional e dos Comandantes das Organizações Bombeiro Militar.'],
                    _F_SERV, heading=_H_SD, proposta=True,
                    nota=NOTA_PROPOSTA + ': restringe o Superior de Dia à Capital e aos postos de Major/Tenente-Coronel; a versão em consulta prevê alcance em todo o território estadual (se-art-31) e os textos finais do Ten. Tiago põem a coordenação no Subcomandante-Geral.',
                ),
                _art(
                    'Compete ao Superior de Dia:',
                    [
                        'I - exercer a supervisão superior do serviço operacional na Capital durante o período para o qual estiver escalado, respeitadas as competências dos comandantes das Organizações Bombeiro Militar;',
                        'II - manter-se informado acerca das ocorrências de maior vulto, complexidade ou repercussão verificadas na Capital;',
                        'III - comparecer às ocorrências de grande vulto, complexidade ou repercussão quando acionado, quando entender necessário ou por determinação de autoridade superior;',
                        'IV - acompanhar e supervisionar, quando necessário, o desenvolvimento das operações de maior vulto, respeitada a cadeia de comando operacional estabelecida neste Regulamento;',
                        'V - comunicar aos escalões superiores as ocorrências relevantes, extraordinárias ou de grande repercussão, mantendo-os informados acerca de sua evolução e das providências adotadas;',
                        'VI - promover, quando necessário, a articulação entre as Organizações Bombeiro Militar sediadas na Capital para o atendimento de ocorrências que demandem emprego integrado de recursos;',
                        'VII - solicitar ou determinar, dentro dos limites de sua competência, o emprego de recursos operacionais adicionais necessários ao atendimento de ocorrências de maior vulto;',
                        'VIII - adotar, durante o serviço, as providências urgentes de natureza operacional que não comportem adiamento, submetendo posteriormente a matéria à autoridade competente quando necessário;',
                        'IX - articular-se com outros órgãos e instituições envolvidos nas operações, quando a natureza ou dimensão da ocorrência assim exigir;',
                        'X - observar as diretrizes institucionais relativas ao relacionamento com a imprensa nas ocorrências de grande vulto ou repercussão, em articulação com o órgão de comunicação social da Corporação;',
                        'XI - tomar conhecimento das alterações relevantes ocorridas durante o serviço e proceder aos registros ou manifestações que lhe forem determinados; e',
                        'XII - cumprir fielmente as determinações dos escalões superiores relacionadas ao serviço operacional.',
                    ],
                    _F_SERV, heading=_H_SD,
                ),
            ],
        },
        {   # Oficial de Dia — no lugar do bloco suprimido (se-art-32..38); entra após se-art-38
            'apos': 'se-art-38',
            'artigos': [
                _art(
                    'O serviço de Oficial de Dia será realizado exclusivamente no Quartel do Comando-Geral – QCG, em regime presencial de 24 (vinte e quatro) horas, sendo exercido por oficiais dos postos de Segundo-Tenente BM, Primeiro-Tenente BM e Capitão BM.',
                    ['§ 1º O Oficial de Dia exercerá suas atribuições no âmbito interno do QCG, competindo-lhe zelar pela disciplina, segurança, ordem e regular funcionamento do aquartelamento durante o período de serviço.',
                     '§ 2º O Oficial de Dia representará, durante o período de serviço e nos limites de suas atribuições, a autoridade responsável pelo aquartelamento nas questões relacionadas à disciplina e à segurança interna.'],
                    _F_SERV, heading=_H_OD, proposta=True,
                    nota=NOTA_PROPOSTA + ': redefine o Oficial de Dia como serviço interno do QCG (aquartelamento); na versão em consulta era função operacional coordenada pelo COB em cada OBM (se-art-32 a 38, marcados "Excluir" pelo Ten. Tiago). Avaliar extensão aos quartéis das OBMs.',
                ),
                _art(
                    'Compete ao Oficial de Dia:',
                    [
                        'I - participar das solenidades, formaturas e demais atos regulamentares previstos para o início e término do serviço;',
                        'II - receber do Oficial de Dia substituído e transmitir ao seu substituto as ordens, determinações, alterações e demais informações necessárias à continuidade do serviço;',
                        'III - orientar os militares empregados nos serviços internos do QCG quanto às suas atribuições e às determinações em vigor;',
                        'IV - realizar inspeções nas dependências do QCG, adotando ou solicitando as providências necessárias diante das irregularidades constatadas;',
                        'V - fiscalizar os serviços internos, verificando o cumprimento das normas, ordens e determinações em vigor;',
                        'VI - zelar pela disciplina, segurança e ordem no interior do QCG;',
                        'VII - fiscalizar os serviços de guarda e segurança do aquartelamento;',
                        'VIII - certificar-se de que as dependências que devam permanecer fechadas estejam devidamente resguardadas, mantendo o controle das respectivas chaves nos termos das normas internas;',
                        'IX - providenciar, na forma regulamentar, a substituição dos militares que não comparecerem aos serviços internos para os quais estejam escalados;',
                        'X - zelar pelo cumprimento das normas referentes à entrada, saída e permanência de pessoas no QCG;',
                        'XI - fiscalizar a entrada e saída de viaturas do aquartelamento, observadas as normas estabelecidas;',
                        'XII - registrar a entrada ou saída de materiais do QCG fora do horário de expediente, não permitindo sua retirada sem a devida autorização;',
                        'XIII - zelar pelos materiais, armamentos, instalações e demais bens que estejam sob sua responsabilidade durante o serviço;',
                        'XIV - receber autoridades civis e militares que compareçam ao QCG fora do horário de expediente, adotando as providências protocolares cabíveis;',
                        'XV - comunicar imediatamente à autoridade competente as ocorrências extraordinárias verificadas durante o serviço, especialmente aquelas relacionadas à disciplina, segurança, pessoal ou patrimônio;',
                        'XVI - adotar as providências imediatas destinadas a sanar ou minimizar alterações verificadas no funcionamento interno do QCG, submetendo à autoridade competente aquelas que excedam sua atribuição;',
                        'XVII - receber e encaminhar, fora do horário de expediente, documentos ou comunicações de caráter urgente, adotando as providências necessárias para que cheguem tempestivamente à autoridade competente;',
                        'XVIII - registrar em livro ou sistema próprio as ocorrências e alterações verificadas durante sua jornada de serviço;',
                        'XIX - elaborar e encaminhar a parte de serviço à autoridade competente, consignando as ocorrências e alterações relevantes verificadas durante a jornada;',
                        'XX - comunicar imediatamente qualquer acidente envolvendo pessoal, viatura, material ou patrimônio ocorrido no âmbito do QCG;',
                        'XXI - fiscalizar as condições de conservação, limpeza e organização das dependências do QCG;',
                        'XXII - fiscalizar o cumprimento das prisões e detenções de natureza disciplinar executadas nas dependências do aquartelamento, zelando pela observância das determinações da autoridade competente, das condições de segurança e das normas aplicáveis;',
                        'XXIII - diante da ocorrência de fato que, em tese, constitua crime militar, adotar as providências imediatas destinadas à preservação do local, dos elementos de informação e das provas, quando cabíveis, bem como comunicar imediatamente o fato à autoridade de polícia judiciária militar competente, para adoção das medidas previstas na legislação processual penal militar;',
                        'XXIV - adotar, nas hipóteses de flagrante de crime militar, as providências que lhe competirem nos termos da legislação processual penal militar, comunicando imediatamente o fato à autoridade de polícia judiciária militar competente; e',
                        'XXV - cumprir e fazer cumprir as ordens e determinações dos escalões superiores relacionadas ao serviço interno do aquartelamento.',
                    ],
                    _F_SERV, heading=_H_OD,
                    nota='Incisos X e XIII chegaram truncados na sugestão original ("rviço;" e "durante o se"); completados por dedução — confirmar com o autor. Incisos XXII a XXIV: conferir com a Corregedoria quanto ao CPPM.',
                ),
            ],
        },
        {   # Comandante de Socorro — depois do bloco Cmt de Socorro/Oficial de Dia nas OBMs (39..43)
            'apos': 'se-art-43',
            'artigos': [
                _art(
                    'O serviço de Comandante de Socorro será realizado exclusivamente na Capital do Estado, em regime presencial de 24 (vinte e quatro) horas, sendo exercido por Aspirantes a Oficial BM e oficiais dos postos de Segundo-Tenente BM, Primeiro-Tenente BM e Capitão BM, regularmente escalados para a função.',
                    ['§ 1º O Comandante de Socorro exercerá suas funções no âmbito do 1º Grupamento de Bombeiro Militar, observada a cadeia de comando operacional estabelecida neste Regulamento.',
                     '§ 2º Durante o período de serviço, o Comandante de Socorro representará a autoridade do Comandante do 1º Grupamento de Bombeiro Militar perante a prontidão operacional, exercendo, nos limites de suas atribuições, as competências necessárias à coordenação e à continuidade do serviço, sem prejuízo das matérias reservadas ao Comandante da Unidade ou aos escalões superiores.'],
                    _F_SERV, heading=_H_CS, proposta=True,
                    nota=NOTA_PROPOSTA + ': restringe o Comandante de Socorro à Capital/1º GBM e inclui Capitães; a versão em consulta prevê o serviço no quartel de cada OBM (se-art-40/42) e só subalternos e Aspirantes (se-art-39).',
                ),
                _art(
                    'Compete ao Comandante de Socorro:',
                    [
                        'I - coordenar, supervisionar e fiscalizar as atividades da prontidão operacional durante o período de serviço;',
                        'II - realizar a passagem de serviço, tomando conhecimento das alterações existentes e transmitindo ao seu substituto as informações necessárias à continuidade do serviço;',
                        'III - supervisionar, juntamente com os Comandantes de Guarnição, a conferência das viaturas, materiais e equipamentos operacionais;',
                        'IV - verificar as condições de prontidão das guarnições, viaturas, equipamentos e demais recursos operacionais disponíveis;',
                        'V - verificar a disponibilidade e o correto emprego dos equipamentos de proteção individual pelo efetivo de serviço;',
                        'VI - ministrar ou coordenar as instruções destinadas à prontidão de serviço, observadas as orientações e o planejamento estabelecidos;',
                        'VII - coordenar o emprego das guarnições e dos recursos operacionais durante o serviço;',
                        'VIII - acompanhar as ocorrências em andamento e comparecer àquelas cuja natureza, complexidade ou magnitude exija sua presença;',
                        'IX - exercer o comando das operações quando lhe couber, observadas a cadeia de comando operacional e a sistemática de comando de incidentes adotada pela Corporação;',
                        'X - solicitar o emprego de recursos operacionais adicionais quando aqueles disponíveis forem insuficientes para o atendimento da ocorrência;',
                        'XI - manter o Oficial de Dia e os escalões competentes informados acerca das ocorrências relevantes, alterações do serviço e indisponibilidade de recursos;',
                        'XII - receber dos Comandantes de Guarnição as informações relativas às ocorrências atendidas e às alterações verificadas durante o serviço;',
                        'XIII - adotar as providências imediatas diante das alterações ocorridas durante o serviço, encaminhando ao escalão competente aquelas que excedam sua competência;',
                        'XIV - zelar pela disciplina, segurança, apresentação e adequada atuação do efetivo integrante da prontidão operacional;',
                        'XV - fiscalizar o cumprimento das normas, protocolos, ordens e procedimentos relativos ao serviço operacional;',
                        'XVI - visitar, sempre que possível e desde que não haja prejuízo à execução do serviço operacional, os militares pertencentes ao 1º Grupamento de Bombeiro Militar que se encontrem hospitalizados, tomando conhecimento de sua situação e das eventuais necessidades de apoio institucional;',
                        'XVII - acompanhar os militares da ativa e da reserva remunerada que se encontrem detidos ou conduzidos perante autoridade policial, permanecendo no local, quando necessário, até a conclusão do registro da ocorrência e das providências iniciais adotadas pelo respectivo órgão;',
                        'XVIII - comunicar imediatamente ao Superior de Dia as situações previstas nos incisos IX e X, bem como quaisquer fatos envolvendo militares que, por sua natureza ou repercussão, demandem conhecimento ou providências dos escalões superiores;',
                        'XIX - acionar, quando necessário, o Plano de Chamada do 1º Grupamento de Bombeiro Militar, diante de ocorrência ou situação que demande reforço extraordinário de efetivo, comunicando imediatamente o acionamento ao Comandante da Unidade e ao Superior de Dia; e',
                        'XX - cumprir as determinações dos escalões superiores relacionadas ao serviço operacional.',
                    ],
                    _F_SERV, heading=_H_CS,
                    nota='Inciso XVII (acompanhar militar detido, inclusive da reserva remunerada): conferir com a Corregedoria.',
                ),
            ],
        },
    ],
}


# ── Aplicação ────────────────────────────────────────────────────────────────────────
def _tema(cap):
    return cap['id'].split(':')[-1]


def _prefixo(cap):
    return cap['id'][: -len(_tema(cap))]  # 'reg:atual:' ou 'reg:'


def aplicar_correcoes(structure):
    """Aplica CORRECOES in place (nas duas versões). Aborta se um trecho não existir."""
    n = 0
    pendentes = {(t, i) for t, arts in CORRECOES.items() for i in arts}
    for cap in structure['chapters']:
        tema = _tema(cap)
        regras = CORRECOES.get(tema, {})
        for art in cap['articles']:
            r = regras.get(art['id'])
            if not r:
                continue
            pendentes.discard((tema, art['id']))
            for velho, novo in r.get('caput', []):
                if velho not in art['caput']:
                    raise SystemExit(f'CORRECAO nao encontrada: {tema}/{art["id"]} caput: {velho!r}')
                art['caput'] = art['caput'].replace(velho, novo)
                n += 1
            for velho, novo in r.get('items', []):
                achou = False
                for it in art['items']:
                    if velho in it['text']:
                        it['text'] = it['text'].replace(velho, novo)
                        achou = True
                        n += 1
                if not achou:
                    raise SystemExit(f'CORRECAO nao encontrada: {tema}/{art["id"]} item: {velho!r}')
            art['corrigido'] = True
    if pendentes:
        raise SystemExit(f'CORRECOES sem artigo correspondente: {sorted(pendentes)}')
    return n


def _novo_artigo(cap, base_id, seq, spec, substitui=None):
    novo_id = f'{base_id}-r{seq}' if substitui else f'{base_id}-c{seq}'
    leaf = {
        'id': novo_id,
        'kind': 'incisos',
        'editId': f'{_prefixo(cap)}{_tema(cap)}/{novo_id}',
        'caput': spec['caput'],
        'items': [{'text': t, 'source': spec['fundamento']} for t in spec['dispositivos']],
        'source': spec['fundamento'],
        'match': 'exata',
        'heading': spec.get('heading'),
        'autoral': True,
        'fundamento': spec['fundamento'],
        'origem': 'consulta-2026-08',
    }
    if substitui:
        leaf['substitui'] = substitui
    else:
        leaf['incluido'] = True
    if spec.get('orgao'):
        leaf['orgao'] = spec['orgao']
    if spec.get('proposta'):
        leaf['proposta'] = True
    if spec.get('nota'):
        leaf['nota'] = spec['nota']
    return leaf


def aplicar_alteracoes(structure):
    """Aplica TEXTOS_FINAIS_ATUAL, SUPRIMIR, SUBSTITUIR e INCLUIR in place (só na atual).
    Devolve contagens. Aborta se algum id alvo não existir."""
    cont = {'textos_finais': 0, 'suprimidos': 0, 'substituidos': 0, 'novos': 0}
    for cap in structure['chapters']:
        tema = _tema(cap)
        finais = TEXTOS_FINAIS_ATUAL.get(tema, {})
        suprimir = SUPRIMIR.get(tema, {})
        substituir = SUBSTITUIR.get(tema, {})
        incluir = {b['apos']: b['artigos'] for b in INCLUIR.get(tema, [])}
        ids = {a['id'] for a in cap['articles']}
        for alvo in list(finais) + list(suprimir) + list(substituir) + list(incluir):
            if alvo not in ids:
                raise SystemExit(f'ALTERACAO aponta para id inexistente: {tema}/{alvo}')
        novos = []
        for art in cap['articles']:
            aid = art['id']
            if aid in finais:
                f = finais[aid]
                if 'caput' in f:
                    art['caput'] = f['caput']
                for idx, texto in f.get('items', {}).items():
                    art['items'][idx]['text'] = texto
                art['alterado'] = 'texto final'
                art['fundamento_alteracao'] = _F_FINAL
                cont['textos_finais'] += 1
            if aid in suprimir:
                cont['suprimidos'] += 1
                # o artigo sai; registra a supressão no capítulo para o comparativo
                cap.setdefault('suprimidos', []).append({'id': aid, 'motivo': suprimir[aid]})
            elif aid in substituir:
                for k, spec in enumerate(substituir[aid], start=1):
                    novos.append(_novo_artigo(cap, aid, k, spec, substitui=aid))
                cont['substituidos'] += 1
            else:
                novos.append(art)
            if aid in incluir:
                for k, spec in enumerate(incluir[aid], start=1):
                    novos.append(_novo_artigo(cap, aid, k, spec))
                    cont['novos'] += 1
        cap['articles'] = novos
    return cont


def gerar_versoes(structure):
    """A partir da estrutura gerada (cenário atual, ids reg:atual:), devolve
    (consulta, atual): a consulta só com CORRECOES; a atual com CORRECOES + ALTERACOES."""
    consulta = copy.deepcopy(structure)
    n_corr = aplicar_correcoes(consulta)
    consulta['versao'] = 'consulta'
    consulta['curadoria'] = {'correcoes': n_corr}
    atual = copy.deepcopy(consulta)
    cont = aplicar_alteracoes(atual)
    atual['versao'] = 'atual'
    atual['curadoria'] = {'correcoes': n_corr, **cont}
    return consulta, atual
