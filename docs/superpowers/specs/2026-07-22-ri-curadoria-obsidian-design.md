# Frente B — Regimento Interno + LOBs no Obsidian (espelho da curadoria)

**Data:** 2026-07-22 · **Status:** aprovado (brainstorming com o Wândrio)

## Objetivo

Expandir o vault para ser o repositório conectado das DUAS minutas: criar a curadoria do
**Regimento Interno** no mesmo formato validado do Regulamento, permitindo análises e
cruzamentos entre estados (e entre RI ↔ Regulamento) para a construção das minutas.

## Escopo (decisões do brainstorming)

- **Recorte**: espelhar a curadoria — notas por ÓRGÃO da minuta (não LOBs integrais
  verbatim; não só RO). Fonte dos dados: `database/minuta_structure.json` (26 órgãos +
  Guarnição, com `alternatives` verbatim de 25 estados — Bloco D) e `database/organs_detail/`
  — NUNCA os .md crus.
- **Cenário**: LOB FUTURA primeiro (é a que tem o comparativo de 25 estados); RI do cenário
  atual fica para onda futura.
- Pasta nova no vault: `Codebases/Comparativo-de-cargos-e-funcoes/Regimento Interno — Curadoria/`
  com os 4 tipos de nota do formato validado:
  - `_Índice — Curadoria do Regimento Interno.md` — órgãos agrupados por bloco da LOB
    (Comando/Direção, Apoio, Execução…), status ⚪/🟡/🟢 por órgão.
  - `Fonte — LOB-<UF>.md` / `Fonte — RI-<UF>.md` — uma nota por documento-fonte que aparece
    nas `alternatives` da minuta do RI (reusar as notas de fonte JÁ existentes do Regulamento
    quando for o MESMO documento — ex.: RI-RS; criar apenas as que faltarem, ex.: LOBs).
  - `Órgão — <organKey>.md` (26+1) — a mesa por órgão: competências de RO (resumo por
    número), tabela de cobertura (quais estados têm órgão equivalente e o que dizem),
    divergências reais, lacunas (os 2 conhecidos: guarnicao sem RISD equivalente; gbm
    homônimo no RS).
  - `Decisão — ri — <organKey> — <assunto>.md` — só onde houver divergência REAL entre
    estados sobre o mesmo órgão (estrutura/subordinação/competência conflitante — não
    redação diferente).
- **Ligações cruzadas** RI ↔ Regulamento onde a matéria se toca (ex.: órgão operacional ↔
  tema servico-operacional), por wikilink nas seções "Ligações".
- Índice do Regulamento e Índice do RI apontam um para o outro.

## Regras (herdadas)

- Semeadura única a partir do JSON verificado; depois as notas são do Wândrio.
- Verbatim rotulado com `cf.` em toda citação de decisão; defeitos de fonte reproduzidos
  e anotados fora da citação; "## Decisão CBMRO" nasce vazia, `decidido: false`.
- pt-BR de gestor; tabelas enxutas (apontar para o portal, não duplicar tudo).
- Nenhuma mudança de código no repo; `ro.json`/minuta intocados.

## Aceite

- Índice + fontes + 27 notas de órgão criadas; decisões onde houver divergência real;
  0 wikilinks quebrados; amostragem verbatim das decisões confere com o JSON; ligações
  cruzadas RI↔Regulamento presentes; Diário e pendências atualizados.
