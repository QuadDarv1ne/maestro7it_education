// Advanced Filtering System for Tournaments

class AdvancedFilters {
    constructor() {
        this.filters = {
            search: '',
            category: '',
            status: '',
            location: '',
            dateFrom: '',
            dateTo: '',
            prizeMin: '',
            prizeMax: '',
            tags: []
        };
        this.init();
    }

    init() {
        this.loadSavedFilters();
        this.createFilterPanel();
        this.attachEventListeners();
    }

    loadSavedFilters() {
        const saved = localStorage.getItem('tournamentFilters');
        if (saved) {
            this.filters = { ...this.filters, ...JSON.parse(saved) };
        }
    }

    saveFilters() {
        localStorage.setItem('tournamentFilters', JSON.stringify(this.filters));
    }

    createFilterPanel() {
        // Check if filter panel already exists
        if (document.getElementById('advancedFiltersPanel')) return;

        const panel = document.createElement('div');
        panel.id = 'advancedFiltersPanel';
        panel.className = 'advanced-filters-panel';
        panel.innerHTML = `
            <style>
                .advanced-filters-panel {
                    background: var(--bg-primary);
                    border-radius: var(--border-radius);
                    padding: 1.5rem;
                    margin-bottom: 2rem;
                    box-shadow: var(--box-shadow);
                    border: 2px solid var(--border-color);
                }
                
                .filter-header {
                    display: flex;
                    justify-content: space-between;
                    align-items: center;
                    margin-bottom: 1.5rem;
                    padding-bottom: 1rem;
                    border-bottom: 2px solid var(--border-color);
                }
                
                .filter-header h4 {
                    margin: 0;
                    display: flex;
                    align-items: center;
                    gap: 0.5rem;
                    color: var(--text-primary);
                    font-weight: 700;
                }
                
                .filter-grid {
                    display: grid;
                    grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
                    gap: 1rem;
                    margin-bottom: 1rem;
                }
                
                .filter-group {
                    display: flex;
                    flex-direction: column;
                    gap: 0.5rem;
                }
                
                .filter-group label {
                    font-weight: 600;
                    font-size: 0.875rem;
                    color: var(--text-primary);
                    display: flex;
                    align-items: center;
                    gap: 0.25rem;
                }
                
                .filter-actions {
                    display: flex;
                    gap: 1rem;
                    justify-content: flex-end;
                    margin-top: 1.5rem;
                    padding-top: 1rem;
                    border-top: 1px solid var(--border-color);
                }
                
                .tag-input-container {
                    display: flex;
                    flex-wrap: wrap;
                    gap: 0.5rem;
                    padding: 0.5rem;
                    border: 1px solid var(--border-color);
                    border-radius: 8px;
                    background: var(--bg-primary);
                }
                
                .tag-badge {
                    display: inline-flex;
                    align-items: center;
                    gap: 0.25rem;
                    padding: 0.25rem 0.75rem;
                    background: var(--primary-color);
                    color: white;
                    border-radius: 20px;
                    font-size: 0.875rem;
                }
                
                .tag-badge button {
                    background: none;
                    border: none;
                    color: white;
                    cursor: pointer;
                    padding: 0;
                    margin-left: 0.25rem;
                }
                
                .active-filters {
                    display: flex;
                    flex-wrap: wrap;
                    gap: 0.5rem;
                    margin-top: 1rem;
                    padding-top: 1rem;
                    border-top: 1px solid var(--border-color);
                }
                
                .active-filter-badge {
                    display: inline-flex;
                    align-items: center;
                    gap: 0.5rem;
                    padding: 0.5rem 1rem;
                    background: var(--bg-secondary);
                    border-radius: 20px;
                    font-size: 0.875rem;
                    color: var(--text-primary);
                    border: 1px solid var(--border-color);
                }
                
                .active-filter-badge button {
                    background: none;
                    border: none;
                    color: var(--text-secondary);
                    cursor: pointer;
                    padding: 0;
                    font-size: 1.1rem;
                    line-height: 1;
                }
                
                .active-filter-badge button:hover {
                    color: var(--danger-color);
                }
                
                #filterContent {
                    transition: all 0.3s ease;
                }
                
                #filterContent.collapsed {
                    display: none;
                }
            </style>
            
            <div class="filter-header">
                <h4>
                    <i class="bi bi-funnel"></i> Расширенные фильтры
                </h4>
                <button class="btn btn-sm btn-outline-secondary" onclick="advancedFilters.togglePanel()">
                    <i class="bi bi-chevron-up" id="filterToggleIcon"></i>
                </button>
            </div>
            
            <div id="filterContent">
                <div class="filter-grid">
                    <div class="filter-group">
                        <label for="filterCategory">Категория</label>
                        <select class="form-select" id="filterCategory">
                            <option value="">Все категории</option>
                        </select>
                    </div>
                    
                    <div class="filter-group">
                        <label for="filterStatus">Статус</label>
                        <select class="form-select" id="filterStatus">
                            <option value="">Все статусы</option>
                            <option value="upcoming">Предстоящие</option>
                            <option value="ongoing">Идут сейчас</option>
                            <option value="completed">Завершенные</option>
                        </select>
                    </div>
                    
                    <div class="filter-group">
                        <label for="filterLocation">Город</label>
                        <input type="text" class="form-control" id="filterLocation" 
                               placeholder="Введите город...">
                    </div>
                    
                    <div class="filter-group">
                        <label for="filterDateFrom">Дата от</label>
                        <input type="date" class="form-control" id="filterDateFrom">
                    </div>
                    
                    <div class="filter-group">
                        <label for="filterDateTo">Дата до</label>
                        <input type="date" class="form-control" id="filterDateTo">
                    </div>
                    
                    <div class="filter-group">
                        <label for="filterPrizeMin">Призовой фонд от</label>
                        <input type="number" class="form-control" id="filterPrizeMin" 
                               placeholder="0">
                    </div>
                </div>
                
                <div class="filter-actions">
                    <button class="btn btn-outline-secondary" onclick="advancedFilters.resetFilters()">
                        <i class="bi bi-x-circle"></i> Сбросить
                    </button>
                    <button class="btn btn-primary" onclick="advancedFilters.applyFilters()">
                        <i class="bi bi-check-circle"></i> Применить
                    </button>
                </div>
                
                <div class="active-filters" id="activeFilters"></div>
            </div>
        `;

        // Insert before tournament list
        const container = document.querySelector('.container-fluid, .container');
        if (container) {
            const firstChild = container.querySelector('.row');
            if (firstChild) {
                container.insertBefore(panel, firstChild);
            } else {
                container.prepend(panel);
            }
        }
    }

    attachEventListeners() {
        // Load categories dynamically
        this.loadCategories();
        
        // Apply saved filters
        this.applySavedFilters();
    }

    async loadCategories() {
        try {
            const response = await fetch('/api/tournaments');
            const data = await response.json();
            
            const categories = new Set();
            data.tournaments.forEach(t => {
                if (t.category) categories.add(t.category);
            });
            
            const select = document.getElementById('filterCategory');
            if (select) {
                categories.forEach(cat => {
                    const option = document.createElement('option');
                    option.value = cat;
                    option.textContent = cat;
                    select.appendChild(option);
                });
            }
        } catch (error) {
            console.error('Error loading categories:', error);
        }
    }

    applySavedFilters() {
        // Apply saved filter values to inputs
        Object.keys(this.filters).forEach(key => {
            const input = document.getElementById(`filter${key.charAt(0).toUpperCase() + key.slice(1)}`);
            if (input && this.filters[key]) {
                input.value = this.filters[key];
            }
        });
        
        this.updateActiveFilters();
    }

    applyFilters() {
        // Collect filter values
        this.filters.category = document.getElementById('filterCategory')?.value || '';
        this.filters.status = document.getElementById('filterStatus')?.value || '';
        this.filters.location = document.getElementById('filterLocation')?.value || '';
        this.filters.dateFrom = document.getElementById('filterDateFrom')?.value || '';
        this.filters.dateTo = document.getElementById('filterDateTo')?.value || '';
        this.filters.prizeMin = document.getElementById('filterPrizeMin')?.value || '';
        
        // Save filters
        this.saveFilters();
        
        // Track achievement
        if (window.achievementsSystem) {
            window.achievementsSystem.trackAction('filter_used');
        }
        
        // Show toast
        if (window.toast) {
            window.toast.filterApplied();
        }
        
        // Build query string
        const params = new URLSearchParams();
        Object.keys(this.filters).forEach(key => {
            if (this.filters[key]) {
                params.append(key, this.filters[key]);
            }
        });
        
        // Redirect with filters
        window.location.href = `${window.location.pathname}?${params.toString()}`;
    }

    resetFilters() {
        this.filters = {
            search: '',
            category: '',
            status: '',
            location: '',
            dateFrom: '',
            dateTo: '',
            prizeMin: '',
            prizeMax: '',
            tags: []
        };
        
        localStorage.removeItem('tournamentFilters');
        
        // Clear inputs
        document.querySelectorAll('#advancedFiltersPanel input, #advancedFiltersPanel select').forEach(input => {
            input.value = '';
        });
        
        this.updateActiveFilters();
        
        // Reload without filters
        window.location.href = window.location.pathname;
    }

    updateActiveFilters() {
        const container = document.getElementById('activeFilters');
        if (!container) return;
        
        container.innerHTML = '';
        
        const activeCount = Object.values(this.filters).filter(v => v && v.length > 0).length;
        
        if (activeCount === 0) {
            container.innerHTML = '<small class="text-muted">Фильтры не применены</small>';
            return;
        }
        
        Object.keys(this.filters).forEach(key => {
            if (this.filters[key]) {
                const badge = document.createElement('div');
                badge.className = 'active-filter-badge';
                badge.innerHTML = `
                    <strong>${this.getFilterLabel(key)}:</strong> ${this.filters[key]}
                    <button onclick="advancedFilters.removeFilter('${key}')">
                        <i class="bi bi-x"></i>
                    </button>
                `;
                container.appendChild(badge);
            }
        });
    }

    getFilterLabel(key) {
        const labels = {
            category: 'Категория',
            status: 'Статус',
            location: 'Город',
            dateFrom: 'Дата от',
            dateTo: 'Дата до',
            prizeMin: 'Призовой фонд от'
        };
        return labels[key] || key;
    }

    removeFilter(key) {
        this.filters[key] = '';
        const input = document.getElementById(`filter${key.charAt(0).toUpperCase() + key.slice(1)}`);
        if (input) input.value = '';
        
        this.saveFilters();
        this.updateActiveFilters();
        this.applyFilters();
    }

    togglePanel() {
        const content = document.getElementById('filterContent');
        const icon = document.getElementById('filterToggleIcon');
        
        if (content.style.display === 'none') {
            content.style.display = 'block';
            icon.className = 'bi bi-chevron-up';
        } else {
            content.style.display = 'none';
            icon.className = 'bi bi-chevron-down';
        }
    }
}

// DISABLED: This feature is redundant with the main filter form in index.html
// To re-enable, uncomment the line below:
// if (window.location.pathname === '/' || window.location.pathname.includes('/tournaments')) {
//     const advancedFilters = new AdvancedFilters();
// }
