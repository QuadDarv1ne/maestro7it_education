-- TEST: Получение списка всех таблиц | 11
SELECT name FROM sqlite_master WHERE type = 'table';

-- TEST: Количество исполнителей | 275
SELECT COUNT(*) FROM Artist;

-- TEST: Количество альбомов AC/DC | 2
SELECT COUNT(*) 
FROM Album a
JOIN Artist ar ON a.ArtistId = ar.ArtistId
WHERE ar.Name = 'AC/DC';

-- TEST: 10 самых дорогих треков | 10
SELECT t.Name, t.UnitPrice
FROM Track t
ORDER BY t.UnitPrice DESC
LIMIT 10;

-- TEST: Количество треков по жанрам | 25
SELECT COUNT(DISTINCT g.GenreId) 
FROM Genre g
JOIN Track t ON g.GenreId = t.GenreId;

-- TEST: Общие продажи по странам | 24
SELECT COUNT(DISTINCT c.Country)
FROM Customer c
JOIN Invoice i ON c.CustomerId = i.CustomerId;

-- TEST: Клиенты из США | 13
SELECT COUNT(*) 
FROM Customer 
WHERE Country = 'USA';

-- TEST: Сумма всех продаж | 1
SELECT SUM(Total) as TotalSales
FROM Invoice;

-- TEST: Самые популярные треки (топ 5) | 5
SELECT t.Name, SUM(il.Quantity) as TotalSold
FROM Track t
JOIN InvoiceLine il ON t.TrackId = il.TrackId
GROUP BY t.TrackId
ORDER BY TotalSold DESC
LIMIT 5;

-- TEST: Количество заказов у клиентов | 59
SELECT COUNT(DISTINCT InvoiceId) 
FROM Invoice;