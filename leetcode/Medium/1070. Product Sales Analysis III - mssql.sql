/* Write your T-SQL query statement below */
SELECT s.product_id, s.year AS first_year, s.quantity, s.price
FROM Sales s
INNER JOIN (
    SELECT product_id, MIN(year) AS first_year
    FROM Sales
    GROUP BY product_id
) fs ON s.product_id = fs.product_id AND s.year = fs.first_year
ORDER BY s.product_id; -- ORDER BY опционален, но помогает при проверке