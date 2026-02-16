/**
 * Gesture Handler Module
 * Обработка жестов (свайпы, пинч, долгое нажатие)
 */

class GestureHandler {
    constructor() {
        this.touchStartX = 0;
        this.touchStartY = 0;
        this.touchEndX = 0;
        this.touchEndY = 0;
        this.touchStartTime = 0;
        this.longPressTimer = null;
        this.swipeThreshold = 50;
        this.longPressDelay = 500;
        this.gestures = new Map();
        
        this.init();
    }

    init() {
        console.log('[GestureHandler] Инициализация обработчика жестов');
        
        if (!('ontouchstart' in window)) {
            console.log('[GestureHandler] Touch не поддерживается');
            return;
        }

        this.setupGlobalGestures();
        this.setupSwipeNavigation();
        this.setupPullToRefresh();
    }

    setupGlobalGestures() {
        document.addEventListener('touchstart', (e) => {
            this.handleTouchStart(e);
        }, { passive: true });

        document.addEventListener('touchmove', (e) => {
            this.handleTouchMove(e);
        }, { passive: false });

        document.addEventListener('touchend', (e) => {
            this.handleTouchEnd(e);
        }, { passive: true });

        document.addEventListener('touchcancel', (e) => {
            this.handleTouchCancel(e);
        }, { passive: true });
    }

    handleTouchStart(e) {
        const touch = e.touches[0];
        this.touchStartX = touch.clientX;
        this.touchStartY = touch.clientY;
        this.touchStartTime = Date.now();

        // Долгое нажатие
        this.longPressTimer = setTimeout(() => {
            this.triggerLongPress(e);
        }, this.longPressDelay);
    }

    handleTouchMove(e) {
        // Отменяем долгое нажатие при движении
        if (this.longPressTimer) {
            clearTimeout(this.longPressTimer);
            this.longPressTimer = null;
        }

        const touch = e.touches[0];
        this.touchEndX = touch.clientX;
        this.touchEndY = touch.clientY;
    }

    handleTouchEnd(e) {
        if (this.longPressTimer) {
            clearTimeout(this.longPressTimer);
            this.longPressTimer = null;
        }

        const deltaX = this.touchEndX - this.touchStartX;
        const deltaY = this.touchEndY - this.touchStartY;
        const deltaTime = Date.now() - this.touchStartTime;

        // Определяем тип жеста
        if (Math.abs(deltaX) > this.swipeThreshold || Math.abs(deltaY) > this.swipeThreshold) {
            if (Math.abs(deltaX) > Math.abs(deltaY)) {
                // Горизонтальный свайп
                if (deltaX > 0) {
                    this.triggerSwipe('right', deltaX, deltaTime, e);
                } else {
                    this.triggerSwipe('left', Math.abs(deltaX), deltaTime, e);
                }
            } else {
                // Вертикальный свайп
                if (deltaY > 0) {
                    this.triggerSwipe('down', deltaY, deltaTime, e);
                } else {
                    this.triggerSwipe('up', Math.abs(deltaY), deltaTime, e);
                }
            }
        } else if (deltaTime < 200) {
            // Быстрый тап
            this.triggerTap(e);
        }

        // Сброс
        this.touchStartX = 0;
        this.touchStartY = 0;
        this.touchEndX = 0;
        this.touchEndY = 0;
    }

    handleTouchCancel(e) {
        if (this.longPressTimer) {
            clearTimeout(this.longPressTimer);
            this.longPressTimer = null;
        }
    }

    triggerSwipe(direction, distance, duration, event) {
        const velocity = distance / duration;
        
        console.log(`[GestureHandler] Свайп ${direction}:`, {
            distance,
            duration,
            velocity
        });

        const customEvent = new CustomEvent('swipe', {
            detail: {
                direction,
                distance,
                duration,
                velocity,
                originalEvent: event
            }
        });

        document.dispatchEvent(customEvent);

        // Направленные события
        const directionEvent = new CustomEvent(`swipe${direction}`, {
            detail: {
                distance,
                duration,
                velocity,
                originalEvent: event
            }
        });

        document.dispatchEvent(directionEvent);
    }

    triggerLongPress(event) {
        console.log('[GestureHandler] Долгое нажатие');

        const customEvent = new CustomEvent('longpress', {
            detail: {
                x: this.touchStartX,
                y: this.touchStartY,
                originalEvent: event
            }
        });

        document.dispatchEvent(customEvent);
    }

    triggerTap(event) {
        const customEvent = new CustomEvent('quicktap', {
            detail: {
                x: this.touchStartX,
                y: this.touchStartY,
                originalEvent: event
            }
        });

        document.dispatchEvent(customEvent);
    }

    setupSwipeNavigation() {
        // Свайп вправо - назад
        document.addEventListener('swiperight', (e) => {
            if (e.detail.distance > 100 && e.detail.velocity > 0.5) {
                // Проверяем, что свайп начался с края экрана
                if (this.touchStartX < 50) {
                    this.navigateBack();
                }
            }
        });

        // Свайп влево - вперёд (если есть история)
        document.addEventListener('swipeleft', (e) => {
            if (e.detail.distance > 100 && e.detail.velocity > 0.5) {
                // Проверяем, что свайп начался с края экрана
                if (this.touchStartX > window.innerWidth - 50) {
                    this.navigateForward();
                }
            }
        });
    }

    navigateBack() {
        if (window.history.length > 1) {
            console.log('[GestureHandler] Навигация назад');
            this.showNavigationFeedback('left');
            setTimeout(() => {
                window.history.back();
            }, 200);
        }
    }

    navigateForward() {
        console.log('[GestureHandler] Навигация вперёд');
        this.showNavigationFeedback('right');
        // Браузеры обычно не позволяют программно идти вперёд
    }

    showNavigationFeedback(direction) {
        const feedback = document.createElement('div');
        feedback.className = `navigation-feedback navigation-${direction}`;
        feedback.innerHTML = `<i class="bi bi-arrow-${direction}"></i>`;
        document.body.appendChild(feedback);

        setTimeout(() => {
            feedback.classList.add('show');
        }, 10);

        setTimeout(() => {
            feedback.classList.remove('show');
            setTimeout(() => {
                feedback.remove();
            }, 300);
        }, 500);
    }

    setupPullToRefresh() {
        let startY = 0;
        let currentY = 0;
        let pulling = false;
        let refreshThreshold = 80;
        let refreshIndicator = null;

        document.addEventListener('touchstart', (e) => {
            if (window.scrollY === 0) {
                startY = e.touches[0].clientY;
                pulling = true;
            }
        }, { passive: true });

        document.addEventListener('touchmove', (e) => {
            if (!pulling) return;

            currentY = e.touches[0].clientY;
            const pullDistance = currentY - startY;

            if (pullDistance > 0 && pullDistance < 150) {
                e.preventDefault();
                this.showPullToRefreshIndicator(pullDistance, refreshThreshold);
            }
        }, { passive: false });

        document.addEventListener('touchend', (e) => {
            if (!pulling) return;

            const pullDistance = currentY - startY;
            
            if (pullDistance > refreshThreshold) {
                this.triggerRefresh();
            } else {
                this.hidePullToRefreshIndicator();
            }

            pulling = false;
            startY = 0;
            currentY = 0;
        }, { passive: true });
    }

    showPullToRefreshIndicator(distance, threshold) {
        let indicator = document.getElementById('pullToRefreshIndicator');
        
        if (!indicator) {
            indicator = document.createElement('div');
            indicator.id = 'pullToRefreshIndicator';
            indicator.className = 'pull-to-refresh-indicator';
            indicator.innerHTML = `
                <div class="refresh-spinner">
                    <i class="bi bi-arrow-clockwise"></i>
                </div>
                <div class="refresh-text">Потяните для обновления</div>
            `;
            document.body.insertBefore(indicator, document.body.firstChild);
        }

        const progress = Math.min(distance / threshold, 1);
        indicator.style.transform = `translateY(${distance}px)`;
        indicator.style.opacity = progress;

        const spinner = indicator.querySelector('.refresh-spinner');
        spinner.style.transform = `rotate(${progress * 360}deg)`;

        if (progress >= 1) {
            indicator.querySelector('.refresh-text').textContent = 'Отпустите для обновления';
            indicator.classList.add('ready');
        } else {
            indicator.querySelector('.refresh-text').textContent = 'Потяните для обновления';
            indicator.classList.remove('ready');
        }
    }

    hidePullToRefreshIndicator() {
        const indicator = document.getElementById('pullToRefreshIndicator');
        if (indicator) {
            indicator.style.transform = 'translateY(-100%)';
            indicator.style.opacity = '0';
            setTimeout(() => {
                indicator.remove();
            }, 300);
        }
    }

    triggerRefresh() {
        console.log('[GestureHandler] Обновление страницы');
        
        const indicator = document.getElementById('pullToRefreshIndicator');
        if (indicator) {
            indicator.classList.add('refreshing');
            indicator.querySelector('.refresh-text').textContent = 'Обновление...';
            indicator.querySelector('.refresh-spinner').classList.add('spinning');
        }

        // Событие обновления
        const event = new CustomEvent('pulltorefresh');
        document.dispatchEvent(event);

        // Обновляем страницу через 1 секунду
        setTimeout(() => {
            window.location.reload();
        }, 1000);
    }

    // Регистрация пользовательского жеста
    registerGesture(name, handler) {
        this.gestures.set(name, handler);
        console.log(`[GestureHandler] Зарегистрирован жест: ${name}`);
    }

    // Удаление жеста
    unregisterGesture(name) {
        this.gestures.delete(name);
        console.log(`[GestureHandler] Удалён жест: ${name}`);
    }
}

// Стили для жестов
const style = document.createElement('style');
style.textContent = `
    /* Navigation feedback */
    .navigation-feedback {
        position: fixed;
        top: 50%;
        transform: translateY(-50%);
        width: 60px;
        height: 60px;
        background: var(--primary-color);
        color: white;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 1.5rem;
        opacity: 0;
        transition: opacity 0.3s ease, transform 0.3s ease;
        z-index: 10000;
        pointer-events: none;
    }

    .navigation-feedback.navigation-left {
        left: 20px;
        transform: translateY(-50%) translateX(-20px);
    }

    .navigation-feedback.navigation-right {
        right: 20px;
        transform: translateY(-50%) translateX(20px);
    }

    .navigation-feedback.show {
        opacity: 0.9;
        transform: translateY(-50%) translateX(0);
    }

    /* Pull to refresh indicator */
    .pull-to-refresh-indicator {
        position: fixed;
        top: 0;
        left: 0;
        right: 0;
        height: 80px;
        background: var(--bg-primary);
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        gap: 0.5rem;
        z-index: 9999;
        transform: translateY(-100%);
        transition: transform 0.3s ease, opacity 0.3s ease;
        box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
    }

    .refresh-spinner {
        width: 30px;
        height: 30px;
        display: flex;
        align-items: center;
        justify-content: center;
        transition: transform 0.3s ease;
    }

    .refresh-spinner i {
        font-size: 1.5rem;
        color: var(--primary-color);
    }

    .refresh-spinner.spinning {
        animation: spin 1s linear infinite;
    }

    @keyframes spin {
        from {
            transform: rotate(0deg);
        }
        to {
            transform: rotate(360deg);
        }
    }

    .refresh-text {
        font-size: 0.875rem;
        color: var(--text-secondary);
        font-weight: 500;
    }

    .pull-to-refresh-indicator.ready .refresh-spinner i {
        color: var(--success-color);
    }

    .pull-to-refresh-indicator.refreshing {
        transform: translateY(0) !important;
        opacity: 1 !important;
    }

    /* Отключение выделения текста при жестах */
    body.gesturing {
        user-select: none;
        -webkit-user-select: none;
        -moz-user-select: none;
        -ms-user-select: none;
    }

    /* Smooth scrolling для жестов */
    html {
        scroll-behavior: smooth;
    }
`;
document.head.appendChild(style);

// Инициализация
document.addEventListener('DOMContentLoaded', () => {
    window.ChessCalendar = window.ChessCalendar || {};
    window.ChessCalendar.gestureHandler = new GestureHandler();
    
    // Примеры использования
    
    // Свайп влево на карточке турнира - добавить в избранное
    document.addEventListener('swipeleft', (e) => {
        const card = e.detail.originalEvent.target.closest('.tournament-card');
        if (card && e.detail.velocity > 0.8) {
            console.log('[GestureHandler] Быстрый свайп влево на карточке');
            // Добавить в избранное
        }
    });
    
    // Долгое нажатие на карточке - показать меню
    document.addEventListener('longpress', (e) => {
        const card = e.detail.originalEvent.target.closest('.tournament-card');
        if (card) {
            console.log('[GestureHandler] Долгое нажатие на карточке');
            // Показать контекстное меню
        }
    });
});

// Экспорт
if (typeof module !== 'undefined' && module.exports) {
    module.exports = GestureHandler;
}
