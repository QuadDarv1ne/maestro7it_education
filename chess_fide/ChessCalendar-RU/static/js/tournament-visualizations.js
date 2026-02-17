/**
 * Визуализация данных турниров
 * Графики, диаграммы, статистика
 */

class TournamentVisualizations {
    constructor() {
        this.charts = new Map();
        this.init();
    }

    init() {
        this.createStatsCards();
        this.setupChartContainers();
    }

    /**
     * Создание карточек статистики
     */
    createStatsCards() {
        const statsContainer = document.querySelector('.stats-container');
        if (!statsContainer) return;

        // Получаем данные из data-атрибутов или API
        this.loadStats().then(stats => {
            this.renderStatsCards(stats, statsContainer);
        });
    }

    /**
     * Загрузка статистики
     */
    async loadStats() {
        try {
            const response = await fetch('/api/tournaments/statistics');
            if (!response.ok) throw new Error('Failed to load stats');
            return await response.json();
        } catch (error) {
            console.error('Error loading stats:', error);
            return this.getDefaultStats();
        }
    }

    /**
     * Статистика по умолчанию
     */
    getDefaultStats() {
        return {
            total: 0,
            upcoming: 0,
            ongoing: 0,
            completed: 0,
            by_category: {},
            by_location: {}
        };
    }

    /**
     * Отрисовка карточек статистики
     */
    renderStatsCards(stats, container) {
        const cards = [
            {
                title: 'Всего турниров',
                value: stats.total || 0,
                icon: 'trophy',
                color: 'primary',
                trend: '+12%'
            },
            {
                title: 'Предстоящие',
                value: stats.upcoming || 0,
                icon: 'calendar-check',
                color: 'info',
                trend: '+5%'
            },
            {
                title: 'Идут сейчас',
                value: stats.ongoing || 0,
                icon: 'play-circle',
                color: 'warning',
                trend: '0%'
            },
            {
                title: 'Завершенные',
                value: stats.completed || 0,
                icon: 'check-circle',
                color: 'success',
                trend: '+8%'
            }
        ];

        container.innerHTML = cards.map(card => `
            <div class="stat-card stat-card-${card.color}">
                <div class="stat-card-icon">
                    <i class="bi bi-${card.icon}"></i>
                </div>
                <div class="stat-card-content">
                    <div class="stat-card-title">${card.title}</div>
                    <div class="stat-card-value">${card.value}</div>
                    <div class="stat-card-trend ${card.trend.startsWith('+') ? 'positive' : 'negative'}">
                        <i class="bi bi-arrow-${card.trend.startsWith('+') ? 'up' : 'down'}"></i>
                        ${card.trend}
                    </div>
                </div>
            </div>
        `).join('');
    }

    /**
     * Настройка контейнеров для графиков
     */
    setupChartContainers() {
        // График по категориям
        const categoryChart = document.getElementById('categoryChart');
        if (categoryChart) {
            this.createCategoryChart(categoryChart);
        }

        // График по месяцам
        const monthlyChart = document.getElementById('monthlyChart');
        if (monthlyChart) {
            this.createMonthlyChart(monthlyChart);
        }

        // График по локациям
        const locationChart = document.getElementById('locationChart');
        if (locationChart) {
            this.createLocationChart(locationChart);
        }
    }

    /**
     * График по категориям (Pie Chart)
     */
    async createCategoryChart(container) {
        const data = await this.loadCategoryData();
        
        const canvas = document.createElement('canvas');
        container.appendChild(canvas);

        // Простая реализация без библиотек
        this.drawPieChart(canvas, data, {
            title: 'Турниры по категориям',
            colors: ['#3b82f6', '#10b981', '#f59e0b', '#ef4444', '#8b5cf6']
        });
    }

    /**
     * График по месяцам (Bar Chart)
     */
    async createMonthlyChart(container) {
        const data = await this.loadMonthlyData();
        
        const canvas = document.createElement('canvas');
        container.appendChild(canvas);

        this.drawBarChart(canvas, data, {
            title: 'Турниры по месяцам',
            color: '#3b82f6'
        });
    }

    /**
     * График по локациям (Horizontal Bar)
     */
    async createLocationChart(container) {
        const data = await this.loadLocationData();
        
        const canvas = document.createElement('canvas');
        container.appendChild(canvas);

        this.drawHorizontalBarChart(canvas, data, {
            title: 'Топ локаций',
            color: '#10b981'
        });
    }

    /**
     * Отрисовка круговой диаграммы
     */
    drawPieChart(canvas, data, options = {}) {
        const ctx = canvas.getContext('2d');
        const width = canvas.width = canvas.offsetWidth * 2;
        const height = canvas.height = canvas.offsetHeight * 2;
        
        ctx.scale(2, 2);
        
        const centerX = width / 4;
        const centerY = height / 4;
        const radius = Math.min(width, height) / 4 - 40;
        
        let currentAngle = -Math.PI / 2;
        const total = data.reduce((sum, item) => sum + item.value, 0);
        
        data.forEach((item, index) => {
            const sliceAngle = (item.value / total) * 2 * Math.PI;
            
            // Рисуем сектор
            ctx.beginPath();
            ctx.moveTo(centerX, centerY);
            ctx.arc(centerX, centerY, radius, currentAngle, currentAngle + sliceAngle);
            ctx.closePath();
            
            ctx.fillStyle = options.colors[index % options.colors.length];
            ctx.fill();
            
            // Рисуем границу
            ctx.strokeStyle = '#fff';
            ctx.lineWidth = 2;
            ctx.stroke();
            
            // Рисуем метку
            const labelAngle = currentAngle + sliceAngle / 2;
            const labelX = centerX + Math.cos(labelAngle) * (radius + 30);
            const labelY = centerY + Math.sin(labelAngle) * (radius + 30);
            
            ctx.fillStyle = '#374151';
            ctx.font = '12px Inter, sans-serif';
            ctx.textAlign = 'center';
            ctx.fillText(`${item.label} (${item.value})`, labelX, labelY);
            
            currentAngle += sliceAngle;
        });
        
        // Заголовок
        if (options.title) {
            ctx.fillStyle = '#1f2937';
            ctx.font = 'bold 16px Inter, sans-serif';
            ctx.textAlign = 'center';
            ctx.fillText(options.title, centerX, 20);
        }
    }

    /**
     * Отрисовка столбчатой диаграммы
     */
    drawBarChart(canvas, data, options = {}) {
        const ctx = canvas.getContext('2d');
        const width = canvas.width = canvas.offsetWidth * 2;
        const height = canvas.height = canvas.offsetHeight * 2;
        
        ctx.scale(2, 2);
        
        const padding = 40;
        const chartWidth = width / 2 - padding * 2;
        const chartHeight = height / 2 - padding * 2;
        
        const maxValue = Math.max(...data.map(d => d.value));
        const barWidth = chartWidth / data.length - 10;
        
        data.forEach((item, index) => {
            const barHeight = (item.value / maxValue) * chartHeight;
            const x = padding + index * (barWidth + 10);
            const y = height / 2 - padding - barHeight;
            
            // Рисуем столбец
            ctx.fillStyle = options.color;
            ctx.fillRect(x, y, barWidth, barHeight);
            
            // Рисуем значение
            ctx.fillStyle = '#374151';
            ctx.font = '12px Inter, sans-serif';
            ctx.textAlign = 'center';
            ctx.fillText(item.value, x + barWidth / 2, y - 5);
            
            // Рисуем метку
            ctx.save();
            ctx.translate(x + barWidth / 2, height / 2 - padding + 15);
            ctx.rotate(-Math.PI / 4);
            ctx.textAlign = 'right';
            ctx.fillText(item.label, 0, 0);
            ctx.restore();
        });
        
        // Заголовок
        if (options.title) {
            ctx.fillStyle = '#1f2937';
            ctx.font = 'bold 16px Inter, sans-serif';
            ctx.textAlign = 'center';
            ctx.fillText(options.title, width / 4, 20);
        }
    }

    /**
     * Отрисовка горизонтальной столбчатой диаграммы
     */
    drawHorizontalBarChart(canvas, data, options = {}) {
        const ctx = canvas.getContext('2d');
        const width = canvas.width = canvas.offsetWidth * 2;
        const height = canvas.height = canvas.offsetHeight * 2;
        
        ctx.scale(2, 2);
        
        const padding = 40;
        const chartWidth = width / 2 - padding * 2 - 100;
        const chartHeight = height / 2 - padding * 2;
        
        const maxValue = Math.max(...data.map(d => d.value));
        const barHeight = chartHeight / data.length - 10;
        
        data.forEach((item, index) => {
            const barWidth = (item.value / maxValue) * chartWidth;
            const x = padding + 100;
            const y = padding + index * (barHeight + 10);
            
            // Рисуем столбец
            ctx.fillStyle = options.color;
            ctx.fillRect(x, y, barWidth, barHeight);
            
            // Рисуем метку
            ctx.fillStyle = '#374151';
            ctx.font = '12px Inter, sans-serif';
            ctx.textAlign = 'right';
            ctx.fillText(item.label, x - 10, y + barHeight / 2 + 4);
            
            // Рисуем значение
            ctx.textAlign = 'left';
            ctx.fillText(item.value, x + barWidth + 5, y + barHeight / 2 + 4);
        });
        
        // Заголовок
        if (options.title) {
            ctx.fillStyle = '#1f2937';
            ctx.font = 'bold 16px Inter, sans-serif';
            ctx.textAlign = 'center';
            ctx.fillText(options.title, width / 4, 20);
        }
    }

    /**
     * Загрузка данных по категориям
     */
    async loadCategoryData() {
        try {
            const response = await fetch('/api/tournaments/statistics');
            const data = await response.json();
            
            return Object.entries(data.by_category || {}).map(([label, value]) => ({
                label,
                value
            }));
        } catch (error) {
            return [
                { label: 'International', value: 45 },
                { label: 'National', value: 120 },
                { label: 'Regional', value: 85 },
                { label: 'Local', value: 60 }
            ];
        }
    }

    /**
     * Загрузка данных по месяцам
     */
    async loadMonthlyData() {
        const months = ['Янв', 'Фев', 'Мар', 'Апр', 'Май', 'Июн', 'Июл', 'Авг', 'Сен', 'Окт', 'Ноя', 'Дек'];
        
        // Здесь должен быть реальный запрос к API
        return months.map((label, index) => ({
            label,
            value: Math.floor(Math.random() * 50) + 10
        }));
    }

    /**
     * Загрузка данных по локациям
     */
    async loadLocationData() {
        try {
            const response = await fetch('/api/tournaments/statistics');
            const data = await response.json();
            
            const locations = Object.entries(data.by_location || {})
                .sort((a, b) => b[1] - a[1])
                .slice(0, 10);
            
            return locations.map(([label, value]) => ({ label, value }));
        } catch (error) {
            return [
                { label: 'Москва', value: 85 },
                { label: 'Санкт-Петербург', value: 62 },
                { label: 'Казань', value: 45 },
                { label: 'Екатеринбург', value: 38 },
                { label: 'Новосибирск', value: 32 }
            ];
        }
    }

    /**
     * Обновление графиков
     */
    async refresh() {
        this.charts.forEach(chart => chart.destroy());
        this.charts.clear();
        this.setupChartContainers();
    }
}

// CSS стили
const style = document.createElement('style');
style.textContent = `
    .stats-container {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
        gap: 1.5rem;
        margin-bottom: 2rem;
    }

    .stat-card {
        display: flex;
        align-items: center;
        gap: 1rem;
        padding: 1.5rem;
        background: white;
        border-radius: 1rem;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
        transition: all 0.3s ease;
    }

    .stat-card:hover {
        transform: translateY(-4px);
        box-shadow: 0 8px 16px rgba(0, 0, 0, 0.12);
    }

    .stat-card-icon {
        width: 60px;
        height: 60px;
        display: flex;
        align-items: center;
        justify-content: center;
        border-radius: 1rem;
        font-size: 1.75rem;
    }

    .stat-card-primary .stat-card-icon {
        background: linear-gradient(135deg, #3b82f6, #2563eb);
        color: white;
    }

    .stat-card-info .stat-card-icon {
        background: linear-gradient(135deg, #06b6d4, #0891b2);
        color: white;
    }

    .stat-card-warning .stat-card-icon {
        background: linear-gradient(135deg, #f59e0b, #d97706);
        color: white;
    }

    .stat-card-success .stat-card-icon {
        background: linear-gradient(135deg, #10b981, #059669);
        color: white;
    }

    .stat-card-content {
        flex: 1;
    }

    .stat-card-title {
        font-size: 0.875rem;
        color: #6b7280;
        margin-bottom: 0.25rem;
    }

    .stat-card-value {
        font-size: 2rem;
        font-weight: 700;
        color: #1f2937;
        line-height: 1;
        margin-bottom: 0.5rem;
    }

    .stat-card-trend {
        display: flex;
        align-items: center;
        gap: 0.25rem;
        font-size: 0.875rem;
        font-weight: 600;
    }

    .stat-card-trend.positive {
        color: #10b981;
    }

    .stat-card-trend.negative {
        color: #ef4444;
    }

    .chart-container {
        background: white;
        border-radius: 1rem;
        padding: 1.5rem;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
        margin-bottom: 1.5rem;
    }

    .chart-container canvas {
        width: 100%;
        height: 300px;
    }

    @media (max-width: 768px) {
        .stats-container {
            grid-template-columns: 1fr;
        }

        .stat-card-value {
            font-size: 1.5rem;
        }
    }
`;
document.head.appendChild(style);

// Инициализация
document.addEventListener('DOMContentLoaded', () => {
    window.tournamentVisualizations = new TournamentVisualizations();
});

// Экспорт
if (typeof module !== 'undefined' && module.exports) {
    module.exports = TournamentVisualizations;
}
