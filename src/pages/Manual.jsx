// Manual de uso do portal, dentro do próprio sistema (parte Geral do menu).
// Texto-guia por tela; como o usuário está no sistema, não repete prints.
const SECTIONS = [
  {
    id: 'visao', title: 'Visão geral',
    body: (
      <>
        <p>
          O <b>Portal de Legislação do CBMRO</b> é onde o Corpo de Bombeiros elabora, com método e
          embasamento, as suas duas normas internas: a <b>Minuta do Regimento Interno</b> e a
          <b> Minuta do Regulamento Geral</b>. A ideia central é reunir a legislação de Corpos de
          Bombeiros de todo o país e construir as nossas minutas <b>a partir desse comparativo</b>,
          de modo que cada dispositivo tenha origem rastreável.
        </p>
        <div className="manual-callout">
          <b>Como o menu é organizado.</b> A parte <b>Geral</b> reúne o que é comum (Acervo, Busca,
          Manual, Acessos). Abaixo, cada minuta tem a <b>mesma trilha</b>:
          <b> Subsídio → Minuta → Diagramas → Revisão</b>.
        </div>
      </>
    ),
  },
  {
    id: 'acesso', title: 'Acessar o sistema',
    body: (
      <>
        <p>Todas as páginas exigem login. O seu <b>papel</b> define o que você vê:</p>
        <ul>
          <li><b>Participante / comissão</b>: navega, consulta e comenta na Revisão.</li>
          <li><b>Administrador</b>: além disso, gerencia acessos e libera os comentários do Regulamento.</li>
        </ul>
        <p className="manual-tip">
          A barra lateral começa expandida. Use <b>“Recolher menu”</b> no rodapé dela (ou o ☰ no
          topo) para ganhar espaço — clicar num item do menu não recolhe a barra.
        </p>
      </>
    ),
  },
  {
    id: 'acervo', title: 'Acervo Legal',
    body: (
      <>
        <p>É o ponto de partida: todas as legislações levantadas, organizadas por estado.</p>
        <ul>
          <li>A tabela <b>Cobertura por estado</b> mostra, por Corpo de Bombeiros, se há <b>LOB</b>, <b>Regimento Interno</b> e <b>Regulamento de Serviço</b>.</li>
          <li>Clique no <b>nome de uma coluna</b> para filtrar só os estados que possuem aquele documento.</li>
          <li>Alterne as abas <b>Tabela</b>, <b>Por documento</b> e <b>Documentos por estado</b>.</li>
          <li>Clique em um <b>documento</b> para abrir o <b>PDF oficial</b> num popup.</li>
        </ul>
      </>
    ),
  },
  {
    id: 'subsidio', title: 'Subsídio',
    body: (
      <>
        <p>Onde comparamos a nossa minuta com a de outros estados, dispositivo por dispositivo.</p>
        <ul>
          <li>No topo, escolha <b>Navegar por: Organização</b> (capítulos) ou <b>Órgãos</b> (organograma) — as duas formas levam ao mesmo item.</li>
          <li>No centro fica <b>a nossa minuta</b>; à direita, o <b>estado</b> selecionado.</li>
          <li>O painel mostra o <b>texto original</b> do artigo quando existe (com os incisos) ou, na falta dele, um <b>resumo de competências</b> rotulado como “texto integral ainda não extraído”.</li>
          <li>A aba <b>LOB</b> compara pela Lei de Organização Básica. A seleção de <b>órgão e estado é compartilhada</b> entre as abas.</li>
        </ul>
      </>
    ),
  },
  {
    id: 'minuta', title: 'Minuta',
    body: (
      <>
        <p>O assistente onde a minuta é montada, curada e exportada.</p>
        <ul>
          <li><b>Visão geral</b>: veja a estrutura e as fontes.</li>
          <li><b>Revisão &amp; curadoria</b>: ajuste o texto item a item; cada trecho mostra a origem (próprio do RO ou “cf. CBM-XX”).</li>
          <li><b>Download</b>: gere o arquivo <b>.docx</b> para tramitação.</li>
        </ul>
      </>
    ),
  },
  {
    id: 'diagramas', title: 'Diagramas',
    body: (
      <>
        <p>Visão gráfica da estrutura da minuta.</p>
        <ul>
          <li>Alterne entre <b>Organograma</b> e <b>Mapa mental</b>.</li>
          <li>Use <b>Expandir tudo</b> / <b>Recolher tudo</b> para navegar a hierarquia.</li>
          <li><b>Imprimir / PDF</b> gera uma versão para levar à reunião.</li>
        </ul>
      </>
    ),
  },
  {
    id: 'revisao', title: 'Revisão',
    body: (
      <>
        <p>A etapa colaborativa: a comissão comenta e o texto final é fechado.</p>
        <ul>
          <li>Navegue pelos <b>capítulos</b>; o número ao lado indica quantas sugestões há.</li>
          <li>Clique no <b>balão</b> ao lado de um dispositivo para <b>comentar</b>. As sugestões de todos ficam visíveis.</li>
          <li>O administrador <b>consolida</b> e <b>fecha o texto final</b> de cada dispositivo.</li>
        </ul>
        <div className="manual-callout">
          <b>Regulamento.</b> Os comentários do Regulamento só abrem quando o administrador libera
          (interruptor de segurança). Antes disso, a comissão vê “em preparação”.
        </div>
      </>
    ),
  },
  {
    id: 'faq', title: 'Perguntas rápidas',
    body: (
      <dl className="manual-faq">
        <dt>De onde vem cada trecho da minuta?</dt>
        <dd>Sempre há um selo de origem: conteúdo próprio do RO ou citação da fonte (“cf. CBM-XX, …”).</dd>
        <dt>Por que às vezes aparece “competências” em vez do texto do artigo?</dt>
        <dd>Porque o texto integral daquele estado/órgão ainda não foi extraído; mostramos o resumo de competências, com a fonte, até o texto completo ser curado.</dd>
        <dt>As duas minutas funcionam igual?</dt>
        <dd>Sim — mesma trilha (Subsídio → Minuta → Diagramas → Revisão) para o Regimento Interno e para o Regulamento Geral.</dd>
      </dl>
    ),
  },
]

export default function Manual() {
  return (
    <>
      <div className="page-header">
        <div className="page-header-left">
          <h1 className="page-title">Manual de uso</h1>
          <p className="page-subtitle">Como usar o portal, tela por tela.</p>
        </div>
      </div>
      <div className="page-body manual">
        <nav className="manual-toc">
          {SECTIONS.map(s => <a key={s.id} href={`#${s.id}`}>{s.title}</a>)}
        </nav>
        <div className="manual-main">
          {SECTIONS.map(s => (
            <section key={s.id} id={s.id} className="manual-sec">
              <h2>{s.title}</h2>
              {s.body}
            </section>
          ))}
        </div>
      </div>
    </>
  )
}
