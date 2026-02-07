-- Система логирования действий пользователей для базы данных зоопарка

USE animals_db;

-- Таблица для хранения логов действий пользователей
CREATE TABLE IF NOT EXISTS user_action_logs (
    id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT,
    username VARCHAR(100),
    action_type VARCHAR(100) NOT NULL,  -- тип действия (INSERT, UPDATE, DELETE, SELECT)
    table_name VARCHAR(100) NOT NULL,   -- имя таблицы, с которой производилось действие
    record_id INT,                      -- ID записи, с которой произведено действие
    old_values JSON,                    -- старые значения (для UPDATE и DELETE)
    new_values JSON,                    -- новые значения (для INSERT и UPDATE)
    ip_address VARCHAR(45),             -- IP-адрес пользователя
    user_agent TEXT,                    -- User Agent браузера
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    session_id VARCHAR(255),            -- ID сессии пользователя
    details TEXT,                       -- дополнительная информация о действии
    FOREIGN KEY (user_id) REFERENCES system_users(id)
);

-- Таблица для настройки правил логирования
CREATE TABLE IF NOT EXISTS logging_rules (
    id INT PRIMARY KEY AUTO_INCREMENT,
    table_name VARCHAR(100) NOT NULL,
    action_type ENUM('INSERT', 'UPDATE', 'DELETE', 'SELECT') DEFAULT 'UPDATE',
    log_enabled BOOLEAN DEFAULT TRUE,
    log_old_values BOOLEAN DEFAULT TRUE,
    log_new_values BOOLEAN DEFAULT TRUE,
    min_severity ENUM('LOW', 'MEDIUM', 'HIGH', 'CRITICAL') DEFAULT 'MEDIUM',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- Создание триггеров для логирования изменений в основных таблицах

-- Триггеры для таблицы animals
DELIMITER //

CREATE TRIGGER animals_insert_log 
AFTER INSERT ON animals
FOR EACH ROW
BEGIN
    INSERT INTO user_action_logs (action_type, table_name, record_id, new_values, details)
    VALUES ('INSERT', 'animals', NEW.id, 
            JSON_OBJECT(
                'id', NEW.id,
                'name', NEW.name,
                'species_id', NEW.species_id,
                'birth_date', NEW.birth_date,
                'gender', NEW.gender,
                'health_status', NEW.health_status,
                'arrival_date', NEW.arrival_date,
                'departure_date', NEW.departure_date,
                'mother_id', NEW.mother_id,
                'father_id', NEW.father_id,
                'enclosure_id', NEW.enclosure_id
            ),
            CONCAT('Added new animal: ', NEW.name));
END //

CREATE TRIGGER animals_update_log 
AFTER UPDATE ON animals
FOR EACH ROW
BEGIN
    INSERT INTO user_action_logs (action_type, table_name, record_id, old_values, new_values, details)
    VALUES ('UPDATE', 'animals', NEW.id,
            JSON_OBJECT(
                'id', OLD.id,
                'name', OLD.name,
                'species_id', OLD.species_id,
                'birth_date', OLD.birth_date,
                'gender', OLD.gender,
                'health_status', OLD.health_status,
                'arrival_date', OLD.arrival_date,
                'departure_date', OLD.departure_date,
                'mother_id', OLD.mother_id,
                'father_id', OLD.father_id,
                'enclosure_id', OLD.enclosure_id
            ),
            JSON_OBJECT(
                'id', NEW.id,
                'name', NEW.name,
                'species_id', NEW.species_id,
                'birth_date', NEW.birth_date,
                'gender', NEW.gender,
                'health_status', NEW.health_status,
                'arrival_date', NEW.arrival_date,
                'departure_date', NEW.departure_date,
                'mother_id', NEW.mother_id,
                'father_id', NEW.father_id,
                'enclosure_id', NEW.enclosure_id
            ),
            CONCAT('Updated animal: ', NEW.name));
END //

CREATE TRIGGER animals_delete_log 
BEFORE DELETE ON animals
FOR EACH ROW
BEGIN
    INSERT INTO user_action_logs (action_type, table_name, record_id, old_values, details)
    VALUES ('DELETE', 'animals', OLD.id,
            JSON_OBJECT(
                'id', OLD.id,
                'name', OLD.name,
                'species_id', OLD.species_id,
                'birth_date', OLD.birth_date,
                'gender', OLD.gender,
                'health_status', OLD.health_status,
                'arrival_date', OLD.arrival_date,
                'departure_date', OLD.departure_date,
                'mother_id', OLD.mother_id,
                'father_id', OLD.father_id,
                'enclosure_id', OLD.enclosure_id
            ),
            CONCAT('Deleted animal: ', OLD.name));
END //

-- Триггеры для таблицы medical_records
CREATE TRIGGER medical_records_insert_log 
AFTER INSERT ON medical_records
FOR EACH ROW
BEGIN
    INSERT INTO user_action_logs (action_type, table_name, record_id, new_values, details)
    VALUES ('INSERT', 'medical_records', NEW.id,
            JSON_OBJECT(
                'id', NEW.id,
                'animal_id', NEW.animal_id,
                'vet_id', NEW.vet_id,
                'record_date', NEW.record_date,
                'diagnosis', NEW.diagnosis,
                'treatment', NEW.treatment,
                'medication', NEW.medication,
                'next_checkup', NEW.next_checkup
            ),
            CONCAT('Added medical record for animal ID: ', NEW.animal_id));
END //

CREATE TRIGGER medical_records_update_log 
AFTER UPDATE ON medical_records
FOR EACH ROW
BEGIN
    INSERT INTO user_action_logs (action_type, table_name, record_id, old_values, new_values, details)
    VALUES ('UPDATE', 'medical_records', NEW.id,
            JSON_OBJECT(
                'id', OLD.id,
                'animal_id', OLD.animal_id,
                'vet_id', OLD.vet_id,
                'record_date', OLD.record_date,
                'diagnosis', OLD.diagnosis,
                'treatment', OLD.treatment,
                'medication', OLD.medication,
                'next_checkup', OLD.next_checkup
            ),
            JSON_OBJECT(
                'id', NEW.id,
                'animal_id', NEW.animal_id,
                'vet_id', NEW.vet_id,
                'record_date', NEW.record_date,
                'diagnosis', NEW.diagnosis,
                'treatment', NEW.treatment,
                'medication', NEW.medication,
                'next_checkup', NEW.next_checkup
            ),
            CONCAT('Updated medical record for animal ID: ', NEW.animal_id));
END //

CREATE TRIGGER medical_records_delete_log 
BEFORE DELETE ON medical_records
FOR EACH ROW
BEGIN
    INSERT INTO user_action_logs (action_type, table_name, record_id, old_values, details)
    VALUES ('DELETE', 'medical_records', OLD.id,
            JSON_OBJECT(
                'id', OLD.id,
                'animal_id', OLD.animal_id,
                'vet_id', OLD.vet_id,
                'record_date', OLD.record_date,
                'diagnosis', OLD.diagnosis,
                'treatment', OLD.treatment,
                'medication', OLD.medication,
                'next_checkup', OLD.next_checkup
            ),
            CONCAT('Deleted medical record for animal ID: ', OLD.animal_id));
END //

-- Триггеры для таблицы feedings
CREATE TRIGGER feedings_insert_log 
AFTER INSERT ON feedings
FOR EACH ROW
BEGIN
    INSERT INTO user_action_logs (action_type, table_name, record_id, new_values, details)
    VALUES ('INSERT', 'feedings', NEW.id,
            JSON_OBJECT(
                'id', NEW.id,
                'animal_id', NEW.animal_id,
                'employee_id', NEW.employee_id,
                'food_type', NEW.food_type,
                'quantity', NEW.quantity,
                'feeding_time', NEW.feeding_time,
                'feeding_date', NEW.feeding_date,
                'notes', NEW.notes
            ),
            CONCAT('Added feeding record for animal ID: ', NEW.animal_id));
END //

CREATE TRIGGER feedings_update_log 
AFTER UPDATE ON feedings
FOR EACH ROW
BEGIN
    INSERT INTO user_action_logs (action_type, table_name, record_id, old_values, new_values, details)
    VALUES ('UPDATE', 'feedings', NEW.id,
            JSON_OBJECT(
                'id', OLD.id,
                'animal_id', OLD.animal_id,
                'employee_id', OLD.employee_id,
                'food_type', OLD.food_type,
                'quantity', OLD.quantity,
                'feeding_time', OLD.feeding_time,
                'feeding_date', OLD.feeding_date,
                'notes', OLD.notes
            ),
            JSON_OBJECT(
                'id', NEW.id,
                'animal_id', NEW.animal_id,
                'employee_id', NEW.employee_id,
                'food_type', NEW.food_type,
                'quantity', NEW.quantity,
                'feeding_time', NEW.feeding_time,
                'feeding_date', NEW.feeding_date,
                'notes', NEW.notes
            ),
            CONCAT('Updated feeding record for animal ID: ', NEW.animal_id));
END //

CREATE TRIGGER feedings_delete_log 
BEFORE DELETE ON feedings
FOR EACH ROW
BEGIN
    INSERT INTO user_action_logs (action_type, table_name, record_id, old_values, details)
    VALUES ('DELETE', 'feedings', OLD.id,
            JSON_OBJECT(
                'id', OLD.id,
                'animal_id', OLD.animal_id,
                'employee_id', OLD.employee_id,
                'food_type', OLD.food_type,
                'quantity', OLD.quantity,
                'feeding_time', OLD.feeding_time,
                'feeding_date', OLD.feeding_date,
                'notes', OLD.notes
            ),
            CONCAT('Deleted feeding record for animal ID: ', OLD.animal_id));
END //

-- Процедура для получения логов действий пользователя
CREATE PROCEDURE GetUserActionLogs(
    IN p_user_id INT,
    IN p_start_date DATE,
    IN p_end_date DATE,
    IN p_limit INT
)
BEGIN
    SELECT 
        id,
        username,
        action_type,
        table_name,
        record_id,
        DATE_FORMAT(timestamp, '%Y-%m-%d %H:%i:%s') AS formatted_timestamp,
        details
    FROM user_action_logs
    WHERE (p_user_id IS NULL OR user_id = p_user_id)
      AND (p_start_date IS NULL OR DATE(timestamp) >= p_start_date)
      AND (p_end_date IS NULL OR DATE(timestamp) <= p_end_date)
    ORDER BY timestamp DESC
    LIMIT COALESCE(p_limit, 100);
END //

-- Процедура для получения логов по типу действия
CREATE PROCEDURE GetActionLogsByType(
    IN p_action_type VARCHAR(100),
    IN p_table_name VARCHAR(100),
    IN p_start_date DATE,
    IN p_end_date DATE
)
BEGIN
    SELECT 
        ual.id,
        su.username,
        ual.action_type,
        ual.table_name,
        ual.record_id,
        DATE_FORMAT(ual.timestamp, '%Y-%m-%d %H:%i:%s') AS formatted_timestamp,
        ual.details,
        ual.ip_address
    FROM user_action_logs ual
    LEFT JOIN system_users su ON ual.user_id = su.id
    WHERE (p_action_type IS NULL OR ual.action_type = p_action_type)
      AND (p_table_name IS NULL OR ual.table_name = p_table_name)
      AND (p_start_date IS NULL OR DATE(ual.timestamp) >= p_start_date)
      AND (p_end_date IS NULL OR DATE(ual.timestamp) <= p_end_date)
    ORDER BY ual.timestamp DESC;
END //

-- Процедура для очистки старых логов
CREATE PROCEDURE CleanupOldActionLogs(
    IN p_days_to_keep INT
)
BEGIN
    DECLARE deleted_count INT DEFAULT 0;
    
    DELETE FROM user_action_logs 
    WHERE timestamp < DATE_SUB(NOW(), INTERVAL p_days_to_keep DAY);
    
    SET deleted_count = ROW_COUNT();
    
    SELECT deleted_count AS logs_deleted_count;
END //

-- Представление для получения статистики по действиям пользователей
CREATE VIEW user_activity_stats AS
SELECT 
    su.username,
    su.role,
    COUNT(ual.id) AS total_actions,
    SUM(CASE WHEN ual.action_type = 'INSERT' THEN 1 ELSE 0 END) AS inserts,
    SUM(CASE WHEN ual.action_type = 'UPDATE' THEN 1 ELSE 0 END) AS updates,
    SUM(CASE WHEN ual.action_type = 'DELETE' THEN 1 ELSE 0 END) AS deletes,
    SUM(CASE WHEN ual.action_type = 'SELECT' THEN 1 ELSE 0 END) AS selects,
    MAX(ual.timestamp) AS last_activity
FROM system_users su
LEFT JOIN user_action_logs ual ON su.id = ual.user_id
GROUP BY su.id, su.username, su.role
HAVING total_actions > 0
ORDER BY total_actions DESC;

DELIMITER ;

-- Примеры запросов для работы с системой логирования

/*
-- Получить последние 10 действий конкретного пользователя
CALL GetUserActionLogs(1, NULL, NULL, 10);

-- Получить все обновления в таблице животных за последнюю неделю
CALL GetActionLogsByType('UPDATE', 'animals', DATE_SUB(CURDATE(), INTERVAL 7 DAY), CURDATE());

-- Очистить логи старше 30 дней
CALL CleanupOldActionLogs(30);

-- Посмотреть статистику активности пользователей
SELECT * FROM user_activity_stats;
*/