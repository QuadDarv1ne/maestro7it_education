-- Write your PostgreSQL query statement below
-- Вариант 1: Оператор UPDATE
UPDATE Salary
SET sex = CASE
            WHEN sex = 'f' THEN 'm'
            ELSE 'f'
          END;

-- Вариант 2: SELECT для получения результата
SELECT id, name,
       CASE
         WHEN sex = 'f' THEN 'm'
         ELSE 'f'
       END AS sex,
       salary
FROM Salary;