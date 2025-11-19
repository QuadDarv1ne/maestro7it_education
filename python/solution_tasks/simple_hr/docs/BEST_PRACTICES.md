"""
# Руководство по лучшим практикам - Simple HR v2.4

## Оглавление
1. [Код и типизация](#код-и-типизация)
2. [Обработка ошибок](#обработка-ошибок)
3. [Валидация данных](#валидация-данных)
4. [Оптимизация запросов](#оптимизация-запросов)
5. [Кэширование](#кэширование)
6. [Логирование](#логирование)
7. [Тестирование](#тестирование)
8. [Безопасность](#безопасность)

---

## Код и типизация

### ✅ ПРАВИЛЬНО:
```python
from typing import Optional, List, Dict, Any

def create_user(name: str, email: str, age: int) -> Dict[str, Any]:
    \"\"\"Create a new user with validation.\"\"\"
    user = User(name=name, email=email, age=age)
    return user.to_dict()

def get_users(active: bool = True) -> List['User']:
    \"\"\"Get all users, optionally filtered by active status.\"\"\"
    return User.query.filter_by(active=active).all()
```

### ❌ НЕПРАВИЛЬНО:
```python
def create_user(name, email, age):
    user = User(name=name, email=email, age=age)
    return user.to_dict()

def get_users(active=True):
    return User.query.filter_by(active=active).all()
```

---

## Обработка ошибок

### ✅ ПРАВИЛЬНО:
```python
from app.exceptions import ValidationError, NotFoundError, DatabaseError

@app.route('/api/users/<int:user_id>', methods=['GET'])
def get_user(user_id: int) -> Dict[str, Any]:
    try:
        user = User.query.get(user_id)
        if not user:
            raise NotFoundError("User")
        return user.to_dict()
    except Exception as e:
        logger.error(f"Failed to get user {user_id}: {str(e)}")
        raise DatabaseError("Failed to retrieve user")
```

### ❌ НЕПРАВИЛЬНО:
```python
@app.route('/api/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    user = User.query.get(user_id)
    return user.to_dict()  # Может вернуть None
```

---

## Валидация данных

### ✅ ПРАВИЛЬНО:
```python
from app.validators import EmailValidator, StringValidator, validate_dict

@app.route('/api/users', methods=['POST'])
def create_user_endpoint() -> Dict[str, Any]:
    data = request.get_json()
    
    # Валидация входных данных
    schema = {
        'name': StringValidator,
        'email': EmailValidator,
    }
    
    is_valid, errors = validate_dict(data, schema)
    if not is_valid:
        raise ValidationError(details=errors)
    
    # Создание пользователя
    user = User(**data)
    db.session.add(user)
    db.session.commit()
    
    return user.to_dict(), 201
```

### ❌ НЕПРАВИЛЬНО:
```python
@app.route('/api/users', methods=['POST'])
def create_user_endpoint():
    data = request.get_json()
    user = User(**data)  # Нет валидации!
    db.session.add(user)
    db.session.commit()
    return user.to_dict()
```

---

## Оптимизация запросов

### ✅ ПРАВИЛЬНО:
```python
from app.query_optimization import OptimizedQuery

@app.route('/api/departments/<int:dept_id>/employees')
def get_department_employees(dept_id: int) -> Dict[str, Any]:
    # Используем OptimizedQuery для предотвращения N+1
    query = OptimizedQuery(Employee, db.session)
    employees = (query
                 .with_relationships('position', 'department')
                 .with_columns('id', 'name', 'position_id')
                 .filter_by(department_id=dept_id)
                 .all())
    
    return {
        'employees': [e.to_dict() for e in employees],
        'count': len(employees)
    }
```

### ❌ НЕПРАВИЛЬНО:
```python
@app.route('/api/departments/<int:dept_id>/employees')
def get_department_employees(dept_id):
    employees = Employee.query.filter_by(department_id=dept_id).all()
    # Если Employee имеет связи с Position и Department,
    # это вызовет N+1 проблему!
    return [e.to_dict() for e in employees]
```

---

## Кэширование

### ✅ ПРАВИЛЬНО:
```python
from app.cache_utils import cached, cache_per_user

# Общее кэширование на 1 час
@cached(timeout=3600, key_prefix="dashboard_stats")
def get_dashboard_statistics() -> Dict[str, int]:
    return {
        'total_employees': Employee.query.count(),
        'total_departments': Department.query.count(),
        'active_vacations': Vacation.query.filter_by(active=True).count(),
    }

# Кэширование на пользователя
@cache_per_user(timeout=300)
def get_user_settings() -> Dict[str, Any]:
    user = current_user
    return {
        'theme': user.theme,
        'language': user.language,
        'notifications': user.notifications_enabled,
    }
```

### ❌ НЕПРАВИЛЬНО:
```python
# Без кэширования - запрос выполняется каждый раз
def get_dashboard_statistics():
    return {
        'total_employees': Employee.query.count(),
        'total_departments': Department.query.count(),
    }
```

---

## Логирование

### ✅ ПРАВИЛЬНО:
```python
from app.logging_utils import log_execution, StructuredLogger

logger = StructuredLogger(__name__)

@log_execution(log_args=False, log_result=False)
def process_employee_data(employee_id: int) -> bool:
    try:
        logger.info("Starting employee processing", employee_id=employee_id)
        
        employee = Employee.query.get(employee_id)
        if not employee:
            logger.warning("Employee not found", employee_id=employee_id)
            return False
        
        # Обработка
        result = perform_operation(employee)
        
        logger.info("Employee processed successfully", 
                   employee_id=employee_id, 
                   result=result)
        return True
        
    except Exception as e:
        logger.error("Failed to process employee", 
                    exception=e, 
                    employee_id=employee_id)
        raise
```

### ❌ НЕПРАВИЛЬНО:
```python
def process_employee_data(employee_id):
    employee = Employee.query.get(employee_id)
    # Нет логирования!
    result = perform_operation(employee)
    return result
```

---

## Тестирование

### ✅ ПРАВИЛЬНО:
```python
import pytest
from app.validators import EmailValidator, validate_employee_data

class TestEmailValidator:
    \"\"\"Test cases for EmailValidator.\"\"\"
    
    def test_valid_email(self):
        \"\"\"Test validation of valid email.\"\"\"
        validator = EmailValidator()
        is_valid, error = validator.validate("user@example.com")
        assert is_valid is True
        assert error is None
    
    def test_invalid_email(self):
        \"\"\"Test validation of invalid email.\"\"\"
        validator = EmailValidator()
        is_valid, error = validator.validate("invalid-email")
        assert is_valid is False
        assert error is not None

@pytest.mark.validators
def test_validate_employee_data_valid():
    \"\"\"Test employee data validation with valid data.\"\"\"
    data = {
        'first_name': 'John',
        'last_name': 'Doe',
        'email': 'john@example.com',
        'phone': '+1234567890',
    }
    is_valid, errors = validate_employee_data(data)
    assert is_valid is True
```

### ❌ НЕПРАВИЛЬНО:
```python
# Без тестов!
# или
def test_something():
    result = some_function()
    # Нет assert-ов!
```

---

## Безопасность

### ✅ ПРАВИЛЬНО:
```python
from app.validators import sanitize_input, EmailValidator
from app.exceptions import ValidationError

@app.route('/api/search', methods=['GET'])
def search() -> Dict[str, Any]:
    # Санитизация входных данных
    query = sanitize_input(request.args.get('q', ''), max_length=100)
    
    if not query or len(query) < 3:
        raise ValidationError("Search query must be at least 3 characters")
    
    # SQL-инъекции невозможны благодаря SQLAlchemy
    results = (Employee.query
               .filter(Employee.name.ilike(f"%{query}%"))
               .limit(10)
               .all())
    
    return {'results': [r.to_dict() for r in results]}
```

### ❌ НЕПРАВИЛЬНО:
```python
# Опасно! SQL-инъекция возможна
@app.route('/api/search')
def search():
    query = request.args.get('q')
    sql = f"SELECT * FROM employees WHERE name LIKE '%{query}%'"
    # Нет санитизации!
    results = db.session.execute(sql).fetchall()
    return results
```

---

## Структура запроса API

### ✅ ПРАВИЛЬНО:
```python
@app.route('/api/employees', methods=['POST'])
def create_employee() -> tuple[Dict[str, Any], int]:
    \"\"\"
    Create a new employee.
    
    Request body:
        {
            "first_name": "John",
            "last_name": "Doe",
            "email": "john@example.com",
            "department_id": 1
        }
    
    Returns:
        (employee_dict, 201)
    \"\"\"
    try:
        data = request.get_json()
        
        # Валидация
        is_valid, errors = validate_employee_data(data)
        if not is_valid:
            raise ValidationError(details=errors)
        
        # Создание
        employee = Employee(**data)
        db.session.add(employee)
        db.session.commit()
        
        logger.info("Employee created", employee_id=employee.id)
        
        return employee.to_dict(), 201
        
    except ValidationError as e:
        return e.to_dict(), e.code
    except Exception as e:
        logger.error("Failed to create employee", exception=e)
        raise DatabaseError("Failed to create employee")
```

---

## Быстрая справка команд

```bash
# Проверка качества кода
make quality

# Запуск тестов
make test
make test-validators
make test-exceptions

# Форматирование кода
make format

# Запуск приложения
make dev          # Разработка
make run          # Production

# Docker
make docker-up
make docker-logs
make docker-down
```

---

## Чек-лист перед commit

- [ ] Использованы type hints везде
- [ ] Добавлены docstrings
- [ ] Входные данные валидированы
- [ ] Обработаны все исключения
- [ ] Код форматирован (`make format`)
- [ ] Тесты проходят (`make test`)
- [ ] Качество кода проверено (`make quality`)
- [ ] Нет TODO комментариев (или задача создана)

---

## Полезные ссылки

- [Type Hints Documentation](https://docs.python.org/3/library/typing.html)
- [SQLAlchemy Docs](https://docs.sqlalchemy.org/)
- [Flask Best Practices](https://flask.palletsprojects.com/best_practices/)
- [OWASP Security](https://owasp.org/www-community/)

---

**Версия:** 2.4  
**Последнее обновление:** 19 ноября 2025
"""
