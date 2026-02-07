-- Система аутентификации и авторизации пользователей для базы данных зоопарка

USE animals_db;

-- Таблица пользователей системы (отдельно от сотрудников зоопарка)
CREATE TABLE IF NOT EXISTS system_users (
    id INT PRIMARY KEY AUTO_INCREMENT,
    username VARCHAR(100) UNIQUE NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    first_name VARCHAR(100),
    last_name VARCHAR(100),
    employee_id INT,  -- Связь с таблицей сотрудников зоопарка
    role ENUM('admin', 'veterinarian', 'keeper', 'nutritionist', 'manager', 'readonly') DEFAULT 'readonly',
    is_active BOOLEAN DEFAULT TRUE,
    last_login TIMESTAMP NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (employee_id) REFERENCES employees(id)
);

-- Таблица ролей и разрешений
CREATE TABLE IF NOT EXISTS roles_permissions (
    id INT PRIMARY KEY AUTO_INCREMENT,
    role_name ENUM('admin', 'veterinarian', 'keeper', 'nutritionist', 'manager', 'readonly') NOT NULL,
    permission_name VARCHAR(100) NOT NULL,
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Таблица для хранения логов аутентификации
CREATE TABLE IF NOT EXISTS auth_logs (
    id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT,
    username VARCHAR(100),
    action ENUM('login', 'logout', 'failed_login', 'permission_denied') NOT NULL,
    ip_address VARCHAR(45),
    user_agent TEXT,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    details JSON,
    FOREIGN KEY (user_id) REFERENCES system_users(id)
);

-- Заполнение таблицы разрешений для различных ролей
INSERT INTO roles_permissions (role_name, permission_name, description) VALUES
-- Администратор: полный доступ
('admin', 'animals_read', 'Просмотр информации о животных'),
('admin', 'animals_create', 'Создание новых животных'),
('admin', 'animals_update', 'Изменение информации о животных'),
('admin', 'animals_delete', 'Удаление животных'),
('admin', 'medical_read', 'Просмотр медицинских записей'),
('admin', 'medical_create', 'Создание медицинских записей'),
('admin', 'medical_update', 'Изменение медицинских записей'),
('admin', 'feeding_read', 'Просмотр записей о кормлениях'),
('admin', 'feeding_create', 'Создание записей о кормлениях'),
('admin', 'feeding_update', 'Изменение записей о кормлениях'),
('admin', 'vaccination_read', 'Просмотр вакцинаций'),
('admin', 'vaccination_create', 'Создание вакцинаций'),
('admin', 'vaccination_update', 'Изменение вакцинаций'),
('admin', 'users_manage', 'Управление пользователями системы'),
('admin', 'reports_generate', 'Генерация отчетов'),

-- Ветеринар: доступ к медицинской информации
('veterinarian', 'animals_read', 'Просмотр информации о животных'),
('veterinarian', 'medical_read', 'Просмотр медицинских записей'),
('veterinarian', 'medical_create', 'Создание медицинских записей'),
('veterinarian', 'medical_update', 'Изменение медицинских записей'),
('veterinarian', 'vaccination_read', 'Просмотр вакцинаций'),
('veterinarian', 'vaccination_create', 'Создание вакцинаций'),
('veterinarian', 'vaccination_update', 'Изменение вакцинаций'),
('veterinarian', 'reports_generate', 'Генерация медицинских отчетов'),

-- Смотритель: доступ к информации о животных и кормлениях
('keeper', 'animals_read', 'Просмотр информации о животных'),
('keeper', 'feeding_read', 'Просмотр записей о кормлениях'),
('keeper', 'feeding_create', 'Создание записей о кормлениях'),
('keeper', 'feeding_update', 'Изменение записей о кормлениях'),
('keeper', 'reports_generate', 'Генерация отчетов о кормлениях'),

-- Диетолог: доступ к информации о питании
('nutritionist', 'animals_read', 'Просмотр информации о животных'),
('nutritionist', 'feeding_read', 'Просмотр записей о кормлениях'),
('nutritionist', 'feeding_create', 'Создание записей о кормлениях'),
('nutritionist', 'feeding_update', 'Изменение записей о кормлениях'),
('nutritionist', 'diets_read', 'Просмотр информации о диетах'),
('nutritionist', 'diets_create', 'Создание информации о диетах'),
('nutritionist', 'diets_update', 'Изменение информации о диетах'),

-- Менеджер: доступ к отчетам и общей информации
('manager', 'animals_read', 'Просмотр информации о животных'),
('manager', 'reports_generate', 'Генерация отчетов'),
('manager', 'enclosures_read', 'Просмотр информации о вольерах'),

-- Только чтение: ограниченный доступ к информации
('readonly', 'animals_read', 'Просмотр информации о животных');

-- Процедура для регистрации нового пользователя
DELIMITER //
CREATE PROCEDURE RegisterUser(
    IN p_username VARCHAR(100),
    IN p_email VARCHAR(255),
    IN p_password_hash VARCHAR(255),  -- Хэш пароля должен быть подготовлен вне процедуры
    IN p_first_name VARCHAR(100),
    IN p_last_name VARCHAR(100),
    IN p_employee_id INT,
    IN p_role ENUM('admin', 'veterinarian', 'keeper', 'nutritionist', 'manager', 'readonly')
)
BEGIN
    DECLARE EXIT HANDLER FOR SQLEXCEPTION
    BEGIN
        ROLLBACK;
        RESIGNAL;
    END;
    
    START TRANSACTION;
    
    INSERT INTO system_users (username, email, password_hash, first_name, last_name, employee_id, role)
    VALUES (p_username, p_email, p_password_hash, p_first_name, p_last_name, p_employee_id, p_role);
    
    INSERT INTO auth_logs (user_id, username, action, details)
    SELECT id, p_username, 'login', JSON_OBJECT('description', 'User registered and logged in')
    FROM system_users 
    WHERE username = p_username;
    
    COMMIT;
END //

-- Процедура для аутентификации пользователя
CREATE PROCEDURE AuthenticateUser(
    IN p_username VARCHAR(100),
    IN p_password_hash VARCHAR(255),
    OUT p_user_id INT,
    OUT p_role VARCHAR(20),
    OUT p_is_authenticated BOOLEAN
)
BEGIN
    DECLARE user_count INT DEFAULT 0;
    
    SELECT COUNT(*), id, role INTO user_count, p_user_id, p_role
    FROM system_users 
    WHERE username = p_username 
      AND password_hash = p_password_hash 
      AND is_active = TRUE
    GROUP BY id, role;
    
    IF user_count = 1 THEN
        SET p_is_authenticated = TRUE;
        
        -- Логируем успешный вход
        INSERT INTO auth_logs (user_id, username, action, details)
        VALUES (p_user_id, p_username, 'login', 
                JSON_OBJECT('success', TRUE, 'timestamp', NOW()));
                
        -- Обновляем время последнего входа
        UPDATE system_users 
        SET last_login = NOW() 
        WHERE id = p_user_id;
    ELSE
        SET p_is_authenticated = FALSE;
        SET p_user_id = NULL;
        SET p_role = NULL;
        
        -- Логируем неудачную попытку входа
        INSERT INTO auth_logs (username, action, details)
        VALUES (p_username, 'failed_login', 
                JSON_OBJECT('reason', 'Invalid credentials', 'timestamp', NOW()));
    END IF;
END //

-- Процедура для проверки разрешений пользователя
CREATE PROCEDURE CheckPermission(
    IN p_user_id INT,
    IN p_permission_name VARCHAR(100),
    OUT p_has_permission BOOLEAN
)
BEGIN
    DECLARE user_role VARCHAR(20);
    DECLARE permission_count INT DEFAULT 0;
    
    -- Получаем роль пользователя
    SELECT role INTO user_role FROM system_users WHERE id = p_user_id;
    
    -- Проверяем, есть ли у роли такое разрешение
    SELECT COUNT(*) INTO permission_count
    FROM roles_permissions
    WHERE role_name = user_role AND permission_name = p_permission_name;
    
    IF permission_count > 0 THEN
        SET p_has_permission = TRUE;
    ELSE
        SET p_has_permission = FALSE;
    END IF;
END //

-- Процедура для получения информации о пользователе
CREATE PROCEDURE GetUserDetails(
    IN p_user_id INT
)
BEGIN
    SELECT 
        u.id,
        u.username,
        u.email,
        u.first_name,
        u.last_name,
        u.role,
        u.is_active,
        u.last_login,
        e.first_name AS employee_first_name,
        e.last_name AS employee_last_name,
        e.position AS employee_position
    FROM system_users u
    LEFT JOIN employees e ON u.employee_id = e.id
    WHERE u.id = p_user_id;
END //

-- Представление для получения активных пользователей
CREATE VIEW active_users AS
SELECT 
    u.id,
    u.username,
    u.first_name,
    u.last_name,
    u.role,
    u.last_login,
    e.position AS employee_position,
    CASE 
        WHEN u.last_login > DATE_SUB(NOW(), INTERVAL 1 DAY) THEN 'active_today'
        WHEN u.last_login > DATE_SUB(NOW(), INTERVAL 7 DAY) THEN 'active_this_week'
        WHEN u.last_login > DATE_SUB(NOW(), INTERVAL 30 DAY) THEN 'active_this_month'
        ELSE 'inactive'
    END AS activity_status
FROM system_users u
LEFT JOIN employees e ON u.employee_id = e.id
WHERE u.is_active = TRUE;

DELIMITER ;

-- Примеры SQL-запросов для работы с системой аутентификации

/*
-- Пример: Создание администратора системы
CALL RegisterUser(
    'admin_user',                    -- username
    'admin@zoo.example.com',        -- email  
    '$2y$10$example_hash_value',    -- password_hash (пример хэша bcrypt)
    'Admin',                        -- first_name
    'User',                         -- last_name
    NULL,                           -- employee_id (может быть связан с сотрудником)
    'admin'                         -- role
);

-- Пример: Аутентификация пользователя
SET @user_id = NULL;
SET @role = NULL;
SET @is_auth = FALSE;

CALL AuthenticateUser('admin_user', '$2y$10$example_hash_value', @user_id, @role, @is_auth);

SELECT @user_id, @role, @is_auth;

-- Пример: Проверка разрешений
SET @has_perm = FALSE;
CALL CheckPermission(@user_id, 'animals_create', @has_perm);
SELECT @has_perm AS can_create_animals;
*/