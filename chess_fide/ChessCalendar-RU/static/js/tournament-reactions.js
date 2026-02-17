/**
 * Tournament Reactions System
 * Система реакций на турниры (лайки, дизлайки, эмоции)
 */

class TournamentReactions {
    constructor() {
        this.reactions = this.loadReactions();
        this.availableReactions = this.getAvailableReactions();
        this.init();
    }

    init() {
        this.attachEventListeners();
        this.updateAllReactionButtons();
    }

    /**
     * Доступные реакции
     */
    getAvailableReactions() {
        return [
            { id: 'like', icon: 'hand-thumbs-up-fill', label: 'Нравится', color: '#3b82f6' },
            { id: 'love', icon: 'heart-fill', label: 'Обожаю', color: '#ef4444' },
            { id: 'fire', icon: 'fire', label: 'Огонь', color: '#f59e0b' },
            { id: 'star', icon: 'star-fill', label: 'Супер', color: '#fbbf24' },
            { id: 'thinking', icon: 'emoji-thinking', label: 'Интересно', color: '#8b5cf6' }
        ];
    }

    /**
     * Загрузить реакции
     */
    loadReactions() {
        try {
            const stored = localStorage.getItem('tournamentReactions');
            return stored ? JSON.parse(stored) : {};
        } catch (error) {
            console.error('Error loading reactions:', error);
            return {};
        }
    }

    /**
     * Сохранить реакции
     */
    saveReactions() {
        try {
            localStorage.setItem('tournamentReactions', JSON.stringify(this.reactions));
        } catch (error) {
            console.error('Error saving reactions:', error);
        }
    }

    /**
     * Прикрепить обработчики событий
     */
    attachEventListeners() {
        // Кнопка реакций
        document.addEventListener('click', (e) => {
            const reactionBtn = e.target.closest('[data-action="react"]');
            if (reactionBtn) {
                e.preventDefault();
                e.stopPropagation();
                const tournamentId = parseInt(reactionBtn.dataset.tournamentId);
                this.showReactionPicker(tournamentId, reactionBtn);
            }
        });

        // Быстрая реакция (лайк)
        document.addEventListener('click', (e) => {
            const likeBtn = e.target.closest('[data-action="quick-like"]');
            if (likeBtn) {
                e.preventDefault();
                e.stopPropagation();
                const tournamentId = parseInt(likeBtn.dataset.tournamentId);
                this.toggleReaction(tournamentId, 'like');
            }
        });
    }

    /**
     * Показать выбор реакций
     */
    showReactionPicker(tournamentId, button) {
        const currentReaction = this.reactions[tournamentId];

        const pickerHTML = `
            <div class="reaction-picker">
                <div class="reaction-picker-header">
                    <span>Выберите реакцию</span>
                    <button class="btn-close-sm" onclick="this.closest('.reaction-picker').remove()">
                        <i class="bi bi-x"></i>
                    </button>
                </div>
                <div class="reaction-picker-list">
                    ${this.availableReactions.map(reaction => `
                        <button class="reaction-item ${currentReaction === reaction.id ? 'active' : ''}"
                                data-reaction="${reaction.id}"
                                style="--reaction-color: ${reaction.color}"
                                onclick="window.tournamentReactions.selectReaction(${tournamentId}, '${reaction.id}', this)"
                                title="${reaction.label}">
                            <i class="bi bi-${reaction.icon}"></i>
                            <span>${reaction.label}</span>
                        </button>
                    `).join('')}
                </div>
                ${currentReaction ? `
                    <button class="reaction-remove-btn" onclick="window.tournamentReactions.removeReaction(${tournamentId})">
                        <i class="bi bi-trash"></i>
                        Удалить реакцию
                    </button>
                ` : ''}
            </div>
        `;

        // Удалить существующий picker
        document.querySelectorAll('.reaction-picker').forEach(el => el.remove());

        // Добавить новый
        button.insertAdjacentHTML('afterend', pickerHTML);

        // Позиционирование
        const picker = button.nextElementSibling;
        const rect = button.getBoundingClientRect();
        picker.style.top = `${rect.bottom + 5}px`;
        picker.style.left = `${rect.left}px`;

        // Закрыть при клике вне
        setTimeout(() => {
            document.addEventListener('click', function closePicker(e) {
                if (!e.target.closest('.reaction-picker') && !e.target.closest('[data-action="react"]')) {
                    picker.remove();
                    document.removeEventListener('click', closePicker);
                }
            });
        }, 100);
    }

    /**
     * Выбрать реакцию
     */
    async selectReaction(tournamentId, reactionId, button) {
        const wasActive = button.classList.contains('active');

        if (wasActive) {
            // Удалить реакцию
            this.removeReaction(tournamentId);
        } else {
            // Установить реакцию
            this.reactions[tournamentId] = reactionId;
            this.saveReactions();

            // Обновить UI
            this.updateReactionButton(tournamentId);

            // Анимация
            button.classList.add('reaction-animate');
            setTimeout(() => button.classList.remove('reaction-animate'), 500);

            // Отправить на сервер
            await this.syncWithServer(tournamentId, reactionId);

            // Уведомление
            const reaction = this.availableReactions.find(r => r.id === reactionId);
            if (reaction && window.notificationSystem) {
                window.notificationSystem.show(`Реакция "${reaction.label}" добавлена`, 'success');
            }

            // Отследить
            if (window.analyticsTracker) {
                window.analyticsTracker.track('tournament_reaction', { 
                    tournament_id: tournamentId, 
                    reaction: reactionId 
                });
            }
        }

        // Закрыть picker
        document.querySelectorAll('.reaction-picker').forEach(el => el.remove());
    }

    /**
     * Переключить реакцию (быстрый лайк)
     */
    toggleReaction(tournamentId, reactionId) {
        const currentReaction = this.reactions[tournamentId];

        if (currentReaction === reactionId) {
            this.removeReaction(tournamentId);
        } else {
            this.selectReaction(tournamentId, reactionId);
        }
    }

    /**
     * Удалить реакцию
     */
    removeReaction(tournamentId) {
        delete this.reactions[tournamentId];
        this.saveReactions();
        this.updateReactionButton(tournamentId);

        // Отправить на сервер
        this.syncWithServer(tournamentId, null);

        if (window.notificationSystem) {
            window.notificationSystem.show('Реакция удалена', 'info');
        }

        // Закрыть picker
        document.querySelectorAll('.reaction-picker').forEach(el => el.remove());
    }

    /**
     * Обновить кнопку реакции
     */
    updateReactionButton(tournamentId) {
        const card = document.querySelector(`[data-tournament-id="${tournamentId}"]`);
        if (!card) return;

        const reactionBtn = card.querySelector('[data-action="react"]');
        if (!reactionBtn) return;

        const currentReaction = this.reactions[tournamentId];

        if (currentReaction) {
            const reaction = this.availableReactions.find(r => r.id === currentReaction);
            if (reaction) {
                reactionBtn.classList.add('active');
                reactionBtn.innerHTML = `<i class="bi bi-${reaction.icon}"></i>`;
                reactionBtn.style.color = reaction.color;
                reactionBtn.title = reaction.label;
            }
        } else {
            reactionBtn.classList.remove('active');
            reactionBtn.innerHTML = '<i class="bi bi-emoji-smile"></i>';
            reactionBtn.style.color = '';
            reactionBtn.title = 'Добавить реакцию';
        }
    }

    /**
     * Обновить все кнопки реакций
     */
    updateAllReactionButtons() {
        Object.keys(this.reactions).forEach(tournamentId => {
            this.updateReactionButton(parseInt(tournamentId));
        });
    }

    /**
     * Синхронизация с сервером
     */
    async syncWithServer(tournamentId, reactionId) {
        try {
            const response = await fetch('/api/tournaments/reactions', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRF-Token': this.getCSRFToken()
                },
                body: JSON.stringify({
                    tournament_id: tournamentId,
                    reaction: reactionId
                })
            });

            if (!response.ok) {
                console.warn('Failed to sync reaction with server');
            }
        } catch (error) {
            console.error('Error syncing reaction:', error);
        }
    }

    /**
     * Получить CSRF токен
     */
    getCSRFToken() {
        return document.querySelector('meta[name="csrf-token"]')?.content || '';
    }

    /**
     * Получить статистику реакций
     */
    getReactionStats() {
        const stats = {};
        
        Object.values(this.reactions).forEach(reactionId => {
            stats[reactionId] = (stats[reactionId] || 0) + 1;
        });

        return stats;
    }

    /**
     * Экспорт реакций
     */
    exportReactions() {
        const json = JSON.stringify(this.reactions, null, 2);
        const blob = new Blob([json], { type: 'application/json' });
        const url = URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = 'tournament-reactions.json';
        a.click();
        URL.revokeObjectURL(url);
    }
}

// CSS стили
const style = document.createElement('style');
style.textContent = `
    .reaction-picker {
        position: fixed;
        background: var(--bg-primary);
        border: 1px solid var(--border-color);
        border-radius: 16px;
        box-shadow: 0 12px 32px rgba(0, 0, 0, 0.2);
        z-index: 1000;
        min-width: 280px;
        animation: reactionPickerIn 0.2s ease;
    }

    @keyframes reactionPickerIn {
        from {
            opacity: 0;
            transform: scale(0.9) translateY(-10px);
        }
        to {
            opacity: 1;
            transform: scale(1) translateY(0);
        }
    }

    .reaction-picker-header {
        display: flex;
        align-items: center;
        justify-content: space-between;
        padding: 1rem;
        border-bottom: 1px solid var(--border-color);
        font-weight: 600;
        font-size: 0.875rem;
    }

    .reaction-picker-list {
        padding: 0.5rem;
        display: grid;
        gap: 0.5rem;
    }

    .reaction-item {
        display: flex;
        align-items: center;
        gap: 0.75rem;
        padding: 0.75rem;
        border: 2px solid transparent;
        border-radius: 12px;
        background: var(--bg-secondary);
        cursor: pointer;
        transition: all 0.2s ease;
        font-weight: 500;
    }

    .reaction-item:hover {
        background: var(--bg-tertiary);
        transform: translateX(4px);
    }

    .reaction-item.active {
        border-color: var(--reaction-color);
        background: color-mix(in srgb, var(--reaction-color) 10%, transparent);
    }

    .reaction-item i {
        font-size: 1.5rem;
        color: var(--reaction-color);
    }

    .reaction-animate {
        animation: reactionPop 0.5s ease;
    }

    @keyframes reactionPop {
        0%, 100% { transform: scale(1); }
        25% { transform: scale(1.3) rotate(-10deg); }
        50% { transform: scale(1.1) rotate(10deg); }
        75% { transform: scale(1.2) rotate(-5deg); }
    }

    .reaction-remove-btn {
        width: 100%;
        padding: 0.75rem;
        border: none;
        border-top: 1px solid var(--border-color);
        background: transparent;
        color: var(--danger-color);
        font-weight: 500;
        cursor: pointer;
        transition: background 0.2s ease;
        border-radius: 0 0 16px 16px;
    }

    .reaction-remove-btn:hover {
        background: var(--bg-secondary);
    }

    [data-action="react"].active {
        animation: reactionPulse 2s infinite;
    }

    @keyframes reactionPulse {
        0%, 100% { transform: scale(1); }
        50% { transform: scale(1.1); }
    }

    /* Быстрая реакция */
    [data-action="quick-like"].active {
        color: #3b82f6 !important;
        background: rgba(59, 130, 246, 0.1);
    }
`;
document.head.appendChild(style);

// Инициализация
document.addEventListener('DOMContentLoaded', () => {
    window.tournamentReactions = new TournamentReactions();
    console.log('[Tournament Reactions] Initialized');
});

// Экспорт
if (typeof module !== 'undefined' && module.exports) {
    module.exports = TournamentReactions;
}
