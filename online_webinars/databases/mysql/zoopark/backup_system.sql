-- Система резервного копирования базы данных зоопарка

USE animals_db;

-- Таблица для хранения информации о резервных копиях
CREATE TABLE IF NOT EXISTS backup_logs (
    id INT PRIMARY KEY AUTO_INCREMENT,
    backup_name VARCHAR(255) NOT NULL,
    backup_date DATETIME DEFAULT CURRENT_TIMESTAMP,
    backup_size BIGINT,
    backup_location VARCHAR(500),
    created_by VARCHAR(100),
    status ENUM('SUCCESS', 'FAILED', 'IN_PROGRESS') DEFAULT 'IN_PROGRESS',
    notes TEXT
);

-- Процедура для создания резервной копии
DELIMITER //
CREATE PROCEDURE CreateBackup(
    IN p_backup_name VARCHAR(255),
    IN p_backup_location VARCHAR(500),
    IN p_created_by VARCHAR(100)
)
BEGIN
    DECLARE EXIT HANDLER FOR SQLEXCEPTION
    BEGIN
        ROLLBACK;
        INSERT INTO backup_logs (backup_name, backup_location, created_by, status, notes)
        VALUES (p_backup_name, p_backup_location, p_created_by, 'FAILED', 'Error occurred during backup');
    END;
    
    START TRANSACTION;
    
    -- Записываем начало резервного копирования
    INSERT INTO backup_logs (backup_name, backup_location, created_by, status)
    VALUES (p_backup_name, p_backup_location, p_created_by, 'IN_PROGRESS');
    
    -- Здесь будет вызов внешней команды mysqldump через системную процедуру
    -- Так как MySQL не позволяет напрямую вызывать mysqldump из хранимой процедуры,
    -- то в реальной системе это будет реализовано через внешний скрипт
    
    -- Обновляем статус на успешный
    UPDATE backup_logs 
    SET status = 'SUCCESS', 
        backup_date = CURRENT_TIMESTAMP,
        notes = 'Backup completed successfully'
    WHERE backup_name = p_backup_name AND status = 'IN_PROGRESS';
    
    COMMIT;
END //

-- Процедура для просмотра истории резервных копий
CREATE PROCEDURE GetBackupHistory()
BEGIN
    SELECT 
        id,
        backup_name,
        DATE_FORMAT(backup_date, '%Y-%m-%d %H:%i:%s') AS formatted_date,
        backup_size,
        backup_location,
        created_by,
        status,
        notes
    FROM backup_logs
    ORDER BY backup_date DESC;
END //

-- Процедура для очистки старых логов резервного копирования (старше 30 дней)
CREATE PROCEDURE CleanupOldBackupLogs()
BEGIN
    DELETE FROM backup_logs 
    WHERE backup_date < DATE_SUB(NOW(), INTERVAL 30 DAY);
    
    SELECT ROW_COUNT() AS deleted_logs_count;
END //

-- Представление для получения последней успешной резервной копии
CREATE VIEW latest_successful_backup AS
SELECT 
    backup_name,
    DATE_FORMAT(backup_date, '%Y-%m-%d %H:%i:%s') AS backup_datetime,
    backup_location,
    created_by,
    notes
FROM backup_logs
WHERE status = 'SUCCESS'
ORDER BY backup_date DESC
LIMIT 1;

DELIMITER ;

-- Пример cron-задания для автоматического резервного копирования
/*
# Автоматическое резервное копирование базы данных зоопарка
# Выполнять ежедневно в 2:00 ночи
0 2 * * * /usr/bin/mysqldump -u username -p'password' animals_db > /path/to/backups/zoopark_backup_$(date +\%Y\%m\%d).sql

# Удаление резервных копий старше 30 дней
0 3 * * * find /path/to/backups/ -name "zoopark_backup_*.sql" -mtime +30 -delete

# Логирование операций
0 2 * * * /usr/bin/mysqldump -u username -p'password' animals_db > /path/to/backups/zoopark_backup_$(date +\%Y\%m\%d).sql && echo "$(date): Backup completed" >> /var/log/zoopark_backup.log || echo "$(date): Backup failed" >> /var/log/zoopark_backup.log
*/

-- Пример bash-скрипта для резервного копирования
/*
#!/bin/bash

# Параметры подключения к базе данных
DB_USER="username"
DB_PASS="password"
DB_NAME="animals_db"
BACKUP_DIR="/path/to/backups"
DATE=$(date +%Y%m%d_%H%M%S)
BACKUP_FILE="$BACKUP_DIR/zoopark_backup_$DATE.sql"

# Создание резервной копии
mysqldump -u $DB_USER -p$DB_PASS $DB_NAME > $BACKUP_FILE

if [ $? -eq 0 ]; then
    # Обновление лога в базе данных
    mysql -u $DB_USER -p$DB_PASS $DB_NAME -e "CALL CreateBackup('Daily Backup $DATE', '$BACKUP_FILE', 'System');"
    echo "$(date): Backup $BACKUP_FILE created successfully"
else
    # Запись ошибки в лог
    mysql -u $DB_USER -p$DB_PASS $DB_NAME -e "INSERT INTO backup_logs (backup_name, backup_location, created_by, status, notes) VALUES ('Failed Backup $DATE', '$BACKUP_FILE', 'System', 'FAILED', 'mysqldump command failed');"
    echo "$(date): Backup $BACKUP_FILE creation failed"
fi

# Удаление резервных копий старше 30 дней
find $BACKUP_DIR -name "zoopark_backup_*.sql" -mtime +30 -delete
*/