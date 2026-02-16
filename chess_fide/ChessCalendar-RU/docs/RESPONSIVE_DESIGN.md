# Адаптивный дизайн - ChessCalendar-RU

## Обзор

Проект ChessCalendar-RU использует комплексный подход к адаптивному дизайну, обеспечивая отличный пользовательский опыт на всех устройствах.

---

## Breakpoints (Точки останова)

### Стандартные breakpoints:

```css
xs: 0-575px      /* Мобильные телефоны (портрет) */
sm: 576-767px    /* Мобильные телефоны (ландшафт) */
md: 768-991px    /* Планшеты */
lg: 992-1199px   /* Десктопы */
xl: 1200-1399px  /* Большие десктопы */
xxl: 1400px+     /* Очень большие экраны */
```

### Специальные breakpoints:

```css
< 360px          /* Очень маленькие экраны */
768-1024px       /* Планшеты (специальная оптимизация) */
1920px+          /* 4K и выше */
```

---

## Файловая структура

### CSS файлы:

1. **`mobile.css`** - Базовые мобильные стили
2. **`mobile-enhanced.css`** - Расширенные мобильные стили
3. **`responsive-enhanced.css`** - Комплексная адаптивность
4. **`improvements.css`** - Общие улучшения UX
5. **`dark-theme.css`** - Тёмная тема
6. **`print-optimization.css`** - Оптимизация печати

### JavaScript файлы:

1. **`responsive-manager.js`** - Управление адаптивным поведением

---

## Основные возможности

### 1. Адаптивная типографика

Использует `clamp()` для плавного масштабирования:

```css
h1 {
    font-size: clamp(1.75rem, 5vw, 3rem);
}

p {
    font-size: clamp(0.875rem, 1.5vw, 1rem);
}
```

### 2. Адаптивная сетка

Автоматическая адаптация количества колонок:

```css
.responsive-grid {
    display: grid;
    gap: 1rem;
    grid-template-columns: 1fr;              /* xs */
    grid-template-columns: repeat(2, 1fr);   /* sm */
    grid-template-columns: repeat(3, 1fr);   /* lg */
    grid-template-columns: repeat(4, 1fr);   /* xxl */
}
```

### 3. Мобильная навигация

- Верхняя навигация с гамбургер-меню
- Нижняя навигация с 4-5 основными разделами
- Плавные анимации открытия/закрытия
- Индикатор активного раздела

### 4. Адаптивные карточки

- Компактный вид на мобильных
- Средний размер на планшетах
- Полный размер на десктопе
- Оптимизированные отступы

### 5. Адаптивные формы

- Размер шрифта 16px (предотвращает зум на iOS)
- Минимальная высота 44px для удобного нажатия
- Полноширинные элементы на мобильных
- Улучшенные состояния фокуса

### 6. Адаптивные модальные окна

- Полноэкранные на мобильных
- Появление снизу с анимацией
- Индикатор перетаскивания
- Оптимизированная прокрутка

### 7. Адаптивные таблицы

- Горизонтальная прокрутка на мобильных
- Вертикальный вид для лучшей читаемости
- Компактные ячейки
- Адаптивные заголовки

---

## Responsive Manager

### Основные методы:

```javascript
// Получить текущий breakpoint
responsiveManager.getCurrentBreakpoint() // 'xs', 'sm', 'md', 'lg', 'xl', 'xxl'

// Проверка типа устройства
responsiveManager.isMobile()    // true/false
responsiveManager.isTablet()    // true/false
responsiveManager.isDesktop()   // true/false

// Проверка возможностей
responsiveManager.isTouchDevice()           // true/false
responsiveManager.supportsFeature('webp')   // true/false

// Получить информацию об устройстве
responsiveManager.getDeviceInfo()

// Адаптивные изображения
responsiveManager.getResponsiveImageSrc('/img/photo.jpg')

// Адаптивные модальные окна
responsiveManager.showResponsiveModal(content, options)
```

### События:

```javascript
// Изменение breakpoint
window.addEventListener('breakpointChange', (e) => {
    console.log('Новый breakpoint:', e.detail.breakpoint);
});

// Изменение ориентации
window.addEventListener('orientationChange', (e) => {
    console.log('Новая ориентация:', e.detail.orientation);
});
```

---

## Оптимизация для мобильных

### 1. Viewport Height Fix

Решает проблему с `100vh` на мобильных:

```css
.full-height {
    height: 100vh;
    height: calc(var(--vh, 1vh) * 100);
}
```

```javascript
// Автоматически обновляется при изменении размера
const vh = window.innerHeight * 0.01;
document.documentElement.style.setProperty('--vh', `${vh}px`);
```

### 2. Touch Optimizations

- Увеличенные области нажатия (минимум 44x44px)
- Отключение подсветки при нажатии
- Тактильная обратная связь (scale эффект)
- Быстрый клик для iOS
- Предотвращение двойного тапа для зума

### 3. Performance Optimizations

- Сокращённые анимации на мобильных
- Оптимизация прокрутки (`-webkit-overflow-scrolling: touch`)
- GPU ускорение (`transform: translateZ(0)`)
- Ленивая загрузка изображений
- Отключение сложных эффектов

### 4. Image Lazy Loading

```html
<img data-src="/path/to/image.jpg" alt="Description">
```

Автоматически загружается при появлении в viewport.

---

## Адаптивные компоненты

### Навигация

```html
<!-- Верхняя навигация -->
<nav class="navbar navbar-expand-lg">
    <!-- Контент -->
</nav>

<!-- Нижняя мобильная навигация -->
<nav class="mobile-bottom-nav d-sm-none">
    <a href="/" class="mobile-nav-item active">
        <i class="bi bi-house-fill"></i>
        <span>Главная</span>
    </a>
    <!-- Другие элементы -->
</nav>
```

### Карточки

```html
<div class="card tournament-card">
    <div class="card-header">
        <h5 class="card-title">Название турнира</h5>
        <span class="badge bg-primary">Блиц</span>
    </div>
    <div class="card-body">
        <p class="card-text">Описание</p>
    </div>
    <div class="card-footer">
        <div class="btn-group">
            <button class="btn btn-primary">Подробнее</button>
            <button class="btn btn-outline-primary">Избранное</button>
        </div>
    </div>
</div>
```

### Формы

```html
<form>
    <div class="mb-3">
        <label class="form-label">Название</label>
        <input type="text" class="form-control" placeholder="Введите название">
    </div>
    
    <div class="mb-3">
        <label class="form-label">Категория</label>
        <select class="form-select">
            <option>Выберите категорию</option>
        </select>
    </div>
    
    <button type="submit" class="btn btn-primary btn-mobile-full">
        Отправить
    </button>
</form>
```

### Таблицы

```html
<div class="table-responsive">
    <table class="table table-mobile-vertical">
        <thead>
            <tr>
                <th>Название</th>
                <th>Дата</th>
                <th>Место</th>
            </tr>
        </thead>
        <tbody>
            <tr>
                <td data-label="Название">Турнир 1</td>
                <td data-label="Дата">01.01.2026</td>
                <td data-label="Место">Москва</td>
            </tr>
        </tbody>
    </table>
</div>
```

### Модальные окна

```html
<div class="modal fade">
    <div class="modal-dialog modal-fullscreen-sm-down">
        <div class="modal-content">
            <div class="modal-header">
                <h5 class="modal-title">Заголовок</h5>
                <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
            </div>
            <div class="modal-body">
                Контент
            </div>
            <div class="modal-footer">
                <button class="btn btn-secondary" data-bs-dismiss="modal">Отмена</button>
                <button class="btn btn-primary">Сохранить</button>
            </div>
        </div>
    </div>
</div>
```

---

## Утилитарные классы

### Видимость

```css
.hide-mobile          /* Скрыть на мобильных */
.show-mobile          /* Показать только на мобильных */
.d-mobile-none        /* display: none на мобильных */
.d-mobile-block       /* display: block на мобильных */
.d-mobile-flex        /* display: flex на мобильных */
```

### Отступы

```css
.p-mobile-0           /* padding: 0 */
.p-mobile-1           /* padding: 0.25rem */
.p-mobile-2           /* padding: 0.5rem */
.p-mobile-3           /* padding: 1rem */

.px-mobile-2          /* padding-left/right: 0.5rem */
.py-mobile-2          /* padding-top/bottom: 0.5rem */

.m-mobile-2           /* margin: 0.5rem */
.mx-mobile-2          /* margin-left/right: 0.5rem */
.my-mobile-2          /* margin-top/bottom: 0.5rem */
```

### Текст

```css
.text-mobile-center   /* text-align: center */
.text-mobile-left     /* text-align: left */
.text-mobile-right    /* text-align: right */

.fs-mobile-small      /* font-size: 0.875rem */
.fs-mobile-normal     /* font-size: 1rem */
.fs-mobile-large      /* font-size: 1.125rem */
```

### Кнопки

```css
.btn-mobile-full      /* width: 100% на мобильных */
.btn-group-horizontal /* Горизонтальная группа кнопок */
```

---

## Тестирование

### Устройства для тестирования:

**Мобильные:**
- iPhone SE (375x667)
- iPhone 12/13 (390x844)
- iPhone 14 Pro Max (430x932)
- Samsung Galaxy S21 (360x800)
- Google Pixel 5 (393x851)

**Планшеты:**
- iPad Mini (768x1024)
- iPad Air (820x1180)
- iPad Pro 11" (834x1194)
- iPad Pro 12.9" (1024x1366)

**Десктопы:**
- 1366x768 (HD)
- 1920x1080 (Full HD)
- 2560x1440 (2K)
- 3840x2160 (4K)

### Инструменты тестирования:

1. **Chrome DevTools**
   - Device Mode
   - Network throttling
   - Touch simulation

2. **Firefox Responsive Design Mode**
   - Различные устройства
   - Ориентация
   - DPR (Device Pixel Ratio)

3. **BrowserStack / LambdaTest**
   - Реальные устройства
   - Различные браузеры
   - Различные ОС

4. **Lighthouse**
   - Performance
   - Accessibility
   - Best Practices
   - SEO

---

## Best Practices

### 1. Mobile First

Начинайте с мобильных стилей, затем добавляйте для больших экранов:

```css
/* Базовые стили (мобильные) */
.element {
    font-size: 0.875rem;
    padding: 0.5rem;
}

/* Планшеты и выше */
@media (min-width: 768px) {
    .element {
        font-size: 1rem;
        padding: 1rem;
    }
}
```

### 2. Touch Targets

Минимальный размер 44x44px:

```css
.btn, .nav-link, a {
    min-height: 44px;
    min-width: 44px;
}
```

### 3. Readable Text

Минимальный размер шрифта 16px на мобильных:

```css
input, select, textarea {
    font-size: 16px; /* Предотвращает зум на iOS */
}
```

### 4. Flexible Images

```css
img {
    max-width: 100%;
    height: auto;
}
```

### 5. Viewport Meta Tag

```html
<meta name="viewport" content="width=device-width, initial-scale=1.0">
```

### 6. Performance

- Минимизируйте CSS/JS
- Оптимизируйте изображения
- Используйте ленивую загрузку
- Кэшируйте ресурсы
- Используйте CDN

### 7. Accessibility

- Семантический HTML
- ARIA атрибуты
- Клавиатурная навигация
- Контрастность цветов
- Альтернативный текст для изображений

---

## Производительность

### Метрики:

- **FCP (First Contentful Paint):** < 1.8s
- **LCP (Largest Contentful Paint):** < 2.5s
- **FID (First Input Delay):** < 100ms
- **CLS (Cumulative Layout Shift):** < 0.1
- **TTI (Time to Interactive):** < 3.8s

### Оптимизации:

1. **CSS:**
   - Минификация
   - Критический CSS inline
   - Отложенная загрузка некритического CSS

2. **JavaScript:**
   - Минификация
   - Code splitting
   - Отложенная загрузка
   - Tree shaking

3. **Изображения:**
   - WebP формат
   - Адаптивные изображения (srcset)
   - Ленивая загрузка
   - Сжатие

4. **Шрифты:**
   - font-display: swap
   - Подмножества шрифтов
   - Предзагрузка критических шрифтов

---

## Поддержка браузеров

### Полная поддержка:
- ✅ Chrome 90+
- ✅ Firefox 88+
- ✅ Safari 14+
- ✅ Edge 90+
- ✅ Samsung Internet 14+
- ✅ Opera 76+

### Частичная поддержка:
- ⚠️ IE 11 (базовая функциональность)

---

## Отладка

### Включение режима отладки:

```
?debug=true
```

Показывает:
- Информацию об устройстве в консоли
- Текущий breakpoint
- Ориентацию
- Возможности устройства

### Консольные команды:

```javascript
// Информация об устройстве
ChessCalendar.responsiveManager.logDeviceInfo()

// Текущий breakpoint
ChessCalendar.responsiveManager.getCurrentBreakpoint()

// Проверка возможностей
ChessCalendar.responsiveManager.supportsFeature('webp')
```

---

## Дополнительные ресурсы

- [MDN: Responsive Design](https://developer.mozilla.org/en-US/docs/Learn/CSS/CSS_layout/Responsive_Design)
- [Google Web Fundamentals](https://developers.google.com/web/fundamentals/design-and-ux/responsive)
- [Bootstrap Documentation](https://getbootstrap.com/docs/5.3/layout/breakpoints/)
- [Can I Use](https://caniuse.com/)

---

**Версия:** 2.4.0  
**Дата:** 2026-02-16  
**Статус:** ✅ Готово
