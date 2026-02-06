-- Решение 1: Универсальный подход
SELECT MAX(salary) AS "SecondHighestSalary"
FROM Employee
WHERE salary < (SELECT MAX(salary) FROM Employee);

-- Решение 2: С LIMIT и OFFSET
SELECT 
    COALESCE(
        (SELECT DISTINCT salary 
         FROM Employee 
         ORDER BY salary DESC 
         LIMIT 1 OFFSET 1),
        NULL
    ) AS "SecondHighestSalary";

-- Решение 3: С оконной функцией
SELECT 
    COALESCE(
        (SELECT DISTINCT salary
         FROM (SELECT salary, DENSE_RANK() OVER (ORDER BY salary DESC) rnk
               FROM Employee) t
         WHERE rnk = 2),
        NULL
    ) AS "SecondHighestSalary";