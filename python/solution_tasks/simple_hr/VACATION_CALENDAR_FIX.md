# Исправление отображения отпусков в календаре

## Проблема
Отпуска не отображаются в календаре из-за отсутствия поля `status` в модели Vacation.

## Решение

### Вариант 1: Автоматическая миграция (рекомендуется)

Выполните CLI команду для автоматической миграции:

```bash
flask cli migrate-vacation-status
```

Эта команда:
- Добавит поле `status` в таблицу `vacation`
- Добавит поля `notes`, `created_at`, `updated_at`
- Создаст индекс для ускорения поиска
- Установит статус `approved` для всех существующих отпусков

### Вариант 2: Ручная миграция SQL

Если вы используете SQLite, выполните:

```sql
ALTER TABLE vacation ADD COLUMN status VARCHAR(20) NOT NULL DEFAULT 'approved';
ALTER TABLE vacation ADD COLUMN notes TEXT;
ALTER TABLE vacation ADD COLUMN created_at DATETIME DEFAULT CURRENT_TIMESTAMP;
ALTER TABLE vacation ADD COLUMN updated_at DATETIME DEFAULT CURRENT_TIMESTAMP;
```

Если вы используете MySQL, выполните скрипт из файла:
`migrations/add_vacation_status.sql`

### Вариант 3: Использование Flask-Migrate

```bash
flask db migrate -m "Add status field to vacation"
flask db upgrade
```

## Что изменилось

### Модель Vacation
Добавлены новые поля:
- `status` - статус отпуска (pending, approved, rejected)
- `notes` - заметки/причина отклонения
- `created_at` - дата создания записи
- `updated_at` - дата последнего обновления

Добавлены методы:
- `approve()` - одобрить отпуск
- `reject(notes)` - отклонить отпуск с указанием причины
- `is_approved()` - проверка статуса
- `duration_days()` - расчет продолжительности

### Отображение календаря
- Теперь в календаре показываются только **одобренные** отпуска (status='approved')
- Использует `db.joinedload()` для оптимизации загрузки связанных сотрудников
- Улучшено логирование для отладки

### Управление отпусками
В списке отпусков добавлены:
- Колонка "Статус" с цветовыми индикаторами
- Кнопки для одобрения/отклонения отпусков со статусом "pending"
- Модальное окно для указания причины отклонения

### Новые маршруты
- `/vacations/<id>/approve` - одобрить отпуск
- `/vacations/<id>/reject` - отклонить отпуск
- `/vacations/debug/calendar-data` - отладка данных календаря

## Проверка работы

1. После выполнения миграции перезапустите приложение
2. Откройте `/vacations/debug/calendar-data` для проверки данных
3. Откройте календарь `/vacations/calendar`
4. Убедитесь, что отпуска отображаются

## Создание тестового отпуска

```python
from app.models import Vacation, Employee
from app import db
from datetime import date, timedelta

# Получаем любого сотрудника
employee = Employee.query.first()

# Создаем тестовый отпуск
vacation = Vacation(
    employee_id=employee.id,
    start_date=date.today(),
    end_date=date.today() + timedelta(days=14),
    type='paid',
    status='approved'
)

db.session.add(vacation)
db.session.commit()

print(f"Создан тестовый отпуск ID: {vacation.id}")
```

## Устранение проблем

### Ошибка "column status does not exist"
Выполните миграцию базы данных (см. Вариант 1)

### Отпуска все еще не отображаются
1. Проверьте статус отпусков: `SELECT * FROM vacation;`
2. Убедитесь, что `status = 'approved'`
3. Проверьте даты: отпуска должны попадать в выбранный месяц
4. Откройте `/vacations/debug/calendar-data` для детальной информации

### Ошибка при загрузке employee
Убедитесь, что у всех отпусков есть связанный сотрудник:
```sql
SELECT v.*, e.full_name 
FROM vacation v 
LEFT JOIN employee e ON v.employee_id = e.id 
WHERE e.id IS NULL;
```
