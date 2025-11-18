/**
 * Icon Loader - Проверка и загрузка иконочных шрифтов
 * Обеспечивает fallback если Font Awesome или Bootstrap Icons не загружены
 */

(function() {
    'use strict';

    // Конфигурация
    const CONFIG = {
        checkDelay: 100,
        maxRetries: 30,
        fontAwesomeTest: 'FontAwesome',
        bootstrapIconsTest: 'bootstrap-icons'
    };

    /**
     * Проверяет, загружен ли шрифт
     */
    function isFontLoaded(fontFamily) {
        // Создаем тестовый элемент
        const testString = 'mmmmmmmmmwwwwwww';
        const testSize = '72px';
        
        const canvas = document.createElement('canvas');
        const context = canvas.getContext('2d');
        
        // Измеряем ширину с базовым шрифтом
        context.font = testSize + ' monospace';
        const baselineWidth = context.measureText(testString).width;
        
        // Измеряем ширину с тестируемым шрифтом
        context.font = testSize + ' ' + fontFamily + ', monospace';
        const testWidth = context.measureText(testString).width;
        
        // Если ширина отличается, шрифт загружен
        return testWidth !== baselineWidth;
    }

    /**
     * Проверяет наличие Font Awesome
     */
    function checkFontAwesome() {
        // Проверяем несколько способов
        const methods = [
            // Метод 1: Проверка через DOM
            function() {
                const test = document.createElement('i');
                test.className = 'fas fa-check';
                test.style.position = 'absolute';
                test.style.left = '-9999px';
                document.body.appendChild(test);
                
                const computedStyle = window.getComputedStyle(test, ':before');
                const content = computedStyle.getPropertyValue('content');
                
                document.body.removeChild(test);
                
                return content && content !== 'none' && content !== '';
            },
            
            // Метод 2: Проверка шрифта
            function() {
                return isFontLoaded('"Font Awesome 6 Free"') || 
                       isFontLoaded('"Font Awesome 5 Free"') ||
                       isFontLoaded('FontAwesome');
            },
            
            // Метод 3: Проверка через document.fonts API
            function() {
                if (!document.fonts) return false;
                
                return document.fonts.check('1em "Font Awesome 6 Free"') ||
                       document.fonts.check('1em "Font Awesome 5 Free"') ||
                       document.fonts.check('1em FontAwesome');
            }
        ];
        
        return methods.some(method => {
            try {
                return method();
            } catch (e) {
                console.warn('Font Awesome check method failed:', e);
                return false;
            }
        });
    }

    /**
     * Проверяет наличие Bootstrap Icons
     */
    function checkBootstrapIcons() {
        const methods = [
            // Метод 1: Проверка через DOM
            function() {
                const test = document.createElement('i');
                test.className = 'bi bi-check';
                test.style.position = 'absolute';
                test.style.left = '-9999px';
                document.body.appendChild(test);
                
                const computedStyle = window.getComputedStyle(test, ':before');
                const content = computedStyle.getPropertyValue('content');
                
                document.body.removeChild(test);
                
                return content && content !== 'none' && content !== '';
            },
            
            // Метод 2: Проверка шрифта
            function() {
                return isFontLoaded('"bootstrap-icons"') || 
                       isFontLoaded('bootstrap-icons');
            },
            
            // Метод 3: Проверка через document.fonts API
            function() {
                if (!document.fonts) return false;
                return document.fonts.check('1em "bootstrap-icons"');
            }
        ];
        
        return methods.some(method => {
            try {
                return method();
            } catch (e) {
                console.warn('Bootstrap Icons check method failed:', e);
                return false;
            }
        });
    }

    /**
     * Включает fallback для иконок
     */
    function enableIconFallback() {
        document.documentElement.classList.add('icon-fallback-enabled');
        console.warn('Icon fonts not loaded - using fallback emoji icons');
        
        // Показываем уведомление пользователю (опционально)
        if (window.NotificationManager) {
            window.NotificationManager.warning(
                'Иконки загружаются из резервного источника',
                { duration: 3000 }
            );
        }
    }

    /**
     * Пытается загрузить иконки с альтернативных CDN
     */
    function loadAlternativeFontAwesome() {
        const alternatives = [
            'https://use.fontawesome.com/releases/v6.5.1/css/all.css',
            'https://cdn.jsdelivr.net/npm/@fortawesome/fontawesome-free@6.5.1/css/all.min.css',
            'https://maxcdn.bootstrapcdn.com/font-awesome/latest/css/font-awesome.min.css'
        ];
        
        alternatives.forEach((url, index) => {
            setTimeout(() => {
                const link = document.createElement('link');
                link.rel = 'stylesheet';
                link.href = url;
                link.onerror = () => console.warn(`Failed to load Font Awesome from ${url}`);
                document.head.appendChild(link);
            }, index * 1000);
        });
    }

    function loadAlternativeBootstrapIcons() {
        const alternatives = [
            'https://unpkg.com/bootstrap-icons@1.11.3/font/bootstrap-icons.css',
            'https://cdn.jsdelivr.net/npm/bootstrap-icons@1.11.3/font/bootstrap-icons.css'
        ];
        
        alternatives.forEach((url, index) => {
            setTimeout(() => {
                const link = document.createElement('link');
                link.rel = 'stylesheet';
                link.href = url;
                link.onerror = () => console.warn(`Failed to load Bootstrap Icons from ${url}`);
                document.head.appendChild(link);
            }, index * 1000);
        });
    }

    /**
     * Основная функция проверки
     */
    function checkIcons(retryCount = 0) {
        const fontAwesomeLoaded = checkFontAwesome();
        const bootstrapIconsLoaded = checkBootstrapIcons();
        
        console.log(`Icon check (attempt ${retryCount + 1}):`, {
            fontAwesome: fontAwesomeLoaded,
            bootstrapIcons: bootstrapIconsLoaded
        });
        
        if (fontAwesomeLoaded && bootstrapIconsLoaded) {
            console.log('✓ All icon fonts loaded successfully');
            document.documentElement.classList.add('icons-loaded');
            document.documentElement.classList.remove('icons-loading');
            return;
        }
        
        if (retryCount < CONFIG.maxRetries) {
            // Продолжаем проверять
            setTimeout(() => checkIcons(retryCount + 1), CONFIG.checkDelay);
        } else {
            // Превышен лимит попыток
            console.warn('Icon fonts failed to load after max retries');
            
            if (!fontAwesomeLoaded) {
                console.warn('Font Awesome not loaded, trying alternatives...');
                loadAlternativeFontAwesome();
            }
            
            if (!bootstrapIconsLoaded) {
                console.warn('Bootstrap Icons not loaded, trying alternatives...');
                loadAlternativeBootstrapIcons();
            }
            
            // Включаем fallback
            setTimeout(() => {
                if (!checkFontAwesome() && !checkBootstrapIcons()) {
                    enableIconFallback();
                }
            }, 2000);
        }
    }

    /**
     * Инициализация при загрузке страницы
     */
    function init() {
        document.documentElement.classList.add('icons-loading');
        
        // Начинаем проверку после загрузки DOM
        if (document.readyState === 'loading') {
            document.addEventListener('DOMContentLoaded', () => {
                setTimeout(() => checkIcons(), CONFIG.checkDelay);
            });
        } else {
            setTimeout(() => checkIcons(), CONFIG.checkDelay);
        }
        
        // Также проверяем после полной загрузки страницы
        window.addEventListener('load', () => {
            setTimeout(() => {
                if (!document.documentElement.classList.contains('icons-loaded')) {
                    checkIcons();
                }
            }, 500);
        });
    }

    // Запускаем инициализацию
    init();

    // Экспортируем API для внешнего использования
    window.IconLoader = {
        check: checkIcons,
        checkFontAwesome: checkFontAwesome,
        checkBootstrapIcons: checkBootstrapIcons,
        enableFallback: enableIconFallback
    };

})();
