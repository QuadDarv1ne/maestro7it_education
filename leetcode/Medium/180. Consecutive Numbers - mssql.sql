/* Write your T-SQL query statement below */
WITH Consecutive AS (
    SELECT 
        num,
        LAG(num, 1) OVER (ORDER BY id) AS prev1,
        LAG(num, 2) OVER (ORDER BY id) AS prev2
    FROM Logs
)
SELECT DISTINCT num AS ConsecutiveNums
FROM Consecutive
WHERE num = prev1 AND num = prev2;