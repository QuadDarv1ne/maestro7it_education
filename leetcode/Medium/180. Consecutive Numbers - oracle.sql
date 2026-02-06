WITH Numbered AS (
    SELECT 
        num,
        id,
        ROW_NUMBER() OVER (ORDER BY id) AS rn,
        id - ROW_NUMBER() OVER (PARTITION BY num ORDER BY id) AS diff
    FROM Logs
),
Grouped AS (
    SELECT 
        num,
        diff,
        COUNT(*) AS cnt,
        MIN(id) AS start_id,
        MAX(id) AS end_id
    FROM Numbered
    GROUP BY num, diff
    HAVING COUNT(*) >= 3
)
SELECT DISTINCT num AS "ConsecutiveNums"
FROM Grouped
ORDER BY num;