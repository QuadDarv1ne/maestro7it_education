/* Write your PL/SQL query statement below */
-- Используем CASE внутри SUM, группировка по имени акции
SELECT 
    stock_name,
    SUM(
        CASE operation 
            WHEN 'Sell' THEN price 
            ELSE -price 
        END
    ) AS capital_gain_loss
FROM Stocks
GROUP BY stock_name;