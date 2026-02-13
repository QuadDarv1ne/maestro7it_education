/* Write your PL/SQL query statement below */
SELECT 
    ua1.user_id,
    ROUND(AVG(CASE WHEN ua1.activity_type = 'free_trial' THEN ua1.activity_duration END), 2) AS trial_avg_duration,
    ROUND(AVG(CASE WHEN ua1.activity_type = 'paid' THEN ua1.activity_duration END), 2) AS paid_avg_duration
FROM 
    UserActivity ua1
WHERE 
    EXISTS (
        SELECT 1 
        FROM UserActivity ua2 
        WHERE ua2.user_id = ua1.user_id 
          AND ua2.activity_type = 'paid'
    )
GROUP BY 
    ua1.user_id
HAVING 
    COUNT(DISTINCT CASE WHEN ua1.activity_type = 'free_trial' THEN ua1.activity_date END) > 0
ORDER BY 
    ua1.user_id;