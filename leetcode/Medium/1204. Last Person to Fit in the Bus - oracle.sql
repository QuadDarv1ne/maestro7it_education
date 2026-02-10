/* Write your PL/SQL query statement below */
-- Способ 1: использование ROWNUM
SELECT person_name
FROM (
    SELECT 
        person_name,
        turn,
        SUM(weight) OVER (ORDER BY turn) AS cumulative_weight
    FROM Queue
    WHERE (SELECT SUM(weight) FROM Queue q2 WHERE q2.turn <= Queue.turn) <= 1000
    ORDER BY turn DESC
)
WHERE ROWNUM = 1;