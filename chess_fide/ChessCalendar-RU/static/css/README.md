# ChessCalendar-RU Design System

## Быстрый старт

### 1. Подключение дизайн-системы

```html
<!-- В вашем шаблоне -->
<link rel="stylesheet" href="{{ url_for('static', filename='css/design-system.css') }}">
```

### 2. Использование компонентов

```html
{% import "components/tournament_cards.html" as cards %}

<!-- Стандартная карточка -->
{{ cards.tournament_card(tournament) }}

<!-- Компактная карточка -->
{{ cards.tournament_card_compact(tournament) }}

<!-- Сетка карточек -->
{{ cards.tournament_grid(tournaments) }}
```

### 3. Использование утилит

```html
<!-- Кнопки -->
<button class="btn btn-primary">
  <i class="bi bi-check"></i> Применить
</button>

<!-- Бейджи -->
<span class="badge badge-success">Успех</span>

<!-- Spacing -->
<div class="p-4 mb-6">
  Контент с отступами
</div>

<!-- Flexbox -->
<div class="d-flex justify-between items-center gap-4">
  <div>Элемент 1</div>
  <div>Элемент 2</div>
</div>
```

## Структура файлов

```
static/css/
├── design-system.css       # Основная дизайн-система
└── README.md              # Эта документация

templates/components/
└── tournament_cards.html  # Компоненты карточек турниров

docs/
└── DESIGN_SYSTEM.md       # Полная документация
```

## Основные компоненты

### Карточки турниров

- `tournament_card()` - Стандартная карточка
- `tournament_card_compact()` - Компактная карточка
- `tournament_card_featured()` - Featured карточка с изображением
- `tournament_list_item()` - Элемент списка
- `tournament_grid()` - Сетка карточек
- `tournament_list()` - Список карточек

### Кнопки

- `.btn-primary` - Основная кнопка
- `.btn-secondary` - Вторичная кнопка
- `.btn-outline` - Контурная кнопка
- `.btn-ghost` - Призрачная кнопка
- `.btn-sm`, `.btn-lg` - Размеры
- `.btn-icon` - Кнопка-иконка

### Бейджи

- `.badge-primary` - Основной
- `.badge-success` - Успех
- `.badge-warning` - Предупреждение
- `.badge-danger` - Ошибка
- `.badge-info` - Информация

## CSS Переменные

### Цвета

```css
--color-primary: #8B4513;
--color-secondary: #D2691E;
--color-accent: #FFD700;
--color-success: #28a745;
--color-warning: #ffc107;
--color-danger: #dc3545;
--color-info: #17a2b8;
```

### Spacing

```css
--spacing-1: 0.25rem;  /* 4px */
--spacing-2: 0.5rem;   /* 8px */
--spacing-3: 0.75rem;  /* 12px */
--spacing-4: 1rem;     /* 16px */
--spacing-5: 1.25rem;  /* 20px */
--spacing-6: 1.5rem;   /* 24px */
```

### Тени

```css
--shadow-sm: 0 2px 4px rgba(0, 0, 0, 0.08);
--shadow-md: 0 4px 8px rgba(0, 0, 0, 0.1);
--shadow-lg: 0 8px 16px rgba(0, 0, 0, 0.12);
--shadow-xl: 0 12px 24px rgba(0, 0, 0, 0.15);
```

## Примеры

### Страница со списком турниров

```html
{% extends "base_modern.html" %}
{% import "components/tournament_cards.html" as cards %}

{% block extra_css %}
<link rel="stylesheet" href="{{ url_for('static', filename='css/design-system.css') }}">
{% endblock %}

{% block content %}
<div class="container py-6">
  <h1 class="display-5 font-bold mb-6">
    <i class="bi bi-trophy"></i> Турниры
  </h1>
  
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

### Кастомная карточка

```html
<div class="tournament-card">
  <div class="tournament-card-header">
    <div>
      <h3 class="tournament-card-title">Название турнира</h3>
      <p class="tournament-card-subtitle">Организатор</p>
    </div>
    <span class="tournament-card-badge status-scheduled">
      Запланирован
    </span>
  </div>
  
  <div class="tournament-card-body">
    <div class="tournament-card-meta">
      <div class="tournament-card-meta-item">
        <i class="bi bi-geo-alt"></i>
        <span>Москва</span>
      </div>
      <div class="tournament-card-meta-item">
        <i class="bi bi-calendar"></i>
        <span>15.03.2026 - 25.03.2026</span>
      </div>
    </div>
    
    <p class="tournament-card-description">
      Описание турнира...
    </p>
  </div>
  
  <div class="tournament-card-footer">
    <div class="tournament-card-tags">
      <span class="tournament-card-tag">Чемпионат</span>
    </div>
    <div class="tournament-card-actions">
      <button class="btn btn-primary btn-sm">
        <i class="bi bi-eye"></i> Подробнее
      </button>
    </div>
  </div>
</div>
```

## Темная тема

Дизайн-система автоматически поддерживает темную тему:

```javascript
// Переключение темы
document.documentElement.setAttribute('data-bs-theme', 'dark');

// Или
document.documentElement.setAttribute('data-bs-theme', 'light');
```

## Адаптивность

Все компоненты адаптивны по умолчанию:

```html
<!-- Адаптивная сетка -->
<div class="row g-4">
  <div class="col-12 col-md-6 col-lg-4">
    <!-- 1 колонка на мобильных, 2 на планшетах, 3 на десктопе -->
  </div>
</div>
```

## Демонстрация

Посмотрите полную демонстрацию всех компонентов:

```
/design-system
```

## Документация

Полная документация доступна в:

```
docs/DESIGN_SYSTEM.md
```

## Поддержка

По вопросам дизайн-системы обращайтесь к команде разработки.
