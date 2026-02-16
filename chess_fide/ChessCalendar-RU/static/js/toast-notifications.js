// Toast Notifications System
// Beautiful, non-intrusive notifications for user actions

class ToastNotifications {
    constructor() {
        this.container = null;
        this.toasts = [];
        this.maxToasts = 5;
        this.init();
    }

    init() {
        this.createContainer();
        this.injectStyles();
    }

    createContainer() {
        if (document.getElementById('toastContainer')) return;

        this.container = document.createElement('div');
        this.container.id = 'toastContainer';
        this.container.className = 'toast-container';
        document.body.appendChild(this.container);
    }

    injectStyles() {
        if (document.getElementById('toastStyles')) return;

        const style = document.createElement('style');
        style.id = 'toastStyles';
        style.textContent = `
            .toast-container {
                position: fixed;
                top: 80px;
                right: 20px;
                z-index: 9999;
                display: flex;
                flex-direction: column;
                gap: 10px;
                max-width: 400px;
            }

            .toast {
                background: var(--bg-primary);
                border-radius: 12px;
                box-shadow: 0 8px 24px rgba(0, 0, 0, 0.15);
                padding: 16px 20px;
                display: flex;
                align-items: center;
                gap: 12px;
                min-width: 300px;
                animation: slideIn 0.3s ease;
                border-left: 4px solid;
                position: relative;
                overflow: hidden;
            }

            .toast::before {
                content: '';
                position: absolute;
                bottom: 0;
                left: 0;
                height: 3px;
                background: currentColor;
                animation: progress linear;
            }

            .toast.success {
                border-left-color: var(--success-color);
            }

            .toast.success::before {
                background: var(--success-color);
            }

            .toast.error {
                border-left-color: var(--danger-color);
            }

            .toast.error::before {
                background: var(--danger-color);
            }

            .toast.warning {
                border-left-color: var(--warning-color);
            }

            .toast.warning::before {
                background: var(--warning-color);
            }

            .toast.info {
                border-left-color: var(--info-color);
            }

            .toast.info::before {
                background: var(--info-color);
            }

            .toast-icon {
                font-size: 24px;
                flex-shrink: 0;
            }

            .toast.success .toast-icon {
                color: var(--success-color);
            }

            .toast.error .toast-icon {
                color: var(--danger-color);
            }

            .toast.warning .toast-icon {
                color: var(--warning-color);
            }

            .toast.info .toast-icon {
                color: var(--info-color);
            }

            .toast-content {
                flex: 1;
            }

            .toast-title {
                font-weight: 600;
                color: var(--text-primary);
                margin-bottom: 4px;
            }

            .toast-message {
                font-size: 14px;
                color: var(--text-secondary);
                line-height: 1.4;
            }

            .toast-close {
                background: none;
                border: none;
                color: var(--text-secondary);
                cursor: pointer;
                padding: 4px;
                font-size: 18px;
                line-height: 1;
                opacity: 0.6;
                transition: opacity 0.2s;
                flex-shrink: 0;
            }

            .toast-close:hover {
                opacity: 1;
            }

            @keyframes slideIn {
                from {
                    transform: translateX(400px);
                    opacity: 0;
                }
                to {
                    transform: translateX(0);
                    opacity: 1;
                }
            }

            @keyframes slideOut {
                from {
                    transform: translateX(0);
                    opacity: 1;
                }
                to {
                    transform: translateX(400px);
                    opacity: 0;
                }
            }

            @keyframes progress {
                from {
                    width: 100%;
                }
                to {
                    width: 0%;
                }
            }

            .toast.removing {
                animation: slideOut 0.3s ease forwards;
            }

            @media (max-width: 768px) {
                .toast-container {
                    top: 70px;
                    right: 10px;
                    left: 10px;
                    max-width: none;
                }

                .toast {
                    min-width: auto;
                }
            }
        `;
        document.head.appendChild(style);
    }

    show(options) {
        const {
            type = 'info',
            title = '',
            message = '',
            duration = 5000,
            closable = true
        } = options;

        // Limit number of toasts
        if (this.toasts.length >= this.maxToasts) {
            this.remove(this.toasts[0]);
        }

        const toast = this.createToast(type, title, message, duration, closable);
        this.container.appendChild(toast);
        this.toasts.push(toast);

        // Auto remove after duration
        if (duration > 0) {
            const progressBar = toast.querySelector('::before');
            if (progressBar) {
                toast.style.setProperty('--duration', `${duration}ms`);
            }

            setTimeout(() => {
                this.remove(toast);
            }, duration);
        }

        return toast;
    }

    createToast(type, title, message, duration, closable) {
        const toast = document.createElement('div');
        toast.className = `toast ${type}`;

        const icons = {
            success: 'bi-check-circle-fill',
            error: 'bi-x-circle-fill',
            warning: 'bi-exclamation-triangle-fill',
            info: 'bi-info-circle-fill'
        };

        const titles = {
            success: 'Успешно',
            error: 'Ошибка',
            warning: 'Внимание',
            info: 'Информация'
        };

        toast.innerHTML = `
            <div class="toast-icon">
                <i class="bi ${icons[type]}"></i>
            </div>
            <div class="toast-content">
                ${title ? `<div class="toast-title">${title}</div>` : `<div class="toast-title">${titles[type]}</div>`}
                ${message ? `<div class="toast-message">${message}</div>` : ''}
            </div>
            ${closable ? '<button class="toast-close"><i class="bi bi-x"></i></button>' : ''}
        `;

        // Set progress animation duration
        if (duration > 0) {
            toast.style.setProperty('--duration', `${duration}ms`);
            const style = document.createElement('style');
            style.textContent = `
                .toast::before {
                    animation-duration: ${duration}ms;
                }
            `;
            toast.appendChild(style);
        }

        if (closable) {
            const closeBtn = toast.querySelector('.toast-close');
            closeBtn.addEventListener('click', () => this.remove(toast));
        }

        return toast;
    }

    remove(toast) {
        if (!toast || !toast.parentElement) return;

        toast.classList.add('removing');
        setTimeout(() => {
            if (toast.parentElement) {
                toast.parentElement.removeChild(toast);
            }
            this.toasts = this.toasts.filter(t => t !== toast);
        }, 300);
    }

    success(message, title = '') {
        return this.show({ type: 'success', title, message });
    }

    error(message, title = '') {
        return this.show({ type: 'error', title, message });
    }

    warning(message, title = '') {
        return this.show({ type: 'warning', title, message });
    }

    info(message, title = '') {
        return this.show({ type: 'info', title, message });
    }

    // Preset notifications for common actions
    tournamentAdded() {
        return this.success('Турнир успешно добавлен в избранное');
    }

    tournamentRemoved() {
        return this.info('Турнир удален из избранного');
    }

    filterApplied() {
        return this.success('Фильтры применены');
    }

    exportSuccess(format) {
        return this.success(`Данные экспортированы в формате ${format}`);
    }

    exportError() {
        return this.error('Не удалось экспортировать данные');
    }

    comparisonReady(count) {
        return this.success(`Готово к сравнению ${count} турниров`);
    }

    networkError() {
        return this.error('Ошибка сети. Проверьте подключение к интернету');
    }

    copied() {
        return this.success('Скопировано в буфер обмена');
    }

    saved() {
        return this.success('Изменения сохранены');
    }

    loading(message = 'Загрузка...') {
        return this.show({
            type: 'info',
            message,
            duration: 0,
            closable: false
        });
    }
}

// Initialize global instance
window.toast = new ToastNotifications();

// Make it available globally
window.showToast = (message, type = 'info') => {
    return window.toast.show({ type, message });
};
