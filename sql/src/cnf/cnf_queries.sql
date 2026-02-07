-- Запросы к базе данных CNF
-- База данных Canadian National Railway с маршрутами, станциями, расписаниями

-- 1. Базовое исследование таблиц
SELECT name AS table_name
FROM sqlite_master 
WHERE type = 'table';

-- 2. Получить схему базы данных
PRAGMA table_info(routes);

-- 3. Простое исследование данных
SELECT * FROM routes LIMIT 5;
SELECT * FROM stations LIMIT 5;
SELECT * FROM schedules LIMIT 5;

-- 4. Найти маршруты между конкретными городами
SELECT 
    r.route_id,
    r.origin_city,
    r.destination_city,
    r.distance_km
FROM routes r
WHERE r.origin_city = 'Montreal' 
  AND r.destination_city = 'Toronto';

-- 5. Станции в конкретной провинции
SELECT 
    station_name,
    city,
    province
FROM stations
WHERE province = 'ON'  -- Ontario
ORDER BY city, station_name;

-- 6. Активные расписания на сегодня
SELECT 
    s.train_id,
    s.route_id,
    s.departure_time,
    s.arrival_time,
    s.status
FROM schedules s
WHERE date(s.departure_time) = date('now')
  AND s.status = 'Active'
ORDER BY s.departure_time;

-- 7. Самые популярные маршруты по частоте
SELECT 
    r.origin_city,
    r.destination_city,
    COUNT(s.schedule_id) AS frequency
FROM routes r
JOIN schedules s ON r.route_id = s.route_id
GROUP BY r.route_id
ORDER BY frequency DESC
LIMIT 10;

-- 8. Среднее время в пути по маршрутам
SELECT 
    r.origin_city,
    r.destination_city,
    AVG(strftime('%s', s.arrival_time) - strftime('%s', s.departure_time)) / 3600.0 AS avg_hours
FROM routes r
JOIN schedules s ON r.route_id = s.route_id
WHERE s.arrival_time > s.departure_time
GROUP BY r.route_id
ORDER BY avg_hours DESC;

-- 9. Станции со статусом обслуживания
SELECT 
    st.station_name,
    st.city,
    st.maintenance_status,
    COUNT(s.schedule_id) AS daily_trains
FROM stations st
LEFT JOIN schedules s ON st.station_id = s.origin_station_id 
    AND date(s.departure_time) = date('now')
GROUP BY st.station_id
ORDER BY st.maintenance_status, st.station_name;

-- 10. Анализ задержек
SELECT 
    s.train_id,
    s.route_id,
    s.scheduled_departure,
    s.actual_departure,
    strftime('%s', s.actual_departure) - strftime('%s', s.scheduled_departure) AS delay_minutes
FROM schedules s
WHERE s.actual_departure IS NOT NULL
  AND s.actual_departure > s.scheduled_departure
ORDER BY delay_minutes DESC
LIMIT 20;