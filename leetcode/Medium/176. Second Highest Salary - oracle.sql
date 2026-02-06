-- Решение 1: Базовый подход
SELECT MAX(salary) AS SecondHighestSalary
FROM Employee
WHERE salary < (SELECT MAX(salary) FROM Employee);

-- Решение 2: С ROWNUM
SELECT 
    (SELECT MAX(salary) 
     FROM (SELECT DISTINCT salary 
           FROM Employee 
           ORDER BY salary DESC)
     WHERE ROWNUM = 2) AS SecondHighestSalary
FROM DUAL;

-- Решение 3: С FETCH FIRST (Oracle 12c+)
SELECT 
    NVL(
        (SELECT DISTINCT salary
         FROM Employee
         ORDER BY salary DESC
         OFFSET 1 ROW FETCH NEXT 1 ROW ONLY),
        NULL
    ) AS SecondHighestSalary
FROM DUAL;