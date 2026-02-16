# Дизайн-система ChessCalendar-RU

## Обзор

Современная дизайн-система для шахматного календаря, обеспечивающая консистентность UI/UX во всем приложении.

## Содержание

1. [Цветовая палитра](#цветовая-палитра)
2. [Типографика](#типографика)
3. [Компоненты](#компоненты)
4. [Утилиты](#утилиты)
5. [Адаптивность](#адаптивность)

## Цветовая палитра

### Основные цвета

```css
--color-primary: #8B4513;        /* Основной коричневый */
--color-primary-light: #A0522D;  /* Светлый коричневый */
--color-primary-dark: #654321;   /* Темный коричневый */
--color-secondary: #D2691E;      /* Вторичный оранжевый */
--color-accent: #FFD700;         /* Акцентный золотой */
```

### Семантические цвета

```css
--color-success: #28a745;  /* Успех */
--color-warning: #ffc107;  /* Предупреждение */
--color-danger: #dc3545;   /* Ошибка */
--color-info: #17a2b8;     /* Информация */
```

### Нейтральные цвета

```css
--color-gray-50: #F8F9FA;   /* Самый светлый */
--color-gray-100: #F1F3F5;
--color-gray-200: #E9ECEF;
--color-gray-300: #DEE2E6;
--color-gray-400: #CED4DA;
--color-gray-500: #ADB5BD;
--color-gray-600: #6C757D;
--color-gray-700: #495057;
--color-gray-800: #343A40;
--color-gray-900: #212529;  /* Самый темный */
```

## Типографика

### Шрифты

```css
--font-family-base: 'Roboto', sans-serif;
--font-family-heading: 'Roboto', sans-serif;
--font-family-mono: 'Roboto Mono', monospace;
```

### Размеры шрифтов

| Класс | Размер | Использование |
|-------|--------|---------------|
| `text-xs` | 12px | Мелкий текст, метки |
| `text-sm` | 14px | Вторичный текст |
| `text-base` | 16px | Основной текст |
| `text-lg` | 18px | Крупный текст |
| `text-xl` | 20px | Подзаголовки |
| `text-2xl` | 24px | Заголовки H3 |
| `text-3xl` | 30px | Заголовки H2 |
| `text-4xl` | 36px | Заголовки H1 |

### Веса шрифтов

```css
font-light: 300
font-normal: 400
font-medium: 500
font-semibold: 600
font-bold: 700
```

## Компоненты

### Карточки турниров

#### Стандартная карточка

```html
{% import "components/tournament_cards.html" as cards %}
{{ cards.tournament_card(tournament) }}
```

**Особенности:**
- Градиентная левая граница
- Hover эффект с подъемом
- Адаптивная структура
- Бейджи статуса
- Метаинформация с иконками

#### Компактная карточка

```html
{{ cards.tournament_card_compact(tournament) }}
```

**Использование:**
- Списки турниров
- Боковые панели
- Мобильные устройства

#### Featured карточка

```html
{{ cards.tournament_card_featured(tournament, image_url) }}
```

**Использование:**
- Главная страница
- Промо-блоки
- Избранные турниры

### Кнопки

#### Варианты

```html
<!-- Основная -->
<button class="btn btn-primary">
  <i class="bi bi-check"></i> Применить
</button>

<!-- Вторичная -->
<button class="btn btn-secondary">Отмена</button>

<!-- Контурная -->
<button class="btn btn-outline">Подробнее</button>

<!-- Призрачная -->
<button class="btn btn-ghost">
  <i class="bi bi-heart"></i>
</button>
```

#### Размеры

```html
<button class="btn btn-primary btn-sm">Маленькая</button>
<button class="btn btn-primary">Обычная</button>
<button class="btn btn-primary btn-lg">Большая</button>
<button class="btn btn-primary btn-icon">
  <i class="bi bi-heart"></i>
</button>
```

### Бейджи

```html
<span class="badge badge-primary">Основной</span>
<span class="badge badge-success">Успех</span>
<span class="badge badge-warning">Предупреждение</span>
<span class="badge badge-danger">Ошибка</span>
<span class="badge badge-info">Информация</span>
```

### Статусы турниров

```html
<span class="tournament-card-badge status-scheduled">Запланирован</span>
<span class="tournament-card-badge status-ongoing">Идет сейчас</span>
<span class="tournament-card-badge status-completed">Завершен</span>
```

## Утилиты

### Spacing

Используйте классы для отступов:

```html
<!-- Margin -->
<div class="m-4">Отступ со всех сторон</div>
<div class="mt-4">Отступ сверху</div>
<div class="mb-4">Отступ снизу</div>

<!-- Padding -->
<div class="p-4">Внутренний отступ</div>
<div class="pt-4">Внутренний отступ сверху</div>
```

Доступные значения: 0, 1, 2, 3, 4, 5, 6 (соответствуют 0, 4px, 8px, 12px, 16px, 20px, 24px)

### Flexbox

```html
<div class="d-flex justify-between items-center gap-4">
  <div>Элемент 1</div>
  <div>Элемент 2</div>
</div>
```

### Тени

```html
<div class="shadow-sm">Маленькая тень</div>
<div class="shadow-md">Средняя тень</div>
<div class="shadow-lg">Большая тень</div>
<div class="shadow-xl">Очень большая тень</div>
```

### Скругление углов

```html
<div class="rounded-sm">4px</div>
<div class="rounded-md">8px</div>
<div class="rounded-lg">12px</div>
<div class="rounded-xl">16px</div>
<div class="rounded-full">Полное скругление</div>
```

### Анимации

```html
<div class="animate-fade-in">Плавное появление</div>
<div class="animate-fade-in-up">Появление снизу</div>
<div class="animate-slide-in-right">Появление справа</div>
<div class="animate-pulse">Пульсация</div>
```

## Адаптивность

### Breakpoints

```css
/* Mobile first подход */
@media (max-width: 768px) {
  /* Мобильные устройства */
}

@media (min-width: 769px) and (max-width: 1024px) {
  /* Планшеты */
}

@media (min-width: 1025px) {
  /* Десктоп */
}
```

### Адаптивные карточки

Карточки автоматически адаптируются:
- **Мобильные**: 1 колонка
- **Планшеты**: 2 колонки
- **Десктоп**: 3 колонки

```html
<div class="row g-4">
  <div class="col-12 col-md-6 col-lg-4">
    {{ cards.tournament_card(tournament) }}
  </div>
</div>
```

## Темная тема

Дизайн-система поддерживает темную тему через атрибут `data-bs-theme`:

```html
<html data-bs-theme="dark">
```

Переключение темы:

```javascript
document.documentElement.setAttribute('data-bs-theme', 'dark');
```

## Примеры использования

### Страница со списком турниров

```html
{% extends "base_modern.html" %}
{% import "components/tournament_cards.html" as cards %}

{% block extra_css %}
<link rel="stylesheet" href="{{ url_for('static', filename='css/design-system.css') }}">
{% endblock %}

{% block content %}
<div class="container py-6">
  <h1 class="display-5 font-bold mb-6">Турниры</h1>
  
  {{ cards.tournament_grid(tournaments, 'standard') }}
</div>
{% endblock %}
```

### Компактный список

```html
<div class="tournament-list">
  {% for tournament in tournaments %}
    {{ cards.tournament_card_compact(tournament) }}
  {% endfor %}
</div>
```

### Featured секция

```html
<div class="row g-4">
  {% for tournament in featured_tournaments %}
  <div class="col-12 col-md-6">
    {{ cards.tournament_card_featured(tournament, tournament.image_url) }}
  </div>
  {% endfor %}
</div>
```

## Лучшие практики

### 1. Консистентность

Используйте компоненты из дизайн-системы вместо создания новых:

```html
<!-- ✅ Хорошо -->
<button class="btn btn-primary">Кнопка</button>

<!-- ❌ Плохо -->
<button style="background: blue; padding: 10px;">Кнопка</button>
```

### 2. Семантические цвета

Используйте семантические цвета для статусов:

```html
<!-- ✅ Хорошо -->
<span class="badge badge-success">Успешно</span>

<!-- ❌ Плохо -->
<span style="color: green;">Успешно</span>
```

### 3. Spacing

Используйте утилиты spacing вместо inline стилей:

```html
<!-- ✅ Хорошо -->
<div class="mb-4">Контент</div>

<!-- ❌ Плохо -->
<div style="margin-bottom: 16px;">Контент</div>
```

### 4. Адаптивность

Всегда тестируйте на разных устройствах:

```html
<!-- ✅ Хорошо -->
<div class="col-12 col-md-6 col-lg-4">
  Адаптивная колонка
</div>
```

### 5. Доступность

Используйте семантические HTML теги и ARIA атрибуты:

```html
<!-- ✅ Хорошо -->
<button class="btn btn-primary" aria-label="Добавить в избранное">
  <i class="bi bi-heart"></i>
</button>
```

## Расширение дизайн-системы

### Добавление новых компонентов

1. Создайте компонент в `templates/components/`
2. Используйте существующие CSS переменные
3. Добавьте документацию
4. Протестируйте на всех устройствах

### Добавление новых цветов

```css
:root {
  --color-custom: #YOUR_COLOR;
}

.badge-custom {
  background: rgba(YOUR_RGB, 0.1);
  color: var(--color-custom);
}
```

## Поддержка браузеров

- Chrome 90+
- Firefox 88+
- Safari 14+
- Edge 90+

## Changelog

### v1.0.0 (2026-02-16)
- Первый релиз дизайн-системы
- Базовые компоненты карточек
- Утилиты и переменные
- Поддержка темной темы
- Адаптивный дизайн

## Ресурсы

- [Bootstrap Icons](https://icons.getbootstrap.com/)
- [Google Fonts - Roboto](https://fonts.google.com/specimen/Roboto)
- [CSS Variables](https://developer.mozilla.org/en-US/docs/Web/CSS/Using_CSS_custom_properties)

## Контакты

По вопросам дизайн-системы обращайтесь к команде разработки.
