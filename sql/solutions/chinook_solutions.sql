-- Решения упражнений по базе данных Chinook
-- Музыкальный магазин

-- Упражнение 1: Найти всех исполнителей, начинающихся на букву "B"
SELECT Name AS Исполнитель
FROM Artist
WHERE Name LIKE 'B%'
ORDER BY Name;

-- Упражнение 2: Показать 5 самых дорогих треков каждого жанра
SELECT 
    g.Name AS Жанр,
    t.Name AS Трек,
    t.UnitPrice AS Цена,
    ROW_NUMBER() OVER (PARTITION BY g.GenreId ORDER BY t.UnitPrice DESC) AS Рейтинг
FROM Track t
JOIN Genre g ON t.GenreId = g.GenreId
WHERE ROW_NUMBER() OVER (PARTITION BY g.GenreId ORDER BY t.UnitPrice DESC) <= 5
ORDER BY g.Name, t.UnitPrice DESC;

-- Альтернативное решение для упражнения 2 (без оконных функций):
WITH TopTracks AS (
    SELECT 
        g.GenreId,
        g.Name AS Жанр,
        t.Name AS Трек,
        t.UnitPrice AS Цена,
        ROW_NUMBER() OVER (PARTITION BY g.GenreId ORDER BY t.UnitPrice DESC) as rn
    FROM Track t
    JOIN Genre g ON t.GenreId = g.GenreId
)
SELECT Жанр, Трек, Цена
FROM TopTracks
WHERE rn <= 5
ORDER BY Жанр, Цена DESC;

-- Упражнение 3: Найти клиентов, которые потратили более $40
SELECT 
    c.FirstName || ' ' || c.LastName AS Клиент,
    c.Country AS Страна,
    SUM(i.Total) AS Общая_Сумма
FROM Customer c
JOIN Invoice i ON c.CustomerId = i.CustomerId
GROUP BY c.CustomerId
HAVING SUM(i.Total) > 40
ORDER BY Общая_Сумма DESC;

-- Упражнение 4: Показать месячную статистику продаж за 2021 год
SELECT 
    strftime('%Y-%m', InvoiceDate) AS Месяц,
    COUNT(*) AS Количество_Счетов,
    SUM(Total) AS Общая_Сумма,
    AVG(Total) AS Средний_Чек
FROM Invoice
WHERE strftime('%Y', InvoiceDate) = '2021'
GROUP BY strftime('%Y-%m', InvoiceDate)
ORDER BY Месяц;

-- Упражнение 5: Найти треки, которые есть в более чем 10 плейлистах
SELECT 
    t.Name AS Трек,
    COUNT(pt.PlaylistId) AS Количество_Плейлистов
FROM Track t
JOIN PlaylistTrack pt ON t.TrackId = pt.TrackId
GROUP BY t.TrackId
HAVING COUNT(pt.PlaylistId) > 10
ORDER BY Количество_Плейлистов DESC;

-- Упражнение 6: Сравнение продаж по странам
SELECT 
    c.Country AS Страна,
    COUNT(DISTINCT c.CustomerId) AS Количество_Клиентов,
    COUNT(i.InvoiceId) AS Количество_Счетов,
    SUM(i.Total) AS Общая_Сумма,
    ROUND(AVG(i.Total), 2) AS Средний_Чек
FROM Customer c
JOIN Invoice i ON c.CustomerId = i.CustomerId
GROUP BY c.Country
ORDER BY Общая_Сумма DESC;

-- Упражнение 7: Топ-10 альбомов по выручке
SELECT 
    a.Title AS Альбом,
    ar.Name AS Исполнитель,
    SUM(il.UnitPrice * il.Quantity) AS Выручка
FROM Album a
JOIN Artist ar ON a.ArtistId = ar.ArtistId
JOIN Track t ON a.AlbumId = t.AlbumId
JOIN InvoiceLine il ON t.TrackId = il.TrackId
GROUP BY a.AlbumId
ORDER BY Выручка DESC
LIMIT 10;

-- Упражнение 8: Клиенты по штатам/областям (только где клиенты есть)
SELECT 
    c.State AS Штат,
    COUNT(*) AS Количество_Клиентов,
    SUM(i.Total) AS Общая_Сумма
FROM Customer c
JOIN Invoice i ON c.CustomerId = i.CustomerId
WHERE c.State IS NOT NULL AND c.State != ''
GROUP BY c.State
ORDER BY Количество_Клиентов DESC;

-- Упражнение 9: Анализ продолжительности треков по жанрам
SELECT 
    g.Name AS Жанр,
    COUNT(*) AS Количество_Треков,
    ROUND(AVG(t.Milliseconds) / 1000.0 / 60, 2) AS Средняя_Длительность_мин,
    ROUND(MIN(t.Milliseconds) / 1000.0 / 60, 2) AS Минимальная_Длительность_мин,
    ROUND(MAX(t.Milliseconds) / 1000.0 / 60, 2) AS Максимальная_Длительность_мин
FROM Track t
JOIN Genre g ON t.GenreId = g.GenreId
GROUP BY g.GenreId
ORDER BY Количество_Треков DESC;

-- Упражнение 10: Клиенты, которые покупали в каждом году
SELECT 
    c.FirstName || ' ' || c.LastName AS Клиент,
    COUNT(DISTINCT strftime('%Y', i.InvoiceDate)) AS Количество_Лет_Покупок
FROM Customer c
JOIN Invoice i ON c.CustomerId = i.CustomerId
GROUP BY c.CustomerId
HAVING COUNT(DISTINCT strftime('%Y', i.InvoiceDate)) = (
    SELECT COUNT(DISTINCT strftime('%Y', InvoiceDate)) 
    FROM Invoice
)
ORDER BY Клиент;