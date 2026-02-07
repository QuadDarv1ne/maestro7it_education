-- Шаблон проекта: Анализ продаж в розничной сети
-- Использует базу данных Northwind в качестве примера

-- ==========================================
-- 1. ИССЛЕДОВАНИЕ БАЗЫ ДАННЫХ
-- ==========================================

-- Просмотр структуры таблиц
SELECT name FROM sqlite_master WHERE type = 'table';

-- Просмотр структуры ключевых таблиц
PRAGMA table_info(Products);
PRAGMA table_info(Customers);
PRAGMA table_info(Orders);
PRAGMA table_info('Order Details');

-- ==========================================
-- 2. АНАЛИЗ ПРОДУКТОВ
-- ==========================================

-- Общая статистика по продуктам
SELECT 
    COUNT(*) as ОбщееКоличествоПродуктов,
    COUNT(DISTINCT CategoryID) as КоличествоКатегорий,
    MIN(UnitPrice) as МинимальнаяЦена,
    MAX(UnitPrice) as МаксимальнаяЦена,
    AVG(UnitPrice) as СредняяЦена
FROM Products;

-- Продукты по категориям
SELECT 
    c.CategoryName as Категория,
    COUNT(p.ProductID) as КоличествоПродуктов,
    AVG(p.UnitPrice) as СредняяЦена,
    SUM(p.UnitsInStock) as ОбщийЗапас
FROM Categories c
JOIN Products p ON c.CategoryID = p.CategoryID
GROUP BY c.CategoryID
ORDER BY КоличествоПродуктов DESC;

-- Топ-10 самых дорогих продуктов
SELECT 
    p.ProductName as Продукт,
    c.CategoryName as Категория,
    p.UnitPrice as Цена,
    p.UnitsInStock as НаСкладе
FROM Products p
JOIN Categories c ON p.CategoryID = c.CategoryID
ORDER BY p.UnitPrice DESC
LIMIT 10;

-- Продукты с низким запасом
SELECT 
    p.ProductName as Продукт,
    c.CategoryName as Категория,
    p.UnitsInStock as НаСкладе,
    p.ReorderLevel as УровеньЗаказа,
    s.CompanyName as Поставщик
FROM Products p
JOIN Categories c ON p.CategoryID = c.CategoryID
JOIN Suppliers s ON p.SupplierID = s.SupplierID
WHERE p.UnitsInStock <= p.ReorderLevel
ORDER BY p.UnitsInStock;

-- ==========================================
-- 3. АНАЛИЗ КЛИЕНТОВ
-- ==========================================

-- Статистика клиентов
SELECT 
    COUNT(*) as ОбщееКоличествоКлиентов,
    COUNT(DISTINCT Country) as КоличествоСтран,
    COUNT(DISTINCT City) as КоличествоГородов
FROM Customers;

-- Клиенты по странам
SELECT 
    Country as Страна,
    COUNT(*) as КоличествоКлиентов,
    COUNT(DISTINCT City) as Городов
FROM Customers
GROUP BY Country
ORDER BY КоличествоКлиентов DESC;

-- Топ-10 клиентов по количеству заказов
SELECT 
    c.CompanyName as Клиент,
    c.Country as Страна,
    c.City as Город,
    COUNT(o.OrderID) as КоличествоЗаказов,
    SUM(od.Quantity * od.UnitPrice) as ОбщаяСумма
FROM Customers c
JOIN Orders o ON c.CustomerID = o.CustomerID
JOIN "Order Details" od ON o.OrderID = od.OrderID
GROUP BY c.CustomerID
ORDER BY КоличествоЗаказов DESC
LIMIT 10;

-- ==========================================
-- 4. АНАЛИЗ ЗАКАЗОВ
-- ==========================================

-- Статистика заказов
SELECT 
    COUNT(*) as ОбщееКоличествоЗаказов,
    COUNT(DISTINCT CustomerID) as УникальныхКлиентов,
    COUNT(DISTINCT EmployeeID) as КоличествоCотрудников,
    MIN(OrderDate) as ПерваяДатаЗаказа,
    MAX(OrderDate) as ПоследняяДатаЗаказа
FROM Orders;

-- Заказы по периодам (год)
SELECT 
    strftime('%Y', OrderDate) as Год,
    COUNT(*) as Количество_заказов,
    COUNT(DISTINCT CustomerID) as Уникальных_клиентов,
    SUM(od.Quantity * od.UnitPrice) as Общая_сумма
FROM Orders o
JOIN "Order Details" od ON o.OrderID = od.OrderID
GROUP BY strftime('%Y', OrderDate)
ORDER BY Год;

-- Заказы по кварталам
SELECT 
    strftime('%Y', OrderDate) as Год,
    CASE 
        WHEN CAST(strftime('%m', OrderDate) AS INTEGER) BETWEEN 1 AND 3 THEN 'Q1'
        WHEN CAST(strftime('%m', OrderDate) AS INTEGER) BETWEEN 4 AND 6 THEN 'Q2'
        WHEN CAST(strftime('%m', OrderDate) AS INTEGER) BETWEEN 7 AND 9 THEN 'Q3'
        ELSE 'Q4'
    END as Квартал,
    COUNT(*) as Количество_заказов,
    SUM(od.Quantity * od.UnitPrice) as Общая_сумма
FROM Orders o
JOIN "Order Details" od ON o.OrderID = od.OrderID
GROUP BY 
    strftime('%Y', OrderDate),
    CASE 
        WHEN CAST(strftime('%m', OrderDate) AS INTEGER) BETWEEN 1 AND 3 THEN 'Q1'
        WHEN CAST(strftime('%m', OrderDate) AS INTEGER) BETWEEN 4 AND 6 THEN 'Q2'
        WHEN CAST(strftime('%m', OrderDate) AS INTEGER) BETWEEN 7 AND 9 THEN 'Q3'
        ELSE 'Q4'
    END
ORDER BY Год DESC, Квартал;

-- ==========================================
-- 5. АНАЛИЗ ПОСТАВЩИКОВ
-- ==========================================

-- Статистика по поставщикам
SELECT 
    s.CompanyName as Поставщик,
    s.Country as Страна,
    COUNT(p.ProductID) as КоличествоПродуктов,
    AVG(p.UnitPrice) as СредняяЦена,
    SUM(p.UnitsInStock) as ОбщийЗапас
FROM Suppliers s
JOIN Products p ON s.SupplierID = p.SupplierID
GROUP BY s.SupplierID
ORDER BY КоличествоПродуктов DESC;

-- Поставщики по странам
SELECT 
    Country as Страна,
    COUNT(*) as КоличествоПоставщиков,
    SUM(КоличествоПродуктов) as ОбщееКоличествоПродуктов
FROM (
    SELECT 
        s.Country,
        s.SupplierID,
        COUNT(p.ProductID) as КоличествоПродуктов
    FROM Suppliers s
    JOIN Products p ON s.SupplierID = p.SupplierID
    GROUP BY s.SupplierID
) as supplier_stats
GROUP BY Country
ORDER BY КоличествоПоставщиков DESC;

-- ==========================================
-- 6. КОМПЛЕКСНЫЙ АНАЛИЗ
-- ==========================================

-- Топ-10 самых прибыльных продуктов
SELECT 
    p.ProductName as Продукт,
    c.CategoryName as Категория,
    SUM(od.Quantity) as ОбщееКоличество,
    SUM(od.Quantity * od.UnitPrice) as ОбщаяВыручка,
    AVG(od.UnitPrice) as СредняяЦенаПродажи
FROM Products p
JOIN Categories c ON p.CategoryID = c.CategoryID
JOIN "Order Details" od ON p.ProductID = od.ProductID
GROUP BY p.ProductID
ORDER BY ОбщаяВыручка DESC
LIMIT 10;

-- Анализ сезонности продаж
SELECT 
    strftime('%m', OrderDate) as Месяц,
    COUNT(*) as Количество_заказов,
    SUM(od.Quantity * od.UnitPrice) as Общая_сумма,
    AVG(od.Quantity * od.UnitPrice) as Средний_чек
FROM Orders o
JOIN "Order Details" od ON o.OrderID = od.OrderID
GROUP BY strftime('%m', OrderDate)
ORDER BY Месяц;

-- Клиенты с высокой ценностью (более 10 заказов)
SELECT 
    c.CompanyName as Клиент,
    c.Country as Страна,
    COUNT(o.OrderID) as КоличествоЗаказов,
    SUM(od.Quantity * od.UnitPrice) as ОбщаяСумма,
    AVG(od.Quantity * od.UnitPrice) as СреднийЧек,
    MIN(o.OrderDate) as ПервыйЗаказ,
    MAX(o.OrderDate) as ПоследнийЗаказ
FROM Customers c
JOIN Orders o ON c.CustomerID = o.CustomerID
JOIN "Order Details" od ON o.OrderID = od.OrderID
GROUP BY c.CustomerID
HAVING COUNT(o.OrderID) > 10
ORDER BY ОбщаяСумма DESC;

-- ==========================================
-- 7. ОТЧЕТЫ И РЕКОМЕНДАЦИИ
-- ==========================================

-- Продукты для снятия с производства (никогда не заказывались)
SELECT 
    p.ProductName as НеПродаваемыйПродукт,
    c.CategoryName as Категория,
    p.UnitPrice as Цена,
    p.UnitsInStock as НаСкладе
FROM Products p
JOIN Categories c ON p.CategoryID = c.CategoryID
LEFT JOIN "Order Details" od ON p.ProductID = od.ProductID
WHERE od.ProductID IS NULL
ORDER BY p.UnitPrice DESC;

-- Потенциальные проблемы с запасами
SELECT 
    p.ProductName as Продукт,
    c.CategoryName as Категория,
    p.UnitsInStock as НаСкладе,
    p.ReorderLevel as УровеньЗаказа,
    CASE 
        WHEN p.UnitsInStock = 0 THEN 'Нет в наличии'
        WHEN p.UnitsInStock <= p.ReorderLevel * 0.5 THEN 'Критический уровень'
        WHEN p.UnitsInStock <= p.ReorderLevel THEN 'Низкий уровень'
        ELSE 'Нормальный уровень'
    END as СтатусЗапаса
FROM Products p
JOIN Categories c ON p.CategoryID = c.CategoryID
WHERE p.UnitsInStock <= p.ReorderLevel OR p.UnitsInStock = 0
ORDER BY 
    CASE 
        WHEN p.UnitsInStock = 0 THEN 1
        WHEN p.UnitsInStock <= p.ReorderLevel * 0.5 THEN 2
        WHEN p.UnitsInStock <= p.ReorderLevel THEN 3
        ELSE 4
    END;

-- ==========================================
-- 8. ДОПОЛНИТЕЛЬНЫЕ ЗАПРОСЫ ДЛЯ АНАЛИЗА
-- ==========================================

-- Среднее время выполнения заказов
-- (предполагая, что ShippedDate доступно)
SELECT 
    AVG(julianday(ShippedDate) - julianday(OrderDate)) as СреднееВремяВыполнения_дней
FROM Orders
WHERE ShippedDate IS NOT NULL;

-- Клиенты, которые не делали заказы более 90 дней
-- SELECT 
--     c.CompanyName as Клиент,
--     c.Country as Страна,
--     MAX(o.OrderDate) as ПоследнийЗаказ,
--     julianday('now') - julianday(MAX(o.OrderDate)) as ДнейСПоследнегоЗаказа
-- FROM Customers c
-- LEFT JOIN Orders o ON c.CustomerID = o.CustomerID
-- GROUP BY c.CustomerID
-- HAVING MAX(o.OrderDate) IS NULL OR julianday('now') - julianday(MAX(o.OrderDate)) > 90
-- ORDER BY ДнейСПоследнегоЗаказа DESC;

-- Тренды по категориям продуктов
-- SELECT 
--     c.CategoryName as Категория,
--     strftime('%Y-%m', o.OrderDate) as Месяц,
--     SUM(od.Quantity * od.UnitPrice) as Выручка
-- FROM Categories c
-- JOIN Products p ON c.CategoryID = p.CategoryID
-- JOIN "Order Details" od ON p.ProductID = od.ProductID
-- JOIN Orders o ON od.OrderID = o.OrderID
-- GROUP BY c.CategoryID, strftime('%Y-%m', o.OrderDate)
-- ORDER BY Месяц DESC, Выручка DESC;