// Keyboard Shortcuts - горячие клавиши для быстрой навигации

class KeyboardShortcuts {
    constructor() {
        this.shortcuts = {
            // Навигация
            'h': { action: () => window.location.href = '/', description: 'Главная страница' },
            'c': { action: () => window.location.href = '/calendar', description: 'Календарь' },
            'm': { action: () => window.location.href = '/map', description: 'Карта турниров' },
            's': { action: () => window.location.href = '/statistics', description: 'Статистика' },
            
            // Поиск и фильтры
            '/': { action: () => this.focusSearch(), description: 'Фокус на поиск' },
            'f': { action: () => this.toggleFilters(), description: 'Показать/скрыть фильтры' },
            'r': { action: () => this.resetFilters(), description: 'Сбросить фильтры' },
            
            // Функции
            'n': { action: () => this.openNotifications(), description: 'Уведомления' },
            'i': { action: () => this.openHistory(), description: 'История просмотров' },
            'p': { action: () => this.openStats(), description: 'Моя статистика' },
            'o': { action: () => this.openCompare(), description: 'Сравнение турниров' },
            
            // Утилиты
            't': { action: () => this.toggleTheme(), description: 'Переключить тему' },
            '?': { action: () => this.showHelp(), description: 'Показать справку' },
            'Escape': { action: () => this.closeModals(), description: 'Закрыть модальные окна' },
            
            // Прокрутка
            'g g': { action: () => this.scrollToTop(), description: 'Прокрутить наверх' },
            'g b': { action: () => this.scrollToBottom(), description: 'Прокрутить вниз' }
        };
        
        this.keySequence = '';
        this.sequenceTimeout = null;
        this.enabled = true;
        
        this.init();
    }

    init() {
        this.loadSettings();
        this.attachEventListeners();
        this.createHelpModal();
        this.showWelcomeHint();
    }

    loadSettings() {
        const stored = localStorage.getItem('keyboard_shortcuts_enabled');
        this.enabled = stored !== 'false';
    }

    saveSettings() {
        localStorage.setItem('keyboard_shortcuts_enabled', this.enabled);
    }

    attachEventListeners() {
        document.addEventListener('keydown', (e) => {
            if (!this.enabled) return;
            
            // Игнорируем, если фокус на input/textarea
            if (e.target.matches('input, textarea, select')) {
                // Кроме Escape
                if (e.key !== 'Escape') return;
            }
            
            this.handleKeyPress(e);
        });
    }

    handleKeyPress(e) {
        const key = e.key.toLowerCase();
        
        // Обработка последовательностей (например, "g g")
        if (this.keySequence) {
            const sequence = this.keySequence + ' ' + key;
            if (this.shortcuts[sequence]) {
                e.preventDefault();
                this.shortcuts[sequence].action();
                this.keySequence = '';
                clearTimeout(this.sequenceTimeout);
                return;
            }
        }
        
        // Начало последовательности
        if (key === 'g') {
            this.keySequence = 'g';
            this.sequenceTimeout = setTimeout(() => {
                this.keySequence = '';
            }, 1000);
            return;
        }
        
        // Одиночные клавиши
        if (this.shortcuts[key]) {
            e.preventDefault();
            this.shortcuts[key].action();
        }
    }

    focusSearch() {
        const searchInput = document.querySelector('#searchInput, input[type="search"]');
        if (searchInput) {
            searchInput.focus();
            searchInput.select();
        }
    }

    toggleFilters() {
        const filterSection = document.querySelector('.filter-form, .filters, #filters');
        if (filterSection) {
            filterSection.scrollIntoView({ behavior: 'smooth' });
            filterSection.classList.add('highlight-pulse');
            setTimeout(() => filterSection.classList.remove('highlight-pulse'), 2000);
        }
    }

    resetFilters() {
        window.location.href = window.location.pathname;
    }

    openNotifications() {
        if (window.smartNotifications) {
            window.smartNotifications.toggle();
        }
    }

    openHistory() {
        if (window.tournamentHistory) {
            window.tournamentHistory.toggle();
        }
    }

    openStats() {
        if (window.userStats) {
            window.userStats.openStatsModal();
        }
    }

    openCompare() {
        if (window.tournamentCompare) {
            window.tournamentCompare.openModal();
        }
    }

    toggleTheme() {
        if (typeof toggleTheme === 'function') {
            toggleTheme();
        }
    }

    closeModals() {
        // Закрываем все открытые модальные окна
        document.querySelectorAll('.modal.show').forEach(modal => {
            const bsModal = bootstrap.Modal.getInstance(modal);
            if (bsModal) bsModal.hide();
        });
        
        // Закрываем панели
        document.querySelectorAll('.panel.open, .widget.open').forEach(panel => {
            panel.classList.remove('open');
        });
    }

    scrollToTop() {
        window.scrollTo({ top: 0, behavior: 'smooth' });
    }

    scrollToBottom() {
        window.scrollTo({ top: document.body.scrollHeight, behavior: 'smooth' });
    }

    showHelp() {
        const modal = document.getElementById('shortcutsHelpModal');
        if (modal) {
            const bsModal = new bootstrap.Modal(modal);
            bsModal.show();
        }
    }

    createHelpModal() {
        // Проверяем, не создана ли уже модалка
        if (document.getElementById('shortcutsHelpModal')) return;

        const modal = document.createElement('div');
        modal.id = 'shortcutsHelpModal';
        modal.className = 'modal fade';
        modal.innerHTML = `
            <div class="modal-dialog modal-lg">
                <div class="modal-content">
                    <div class="modal-header">
                        <h5 class="modal-title">
                            <i class="bi bi-keyboard"></i> Горячие клавиши
                        </h5>
                        <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
                    </div>
                    <div class="modal-body">
                        ${this.renderShortcutsList()}
                    </div>
                    <div class="modal-footer">
                        <div class="form-check me-auto">
                            <input class="form-check-input" type="checkbox" id="enableShortcuts" 
                                   ${this.enabled ? 'checked' : ''} 
                                   onchange="keyboardShortcuts.toggleShortcuts(this.checked)">
                            <label class="form-check-label" for="enableShortcuts">
                                Включить горячие клавиши
                            </label>
                        </div>
                        <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">
                            Закрыть
                        </button>
                    </div>
                </div>
            </div>
        `;

        document.body.appendChild(modal);
    }

    renderShortcutsList() {
        const categories = {
            'Навигация': ['h', 'c', 'm', 's'],
            'Поиск и фильтры': ['/', 'f', 'r'],
            'Функции': ['n', 'i', 'p', 'o'],
            'Утилиты': ['t', '?', 'Escape'],
            'Прокрутка': ['g g', 'g b']
        };

        let html = '<div class="row g-3">';

        Object.entries(categories).forEach(([category, keys]) => {
            html += `
                <div class="col-md-6">
                    <h6 class="mb-3"><i class="bi bi-folder"></i> ${category}</h6>
                    <div class="list-group">
            `;

            keys.forEach(key => {
                const shortcut = this.shortcuts[key];
                if (shortcut) {
                    html += `
                        <div class="list-group-item d-flex justify-content-between align-items-center">
                            <span>${shortcut.description}</span>
                            <kbd class="bg-dark text-white px-2 py-1 rounded">${key}</kbd>
                        </div>
                    `;
                }
            });

            html += `
                    </div>
                </div>
            `;
        });

        html += '</div>';
        return html;
    }

    toggleShortcuts(enabled) {
        this.enabled = enabled;
        this.saveSettings();
        
        if (window.toast) {
            window.toast.success(enabled ? 'Горячие клавиши включены' : 'Горячие клавиши отключены');
        }
    }

    showWelcomeHint() {
        // Показываем подсказку только один раз
        if (localStorage.getItem('shortcuts_hint_shown')) return;

        setTimeout(() => {
            if (window.toast) {
                window.toast.info('Нажмите ? для просмотра горячих клавиш', 5000);
            }
            localStorage.setItem('shortcuts_hint_shown', 'true');
        }, 3000);
    }

    addCustomShortcut(key, action, description) {
        this.shortcuts[key] = { action, description };
    }
}

// Инициализация
const keyboardShortcuts = new KeyboardShortcuts();
window.keyboardShortcuts = keyboardShortcuts;

// Добавляем CSS для highlight-pulse
const style = document.createElement('style');
style.textContent = `
    @keyframes highlight-pulse {
        0%, 100% { box-shadow: 0 0 0 0 rgba(37, 99, 235, 0.7); }
        50% { box-shadow: 0 0 0 10px rgba(37, 99, 235, 0); }
    }
    
    .highlight-pulse {
        animation: highlight-pulse 1s ease-in-out 2;
    }
`;
document.head.appendChild(style);
