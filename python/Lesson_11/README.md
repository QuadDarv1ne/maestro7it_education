# Работа с базами данных: Основы SQL и использование SQLite

Работа с базами данных в Python может включать использование SQL для управления данными и библиотек для взаимодействия с базами данных.

В этом руководстве рассмотрим основы SQL, использование `SQLite` и основы `ORM (Object-Relational Mapping)`.

### Основы SQL-запросов

`SQL (Structured Query Language)` — это язык запросов для управления и манипулирования данными в реляционных базах данных.

**Вот основные SQL-запросы:**

#### 1. Создание таблиц

```sql
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL,
    email TEXT NOT NULL UNIQUE,
    password TEXT NOT NULL
);
```

#### 2. Вставка данных

```sql
INSERT INTO users (username, email, password) VALUES ('Alice', 'alice@example.com', 'password123');
```

#### 3. Выбор данных

```sql
SELECT * FROM users;
SELECT username, email FROM users WHERE id = 1;
```

#### 4. Обновление данных

```sql
UPDATE users SET email = 'alice_new@example.com' WHERE username = 'Alice';
```

#### 5. Удаление данных

```sql
DELETE FROM users WHERE id = 1;
```

#### 6. Условные операторы и сортировка

```sql
SELECT * FROM users WHERE username LIKE 'A%' ORDER BY username DESC;
```

### Работа с базами данных SQLite

`SQLite` — это встроенная база данных, которая хранит данные в одном файле и не требует установки серверного ПО.

В Python взаимодействие с SQLite осуществляется с помощью модуля `sqlite3`.

#### 1. Установка и подключение

```python
import sqlite3

# Подключение к базе данных (создает файл базы данных, если его нет)
connection = sqlite3.connect('example.db')

# Создание курсора для выполнения запросов
cursor = connection.cursor()
```

#### 2. Создание таблицы

```python
cursor.execute('''
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL,
    email TEXT NOT NULL UNIQUE,
    password TEXT NOT NULL
)
''')

# Сохранение изменений
connection.commit()
```

#### 3. Вставка данных

```python
cursor.execute('''
INSERT INTO users (username, email, password) VALUES (?, ?, ?)
''', ('Alice', 'alice@example.com', 'password123'))

# Сохранение изменений
connection.commit()
```

#### 4. Выбор данных

```python
cursor.execute('SELECT * FROM users')
rows = cursor.fetchall()

for row in rows:
    print(row)
```

#### 5. Обновление и удаление данных

```python
cursor.execute('''
UPDATE users SET email = ? WHERE username = ?
''', ('alice_new@example.com', 'Alice'))

cursor.execute('''
DELETE FROM users WHERE username = ?
''', ('Alice',))

# Сохранение изменений
connection.commit()
```

#### 6. Закрытие соединения

```python
# Закрытие соединения с базой данных
connection.close()
```

### Основы ORM (Object-Relational Mapping)

`ORM (Object-Relational Mapping)` позволяет работать с базами данных, используя объекты Python, что упрощает работу с данными.

**В Python популярным инструментом для ORM является SQLAlchemy.**

#### 1. Установка SQLAlchemy

```bash
pip install sqlalchemy
```

#### 2. Основы SQLAlchemy

**Пример использования SQLAlchemy для работы с базой данных SQLite:**

```python
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Создание базы данных и подключение к ней
engine = create_engine('sqlite:///example.db', echo=True)
Base = declarative_base()

# Определение модели
class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True)
    email = Column(String, unique=True)
    password = Column(String)

# Создание таблицы
Base.metadata.create_all(engine)

# Создание сессии
Session = sessionmaker(bind=engine)
session = Session()

# Вставка данных
new_user = User(username='Alice', email='alice@example.com', password='password123')
session.add(new_user)
session.commit()

# Запрос данных
users = session.query(User).all()
for user in users:
    print(user.username, user.email)

# Обновление данных
user = session.query(User).filter_by(username='Alice').first()
user.email = 'alice_new@example.com'
session.commit()

# Удаление данных
session.delete(user)
session.commit()

# Закрытие сессии
session.close()
```

### Выводы

Работа с базами данных в Python может включать использование SQL для выполнения запросов и SQLite для хранения данных в файле.

SQLAlchemy предоставляет удобные средства для работы с базами данных через ORM, упрощая взаимодействие с данными и управляя ими через объекты Python.

Эти инструменты позволяют эффективно управлять данными и интегрировать базы данных в ваши приложения.



**Автор:** Дуплей Максим Игоревич

**Дата:** 07.09.2024

**Версия:** 1.0