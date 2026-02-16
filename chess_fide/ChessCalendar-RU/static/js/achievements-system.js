// Achievements System - Gamification for user engagement

class AchievementsSystem {
    constructor() {
        this.achievements = this.loadAchievements();
        this.stats = this.loadStats();
        this.init();
    }

    init() {
        this.defineAchievements();
        this.checkAchievements();
        this.createAchievementsButton();
    }

    defineAchievements() {
        this.achievementDefinitions = [
            {
                id: 'first_favorite',
                name: 'Первое избранное',
                description: 'Добавьте первый турнир в избранное',
                icon: 'bi-heart-fill',
                color: '#ef4444',
                requirement: () => this.stats.favoritesAdded >= 1
            },
            {
                id: 'favorite_collector',
                name: 'Коллекционер',
                description: 'Добавьте 10 турниров в избранное',
                icon: 'bi-collection-fill',
                color: '#f59e0b',
                requirement: () => this.stats.favoritesAdded >= 10
            },
            {
                id: 'first_comparison',
                name: 'Аналитик',
                description: 'Сравните турниры впервые',
                icon: 'bi-bar-chart-fill',
                color: '#3b82f6',
                requirement: () => this.stats.comparisonsUsed >= 1
            },
            {
                id: 'filter_master',
                name: 'Мастер фильтров',
                description: 'Используйте фильтры 5 раз',
                icon: 'bi-funnel-fill',
                color: '#8b5cf6',
                requirement: () => this.stats.filtersUsed >= 5
            },
            {
                id: 'export_expert',
                name: 'Эксперт экспорта',
                description: 'Экспортируйте данные 3 раза',
                icon: 'bi-download',
                color: '#10b981',
                requirement: () => this.stats.exportsUsed >= 3
            },
            {
                id: 'daily_visitor',
                name: 'Постоянный посетитель',
                description: 'Посещайте сайт 7 дней подряд',
                icon: 'bi-calendar-check-fill',
                color: '#06b6d4',
                requirement: () => this.stats.consecutiveDays >= 7
            },
            {
                id: 'tournament_explorer',
                name: 'Исследователь',
                description: 'Просмотрите 20 турниров',
                icon: 'bi-eye-fill',
                color: '#ec4899',
                requirement: () => this.stats.tournamentsViewed >= 20
            },
            {
                id: 'map_navigator',
                name: 'Навигатор',
                description: 'Используйте карту турниров',
                icon: 'bi-geo-alt-fill',
                color: '#14b8a6',
                requirement: () => this.stats.mapUsed >= 1
            },
            {
                id: 'statistics_fan',
                name: 'Любитель статистики',
                description: 'Посетите страницу статистики',
                icon: 'bi-graph-up',
                color: '#f97316',
                requirement: () => this.stats.statisticsViewed >= 1
            },
            {
                id: 'theme_switcher',
                name: 'Переключатель тем',
                description: 'Переключите тему оформления',
                icon: 'bi-moon-stars-fill',
                color: '#6366f1',
                requirement: () => this.stats.themeSwitched >= 1
            }
        ];
    }

    loadAchievements() {
        const saved = localStorage.getItem('userAchievements');
        return saved ? JSON.parse(saved) : [];
    }

    saveAchievements() {
        localStorage.setItem('userAchievements', JSON.stringify(this.achievements));
    }

    loadStats() {
        const saved = localStorage.getItem('userStats');
        return saved ? JSON.parse(saved) : {
            favoritesAdded: 0,
            comparisonsUsed: 0,
            filtersUsed: 0,
            exportsUsed: 0,
            consecutiveDays: 0,
            tournamentsViewed: 0,
            mapUsed: 0,
            statisticsViewed: 0,
            themeSwitched: 0,
            lastVisit: null
        };
    }

    saveStats() {
        localStorage.setItem('userStats', JSON.stringify(this.stats));
    }

    // Track user actions
    trackAction(action) {
        switch (action) {
            case 'favorite_added':
                this.stats.favoritesAdded++;
                break;
            case 'comparison_used':
                this.stats.comparisonsUsed++;
                break;
            case 'filter_used':
                this.stats.filtersUsed++;
                break;
            case 'export_used':
                this.stats.exportsUsed++;
                break;
            case 'tournament_viewed':
                this.stats.tournamentsViewed++;
                break;
            case 'map_used':
                this.stats.mapUsed++;
                break;
            case 'statistics_viewed':
                this.stats.statisticsViewed++;
                break;
            case 'theme_switched':
                this.stats.themeSwitched++;
                break;
        }

        this.saveStats();
        this.checkAchievements();
    }

    checkConsecutiveDays() {
        const today = new Date().toDateString();
        const lastVisit = this.stats.lastVisit;

        if (!lastVisit) {
            this.stats.consecutiveDays = 1;
        } else {
            const lastDate = new Date(lastVisit);
            const todayDate = new Date(today);
            const diffDays = Math.floor((todayDate - lastDate) / (1000 * 60 * 60 * 24));

            if (diffDays === 1) {
                this.stats.consecutiveDays++;
            } else if (diffDays > 1) {
                this.stats.consecutiveDays = 1;
            }
        }

        this.stats.lastVisit = today;
        this.saveStats();
    }

    checkAchievements() {
        let newAchievements = [];

        this.achievementDefinitions.forEach(def => {
            if (!this.hasAchievement(def.id) && def.requirement()) {
                this.unlockAchievement(def);
                newAchievements.push(def);
            }
        });

        if (newAchievements.length > 0) {
            this.showAchievementNotification(newAchievements);
        }
    }

    hasAchievement(id) {
        return this.achievements.includes(id);
    }

    unlockAchievement(achievement) {
        this.achievements.push(achievement.id);
        this.saveAchievements();
    }

    showAchievementNotification(achievements) {
        achievements.forEach((achievement, index) => {
            setTimeout(() => {
                this.createAchievementToast(achievement);
            }, index * 500);
        });
    }

    createAchievementToast(achievement) {
        const toast = document.createElement('div');
        toast.className = 'achievement-toast';
        toast.style.cssText = `
            position: fixed;
            top: ${80 + (this.achievements.length * 10)}px;
            right: 20px;
            background: linear-gradient(135deg, ${achievement.color} 0%, ${this.darkenColor(achievement.color)} 100%);
            color: white;
            padding: 20px;
            border-radius: 12px;
            box-shadow: 0 8px 24px rgba(0, 0, 0, 0.3);
            z-index: 10000;
            min-width: 350px;
            animation: achievementSlide 0.5s ease;
        `;

        toast.innerHTML = `
            <div style="display: flex; align-items: center; gap: 15px;">
                <div style="font-size: 40px;">
                    <i class="bi ${achievement.icon}"></i>
                </div>
                <div style="flex: 1;">
                    <div style="font-weight: 700; font-size: 18px; margin-bottom: 4px;">
                        🏆 Достижение разблокировано!
                    </div>
                    <div style="font-weight: 600; font-size: 16px; margin-bottom: 4px;">
                        ${achievement.name}
                    </div>
                    <div style="font-size: 14px; opacity: 0.9;">
                        ${achievement.description}
                    </div>
                </div>
            </div>
        `;

        // Add animation style
        if (!document.getElementById('achievementStyles')) {
            const style = document.createElement('style');
            style.id = 'achievementStyles';
            style.textContent = `
                @keyframes achievementSlide {
                    from {
                        transform: translateX(400px);
                        opacity: 0;
                    }
                    to {
                        transform: translateX(0);
                        opacity: 1;
                    }
                }
            `;
            document.head.appendChild(style);
        }

        document.body.appendChild(toast);

        // Remove after 5 seconds
        setTimeout(() => {
            toast.style.animation = 'achievementSlide 0.5s ease reverse';
            setTimeout(() => {
                if (toast.parentElement) {
                    toast.parentElement.removeChild(toast);
                }
            }, 500);
        }, 5000);
    }

    darkenColor(color) {
        // Simple color darkening
        const hex = color.replace('#', '');
        const r = Math.max(0, parseInt(hex.substr(0, 2), 16) - 30);
        const g = Math.max(0, parseInt(hex.substr(2, 2), 16) - 30);
        const b = Math.max(0, parseInt(hex.substr(4, 2), 16) - 30);
        return `#${r.toString(16).padStart(2, '0')}${g.toString(16).padStart(2, '0')}${b.toString(16).padStart(2, '0')}`;
    }

    createAchievementsButton() {
        // Add achievements button to navbar
        const navbar = document.querySelector('.navbar .d-flex');
        if (!navbar || document.getElementById('achievementsBtn')) return;

        const button = document.createElement('button');
        button.id = 'achievementsBtn';
        button.className = 'btn btn-outline-light position-relative me-2';
        button.innerHTML = `
            <i class="bi bi-trophy-fill"></i>
            <span class="position-absolute top-0 start-100 translate-middle badge rounded-pill bg-warning" 
                  id="achievementsBadge">${this.achievements.length}</span>
        `;
        button.onclick = () => this.showAchievementsModal();
        button.title = 'Достижения';
        
        navbar.insertBefore(button, navbar.firstChild);
    }

    showAchievementsModal() {
        const existingModal = document.getElementById('achievementsModal');
        if (existingModal) existingModal.remove();

        const modal = document.createElement('div');
        modal.id = 'achievementsModal';
        modal.className = 'modal fade';
        modal.innerHTML = `
            <div class="modal-dialog modal-lg modal-dialog-scrollable">
                <div class="modal-content">
                    <div class="modal-header">
                        <h5 class="modal-title">
                            <i class="bi bi-trophy-fill text-warning"></i> Достижения
                        </h5>
                        <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
                    </div>
                    <div class="modal-body">
                        <div class="mb-3">
                            <div class="progress" style="height: 25px;">
                                <div class="progress-bar bg-warning" role="progressbar" 
                                     style="width: ${(this.achievements.length / this.achievementDefinitions.length) * 100}%">
                                    ${this.achievements.length} / ${this.achievementDefinitions.length}
                                </div>
                            </div>
                        </div>
                        ${this.generateAchievementsList()}
                    </div>
                    <div class="modal-footer">
                        <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Закрыть</button>
                    </div>
                </div>
            </div>
        `;

        document.body.appendChild(modal);
        const bsModal = new bootstrap.Modal(modal);
        bsModal.show();
    }

    generateAchievementsList() {
        let html = '<div class="row g-3">';

        this.achievementDefinitions.forEach(achievement => {
            const unlocked = this.hasAchievement(achievement.id);
            const opacity = unlocked ? '1' : '0.4';
            const grayscale = unlocked ? '0' : '1';

            html += `
                <div class="col-md-6">
                    <div class="card" style="opacity: ${opacity}; filter: grayscale(${grayscale});">
                        <div class="card-body">
                            <div class="d-flex align-items-center gap-3">
                                <div style="
                                    width: 60px;
                                    height: 60px;
                                    border-radius: 50%;
                                    background: ${achievement.color};
                                    display: flex;
                                    align-items: center;
                                    justify-content: center;
                                    color: white;
                                    font-size: 28px;
                                ">
                                    <i class="bi ${achievement.icon}"></i>
                                </div>
                                <div class="flex-grow-1">
                                    <h6 class="mb-1">${achievement.name}</h6>
                                    <small class="text-muted">${achievement.description}</small>
                                    ${unlocked ? '<div class="badge bg-success mt-1">Разблокировано</div>' : '<div class="badge bg-secondary mt-1">Заблокировано</div>'}
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            `;
        });

        html += '</div>';
        return html;
    }

    // Public methods for tracking
    getProgress() {
        return {
            unlocked: this.achievements.length,
            total: this.achievementDefinitions.length,
            percentage: (this.achievements.length / this.achievementDefinitions.length) * 100
        };
    }

    getStats() {
        return this.stats;
    }
}

// Initialize
const achievementsSystem = new AchievementsSystem();

// Check consecutive days on load
achievementsSystem.checkConsecutiveDays();

// Track page views
if (window.location.pathname.includes('/tournament/')) {
    achievementsSystem.trackAction('tournament_viewed');
}

if (window.location.pathname === '/map') {
    achievementsSystem.trackAction('map_used');
}

if (window.location.pathname === '/statistics') {
    achievementsSystem.trackAction('statistics_viewed');
}

// Export for use in other scripts
window.achievementsSystem = achievementsSystem;
