/* Write your T-SQL query statement below */
-- SQL Server 2017+ поддерживает STRING_AGG, но не поддерживает DISTINCT внутри неё.
-- Используем подзапрос с DISTINCT для получения уникальных продуктов по дате.
SELECT 
    sell_date,
    COUNT(DISTINCT product) AS num_sold,
    STRING_AGG(product, ',') WITHIN GROUP (ORDER BY product) AS products
FROM (
    SELECT DISTINCT sell_date, product
    FROM Activities
) AS distinct_products
GROUP BY sell_date
ORDER BY sell_date;