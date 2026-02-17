/**
 * Тестовый скрипт для проверки работы аналитики
 * Генерирует тестовые события для демонстрации
 */

class AnalyticsTest {
    constructor() {
        this.testEvents = [
            { type: 'page_view', data: { url: '/tournaments', title: 'Турниры' } },
            { type: 'tournament_view', data: { tournament_id: 1 } },
            { type: 'tournament_favorite', data: { tournament_id: 1, action: 'add' } },
            { type: 'tournament_share', data: { tournament_id: 1, platform: 'telegram' } },
            { type: 'click', data: { element: 'filter-button', text: 'Фильтры' } },
            { type: 'scroll_depth', data: { depth: 50 } }
        ];
    }

    /**
     * Генерация случайного события
     */
    generateRandomEvent() {
        const event = this.testEvents[Math.floor(Math.random() * this.testEvents.length)];
        
        if (window.analyticsTracker) {
            window.analyticsTracker.track(event.type, event.data);
            console.log('[Analytics Test] Generated event:', event.type, event.data);
        } else {
            console.warn('[Analytics Test] Analytics tracker not found');
        }
    }

    /**
     * Генерация серии событий
     */
    generateEventBatch(count = 10) {
        console.log(`[Analytics Test] Generating ${count} test events...`);
        
        for (let i = 0; i < count; i++) {
            setTimeout(() => {
                this.generateRandomEvent();
            }, i * 500); // 500ms между событиями
        }
    }

    /**
     * Симуляция пользовательской сессии
     */
    simulateUserSession() {
        console.log('[Analytics Test] Simulating user session...');
        
        const sessionEvents = [
            { delay: 0, type: 'page_view', data: { url: '/', title: 'Главная' } },
            { delay: 2000, type: 'scroll_depth', data: { depth: 25 } },
            { delay: 5000, type: 'click', data: { element: 'tournament-card', text: 'Чемпионат России' } },
            { delay: 6000, type: 'tournament_view', data: { tournament_id: 1 } },
            { delay: 8000, type: 'scroll_depth', data: { depth: 50 } },
            { delay: 10000, type: 'tournament_favorite', data: { tournament_id: 1, action: 'add' } },
            { delay: 12000, type: 'tournament_share', data: { tournament_id: 1, platform: 'vk' } },
            { delay: 15000, type: 'scroll_depth', data: { depth: 100 } }
        ];

        sessionEvents.forEach(event => {
            setTimeout(() => {
                if (window.analyticsTracker) {
                    window.analyticsTracker.track(event.type, event.data);
                    console.log('[Analytics Test] Session event:', event.type);
                }
            }, event.delay);
        });

        console.log('[Analytics Test] Session simulation started (15 seconds)');
    }

    /**
     * Тест производительности
     */
    performanceTest(eventCount = 100) {
        console.log(`[Analytics Test] Performance test with ${eventCount} events...`);
        
        const startTime = performance.now();
        
        for (let i = 0; i < eventCount; i++) {
            this.generateRandomEvent();
        }
        
        const endTime = performance.now();
        const duration = endTime - startTime;
        
        console.log(`[Analytics Test] Generated ${eventCount} events in ${duration.toFixed(2)}ms`);
        console.log(`[Analytics Test] Average: ${(duration / eventCount).toFixed(2)}ms per event`);
    }

    /**
     * Проверка отправки на сервер
     */
    async testServerTracking() {
        console.log('[Analytics Test] Testing server tracking...');
        
        if (!window.analyticsTracker) {
            console.error('[Analytics Test] Analytics tracker not found');
            return;
        }

        // Генерируем несколько событий
        this.generateEventBatch(5);

        // Принудительная отправка
        setTimeout(async () => {
            console.log('[Analytics Test] Flushing events to server...');
            await window.analyticsTracker.flush();
            console.log('[Analytics Test] Events sent to server');
        }, 3000);
    }

    /**
     * Показать статистику трекера
     */
    showTrackerStats() {
        if (!window.analyticsTracker) {
            console.error('[Analytics Test] Analytics tracker not found');
            return;
        }

        console.log('[Analytics Test] Tracker Statistics:');
        console.log('- Session ID:', window.analyticsTracker.sessionId);
        console.log('- User ID:', window.analyticsTracker.userId);
        console.log('- Pending events:', window.analyticsTracker.events.length);
        console.log('- Page load time:', Date.now() - window.analyticsTracker.pageLoadTime, 'ms');
    }
}

// Создаем глобальный экземпляр для тестирования
window.analyticsTest = new AnalyticsTest();

// Добавляем команды в консоль
console.log('%c[Analytics Test] Available commands:', 'color: #2563eb; font-weight: bold;');
console.log('- analyticsTest.generateRandomEvent() - Generate single random event');
console.log('- analyticsTest.generateEventBatch(10) - Generate batch of events');
console.log('- analyticsTest.simulateUserSession() - Simulate user session');
console.log('- analyticsTest.performanceTest(100) - Performance test');
console.log('- analyticsTest.testServerTracking() - Test server tracking');
console.log('- analyticsTest.showTrackerStats() - Show tracker statistics');

// Автоматический тест при загрузке (только в dev режиме)
if (window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1') {
    document.addEventListener('DOMContentLoaded', () => {
        setTimeout(() => {
            console.log('[Analytics Test] Running automatic test...');
            window.analyticsTest.generateEventBatch(3);
        }, 2000);
    });
}
