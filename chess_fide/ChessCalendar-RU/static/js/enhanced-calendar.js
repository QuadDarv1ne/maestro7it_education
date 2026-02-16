/**
 * Улучшенный календарь для ChessCalendar-RU
 * Добавляет интерактивные возможности и интеграцию с различными календарными сервисами
 */
class EnhancedCalendar {
    constructor(containerId, options = {}) {
        this.container = document.getElementById(containerId);
        this.options = {
            locale: 'ru-RU',
            startDay: 1, // Понедельник
            showWeekNumbers: true,
            ...options
        };
        
        this.currentDate = new Date();
        this.tournaments = [];
        this.filteredTournaments = [];
        
        this.init();
    }
    
    init() {
        this.render();
        this.bindEvents();
        this.loadTournaments();
    }
    
    async loadTournaments() {
        try {
            const response = await fetch('/api/tournaments');
            const data = await response.json();
            this.tournaments = data.tournaments || [];
            this.filteredTournaments = [...this.tournaments];
            this.updateCalendarDays();
        } catch (error) {
            console.error('Ошибка загрузки турниров:', error);
        }
    }
    
    render() {
        this.container.innerHTML = this.getTemplate();
        this.updateCalendar();
    }
    
    getTemplate() {
        return `
            <div class="enhanced-calendar">
                <div class="calendar-controls mb-3">
                    <div class="row align-items-center">
                        <div class="col-md-6">
                            <div class="btn-group">
                                <button class="btn btn-outline-primary btn-sm" id="prevMonth">
                                    <i class="bi bi-chevron-left"></i>
                                </button>
                                <button class="btn btn-primary btn-sm" id="currentMonth">
                                    Сегодня
                                </button>
                                <button class="btn btn-outline-primary btn-sm" id="nextMonth">
                                    <i class="bi bi-chevron-right"></i>
                                </button>
                            </div>
                            <span class="mx-3 fs-5" id="currentMonthYear"></span>
                        </div>
                        <div class="col-md-6 text-md-end">
                            <div class="btn-group">
                                <button class="btn btn-outline-secondary btn-sm" id="viewMonth" data-view="month">
                                    Месяц
                                </button>
                                <button class="btn btn-outline-secondary btn-sm" id="viewWeek" data-view="week">
                                    Неделя
                                </button>
                                <button class="btn btn-outline-secondary btn-sm" id="viewDay" data-view="day">
                                    День
                                </button>
                            </div>
                            <div class="dropdown d-inline-block ms-2">
                                <button class="btn btn-outline-secondary btn-sm dropdown-toggle" type="button" id="exportDropdown" data-bs-toggle="dropdown">
                                    Экспорт
                                </button>
                                <ul class="dropdown-menu">
                                    <li><a class="dropdown-item" href="#" id="exportICS">ICS (календарь)</a></li>
                                    <li><a class="dropdown-item" href="#" id="exportGoogle">Google Calendar</a></li>
                                    <li><a class="dropdown-item" href="#" id="exportOutlook">Outlook</a></li>
                                    <li><hr class="dropdown-divider"></li>
                                    <li><a class="dropdown-item" href="#" id="exportCSV">CSV</a></li>
                                </ul>
                            </div>
                        </div>
                    </div>
                </div>
                
                <div class="calendar-container">
                    <div class="calendar-grid" id="calendarGrid">
                        <!-- Календарь будет сгенерирован здесь -->
                    </div>
                </div>
                
                <div class="calendar-sidebar mt-3" id="calendarSidebar" style="display: none;">
                    <div class="card">
                        <div class="card-header">
                            <h6 class="mb-0">Турниры на выбранную дату</h6>
                        </div>
                        <div class="card-body">
                            <div id="dayTournaments">
                                <!-- Турниры дня будут отображаться здесь -->
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        `;
    }
    
    updateCalendar() {
        this.updateMonthYearDisplay();
        this.renderCalendarGrid();
    }
    
    updateMonthYearDisplay() {
        const monthYearElement = document.getElementById('currentMonthYear');
        monthYearElement.textContent = this.currentDate.toLocaleDateString(this.options.locale, {
            month: 'long',
            year: 'numeric'
        }).replace(/^\w/, char => char.toUpperCase());
    }
    
    renderCalendarGrid() {
        const gridElement = document.getElementById('calendarGrid');
        const year = this.currentDate.getFullYear();
        const month = this.currentDate.getMonth();
        
        // Получаем первый день месяца и последний день месяца
        const firstDay = new Date(year, month, 1);
        const lastDay = new Date(year, month + 1, 0);
        
        // Получаем день недели первого дня (0 = воскресенье, 1 = понедельник, etc.)
        const firstDayOfWeek = this.options.startDay === 1 ? 
            (firstDay.getDay() === 0 ? 6 : firstDay.getDay() - 1) : firstDay.getDay();
        
        // Создаем заголовки дней недели
        const weekdays = this.getWeekdayNames();
        let weekdaysHtml = '<div class="calendar-weekdays">';
        if (this.options.showWeekNumbers) {
            weekdaysHtml += '<div class="calendar-weekday week-number">#</div>';
        }
        weekdays.forEach(day => {
            weekdaysHtml += `<div class="calendar-weekday">${day}</div>`;
        });
        weekdaysHtml += '</div>';
        
        // Создаем дни календаря
        const daysInMonth = lastDay.getDate();
        const daysHtml = this.generateMonthDays(year, month, firstDayOfWeek, daysInMonth);
        
        gridElement.innerHTML = weekdaysHtml + daysHtml;
    }
    
    getWeekdayNames() {
        const weekdays = ['Пн', 'Вт', 'Ср', 'Чт', 'Пт', 'Сб', 'Вс'];
        if (this.options.startDay === 0) {
            // Если неделя начинается с воскресенья, перемещаем последний элемент в начало
            weekdays.unshift(weekdays.pop());
        }
        return weekdays;
    }
    
    generateMonthDays(year, month, firstDayOfWeek, daysInMonth) {
        let daysHtml = '<div class="calendar-days">';
        
        // Добавляем пустые ячейки для дней до начала месяца
        for (let i = 0; i < firstDayOfWeek; i++) {
            daysHtml += '<div class="calendar-day empty"></div>';
        }
        
        // Добавляем дни месяца
        for (let day = 1; day <= daysInMonth; day++) {
            const date = new Date(year, month, day);
            const dateStr = date.toISOString().split('T')[0];
            const dayTournaments = this.getTournamentsForDate(date);
            const isToday = this.isToday(date);
            const hasTournaments = dayTournaments.length > 0;
            
            daysHtml += `
                <div class="calendar-day ${isToday ? 'today' : ''}" data-date="${dateStr}">
                    <div class="day-header">
                        <span class="day-number">${day}</span>
                        ${hasTournaments ? '<span class="tournament-indicator"></span>' : ''}
                    </div>
                    <div class="day-tournaments">
                        ${this.renderDayTournaments(dayTournaments)}
                    </div>
                </div>
            `;
        }
        
        daysHtml += '</div>';
        return daysHtml;
    }
    
    renderDayTournaments(tournaments) {
        if (tournaments.length === 0) return '';
        
        let tournamentsHtml = '<div class="day-tournaments-list">';
        tournaments.slice(0, 3).forEach(tournament => {
            tournamentsHtml += `
                <div class="tournament-badge ${tournament.category.toLowerCase().replace(/\s+/g, '-')}">
                    <a href="/tournament/${tournament.id}" class="tournament-link">
                        ${this.truncateText(tournament.name, 20)}
                    </a>
                </div>
            `;
        });
        
        if (tournaments.length > 3) {
            tournamentsHtml += `<div class="more-tournaments">+${tournaments.length - 3} еще</div>`;
        }
        
        tournamentsHtml += '</div>';
        return tournamentsHtml;
    }
    
    truncateText(text, maxLength) {
        if (text.length <= maxLength) return text;
        return text.substr(0, maxLength) + '...';
    }
    
    getTournamentsForDate(date) {
        const dateStr = date.toISOString().split('T')[0];
        return this.filteredTournaments.filter(tournament => {
            const startDate = new Date(tournament.start_date);
            const endDate = new Date(tournament.end_date);
            return date >= startDate && date <= endDate;
        });
    }
    
    isToday(date) {
        const today = new Date();
        return date.getDate() === today.getDate() &&
               date.getMonth() === today.getMonth() &&
               date.getFullYear() === today.getFullYear();
    }
    
    bindEvents() {
        // Обработчики навигации
        document.getElementById('prevMonth').addEventListener('click', () => {
            this.currentDate.setMonth(this.currentDate.getMonth() - 1);
            this.updateCalendar();
        });
        
        document.getElementById('nextMonth').addEventListener('click', () => {
            this.currentDate.setMonth(this.currentDate.getMonth() + 1);
            this.updateCalendar();
        });
        
        document.getElementById('currentMonth').addEventListener('click', () => {
            this.currentDate = new Date();
            this.updateCalendar();
        });
        
        // Обработчики просмотра
        document.querySelectorAll('[id^="view"]').forEach(button => {
            button.addEventListener('click', (e) => {
                this.switchView(e.target.dataset.view);
            });
        });
        
        // Обработчики экспорта
        document.getElementById('exportICS').addEventListener('click', () => this.exportToICS());
        document.getElementById('exportGoogle').addEventListener('click', () => this.exportToGoogle());
        document.getElementById('exportOutlook').addEventListener('click', () => this.exportToOutlook());
        document.getElementById('exportCSV').addEventListener('click', () => this.exportToCSV());
        
        // Обработчики кликов по дням
        this.container.addEventListener('click', (e) => {
            if (e.target.closest('.calendar-day') && !e.target.closest('.calendar-day.empty')) {
                const dayElement = e.target.closest('.calendar-day');
                const date = dayElement.dataset.date;
                if (date) {
                    this.showDayTournaments(date);
                }
            }
        });
    }
    
    switchView(view) {
        // Реализация переключения между видами (месяц, неделя, день)
        console.log(`Переключение на вид: ${view}`);
        // TODO: Реализовать переключение между видами
    }
    
    showDayTournaments(dateStr) {
        const date = new Date(dateStr);
        const tournaments = this.getTournamentsForDate(date);
        
        const sidebar = document.getElementById('calendarSidebar');
        const dayTournaments = document.getElementById('dayTournaments');
        
        if (tournaments.length > 0) {
            let html = '<ul class="list-unstyled">';
            tournaments.forEach(tournament => {
                html += `
                    <li class="mb-2">
                        <div class="tournament-day-item p-2 border rounded">
                            <div class="d-flex justify-content-between">
                                <strong>${tournament.name}</strong>
                                <span class="badge bg-${this.getStatusBadgeClass(tournament.status)}">${tournament.status}</span>
                            </div>
                            <small class="text-muted">${tournament.location}</small>
                            <div class="mt-1">
                                <small>${new Date(tournament.start_date).toLocaleDateString()} - ${new Date(tournament.end_date).toLocaleDateString()}</small>
                            </div>
                        </div>
                    </li>
                `;
            });
            html += '</ul>';
            dayTournaments.innerHTML = html;
            sidebar.style.display = 'block';
        } else {
            dayTournaments.innerHTML = '<p class="text-muted">На эту дату нет турниров</p>';
            sidebar.style.display = 'block';
        }
    }
    
    getStatusBadgeClass(status) {
        const statusClasses = {
            'Scheduled': 'primary',
            'Ongoing': 'warning',
            'Completed': 'success',
            'Cancelled': 'danger'
        };
        return statusClasses[status] || 'secondary';
    }
    
    async exportToICS() {
        try {
            const response = await fetch('/api/export/ics', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    tournaments: this.filteredTournaments
                })
            });
            
            if (response.ok) {
                const blob = await response.blob();
                const url = window.URL.createObjectURL(blob);
                const a = document.createElement('a');
                a.href = url;
                a.download = `chess-tournaments-${this.currentDate.getFullYear()}-${String(this.currentDate.getMonth() + 1).padStart(2, '0')}.ics`;
                document.body.appendChild(a);
                a.click();
                window.URL.revokeObjectURL(url);
                document.body.removeChild(a);
            }
        } catch (error) {
            console.error('Ошибка экспорта в ICS:', error);
            alert('Ошибка при экспорте в ICS');
        }
    }
    
    exportToGoogle() {
        alert('Функция экспорта в Google Calendar будет реализована в следующем обновлении');
        // Здесь должна быть реализация интеграции с Google Calendar API
    }
    
    exportToOutlook() {
        alert('Функция экспорта в Outlook будет реализована в следующем обновлении');
        // Здесь должна быть реализация интеграции с Outlook API
    }
    
    exportToCSV() {
        alert('Функция экспорта в CSV будет реализована в следующем обновлении');
        // Здесь должна быть реализация экспорта в CSV
    }
    
    updateCalendarDays() {
        // Обновляем отображение дней календаря с новыми данными
        this.renderCalendarGrid();
    }
}

// Инициализация календаря при загрузке DOM
document.addEventListener('DOMContentLoaded', function() {
    if (document.getElementById('enhanced-calendar')) {
        new EnhancedCalendar('enhanced-calendar');
    }
});