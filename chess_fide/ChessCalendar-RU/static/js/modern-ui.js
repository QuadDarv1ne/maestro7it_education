/**
 * Modern UI JavaScript
 * Интерактивность для современного интерфейса
 */

(function() {
    'use strict';
    
    // ============================================
    // NAVBAR SCROLL EFFECT
    // ============================================
    function initNavbarScroll() {
        const navbar = document.querySelector('.navbar-modern, .navbar');
        if (!navbar) return;
        
        let lastScroll = 0;
        
        window.addEventListener('scroll', () => {
            const currentScroll = window.pageYOffset;
            
            if (currentScroll > 50) {
                navbar.classList.add('scrolled');
            } else {
                navbar.classList.remove('scrolled');
            }
            
            // Hide navbar on scroll down, show on scroll up
            if (currentScroll > lastScroll && currentScroll > 100) {
                navbar.style.transform = 'translateY(-100%)';
            } else {
                navbar.style.transform = 'translateY(0)';
            }
            
            lastScroll = currentScroll;
        });
    }
    
    // ============================================
    // MOBILE MENU TOGGLE
    // ============================================
    function initMobileMenu() {
        const toggle = document.querySelector('.navbar-toggle-modern');
        const menu = document.querySelector('.navbar-mobile-menu-modern');
        
        if (!toggle || !menu) return;
        
        toggle.addEventListener('click', () => {
            toggle.classList.toggle('active');
            menu.classList.toggle('show');
            document.body.classList.toggle('modal-open');
        });
        
        // Close menu when clicking outside
        document.addEventListener('click', (e) => {
            if (!toggle.contains(e.target) && !menu.contains(e.target)) {
                toggle.classList.remove('active');
                menu.classList.remove('show');
                document.body.classList.remove('modal-open');
            }
        });
    }
    
    // ============================================
    // MODAL FUNCTIONALITY
    // ============================================
    function initModals() {
        // Open modal
        document.querySelectorAll('[data-modal-open]').forEach(btn => {
            btn.addEventListener('click', (e) => {
                e.preventDefault();
                const modalId = btn.getAttribute('data-modal-open');
                const modal = document.getElementById(modalId);
                if (modal) {
                    modal.classList.add('show');
                    document.body.classList.add('modal-open');
                }
            });
        });
        
        // Close modal
        document.querySelectorAll('.modal-close-modern, [data-modal-close]').forEach(btn => {
            btn.addEventListener('click', () => {
                const modal = btn.closest('.modal-modern');
                if (modal) {
                    modal.classList.remove('show');
                    document.body.classList.remove('modal-open');
                }
            });
        });
        
        // Close on backdrop click
        document.querySelectorAll('.modal-backdrop-modern').forEach(backdrop => {
            backdrop.addEventListener('click', () => {
                const modal = backdrop.closest('.modal-modern');
                if (modal) {
                    modal.classList.remove('show');
                    document.body.classList.remove('modal-open');
                }
            });
        });
        
        // Close on ESC key
        document.addEventListener('keydown', (e) => {
            if (e.key === 'Escape') {
                document.querySelectorAll('.modal-modern.show').forEach(modal => {
                    modal.classList.remove('show');
                    document.body.classList.remove('modal-open');
                });
            }
        });
    }
    
    // ============================================
    // FILTER PANEL TOGGLE
    // ============================================
    function initFilterPanel() {
        const toggles = document.querySelectorAll('.filter-panel-toggle-modern');
        
        toggles.forEach(toggle => {
            toggle.addEventListener('click', () => {
                const panel = toggle.closest('.filter-panel-modern');
                const body = panel.querySelector('.filter-panel-body-modern');
                
                if (body) {
                    body.classList.toggle('show');
                    toggle.querySelector('i').classList.toggle('bi-chevron-down');
                    toggle.querySelector('i').classList.toggle('bi-chevron-up');
                }
            });
        });
    }
    
    // ============================================
    // SEARCH AUTOCOMPLETE
    // ============================================
    function initSearchAutocomplete() {
        const searchInputs = document.querySelectorAll('.search-input-modern');
        
        searchInputs.forEach(input => {
            const dropdown = input.closest('.search-autocomplete-modern')
                ?.querySelector('.search-dropdown-modern');
            const clearBtn = input.closest('.search-input-wrapper-modern')
                ?.querySelector('.search-clear-modern');
            
            if (!dropdown) return;
            
            let debounceTimer;
            
            // Show dropdown on input
            input.addEventListener('input', () => {
                clearTimeout(debounceTimer);
                
                if (input.value.length >= 2) {
                    debounceTimer = setTimeout(() => {
                        dropdown.classList.add('show');
                        // Here you would typically fetch search results
                    }, 300);
                } else {
                    dropdown.classList.remove('show');
                }
            });
            
            // Clear button
            if (clearBtn) {
                clearBtn.addEventListener('click', () => {
                    input.value = '';
                    dropdown.classList.remove('show');
                    input.focus();
                });
            }
            
            // Hide dropdown on outside click
            document.addEventListener('click', (e) => {
                if (!input.contains(e.target) && !dropdown.contains(e.target)) {
                    dropdown.classList.remove('show');
                }
            });
            
            // Keyboard navigation
            input.addEventListener('keydown', (e) => {
                const items = dropdown.querySelectorAll('.search-result-item-modern');
                const activeItem = dropdown.querySelector('.search-result-item-modern.active');
                let index = Array.from(items).indexOf(activeItem);
                
                if (e.key === 'ArrowDown') {
                    e.preventDefault();
                    index = Math.min(index + 1, items.length - 1);
                    items.forEach(item => item.classList.remove('active'));
                    items[index]?.classList.add('active');
                    items[index]?.scrollIntoView({ block: 'nearest' });
                } else if (e.key === 'ArrowUp') {
                    e.preventDefault();
                    index = Math.max(index - 1, 0);
                    items.forEach(item => item.classList.remove('active'));
                    items[index]?.classList.add('active');
                    items[index]?.scrollIntoView({ block: 'nearest' });
                } else if (e.key === 'Enter' && activeItem) {
                    e.preventDefault();
                    activeItem.click();
                }
            });
        });
    }
    
    // ============================================
    // FAVORITE BUTTON
    // ============================================
    function initFavoriteButtons() {
        document.querySelectorAll('.tournament-favorite-btn-modern').forEach(btn => {
            btn.addEventListener('click', (e) => {
                e.preventDefault();
                e.stopPropagation();
                btn.classList.toggle('active');
                
                // Here you would typically send an API request
                const icon = btn.querySelector('i');
                if (btn.classList.contains('active')) {
                    icon.classList.remove('bi-heart');
                    icon.classList.add('bi-heart-fill');
                } else {
                    icon.classList.remove('bi-heart-fill');
                    icon.classList.add('bi-heart');
                }
            });
        });
    }
    
    // ============================================
    // LAZY LOADING IMAGES
    // ============================================
    function initLazyLoading() {
        if ('IntersectionObserver' in window) {
            const imageObserver = new IntersectionObserver((entries, observer) => {
                entries.forEach(entry => {
                    if (entry.isIntersecting) {
                        const img = entry.target;
                        img.src = img.dataset.src;
                        img.classList.remove('lazy');
                        observer.unobserve(img);
                    }
                });
            });
            
            document.querySelectorAll('img.lazy').forEach(img => {
                imageObserver.observe(img);
            });
        }
    }
    
    // ============================================
    // SMOOTH SCROLL
    // ============================================
    function initSmoothScroll() {
        document.querySelectorAll('a[href^="#"]').forEach(anchor => {
            anchor.addEventListener('click', function(e) {
                const href = this.getAttribute('href');
                if (href === '#') return;
                
                const target = document.querySelector(href);
                if (target) {
                    e.preventDefault();
                    target.scrollIntoView({
                        behavior: 'smooth',
                        block: 'start'
                    });
                }
            });
        });
    }
    
    // ============================================
    // TOAST NOTIFICATIONS
    // ============================================
    window.showToast = function(message, type = 'info', duration = 3000) {
        const toast = document.createElement('div');
        toast.className = `toast-modern toast-${type} animate-slide-in-right`;
        toast.innerHTML = `
            <div class="toast-icon-modern">
                <i class="bi bi-${type === 'success' ? 'check-circle' : type === 'error' ? 'x-circle' : 'info-circle'}"></i>
            </div>
            <div class="toast-content-modern">${message}</div>
            <button class="toast-close-modern">
                <i class="bi bi-x"></i>
            </button>
        `;
        
        document.body.appendChild(toast);
        
        // Position toast
        const toasts = document.querySelectorAll('.toast-modern');
        toast.style.bottom = `${20 + (toasts.length - 1) * 80}px`;
        
        // Close button
        toast.querySelector('.toast-close-modern').addEventListener('click', () => {
            toast.classList.add('animate-slide-out-right');
            setTimeout(() => toast.remove(), 300);
        });
        
        // Auto remove
        setTimeout(() => {
            toast.classList.add('animate-slide-out-right');
            setTimeout(() => toast.remove(), 300);
        }, duration);
    };
    
    // ============================================
    // INITIALIZE ALL
    // ============================================
    document.addEventListener('DOMContentLoaded', () => {
        initNavbarScroll();
        initMobileMenu();
        initModals();
        initFilterPanel();
        initSearchAutocomplete();
        initFavoriteButtons();
        initLazyLoading();
        initSmoothScroll();
        
        console.log('Modern UI initialized');
    });
    
})();
