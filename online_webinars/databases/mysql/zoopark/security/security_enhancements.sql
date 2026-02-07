-- Улучшения безопасности для базы данных зоопарка

USE animals_db;

-- 1. Создание ролей для различных уровней доступа
-- Роль для обычных сотрудников (только чтение и ограниченная запись)
CREATE ROLE IF NOT EXISTS 'zoo_employee';
GRANT SELECT ON animals_db.* TO 'zoo_employee';
GRANT INSERT, UPDATE ON animals_db.feedings TO 'zoo_employee';
GRANT INSERT ON animals_db.animal_enclosures TO 'zoo_employee';

-- Роль для ветеринаров (доступ к медицинским записям)
CREATE ROLE IF NOT EXISTS 'zoo_veterinarian';
GRANT SELECT ON animals_db.* TO 'zoo_veterinarian';
GRANT INSERT, UPDATE ON animals_db.medical_records TO 'zoo_veterinarian';
GRANT INSERT, UPDATE ON animals_db.vaccinations TO 'zoo_veterinarian';

-- Роль для менеджеров (широкий доступ к данным)
CREATE ROLE IF NOT EXISTS 'zoo_manager';
GRANT SELECT, INSERT, UPDATE ON animals_db.animals TO 'zoo_manager';
GRANT SELECT, INSERT, UPDATE ON animals_db.enclosures TO 'zoo_manager';
GRANT SELECT, INSERT, UPDATE ON animals_db.employees TO 'zoo_manager';

-- Роль для администраторов (полный доступ)
CREATE ROLE IF NOT EXISTS 'zoo_admin';
GRANT ALL PRIVILEGES ON animals_db.* TO 'zoo_admin';

-- 2. Создание таблицы для аудита изменений
CREATE TABLE IF NOT EXISTS audit_log (
    id INT PRIMARY KEY AUTO_INCREMENT,
    table_name VARCHAR(100) NOT NULL,
    operation_type ENUM('INSERT', 'UPDATE', 'DELETE') NOT NULL,
    record_id INT,
    user_name VARCHAR(100),
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    old_values JSON,
    new_values JSON
);

-- 3. Добавление триггеров для аудита (пример для таблицы animals)
DELIMITER //

-- Триггер для логирования изменений в таблице animals
CREATE TRIGGER animals_audit_trigger
AFTER UPDATE ON animals
FOR EACH ROW
BEGIN
    INSERT INTO audit_log (table_name, operation_type, record_id, user_name, old_values, new_values)
    VALUES (
        'animals', 
        'UPDATE', 
        NEW.id, 
        USER(),
        JSON_OBJECT(
            'name', OLD.name,
            'health_status', OLD.health_status,
            'arrival_date', OLD.arrival_date
        ),
        JSON_OBJECT(
            'name', NEW.name,
            'health_status', NEW.health_status,
            'arrival_date', NEW.arrival_date
        )
    );
END //

-- Триггер для логирования удалений в таблице animals
CREATE TRIGGER animals_delete_audit_trigger
AFTER DELETE ON animals
FOR EACH ROW
BEGIN
    INSERT INTO audit_log (table_name, operation_type, record_id, user_name, old_values)
    VALUES (
        'animals', 
        'DELETE', 
        OLD.id, 
        USER(),
        JSON_OBJECT(
            'name', OLD.name,
            'species_id', OLD.species_id,
            'birth_date', OLD.birth_date,
            'health_status', OLD.health_status
        )
    );
END //

DELIMITER ;

-- 4. Добавление дополнительных ограничений для обеспечения целостности данных
-- Проверка, что дата рождения не может быть в будущем
ALTER TABLE animals 
ADD CONSTRAINT chk_birth_date_not_future 
CHECK (birth_date <= CURDATE());

-- Проверка, что дата прибытия не может быть в будущем
ALTER TABLE animals 
ADD CONSTRAINT chk_arrival_date_not_future 
CHECK (arrival_date <= CURDATE());

-- Проверка, что дата увольнения сотрудника (если есть) не в прошлом
ALTER TABLE employees 
ADD COLUMN termination_date DATE NULL;
ALTER TABLE employees 
ADD CONSTRAINT chk_termination_date_valid 
CHECK (termination_date IS NULL OR termination_date >= hire_date);

-- 5. Создание индексов для улучшения производительности аудита
CREATE INDEX idx_audit_log_timestamp ON audit_log(timestamp);
CREATE INDEX idx_audit_log_table_operation ON audit_log(table_name, operation_type);