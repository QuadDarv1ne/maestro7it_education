/**
 * JavaScript для системы избранных турниров
 */
class FavoritesManager {
    constructor() {
        this.userId = 'user_1'; // В реальном приложении брать из сессии
        this.apiBase = '/api/favorites';
        this.heartButtons = [];
    }
    
    // Инициализация системы
    init() {
        this.bindHeartButtons();
        this.loadFavorites();
        this.setupEventListeners();
    }
    
    // Привязка кнопок сердечек
    bindHeartButtons() {
        this.heartButtons = document.querySelectorAll('[data-tournament-id]');
        this.heartButtons.forEach(button => {
            button.addEventListener('click', (e) => {
                e.preventDefault();
                this.toggleFavorite(button);
            });
        });
    }
    
    // Загрузка избранных турниров
    async loadFavorites() {
        try {
            const response = await fetch(`${this.apiBase}/${this.userId}`);
            if (response.ok) {
                const data = await response.json();
                this.updateFavoriteButtons(data.favorites);
                this.updateFavoritesList(data.favorites);
            }
        } catch (error) {
            console.error('Ошибка загрузки избранных:', error);
        }
    }
    
    // Обновление состояния кнопок
    updateFavoriteButtons(favorites) {
        const favoriteIds = favorites.map(fav => fav.tournament_id);
        
        this.heartButtons.forEach(button => {
            const tournamentId = parseInt(button.dataset.tournamentId);
            const isFavorite = favoriteIds.includes(tournamentId);
            this.updateButtonState(button, isFavorite);
        });
    }
    
    // Обновление состояния кнопки
    updateButtonState(button, isFavorite) {
        if (isFavorite) {
            button.classList.remove('btn-outline-danger');
            button.classList.add('btn-danger');
            button.innerHTML = '<i class="bi bi-heart-fill"></i>';
        } else {
            button.classList.remove('btn-danger');
            button.classList.add('btn-outline-danger');
            button.innerHTML = '<i class="bi bi-heart"></i>';
        }
    }
    
    // Переключение избранного
    async toggleFavorite(button) {
        const tournamentId = parseInt(button.dataset.tournamentId);
        
        try {
            // Проверяем текущее состояние
            const checkResponse = await fetch(`${this.apiBase}/check/${this.userId}/${tournamentId}`);
            const checkData = await checkResponse.json();
            
            if (checkData.is_favorite) {
                // Удаление из избранного
                await this.removeFavorite(button, tournamentId);
            } else {
                // Добавление в избранное
                await this.addFavorite(button, tournamentId);
            }
        } catch (error) {
            console.error('Ошибка переключения избранного:', error);
            this.showNotification('Ошибка операции', 'error');
        }
    }
    
    // Добавление в избранное
    async addFavorite(button, tournamentId) {
        const response = await fetch(`${this.apiBase}/${this.userId}`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                tournament_id: tournamentId,
                notes: 'Добавлено из интерфейса'
            })
        });
        
        if (response.ok) {
            this.updateButtonState(button, true);
            this.showNotification('Турнир добавлен в избранное', 'success');
            this.refreshFavoritesList();
        } else {
            const error = await response.json();
            this.showNotification(`Ошибка: ${error.error}`, 'error');
        }
    }
    
    // Удаление из избранного
    async removeFavorite(button, tournamentId) {
        // Получаем ID записи избранного
        const favoritesResponse = await fetch(`${this.apiBase}/${this.userId}`);
        const favoritesData = await favoritesResponse.json();
        const favoriteRecord = favoritesData.favorites.find(fav => fav.tournament_id === tournamentId);
        
        if (favoriteRecord) {
            const response = await fetch(`${this.apiBase}/${this.userId}/${favoriteRecord.id}`, {
                method: 'DELETE'
            });
            
            if (response.ok) {
                this.updateButtonState(button, false);
                this.showNotification('Турнир удален из избранного', 'info');
                this.refreshFavoritesList();
            } else {
                const error = await response.json();
                this.showNotification(`Ошибка: ${error.error}`, 'error');
            }
        }
    }
    
    // Обновление списка избранных
    updateFavoritesList(favorites) {
        const container = document.getElementById('favoritesContainer');
        if (!container) return;
        
        if (favorites.length === 0) {
            container.innerHTML = `
                <div class="col-12 text-center py-5">
                    <i class="bi bi-heart display-4 text-muted"></i>
                    <h4 class="mt-3">Избранных турниров нет</h4>
                    <p class="text-muted">Добавьте турниры в избранное, чтобы отслеживать их</p>
                </div>
            `;
            return;
        }
        
        container.innerHTML = favorites.map(favorite => {
            const tournament = favorite.tournament;
            return `
                <div class="col-md-6 col-lg-4 mb-4">
                    <div class="card h-100 tournament-favorite">
                        <div class="card-body">
                            <div class="d-flex justify-content-between align-items-start mb-2">
                                <h6 class="card-title">${tournament.name}</h6>
                                <button class="btn btn-sm btn-outline-danger" 
                                        data-tournament-id="${tournament.id}"
                                        onclick="favoritesManager.removeFromFavoritesList(this, ${favorite.id})">
                                    <i class="bi bi-heart-fill"></i>
                                </button>
                            </div>
                            <p class="card-text text-muted">${tournament.description}</p>
                            <div class="d-flex justify-content-between align-items-center">
                                <span class="badge bg-primary">${tournament.location}</span>
                                <small class="text-muted">${this.formatDateRange(tournament.start_date, tournament.end_date)}</small>
                            </div>
                            ${favorite.notes ? `<div class="mt-2"><small class="text-muted">Заметка: ${favorite.notes}</small></div>` : ''}
                        </div>
                    </div>
                </div>
            `;
        }).join('');
        
        // Перепривязываем обработчики
        this.bindHeartButtons();
    }
    
    // Удаление из списка избранных
    async removeFromFavoritesList(button, favoriteId) {
        try {
            const response = await fetch(`${this.apiBase}/${this.userId}/${favoriteId}`, {
                method: 'DELETE'
            });
            
            if (response.ok) {
                const card = button.closest('.col-md-6');
                card.style.transition = 'opacity 0.3s ease, transform 0.3s ease';
                card.style.opacity = '0';
                card.style.transform = 'translateX(-100px)';
                
                setTimeout(() => {
                    card.remove();
                    this.showNotification('Турнир удален из избранного', 'info');
                    this.refreshFavoritesList();
                }, 300);
            }
        } catch (error) {
            console.error('Ошибка удаления:', error);
        }
    }
    
    // Обновление списка избранных
    async refreshFavoritesList() {
        await this.loadFavorites();
    }
    
    // Форматирование диапазона дат
    formatDateRange(startDate, endDate) {
        const start = new Date(startDate);
        const end = new Date(endDate);
        
        if (start.toDateString() === end.toDateString()) {
            return start.toLocaleDateString('ru-RU', { day: 'numeric', month: 'short' });
        } else {
            return `${start.toLocaleDateString('ru-RU', { day: 'numeric', month: 'short' })} - ${end.toLocaleDateString('ru-RU', { day: 'numeric', month: 'short' })}`;
        }
    }
    
    // Настройка обработчиков событий
    setupEventListeners() {
        // Обновление заметок
        document.addEventListener('click', (e) => {
            if (e.target.closest('[data-action="edit-notes"]')) {
                const button = e.target.closest('[data-action="edit-notes"]');
                this.editNotes(button);
            }
        });
    }
    
    // Редактирование заметок
    async editNotes(button) {
        const favoriteId = button.dataset.favoriteId;
        const currentNotes = button.dataset.currentNotes || '';
        
        const newNotes = prompt('Введите заметку:', currentNotes);
        if (newNotes !== null) { // Пользователь не отменил
            try {
                const response = await fetch(`${this.apiBase}/${this.userId}/${favoriteId}`, {
                    method: 'PUT',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({ notes: newNotes })
                });
                
                if (response.ok) {
                    this.showNotification('Заметка обновлена', 'success');
                    button.dataset.currentNotes = newNotes;
                    this.refreshFavoritesList();
                }
            } catch (error) {
                console.error('Ошибка обновления заметок:', error);
            }
        }
    }
    
    // Показ уведомлений
    showNotification(message, type = 'info') {
        const notification = document.createElement('div');
        notification.className = `alert alert-${type} alert-dismissible fade show position-fixed`;
        notification.style = 'top: 20px; right: 20px; z-index: 10000; min-width: 300px;';
        notification.innerHTML = `
            ${message}
            <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
        `;
        
        document.body.appendChild(notification);
        
        setTimeout(() => {
            if (notification.parentNode) {
                notification.remove();
            }
        }, 3000);
    }
    
    // Получение статистики
    async getStats() {
        try {
            const response = await fetch(`${this.apiBase}/stats/${this.userId}`);
            if (response.ok) {
                return await response.json();
            }
        } catch (error) {
            console.error('Ошибка получения статистики:', error);
        }
        return null;
    }
    
    // Обновление статистики в интерфейсе
    async updateStatsDisplay() {
        const stats = await this.getStats();
        if (stats) {
            const statsContainer = document.getElementById('favoritesStats');
            if (statsContainer) {
                statsContainer.innerHTML = `
                    <div class="row text-center">
                        <div class="col-4">
                            <div class="h4 mb-0">${stats.total_favorites}</div>
                            <div class="small text-muted">Всего</div>
                        </div>
                        <div class="col-4">
                            <div class="h4 mb-0">${Object.keys(stats.category_stats).length}</div>
                            <div class="small text-muted">Категорий</div>
                        </div>
                        <div class="col-4">
                            <div class="h4 mb-0">${Object.keys(stats.location_stats).length}</div>
                            <div class="small text-muted">Городов</div>
                        </div>
                    </div>
                `;
            }
        }
    }
}

// Инициализация при загрузке страницы
document.addEventListener('DOMContentLoaded', function() {
    window.favoritesManager = new FavoritesManager();
    window.favoritesManager.init();
    
    // Обновление статистики каждые 30 секунд
    setInterval(() => {
        window.favoritesManager.updateStatsDisplay();
    }, 30000);
});