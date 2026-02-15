// Service Worker для ChessCalendar-RU PWA
const CACHE_NAME = 'chess-calendar-v2.0';
const urlsToCache = [
    '/',
    '/static/css/style.css',
    '/static/manifest.json',
    'https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css',
    'https://cdn.jsdelivr.net/npm/bootstrap-icons@1.8.1/font/bootstrap-icons.css',
    'https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/js/bootstrap.bundle.min.js',
    '/static/icons/icon-192x192.png',
    '/static/icons/icon-512x512.png'
];

// Установка Service Worker
self.addEventListener('install', function(event) {
    event.waitUntil(
        caches.open(CACHE_NAME)
            .then(function(cache) {
                console.log('Opened cache');
                return cache.addAll(urlsToCache);
            })
    );
});

// Перехват сетевых запросов
self.addEventListener('fetch', function(event) {
    // Кэшируем только GET запросы
    if (event.request.method === 'GET') {
        event.respondWith(
            caches.match(event.request)
                .then(function(response) {
                    // Возвращаем кэшированный ресурс
                    if (response) {
                        return response;
                    }
                    
                    // Пытаемся получить ответ из сети
                    return fetch(event.request).then(function(fetchResponse) {
                        // Проверяем валидность ответа
                        if (!fetchResponse || fetchResponse.status !== 200 || fetchResponse.type !== 'basic') {
                            return fetchResponse;
                        }
                        
                        // Клонируем ответ для помещения в кэш
                        var responseToCache = fetchResponse.clone();
                        
                        caches.open(CACHE_NAME)
                            .then(function(cache) {
                                cache.put(event.request, responseToCache);
                            });
                        
                        return fetchResponse;
                    }).catch(function() {
                        // Если это HTML запрос, возвращаем заглушку
                        if (event.request.destination === 'document') {
                            return caches.match('/');
                        }
                    });
                })
        );
    }
});

// Активация Service Worker
self.addEventListener('activate', function(event) {
    event.waitUntil(
        caches.keys().then(function(cacheNames) {
            return Promise.all(
                cacheNames.map(function(cacheName) {
                    if (cacheName !== CACHE_NAME) {
                        console.log('Deleting old cache:', cacheName);
                        return caches.delete(cacheName);
                    }
                })
            );
        })
    );
});

// Обработка push-уведомлений
self.addEventListener('push', function(event) {
    if (event.data) {
        const data = event.data.json();
        const title = data.title || 'ChessCalendar-RU';
        const options = {
            body: data.body || 'Новое уведомление',
            icon: '/static/icons/icon-192x192.png',
            badge: '/static/icons/badge-72x72.png',
            tag: 'chess-calendar-notification',
            data: data.url || '/'
        };
        
        event.waitUntil(
            self.registration.showNotification(title, options)
        );
    }
});

// Обработка кликов по уведомлениям
self.addEventListener('notificationclick', function(event) {
    event.notification.close();
    
    event.waitUntil(
        clients.openWindow(event.notification.data || '/')
    );
});