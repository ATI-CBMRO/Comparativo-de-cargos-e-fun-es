# Análise complementar — normas de outros estados no recorte do Regulamento de Serviço

**Data:** 2026-08-13
**Pedido:** o Wândrio pediu, ao autorizar a execução do plano, uma verificação de que a
minuta setorizada não replica normas de outros estados que vão de encontro ao que a LOB
de Rondônia (Lei nº 2.204/2009) já estabelece — além da análise de lacuna transversal já
feita na spec principal (seção "Análise de conteúdo transversal").

**Método:** cada artigo de `regulamento_structure.json` carrega `source` (de qual
regulamento de outro CBM o texto foi adaptado), `original_caput` (o texto antes da
adaptação) e `adapted` (se houve reescrita). Isso permite comparar, artigo a artigo do
recorte de 185 (7 capítulos), o texto final contra o texto de origem, e cruzar nomes de
órgãos citados contra o texto integral da LOB de RO (`database/markdown/Rondônia - LOB
atual (2).md`). **Nenhum arquivo de `database/` foi alterado** — esta é uma análise, a
correção do conteúdo é decisão do Wândrio (e provavelmente do representante da CAT/COB na
reunião, que reconhece os órgãos de cabeça).

## Achado 1 (alta confiança — corrigir antes da reunião): sigla de outro CBM sobrou no texto

Três trechos do capítulo **Central de Operações e do Teledespacho** — justamente matéria
do COB, o público da reunião — citam **"CBMBA"** (Bahia) em vez de CBMRO:

| Artigo | Trecho |
|---|---|
| `reg:atual:central-operacoes-193/ba-art-8` | "...sob a égide do **CBMBA**, sendo o responsável pel[o]..." |
| `reg:atual:central-operacoes-193/ba-art-9`, inciso XXIV | "...previsto no âmbito do **CBMBA**, não permitindo o uso de linguagem inapropriada..." |
| `reg:atual:central-operacoes-193/ba-art-9`, inciso XXVII | "...manter contatos com outros órgãos..." (trecho ok, mas o artigo é o mesmo `ba-art-9`) |

Isto não é "norma de outro estado que conflita" no sentido jurídico — é resíduo de
adaptação incompleta: o texto foi importado do Regulamento do CBM da Bahia e o
find-replace de sigla não cobriu esses três pontos. Um participante da CAT/COB vai notar
na hora. **Recomendo corrigir antes de abrir para a reunião** — é edição de conteúdo
(`database/atual/regulamento_structure.json`), fora do escopo desta entrega de ambiente,
e por isso não mexi; fica registrado aqui para o Wândrio decidir se corrige ele mesmo ou
me pede para corrigir à parte.

## Achado 2 (confiança média — verificar, não é claramente errado): órgãos sem lastro textual na LOB de RO

**15 dos 185 artigos do recorte** foram importados de CBMMT ou CBMSE **sem nenhuma
adaptação de texto** (`caput` idêntico ao `original_caput`). A maioria é inofensiva (regras
de conduta genéricas). Mas 8 desses artigos **atribuem competência a um órgão nomeado**, e
esses nomes não aparecem em lugar nenhum da LOB de RO (busquei o texto completo):

| Órgão citado no artigo importado | Aparece na LOB de RO (2.204/2009)? | Artigo |
|---|---|---|
| Coordenadoria de estudos e análises de processos – **CCIP 1** | Não | `seguranca-contra-incendio/mt-art-206` |
| **Seção de Legislação e Normatização** | Não | `seguranca-contra-incendio/mt-art-213` |
| **Coordenadoria de Perícias Técnicas – CCIP 4** | Não | `seguranca-contra-incendio/mt-art-215` |
| Coordenador de Comunicação Social | Não | `atribuicoes-funcoes/mt-art-111` |
| Comandante do **Centro de Ensino e Instrução de Bombeiros – CEIB** | **Sim** (7 ocorrências) | `atribuicoes-funcoes/mt-art-170` |
| Chefe do **Centro de Capacitação Física** | Não | `atribuicoes-funcoes/mt-art-181`, `182` |
| Diretor da **Escola Dom Pedro II** | Não | `atribuicoes-funcoes/mt-art-190` |
| Comandantes das **Companhias de Bombeiro Militar – CiaBM** | Não | `atribuicoes-funcoes/mt-art-262` |

**Por que isto merece atenção e não é auto-evidente que esteja errado:** a própria LOB de
RO delega a órgãos operacionais (Grupamentos, Subgrupamentos, Pelotões, Seções de
Bombeiros) a definição da "estrutura básica... no regulamento da presente Lei" (Art. 48,
com quatro redações sucessivas — a mais recente pela Lei nº 3.413/2014). Ou seja, para o
lado **operacional (COB)** é normal e esperado que o Regulamento crie unidades que a Lei
não nomeia uma a uma — a Lei antecipou isso.

Já a delegação equivalente para o lado **técnico/prevencional (CAT/DPST)** — o Art. 50,
"Dos Órgãos de Execução Prevencional" — está **revogado pela Lei nº 4.303/2018** no texto
que localizei, sem que eu encontrasse uma redação substituta em vigor. Ou seja: o lastro
legal que autorizaria o Regulamento a nomear sub-unidades dentro da CAT (CCIP, Seção de
Legislação, Escola Dom Pedro II, Centro de Capacitação Física) é, no mínimo, menos claro do
que o lastro do lado operacional. Pode ser que exista uma lei ou decreto posterior que eu
não tenha no acervo local — não afirmo que está errado, só que **não achei o texto que
sustenta**.

**Recomendação:** não é caso de eu corrigir sozinho (é conteúdo técnico-jurídico, não
ambiente de sistema) nem de travar a reunião por causa disso. Sugiro **perguntar
diretamente ao representante da CAT** se essas unidades (CCIP, Seção de Legislação e
Normatização, Escola Dom Pedro II, Centro de Capacitação Física, CiaBM) existem de fato na
estrutura de Rondônia hoje, sob outro nome ou nenhum. Se não existirem, é exatamente o
tipo de manifestação que a tela de Revisão foi feita para capturar — o comentário fica
ancorado no artigo certo (`editId`) e não se perde.

## O que NÃO apareceu (checado e limpo)

- Nenhum outro nome de estado (Mato Grosso, Sergipe, Rio Grande do Sul/Norte, Bahia, Goiás,
  Paraná, Distrito Federal, Santa Catarina, Amazonas, Pará, Ceará) sobrou no texto final
  fora do caso do Achado 1. A primeira varredura acusou 17 ocorrências de "Pará" que eram
  falso-positivo (prefixo de "Parágrafo") — corrigido com busca por borda de palavra antes
  de reportar.
- Os outros 170 artigos importados (185 − 15 idênticos) tiveram texto efetivamente
  reescrito para Rondônia (`adapted: true`, `caput` ≠ `original_caput`).

## Escopo desta análise

Cobre só os **7 capítulos / 185 artigos** do recorte que vai para a reunião de 14/08 — não
os outros 228 artigos do Regulamento Geral completo (Parte I fora do recorte), que ficam
para a 2ª etapa e podem receber a mesma varredura depois.
