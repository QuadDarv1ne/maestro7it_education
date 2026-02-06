-- Решение 1: Самый безопасный и совместимый (работает во всех версиях MySQL)
SELECT 
    (SELECT MAX(salary)
     FROM Employee 
     WHERE salary < (SELECT MAX(salary) FROM Employee)
    ) AS SecondHighestSalary;

-- Решение 2: С использованием IFNULL и LIMIT (MySQL 5.0+)
SELECT 
    IFNULL(
        (SELECT DISTINCT salary 
         FROM Employee 
         ORDER BY salary DESC 
         LIMIT 1, 1),
        NULL
    ) AS SecondHighestSalary;

-- Решение 3: С подзапросом в FROM
SELECT 
    (SELECT DISTINCT salary
     FROM Employee
     ORDER BY salary DESC
     LIMIT 1 OFFSET 1
    ) AS SecondHighestSalary
FROM DUAL;

-- Решение 4: Для старых версий MySQL (до 5.0)
SELECT 
    MAX(salary) AS SecondHighestSalary
FROM Employee
WHERE salary < (SELECT MAX(salary) FROM Employee);