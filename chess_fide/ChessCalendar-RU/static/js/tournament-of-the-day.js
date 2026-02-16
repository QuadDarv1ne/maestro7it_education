// Tournament of the Day - рекомендация турнира дня

class TournamentOfTheDay {
    constructor() {
        this.storageKey = 'tournament_of_the_day';
        this.lastUpdateKey = 'totd_last_update';
        this.init();
    }

    init() {
        this.checkAndUpdate();
        this.createWidget();
    }

    checkAndUpdate() {
        const lastUpdate = localStorage.getItem(this.lastUpdateKey);
        const today = new Date().toDateString();
        
        if (lastUpdate !== today) {
            this.selectTournamentOfTheDay();
            localStorage.setItem(this.lastUpdateKey, today);
        }
    }

    async selectTournamentOfTheDay() {
        try {
            // Получаем предстоящие турниры
            const response = await fetch('/api/tournaments?status=Scheduled&per_page=50');
            const data = await response.json();
            
            if (data.tournaments && data.tournaments.length > 0) {
                // Выбираем случайный турнир с весами
                const tournament = this.selectWeightedRandom(data.tournaments);
                
                localStorage.setItem(this.storageKey, JSON.stringify({
                    tournament: tournament,
                    date: new Date().toISOString()
                }));
            }
        } catch (error) {
            console.error('Error selecting tournament of the day:', error);
        }
    }

    selectWeightedRandom(tournaments) {
        // Присваиваем веса турнирам
        const weighted = tournaments.map(t => {
            let weight = 1;
            
            // Международные турниры - больший вес
            if (t.category && (t.category.includes('International') || t.category.includes('World'))) {
                weight += 3;
            }
            
            // Турниры с призовым фондом
            if (t.prize_fund) {
                weight += 2;
            }
            
            // Турниры в ближайшие 30 дней
            const startDate = new Date(t.start_date);
            const daysUntil = Math.floor((startDate - new Date()) / (1000 * 60 * 60 * 24));
            if (daysUntil <= 30) {
                weight += 2;
            }
            
            return { tournament: t, weight };
        });
        
        // Выбираем случайный с учётом весов
        const totalWeight = weighted.reduce((sum, item) => sum + item.weight, 0);
        let random = Math.random() * totalWeight;
        
        for (const item of weighted) {
            random -= item.weight;
            if (random <= 0) {
                return item.tournament;
            }
        }
        
        return weighted[0].tournament;
    }

    getTournamentOfTheDay() {
        const stored = localStorage.getItem(this.storageKey);
        return stored ? JSON.parse(stored) : null;
    }

    createWidget() {
        // Проверяем, находимся ли мы на главной странице
        if (window.location.pathname !== '/') return;
        
        // Проверяем, не создан ли уже виджет
        if (document.getElementById('totdWidget')) return;
        
        const data = this.getTournamentOfTheDay();
        if (!data || !data.tournament) return;
        
        const tournament = data.tournament;
        
        const widget = document.createElement('div');
        widget.id = 'totdWidget';
        widget.innerHTML = `
            <style>
                #totdWidget {
                    background: linear-gradient(135deg, #f59e0b 0%, #d97706 100%);
                    border-radius: 16px;
                    padding: 2rem;
                    margin-bottom: 2rem;
                    color: white;
                    box-shadow: 0 10px 30px rgba(245, 158, 11, 0.3);
                    position: relative;
                    overflow: hidden;
                }
                
                #totdWidget::before {
                    content: '';
                    position: absolute;
                    top: -50%;
                    right: -10%;
                    width: 400px;
                    height: 400px;
                    background: radial-gradient(circle, rgba(255,255,255,0.1) 0%, transparent 70%);
                    border-radius: 50%;
                }
                
                .totd-badge {
                    display: inline-flex;
                    align-items: center;
                    gap: 0.5rem;
                    background: rgba(255, 255, 255, 0.2);
                    padding: 0.5rem 1rem;
                    border-radius: 20px;
                    font-weight: 700;
                    font-size: 0.875rem;
                    margin-bottom: 1rem;
                    backdrop-filter: blur(10px);
                }
                
                .totd-title {
                    font-size: 1.75rem;
                    font-weight: 800;
                    margin-bottom: 1rem;
                    text-shadow: 0 2px 4px rgba(0,0,0,0.2);
                }
                
                .totd-info {
                    display: grid;
                    grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
                    gap: 1rem;
                    margin-bottom: 1.5rem;
                }
                
                .totd-info-item {
                    display: flex;
                    align-items: center;
                    gap: 0.5rem;
                    font-size: 0.95rem;
                }
                
                .totd-info-item i {
                    font-size: 1.2rem;
                    opacity: 0.9;
                }
                
                .totd-actions {
                    display: flex;
                    gap: 1rem;
                    flex-wrap: wrap;
                }
                
                .totd-btn {
                    padding: 0.75rem 1.5rem;
                    border-radius: 10px;
                    font-weight: 600;
                    text-decoration: none;
                    transition: all 0.3s ease;
                    display: inline-flex;
                    align-items: center;
                    gap: 0.5rem;
                    border: none;
                    cursor: pointer;
                }
                
                .totd-btn-primary {
                    background: white;
                    color: #d97706;
                }
                
                .totd-btn-primary:hover {
                    transform: translateY(-2px);
                    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
                    color: #d97706;
                }
                
                .totd-btn-secondary {
                    background: rgba(255, 255, 255, 0.2);
                    color: white;
                    backdrop-filter: blur(10px);
                }
                
                .totd-btn-secondary:hover {
                    background: rgba(255, 255, 255, 0.3);
                    color: white;
                }
                
                .totd-icon {
                    position: absolute;
                    right: 2rem;
                    top: 50%;
                    transform: translateY(-50%);
                    font-size: 8rem;
                    opacity: 0.1;
                    animation: pulse 3s ease-in-out infinite;
                }
                
                @keyframes pulse {
                    0%, 100% { transform: translateY(-50%) scale(1); }
                    50% { transform: translateY(-50%) scale(1.05); }
                }
                
                @media (max-width: 768px) {
                    #totdWidget {
                        padding: 1.5rem;
                    }
                    
                    .totd-title {
                        font-size: 1.35rem;
                    }
                    
                    .totd-info {
                        grid-template-columns: 1fr;
                        gap: 0.75rem;
                    }
                    
                    .totd-icon {
                        font-size: 4rem;
                        opacity: 0.08;
                    }
                }
            </style>
            
            <div class="totd-badge">
                <i class="bi bi-star-fill"></i>
                Турнир дня
            </div>
            
            <div class="totd-title">${this.escapeHtml(tournament.name)}</div>
            
            <div class="totd-info">
                <div class="totd-info-item">
                    <i class="bi bi-calendar-event"></i>
                    <span>${this.formatDate(tournament.start_date)}</span>
                </div>
                <div class="totd-info-item">
                    <i class="bi bi-geo-alt-fill"></i>
                    <span>${this.escapeHtml(tournament.location)}</span>
                </div>
                <div class="totd-info-item">
                    <i class="bi bi-tag-fill"></i>
                    <span>${this.escapeHtml(tournament.category)}</span>
                </div>
                ${tournament.prize_fund ? `
                <div class="totd-info-item">
                    <i class="bi bi-cash-coin"></i>
                    <span>${this.escapeHtml(tournament.prize_fund)}</span>
                </div>
                ` : ''}
            </div>
            
            <div class="totd-actions">
                <a href="/tournament/${tournament.id}" class="totd-btn totd-btn-primary">
                    <i class="bi bi-eye-fill"></i>
                    Подробнее
                </a>
                <button class="totd-btn totd-btn-secondary" onclick="tournamentOfTheDay.addToFavorites(${tournament.id})">
                    <i class="bi bi-heart-fill"></i>
                    В избранное
                </button>
                <button class="totd-btn totd-btn-secondary" onclick="tournamentOfTheDay.share(${tournament.id})">
                    <i class="bi bi-share-fill"></i>
                    Поделиться
                </button>
            </div>
            
            <i class="bi bi-trophy-fill totd-icon"></i>
        `;
        
        // Вставляем после hero-секции
        const container = document.querySelector('.container');
        const heroSection = container?.querySelector('.hero-section');
        
        if (container && heroSection) {
            heroSection.parentNode.insertBefore(widget, heroSection.nextSibling);
        }
    }

    addToFavorites(tournamentId) {
        if (window.favoritesManager) {
            window.favoritesManager.toggleFavorite(tournamentId);
        } else {
            if (window.toast) {
                window.toast.info('Функция избранного недоступна');
            }
        }
    }

    share(tournamentId) {
        const url = `${window.location.origin}/tournament/${tournamentId}`;
        
        if (navigator.share) {
            navigator.share({
                title: 'Турнир дня - ChessCalendar-RU',
                text: 'Посмотрите этот интересный турнир!',
                url: url
            }).catch(() => {});
        } else {
            if (window.ChessCalendar) {
                window.ChessCalendar.copyToClipboard(url, 'Ссылка скопирована!');
            }
        }
    }

    escapeHtml(text) {
        if (!text) return '';
        const div = document.createElement('div');
        div.textContent = text;
        return div.innerHTML;
    }

    formatDate(dateString) {
        try {
            const date = new Date(dateString);
            return date.toLocaleDateString('ru-RU', {
                day: '2-digit',
                month: 'long',
                year: 'numeric'
            });
        } catch (e) {
            return dateString;
        }
    }
}

// Инициализация
if (window.location.pathname === '/') {
    const tournamentOfTheDay = new TournamentOfTheDay();
    window.tournamentOfTheDay = tournamentOfTheDay;
}
