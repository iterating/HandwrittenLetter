import { build } from 'vite'
import { fileURLToPath } from 'url'
import { dirname, resolve } from 'path'

const __filename = fileURLToPath(import.meta.url)
const __dirname = dirname(__filename)

async function buildApp() {
  try {
    await build({
      root: __dirname,
      build: {
        outDir: resolve(__dirname, 'dist'),
        emptyOutDir: true
      }
    })
    console.log('Build completed successfully')
  } catch (e) {
    console.error('Build failed:', e)
    process.exit(1)
  }
}

buildApp()
