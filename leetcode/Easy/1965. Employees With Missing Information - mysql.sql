# Write your MySQL query statement below
SELECT employee_id
FROM Employees
LEFT JOIN Salaries USING (employee_id)
WHERE name IS NULL OR salary IS NULL

UNION

SELECT employee_id
FROM Employees
RIGHT JOIN Salaries USING (employee_id)
WHERE name IS NULL OR salary IS NULL

ORDER BY employee_id;