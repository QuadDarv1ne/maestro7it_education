// Theme Switcher for Chess Calendar RU

class ThemeSwitcher {
    constructor() {
        this.theme = localStorage.getItem('theme') || 'light';
        this.init();
    }

    init() {
        // Apply saved theme
        this.applyTheme(this.theme);
        
        // Create theme toggle button
        this.createToggleButton();
        
        // Listen for system theme changes
        this.watchSystemTheme();
    }

    applyTheme(theme) {
        document.documentElement.setAttribute('data-theme', theme);
        localStorage.setItem('theme', theme);
        this.theme = theme;
        
        // Update button icon if exists
        const icon = document.getElementById('themeIcon');
        if (icon) {
            icon.className = theme === 'dark' ? 'bi bi-sun-fill' : 'bi bi-moon-fill';
        }
    }

    toggleTheme() {
        const newTheme = this.theme === 'light' ? 'dark' : 'light';
        this.applyTheme(newTheme);
        
        // Track achievement
        if (window.achievementsSystem) {
            window.achievementsSystem.trackAction('theme_switched');
        }
        
        // Add animation
        document.body.style.transition = 'background-color 0.3s ease, color 0.3s ease';
        setTimeout(() => {
            document.body.style.transition = '';
        }, 300);
    }

    createToggleButton() {
        // Check if button already exists
        if (document.getElementById('themeToggle')) return;
        
        // Find navbar or create container
        const navbar = document.querySelector('.navbar .container');
        if (!navbar) return;
        
        // Create button
        const button = document.createElement('button');
        button.id = 'themeToggle';
        button.className = 'btn btn-link text-white';
        button.setAttribute('aria-label', 'Toggle theme');
        button.innerHTML = `<i id="themeIcon" class="${this.theme === 'dark' ? 'bi bi-sun-fill' : 'bi bi-moon-fill'}"></i>`;
        button.style.cssText = 'font-size: 1.2rem; padding: 0.5rem;';
        
        button.addEventListener('click', () => this.toggleTheme());
        
        // Add to navbar
        const navbarEnd = navbar.querySelector('.d-flex') || navbar;
        navbarEnd.appendChild(button);
    }

    watchSystemTheme() {
        if (!window.matchMedia) return;
        
        const darkModeQuery = window.matchMedia('(prefers-color-scheme: dark)');
        darkModeQuery.addEventListener('change', (e) => {
            // Only auto-switch if user hasn't manually set a preference
            if (!localStorage.getItem('theme')) {
                this.applyTheme(e.matches ? 'dark' : 'light');
            }
        });
    }

    // Public method to get current theme
    getCurrentTheme() {
        return this.theme;
    }
}

// Initialize theme switcher when DOM is ready
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', () => {
        window.themeSwitcher = new ThemeSwitcher();
    });
} else {
    window.themeSwitcher = new ThemeSwitcher();
}
