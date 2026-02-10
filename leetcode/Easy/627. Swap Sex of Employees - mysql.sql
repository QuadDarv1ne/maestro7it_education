# Write your MySQL query statement below
-- Вариант 1: Оператор UPDATE
UPDATE Salary
SET sex = IF(sex = 'f', 'm', 'f');

-- Вариант 2: SELECT для получения результата (может потребоваться для прохождения теста)
-- SELECT id, name, IF(sex = 'f', 'm', 'f') AS sex, salary
-- FROM Salary;