-- Система мониторинга и алертинга для базы данных зоопарка

USE animals_db;

-- Таблица для хранения логов мониторинга
CREATE TABLE IF NOT EXISTS monitoring_logs (
    id INT PRIMARY KEY AUTO_INCREMENT,
    alert_type VARCHAR(100) NOT NULL,
    severity ENUM('INFO', 'WARNING', 'CRITICAL') DEFAULT 'INFO',
    alert_message TEXT NOT NULL,
    alert_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    resolved BOOLEAN DEFAULT FALSE,
    resolution_timestamp TIMESTAMP NULL,
    resolved_by VARCHAR(100),
    additional_info JSON
);

-- Таблица для настройки правил алертинга
CREATE TABLE IF NOT EXISTS alert_rules (
    id INT PRIMARY KEY AUTO_INCREMENT,
    rule_name VARCHAR(255) NOT NULL,
    description TEXT,
    condition_sql TEXT NOT NULL,
    severity ENUM('INFO', 'WARNING', 'CRITICAL') DEFAULT 'WARNING',
    enabled BOOLEAN DEFAULT TRUE,
    notification_email VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- Процедура для проверки наличия животных, требующих медицинского внимания
DELIMITER //
CREATE PROCEDURE CheckHealthAlerts()
BEGIN
    DECLARE animal_count INT DEFAULT 0;
    DECLARE alert_message TEXT;
    
    -- Подсчет животных с проблемами со здоровьем
    SELECT COUNT(*) INTO animal_count 
    FROM animals 
    WHERE health_status != 'healthy' AND departure_date IS NULL;
    
    IF animal_count > 0 THEN
        SELECT CONCAT('Найдено ', animal_count, ' животных с нездоровым статусом') INTO alert_message;
        
        INSERT INTO monitoring_logs (alert_type, severity, alert_message, additional_info)
        VALUES ('HEALTH_ISSUES', 'CRITICAL', alert_message, 
                JSON_OBJECT('animal_count', animal_count));
    END IF;
    
    -- Проверка просроченных медицинских проверок
    SELECT COUNT(*) INTO animal_count
    FROM animals a
    LEFT JOIN medical_records mr ON a.id = mr.animal_id
    WHERE a.departure_date IS NULL 
      AND (a.health_status != 'healthy' OR mr.record_date < DATE_SUB(CURDATE(), INTERVAL 6 MONTH))
      AND a.last_medical_check < DATE_SUB(CURDATE(), INTERVAL 6 MONTH);
    
    IF animal_count > 0 THEN
        SELECT CONCAT('Найдено ', animal_count, ' животных, требующих медицинской проверки (не проверялись более 6 месяцев)') INTO alert_message;
        
        INSERT INTO monitoring_logs (alert_type, severity, alert_message, additional_info)
        VALUES ('MEDICAL_CHECK_OVERDUE', 'WARNING', alert_message, 
                JSON_OBJECT('animal_count', animal_count));
    END IF;
END //

-- Процедура для проверки необходимости вакцинации
CREATE PROCEDURE CheckVaccinationAlerts()
BEGIN
    DECLARE animal_count INT DEFAULT 0;
    DECLARE alert_message TEXT;
    
    -- Подсчет животных с просроченными вакцинацией
    SELECT COUNT(*) INTO animal_count
    FROM vaccinations v
    JOIN animals a ON v.animal_id = a.id
    WHERE v.expiration_date < CURDATE() AND a.departure_date IS NULL;
    
    IF animal_count > 0 THEN
        SELECT CONCAT('Найдено ', animal_count, ' животных с просроченной вакцинацией') INTO alert_message;
        
        INSERT INTO monitoring_logs (alert_type, severity, alert_message, additional_info)
        VALUES ('VACCINATION_EXPIRED', 'CRITICAL', alert_message, 
                JSON_OBJECT('animal_count', animal_count));
    END IF;
    
    -- Подсчет животных с вакцинацией, срок действия которой истекает в ближайшие 30 дней
    SELECT COUNT(*) INTO animal_count
    FROM vaccinations v
    JOIN animals a ON v.animal_id = a.id
    WHERE v.expiration_date BETWEEN CURDATE() AND DATE_ADD(CURDATE(), INTERVAL 30 DAY)
      AND a.departure_date IS NULL;
    
    IF animal_count > 0 THEN
        SELECT CONCAT('Найдено ', animal_count, ' животных, которым необходима вакцинация в ближайшие 30 дней') INTO alert_message;
        
        INSERT INTO monitoring_logs (alert_type, severity, alert_message, additional_info)
        VALUES ('VACCINATION_DUE_SOON', 'WARNING', alert_message, 
                JSON_OBJECT('animal_count', animal_count));
    END IF;
END //

-- Процедура для проверки проблем с кормлением
CREATE PROCEDURE CheckFeedingAlerts()
BEGIN
    DECLARE animal_count INT DEFAULT 0;
    DECLARE alert_message TEXT;
    
    -- Подсчет животных, не кормленных сегодня
    SELECT COUNT(*) INTO animal_count
    FROM animals a
    LEFT JOIN feedings f ON a.id = f.animal_id AND f.feeding_date = CURDATE()
    WHERE a.departure_date IS NULL AND f.id IS NULL;
    
    IF animal_count > 0 THEN
        SELECT CONCAT('Найдено ', animal_count, ' животных, которые не были покормлены сегодня') INTO alert_message;
        
        INSERT INTO monitoring_logs (alert_type, severity, alert_message, additional_info)
        VALUES ('FEEDING_MISSED', 'WARNING', alert_message, 
                JSON_OBJECT('animal_count', animal_count));
    END IF;
END //

-- Процедура для общего мониторинга системы
CREATE PROCEDURE RunSystemMonitoring()
BEGIN
    -- Проверяем проблемы со здоровьем
    CALL CheckHealthAlerts();
    
    -- Проверяем вакцинацию
    CALL CheckVaccinationAlerts();
    
    -- Проверяем кормление
    CALL CheckFeedingAlerts();
    
    -- Возвращаем количество новых алертов
    SELECT 
        COUNT(*) AS total_alerts,
        SUM(CASE WHEN severity = 'CRITICAL' THEN 1 ELSE 0 END) AS critical_alerts,
        SUM(CASE WHEN severity = 'WARNING' THEN 1 ELSE 0 END) AS warning_alerts,
        SUM(CASE WHEN severity = 'INFO' THEN 1 ELSE 0 END) AS info_alerts
    FROM monitoring_logs 
    WHERE DATE(alert_timestamp) = CURDATE() AND resolved = FALSE;
END //

-- Процедура для получения активных алертов
CREATE PROCEDURE GetActiveAlerts()
BEGIN
    SELECT 
        id,
        alert_type,
        severity,
        alert_message,
        DATE_FORMAT(alert_timestamp, '%Y-%m-%d %H:%i:%s') AS timestamp,
        additional_info
    FROM monitoring_logs
    WHERE resolved = FALSE
    ORDER BY severity DESC, alert_timestamp DESC;
END //

-- Процедура для отметки алерта как решенного
CREATE PROCEDURE ResolveAlert(
    IN p_alert_id INT,
    IN p_resolved_by VARCHAR(100)
)
BEGIN
    UPDATE monitoring_logs
    SET resolved = TRUE,
        resolution_timestamp = CURRENT_TIMESTAMP,
        resolved_by = p_resolved_by
    WHERE id = p_alert_id AND resolved = FALSE;
    
    SELECT ROW_COUNT() AS rows_affected;
END //

-- Представление для получения дашборда мониторинга
CREATE VIEW monitoring_dashboard AS
SELECT 
    (SELECT COUNT(*) FROM animals WHERE departure_date IS NULL) AS total_animals,
    (SELECT COUNT(*) FROM animals WHERE health_status != 'healthy' AND departure_date IS NULL) AS unhealthy_animals,
    (SELECT COUNT(*) FROM vaccinations WHERE expiration_date < CURDATE()) AS expired_vaccinations,
    (SELECT COUNT(*) FROM animals WHERE last_feeding_date < CURDATE()) AS not_fed_today,
    (SELECT COUNT(*) FROM monitoring_logs WHERE resolved = FALSE) AS active_alerts,
    (SELECT COUNT(*) FROM medical_records WHERE record_date > DATE_SUB(CURDATE(), INTERVAL 7 DAY)) AS recent_medical_checks,
    (SELECT COUNT(*) FROM feedings WHERE feeding_date = CURDATE()) AS today_feedings
FROM dual;

DELIMITER ;

-- Пример cron-задания для автоматического мониторинга
/*
# Ежедневная проверка состояния базы данных зоопарка
# Выполнять каждый день в 8:00 утра
0 8 * * * mysql -u username -p'password' animals_db -e "CALL RunSystemMonitoring();"

# Проверка каждые 6 часов в течение дня
0 */6 * * * mysql -u username -p'password' animals_db -e "CALL CheckHealthAlerts(); CALL CheckVaccinationAlerts();"
*/

-- Пример bash-скрипта для мониторинга и отправки уведомлений
/*
#!/bin/bash

# Параметры подключения к базе данных
DB_USER="username"
DB_PASS="password"
DB_NAME="animals_db"

# Выполнение проверки системы
mysql -u $DB_USER -p$DB_PASS $DB_NAME -e "CALL RunSystemMonitoring();" > /tmp/monitoring_result.txt

# Проверка наличия критических алертов
CRITICAL_ALERTS=$(mysql -u $DB_USER -p$DB_PASS $DB_NAME -sN -e "SELECT COUNT(*) FROM monitoring_logs WHERE severity = 'CRITICAL' AND resolved = FALSE AND DATE(alert_timestamp) = CURDATE();")

if [ $CRITICAL_ALERTS -gt 0 ]; then
    # Отправка уведомления о критических алертах
    echo "Обнаружены критические алерты в системе зоопарка!" | mail -s "КРИТИЧЕСКИЕ АЛЕРТЫ - Система зоопарка" admin@zoo.example.com
fi

# Проверка наличия предупреждений
WARNING_ALERTS=$(mysql -u $DB_USER -p$DB_PASS $DB_NAME -sN -e "SELECT COUNT(*) FROM monitoring_logs WHERE severity = 'WARNING' AND resolved = FALSE AND DATE(alert_timestamp) = CURDATE();")

if [ $WARNING_ALERTS -gt 0 ]; then
    # Отправка уведомления о предупреждениях
    echo "Обнаружены предупреждения в системе зоопарка!" | mail -s "ПРЕДУПРЕЖДЕНИЯ - Система зоопарка" staff@zoo.example.com
fi
*/