-- Write your PostgreSQL query statement below
-- Особенности: LIMIT, явное приведение типов для AVG, UNION ALL

(
    SELECT 
        u.name AS results
    FROM 
        Users u
        JOIN MovieRating mr ON u.user_id = mr.user_id
    GROUP BY 
        u.user_id, u.name
    ORDER BY 
        COUNT(*) DESC,          -- сначала по количеству оценок (убывание)
        u.name ASC              -- при равенстве — лексикографически
    LIMIT 1
)

UNION ALL

(
    SELECT 
        m.title AS results
    FROM 
        Movies m
        JOIN MovieRating mr ON m.movie_id = mr.movie_id
    WHERE 
        mr.created_at >= '2020-02-01' 
        AND mr.created_at < '2020-03-01'   -- весь февраль 2020
    GROUP BY 
        m.movie_id, m.title
    ORDER BY 
        AVG(mr.rating) DESC,    -- сначала по среднему рейтингу
        m.title ASC
    LIMIT 1
);