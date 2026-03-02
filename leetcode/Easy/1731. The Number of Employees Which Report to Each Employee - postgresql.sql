-- PostgreSQL решение
SELECT 
    e1.employee_id,
    e1.name,
    COUNT(e2.employee_id) AS reports_count,
    ROUND(AVG(e2.age)) AS average_age   -- AVG от целых чисел возвращает numeric, ROUND округляет
FROM 
    Employees e1
INNER JOIN 
    Employees e2 ON e1.employee_id = e2.reports_to
GROUP BY 
    e1.employee_id, e1.name
ORDER BY 
    e1.employee_id;