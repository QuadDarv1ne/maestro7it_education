# Функции и модули: Объявление и использование

### Цели урока:
- Научиться определять функции в Python.
- Понять работу с аргументами и возвращаемыми значениями.
- Изучить работу с модулями и пакетами для организации кода.

### 1. Определение функций

**Функция** — это блок кода, который выполняется только тогда, когда его вызывают.

Функции помогают структурировать код, делая его более читаемым и повторно используемым.

**Синтаксис:**
```python
def имя_функции(параметры):
    # тело функции
    return результат
```

**Пример функции:**
```python
def greet(name):
    return f"Hello, {name}!"
```

**Вызов функции:**
```python
print(greet("Alice"))  # Вывод: Hello, Alice
```

### 2. Аргументы и возвращаемые значения

Функции могут принимать аргументы, которые передаются при вызове функции.

Также они могут возвращать значения с помощью оператора `return`.

**Позиционные аргументы:**

Аргументы передаются в функцию в том порядке, в котором они определены.

```python
def add(x, y):
    return x + y

print(add(2, 3))  # Вывод: 5
```

**Именованные аргументы:**

Вы можете передавать аргументы по их имени, что делает код более читаемым.

```python
def introduce(name, age):
    return f"My name is {name} and I am {age} years old."

print(introduce(name="Bob", age=25))  # Вывод: My name is Bob and I am 25 years old.
```

**Значения по умолчанию:**

Функции могут иметь аргументы со значениями по умолчанию.

```python
def greet(name="Guest"):
    return f"Hello, {name}!"

print(greet())  # Вывод: Hello, Guest!
```

**Возвращаемые значения:**

Функция может возвращать любое значение или ничего не возвращать (тогда возвращается None).

```python
def square(x):
    return x ** 2

result = square(4)
print(result)  # Вывод: 16
```

### 3. Работа с модулями и пакетами

- **Модули** — это файлы с Python-кодом, которые можно импортировать в другие программы.
- **Пакеты** — это наборы модулей, организованных в каталогах.

**Импорт модулей**

Вы можете импортировать встроенные модули или свои собственные.

```python
import math

# Использование функции из модуля
print(math.sqrt(16))  # Вывод: 4.0
```

**Импорт конкретных функций**

Можно импортировать только определённые функции из модуля.

```python
from math import sqrt

print(sqrt(25))  # Вывод: 5.0
```

**Создание собственного модуля**

Вы можете создавать собственные модули, чтобы структурировать код.

**Для этого создайте файл с расширением `.py`, например, `my_module.py`:**

```python
# my_module.py
def say_hello():
    return "Hello from the module!"
```

**Затем импортируйте и используйте модуль:**

```python
from my_module import say_hello

print(say_hello())  # Вывод: Hello from the module!
```

**Пакеты**

**Пакет** — это каталог, содержащий модули.

Чтобы Python распознавал каталог как пакет, в нём должен быть файл `__init__.py`

```
my_package/
    __init__.py
    module1.py
    module2.py
```

**Вы можете импортировать модули из пакета:**

```python
from my_package import module1

```

### 4. Заключение

На этом уроке вы изучили, как создавать функции, работать с аргументами и возвращаемыми значениями, а также как использовать модули и пакеты.

Это позволяет структурировать ваш код и делать его более организованным и повторно используемым.

В следующем уроке мы рассмотрим работу с массивами и строками.



**Автор:** Дуплей Максим Игоревич

**Дата:** 07.09.2024

**Версия 1.0**