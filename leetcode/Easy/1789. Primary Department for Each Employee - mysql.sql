# Write your MySQL query statement below
WITH ranked AS (
    SELECT 
        employee_id,
        department_id,
        primary_flag,
        COUNT(*) OVER (PARTITION BY employee_id) AS dept_count,
        SUM(CASE WHEN primary_flag = 'Y' THEN 1 ELSE 0 END) OVER (PARTITION BY employee_id) AS y_count
    FROM Employee
)

SELECT 
    employee_id,
    department_id
FROM ranked
WHERE 
    -- случай 1: есть primary_flag = 'Y'
    (y_count = 1 AND primary_flag = 'Y')
    OR
    -- случай 2: нет Y, но всего один департамент
    (y_count = 0 AND dept_count = 1)
ORDER BY employee_id;