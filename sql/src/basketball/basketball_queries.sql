-- Запросы к базе данных Basketball
-- База данных спортивной аналитики с командами, игроками, играми, статистикой

-- 1. Базовое исследование таблиц
SELECT name AS table_name
FROM sqlite_master 
WHERE type = 'table';

-- 2. Получить схему базы данных для таблицы Team
PRAGMA table_info(Team);

-- 3. Простое исследование данных
SELECT * FROM Team LIMIT 5;
SELECT * FROM Player LIMIT 5;
SELECT * FROM Game LIMIT 5;

-- 4. Найти команды, основанные после 2000 года
SELECT 
    full_name,
    abbreviation,
    year_founded
FROM Team
WHERE year_founded > 2000
ORDER BY year_founded;

-- 5. Команды по конференциям
SELECT 
    conference,
    COUNT(*) AS team_count
FROM Team
GROUP BY conference
ORDER BY team_count DESC;

-- 6. Игроки с конкретной позицией
SELECT 
    p.name,
    p.team_abbreviation,
    p.position,
    p.height,
    p.weight
FROM Player p
WHERE p.position = 'PG'  -- Point Guard
ORDER BY p.name;

-- 7. Статистика игроков за конкретный сезон
SELECT 
    p.name,
    p.team_abbreviation,
    ps.pts AS points_per_game,
    ps.ast AS assists_per_game,
    ps.reb AS rebounds_per_game,
    ps.fg_pct AS field_goal_percentage
FROM Player p
JOIN PlayerStats ps ON p.player_id = ps.player_id
WHERE ps.season = 2022
ORDER BY ps.pts DESC
LIMIT 10;

-- 8. Рекорд побед-поражений команды
SELECT 
    t.full_name,
    SUM(CASE WHEN g.home_team_id = t.team_id AND g.home_team_score > g.visitor_team_score THEN 1
             WHEN g.visitor_team_id = t.team_id AND g.visitor_team_score > g.home_team_score THEN 1
             ELSE 0 END) AS wins,
    SUM(CASE WHEN g.home_team_id = t.team_id AND g.home_team_score < g.visitor_team_score THEN 1
             WHEN g.visitor_team_id = t.team_id AND g.visitor_team_score < g.home_team_score THEN 1
             ELSE 0 END) AS losses
FROM Team t
JOIN Game g ON t.team_id = g.home_team_id OR t.team_id = g.visitor_team_id
WHERE strftime('%Y', g.date_game) = '2022'
GROUP BY t.team_id
ORDER BY wins DESC;

-- 9. Лучшие бомбардиры по командам
SELECT 
    t.full_name AS team,
    p.name AS player,
    ps.pts AS points_per_game
FROM Player p
JOIN PlayerStats ps ON p.player_id = ps.player_id
JOIN Team t ON p.team_id = t.team_id
WHERE ps.season = 2022
ORDER BY ps.pts DESC
LIMIT 15;

-- 10. Статистика посещаемости игр
SELECT 
    AVG(attendance) AS avg_attendance,
    MAX(attendance) AS max_attendance,
    MIN(attendance) AS min_attendance
FROM Game
WHERE strftime('%Y', date_game) = '2022';