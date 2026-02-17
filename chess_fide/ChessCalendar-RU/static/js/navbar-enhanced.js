/**
 * Enhanced Navbar JavaScript
 * Функциональность для улучшенного navbar
 */

(function() {
    'use strict';
    
    // Mobile menu toggle
    const mobileMenuToggle = document.getElementById('mobileMenuToggle');
    const mobileMenu = document.getElementById('mobileMenu');
    
    if (mobileMenuToggle && mobileMenu) {
        mobileMenuToggle.addEventListener('click', () => {
            mobileMenu.classList.toggle('show');
            const icon = mobileMenuToggle.querySelector('i');
            icon.classList.toggle('bi-list');
            icon.classList.toggle('bi-x-lg');
        });
        
        // Close mobile menu when clicking outside
        document.addEventListener('click', (e) => {
            if (!mobileMenuToggle.contains(e.target) && !mobileMenu.contains(e.target)) {
                mobileMenu.classList.remove('show');
                const icon = mobileMenuToggle.querySelector('i');
                icon.classList.remove('bi-x-lg');
                icon.classList.add('bi-list');
            }
        });
        
        // Close mobile menu when clicking on a link
        mobileMenu.querySelectorAll('.nav-link-enhanced').forEach(link => {
            link.addEventListener('click', () => {
                mobileMenu.classList.remove('show');
                const icon = mobileMenuToggle.querySelector('i');
                icon.classList.remove('bi-x-lg');
                icon.classList.add('bi-list');
            });
        });
    }
    
    // Navbar scroll effect
    const navbar = document.querySelector('.navbar-enhanced');
    if (navbar) {
        let lastScroll = 0;
        
        window.addEventListener('scroll', () => {
            const currentScroll = window.pageYOffset;
            
            if (currentScroll > 50) {
                navbar.classList.add('scrolled');
            } else {
                navbar.classList.remove('scrolled');
            }
            
            lastScroll = currentScroll;
        });
    }
    
    // Search functionality
    function initSearch(inputId, clearId) {
        const searchInput = document.getElementById(inputId);
        const searchClear = document.getElementById(clearId);
        
        if (!searchInput || !searchClear) return;
        
        // Clear button
        searchClear.addEventListener('click', () => {
            searchInput.value = '';
            searchInput.focus();
        });
        
        // Search on Enter
        searchInput.addEventListener('keypress', (e) => {
            if (e.key === 'Enter') {
                const query = searchInput.value.trim();
                if (query) {
                    window.location.href = `/?search=${encodeURIComponent(query)}`;
                }
            }
        });
        
        // Live search (optional - можно включить позже)
        let searchTimeout;
        searchInput.addEventListener('input', () => {
            clearTimeout(searchTimeout);
            const query = searchInput.value.trim();
            
            if (query.length >= 2) {
                searchTimeout = setTimeout(() => {
                    performLiveSearch(query);
                }, 300);
            }
        });
    }
    
    // Initialize search for both desktop and mobile
    initSearch('navbarSearchInput', 'navbarSearchClear');
    initSearch('mobileSearchInput', 'mobileSearchClear');
    
    // Live search function
    function performLiveSearch(query) {
        // Здесь можно добавить AJAX запрос для живого поиска
        // Пока просто логируем
        console.log('Searching for:', query);
        
        // Пример AJAX запроса:
        /*
        fetch(`/api/tournaments/search?q=${encodeURIComponent(query)}`)
            .then(response => response.json())
            .then(data => {
                // Показать результаты в dropdown
                showSearchResults(data);
            })
            .catch(error => {
                console.error('Search error:', error);
            });
        */
    }
    
    // Show search results dropdown
    function showSearchResults(results) {
        // Создать и показать dropdown с результатами
        // Реализация зависит от дизайна
    }
    
})();
