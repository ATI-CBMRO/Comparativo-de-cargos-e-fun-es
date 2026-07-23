// Aviso visual de queda de sincronização com o Firestore (auditoria 2026-07-23).
// Antes, erros de onSnapshot eram só logados no console e a tela ficava com dados
// congelados sem nenhum sinal — quem usa podia decidir em cima de dado velho.
export default function AvisoSincronizacao({ visivel, children }) {
  if (!visivel) return null
  return (
    <div
      role="alert"
      style={{
        margin: '8px 0', padding: '8px 12px', borderRadius: 8,
        background: '#fdecea', border: '1px solid #f5c6cb', color: '#8a1c24',
        fontSize: 13, fontWeight: 600,
      }}
    >
      ⚠️ {children ?? 'A sincronização com o servidor caiu — os dados abaixo podem estar desatualizados. Recarregue a página.'}
    </div>
  )
}
