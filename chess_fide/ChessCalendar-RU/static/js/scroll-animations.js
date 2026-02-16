/**
 * Scroll Animations Module
 * Анимации при прокрутке страницы
 */

class ScrollAnimations {
    constructor() {
        this.elements = [];
        this.parallaxElements = [];
        this.progressBars = [];
        this.init();
    }

    init() {
        console.log('[ScrollAnimations] Инициализация scroll анимаций');
        
        this.setupScrollReveal();
        this.setupParallax();
        this.setupScrollProgress();
        this.setupSmoothScroll();
        this.setupScrollToTop();
        this.setupInfiniteScroll();
    }

    setupScrollReveal() {
        if (!('IntersectionObserver' in window)) {
            console.warn('[ScrollAnimations] IntersectionObserver не поддерживается');
            return;
        }

        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    entry.target.classList.add('revealed');
                    
                    // Опционально: отключаем наблюдение после появления
                    if (entry.target.dataset.revealOnce !== 'false') {
                        observer.unobserve(entry.target);
                    }
                } else {
                    // Скрываем снова если revealOnce = false
                    if (entry.target.dataset.revealOnce === 'false') {
                        entry.target.classList.remove('revealed');
                    }
                }
            });
        }, {
            threshold: 0.1,
            rootMargin: '0px 0px -50px 0px'
        });

        // Наблюдаем за элементами с классом 