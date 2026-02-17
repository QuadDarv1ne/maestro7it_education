/**
 * Система аналитики и отслеживания
 * Tracking пользовательских действий, A/B тестирование, heatmaps
 */

class AnalyticsTracker {
    constructor(options = {}) {
        this.options = {
            endpoint: options.endpoint || '/api/analytics/track',
            batchSize: options.batchSize || 10,
            flushInterval: options.flushInterval || 30000, // 30 секунд
            enableHeatmap: options.enableHeatmap !== false,
            enableScrollTracking: options.enableScrollTracking !== false,
            enableClickTracking: options.enableClickTracking !== false
        };
        
        this.events = [];
        this.sessionId = this.generateSessionId();
        this.userId = this.getUserId();
        this.pageLoadTime = Date.now();
        this.flushTimer = null;
        
        this.init();
    }

    init() {
        this.trackPageView();
        this.setupEventListeners();
        this.startFlushTimer();
        
        // Отправка при закрытии страницы
        window.addEventListener('beforeunload', () => this.flush(true));
    }

    /**
     * Генерация ID сессии
     */
    generateSessionId() {
        const stored = sessionStorage.getItem('analytics_session_id');
        if (stored) return stored;
        
        const sessionId = `session_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;
        sessionStorage.setItem('analytics_session_id', sessionId);
        return sessionId;
    }

    /**
     * Получение ID пользователя
     */
    getUserId() {
        return document.querySelector('meta[name="user-id"]')?.content || 
               document.body.dataset.userId || 
               'anonymous';
    }

    /**
     * Отслеживание просмотра страницы
     */
    trackPageView() {
        this.track('page_view', {
            url: window.location.href,
            title: document.title,
            referrer: document.referrer,
            screen_width: window.screen.width,
            screen_height: window.screen.height,
            viewport_width: window.innerWidth,
            viewport_height: window.innerHeight
        });
    }

    /**
     * Настройка слушателей событий
     */
    setupEventListeners() {
        if (this.options.enableClickTracking) {
            this.setupClickTracking();
        }
        
        if (this.options.enableScrollTracking) {
            this.setupScrollTracking();
        }
        
        if (this.options.enableHeatmap) {
            this.setupHeatmapTracking();
        }
        
        this.setupTournamentTracking();
        this.setupPerformanceTracking();
    }

    /**
     * Отслеживание кликов
     */
    setupClickTracking() {
        document.addEventListener('click', (e) => {
            const target = e.target.closest('a, button, [data-track]');
            if (!target) return;
            
            const data = {
                element: target.tagName.toLowerCase(),
                text: target.textContent?.trim().substring(0, 100),
                href: target.href || null,
                classes: target.className,
                x: e.clientX,
                y: e.clientY
            };
            
            // Специальное отслеживание для data-track элементов
            if (target.dataset.track) {
                data.track_id = target.dataset.track;
                data.track_category = target.dataset.trackCategory || 'interaction';
            }
            
            this.track('click', data);
        });
    }

    /**
     * Отслеживание прокрутки
     */
    setupScrollTracking() {
        let maxScroll = 0;
        let scrollTimeout;
        
        window.addEventListener('scroll', () => {
            clearTimeout(scrollTimeout);
            
            scrollTimeout = setTimeout(() => {
                const scrollPercent = Math.round(
                    (window.scrollY / (document.documentElement.scrollHeight - window.innerHeight)) * 100
                );
                
                if (scrollPercent > maxScroll) {
                    maxScroll = scrollPercent;
                    
                    // Отслеживаем каждые 25%
                    if (scrollPercent >= 25 && scrollPercent < 50 && maxScroll < 50) {
                        this.track('scroll_depth', { depth: 25 });
                    } else if (scrollPercent >= 50 && scrollPercent < 75 && maxScroll < 75) {
                        this.track('scroll_depth', { depth: 50 });
                    } else if (scrollPercent >= 75 && scrollPercent < 100 && maxScroll < 100) {
                        this.track('scroll_depth', { depth: 75 });
                    } else if (scrollPercent >= 100) {
                        this.track('scroll_depth', { depth: 100 });
                    }
                }
            }, 500);
        });
    }

    /**
     * Отслеживание для heatmap
     */
    setupHeatmapTracking() {
        let moveTimeout;
        const moves = [];
        
        document.addEventListener('mousemove', (e) => {
            clearTimeout(moveTimeout);
            
            moves.push({
                x: e.clientX,
                y: e.clientY,
                time: Date.now()
            });
            
            // Отправляем батчами по 50 движений
            if (moves.length >= 50) {
                this.track('mouse_movement', { moves: moves.splice(0, 50) });
            }
            
            moveTimeout = setTimeout(() => {
                if (moves.length > 0) {
                    this.track('mouse_movement', { moves: moves.splice(0) });
                }
            }, 5000);
        });
    }

    /**
     * Отслеживание действий с турнирами
     */
    setupTournamentTracking() {
        // Просмотр турнира
        document.addEventListener('click', (e) => {
            const tournamentLink = e.target.closest('a[href*="/tournament/"]');
            if (tournamentLink) {
                const tournamentId = tournamentLink.href.match(/\/tournament\/(\d+)/)?.[1];
                if (tournamentId) {
                    this.track('tournament_view', { tournament_id: tournamentId });
                }
            }
        });
        
        // Добавление в избранное
        document.addEventListener('click', (e) => {
            const favoriteBtn = e.target.closest('[data-action="favorite"]');
            if (favoriteBtn) {
                const card = favoriteBtn.closest('[data-tournament-id]');
                if (card) {
                    this.track('tournament_favorite', {
                        tournament_id: card.dataset.tournamentId,
                        action: favoriteBtn.classList.contains('active') ? 'remove' : 'add'
                    });
                }
            }
        });
        
        // Сравнение турниров
        document.addEventListener('click', (e) => {
            const compareBtn = e.target.closest('[data-action="compare"]');
            if (compareBtn) {
                const card = compareBtn.closest('[data-tournament-id]');
                if (card) {
                    this.track('tournament_compare', {
                        tournament_id: card.dataset.tournamentId
                    });
                }
            }
        });
        
        // Поделиться
        document.addEventListener('click', (e) => {
            const shareBtn = e.target.closest('[data-action="share"]');
            if (shareBtn) {
                const card = shareBtn.closest('[data-tournament-id]');
                if (card) {
                    this.track('tournament_share', {
                        tournament_id: card.dataset.tournamentId
                    });
                }
            }
        });
    }

    /**
     * Отслеживание производительности
     */
    setupPerformanceTracking() {
        // Web Vitals
        if ('PerformanceObserver' in window) {
            // LCP (Largest Contentful Paint)
            try {
                const lcpObserver = new PerformanceObserver((list) => {
                    const entries = list.getEntries();
                    const lastEntry = entries[entries.length - 1];
                    this.track('performance_lcp', {
                        value: lastEntry.renderTime || lastEntry.loadTime
                    });
                });
                lcpObserver.observe({ entryTypes: ['largest-contentful-paint'] });
            } catch (e) {}
            
            // FID (First Input Delay)
            try {
                const fidObserver = new PerformanceObserver((list) => {
                    const entries = list.getEntries();
                    entries.forEach(entry => {
                        this.track('performance_fid', {
                            value: entry.processingStart - entry.startTime
                        });
                    });
                });
                fidObserver.observe({ entryTypes: ['first-input'] });
            } catch (e) {}
        }
        
        // Page Load Time
        window.addEventListener('load', () => {
            setTimeout(() => {
                const perfData = performance.timing;
                const pageLoadTime = perfData.loadEventEnd - perfData.navigationStart;
                
                this.track('performance_page_load', {
                    total: pageLoadTime,
                    dns: perfData.domainLookupEnd - perfData.domainLookupStart,
                    tcp: perfData.connectEnd - perfData.connectStart,
                    request: perfData.responseStart - perfData.requestStart,
                    response: perfData.responseEnd - perfData.responseStart,
                    dom: perfData.domComplete - perfData.domLoading
                });
            }, 0);
        });
    }

    /**
     * Отслеживание события
     */
    track(eventName, data = {}) {
        const event = {
            event: eventName,
            timestamp: Date.now(),
            session_id: this.sessionId,
            user_id: this.userId,
            url: window.location.href,
            ...data
        };
        
        this.events.push(event);
        
        // Автоматическая отправка при достижении размера батча
        if (this.events.length >= this.options.batchSize) {
            this.flush();
        }
    }

    /**
     * Отправка событий на сервер
     */
    async flush(sync = false) {
        if (this.events.length === 0) return;
        
        const eventsToSend = [...this.events];
        this.events = [];
        
        const payload = {
            events: eventsToSend,
            session_id: this.sessionId,
            user_id: this.userId
        };
        
        if (sync) {
            // Синхронная отправка при закрытии страницы
            navigator.sendBeacon(this.options.endpoint, JSON.stringify(payload));
        } else {
            // Асинхронная отправка
            try {
                await fetch(this.options.endpoint, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'X-CSRF-Token': this.getCSRFToken()
                    },
                    body: JSON.stringify(payload)
                });
            } catch (error) {
                console.error('Analytics tracking error:', error);
                // Возвращаем события обратно при ошибке
                this.events.unshift(...eventsToSend);
            }
        }
    }

    /**
     * Запуск таймера отправки
     */
    startFlushTimer() {
        this.flushTimer = setInterval(() => {
            this.flush();
        }, this.options.flushInterval);
    }

    /**
     * Получение CSRF токена
     */
    getCSRFToken() {
        return document.querySelector('meta[name="csrf-token"]')?.content || '';
    }

    /**
     * Кастомное событие
     */
    trackCustom(eventName, data = {}) {
        this.track(`custom_${eventName}`, data);
    }

    /**
     * Отслеживание ошибок
     */
    trackError(error, context = {}) {
        this.track('error', {
            message: error.message,
            stack: error.stack,
            ...context
        });
    }

    /**
     * Отслеживание времени на странице
     */
    trackTimeOnPage() {
        const timeSpent = Date.now() - this.pageLoadTime;
        this.track('time_on_page', {
            duration: timeSpent,
            duration_seconds: Math.round(timeSpent / 1000)
        });
    }

    /**
     * Уничтожение трекера
     */
    destroy() {
        if (this.flushTimer) {
            clearInterval(this.flushTimer);
        }
        this.flush(true);
    }
}

// Глобальная обработка ошибок
window.addEventListener('error', (e) => {
    if (window.analyticsTracker) {
        window.analyticsTracker.trackError(e.error || new Error(e.message), {
            filename: e.filename,
            lineno: e.lineno,
            colno: e.colno
        });
    }
});

// Инициализация
document.addEventListener('DOMContentLoaded', () => {
    window.analyticsTracker = new AnalyticsTracker({
        endpoint: '/api/analytics/track',
        batchSize: 10,
        flushInterval: 30000
    });
    
    // Отслеживание времени при уходе
    window.addEventListener('beforeunload', () => {
        if (window.analyticsTracker) {
            window.analyticsTracker.trackTimeOnPage();
        }
    });
});

// Экспорт
if (typeof module !== 'undefined' && module.exports) {
    module.exports = AnalyticsTracker;
}
