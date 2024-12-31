import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// https://vite.dev/config/
export default defineConfig({
  plugins: [react()],
  server: {
    port: 5173,
    proxy: {
      '/api': {
        target: process.env.NODE_ENV === 'production'
          ? 'http://handwritten-env.eba-szypw8be.us-west-2.elasticbeanstalk.com'
          : 'http://localhost:5000',
        changeOrigin: true,
        rewrite: (path) => path.replace(/^\/api/, ''),
      },
      '/images': {
        target: process.env.NODE_ENV === 'production'
          ? 'http://handwritten-env.eba-szypw8be.us-west-2.elasticbeanstalk.com'
          : 'http://localhost:5000',
        changeOrigin: true
      }
    }
  }
})
