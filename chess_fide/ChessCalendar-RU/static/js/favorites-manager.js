// Favorites Manager - Quick access to favorite tournaments

class FavoritesManager {
    constructor() {
        this.favorites = this.loadFavorites();
        this.init();
    }

    init() {
        this.createFavoritesPanel();
        this.addFavoriteButtons();
        this.updateFavoritesCount();
    }

    loadFavorites() {
        const saved = localStorage.getItem('favoriteTournaments');
        return saved ? JSON.parse(saved) : [];
    }

    saveFavorites() {
        localStorage.setItem('favoriteTournaments', JSON.stringify(this.favorites));
        this.updateFavoritesCount();
    }

    createFavoritesPanel() {
        // Add favorites button to navbar
        const navbar = document.querySelector('.navbar .d-flex');
        if (!navbar || document.getElementById('favoritesBtn')) return;

        const button = document.createElement('button');
        button.id = 'favoritesBtn';
        button.className = 'btn btn-outline-light position-relative me-2';
        button.innerHTML = `
            <i class="bi bi-heart-fill"></i> Избранное
            <span class="position-absolute top-0 start-100 translate-middle badge rounded-pill bg-danger" 
                  id="favoritesBadge" style="display: none;">0</span>
        `;
        button.onclick = () => this.showFavoritesModal();
        
        navbar.insertBefore(button, navbar.firstChild);
    }

    addFavoriteButtons() {
        // Add favorite buttons to tournament cards
        document.addEventListener('DOMContentLoaded', () => {
            this.attachFavoriteButtons();
        });

        // Re-attach on dynamic content load
        const observer = new MutationObserver(() => {
            this.attachFavoriteButtons();
        });

        observer.observe(document.body, {
            childList: true,
            subtree: true
        });
    }

    attachFavoriteButtons() {
        const tournamentCards = document.querySelectorAll('.tournament-card, .card');
        
        tournamentCards.forEach(card => {
            if (card.querySelector('.favorite-btn')) return;

            const tournamentId = this.extractTournamentId(card);
            if (!tournamentId) return;

            const isFavorite = this.isFavorite(tournamentId);
            
            const button = document.createElement('button');
            button.className = 'btn btn-sm btn-outline-danger favorite-btn position-absolute';
            button.style.cssText = 'top: 10px; right: 10px; z-index: 10;';
            button.innerHTML = `<i class="bi bi-heart${isFavorite ? '-fill' : ''}"></i>`;
            button.title = isFavorite ? 'Удалить из избранного' : 'Добавить в избранное';
            
            button.addEventListener('click', (e) => {
                e.preventDefault();
                e.stopPropagation();
                this.toggleFavorite(tournamentId, card);
            });

            card.style.position = 'relative';
            card.appendChild(button);
        });
    }

    extractTournamentId(card) {
        const link = card.querySelector('a[href*="/tournament/"]');
        if (link) {
            const match = link.href.match(/\/tournament\/(\d+)/);
            return match ? parseInt(match[1]) : null;
        }
        return null;
    }

    async toggleFavorite(tournamentId, card) {
        const button = card.querySelector('.favorite-btn');
        const icon = button.querySelector('i');

        if (this.isFavorite(tournamentId)) {
            // Remove from favorites
            this.favorites = this.favorites.filter(fav => fav.id !== tournamentId);
            icon.className = 'bi bi-heart';
            button.title = 'Добавить в избранное';
            button.classList.remove('btn-danger');
            button.classList.add('btn-outline-danger');
            
            if (window.toast) {
                window.toast.tournamentRemoved();
            }
        } else {
            // Add to favorites
            const tournamentData = await this.fetchTournamentData(tournamentId);
            if (tournamentData) {
                this.favorites.push(tournamentData);
                icon.className = 'bi bi-heart-fill';
                button.title = 'Удалить из избранного';
                button.classList.remove('btn-outline-danger');
                button.classList.add('btn-danger');
                
                if (window.toast) {
                    window.toast.tournamentAdded();
                }
                
                // Track achievement
                if (window.achievementsSystem) {
                    window.achievementsSystem.trackAction('favorite_added');
                }
            }
        }

        this.saveFavorites();
        
        // Animate button
        button.style.transform = 'scale(1.3)';
        setTimeout(() => {
            button.style.transform = 'scale(1)';
        }, 200);
    }

    async fetchTournamentData(tournamentId) {
        try {
            const response = await fetch(`/api/tournaments/${tournamentId}`);
            if (response.ok) {
                return await response.json();
            }
        } catch (error) {
            console.error('Error fetching tournament:', error);
            if (window.toast) {
                window.toast.error('Не удалось загрузить данные турнира');
            }
        }
        return null;
    }

    isFavorite(tournamentId) {
        return this.favorites.some(fav => fav.id === tournamentId);
    }

    updateFavoritesCount() {
        const badge = document.getElementById('favoritesBadge');
        if (badge) {
            if (this.favorites.length > 0) {
                badge.textContent = this.favorites.length;
                badge.style.display = 'block';
            } else {
                badge.style.display = 'none';
            }
        }
    }

    showFavoritesModal() {
        if (this.favorites.length === 0) {
            if (window.toast) {
                window.toast.info('У вас пока нет избранных турниров');
            }
            return;
        }

        // Remove existing modal
        const existingModal = document.getElementById('favoritesModal');
        if (existingModal) existingModal.remove();

        const modal = document.createElement('div');
        modal.id = 'favoritesModal';
        modal.className = 'modal fade';
        modal.innerHTML = `
            <div class="modal-dialog modal-lg modal-dialog-scrollable">
                <div class="modal-content">
                    <div class="modal-header">
                        <h5 class="modal-title">
                            <i class="bi bi-heart-fill text-danger"></i> Избранные турниры
                        </h5>
                        <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
                    </div>
                    <div class="modal-body">
                        ${this.generateFavoritesList()}
                    </div>
                    <div class="modal-footer">
                        <button type="button" class="btn btn-outline-danger" onclick="favoritesManager.clearAllFavorites()">
                            <i class="bi bi-trash"></i> Очистить все
                        </button>
                        <button type="button" class="btn btn-primary" onclick="favoritesManager.exportFavorites()">
                            <i class="bi bi-download"></i> Экспортировать
                        </button>
                        <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Закрыть</button>
                    </div>
                </div>
            </div>
        `;

        document.body.appendChild(modal);
        const bsModal = new bootstrap.Modal(modal);
        bsModal.show();
    }

    generateFavoritesList() {
        if (this.favorites.length === 0) {
            return '<p class="text-center text-muted">Нет избранных турниров</p>';
        }

        let html = '<div class="list-group">';
        
        this.favorites.forEach(tournament => {
            html += `
                <div class="list-group-item list-group-item-action">
                    <div class="d-flex w-100 justify-content-between align-items-start">
                        <div class="flex-grow-1">
                            <h6 class="mb-1">
                                <a href="/tournament/${tournament.id}" class="text-decoration-none">
                                    ${tournament.name}
                                </a>
                            </h6>
                            <p class="mb-1 text-muted">
                                <i class="bi bi-geo-alt"></i> ${tournament.location}
                            </p>
                            <small class="text-success">
                                <i class="bi bi-calendar"></i> 
                                ${this.formatDate(tournament.start_date)} - ${this.formatDate(tournament.end_date)}
                            </small>
                        </div>
                        <button class="btn btn-sm btn-outline-danger" 
                                onclick="favoritesManager.removeFavorite(${tournament.id})"
                                title="Удалить из избранного">
                            <i class="bi bi-x-lg"></i>
                        </button>
                    </div>
                    ${tournament.category ? `<span class="badge bg-primary mt-2">${tournament.category}</span>` : ''}
                    ${tournament.prize_fund ? `<span class="badge bg-success mt-2">${tournament.prize_fund}</span>` : ''}
                </div>
            `;
        });

        html += '</div>';
        return html;
    }

    formatDate(dateString) {
        const date = new Date(dateString);
        return date.toLocaleDateString('ru-RU', {
            day: '2-digit',
            month: '2-digit',
            year: 'numeric'
        });
    }

    removeFavorite(tournamentId) {
        this.favorites = this.favorites.filter(fav => fav.id !== tournamentId);
        this.saveFavorites();
        
        // Update modal
        const modal = document.getElementById('favoritesModal');
        if (modal) {
            const modalBody = modal.querySelector('.modal-body');
            modalBody.innerHTML = this.generateFavoritesList();
        }

        // Update buttons on page
        this.attachFavoriteButtons();

        if (window.toast) {
            window.toast.info('Турнир удален из избранного');
        }
    }

    clearAllFavorites() {
        if (confirm('Вы уверены, что хотите удалить все избранные турниры?')) {
            this.favorites = [];
            this.saveFavorites();
            
            // Close modal
            const modal = bootstrap.Modal.getInstance(document.getElementById('favoritesModal'));
            if (modal) modal.hide();

            // Update buttons on page
            this.attachFavoriteButtons();

            if (window.toast) {
                window.toast.success('Все избранные турниры удалены');
            }
        }
    }

    async exportFavorites() {
        if (this.favorites.length === 0) {
            if (window.toast) {
                window.toast.warning('Нет турниров для экспорта');
            }
            return;
        }

        // Create CSV
        let csv = 'Название,Дата начала,Дата окончания,Место,Категория,Призовой фонд\n';
        
        this.favorites.forEach(t => {
            csv += `"${t.name}","${t.start_date}","${t.end_date}","${t.location}","${t.category || ''}","${t.prize_fund || ''}"\n`;
        });

        // Download
        const blob = new Blob([csv], { type: 'text/csv;charset=utf-8;' });
        const link = document.createElement('a');
        link.href = URL.createObjectURL(blob);
        link.download = `favorites_${new Date().toISOString().split('T')[0]}.csv`;
        link.click();

        if (window.toast) {
            window.toast.exportSuccess('CSV');
        }
    }

    // Quick access methods
    getFavorites() {
        return this.favorites;
    }

    getFavoriteIds() {
        return this.favorites.map(fav => fav.id);
    }

    hasFavorites() {
        return this.favorites.length > 0;
    }
}

// Initialize
const favoritesManager = new FavoritesManager();
