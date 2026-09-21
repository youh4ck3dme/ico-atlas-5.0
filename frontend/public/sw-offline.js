// Offline Service Worker pre ILUMINATI SYSTEM
// Rozširuje základný Service Worker o offline funkcionalitu

const CACHE_NAME = 'iluminati-offline-v1';
const OFFLINE_PAGE = '/offline.html';
const API_CACHE_NAME = 'iluminati-api-cache-v1';

// Assets ktoré sa majú cacheovať offline
const STATIC_ASSETS = [
  '/',
  '/offline.html',
  '/manifest.json',
  '/favicon.svg'
];

// API endpoints ktoré sa majú cacheovať
const API_ENDPOINTS = [
  '/api/health',
  '/api/cache/stats'
];

// Inštalácia Service Workera
self.addEventListener('install', (event) => {
  console.log('[SW] Installing offline service worker...');
  event.waitUntil(
    caches.open(CACHE_NAME).then((cache) => {
      console.log('[SW] Caching static assets');
      return cache.addAll(STATIC_ASSETS);
    }).then(() => {
      return self.skipWaiting();
    })
  );
});

// Aktivácia Service Workera
self.addEventListener('activate', (event) => {
  console.log('[SW] Activating offline service worker...');
  event.waitUntil(
    caches.keys().then((cacheNames) => {
      return Promise.all(
        cacheNames.map((cacheName) => {
          if (cacheName !== CACHE_NAME && cacheName !== API_CACHE_NAME) {
            console.log('[SW] Deleting old cache:', cacheName);
            return caches.delete(cacheName);
          }
        })
      );
    }).then(() => {
      return self.clients.claim();
    })
  );
});

// Fetch event - Network First s Cache Fallback
self.addEventListener('fetch', (event) => {
  const { request } = event;
  const url = new URL(request.url);

  // API requests - Network First s Cache Fallback
  if (url.pathname.startsWith('/api/')) {
    event.respondWith(networkFirstWithCache(request));
    return;
  }

  // Static assets - Cache First
  if (isStaticAsset(request.url)) {
    event.respondWith(cacheFirst(request));
    return;
  }

  // HTML pages - Network First s Offline Fallback
  if (request.mode === 'navigate') {
    event.respondWith(networkFirstWithOfflinePage(request));
    return;
  }

  // Default - Network First
  event.respondWith(networkFirst(request));
});

// Network First s Cache Fallback (pre API)
async function networkFirstWithCache(request) {
  try {
    const response = await fetch(request);
    
    // Cache successful responses
    if (response.ok) {
      const cache = await caches.open(API_CACHE_NAME);
      cache.put(request, response.clone());
    }
    
    return response;
  } catch (error) {
    console.log('[SW] Network failed, trying cache:', request.url);
    
    // Try cache
    const cachedResponse = await caches.match(request);
    if (cachedResponse) {
      return cachedResponse;
    }
    
    // Return offline response for API
    return new Response(
      JSON.stringify({
        error: true,
        message: 'Offline - cached data not available',
        offline: true
      }),
      {
        status: 503,
        headers: { 'Content-Type': 'application/json' }
      }
    );
  }
}

// Cache First (pre static assets)
async function cacheFirst(request) {
  const cachedResponse = await caches.match(request);
  if (cachedResponse) {
    return cachedResponse;
  }
  
  try {
    const response = await fetch(request);
    if (response.ok) {
      const cache = await caches.open(CACHE_NAME);
      cache.put(request, response.clone());
    }
    return response;
  } catch (error) {
    console.log('[SW] Failed to fetch:', request.url);
    return new Response('Offline', { status: 503 });
  }
}

// Network First s Offline Page Fallback (pre HTML)
async function networkFirstWithOfflinePage(request) {
  try {
    const response = await fetch(request);
    return response;
  } catch (error) {
    console.log('[SW] Network failed, showing offline page');
    const cache = await caches.open(CACHE_NAME);
    const offlinePage = await cache.match(OFFLINE_PAGE);
    if (offlinePage) {
      return offlinePage;
    }
    return new Response('Offline', { status: 503 });
  }
}

// Network First (default)
async function networkFirst(request) {
  try {
    return await fetch(request);
  } catch (error) {
    const cachedResponse = await caches.match(request);
    if (cachedResponse) {
      return cachedResponse;
    }
    throw error;
  }
}

// Helper - check if static asset
function isStaticAsset(url) {
  return url.match(/\.(js|css|png|jpg|jpeg|gif|svg|ico|woff|woff2|ttf|eot)$/);
}

// Background sync pre offline actions
self.addEventListener('sync', (event) => {
  if (event.tag === 'sync-search') {
    event.waitUntil(syncSearches());
  }
});

async function syncSearches() {
  // Sync offline searches when back online
  console.log('[SW] Syncing offline searches...');
  // Implementation would sync queued searches
}

// Push notifications (pre budúce rozšírenia)
self.addEventListener('push', (event) => {
  const data = event.data ? event.data.json() : {};
  const title = data.title || 'ILUMINATI SYSTEM';
  const options = {
    body: data.body || 'New update available',
    icon: '/favicon.svg',
    badge: '/favicon.svg'
  };
  
  event.waitUntil(
    self.registration.showNotification(title, options)
  );
});

