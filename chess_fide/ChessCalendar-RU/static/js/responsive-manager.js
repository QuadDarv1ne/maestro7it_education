/**
 * Responsive Manager
 * Управление адаптивным поведением приложения
 */

class ResponsiveManager {
    constructor() {
        this.breakpoints = {
            xs: 0,
            sm: 576,
            md: 768,
            lg: 992,
            xl: 1200,
            xxl: 1400
        };
        
        this.currentBreakpoint = this.getCurrentBreakpoint();
        this.orientation = this.getOrientation();
        this.touchDevice = this.isTouchDevice();
        
        this.init();
    }

    init() {
        console.log('[ResponsiveManager] Инициализация адаптивного менеджера');
        console.log('[ResponsiveManager] Текущий breakpoint:', this.currentBreakpoint);
        console.log('[ResponsiveManager] Ориентация:', this.orientation);
        console.log('[ResponsiveManager] Тачскрин:', this.touchDevice);
        
        this.setupListeners();
        this.optimizeForDevice();
        this.handleOrientation();
        this.setupViewportHeight();
        this.setupImageLazyLoading();
        this.setupTouchOptimizations();
    }

    setupListeners() {
        // Отслеживание изменения размера окна
        let resizeTimer;
        window.addEventListener('resize', () => {
            clearTimeout(resizeTimer);
            resizeTimer = setTimeout(() => {
                this.handleResize();
            }, 250);
        });

        // Отслеживание изменения ориентации
        window.addEventListener('orientationchange', () => {
            setTimeout(() => {
                this.handleOrientation();
            }, 100);
        });

        // Отслеживание изменения видимости страницы
        document.addEventListener('visibilitychange', () => {
            this.handleVisibilityChange();
        });
    }

    handleResize() {
        const newBreakpoint = this.getCurrentBreakpoint();
        
        if (newBreakpoint !== this.currentBreakpoint) {
            console.log('[ResponsiveManager] Breakpoint изменён:', this.currentBreakpoint, '→', newBreakpoint);
            this.currentBreakpoint = newBreakpoint;
            this.optimizeForDevice();
            this.triggerBreakpointChange(newBreakpoint);
        }

        this.setupViewportHeight();
    }

    handleOrientation() {
        const newOrientation = this.getOrientation();
        
        if (newOrientation !== this.orientation) {
            console.log('[ResponsiveManager] Ориентация изменена:', newOrientation);
            this.orientation = newOrientation;
            this.setupViewportHeight();
            this.triggerOrientationChange(newOrientation);
        }
    }

    handleVisibilityChange() {
        if (document.hidden) {
            console.log('[ResponsiveManager] Страница скрыта');
        } else {
            console.log('[ResponsiveManager] Страница видима');
            this.setupViewportHeight();
        }
    }

    getCurrentBreakpoint() {
        const width = window.innerWidth;
        
        if (width >= this.breakpoints.xxl) return 'xxl';
        if (width >= this.breakpoints.xl) return 'xl';
        if (width >= this.breakpoints.lg) return 'lg';
        if (width >= this.breakpoints.md) return 'md';
        if (width >= this.breakpoints.sm) return 'sm';
        return 'xs';
    }

    getOrientation() {
        return window.innerHeight > window.innerWidth ? 'portrait' : 'landscape';
    }

    isTouchDevice() {
        return ('ontouchstart' in window) ||
               (navigator.maxTouchPoints > 0) ||
               (navigator.msMaxTouchPoints > 0);
    }

    isMobile() {
        return this.currentBreakpoint === 'xs' || this.currentBreakpoint === 'sm';
    }

    isTablet() {
        return this.currentBreakpoint === 'md';
    }

    isDesktop() {
        return ['lg', 'xl', 'xxl'].includes(this.currentBreakpoint);
    }

    optimizeForDevice() {
        document.body.classList.remove('device-mobile', 'device-tablet', 'device-desktop');
        
        if (this.isMobile()) {
            document.body.classList.add('device-mobile');
            this.optimizeForMobile();
        } else if (this.isTablet()) {
            document.body.classList.add('device-tablet');
            this.optimizeForTablet();
        } else {
            document.body.classList.add('device-desktop');
            this.optimizeForDesktop();
        }

        if (this.touchDevice) {
            document.body.classList.add('touch-device');
        }
    }

    optimizeForMobile() {
        console.log('[ResponsiveManager] Оптимизация для мобильных');
        
        // Компактные карточки
        document.querySelectorAll('.card').forEach(card => {
            card.classList.add('card-compact');
        });

        // Полноширинные кнопки
        document.querySelectorAll('.btn-group .btn').forEach(btn => {
            if (!btn.classList.contains('btn-sm')) {
                btn.classList.add('btn-mobile-full');
            }
        });

        // Упрощённые модальные окна
        document.querySelectorAll('.modal-dialog').forEach(modal => {
            if (!modal.classList.contains('modal-fullscreen')) {
                modal.classList.add('modal-dialog-scrollable');
            }
        });
    }

    optimizeForTablet() {
        console.log('[ResponsiveManager] Оптимизация для планшетов');
        
        // Средний размер карточек
        document.querySelectorAll('.card').forEach(card => {
            card.classList.remove('card-compact');
        });
    }

    optimizeForDesktop() {
        console.log('[ResponsiveManager] Оптимизация для десктопа');
        
        // Полноразмерные карточки
        document.querySelectorAll('.card').forEach(card => {
            card.classList.remove('card-compact');
        });

        // Убираем полноширинные кнопки
        document.querySelectorAll('.btn-mobile-full').forEach(btn => {
            btn.classList.remove('btn-mobile-full');
        });
    }

    setupViewportHeight() {
        // Фикс для мобильных браузеров (100vh проблема)
        const vh = window.innerHeight * 0.01;
        document.documentElement.style.setProperty('--vh', `${vh}px`);
    }

    setupImageLazyLoading() {
        if ('IntersectionObserver' in window) {
            const imageObserver = new IntersectionObserver((entries, observer) => {
                entries.forEach(entry => {
                    if (entry.isIntersecting) {
                        const img = entry.target;
                        if (img.dataset.src) {
                            img.src = img.dataset.src;
                            img.removeAttribute('data-src');
                            observer.unobserve(img);
                        }
                    }
                });
            }, {
                rootMargin: '50px'
            });

            document.querySelectorAll('img[data-src]').forEach(img => {
                imageObserver.observe(img);
            });
        }
    }

    setupTouchOptimizations() {
        if (!this.touchDevice) return;

        // Быстрый клик для iOS
        document.addEventListener('touchstart', function() {}, { passive: true });

        // Предотвращение двойного тапа для зума
        let lastTouchEnd = 0;
        document.addEventListener('touchend', (e) => {
            const now = Date.now();
            if (now - lastTouchEnd <= 300) {
                e.preventDefault();
            }
            lastTouchEnd = now;
        }, false);

        // Улучшенная прокрутка
        document.addEventListener('touchmove', function() {}, { passive: true });
    }

    triggerBreakpointChange(breakpoint) {
        const event = new CustomEvent('breakpointChange', {
            detail: { breakpoint: breakpoint }
        });
        window.dispatchEvent(event);
    }

    triggerOrientationChange(orientation) {
        const event = new CustomEvent('orientationChange', {
            detail: { orientation: orientation }
        });
        window.dispatchEvent(event);
    }

    // Утилиты для адаптивных изображений
    getResponsiveImageSrc(basePath, sizes = {}) {
        const defaultSizes = {
            xs: '_mobile',
            sm: '_mobile',
            md: '_tablet',
            lg: '',
            xl: '',
            xxl: '_large'
        };

        const sizeMap = { ...defaultSizes, ...sizes };
        const suffix = sizeMap[this.currentBreakpoint] || '';
        
        const ext = basePath.split('.').pop();
        const base = basePath.substring(0, basePath.lastIndexOf('.'));
        
        return `${base}${suffix}.${ext}`;
    }

    // Адаптивная загрузка контента
    loadContentForBreakpoint(contentMap) {
        const content = contentMap[this.currentBreakpoint] || 
                       contentMap['default'] || 
                       '';
        return content;
    }

    // Проверка поддержки функций
    supportsFeature(feature) {
        const features = {
            'touch': this.touchDevice,
            'webp': this.supportsWebP(),
            'intersection-observer': 'IntersectionObserver' in window,
            'service-worker': 'serviceWorker' in navigator,
            'web-share': 'share' in navigator,
            'notifications': 'Notification' in window,
            'geolocation': 'geolocation' in navigator
        };

        return features[feature] || false;
    }

    supportsWebP() {
        const canvas = document.createElement('canvas');
        if (canvas.getContext && canvas.getContext('2d')) {
            return canvas.toDataURL('image/webp').indexOf('data:image/webp') === 0;
        }
        return false;
    }

    // Адаптивные модальные окна
    showResponsiveModal(content, options = {}) {
        const modal = document.createElement('div');
        modal.className = 'modal fade';
        
        const dialogClass = this.isMobile() ? 
            'modal-dialog modal-fullscreen-sm-down' : 
            'modal-dialog modal-dialog-centered';
        
        modal.innerHTML = `
            <div class="${dialogClass}">
                <div class="modal-content">
                    <div class="modal-header">
                        <h5 class="modal-title">${options.title || ''}</h5>
                        <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
                    </div>
                    <div class="modal-body">
                        ${content}
                    </div>
                    ${options.footer ? `<div class="modal-footer">${options.footer}</div>` : ''}
                </div>
            </div>
        `;

        document.body.appendChild(modal);
        const bsModal = new bootstrap.Modal(modal);
        bsModal.show();

        modal.addEventListener('hidden.bs.modal', () => {
            modal.remove();
        });

        return bsModal;
    }

    // Адаптивные уведомления
    showResponsiveToast(message, type = 'info') {
        if (window.ChessCalendar && window.ChessCalendar.showToast) {
            window.ChessCalendar.showToast(message, type);
        }
    }

    // Получить информацию об устройстве
    getDeviceInfo() {
        return {
            breakpoint: this.currentBreakpoint,
            orientation: this.orientation,
            isMobile: this.isMobile(),
            isTablet: this.isTablet(),
            isDesktop: this.isDesktop(),
            touchDevice: this.touchDevice,
            screenWidth: window.innerWidth,
            screenHeight: window.innerHeight,
            pixelRatio: window.devicePixelRatio || 1,
            userAgent: navigator.userAgent
        };
    }

    // Логирование информации об устройстве
    logDeviceInfo() {
        const info = this.getDeviceInfo();
        console.table(info);
    }
}

// Дополнительные стили для адаптивного менеджера
const style = document.createElement('style');
style.textContent = `
    /* Фикс высоты viewport для мобильных */
    .full-height {
        height: 100vh;
        height: calc(var(--vh, 1vh) * 100);
    }

    /* Компактные карточки */
    .card-compact .card-body {
        padding: 0.75rem;
    }

    .card-compact .card-title {
        font-size: 0.95rem;
        margin-bottom: 0.5rem;
    }

    /* Адаптивные изображения */
    img[data-src] {
        background: var(--bg-secondary);
        min-height: 100px;
    }

    /* Плавная загрузка изображений */
    img {
        transition: opacity 0.3s ease;
    }

    img[data-src] {
        opacity: 0.5;
    }

    /* Индикатор загрузки для изображений */
    .image-loading {
        position: relative;
    }

    .image-loading::after {
        content: '';
        position: absolute;
        top: 50%;
        left: 50%;
        width: 30px;
        height: 30px;
        margin: -15px 0 0 -15px;
        border: 3px solid var(--border-color);
        border-top-color: var(--primary-color);
        border-radius: 50%;
        animation: spin 0.8s linear infinite;
    }

    /* Оптимизация для тачскрина */
    .touch-device .btn,
    .touch-device .nav-link,
    .touch-device a {
        cursor: pointer;
    }

    /* Улучшенная прокрутка на мобильных */
    .device-mobile {
        -webkit-overflow-scrolling: touch;
    }

    /* Адаптивные отступы */
    @media (max-width: 576px) {
        .container,
        .container-fluid {
            padding-left: 1rem;
            padding-right: 1rem;
        }
    }
`;
document.head.appendChild(style);

// Инициализация
document.addEventListener('DOMContentLoaded', () => {
    window.ChessCalendar = window.ChessCalendar || {};
    window.ChessCalendar.responsiveManager = new ResponsiveManager();
    
    // Логируем информацию об устройстве в консоль
    if (window.location.search.includes('debug=true')) {
        window.ChessCalendar.responsiveManager.logDeviceInfo();
    }
});

// Экспорт для использования в других модулях
if (typeof module !== 'undefined' && module.exports) {
    module.exports = ResponsiveManager;
}
