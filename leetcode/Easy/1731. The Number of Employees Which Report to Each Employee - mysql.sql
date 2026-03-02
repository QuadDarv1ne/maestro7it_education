-- MySQL решение
-- Используем самосоединение таблицы Employees, чтобы связать менеджеров и их подчинённых.
SELECT 
    e1.employee_id,
    e1.name,
    COUNT(e2.employee_id) AS reports_count,  -- количество подчинённых
    ROUND(AVG(e2.age)) AS average_age        -- средний возраст подчинённых, округлённый до ближайшего целого
FROM 
    Employees e1
INNER JOIN 
    Employees e2 ON e1.employee_id = e2.reports_to  -- соединяем менеджера с его прямыми подчинёнными
GROUP BY 
    e1.employee_id, e1.name
ORDER BY 
    e1.employee_id;