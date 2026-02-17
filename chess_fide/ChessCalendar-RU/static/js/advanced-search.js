/**
 * Advanced Search with Autocomplete
 * Улучшенный поиск с автодополнением и историей
 */

class AdvancedSearch {
    constructor() {
        this.searchHistory = this.loadSearchHistory();
        this.recentSearches = [];
        this.searchCache = new Map();
        this.debounceTimer = null;
        this.currentQuery = '';
        this.init();
    }

    init() {
        this.attachEventListeners();
        this.createSearchDropdown();
    }

    /**
     * Загрузить историю поиска
     */
    loadSearchHistory() {
        try {
            const stored = localStorage.getItem('searchHistory');
            return stored ? JSON.parse(stored) : [];
        } catch (error) {
            console.error('Error loading search history:', error);
            return [];
        }
    }

    /**
     * Сохранить историю поиска
     */
    saveSearchHistory() {
        try {
            // Ограничиваем историю 50 записями
            const limited = this.searchHistory.slice(0, 50);
            localStorage.setItem('searchHistory', JSON.stringify(limited));
        } catch (error) {
            console.error('Error saving search history:', error);
        }
    }

    /**
     * Создать выпадающий список результатов
     */
    createSearchDropdown() {
        const dropdownHTML = `
            <div class="search-dropdown" id="searchDropdown">
                <div class="search-dropdown-content" id="searchDropdownContent"></div>
            </div>
        `;

        // Добавляем для каждого поля поиска
        document.querySelectorAll('#navbarSearchInput, #mobileSearchInput').forEach(input => {
            if (!input.nextElementSibling?.classList.contains('search-dropdown')) {
                input.insertAdjacentHTML('afterend', dropdownHTML);
            }
        });
    }

    /**
     * Прикрепить обработчики событий
     */
    attachEventListeners() {
        // Поиск в навигации
        const navbarSearch = document.getElementById('navbarSearchInput');
        const mobileSearch = document.getElementById('mobileSearchInput');

        [navbarSearch, mobileSearch].forEach(input => {
            if (!input) return;

            // Ввод текста
            input.addEventListener('input', (e) => {
                this.handleSearchInput(e.target);
            });

            // Фокус - показать историю
            input.addEventListener('focus', (e) => {
                if (!e.target.value) {
                    this.showSearchHistory(e.target);
                }
            });

            // Клавиши навигации
            input.addEventListener('keydown', (e) => {
                this.handleKeyNavigation(e, e.target);
            });

            // Потеря фокуса - скрыть dropdown
            input.addEventListener('blur', (e) => {
                setTimeout(() => {
                    this.hideDropdown(e.target);
                }, 200);
            });
        });

        // Кнопка очистки
        document.querySelectorAll('.navbar-search-clear').forEach(btn => {
            btn.addEventListener('click', (e) => {
                const input = e.target.closest('.navbar-search-enhanced').querySelector('input');
                if (input) {
                    input.value = '';
                    input.focus();
                    this.hideDropdown(input);
                }
            });
        });

        // Клик вне поиска
        document.addEventListener('click', (e) => {
            if (!e.target.closest('.navbar-search-enhanced')) {
                document.querySelectorAll('.search-dropdown').forEach(dropdown => {
                    dropdown.classList.remove('active');
                });
            }
        });
    }

    /**
     * Обработка ввода в поиск
     */
    handleSearchInput(input) {
        const query = input.value.trim();
        this.currentQuery = query;

        // Показать/скрыть кнопку очистки
        const clearBtn = input.closest('.navbar-search-enhanced').querySelector('.navbar-search-clear');
        if (clearBtn) {
            clearBtn.style.display = query ? 'flex' : 'none';
        }

        if (query.length < 2) {
            if (query.length === 0) {
                this.showSearchHistory(input);
            } else {
                this.hideDropdown(input);
            }
            return;
        }

        // Debounce поиска
        clearTimeout(this.debounceTimer);
        this.debounceTimer = setTimeout(() => {
            this.performSearch(query, input);
        }, 300);
    }

    /**
     * Выполнить поиск
     */
    async performSearch(query, input) {
        // Проверить кэш
        if (this.searchCache.has(query)) {
            this.showResults(this.searchCache.get(query), input);
            return;
        }

        try {
            const response = await fetch(`/api/tournaments/search?q=${encodeURIComponent(query)}&limit=10`);
            if (!response.ok) throw new Error('Search failed');

            const results = await response.json();
            
            // Сохранить в кэш
            this.searchCache.set(query, results);
            
            // Показать результаты
            this.showResults(results, input);

            // Отследить поиск
            if (window.analyticsTracker) {
                window.analyticsTracker.track('search', { query, results_count: results.length });
            }
        } catch (error) {
            console.error('Search error:', error);
            this.showError(input);
        }
    }

    /**
     * Показать результаты поиска
     */
    showResults(results, input) {
        const dropdown = input.nextElementSibling;
        if (!dropdown) return;

        const content = dropdown.querySelector('.search-dropdown-content');
        if (!content) return;

        if (results.length === 0) {
            content.innerHTML = `
                <div class="search-dropdown-empty">
                    <i class="bi bi-search"></i>
                    <p>Ничего не найдено</p>
                    <small>Попробуйте изменить запрос</small>
                </div>
            `;
        } else {
            content.innerHTML = `
                <div class="search-dropdown-header">
                    <span>Найдено турниров: ${results.length}</span>
                </div>
                ${results.map((tournament, index) => `
                    <div class="search-dropdown-item" data-index="${index}" data-tournament-id="${tournament.id}">
                        <div class="search-item-icon">
                            <i class="bi bi-trophy"></i>
                        </div>
                        <div class="search-item-content">
                            <div class="search-item-title">${this.highlightQuery(tournament.name, this.currentQuery)}</div>
                            <div class="search-item-meta">
                                <span><i class="bi bi-geo-alt"></i> ${tournament.location}</span>
                                <span><i class="bi bi-calendar"></i> ${this.formatDate(tournament.start_date)}</span>
                            </div>
                        </div>
                        <div class="search-item-badge">
                            <span class="badge bg-${this.getStatusColor(tournament.status)}">${tournament.status}</span>
                        </div>
                    </div>
                `).join('')}
            `;

            // Обработчики кликов
            content.querySelectorAll('.search-dropdown-item').forEach(item => {
                item.addEventListener('click', () => {
                    const tournamentId = item.dataset.tournamentId;
                    this.selectResult(tournamentId, input);
                });
            });
        }

        dropdown.classList.add('active');
    }

    /**
     * Показать историю поиска
     */
    showSearchHistory(input) {
        if (this.searchHistory.length === 0) return;

        const dropdown = input.nextElementSibling;
        if (!dropdown) return;

        const content = dropdown.querySelector('.search-dropdown-content');
        if (!content) return;

        content.innerHTML = `
            <div class="search-dropdown-header">
                <span>История поиска</span>
                <button class="btn-link-sm" onclick="window.advancedSearch.clearHistory()">
                    Очистить
                </button>
            </div>
            ${this.searchHistory.slice(0, 10).map((item, index) => `
                <div class="search-dropdown-item search-history-item" data-index="${index}">
                    <div class="search-item-icon">
                        <i class="bi bi-clock-history"></i>
                    </div>
                    <div class="search-item-content">
                        <div class="search-item-title">${item.query}</div>
                        <div class="search-item-meta">
                            <small>${this.formatTimeAgo(item.timestamp)}</small>
                        </div>
                    </div>
                    <button class="btn-icon-sm" onclick="window.advancedSearch.removeFromHistory(${index}); event.stopPropagation();">
                        <i class="bi bi-x"></i>
                    </button>
                </div>
            `).join('')}
        `;

        // Обработчики кликов
        content.querySelectorAll('.search-history-item').forEach(item => {
            item.addEventListener('click', () => {
                const index = parseInt(item.dataset.index);
                const historyItem = this.searchHistory[index];
                input.value = historyItem.query;
                this.handleSearchInput(input);
            });
        });

        dropdown.classList.add('active');
    }

    /**
     * Показать ошибку
     */
    showError(input) {
        const dropdown = input.nextElementSibling;
        if (!dropdown) return;

        const content = dropdown.querySelector('.search-dropdown-content');
        if (!content) return;

        content.innerHTML = `
            <div class="search-dropdown-empty">
                <i class="bi bi-exclamation-triangle text-danger"></i>
                <p>Ошибка поиска</p>
                <small>Попробуйте позже</small>
            </div>
        `;

        dropdown.classList.add('active');
    }

    /**
     * Скрыть dropdown
     */
    hideDropdown(input) {
        const dropdown = input.nextElementSibling;
        if (dropdown) {
            dropdown.classList.remove('active');
        }
    }

    /**
     * Выбрать результат
     */
    selectResult(tournamentId, input) {
        // Добавить в историю
        this.addToHistory(this.currentQuery);

        // Перейти на страницу турнира
        window.location.href = `/tournament/${tournamentId}`;
    }

    /**
     * Добавить в историю поиска
     */
    addToHistory(query) {
        if (!query || query.length < 2) return;

        // Удалить дубликаты
        this.searchHistory = this.searchHistory.filter(item => item.query !== query);

        // Добавить в начало
        this.searchHistory.unshift({
            query: query,
            timestamp: Date.now()
        });

        this.saveSearchHistory();
    }

    /**
     * Удалить из истории
     */
    removeFromHistory(index) {
        this.searchHistory.splice(index, 1);
        this.saveSearchHistory();
        
        // Обновить отображение
        const input = document.querySelector('#navbarSearchInput, #mobileSearchInput');
        if (input && !input.value) {
            this.showSearchHistory(input);
        }
    }

    /**
     * Очистить историю
     */
    clearHistory() {
        if (!confirm('Очистить всю историю поиска?')) return;

        this.searchHistory = [];
        this.saveSearchHistory();

        // Скрыть dropdown
        document.querySelectorAll('.search-dropdown').forEach(dropdown => {
            dropdown.classList.remove('active');
        });

        if (window.notificationSystem) {
            window.notificationSystem.show('История поиска очищена', 'success');
        }
    }

    /**
     * Обработка навигации клавишами
     */
    handleKeyNavigation(e, input) {
        const dropdown = input.nextElementSibling;
        if (!dropdown || !dropdown.classList.contains('active')) return;

        const items = dropdown.querySelectorAll('.search-dropdown-item');
        if (items.length === 0) return;

        let currentIndex = -1;
        items.forEach((item, index) => {
            if (item.classList.contains('active')) {
                currentIndex = index;
            }
        });

        switch (e.key) {
            case 'ArrowDown':
                e.preventDefault();
                currentIndex = (currentIndex + 1) % items.length;
                break;
            case 'ArrowUp':
                e.preventDefault();
                currentIndex = currentIndex <= 0 ? items.length - 1 : currentIndex - 1;
                break;
            case 'Enter':
                e.preventDefault();
                if (currentIndex >= 0) {
                    items[currentIndex].click();
                }
                return;
            case 'Escape':
                this.hideDropdown(input);
                return;
            default:
                return;
        }

        // Обновить активный элемент
        items.forEach((item, index) => {
            item.classList.toggle('active', index === currentIndex);
        });

        // Прокрутить к активному элементу
        if (currentIndex >= 0) {
            items[currentIndex].scrollIntoView({ block: 'nearest' });
        }
    }

    /**
     * Подсветить запрос в тексте
     */
    highlightQuery(text, query) {
        if (!query) return text;
        
        const regex = new RegExp(`(${query})`, 'gi');
        return text.replace(regex, '<mark>$1</mark>');
    }

    /**
     * Форматировать дату
     */
    formatDate(dateString) {
        if (!dateString) return 'Не указана';
        const date = new Date(dateString);
        return date.toLocaleDateString('ru-RU', { day: '2-digit', month: '2-digit', year: 'numeric' });
    }

    /**
     * Форматировать время назад
     */
    formatTimeAgo(timestamp) {
        const seconds = Math.floor((Date.now() - timestamp) / 1000);
        
        if (seconds < 60) return 'только что';
        if (seconds < 3600) return `${Math.floor(seconds / 60)} мин назад`;
        if (seconds < 86400) return `${Math.floor(seconds / 3600)} ч назад`;
        if (seconds < 604800) return `${Math.floor(seconds / 86400)} дн назад`;
        
        return new Date(timestamp).toLocaleDateString('ru-RU');
    }

    /**
     * Получить цвет статуса
     */
    getStatusColor(status) {
        const colors = {
            'Scheduled': 'primary',
            'Ongoing': 'warning',
            'Completed': 'success',
            'Cancelled': 'danger'
        };
        return colors[status] || 'secondary';
    }

    /**
     * Очистить кэш
     */
    clearCache() {
        this.searchCache.clear();
    }
}

// CSS стили
const style = document.createElement('style');
style.textContent = `
    .search-dropdown {
        position: absolute;
        top: calc(100% + 8px);
        left: 0;
        right: 0;
        background: var(--bg-primary);
        border: 1px solid var(--border-color);
        border-radius: 12px;
        box-shadow: 0 8px 24px rgba(0, 0, 0, 0.15);
        max-height: 500px;
        overflow-y: auto;
        z-index: 1000;
        opacity: 0;
        transform: translateY(-10px);
        pointer-events: none;
        transition: all 0.2s ease;
    }

    .search-dropdown.active {
        opacity: 1;
        transform: translateY(0);
        pointer-events: all;
    }

    .search-dropdown-header {
        display: flex;
        align-items: center;
        justify-content: space-between;
        padding: 0.75rem 1rem;
        border-bottom: 1px solid var(--border-color);
        font-size: 0.875rem;
        font-weight: 600;
        color: var(--text-secondary);
    }

    .search-dropdown-item {
        display: flex;
        align-items: center;
        gap: 0.75rem;
        padding: 0.75rem 1rem;
        cursor: pointer;
        transition: all 0.2s ease;
        border-bottom: 1px solid var(--border-color);
    }

    .search-dropdown-item:last-child {
        border-bottom: none;
    }

    .search-dropdown-item:hover,
    .search-dropdown-item.active {
        background: var(--bg-secondary);
    }

    .search-item-icon {
        width: 40px;
        height: 40px;
        display: flex;
        align-items: center;
        justify-content: center;
        background: var(--bg-secondary);
        border-radius: 10px;
        font-size: 1.25rem;
        color: var(--primary-color);
        flex-shrink: 0;
    }

    .search-item-content {
        flex: 1;
        min-width: 0;
    }

    .search-item-title {
        font-weight: 600;
        color: var(--text-primary);
        margin-bottom: 0.25rem;
        overflow: hidden;
        text-overflow: ellipsis;
        white-space: nowrap;
    }

    .search-item-title mark {
        background: var(--warning-color);
        color: var(--dark-color);
        padding: 0.1rem 0.2rem;
        border-radius: 3px;
    }

    .search-item-meta {
        display: flex;
        gap: 1rem;
        font-size: 0.75rem;
        color: var(--text-secondary);
    }

    .search-item-meta span {
        display: flex;
        align-items: center;
        gap: 0.25rem;
    }

    .search-item-badge {
        flex-shrink: 0;
    }

    .search-dropdown-empty {
        padding: 3rem 1rem;
        text-align: center;
        color: var(--text-secondary);
    }

    .search-dropdown-empty i {
        font-size: 3rem;
        margin-bottom: 1rem;
        opacity: 0.5;
    }

    .search-dropdown-empty p {
        font-weight: 600;
        margin-bottom: 0.5rem;
    }

    .btn-link-sm {
        padding: 0;
        border: none;
        background: none;
        color: var(--primary-color);
        font-size: 0.875rem;
        cursor: pointer;
        transition: opacity 0.2s ease;
    }

    .btn-link-sm:hover {
        opacity: 0.7;
    }

    .navbar-search-clear {
        display: none;
    }

    /* Скроллбар для dropdown */
    .search-dropdown::-webkit-scrollbar {
        width: 6px;
    }

    .search-dropdown::-webkit-scrollbar-track {
        background: var(--bg-secondary);
    }

    .search-dropdown::-webkit-scrollbar-thumb {
        background: var(--border-color);
        border-radius: 3px;
    }

    .search-dropdown::-webkit-scrollbar-thumb:hover {
        background: var(--text-muted);
    }
`;
document.head.appendChild(style);

// Инициализация
document.addEventListener('DOMContentLoaded', () => {
    window.advancedSearch = new AdvancedSearch();
    console.log('[Advanced Search] Initialized');
});

// Экспорт
if (typeof module !== 'undefined' && module.exports) {
    module.exports = AdvancedSearch;
}
