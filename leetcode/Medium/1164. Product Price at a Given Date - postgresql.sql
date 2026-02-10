-- Write your PostgreSQL query statement below
WITH LastPrice AS (
    SELECT DISTINCT product_id,
           FIRST_VALUE(new_price) OVER (
               PARTITION BY product_id 
               ORDER BY change_date DESC
           ) AS price
    FROM Products
    WHERE change_date <= '2019-08-16'
)
SELECT product_id, COALESCE(price, 10) AS price
FROM LastPrice
UNION ALL
SELECT DISTINCT product_id, 10
FROM Products
WHERE product_id NOT IN (SELECT product_id FROM LastPrice)
ORDER BY product_id;