// User Statistics - продвинутая статистика пользователя

class UserStats {
    constructor() {
        this.storageKey = 'user_statistics';
        this.init();
    }

    init() {
        this.loadStats();
        this.trackPageView();
        this.createStatsWidget();
    }

    loadStats() {
        const stored = localStorage.getItem(this.storageKey);
        this.stats = stored ? JSON.parse(stored) : {
            pageViews: 0,
            tournamentsViewed: 0,
            searchesPerformed: 0,
            filtersUsed: 0,
            favoritesAdded: 0,
            comparisonsUsed: 0,
            exportsUsed: 0,
            timeSpent: 0,
            lastVisit: null,
            firstVisit: new Date().toISOString(),
            visitDays: [],
            mostViewedCategories: {},
            mostViewedLocations: {},
            activityByHour: Array(24).fill(0),
            activityByDay: Array(7).fill(0)
        };
    }

    saveStats() {
        localStorage.setItem(this.storageKey, JSON.stringify(this.stats));
    }

    trackPageView() {
        this.stats.pageViews++;
        this.stats.lastVisit = new Date().toISOString();
        
        // Отслеживаем день посещения
        const today = new Date().toDateString();
        if (!this.stats.visitDays.includes(today)) {
            this.stats.visitDays.push(today);
        }
        
        // Отслеживаем активность по часам
        const hour = new Date().getHours();
        this.stats.activityByHour[hour]++;
        
        // Отслеживаем активность по дням недели
        const day = new Date().getDay();
        this.stats.activityByDay[day]++;
        
        this.saveStats();
    }

    trackTournamentView(category, location) {
        this.stats.tournamentsViewed++;
        
        // Отслеживаем категории
        if (category) {
            this.stats.mostViewedCategories[category] = 
                (this.stats.mostViewedCategories[category] || 0) + 1;
        }
        
        // Отслеживаем локации
        if (location) {
            this.stats.mostViewedLocations[location] = 
                (this.stats.mostViewedLocations[location] || 0) + 1;
        }
        
        this.saveStats();
    }

    trackAction(action) {
        const actionMap = {
            'search': 'searchesPerformed',
            'filter': 'filtersUsed',
            'favorite': 'favoritesAdded',
            'comparison': 'comparisonsUsed',
            'export': 'exportsUsed'
        };
        
        const statKey = actionMap[action];
        if (statKey) {
            this.stats[statKey]++;
            this.saveStats();
        }
    }

    createStatsWidget() {
        // Создаём кнопку для открытия статистики
        this.createStatsButton();
    }

    createStatsButton() {
        // Проверяем, не создана ли уже кнопка
        if (document.getElementById('statsButton')) return;
        
        const button = document.createElement('li');
        button.id = 'statsButton';
        button.className = 'nav-item';
        button.innerHTML = `
            <a class="nav-link" href="#" onclick="userStats.openStatsModal(); return false;">
                <i class="bi bi-graph-up"></i> Моя статистика
            </a>
        `;
        
        // Добавляем в навбар
        const navbar = document.querySelector('.navbar-nav');
        if (navbar) {
            navbar.appendChild(button);
        }
    }

    openStatsModal() {
        // Удаляем старую модалку если есть
        const oldModal = document.getElementById('statsModal');
        if (oldModal) oldModal.remove();
        
        const modal = document.createElement('div');
        modal.id = 'statsModal';
        modal.className = 'modal fade';
        modal.innerHTML = `
            <div class="modal-dialog modal-xl modal-dialog-scrollable">
                <div class="modal-content">
                    <div class="modal-header">
                        <h5 class="modal-title">
                            <i class="bi bi-graph-up"></i> Моя статистика
                        </h5>
                        <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
                    </div>
                    <div class="modal-body">
                        ${this.renderStats()}
                    </div>
                    <div class="modal-footer">
                        <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">
                            Закрыть
                        </button>
                        <button type="button" class="btn btn-danger" onclick="userStats.resetStats()">
                            <i class="bi bi-trash"></i> Сбросить статистику
                        </button>
                        <button type="button" class="btn btn-primary" onclick="userStats.exportStats()">
                            <i class="bi bi-download"></i> Экспорт
                        </button>
                    </div>
                </div>
            </div>
        `;
        
        document.body.appendChild(modal);
        
        const bsModal = new bootstrap.Modal(modal);
        bsModal.show();
        
        modal.addEventListener('hidden.bs.modal', () => modal.remove());
        
        // Рисуем графики после открытия модалки
        setTimeout(() => this.renderCharts(), 300);
    }

    renderStats() {
        const daysSinceFirst = Math.floor(
            (new Date() - new Date(this.stats.firstVisit)) / (1000 * 60 * 60 * 24)
        );
        
        return `
            <div class="row g-4">
                <!-- Основные метрики -->
                <div class="col-12">
                    <h6 class="mb-3"><i class="bi bi-bar-chart-fill"></i> Основные метрики</h6>
                    <div class="row g-3">
                        ${this.renderMetricCard('Просмотров страниц', this.stats.pageViews, 'eye', 'primary')}
                        ${this.renderMetricCard('Турниров просмотрено', this.stats.tournamentsViewed, 'trophy', 'success')}
                        ${this.renderMetricCard('Поисковых запросов', this.stats.searchesPerformed, 'search', 'info')}
                        ${this.renderMetricCard('Фильтров применено', this.stats.filtersUsed, 'funnel', 'warning')}
                        ${this.renderMetricCard('В избранном', this.stats.favoritesAdded, 'heart', 'danger')}
                        ${this.renderMetricCard('Сравнений', this.stats.comparisonsUsed, 'arrow-left-right', 'secondary')}
                    </div>
                </div>
                
                <!-- Временная статистика -->
                <div class="col-12">
                    <h6 class="mb-3"><i class="bi bi-clock-history"></i> Временная статистика</h6>
                    <div class="row g-3">
                        <div class="col-md-4">
                            <div class="card">
                                <div class="card-body">
                                    <small class="text-muted">Первое посещение</small>
                                    <div class="h5 mb-0">${this.formatDate(this.stats.firstVisit)}</div>
                                </div>
                            </div>
                        </div>
                        <div class="col-md-4">
                            <div class="card">
                                <div class="card-body">
                                    <small class="text-muted">Последнее посещение</small>
                                    <div class="h5 mb-0">${this.formatDate(this.stats.lastVisit)}</div>
                                </div>
                            </div>
                        </div>
                        <div class="col-md-4">
                            <div class="card">
                                <div class="card-body">
                                    <small class="text-muted">Дней с момента регистрации</small>
                                    <div class="h5 mb-0">${daysSinceFirst}</div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
                
                <!-- Топ категорий -->
                <div class="col-md-6">
                    <h6 class="mb-3"><i class="bi bi-tag-fill"></i> Топ категорий</h6>
                    <div class="card">
                        <div class="card-body">
                            ${this.renderTopList(this.stats.mostViewedCategories, 'Категорий не просмотрено')}
                        </div>
                    </div>
                </div>
                
                <!-- Топ городов -->
                <div class="col-md-6">
                    <h6 class="mb-3"><i class="bi bi-geo-alt-fill"></i> Топ городов</h6>
                    <div class="card">
                        <div class="card-body">
                            ${this.renderTopList(this.stats.mostViewedLocations, 'Городов не просмотрено')}
                        </div>
                    </div>
                </div>
                
                <!-- Активность по часам -->
                <div class="col-md-6">
                    <h6 class="mb-3"><i class="bi bi-clock"></i> Активность по часам</h6>
                    <div class="card">
                        <div class="card-body">
                            <canvas id="hourlyActivityChart" height="200"></canvas>
                        </div>
                    </div>
                </div>
                
                <!-- Активность по дням недели -->
                <div class="col-md-6">
                    <h6 class="mb-3"><i class="bi bi-calendar-week"></i> Активность по дням недели</h6>
                    <div class="card">
                        <div class="card-body">
                            <canvas id="weeklyActivityChart" height="200"></canvas>
                        </div>
                    </div>
                </div>
            </div>
        `;
    }

    renderMetricCard(label, value, icon, color) {
        return `
            <div class="col-md-4 col-sm-6">
                <div class="card">
                    <div class="card-body text-center">
                        <i class="bi bi-${icon} text-${color}" style="font-size: 2rem;"></i>
                        <h3 class="text-${color} mt-2 mb-0">${value}</h3>
                        <small class="text-muted">${label}</small>
                    </div>
                </div>
            </div>
        `;
    }

    renderTopList(data, emptyMessage) {
        const sorted = Object.entries(data)
            .sort((a, b) => b[1] - a[1])
            .slice(0, 5);
        
        if (sorted.length === 0) {
            return `<p class="text-muted text-center mb-0">${emptyMessage}</p>`;
        }
        
        return sorted.map(([name, count], index) => `
            <div class="d-flex justify-content-between align-items-center mb-2 pb-2 ${index < sorted.length - 1 ? 'border-bottom' : ''}">
                <div>
                    <span class="badge bg-primary me-2">${index + 1}</span>
                    <strong>${this.escapeHtml(name)}</strong>
                </div>
                <span class="badge bg-secondary">${count}</span>
            </div>
        `).join('');
    }

    renderCharts() {
        // График активности по часам
        const hourlyCtx = document.getElementById('hourlyActivityChart');
        if (hourlyCtx && typeof Chart !== 'undefined') {
            new Chart(hourlyCtx, {
                type: 'bar',
                data: {
                    labels: Array.from({length: 24}, (_, i) => `${i}:00`),
                    datasets: [{
                        label: 'Активность',
                        data: this.stats.activityByHour,
                        backgroundColor: 'rgba(37, 99, 235, 0.5)',
                        borderColor: 'rgba(37, 99, 235, 1)',
                        borderWidth: 1
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: {
                        legend: { display: false }
                    },
                    scales: {
                        y: { beginAtZero: true }
                    }
                }
            });
        }
        
        // График активности по дням недели
        const weeklyCtx = document.getElementById('weeklyActivityChart');
        if (weeklyCtx && typeof Chart !== 'undefined') {
            new Chart(weeklyCtx, {
                type: 'bar',
                data: {
                    labels: ['Вс', 'Пн', 'Вт', 'Ср', 'Чт', 'Пт', 'Сб'],
                    datasets: [{
                        label: 'Активность',
                        data: this.stats.activityByDay,
                        backgroundColor: 'rgba(16, 185, 129, 0.5)',
                        borderColor: 'rgba(16, 185, 129, 1)',
                        borderWidth: 1
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: {
                        legend: { display: false }
                    },
                    scales: {
                        y: { beginAtZero: true }
                    }
                }
            });
        }
    }

    resetStats() {
        if (confirm('Вы уверены, что хотите сбросить всю статистику? Это действие нельзя отменить.')) {
            localStorage.removeItem(this.storageKey);
            this.loadStats();
            
            // Закрываем модалку
            const modal = bootstrap.Modal.getInstance(document.getElementById('statsModal'));
            if (modal) modal.hide();
            
            if (window.toast) {
                window.toast.success('Статистика сброшена');
            }
        }
    }

    exportStats() {
        const data = {
            'Метрика': 'Значение',
            'Просмотров страниц': this.stats.pageViews,
            'Турниров просмотрено': this.stats.tournamentsViewed,
            'Поисковых запросов': this.stats.searchesPerformed,
            'Фильтров применено': this.stats.filtersUsed,
            'В избранном': this.stats.favoritesAdded,
            'Сравнений': this.stats.comparisonsUsed,
            'Экспортов': this.stats.exportsUsed,
            'Первое посещение': this.formatDate(this.stats.firstVisit),
            'Последнее посещение': this.formatDate(this.stats.lastVisit),
            'Дней посещений': this.stats.visitDays.length
        };
        
        const json = JSON.stringify(data, null, 2);
        const blob = new Blob([json], { type: 'application/json' });
        const link = document.createElement('a');
        link.href = URL.createObjectURL(blob);
        link.download = `user_stats_${new Date().toISOString().split('T')[0]}.json`;
        link.click();
        
        if (window.toast) {
            window.toast.success('Статистика экспортирована');
        }
    }

    escapeHtml(text) {
        if (!text) return '';
        const div = document.createElement('div');
        div.textContent = text;
        return div.innerHTML;
    }

    formatDate(dateString) {
        if (!dateString) return 'Не указано';
        try {
            const date = new Date(dateString);
            return date.toLocaleDateString('ru-RU', {
                day: '2-digit',
                month: '2-digit',
                year: 'numeric',
                hour: '2-digit',
                minute: '2-digit'
            });
        } catch (e) {
            return dateString;
        }
    }
}

// Инициализация
const userStats = new UserStats();
window.userStats = userStats;

// Интеграция с другими системами
document.addEventListener('DOMContentLoaded', () => {
    // Отслеживаем просмотры турниров
    if (window.location.pathname.includes('/tournament/')) {
        const categoryElement = document.querySelector('[data-category]');
        const locationElement = document.querySelector('[data-location]');
        
        userStats.trackTournamentView(
            categoryElement?.dataset.category,
            locationElement?.dataset.location
        );
    }
});
