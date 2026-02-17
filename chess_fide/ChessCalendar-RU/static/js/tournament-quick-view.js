/**
 * Tournament Quick View Modal
 * Быстрый просмотр турнира без перехода на страницу
 */

class TournamentQuickView {
    constructor() {
        this.modal = null;
        this.currentTournamentId = null;
        this.init();
    }

    init() {
        this.createModal();
        this.attachEventListeners();
    }

    /**
     * Создание модального окна
     */
    createModal() {
        const modalHTML = `
            <div class="modal fade" id="tournamentQuickViewModal" tabindex="-1" aria-hidden="true">
                <div class="modal-dialog modal-lg modal-dialog-centered modal-dialog-scrollable">
                    <div class="modal-content">
                        <div class="modal-header">
                            <h5 class="modal-title" id="quickViewTitle">Загрузка...</h5>
                            <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                        </div>
                        <div class="modal-body" id="quickViewBody">
                            <div class="text-center py-5">
                                <div class="spinner-border text-primary" role="status">
                                    <span class="visually-hidden">Загрузка...</span>
                                </div>
                            </div>
                        </div>
                        <div class="modal-footer">
                            <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Закрыть</button>
                            <a href="#" class="btn btn-primary" id="quickViewFullLink">
                                <i class="bi bi-box-arrow-up-right"></i>
                                Полная информация
                            </a>
                        </div>
                    </div>
                </div>
            </div>
        `;

        // Удаляем старое модальное окно если есть
        const existingModal = document.getElementById('tournamentQuickViewModal');
        if (existingModal) {
            existingModal.remove();
        }

        // Добавляем новое
        document.body.insertAdjacentHTML('beforeend', modalHTML);
        this.modal = new bootstrap.Modal(document.getElementById('tournamentQuickViewModal'));
    }

    /**
     * Прикрепить обработчики событий
     */
    attachEventListeners() {
        // Клик по карточке с Ctrl/Cmd для быстрого просмотра
        document.addEventListener('click', (e) => {
            if (e.ctrlKey || e.metaKey) {
                const card = e.target.closest('[data-tournament-id]');
                if (card && !e.target.closest('button, a')) {
                    e.preventDefault();
                    const tournamentId = parseInt(card.dataset.tournamentId);
                    this.show(tournamentId);
                }
            }
        });

        // Кнопка быстрого просмотра
        document.addEventListener('click', (e) => {
            const quickViewBtn = e.target.closest('[data-action="quick-view"]');
            if (quickViewBtn) {
                e.preventDefault();
                e.stopPropagation();
                const tournamentId = parseInt(quickViewBtn.dataset.tournamentId);
                this.show(tournamentId);
            }
        });
    }

    /**
     * Показать модальное окно
     */
    async show(tournamentId) {
        this.currentTournamentId = tournamentId;
        this.modal.show();

        // Загрузить данные
        await this.loadTournamentData(tournamentId);
    }

    /**
     * Загрузить данные турнира
     */
    async loadTournamentData(tournamentId) {
        try {
            const response = await fetch(`/api/tournaments/${tournamentId}`);
            if (!response.ok) throw new Error('Failed to load tournament');

            const tournament = await response.json();
            this.renderTournament(tournament);

            // Обновить ссылку на полную страницу
            document.getElementById('quickViewFullLink').href = `/tournament/${tournamentId}`;

            // Отследить просмотр
            if (window.analyticsTracker) {
                window.analyticsTracker.track('tournament_quick_view', { tournament_id: tournamentId });
            }
        } catch (error) {
            console.error('Error loading tournament:', error);
            this.showError();
        }
    }

    /**
     * Отрисовать данные турнира
     */
    renderTournament(tournament) {
        document.getElementById('quickViewTitle').textContent = tournament.name;

        const bodyHTML = `
            <div class="tournament-quick-view">
                <!-- Статус и категория -->
                <div class="d-flex gap-2 mb-3">
                    <span class="badge bg-${this.getStatusColor(tournament.status)} fs-6">
                        ${this.getStatusLabel(tournament.status)}
                    </span>
                    <span class="badge bg-secondary fs-6">${tournament.category}</span>
                    ${tournament.rating_type ? `<span class="badge bg-info fs-6">${tournament.rating_type}</span>` : ''}
                </div>

                <!-- Основная информация -->
                <div class="row g-3 mb-4">
                    <div class="col-md-6">
                        <div class="info-item">
                            <i class="bi bi-geo-alt text-primary"></i>
                            <div>
                                <small class="text-muted">Место проведения</small>
                                <div class="fw-semibold">${tournament.location}</div>
                            </div>
                        </div>
                    </div>
                    <div class="col-md-6">
                        <div class="info-item">
                            <i class="bi bi-calendar text-primary"></i>
                            <div>
                                <small class="text-muted">Даты</small>
                                <div class="fw-semibold">
                                    ${this.formatDate(tournament.start_date)} - ${this.formatDate(tournament.end_date)}
                                </div>
                            </div>
                        </div>
                    </div>
                    ${tournament.organizer ? `
                    <div class="col-md-6">
                        <div class="info-item">
                            <i class="bi bi-person text-primary"></i>
                            <div>
                                <small class="text-muted">Организатор</small>
                                <div class="fw-semibold">${tournament.organizer}</div>
                            </div>
                        </div>
                    </div>
                    ` : ''}
                    ${tournament.prize_fund ? `
                    <div class="col-md-6">
                        <div class="info-item">
                            <i class="bi bi-currency-dollar text-primary"></i>
                            <div>
                                <small class="text-muted">Призовой фонд</small>
                                <div class="fw-semibold">${tournament.prize_fund}</div>
                            </div>
                        </div>
                    </div>
                    ` : ''}
                    ${tournament.participants_count ? `
                    <div class="col-md-6">
                        <div class="info-item">
                            <i class="bi bi-people text-primary"></i>
                            <div>
                                <small class="text-muted">Участников</small>
                                <div class="fw-semibold">${tournament.participants_count}</div>
                            </div>
                        </div>
                    </div>
                    ` : ''}
                </div>

                <!-- Рейтинг -->
                ${tournament.average_rating > 0 ? `
                <div class="mb-4">
                    <div class="d-flex align-items-center gap-2 mb-2">
                        <span class="text-muted">Рейтинг:</span>
                        <div class="tournament-rating">
                            ${this.renderStars(tournament.average_rating)}
                            <span class="rating-value">${tournament.average_rating.toFixed(1)}</span>
                        </div>
                        <small class="text-muted">(${tournament.total_ratings} отзывов)</small>
                    </div>
                </div>
                ` : ''}

                <!-- Описание -->
                ${tournament.description ? `
                <div class="mb-4">
                    <h6 class="fw-semibold mb-2">Описание</h6>
                    <p class="text-muted">${tournament.description}</p>
                </div>
                ` : ''}

                <!-- Быстрые действия -->
                <div class="d-flex gap-2 flex-wrap">
                    <button class="btn btn-outline-danger btn-sm" onclick="window.tournamentCardManager?.handleFavoriteClick(this)" data-tournament-id="${tournament.id}">
                        <i class="bi bi-heart"></i>
                        В избранное
                    </button>
                    <button class="btn btn-outline-info btn-sm" onclick="window.tournamentCardManager?.handleCompareClick(this)" data-tournament-id="${tournament.id}">
                        <i class="bi bi-arrow-left-right"></i>
                        Сравнить
                    </button>
                    <button class="btn btn-outline-primary btn-sm" onclick="window.tournamentCardManager?.handleShareClick(this)" data-tournament-id="${tournament.id}">
                        <i class="bi bi-share"></i>
                        Поделиться
                    </button>
                    <button class="btn btn-outline-success btn-sm" onclick="window.tournamentCardManager?.handleExportClick(this)" data-tournament-id="${tournament.id}">
                        <i class="bi bi-download"></i>
                        Экспорт
                    </button>
                </div>
            </div>
        `;

        document.getElementById('quickViewBody').innerHTML = bodyHTML;
    }

    /**
     * Отрисовать звезды рейтинга
     */
    renderStars(rating) {
        const stars = [];
        for (let i = 1; i <= 5; i++) {
            if (i <= rating) {
                stars.push('<i class="bi bi-star-fill text-warning"></i>');
            } else if (i - 0.5 <= rating) {
                stars.push('<i class="bi bi-star-half text-warning"></i>');
            } else {
                stars.push('<i class="bi bi-star text-muted"></i>');
            }
        }
        return stars.join('');
    }

    /**
     * Получить цвет статуса
     */
    getStatusColor(status) {
        const colors = {
            'Scheduled': 'primary',
            'Ongoing': 'warning',
            'Completed': 'success',
            'Cancelled': 'danger'
        };
        return colors[status] || 'secondary';
    }

    /**
     * Получить метку статуса
     */
    getStatusLabel(status) {
        const labels = {
            'Scheduled': 'Запланирован',
            'Ongoing': 'Идет сейчас',
            'Completed': 'Завершен',
            'Cancelled': 'Отменен'
        };
        return labels[status] || status;
    }

    /**
     * Форматировать дату
     */
    formatDate(dateString) {
        if (!dateString) return 'Не указана';
        const date = new Date(dateString);
        return date.toLocaleDateString('ru-RU', { day: '2-digit', month: '2-digit', year: 'numeric' });
    }

    /**
     * Показать ошибку
     */
    showError() {
        document.getElementById('quickViewBody').innerHTML = `
            <div class="alert alert-danger" role="alert">
                <i class="bi bi-exclamation-triangle"></i>
                Не удалось загрузить данные турнира. Попробуйте позже.
            </div>
        `;
    }
}

// CSS стили
const style = document.createElement('style');
style.textContent = `
    .tournament-quick-view .info-item {
        display: flex;
        align-items: flex-start;
        gap: 0.75rem;
        padding: 0.75rem;
        background: var(--bg-secondary);
        border-radius: 8px;
    }

    .tournament-quick-view .info-item i {
        font-size: 1.25rem;
        margin-top: 0.25rem;
    }

    .tournament-quick-view .info-item > div {
        flex: 1;
    }

    .tournament-quick-view .tournament-rating {
        display: inline-flex;
        align-items: center;
        gap: 0.25rem;
    }

    .tournament-quick-view .rating-value {
        margin-left: 0.5rem;
        font-weight: 600;
        color: var(--text-primary);
    }

    #tournamentQuickViewModal .modal-content {
        border: none;
        box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
    }

    #tournamentQuickViewModal .modal-header {
        background: linear-gradient(135deg, var(--primary-color) 0%, #1e40af 100%);
        color: white;
        border-bottom: none;
    }

    #tournamentQuickViewModal .modal-header .btn-close {
        filter: brightness(0) invert(1);
    }

    #tournamentQuickViewModal .modal-footer {
        border-top: 1px solid var(--border-color);
        background: var(--bg-secondary);
    }

    /* Анимация появления */
    #tournamentQuickViewModal.show .modal-dialog {
        animation: slideInDown 0.3s ease-out;
    }

    @keyframes slideInDown {
        from {
            transform: translateY(-50px);
            opacity: 0;
        }
        to {
            transform: translateY(0);
            opacity: 1;
        }
    }
`;
document.head.appendChild(style);

// Инициализация
document.addEventListener('DOMContentLoaded', () => {
    window.tournamentQuickView = new TournamentQuickView();
    console.log('[Tournament Quick View] Initialized');
});

// Экспорт
if (typeof module !== 'undefined' && module.exports) {
    module.exports = TournamentQuickView;
}
