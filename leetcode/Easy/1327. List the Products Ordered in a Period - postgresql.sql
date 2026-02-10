-- Write your PostgreSQL query statement below
SELECT 
    p.product_name,
    SUM(o.unit) AS unit
FROM 
    Products p
INNER JOIN 
    Orders o ON p.product_id = o.product_id
WHERE 
    -- Альтернативный вариант фильтрации дат
    o.order_date BETWEEN '2020-02-01' AND '2020-02-29'
GROUP BY 
    p.product_id, p.product_name
HAVING 
    SUM(o.unit) >= 100
ORDER BY 
    unit DESC;