-- Тестовые данные для проверки SQL-запросов
-- Используются для тестирования и обучения

-- Таблица: тестовые клиенты
CREATE TABLE IF NOT EXISTS test_customers (
    customer_id INTEGER PRIMARY KEY,
    first_name TEXT NOT NULL,
    last_name TEXT NOT NULL,
    email TEXT UNIQUE,
    phone TEXT,
    city TEXT,
    country TEXT,
    registration_date DATE
);

-- Таблица: тестовые продукты
CREATE TABLE IF NOT EXISTS test_products (
    product_id INTEGER PRIMARY KEY,
    product_name TEXT NOT NULL,
    category TEXT,
    price DECIMAL(10,2),
    stock_quantity INTEGER,
    supplier_id INTEGER
);

-- Таблица: тестовые заказы
CREATE TABLE IF NOT EXISTS test_orders (
    order_id INTEGER PRIMARY KEY,
    customer_id INTEGER,
    order_date DATE,
    total_amount DECIMAL(10,2),
    status TEXT
);

-- Таблица: тестовые поставщики
CREATE TABLE IF NOT EXISTS test_suppliers (
    supplier_id INTEGER PRIMARY KEY,
    supplier_name TEXT NOT NULL,
    contact_person TEXT,
    phone TEXT,
    email TEXT,
    country TEXT
);

-- Вставка тестовых данных

-- Тестовые клиенты
INSERT INTO test_customers (customer_id, first_name, last_name, email, phone, city, country, registration_date) VALUES
(1, 'Иван', 'Иванов', 'ivan.ivanov@email.com', '+7(999)123-45-67', 'Москва', 'Россия', '2023-01-15'),
(2, 'Мария', 'Петрова', 'maria.petrova@email.com', '+7(999)234-56-78', 'Санкт-Петербург', 'Россия', '2023-02-20'),
(3, 'Алексей', 'Сидоров', 'alex.sidorov@email.com', '+7(999)345-67-89', 'Новосибирск', 'Россия', '2023-03-10'),
(4, 'Елена', 'Козлова', 'elena.kozlova@email.com', '+7(999)456-78-90', 'Екатеринбург', 'Россия', '2023-04-05'),
(5, 'Дмитрий', 'Морозов', 'dmitry.morozov@email.com', '+7(999)567-89-01', 'Казань', 'Россия', '2023-05-12'),
(6, 'Анна', 'Волкова', 'anna.volkova@email.com', '+7(999)678-90-12', 'Нижний Новгород', 'Россия', '2023-06-18'),
(7, 'Сергей', 'Лебедев', 'sergey.lebedev@email.com', '+7(999)789-01-23', 'Челябинск', 'Россия', '2023-07-22'),
(8, 'Ольга', 'Новикова', 'olga.novikova@email.com', '+7(999)890-12-34', 'Самара', 'Россия', '2023-08-30'),
(9, 'Павел', 'Кузнецов', 'pavel.kuznetsov@email.com', '+7(999)901-23-45', 'Омск', 'Россия', '2023-09-15'),
(10, 'Татьяна', 'Попова', 'tatiana.popova@email.com', '+7(999)012-34-56', 'Ростов-на-Дону', 'Россия', '2023-10-08');

-- Тестовые поставщики
INSERT INTO test_suppliers (supplier_id, supplier_name, contact_person, phone, email, country) VALUES
(1, 'ТехноПоставка', 'Андрей Смирнов', '+7(495)111-11-11', 'smirnov@techno.ru', 'Россия'),
(2, 'ГлобалСнаб', 'Екатерина Волкова', '+7(495)222-22-22', 'volkova@globalsnab.ru', 'Россия'),
(3, 'ЭлектроМир', 'Михаил Петров', '+7(495)333-33-33', 'petrov@electromir.ru', 'Россия'),
(4, 'Оптовый Дом', 'Наталья Соколова', '+7(495)444-44-44', 'sokolova@optdom.ru', 'Россия'),
(5, 'ИмпортТорг', 'Владимир Козлов', '+7(495)555-55-55', 'kozlov@import.ru', 'Россия');

-- Тестовые продукты
INSERT INTO test_products (product_id, product_name, category, price, stock_quantity, supplier_id) VALUES
(1, 'Смартфон Samsung Galaxy S23', 'Электроника', 65000.00, 25, 1),
(2, 'Ноутбук Lenovo ThinkPad X1', 'Электроника', 120000.00, 15, 1),
(3, 'Планшет Apple iPad Pro', 'Электроника', 85000.00, 12, 2),
(4, 'Наушники Sony WH-1000XM5', 'Электроника', 25000.00, 40, 2),
(5, 'Чайник электрический Bosch', 'Бытовая техника', 3500.00, 50, 3),
(6, 'Пылесос Dyson V15', 'Бытовая техника', 45000.00, 8, 3),
(7, 'Кофемашина DeLonghi', 'Бытовая техника', 32000.00, 20, 4),
(8, 'Микроволновая печь Samsung', 'Бытовая техника', 12000.00, 30, 4),
(9, 'Флеш-карта Kingston 128GB', 'Компьютерные аксессуары', 1500.00, 100, 5),
(10, 'Внешний жесткий диск Seagate 2TB', 'Компьютерные аксессуары', 8000.00, 35, 5),
(11, 'Клавиатура Logitech K380', 'Компьютерные аксессуары', 3000.00, 45, 1),
(12, 'Мышь SteelSeries Rival 310', 'Компьютерные аксессуары', 4500.00, 28, 2);

-- Тестовые заказы
INSERT INTO test_orders (order_id, customer_id, order_date, total_amount, status) VALUES
(1, 1, '2023-10-15', 68500.00, 'Доставлен'),
(2, 2, '2023-10-16', 120000.00, 'Доставлен'),
(3, 3, '2023-10-17', 25000.00, 'В обработке'),
(4, 1, '2023-10-18', 3500.00, 'Доставлен'),
(5, 4, '2023-10-19', 45000.00, 'Отменен'),
(6, 5, '2023-10-20', 32000.00, 'Доставлен'),
(7, 2, '2023-10-21', 12000.00, 'Доставлен'),
(8, 6, '2023-10-22', 8000.00, 'В обработке'),
(9, 7, '2023-10-23', 1500.00, 'Доставлен'),
(10, 8, '2023-10-24', 4500.00, 'Доставлен'),
(11, 3, '2023-10-25', 85000.00, 'В обработке'),
(12, 9, '2023-10-26', 65000.00, 'Доставлен'),
(13, 10, '2023-10-27', 3000.00, 'Доставлен'),
(14, 1, '2023-10-28', 25000.00, 'В обработке'),
(15, 5, '2023-10-29', 12000.00, 'Доставлен');

-- Тестовые запросы для проверки

-- Базовый SELECT
SELECT * FROM test_customers LIMIT 5;

-- Фильтрация
SELECT first_name, last_name, city 
FROM test_customers 
WHERE country = 'Россия' 
ORDER BY last_name;

-- JOIN запросы
SELECT 
    c.first_name,
    c.last_name,
    o.order_date,
    o.total_amount,
    o.status
FROM test_customers c
JOIN test_orders o ON c.customer_id = o.customer_id
WHERE o.status = 'Доставлен'
ORDER BY o.order_date DESC;

-- Агрегация
SELECT 
    category,
    COUNT(*) as product_count,
    AVG(price) as avg_price,
    SUM(stock_quantity) as total_stock
FROM test_products
GROUP BY category
ORDER BY product_count DESC;

-- Сложная агрегация с JOIN
SELECT 
    s.supplier_name,
    COUNT(p.product_id) as product_count,
    AVG(p.price) as avg_price,
    SUM(o.total_amount) as total_sales
FROM test_suppliers s
JOIN test_products p ON s.supplier_id = p.supplier_id
LEFT JOIN test_orders o ON EXISTS (
    SELECT 1 FROM test_customers c 
    WHERE c.customer_id = o.customer_id
)
GROUP BY s.supplier_id
ORDER BY total_sales DESC;

-- Подзапросы
SELECT 
    first_name,
    last_name,
    city
FROM test_customers
WHERE customer_id IN (
    SELECT DISTINCT customer_id 
    FROM test_orders 
    WHERE total_amount > 50000
);

-- Оконные функции
SELECT 
    product_name,
    category,
    price,
    ROW_NUMBER() OVER (PARTITION BY category ORDER BY price DESC) as price_rank,
    AVG(price) OVER (PARTITION BY category) as avg_category_price
FROM test_products
ORDER BY category, price_rank;

-- Дата и время
SELECT 
    strftime('%Y-%m', order_date) as month,
    COUNT(*) as order_count,
    SUM(total_amount) as total_revenue
FROM test_orders
WHERE order_date >= date('now', '-3 months')
GROUP BY strftime('%Y-%m', order_date)
ORDER BY month DESC;