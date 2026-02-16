/**
 * Auto Theme Scheduler
 * Автоматическое переключение темы по расписанию
 */

class AutoThemeScheduler {
    constructor() {
        this.settings = this.loadSettings();
        this.init();
    }

    init() {
        console.log('[AutoThemeScheduler] Инициализация планировщика тем');
        this.createSettingsButton();
        this.startScheduler();
    }

    createSettingsButton() {
        // Добавляем кнопку настроек в меню темы
        const themeToggle = document.getElementById('themeToggle');
        if (themeToggle) {
            const settingsBtn = document.createElement('button');
            settingsBtn.className = 'nav-link btn btn-link';
            settingsBtn.innerHTML = '<i class="bi bi-clock-history"></i>';
            settingsBtn.title = 'Расписание темы';
            settingsBtn.onclick = () => this.showSettingsModal();
            
            themeToggle.parentNode.insertBefore(settingsBtn, themeToggle.nextSibling);
        }
    }

    showSettingsModal() {
        const modal = document.createElement('div');
        modal.className = 'modal fade';
        modal.id = 'themeSchedulerModal';
        modal.innerHTML = `
            <div class="modal-dialog modal-dialog-centered">
                <div class="modal-content">
                    <div class="modal-header">
                        <h5 class="modal-title">
                            <i class="bi bi-clock-history"></i> Расписание темы
                        </h5>
                        <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
                    </div>
                    <div class="modal-body">
                        <div class="mb-3">
                            <div class="form-check form-switch">
                                <input class="form-check-input" type="checkbox" id="autoThemeEnabled" 
                                    ${this.settings.enabled ? 'checked' : ''}>
                                <label class="form-check-label" for="autoThemeEnabled">
                                    Автоматическое переключение
                                </label>
                            </div>
                        </div>

                        <div id="scheduleSettings" ${!this.settings.enabled ? 'style="display:none"' : ''}>
                            <div class="schedule-mode mb-3">
                                <label class="form-label">Режим:</label>
                                <div class="btn-group w-100" role="group">
                                    <input type="radio" class="btn-check" name="scheduleMode" id="modeTime" 
                                        value="time" ${this.settings.mode === 'time' ? 'checked' : ''}>
                                    <label class="btn btn-outline-primary" for="modeTime">
                                        <i class="bi bi-clock"></i> По времени
                                    </label>
                                    
                                    <input type="radio" class="btn-check" name="scheduleMode" id="modeSunset" 
                                        value="sunset" ${this.settings.mode === 'sunset' ? 'checked' : ''}>
                                    <label class="btn btn-outline-primary" for="modeSunset">
                                        <i class="bi bi-sunset"></i> По закату
                                    </label>
                                    
                                    <input type="radio" class="btn-check" name="scheduleMode" id="modeSystem" 
                                        value="system" ${this.settings.mode === 'system' ? 'checked' : ''}>
                                    <label class="btn btn-outline-primary" for="modeSystem">
                                        <i class="bi bi-laptop"></i> Системная
                                    </label>
                                </div>
                            </div>

                            <div id="timeSettings" ${this.settings.mode !== 'time' ? 'style="display:none"' : ''}>
                                <div class="row">
                                    <div class="col-6">
                                        <label class="form-label">Светлая тема с:</label>
                                        <input type="time" class="form-control" id="lightThemeStart" 
                                            value="${this.settings.lightStart}">
                                    </div>
                                    <div class="col-6">
                                        <label class="form-label">Тёмная тема с:</label>
                                        <input type="time" class="form-control" id="darkThemeStart" 
                                            value="${this.settings.darkStart}">
                                    </div>
                                </div>
                            </div>

                            <div id="sunsetSettings" ${this.settings.mode !== 'sunset' ? 'style="display:none"' : ''}>
                                <div class="alert alert-info">
                                    <i class="bi bi-info-circle"></i>
                                    Тема будет переключаться автоматически на основе времени восхода и заката солнца в вашем регионе.
                                </div>
                                <div class="mb-2">
                                    <label class="form-label">Смещение (минуты):</label>
                                    <input type="number" class="form-control" id="sunsetOffset" 
                                        value="${this.settings.sunsetOffset}" min="-120" max="120">
                                    <small class="text-muted">Положительное значение = позже, отрицательное = раньше</small>
                                </div>
                            </div>

                            <div id="systemSettings" ${this.settings.mode !== 'system' ? 'style="display:none"' : ''}>
                                <div class="alert alert-info">
                                    <i class="bi bi-info-circle"></i>
                                    Тема будет следовать системным настройкам вашего устройства.
                                </div>
                            </div>

                            <div class="mt-3">
                                <div class="form-check">
                                    <input class="form-check-input" type="checkbox" id="smoothTransition" 
                                        ${this.settings.smoothTransition ? 'checked' : ''}>
                                    <label class="form-check-label" for="smoothTransition">
                                        Плавный переход
                                    </label>
                                </div>
                            </div>

                            <div class="mt-3 p-3 bg-light rounded">
                                <h6>Текущий статус:</h6>
                                <p class="mb-1">
                                    <strong>Текущая тема:</strong> 
                                    <span id="currentThemeStatus"></span>
                                </p>
                                <p class="mb-0">
                                    <strong>Следующее переключение:</strong> 
                                    <span id="nextSwitchTime"></span>
                                </p>
                            </div>
                        </div>
                    </div>
                    <div class="modal-footer">
                        <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Отмена</button>
                        <button type="button" class="btn btn-primary" id="saveThemeSchedule">
                            <i class="bi bi-check-lg"></i> Сохранить
                        </button>
                    </div>
                </div>
            </div>
        `;

        document.body.appendChild(modal);
        const bsModal = new bootstrap.Modal(modal);
        bsModal.show();

        // Обновляем статус
        this.updateStatus(modal);

        // Обработчики
        modal.querySelector('#autoThemeEnabled').addEventListener('change', (e) => {
            modal.querySelector('#scheduleSettings').style.display = e.target.checked ? 'block' : 'none';
        });

        modal.querySelectorAll('input[name="scheduleMode"]').forEach(radio => {
            radio.addEventListener('change', (e) => {
                modal.querySelector('#timeSettings').style.display = e.target.value === 'time' ? 'block' : 'none';
                modal.querySelector('#sunsetSettings').style.display = e.target.value === 'sunset' ? 'block' : 'none';
                modal.querySelector('#systemSettings').style.display = e.target.value === 'system' ? 'block' : 'none';
            });
        });

        modal.querySelector('#saveThemeSchedule').addEventListener('click', () => {
            this.saveSettings(modal);
            bsModal.hide();
        });

        modal.addEventListener('hidden.bs.modal', () => {
            modal.remove();
        });
    }

    saveSettings(modal) {
        this.settings = {
            enabled: modal.querySelector('#autoThemeEnabled').checked,
            mode: modal.querySelector('input[name="scheduleMode"]:checked').value,
            lightStart: modal.querySelector('#lightThemeStart').value,
            darkStart: modal.querySelector('#darkThemeStart').value,
            sunsetOffset: parseInt(modal.querySelector('#sunsetOffset').value),
            smoothTransition: modal.querySelector('#smoothTransition').checked
        };

        localStorage.setItem('theme_scheduler_settings', JSON.stringify(this.settings));
        this.showToast('Настройки сохранены', 'success');
        
        // Перезапускаем планировщик
        this.startScheduler();
    }

    startScheduler() {
        // Останавливаем предыдущий интервал
        if (this.interval) {
            clearInterval(this.interval);
        }

        if (!this.settings.enabled) {
            return;
        }

        // Применяем тему сразу
        this.applyScheduledTheme();

        // Проверяем каждую минуту
        this.interval = setInterval(() => {
            this.applyScheduledTheme();
        }, 60000);
    }

    applyScheduledTheme() {
        let shouldBeDark = false;

        switch (this.settings.mode) {
            case 'time':
                shouldBeDark = this.shouldBeDarkByTime();
                break;
            case 'sunset':
                shouldBeDark = this.shouldBeDarkBySunset();
                break;
            case 'system':
                shouldBeDark = this.shouldBeDarkBySystem();
                break;
        }

        const currentTheme = document.documentElement.getAttribute('data-theme');
        const targetTheme = shouldBeDark ? 'dark' : 'light';

        if (currentTheme !== targetTheme) {
            this.switchTheme(targetTheme);
        }
    }

    shouldBeDarkByTime() {
        const now = new Date();
        const currentTime = now.getHours() * 60 + now.getMinutes();
        
        const [lightH, lightM] = this.settings.lightStart.split(':').map(Number);
        const [darkH, darkM] = this.settings.darkStart.split(':').map(Number);
        
        const lightTime = lightH * 60 + lightM;
        const darkTime = darkH * 60 + darkM;

        if (darkTime > lightTime) {
            return currentTime >= darkTime || currentTime < lightTime;
        } else {
            return currentTime >= darkTime && currentTime < lightTime;
        }
    }

    shouldBeDarkBySunset() {
        // Упрощённый расчёт на основе времени
        // В реальном приложении можно использовать API для получения точного времени заката
        const now = new Date();
        const hour = now.getHours();
        const offset = this.settings.sunsetOffset / 60;
        
        // Примерное время заката: 18:00 зимой, 21:00 летом
        const month = now.getMonth();
        let sunsetHour = 18;
        if (month >= 4 && month <= 8) {
            sunsetHour = 21;
        } else if (month === 3 || month === 9) {
            sunsetHour = 19;
        }
        
        sunsetHour += offset;
        const sunriseHour = sunsetHour - 12;

        return hour >= sunsetHour || hour < sunriseHour;
    }

    shouldBeDarkBySystem() {
        return window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches;
    }

    switchTheme(theme) {
        const html = document.documentElement;
        
        if (this.settings.smoothTransition) {
            html.style.transition = 'background-color 1s ease, color 1s ease';
            setTimeout(() => {
                html.style.transition = '';
            }, 1000);
        }

        html.setAttribute('data-theme', theme);
        localStorage.setItem('theme', theme);

        // Обновляем иконку
        const icon = document.getElementById('themeIcon');
        if (icon) {
            icon.className = theme === 'dark' ? 'bi bi-sun-fill' : 'bi bi-moon-fill';
        }

        console.log(`[AutoThemeScheduler] Тема переключена на: ${theme}`);
    }

    updateStatus(modal) {
        const currentTheme = document.documentElement.getAttribute('data-theme') || 'light';
        const statusEl = modal.querySelector('#currentThemeStatus');
        const nextSwitchEl = modal.querySelector('#nextSwitchTime');

        if (statusEl) {
            statusEl.textContent = currentTheme === 'dark' ? 'Тёмная' : 'Светлая';
        }

        if (nextSwitchEl && this.settings.enabled) {
            const nextSwitch = this.getNextSwitchTime();
            nextSwitchEl.textContent = nextSwitch;
        }
    }

    getNextSwitchTime() {
        if (this.settings.mode === 'time') {
            const now = new Date();
            const currentTime = now.getHours() * 60 + now.getMinutes();
            
            const [lightH, lightM] = this.settings.lightStart.split(':').map(Number);
            const [darkH, darkM] = this.settings.darkStart.split(':').map(Number);
            
            const lightTime = lightH * 60 + lightM;
            const darkTime = darkH * 60 + darkM;

            let nextTime;
            if (currentTime < lightTime) {
                nextTime = `${this.settings.lightStart} (светлая)`;
            } else if (currentTime < darkTime) {
                nextTime = `${this.settings.darkStart} (тёмная)`;
            } else {
                nextTime = `${this.settings.lightStart} завтра (светлая)`;
            }

            return nextTime;
        } else if (this.settings.mode === 'system') {
            return 'Следует системным настройкам';
        } else {
            return 'На закате/рассвете';
        }
    }

    loadSettings() {
        const defaults = {
            enabled: false,
            mode: 'time',
            lightStart: '07:00',
            darkStart: '19:00',
            sunsetOffset: 0,
            smoothTransition: true
        };

        const saved = localStorage.getItem('theme_scheduler_settings');
        return saved ? { ...defaults, ...JSON.parse(saved) } : defaults;
    }

    showToast(message, type = 'info') {
        if (window.ChessCalendar && window.ChessCalendar.showToast) {
            window.ChessCalendar.showToast(message, type);
        }
    }
}

// Инициализация
document.addEventListener('DOMContentLoaded', () => {
    window.ChessCalendar = window.ChessCalendar || {};
    window.ChessCalendar.autoThemeScheduler = new AutoThemeScheduler();
});
