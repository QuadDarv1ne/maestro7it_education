/* Write your PL/SQL query statement below */
SELECT 
    player_id,
    TO_CHAR(MIN(event_date), 'YYYY-MM-DD') AS first_login
FROM 
    Activity
GROUP BY 
    player_id;