-- Решение 1: Базовый подход
SELECT MAX(salary) AS SecondHighestSalary
FROM Employee
WHERE salary < (SELECT MAX(salary) FROM Employee);

-- Решение 2: С OFFSET-FETCH (SQL Server 2012+)
SELECT 
    ISNULL(
        (SELECT DISTINCT salary 
         FROM Employee 
         ORDER BY salary DESC 
         OFFSET 1 ROWS FETCH NEXT 1 ROWS ONLY),
        NULL
    ) AS SecondHighestSalary;

-- Решение 3: С CTE и оконной функцией
WITH RankedSalaries AS (
    SELECT salary, DENSE_RANK() OVER (ORDER BY salary DESC) as rnk
    FROM Employee
)
SELECT 
    ISNULL(
        (SELECT DISTINCT salary FROM RankedSalaries WHERE rnk = 2),
        NULL
    ) AS SecondHighestSalary;