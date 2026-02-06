/* Write your PL/SQL query statement below */
DELETE FROM Person p1
WHERE p1.Id > (
    SELECT MIN(p2.Id)
    FROM Person p2
    WHERE p2.Email = p1.Email
);