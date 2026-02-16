// ChessCalendar-RU - Tournament Features Bundle
// Consolidated tournament-related functionality for optimized loading

// Import necessary utilities
import { debounce, throttle } from './utils.js';

// Tournament comparison functionality
export class TournamentComparison {
    constructor() {
        this.comparedTournaments = [];
        this.maxCompare = 4; // Maximum tournaments to compare
    }

    addTournament(tournamentId) {
        if (this.comparedTournaments.length >= this.maxCompare) {
            alert(`Можно сравнивать не более ${this.maxCompare} турниров одновременно`);
            return false;
        }

        if (!this.comparedTournaments.includes(tournamentId)) {
            this.comparedTournaments.push(tournamentId);
            this.updateComparisonUI();
            return true;
        }
        return false;
    }

    removeTournament(tournamentId) {
        this.comparedTournaments = this.comparedTournaments.filter(id => id !== tournamentId);
        this.updateComparisonUI();
    }

    updateComparisonUI() {
        // Update the comparison UI - would typically update a modal or sidebar
        const compareCount = document.getElementById('compare-count');
        if (compareCount) {
            compareCount.textContent = this.comparedTournaments.length;
            compareCount.style.display = this.comparedTournaments.length > 0 ? 'inline' : 'none';
        }
        
        // Trigger custom event
        document.dispatchEvent(new CustomEvent('tournamentComparisonUpdated', {
            detail: { count: this.comparedTournaments.length }
        }));
    }

    clearAll() {
        this.comparedTournaments = [];
        this.updateComparisonUI();
    }
}

// Favorites manager
export class FavoritesManager {
    constructor() {
        this.favorites = new Set(JSON.parse(localStorage.getItem('favorites') || '[]'));
    }

    addFavorite(tournamentId) {
        this.favorites.add(tournamentId.toString());
        this.saveFavorites();
        this.updateUI();
    }

    removeFavorite(tournamentId) {
        this.favorites.delete(tournamentId.toString());
        this.saveFavorites();
        this.updateUI();
    }

    isFavorite(tournamentId) {
        return this.favorites.has(tournamentId.toString());
    }

    saveFavorites() {
        localStorage.setItem('favorites', JSON.stringify(Array.from(this.favorites)));
    }

    updateUI() {
        // Update UI elements showing favorite counts
        document.querySelectorAll('[data-favorite-count]').forEach(el => {
            el.textContent = this.favorites.size;
        });
        
        // Update individual favorite buttons
        document.querySelectorAll('[data-tournament-id]').forEach(btn => {
            const id = btn.getAttribute('data-tournament-id');
            if (this.isFavorite(id)) {
                btn.classList.add('favorited');
                btn.innerHTML = '<i class="bi bi-heart-fill"></i> В избранном';
            } else {
                btn.classList.remove('favorited');
                btn.innerHTML = '<i class="bi bi-heart"></i> В избранное';
            }
        });
    }

    getFavorites() {
        return Array.from(this.favorites).map(id => parseInt(id));
    }
}

// Rating system
export class RatingSystem {
    constructor() {
        this.currentRatings = {};
    }

    async submitRating(tournamentId, rating, review = '') {
        try {
            const response = await fetch('/api/tournaments/' + tournamentId + '/rate', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    user_id: window.currentUser?.id || 1, // Would get from session
                    rating: rating,
                    review: review
                })
            });

            if (response.ok) {
                const data = await response.json();
                // Update local cache
                this.currentRatings[tournamentId] = rating;
                return data;
            } else {
                throw new Error('Failed to submit rating');
            }
        } catch (error) {
            console.error('Rating submission error:', error);
            throw error;
        }
    }

    async getTournamentRating(tournamentId) {
        try {
            const response = await fetch(`/api/tournaments/${tournamentId}`);
            const data = await response.json();
            return data.rating || 0;
        } catch (error) {
            console.error('Rating fetch error:', error);
            return 0;
        }
    }
}

// Search functionality
export class TournamentSearch {
    constructor() {
        this.debounceTimeout = null;
        this.lastQuery = '';
    }

    async search(query, filters = {}) {
        if (query.length < 2) return [];

        // Debounce multiple rapid requests
        if (this.debounceTimeout) {
            clearTimeout(this.debounceTimeout);
        }

        return new Promise((resolve, reject) => {
            this.debounceTimeout = setTimeout(async () => {
                try {
                    const params = new URLSearchParams({
                        q: query,
                        ...filters
                    });

                    const response = await fetch(`/api/tournaments/search?${params}`);
                    const data = await response.json();
                    
                    this.lastQuery = query;
                    resolve(data.tournaments || []);
                } catch (error) {
                    reject(error);
                }
            }, 300);
        });
    }
}

// Filter functionality
export class TournamentFilters {
    constructor() {
        this.filters = {
            category: '',
            location: '',
            status: '',
            startDate: '',
            endDate: ''
        };
    }

    setFilter(name, value) {
        this.filters[name] = value;
        this.saveFilters();
    }

    getFilters() {
        return { ...this.filters };
    }

    saveFilters() {
        localStorage.setItem('tournamentFilters', JSON.stringify(this.filters));
    }

    loadFilters() {
        const saved = localStorage.getItem('tournamentFilters');
        if (saved) {
            this.filters = { ...this.filters, ...JSON.parse(saved) };
        }
    }

    applyFilters(tournaments) {
        return tournaments.filter(tournament => {
            if (this.filters.category && tournament.category !== this.filters.category) return false;
            if (this.filters.location && !tournament.location.toLowerCase().includes(this.filters.location.toLowerCase())) return false;
            if (this.filters.status && tournament.status !== this.filters.status) return false;
            if (this.filters.startDate && new Date(tournament.start_date) < new Date(this.filters.startDate)) return false;
            if (this.filters.endDate && new Date(tournament.end_date) > new Date(this.filters.endDate)) return false;
            
            return true;
        });
    }
}

// Initialize when DOM is ready
document.addEventListener('DOMContentLoaded', () => {
    // Initialize components
    window.tournamentComparison = new TournamentComparison();
    window.favoritesManager = new FavoritesManager();
    window.ratingSystem = new RatingSystem();
    window.tournamentSearch = new TournamentSearch();
    window.tournamentFilters = new TournamentFilters();
    
    // Load saved filters
    window.tournamentFilters.loadFilters();
    
    // Update UI for favorites
    window.favoritesManager.updateUI();
});

// Export everything for bundle
export default {
    TournamentComparison,
    FavoritesManager,
    RatingSystem,
    TournamentSearch,
    TournamentFilters,
    debounce,
    throttle
};