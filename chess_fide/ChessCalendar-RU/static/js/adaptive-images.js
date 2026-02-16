/**
 * Adaptive Images Module
 * Адаптивная загрузка изображений с поддержкой srcset и WebP
 */

class AdaptiveImages {
    constructor() {
        this.supportsWebP = false;
        this.supportsAvif = false;
        this.devicePixelRatio = window.devicePixelRatio || 1;
        this.init();
    }

    async init() {
        console.log('[AdaptiveImages] Инициализация адаптивных изображений');
        
        // Проверяем поддержку форматов
        this.supportsWebP = await this.checkWebPSupport();
        this.supportsAvif = await this.checkAvifSupport();
        
        console.log('[AdaptiveImages] WebP:', this.supportsWebP);
        console.log('[AdaptiveImages] AVIF:', this.supportsAvif);
        console.log('[AdaptiveImages] DPR:', this.devicePixelRatio);
        
        this.setupLazyLoading();
        this.setupResponsiveImages();
        this.setupImageOptimization();
        this.setupImagePlaceholders();
    }

    async checkWebPSupport() {
        return new Promise((resolve) => {
            const webP = new Image();
            webP.onload = webP.onerror = () => {
                resolve(webP.height === 2);
            };
            webP.src = 'data:image/webp;base64,UklGRjoAAABXRUJQVlA4IC4AAACyAgCdASoCAAIALmk0mk0iIiIiIgBoSygABc6WWgAA/veff/0PP8bA//LwYAAA';
        });
    }

    async checkAvifSupport() {
        return new Promise((resolve) => {
            const avif = new Image();
            avif.onload = avif.onerror = () => {
                resolve(avif.height === 2);
            };
            avif.src = 'data:image/avif;base64,AAAAIGZ0eXBhdmlmAAAAAGF2aWZtaWYxbWlhZk1BMUIAAADybWV0YQAAAAAAAAAoaGRscgAAAAAAAAAAcGljdAAAAAAAAAAAAAAAAGxpYmF2aWYAAAAADnBpdG0AAAAAAAEAAAAeaWxvYwAAAABEAAABAAEAAAABAAABGgAAAB0AAAAoaWluZgAAAAAAAQAAABppbmZlAgAAAAABAABhdjAxQ29sb3IAAAAAamlwcnAAAABLaXBjbwAAABRpc3BlAAAAAAAAAAIAAAACAAAAEHBpeGkAAAAAAwgICAAAAAxhdjFDgQ0MAAAAABNjb2xybmNseAACAAIAAYAAAAAXaXBtYQAAAAAAAAABAAEEAQKDBAAAACVtZGF0EgAKCBgANogQEAwgMg8f8D///8WfhwB8+ErK42A=';
        });
    }

    setupLazyLoading() {
        if (!('IntersectionObserver' in window)) {
            console.warn('[AdaptiveImages] IntersectionObserver не поддерживается');
            this.loadAllImages();
            return;
        }

        const imageObserver = new IntersectionObserver((entries, observer) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    const img = entry.target;
                    this.loadImage(img);
                    observer.unobserve(img);
                }
            });
        }, {
            rootMargin: '50px 0px',
            threshold: 0.01
        });

        // Наблюдаем за всеми изображениями с data-src
        document.querySelectorAll('img[data-src], img[data-srcset]').forEach(img => {
            imageObserver.observe(img);
        });

        // Наблюдаем за background images
        document.querySelectorAll('[data-bg]').forEach(el => {
            imageObserver.observe(el);
        });
    }

    loadImage(img) {
        // Показываем placeholder
        img.classList.add('loading');

        // Определяем оптимальный источник
        const src = this.getOptimalImageSrc(img);
        
        if (img.tagName === 'IMG') {
            // Загружаем изображение
            const tempImg = new Image();
            
            tempImg.onload = () => {
                img.src = src;
                if (img.dataset.srcset) {
                    img.srcset = this.getOptimalSrcset(img.dataset.srcset);
                }
                img.classList.remove('loading');
                img.classList.add('loaded');
                
                // Удаляем data атрибуты
                delete img.dataset.src;
                delete img.dataset.srcset;
            };
            
            tempImg.onerror = () => {
                console.error('[AdaptiveImages] Ошибка загрузки:', src);
                img.classList.remove('loading');
                img.classList.add('error');
            };
            
            tempImg.src = src;
        } else {
            // Background image
            const bgUrl = this.getOptimalImageSrc(img);
            img.style.backgroundImage = `url('${bgUrl}')`;
            img.classList.remove('loading');
            img.classList.add('loaded');
            delete img.dataset.bg;
        }
    }

    getOptimalImageSrc(element) {
        let src = element.dataset.src || element.dataset.bg;
        
        if (!src) return '';

        // Определяем размер изображения на основе viewport
        const width = element.offsetWidth || window.innerWidth;
        const size = this.getImageSize(width);
        
        // Добавляем суффикс размера
        const ext = src.split('.').pop();
        const base = src.substring(0, src.lastIndexOf('.'));
        
        // Определяем формат
        let format = ext;
        if (this.supportsAvif) {
            format = 'avif';
        } else if (this.supportsWebP) {
            format = 'webp';
        }
        
        // Формируем URL
        return `${base}${size}.${format}`;
    }

    getImageSize(width) {
        const dpr = this.devicePixelRatio;
        const actualWidth = width * dpr;
        
        if (actualWidth <= 320) return '_xs';
        if (actualWidth <= 640) return '_sm';
        if (actualWidth <= 768) return '_md';
        if (actualWidth <= 1024) return '_lg';
        if (actualWidth <= 1920) return '_xl';
        return '_xxl';
    }

    getOptimalSrcset(srcset) {
        // Преобразуем srcset с учётом поддерживаемых форматов
        const sources = srcset.split(',').map(s => s.trim());
        
        return sources.map(source => {
            const [url, descriptor] = source.split(' ');
            const ext = url.split('.').pop();
            const base = url.substring(0, url.lastIndexOf('.'));
            
            let format = ext;
            if (this.supportsAvif) {
                format = 'avif';
            } else if (this.supportsWebP) {
                format = 'webp';
            }
            
            return `${base}.${format} ${descriptor}`;
        }).join(', ');
    }

    setupResponsiveImages() {
        // Автоматически создаём srcset для изображений
        document.querySelectorAll('img[data-responsive]').forEach(img => {
            const src = img.src || img.dataset.src;
            if (!src) return;

            const ext = src.split('.').pop();
            const base = src.substring(0, src.lastIndexOf('.'));
            
            // Создаём srcset
            const srcset = [
                `${base}_xs.${ext} 320w`,
                `${base}_sm.${ext} 640w`,
                `${base}_md.${ext} 768w`,
                `${base}_lg.${ext} 1024w`,
                `${base}_xl.${ext} 1920w`
            ].join(', ');
            
            img.srcset = srcset;
            img.sizes = '(max-width: 576px) 100vw, (max-width: 768px) 50vw, (max-width: 992px) 33vw, 25vw';
        });
    }

    setupImageOptimization() {
        // Оптимизация изображений при изменении размера окна
        let resizeTimer;
        window.addEventListener('resize', () => {
            clearTimeout(resizeTimer);
            resizeTimer = setTimeout(() => {
                this.optimizeVisibleImages();
            }, 500);
        });
    }

    optimizeVisibleImages() {
        document.querySelectorAll('img.loaded').forEach(img => {
            const currentWidth = img.offsetWidth;
            const naturalWidth = img.naturalWidth;
            
            // Если изображение слишком большое, перезагружаем оптимальный размер
            if (naturalWidth > currentWidth * 2) {
                const optimalSrc = this.getOptimalImageSrc(img);
                if (optimalSrc !== img.src) {
                    img.src = optimalSrc;
                }
            }
        });
    }

    setupImagePlaceholders() {
        // Добавляем placeholder для изображений
        document.querySelectorAll('img[data-src]').forEach(img => {
            if (!img.src || img.src === window.location.href) {
                // Создаём SVG placeholder
                const width = img.dataset.width || 400;
                const height = img.dataset.height || 300;
                const placeholder = this.createPlaceholder(width, height);
                img.src = placeholder;
            }
        });
    }

    createPlaceholder(width, height) {
        const svg = `
            <svg xmlns="http://www.w3.org/2000/svg" width="${width}" height="${height}">
                <rect width="100%" height="100%" fill="#e2e8f0"/>
                <text x="50%" y="50%" font-family="Arial" font-size="14" fill="#94a3b8" 
                      text-anchor="middle" dominant-baseline="middle">
                    ${width}×${height}
                </text>
            </svg>
        `;
        return 'data:image/svg+xml;base64,' + btoa(svg);
    }

    loadAllImages() {
        // Загружаем все изображения (fallback для старых браузеров)
        document.querySelectorAll('img[data-src]').forEach(img => {
            this.loadImage(img);
        });
    }

    // Утилита для предзагрузки изображений
    preloadImage(src) {
        return new Promise((resolve, reject) => {
            const img = new Image();
            img.onload = () => resolve(img);
            img.onerror = reject;
            img.src = src;
        });
    }

    // Утилита для предзагрузки нескольких изображений
    async preloadImages(sources) {
        const promises = sources.map(src => this.preloadImage(src));
        return Promise.all(promises);
    }

    // Получить информацию об изображении
    getImageInfo(img) {
        return {
            src: img.src,
            naturalWidth: img.naturalWidth,
            naturalHeight: img.naturalHeight,
            displayWidth: img.offsetWidth,
            displayHeight: img.offsetHeight,
            aspectRatio: img.naturalWidth / img.naturalHeight,
            loaded: img.complete && img.naturalHeight !== 0,
            format: this.getImageFormat(img.src)
        };
    }

    getImageFormat(src) {
        const ext = src.split('.').pop().split('?')[0];
        return ext.toLowerCase();
    }

    // Конвертация изображения в другой формат (требует canvas)
    async convertImage(img, format = 'webp', quality = 0.8) {
        return new Promise((resolve, reject) => {
            const canvas = document.createElement('canvas');
            canvas.width = img.naturalWidth;
            canvas.height = img.naturalHeight;
            
            const ctx = canvas.getContext('2d');
            ctx.drawImage(img, 0, 0);
            
            canvas.toBlob((blob) => {
                if (blob) {
                    resolve(URL.createObjectURL(blob));
                } else {
                    reject(new Error('Не удалось конвертировать изображение'));
                }
            }, `image/${format}`, quality);
        });
    }
}

// Стили для адаптивных изображений
const style = document.createElement('style');
style.textContent = `
    /* Базовые стили для изображений */
    img {
        max-width: 100%;
        height: auto;
        display: block;
    }

    /* Состояние загрузки */
    img.loading {
        opacity: 0.5;
        background: linear-gradient(
            90deg,
            var(--bg-secondary) 0%,
            var(--bg-tertiary) 50%,
            var(--bg-secondary) 100%
        );
        background-size: 200% 100%;
        animation: shimmer 1.5s infinite;
    }

    @keyframes shimmer {
        0% {
            background-position: -200% 0;
        }
        100% {
            background-position: 200% 0;
        }
    }

    /* Состояние загружено */
    img.loaded {
        opacity: 1;
        transition: opacity 0.3s ease;
    }

    /* Состояние ошибки */
    img.error {
        opacity: 0.3;
        filter: grayscale(100%);
    }

    /* Адаптивные изображения */
    img[data-responsive] {
        width: 100%;
        height: auto;
        object-fit: cover;
    }

    /* Background images */
    [data-bg] {
        background-size: cover;
        background-position: center;
        background-repeat: no-repeat;
    }

    [data-bg].loading {
        background: linear-gradient(
            90deg,
            var(--bg-secondary) 0%,
            var(--bg-tertiary) 50%,
            var(--bg-secondary) 100%
        );
        background-size: 200% 100%;
        animation: shimmer 1.5s infinite;
    }

    /* Aspect ratio containers */
    .img-container {
        position: relative;
        overflow: hidden;
    }

    .img-container::before {
        content: '';
        display: block;
        padding-top: 75%; /* 4:3 по умолчанию */
    }

    .img-container.ratio-16-9::before {
        padding-top: 56.25%;
    }

    .img-container.ratio-1-1::before {
        padding-top: 100%;
    }

    .img-container.ratio-21-9::before {
        padding-top: 42.86%;
    }

    .img-container img {
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        object-fit: cover;
    }

    /* Оптимизация для печати */
    @media print {
        img.loading {
            display: none;
        }
    }
`;
document.head.appendChild(style);

// Инициализация
document.addEventListener('DOMContentLoaded', () => {
    window.ChessCalendar = window.ChessCalendar || {};
    window.ChessCalendar.adaptiveImages = new AdaptiveImages();
});

// Экспорт
if (typeof module !== 'undefined' && module.exports) {
    module.exports = AdaptiveImages;
}
