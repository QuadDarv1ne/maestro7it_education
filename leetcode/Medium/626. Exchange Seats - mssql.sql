/* Write your T-SQL query statement below */
SELECT 
    CASE
        WHEN id % 2 = 0 THEN id - 1  -- Чётный ID: меняемся с предыдущим
        WHEN id % 2 = 1 AND id < (SELECT MAX(id) FROM Seat) THEN id + 1  -- Нечётный и не последний: меняемся со следующим
        ELSE id  -- Последний нечётный ID: остаётся на месте
    END AS id,
    student
FROM Seat
ORDER BY id;