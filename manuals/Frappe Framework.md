# 🏗️ Полный мануал по Frappe Framework: От основ до продвинутых практик

## 📋 Содержание

1. [Введение в Frappe Framework](#введение-в-frappe-framework)
2. [Установка и настройка](#установка-и-настройка)
3. [Архитектура Frappe](#архитектура-frappe)
4. [Документы и DocTypes](#документы-и-doctypes)
5. [Frontend разработка](#frontend-разработка)
6. [Backend разработка](#backend-разработка)
7. [API и интеграции](#api-и-интеграции)
8. [Безопасность](#безопасность)
9. [Тестирование](#тестирование)
10. [Развертывание](#развертывание)
11. [Лучшие практики](#лучшие-практики)

## Введение в Frappe Framework

**Frappe Framework** — это современный full-stack фреймворк с открытым исходным кодом, написанный на Python и JavaScript. Он используется для быстрой разработки веб-приложений и ERP-систем, таких как ERPNext.

### Особенности Frappe:

✅ **Full-stack**: Python (backend) + JavaScript (frontend)
✅ **No-code/Low-code**: Встроенная система создания документов
✅ **Многоуровневая архитектура**: Tenant isolation
✅ **Мощная ORM**: Автоматическое создание CRUD операций
✅ **Встроенные функции**: Авторизация, аудит, кэширование
✅ **WebSocket поддержка**: Real-time обновления
✅ **Международализация**: Поддержка нескольких языков

### Когда использовать Frappe?

**Подходит для:**
- ERP-систем
- CRM-приложений
- Бухгалтерских систем
- Систем управления проектами
- Бизнес-приложений
- SAAS-решений

**Не всегда подходит для:**
- Простых лендингов
- Статических сайтов
- Высоконагруженных систем без админ-панели
- Проектов с минимальными бизнес-логиками

## Установка и настройка

### Установка через Bench:

```bash
# Установка Bench (управление Frappe инстансами)
pip install frappe-bench

# Создание нового Frappe инстанса
bench init ~/frappe-bench --frappe-branch version-14

# Переход в директорию
cd ~/frappe-bench

# Создание нового сайта
bench new-site mysite.local

# Установка приложения
bench get-app erpnext
bench --site mysite.local install-app erpnext

# Запуск сервера
bench start
```

### Установка в Docker:

```yaml
# docker-compose.yml
version: '3.7'

services:
  mariadb:
    image: mariadb:10.3
    environment:
      MYSQL_ROOT_PASSWORD: 123
      MYSQL_USER: frappe
      MYSQL_PASSWORD: 123
      MYSQL_DATABASE: frappe
    volumes:
      - mariadb-data:/var/lib/mysql

  redis-cache:
    image: redis:latest

  redis-queue:
    image: redis:latest

  redis-socketio:
    image: redis:latest

  frappe:
    image: frappe/bench:latest
    command: >
      sh -c "bench new-site site1.local --mariadb-root-password 123 --admin-password admin
      && bench --site site1.local install-app erpnext
      && bench start"
    depends_on:
      - mariadb
      - redis-cache
      - redis-queue
      - redis-socketio
    ports:
      - "8000:8000"
    volumes:
      - ./sites:/home/frappe/frappe-bench/sites

volumes:
  mariadb-data:
```

### Установка зависимостей:

```bash
# Установка системных зависимостей (Ubuntu/Debian)
sudo apt-get update
sudo apt-get install -y python3-dev python3-setuptools python3-pip
sudo apt-get install -y mariadb-client mariadb-server
sudo apt-get install -y redis-server
sudo apt-get install -y nodejs npm
sudo apt-get install -y yarn

# Установка Python зависимости
pip3 install frappe-bench

# Установка Node.js зависимости
npm install -g yarn
```

## Архитектура Frappe

### Структура приложения:

```
my_app/
├── __init__.py
├── hooks.py                 # Конфигурация приложения
├── modules.txt             # Названия модулей
├── patches.txt            # Миграции
├── templates/             # HTML шаблоны
│   ├── pages/            # Page шаблоны
│   └── includes/         # Reusable компоненты
├── www/                  # Public страницы
├── public/               # Статические файлы
│   ├── css/
│   ├── js/
│   └── images/
├── config/               # Конфигурация маршрутов
│   └── desktop.py       # Desk icons
├── docs/                # Документация
├── fixtures/            # Фикстуры данных
├── translations/        # Переводы
└── my_app/
    ├── __init__.py
    ├── api.py           # API методы
    ├── hooks.py        # Hooks для этого приложения
    ├── modules/        # Модули приложения
    │   ├── doc_types/  # DocType определения
    │   ├── pages/      # Page определения
    │   └── reports/    # Report определения
    └── utils/          # Утилиты
```

### Основные компоненты:

#### 1. DocType (Document Type):
```python
# my_app/my_app/doc_types/todo/todo.json
{
  "doctype": "DocType",
  "name": "ToDo",
  "module": "My App",
  "custom": 0,
  "fields": [
    {
      "fieldname": "description",
      "fieldtype": "Text Editor",
      "label": "Description",
      "reqd": 1
    },
    {
      "fieldname": "priority",
      "fieldtype": "Select",
      "label": "Priority",
      "options": "Low\nMedium\nHigh",
      "default": "Medium"
    },
    {
      "fieldname": "due_date",
      "fieldtype": "Date",
      "label": "Due Date"
    },
    {
      "fieldname": "status",
      "fieldtype": "Select",
      "label": "Status",
      "options": "Open\nCompleted",
      "default": "Open"
    }
  ],
  "permissions": [
    {
      "role": "System Manager",
      "permlevel": 0,
      "read": 1,
      "write": 1,
      "create": 1,
      "delete": 1,
      "submit": 0,
      "cancel": 0,
      "amend": 0
    }
  ]
}
```

#### 2. Hooks:
```python
# hooks.py
app_name = "my_app"
app_title = "My App"
app_publisher = "My Publisher"
app_version = "0.0.1"

# Сайт
website_context = {
    "favicon": "/assets/my_app/images/favicon.ico",
    "splash_image": "/assets/my_app/images/splash.png"
}

# Запланированные задачи
scheduler_events = {
    "daily": [
        "my_app.tasks.daily_backup"
    ],
    "hourly": [
        "my_app.tasks.hourly_sync"
    ]
}

# API точки
override_whitelisted_methods = {
    "frappe.desk.form.save.handler": "my_app.api.custom_save"
}

# DocType события
doc_events = {
    "ToDo": {
        "after_insert": "my_app.handlers.todo_after_insert",
        "validate": "my_app.handlers.todo_validate"
    }
}
```

## Документы и DocTypes

### Создание DocType программно:

```python
# my_app/my_app/setup.py
import frappe

def create_custom_doctypes():
    """Создание кастомных DocTypes"""
    
    # Создание DocType через код
    if not frappe.db.exists('DocType', 'Custom Customer'):
        doc = frappe.get_doc({
            'doctype': 'DocType',
            'name': 'Custom Customer',
            'module': 'My App',
            'custom': 0,
            'autoname': 'field:customer_name',
            'fields': [
                {
                    'fieldname': 'customer_name',
                    'fieldtype': 'Data',
                    'label': 'Customer Name',
                    'reqd': 1
                },
                {
                    'fieldname': 'email',
                    'fieldtype': 'Data',
                    'label': 'Email',
                    'options': 'Email'
                },
                {
                    'fieldname': 'phone',
                    'fieldtype': 'Data',
                    'label': 'Phone',
                    'options': 'Phone'
                },
                {
                    'fieldname': 'customer_group',
                    'fieldtype': 'Link',
                    'label': 'Customer Group',
                    'options': 'Customer Group'
                }
            ],
            'permissions': [
                {
                    'role': 'System Manager',
                    'read': 1,
                    'write': 1,
                    'create': 1,
                    'delete': 1
                }
            ]
        })
        doc.insert()
        frappe.db.commit()

def setup_data():
    """Настройка начальных данных"""
    
    # Создание Customer Groups
    customer_groups = ['Individual', 'Corporate', 'Government']
    
    for group in customer_groups:
        if not frappe.db.exists('Customer Group', group):
            frappe.get_doc({
                'doctype': 'Customer Group',
                'customer_group_name': group
            }).insert()

# Запуск при установке
def after_install():
    create_custom_doctypes()
    setup_data()
```

### Работа с документами:

```python
# my_app/my_app/api.py
import frappe
from frappe import _
from frappe.model.document import Document

@frappe.whitelist()
def create_todo(description, priority="Medium", due_date=None):
    """Создание ToDo"""
    todo = frappe.new_doc("ToDo")
    todo.description = description
    todo.priority = priority
    if due_date:
        todo.due_date = due_date
    todo.insert()
    frappe.db.commit()
    return todo

@frappe.whitelist()
def get_todos(filters=None):
    """Получение списка ToDo"""
    todo_list = frappe.get_all(
        "ToDo",
        filters=filters or {},
        fields=["name", "description", "priority", "status", "due_date"],
        order_by="creation desc"
    )
    return todo_list

@frappe.whitelist()
def update_todo_status(todo_name, status):
    """Обновление статуса ToDo"""
    todo = frappe.get_doc("ToDo", todo_name)
    todo.status = status
    todo.save()
    return todo

# Кастомный DocType класс
class CustomCustomer(Document):
    def validate(self):
        """Валидация при сохранении"""
        if self.email:
            # Проверка уникальности email
            existing = frappe.db.exists(
                "Custom Customer", 
                {"email": self.email, "name": ["!=", self.name]}
            )
            if existing:
                frappe.throw(_("Email already exists"))
    
    def before_save(self):
        """Перед сохранением"""
        # Автоматическое заполнение полей
        if not self.customer_group:
            self.customer_group = "Individual"
    
    def after_insert(self):
        """После создания"""
        # Создание связанной записи
        frappe.log("New customer created: {}".format(self.customer_name))

@frappe.whitelist()
def get_customer_summary(customer_name):
    """Получение сводки по клиенту"""
    customer = frappe.get_doc("Custom Customer", customer_name)
    
    # Получение связанных записей
    orders = frappe.get_all(
        "Sales Order",
        filters={"customer": customer_name},
        fields=["name", "grand_total", "status", "transaction_date"]
    )
    
    total_orders = len(orders)
    total_amount = sum(order.grand_total for order in orders)
    
    return {
        "customer": customer.as_dict(),
        "summary": {
            "total_orders": total_orders,
            "total_amount": total_amount,
            "recent_orders": orders[:5]  # последние 5 заказов
        }
    }
```

### Кастомные методы для DocTypes:

```javascript
// my_app/public/js/todo.js
frappe.ui.form.on('ToDo', {
    refresh: function(frm) {
        // Добавление кнопки при определенных условиях
        if (frm.doc.status === 'Open') {
            frm.add_custom_button(__('Mark Completed'), function() {
                frappe.call({
                    method: 'my_app.api.update_todo_status',
                    args: {
                        todo_name: frm.doc.name,
                        status: 'Completed'
                    },
                    callback: function(r) {
                        if (!r.exc) {
                            frm.reload_doc();
                        }
                    }
                });
            });
        }
        
        // Условное скрытие полей
        if (frm.doc.priority === 'Low') {
            frm.set_df_property('due_date', 'hidden', 1);
        } else {
            frm.set_df_property('due_date', 'hidden', 0);
        }
    },
    
    priority: function(frm) {
        // Изменение цвета в зависимости от приоритета
        let color = {
            'Low': 'green',
            'Medium': 'orange',
            'High': 'red'
        }[frm.doc.priority] || 'gray';
        
        $(frm.fields_dict.description.wrapper).css('border-left', `3px solid ${color}`);
    },
    
    due_date: function(frm) {
        // Проверка даты
        if (frm.doc.due_date && frm.doc.due_date < frappe.datetime.get_today()) {
            frappe.show_alert({
                message: __('Due date is in the past'),
                indicator: 'orange'
            });
        }
    }
});
```

## Frontend разработка

### Page разработка:

```python
# my_app/www/custom_page.py
import frappe
from frappe import _

def get_context(context):
    """Подготовка данных для страницы"""
    context.no_cache = 1
    context.todos = frappe.get_all(
        "ToDo",
        filters={"status": "Open"},
        fields=["name", "description", "priority", "due_date"],
        order_by="creation desc"
    )
    
    context.customers = frappe.get_all(
        "Custom Customer",
        fields=["name", "customer_name", "email"],
        order_by="modified desc"
    )
    
    # Добавление JS/CSS
    context.styles = ['/assets/my_app/css/custom.css']
    context.scripts = ['/assets/my_app/js/custom.js']
    
    return context
```

```html
<!-- my_app/templates/pages/custom_page.html -->
{% extends "templates/web.html" %}

{% block page_content %}
<div class="container">
    <h1>Custom Dashboard</h1>
    
    <div class="row">
        <div class="col-md-6">
            <h3>Open Tasks</h3>
            <div class="list-group">
                {% for todo in todos %}
                <div class="list-group-item">
                    <div class="d-flex justify-content-between">
                        <span class="priority-{{ todo.priority.lower() }}">
                            {{ todo.description }}
                        </span>
                        <small>{{ todo.due_date or "No deadline" }}</small>
                    </div>
                </div>
                {% endfor %}
            </div>
        </div>
        
        <div class="col-md-6">
            <h3>Recent Customers</h3>
            <table class="table table-striped">
                <thead>
                    <tr>
                        <th>Name</th>
                        <th>Email</th>
                    </tr>
                </thead>
                <tbody>
                    {% for customer in customers %}
                    <tr>
                        <td>{{ customer.customer_name }}</td>
                        <td>{{ customer.email }}</td>
                    </tr>
                    {% endfor %}
                </tbody>
            </table>
        </div>
    </div>
</div>
{% endblock %}
```

### Desk Page (Admin Interface):

```javascript
// my_app/public/js/desk_pages/custom_dashboard.js
frappe.pages['custom-dashboard'].on_page_load = function(wrapper) {
    var page = frappe.ui.make_app_page({
        parent: wrapper,
        title: 'Custom Dashboard',
        single_column: true
    });
    
    // Добавление элементов управления
    page.add_inner_button(__('Refresh'), function() {
        refresh_dashboard();
    });
    
    page.add_inner_button(__('Export Data'), function() {
        export_data();
    });
    
    // Рендер контента
    render_dashboard(page);
};

function render_dashboard(page) {
    $(page.body).empty();
    
    // Создание карточек
    var cards_html = `
        <div class="dashboard-cards">
            <div class="card">
                <div class="card-body">
                    <h5 class="card-title">Open Tasks</h5>
                    <p class="card-text" id="open-tasks-count">0</p>
                </div>
            </div>
            <div class="card">
                <div class="card-body">
                    <h5 class="card-title">Customers</h5>
                    <p class="card-text" id="customers-count">0</p>
                </div>
            </div>
            <div class="card">
                <div class="card-body">
                    <h5 class="card-title">Revenue</h5>
                    <p class="card-text" id="revenue-amount">$0</p>
                </div>
            </div>
        </div>
    `;
    
    $(page.body).append(cards_html);
    
    // Загрузка данных
    load_dashboard_data();
}

function load_dashboard_data() {
    frappe.call({
        method: 'my_app.api.get_dashboard_data',
        callback: function(r) {
            if (!r.exc) {
                $('#open-tasks-count').text(r.message.open_tasks);
                $('#customers-count').text(r.message.total_customers);
                $('#revenue-amount').text('$' + r.message.monthly_revenue);
            }
        }
    });
}

function refresh_dashboard() {
    load_dashboard_data();
    frappe.show_alert({
        message: 'Dashboard refreshed',
        indicator: 'green'
    });
}

function export_data() {
    frappe.call({
        method: 'my_app.api.export_data',
        args: {
            doctype: 'ToDo'
        },
        callback: function(r) {
            if (!r.exc) {
                frappe.show_alert({
                    message: 'Export completed',
                    indicator: 'green'
                });
            }
        }
    });
}
```

### Кастомные Formatters:

```javascript
// my_app/public/js/formatters.js
frappe.provide('my_app.formatters');

// Кастомный formatter для приоритета
my_app.formatters.priority = function(value, doc, field, options) {
    if (!value) return '';
    
    var colors = {
        'High': 'red',
        'Medium': 'orange',
        'Low': 'green'
    };
    
    return `<span class="indicator-pill ${colors[value] || 'gray'}">${value}</span>`;
};

// Кастомный formatter для статуса
my_app.formatters.status = function(value, doc, field, options) {
    if (!value) return '';
    
    var colors = {
        'Open': 'orange',
        'Completed': 'green',
        'Cancelled': 'red',
        'In Progress': 'blue'
    };
    
    return `<span class="indicator-pill ${colors[value] || 'gray'}">${value}</span>`;
};

// Регистрация formatter'ов
frappe.form.link_formatters['ToDo'] = function(value, doc) {
    if (doc && doc.priority) {
        return my_app.formatters.priority(doc.priority) + ' ' + value;
    }
    return value;
};
```

## Backend разработка

### Кастомные методы и API:

```python
# my_app/my_app/api.py
import frappe
from frappe import _
import json
from frappe.utils.response import json_handler
from frappe.auth import HTTPRequest

@frappe.whitelist()
def get_sales_summary(start_date=None, end_date=None):
    """Получение сводки по продажам"""
    from datetime import datetime, timedelta
    
    if not start_date:
        start_date = frappe.utils.add_days(frappe.utils.today(), -30)
    if not end_date:
        end_date = frappe.utils.today()
    
    # Запрос к базе данных
    sales_data = frappe.db.sql("""
        SELECT 
            DATE(creation) as date,
            COUNT(*) as count,
            SUM(grand_total) as total
        FROM `tabSales Order`
        WHERE creation BETWEEN %(start_date)s AND %(end_date)s
        GROUP BY DATE(creation)
        ORDER BY DATE(creation)
    """, {
        'start_date': start_date,
        'end_date': end_date
    }, as_dict=True)
    
    # Подсчет общих показателей
    total_orders = sum(row.count for row in sales_data)
    total_revenue = sum(row.total for row in sales_data)
    
    return {
        'sales_data': sales_data,
        'summary': {
            'total_orders': total_orders,
            'total_revenue': total_revenue,
            'average_order_value': total_revenue / total_orders if total_orders > 0 else 0
        }
    }

@frappe.whitelist(allow_guest=True)
def submit_feedback(name, email, message, rating=5):
    """Сохранение отзыва"""
    if not all([name, email, message]):
        frappe.throw(_("Name, Email and Message are required"))
    
    if not frappe.utils.validate_email_address(email):
        frappe.throw(_("Invalid email address"))
    
    feedback_doc = frappe.get_doc({
        'doctype': 'Feedback',
        'name': name,
        'email': email,
        'message': message,
        'rating': min(5, max(1, int(rating)))  # Ограничение от 1 до 5
    })
    
    feedback_doc.insert(ignore_permissions=True)
    frappe.db.commit()
    
    return {
        'status': 'success',
        'message': _('Thank you for your feedback!')
    }

@frappe.whitelist()
def bulk_update_todos(todo_list, field, value):
    """Массовое обновление ToDo"""
    updated_count = 0
    
    for todo_name in todo_list:
        try:
            todo = frappe.get_doc("ToDo", todo_name)
            setattr(todo, field, value)
            todo.save()
            updated_count += 1
        except Exception as e:
            frappe.log_error(f"Error updating ToDo {todo_name}: {str(e)}")
    
    frappe.db.commit()
    return {
        'updated': updated_count,
        'failed': len(todo_list) - updated_count
    }

def send_daily_reminders():
    """Отправка ежедневных напоминаний"""
    from datetime import datetime, timedelta
    
    tomorrow = frappe.utils.add_days(frappe.utils.today(), 1)
    
    todos_due_tomorrow = frappe.get_all(
        "ToDo",
        filters={
            "due_date": tomorrow,
            "status": "Open"
        },
        fields=["name", "description", "allocated_to"]
    )
    
    for todo in todos_due_tomorrow:
        if todo.allocated_to:
            frappe.sendmail(
                recipients=[todo.allocated_to],
                subject=_("Tomorrow's Task Reminder"),
                message=_("Task '{}' is due tomorrow: {}").format(
                    todo.name, todo.description
                ),
                delayed=False
            )

def cleanup_old_logs():
    """Очистка старых логов"""
    from datetime import datetime, timedelta
    
    # Удаление логов старше 30 дней
    cutoff_date = frappe.utils.add_days(frappe.utils.today(), -30)
    
    old_logs = frappe.get_all(
        "Custom Log",
        filters={"creation": ["<", cutoff_date]},
        pluck="name"
    )
    
    for log_name in old_logs:
        frappe.delete_doc("Custom Log", log_name, ignore_permissions=True)
    
    frappe.db.commit()
```

### Кастомные Reports:

```python
# my_app/my_app/reports/todo_summary/todo_summary.py
import frappe
from frappe import _

def execute(filters=None):
    columns = get_columns()
    data = get_data(filters)
    chart = get_chart(data)
    report_summary = get_report_summary(data)
    
    return columns, data, chart, None, report_summary

def get_columns():
    return [
        {
            "fieldname": "priority",
            "label": _("Priority"),
            "fieldtype": "Data",
            "width": 120
        },
        {
            "fieldname": "count",
            "label": _("Count"),
            "fieldtype": "Int",
            "width": 100
        },
        {
            "fieldname": "completed",
            "label": _("Completed"),
            "fieldtype": "Int",
            "width": 120
        },
        {
            "fieldname": "open",
            "label": _("Open"),
            "fieldtype": "Int",
            "width": 100
        }
    ]

def get_data(filters):
    conditions = []
    if filters.get("status"):
        conditions.append(f"status = '{filters.get('status')}'")
    
    condition_str = " AND ".join(conditions) if conditions else "1=1"
    
    data = frappe.db.sql(f"""
        SELECT 
            priority,
            COUNT(*) as count,
            SUM(CASE WHEN status = 'Completed' THEN 1 ELSE 0 END) as completed,
            SUM(CASE WHEN status = 'Open' THEN 1 ELSE 0 END) as open
        FROM `tabToDo`
        WHERE {condition_str}
        GROUP BY priority
    """, as_dict=True)
    
    return data

def get_chart(data):
    if not data:
        return None
    
    priorities = [row.priority for row in data]
    counts = [row.count for row in data]
    
    return {
        "data": {
            "labels": priorities,
            "datasets": [
                {
                    "name": "Tasks",
                    "values": counts
                }
            ]
        },
        "type": "bar"
    }

def get_report_summary(data):
    if not data:
        return []
    
    total_tasks = sum(row.count for row in data)
    completed_tasks = sum(row.completed for row in data)
    open_tasks = sum(row.open for row in data)
    
    return [
        {
            "value": total_tasks,
            "indicator": "Blue",
            "label": _("Total Tasks"),
            "datatype": "Int"
        },
        {
            "value": completed_tasks,
            "indicator": "Green",
            "label": _("Completed"),
            "datatype": "Int"
        },
        {
            "value": open_tasks,
            "indicator": "Red",
            "label": _("Open"),
            "datatype": "Int"
        }
    ]
```

## API и интеграции

### REST API:

```python
# my_app/my_app/api_integration.py
import frappe
import requests
import json
from frappe import _
from frappe.utils.password import get_decrypted_password

class ExternalAPIClient:
    def __init__(self, base_url, api_key=None):
        self.base_url = base_url.rstrip('/')
        self.api_key = api_key or get_decrypted_password(
            'System Settings', 'System Settings', 'external_api_key'
        )
        self.session = requests.Session()
        
        if self.api_key:
            self.session.headers.update({
                'Authorization': f'Bearer {self.api_key}',
                'Content-Type': 'application/json'
            })
    
    def get(self, endpoint, params=None):
        """GET запрос"""
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        response = self.session.get(url, params=params)
        return self._handle_response(response)
    
    def post(self, endpoint, data=None):
        """POST запрос"""
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        response = self.session.post(url, json=data)
        return self._handle_response(response)
    
    def put(self, endpoint, data=None):
        """PUT запрос"""
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        response = self.session.put(url, json=data)
        return self._handle_response(response)
    
    def delete(self, endpoint):
        """DELETE запрос"""
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        response = self.session.delete(url)
        return self._handle_response(response)
    
    def _handle_response(self, response):
        """Обработка ответа"""
        if response.status_code in [200, 201]:
            try:
                return response.json()
            except json.JSONDecodeError:
                return {'message': response.text}
        else:
            frappe.log_error(f"API Error: {response.status_code} - {response.text}")
            frappe.throw(_(f"External API Error: {response.status_code}"))

@frappe.whitelist()
def sync_customers_with_external_system():
    """Синхронизация клиентов с внешней системой"""
    client = ExternalAPIClient('https://api.external-system.com')
    
    try:
        # Получение клиентов из внешней системы
        external_customers = client.get('/customers')
        
        synced_count = 0
        error_count = 0
        
        for ext_customer in external_customers:
            try:
                # Проверка существования клиента
                if frappe.db.exists('Custom Customer', ext_customer.get('external_id')):
                    # Обновление существующего
                    customer = frappe.get_doc('Custom Customer', ext_customer.get('external_id'))
                else:
                    # Создание нового
                    customer = frappe.new_doc('Custom Customer')
                    customer.name = ext_customer.get('external_id')
                
                # Обновление данных
                customer.customer_name = ext_customer.get('name')
                customer.email = ext_customer.get('email')
                customer.phone = ext_customer.get('phone')
                customer.external_sync = 1  # Пометка синхронизации
                
                customer.save()
                synced_count += 1
                
            except Exception as e:
                frappe.log_error(f"Sync error for customer {ext_customer.get('id')}: {str(e)}")
                error_count += 1
        
        frappe.db.commit()
        
        return {
            'status': 'success',
            'synced': synced_count,
            'errors': error_count,
            'message': f'Sync completed: {synced_count} synced, {error_count} errors'
        }
        
    except Exception as e:
        frappe.log_error(f"Sync failed: {str(e)}")
        frappe.throw(_(f"Sync failed: {str(e)}"))

@frappe.whitelist()
def webhook_handler():
    """Обработчик вебхуков"""
    import json
    
    # Получение данных вебхука
    data = frappe.request.get_json()
    event_type = frappe.request.headers.get('X-Event-Type')
    
    if event_type == 'customer.created':
        handle_customer_created(data)
    elif event_type == 'order.updated':
        handle_order_updated(data)
    elif event_type == 'payment.completed':
        handle_payment_completed(data)
    
    return {'status': 'received'}

def handle_customer_created(data):
    """Обработка события создания клиента"""
    customer_data = data.get('customer', {})
    
    if not frappe.db.exists('Custom Customer', customer_data.get('id')):
        customer = frappe.new_doc('Custom Customer')
        customer.name = customer_data.get('id')
        customer.customer_name = customer_data.get('name')
        customer.email = customer_data.get('email')
        customer.phone = customer_data.get('phone')
        customer.insert()

def handle_order_updated(data):
    """Обработка события обновления заказа"""
    order_data = data.get('order', {})
    # Логика обновления заказа...

def handle_payment_completed(data):
    """Обработка события завершения платежа"""
    payment_data = data.get('payment', {})
    # Логика обработки платежа...
```

### WebSocket и Real-time:

```javascript
// my_app/public/js/realtime.js
frappe.provide('my_app.realtime');

my_app.realtime.SocketManager = class {
    constructor() {
        this.socket = null;
        this.connected = false;
        this.listeners = {};
        this.initialize();
    }
    
    initialize() {
        // Использование Frappe Socket.IO
        if (typeof io !== 'undefined') {
            this.connect();
        }
    }
    
    connect() {
        this.socket = io(frappe.socketio_port, {
            transports: ['websocket']
        });
        
        this.socket.on('connect', () => {
            this.connected = true;
            this.emit('user_connected', {
                user: frappe.session.user,
                sid: frappe.get_cookie('sid')
            });
        });
        
        this.socket.on('disconnect', () => {
            this.connected = false;
        });
        
        // Слушатель для кастомных событий
        this.socket.on('todo_update', (data) => {
            this.handle_todo_update(data);
        });
        
        this.socket.on('notification', (data) => {
            this.handle_notification(data);
        });
    }
    
    handle_todo_update(data) {
        // Обновление ToDo в реальном времени
        if (data.action === 'created' && data.assigned_to === frappe.session.user) {
            frappe.show_alert({
                message: `New task assigned: ${data.description}`,
                indicator: 'info'
            });
        }
        
        // Обновление списка задач если пользователь на соответствующей странице
        if (cur_frm && cur_frm.doc.doctype === 'ToDo') {
            cur_frm.refresh();
        }
    }
    
    handle_notification(data) {
        // Показ уведомления
        frappe.show_alert({
            message: data.message,
            indicator: data.indicator || 'blue'
        });
    }
    
    emit(event, data) {
        if (this.socket && this.connected) {
            this.socket.emit(event, data);
        }
    }
    
    on(event, callback) {
        if (this.socket) {
            this.socket.on(event, callback);
        }
    }
    
    off(event) {
        if (this.socket) {
            this.socket.off(event);
        }
    }
};

// Инициализация
$(document).ready(function() {
    my_app.realtime.socket_manager = new my_app.realtime.SocketManager();
});

// Пример использования в форме
frappe.ui.form.on('ToDo', {
    setup: function(frm) {
        // Подписка на обновления
        my_app.realtime.socket_manager.on('todo_assigned', function(data) {
            if (data.todo_name === frm.doc.name && data.assigned_to !== frappe.session.user) {
                frm.refresh();
                frappe.show_alert('Task reassigned');
            }
        });
    }
});
```

## Безопасность

### Права доступа:

```python
# my_app/my_app/security.py
import frappe
from frappe import _
from frappe.permissions import has_permission, get_doc_permissions

def validate_todo_access(doc, method):
    """Валидация доступа к ToDo"""
    if doc.allocated_to and doc.allocated_to != frappe.session.user:
        # Проверка, является ли пользователь менеджером
        if not 'System Manager' in frappe.get_roles() and not 'ToDo Manager' in frappe.get_roles():
            frappe.throw(_("You don't have permission to access this ToDo"))

def get_todo_filters(user):
    """Получение фильтров для ToDo в зависимости от роли"""
    filters = {}
    
    # Пользователь может видеть только свои задачи
    if not 'System Manager' in frappe.get_roles() and not 'ToDo Manager' in frappe.get_roles():
        filters['allocated_to'] = user
    
    return filters

@frappe.whitelist()
def get_secure_todos():
    """Получение задач с учетом прав доступа"""
    user = frappe.session.user
    filters = get_todo_filters(user)
    
    todos = frappe.get_all(
        "ToDo",
        filters=filters,
        fields=["name", "description", "priority", "status", "allocated_to"],
        order_by="creation desc"
    )
    
    return todos

def before_insert_todo(doc, method):
    """Проверка перед созданием ToDo"""
    # Проверка, что пользователь может создавать задачи
    if not has_permission('ToDo', 'create'):
        frappe.throw(_("You don't have permission to create ToDo items"))
    
    # Если назначен другому пользователю, проверить права
    if doc.allocated_to and doc.allocated_to != frappe.session.user:
        if not has_permission('ToDo', 'write'):
            frappe.throw(_("You don't have permission to assign tasks to others"))

def before_save_todo(doc, method):
    """Проверка перед сохранением ToDo"""
    # Проверка прав на редактирование
    if doc.allocated_to != frappe.session.user and not 'System Manager' in frappe.get_roles():
        # Можно редактировать только если есть права на все задачи
        if not frappe.has_permission('ToDo', 'write'):
            frappe.throw(_("You can only edit your own tasks"))
```

### Защита от XSS и CSRF:

```python
# my_app/my_app/utils/security.py
import frappe
import html
import bleach
from frappe.utils import sanitize_html

def sanitize_user_input(text):
    """Санитизация пользовательского ввода"""
    if not text:
        return text
    
    # Очистка HTML
    clean_text = sanitize_html(text)
    
    # Дополнительная очистка с использованием bleach
    allowed_tags = ['p', 'br', 'strong', 'em', 'u', 'ol', 'ul', 'li', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6']
    allowed_attributes = {
        'a': ['href', 'title'],
        '*': ['class']
    }
    
    clean_text = bleach.clean(clean_text, tags=allowed_tags, attributes=allowed_attributes)
    
    return clean_text

@frappe.whitelist()
def save_safe_todo(description, priority="Medium"):
    """Сохранение безопасного ToDo"""
    # Санитизация ввода
    clean_description = sanitize_user_input(description)
    
    # Проверка длины
    if len(clean_description) > 10000:
        frappe.throw(_("Description too long"))
    
    # Создание документа
    todo = frappe.new_doc("ToDo")
    todo.description = clean_description
    todo.priority = priority
    todo.insert()
    
    return todo

def validate_api_request():
    """Валидация API запроса"""
    # Проверка CSRF токена
    if frappe.request and frappe.request.method in ['POST', 'PUT', 'DELETE']:
        csrf_token = frappe.get_request_header('X-Frappe-CSRF-Token')
        if not csrf_token or csrf_token != frappe.sessions.get_csrf_token():
            frappe.throw(_("CSRF token mismatch"), frappe.PermissionError)
    
    # Проверка referer для безопасности
    referer = frappe.get_request_header('Referer')
    if referer and not referer.startswith(frappe.utils.get_url()):
        # Дополнительная проверка для критических операций
        pass

# Hooks для автоматической проверки
doc_events = {
    "ToDo": {
        "validate": "my_app.security.validate_todo_access",
        "before_insert": "my_app.security.before_insert_todo",
        "before_save": "my_app.security.before_save_todo"
    }
}
```

## Тестирование

### Unit Tests:

```python
# my_app/my_app/test_todo.py
import unittest
import frappe
from frappe.tests.utils import FrappeTestCase
from my_app.api import create_todo, get_todos, update_todo_status

class TestToDo(FrappeTestCase):
    def setUp(self):
        """Setup test data"""
        # Очистка тестовых данных
        frappe.db.sql("DELETE FROM `tabToDo` WHERE description LIKE 'Test%'")
        frappe.db.commit()
    
    def tearDown(self):
        """Cleanup after tests"""
        frappe.db.sql("DELETE FROM `tabToDo` WHERE description LIKE 'Test%'")
        frappe.db.commit()
    
    def test_create_todo(self):
        """Test creating a new todo"""
        todo = create_todo("Test task", "High")
        
        self.assertIsNotNone(todo)
        self.assertEqual(todo.description, "Test task")
        self.assertEqual(todo.priority, "High")
        self.assertEqual(todo.status, "Open")
        
        # Проверка сохранения в базе
        db_todo = frappe.get_doc("ToDo", todo.name)
        self.assertEqual(db_todo.description, "Test task")
    
    def test_get_todos(self):
        """Test getting todos"""
        # Создание тестовых данных
        create_todo("Test task 1", "Low")
        create_todo("Test task 2", "High")
        
        # Получение всех задач
        todos = get_todos()
        self.assertGreaterEqual(len(todos), 2)
        
        # Получение задач с фильтром
        high_priority_todos = get_todos({"priority": "High"})
        self.assertGreaterEqual(len(high_priority_todos), 1)
        
        for todo in high_priority_todos:
            self.assertEqual(todo.priority, "High")
    
    def test_update_todo_status(self):
        """Test updating todo status"""
        todo = create_todo("Test task for status update", "Medium")
        
        # Обновление статуса
        updated_todo = update_todo_status(todo.name, "Completed")
        
        self.assertEqual(updated_todo.status, "Completed")
        
        # Проверка в базе данных
        db_todo = frappe.get_doc("ToDo", todo.name)
        self.assertEqual(db_todo.status, "Completed")
    
    def test_invalid_todo_creation(self):
        """Test invalid todo creation"""
        with self.assertRaises(Exception):
            # Тестируем без описания (обязательное поле)
            frappe.get_doc({
                "doctype": "ToDo",
                "priority": "High"
            }).insert()

class TestSecurity(FrappeTestCase):
    def test_todo_validation(self):
        """Test todo validation"""
        from my_app.security import validate_todo_access
        
        # Создание тестового пользователя
        if not frappe.db.exists("User", "test@example.com"):
            test_user = frappe.get_doc({
                "doctype": "User",
                "email": "test@example.com",
                "first_name": "Test",
                "send_welcome_email": 0
            }).insert()
        
        # Тестирование валидации
        todo = frappe.new_doc("ToDo")
        todo.description = "Test validation"
        todo.allocated_to = "test@example.com"
        
        # Валидация должна пройти успешно
        # (в реальных тестах нужно учитывать сессию пользователя)
        pass

# Тестирование API
def test_api_endpoints():
    """Test API endpoints manually"""
    import requests
    
    # Настройка сессии
    session = requests.Session()
    site_url = "http://localhost:8000"
    
    # Получение CSRF токена
    response = session.get(f"{site_url}/api/method/frappe.auth.get_logged_user")
    # ... продолжение тестирования API
```

### Frontend Tests:

```javascript
// my_app/public/js/test_todo.js
QUnit.module('ToDo Tests', {
    beforeEach: function() {
        // Установка фикстур
        this.server = sinon.fakeServer.create();
        this.server.autoRespond = true;
    },
    
    afterEach: function() {
        // Очистка
        this.server.restore();
    }
});

QUnit.test('Create ToDo', function(assert) {
    var done = assert.async();
    
    // Mock API response
    this.server.respondWith('POST', '/api/method/my_app.api.create_todo', [
        200,
        { 'Content-Type': 'application/json' },
        JSON.stringify({
            message: {
                name: 'TODO-00001',
                description: 'Test task',
                priority: 'Medium',
                status: 'Open'
            }
        })
    ]);
    
    // Тестирование
    frappe.call({
        method: 'my_app.api.create_todo',
        args: {
            description: 'Test task',
            priority: 'Medium'
        },
        callback: function(r) {
            assert.ok(r.message, 'Response received');
            assert.equal(r.message.description, 'Test task', 'Description matches');
            assert.equal(r.message.priority, 'Medium', 'Priority matches');
            done();
        }
    });
});

QUnit.test('Get Todos', function(assert) {
    var done = assert.async();
    
    // Mock data
    var mockTodos = [
        { name: 'TODO-00001', description: 'Task 1', priority: 'High' },
        { name: 'TODO-00002', description: 'Task 2', priority: 'Low' }
    ];
    
    this.server.respondWith('GET', '/api/method/my_app.api.get_todos', [
        200,
        { 'Content-Type': 'application/json' },
        JSON.stringify({ message: mockTodos })
    ]);
    
    frappe.call({
        method: 'my_app.api.get_todos',
        callback: function(r) {
            assert.ok(r.message, 'Response received');
            assert.equal(r.message.length, 2, 'Correct number of todos');
            assert.equal(r.message[0].description, 'Task 1', 'First task correct');
            done();
        }
    });
});

QUnit.test('Update Todo Status', function(assert) {
    var done = assert.async();
    
    this.server.respondWith('POST', '/api/method/my_app.api.update_todo_status', [
        200,
        { 'Content-Type': 'application/json' },
        JSON.stringify({
            message: {
                name: 'TODO-00001',
                status: 'Completed'
            }
        })
    ]);
    
    frappe.call({
        method: 'my_app.api.update_todo_status',
        args: {
            todo_name: 'TODO-00001',
            status: 'Completed'
        },
        callback: function(r) {
            assert.ok(r.message, 'Response received');
            assert.equal(r.message.status, 'Completed', 'Status updated');
            done();
        }
    });
});
```

## Развертывание

### Production Setup:

```bash
# production.sh - Скрипт для production установки
#!/bin/bash

# Установка зависимостей
sudo apt-get update
sudo apt-get install -y python3-dev python3-setuptools python3-pip
sudo apt-get install -y mariadb-server redis-server nginx supervisor

# Установка Node.js
curl -sL https://deb.nodesource.com/setup_16.x | sudo -E bash -
sudo apt-get install -y nodejs

# Установка Bench
pip3 install frappe-bench

# Создание пользователя для frappe
sudo adduser --system --group frappe
sudo mkdir -p /opt/frappe
sudo chown frappe:frappe /opt/frappe

# Создание инстанса
sudo -u frappe -H bash -c "
    cd /opt/frappe &&
    bench init frappe-bench --frappe-branch version-14
"

# Настройка сайта
sudo -u frappe -H bash -c "
    cd /opt/frappe/frappe-bench &&
    bench new-site mysite.com --mariadb-root-password production_password
"

# Установка приложений
sudo -u frappe -H bash -c "
    cd /opt/frappe/frappe-bench &&
    bench get-app my_app /path/to/my_app &&
    bench --site mysite.com install-app my_app
"

# Настройка supervisor
sudo tee /etc/supervisor/conf.d/frappe-workers.conf > /dev/null << EOF
[group:frappe]
programs:frappe-web,frappe-long,frappe-short,frappe-default

[program:frappe-web]
command=/opt/frappe/frappe-bench/env/bin/python -m frappe.utils.bench_helper start
directory=/opt/frappe/frappe-bench/sites
user=frappe
autostart=true
autorestart=true
redirect_stderr=true
stdout_logfile=/opt/frappe/frappe-bench/logs/web.log

[program:frappe-default]
command=/opt/frappe/frappe-bench/env/bin/python -m frappe.utils.background_jobs --queue default
directory=/opt/frappe/frappe-bench/sites
user=frappe
autostart=true
autorestart=true
redirect_stderr=true
stdout_logfile=/opt/frappe/frappe-bench/logs/default_worker.log

[program:frappe-short]
command=/opt/frappe/frappe-bench/env/bin/python -m frappe.utils.background_jobs --queue short
directory=/opt/frappe/frappe-bench/sites
user=frappe
autostart=true
autorestart=true
redirect_stderr=true
stdout_logfile=/opt/frappe/frappe-bench/logs/short_worker.log

[program:frappe-long]
command=/opt/frappe/frappe-bench/env/bin/python -m frappe.utils.background_jobs --queue long
directory=/opt/frappe/frappe-bench/sites
user=frappe
autostart=true
autorestart=true
redirect_stderr=true
stdout_logfile=/opt/frappe/frappe-bench/logs/long_worker.log
EOF

# Настройка nginx
sudo tee /etc/nginx/sites-available/mysite.com > /dev/null << EOF
upstream frappe {
    server 127.0.0.1:8000;
}

server {
    listen 80;
    server_name mysite.com;
    client_max_body_size 100M;

    # static files
    location /assets {
        alias /opt/frappe/frappe-bench/sites/assets;
        expires 1y;
        add_header Cache-Control "public, immutable";
    }

    location /files {
        alias /opt/frappe/frappe-bench/sites/;
        expires 1y;
        add_header Cache-Control "public, immutable";
        try_files \$uri =404;
    }

    location / {
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header Host \$host;
        proxy_set_header X-Use-X-Accel-Redirect True;
        proxy_redirect off;
        proxy_pass http://frappe;
    }
}
EOF

sudo ln -s /etc/nginx/sites-available/mysite.com /etc/nginx/sites-enabled/mysite.com
sudo nginx -t
sudo systemctl reload nginx

# Перезапуск сервисов
sudo supervisorctl reread
sudo supervisorctl update
sudo supervisorctl restart frappe:*
```

### Docker Production:

```dockerfile
# Dockerfile.production
FROM python:3.10-slim

# Установка системных зависимостей
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    git \
    mariadb-client \
    && rm -rf /var/lib/apt/lists/*

# Установка Node.js
RUN curl -sL https://deb.nodesource.com/setup_16.x | bash - \
    && apt-get install -y nodejs

# Создание пользователя
RUN useradd -m -s /bin/bash frappe

# Установка Bench
RUN pip install frappe-bench

# Копирование приложения
COPY --chown=frappe:frappe . /home/frappe/frappe-bench/apps/my_app

# Переключение на пользователя frappe
USER frappe
WORKDIR /home/frappe/frappe-bench

# Установка приложения
RUN bench get-app my_app /home/frappe/frappe-bench/apps/my_app

# Создание сайта
RUN bench new-site site1.local --mariadb-root-password 123 --admin-password admin

# Установка приложения на сайт
RUN bench --site site1.local install-app my_app

# Создание конфигурации
RUN bench setup production frappe

EXPOSE 8000

CMD ["bench", "start"]
```

## Лучшие практики

### 1. Структура приложения:

```python
# my_app/hooks.py - Хорошая организация hooks
app_name = "my_app"
app_title = "My App"
app_publisher = "My Publisher"
app_version = "0.0.1"

# Сайт
website_context = {
    "favicon": "/assets/my_app/images/favicon.ico",
    "splash_image": "/assets/my_app/images/splash.png"
}

# Запланированные задачи
scheduler_events = {
    "daily": [
        "my_app.tasks.daily_cleanup"
    ],
    "hourly": [
        "my_app.tasks.hourly_sync"
    ],
    "all": [
        "my_app.tasks.every_minute_check"
    ]
}

# API переопределения
override_whitelisted_methods = {
    "frappe.desk.form.save.handler": "my_app.api.custom_save"
}

# DocType события
doc_events = {
    "*": {
        "on_update": "my_app.event_handlers.log_changes",
        "after_insert": "my_app.event_handlers.track_creation"
    },
    "ToDo": {
        "on_submit": "my_app.todo.handlers.on_submit",
        "on_cancel": "my_app.todo.handlers.on_cancel",
        "before_save": "my_app.todo.handlers.before_save"
    }
}

# Разрешения
has_permission = {
    "ToDo": "my_app.permissions.todo_has_permission",
    "Custom Customer": "my_app.permissions.customer_has_permission"
}

# Поля для игнорирования в логах
doc_events_ignore = {
    "*": ["modified", "modified_by", "owner"]
}
```

### 2. Оптимизация производительности:

```python
# my_app/utils/performance.py
import frappe
import time
from functools import wraps
from frappe.utils import cint

def cache_results(ttl=300):
    """Декоратор для кэширования результатов"""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            # Создание ключа кэша
            cache_key = f"{func.__name__}:{str(args)}:{str(kwargs)}"
            cached_result = frappe.cache().get_value(cache_key)
            
            if cached_result is not None:
                return cached_result
            
            # Выполнение функции
            result = func(*args, **kwargs)
            
            # Сохранение в кэш
            frappe.cache().set_value(cache_key, result, expires_in_sec=ttl)
            
            return result
        return wrapper
    return decorator

@cache_results(ttl=600)  # 10 минут
@frappe.whitelist()
def get_expensive_report_data(filters=None):
    """Получение данных отчета с кэшированием"""
    # Запрос к базе данных
    data = frappe.db.sql("""
        SELECT 
            customer,
            SUM(amount) as total_amount,
            COUNT(*) as order_count
        FROM `tabSales Order`
        WHERE docstatus = 1
        GROUP BY customer
        ORDER BY total_amount DESC
    """, as_dict=True)
    
    return data

def optimize_queries():
    """Пример оптимизации запросов"""
    
    # ПЛОХО: Много отдельных запросов
    # customers = frappe.get_all('Customer')
    # for customer in customers:
    #     details = frappe.get_doc('Customer', customer.name)  # Отдельный запрос!
    
    # ХОРОШО: Один запрос с полями
    customers = frappe.get_all(
        'Customer',
        fields=['name', 'customer_name', 'email', 'territory'],
        limit_page_length=1000
    )
    
    return customers

@frappe.whitelist()
def batch_process_large_dataset():
    """Пакетная обработка большого набора данных"""
    batch_size = 500
    processed = 0
    
    # Получение идентификаторов
    todo_names = frappe.get_all(
        'ToDo',
        filters={'status': 'Open'},
        pluck='name',
        limit=10000  # Ограничение для больших наборов
    )
    
    for i in range(0, len(todo_names), batch_size):
        batch = todo_names[i:i + batch_size]
        
        # Пакетная обработка
        for todo_name in batch:
            try:
                todo = frappe.get_doc('ToDo', todo_name)
                todo.status = 'In Progress'
                todo.save()
                processed += 1
            except Exception as e:
                frappe.log_error(f"Batch processing error: {str(e)}")
        
        # Commit после каждого батча
        frappe.db.commit()
        
        # Уведомление о прогрессе
        frappe.publish_progress(
            percent=i/len(todo_names)*100,
            title=_('Processing...'),
            description=f'Processed {processed} of {len(todo_names)}'
        )
    
    return {'processed': processed, 'total': len(todo_names)}

# Индексация для производительности
def setup_indexes():
    """Настройка индексов для производительности"""
    
    # Создание индексов для часто используемых полей
    indexes_config = [
        ('ToDo', 'status'),
        ('ToDo', 'priority'),
        ('ToDo', 'allocated_to'),
        ('ToDo', ['status', 'priority']),  # Композитный индекс
        ('Custom Customer', 'customer_group'),
        ('Sales Order', 'customer'),
        ('Sales Order', 'transaction_date'),
        ('Sales Order', ['customer', 'docstatus'])
    ]
    
    for doctype, fieldnames in indexes_config:
        if isinstance(fieldnames, str):
            fieldnames = [fieldnames]
        
        # Создание индекса
        try:
            index_name = f"idx_{doctype.lower()}_{'_'.join(fieldnames)}".replace(' ', '_')
            frappe.db.sql(f"""
                CREATE INDEX IF NOT EXISTS `{index_name}` 
                ON `tab{doctype}` ({','.join(f'`{f}`' for f in fieldnames)})
            """)
        except Exception as e:
            frappe.log_error(f"Index creation error: {str(e)}")
```

### 3. Обработка ошибок и логирование:

```python
# my_app/utils/error_handling.py
import frappe
import traceback
import logging
from frappe import _
from frappe.utils import now

class ErrorHandler:
    @staticmethod
    def handle_error(error, context=""):
        """Централизованная обработка ошибок"""
        error_details = {
            'error': str(error),
            'traceback': traceback.format_exc(),
            'context': context,
            'timestamp': now(),
            'user': frappe.session.user,
            'request': getattr(frappe.local, 'request', {}).get('path') if hasattr(frappe.local, 'request') else None
        }
        
        # Логирование в базу данных
        try:
            error_log = frappe.get_doc({
                'doctype': 'Error Log',
                'method': context,
                'error': error_details['traceback']
            })
            error_log.insert(ignore_permissions=True)
        except Exception as log_error:
            # Если не можем записать в базу, логируем в файл
            frappe.log_error(f"Could not create error log: {str(log_error)}")
        
        # Возвращаем пользовательское сообщение
        if frappe.conf.developer_mode:
            # В режиме разработчика показываем полную ошибку
            frappe.throw(error_details['traceback'])
        else:
            # В продакшене - дружелюбное сообщение
            frappe.throw(_("An error occurred. Please contact administrator."))

def safe_execute(func, *args, **kwargs):
    """Безопасное выполнение функции с обработкой ошибок"""
    try:
        return func(*args, **kwargs)
    except Exception as e:
        ErrorHandler.handle_error(e, f"{func.__module__}.{func.__name__}")
        return None

@frappe.whitelist()
def robust_api_method(param1, param2=None):
    """Пример надежного API метода"""
    try:
        # Валидация параметров
        if not param1:
            frappe.throw(_("Parameter param1 is required"))
        
        # Основная логика
        result = process_data(param1, param2)
        
        # Логирование успешного выполнения
        frappe.log(
            f"API method executed successfully with params: {param1}, {param2}",
            "INFO"
        )
        
        return result
        
    except frappe.ValidationError:
        # Ошибки валидации - возвращаем пользователю
        raise
    except Exception as e:
        # Все остальные ошибки - обрабатываем централизованно
        ErrorHandler.handle_error(e, "robust_api_method")
        return None

def process_data(param1, param2=None):
    """Обработка данных с валидацией"""
    # Валидация
    if not isinstance(param1, str):
        raise ValueError("param1 must be string")
    
    if param2 and not isinstance(param2, dict):
        raise ValueError("param2 must be dictionary if provided")
    
    # Обработка
    processed_data = {
        'input': param1,
        'processed': param1.upper(),
        'length': len(param1),
        'metadata': param2 or {}
    }
    
    return processed_data

# Логирование производительности
def log_performance(func):
    """Декоратор для логирования производительности"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        
        try:
            result = func(*args, **kwargs)
            execution_time = time.time() - start_time
            
            # Логирование медленных выполнений
            if execution_time > 1.0:  # Больше 1 секунды
                frappe.log(
                    f"SLOW EXECUTION: {func.__name__} took {execution_time:.2f}s",
                    "WARNING"
                )
            
            return result
            
        except Exception as e:
            execution_time = time.time() - start_time
            frappe.log(
                f"ERROR in {func.__name__} after {execution_time:.2f}s: {str(e)}",
                "ERROR"
            )
            raise
    
    return wrapper
```

> Этот мануал охватывает основные аспекты `Frappe Framework`

> Для более глубокого изучения рекомендуется практиковаться на реальных проектах и изучать официальную документацию.

