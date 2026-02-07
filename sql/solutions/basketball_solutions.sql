-- Решения упражнений по базе данных Basketball
-- Спортивная аналитика

-- Упражнение 1: Найти команды с лучшим процентом побед в 2022 году
SELECT 
    t.full_name AS Команда,
    t.abbreviation AS Аббревиатура,
    COUNT(g.game_id) AS Всего_Игр,
    SUM(CASE 
        WHEN (g.home_team_id = t.team_id AND g.home_team_score > g.visitor_team_score) OR
             (g.visitor_team_id = t.team_id AND g.visitor_team_score > g.home_team_score) 
        THEN 1 ELSE 0 END) AS Победы,
    ROUND(SUM(CASE 
        WHEN (g.home_team_id = t.team_id AND g.home_team_score > g.visitor_team_score) OR
             (g.visitor_team_id = t.team_id AND g.visitor_team_score > g.home_team_score) 
        THEN 1 ELSE 0 END) * 100.0 / COUNT(g.game_id), 1) AS Процент_Побед
FROM Team t
JOIN Game g ON t.team_id = g.home_team_id OR t.team_id = g.visitor_team_id
WHERE strftime('%Y', g.date_game) = '2022'
GROUP BY t.team_id
HAVING COUNT(g.game_id) >= 10
ORDER BY Процент_Побед DESC
LIMIT 10;

-- Упражнение 2: Топ-15 игроков по среднему количеству очков за игру в 2022 году
SELECT 
    p.name AS Игрок,
    t.full_name AS Команда,
    ps.pts AS Очки_в_среднем,
    ps.ast AS Передачи_в_среднем,
    ps.reb AS Подборы_в_среднем,
    ps.gp AS Игр_Сыграно
FROM Player p
JOIN PlayerStats ps ON p.player_id = ps.player_id
JOIN Team t ON p.team_id = t.team_id
WHERE ps.season = 2022 AND ps.gp >= 20
ORDER BY ps.pts DESC
LIMIT 15;

-- Упражнение 3: Команды по конференциям с количеством игроков
SELECT 
    t.conference AS Конференция,
    COUNT(DISTINCT t.team_id) AS Команд,
    COUNT(p.player_id) AS Игроков,
    ROUND(COUNT(p.player_id) * 1.0 / COUNT(DISTINCT t.team_id), 1) AS СреднеИгроков_на_Команду
FROM Team t
LEFT JOIN Player p ON t.team_id = p.team_id
GROUP BY t.conference
ORDER BY Команд DESC;

-- Упражнение 4: Игроки с лучшим процентом бросков с игры (минимум 30 игр)
SELECT 
    p.name AS Игрок,
    t.full_name AS Команда,
    ps.fg_pct AS Процент_Бросков,
    ps.fga AS Попыток_в_среднем,
    ps.fgm AS Попаданий_в_среднем,
    ps.gp AS Игр_Сыграно
FROM Player p
JOIN PlayerStats ps ON p.player_id = ps.player_id
JOIN Team t ON p.team_id = t.team_id
WHERE ps.season = 2022 AND ps.gp >= 30
ORDER BY ps.fg_pct DESC
LIMIT 10;

-- Упражнение 5: Анализ посещаемости по месяцам
SELECT 
    strftime('%m', g.date_game) AS Месяц,
    COUNT(*) AS Количество_Игр,
    AVG(g.attendance) AS Средняя_Посещаемость,
    MAX(g.attendance) AS Максимальная_Посещаемость,
    MIN(g.attendance) AS Минимальная_Посещаемость
FROM Game g
WHERE strftime('%Y', g.date_game) = '2022'
GROUP BY strftime('%m', g.date_game)
ORDER BY Месяц;

-- Упражнение 6: Команды с лучшей защитной статистикой (меньше очков пропущено)
SELECT 
    t.full_name AS Команда,
    COUNT(g.game_id) AS Игр_Дома,
    AVG(CASE WHEN g.home_team_id = t.team_id THEN g.visitor_team_score 
             ELSE g.home_team_score END) AS СреднеОчков_Пропущено
FROM Team t
JOIN Game g ON t.team_id = g.home_team_id OR t.team_id = g.visitor_team_id
WHERE strftime('%Y', g.date_game) = '2022'
GROUP BY t.team_id
ORDER BY СреднеОчков_Пропущено ASC
LIMIT 10;

-- Упражнение 7: Игроки с лучшим процентом трехочковых бросков
SELECT 
    p.name AS Игрок,
    t.full_name AS Команда,
    ps.three_fg_pct AS Процент_Трехочковых,
    ps.three_pa AS Попыток_Трехочковых_в_среднем,
    ps.three_pm AS Попаданий_Трехочковых_в_среднем,
    ps.gp AS Игр_Сыграно
FROM Player p
JOIN PlayerStats ps ON p.player_id = ps.player_id
JOIN Team t ON p.team_id = t.team_id
WHERE ps.season = 2022 AND ps.three_pa >= 3 AND ps.gp >= 20
ORDER BY ps.three_fg_pct DESC
LIMIT 15;

-- Упражнение 8: Сравнение домашних и выездных побед команд
SELECT 
    t.full_name AS Команда,
    SUM(CASE WHEN g.home_team_id = t.team_id AND g.home_team_score > g.visitor_team_score THEN 1 ELSE 0 END) AS Домашних_Побед,
    SUM(CASE WHEN g.visitor_team_id = t.team_id AND g.visitor_team_score > g.home_team_score THEN 1 ELSE 0 END) AS Выездных_Побед,
    SUM(CASE WHEN g.home_team_id = t.team_id THEN 1 ELSE 0 END) AS Домашних_Игр,
    SUM(CASE WHEN g.visitor_team_id = t.team_id THEN 1 ELSE 0 END) AS Выездных_Игр
FROM Team t
JOIN Game g ON t.team_id = g.home_team_id OR t.team_id = g.visitor_team_id
WHERE strftime('%Y', g.date_game) = '2022'
GROUP BY t.team_id
ORDER BY (Домашних_Побед + Выездных_Побед) DESC;

-- Упражнение 9: Игроки-новички 2022 года (меньше 2 лет в лиге)
SELECT 
    p.name AS Игрок,
    t.full_name AS Команда,
    p.position AS Позиция,
    ps.pts AS Очки_в_среднем,
    ps.ast AS Передачи_в_среднем,
    ps.reb AS Подборы_в_среднем
FROM Player p
JOIN PlayerStats ps ON p.player_id = ps.player_id
JOIN Team t ON p.team_id = t.team_id
WHERE ps.season = 2022 
    AND p.player_id NOT IN (
        SELECT DISTINCT player_id 
        FROM PlayerStats 
        WHERE season < 2022
    )
ORDER BY ps.pts DESC;

-- Упражнение 10: Команды с самой высокой зарплатой (оценка по статистике)
-- (Предполагаем, что более продуктивные команды имеют более высокую "зарплату")
SELECT 
    t.full_name AS Команда,
    SUM(ps.pts * ps.gp) AS Общий_Очковой_Вклад,
    AVG(ps.pts) AS СредниеОчки_на_Игрока,
    COUNT(DISTINCT p.player_id) AS Игроков_в_Статистике
FROM Team t
JOIN Player p ON t.team_id = p.team_id
JOIN PlayerStats ps ON p.player_id = ps.player_id
WHERE ps.season = 2022
GROUP BY t.team_id
ORDER BY Общий_Очковой_Вклад DESC
LIMIT 10;