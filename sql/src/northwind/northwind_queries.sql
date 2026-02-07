-- Northwind Database Queries
-- Classic business database with suppliers, products, customers, orders

-- 1. Basic table exploration
SELECT name AS table_name
FROM sqlite_master 
WHERE type = 'table';

-- 2. Get database schema
PRAGMA table_info(Products);

-- 3. Simple data exploration
SELECT * FROM Categories LIMIT 5;
SELECT * FROM Products LIMIT 5;
SELECT * FROM Customers LIMIT 5;

-- 4. Find products in specific category
SELECT 
    c.CategoryName,
    p.ProductName,
    p.UnitPrice
FROM Categories c
JOIN Products p ON c.CategoryID = p.CategoryID
WHERE c.CategoryName = 'Beverages'
ORDER BY p.UnitPrice DESC;

-- 5. Find suppliers from specific country
SELECT 
    CompanyName,
    ContactName,
    Country,
    Phone
FROM Suppliers
WHERE Country = 'UK'
ORDER BY CompanyName;

-- 6. Top 10 most expensive products
SELECT 
    ProductName,
    UnitPrice,
    UnitsInStock
FROM Products
ORDER BY UnitPrice DESC
LIMIT 10;

-- 7. Products that need reordering (low stock)
SELECT 
    ProductName,
    UnitsInStock,
    ReorderLevel
FROM Products
WHERE UnitsInStock <= ReorderLevel
ORDER BY UnitsInStock;

-- 8. Total orders by customer
SELECT 
    c.CompanyName,
    COUNT(o.OrderID) AS TotalOrders,
    SUM(od.Quantity * od.UnitPrice) AS TotalSpent
FROM Customers c
JOIN Orders o ON c.CustomerID = o.CustomerID
JOIN "Order Details" od ON o.OrderID = od.OrderID
GROUP BY c.CustomerID
ORDER BY TotalSpent DESC
LIMIT 10;

-- 9. Sales by employee
SELECT 
    e.FirstName || ' ' || e.LastName AS Employee,
    COUNT(o.OrderID) AS OrdersHandled,
    SUM(od.Quantity * od.UnitPrice) AS TotalSales
FROM Employees e
JOIN Orders o ON e.EmployeeID = o.EmployeeID
JOIN "Order Details" od ON o.OrderID = od.OrderID
GROUP BY e.EmployeeID
ORDER BY TotalSales DESC;

-- 10. Monthly sales report
SELECT 
    strftime('%Y-%m', OrderDate) AS Month,
    COUNT(OrderID) AS TotalOrders,
    SUM(Freight) AS TotalFreight,
    COUNT(DISTINCT CustomerID) AS UniqueCustomers
FROM Orders
GROUP BY strftime('%Y-%m', OrderDate)
ORDER BY Month DESC
LIMIT 12;