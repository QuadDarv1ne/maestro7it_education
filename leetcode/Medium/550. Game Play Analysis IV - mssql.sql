/* Write your T-SQL query statement below */
WITH FirstLogin AS (
    SELECT 
        player_id,
        MIN(event_date) AS first_login_date
    FROM Activity
    GROUP BY player_id
)
SELECT 
    CAST(
        ROUND(
            CAST(COUNT(DISTINCT a.player_id) AS FLOAT) / 
            (SELECT COUNT(DISTINCT player_id) FROM Activity),
            2
        ) AS DECIMAL(10, 2)
    ) AS fraction
FROM Activity a
JOIN FirstLogin f 
    ON a.player_id = f.player_id 
    AND DATEDIFF(DAY, f.first_login_date, a.event_date) = 1;