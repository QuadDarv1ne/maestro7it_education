-- Решения упражнений по базе данных Northwind
-- Бизнес/торговля

-- Упражнение 1: Найти 10 самых дорогих продуктов
SELECT 
    ProductName AS Название_Продукта,
    UnitPrice AS Цена,
    UnitsInStock AS НаСкладе
FROM Products
ORDER BY UnitPrice DESC
LIMIT 10;

-- Упражнение 2: Показать продукты, которых нет в наличии
SELECT 
    p.ProductName AS Название_Продукта,
    c.CategoryName AS Категория,
    p.UnitsInStock AS НаСкладе,
    p.ReorderLevel AS Уровень_Заказа
FROM Products p
JOIN Categories c ON p.CategoryID = c.CategoryID
WHERE p.UnitsInStock = 0
ORDER BY c.CategoryName, p.ProductName;

-- Упражнение 3: Топ-5 поставщиков по количеству продуктов
SELECT 
    s.CompanyName AS Поставщик,
    s.Country AS Страна,
    COUNT(p.ProductID) AS Количество_Продуктов
FROM Suppliers s
JOIN Products p ON s.SupplierID = p.SupplierID
GROUP BY s.SupplierID
ORDER BY Количество_Продуктов DESC
LIMIT 5;

-- Упражнение 4: Заказы за последний месяц
SELECT 
    o.OrderID AS Номер_Заказа,
    c.CompanyName AS Клиент,
    o.OrderDate AS Дата_Заказа,
    o.RequiredDate AS Требуемая_Дата,
    o.ShippedDate AS Дата_Отгрузки
FROM Orders o
JOIN Customers c ON o.CustomerID = c.CustomerID
WHERE o.OrderDate >= date('now', '-1 month')
ORDER BY o.OrderDate DESC;

-- Упражнение 5: Сотрудники с наибольшим количеством заказов
SELECT 
    e.FirstName || ' ' || e.LastName AS Сотрудник,
    COUNT(o.OrderID) AS Количество_Заказов,
    SUM(od.Quantity * od.UnitPrice) AS Общая_Сумма
FROM Employees e
JOIN Orders o ON e.EmployeeID = o.EmployeeID
JOIN "Order Details" od ON o.OrderID = od.OrderID
GROUP BY e.EmployeeID
ORDER BY Количество_Заказов DESC;

-- Упражнение 6: Категории с самыми дорогими продуктами
SELECT 
    c.CategoryName AS Категория,
    MAX(p.UnitPrice) AS Максимальная_Цена,
    AVG(p.UnitPrice) AS Средняя_Цена,
    COUNT(*) AS Количество_Продуктов
FROM Categories c
JOIN Products p ON c.CategoryID = p.CategoryID
GROUP BY c.CategoryID
ORDER BY Максимальная_Цена DESC;

-- Упражнение 7: Клиенты, которые сделали заказы в 1997 году
SELECT DISTINCT
    c.CompanyName AS Клиент,
    c.Country AS Страна,
    c.City AS Город
FROM Customers c
JOIN Orders o ON c.CustomerID = o.CustomerID
WHERE strftime('%Y', o.OrderDate) = '1997'
ORDER BY c.CompanyName;

-- Упражнение 8: Продукты, которые никогда не заказывали
SELECT 
    p.ProductName AS Никогда_НеЗаказывали
FROM Products p
LEFT JOIN "Order Details" od ON p.ProductID = od.ProductID
WHERE od.ProductID IS NULL
ORDER BY p.ProductName;

-- Упражнение 9: Анализ продаж по кварталам
SELECT 
    strftime('%Y', o.OrderDate) AS Год,
    CASE 
        WHEN CAST(strftime('%m', o.OrderDate) AS INTEGER) BETWEEN 1 AND 3 THEN 'Q1'
        WHEN CAST(strftime('%m', o.OrderDate) AS INTEGER) BETWEEN 4 AND 6 THEN 'Q2'
        WHEN CAST(strftime('%m', o.OrderDate) AS INTEGER) BETWEEN 7 AND 9 THEN 'Q3'
        ELSE 'Q4'
    END AS Квартал,
    COUNT(o.OrderID) AS Количество_Заказов,
    SUM(od.Quantity * od.UnitPrice) AS Общая_Сумма
FROM Orders o
JOIN "Order Details" od ON o.OrderID = od.OrderID
GROUP BY strftime('%Y', o.OrderDate), 
         CASE 
             WHEN CAST(strftime('%m', o.OrderDate) AS INTEGER) BETWEEN 1 AND 3 THEN 'Q1'
             WHEN CAST(strftime('%m', o.OrderDate) AS INTEGER) BETWEEN 4 AND 6 THEN 'Q2'
             WHEN CAST(strftime('%m', o.OrderDate) AS INTEGER) BETWEEN 7 AND 9 THEN 'Q3'
             ELSE 'Q4'
         END
ORDER BY Год DESC, Квартал;

-- Упражнение 10: Поставщики из США с продуктами дороже $50
SELECT 
    s.CompanyName AS Поставщик,
    s.ContactName AS Контакт,
    s.Phone AS Телефон,
    COUNT(p.ProductID) AS Дорогих_Продуктов
FROM Suppliers s
JOIN Products p ON s.SupplierID = p.SupplierID
WHERE s.Country = 'USA' AND p.UnitPrice > 50
GROUP BY s.SupplierID
ORDER BY Дорогих_Продуктов DESC;