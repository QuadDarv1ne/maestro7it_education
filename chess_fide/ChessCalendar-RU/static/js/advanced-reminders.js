/**
 * Advanced Reminders Module
 * Продвинутая система напоминаний о турнирах
 */

class AdvancedReminders {
    constructor() {
        this.reminders = this.loadReminders();
        this.init();
    }

    init() {
        console.log('[AdvancedReminders] Инициализация системы напоминаний');
        this.setupReminderButtons();
        this.checkReminders();
        this.startReminderChecker();
    }

    setupReminderButtons() {
        document.addEventListener('click', (e) => {
            if (e.target.closest('.set-reminder-btn')) {
                e.preventDefault();
                const btn = e.target.closest('.set-reminder-btn');
                const tournamentId = btn.dataset.tournamentId;
                const tournamentName = btn.dataset.tournamentName;
                const startDate = btn.dataset.startDate;
                this.showReminderModal(tournamentId, tournamentName, startDate);
            }
        });
    }

    showReminderModal(tournamentId, tournamentName, startDate) {
        const modal = document.createElement('div');
        modal.className = 'modal fade';
        modal.id = 'reminderModal';
        modal.innerHTML = `
            <div class="modal-dialog modal-dialog-centered">
                <div class="modal-content">
                    <div class="modal-header">
                        <h5 class="modal-title">
                            <i class="bi bi-alarm"></i> Настроить напоминание
                        </h5>
                        <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
                    </div>
                    <div class="modal-body">
                        <h6 class="mb-3">${tournamentName}</h6>
                        <p class="text-muted">Начало: ${this.formatDate(startDate)}</p>
                        
                        <div class="reminder-options">
                            <div class="form-check reminder-option">
                                <input class="form-check-input" type="checkbox" id="reminder1day" value="1">
                                <label class="form-check-label" for="reminder1day">
                                    <i class="bi bi-bell"></i> За 1 день
                                </label>
                            </div>
                            <div class="form-check reminder-option">
                                <input class="form-check-input" type="checkbox" id="reminder3days" value="3">
                                <label class="form-check-label" for="reminder3days">
                                    <i class="bi bi-bell"></i> За 3 дня
                                </label>
                            </div>
                            <div class="form-check reminder-option">
                                <input class="form-check-input" type="checkbox" id="reminder1week" value="7">
                                <label class="form-check-label" for="reminder1week">
                                    <i class="bi bi-bell"></i> За 1 неделю
                                </label>
                            </div>
                            <div class="form-check reminder-option">
                                <input class="form-check-input" type="checkbox" id="reminder2weeks" value="14">
                                <label class="form-check-label" for="reminder2weeks">
                                    <i class="bi bi-bell"></i> За 2 недели
                                </label>
                            </div>
                            <div class="form-check reminder-option">
                                <input class="form-check-input" type="checkbox" id="reminder1month" value="30">
                                <label class="form-check-label" for="reminder1month">
                                    <i class="bi bi-bell"></i> За 1 месяц
                                </label>
                            </div>
                        </div>

                        <div class="mt-3">
                            <label class="form-label">Пользовательское напоминание:</label>
                            <div class="input-group">
                                <input type="number" class="form-control" id="customDays" min="1" max="365" placeholder="Дней">
                                <button class="btn btn-outline-primary" id="addCustomReminder">
                                    <i class="bi bi-plus-lg"></i> Добавить
                                </button>
                            </div>
                        </div>

                        <div class="mt-3">
                            <div class="form-check form-switch">
                                <input class="form-check-input" type="checkbox" id="emailNotification">
                                <label class="form-check-label" for="emailNotification">
                                    Email уведомления
                                </label>
                            </div>
                            <div class="form-check form-switch">
                                <input class="form-check-input" type="checkbox" id="pushNotification" checked>
                                <label class="form-check-label" for="pushNotification">
                                    Push уведомления
                                </label>
                            </div>
                        </div>

                        <div id="activeReminders" class="mt-3"></div>
                    </div>
                    <div class="modal-footer">
                        <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Отмена</button>
                        <button type="button" class="btn btn-primary" id="saveReminders">
                            <i class="bi bi-check-lg"></i> Сохранить
                        </button>
                    </div>
                </div>
            </div>
        `;

        document.body.appendChild(modal);
        const bsModal = new bootstrap.Modal(modal);
        bsModal.show();

        // Загружаем существующие напоминания
        this.loadExistingReminders(tournamentId, modal);

        // Обработчики
        modal.querySelector('#addCustomReminder').addEventListener('click', () => {
            const days = parseInt(modal.querySelector('#customDays').value);
            if (days > 0 && days <= 365) {
                this.addCustomReminderOption(modal, days);
                modal.querySelector('#customDays').value = '';
            }
        });

        modal.querySelector('#saveReminders').addEventListener('click', () => {
            this.saveReminders(tournamentId, tournamentName, startDate, modal);
            bsModal.hide();
        });

        modal.addEventListener('hidden.bs.modal', () => {
            modal.remove();
        });
    }

    loadExistingReminders(tournamentId, modal) {
        const existing = this.reminders[tournamentId] || [];
        existing.forEach(reminder => {
            const checkbox = modal.querySelector(`#reminder${reminder.days}day${reminder.days === 1 ? '' : 's'}`);
            if (checkbox) {
                checkbox.checked = true;
            }
        });
    }

    addCustomReminderOption(modal, days) {
        const container = modal.querySelector('.reminder-options');
        const option = document.createElement('div');
        option.className = 'form-check reminder-option custom-reminder';
        option.innerHTML = `
            <input class="form-check-input" type="checkbox" id="reminderCustom${days}" value="${days}" checked>
            <label class="form-check-label" for="reminderCustom${days}">
                <i class="bi bi-bell"></i> За ${days} ${this.getDaysWord(days)}
            </label>
            <button class="btn btn-sm btn-link text-danger remove-custom" data-days="${days}">
                <i class="bi bi-x-lg"></i>
            </button>
        `;
        container.appendChild(option);

        option.querySelector('.remove-custom').addEventListener('click', () => {
            option.remove();
        });
    }

    saveReminders(tournamentId, tournamentName, startDate, modal) {
        const checkboxes = modal.querySelectorAll('.reminder-option input[type="checkbox"]:checked');
        const reminders = [];

        checkboxes.forEach(checkbox => {
            const days = parseInt(checkbox.value);
            const reminderDate = new Date(startDate);
            reminderDate.setDate(reminderDate.getDate() - days);

            reminders.push({
                days: days,
                reminderDate: reminderDate.toISOString(),
                tournamentName: tournamentName,
                startDate: startDate,
                emailEnabled: modal.querySelector('#emailNotification').checked,
                pushEnabled: modal.querySelector('#pushNotification').checked,
                triggered: false
            });
        });

        this.reminders[tournamentId] = reminders;
        this.saveToStorage();
        
        this.showToast(`Установлено ${reminders.length} напоминаний`, 'success');
        
        // Запрашиваем разрешение на уведомления
        if (reminders.some(r => r.pushEnabled)) {
            this.requestNotificationPermission();
        }
    }

    checkReminders() {
        const now = new Date();
        let triggered = 0;

        Object.keys(this.reminders).forEach(tournamentId => {
            this.reminders[tournamentId].forEach(reminder => {
                if (!reminder.triggered) {
                    const reminderDate = new Date(reminder.reminderDate);
                    if (now >= reminderDate) {
                        this.triggerReminder(tournamentId, reminder);
                        reminder.triggered = true;
                        triggered++;
                    }
                }
            });
        });

        if (triggered > 0) {
            this.saveToStorage();
        }
    }

    triggerReminder(tournamentId, reminder) {
        console.log('[AdvancedReminders] Срабатывание напоминания:', reminder);

        // Push уведомление
        if (reminder.pushEnabled && 'Notification' in window && Notification.permission === 'granted') {
            new Notification('Напоминание о турнире', {
                body: `${reminder.tournamentName} начнётся через ${reminder.days} ${this.getDaysWord(reminder.days)}`,
                icon: '/static/icons/icon-192x192.png',
                badge: '/static/icons/icon-72x72.png',
                tag: `reminder-${tournamentId}`,
                requireInteraction: true,
                data: { tournamentId: tournamentId }
            });
        }

        // Визуальное уведомление
        this.showToast(
            `Напоминание: ${reminder.tournamentName} начнётся через ${reminder.days} ${this.getDaysWord(reminder.days)}`,
            'info',
            10000
        );

        // Email (требует серверной части)
        if (reminder.emailEnabled) {
            this.sendEmailReminder(tournamentId, reminder);
        }
    }

    async sendEmailReminder(tournamentId, reminder) {
        try {
            await fetch('/api/reminders/email', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    tournamentId: tournamentId,
                    reminder: reminder
                })
            });
        } catch (error) {
            console.error('[AdvancedReminders] Ошибка отправки email:', error);
        }
    }

    startReminderChecker() {
        // Проверяем каждый час
        setInterval(() => {
            this.checkReminders();
        }, 60 * 60 * 1000);

        // Проверяем при загрузке страницы
        this.checkReminders();
    }

    async requestNotificationPermission() {
        if ('Notification' in window && Notification.permission === 'default') {
            const permission = await Notification.requestPermission();
            if (permission === 'granted') {
                this.showToast('Уведомления включены!', 'success');
            }
        }
    }

    loadReminders() {
        const data = localStorage.getItem('tournament_reminders');
        return data ? JSON.parse(data) : {};
    }

    saveToStorage() {
        localStorage.setItem('tournament_reminders', JSON.stringify(this.reminders));
    }

    formatDate(dateString) {
        const date = new Date(dateString);
        return date.toLocaleDateString('ru-RU', {
            day: 'numeric',
            month: 'long',
            year: 'numeric'
        });
    }

    getDaysWord(days) {
        if (days === 1) return 'день';
        if (days >= 2 && days <= 4) return 'дня';
        return 'дней';
    }

    showToast(message, type = 'info', duration = 5000) {
        if (window.ChessCalendar && window.ChessCalendar.showToast) {
            window.ChessCalendar.showToast(message, type, duration);
        }
    }

    // Получить все напоминания
    getAllReminders() {
        return this.reminders;
    }

    // Удалить напоминание
    deleteReminder(tournamentId) {
        delete this.reminders[tournamentId];
        this.saveToStorage();
        this.showToast('Напоминания удалены', 'success');
    }
}

// Стили
const style = document.createElement('style');
style.textContent = `
    .reminder-option {
        padding: 0.75rem;
        border: 2px solid var(--border-color);
        border-radius: 8px;
        margin-bottom: 0.5rem;
        transition: all 0.3s ease;
        display: flex;
        align-items: center;
        justify-content: space-between;
    }

    .reminder-option:hover {
        background: var(--bg-secondary);
        border-color: var(--primary-color);
    }

    .reminder-option input:checked ~ label {
        color: var(--primary-color);
        font-weight: 600;
    }

    .reminder-option label {
        margin-bottom: 0;
        cursor: pointer;
        flex: 1;
    }

    .reminder-option i {
        margin-right: 0.5rem;
    }

    .custom-reminder {
        background: var(--bg-secondary);
    }

    .remove-custom {
        padding: 0.25rem 0.5rem;
    }
`;
document.head.appendChild(style);

// Инициализация
document.addEventListener('DOMContentLoaded', () => {
    window.ChessCalendar = window.ChessCalendar || {};
    window.ChessCalendar.advancedReminders = new AdvancedReminders();
});
