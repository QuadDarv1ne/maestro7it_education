-- TEST: Получение списка всех таблиц | 13
SELECT name FROM sqlite_master WHERE type = 'table';

-- TEST: Количество команд | 30
SELECT COUNT(*) FROM Team;

-- TEST: Количество игроков | 500
SELECT COUNT(*) FROM Player;

-- TEST: Количество сезонов | 5
SELECT COUNT(*) FROM Season;

-- TEST: Команды конференции West | 15
SELECT COUNT(*) 
FROM Team 
WHERE Conference = 'West';

-- TEST: Средний рост игроков | 1
SELECT AVG(Height) as AverageHeight
FROM Player
WHERE Height IS NOT NULL;

-- TEST: Игроки из команды с ID 1610612738 | 18
SELECT COUNT(*) 
FROM Player 
WHERE Team_id = 1610612738;

-- TEST: Игры сезона 2018 | 1230
SELECT COUNT(*) 
FROM Game 
WHERE SEASON_id = 2018;

-- TEST: Количество побед и поражений для команды | 1
SELECT W + L as TotalGames
FROM TeamDetail
WHERE TEAM_ID = 1610612738
LIMIT 1;

-- TEST: Средняя продолжительность игр (минут) | 1
SELECT AVG(LENGTH) as AvgMinutes
FROM GameDetail;