// Diagramas do Regulamento Geral — mesmo formato do RI, aguardando o dado de
// estrutura (commandChart) do Regulamento ser gerado.
export default function RegDiagramas() {
  return (
    <>
      <div className="page-header">
        <div className="page-header-left">
          <h1 className="page-title">Diagramas — Regulamento Geral</h1>
          <p className="page-subtitle">Organograma e mapa mental da hierarquia de órgãos da minuta.</p>
        </div>
      </div>
      <div className="subsidio-empty" style={{ marginTop: 16 }}>
        <b>Em breve</b>
        <p>
          Os diagramas do Regulamento seguirão exatamente o mesmo formato do Regimento
          Interno (organograma + mapa mental), assim que o dado de estrutura
          (<code>commandChart</code>) do Regulamento for gerado.
        </p>
      </div>
    </>
  )
}
