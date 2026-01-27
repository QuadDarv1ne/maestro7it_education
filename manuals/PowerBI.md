# 📊 Power BI: Полное руководство по бизнес-аналитике и визуализации данных

## 📋 Содержание

1. [Введение в Power BI](#введение-в-power-bi)
2. [Архитектура Power BI](#архитектура-power-bi)
3. [Установка и настройка](#установка-и-настройка)
4. [Подключение к данным](#подключение-к-данным)
5. [Моделирование данных](#моделирование-данных)
6. [DAX (Data Analysis Expressions)](#dax-data-analysis-expressions)
7. [Создание визуализаций](#создание-визуализаций)
8. [Дашборды и отчеты](#дашборды-и-отчеты)
9. [Публикация и совместная работа](#публикация-и-совместная-работа)
10. [Продвинутые техники](#продвинутые-техники)
11. [Практические примеры](#практические-примеры)

## Введение в Power BI

### Что такое Power BI?

**Power BI** — это бизнес-аналитическая платформа от `Microsoft`, предназначенная для анализа данных и создания интерактивных визуализаций.

### Основные компоненты:

#### 1. Power BI Desktop
- **Описание**: Бесплатное приложение для `Windows`
- **Назначение**: Создание отчетов и моделей данных
- **Возможности**: Подключение к источникам данных, моделирование, визуализация

#### 2. Power BI Service (Power BI Online)
- **Описание**: Веб-сервис для публикации и совместной работы
- **Назначение**: Хостинг отчетов, создание дашбордов, совместная работа
- **Возможности**: Расписание обновлений, безопасность, мобильный доступ

#### 3. Power BI Mobile
- **Описание**: Мобильные приложения для `iOS`, `Android`, `Windows`
- **Назначение**: Просмотр отчетов на мобильных устройствах
- **Возможности**: Push-уведомления, offline-доступ

#### 4. Power BI Report Builder
- **Описание**: Инструмент для создания пагинированных отчетов
- **Назначение**: Создание традиционных отчетов с фиксированным форматом

### Преимущества Power BI:

✅ **Интеграция с Microsoft** (`Office 365`, `Azure`, `SQL Server`)
✅ **Широкая поддержка источников данных** (100+ коннекторов)
✅ **Интуитивный интерфейс** с drag-and-drop функционалом
✅ **Мощные аналитические возможности** через `DAX`
✅ **Совместная работа** в реальном времени
✅ **Мобильная доступность**
✅ **Конкурентоспособная цена**

---

## Архитектура Power BI

### Общая архитектура:

```
[Источники данных] → [Power BI Desktop] → [Power BI Service] → [Конечные пользователи]
       ↓                    ↓                    ↓
[Базы данных]      [Модель данных]      [Дашборды/Отчеты]
[API]              [DAX меры]           [Мобильные приложения]
[Файлы Excel]      [Визуализации]       [Embedding]
```

### Компоненты архитектуры:

#### 1. Источники данных:
- Реляционные базы данных (`SQL Server`, `Oracle`, `MySQL`)
- Облачные сервисы (`Azure`, `AWS`, `Google Cloud`)
- Файлы (`Excel`, `CSV`, `JSON`)
- Веб-сервисы и `API`
- `CRM/ERP` системы (`Salesforce`, `SAP`)

#### 2. Модель данных:
- **Факт-таблицы**: Содержат измеримые данные
- **Измерения**: Содержат описательные атрибуты
- **Связи**: Определяют отношения между таблицами

#### 3. DAX:
- Язык для создания вычисляемых столбцов
- Создание мер и `KPI`
- Расширенная аналитика

---

## Установка и настройка

### Системные требования:

**Power BI Desktop:**
- Windows 10/11 (64-bit)
- 4 GB RAM (рекомендуется 8+ GB)
- 1 GB свободного места
- .NET Framework 4.8

### Установка Power BI Desktop:

```powershell
# Скачать с официального сайта
# https://powerbi.microsoft.com/desktop/

# Или через Microsoft Store
Start-Process "ms-windows-store://pdp/?productid=9NTXR16HNW1T"
```

### Базовая настройка:

#### 1. Настройка региональных параметров:
```
File → Options and settings → Options → Current File → Regional Settings
```

#### 2. Настройка безопасности:
```
File → Options and settings → Options → Security → 
Enable/Disable data sources
```

#### 3. Настройка обновлений:
```
File → Options and settings → Options → Updates
```

---

## Подключение к данным

### Типы источников данных:

#### 1. Файлы:
```powerbi
# Excel
Get Data → File → Excel Workbook

# CSV
Get Data → File → Text/CSV

# JSON
Get Data → File → JSON
```

#### 2. Базы данных:
```powerbi
# SQL Server
Get Data → Database → SQL Server Database

# Oracle
Get Data → Database → Oracle Database

# MySQL
Get Data → Database → MySQL Database
```

#### 3. Облачные сервисы:
```powerbi
# Azure SQL Database
Get Data → Azure → Azure SQL Database

# SharePoint
Get Data → Online Services → SharePoint Online List

# Web
Get Data → Other → Web
```

### Пример подключения к SQL Server:

```powerbi
# Шаг 1: Подключение
Server: localhost\SQLEXPRESS
Database: SalesDB
Authentication: Windows

# Шаг 2: Выбор таблиц
Tables to include:
- Sales_Fact
- Customers_Dim
- Products_Dim
- Dates_Dim
```

### Настройка параметров запроса:

```powerbi
# Редактор Power Query
Home → Edit Queries → 
Advanced Editor → 

let
    Source = Sql.Database("localhost", "SalesDB"),
    Sales_Table = Source{[Schema="dbo",Item="Sales"]}[Data]
in
    Sales_Table
```

---

## Моделирование данных

### Star Schema (Звездная схема):

#### Основные принципы:

```
    DIM_Customers        DIM_Products        DIM_Dates
         │                    │                    │
         ▼                    ▼                    ▼
    [CustomerID]         [ProductID]          [DateKey]
         │                    │                    │
         └───────┬────────────┼────────────┬───────┘
                 ▼            ▼            ▼
            FACT_Sales (Центральная таблица фактов)
            - CustomerID (FK)
            - ProductID (FK)  
            - DateKey (FK)
            - SalesAmount
            - Quantity
```

### Создание связей:

#### 1. Один ко многим (1:N):
```powerbi
DIM_Customers[CustomerID] → FACT_Sales[CustomerID]
DIM_Products[ProductID] → FACT_Sales[ProductID]
DIM_Dates[DateKey] → FACT_Sales[DateKey]
```

#### 2. Многие ко многим (N:M):
```powerbi
# Через промежуточную таблицу фактов
DIM_Regions[RegionID] → BRIDGE_RegionSales[RegionID]
BRIDGE_RegionSales[SalesID] → FACT_Sales[SalesID]
```

### Настройка кардинальности:

```powerbi
# В Model View
Table1[Key] 1 → * Table2[ForeignKey]
# 1:* означает один ко многим
```

### Настройка направления кросс-фильтрации:

```powerbi
# Single (Односторонняя)
FACT_Sales → DIM_Customers

# Both (Двусторонняя)  
FACT_Sales ↔ DIM_Customers
```

### Создание вычисляемых столбцов:

```dax
# В Power BI Desktop
Modeling → New Column

# Примеры:
Full_Name = Customers[First_Name] & " " & Customers[Last_Name]

Age_Category = 
IF(Customers[Age] < 25, "Молодежь",
IF(Customers[Age] < 45, "Взрослые", "Пенсионеры"))

Profit_Margin = (Sales[Revenue] - Sales[Cost]) / Sales[Revenue]
```

---

## DAX (Data Analysis Expressions)

### Основы DAX:

#### 1. Синтаксис:
```dax
Measure_Name = CALCULATION(FUNCTION(TABLE[COLUMN]), FILTERS)
```

#### 2. Типы вычислений:
- **Меры (Measures)**: Агрегированные значения
- **Вычисляемые столбцы**: Значения для каждой строки
- **Вычисляемые таблицы**: Новые таблицы на основе расчетов

### Основные функции DAX:

#### Агрегатные функции:
```dax
Total_Sales = SUM(Sales[Amount])

Average_Price = AVERAGE(Products[Price])

Count_Transactions = COUNTROWS(Sales)

Max_Date = MAX(Dates[Date])

Min_Value = MIN(Table[Value])
```

#### Функции фильтрации:
```dax
# CALCULATE - изменение контекста фильтрации
Current_Year_Sales = 
CALCULATE(
    SUM(Sales[Amount]),
    Dates[Year] = YEAR(TODAY())
)

# FILTER - применение фильтра к таблице
High_Value_Customers = 
CALCULATE(
    [Total_Sales],
    FILTER(
        Customers,
        Customers[Total_Purchases] > 10000
    )
)
```

#### Временные функции:
```dax
# TOTALYTD - сумма с начала года
YTD_Sales = TOTALYTD(SUM(Sales[Amount]), Dates[Date])

# SAMEPERIODLASTYEAR - аналогичный период прошлого года
Previous_Year_Sales = 
CALCULATE(
    SUM(Sales[Amount]),
    SAMEPERIODLASTYEAR(Dates[Date])
)

# DATESBETWEEN - диапазон дат
Last_30_Days_Sales = 
CALCULATE(
    SUM(Sales[Amount]),
    DATESBETWEEN(
        Dates[Date],
        TODAY() - 30,
        TODAY()
    )
)
```

#### Логические функции:
```dax
# IF - условное выражение
Sales_Category = 
IF(
    [Total_Sales] > 10000,
    "Премиум",
    IF([Total_Sales] > 5000, "Стандарт", "Базовый")
)

# SWITCH - множественные условия
Customer_Tier = 
SWITCH(
    TRUE(),
    Customers[Annual_Spend] > 50000, "VIP",
    Customers[Annual_Spend] > 20000, "Premium",
    Customers[Annual_Spend] > 5000, "Standard",
    "Basic"
)
```

#### Таблицевые функции:
```dax
# SUMMARIZE - группировка данных
Monthly_Sales_Summary = 
SUMMARIZE(
    Sales,
    Dates[Year],
    Dates[Month],
    "Total_Sales", SUM(Sales[Amount]),
    "Transaction_Count", COUNTROWS(Sales)
)

# ADDCOLUMNS - добавление вычисляемых столбцов
Enhanced_Customer_Data = 
ADDCOLUMNS(
    Customers,
    "Lifetime_Value", [Total_Customer_Spend],
    "Avg_Order_Value", DIVIDE([Total_Customer_Spend], [Order_Count])
)
```

### Продвинутые техники DAX:

#### 1. Переменные (VAR):
```dax
Customer_Analysis = 
VAR TotalCustomers = COUNTROWS(Customers)
VAR ActiveCustomers = 
    CALCULATE(
        COUNTROWS(Customers),
        Customers[Status] = "Active"
    )
VAR ChurnRate = DIVIDE(TotalCustomers - ActiveCustomers, TotalCustomers)
RETURN
    ChurnRate
```

#### 2. Итерационные функции:
```dax
# SUMX - суммирование с итерацией
Weighted_Average_Price = 
DIVIDE(
    SUMX(Products, Products[Price] * Products[Quantity]),
    SUM(Products[Quantity])
)

# AVERAGEX - среднее значение с итерацией
Average_Discount_Rate = 
AVERAGEX(
    Sales,
    DIVIDE(Sales[Discount], Sales[ListPrice])
)
```

#### 3. Контекст в DAX:
```dax
# Row Context - контекст строки
Calculated_Column = Sales[Quantity] * Sales[UnitPrice]

# Filter Context - контекст фильтрации
Measure_Context = 
CALCULATE(
    SUM(Sales[Amount]),
    Products[Category] = "Electronics"
)
```

---

## Создание визуализаций

### Типы визуализаций:

#### 1. Диаграммы:
```powerbi
# Столбчатая диаграмма
Axis: Product_Category
Legend: Year
Values: Total_Sales

# Линейная диаграмма
Axis: Date
Values: Sales_Trend, Target_Line

# Круговая диаграмма
Legend: Region
Values: Market_Share
```

#### 2. Таблицы и матрицы:
```powerbi
# Матрица с иерархией
Rows: Region → City
Columns: Year
Values: Sales, Profit
```

#### 3. Картографические визуализации:
```powerbi
# Хороплет (Choropleth Map)
Location: Country/State
Color saturation: Sales_Per_Capita

# Точечная карта
Latitude: Store_Latitude
Longitude: Store_Longitude
Size: Revenue
Color: Performance_Category
```

### Настройка визуализаций:

#### 1. Форматирование:
```powerbi
# Цветовая схема
Format → Data colors → Customize colors

# Шрифты и размеры
Format → Title → Font size, Color

# Оси и сетка
Format → X-axis/Y-axis → Show/Hide, Labels
```

#### 2. Взаимодействия:
```powerbi
# Фильтрация других визуализаций
Selection → Edit Interactions → Filter/Highlight/None

# Drill-down иерархии
Double-click on visual element to drill down
```

#### 3. Закладки:
```powerbi
# Создание закладок состояния
View → Bookmarks → Add

# Навигация между состояниями
Bookmarks pane → Select bookmark
```

### Пример комплексной визуализации:

```powerbi
# Sales Dashboard Visual
Type: Multi-row card
Fields:
- Total Sales (KPI)
- Sales Growth YoY (%)
- Active Customers
- Average Order Value

Formatting:
- Data labels: Large, Bold
- Trend indicators: Arrows with color coding
- Conditional formatting: Red/Yellow/Green thresholds
```

---

## Дашборды и отчеты

### Создание дашборда:

#### 1. Структура дашборда:
```powerbi
# Header Section
- Company Logo
- Dashboard Title
- Last Refresh Time

# KPI Tiles (Top Row)
- Revenue
- Profit Margin
- Customer Satisfaction

# Main Visualizations (Middle Section)
- Sales Trend Chart
- Regional Performance Map
- Product Category Breakdown

# Detailed Tables (Bottom Section)
- Top Performing Products
- Recent Transactions
```

#### 2. Настройка фильтров:
```powerbi
# Срезы (Slicers)
- Date Range Slider
- Category Dropdown
- Region Checklist

# Синхронизация срезов
Format → Edit Interactions → Apply to all visuals
```

### Создание отчета:

#### 1. Страницы отчета:
```powerbi
Page 1: Executive Summary
- High-level KPIs
- Overall trend charts

Page 2: Sales Analysis
- Detailed sales breakdown
- Customer segmentation

Page 3: Product Performance
- Product category analysis
- Inventory metrics
```

#### 2. Навигация:
```powerbi
# Вкладки страниц
Pages pane → Rename pages with clear labels

# Кнопки навигации
Insert → Buttons → Page navigation buttons

# Закладки для детализации
Bookmarks → Detail views for each section
```

### Настройка безопасности:

#### 1. Row-level security (RLS):
```dax
# Создание ролей
Modeling → Manage Roles

# Пример правила RLS
Sales Representative Role:
[SalesRepID] = USERPRINCIPALNAME()

Regional Manager Role:
[Region] IN {"North", "South"}
```

#### 2. Динамическая безопасность:
```dax
# Динамическое ограничение по пользователю
User_Security = 
IF(
    Sales[SalesRepEmail] = USERPRINCIPALNAME(),
    TRUE(),
    FALSE()
)
```

---

## Публикация и совместная работа

### Публикация в Power BI Service:

#### 1. Подготовка к публикации:
```powerbi
# Проверка производительности
Home → Performance Analyzer

# Оптимизация модели
Modeling → Manage Relationships → Check cardinality

# Настройка параметров обновления
File → Options and settings → Data source settings
```

#### 2. Публикация:
```powerbi
Home → Publish → Select workspace
Enter credentials → Publish
```

### Совместная работа:

#### 1. Рабочие области:
```powerbi
# Создание рабочей области
Workspaces → Create workspace

# Добавление участников
Workspace settings → Access → Add members

# Настройка ролей
Admin, Member, Contributor, Viewer
```

#### 2. Совместное редактирование:
```powerbi
# Совместная разработка
Share → Send link to colleagues

# Комментарии и обсуждения
Report → Comments → Add feedback

# Версионирование
File → Save a copy → Version control
```

### Расписание обновлений:

```powerbi
# Настройка gateway
Settings → Gateways → Add data gateway

# Расписание обновлений
Dataset → Schedule refresh → Configure frequency

# Мониторинг обновлений
Dataset → Refresh history → View status
```

---

## Продвинутые техники

### 1. Composite Models:

#### Настройка DirectQuery и Import:
```powerbi
# Mixed mode modeling
Table1: Import mode (Historical data)
Table2: DirectQuery mode (Real-time data)

# Настройка в Model view
Table properties → Storage mode → Select appropriate mode
```

### 2. Aggregations:

#### Создание агрегированных таблиц:
```dax
# Агрегированная таблица для производительности
Sales_Aggregated = 
SUMMARIZE(
    Sales,
    Dates[Year],
    Dates[Month],
    Products[Category],
    "Total_Sales", SUM(Sales[Amount]),
    "Transaction_Count", COUNTROWS(Sales)
)
```

### 3. Advanced DAX Patterns:

#### Pattern 1: Running Totals:
```dax
Running_Total_Sales = 
CALCULATE(
    SUM(Sales[Amount]),
    FILTER(
        ALL(Dates),
        Dates[Date] <= MAX(Dates[Date])
    )
)
```

#### Pattern 2: Moving Averages:
```dax
Moving_Avg_30Days = 
CALCULATE(
    AVERAGE(Sales[Daily_Sales]),
    DATESINPERIOD(Dates[Date], MAX(Dates[Date]), -30, DAY)
)
```

#### Pattern 3: Percent of Total:
```dax
Percent_of_Total = 
DIVIDE(
    SUM(Sales[Amount]),
    CALCULATE(SUM(Sales[Amount]), ALLSELECTED())
)
```

### 4. Custom Visuals:

#### Установка пользовательских визуализаций:
```powerbi
# Marketplace
Home → Get more visuals → Browse marketplace

# Примеры полезных визуализаций:
- Deneb (Vega-lite visualizations)
- Financial Reporting Matrix
- Synoptic Panel
- Gantt Chart
```

---

## Практические примеры

### Пример 1: Аналитика продаж

#### Модель данных:
```sql
-- Создание таблиц
CREATE TABLE DIM_Customers (
    CustomerID INT PRIMARY KEY,
    CustomerName VARCHAR(100),
    Region VARCHAR(50),
    CustomerSegment VARCHAR(30)
);

CREATE TABLE DIM_Products (
    ProductID INT PRIMARY KEY,
    ProductName VARCHAR(100),
    Category VARCHAR(50),
    Subcategory VARCHAR(50)
);

CREATE TABLE DIM_Dates (
    DateKey DATE PRIMARY KEY,
    Year INT,
    Month INT,
    Quarter VARCHAR(10),
    DayOfWeek VARCHAR(10)
);

CREATE TABLE FACT_Sales (
    SaleID INT PRIMARY KEY,
    CustomerID INT,
    ProductID INT,
    DateKey DATE,
    Quantity INT,
    UnitPrice DECIMAL(10,2),
    Discount DECIMAL(5,2),
    FOREIGN KEY (CustomerID) REFERENCES DIM_Customers(CustomerID),
    FOREIGN KEY (ProductID) REFERENCES DIM_Products(ProductID),
    FOREIGN KEY (DateKey) REFERENCES DIM_Dates(DateKey)
);
```

#### Основные меры DAX:
```dax
# Общие показатели
Total_Revenue = SUM(FACT_Sales[Quantity] * FACT_Sales[UnitPrice])

Total_Quantity = SUM(FACT_Sales[Quantity])

Average_Order_Value = DIVIDE([Total_Revenue], COUNTROWS(FACT_Sales))

# Анализ по времени
Revenue_YTD = TOTALYTD([Total_Revenue], DIM_Dates[DateKey])

Revenue_Growth_YoY = 
DIVIDE(
    [Total_Revenue] - 
    CALCULATE([Total_Revenue], SAMEPERIODLASTYEAR(DIM_Dates[DateKey])),
    CALCULATE([Total_Revenue], SAMEPERIODLASTYEAR(DIM_Dates[DateKey]))
)

# Анализ по категориям
Top_Products = 
TOPN(10, 
    VALUES(DIM_Products[ProductName]), 
    [Total_Revenue]
)

# Когортный анализ
Customer_Lifetime_Value = 
CALCULATE(
    [Total_Revenue],
    DATESBETWEEN(
        DIM_Dates[DateKey],
        MIN(DIM_Dates[DateKey]),
        TODAY()
    )
)
```

#### Визуализации дашборда:
```powerbi
# KPI Cards
- Total Revenue (with trend arrow)
- Orders Count
- Average Order Value
- Customer Acquisition Rate

# Charts
- Revenue Trend (Line chart with months)
- Category Breakdown (Stacked column chart)
- Regional Performance (Map visualization)
- Top Products (Horizontal bar chart)

# Tables
- Recent Orders (Detailed transaction table)
- Customer Segmentation (Matrix with segments)
```

### Пример 2: HR Аналитика

#### Модель данных:
```sql
CREATE TABLE DIM_Employees (
    EmployeeID INT PRIMARY KEY,
    FirstName VARCHAR(50),
    LastName VARCHAR(50),
    Department VARCHAR(50),
    Position VARCHAR(50),
    HireDate DATE,
    TerminationDate DATE NULL,
    Salary DECIMAL(10,2)
);

CREATE TABLE DIM_Time (
    DateKey DATE PRIMARY KEY,
    Year INT,
    Month INT,
    Quarter VARCHAR(10)
);

CREATE TABLE FACT_Attendance (
    AttendanceID INT PRIMARY KEY,
    EmployeeID INT,
    DateKey DATE,
    HoursWorked DECIMAL(5,2),
    OvertimeHours DECIMAL(5,2),
    FOREIGN KEY (EmployeeID) REFERENCES DIM_Employees(EmployeeID),
    FOREIGN KEY (DateKey) REFERENCES DIM_Time(DateKey)
);
```

#### Меры DAX для HR:
```dax
# Показатели персонала
Active_Employees = 
CALCULATE(
    COUNTROWS(DIM_Employees),
    ISBLANK(DIM_Employees[TerminationDate]) ||
    DIM_Employees[TerminationDate] > TODAY()
)

Turnover_Rate = 
DIVIDE(
    COUNTROWS(
        FILTER(
            DIM_Employees,
            DIM_Employees[TerminationDate] >= STARTOFMONTH(TODAY()) &&
            DIM_Employees[TerminationDate] <= ENDOFMONTH(TODAY())
        )
    ),
    [Active_Employees]
)

# Анализ производительности
Average_Hours_Worked = AVERAGE(FACT_Attendance[HoursWorked])

Overtime_Rate = 
DIVIDE(
    SUM(FACT_Attendance[OvertimeHours]),
    SUM(FACT_Attendance[HoursWorked])
)

# Аналитика по отделам
Employees_per_Department = 
DISTINCTCOUNT(DIM_Employees[EmployeeID])

Salary_Budget_by_Department = 
SUM(DIM_Employees[Salary])

# Прогнозирование
Headcount_Forecast = 
FORECAST.LINEAR(
    TODAY(),
    VALUES(DIM_Time[DateKey]),
    [Active_Employees]
)
```

### Пример 3: Финансовая отчетность

#### Меры для финансового анализа:
```dax
# Финансовые коэффициенты
Gross_Profit = [Total_Revenue] - [Cost_of_Goods_Sold]

Gross_Profit_Margin = DIVIDE([Gross_Profit], [Total_Revenue])

Operating_Income = [Gross_Profit] - [Operating_Expenses]

Net_Profit_Margin = DIVIDE([Net_Income], [Total_Revenue])

# Анализ денежных потоков
Cash_Flow_Operating = 
CALCULATE(
    SUM(FACT_Transactions[Amount]),
    FACT_Transactions[AccountType] = "Operating"
)

Cash_Flow_Investing = 
CALCULATE(
    SUM(FACT_Transactions[Amount]),
    FACT_Transactions[AccountType] = "Investing"
)

# Бюджетный анализ
Budget_Variance = [Actual_Expenses] - [Budgeted_Expenses]

Budget_Variance_Percent = 
DIVIDE([Budget_Variance], [Budgeted_Expenses])

# ROI расчеты
Return_on_Investment = 
DIVIDE([Net_Profit], [Total_Investment])

Payback_Period = 
DIVIDE([Initial_Investment], [Annual_Cash_Flow])
```

---

## Заключение

`Power BI` — это мощная платформа для бизнес-аналитики, которая сочетает в себе удобство использования с продвинутыми аналитическими возможностями.

**Освоение `Power BI` открывает возможности для:**

✅ **Самообслуживания аналитики** - бизнес-пользователи могут создавать свои отчеты
✅ **Data-driven принятия решений** - основанное на данных принятие решений
✅ **Улучшенной визуализации** - понятные и интерактивные дашборды
✅ **Совместной работы** - командная работа над аналитикой
✅ **Масштабируемости** - от малого бизнеса до крупных корпораций

### Дальнейшее изучение:

#### Рекомендуемые ресурсы:
- **Microsoft Learn**: Официальные курсы по `Power BI`
- **Power BI Community**: Форум и поддержка сообщества
- **YouTube каналы**: `Guy in a Cube`, `SQLBI`
- **Книги**: `"The Definitive Guide to DAX"`, `"Power BI Cookbook"`

#### Сертификации:
- **PL-300**: `Microsoft Power BI Data Analyst`
- **DP-500**: `Designing and Implementing Enterprise-Scale Analytics Solutions`

Это руководство охватывает основы `Power BI`

Для профессионального использования рекомендуется практика на реальных данных и изучение продвинутых техник.

---

#### 💼 Автор: Дуплей Максим Игоревич

### 📲 Контакты:

- **Telegram №1:** [@quadd4rv1n7](https://t.me/quadd4rv1n7)
- **Telegram №2:** [@dupley_maxim_1999](https://t.me/dupley_maxim_1999)

📅 Дата: 26.01.2026

▶️ Версия 1.0

---
> 📧 **Предложения по сотрудничеству:** maksimqwe42@mail.ru

---

### 💼 Профиль на Profi.ru
[![Profi.ru Profile](https://img.shields.io/badge/Profi.ru-Дуплей%20М.И.-FF6B35?style=for-the-badge)](https://profi.ru/profile/DupleyMI)

> Консультации и услуги программирования на платформе Profi.ru

---

### 📚 Услуги обучения
[![Обучение технологиям и языкам программирования на Kwork](https://img.shields.io/badge/Kwork-Обучение%20Программированию-blue?style=for-the-badge&logo=kwork)](https://kwork.ru/usability-testing/42465951/obuchenie-tekhnologiyam-i-yazykam-programmirovaniya)

> Профессиональное обучение технологиям и языкам программирования. Персональные консультации и курсы от опытного преподавателя.

---

### 🏫 О школе
[![Website](https://img.shields.io/badge/Maestro7IT-school--maestro7it.ru-darkgreen?style=for-the-badge)](https://school-maestro7it.ru/)

> Инновационная школа программирования, специализирующаяся на подготовке специалистов в области современных технологий и языков программирования.
