-- Запросы к базе данных Chinook - Уровень Новичок
-- База данных музыкального магазина

-- 🔰 УРОВЕНЬ НОВИЧОК (BEGINNER)
-- ================================================

-- 1. Базовое исследование таблиц
SELECT name AS table_name
FROM sqlite_master 
WHERE type = 'table';

-- 2. Просмотр структуры таблицы
PRAGMA table_info(Artist);

-- 3. Первые 5 записей из таблицы исполнителей
SELECT * FROM Artist LIMIT 5;

-- 4. Подсчет общего количества исполнителей
SELECT COUNT(*) AS TotalArtists FROM Artist;

-- 5. Список всех жанров
SELECT Name FROM Genre ORDER BY Name;

-- 6. Найти исполнителей, чьи имена начинаются на 'A'
SELECT Name FROM Artist WHERE Name LIKE 'A%' ORDER BY Name;

-- 7. Количество альбомов
SELECT COUNT(*) AS TotalAlbums FROM Album;

-- 8. Средняя цена трека
SELECT AVG(UnitPrice) AS AveragePrice FROM Track;

-- 9. Клиенты из США
SELECT FirstName, LastName, City 
FROM Customer 
WHERE Country = 'USA';

-- 10. Треки продолжительностью более 5 минут
SELECT Name, Milliseconds/60000.0 AS Minutes
FROM Track 
WHERE Milliseconds > 300000
ORDER BY Minutes DESC;

-- 📈 УРОВЕНЬ СРЕДНИЙ (INTERMEDIATE)
-- ================================================

-- 11. Все альбомы конкретного исполнителя (AC/DC)
SELECT 
    ar.Name AS Artist,
    al.Title AS Album
FROM Artist ar
JOIN Album al ON ar.ArtistId = al.ArtistId
WHERE ar.Name = 'AC/DC';

-- 12. Треки с их альбомами и исполнителями
SELECT 
    t.Name AS Track,
    al.Title AS Album,
    ar.Name AS Artist
FROM Track t
JOIN Album al ON t.AlbumId = al.AlbumId
JOIN Artist ar ON al.ArtistId = ar.ArtistId
LIMIT 10;

-- 13. Количество треков по жанрам
SELECT 
    g.Name AS Genre,
    COUNT(t.TrackId) AS TrackCount
FROM Genre g
JOIN Track t ON g.GenreId = t.GenreId
GROUP BY g.GenreId, g.Name
ORDER BY TrackCount DESC;

-- 14. Топ-5 самых дорогих треков
SELECT 
    t.Name AS Track,
    t.UnitPrice,
    al.Title AS Album
FROM Track t
JOIN Album al ON t.AlbumId = al.AlbumId
ORDER BY t.UnitPrice DESC
LIMIT 5;

-- 15. Клиенты и их общие расходы
SELECT 
    c.FirstName,
    c.LastName,
    c.Country,
    SUM(i.Total) AS TotalSpent
FROM Customer c
JOIN Invoice i ON c.CustomerId = i.CustomerId
GROUP BY c.CustomerId
ORDER BY TotalSpent DESC
LIMIT 10;

-- 16. Продажи по странам
SELECT 
    c.Country,
    COUNT(i.InvoiceId) AS TotalInvoices,
    SUM(i.Total) AS TotalSales
FROM Customer c
JOIN Invoice i ON c.CustomerId = i.CustomerId
GROUP BY c.Country
ORDER BY TotalSales DESC;

-- 🚀 УРОВЕНЬ ПРОДВИНУТЫЙ (ADVANCED)
-- ================================================

-- 17. Самые популярные треки (топ 10)
SELECT 
    t.Name AS Track,
    ar.Name AS Artist,
    al.Title AS Album,
    SUM(il.Quantity) AS TotalSold,
    SUM(il.Quantity * il.UnitPrice) AS Revenue
FROM Track t
JOIN Album al ON t.AlbumId = al.AlbumId
JOIN Artist ar ON al.ArtistId = ar.ArtistId
JOIN InvoiceLine il ON t.TrackId = il.TrackId
GROUP BY t.TrackId
ORDER BY TotalSold DESC
LIMIT 10;

-- 18. Анализ покупательского поведения по жанрам
SELECT 
    g.Name AS Genre,
    COUNT(DISTINCT c.CustomerId) AS UniqueCustomers,
    SUM(il.Quantity) AS TotalTracksSold,
    AVG(il.UnitPrice) AS AveragePrice
FROM Genre g
JOIN Track t ON g.GenreId = t.GenreId
JOIN InvoiceLine il ON t.TrackId = il.TrackId
JOIN Invoice i ON il.InvoiceId = i.InvoiceId
JOIN Customer c ON i.CustomerId = c.CustomerId
GROUP BY g.GenreId
ORDER BY TotalTracksSold DESC;

-- 19. Месячные продажи с ростом/падением
WITH MonthlySales AS (
    SELECT 
        strftime('%Y-%m', InvoiceDate) AS Month,
        SUM(Total) AS MonthlyTotal
    FROM Invoice
    GROUP BY strftime('%Y-%m', InvoiceDate)
)
SELECT 
    Month,
    MonthlyTotal,
    LAG(MonthlyTotal) OVER (ORDER BY Month) AS PreviousMonth,
    MonthlyTotal - LAG(MonthlyTotal) OVER (ORDER BY Month) AS Difference,
    ROUND(
        (MonthlyTotal - LAG(MonthlyTotal) OVER (ORDER BY Month)) * 100.0 / 
        LAG(MonthlyTotal) OVER (ORDER BY Month), 2
    ) AS PercentChange
FROM MonthlySales
ORDER BY Month DESC
LIMIT 12;

-- 20. Рекомендации для клиентов (на основе предыдущих покупок)
SELECT DISTINCT
    c.FirstName,
    c.LastName,
    ar.Name AS RecommendedArtist,
    COUNT(*) AS MatchScore
FROM Customer c
JOIN Invoice i ON c.CustomerId = i.CustomerId
JOIN InvoiceLine il ON i.InvoiceId = il.InvoiceId
JOIN Track t ON il.TrackId = t.TrackId
JOIN Album al ON t.AlbumId = al.AlbumId
JOIN Artist ar ON al.ArtistId = ar.ArtistId
WHERE c.CustomerId = 2  -- Пример для клиента с ID 2
  AND ar.ArtistId NOT IN (
    SELECT DISTINCT ar2.ArtistId
    FROM Artist ar2
    JOIN Album al2 ON ar2.ArtistId = al2.ArtistId
    JOIN Track t2 ON al2.AlbumId = t2.AlbumId
    JOIN InvoiceLine il2 ON t2.TrackId = il2.TrackId
    JOIN Invoice i2 ON il2.InvoiceId = i2.InvoiceId
    WHERE i2.CustomerId = 2
  )
GROUP BY ar.ArtistId
ORDER BY MatchScore DESC
LIMIT 5;