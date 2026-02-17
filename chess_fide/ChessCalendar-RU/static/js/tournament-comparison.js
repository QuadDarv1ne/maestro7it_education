/**
 * Сравнение турниров
 * Позволяет пользователям сравнивать несколько турниров side-by-side
 */

class TournamentComparison {
    constructor(options = {}) {
        this.options = {
            maxCompare: options.maxCompare || 3,
            storageKey: options.storageKey || 'tournament_comparison',
            modalId: options.modalId || 'comparisonModal'
        };
        
        this.selectedTournaments = new Set();
        this.tournamentsData = new Map();
        
        this.init();
    }

    init() {
        this.loadFromStorage();
        this.attachEventListeners();
        this.updateUI();
    }

    /**
     * Загрузка из localStorage
     */
    loadFromStorage() {
        try {
            const stored = localStorage.getItem(this.options.storageKey);
            if (stored) {
                const data = JSON.parse(stored);
                this.selectedTournaments = new Set(data.ids || []);
                this.tournamentsData = new Map(Object.entries(data.tournaments || {}));
            }
        } catch (error) {
            console.error('Error loading comparison data:', error);
        }
    }

    /**
     * Сохранение в localStorage
     */
    saveToStorage() {
        try {
            const data = {
                ids: Array.from(this.selectedTournaments),
                tournaments: Object.fromEntries(this.tournamentsData)
            };
            localStorage.setItem(this.options.storageKey, JSON.stringify(data));
        } catch (error) {
            console.error('Error saving comparison data:', error);
        }
    }

    /**
     * Прикрепление обработчиков событий
     */
    attachEventListeners() {
        // Кнопки сравнения на карточках
        document.addEventListener('click', (e) => {
            const compareBtn = e.target.closest('[data-action="compare"]');
            if (compareBtn) {
                e.preventDefault();
                const card = compareBtn.closest('[data-tournament-id]');
                if (card) {
                    const tournamentId = parseInt(card.dataset.tournamentId);
                    this.toggleTournament(tournamentId, card);
                }
            }

            // Кнопка открытия модального окна сравнения
            const showCompareBtn = e.target.closest('#showComparisonBtn');
            if (showCompareBtn) {
                e.preventDefault();
                this.showComparisonModal();
            }

            // Кнопка очистки сравнения
            const clearBtn = e.target.closest('#clearComparisonBtn');
            if (clearBtn) {
                e.preventDefault();
                this.clearAll();
            }
        });
    }

    /**
     * Переключение турнира в сравнении
     */
    async toggleTournament(tournamentId, cardElement) {
        if (this.selectedTournaments.has(tournamentId)) {
            this.removeTournament(tournamentId);
        } else {
            if (this.selectedTournaments.size >= this.options.maxCompare) {
                this.showToast(
                    `Можно сравнивать максимум ${this.options.maxCompare} турнира`,
                    'warning'
                );
                return;
            }
            
            await this.addTournament(tournamentId, cardElement);
        }
        
        this.updateUI();
        this.saveToStorage();
    }

    /**
     * Добавление турнира в сравнение
     */
    async addTournament(tournamentId, cardElement) {
        // Извлекаем данные из карточки
        const tournamentData = this.extractTournamentData(cardElement);
        
        // Если данных нет в карточке, загружаем с сервера
        if (!tournamentData.name) {
            try {
                const data = await this.fetchTournamentData(tournamentId);
                this.tournamentsData.set(tournamentId, data);
            } catch (error) {
                console.error('Error fetching tournament data:', error);
                this.showToast('Ошибка загрузки данных турнира', 'error');
                return;
            }
        } else {
            this.tournamentsData.set(tournamentId, tournamentData);
        }
        
        this.selectedTournaments.add(tournamentId);
        this.showToast('Турнир добавлен в сравнение', 'success');
    }

    /**
     * Удаление турнира из сравнения
     */
    removeTournament(tournamentId) {
        this.selectedTournaments.delete(tournamentId);
        this.tournamentsData.delete(tournamentId);
        this.showToast('Турнир удален из сравнения', 'info');
    }

    /**
     * Извлечение данных турнира из карточки
     */
    extractTournamentData(cardElement) {
        return {
            id: parseInt(cardElement.dataset.tournamentId),
            name: cardElement.querySelector('.tournament-card-title, .tournament-card-title-modern')?.textContent?.trim() || '',
            location: cardElement.querySelector('[class*="location"]')?.textContent?.trim() || '',
            startDate: cardElement.querySelector('[class*="start-date"]')?.textContent?.trim() || '',
            endDate: cardElement.querySelector('[class*="end-date"]')?.textContent?.trim() || '',
            category: cardElement.querySelector('[class*="category"]')?.textContent?.trim() || '',
            status: cardElement.querySelector('[class*="status"]')?.textContent?.trim() || '',
            prizeFund: cardElement.querySelector('[class*="prize"]')?.textContent?.trim() || '',
            organizer: cardElement.querySelector('[class*="organizer"]')?.textContent?.trim() || ''
        };
    }

    /**
     * Загрузка данных турнира с сервера
     */
    async fetchTournamentData(tournamentId) {
        const response = await fetch(`/api/tournaments/${tournamentId}`, {
            headers: {
                'Accept': 'application/json'
            }
        });
        
        if (!response.ok) {
            throw new Error('Failed to fetch tournament data');
        }
        
        return await response.json();
    }

    /**
     * Показать модальное окно сравнения
     */
    showComparisonModal() {
        if (this.selectedTournaments.size === 0) {
            this.showToast('Выберите турниры для сравнения', 'warning');
            return;
        }
        
        const modal = this.createComparisonModal();
        document.body.appendChild(modal);
        
        // Показываем модальное окно
        const bsModal = new bootstrap.Modal(modal);
        bsModal.show();
        
        // Удаляем модальное окно после закрытия
        modal.addEventListener('hidden.bs.modal', () => {
            modal.remove();
        });
    }

    /**
     * Создание модального окна сравнения
     */
    createComparisonModal() {
        const modal = document.createElement('div');
        modal.className = 'modal fade';
        modal.id = this.options.modalId;
        modal.tabIndex = -1;
        
        const tournaments = Array.from(this.selectedTournaments).map(id => 
            this.tournamentsData.get(id)
        );
        
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
                        <div class="table-responsive">
                            <table class="table table-bordered table-hover comparison-table">
                                <thead class="table-light">
                                    <tr>
                                        <th style="width: 200px;">Параметр</th>
                                        ${tournaments.map(t => `
                                            <th class="text-center">
                                                <div class="d-flex flex-column align-items-center gap-2">
                                                    <span class="fw-bold">${t.name || 'Турнир'}</span>
                                                    <button class="btn btn-sm btn-outline-danger" 
                                                            onclick="tournamentComparison.removeTournament(${t.id}); this.closest('.modal').querySelector('[data-bs-dismiss]').click();">
                                                        <i class="bi bi-x-circle"></i> Удалить
                                                    </button>
                                                </div>
                                            </th>
                                        `).join('')}
                                    </tr>
                                </thead>
                                <tbody>
                                    ${this.generateComparisonRows(tournaments)}
                                </tbody>
                            </table>
                        </div>
                    </div>
                    <div class="modal-footer">
                        <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">
                            Закрыть
                        </button>
                        <button type="button" class="btn btn-danger" onclick="tournamentComparison.clearAll(); this.closest('.modal').querySelector('[data-bs-dismiss]').click();">
                            <i class="bi bi-trash"></i> Очистить все
                        </button>
                    </div>
                </div>
            </div>
        `;
        
        return modal;
    }

    /**
     * Генерация строк сравнения
     */
    generateComparisonRows(tournaments) {
        const fields = [
            { key: 'location', label: 'Место проведения', icon: 'geo-alt' },
            { key: 'startDate', label: 'Дата начала', icon: 'calendar-check' },
            { key: 'endDate', label: 'Дата окончания', icon: 'calendar-x' },
            { key: 'category', label: 'Категория', icon: 'tag' },
            { key: 'status', label: 'Статус', icon: 'info-circle' },
            { key: 'prizeFund', label: 'Призовой фонд', icon: 'currency-dollar' },
            { key: 'organizer', label: 'Организатор', icon: 'building' }
        ];
        
        return fields.map(field => `
            <tr>
                <td class="fw-semibold">
                    <i class="bi bi-${field.icon} text-primary me-2"></i>
                    ${field.label}
                </td>
                ${tournaments.map(t => `
                    <td class="text-center">
                        ${t[field.key] || '<span class="text-muted">Не указано</span>'}
                    </td>
                `).join('')}
            </tr>
        `).join('');
    }

    /**
     * Обновление UI
     */
    updateUI() {
        // Обновляем кнопки на карточках
        document.querySelectorAll('[data-tournament-id]').forEach(card => {
            const tournamentId = parseInt(card.dataset.tournamentId);
            const compareBtn = card.querySelector('[data-action="compare"]');
            
            if (compareBtn) {
                if (this.selectedTournaments.has(tournamentId)) {
                    compareBtn.classList.add('active');
                    compareBtn.innerHTML = '<i class="bi bi-check-circle-fill"></i>';
                    compareBtn.title = 'Убрать из сравнения';
                } else {
                    compareBtn.classList.remove('active');
                    compareBtn.innerHTML = '<i class="bi bi-bar-chart"></i>';
                    compareBtn.title = 'Добавить к сравнению';
                }
            }
        });
        
        // Обновляем плавающую панель сравнения
        this.updateFloatingPanel();
    }

    /**
     * Обновление плавающей панели
     */
    updateFloatingPanel() {
        let panel = document.getElementById('comparisonFloatingPanel');
        
        if (this.selectedTournaments.size === 0) {
            if (panel) {
                panel.remove();
            }
            return;
        }
        
        if (!panel) {
            panel = this.createFloatingPanel();
            document.body.appendChild(panel);
        }
        
        const counter = panel.querySelector('.comparison-counter');
        if (counter) {
            counter.textContent = this.selectedTournaments.size;
        }
    }

    /**
     * Создание плавающей панели
     */
    createFloatingPanel() {
        const panel = document.createElement('div');
        panel.id = 'comparisonFloatingPanel';
        panel.className = 'comparison-floating-panel';
        panel.innerHTML = `
            <div class="d-flex align-items-center gap-3">
                <div class="d-flex align-items-center gap-2">
                    <i class="bi bi-bar-chart-line fs-4"></i>
                    <span class="fw-semibold">Сравнение:</span>
                    <span class="badge bg-primary comparison-counter">${this.selectedTournaments.size}</span>
                </div>
                <button class="btn btn-sm btn-primary" id="showComparisonBtn">
                    <i class="bi bi-eye"></i> Сравнить
                </button>
                <button class="btn btn-sm btn-outline-danger" id="clearComparisonBtn">
                    <i class="bi bi-x-circle"></i>
                </button>
            </div>
        `;
        
        return panel;
    }

    /**
     * Очистка всех турниров
     */
    clearAll() {
        this.selectedTournaments.clear();
        this.tournamentsData.clear();
        this.saveToStorage();
        this.updateUI();
        this.showToast('Сравнение очищено', 'info');
    }

    /**
     * Показать уведомление
     */
    showToast(message, type = 'info') {
        if (typeof showToast === 'function') {
            showToast(message, type);
            return;
        }
        
        const toast = document.createElement('div');
        toast.className = `alert alert-${type} alert-dismissible fade show position-fixed`;
        toast.style.cssText = 'top: 20px; right: 20px; z-index: 9999; min-width: 300px;';
        toast.innerHTML = `
            ${message}
            <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
        `;
        document.body.appendChild(toast);
        
        setTimeout(() => toast.remove(), 3000);
    }
}

// CSS для плавающей панели
const style = document.createElement('style');
style.textContent = `
    .comparison-floating-panel {
        position: fixed;
        bottom: 2rem;
        right: 2rem;
        background: white;
        padding: 1rem 1.5rem;
        border-radius: 1rem;
        box-shadow: 0 10px 40px rgba(0, 0, 0, 0.15);
        z-index: 1000;
        animation: slideInUp 0.3s ease;
    }
    
    @keyframes slideInUp {
        from {
            transform: translateY(100%);
            opacity: 0;
        }
        to {
            transform: translateY(0);
            opacity: 1;
        }
    }
    
    .comparison-table th {
        background: #f8f9fa;
        font-weight: 600;
    }
    
    .comparison-table td {
        vertical-align: middle;
    }
    
    [data-action="compare"].active {
        background: #10b981;
        color: white;
        border-color: #10b981;
    }
`;
document.head.appendChild(style);

// Инициализация при загрузке страницы
document.addEventListener('DOMContentLoaded', () => {
    window.tournamentComparison = new TournamentComparison({
        maxCompare: 3
    });
});

// Экспорт для использования в других модулях
if (typeof module !== 'undefined' && module.exports) {
    module.exports = TournamentComparison;
}
