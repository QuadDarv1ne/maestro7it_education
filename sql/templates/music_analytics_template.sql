-- Шаблон проекта: Музыкальная аналитика
-- Использует базу данных Chinook в качестве примера

-- ==========================================
-- 1. ИССЛЕДОВАНИЕ БАЗЫ ДАННЫХ
-- ==========================================

-- Просмотр структуры таблиц
SELECT name FROM sqlite_master WHERE type = 'table';

-- Просмотр структуры ключевых таблиц
PRAGMA table_info(Artist);
PRAGMA table_info(Album);
PRAGMA table_info(Track);
PRAGMA table_info(Customer);
PRAGMA table_info(Invoice);

-- ==========================================
-- 2. АНАЛИЗ ИСПОЛНИТЕЛЕЙ И АЛЬБОМОВ
-- ==========================================

-- Общая статистика
SELECT 
    (SELECT COUNT(*) FROM Artist) as КоличествоИсполнителей,
    (SELECT COUNT(*) FROM Album) as КоличествоАльбомов,
    (SELECT COUNT(*) FROM Track) as КоличествоТреков,
    (SELECT COUNT(*) FROM Genre) as КоличествоЖанров;

-- Исполнители по количеству альбомов
SELECT 
    a.Name as Исполнитель,
    COUNT(al.AlbumId) as КоличествоАльбомов
FROM Artist a
JOIN Album al ON a.ArtistId = al.ArtistId
GROUP BY a.ArtistId
ORDER BY КоличествоАльбомов DESC
LIMIT 15;

-- Альбомы по количеству треков
SELECT 
    al.Title as Альбом,
    ar.Name as Исполнитель,
    COUNT(t.TrackId) as КоличествоТреков,
    SUM(t.Milliseconds) / 1000 / 60 as ОбщееВремя_минут
FROM Album al
JOIN Artist ar ON al.ArtistId = ar.ArtistId
JOIN Track t ON al.AlbumId = t.AlbumId
GROUP BY al.AlbumId
ORDER BY КоличествоТреков DESC
LIMIT 10;

-- ==========================================
-- 3. АНАЛИЗ ЖАНРОВ
-- ==========================================

-- Популярность жанров
SELECT 
    g.Name as Жанр,
    COUNT(t.TrackId) as КоличествоТреков,
    COUNT(DISTINCT al.AlbumId) as КоличествоАльбомов,
    COUNT(DISTINCT ar.ArtistId) as КоличествоИсполнителей
FROM Genre g
JOIN Track t ON g.GenreId = t.GenreId
JOIN Album al ON t.AlbumId = al.AlbumId
JOIN Artist ar ON al.ArtistId = ar.ArtistId
GROUP BY g.GenreId
ORDER BY КоличествоТреков DESC;

-- Средняя продолжительность треков по жанрам
SELECT 
    g.Name as Жанр,
    COUNT(t.TrackId) as КоличествоТреков,
    ROUND(AVG(t.Milliseconds) / 1000.0 / 60, 2) as СредняяПродолжительность_минут,
    MIN(t.Milliseconds) / 1000 / 60 as Минимальная_минут,
    MAX(t.Milliseconds) / 1000 / 60 as Максимальная_минут
FROM Genre g
JOIN Track t ON g.GenreId = t.GenreId
GROUP BY g.GenreId
ORDER BY СредняяПродолжительность_минут DESC;

-- ==========================================
-- 4. АНАЛИЗ ЦЕНОВОЙ ПОЛИТИКИ
-- ==========================================

-- Статистика по ценам
SELECT 
    MIN(UnitPrice) as МинимальнаяЦена,
    MAX(UnitPrice) as МаксимальнаяЦена,
    ROUND(AVG(UnitPrice), 2) as СредняяЦена,
    ROUND(AVG(UnitPrice) * COUNT(*), 2) as ПотенциальныйДоход
FROM Track;

-- Треки по ценовым категориям
SELECT 
    CASE 
        WHEN UnitPrice < 0.99 THEN 'Бюджетные (<$0.99)'
        WHEN UnitPrice = 0.99 THEN 'Стандартные ($0.99)'
        WHEN UnitPrice > 0.99 THEN 'Премиум (>$0.99)'
    END as ЦеноваяКатегория,
    COUNT(*) as КоличествоТреков,
    ROUND(AVG(UnitPrice), 2) as СредняяЦена
FROM Track
GROUP BY 
    CASE 
        WHEN UnitPrice < 0.99 THEN 'Бюджетные (<$0.99)'
        WHEN UnitPrice = 0.99 THEN 'Стандартные ($0.99)'
        WHEN UnitPrice > 0.99 THEN 'Премиум (>$0.99)'
    END
ORDER BY СредняяЦена;

-- Самые дорогие треки
SELECT 
    t.Name as Трек,
    al.Title as Альбом,
    ar.Name as Исполнитель,
    g.Name as Жанр,
    t.UnitPrice as Цена
FROM Track t
JOIN Album al ON t.AlbumId = al.AlbumId
JOIN Artist ar ON al.ArtistId = ar.ArtistId
JOIN Genre g ON t.GenreId = g.GenreId
ORDER BY t.UnitPrice DESC
LIMIT 15;

-- ==========================================
-- 5. АНАЛИЗ КЛИЕНТОВ
-- ==========================================

-- Географическое распределение клиентов
SELECT 
    Country as Страна,
    COUNT(*) as КоличествоКлиентов,
    COUNT(DISTINCT City) as КоличествоГородов,
    ROUND(AVG(Total), 2) as СреднийЧек
FROM Customer c
JOIN Invoice i ON c.CustomerId = i.CustomerId
GROUP BY Country
ORDER BY КоличествоКлиентов DESC;

-- Топ-10 клиентов по тратам
SELECT 
    c.FirstName || ' ' || c.LastName as Клиент,
    c.Country as Страна,
    c.City as Город,
    COUNT(i.InvoiceId) as КоличествоПокупок,
    ROUND(SUM(i.Total), 2) as ОбщаяСумма,
    ROUND(AVG(i.Total), 2) as СреднийЧек
FROM Customer c
JOIN Invoice i ON c.CustomerId = i.CustomerId
GROUP BY c.CustomerId
ORDER BY ОбщаяСумма DESC
LIMIT 10;

-- Активные клиенты (покупали в последние 6 месяцев)
SELECT 
    c.FirstName || ' ' || c.LastName as Клиент,
    c.Country as Страна,
    MAX(i.InvoiceDate) as ПоследняяПокупка,
    COUNT(i.InvoiceId) as ВсегоПокупок,
    ROUND(SUM(i.Total), 2) as ОбщаяСумма
FROM Customer c
JOIN Invoice i ON c.CustomerId = i.CustomerId
WHERE i.InvoiceDate >= date('now', '-6 months')
GROUP BY c.CustomerId
ORDER BY ОбщаяСумма DESC;

-- ==========================================
-- 6. АНАЛИЗ ПРОДАЖ
-- ==========================================

-- Продажи по периодам
SELECT 
    strftime('%Y', InvoiceDate) as Год,
    COUNT(*) as КоличествоСчетов,
    COUNT(DISTINCT CustomerId) as УникальныхКлиентов,
    ROUND(SUM(Total), 2) as ОбщаяСумма,
    ROUND(AVG(Total), 2) as СреднийЧек
FROM Invoice
GROUP BY strftime('%Y', InvoiceDate)
ORDER BY Год DESC;

-- Месячная динамика продаж
SELECT 
    strftime('%Y-%m', InvoiceDate) as Месяц,
    COUNT(*) as КоличествоСчетов,
    ROUND(SUM(Total), 2) as ОбщаяСумма,
    ROUND(AVG(Total), 2) as СреднийЧек
FROM Invoice
GROUP BY strftime('%Y-%m', InvoiceDate)
ORDER BY Месяц DESC
LIMIT 24;

-- Сезонность продаж
SELECT 
    CASE strftime('%m', InvoiceDate)
        WHEN '12' THEN 'Зима'
        WHEN '01' THEN 'Зима'
        WHEN '02' THEN 'Зима'
        WHEN '03' THEN 'Весна'
        WHEN '04' THEN 'Весна'
        WHEN '05' THEN 'Весна'
        WHEN '06' THEN 'Лето'
        WHEN '07' THEN 'Лето'
        WHEN '08' THEN 'Лето'
        ELSE 'Осень'
    END as Сезон,
    COUNT(*) as КоличествоСчетов,
    ROUND(SUM(Total), 2) as ОбщаяСумма
FROM Invoice
GROUP BY 
    CASE strftime('%m', InvoiceDate)
        WHEN '12' THEN 'Зима'
        WHEN '01' THEN 'Зима'
        WHEN '02' THEN 'Зима'
        WHEN '03' THEN 'Весна'
        WHEN '04' THEN 'Весна'
        WHEN '05' THEN 'Весна'
        WHEN '06' THEN 'Лето'
        WHEN '07' THEN 'Лето'
        WHEN '08' THEN 'Лето'
        ELSE 'Осень'
    END
ORDER BY ОбщаяСумма DESC;

-- ==========================================
-- 7. АНАЛИЗ ПОПУЛЯРНОСТИ
-- ==========================================

-- Самые продаваемые треки
SELECT 
    t.Name as Трек,
    al.Title as Альбом,
    ar.Name as Исполнитель,
    g.Name as Жанр,
    COUNT(il.InvoiceLineId) as КоличествоПродаж,
    SUM(il.Quantity) as ОбщееКоличество,
    ROUND(SUM(il.UnitPrice * il.Quantity), 2) as ОбщаяВыручка
FROM Track t
JOIN Album al ON t.AlbumId = al.AlbumId
JOIN Artist ar ON al.ArtistId = ar.ArtistId
JOIN Genre g ON t.GenreId = g.GenreId
JOIN InvoiceLine il ON t.TrackId = il.TrackId
GROUP BY t.TrackId
ORDER BY ОбщаяВыручка DESC
LIMIT 15;

-- Самые популярные альбомы
SELECT 
    al.Title as Альбом,
    ar.Name as Исполнитель,
    COUNT(DISTINCT il.InvoiceId) as КоличествоПокупок,
    SUM(il.Quantity) as ОбщееКоличество,
    ROUND(SUM(il.UnitPrice * il.Quantity), 2) as ОбщаяВыручка
FROM Album al
JOIN Artist ar ON al.ArtistId = ar.ArtistId
JOIN Track t ON al.AlbumId = t.AlbumId
JOIN InvoiceLine il ON t.TrackId = il.TrackId
GROUP BY al.AlbumId
ORDER BY ОбщаяВыручка DESC
LIMIT 10;

-- Топ-10 исполнителей по выручке
SELECT 
    ar.Name as Исполнитель,
    COUNT(DISTINCT al.AlbumId) as КоличествоАльбомов,
    COUNT(DISTINCT t.TrackId) as КоличествоТреков,
    SUM(il.Quantity) as ОбщееКоличество,
    ROUND(SUM(il.UnitPrice * il.Quantity), 2) as ОбщаяВыручка
FROM Artist ar
JOIN Album al ON ar.ArtistId = al.ArtistId
JOIN Track t ON al.AlbumId = t.AlbumId
JOIN InvoiceLine il ON t.TrackId = il.TrackId
GROUP BY ar.ArtistId
ORDER BY ОбщаяВыручка DESC
LIMIT 10;

-- ==========================================
-- 8. АНАЛИЗ ПЛЕЙЛИСТОВ
-- ==========================================

-- Статистика плейлистов
SELECT 
    p.Name as Плейлист,
    COUNT(pt.TrackId) as КоличествоТреков,
    ROUND(AVG(t.UnitPrice), 2) as СредняяЦена,
    ROUND(SUM(t.UnitPrice), 2) as ОбщаяСтоимость
FROM Playlist p
JOIN PlaylistTrack pt ON p.PlaylistId = pt.PlaylistId
JOIN Track t ON pt.TrackId = t.TrackId
GROUP BY p.PlaylistId
ORDER BY КоличествоТреков DESC;

-- Треки в нескольких плейлистах
SELECT 
    t.Name as Трек,
    al.Title as Альбом,
    ar.Name as Исполнитель,
    COUNT(pt.PlaylistId) as КоличествоПлейлистов
FROM Track t
JOIN Album al ON t.AlbumId = al.AlbumId
JOIN Artist ar ON al.ArtistId = ar.ArtistId
JOIN PlaylistTrack pt ON t.TrackId = pt.TrackId
GROUP BY t.TrackId
HAVING COUNT(pt.PlaylistId) > 5
ORDER BY КоличествоПлейлистов DESC
LIMIT 20;

-- ==========================================
-- 9. КОМПЛЕКСНЫЙ АНАЛИЗ
-- ==========================================

-- RFM-анализ клиентов (Recency, Frequency, Monetary)
WITH CustomerMetrics AS (
    SELECT 
        c.CustomerId,
        c.FirstName || ' ' || c.LastName as Клиент,
        julianday('now') - julianday(MAX(i.InvoiceDate)) as Давность_дней,
        COUNT(i.InvoiceId) as Частота_покупок,
        SUM(i.Total) as Денежная_ценность
    FROM Customer c
    JOIN Invoice i ON c.CustomerId = i.CustomerId
    GROUP BY c.CustomerId
)
SELECT 
    Клиент,
    Давность_дней,
    Частота_покупок,
    Денежная_ценность,
    CASE 
        WHEN Давность_дней <= 30 THEN 'Высокая'
        WHEN Давность_дней <= 90 THEN 'Средняя'
        ELSE 'Низкая'
    END as Категория_давности,
    CASE 
        WHEN Частота_покупок >= 10 THEN 'Высокая'
        WHEN Частота_покупок >= 5 THEN 'Средняя'
        ELSE 'Низкая'
    END as Категория_частоты,
    CASE 
        WHEN Денежная_ценность >= 100 THEN 'Высокая'
        WHEN Денежная_ценность >= 50 THEN 'Средняя'
        ELSE 'Низкая'
    END as Категория_ценности
FROM CustomerMetrics
ORDER BY Денежная_ценность DESC;

-- Анализ прибыльности по жанрам
SELECT 
    g.Name as Жанр,
    COUNT(t.TrackId) as КоличествоТреков,
    COUNT(il.InvoiceLineId) as КоличествоПродаж,
    ROUND(SUM(il.UnitPrice * il.Quantity), 2) as ОбщаяВыручка,
    ROUND(AVG(il.UnitPrice), 2) as СредняяЦенаПродажи,
    ROUND(SUM(il.UnitPrice * il.Quantity) / COUNT(t.TrackId), 2) as ВыручкаНаТрек
FROM Genre g
JOIN Track t ON g.GenreId = t.GenreId
JOIN InvoiceLine il ON t.TrackId = il.TrackId
GROUP BY g.GenreId
ORDER BY ВыручкаНаТрек DESC;

-- ==========================================
-- 10. БИЗНЕС-РЕКОМЕНДАЦИИ
-- ==========================================

-- Продукты для продвижения (высокая цена, низкие продажи)
SELECT 
    t.Name as Трек,
    al.Title as Альбом,
    ar.Name as Исполнитель,
    t.UnitPrice as Цена,
    COUNT(il.InvoiceLineId) as КоличествоПродаж
FROM Track t
JOIN Album al ON t.AlbumId = al.AlbumId
JOIN Artist ar ON al.ArtistId = ar.ArtistId
LEFT JOIN InvoiceLine il ON t.TrackId = il.TrackId
WHERE t.UnitPrice > (SELECT AVG(UnitPrice) FROM Track)
GROUP BY t.TrackId
HAVING COUNT(il.InvoiceLineId) < (SELECT AVG(КоличествоПродаж) FROM (
    SELECT COUNT(InvoiceLineId) as КоличествоПродаж
    FROM InvoiceLine
    GROUP BY TrackId
))
ORDER BY t.UnitPrice DESC, КоличествоПродаж ASC
LIMIT 10;

-- Потенциальные проблемы (низкие продажи)
SELECT 
    t.Name as Трек,
    al.Title as Альбом,
    ar.Name as Исполнитель,
    COUNT(il.InvoiceLineId) as КоличествоПродаж
FROM Track t
JOIN Album al ON t.AlbumId = al.AlbumId
JOIN Artist ar ON al.ArtistId = ar.ArtistId
LEFT JOIN InvoiceLine il ON t.TrackId = il.TrackId
GROUP BY t.TrackId
HAVING COUNT(il.InvoiceLineId) = 0
ORDER BY al.Title;

-- Анализ сезонных предложений
-- SELECT 
--     strftime('%m', InvoiceDate) as Месяц,
--     g.Name as Жанр,
--     COUNT(il.InvoiceLineId) as Продажи,
--     ROUND(SUM(il.UnitPrice * il.Quantity), 2) as Выручка
-- FROM Invoice i
-- JOIN InvoiceLine il ON i.InvoiceId = il.InvoiceId
-- JOIN Track t ON il.TrackId = t.TrackId
-- JOIN Genre g ON t.GenreId = g.GenreId
-- WHERE strftime('%Y', InvoiceDate) = '2021'
-- GROUP BY strftime('%m', InvoiceDate), g.GenreId
-- ORDER BY Месяц, Выручка DESC;