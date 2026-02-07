-- Расширенная аналитика для базы данных зоопарка

USE animals_db;

-- 1. Аналитика по популярности животных (на основе обращений сотрудников)
CREATE VIEW animal_popularity_metrics AS
SELECT 
    a.name AS animal_name,
    s.name AS species,
    COUNT(f.id) AS feeding_count_last_month,
    COUNT(mr.id) AS medical_visits_last_month,
    COUNT(v.id) AS vaccination_count_last_year,
    TIMESTAMPDIFF(YEAR, a.birth_date, CURDATE()) AS age_years
FROM animals a
JOIN species s ON a.species_id = s.id
LEFT JOIN feedings f ON a.id = f.animal_id 
    AND f.feeding_date >= DATE_SUB(CURDATE(), INTERVAL 1 MONTH)
LEFT JOIN medical_records mr ON a.id = mr.animal_id 
    AND mr.record_date >= DATE_SUB(CURDATE(), INTERVAL 1 MONTH)
LEFT JOIN vaccinations v ON a.id = v.animal_id 
    AND v.vaccination_date >= DATE_SUB(CURDATE(), INTERVAL 1 YEAR)
WHERE a.departure_date IS NULL
GROUP BY a.id, a.name, s.name, a.birth_date
ORDER BY feeding_count_last_month DESC, medical_visits_last_month DESC;

-- 2. Аналитика по эффективности сотрудников
CREATE VIEW employee_performance_metrics AS
SELECT 
    e.id,
    CONCAT(e.first_name, ' ', e.last_name) AS employee_name,
    e.position,
    COUNT(DISTINCT f.animal_id) AS animals_fed_last_month,
    COUNT(DISTINCT mr.animal_id) AS animals_medically_attended_last_month,
    COUNT(DISTINCT ae.animal_id) AS animals_managed_last_month,
    TIMESTAMPDIFF(YEAR, e.hire_date, CURDATE()) AS years_of_service
FROM employees e
LEFT JOIN feedings f ON e.id = f.employee_id 
    AND f.feeding_date >= DATE_SUB(CURDATE(), INTERVAL 1 MONTH)
LEFT JOIN medical_records mr ON e.id = mr.vet_id 
    AND mr.record_date >= DATE_SUB(CURDATE(), INTERVAL 1 MONTH)
LEFT JOIN animal_enclosures ae ON e.id = ae.animal_id 
    AND ae.start_date >= DATE_SUB(CURDATE(), INTERVAL 1 MONTH)
GROUP BY e.id, e.first_name, e.last_name, e.position, e.hire_date
ORDER BY years_of_service DESC;

-- 3. Аналитика по использованию вольеров
CREATE VIEW enclosure_utilization AS
SELECT 
    e.name AS enclosure_name,
    e.type,
    e.capacity,
    COUNT(a.id) AS current_animals,
    ROUND((COUNT(a.id) / e.capacity) * 100, 2) AS occupancy_percentage,
    GROUP_CONCAT(DISTINCT s.name SEPARATOR ', ') AS species_present
FROM enclosures e
LEFT JOIN animals a ON e.id = a.enclosure_id AND a.departure_date IS NULL
LEFT JOIN species s ON a.species_id = s.id
GROUP BY e.id, e.name, e.type, e.capacity
ORDER BY occupancy_percentage DESC;

-- 4. Аналитика по затратам на содержание
CREATE VIEW cost_analysis AS
SELECT 
    s.name AS species,
    COUNT(a.id) AS animal_count,
    SUM(CASE WHEN d.daily_amount LIKE '%кг%' THEN 
        CAST(REPLACE(d.daily_amount, ' кг', '') AS DECIMAL(10,2)) * 30 
        ELSE 0 END) AS monthly_food_kg_estimate,
    COUNT(mr.id) AS medical_procedures_last_year,
    COUNT(v.id) AS vaccination_procedures_last_year
FROM species s
LEFT JOIN animals a ON s.id = a.species_id AND a.departure_date IS NULL
LEFT JOIN diets d ON s.id = d.species_id
LEFT JOIN medical_records mr ON a.id = mr.animal_id 
    AND mr.record_date >= DATE_SUB(CURDATE(), INTERVAL 1 YEAR)
LEFT JOIN vaccinations v ON a.id = v.animal_id 
    AND v.vaccination_date >= DATE_SUB(CURDATE(), INTERVAL 1 YEAR)
GROUP BY s.id, s.name
HAVING animal_count > 0
ORDER BY animal_count DESC;

-- 5. Аналитика по рождаемости и выживаемости
CREATE VIEW breeding_and_survival AS
SELECT 
    s.name AS species,
    s.conservation_status,
    COUNT(a.id) AS total_animals,
    COUNT(CASE WHEN a.mother_id IS NOT NULL OR a.father_id IS NOT NULL 
         THEN 1 END) AS born_in_zoo,
    AVG(TIMESTAMPDIFF(YEAR, a.birth_date, CURDATE())) AS average_age,
    COUNT(CASE WHEN a.departure_date IS NOT NULL THEN 1 END) AS departed_animals
FROM species s
LEFT JOIN animals a ON s.id = a.species_id
GROUP BY s.id, s.name, s.conservation_status
HAVING total_animals > 0
ORDER BY total_animals DESC;