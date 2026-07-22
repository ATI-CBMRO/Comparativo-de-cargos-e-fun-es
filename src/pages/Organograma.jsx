// Página "Organograma" (parte Geral): estrutura organizacional do CBMRO em 7
// visualizações. Porte fiel do protótipo validado com a comissão. Os dados de
// classificação por natureza e a projeção territorial são curados aqui (a LOB não
// nomeia as unidades municipais); ficam neste arquivo para edição posterior.
import { useState } from 'react'
import { useScenario } from '../context/ScenarioContext'

/* ---------------- DADOS: órgãos do Comando-Geral (natureza inferida, ajustável) ---------------- */
const ORGAOS = [
  { sig: 'GAB/CG', nome: 'Gabinete do Comandante-Geral', nat: 'direcao',
    subs: ['Chefia de Gabinete', 'Secretaria', 'Assessorias', 'Ajudância de Ordens'] },
  { sig: 'CONDEG', nome: 'Conselho Deliberativo de Estratégia e Gestão', nat: 'direcao', adv: true,
    subs: ['Presidido pelo Comandante-Geral', 'Coronéis BM da ativa'] },
  { sig: 'AG', nome: 'Ajudância-Geral', nat: 'direcao',
    subs: ['Ajudante-Geral', 'Adjunto', 'Secretaria-Geral', 'Cia de Comando e Serviços'] },
  { sig: 'CORREG', nome: 'Corregedoria-Geral', nat: 'direcao',
    subs: ['Corregedor-Geral', 'Adjunto', 'Cartório', 'Núcleo de Inteligência', 'Seção de Processo Administrativo'] },
  { sig: 'ASSESS.', nome: 'Assessorias', nat: 'direcao', adv: true,
    subs: ['Institucional', 'Especial', 'Legislativa', 'Parlamentar', 'Projetos e Gestão Estratégica', 'Fundacional', 'Controle Interno'] },
  { sig: 'CINT', nome: 'Coordenadoria de Inteligência', nat: 'direcao',
    subs: ['Inteligência', 'Contra-Inteligência', 'Operações de Inteligência', 'Controle de Armamento'] },
  { sig: 'CCS', nome: 'Coordenadoria de Comunicação Social', nat: 'direcao',
    subs: ['Imprensa', 'Relações Públicas', 'Comunicação Institucional'] },

  { sig: 'DP', nome: 'Diretoria de Pessoal', nat: 'apoio',
    subs: ['Gestão de Pessoal Ativo', 'Inativo e Pensionistas', 'Legislação, Controle e Análise de Processos'] },
  { sig: 'DEEI', nome: 'Diretoria de Educação, Ensino e Instrução', nat: 'apoio',
    subs: ['Coordenadoria de Educação', 'Ensino, Instrução e Pesquisa'] },
  { sig: 'DPOF', nome: 'Diretoria de Planejamento, Orçamento e Finanças', nat: 'apoio',
    subs: ['Planejamento e Orçamento', 'Administração e Finanças', 'Compras', 'Comissão Permanente de Licitações'] },
  { sig: 'DSAP', nome: 'Diretoria de Saúde e Assistência ao Pessoal', nat: 'apoio',
    subs: ['Coordenadoria de Saúde', 'Assistência ao Pessoal', 'Saúde Ocupacional', 'Centro Médico-Hospitalar'] },
  { sig: 'DLOG', nome: 'Diretoria de Logística', nat: 'apoio',
    subs: ['Controle de Material e Patrimônio', 'Suprimento e Material', 'Manutenção'] },
  { sig: 'CINF', nome: 'Coordenadoria de Informática', nat: 'apoio',
    subs: ['Projetos e Desenvolvimento', 'Suporte', 'Redes'] },

  { sig: 'DEPDEC', nome: 'Diretoria Estadual de Proteção e Defesa Civil', nat: 'exec',
    subs: ['Operações Emergenciais', 'Minimização de Desastres', 'Apoio Administrativo e Financeiro'] },
  { sig: 'DPO', nome: 'Diretoria de Planejamento Operacional', nat: 'exec',
    subs: ['COT — Comando de Operações Técnicas', 'CRBM — Comandos Regionais', 'BBM · CIBM · GBM (unidades territoriais)'] },
  { sig: 'DOE', nome: 'Diretoria Operacional Especializada', nat: 'exec',
    subs: ['BBS — Busca e Salvamento', 'BIFEA — Incêndio Florestal e Emerg. Ambientais', 'BOA — Operações Aéreas'] },
]

/* Cadeia operacional detalhada (árvore interativa e ramo operacional do unificado) */
const TREE = {
  sig: 'CG', nome: 'Comando-Geral', nat: 'comando', kids: [
    { sig: 'GAB/CG', nome: 'Gabinete do Comandante-Geral', nat: 'direcao' },
    { sig: 'CONDEG', nome: 'Conselho Deliberativo de Estratégia e Gestão', nat: 'direcao' },
    { sig: 'AG', nome: 'Ajudância-Geral', nat: 'direcao' },
    { sig: 'CORREG', nome: 'Corregedoria-Geral', nat: 'direcao' },
    { sig: 'ASSESS.', nome: 'Assessorias', nat: 'direcao' },
    { sig: 'CINT', nome: 'Coordenadoria de Inteligência', nat: 'direcao' },
    { sig: 'CCS', nome: 'Coordenadoria de Comunicação Social', nat: 'direcao' },
    { sig: 'DP', nome: 'Diretoria de Pessoal', nat: 'apoio' },
    { sig: 'DEEI', nome: 'Diretoria de Educação, Ensino e Instrução', nat: 'apoio' },
    { sig: 'DPOF', nome: 'Diretoria de Planejamento, Orçamento e Finanças', nat: 'apoio' },
    { sig: 'DSAP', nome: 'Diretoria de Saúde e Assistência ao Pessoal', nat: 'apoio' },
    { sig: 'DLOG', nome: 'Diretoria de Logística', nat: 'apoio' },
    { sig: 'CINF', nome: 'Coordenadoria de Informática', nat: 'apoio' },
    { sig: 'DEPDEC', nome: 'Diretoria Estadual de Proteção e Defesa Civil', nat: 'exec' },
    { sig: 'DPO', nome: 'Diretoria de Planejamento Operacional', nat: 'exec', kids: [
      { sig: 'COT', nome: 'Comando de Operações Técnicas', nat: 'exec', kids: [
        { sig: 'CAT', nome: 'Coordenadoria de Atividades Técnicas', nat: 'exec' }] },
      { sig: 'CRBM', nome: 'Comandos Regionais de Bombeiro Militar', nat: 'exec', kids: [
        { sig: 'BBM', nome: 'Batalhão de Bombeiros Militar', nat: 'exec', kids: [
          { sig: 'Cia BM', nome: 'Companhia de Bombeiros Militar', nat: 'exec', kids: [
            { sig: 'Pel BM', nome: 'Pelotão de Bombeiros Militar', nat: 'exec', kids: [
              { sig: 'GuSv', nome: 'Guarnição de Serviço Operacional', nat: 'exec' }] }] }] },
        { sig: 'CIBM', nome: 'Companhia Independente de Bombeiros Militar', nat: 'exec' },
        { sig: 'GBM', nome: 'Grupo de Bombeiros Militar', nat: 'exec' }] }] },
    { sig: 'DOE', nome: 'Diretoria Operacional Especializada', nat: 'exec', kids: [
      { sig: 'BBS', nome: 'Batalhão de Busca e Salvamento', nat: 'exec' },
      { sig: 'BIFEA', nome: 'Batalhão de Incêndio Florestal e Emergências Ambientais', nat: 'exec' },
      { sig: 'BOA', nome: 'Batalhão de Operações Aéreas', nat: 'exec' }] },
  ],
}

const NATS = ['comando', 'direcao', 'apoio', 'exec']
const NAT_LABEL = { comando: 'Comando-Geral', direcao: 'Direção & Assessoramento', apoio: 'Apoio', exec: 'Execução' }
const NAT_ICON = { direcao: '◆', apoio: '▲', exec: '●' }
const SUB_TREE = { DPO: TREE.kids.find(k => k.sig === 'DPO'), DOE: TREE.kids.find(k => k.sig === 'DOE') }
const byNat = n => ORGAOS.filter(o => o.nat === n)

/* Projeção territorial (nova LOB × unidades municipais reais) */
const OPTREE = { sig: 'DPO', nome: 'Diretoria de Planejamento Operacional', nat: 'exec', badge: 'lob', children: [
  { sig: 'CRBM', nome: 'Comando Regional — Área I', nat: 'exec', badge: 'lob', was: 'COB I', children: [
    { sig: 'BBM', nome: 'Porto Velho', nat: 'exec', badge: 'lob', was: '1º GBM', stack: ['Porto Velho', 'Guajará-Mirim', 'Candeias do Jamari'] },
    { sig: 'BBM', nome: 'Ji-Paraná', nat: 'exec', badge: 'lob', was: '2º GBM', stack: ['Ji-Paraná', 'Ouro Preto do Oeste', 'Jaru'] },
    { sig: 'BBM', nome: 'Ariquemes', nat: 'exec', badge: 'lob', was: '5º GBM', stack: ['Ariquemes', 'Machadinho D’Oeste', 'Buritis'] },
  ] },
  { sig: 'CRBM', nome: 'Comando Regional — Área II', nat: 'exec', badge: 'lob', was: 'COB II', children: [
    { sig: 'BBM', nome: 'Rolim de Moura', nat: 'exec', badge: 'lob', was: '6º GBM', stack: ['Rolim de Moura', 'São Miguel do Guaporé', 'Espigão D’Oeste'] },
    { sig: 'BBM', nome: 'Cacoal', nat: 'exec', badge: 'lob', was: '4º GBM', stack: ['Cacoal', 'Pimenta Bueno'] },
    { sig: 'BBM', nome: 'Vilhena', nat: 'exec', badge: 'lob', was: '3º GBM', stack: ['Vilhena', 'Cerejeiras', 'Colorado do Oeste'] },
  ] },
] }
const TECTREE = { sig: 'COT', nome: 'Comando de Operações Técnicas', nat: 'apoio', badge: 'lob', children: [
  { sig: 'CAT', nome: 'Coordenadoria de Atividades Técnicas', nat: 'apoio', badge: 'lob', children: [
    { sig: 'DAT', nome: 'Porto Velho', nat: 'apoio', badge: 'lob', stack: ['Porto Velho', 'Candeias do Jamari', 'Guajará-Mirim'] },
    { sig: 'DAT', nome: 'Ariquemes', nat: 'apoio', badge: 'lob', stack: ['Ariquemes', 'Machadinho D’Oeste', 'Buritis'] },
    { sig: 'DAT', nome: 'Ji-Paraná', nat: 'apoio', badge: 'lob', stack: ['Ji-Paraná', 'Ouro Preto do Oeste', 'Jaru'] },
    { sig: 'DAT', nome: 'Cacoal', nat: 'apoio', badge: 'lob', stack: ['Cacoal', 'Pimenta Bueno', 'Espigão D’Oeste'] },
    { sig: 'DAT', nome: 'Rolim de Moura', nat: 'apoio', badge: 'lob', stack: ['Rolim de Moura', 'São Miguel do Guaporé'] },
    { sig: 'DAT', nome: 'Vilhena', nat: 'apoio', badge: 'lob', stack: ['Vilhena', 'Colorado do Oeste', 'Cerejeiras'] },
  ] },
] }
const ESPTREE = { sig: 'DOE', nome: 'Diretoria Operacional Especializada', nat: 'exec', badge: 'lob', children: [
  { sig: 'BBS', nome: 'Batalhão de Busca e Salvamento', nat: 'exec', badge: 'lob', was: 'Grpto de Busca e Salvamento' },
  { sig: 'BOA', nome: 'Batalhão de Operações Aéreas', nat: 'exec', badge: 'lob', was: 'Cmdo/Grpto de Operações Aéreas' },
  { sig: 'BIFEA', nome: 'Incêndio Florestal e Emerg. Ambientais', nat: 'exec', badge: 'nova', was: 'nova unidade' },
] }

/* ---------------- componentes de apoio ---------------- */
function Box({ o, big }) {
  return (
    <div className={`orgv-box ${o.nat}${big ? ' big' : ''}`}>
      <span className="sig">{o.sig}</span>
      <span className="nm">{o.nome}</span>
    </div>
  )
}

// Nó com estado próprio de expandir/recolher (usado no unificado).
function MiniNode({ node }) {
  const kids = node.kids || []
  const has = kids.length > 0
  const [open, setOpen] = useState(true)
  const cls = NATS.includes(node.nat) ? node.nat : 'int'
  return (
    <div className={`tnode${has && !open ? ' closed' : ''}`}>
      <div className="trow" onClick={has ? () => setOpen(o => !o) : undefined}>
        <span className="tw">{has ? '▾' : '·'}</span>
        <span className={`tsig ${cls}`}>{node.sig}</span>
        <span className="tnm">{node.nome}</span>
      </div>
      {has && <div className="kids">{kids.map((k, i) => <MiniNode key={i} node={k} />)}</div>}
    </div>
  )
}

// Nó da árvore interativa (P4): respeita expandir/recolher tudo via remontagem.
function P4Node({ node, depth, mode }) {
  const kids = node.kids || []
  const has = kids.length > 0
  const [open, setOpen] = useState(mode === 'col' ? depth === 0 : true)
  const cls = NATS.includes(node.nat) ? node.nat : 'int'
  return (
    <div className={`tnode${has && !open ? ' closed' : ''}`}>
      <div className="trow" onClick={has ? () => setOpen(o => !o) : undefined}>
        <span className="tw">{has ? '▾' : '·'}</span>
        <span className={`tsig ${cls}`}>{node.sig}</span>
        <span className="tnm">{node.nome}</span>
      </div>
      {has && <div className="kids">{kids.map((k, i) => <P4Node key={i} node={k} depth={depth + 1} mode={mode} />)}</div>}
    </div>
  )
}

// Item do unificado (P6): abre subunidades / cadeia operacional.
function UnifItem({ o }) {
  const [open, setOpen] = useState(false)
  const deep = SUB_TREE[o.sig]
  return (
    <div className={`u6-item ${o.nat}${o.adv ? ' adv' : ''}${open ? ' open' : ''}`}>
      <div className="u6-org" onClick={() => setOpen(v => !v)}>
        <div className="u6-head">
          <span className="u6-sig">{o.sig}{o.adv && <span className="u6-tag">assessoria</span>}</span>
          <span className="u6-caret">+</span>
        </div>
        <div className="u6-nm">{o.nome}</div>
      </div>
      <div className="u6-subs">
        {deep ? (
          <><div className="u-oplabel">Cadeia de comando</div><MiniNode node={deep} /></>
        ) : o.subs.map((s, i) => <div key={i} className="u6-subchip">{s}</div>)}
      </div>
    </div>
  )
}

// Nó da árvore top-down da projeção territorial (P7).
function OtNode({ n }) {
  const pill = n.badge === 'nova'
    ? <span className="pill nova">nova</span>
    : n.badge === 'lob' ? <span className="pill lob">LOB</span> : null
  const tag = n.sig === 'DAT' ? 'Seção AT' : 'Cia/Pel'
  return (
    <li>
      <div className={`obox ${n.nat}`}>
        <div className="ob-top"><span className="ob-sig">{n.sig}</span>{pill}</div>
        <div className="ob-nm">{n.nome}</div>
        {n.was && <div className="was">{n.was}</div>}
      </div>
      {n.stack && n.stack.length > 0 && (
        <div className="ostack">
          {n.stack.map((c, i) => (
            <div key={i} className="ost-item">{c}<span className="pill terr">{tag}</span></div>
          ))}
        </div>
      )}
      {n.children && n.children.length > 0 && (
        <ul>{n.children.map((c, i) => <OtNode key={i} n={c} />)}</ul>
      )}
    </li>
  )
}
const OtTree = ({ root }) => <div className="tree"><ul><OtNode n={root} /></ul></div>

/* ---------------- as 7 visualizações ---------------- */
function P1() {
  const order = [['direcao', 'Órgãos de direção & assessoramento'], ['apoio', 'Órgãos de apoio (atividade-meio)'], ['exec', 'Órgãos de execução (atividade-fim)']]
  return (
    <div className="p1">
      <div className="top-org"><Box o={{ sig: 'CG', nome: 'Comando-Geral', nat: 'comando' }} big /></div>
      <div className="vbar" /><div className="connector" />
      {order.map(([nat, label]) => (
        <div key={nat} style={{ width: '100%' }}>
          <div className="row-label">{label}</div>
          <div className="grid-orgs">
            {byNat(nat).map((o, i) => (
              <div key={i} className="col-org">
                <Box o={o} />
                <div className="subs">
                  {o.subs.slice(0, 3).map((s, j) => <span key={j} className="sub-chip">{s}</span>)}
                  {o.subs.length > 3 && <span className="sub-chip">+{o.subs.length - 3} un.</span>}
                </div>
              </div>
            ))}
          </div>
        </div>
      ))}
    </div>
  )
}

function P2() {
  return (
    <div className="p2">
      <div className="lane comando"><div className="lane-rail">Comando</div>
        <div className="lane-body"><Box o={{ sig: 'CG', nome: 'Comando-Geral', nat: 'comando' }} big /></div></div>
      {['direcao', 'apoio', 'exec'].map(nat => (
        <div key={nat} className={`lane ${nat}`}>
          <div className="lane-rail">{NAT_LABEL[nat]}</div>
          <div className="lane-body">{byNat(nat).map((o, i) => <Box key={i} o={o} />)}</div>
        </div>
      ))}
    </div>
  )
}

function P3() {
  const cols = [['comando', [{ sig: 'CG', nome: 'Comando-Geral', subs: ['Direção superior do CBMRO'] }]],
    ['direcao', byNat('direcao')], ['apoio', byNat('apoio')], ['exec', byNat('exec')]]
  return (
    <div className="p3">
      {cols.map(([nat, list]) => (
        <div key={nat} className={`catcol ${nat}`}>
          <div className="catcol-h"><span>{NAT_LABEL[nat]}</span><span>{list.length}</span></div>
          <div className="catcol-b">
            {list.map((o, i) => (
              <div key={i} className="ocard">
                <div className="sig">{o.sig}</div>
                <div className="nm">{o.nome}</div>
                {o.subs && <div className="cnt">{o.subs.length} subunidade{o.subs.length > 1 ? 's' : ''}</div>}
              </div>
            ))}
          </div>
        </div>
      ))}
    </div>
  )
}

function P4() {
  const [mode, setMode] = useState('def')
  const [k, setK] = useState(0)
  const set = m => { setMode(m); setK(x => x + 1) }
  return (
    <>
      <div className="p4-tools">
        <button type="button" onClick={() => set('exp')}>Expandir tudo</button>
        <button type="button" onClick={() => set('col')}>Recolher tudo</button>
      </div>
      <div className="p4"><P4Node key={k} node={TREE} depth={0} mode={mode} /></div>
    </>
  )
}

function P5() {
  let i = 0
  return (
    <div className="p5">
      <div className="bp-head"><div className="bp-cg">CG · COMANDO-GERAL DO CBMRO</div></div>
      <div className="bp-grid">
        {['direcao', 'apoio', 'exec'].flatMap(nat => byNat(nat).map(o => {
          i++
          const badge = nat === 'exec' ? 'Exec' : nat === 'apoio' ? 'Apoio' : 'Direção'
          return (
            <div key={o.sig} className={`bp-cell ${nat}`}>
              <div className="k">
                <span className="idx">{String(i).padStart(2, '0')}</span>
                <span className="sig">{o.sig}</span>
                <span className="badge">{badge}</span>
              </div>
              <div className="nm">{o.nome}</div>
              <ul>
                {o.subs.slice(0, 4).map((s, j) => <li key={j}>{s}</li>)}
                {o.subs.length > 4 && <li>+{o.subs.length - 4} subunidades</li>}
              </ul>
            </div>
          )
        }))}
      </div>
    </div>
  )
}

function P6() {
  const order = [['direcao', 'Direção & Assessoramento'], ['apoio', 'Apoio — atividade-meio'], ['exec', 'Execução — atividade-fim']]
  return (
    <div className="p6">
      <div className="u6-top"><Box o={{ sig: 'CG', nome: 'Comando-Geral do CBMRO', nat: 'comando' }} big /></div>
      <div className="u6-groups">
        {order.map(([nat, label]) => (
          <div key={nat} className="u6-col">
            <div className={`u6-grouphead ${nat}`}><span className="gh-ic" aria-hidden="true">{NAT_ICON[nat]}</span>{label}</div>
            <div className="u6-list">{byNat(nat).map((o, i) => <UnifItem key={i} o={o} />)}</div>
          </div>
        ))}
      </div>
      <div className="u6-legend">
        <span><span className="ll-solid" /> Linha sólida — subordinação direta</span>
        <span><span className="ll-dash" /> Linha tracejada — órgão de assessoria / consultivo</span>
      </div>
    </div>
  )
}

function P7() {
  return (
    <div className="p7">
      <div className="p7-intro">
        <b>Por que esta aba existe.</b> A nova LOB define a estrutura por <b>tipos de unidade</b> (Comando
        Regional, Batalhão, Companhia, Pelotão, Guarnição, além de BBS/BIFEA/BOA). Ela <b>não nomeia</b> as
        unidades instaladas nos municípios — essas vêm do desdobramento atual e são criadas por ato próprio.
        Abaixo, as <b>17 cidades onde o CBMRO já atua</b> projetadas na nova nomenclatura, com as
        <b> linhas de subordinação</b> no padrão do organograma oficial. Note o duplo agrupamento:
        <b> operacional</b> (Comandos/GBM) e <b>administrativo-técnico</b> (Atividades Técnicas) agrupam as
        cidades de formas diferentes. <i>Mapeamento é proposta, a validar com a redação final.</i>
      </div>
      <div className="p7-legend">
        <span><span className="pill lob">Tipo previsto na LOB</span></span>
        <span><span className="pill terr">Unidade municipal — não nominada na LOB</span></span>
        <span><span className="pill nova">Nova unidade criada pela LOB</span></span>
      </div>
      <div className="p7-sec">
        <div className="p7-sechead exec"><span>① Execução operacional</span><code>DPO → CRBM → BBM → Cia/Pel BM → Guarnição</code></div>
        <div className="p7-scroll"><OtTree root={OPTREE} /></div>
      </div>
      <div className="p7-sec">
        <div className="p7-sechead apoio"><span>② Atividades técnicas (prevenção / vistorias)</span><code>DPO → COT → CAT → Seções de Atividades Técnicas</code></div>
        <div className="p7-scroll"><OtTree root={TECTREE} /></div>
      </div>
      <div className="p7-sec">
        <div className="p7-sechead exec"><span>③ Execução especializada</span><code>DOE → BBS · BIFEA · BOA</code></div>
        <div className="p7-scroll"><OtTree root={ESPTREE} /></div>
      </div>
    </div>
  )
}

const VIEWS = [
  { n: 'Institucional clássico', d: 'Árvore hierárquica de cima para baixo com linhas conectoras e caixas coloridas por natureza — o formato mais próximo dos organogramas oficiais em papel. Ideal para imprimir e levar à reunião.', C: P1 },
  { n: 'Faixas por natureza', d: 'Cada natureza vira uma faixa horizontal com etiqueta lateral. Deixa a leitura por tipo de órgão imediata e economiza altura.', C: P2 },
  { n: 'Cartões modernos', d: 'Quatro colunas (Comando · Direção · Apoio · Execução), cada órgão num cartão com contagem de subunidades. Visual limpo de painel.', C: P3 },
  { n: 'Árvore interativa', d: 'Estrutura completa e navegável — inclusive a cadeia operacional (DPO → CRBM → BBM → Companhia → Pelotão → Guarnição). Expande/recolhe cada ramo.', C: P4 },
  { n: 'Blueprint / matriz', d: 'Grade editorial monocromática com numeração e etiquetas discretas — foco no conteúdo e nas subunidades de cada órgão. Sóbrio para documentos formais.', C: P5 },
  { n: 'Unificado (definitivo)', d: 'Árvore de subordinação: o Comando-Geral no topo, um barramento descendo às três naturezas e cada diretoria pendurada por uma linha conectora. Clique numa diretoria para ver as subunidades; nos operacionais abre a cadeia completa até a Guarnição.', C: P6 },
  { n: 'Projeção territorial · nova LOB', d: 'Projeta as unidades REAIS do CBMRO — as 17 cidades onde já há bombeiro, que a LOB não nomeia — dentro da nova nomenclatura, com linhas de subordinação no padrão oficial. Distingue tipo previsto na LOB, unidade municipal a manter, e unidade nova (ex.: BIFEA). Mapeamento é proposta a validar.', C: P7 },
]

export default function Organograma() {
  const [view, setView] = useState(0)
  const { cenario } = useScenario()
  const Current = VIEWS[view].C
  if (cenario === 'atual') {
    return (
      <>
        <div className="page-header">
          <div className="page-header-left">
            <h2 className="page-title">Organograma</h2>
            <p className="page-subtitle">Estrutura organizacional vigente do CBMRO (Lei nº 2.204/2009) — organograma oficial.</p>
          </div>
        </div>
        <div className="page-body">
          <div className="orgv">
            <div className="toptabs">
              <button type="button" className="toptab active">Organograma oficial (vigente)</button>
              <a className="toptab" href="/organograma-oficial-cbmro.pdf" target="_blank" rel="noreferrer">Abrir PDF</a>
            </div>
            <p className="proto-desc">
              Organograma oficial da estrutura vigente, com a classificação em Órgãos de
              Direção, de Apoio e de Execução (Art. 8º da Lei nº 2.204/2009, redação da Lei
              nº 4.303/2018). Clique na imagem para ampliar.
            </p>
            <div className="stage" style={{ overflow: 'auto' }}>
              <a href="/organograma-oficial-cbmro.png" target="_blank" rel="noreferrer">
                <img
                  src="/organograma-oficial-cbmro.png"
                  alt="Organograma oficial do CBMRO — estrutura vigente (Lei nº 2.204/2009)"
                  style={{ width: '100%', maxWidth: 900, display: 'block', margin: '0 auto' }}
                />
              </a>
            </div>
          </div>
        </div>
      </>
    )
  }
  return (
    <>
      <div className="page-header">
        <div className="page-header-left">
          <h2 className="page-title">Organograma</h2>
          <p className="page-subtitle">Estrutura organizacional do CBMRO — 7 visualizações da mesma estrutura.</p>
        </div>
      </div>
      <div className="page-body">
        <div className="orgv">
          <div className="toptabs"><button type="button" className="toptab active">Organograma</button></div>
          <div className="sub-hint">Escolha a visualização:</div>
          <div className="protos">
            {VIEWS.map((v, i) => (
              <button key={i} type="button" className={`proto-btn${i === view ? ' active' : ''}`} onClick={() => setView(i)}>
                <span className="n">{i + 1}</span>{v.n}
              </button>
            ))}
          </div>
          <div className="proto-name">Visualização {view + 1} — {VIEWS[view].n}</div>
          <p className="proto-desc">{VIEWS[view].d}</p>
          <div className="legend">
            <span className="lg"><span className="dot comando" /> Comando-Geral</span>
            <span className="lg"><span className="dot direcao" /> Direção &amp; Assessoramento</span>
            <span className="lg"><span className="dot apoio" /> Apoio (atividade-meio)</span>
            <span className="lg"><span className="dot exec" /> Execução (atividade-fim)</span>
          </div>
          <div className="stage"><Current /></div>
        </div>
      </div>
    </>
  )
}
