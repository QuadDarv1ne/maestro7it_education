# Тестовые скрипты

Эта директория содержит тестовые скрипты для проверки функциональности шахматного проекта.

## Основные тесты

### [automated_test.py](file:///c:/Users/maksi/OneDrive/Documents/GitHub/maestro7it_education/python/solution_tasks/chess_stockfish/tests/automated_test.py)
Основной автоматизированный тест, проверяющий:
- Инициализацию Pygame
- Импорт всех модулей
- Работу с библиотеками Stockfish и python-chess

### [comprehensive_test.py](file:///c:/Users/maksi/OneDrive/Documents/GitHub/maestro7it_education/python/solution_tasks/chess_stockfish/tests/comprehensive_test.py)
Комплексный тест, проверяющий все аспекты игры:
- Обнаружение состояний игры (мат, пат)
- Оптимизации производительности
- 3D визуальные улучшения
- Улучшения пользовательского интерфейса

### [check_installation.py](file:///c:/Users/maksi/OneDrive/Documents/GitHub/maestro7it_education/python/solution_tasks/chess_stockfish/tests/check_installation.py)
Проверка корректности установки:
- Наличие всех зависимостей
- Доступность движка Stockfish
- Правильность путей к файлам

## Специализированные тесты

### [test_achievements.py](file:///c:/Users/maksi/OneDrive/Documents/GitHub/maestro7it_education/python/solution_tasks/chess_stockfish/tests/test_achievements.py)
Тестирование системы достижений:
- Получение достижений
- Отслеживание прогресса
- Корректность статистики

### [test_caching.py](file:///c:/Users/maksi/OneDrive/Documents/GitHub/maestro7it_education/python/solution_tasks/chess_stockfish/tests/test_caching.py)
Тестирование системы кэширования:
- Эффективность кэширования
- Сроки действия кэша
- Очистку кэша

### [test_endgame_trainer.py](file:///c:/Users/maksi/OneDrive/Documents/GitHub/maestro7it_education/python/solution_tasks/chess_stockfish/tests/test_endgame_trainer.py)
Тестирование тренажера эндшпиля:
- Корректность упражнений
- Обнаружение решений
- Отслеживание прогресса

### [test_graphics_improvements.py](file:///c:/Users/maksi/OneDrive/Documents/GitHub/maestro7it_education/python/solution_tasks/chess_stockfish/tests/test_graphics_improvements.py)
Тестирование графических улучшений:
- Улучшенную отрисовку фигур
- Визуальные эффекты
- Подсказки возможных ходов

### [test_opening_book.py](file:///c:/Users/maksi/OneDrive/Documents/GitHub/maestro7it_education/python/solution_tasks/chess_stockfish/tests/test_opening_book.py)
Тестирование дебютной книги:
- Корректность дебютных позиций
- Рекомендации ходов
- Образовательные советы

### [test_sound_manager.py](file:///c:/Users/maksi/OneDrive/Documents/GitHub/maestro7it_education/python/solution_tasks/chess_stockfish/tests/test_sound_manager.py)
Тестирование звуковой системы:
- Воспроизведение звуковых эффектов
- Фоновую музыку
- Управление громкостью

### [test_ui_enhancements.py](file:///c:/Users/maksi/OneDrive/Documents/GitHub/maestro7it_education/python/solution_tasks/chess_stockfish/tests/test_ui_enhancements.py)
Тестирование улучшений пользовательского интерфейса:
- Компоненты интерфейса
- Визуальные улучшения
- Индикаторы статуса

### [test_visual_fixes.py](file:///c:/Users/maksi/OneDrive/Documents/GitHub/maestro7it_education/python/solution_tasks/chess_stockfish/tests/test_visual_fixes.py)
Тестирование исправлений визуальных артефактов:
- Упрощенные визуальные эффекты
- Корректность отображения кругов вокруг фигур

## Запуск тестов

Для запуска любого теста, используйте команду:

```bash
python tests/[test_name].py
```

Для запуска всех тестов сразу:
```bash
python tests/automated_test.py
python tests/comprehensive_test.py
```