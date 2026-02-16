// Interactive Calendar for ChessCalendar-RU

class TournamentCalendar {
    constructor(containerId, tournaments) {
        this.container = document.getElementById(containerId);
        this.tournaments = tournaments;
        this.currentDate = new Date();
        this.selectedDate = null;
        
        this.init();
    }
    
    init() {
        if (!this.container) return;
        
        this.render();
        this.attachEventListeners();
    }
    
    render() {
        const year = this.currentDate.getFullYear();
        const month = this.currentDate.getMonth();
        
        this.container.innerHTML = `
            <div class="calendar-header">
                <button class="btn btn-sm btn-outline-primary" id="prevMonth">
                    <i class="bi bi-chevron-left"></i>
                </button>
                <h4 class="mb-0">${this.getMonthName(month)} ${year}</h4>
                <button class="btn btn-sm btn-outline-primary" id="nextMonth">
                    <i class="bi bi-chevron-right"></i>
                </button>
            </div>
            <div class="calendar-weekdays">
                ${this.renderWeekdays()}
            </div>
            <div class="calendar-days">
                ${this.renderDays(year, month)}
            </div>
        `;
    }
    
    renderWeekdays() {
        const weekdays = ['Пн', 'Вт', 'Ср', 'Чт', 'Пт', 'Сб', 'Вс'];
        return weekdays.map(day => `<div class="calendar-weekday">${day}</div>`).join('');
    }
    
    renderDays(year, month) {
        const firstDay = new Date(year, month, 1);
        const lastDay = new Date(year, month + 1, 0);
        const daysInMonth = lastDay.getDate();
        const startingDayOfWeek = firstDay.getDay() || 7; // Monday = 1, Sunday = 7
        
        let html = '';
        
        // Empty cells before first day
        for (let i = 1; i < startingDayOfWeek; i++) {
            html += '<div class="calendar-day empty"></div>';
        }
        
        // Days of month
        for (let day = 1; day <= daysInMonth; day++) {
            const date = new Date(year, month, day);
            const dateStr = this.formatDate(date);
            const tournamentsOnDay = this.getTournamentsOnDate(date);
            const isToday = this.isToday(date);
            const isSelected = this.selectedDate && this.formatDate(this.selectedDate) === dateStr;
            
            let classes = 'calendar-day';
            if (isToday) classes += ' today';
            if (isSelected) classes += ' selected';
            if (tournamentsOnDay.length > 0) classes += ' has-tournaments';
            
            html += `
                <div class="${classes}" data-date="${dateStr}">
                    <div class="day-number">${day}</div>
                    ${tournamentsOnDay.length > 0 ? `
                        <div class="tournament-indicator">
                            <span class="badge bg-primary">${tournamentsOnDay.length}</span>
                        </div>
                    ` : ''}
                </div>
            `;
        }
        
        return html;
    }
    
    attachEventListeners() {
        // Navigation buttons
        const prevBtn = document.getElementById('prevMonth');
        const nextBtn = document.getElementById('nextMonth');
        
        if (prevBtn) {
            prevBtn.addEventListener('click', () => {
                this.currentDate.setMonth(this.currentDate.getMonth() - 1);
                this.render();
                this.attachEventListeners();
            });
        }
        
        if (nextBtn) {
            nextBtn.addEventListener('click', () => {
                this.currentDate.setMonth(this.currentDate.getMonth() + 1);
                this.render();
                this.attachEventListeners();
            });
        }
        
        // Day clicks
        const days = this.container.querySelectorAll('.calendar-day:not(.empty)');
        days.forEach(day => {
            day.addEventListener('click', (e) => {
                const dateStr = day.dataset.date;
                if (dateStr) {
                    this.selectedDate = new Date(dateStr);
                    this.render();
                    this.attachEventListeners();
                    this.showTournamentsForDate(this.selectedDate);
                }
            });
        });
    }
    
    showTournamentsForDate(date) {
        const tournaments = this.getTournamentsOnDate(date);
        const detailsContainer = document.getElementById('tournamentDetails');
        
        if (!detailsContainer) return;
        
        if (tournaments.length === 0) {
            detailsContainer.innerHTML = `
                <div class="text-center py-5">
                    <i class="bi bi-calendar-x" style="font-size: 3rem; color: var(--text-muted);"></i>
                    <p class="text-muted mt-3">Нет турниров на ${this.formatDateRu(date)}</p>
                </div>
            `;
            return;
        }
        
        detailsContainer.innerHTML = `
            <h5 class="mb-3">Турниры на ${this.formatDateRu(date)}</h5>
            <div class="list-group">
                ${tournaments.map(t => `
                    <a href="/tournament/${t.id}" class="list-group-item list-group-item-action">
                        <div class="d-flex justify-content-between align-items-start">
                            <div>
                                <h6 class="mb-1">${this.escapeHtml(t.name)}</h6>
                                <p class="mb-1 text-muted">
                                    <i class="bi bi-geo-alt"></i> ${this.escapeHtml(t.location)}
                                </p>
                                ${t.category ? `<span class="badge bg-secondary">${this.escapeHtml(t.category)}</span>` : ''}
                            </div>
                            <i class="bi bi-chevron-right"></i>
                        </div>
                    </a>
                `).join('')}
            </div>
        `;
    }
    
    getTournamentsOnDate(date) {
        const dateStr = this.formatDate(date);
        return this.tournaments.filter(t => {
            const startDate = new Date(t.start_date);
            const endDate = new Date(t.end_date);
            const checkDate = new Date(dateStr);
            
            return checkDate >= startDate && checkDate <= endDate;
        });
    }
    
    isToday(date) {
        const today = new Date();
        return date.getDate() === today.getDate() &&
               date.getMonth() === today.getMonth() &&
               date.getFullYear() === today.getFullYear();
    }
    
    formatDate(date) {
        return date.toISOString().split('T')[0];
    }
    
    formatDateRu(date) {
        return date.toLocaleDateString('ru-RU', {
            day: 'numeric',
            month: 'long',
            year: 'numeric'
        });
    }
    
    getMonthName(month) {
        const months = [
            'Январь', 'Февраль', 'Март', 'Апрель', 'Май', 'Июнь',
            'Июль', 'Август', 'Сентябрь', 'Октябрь', 'Ноябрь', 'Декабрь'
        ];
        return months[month];
    }
    
    escapeHtml(text) {
        const div = document.createElement('div');
        div.textContent = text;
        return div.innerHTML;
    }
}

// Export for global use
window.TournamentCalendar = TournamentCalendar;
