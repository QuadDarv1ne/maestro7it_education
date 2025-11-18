# Документация по JavaScript компонентам Simple HR

## Обзор

В проекте Simple HR реализованы 12 мощных JavaScript компонентов для улучшения UX/UI:

### 📦 Список компонентов

1. **DateUtils** - работа с датами
2. **ThemeSwitcher** - тёмная/светлая тема
3. **NotificationManager** - уведомления
4. **FormValidator** - валидация форм
5. **EnhancedTable** - улучшенные таблицы
6. **DataGrid** - продвинутые таблицы данных
7. **StorageManager** - работа с localStorage
8. **CacheManager** - кеширование данных
9. **APIClient** - HTTP запросы
10. **ModalManager** - модальные окна
11. **ChartHelper** - графики и диаграммы
12. **LoadingHelpers** - индикаторы загрузки

---

## 1. DateUtils

Утилиты для работы с датами.

### Основные методы

```javascript
// Форматирование
DateUtils.format(new Date(), 'DD.MM.YYYY'); // "15.12.2024"
DateUtils.formatRu(new Date(), 'long'); // "15 декабря 2024 г."
DateUtils.relative(new Date(Date.now() - 3600000)); // "1 час назад"

// Парсинг
DateUtils.parse('15.12.2024', 'DD.MM.YYYY'); // Date объект

// Арифметика
DateUtils.addDays(new Date(), 7); // +7 дней
DateUtils.addMonths(new Date(), 1); // +1 месяц
DateUtils.diffInDays(date1, date2); // разница в днях

// Проверки
DateUtils.isToday(new Date()); // true
DateUtils.isWeekend(new Date()); // true/false
DateUtils.isValid(date); // проверка валидности

// Утилиты
DateUtils.getAge('1990-05-15'); // возраст
DateUtils.getWorkingDays(start, end); // рабочие дни
DateUtils.formatDuration(3600000); // "1 час"
```

---

## 2. ThemeSwitcher

Переключение между светлой и тёмной темой.

### Использование

```javascript
// Автоматически создаёт кнопку в navbar
// Сохраняет предпочтения в localStorage

// События
document.addEventListener('themeChanged', (e) => {
    console.log('Новая тема:', e.detail.theme);
});
```

---

## 3. NotificationManager

Система toast-уведомлений.

### Методы

```javascript
// Типы уведомлений
notificationManager.success('Операция выполнена!', 'Успех');
notificationManager.error('Что-то пошло не так', 'Ошибка');
notificationManager.warning('Внимание!', 'Предупреждение');
notificationManager.info('Информация', 'К сведению');

// Позиции: top-right, top-left, bottom-right, bottom-left, top-center, bottom-center
notificationManager.success('Сообщение', 'Заголовок', { position: 'bottom-right' });

// Продолжительность
notificationManager.info('Короткое', 'Сообщение', { duration: 2000 });

// Без автозакрытия
notificationManager.warning('Важно!', 'Внимание', { autoClose: false });
```

---

## 4. FormValidator

Клиентская валидация форм.

### Использование

```javascript
const validator = new FormValidator('myForm');

// Добавить правила
validator.addRule('email', [
    { type: 'required', message: 'Email обязателен' },
    { type: 'email', message: 'Некорректный email' }
]);

validator.addRule('phone', [
    { type: 'required' },
    { type: 'phone', message: 'Некорректный телефон' }
]);

// Валидация при отправке
document.getElementById('myForm').addEventListener('submit', (e) => {
    if (!validator.validate()) {
        e.preventDefault();
    }
});

// Встроенные валидаторы: required, email, phone, url, min, max, minLength, 
// maxLength, pattern, passport, snils, inn, date, custom
```

---

## 5. EnhancedTable

Простые таблицы с сортировкой и поиском.

### Использование

```html
<table data-enhanced-table data-page-size="10">
    <thead>
        <tr>
            <th>Имя</th>
            <th>Email</th>
        </tr>
    </thead>
    <tbody>
        <tr><td>Иван</td><td>ivan@example.com</td></tr>
    </tbody>
</table>
```

Автоматически добавляет сортировку, поиск и пагинацию.

---

## 6. DataGrid

Продвинутая таблица с множеством возможностей.

### Пример

```javascript
const grid = new DataGrid('containerId', {
    data: employees,
    columns: [
        { key: 'id', label: 'ID', width: '60px', sortable: true },
        { key: 'name', label: 'Имя', sortable: true, filterable: true },
        { 
            key: 'salary', 
            label: 'Зарплата',
            sortable: true,
            render: (value) => value.toLocaleString('ru-RU') + ' ₽'
        }
    ],
    pageSize: 10,
    selectable: true,
    searchable: true,
    exportable: true
});

// Методы
grid.refresh(); // обновить
grid.setData(newData); // новые данные
grid.sort('name', 'asc'); // сортировка
grid.filter('department', 'IT'); // фильтр
grid.exportToCSV(); // экспорт в CSV
```

---

## 7. StorageManager

Работа с localStorage/sessionStorage.

### Примеры

```javascript
// Сохранение
storage.set('user', { name: 'Иван', age: 30 });
storage.set('temp', 'data', { session: true }); // в sessionStorage
storage.set('cached', 'value', { expires: Date.now() + 3600000 }); // с TTL

// Получение
const user = storage.get('user');
const value = storage.get('missing', 'default'); // с дефолтным значением

// Массивы
storage.pushToArray('recent', 'item');
storage.removeFromArray('recent', 'item');

// Счетчики
storage.increment('counter', 5);
storage.decrement('counter', 2);

// Утилиты
storage.keys(); // все ключи
storage.has('key'); // проверка наличия
storage.size(); // размер в байтах
storage.clear(); // очистить всё
```

---

## 8. CacheManager

Кеширование с TTL.

### Использование

```javascript
// Сохранение (1 час по умолчанию)
cache.set('employees', employeesList, 3600000);

// Получение
const employees = cache.get('employees');

// Получить или загрузить
const data = await cache.getOrFetch('key', async () => {
    const response = await fetch('/api/data');
    return await response.json();
}, 3600000);

// Инвалидация
cache.invalidate('employees');
cache.clear(); // очистить весь кеш

// Статистика
const stats = cache.stats();
console.log(`Размер: ${stats.size}, Элементов: ${stats.count}`);
```

---

## 9. APIClient & SimpleHRAPI

HTTP клиент для REST API.

### Базовый APIClient

```javascript
const api = new APIClient('/api/v1');

// GET
const data = await api.get('/users', { page: 1, limit: 10 });

// POST
const result = await api.post('/users', { name: 'Иван' });

// PUT, PATCH, DELETE
await api.put('/users/1', userData);
await api.patch('/users/1', { status: 'active' });
await api.delete('/users/1');

// Загрузка файла
await api.upload('/upload', file, 'document');

// Скачивание файла
await api.download('/download/report.pdf', 'report.pdf');

// Batch запросы
const results = await api.batch([
    { method: 'GET', url: '/users' },
    { method: 'GET', url: '/departments' }
]);
```

### SimpleHRAPI

```javascript
// Специализированный клиент для Simple HR

// Сотрудники
const employees = await hrAPI.getEmployees({ page: 1 });
const employee = await hrAPI.getEmployee(1);
await hrAPI.createEmployee(data);
await hrAPI.updateEmployee(1, data);
await hrAPI.deleteEmployee(1);

// Отпуска
const vacations = await hrAPI.getVacations();
await hrAPI.approveVacation(5);
await hrAPI.rejectVacation(5, 'Недостаточно дней');

// Аналитика
const stats = await hrAPI.getDashboardStats();
const hiring = await hrAPI.getHiringTrends();

// Уведомления
const unread = await hrAPI.getUnreadNotifications();
await hrAPI.markNotificationRead(10);
await hrAPI.markAllNotificationsRead();
```

---

## 10. ModalManager

Удобная работа с модальными окнами Bootstrap.

### Создание модального окна

```javascript
modalManager.create('myModal', {
    title: 'Заголовок',
    content: '<p>Содержимое</p>',
    footer: '<button class="btn btn-primary">OK</button>',
    size: 'lg', // sm, lg, xl
    centered: true,
    scrollable: true,
    onShown: () => console.log('Показано'),
    onHidden: () => console.log('Скрыто')
});

modalManager.show('myModal');
modalManager.hide('myModal');
modalManager.destroy('myModal');
```

### Подтверждение

```javascript
const confirmed = await modalManager.confirm({
    title: 'Удалить?',
    message: 'Вы уверены, что хотите удалить этот элемент?',
    confirmText: 'Удалить',
    cancelText: 'Отмена',
    confirmClass: 'btn-danger'
});

if (confirmed) {
    // Удалить
}
```

### Предупреждение

```javascript
await modalManager.alert({
    title: 'Успех',
    message: 'Операция выполнена успешно!',
    icon: 'success', // info, success, warning, danger
    buttonText: 'OK'
});
```

### Форма

```javascript
const formData = await modalManager.form({
    title: 'Новый сотрудник',
    fields: [
        { name: 'name', label: 'ФИО', type: 'text', required: true },
        { name: 'email', label: 'Email', type: 'email', required: true },
        { 
            name: 'department', 
            label: 'Отдел', 
            type: 'select',
            options: [
                { value: '1', label: 'IT' },
                { value: '2', label: 'HR' }
            ]
        },
        { name: 'bio', label: 'О себе', type: 'textarea' }
    ],
    submitText: 'Создать',
    onSubmit: async (data) => {
        await hrAPI.createEmployee(data);
    }
});
```

### Загрузка

```javascript
const loadingId = modalManager.loading({
    title: 'Загрузка...',
    message: 'Пожалуйста, подождите',
    spinner: 'border' // или 'grow'
});

// После завершения операции
modalManager.closeLoading(loadingId);
```

---

## 11. ChartHelper

Обёртка для Chart.js.

### Линейный график

```javascript
const chartHelper = new ChartHelper();

chartHelper.createLineChart('canvas', {
    labels: ['Янв', 'Фев', 'Мар', 'Апр', 'Май'],
    datasets: [{
        label: 'Продажи',
        data: [12, 19, 8, 15, 22]
    }]
}, {
    title: 'Продажи по месяцам'
});
```

### Столбчатый график

```javascript
chartHelper.createBarChart('canvas', {
    labels: ['IT', 'HR', 'Sales'],
    datasets: [{
        label: 'Сотрудники',
        data: [45, 15, 32]
    }]
});
```

### Круговая диаграмма

```javascript
chartHelper.createPieChart('canvas', {
    labels: ['Frontend', 'Backend', 'DevOps'],
    datasets: [{
        data: [30, 50, 20]
    }]
});
```

### Другие типы

```javascript
// Area chart
chartHelper.createAreaChart('canvas', data);

// Doughnut
chartHelper.createDoughnutChart('canvas', data);

// Mixed (bar + line)
chartHelper.createMixedChart('canvas', {
    labels: ['Янв', 'Фев', 'Мар'],
    datasets: [
        { type: 'bar', label: 'План', data: [100, 120, 110] },
        { type: 'line', label: 'Факт', data: [95, 125, 108] }
    ]
});
```

### Sparklines

```javascript
chartHelper.createSparkline('canvas', [5, 8, 12, 10, 15], 'line');
```

### Progress Bar

```javascript
chartHelper.createProgressBar('container', 75, 100, {
    color: '#0d6efd',
    label: 'Прогресс: 75%'
});
```

### Анимация чисел

```javascript
chartHelper.animateNumber(element, 0, 1000, 2000); // от 0 до 1000 за 2 секунды
```

---

## 12. LoadingHelpers

Индикаторы загрузки.

### Использование

```javascript
// Показать skeleton
showSkeleton('container');

// Скрыть skeleton
hideSkeleton('container');

// Spinner
showSpinner('container');
hideSpinner('container');

// Overlay
showOverlay('Загрузка...');
hideOverlay();

// Для кнопок
const btn = document.querySelector('button');
btn.addEventListener('click', async () => {
    showButtonLoading(btn, 'Отправка...');
    await api.post('/data', data);
    hideButtonLoading(btn, 'Отправить');
});
```

---

## PreferencesManager

Управление настройками пользователя.

```javascript
// Установить настройку
preferences.set('theme', 'dark');
preferences.set('language', 'ru');

// Получить настройку
const theme = preferences.get('theme', 'light'); // с дефолтным значением

// Все настройки
const allPrefs = preferences.getAll();

// Экспорт/импорт
const json = preferences.export();
preferences.import(JSON.parse(json));

// Сброс
preferences.reset();
```

---

## RecentItemsManager

Управление списком недавних элементов.

```javascript
const recentItems = new RecentItemsManager(10); // макс 10 элементов

// Добавить элемент
recentItems.add('documents', {
    id: 1,
    title: 'Документ 1',
    url: '/documents/1'
});

// Получить элементы
const recent = recentItems.get('documents');

// Очистить категорию
recentItems.clear('documents');

// Очистить всё
recentItems.clearAll();
```

---

## FormStateManager

Автосохранение состояния форм.

```javascript
// Настроить автосохранение (каждые 5 секунд)
const form = document.getElementById('employeeForm');
formState.setupAutoSave(form, 5000);

// Форма автоматически восстанавливается при загрузке
// И очищается при успешной отправке

// Ручное управление
formState.save('employeeForm', { name: 'Иван', email: 'ivan@example.com' });
const savedData = formState.load('employeeForm');
formState.clear('employeeForm');
```

---

## Интеграция всех компонентов

### Пример комплексного использования

```javascript
// Страница со списком сотрудников
document.addEventListener('DOMContentLoaded', async () => {
    // Показать загрузку
    const loadingId = modalManager.loading({ message: 'Загрузка сотрудников...' });
    
    try {
        // Получить данные (с кешированием)
        const employees = await cache.getOrFetch('employees', async () => {
            return await hrAPI.getEmployees();
        }, 300000); // 5 минут
        
        // Создать DataGrid
        const grid = new DataGrid('employeesGrid', {
            data: employees,
            columns: [
                { key: 'id', label: 'ID', sortable: true },
                { key: 'name', label: 'ФИО', sortable: true, filterable: true },
                { 
                    key: 'hire_date', 
                    label: 'Дата найма',
                    render: (value) => DateUtils.formatRu(value, 'short')
                }
            ],
            pageSize: preferences.get('gridPageSize', 10),
            selectable: true,
            exportable: true
        });
        
        // Сохранить размер страницы при изменении
        grid.element.addEventListener('pageSizeChanged', (e) => {
            preferences.set('gridPageSize', e.detail.pageSize);
        });
        
        // Закрыть загрузку
        modalManager.closeLoading(loadingId);
        
        // Показать успех
        notificationManager.success('Данные загружены', 'Успех');
        
    } catch (error) {
        modalManager.closeLoading(loadingId);
        notificationManager.error('Не удалось загрузить данные', 'Ошибка');
    }
});
```

---

## Страницы демонстрации

- `/features-demo` - демо всех UI компонентов
- `/data-demo` - демо DataGrid и графиков
- `/icon-test` - тестирование иконок
- `/animations-demo` - демо анимаций

---

## Поддержка браузеров

Все компоненты работают в современных браузерах:
- Chrome 90+
- Firefox 88+
- Safari 14+
- Edge 90+

---

## Лицензия

MIT License - Simple HR System 2024
