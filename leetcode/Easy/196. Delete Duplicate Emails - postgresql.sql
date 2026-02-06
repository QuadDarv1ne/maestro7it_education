-- Write your PostgreSQL query statement below
DELETE FROM Person p1
WHERE EXISTS (
    SELECT 1 FROM Person p2
    WHERE p2.Email = p1.Email AND p2.Id < p1.Id
);