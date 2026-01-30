**CalDAV** — сетевой протокол прикладного уровня, расширяющий возможности WebDAV и предназначенный для доступа, синхронизации и управления календарными данными.

## Оглавление
- [Введение](#введение)
- [Основные концепции](#основные-концепции)
- [Архитектура](#архитектура)
- [Установка и настройка](#установка-и-настройка)
- [Основные операции](#основные-операции)
- [Практические примеры](#практические-примеры)
- [Лучшие практики](#лучшие-практики)
- [Сравнение с аналогами](#сравнение-с-аналогами)
- [Полезные ресурсы](#полезные-ресурсы)

## Введение

`CalDAV (Calendar Extensions to WebDAV)` — это стандарт IETF (RFC 4791), который позволяет клиентам получать доступ к календарным данным на удаленных серверах через HTTP/HTTPS.

Протокол поддерживает создание, изменение, удаление и синхронизацию событий, задач и другой календарной информации.

### Основные преимущества:

- **Стандартизация** — открытый стандарт IETF
- **Синхронизация** — двухсторонняя синхронизация между клиентами
- **Масштабируемость** — работает через HTTP/HTTPS
- **Интеграция** — поддерживается большинством календарных приложений

## Основные концепции

### Компоненты CalDAV

1. **Календарь (Calendar)**
   - Коллекция календарных объектов
   - Может содержать события, задачи, свободное/занятое время
   - Имеет уникальный URL и свойства (имя, описание, цвет)

2. **Календарный объект (Calendar Object)**
   - Единица данных в формате iCalendar (RFC 5545)
   - Может быть событием (VEVENT), задачей (VTODO), заметкой (VJOURNAL)

3. **Свойства (Properties)**
   - Метаданные календаря или объекта
   - Примеры: имя, описание, временная зона, права доступа

4. **Отчеты (Reports)**
   - Расширенные запросы к серверу
   - Поиск событий по дате, участникам, категориям

## Архитектура

### Стек протоколов

```
Приложение (клиент)
       ↓
CalDAV (уровень приложения)
       ↓
WebDAV (расширения HTTP)
       ↓
HTTP/HTTPS (транспорт)
       ↓
TCP/IP (сетевой стек)
```

### Типичная архитектура системы

```
┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│  Клиент 1   │    │  Клиент 2   │    │  Клиент N   │
│ (Outlook)   │    │ (Thunderbird)│    │ (iOS Cal)   │
└──────┬──────┘    └──────┬──────┘    └──────┬──────┘
       │                  │                  │
       └──────────────────┼──────────────────┘
                          │
                ┌─────────▼─────────┐
                │   CalDAV Сервер   │
                │  (Radicale, Baïkal│
                │   или другие)     │
                └─────────┬─────────┘
                          │
                ┌─────────▼─────────┐
                │   Хранилище       │
                │ (файлы, БД)       │
                └───────────────────┘
```

## Установка и настройка

### Сервер Radicale (Python)

#### Установка
```bash
pip install radicale
```

#### Конфигурация (config file)
```ini
[server]
hosts = 0.0.0.0:5232

[auth]
type = htpasswd
htpasswd_filename = /etc/radicale/users
htpasswd_encryption = bcrypt

[storage]
type = multifilesystem
directory = /var/lib/radicale/collections
```

#### Запуск
```bash
radicale --config /etc/radicale/config
```

### Сервер Baïkal (PHP)

#### Требования
- PHP 7.4+
- SQLite или MySQL
- Веб-сервер (Apache/Nginx)

#### Установка
1. Скачать последнюю версию с [baikal-server.com](https://sabre.io/baikal/)
2. Распаковать в веб-директорию
3. Настроить веб-сервер
4. Пройти установку через браузер

#### Пример конфигурации Nginx
```nginx
server {
    listen 80;
    server_name cal.example.com;
    
    root /var/www/baikal/html;
    index index.php;
    
    location ~ \.(php|inc)$ {
        fastcgi_pass unix:/var/run/php/php8.1-fpm.sock;
        fastcgi_index index.php;
        include fastcgi_params;
        fastcgi_param SCRIPT_FILENAME $document_root$fastcgi_script_name;
    }
}
```

## Основные операции

### HTTP методы CalDAV

| Метод | Назначение |
|-------|------------|
| PROPFIND | Получение свойств ресурсов |
| PROPPATCH | Изменение свойств ресурсов |
| MKCALENDAR | Создание нового календаря |
| REPORT | Расширенные запросы и отчеты |
| PUT | Создание/обновление календарного объекта |
| DELETE | Удаление ресурса |

### Примеры запросов

#### 1. Создание календаря
```http
MKCALENDAR /calendars/user/main/ HTTP/1.1
Host: cal.example.com
Authorization: Basic dXNlcjpwYXNz
Content-Type: application/xml; charset=utf-8

<?xml version="1.0" encoding="utf-8" ?>
<C:mkcalendar xmlns:D="DAV:" xmlns:C="urn:ietf:params:xml:ns:caldav">
  <D:set>
    <D:prop>
      <D:displayname>Основной календарь</D:displayname>
      <C:calendar-description xml:lang="ru">Мой рабочий календарь</C:calendar-description>
      <C:supported-calendar-component-set>
        <C:comp name="VEVENT"/>
        <C:comp name="VTODO"/>
      </C:supported-calendar-component-set>
    </D:prop>
  </D:set>
</C:mkcalendar>
```

#### 2. Создание события
```http
PUT /calendars/user/main/event1.ics HTTP/1.1
Host: cal.example.com
Authorization: Basic dXNlcjpwYXNz
Content-Type: text/calendar; charset=utf-8
If-None-Match: *

BEGIN:VCALENDAR
VERSION:2.0
PRODID:-//Example Corp.//CalDAV Client//EN
BEGIN:VEVENT
UID:event1@example.com
DTSTAMP:20240115T100000Z
DTSTART:20240120T100000Z
DTEND:20240120T110000Z
SUMMARY:Встреча команды
DESCRIPTION:Еженедельная встреча разработчиков
LOCATION:Конференц-зал A
END:VEVENT
END:VCALENDAR
```

#### 3. Поиск событий за период
```http
REPORT /calendars/user/main/ HTTP/1.1
Host: cal.example.com
Authorization: Basic dXNlcjpwYXNz
Content-Type: application/xml; charset=utf-8
Depth: 1

<?xml version="1.0" encoding="utf-8" ?>
<C:calendar-query xmlns:D="DAV:" xmlns:C="urn:ietf:params:xml:ns:caldav">
  <D:prop>
    <D:getetag/>
    <C:calendar-data/>
  </D:prop>
  <C:filter>
    <C:comp-filter name="VCALENDAR">
      <C:comp-filter name="VEVENT">
        <C:time-range start="20240101T000000Z" end="20240201T000000Z"/>
      </C:comp-filter>
    </C:comp-filter>
  </C:filter>
</C:calendar-query>
```

## Практические примеры

### Python клиент с помощью requests

```python
import requests
from requests.auth import HTTPBasicAuth

# Конфигурация
CALDAV_URL = "https://cal.example.com/calendars/user/main/"
USERNAME = "user"
PASSWORD = "pass"

# Аутентификация
auth = HTTPBasicAuth(USERNAME, PASSWORD)

# Создание события
ical_data = """BEGIN:VCALENDAR
VERSION:2.0
PRODID:-//MyApp//CalDAV Client//EN
BEGIN:VEVENT
UID:event2@example.com
DTSTAMP:20240115T110000Z
DTSTART:20240125T140000Z
DTEND:20240125T150000Z
SUMMARY:Code Review
DESCRIPTION:Проверка кода новой фичи
END:VEVENT
END:VCALENDAR"""

response = requests.put(
    f"{CALDAV_URL}event2.ics",
    data=ical_data,
    auth=auth,
    headers={
        "Content-Type": "text/calendar; charset=utf-8",
        "If-None-Match": "*"
    }
)

print(f"Status: {response.status_code}")
```

### JavaScript/Node.js клиент

```javascript
const axios = require('axios');

async function createEvent() {
    const config = {
        baseURL: 'https://cal.example.com',
        auth: {
            username: 'user',
            password: 'pass'
        },
        headers: {
            'Content-Type': 'text/calendar; charset=utf-8'
        }
    };
    
    const icalData = `BEGIN:VCALENDAR
VERSION:2.0
PRODID:-//MyApp//CalDAV Client//EN
BEGIN:VEVENT
UID:event3@example.com
DTSTAMP:20240115T120000Z
DTSTART:20240130T090000Z
DTEND:20240130T100000Z
SUMMARY:Планирование спринта
END:VEVENT
END:VCALENDAR`;
    
    try {
        const response = await axios.put(
            '/calendars/user/main/event3.ics',
            icalData,
            config
        );
        console.log('Event created:', response.status);
    } catch (error) {
        console.error('Error:', error.response?.status, error.message);
    }
}
```

### PHP клиент

```php
<?php
$url = 'https://cal.example.com/calendars/user/main/event4.ics';
$username = 'user';
$password = 'pass';

$icalData = "BEGIN:VCALENDAR\n" .
           "VERSION:2.0\n" .
           "PRODID:-//MyApp//CalDAV Client//EN\n" .
           "BEGIN:VEVENT\n" .
           "UID:event4@example.com\n" .
           "DTSTAMP:20240115T130000Z\n" .
           "DTSTART:20240201T110000Z\n" .
           "DTEND:20240201T120000Z\n" .
           "SUMMARY:Обзор задач\n" .
           "END:VEVENT\n" .
           "END:VCALENDAR";

$ch = curl_init();
curl_setopt($ch, CURLOPT_URL, $url);
curl_setopt($ch, CURLOPT_CUSTOMREQUEST, 'PUT');
curl_setopt($ch, CURLOPT_POSTFIELDS, $icalData);
curl_setopt($ch, CURLOPT_HTTPHEADER, [
    'Content-Type: text/calendar; charset=utf-8'
]);
curl_setopt($ch, CURLOPT_USERPWD, "$username:$password");
curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);

$response = curl_exec($ch);
$httpCode = curl_getinfo($ch, CURLINFO_HTTP_CODE);
curl_close($ch);

echo "Status: $httpCode\n";
?>
```

## Лучшие практики

### Безопасность
1. **Используйте HTTPS** — всегда шифруйте трафик
2. **Сильная аутентификация** — двухфакторная аутентификация
3. **Ограниченные права** — давайте минимально необходимые права
4. **Регулярные обновления** — обновляйте сервер и зависимости

### Производительность
1. **Кэширование** — используйте ETags для проверки изменений
2. **Пагинация** — ограничивайте количество возвращаемых записей
3. **Индексация** — правильно индексируйте поля в базе данных
4. **Сжатие** — включите gzip для больших ответов

### Совместимость
1. **Тестирование** — тестируйте с разными клиентами
2. **Валидация** — проверяйте формат iCalendar
3. **Обработка ошибок** — корректно обрабатывайте HTTP ошибки
4. **Логирование** — ведите логи для диагностики проблем

## Сравнение с аналогами

| Протокол | Преимущества | Недостатки | Использование |
|----------|--------------|------------|---------------|
| **CalDAV** | Стандарт IETF, широкая поддержка, двухсторонняя синхронизация | Сложность реализации сервера | Корпоративные календари, личные планировщики |
| **iCalendar (.ics)** | Простота, универсальность | Односторонний импорт/экспорт | Обмен событиями, подписки на календари |
| **Google Calendar API** | Богатая функциональность, интеграция с экосистемой Google | Проприетарный, зависимость от Google | Веб-приложения, интеграции с Google сервисами |
| **Microsoft Exchange** | Глубокая интеграция с Outlook, enterprise функции | Высокая стоимость, сложность настройки | Корпоративные среды, Microsoft экосистема |

## Полезные ресурсы

### Официальная документация
- [RFC 4791 - CalDAV](https://datatracker.ietf.org/doc/html/rfc4791)
- [RFC 5545 - iCalendar](https://datatracker.ietf.org/doc/html/rfc5545)
- [RFC 6638 - CalDAV Scheduling](https://datatracker.ietf.org/doc/html/rfc6638)

### Серверные реализации
- [Radicale](https://radicale.org/) - легковесный Python сервер
- [Baïkal](https://sabre.io/baikal/) - PHP сервер с веб-интерфейсом
- [Nextcloud Calendar](https://apps.nextcloud.com/apps/calendar) - часть экосистемы Nextcloud
- [ownCloud Calendar](https://marketplace.owncloud.com/apps/calendar)

### Клиентские библиотеки
- Python: [caldav](https://github.com/python-caldav/caldav)
- JavaScript: [ical.js](https://github.com/kewisch/ical.js/)
- PHP: [SabreDAV](https://sabre.io/dav/)
- Java: [ical4j](https://github.com/ical4j/ical4j)

### Онлайн инструменты
- [iCalendar validator](https://icalendar.org/validator.html)
- [CalDAV tester](https://www.davtest.com/)

---

**Автор:** Dupley Maxim Igorevich
**Контакты:** maksimqwe42@mail.ru
**Дата создания:** Январь 2026
**Последнее обновление:** Январь 2026

