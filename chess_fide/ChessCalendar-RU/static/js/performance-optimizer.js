/**
 * Performance Optimizer
 * Оптимизация производительности приложения
 */

class PerformanceOptimizer {
    constructor() {
        this.metrics = {
            fps: [],
            memory: [],
            loadTimes: {},
            interactions: []
        };
        this.init();
    }

    init() {
        this.setupPerformanceObserver();
        this.setupFPSMonitor();
        this.setupMemoryMonitor();
        this.optimizeImages();
        this.optimizeAnimations();
        this.setupIntersectionObserver();
        this.debounceScrollEvents();
    }

    /**
     * Performance Observer для отслеживания метрик
     */
    setupPerformanceObserver() {
        if ('PerformanceObserver' in window) {
            // Отслеживание загрузки ресурсов
            const resourceObserver = new PerformanceObserver((list) => {
                for (const entry of list.getEntries()) {
                    if (entry.duration > 1000) {
                        console.warn(`[Performance] Slow resource: ${entry.name} (${entry.duration}ms)`);
                    }
                    this.metrics.loadTimes[entry.name] = entry.duration;
                }
            });
            resourceObserver.observe({ entryTypes: ['resource'] });

            // Отслеживание Long Tasks
            const longTaskObserver = new PerformanceObserver((list) => {
                for (const entry of list.getEntries()) {
                    console.warn(`[Performance] Long task detected: ${entry.duration}ms`);
                }
            });
            try {
                longTaskObserver.observe({ entryTypes: ['longtask'] });
            } catch (e) {
                // Long tasks не поддерживаются
            }

            // Отслеживание Layout Shifts
            const layoutShiftObserver = new PerformanceObserver((list) => {
                for (const entry of list.getEntries()) {
                    if (entry.value > 0.1) {
                        console.warn(`[Performance] Layout shift: ${entry.value}`);
                    }
                }
            });
            try {
                layoutShiftObserver.observe({ entryTypes: ['layout-shift'] });
            } catch (e) {
                // Layout shifts не поддерживаются
            }
        }
    }

    /**
     * Мониторинг FPS
     */
    setupFPSMonitor() {
        let lastTime = performance.now();
        let frames = 0;

        const measureFPS = () => {
            frames++;
            const currentTime = performance.now();
            
            if (currentTime >= lastTime + 1000) {
                const fps = Math.round((frames * 1000) / (currentTime - lastTime));
                this.metrics.fps.push(fps);
                
                // Сохраняем только последние 60 значений
                if (this.metrics.fps.length > 60) {
                    this.metrics.fps.shift();
                }
                
                // Предупреждение при низком FPS
                if (fps < 30) {
                    console.warn(`[Performance] Low FPS detected: ${fps}`);
                    this.reducePerfImpact();
                }
                
                frames = 0;
                lastTime = currentTime;
            }
            
            requestAnimationFrame(measureFPS);
        };

        requestAnimationFrame(measureFPS);
    }

    /**
     * Мониторинг памяти
     */
    setupMemoryMonitor() {
        if (performance.memory) {
            setInterval(() => {
                const memoryUsage = {
                    used: Math.round(performance.memory.usedJSHeapSize / 1048576),
                    total: Math.round(performance.memory.totalJSHeapSize / 1048576),
                    limit: Math.round(performance.memory.jsHeapSizeLimit / 1048576)
                };
                
                this.metrics.memory.push(memoryUsage);
                
                // Сохраняем только последние 60 значений
                if (this.metrics.memory.length > 60) {
                    this.metrics.memory.shift();
                }
                
                // Предупреждение при высоком использовании памяти
                const usagePercent = (memoryUsage.used / memoryUsage.limit) * 100;
                if (usagePercent > 80) {
                    console.warn(`[Performance] High memory usage: ${usagePercent.toFixed(1)}%`);
                    this.cleanupMemory();
                }
            }, 5000);
        }
    }

    /**
     * Оптимизация изображений
     */
    optimizeImages() {
        // Ленивая загрузка изображений
        if ('loading' in HTMLImageElement.prototype) {
            document.querySelectorAll('img[data-src]').forEach(img => {
                img.src = img.dataset.src;
                img.removeAttribute('data-src');
            });
        } else {
            // Fallback для старых браузеров
            const imageObserver = new IntersectionObserver((entries) => {
                entries.forEach(entry => {
                    if (entry.isIntersecting) {
                        const img = entry.target;
                        img.src = img.dataset.src;
                        img.removeAttribute('data-src');
                        imageObserver.unobserve(img);
                    }
                });
            });

            document.querySelectorAll('img[data-src]').forEach(img => {
                imageObserver.observe(img);
            });
        }

        // WebP поддержка
        this.checkWebPSupport();
    }

    /**
     * Проверка поддержки WebP
     */
    async checkWebPSupport() {
        const webpData = 'data:image/webp;base64,UklGRiQAAABXRUJQVlA4IBgAAAAwAQCdASoBAAEAAwA0JaQAA3AA/vuUAAA=';
        
        try {
            const img = new Image();
            img.src = webpData;
            await img.decode();
            document.documentElement.classList.add('webp-supported');
        } catch (e) {
            document.documentElement.classList.add('webp-not-supported');
        }
    }

    /**
     * Оптимизация анимаций
     */
    optimizeAnimations() {
        // Отключить анимации при низкой производительности
        const prefersReducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)');
        
        if (prefersReducedMotion.matches) {
            document.documentElement.classList.add('reduce-motion');
        }

        prefersReducedMotion.addEventListener('change', (e) => {
            if (e.matches) {
                document.documentElement.classList.add('reduce-motion');
            } else {
                document.documentElement.classList.remove('reduce-motion');
            }
        });

        // Использовать CSS containment для изоляции
        document.querySelectorAll('.tournament-card').forEach(card => {
            card.style.contain = 'layout style paint';
        });
    }

    /**
     * Intersection Observer для видимых элементов
     */
    setupIntersectionObserver() {
        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    entry.target.classList.add('is-visible');
                } else {
                    entry.target.classList.remove('is-visible');
                }
            });
        }, {
            rootMargin: '50px'
        });

        document.querySelectorAll('.tournament-card, .feature-card').forEach(el => {
            observer.observe(el);
        });
    }

    /**
     * Debounce для scroll событий
     */
    debounceScrollEvents() {
        let scrollTimeout;
        let lastScrollY = window.scrollY;

        window.addEventListener('scroll', () => {
            clearTimeout(scrollTimeout);
            
            scrollTimeout = setTimeout(() => {
                const currentScrollY = window.scrollY;
                const scrollDelta = Math.abs(currentScrollY - lastScrollY);
                
                // Отслеживаем только значительные скроллы
                if (scrollDelta > 50) {
                    this.onSignificantScroll(currentScrollY, lastScrollY);
                    lastScrollY = currentScrollY;
                }
            }, 100);
        }, { passive: true });
    }

    /**
     * Обработка значительного скролла
     */
    onSignificantScroll(currentY, lastY) {
        // Можно добавить логику для оптимизации при скролле
        if (window.analyticsTracker) {
            window.analyticsTracker.track('scroll', {
                position: currentY,
                direction: currentY > lastY ? 'down' : 'up'
            });
        }
    }

    /**
     * Снижение влияния на производительность
     */
    reducePerfImpact() {
        // Отключить сложные анимации
        document.documentElement.classList.add('low-performance-mode');
        
        // Уменьшить частоту обновлений
        if (window.tournamentVisualizations) {
            window.tournamentVisualizations.setUpdateInterval(5000);
        }

        console.log('[Performance] Reduced performance impact mode enabled');
    }

    /**
     * Очистка памяти
     */
    cleanupMemory() {
        // Очистить старые кэши
        if (window.tournamentCache) {
            window.tournamentCache.cleanup();
        }

        // Удалить неиспользуемые элементы DOM
        document.querySelectorAll('.tournament-card:not(.is-visible)').forEach(card => {
            // Можно удалить тяжелые элементы из невидимых карточек
            const images = card.querySelectorAll('img');
            images.forEach(img => {
                if (img.src && !img.dataset.originalSrc) {
                    img.dataset.originalSrc = img.src;
                    img.src = '';
                }
            });
        });

        console.log('[Performance] Memory cleanup performed');
    }

    /**
     * Получить метрики производительности
     */
    getMetrics() {
        const avgFPS = this.metrics.fps.length > 0
            ? Math.round(this.metrics.fps.reduce((a, b) => a + b, 0) / this.metrics.fps.length)
            : 0;

        const latestMemory = this.metrics.memory[this.metrics.memory.length - 1] || {
            used: 0,
            total: 0,
            limit: 0
        };

        return {
            fps: {
                current: this.metrics.fps[this.metrics.fps.length - 1] || 0,
                average: avgFPS,
                min: Math.min(...this.metrics.fps) || 0,
                max: Math.max(...this.metrics.fps) || 0
            },
            memory: latestMemory,
            loadTimes: this.metrics.loadTimes,
            performance: this.getPerformanceScore()
        };
    }

    /**
     * Рассчитать общий балл производительности
     */
    getPerformanceScore() {
        const avgFPS = this.metrics.fps.length > 0
            ? this.metrics.fps.reduce((a, b) => a + b, 0) / this.metrics.fps.length
            : 60;

        const fpsScore = Math.min((avgFPS / 60) * 100, 100);
        
        const latestMemory = this.metrics.memory[this.metrics.memory.length - 1];
        const memoryScore = latestMemory
            ? Math.max(100 - ((latestMemory.used / latestMemory.limit) * 100), 0)
            : 100;

        const totalScore = Math.round((fpsScore * 0.6) + (memoryScore * 0.4));

        return {
            total: totalScore,
            fps: Math.round(fpsScore),
            memory: Math.round(memoryScore),
            grade: this.getGrade(totalScore)
        };
    }

    /**
     * Получить оценку производительности
     */
    getGrade(score) {
        if (score >= 90) return 'A';
        if (score >= 80) return 'B';
        if (score >= 70) return 'C';
        if (score >= 60) return 'D';
        return 'F';
    }

    /**
     * Показать панель метрик (для разработки)
     */
    showMetricsPanel() {
        const panel = document.createElement('div');
        panel.id = 'performance-metrics-panel';
        panel.style.cssText = `
            position: fixed;
            bottom: 20px;
            right: 20px;
            background: rgba(0, 0, 0, 0.9);
            color: white;
            padding: 15px;
            border-radius: 8px;
            font-family: monospace;
            font-size: 12px;
            z-index: 10000;
            min-width: 200px;
        `;

        const updatePanel = () => {
            const metrics = this.getMetrics();
            panel.innerHTML = `
                <div style="font-weight: bold; margin-bottom: 10px;">Performance Metrics</div>
                <div>FPS: ${metrics.fps.current} (avg: ${metrics.fps.average})</div>
                <div>Memory: ${metrics.memory.used}MB / ${metrics.memory.limit}MB</div>
                <div>Score: ${metrics.performance.total} (${metrics.performance.grade})</div>
            `;
        };

        document.body.appendChild(panel);
        setInterval(updatePanel, 1000);
        updatePanel();
    }
}

// CSS для режима низкой производительности
const style = document.createElement('style');
style.textContent = `
    .low-performance-mode * {
        animation-duration: 0.1s !important;
        transition-duration: 0.1s !important;
    }

    .reduce-motion * {
        animation: none !important;
        transition: none !important;
    }

    .webp-supported img[data-webp] {
        content: attr(data-webp);
    }
`;
document.head.appendChild(style);

// Инициализация
document.addEventListener('DOMContentLoaded', () => {
    window.performanceOptimizer = new PerformanceOptimizer();
    console.log('[Performance Optimizer] Initialized');

    // Показать панель метрик в режиме разработки
    if (window.location.hostname === 'localhost' || window.location.search.includes('debug=true')) {
        // window.performanceOptimizer.showMetricsPanel();
    }
});

// Экспорт
if (typeof module !== 'undefined' && module.exports) {
    module.exports = PerformanceOptimizer;
}
