/* Write your T-SQL query statement below */
-- Вариант 1: Оператор UPDATE с IIF
UPDATE Salary
SET sex = IIF(sex = 'm', 'f', 'm');

-- Вариант 2: SELECT для получения результата
SELECT id, name, IIF(sex = 'm', 'f', 'm') AS sex, salary
FROM Salary;