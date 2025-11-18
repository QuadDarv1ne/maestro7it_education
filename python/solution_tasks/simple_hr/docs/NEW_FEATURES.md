# Новые улучшения Simple HR System

## 🎨 Темная тема

### Функциональность
- **Автоматическое переключение**: Кнопка в навигационной панели
- **Сохранение настроек**: Предпочтения сохраняются в localStorage
- **Системная тема**: Автоматическое определение темы операционной системы
- **Плавные переходы**: Анимированное переключение между темами

### Использование
```javascript
// Программное переключение темы
themeSwitcher.setTheme('dark');
themeSwitcher.setTheme('light');

// Получить текущую тему
const currentTheme = themeSwitcher.getTheme();

// Событие изменения темы
document.addEventListener('themeChanged', (e) => {
    console.log('Новая тема:', e.detail.theme);
});
```

### CSS переменные
```css
:root {
    --bg-primary: #ffffff;
    --bg-secondary: #f8f9fa;
    --text-primary: #212529;
    --text-secondary: #6c757d;
    /* и другие... */
}

[data-theme="dark"] {
    --bg-primary: #1a1d23;
    --bg-secondary: #22262e;
    --text-primary: #e4e6eb;
    --text-secondary: #b0b3b8;
    /* и другие... */
}
```

## ✨ Расширенные анимации

### Новые классы анимации

#### Fade анимации
- `.animate-fade-in-up` - Появление снизу вверх
- `.animate-fade-in-down` - Появление сверху вниз
- `.animate-fade-in-left` - Появление слева
- `.animate-fade-in-right` - Появление справа

#### Scale анимации
- `.animate-zoom-in` - Увеличение
- `.animate-zoom-out` - Уменьшение
- `.animate-bounce-in` - Появление с отскоком

#### Slide анимации
- `.animate-slide-in-up` - Скольжение снизу
- `.animate-slide-in-down` - Скольжение сверху

#### Другие анимации
- `.animate-rotate-in` - Вращение при появлении
- `.animate-flip-in-x` - Переворот по оси X
- `.animate-shake` - Тряска (для ошибок)
- `.animate-pulse-glow` - Пульсирующее свечение

#### Задержки анимации
- `.animate-delay-100` до `.animate-delay-500`

### Hover эффекты
- `.hover-lift` - Поднятие при наведении
- `.hover-grow` - Увеличение при наведении
- `.hover-rotate` - Вращение при наведении

### Пример использования
```html
<div class="card animate-fade-in-up animate-delay-200">
    <div class="card-body hover-lift">
        Контент с анимацией
    </div>
</div>

<!-- Последовательная анимация списка -->
<ul class="stagger-animation">
    <li>Элемент 1</li>
    <li>Элемент 2</li>
    <li>Элемент 3</li>
</ul>
```

## 🔔 Система уведомлений

### Функции
- Уведомления success, error, warning, info
- Настраиваемая позиция на экране
- Автоматическое закрытие с таймером
- Максимальное количество уведомлений
- Прогресс-бар до закрытия
- Поддержка темной темы

### Использование
```javascript
// Простые методы
showSuccess('Операция выполнена успешно!');
showError('Произошла ошибка!');
showWarning('Внимание!');
showInfo('Полезная информация');

// С дополнительными настройками
showSuccess('Сохранено', {
    title: 'Успешно',
    duration: 3000,
    closable: true
});

// Через менеджер уведомлений
notificationManager.show('Сообщение', 'info', {
    title: 'Заголовок',
    duration: 5000,
    closable: true
});

// Удалить все уведомления
notificationManager.removeAll();
```

### Позиции
- `top-right` (по умолчанию)
- `top-left`
- `top-center`
- `bottom-right`
- `bottom-left`
- `bottom-center`

### Настройка
```javascript
const notificationManager = new NotificationManager({
    position: 'top-right',
    maxNotifications: 5,
    defaultDuration: 5000,
    animationDuration: 300,
    soundEnabled: false
});
```

## ✅ Улучшенная валидация форм

### Автоматическая валидация
Добавьте атрибут `data-validate` к форме:

```html
<form data-validate>
    <input type="email" name="email" required>
    <input type="password" name="password" data-validate-minlength="8">
    <button type="submit">Отправить</button>
</form>
```

### Встроенные валидаторы
- `required` - Обязательное поле
- `email` - Email адрес
- `phone` - Телефон
- `url` - URL адрес
- `number` - Число
- `date` - Дата
- `pattern` - Регулярное выражение
- `minlength` - Минимальная длина
- `maxlength` - Максимальная длина
- `min` - Минимальное значение
- `max` - Максимальное значение
- `passport` - Российский паспорт
- `snils` - СНИЛС
- `inn` - ИНН

### Программное использование
```javascript
const form = document.querySelector('#myForm');
const validator = new FormValidator(form, {
    validateOnBlur: true,
    validateOnInput: false,
    showErrors: true,
    scrollToError: true
});

// Добавить пользовательский валидатор
validator.addValidator('customRule', (value) => {
    return value.length > 5;
}, 'Длина должна быть больше 5 символов');

// Программная валидация
const isValid = validator.validateForm();

// Сброс формы
validator.reset();
```

### Примеры атрибутов
```html
<!-- Email -->
<input type="email" data-validate-email>

<!-- Телефон -->
<input type="tel" data-validate-phone>

<!-- Минимальная длина -->
<input type="text" data-validate-minlength="8">

<!-- Диапазон значений -->
<input type="number" data-validate-min="1" data-validate-max="100">

<!-- Паспорт -->
<input type="text" data-validate-passport placeholder="1234 567890">

<!-- СНИЛС -->
<input type="text" data-validate-snils placeholder="123-456-789 00">

<!-- ИНН -->
<input type="text" data-validate-inn placeholder="1234567890">
```

## 📊 Улучшенные таблицы

### Функции
- Сортировка по столбцам
- Поиск по всем полям
- Пагинация с настраиваемым количеством строк
- Автоматический подсчет записей
- Responsive дизайн
- Поддержка темной темы

### Автоматическая инициализация
```html
<table class="table" data-enhanced-table>
    <thead>
        <tr>
            <th>Имя</th>
            <th>Email</th>
            <th class="no-sort">Действия</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td>Иван Иванов</td>
            <td>ivan@example.com</td>
            <td><button>Редактировать</button></td>
        </tr>
    </tbody>
</table>
```

### Программная инициализация
```javascript
const table = document.querySelector('#myTable');
const enhancedTable = new EnhancedTable(table, {
    sortable: true,
    filterable: true,
    pagination: true,
    itemsPerPage: 25,
    searchPlaceholder: 'Найти...',
    noDataText: 'Данные отсутствуют',
    showEntriesText: 'Показано {start} - {end} из {total}'
});

// Обновить данные
enhancedTable.refresh();
```

### Отключение сортировки для столбца
```html
<th class="no-sort">Действия</th>
```

## 🎯 Улучшения доступности

### Новые функции
1. **Улучшенный фокус** - Видимая индикация для клавиатурной навигации
2. **Skip to content** - Быстрый переход к основному содержимому
3. **ARIA атрибуты** - Правильные роли и метки
4. **Контрастность** - Соответствие WCAG 2.1 AA

### Skip to Content
```html
<a href="#main-content" class="skip-to-content">
    Перейти к содержимому
</a>

<main id="main-content">
    <!-- Основной контент -->
</main>
```

## 🖨️ Стили для печати

### Автоматические настройки
- Скрытие навигации и боковой панели
- Оптимизация таблиц и карточек
- Черно-белая печать
- Экономия чернил

### Отключение печати элемента
```html
<div class="no-print">
    Этот элемент не будет напечатан
</div>
```

## 🎨 Кастомная прокрутка

### Стилизованный scrollbar
- Градиентный ползунок
- Скругленные края
- Поддержка темной темы
- Hover эффекты

### Переопределение
```css
::-webkit-scrollbar {
    width: 12px;
}

::-webkit-scrollbar-thumb {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    border-radius: 10px;
}
```

## 📱 Адаптивность

### Breakpoints
- **Mobile**: < 768px
- **Tablet**: 768px - 1024px
- **Desktop**: > 1024px

### Мобильные улучшения
- Адаптивные таблицы
- Скрываемая боковая панель
- Touch-friendly кнопки
- Оптимизированные модальные окна

## 🚀 Производительность

### Оптимизации
1. **CSS переменные** - Быстрое переключение тем
2. **Hardware acceleration** - Использование transform и opacity
3. **Debouncing** - Для поиска и фильтрации
4. **Lazy loading** - Загрузка по требованию

## 📦 Подключение файлов

### В base.html
```html
<!-- CSS -->
<link rel="stylesheet" href="{{ url_for('static', filename='enhanced-animations.css') }}">
<link rel="stylesheet" href="{{ url_for('static', filename='style.css') }}">

<!-- JavaScript -->
<script src="{{ url_for('static', filename='theme-switcher.js') }}"></script>
<script src="{{ url_for('static', filename='notification-manager.js') }}"></script>
<script src="{{ url_for('static', filename='form-validator.js') }}"></script>
<script src="{{ url_for('static', filename='enhanced-table.js') }}"></script>
```

## 🔧 Конфигурация

### Глобальные настройки
```javascript
// В начале вашего скрипта
const appConfig = {
    theme: {
        default: 'light',
        storageKey: 'theme'
    },
    notifications: {
        position: 'top-right',
        duration: 5000
    },
    tables: {
        itemsPerPage: 25
    }
};
```

## 📝 Примеры использования

### Комплексная форма
```html
<form data-validate>
    <div class="mb-3">
        <label for="fullName" class="form-label">ФИО</label>
        <input type="text" 
               class="form-control" 
               id="fullName" 
               required 
               data-validate-minlength="3">
    </div>
    
    <div class="mb-3">
        <label for="email" class="form-label">Email</label>
        <input type="email" 
               class="form-control" 
               id="email" 
               required 
               data-validate-email>
    </div>
    
    <div class="mb-3">
        <label for="phone" class="form-label">Телефон</label>
        <input type="tel" 
               class="form-control" 
               id="phone" 
               required 
               data-validate-phone>
    </div>
    
    <button type="submit" class="btn btn-primary">
        Отправить
    </button>
</form>
```

### Анимированная карточка
```html
<div class="card animate-fade-in-up animate-delay-200 hover-lift">
    <div class="card-body">
        <h5 class="card-title">Заголовок</h5>
        <p class="card-text">Текст карточки</p>
        <button class="btn btn-primary" onclick="showSuccess('Успешно!')">
            Действие
        </button>
    </div>
</div>
```

### Улучшенная таблица
```html
<table class="table table-striped table-hover" data-enhanced-table>
    <thead>
        <tr>
            <th>№</th>
            <th>Сотрудник</th>
            <th>Должность</th>
            <th>Email</th>
            <th class="no-sort">Действия</th>
        </tr>
    </thead>
    <tbody>
        <!-- Данные -->
    </tbody>
</table>
```

## 🐛 Отладка

### Включение логов
```javascript
// В консоли браузера
localStorage.setItem('debug', 'true');

// Отключение
localStorage.removeItem('debug');
```

### Проверка состояния
```javascript
// Текущая тема
console.log(themeSwitcher.getTheme());

// Активные уведомления
console.log(notificationManager.notifications);

// Валидация формы
const validator = new FormValidator(form);
console.log(validator.validateForm());
```

## 📚 Дополнительная документация

Смотрите также:
- [API.md](docs/API.md) - API документация
- [CHANGELOG.md](CHANGELOG.md) - История изменений
- [README.md](README.md) - Основная документация

## 💡 Советы

1. **Темы**: Используйте CSS переменные для кастомизации цветов
2. **Анимации**: Не переусердствуйте, используйте с умом
3. **Уведомления**: Ограничьте максимум до 5 одновременно
4. **Валидация**: Добавляйте валидацию на стороне сервера тоже
5. **Таблицы**: Для больших данных используйте серверную пагинацию

## 🎓 Обучение

### Запуск демо
```bash
# Откройте браузер
http://127.0.0.1:5000/animations_demo

# Или создайте свою демо-страницу
```

### Тестирование компонентов
```javascript
// В консоли браузера
showSuccess('Тестовое уведомление');
themeSwitcher.toggleTheme();
```
