/* Write your T-SQL query statement below */
-- Решение задачи 1341. Movie Rating для Microsoft SQL Server
--
-- Найти:
-- 1. Имя пользователя, который оценил наибольшее количество фильмов.
--    При равенстве — лексикографически меньшее имя.
-- 2. Название фильма с наивысшим средним рейтингом в феврале 2020.
--    При равенстве — лексикографически меньшее название.
--
-- Особенности MSSQL:
--   - Вместо LIMIT используется TOP 1.
--   - ORDER BY допустим только внутри подзапроса с TOP (или OFFSET).
--   - Для вычисления среднего рейтинга как числа с плавающей точкой
--     необходимо явное преобразование типа (иначе AVG вернёт целое).
--   - UNION ALL сохраняет обе строки даже при одинаковых значениях.

SELECT 
    name AS results
FROM (
    SELECT TOP 1
        u.name,
        COUNT(*) AS rating_count
    FROM 
        Users u
        INNER JOIN MovieRating mr ON u.user_id = mr.user_id
    GROUP BY 
        u.user_id, u.name
    ORDER BY 
        rating_count DESC,      -- сначала по количеству оценок (убывание)
        u.name ASC              -- при равенстве — лексикографически
) AS user_winner

UNION ALL

SELECT 
    title AS results
FROM (
    SELECT TOP 1
        m.title,
        AVG(CAST(mr.rating AS FLOAT)) AS avg_rating
    FROM 
        Movies m
        INNER JOIN MovieRating mr ON m.movie_id = mr.movie_id
    WHERE 
        mr.created_at BETWEEN '2020-02-01' AND '2020-02-29'
    GROUP BY 
        m.movie_id, m.title
    ORDER BY 
        avg_rating DESC,        -- сначала по среднему рейтингу (убывание)
        m.title ASC             -- при равенстве — лексикографически
) AS movie_winner;