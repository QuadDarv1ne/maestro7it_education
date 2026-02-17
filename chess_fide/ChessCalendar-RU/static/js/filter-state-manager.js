/**
 * Filter State Manager
 * Управление состоянием фильтров с сохранением
 */

class FilterStateManager {
    constructor() {
        this.currentState = this.loadState();
        this.defaultState = this.getDefaultState();
        this.init();
    }

    init() {
        this.attachEventListeners();
        this.applyState();
        this.syncWithURL();
    }

    /**
     * Получить состояние по умолчанию
     */
    getDefaultState() {
        return {
            category: '',
            location: '',
            status: '',
            dateFrom: '',
            dateTo: '',
            sortBy: 'start_date',
            sortOrder: 'asc',
            viewMode: 'grid', // grid или list
            perPage: 20
        };
    }

    /**
     * Загрузить состояние
     */
    loadState() {
        try {
            const stored = localStorage.getItem('filterState');
            return stored ? { ...this.getDefaultState(), ...JSON.parse(stored) } : this.getDefaultState();
        } catch (error) {
            console.error('Error loading filter state:', error);
            return this.getDefaultState();
        }
    }

    /**
     * Сохранить состояние
     */
    saveState() {
        try {
            localStorage.setItem('filterState', JSON.stringify(this.currentState));
            this.syncWithURL();
        } catch (error) {
            console.error('Error saving filter state:', error);
        }
    }

    /**
     * Прикрепить обработчики событий
     */
    attachEventListeners() {
        // Фильтры
        document.querySelectorAll('[data-filter]').forEach(filter => {
            filter.addEventListener('change', (e) => {
                const filterName = e.target.dataset.filter;
                const value = e.target.value;
                this.updateFilter(filterName, value);
            });
        });

        // Сортировка
        document.querySelectorAll('[data-sort]').forEach(sortBtn => {
            sortBtn.addEventListener('click', (e) => {
                e.preventDefault();
                const sortBy = e.currentTarget.dataset.sort;
                this.updateSort(sortBy);
            });
        });

        // Режим отображения
        document.querySelectorAll('[data-view-mode]').forEach(btn => {
            btn.addEventListener('click', (e) => {
                e.preventDefault();
                const mode = e.currentTarget.dataset.viewMode;
                this.updateViewMode(mode);
            });
        });

        // Кнопка сброса фильтров
        document.querySelectorAll('[data-action="reset-filters"]').forEach(btn => {
            btn.addEventListener('click', (e) => {
                e.preventDefault();
                this.resetFilters();
            });
        });

        // Сохранение пресета
        document.querySelectorAll('[data-action="save-preset"]').forEach(btn => {
            btn.addEventListener('click', (e) => {
                e.preventDefault();
                this.savePreset();
            });
        });

        // Загрузка пресета
        document.querySelectorAll('[data-preset]').forEach(btn => {
            btn.addEventListener('click', (e) => {
                e.preventDefault();
                const presetName = e.currentTarget.dataset.preset;
                this.loadPreset(presetName);
            });
        });
    }

    /**
     * Обновить фильтр
     */
    updateFilter(filterName, value) {
        this.currentState[filterName] = value;
        this.saveState();
        this.applyFilters();

        // Отследить изменение
        if (window.analyticsTracker) {
            window.analyticsTracker.track('filter_change', { filter: filterName, value });
        }
    }

    /**
     * Обновить сортировку
     */
    updateSort(sortBy) {
        if (this.currentState.sortBy === sortBy) {
            // Переключить порядок
            this.currentState.sortOrder = this.currentState.sortOrder === 'asc' ? 'desc' : 'asc';
        } else {
            this.currentState.sortBy = sortBy;
            this.currentState.sortOrder = 'asc';
        }

        this.saveState();
        this.applySort();
        this.updateSortButtons();
    }

    /**
     * Обновить режим отображения
     */
    updateViewMode(mode) {
        this.currentState.viewMode = mode;
        this.saveState();
        this.applyViewMode();
        this.updateViewModeButtons();
    }

    /**
     * Применить состояние
     */
    applyState() {
        this.applyFilters();
        this.applySort();
        this.applyViewMode();
        this.updateUI();
    }

    /**
     * Применить фильтры
     */
    applyFilters() {
        // Обновить значения в UI
        Object.entries(this.currentState).forEach(([key, value]) => {
            const filter = document.querySelector(`[data-filter="${key}"]`);
            if (filter) {
                filter.value = value;
            }
        });

        // Применить фильтры к турнирам
        this.filterTournaments();
    }

    /**
     * Фильтровать турниры
     */
    filterTournaments() {
        const cards = document.querySelectorAll('[data-tournament-id]');
        let visibleCount = 0;

        cards.forEach(card => {
            const tournament = {
                category: card.dataset.tournamentCategory || '',
                location: card.dataset.tournamentLocation || '',
                status: card.querySelector('.tournament-card-badge')?.textContent.trim() || ''
            };

            let visible = true;

            // Фильтр по категории
            if (this.currentState.category && tournament.category !== this.currentState.category) {
                visible = false;
            }

            // Фильтр по локации
            if (this.currentState.location && !tournament.location.includes(this.currentState.location)) {
                visible = false;
            }

            // Фильтр по статусу
            if (this.currentState.status && !tournament.status.includes(this.currentState.status)) {
                visible = false;
            }

            card.style.display = visible ? '' : 'none';
            if (visible) visibleCount++;
        });

        // Обновить счетчик
        this.updateResultsCount(visibleCount);
    }

    /**
     * Применить сортировку
     */
    applySort() {
        const container = document.querySelector('.tournament-grid, .tournament-list');
        if (!container) return;

        const cards = Array.from(container.querySelectorAll('[data-tournament-id]'));
        
        cards.sort((a, b) => {
            let aValue, bValue;

            switch (this.currentState.sortBy) {
                case 'name':
                    aValue = a.dataset.tournamentName || '';
                    bValue = b.dataset.tournamentName || '';
                    break;
                case 'location':
                    aValue = a.dataset.tournamentLocation || '';
                    bValue = b.dataset.tournamentLocation || '';
                    break;
                case 'start_date':
                default:
                    aValue = a.dataset.tournamentStartDate || '';
                    bValue = b.dataset.tournamentStartDate || '';
                    break;
            }

            const comparison = aValue.localeCompare(bValue);
            return this.currentState.sortOrder === 'asc' ? comparison : -comparison;
        });

        // Переупорядочить карточки
        cards.forEach(card => container.appendChild(card));
    }

    /**
     * Применить режим отображения
     */
    applyViewMode() {
        const container = document.querySelector('.tournament-grid, .tournament-list');
        if (!container) return;

        if (this.currentState.viewMode === 'grid') {
            container.classList.remove('tournament-list');
            container.classList.add('tournament-grid');
        } else {
            container.classList.remove('tournament-grid');
            container.classList.add('tournament-list');
        }
    }

    /**
     * Обновить UI
     */
    updateUI() {
        this.updateSortButtons();
        this.updateViewModeButtons();
        this.updateFilterBadges();
    }

    /**
     * Обновить кнопки сортировки
     */
    updateSortButtons() {
        document.querySelectorAll('[data-sort]').forEach(btn => {
            const sortBy = btn.dataset.sort;
            const isActive = sortBy === this.currentState.sortBy;
            
            btn.classList.toggle('active', isActive);
            
            if (isActive) {
                const icon = btn.querySelector('i');
                if (icon) {
                    icon.className = this.currentState.sortOrder === 'asc' 
                        ? 'bi bi-arrow-up' 
                        : 'bi bi-arrow-down';
                }
            }
        });
    }

    /**
     * Обновить кнопки режима отображения
     */
    updateViewModeButtons() {
        document.querySelectorAll('[data-view-mode]').forEach(btn => {
            const mode = btn.dataset.viewMode;
            btn.classList.toggle('active', mode === this.currentState.viewMode);
        });
    }

    /**
     * Обновить бейджи активных фильтров
     */
    updateFilterBadges() {
        const container = document.getElementById('activeFilterBadges');
        if (!container) return;

        const activeFilters = Object.entries(this.currentState).filter(([key, value]) => {
            return value && value !== this.defaultState[key] && 
                   ['category', 'location', 'status'].includes(key);
        });

        if (activeFilters.length === 0) {
            container.innerHTML = '';
            return;
        }

        container.innerHTML = activeFilters.map(([key, value]) => `
            <span class="filter-badge">
                ${this.getFilterLabel(key)}: ${value}
                <button class="filter-badge-remove" onclick="window.filterStateManager.removeFilter('${key}')">
                    <i class="bi bi-x"></i>
                </button>
            </span>
        `).join('');
    }

    /**
     * Получить метку фильтра
     */
    getFilterLabel(key) {
        const labels = {
            category: 'Категория',
            location: 'Локация',
            status: 'Статус'
        };
        return labels[key] || key;
    }

    /**
     * Удалить фильтр
     */
    removeFilter(filterName) {
        this.currentState[filterName] = this.defaultState[filterName];
        this.saveState();
        this.applyState();
    }

    /**
     * Обновить счетчик результатов
     */
    updateResultsCount(count) {
        const counter = document.getElementById('resultsCount');
        if (counter) {
            counter.textContent = `Найдено: ${count}`;
        }
    }

    /**
     * Сбросить фильтры
     */
    resetFilters() {
        this.currentState = { ...this.defaultState };
        this.saveState();
        this.applyState();

        if (window.notificationSystem) {
            window.notificationSystem.show('Фильтры сброшены', 'success');
        }
    }

    /**
     * Синхронизация с URL
     */
    syncWithURL() {
        const params = new URLSearchParams();
        
        Object.entries(this.currentState).forEach(([key, value]) => {
            if (value && value !== this.defaultState[key]) {
                params.set(key, value);
            }
        });

        const newURL = params.toString() ? `?${params.toString()}` : window.location.pathname;
        window.history.replaceState({}, '', newURL);
    }

    /**
     * Загрузить из URL
     */
    loadFromURL() {
        const params = new URLSearchParams(window.location.search);
        
        params.forEach((value, key) => {
            if (this.currentState.hasOwnProperty(key)) {
                this.currentState[key] = value;
            }
        });

        this.saveState();
        this.applyState();
    }

    /**
     * Сохранить пресет
     */
    savePreset() {
        const name = prompt('Название пресета:');
        if (!name) return;

        try {
            const presets = JSON.parse(localStorage.getItem('filterPresets') || '{}');
            presets[name] = { ...this.currentState };
            localStorage.setItem('filterPresets', JSON.stringify(presets));

            if (window.notificationSystem) {
                window.notificationSystem.show(`Пресет "${name}" сохранен`, 'success');
            }

            this.updatePresetsMenu();
        } catch (error) {
            console.error('Error saving preset:', error);
        }
    }

    /**
     * Загрузить пресет
     */
    loadPreset(name) {
        try {
            const presets = JSON.parse(localStorage.getItem('filterPresets') || '{}');
            if (presets[name]) {
                this.currentState = { ...presets[name] };
                this.saveState();
                this.applyState();

                if (window.notificationSystem) {
                    window.notificationSystem.show(`Пресет "${name}" загружен`, 'success');
                }
            }
        } catch (error) {
            console.error('Error loading preset:', error);
        }
    }

    /**
     * Обновить меню пресетов
     */
    updatePresetsMenu() {
        const menu = document.getElementById('presetsMenu');
        if (!menu) return;

        try {
            const presets = JSON.parse(localStorage.getItem('filterPresets') || '{}');
            const presetNames = Object.keys(presets);

            if (presetNames.length === 0) {
                menu.innerHTML = '<div class="dropdown-item text-muted">Нет сохраненных пресетов</div>';
                return;
            }

            menu.innerHTML = presetNames.map(name => `
                <a class="dropdown-item" href="#" data-preset="${name}">
                    <i class="bi bi-bookmark"></i> ${name}
                </a>
            `).join('');
        } catch (error) {
            console.error('Error updating presets menu:', error);
        }
    }

    /**
     * Экспорт состояния
     */
    exportState() {
        const json = JSON.stringify(this.currentState, null, 2);
        const blob = new Blob([json], { type: 'application/json' });
        const url = URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = 'filter-state.json';
        a.click();
        URL.revokeObjectURL(url);
    }

    /**
     * Импорт состояния
     */
    importState(file) {
        const reader = new FileReader();
        reader.onload = (e) => {
            try {
                const state = JSON.parse(e.target.result);
                this.currentState = { ...this.defaultState, ...state };
                this.saveState();
                this.applyState();

                if (window.notificationSystem) {
                    window.notificationSystem.show('Состояние импортировано', 'success');
                }
            } catch (error) {
                console.error('Error importing state:', error);
                if (window.notificationSystem) {
                    window.notificationSystem.show('Ошибка импорта', 'error');
                }
            }
        };
        reader.readAsText(file);
    }
}

// CSS стили
const style = document.createElement('style');
style.textContent = `
    .filter-badge {
        display: inline-flex;
        align-items: center;
        gap: 0.5rem;
        padding: 0.375rem 0.75rem;
        background: var(--primary-color);
        color: white;
        border-radius: 20px;
        font-size: 0.875rem;
        font-weight: 500;
        margin: 0.25rem;
    }

    .filter-badge-remove {
        padding: 0;
        border: none;
        background: none;
        color: white;
        cursor: pointer;
        display: flex;
        align-items: center;
        justify-content: center;
        width: 18px;
        height: 18px;
        border-radius: 50%;
        transition: background 0.2s ease;
    }

    .filter-badge-remove:hover {
        background: rgba(255, 255, 255, 0.2);
    }

    #activeFilterBadges {
        display: flex;
        flex-wrap: wrap;
        gap: 0.5rem;
        margin: 1rem 0;
    }

    [data-sort].active,
    [data-view-mode].active {
        background: var(--primary-color);
        color: white;
    }
`;
document.head.appendChild(style);

// Инициализация
document.addEventListener('DOMContentLoaded', () => {
    window.filterStateManager = new FilterStateManager();
    
    // Загрузить из URL при загрузке
    window.filterStateManager.loadFromURL();
    
    console.log('[Filter State Manager] Initialized');
});

// Экспорт
if (typeof module !== 'undefined' && module.exports) {
    module.exports = FilterStateManager;
}
