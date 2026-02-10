-- Write your PostgreSQL query statement below
WITH DailyRevenue AS (
    SELECT visited_on, SUM(amount) AS daily_amount
    FROM Customer
    GROUP BY visited_on
),
MovingTotals AS (
    SELECT 
        visited_on,
        SUM(daily_amount) OVER (ORDER BY visited_on ROWS BETWEEN 6 PRECEDING AND CURRENT ROW) AS amount,
        ROUND(AVG(daily_amount) OVER (ORDER BY visited_on ROWS BETWEEN 6 PRECEDING AND CURRENT ROW)::NUMERIC, 2) AS average_amount,
        ROW_NUMBER() OVER (ORDER BY visited_on) AS rn
    FROM DailyRevenue
)
SELECT visited_on, amount, average_amount
FROM MovingTotals
WHERE rn >= 7
ORDER BY visited_on;