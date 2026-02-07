USE animals_db;

-- 1. Основная информация о животных с деталями вида и вольера
CREATE VIEW animals_full_info AS
SELECT 
    a.id,
    a.name AS animal_name,
    s.name AS species,
    s.latin_name,
    s.class,
    s.conservation_status,
    a.gender,
    a.birth_date,
    TIMESTAMPDIFF(YEAR, a.birth_date, CURDATE()) AS age_years,
    a.health_status,
    a.arrival_date,
    e.name AS enclosure_name,
    e.type AS enclosure_type
FROM animals a
LEFT JOIN species s ON a.species_id = s.id
LEFT JOIN enclosures e ON a.enclosure_id = e.id
WHERE a.departure_date IS NULL; -- только текущие животные

-- 2. Расписание кормлений на сегодня
CREATE VIEW todays_feeding_schedule AS
SELECT 
    f.id,
    a.name AS animal_name,
    s.name AS species,
    f.feeding_time,
    f.food_type,
    f.quantity,
    CONCAT(e.first_name, ' ', e.last_name) AS employee_name,
    e.position,
    f.notes
FROM feedings f
JOIN animals a ON f.animal_id = a.id
JOIN species s ON a.species_id = s.id
JOIN employees e ON f.employee_id = e.id
WHERE f.feeding_date = CURDATE()
ORDER BY f.feeding_time;

-- 3. История вольеров для животных (перемещения)
CREATE VIEW animal_relocation_history AS
SELECT 
    a.name AS animal_name,
    s.name AS species,
    e1.name AS from_enclosure,
    e2.name AS to_enclosure,
    ae.start_date,
    ae.end_date,
    ae.reason
FROM animal_enclosures ae
JOIN animals a ON ae.animal_id = a.id
JOIN species s ON a.species_id = s.id
LEFT JOIN enclosures e1 ON ae.enclosure_id = e1.id
LEFT JOIN enclosures e2 ON a.enclosure_id = e2.id
ORDER BY ae.start_date DESC;

-- 4. Медицинские записи животных
CREATE VIEW medical_history AS
SELECT 
    a.name AS animal_name,
    s.name AS species,
    mr.record_date,
    mr.diagnosis,
    mr.treatment,
    mr.medication,
    mr.next_checkup,
    CONCAT(e.first_name, ' ', e.last_name) AS veterinarian,
    e.position
FROM medical_records mr
JOIN animals a ON mr.animal_id = a.id
JOIN species s ON a.species_id = s.id
JOIN employees e ON mr.vet_id = e.id
ORDER BY mr.record_date DESC;

-- 5. Статистика по вольерам
CREATE VIEW enclosure_statistics AS
SELECT 
    e.id,
    e.name AS enclosure_name,
    e.type,
    e.area,
    e.capacity,
    COUNT(a.id) AS current_animals,
    GROUP_CONCAT(s.name SEPARATOR ', ') AS species_list,
    CONCAT(emp.first_name, ' ', emp.last_name) AS responsible_employee,
    emp.position
FROM enclosures e
LEFT JOIN animals a ON e.id = a.enclosure_id AND a.departure_date IS NULL
LEFT JOIN species s ON a.species_id = s.id
LEFT JOIN employee_enclosures ee ON e.id = ee.enclosure_id 
    AND ee.assignment_date = (SELECT MAX(assignment_date) 
                             FROM employee_enclosures 
                             WHERE enclosure_id = e.id)
LEFT JOIN employees emp ON ee.employee_id = emp.id
GROUP BY e.id, e.name, e.type, e.area, e.capacity, emp.first_name, emp.last_name, emp.position;

-- 6. Животные, нуждающиеся в вакцинации (просроченные или скоро истекающие)
CREATE VIEW vaccination_due AS
SELECT 
    a.name AS animal_name,
    s.name AS species,
    v.vaccine_name,
    v.vaccination_date,
    v.expiration_date,
    CASE 
        WHEN v.expiration_date < CURDATE() THEN 'ПРОСРОЧЕНО'
        WHEN v.expiration_date <= DATE_ADD(CURDATE(), INTERVAL 30 DAY) THEN 'СКОРО ИСТЕКАЕТ'
        ELSE 'ДЕЙСТВУЕТ'
    END AS status,
    CONCAT(e.first_name, ' ', e.last_name) AS last_vaccinated_by
FROM vaccinations v
JOIN animals a ON v.animal_id = a.id
JOIN species s ON a.species_id = s.id
JOIN employees e ON v.administered_by = e.id
WHERE v.expiration_date IS NOT NULL
ORDER BY v.expiration_date ASC;

-- 7. Рацион питания по животным
CREATE VIEW animal_diet_schedule AS
SELECT 
    a.name AS animal_name,
    s.name AS species,
    d.food_description,
    d.feeding_frequency,
    d.daily_amount,
    f.feeding_time,
    f.feeding_date
FROM animals a
JOIN species s ON a.species_id = s.id
JOIN diets d ON s.id = d.species_id
LEFT JOIN feedings f ON a.id = f.animal_id 
    AND f.feeding_date = CURDATE()
ORDER BY a.name, f.feeding_time;

-- 8. Родственные связи животных
CREATE VIEW family_tree AS
SELECT 
    child.name AS child_name,
    child.birth_date AS child_birth_date,
    mother.name AS mother_name,
    father.name AS father_name,
    s.name AS species
FROM animals child
LEFT JOIN animals mother ON child.mother_id = mother.id
LEFT JOIN animals father ON child.father_id = father.id
JOIN species s ON child.species_id = s.id
WHERE child.mother_id IS NOT NULL OR child.father_id IS NOT NULL;

-- 9. Сотрудники и их обязанности
CREATE VIEW employee_responsibilities AS
SELECT 
    e.id,
    CONCAT(e.first_name, ' ', e.last_name) AS employee_name,
    e.position,
    e.hire_date,
    TIMESTAMPDIFF(YEAR, e.hire_date, CURDATE()) AS experience_years,
    GROUP_CONCAT(DISTINCT en.name SEPARATOR ', ') AS assigned_enclosures,
    COUNT(DISTINCT f.animal_id) AS animals_fed_last_week,
    COUNT(DISTINCT mr.animal_id) AS animals_medically_treated
FROM employees e
LEFT JOIN employee_enclosures ee ON e.id = ee.employee_id
LEFT JOIN enclosures en ON ee.enclosure_id = en.id
LEFT JOIN feedings f ON e.id = f.employee_id 
    AND f.feeding_date >= DATE_SUB(CURDATE(), INTERVAL 7 DAY)
LEFT JOIN medical_records mr ON e.id = mr.vet_id 
    AND mr.record_date >= DATE_SUB(CURDATE(), INTERVAL 30 DAY)
GROUP BY e.id, e.first_name, e.last_name, e.position, e.hire_date;

-- 10. Ежедневный отчет по здоровью животных
CREATE VIEW daily_health_report AS
SELECT 
    a.name AS animal_name,
    s.name AS species,
    a.health_status,
    MAX(mr.record_date) AS last_checkup,
    MAX(v.expiration_date) AS last_vaccination_expiry,
    CASE 
        WHEN a.health_status != 'healthy' THEN 'ТРЕБУЕТ ВНИМАНИЯ'
        WHEN MAX(mr.record_date) < DATE_SUB(CURDATE(), INTERVAL 6 MONTH) THEN 'НУЖЕН ПЛАНОВЫЙ ОСМОТР'
        ELSE 'НОРМА'
    END AS status_comment
FROM animals a
JOIN species s ON a.species_id = s.id
LEFT JOIN medical_records mr ON a.id = mr.animal_id
LEFT JOIN vaccinations v ON a.id = v.animal_id
WHERE a.departure_date IS NULL
GROUP BY a.id, a.name, s.name, a.health_status
ORDER BY 
    CASE 
        WHEN a.health_status != 'healthy' THEN 1
        WHEN MAX(mr.record_date) < DATE_SUB(CURDATE(), INTERVAL 6 MONTH) THEN 2
        ELSE 3
    END;