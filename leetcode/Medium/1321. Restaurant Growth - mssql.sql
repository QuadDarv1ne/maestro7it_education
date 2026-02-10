/* Write your T-SQL query statement below */
WITH DailyRevenue AS (
    -- 1. Суммируем выручку по каждому дню
    SELECT 
        visited_on,
        SUM(amount) AS daily_amount
    FROM Customer
    GROUP BY visited_on
),
MovingTotals AS (
    -- 2. Вычисляем скользящие суммы и средние
    SELECT 
        visited_on,
        -- Сумма за 7 дней (текущий день + 6 предыдущих)
        SUM(daily_amount) OVER (
            ORDER BY visited_on 
            ROWS BETWEEN 6 PRECEDING AND CURRENT ROW
        ) AS amount,
        -- Среднее за 7 дней с округлением
        ROUND(
            AVG(daily_amount * 1.0) OVER (
                ORDER BY visited_on 
                ROWS BETWEEN 6 PRECEDING AND CURRENT ROW
            ), 
            2
        ) AS average_amount,
        -- Номер строки для фильтрации первых 6 дней
        ROW_NUMBER() OVER (ORDER BY visited_on) AS row_num
    FROM DailyRevenue
)
-- 3. Отбираем только строки, начиная с 7-го дня
SELECT 
    visited_on,
    amount,
    average_amount
FROM MovingTotals
WHERE row_num >= 7  -- Пропускаем первые 6 дней
ORDER BY visited_on;