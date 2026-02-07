-- Шаблон проекта: Спортивная аналитика
-- Использует базу данных Basketball в качестве примера

-- ==========================================
-- 1. ИССЛЕДОВАНИЕ БАЗЫ ДАННЫХ
-- ==========================================

-- Просмотр структуры таблиц
SELECT name FROM sqlite_master WHERE type = 'table';

-- Просмотр структуры ключевых таблиц
PRAGMA table_info(Team);
PRAGMA table_info(Player);
PRAGMA table_info(PlayerStats);
PRAGMA table_info(Game);

-- ==========================================
-- 2. АНАЛИЗ КОМАНД
-- ==========================================

-- Общая статистика команд
SELECT 
    COUNT(*) as ОбщееКоличествоКоманд,
    COUNT(DISTINCT conference) as КоличествоКонференций,
    MIN(year_founded) as СамыйСтарыйГодОснования,
    MAX(year_founded) as СамыйНовыйГодОснования
FROM Team;

-- Команды по конференциям
SELECT 
    conference as Конференция,
    COUNT(*) as КоличествоКоманд,
    AVG(year_founded) as СреднийГодОснования
FROM Team
GROUP BY conference
ORDER BY КоличествоКоманд DESC;

-- Команды по годам основания
SELECT 
    year_founded as ГодОснования,
    COUNT(*) as КоличествоКоманд,
    GROUP_CONCAT(abbreviation) as Аббревиатуры
FROM Team
GROUP BY year_founded
ORDER BY year_founded;

-- ==========================================
-- 3. АНАЛИЗ ИГРОКОВ
-- ==========================================

-- Общая статистика игроков
SELECT 
    COUNT(*) as ОбщееКоличествоИгроков,
    COUNT(DISTINCT team_id) as КоличествоКоманд,
    COUNT(DISTINCT position) as КоличествоПозиций
FROM Player;

-- Игроки по позициям
SELECT 
    position as Позиция,
    COUNT(*) as КоличествоИгроков,
    COUNT(DISTINCT team_id) as КоличествоКоманд
FROM Player
GROUP BY position
ORDER BY КоличествоИгроков DESC;

-- Топ-20 игроков по росту
SELECT 
    name as Игрок,
    team_abbreviation as Команда,
    position as Позиция,
    height as Рост,
    weight as Вес
FROM Player
ORDER BY 
    CAST(SUBSTR(height, 1, INSTR(height, '-') - 1) AS INTEGER) DESC,
    CAST(SUBSTR(height, INSTR(height, '-') + 1) AS INTEGER) DESC
LIMIT 20;

-- Игроки по командам
SELECT 
    t.full_name as Команда,
    COUNT(p.player_id) as КоличествоИгроков,
    AVG(CAST(SUBSTR(p.height, 1, INSTR(p.height, '-') - 1) AS INTEGER) * 12 + 
        CAST(SUBSTR(p.height, INSTR(p.height, '-') + 1) AS INTEGER)) as СреднийРост_дюймы,
    AVG(p.weight) as СреднийВес
FROM Team t
JOIN Player p ON t.team_id = p.team_id
GROUP BY t.team_id
ORDER BY КоличествоИгроков DESC;

-- ==========================================
-- 4. АНАЛИЗ СТАТИСТИКИ ИГРОКОВ
-- ==========================================

-- Сезонная статистика (2022)
SELECT 
    COUNT(*) as ИгроковСоСтатистикой,
    AVG(gp) as СреднееКоличествоИгр,
    AVG(pts) as СредниеОчки,
    AVG(ast) as СредниеПередачи,
    AVG(reb) as СредниеПодборы
FROM PlayerStats
WHERE season = 2022;

-- Топ-25 игроков по очкам за игру (минимум 30 игр)
SELECT 
    p.name as Игрок,
    t.full_name as Команда,
    ps.pts as Очки_в_среднем,
    ps.ast as Передачи_в_среднем,
    ps.reb as Подборы_в_среднем,
    ps.gp as Игр_сыграно,
    ps.fg_pct as Процент_бросков
FROM Player p
JOIN PlayerStats ps ON p.player_id = ps.player_id
JOIN Team t ON p.team_id = t.team_id
WHERE ps.season = 2022 AND ps.gp >= 30
ORDER BY ps.pts DESC
LIMIT 25;

-- Лучшие ассистенты (минимум 20 игр)
SELECT 
    p.name as Игрок,
    t.full_name as Команда,
    ps.ast as Передачи_в_среднем,
    ps.pts as Очки_в_среднем,
    ps.gp as Игр_сыграно
FROM Player p
JOIN PlayerStats ps ON p.player_id = ps.player_id
JOIN Team t ON p.team_id = t.team_id
WHERE ps.season = 2022 AND ps.gp >= 20
ORDER BY ps.ast DESC
LIMIT 15;

-- Лучшие подбирающие (минимум 20 игр)
SELECT 
    p.name as Игрок,
    t.full_name as Команда,
    ps.reb as Подборы_в_среднем,
    ps.pts as Очки_в_среднем,
    ps.gp as Игр_сыграно
FROM Player p
JOIN PlayerStats ps ON p.player_id = ps.player_id
JOIN Team t ON p.team_id = t.team_id
WHERE ps.season = 2022 AND ps.gp >= 20
ORDER BY ps.reb DESC
LIMIT 15;

-- ==========================================
-- 5. АНАЛИЗ ЭФФЕКТИВНОСТИ
-- ==========================================

-- Игроки с лучшим процентом бросков (минимум 50 попыток)
SELECT 
    p.name as Игрок,
    t.full_name as Команда,
    ps.fg_pct as Процент_бросков,
    ps.fga as Попыток_в_среднем,
    ps.fgm as Попаданий_в_среднем,
    ps.gp as Игр_сыграно
FROM Player p
JOIN PlayerStats ps ON p.player_id = ps.player_id
JOIN Team t ON p.team_id = t.team_id
WHERE ps.season = 2022 AND ps.fga >= 5 AND ps.gp >= 20
ORDER BY ps.fg_pct DESC
LIMIT 20;

-- Лучшие трёхочковые стрелки (минимум 100 попыток)
SELECT 
    p.name as Игрок,
    t.full_name as Команда,
    ps.three_fg_pct as Процент_трёхочковых,
    ps.three_pa as Попыток_трёхочковых_в_среднем,
    ps.three_pm as Попаданий_трёхочковых_в_среднем,
    ps.gp as Игр_сыграно
FROM Player p
JOIN PlayerStats ps ON p.player_id = ps.player_id
JOIN Team t ON p.team_id = t.team_id
WHERE ps.season = 2022 AND ps.three_pa >= 3 AND ps.gp >= 20
ORDER BY ps.three_fg_pct DESC
LIMIT 15;

-- Эффективные игроки (высокий PER - Player Efficiency Rating)
SELECT 
    p.name as Игрок,
    t.full_name as Команда,
    ps.pts as Очки,
    ps.ast as Передачи,
    ps.reb as Подборы,
    ps.stl as Перехваты,
    ps.blk as Блоки,
    ps.gp as Игр_сыграно,
    (ps.pts + ps.reb + ps.ast + ps.stl + ps.blk - 
     (ps.fga - ps.fgm) - (ps.fta - ps.ftm) - ps.tov) as Эффективность
FROM Player p
JOIN PlayerStats ps ON p.player_id = ps.player_id
JOIN Team t ON p.team_id = t.team_id
WHERE ps.season = 2022 AND ps.gp >= 20
ORDER BY Эффективность DESC
LIMIT 20;

-- ==========================================
-- 6. АНАЛИЗ КОМАНДНОЙ СТАТИСТИКИ
-- ==========================================

-- Команды по победам (2022 сезон)
SELECT 
    t.full_name as Команда,
    t.conference as Конференция,
    COUNT(g.game_id) as Всего_игр,
    SUM(CASE 
        WHEN (g.home_team_id = t.team_id AND g.home_team_score > g.visitor_team_score) OR
             (g.visitor_team_id = t.team_id AND g.visitor_team_score > g.home_team_score) 
        THEN 1 ELSE 0 END) as Победы,
    ROUND(SUM(CASE 
        WHEN (g.home_team_id = t.team_id AND g.home_team_score > g.visitor_team_score) OR
             (g.visitor_team_id = t.team_id AND g.visitor_team_score > g.home_team_score) 
        THEN 1 ELSE 0 END) * 100.0 / COUNT(g.game_id), 1) as Процент_побед
FROM Team t
JOIN Game g ON t.team_id = g.home_team_id OR t.team_id = g.visitor_team_id
WHERE strftime('%Y', g.date_game) = '2022'
GROUP BY t.team_id
HAVING COUNT(g.game_id) >= 10
ORDER BY Процент_побед DESC;

-- Домашние vs выездные победы
SELECT 
    t.full_name as Команда,
    SUM(CASE WHEN g.home_team_id = t.team_id THEN 1 ELSE 0 END) as Домашних_игр,
    SUM(CASE WHEN g.home_team_id = t.team_id AND g.home_team_score > g.visitor_team_score THEN 1 ELSE 0 END) as Домашних_побед,
    SUM(CASE WHEN g.visitor_team_id = t.team_id THEN 1 ELSE 0 END) as Выездных_игр,
    SUM(CASE WHEN g.visitor_team_id = t.team_id AND g.visitor_team_score > g.home_team_score THEN 1 ELSE 0 END) as Выездных_побед
FROM Team t
JOIN Game g ON t.team_id = g.home_team_id OR t.team_id = g.visitor_team_id
WHERE strftime('%Y', g.date_game) = '2022'
GROUP BY t.team_id
ORDER BY (Домашних_побед + Выездных_побед) DESC;

-- ==========================================
-- 7. АНАЛИЗ ПОСЕЩАЕМОСТИ
-- ==========================================

-- Посещаемость по месяцам
SELECT 
    strftime('%m', g.date_game) as Месяц,
    COUNT(*) as Количество_игр,
    AVG(g.attendance) as Средняя_посещаемость,
    MAX(g.attendance) as Максимальная_посещаемость,
    MIN(g.attendance) as Минимальная_посещаемость
FROM Game g
WHERE strftime('%Y', g.date_game) = '2022'
GROUP BY strftime('%m', g.date_game)
ORDER BY Месяц;

-- Команды с лучшей посещаемостью
SELECT 
    t.full_name as Команда,
    AVG(CASE WHEN g.home_team_id = t.team_id THEN g.attendance END) as Средняя_домашняя_посещаемость,
    COUNT(CASE WHEN g.home_team_id = t.team_id THEN 1 END) as Домашних_игр
FROM Team t
JOIN Game g ON t.team_id = g.home_team_id
WHERE strftime('%Y', g.date_game) = '2022'
GROUP BY t.team_id
HAVING Домашних_игр >= 5
ORDER BY Средняя_домашняя_посещаемость DESC
LIMIT 10;

-- ==========================================
-- 8. СЕЗОННЫЕ ТРЕНДЫ
-- ==========================================

-- Развитие игроков по сезонам
-- (для анализа прогресса игроков)
SELECT 
    p.name as Игрок,
    ps.season as Сезон,
    ps.gp as Игр_сыграно,
    ps.pts as Очки_в_среднем,
    ps.ast as Передачи_в_среднем,
    ps.reb as Подборы_в_среднем
FROM Player p
JOIN PlayerStats ps ON p.player_id = ps.player_id
WHERE p.name LIKE '%LeBron%'  -- Пример для конкретного игрока
ORDER BY ps.season;

-- Сравнение конференций
SELECT 
    t.conference as Конференция,
    COUNT(DISTINCT t.team_id) as Команд,
    AVG(CASE 
        WHEN (g.home_team_id = t.team_id AND g.home_team_score > g.visitor_team_score) OR
             (g.visitor_team_id = t.team_id AND g.visitor_team_score > g.home_team_score) 
        THEN 1.0 ELSE 0 END) as Средний_процент_побед
FROM Team t
JOIN Game g ON t.team_id = g.home_team_id OR t.team_id = g.visitor_team_id
WHERE strftime('%Y', g.date_game) = '2022'
GROUP BY t.conference;

-- ==========================================
-- 9. ДОПОЛНИТЕЛЬНЫЕ АНАЛИТИЧЕСКИЕ ЗАПРОСЫ
-- ==========================================

-- Игроки-новички (первый сезон)
SELECT 
    p.name as Новичок,
    t.full_name as Команда,
    ps.pts as Очки_в_среднем,
    ps.ast as Передачи_в_среднем,
    ps.reb as Подборы_в_среднем,
    ps.gp as Игр_сыграно
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

-- Команды с лучшей обороной (меньше очков пропущено)
SELECT 
    t.full_name as Команда,
    AVG(CASE WHEN g.home_team_id = t.team_id THEN g.visitor_team_score 
             ELSE g.home_team_score END) as Средне_очков_пропущено
FROM Team t
JOIN Game g ON t.team_id = g.home_team_id OR t.team_id = g.visitor_team_id
WHERE strftime('%Y', g.date_game) = '2022'
GROUP BY t.team_id
ORDER BY Средне_очков_пропущено ASC
LIMIT 10;

-- Статистика по возрасту игроков
-- SELECT 
--     CASE 
--         WHEN CAST(SUBSTR(height, 1, INSTR(height, '-') - 1) AS INTEGER) < 6 THEN 'Низкий (<6 футов)'
--         WHEN CAST(SUBSTR(height, 1, INSTR(height, '-') - 1) AS INTEGER) = 6 THEN 'Средний (6 футов)'
--         ELSE 'Высокий (>6 футов)'
--     END as Ростовая_категория,
--     COUNT(*) as КоличествоИгроков,
--     AVG(pts) as СредниеОчки,
--     AVG(reb) as СредниеПодборы
-- FROM Player p
-- JOIN PlayerStats ps ON p.player_id = ps.player_id
-- WHERE ps.season = 2022 AND ps.gp >= 20
-- GROUP BY 
--     CASE 
--         WHEN CAST(SUBSTR(height, 1, INSTR(height, '-') - 1) AS INTEGER) < 6 THEN 'Низкий (<6 футов)'
--         WHEN CAST(SUBSTR(height, 1, INSTR(height, '-') - 1) AS INTEGER) = 6 THEN 'Средний (6 футов)'
--         ELSE 'Высокий (>6 футов)'
--     END
-- ORDER BY СредниеОчки DESC;