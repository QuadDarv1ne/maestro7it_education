/* Write your PL/SQL query statement below */
-- ✅ Решение для Oracle (работает во всех версиях, включая 11g и старше)
-- Используем ROWNUM вместо FETCH FIRST, так как FETCH FIRST может вызывать ORA-00933
-- в некоторых окружениях или при неправильном синтаксисе.

-- 1. Пользователь с максимальным количеством оценок
SELECT name AS results
FROM (
    SELECT 
        u.name,
        COUNT(*) AS cnt
    FROM 
        Users u
        JOIN MovieRating mr ON u.user_id = mr.user_id
    GROUP BY 
        u.user_id, u.name
    ORDER BY 
        cnt DESC, 
        u.name ASC
)
WHERE ROWNUM = 1

UNION ALL

-- 2. Фильм с наивысшим средним рейтингом в феврале 2020
SELECT title AS results
FROM (
    SELECT 
        m.title,
        AVG(mr.rating) AS avg_rating
    FROM 
        Movies m
        JOIN MovieRating mr ON m.movie_id = mr.movie_id
    WHERE 
        EXTRACT(YEAR FROM mr.created_at) = 2020 
        AND EXTRACT(MONTH FROM mr.created_at) = 2
    GROUP BY 
        m.movie_id, m.title
    ORDER BY 
        avg_rating DESC, 
        m.title ASC
)
WHERE ROWNUM = 1;