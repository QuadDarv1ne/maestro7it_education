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
        return `${base}_${size}.${format}`;
    }

    getImageSize(width) {
        const dpr = this.devicePixelRatio;
        const actualWidth = width * dpr;
        
        if (actualWidth <= 320) return 'xs';
        if (actualWidth <= 640) return 'sm';
        if (actualWidth <= 768) return 'md';
        if (actualWidth <= 1024) return 'lg';
        if (actualWidth <= 1366) return 'xl';
        return 'xxl';
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

            const srcset = this.generateSrcset(src);
            img.srcset = srcset;
            img.sizes = this.generateSizes();
        });
    }

    generateSrcset(src) {
        const ext = src.split('.').pop();
        const base = src.substring(0, src.lastIndexOf('.'));
        
        const sizes = ['xs', 'sm', 'md', 'lg', 'xl', 'xxl'];
        const widths = [320, 640, 768, 1024, 1366, 1920];
        
        return sizes.map((size, index) => {
            return `${base}_${size}.${ext} ${widths[index]}w`;
        }).join(', ');
    }

    generateSizes() {
        return '(max-width: 576px) 100vw, (max-width: 768px) 50vw, (max-width: 992px) 33vw, 25vw';
    }

    setupImageOptimization() {
        // Оптимизация загрузки изображений
        document.querySelectorAll('img').forEach(img => {
            // Добавляем loading="lazy" для нативной ленивой загрузки
            if (!img.loading) {
                img.loading = 'lazy';
            }
            
            // Добавляем decoding="async" для асинхронной декодировки
            if (!img.decoding) {
                img.decoding = 'async';
            }
        });
    }

    setupImagePlaceholders() {
        // Создаём blur placeholder для изображений
        document.querySelectorAll('img[data-placeholder]').forEach(img => {
            const placeholder = img.dataset.placeholder;
            
            // Создаём временное изображение с низким разрешением
            const tempImg = new Image();
            tempImg.src = placeholder;
            tempImg.style.filter = 'blur(10px)';
            tempImg.style.transform = 'scale(1.1)';
            
            img.parentNode.insertBefore(tempImg, img);
            
            // Удаляем placeholder после загрузки основного изображения
            img.addEventListener('load', () => {
                tempImg.style.opacity = '0';
                setTimeout(() => tempImg.remove(), 300);
            });
        });
    }

    loadAllImages() {
        // Загружаем все изображения (fallback для старых браузеров)
        document.querySelectorAll('img[data-src]').forEach(img => {
            img.src = img.dataset.src;
            delete img.dataset.src;
        });
    }

    // Предзагрузка критических изображений
    preloadImages(urls) {
        urls.forEach(url => {
            const link = document.createElement('link');
            link.rel = 'preload';
            link.as = 'image';
            link.href = url;
            document.head.appendChild(link);
        });
    }

    // Получить оптимальный формат изображения
    getOptimalFormat() {
        if (this.supportsAvif) return 'avif';
        if (this.supportsWebP) return 'webp';
        return 'jpg';
    }

    // Конвертировать URL изображения в оптимальный формат
    convertImageUrl(url, format = null) {
        const targetFormat = format || this.getOptimalFormat();
        const ext = url.split('.').pop();
        const base = url.substring(0, url.lastIndexOf('.'));
        return `${base}.${targetFormat}`;
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
        background: linear-gradient(
            90deg,
            var(--bg-secondary) 0%,
            var(--bg-tertiary) 50%,
            var(--bg-secondary) 100%
        );
        background-size: 200% 100%;
        animation: shimmer 1.5s infinite;
        min-height: 200px;
    }

    @keyframes shimmer {
        0% { background-position: -200% 0; }
        100% { background-position: 200% 0; }
    }

    /* Состояние загружено */
    img.loaded {
        animation: fadeIn 0.3s ease-in;
    }

    @keyframes fadeIn {
        from { opacity: 0; }
        to { opacity: 1; }
    }

    /* Состояние ошибки */
    img.error {
        background: var(--bg-secondary);
        position: relative;
        min-height: 200px;
    }

    img.error::after {
        content: '⚠️ Ошибка загрузки';
        position: absolute;
        top: 50%;
        left: 50%;
        transform: translate(-50%, -50%);
        color: var(--text-muted);
        font-size: 0.875rem;
    }

    /* Aspect ratio контейнеры */
    .img-container {
        position: relative;
        overflow: hidden;
        background: var(--bg-secondary);
    }

    .img-container::before {
        content: '';
        display: block;
        padding-top: 56.25%; /* 16:9 по умолчанию */
    }

    .img-container.ratio-1-1::before {
        padding-top: 100%; /* 1:1 */
    }

    .img-container.ratio-4-3::before {
        padding-top: 75%; /* 4:3 */
    }

    .img-container.ratio-16-9::before {
        padding-top: 56.25%; /* 16:9 */
    }

    .img-container.ratio-21-9::before {
        padding-top: 42.86%; /* 21:9 */
    }

    .img-container img {
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        object-fit: cover;
    }

    /* Адаптивные background images */
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

    /* Picture element стили */
    picture {
        display: block;
    }

    picture img {
        width: 100%;
        height: auto;
    }

    /* Оптимизация для печати */
    @media print {
        img {
            max-width: 100% !important;
            page-break-inside: avoid;
        }
    }

    /* Высокий DPR */
    @media (-webkit-min-device-pixel-ratio: 2), (min-resolution: 192dpi) {
        img {
            image-rendering: -webkit-optimize-contrast;
            image-rendering: crisp-edges;
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
