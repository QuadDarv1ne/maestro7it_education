// Performance Monitor - мониторинг производительности клиента

class PerformanceMonitor {
    constructor() {
        this.metrics = {
            pageLoadTime: 0,
            domContentLoaded: 0,
            firstPaint: 0,
            firstContentfulPaint: 0,
            largestContentfulPaint: 0,
            timeToInteractive: 0,
            totalBlockingTime: 0,
            cumulativeLayoutShift: 0,
            memoryUsage: 0,
            jsHeapSize: 0
        };
        
        this.enabled = false; // Отключено по умолчанию для производительности
        this.init();
    }

    init() {
        this.loadSettings();
        
        if (this.enabled) {
            this.collectMetrics();
            this.createMonitorWidget();
        }
    }

    loadSettings() {
        const stored = localStorage.getItem('performance_monitor_enabled');
        this.enabled = stored === 'true';
    }

    saveSettings() {
        localStorage.setItem('performance_monitor_enabled', this.enabled);
    }

    collectMetrics() {
        // Ждём полной загрузки страницы
        if (document.readyState === 'complete') {
            this.gatherMetrics();
        } else {
            window.addEventListener('load', () => this.gatherMetrics());
        }
    }

    gatherMetrics() {
        // Navigation Timing API
        const navigation = performance.getEntriesByType('navigation')[0];
        if (navigation) {
            this.metrics.pageLoadTime = navigation.loadEventEnd - navigation.fetchStart;
            this.metrics.domContentLoaded = navigation.domContentLoadedEventEnd - navigation.fetchStart;
        }

        // Paint Timing API
        const paintEntries = performance.getEntriesByType('paint');
        paintEntries.forEach(entry => {
            if (entry.name === 'first-paint') {
                this.metrics.firstPaint = entry.startTime;
            } else if (entry.name === 'first-contentful-paint') {
                this.metrics.firstContentfulPaint = entry.startTime;
            }
        });

        // Largest Contentful Paint
        if ('PerformanceObserver' in window) {
            try {
                const lcpObserver = new PerformanceObserver((list) => {
                    const entries = list.getEntries();
                    const lastEntry = entries[entries.length - 1];
                    this.metrics.largestContentfulPaint = lastEntry.renderTime || lastEntry.loadTime;
                });
                lcpObserver.observe({ entryTypes: ['largest-contentful-paint'] });
            } catch (e) {
                console.warn('LCP observer not supported');
            }
        }

        // Memory Usage (если доступно)
        if (performance.memory) {
            this.metrics.memoryUsage = performance.memory.usedJSHeapSize / 1048576; // MB
            this.metrics.jsHeapSize = performance.memory.totalJSHeapSize / 1048576; // MB
        }

        // Обновляем виджет
        this.updateWidget();
    }

    createMonitorWidget() {
        // Проверяем, не создан ли уже виджет
        if (document.getElementById('performanceMonitor')) return;

        const widget = document.createElement('div');
        widget.id = 'performanceMonitor';
        widget.innerHTML = `
            <style>
                #performanceMonitor {
                    position: fixed;
                    bottom: 30px;
                    right: 100px;
                    background: rgba(0, 0, 0, 0.85);
                    color: #00ff00;
                    padding: 1rem;
                    border-radius: 8px;
                    font-family: 'Courier New', monospace;
                    font-size: 0.75rem;
                    z-index: 9998;
                    min-width: 250px;
                    backdrop-filter: blur(10px);
                    border: 1px solid rgba(0, 255, 0, 0.3);
                }
                
                .perf-header {
                    display: flex;
                    justify-content: space-between;
                    align-items: center;
                    margin-bottom: 0.75rem;
                    padding-bottom: 0.5rem;
                    border-bottom: 1px solid rgba(0, 255, 0, 0.3);
                }
                
                .perf-title {
                    font-weight: bold;
                    color: #00ff00;
                }
                
                .perf-close {
                    background: none;
                    border: none;
                    color: #00ff00;
                    cursor: pointer;
                    font-size: 1rem;
                    padding: 0;
                    line-height: 1;
                }
                
                .perf-metric {
                    display: flex;
                    justify-content: space-between;
                    margin-bottom: 0.5rem;
                    line-height: 1.4;
                }
                
                .perf-label {
                    color: #00ff00;
                }
                
                .perf-value {
                    color: #ffff00;
                    font-weight: bold;
                }
                
                .perf-value.good {
                    color: #00ff00;
                }
                
                .perf-value.warning {
                    color: #ffaa00;
                }
                
                .perf-value.bad {
                    color: #ff0000;
                }
                
                .perf-refresh {
                    margin-top: 0.75rem;
                    padding-top: 0.75rem;
                    border-top: 1px solid rgba(0, 255, 0, 0.3);
                    text-align: center;
                }
                
                .perf-refresh button {
                    background: rgba(0, 255, 0, 0.2);
                    border: 1px solid #00ff00;
                    color: #00ff00;
                    padding: 0.25rem 0.75rem;
                    border-radius: 4px;
                    cursor: pointer;
                    font-family: 'Courier New', monospace;
                    font-size: 0.75rem;
                }
                
                .perf-refresh button:hover {
                    background: rgba(0, 255, 0, 0.3);
                }
                
                @media (max-width: 768px) {
                    #performanceMonitor {
                        bottom: 90px;
                        right: 15px;
                        left: 15px;
                        min-width: auto;
                    }
                }
            </style>
            
            <div class="perf-header">
                <div class="perf-title">⚡ Performance</div>
                <button class="perf-close" onclick="performanceMonitor.toggle()">×</button>
            </div>
            
            <div id="perfMetrics">
                ${this.renderMetrics()}
            </div>
            
            <div class="perf-refresh">
                <button onclick="performanceMonitor.refresh()">🔄 Refresh</button>
            </div>
        `;

        document.body.appendChild(widget);
    }

    renderMetrics() {
        return `
            <div class="perf-metric">
                <span class="perf-label">Page Load:</span>
                <span class="perf-value ${this.getLoadTimeClass(this.metrics.pageLoadTime)}">
                    ${this.formatTime(this.metrics.pageLoadTime)}
                </span>
            </div>
            <div class="perf-metric">
                <span class="perf-label">DOM Ready:</span>
                <span class="perf-value ${this.getLoadTimeClass(this.metrics.domContentLoaded)}">
                    ${this.formatTime(this.metrics.domContentLoaded)}
                </span>
            </div>
            <div class="perf-metric">
                <span class="perf-label">First Paint:</span>
                <span class="perf-value ${this.getLoadTimeClass(this.metrics.firstPaint)}">
                    ${this.formatTime(this.metrics.firstPaint)}
                </span>
            </div>
            <div class="perf-metric">
                <span class="perf-label">FCP:</span>
                <span class="perf-value ${this.getLoadTimeClass(this.metrics.firstContentfulPaint)}">
                    ${this.formatTime(this.metrics.firstContentfulPaint)}
                </span>
            </div>
            ${this.metrics.largestContentfulPaint > 0 ? `
            <div class="perf-metric">
                <span class="perf-label">LCP:</span>
                <span class="perf-value ${this.getLCPClass(this.metrics.largestContentfulPaint)}">
                    ${this.formatTime(this.metrics.largestContentfulPaint)}
                </span>
            </div>
            ` : ''}
            ${this.metrics.memoryUsage > 0 ? `
            <div class="perf-metric">
                <span class="perf-label">Memory:</span>
                <span class="perf-value ${this.getMemoryClass(this.metrics.memoryUsage)}">
                    ${this.metrics.memoryUsage.toFixed(1)} MB
                </span>
            </div>
            ` : ''}
        `;
    }

    updateWidget() {
        const metricsContainer = document.getElementById('perfMetrics');
        if (metricsContainer) {
            metricsContainer.innerHTML = this.renderMetrics();
        }
    }

    formatTime(ms) {
        if (ms === 0) return '0ms';
        if (ms < 1000) return `${Math.round(ms)}ms`;
        return `${(ms / 1000).toFixed(2)}s`;
    }

    getLoadTimeClass(time) {
        if (time === 0) return '';
        if (time < 1000) return 'good';
        if (time < 3000) return 'warning';
        return 'bad';
    }

    getLCPClass(time) {
        if (time === 0) return '';
        if (time < 2500) return 'good';
        if (time < 4000) return 'warning';
        return 'bad';
    }

    getMemoryClass(mb) {
        if (mb < 50) return 'good';
        if (mb < 100) return 'warning';
        return 'bad';
    }

    toggle() {
        this.enabled = !this.enabled;
        this.saveSettings();
        
        const widget = document.getElementById('performanceMonitor');
        if (widget) {
            widget.remove();
        }
        
        if (this.enabled) {
            this.collectMetrics();
            this.createMonitorWidget();
        }
    }

    refresh() {
        this.gatherMetrics();
        
        if (window.toast) {
            window.toast.success('Метрики обновлены');
        }
    }

    getReport() {
        return {
            ...this.metrics,
            timestamp: new Date().toISOString(),
            userAgent: navigator.userAgent,
            connection: navigator.connection ? {
                effectiveType: navigator.connection.effectiveType,
                downlink: navigator.connection.downlink,
                rtt: navigator.connection.rtt
            } : null
        };
    }

    exportReport() {
        const report = this.getReport();
        const json = JSON.stringify(report, null, 2);
        const blob = new Blob([json], { type: 'application/json' });
        const link = document.createElement('a');
        link.href = URL.createObjectURL(blob);
        link.download = `performance_report_${new Date().toISOString().split('T')[0]}.json`;
        link.click();
        
        if (window.toast) {
            window.toast.success('Отчёт экспортирован');
        }
    }
}

// Инициализация
const performanceMonitor = new PerformanceMonitor();
window.performanceMonitor = performanceMonitor;

// Добавляем в меню разработчика (Ctrl+Shift+P)
document.addEventListener('keydown', (e) => {
    if (e.ctrlKey && e.shiftKey && e.key === 'P') {
        e.preventDefault();
        performanceMonitor.toggle();
    }
});
