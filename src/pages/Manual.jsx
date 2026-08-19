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
    id: 'apresentacao', title: 'Apresentação — Regulamento de Serviço',
    body: (
      <>
        <p>
          Apresentação usada na reunião de 18/08/2026 com a Coordenação da CAT e do COB e os
          Comandantes de GBM e DAT: por que o sistema existe, o recorte de escopo (7 temas, 180
          artigos), como solicitar acesso, como comentar na sala de revisão e o cronograma da
          Fase 1.
        </p>
        <p>
          <a
            href="https://claude.ai/code/artifact/e4c0b4e6-0f43-455d-b07c-30e714deae2c"
            target="_blank"
            rel="noopener noreferrer"
          >
            Abrir a apresentação →
          </a>
        </p>
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
          A barra lateral começa expandida. Use <b>"Recolher menu"</b> no rodapé dela (ou o ☰ no
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
    id: 'acervo-publico', title: 'Acervo Legal — consulta pública',
    body: (
      <>
        <p>
          Existe um endereço <b>público</b> do Acervo, para divulgar a quem só precisa
          consultar a legislação e não participa da elaboração das minutas:
          <b> /acervo-publico</b>. Serve para ofício, site institucional ou QR code.
        </p>
        <ul>
          <li>Não exige login e senha: a pessoa informa <b>nome, e-mail e instituição</b> e já entra.</li>
          <li>Ela enxerga <b>apenas</b> o Acervo, a ficha de cada estado e a Busca. Nenhuma minuta,
              nenhum subsídio, nenhuma tela de curadoria.</li>
          <li>O navegador lembra o cadastro: quem volta não preenche de novo.</li>
          <li>Quem entrou aparece em <b>Acessos</b>, na seção <b>Visitantes do acervo público</b> —
              é registro de histórico, sem aprovação e sem bloqueio.</li>
        </ul>
        <div className="manual-callout">
          <b>Por que não tem senha.</b> Os documentos do acervo são legislação pública de outros
          Corpos de Bombeiros. O cadastro existe para o comando saber quem consulta, não para
          restringir o acesso.
        </div>
      </>
    ),
  },
  {
    id: 'acervo-publico-envio', title: 'Acervo público — recebendo documentos',
    body: (
      <>
        <p>
          Quem entra pela página pública (<b>/acervo-publico</b>) também pode <b>contribuir</b>:
          a aba <b>Enviar documento</b> aceita um PDF de até 20 MB, com o estado de origem, o
          tipo de documento e uma observação.
        </p>
        <ul>
          <li>Os envios aparecem em <b>Acessos</b>, seção <b>Documentos enviados por visitantes</b>.</li>
          <li>Clique em <b>baixar</b> para abrir o PDF e avaliar.</li>
          <li>Se o documento for aproveitado, ele entra no acervo pelo <b>processo de ingestão de
              sempre</b> — o envio não publica nada sozinho.</li>
          <li><b>remover</b> tira da lista e apaga o arquivo junto; use depois de já ter baixado
              ou decidido descartar.</li>
        </ul>
        <div className="manual-callout">
          <b>Nada entra no acervo automaticamente.</b> A tela de envio é uma caixa de entrada:
          todo arquivo passa pela curadoria antes de virar parte do acervo comparado.
        </div>
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
          <li>O painel mostra o <b>texto original</b> do artigo quando existe (com os incisos) ou, na falta dele, um <b>resumo de competências</b> rotulado como "texto integral ainda não extraído".</li>
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
          <li><b>Revisão &amp; curadoria</b>: ajuste o texto item a item; cada trecho mostra a origem (próprio do RO ou "cf. CBM-XX").</li>
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
          (interruptor de segurança). Antes disso, a comissão vê "em preparação".
        </div>
      </>
    ),
  },
  {
    id: 'faq', title: 'Perguntas rápidas',
    body: (
      <>
        <dl className="manual-faq">
          <dt>De onde vem cada trecho da minuta?</dt>
          <dd>Sempre há um selo de origem: conteúdo próprio do RO ou citação da fonte ("cf. CBM-XX, …").</dd>
          <dt>Por que às vezes aparece "competências" em vez do texto do artigo?</dt>
          <dd>Porque o texto integral daquele estado/órgão ainda não foi extraído; mostramos o resumo de competências, com a fonte, até o texto completo ser curado.</dd>
          <dt>As duas minutas funcionam igual?</dt>
          <dd>Sim — mesma trilha (Subsídio → Minuta → Diagramas → Revisão) para o Regimento Interno e para o Regulamento Geral.</dd>
        </dl>
      </>
    ),
  },
  {
    id: 'cockpit', title: 'Cockpit de curadoria — como decidir',
    body: (
      <>
        <p>
          O <b>cockpit de curadoria</b> é o conjunto de telas onde as minutas são conferidas e
          as <b>Decisões CBMRO</b> são analisadas e registradas. Quem analisa as decisões deve
          seguir esta dinâmica:
        </p>
        <p>
          <b>1. Conferência</b> (menu de cada trilha): percorra a minuta artigo por artigo, com as
          referências dos outros estados ao lado. Marque <b>Confere</b> ou <b>Divergente</b> —
          logado, a marcação fica salva para todos; o Divergente vira pendência na aba Decisões.
        </p>
        <p>
          <b>2. Decisões</b> (menu de cada trilha): cada cartão traz a <b>Questão</b> (o que precisa
          ser decidido), as <b>redações candidatas</b> (texto literal das leis de outros estados,
          com a leitura do curador) e a <b>Comparação</b>. Os selos: <b>Pendente</b> (ninguém
          decidiu), <b>Decidida no vault</b> (decisão anotada no acervo de estudo) e
          <b> Decidida no sistema</b> (registrada aqui — é a que vale).
        </p>
        <p>
          <b>3. Registrar</b> (botão visível para o papel administrador): escolha o tipo —
          <b> Redação</b> (você aponta o artigo alvo e escreve o texto final; ele passa a aparecer
          na Minuta e no arquivo .docx baixado, com o aviso de quantos textos finais estão
          aplicados) ou <b>Estrutural</b> (muda a organização — fusão de órgãos, subordinação;
          gera uma <b>ficha de aplicação</b> que fica pendente até ser aplicada em sessão de
          trabalho). Registre sempre o <b>porquê</b> da decisão.
        </p>
        <p>
          <b>4. Retorno ao acervo</b>: o administrador exporta as decisões registradas
          (botão <b>Exportar decisões</b>) e um passo local atualiza as notas de estudo no
          Obsidian — nada se perde e o histórico fica completo.
        </p>
        <div className="manual-callout">
          <b>Regra de ouro:</b> decida <b>lendo o conteúdo</b> das candidatas, nunca pela
          semelhança de nomes de órgãos ou temas — órgãos com nomes parecidos podem tratar de
          matérias completamente diferentes.
        </div>
      </>
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
