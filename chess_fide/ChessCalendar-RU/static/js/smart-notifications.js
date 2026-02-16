// Smart Notifications - умные напоминания о турнирах

class SmartNotifications {
    constructor() {
        this.storageKey = 'smart_notifications';
        this.remindersKey = 'tournament_reminders';
        this.init();
    }

    init() {
        this.loadSettings();
        this.loadReminders();
        this.checkPermissions();
        this.createNotificationCenter();
        this.startReminderCheck();
    }

    loadSettings() {
        const stored = localStorage.getItem(this.storageKey);
        this.settings = stored ? JSON.parse(stored) : {
            enabled: false,
            beforeDays: [7, 3, 1], // За сколько дней напоминать
            beforeHours: [24, 12, 1], // За сколько часов напоминать
            sound: true,
            desktop: false
        };
    }

    saveSettings() {
        localStorage.setItem(this.storageKey, JSON.stringify(this.settings));
    }

    loadReminders() {
        const stored = localStorage.getItem(this.remindersKey);
        this.reminders = stored ? JSON.parse(stored) : [];
    }

    saveReminders() {
        localStorage.setItem(this.remindersKey, JSON.stringify(this.reminders));
    }

    async checkPermissions() {
        if ('Notification' in window && this.settings.desktop) {
            if (Notification.permission === 'default') {
                const permission = await Notification.requestPermission();
                this.settings.desktop = permission === 'granted';
                this.saveSettings();
            } else if (Notification.permission === 'denied') {
                this.settings.desktop = false;
                this.saveSettings();
            }
        }
    }

    createNotificationCenter() {
        // Проверяем, не создан ли уже центр
        if (document.getElementById('notificationCenter')) return;

        const center = document.createElement('div');
        center.id = 'notificationCenter';
        center.innerHTML = `
            <style>
                #notificationCenter {
                    position: fixed;
                    top: 70px;
                    right: 20px;
                    width: 380px;
                    max-height: 600px;
                    background: var(--bg-primary);
                    border-radius: 12px;
                    box-shadow: 0 8px 32px rgba(0, 0, 0, 0.15);
                    z-index: 1000;
                    display: none;
                    flex-direction: column;
                    overflow: hidden;
                }
                
                #notificationCenter.open {
                    display: flex;
                }
                
                .notification-center-header {
                    padding: 1.25rem;
                    background: linear-gradient(135deg, var(--primary-color) 0%, #1e40af 100%);
                    color: white;
                    display: flex;
                    justify-content: space-between;
                    align-items: center;
                }
                
                .notification-center-header h5 {
                    margin: 0;
                    font-weight: 700;
                    display: flex;
                    align-items: center;
                    gap: 0.5rem;
                }
                
                .notification-center-tabs {
                    display: flex;
                    background: var(--bg-secondary);
                    border-bottom: 2px solid var(--border-color);
                }
                
                .notification-tab {
                    flex: 1;
                    padding: 0.75rem;
                    text-align: center;
                    cursor: pointer;
                    font-weight: 600;
                    font-size: 0.875rem;
                    color: var(--text-secondary);
                    transition: all 0.2s ease;
                    border-bottom: 3px solid transparent;
                }
                
                .notification-tab:hover {
                    background: var(--bg-primary);
                }
                
                .notification-tab.active {
                    color: var(--primary-color);
                    border-bottom-color: var(--primary-color);
                    background: var(--bg-primary);
                }
                
                .notification-center-content {
                    flex: 1;
                    overflow-y: auto;
                    padding: 1rem;
                }
                
                .notification-item {
                    padding: 1rem;
                    margin-bottom: 0.75rem;
                    background: var(--bg-secondary);
                    border-radius: 8px;
                    border-left: 4px solid var(--primary-color);
                    cursor: pointer;
                    transition: all 0.2s ease;
                }
                
                .notification-item:hover {
                    transform: translateX(-5px);
                    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
                }
                
                .notification-item.unread {
                    background: rgba(37, 99, 235, 0.05);
                    border-left-color: var(--primary-color);
                }
                
                .notification-item-header {
                    display: flex;
                    justify-content: space-between;
                    align-items: start;
                    margin-bottom: 0.5rem;
                }
                
                .notification-item-title {
                    font-weight: 600;
                    color: var(--text-primary);
                    font-size: 0.95rem;
                    line-height: 1.3;
                }
                
                .notification-item-time {
                    font-size: 0.75rem;
                    color: var(--text-muted);
                    white-space: nowrap;
                }
                
                .notification-item-body {
                    font-size: 0.875rem;
                    color: var(--text-secondary);
                    line-height: 1.4;
                }
                
                .notification-item-actions {
                    margin-top: 0.75rem;
                    display: flex;
                    gap: 0.5rem;
                }
                
                .notification-item-actions button {
                    padding: 0.4rem 0.875rem;
                    border: none;
                    border-radius: 6px;
                    font-size: 0.8rem;
                    font-weight: 600;
                    cursor: pointer;
                    transition: all 0.2s ease;
                }
                
                .btn-view {
                    background: var(--primary-color);
                    color: white;
                }
                
                .btn-dismiss {
                    background: var(--bg-tertiary);
                    color: var(--text-primary);
                }
                
                .notification-empty {
                    text-align: center;
                    padding: 3rem 1rem;
                    color: var(--text-muted);
                }
                
                .notification-empty i {
                    font-size: 3rem;
                    margin-bottom: 1rem;
                    opacity: 0.5;
                }
                
                .notification-settings {
                    padding: 1rem;
                }
                
                .setting-item {
                    display: flex;
                    justify-content: space-between;
                    align-items: center;
                    padding: 0.75rem 0;
                    border-bottom: 1px solid var(--border-color);
                }
                
                .setting-item:last-child {
                    border-bottom: none;
                }
                
                .setting-label {
                    font-weight: 600;
                    color: var(--text-primary);
                    font-size: 0.9rem;
                }
                
                .setting-description {
                    font-size: 0.8rem;
                    color: var(--text-secondary);
                    margin-top: 0.25rem;
                }
                
                .toggle-switch {
                    position: relative;
                    width: 50px;
                    height: 26px;
                }
                
                .toggle-switch input {
                    opacity: 0;
                    width: 0;
                    height: 0;
                }
                
                .toggle-slider {
                    position: absolute;
                    cursor: pointer;
                    top: 0;
                    left: 0;
                    right: 0;
                    bottom: 0;
                    background-color: var(--bg-tertiary);
                    transition: 0.3s;
                    border-radius: 26px;
                }
                
                .toggle-slider:before {
                    position: absolute;
                    content: "";
                    height: 20px;
                    width: 20px;
                    left: 3px;
                    bottom: 3px;
                    background-color: white;
                    transition: 0.3s;
                    border-radius: 50%;
                }
                
                input:checked + .toggle-slider {
                    background-color: var(--primary-color);
                }
                
                input:checked + .toggle-slider:before {
                    transform: translateX(24px);
                }
                
                @media (max-width: 768px) {
                    #notificationCenter {
                        width: 100%;
                        max-width: 100%;
                        right: 0;
                        top: 60px;
                        max-height: calc(100vh - 60px);
                        border-radius: 0;
                    }
                }
            </style>
            
            <div class="notification-center-header">
                <h5><i class="bi bi-bell-fill"></i> Уведомления</h5>
                <button class="btn btn-link text-white p-0" onclick="smartNotifications.toggle()">
                    <i class="bi bi-x-lg"></i>
                </button>
            </div>
            
            <div class="notification-center-tabs">
                <div class="notification-tab active" data-tab="reminders" onclick="smartNotifications.switchTab('reminders')">
                    <i class="bi bi-clock"></i> Напоминания
                </div>
                <div class="notification-tab" data-tab="settings" onclick="smartNotifications.switchTab('settings')">
                    <i class="bi bi-gear"></i> Настройки
                </div>
            </div>
            
            <div class="notification-center-content">
                <div id="remindersTab" class="tab-content active">
                    ${this.renderReminders()}
                </div>
                <div id="settingsTab" class="tab-content" style="display: none;">
                    ${this.renderSettings()}
                </div>
            </div>
        `;

        document.body.appendChild(center);
        
        // Добавляем кнопку в навбар
        this.addNavbarButton();
    }

    addNavbarButton() {
        const navbar = document.querySelector('.navbar-nav');
        if (!navbar || document.getElementById('notificationBellBtn')) return;

        const bellBtn = document.createElement('li');
        bellBtn.className = 'nav-item';
        bellBtn.innerHTML = `
            <a class="nav-link position-relative" href="#" id="notificationBellBtn" onclick="smartNotifications.toggle(); return false;">
                <i class="bi bi-bell-fill"></i>
                <span class="position-absolute top-0 start-100 translate-middle badge rounded-pill bg-danger" 
                      id="notificationBadge" style="display: none; font-size: 0.65rem;">
                    0
                </span>
            </a>
        `;
        
        // Вставляем перед кнопкой темы
        const themeBtn = navbar.querySelector('#themeToggle')?.parentElement;
        if (themeBtn) {
            navbar.insertBefore(bellBtn, themeBtn);
        } else {
            navbar.appendChild(bellBtn);
        }
    }

    renderReminders() {
        if (this.reminders.length === 0) {
            return `
                <div class="notification-empty">
                    <i class="bi bi-bell-slash"></i>
                    <p>Нет активных напоминаний</p>
                    <small>Добавьте напоминания о турнирах</small>
                </div>
            `;
        }

        return this.reminders.map(reminder => `
            <div class="notification-item ${reminder.read ? '' : 'unread'}" data-reminder-id="${reminder.id}">
                <div class="notification-item-header">
                    <div class="notification-item-title">${this.escapeHtml(reminder.title)}</div>
                    <div class="notification-item-time">${this.formatTime(reminder.time)}</div>
                </div>
                <div class="notification-item-body">${this.escapeHtml(reminder.message)}</div>
                <div class="notification-item-actions">
                    <button class="btn-view" onclick="smartNotifications.viewTournament(${reminder.tournamentId})">
                        <i class="bi bi-eye"></i> Посмотреть
                    </button>
                    <button class="btn-dismiss" onclick="smartNotifications.dismissReminder('${reminder.id}')">
                        <i class="bi bi-x"></i> Отклонить
                    </button>
                </div>
            </div>
        `).join('');
    }

    renderSettings() {
        return `
            <div class="notification-settings">
                <div class="setting-item">
                    <div>
                        <div class="setting-label">Включить уведомления</div>
                        <div class="setting-description">Получать напоминания о турнирах</div>
                    </div>
                    <label class="toggle-switch">
                        <input type="checkbox" ${this.settings.enabled ? 'checked' : ''} 
                               onchange="smartNotifications.toggleSetting('enabled', this.checked)">
                        <span class="toggle-slider"></span>
                    </label>
                </div>
                
                <div class="setting-item">
                    <div>
                        <div class="setting-label">Звуковые уведомления</div>
                        <div class="setting-description">Воспроизводить звук при напоминании</div>
                    </div>
                    <label class="toggle-switch">
                        <input type="checkbox" ${this.settings.sound ? 'checked' : ''}
                               onchange="smartNotifications.toggleSetting('sound', this.checked)">
                        <span class="toggle-slider"></span>
                    </label>
                </div>
                
                <div class="setting-item">
                    <div>
                        <div class="setting-label">Системные уведомления</div>
                        <div class="setting-description">Показывать уведомления на рабочем столе</div>
                    </div>
                    <label class="toggle-switch">
                        <input type="checkbox" ${this.settings.desktop ? 'checked' : ''}
                               onchange="smartNotifications.toggleSetting('desktop', this.checked)">
                        <span class="toggle-slider"></span>
                    </label>
                </div>
            </div>
        `;
    }

    toggle() {
        const center = document.getElementById('notificationCenter');
        if (center) {
            center.classList.toggle('open');
            
            // Обновляем счетчик при открытии
            if (center.classList.contains('open')) {
                this.updateBadge();
            }
        }
    }

    switchTab(tabName) {
        // Переключаем активную вкладку
        document.querySelectorAll('.notification-tab').forEach(tab => {
            tab.classList.remove('active');
        });
        document.querySelector(`[data-tab="${tabName}"]`).classList.add('active');

        // Показываем соответствующий контент
        document.getElementById('remindersTab').style.display = tabName === 'reminders' ? 'block' : 'none';
        document.getElementById('settingsTab').style.display = tabName === 'settings' ? 'block' : 'none';
    }

    toggleSetting(setting, value) {
        this.settings[setting] = value;
        this.saveSettings();

        if (setting === 'desktop' && value) {
            this.checkPermissions();
        }

        if (window.toast) {
            window.toast.success('Настройки сохранены');
        }
    }

    addReminder(tournament, daysBeforeStart) {
        const reminder = {
            id: `reminder_${Date.now()}`,
            tournamentId: tournament.id,
            title: tournament.name,
            message: `Турнир начнётся через ${daysBeforeStart} ${this.getDaysWord(daysBeforeStart)}`,
            time: new Date(tournament.startDate).getTime() - (daysBeforeStart * 24 * 60 * 60 * 1000),
            read: false,
            dismissed: false
        };

        this.reminders.push(reminder);
        this.saveReminders();
        this.updateBadge();

        if (window.toast) {
            window.toast.success('Напоминание добавлено');
        }
    }

    dismissReminder(reminderId) {
        this.reminders = this.reminders.filter(r => r.id !== reminderId);
        this.saveReminders();
        
        // Обновляем UI
        const reminderElement = document.querySelector(`[data-reminder-id="${reminderId}"]`);
        if (reminderElement) {
            reminderElement.remove();
        }
        
        this.updateBadge();
        
        // Если напоминаний не осталось, показываем пустое состояние
        if (this.reminders.length === 0) {
            document.getElementById('remindersTab').innerHTML = this.renderReminders();
        }
    }

    viewTournament(tournamentId) {
        window.location.href = `/tournament/${tournamentId}`;
    }

    startReminderCheck() {
        // Проверяем напоминания каждую минуту
        setInterval(() => {
            if (!this.settings.enabled) return;

            const now = Date.now();
            this.reminders.forEach(reminder => {
                if (!reminder.dismissed && !reminder.shown && reminder.time <= now) {
                    this.showReminder(reminder);
                    reminder.shown = true;
                    this.saveReminders();
                }
            });
        }, 60000); // Каждую минуту
    }

    showReminder(reminder) {
        // Показываем toast
        if (window.toast) {
            window.toast.info(reminder.message);
        }

        // Воспроизводим звук
        if (this.settings.sound) {
            this.playNotificationSound();
        }

        // Показываем системное уведомление
        if (this.settings.desktop && Notification.permission === 'granted') {
            new Notification(reminder.title, {
                body: reminder.message,
                icon: '/static/img/logo.png',
                badge: '/static/img/badge.png'
            });
        }

        this.updateBadge();
    }

    playNotificationSound() {
        // Простой звук уведомления
        const audio = new Audio('data:audio/wav;base64,UklGRnoGAABXQVZFZm10IBAAAAABAAEAQB8AAEAfAAABAAgAZGF0YQoGAACBhYqFbF1fdJivrJBhNjVgodDbq2EcBj+a2/LDciUFLIHO8tiJNwgZaLvt559NEAxQp+PwtmMcBjiR1/LMeSwFJHfH8N2QQAoUXrTp66hVFApGn+DyvmwhBSuBzvLZiTYIGGS57OihUBELTKXh8bllHAU2jdXvzn0pBSh+zPDajzsKElyx6OyrWBUIQ5zd8sFuJAUuhM/z24k2CBhkuezooVARC0yl4fG5ZRwFNo3V7859KQUofsz');
        audio.volume = 0.3;
        audio.play().catch(() => {});
    }

    updateBadge() {
        const unreadCount = this.reminders.filter(r => !r.read && !r.dismissed).length;
        const badge = document.getElementById('notificationBadge');
        
        if (badge) {
            if (unreadCount > 0) {
                badge.textContent = unreadCount;
                badge.style.display = 'inline-block';
            } else {
                badge.style.display = 'none';
            }
        }
    }

    escapeHtml(text) {
        const div = document.createElement('div');
        div.textContent = text;
        return div.innerHTML;
    }

    formatTime(timestamp) {
        const date = new Date(timestamp);
        const now = new Date();
        const diff = now - date;
        
        if (diff < 60000) return 'только что';
        if (diff < 3600000) return `${Math.floor(diff / 60000)} мин назад`;
        if (diff < 86400000) return `${Math.floor(diff / 3600000)} ч назад`;
        
        return date.toLocaleDateString('ru-RU', { 
            day: '2-digit', 
            month: '2-digit',
            year: 'numeric'
        });
    }

    getDaysWord(days) {
        if (days === 1) return 'день';
        if (days >= 2 && days <= 4) return 'дня';
        return 'дней';
    }
}

// Инициализация
const smartNotifications = new SmartNotifications();
window.smartNotifications = smartNotifications;
