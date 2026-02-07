-- Система архивирования старых данных для базы данных зоопарка

USE animals_db;

-- Таблица для хранения информации об архивах
CREATE TABLE IF NOT EXISTS archive_logs (
    id INT PRIMARY KEY AUTO_INCREMENT,
    archive_name VARCHAR(255) NOT NULL,
    table_name VARCHAR(100) NOT NULL,
    archived_records_count INT,
    archive_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    archive_size BIGINT,
    archive_location VARCHAR(500),
    created_by VARCHAR(100),
    status ENUM('SUCCESS', 'FAILED', 'IN_PROGRESS') DEFAULT 'IN_PROGRESS',
    criteria_used TEXT,  -- критерии, по которым данные были заархивированы
    notes TEXT
);

-- Архивная таблица для старых записей о кормлениях
CREATE TABLE IF NOT EXISTS feedings_archive (
    id INT,
    animal_id INT,
    employee_id INT,
    food_type VARCHAR(200),
    quantity VARCHAR(50),
    feeding_time TIME,
    feeding_date DATE,
    notes TEXT,
    archived_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    original_id INT  -- ID записи в оригинальной таблице
);

-- Архивная таблица для старых медицинских записей
CREATE TABLE IF NOT EXISTS medical_records_archive (
    id INT,
    animal_id INT,
    vet_id INT,
    record_date DATE,
    diagnosis TEXT,
    treatment TEXT,
    medication VARCHAR(200),
    next_checkup DATE,
    archived_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    original_id INT  -- ID записи в оригинальной таблице
);

-- Архивная таблица для старых вакцинаций
CREATE TABLE IF NOT EXISTS vaccinations_archive (
    id INT,
    animal_id INT,
    vaccine_name VARCHAR(150),
    vaccination_date DATE,
    expiration_date DATE,
    administered_by INT,
    archived_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    original_id INT  -- ID записи в оригинальной таблице
);

-- Процедура для архивирования старых записей о кормлениях
DELIMITER //
CREATE PROCEDURE ArchiveOldFeedings(
    IN p_months_threshold INT,
    IN p_archived_by VARCHAR(100)
)
BEGIN
    DECLARE threshold_date DATE;
    DECLARE archived_count INT DEFAULT 0;
    
    SET threshold_date = DATE_SUB(CURDATE(), INTERVAL p_months_threshold MONTH);
    
    -- Архивируем записи о кормлениях старше заданного порога
    INSERT INTO feedings_archive (id, animal_id, employee_id, food_type, quantity, 
                                 feeding_time, feeding_date, notes, original_id)
    SELECT id, animal_id, employee_id, food_type, quantity, 
           feeding_time, feeding_date, notes, id
    FROM feedings
    WHERE feeding_date < threshold_date;
    
    -- Получаем количество заархивированных записей
    SET archived_count = ROW_COUNT();
    
    -- Удаляем заархивированные записи из основной таблицы
    DELETE FROM feedings
    WHERE feeding_date < threshold_date;
    
    -- Записываем лог архивации
    INSERT INTO archive_logs (archive_name, table_name, archived_records_count, 
                            created_by, status, criteria_used)
    VALUES (CONCAT('Feedings_Archive_', DATE_FORMAT(NOW(), '%Y%m')), 
            'feedings', archived_count, p_archived_by, 'SUCCESS',
            CONCAT('Archived feedings older than ', threshold_date));
            
    SELECT archived_count AS records_archived;
END //

-- Процедура для архивирования старых медицинских записей
CREATE PROCEDURE ArchiveOldMedicalRecords(
    IN p_months_threshold INT,
    IN p_archived_by VARCHAR(100)
)
BEGIN
    DECLARE threshold_date DATE;
    DECLARE archived_count INT DEFAULT 0;
    
    SET threshold_date = DATE_SUB(CURDATE(), INTERVAL p_months_threshold MONTH);
    
    -- Архивируем медицинские записи старше заданного порога
    INSERT INTO medical_records_archive (id, animal_id, vet_id, record_date, diagnosis, 
                                       treatment, medication, next_checkup, original_id)
    SELECT id, animal_id, vet_id, record_date, diagnosis, 
           treatment, medication, next_checkup, id
    FROM medical_records
    WHERE record_date < threshold_date;
    
    -- Получаем количество заархивированных записей
    SET archived_count = ROW_COUNT();
    
    -- Удаляем заархивированные записи из основной таблицы
    DELETE FROM medical_records
    WHERE record_date < threshold_date;
    
    -- Записываем лог архивации
    INSERT INTO archive_logs (archive_name, table_name, archived_records_count, 
                            created_by, status, criteria_used)
    VALUES (CONCAT('Medical_Records_Archive_', DATE_FORMAT(NOW(), '%Y%m')), 
            'medical_records', archived_count, p_archived_by, 'SUCCESS',
            CONCAT('Archived medical records older than ', threshold_date));
            
    SELECT archived_count AS records_archived;
END //

-- Процедура для архивирования старых вакцинаций
CREATE PROCEDURE ArchiveOldVaccinations(
    IN p_months_threshold INT,
    IN p_archived_by VARCHAR(100)
)
BEGIN
    DECLARE threshold_date DATE;
    DECLARE archived_count INT DEFAULT 0;
    
    SET threshold_date = DATE_SUB(CURDATE(), INTERVAL p_months_threshold MONTH);
    
    -- Архивируем вакцинации старше заданного порога
    INSERT INTO vaccinations_archive (id, animal_id, vaccine_name, vaccination_date, 
                                    expiration_date, administered_by, original_id)
    SELECT id, animal_id, vaccine_name, vaccination_date, 
           expiration_date, administered_by, id
    FROM vaccinations
    WHERE vaccination_date < threshold_date 
       OR (expiration_date IS NOT NULL AND expiration_date < threshold_date);
    
    -- Получаем количество заархивированных записей
    SET archived_count = ROW_COUNT();
    
    -- Удаляем заархивированные записи из основной таблицы
    DELETE FROM vaccinations
    WHERE vaccination_date < threshold_date 
       OR (expiration_date IS NOT NULL AND expiration_date < threshold_date);
    
    -- Записываем лог архивации
    INSERT INTO archive_logs (archive_name, table_name, archived_records_count, 
                            created_by, status, criteria_used)
    VALUES (CONCAT('Vaccinations_Archive_', DATE_FORMAT(NOW(), '%Y%m')), 
            'vaccinations', archived_count, p_archived_by, 'SUCCESS',
            CONCAT('Archived vaccinations older than ', threshold_date, ' or with expiration before ', threshold_date));
            
    SELECT archived_count AS records_archived;
END //

-- Процедура для полного архивирования по критериям
CREATE PROCEDURE ArchiveOldData(
    IN p_months_threshold INT,
    IN p_archived_by VARCHAR(100),
    IN p_tables_to_archive VARCHAR(255)  -- через запятую: 'feedings,medical_records,vaccinations'
)
BEGIN
    DECLARE done INT DEFAULT FALSE;
    DECLARE table_name VARCHAR(50);
    DECLARE archive_cursor CURSOR FOR 
        SELECT TRIM(value) FROM (
            SELECT SUBSTRING_INDEX(SUBSTRING_INDEX(p_tables_to_archive, ',', numbers.n), ',', -1) value
            FROM (SELECT 1 n UNION SELECT 2 UNION SELECT 3 UNION SELECT 4 UNION SELECT 5) numbers
            WHERE CHAR_LENGTH(p_tables_to_archive) - CHAR_LENGTH(REPLACE(p_tables_to_archive, ',', '')) >= numbers.n - 1
        ) AS extracted_tables;
    DECLARE CONTINUE HANDLER FOR NOT FOUND SET done = TRUE;
    
    OPEN archive_cursor;
    
    read_loop: LOOP
        FETCH archive_cursor INTO table_name;
        IF done THEN
            LEAVE read_loop;
        END IF;
        
        CASE table_name
            WHEN 'feedings' THEN
                CALL ArchiveOldFeedings(p_months_threshold, p_archived_by);
            WHEN 'medical_records' THEN
                CALL ArchiveOldMedicalRecords(p_months_threshold, p_archived_by);
            WHEN 'vaccinations' THEN
                CALL ArchiveOldVaccinations(p_months_threshold, p_archived_by);
        END CASE;
    END LOOP;
    
    CLOSE archive_cursor;
    
    SELECT 'Data archiving completed' AS result;
END //

-- Процедура для просмотра архивов
CREATE PROCEDURE GetArchiveLogs()
BEGIN
    SELECT 
        id,
        archive_name,
        table_name,
        archived_records_count,
        DATE_FORMAT(archive_date, '%Y-%m-%d %H:%i:%s') AS formatted_date,
        created_by,
        status,
        criteria_used
    FROM archive_logs
    ORDER BY archive_date DESC;
END //

-- Процедура для восстановления данных из архива (для кормлений)
CREATE PROCEDURE RestoreFeedingsFromArchive(
    IN p_archive_ids TEXT  -- через запятую
)
BEGIN
    SET @sql = CONCAT('INSERT INTO feedings (id, animal_id, employee_id, food_type, quantity, feeding_time, feeding_date, notes) ',
                      'SELECT original_id, animal_id, employee_id, food_type, quantity, feeding_time, feeding_date, notes ',
                      'FROM feedings_archive ',
                      'WHERE FIND_IN_SET(id, ''', p_archive_ids, ''') > 0');
    
    PREPARE stmt FROM @sql;
    EXECUTE stmt;
    DEALLOCATE PREPARE stmt;
    
    -- Удаляем восстановленные записи из архива
    SET @delete_sql = CONCAT('DELETE FROM feedings_archive WHERE FIND_IN_SET(id, ''', p_archive_ids, ''') > 0');
    
    PREPARE del_stmt FROM @delete_sql;
    EXECUTE del_stmt;
    DEALLOCATE PREPREPARE del_stmt;
    
    SELECT 'Feedings restored from archive' AS result;
END //

-- Представление для получения статистики по архивам
CREATE VIEW archive_statistics AS
SELECT 
    table_name,
    COUNT(*) AS archive_operations,
    SUM(archived_records_count) AS total_archived_records,
    AVG(archived_records_count) AS avg_records_per_archive,
    MIN(archive_date) AS first_archive_date,
    MAX(archive_date) AS last_archive_date
FROM archive_logs
GROUP BY table_name;

DELIMITER ;

-- Примеры использования процедур архивирования

/*
-- Архивировать кормления старше 24 месяцев
CALL ArchiveOldFeedings(24, 'System Admin');

-- Архивировать медицинские записи старше 36 месяцев
CALL ArchiveOldMedicalRecords(36, 'System Admin');

-- Архивировать вакцинации старше 24 месяцев
CALL ArchiveOldVaccinations(24, 'System Admin');

-- Архивировать несколько типов данных сразу
CALL ArchiveOldData(24, 'System Admin', 'feedings,medical_records,vaccinations');

-- Посмотреть логи архивации
CALL GetArchiveLogs();

-- Посмотреть статистику архивации
SELECT * FROM archive_statistics;
*/

-- Пример cron-задания для автоматического архивирования
/*
# Ежемесячное архивирование старых данных
# Выполнять первого числа каждого месяца в 3:00 ночи
0 3 1 * * mysql -u username -p'password' animals_db -e "CALL ArchiveOldData(24, 'System', 'feedings,medical_records,vaccinations');"
*/