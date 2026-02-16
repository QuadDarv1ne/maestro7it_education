// ChessCalendar-RU - UI Features Bundle
// Consolidated UI functionality for optimized loading

// Import utilities
import { debounce, throttle } from './utils.js';

// Theme switcher functionality
export class ThemeSwitcher {
    constructor() {
        this.currentTheme = localStorage.getItem('theme') || 'light';
        this.init();
    }

    init() {
        // Set initial theme
        document.documentElement.setAttribute('data-theme', this.currentTheme);
        this.updateThemeIcon();
        
        // Listen for theme changes
        document.addEventListener('DOMContentLoaded', () => {
            const themeToggle = document.getElementById('themeToggle');
            if (themeToggle) {
                themeToggle.addEventListener('click', () => this.toggleTheme());
            }
        });
    }

    toggleTheme() {
        this.currentTheme = this.currentTheme === 'dark' ? 'light' : 'dark';
        document.documentElement.setAttribute('data-theme', this.currentTheme);
        localStorage.setItem('theme', this.currentTheme);
        this.updateThemeIcon();
        
        // Dispatch theme change event
        document.dispatchEvent(new CustomEvent('themeChanged', {
            detail: { theme: this.currentTheme }
        }));
    }

    updateThemeIcon() {
        const icon = document.getElementById('themeIcon');
        if (icon) {
            icon.className = this.currentTheme === 'dark' ? 'bi bi-sun-fill' : 'bi bi-moon-fill';
        }
    }
}

// Back to top button functionality
export class BackToTop {
    constructor() {
        this.button = null;
        this.init();
    }

    init() {
        // Create button
        this.button = document.createElement('button');
        this.button.id = 'backToTop';
        this.button.className = 'btn btn-primary';
        this.button.innerHTML = '<i class="bi bi-arrow-up"></i>';
        this.button.style.cssText = `
            position: fixed;
            bottom: 30px;
            right: 30px;
            z-index: 999;
            display: none;
            width: 50px;
            height: 50px;
            border-radius: 50%;
            box-shadow: 0 4px 12px rgba(37, 99, 235, 0.4);
            transition: all 0.3s ease;
        `;

        document.body.appendChild(this.button);

        // Add click handler
        this.button.addEventListener('click', () => {
            window.scrollTo({
                top: 0,
                behavior: 'smooth'
            });
        });

        // Add scroll listener
        window.addEventListener('scroll', throttle(() => {
            if (window.pageYOffset > 300) {
                this.button.style.display = 'block';
            } else {
                this.button.style.display = 'none';
            }
        }, 100));
    }
}

// Smooth scrolling for anchor links
export class SmoothScroll {
    constructor() {
        this.init();
    }

    init() {
        document.querySelectorAll('a[href^="#"]').forEach(anchor => {
            anchor.addEventListener('click', function (e) {
                const href = this.getAttribute('href');
                if (href !== '#' && href !== '#!') {
                    e.preventDefault();
                    const target = document.querySelector(href);
                    if (target) {
                        target.scrollIntoView({
                            behavior: 'smooth',
                            block: 'start'
                        });
                    }
                }
            });
        });
    }
}

// Tooltip and popover initialization
export class UIInitialization {
    constructor() {
        this.init();
    }

    init() {
        // Initialize tooltips
        document.addEventListener('DOMContentLoaded', () => {
            this.initTooltips();
            this.initPopovers();
        });
    }

    initTooltips() {
        if (typeof bootstrap !== 'undefined') {
            const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
            tooltipTriggerList.map(function (tooltipTriggerEl) {
                return new bootstrap.Tooltip(tooltipTriggerEl);
            });
        }
    }

    initPopovers() {
        if (typeof bootstrap !== 'undefined') {
            const popoverTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="popover"]'));
            popoverTriggerList.map(function (popoverTriggerEl) {
                return new bootstrap.Popover(popoverTriggerEl);
            });
        }
    }
}

// Card animations
export class CardAnimations {
    constructor() {
        this.animateOnLoad();
    }

    animateOnLoad() {
        document.addEventListener('DOMContentLoaded', () => {
            const cards = document.querySelectorAll('.card, .tournament-card');
            cards.forEach((card, index) => {
                card.style.opacity = '0';
                card.style.transform = 'translateY(20px)';
                card.style.transition = 'all 0.5s ease';
                
                setTimeout(() => {
                    card.style.opacity = '1';
                    card.style.transform = 'translateY(0)';
                }, index * 50);
            });
        });
    }
}

// Mobile UI enhancements
export class MobileUI {
    constructor() {
        this.init();
    }

    init() {
        document.addEventListener('DOMContentLoaded', () => {
            this.initMobileNavigation();
            this.initTouchGestures();
            this.initPullToRefresh();
        });
    }

    initMobileNavigation() {
        const hamburger = document.querySelector('.hamburger');
        const navbarCollapse = document.querySelector('.navbar-collapse');
        
        if (hamburger) {
            hamburger.addEventListener('click', function() {
                hamburger.classList.toggle('active');
                
                if (navbarCollapse) {
                    navbarCollapse.classList.toggle('show');
                }
            });
        }
    }

    initTouchGestures() {
        // Touch swipe gestures for tournament cards
        let touchStartX = 0;
        let touchEndX = 0;
        
        const tournamentCards = document.querySelectorAll('.tournament-card');
        
        tournamentCards.forEach(card => {
            card.addEventListener('touchstart', e => {
                touchStartX = e.changedTouches[0].screenX;
            });
            
            card.addEventListener('touchend', e => {
                touchEndX = e.changedTouches[0].screenX;
                this.handleSwipe(card, touchStartX, touchEndX);
            });
        });
    }

    handleSwipe(element, startX, endX) {
        const threshold = 50; // Minimum distance for swipe
        const diff = startX - endX;
        
        if (Math.abs(diff) > threshold) {
            if (diff > 0) {
                // Swipe left - next item
                console.log('Swiped left on', element);
            } else {
                // Swipe right - previous item
                console.log('Swiped right on', element);
            }
        }
    }

    initPullToRefresh() {
        let startY = 0;
        let currentY = 0;
        let pullDistance = 0;
        const pullToRefreshElement = document.querySelector('.pull-to-refresh');
        
        if (pullToRefreshElement) {
            document.addEventListener('touchstart', e => {
                if (window.scrollY === 0) {
                    startY = e.touches[0].pageY;
                }
            });
            
            document.addEventListener('touchmove', e => {
                if (startY > 0) {
                    currentY = e.touches[0].pageY;
                    pullDistance = currentY - startY;
                    
                    if (pullDistance > 0) {
                        e.preventDefault();
                        pullToRefreshElement.style.transform = `translateY(${Math.min(pullDistance / 2, 60)}px)`;
                    }
                }
            });
            
            document.addEventListener('touchend', () => {
                if (pullDistance > 60) {
                    // Trigger refresh
                    pullToRefreshElement.classList.add('active');
                    setTimeout(() => {
                        location.reload();
                    }, 1000);
                } else {
                    // Reset
                    pullToRefreshElement.style.transform = 'translateY(-100%)';
                }
                
                startY = 0;
                currentY = 0;
                pullDistance = 0;
            });
        }
    }
}

// Form validation enhancement
export class FormValidation {
    constructor() {
        this.enhanceFormValidation();
    }

    enhanceFormValidation() {
        const forms = document.querySelectorAll('.needs-validation');
        
        Array.from(forms).forEach(form => {
            form.addEventListener('submit', event => {
                if (!form.checkValidity()) {
                    event.preventDefault();
                    event.stopPropagation();
                    
                    // Show first error
                    const firstInvalid = form.querySelector(':invalid');
                    if (firstInvalid) {
                        firstInvalid.focus();
                        
                        // Import showToast from utils if available
                        if (typeof showToast !== 'undefined') {
                            showToast('Пожалуйста, заполните все обязательные поля', 'warning');
                        }
                    }
                }
                
                form.classList.add('was-validated');
            }, false);
        });
    }
}

// Initialize all UI features when DOM is ready
document.addEventListener('DOMContentLoaded', () => {
    window.themeSwitcher = new ThemeSwitcher();
    window.backToTop = new BackToTop();
    window.smoothScroll = new SmoothScroll();
    window.uiInit = new UIInitialization();
    window.cardAnimations = new CardAnimations();
    window.mobileUI = new MobileUI();
    window.formValidation = new FormValidation();
});

// Export all UI features
export default {
    ThemeSwitcher,
    BackToTop,
    SmoothScroll,
    UIInitialization,
    CardAnimations,
    MobileUI,
    FormValidation,
    debounce,
    throttle
};