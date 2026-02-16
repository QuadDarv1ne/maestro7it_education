// Quick Actions Menu - Floating Action Button with shortcuts

class QuickActions {
    constructor() {
        this.isOpen = false;
        this.init();
    }

    init() {
        this.createFAB();
        this.attachEventListeners();
    }

    createFAB() {
        // Check if already exists
        if (document.getElementById('quickActionsFAB')) return;

        const fab = document.createElement('div');
        fab.id = 'quickActionsFAB';
        fab.innerHTML = `
            <style>
                #quickActionsFAB {
                    position: fixed;
                    bottom: 30px;
                    right: 30px;
                    z-index: 999;
                }
                
                /* Adjust for mobile bottom nav */
                @media (max-width: 576px) {
                    #quickActionsFAB {
                        bottom: 90px;
                        right: 15px;
                    }
                }
                
                .fab-button {
                    width: 60px;
                    height: 60px;
                    border-radius: 50%;
                    background: linear-gradient(135deg, #2563eb 0%, #1e40af 100%);
                    color: white;
                    border: none;
                    box-shadow: 0 4px 12px rgba(37, 99, 235, 0.4);
                    cursor: pointer;
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    font-size: 24px;
                    transition: all 0.3s ease;
                }
                
                .fab-button:hover {
                    transform: scale(1.1);
                    box-shadow: 0 6px 20px rgba(37, 99, 235, 0.6);
                }
                
                .fab-button.active {
                    transform: rotate(45deg);
                }
                
                .fab-actions {
                    position: absolute;
                    bottom: 70px;
                    right: 0;
                    display: flex;
                    flex-direction: column;
                    gap: 10px;
                    opacity: 0;
                    pointer-events: none;
                    transition: all 0.3s ease;
                }
                
                .fab-actions.active {
                    opacity: 1;
                    pointer-events: all;
                    bottom: 80px;
                }
                
                .fab-action {
                    display: flex;
                    align-items: center;
                    gap: 10px;
                    background: white;
                    padding: 12px 20px;
                    border-radius: 30px;
                    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.15);
                    cursor: pointer;
                    transition: all 0.3s ease;
                    white-space: nowrap;
                    transform: translateX(100px);
                    opacity: 0;
                }
                
                .fab-actions.active .fab-action {
                    transform: translateX(0);
                    opacity: 1;
                }
                
                .fab-action:nth-child(1) { transition-delay: 0.05s; }
                .fab-action:nth-child(2) { transition-delay: 0.1s; }
                .fab-action:nth-child(3) { transition-delay: 0.15s; }
                .fab-action:nth-child(4) { transition-delay: 0.2s; }
                .fab-action:nth-child(5) { transition-delay: 0.25s; }
                
                .fab-action:hover {
                    transform: translateX(-5px);
                    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
                }
                
                .fab-action i {
                    font-size: 20px;
                    color: #2563eb;
                }
                
                .fab-action span {
                    font-weight: 500;
                    color: #1e293b;
                }
                
                @media (max-width: 768px) {
                    #quickActionsFAB {
                        right: 15px;
                    }
                    
                    .fab-button {
                        width: 50px;
                        height: 50px;
                        font-size: 20px;
                    }
                    
                    .fab-action {
                        padding: 10px 15px;
                        font-size: 14px;
                    }
                }
            </style>
            
            <div class="fab-actions" id="fabActions">
                <div class="fab-action" data-action="export">
                    <i class="bi bi-download"></i>
                    <span>Экспорт</span>
                </div>
                <div class="fab-action" data-action="filter">
                    <i class="bi bi-funnel"></i>
                    <span>Фильтры</span>
                </div>
                <div class="fab-action" data-action="calendar">
                    <i class="bi bi-calendar-plus"></i>
                    <span>В календарь</span>
                </div>
                <div class="fab-action" data-action="share">
                    <i class="bi bi-share"></i>
                    <span>Поделиться</span>
                </div>
                <div class="fab-action" data-action="top">
                    <i class="bi bi-arrow-up"></i>
                    <span>Наверх</span>
                </div>
            </div>
            
            <button class="fab-button" id="fabButton">
                <i class="bi bi-plus-lg"></i>
            </button>
        `;

        document.body.appendChild(fab);
    }

    attachEventListeners() {
        const fabButton = document.getElementById('fabButton');
        const fabActions = document.getElementById('fabActions');

        if (fabButton) {
            fabButton.addEventListener('click', () => this.toggle());
        }

        // Action handlers
        document.querySelectorAll('.fab-action').forEach(action => {
            action.addEventListener('click', (e) => {
                const actionType = e.currentTarget.dataset.action;
                this.handleAction(actionType);
                this.close();
            });
        });

        // Close on outside click
        document.addEventListener('click', (e) => {
            if (!e.target.closest('#quickActionsFAB')) {
                this.close();
            }
        });
    }

    toggle() {
        this.isOpen = !this.isOpen;
        const fabButton = document.getElementById('fabButton');
        const fabActions = document.getElementById('fabActions');

        if (this.isOpen) {
            fabButton.classList.add('active');
            fabActions.classList.add('active');
        } else {
            fabButton.classList.remove('active');
            fabActions.classList.remove('active');
        }
    }

    close() {
        this.isOpen = false;
        document.getElementById('fabButton')?.classList.remove('active');
        document.getElementById('fabActions')?.classList.remove('active');
    }

    handleAction(action) {
        switch (action) {
            case 'export':
                this.showExportMenu();
                break;
            case 'filter':
                this.toggleFilters();
                break;
            case 'calendar':
                this.addToCalendar();
                break;
            case 'share':
                this.shareCurrentPage();
                break;
            case 'top':
                this.scrollToTop();
                break;
        }
    }

    showExportMenu() {
        const modal = document.createElement('div');
        modal.className = 'modal fade';
        modal.innerHTML = `
            <div class="modal-dialog">
                <div class="modal-content">
                    <div class="modal-header">
                        <h5 class="modal-title"><i class="bi bi-download"></i> Экспорт данных</h5>
                        <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
                    </div>
                    <div class="modal-body">
                        <div class="d-grid gap-2">
                            <a href="/export/csv" class="btn btn-outline-primary">
                                <i class="bi bi-filetype-csv"></i> Экспорт в CSV
                            </a>
                            <a href="/export/json" class="btn btn-outline-primary">
                                <i class="bi bi-filetype-json"></i> Экспорт в JSON
                            </a>
                            <button class="btn btn-outline-primary" onclick="quickActions.exportToICS()">
                                <i class="bi bi-calendar"></i> Экспорт в ICS (календарь)
                            </button>
                        </div>
                    </div>
                </div>
            </div>
        `;
        document.body.appendChild(modal);
        const bsModal = new bootstrap.Modal(modal);
        bsModal.show();
        modal.addEventListener('hidden.bs.modal', () => modal.remove());
    }

    toggleFilters() {
        const filterSection = document.querySelector('.filter-section, .filters, #filters');
        if (filterSection) {
            filterSection.scrollIntoView({ behavior: 'smooth', block: 'start' });
            filterSection.classList.add('highlight');
            setTimeout(() => filterSection.classList.remove('highlight'), 2000);
        }
    }

    addToCalendar() {
        // Get current page tournaments
        const tournaments = this.getCurrentPageTournaments();
        
        if (tournaments.length === 0) {
            alert('Нет турниров для добавления в календарь');
            return;
        }

        const modal = document.createElement('div');
        modal.className = 'modal fade';
        modal.innerHTML = `
            <div class="modal-dialog">
                <div class="modal-content">
                    <div class="modal-header">
                        <h5 class="modal-title"><i class="bi bi-calendar-plus"></i> Добавить в календарь</h5>
                        <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
                    </div>
                    <div class="modal-body">
                        <p>Выберите сервис календаря:</p>
                        <div class="d-grid gap-2">
                            <button class="btn btn-outline-primary" onclick="quickActions.exportToGoogleCalendar()">
                                <i class="bi bi-google"></i> Google Calendar
                            </button>
                            <button class="btn btn-outline-primary" onclick="quickActions.exportToOutlook()">
                                <i class="bi bi-microsoft"></i> Outlook Calendar
                            </button>
                            <button class="btn btn-outline-primary" onclick="quickActions.exportToICS()">
                                <i class="bi bi-calendar"></i> Скачать ICS файл
                            </button>
                        </div>
                    </div>
                </div>
            </div>
        `;
        document.body.appendChild(modal);
        const bsModal = new bootstrap.Modal(modal);
        bsModal.show();
        modal.addEventListener('hidden.bs.modal', () => modal.remove());
    }

    getCurrentPageTournaments() {
        const tournaments = [];
        document.querySelectorAll('.tournament-card, .card').forEach(card => {
            const link = card.querySelector('a[href*="/tournament/"]');
            if (link) {
                const match = link.href.match(/\/tournament\/(\d+)/);
                if (match) {
                    tournaments.push({ id: parseInt(match[1]) });
                }
            }
        });
        return tournaments;
    }

    async exportToICS() {
        const tournaments = this.getCurrentPageTournaments();
        
        // Track achievement
        if (window.achievementsSystem) {
            window.achievementsSystem.trackAction('export_used');
        }
        
        if (window.toast) {
            window.toast.exportSuccess('ICS');
        }
        
        // Implementation would call the API endpoint
        window.location.href = '/export/ics';
    }

    async exportToGoogleCalendar() {
        if (window.toast) {
            window.toast.info('Функция экспорта в Google Calendar будет доступна в следующей версии');
        }
    }

    async exportToOutlook() {
        if (window.toast) {
            window.toast.info('Функция экспорта в Outlook Calendar будет доступна в следующей версии');
        }
    }

    async shareCurrentPage() {
        const shareData = {
            title: document.title,
            text: 'Шахматный календарь России',
            url: window.location.href
        };

        if (navigator.share) {
            try {
                await navigator.share(shareData);
                if (window.toast) {
                    window.toast.success('Ссылка успешно отправлена');
                }
            } catch (err) {
                if (err.name !== 'AbortError') {
                    this.fallbackShare();
                }
            }
        } else {
            this.fallbackShare();
        }
    }

    fallbackShare() {
        const url = window.location.href;
        navigator.clipboard.writeText(url).then(() => {
            if (window.toast) {
                window.toast.copied();
            } else {
                alert('Ссылка скопирована в буфер обмена!');
            }
        }).catch(() => {
            prompt('Скопируйте ссылку:', url);
        });
    }

    scrollToTop() {
        window.scrollTo({
            top: 0,
            behavior: 'smooth'
        });
    }
}

// Initialize
const quickActions = new QuickActions();
