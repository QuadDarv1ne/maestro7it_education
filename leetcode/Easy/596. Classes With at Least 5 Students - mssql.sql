/* Write your T-SQL query statement below */
SELECT class
FROM Courses
GROUP BY class
HAVING COUNT(student) >= 5;