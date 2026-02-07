-- Создание базы данных
CREATE DATABASE animals_db;
USE animals_db;

-- Таблица видов животных
CREATE TABLE species (
    id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(100) NOT NULL,
    latin_name VARCHAR(150),
    class VARCHAR(50) NOT NULL, -- млекопитающие, птицы, рыбы и т.д.
    conservation_status VARCHAR(50), -- охранный статус
    description TEXT
);

-- Таблица животных
CREATE TABLE animals (
    id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(100),
    species_id INT NOT NULL,
    birth_date DATE,
    gender ENUM('male', 'female', 'unknown'),
    health_status VARCHAR(100) DEFAULT 'healthy',
    arrival_date DATE NOT NULL,
    departure_date DATE,
    mother_id INT,
    father_id INT,
    enclosure_id INT,
    FOREIGN KEY (species_id) REFERENCES species(id),
    FOREIGN KEY (mother_id) REFERENCES animals(id),
    FOREIGN KEY (father_id) REFERENCES animals(id)
);

-- Таблица вольеров/территорий
CREATE TABLE enclosures (
    id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(100) NOT NULL,
    type VARCHAR(50), -- открытый, закрытый, аквариум, вольер
    area DECIMAL(10,2), -- площадь в кв. метрах
    capacity INT,
    temperature_range VARCHAR(50),
    humidity_range VARCHAR(50)
);

-- Таблица сотрудников
CREATE TABLE employees (
    id INT PRIMARY KEY AUTO_INCREMENT,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    position VARCHAR(100) NOT NULL,
    phone VARCHAR(20),
    email VARCHAR(100),
    hire_date DATE NOT NULL
);

-- Таблица кормлений
CREATE TABLE feedings (
    id INT PRIMARY KEY AUTO_INCREMENT,
    animal_id INT NOT NULL,
    employee_id INT NOT NULL,
    food_type VARCHAR(200) NOT NULL,
    quantity VARCHAR(50),
    feeding_time TIME NOT NULL,
    feeding_date DATE NOT NULL,
    notes TEXT,
    FOREIGN KEY (animal_id) REFERENCES animals(id),
    FOREIGN KEY (employee_id) REFERENCES employees(id)
);

-- Таблица медицинских записей
CREATE TABLE medical_records (
    id INT PRIMARY KEY AUTO_INCREMENT,
    animal_id INT NOT NULL,
    vet_id INT NOT NULL,
    record_date DATE NOT NULL,
    diagnosis TEXT,
    treatment TEXT,
    medication VARCHAR(200),
    next_checkup DATE,
    FOREIGN KEY (animal_id) REFERENCES animals(id),
    FOREIGN KEY (vet_id) REFERENCES employees(id)
);

-- Таблица вакцинаций
CREATE TABLE vaccinations (
    id INT PRIMARY KEY AUTO_INCREMENT,
    animal_id INT NOT NULL,
    vaccine_name VARCHAR(150) NOT NULL,
    vaccination_date DATE NOT NULL,
    expiration_date DATE,
    administered_by INT NOT NULL,
    FOREIGN KEY (animal_id) REFERENCES animals(id),
    FOREIGN KEY (administered_by) REFERENCES employees(id)
);

-- Таблица рационов питания по видам
CREATE TABLE diets (
    id INT PRIMARY KEY AUTO_INCREMENT,
    species_id INT NOT NULL,
    food_description TEXT NOT NULL,
    feeding_frequency VARCHAR(100),
    daily_amount VARCHAR(100),
    FOREIGN KEY (species_id) REFERENCES species(id)
);

-- Связь животных и вольеров (история перемещений)
CREATE TABLE animal_enclosures (
    id INT PRIMARY KEY AUTO_INCREMENT,
    animal_id INT NOT NULL,
    enclosure_id INT NOT NULL,
    start_date DATE NOT NULL,
    end_date DATE,
    reason VARCHAR(200),
    FOREIGN KEY (animal_id) REFERENCES animals(id),
    FOREIGN KEY (enclosure_id) REFERENCES enclosures(id)
);

-- Связь сотрудников и вольеров (за кем закреплен)
CREATE TABLE employee_enclosures (
    id INT PRIMARY KEY AUTO_INCREMENT,
    employee_id INT NOT NULL,
    enclosure_id INT NOT NULL,
    assignment_date DATE NOT NULL,
    FOREIGN KEY (employee_id) REFERENCES employees(id),
    FOREIGN KEY (enclosure_id) REFERENCES enclosures(id)
);

-- Индексы для улучшения производительности
CREATE INDEX idx_animals_species ON animals(species_id);
CREATE INDEX idx_animals_enclosure ON animals(enclosure_id);
CREATE INDEX idx_feedings_animal ON feedings(animal_id);
CREATE INDEX idx_medical_animal ON medical_records(animal_id);
CREATE INDEX idx_vaccinations_animal ON vaccinations(animal_id);