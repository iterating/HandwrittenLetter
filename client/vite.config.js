import { defineConfig, loadEnv } from 'vite';
import react from '@vitejs/plugin-react';

// https://vitejs.dev/config/
export default defineConfig(({ mode }) => {
  // Load env file based on mode
  const env = loadEnv(mode, process.cwd());
  
  // Get API URL from environment or use default
  const apiUrl = env.VITE_API_URL || 'http://localhost:5000';
  
  console.log(`Mode: ${mode}, API URL: ${apiUrl}`);
  
  return {
    plugins: [react()],
    build: {
      outDir: 'dist',
    },
    server: {
      proxy: {
        '/api': {
          target: apiUrl,
          changeOrigin: true,
          secure: false,
          rewrite: (path) => path,
          configure: (proxy, _options) => {
            proxy.on('error', (err, _req, _res) => {
              console.log('Proxy error:', err);
            });
            proxy.on('proxyReq', (proxyReq, req, _res) => {
              console.log('Sending Request:', req.method, req.url);
            });
            proxy.on('proxyRes', (proxyRes, req, _res) => {
              console.log('Received Response:', proxyRes.statusCode, req.url);
            });
          },
        },
        '/health': {
          target: apiUrl,
          changeOrigin: true,
          secure: false,
        }
      },
    },
    define: {
      // Make environment variables available to the client
      'process.env.VITE_API_URL': JSON.stringify(apiUrl),
    },
  };
});
