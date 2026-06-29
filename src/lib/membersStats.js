// Helpers puros (sem Firebase) sobre a lista de membros: normalização de e-mail,
// situação de acesso exibida e contagem para os cartões da aba Acessos.

export function normalizeEmail(email) {
  return (email ?? '').trim().toLowerCase()
}

// Situação exibida: bloqueado vence tudo (ativo:false); senão o próprio status.
export function situacaoMembro(member) {
  if (member.ativo === false) return 'bloqueado'
  return member.status === 'cadastrado' ? 'cadastrado' : 'convidado'
}

export function contaStatus(members) {
  const c = { total: 0, cadastrados: 0, convidados: 0, bloqueados: 0 }
  for (const m of members) {
    c.total += 1
    const s = situacaoMembro(m)
    if (s === 'bloqueado') c.bloqueados += 1
    else if (s === 'cadastrado') c.cadastrados += 1
    else c.convidados += 1
  }
  return c
}
