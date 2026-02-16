// Tournament History Tracker - отслеживание просмотренных турниров

class TournamentHistory {
    constructor() {
        this.maxHistory = 20;
        this.storageKey = 'tournament_history';
        this.init();
    }

    init() {
        this.loadHistory();
        this.trackCurrentPage();
        this.createHistoryWidget();
    }

    loadHistory() {
        const stored = localStorage.getItem(this.storageKey);
        this.history = stored ? JSON.parse(stored) : [];
    }

    saveHistory() {
        localStorage.setItem(this.storageKey, JSON.stringify(this.history));
    }

    addToHistory(tournament) {
        // Удаляем дубликаты
        this.history = this.history.filter(t => t.id !== tournament.id);
        
        // Добавляем в начало
        this.history.unshift({
            id: tournament.id,
            name: tournament.name,
            location: tournament.location,
            startDate: tournament.startDate,
            category: tournament.category,
            viewedAt: new Date().toISOString()
        });
        
        // Ограничиваем размер истории
        if (this.history.length > this.maxHistory) {
            this.history = this.history.slice(0, this.maxHistory);
        }
        
        this.saveHistory();
        this.updateWidget();
        
        // Track achievement
        if (window.achievementsSystem) {
            window.achievementsSystem.trackAction('tournament_viewed');
        }
    }

    trackCurrentPage() {
        // Проверяем, находимся ли мы на странице турнира
        const match = window.location.pathname.match(/\/tournament\/(\d+)/);
        if (match) {
            const tournamentId = parseInt(match[1]);
            
            // Получаем данные турнира со страницы
            const nameElement = document.querySelector('h1, .tournament-title');
            const locationElement = document.querySelector('.tournament-location, [data-location]');
            const dateElement = document.querySelector('.tournament-date, [data-start-date]');
            const categoryElement = document.querySelector('.tournament-category, [data-category]');
            
            if (nameElement) {
                const tournament = {
                    id: tournamentId,
                    name: nameElement.textContent.trim(),
                    location: locationElement ? locationElement.textContent.trim() : 'Не указано',
                    startDate: dateElement ? dateElement.dataset.startDate || dateElement.textContent.trim() : '',
                    category: categoryElement ? categoryElement.textContent.trim() : 'Общий'
                };
                
                this.addToHistory(tournament);
            }
        }
    }

    createHistoryWidget() {
        // Проверяем, не создан ли уже виджет
        if (document.getElementById('historyWidget')) return;

        const widget = document.createElement('div');
        widget.id = 'historyWidget';
        widget.innerHTML = `
            <style>
                #historyWidget {
                    position: fixed;
                    right: -350px;
                    top: 50%;
                    transform: translateY(-50%);
                    width: 350px;
                    max-height: 80vh;
                    background: var(--bg-primary);
                    border-radius: 12px 0 0 12px;
                    box-shadow: -4px 0 20px rgba(0, 0, 0, 0.15);
                    transition: right 0.3s ease;
                    z-index: 998;
                    overflow: hidden;
                    display: flex;
                    flex-direction: column;
                }
                
                #historyWidget.open {
                    right: 0;
                }
                
                .history-toggle {
                    position: absolute;
                    left: -40px;
                    top: 50%;
                    transform: translateY(-50%);
                    width: 40px;
                    height: 80px;
                    background: var(--primary-color);
                    border-radius: 8px 0 0 8px;
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    cursor: pointer;
                    color: white;
                    font-size: 1.2rem;
                    transition: all 0.3s ease;
                    box-shadow: -2px 0 8px rgba(0, 0, 0, 0.1);
                }
                
                .history-toggle:hover {
                    background: var(--primary-color);
                    filter: brightness(1.1);
                }
                
                .history-header {
                    padding: 1.25rem;
                    background: linear-gradient(135deg, var(--primary-color) 0%, #1e40af 100%);
                    color: white;
                    display: flex;
                    justify-content: space-between;
                    align-items: center;
                }
                
                .history-header h5 {
                    margin: 0;
                    font-weight: 700;
                    display: flex;
                    align-items: center;
                    gap: 0.5rem;
                }
                
                .history-content {
                    flex: 1;
                    overflow-y: auto;
                    padding: 1rem;
                }
                
                .history-item {
                    padding: 0.875rem;
                    margin-bottom: 0.75rem;
                    background: var(--bg-secondary);
                    border-radius: 8px;
                    border-left: 3px solid var(--primary-color);
                    cursor: pointer;
                    transition: all 0.2s ease;
                }
                
                .history-item:hover {
                    transform: translateX(-5px);
                    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
                }
                
                .history-item-title {
                    font-weight: 600;
                    color: var(--text-primary);
                    margin-bottom: 0.25rem;
                    font-size: 0.95rem;
                    line-height: 1.3;
                }
                
                .history-item-meta {
                    font-size: 0.8rem;
                    color: var(--text-secondary);
                    display: flex;
                    align-items: center;
                    gap: 0.5rem;
                    flex-wrap: wrap;
                }
                
                .history-item-meta i {
                    font-size: 0.75rem;
                }
                
                .history-empty {
                    text-align: center;
                    padding: 3rem 1rem;
                    color: var(--text-muted);
                }
                
                .history-empty i {
                    font-size: 3rem;
                    margin-bottom: 1rem;
                    opacity: 0.5;
                }
                
                .history-actions {
                    padding: 1rem;
                    border-top: 1px solid var(--border-color);
                    display: flex;
                    gap: 0.5rem;
                }
                
                .history-actions button {
                    flex: 1;
                    padding: 0.5rem;
                    border: none;
                    border-radius: 6px;
                    font-size: 0.875rem;
                    font-weight: 600;
                    cursor: pointer;
                    transition: all 0.2s ease;
                }
                
                .btn-clear-history {
                    background: var(--danger-color);
                    color: white;
                }
                
                .btn-clear-history:hover {
                    filter: brightness(1.1);
                }
                
                @media (max-width: 768px) {
                    #historyWidget {
                        width: 100%;
                        right: -100%;
                        border-radius: 0;
                        max-height: 100vh;
                    }
                    
                    #historyWidget.open {
                        right: 0;
                    }
                    
                    .history-toggle {
                        display: none;
                    }
                }
            </style>
            
            <div class="history-toggle" onclick="tournamentHistory.toggle()">
                <i class="bi bi-clock-history"></i>
            </div>
            
            <div class="history-header">
                <h5><i class="bi bi-clock-history"></i> История просмотров</h5>
                <button class="btn btn-link text-white p-0" onclick="tournamentHistory.toggle()">
                    <i class="bi bi-x-lg"></i>
                </button>
            </div>
            
            <div class="history-content" id="historyContent">
                ${this.renderHistory()}
            </div>
            
            <div class="history-actions">
                <button class="btn-clear-history" onclick="tournamentHistory.clearHistory()">
                    <i class="bi bi-trash"></i> Очистить историю
                </button>
            </div>
        `;

        document.body.appendChild(widget);
    }

    renderHistory() {
        if (this.history.length === 0) {
            return `
                <div class="history-empty">
                    <i class="bi bi-clock-history"></i>
                    <p>История просмотров пуста</p>
                    <small>Просмотренные турниры появятся здесь</small>
                </div>
            `;
        }

        return this.history.map(item => `
            <div class="history-item" onclick="window.location.href='/tournament/${item.id}'">
                <div class="history-item-title">${this.escapeHtml(item.name)}</div>
                <div class="history-item-meta">
                    <span><i class="bi bi-geo-alt-fill"></i> ${this.escapeHtml(item.location)}</span>
                    ${item.startDate ? `<span><i class="bi bi-calendar"></i> ${this.formatDate(item.startDate)}</span>` : ''}
                    <span><i class="bi bi-tag"></i> ${this.escapeHtml(item.category)}</span>
                </div>
            </div>
        `).join('');
    }

    updateWidget() {
        const content = document.getElementById('historyContent');
        if (content) {
            content.innerHTML = this.renderHistory();
        }
    }

    toggle() {
        const widget = document.getElementById('historyWidget');
        if (widget) {
            widget.classList.toggle('open');
        }
    }

    clearHistory() {
        if (confirm('Вы уверены, что хотите очистить историю просмотров?')) {
            this.history = [];
            this.saveHistory();
            this.updateWidget();
            
            if (window.toast) {
                window.toast.success('История очищена');
            }
        }
    }

    escapeHtml(text) {
        const div = document.createElement('div');
        div.textContent = text;
        return div.innerHTML;
    }

    formatDate(dateString) {
        try {
            const date = new Date(dateString);
            return date.toLocaleDateString('ru-RU', { 
                day: '2-digit', 
                month: '2-digit',
                year: 'numeric'
            });
        } catch (e) {
            return dateString;
        }
    }

    getRecentTournaments(limit = 5) {
        return this.history.slice(0, limit);
    }
}

// Инициализация
const tournamentHistory = new TournamentHistory();

// Экспорт для глобального использования
window.tournamentHistory = tournamentHistory;
