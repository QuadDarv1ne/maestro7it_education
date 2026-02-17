/**
 * Tournament Export System
 * Экспорт турниров в различные форматы (PDF, CSV, JSON, iCal)
 */

class TournamentExport {
    constructor() {
        this.init();
    }

    init() {
        this.attachEventListeners();
    }

    /**
     * Прикрепить обработчики событий
     */
    attachEventListeners() {
        // Кнопка экспорта
        document.addEventListener('click', (e) => {
            const exportBtn = e.target.closest('[data-action="export"]');
            if (exportBtn) {
                e.preventDefault();
                e.stopPropagation();
                const tournamentId = parseInt(exportBtn.dataset.tournamentId);
                this.showExportMenu(tournamentId, exportBtn);
            }
        });

        // Массовый экспорт
        document.addEventListener('click', (e) => {
            const bulkExportBtn = e.target.closest('[data-action="bulk-export"]');
            if (bulkExportBtn) {
                e.preventDefault();
                this.showBulkExportMenu(bulkExportBtn);
            }
        });
    }

    /**
     * Показать меню экспорта
     */
    showExportMenu(tournamentId, button) {
        const menuHTML = `
            <div class="export-menu">
                <div class="export-menu-header">
                    <span>Экспорт турнира</span>
                    <button class="btn-close-sm" onclick="this.closest('.export-menu').remove()">
                        <i class="bi bi-x"></i>
                    </button>
                </div>
                <div class="export-menu-list">
                    <button class="export-menu-item" onclick="window.tournamentExport.exportTournament(${tournamentId}, 'pdf')">
                        <i class="bi bi-file-pdf"></i>
                        <span>PDF документ</span>
                    </button>
                    <button class="export-menu-item" onclick="window.tournamentExport.exportTournament(${tournamentId}, 'csv')">
                        <i class="bi bi-file-spreadsheet"></i>
                        <span>CSV таблица</span>
                    </button>
                    <button class="export-menu-item" onclick="window.tournamentExport.exportTournament(${tournamentId}, 'json')">
                        <i class="bi bi-file-code"></i>
                        <span>JSON данные</span>
                    </button>
                    <button class="export-menu-item" onclick="window.tournamentExport.exportTournament(${tournamentId}, 'ical')">
                        <i class="bi bi-calendar-plus"></i>
                        <span>iCal календарь</span>
                    </button>
                    <button class="export-menu-item" onclick="window.tournamentExport.printTournament(${tournamentId})">
                        <i class="bi bi-printer"></i>
                        <span>Печать</span>
                    </button>
                </div>
            </div>
        `;

        // Удалить существующее меню
        document.querySelectorAll('.export-menu').forEach(el => el.remove());

        // Добавить новое
        button.insertAdjacentHTML('afterend', menuHTML);

        // Позиционирование
        const menu = button.nextElementSibling;
        const rect = button.getBoundingClientRect();
        menu.style.top = `${rect.bottom + 5}px`;
        menu.style.left = `${rect.left}px`;

        // Закрыть при клике вне
        setTimeout(() => {
            document.addEventListener('click', function closeMenu(e) {
                if (!e.target.closest('.export-menu') && !e.target.closest('[data-action="export"]')) {
                    menu.remove();
                    document.removeEventListener('click', closeMenu);
                }
            });
        }, 100);
    }

    /**
     * Показать меню массового экспорта
     */
    showBulkExportMenu(button) {
        const menuHTML = `
            <div class="export-menu">
                <div class="export-menu-header">
                    <span>Массовый экспорт</span>
                    <button class="btn-close-sm" onclick="this.closest('.export-menu').remove()">
                        <i class="bi bi-x"></i>
                    </button>
                </div>
                <div class="export-menu-list">
                    <button class="export-menu-item" onclick="window.tournamentExport.bulkExport('pdf')">
                        <i class="bi bi-file-pdf"></i>
                        <span>Все в PDF</span>
                    </button>
                    <button class="export-menu-item" onclick="window.tournamentExport.bulkExport('csv')">
                        <i class="bi bi-file-spreadsheet"></i>
                        <span>Все в CSV</span>
                    </button>
                    <button class="export-menu-item" onclick="window.tournamentExport.bulkExport('json')">
                        <i class="bi bi-file-code"></i>
                        <span>Все в JSON</span>
                    </button>
                    <button class="export-menu-item" onclick="window.tournamentExport.bulkExport('ical')">
                        <i class="bi bi-calendar-plus"></i>
                        <span>Все в iCal</span>
                    </button>
                </div>
            </div>
        `;

        document.querySelectorAll('.export-menu').forEach(el => el.remove());
        button.insertAdjacentHTML('afterend', menuHTML);

        const menu = button.nextElementSibling;
        const rect = button.getBoundingClientRect();
        menu.style.top = `${rect.bottom + 5}px`;
        menu.style.left = `${rect.left}px`;

        setTimeout(() => {
            document.addEventListener('click', function closeMenu(e) {
                if (!e.target.closest('.export-menu') && !e.target.closest('[data-action="bulk-export"]')) {
                    menu.remove();
                    document.removeEventListener('click', closeMenu);
                }
            });
        }, 100);
    }

    /**
     * Экспорт турнира
     */
    async exportTournament(tournamentId, format) {
        try {
            // Закрыть меню
            document.querySelectorAll('.export-menu').forEach(el => el.remove());

            // Показать загрузку
            if (window.notificationSystem) {
                window.notificationSystem.show(`Экспорт в ${format.toUpperCase()}...`, 'info');
            }

            if (format === 'ical') {
                // iCal экспорт через API
                window.location.href = `/api/tournaments/${tournamentId}/export/ical`;
            } else if (format === 'pdf') {
                await this.exportToPDF(tournamentId);
            } else if (format === 'csv') {
                await this.exportToCSV(tournamentId);
            } else if (format === 'json') {
                await this.exportToJSON(tournamentId);
            }

            // Отследить
            if (window.analyticsTracker) {
                window.analyticsTracker.track('tournament_export', { 
                    tournament_id: tournamentId, 
                    format: format 
                });
            }

            if (window.notificationSystem) {
                window.notificationSystem.show('Экспорт завершен', 'success');
            }
        } catch (error) {
            console.error('Export error:', error);
            if (window.notificationSystem) {
                window.notificationSystem.show('Ошибка экспорта', 'error');
            }
        }
    }

    /**
     * Экспорт в PDF
     */
    async exportToPDF(tournamentId) {
        const tournament = await this.fetchTournament(tournamentId);
        
        // Создать HTML для печати
        const printWindow = window.open('', '_blank');
        printWindow.document.write(this.generatePrintHTML(tournament));
        printWindow.document.close();
        
        // Печать
        setTimeout(() => {
            printWindow.print();
        }, 500);
    }

    /**
     * Экспорт в CSV
     */
    async exportToCSV(tournamentId) {
        const tournament = await this.fetchTournament(tournamentId);
        
        const csv = [
            ['Поле', 'Значение'],
            ['ID', tournament.id],
            ['Название', tournament.name],
            ['Локация', tournament.location],
            ['Дата начала', tournament.start_date],
            ['Дата окончания', tournament.end_date],
            ['Категория', tournament.category],
            ['Статус', tournament.status],
            ['Организатор', tournament.organizer || ''],
            ['Призовой фонд', tournament.prize_fund || ''],
            ['Описание', tournament.description || '']
        ].map(row => row.map(cell => `"${cell}"`).join(',')).join('\n');

        this.downloadFile(csv, `tournament_${tournamentId}.csv`, 'text/csv');
    }

    /**
     * Экспорт в JSON
     */
    async exportToJSON(tournamentId) {
        const tournament = await this.fetchTournament(tournamentId);
        const json = JSON.stringify(tournament, null, 2);
        this.downloadFile(json, `tournament_${tournamentId}.json`, 'application/json');
    }

    /**
     * Массовый экспорт
     */
    async bulkExport(format) {
        try {
            document.querySelectorAll('.export-menu').forEach(el => el.remove());

            if (window.notificationSystem) {
                window.notificationSystem.show(`Массовый экспорт в ${format.toUpperCase()}...`, 'info');
            }

            // Получить все видимые турниры
            const tournamentCards = document.querySelectorAll('.tournament-card[data-tournament-id]');
            const tournamentIds = Array.from(tournamentCards).map(card => 
                parseInt(card.dataset.tournamentId)
            );

            if (tournamentIds.length === 0) {
                if (window.notificationSystem) {
                    window.notificationSystem.show('Нет турниров для экспорта', 'warning');
                }
                return;
            }

            if (format === 'ical') {
                // Экспорт всех в iCal
                window.location.href = '/api/tournaments/export/ical';
            } else if (format === 'csv') {
                await this.bulkExportToCSV(tournamentIds);
            } else if (format === 'json') {
                await this.bulkExportToJSON(tournamentIds);
            } else if (format === 'pdf') {
                await this.bulkExportToPDF(tournamentIds);
            }

            if (window.notificationSystem) {
                window.notificationSystem.show(`Экспортировано ${tournamentIds.length} турниров`, 'success');
            }
        } catch (error) {
            console.error('Bulk export error:', error);
            if (window.notificationSystem) {
                window.notificationSystem.show('Ошибка массового экспорта', 'error');
            }
        }
    }

    /**
     * Массовый экспорт в CSV
     */
    async bulkExportToCSV(tournamentIds) {
        const tournaments = await Promise.all(
            tournamentIds.map(id => this.fetchTournament(id))
        );

        const csv = [
            ['ID', 'Название', 'Локация', 'Дата начала', 'Дата окончания', 'Категория', 'Статус', 'Организатор', 'Призовой фонд'],
            ...tournaments.map(t => [
                t.id,
                t.name,
                t.location,
                t.start_date,
                t.end_date,
                t.category,
                t.status,
                t.organizer || '',
                t.prize_fund || ''
            ])
        ].map(row => row.map(cell => `"${cell}"`).join(',')).join('\n');

        this.downloadFile(csv, 'tournaments.csv', 'text/csv');
    }

    /**
     * Массовый экспорт в JSON
     */
    async bulkExportToJSON(tournamentIds) {
        const tournaments = await Promise.all(
            tournamentIds.map(id => this.fetchTournament(id))
        );

        const json = JSON.stringify(tournaments, null, 2);
        this.downloadFile(json, 'tournaments.json', 'application/json');
    }

    /**
     * Массовый экспорт в PDF
     */
    async bulkExportToPDF(tournamentIds) {
        const tournaments = await Promise.all(
            tournamentIds.map(id => this.fetchTournament(id))
        );

        const printWindow = window.open('', '_blank');
        printWindow.document.write(this.generateBulkPrintHTML(tournaments));
        printWindow.document.close();

        setTimeout(() => {
            printWindow.print();
        }, 500);
    }

    /**
     * Печать турнира
     */
    async printTournament(tournamentId) {
        document.querySelectorAll('.export-menu').forEach(el => el.remove());
        await this.exportToPDF(tournamentId);
    }

    /**
     * Получить данные турнира
     */
    async fetchTournament(tournamentId) {
        const response = await fetch(`/api/tournaments/${tournamentId}`);
        if (!response.ok) throw new Error('Failed to fetch tournament');
        return await response.json();
    }

    /**
     * Скачать файл
     */
    downloadFile(content, filename, mimeType) {
        const blob = new Blob([content], { type: mimeType });
        const url = URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = filename;
        a.click();
        URL.revokeObjectURL(url);
    }

    /**
     * Генерация HTML для печати
     */
    generatePrintHTML(tournament) {
        return `
            <!DOCTYPE html>
            <html>
            <head>
                <meta charset="UTF-8">
                <title>${tournament.name}</title>
                <style>
                    body { font-family: Arial, sans-serif; padding: 20px; }
                    h1 { color: #2563eb; }
                    .info { margin: 10px 0; }
                    .label { font-weight: bold; }
                    @media print {
                        body { padding: 0; }
                    }
                </style>
            </head>
            <body>
                <h1>${tournament.name}</h1>
                <div class="info"><span class="label">Локация:</span> ${tournament.location}</div>
                <div class="info"><span class="label">Дата:</span> ${tournament.start_date} - ${tournament.end_date}</div>
                <div class="info"><span class="label">Категория:</span> ${tournament.category}</div>
                <div class="info"><span class="label">Статус:</span> ${tournament.status}</div>
                ${tournament.organizer ? `<div class="info"><span class="label">Организатор:</span> ${tournament.organizer}</div>` : ''}
                ${tournament.prize_fund ? `<div class="info"><span class="label">Призовой фонд:</span> ${tournament.prize_fund}</div>` : ''}
                ${tournament.description ? `<div class="info"><span class="label">Описание:</span><br>${tournament.description}</div>` : ''}
            </body>
            </html>
        `;
    }

    /**
     * Генерация HTML для массовой печати
     */
    generateBulkPrintHTML(tournaments) {
        const items = tournaments.map(t => `
            <div class="tournament-item">
                <h2>${t.name}</h2>
                <div class="info"><span class="label">Локация:</span> ${t.location}</div>
                <div class="info"><span class="label">Дата:</span> ${t.start_date} - ${t.end_date}</div>
                <div class="info"><span class="label">Категория:</span> ${t.category}</div>
            </div>
        `).join('');

        return `
            <!DOCTYPE html>
            <html>
            <head>
                <meta charset="UTF-8">
                <title>Турниры</title>
                <style>
                    body { font-family: Arial, sans-serif; padding: 20px; }
                    h1 { color: #2563eb; }
                    .tournament-item { margin-bottom: 30px; page-break-inside: avoid; }
                    .info { margin: 5px 0; }
                    .label { font-weight: bold; }
                    @media print {
                        body { padding: 0; }
                    }
                </style>
            </head>
            <body>
                <h1>Список турниров</h1>
                ${items}
            </body>
            </html>
        `;
    }
}

// CSS стили
const style = document.createElement('style');
style.textContent = `
    .export-menu {
        position: fixed;
        background: var(--bg-primary);
        border: 1px solid var(--border-color);
        border-radius: 12px;
        box-shadow: 0 8px 24px rgba(0, 0, 0, 0.15);
        z-index: 1000;
        min-width: 220px;
        animation: exportMenuIn 0.2s ease;
    }

    @keyframes exportMenuIn {
        from {
            opacity: 0;
            transform: scale(0.95) translateY(-5px);
        }
        to {
            opacity: 1;
            transform: scale(1) translateY(0);
        }
    }

    .export-menu-header {
        display: flex;
        align-items: center;
        justify-content: space-between;
        padding: 0.75rem 1rem;
        border-bottom: 1px solid var(--border-color);
        font-weight: 600;
        font-size: 0.875rem;
    }

    .export-menu-list {
        padding: 0.5rem;
    }

    .export-menu-item {
        display: flex;
        align-items: center;
        gap: 0.75rem;
        width: 100%;
        padding: 0.75rem;
        border: none;
        border-radius: 8px;
        background: transparent;
        color: var(--text-primary);
        cursor: pointer;
        transition: all 0.2s ease;
        font-size: 0.875rem;
    }

    .export-menu-item:hover {
        background: var(--bg-secondary);
        transform: translateX(4px);
    }

    .export-menu-item i {
        font-size: 1.25rem;
        color: var(--primary-color);
    }
`;
document.head.appendChild(style);

// Инициализация
document.addEventListener('DOMContentLoaded', () => {
    window.tournamentExport = new TournamentExport();
    console.log('[Tournament Export] Initialized');
});

// Экспорт
if (typeof module !== 'undefined' && module.exports) {
    module.exports = TournamentExport;
}
