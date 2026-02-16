// Advanced Search with Autocomplete

class AdvancedSearch {
    constructor() {
        this.searchCache = new Map();
        this.searchHistory = this.loadSearchHistory();
        this.init();
    }

    init() {
        this.enhanceSearchInput();
        this.createAdvancedSearchModal();
    }

    loadSearchHistory() {
        const saved = localStorage.getItem('searchHistory');
        return saved ? JSON.parse(saved) : [];
    }

    saveSearchHistory() {
        // Keep only last 10 searches
        const history = this.searchHistory.slice(0, 10);
        localStorage.setItem('searchHistory', JSON.stringify(history));
    }

    addToHistory(query) {
        // Remove if already exists
        this.searchHistory = this.searchHistory.filter(item => item.query !== query);
        
        // Add to beginning
        this.searchHistory.unshift({
            query: query,
            timestamp: new Date().toISOString()
        });

        this.saveSearchHistory();
    }

    enhanceSearchInput() {
        const searchInput = document.getElementById('searchInput');
        if (!searchInput) return;

        // Create autocomplete container
        const autocomplete = document.createElement('div');
        autocomplete.id = 'searchAutocomplete';
        autocomplete.className = 'search-autocomplete';
        autocomplete.style.cssText = `
            position: absolute;
            top: 100%;
            left: 0;
            right: 0;
            background: var(--bg-primary);
            border: 1px solid var(--border-color);
            border-radius: 8px;
            box-shadow: var(--box-shadow-lg);
            max-height: 400px;
            overflow-y: auto;
            z-index: 1000;
            display: none;
            margin-top: 5px;
        `;

        searchInput.parentElement.style.position = 'relative';
        searchInput.parentElement.appendChild(autocomplete);

        // Add event listeners
        let debounceTimer;
        searchInput.addEventListener('input', (e) => {
            clearTimeout(debounceTimer);
            debounceTimer = setTimeout(() => {
                this.handleSearch(e.target.value);
            }, 300);
        });

        searchInput.addEventListener('focus', () => {
            if (searchInput.value.length >= 2) {
                this.handleSearch(searchInput.value);
            } else {
                this.showSearchHistory();
            }
        });

        // Close on click outside
        document.addEventListener('click', (e) => {
            if (!searchInput.contains(e.target) && !autocomplete.contains(e.target)) {
                autocomplete.style.display = 'none';
            }
        });

        // Keyboard navigation
        searchInput.addEventListener('keydown', (e) => {
            this.handleKeyboardNavigation(e);
        });

        // Add advanced search button
        this.addAdvancedSearchButton(searchInput);
    }

    addAdvancedSearchButton(searchInput) {
        const button = document.createElement('button');
        button.className = 'btn btn-outline-primary';
        button.innerHTML = '<i class="bi bi-sliders"></i>';
        button.title = 'Расширенный поиск';
        button.onclick = () => this.showAdvancedSearchModal();

        const searchForm = searchInput.closest('form');
        if (searchForm) {
            searchForm.style.display = 'flex';
            searchForm.style.gap = '0.5rem';
            searchForm.appendChild(button);
        }
    }

    async handleSearch(query) {
        const autocomplete = document.getElementById('searchAutocomplete');
        if (!autocomplete) return;

        if (query.length < 2) {
            this.showSearchHistory();
            return;
        }

        // Check cache
        if (this.searchCache.has(query)) {
            this.displayResults(this.searchCache.get(query));
            return;
        }

        try {
            const response = await fetch(`/api/tournaments/search?q=${encodeURIComponent(query)}`);
            const results = await response.json();

            // Cache results
            this.searchCache.set(query, results);

            this.displayResults(results);
        } catch (error) {
            console.error('Search error:', error);
            if (window.toast) {
                window.toast.error('Ошибка поиска');
            }
        }
    }

    displayResults(results) {
        const autocomplete = document.getElementById('searchAutocomplete');
        if (!autocomplete) return;

        if (results.length === 0) {
            autocomplete.innerHTML = `
                <div style="padding: 1rem; text-align: center; color: var(--text-secondary);">
                    <i class="bi bi-search"></i> Ничего не найдено
                </div>
            `;
            autocomplete.style.display = 'block';
            return;
        }

        autocomplete.innerHTML = `
            <div style="padding: 0.5rem; border-bottom: 1px solid var(--border-color); font-weight: 600; color: var(--text-secondary);">
                Найдено: ${results.length}
            </div>
            ${results.map((result, index) => `
                <div class="autocomplete-item" data-index="${index}" 
                     onclick="advancedSearch.selectResult(${result.id})"
                     style="
                         padding: 1rem;
                         cursor: pointer;
                         border-bottom: 1px solid var(--border-color);
                         transition: background 0.2s;
                     "
                     onmouseover="this.style.background='var(--bg-secondary)'"
                     onmouseout="this.style.background='transparent'">
                    <div style="font-weight: 600; color: var(--text-primary); margin-bottom: 0.25rem;">
                        ${this.highlightMatch(result.name, document.getElementById('searchInput').value)}
                    </div>
                    <div style="font-size: 0.875rem; color: var(--text-secondary);">
                        <i class="bi bi-geo-alt"></i> ${result.location}
                        <span style="margin-left: 1rem;">
                            <i class="bi bi-calendar"></i> ${this.formatDate(result.start_date)}
                        </span>
                    </div>
                    ${result.category ? `<span class="badge bg-primary mt-1">${result.category}</span>` : ''}
                </div>
            `).join('')}
        `;

        autocomplete.style.display = 'block';
    }

    showSearchHistory() {
        const autocomplete = document.getElementById('searchAutocomplete');
        if (!autocomplete || this.searchHistory.length === 0) return;

        autocomplete.innerHTML = `
            <div style="padding: 0.5rem; border-bottom: 1px solid var(--border-color); font-weight: 600; color: var(--text-secondary); display: flex; justify-content: space-between; align-items: center;">
                <span><i class="bi bi-clock-history"></i> История поиска</span>
                <button class="btn btn-sm btn-link" onclick="advancedSearch.clearHistory()" style="padding: 0;">
                    Очистить
                </button>
            </div>
            ${this.searchHistory.map(item => `
                <div class="autocomplete-item" 
                     onclick="advancedSearch.searchFromHistory('${item.query}')"
                     style="
                         padding: 1rem;
                         cursor: pointer;
                         border-bottom: 1px solid var(--border-color);
                         transition: background 0.2s;
                         display: flex;
                         justify-content: space-between;
                         align-items: center;
                     "
                     onmouseover="this.style.background='var(--bg-secondary)'"
                     onmouseout="this.style.background='transparent'">
                    <span style="color: var(--text-primary);">
                        <i class="bi bi-search"></i> ${item.query}
                    </span>
                    <small style="color: var(--text-secondary);">
                        ${this.formatRelativeTime(item.timestamp)}
                    </small>
                </div>
            `).join('')}
        `;

        autocomplete.style.display = 'block';
    }

    selectResult(tournamentId) {
        const searchInput = document.getElementById('searchInput');
        if (searchInput) {
            this.addToHistory(searchInput.value);
        }

        window.location.href = `/tournament/${tournamentId}`;
    }

    searchFromHistory(query) {
        const searchInput = document.getElementById('searchInput');
        if (searchInput) {
            searchInput.value = query;
            this.handleSearch(query);
        }
    }

    clearHistory() {
        this.searchHistory = [];
        this.saveSearchHistory();
        
        const autocomplete = document.getElementById('searchAutocomplete');
        if (autocomplete) {
            autocomplete.style.display = 'none';
        }

        if (window.toast) {
            window.toast.success('История поиска очищена');
        }
    }

    handleKeyboardNavigation(e) {
        const autocomplete = document.getElementById('searchAutocomplete');
        if (!autocomplete || autocomplete.style.display === 'none') return;

        const items = autocomplete.querySelectorAll('.autocomplete-item');
        if (items.length === 0) return;

        const currentIndex = Array.from(items).findIndex(item => 
            item.style.background === 'var(--bg-secondary)'
        );

        if (e.key === 'ArrowDown') {
            e.preventDefault();
            const nextIndex = currentIndex < items.length - 1 ? currentIndex + 1 : 0;
            this.highlightItem(items, nextIndex);
        } else if (e.key === 'ArrowUp') {
            e.preventDefault();
            const prevIndex = currentIndex > 0 ? currentIndex - 1 : items.length - 1;
            this.highlightItem(items, prevIndex);
        } else if (e.key === 'Enter' && currentIndex >= 0) {
            e.preventDefault();
            items[currentIndex].click();
        } else if (e.key === 'Escape') {
            autocomplete.style.display = 'none';
        }
    }

    highlightItem(items, index) {
        items.forEach((item, i) => {
            item.style.background = i === index ? 'var(--bg-secondary)' : 'transparent';
        });
    }

    highlightMatch(text, query) {
        const regex = new RegExp(`(${query})`, 'gi');
        return text.replace(regex, '<mark style="background: var(--warning-color); padding: 0.1rem 0.2rem; border-radius: 3px;">$1</mark>');
    }

    formatDate(dateString) {
        const date = new Date(dateString);
        return date.toLocaleDateString('ru-RU', {
            day: '2-digit',
            month: '2-digit',
            year: 'numeric'
        });
    }

    formatRelativeTime(timestamp) {
        const date = new Date(timestamp);
        const now = new Date();
        const diff = now - date;
        const minutes = Math.floor(diff / 60000);
        const hours = Math.floor(diff / 3600000);
        const days = Math.floor(diff / 86400000);

        if (minutes < 1) return 'только что';
        if (minutes < 60) return `${minutes} мин назад`;
        if (hours < 24) return `${hours} ч назад`;
        if (days < 7) return `${days} дн назад`;
        return date.toLocaleDateString('ru-RU');
    }

    createAdvancedSearchModal() {
        // Modal will be created on demand
    }

    showAdvancedSearchModal() {
        const existingModal = document.getElementById('advancedSearchModal');
        if (existingModal) existingModal.remove();

        const modal = document.createElement('div');
        modal.id = 'advancedSearchModal';
        modal.className = 'modal fade';
        modal.innerHTML = `
            <div class="modal-dialog modal-lg">
                <div class="modal-content">
                    <div class="modal-header">
                        <h5 class="modal-title">
                            <i class="bi bi-sliders"></i> Расширенный поиск
                        </h5>
                        <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
                    </div>
                    <div class="modal-body">
                        <form id="advancedSearchForm">
                            <div class="row g-3">
                                <div class="col-md-6">
                                    <label class="form-label">Название турнира</label>
                                    <input type="text" class="form-control" name="name" placeholder="Введите название...">
                                </div>
                                <div class="col-md-6">
                                    <label class="form-label">Город</label>
                                    <input type="text" class="form-control" name="location" placeholder="Москва, Санкт-Петербург...">
                                </div>
                                <div class="col-md-6">
                                    <label class="form-label">Категория</label>
                                    <select class="form-select" name="category">
                                        <option value="">Все категории</option>
                                        <option value="Блиц">Блиц</option>
                                        <option value="Рапид">Рапид</option>
                                        <option value="Классика">Классика</option>
                                    </select>
                                </div>
                                <div class="col-md-6">
                                    <label class="form-label">Статус</label>
                                    <select class="form-select" name="status">
                                        <option value="">Все статусы</option>
                                        <option value="upcoming">Предстоящие</option>
                                        <option value="ongoing">Идут сейчас</option>
                                        <option value="completed">Завершенные</option>
                                    </select>
                                </div>
                                <div class="col-md-6">
                                    <label class="form-label">Дата от</label>
                                    <input type="date" class="form-control" name="dateFrom">
                                </div>
                                <div class="col-md-6">
                                    <label class="form-label">Дата до</label>
                                    <input type="date" class="form-control" name="dateTo">
                                </div>
                                <div class="col-md-6">
                                    <label class="form-label">Призовой фонд от</label>
                                    <input type="number" class="form-control" name="prizeMin" placeholder="0">
                                </div>
                                <div class="col-md-6">
                                    <label class="form-label">Организатор</label>
                                    <input type="text" class="form-control" name="organizer" placeholder="Название организации...">
                                </div>
                            </div>
                        </form>
                    </div>
                    <div class="modal-footer">
                        <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Отмена</button>
                        <button type="button" class="btn btn-outline-secondary" onclick="advancedSearch.resetAdvancedSearch()">
                            Сбросить
                        </button>
                        <button type="button" class="btn btn-primary" onclick="advancedSearch.performAdvancedSearch()">
                            <i class="bi bi-search"></i> Найти
                        </button>
                    </div>
                </div>
            </div>
        `;

        document.body.appendChild(modal);
        const bsModal = new bootstrap.Modal(modal);
        bsModal.show();
    }

    resetAdvancedSearch() {
        document.getElementById('advancedSearchForm').reset();
    }

    performAdvancedSearch() {
        const form = document.getElementById('advancedSearchForm');
        const formData = new FormData(form);
        const params = new URLSearchParams();

        for (const [key, value] of formData.entries()) {
            if (value) {
                params.append(key, value);
            }
        }

        // Close modal
        const modal = bootstrap.Modal.getInstance(document.getElementById('advancedSearchModal'));
        if (modal) modal.hide();

        // Redirect to search results
        window.location.href = `/?${params.toString()}`;
    }
}

// Initialize
const advancedSearch = new AdvancedSearch();

// Export for use in other scripts
window.advancedSearch = advancedSearch;
