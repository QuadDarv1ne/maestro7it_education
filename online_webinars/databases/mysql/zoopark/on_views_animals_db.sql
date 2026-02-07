-- Получить полную информацию о всех животных
SELECT * FROM animals_full_info;

-- Посмотреть расписание кормлений на сегодня
SELECT * FROM todays_feeding_schedule;

-- Найти животных, которым нужна вакцинация
SELECT * FROM vaccination_due WHERE status != 'ДЕЙСТВУЕТ';

-- Получить медицинскую историю конкретного животного
SELECT * FROM medical_history WHERE animal_name = 'Амур';

-- Проверить статистику по вольерам
SELECT * FROM enclosure_statistics WHERE current_animals > capacity;

-- Посмотреть родственные связи
SELECT * FROM family_tree WHERE species = 'Амурский тигр';

-- Ежедневный отчет о здоровье
SELECT * FROM daily_health_report WHERE status_comment != 'НОРМА';