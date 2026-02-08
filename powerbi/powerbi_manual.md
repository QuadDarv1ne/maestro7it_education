# Полное руководство по Power BI

## Содержание

1. [Введение в Power BI](#введение-в-power-bi)
2. [Установка и настройка](#установка-и-настройка)
3. [Основные компоненты Power BI](#основные-компоненты-power-bi)
4. [Подключение к данным](#подключение-к-данным)
5. [Power Query - преобразование данных](#power-query---преобразование-данных)
6. [Моделирование данных](#моделирование-данных)
7. [Создание визуализаций](#создание-визуализаций)
8. [Язык DAX](#язык-dax)
9. [Публикация и совместная работа](#публикация-и-совместная-работа)
10. [Безопасность данных](#безопасность-данных)
11. [Продвинутые техники](#продвинутые-техники)
12. [Практические задания](#практические-задания)
13. [Шаблоны отчетов](#шаблоны-отчетов)
14. [Практические примеры](#практические-примеры)

---

## Power Query - преобразование данных

Power Query - мощный инструмент ETL (Extract, Transform, Load) для подготовки данных перед анализом.

### Основные возможности Power Query:

- Подключение к множеству источников данных
- Преобразование и очистка данных
- Объединение таблиц
- Создание пользовательских функций
- Автоматизация процессов обработки

### Интерфейс Power Query Editor:

```
┌─────────────────────────────────────────────────────┐
│  Лента запросов        │  Свойства запроса           │
│  [Запрос1]            │                             │
│  [Запрос2]            │  Шаги применения            │
│  [Запрос3]            │  1. Исходные данные         │
│                       │  2. Удалить столбцы         │
│                       │  3. Изменить тип данных     │
│                       │  4. Фильтровать строки      │
├───────────────────────┼─────────────────────────────┤
│  Область предварительного просмотра данных          │
└─────────────────────────────────────────────────────┘
```

### Основные преобразования:

#### 1. Очистка данных:

```powerquery
// Удаление дубликатов
let
    Source = Excel.CurrentWorkbook(){[Name="Table1"]}[Content],
    RemovedDuplicates = Table.Distinct(Source)
in
    RemovedDuplicates

// Замена значений
ReplacedValues = 
    Table.ReplaceValue(
        Source, 
        "N/A", 
        null, 
        Replacer.ReplaceValue,
        {"Status"}
    )

// Удаление пустых строк
FilteredRows = 
    Table.SelectRows(
        Source, 
        each [Column1] <> null
    )
```

#### 2. Преобразование типов данных:

```powerquery
// Изменение типов данных
ChangedTypes = 
    Table.TransformColumnTypes(
        Source,
        {
            {"Date", type date},
            {"Amount", type number},
            {"Quantity", Int64.Type},
            {"IsActive", type logical}
        }
    )

// Создание пользовательского типа
CustomType = 
    Table.AddColumn(
        Source, 
        "FormattedDate", 
        each Date.ToText([Date], "dd.MM.yyyy"),
        type text
    )
```

#### 3. Работа с текстом:

```powerquery
// Очистка текста
TextCleaning = 
    Table.TransformColumns(
        Source,
        {
            {"ProductName", Text.Proper},      // Капитализация
            {"Description", Text.Upper},       // Верхний регистр
            {"Code", Text.Lower},              // Нижний регистр
            {"Comments", Text.Trim}            // Удаление пробелов
        }
    )

// Извлечение подстрок
ExtractText = 
    Table.AddColumn(
        Source, 
        "Domain", 
        each Text.BeforeDelimiter([Email], "@"),
        type text
    )
```

#### 4. Работа с датами:

```powerquery
// Извлечение компонентов даты
DateComponents = 
    Table.AddColumn(
        Source,
        "Year", each Date.Year([OrderDate]), Int64.Type,
        "Month", each Date.Month([OrderDate]), Int64.Type,
        "Day", each Date.Day([OrderDate]), Int64.Type,
        "Weekday", each Date.DayOfWeek([OrderDate]), Int64.Type
    )

// Создание периода
AddPeriod = 
    Table.AddColumn(
        Source,
        "Period",
        each Date.ToText([OrderDate], "yyyy-MM"),
        type text
    )
```

#### 5. Объединение таблиц:

```powerquery
// Объединение по ключу (JOIN)
MergedTables = 
    Table.NestedJoin(
        Orders, 
        {"CustomerID"}, 
        Customers, 
        {"ID"}, 
        "CustomerData", 
        JoinKind.LeftOuter
    )

// Расширение объединенных данных
ExpandedData = 
    Table.ExpandTableColumn(
        MergedTables, 
        "CustomerData",
        {"Name", "City", "Country"},
        {"CustomerName", "CustomerCity", "CustomerCountry"}
    )

// Добавление строк (UNION)
CombinedTables = 
    Table.Combine({Table1, Table2, Table3})
```

#### 6. Группировка и агрегация:

```powerquery
// Группировка по нескольким полям
GroupedData = 
    Table.Group(
        Source,
        {"Category", "Year"},
        {
            {"TotalSales", each List.Sum([Amount]), type number},
            {"OrderCount", each Table.RowCount(_), Int64.Type},
            {"AveragePrice", each List.Average([Price]), type number},
            {"UniqueCustomers", each List.Count(List.Distinct([CustomerID])), Int64.Type}
        }
    )

// Пивотирование данных
PivotedData = 
    Table.Pivot(
        Source,
        List.Distinct(Source[Month]),
        "Month",
        "Amount",
        List.Sum
    )
```

#### 7. Условные преобразования:

```powerquery
// Условная замена значений
ConditionalReplace = 
    Table.AddColumn(
        Source,
        "StatusDescription",
        each 
            if [StatusCode] = 1 then "Активный"
            else if [StatusCode] = 2 then "Неактивный"
            else "Неизвестно",
        type text
    )

// Условное удаление строк
FilteredRows = 
    Table.SelectRows(
        Source,
        each [Amount] > 0 and [Quantity] > 0
    )
```

#### 8. Создание пользовательских функций:

```powerquery
// Функция для расчета скидки
(fAmount as number, fDiscountRate as number) as number =>
let
    DiscountAmount = fAmount * fDiscountRate,
    FinalAmount = fAmount - DiscountAmount
in
    FinalAmount

// Использование функции
AppliedDiscount = 
    Table.AddColumn(
        Source,
        "FinalPrice",
        each CalculateDiscount([OriginalPrice], [DiscountRate]),
        type number
    )
```

### Лучшие практики Power Query:

1. **Именование запросов**: Используйте понятные имена для запросов
2. **Документирование**: Добавляйте комментарии к сложным преобразованиям
3. **Модульность**: Разбивайте сложные процессы на отдельные запросы
4. **Производительность**: Используйте ранние фильтры для уменьшения объема данных
5. **Обработка ошибок**: Добавляйте проверки на null и недопустимые значения

---

## Введение в Power BI

`Power BI` - это бизнес-аналитическая платформа `Microsoft`, позволяющая создавать интерактивные отчеты и дашборды для анализа данных.

### Основные возможности:

- Подключение к более чем 100 источникам данных
- Создание интерактивных визуализаций
- Совместная работа в реальном времени
- Мобильный доступ к отчетам
- Интеграция с другими продуктами `Microsoft`

### Компоненты Power BI:

1. **Power BI Desktop** - десктопное приложение для создания отчетов
2. **Power BI Service** - облачный сервис для публикации и совместной работы
3. **Power BI Mobile** - мобильные приложения
4. **Power BI Report Builder** - создание пагинированных отчетов
5. **Power BI Gateway** - локальный шлюз для подключения к локальным данным

---

## Установка и настройка

### Установка Power BI Desktop:

1. Перейдите на сайт [powerbi.microsoft.com](https://powerbi.microsoft.com)
2. Скачайте Power BI Desktop (бесплатно)
3. Запустите установщик и следуйте инструкциям
4. После установки запустите приложение

### Системные требования:

- Windows 10 или выше
- Как минимум 4 ГБ ОЗУ (рекомендуется 8 ГБ)
- 4 ГБ свободного места на диске
- .NET Framework 4.8

---

## Основные компоненты Power BI

### Интерфейс Power BI Desktop:

```
┌─────────────────────────────────────────────────────┐
│  Лента (Ribbon)                                     │
├─────────────────────────────────────────────────────┤
│  Область отчета (Report View)                       │
│                                                     │
│  [Визуализации]    [Поля]    [Фильтры]             │
├─────────────────────────────────────────────────────┤
│  Область данных (Data View)                         │
├─────────────────────────────────────────────────────┤
│  Область модели (Model View)                        │
└─────────────────────────────────────────────────────┘
```

### Три основных представления:
1. **Report View** - создание визуализаций
2. **Data View** - просмотр и редактирование данных
3. **Model View** - управление отношениями между таблицами

---

## Подключение к данным

### Поддерживаемые источники данных:
- Excel файлы (.xlsx, .xls)
- Базы данных (SQL Server, MySQL, PostgreSQL)
- Облачные сервисы (Azure, Google Analytics, Salesforce)
- Веб-страницы и API
- Текстовые файлы (CSV, TXT)
- SharePoint, OneDrive

### Пример подключения к Excel:
1. В Power BI Desktop выберите "Получить данные" → "Excel"
2. Найдите и выберите ваш Excel файл
3. Выберите нужные листы или таблицы
4. Нажмите "Загрузить" или "Преобразовать данные"

### Использование Power Query:
Power Query - инструмент для преобразования данных перед загрузкой:

```powerquery
// Пример Power Query скрипта
let
    Source = Excel.Workbook(File.Contents("C:\data\sales.xlsx"), null, true),
    SalesSheet = Source{[Item="Sales",Kind="Sheet"]}[Data],
    PromotedHeaders = Table.PromoteHeaders(SalesSheet, [PromoteAllScalars=true]),
    ChangedType = Table.TransformColumnTypes(PromotedHeaders,{
        {"Date", type date},
        {"Amount", type number},
        {"Product", type text}
    })
in
    ChangedType
```

---

## Моделирование данных

### Создание отношений между таблицами:

```
Customers (1) ───── (Многие) Orders
    │                        │
    └──────── (Многие) ──────┘
              OrderItems
```

### Типы кардинальности:
- **Один ко многим** (1:*)
- **Многие к одному** (*:1)
- **Один к одному** (1:1)

### Создание вычисляемых столбцов:
```dax
// В Power BI Desktop → Вкладка "Моделирование"
// Новый столбец
FullName = Customers[FirstName] & " " & Customers[LastName]

// Классификация по возрасту
AgeGroup = 
SWITCH(
    TRUE(),
    Customers[Age] < 18, "Молодежь",
    Customers[Age] < 35, "Молодые взрослые",
    Customers[Age] < 50, "Взрослые",
    "Пожилые"
)
```

### Создание вычисляемых таблиц:
```dax
// Таблица с календарем
Calendar = CALENDAR(DATE(2020,1,1), DATE(2024,12,31))

// Таблица с категориями
Categories = 
UNION(
    ROW("Category", "Электроника"),
    ROW("Category", "Одежда"),
    ROW("Category", "Продукты")
)
```

---

## Создание визуализаций

### Основные типы визуализаций:

#### 1. Гистограммы и столбчатые диаграммы
```
Продажи по месяцам:
┌─────────────────┐
│     ████        │
│   ████████      │
│ ████████████    │
│─────────────────│
  Янв Фев Мар Апр
```

#### 2. Круговые диаграммы
```
Доля рынка:
    ○○○○○○○○
  ○○        ○○
 ○            ○
○   35%       ○
 ○            ○
  ○○        ○○
    ○○○○○○○○
```

#### 3. Линейные графики
```
Тренд продаж:
  │    ╱
  │   ╱ ╲
  │  ╱   ╲
  │ ╱     ╲
  │╱       ╲
  └─────────
```

#### 4. Карты
```
Географическое распределение:
┌─────────────────┐
│  ●    ●    ●    │
│    ●      ●     │
│  ●        ●     │
│    ●  ●         │
└─────────────────┘
```

### Интерактивные фильтры:

#### Срезы (Slicers):
- Горизонтальные/вертикальные
- Списки с множественным выбором
- Ползунки диапазонов
- Иерархические срезы

#### Кросс-фильтрация:
При клике на элемент в одной визуализации автоматически фильтруются другие визуализации на странице.

---

## Язык DAX (Data Analysis Expressions)

### Основные функции DAX:

#### Агрегатные функции:
```dax
Total Sales = SUM(Sales[Amount])
Average Price = AVERAGE(Products[Price])
Count of Orders = COUNT(Orders[OrderID])
Distinct Customers = DISTINCTCOUNT(Orders[CustomerID])
```

#### Логические функции:
```dax
Sales Status = 
IF(
    [Total Sales] > 10000,
    "Высокий",
    IF([Total Sales] > 5000, "Средний", "Низкий")
)

Is Active Customer = 
IF(
    ISINSCOPE(Customers[CustomerID]),
    "Да",
    "Нет"
)
```

#### Функции времени:
```dax
Year to Date Sales = 
TOTALYTD(
    SUM(Sales[Amount]),
    Calendar[Date]
)

Same Period Last Year = 
SAMEPERIODLASTYEAR(Calendar[Date])

Running Total = 
CALCULATE(
    SUM(Sales[Amount]),
    FILTER(
        ALL(Calendar),
        Calendar[Date] <= MAX(Calendar[Date])
    )
)
```

#### Функции работы с таблицами:
```dax
Top 10 Products = 
TOPN(
    10,
    Products,
    [Total Sales],
    DESC
)

Filtered Table = 
FILTER(
    Sales,
    Sales[Amount] > 1000
)

Summarized Data = 
SUMMARIZE(
    Sales,
    Products[Category],
    Products[ProductName],
    "Total Sales", SUM(Sales[Amount]),
    "Order Count", COUNT(Sales[OrderID])
)
```

### Переменные в DAX:
```dax
Sales Analysis = 
VAR CurrentSales = SUM(Sales[Amount])
VAR PreviousSales = 
    CALCULATE(
        SUM(Sales[Amount]),
        DATEADD(Calendar[Date], -1, YEAR)
    )
VAR GrowthRate = 
    DIVIDE(CurrentSales - PreviousSales, PreviousSales)
RETURN
    GrowthRate
```

---

## Публикация и совместная работа

### Публикация в Power BI Service:
1. В Power BI Desktop: Файл → Опубликовать → Опубликовать в Power BI
2. Войдите в учетную запись Microsoft
3. Выберите рабочую область
4. Нажмите "Опубликовать"

### Совместная работа:
- **Рабочие области** - централизованное хранение отчетов
- **Приложения** - пакеты отчетов для пользователей
- **Шлюзы данных** - подключение к локальным источникам
- **Роли безопасности** - контроль доступа

### Расписание обновлений:
1. В Power BI Service откройте набор данных
2. Настройки → Расписание обновлений
3. Укажите частоту и время обновления
4. Настройте учетные данные для источников данных

---

## Продвинутые техники

### Параметризация отчетов:
```dax
// Создание параметра в Power Query
Parameter = 
let
    Source = #table(type table [ParameterName = text, ParameterValue = text], 
    {
        {"StartDate", "2024-01-01"},
        {"EndDate", "2024-12-31"}
    })
in
    Source
```

### Динамическое форматирование:
```dax
Formatted Sales = 
FORMAT(
    [Total Sales],
    IF([Total Sales] > 1000000, "0,0.00,,"М", "0,0.0,"К")
)
```

### Создание пользовательских визуализаций:
1. Использование Power BI Marketplace
2. Создание собственных визуализаций на R/Python
3. Импорт визуализаций из внешних источников

### Оптимизация производительности:
- Использование агрегированных таблиц
- Создание суммарных таблиц (Summarized Tables)
- Оптимизация DAX выражений
- Использование составных индексов

---

## Практические примеры

### Пример 1: Анализ продаж
```dax
// Метрики продаж
Total Revenue = SUM(Sales[Amount])

Revenue Growth = 
DIVIDE(
    [Total Revenue] - 
    CALCULATE([Total Revenue], DATEADD(Calendar[Date], -1, YEAR)),
    CALCULATE([Total Revenue], DATEADD(Calendar[Date], -1, YEAR))
)

Orders Count = COUNTROWS(Orders)

Average Order Value = DIVIDE([Total Revenue], [Orders Count])
```

### Пример 2: Анализ клиентов
```dax
Customer Lifetime Value = 
AVERAGEX(
    Customers,
    CALCULATE([Total Revenue], ALLEXCEPT(Customers, Customers[CustomerID]))
)

New Customers = 
CALCULATE(
    DISTINCTCOUNT(Orders[CustomerID]),
    FILTER(
        Orders,
        Orders[OrderDate] = MIN(Orders[OrderDate])
    )
)

Customer Retention Rate = 
DIVIDE(
    DISTINCTCOUNT(Orders[CustomerID]),
    [Total Customers]
)
```

### Пример 3: Бюджетирование
```dax
Budget Variance = [Actual Sales] - [Budget Sales]

Variance Percentage = 
DIVIDE([Budget Variance], [Budget Sales])

Budget Status = 
IF([Variance Percentage] > 0.1, "Превышение",
   IF([Variance Percentage] < -0.1, "Недовыполнение", "В пределах нормы"))
```

---

## Полезные советы и лучшие практики

### Организация модели данных:
1. Используйте понятные имена для таблиц и столбцов
2. Создавайте иерархии для временных данных
3. Удаляйте неиспользуемые столбцы и таблицы
4. Используйте префиксы для вычисляемых столбцов и мер

### Оптимизация производительности:
1. Избегайте сложных вычислений в больших таблицах
2. Используйте переменные для повторяющихся вычислений
3. Создавайте агрегированные таблицы для часто используемых данных
4. Ограничивайте количество строк в визуализациях

### Безопасность данных:
1. Используйте Row-Level Security (RLS)
2. Настраивайте роли пользователей
3. Ограничивайте доступ к чувствительным данным
4. Регулярно обновляйте учетные данные

### Совместная работа:
1. Используйте версионный контроль
2. Документируйте изменения
3. Создавайте шаблоны для повторяющихся задач
4. Обучайте команду лучшим практикам

---

## Ресурсы для обучения

### Официальная документация:
- [Power BI Documentation](https://docs.microsoft.com/ru-ru/power-bi/)
- [DAX Reference](https://docs.microsoft.com/ru-ru/dax/)

### Сообщества и форумы:
- Power BI Community
- Stack Overflow (тег powerbi)
- Reddit (r/PowerBI)

### Онлайн-курсы:
- Microsoft Learn
- Coursera
- Udemy
- Pluralsight

---

*Это руководство будет регулярно обновляться с новыми примерами и лучшими практиками.*