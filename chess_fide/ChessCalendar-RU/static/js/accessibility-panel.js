// Accessibility Panel - панель настроек доступности

class AccessibilityPanel {
    constructor() {
        this.settings = {
            fontSize: 'normal', // small, normal, large, xlarge
            contrast: 'normal', // normal, high
            animations: true,
            focusIndicator: true,
            keyboardNav: true,
            screenReader: false,
            dyslexiaFont: false,
            lineHeight: 'normal', // normal, increased
            letterSpacing: 'normal' // normal, increased
        };
        
        this.init();
    }

    init() {
        this.loadSettings();
        this.applySettings();
        this.createPanel();
        this.createToggleButton();
    }

    loadSettings() {
        const stored = localStorage.getItem('accessibility_settings');
        if (stored) {
            this.settings = { ...this.settings, ...JSON.parse(stored) };
        }
    }

    saveSettings() {
        localStorage.setItem('accessibility_settings', JSON.stringify(this.settings));
    }

    applySettings() {
        const root = document.documentElement;
        
        // Размер шрифта
        root.classList.remove('font-small', 'font-normal', 'font-large', 'font-xlarge');
        root.classList.add(`font-${this.settings.fontSize}`);
        
        // Контрастность
        root.classList.toggle('high-contrast', this.settings.contrast === 'high');
        
        // Анимации
        root.classList.toggle('reduce-motion', !this.settings.animations);
        
        // Индикатор фокуса
        root.classList.toggle('enhanced-focus', this.settings.focusIndicator);
        
        // Шрифт для дислексии
        root.classList.toggle('dyslexia-font', this.settings.dyslexiaFont);
        
        // Межстрочный интервал
        root.classList.toggle('increased-line-height', this.settings.lineHeight === 'increased');
        
        // Межбуквенный интервал
        root.classList.toggle('increased-letter-spacing', this.settings.letterSpacing === 'increased');
        
        // Применяем CSS
        this.injectStyles();
    }

    injectStyles() {
        // Удаляем старые стили если есть
        const oldStyle = document.getElementById('accessibility-styles');
        if (oldStyle) oldStyle.remove();
        
        const style = document.createElement('style');
        style.id = 'accessibility-styles';
        style.textContent = `
            /* Размеры шрифта */
            .font-small { font-size: 14px; }
            .font-normal { font-size: 16px; }
            .font-large { font-size: 18px; }
            .font-xlarge { font-size: 20px; }
            
            /* Высокая контрастность */
            .high-contrast {
                --bg-primary: #000000;
                --bg-secondary: #1a1a1a;
                --bg-tertiary: #2a2a2a;
                --text-primary: #ffffff;
                --text-secondary: #e0e0e0;
                --border-color: #ffffff;
            }
            
            .high-contrast .card,
            .high-contrast .modal-content {
                border: 2px solid #ffffff;
            }
            
            /* Уменьшение анимаций */
            .reduce-motion *,
            .reduce-motion *::before,
            .reduce-motion *::after {
                animation-duration: 0.01ms !important;
                animation-iteration-count: 1 !important;
                transition-duration: 0.01ms !important;
            }
            
            /* Улучшенный индикатор фокуса */
            .enhanced-focus *:focus {
                outline: 3px solid #2563eb !important;
                outline-offset: 3px !important;
                box-shadow: 0 0 0 5px rgba(37, 99, 235, 0.3) !important;
            }
            
            /* Шрифт для дислексии */
            .dyslexia-font * {
                font-family: 'OpenDyslexic', 'Comic Sans MS', sans-serif !important;
            }
            
            /* Увеличенный межстрочный интервал */
            .increased-line-height * {
                line-height: 1.8 !important;
            }
            
            /* Увеличенный межбуквенный интервал */
            .increased-letter-spacing * {
                letter-spacing: 0.12em !important;
            }
            
            /* Скрытие для скринридеров */
            .sr-only {
                position: absolute;
                width: 1px;
                height: 1px;
                padding: 0;
                margin: -1px;
                overflow: hidden;
                clip: rect(0, 0, 0, 0);
                white-space: nowrap;
                border: 0;
            }
        `;
        
        document.head.appendChild(style);
    }

    createToggleButton() {
        // Проверяем, не создана ли уже кнопка
        if (document.getElementById('a11yToggleBtn')) return;
        
        const button = document.createElement('button');
        button.id = 'a11yToggleBtn';
        button.className = 'a11y-toggle-btn';
        button.setAttribute('aria-label', 'Открыть панель доступности');
        button.innerHTML = `
            <style>
                .a11y-toggle-btn {
                    position: fixed;
                    right: 30px;
                    top: 50%;
                    transform: translateY(-50%);
                    width: 50px;
                    height: 50px;
                    border-radius: 50%;
                    background: linear-gradient(135deg, #8b5cf6 0%, #7c3aed 100%);
                    color: white;
                    border: none;
                    box-shadow: 0 4px 12px rgba(139, 92, 246, 0.4);
                    cursor: pointer;
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    font-size: 1.5rem;
                    z-index: 997;
                    transition: all 0.3s ease;
                }
                
                .a11y-toggle-btn:hover {
                    transform: translateY(-50%) scale(1.1);
                    box-shadow: 0 6px 20px rgba(139, 92, 246, 0.6);
                }
                
                @media (max-width: 768px) {
                    .a11y-toggle-btn {
                        right: 15px;
                        width: 45px;
                        height: 45px;
                        font-size: 1.25rem;
                    }
                }
            </style>
            <i class="bi bi-universal-access"></i>
        `;
        
        button.addEventListener('click', () => this.toggle());
        document.body.appendChild(button);
    }

    createPanel() {
        // Проверяем, не создана ли уже панель
        if (document.getElementById('a11yPanel')) return;
        
        const panel = document.createElement('div');
        panel.id = 'a11yPanel';
        panel.innerHTML = `
            <style>
                #a11yPanel {
                    position: fixed;
                    right: -400px;
                    top: 0;
                    width: 400px;
                    height: 100vh;
                    background: var(--bg-primary);
                    box-shadow: -4px 0 20px rgba(0, 0, 0, 0.15);
                    z-index: 9999;
                    transition: right 0.3s ease;
                    overflow-y: auto;
                    display: flex;
                    flex-direction: column;
                }
                
                #a11yPanel.open {
                    right: 0;
                }
                
                .a11y-header {
                    padding: 1.5rem;
                    background: linear-gradient(135deg, #8b5cf6 0%, #7c3aed 100%);
                    color: white;
                    display: flex;
                    justify-content: space-between;
                    align-items: center;
                }
                
                .a11y-header h5 {
                    margin: 0;
                    font-weight: 700;
                    display: flex;
                    align-items: center;
                    gap: 0.5rem;
                }
                
                .a11y-content {
                    flex: 1;
                    padding: 1.5rem;
                    overflow-y: auto;
                }
                
                .a11y-section {
                    margin-bottom: 2rem;
                }
                
                .a11y-section-title {
                    font-weight: 700;
                    margin-bottom: 1rem;
                    color: var(--text-primary);
                    display: flex;
                    align-items: center;
                    gap: 0.5rem;
                }
                
                .a11y-option {
                    margin-bottom: 1.25rem;
                    padding-bottom: 1.25rem;
                    border-bottom: 1px solid var(--border-color);
                }
                
                .a11y-option:last-child {
                    border-bottom: none;
                }
                
                .a11y-option-label {
                    font-weight: 600;
                    margin-bottom: 0.5rem;
                    color: var(--text-primary);
                }
                
                .a11y-option-description {
                    font-size: 0.875rem;
                    color: var(--text-secondary);
                    margin-bottom: 0.75rem;
                }
                
                .a11y-buttons {
                    display: flex;
                    gap: 0.5rem;
                    flex-wrap: wrap;
                }
                
                .a11y-btn {
                    padding: 0.5rem 1rem;
                    border: 2px solid var(--border-color);
                    background: var(--bg-secondary);
                    color: var(--text-primary);
                    border-radius: 8px;
                    cursor: pointer;
                    font-weight: 600;
                    transition: all 0.2s ease;
                }
                
                .a11y-btn:hover {
                    border-color: var(--primary-color);
                    background: var(--primary-color);
                    color: white;
                }
                
                .a11y-btn.active {
                    border-color: var(--primary-color);
                    background: var(--primary-color);
                    color: white;
                }
                
                .a11y-toggle {
                    display: flex;
                    align-items: center;
                    gap: 0.75rem;
                }
                
                .a11y-footer {
                    padding: 1rem 1.5rem;
                    border-top: 2px solid var(--border-color);
                    display: flex;
                    gap: 0.5rem;
                }
                
                @media (max-width: 768px) {
                    #a11yPanel {
                        width: 100%;
                        right: -100%;
                    }
                    
                    #a11yPanel.open {
                        right: 0;
                    }
                }
            </style>
            
            <div class="a11y-header">
                <h5><i class="bi bi-universal-access"></i> Доступность</h5>
                <button class="btn btn-link text-white p-0" onclick="accessibilityPanel.toggle()">
                    <i class="bi bi-x-lg"></i>
                </button>
            </div>
            
            <div class="a11y-content">
                ${this.renderOptions()}
            </div>
            
            <div class="a11y-footer">
                <button class="btn btn-secondary flex-1" onclick="accessibilityPanel.reset()">
                    <i class="bi bi-arrow-clockwise"></i> Сбросить
                </button>
                <button class="btn btn-primary flex-1" onclick="accessibilityPanel.toggle()">
                    <i class="bi bi-check"></i> Применить
                </button>
            </div>
        `;
        
        document.body.appendChild(panel);
    }

    renderOptions() {
        return `
            <div class="a11y-section">
                <div class="a11y-section-title">
                    <i class="bi bi-type"></i> Размер текста
                </div>
                <div class="a11y-option">
                    <div class="a11y-option-label">Размер шрифта</div>
                    <div class="a11y-option-description">Выберите комфортный размер текста</div>
                    <div class="a11y-buttons">
                        <button class="a11y-btn ${this.settings.fontSize === 'small' ? 'active' : ''}" 
                                onclick="accessibilityPanel.setSetting('fontSize', 'small')">
                            Маленький
                        </button>
                        <button class="a11y-btn ${this.settings.fontSize === 'normal' ? 'active' : ''}" 
                                onclick="accessibilityPanel.setSetting('fontSize', 'normal')">
                            Обычный
                        </button>
                        <button class="a11y-btn ${this.settings.fontSize === 'large' ? 'active' : ''}" 
                                onclick="accessibilityPanel.setSetting('fontSize', 'large')">
                            Большой
                        </button>
                        <button class="a11y-btn ${this.settings.fontSize === 'xlarge' ? 'active' : ''}" 
                                onclick="accessibilityPanel.setSetting('fontSize', 'xlarge')">
                            Очень большой
                        </button>
                    </div>
                </div>
            </div>
            
            <div class="a11y-section">
                <div class="a11y-section-title">
                    <i class="bi bi-eye"></i> Визуальные настройки
                </div>
                <div class="a11y-option">
                    <div class="a11y-option-label">Контрастность</div>
                    <div class="a11y-option-description">Увеличьте контраст для лучшей читаемости</div>
                    <div class="a11y-buttons">
                        <button class="a11y-btn ${this.settings.contrast === 'normal' ? 'active' : ''}" 
                                onclick="accessibilityPanel.setSetting('contrast', 'normal')">
                            Обычная
                        </button>
                        <button class="a11y-btn ${this.settings.contrast === 'high' ? 'active' : ''}" 
                                onclick="accessibilityPanel.setSetting('contrast', 'high')">
                            Высокая
                        </button>
                    </div>
                </div>
                
                <div class="a11y-option">
                    <div class="a11y-option-label">Межстрочный интервал</div>
                    <div class="a11y-option-description">Увеличьте расстояние между строками</div>
                    <div class="a11y-buttons">
                        <button class="a11y-btn ${this.settings.lineHeight === 'normal' ? 'active' : ''}" 
                                onclick="accessibilityPanel.setSetting('lineHeight', 'normal')">
                            Обычный
                        </button>
                        <button class="a11y-btn ${this.settings.lineHeight === 'increased' ? 'active' : ''}" 
                                onclick="accessibilityPanel.setSetting('lineHeight', 'increased')">
                            Увеличенный
                        </button>
                    </div>
                </div>
                
                <div class="a11y-option">
                    <div class="a11y-option-label">Межбуквенный интервал</div>
                    <div class="a11y-option-description">Увеличьте расстояние между буквами</div>
                    <div class="a11y-buttons">
                        <button class="a11y-btn ${this.settings.letterSpacing === 'normal' ? 'active' : ''}" 
                                onclick="accessibilityPanel.setSetting('letterSpacing', 'normal')">
                            Обычный
                        </button>
                        <button class="a11y-btn ${this.settings.letterSpacing === 'increased' ? 'active' : ''}" 
                                onclick="accessibilityPanel.setSetting('letterSpacing', 'increased')">
                            Увеличенный
                        </button>
                    </div>
                </div>
            </div>
            
            <div class="a11y-section">
                <div class="a11y-section-title">
                    <i class="bi bi-gear"></i> Дополнительно
                </div>
                <div class="a11y-option">
                    <div class="a11y-toggle">
                        <input type="checkbox" id="animationsToggle" 
                               ${this.settings.animations ? 'checked' : ''}
                               onchange="accessibilityPanel.setSetting('animations', this.checked)">
                        <label for="animationsToggle">
                            <div class="a11y-option-label">Анимации</div>
                            <div class="a11y-option-description">Включить анимации интерфейса</div>
                        </label>
                    </div>
                </div>
                
                <div class="a11y-option">
                    <div class="a11y-toggle">
                        <input type="checkbox" id="focusToggle" 
                               ${this.settings.focusIndicator ? 'checked' : ''}
                               onchange="accessibilityPanel.setSetting('focusIndicator', this.checked)">
                        <label for="focusToggle">
                            <div class="a11y-option-label">Улучшенный индикатор фокуса</div>
                            <div class="a11y-option-description">Более заметная рамка фокуса</div>
                        </label>
                    </div>
                </div>
                
                <div class="a11y-option">
                    <div class="a11y-toggle">
                        <input type="checkbox" id="dyslexiaToggle" 
                               ${this.settings.dyslexiaFont ? 'checked' : ''}
                               onchange="accessibilityPanel.setSetting('dyslexiaFont', this.checked)">
                        <label for="dyslexiaToggle">
                            <div class="a11y-option-label">Шрифт для дислексии</div>
                            <div class="a11y-option-description">Специальный шрифт для людей с дислексией</div>
                        </label>
                    </div>
                </div>
            </div>
        `;
    }

    setSetting(key, value) {
        this.settings[key] = value;
        this.saveSettings();
        this.applySettings();
        
        // Обновляем панель
        const content = document.querySelector('.a11y-content');
        if (content) {
            content.innerHTML = this.renderOptions();
        }
    }

    toggle() {
        const panel = document.getElementById('a11yPanel');
        if (panel) {
            panel.classList.toggle('open');
        }
    }

    reset() {
        if (confirm('Сбросить все настройки доступности?')) {
            this.settings = {
                fontSize: 'normal',
                contrast: 'normal',
                animations: true,
                focusIndicator: true,
                keyboardNav: true,
                screenReader: false,
                dyslexiaFont: false,
                lineHeight: 'normal',
                letterSpacing: 'normal'
            };
            
            this.saveSettings();
            this.applySettings();
            
            // Обновляем панель
            const content = document.querySelector('.a11y-content');
            if (content) {
                content.innerHTML = this.renderOptions();
            }
            
            if (window.toast) {
                window.toast.success('Настройки доступности сброшены');
            }
        }
    }
}

// Инициализация
const accessibilityPanel = new AccessibilityPanel();
window.accessibilityPanel = accessibilityPanel;
