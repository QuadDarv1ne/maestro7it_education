-- Добавление поля status в таблицу vacation
-- Выполните этот скрипт для обновления базы данных

-- Добавляем колонку status со значением по умолчанию 'approved'
ALTER TABLE vacation ADD COLUMN status VARCHAR(20) NOT NULL DEFAULT 'approved';

-- Добавляем колонку notes для заметок
ALTER TABLE vacation ADD COLUMN notes TEXT;

-- Добавляем колонки для отслеживания времени
ALTER TABLE vacation ADD COLUMN created_at DATETIME DEFAULT CURRENT_TIMESTAMP;
ALTER TABLE vacation ADD COLUMN updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP;

-- Создаем индекс для ускорения поиска по статусу
CREATE INDEX idx_vacation_status ON vacation(status);

-- Обновляем все существующие записи, устанавливая статус 'approved'
UPDATE vacation SET status = 'approved' WHERE status IS NULL;

-- Информация о завершении
SELECT 'Migration completed successfully!' AS message;
SELECT COUNT(*) AS total_vacations, status, COUNT(*) AS count 
FROM vacation 
GROUP BY status;
