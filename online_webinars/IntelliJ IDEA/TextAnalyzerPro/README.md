# TextAnalyzerPro

Профессиональный анализатор текста на Java с поддержкой Unicode и блочным чтением.

## Возможности

- **Универсальный сканер** с блочным чтением и поддержкой Unicode
- **Статистика слов** с сохранением порядка и позиций
- **Обработка чисел** с различными статистическими функциями
- **Задача "Реверс"** для матриц чисел
- **Задача "Статистика слов++"** с полной информацией о словах
- **Поддержка различных кодировок** (UTF-8 по умолчанию)
- **Современное логирование** с SLF4J и Logback
- **Unit тестирование** с JUnit 5
- **Анализ покрытия кода** с JaCoCo
- **Контейнеризация** с Docker

## Требования

- Java 11 или выше
- Maven 3.6 или выше (для сборки)
- Docker (опционально, для контейнеризации)

## Сборка и запуск

### Сборка проекта

```bash
mvn clean compile
```

### Создание JAR-файла

```bash
mvn package
```

### Запуск приложения

```bash
mvn exec:java
```

Или с аргументами:

```bash
mvn exec:java -Dexec.args="reverse input.txt output.txt"
```

### Запуск тестов

```bash
mvn test
```

### Генерация отчета о покрытии кода

```bash
mvn test jacoco:report
```

Отчет будет доступен в `target/site/jacoco/index.html`

## Docker

### Сборка Docker образа

```bash
mvn package
docker build -t textanalyzerpro .
```

### Запуск в контейнере

```bash
docker run -v $(pwd)/input:/app/input -v $(pwd)/output:/app/output textanalyzerpro reverse input/reverse.txt output/result.txt
```

## Структура проекта

```
TextAnalyzerPro/
├── src/
│   ├── main/java/
│   │   ├── analyzer/
│   │   │   ├── scanner/
│   │   │   │   ├── TextScanner.java      # Основной класс сканера
│   │   │   │   ├── TokenType.java        # Типы токенов
│   │   │   │   └── Token.java            # Класс токена
│   │   │   ├── statistics/
│   │   │   │   ├── WordStatistics.java   # Статистика слов
│   │   │   │   ├── NumberStatistics.java # Статистика чисел
│   │   │   │   └── TextStatistics.java   # Общая статистика
│   │   │   └── utils/
│   │   │       ├── IntList.java          # Список целых чисел
│   │   │       ├── FileUtils.java        # Утилиты для работы с файлами
│   │   │       ├── Logger.java           # Логгер
│   │   │       └── StringUtils.java      # Утилиты для строк
│   │   ├── tasks/
│   │   │   ├── ReverseTask.java          # Задача "Реверс"
│   │   │   ├── WordStatTask.java         # Задача "Статистика слов"
│   │   │   ├── WordStatPlusTask.java     # Задача "Статистика слов++"
│   │   │   ├── TextStatTask.java         # Задача "Статистика текста"
│   │   │   ├── TopWordsTask.java         # Задача "Топ слов"
│   │   │   └── WordLengthTask.java       # Задача "Длина слов"
│   │   ├── AppConfig.java                # Конфигурация приложения
│   │   └── MyScanner.java                # Пользовательский сканер
│   │   └── Main.java                     # Главный класс
│   └── test/java/
│       └── TestRunner.java               # Тестовый запускатор
├── test/
│   ├── input/
│   │   ├── reverse.txt
│   │   ├── words.txt
│   │   └── words_plus.txt
│   ├── expected/
│   │   ├── reverse_output.txt
│   │   ├── words_output.txt
│   │   └── words_plus_output.txt
│   └── actual/                           # Создается автоматически
├── scripts/
│   ├── build.bat                         # Скрипт сборки
│   ├── run.bat                           # Скрипт запуска
│   └── test.bat                          # Скрипт тестирования
├── pom.xml                               # Maven конфигурация
├── .gitignore                            # Игнорируемые файлы
├── LICENSE
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
