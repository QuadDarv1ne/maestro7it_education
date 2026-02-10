/* Write your PL/SQL query statement below */
WITH unique_nums AS (
    SELECT num
    FROM MyNumbers
    GROUP BY num
    HAVING COUNT(*) = 1
)
SELECT MAX(num) AS num
FROM unique_nums;