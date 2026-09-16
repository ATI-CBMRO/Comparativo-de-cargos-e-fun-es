"""Curadoria da Minuta do Regulamento de Serviço após a CONSULTA aos militares (ago/2026).

Regra (definida em 2026-09-14), para que a minuta que os militares leram possa ser
COMPARADA com a que resultou da consulta:

  VERSÃO EM CONSULTA — exatamente o texto lido pelos militares. Nada é aplicado nela; é
               onde os comentários do Firestore (editId#index) ficam ancorados.
  VERSÃO ATUAL — tudo o que a curadoria fez: CORRECOES (grafia, concordância, citação,
               resíduos de extração, nomenclatura), TEXTOS_FINAIS_ATUAL (redações fechadas
               no portal ou ajustadas na curadoria), SUPRIMIR, SUBSTITUIR e INCLUIR. Cada
               artigo reescrito ganha id NOVO com o campo `substitui`, de modo que os
               comentários dos militares sigam apontando para o texto que eles leram, na
               versão em consulta, e nunca caiam no dispositivo errado na atual (AR-03).

As correções e ajustes de redação da curadoria (feitos pelos administradores do portal em
ago-set/2026) são trabalho interno de revisão: NÃO aparecem como "sugestão" em relatório
nenhum e não levam autoria. As únicas sugestões relatadas ao SEI são as dos militares
consultados (coleção `suggestions`, contas com escopo "servico"): 271 registros do Cel. BM
Luiz Eduardo Oliveira Firmino (19 e 25/08/2026). Análise de mérito em
docs/sei/2026-09-11-regulamento-servico/Analise_Interacoes_e_Proposta_de_Aplicacao.md.

Decisões (2026-09-14): reescritas do Cel. só na atual; os três blocos que mudavam regra de
mérito entraram marcados `proposta: True` ("pendente de deliberação do CONDEG") e foram todos
decididos em 15/09/2026: Comandante de Socorro eliminado; Oficial de Dia só no 1º GBM; Superior
de Dia com alcance estadual mantido (se-art-31). Não resta proposta pendente.

Determinação de 16/09/2026: o que for SUPRIMIDO na atual é suprimido também na versão em
consulta — vale para SUPRIMIR (14–15/09), SUPRIMIR_AMBAS e ITENS_SUPRIMIR_AMBAS (16/09); nenhum
documento, comparativo ou relatório menciona texto suprimido. As alterações de texto continuam
só na atual.

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
_F_FINAL = 'Texto final fechado na curadoria do Portal de Legislação CBM (ago/2026) sobre a LOB, Lei nº 2.204/2009'
_F_CURADORIA = 'Curadoria da Minuta do Regulamento de Serviço (set/2026) sobre a LOB, Lei nº 2.204/2009'
_F_DELIB = 'Deliberação sobre dispositivos com texto semelhante (quadro de 15/09/2026) sobre a LOB, Lei nº 2.204/2009'
_F_REV16 = 'Revisão de texto da Minuta do Regulamento de Serviço (lote de 16/09/2026) sobre a LOB, Lei nº 2.204/2009'

NOTA_PROPOSTA = ('PROPOSTA PENDENTE DE DELIBERAÇÃO DO CONDEG — muda regra de mérito em '
                 'relação à versão em consulta')

# ── CORREÇÕES (só na versão atual) ───────────────────────────────────────────────────
# {tema: {id: {'caput': [(velho, novo), ...], 'items': [(velho, novo), ...]}}}
# Casamento por TEXTO (substring), nunca por índice. Todo `velho` PRECISA existir — o
# builder aborta se não achar (correção silenciosa que não aplica é pior que nenhuma).
CORRECOES = {
    'disposicoes-preliminares': {
        # A citação era a de Mato Grosso; em RO o CBM está no art. 148 da Constituição Estadual.
        'mt-art-1': {'caput': [('Art. 82 da Constituição Estadual', 'Art. 148 da Constituição Estadual')]},
        # Nome atual do sistema e da atividade: "proteção e defesa civil".
        'mt-art-3': {'items': [('Sistema Estadual de Defesa Civil', 'Sistema Estadual de Proteção e Defesa Civil'),
                               ('executar as atividades de defesa civil do Estado', 'executar as atividades de proteção e defesa civil do Estado')]},
    },
    'servico-operacional': {
        # ── Resíduos de nomenclatura do RISD de Sergipe / Regulamento do CBMMT (15/09/2026) ──
        'se-art-39': {'caput': [('escala de Oficial de Dia e de Oficial de dia os oficiais', 'escala de Oficial de Dia os oficiais')]},
        'se-art-40': {'caput': [('Esses serviços serão realizados no Quartel de cada respectiva Unidade Operacional', 'O serviço de Oficial de Dia será realizado no quartel do 1º Grupamento de Bombeiro Militar')]},
        'se-art-42': {'caput': [('Esses serviços serão realizados no Quartel de cada OBM com abrangência em toda sua área de jurisdição', 'O serviço de Oficial de Dia será realizado no quartel do 1º Grupamento de Bombeiro Militar, com abrangência em toda a sua área de jurisdição')]},
        'se-art-51': {'caput': [('apresentar-se a sua Unidade Operacional', 'apresentar-se à sua OBM')]},
        'se-art-52': {'caput': [('pelos médicos militares estaduais , deverão seguir os protocolos expedidos pela Corporação ou pela UM de Saúde , tão logo',
                                 'pelos médicos militares estaduais deverão seguir os protocolos expedidos pela Corporação, por meio do seu órgão de saúde, tão logo')]},
        'se-art-127': {'items': [('por escrito, ao comandante do SOS para', 'por escrito, ao Oficial de Dia para')]},
        'se-art-129': {'caput': [('da Unidade Operacional responsável pela área', 'da OBM responsável pela área')]},
        'se-art-130': {'caput': [('poder de combate da Unidade Operacional da área', 'poder de combate da OBM da área'),
                                 ('apoio dos socorros das demais Unidades,', 'apoio dos socorros das demais OBM,')]},
        'se-art-136': {'caput': [('para efeito deste regimento', 'para efeito deste Regulamento')]},
        'se-art-141': {'caput': [('pelo Comandante de Operações', 'pelo Comandante do Incidente')]},
        'se-art-142': {'caput': [('O Comandante de Operações deverá', 'O Comandante do Incidente deverá')]},
        'se-art-143': {'caput': [('orientações do Comandante de Operações', 'orientações do Comandante do Incidente')]},
        'se-art-145': {'caput': [('do Oficial de Dia ou Cmt de Operações', 'do Oficial de Dia ou do Comandante do Incidente')]},
        'se-art-116': {'caput': [('O Comando do CBMRO, a fim de regularizar a questão envolvendo pacientes com distúrbios mentais no Estado de Rondônia determina que:',
                                  'No atendimento às ocorrências envolvendo pacientes com transtorno mental no Estado de Rondônia observa-se o seguinte:')],
                       'items': [('seguindo os protocolos integrado SES/SSP e o do CBMRO', 'seguindo os protocolos integrados da Secretaria de Estado da Saúde, da SESDEC e do CBMRO'),
                                 ('através do CIOSP,', 'através do CIOP,'),
                                 ('§ 1º Diante do exposto acima, fica estabelecido que o CBMRO somente atuará ,', '§ 1º O CBMRO somente atuará,')]},
        # Sobra da quebra "Art. Nº" na extração do RISD de Sergipe.
        'se-art-1': {'caput': [('º O presente Regulamento', 'O presente Regulamento')]},
        'se-art-31': {'caput': [('Serviço de Superior dia ao CBMRO', 'serviço de Superior de Dia ao CBMRO')]},
        'se-art-2': {'caput': [('º São objetivos', 'São objetivos')]},
        'se-art-3': {'caput': [('º Chama-se política', 'Chama-se política')]},
        'se-art-4': {'caput': [('º Visando a otimização', 'Visando a otimização')]},
        # Concordância: "para que concorre" → "para quem concorre".
        'se-art-23': {'items': [('As escalas para que concorre exclusivamente', 'As escalas para quem concorre exclusivamente')]},
        # Resíduos de título de seção da fonte grudados no fim do caput.
        'se-art-43': {'caput': [(' Comandante de Guarnição – Do Condutor e Operador de Viaturas – Dos Auxiliares da Guarnição e do Operador de Rádio', '')]},
        'se-art-44': {'caput': [('excepcion ais', 'excepcionais'),
                                ('Em todas as Unidades Operacionais, Especializadas e Subunidade Operacionais do CBMRO', 'Em todas as Organizações Bombeiro Militar do CBMRO'),
                                # figuras eliminadas (15/09): adjunto do oficial de dia e auxiliares da guarnição
                                ('o regime das escalas de adjunto do oficial de dia, do comandante de guarnição, do condutor e operador de viaturas, dos auxiliares da guarnição e do operador de rádio',
                                 'o regime das escalas de comandante de guarnição, de condutor e operador de viaturas e de operador de rádio')]},
        'se-art-47': {'caput': [('pelo Comandante da OBM. Operações', 'pelo Comandante da OBM.')]},
        'se-art-112': {'caput': [('análise do comandante da OBM. durante Ocorrências', 'análise do comandante da OBM.')]},
        'se-art-115': {'caput': [('Comandante do incidente. com Distúrbios Mentais', 'Comandante do incidente.')]},
        # Resíduo "Grande Porte" (título de seção colado) e a sigla de Sergipe "GTA" — em RO a
        # unidade é o Grupamento de Operações Aéreas (GOA).
        'se-art-135': {'items': [('nos acidentes contra o meio ambiente. Grande Porte', 'nos acidentes contra o meio ambiente.'),
                                 ('Acionar o Instituto Médico Legal sempre', 'Acionar o Instituto Médico Legal – IML/POLITEC sempre'),
                                 ('Acionar a Defesa Civil Estadual e a Defesa Civil Municipal', 'Acionar a Coordenadoria Estadual de Proteção e Defesa Civil e a Coordenadoria Municipal de Proteção e Defesa Civil'),
                                 ('Acionar o helicóptero do GTA nos acidentes', 'Acionar a aeronave do Grupamento de Operações Aéreas – GOA nos acidentes')]},
        'se-art-147': {'caput': [('emprego desnecessário de bombeiros militares. Disposições Gerais', 'emprego desnecessário de bombeiros militares.')]},
    },
    'servico-interno-dia': {
        # 16/09: escala publicada em Boletim Interno
        'se-art-109': {'caput': [('Depois de publicada a escala em Boletim Geral', 'Depois de publicada a escala em Boletim Interno')]},
        # ── Resíduos de nomenclatura do RISD de Sergipe (15/09/2026) ──
        'se-art-58': {'caput': [('Subcomandante de cada Unidade', 'Subcomandante de cada OBM')]},
        'se-art-100': {'caput': [('Comandante-Geral, Subcomandante ou Comandante Operacional', 'Comandante-Geral, Subcomandante-Geral ou Comandante Operacional')]},
        'se-art-61': {'items': [('pelo Chefe da Prontidão de Serviço que entra', 'pelo Oficial de Dia que entra')]},
        'se-art-72': {'caput': [('Cada Unidade Operacional deverá', 'Cada OBM deverá')]},
        'se-art-76': {'caput': [('solicitados a Diretoria de Pessoal, Ensino e Instrução', 'solicitados à Coordenadoria de Educação, Ensino e Instrução')]},
        'se-art-91': {'caput': [('apresentar-se ao Chefe da Prontidão,', 'apresentar-se ao Oficial de Dia,')]},
        'se-art-106': {'caput': [('baixada ao Setor de Manutenção', 'baixada ao Centro de Manutenção')]},
        'se-art-107': {'caput': [('equipe de mecânicos as Unidades', 'equipe de mecânicos às OBM')]},
        'se-art-77': {'caput': [('O Oficial de Dia e/ou o Oficial de Dia, ao entrar de serviço', 'O Oficial de Dia, ao entrar de serviço')]},
        'se-art-78': {'caput': [('O acesso aos alojamento deve obedecer', 'O acesso aos alojamentos deve obedecer')]},
        'se-art-81': {'caput': [('ficando proibido a prática', 'ficando proibida a prática')]},
        'se-art-83': {'caput': [('deverá está consciente', 'deverá estar consciente')]},
        'se-art-90': {'caput': [('lubrific ado', 'lubrificado')]},
        'se-art-98': {'caput': [('o mlitar deverá trajar', 'o militar deverá trajar')]},
        'se-art-107': {'caput': [('condições de conserto no local. Operacional', 'condições de conserto no local.')]},
    },
    'disposicoes-finais': {
        # Resíduo da adaptação CBMMT→CBMRO: em RO as unidades são Grupamentos (LOB, Art. 47).
        'mt-art-264': {'caput': [('estabelecidas aos Batalhões Bombeiro Militar', 'estabelecidas aos Grupamentos de Bombeiro Militar'),
                                 ('das demais Unidades e Subunidades integrantes', 'das demais Organizações Bombeiro Militar integrantes')]},
        'mt-art-265': {'caput': [('As Unidades e Subunidades de todos os órgãos e níveis da Corporação', 'Os órgãos e as Organizações Bombeiro Militar de todos os níveis da Corporação')]},
        # Rodapé de publicação do Boletim de MT colado no caput do artigo de fecho.
        'mt-art-266': {'caput': [(' ** Este texto não substitui o publicado no Boletim Geral Eletrônico – BGE', ''),
                                 ('ao presente Regulamento Geral', 'ao presente Regulamento')]},
    },
}

# Correções de grafia válidas para o documento INTEIRO: "Comandante Geral" → "Comandante-Geral",
# a grafia da Lei nº 2.204/2009. Aplicada em todo artigo que traga o termo (18 na exportação).
CORRECOES_GLOBAIS = [
    ('Comandante Geral', 'Comandante-Geral'),
    # Nomenclatura de RO (15/09/2026): o órgão é o Centro Integrado de Operações – CIOP (nome da
    # NGA-CIOP-001/2026), masculino; o texto herdado dizia "Central Integrada" com gênero variado.
    ('ao Central Integrada de Operações', 'ao Centro Integrado de Operações'),
    ('à Central Integrada de Operações', 'ao Centro Integrado de Operações'),
    ('da Central Integrada de Operações', 'do Centro Integrado de Operações'),
    ('do Central Integrada de Operações', 'do Centro Integrado de Operações'),
    ('na Central Integrada de Operações', 'no Centro Integrado de Operações'),
    ('pela Central Integrada de Operações', 'pelo Centro Integrado de Operações'),
    ('uma Central Integrada de Operações', 'um Centro Integrado de Operações'),
    ('Central Integrada de Operações', 'Centro Integrado de Operações'),
    # Sergipe: Boletim Geral Ostensivo → Boletim Geral (RO); Comandante do Socorro → de Socorro;
    # "Comandante da Unidade" → da OBM.
    ('Boletim Geral Ostensivo', 'Boletim Geral'),
    # Determinação de 15/09/2026: a figura do COMANDANTE DE SOCORRO deixa de existir. Quem comanda o
    # serviço é o Oficial de Dia; nas localidades sem Oficial de Dia, o Comandante de Guarnição (o
    # militar mais antigo de serviço) — parágrafo único acrescentado ao artigo das funções (se-art-4).
    ('Comandante do Socorro', 'Oficial de Dia'),
    ('Comandante do socorro', 'Oficial de Dia'),
    ('Comandante de Socorro', 'Oficial de Dia'),
    ('Comandante de socorro', 'Oficial de Dia'),
    ('Cmt de Socorro', 'Oficial de Dia'),
    ('Comandante da Unidade', 'Comandante da OBM'),
]

# ── ALTERAÇÕES (só na versão atual) ───────────────────────────────────────────────────

# (1) Textos finais SUBSTANTIVOS fechados no portal: mudam regra (a quem se reporta, quem
# autoriza, base legal). O id NÃO muda (é o mesmo artigo, com decisão da curadoria) — o
# artigo ganha `alterado: 'texto final'`. Entradas com 'fundamento'/'alterado' próprios são
# ajustes de redação feitos na curadoria de set/2026 (`alterado: 'redação'`). Em 'items', o
# valor None SUPRIME o inciso: o texto vira vazio (o portal pula itens vazios sem re-indexar
# os demais — AR-03) e o índice fica registrado em `incisos_suprimidos`.
TEXTOS_FINAIS_ATUAL = {
    'servico-operacional': {
        # A Parte I da minuta publicável é comum ao serviço operacional e ao serviço técnico
        # (Título II da Parte II); a finalidade não pode falar só do operacional (15/09).
        'se-art-1': {
            'caput': 'O presente Regulamento tem por finalidade dispor sobre o serviço operacional e o serviço técnico no âmbito do Corpo de Bombeiros Militar do Estado de Rondônia, estabelecendo princípios doutrinadores, uniformizando procedimentos e definindo competências para melhorar a eficiência da execução das ações, operações e atividades técnicas de caráter bombeiro militar.',
            'fundamento': _F_CURADORIA, 'alterado': 'redação',
            'nota': 'Finalidade estendida ao serviço técnico (15/09/2026): a Parte I da minuta publicável é comum aos dois serviços.',
        },
        # 16/09 (Arts. 52–59 da publicável): o capítulo do Superior de Dia abre com o artigo de abrangência/regime
        # (se-art-31-c1) e o Comandante do COB I coordena o serviço, a escala e as permutas, sem o gabinete do
        # Subcomando-Geral; "sobreaviso de 24 horas" fica só no artigo de abertura.
        'se-art-24': {
            'caput': 'Durante o período de serviço, o Superior de Dia não deverá se ausentar da área de sua residência, permanecendo em condições de pronto acionamento, com o telefone celular funcional ligado ou outro meio de comunicação que permita seu imediato contato e comparecimento, o qual deverá ser informado ao Comandante do COB I.',
            'items': {0: '§ 1º Ao final do serviço, o Superior de Dia deverá assinar, via Sistema Eletrônico de Informações - SEI, juntamente com o Oficial de Dia, a Parte Diária.',
                      1: '§ 2º O regime do serviço poderá sofrer alterações, mediante publicação em Boletim Geral, por determinação do Comandante-Geral ou do Comandante do COB I, em virtude das necessidades do momento.'},
            'fundamento': _F_REV16, 'alterado': 'redação',
            'nota': 'Revisão de 16/09/2026: o regime de sobreaviso de 24 horas e os postos passam ao artigo de abertura do capítulo; aqui ficam as obrigações durante o serviço. Comandante do COB I no lugar do Subcomandante-Geral.',
        },
        'se-art-25': {'caput': 'A permuta de serviço do Superior de Dia só será permitida mediante autorização por escrito do Comandante do COB I, via Sistema Eletrônico de Informações - SEI.'},
        'se-art-26': {'caput': 'O serviço de Superior de Dia será coordenado pelo Comandante do COB I.',
                      'items': {0: 'Parágrafo único. As escalas serão publicadas em processo eletrônico, via Sistema Eletrônico de Informações - SEI.'},
                      'fundamento': _F_REV16, 'alterado': 'redação',
                      'nota': 'Revisão de 16/09/2026: coordenação exclusiva do Comandante do COB I, sem relação com o gabinete do Subcomando-Geral.'},
        'se-art-27': {'caput': 'O regime da escala de serviços diários de Superior de Dia obedecerá ao critério de dias corridos, podendo, a critério do Comandante do COB I, ser alterado.',
                      'fundamento': _F_REV16, 'alterado': 'redação'},
        'se-art-29': {'caput': 'O militar que concorre à escala aqui tratada quando tiver que se ausentar ou retornar às suas atividades normais em decorrência de férias, dispensas, licenças ou que comporão as mesmas deverá dar ciência ao Comandante do COB I a fim de ser reinserido ou inserido na respectiva escala.'},
        'se-art-33': {'caput': 'A permuta de escala do Oficial de Dia, só será permitida mediante autorização por escrito do Comandante Operacional de Bombeiros do CBMRO, via Sistema Eletrônico de Informações - SEI.', 'fundamento': _F_REV16, 'alterado': 'redação'},
        # 16/09: escalas de quem trabalha no expediente (inciso II e alínea a)
        'se-art-23': {'items': {5: 'II. As escalas para quem trabalha no expediente:', 6: 'a) 6 horas de trabalho por 18 horas de folga da escala;'}, 'fundamento': _F_REV16, 'alterado': 'redação'},
        # 16/09: procedimentos nas operações seguem o SCI (os 11 artigos seguintes foram suprimidos nas duas versões)
        'se-art-136': {'caput': 'Os procedimentos nas operações para efeito deste Regulamento deverão seguir os princípios do Sistema de Comando de Incidentes – SCI.', 'fundamento': _F_REV16, 'alterado': 'redação'},
        # Acidente com viatura: sem a cláusula de "acordo formal entre as partes" (IV), sem a
        # "ficha de acidentes", documento que não existe (V), e o relato em Parte Especial (VIII).
        'se-art-127': {
            'items': {3: 'IV. Solicitar o comparecimento da perícia de trânsito para que seja feito o laudo;',
                      4: None,
                      7: 'VIII. Relatar os fatos, através de Parte Especial.'},
            'fundamento': _F_CURADORIA, 'alterado': 'redação',
        },
        # Nas ocorrências com socorros de duas ou mais Unidades, o que se exige é a CIÊNCIA do
        # Superior de Dia, não a presença do Oficial de Dia.
        'se-art-132': {
            'caput': 'Torna-se obrigatória a ciência ao Superior de Dia nas ocorrências que envolvam os socorros de duas ou mais OBM.',
            'fundamento': _F_CURADORIA, 'alterado': 'redação',
        },
        # Redação simplificada da reserva operacional.
        'se-art-134': {
            'caput': 'Nas ocorrências de grande vulto, deverá, pelo menos por questão de conveniência, existir um socorro de combate a incêndio de reserva para atender quaisquer outras emergências que porventura venham a acontecer.',
            'fundamento': _F_CURADORIA, 'alterado': 'redação',
        },
        # Apoio externo: IX (SAMU) e X (companhia de elevadores) saem — não existem em todas as
        # localidades com OBM; XII (Capitania dos Portos) fica condicionado às localidades que
        # têm o órgão. XI (GOA): nomenclatura corrigida em CORRECOES; quem aciona a aeronave e
        # o protocolo para o interior continuam sem redação (decisão do COB/GOA).
        # Deliberação de 15/09/2026 (quadro de dispositivos semelhantes, grupo 3): no inciso VI
        # fica só a primeira frase; o "Parágrafo Único. Os casos omissos…" que veio grudado no
        # inciso pela extração sai daqui — a regra dos casos omissos permanece íntegra no
        # parágrafo único do artigo dos pacientes com transtorno mental (se-art-116).
        'se-art-114': {
            'items': {0: 'I. O bombeiro militar de folga que primeiro presencie uma ocorrência deverá, dentro do possível, não se omitir de prestar os primeiros atendimentos antes da chegada da Guarnição de Serviço;',
                      1: 'II. Após a chegada da Guarnição de Serviço deverá repassar todas as informações coletadas anteriormente ao responsável pela guarnição independentemente do seu nível hierárquico e funcional sobre este, não interferindo, desde então, no desenrolar das operações, salvo se autorizado pela autoridade competente;',
                      2: 'III. Caso seja necessária a sua presença no local deverá assim proceder, providenciando junto à Guarnição de Serviço os equipamentos de proteção individual para que possa participar das operações;',
                      3: 'IV. Caso o militar presencie a Guarnição de Serviço atuando em uma ocorrência, somente fará parte das operações caso seja solicitado pelo responsável por ela;',
                      4: 'V. A participação do militar de folga em ocorrência deverá se limitar ao auxílio, inicialmente, à(s) vítima(s) e à Guarnição de Serviço, evitando aparecer ou responder aos questionamentos da imprensa e de terceiros presentes no local, salvo se autorizado pela autoridade competente; e',
                      5: 'VI. A participação de pessoas e de outros órgãos no local da ocorrência deverá, inicialmente, ser analisada pelo Oficial de Dia/Comandante de Guarnição.'},
            'fundamento': _F_REV16, 'alterado': 'redação',
            'nota': 'Inciso VI: deliberação de 15/09 (casos omissos) e revisão de 16/09 (Guarnição de Serviço; Oficial de Dia/Comandante de Guarnição).',
        },
        # Determinação de 15/09/2026: ficam só Superior de Dia, Oficial de Dia, Comandante de Guarnição,
        # Condutor e Operador de Viaturas, Operador de Rádio, Socorristas e Permanência. Saem Comandante
        # de Área, Comandante de Socorro, Adjunto ao Oficial de Dia, Auxiliares do Comandante da
        # Guarnição, Comandante de Guarda de Quartel e Auxiliar da Guarda de OBM. O parágrafo único
        # fixa a regra: sem Oficial de Dia na localidade, comanda o Comandante de Guarnição (o mais antigo).
        'se-art-4': {
            'items': {1: None, 2: None, 4: None, 7: None, 9: None, 10: None},
            'acrescentar': ['Parágrafo único. O serviço de Oficial de Dia existe apenas no 1º Grupamento de Bombeiro Militar, na Capital; nas demais Organizações Bombeiro Militar, o Comandante de Guarnição, militar mais antigo de serviço, é o responsável pelo serviço operacional diário, aplicando-se-lhe as atribuições conferidas ao Oficial de Dia neste Regulamento.'],
            'fundamento': _F_CURADORIA, 'alterado': 'redação',
        },
        'se-art-135': {
            'items': {8: None, 9: None,
                      11: 'XII. Solicitar o apoio da Capitania dos Portos, nas localidades onde houver o referido órgão, nos acidentes aquáticos.'},
            'fundamento': _F_CURADORIA, 'alterado': 'redação',
            'nota': 'Inciso XI: quem aciona a aeronave do GOA e o protocolo para ocorrências no interior do Estado seguem sem redação — a definir pelo COB/GOA.',
        },
    },
    'servico-interno-dia': {
        # Lote de 16/09/2026: Guarnição de Serviço no lugar de Prontidão; Oficial de Dia/Comandante de
        # Guarnição (ou do SGBM) onde a atribuição vale para todas as OBM.
        'se-art-102': {'caput': 'Qualquer empréstimo de material operacional, além de registrado na Parte Diária da OBM cedente deverá ser realizado mediante cautela devidamente assinada pelo seu Comandante.', 'fundamento': _F_REV16, 'alterado': 'redação'},
        'se-art-93': {'items': {0: 'Parágrafo único. Quaisquer danos ocorridos no EPI do bombeiro militar de serviço deverão obedecer ao mesmo parâmetro estabelecido para o material operacional, devendo as peças de fardamento danificadas, como meio de comprovação, acompanharem o procedimento administrativo adequado.'}, 'fundamento': _F_REV16, 'alterado': 'redação'},
        'se-art-61': {
            # 16/09 (ajuste do Art. 69 da publicável): só no 1º GBM há passagem de serviço do Oficial de Dia
            # que sai ao que entra; nas demais OBM o Comandante do SGBM apenas conduz a solenidade.
            'caput': 'A passagem de serviço, presidida pelo Oficial de Dia no 1º Grupamento de Bombeiro Militar e conduzida, nas demais Organizações Bombeiro Militar, pelo Comandante do Subgrupamento de Bombeiro Militar, deverá ser assim realizada:',
            'items': {0: 'I. O Oficial de Dia que sai ou, nas demais Organizações Bombeiro Militar, o Comandante do SGBM, posicionado em posição intermediária defronte à tropa, comanda “para passagem de serviço – sentido”.',
                      1: 'II. No 1º Grupamento de Bombeiro Militar, o Oficial de Dia que entra tomará o mesmo procedimento previsto no item anterior.',
                      2: 'III. O Oficial de Dia que sai ou o Comandante do SGBM comanda: “para os Comandantes de Guarnições, um passo em frente, marche”. No 1º Grupamento de Bombeiro Militar, tal ato será também comandado pelo Oficial de Dia que entra.',
                      4: 'V. No 1º Grupamento de Bombeiro Militar, apresentados todos os Comandantes de Guarnição e passadas todas as alterações existentes, o Oficial de Dia que sai se apresenta passando o serviço ao Oficial de Dia que entra. a. O Oficial de Dia que entra comandará: - “Em continência ao terreno apresentar armas”, b. O Oficial de Dia que sai comandará: - “Apresentar armas” c. Em seguida, o Oficial de Dia que entra comandará: -“Descansar armas”, repetindo o mesmo o Oficial de Dia que sai, d. Por fim, ambos comandarão: - “Descansar”.'},
            'acrescentar': ['Parágrafo único. Nas demais Organizações Bombeiro Militar, o Comandante do SGBM apenas conduz a solenidade, não havendo passagem de serviço a ele; o ato encerra-se com a passagem do serviço entre os Comandantes de Guarnição, na forma do inciso IV.'],
            'fundamento': _F_REV16, 'alterado': 'redação',
            'nota': 'Oficial de Dia só no 1º GBM (Capital): só ali há passagem de serviço do Oficial de Dia que sai ao que entra; nas demais OBM o Comandante do SGBM apenas conduz a solenidade (16/09/2026).',
        },
        'se-art-62': {'caput': 'Toda Guarnição de Serviço que entra de serviço deverá obrigatoriamente conferir o material constante na carga da viatura, comunicando as faltas e carências ao Oficial de Dia/Comandante do SGBM.', 'fundamento': _F_REV16, 'alterado': 'redação'},
        'se-art-63': {'caput': 'Por ocasião da conferência do material operacional constante na viatura, ficará a Guarnição de Serviço responsável de dar manutenção em todos os equipamentos deixando-os em perfeitas condições de uso.', 'fundamento': _F_REV16, 'alterado': 'redação'},
        'se-art-66': {'caput': 'Não será admitido por parte da Guarnição de Serviço qualquer desconhecimento do material operacional.', 'fundamento': _F_REV16, 'alterado': 'redação'},
        'se-art-68': {'caput': 'O Oficial de Dia/Comandante de Guarnição deverá supervisionar a conferência de todo o material.', 'fundamento': _F_REV16, 'alterado': 'redação'},
        'se-art-70': {'caput': 'Todo o pessoal de serviço deverá utilizar os Equipamentos de Proteção Individual nos atendimentos de todas e quaisquer ocorrências, devendo o Oficial de Dia/Comandante de Guarnição verificar a disponibilidade e o uso correto dos EPI.', 'fundamento': _F_REV16, 'alterado': 'redação'},
        'se-art-82': {'caput': 'A Guarnição de Serviço ao ouvir o toque de alerta referente ao emprego de seu socorro deverá imediatamente deslocar-se para viatura, para deixar o quartel e partir para o local da ocorrência.', 'fundamento': _F_REV16, 'alterado': 'redação'},
        'se-art-83': {'caput': 'A Guarnição deverá estar consciente de que o tempo entre o alarme e o início das operações de socorro deverá ser o mais breve possível, pois quanto menor o tempo de atendimento, maiores serão as possibilidades de êxito.', 'fundamento': _F_REV16, 'alterado': 'redação'},
        'se-art-87': {'caput': 'Mesmo um aviso de pessoas em risco, o Oficial de Dia/Comandante da Guarnição não deverá permitir que se coloque em segundo plano a segurança da guarnição em função de um mínimo de ganho de tempo.', 'fundamento': _F_REV16, 'alterado': 'redação'},
        'se-art-88': {'caput': 'O Oficial de Dia/Comandante da Guarnição não deverá deixar que os bombeiros militares posicionados sobre a viatura se desloquem em condições de insegurança, devendo para isso, orientá-los a firmar seu corpo em algum ponto de apoio existente na viatura, inclusive usar o cinto de segurança.', 'fundamento': _F_REV16, 'alterado': 'redação'},
        'se-art-89': {'caput': 'Ao chegar de qualquer ocorrência o Oficial de Dia/Comandante da Guarnição deverá colocar a tropa em forma, comentar os acertos e erros acontecidos durante a operação para possíveis correções.', 'fundamento': _F_REV16, 'alterado': 'redação'},
    },
}

# (2) Supressões — "Excluir" fechado no portal + duplicidades apontadas na análise
# (se-art-36/37/38 repetem 29/30/31; 46/47 repetem 42/43). O bloco do Oficial de Dia (32-38)
# é substituído pelos artigos novos do Cel. (ver INCLUIR abaixo). O `motivo` sai no comparativo.
SUPRIMIR = {
    'servico-operacional': {
        'se-art-32': 'Suprimido — regime do Oficial de Dia refeito pelos artigos novos',
        'se-art-34': 'Suprimido — regime do Oficial de Dia refeito pelos artigos novos',
        'se-art-35': 'Suprimido — regime do Oficial de Dia refeito pelos artigos novos',
        'se-art-36': 'Suprimido — duplica o Art. 14 da versão em consulta (se-art-29)',
        'se-art-37': 'Suprimido — duplica o Art. 15 da versão em consulta (se-art-30)',
        'se-art-38': 'Suprimido — duplica o Art. 16 da versão em consulta (se-art-31) e está no bloco errado',
        'se-art-46': 'Suprimido — duplica o Art. 27 da versão em consulta (se-art-42)',
        'se-art-47': 'Suprimido — duplica o Art. 28 da versão em consulta (se-art-43)',
        'se-art-30': ('Suprimido — duplicidade com o Art. 10 da versão em consulta (se-art-25, permuta do '
                      'Superior de Dia). Atenção: o prazo de 48 horas e o formulário de permuta saem junto — '
                      'se forem mantidos, redigir como parágrafo do Art. 10.'),
        'se-art-43': 'Deslocado — o artigo dos casos omissos passa a fechar o capítulo (ro-art-2-c1).',
        'se-art-112': 'Suprimido — permuta fora do mês; matéria da rotina interna de cada OBM.',
    },
    # Resíduo de Sergipe (15/09/2026): a "Reserva Técnica Operacional (RTO)" é figura do RISD do
    # CBMSE, sem previsão na LOB ou nas normas de RO — o capítulo inteiro sai (e com ele as
    # referências aos uniformes "4ºA" e "5B" do regulamento de uniformes de Sergipe).
    'servico-interno-dia': {
        'se-art-95': 'Suprimido — Reserva Técnica Operacional (RTO), figura do RISD/CBMSE sem previsão em RO',
        'se-art-96': 'Suprimido — idem (RTO)',
        'se-art-97': 'Suprimido — idem (RTO)',
        'se-art-98': 'Suprimido — idem (RTO); citava o uniforme "4ºA" do CBMSE',
        'se-art-99': 'Suprimido — idem (RTO); citava o uniforme "5B" do CBMSE',
    },
}

# (2b) Suprimidos (lote de 16/09/2026). Desde a revisão geral de 16/09 TODA supressão (SUPRIMIR
# e SUPRIMIR_AMBAS) sai das duas versões e é registrada em chapter.suprimidos com 'ambas': True;
# as duas tabelas só se distinguem pela data/motivo.
_M16 = 'Suprimido na revisão de 16/09/2026'
SUPRIMIR_AMBAS = {
    'servico-operacional': {
        'se-art-31': _M16 + ' (duplicidade com o artigo de regime do Superior de Dia, que já fixa o alcance estadual)',
        'se-art-39': _M16 + ' (escala do Oficial de Dia: regime já disciplinado no artigo de regime, só no 1º GBM)',
        'se-art-40': _M16 + ' (idem)',
        'se-art-41': _M16 + ' (idem)',
        'se-art-42': _M16 + ' (idem)',
        'se-art-44': _M16 + ' (capítulo das demais funções de serviço nas unidades eliminado)',
        'se-art-45': _M16 + ' (capítulo das demais funções de serviço nas unidades eliminado)',
        **{f'se-art-{n}': _M16 + ' (áreas de emergência/apoio emergencial substituídas pela remissão ao Sistema de Comando de Incidentes – SCI)' for n in range(137, 148)},
        'se-art-116': _M16 + ' (protocolo de pacientes com transtorno mental e casos omissos: fora do Regulamento)',
    },
    'servico-interno-dia': {
        'se-art-54': _M16 + ' (quadro de atividades diárias eliminado; o capítulo passa a "Da passagem de serviço")',
        **{f'se-art-{n}': _M16 + ' (prova de bomba armar, instruções diárias e alojamento: fora do Regulamento)' for n in range(71, 78)},
        'se-art-91': _M16,
    },
    'disposicoes-finais': {
        'mt-art-265': _M16 + ' (prazo de 60 dias para envio das NGA à Assessoria Legislativa)',
    },
}
# Incisos/parágrafos suprimidos nas duas versões (texto vazio + incisos_suprimidos, sem re-indexar — AR-03).
ITENS_SUPRIMIR_AMBAS = {
    'seguranca-contra-incendio': {'ro-art-6': [0]},   # parágrafo único com a lista nominal das DAT
    # incisos que TEXTOS_FINAIS_ATUAL suprime na atual (items: None) saem também da consulta (revisão de 16/09)
    'servico-operacional': {'se-art-4': [1, 2, 4, 7, 9, 10], 'se-art-127': [4], 'se-art-135': [8, 9]},
}


def _art(caput, dispositivos, fundamento, heading=None, orgao=None, proposta=False, nota=None, suprimir_itens=None):
    a = {'caput': caput, 'dispositivos': list(dispositivos), 'fundamento': fundamento}
    if suprimir_itens:
        a['suprimir_itens'] = list(suprimir_itens)
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
                    'IX - autorizar, via Sistema Eletrônico de Informações - SEI, a permuta de escala do serviço de Oficial de Dia;',
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
                    'V - coordenar o emprego dos recursos humanos e materiais das unidades subordinadas, podendo determinar seu emprego dentro da área de responsabilidade do Grupamento, conforme a necessidade do serviço;',
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
                'I - estabelecer as competências, atribuições e responsabilidades das funções integrantes do serviço operacional e do serviço técnico do Corpo de Bombeiros Militar, definindo os procedimentos funcionais correspondentes às respectivas esferas de atuação;',
                'II - delimitar as competências dos diferentes níveis de comando e das funções integrantes da estrutura operacional e técnica da Corporação, estabelecendo os respectivos limites de atuação e prevenindo conflitos, sobreposições ou lacunas de atribuições;',
                'III - estabelecer os níveis de planejamento, coordenação, supervisão, execução e controle das atividades operacionais e técnicas, observada a estrutura organizacional e a cadeia de comando da Corporação;',
                'IV - assegurar a integração e a adequada articulação entre os diferentes escalões, Organizações Bombeiro Militar, órgãos do Sistema de Segurança Contra Incêndio e Pânico e demais frações da Corporação;',
                'V - adequar a atuação das Organizações Bombeiro Militar e dos órgãos de atividades técnicas às políticas, diretrizes e determinações emanadas do Comando-Geral e dos demais escalões competentes;',
                'VI - promover a padronização dos procedimentos operacionais, técnicos e administrativos diretamente relacionados à execução dos serviços de que trata este Regulamento;',
                'VII - promover a eficiência, a eficácia e a efetividade na execução das atividades operacionais e técnicas, buscando o adequado emprego dos recursos humanos e materiais disponíveis;',
                'VIII - estabelecer fluxos de comunicação, encaminhamento e decisão entre as Organizações Bombeiro Militar, os órgãos de atividades técnicas e os diferentes níveis da cadeia de comando, respeitadas as competências legalmente estabelecidas;',
                'IX - proporcionar aos oficiais e praças orientações funcionais que subsidiem a tomada de decisão e a solução de situações decorrentes da execução das atividades operacionais e técnicas, observados os limites de competência de cada função; e',
                'X - uniformizar os procedimentos de análise de projetos, vistoria, fiscalização e demais atividades de segurança contra incêndio e pânico, nos termos da legislação estadual e das Instruções Técnicas.',
            ],
            _F_SERV, heading='RISD, Caps. I–IV — Finalidade, Objetivos, Políticas e Funções Operacionais',
            nota='Objetivos generalizados em 15/09/2026 para alcançar também o serviço técnico (a Parte I da minuta publicável é comum aos dois serviços); inciso X acrescido. Texto de partida sugerido na consulta (RISD).',
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
_H_CS = 'RISD, Cap. VI — Regime e Escalas de Serviço · Do Oficial de Dia nas unidades'

# (4) Inclusões — artigos NOVOS, inseridos APÓS o id indicado (id da versão em consulta).
# {tema: [{'apos': id, 'artigos': [...]}, ...]}
_H_SSCIP = 'Cap. VI — Do Sistema de Segurança Contra Incêndio e Pânico'

INCLUIR = {
    'seguranca-contra-incendio': [
        {   # Política do serviço técnico — espelho da política do serviço operacional (se-art-3);
            # abre o Título II da Parte II (posição explícita na ESTRUTURA, antes do ro-art-13).
            'apos': 'ro-art-13',
            'artigos': [
                _art(
                    'Entende-se por política do serviço técnico o conjunto de princípios, objetivos e diretrizes destinados a orientar o planejamento, a normatização, a execução e o aperfeiçoamento das atividades de segurança contra incêndio e pânico do Corpo de Bombeiros Militar.',
                    [
                        'Parágrafo único. Constituem objetivos básicos da política do serviço técnico:',
                        'I - promover a proteção da vida, do patrimônio e do meio ambiente por meio da prevenção e da proteção contra incêndio e pânico nas edificações e áreas de risco;',
                        'II - manter atualizadas e uniformes as normas e as Instruções Técnicas de segurança contra incêndio e pânico, observada a legislação estadual;',
                        'III - padronizar, em todo o Estado, os procedimentos de análise de projetos, vistoria, fiscalização e emissão dos certificados e licenças de competência da Corporação;',
                        'IV - assegurar a habilitação e a capacitação continuada dos oficiais e praças que atuam no Sistema de Segurança Contra Incêndio e Pânico;',
                        'V - promover a celeridade, a transparência e a impessoalidade no atendimento ao cidadão e aos responsáveis pelas edificações e áreas de risco;',
                        'VI - integrar as atividades técnicas às atividades operacionais, subsidiando o planejamento das operações com as informações sobre as edificações e áreas de risco;',
                        'VII - fomentar programas de educação pública e a cultura de prevenção de incêndio e pânico; e',
                        'VIII - orientar o emprego dos recursos do serviço técnico segundo critérios de necessidade, eficiência, segurança e capacidade de atendimento.',
                    ],
                    _F_CURADORIA, heading=_H_SSCIP,
                    nota='Artigo novo (15/09/2026): abertura própria do Título II — Do Serviço Técnico, espelho da política do serviço operacional (se-art-3), que passou a abrir o Título I.',
                ),
            ],
        },
    ],
    'servico-operacional': [
        {   # Seção do Superior de Dia — depois do bloco de regime/escala (se-art-24..31)
            'apos': 'se-art-31',
            'artigos': [
                _art(
                    'O serviço de Superior de Dia será estabelecido com abrangência em todo o território estadual, em regime de sobreaviso de 24 (vinte e quatro) horas, concorrendo à respectiva escala os oficiais dos postos de Major BM e Tenente-Coronel BM.',
                    ['Parágrafo único. A atuação do Superior de Dia observará as competências próprias do Comando Operacional de Bombeiros e dos Comandantes das Organizações Bombeiro Militar.'],
                    _F_SERV, heading=_H_SD,
                    nota='Deliberação de 15/09/2026: mantido o alcance estadual do Superior de Dia; o texto de partida sugerido na consulta restringia o serviço à Capital. Postos de Major e Tenente-Coronel conforme a sugestão. Revisão de 16/09/2026: abre o capítulo na minuta publicável; o parágrafo sobre o meio de comunicação saiu por duplicidade com o artigo das obrigações durante o serviço.',
                ),
                _art(
                    'Compete ao Superior de Dia:',
                    [
                        'I - exercer a supervisão superior do serviço operacional em todo o Estado durante o período para o qual estiver escalado, respeitadas as competências dos comandantes das Organizações Bombeiro Militar;',
                        'II - manter-se informado acerca das ocorrências de maior vulto, complexidade ou repercussão verificadas no Estado;',
                        'III - comparecer às ocorrências de grande vulto, complexidade ou repercussão quando acionado, quando entender necessário ou por determinação de autoridade superior;',
                        'IV - acompanhar e supervisionar, quando necessário, o desenvolvimento das operações de maior vulto, respeitada a cadeia de comando operacional estabelecida neste Regulamento;',
                        'V - comunicar aos escalões superiores as ocorrências relevantes, extraordinárias ou de grande repercussão, mantendo-os informados acerca de sua evolução e das providências adotadas;',
                        'VI - promover, quando necessário, a articulação entre as Organizações Bombeiro Militar para o atendimento de ocorrências que demandem emprego integrado de recursos;',
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
                    'O serviço de Oficial de Dia será realizado exclusivamente no 1º Grupamento de Bombeiro Militar, na Capital, em regime presencial de 24 (vinte e quatro) horas, sendo exercido por oficiais dos postos de Segundo-Tenente BM, Primeiro-Tenente BM e Capitão BM.',
                    ['§ 1º O Oficial de Dia é o responsável pelo serviço operacional diário e pelo serviço interno do 1º Grupamento de Bombeiro Militar, competindo-lhe zelar pela disciplina, segurança, ordem e regular funcionamento do aquartelamento durante o período de serviço.',
                     '§ 2º O Oficial de Dia representará, durante o período de serviço e nos limites de suas atribuições, a autoridade do Comandante do 1º Grupamento de Bombeiro Militar perante a prontidão operacional e nas questões relacionadas à disciplina e à segurança interna.'],
                    _F_SERV, heading=_H_OD,
                    nota='Alcance definido em 15/09/2026: o Oficial de Dia existe só no 1º GBM (Capital) e responde pelo serviço operacional diário e pelo serviço interno; nas demais OBMs o Comandante de Guarnição é o responsável (se-art-4, parágrafo único). Texto de partida sugerido na consulta (serviço interno do QCG).',
                ),
                _art(
                    'Compete ao Oficial de Dia:',
                    [
                        'I - participar das solenidades, formaturas e demais atos regulamentares previstos para o início e término do serviço;',
                        'II - receber do Oficial de Dia substituído e transmitir ao seu substituto as ordens, determinações, alterações e demais informações necessárias à continuidade do serviço;',
                        'III - orientar os militares empregados nos serviços internos do quartel quanto às suas atribuições e às determinações em vigor;',
                        'IV - realizar inspeções nas dependências do quartel, adotando ou solicitando as providências necessárias diante das irregularidades constatadas;',
                        'V - fiscalizar os serviços internos, verificando o cumprimento das normas, ordens e determinações em vigor;',
                        'VI - zelar pela disciplina, segurança e ordem no interior do quartel;',
                        'VII - fiscalizar os serviços de guarda e segurança do aquartelamento;',
                        'VIII - certificar-se de que as dependências que devam permanecer fechadas estejam devidamente resguardadas, mantendo o controle das respectivas chaves nos termos das normas internas;',
                        'IX - providenciar, na forma regulamentar, a substituição dos militares que não comparecerem aos serviços internos para os quais estejam escalados;',
                        'X - zelar pelo cumprimento das normas referentes à entrada, saída e permanência de pessoas no quartel;',
                        'XI - fiscalizar a entrada e saída de viaturas do aquartelamento, observadas as normas estabelecidas;',
                        'XII - registrar a entrada ou saída de materiais do quartel fora do horário de expediente, não permitindo sua retirada sem a devida autorização;',
                        'XIII - zelar pelos materiais, armamentos, instalações e demais bens que estejam sob sua responsabilidade durante o serviço;',
                        'XIV - receber autoridades civis e militares que compareçam ao quartel fora do horário de expediente, adotando as providências protocolares cabíveis;',
                        'XV - comunicar imediatamente à autoridade competente as ocorrências extraordinárias verificadas durante o serviço, especialmente aquelas relacionadas à disciplina, segurança, pessoal ou patrimônio;',
                        'XVI - adotar as providências imediatas destinadas a sanar ou minimizar alterações verificadas no funcionamento interno do quartel, submetendo à autoridade competente aquelas que excedam sua atribuição;',
                        'XVII - receber e encaminhar, fora do horário de expediente, documentos ou comunicações de caráter urgente, adotando as providências necessárias para que cheguem tempestivamente à autoridade competente;',
                        'XVIII - registrar em Parte Diária, via Sistema Eletrônico de Informações - SEI, as ocorrências e alterações verificadas durante sua jornada de serviço;',
                        'XIX - elaborar e encaminhar a parte de serviço à autoridade competente, consignando as ocorrências e alterações relevantes verificadas durante a jornada;',
                        'XX - comunicar imediatamente qualquer acidente envolvendo pessoal, viatura, material ou patrimônio ocorrido no âmbito do quartel;',
                        'XXI - fiscalizar as condições de conservação, limpeza e organização das dependências do quartel;',
                        'XXII - fiscalizar o cumprimento das prisões e detenções de natureza disciplinar executadas nas dependências do aquartelamento, zelando pela observância das determinações da autoridade competente, das condições de segurança e das normas aplicáveis;',
                        'XXIII - diante da ocorrência de fato que, em tese, constitua crime militar, adotar as providências imediatas destinadas à preservação do local, dos elementos de informação e das provas, quando cabíveis, bem como comunicar imediatamente o fato à autoridade de polícia judiciária militar competente, para adoção das medidas previstas na legislação processual penal militar;',
                        'XXIV - adotar, nas hipóteses de flagrante de crime militar, as providências que lhe competirem nos termos da legislação processual penal militar, comunicando imediatamente o fato à autoridade de polícia judiciária militar competente; e',
                        'XXV - cumprir e fazer cumprir as ordens e determinações dos escalões superiores relacionadas ao serviço interno do aquartelamento.',
                    ],
                    _F_SERV, heading=_H_OD, suprimir_itens=[18],
                    
                    nota='Incisos X e XIII chegaram truncados na sugestão original ("rviço;" e "durante o se"); completados por dedução — confirmar com o autor. Incisos XXII a XXIV: conferir com a Corregedoria quanto ao CPPM.',
                ),
            ],
        },
        {   # Casos omissos — movido do se-art-43 (Art. 28 da versão em consulta) para o FIM do
            # capítulo. ro-art-2 é o último artigo do tema.
            'apos': 'ro-art-2',
            'artigos': [
                _art(
                    'Os casos omissos serão resolvidos em conjunto pelo Comandante Operacional de Bombeiros e pelo Comandante da OBM.',
                    [],
                    _F_CURADORIA, heading='Dos casos omissos',
                    nota='Movido do Art. 28 da versão em consulta (se-art-43): o artigo dos casos omissos passa a fechar o capítulo do Serviço Operacional. Texto idêntico.',
                ),
            ],
        },
    ],
}

# ── APLICAÇÃO por artigo (coluna "Aplicação" do relatório das interações) ────────────────
# O relatório deduz, artigo a artigo, o que a versão atual fez com cada dispositivo comentado
# pelos militares consultados (aplicacaoPorArtigo em src/lib/consultaRelatorios.js). Quando a
# dedução não enxerga o que aconteceu, o registro explícito abaixo (chave = editId da versão em
# consulta) vence. `como` ∈ COMO_VALIDOS.
COMO_VALIDOS = {'correcao', 'texto-final', 'redacao', 'inciso-suprimido', 'suprimido', 'movido',
                'reescrito', 'incluido'}


def _at(como, nota, onde=None):
    d = {'como': como, 'nota': nota}
    if onde:
        d['onde'] = onde
    return d

# Caso: as 74 sugestões do Cel. Luiz Eduardo sobre se-art-4 (lista das funções do serviço) são
# o Bloco 14 — regime e competências do Superior de Dia, do Oficial de Dia e do Comandante de
# Socorro — que entrou como 6 artigos NOVOS (INCLUIR), não como correção do se-art-4 (o artigo
# só ganhou a correção "º Visando").
# ── DELIBERAÇÕES sobre o quadro de dispositivos com texto semelhante ─────────────────────
# Registro do que o Comando decidiu para cada grupo (sai no fim do quadro, como "deliberações
# já registradas"); a aplicação em si está em TEXTOS_FINAIS_ATUAL/SUPRIMIR.
DELIBERACOES_SEMELHANTES = [
    {
        'data': '2026-09-15',
        'dispositivos': ['servico-operacional/se-art-114#5', 'servico-operacional/se-art-116#5'],
        'assunto': 'Casos omissos repetidos (inciso VI do artigo do bombeiro militar de folga em ocorrência × parágrafo único do artigo dos pacientes com transtorno mental)',
        'decisao': ('No inciso VI mantém-se apenas "A participação de pessoas e de outros órgãos no local da ocorrência '
                    'deverá, inicialmente, ser analisada pelo Comandante do SOS"; o parágrafo único do outro artigo '
                    'mantém a íntegra do texto.'),
    },
    {
        'data': '2026-09-15',
        'dispositivos': ['seguranca-contra-incendio/ro-art-3 × atribuicoes-funcoes/ro-art-15', 'atribuicoes-funcoes/ro-art-3..7 (caputs)',
                         'seguranca-contra-incendio/ro-art-2 × ro-art-7', 'servico-operacional/se-art-23 (alíneas a/b do inciso II)',
                         'atribuicoes-funcoes/ro-art-11 × seguranca-contra-incendio/ro-art-15'],
        'assunto': 'Demais 5 grupos do quadro de dispositivos semelhantes de 15/09/2026',
        'decisao': 'Permanecem como estão (mantidos os dois dispositivos em cada grupo). O quadro foi eliminado do pacote.',
    },
    {
        'data': '2026-09-15',
        'dispositivos': ['servico-operacional/se-art-4', 'servico-operacional/se-art-39..44', 'servico-operacional/se-art-43-c1 (removido)',
                         'servico-interno-dia/se-art-95..99 (removidos)', 'todas as menções a Comandante de Socorro'],
        'assunto': 'Figuras do serviço eliminadas: Comandante de Área, Comandante de Socorro, Adjunto ao Oficial de Dia, Auxiliares do Comandante da Guarnição, Comandante de Guarda de Quartel, Auxiliar da Guarda de OBM; Reserva Técnica Operacional',
        'decisao': ('Ficam Superior de Dia, Oficial de Dia, Comandante de Guarnição, Condutor e Operador de Viaturas, Operador de Rádio, '
                    'Socorristas e Permanência. O Oficial de Dia existe só no 1º GBM (Capital); nas demais OBMs o Comandante de Guarnição, '
                    'militar mais antigo de serviço, é o responsável pelo serviço operacional diário (parágrafo único do artigo das funções). '
                    'As atribuições antes do Comandante de Socorro passam ao Oficial de Dia e, nas demais OBMs, ao Comandante de Guarnição. '
                    'O capítulo da RTO foi suprimido.'),
    },
    {
        'data': '2026-09-15',
        'dispositivos': ['servico-operacional/se-art-1', 'servico-operacional/se-art-2', 'servico-operacional/se-art-3',
                         'seguranca-contra-incendio/ro-art-13-c1 (novo)'],
        'assunto': 'Capítulo dos objetivos e da política do serviço (Parte I) só falava do serviço operacional',
        'decisao': ('A finalidade (se-art-1) e os objetivos do Regulamento (se-art-2) ficam na Parte I, generalizados para os '
                    'dois serviços (inciso X sobre a segurança contra incêndio e pânico acrescido). A política do serviço '
                    'operacional (se-art-3) migra para a Parte II como capítulo de abertura do Título I. O Título II ganha '
                    'capítulo próprio de abertura, "Da política do serviço técnico", com artigo novo espelhado no se-art-3.'),
    },
    {
        'data': '2026-09-15',
        'dispositivos': ['servico-operacional/se-art-31', 'servico-operacional/se-art-31-c1', 'servico-operacional/se-art-31-c2 (incisos I, II e VI)'],
        'assunto': 'Alcance do serviço de Superior de Dia (proposta da consulta: só na Capital)',
        'decisao': ('Mantido o alcance estadual (área de atuação em todo o território do Estado). O artigo de regime deixa de ser '
                    'proposta pendente; as competências deixam de citar a Capital. Postos de Major e Tenente-Coronel mantidos.'),
    },
    {
        'data': '2026-09-16',
        'dispositivos': ['servico-operacional/se-art-31, 39..42, 44, 45, 116, 137..147', 'servico-operacional/se-art-43-c1 (removido)',
                         'servico-interno-dia/se-art-54, 71..77, 91', 'disposicoes-finais/mt-art-265', 'seguranca-contra-incendio/ro-art-6 (parágrafo único)',
                         'servico-operacional/se-art-23, 24, 25, 26, 29, 33, 109, 114, 136', 'servico-interno-dia/se-art-61, 62, 63, 66, 68, 70, 82, 83, 87, 88, 89, 93, 102',
                         'atribuicoes-funcoes/ro-art-1-r2 (IX), ro-art-2-r1 (V)', 'servico-operacional/se-art-38-c2 (XVIII, XIX)'],
        'assunto': 'Lote de revisão de 16/09/2026 (documento "Faça as seguintes modificações nos textos")',
        'decisao': ('Supressões aplicadas nas DUAS versões (consulta e atual): área de atuação do Superior de Dia (duplicidade), '
                    'escala/regime do Oficial de Dia (Arts. 64–67), competências operacionais do Oficial de Dia (Art. 68, já constam '
                    'no Art. 63; inciso XIX das competências suprimido por duplicidade com o XVIII), capítulo das demais funções de '
                    'serviço (Arts. 69–70), quadro de atividades (Art. 71; capítulo renomeado "Da passagem de serviço"), instruções e '
                    'alojamento (Arts. 88–94), Art. 108, áreas de emergência (Arts. 119–129, substituídas pela remissão ao SCI no '
                    'Art. 118), pacientes com transtorno mental (Art. 130), lista nominal das DAT e prazo das NGA (Art. 163). '
                    'Alterações de texto só na atual: SEI nas permutas e na Parte Diária, Comandante do COB I na coordenação do '
                    'Superior de Dia, Boletim Interno na publicação da escala, Guarnição de Serviço no lugar de Prontidão, '
                    'Oficial de Dia/Comandante de Guarnição (ou do SGBM) nas atribuições comuns a todas as OBM, passagem de '
                    'serviço entre oficiais só no 1º GBM (fora da Capital o Comandante do SGBM apenas conduz a solenidade), EPI no parágrafo dos danos, escalas do expediente.'),
    },
    {
        'data': '2026-09-16',
        'dispositivos': ['servico-operacional/se-art-24, 25, 26, 27', 'servico-operacional/se-art-31-c1 (§ 1º retirado)', 'ordem do capítulo "Do Superior de Dia" na minuta publicável (Arts. 52–59)'],
        'assunto': 'Capítulo do Superior de Dia: coordenação, redundâncias e ordem dos artigos',
        'decisao': ('O Comandante do COB I coordena o serviço, o regime da escala e as permutas, sem relação com o gabinete do Subcomando-Geral. '
                    'A abrangência estadual, o sobreaviso de 24 horas e os postos (Major e Tenente-Coronel) ficam só no artigo de abertura do capítulo '
                    '(se-art-31-c1), seguido das competências; o artigo das obrigações durante o serviço (se-art-24) deixa de repetir o sobreaviso e '
                    'absorve o meio de comunicação. Alterações de texto só na versão atual; nenhum artigo suprimido.'),
    },
]

ATENDIMENTOS_POR_ARTIGO = {
    'reg:atual:servico-operacional/se-art-4': _at(
        'incluido',
        'sugestões do Cel. Luiz Eduardo sobre o artigo das funções do serviço: os artigos de regime e '
        'de competências do Superior de Dia, do Oficial de Dia e do Comandante de Socorro entraram na '
        'versão atual como artigos novos (se-art-31-c1/c2, se-art-38-c1/c2); as duas propostas de mérito foram decididas em 15/09: Superior de Dia mantém o alcance '
        'estadual; Oficial de Dia só no 1º GBM)',
    ),
}


# ── Aplicação ────────────────────────────────────────────────────────────────────────
def _tema(cap):
    return cap['id'].split(':')[-1]


def _prefixo(cap):
    return cap['id'][: -len(_tema(cap))]  # 'reg:atual:' ou 'reg:'


def aplicar_correcoes(structure):
    """Aplica CORRECOES e CORRECOES_GLOBAIS in place (só na versão atual). Aborta se um
    trecho de CORRECOES não existir; as globais exigem ao menos um artigo atingido."""
    n = 0
    pendentes = {(t, i) for t, arts in CORRECOES.items() for i in arts}
    atingidos_globais = 0
    for cap in structure['chapters']:
        tema = _tema(cap)
        regras = CORRECOES.get(tema, {})
        for art in cap['articles']:
            for velho, novo in CORRECOES_GLOBAIS:
                achou = velho in art.get('caput', '')
                art['caput'] = art.get('caput', '').replace(velho, novo)
                for it in art.get('items', []):
                    if velho in it['text']:
                        it['text'] = it['text'].replace(velho, novo)
                        achou = True
                if achou:
                    art['corrigido'] = True
                    atingidos_globais += 1
                    n += 1
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
    if CORRECOES_GLOBAIS and not atingidos_globais:
        raise SystemExit('CORRECOES_GLOBAIS não atingiram nenhum artigo — conferir o trecho')
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
    for idx in spec.get('suprimir_itens', []):   # inciso suprimido sem re-indexar (AR-03)
        leaf['items'][idx]['text'] = ''
        leaf.setdefault('incisos_suprimidos', []).append(idx)
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
                    if idx >= len(art['items']) or not art['items'][idx]['text'].strip():
                        raise SystemExit(f'ALTERACAO aponta para inciso inexistente: {tema}/{aid}#{idx}')
                    if texto is None:  # supressão do inciso, sem re-indexar (AR-03)
                        art['items'][idx]['text'] = ''
                        art.setdefault('incisos_suprimidos', []).append(idx)
                    else:
                        art['items'][idx]['text'] = texto
                for texto in f.get('acrescentar', []):
                    art['items'].append({'text': texto, 'source': f.get('fundamento', _F_FINAL)})
                    art.setdefault('incisos_acrescidos', []).append(len(art['items']) - 1)
                art['alterado'] = f.get('alterado', 'texto final')
                art['fundamento_alteracao'] = f.get('fundamento', _F_FINAL)
                if f.get('nota'):
                    art['nota'] = f['nota']
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


def aplicar_supressoes_comuns(structure, incluir_suprimir=False):
    """SUPRIMIR_AMBAS e ITENS_SUPRIMIR_AMBAS (e, com incluir_suprimir, também SUPRIMIR — usado na
    versão em consulta, onde aplicar_alteracoes não roda). Toda supressão fica registrada em
    chapter.suprimidos com 'ambas': True. Aborta se um id não existir."""
    n_art = n_it = 0
    for cap in structure['chapters']:
        tema = _tema(cap)
        sup = dict(SUPRIMIR_AMBAS.get(tema, {}))
        if incluir_suprimir:
            sup.update(SUPRIMIR.get(tema, {}))
        itens = ITENS_SUPRIMIR_AMBAS.get(tema, {})
        ids = {a['id'] for a in cap['articles']}
        for alvo in list(sup) + list(itens):
            if alvo not in ids:
                raise SystemExit(f'SUPRIMIR_AMBAS aponta para id inexistente: {tema}/{alvo}')
        for reg in cap.get('suprimidos', []):   # supressões já aplicadas por aplicar_alteracoes (atual)
            reg['ambas'] = True
        novos = []
        for art in cap['articles']:
            if art['id'] in sup:
                cap.setdefault('suprimidos', []).append({'id': art['id'], 'motivo': sup[art['id']], 'ambas': True})
                n_art += 1
                continue
            for idx in itens.get(art['id'], []):
                if idx < len(art['items']) and idx in art.get('incisos_suprimidos', []):
                    continue   # já suprimido por TEXTOS_FINAIS_ATUAL (atual)
                if idx >= len(art['items']) or not art['items'][idx]['text'].strip():
                    raise SystemExit(f'ITENS_SUPRIMIR_AMBAS aponta para inciso inexistente: {tema}/{art["id"]}#{idx}')
                art['items'][idx]['text'] = ''
                art.setdefault('incisos_suprimidos', []).append(idx)
                n_it += 1
            novos.append(art)
        cap['articles'] = novos
    return {'suprimidos_ambas': n_art, 'incisos_suprimidos_ambas': n_it}


def gerar_versoes(structure):
    """A partir da estrutura gerada (cenário atual, ids reg:atual:), devolve
    (consulta, atual): a consulta é o texto lido pelos militares, menos TODAS as supressões
    (determinação de 16/09); a atual tem CORRECOES + ALTERACOES + as mesmas supressões."""
    invalidos = {k: v['como'] for k, v in ATENDIMENTOS_POR_ARTIGO.items() if v['como'] not in COMO_VALIDOS}
    if invalidos:
        raise SystemExit(f'ATENDIMENTOS_POR_ARTIGO com `como` inválido: {invalidos}')
    consulta = copy.deepcopy(structure)
    consulta['versao'] = 'consulta'
    comuns_c = aplicar_supressoes_comuns(consulta, incluir_suprimir=True)
    consulta['curadoria'] = {**comuns_c, 'atendimentos_artigos': ATENDIMENTOS_POR_ARTIGO, 'deliberacoes': DELIBERACOES_SEMELHANTES}
    atual = copy.deepcopy(structure)
    n_corr = aplicar_correcoes(atual)
    cont = aplicar_alteracoes(atual)
    comuns_a = aplicar_supressoes_comuns(atual)
    atual['versao'] = 'atual'
    atual['curadoria'] = {'correcoes': n_corr, **cont, **comuns_a, 'atendimentos_artigos': ATENDIMENTOS_POR_ARTIGO,
                          'deliberacoes': DELIBERACOES_SEMELHANTES}
    return consulta, atual
