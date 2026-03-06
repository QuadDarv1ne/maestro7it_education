# Сборка проекта с Ninja

## Установка Ninja

Ninja уже включен в репозиторий в папке `.tools/ninja/`.

**Версия:** Ninja 1.13.2

## Быстрый старт

### Windows (PowerShell / CMD)

```powershell
# Создание папки сборки
mkdir build
cd build

# Конфигурация с Ninja
cmake .. -G Ninja -DCMAKE_BUILD_TYPE=Debug

# Сборка
cmake --build .

# Запуск тестов
.\tests.exe
```

### Команды для разных конфигураций

```powershell
# Debug сборка
cmake .. -G Ninja -DCMAKE_BUILD_TYPE=Debug
cmake --build .

# Release сборка
cmake .. -G Ninja -DCMAKE_BUILD_TYPE=Release
cmake --build .

# Очистка и пересборка
rm -r *
cmake .. -G Ninja -DCMAKE_BUILD_TYPE=Debug
cmake --build .
```

## Преимущества Ninja

- **Быстрая сборка** — параллельное выполнение задач по умолчанию
- **Инкрементальная сборка** — пересобирает только измененные файлы
- **Меньше вывод** — чистый и понятный вывод в консоль
- **Кроссплатформенный** — работает на Windows, Linux, macOS

## Структура проекта

```
university-exercises-dupleymi/
├── .tools/ninja/          # Ninja build system
├── CMakeLists.txt         # Корневой CMake
├── docs/
│   └── ninja.md           # Эта документация
└── ITMO University/
    └── 7_task_scheduler_project/
        ├── CMakeLists.txt
        ├── task_scheduler.hpp
        ├── task_scheduler.cpp
        └── tests.cpp
```

## Альтернативные генераторы

Если Ninja недоступен, можно использовать стандартные генераторы:

```powershell
# MinGW Makefiles
cmake .. -G "MinGW Makefiles" -DCMAKE_BUILD_TYPE=Debug
cmake --build .

# Visual Studio (Windows)
cmake .. -G "Visual Studio 17 2022"
cmake --build . --config Debug
```

## Переменные окружения

Для использования Ninja из любой папки добавьте в PATH:

```powershell
$env:Path += ";C:\Users\maksi\OneDrive\Documents\GitHub\university-exercises-dupleymi\.tools\ninja"
```

Или используйте полный путь к исполняемому файлу:

```powershell
cmake .. -G Ninja -DCMAKE_MAKE_PROGRAM="C:\Users\maksi\OneDrive\Documents\GitHub\university-exercises-dupleymi\.tools\ninja\ninja.exe"
```
