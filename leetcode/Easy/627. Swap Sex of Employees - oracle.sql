/* Write your PL/SQL query statement below */
-- Вариант 1: Оператор UPDATE с CASE (или DECODE)
UPDATE Salary
SET sex = CASE sex
            WHEN 'f' THEN 'm'
            WHEN 'm' THEN 'f'
            ELSE sex
          END;

-- Вариант 2: SELECT для получения результата
-- SELECT id, name, CASE sex
--                    WHEN 'f' THEN 'm'
--                    WHEN 'm' THEN 'f'
--                  END AS sex,
--        salary
-- FROM Salary;