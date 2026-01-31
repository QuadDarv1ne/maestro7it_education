# 🐍 Полный мануал по Reflex Framework: Создание веб-приложений на Python

## 📋 Содержание

1. [Введение в Reflex](#введение-в-reflex)
2. [Установка и настройка](#установка-и-настройка)
3. [Архитектура Reflex](#архитектура-reflex)
4. [Состояния и реактивность](#состояния-и-реактивность)
5. [Компоненты и стили](#компоненты-и-стили)
6. [Маршрутизация](#маршрутизация)
7. [Работа с данными](#работа-с-данными)
8. [События и обработчики](#события-и-обработчики)
9. [Развертывание](#развертывание)
10. [Лучшие практики](#лучшие-практики)

## Введение в Reflex

**Reflex** — это современный фреймворк с открытым исходным кодом для создания веб-приложений на Python. В отличие от традиционных подходов, где фронтенд и бэкенд разрабатываются отдельно, Reflex позволяет создавать полные веб-приложения исключительно на Python.

### Особенности Reflex:

✅ **Python-first**: Полностью на Python (без JavaScript)
✅ **Реактивность**: Автоматическое обновление UI при изменении состояния
✅ **Безопасность**: Встроенная безопасность (без XSS, CSRF и т.д.)
✅ **Простота**: Минимум настройки, максимум продуктивности
✅ **Масштабируемость**: Подходит для прототипов и production
✅ **Компонентный подход**: Переиспользуемые компоненты
✅ **Автоматическая маршрутизация**: Страницы создаются автоматически

### Когда использовать Reflex?

**Подходит для:**
- Прототипов и MVP
- Дашбордов и аналитических панелей
- CRUD приложений
- Машинного обучения и анализа данных
- Внутренних инструментов
- Образовательных приложений

**Не всегда подходит для:**
- Сложных SPA с богатым UX
- Приложений с интенсивной клиентской логикой
- Проектов, требующих полного контроля над фронтендом
- Высоконагруженных систем (пока в разработке)

## Установка и настройка

### Требования:

- Python 3.7+
- pip (пакетный менеджер Python)
- Node.js и npm (для компиляции фронтенда, автоматически устанавливается)

### Установка:

```bash
# Установка Reflex
pip install reflex

# Проверка установки
reflex --version

# Создание нового проекта
reflex init my_app

# Перейти в директорию проекта
cd my_app

# Запуск приложения
reflex run
```

### Структура проекта:

```
my_app/
├── .web/                    # Скомпилированные файлы фронтенда
├── assets/                 # Статические файлы
│   ├── favicon.ico
│   └── logo.svg
├── my_app/                 # Основной код приложения
│   ├── __init__.py
│   ├── my_app.py          # Главный файл приложения
│   └── styles.py          # Стили приложения
├── rxconfig.py            # Конфигурация приложения
└── requirements.txt       # Зависимости Python
```

### Конфигурация приложения:

```python
# rxconfig.py
import reflex as rx

config = rx.Config(
    app_name="my_app",
    db_url="sqlite:///reflex.db",  # URL базы данных
    env=rx.Env.DEV,               # Режим окружения
    telemetry_enabled=True,       # Сбор телеметрии
    admin_dash=rx.AdminDash(      # Админ панель (опционально)
        models=[],
        view_class=rx.AdminDashConfig
    ),
)
```

### Настройка виртуального окружения:

```bash
# Создание виртуального окружения
python -m venv venv

# Активация (Windows)
venv\Scripts\activate

# Активация (macOS/Linux)
source venv/bin/activate

# Установка зависимостей
pip install reflex

# Установка дополнительных пакетов
pip install pandas numpy requests
```

## Архитектура Reflex

### Основные компоненты:

#### 1. App (Приложение):
```python
# my_app/my_app.py
import reflex as rx

class State(rx.State):
    """Состояние приложения."""
    pass

def index() -> rx.Component:
    """Главная страница."""
    return rx.text("Hello Reflex!")

# Создание приложения
app = rx.App()
app.add_page(index)
```

#### 2. State (Состояние):
```python
import reflex as rx
import requests

class State(rx.State):
    """Основное состояние приложения."""
    
    # Переменные состояния
    text: str = "Hello"
    count: int = 0
    user_input: str = ""
    items: list = []
    
    # Асинхронное состояние
    loading: bool = False
    api_data: list = []
    
    def increment(self):
        """Увеличить счетчик."""
        self.count += 1
    
    def decrement(self):
        """Уменьшить счетчик."""
        self.count -= 1
    
    def add_item(self):
        """Добавить элемент."""
        if self.user_input:
            self.items.append(self.user_input)
            self.user_input = ""
    
    def clear_items(self):
        """Очистить список."""
        self.items = []
    
    async def fetch_data(self):
        """Асинхронное получение данных."""
        self.loading = True
        try:
            # Симуляция API вызова
            import asyncio
            await asyncio.sleep(1)  # Задержка
            self.api_data = ["Item 1", "Item 2", "Item 3"]
        finally:
            self.loading = False
```

#### 3. Components (Компоненты):
```python
import reflex as rx
from . import style
from .state import State

def index() -> rx.Component:
    """Главная страница."""
    return rx.container(
        rx.vstack(
            rx.heading("My Reflex App", size="2xl"),
            rx.text("Count: ", State.count),
            rx.hstack(
                rx.button("Increment", on_click=State.increment),
                rx.button("Decrement", on_click=State.decrement),
            ),
            rx.input(
                placeholder="Enter item...",
                value=State.user_input,
                on_change=State.set_user_input
            ),
            rx.button("Add Item", on_click=State.add_item),
            rx.button("Clear Items", on_click=State.clear_items),
            rx.foreach(
                State.items,
                lambda item: rx.badge(item, variant="outline")
            ),
            spacing="1.5em",
            padding="2em",
            align="center",
        ),
        bg=style.bg_dark_color,
        min_height="100vh",
    )
```

### Стили приложения:

```python
# my_app/styles.py
import reflex as rx

# Цвета
border_radius = "0.375rem"
border = f"1px solid {rx.color.alpha('gray', 6)}"
text_color = rx.color("gray", 12)
bg_color = rx.color("gray", 1)
bg_dark_color = rx.color("gray", 2)
accent_color = rx.color("accent", 10)
border_color = rx.color("gray", 5)

# Стили
template_row_gap = "1em"
template_column_gap = "1em"
template_pad = "2em"

# Стиль для карточки
card = {
    "bg": bg_color,
    "padding": "1em",
    "border_radius": border_radius,
    "border": border,
}

# Стиль для кнопки
button_style = {
    "border_radius": border_radius,
    "bg": accent_color,
    "color": "white",
    "_hover": {
        "bg": rx.color("accent", 8),
    },
}
```

## Состояния и реактивность

### Основы состояний:

```python
import reflex as rx

class CounterState(rx.State):
    """Состояние счетчика."""
    count: int = 0
    
    def increment(self):
        self.count += 1
    
    def decrement(self):
        self.count -= 1
    
    def reset(self):
        self.count = 0

# Состояние с валидацией
class FormState(rx.State):
    """Состояние формы."""
    name: str = ""
    email: str = ""
    age: int = 0
    errors: dict = {}
    
    def set_name(self, name: str):
        self.name = name
        # Валидация
        if len(name) < 2:
            self.errors["name"] = "Name must be at least 2 characters"
        else:
            self.errors.pop("name", None)
    
    def set_email(self, email: str):
        self.email = email
        # Простая валидация email
        if "@" not in email:
            self.errors["email"] = "Invalid email format"
        else:
            self.errors.pop("email", None)
    
    def set_age(self, age: str):
        try:
            self.age = int(age)
            if self.age < 0 or self.age > 120:
                self.errors["age"] = "Age must be between 0 and 120"
            else:
                self.errors.pop("age", None)
        except ValueError:
            self.errors["age"] = "Age must be a number"
    
    def submit_form(self):
        """Отправка формы."""
        if not self.errors:
            # Здесь логика сохранения данных
            print(f"Form submitted: {self.name}, {self.email}, {self.age}")
            # Сброс формы
            self.name = ""
            self.email = ""
            self.age = 0
```

### Компьютерные свойства:

```python
import reflex as rx

class CalculatorState(rx.State):
    """Состояние калькулятора."""
    num1: float = 0
    num2: float = 0
    operation: str = "+"
    
    @rx.var
    def result(self) -> float:
        """Вычисляемое свойство для результата."""
        if self.operation == "+":
            return self.num1 + self.num2
        elif self.operation == "-":
            return self.num1 - self.num2
        elif self.operation == "*":
            return self.num1 * self.num2
        elif self.operation == "/":
            if self.num2 != 0:
                return self.num1 / self.num2
            else:
                return float('inf')  # Бесконечность при делении на 0
        else:
            return 0
    
    @rx.var
    def is_positive(self) -> bool:
        """Проверка, является ли результат положительным."""
        return self.result > 0
    
    @rx.var
    def calculation_string(self) -> str:
        """Строка вычисления."""
        return f"{self.num1} {self.operation} {self.num2} = {self.result}"

class TodoState(rx.State):
    """Состояние задач."""
    todos: list = []
    new_todo: str = ""
    
    @rx.var
    def completed_count(self) -> int:
        """Количество выполненных задач."""
        return len([todo for todo in self.todos if todo.get('completed', False)])
    
    @rx.var
    def pending_count(self) -> int:
        """Количество невыполненных задач."""
        return len([todo for todo in self.todos if not todo.get('completed', False)])
    
    @rx.var
    def total_count(self) -> int:
        """Общее количество задач."""
        return len(self.todos)
    
    def add_todo(self):
        """Добавить задачу."""
        if self.new_todo.strip():
            self.todos.append({
                'text': self.new_todo.strip(),
                'completed': False,
                'id': len(self.todos)
            })
            self.new_todo = ""
    
    def toggle_todo(self, todo_id: int):
        """Переключить статус задачи."""
        for todo in self.todos:
            if todo['id'] == todo_id:
                todo['completed'] = not todo['completed']
                break
```

### Асинхронные состояния:

```python
import reflex as rx
import asyncio
import aiohttp

class AsyncState(rx.State):
    """Асинхронное состояние."""
    loading: bool = False
    data: list = []
    error: str = ""
    
    async def fetch_data(self):
        """Асинхронное получение данных."""
        self.loading = True
        self.error = ""
        
        try:
            # Используем asyncio для симуляции API вызова
            await asyncio.sleep(2)  # Симуляция задержки
            
            # В реальном приложении здесь будет вызов API
            self.data = [
                {"id": 1, "name": "Item 1", "value": 100},
                {"id": 2, "name": "Item 2", "value": 200},
                {"id": 3, "name": "Item 3", "value": 300},
            ]
        except Exception as e:
            self.error = str(e)
        finally:
            self.loading = False
    
    async def fetch_from_api(self):
        """Получение данных из внешнего API."""
        self.loading = True
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get('https://jsonplaceholder.typicode.com/posts?_limit=5') as response:
                    self.data = await response.json()
        except Exception as e:
            self.error = f"API Error: {str(e)}"
        finally:
            self.loading = False

class FileUploadState(rx.State):
    """Состояние загрузки файлов."""
    file_data: str = ""
    file_name: str = ""
    uploading: bool = False
    
    async def handle_upload(self, files: list[rx.UploadFile]):
        """Обработка загрузки файлов."""
        for file in files:
            self.uploading = True
            try:
                upload_data = await file.read()
                self.file_data = upload_data.decode("utf-8")
                self.file_name = file.filename
            except Exception as e:
                self.file_data = f"Error reading file: {str(e)}"
            finally:
                self.uploading = False
```

## Компоненты и стили

### Основные компоненты:

```python
import reflex as rx
from .styles import *

def header_component(title: str) -> rx.Component:
    """Компонент заголовка."""
    return rx.box(
        rx.heading(title, size="lg"),
        padding="1em",
        bg=accent_color,
        color="white",
        border_radius=border_radius,
    )

def button_component(text: str, on_click, variant: str = "solid") -> rx.Component:
    """Компонент кнопки."""
    return rx.button(
        text,
        on_click=on_click,
        variant=variant,
        style=button_style
    )

def input_component(placeholder: str, value, on_change) -> rx.Component:
    """Компонент ввода."""
    return rx.input(
        placeholder=placeholder,
        value=value,
        on_change=on_change,
        border=border,
        border_radius=border_radius,
        padding="0.5em",
    )

def card_component(content: rx.Component) -> rx.Component:
    """Компонент карточки."""
    return rx.card(
        content,
        style=card
    )

def list_component(items: list) -> rx.Component:
    """Компонент списка."""
    return rx.vstack(
        rx.foreach(
            items,
            lambda item: rx.list_item(
                rx.text(item),
                padding="0.5em",
                border_bottom=border
            )
        ),
        spacing="0"
    )
```

### Сложные компоненты:

```python
import reflex as rx
from .state import TodoState

def todo_list() -> rx.Component:
    """Компонент списка задач."""
    return rx.card(
        rx.vstack(
            # Форма добавления
            rx.hstack(
                rx.input(
                    placeholder="Add a new task...",
                    value=TodoState.new_todo,
                    on_change=TodoState.set_new_todo,
                    flex="1"
                ),
                rx.button(
                    "Add",
                    on_click=TodoState.add_todo,
                    bg="green",
                    color="white"
                ),
                width="100%"
            ),
            
            # Счетчики
            rx.hstack(
                rx.badge(f"Total: {TodoState.total_count}", variant="outline"),
                rx.badge(f"Pending: {TodoState.pending_count}", variant="outline"),
                rx.badge(f"Completed: {TodoState.completed_count}", variant="outline"),
                padding="1em 0"
            ),
            
            # Список задач
            rx.vstack(
                rx.foreach(
                    TodoState.todos,
                    lambda todo: todo_item(todo)
                ),
                spacing="0.5em",
                width="100%"
            ),
            
            spacing="1em",
            width="100%"
        ),
        padding="1.5em",
        width="100%",
        max_width="600px"
    )

def todo_item(todo) -> rx.Component:
    """Компонент отдельной задачи."""
    return rx.hstack(
        rx.checkbox(
            checked=todo["completed"],
            on_change=lambda checked: TodoState.toggle_todo(todo["id"])
        ),
        rx.text(
            todo["text"],
            text_decoration="line-through" if todo["completed"] else "none",
            color="gray" if todo["completed"] else "inherit"
        ),
        rx.button(
            "Delete",
            size="sm",
            variant="outline",
            color_scheme="red"
        ),
        width="100%",
        padding="0.5em",
        border=border,
        border_radius=border_radius
    )

def data_table(data: list) -> rx.Component:
    """Компонент таблицы данных."""
    if not data:
        return rx.text("No data available")
    
    headers = list(data[0].keys()) if data else []
    
    return rx.table.root(
        rx.table.header(
            rx.table.row(
                *[rx.table.column_header_cell(header) for header in headers]
            )
        ),
        rx.table.body(
            rx.foreach(
                data,
                lambda row: rx.table.row(
                    *[rx.table.cell(row[key]) for key in headers]
                )
            )
        ),
        variant="striped",
        size="md"
    )
```

### Стили и темизация:

```python
import reflex as rx

# Темы
class ThemeState(rx.State):
    """Состояние темы."""
    dark_mode: bool = False
    
    def toggle_theme(self):
        self.dark_mode = not self.dark_mode

def theme_switch() -> rx.Component:
    """Переключатель темы."""
    return rx.cond(
        ThemeState.dark_mode,
        rx.icon_button(
            rx.icon("sun", size=24),
            on_click=ThemeState.toggle_theme,
            variant="ghost"
        ),
        rx.icon_button(
            rx.icon("moon", size=24),
            on_click=ThemeState.toggle_theme,
            variant="ghost"
        )
    )

# Стили на основе состояния
def conditional_styled_component() -> rx.Component:
    """Компонент с условными стилями."""
    return rx.cond(
        ThemeState.dark_mode,
        rx.box(
            rx.text("Dark mode content"),
            bg="gray.800",
            color="white",
            padding="1em",
            border_radius="md"
        ),
        rx.box(
            rx.text("Light mode content"),
            bg="gray.100",
            color="black",
            padding="1em",
            border_radius="md"
        )
    )

# Адаптивные стили
def responsive_component() -> rx.Component:
    """Адаптивный компонент."""
    return rx.vstack(
        rx.heading("Responsive Design", size="lg"),
        rx.text("This layout adapts to different screen sizes"),
        rx.grid(
            rx.box("Item 1", padding="1em", bg="blue.100"),
            rx.box("Item 2", padding="1em", bg="green.100"),
            rx.box("Item 3", padding="1em", bg="purple.100"),
            rx.box("Item 4", padding="1em", bg="orange.100"),
            columns=[1, 2, 3, 4],  # [mobile, tablet, laptop, desktop]
            gap="1em",
            width="100%"
        ),
        spacing="1.5em",
        padding="2em"
    )
```

## Маршрутизация

### Базовая маршрутизация:

```python
import reflex as rx
from . import styles
from .states.main_state import MainState
from .pages import index, about, contact, dashboard

class AppState(rx.State):
    """Глобальное состояние приложения."""
    pass

def sidebar() -> rx.Component:
    """Боковая панель навигации."""
    return rx.drawer(
        rx.drawer_overlay(
            rx.drawer_content(
                rx.vstack(
                    rx.heading("Menu", size="lg"),
                    rx.divider(),
                    nav_link("Home", "/"),
                    nav_link("About", "/about"),
                    nav_link("Contact", "/contact"),
                    nav_link("Dashboard", "/dashboard"),
                    padding="2em",
                    height="100vh",
                    bg=styles.bg_color
                )
            )
        ),
        placement="left"
    )

def nav_link(text: str, href: str) -> rx.Component:
    """Компонент ссылки навигации."""
    return rx.link(
        rx.button(
            text,
            variant="ghost",
            width="100%",
            justify="start"
        ),
        href=href,
        text_decoration="none",
        width="100%"
    )

def navbar() -> rx.Component:
    """Навигационная панель."""
    return rx.hstack(
        rx.heading("My App", size="lg"),
        rx.spacer(),
        rx.desktop_only(
            rx.hstack(
                nav_link("Home", "/"),
                nav_link("About", "/about"),
                nav_link("Contact", "/contact"),
                nav_link("Dashboard", "/dashboard"),
            )
        ),
        rx.mobile_and_tablet(
            rx.menu(
                rx.menu_button(
                    rx.icon("menu", size=32)
                ),
                rx.menu_list(
                    nav_link("Home", "/"),
                    nav_link("About", "/about"),
                    nav_link("Contact", "/contact"),
                    nav_link("Dashboard", "/dashboard"),
                )
            )
        ),
        padding_x="2em",
        padding_y="1em",
        bg=styles.accent_color,
        color="white",
        width="100%"
    )

# Определение страниц
def index_page() -> rx.Component:
    """Главная страница."""
    return rx.vstack(
        navbar(),
        rx.container(
            rx.heading("Welcome to Reflex!", size="2xl"),
            rx.text("Build web apps with Python"),
            rx.button(
                "Get Started",
                on_click=lambda: rx.redirect("/about"),
                bg="blue.500",
                color="white"
            ),
            padding_y="6em",
            align="center",
            spacing="1.5em"
        ),
        width="100%",
        spacing="0"
    )

def about_page() -> rx.Component:
    """Страница о нас."""
    return rx.vstack(
        navbar(),
        rx.container(
            rx.heading("About Us", size="2xl"),
            rx.text("Learn more about our company and mission."),
            rx.button(
                "Back to Home",
                on_click=lambda: rx.redirect("/"),
                variant="outline"
            ),
            padding_y="6em",
            align="center",
            spacing="1.5em"
        ),
        width="100%",
        spacing="0"
    )

def contact_page() -> rx.Component:
    """Страница контактов."""
    return rx.vstack(
        navbar(),
        rx.container(
            rx.heading("Contact Us", size="2xl"),
            rx.text("Get in touch with our team."),
            rx.form(
                rx.vstack(
                    rx.input(placeholder="Your Name", name="name"),
                    rx.text_area(placeholder="Your Message", name="message"),
                    rx.button("Send Message", type_="submit"),
                    spacing="1em"
                )
            ),
            padding_y="6em",
            align="center",
            spacing="1.5em"
        ),
        width="100%",
        spacing="0"
    )
```

### Динамическая маршрутизация:

```python
import reflex as rx
from typing import Dict

class UserProfileState(rx.State):
    """Состояние профиля пользователя."""
    user_id: str = ""
    user_data: Dict = {}
    loading: bool = False
    
    def set_user_id(self, user_id: str):
        """Установить ID пользователя из URL."""
        self.user_id = user_id
        self.load_user_data()
    
    def load_user_data(self):
        """Загрузить данные пользователя."""
        self.loading = True
        # Симуляция загрузки данных
        import asyncio
        asyncio.create_task(self._async_load())
    
    async def _async_load(self):
        """Асинхронная загрузка данных."""
        await asyncio.sleep(1)  # Симуляция задержки
        self.user_data = {
            "id": self.user_id,
            "name": f"User {self.user_id}",
            "email": f"user{self.user_id}@example.com",
            "join_date": "2023-01-01"
        }
        self.loading = False

def user_profile_page(user_id: str) -> rx.Component:
    """Страница профиля пользователя."""
    # Установка user_id из параметров маршрута
    UserProfileState.set_user_id(user_id)
    
    return rx.vstack(
        navbar(),
        rx.container(
            rx.cond(
                UserProfileState.loading,
                rx.spinner(size="lg"),
                rx.vstack(
                    rx.heading(f"Profile: {UserProfileState.user_data['name']}", size="xl"),
                    rx.card(
                        rx.vstack(
                            rx.text(f"ID: {UserProfileState.user_data['id']}"),
                            rx.text(f"Email: {UserProfileState.user_data['email']}"),
                            rx.text(f"Joined: {UserProfileState.user_data['join_date']}"),
                            spacing="0.5em"
                        ),
                        padding="1.5em"
                    ),
                    rx.button(
                        "Back to Users",
                        on_click=lambda: rx.redirect("/users"),
                        variant="outline"
                    ),
                    spacing="1.5em",
                    align="center"
                )
            ),
            padding_y="4em",
            max_width="600px"
        ),
        width="100%",
        spacing="0"
    )

class UsersState(rx.State):
    """Состояние списка пользователей."""
    users: list = [
        {"id": "1", "name": "Alice Johnson", "email": "alice@example.com"},
        {"id": "2", "name": "Bob Smith", "email": "bob@example.com"},
        {"id": "3", "name": "Carol Davis", "email": "carol@example.com"},
    ]
    
    def view_user(self, user_id: str):
        """Перейти к просмотру пользователя."""
        return rx.redirect(f"/user/{user_id}")

def users_list_page() -> rx.Component:
    """Страница списка пользователей."""
    return rx.vstack(
        navbar(),
        rx.container(
            rx.vstack(
                rx.heading("Users", size="2xl"),
                rx.table.root(
                    rx.table.header(
                        rx.table.row(
                            rx.table.column_header_cell("ID"),
                            rx.table.column_header_cell("Name"),
                            rx.table.column_header_cell("Email"),
                            rx.table.column_header_cell("Actions")
                        )
                    ),
                    rx.table.body(
                        rx.foreach(
                            UsersState.users,
                            lambda user: rx.table.row(
                                rx.table.cell(user["id"]),
                                rx.table.cell(user["name"]),
                                rx.table.cell(user["email"]),
                                rx.table.cell(
                                    rx.button(
                                        "View",
                                        on_click=lambda: UsersState.view_user(user["id"]),
                                        size="sm"
                                    )
                                )
                            )
                        )
                    ),
                    variant="striped",
                    width="100%"
                ),
                spacing="1.5em",
                align="stretch"
            ),
            padding_y="4em",
            max_width="800px"
        ),
        width="100%",
        spacing="0"
    )
```

### Маршрутизация с параметрами:

```python
import reflex as rx
from urllib.parse import urlparse, parse_qs

class ProductState(rx.State):
    """Состояние продукта."""
    product_id: str = ""
    category: str = ""
    sort_by: str = "name"
    page: int = 1
    products: list = []
    
    def on_load(self, router_data: dict):
        """Обработка параметров маршрута."""
        self.product_id = router_data.get("pathname", "").split("/")[-1]
        query_params = router_data.get("query", {})
        self.category = query_params.get("category", "")
        self.sort_by = query_params.get("sort", "name")
        self.page = int(query_params.get("page", 1))
        self.load_products()
    
    def load_products(self):
        """Загрузка продуктов с учетом фильтров."""
        # Симуляция загрузки продуктов
        self.products = [
            {"id": f"prod-{i}", "name": f"Product {i}", "price": i * 10, "category": "electronics"}
            for i in range(1, 11)
        ]

def product_detail_page(product_id: str) -> rx.Component:
    """Страница деталей продукта."""
    return rx.vstack(
        navbar(),
        rx.container(
            rx.vstack(
                rx.heading(f"Product: {product_id}", size="2xl"),
                # Здесь будет отображение деталей продукта
                rx.button(
                    "Back to Products",
                    on_click=lambda: rx.redirect("/products"),
                    variant="outline"
                ),
                spacing="1.5em",
                align="center"
            ),
            padding_y="4em",
            max_width="800px"
        ),
        width="100%",
        spacing="0"
    )

def products_page() -> rx.Component:
    """Страница списка продуктов."""
    return rx.vstack(
        navbar(),
        rx.container(
            rx.vstack(
                rx.heading("Products", size="2xl"),
                
                # Фильтры
                rx.hstack(
                    rx.select(
                        ["electronics", "clothing", "books"],
                        placeholder="Category",
                        on_change=lambda value: rx.redirect(f"/products?category={value}")
                    ),
                    rx.select(
                        ["name", "price", "date"],
                        placeholder="Sort by",
                        on_change=lambda value: rx.redirect(f"/products?sort={value}")
                    ),
                    rx.input(
                        placeholder="Search...",
                        on_change=lambda value: rx.redirect(f"/products?q={value}")
                    ),
                    width="100%",
                    spacing="1em"
                ),
                
                # Список продуктов
                rx.responsive_grid(
                    rx.foreach(
                        ProductState.products,
                        lambda product: product_card(product)
                    ),
                    columns=[1, 2, 3, 4],
                    gap="1em",
                    width="100%"
                ),
                
                # Пагинация
                rx.hstack(
                    rx.button("Previous", disabled=ProductState.page <= 1),
                    rx.text(f"Page {ProductState.page}"),
                    rx.button("Next", disabled=ProductState.page >= 10),
                    spacing="1em"
                ),
                
                spacing="1.5em",
                align="stretch"
            ),
            padding_y="4em",
            max_width="1200px"
        ),
        width="100%",
        spacing="0"
    )

def product_card(product) -> rx.Component:
    """Карточка продукта."""
    return rx.card(
        rx.vstack(
            rx.heading(product["name"], size="md"),
            rx.text(f"${product['price']}", font_size="lg", font_weight="bold"),
            rx.text(f"Category: {product['category']}"),
            rx.button(
                "View Details",
                on_click=lambda: rx.redirect(f"/product/{product['id']}"),
                width="100%"
            ),
            spacing="0.5em",
            align="stretch"
        ),
        padding="1.5em"
    )
```

## Работа с данными

### Локальное хранение:

```python
import reflex as rx
import json
import os
from typing import List, Dict, Any

class LocalStorageState(rx.State):
    """Состояние с локальным хранением."""
    # Данные в памяти
    items: List[Dict[str, Any]] = []
    
    def add_item(self, item_data: Dict[str, Any]):
        """Добавить элемент в локальное хранилище."""
        self.items.append(item_data)
        self.save_to_file()
    
    def remove_item(self, item_id: str):
        """Удалить элемент из локального хранилища."""
        self.items = [item for item in self.items if item.get('id') != item_id]
        self.save_to_file()
    
    def update_item(self, item_id: str, new_data: Dict[str, Any]):
        """Обновить элемент в локальном хранилище."""
        for i, item in enumerate(self.items):
            if item.get('id') == item_id:
                self.items[i].update(new_data)
                break
        self.save_to_file()
    
    def save_to_file(self):
        """Сохранить данные в файл."""
        try:
            with open('local_data.json', 'w') as f:
                json.dump(self.items, f)
        except Exception as e:
            print(f"Error saving data: {e}")
    
    def load_from_file(self):
        """Загрузить данные из файла."""
        try:
            if os.path.exists('local_data.json'):
                with open('local_data.json', 'r') as f:
                    self.items = json.load(f)
        except Exception as e:
            print(f"Error loading data: {e}")
            self.items = []

class SessionStorageState(rx.State):
    """Состояние с сессионным хранилищем."""
    # Данные сохраняются на время сессии пользователя
    user_preferences: Dict[str, Any] = {}
    recent_searches: List[str] = []
    
    def set_preference(self, key: str, value: Any):
        """Установить пользовательскую настройку."""
        self.user_preferences[key] = value
    
    def add_search_history(self, search_term: str):
        """Добавить в историю поиска."""
        if search_term not in self.recent_searches:
            self.recent_searches.insert(0, search_term)
            # Ограничиваем историю 10 последними поисками
            if len(self.recent_searches) > 10:
                self.recent_searches = self.recent_searches[:10]
```

### Работа с API:

```python
import reflex as rx
import httpx
from typing import List, Dict, Any, Optional

class APIState(rx.State):
    """Состояние для работы с API."""
    loading: bool = False
    error: str = ""
    api_token: str = ""
    
    async def make_api_request(
        self, 
        method: str, 
        endpoint: str, 
        data: Optional[Dict] = None,
        params: Optional[Dict] = None
    ) -> Optional[Dict]:
        """Универсальный метод для API запросов."""
        self.loading = True
        self.error = ""
        
        try:
            headers = {"Authorization": f"Bearer {self.api_token}"} if self.api_token else {}
            
            async with httpx.AsyncClient(timeout=30.0) as client:
                response = await client.request(
                    method=method.upper(),
                    url=f"https://api.example.com{endpoint}",
                    json=data,
                    params=params,
                    headers=headers
                )
                
                response.raise_for_status()
                return response.json()
                
        except httpx.RequestError as exc:
            self.error = f"Request error: {str(exc)}"
        except httpx.HTTPStatusError as exc:
            self.error = f"HTTP error {exc.response.status_code}: {exc.response.text}"
        except Exception as exc:
            self.error = f"Unexpected error: {str(exc)}"
        finally:
            self.loading = False
        
        return None

class UserService(APIState):
    """Сервис для работы с пользователями через API."""
    users: List[Dict] = []
    current_user: Optional[Dict] = None
    
    async def fetch_users(self):
        """Получить список пользователей."""
        data = await self.make_api_request("GET", "/users")
        if data:
            self.users = data.get("users", [])
        return self.users
    
    async def fetch_user(self, user_id: str):
        """Получить конкретного пользователя."""
        data = await self.make_api_request("GET", f"/users/{user_id}")
        if data:
            self.current_user = data
        return self.current_user
    
    async def create_user(self, user_data: Dict[str, Any]):
        """Создать нового пользователя."""
        data = await self.make_api_request("POST", "/users", data=user_data)
        if data:
            self.users.append(data)
        return data
    
    async def update_user(self, user_id: str, user_data: Dict[str, Any]):
        """Обновить пользователя."""
        data = await self.make_api_request("PUT", f"/users/{user_id}", data=user_data)
        if data:
            # Обновляем в списке
            for i, user in enumerate(self.users):
                if user.get("id") == user_id:
                    self.users[i] = data
                    break
        return data
    
    async def delete_user(self, user_id: str):
        """Удалить пользователя."""
        await self.make_api_request("DELETE", f"/users/{user_id}")
        self.users = [user for user in self.users if user.get("id") != user_id]

class DataManager(rx.State):
    """Менеджер данных для сложных операций."""
    raw_data: List[Dict] = []
    filtered_data: List[Dict] = []
    search_term: str = ""
    sort_field: str = ""
    sort_direction: str = "asc"  # "asc" or "desc"
    
    def load_data(self, data_source: List[Dict]):
        """Загрузить данные из источника."""
        self.raw_data = data_source
        self.apply_filters()
    
    def set_search_term(self, term: str):
        """Установить поисковый запрос."""
        self.search_term = term.lower()
        self.apply_filters()
    
    def set_sort(self, field: str, direction: str = "toggle"):
        """Установить сортировку."""
        if direction == "toggle":
            if self.sort_field == field:
                self.sort_direction = "desc" if self.sort_direction == "asc" else "asc"
            else:
                self.sort_field = field
                self.sort_direction = "asc"
        else:
            self.sort_field = field
            self.sort_direction = direction
        
        self.apply_filters()
    
    def apply_filters(self):
        """Применить фильтры к данным."""
        # Фильтрация по поисковому запросу
        if self.search_term:
            filtered = [
                item for item in self.raw_data
                if any(
                    self.search_term in str(value).lower()
                    for value in item.values()
                )
            ]
        else:
            filtered = self.raw_data[:]
        
        # Сортировка
        if self.sort_field:
            reverse = self.sort_direction == "desc"
            filtered.sort(
                key=lambda x: x.get(self.sort_field, ""),
                reverse=reverse
            )
        
        self.filtered_data = filtered
    
    def export_filtered_data(self) -> str:
        """Экспорт отфильтрованных данных."""
        import csv
        import io
        
        if not self.filtered_data:
            return ""
        
        output = io.StringIO()
        writer = csv.DictWriter(output, fieldnames=self.filtered_data[0].keys())
        writer.writeheader()
        writer.writerows(self.filtered_data)
        
        return output.getvalue()
```

### Работа с базой данных:

```python
import reflex as rx
from sqlmodel import Field, Session, SQLModel, create_engine, select
from typing import Optional
import os

# Определение модели данных
class User(SQLModel, table=True):
    """Модель пользователя."""
    id: Optional[int] = Field(default=None, primary_key=True)
    username: str = Field(unique=True)
    email: str = Field(unique=True)
    full_name: str = ""
    disabled: bool = False

class Task(SQLModel, table=True):
    """Модель задачи."""
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str
    description: str = ""
    completed: bool = False
    user_id: int = Field(foreign_key="user.id")

class DatabaseState(rx.State):
    """Состояние для работы с базой данных."""
    # Путь к базе данных
    db_url: str = "sqlite:///reflex_app.db"
    engine = None
    
    def setup_db(self):
        """Настройка базы данных."""
        if not self.engine:
            self.engine = create_engine(self.db_url)
            # Создание таблиц
            SQLModel.metadata.create_all(self.engine)
    
    def get_session(self) -> Session:
        """Получить сессию базы данных."""
        if not self.engine:
            self.setup_db()
        return Session(self.engine)

class UserDatabaseState(DatabaseState):
    """Состояние для работы с пользователями в базе данных."""
    current_user: Optional[User] = None
    users: list = []
    
    def load_users(self):
        """Загрузить всех пользователей."""
        with self.get_session() as session:
            users = session.exec(select(User)).all()
            self.users = users
        return self.users
    
    def create_user(self, username: str, email: str, full_name: str = ""):
        """Создать нового пользователя."""
        user = User(username=username, email=email, full_name=full_name)
        with self.get_session() as session:
            session.add(user)
            session.commit()
            session.refresh(user)
        self.load_users()  # Обновить список
        return user
    
    def get_user(self, user_id: int) -> Optional[User]:
        """Получить пользователя по ID."""
        with self.get_session() as session:
            user = session.get(User, user_id)
            self.current_user = user
        return user
    
    def update_user(self, user_id: int, **kwargs):
        """Обновить пользователя."""
        with self.get_session() as session:
            user = session.get(User, user_id)
            for key, value in kwargs.items():
                setattr(user, key, value)
            session.add(user)
            session.commit()
            session.refresh(user)
        self.load_users()  # Обновить список
        return user
    
    def delete_user(self, user_id: int):
        """Удалить пользователя."""
        with self.get_session() as session:
            user = session.get(User, user_id)
            session.delete(user)
            session.commit()
        self.load_users()  # Обновить список

class TaskDatabaseState(DatabaseState):
    """Состояние для работы с задачами в базе данных."""
    tasks: list = []
    current_task: Optional[Task] = None
    
    def load_tasks(self, user_id: Optional[int] = None):
        """Загрузить задачи."""
        with self.get_session() as session:
            query = select(Task)
            if user_id:
                query = query.where(Task.user_id == user_id)
            tasks = session.exec(query).all()
            self.tasks = tasks
        return self.tasks
    
    def create_task(self, title: str, description: str = "", user_id: int = 1):
        """Создать новую задачу."""
        task = Task(title=title, description=description, user_id=user_id)
        with self.get_session() as session:
            session.add(task)
            session.commit()
            session.refresh(task)
        self.load_tasks()  # Обновить список
        return task
    
    def toggle_task_completion(self, task_id: int):
        """Переключить статус выполнения задачи."""
        with self.get_session() as session:
            task = session.get(Task, task_id)
            task.completed = not task.completed
            session.add(task)
            session.commit()
            session.refresh(task)
        self.load_tasks()  # Обновить список
        return task
    
    def delete_task(self, task_id: int):
        """Удалить задачу."""
        with self.get_session() as session:
            task = session.get(Task, task_id)
            session.delete(task)
            session.commit()
        self.load_tasks()  # Обновить список

# Компоненты для работы с базой данных
def user_management_panel() -> rx.Component:
    """Панель управления пользователями."""
    return rx.vstack(
        rx.heading("User Management", size="lg"),
        rx.input(
            placeholder="Username",
            id="username_input"
        ),
        rx.input(
            placeholder="Email",
            id="email_input"
        ),
        rx.input(
            placeholder="Full Name",
            id="fullname_input"
        ),
        rx.button(
            "Create User",
            on_click=lambda: UserDatabaseState.create_user(
                username=rx.Var("username_input.value"),
                email=rx.Var("email_input.value"),
                full_name=rx.Var("fullname_input.value")
            )
        ),
        rx.divider(),
        rx.heading("Users List", size="md"),
        rx.foreach(
            UserDatabaseState.users,
            lambda user: rx.hstack(
                rx.text(user.username),
                rx.text(user.email),
                rx.button(
                    "Edit",
                    size="sm"
                ),
                rx.button(
                    "Delete",
                    size="sm",
                    color_scheme="red",
                    on_click=lambda u=user: UserDatabaseState.delete_user(u.id)
                ),
                border=rx.color("gray", 4),
                padding="0.5em",
                border_radius="0.375rem"
            )
        ),
        spacing="1em",
        align="stretch"
    )
```

## События и обработчики

### Обработчики событий:

```python
import reflex as rx
import asyncio
from typing import Callable, Any

class EventHandlerState(rx.State):
    """Состояние для демонстрации обработчиков событий."""
    clicks: int = 0
    last_event: str = ""
    event_history: list = []
    
    def handle_click(self):
        """Обработчик клика."""
        self.clicks += 1
        self.last_event = f"Click #{self.clicks}"
        self.event_history.append(self.last_event)
        if len(self.event_history) > 10:
            self.event_history.pop(0)
    
    def handle_key_down(self, key: str):
        """Обработчик нажатия клавиши."""
        event_desc = f"Key pressed: {key}"
        self.last_event = event_desc
        self.event_history.append(event_desc)
        if len(self.event_history) > 10:
            self.event_history.pop(0)
    
    def handle_focus(self):
        """Обработчик получения фокуса."""
        event_desc = "Input focused"
        self.last_event = event_desc
        self.event_history.append(event_desc)
        if len(self.event_history) > 10:
            self.event_history.pop(0)
    
    def handle_blur(self):
        """Обработчик потери фокуса."""
        event_desc = "Input blurred"
        self.last_event = event_desc
        self.event_history.append(event_desc)
        if len(self.event_history) > 10:
            self.event_history.pop(0)

def event_demo_component() -> rx.Component:
    """Компонент для демонстрации событий."""
    return rx.vstack(
        rx.heading("Event Handling Demo", size="lg"),
        rx.hstack(
            rx.button(
                "Click me!",
                on_click=EventHandlerState.handle_click,
                bg="blue.500",
                color="white"
            ),
            rx.input(
                placeholder="Focus and type here...",
                on_focus=EventHandlerState.handle_focus,
                on_blur=EventHandlerState.handle_blur,
                on_key_down=EventHandlerState.handle_key_down,
                width="300px"
            ),
        ),
        rx.text(f"Total clicks: {EventHandlerState.clicks}"),
        rx.text(f"Last event: {EventHandlerState.last_event}"),
        rx.heading("Event History", size="md"),
        rx.vstack(
            rx.foreach(
                EventHandlerState.event_history,
                lambda event: rx.text(event, font_size="sm")
            ),
            spacing="0.25em",
            align="start"
        ),
        spacing="1.5em",
        padding="2em",
        border=rx.color("gray", 4),
        border_radius="0.375rem"
    )
```

### Асинхронные обработчики:

```python
import reflex as rx
import asyncio
import aiohttp
from typing import List, Dict

class AsyncHandlerState(rx.State):
    """Состояние для асинхронных обработчиков."""
    loading: bool = False
    results: List[Dict] = []
    progress: int = 0
    status_message: str = ""
    
    async def async_operation(self):
        """Асинхронная операция."""
        self.loading = True
        self.progress = 0
        self.status_message = "Starting operation..."
        
        try:
            # Симуляция длительной операции
            for i in range(1, 11):
                self.progress = i * 10
                self.status_message = f"Processing... {self.progress}%"
                await asyncio.sleep(0.5)  # Симуляция работы
            
            # Имитация получения результатов
            self.results = [
                {"id": i, "name": f"Result {i}", "value": i * 10}
                for i in range(1, 6)
            ]
            self.status_message = "Operation completed!"
            
        except Exception as e:
            self.status_message = f"Error: {str(e)}"
        finally:
            self.loading = False
    
    async def fetch_multiple_apis(self):
        """Получение данных из нескольких API одновременно."""
        self.loading = True
        self.status_message = "Fetching data from APIs..."
        
        try:
            async with aiohttp.ClientSession() as session:
                # Параллельные запросы
                tasks = [
                    self._fetch_api(session, 'https://jsonplaceholder.typicode.com/posts?_limit=3'),
                    self._fetch_api(session, 'https://jsonplaceholder.typicode.com/users?_limit=3'),
                    self._fetch_api(session, 'https://jsonplaceholder.typicode.com/comments?_limit=3')
                ]
                
                results = await asyncio.gather(*tasks, return_exceptions=True)
                
                combined_results = []
                for i, result in enumerate(results):
                    if isinstance(result, Exception):
                        combined_results.append({"error": f"API {i+1} failed: {str(result)}"})
                    else:
                        combined_results.extend(result)
                
                self.results = combined_results
                self.status_message = f"Received {len(combined_results)} items"
                
        except Exception as e:
            self.status_message = f"Error: {str(e)}"
        finally:
            self.loading = False
    
    async def _fetch_api(self, session: aiohttp.ClientSession, url: str):
        """Вспомогательная функция для получения данных из API."""
        async with session.get(url) as response:
            return await response.json()

def async_demo_component() -> rx.Component:
    """Компонент для демонстрации асинхронных операций."""
    return rx.vstack(
        rx.heading("Async Operations Demo", size="lg"),
        rx.hstack(
            rx.button(
                "Start Long Operation",
                on_click=AsyncHandlerState.async_operation,
                bg="purple.500",
                color="white",
                disabled=AsyncHandlerState.loading
            ),
            rx.button(
                "Fetch Multiple APIs",
                on_click=AsyncHandlerState.fetch_multiple_apis,
                bg="teal.500",
                color="white",
                disabled=AsyncHandlerState.loading
            ),
        ),
        rx.cond(
            AsyncHandlerState.loading,
            rx.vstack(
                rx.progress(value=AsyncHandlerState.progress, width="100%"),
                rx.text(AsyncHandlerState.status_message),
                rx.spinner(size="lg"),
            ),
            rx.text(AsyncHandlerState.status_message)
        ),
        rx.cond(
            AsyncHandlerState.results.length() > 0,
            rx.vstack(
                rx.heading("Results", size="md"),
                rx.scroll_area(
                    rx.vstack(
                        rx.foreach(
                            AsyncHandlerState.results,
                            lambda item: rx.card(
                                rx.vstack(
                                    rx.text(f"ID: {item['id']}", font_weight="bold") if "id" in item else rx.text("Data", font_weight="bold"),
                                    rx.text(str(item)),
                                    spacing="0.25em"
                                ),
                                padding="1em",
                                width="100%"
                            )
                        ),
                        spacing="0.5em"
                    ),
                    height="200px",
                    type_="auto"
                ),
                width="100%"
            )
        ),
        spacing="1.5em",
        padding="2em",
        border=rx.color("gray", 4),
        border_radius="0.375rem"
    )
```

### Сложные обработчики с условиями:

```python
import reflex as rx
from typing import Optional

class ConditionalHandlerState(rx.State):
    """Состояние для условных обработчиков."""
    user_role: str = "guest"  # guest, user, admin
    permissions: dict = {}
    action_log: list = []
    
    def setup_permissions(self):
        """Настройка разрешений на основе роли."""
        permission_map = {
            "guest": {"view": True, "edit": False, "delete": False, "admin": False},
            "user": {"view": True, "edit": True, "delete": False, "admin": False},
            "admin": {"view": True, "edit": True, "delete": True, "admin": True}
        }
        self.permissions = permission_map.get(self.user_role, permission_map["guest"])
    
    def safe_action(self, action: str, resource: str):
        """Безопасное выполнение действия с проверкой разрешений."""
        if not self.permissions.get(action, False):
            self.action_log.append(f"Access denied: {self.user_role} cannot {action} {resource}")
            return
        
        # Выполнение действия
        self.action_log.append(f"Action performed: {self.user_role} {action}ed {resource}")
        
        # Ограничение истории действий
        if len(self.action_log) > 20:
            self.action_log.pop(0)
    
    def change_role(self, new_role: str):
        """Смена роли пользователя."""
        self.user_role = new_role
        self.setup_permissions()
        self.action_log.append(f"Role changed to: {new_role}")
    
    def can_perform_action(self, action: str) -> bool:
        """Проверка возможности выполнения действия."""
        return self.permissions.get(action, False)

def conditional_ui_component() -> rx.Component:
    """Компонент с условным UI."""
    return rx.vstack(
        rx.heading("Conditional UI Demo", size="lg"),
        
        # Выбор роли
        rx.hstack(
            rx.text("Role:"),
            rx.select(
                ["guest", "user", "admin"],
                value=ConditionalHandlerState.user_role,
                on_change=ConditionalHandlerState.change_role,
            ),
            rx.badge(ConditionalHandlerState.user_role, variant="outline")
        ),
        
        # Кнопки действий (условно отображаются)
        rx.hstack(
            rx.cond(
                ConditionalHandlerState.can_perform_action("view"),
                rx.button(
                    "View",
                    on_click=lambda: ConditionalHandlerState.safe_action("view", "document"),
                    bg="blue.500",
                    color="white"
                )
            ),
            rx.cond(
                ConditionalHandlerState.can_perform_action("edit"),
                rx.button(
                    "Edit",
                    on_click=lambda: ConditionalHandlerState.safe_action("edit", "document"),
                    bg="yellow.500",
                    color="black"
                )
            ),
            rx.cond(
                ConditionalHandlerState.can_perform_action("delete"),
                rx.button(
                    "Delete",
                    on_click=lambda: ConditionalHandlerState.safe_action("delete", "document"),
                    bg="red.500",
                    color="white"
                )
            ),
            rx.cond(
                ConditionalHandlerState.can_perform_action("admin"),
                rx.button(
                    "Admin Panel",
                    on_click=lambda: ConditionalHandlerState.safe_action("admin", "panel"),
                    bg="purple.500",
                    color="white"
                )
            ),
        ),
        
        # Лог действий
        rx.vstack(
            rx.heading("Action Log", size="sm"),
            rx.scroll_area(
                rx.vstack(
                    rx.foreach(
                        ConditionalHandlerState.action_log,
                        lambda log: rx.text(log, font_size="sm")
                    ),
                    spacing="0.25em"
                ),
                height="150px",
                type_="auto"
            ),
            width="100%"
        ),
        
        spacing="1.5em",
        padding="2em",
        border=rx.color("gray", 4),
        border_radius="0.375rem"
    )
```

## Развертывание

### Подготовка к развертыванию:

```bash
# requirements.txt
reflex==0.4.5
sqlmodel
httpx
aiohttp
python-multipart
uvicorn
gunicorn
psycopg2-binary  # для PostgreSQL
pymysql         # для MySQL
```

```python
# rxconfig.py для production
import reflex as rx

config = rx.Config(
    app_name="my_app",
    # Использование production базы данных
    db_url="postgresql://user:password@localhost/proddb",
    # Отключение отладки в production
    env=rx.Env.PROD,
    # Отключение телеметрии
    telemetry_enabled=False,
    # Настройка CORS для production
    cors_allowed_origins=["https://yourdomain.com"],
    # Настройка сессий
    redis_url="redis://localhost:6379",
)
```

### Docker для развертывания:

```dockerfile
# Dockerfile
FROM python:3.10-slim

# Установка зависимостей
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    git \
    && rm -rf /var/lib/apt/lists/*

# Установка Node.js (требуется для Reflex)
RUN curl -sL https://deb.nodesource.com/setup_18.x | bash - \
    && apt-get install -y nodejs

# Создание пользователя
RUN useradd --create-home --shell /bin/bash app

# Установка приложения
WORKDIR /home/app
COPY --chown=app:app . /home/app/
RUN pip install --no-cache-dir -r requirements.txt

# Установка Reflex
RUN pip install reflex

# Сборка приложения
USER app
RUN reflex init
RUN reflex export --frontend-only

# Открытие порта
EXPOSE 8000

# Запуск приложения
CMD ["reflex", "run", "--env", "prod"]
```

```yaml
# docker-compose.yml для production
version: '3.8'

services:
  web:
    build: .
    ports:
      - "8000:8000"
    environment:
      - REFLEX_DB_URL=postgresql://reflex:password@db:5432/reflexdb
      - REFLEX_REDIS_URL=redis://redis:6379
    depends_on:
      - db
      - redis
    restart: unless-stopped

  db:
    image: postgres:13
    environment:
      POSTGRES_DB: reflexdb
      POSTGRES_USER: reflex
      POSTGRES_PASSWORD: password
    volumes:
      - postgres_data:/var/lib/postgresql/data
    restart: unless-stopped

  redis:
    image: redis:6-alpine
    restart: unless-stopped

  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf
      - ./ssl:/etc/nginx/ssl
    depends_on:
      - web
    restart: unless-stopped

volumes:
  postgres_data:
```

### CI/CD Pipeline:

```yaml
# .github/workflows/deploy.yml
name: Deploy Reflex App

on:
  push:
    branches: [ main ]

jobs:
  deploy:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v3
    
    - name: Setup Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.10'
    
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install reflex
        pip install -r requirements.txt
    
    - name: Run tests
      run: pytest tests/
    
    - name: Build application
      run: |
        reflex init
        reflex export --frontend-only
    
    - name: Deploy to production
      run: |
        # Здесь ваш скрипт деплоя
        # Например, rsync файлов на сервер
        # или вызов API для деплоя
        echo "Deploying to production..."
```

### Production настройки:

```python
# production_config.py
import os
import reflex as rx

class ProductionConfig:
    """Конфигурация для production среды."""
    
    @staticmethod
    def get_config():
        """Получить production конфигурацию."""
        return rx.Config(
            app_name=os.getenv("REFLEX_APP_NAME", "my_app"),
            db_url=os.getenv("DATABASE_URL", "sqlite:///prod.db"),
            env=rx.Env.PROD,
            telemetry_enabled=False,
            cors_allowed_origins=[
                os.getenv("FRONTEND_URL", "https://myapp.com"),
                "https://www.myapp.com"
            ],
            cors_credentials=True,
            cors_max_age=3600,
            compress_response=True,
            admin_dash=rx.AdminDash(
                models=[],  # Определите модели для админ панели
                view_class=None
            ),
            redis_url=os.getenv("REDIS_URL"),
            upload_path=os.getenv("UPLOAD_PATH", "/tmp/uploads"),
            frontend_packages=[
                # Дополнительные npm пакеты для frontend
            ]
        )

# gunicorn_config.py
bind = "0.0.0.0:8000"
workers = 4
worker_class = "uvicorn.workers.UvicornWorker"
timeout = 120
keepalive = 5
max_requests = 1000
max_requests_jitter = 100
preload_app = True
```

## Лучшие практики

### 1. Структура проекта:

```
my_reflex_app/
├── .github/
│   └── workflows/
│       └── deploy.yml
├── .vscode/
│   └── settings.json
├── assets/
│   ├── favicon.ico
│   ├── logo.svg
│   └── images/
├── my_reflex_app/
│   ├── __init__.py
│   ├── app.py                 # Главный файл приложения
│   ├── config.py             # Конфигурация приложения
│   ├── styles.py            # Глобальные стили
│   ├── components/          # Пользовательские компоненты
│   │   ├── __init__.py
│   │   ├── navigation.py
│   │   ├── cards.py
│   │   └── forms.py
│   ├── states/              # Файлы состояний
│   │   ├── __init__.py
│   │   ├── base.py         # Базовое состояние
│   │   ├── auth.py         # Состояние аутентификации
│   │   ├── user.py         # Состояние пользователя
│   │   └── dashboard.py    # Состояние дашборда
│   ├── pages/              # Файлы страниц
│   │   ├── __init__.py
│   │   ├── home.py
│   │   ├── dashboard.py
│   │   ├── profile.py
│   │   └── settings.py
│   └── utils/              # Утилиты
│       ├── __init__.py
│       ├── validators.py
│       ├── helpers.py
│       └── constants.py
├── tests/                  # Тесты
│   ├── __init__.py
│   ├── test_states.py
│   └── test_components.py
├── docs/                   # Документация
├── migrations/            # Миграции базы данных
├── scripts/              # Вспомогательные скрипты
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── rxconfig.py
├── pyproject.toml
└── README.md
```

### 2. Организация состояний:

```python
# my_reflex_app/states/base.py
import reflex as rx

class BaseState(rx.State):
    """Базовое состояние для всех других состояний."""
    # Глобальные переменные
    loading: bool = False
    error_message: str = ""
    success_message: str = ""
    
    def show_loading(self):
        """Показать индикатор загрузки."""
        self.loading = True
        self.error_message = ""
    
    def hide_loading(self):
        """Скрыть индикатор загрузки."""
        self.loading = False
    
    def set_error(self, message: str):
        """Установить сообщение об ошибке."""
        self.error_message = message
        self.hide_loading()
    
    def set_success(self, message: str):
        """Установить сообщение об успехе."""
        self.success_message = message
        self.hide_loading()

# my_reflex_app/states/auth.py
from .base import BaseState

class AuthState(BaseState):
    """Состояние аутентификации."""
    user_id: str = ""
    username: str = ""
    is_authenticated: bool = False
    redirect_to: str = "/"
    
    def login(self, username: str, password: str):
        """Процесс входа в систему."""
        self.show_loading()
        try:
            # Здесь логика аутентификации
            # Проверка учетных данных
            if self.validate_credentials(username, password):
                self.user_id = self.get_user_id(username)
                self.username = username
                self.is_authenticated = True
                self.success_message = "Successfully logged in!"
                
                # Редирект если был указан
                if self.redirect_to and self.redirect_to != "/":
                    return rx.redirect(self.redirect_to)
            else:
                self.set_error("Invalid username or password")
        except Exception as e:
            self.set_error(f"Login failed: {str(e)}")
        finally:
            self.hide_loading()
    
    def logout(self):
        """Процесс выхода из системы."""
        self.user_id = ""
        self.username = ""
        self.is_authenticated = False
        self.success_message = "Successfully logged out"
        return rx.redirect("/")
    
    def validate_credentials(self, username: str, password: str) -> bool:
        """Валидация учетных данных (заглушка)."""
        # Реализуйте вашу логику проверки
        return username == "admin" and password == "password"
    
    def get_user_id(self, username: str) -> str:
        """Получить ID пользователя (заглушка)."""
        # Реализуйте вашу логику получения ID
        return f"user_{hash(username)}"
```

### 3. Компоненты с хорошей архитектурой:

```python
# my_reflex_app/components/cards.py
import reflex as rx
from ..styles import *

def data_card(
    title: str,
    content: rx.Component,
    footer: rx.Component = None,
    variant: str = "elevated"
) -> rx.Component:
    """Универсальная карточка данных."""
    base_style = {
        "bg": bg_color if variant == "filled" else "transparent",
        "border": border if variant == "outlined" else "none",
        "border_radius": border_radius,
        "padding": "1.5rem",
        "box_shadow": "0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06)" if variant == "elevated" else "none",
    }
    
    card_parts = [
        rx.heading(title, size="md", margin_bottom="1rem") if title else None,
        content,
        rx.divider(margin_y="1rem") if footer else None,
        footer if footer else None
    ]
    
    # Убираем None значения
    card_parts = [part for part in card_parts if part is not None]
    
    return rx.card(
        *card_parts,
        style=base_style
    )

def stat_card(
    title: str,
    value: str,
    change: str = "",
    icon: str = "",
    trend: str = "up"  # "up", "down", or "neutral"
) -> rx.Component:
    """Карточка статистики."""
    trend_color = "green" if trend == "up" else "red" if trend == "down" else "gray"
    
    return data_card(
        title=title,
        content=rx.vstack(
            rx.hstack(
                rx.icon(icon, size=24) if icon else None,
                rx.text(value, font_size="2rem", font_weight="bold"),
                align="center"
            ),
            rx.hstack(
                rx.text(change, color=trend_color),
                rx.icon("arrow-up" if trend == "up" else "arrow-down" if trend == "down" else "minus", 
                       color=trend_color, size=16) if change else None,
                align="center"
            ) if change else None,
            spacing="0.5rem",
            align="start"
        )
    )

# my_reflex_app/components/forms.py
def input_field(
    label: str,
    placeholder: str,
    value,
    on_change,
    error_text: str = "",
    required: bool = False,
    type_: str = "text"
) -> rx.Component:
    """Стандартизированное поле ввода."""
    return rx.vstack(
        rx.hstack(
            rx.text(label, font_weight="medium"),
            rx.text("*", color="red.500") if required else None,
            spacing="0.25rem"
        ) if label else None,
        rx.input(
            placeholder=placeholder,
            value=value,
            on_change=on_change,
            type_=type_,
            border=border,
            border_radius=border_radius,
            padding="0.75rem",
            style={
                "focus": {
                    "border_color": accent_color,
                    "box_shadow": f"0 0 0 3px {rx.color('accent', 5)}",
                }
            }
        ),
        rx.text(error_text, color="red.500", font_size="0.875rem") if error_text else None,
        align="start",
        spacing="0.5rem",
        width="100%"
    )

def form_container(
    *children,
    title: str = "",
    subtitle: str = "",
    submit_handler=None,
    submit_label: str = "Submit"
) -> rx.Component:
    """Контейнер формы."""
    return rx.card(
        rx.vstack(
            rx.vstack(
                rx.heading(title, size="lg") if title else None,
                rx.text(subtitle, color="gray.600") if subtitle else None,
                spacing="0.25rem",
                align="start",
                width="100%"
            ) if title or subtitle else None,
            
            *children,
            
            rx.button(
                submit_label,
                on_click=submit_handler,
                bg=accent_color,
                color="white",
                width="100%",
                margin_top="1.5rem"
            ) if submit_handler else None,
            
            spacing="1.5rem",
            width="100%"
        ),
        padding="2rem",
        width="100%",
        max_width="24rem"
    )
```

### 4. Тестирование:

```python
# tests/test_states.py
import pytest
import reflex as rx
from my_reflex_app.states.auth import AuthState

def test_initial_auth_state():
    """Тест начального состояния аутентификации."""
    state = AuthState()
    assert state.user_id == ""
    assert state.username == ""
    assert not state.is_authenticated
    assert state.error_message == ""

@pytest.mark.asyncio
async def test_login_success():
    """Тест успешного входа."""
    state = AuthState()
    
    # Устанавливаем мок-методы
    original_validate = state.validate_credentials
    original_get_user_id = state.get_user_id
    
    state.validate_credentials = lambda u, p: True
    state.get_user_id = lambda u: "mock_user_id"
    
    await state.login("testuser", "password")
    
    assert state.is_authenticated
    assert state.username == "testuser"
    assert state.user_id == "mock_user_id"
    assert "Successfully logged in" in state.success_message
    
    # Восстанавливаем оригинальные методы
    state.validate_credentials = original_validate
    state.get_user_id = original_get_user_id

def test_logout():
    """Тест выхода из системы."""
    state = AuthState()
    state.user_id = "test_user"
    state.username = "testuser"
    state.is_authenticated = True
    
    result = state.logout()
    
    assert not state.is_authenticated
    assert state.user_id == ""
    assert state.username == ""
    assert result == rx.redirect("/")

# tests/test_components.py
import reflex as rx
from my_reflex_app.components.cards import stat_card

def test_stat_card_render():
    """Тест рендеринга карточки статистики."""
    card = stat_card(
        title="Sales",
        value="$12,345",
        change="+12%",
        icon="trending-up",
        trend="up"
    )
    
    # Проверяем, что компонент создается без ошибок
    assert card is not None
```

> Этот мануал охватывает основные аспекты Reflex Framework. Для более глубокого изучения рекомендуется практиковаться на реальных примерах и изучать официальную документацию.