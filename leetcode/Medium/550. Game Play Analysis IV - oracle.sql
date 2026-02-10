/* Write your PL/SQL query statement below */
WITH FirstLogin AS (
    SELECT 
        player_id,
        MIN(event_date) AS first_login_date
    FROM Activity
    GROUP BY player_id
),
NextDayLogins AS (
    SELECT 
        a.player_id
    FROM Activity a
    JOIN FirstLogin f 
        ON a.player_id = f.player_id 
        AND a.event_date = f.first_login_date + 1
)
SELECT 
    ROUND(
        (SELECT COUNT(DISTINCT player_id) FROM NextDayLogins) * 1.0 / 
        (SELECT COUNT(DISTINCT player_id) FROM Activity),
        2
    ) AS fraction
FROM DUAL;