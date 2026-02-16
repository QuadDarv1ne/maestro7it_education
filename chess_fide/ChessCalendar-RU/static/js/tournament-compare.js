// Tournament Comparison System - детальное сравнение турниров

class TournamentCompare {
    constructor() {
        this.selectedTournaments = [];
        this.maxCompare = 4;
        this.storageKey = 'compare_tournaments';
        this.init();
    }

    init() {
        this.loadSelected();
        this.createCompareWidget();
        this.attachEventListeners();
        this.updateBadge();
    }

    loadSelected() {
        const stored = localStorage.getItem(this.storageKey);
        this.selectedTournaments = stored ? JSON.parse(stored) : [];
    }

    saveSelected() {
        localStorage.setItem(this.storageKey, JSON.stringify(this.selectedTournaments));
    }

    createCompareWidget() {
        // Проверяем, не создан ли уже виджет
        if (document.getElementById('compareWidget')) return;

        const widget = document.createElement('div');
        widget.id = 'compareWidget';
        widget.innerHTML = `
            <style>
                #compareWidget {
                    position: fixed;
                    bottom: 30px;
                    left: 30px;
                    z-index: 998;
                }
                
                .compare-fab {
                    width: 60px;
                    height: 60px;
                    border-radius: 50%;
                    background: linear-gradient(135deg, #10b981 0%, #059669 100%);
                    color: white;
                    border: none;
                    box-shadow: 0 4px 12px rgba(16, 185, 129, 0.4);
                    cursor: pointer;
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    font-size: 24px;
                    transition: all 0.3s ease;
                    position: relative;
                }
                
                .compare-fab:hover {
                    transform: scale(1.1);
                    box-shadow: 0 6px 20px rgba(16, 185, 129, 0.6);
                }
                
                .compare-badge {
                    position: absolute;
                    top: -5px;
                    right: -5px;
                    background: #ef4444;
                    color: white;
                    border-radius: 50%;
                    width: 24px;
                    height: 24px;
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    font-size: 0.75rem;
                    font-weight: 700;
                    display: none;
                }
                
                .compare-badge.visible {
                    display: flex;
                }
                
                @media (max-width: 576px) {
                    #compareWidget {
                        bottom: 90px;
                        left: 15px;
                    }
                    
                    .compare-fab {
                        width: 50px;
                        height: 50px;
                        font-size: 20px;
                    }
                }
            </style>
            
            <button class="compare-fab" onclick="tournamentCompare.openModal()" title="Сравнить турниры">
                <i class="bi bi-arrow-left-right"></i>
                <span class="compare-badge" id="compareBadge">0</span>
            </button>
        `;

        document.body.appendChild(widget);
        
        // Добавляем чекбоксы на карточки турниров
        this.addCheckboxesToCards();
    }

    addCheckboxesToCards() {
        const cards = document.querySelectorAll('.tournament-card');
        
        cards.forEach(card => {
            // Проверяем, не добавлен ли уже чекбокс
            if (card.querySelector('.compare-checkbox')) return;
            
            const link = card.querySelector('a[href*="/tournament/"]');
            if (!link) return;
            
            const match = link.href.match(/\/tournament\/(\d+)/);
            if (!match) return;
            
            const tournamentId = parseInt(match[1]);
            
            // Создаём чекбокс
            const checkbox = document.createElement('div');
            checkbox.className = 'compare-checkbox';
            checkbox.innerHTML = `
                <style>
                    .compare-checkbox {
                        position: absolute;
                        top: 10px;
                        right: 10px;
                        z-index: 10;
                    }
                    
                    .compare-checkbox input[type="checkbox"] {
                        width: 20px;
                        height: 20px;
                        cursor: pointer;
                        accent-color: var(--success-color);
                    }
                    
                    .compare-checkbox label {
                        display: flex;
                        align-items: center;
                        gap: 0.5rem;
                        background: rgba(255, 255, 255, 0.95);
                        padding: 0.5rem 0.75rem;
                        border-radius: 20px;
                        cursor: pointer;
                        font-size: 0.875rem;
                        font-weight: 600;
                        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
                        transition: all 0.2s ease;
                    }
                    
                    [data-theme="dark"] .compare-checkbox label {
                        background: rgba(30, 41, 59, 0.95);
                        color: var(--text-primary);
                    }
                    
                    .compare-checkbox label:hover {
                        transform: scale(1.05);
                        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
                    }
                    
                    .compare-checkbox input:checked + label {
                        background: var(--success-color);
                        color: white;
                    }
                </style>
                
                <input type="checkbox" id="compare_${tournamentId}" 
                       data-tournament-id="${tournamentId}"
                       ${this.isSelected(tournamentId) ? 'checked' : ''}>
                <label for="compare_${tournamentId}">
                    <i class="bi bi-check-circle"></i>
                    Сравнить
                </label>
            `;
            
            // Делаем карточку относительно позиционированной
            card.style.position = 'relative';
            card.appendChild(checkbox);
            
            // Обработчик изменения чекбокса
            const input = checkbox.querySelector('input');
            input.addEventListener('change', (e) => {
                e.stopPropagation();
                this.toggleTournament(tournamentId, card);
            });
        });
    }

    isSelected(tournamentId) {
        return this.selectedTournaments.some(t => t.id === tournamentId);
    }

    toggleTournament(tournamentId, cardElement) {
        const index = this.selectedTournaments.findIndex(t => t.id === tournamentId);
        
        if (index > -1) {
            // Удаляем
            this.selectedTournaments.splice(index, 1);
        } else {
            // Проверяем лимит
            if (this.selectedTournaments.length >= this.maxCompare) {
                if (window.toast) {
                    window.toast.warning(`Можно сравнить максимум ${this.maxCompare} турнира`);
                }
                
                // Снимаем галочку
                const checkbox = cardElement.querySelector('input[type="checkbox"]');
                if (checkbox) checkbox.checked = false;
                
                return;
            }
            
            // Добавляем
            const tournament = this.extractTournamentData(cardElement);
            tournament.id = tournamentId;
            this.selectedTournaments.push(tournament);
        }
        
        this.saveSelected();
        this.updateBadge();
        
        // Track achievement
        if (window.achievementsSystem && this.selectedTournaments.length >= 2) {
            window.achievementsSystem.trackAction('comparison_used');
        }
    }

    extractTournamentData(cardElement) {
        const titleElement = cardElement.querySelector('.card-title');
        const locationElement = cardElement.querySelector('[class*="geo-alt"]')?.parentElement;
        const dateElement = cardElement.querySelector('[class*="calendar"]')?.parentElement;
        const categoryBadge = cardElement.querySelector('.tournament-badge');
        const statusBadge = cardElement.querySelector('.badge');
        const prizeElement = cardElement.querySelector('[class*="cash-coin"]')?.parentElement;
        const organizerElement = cardElement.querySelector('[class*="building"]')?.parentElement;
        
        return {
            name: titleElement?.textContent.trim() || 'Неизвестно',
            location: locationElement?.textContent.trim() || 'Не указано',
            dates: dateElement?.textContent.trim() || 'Не указано',
            category: categoryBadge?.textContent.trim() || 'Общий',
            status: statusBadge?.textContent.trim() || 'Неизвестно',
            prize: prizeElement?.textContent.replace('Призовой фонд:', '').trim() || 'Не указан',
            organizer: organizerElement?.textContent.replace('Организатор:', '').trim() || 'Не указан'
        };
    }

    updateBadge() {
        const badge = document.getElementById('compareBadge');
        if (badge) {
            badge.textContent = this.selectedTournaments.length;
            if (this.selectedTournaments.length > 0) {
                badge.classList.add('visible');
            } else {
                badge.classList.remove('visible');
            }
        }
    }

    openModal() {
        if (this.selectedTournaments.length < 2) {
            if (window.toast) {
                window.toast.info('Выберите минимум 2 турнира для сравнения');
            }
            return;
        }
        
        this.createComparisonModal();
    }

    createComparisonModal() {
        // Удаляем старую модалку если есть
        const oldModal = document.getElementById('comparisonModal');
        if (oldModal) oldModal.remove();
        
        const modal = document.createElement('div');
        modal.id = 'comparisonModal';
        modal.className = 'modal fade';
        modal.innerHTML = `
            <div class="modal-dialog modal-xl modal-dialog-scrollable">
                <div class="modal-content">
                    <div class="modal-header">
                        <h5 class="modal-title">
                            <i class="bi bi-arrow-left-right"></i> 
                            Сравнение турниров (${this.selectedTournaments.length})
                        </h5>
                        <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
                    </div>
                    <div class="modal-body">
                        ${this.renderComparison()}
                    </div>
                    <div class="modal-footer">
                        <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">
                            Закрыть
                        </button>
                        <button type="button" class="btn btn-danger" onclick="tournamentCompare.clearAll()">
                            <i class="bi bi-trash"></i> Очистить выбор
                        </button>
                        <button type="button" class="btn btn-primary" onclick="tournamentCompare.exportComparison()">
                            <i class="bi bi-download"></i> Экспорт
                        </button>
                    </div>
                </div>
            </div>
        `;
        
        document.body.appendChild(modal);
        
        const bsModal = new bootstrap.Modal(modal);
        bsModal.show();
        
        modal.addEventListener('hidden.bs.modal', () => modal.remove());
    }

    renderComparison() {
        const fields = [
            { key: 'name', label: 'Название', icon: 'trophy' },
            { key: 'location', label: 'Место проведения', icon: 'geo-alt' },
            { key: 'dates', label: 'Даты', icon: 'calendar' },
            { key: 'category', label: 'Категория', icon: 'tag' },
            { key: 'status', label: 'Статус', icon: 'info-circle' },
            { key: 'prize', label: 'Призовой фонд', icon: 'cash-coin' },
            { key: 'organizer', label: 'Организатор', icon: 'building' }
        ];
        
        let html = '<div class="table-responsive"><table class="table table-bordered table-hover">';
        html += '<thead class="table-light"><tr><th style="width: 200px;">Параметр</th>';
        
        this.selectedTournaments.forEach((t, index) => {
            html += `<th>Турнир ${index + 1}</th>`;
        });
        
        html += '</tr></thead><tbody>';
        
        fields.forEach(field => {
            html += '<tr>';
            html += `<td class="fw-bold"><i class="bi bi-${field.icon}"></i> ${field.label}</td>`;
            
            this.selectedTournaments.forEach(tournament => {
                const value = tournament[field.key];
                html += `<td>${this.escapeHtml(value)}</td>`;
            });
            
            html += '</tr>';
        });
        
        html += '</tbody></table></div>';
        
        // Добавляем визуальное сравнение
        html += this.renderVisualComparison();
        
        return html;
    }

    renderVisualComparison() {
        let html = '<div class="mt-4"><h6 class="mb-3"><i class="bi bi-bar-chart"></i> Визуальное сравнение</h6>';
        html += '<div class="row g-3">';
        
        this.selectedTournaments.forEach((tournament, index) => {
            html += `
                <div class="col-md-${12 / this.selectedTournaments.length}">
                    <div class="card h-100">
                        <div class="card-body">
                            <h6 class="card-title">Турнир ${index + 1}</h6>
                            <div class="mb-2">
                                <small class="text-muted">Категория</small>
                                <div class="progress" style="height: 25px;">
                                    <div class="progress-bar ${this.getCategoryColor(tournament.category)}" 
                                         style="width: 100%">
                                        ${tournament.category}
                                    </div>
                                </div>
                            </div>
                            <div class="mb-2">
                                <small class="text-muted">Статус</small>
                                <div class="progress" style="height: 25px;">
                                    <div class="progress-bar ${this.getStatusColor(tournament.status)}" 
                                         style="width: 100%">
                                        ${tournament.status}
                                    </div>
                                </div>
                            </div>
                            <div class="mt-3">
                                <a href="/tournament/${tournament.id}" class="btn btn-sm btn-primary w-100" target="_blank">
                                    <i class="bi bi-eye"></i> Открыть
                                </a>
                            </div>
                        </div>
                    </div>
                </div>
            `;
        });
        
        html += '</div></div>';
        return html;
    }

    getCategoryColor(category) {
        if (category.includes('International') || category.includes('World')) return 'bg-primary';
        if (category.includes('National')) return 'bg-success';
        return 'bg-secondary';
    }

    getStatusColor(status) {
        if (status.includes('Completed')) return 'bg-success';
        if (status.includes('Ongoing')) return 'bg-warning';
        return 'bg-info';
    }

    clearAll() {
        if (confirm('Очистить весь список сравнения?')) {
            this.selectedTournaments = [];
            this.saveSelected();
            this.updateBadge();
            
            // Снимаем все галочки
            document.querySelectorAll('.compare-checkbox input[type="checkbox"]').forEach(cb => {
                cb.checked = false;
            });
            
            // Закрываем модалку
            const modal = bootstrap.Modal.getInstance(document.getElementById('comparisonModal'));
            if (modal) modal.hide();
            
            if (window.toast) {
                window.toast.success('Список сравнения очищен');
            }
        }
    }

    exportComparison() {
        const data = this.selectedTournaments.map((t, index) => ({
            'Номер': index + 1,
            'Название': t.name,
            'Место': t.location,
            'Даты': t.dates,
            'Категория': t.category,
            'Статус': t.status,
            'Призовой фонд': t.prize,
            'Организатор': t.organizer
        }));
        
        // Конвертируем в CSV
        const csv = this.convertToCSV(data);
        
        // Скачиваем
        const blob = new Blob([csv], { type: 'text/csv;charset=utf-8;' });
        const link = document.createElement('a');
        link.href = URL.createObjectURL(blob);
        link.download = `tournament_comparison_${new Date().toISOString().split('T')[0]}.csv`;
        link.click();
        
        if (window.toast) {
            window.toast.success('Сравнение экспортировано');
        }
    }

    convertToCSV(data) {
        if (data.length === 0) return '';
        
        const headers = Object.keys(data[0]);
        const rows = data.map(row => 
            headers.map(header => `"${row[header]}"`).join(',')
        );
        
        return [headers.join(','), ...rows].join('\n');
    }

    escapeHtml(text) {
        const div = document.createElement('div');
        div.textContent = text;
        return div.innerHTML;
    }

    attachEventListeners() {
        // Обновляем чекбоксы при изменении DOM
        const observer = new MutationObserver(() => {
            this.addCheckboxesToCards();
        });
        
        observer.observe(document.body, {
            childList: true,
            subtree: true
        });
    }
}

// Инициализация
if (window.location.pathname === '/' || window.location.pathname.includes('/tournament')) {
    const tournamentCompare = new TournamentCompare();
    window.tournamentCompare = tournamentCompare;
}
