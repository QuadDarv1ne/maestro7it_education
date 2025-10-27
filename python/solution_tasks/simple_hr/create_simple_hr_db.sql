/**
 * 📜 SQL-скрипт: create_simple_hr_db.sql
 **/

-- 1. Создание базы данных (если не существует)
CREATE DATABASE IF NOT EXISTS simple_hr_db
  CHARACTER SET utf8mb4
  COLLATE utf8mb4_unicode_ci;

-- 2. Используем базу данных
USE simple_hr_db;

-- 3. Таблица пользователей (авторизация)
CREATE TABLE IF NOT EXISTS `user` (
    id INT PRIMARY KEY AUTO_INCREMENT,
    username VARCHAR(80) NOT NULL UNIQUE,
    password_hash VARCHAR(256) NOT NULL,
    role ENUM('admin', 'hr') NOT NULL
) ENGINE=InnoDB;

-- 4. Подразделения
CREATE TABLE IF NOT EXISTS `department` (
    id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(100) NOT NULL UNIQUE
) ENGINE=InnoDB;

-- 5. Должности
CREATE TABLE IF NOT EXISTS `position` (
    id INT PRIMARY KEY AUTO_INCREMENT,
    title VARCHAR(100) NOT NULL UNIQUE
) ENGINE=InnoDB;

-- 6. Сотрудники
CREATE TABLE IF NOT EXISTS `employee` (
    id INT PRIMARY KEY AUTO_INCREMENT,
    full_name VARCHAR(150) NOT NULL,
    email VARCHAR(120) NOT NULL UNIQUE,
    employee_id VARCHAR(50) NOT NULL UNIQUE COMMENT 'Табельный номер',
    hire_date DATE NOT NULL,
    status ENUM('active', 'dismissed') NOT NULL DEFAULT 'active',
    department_id INT NOT NULL,
    position_id INT NOT NULL,
    
    -- Внешние ключи
    FOREIGN KEY (department_id) REFERENCES department(id)
        ON DELETE RESTRICT ON UPDATE CASCADE,
    FOREIGN KEY (position_id) REFERENCES position(id)
        ON DELETE RESTRICT ON UPDATE CASCADE
) ENGINE=InnoDB;

-- 7. Кадровые приказы
CREATE TABLE IF NOT EXISTS `order` (
    id INT PRIMARY KEY AUTO_INCREMENT,
    employee_id INT NOT NULL,
    type ENUM('hire', 'transfer', 'dismissal') NOT NULL,
    date_issued DATE NOT NULL,
    new_department_id INT NULL,
    new_position_id INT NULL,
    
    -- Внешние ключи
    FOREIGN KEY (employee_id) REFERENCES employee(id)
        ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (new_department_id) REFERENCES department(id)
        ON DELETE SET NULL ON UPDATE CASCADE,
    FOREIGN KEY (new_position_id) REFERENCES position(id)
        ON DELETE SET NULL ON UPDATE CASCADE
) ENGINE=InnoDB;

-- 8. Отпуска
CREATE TABLE IF NOT EXISTS `vacation` (
    id INT PRIMARY KEY AUTO_INCREMENT,
    employee_id INT NOT NULL,
    start_date DATE NOT NULL,
    end_date DATE NOT NULL,
    type ENUM('paid', 'unpaid', 'sick') NOT NULL,
    
    -- Проверка: дата окончания >= даты начала (реализуется на уровне приложения, т.к. MySQL < 8.0.16 не поддерживает CHECK)
    FOREIGN KEY (employee_id) REFERENCES employee(id)
        ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB;

-- 9. Уведомления
CREATE TABLE IF NOT EXISTS `notification` (
    id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT NOT NULL,
    title VARCHAR(200) NOT NULL,
    message TEXT NOT NULL,
    is_read BOOLEAN DEFAULT FALSE NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
    
    FOREIGN KEY (user_id) REFERENCES user(id)
        ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB;

-- 10. Аудит действий пользователей
CREATE TABLE IF NOT EXISTS `audit_log` (
    id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT NOT NULL,
    action VARCHAR(100) NOT NULL,
    entity_type VARCHAR(50) NOT NULL,
    entity_id INT NULL,
    description TEXT NULL,
    ip_address VARCHAR(45) NULL,
    user_agent TEXT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
    
    FOREIGN KEY (user_id) REFERENCES user(id)
        ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB;

-- 11. Индексы для ускорения поиска и фильтрации
CREATE INDEX idx_employee_status ON employee(status);
CREATE INDEX idx_employee_department ON employee(department_id);
CREATE INDEX idx_employee_name ON employee(full_name);
CREATE INDEX idx_vacation_dates ON vacation(start_date, end_date);
CREATE INDEX idx_order_date ON `order`(date_issued);
CREATE INDEX idx_notification_user ON notification(user_id);
CREATE INDEX idx_notification_created ON notification(created_at);
CREATE INDEX idx_audit_user ON audit_log(user_id);
CREATE INDEX idx_audit_action ON audit_log(action);
CREATE INDEX idx_audit_entity ON audit_log(entity_type, entity_id);
CREATE INDEX idx_audit_created ON audit_log(created_at);
