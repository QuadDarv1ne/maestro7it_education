/* Write your PL/SQL query statement below */
SELECT employee_id
FROM Employees
FULL OUTER JOIN Salaries USING (employee_id)
WHERE name IS NULL OR salary IS NULL
ORDER BY employee_id;