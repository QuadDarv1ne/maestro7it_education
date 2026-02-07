-- Автоматизированные тесты для проверки корректности работы процедур

USE animals_db;

-- Тест 1: Проверка добавления нового животного
DROP PROCEDURE IF EXISTS test_add_new_animal;
DELIMITER //
CREATE PROCEDURE test_add_new_animal()
BEGIN
    DECLARE animal_count_before INT;
    DECLARE animal_count_after INT;
    DECLARE animal_exists INT DEFAULT 0;
    
    -- Подсчитываем количество животных до добавления
    SELECT COUNT(*) INTO animal_count_before FROM animals;
    
    -- Добавляем тестовое животное
    CALL AddNewAnimal(
        'Тестовое_Животное',      -- имя
        'Лев',                   -- вид
        '2020-01-01',           -- дата рождения
        'male',                  -- пол
        'healthy',               -- состояние здоровья
        '2022-01-01',           -- дата прибытия
        'Львиный вольер',       -- вольер
        NULL,                    -- мать
        NULL                     -- отец
    );
    
    -- Подсчитываем количество животных после добавления
    SELECT COUNT(*) INTO animal_count_after FROM animals;
    
    -- Проверяем, что животное было добавлено
    SELECT COUNT(*) INTO animal_exists FROM animals WHERE name = 'Тестовое_Животное';
    
    -- Выводим результаты теста
    SELECT 
        'Тест добавления животного' AS test_name,
        animal_count_before,
        animal_count_after,
        animal_exists,
        CASE 
            WHEN animal_count_after = animal_count_before + 1 AND animal_exists = 1 
            THEN 'ПРОЙДЕН' 
            ELSE 'НЕ ПРОЙДЕН' 
        END AS test_result;
        
    -- Удаляем тестовое животное
    DELETE FROM animals WHERE name = 'Тестовое_Животное';
END //
DELIMITER ;

-- Тест 2: Проверка добавления кормления
DROP PROCEDURE IF EXISTS test_add_feeding;
DELIMITER //
CREATE PROCEDURE test_add_feeding()
BEGIN
    DECLARE feeding_count_before INT;
    DECLARE feeding_count_after INT;
    DECLARE first_animal_name VARCHAR(100);
    DECLARE first_employee_name VARCHAR(200);
    
    -- Получаем существующее животное и сотрудника
    SELECT a.name INTO first_animal_name 
    FROM animals a 
    LIMIT 1;
    
    SELECT CONCAT(e.first_name, ' ', e.last_name) INTO first_employee_name 
    FROM employees e 
    LIMIT 1;
    
    -- Подсчитываем количество кормлений до добавления
    SELECT COUNT(*) INTO feeding_count_before FROM feedings;
    
    -- Добавляем тестовое кормление
    CALL AddFeeding(
        first_animal_name,        -- имя животного
        first_employee_name,      -- имя сотрудника
        'Тестовая еда',          -- тип еды
        '1 кг',                  -- количество
        '12:00:00',              -- время кормления
        CURDATE(),               -- дата кормления
        'Тестовое кормление'     -- заметки
    );
    
    -- Подсчитываем количество кормлений после добавления
    SELECT COUNT(*) INTO feeding_count_after FROM feedings;
    
    -- Выводим результаты теста
    SELECT 
        'Тест добавления кормления' AS test_name,
        feeding_count_before,
        feeding_count_after,
        CASE 
            WHEN feeding_count_after = feeding_count_before + 1 
            THEN 'ПРОЙДЕН' 
            ELSE 'НЕ ПРОЙДЕН' 
        END AS test_result;
        
    -- Удаляем тестовое кормление
    DELETE FROM feedings 
    WHERE animal_id = (SELECT id FROM animals WHERE name = first_animal_name)
    AND feeding_date = CURDATE()
    AND notes = 'Тестовое кормление'
    LIMIT 1;
END //
DELIMITER ;

-- Тест 3: Проверка добавления медицинской записи
DROP PROCEDURE IF EXISTS test_add_medical_record;
DELIMITER //
CREATE PROCEDURE test_add_medical_record()
BEGIN
    DECLARE record_count_before INT;
    DECLARE record_count_after INT;
    DECLARE first_animal_name VARCHAR(100);
    DECLARE first_vet_name VARCHAR(200);
    
    -- Получаем существующее животное и ветеринара
    SELECT a.name INTO first_animal_name 
    FROM animals a 
    LIMIT 1;
    
    SELECT CONCAT(e.first_name, ' ', e.last_name) INTO first_vet_name 
    FROM employees e 
    WHERE position LIKE '%ветеринар%' OR position LIKE '%вет%'
    LIMIT 1;
    
    -- Если не найден ветеринар, берем любого сотрудника
    IF first_vet_name IS NULL THEN
        SELECT CONCAT(e.first_name, ' ', e.last_name) INTO first_vet_name 
        FROM employees e 
        LIMIT 1;
    END IF;
    
    -- Подсчитываем количество медицинских записей до добавления
    SELECT COUNT(*) INTO record_count_before FROM medical_records;
    
    -- Добавляем тестовую медицинскую запись
    CALL AddMedicalRecord(
        first_animal_name,        -- имя животного
        first_vet_name,           -- имя ветеринара
        CURDATE(),               -- дата осмотра
        'Тестовый диагноз',      -- диагноз
        'Тестовое лечение',      -- лечение
        'Тестовые лекарства',    -- лекарства
        DATE_ADD(CURDATE(), INTERVAL 30 DAY) -- следующая проверка
    );
    
    -- Подсчитываем количество медицинских записей после добавления
    SELECT COUNT(*) INTO record_count_after FROM medical_records;
    
    -- Выводим результаты теста
    SELECT 
        'Тест добавления медицинской записи' AS test_name,
        record_count_before,
        record_count_after,
        CASE 
            WHEN record_count_after = record_count_before + 1 
            THEN 'ПРОЙДЕН' 
            ELSE 'НЕ ПРОЙДЕН' 
        END AS test_result;
        
    -- Удаляем тестовую медицинскую запись
    DELETE FROM medical_records 
    WHERE animal_id = (SELECT id FROM animals WHERE name = first_animal_name)
    AND record_date = CURDATE()
    AND diagnosis = 'Тестовый диагноз'
    LIMIT 1;
END //
DELIMITER ;

-- Запуск всех тестов
SELECT '=== ЗАПУСК АВТОМАТИЗИРОВАННЫХ ТЕСТОВ ===' AS test_header;

CALL test_add_new_animal();
CALL test_add_feeding();
CALL test_add_medical_record();

SELECT '=== ТЕСТИРОВАНИЕ ЗАВЕРШЕНО ===' AS test_footer;