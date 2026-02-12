# Write your MySQL query statement below
-- Решение задачи 1341. Movie Rating
-- 
-- Найти:
-- 1. Имя пользователя, который оценил наибольшее количество фильмов.
--    При равенстве — лексикографически меньшее имя.
-- 2. Название фильма с наивысшим средним рейтингом в феврале 2020.
--    При равенстве — лексикографически меньшее название.
--
-- Алгоритм:
--   - Два независимых запроса, объединённых через UNION ALL.
--   - В первом: группировка по user_id, сортировка по COUNT(*) DESC, name ASC.
--   - Во втором: фильтр по дате, группировка по movie_id, 
--     сортировка по AVG(rating) DESC, title ASC.
--   - Используем UNION ALL, чтобы сохранить обе строки даже при совпадении значений.

(
    SELECT 
        u.name AS results
    FROM 
        Users u
        INNER JOIN MovieRating mr ON u.user_id = mr.user_id
    GROUP BY 
        u.user_id, u.name
    ORDER BY 
        COUNT(*) DESC,          -- сначала по количеству оценок (убывание)
        u.name ASC              -- при равенстве — лексикографически меньшее имя
    LIMIT 1
)

UNION ALL

(
    SELECT 
        m.title AS results
    FROM 
        Movies m
        INNER JOIN MovieRating mr ON m.movie_id = mr.movie_id
    WHERE 
        mr.created_at BETWEEN '2020-02-01' AND '2020-02-29'
    GROUP BY 
        m.movie_id, m.title
    ORDER BY 
        AVG(mr.rating) DESC,    -- сначала по среднему рейтингу (убывание)
        m.title ASC             -- при равенстве — лексикографически меньшее название
    LIMIT 1
);