// ChessCalendar-RU - Main JavaScript with Lazy Loading Support
// Updated to work with lazy loading system and PWA enhancements

// Loading Spinner
function showLoader() {
    const loader = document.createElement('div');
    loader.id = 'globalLoader';
    loader.innerHTML = `
        <div style="position: fixed; top: 0; left: 0; width: 100%; height: 100%; 
                    background: rgba(0,0,0,0.5); z-index: 9999; 
                    display: flex; align-items: center; justify-content: center;">
            <div class="spinner-border text-light" style="width: 3rem; height: 3rem;" role="status">
                <span class="visually-hidden">Загрузка...</span>
            </div>
        </div>
    `;
    document.body.appendChild(loader);
}

function hideLoader() {
    const loader = document.getElementById('globalLoader');
    if (loader) {
        loader.remove();
    }
}

// Toast Notifications
function showToast(message, type = 'info', duration = 5000) {
    const toastContainer = document.getElementById('toastContainer') || createToastContainer();
    
    const toast = document.createElement('div');
    toast.className = `toast align-items-center text-white bg-${type} border-0`;
    toast.setAttribute('role', 'alert');
    toast.setAttribute('aria-live', 'assertive');
    toast.setAttribute('aria-atomic', 'true');
    
    toast.innerHTML = `
        <div class="d-flex">
            <div class="toast-body">
                <i class="bi bi-${getIconForType(type)}"></i> ${message}
            </div>
            <button type="button" class="btn-close btn-close-white me-2 m-auto" data-bs-dismiss="toast"></button>
        </div>
    `;
    
    toastContainer.appendChild(toast);
    
    const bsToast = new bootstrap.Toast(toast, { delay: duration });
    bsToast.show();
    
    toast.addEventListener('hidden.bs.toast', () => {
        toast.remove();
    });
}

function createToastContainer() {
    const container = document.createElement('div');
    container.id = 'toastContainer';
    container.className = 'toast-container position-fixed top-0 end-0 p-3';
    container.style.zIndex = '9999';
    document.body.appendChild(container);
    return container;
}

function getIconForType(type) {
    const icons = {
        'success': 'check-circle-fill',
        'danger': 'exclamation-triangle-fill',
        'warning': 'exclamation-circle-fill',
        'info': 'info-circle-fill'
    };
    return icons[type] || 'info-circle-fill';
}

// Smooth Scroll
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

// Back to Top Button
function createBackToTopButton() {
    const button = document.createElement('button');
    button.id = 'backToTop';
    button.className = 'btn btn-primary';
    button.innerHTML = '<i class="bi bi-arrow-up"></i>';
    button.style.cssText = `
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
    
    button.addEventListener('click', () => {
        window.scrollTo({
            top: 0,
            behavior: 'smooth'
        });
    });
    
    document.body.appendChild(button);
    
    window.addEventListener('scroll', () => {
        if (window.pageYOffset > 300) {
            button.style.display = 'block';
        } else {
            button.style.display = 'none';
        }
    });
}

// Initialize tooltips
function initTooltips() {
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
}

// Initialize popovers
function initPopovers() {
    const popoverTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="popover"]'));
    popoverTriggerList.map(function (popoverTriggerEl) {
        return new bootstrap.Popover(popoverTriggerEl);
    });
}

// Lazy Loading Images
function initLazyLoading() {
    const images = document.querySelectorAll('img[data-src]');
    
    const imageObserver = new IntersectionObserver((entries, observer) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const img = entry.target;
                img.src = img.dataset.src;
                img.removeAttribute('data-src');
                observer.unobserve(img);
            }
        });
    });
    
    images.forEach(img => imageObserver.observe(img));
}

// Form Validation Enhancement
function enhanceFormValidation() {
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
                    showToast('Пожалуйста, заполните все обязательные поля', 'warning');
                }
            }
            
            form.classList.add('was-validated');
        }, false);
    });
}

// Copy to Clipboard
function copyToClipboard(text, successMessage = 'Скопировано!') {
    if (navigator.clipboard) {
        navigator.clipboard.writeText(text).then(() => {
            showToast(successMessage, 'success');
        }).catch(err => {
            showToast('Ошибка копирования', 'danger');
        });
    } else {
        // Fallback for older browsers
        const textarea = document.createElement('textarea');
        textarea.value = text;
        textarea.style.position = 'fixed';
        textarea.style.opacity = '0';
        document.body.appendChild(textarea);
        textarea.select();
        try {
            document.execCommand('copy');
            showToast(successMessage, 'success');
        } catch (err) {
            showToast('Ошибка копирования', 'danger');
        }
        document.body.removeChild(textarea);
    }
}

// Share functionality
function shareContent(title, text, url) {
    if (navigator.share) {
        navigator.share({
            title: title,
            text: text,
            url: url
        }).then(() => {
            showToast('Успешно поделились!', 'success');
        }).catch(err => {
            console.log('Error sharing:', err);
        });
    } else {
        // Fallback - copy link
        copyToClipboard(url, 'Ссылка скопирована!');
    }
}

// PWA Connection Status Indicator
function initConnectionIndicator() {
    const indicator = document.createElement('div');
    indicator.id = 'connection-indicator';
    indicator.style.cssText = `
        position: fixed;
        top: 10px;
        right: 10px;
        z-index: 10000;
        padding: 8px 15px;
        border-radius: 20px;
        font-size: 0.8rem;
        font-weight: 500;
        transition: all 0.3s ease;
        box-shadow: 0 2px 10px rgba(0,0,0,0.2);
    `;
    
    function updateIndicator() {
        if (navigator.onLine) {
            indicator.style.background = 'linear-gradient(135deg, #10b981, #059669)';
            indicator.style.color = 'white';
            indicator.innerHTML = '<i class="bi bi-wifi me-1"></i> Онлайн';
            indicator.style.display = 'none'; // Hide when online unless needed
        } else {
            indicator.style.background = 'linear-gradient(135deg, #ef4444, #dc2626)';
            indicator.style.color = 'white';
            indicator.innerHTML = '<i class="bi bi-wifi-off me-1"></i> Оффлайн';
            indicator.style.display = 'block';
        }
    }
    
    document.body.appendChild(indicator);
    updateIndicator();
    
    // Show indicator when offline
    window.addEventListener('online', () => {
        setTimeout(() => {
            indicator.style.display = 'none';
        }, 2000); // Hide after 2 seconds when back online
    });
    
    window.addEventListener('offline', updateIndicator);
}

// PWA Offline Data Storage
const OfflineStorage = {
    async saveFavorite(tournamentId, userId, action = 'POST') {
        if (!navigator.onLine) {
            const pendingAction = {
                id: Date.now(),
                type: 'favorite',
                tournament_id: tournamentId,
                user_id: userId,
                action: action,
                timestamp: new Date().toISOString()
            };
            
            const pendingActions = JSON.parse(localStorage.getItem('pendingActions') || '[]');
            pendingActions.push(pendingAction);
            localStorage.setItem('pendingActions', JSON.stringify(pendingActions));
            
            showToast('Действие сохранено. Будет выполнено при восстановлении соединения.', 'info');
        }
    },
    
    async saveRating(tournamentId, userId, rating, review = '') {
        if (!navigator.onLine) {
            const pendingAction = {
                id: Date.now(),
                type: 'rating',
                tournament_id: tournamentId,
                user_id: userId,
                rating: rating,
                review: review,
                timestamp: new Date().toISOString()
            };
            
            const pendingActions = JSON.parse(localStorage.getItem('pendingActions') || '[]');
            pendingActions.push(pendingAction);
            localStorage.setItem('pendingActions', JSON.stringify(pendingActions));
            
            showToast('Оценка сохранена. Будет отправлена при восстановлении соединения.', 'info');
        }
    },
    
    async syncPendingActions() {
        if (!navigator.onLine) return;
        
        const pendingActions = JSON.parse(localStorage.getItem('pendingActions') || '[]');
        if (pendingActions.length === 0) return;
        
        for (const action of pendingActions) {
            try {
                if (action.type === 'favorite') {
                    await fetch(`/api/tournaments/${action.tournament_id}/favorite`, {
                        method: action.action,
                        headers: { 'Content-Type': 'application/json' },
                        body: JSON.stringify({ user_id: action.user_id })
                    });
                } else if (action.type === 'rating') {
                    await fetch(`/api/tournaments/${action.tournament_id}/rate`, {
                        method: 'POST',
                        headers: { 'Content-Type': 'application/json' },
                        body: JSON.stringify({
                            user_id: action.user_id,
                            rating: action.rating,
                            review: action.review
                        })
                    });
                }
            } catch (error) {
                console.error('Failed to sync action:', error);
                continue; // Continue with other actions
            }
        }
        
        // Clear synced actions
        localStorage.removeItem('pendingActions');
        showToast('Офлайн-действия синхронизированы!', 'success');
    }
};

// Initialize on DOM ready
document.addEventListener('DOMContentLoaded', function() {
    initTooltips();
    initPopovers();
    initLazyLoading();
    enhanceFormValidation();
    createBackToTopButton();
    initConnectionIndicator();
    
    // Add fade-in animation to cards
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
    
    // Mark app as ready for lazy loading
    document.body.classList.add('app-ready');
    
    // Sync pending offline actions when coming online
    window.addEventListener('online', () => {
        OfflineStorage.syncPendingActions();
    });
    
    // Initial sync if online
    if (navigator.onLine) {
        OfflineStorage.syncPendingActions();
    }
});

// Mobile UI enhancements
document.addEventListener('DOMContentLoaded', function() {
    // Mobile filter panel functionality
    const mobileFiltersBtn = document.querySelector('.mobile-filters-btn');
    const mobileFiltersPanel = document.querySelector('.mobile-filters');
    const closeFilterBtn = document.querySelector('.mobile-filters .close-btn');
    
    if (mobileFiltersBtn && mobileFiltersPanel) {
        mobileFiltersBtn.addEventListener('click', function() {
            mobileFiltersPanel.classList.add('active');
        });
        
        closeFilterBtn.addEventListener('click', function() {
            mobileFiltersPanel.classList.remove('active');
        });
        
        // Close panel when clicking outside
        mobileFiltersPanel.addEventListener('click', function(e) {
            if (e.target === mobileFiltersPanel) {
                mobileFiltersPanel.classList.remove('active');
            }
        });
    }
    
    // Mobile search overlay functionality
    const searchOverlay = document.querySelector('.search-overlay');
    const searchToggle = document.querySelector('.search-toggle');
    
    if (searchToggle && searchOverlay) {
        searchToggle.addEventListener('click', function() {
            searchOverlay.classList.add('active');
            document.querySelector('.search-overlay input[type="search"]').focus();
        });
        
        // Close search overlay
        searchOverlay.addEventListener('click', function(e) {
            if (e.target === searchOverlay) {
                searchOverlay.classList.remove('active');
            }
        });
    }
    
    // Hamburger menu animation
    const hamburger = document.querySelector('.hamburger');
    const navbarCollapse = document.querySelector('.navbar-collapse');
    
    if (hamburger) {
        hamburger.addEventListener('click', function() {
            hamburger.classList.toggle('active');
            
            // Toggle navbar collapse
            if (navbarCollapse) {
                navbarCollapse.classList.toggle('show');
            }
        });
    }
    
    // Mobile tab navigation
    const mobileTabs = document.querySelectorAll('.mobile-tab');
    
    mobileTabs.forEach(tab => {
        tab.addEventListener('click', function() {
            // Remove active class from all tabs
            mobileTabs.forEach(t => t.classList.remove('active'));
            
            // Add active class to clicked tab
            this.classList.add('active');
            
            // Show corresponding content (if applicable)
            const tabContent = document.getElementById(this.dataset.tab);
            if (tabContent) {
                // Hide all tab contents
                document.querySelectorAll('.tab-content').forEach(content => {
                    content.classList.remove('active');
                });
                
                // Show clicked tab content
                tabContent.classList.add('active');
            }
        });
    });
    
    // Quick actions floating button
    const quickActionBtn = document.querySelector('.quick-action-btn');
    const quickActionMenu = document.querySelector('.quick-action-menu');
    
    if (quickActionBtn && quickActionMenu) {
        quickActionBtn.addEventListener('click', function() {
            quickActionMenu.classList.toggle('active');
        });
    }
    
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
            handleSwipe(card);
        });
    });
    
    function handleSwipe(element) {
        const threshold = 50; // Minimum distance for swipe
        const diff = touchStartX - touchEndX;
        
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
    
    // Pull to refresh functionality
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
    
    // Optimize for mobile performance
    if ('serviceWorker' in navigator) {
        navigator.serviceWorker.register('/sw.js')
            .then(registration => {
                console.log('SW registered: ', registration.scope);
                
                // Register for periodic sync if supported
                if ('periodicSync' in registration) {
                    try {
                        registration.periodicSync.register('refresh-tournaments', {
                            minInterval: 24 * 60 * 60 * 1000 // 24 hours
                        });
                    } catch (error) {
                        console.log('Periodic sync not supported:', error);
                    }
                }
                
                // Register for background sync if supported
                if ('sync' in registration) {
                    // Sync pending actions when service worker becomes active
                    registration.active?.postMessage({ action: 'syncPendingActions' });
                }
            })
            .catch(registrationError => {
                console.log('SW registration failed: ', registrationError);
            });
    }
});

// Debounce function for performance optimization
function debounce(func, wait, immediate) {
    let timeout;
    return function() {
        const context = this, args = arguments;
        const later = function() {
            timeout = null;
            if (!immediate) func.apply(context, args);
        };
        const callNow = immediate && !timeout;
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
        if (callNow) func.apply(context, args);
    };
}

// Throttle function for scroll and resize events
function throttle(func, limit) {
    let inThrottle;
    return function() {
        const args = arguments;
        const context = this;
        if (!inThrottle) {
            func.apply(context, args);
            inThrottle = true;
            setTimeout(() => inThrottle = false, limit);
        }
    };
}

// Export functions for global use
window.ChessCalendar = {
    showLoader,
    hideLoader,
    showToast,
    copyToClipboard,
    shareContent,
    debounce,
    throttle,
    OfflineStorage
};

// Initialize lazy loading if available
document.addEventListener('DOMContentLoaded', function() {
    // Check if lazy loader is available and initialize it
    if (typeof LazyLoader !== 'undefined') {
        console.log('Lazy loader initialized');
    } else {
        // Fallback: load additional modules manually if needed
        console.log('Lazy loader not available, using standard loading');
    }
});