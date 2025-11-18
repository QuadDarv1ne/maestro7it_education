/**
 * Theme Switcher - Dark/Light Mode
 */
class ThemeSwitcher {
    constructor() {
        this.currentTheme = localStorage.getItem('theme') || 'light';
        this.init();
    }

    init() {
        // Apply saved theme
        this.applyTheme(this.currentTheme);
        
        // Create theme toggle button if not exists
        this.createToggleButton();
        
        // Listen for system theme changes
        if (window.matchMedia) {
            window.matchMedia('(prefers-color-scheme: dark)').addEventListener('change', e => {
                if (!localStorage.getItem('theme')) {
                    this.setTheme(e.matches ? 'dark' : 'light');
                }
            });
        }
    }

    createToggleButton() {
        const existingButton = document.getElementById('theme-toggle');
        if (existingButton) return;

        const button = document.createElement('button');
        button.id = 'theme-toggle';
        button.className = 'btn btn-link nav-link';
        button.setAttribute('aria-label', 'Переключить тему');
        button.setAttribute('title', 'Переключить тему');
        button.innerHTML = this.currentTheme === 'dark' 
            ? '<i class="bi bi-sun-fill"></i>' 
            : '<i class="bi bi-moon-fill"></i>';
        
        button.addEventListener('click', () => this.toggleTheme());

        // Try to add to navbar
        const navbar = document.querySelector('.navbar-nav');
        if (navbar) {
            const li = document.createElement('li');
            li.className = 'nav-item';
            li.appendChild(button);
            navbar.insertBefore(li, navbar.firstChild);
        }
    }

    toggleTheme() {
        const newTheme = this.currentTheme === 'light' ? 'dark' : 'light';
        this.setTheme(newTheme);
    }

    setTheme(theme) {
        this.currentTheme = theme;
        this.applyTheme(theme);
        localStorage.setItem('theme', theme);
        
        // Update button icon
        const button = document.getElementById('theme-toggle');
        if (button) {
            button.innerHTML = theme === 'dark' 
                ? '<i class="bi bi-sun-fill"></i>' 
                : '<i class="bi bi-moon-fill"></i>';
        }
        
        // Dispatch event for other components
        document.dispatchEvent(new CustomEvent('themeChanged', { detail: { theme } }));
    }

    applyTheme(theme) {
        document.documentElement.setAttribute('data-theme', theme);
        
        if (theme === 'dark') {
            document.body.classList.add('dark-mode');
        } else {
            document.body.classList.remove('dark-mode');
        }
    }

    getTheme() {
        return this.currentTheme;
    }
}

// Initialize theme switcher
const themeSwitcher = new ThemeSwitcher();

// Export for use in other scripts
window.themeSwitcher = themeSwitcher;
