# Руководство по использованию дизайн-системы

## Введение

Дизайн-система ChessCalendar-RU обеспечивает консистентный и современный пользовательский интерфейс во всем приложении.

## Содержание

1. [Начало работы](#начало-работы)
2. [Компоненты](#компоненты)
3. [Утилиты](#утилиты)
4. [Лучшие практики](#лучшие-практики)
5. [Примеры](#примеры)

## Начало работы

### Подключение

В вашем шаблоне добавьте:

```html
{% extends "base_modern.html" %}

{% block extra_css %}
<link rel="stylesheet" href="{{ url_for('static', filename='css/design-system.css') }}">
{% endblock %}
```

### Импорт компонентов

```html
{% import "components/tournament_cards.html" as cards %}
```

## Компоненты

### 1. Карточки турниров

#### Стандартная карточка

Используется для основного отображения турниров.

```html
{{ cards.tournament_card(tournament) }}
```

**Когда использовать:**
- Главная страница
- Страница списка турниров
- Результаты поиска

**Особенности:**
- Полная информация о турнире
- Hover эффекты
- Адаптивный дизайн
- Действия (избранное, поделиться, подробнее)

#### Компактная карточка

Используется для боковых панелей и списков.

```html
{{ cards.tournament_card_compact(tournament) }}
```

**Когда использовать:**
- Боковые панели
- Виджеты
- Мобильные устройства
- Списки с большим количеством элементов

**Особенности:**
- Минималистичный дизайн
- Дата в отдельном блоке
- Компактная метаинформация

#### Featured карточка

Используется для промо-блоков и избранных турниров.

```html
{{ cards.tournament_card_featured(tournament, image_url) }}
```

**Когда использовать:**
- Главная страница (топ турниры)
- Промо-секции
- Баннеры

**Особенности:**
- Фоновое изображение
- Градиентный оверлей
- Крупный текст
- Визуально привлекательный

### 2. Кнопки

#### Основные варианты

```html
<!-- Основная действие -->
<button class="btn btn-primary">
  <i class="bi bi-check"></i> Применить
</button>

<!-- Вторичное действие -->
<button class="btn btn-secondary">
  Отмена
</button>

<!-- Контурная (для менее важных действий) -->
<button class="btn btn-outline">
  Подробнее
</button>

<!-- Призрачная (для иконок) -->
<button class="btn btn-ghost btn-icon">
  <i class="bi bi-heart"></i>
</button>
```

#### Размеры

```html
<button class="btn btn-primary btn-sm">Маленькая</button>
<button class="btn btn-primary">Обычная</button>
<button class="btn btn-primary btn-lg">Большая</button>
```

#### Состояния

```html
<!-- Отключенная -->
<button class="btn btn-primary" disabled>
  Недоступно
</button>

<!-- Загрузка -->
<button class="btn btn-primary">
  <span class="spinner-border spinner-border-sm"></span>
  Загрузка...
</button>
```

### 3. Бейджи

```html
<!-- Статусы -->
<span class="badge badge-success">Активен</span>
<span class="badge badge-warning">Ожидание</span>
<span class="badge badge-danger">Отменен</span>
<span class="badge badge-info">Информация</span>

<!-- Статусы турниров -->
<span class="tournament-card-badge status-scheduled">
  Запланирован
</span>
<span class="tournament-card-badge status-ongoing">
  Идет сейчас
</span>
<span class="tournament-card-badge status-completed">
  Завершен
</span>
```

## Утилиты

### Spacing (отступы)

```html
<!-- Margin -->
<div class="m-4">Отступ со всех сторон (16px)</div>
<div class="mt-4">Отступ сверху (16px)</div>
<div class="mb-6">Отступ снизу (24px)</div>

<!-- Padding -->
<div class="p-4">Внутренний отступ (16px)</div>
<div class="pt-6 pb-6">Вертикальные отступы (24px)</div>
```

**Доступные значения:**
- `0` = 0px
- `1` = 4px
- `2` = 8px
- `3` = 12px
- `4` = 16px
- `5` = 20px
- `6` = 24px

### Flexbox

```html
<!-- Горизонтальное выравнивание -->
<div class="d-flex justify-between items-center gap-4">
  <div>Слева</div>
  <div>Справа</div>
</div>

<!-- Вертикальное выравнивание -->
<div class="d-flex flex-column items-center gap-3">
  <div>Элемент 1</div>
  <div>Элемент 2</div>
</div>

<!-- Центрирование -->
<div class="d-flex justify-center items-center" style="height: 200px;">
  <div>Центрированный контент</div>
</div>
```

### Типографика

```html
<!-- Размеры -->
<p class="text-xs">Очень мелкий (12px)</p>
<p class="text-sm">Мелкий (14px)</p>
<p class="text-base">Обычный (16px)</p>
<p class="text-lg">Крупный (18px)</p>
<p class="text-xl">Очень крупный (20px)</p>

<!-- Веса -->
<p class="font-light">Легкий (300)</p>
<p class="font-normal">Обычный (400)</p>
<p class="font-medium">Средний (500)</p>
<p class="font-semibold">Полужирный (600)</p>
<p class="font-bold">Жирный (700)</p>

<!-- Цвета -->
<p class="text-primary">Основной цвет</p>
<p class="text-success">Успех</p>
<p class="text-danger">Ошибка</p>
<p class="text-muted">Приглушенный</p>
```

### Тени

```html
<div class="shadow-sm">Маленькая тень</div>
<div class="shadow-md">Средняя тень</div>
<div class="shadow-lg">Большая тень</div>
<div class="shadow-xl">Очень большая тень</div>
```

### Скругление

```html
<div class="rounded-sm">4px</div>
<div class="rounded-md">8px</div>
<div class="rounded-lg">12px</div>
<div class="rounded-xl">16px</div>
<div class="rounded-full">Полное</div>
```

### Анимации

```html
<div class="animate-fade-in">Плавное появление</div>
<div class="animate-fade-in-up">Появление снизу</div>
<div class="animate-slide-in-right">Появление справа</div>
<div class="animate-pulse">Пульсация</div>
```

## Лучшие практики

### 1. Используйте компоненты вместо кастомных стилей

❌ **Плохо:**
```html
<div style="padding: 16px; background: white; border-radius: 12px;">
  Контент
</div>
```

✅ **Хорошо:**
```html
<div class="card">
  <div class="card-body">
    Контент
  </div>
</div>
```

### 2. Используйте утилиты spacing

❌ **Плохо:**
```html
<div style="margin-bottom: 24px;">Контент</div>
```

✅ **Хорошо:**
```html
<div class="mb-6">Контент</div>
```

### 3. Используйте семантические цвета

❌ **Плохо:**
```html
<span style="color: green;">Успешно</span>
```

✅ **Хорошо:**
```html
<span class="badge badge-success">Успешно</span>
```

### 4. Используйте адаптивные классы

❌ **Плохо:**
```html
<div class="col-4">Контент</div>
```

✅ **Хорошо:**
```html
<div class="col-12 col-md-6 col-lg-4">Контент</div>
```

### 5. Группируйте связанные элементы

❌ **Плохо:**
```html
<button class="btn btn-primary">Кнопка 1</button>
<button class="btn btn-primary">Кнопка 2</button>
```

✅ **Хорошо:**
```html
<div class="d-flex gap-2">
  <button class="btn btn-primary">Кнопка 1</button>
  <button class="btn btn-primary">Кнопка 2</button>
</div>
```

## Примеры

### Пример 1: Страница списка турниров

```html
{% extends "base_modern.html" %}
{% import "components/tournament_cards.html" as cards %}

{% block extra_css %}
<link rel="stylesheet" href="{{ url_for('static', filename='css/design-system.css') }}">
{% endblock %}

{% block content %}
<div class="container py-6">
  <!-- Заголовок -->
  <div class="d-flex justify-between items-center mb-6">
    <div>
      <h1 class="display-5 font-bold mb-2">
        <i class="bi bi-trophy"></i> Турниры
      </h1>
      <p class="text-muted">Найдите идеальный турнир</p>
    </div>
    <button class="btn btn-primary">
      <i class="bi bi-plus"></i> Добавить турнир
    </button>
  </div>
  
  <!-- Сетка турниров -->
  <div class="row g-4">
    {% for tournament in tournaments %}
    <div class="col-12 col-md-6 col-lg-4">
      {{ cards.tournament_card(tournament) }}
    </div>
    {% endfor %}
  </div>
</div>
{% endblock %}
```

### Пример 2: Боковая панель с компактными карточками

```html
<div class="sidebar">
  <h5 class="font-semibold mb-4">
    <i class="bi bi-star"></i> Избранные турниры
  </h5>
  
  {% for tournament in favorite_tournaments %}
    {{ cards.tournament_card_compact(tournament) }}
  {% endfor %}
</div>
```

### Пример 3: Featured секция на главной

```html
<div class="container py-6">
  <h2 class="display-6 font-bold mb-6 text-center">
    Топ турниры месяца
  </h2>
  
  <div class="row g-4">
    {% for tournament in featured_tournaments %}
    <div class="col-12 col-md-6">
      {{ cards.tournament_card_featured(tournament, tournament.image_url) }}
    </div>
    {% endfor %}
  </div>
</div>
```

### Пример 4: Форма с кнопками

```html
<form class="card">
  <div class="card-body">
    <h3 class="card-title mb-4">Добавить турнир</h3>
    
    <div class="mb-4">
      <label class="form-label">Название</label>
      <input type="text" class="form-control" name="name">
    </div>
    
    <div class="mb-4">
      <label class="form-label">Описание</label>
      <textarea class="form-control" name="description" rows="3"></textarea>
    </div>
  </div>
  
  <div class="card-footer">
    <div class="d-flex justify-end gap-2">
      <button type="button" class="btn btn-secondary">
        Отмена
      </button>
      <button type="submit" class="btn btn-primary">
        <i class="bi bi-check"></i> Сохранить
      </button>
    </div>
  </div>
</form>
```

### Пример 5: Статусы и бейджи

```html
<div class="d-flex flex-wrap gap-2 mb-4">
  <span class="badge badge-success">
    <i class="bi bi-check-circle"></i> Активен
  </span>
  <span class="badge badge-warning">
    <i class="bi bi-clock"></i> Ожидание
  </span>
  <span class="badge badge-danger">
    <i class="bi bi-x-circle"></i> Отменен
  </span>
</div>
```

## Адаптивность

### Breakpoints

- **Mobile**: < 768px
- **Tablet**: 768px - 1024px
- **Desktop**: > 1024px

### Адаптивные классы

```html
<!-- Скрыть на мобильных -->
<div class="d-none d-md-block">
  Видно только на планшетах и десктопе
</div>

<!-- Показать только на мобильных -->
<div class="d-block d-md-none">
  Видно только на мобильных
</div>

<!-- Адаптивные колонки -->
<div class="row">
  <div class="col-12 col-md-6 col-lg-4">
    1 колонка на мобильных
    2 колонки на планшетах
    3 колонки на десктопе
  </div>
</div>
```

## Темная тема

### Переключение темы

```javascript
// Установить темную тему
document.documentElement.setAttribute('data-bs-theme', 'dark');

// Установить светлую тему
document.documentElement.setAttribute('data-bs-theme', 'light');

// Сохранить выбор
localStorage.setItem('theme', 'dark');

// Загрузить сохраненную тему
const savedTheme = localStorage.getItem('theme') || 'light';
document.documentElement.setAttribute('data-bs-theme', savedTheme);
```

### Кастомные стили для темной темы

```css
/* Автоматически применяется в темной теме */
[data-bs-theme="dark"] .custom-element {
  background: var(--color-gray-800);
  color: var(--color-gray-100);
}
```

## Доступность

### Используйте семантические теги

```html
<!-- ✅ Хорошо -->
<button class="btn btn-primary">Кнопка</button>
<nav>...</nav>
<main>...</main>

<!-- ❌ Плохо -->
<div onclick="...">Кнопка</div>
```

### Добавляйте ARIA атрибуты

```html
<button class="btn btn-icon" aria-label="Добавить в избранное">
  <i class="bi bi-heart"></i>
</button>

<nav aria-label="Основная навигация">
  ...
</nav>
```

### Обеспечьте контрастность

Все цвета в дизайн-системе соответствуют WCAG AA стандартам.

## Производительность

### Оптимизация изображений

```html
<!-- Используйте srcset для адаптивных изображений -->
<img src="image.jpg" 
     srcset="image-small.jpg 480w, image-medium.jpg 768w, image-large.jpg 1200w"
     sizes="(max-width: 768px) 100vw, 50vw"
     alt="Описание">
```

### Ленивая загрузка

```html
<img src="image.jpg" loading="lazy" alt="Описание">
```

## Ресурсы

- [Полная документация](../DESIGN_SYSTEM.md)
- [Демонстрация компонентов](/design-system)
- [Bootstrap Icons](https://icons.getbootstrap.com/)

## Поддержка

По вопросам дизайн-системы обращайтесь к команде разработки.
