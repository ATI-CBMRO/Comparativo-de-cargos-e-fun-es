# Tabela de Cobertura do Acervo Legal — Design

**Data:** 2026-07-09
**Autor:** brainstorming com o Wândrio (dono do projeto)
**Branch:** `feat/auditoria-seguranca-e-comparador-regulamento`

## Objetivo

Adicionar, no topo da página **Acervo Legal** (`src/pages/Legislations.jsx`), uma
tabela-resumo que mostra, de relance, quais dos 27 estados possuem cada um dos três
tipos de documento-fonte que interessam à elaboração das minutas do CBMRO — e, para
cada documento, se o tipo foi **conferido por leitura de conteúdo** ou apenas
**classificado pelo nome do arquivo**.

## Motivação

Durante a curadoria, o Wândrio percebeu que havia confusão real entre "Regimento
Interno" e "Regulamento de Serviços Gerais" — inclusive porque as próprias instituições
fonte nomeiam esses documentos de forma inconsistente. A camada de dados já foi
corrigida (campo `typeVerified` por documento, curadoria de 9 estados pelo Fable), e a
lista detalhada já mostra um selo por documento. Falta uma **visão panorâmica**: uma
grade estado × tipo que torne visível, num único olhar, onde estão as lacunas de
cobertura e onde a classificação ainda é frágil (só por nome de arquivo).

## Decisões tomadas no brainstorming

1. **Convivência, não substituição.** A tabela entra como um bloco novo no **topo** da
   página Acervo Legal. A lista detalhada atual (com busca, selos por documento e link
   para PDF) **permanece intacta abaixo dela**. Nada da lista atual é removido.

2. **Três colunas de tipo, mais a coluna do estado.** Colunas:
   `Estado | LOB | Regimento Interno | Regulamento de Serviço`.
   - **LOB** = documentos com `type === 'Lei de Organização Básica'`.
   - **Regimento Interno** = documentos com `type === 'Regimento Interno'`.
   - **Regulamento de Serviço** = documentos com `type ∈ {'Regulamento Geral',
     'Regimento de Serviços'}` (as duas categorias reais dos dados são fundidas sob
     este único rótulo, conforme decisão do Wândrio).

3. **Célula vazia → travessão discreto "—".** Quando o estado não tem documento daquele
   tipo, a célula mostra um "—" apagado (cor `--text-muted`), deixando a lacuna de
   cobertura visível de relance.

4. **Célula preenchida → selo de verificação.** Reaproveita a mesma semântica do selo já
   existente na lista detalhada:
   - `✓` verde (`--success-text`) quando **todos** os documentos daquele tipo naquele
     estado têm `typeVerified === true`.
   - `⚠` cinza/atenção quando **algum** documento daquele tipo ainda é `typeVerified`
     falso (classificado só por nome de arquivo).
   - **Exceção da LOB:** na lista atual, a LOB nunca exibe selo (é sempre tratada como
     certa). Para manter coerência, a **coluna LOB da tabela mostra apenas presença**
     (um marcador de "possui", sem o par ✓/⚠). As colunas Regimento Interno e
     Regulamento de Serviço mostram o selo ✓/⚠.

5. **Múltiplos documentos do mesmo tipo → contador "+N".** Quando o estado tem mais de
   um documento do mesmo tipo (ex.: Sergipe tem 2 LOBs), a célula mostra um único selo
   e um sufixo pequeno "+2" (total de documentos daquele tipo). O detalhe fica na página
   do estado.

6. **Clique na célula preenchida → página do estado.** Navega para `/estados/:id`
   (mesma navegação já usada na lista atual), que lista todos os documentos daquele
   estado com contexto completo. Não linka para PDF direto (alguns documentos não têm
   PDF, ex.: Espírito Santo, cuja fonte é HTML).

7. **Mobile → rolagem horizontal.** A tabela mantém o formato de tabela real; num
   contêiner com `overflow-x: auto`, desliza para os lados no celular. Mesmo padrão já
   usado em outras telas do sistema.

8. **Documentos fora das 3 colunas ficam de fora da tabela.** Os 5 documentos que não
   são LOB / Regimento Interno / Regulamento de Serviço (Normas Gerais de Ação, Quadro
   Demonstrativo de Cargos, Quadro de Organização e Distribuição) **não aparecem na
   tabela** — ela é estritamente sobre as 3 colunas pedidas. Esses documentos continuam
   normalmente na lista detalhada abaixo, como hoje.

## Dados de referência (verificados em 2026-07-09)

Sobre os 27 estados de `database/states_data.json`:
- **LOB:** todos os 27 têm (6 têm 2 documentos de LOB: AC, CE, PE, PI, SE, SP).
- **Regimento Interno:** 5 estados — AL, DF, PR, PA, RS.
- **Regulamento de Serviço:** 4 estados — GO, MT, RN, SE
  (RN e MT como `Regulamento Geral`; GO e SE como `Regimento de Serviços`).

## Arquitetura

### Camada de dados pura (nova, testável)

**Novo arquivo: `src/lib/acervoCoverage.js`**

Função pura `buildCoverageRows(states)` que recebe o array `data.states` e devolve uma
linha por estado, já resolvida para as 3 colunas. Interface:

```js
// Entrada: data.states (array de estados do states_data.json)
// Saída: array de linhas, uma por estado, ordenadas por nome (pt-BR)
buildCoverageRows(states) => [
  {
    stateId: 'se',
    stateName: 'Sergipe',
    abbreviation: 'SE',
    columns: {
      lob:        { count: 2, present: true,  verified: null },  // LOB: verified sempre null (sem selo)
      regimento:  { count: 0, present: false, verified: null },  // ausente
      regulamento:{ count: 1, present: true,  verified: true },  // presente e conferido
    },
  },
  // ...
]
```

Regra de `verified` por coluna (para Regimento Interno e Regulamento de Serviço):
- `null` quando a coluna é LOB (não exibe selo) OU quando `present === false`.
- `true` quando `present` e **todos** os documentos daquele tipo têm `typeVerified === true`.
- `false` quando `present` e **algum** documento daquele tipo tem `typeVerified` falso/ausente.

Constante de fusão exportada do módulo:
```js
export const REGULAMENTO_SERVICO_TYPES = ['Regulamento Geral', 'Regimento de Serviços']
```

**Novo arquivo: `src/lib/acervoCoverage.test.js`** (node --test), cobrindo:
- estado com 2 LOBs → `columns.lob.count === 2`, `present === true`, `verified === null`.
- estado sem Regimento Interno → `regimento.present === false`, `verified === null`.
- estado com Regulamento de Serviço todo verificado → `verified === true`.
- estado com um documento do tipo `typeVerified` falso → `verified === false`.
- fusão: um estado com `Regimento de Serviços` e outro com `Regulamento Geral` caem
  ambos na coluna `regulamento`.
- ordenação alfabética por `stateName` (pt-BR).

### Camada de apresentação (componente novo)

**Novo arquivo: `src/components/AcervoCoverageTable.jsx`**

Componente de apresentação puro: recebe `rows` (saída de `buildCoverageRows`) e um
`onSelectState(stateId)`. Renderiza:
- `<div className="acervo-cov-wrap">` com `overflow-x: auto` (rolagem mobile).
- `<table className="acervo-cov-table">` com cabeçalho fixo das 4 colunas.
- Célula de estado: sigla + nome (botão, navega ao clicar).
- Células de tipo: travessão "—" quando ausente; selo ✓/⚠ + "+N" quando presente;
  clicáveis quando presentes (mesma navegação da célula de estado).
- Legenda curta abaixo da tabela explicando ✓ (conferido por conteúdo) × ⚠ (só por
  nome de arquivo) × — (não possui).

Não busca dados nem conhece rotas diretamente — recebe tudo por props (testável e
isolado). O contêiner (`Legislations.jsx`) injeta `navigate`.

### Integração

**Editar `src/pages/Legislations.jsx`:**
- Importar `buildCoverageRows` e `<AcervoCoverageTable>`.
- Calcular `rows` com `useMemo` a partir de `data.states` (sem tocar no `allDocs`
  existente).
- Renderizar `<AcervoCoverageTable rows={rows} onSelectState={id => navigate('/estados/'+id)} />`
  **acima** da busca e da lista atual, dentro de `page-body`, com um pequeno título de
  seção ("Cobertura por estado").
- A tabela mostra sempre os 27 estados; **não** é filtrada pela busca de texto (a busca
  continua governando só a lista detalhada abaixo). Isso mantém a tabela como panorama
  estável e evita a ambiguidade de "a busca esconde linhas da tabela".

### CSS

Adicionar em `src/index.css` um pequeno bloco `.acervo-cov-*` (contêiner com
`overflow-x`, tabela com `border-collapse`, cabeçalho, células, selos, legenda),
reutilizando as variáveis de cor existentes (`--success-text`, `--text-muted`,
`--border-card`, `--bg-surface`). Sem cores hardcoded novas.

## Tratamento de erro e estados de carregamento

Nenhum novo. A página já trata loading (spinner) e erro (mensagem) via o `fetchJson`
existente; a tabela só renderiza quando `data` já chegou, junto com o resto da página.
Se `data.states` vier vazio (situação que já quebraria a página inteira hoje), a tabela
simplesmente não renderiza linhas.

## Testes

- **`src/lib/acervoCoverage.test.js`** (node --test) — cobre a lógica pura descrita
  acima. Entra no `npm test` existente (glob `src/lib/`).
- **Verificação visual** (manual, no preview local, após implementar): tabela aparece no
  topo; 27 linhas; AL/DF/PR/PA/RS com selo na coluna Regimento Interno; GO/MT/RN/SE com
  selo na coluna Regulamento de Serviço; SE com "+2" na LOB; clique numa célula abre a
  página do estado; rolagem horizontal no viewport mobile.

## Fora de escopo (YAGNI)

- Auditoria de conteúdo dos 18 estados ainda não verificados (decisão do Wândrio: a
  tabela sai já com o selo ⚠, sem bloquear).
- Ordenação/filtro interativo da tabela (ordena alfabético fixo).
- Exportação da tabela (PDF/CSV).
- Qualquer alteração na lista detalhada existente ou no schema de dados.
