# Implementation Plan: Fix Tournament Cards Responsive

## Overview

Данный план описывает пошаговую реализацию исправлений адаптивности карточек турниров. Реализация следует принципу Mobile-First и включает создание нового CSS файла с адаптивными стилями, обновление Jinja2 макросов и комплексное тестирование на различных устройствах.

## Tasks

- [x] 1. Создать базовую структуру адаптивного CSS файла
  - Создать файл `static/css/tournament-cards-responsive.css`
  - Добавить CSS custom properties для breakpoints
  - Добавить базовые mobile-first стили для всех типов карточек
  - Подключить новый CSS файл в `templates/base_modern.html` после `tournament-cards-enhanced.css`
  - _Requirements: 1.1, 1.2, 2.1, 2.2, 2.3, 3.1, 3.3, 3.5_

- [ ] 2. Реализовать адаптивные стили для Standard Card
  - [x] 2.1 Добавить адаптивные стили для заголовка карточки
    - Реализовать mobile стили: padding 0.75rem, flex-direction column, gap 0.5rem
    - Реализовать desktop стили (>= 768px): padding 1rem, flex-direction row, space-between
    - Добавить адаптивную типографику для title и subtitle
    - _Requirements: 2.1, 2.4, 3.1, 3.2, 3.3, 3.4, 4.1, 4.2, 4.3, 4.4, 4.5_
  
  - [ ]* 2.2 Написать property тест для заголовка карточки
    - **Property 7: Header layout responsiveness**
    - **Validates: Requirements 4.1, 4.2, 4.3, 4.4, 4.5**
  
  - [x] 2.3 Добавить адаптивные стили для тела карточки
    - Реализовать mobile стили: padding 1rem, gap 0.75rem
    - Реализовать desktop стили (>= 768px): padding 1.25rem, gap 1rem
    - Добавить адаптивные стили для meta items (column на mobile, row на desktop)
    - _Requirements: 2.2, 2.5, 3.5, 3.6, 9.1, 9.2, 9.3, 9.4, 9.5_
  
  - [ ]* 2.4 Написать property тест для тела карточки
    - **Property 3: Standard card padding responsiveness**
    - **Validates: Requirements 2.1, 2.2, 2.3, 2.4, 2.5, 2.6**
  
  - [x] 2.5 Добавить адаптивные стили для футера карточки
    - Реализовать mobile стили: padding 0.75rem, flex-direction column, 100% width buttons
    - Реализовать desktop стили (>= 768px): padding 1rem, flex-direction row, auto width buttons
    - Обеспечить минимальный размер touch target 44x44px для всех кнопок
    - _Requirements: 2.3, 2.6, 5.1, 5.2, 5.3, 5.4, 5.5, 5.6_
  
  - [ ]* 2.6 Написать property тест для футера карточки
    - **Property 9: Footer actions layout responsiveness**
    - **Validates: Requirements 5.1, 5.2, 5.3, 5.4**
  
  - [x] 2.7 Добавить адаптивные стили для border-radius и tags
    - Реализовать mobile border-radius: 0.5rem
    - Реализовать desktop border-radius (>= 768px): 0.75rem
    - Добавить адаптивные стили для tags (font-size, padding, wrapping)
    - _Requirements: 2.7, 2.8, 11.1, 11.2, 11.3, 11.4, 11.5, 11.6_
  
  - [ ]* 2.8 Написать property тест для border-radius
    - **Property 4: Standard card border-radius responsiveness**
    - **Validates: Requirements 2.7, 2.8**

- [ ] 3. Checkpoint - Проверить Standard Card на разных устройствах
  - Убедиться, что все стили Standard Card корректно применяются
  - Проверить на iPhone SE (375px), iPad (768px), Desktop (1920px)
  - Задать вопросы пользователю, если возникли проблемы

- [ ] 4. Реализовать адаптивные стили для Compact Card
  - [ ] 4.1 Добавить адаптивную структуру Compact Card
    - Реализовать mobile стили: flex-direction column, 100% width date block
    - Реализовать desktop стили (>= 576px): flex-direction row, 80px width date block
    - Изменить border с bottom на right при переходе на desktop
    - _Requirements: 6.1, 6.2, 6.3, 6.4, 6.5_
  
  - [ ]* 4.2 Написать property тест для Compact Card layout
    - **Property 11: Compact card layout responsiveness**
    - **Validates: Requirements 6.1, 6.2, 6.3, 6.4**
  
  - [ ] 4.3 Добавить адаптивные стили для контента Compact Card
    - Реализовать mobile padding: 1rem
    - Реализовать desktop padding (>= 576px): 0.75rem
    - Добавить адаптивную типографику для title и meta
    - _Requirements: 6.6, 6.7_
  
  - [ ]* 4.4 Написать property тест для Compact Card padding
    - **Property 13: Compact card content padding**
    - **Validates: Requirements 6.6, 6.7**

- [ ] 5. Реализовать адаптивные стили для Featured Card
  - [ ] 5.1 Добавить адаптивные размеры Featured Card
    - Реализовать mobile min-height: 300px
    - Реализовать desktop min-height (>= 768px): 400px
    - Обеспечить object-fit: cover для изображений
    - _Requirements: 7.1, 7.2, 7.7, 13.4_
  
  - [ ]* 5.2 Написать property тест для Featured Card height
    - **Property 14: Featured card height responsiveness**
    - **Validates: Requirements 7.1, 7.2**
  
  - [ ] 5.3 Добавить адаптивные стили для overlay Featured Card
    - Реализовать mobile padding: 1rem
    - Реализовать desktop padding (>= 768px): 1.5rem
    - Добавить адаптивную типографику для title
    - _Requirements: 7.3, 7.4, 7.5, 7.6_
  
  - [ ]* 5.4 Написать property тест для Featured Card overlay
    - **Property 15: Featured card overlay padding**
    - **Validates: Requirements 7.3, 7.4**
  
  - [x] 5.5 Добавить обработку ошибок загрузки изображений
    - Реализовать JavaScript fallback для failed images
    - Использовать default-tournament.jpg как fallback
    - _Requirements: 13.5_
  
  - [ ]* 5.6 Написать unit тест для image fallback
    - Проверить, что при ошибке загрузки используется fallback изображение
    - _Requirements: 13.5_

- [ ] 6. Реализовать адаптивные стили для List Item Card
  - [ ] 6.1 Добавить адаптивную структуру List Item Card
    - Реализовать mobile стили: flex-direction column, 100% width actions
    - Реализовать desktop стили (>= 768px): flex-direction row, auto width actions
    - Добавить flex-wrap для meta items на mobile
    - _Requirements: 8.1, 8.2, 8.3, 8.4, 8.5, 8.6_
  
  - [ ]* 6.2 Написать property тест для List Item Card layout
    - **Property 18: List item card layout responsiveness**
    - **Validates: Requirements 8.1, 8.2**
  
  - [ ] 6.3 Добавить адаптивные стили для padding List Item Card
    - Реализовать mobile padding: 0.75rem
    - Реализовать desktop padding (>= 768px): 1rem
    - _Requirements: 8.7_
  
  - [ ]* 6.4 Написать property тест для List Item Card padding
    - **Property 20: List item card padding**
    - **Validates: Requirements 8.7**

- [ ] 7. Checkpoint - Проверить все типы карточек
  - Убедиться, что все 4 типа карточек корректно отображаются
  - Проверить на мобильных (< 576px), планшетах (768px), десктопах (>= 992px)
  - Задать вопросы пользователю, если возникли проблемы

- [ ] 8. Реализовать адаптивную сетку и hover эффекты
  - [x] 8.1 Обновить tournament_grid макрос
    - Обновить Bootstrap классы: col-12, col-md-6, col-lg-4
    - Использовать g-3 для mobile и g-4 для desktop gap
    - _Requirements: 1.1, 1.2, 1.3, 1.4, 1.5, 1.6, 14.1, 14.2, 14.3, 14.4, 14.5, 14.6_
  
  - [ ]* 8.2 Написать property тест для grid layout
    - **Property 1: Responsive grid column layout**
    - **Validates: Requirements 1.1, 1.2, 1.3, 1.4, 1.5**
  
  - [ ] 8.3 Добавить адаптивные hover эффекты
    - Использовать @media (hover: hover) and (pointer: fine) для desktop hover
    - Отключить transform hover на touch устройствах
    - Показывать quick action buttons по умолчанию на mobile
    - _Requirements: 10.1, 10.2, 10.3, 10.4, 10.5_
  
  - [ ]* 8.4 Написать unit тесты для hover behavior
    - Проверить hover эффекты на desktop
    - Проверить отсутствие hover на mobile
    - _Requirements: 10.1, 10.2, 10.3, 10.4, 10.5_

- [ ] 9. Реализовать оптимизации производительности для mobile
  - [ ] 9.1 Добавить оптимизации анимаций
    - Отключить 3D transforms на mobile
    - Использовать упрощенные анимации с shorter duration
    - Добавить will-change только во время активных анимаций
    - _Requirements: 12.1, 12.2, 12.4_
  
  - [x] 9.2 Добавить feature detection для backdrop-filter
    - Проверить поддержку backdrop-filter
    - Использовать fallback для неподдерживаемых браузеров
    - _Requirements: 12.3_
  
  - [x] 9.3 Добавить viewport detection и resize handling
    - Реализовать getCurrentBreakpoint() функцию
    - Добавить debounced resize handler
    - Добавить data-breakpoint атрибут к body
    - _Requirements: 1.1, 1.2, 1.3, 1.4, 1.5_
  
  - [x] 9.4 Добавить touch device detection
    - Определить touch устройства
    - Добавить touch-device или no-touch класс к body
    - _Requirements: 10.3, 10.4_

- [ ] 10. Реализовать accessibility улучшения
  - [ ] 10.1 Обеспечить минимальные touch targets
    - Проверить все кнопки и иконки на min-height/width 44px
    - Проверить tags на min-height 32px на mobile
    - _Requirements: 5.5, 5.6, 11.6_
  
  - [ ]* 10.2 Написать property тест для touch targets
    - **Property 10: Touch target minimum size**
    - **Validates: Requirements 5.5, 5.6**
  
  - [ ] 10.3 Добавить ARIA labels и focus indicators
    - Добавить aria-label для иконок без текста
    - Обеспечить видимые focus states для всех интерактивных элементов
    - _Requirements: Accessibility best practices_
  
  - [ ] 10.4 Обеспечить минимальный font-size для inputs
    - Проверить, что все input элементы имеют font-size >= 16px
    - _Requirements: 3.7_
  
  - [ ]* 10.5 Написать property тест для input font-size
    - **Property 6: Input font-size minimum for iOS**
    - **Validates: Requirements 3.7**

- [ ] 11. Реализовать text truncation и wrapping
  - [ ] 11.1 Добавить truncation для titles
    - Реализовать line-clamp: 2 для Standard_Card title
    - Добавить overflow: hidden и text-overflow: ellipsis
    - _Requirements: 4.6_
  
  - [ ]* 11.2 Написать property тест для title truncation
    - **Property 8: Title text truncation**
    - **Validates: Requirements 4.6**
  
  - [ ] 11.3 Добавить truncation для meta items
    - Реализовать text-overflow: ellipsis для длинных meta items
    - _Requirements: 9.6_
  
  - [ ]* 11.4 Написать property тест для meta truncation
    - **Property 24: Meta items text truncation**
    - **Validates: Requirements 9.6**

- [ ] 12. Checkpoint - Комплексное тестирование
  - Убедиться, что все property тесты проходят
  - Проверить все unit тесты
  - Задать вопросы пользователю, если возникли проблемы

- [ ] 13. Провести visual regression тестирование
  - [ ] 13.1 Настроить Playwright для visual testing
    - Установить Playwright
    - Создать конфигурацию для целевых устройств
    - _Requirements: 15.1, 15.2, 15.3, 15.4, 15.5, 15.6_
  
  - [ ]* 13.2 Написать visual regression тесты для всех устройств
    - Создать тесты для iPhone SE (375x667)
    - Создать тесты для iPhone 12/13 (390x844)
    - Создать тесты для Samsung Galaxy S21 (360x800)
    - Создать тесты для iPad Mini (768x1024)
    - Создать тесты для iPad Air (820x1180)
    - Создать тесты для Desktop (1920x1080)
    - _Requirements: 15.1, 15.2, 15.3, 15.4, 15.5, 15.6_
  
  - [ ]* 13.3 Написать тесты для orientation compatibility
    - **Property 29: Orientation compatibility**
    - **Validates: Requirements 15.7**

- [ ] 14. Провести тестирование на реальных устройствах
  - [ ]* 14.1 Тестирование на iPhone
    - Проверить на iPhone SE, iPhone 12/13
    - Проверить в portrait и landscape
    - _Requirements: 15.1, 15.2, 15.7_
  
  - [ ]* 14.2 Тестирование на Android
    - Проверить на Samsung Galaxy S21
    - Проверить в portrait и landscape
    - _Requirements: 15.3, 15.7_
  
  - [ ]* 14.3 Тестирование на iPad
    - Проверить на iPad Mini, iPad Air
    - Проверить в portrait и landscape
    - _Requirements: 15.4, 15.5, 15.7_
  
  - [ ]* 14.4 Тестирование на Desktop
    - Проверить на различных разрешениях (1366x768, 1920x1080, 2560x1440)
    - Проверить в различных браузерах (Chrome, Firefox, Safari, Edge)
    - _Requirements: 15.6_

- [ ] 15. Оптимизация и финализация
  - [ ] 15.1 Минифицировать CSS
    - Создать минифицированную версию tournament-cards-responsive.css
    - Обновить ссылки в production
    - _Requirements: Performance optimization_
  
  - [ ] 15.2 Добавить CSS fallbacks
    - Добавить fallback для flexbox
    - Добавить fallback для CSS custom properties
    - Добавить fallback для object-fit
    - _Requirements: Browser compatibility_
  
  - [x] 15.3 Обновить документацию
    - Обновить RESPONSIVE_DESIGN.md с новыми стилями
    - Добавить примеры использования обновленных макросов
    - Документировать новые CSS классы и переменные
    - _Requirements: Documentation_

- [ ] 16. Final Checkpoint - Финальная проверка
  - Убедиться, что все тесты проходят (unit, property, visual)
  - Проверить производительность на мобильных устройствах
  - Проверить accessibility с помощью Lighthouse
  - Получить одобрение пользователя для deployment

## Notes

- Задачи, отмеченные `*`, являются опциональными и могут быть пропущены для быстрого MVP
- Каждая задача ссылается на конкретные требования для отслеживаемости
- Checkpoints обеспечивают инкрементальную валидацию
- Property тесты валидируют универсальные свойства корректности
- Unit тесты валидируют конкретные примеры и edge cases
- Visual regression тесты обеспечивают корректное визуальное отображение
