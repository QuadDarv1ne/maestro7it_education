# Обработка строк и регулярные выражения в Python

Python предоставляет мощные возможности для работы со строками и поддержки регулярных выражений.

Ниже рассмотрим основные операции с ними.

### 1. Основные операции со строками

**Строки в Python** — это неизменяемые последовательности символов.

**Основные операции со строками:**

- **Создание строки:**

```python
my_string = "Привет, мир!"
```

- **Конкатенация строк (объединение):**

```python
new_string = my_string + " Как дела?"  # "Привет, мир! Как дела?"
```

- **Повторение строки:**

```python
repeated = "Привет " * 3  # "Привет Привет Привет "
```

- **Доступ к символам по индексу:**

```python
first_letter = my_string[0]  # 'П'
last_letter = my_string[-1]  # '!'
```

- **Срезы строк:**

```python
substring = my_string[0:6]  # "Привет"
```

- **Длина строки:**

```python
length = len(my_string)  # 12
```

- **Проверка наличия подстроки:**

```python
Копировать код
result = "мир" in my_string  # True
```

- **Изменение регистра:**

```python
lower = my_string.lower()  # "привет, мир!"
upper = my_string.upper()  # "ПРИВЕТ, МИР!"
```

- **Удаление пробелов:**

```python
stripped = "  текст с пробелами  ".strip()  # "текст с пробелами"
```

- **Разделение строки на части:**

```python
words = my_string.split()  # ['Привет,', 'мир!']
```

- **Соединение списка строк:**

```python
joined = " ".join(['Привет', 'мир'])  # "Привет мир"
```

### 2. Форматирование строк

Форматирование позволяет вставлять значения в строку с помощью специальных синтаксисов.

**Метод `format`:**

```python
name = "Алиса"
age = 25
greeting = "Меня зовут {}, мне {} лет".format(name, age)
# "Меня зовут Алиса, мне 25 лет"
```

**`F-строки (Python 3.6+)`:**

```python
greeting = f"Меня зовут {name}, мне {age} лет"
# "Меня зовут Алиса, мне 25 лет"
```

**Форматирование с указанием ширины, точности:**

```python
pi = 3.14159
formatted_pi = f"Число Пи: {pi:.2f}"  # "Число Пи: 3.14"
```

### 3. Введение в регулярные выражения

**Регулярные выражения (`regular expressions`, или `regex`)** — это мощный инструмент для поиска и манипуляции с текстом по шаблону.

Чтобы работать с регулярными выражениями в Python, используется модуль `re`.

- **Импорт модуля re:**

```python
import re
```

- **Поиск по шаблону:** Метод `search` находит первое совпадение в строке.

```python
pattern = r"\d+"  # Шаблон для поиска одной или более цифр
result = re.search(pattern, "У меня 3 яблока")
if result:
    print(result.group())  # "3"
```

- **Метод `findall` — находит все совпадения:**

```python
result = re.findall(r"\d+", "У меня 3 яблока и 5 груш")
print(result)  # ['3', '5']
```

- **Метод `sub` — замена по шаблону:**

```python
result = re.sub(r"\d+", "X", "Мой номер 12345")  # "Мой номер X"

- **Пример использования регулярных выражений для проверки email:**

```python
email_pattern = r"[^@]+@[^@]+\.[^@]+"
email = "example@example.com"
if re.match(email_pattern, email):
    print("Email корректен")
else:
    print("Неверный формат email")
```

### Заключение

Python предоставляет простые и мощные инструменты для работы со строками, начиная от базовых операций и заканчивая сложными шаблонами с использованием регулярных выражений.



**Автор:** Дуплей Максим Игоревич

**Дата:** 07.09.2024

**Версия 1.0**