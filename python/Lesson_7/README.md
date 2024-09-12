# Работа с файлами и ввод/вывод в Python

Python предлагает простой и удобный способ работы с файлами, включая чтение, запись и обработку ошибок.

Рассмотрим основные моменты.

### 1. Чтение и запись файлов

**Файлы можно открывать в различных режимах:** чтение, запись, добавление и другие.

Для этого используется функция `open()`.

**Основные режимы открытия файлов:**

- 'r' — чтение (по умолчанию)
- 'w' — запись (перезаписывает файл)
- 'a' — добавление (добавляет в конец файла)
- 'b' — бинарный режим (для работы с файлами не в текстовом формате)
- 'x' — создание нового файла (если файл существует, возникает ошибка)

**Пример чтения файла:**
```python
# Открытие файла и чтение всех строк
with open('example.txt', 'r', encoding='utf-8') as file:
    content = file.read()  # Чтение всего содержимого файла
    print(content)
```

- **Чтение построчно:**
```python
with open('example.txt', 'r', encoding='utf-8') as file:
    for line in file:
        print(line.strip())  # strip() удаляет символы новой строки
```

**Пример записи в файл:**
```pytnon
# Открытие файла для записи
with open('output.txt', 'w', encoding='utf-8') as file:
    file.write("Привет, мир!\n")  # Запись строки в файл
    file.write("Это вторая строка.\n")
```

- **Добавление в файл:**
```python
with open('output.txt', 'a', encoding='utf-8') as file:
    file.write("Добавляю еще одну строку.\n")
```

### 2. Работа с CSV-файлами

Модуль csv позволяет легко работать с CSV-файлами (`Comma-Separated Values`, значения, разделённые запятыми).

- **Чтение CSV-файла:**
```python
import csv

with open('data.csv', 'r', encoding='utf-8') as csvfile:
    reader = csv.reader(csvfile)
    for row in reader:
        print(row)  # Каждая строка — это список
```

- **Запись в CSV-файл:**
```python
import csv

data = [
    ['Name', 'Age', 'City'],
    ['Alice', 30, 'New York'],
    ['Bob', 25, 'Los Angeles']
]

with open('output.csv', 'w', newline='', encoding='utf-8') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerows(data)
```

**Чтение и запись CSV с использованием `DictReader` и `DictWriter`:** Эти классы работают с CSV-файлами как со словарями, где заголовки столбцов становятся ключами.

- **Чтение с `DictReader`:**
```python
import csv

with open('data.csv', 'r', encoding='utf-8') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        print(row)  # Каждая строка — это словарь
```

- **Запись с `DictWriter`:**
```
import csv

data = [
    {'Name': 'Alice', 'Age': 30, 'City': 'New York'},
    {'Name': 'Bob', 'Age': 25, 'City': 'Los Angeles'}
]

with open('output.csv', 'w', newline='', encoding='utf-8') as csvfile:
    fieldnames = ['Name', 'Age', 'City']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    
    writer.writeheader()  # Запись заголовков
    writer.writerows(data)
```

### 3. Обработка ошибок ввода/вывода

**При работе с файлами часто могут возникать ошибки:** файл может не существовать, или доступ может быть ограничен.

Для таких ситуаций в Python используются конструкции `try-except`.

**Пример обработки ошибок:**
```python
try:
    with open('non_existent_file.txt', 'r', encoding='utf-8') as file:
        content = file.read()
except FileNotFoundError:
    print("Файл не найден.")
except IOError:
    print("Ошибка ввода/вывода.")
```

**Типичные ошибки при работе с файлами:**
- `FileNotFoundError` — файл не существует.
- `PermissionError` — недостаточно прав для доступа к файлу.
- `IOError` — общая ошибка ввода/вывода.

### Выводы

Python делает работу с файлами простой и удобной благодаря использованию контекстных менеджеров (with), обеспечивая автоматическое закрытие файла после работы с ним.

Модуль csv облегчает работу с данными в табличном формате, а использование исключений позволяет обработать возможные ошибки при работе с файлами.



**Автор:** Дуплей Максим Игоревич

**Дата:** 07.09.2024

**Версия 1.0**