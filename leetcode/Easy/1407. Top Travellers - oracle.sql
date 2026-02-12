/* Write your PL/SQL query statement below */
-- NVL заменяет NULL на 0
SELECT 
    u.name,
    NVL(SUM(r.distance), 0) AS travelled_distance
FROM 
    Users u
    LEFT JOIN Rides r ON u.id = r.user_id
GROUP BY 
    u.id, u.name
ORDER BY 
    travelled_distance DESC,
    u.name ASC;