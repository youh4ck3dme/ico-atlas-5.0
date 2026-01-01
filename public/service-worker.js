const CACHE_NAME = 'ico-atlas-v5-cache';
const RUNTIME_CACHE = 'ico-atlas-v5-runtime';

// Assets to cache on install
const PRECACHE_ASSETS = [
    '/',
    '/manifest.json',
    // Add your critical assets here
];

// Install event - precache critical assets
self.addEventListener('install', (event) => {
    console.log('Service Worker installing...');
    
    event.waitUntil(
        caches.open(CACHE_NAME)
            .then((cache) => {
                console.log('Precaching assets');
                return cache.addAll(PRECACHE_ASSETS);
            })
            .then(() => self.skipWaiting())
    );
});

// Activate event - clean up old caches
self.addEventListener('activate', (event) => {
    console.log('Service Worker activating...');
    
    event.waitUntil(
        caches.keys().then((cacheNames) => {
            return Promise.all(
                cacheNames.map((cacheName) => {
                    if (cacheName !== CACHE_NAME && cacheName !== RUNTIME_CACHE) {
                        console.log('Deleting old cache:', cacheName);
                        return caches.delete(cacheName);
                    }
                })
            );
        }).then(() => self.clients.claim())
    );
});

// Fetch event - serve from cache, fallback to network
self.addEventListener('fetch', (event) => {
    // Skip cross-origin requests
    if (!event.request.url.startsWith(self.location.origin)) {
        return;
    }

    // Skip non-GET requests
    if (event.request.method !== 'GET') {
        return;
    }

    event.respondWith(
        caches.match(event.request).then((cachedResponse) => {
            if (cachedResponse) {
                // Return cached version
                return cachedResponse;
            }

            // Clone the request
            const fetchRequest = event.request.clone();

            return fetch(fetchRequest).then((response) => {
                // Check if valid response
                if (!response || response.status !== 200 || response.type !== 'basic') {
                    return response;
                }

                // Clone the response
                const responseToCache = response.clone();

                // Cache the new response
                caches.open(RUNTIME_CACHE).then((cache) => {
                    cache.put(event.request, responseToCache);
                });

                return response;
            }).catch(() => {
                // Return offline page if available
                return caches.match('/offline.html');
            });
        })
    );
});

// Background sync for offline data
self.addEventListener('sync', (event) => {
    console.log('Background sync:', event.tag);
    
    if (event.tag === 'sync-searches') {
        event.waitUntil(syncSearches());
    }
});

async function syncSearches() {
    // Implement your sync logic here
    console.log('Syncing offline searches...');
}

// Push notifications
self.addEventListener('push', (event) => {
    console.log('Push notification received');
    
    const options = {
        body: event.data ? event.data.text() : 'New notification from IČO ATLAS',
        icon: '/images/icon-192x192.png',
        badge: '/images/badge-72x72.png',
        vibrate: [200, 100, 200],
        data: {
            dateOfArrival: Date.now(),
            primaryKey: 1
        },
        actions: [
            {
                action: 'explore',
                title: 'Otvoriť',
                icon: '/images/checkmark.png'
            },
            {
                action: 'close',
                title: 'Zavrieť',
                icon: '/images/cross.png'
            }
        ]
    };
    
    event.waitUntil(
        self.registration.showNotification('IČO ATLAS 5.0', options)
    );
});

// Notification click handler
self.addEventListener('notificationclick', (event) => {
    console.log('Notification click:', event.action);
    
    event.notification.close();
    
    if (event.action === 'explore') {
        event.waitUntil(
            clients.openWindow('/')
        );
    }
});

console.log('🇸🇰 IČO ATLAS 5.0 Service Worker loaded');
