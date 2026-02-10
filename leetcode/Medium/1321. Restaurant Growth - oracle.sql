/* Write your PL/SQL query statement below */
WITH DailyRevenue AS (
    SELECT 
        visited_on,
        SUM(amount) AS daily_amount
    FROM Customer
    GROUP BY visited_on
),
MovingTotals AS (
    SELECT 
        visited_on,
        -- Сумма за 7 дней
        SUM(daily_amount) OVER (
            ORDER BY visited_on 
            ROWS BETWEEN 6 PRECEDING AND CURRENT ROW
        ) AS amount,
        -- Среднее за 7 дней с округлением
        ROUND(
            AVG(daily_amount) OVER (
                ORDER BY visited_on 
                ROWS BETWEEN 6 PRECEDING AND CURRENT ROW
            ), 
            2
        ) AS average_amount,
        -- Номер строки для фильтрации
        ROW_NUMBER() OVER (ORDER BY visited_on) AS rn
    FROM DailyRevenue
)
SELECT 
    -- Форматируем дату в YYYY-MM-DD
    TO_CHAR(visited_on, 'YYYY-MM-DD') AS visited_on,
    amount,
    average_amount
FROM MovingTotals
WHERE rn >= 7
ORDER BY visited_on;