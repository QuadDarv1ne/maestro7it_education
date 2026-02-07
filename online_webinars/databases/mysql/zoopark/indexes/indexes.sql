-- Дополнительные индексы для оптимизации производительности

USE animals_db;

-- Индексы для таблицы animals
CREATE INDEX idx_animals_birth_date ON animals(birth_date);
CREATE INDEX idx_animals_gender ON animals(gender);
CREATE INDEX idx_animals_health_status ON animals(health_status);
CREATE INDEX idx_animals_arrival_date ON animals(arrival_date);

-- Индексы для таблицы feedings
CREATE INDEX idx_feedings_date_time ON feedings(feeding_date, feeding_time);
CREATE INDEX idx_feedings_food_type ON feedings(food_type);

-- Индексы для таблицы medical_records
CREATE INDEX idx_medical_records_date ON medical_records(record_date);
CREATE INDEX idx_medical_records_diagnosis ON medical_records(diagnosis);

-- Индексы для таблицы vaccinations
CREATE INDEX idx_vaccinations_dates ON vaccinations(vaccination_date, expiration_date);

-- Индексы для таблицы animal_enclosures
CREATE INDEX idx_animal_enclosures_dates ON animal_enclosures(start_date, end_date);

-- Индексы для таблицы employees
CREATE INDEX idx_employees_position ON employees(position);
CREATE INDEX idx_employees_hire_date ON employees(hire_date);

-- Индексы для таблицы species
CREATE INDEX idx_species_class ON species(class);
CREATE INDEX idx_species_conservation_status ON species(conservation_status);

-- Композитные индексы для часто используемых JOIN'ов
CREATE INDEX idx_feedings_animal_date ON feedings(animal_id, feeding_date);
CREATE INDEX idx_medical_records_animal_date ON medical_records(animal_id, record_date);
CREATE INDEX idx_vaccinations_animal_date ON vaccinations(animal_id, vaccination_date);