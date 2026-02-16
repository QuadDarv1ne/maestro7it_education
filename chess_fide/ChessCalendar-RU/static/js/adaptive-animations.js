/**
 * Adaptive Animations Module
 * Адаптивные анимации с учётом производительности и предпочтений пользователя
 */

class AdaptiveAnimations {
    constructor() {
        this.prefersReducedMotion = false;
        this.performanceLevel = 'high';
        this.animations = new Map();
        this.observers = new Map();
        
        this.init();
    }

    init() {
        console.log('[AdaptiveAnimations] Инициализация адаптивных анимаций');
        
        this.detectMotionPreference();
        this.detectPerformanceLevel();
        this.setupAnimationObservers();
        this.setupScrollAnimations();
        this.setupHoverAnimations();
        this.setupTransitionOptimizations();
    }

    detectMotionPreference() {
        // Проверяем предпочтения пользователя
        const mediaQuery = window.matchMedia('(prefers-reduced-motion: reduce)');
        this.prefersReducedMotion = mediaQuery.matches;
        
        console.log('[AdaptiveAnimations] Reduced motion:', this.prefersReducedMotion);
        
        // Слушаем изменения
        mediaQuery.addEventListener('change', (e) => {
            this.prefersReducedMotion = e.matches;
            this.updateAnimations();
        });
        
        // Применяем класс к body
        if (this.prefersReducedMotion) {
            document.body.classList.add('reduced-motion');
        }
    }

    detectPerformanceLevel() {
        // Определяем уровень производительности устройства
        const connection = navigator.connection || navigator.mozConnection || navigator.webkitConnection;
        const memory = navigator.deviceMemory;
        const cores = navigator.hardwareConcurrency;
        
        // Низкая производительность
        if (
            (connection && connection.saveData) ||
            (memory && memory < 4) ||
            (cores && cores < 4)
        ) {
            this.performanceLevel = 'low';
        }
        // Средняя производительность
        else if (
            (memory && memory < 8) ||
            (cores && cores < 8)
        ) {
            this.performanceLevel = 'medium';
        }
        // Высокая производительность
        else {
            this.performanceLevel = 'high';
        }
        
        console.log('[AdaptiveAnimations] Performance level:', this.performanceLevel);
        document.body.classList.add(`performance-${this.performanceLevel}`);
    }

    setupAnimationObservers() {
        if (!('IntersectionObserver' in window)) {
            console.warn('[AdaptiveAnimations] IntersectionObserver не поддерживается');
            return;
        }

        // Наблюдатель для анимаций при появлении
        const appearObserver = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    this.animateElement(entry.target, 'appear');
                }
            });
        }, {
            threshold: 0.1,
            rootMargin: '0px 0px -50px 0px'
        });

        // Наблюдаем за элементами с data-animate
        document.querySelectorAll('[data-animate]').forEach(el => {
            appearObserver.observe(el);
        });

        this.observers.set('appear', appearObserver);
    }

    animateElement(element, type) {
        if (this.prefersReducedMotion) {
            element.classList.add('no-animation');
            return;
        }

        const animationType = element.dataset.animate || 'fade-in';
        const delay = element.dataset.animateDelay || 0;
        const duration = this.getAnimationDuration(element.dataset.animateDuration);

        setTimeout(() => {
            element.style.animationDuration = duration;
            element.classList.add('animated', `animate-${animationType}`);
            
            // Удаляем класс после завершения анимации
            element.addEventListener('animationend', () => {
                element.classList.remove('animated', `animate-${animationType}`);
                element.classList.add('animation-complete');
            }, { once: true });
        }, delay);
    }

    getAnimationDuration(customDuration) {
        if (customDuration) return customDuration;
        
        // Адаптируем длительность в зависимости от производительности
        switch (this.performanceLevel) {
            case 'low':
                return '0.2s';
            case 'medium':
                return '0.3s';
            case 'high':
            default:
                return '0.5s';
        }
    }

    setupScrollAnimations() {
        // Параллакс эффект для фоновых элементов
        if (this.performanceLevel === 'high' && !this.prefersReducedMotion) {
            let ticking = false;
            
            window.addEventListener('scroll', () => {
                if (!ticking) {
                    window.requestAnimationFrame(() => {
                        this.updateParallax();
                        ticking = false;
                    });
                    ticking = true;
                }
            }, { passive: true });
        }

        // Fade out при прокрутке
        document.querySelectorAll('[data-scroll-fade]').forEach(el => {
            this.setupScrollFade(el);
        });
    }

    updateParallax() {
        const scrolled = window.pageYOffset;
        
        document.querySelectorAll('[data-parallax]').forEach(el => {
            const speed = parseFloat(el.dataset.parallax) || 0.5;
            const yPos = -(scrolled * speed);
            el.style.transform = `translate3d(0, ${yPos}px, 0)`;
        });
    }

    setupScrollFade(element) {
        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                const ratio = entry.intersectionRatio;
                element.style.opacity = ratio;
            });
        }, {
            threshold: Array.from({ length: 101 }, (_, i) => i / 100)
        });

        observer.observe(element);
    }

    setupHoverAnimations() {
        if (this.prefersReducedMotion) return;

        // Добавляем hover эффекты для карточек
        document.querySelectorAll('.card, .btn, .nav-link').forEach(el => {
            if (!el.classList.contains('no-hover')) {
                el.classList.add('hover-lift');
            }
        });
    }

    setupTransitionOptimizations() {
        // Оптимизируем transitions для лучшей производительности
        if (this.performanceLevel === 'low') {
            // Отключаем сложные transitions
            document.body.classList.add('simple-transitions');
        }
    }

    updateAnimations() {
        if (this.prefersReducedMotion) {
            document.body.classList.add('reduced-motion');
            // Останавливаем все анимации
            document.querySelectorAll('.animated').forEach(el => {
                el.classList.remove('animated');
                el.classList.add('no-animation');
            });
        } else {
            document.body.classList.remove('reduced-motion');
        }
    }

    // Программная анимация элемента
    animate(element, animation, options = {}) {
        if (this.prefersReducedMotion && !options.force) {
            return Promise.resolve();
        }

        return new Promise((resolve) => {
            const duration = options.duration || this.getAnimationDuration();
            const delay = options.delay || 0;
            const easing = options.easing || 'ease';

            element.style.animation = `${animation} ${duration} ${easing} ${delay}ms`;
            
            const handleAnimationEnd = () => {
                element.style.animation = '';
                resolve();
            };

            element.addEventListener('animationend', handleAnimationEnd, { once: true });
        });
    }

    // Плавное появление элемента
    fadeIn(element, duration = 300) {
        if (this.prefersReducedMotion) {
            element.style.opacity = '1';
            return Promise.resolve();
        }

        return new Promise((resolve) => {
            element.style.opacity = '0';
            element.style.transition = `opacity ${duration}ms ease`;
            
            requestAnimationFrame(() => {
                element.style.opacity = '1';
                setTimeout(resolve, duration);
            });
        });
    }

    // Плавное исчезновение элемента
    fadeOut(element, duration = 300) {
        if (this.prefersReducedMotion) {
            element.style.opacity = '0';
            return Promise.resolve();
        }

        return new Promise((resolve) => {
            element.style.transition = `opacity ${duration}ms ease`;
            element.style.opacity = '0';
            setTimeout(resolve, duration);
        });
    }

    // Slide анимация
    slideIn(element, direction = 'left', duration = 300) {
        if (this.prefersReducedMotion) {
            element.style.transform = 'none';
            return Promise.resolve();
        }

        return new Promise((resolve) => {
            const transforms = {
                left: 'translateX(-100%)',
                right: 'translateX(100%)',
                up: 'translateY(-100%)',
                down: 'translateY(100%)'
            };

            element.style.transform = transforms[direction];
            element.style.transition = `transform ${duration}ms ease`;
            
            requestAnimationFrame(() => {
                element.style.transform = 'none';
                setTimeout(resolve, duration);
            });
        });
    }

    // Scale анимация
    scale(element, from = 0, to = 1, duration = 300) {
        if (this.prefersReducedMotion) {
            element.style.transform = `scale(${to})`;
            return Promise.resolve();
        }

        return new Promise((resolve) => {
            element.style.transform = `scale(${from})`;
            element.style.transition = `transform ${duration}ms ease`;
            
            requestAnimationFrame(() => {
                element.style.transform = `scale(${to})`;
                setTimeout(resolve, duration);
            });
        });
    }

    // Shake анимация
    shake(element, intensity = 10) {
        if (this.prefersReducedMotion) {
            return Promise.resolve();
        }

        return this.animate(element, `shake-${intensity}`, { duration: '0.5s' });
    }

    // Pulse анимация
    pulse(element, scale = 1.05) {
        if (this.prefersReducedMotion) {
            return Promise.resolve();
        }

        return this.animate(element, 'pulse', { duration: '0.5s' });
    }

    // Bounce анимация
    bounce(element) {
        if (this.prefersReducedMotion) {
            return Promise.resolve();
        }

        return this.animate(element, 'bounce', { duration: '0.5s' });
    }

    // Создание пользовательской анимации
    createAnimation(name, keyframes) {
        const styleSheet = document.createElement('style');
        styleSheet.textContent = `
            @keyframes ${name} {
                ${keyframes}
            }
        `;
        document.head.appendChild(styleSheet);
        
        this.animations.set(name, styleSheet);
    }

    // Удаление анимации
    removeAnimation(name) {
        const styleSheet = this.animations.get(name);
        if (styleSheet) {
            styleSheet.remove();
            this.animations.delete(name);
        }
    }
}

// Стили для анимаций
const style = document.createElement('style');
style.textContent = `
    /* Базовые анимации */
    @keyframes fade-in {
        from {
            opacity: 0;
        }
        to {
            opacity: 1;
        }
    }

    @keyframes fade-in-up {
        from {
            opacity: 0;
            transform: translateY(30px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }

    @keyframes fade-in-down {
        from {
            opacity: 0;
            transform: translateY(-30px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }

    @keyframes fade-in-left {
        from {
            opacity: 0;
            transform: translateX(-30px);
        }
        to {
            opacity: 1;
            transform: translateX(0);
        }
    }

    @keyframes fade-in-right {
        from {
            opacity: 0;
            transform: translateX(30px);
        }
        to {
            opacity: 1;
            transform: translateX(0);
        }
    }

    @keyframes scale-in {
        from {
            opacity: 0;
            transform: scale(0.8);
        }
        to {
            opacity: 1;
            transform: scale(1);
        }
    }

    @keyframes slide-in-up {
        from {
            transform: translateY(100%);
        }
        to {
            transform: translateY(0);
        }
    }

    @keyframes slide-in-down {
        from {
            transform: translateY(-100%);
        }
        to {
            transform: translateY(0);
        }
    }

    @keyframes bounce {
        0%, 20%, 50%, 80%, 100% {
            transform: translateY(0);
        }
        40% {
            transform: translateY(-20px);
        }
        60% {
            transform: translateY(-10px);
        }
    }

    @keyframes pulse {
        0%, 100% {
            transform: scale(1);
        }
        50% {
            transform: scale(1.05);
        }
    }

    @keyframes shake-10 {
        0%, 100% {
            transform: translateX(0);
        }
        10%, 30%, 50%, 70%, 90% {
            transform: translateX(-10px);
        }
        20%, 40%, 60%, 80% {
            transform: translateX(10px);
        }
    }

    @keyframes rotate-in {
        from {
            opacity: 0;
            transform: rotate(-180deg);
        }
        to {
            opacity: 1;
            transform: rotate(0);
        }
    }

    /* Применение анимаций */
    .animate-fade-in {
        animation-name: fade-in;
    }

    .animate-fade-in-up {
        animation-name: fade-in-up;
    }

    .animate-fade-in-down {
        animation-name: fade-in-down;
    }

    .animate-fade-in-left {
        animation-name: fade-in-left;
    }

    .animate-fade-in-right {
        animation-name: fade-in-right;
    }

    .animate-scale-in {
        animation-name: scale-in;
    }

    .animate-slide-in-up {
        animation-name: slide-in-up;
    }

    .animate-slide-in-down {
        animation-name: slide-in-down;
    }

    .animate-bounce {
        animation-name: bounce;
    }

    .animate-pulse {
        animation-name: pulse;
    }

    .animate-rotate-in {
        animation-name: rotate-in;
    }

    /* Hover эффекты */
    .hover-lift {
        transition: transform 0.3s ease, box-shadow 0.3s ease;
    }

    .hover-lift:hover {
        transform: translateY(-5px);
        box-shadow: var(--box-shadow-lg);
    }

    .hover-scale {
        transition: transform 0.3s ease;
    }

    .hover-scale:hover {
        transform: scale(1.05);
    }

    .hover-glow {
        transition: box-shadow 0.3s ease;
    }

    .hover-glow:hover {
        box-shadow: 0 0 20px rgba(37, 99, 235, 0.5);
    }

    /* Reduced motion */
    @media (prefers-reduced-motion: reduce) {
        *,
        *::before,
        *::after {
            animation-duration: 0.01ms !important;
            animation-iteration-count: 1 !important;
            transition-duration: 0.01ms !important;
            scroll-behavior: auto !important;
        }
    }

    .reduced-motion * {
        animation: none !important;
        transition: none !important;
    }

    .no-animation {
        animation: none !important;
    }

    /* Performance optimizations */
    .performance-low .hover-lift:hover {
        transform: none;
    }

    .performance-low [data-parallax] {
        transform: none !important;
    }

    .simple-transitions * {
        transition-duration: 0.1s !important;
    }

    /* Parallax */
    [data-parallax] {
        will-change: transform;
        transform: translateZ(0);
    }

    /* Scroll fade */
    [data-scroll-fade] {
        transition: opacity 0.3s ease;
    }

    /* Animation delays */
    .delay-100 {
        animation-delay: 100ms;
    }

    .delay-200 {
        animation-delay: 200ms;
    }

    .delay-300 {
        animation-delay: 300ms;
    }

    .delay-400 {
        animation-delay: 400ms;
    }

    .delay-500 {
        animation-delay: 500ms;
    }
`;
document.head.appendChild(style);

// Инициализация
document.addEventListener('DOMContentLoaded', () => {
    window.ChessCalendar = window.ChessCalendar || {};
    window.ChessCalendar.adaptiveAnimations = new AdaptiveAnimations();
});

// Экспорт
if (typeof module !== 'undefined' && module.exports) {
    module.exports = AdaptiveAnimations;
}
