# Дополнительные материалы по Power BI

## Безопасность данных

### Row-Level Security (RLS):

RLS позволяет ограничить доступ к данным на уровне строк для разных пользователей.

#### Создание ролей:
```dax
// Роль "Менеджеры по продажам"
[SalesPersonID] = USERPRINCIPALNAME()

// Роль "Региональные менеджеры"
[Region] IN {
    "Москва",
    "Санкт-Петербург", 
    "Новосибирск"
}

// Роль "Аналитики"
[Department] = "Analytics" && 
[YEAR] >= YEAR(TODAY()) - 2
```

#### Настройка RLS в Power BI Desktop:
1. Вкладка "Моделирование" → "Управление ролями"
2. Создайте новую роль
3. Добавьте фильтры для таблиц
4. Тестирование ролей в режиме разработки

#### Динамическая безопасность:
```dax
// Динамическая фильтрация по пользователю
UserAccess = 
VAR CurrentUser = USERPRINCIPALNAME()
VAR UserTable = 
    FILTER(
        Users,
        Users[Email] = CurrentUser
    )
RETURN
    IF(
        ISINSCOPE(Users[UserID]),
        SELECTEDVALUE(Users[AllowedRegions]),
        "Все регионы"
    )
```

### Column-Level Security:

Ограничение доступа к отдельным столбцам:

```dax
// Скрытие конфиденциальных данных
SensitiveData = 
IF(
    [UserType] = "Admin",
    [Salary],
    BLANK()
)
```

### Настройка в Power BI Service:

1. **Рабочие области**: Настройка ролей для рабочих областей
2. **Приложения**: Управление доступом к опубликованным приложениям
3. **Шлюзы данных**: Настройка безопасности для локальных источников
4. **Аудит**: Мониторинг доступа и использования данных

### Шифрование данных:

- **На уровне хранения**: Шифрование в Power BI Service
- **На уровне передачи**: HTTPS/TLS для всех соединений
- **На уровне приложения**: Защита учетных данных

---

## Практические задания

### Задание 1: Анализ продаж

**Цель**: Создать отчет по анализу продаж компании

**Исходные данные**:
- Файл sales_data.xlsx с таблицами: Sales, Products, Customers, Calendar

**Задачи**:
1. Подключить данные через Power Query
2. Очистить и преобразовать данные
3. Создать модель данных с правильными отношениями
4. Рассчитать ключевые метрики:
   - Общий объем продаж
   - Количество заказов
   - Средний чек
   - Рост продаж по сравнению с прошлым периодом
5. Создать визуализации:
   - Гистограмма продаж по месяцам
   - Круговая диаграмма по категориям продуктов
   - Топ-10 клиентов
   - Географическое распределение продаж

**DAX формулы**:
```dax
Total Sales = SUM(Sales[Amount])

Sales Growth = 
DIVIDE(
    [Total Sales] - 
    CALCULATE([Total Sales], SAMEPERIODLASTYEAR(Calendar[Date])),
    CALCULATE([Total Sales], SAMEPERIODLASTYEAR(Calendar[Date]))
)

Orders Count = COUNTROWS(Orders)

Average Order Value = DIVIDE([Total Sales], [Orders Count])
```

### Задание 2: Финансовый анализ

**Цель**: Создать дашборд для финансового анализа

**Исходные данные**:
- База данных с таблицами: Transactions, Accounts, Budget

**Задачи**:
1. Подключиться к базе данных SQL Server
2. Создать вычисляемые таблицы для календаря и категорий
3. Реализовать бюджетирование:
   - Фактические vs Плановые показатели
   - Отклонения от бюджета
   - Прогнозирование на следующий период
4. Добавить интерактивные фильтры
5. Настроить автоматическое обновление данных

**Продвинутые DAX формулы**:
```dax
Budget Variance = [Actual Amount] - [Budget Amount]

Variance % = DIVIDE([Budget Variance], [Budget Amount])

Running Total = 
CALCULATE(
    SUM(Transactions[Amount]),
    FILTER(
        ALL(Calendar),
        Calendar[Date] <= MAX(Calendar[Date])
    )
)

Forecast = 
CALCULATE(
    AVERAGE(Transactions[Amount]),
    DATESINPERIOD(
        Calendar[Date],
        LASTDATE(Calendar[Date]),
        -3,
        MONTH
    )
) * COUNTROWS(VALUES(Calendar[Month]))
```

### Задание 3: HR-аналитика

**Цель**: Анализ кадровых метрик

**Исходные данные**:
- CSV файлы с данными о сотрудниках

**Задачи**:
1. Объединить несколько источников данных
2. Создать иерархию организационной структуры
3. Рассчитать метрики:
   - Текучесть кадров
   - Средняя продолжительность работы
   - Распределение по отделам
   - Анализ компенсаций
4. Реализовать параметрические фильтры
5. Настроить оповещения о критических значениях

### Задание 4: Маркетинговая аналитика

**Цель**: Анализ эффективности маркетинговых кампаний

**Исходные данные**:
- Данные из Google Analytics
- Данные из CRM системы
- Данные о рекламных расходах

**Задачи**:
1. Настроить подключение к API Google Analytics
2. Интегрировать данные из разных источников
3. Рассчитать ROI маркетинговых кампаний
4. Создать воронку конверсий
5. Реализовать когортный анализ

**Когортный анализ DAX**:
```dax
Cohort = 
VAR FirstPurchase = 
    CALCULATE(
        MIN(Orders[OrderDate]),
        ALLEXCEPT(Customers, Customers[CustomerID])
    )
RETURN
    FORMAT(FirstPurchase, "YYYY-MM")

Retention Rate = 
DIVIDE(
    DISTINCTCOUNT(Orders[CustomerID]),
    CALCULATE(
        DISTINCTCOUNT(Orders[CustomerID]),
        FILTER(
            ALL(Calendar),
            Calendar[Date] = 
                CALCULATE(MIN(Calendar[Date]), ALLEXCEPT(Customers, Customers[CustomerID]))
        )
    )
)
```

### Задание 5: Логистика и цепочки поставок

**Цель**: Оптимизация логистических процессов

**Исходные данные**:
- Данные о поставках
- Данные о складских запасах
- Данные о доставке

**Задачи**:
1. Создать модель для анализа цепочек поставок
2. Рассчитать ключевые метрики:
   - Время доставки
   - Уровень запасов
   - Стоимость логистики
   - Процент успешных поставок
3. Реализовать прогнозирование спроса
4. Создать систему ранних оповещений

---

## Шаблоны отчетов

### Шаблон 1: Ежемесячный отчет о продажах

```dax
// Основные метрики
Monthly Sales = TOTALMTD(SUM(Sales[Amount]), Calendar[Date])

MTD Growth = 
DIVIDE(
    [Monthly Sales] - 
    CALCULATE([Monthly Sales], DATEADD(Calendar[Date], -1, MONTH)),
    CALCULATE([Monthly Sales], DATEADD(Calendar[Date], -1, MONTH))
)

Active Customers MTD = 
CALCULATE(
    DISTINCTCOUNT(Orders[CustomerID]),
    DATESMTD(Calendar[Date])
)
```

### Шаблон 2: Дашборд KPI

```dax
// Финансовые KPI
Revenue = SUM(Transactions[Amount])

Costs = SUM(Expenses[Amount])

Profit = [Revenue] - [Costs]

Profit Margin = DIVIDE([Profit], [Revenue])

// Операционные KPI
Customer Satisfaction = AVERAGE(Surveys[Rating])

On-time Delivery = 
DIVIDE(
    COUNTROWS(FILTER(Deliveries, Deliveries[Status] = "On Time")),
    COUNTROWS(Deliveries)
)
```

### Шаблон 3: Аналитика интернет-магазина

```dax
// E-commerce метрики
Conversion Rate = 
DIVIDE(
    COUNTROWS(Orders),
    COUNTROWS(Visits)
)

Average Order Value = 
DIVIDE(
    SUM(Orders[Amount]),
    COUNTROWS(Orders)
)

Customer Lifetime Value = 
AVERAGEX(
    Customers,
    CALCULATE(
        SUM(Orders[Amount]),
        ALLEXCEPT(Customers, Customers[CustomerID])
    )
)

Cart Abandonment Rate = 
DIVIDE(
    COUNTROWS(Carts) - COUNTROWS(Orders),
    COUNTROWS(Carts)
)
```

### Шаблон 4: Производственный дашборд

```dax
// Производственные метрики
Production Volume = SUM(Production[Quantity])

Capacity Utilization = 
DIVIDE(
    [Production Volume],
    SUM(Production[Capacity])
)

Quality Rate = 
DIVIDE(
    COUNTROWS(FILTER(Production, Production[Defects] = 0)),
    COUNTROWS(Production)
)

Downtime = 
SUMX(
    Equipment,
    IF(Equipment[Status] = "Down", 1, 0)
)
```

### Шаблон 5: Финансовый контроль

```dax
// Бюджетный анализ
Budget Compliance = 
DIVIDE(
    SUM(Actuals[Amount]),
    SUM(Budget[Amount])
)

Variance Analysis = 
SUM(Actuals[Amount]) - SUM(Budget[Amount])

Cash Flow = 
CALCULATE(
    SUM(Transactions[Amount]),
    Transactions[Type] = "Incoming"
) - 
CALCULATE(
    SUM(Transactions[Amount]),
    Transactions[Type] = "Outgoing"
)

Working Capital = 
[Cash Flow] + 
[Accounts Receivable] - 
[Accounts Payable]
```

---

## Дополнительные ресурсы

### Полезные ссылки:
- [Официальная документация Microsoft](https://docs.microsoft.com/ru-ru/power-bi/)
- [Power BI Community](https://community.powerbi.com/)
- [YouTube каналы по Power BI](https://www.youtube.com/results?search_query=power+bi+tutorial)
- [GitHub репозитории с примерами](https://github.com/topics/powerbi)

### Рекомендуемые книги:
- "The Definitive Guide to DAX" by Marco Russo
- "Power BI MVP Book" by various authors
- "Analyzing Data with Power BI and Power Pivot for Excel" by Alberto Ferrari

### Онлайн-курсы:
- Microsoft Learn (бесплатно)
- Coursera: "Data Visualization and Communication with Tableau and Power BI"
- Udemy: "Microsoft Power BI - A Complete Introduction"
- Pluralsight: "Power BI Fundamentals"