-- Хранимые процедуры для часто используемых операций

USE animals_db;

DELIMITER //

-- Процедура для добавления нового животного
CREATE PROCEDURE AddNewAnimal(
    IN p_name VARCHAR(100),
    IN p_species_name VARCHAR(100),
    IN p_birth_date DATE,
    IN p_gender ENUM('male', 'female', 'unknown'),
    IN p_health_status VARCHAR(100),
    IN p_arrival_date DATE,
    IN p_enclosure_name VARCHAR(100),
    IN p_mother_name VARCHAR(100),
    IN p_father_name VARCHAR(100)
)
BEGIN
    DECLARE v_species_id INT;
    DECLARE v_enclosure_id INT;
    DECLARE v_mother_id INT DEFAULT NULL;
    DECLARE v_father_id INT DEFAULT NULL;
    
    -- Получаем ID вида
    SELECT id INTO v_species_id FROM species WHERE name = p_species_name;
    
    -- Получаем ID вольера
    SELECT id INTO v_enclosure_id FROM enclosures WHERE name = p_enclosure_name;
    
    -- Получаем ID матери если указана
    IF p_mother_name IS NOT NULL THEN
        SELECT id INTO v_mother_id FROM animals WHERE name = p_mother_name;
    END IF;
    
    -- Получаем ID отца если указан
    IF p_father_name IS NOT NULL THEN
        SELECT id INTO v_father_id FROM animals WHERE name = p_father_name;
    END IF;
    
    -- Добавляем животное
    INSERT INTO animals (name, species_id, birth_date, gender, health_status, arrival_date, enclosure_id, mother_id, father_id)
    VALUES (p_name, v_species_id, p_birth_date, p_gender, p_health_status, p_arrival_date, v_enclosure_id, v_mother_id, v_father_id);
    
    -- Добавляем запись в историю вольеров
    INSERT INTO animal_enclosures (animal_id, enclosure_id, start_date)
    VALUES (LAST_INSERT_ID(), v_enclosure_id, p_arrival_date);
END //

-- Процедура для добавления кормления
CREATE PROCEDURE AddFeeding(
    IN p_animal_name VARCHAR(100),
    IN p_employee_name VARCHAR(100),
    IN p_food_type VARCHAR(200),
    IN p_quantity VARCHAR(50),
    IN p_feeding_time TIME,
    IN p_feeding_date DATE,
    IN p_notes TEXT
)
BEGIN
    DECLARE v_animal_id INT;
    DECLARE v_employee_id INT;
    
    -- Получаем ID животного
    SELECT id INTO v_animal_id FROM animals WHERE name = p_animal_name;
    
    -- Получаем ID сотрудника
    SELECT id INTO v_employee_id FROM employees 
    WHERE CONCAT(first_name, ' ', last_name) = p_employee_name 
    OR CONCAT(last_name, ' ', first_name) = p_employee_name;
    
    -- Добавляем запись о кормлении
    INSERT INTO feedings (animal_id, employee_id, food_type, quantity, feeding_time, feeding_date, notes)
    VALUES (v_animal_id, v_employee_id, p_food_type, p_quantity, p_feeding_time, p_feeding_date, p_notes);
END //

-- Процедура для добавления медицинской записи
CREATE PROCEDURE AddMedicalRecord(
    IN p_animal_name VARCHAR(100),
    IN p_vet_name VARCHAR(100),
    IN p_record_date DATE,
    IN p_diagnosis TEXT,
    IN p_treatment TEXT,
    IN p_medication VARCHAR(200),
    IN p_next_checkup DATE
)
BEGIN
    DECLARE v_animal_id INT;
    DECLARE v_vet_id INT;
    
    -- Получаем ID животного
    SELECT id INTO v_animal_id FROM animals WHERE name = p_animal_name;
    
    -- Получаем ID ветеринара
    SELECT id INTO v_vet_id FROM employees 
    WHERE CONCAT(first_name, ' ', last_name) = p_vet_name 
    OR CONCAT(last_name, ' ', first_name) = p_vet_name;
    
    -- Добавляем медицинскую запись
    INSERT INTO medical_records (animal_id, vet_id, record_date, diagnosis, treatment, medication, next_checkup)
    VALUES (v_animal_id, v_vet_id, p_record_date, p_diagnosis, p_treatment, p_medication, p_next_checkup);
    
    -- Обновляем дату последнего медицинского осмотра у животного
    UPDATE animals SET last_medical_check = p_record_date WHERE id = v_animal_id;
END //

-- Процедура для получения отчета о здоровье животных
CREATE PROCEDURE GetHealthReport()
BEGIN
    SELECT 
        a.name AS animal_name,
        s.name AS species,
        a.health_status,
        a.last_medical_check,
        CASE 
            WHEN a.health_status != 'healthy' THEN 'ТРЕБУЕТ ВНИМАНИЯ'
            WHEN a.last_medical_check IS NULL OR a.last_medical_check < DATE_SUB(CURDATE(), INTERVAL 6 MONTH) THEN 'НЕОБХОДИМ ОСМОТР'
            ELSE 'НОРМА'
        END AS status_comment
    FROM animals a
    JOIN species s ON a.species_id = s.id
    WHERE a.departure_date IS NULL
    ORDER BY status_comment, a.health_status;
END //

-- Процедура для получения списка животных, нуждающихся в вакцинации
CREATE PROCEDURE GetVaccinationDueList()
BEGIN
    SELECT 
        a.name AS animal_name,
        s.name AS species,
        v.vaccine_name,
        v.expiration_date,
        CASE 
            WHEN v.expiration_date < CURDATE() THEN 'ПРОСРОЧЕНО'
            WHEN v.expiration_date <= DATE_ADD(CURDATE(), INTERVAL 30 DAY) THEN 'СКОРО ИСТЕКАЕТ'
            ELSE 'ДЕЙСТВУЕТ'
        END AS status
    FROM vaccinations v
    JOIN animals a ON v.animal_id = a.id
    JOIN species s ON a.species_id = s.id
    WHERE v.expiration_date IS NOT NULL
    ORDER BY v.expiration_date ASC;
END //

DELIMITER ;