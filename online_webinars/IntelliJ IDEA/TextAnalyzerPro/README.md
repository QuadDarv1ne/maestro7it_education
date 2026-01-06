# TextAnalyzerPro

Профессиональный анализатор текста на Java с поддержкой Unicode и блочным чтением.

## Возможности

- **Универсальный сканер** с блочным чтением и поддержкой Unicode
- **Статистика слов** с сохранением порядка и позиций
- **Обработка чисел** с различными статистическими функциями
- **Задача "Реверс"** для матриц чисел
- **Задача "Статистика слов++"** с полной информацией о словах
- **Поддержка различных кодировок** (UTF-8 по умолчанию)

## Структура проекта

```textline
TextAnalyzerPro/
├── src/
│   ├── analyzer/
│   │   ├── scanner/
│   │   │   ├── TextScanner.java      # Основной класс сканера
│   │   │   ├── TokenType.java        # Типы токенов
│   │   │   └── Token.java            # Класс токена
│   │   ├── statistics/
│   │   │   ├── WordStatistics.java   # Статистика слов
│   │   │   ├── NumberStatistics.java # Статистика чисел
│   │   │   └── TextStatistics.java   # Общая статистика
│   │   └── utils/
│   │       ├── IntList.java          # Список целых чисел
│   │       ├── FileUtils.java        # Утилиты для работы с файлами
│   │       └── StringUtils.java      # Утилиты для строк
│   ├── tasks/
│   │   ├── ReverseTask.java          # Задача "Реверс"
│   │   ├── WordStatTask.java         # Задача "Статистика слов"
│   │   └── WordStatPlusTask.java     # Задача "Статистика слов++"
│   └── Main.java                     # Главный класс
├── test/
│   ├── input/
│   │   ├── reverse.txt
│   │   ├── words.txt
│   │   └── words_plus.txt
│   ├── expected/
│   │   ├── reverse_output.txt
│   │   ├── words_output.txt
│   │   └── words_plus_output.txt
│   └── TestRunner.java
├── lib/
├── docs/
├── build.gradle
└── README.md
```

### Компиляция и запуск

```
# Компиляция
javac -d bin -encoding UTF-8 src/analyzer/scanner/*.java \
                             src/analyzer/statistics/*.java \
                             src/analyzer/utils/*.java \
                             src/tasks/*.java \
                             src/Main.java

# Запуск задачи "Реверс"
java -cp bin Main reverse input.txt output.txt

# Запуск задачи "Статистика слов++"
java -cp bin Main wordstat input.txt output.txt

# Запуск тестов
javac -d bin -encoding UTF-8 test/TestRunner.java
java -cp bin TestRunner
```
