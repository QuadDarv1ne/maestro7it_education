/* Write your PL/SQL query statement below */
SELECT 
    TO_CHAR(activity_date, 'YYYY-MM-DD') AS day, 
    COUNT(DISTINCT user_id) AS active_users
FROM Activity
WHERE activity_date BETWEEN TO_DATE('2019-07-27', 'YYYY-MM-DD') - 29 
                        AND TO_DATE('2019-07-27', 'YYYY-MM-DD')
GROUP BY activity_date
ORDER BY activity_date;