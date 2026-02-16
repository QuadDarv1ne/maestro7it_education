// ChessCalendar-RU - Main JavaScript

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

// Initialize on DOM ready
document.addEventListener('DOMContentLoaded', function() {
    initTooltips();
    initPopovers();
    initLazyLoading();
    enhanceFormValidation();
    createBackToTopButton();
    
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
                console.log('SW registered: ', registration);
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
    }
}

// Export functions for global use
window.ChessCalendar = {
    showLoader,
    hideLoader,
    showToast,
    copyToClipboard,
    shareContent
};
