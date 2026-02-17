/**
 * Система уведомлений в реальном времени
 * Push notifications, toast messages, и notification center
 */

class NotificationSystem {
    constructor(options = {}) {
        this.options = {
            position: options.position || 'top-right',
            duration: options.duration || 5000,
            maxNotifications: options.maxNotifications || 5,
            enableSound: options.enableSound !== false,
            enablePush: options.enablePush !== false
        };
        
        this.notifications = [];
        this.notificationId = 0;
        this.container = null;
        
        this.init();
    }

    init() {
        this.createContainer();
        this.requestPermission();
        this.loadNotifications();
    }

    /**
     * Создание контейнера для уведомлений
     */
    createContainer() {
        this.container = document.createElement('div');
        this.container.id = 'notificationContainer';
        this.container.className = `notification-container notification-${this.options.position}`;
        document.body.appendChild(this.container);
    }

    /**
     * Запрос разрешения на push уведомления
     */
    async requestPermission() {
        if (!this.options.enablePush || !('Notification' in window)) {
            return;
        }

        if (Notification.permission === 'default') {
            try {
                const permission = await Notification.requestPermission();
                if (permission === 'granted') {
                    this.show('Уведомления включены', 'success', {
                        body: 'Вы будете получать уведомления о новых турнирах'
                    });
                }
            } catch (error) {
                console.error('Error requesting notification permission:', error);
            }
        }
    }

    /**
     * Показать уведомление
     */
    show(title, type = 'info', options = {}) {
        const notification = {
            id: ++this.notificationId,
            title,
            type,
            body: options.body || '',
            icon: options.icon || this.getIconForType(type),
            timestamp: new Date(),
            read: false,
            action: options.action || null
        };

        this.notifications.unshift(notification);
        this.saveNotifications();

        // Показываем toast
        this.showToast(notification);

        // Push уведомление (если разрешено)
        if (this.options.enablePush && options.push !== false) {
            this.showPushNotification(notification);
        }

        // Звук
        if (this.options.enableSound && options.sound !== false) {
            this.playSound(type);
        }

        // Обновляем счетчик
        this.updateBadge();

        return notification.id;
    }

    /**
     * Показать toast уведомление
     */
    showToast(notification) {
        const toast = document.createElement('div');
        toast.className = `notification-toast notification-${notification.type}`;
        toast.dataset.notificationId = notification.id;
        
        toast.innerHTML = `
            <div class="notification-icon">
                <i class="bi bi-${notification.icon}"></i>
            </div>
            <div class="notification-content">
                <div class="notification-title">${notification.title}</div>
                ${notification.body ? `<div class="notification-body">${notification.body}</div>` : ''}
            </div>
            <button class="notification-close" onclick="notificationSystem.closeToast(${notification.id})">
                <i class="bi bi-x"></i>
            </button>
        `;

        // Добавляем action кнопку если есть
        if (notification.action) {
            const actionBtn = document.createElement('button');
            actionBtn.className = 'notification-action';
            actionBtn.textContent = notification.action.label;
            actionBtn.onclick = () => {
                notification.action.callback();
                this.closeToast(notification.id);
            };
            toast.querySelector('.notification-content').appendChild(actionBtn);
        }

        this.container.appendChild(toast);

        // Анимация появления
        requestAnimationFrame(() => {
            toast.classList.add('show');
        });

        // Автоматическое закрытие
        if (this.options.duration > 0) {
            setTimeout(() => {
                this.closeToast(notification.id);
            }, this.options.duration);
        }

        // Ограничение количества
        this.limitToasts();
    }

    /**
     * Закрыть toast
     */
    closeToast(notificationId) {
        const toast = this.container.querySelector(`[data-notification-id="${notificationId}"]`);
        if (toast) {
            toast.classList.remove('show');
            toast.classList.add('hide');
            setTimeout(() => toast.remove(), 300);
        }
    }

    /**
     * Ограничение количества toast
     */
    limitToasts() {
        const toasts = this.container.querySelectorAll('.notification-toast');
        if (toasts.length > this.options.maxNotifications) {
            for (let i = this.options.maxNotifications; i < toasts.length; i++) {
                toasts[i].remove();
            }
        }
    }

    /**
     * Push уведомление
     */
    showPushNotification(notification) {
        if (!('Notification' in window) || Notification.permission !== 'granted') {
            return;
        }

        const pushNotification = new Notification(notification.title, {
            body: notification.body,
            icon: '/static/images/logo.png',
            badge: '/static/images/badge.png',
            tag: `notification-${notification.id}`,
            requireInteraction: false
        });

        pushNotification.onclick = () => {
            window.focus();
            if (notification.action) {
                notification.action.callback();
            }
            pushNotification.close();
        };
    }

    /**
     * Воспроизведение звука
     */
    playSound(type) {
        const audio = new Audio(`/static/sounds/notification-${type}.mp3`);
        audio.volume = 0.3;
        audio.play().catch(() => {
            // Игнорируем ошибки воспроизведения
        });
    }

    /**
     * Получить иконку для типа
     */
    getIconForType(type) {
        const icons = {
            success: 'check-circle-fill',
            error: 'exclamation-circle-fill',
            warning: 'exclamation-triangle-fill',
            info: 'info-circle-fill',
            tournament: 'trophy-fill',
            favorite: 'heart-fill'
        };
        return icons[type] || 'bell-fill';
    }

    /**
     * Обновить badge счетчик
     */
    updateBadge() {
        const unreadCount = this.notifications.filter(n => !n.read).length;
        const badge = document.querySelector('.notification-badge');
        
        if (badge) {
            if (unreadCount > 0) {
                badge.textContent = unreadCount > 99 ? '99+' : unreadCount;
                badge.style.display = 'flex';
            } else {
                badge.style.display = 'none';
            }
        }
    }

    /**
     * Пометить как прочитанное
     */
    markAsRead(notificationId) {
        const notification = this.notifications.find(n => n.id === notificationId);
        if (notification) {
            notification.read = true;
            this.saveNotifications();
            this.updateBadge();
        }
    }

    /**
     * Пометить все как прочитанные
     */
    markAllAsRead() {
        this.notifications.forEach(n => n.read = true);
        this.saveNotifications();
        this.updateBadge();
    }

    /**
     * Очистить все уведомления
     */
    clearAll() {
        this.notifications = [];
        this.saveNotifications();
        this.updateBadge();
    }

    /**
     * Сохранить уведомления
     */
    saveNotifications() {
        try {
            // Сохраняем только последние 50
            const toSave = this.notifications.slice(0, 50);
            localStorage.setItem('notifications', JSON.stringify(toSave));
        } catch (error) {
            console.error('Error saving notifications:', error);
        }
    }

    /**
     * Загрузить уведомления
     */
    loadNotifications() {
        try {
            const stored = localStorage.getItem('notifications');
            if (stored) {
                this.notifications = JSON.parse(stored);
                this.notificationId = Math.max(...this.notifications.map(n => n.id), 0);
                this.updateBadge();
            }
        } catch (error) {
            console.error('Error loading notifications:', error);
        }
    }

    /**
     * Получить все уведомления
     */
    getAll() {
        return this.notifications;
    }

    /**
     * Получить непрочитанные
     */
    getUnread() {
        return this.notifications.filter(n => !n.read);
    }
}

// CSS стили
const style = document.createElement('style');
style.textContent = `
    .notification-container {
        position: fixed;
        z-index: 10000;
        display: flex;
        flex-direction: column;
        gap: 0.75rem;
        max-width: 400px;
        pointer-events: none;
    }

    .notification-container.notification-top-right {
        top: 1rem;
        right: 1rem;
    }

    .notification-container.notification-top-left {
        top: 1rem;
        left: 1rem;
    }

    .notification-container.notification-bottom-right {
        bottom: 1rem;
        right: 1rem;
    }

    .notification-container.notification-bottom-left {
        bottom: 1rem;
        left: 1rem;
    }

    .notification-toast {
        display: flex;
        align-items: flex-start;
        gap: 0.75rem;
        padding: 1rem;
        background: white;
        border-radius: 0.75rem;
        box-shadow: 0 10px 40px rgba(0, 0, 0, 0.15);
        pointer-events: auto;
        transform: translateX(120%);
        opacity: 0;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        border-left: 4px solid;
    }

    .notification-toast.show {
        transform: translateX(0);
        opacity: 1;
    }

    .notification-toast.hide {
        transform: translateX(120%);
        opacity: 0;
    }

    .notification-toast.notification-success {
        border-left-color: #10b981;
    }

    .notification-toast.notification-error {
        border-left-color: #ef4444;
    }

    .notification-toast.notification-warning {
        border-left-color: #f59e0b;
    }

    .notification-toast.notification-info {
        border-left-color: #3b82f6;
    }

    .notification-icon {
        width: 40px;
        height: 40px;
        display: flex;
        align-items: center;
        justify-content: center;
        border-radius: 50%;
        flex-shrink: 0;
        font-size: 1.25rem;
    }

    .notification-success .notification-icon {
        background: #d1fae5;
        color: #10b981;
    }

    .notification-error .notification-icon {
        background: #fee2e2;
        color: #ef4444;
    }

    .notification-warning .notification-icon {
        background: #fef3c7;
        color: #f59e0b;
    }

    .notification-info .notification-icon {
        background: #dbeafe;
        color: #3b82f6;
    }

    .notification-content {
        flex: 1;
        min-width: 0;
    }

    .notification-title {
        font-weight: 600;
        color: #1f2937;
        margin-bottom: 0.25rem;
    }

    .notification-body {
        font-size: 0.875rem;
        color: #6b7280;
        line-height: 1.4;
    }

    .notification-action {
        margin-top: 0.5rem;
        padding: 0.375rem 0.75rem;
        background: #f3f4f6;
        border: none;
        border-radius: 0.375rem;
        font-size: 0.875rem;
        font-weight: 500;
        color: #374151;
        cursor: pointer;
        transition: background 0.2s;
    }

    .notification-action:hover {
        background: #e5e7eb;
    }

    .notification-close {
        width: 24px;
        height: 24px;
        display: flex;
        align-items: center;
        justify-content: center;
        background: transparent;
        border: none;
        border-radius: 0.25rem;
        color: #9ca3af;
        cursor: pointer;
        transition: all 0.2s;
        flex-shrink: 0;
    }

    .notification-close:hover {
        background: #f3f4f6;
        color: #374151;
    }

    .notification-badge {
        position: absolute;
        top: -4px;
        right: -4px;
        min-width: 20px;
        height: 20px;
        display: flex;
        align-items: center;
        justify-content: center;
        padding: 0 6px;
        background: #ef4444;
        color: white;
        border-radius: 10px;
        font-size: 0.75rem;
        font-weight: 600;
        line-height: 1;
    }

    @media (max-width: 768px) {
        .notification-container {
            max-width: calc(100vw - 2rem);
            left: 1rem !important;
            right: 1rem !important;
        }
    }
`;
document.head.appendChild(style);

// Инициализация
document.addEventListener('DOMContentLoaded', () => {
    window.notificationSystem = new NotificationSystem({
        position: 'top-right',
        duration: 5000,
        maxNotifications: 5
    });
});

// Экспорт
if (typeof module !== 'undefined' && module.exports) {
    module.exports = NotificationSystem;
}
