# C++ Debug Pro Template - Полная настройка отладки C++ в VS Code

**Этот шаблон предоставляет готовую конфигурацию для профессиональной отладки C++ проектов с поддержкой:**

- Отладка через `GDB (MinGW)` с расширенными возможностями
- Интеграция с `MSVC (Visual Studio)`
- Автоматическое определение компиляторов
- Поддержка кириллицы и `UTF-8`
- Кастомные визуализаторы данных

## Быстрый старт

1. Склонируйте репозиторий или создайте папку проекта
2. Поместите содержимое `.vscode` в папку вашего проекта
3. **Установите зависимости:**
   - **Для MinGW:** `https://winlibs.com/` (выберите `x86_64-posix-seh`)
   - **Для MSVC:** Установите `Desktop development with C++` в `Visual Studio`

## Структура проекта

```testline
cpp-advanced-debug-template/
 │
 ├── .vscode/
 │   ├── launch.json                       # Конфигурации отладки
 │   ├── tasks.json                        # Система сборки
 │   ├── settings.json                     # Настройки среды
 │   └── extensions.json                   # Рекомендуемые расширения
 │
 ├── .gdbinit                              # Пользовательские команды GDB
 ├── README-note.md
 └── example.cpp (опционально, пример кода)
```

## Основные возможности

### Для MinGW/GDB

- Расширенная визуализация STL-контейнеров
- Поддержка дизассемблирования
- Сетевая отладка через `gdbserver`
- Автоочистка временных файлов

### Для MSVC

- Интеграция с компилятором `cl.exe`
- Внешняя консоль для корректного вывода
- Поддержка многопоточности

### Универсальные

- Автовыбор компилятора при запуске
- Поддержка кириллических путей
- Генерация ассемблерного кода (`Ctrl+Shift+B` → `Generate Assembly`)

## Горячие клавиши

| Команда                | Горячие клавиши    | Описание                          |
 |------------------------|-------------------|-----------------------------------|
 | Запуск отладки         | `F5`             | Запуск основной конфигурации      |
 | Сборка проекта         | `Ctrl+Shift+B`   | Компиляция текущего файла         |
 | Показать точки останова| `Ctrl+Shift+D`   | Открыть панель отладки            |
 | Открыть консоль GDB    | `Ctrl+Shift+Y`   | Показать консоль отладчика        |
 | Генерация ассемблера   | `Ctrl+Shift+P → Tasks: Run Task → Generate Assembly` | Создать .asm файл |

## Расширенные функции GDB

### Пользовательские команды (ввести в консоли GDB)

- `asm`: Переключиться на ассемблерное представление
- `src`: Вернуться к исходному коду
- `vector_print [имя]`: Красивый вывод `std::vector`
- `mem_view [адрес] [размер]`: Просмотр памяти в `hex`

### Кастомные визуализаторы

- `std::vector`
- `std::map`
- `std::string` (поддержка `UTF-8`)
- Пользовательские структуры (через `.natvis`)

## Решение проблем

### Если g++ не распознан

1. Проверьте установку `MinGW`
2. **Выполните в терминале:** `g++ --version`
3. Добавьте путь к `bin` в системный `PATH`
4. **В `settings.json` укажите полный путь:**

   ```json
   "cpp.compilerPath": "C:/mingw64/bin/g++.exe",
   "cpp.debuggerPath": "C:/mingw64/bin/gdb.exe"
   ```

### Если cl.exe недоступен

1. Запустите `VS Code` через `Developer Command Prompt`
2. Проверьте установку `C++` компонентов в `Visual Studio`
3. **Вручную вызовите:** `cl /?`

### Проблемы с кириллицей

Добавьте в `tasks.json`:

```json
"options": {
    "env": {
        "PYTHONIOENCODING": "utf8",
        "LANG": "C.UTF-8"
    }
}
```

### Отладка многопоточных приложений

В `.gdbinit` добавьте:

```textline
set non-stop on
set target-async on
```

## Расширенные возможности

1. **Сетевая отладка**:

   ```bash
   # На удаленной машине:
   gdbserver :1234 ./program

   # В launch.json:
   "debugServerPath": "gdbserver",
   "debugServerArgs": "localhost:1234"
   ```

2. **Визуализация структур**:
   Создайте файл `.natvis`:

   ```xml
   <AutoVisualizer>
     <Type Name="MyStruct">
       <DisplayString>{{x={x}, y={y}}}</DisplayString>
     </Type>
   </AutoVisualizer>
   ```

3. **Анализ памяти**:
   Используйте встроенную Memory View (Ctrl+Shift+Y → View Memory)

## Рекомендуемые расширения

- [C/C++ (Microsoft)](https://marketplace.visualstudio.com/items?itemName=ms-vscode.cpptools)
- [GDB Debug (WebFreak)](https://marketplace.visualstudio.com/items?itemName=webfreak.debug)
- [Memory View](https://marketplace.visualstudio.com/items?itemName=VisualStudioExptTeam.vscodeintellicode)
- [CMake Tools](https://marketplace.visualstudio.com/items?itemName=ms-vscode.cmake-tools)

---

### 📄 Лицензия

[Этот проект лицензирован под лицензией MIT](LICENCE)

Для получения дополнительной информации ознакомьтесь с файлом `LICENSE`

---

💼 **Автор:** Дуплей Максим Игоревич

📲 **Telegram:** @quadd4rv1n7

📅 **Дата:** 28.07.2025

▶️ **Версия 1.0**

```textline
※ Предложения по сотрудничеству можете присылать на почту ※
📧 maksimqwe42@mail.ru
```
