/**
 * Enhanced Notification System for Simple HR
 */
class NotificationManager {
    constructor(options = {}) {
        this.options = {
            position: 'top-right',
            maxNotifications: 5,
            defaultDuration: 5000,
            animationDuration: 300,
            soundEnabled: false,
            ...options
        };
        
        this.notifications = [];
        this.container = null;
        this.init();
    }

    init() {
        this.createContainer();
        this.setupStyles();
    }

    createContainer() {
        if (!this.container) {
            this.container = document.createElement('div');
            this.container.className = `notification-manager notification-${this.options.position}`;
            this.container.setAttribute('role', 'region');
            this.container.setAttribute('aria-label', 'Уведомления');
            document.body.appendChild(this.container);
        }
    }

    setupStyles() {
        if (!document.getElementById('notification-manager-styles')) {
            const style = document.createElement('style');
            style.id = 'notification-manager-styles';
            style.textContent = `
                .notification-manager {
                    position: fixed;
                    z-index: 10000;
                    max-width: 400px;
                    pointer-events: none;
                }
                
                .notification-manager.notification-top-right {
                    top: 20px;
                    right: 20px;
                }
                
                .notification-manager.notification-top-left {
                    top: 20px;
                    left: 20px;
                }
                
                .notification-manager.notification-bottom-right {
                    bottom: 20px;
                    right: 20px;
                }
                
                .notification-manager.notification-bottom-left {
                    bottom: 20px;
                    left: 20px;
                }
                
                .notification-manager.notification-top-center {
                    top: 20px;
                    left: 50%;
                    transform: translateX(-50%);
                }
                
                .notification-manager.notification-bottom-center {
                    bottom: 20px;
                    left: 50%;
                    transform: translateX(-50%);
                }
                
                .notification-item {
                    background: white;
                    border-radius: 8px;
                    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
                    margin-bottom: 10px;
                    padding: 16px;
                    pointer-events: auto;
                    display: flex;
                    align-items: flex-start;
                    gap: 12px;
                    animation: slideInRight 0.3s ease-out;
                    position: relative;
                    overflow: hidden;
                }
                
                .notification-item::before {
                    content: '';
                    position: absolute;
                    left: 0;
                    top: 0;
                    bottom: 0;
                    width: 4px;
                }
                
                .notification-item.success::before {
                    background: #28a745;
                }
                
                .notification-item.error::before {
                    background: #dc3545;
                }
                
                .notification-item.warning::before {
                    background: #ffc107;
                }
                
                .notification-item.info::before {
                    background: #17a2b8;
                }
                
                .notification-icon {
                    font-size: 24px;
                    flex-shrink: 0;
                }
                
                .notification-icon.success {
                    color: #28a745;
                }
                
                .notification-icon.error {
                    color: #dc3545;
                }
                
                .notification-icon.warning {
                    color: #ffc107;
                }
                
                .notification-icon.info {
                    color: #17a2b8;
                }
                
                .notification-content {
                    flex: 1;
                }
                
                .notification-title {
                    font-weight: 600;
                    margin-bottom: 4px;
                    color: #212529;
                }
                
                .notification-message {
                    font-size: 14px;
                    color: #6c757d;
                    line-height: 1.4;
                }
                
                .notification-close {
                    background: none;
                    border: none;
                    font-size: 20px;
                    color: #6c757d;
                    cursor: pointer;
                    padding: 0;
                    width: 24px;
                    height: 24px;
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    transition: color 0.2s;
                    flex-shrink: 0;
                }
                
                .notification-close:hover {
                    color: #212529;
                }
                
                .notification-progress {
                    position: absolute;
                    bottom: 0;
                    left: 0;
                    height: 3px;
                    background: rgba(0, 0, 0, 0.1);
                    animation: progress linear;
                }
                
                .notification-item.removing {
                    animation: slideOutRight 0.3s ease-in forwards;
                }
                
                @keyframes slideInRight {
                    from {
                        transform: translateX(100%);
                        opacity: 0;
                    }
                    to {
                        transform: translateX(0);
                        opacity: 1;
                    }
                }
                
                @keyframes slideOutRight {
                    from {
                        transform: translateX(0);
                        opacity: 1;
                    }
                    to {
                        transform: translateX(100%);
                        opacity: 0;
                    }
                }
                
                @keyframes progress {
                    from {
                        width: 100%;
                    }
                    to {
                        width: 0;
                    }
                }
                
                /* Dark mode support */
                body.dark-mode .notification-item {
                    background: var(--card-bg, #22262e);
                    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.4);
                }
                
                body.dark-mode .notification-title {
                    color: var(--text-primary, #e4e6eb);
                }
                
                body.dark-mode .notification-message {
                    color: var(--text-secondary, #b0b3b8);
                }
                
                body.dark-mode .notification-close {
                    color: var(--text-secondary, #b0b3b8);
                }
                
                body.dark-mode .notification-close:hover {
                    color: var(--text-primary, #e4e6eb);
                }
            `;
            document.head.appendChild(style);
        }
    }

    show(message, type = 'info', options = {}) {
        const config = {
            title: this.getDefaultTitle(type),
            duration: this.options.defaultDuration,
            closable: true,
            ...options
        };

        const notification = this.createNotification(message, type, config);
        this.addNotification(notification);

        if (config.duration > 0) {
            setTimeout(() => {
                this.remove(notification.id);
            }, config.duration);
        }

        if (this.options.soundEnabled) {
            this.playSound(type);
        }

        return notification.id;
    }

    success(message, options = {}) {
        return this.show(message, 'success', options);
    }

    error(message, options = {}) {
        return this.show(message, 'error', options);
    }

    warning(message, options = {}) {
        return this.show(message, 'warning', options);
    }

    info(message, options = {}) {
        return this.show(message, 'info', options);
    }

    createNotification(message, type, config) {
        const id = `notification-${Date.now()}-${Math.random().toString(36).substr(2, 9)}`;
        
        const notification = document.createElement('div');
        notification.className = `notification-item ${type}`;
        notification.id = id;
        notification.setAttribute('role', 'alert');
        notification.setAttribute('aria-live', 'polite');

        const icon = this.getIcon(type);
        
        notification.innerHTML = `
            <div class="notification-icon ${type}">
                <i class="${icon}"></i>
            </div>
            <div class="notification-content">
                ${config.title ? `<div class="notification-title">${config.title}</div>` : ''}
                <div class="notification-message">${message}</div>
            </div>
            ${config.closable ? `
                <button class="notification-close" aria-label="Закрыть">
                    <i class="bi bi-x"></i>
                </button>
            ` : ''}
            ${config.duration > 0 ? `
                <div class="notification-progress" style="animation-duration: ${config.duration}ms;"></div>
            ` : ''}
        `;

        if (config.closable) {
            notification.querySelector('.notification-close').addEventListener('click', () => {
                this.remove(id);
            });
        }

        return { id, element: notification };
    }

    addNotification(notification) {
        // Remove oldest notification if max reached
        if (this.notifications.length >= this.options.maxNotifications) {
            this.remove(this.notifications[0].id);
        }

        this.notifications.push(notification);
        this.container.appendChild(notification.element);
    }

    remove(id) {
        const index = this.notifications.findIndex(n => n.id === id);
        if (index === -1) return;

        const notification = this.notifications[index];
        notification.element.classList.add('removing');

        setTimeout(() => {
            if (notification.element.parentElement) {
                notification.element.remove();
            }
            this.notifications.splice(index, 1);
        }, this.options.animationDuration);
    }

    removeAll() {
        this.notifications.forEach(notification => {
            this.remove(notification.id);
        });
    }

    getIcon(type) {
        const icons = {
            success: 'bi bi-check-circle-fill',
            error: 'bi bi-x-circle-fill',
            warning: 'bi bi-exclamation-triangle-fill',
            info: 'bi bi-info-circle-fill'
        };
        return icons[type] || icons.info;
    }

    getDefaultTitle(type) {
        const titles = {
            success: 'Успешно',
            error: 'Ошибка',
            warning: 'Предупреждение',
            info: 'Информация'
        };
        return titles[type] || titles.info;
    }

    playSound(type) {
        // Placeholder for sound functionality
        // Can be implemented with Web Audio API
        console.log(`Playing ${type} sound`);
    }
}

// Create global instance
const notificationManager = new NotificationManager();

// Export for use in other scripts
window.notificationManager = notificationManager;

// Convenience methods on window object
window.showNotification = (message, type, options) => notificationManager.show(message, type, options);
window.showSuccess = (message, options) => notificationManager.success(message, options);
window.showError = (message, options) => notificationManager.error(message, options);
window.showWarning = (message, options) => notificationManager.warning(message, options);
window.showInfo = (message, options) => notificationManager.info(message, options);
