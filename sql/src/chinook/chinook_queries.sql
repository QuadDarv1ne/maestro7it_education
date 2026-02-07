-- Chinook Database Queries
-- Music store database with artists, albums, tracks, customers, invoices

-- 1. Basic table exploration
SELECT name AS table_name
FROM sqlite_master 
WHERE type = 'table';

-- 2. Get database schema for specific table
PRAGMA table_info(Album);

-- 3. Simple data exploration
SELECT * FROM Artist LIMIT 5;
SELECT * FROM Album LIMIT 5;
SELECT * FROM Track LIMIT 5;

-- 4. Find all albums by a specific artist (AC/DC example)
SELECT 
    a.Name AS Artist,
    al.Title AS Album
FROM Artist a
JOIN Album al ON a.ArtistId = al.ArtistId
WHERE a.Name = 'AC/DC';

-- 5. Find top 10 most expensive tracks
SELECT 
    t.Name AS Track,
    a.Title AS Album,
    t.UnitPrice
FROM Track t
JOIN Album al ON t.AlbumId = al.AlbumId
ORDER BY t.UnitPrice DESC
LIMIT 10;

-- 6. Count tracks per genre
SELECT 
    g.Name AS Genre,
    COUNT(t.TrackId) AS TrackCount
FROM Genre g
JOIN Track t ON g.GenreId = t.GenreId
GROUP BY g.GenreId, g.Name
ORDER BY TrackCount DESC;

-- 7. Find customers from specific country
SELECT 
    FirstName,
    LastName,
    Country,
    City
FROM Customer
WHERE Country = 'USA'
ORDER BY LastName;

-- 8. Total sales by country
SELECT 
    c.Country,
    COUNT(i.InvoiceId) AS TotalInvoices,
    SUM(i.Total) AS TotalSales
FROM Customer c
JOIN Invoice i ON c.CustomerId = i.CustomerId
GROUP BY c.Country
ORDER BY TotalSales DESC;

-- 9. Best selling tracks
SELECT 
    t.Name AS Track,
    a.Title AS Album,
    ar.Name AS Artist,
    SUM(il.Quantity) AS TotalSold
FROM Track t
JOIN Album al ON t.AlbumId = al.AlbumId
JOIN Artist ar ON al.ArtistId = ar.ArtistId
JOIN InvoiceLine il ON t.TrackId = il.TrackId
GROUP BY t.TrackId
ORDER BY TotalSold DESC
LIMIT 10;

-- 10. Customer purchase history
SELECT 
    c.FirstName,
    c.LastName,
    i.InvoiceDate,
    i.Total
FROM Customer c
JOIN Invoice i ON c.CustomerId = i.CustomerId
WHERE c.CustomerId = 2
ORDER BY i.InvoiceDate DESC;