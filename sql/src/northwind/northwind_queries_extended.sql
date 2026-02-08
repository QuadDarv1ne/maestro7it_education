-- Запросы к базе данных Northwind - Уровень Новичок
-- Бизнес-база данных с поставщиками, продуктами, клиентами, заказами

-- 🔰 УРОВЕНЬ НОВИЧОК (BEGINNER)
-- ================================================

-- 1. Базовое исследование таблиц
SELECT name AS table_name
FROM sqlite_master 
WHERE type = 'table';

-- 2. Просмотр структуры таблицы Products
PRAGMA table_info(Products);

-- 3. Первые 5 продуктов
SELECT * FROM Products LIMIT 5;

-- 4. Все категории продуктов
SELECT CategoryName, Description 
FROM Categories 
ORDER BY CategoryName;

-- 5. Поставщики из США
SELECT CompanyName, ContactName, City
FROM Suppliers 
WHERE Country = 'USA';

-- 6. Продукты с низким запасом (менее 10 единиц)
SELECT ProductName, UnitsInStock, ReorderLevel
FROM Products 
WHERE UnitsInStock < 10
ORDER BY UnitsInStock;

-- 7. Количество клиентов
SELECT COUNT(*) AS TotalCustomers FROM Customers;

-- 8. Средняя цена продуктов
SELECT AVG(UnitPrice) AS AveragePrice FROM Products;

-- 9. Клиенты из Лондона
SELECT CompanyName, ContactName 
FROM Customers 
WHERE City = 'London';

-- 10. Продукты, снятые с производства
SELECT ProductName, Discontinued 
FROM Products 
WHERE Discontinued = 1;

-- 📈 УРОВЕНЬ СРЕДНИЙ (INTERMEDIATE)
-- ================================================

-- 11. Продукты по категориям с количеством
SELECT 
    c.CategoryName,
    COUNT(p.ProductID) AS ProductCount,
    AVG(p.UnitPrice) AS AveragePrice
FROM Categories c
JOIN Products p ON c.CategoryID = p.CategoryID
GROUP BY c.CategoryID
ORDER BY ProductCount DESC;

-- 12. Топ-10 самых дорогих продуктов
SELECT 
    ProductName,
    UnitPrice,
    c.CategoryName
FROM Products p
JOIN Categories c ON p.CategoryID = c.CategoryID
ORDER BY UnitPrice DESC
LIMIT 10;

-- 13. Поставщики и количество поставляемых продуктов
SELECT 
    s.CompanyName,
    s.Country,
    COUNT(p.ProductID) AS ProductsSupplied
FROM Suppliers s
JOIN Products p ON s.SupplierID = p.SupplierID
GROUP BY s.SupplierID
ORDER BY ProductsSupplied DESC;

-- 14. Заказы клиентов из Германии
SELECT 
    c.CompanyName,
    o.OrderID,
    o.OrderDate,
    o.Freight
FROM Customers c
JOIN Orders o ON c.CustomerID = o.CustomerID
WHERE c.Country = 'Germany'
ORDER BY o.OrderDate DESC
LIMIT 10;

-- 15. Сотрудники и количество обработанных заказов
SELECT 
    e.FirstName || ' ' || e.LastName AS Employee,
    COUNT(o.OrderID) AS OrdersHandled
FROM Employees e
JOIN Orders o ON e.EmployeeID = o.EmployeeID
GROUP BY e.EmployeeID
ORDER BY OrdersHandled DESC;

-- 16. Продажи по странам клиентов
SELECT 
    c.Country,
    COUNT(o.OrderID) AS TotalOrders,
    SUM(od.Quantity * od.UnitPrice) AS TotalRevenue
FROM Customers c
JOIN Orders o ON c.CustomerID = o.CustomerID
JOIN "Order Details" od ON o.OrderID = od.OrderID
GROUP BY c.Country
ORDER BY TotalRevenue DESC;

-- 🚀 УРОВЕНЬ ПРОДВИНУТЫЙ (ADVANCED)
-- ================================================

-- 17. Анализ прибыльности продуктов
SELECT 
    p.ProductName,
    c.CategoryName,
    p.UnitPrice,
    SUM(od.Quantity) AS TotalSold,
    SUM(od.Quantity * od.UnitPrice) AS Revenue,
    SUM(od.Quantity * (od.UnitPrice - p.UnitPrice)) AS Profit
FROM Products p
JOIN Categories c ON p.CategoryID = c.CategoryID
JOIN "Order Details" od ON p.ProductID = od.ProductID
GROUP BY p.ProductID
HAVING TotalSold > 50
ORDER BY Profit DESC
LIMIT 15;

-- 18. Ежемесячный анализ продаж с трендами
WITH MonthlySales AS (
    SELECT 
        strftime('%Y-%m', OrderDate) AS Month,
        COUNT(OrderID) AS OrdersCount,
        SUM(Freight) AS TotalFreight,
        COUNT(DISTINCT CustomerID) AS UniqueCustomers
    FROM Orders
    GROUP BY strftime('%Y-%m', OrderDate)
)
SELECT 
    Month,
    OrdersCount,
    TotalFreight,
    UniqueCustomers,
    LAG(OrdersCount) OVER (ORDER BY Month) AS PreviousMonthOrders,
    OrdersCount - LAG(OrdersCount) OVER (ORDER BY Month) AS OrdersChange,
    ROUND(
        (OrdersCount - LAG(OrdersCount) OVER (ORDER BY Month)) * 100.0 / 
        NULLIF(LAG(OrdersCount) OVER (ORDER BY Month), 0), 2
    ) AS OrdersGrowthPercent
FROM MonthlySales
ORDER BY Month DESC
LIMIT 12;

-- 19. Лучшие клиенты по объему покупок
SELECT 
    c.CompanyName,
    c.Country,
    COUNT(o.OrderID) AS TotalOrders,
    SUM(od.Quantity * od.UnitPrice) AS TotalSpent,
    AVG(od.Quantity * od.UnitPrice) AS AverageOrderValue,
    MAX(o.OrderDate) AS LastOrderDate
FROM Customers c
JOIN Orders o ON c.CustomerID = o.CustomerID
JOIN "Order Details" od ON o.OrderID = od.OrderID
GROUP BY c.CustomerID
HAVING TotalOrders > 5
ORDER BY TotalSpent DESC
LIMIT 20;

-- 20. Оптимизация запасов: прогноз потребностей
SELECT 
    p.ProductName,
    p.UnitsInStock,
    p.ReorderLevel,
    AVG(od.Quantity) AS AvgMonthlySales,
    p.UnitsInStock / NULLIF(AVG(od.Quantity), 0) AS MonthsOfSupply,
    CASE 
        WHEN p.UnitsInStock <= p.ReorderLevel THEN 'Нужно заказывать'
        WHEN p.UnitsInStock / NULLIF(AVG(od.Quantity), 0) < 2 THEN 'Заказать в ближайшее время'
        ELSE 'Запасов достаточно'
    END AS StockStatus
FROM Products p
JOIN "Order Details" od ON p.ProductID = od.ProductID
JOIN Orders o ON od.OrderID = o.OrderID
WHERE o.OrderDate >= date('now', '-6 months')
GROUP BY p.ProductID
ORDER BY MonthsOfSupply ASC;