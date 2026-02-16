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
        
        this.storageKey = 'accessibility_settings';
        this.init();
    }

    init() {
        this.loadSettings();
        this.applySettings();
        this.createPanel();
        this.createToggleButton();
    }

    loadSettings() {
        const stored = localStorage.getItem(this.storageKey);
        if (stored) {
            this.settings = { ...this.settings, ...JSON.parse(stored) };
        }
    }

    saveSettings() {
        localStorage.setItem(this.storageKey, JSON.stringify(this.settings));
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
                --text-primary: #ffffff;
                --text-secondary: #e0e0e0;
                --border-color: #ffffff;
            }
            
            .high-contrast .card,
            .high-contrast .modal-content {
                border: 2px solid #ffffff;
            }
            
            /* Уменьшение анимаций */
            .reduce-motion * {
                animation-duration: 0.01ms !important;
                animation-iteration-count: 1 !important;
                transition-duration: 0.01ms !important;
            }
            
            /* Усиленный индикатор фокуса */
            .enhanced-focus *:focus {
                outline: 3px solid #2563eb !important;
                outline-offset: 3px !important;
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
                letter-spacing: 0.1em !important;
            }
        `;
        
        document.head.appendChild(style);
    }

    createPanel() {
        // Проверяем, не создана ли уже панель
        if (document.getElementById('accessibilityPanel')) return;
        
        const panel = document.createElement('div');
        panel.id = 'accessibilityPanel';
        panel.innerHTML = `
            <style>
                #accessibilityPanel {
                    position: fixed;
                    right: -400px;
                    top: 70px;
                    bottom: 0;
                    width: 400px;
                    background: var(--bg-primary);
                    box-shadow: -4px 0 20px rgba(0, 0, 0, 