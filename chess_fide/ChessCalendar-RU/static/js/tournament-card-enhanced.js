/**
 * Enhanced Tournament Card Functionality
 * Улучшенная функциональность карточек турниров
 */

class TournamentCardManager {
    constructor() {
        this.favorites = new Set();
        this.init();
    }

    init() {
        this.loadFavorites();
        this.attachEventListeners();
        this.initializeCards();
    }

    /**
     * Загрузить избранные турниры из localStorage
     */
    loadFavorites() {
        try {
            const stored = localStorage.getItem('favoriteTournaments');
            if (stored) {
                this.favorites = new Set(JSON.parse(stored));
            }
        } catch (error) {
            console.error('Error loading favorites:', error);
        }
    }

    /**
     * Сохранить избранные в localStorage
     */
    saveFavorites() {
        try {
            localStorage.setItem('favoriteTournaments', JSON.stringify([...this.favorites]));
        } catch (error) {
            console.error('Error saving favorites:', error);
        }
    }

    /**
     * Инициализировать карточки
     */
    initializeCards() {
        // Обновить состояние кнопок избранного
        document.querySelectorAll('[data-tournament-id]').forEach(card => {
            const tournamentId = parseInt(card.dataset.tournamentId);
            if (this.favorites.has(tournamentId)) {
                this.updateFavoriteButton(card, true);
            }
        });
    }

    /**
     * Прикрепить обработчики событий
     */
    attachEventListeners() {
        // Кнопки избранного
        document.addEventListener('click', (e) => {
            const favoriteBtn = e.target.closest('.tournament-favorite-btn, .card-favorite-btn, [data-action="favorite"]');
            if (favoriteBtn) {
                e.preventDefault();
                e.stopPropagation();
                this.handleFavoriteClick(favoriteBtn);
            }

            // Кнопки поделиться
            const shareBtn = e.target.closest('[data-action="share"]');
            if (shareBtn) {
                e.preventDefault();
                e.stopPropagation();
                this.handleShareClick(shareBtn);
            }

            // Кнопки экспорта
            const exportBtn = e.target.closest('[data-action="export"]');
            if (exportBtn) {
                e.preventDefault();
                e.stopPropagation();
                this.handleExportClick(exportBtn);
            }
        });

        // Hover эффекты для карточек
        document.querySelectorAll('.tournament-card-modern, .tournament-card').forEach(card => {
            card.addEventListener('mouseenter', () => this.handleCardHover(card, true));
            card.addEventListener('mouseleave', () => this.handleCardHover(card, false));
        });
    }

    /**
     * Обработка клика по кнопке избранного
     */
    async handleFavoriteClick(button) {
        const card = button.closest('[data-tournament-id]');
        if (!card) return;

        const tournamentId = parseInt(card.dataset.tournamentId);
        const isFavorite = this.favorites.has(tournamentId);

        // Проверка авторизации
        if (!this.getUserId()) {
            this.showToast('Пожалуйста, войдите в систему', 'warning');
            setTimeout(() => {
                window.location.href = '/user/login';
            }, 1500);
            return;
        }

        // Анимация кнопки
        button.classList.add('animate-pulse');
        setTimeout(() => button.classList.remove('animate-pulse'), 300);

        try {
            // Отправить запрос на сервер
            const response = await this.toggleFavoriteOnServer(tournamentId, !isFavorite);
            const data = await response.json();

            if (response.ok && data.success) {
                // Обновить локальное состояние на основе ответа сервера
                if (data.is_favorite) {
                    this.favorites.add(tournamentId);
                } else {
                    this.favorites.delete(tournamentId);
                }

                this.saveFavorites();
                this.updateFavoriteButton(card, data.is_favorite);

                // Показать уведомление
                this.showToast(data.message, 'success');
            } else {
                throw new Error(data.error || 'Failed to update favorite');
            }
        } catch (error) {
            console.error('Error toggling favorite:', error);
            this.showToast('Ошибка при обновлении избранного', 'error');
        }
    }

    /**
     * Переключить избранное на сервере
     */
    async toggleFavoriteOnServer(tournamentId, add) {
        const endpoint = `/api/tournaments/${tournamentId}/toggle-favorite`;

        return fetch(endpoint, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRF-Token': this.getCSRFToken()
            },
            credentials: 'same-origin',
            body: JSON.stringify({
                user_id: this.getUserId()
            })
        });
    }

    /**
     * Обновить кнопку избранного
     */
    updateFavoriteButton(card, isFavorite) {
        const button = card.querySelector('.tournament-favorite-btn, .card-favorite-btn, [data-action="favorite"]');
        if (!button) return;

        if (isFavorite) {
            button.classList.add('active');
            button.setAttribute('title', 'Удалить из избранного');
            const icon = button.querySelector('i');
            if (icon) {
                icon.classList.remove('bi-heart');
                icon.classList.add('bi-heart-fill');
            }
        } else {
            button.classList.remove('active');
            button.setAttribute('title', 'Добавить в избранное');
            const icon = button.querySelector('i');
            if (icon) {
                icon.classList.remove('bi-heart-fill');
                icon.classList.add('bi-heart');
            }
        }
    }

    /**
     * Обработка клика по кнопке поделиться
     */
    async handleShareClick(button) {
        const card = button.closest('[data-tournament-id]');
        if (!card) return;

        const tournamentId = card.dataset.tournamentId;
        const tournamentName = card.querySelector('.tournament-card-title, .tournament-card-title-modern')?.textContent || 'Турнир';
        const url = `${window.location.origin}/tournament/${tournamentId}`;

        // Проверить поддержку Web Share API
        if (navigator.share) {
            try {
                await navigator.share({
                    title: tournamentName,
                    text: `Посмотрите этот турнир: ${tournamentName}`,
                    url: url
                });
                this.showToast('Успешно поделились', 'success');
            } catch (error) {
                if (error.name !== 'AbortError') {
                    console.error('Error sharing:', error);
                }
            }
        } else {
            // Fallback: копировать ссылку
            this.copyToClipboard(url);
            this.showToast('Ссылка скопирована в буфер обмена', 'success');
        }
    }

    /**
     * Обработка клика по кнопке экспорта
     */
    handleExportClick(button) {
        const card = button.closest('[data-tournament-id]');
        if (!card) return;

        const tournamentId = card.dataset.tournamentId;
        
        // Открыть модальное окно экспорта или скачать iCal
        window.location.href = `/api/tournaments/${tournamentId}/export/ical`;
        this.showToast('Экспорт начат', 'info');
    }

    /**
     * Обработка hover эффекта карточки
     */
    handleCardHover(card, isHovering) {
        if (isHovering) {
            card.style.transform = 'translateY(-8px)';
        } else {
            card.style.transform = '';
        }
    }

    /**
     * Копировать текст в буфер обмена
     */
    async copyToClipboard(text) {
        try {
            await navigator.clipboard.writeText(text);
        } catch (error) {
            // Fallback для старых браузеров
            const textarea = document.createElement('textarea');
            textarea.value = text;
            textarea.style.position = 'fixed';
            textarea.style.opacity = '0';
            document.body.appendChild(textarea);
            textarea.select();
            document.execCommand('copy');
            document.body.removeChild(textarea);
        }
    }

    /**
     * Показать уведомление
     */
    showToast(message, type = 'info') {
        // Используем глобальную систему уведомлений если доступна
        if (window.notificationSystem) {
            window.notificationSystem.show(message, type);
            return;
        }
        
        // Проверить наличие toast системы
        if (typeof showToast === 'function') {
            showToast(message, type);
            return;
        }

        // Простое уведомление (fallback)
        const toast = document.createElement('div');
        toast.className = `toast toast-${type}`;
        toast.textContent = message;
        toast.style.cssText = `
            position: fixed;
            bottom: 2rem;
            right: 2rem;
            padding: 1rem 1.5rem;
            background: ${type === 'success' ? '#10b981' : type === 'error' ? '#ef4444' : '#3b82f6'};
            color: white;
            border-radius: 0.5rem;
            box-shadow: 0 10px 25px rgba(0, 0, 0, 0.2);
            z-index: 9999;
            animation: slideInRight 0.3s ease;
        `;

        document.body.appendChild(toast);

        setTimeout(() => {
            toast.style.animation = 'slideOutRight 0.3s ease';
            setTimeout(() => toast.remove(), 300);
        }, 3000);
    }

    /**
     * Получить CSRF токен
     */
    getCSRFToken() {
        return document.querySelector('meta[name="csrf-token"]')?.content || '';
    }

    /**
     * Получить ID пользователя
     */
    getUserId() {
        // Попробовать получить из data-атрибута, meta-тега или cookie
        const bodyUserId = document.body.dataset.userId;
        if (bodyUserId) return bodyUserId;
        
        const metaUserId = document.querySelector('meta[name="user-id"]')?.content;
        if (metaUserId) return metaUserId;
        
        // Попробовать получить из cookie
        const cookies = document.cookie.split(';');
        for (let cookie of cookies) {
            const [name, value] = cookie.trim().split('=');
            if (name === 'user_id') return value;
        }
        
        return null;
    }
}

// Инициализация при загрузке страницы
document.addEventListener('DOMContentLoaded', () => {
    window.tournamentCardManager = new TournamentCardManager();
});

// Экспорт для использования в других модулях
if (typeof module !== 'undefined' && module.exports) {
    module.exports = TournamentCardManager;
}

// Добавить CSS анимации
const style = document.createElement('style');
style.textContent = `
    @keyframes slideInRight {
        from {
            transform: translateX(100%);
            opacity: 0;
        }
        to {
            transform: translateX(0);
            opacity: 1;
        }
    }

    @keyframes slideOutRight {
        from {
            transform: translateX(0);
            opacity: 1;
        }
        to {
            transform: translateX(100%);
            opacity: 0;
        }
    }

    .animate-pulse {
        animation: pulse 0.3s ease;
    }

    @keyframes pulse {
        0%, 100% {
            transform: scale(1);
        }
        50% {
            transform: scale(1.2);
        }
    }

    .tournament-favorite-btn.active {
        background: #ef4444;
        border-color: #ef4444;
        color: white;
    }

    .tournament-favorite-btn:hover {
        transform: scale(1.1);
    }
`;
document.head.appendChild(style);


    /**
     * Обработка клика по кнопке сравнения
     */
    async handleCompareClick(button) {
        const card = button.closest('[data-tournament-id]');
        if (!card) return;

        const tournamentId = parseInt(card.dataset.tournamentId);
        const tournamentName = card.dataset.tournamentName || 'Турнир';

        // Проверяем, есть ли система сравнения
        if (window.tournamentComparison) {
            const added = window.tournamentComparison.toggleTournament(tournamentId);
            
            // Обновляем кнопку
            if (added) {
                button.classList.add('active');
                this.showToast(`${tournamentName} добавлен в сравнение`, 'success');
            } else {
                button.classList.remove('active');
                this.showToast(`${tournamentName} удален из сравнения`, 'info');
            }

            // Анимация
            button.classList.add('animate-pulse');
            setTimeout(() => button.classList.remove('animate-pulse'), 300);
        } else {
            this.showToast('Система сравнения недоступна', 'warning');
        }
    }

    /**
     * Обработка клика по кнопке уведомлений
     */
    async handleNotifyClick(button) {
        const card = button.closest('[data-tournament-id]');
        if (!card) return;

        const tournamentId = parseInt(card.dataset.tournamentId);
        const tournamentName = card.dataset.tournamentName || 'Турнир';

        // Проверка авторизации
        if (!this.getUserId()) {
            this.showToast('Пожалуйста, войдите в систему', 'warning');
            return;
        }

        // Проверяем текущее состояние
        const isActive = button.classList.contains('active');

        try {
            // Отправляем запрос на сервер
            const response = await fetch('/api/notifications', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRF-Token': this.getCSRFToken()
                },
                body: JSON.stringify({
                    tournament_id: tournamentId,
                    action: isActive ? 'disable' : 'enable'
                })
            });

            const data = await response.json();

            if (response.ok && data.success) {
                // Обновляем кнопку
                button.classList.toggle('active');
                
                // Анимация колокольчика
                button.classList.add('animate-pulse');
                setTimeout(() => button.classList.remove('animate-pulse'), 300);

                this.showToast(
                    isActive 
                        ? `Уведомления для "${tournamentName}" отключены` 
                        : `Уведомления для "${tournamentName}" включены`,
                    'success'
                );
            } else {
                throw new Error(data.error || 'Failed to toggle notifications');
            }
        } catch (error) {
            console.error('Error toggling notifications:', error);
            this.showToast('Ошибка при настройке уведомлений', 'error');
        }
    }

    /**
     * Обновить все обработчики событий для новых кнопок
     */
    updateEventListeners() {
        // Кнопки сравнения
        document.querySelectorAll('[data-action="compare"]').forEach(btn => {
            btn.addEventListener('click', (e) => {
                e.preventDefault();
                e.stopPropagation();
                this.handleCompareClick(btn);
            });
        });

        // Кнопки уведомлений
        document.querySelectorAll('[data-action="notify"]').forEach(btn => {
            btn.addEventListener('click', (e) => {
                e.preventDefault();
                e.stopPropagation();
                this.handleNotifyClick(btn);
            });
        });
    }

    /**
     * Инициализация состояния кнопок при загрузке
     */
    initializeButtonStates() {
        // Проверяем состояние кнопок сравнения
        if (window.tournamentComparison) {
            const comparedIds = window.tournamentComparison.getComparedTournaments();
            comparedIds.forEach(id => {
                const button = document.querySelector(`[data-action="compare"][data-tournament-id="${id}"]`);
                if (button) {
                    button.classList.add('active');
                }
            });
        }

        // Проверяем состояние уведомлений из localStorage
        try {
            const notifications = JSON.parse(localStorage.getItem('tournamentNotifications') || '[]');
            notifications.forEach(id => {
                const button = document.querySelector(`[data-action="notify"][data-tournament-id="${id}"]`);
                if (button) {
                    button.classList.add('active');
                }
            });
        } catch (error) {
            console.error('Error loading notification states:', error);
        }
    }

    /**
     * Анимация при наведении на карточку
     */
    handleCardHover(card, isHovering) {
        const actions = card.querySelector('.tournament-card-actions');
        if (actions) {
            if (isHovering) {
                actions.style.opacity = '1';
            } else {
                actions.style.opacity = '';
            }
        }
    }

    /**
     * Показать рейтинг турнира
     */
    displayRating(card, rating) {
        const ratingContainer = card.querySelector('.tournament-rating');
        if (!ratingContainer) return;

        const stars = Math.round(rating);
        const starsHTML = Array.from({ length: 5 }, (_, i) => {
            if (i < stars) {
                return '<i class="bi bi-star-fill text-warning"></i>';
            } else {
                return '<i class="bi bi-star text-muted"></i>';
            }
        }).join('');

        ratingContainer.innerHTML = `
            ${starsHTML}
            <span class="rating-value">${rating.toFixed(1)}</span>
        `;
    }

    /**
     * Обновить счетчик просмотров
     */
    updateViewCount(tournamentId) {
        const card = document.querySelector(`[data-tournament-id="${tournamentId}"]`);
        if (!card) return;

        const viewsElement = card.querySelector('.tournament-views span');
        if (viewsElement) {
            const currentViews = parseInt(viewsElement.textContent) || 0;
            viewsElement.textContent = currentViews + 1;
        }
    }

    /**
     * Показать индикатор популярности
     */
    showTrendingIndicator(card, viewCount) {
        if (viewCount > 100 && !card.querySelector('.tournament-card-trending')) {
            const indicator = document.createElement('div');
            indicator.className = 'tournament-card-trending';
            indicator.innerHTML = '<i class="bi bi-fire"></i><span>Популярный</span>';
            card.appendChild(indicator);
        }
    }

    /**
     * Обновить прогресс-бар для текущих турниров
     */
    updateProgressBar(card, startDate, endDate) {
        const progressContainer = card.querySelector('.tournament-progress');
        if (!progressContainer) return;

        const now = new Date();
        const start = new Date(startDate);
        const end = new Date(endDate);

        const totalDays = Math.ceil((end - start) / (1000 * 60 * 60 * 24));
        const elapsedDays = Math.ceil((now - start) / (1000 * 60 * 60 * 24));
        const progress = Math.min(100, Math.max(0, (elapsedDays / totalDays) * 100));

        const progressBar = progressContainer.querySelector('.progress-bar');
        const progressText = progressContainer.querySelector('small');

        if (progressBar) {
            progressBar.style.width = `${progress}%`;
            progressBar.setAttribute('aria-valuenow', progress);
        }

        if (progressText) {
            progressText.textContent = `День ${elapsedDays} из ${totalDays}`;
        }
    }
}

// Обновляем инициализацию при загрузке страницы
document.addEventListener('DOMContentLoaded', () => {
    const manager = new TournamentCardManager();
    
    // Обновляем обработчики для новых кнопок
    manager.updateEventListeners();
    
    // Инициализируем состояние кнопок
    manager.initializeButtonStates();
    
    // Делаем доступным глобально
    window.tournamentCardManager = manager;
    
    console.log('[Tournament Cards] Enhanced functionality initialized');
});

// Экспорт для использования в других модулях
if (typeof module !== 'undefined' && module.exports) {
    module.exports = TournamentCardManager;
}
