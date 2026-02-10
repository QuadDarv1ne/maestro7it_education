# Write your MySQL query statement below
SELECT 
    p.product_name,          -- Название продукта
    SUM(o.unit) AS unit      -- Общее количество за период
FROM 
    Products p                -- Основная таблица продуктов
JOIN 
    Orders o                 -- Присоединяем таблицу заказов
    ON p.product_id = o.product_id  -- Связь по product_id
WHERE 
    -- Фильтруем заказы за февраль 2020 года
    o.order_date >= '2020-02-01' 
    AND o.order_date <= '2020-02-29'
GROUP BY 
    p.product_id,            -- Группируем по продукту
    p.product_name           -- Также включаем название (для SELECT)
HAVING 
    SUM(o.unit) >= 100       -- Оставляем только товары с ≥100 единиц
ORDER BY 
    unit DESC,               -- Сначала товары с наибольшим количеством
    p.product_name ASC;      -- При равном количестве - по алфавиту