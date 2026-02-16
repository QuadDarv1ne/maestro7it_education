// Service Worker для ChessCalendar-RU PWA
const CACHE_VERSION = 'v3.0';
const CACHE_NAME = `chess-calendar-${CACHE_VERSION}`;
const RUNTIME_CACHE = `runtime-${CACHE_VERSION}`;
const IMAGE_CACHE = `images-${CACHE_VERSION}`;

// Ресурсы для предварительного кэширования
const PRECACHE_URLS = [
    '/',
    '/static/js/app.js',
    '/static/js/search.js',
    '/static/css/mobile.css',
    '/static/manifest.json',
    'https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css',
    'https://cdn.jsdelivr.net/npm/bootstrap-icons@1.11.0/font/bootstrap-icons.css',
    'https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js',
    'https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap',
    '/static/icons/icon-192x192.png',
    '/static/icons/icon-512x512.png'
];

// Установка Service Worker
self.addEventListener('install', (event) => {
    console.log('[SW] Installing Service Worker...');
    
    event.waitUntil(
        caches.open(CACHE_NAME)
            .then((cache) => {
                console.log('[SW] Precaching app shell');
                return cache.addAll(PRECACHE_URLS);
            })
            .then(() => self.skipWaiting())
    );
});

// Активация Service Worker
self.addEventListener('activate', (event) => {
    console.log('[SW] Activating Service Worker...');
    
    event.waitUntil(
        caches.keys()
            .then((cacheNames) => {
                return Promise.all(
                    cacheNames
                        .filter((cacheName) => {
                            return cacheName.startsWith('chess-calendar-') && 
                                   cacheName !== CACHE_NAME &&
                                   cacheName !== RUNTIME_CACHE &&
                                   cacheName !== IMAGE_CACHE;
                        })
                        .map((cacheName) => {
                            console.log('[SW] Deleting old cache:', cacheName);
                            return caches.delete(cacheName);
                        })
                );
            })
            .then(() => self.clients.claim())
    );
});

// Стратегии кэширования
const strategies = {
    // Network First - для API запросов
    networkFirst: async (request) => {
        try {
            const networkResponse = await fetch(request);
            if (networkResponse.ok) {
                const cache = await caches.open(RUNTIME_CACHE);
                cache.put(request, networkResponse.clone());
            }
            return networkResponse;
        } catch (error) {
            const cachedResponse = await caches.match(request);
            if (cachedResponse) {
                return cachedResponse;
            }
            throw error;
        }
    },
    
    // Cache First - для статических ресурсов
    cacheFirst: async (request) => {
        const cachedResponse = await caches.match(request);
        if (cachedResponse) {
            return cachedResponse;
        }
        
        try {
            const networkResponse = await fetch(request);
            if (networkResponse.ok) {
                const cache = await caches.open(CACHE_NAME);
                cache.put(request, networkResponse.clone());
            }
            return networkResponse;
        } catch (error) {
            throw error;
        }
    },
    
    // Stale While Revalidate - для изображений
    staleWhileRevalidate: async (request) => {
        const cachedResponse = await caches.match(request);
        
        const fetchPromise = fetch(request).then((networkResponse) => {
            if (networkResponse.ok) {
                const cache = caches.open(IMAGE_CACHE);
                cache.then((c) => c.put(request, networkResponse.clone()));
            }
            return networkResponse;
        });
        
        return cachedResponse || fetchPromise;
    }
};

// Перехват fetch запросов
self.addEventListener('fetch', (event) => {
    const { request } = event;
    const url = new URL(request.url);
    
    // Игнорируем не-GET запросы
    if (request.method !== 'GET') {
        return;
    }
    
    // Игнорируем chrome-extension и другие схемы
    if (!url.protocol.startsWith('http')) {
        return;
    }
    
    // API запросы - Network First
    if (url.pathname.startsWith('/api/')) {
        event.respondWith(strategies.networkFirst(request));
        return;
    }
    
    // Изображения - Stale While Revalidate
    if (request.destination === 'image') {
        event.respondWith(strategies.staleWhileRevalidate(request));
        return;
    }
    
    // Статические ресурсы - Cache First
    if (url.pathname.startsWith('/static/') || 
        url.hostname.includes('cdn.jsdelivr.net') ||
        url.hostname.includes('fonts.googleapis.com') ||
        url.hostname.includes('fonts.gstatic.com')) {
        event.respondWith(strategies.cacheFirst(request));
        return;
    }
    
    // HTML страницы - Network First с fallback
    if (request.destination === 'document') {
        event.respondWith(
            strategies.networkFirst(request)
                .catch(() => caches.match('/'))
        );
        return;
    }
    
    // Все остальное - Network First
    event.respondWith(strategies.networkFirst(request));
});

// Background Sync для офлайн действий
self.addEventListener('sync', (event) => {
    console.log('[SW] Background sync:', event.tag);
    
    if (event.tag === 'sync-favorites') {
        event.waitUntil(syncFavorites());
    }
});

async function syncFavorites() {
    // Синхронизация избранного при восстановлении соединения
    try {
        const cache = await caches.open(RUNTIME_CACHE);
        const requests = await cache.keys();
        
        // Отправляем отложенные запросы
        for (const request of requests) {
            if (request.url.includes('/favorites/')) {
                await fetch(request);
            }
        }
    } catch (error) {
        console.error('[SW] Sync failed:', error);
    }
}

// Push уведомления
self.addEventListener('push', (event) => {
    console.log('[SW] Push notification received');
    
    let data = {
        title: 'ChessCalendar-RU',
        body: 'Новое уведомление',
        icon: '/static/icons/icon-192x192.png',
        badge: '/static/icons/icon-72x72.png',
        url: '/'
    };
    
    if (event.data) {
        try {
            data = { ...data, ...event.data.json() };
        } catch (e) {
            data.body = event.data.text();
        }
    }
    
    const options = {
        body: data.body,
        icon: data.icon,
        badge: data.badge,
        tag: 'chess-calendar-notification',
        data: { url: data.url },
        vibrate: [200, 100, 200],
        actions: [
            {
                action: 'open',
                title: 'Открыть',
                icon: '/static/icons/icon-72x72.png'
            },
            {
                action: 'close',
                title: 'Закрыть'
            }
        ]
    };
    
    event.waitUntil(
        self.registration.showNotification(data.title, options)
    );
});

// Обработка кликов по уведомлениям
self.addEventListener('notificationclick', (event) => {
    console.log('[SW] Notification clicked:', event.action);
    
    event.notification.close();
    
    if (event.action === 'close') {
        return;
    }
    
    const urlToOpen = event.notification.data?.url || '/';
    
    event.waitUntil(
        clients.matchAll({ type: 'window', includeUncontrolled: true })
            .then((clientList) => {
                // Проверяем, есть ли уже открытое окно
                for (const client of clientList) {
                    if (client.url === urlToOpen && 'focus' in client) {
                        return client.focus();
                    }
                }
                // Открываем новое окно
                if (clients.openWindow) {
                    return clients.openWindow(urlToOpen);
                }
            })
    );
});

// Обработка сообщений от клиента
self.addEventListener('message', (event) => {
    console.log('[SW] Message received:', event.data);
    
    if (event.data.action === 'skipWaiting') {
        self.skipWaiting();
    }
    
    if (event.data.action === 'clearCache') {
        event.waitUntil(
            caches.keys().then((cacheNames) => {
                return Promise.all(
                    cacheNames.map((cacheName) => caches.delete(cacheName))
                );
            })
        );
    }
});

console.log('[SW] Service Worker loaded');
