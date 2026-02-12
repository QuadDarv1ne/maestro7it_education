/* Write your T-SQL query statement below */
SELECT 
    u.name,
    SUM(t.amount) AS balance
FROM 
    Users u
    INNER JOIN Transactions t ON u.account = t.account
GROUP BY 
    u.account, u.name
HAVING 
    SUM(t.amount) > 10000;