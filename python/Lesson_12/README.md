# Веб-разработка на Python: Основы FastAPI, Flask и Django

Веб-разработка на Python предлагает несколько мощных фреймворков для создания веб-приложений.

**Рассмотрим основы `FastAPI`, `Flask` и `Django`, а также примеры работы с этими инструментами.**

### Основы FastAPI: создание проекта и работа с API

`FastAPI` — современный веб-фреймворк для создания API на Python, который обеспечивает быструю разработку и высокую производительность.

#### 1. Установка FastAPI и Uvicorn

```bash
pip install fastapi uvicorn
```

#### 2. Создание простого API

**Создайте файл `main.py`:**

```python
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/items/{item_id}")
def read_item(item_id: int, q: str = None):
    return {"item_id": item_id, "q": q}
```

#### 3. Запуск приложения

**Запустите сервер с помощью `Uvicorn`:**

```bash
uvicorn main:app --reload
```

Теперь вы можете открыть `http://127.0.0.1:8000` в браузере, чтобы увидеть ваше приложение.

Документация API будет доступна по адресу: `http://127.0.0.1:8000/docs`.

### Введение в Flask: создание простого web-приложения

`Flask` — лёгкий веб-фреймворк, который позволяет быстро создавать веб-приложения.

#### 1. Установка Flask

```bash
pip install flask
```

#### 2. Создание простого web-приложения

**Создайте файл `app.py`:**

```python
from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/')
def home():
    return jsonify({"message": "Hello, World!"})

@app.route('/items/<int:item_id>')
def get_item(item_id):
    return jsonify({"item_id": item_id})

if __name__ == '__main__':
    app.run(debug=True)
```

#### 3. Запуск приложения

**Запустите приложение:**

```bash
python app.py
```

Теперь вы можете открыть `http://127.0.0.1:5000` в браузере, чтобы увидеть ваше приложение.

### Основы Django: Создание проекта и работа с моделями

`Django` — полный фреймворк для создания веб-приложений, который включает множество встроенных инструментов.

#### 1. Установка Django

```bash
pip install django
```

#### 2. Создание проекта

**Создайте проект Django:**

```bash
django-admin startproject myproject
cd myproject
```

#### 3. Создание приложения

**Создайте приложение внутри проекта:**

```bash
python manage.py startapp myapp
```

#### 4. Определение моделей

**В файле `myapp/models.py` определите модели:**

```python
from django.db import models

class Item(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()

    def __str__(self):
        return self.name
```

#### 5. Миграции и Администрирование

**Примените миграции:**

```bash
python manage.py makemigrations
python manage.py migrate
```

**Добавьте приложение в `INSTALLED_APPS` в `myproject/settings.py`:**

```python
INSTALLED_APPS = [
    ...
    'myapp',
]
```

#### 6. Запуск сервера

**Запустите сервер:**

```bash
python manage.py runserver
```

Теперь вы можете открыть `http://127.0.0.1:8000` в браузере, чтобы увидеть ваш проект.

`Вы также можете использовать админ-панель Django для управления моделями`

### Выводы 

- `FastAPI` идеально подходит для создания быстрых и высокопроизводительных API. Он обеспечивает автоматическую документацию и поддержку асинхронного программирования.

- `Flask` является лёгким и гибким фреймворком для создания простых веб-приложений. Он предоставляет основную функциональность и позволяет добавлять расширения по мере необходимости.

- `Django` предоставляет полный набор инструментов для создания сложных веб-приложений, включая систему управления базами данных, админ-панель и поддержку аутентификации.

Эти фреймворки позволяют разрабатывать веб-приложения на Python, выбирая тот, который лучше всего соответствует вашим потребностям и предпочтениям.


**Автор:** Дуплей Максим Игоревич

**Дата:** 07.09.2024

**Версия:** 1.0