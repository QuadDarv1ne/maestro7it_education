/* Write your T-SQL query statement below */
WITH CTE AS (
    SELECT Id, Email,
    ROW_NUMBER() OVER (PARTITION BY Email ORDER BY Id) AS rn
    FROM Person
)
DELETE FROM CTE WHERE rn > 1;