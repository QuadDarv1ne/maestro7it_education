-- Sakila Database Queries
-- DVD rental store database with films, customers, rentals, payments

-- 1. Basic table exploration
SELECT name AS table_name
FROM sqlite_master 
WHERE type = 'table';

-- 2. Get database schema
PRAGMA table_info(film);

-- 3. Simple data exploration
SELECT * FROM film LIMIT 5;
SELECT * FROM customer LIMIT 5;
SELECT * FROM rental LIMIT 5;

-- 4. Find films by category
SELECT 
    f.title,
    c.name AS category,
    f.release_year,
    f.rental_rate
FROM film f
JOIN film_category fc ON f.film_id = fc.film_id
JOIN category c ON fc.category_id = c.category_id
WHERE c.name = 'Action'
ORDER BY f.rental_rate DESC
LIMIT 10;

-- 5. Most popular films by rental count
SELECT 
    f.title,
    COUNT(r.rental_id) AS rental_count
FROM film f
JOIN inventory i ON f.film_id = i.film_id
JOIN rental r ON i.inventory_id = r.inventory_id
GROUP BY f.film_id
ORDER BY rental_count DESC
LIMIT 10;

-- 6. Customer rental history
SELECT 
    c.first_name,
    c.last_name,
    f.title,
    r.rental_date,
    r.return_date
FROM customer c
JOIN rental r ON c.customer_id = r.customer_id
JOIN inventory i ON r.inventory_id = i.inventory_id
JOIN film f ON i.film_id = f.film_id
WHERE c.customer_id = 1
ORDER BY r.rental_date DESC;

-- 7. Revenue by store
SELECT 
    s.store_id,
    a.address,
    ci.city,
    co.country,
    SUM(p.amount) AS total_revenue
FROM store s
JOIN address a ON s.address_id = a.address_id
JOIN city ci ON a.city_id = ci.city_id
JOIN country co ON ci.country_id = co.country_id
JOIN inventory i ON s.store_id = i.store_id
JOIN rental r ON i.inventory_id = r.inventory_id
JOIN payment p ON r.rental_id = p.rental_id
GROUP BY s.store_id
ORDER BY total_revenue DESC;

-- 8. Actor filmography
SELECT 
    a.first_name,
    a.last_name,
    f.title,
    f.release_year
FROM actor a
JOIN film_actor fa ON a.actor_id = fa.actor_id
JOIN film f ON fa.film_id = f.film_id
WHERE a.first_name = 'PENELOPE' AND a.last_name = 'GUINESS'
ORDER BY f.release_year;

-- 9. Overdue rentals
SELECT 
    c.first_name,
    c.last_name,
    f.title,
    r.rental_date,
    r.return_date,
    date('now') - date(r.rental_date) AS days_rented
FROM customer c
JOIN rental r ON c.customer_id = r.customer_id
JOIN inventory i ON r.inventory_id = i.inventory_id
JOIN film f ON i.film_id = f.film_id
WHERE r.return_date IS NULL
  AND date('now') > date(r.rental_date, '+' || f.rental_duration || ' days')
ORDER BY days_rented DESC;

-- 10. Monthly revenue report
SELECT 
    strftime('%Y-%m', p.payment_date) AS month,
    COUNT(p.payment_id) AS total_payments,
    SUM(p.amount) AS total_revenue,
    AVG(p.amount) AS avg_payment
FROM payment p
GROUP BY strftime('%Y-%m', p.payment_date)
ORDER BY month DESC
LIMIT 12;