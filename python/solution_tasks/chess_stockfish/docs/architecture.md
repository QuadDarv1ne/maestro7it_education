# Архитектура проекта chess_stockfish

## Общая структура

```mermaid
graph TD
    A[main.py] --> B[game/]
    A --> C[engine/]
    A --> D[ui/]
    A --> E[utils/]
    
    B --> B1[chess_game.py]
    B --> B2[menu.py]
    
    C --> C1[stockfish_wrapper.py]
    
    D --> D1[board_renderer.py]
    
    E --> E1[game_stats.py]
    
    A --> F[requirements.txt]
    A --> G[README.md]
```

## Компоненты проекта

### 1. Основной модуль ([main.py](file://c:\Users\maksi\OneDrive\Documents\GitHub\maestro7it_education\python\solution_tasks\chess_stockfish\main.py))
- Точка входа в приложение
- Инициализация Pygame
- Запуск меню и игрового цикла
- Обработка ошибок и исключений

### 2. Игровая логика ([game/](file://c:\Users\maksi\OneDrive\Documents\GitHub\maestro7it_education\python\solution_tasks\chess_stockfish\game))
- [chess_game.py](file://c:\Users\maksi\OneDrive\Documents\GitHub\maestro7it_education\python\solution_tasks\chess_stockfish\game\chess_game.py) - основная логика игры
- [menu.py](file://c:\Users\maksi\OneDrive\Documents\GitHub\maestro7it_education\python\solution_tasks\chess_stockfish\game\menu.py) - консольное меню

### 3. Движок ([engine/](file://c:\Users\maksi\OneDrive\Documents\GitHub\maestro7it_education\python\solution_tasks\chess_stockfish\engine))
- [stockfish_wrapper.py](file://c:\Users\maksi\OneDrive\Documents\GitHub\maestro7it_education\python\solution_tasks\chess_stockfish\engine\stockfish_wrapper.py) - обёртка для работы с Stockfish

### 4. Интерфейс ([ui/](file://c:\Users\maksi\OneDrive\Documents\GitHub\maestro7it_education\python\solution_tasks\chess_stockfish\ui))
- [board_renderer.py](file://c:\Users\maksi\OneDrive\Documents\GitHub\maestro7it_education\python\solution_tasks\chess_stockfish\ui\board_renderer.py) - отрисовка доски и интерфейса

### 5. Утилиты ([utils/](file://c:\Users\maksi\OneDrive\Documents\GitHub\maestro7it_education\python\solution_tasks\chess_stockfish\utils))
- [game_stats.py](file://c:\Users\maksi\OneDrive\Documents\GitHub\maestro7it_education\python\solution_tasks\chess_stockfish\utils\game_stats.py) - статистика игр

## Поток данных

```mermaid
sequenceDiagram
    participant User
    participant Main
    participant Game
    participant Engine
    participant UI
    
    User->>Main: Запуск приложения
    Main->>Main: Проверка зависимостей
    Main->>Game: Создание игры
    Game->>Engine: Инициализация Stockfish
    Engine-->>Game: Готовность
    Game->>UI: Инициализация Pygame
    UI-->>Game: Готовность
    Game->>User: Показ меню
    User->>Game: Выбор параметров
    Game->>Game: Запуск игрового цикла
    loop Игровой цикл
        Game->>UI: Отрисовка доски
        User->>Game: Ход игрока
        Game->>Engine: Проверка хода
        Engine-->>Game: Результат
        Game->>Engine: Ход ИИ
        Engine-->>Game: Лучший ход
        Game->>UI: Обновление доски
    end
```

## Зависимости

### Python библиотеки
- `pygame` - графический интерфейс
- `stockfish` - Python обёртка для Stockfish
- `python-chess` - работа с шахматными позициями

### Внешние зависимости
- `Stockfish` - шахматный движок (исполняемый файл)

## Обработка ошибок

Проект включает несколько уровней обработки ошибок:

1. **Проверка зависимостей** - на старте приложения
2. **Обработка исключений Stockfish** - в обёртке движка
3. **Графические ошибки** - в модуле отрисовки
4. **Ошибки ввода** - в меню и игровой логике

## Режимы работы

1. **Полнофункциональный режим** - с установленным Stockfish
2. **Ограниченный режим** - без Stockfish (только для демонстрации)