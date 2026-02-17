/**
 * Система быстрых действий для карточек турниров
 * Контекстное меню, горячие клавиши, drag & drop
 */

class QuickActions {
    constructor() {
        this.selectedCards = new Set();
        this.contextMenu = null;
        this.init();
    }

    init() {
        this.createContextMenu();
        this.attachEventListeners();
        this.registerKeyboardShortcuts();
    }

    /**
     * Создание контекстного меню
     */
    createContextMenu() {
        this.contextMenu = document.createElement('div');
        this.contextMenu.id = 'tournamentContextMenu';
        this.contextMenu.className = 'context-menu';
        this.contextMenu.innerHTML = `
            <div class="context-menu-item" data-action="open">
                <i class="bi bi-box-arrow-up-right"></i>
                <span>Открыть</span>
                <kbd>Enter</kbd>
            </div>
            <div class="context-menu-item" data-action="favorite">
                <i class="bi bi-heart"></i>
                <span>В избранное</span>
                <kbd>F</kbd>
            </div>
            <div class="context-menu-item" data-action="compare">
                <i class="bi bi-bar-chart"></i>
                <span>Сравнить</span>
                <kbd>C</kbd>
            </div>
            <div class="context-menu-divider"></div>
            <div class="context-menu-item" data-action="share">
                <i class="bi bi-share"></i>
                <span>Поделиться</span>
                <kbd>S</kbd>
            </div>
            <div class="context-menu-item" data-action="export">
                <i class="bi bi-download"></i>
                <span>Экспорт</span>
                <kbd>E</kbd>
            </div>
            <div class="context-menu-divider"></div>
            <div class="context-menu-item" data-action="notify">
                <i class="bi bi-bell"></i>
                <span>Уведомить</span>
                <kbd>N</kbd>
            </div>
        `;
        document.body.appendChild(this.contextMenu);
    }

    /**
     * Прикрепление обработчиков событий
     */
    attachEventListeners() {
        // Правый клик на карточках
        document.addEventListener('contextmenu', (e) => {
            const card = e.target.closest('[data-tournament-id]');
            if (card) {
                e.preventDefault();
                this.showContextMenu(e, card);
            }
        });

        // Клик вне меню - закрыть
        document.addEventListener('click', (e) => {
            if (!e.target.closest('.context-menu')) {
                this.hideContextMenu();
            }
        });

        // Клик по пункту меню
        this.contextMenu.addEventListener('click', (e) => {
            const item = e.target.closest('.context-menu-item');
            if (item) {
                const action = item.dataset.action;
                const card = this.contextMenu.dataset.cardId;
                this.executeAction(action, card);
                this.hideContextMenu();
            }
        });

        // Выделение карточек (Ctrl/Cmd + Click)
        document.addEventListener('click', (e) => {
            if (e.ctrlKey || e.metaKey) {
                const card = e.target.closest('[data-tournament-id]');
                if (card) {
                    e.preventDefault();
                    this.toggleCardSelection(card);
                }
            }
        });

        // Drag & Drop
        this.setupDragAndDrop();
    }

    /**
     * Показать контекстное меню
     */
    showContextMenu(event, card) {
        const tournamentId = card.dataset.tournamentId;
        this.contextMenu.dataset.cardId = tournamentId;

        // Позиционирование
        const x = event.pageX;
        const y = event.pageY;
        
        this.contextMenu.style.left = `${x}px`;
        this.contextMenu.style.top = `${y}px`;
        this.contextMenu.classList.add('show');

        // Проверка выхода за границы экрана
        requestAnimationFrame(() => {
            const rect = this.contextMenu.getBoundingClientRect();
            
            if (rect.right > window.innerWidth) {
                this.contextMenu.style.left = `${x - rect.width}px`;
            }
            
            if (rect.bottom > window.innerHeight) {
                this.contextMenu.style.top = `${y - rect.height}px`;
            }
        });
    }

    /**
     * Скрыть контекстное меню
     */
    hideContextMenu() {
        this.contextMenu.classList.remove('show');
    }

    /**
     * Выполнить действие
     */
    executeAction(action, tournamentId) {
        const card = document.querySelector(`[data-tournament-id="${tournamentId}"]`);
        if (!card) return;

        switch (action) {
            case 'open':
                window.location.href = `/tournament/${tournamentId}`;
                break;
            
            case 'favorite':
                const favoriteBtn = card.querySelector('[data-action="favorite"]');
                if (favoriteBtn) favoriteBtn.click();
                break;
            
            case 'compare':
                const compareBtn = card.querySelector('[data-action="compare"]');
                if (compareBtn) compareBtn.click();
                break;
            
            case 'share':
                const shareBtn = card.querySelector('[data-action="share"]');
                if (shareBtn) shareBtn.click();
                break;
            
            case 'export':
                const exportBtn = card.querySelector('[data-action="export"]');
                if (exportBtn) exportBtn.click();
                break;
            
            case 'notify':
                const notifyBtn = card.querySelector('[data-action="notify"]');
                if (notifyBtn) notifyBtn.click();
                break;
        }
    }

    /**
     * Регистрация горячих клавиш
     */
    registerKeyboardShortcuts() {
        document.addEventListener('keydown', (e) => {
            // Игнорируем если фокус в input/textarea
            if (e.target.matches('input, textarea')) {
                return;
            }

            const focusedCard = document.querySelector('[data-tournament-id]:focus');
            if (!focusedCard) return;

            const tournamentId = focusedCard.dataset.tournamentId;

            switch (e.key.toLowerCase()) {
                case 'enter':
                    e.preventDefault();
                    this.executeAction('open', tournamentId);
                    break;
                
                case 'f':
                    e.preventDefault();
                    this.executeAction('favorite', tournamentId);
                    break;
                
                case 'c':
                    e.preventDefault();
                    this.executeAction('compare', tournamentId);
                    break;
                
                case 's':
                    e.preventDefault();
                    this.executeAction('share', tournamentId);
                    break;
                
                case 'e':
                    e.preventDefault();
                    this.executeAction('export', tournamentId);
                    break;
                
                case 'n':
                    e.preventDefault();
                    this.executeAction('notify', tournamentId);
                    break;
            }
        });

        // Навигация стрелками
        document.addEventListener('keydown', (e) => {
            if (e.target.matches('input, textarea')) {
                return;
            }

            const focusedCard = document.querySelector('[data-tournament-id]:focus');
            if (!focusedCard) return;

            const cards = Array.from(document.querySelectorAll('[data-tournament-id]'));
            const currentIndex = cards.indexOf(focusedCard);

            let nextIndex = currentIndex;

            switch (e.key) {
                case 'ArrowDown':
                case 'ArrowRight':
                    e.preventDefault();
                    nextIndex = Math.min(currentIndex + 1, cards.length - 1);
                    break;
                
                case 'ArrowUp':
                case 'ArrowLeft':
                    e.preventDefault();
                    nextIndex = Math.max(currentIndex - 1, 0);
                    break;
            }

            if (nextIndex !== currentIndex) {
                cards[nextIndex].focus();
                cards[nextIndex].scrollIntoView({ behavior: 'smooth', block: 'center' });
            }
        });
    }

    /**
     * Переключение выделения карточки
     */
    toggleCardSelection(card) {
        const tournamentId = card.dataset.tournamentId;
        
        if (this.selectedCards.has(tournamentId)) {
            this.selectedCards.delete(tournamentId);
            card.classList.remove('selected');
        } else {
            this.selectedCards.add(tournamentId);
            card.classList.add('selected');
        }

        this.updateSelectionUI();
    }

    /**
     * Обновление UI выделения
     */
    updateSelectionUI() {
        const count = this.selectedCards.size;
        
        if (count > 0) {
            this.showSelectionToolbar(count);
        } else {
            this.hideSelectionToolbar();
        }
    }

    /**
     * Показать панель выделения
     */
    showSelectionToolbar(count) {
        let toolbar = document.getElementById('selectionToolbar');
        
        if (!toolbar) {
            toolbar = document.createElement('div');
            toolbar.id = 'selectionToolbar';
            toolbar.className = 'selection-toolbar';
            toolbar.innerHTML = `
                <div class="selection-info">
                    <span class="selection-count">${count}</span> выбрано
                </div>
                <div class="selection-actions">
                    <button class="btn btn-sm btn-primary" onclick="quickActions.compareSelected()">
                        <i class="bi bi-bar-chart"></i> Сравнить
                    </button>
                    <button class="btn btn-sm btn-outline-danger" onclick="quickActions.addSelectedToFavorites()">
                        <i class="bi bi-heart"></i> В избранное
                    </button>
                    <button class="btn btn-sm btn-outline-secondary" onclick="quickActions.clearSelection()">
                        <i class="bi bi-x"></i> Отменить
                    </button>
                </div>
            `;
            document.body.appendChild(toolbar);
        } else {
            toolbar.querySelector('.selection-count').textContent = count;
        }

        toolbar.classList.add('show');
    }

    /**
     * Скрыть панель выделения
     */
    hideSelectionToolbar() {
        const toolbar = document.getElementById('selectionToolbar');
        if (toolbar) {
            toolbar.classList.remove('show');
        }
    }

    /**
     * Очистить выделение
     */
    clearSelection() {
        this.selectedCards.clear();
        document.querySelectorAll('[data-tournament-id].selected').forEach(card => {
            card.classList.remove('selected');
        });
        this.hideSelectionToolbar();
    }

    /**
     * Сравнить выбранные
     */
    compareSelected() {
        if (window.tournamentComparison) {
            this.selectedCards.forEach(id => {
                const card = document.querySelector(`[data-tournament-id="${id}"]`);
                if (card) {
                    const compareBtn = card.querySelector('[data-action="compare"]');
                    if (compareBtn) compareBtn.click();
                }
            });
            this.clearSelection();
        }
    }

    /**
     * Добавить выбранные в избранное
     */
    addSelectedToFavorites() {
        if (window.tournamentCardManager) {
            this.selectedCards.forEach(id => {
                const card = document.querySelector(`[data-tournament-id="${id}"]`);
                if (card) {
                    const favoriteBtn = card.querySelector('[data-action="favorite"]');
                    if (favoriteBtn) favoriteBtn.click();
                }
            });
            this.clearSelection();
        }
    }

    /**
     * Настройка Drag & Drop
     */
    setupDragAndDrop() {
        document.addEventListener('dragstart', (e) => {
            const card = e.target.closest('[data-tournament-id]');
            if (card) {
                card.classList.add('dragging');
                e.dataTransfer.effectAllowed = 'move';
                e.dataTransfer.setData('text/plain', card.dataset.tournamentId);
            }
        });

        document.addEventListener('dragend', (e) => {
            const card = e.target.closest('[data-tournament-id]');
            if (card) {
                card.classList.remove('dragging');
            }
        });

        // Можно добавить drop zones для различных действий
    }
}

// CSS стили
const style = document.createElement('style');
style.textContent = `
    .context-menu {
        position: absolute;
        background: white;
        border-radius: 0.5rem;
        box-shadow: 0 10px 40px rgba(0, 0, 0, 0.2);
        padding: 0.5rem 0;
        min-width: 200px;
        z-index: 10000;
        opacity: 0;
        transform: scale(0.95);
        pointer-events: none;
        transition: all 0.15s ease;
    }

    .context-menu.show {
        opacity: 1;
        transform: scale(1);
        pointer-events: auto;
    }

    .context-menu-item {
        display: flex;
        align-items: center;
        gap: 0.75rem;
        padding: 0.625rem 1rem;
        cursor: pointer;
        transition: background 0.15s;
        color: #374151;
    }

    .context-menu-item:hover {
        background: #f3f4f6;
    }

    .context-menu-item i {
        width: 20px;
        font-size: 1rem;
        color: #6b7280;
    }

    .context-menu-item span {
        flex: 1;
        font-size: 0.875rem;
    }

    .context-menu-item kbd {
        padding: 0.125rem 0.375rem;
        background: #f3f4f6;
        border: 1px solid #e5e7eb;
        border-radius: 0.25rem;
        font-size: 0.75rem;
        font-family: monospace;
        color: #6b7280;
    }

    .context-menu-divider {
        height: 1px;
        background: #e5e7eb;
        margin: 0.5rem 0;
    }

    [data-tournament-id].selected {
        outline: 3px solid #3b82f6;
        outline-offset: 2px;
    }

    [data-tournament-id].dragging {
        opacity: 0.5;
    }

    .selection-toolbar {
        position: fixed;
        bottom: 2rem;
        left: 50%;
        transform: translateX(-50%) translateY(100px);
        background: white;
        padding: 1rem 1.5rem;
        border-radius: 1rem;
        box-shadow: 0 10px 40px rgba(0, 0, 0, 0.15);
        display: flex;
        align-items: center;
        gap: 1.5rem;
        z-index: 1000;
        opacity: 0;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    }

    .selection-toolbar.show {
        transform: translateX(-50%) translateY(0);
        opacity: 1;
    }

    .selection-info {
        display: flex;
        align-items: center;
        gap: 0.5rem;
        font-weight: 500;
        color: #374151;
    }

    .selection-count {
        display: inline-flex;
        align-items: center;
        justify-content: center;
        min-width: 24px;
        height: 24px;
        padding: 0 8px;
        background: #3b82f6;
        color: white;
        border-radius: 12px;
        font-size: 0.875rem;
        font-weight: 600;
    }

    .selection-actions {
        display: flex;
        gap: 0.5rem;
    }

    [data-tournament-id] {
        cursor: pointer;
        user-select: none;
    }

    [data-tournament-id]:focus {
        outline: 2px solid #3b82f6;
        outline-offset: 2px;
    }

    @media (max-width: 768px) {
        .selection-toolbar {
            left: 1rem;
            right: 1rem;
            transform: translateX(0) translateY(100px);
            flex-direction: column;
            gap: 1rem;
        }

        .selection-toolbar.show {
            transform: translateX(0) translateY(0);
        }

        .selection-actions {
            width: 100%;
            flex-direction: column;
        }

        .selection-actions button {
            width: 100%;
        }
    }
`;
document.head.appendChild(style);

// Инициализация
document.addEventListener('DOMContentLoaded', () => {
    window.quickActions = new QuickActions();
    
    // Делаем карточки focusable
    document.querySelectorAll('[data-tournament-id]').forEach(card => {
        card.setAttribute('tabindex', '0');
        card.setAttribute('draggable', 'true');
    });
});

// Экспорт
if (typeof module !== 'undefined' && module.exports) {
    module.exports = QuickActions;
}
