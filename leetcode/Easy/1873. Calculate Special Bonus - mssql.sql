/* Write your T-SQL query statement below */
SELECT 
    employee_id,
    IIF(employee_id % 2 != 0 AND name NOT LIKE 'M%', salary, 0) AS bonus
FROM Employees
ORDER BY employee_id;