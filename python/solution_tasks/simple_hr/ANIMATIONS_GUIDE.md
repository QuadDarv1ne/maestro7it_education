# Руководство по использованию анимаций и загрузок

## Обзор

Система включает в себя мощный набор CSS анимаций и JavaScript утилит для улучшения пользовательского опыта.

## Файлы

- `app/static/animations.css` - CSS анимации и скелетоны
- `app/static/loading-helpers.js` - JavaScript утилиты для управления загрузками
- `app/templates/animations_demo.html` - Демо-страница с примерами

## CSS Анимации

### Скелетоны загрузки

```html
<!-- Простой скелетон -->
<div class="skeleton skeleton-text"></div>
<div class="skeleton skeleton-title"></div>
<div class="skeleton skeleton-avatar"></div>
<div class="skeleton skeleton-card"></div>
```

### Анимации появления

```html
<!-- Fade In -->
<div class="fade-in">Содержимое появляется плавно</div>

<!-- Slide In From Bottom -->
<div class="slide-in-bottom">Содержимое выезжает снизу</div>

<!-- Bounce In -->
<div class="bounce-in">Содержимое прыгает</div>

<!-- Pulse -->
<div class="pulse-animation">Пульсирующий элемент</div>
```

### Эффекты при наведении

```html
<!-- Scale on Hover -->
<div class="hover-scale">Увеличивается при наведении</div>

<!-- Smooth Transition -->
<div class="smooth-transition">Плавный переход</div>

<!-- Ripple Effect -->
<button class="btn ripple">Ripple эффект</button>

<!-- Glow Effect -->
<div class="glow">Светящийся эффект</div>
```

### Эффекты ошибок

```html
<!-- Shake Animation -->
<div class="shake">Трясется при ошибке</div>
```

## JavaScript API

### LoadingManager

Глобальный объект `loadingManager` предоставляет методы для управления состояниями загрузки.

#### Overlay Loading

```javascript
// Показать оверлей загрузки
loadingManager.showOverlay('Загрузка данных...');

// Скрыть оверлей
loadingManager.hideOverlay();
```

#### Button Loading States

```javascript
// Показать состояние загрузки на кнопке
const button = document.getElementById('myButton');
loadingManager.showButtonLoading(button, 'Оригинальный текст');

// Скрыть состояние загрузки
loadingManager.hideButtonLoading(button);
```

#### Skeleton Loaders

```javascript
// Показать скелетон в контейнере
const container = document.getElementById('myContainer');
loadingManager.showSkeleton(container, 'table', 10); // table, cards, или list

// Скрыть скелетон и показать содержимое
loadingManager.hideSkeleton(container, '<p>Реальное содержимое</p>');
```

#### Success/Error Animations

```javascript
// Показать успех
loadingManager.showSuccess('Операция выполнена успешно!', () => {
    console.log('Callback после анимации');
});

// Показать ошибку
loadingManager.showError('Произошла ошибка!');
```

#### Typing Indicator

```javascript
// Добавить индикатор печати
const container = document.getElementById('chatBox');
loadingManager.showTyping(container);
```

#### Progress Bar

```javascript
// Создать прогресс-бар
const html = loadingManager.createProgressBar(75, 'Загрузка файлов');
document.getElementById('progressContainer').innerHTML = html;
```

### AjaxHelper

Помощник для AJAX запросов с автоматическими состояниями загрузки.

#### Fetch с Loading

```javascript
// Автоматический оверлей при загрузке
const result = await AjaxHelper.fetch('/api/employees', {}, true);

if (result.success) {
    console.log(result.data);
} else {
    console.error(result.error);
}
```

#### Submit Form с Loading

```javascript
const form = document.getElementById('myForm');
const submitButton = document.getElementById('submitBtn');

const result = await AjaxHelper.submitForm(form, submitButton);

if (result.success) {
    loadingManager.showSuccess('Форма отправлена!');
}
```

### LazyLoader

Ленивая загрузка изображений для оптимизации производительности.

```html
<!-- Изображение с ленивой загрузкой -->
<img data-src="/static/images/large-image.jpg" 
     class="lazy-load-placeholder" 
     alt="Описание">

<script>
    // Автоматически инициализируется при загрузке страницы
    // Или вручную:
    lazyLoader.observe('[data-src]');
</script>
```

## Примеры использования

### Пример 1: Форма с загрузкой

```html
<form id="employeeForm" action="/employees/create" method="POST">
    <!-- Поля формы -->
    <button type="submit" id="submitBtn" class="btn btn-primary">
        <i class="bi bi-save"></i> Сохранить
    </button>
</form>

<script>
    const form = document.getElementById('employeeForm');
    const submitBtn = document.getElementById('submitBtn');
    
    form.addEventListener('submit', async function(e) {
        e.preventDefault();
        
        loadingManager.showButtonLoading(submitBtn);
        
        try {
            const formData = new FormData(form);
            const response = await fetch(form.action, {
                method: 'POST',
                body: formData
            });
            
            if (response.ok) {
                loadingManager.hideButtonLoading(submitBtn);
                loadingManager.showSuccess('Сотрудник добавлен!', () => {
                    window.location.href = '/employees';
                });
            } else {
                throw new Error('Server error');
            }
        } catch (error) {
            loadingManager.hideButtonLoading(submitBtn);
            loadingManager.showError('Ошибка сохранения данных');
        }
    });
</script>
```

### Пример 2: Таблица со скелетоном

```html
<div id="employeesTable">
    <!-- Здесь будет таблица -->
</div>

<script>
    async function loadEmployees() {
        const container = document.getElementById('employeesTable');
        
        // Показать скелетон
        loadingManager.showSkeleton(container, 'table', 10);
        
        try {
            const response = await fetch('/api/employees');
            const employees = await response.json();
            
            // Генерировать HTML таблицы
            let html = '<table class="table"><thead>...';
            employees.forEach(emp => {
                html += `<tr><td>${emp.name}</td>...`;
            });
            html += '</table>';
            
            // Показать таблицу
            loadingManager.hideSkeleton(container, html);
        } catch (error) {
            loadingManager.hideSkeleton(container, '');
            loadingManager.showError('Ошибка загрузки сотрудников');
        }
    }
    
    // Загрузить при загрузке страницы
    document.addEventListener('DOMContentLoaded', loadEmployees);
</script>
```

### Пример 3: Карточки со скелетоном

```html
<div id="statsCards" class="row">
    <!-- Здесь будут карточки статистики -->
</div>

<script>
    async function loadStats() {
        const container = document.getElementById('statsCards');
        
        loadingManager.showSkeleton(container, 'cards', 4);
        
        const result = await AjaxHelper.fetch('/api/stats', {}, false);
        
        if (result.success) {
            const stats = result.data;
            const html = `
                <div class="col-md-3">
                    <div class="card bounce-in">
                        <div class="card-body">
                            <h5>Сотрудники</h5>
                            <h2>${stats.employees}</h2>
                        </div>
                    </div>
                </div>
                <!-- Другие карточки -->
            `;
            loadingManager.hideSkeleton(container, html);
        }
    }
</script>
```

### Пример 4: Прогресс бар для загрузки файла

```html
<input type="file" id="fileInput">
<div id="uploadProgress"></div>

<script>
    document.getElementById('fileInput').addEventListener('change', async function(e) {
        const file = e.target.files[0];
        if (!file) return;
        
        const progressDiv = document.getElementById('uploadProgress');
        let progress = 0;
        
        // Симуляция загрузки (в реальности используйте XMLHttpRequest)
        const interval = setInterval(() => {
            progress += 10;
            progressDiv.innerHTML = loadingManager.createProgressBar(
                progress, 
                `Загрузка ${file.name}`
            );
            
            if (progress >= 100) {
                clearInterval(interval);
                loadingManager.showSuccess('Файл загружен!');
            }
        }, 200);
    });
</script>
```

## Best Practices

### 1. Всегда показывайте индикацию загрузки

```javascript
// ❌ Плохо - пользователь не знает, что происходит
fetch('/api/data').then(response => response.json());

// ✅ Хорошо - пользователь видит индикатор загрузки
loadingManager.showOverlay('Загрузка...');
fetch('/api/data')
    .then(response => response.json())
    .finally(() => loadingManager.hideOverlay());
```

### 2. Используйте скелетоны для списков

```javascript
// ✅ Хорошо - скелетон дает представление о структуре
loadingManager.showSkeleton(container, 'table', 10);
```

### 3. Обрабатывайте ошибки

```javascript
try {
    // Операция
    loadingManager.showSuccess('Успех!');
} catch (error) {
    loadingManager.showError('Ошибка: ' + error.message);
}
```

### 4. Используйте анимации появления

```javascript
// После загрузки данных добавьте класс анимации
element.classList.add('fade-in');
```

### 5. Оптимизируйте изображения

```html
<!-- Используйте ленивую загрузку для больших изображений -->
<img data-src="/static/images/large.jpg" class="lazy-load-placeholder">
```

## Демо-страница

Посетите `/animations-demo` для интерактивной демонстрации всех анимаций и эффектов.

## Кастомизация

### Изменение цветов

Отредактируйте `animations.css`:

```css
/* Изменить цвет скелетона */
.skeleton {
    background: linear-gradient(
        90deg,
        #yourColor1 25%,
        #yourColor2 50%,
        #yourColor1 75%
    );
}

/* Изменить цвет спиннера */
.loading-spinner {
    border-top-color: #yourColor;
}
```

### Изменение скорости анимаций

```css
/* Замедлить fade-in */
.fade-in {
    animation: fadeIn 1s ease-in; /* вместо 0.5s */
}
```

## Производительность

1. **Скелетоны** - используйте вместо спиннеров для улучшения восприятия скорости
2. **Ленивая загрузка** - автоматически загружает изображения при прокрутке
3. **Debouncing** - уже встроен в поисковые поля
4. **CSS анимации** - используют GPU ускорение для плавности

## Поддержка браузеров

- Chrome/Edge: Полная поддержка
- Firefox: Полная поддержка
- Safari: Полная поддержка
- IE11: Частичная поддержка (без некоторых анимаций)

## Troubleshooting

### Анимации не работают

1. Убедитесь, что `animations.css` подключен в `base.html`
2. Проверьте консоль браузера на ошибки
3. Убедитесь, что `loading-helpers.js` загружен

### Скелетоны не исчезают

```javascript
// Всегда вызывайте hideSkeleton
loadingManager.hideSkeleton(container, content);
```

### Оверлей блокирует всю страницу

```javascript
// Не забывайте скрывать оверлей
loadingManager.hideOverlay();
```
