# Основы тестирования и отладки в Python

**Тестирование и отладка кода** — важные этапы разработки, которые помогают убедиться в правильной работе программы, выявить ошибки и исключить неожиданные поведения.

### 1. Основы юнит-тестирования

**Юнит-тестирование** — это процесс проверки отдельных модулей или функций программы на корректность.

Для юнит-тестирования в Python часто используется встроенный модуль unittest.

#### 1.1 Юнит-тестирование с unittest

Модуль `unittest` позволяет создавать тестовые случаи (`test cases`), которые проверяют конкретные функции или методы.

Юнит-тесты помогают выявить ошибки на ранних этапах разработки.

**Пример использования unittest:**

```python
import unittest

# Пример функции для тестирования
def add(a, b):
    return a + b

# Определение теста
class TestAddFunction(unittest.TestCase):
    def test_add(self):
        self.assertEqual(add(1, 2), 3)  # Проверка результата
        self.assertEqual(add(-1, 1), 0)
        self.assertEqual(add(0, 0), 0)

# Запуск тестов
if __name__ == '__main__':
    unittest.main()
```

**Общие методы для тестирования:**

- assertEqual(a, b) — проверяет, что значения a и b равны.
- assertNotEqual(a, b) — проверяет, что значения a и b не равны.
- assertTrue(x) — проверяет, что выражение x истинно.
- assertFalse(x) — проверяет, что выражение x ложно.

#### 1.2 Тестирование с pytest

**pytest** — это более мощный и гибкий инструмент для тестирования в Python.

Его популярность обусловлена простотой синтаксиса и расширяемостью.

**Пример использования pytest:**

```python
# test_sample.py
def add(a, b):
    return a + b

def test_add():
    assert add(1, 2) == 3
    assert add(-1, 1) == 0
```

**Для запуска тестов используется команда:**

```bash
pytest
```

### 2. Инструменты для отладки

**Отладка** — это процесс пошагового выполнения программы для выявления ошибок и анализа её работы.

В Python есть несколько инструментов для отладки.

#### 2.1 Использование print() для отладки

**Простой, но эффективный способ отладки** — вывод промежуточных значений с помощью функции `print()`.

Хотя этот метод не всегда является лучшим, он помогает быстро увидеть текущие значения переменных.

**Пример:**

```python
def divide(a, b):
    print(f"Значения a={a}, b={b}")
    return a / b

divide(10, 2)  # выводит "Значения a=10, b=2"
```

#### 2.2 Использование модуля pdb

`pdb (Python Debugger)` — это встроенный отладчик в Python, который позволяет приостановить выполнение программы и исследовать состояние переменных.

**Пример использования pdb:**

```python
import pdb

def divide(a, b):
    pdb.set_trace()  # Установка точки останова
    return a / b

divide(10, 2)
```

При запуске программы выполнение остановится на строке с `pdb.set_trace()`, и откроется интерактивная консоль для отладки.

#### 2.3 Отладка в IDE

Многие современные среды разработки (PyCharm, VS Code и другие) поддерживают встроенные средства отладки, которые позволяют пошагово выполнять код, устанавливать точки останова, анализировать значения переменных и стек вызовов.

### 3. Логирование и обработка исключений

Логирование и обработка исключений помогают отслеживать поведение программы в режиме выполнения и реагировать на непредвиденные ошибки.

#### 3.1 Обработка исключений

В Python для обработки ошибок используется механизм исключений (`try-except`).

Этот механизм позволяет перехватывать ошибки и предотвращать аварийное завершение программы.

**Пример обработки исключений:**

```python
def divide(a, b):
    try:
        result = a / b
    except ZeroDivisionError:
        print("Ошибка: деление на ноль!")
        return None
    return result

print(divide(10, 2))  # 5.0
print(divide(10, 0))  # Ошибка: деление на ноль
```

В данном примере блок `try-except` перехватывает исключение `ZeroDivisionError` и предотвращает ошибку при делении на ноль.

#### 3.2 Логирование с помощью модуля logging

Модуль `logging` позволяет сохранять сообщения о состоянии программы в файл или консоль, что помогает при анализе работы программы в будущем.

**Пример использования logging:**

```python
import logging

# Настройка логирования
logging.basicConfig(level=logging.INFO)

def divide(a, b):
    try:
        result = a / b
        logging.info(f"Успешное деление: {a} / {b} = {result}")
    except ZeroDivisionError:
        logging.error("Ошибка: деление на ноль!")
        return None
    return result

divide(10, 2)
divide(10, 0)
```

**Уровни логирования:**

- `DEBUG` — подробные сообщения для отладки.
- `INFO` — информационные сообщения.
- `WARNING` — предупреждения.
- `ERROR` — ошибки, которые не приводят к завершению программы.
- `CRITICAL` — критические ошибки.

### Выводы

**Тестирование и отладка** — важные части процесса разработки.

**Юнит-тесты** помогают убедиться в корректной работе каждой части программы, **инструменты для отладки** — выявить ошибки, а **логирование** — отслеживать выполнение программы в реальном времени.



**Автор:** Дуплей Максим Игоревич

**Дата:** 07.09.2024

**Версия:** 1.0