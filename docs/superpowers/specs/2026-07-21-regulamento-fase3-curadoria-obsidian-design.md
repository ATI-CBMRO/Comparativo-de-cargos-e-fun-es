# Regulamento — Fase 3: curadoria no Obsidian (repositório conectado + mesa de decisão)

**Data:** 2026-07-21 · **Status:** aprovado (brainstorming com o Wândrio)

## Propósito

O Wândrio quer o Obsidian como **repositório que conecta as legislações** e o ajuda na
**curadoria para a construção da minuta** do Regulamento Geral. Decisões do brainstorming:

1. **Uso principal**: mesa de DECISÃO da redação final (não só arquivo nem só material de
   apresentação — esses vêm de brinde).
2. **Granularidade**: HÍBRIDA — 16 notas de tema + notas de decisão só onde há divergência
   real entre estados (evita 413 notas vazias).
3. **Caminho de volta**: o Wândrio preenche a seção "Decisão CBMRO" na nota; numa sessão, o
   Claude lê as notas decididas e aplica nos dados do portal (ADAPTATIONS/enrichment) com
   verificação verbatim e commit. O vault ORIENTA; scripts/JSON continuam a fonte da verdade.
4. **Partida**: PILOTO — infraestrutura + 1 tema completo (`servico-operacional`), validar o
   formato vendo antes de replicar aos 16.

Relação com o método atual: NÃO substitui a linha de montagem (extração verbatim +
verificação + JSON); acrescenta a etapa de decisão por assunto que faltava.

## Estrutura no vault

Pasta: `Codebases/Comparativo-de-cargos-e-funcoes/Regulamento — Curadoria/` (vault
`/Users/wandriobandeira/Documents/Obsidian Vault/`). 4 tipos de nota:

- **Índice** (`_Índice — Curadoria do Regulamento.md`): porta de entrada — 2 Partes, 16
  temas com estado de decisão (🟢 decidido / 🟡 em curadoria / ⚪ não iniciado), links.
- **Fontes** (~10 notas, `Fonte — <doc>.md`): uma por documento-fonte (Regulamento CBMMT,
  RISD-SE, RI-BA, Regulamento-BA, RR, TO, normas AL, NGA-ES, GO, RISG-Exército): o que é,
  abrangência, em que temas aparece (backlinks). São os hubs do grafo.
- **Temas** (16 notas, `Tema — <tema>.md`): a mesa — tabela de cobertura (estado × matéria),
  contradições entre redações, lacunas, links para decisões. Frontmatter: `parte`,
  `themeKey`, `status`.
- **Decisões** (`Decisão — <tema> — <assunto>.md`, só onde há decisão real): redações
  candidatas lado a lado (verbatim, com fonte citada), prós/contras, seção **"## Decisão
  CBMRO"** (vazia até o Wândrio decidir) + campo `decidido: false` no frontmatter.

Conexões: tema ↔ fontes; decisão ↔ tema ↔ fontes; ligações com notas existentes
(Comparativo RISG Round 1/2, Diário de Construção).

## Regras

- **Semeadura única**: as notas nascem do `database/regulamento_structure.json` (dados já
  verificados — NUNCA reler PDFs para semear). Depois de semeadas, são do Wândrio: nenhuma
  regeneração automática; correção de dado errado se faz na fonte (JSON) e se anota na nota.
- **Verbatim rotulado**: todo excerto citado nas notas carrega a fonte (`cf. …`) exatamente
  como no JSON. Nada de parafrasear texto legal.
- **Aplicar decisão é ação explícita** em sessão (futura skill/rotina), com verificação
  verbatim e commit — nunca automática. Fora do escopo do piloto.
- Notas em pt-BR, tom claro; tabelas enxutas (o material integral está no portal — a nota
  aponta, não duplica tudo).

## Escopo do piloto (esta fase)

1. Criar a pasta + nota Índice.
2. Criar as ~10 notas de Fonte (a partir de `PRIMARY_SOURCE`/fontes do JSON e do CLAUDE.md).
3. Criar a nota do Tema `servico-operacional` (Parte II): cobertura por estado, contradições
   e lacunas detectadas a partir das `alternatives` do JSON.
4. Criar as notas de Decisão do tema-piloto — uma por assunto onde os estados divergem de
   verdade (quantidade descoberta na análise; se um assunto não tiver divergência, não ganha
   nota).
5. Atualizar o Diário de Construção (novo marco) e o índice de notas do projeto.

**Fora do escopo**: os outros 15 temas (rodadas seguintes, após o Wândrio validar o
formato); o mecanismo de "aplicar decisão" no portal; qualquer mudança de código no repo.

## Critérios de aceite

- Notas abrem no Obsidian com backlinks funcionando (grafo conecta tema↔fontes↔decisões).
- Todo excerto verbatim confere com o `regulamento_structure.json` (amostragem verificada).
- Nota de tema responde em 1 tela: quem cobre o quê, onde divergem, o que falta decidir.
- O Wândrio consegue preencher uma "Decisão CBMRO" sem instrução adicional.
