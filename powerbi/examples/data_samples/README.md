# Power BI Project Structure

## Sample Data Files

This folder contains sample datasets for Power BI practice.

### Sales Data
- `sales_2023.xlsx` - Продажи за 2023 год
- `sales_2024.xlsx` - Продажи за 2024 год
- `customers.xlsx` - База клиентов
- `products.xlsx` - Каталог продуктов

### Financial Data
- `pnl_2023.xlsx` - Отчет о прибылях и убытках
- `budget_2024.xlsx` - Бюджет на 2024 год
- `cash_flow.xlsx` - Движение денежных средств

### HR Data
- `employees.xlsx` - База сотрудников
- `attendance.xlsx` - Данные о посещаемости
- `performance.xlsx` - Оценка эффективности

## Usage Instructions

1. Загрузите данные в Power BI Desktop
2. Используйте Power Query для очистки данных
3. Создайте модель данных с правильными связями
4. Примените DAX формулы из примеров
5. Постройте визуализации по шаблонам

## Data Dictionary

### Sales Table
| Column | Type | Description |
|--------|------|-------------|
| OrderID | Integer | Уникальный номер заказа |
| OrderDate | Date | Дата заказа |
| CustomerID | Integer | ID клиента |
| ProductID | Integer | ID продукта |
| Quantity | Integer | Количество |
| UnitPrice | Decimal | Цена за единицу |
| Amount | Decimal | Общая сумма |

### Customers Table
| Column | Type | Description |
|--------|------|-------------|
| CustomerID | Integer | Уникальный ID клиента |
| CustomerName | String | Имя клиента |
| City | String | Город |
| Region | String | Регион |
| CustomerType | String | Тип клиента |

### Products Table
| Column | Type | Description |
|--------|------|-------------|
| ProductID | Integer | Уникальный ID продукта |
| ProductName | String | Название продукта |
| Category | String | Категория |
| Price | Decimal | Цена |
| Cost | Decimal | Себестоимость |