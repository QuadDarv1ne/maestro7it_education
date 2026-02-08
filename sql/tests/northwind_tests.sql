-- TEST: Получение списка всех таблиц | 13
SELECT name FROM sqlite_master WHERE type = 'table';

-- TEST: Количество продуктов | 77
SELECT COUNT(*) FROM Product;

-- TEST: Количество поставщиков | 29
SELECT COUNT(*) FROM Supplier;

-- TEST: Количество заказов | 150
SELECT COUNT(*) FROM [Order];

-- TEST: Топ 5 самых дорогих продуктов | 5
SELECT ProductName, UnitPrice
FROM Product
ORDER BY UnitPrice DESC
LIMIT 5;

-- TEST: Количество клиентов | 91
SELECT COUNT(*) FROM Customer;

-- TEST: Заказы из Германии | 13
SELECT COUNT(*) 
FROM [Order] o
JOIN Customer c ON o.CustomerId = c.Id
WHERE c.Country = 'Germany';

-- TEST: Общая сумма заказов | 1
SELECT SUM(Freight) as TotalFreight
FROM [Order];

-- TEST: Продукты категории Beverages | 12
SELECT COUNT(*)
FROM Product p
JOIN Category c ON p.CategoryId = c.Id
WHERE c.CategoryName = 'Beverages';

-- TEST: Количество заказов по странам | 21
SELECT COUNT(DISTINCT c.Country)
FROM Customer c
JOIN [Order] o ON c.Id = o.CustomerId;