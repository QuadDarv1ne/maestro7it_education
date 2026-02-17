/**
 * Tournament Tags System
 * Система тегов и закладок для турниров
 */

class TournamentTags {
    constructor() {
        this.tags = this.loadTags();
        this.tournamentTags = this.loadTournamentTags();
        this.init();
    }

    init() {
        this.createTagsPanel();
        this.attachEventListeners();
        this.updateTagsDisplay();
    }

    /**
     * Загрузить теги из localStorage
     */
    loadTags() {
        try {
            const stored = localStorage.getItem('tournamentTagsList');
            return stored ? JSON.parse(stored) : this.getDefaultTags();
        } catch (error) {
            console.error('Error loading tags:', error);
            return this.getDefaultTags();
        }
    }

    /**
     * Загрузить связи турниров с тегами
     */
    loadTournamentTags() {
        try {
            const stored = localStorage.getItem('tournamentTagsMap');
            return stored ? JSON.parse(stored) : {};
        } catch (error) {
            console.error('Error loading tournament tags:', error);
            return {};
        }
    }

    /**
     * Сохранить теги
     */
    saveTags() {
        try {
            localStorage.setItem('tournamentTagsList', JSON.stringify(this.tags));
            localStorage.setItem('tournamentTagsMap', JSON.stringify(this.tournamentTags));
        } catch (error) {
            console.error('Error saving tags:', error);
        }
    }

    /**
     * Получить теги по умолчанию
     */
    getDefaultTags() {
        return [
            { id: 'important', name: 'Важный', color: '#ef4444', icon: 'star-fill' },
            { id: 'interested', name: 'Интересует', color: '#3b82f6', icon: 'bookmark-fill' },
            { id: 'maybe', name: 'Возможно', color: '#f59e0b', icon: 'question-circle-fill' },
            { id: 'watching', name: 'Слежу', color: '#10b981', icon: 'eye-fill' },
            { id: 'participated', name: 'Участвовал', color: '#8b5cf6', icon: 'trophy-fill' }
        ];
    }

    /**
     * Создать панель тегов
     */
    createTagsPanel() {
        const panelHTML = `
            <div class="tournament-tags-panel" id="tournamentTagsPanel">
                <div class="tags-panel-header">
                    <h6 class="mb-0">
                        <i class="bi bi-tags"></i>
                        Мои теги
                    </h6>
                    <button class="btn btn-sm btn-ghost" onclick="window.tournamentTags.togglePanel()">
                        <i class="bi bi-x-lg"></i>
                    </button>
                </div>
                <div class="tags-panel-body">
                    <div class="tags-list" id="tagsList"></div>
                    <button class="btn btn-sm btn-outline-primary w-100 mt-3" onclick="window.tournamentTags.showAddTagDialog()">
                        <i class="bi bi-plus-lg"></i>
                        Добавить тег
                    </button>
                </div>
            </div>
            <div class="tags-panel-overlay" id="tagsPanelOverlay" onclick="window.tournamentTags.togglePanel()"></div>
        `;

        document.body.insertAdjacentHTML('beforeend', panelHTML);
    }

    /**
     * Прикрепить обработчики событий
     */
    attachEventListeners() {
        // Кнопка тегов на карточках
        document.addEventListener('click', (e) => {
            const tagBtn = e.target.closest('[data-action="tag"]');
            if (tagBtn) {
                e.preventDefault();
                e.stopPropagation();
                const tournamentId = parseInt(tagBtn.dataset.tournamentId);
                this.showTagSelector(tournamentId, tagBtn);
            }
        });

        // Клик по тегу для фильтрации
        document.addEventListener('click', (e) => {
            const tagBadge = e.target.closest('.tournament-tag-badge');
            if (tagBadge) {
                e.preventDefault();
                e.stopPropagation();
                const tagId = tagBadge.dataset.tagId;
                this.filterByTag(tagId);
            }
        });
    }

    /**
     * Показать селектор тегов
     */
    showTagSelector(tournamentId, button) {
        const currentTags = this.tournamentTags[tournamentId] || [];
        
        const selectorHTML = `
            <div class="tag-selector-dropdown">
                <div class="tag-selector-header">
                    <span>Выберите теги</span>
                    <button class="btn-close-sm" onclick="this.closest('.tag-selector-dropdown').remove()">
                        <i class="bi bi-x"></i>
                    </button>
                </div>
                <div class="tag-selector-list">
                    ${this.tags.map(tag => `
                        <label class="tag-selector-item">
                            <input type="checkbox" 
                                   value="${tag.id}" 
                                   ${currentTags.includes(tag.id) ? 'checked' : ''}
                                   onchange="window.tournamentTags.toggleTournamentTag(${tournamentId}, '${tag.id}', this.checked)">
                            <span class="tag-selector-label" style="color: ${tag.color}">
                                <i class="bi bi-${tag.icon}"></i>
                                ${tag.name}
                            </span>
                        </label>
                    `).join('')}
                </div>
            </div>
        `;

        // Удалить существующий селектор
        document.querySelectorAll('.tag-selector-dropdown').forEach(el => el.remove());

        // Добавить новый
        button.insertAdjacentHTML('afterend', selectorHTML);

        // Позиционирование
        const selector = button.nextElementSibling;
        const rect = button.getBoundingClientRect();
        selector.style.top = `${rect.bottom + 5}px`;
        selector.style.left = `${rect.left}px`;

        // Закрыть при клике вне
        setTimeout(() => {
            document.addEventListener('click', function closeSelector(e) {
                if (!e.target.closest('.tag-selector-dropdown') && !e.target.closest('[data-action="tag"]')) {
                    selector.remove();
                    document.removeEventListener('click', closeSelector);
                }
            });
        }, 100);
    }

    /**
     * Переключить тег для турнира
     */
    toggleTournamentTag(tournamentId, tagId, add) {
        if (!this.tournamentTags[tournamentId]) {
            this.tournamentTags[tournamentId] = [];
        }

        if (add) {
            if (!this.tournamentTags[tournamentId].includes(tagId)) {
                this.tournamentTags[tournamentId].push(tagId);
            }
        } else {
            this.tournamentTags[tournamentId] = this.tournamentTags[tournamentId].filter(id => id !== tagId);
        }

        this.saveTags();
        this.updateCardTags(tournamentId);

        // Уведомление
        const tag = this.tags.find(t => t.id === tagId);
        if (tag && window.notificationSystem) {
            window.notificationSystem.show(
                add ? `Тег "${tag.name}" добавлен` : `Тег "${tag.name}" удален`,
                'success'
            );
        }
    }

    /**
     * Обновить отображение тегов на карточке
     */
    updateCardTags(tournamentId) {
        const card = document.querySelector(`[data-tournament-id="${tournamentId}"]`);
        if (!card) return;

        let tagsContainer = card.querySelector('.tournament-tags-display');
        if (!tagsContainer) {
            tagsContainer = document.createElement('div');
            tagsContainer.className = 'tournament-tags-display';
            const cardBody = card.querySelector('.tournament-card-body');
            if (cardBody) {
                cardBody.appendChild(tagsContainer);
            }
        }

        const tournamentTagIds = this.tournamentTags[tournamentId] || [];
        if (tournamentTagIds.length === 0) {
            tagsContainer.innerHTML = '';
            return;
        }

        const tagsHTML = tournamentTagIds.map(tagId => {
            const tag = this.tags.find(t => t.id === tagId);
            if (!tag) return '';
            return `
                <span class="tournament-tag-badge" data-tag-id="${tag.id}" style="background-color: ${tag.color}20; color: ${tag.color}; border-color: ${tag.color}">
                    <i class="bi bi-${tag.icon}"></i>
                    ${tag.name}
                </span>
            `;
        }).join('');

        tagsContainer.innerHTML = tagsHTML;
    }

    /**
     * Обновить отображение всех тегов
     */
    updateTagsDisplay() {
        // Обновить все карточки
        Object.keys(this.tournamentTags).forEach(tournamentId => {
            this.updateCardTags(parseInt(tournamentId));
        });

        // Обновить панель тегов
        const tagsList = document.getElementById('tagsList');
        if (tagsList) {
            tagsList.innerHTML = this.tags.map(tag => {
                const count = Object.values(this.tournamentTags).filter(tags => tags.includes(tag.id)).length;
                return `
                    <div class="tag-item" style="border-left-color: ${tag.color}">
                        <div class="tag-item-info">
                            <i class="bi bi-${tag.icon}" style="color: ${tag.color}"></i>
                            <span>${tag.name}</span>
                            <span class="tag-count">${count}</span>
                        </div>
                        <div class="tag-item-actions">
                            <button class="btn-icon-sm" onclick="window.tournamentTags.filterByTag('${tag.id}')" title="Фильтровать">
                                <i class="bi bi-funnel"></i>
                            </button>
                            <button class="btn-icon-sm" onclick="window.tournamentTags.editTag('${tag.id}')" title="Редактировать">
                                <i class="bi bi-pencil"></i>
                            </button>
                            <button class="btn-icon-sm text-danger" onclick="window.tournamentTags.deleteTag('${tag.id}')" title="Удалить">
                                <i class="bi bi-trash"></i>
                            </button>
                        </div>
                    </div>
                `;
            }).join('');
        }
    }

    /**
     * Фильтровать турниры по тегу
     */
    filterByTag(tagId) {
        const tag = this.tags.find(t => t.id === tagId);
        if (!tag) return;

        // Скрыть все карточки
        document.querySelectorAll('[data-tournament-id]').forEach(card => {
            card.style.display = 'none';
        });

        // Показать только с этим тегом
        Object.entries(this.tournamentTags).forEach(([tournamentId, tags]) => {
            if (tags.includes(tagId)) {
                const card = document.querySelector(`[data-tournament-id="${tournamentId}"]`);
                if (card) {
                    card.style.display = '';
                }
            }
        });

        // Уведомление
        if (window.notificationSystem) {
            window.notificationSystem.show(`Фильтр: ${tag.name}`, 'info');
        }

        // Добавить кнопку сброса фильтра
        this.showClearFilterButton();
    }

    /**
     * Показать кнопку сброса фильтра
     */
    showClearFilterButton() {
        let clearBtn = document.getElementById('clearTagFilter');
        if (!clearBtn) {
            clearBtn = document.createElement('button');
            clearBtn.id = 'clearTagFilter';
            clearBtn.className = 'btn btn-outline-secondary btn-sm';
            clearBtn.innerHTML = '<i class="bi bi-x-circle"></i> Сбросить фильтр';
            clearBtn.onclick = () => this.clearFilter();

            const container = document.querySelector('.tournament-grid, .tournament-list');
            if (container) {
                container.parentElement.insertBefore(clearBtn, container);
            }
        }
    }

    /**
     * Очистить фильтр
     */
    clearFilter() {
        document.querySelectorAll('[data-tournament-id]').forEach(card => {
            card.style.display = '';
        });

        const clearBtn = document.getElementById('clearTagFilter');
        if (clearBtn) {
            clearBtn.remove();
        }
    }

    /**
     * Переключить панель тегов
     */
    togglePanel() {
        const panel = document.getElementById('tournamentTagsPanel');
        const overlay = document.getElementById('tagsPanelOverlay');
        
        if (panel && overlay) {
            panel.classList.toggle('active');
            overlay.classList.toggle('active');
        }
    }

    /**
     * Показать диалог добавления тега
     */
    showAddTagDialog() {
        const name = prompt('Название тега:');
        if (!name) return;

        const color = prompt('Цвет (hex):', '#3b82f6');
        const icon = prompt('Иконка Bootstrap (без bi-):', 'tag-fill');

        const newTag = {
            id: `custom_${Date.now()}`,
            name: name,
            color: color,
            icon: icon
        };

        this.tags.push(newTag);
        this.saveTags();
        this.updateTagsDisplay();

        if (window.notificationSystem) {
            window.notificationSystem.show(`Тег "${name}" создан`, 'success');
        }
    }

    /**
     * Редактировать тег
     */
    editTag(tagId) {
        const tag = this.tags.find(t => t.id === tagId);
        if (!tag) return;

        const name = prompt('Название тега:', tag.name);
        if (!name) return;

        tag.name = name;
        this.saveTags();
        this.updateTagsDisplay();
    }

    /**
     * Удалить тег
     */
    deleteTag(tagId) {
        if (!confirm('Удалить этот тег?')) return;

        this.tags = this.tags.filter(t => t.id !== tagId);
        
        // Удалить из всех турниров
        Object.keys(this.tournamentTags).forEach(tournamentId => {
            this.tournamentTags[tournamentId] = this.tournamentTags[tournamentId].filter(id => id !== tagId);
        });

        this.saveTags();
        this.updateTagsDisplay();
    }
}

// CSS стили
const style = document.createElement('style');
style.textContent = `
    .tournament-tags-panel {
        position: fixed;
        top: 0;
        right: -350px;
        width: 350px;
        height: 100vh;
        background: var(--bg-primary);
        box-shadow: -4px 0 20px rgba(0, 0, 0, 0.1);
        z-index: 1050;
        transition: right 0.3s ease;
        display: flex;
        flex-direction: column;
    }

    .tournament-tags-panel.active {
        right: 0;
    }

    .tags-panel-overlay {
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background: rgba(0, 0, 0, 0.5);
        z-index: 1049;
        opacity: 0;
        pointer-events: none;
        transition: opacity 0.3s ease;
    }

    .tags-panel-overlay.active {
        opacity: 1;
        pointer-events: all;
    }

    .tags-panel-header {
        display: flex;
        align-items: center;
        justify-content: space-between;
        padding: 1.5rem;
        border-bottom: 1px solid var(--border-color);
    }

    .tags-panel-body {
        flex: 1;
        overflow-y: auto;
        padding: 1.5rem;
    }

    .tag-item {
        display: flex;
        align-items: center;
        justify-content: space-between;
        padding: 0.75rem;
        margin-bottom: 0.5rem;
        background: var(--bg-secondary);
        border-radius: 8px;
        border-left: 3px solid;
        transition: all 0.2s ease;
    }

    .tag-item:hover {
        transform: translateX(4px);
    }

    .tag-item-info {
        display: flex;
        align-items: center;
        gap: 0.5rem;
        flex: 1;
    }

    .tag-count {
        margin-left: auto;
        padding: 0.25rem 0.5rem;
        background: var(--bg-tertiary);
        border-radius: 12px;
        font-size: 0.75rem;
        font-weight: 600;
    }

    .tag-item-actions {
        display: flex;
        gap: 0.25rem;
    }

    .btn-icon-sm {
        width: 28px;
        height: 28px;
        padding: 0;
        border: none;
        background: transparent;
        border-radius: 6px;
        cursor: pointer;
        transition: all 0.2s ease;
    }

    .btn-icon-sm:hover {
        background: var(--bg-tertiary);
    }

    .tournament-tags-display {
        display: flex;
        flex-wrap: wrap;
        gap: 0.5rem;
        margin-top: 0.75rem;
    }

    .tournament-tag-badge {
        display: inline-flex;
        align-items: center;
        gap: 0.25rem;
        padding: 0.25rem 0.75rem;
        border-radius: 12px;
        font-size: 0.75rem;
        font-weight: 600;
        border: 1px solid;
        cursor: pointer;
        transition: all 0.2s ease;
    }

    .tournament-tag-badge:hover {
        transform: translateY(-2px);
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
    }

    .tag-selector-dropdown {
        position: fixed;
        background: var(--bg-primary);
        border: 1px solid var(--border-color);
        border-radius: 12px;
        box-shadow: 0 8px 24px rgba(0, 0, 0, 0.15);
        z-index: 1000;
        min-width: 200px;
        max-width: 300px;
    }

    .tag-selector-header {
        display: flex;
        align-items: center;
        justify-content: space-between;
        padding: 0.75rem 1rem;
        border-bottom: 1px solid var(--border-color);
        font-weight: 600;
    }

    .tag-selector-list {
        padding: 0.5rem;
        max-height: 300px;
        overflow-y: auto;
    }

    .tag-selector-item {
        display: flex;
        align-items: center;
        gap: 0.5rem;
        padding: 0.5rem;
        border-radius: 6px;
        cursor: pointer;
        transition: background 0.2s ease;
    }

    .tag-selector-item:hover {
        background: var(--bg-secondary);
    }

    .tag-selector-label {
        display: flex;
        align-items: center;
        gap: 0.5rem;
        font-weight: 500;
    }

    #clearTagFilter {
        margin-bottom: 1rem;
    }
`;
document.head.appendChild(style);

// Инициализация
document.addEventListener('DOMContentLoaded', () => {
    window.tournamentTags = new TournamentTags();
    console.log('[Tournament Tags] Initialized');
});

// Экспорт
if (typeof module !== 'undefined' && module.exports) {
    module.exports = TournamentTags;
}
