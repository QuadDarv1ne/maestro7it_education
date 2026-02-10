/* Write your T-SQL query statement below */
WITH FilteredStadium AS (
    SELECT id, visit_date, people
    FROM Stadium
    WHERE people >= 100
),
GroupedStadium AS (
    SELECT *,
           id - ROW_NUMBER() OVER (ORDER BY id) AS grp
    FROM FilteredStadium
),
ConsecutiveGroups AS (
    SELECT *,
           COUNT(*) OVER (PARTITION BY grp) AS cnt
    FROM GroupedStadium
)
SELECT id, visit_date, people
FROM ConsecutiveGroups
WHERE cnt >= 3
ORDER BY visit_date;