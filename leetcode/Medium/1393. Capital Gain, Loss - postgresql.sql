-- Write your PostgreSQL query statement below
-- Для каждой акции суммируем цену со знаком:
--   'Sell' → +price
--   'Buy'  → –price
-- Результат: capital_gain_loss (может быть отрицательным)
SELECT 
    stock_name,
    SUM(
        CASE 
            WHEN operation = 'Sell' THEN price 
            ELSE -price 
        END
    ) AS capital_gain_loss
FROM Stocks
GROUP BY stock_name;