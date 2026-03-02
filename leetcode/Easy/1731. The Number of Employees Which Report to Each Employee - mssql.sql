-- MSSQL решение
-- Примечание: чтобы избежать целочисленного деления при расчёте среднего, умножаем age на 1.0
SELECT 
    e1.employee_id,
    e1.name,
    COUNT(e2.employee_id) AS reports_count,
    ROUND(AVG(e2.age * 1.0), 0) AS average_age   -- округление до ближайшего целого (0 десятичных знаков)
FROM 
    Employees e1
INNER JOIN 
    Employees e2 ON e1.employee_id = e2.reports_to
GROUP BY 
    e1.employee_id, e1.name
ORDER BY 
    e1.employee_id;