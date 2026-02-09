import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import { VitePWA } from 'vite-plugin-pwa'
import fs from 'fs'
import path from 'path'

export default defineConfig({
  plugins: [
    react(),
    VitePWA({
      registerType: 'autoUpdate',
      includeAssets: ['favicon.svg', 'favicon.ico'],
      manifest: {
        name: 'NEXUS PRIME INTELLIGENCE',
        short_name: 'NEXUS PRIME',
        description: 'Advanced Intelligence Visualization & Analysis System',
        theme_color: '#020617',
        background_color: '#020617',
        display: 'standalone',
        icons: [
          {
            src: '/favicon.svg',
            sizes: 'any',
            type: 'image/svg+xml'
          },
          {
            src: '/favicon.ico',
            sizes: '48x48',
            type: 'image/x-icon'
          }
        ],
        start_url: '/',
        scope: '/',
        orientation: 'portrait-primary'
      },
      workbox: {
        globPatterns: ['**/*.{js,css,html,ico,png,svg,woff,woff2}'],
        runtimeCaching: [
          {
            urlPattern: /^https:\/\/fonts\.googleapis\.com\/.*/i,
            handler: 'CacheFirst',
            options: {
              cacheName: 'google-fonts-cache',
              expiration: {
                maxEntries: 10,
                maxAgeSeconds: 60 * 60 * 24 * 365 // 1 rok
              },
              cacheableResponse: {
                statuses: [0, 200]
              }
            }
          },
          {
            urlPattern: /^https:\/\/fonts\.gstatic\.com\/.*/i,
            handler: 'CacheFirst',
            options: {
              cacheName: 'gstatic-fonts-cache',
              expiration: {
                maxEntries: 10,
                maxAgeSeconds: 60 * 60 * 24 * 365 // 1 rok
              },
              cacheableResponse: {
                statuses: [0, 200]
              }
            }
          },
          {
            urlPattern: /^http:\/\/localhost:8000\/api\/.*/i,
            handler: 'NetworkFirst',
            options: {
              cacheName: 'api-cache',
              expiration: {
                maxEntries: 50,
                maxAgeSeconds: 60 * 60 * 24 // 24 hodín
              },
              networkTimeoutSeconds: 10
            }
          }
        ]
      }
    })
  ],
  optimizeDeps: {
    include: [
      'react',
      'react-dom',
      'react-router-dom',
      'prop-types',
      'react-force-graph-2d'
    ],
    esbuildOptions: {
      mainFields: ['module', 'main'],
      resolveExtensions: ['.mjs', '.js', '.jsx', '.ts', '.tsx']
    }
  },
  resolve: {
    dedupe: ['react', 'react-dom', 'prop-types']
  },
  build: {
    rollupOptions: {
      output: {
        manualChunks: {
          'react-vendor': ['react', 'react-dom', 'react-router-dom'],
          'graph-vendor': ['react-force-graph-2d', 'd3-force'],
          'utils': ['lucide-react']
        }
      }
    },
    chunkSizeWarningLimit: 1000
  },
  server: {
    port: 8009,
    host: true,
    https: (() => {
      // SSL konfigurácia
      const sslKeyPath = path.resolve(__dirname, '../ssl/key.pem')
      const sslCertPath = path.resolve(__dirname, '../ssl/cert.pem')

      // Kontrola, či existujú SSL súbory
      if (fs.existsSync(sslKeyPath) && fs.existsSync(sslCertPath)) {
        console.log('🔐 Používam SSL certifikáty pre HTTPS...')
        return {
          key: fs.readFileSync(sslKeyPath),
          cert: fs.readFileSync(sslCertPath),
        }
      } else {
        console.log('⚠️ SSL certifikáty nenájdené, používam HTTP...')
        return false
      }
    })(),
    hmr: {
      overlay: true
    }
  }
})

