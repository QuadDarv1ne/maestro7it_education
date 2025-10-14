# ♟️ chess_stockfish

**Образовательная шахматная игра с искусственным интеллектом Stockfish**  

Создано для школы программирования [Maestro7IT](https://school-maestro7it.ru/)  

**Автор:** Дуплей М.И. — преподаватель, DevOps-инженер, философ и музыкант

---

## 🌟 Возможности

- Графический интерфейс на **Pygame**
- Игра против **Stockfish** (уровень сложности от 0 до 20)
- Выбор стороны: **белые** или **чёрные**
- Поддержка всех правил шахмат через Stockfish (включая рокировку, взятие на проходе, мат/пат)
- Unicode-отображение фигур (без внешних изображений)
- Кроссплатформенность: Windows, macOS, Linux

---

## 🚀 Установка и запуск

### 1. Установите Stockfish

**Ubuntu/Debian:**

```bash
sudo apt install stockfish
```

**macOS (с Homebrew):**

```bash
brew install stockfish
```

**Windows:**

Скачайте stockfish.exe с [официального сайта](https://stockfishchess.org/download/) и добавьте в PATH

**Проверьте установку:**

```bash
stockfish --help
```

### 2. Установите зависимости Python

```bash
pip install -r requirements.txt
```

### 3. Запустите игру

```bash
python main.py
```

**При первом запуске вы сможете выбрать:**

- Сторону (white/black)
- Уровень сложности Stockfish (0–20)

## 📂 Структура проекта

```textline
chess_stockfish/
├── README.md
├── requirements.txt
├── main.py                     # Точка входа
├── game/
│   ├── __init__.py
│   ├── chess_game.py           # Основная логика игры
│   └── menu.py                 # Консольное меню выбора параметров
├── engine/
│   ├── __init__.py
│   └── stockfish_wrapper.py    # Обёртка для работы с Stockfish
├── ui/
│   ├── __init__.py
│   └── board_renderer.py       # Отображение доски в Pygame
└── assets/
    └── (папка зарезервирована для будущих изображений/звуков)
```
