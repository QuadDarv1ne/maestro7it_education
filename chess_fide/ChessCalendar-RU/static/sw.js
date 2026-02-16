// Service Worker для ChessCalendar-RU PWA
const CACHE_VERSION = 'v4.0';
const CACHE_NAME = `chess-calendar-${CACHE_VERSION}`;
const RUNTIME_CACHE = `runtime-${CACHE_VERSION}`;
const IMAGE_CACHE = `images-${CACHE_VERSION}`;
const API_CACHE = `api-${CACHE_VERSION}`;

// Ресурсы для предварительного кэширования
const PRECACHE_URLS = [
    '/',
    '/offline',
    '/static/js/app.js',
    '/static/js/lazy-loader.js',
    '/static/js/bundles/core.min.js',
    '/static/js/bundles/ui-features.min.js',
    '/static/js/bundles/tournament-features.min.js',
    '/static/css/mobile.css',
    '/static/css/mobile-enhanced.css',
    '/static/css/responsive-enhanced.css',
    '/static/css/dark-theme.css',
    '/static/css/improvements.css',
    '/static/manifest.json',
    'https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css',
    'https://cdn.jsdelivr.net/npm/bootstrap-icons@1.11.0/font/bootstrap-icons.css',
    'https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js',
    'https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap',
    '/static/icons/icon-72x72.png',
    '/static/icons/icon-96x96.png',
    '/static/icons/icon-128x128.png',
    '/static/icons/icon-144x144.png',
    '/static/icons/icon-152x152.png',
    '/static/icons/icon-192x192.png',
    '/static/icons/icon-384x384.png',
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
                                   cacheName !== IMAGE_CACHE &&
                                   cacheName !== API_CACHE;
                        })
                        .map((cacheName) => {
                            console.log('[SW] Deleting old cache:', cacheName);
                            return caches.delete(cacheName);
                        })
                );
            })
            .then(() => {
                console.log('[SW] Claiming clients');
                return self.clients.claim();
            })
    );
});

// Стратегии кэширования
const strategies = {
    // Network First - для API запросов
    networkFirst: async (request) => {
        try {
            const networkResponse = await fetch(request);
            if (networkResponse.ok) {
                const cache = await caches.open(API_CACHE);
                cache.put(request, networkResponse.clone());
            }
            return networkResponse;
        } catch (error) {
            console.log('[SW] Network failed, using cache for:', request.url);
            const cachedResponse = await caches.match(request);
            if (cachedResponse) {
                return cachedResponse;
            }
            // Return offline page for navigation requests
            if (request.destination === 'document') {
                return caches.match('/offline');
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
            console.error('[SW] Both network and cache failed for:', request.url);
            // Return fallback for critical resources
            if (request.destination === 'document') {
                return caches.match('/offline');
            }
            throw error;
        }
    },
    
    // Stale While Revalidate - для изображений
    staleWhileRevalidate: async (request) => {
        const cachedResponse = await caches.match(request);
        
        const fetchPromise = fetch(request).then((networkResponse) => {
            if (networkResponse.ok) {
                caches.open(IMAGE_CACHE).then((cache) => {
                    cache.put(request, networkResponse.clone());
                });
            }
            return networkResponse;
        }).catch(error => {
            console.log('[SW] Image fetch failed, using cached version');
            return cachedResponse;
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
                .catch(() => caches.match('/offline'))
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
    } else if (event.tag === 'sync-ratings') {
        event.waitUntil(syncRatings());
    } else if (event.tag === 'sync-subscriptions') {
        event.waitUntil(syncSubscriptions());
    }
});

async function syncFavorites() {
    // Синхронизация избранного при восстановлении соединения
    try {
        const favorites = await getOfflineData('favorites');
        for (const favorite of favorites) {
            await fetch('/api/tournaments/' + favorite.tournament_id + '/favorite', {
                method: favorite.action,
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ user_id: favorite.user_id })
            });
            // Remove from offline storage after sync
            await removeFromOfflineData('favorites', favorite.id);
        }
    } catch (error) {
        console.error('[SW] Favorites sync failed:', error);
    }
}

async function syncRatings() {
    // Синхронизация оценок при восстановлении соединения
    try {
        const ratings = await getOfflineData('ratings');
        for (const rating of ratings) {
            await fetch('/api/tournaments/' + rating.tournament_id + '/rate', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    user_id: rating.user_id,
                    rating: rating.rating,
                    review: rating.review
                })
            });
            // Remove from offline storage after sync
            await removeFromOfflineData('ratings', rating.id);
        }
    } catch (error) {
        console.error('[SW] Ratings sync failed:', error);
    }
}

async function syncSubscriptions() {
    // Синхронизация подписок при восстановлении соединения
    try {
        const subscriptions = await getOfflineData('subscriptions');
        for (const sub of subscriptions) {
            await fetch('/api/notifications/subscribe', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(sub)
            });
            // Remove from offline storage after sync
            await removeFromOfflineData('subscriptions', sub.id);
        }
    } catch (error) {
        console.error('[SW] Subscriptions sync failed:', error);
    }
}

// Helper functions for offline data storage
async function getOfflineData(type) {
    // Implementation would depend on IndexedDB or similar storage
    // For now, return empty array
    return [];
}

async function removeFromOfflineData(type, id) {
    // Implementation would depend on IndexedDB or similar storage
    // For now, just return
    return Promise.resolve();
}

// Push уведомления
self.addEventListener('push', (event) => {
    console.log('[SW] Push notification received');
    
    let data = {
        title: 'ChessCalendar-RU',
        body: 'Новое уведомление',
        icon: '/static/icons/icon-192x192.png',
        badge: '/static/icons/icon-72x72.png',
        url: '/',
        tournament_id: null
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
        tag: data.tag || 'chess-calendar-notification',
        data: { 
            url: data.url,
            tournament_id: data.tournament_id
        },
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
    
    if (event.data.action === 'syncPendingActions') {
        event.waitUntil(
            self.registration.sync.register('sync-favorites')
                .then(() => self.registration.sync.register('sync-ratings'))
                .then(() => self.registration.sync.register('sync-subscriptions'))
                .catch(error => console.error('[SW] Sync registration failed:', error))
        );
    }
});

// Periodic background sync for refreshing data
self.addEventListener('periodicsync', (event) => {
    if (event.tag === 'refresh-tournaments') {
        event.waitUntil(refreshTournamentData());
    }
});

async function refreshTournamentData() {
    try {
        // Fetch latest tournament data in background
        await fetch('/api/tournaments?limit=50');
        console.log('[SW] Tournament data refreshed in background');
    } catch (error) {
        console.error('[SW] Failed to refresh tournament data:', error);
    }
}

console.log('[SW] Service Worker loaded');