/**
 * Chart Helper для Simple HR
 * Обертка для удобной работы с Chart.js
 */
class ChartHelper {
    constructor() {
        this.charts = new Map();
        this.defaultColors = [
            'rgba(102, 126, 234, 0.8)',
            'rgba(118, 75, 162, 0.8)',
            'rgba(40, 167, 69, 0.8)',
            'rgba(23, 162, 184, 0.8)',
            'rgba(255, 193, 7, 0.8)',
            'rgba(220, 53, 69, 0.8)',
            'rgba(108, 117, 125, 0.8)'
        ];
    }

    /**
     * Создать линейную диаграмму
     */
    createLineChart(canvas, data, options = {}) {
        const ctx = this.getContext(canvas);
        
        const config = {
            type: 'line',
            data: {
                labels: data.labels,
                datasets: data.datasets.map((dataset, index) => ({
                    label: dataset.label,
                    data: dataset.data,
                    borderColor: dataset.color || this.defaultColors[index],
                    backgroundColor: dataset.color || this.defaultColors[index],
                    tension: 0.4,
                    fill: dataset.fill !== undefined ? dataset.fill : false,
                    ...dataset
                }))
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        position: 'top',
                    },
                    tooltip: {
                        mode: 'index',
                        intersect: false,
                    }
                },
                scales: {
                    y: {
                        beginAtZero: true
                    }
                },
                ...options
            }
        };

        return this.createChart(canvas.id, ctx, config);
    }

    /**
     * Создать столбчатую диаграмму
     */
    createBarChart(canvas, data, options = {}) {
        const ctx = this.getContext(canvas);
        
        const config = {
            type: 'bar',
            data: {
                labels: data.labels,
                datasets: data.datasets.map((dataset, index) => ({
                    label: dataset.label,
                    data: dataset.data,
                    backgroundColor: dataset.colors || this.defaultColors[index],
                    borderColor: dataset.borderColor || 'rgba(0,0,0,0.1)',
                    borderWidth: 1,
                    ...dataset
                }))
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        position: 'top',
                    }
                },
                scales: {
                    y: {
                        beginAtZero: true
                    }
                },
                ...options
            }
        };

        return this.createChart(canvas.id, ctx, config);
    }

    /**
     * Создать круговую диаграмму
     */
    createPieChart(canvas, data, options = {}) {
        const ctx = this.getContext(canvas);
        
        const config = {
            type: 'pie',
            data: {
                labels: data.labels,
                datasets: [{
                    data: data.values,
                    backgroundColor: data.colors || this.defaultColors,
                    borderColor: 'rgba(255,255,255,0.8)',
                    borderWidth: 2
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        position: 'right',
                    },
                    tooltip: {
                        callbacks: {
                            label: function(context) {
                                const label = context.label || '';
                                const value = context.parsed || 0;
                                const total = context.dataset.data.reduce((a, b) => a + b, 0);
                                const percentage = ((value / total) * 100).toFixed(1);
                                return `${label}: ${value} (${percentage}%)`;
                            }
                        }
                    }
                },
                ...options
            }
        };

        return this.createChart(canvas.id, ctx, config);
    }

    /**
     * Создать кольцевую диаграмму
     */
    createDoughnutChart(canvas, data, options = {}) {
        const chart = this.createPieChart(canvas, data, options);
        chart.config.type = 'doughnut';
        chart.update();
        return chart;
    }

    /**
     * Создать область с накоплением
     */
    createAreaChart(canvas, data, options = {}) {
        const config = {
            fill: true,
            ...options
        };
        
        return this.createLineChart(canvas, data, config);
    }

    /**
     * Создать смешанную диаграмму
     */
    createMixedChart(canvas, data, options = {}) {
        const ctx = this.getContext(canvas);
        
        const config = {
            type: 'bar',
            data: {
                labels: data.labels,
                datasets: data.datasets.map((dataset, index) => ({
                    type: dataset.type || 'bar',
                    label: dataset.label,
                    data: dataset.data,
                    backgroundColor: dataset.color || this.defaultColors[index],
                    borderColor: dataset.color || this.defaultColors[index],
                    yAxisID: dataset.yAxisID || 'y',
                    ...dataset
                }))
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        position: 'top',
                    }
                },
                scales: {
                    y: {
                        type: 'linear',
                        display: true,
                        position: 'left',
                    },
                    y1: {
                        type: 'linear',
                        display: true,
                        position: 'right',
                        grid: {
                            drawOnChartArea: false,
                        },
                    },
                },
                ...options
            }
        };

        return this.createChart(canvas.id, ctx, config);
    }

    /**
     * Обновить данные диаграммы
     */
    updateChart(chartId, newData) {
        const chart = this.charts.get(chartId);
        if (!chart) {
            console.error(`Chart with id ${chartId} not found`);
            return;
        }

        if (newData.labels) {
            chart.data.labels = newData.labels;
        }

        if (newData.datasets) {
            chart.data.datasets.forEach((dataset, index) => {
                if (newData.datasets[index]) {
                    dataset.data = newData.datasets[index].data;
                    if (newData.datasets[index].label) {
                        dataset.label = newData.datasets[index].label;
                    }
                }
            });
        }

        chart.update();
    }

    /**
     * Уничтожить диаграмму
     */
    destroyChart(chartId) {
        const chart = this.charts.get(chartId);
        if (chart) {
            chart.destroy();
            this.charts.delete(chartId);
        }
    }

    /**
     * Экспортировать диаграмму как изображение
     */
    exportChart(chartId, filename = 'chart.png') {
        const chart = this.charts.get(chartId);
        if (!chart) {
            console.error(`Chart with id ${chartId} not found`);
            return;
        }

        const url = chart.toBase64Image();
        const link = document.createElement('a');
        link.download = filename;
        link.href = url;
        link.click();
    }

    /**
     * Получить контекст canvas
     */
    getContext(canvas) {
        if (typeof canvas === 'string') {
            canvas = document.getElementById(canvas);
        }
        return canvas.getContext('2d');
    }

    /**
     * Создать и сохранить диаграмму
     */
    createChart(id, ctx, config) {
        // Уничтожить существующую диаграмму
        this.destroyChart(id);

        // Создать новую диаграмму
        const chart = new Chart(ctx, config);
        this.charts.set(id, chart);
        
        return chart;
    }

    /**
     * Получить диаграмму по ID
     */
    getChart(chartId) {
        return this.charts.get(chartId);
    }

    /**
     * Уничтожить все диаграммы
     */
    destroyAll() {
        this.charts.forEach(chart => chart.destroy());
        this.charts.clear();
    }

    /**
     * Анимировать числовой счетчик
     */
    animateNumber(element, start, end, duration = 1000) {
        const range = end - start;
        const increment = range / (duration / 16);
        let current = start;

        const timer = setInterval(() => {
            current += increment;
            if ((increment > 0 && current >= end) || (increment < 0 && current <= end)) {
                current = end;
                clearInterval(timer);
            }
            element.textContent = Math.floor(current);
        }, 16);
    }

    /**
     * Создать прогресс-бар
     */
    createProgressBar(container, value, max = 100, options = {}) {
        const percentage = (value / max) * 100;
        const color = options.color || 'primary';
        
        container.innerHTML = `
            <div class="progress" style="height: ${options.height || '20px'}">
                <div class="progress-bar bg-${color}" 
                     role="progressbar" 
                     style="width: ${percentage}%" 
                     aria-valuenow="${value}" 
                     aria-valuemin="0" 
                     aria-valuemax="${max}">
                    ${options.showLabel !== false ? `${Math.round(percentage)}%` : ''}
                </div>
            </div>
        `;

        // Анимация
        if (options.animate !== false) {
            const bar = container.querySelector('.progress-bar');
            bar.style.width = '0%';
            setTimeout(() => {
                bar.style.transition = 'width 1s ease-in-out';
                bar.style.width = `${percentage}%`;
            }, 100);
        }
    }

    /**
     * Создать спарклайн (мини-график)
     */
    createSparkline(canvas, data, type = 'line') {
        const ctx = this.getContext(canvas);
        
        const config = {
            type: type,
            data: {
                labels: data.map((_, i) => i),
                datasets: [{
                    data: data,
                    borderColor: 'rgba(102, 126, 234, 1)',
                    backgroundColor: 'rgba(102, 126, 234, 0.1)',
                    borderWidth: 2,
                    pointRadius: 0,
                    tension: 0.4
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        display: false
                    },
                    tooltip: {
                        enabled: false
                    }
                },
                scales: {
                    x: {
                        display: false
                    },
                    y: {
                        display: false
                    }
                },
                elements: {
                    line: {
                        borderWidth: 2
                    }
                }
            }
        };

        return this.createChart(canvas.id, ctx, config);
    }
}

// Глобальный экземпляр
const chartHelper = new ChartHelper();
window.chartHelper = chartHelper;
