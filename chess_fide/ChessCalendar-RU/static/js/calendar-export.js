// Enhanced Calendar Export System
// Supports Google Calendar, Outlook, Apple Calendar, and ICS

class CalendarExport {
    constructor() {
        this.init();
    }

    init() {
        this.attachExportButtons();
    }

    attachExportButtons() {
        // Add export buttons to tournament detail pages
        document.addEventListener('DOMContentLoaded', () => {
            this.addExportButton();
        });
    }

    addExportButton() {
        const tournamentDetail = document.querySelector('.tournament-detail, .card-body');
        if (!tournamentDetail || document.getElementById('calendarExportBtn')) return;

        const button = document.createElement('div');
        button.id = 'calendarExportBtn';
        button.className = 'btn-group mt-3';
        button.innerHTML = `
            <button type="button" class="btn btn-primary dropdown-toggle" data-bs-toggle="dropdown">
                <i class="bi bi-calendar-plus"></i> Добавить в календарь
            </button>
            <ul class="dropdown-menu">
                <li><a class="dropdown-item" href="#" onclick="calendarExport.exportToGoogle(event)">
                    <i class="bi bi-google"></i> Google Calendar
                </a></li>
                <li><a class="dropdown-item" href="#" onclick="calendarExport.exportToOutlook(event)">
                    <i class="bi bi-microsoft"></i> Outlook
                </a></li>
                <li><a class="dropdown-item" href="#" onclick="calendarExport.exportToApple(event)">
                    <i class="bi bi-apple"></i> Apple Calendar
                </a></li>
                <li><hr class="dropdown-divider"></li>
                <li><a class="dropdown-item" href="#" onclick="calendarExport.downloadICS(event)">
                    <i class="bi bi-download"></i> Скачать ICS файл
                </a></li>
            </ul>
        `;

        tournamentDetail.appendChild(button);
    }

    getTournamentData() {
        // Extract tournament data from page
        const title = document.querySelector('h1, .tournament-title')?.textContent || 'Турнир';
        const location = document.querySelector('.tournament-location, [data-location]')?.textContent || '';
        const description = document.querySelector('.tournament-description, [data-description]')?.textContent || '';
        
        // Try to get dates from data attributes or text
        let startDate = document.querySelector('[data-start-date]')?.dataset.startDate;
        let endDate = document.querySelector('[data-end-date]')?.dataset.endDate;

        if (!startDate) {
            // Try to parse from text
            const dateText = document.querySelector('.tournament-dates')?.textContent;
            if (dateText) {
                const dates = this.parseDateRange(dateText);
                startDate = dates.start;
                endDate = dates.end;
            }
        }

        return {
            title: title.trim(),
            location: location.trim(),
            description: description.trim(),
            startDate: startDate || new Date().toISOString(),
            endDate: endDate || new Date().toISOString()
        };
    }

    parseDateRange(text) {
        // Simple date parsing (can be improved)
        const today = new Date();
        return {
            start: today.toISOString(),
            end: new Date(today.getTime() + 24 * 60 * 60 * 1000).toISOString()
        };
    }

    exportToGoogle(event) {
        event.preventDefault();
        const data = this.getTournamentData();

        const startDate = new Date(data.startDate);
        const endDate = new Date(data.endDate);

        const params = new URLSearchParams({
            action: 'TEMPLATE',
            text: data.title,
            dates: `${this.formatGoogleDate(startDate)}/${this.formatGoogleDate(endDate)}`,
            details: data.description,
            location: data.location,
            trp: 'false'
        });

        const url = `https://www.google.com/calendar/render?${params.toString()}`;
        window.open(url, '_blank');

        if (window.toast) {
            window.toast.success('Открыт Google Calendar');
        }

        if (window.achievementsSystem) {
            window.achievementsSystem.trackAction('export_used');
        }
    }

    exportToOutlook(event) {
        event.preventDefault();
        const data = this.getTournamentData();

        const startDate = new Date(data.startDate);
        const endDate = new Date(data.endDate);

        const params = new URLSearchParams({
            path: '/calendar/action/compose',
            rru: 'addevent',
            subject: data.title,
            startdt: startDate.toISOString(),
            enddt: endDate.toISOString(),
            location: data.location,
            body: data.description
        });

        const url = `https://outlook.live.com/calendar/0/deeplink/compose?${params.toString()}`;
        window.open(url, '_blank');

        if (window.toast) {
            window.toast.success('Открыт Outlook Calendar');
        }

        if (window.achievementsSystem) {
            window.achievementsSystem.trackAction('export_used');
        }
    }

    exportToApple(event) {
        event.preventDefault();
        // Apple Calendar uses ICS files
        this.downloadICS(event);
    }

    downloadICS(event) {
        event.preventDefault();
        const data = this.getTournamentData();

        const ics = this.generateICS(data);
        const blob = new Blob([ics], { type: 'text/calendar;charset=utf-8' });
        const link = document.createElement('a');
        link.href = URL.createObjectURL(blob);
        link.download = `${this.sanitizeFilename(data.title)}.ics`;
        link.click();

        if (window.toast) {
            window.toast.exportSuccess('ICS');
        }

        if (window.achievementsSystem) {
            window.achievementsSystem.trackAction('export_used');
        }
    }

    generateICS(data) {
        const startDate = new Date(data.startDate);
        const endDate = new Date(data.endDate);

        const ics = [
            'BEGIN:VCALENDAR',
            'VERSION:2.0',
            'PRODID:-//ChessCalendar-RU//NONSGML v1.0//EN',
            'CALSCALE:GREGORIAN',
            'METHOD:PUBLISH',
            'BEGIN:VEVENT',
            `UID:${this.generateUID()}@chesscalendar-ru.ru`,
            `DTSTART:${this.formatICSDate(startDate)}`,
            `DTEND:${this.formatICSDate(endDate)}`,
            `SUMMARY:${this.escapeICS(data.title)}`,
            `LOCATION:${this.escapeICS(data.location)}`,
            `DESCRIPTION:${this.escapeICS(data.description)}`,
            'STATUS:CONFIRMED',
            'SEQUENCE:0',
            'END:VEVENT',
            'END:VCALENDAR'
        ].join('\r\n');

        return ics;
    }

    formatGoogleDate(date) {
        return date.toISOString().replace(/[-:]/g, '').split('.')[0] + 'Z';
    }

    formatICSDate(date) {
        return date.toISOString().replace(/[-:]/g, '').split('.')[0] + 'Z';
    }

    escapeICS(text) {
        return text.replace(/\\/g, '\\\\')
                   .replace(/;/g, '\\;')
                   .replace(/,/g, '\\,')
                   .replace(/\n/g, '\\n');
    }

    sanitizeFilename(filename) {
        return filename.replace(/[^a-z0-9]/gi, '_').toLowerCase();
    }

    generateUID() {
        return 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, function(c) {
            const r = Math.random() * 16 | 0;
            const v = c === 'x' ? r : (r & 0x3 | 0x8);
            return v.toString(16);
        });
    }

    // Bulk export for multiple tournaments
    exportMultiple(tournaments) {
        const ics = [
            'BEGIN:VCALENDAR',
            'VERSION:2.0',
            'PRODID:-//ChessCalendar-RU//NONSGML v1.0//EN',
            'CALSCALE:GREGORIAN',
            'METHOD:PUBLISH'
        ];

        tournaments.forEach(tournament => {
            ics.push('BEGIN:VEVENT');
            ics.push(`UID:${this.generateUID()}@chesscalendar-ru.ru`);
            ics.push(`DTSTART:${this.formatICSDate(new Date(tournament.start_date))}`);
            ics.push(`DTEND:${this.formatICSDate(new Date(tournament.end_date))}`);
            ics.push(`SUMMARY:${this.escapeICS(tournament.name)}`);
            ics.push(`LOCATION:${this.escapeICS(tournament.location)}`);
            if (tournament.description) {
                ics.push(`DESCRIPTION:${this.escapeICS(tournament.description)}`);
            }
            ics.push('STATUS:CONFIRMED');
            ics.push('SEQUENCE:0');
            ics.push('END:VEVENT');
        });

        ics.push('END:VCALENDAR');

        const blob = new Blob([ics.join('\r\n')], { type: 'text/calendar;charset=utf-8' });
        const link = document.createElement('a');
        link.href = URL.createObjectURL(blob);
        link.download = `chess_tournaments_${new Date().toISOString().split('T')[0]}.ics`;
        link.click();

        if (window.toast) {
            window.toast.success(`Экспортировано ${tournaments.length} турниров`);
        }
    }
}

// Initialize
const calendarExport = new CalendarExport();

// Export for use in other scripts
window.calendarExport = calendarExport;
