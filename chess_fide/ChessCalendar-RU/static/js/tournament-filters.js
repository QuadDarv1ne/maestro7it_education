/**
 * Фильтрация турниров в реальном времени
 * Улучшенная система фильтров с debounce и кэшированием
 */

class TournamentFilters {
    constructor(options = {}) {
        this.options = {
            formSelector: options.formSelector || '#filterForm',
            resultsSelector: options.resultsSelector || '.tournaments-grid',
            debounceDelay: options.debounceDelay || 300,
            enableUrlUpdate: options.enableUrlUpdate !== false,
            enableCache: options.enableCache !== false
        };
        
        this.form = null;
        this.resultsContainer = null;
        this.debounceTimer = null;
        this.cache = new Map();
        this.currentFilters = {};
        this.isLoading = false;
        
        this.init();
    }

    init() {
        this.form = document.querySelector(this.options.formSelector);
        this.resultsContainer = document.querySelector(this.options.resultsSelector);
        
        if (!this.form || !this.resultsContainer) {
            console.warn('Tournament filters: form or results container not found');
            return;
        }
        
        this.attachEventListeners();
        this.loadInitialFilters();
    }

    /**
     * Прикрепление обработчиков событий
     */
    attachEventListeners() {
        // Select элементы - мгновенная фильтрация
        const selects = this.form.querySelectorAll('select');
        selects.forEach(select => {
            select.addEventListener('change', () => this.handleFilterChange());
        });
        
        // Input элементы - фильтрация с debounce
        const inputs = this.form.querySelectorAll('input[type="text"], input[type="search"]');
        inputs.forEach(input => {
            input.addEventListener('input', () => this.handleFilterChangeDebounced());
        });
        
        // Кнопка сброса
        const resetBtn = this.form.querySelector('[type="reset"], .btn-reset');
        if (resetBtn) {
            resetBtn.addEventListener('click', (e) => {
                e.preventDefault();
                this.resetFilters();
            });
        }
        
        // Предотвращение отправки формы
        this.form.addEventListener('submit', (e) => {
            e.preventDefault();
            this.applyFilters();
        });
    }

    /**
     * Загрузка начальных фильтров из URL
     */
    loadInitialFilters() {
        const urlParams = new URLSearchParams(window.location.search);
        
        this.currentFilters = {
            category: urlParams.get('category') || '',
            status: urlParams.get('status') || '',
            location: urlParams.get('location') || '',
            search: urlParams.get('search') || '',
            sort_by: urlParams.get('sort_by') || 'start_date',
            page: parseInt(urlParams.get('page')) || 1
        };
        
        this.updateFormValues();
    }

    /**
     * Обновление значений формы
     */
    updateFormValues() {
        Object.keys(this.currentFilters).forEach(key => {
            const element = this.form.querySelector(`[name="${key}"]`);
            if (element && this.currentFilters[key]) {
                element.value = this.currentFilters[key];
            }
        });
    }

    /**
     * Обработка изменения фильтра
     */
    handleFilterChange() {
        this.applyFilters();
    }

    /**
     * Обработка изменения фильтра с debounce
     */
    handleFilterChangeDebounced() {
        if (this.debounceTimer) {
            clearTimeout(this.debounceTimer);
        }
        
        this.debounceTimer = setTimeout(() => {
            this.applyFilters();
        }, this.options.debounceDelay);
    }

    /**
     * Применение фильтров
     */
    async applyFilters() {
        if (this.isLoading) {
            return;
        }
        
        // Собираем данные формы
        const formData = new FormData(this.form);
        const filters = {};
        
        for (const [key, value] of formData.entries()) {
            if (value) {
                filters[key] = value;
            }
        }
        
        // Сбрасываем страницу при изменении фильтров
        filters.page = 1;
        
        this.currentFilters = filters;
        
        // Проверяем кэш
        const cacheKey = this.getCacheKey(filters);
        if (this.options.enableCache && this.cache.has(cacheKey)) {
            this.renderResults(this.cache.get(cacheKey));
            this.updateUrl(filters);
            return;
        }
        
        // Загружаем результаты
        await this.loadResults(filters);
    }

    /**
     * Загрузка результатов
     */
    async loadResults(filters) {
        this.isLoading = true;
        this.showLoading();
        
        try {
            const url = this.buildUrl(filters);
            const response = await fetch(url, {
                headers: {
                    'X-Requested-With': 'XMLHttpRequest',
                    'Accept': 'application/json, text/html'
                }
            });
            
            if (!response.ok) {
                throw new Error('Failed to load tournaments');
            }
            
            const contentType = response.headers.get('content-type');
            let data;
            
            if (contentType && contentType.includes('application/json')) {
                data = await response.json();
            } else {
                const html = await response.text();
                data = this.parseHtmlResponse(html);
            }
            
            // Сохраняем в кэш
            if (this.options.enableCache) {
                const cacheKey = this.getCacheKey(filters);
                this.cache.set(cacheKey, data);
            }
            
            this.renderResults(data);
            this.updateUrl(filters);
            
            // Обновляем счетчик результатов
            this.updateResultsCount(data.total || data.tournaments?.length || 0);
            
        } catch (error) {
            console.error('Error loading tournaments:', error);
            this.showError('Ошибка загрузки турниров. Попробуйте еще раз.');
        } finally {
            this.isLoading = false;
            this.hideLoading();
        }
    }

    /**
     * Построение URL для запроса
     */
    buildUrl(filters) {
        const url = new URL(window.location.origin + window.location.pathname);
        
        Object.keys(filters).forEach(key => {
            if (filters[key]) {
                url.searchParams.set(key, filters[key]);
            }
        });
        
        return url.toString();
    }

    /**
     * Парсинг HTML ответа
     */
    parseHtmlResponse(html) {
        const parser = new DOMParser();
        const doc = parser.parseFromString(html, 'text/html');
        
        const tournaments = doc.querySelectorAll('.tournament-card-modern');
        const pagination = doc.querySelector('.pagination');
        
        return {
            tournaments: Array.from(tournaments),
            pagination: pagination ? pagination.outerHTML : '',
            total: tournaments.length
        };
    }

    /**
     * Отрисовка результатов
     */
    renderResults(data) {
        if (!this.resultsContainer) {
            return;
        }
        
        // Очищаем контейнер
        this.resultsContainer.innerHTML = '';
        
        if (data.tournaments && data.tournaments.length > 0) {
            const fragment = document.createDocumentFragment();
            
            data.tournaments.forEach(tournament => {
                if (tournament instanceof HTMLElement) {
                    fragment.appendChild(tournament.cloneNode(true));
                } else {
                    // Если это HTML строка
                    const temp = document.createElement('div');
                    temp.innerHTML = tournament;
                    fragment.appendChild(temp.firstElementChild);
                }
            });
            
            this.resultsContainer.appendChild(fragment);
            
            // Обновляем пагинацию
            if (data.pagination) {
                this.updatePagination(data.pagination);
            }
            
            // Инициализируем lazy loading для новых элементов
            if (window.lazyLoader) {
                window.lazyLoader.refresh();
            }
            
            // Инициализируем tournament card manager для новых карточек
            if (window.tournamentCardManager) {
                window.tournamentCardManager.initializeCards();
            }
            
        } else {
            this.showEmptyState();
        }
        
        // Прокрутка к результатам
        this.scrollToResults();
    }

    /**
     * Обновление пагинации
     */
    updatePagination(paginationHtml) {
        const paginationContainer = document.querySelector('.pagination')?.parentElement;
        if (paginationContainer) {
            paginationContainer.innerHTML = paginationHtml;
        }
    }

    /**
     * Показать пустое состояние
     */
    showEmptyState() {
        this.resultsContainer.innerHTML = `
            <div class="col-12">
                <div class="empty-state text-center py-5">
                    <i class="bi bi-calendar-x display-1 text-muted mb-3"></i>
                    <h4 class="text-muted mb-3">Турниры не найдены</h4>
                    <p class="text-muted mb-4">Попробуйте изменить параметры фильтрации</p>
                    <button class="btn btn-primary" onclick="tournamentFilters.resetFilters()">
                        <i class="bi bi-arrow-clockwise"></i> Сбросить фильтры
                    </button>
                </div>
            </div>
        `;
    }

    /**
     * Обновление счетчика результатов
     */
    updateResultsCount(count) {
        const counter = document.querySelector('.results-count');
        if (counter) {
            counter.textContent = count;
        }
    }

    /**
     * Обновление URL
     */
    updateUrl(filters) {
        if (!this.options.enableUrlUpdate) {
            return;
        }
        
        const url = this.buildUrl(filters);
        window.history.pushState({ filters }, '', url);
    }

    /**
     * Сброс фильтров
     */
    resetFilters() {
        this.form.reset();
        this.currentFilters = {
            page: 1,
            sort_by: 'start_date'
        };
        this.applyFilters();
    }

    /**
     * Получение ключа кэша
     */
    getCacheKey(filters) {
        return JSON.stringify(filters);
    }

    /**
     * Показать индикатор загрузки
     */
    showLoading() {
        this.resultsContainer.style.opacity = '0.5';
        this.resultsContainer.style.pointerEvents = 'none';
        
        // Добавляем спиннер
        const spinner = document.createElement('div');
        spinner.className = 'loading-spinner';
        spinner.innerHTML = `
            <div class="text-center py-5">
                <div class="spinner-border text-primary" role="status">
                    <span class="visually-hidden">Загрузка...</span>
                </div>
                <p class="mt-3 text-muted">Загрузка турниров...</p>
            </div>
        `;
        spinner.id = 'filterLoadingSpinner';
        
        this.resultsContainer.parentElement.insertBefore(spinner, this.resultsContainer);
    }

    /**
     * Скрыть индикатор загрузки
     */
    hideLoading() {
        this.resultsContainer.style.opacity = '1';
        this.resultsContainer.style.pointerEvents = 'auto';
        
        const spinner = document.getElementById('filterLoadingSpinner');
        if (spinner) {
            spinner.remove();
        }
    }

    /**
     * Показать ошибку
     */
    showError(message) {
        const alert = document.createElement('div');
        alert.className = 'alert alert-danger alert-dismissible fade show';
        alert.innerHTML = `
            <i class="bi bi-exclamation-triangle"></i> ${message}
            <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
        `;
        
        this.resultsContainer.parentElement.insertBefore(alert, this.resultsContainer);
        
        setTimeout(() => alert.remove(), 5000);
    }

    /**
     * Прокрутка к результатам
     */
    scrollToResults() {
        const offset = 100;
        const elementPosition = this.resultsContainer.getBoundingClientRect().top;
        const offsetPosition = elementPosition + window.pageYOffset - offset;
        
        window.scrollTo({
            top: offsetPosition,
            behavior: 'smooth'
        });
    }

    /**
     * Очистка кэша
     */
    clearCache() {
        this.cache.clear();
    }
}

// Инициализация при загрузке страницы
document.addEventListener('DOMContentLoaded', () => {
    window.tournamentFilters = new TournamentFilters({
        debounceDelay: 300,
        enableUrlUpdate: true,
        enableCache: true
    });
});

// Экспорт для использования в других модулях
if (typeof module !== 'undefined' && module.exports) {
    module.exports = TournamentFilters;
}
