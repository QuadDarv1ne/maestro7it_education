// Tournament Comparison Feature
// Allows users to compare multiple tournaments side-by-side

class TournamentComparison {
    constructor() {
        this.selectedTournaments = JSON.parse(localStorage.getItem('comparisonTournaments') || '[]');
        this.maxComparisons = 4;
        this.init();
    }

    init() {
        this.createComparisonButton();
        this.updateComparisonBadge();
        this.attachEventListeners();
    }

    createComparisonButton() {
        // Add comparison button to navbar if not exists
        const navbar = document.querySelector('.navbar .d-flex');
        if (!navbar || document.getElementById('comparisonBtn')) return;

        const button = document.createElement('button');
        button.id = 'comparisonBtn';
        button.className = 'btn btn-outline-light position-relative me-2';
        button.innerHTML = `
            <i class="bi bi-bar-chart-line"></i> Сравнить
            <span class="position-absolute top-0 start-100 translate-middle badge rounded-pill bg-danger" 
                  id="comparisonBadge" style="display: none;">0</span>
        `;
        button.onclick = () => this.showComparisonModal();
        
        navbar.insertBefore(button, navbar.firstChild);
    }

    attachEventListeners() {
        // Add comparison checkboxes to tournament cards
        document.addEventListener('DOMContentLoaded', () => {
            this.addComparisonCheckboxes();
        });
    }

    addComparisonCheckboxes() {
        const tournamentCards = document.querySelectorAll('.tournament-card, .card');
        
        tournamentCards.forEach(card => {
            const tournamentId = this.extractTournamentId(card);
            if (!tournamentId) return;

            // Check if checkbox already exists
            if (card.querySelector('.comparison-checkbox')) return;

            const checkbox = document.createElement('div');
            checkbox.className = 'form-check position-absolute top-0 end-0 m-2';
            checkbox.innerHTML = `
                <input class="form-check-input comparison-checkbox" type="checkbox" 
                       value="${tournamentId}" id="compare_${tournamentId}"
                       ${this.selectedTournaments.includes(tournamentId) ? 'checked' : ''}>
                <label class="form-check-label" for="compare_${tournamentId}">
                    <small>Сравнить</small>
                </label>
            `;

            card.style.position = 'relative';
            card.appendChild(checkbox);

            checkbox.querySelector('input').addEventListener('change', (e) => {
                this.toggleTournament(tournamentId, e.target.checked);
            });
        });
    }

    extractTournamentId(card) {
        // Try to extract tournament ID from card
        const link = card.querySelector('a[href*="/tournament/"]');
        if (link) {
            const match = link.href.match(/\/tournament\/(\d+)/);
            return match ? parseInt(match[1]) : null;
        }
        return null;
    }

    toggleTournament(tournamentId, add) {
        if (add) {
            if (this.selectedTournaments.length >= this.maxComparisons) {
                alert(`Можно сравнить максимум ${this.maxComparisons} турнира`);
                const checkbox = document.getElementById(`compare_${tournamentId}`);
                if (checkbox) checkbox.checked = false;
                return;
            }
            if (!this.selectedTournaments.includes(tournamentId)) {
                this.selectedTournaments.push(tournamentId);
            }
        } else {
            this.selectedTournaments = this.selectedTournaments.filter(id => id !== tournamentId);
        }

        localStorage.setItem('comparisonTournaments', JSON.stringify(this.selectedTournaments));
        this.updateComparisonBadge();
    }

    updateComparisonBadge() {
        const badge = document.getElementById('comparisonBadge');
        if (badge) {
            if (this.selectedTournaments.length > 0) {
                badge.textContent = this.selectedTournaments.length;
                badge.style.display = 'block';
            } else {
                badge.style.display = 'none';
            }
        }
    }

    async showComparisonModal() {
        if (this.selectedTournaments.length < 2) {
            if (window.toast) {
                window.toast.warning('Выберите минимум 2 турнира для сравнения');
            } else {
                alert('Выберите минимум 2 турнира для сравнения');
            }
            return;
        }

        // Track achievement
        if (window.achievementsSystem) {
            window.achievementsSystem.trackAction('comparison_used');
        }

        // Fetch tournament data
        const tournaments = await this.fetchTournaments();
        
        // Create modal
        this.createModal(tournaments);
        
        if (window.toast) {
            window.toast.comparisonReady(this.selectedTournaments.length);
        }
    }

    async fetchTournaments() {
        const promises = this.selectedTournaments.map(id => 
            fetch(`/api/tournaments/${id}`).then(r => r.json())
        );
        return Promise.all(promises);
    }

    createModal(tournaments) {
        // Remove existing modal
        const existingModal = document.getElementById('comparisonModal');
        if (existingModal) existingModal.remove();

        const modal = document.createElement('div');
        modal.id = 'comparisonModal';
        modal.className = 'modal fade';
        modal.innerHTML = `
            <div class="modal-dialog modal-xl modal-dialog-scrollable">
                <div class="modal-content">
                    <div class="modal-header">
                        <h5 class="modal-title">
                            <i class="bi bi-bar-chart-line"></i> Сравнение турниров
                        </h5>
                        <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
                    </div>
                    <div class="modal-body">
                        ${this.generateComparisonTable(tournaments)}
                    </div>
                    <div class="modal-footer">
                        <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Закрыть</button>
                        <button type="button" class="btn btn-primary" onclick="tournamentComparison.clearComparison()">
                            <i class="bi bi-trash"></i> Очистить выбор
                        </button>
                    </div>
                </div>
            </div>
        `;

        document.body.appendChild(modal);
        const bsModal = new bootstrap.Modal(modal);
        bsModal.show();
    }

    generateComparisonTable(tournaments) {
        const fields = [
            { key: 'name', label: 'Название', format: v => v },
            { key: 'start_date', label: 'Дата начала', format: v => new Date(v).toLocaleDateString('ru-RU') },
            { key: 'end_date', label: 'Дата окончания', format: v => new Date(v).toLocaleDateString('ru-RU') },
            { key: 'location', label: 'Место проведения', format: v => v },
            { key: 'category', label: 'Категория', format: v => v },
            { key: 'status', label: 'Статус', format: v => v },
            { key: 'prize_fund', label: 'Призовой фонд', format: v => v || 'Не указан' },
            { key: 'organizer', label: 'Организатор', format: v => v || 'Не указан' },
            { key: 'participants_count', label: 'Участников', format: v => v || 'Не указано' }
        ];

        let html = '<div class="table-responsive"><table class="table table-bordered table-hover">';
        html += '<thead class="table-light"><tr><th>Параметр</th>';
        
        tournaments.forEach((t, i) => {
            html += `<th>Турнир ${i + 1}</th>`;
        });
        html += '</tr></thead><tbody>';

        fields.forEach(field => {
            html += `<tr><td class="fw-bold">${field.label}</td>`;
            tournaments.forEach(t => {
                html += `<td>${field.format(t[field.key])}</td>`;
            });
            html += '</tr>';
        });

        html += '</tbody></table></div>';
        return html;
    }

    clearComparison() {
        this.selectedTournaments = [];
        localStorage.removeItem('comparisonTournaments');
        
        // Uncheck all checkboxes
        document.querySelectorAll('.comparison-checkbox').forEach(cb => {
            cb.checked = false;
        });
        
        this.updateComparisonBadge();
        
        // Close modal
        const modal = bootstrap.Modal.getInstance(document.getElementById('comparisonModal'));
        if (modal) modal.hide();
    }
}

// Initialize
const tournamentComparison = new TournamentComparison();
