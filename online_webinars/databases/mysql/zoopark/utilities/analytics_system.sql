-- Система аналитики и отчетности для базы данных зоопарка

USE animals_db;

-- Таблица для хранения настроек отчетов
CREATE TABLE IF NOT EXISTS report_settings (
    id INT PRIMARY KEY AUTO_INCREMENT,
    report_name VARCHAR(255) NOT NULL,
    report_title VARCHAR(500) NOT NULL,
    description TEXT,
    sql_query TEXT NOT NULL,
    frequency ENUM('daily', 'weekly', 'monthly', 'quarterly', 'yearly') DEFAULT 'monthly',
    recipients TEXT,  -- email адреса получателей, через запятую
    is_active BOOLEAN DEFAULT TRUE,
    created_by VARCHAR(100),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- Таблица для хранения результатов аналитики
CREATE TABLE IF NOT EXISTS analytics_results (
    id INT PRIMARY KEY AUTO_INCREMENT,
    report_name VARCHAR(255) NOT NULL,
    generation_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    result_data JSON,
    result_summary TEXT,
    generated_by VARCHAR(100),
    file_path VARCHAR(500),  -- путь к файлу отчета, если был сгенерирован
    execution_time_ms INT
);

-- Представление для анализа популяции животных
CREATE VIEW animal_population_analytics AS
SELECT 
    s.name AS species_name,
    s.latin_name,
    s.class,
    s.conservation_status,
    COUNT(a.id) AS total_count,
    SUM(CASE WHEN a.gender = 'male' THEN 1 ELSE 0 END) AS male_count,
    SUM(CASE WHEN a.gender = 'female' THEN 1 ELSE 0 END) AS female_count,
    SUM(CASE WHEN a.health_status != 'healthy' THEN 1 ELSE 0 END) AS unhealthy_count,
    AVG(TIMESTAMPDIFF(YEAR, a.birth_date, CURDATE())) AS average_age,
    MIN(a.birth_date) AS oldest_animal_born,
    MAX(a.birth_date) AS youngest_animal_born
FROM species s
LEFT JOIN animals a ON s.id = a.species_id AND a.departure_date IS NULL
GROUP BY s.id, s.name, s.latin_name, s.class, s.conservation_status;

-- Представление для анализа кормления
CREATE VIEW feeding_analytics AS
SELECT 
    s.name AS species_name,
    COUNT(f.id) AS total_feedings,
    COUNT(DISTINCT f.animal_id) AS animals_fed,
    AVG(CAST(REPLACE(f.quantity, ' kg', '') AS DECIMAL(10,2))) AS avg_food_per_feeding,
    COUNT(CASE WHEN f.feeding_date = CURDATE() THEN 1 END) AS today_feedings,
    COUNT(CASE WHEN f.feeding_date = DATE_SUB(CURDATE(), INTERVAL 1 DAY) THEN 1 END) AS yesterday_feedings,
    COUNT(CASE WHEN f.feeding_date BETWEEN DATE_SUB(CURDATE(), INTERVAL 7 DAY) AND CURDATE() THEN 1 END) AS week_feedings
FROM feedings f
JOIN animals a ON f.animal_id = a.id
JOIN species s ON a.species_id = s.id
WHERE f.feeding_date >= DATE_SUB(CURDATE(), INTERVAL 30 DAY)
GROUP BY s.id, s.name;

-- Представление для анализа медицинских данных
CREATE VIEW medical_analytics AS
SELECT 
    s.name AS species_name,
    COUNT(mr.id) AS total_medical_records,
    COUNT(DISTINCT mr.animal_id) AS treated_animals,
    COUNT(CASE WHEN mr.diagnosis LIKE '%routine%' OR mr.diagnosis LIKE '%checkup%' THEN 1 END) AS routine_checkups,
    COUNT(CASE WHEN mr.diagnosis LIKE '%sick%' OR mr.diagnosis LIKE '%ill%' OR a.health_status != 'healthy' THEN 1 END) AS sick_animals_treated,
    AVG(CASE WHEN mr.next_checkup IS NOT NULL THEN DATEDIFF(mr.next_checkup, mr.record_date) END) AS avg_follow_up_days
FROM medical_records mr
JOIN animals a ON mr.animal_id = a.id
JOIN species s ON a.species_id = s.id
GROUP BY s.id, s.name;

-- Представление для анализа вакцинации
CREATE VIEW vaccination_analytics AS
SELECT 
    s.name AS species_name,
    COUNT(v.id) AS total_vaccinations,
    COUNT(DISTINCT v.animal_id) AS vaccinated_animals,
    COUNT(CASE WHEN v.expiration_date < CURDATE() THEN 1 END) AS expired_vaccinations,
    COUNT(CASE WHEN v.expiration_date BETWEEN CURDATE() AND DATE_ADD(CURDATE(), INTERVAL 30 DAY) THEN 1 END) AS due_soon_vaccinations,
    COUNT(CASE WHEN v.vaccination_date >= DATE_SUB(CURDATE(), INTERVAL 30 DAY) THEN 1 END) AS recent_vaccinations
FROM vaccinations v
JOIN animals a ON v.animal_id = a.id
JOIN species s ON a.species_id = s.id
GROUP BY s.id, s.name;

-- Представление для анализа эффективности сотрудников
CREATE VIEW employee_performance_analytics AS
SELECT 
    e.id AS employee_id,
    CONCAT(e.first_name, ' ', e.last_name) AS employee_name,
    e.position,
    COUNT(DISTINCT f.animal_id) AS animals_fed,
    COUNT(f.id) AS total_feedings,
    COUNT(DISTINCT mr.animal_id) AS animals_medically_attended,
    COUNT(mr.id) AS total_medical_records,
    COUNT(DISTINCT v.animal_id) AS animals_vaccinated,
    COUNT(v.id) AS total_vaccinations,
    DATEDIFF(CURDATE(), e.hire_date) AS days_employed
FROM employees e
LEFT JOIN feedings f ON e.id = f.employee_id AND f.feeding_date >= DATE_SUB(CURDATE(), INTERVAL 30 DAY)
LEFT JOIN medical_records mr ON e.id = mr.vet_id AND mr.record_date >= DATE_SUB(CURDATE(), INTERVAL 30 DAY)
LEFT JOIN vaccinations v ON e.id = v.administered_by AND v.vaccination_date >= DATE_SUB(CURDATE(), INTERVAL 30 DAY)
GROUP BY e.id, e.first_name, e.last_name, e.position, e.hire_date;

-- Представление для анализа вольеров
CREATE VIEW enclosure_analytics AS
SELECT 
    e.id AS enclosure_id,
    e.name AS enclosure_name,
    e.type AS enclosure_type,
    e.area,
    e.capacity,
    COUNT(a.id) AS current_animals,
    CASE 
        WHEN e.capacity > 0 THEN ROUND((COUNT(a.id) / e.capacity) * 100, 2)
        ELSE 0 
    END AS occupancy_percentage,
    GROUP_CONCAT(DISTINCT s.name) AS species_present,
    COUNT(DISTINCT ee.employee_id) AS assigned_employees
FROM enclosures e
LEFT JOIN animals a ON e.id = a.enclosure_id AND a.departure_date IS NULL
LEFT JOIN species s ON a.species_id = s.id
LEFT JOIN employee_enclosures ee ON e.id = ee.enclosure_id
GROUP BY e.id, e.name, e.type, e.area, e.capacity;

-- Процедура для генерации общего отчета о состоянии зоопарка
DELIMITER //
CREATE PROCEDURE GenerateZooStatusReport()
BEGIN
    SELECT 
        (SELECT COUNT(*) FROM animals WHERE departure_date IS NULL) AS total_animals,
        (SELECT COUNT(*) FROM animals WHERE health_status != 'healthy' AND departure_date IS NULL) AS unhealthy_animals,
        (SELECT COUNT(*) FROM species) AS total_species,
        (SELECT COUNT(*) FROM enclosures) AS total_enclosures,
        (SELECT COUNT(*) FROM employees) AS total_employees,
        (SELECT COUNT(*) FROM feedings WHERE feeding_date = CURDATE()) AS today_feedings,
        (SELECT COUNT(*) FROM medical_records WHERE record_date = CURDATE()) AS today_medical_records,
        (SELECT COUNT(*) FROM vaccinations WHERE vaccination_date = CURDATE()) AS today_vaccinations,
        (SELECT COUNT(*) FROM animals WHERE TIMESTAMPDIFF(YEAR, birth_date, CURDATE()) < 1 AND departure_date IS NULL) AS young_animals,
        (SELECT COUNT(*) FROM animals WHERE TIMESTAMPDIFF(YEAR, birth_date, CURDATE()) > 15 AND departure_date IS NULL) AS senior_animals;
END //

-- Процедура для генерации отчета по сохранению видов
CREATE PROCEDURE GenerateConservationReport()
BEGIN
    SELECT 
        conservation_status,
        COUNT(*) AS species_count,
        SUM(animal_count) AS total_animals,
        AVG(animal_count) AS avg_animals_per_species
    FROM (
        SELECT 
            s.conservation_status,
            s.name AS species_name,
            COUNT(a.id) AS animal_count
        FROM species s
        LEFT JOIN animals a ON s.id = a.species_id AND a.departure_date IS NULL
        GROUP BY s.id, s.conservation_status, s.name
    ) AS species_animal_counts
    GROUP BY conservation_status
    ORDER BY 
        CASE conservation_status 
            WHEN 'CR' THEN 1  -- Critically Endangered
            WHEN 'EN' THEN 2  -- Endangered
            WHEN 'VU' THEN 3  -- Vulnerable
            WHEN 'NT' THEN 4  -- Near Threatened
            WHEN 'LC' THEN 5  -- Least Concern
            WHEN 'DD' THEN 6  -- Data Deficient
            WHEN 'EX' THEN 7  -- Extinct
            ELSE 8
        END;
END //

-- Процедура для генерации отчета по эффективности кормления
CREATE PROCEDURE GenerateFeedingEfficiencyReport()
BEGIN
    SELECT 
        s.name AS species,
        COUNT(f.id) AS total_feedings,
        COUNT(DISTINCT f.animal_id) AS fed_animals,
        ROUND(AVG(CAST(REPLACE(f.quantity, ' kg', '') AS DECIMAL(10,2))), 2) AS avg_food_kg,
        MIN(f.quantity) AS min_food,
        MAX(f.quantity) AS max_food,
        CONCAT(ROUND(COUNT(f.id) / COUNT(DISTINCT f.animal_id), 2), ' feedings per animal') AS feedings_per_animal
    FROM feedings f
    JOIN animals a ON f.animal_id = a.id
    JOIN species s ON a.species_id = s.id
    WHERE f.feeding_date >= DATE_SUB(CURDATE(), INTERVAL 30 DAY)
    GROUP BY s.id, s.name
    ORDER BY total_feedings DESC;
END //

-- Процедура для генерации отчета по медицинским показателям
CREATE PROCEDURE GenerateMedicalReport()
BEGIN
    SELECT 
        s.name AS species,
        COUNT(mr.id) AS total_visits,
        COUNT(DISTINCT mr.animal_id) AS treated_animals,
        ROUND((COUNT(DISTINCT mr.animal_id) / (SELECT COUNT(*) FROM animals WHERE species_id = s.id AND departure_date IS NULL)) * 100, 2) AS treatment_coverage_percent,
        AVG(CASE WHEN mr.next_checkup IS NOT NULL THEN DATEDIFF(mr.next_checkup, mr.record_date) END) AS avg_follow_up_days,
        GROUP_CONCAT(DISTINCT mr.diagnosis SEPARATOR '; ') AS common_diagnoses
    FROM medical_records mr
    JOIN animals a ON mr.animal_id = a.id
    JOIN species s ON a.species_id = s.id
    WHERE mr.record_date >= DATE_SUB(CURDATE(), INTERVAL 90 DAY)
    GROUP BY s.id, s.name
    ORDER BY total_visits DESC;
END //

-- Процедура для сохранения результата аналитики
CREATE PROCEDURE SaveAnalyticsResult(
    IN p_report_name VARCHAR(255),
    IN p_result_summary TEXT,
    IN p_generated_by VARCHAR(100),
    IN p_execution_time_ms INT
)
BEGIN
    INSERT INTO analytics_results (report_name, result_summary, generated_by, execution_time_ms)
    VALUES (p_report_name, p_result_summary, p_generated_by, p_execution_time_ms);
END //

DELIMITER ;

-- Примеры запросов для получения аналитической информации

/*
-- Получить общий отчет о состоянии зоопарка
CALL GenerateZooStatusReport();

-- Получить отчет по сохранению видов
CALL GenerateConservationReport();

-- Получить отчет по эффективности кормления
CALL GenerateFeedingEfficiencyReport();

-- Получить отчет по медицинским показателям
CALL GenerateMedicalReport();

-- Посмотреть аналитику по популяции животных
SELECT * FROM animal_population_analytics;

-- Посмотреть аналитику по кормлению
SELECT * FROM feeding_analytics;

-- Посмотреть медицинскую аналитику
SELECT * FROM medical_analytics;

-- Посмотреть аналитику по вакцинации
SELECT * FROM vaccination_analytics;

-- Посмотреть аналитику по эффективности сотрудников
SELECT * FROM employee_performance_analytics;

-- Посмотреть аналитику по вольерам
SELECT * FROM enclosure_analytics;
*/