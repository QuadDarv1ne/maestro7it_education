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
            this.measurePerformance();
        } else {
            window.addEventListener('load', () => this.measurePerformance());
        }
    }

    measurePerformance() {
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
                    padding: 0.75rem 1rem;
                    border-radius: 8px;
                    font-family: 'Courier New', monospace;
                    font-size: 0.75rem;
                    z-index: 9998;
                    backdrop-filter: blur(10px);
                    border: 1px solid rgba(0, 255, 0, 0.3);
                    min-width: 200px;
                    cursor: move;
                }
                
                .perf-header {
                    display: flex;
                    justify-content: space-between;
                    align-items: center;
                    margin-bottom: 0.5rem;
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
                    padding: 0;
                    font-size: 1rem;
                }
                
                .perf-metric {
                    display: flex;
                    justify-content: space-between;
                    margin-bottom: 0.25rem;
                    line-height: 1.4;
                }
                
                .perf-label {
                    color: #00ff00;
                    opacity: 0.8;
                }
                
                .perf-value {
                    color: #00ff00;
                    font-weight: bold;
                }
                
                .perf-value.good {
                    color: #00ff00;
                }
                
                .perf-value.warning {
                    color: #ffff00;
                }
                
                .perf-value.bad {
                    color: #ff0000;
                }
                
                @media (max-width: 768px) {
                    #performanceMonitor {
                        bottom: 90px;
                        right: 15px;
                        font-size: 0.7rem;
                        min-width: 180px;
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
        `;

        document.body.appendChild(widget);
        this.makeDraggable(widget);
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
                <span class="perf-label">FCP:</span>
                <span class="perf-value ${this.getFCPClass(this.metrics.firstContentfulPaint)}">
                    ${this.formatTime(this.metrics.firstContentfulPaint)}
                </span>
            </div>
            <div class="perf-metric">
                <span class="perf-label">LCP:</span>
                <span class="perf-value ${this.getLCPClass(this.metrics.largestContentfulPaint)}">
                    ${this.formatTime(this.metrics.largestContentfulPaint)}
                </span>
            </div>
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

    getFCPClass(time) {
        if (time === 0) return '';
        if (time < 1800) return 'good';
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

    makeDraggable(element) {
        let pos1 = 0, pos2 = 0, pos3 = 0, pos4 = 0;
        
        element.onmousedown = dragMouseDown;

        function dragMouseDown(e) {
            e = e || window.event;
            e.preventDefault();
            pos3 = e.clientX;
            pos4 = e.clientY;
            document.onmouseup = closeDragElement;
            document.onmousemove = elementDrag;
        }

        function elementDrag(e) {
            e = e || window.event;
            e.preventDefault();
            pos1 = pos3 - e.clientX;
            pos2 = pos4 - e.clientY;
            pos3 = e.clientX;
            pos4 = e.clientY;
            element.style.top = (element.offsetTop - pos2) + "px";
            element.style.left = (element.offsetLeft - pos1) + "px";
            element.style.bottom = 'auto';
            element.style.right = 'auto';
        }

        function closeDragElement() {
            document.onmouseup = null;
            document.onmousemove = null;
        }
    }

    toggle() {
        this.enabled = !this.enabled;
        this.saveSettings();
        
        const widget = document.getElementById('performanceMonitor');
        if (this.enabled) {
            if (!widget) {
                this.collectMetrics();
                this.createMonitorWidget();
            }
        } else {
            if (widget) {
                widget.remove();
            }
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
    }
}

// Инициализация
const performanceMonitor = new PerformanceMonitor();
window.performanceMonitor = performanceMonitor;

// Добавляем в меню разработчика (если нужно)
if (window.location.search.includes('debug=true')) {
    performanceMonitor.enabled = true;
    performanceMonitor.collectMetrics();
    performanceMonitor.createMonitorWidget();
}
