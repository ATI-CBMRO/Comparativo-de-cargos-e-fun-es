// Exporta as coleções da revisão colaborativa (suggestions, finalTexts, members, decisions,
// conferencia) do Firestore via REST, autenticando com e-mail+senha de MEMBRO do portal
// (as regras exigem isMember(); `members` completo exige admin).
//
// A credencial entra SÓ por variável de ambiente e não é gravada em lugar nenhum:
//
//   $env:FB_EMAIL='seu@email'; $env:FB_SENHA='...'; node scripts/exportar_firestore.mjs; Remove-Item Env:FB_SENHA
//
// Saída: .firestore-export/fs_<colecao>.json (pasta ignorada pelo git — contém e-mails).
import fs from 'node:fs'
import path from 'node:path'
import { fileURLToPath } from 'node:url'

const ROOT = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..')
const OUT_DIR = process.argv.includes('--out') ? process.argv[process.argv.indexOf('--out') + 1] : path.join(ROOT, '.firestore-export')

// Config pública do app web (a mesma do bundle do frontend / .env VITE_FIREBASE_*).
const API_KEY = process.env.VITE_FIREBASE_API_KEY ?? lerEnv('VITE_FIREBASE_API_KEY')
const PROJECT = process.env.VITE_FIREBASE_PROJECT_ID ?? lerEnv('VITE_FIREBASE_PROJECT_ID')

function lerEnv(chave) {
  for (const f of ['.env', '.env.local']) {
    const p = path.join(ROOT, f)
    if (!fs.existsSync(p)) continue
    const m = fs.readFileSync(p, 'utf8').match(new RegExp(`^${chave}="?([^"\\r\\n]+)"?`, 'm'))
    if (m) return m[1]
  }
  throw new Error(`${chave} não encontrada no ambiente nem em .env`)
}

const email = process.env.FB_EMAIL
const senha = process.env.FB_SENHA
if (!email || !senha) {
  console.error('Defina FB_EMAIL e FB_SENHA no ambiente (não são gravadas).')
  process.exit(2)
}

const login = await fetch(`https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword?key=${API_KEY}`, {
  method: 'POST', headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({ email, password: senha, returnSecureToken: true }),
})
if (!login.ok) { console.error('Login falhou:', await login.text()); process.exit(1) }
const { idToken } = await login.json()

function fromValue(v) {
  if (v == null) return null
  if ('stringValue' in v) return v.stringValue
  if ('integerValue' in v) return Number(v.integerValue)
  if ('doubleValue' in v) return v.doubleValue
  if ('booleanValue' in v) return v.booleanValue
  if ('nullValue' in v) return null
  if ('timestampValue' in v) return v.timestampValue
  if ('arrayValue' in v) return (v.arrayValue.values ?? []).map(fromValue)
  if ('mapValue' in v) return fromFields(v.mapValue.fields ?? {})
  if ('referenceValue' in v) return v.referenceValue
  return v
}
function fromFields(fields) {
  const o = {}
  for (const [k, v] of Object.entries(fields)) o[k] = fromValue(v)
  return o
}

async function listAll(col) {
  const docs = []
  let pageToken = ''
  do {
    const url = `https://firestore.googleapis.com/v1/projects/${PROJECT}/databases/(default)/documents/${col}?pageSize=300${pageToken ? `&pageToken=${pageToken}` : ''}`
    const r = await fetch(url, { headers: { Authorization: `Bearer ${idToken}` } })
    if (!r.ok) { console.error(`[${col}] HTTP ${r.status}: ${(await r.text()).slice(0, 300)}`); return docs }
    const j = await r.json()
    for (const d of j.documents ?? []) {
      docs.push({ id: decodeURIComponent(d.name.split('/').pop()), ...fromFields(d.fields ?? {}), _createTime: d.createTime, _updateTime: d.updateTime })
    }
    pageToken = j.nextPageToken ?? ''
  } while (pageToken)
  return docs
}

fs.mkdirSync(OUT_DIR, { recursive: true })
for (const col of ['suggestions', 'finalTexts', 'members', 'decisions', 'conferencia']) {
  const docs = await listAll(col)
  fs.writeFileSync(path.join(OUT_DIR, `fs_${col}.json`), JSON.stringify(docs, null, 2), 'utf8')
  console.log(`${col}: ${docs.length} documentos`)
}
console.log(`Exportado em ${OUT_DIR}`)
