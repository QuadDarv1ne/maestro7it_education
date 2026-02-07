-- Триггеры и ограничения для обеспечения целостности данных

USE animals_db;

-- Триггер для проверки, что дата рождения животного не позже даты прибытия
DELIMITER //
CREATE TRIGGER check_birth_before_arrival 
BEFORE INSERT ON animals
FOR EACH ROW
BEGIN
    IF NEW.birth_date > NEW.arrival_date THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Дата рождения не может быть позже даты прибытия';
    END IF;
END //

-- Триггер для обновления даты последнего кормления при добавлении новой записи о кормлении
CREATE TRIGGER update_last_feeding 
AFTER INSERT ON feedings
FOR EACH ROW
BEGIN
    UPDATE animals 
    SET last_feeding_date = NEW.feeding_date 
    WHERE id = NEW.animal_id;
END //

-- Триггер для проверки, что дата вакцинации не позже текущей даты
CREATE TRIGGER check_vaccination_date 
BEFORE INSERT ON vaccinations
FOR EACH ROW
BEGIN
    IF NEW.vaccination_date > CURDATE() THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Дата вакцинации не может быть в будущем';
    END IF;
END //

-- Триггер для проверки, что дата медицинской записи не позже текущей даты
CREATE TRIGGER check_medical_record_date 
BEFORE INSERT ON medical_records
FOR EACH ROW
BEGIN
    IF NEW.record_date > CURDATE() THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Дата медицинской записи не может быть в будущем';
    END IF;
END //

-- Триггер для проверки, что дата найма сотрудника не позже текущей даты
CREATE TRIGGER check_employee_hire_date 
BEFORE INSERT ON employees
FOR EACH ROW
BEGIN
    IF NEW.hire_date > CURDATE() THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Дата найма не может быть в будущем';
    END IF;
END //

-- Добавление столбцов для отслеживания последнего кормления и медицинской проверки
ALTER TABLE animals 
ADD COLUMN last_feeding_date DATE,
ADD COLUMN last_medical_check DATE;

-- Ограничения для проверки значений
ALTER TABLE animals 
ADD CONSTRAINT chk_gender CHECK (gender IN ('male', 'female', 'unknown')),
ADD CONSTRAINT chk_health_status CHECK (health_status IN ('healthy', 'sick', 'injured', 'under observation'));

ALTER TABLE enclosures 
ADD CONSTRAINT chk_capacity CHECK (capacity >= 0),
ADD CONSTRAINT chk_area CHECK (area >= 0);

-- Ограничение для проверки, что дата окончания не раньше даты начала в истории вольеров
ALTER TABLE animal_enclosures 
ADD CONSTRAINT chk_dates CHECK (end_date IS NULL OR end_date >= start_date);

DELIMITER ;