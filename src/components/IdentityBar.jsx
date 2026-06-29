// Barra de "login simulado": escolhe qual coronel você é (autoria das ações) +
// rótulo da fase. No protótipo, a sessão vem do suggestionsStore (não há auth real).
export default function IdentityBar({ users, currentUser, onChangeUser, phaseLabel }) {
  return (
    <div style={{
      display: 'flex', alignItems: 'center', gap: 10, flexWrap: 'wrap',
      background: '#121d3d', color: '#fff', padding: '8px 14px', borderRadius: 8,
      fontSize: 13, marginBottom: 16,
    }}>
      <span style={{ background: 'rgba(255,255,255,.14)', padding: '3px 10px', borderRadius: 20, fontWeight: 600 }}>
        {phaseLabel}
      </span>
      <span style={{ opacity: .7 }}>Minuta de RI · CBMRO</span>
      <label style={{ marginLeft: 'auto', display: 'inline-flex', alignItems: 'center', gap: 8 }}>
        <span style={{ opacity: .7 }}>Você está como</span>
        <select
          value={currentUser?.id ?? ''}
          onChange={e => onChangeUser(e.target.value)}
          style={{
            background: '#0d1730', color: '#fff', border: '1px solid #2a3a63',
            borderRadius: 6, padding: '5px 8px', fontSize: 13, fontWeight: 600,
          }}
        >
          {users.map(u => (
            <option key={u.id} value={u.id}>
              {u.posto} {u.name}{u.role === 'relator' ? ' (relator)' : ''}
            </option>
          ))}
        </select>
      </label>
    </div>
  )
}
