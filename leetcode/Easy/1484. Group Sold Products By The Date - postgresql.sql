-- Write your PostgreSQL query statement below
-- PostgreSQL: оптимальное решение с использованием STRING_AGG
-- 
-- Для каждой даты продажи:
--   - считаем количество уникальных товаров (COUNT DISTINCT)
--   - собираем уникальные названия товаров в строку с разделителем ','
--     в лексикографическом порядке (DISTINCT + ORDER BY внутри STRING_AGG)
-- Результат сортируем по дате.

SELECT 
    sell_date,
    COUNT(DISTINCT product) AS num_sold,                      -- количество уникальных товаров
    STRING_AGG(DISTINCT product, ',' ORDER BY product) AS products -- список товаров через запятую
FROM Activities
GROUP BY sell_date
ORDER BY sell_date;                                           -- сортировка по возрастанию даты