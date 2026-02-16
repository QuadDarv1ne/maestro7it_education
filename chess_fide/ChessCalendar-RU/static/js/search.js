// Advanced Search with Autocomplete

class TournamentSearch {
    constructor() {
        this.searchInput = document.getElementById('searchInput');
        this.searchResults = document.getElementById('searchResults');
        this.debounceTimer = null;
        this.cache = new Map();
        this.recentSearches = this.loadRecentSearches();
        
        this.init();
    }
    
    init() {
        if (!this.searchInput) return;
        
        this.searchInput.addEventListener('input', (e) => this.handleInput(e));
        this.searchInput.addEventListener('focus', () => this.showRecentSearches());
        this.searchInput.addEventListener('keydown', (e) => this.handleKeyboard(e));
        
        // Close on click outside
        document.addEventListener('click', (e) => {
            if (!this.searchInput.contains(e.target) && !this.searchResults.contains(e.target)) {
                this.hideResults();
            }
        });
        
        // Initialize advanced search
        this.initializeAdvancedSearch();
    }
    
    initializeAdvancedSearch() {
        // Add advanced search functionality
        this.advancedFilters = {};
        this.activeFilters = {};
    }
    
    // Method to apply advanced filters
    applyFilters(filters) {
        this.activeFilters = { ...this.activeFilters, ...filters };
        
        // Re-run search with current query and new filters
        const query = this.searchInput.value.trim();
        if (query.length >= 2) {
            this.search(query);
        }
    }
    
    // Method to clear filters
    clearFilters() {
        this.activeFilters = {};
        
        // Re-run search without filters
        const query = this.searchInput.value.trim();
        if (query.length >= 2) {
            this.search(query);
        }
    }
    
    handleInput(e) {
        const query = e.target.value.trim();
        
        clearTimeout(this.debounceTimer);
        
        if (query.length < 2) {
            this.showRecentSearches();
            return;
        }
        
        this.debounceTimer = setTimeout(() => {
            this.search(query);
        }, 300);
    }
    
    async search(query) {
        // Create cache key with active filters
        const cacheKey = `${query}_${JSON.stringify(this.activeFilters)}`;
        
        // Check cache first
        if (this.cache.has(cacheKey)) {
            this.displayResults(this.cache.get(cacheKey), query);
            return;
        }
        
        try {
            // Build query parameters
            let url = `/api/tournaments/search?q=${encodeURIComponent(query)}`;
            
            // Add active filters as query parameters
            Object.entries(this.activeFilters).forEach(([key, value]) => {
                if (value !== null && value !== undefined && value !== '') {
                    url += `&${key}=${encodeURIComponent(value)}`;
                }
            });
            
            const response = await fetch(url);
            const data = await response.json();
            
            // Cache results with filters
            this.cache.set(cacheKey, data);
            
            // Limit cache size
            if (this.cache.size > 50) {
                const firstKey = this.cache.keys().next().value;
                this.cache.delete(firstKey);
            }
            
            this.displayResults(data, query);
        } catch (error) {
            console.error('Search error:', error);
            this.showError('Ошибка поиска. Попробуйте позже.');
        }
    }
    
    displayResults(results, query) {
        if (!results || results.length === 0) {
            this.showNoResults(query);
            return;
        }
        
        this.searchResults.innerHTML = '';
        
        // Add search header
        const header = document.createElement('div');
        header.className = 'search-header';
        header.innerHTML = `
            <div class="d-flex justify-content-between align-items-center p-2 border-bottom">
                <small class="text-muted">Найдено: ${results.length}</small>
                <button class="btn btn-sm btn-link text-muted" onclick="document.getElementById('searchInput').value = ''; document.getElementById('searchResults').style.display = 'none';">
                    <i class="bi bi-x"></i>
                </button>
            </div>
        `;
        this.searchResults.appendChild(header);
        
        // Add results
        results.slice(0, 10).forEach(tournament => {
            const item = this.createResultItem(tournament, query);
            this.searchResults.appendChild(item);
        });
        
        this.showResults();
        this.saveRecentSearch(query);
    }
    
    createResultItem(tournament, query) {
        const item = document.createElement('div');
        item.className = 'search-result-item';
        
        // Highlight matching text
        const highlightedName = this.highlightText(tournament.name, query);
        const highlightedLocation = this.highlightText(tournament.location, query);
        
        item.innerHTML = `
            <div class="d-flex align-items-start gap-2">
                <i class="bi bi-trophy text-primary mt-1"></i>
                <div class="flex-grow-1">
                    <div class="search-result-title">${highlightedName}</div>
                    <div class="search-result-location">
                        <i class="bi bi-geo-alt"></i> ${highlightedLocation}
                    </div>
                    <div class="search-result-dates">
                        <i class="bi bi-calendar"></i> ${this.formatDate(tournament.start_date)} - ${this.formatDate(tournament.end_date)}
                    </div>
                    ${tournament.category ? `<span class="badge bg-secondary mt-1">${tournament.category}</span>` : ''}
                </div>
            </div>
        `;
        
        item.addEventListener('click', () => {
            window.location.href = `/tournament/${tournament.id}`;
        });
        
        return item;
    }
    
    highlightText(text, query) {
        if (!query) return this.escapeHtml(text);
        
        const regex = new RegExp(`(${this.escapeRegex(query)})`, 'gi');
        return this.escapeHtml(text).replace(regex, '<mark>$1</mark>');
    }
    
    showRecentSearches() {
        if (this.recentSearches.length === 0) return;
        
        this.searchResults.innerHTML = '';
        
        const header = document.createElement('div');
        header.className = 'search-header';
        header.innerHTML = `
            <div class="d-flex justify-content-between align-items-center p-2 border-bottom">
                <small class="text-muted"><i class="bi bi-clock-history"></i> Недавние поиски</small>
                <button class="btn btn-sm btn-link text-muted" onclick="localStorage.removeItem('recentSearches'); location.reload();">
                    Очистить
                </button>
            </div>
        `;
        this.searchResults.appendChild(header);
        
        this.recentSearches.forEach(search => {
            const item = document.createElement('div');
            item.className = 'search-result-item';
            item.innerHTML = `
                <div class="d-flex align-items-center gap-2">
                    <i class="bi bi-search"></i>
                    <span>${this.escapeHtml(search)}</span>
                </div>
            `;
            item.addEventListener('click', () => {
                this.searchInput.value = search;
                this.search(search);
            });
            this.searchResults.appendChild(item);
        });
        
        this.showResults();
    }
    
    showNoResults(query) {
        this.searchResults.innerHTML = `
            <div class="search-no-results p-4 text-center">
                <i class="bi bi-search display-4 text-muted"></i>
                <p class="mt-2 mb-0">Ничего не найдено по запросу "<strong>${this.escapeHtml(query)}</strong>"</p>
                <small class="text-muted">Попробуйте изменить запрос</small>
            </div>
        `;
        this.showResults();
    }
    
    showError(message) {
        this.searchResults.innerHTML = `
            <div class="search-error p-3 text-center text-danger">
                <i class="bi bi-exclamation-triangle"></i> ${message}
            </div>
        `;
        this.showResults();
    }
    
    showResults() {
        this.searchResults.style.display = 'block';
    }
    
    hideResults() {
        this.searchResults.style.display = 'none';
    }
    
    handleKeyboard(e) {
        const items = this.searchResults.querySelectorAll('.search-result-item');
        if (items.length === 0) return;
        
        const currentIndex = Array.from(items).findIndex(item => item.classList.contains('active'));
        
        if (e.key === 'ArrowDown') {
            e.preventDefault();
            const nextIndex = currentIndex < items.length - 1 ? currentIndex + 1 : 0;
            this.setActiveItem(items, nextIndex);
        } else if (e.key === 'ArrowUp') {
            e.preventDefault();
            const prevIndex = currentIndex > 0 ? currentIndex - 1 : items.length - 1;
            this.setActiveItem(items, prevIndex);
        } else if (e.key === 'Enter' && currentIndex >= 0) {
            e.preventDefault();
            items[currentIndex].click();
        } else if (e.key === 'Escape') {
            this.hideResults();
        }
    }
    
    setActiveItem(items, index) {
        items.forEach(item => item.classList.remove('active'));
        items[index].classList.add('active');
        items[index].scrollIntoView({ block: 'nearest' });
    }
    
    saveRecentSearch(query) {
        if (!query || this.recentSearches.includes(query)) return;
        
        this.recentSearches.unshift(query);
        this.recentSearches = this.recentSearches.slice(0, 5);
        localStorage.setItem('recentSearches', JSON.stringify(this.recentSearches));
    }
    
    loadRecentSearches() {
        try {
            return JSON.parse(localStorage.getItem('recentSearches') || '[]');
        } catch {
            return [];
        }
    }
    
    formatDate(dateString) {
        const date = new Date(dateString);
        return date.toLocaleDateString('ru-RU', { day: '2-digit', month: '2-digit', year: 'numeric' });
    }
    
    escapeHtml(text) {
        const div = document.createElement('div');
        div.textContent = text;
        return div.innerHTML;
    }
    
    escapeRegex(text) {
        return text.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
    }
}

// Initialize search when DOM is ready
document.addEventListener('DOMContentLoaded', () => {
    new TournamentSearch();
});
