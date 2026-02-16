# Design Document: Fix Tournament Cards Responsive

## Overview

Данный дизайн описывает решение для исправления проблем с адаптивностью карточек турниров в проекте ChessCalendar-RU. Решение основано на принципе Mobile-First и использует современные CSS техники для обеспечения оптимального отображения на всех устройствах.

### Цели дизайна

1. Обеспечить корректное отображение всех типов карточек на устройствах с различными размерами экрана
2. Улучшить пользовательский опыт на мобильных устройствах
3. Сохранить существующий функционал и визуальный стиль
4. Оптимизировать производительность на мобильных устройствах
5. Обеспечить соответствие стандартам доступности (минимальные размеры touch targets)

### Принципы дизайна

- **Mobile-First**: Базовые стили для мобильных устройств, затем расширение для больших экранов
- **Progressive Enhancement**: Добавление расширенных возможностей для устройств, которые их поддерживают
- **Performance**: Оптимизация анимаций и эффектов для мобильных устройств
- **Accessibility**: Минимальные размеры touch targets 44x44px, читаемые размеры шрифтов
- **Consistency**: Единообразное поведение всех типов карточек

## Architecture

### Структура компонентов

```
Tournament Card System
├── Standard Card (tournament_card)
│   ├── Card Header (title, badge, status)
│   ├── Card Body (meta info, description)
│   └── Card Footer (tags, actions)
├── Compact Card (tournament_card_compact)
│   ├── Date Block
│   ├── Content Block
│   └── Actions
├── Featured Card (tournament_card_featured)
│   ├── Image Layer
│   └── Overlay Layer (title, meta, actions)
└── List Item Card (tournament_list_item)
    ├── Content Block
    └── Actions Block
```

### Breakpoint Strategy

Используем стандартные Bootstrap 5 breakpoints:

- **xs (0-575px)**: Мобильные телефоны (портрет) - 1 колонка
- **sm (576-767px)**: Мобильные телефоны (ландшафт) - 1 колонка
- **md (768-991px)**: Планшеты - 2 колонки
- **lg (992-1199px)**: Десктопы - 3 колонки
- **xl (1200px+)**: Большие десктопы - 3 колонки

### CSS Architecture

Создадим новый файл `tournament-cards-responsive.css`, который будет содержать все адаптивные стили. Этот файл будет подключаться после `tournament-cards-enhanced.css` и переопределять необходимые стили.

## Components and Interfaces

### 1. Standard Card (tournament_card)

#### Структура HTML (без изменений)

```html
<div class="tournament-card animate-fade-in-up">
  <div class="tournament-card-header">
    <div>
      <h3 class="tournament-card-title">{{ tournament.name }}</h3>
      <p class="tournament-card-subtitle">{{ tournament.organizer }}</p>
    </div>
    <span class="tournament-card-badge status-{{ tournament.status|lower }}">
      {{ tournament.status }}
    </span>
  </div>
  
  <div class="tournament-card-body">
    <div class="tournament-card-meta">
      <!-- Meta items -->
    </div>
    <p class="tournament-card-description">{{ tournament.description }}</p>
  </div>
  
  <div class="tournament-card-footer">
    <div class="tournament-card-tags"><!-- Tags --></div>
    <div class="tournament-card-actions"><!-- Actions --></div>
  </div>
</div>
```

#### Адаптивные стили

```css
/* Mobile First - Base styles (xs, sm) */
.tournament-card {
    border-radius: 0.5rem; /* 8px */
}

.tournament-card-header {
    padding: 0.75rem; /* 12px */
    display: flex;
    flex-direction: column;
    gap: 0.5rem;
    align-items: flex-start;
}

.tournament-card-body {
    padding: 1rem; /* 16px */
    gap: 0.75rem;
}

.tournament-card-footer {
    padding: 0.75rem; /* 12px */
    flex-direction: column;
    gap: 0.75rem;
}

.tournament-card-title {
    font-size: 1.125rem; /* 18px */
    line-height: 1.4;
}

.tournament-card-subtitle {
    font-size: 0.875rem; /* 14px */
}

.tournament-card-meta {
    display: flex;
    flex-direction: column;
    gap: 0.5rem;
}

.tournament-card-meta-item {
    font-size: 0.8125rem; /* 13px */
}

.tournament-card-meta-item i {
    font-size: 1rem; /* 16px */
}

.tournament-card-actions {
    display: flex;
    flex-direction: column;
    gap: 0.5rem;
    width: 100%;
}

.tournament-card-actions .btn {
    width: 100%;
    min-height: 44px;
}

.tournament-card-actions .btn-icon {
    min-width: 44px;
    min-height: 44px;
}

.tournament-card-tags {
    display: flex;
    flex-wrap: wrap;
    gap: 0.5rem;
}

.tournament-card-tag {
    font-size: 0.75rem; /* 12px */
    padding: 0.25rem 0.5rem;
    min-height: 32px;
    display: inline-flex;
    align-items: center;
}

/* Tablet and up (md) */
@media (min-width: 768px) {
    .tournament-card {
        border-radius: 0.75rem; /* 12px */
    }
    
    .tournament-card-header {
        padding: 1rem; /* 16px */
        flex-direction: row;
        justify-content: space-between;
        align-items: flex-start;
    }
    
    .tournament-card-body {
        padding: 1.25rem; /* 20px */
        gap: 1rem;
    }
    
    .tournament-card-footer {
        padding: 1rem; /* 16px */
        flex-direction: row;
        justify-content: space-between;
        align-items: center;
    }
    
    .tournament-card-title {
        font-size: 1.25rem; /* 20px */
    }
    
    .tournament-card-subtitle {
        font-size: 1rem; /* 16px */
    }
    
    .tournament-card-meta {
        flex-direction: row;
        flex-wrap: wrap;
        gap: 0.75rem;
    }
    
    .tournament-card-meta-item {
        font-size: 0.875rem; /* 14px */
    }
    
    .tournament-card-actions {
        flex-direction: row;
        width: auto;
        gap: 0.5rem;
    }
    
    .tournament-card-actions .btn {
        width: auto;
    }
    
    .tournament-card-tag {
        font-size: 0.8125rem; /* 13px */
        padding: 0.375rem 0.75rem;
    }
}

/* Desktop hover effects (only for devices with hover capability) */
@media (hover: hover) and (pointer: fine) {
    .tournament-card:hover {
        transform: translateY(-8px) scale(1.02);
    }
    
    .tournament-quick-actions {
        opacity: 0;
        transform: translateY(-10px);
    }
    
    .tournament-card:hover .tournament-quick-actions {
        opacity: 1;
        transform: translateY(0);
    }
}

/* Mobile - always show quick actions */
@media (hover: none) {
    .tournament-quick-actions {
        opacity: 1;
        transform: translateY(0);
    }
    
    .tournament-card:hover {
        transform: none;
    }
}
```

### 2. Compact Card (tournament_card_compact)

#### Адаптивные стили

```css
/* Mobile First - Base styles */
.tournament-card-compact {
    flex-direction: column;
}

.tournament-card-compact-date {
    width: 100%;
    padding: 1rem;
    border-right: none;
    border-bottom: 2px solid var(--color-border-primary);
    display: flex;
    flex-direction: row;
    align-items: center;
    justify-content: center;
    gap: 0.5rem;
}

.tournament-card-compact-content {
    padding: 1rem;
    flex: 1;
}

.tournament-card-compact-title {
    font-size: 1rem; /* 16px */
}

.tournament-card-compact-meta {
    font-size: 0.8125rem; /* 13px */
    display: flex;
    flex-direction: column;
    gap: 0.5rem;
}

/* Small devices and up (sm) */
@media (min-width: 576px) {
    .tournament-card-compact {
        flex-direction: row;
    }
    
    .tournament-card-compact-date {
        width: 80px;
        padding: 0.75rem;
        border-right: 2px solid var(--color-border-primary);
        border-bottom: none;
        flex-direction: column;
        gap: 0.25rem;
    }
    
    .tournament-card-compact-content {
        padding: 0.75rem;
    }
    
    .tournament-card-compact-title {
        font-size: 1.125rem; /* 18px */
    }
    
    .tournament-card-compact-meta {
        flex-direction: row;
        flex-wrap: wrap;
        gap: 0.75rem;
    }
}
```

### 3. Featured Card (tournament_card_featured)

#### Адаптивные стили

```css
/* Mobile First - Base styles */
.tournament-card-featured {
    min-height: 300px;
    position: relative;
    overflow: hidden;
}

.tournament-card-featured-image {
    width: 100%;
    height: 100%;
    object-fit: cover;
    position: absolute;
    top: 0;
    left: 0;
}

.tournament-card-featured-overlay {
    position: relative;
    z-index: 1;
    padding: 1rem;
    background: linear-gradient(to top, rgba(0, 0, 0, 0.8) 0%, rgba(0, 0, 0, 0.4) 50%, transparent 100%);
    min-height: 300px;
    display: flex;
    flex-direction: column;
    justify-content: flex-end;
}

.tournament-card-featured-title {
    font-size: 1.25rem; /* 20px */
    color: white;
    margin-bottom: 0.75rem;
}

.tournament-card-featured-meta {
    font-size: 0.875rem; /* 14px */
    color: rgba(255, 255, 255, 0.9);
    display: flex;
    flex-direction: column;
    gap: 0.5rem;
}

/* Tablet and up (md) */
@media (min-width: 768px) {
    .tournament-card-featured {
        min-height: 400px;
    }
    
    .tournament-card-featured-overlay {
        padding: 1.5rem;
        min-height: 400px;
    }
    
    .tournament-card-featured-title {
        font-size: 1.5rem; /* 24px */
    }
    
    .tournament-card-featured-meta {
        flex-direction: row;
        flex-wrap: wrap;
        gap: 1rem;
        font-size: 1rem; /* 16px */
    }
}
```

### 4. List Item Card (tournament_list_item)

#### Адаптивные стили

```css
/* Mobile First - Base styles */
.tournament-list-item {
    display: flex;
    flex-direction: column;
    padding: 0.75rem;
    gap: 0.75rem;
}

.tournament-list-item-content {
    flex: 1;
}

.tournament-list-item-title {
    font-size: 1rem; /* 16px */
}

.tournament-list-item-meta {
    display: flex;
    flex-wrap: wrap;
    gap: 0.5rem;
    font-size: 0.8125rem; /* 13px */
}

.tournament-list-item-actions {
    display: flex;
    flex-direction: column;
    gap: 0.5rem;
    width: 100%;
}

.tournament-list-item-actions .btn {
    width: 100%;
    min-height: 44px;
}

/* Tablet and up (md) */
@media (min-width: 768px) {
    .tournament-list-item {
        flex-direction: row;
        align-items: center;
        justify-content: space-between;
        padding: 1rem;
    }
    
    .tournament-list-item-title {
        font-size: 1.125rem; /* 18px */
    }
    
    .tournament-list-item-meta {
        gap: 0.75rem;
        font-size: 0.875rem; /* 14px */
    }
    
    .tournament-list-item-actions {
        flex-direction: row;
        width: auto;
        gap: 0.5rem;
    }
    
    .tournament-list-item-actions .btn {
        width: auto;
    }
}
```

### 5. Tournament Grid Macro

#### Обновление макроса

```jinja2
{% macro tournament_grid(tournaments, card_type='standard') %}
<div class="row g-3 g-md-4">
  {% for tournament in tournaments %}
  <div class="col-12 col-md-6 col-lg-4">
    {% if card_type == 'compact' %}
      {{ tournament_card_compact(tournament) }}
    {% elif card_type == 'featured' %}
      {{ tournament_card_featured(tournament, tournament.image_url) }}
    {% else %}
      {{ tournament_card(tournament) }}
    {% endif %}
  </div>
  {% else %}
  <div class="col-12">
    {{ tournament_empty_state() }}
  </div>
  {% endfor %}
</div>
{% endmacro %}
```

## Data Models

Данное решение не требует изменений в моделях данных. Все изменения касаются только представления (CSS и HTML структуры).

### Существующая модель Tournament

```python
class Tournament:
    id: int
    name: str
    organizer: str
    location: str
    start_date: datetime
    end_date: datetime
    status: str  # 'Scheduled', 'Ongoing', 'Completed'
    category: str
    rating_type: str
    prize_fund: str (optional)
    description: str (optional)
    image_url: str (optional)
```


## Correctness Properties

A property is a characteristic or behavior that should hold true across all valid executions of a system—essentially, a formal statement about what the system should do. Properties serve as the bridge between human-readable specifications and machine-verifiable correctness guarantees.

### Property Reflection

После анализа всех acceptance criteria, я выявил следующие группы избыточности:

1. **Padding properties (2.1-2.6)**: Можно объединить в одно свойство, которое проверяет все padding значения для всех элементов карточки на обоих breakpoints
2. **Typography properties (3.1-3.6)**: Можно объединить в одно свойство для всех текстовых элементов
3. **Layout direction properties**: Множество свойств проверяют flex-direction на разных breakpoints - можно объединить по компонентам
4. **Column layout properties (1.1-1.5)**: Можно объединить в одно свойство, которое проверяет количество колонок для всех breakpoints

### Core Properties

Property 1: Responsive grid column layout
*For any* viewport width, the tournament grid should display the correct number of columns: 1 column for widths < 768px, 2 columns for 768-991px, and 3 columns for widths >= 992px
**Validates: Requirements 1.1, 1.2, 1.3, 1.4, 1.5**

Property 2: Responsive spacing consistency
*For any* card component, the gap spacing between cards should be 1rem (16px) on mobile (< 768px) and 1.5rem (24px) on desktop (>= 768px)
**Validates: Requirements 1.6**

Property 3: Standard card padding responsiveness
*For any* Standard_Card, the padding values should be: header 0.75rem/1rem, body 1rem/1.25rem, footer 0.75rem/1rem for mobile/desktop respectively, where mobile is < 768px and desktop is >= 768px
**Validates: Requirements 2.1, 2.2, 2.3, 2.4, 2.5, 2.6**

Property 4: Standard card border-radius responsiveness
*For any* Standard_Card, the border-radius should be 0.5rem (8px) when viewport < 768px and 0.75rem (12px) when viewport >= 768px
**Validates: Requirements 2.7, 2.8**

Property 5: Typography scaling across breakpoints
*For any* text element in Standard_Card (title, subtitle, meta items), the font-size should scale appropriately: smaller values for mobile (< 768px) and larger values for desktop (>= 768px) according to the specification
**Validates: Requirements 3.1, 3.2, 3.3, 3.4, 3.5, 3.6**

Property 6: Input font-size minimum for iOS
*For any* input element in the card system, the font-size should be at least 16px to prevent automatic zoom on iOS devices
**Validates: Requirements 3.7**

Property 7: Header layout responsiveness
*For any* Standard_Card header, the flex-direction should be column with flex-start alignment when viewport < 576px, and row with space-between when viewport >= 576px
**Validates: Requirements 4.1, 4.2, 4.3, 4.4, 4.5**

Property 8: Title text truncation
*For any* Standard_Card title with text longer than 2 lines, the text should truncate with ellipsis after 2 lines on all viewport sizes
**Validates: Requirements 4.6**

Property 9: Footer actions layout responsiveness
*For any* Standard_Card footer actions, the layout should be vertical (column) with 100% width buttons when viewport < 576px, and horizontal (row) with auto width buttons when viewport >= 576px
**Validates: Requirements 5.1, 5.2, 5.3, 5.4**

Property 10: Touch target minimum size
*For any* interactive button or icon in the card system, the minimum touch target size should be 44x44px on all devices
**Validates: Requirements 5.5, 5.6**

Property 11: Compact card layout responsiveness
*For any* Compact_Card, the flex-direction should be column with 100% width date block when viewport < 576px, and row with 80px width date block when viewport >= 576px
**Validates: Requirements 6.1, 6.2, 6.3, 6.4**

Property 12: Compact card border positioning
*For any* Compact_Card date block, the border should be on the bottom when viewport < 576px and on the right when viewport >= 576px
**Validates: Requirements 6.5**

Property 13: Compact card content padding
*For any* Compact_Card content block, the padding should be 1rem when viewport < 576px and 0.75rem when viewport >= 576px
**Validates: Requirements 6.6, 6.7**

Property 14: Featured card height responsiveness
*For any* Featured_Card, the minimum height should be 300px when viewport < 768px and 400px when viewport >= 768px
**Validates: Requirements 7.1, 7.2**

Property 15: Featured card overlay padding
*For any* Featured_Card overlay, the padding should be 1rem when viewport < 768px and 1.5rem when viewport >= 768px
**Validates: Requirements 7.3, 7.4**

Property 16: Featured card title typography
*For any* Featured_Card title, the font-size should be 1.25rem (20px) when viewport < 768px and 1.5rem (24px) when viewport >= 768px
**Validates: Requirements 7.5, 7.6**

Property 17: Featured card image aspect ratio
*For any* Featured_Card image, the object-fit property should be set to cover to maintain aspect ratio while covering the card area on all devices
**Validates: Requirements 7.7, 13.4**

Property 18: List item card layout responsiveness
*For any* List_Item_Card, the flex-direction should be column when viewport < 768px and row with space-between when viewport >= 768px
**Validates: Requirements 8.1, 8.2**

Property 19: List item card actions width
*For any* List_Item_Card actions block, the width should be 100% with full-width buttons when viewport < 768px, and auto width with auto-width buttons when viewport >= 768px
**Validates: Requirements 8.4, 8.5, 8.6**

Property 20: List item card padding
*For any* List_Item_Card, the padding should be 0.75rem when viewport < 768px and 1rem when viewport >= 768px
**Validates: Requirements 8.7**

Property 21: Meta items layout responsiveness
*For any* meta items container in the card system, the flex-direction should be column when viewport < 576px and row with wrapping when viewport >= 576px
**Validates: Requirements 9.1, 9.2**

Property 22: Meta items gap spacing
*For any* meta items container, the gap should be 0.5rem when viewport < 576px and 0.75rem when viewport >= 576px
**Validates: Requirements 9.3, 9.4**

Property 23: Meta item icon size
*For any* meta item icon, the font-size should be 1rem (16px) when viewport < 576px
**Validates: Requirements 9.5**

Property 24: Meta items text truncation
*For any* meta item with long text, the text should truncate with ellipsis on all devices
**Validates: Requirements 9.6**

Property 25: Tag typography responsiveness
*For any* tag in the card system, the font-size should be 0.75rem (12px) when viewport < 576px and 0.8125rem (13px) when viewport >= 576px
**Validates: Requirements 11.1, 11.2**

Property 26: Tag padding responsiveness
*For any* tag in the card system, the padding should be 0.25rem 0.5rem when viewport < 576px and 0.375rem 0.75rem when viewport >= 576px
**Validates: Requirements 11.3, 11.4**

Property 27: Tag wrapping behavior
*For any* tags container, the tags should wrap to multiple lines when viewport < 576px
**Validates: Requirements 11.5**

Property 28: Tag touch target size
*For any* tag on mobile devices, the minimum touch target size should be 32x32px
**Validates: Requirements 11.6**

Property 29: Orientation compatibility
*For any* card component, the layout and functionality should remain correct in both portrait and landscape orientations
**Validates: Requirements 15.7**

## Error Handling

### CSS Fallbacks

1. **Flexbox fallback**: Если браузер не поддерживает flexbox, используем display: block с соответствующими отступами
2. **Grid fallback**: Если браузер не поддерживает CSS Grid, используем Bootstrap's flexbox grid
3. **Custom properties fallback**: Предоставляем статические значения для браузеров без поддержки CSS custom properties
4. **Object-fit fallback**: Для браузеров без поддержки object-fit используем background-image подход

### Image Loading Errors

```javascript
// Fallback для изображений
document.querySelectorAll('.tournament-card-featured-image').forEach(img => {
    img.addEventListener('error', function() {
        this.src = '/static/images/default-tournament.jpg';
        this.alt = 'Default tournament image';
    });
});
```

### Viewport Detection

```javascript
// Определение текущего breakpoint
function getCurrentBreakpoint() {
    const width = window.innerWidth;
    if (width < 576) return 'xs';
    if (width < 768) return 'sm';
    if (width < 992) return 'md';
    if (width < 1200) return 'lg';
    return 'xl';
}

// Обработка изменения размера окна
let resizeTimer;
window.addEventListener('resize', function() {
    clearTimeout(resizeTimer);
    resizeTimer = setTimeout(function() {
        const breakpoint = getCurrentBreakpoint();
        document.body.setAttribute('data-breakpoint', breakpoint);
    }, 250);
});
```

### Touch Device Detection

```javascript
// Определение touch устройства
const isTouchDevice = 'ontouchstart' in window || navigator.maxTouchPoints > 0;
if (isTouchDevice) {
    document.body.classList.add('touch-device');
} else {
    document.body.classList.add('no-touch');
}
```

## Testing Strategy

### Dual Testing Approach

Мы будем использовать комбинацию unit тестов и property-based тестов для обеспечения полного покрытия:

- **Unit tests**: Проверка конкретных примеров, edge cases и условий ошибок
- **Property tests**: Проверка универсальных свойств на множестве входных данных

### Unit Testing

Unit тесты будут фокусироваться на:

1. **Конкретные примеры**: Проверка отображения карточек на конкретных размерах экрана (iPhone SE, iPad, Desktop)
2. **Edge cases**: Очень длинные названия турниров, отсутствие изображений, пустые поля
3. **Интеграционные точки**: Взаимодействие с Bootstrap grid, корректная работа Jinja2 макросов
4. **Условия ошибок**: Обработка ошибок загрузки изображений, отсутствие данных

Примеры unit тестов:

```python
def test_standard_card_renders_on_mobile():
    """Test that standard card renders correctly on mobile viewport"""
    viewport_width = 375  # iPhone SE
    card = render_tournament_card(sample_tournament, viewport_width)
    assert card.header_padding == '0.75rem'
    assert card.body_padding == '1rem'
    assert card.title_font_size == '1.125rem'

def test_compact_card_layout_on_tablet():
    """Test that compact card uses horizontal layout on tablet"""
    viewport_width = 768  # iPad
    card = render_compact_card(sample_tournament, viewport_width)
    assert card.flex_direction == 'row'
    assert card.date_block_width == '80px'

def test_featured_card_with_missing_image():
    """Test that featured card handles missing image gracefully"""
    tournament = create_tournament(image_url=None)
    card = render_featured_card(tournament)
    assert card.image_src == '/static/images/default-tournament.jpg'
```

### Property-Based Testing

Property тесты будут использовать библиотеку **Hypothesis** для Python и будут проверять универсальные свойства на множестве сгенерированных входных данных.

Конфигурация:
- Минимум 100 итераций на каждый property тест
- Каждый тест должен ссылаться на соответствующее свойство из дизайна
- Формат тега: **Feature: fix-tournament-cards-responsive, Property {number}: {property_text}**

Примеры property тестов:

```python
from hypothesis import given, strategies as st
import pytest

# Feature: fix-tournament-cards-responsive, Property 1: Responsive grid column layout
@given(viewport_width=st.integers(min_value=320, max_value=2560))
@pytest.mark.property_test
def test_property_1_grid_columns_for_all_viewports(viewport_width):
    """
    For any viewport width, the tournament grid should display the correct 
    number of columns: 1 column for widths < 768px, 2 columns for 768-991px, 
    and 3 columns for widths >= 992px
    """
    grid = render_tournament_grid(sample_tournaments, viewport_width)
    
    if viewport_width < 768:
        assert grid.column_count == 1
    elif 768 <= viewport_width < 992:
        assert grid.column_count == 2
    else:
        assert grid.column_count == 3

# Feature: fix-tournament-cards-responsive, Property 3: Standard card padding responsiveness
@given(
    viewport_width=st.integers(min_value=320, max_value=2560),
    tournament=st.builds(Tournament)
)
@pytest.mark.property_test
def test_property_3_standard_card_padding(viewport_width, tournament):
    """
    For any Standard_Card, the padding values should be: 
    header 0.75rem/1rem, body 1rem/1.25rem, footer 0.75rem/1rem 
    for mobile/desktop respectively
    """
    card = render_standard_card(tournament, viewport_width)
    
    if viewport_width < 768:
        assert card.header_padding == '0.75rem'
        assert card.body_padding == '1rem'
        assert card.footer_padding == '0.75rem'
    else:
        assert card.header_padding == '1rem'
        assert card.body_padding == '1.25rem'
        assert card.footer_padding == '1rem'

# Feature: fix-tournament-cards-responsive, Property 8: Title text truncation
@given(
    title=st.text(min_size=100, max_size=500),
    viewport_width=st.integers(min_value=320, max_value=2560)
)
@pytest.mark.property_test
def test_property_8_title_truncation(title, viewport_width):
    """
    For any Standard_Card title with text longer than 2 lines, 
    the text should truncate with ellipsis after 2 lines
    """
    tournament = create_tournament(name=title)
    card = render_standard_card(tournament, viewport_width)
    
    assert card.title_line_clamp == 2
    assert card.title_overflow == 'hidden'
    assert card.title_text_overflow == 'ellipsis'

# Feature: fix-tournament-cards-responsive, Property 10: Touch target minimum size
@given(
    viewport_width=st.integers(min_value=320, max_value=2560),
    card_type=st.sampled_from(['standard', 'compact', 'featured', 'list_item'])
)
@pytest.mark.property_test
def test_property_10_touch_target_size(viewport_width, card_type):
    """
    For any interactive button or icon in the card system, 
    the minimum touch target size should be 44x44px on all devices
    """
    card = render_card(card_type, sample_tournament, viewport_width)
    buttons = card.get_all_interactive_elements()
    
    for button in buttons:
        assert button.min_height >= 44
        assert button.min_width >= 44

# Feature: fix-tournament-cards-responsive, Property 17: Featured card image aspect ratio
@given(
    viewport_width=st.integers(min_value=320, max_value=2560),
    image_aspect_ratio=st.floats(min_value=0.5, max_value=3.0)
)
@pytest.mark.property_test
def test_property_17_image_aspect_ratio(viewport_width, image_aspect_ratio):
    """
    For any Featured_Card image, the object-fit property should be set to cover 
    to maintain aspect ratio while covering the card area
    """
    tournament = create_tournament_with_image(aspect_ratio=image_aspect_ratio)
    card = render_featured_card(tournament, viewport_width)
    
    assert card.image_object_fit == 'cover'
    assert card.image_width == '100%'
    assert card.image_height == '100%'

# Feature: fix-tournament-cards-responsive, Property 29: Orientation compatibility
@given(
    viewport_width=st.integers(min_value=320, max_value=2560),
    viewport_height=st.integers(min_value=320, max_value=2560),
    card_type=st.sampled_from(['standard', 'compact', 'featured', 'list_item'])
)
@pytest.mark.property_test
def test_property_29_orientation_compatibility(viewport_width, viewport_height, card_type):
    """
    For any card component, the layout and functionality should remain correct 
    in both portrait and landscape orientations
    """
    # Portrait
    card_portrait = render_card(card_type, sample_tournament, viewport_width, viewport_height)
    assert card_portrait.is_valid_layout()
    
    # Landscape (swap dimensions)
    card_landscape = render_card(card_type, sample_tournament, viewport_height, viewport_width)
    assert card_landscape.is_valid_layout()
```

### Visual Regression Testing

Для проверки визуального отображения на различных устройствах будем использовать:

1. **Playwright** или **Puppeteer** для автоматизированного тестирования
2. **Percy** или **Chromatic** для visual regression testing
3. **BrowserStack** для тестирования на реальных устройствах

```python
# Visual regression test example
@pytest.mark.visual
def test_visual_standard_card_on_devices():
    """Test visual appearance of standard card on target devices"""
    devices = [
        ('iPhone SE', 375, 667),
        ('iPhone 12', 390, 844),
        ('Samsung Galaxy S21', 360, 800),
        ('iPad Mini', 768, 1024),
        ('iPad Air', 820, 1180),
        ('Desktop', 1920, 1080)
    ]
    
    for device_name, width, height in devices:
        page = setup_browser(width, height)
        page.goto('/tournaments')
        screenshot = page.screenshot()
        assert_visual_match(screenshot, f'standard_card_{device_name}')
```

### Testing Tools

- **Pytest**: Основной фреймворк для тестирования
- **Hypothesis**: Property-based testing
- **Playwright**: Browser automation
- **pytest-html**: Генерация HTML отчетов
- **coverage.py**: Измерение покрытия кода

### Test Execution

```bash
# Запуск всех тестов
pytest tests/

# Запуск только property тестов
pytest -m property_test tests/

# Запуск visual regression тестов
pytest -m visual tests/

# Запуск с покрытием
pytest --cov=static/css --cov=templates/components tests/

# Генерация HTML отчета
pytest --html=report.html tests/
```

## Implementation Notes

### File Structure

```
static/css/
├── tournament-cards-enhanced.css (существующий)
└── tournament-cards-responsive.css (новый)

templates/components/
└── tournament_cards.html (обновление макросов)
```

### CSS Loading Order

```html
<!-- В base_modern.html -->
<link rel="stylesheet" href="/static/css/tournament-cards-enhanced.css">
<link rel="stylesheet" href="/static/css/tournament-cards-responsive.css">
```

### Browser Support

- Chrome 90+
- Firefox 88+
- Safari 14+
- Edge 90+
- Samsung Internet 14+
- iOS Safari 14+
- Chrome Android 90+

### Performance Considerations

1. **CSS минификация**: Использовать минифицированные версии в production
2. **Critical CSS**: Инлайнить критические стили для первого рендера
3. **Lazy loading**: Отложенная загрузка изображений в featured cards
4. **GPU acceleration**: Использовать transform и opacity для анимаций
5. **Debounce resize**: Ограничить частоту обработки resize событий

### Accessibility

1. **ARIA labels**: Добавить aria-label для иконок без текста
2. **Focus indicators**: Обеспечить видимые focus states для всех интерактивных элементов
3. **Keyboard navigation**: Все действия доступны с клавиатуры
4. **Screen reader support**: Семантический HTML и ARIA атрибуты
5. **Color contrast**: Минимум 4.5:1 для обычного текста, 3:1 для крупного

### Migration Strategy

1. **Phase 1**: Создать новый CSS файл с адаптивными стилями
2. **Phase 2**: Обновить макросы в tournament_cards.html
3. **Phase 3**: Тестирование на всех целевых устройствах
4. **Phase 4**: Постепенный rollout с feature flag
5. **Phase 5**: Мониторинг метрик и обратной связи пользователей

## References

- [Bootstrap 5 Breakpoints](https://getbootstrap.com/docs/5.3/layout/breakpoints/)
- [MDN: Responsive Design](https://developer.mozilla.org/en-US/docs/Learn/CSS/CSS_layout/Responsive_Design)
- [Web Content Accessibility Guidelines (WCAG) 2.1](https://www.w3.org/WAI/WCAG21/quickref/)
- [Google Web Fundamentals: Responsive Web Design](https://developers.google.com/web/fundamentals/design-and-ux/responsive)
- [CSS Tricks: A Complete Guide to Flexbox](https://css-tricks.com/snippets/css/a-guide-to-flexbox/)
