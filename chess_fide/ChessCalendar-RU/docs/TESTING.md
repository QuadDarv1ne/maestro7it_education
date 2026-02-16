# Руководство по тестированию

## Обзор

Проект использует pytest для тестирования с поддержкой:
- Unit тесты
- Integration тесты
- Coverage отчеты
- Fixtures для тестовых данных
- Mocking для внешних зависимостей

## Структура тестов

```
tests/
├── conftest.py           # Общие fixtures
├── unit/                 # Unit тесты
│   ├── test_models.py
│   ├── test_cache.py
│   └── test_celery_tasks.py
├── integration/          # Integration тесты
│   └── test_api.py
└── fixtures/             # Тестовые данные
```

## Запуск тестов

### Все тесты

```bash
# Через pytest
pytest

# Через Makefile
make test

# Через скрипт
./scripts/test.sh
```

### Конкретные тесты

```bash
# Только unit тесты
pytest tests/unit/

# Только integration тесты
pytest tests/integration/

# Конкретный файл
pytest tests/unit/test_models.py

# Конкретный тест
pytest tests/unit/test_models.py::TestTournamentModel::test_create_tournament
```

### С маркерами

```bash
# Только unit тесты
pytest -m unit

# Только integration тесты
pytest -m integration

# Исключить медленные тесты
pytest -m "not slow"
```

## Coverage

### Генерация отчета

```bash
# HTML отчет
pytest --cov=app --cov-report=html

# Terminal отчет
pytest --cov=app --cov-report=term-missing

# XML отчет (для CI)
pytest --cov=app --cov-report=xml

# Все вместе
make test-coverage
```

### Просмотр отчета

```bash
# Открыть HTML отчет
open htmlcov/index.html  # Mac
xdg-open htmlcov/index.html  # Linux
start htmlcov/index.html  # Windows
```

### Требования к coverage

- Минимум: 50%
- Цель: 80%
- Критичные модули: 90%+

## Написание тестов

### Unit тесты

```python
# tests/unit/test_example.py
import pytest
from app.models.tournament import Tournament

class TestTournament:
    """Tests for Tournament model"""
    
    def test_create_tournament(self, db_session):
        """Test creating a tournament"""
        tournament = Tournament(
            name='Test Tournament',
            location='Moscow',
            # ...
        )
        db_session.session.add(tournament)
        db_session.session.commit()
        
        assert tournament.id is not None
        assert tournament.name == 'Test Tournament'
    
    def test_validation(self):
        """Test tournament validation"""
        tournament = Tournament(
            name='Test',
            # Invalid data...
        )
        
        errors = tournament.validate()
        assert len(errors) > 0
```

### Integration тесты

```python
# tests/integration/test_api.py
class TestTournamentAPI:
    """Tests for tournament API"""
    
    def test_get_tournaments(self, client, multiple_tournaments):
        """Test getting tournaments list"""
        response = client.get('/api/tournaments')
        
        assert response.status_code == 200
        data = response.json
        assert len(data) > 0
    
    def test_create_tournament(self, client, auth_headers):
        """Test creating tournament"""
        response = client.post('/api/tournaments',
            headers=auth_headers,
            json={
                'name': 'New Tournament',
                # ...
            }
        )
        
        assert response.status_code == 201
```

### Использование fixtures

```python
def test_with_sample_data(sample_tournament, sample_user):
    """Test using fixtures"""
    assert sample_tournament.id is not None
    assert sample_user.username == 'testuser'
```

### Mocking

```python
from unittest.mock import Mock, patch

@patch('app.tasks.parser_tasks.FIDEParser')
def test_parse_tournaments(mock_parser_class):
    """Test with mocked parser"""
    mock_parser = Mock()
    mock_parser.parse_tournaments.return_value = []
    mock_parser_class.return_value = mock_parser
    
    # Test code...
    
    mock_parser.parse_tournaments.assert_called_once()
```

## Fixtures

### Доступные fixtures

```python
# conftest.py

@pytest.fixture
def app():
    """Flask application"""
    
@pytest.fixture
def client(app):
    """Test client"""
    
@pytest.fixture
def db_session(app):
    """Database session"""
    
@pytest.fixture
def sample_tournament(db_session):
    """Sample tournament"""
    
@pytest.fixture
def sample_user(db_session):
    """Sample user"""
    
@pytest.fixture
def admin_user(db_session):
    """Admin user"""
    
@pytest.fixture
def auth_headers(client, admin_user):
    """JWT auth headers"""
    
@pytest.fixture
def multiple_tournaments(db_session):
    """Multiple tournaments"""
```

### Создание своих fixtures

```python
# tests/conftest.py

@pytest.fixture
def custom_fixture(db_session):
    """Custom fixture"""
    # Setup
    data = create_test_data()
    
    yield data
    
    # Teardown
    cleanup_test_data()
```

## Best Practices

### 1. Именование

```python
# Good
def test_create_tournament_with_valid_data():
    pass

def test_create_tournament_with_invalid_date():
    pass

# Bad
def test1():
    pass

def test_tournament():
    pass
```

### 2. Arrange-Act-Assert

```python
def test_example():
    # Arrange - подготовка
    tournament = Tournament(name='Test')
    
    # Act - действие
    result = tournament.validate()
    
    # Assert - проверка
    assert len(result) == 0
```

### 3. Один тест - одна проверка

```python
# Good
def test_tournament_name():
    tournament = Tournament(name='Test')
    assert tournament.name == 'Test'

def test_tournament_location():
    tournament = Tournament(location='Moscow')
    assert tournament.location == 'Moscow'

# Bad
def test_tournament():
    tournament = Tournament(name='Test', location='Moscow')
    assert tournament.name == 'Test'
    assert tournament.location == 'Moscow'
    assert tournament.status == 'Scheduled'
```

### 4. Использование параметризации

```python
@pytest.mark.parametrize('status,expected', [
    ('Scheduled', True),
    ('Ongoing', True),
    ('Completed', False),
    ('Cancelled', False),
])
def test_tournament_is_active(status, expected):
    tournament = Tournament(status=status)
    assert tournament.is_active() == expected
```

### 5. Тестирование исключений

```python
def test_invalid_tournament():
    with pytest.raises(ValueError):
        tournament = Tournament(name='')
        tournament.validate()
```

## CI/CD Integration

### GitHub Actions

```yaml
# .github/workflows/ci.yml
- name: Run tests
  run: |
    pytest tests/ --cov=app --cov-report=xml
    
- name: Upload coverage
  uses: codecov/codecov-action@v3
  with:
    file: ./coverage.xml
```

### Pre-commit hooks

```bash
# Запуск тестов перед commit
pre-commit install

# Ручной запуск
pre-commit run --all-files
```

## Troubleshooting

### Проблема: Тесты не находятся

```bash
# Проверьте PYTHONPATH
export PYTHONPATH="${PYTHONPATH}:$(pwd)"

# Или установите пакет в dev режиме
pip install -e .
```

### Проблема: Ошибки импорта

```python
# Добавьте в conftest.py
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
```

### Проблема: База данных не очищается

```python
# Используйте scope='function' для fixtures
@pytest.fixture(scope='function')
def db_session(app):
    with app.app_context():
        db.create_all()
        yield db
        db.session.remove()
        db.drop_all()
```

### Проблема: Медленные тесты

```bash
# Найдите медленные тесты
pytest --durations=10

# Пометьте медленные тесты
@pytest.mark.slow
def test_slow_operation():
    pass

# Пропустите их
pytest -m "not slow"
```

## Метрики качества

### Coverage

```bash
# Текущий coverage
pytest --cov=app --cov-report=term-missing

# Требуемый минимум
pytest --cov=app --cov-fail-under=50
```

### Качество тестов

- Все тесты должны проходить
- Coverage > 50%
- Нет пропущенных тестов (skip)
- Нет игнорируемых предупреждений
- Быстрое выполнение (< 1 минута для unit)

## Дополнительные ресурсы

- [Pytest Documentation](https://docs.pytest.org/)
- [Coverage.py Documentation](https://coverage.readthedocs.io/)
- [Testing Best Practices](https://docs.python-guide.org/writing/tests/)
