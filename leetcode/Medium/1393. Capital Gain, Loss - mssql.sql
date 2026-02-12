/* Write your T-SQL query statement below */
-- Синтаксис полностью аналогичен MySQL
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