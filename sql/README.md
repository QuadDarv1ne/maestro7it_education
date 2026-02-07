# SQL

Комплексный учебный ресурс по SQL с реальными базами данных и практическими примерами для анализа данных и бизнес-аналитики.

## 📚 Примеры баз данных

### 1. [Chinook](https://sqliteonline.com/#urldb=https://raw.githubusercontent.com/lerocha/chinook-database/master/ChinookDatabase/DataSources/Chinook_Sqlite.sqlite)
**База данных музыкального магазина**
- Исполнители, альбомы, треки
- Клиенты, счета
- Анализ жанров
- Отчеты по продажам

📁 `src/chinook/` - SQL queries and examples
📁 `data/sample_data/` - Sample CSV data

### 2. [NorthWind](https://sqliteonline.com/#urldb=https://raw.githubusercontent.com/jpwhite3/northwind-SQLite3/master/dist/northwind.db)
**База данных бизнеса/торговли**
- Поставщики, продукты, категории
- Клиенты, заказы
- Управление запасами
- Аналитика продаж

📁 `src/northwind/` - SQL queries and examples
📁 `data/sample_data/` - Sample CSV data

### 3. [CNF](https://sqliteonline.com/#urldb=https://raw.githubusercontent.com/ladieslearningcode/llc-sql/master/data/cnf.db)
**База данных Canadian National Railway**
- Маршруты, станции, расписания
- Транспортная логистика
- Оптимизация маршрутов
- Метрики производительности

📁 `src/cnf/` - SQL queries and examples

### 4. [BasketBall](https://sqliteonline.com/#urldb=https://raw.githubusercontent.com/wyattowalsh/sports-analytics/main/basketball/data/basketball.sqlite)
**База данных спортивной аналитики**
- Команды, игроки, игры
- Статистика игроков
- Производительность команд
- Анализ сезона

📁 `src/basketball/` - SQL queries and examples
📁 `data/sample_data/` - Sample CSV data

### 5. [Sakila](https://sqliteonline.com/#urldb=https://raw.githubusercontent.com/ivanceras/sakila/master/sqlite-sakila-db/sakila.db)
**База данных DVD-проката**
- Фильмы, актеры, категории
- Клиенты, аренды
- Отслеживание инвентаря
- Анализ доходов

📁 `src/sakila/` - SQL queries and examples

## 📁 Структура проекта

```
sql/
├── src/                    # SQL query files
│   ├── chinook/           # Music store queries
│   ├── northwind/         # Business queries
│   ├── cnf/               # Railway queries
│   ├── basketball/        # Sports queries
│   └── sakila/            # DVD rental queries
├── data/                  # Data files
│   ├── sample_data/       # CSV files for practice
│   ├── databases/         # Downloaded SQLite databases
│   └── test_data/         # Test datasets and frameworks
├── scripts/               # Automation scripts
│   ├── download_databases.py  # Database downloader
│   └── sql_tester.py      # SQL query tester
├── notebooks/             # Jupyter notebooks
│   ├── chinook_interactive.ipynb
│   └── northwind_interactive.ipynb
├── templates/             # Project templates
│   ├── retail_analysis_template.sql
│   ├── sports_analytics_template.sql
│   └── music_analytics_template.sql
├── solutions/             # Exercise solutions
│   ├── chinook_solutions.sql
│   ├── northwind_solutions.sql
│   └── basketball_solutions.sql
├── docs/                  # Documentation
├── basketball/            # Basketball resources
├── img/                   # Images
├── .gitignore            # Git ignore rules
├── LICENSE               # MIT License
├── CONTRIBUTING.md       # Contribution guidelines
└── README.md             # This file
```

## 🚀 Начало работы

### Быстрый старт:

1. **Загрузите базы данных**:
   ```bash
   python scripts/download_databases.py
   ```

2. **Изучите структуру**:
   ```sql
   SELECT name FROM sqlite_master WHERE type = 'table';
   ```

3. **Запустите интерактивные notebook'ы**:
   - `notebooks/chinook_interactive.ipynb`
   - `notebooks/northwind_interactive.ipynb`

4. **Практикуйтесь с тестовыми данными**:
   - `data/test_data/test_dataset.sql`
   - `data/test_data/testing_framework.md`

### Альтернативные способы:

- **Используйте онлайн SQLite** с предоставленными ссылками
- **Запустите SQL-тестер** для проверки запросов:
  ```bash
  python scripts/sql_tester.py
  ```
- **Изучите шаблоны проектов** в папке `templates/`

## 📖 Путь обучения

### Уровень новичка
- Базовые операторы SELECT
- Фильтрация с WHERE
- Сортировка с ORDER BY
- Простые агрегации

### Средний уровень
- Операции JOIN
- GROUP BY и HAVING
- Подзапросы
- Функции даты/времени

### Продвинутый уровень
- Оконные функции
- CTE (Обобщенные табличные выражения)
- Оптимизация производительности
- Сложная бизнес-аналитика

## 🛠️ Инструменты и ресурсы

- [SQLite Online](https://sqliteonline.com/) - Web-based SQLite editor
- [DB Browser for SQLite](https://sqlitebrowser.org/) - Desktop application
- [SQLite Documentation](https://www.sqlite.org/docs.html)

## 📊 Включенные образцы данных

All databases include sample CSV data for offline practice:
- Artists, Albums, Tracks (Chinook)
- Products, Orders, Customers (NorthWind)
- Teams, Players, Games (Basketball)
- And more...

## 🎯 Практические применения

- **Бизнес-аналитика**: Анализ продаж, сегментация клиентов
- **Анализ данных**: Выявление трендов, метрики производительности
- **Спортивная аналитика**: Статистика игроков, производительность команд
- **Логистика**: Оптимизация маршрутов, анализ расписаний
- **Управление запасами**: Уровни запасов, точки повторного заказа

![dupley_maxim_igorevich](img/DupleyMI.jpg)

---

💼 **Автор:** Дуплей Максим Игоревич

📲 **Telegram №1:** [@quadd4rv1n7](https://t.me/quadd4rv1n7)

📲 **Telegram №2:** [@dupley_maxim_1999](https://t.me/dupley_maxim_1999)

## 📅 История версий

**Версия 2.0** - Февраль 2026
- Добавлена структурированная организация проекта
- Созданы реальные SQL-файлы запросов для каждой базы данных
- Добавлены образцы CSV-данных для офлайн-практики
- Улучшена документация и путь обучения

**Версия 1.0** - Март 2025
- Первоначальный выпуск со ссылками на базы данных

## 📬 Contact

💼 **Author:** Дуплей Максим Игоревич

📲 **Telegram №1:** [@quadd4rv1n7](https://t.me/quadd4rv1n7)

📲 **Telegram №2:** [@dupley_maxim_1999](https://t.me/dupley_maxim_1999)

📧 **Email:** maksimqwe42@mail.ru

---

*Идеально подходит для новичков в SQL и профессионалов в области анализа данных!*
