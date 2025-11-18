/**
 * Loading Helper Functions
 * Provides utilities for showing/hiding loading states and skeleton screens
 */

class LoadingManager {
    constructor() {
        this.activeLoaders = new Set();
    }

    /**
     * Show global loading overlay
     * @param {string} message - Loading message to display
     */
    showOverlay(message = 'Загрузка...') {
        if (document.getElementById('global-loading-overlay')) {
            return; // Already showing
        }

        const overlay = document.createElement('div');
        overlay.id = 'global-loading-overlay';
        overlay.className = 'loading-overlay';
        overlay.innerHTML = `
            <div class="loading-spinner"></div>
            <div class="loading-text">${message}</div>
        `;
        document.body.appendChild(overlay);
        document.body.style.overflow = 'hidden';
    }

    /**
     * Hide global loading overlay
     */
    hideOverlay() {
        const overlay = document.getElementById('global-loading-overlay');
        if (overlay) {
            overlay.classList.add('fade-out');
            setTimeout(() => {
                overlay.remove();
                document.body.style.overflow = '';
            }, 300);
        }
    }

    /**
     * Show loading state on a button
     * @param {HTMLElement} button - Button element
     * @param {string} originalText - Original button text to restore later
     */
    showButtonLoading(button, originalText = null) {
        if (!button) return;
        
        button.dataset.originalText = originalText || button.innerHTML;
        button.classList.add('btn-loading');
        button.disabled = true;
    }

    /**
     * Hide loading state on a button
     * @param {HTMLElement} button - Button element
     */
    hideButtonLoading(button) {
        if (!button) return;
        
        button.classList.remove('btn-loading');
        button.disabled = false;
        if (button.dataset.originalText) {
            button.innerHTML = button.dataset.originalText;
            delete button.dataset.originalText;
        }
    }

    /**
     * Show skeleton loader in container
     * @param {HTMLElement} container - Container element
     * @param {string} type - Type of skeleton: 'table', 'cards', 'list'
     * @param {number} count - Number of skeleton items
     */
    showSkeleton(container, type = 'list', count = 5) {
        if (!container) return;
        
        container.classList.add('skeleton-container');
        
        let html = '';
        switch (type) {
            case 'table':
                html = this.generateTableSkeleton(count);
                break;
            case 'cards':
                html = this.generateCardsSkeleton(count);
                break;
            case 'list':
            default:
                html = this.generateListSkeleton(count);
                break;
        }
        
        container.innerHTML = html;
    }

    /**
     * Hide skeleton loader and restore content
     * @param {HTMLElement} container - Container element
     * @param {string} content - HTML content to display
     */
    hideSkeleton(container, content = '') {
        if (!container) return;
        
        container.classList.remove('skeleton-container');
        container.innerHTML = content;
        container.classList.add('fade-in');
    }

    /**
     * Generate table skeleton HTML
     */
    generateTableSkeleton(rows = 5) {
        let html = '<table class="table skeleton-table"><tbody>';
        for (let i = 0; i < rows; i++) {
            html += `
                <tr>
                    <td><div class="skeleton skeleton-text" style="width: 80%;"></div></td>
                    <td><div class="skeleton skeleton-text" style="width: 60%;"></div></td>
                    <td><div class="skeleton skeleton-text" style="width: 90%;"></div></td>
                    <td><div class="skeleton skeleton-text" style="width: 70%;"></div></td>
                </tr>
            `;
        }
        html += '</tbody></table>';
        return html;
    }

    /**
     * Generate cards skeleton HTML
     */
    generateCardsSkeleton(count = 4) {
        let html = '<div class="row">';
        for (let i = 0; i < count; i++) {
            html += `
                <div class="col-md-3 mb-3">
                    <div class="card">
                        <div class="card-body">
                            <div class="skeleton skeleton-title"></div>
                            <div class="skeleton skeleton-text"></div>
                            <div class="skeleton skeleton-text" style="width: 80%;"></div>
                        </div>
                    </div>
                </div>
            `;
        }
        html += '</div>';
        return html;
    }

    /**
     * Generate list skeleton HTML
     */
    generateListSkeleton(count = 5) {
        let html = '<div class="list-group">';
        for (let i = 0; i < count; i++) {
            html += `
                <div class="list-group-item">
                    <div class="d-flex align-items-center">
                        <div class="skeleton skeleton-avatar me-3"></div>
                        <div class="flex-grow-1">
                            <div class="skeleton skeleton-text mb-2" style="width: 60%;"></div>
                            <div class="skeleton skeleton-text" style="width: 40%;"></div>
                        </div>
                    </div>
                </div>
            `;
        }
        html += '</div>';
        return html;
    }

    /**
     * Show success animation
     * @param {string} message - Success message
     * @param {function} callback - Callback after animation
     */
    showSuccess(message = 'Успешно!', callback = null) {
        const modal = document.createElement('div');
        modal.className = 'loading-overlay';
        modal.innerHTML = `
            <div class="bounce-in">
                <svg class="checkmark" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 52 52">
                    <circle class="checkmark-circle" cx="26" cy="26" r="25" fill="none"/>
                    <path class="checkmark-check" fill="none" d="M14.1 27.2l7.1 7.2 16.7-16.8"/>
                </svg>
                <div class="loading-text mt-3">${message}</div>
            </div>
        `;
        document.body.appendChild(modal);

        setTimeout(() => {
            modal.classList.add('fade-out');
            setTimeout(() => {
                modal.remove();
                if (callback) callback();
            }, 300);
        }, 2000);
    }

    /**
     * Show error animation
     * @param {string} message - Error message
     */
    showError(message = 'Ошибка!') {
        const alert = document.createElement('div');
        alert.className = 'alert alert-danger alert-dismissible fade show shake position-fixed';
        alert.style.cssText = 'top: 20px; right: 20px; z-index: 10000; min-width: 300px;';
        alert.innerHTML = `
            <i class="bi bi-exclamation-triangle-fill me-2"></i>
            <strong>${message}</strong>
            <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
        `;
        document.body.appendChild(alert);

        setTimeout(() => {
            alert.classList.remove('show');
            setTimeout(() => alert.remove(), 300);
        }, 5000);
    }

    /**
     * Add typing indicator
     * @param {HTMLElement} container - Container element
     */
    showTyping(container) {
        if (!container) return;
        
        const indicator = document.createElement('div');
        indicator.className = 'typing-indicator';
        indicator.innerHTML = '<span></span><span></span><span></span>';
        container.appendChild(indicator);
    }

    /**
     * Create progress bar
     * @param {number} percent - Progress percentage (0-100)
     * @param {string} label - Progress label
     */
    createProgressBar(percent = 0, label = '') {
        return `
            <div class="mb-2">
                <div class="d-flex justify-content-between mb-1">
                    <span>${label}</span>
                    <span>${percent}%</span>
                </div>
                <div class="progress">
                    <div class="progress-bar progress-bar-animated" 
                         role="progressbar" 
                         style="width: ${percent}%"
                         aria-valuenow="${percent}" 
                         aria-valuemin="0" 
                         aria-valuemax="100"></div>
                </div>
            </div>
        `;
    }
}

// Create global instance
const loadingManager = new LoadingManager();

/**
 * AJAX Helper with loading states
 */
class AjaxHelper {
    /**
     * Fetch with automatic loading overlay
     * @param {string} url - URL to fetch
     * @param {object} options - Fetch options
     * @param {boolean} showLoading - Whether to show loading overlay
     */
    static async fetch(url, options = {}, showLoading = true) {
        if (showLoading) {
            loadingManager.showOverlay('Загрузка данных...');
        }

        try {
            const response = await fetch(url, options);
            
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            
            const data = await response.json();
            
            if (showLoading) {
                loadingManager.hideOverlay();
            }
            
            return { success: true, data };
        } catch (error) {
            if (showLoading) {
                loadingManager.hideOverlay();
            }
            
            loadingManager.showError('Ошибка загрузки данных');
            console.error('Fetch error:', error);
            
            return { success: false, error: error.message };
        }
    }

    /**
     * Submit form with loading state
     * @param {HTMLFormElement} form - Form element
     * @param {HTMLButtonElement} submitButton - Submit button
     */
    static async submitForm(form, submitButton = null) {
        if (!form) return;

        if (submitButton) {
            loadingManager.showButtonLoading(submitButton);
        } else {
            loadingManager.showOverlay('Отправка данных...');
        }

        const formData = new FormData(form);
        
        try {
            const response = await fetch(form.action, {
                method: form.method || 'POST',
                body: formData
            });

            if (submitButton) {
                loadingManager.hideButtonLoading(submitButton);
            } else {
                loadingManager.hideOverlay();
            }

            if (response.ok) {
                loadingManager.showSuccess('Данные успешно сохранены!');
                return { success: true };
            } else {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
        } catch (error) {
            if (submitButton) {
                loadingManager.hideButtonLoading(submitButton);
            } else {
                loadingManager.hideOverlay();
            }
            
            loadingManager.showError('Ошибка отправки данных');
            console.error('Form submission error:', error);
            
            return { success: false, error: error.message };
        }
    }
}

/**
 * Lazy Loading Helper
 */
class LazyLoader {
    constructor() {
        this.observer = null;
        this.init();
    }

    init() {
        if ('IntersectionObserver' in window) {
            this.observer = new IntersectionObserver((entries) => {
                entries.forEach(entry => {
                    if (entry.isIntersecting) {
                        this.loadElement(entry.target);
                        this.observer.unobserve(entry.target);
                    }
                });
            });
        }
    }

    loadElement(element) {
        if (element.dataset.src) {
            element.src = element.dataset.src;
            element.classList.remove('lazy-load-placeholder');
            element.classList.add('fade-in');
        }
    }

    observe(selector = '[data-src]') {
        if (!this.observer) return;
        
        document.querySelectorAll(selector).forEach(element => {
            this.observer.observe(element);
        });
    }
}

// Initialize lazy loader
const lazyLoader = new LazyLoader();

// Auto-initialize on DOM ready
document.addEventListener('DOMContentLoaded', () => {
    lazyLoader.observe();
});
