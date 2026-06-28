import { defineConfig, loadEnv } from 'vite'
import react from '@vitejs/plugin-react'
import path from 'path'
import fs from 'fs'
import { gerarPropostaCore } from './api/_gerarProposta.js'

// Plugin que serve a pasta database/ como rota estática /database/ e LEGISLAÇÃO CBMS/ como /legislacao-pdf/
function serveDatabase() {
  return {
    name: 'serve-database',
    configureServer(server) {
      // Servir pasta database
      server.middlewares.use('/database', (req, res, next) => {
        const filePath = path.join(process.cwd(), 'database', req.url || '')
        try {
          if (fs.existsSync(filePath) && fs.statSync(filePath).isFile()) {
            const ext = path.extname(filePath).toLowerCase()
            const types = { '.json': 'application/json', '.md': 'text/plain' }
            res.setHeader('Content-Type', (types[ext] || 'text/plain') + '; charset=utf-8')
            res.setHeader('Cache-Control', 'no-cache')
            res.end(fs.readFileSync(filePath))
          } else {
            next()
          }
        } catch {
          next()
        }
      })

      // Servir pasta LEGISLAÇÃO CBMS
      server.middlewares.use('/legislacao-pdf', (req, res, next) => {
        const decodedUrl = decodeURIComponent(req.url || '')
        const filePath = path.join(process.cwd(), 'LEGISLAÇÃO CBMS', decodedUrl)
        try {
          if (fs.existsSync(filePath) && fs.statSync(filePath).isFile()) {
            res.setHeader('Content-Type', 'application/pdf')
            res.setHeader('Cache-Control', 'no-cache')
            res.end(fs.readFileSync(filePath))
          } else {
            next()
          }
        } catch {
          next()
        }
      })
    }
  }
}

function copyDirRecursive(src, dest) {
  if (!fs.existsSync(src)) return
  fs.mkdirSync(dest, { recursive: true })
  const entries = fs.readdirSync(src, { withFileTypes: true })
  for (const entry of entries) {
    const srcPath = path.join(src, entry.name)
    const destPath = path.join(dest, entry.name)
    if (entry.isDirectory()) {
      copyDirRecursive(srcPath, destPath)
    } else if (entry.isFile()) {
      fs.copyFileSync(srcPath, destPath)
    }
  }
}

function copyDatabaseOnBuild() {
  return {
    name: 'copy-database-on-build',
    closeBundle() {
      const distDir = path.join(process.cwd(), 'dist')
      if (!fs.existsSync(distDir)) return

      // Copiar database/ para dist/database/
      const srcDatabase = path.join(process.cwd(), 'database')
      const destDatabase = path.join(distDir, 'database')
      if (fs.existsSync(srcDatabase)) {
        console.log('\n[Vite] Copiando pasta database para o build de produção...')
        try {
          copyDirRecursive(srcDatabase, destDatabase)
          console.log('[Vite] Pasta database copiada com sucesso.')
        } catch (err) {
          console.error('[Vite] Erro ao copiar a pasta database:', err)
        }
      }

      // Copiar LEGISLAÇÃO CBMS/ para dist/legislacao-pdf/
      const srcPdf = path.join(process.cwd(), 'LEGISLAÇÃO CBMS')
      const destPdf = path.join(distDir, 'legislacao-pdf')
      if (fs.existsSync(srcPdf)) {
        console.log('[Vite] Copiando pasta LEGISLAÇÃO CBMS para o build de produção...')
        try {
          copyDirRecursive(srcPdf, destPdf)
          console.log('[Vite] Pasta LEGISLAÇÃO CBMS copiada com sucesso.')
        } catch (err) {
          console.error('[Vite] Erro ao copiar a pasta LEGISLAÇÃO CBMS:', err)
        }
      }
    }
  }
}

// Em desenvolvimento, atende /api/gerar-proposta com a MESMA lógica da função da Vercel.
function geminiDevApi(apiKey) {
  return {
    name: 'gemini-dev-api',
    configureServer(server) {
      server.middlewares.use('/api/gerar-proposta', async (req, res, next) => {
        if (req.method !== 'POST') return next()
        try {
          let body = ''
          for await (const chunk of req) body += chunk
          const { textoAtual, sugestoes } = JSON.parse(body || '{}')
          const proposta = await gerarPropostaCore({ textoAtual, sugestoes, apiKey })
          res.setHeader('Content-Type', 'application/json; charset=utf-8')
          res.end(JSON.stringify({ proposta }))
        } catch (e) {
          res.statusCode = 500
          res.setHeader('Content-Type', 'application/json; charset=utf-8')
          res.end(JSON.stringify({ error: String(e?.message || e) }))
        }
      })
    },
  }
}

export default defineConfig(({ mode }) => {
  const env = loadEnv(mode, process.cwd(), '')
  return {
    plugins: [react(), serveDatabase(), copyDatabaseOnBuild(), geminiDevApi(env.GEMINI_API_KEY)],
    server: { port: 5173 },
  }
})
