/**
 * Lazy Loading для карточек турниров
 * Оптимизация загрузки изображений и контента
 */

class LazyLoader {
    constructor(options = {}) {
        this.options = {
            rootMargin: options.rootMargin || '50px',
            threshold: options.threshold || 0.01,
            loadingClass: options.loadingClass || 'lazy-loading',
            loadedClass: options.loadedClass || 'lazy-loaded',
            errorClass: options.errorClass || 'lazy-error'
        };
        
        this.observer = null;
        this.init();
    }

    init() {
        // Проверка поддержки IntersectionObserver
        if (!('IntersectionObserver' in window)) {
            this.loadAllImages();
            return;
        }

        this.observer = new IntersectionObserver(
            (entries) => this.handleIntersection(entries),
            {
                rootMargin: this.options.rootMargin,
                threshold: this.options.threshold
            }
        );

        this.observeImages();
        this.observeCards();
    }

    /**
     * Наблюдение за изображениями
     */
    observeImages() {
        const images = document.querySelectorAll('img[data-src], img[data-srcset]');
        images.forEach(img => {
            img.classList.add(this.options.loadingClass);
            this.observer.observe(img);
        });
    }

    /**
     * Наблюдение за карточками
     */
    observeCards() {
        const cards = document.querySelectorAll('[data-lazy-load]');
        cards.forEach(card => {
            card.classList.add(this.options.loadingClass);
            this.observer.observe(card);
        });
    }

    /**
     * Обработка пересечения элементов
     */
    handleIntersection(entries) {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const element = entry.target;
                
                if (element.tagName === 'IMG') {
                    this.loadImage(element);
                } else {
                    this.loadCard(element);
                }
                
                this.observer.unobserve(element);
            }
        });
    }

    /**
     * Загрузка изображения
     */
    loadImage(img) {
        const src = img.dataset.src;
        const srcset = img.dataset.srcset;

        if (!src && !srcset) {
            return;
        }

        img.classList.remove(this.options.loadingClass);

        // Создаем временное изображение для предзагрузки
        const tempImg = new Image();
        
        tempImg.onload = () => {
            if (srcset) {
                img.srcset = srcset;
            }
            if (src) {
                img.src = src;
            }
            
            img.classList.add(this.options.loadedClass);
            
            // Удаляем data-атрибуты
            delete img.dataset.src;
            delete img.dataset.srcset;
        };

        tempImg.onerror = () => {
            img.classList.add(this.options.errorClass);
            img.alt = 'Ошибка загрузки изображения';
        };

        if (src) {
            tempImg.src = src;
        }
    }

    /**
     * Загрузка карточки
     */
    loadCard(card) {
        card.classList.remove(this.options.loadingClass);
        card.classList.add(this.options.loadedClass);
        
        // Анимация появления
        card.style.opacity = '0';
        card.style.transform = 'translateY(20px)';
        
        requestAnimationFrame(() => {
            card.style.transition = 'opacity 0.3s ease, transform 0.3s ease';
            card.style.opacity = '1';
            card.style.transform = 'translateY(0)';
        });
    }

    /**
     * Загрузка всех изображений (fallback для старых браузеров)
     */
    loadAllImages() {
        const images = document.querySelectorAll('img[data-src]');
        images.forEach(img => {
            if (img.dataset.src) {
                img.src = img.dataset.src;
                delete img.dataset.src;
            }
            if (img.dataset.srcset) {
                img.srcset = img.dataset.srcset;
                delete img.dataset.srcset;
            }
        });

        const cards = document.querySelectorAll('[data-lazy-load]');
        cards.forEach(card => {
            card.classList.add(this.options.loadedClass);
        });
    }

    /**
     * Обновление наблюдателя (для динамически добавленных элементов)
     */
    refresh() {
        if (this.observer) {
            this.observeImages();
            this.observeCards();
        }
    }

    /**
     * Уничтожение наблюдателя
     */
    destroy() {
        if (this.observer) {
            this.observer.disconnect();
            this.observer = null;
        }
    }
}

/**
 * Infinite Scroll для турниров
 */
class InfiniteScroll {
    constructor(options = {}) {
        this.options = {
            container: options.container || '.tournaments-grid',
            loadMoreBtn: options.loadMoreBtn || '#loadMoreBtn',
            threshold: options.threshold || 200,
            autoLoad: options.autoLoad !== false
        };
        
        this.loading = false;
        this.hasMore = true;
        this.currentPage = 1;
        
        this.init();
    }

    init() {
        if (this.options.autoLoad) {
            this.setupScrollListener();
        }
        
        this.setupLoadMoreButton();
    }

    /**
     * Настройка слушателя прокрутки
     */
    setupScrollListener() {
        let scrollTimeout;
        
        window.addEventListener('scroll', () => {
            if (scrollTimeout) {
                clearTimeout(scrollTimeout);
            }
            
            scrollTimeout = setTimeout(() => {
                this.checkScroll();
            }, 100);
        });
    }

    /**
     * Проверка позиции прокрутки
     */
    checkScroll() {
        if (this.loading || !this.hasMore) {
            return;
        }

        const scrollTop = window.pageYOffset || document.documentElement.scrollTop;
        const windowHeight = window.innerHeight;
        const documentHeight = document.documentElement.scrollHeight;

        if (scrollTop + windowHeight >= documentHeight - this.options.threshold) {
            this.loadMore();
        }
    }

    /**
     * Настройка кнопки "Загрузить еще"
     */
    setupLoadMoreButton() {
        const btn = document.querySelector(this.options.loadMoreBtn);
        if (btn) {
            btn.addEventListener('click', () => this.loadMore());
        }
    }

    /**
     * Загрузка дополнительных турниров
     */
    async loadMore() {
        if (this.loading || !this.hasMore) {
            return;
        }

        this.loading = true;
        this.showLoading();

        try {
            const nextPage = this.currentPage + 1;
            const url = new URL(window.location.href);
            url.searchParams.set('page', nextPage);

            const response = await fetch(url.toString(), {
                headers: {
                    'X-Requested-With': 'XMLHttpRequest'
                }
            });

            if (!response.ok) {
                throw new Error('Failed to load tournaments');
            }

            const html = await response.text();
            const parser = new DOMParser();
            const doc = parser.parseFromString(html, 'text/html');
            
            const newCards = doc.querySelectorAll('.tournament-card-modern');
            
            if (newCards.length === 0) {
                this.hasMore = false;
                this.hideLoadMoreButton();
            } else {
                this.appendCards(newCards);
                this.currentPage = nextPage;
                
                // Обновляем lazy loader
                if (window.lazyLoader) {
                    window.lazyLoader.refresh();
                }
                
                // Обновляем tournament card manager
                if (window.tournamentCardManager) {
                    window.tournamentCardManager.initializeCards();
                }
            }

        } catch (error) {
            console.error('Error loading more tournaments:', error);
            this.showError();
        } finally {
            this.loading = false;
            this.hideLoading();
        }
    }

    /**
     * Добавление карточек в контейнер
     */
    appendCards(cards) {
        const container = document.querySelector(this.options.container);
        if (!container) {
            return;
        }

        const fragment = document.createDocumentFragment();
        cards.forEach(card => {
            const clone = card.cloneNode(true);
            fragment.appendChild(clone);
        });

        container.appendChild(fragment);
    }

    /**
     * Показать индикатор загрузки
     */
    showLoading() {
        const btn = document.querySelector(this.options.loadMoreBtn);
        if (btn) {
            btn.disabled = true;
            btn.innerHTML = '<span class="spinner-border spinner-border-sm me-2"></span>Загрузка...';
        }
    }

    /**
     * Скрыть индикатор загрузки
     */
    hideLoading() {
        const btn = document.querySelector(this.options.loadMoreBtn);
        if (btn) {
            btn.disabled = false;
            btn.innerHTML = '<i class="bi bi-arrow-down-circle"></i> Загрузить еще';
        }
    }

    /**
     * Скрыть кнопку "Загрузить еще"
     */
    hideLoadMoreButton() {
        const btn = document.querySelector(this.options.loadMoreBtn);
        if (btn) {
            btn.style.display = 'none';
        }
        
        // Показать сообщение
        const container = document.querySelector(this.options.container);
        if (container) {
            const message = document.createElement('div');
            message.className = 'text-center text-muted py-4';
            message.innerHTML = '<i class="bi bi-check-circle"></i> Все турниры загружены';
            container.parentElement.appendChild(message);
        }
    }

    /**
     * Показать ошибку
     */
    showError() {
        const container = document.querySelector(this.options.container);
        if (container) {
            const error = document.createElement('div');
            error.className = 'alert alert-danger mt-3';
            error.innerHTML = '<i class="bi bi-exclamation-triangle"></i> Ошибка загрузки турниров. Попробуйте еще раз.';
            container.parentElement.appendChild(error);
            
            setTimeout(() => error.remove(), 5000);
        }
    }
}

// Инициализация при загрузке страницы
document.addEventListener('DOMContentLoaded', () => {
    // Инициализация lazy loading
    window.lazyLoader = new LazyLoader({
        rootMargin: '100px',
        threshold: 0.01
    });

    // Инициализация infinite scroll (опционально)
    const enableInfiniteScroll = document.body.dataset.infiniteScroll === 'true';
    if (enableInfiniteScroll) {
        window.infiniteScroll = new InfiniteScroll({
            autoLoad: true
        });
    }
});

// Экспорт для использования в других модулях
if (typeof module !== 'undefined' && module.exports) {
    module.exports = { LazyLoader, InfiniteScroll };
}
