/* Write your T-SQL query statement below */
SELECT 
    t.user_id,
    ROUND(t.trial_avg, 2) AS trial_avg_duration,
    ROUND(p.paid_avg, 2) AS paid_avg_duration
FROM (
    SELECT 
        ua.user_id,
        AVG(ua.activity_duration * 1.0) AS trial_avg
    FROM UserActivity ua
    WHERE ua.activity_type = 'free_trial'
      AND EXISTS (
          SELECT 1 
          FROM UserActivity p 
          WHERE p.user_id = ua.user_id 
            AND p.activity_type = 'paid'
      )
      AND ua.activity_date < (
          SELECT MIN(activity_date)
          FROM UserActivity fp
          WHERE fp.user_id = ua.user_id 
            AND fp.activity_type = 'paid'
      )
    GROUP BY ua.user_id
) t
INNER JOIN (
    SELECT 
        ua.user_id,
        AVG(ua.activity_duration * 1.0) AS paid_avg
    FROM UserActivity ua
    WHERE ua.activity_type = 'paid'
      AND EXISTS (
          SELECT 1 
          FROM UserActivity p 
          WHERE p.user_id = ua.user_id 
            AND p.activity_type = 'paid'
      )
      AND ua.activity_date >= (
          SELECT MIN(activity_date)
          FROM UserActivity fp
          WHERE fp.user_id = ua.user_id 
            AND fp.activity_type = 'paid'
      )
    GROUP BY ua.user_id
) p ON t.user_id = p.user_id
ORDER BY t.user_id;