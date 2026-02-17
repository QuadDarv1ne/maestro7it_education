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
        // Проверить наличие toast системы
        if (typeof showToast === 'function') {
            showToast(message, type);
            return;
        }

        // Простое уведомление
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
