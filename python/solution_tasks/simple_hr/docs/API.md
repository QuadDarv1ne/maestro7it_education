# API Документация Simple HR

## Обзор

Simple HR предоставляет веб-интерфейс для управления персоналом. Все endpoints требуют аутентификации через Flask-Login.

## Базовый URL

```
http://localhost:5000
```

## Аутентификация

### POST /login
Вход в систему

**Rate Limit:** 5 запросов в минуту

**Параметры формы:**
- `username` (string, обязательный) - Имя пользователя
- `password` (string, обязательный) - Пароль

**Ответ:**
- Перенаправление на главную страницу при успехе
- Сообщение об ошибке при неудаче

---

### GET /logout
Выход из системы

**Требует:** Аутентификация

**Ответ:** Перенаправление на страницу входа

---

### POST /register
Регистрация нового пользователя

**Rate Limit:** 3 запроса в час

**Параметры формы:**
- `username` (string, 3-80 символов)
- `email` (string, валидный email)
- `password` (string, минимум 6 символов)
- `password2` (string, должен совпадать с password)
- `role` (string, 'hr' или 'admin')

---

## Сотрудники

### GET /employees/
Список всех сотрудников

**Требует:** Аутентификация

**Query параметры:**
- `search` (string, опционально) - Поиск по имени или email
- `department` (int, опционально) - Фильтр по ID отдела
- `status` (string, опционально) - Фильтр по статусу (active/dismissed)

**Ответ:** HTML страница со списком сотрудников

---

### GET /employees/create
Форма создания сотрудника

**Требует:** Аутентификация

---

### POST /employees/create
Создание нового сотрудника

**Требует:** Аутентификация

**Параметры формы:**
- `full_name` (string, обязательный)
- `email` (string, обязательный, уникальный)
- `employee_id` (string, обязательный, уникальный)
- `hire_date` (date, обязательный)
- `department_id` (int, обязательный)
- `position_id` (int, обязательный)

---

### GET /employees/edit/<id>
Форма редактирования сотрудника

**Требует:** Аутентификация

**Параметры URL:**
- `id` (int) - ID сотрудника

---

### POST /employees/edit/<id>
Обновление данных сотрудника

**Требует:** Аутентификация

---

### POST /employees/delete/<id>
Удаление сотрудника

**Требует:** Аутентификация

---

### GET /employees/import
Форма импорта сотрудников из CSV

**Требует:** Аутентификация

---

### POST /employees/import
Импорт сотрудников из CSV файла

**Требует:** Аутентификация

**Параметры:**
- `file` (file, CSV формат)

**Формат CSV:**
```
full_name,email,employee_id,hire_date,department_name,position_title
Иванов Иван,ivanov@example.com,EMP001,2024-01-15,IT,Разработчик
```

---

## Отделы

### GET /departments/
Список всех отделов

**Требует:** Аутентификация

---

### GET /departments/create
Форма создания отдела

---

### POST /departments/create
Создание нового отдела

**Параметры формы:**
- `name` (string, обязательный, уникальный)

---

### GET /departments/edit/<id>
Форма редактирования отдела

---

### POST /departments/edit/<id>
Обновление данных отдела

---

### POST /departments/delete/<id>
Удаление отдела

**Примечание:** Нельзя удалить отдел с сотрудниками

---

## Должности

### GET /positions/
Список всех должностей

---

### GET /positions/create
Форма создания должности

---

### POST /positions/create
Создание новой должности

**Параметры формы:**
- `title` (string, обязательный, уникальный)

---

### GET /positions/edit/<id>
Форма редактирования должности

---

### POST /positions/edit/<id>
Обновление данных должности

---

### POST /positions/delete/<id>
Удаление должности

**Примечание:** Нельзя удалить должность с сотрудниками

---

## Приказы

### GET /orders/
Список всех приказов

---

### GET /orders/create
Форма создания приказа

---

### POST /orders/create
Создание нового приказа

**Параметры формы:**
- `employee_id` (int, обязательный)
- `type` (string, 'hire'/'transfer'/'dismissal')
- `date_issued` (date, обязательный)
- `new_department_id` (int, для transfer)
- `new_position_id` (int, для transfer)

---

### GET /orders/edit/<id>
Форма редактирования приказа

---

### POST /orders/edit/<id>
Обновление данных приказа

---

### POST /orders/delete/<id>
Удаление приказа

---

## Отпуска

### GET /vacations/
Список всех отпусков

---

### GET /vacations/calendar
Календарный вид отпусков

**Query параметры:**
- `year` (int, опционально)
- `month` (int, опционально)

---

### GET /vacations/create
Форма создания отпуска

---

### POST /vacations/create
Создание нового отпуска

**Параметры формы:**
- `employee_id` (int, обязательный)
- `start_date` (date, обязательный)
- `end_date` (date, обязательный)
- `type` (string, 'paid'/'unpaid'/'sick')

**Валидация:**
- end_date должна быть больше start_date
- Проверка на пересечение с существующими отпусками

---

### GET /vacations/edit/<id>
Форма редактирования отпуска

---

### POST /vacations/edit/<id>
Обновление данных отпуска

---

### POST /vacations/delete/<id>
Удаление отпуска

---

## Отчёты

### GET /reports/
Главная страница отчётов

---

### GET /reports/employees
Отчёт по сотрудникам

**Query параметры:**
- `department_id` (int, опционально)
- `status` (string, опционально)
- `format` (string, 'html'/'csv')

---

### GET /reports/departments
Отчёт по отделам

---

### GET /reports/hiring
Отчёт по найму сотрудников

**Query параметры:**
- `start_date` (date, опционально)
- `end_date` (date, опционально)

---

### GET /reports/statistics
Общая статистика

---

## Аналитика

### GET /analytics/dashboard
Дашборд с графиками и аналитикой

**Требует:** Аутентификация

---

### GET /analytics/employee-statistics
Статистика по сотрудникам

---

### GET /analytics/hiring-trends
Тренды найма

---

### GET /analytics/vacation-analysis
Анализ отпусков

---

## Уведомления

### GET /notifications/
Список уведомлений пользователя

**Требует:** Аутентификация

---

### POST /notifications/mark-read/<id>
Пометить уведомление как прочитанное

---

## Административные функции

### GET /admin/
Панель администратора

**Требует:** Роль admin

---

### GET /admin/users
Список пользователей

**Требует:** Роль admin

---

### GET /admin/users/create
Создание пользователя

**Требует:** Роль admin

---

### POST /admin/users/create
Сохранение нового пользователя

---

### GET /admin/users/edit/<id>
Редактирование пользователя

---

### POST /admin/users/edit/<id>
Обновление пользователя

---

### POST /admin/users/delete/<id>
Удаление пользователя

---

### GET /admin/backup
Управление резервными копиями

**Требует:** Роль admin

---

### POST /admin/backup/create
Создание резервной копии БД

---

## Журнал аудита

### GET /audit/
Просмотр журнала аудита

**Требует:** Аутентификация

**Query параметры:**
- `user_id` (int, опционально)
- `action` (string, опционально)
- `start_date` (date, опционально)
- `end_date` (date, опционально)

---

## Коды ответов

- **200** - Успешный запрос
- **400** - Неверный запрос
- **403** - Доступ запрещён
- **404** - Ресурс не найден
- **429** - Превышен лимит запросов
- **500** - Внутренняя ошибка сервера

---

## Rate Limiting

Для защиты от брутфорса применяются следующие лимиты:

- `/login` - 5 запросов в минуту
- `/register` - 3 запроса в час
- Остальные endpoints - 200 запросов в день, 50 в час

---

## Безопасность

### Заголовки безопасности

Все ответы включают следующие заголовки:
- `X-Content-Type-Options: nosniff`
- `X-Frame-Options: SAMEORIGIN`
- `X-XSS-Protection: 1; mode=block`
- `Strict-Transport-Security: max-age=31536000`
- `Content-Security-Policy`

### CSRF Protection

Все формы защищены от CSRF атак через Flask-WTF.

### Password Security

- Минимальная длина: 6 символов
- Требуется минимум одна буква и одна цифра
- Хеширование через Werkzeug (PBKDF2)

---

## Примеры использования

### Создание сотрудника через curl

```bash
curl -X POST http://localhost:5000/employees/create \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "full_name=Иван Иванов" \
  -d "email=ivan@example.com" \
  -d "employee_id=EMP123" \
  -d "hire_date=2024-01-15" \
  -d "department_id=1" \
  -d "position_id=1" \
  --cookie "session=YOUR_SESSION_COOKIE"
```

### Экспорт отчёта в CSV

```bash
curl http://localhost:5000/reports/employees?format=csv \
  --cookie "session=YOUR_SESSION_COOKIE" \
  -o employees_report.csv
```

---

## Поддержка

Для вопросов и предложений создавайте issue в GitHub репозитории.
