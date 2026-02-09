/* Write your PL/SQL query statement below */
SELECT 
    TO_CHAR(request_date, 'YYYY-MM-DD') AS Day,
    ROUND(
        SUM(CASE WHEN t.status IN ('cancelled_by_driver', 'cancelled_by_client') THEN 1 ELSE 0 END) / 
        COUNT(*),
        2
    ) AS "Cancellation Rate"
FROM (
    SELECT 
        t.*,
        TO_DATE(t.request_at, 'YYYY-MM-DD') AS request_date
    FROM Trips t
) t
INNER JOIN Users client ON t.client_id = client.users_id AND client.banned = 'No'
INNER JOIN Users driver ON t.driver_id = driver.users_id AND driver.banned = 'No'
WHERE t.request_date BETWEEN DATE '2013-10-01' AND DATE '2013-10-03'
GROUP BY t.request_date
ORDER BY t.request_date;