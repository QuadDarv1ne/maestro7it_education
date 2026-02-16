// Advanced Filtering System for Tournaments

class TournamentFilters {
    constructor() {
        this.filters = {
            category: [],
            location: [],
            dateRange: { start: null, end: null },
            rating: { min: 0, max: 5 },
            status: [],
            prizePool: { min: 0, max: null }
        };
        
        this.tournaments = [];
        this.filteredTournaments = [];
        
        this.init();
    }
    
    init() {
        this.loadTournaments();
        this.setupFilterControls();
        this.setupSorting();
        this.loadSavedFilters();
    }
    
    async loadTournaments() {
        try {
            const response = await fetch('/api/tournaments?limit=1000');
            const data = await response.json();
            this.tournaments = data.tournaments || [];
            this.applyFilters();
        } catch (error) {
            console.error('Failed to load tournaments:', error);
        }
    }
    
    setupFilterControls() {
        // Category filter
        const categoryCheckboxes = document.querySelectorAll('.filter-category');
        categoryCheckboxes.forEach(checkbox => {
            checkbox.addEventListener('change', (e) => {
                this.toggleFilter('category', e.target.value, e.target.checked);
            });
        });
        
        // Location filter
        const locationCheckboxes = document.querySelectorAll('.filter-location');
        locationCheckboxes.forEach(checkbox => {
            checkbox.addEventListener('change', (e) => {
                this.toggleFilter('location', e.target.value, e.target.checked);
            });
        });
        
        // Date range
        const startDateInput = document.getElementById('filterStartDate');
        const endDateInput = document.getElementById('filterEndDate');
        
        if (startDateInput) {
            startDateInput.addEventListener('change', (e) => {
                this.filters.dateRange.start = e.target.value;
                this.applyFilters();
            });
        }
        
        if (endDateInput) {
            endDateInput.addEventListener('change', (e) => {
                this.filters.dateRange.end = e.target.value;
                this.applyFilters();
            });
        }
        
        // Rating range
        const ratingSlider = document.getElementById('filterRating');
        if (ratingSlider) {
            ratingSlider.addEventListener('input', (e) => {
                this.filters.rating.min = parseFloat(e.target.value);
                document.getElementById('ratingValue').textContent = e.target.value;
                this.applyFilters();
            });
        }
        
        // Status filter
        const statusCheckboxes = document.querySelectorAll('.filter-status');
        statusCheckboxes.forEach(checkbox => {
            checkbox.addEventListener('change', (e) => {
                this.toggleFilter('status', e.target.value, e.target.checked);
            });
        });
        
        // Clear filters button
        const clearBtn = document.getElementById('clearFilters');
        if (clearBtn) {
            clearBtn.addEventListener('click', () => this.clearAllFilters());
        }
        
        // Save filters button
        const saveBtn = document.getElementById('saveFilters');
        if (saveBtn) {
            saveBtn.addEventListener('click', () => this.saveFilters());
        }
    }
    
    setupSorting() {
        const sortSelect = document.getElementById('sortBy');
        if (!sortSelect) return;
        
        sortSelect.addEventListener('change', (e) => {
            this.sortTournaments(e.target.value);
        });
    }
    
    toggleFilter(type, value, checked) {
        if (checked) {
            if (!this.filters[type].includes(value)) {
                this.filters[type].push(value);
            }
        } else {
            this.filters[type] = this.filters[type].filter(v => v !== value);
        }
        
        this.applyFilters();
    }
    
    applyFilters() {
        this.filteredTournaments = this.tournaments.filter(tournament => {
            // Category filter
            if (this.filters.category.length > 0) {
                if (!this.filters.category.includes(tournament.category)) {
                    return false;
                }
            }
            
            // Location filter
            if (this.filters.location.length > 0) {
                const matchesLocation = this.filters.location.some(loc => 
                    tournament.location.toLowerCase().includes(loc.toLowerCase())
                );
                if (!matchesLocation) return false;
            }
            
            // Date range filter
            if (this.filters.dateRange.start) {
                const startDate = new Date(tournament.start_date);
                const filterStart = new Date(this.filters.dateRange.start);
                if (startDate < filterStart) return false;
            }
            
            if (this.filters.dateRange.end) {
                const endDate = new Date(tournament.end_date);
                const filterEnd = new Date(this.filters.dateRange.end);
                if (endDate > filterEnd) return false;
            }
            
            // Rating filter
            if (tournament.average_rating < this.filters.rating.min) {
                return false;
            }
            
            // Status filter
            if (this.filters.status.length > 0) {
                if (!this.filters.status.includes(tournament.status)) {
                    return false;
                }
            }
            
            return true;
        });
        
        this.renderResults();
        this.updateFilterStats();
    }
    
    sortTournaments(sortBy) {
        switch (sortBy) {
            case 'date-asc':
                this.filteredTournaments.sort((a, b) => 
                    new Date(a.start_date) - new Date(b.start_date)
                );
                break;
            case 'date-desc':
                this.filteredTournaments.sort((a, b) => 
                    new Date(b.start_date) - new Date(a.start_date)
                );
                break;
            case 'rating-desc':
                this.filteredTournaments.sort((a, b) => 
                    (b.average_rating || 0) - (a.average_rating || 0)
                );
                break;
            case 'name-asc':
                this.filteredTournaments.sort((a, b) => 
                    a.name.localeCompare(b.name, 'ru')
                );
                break;
            case 'popularity':
                this.filteredTournaments.sort((a, b) => 
                    (b.views_count || 0) - (a.views_count || 0)
                );
                break;
        }
        
        this.renderResults();
    }
    
    renderResults() {
        const container = document.getElementById('tournamentsContainer');
        if (!container) return;
        
        if (this.filteredTournaments.length === 0) {
            container.innerHTML = `
                <div class="col-12">
                    <div class="text-center py-5">
                        <i class="bi bi-search" style="font-size: 4rem; color: var(--text-muted);"></i>
                        <h4 class="mt-3">Турниры не найдены</h4>
                        <p class="text-muted">Попробуйте изменить фильтры</p>
                        <button class="btn btn-primary" onclick="tournamentFilters.clearAllFilters()">
                            Сбросить фильтры
                        </button>
                    </div>
                </div>
            `;
            return;
        }
        
        container.innerHTML = this.filteredTournaments.map(tournament => `
            <div class="col-md-6 col-lg-4 mb-4">
                <div class="card tournament-card h-100">
                    <div class="card-body">
                        <h5 class="card-title">
                            <a href="/tournament/${tournament.id}" class="text-decoration-none">
                                ${this.escapeHtml(tournament.name)}
                            </a>
                        </h5>
                        <p class="text-muted mb-2">
                            <i class="bi bi-geo-alt"></i> ${this.escapeHtml(tournament.location)}
                        </p>
                        <p class="text-muted mb-2">
                            <i class="bi bi-calendar"></i> 
                            ${this.formatDate(tournament.start_date)} - ${this.formatDate(tournament.end_date)}
                        </p>
                        ${tournament.category ? `
                            <span class="badge bg-secondary">${this.escapeHtml(tournament.category)}</span>
                        ` : ''}
                        ${tournament.average_rating ? `
                            <div class="mt-2">
                                ${this.renderStars(tournament.average_rating)}
                                <small class="text-muted">(${tournament.average_rating.toFixed(1)})</small>
                            </div>
                        ` : ''}
                    </div>
                </div>
            </div>
        `).join('');
    }
    
    updateFilterStats() {
        const statsElement = document.getElementById('filterStats');
        if (statsElement) {
            statsElement.innerHTML = `
                <span class="badge bg-primary">
                    Найдено: ${this.filteredTournaments.length} из ${this.tournaments.length}
                </span>
            `;
        }
    }
    
    clearAllFilters() {
        this.filters = {
            category: [],
            location: [],
            dateRange: { start: null, end: null },
            rating: { min: 0, max: 5 },
            status: [],
            prizePool: { min: 0, max: null }
        };
        
        // Reset UI
        document.querySelectorAll('.filter-category, .filter-location, .filter-status')
            .forEach(cb => cb.checked = false);
        
        const startDate = document.getElementById('filterStartDate');
        const endDate = document.getElementById('filterEndDate');
        if (startDate) startDate.value = '';
        if (endDate) endDate.value = '';
        
        const ratingSlider = document.getElementById('filterRating');
        if (ratingSlider) {
            ratingSlider.value = 0;
            document.getElementById('ratingValue').textContent = '0';
        }
        
        this.applyFilters();
        
        if (window.ChessCalendar) {
            window.ChessCalendar.showToast('Фильтры сброшены', 'info');
        }
    }
    
    saveFilters() {
        localStorage.setItem('tournamentFilters', JSON.stringify(this.filters));
        
        if (window.ChessCalendar) {
            window.ChessCalendar.showToast('Фильтры сохранены', 'success');
        }
    }
    
    loadSavedFilters() {
        const saved = localStorage.getItem('tournamentFilters');
        if (saved) {
            try {
                this.filters = JSON.parse(saved);
                this.restoreFilterUI();
                this.applyFilters();
            } catch (e) {
                console.error('Failed to load saved filters:', e);
            }
        }
    }
    
    restoreFilterUI() {
        // Restore checkboxes
        this.filters.category.forEach(value => {
            const checkbox = document.querySelector(`.filter-category[value="${value}"]`);
            if (checkbox) checkbox.checked = true;
        });
        
        this.filters.location.forEach(value => {
            const checkbox = document.querySelector(`.filter-location[value="${value}"]`);
            if (checkbox) checkbox.checked = true;
        });
        
        this.filters.status.forEach(value => {
            const checkbox = document.querySelector(`.filter-status[value="${value}"]`);
            if (checkbox) checkbox.checked = true;
        });
        
        // Restore date range
        if (this.filters.dateRange.start) {
            const startDate = document.getElementById('filterStartDate');
            if (startDate) startDate.value = this.filters.dateRange.start;
        }
        
        if (this.filters.dateRange.end) {
            const endDate = document.getElementById('filterEndDate');
            if (endDate) endDate.value = this.filters.dateRange.end;
        }
        
        // Restore rating
        const ratingSlider = document.getElementById('filterRating');
        if (ratingSlider) {
            ratingSlider.value = this.filters.rating.min;
            document.getElementById('ratingValue').textContent = this.filters.rating.min;
        }
    }
    
    renderStars(rating) {
        const fullStars = Math.floor(rating);
        const hasHalfStar = rating % 1 >= 0.5;
        let html = '';
        
        for (let i = 0; i < fullStars; i++) {
            html += '<i class="bi bi-star-fill text-warning"></i>';
        }
        
        if (hasHalfStar) {
            html += '<i class="bi bi-star-half text-warning"></i>';
        }
        
        const emptyStars = 5 - fullStars - (hasHalfStar ? 1 : 0);
        for (let i = 0; i < emptyStars; i++) {
            html += '<i class="bi bi-star text-warning"></i>';
        }
        
        return html;
    }
    
    formatDate(dateString) {
        if (!dateString) return 'Дата не указана';
        const date = new Date(dateString);
        return date.toLocaleDateString('ru-RU', { 
            day: '2-digit', 
            month: '2-digit', 
            year: 'numeric' 
        });
    }
    
    escapeHtml(text) {
        const div = document.createElement('div');
        div.textContent = text;
        return div.innerHTML;
    }
}

// Initialize on DOM ready
let tournamentFilters;
document.addEventListener('DOMContentLoaded', () => {
    if (document.getElementById('tournamentsContainer')) {
        tournamentFilters = new TournamentFilters();
    }
});

// Export for global use
window.TournamentFilters = TournamentFilters;
