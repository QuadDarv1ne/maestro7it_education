# Анализаторы производительности графики Intel (Intel GPA)

Эта директория должна содержать библиотеки анализа производительности графики Intel для мониторинга графических процессоров Intel.

## Необходимые файлы:
- `IGPA.h` - Заголовочный файл для Intel GPA API
- `igpa.lib` - Статическая библиотека для линковки (Windows)
- `igpa.dll` - Динамическая библиотека (Windows)

## Установка:
1. Скачайте Intel Graphics Performance Analyzers с официального сайта Intel
2. Извлеките файлы Intel GPA в эту директорию
3. Включите поддержку Intel GPA в CMake с помощью флага `-DENABLE_INTEL_GPA=ON`

## Подробная инструкция:
1. Перейдите на сайт разработчика Intel: https://software.intel.com/content/www/us/en/develop/tools/graphics-performance-analyzers.html
2. Скачайте Intel Graphics Performance Analyzers
3. После установки найдите файлы библиотеки в директории установки
4. Скопируйте необходимые файлы в эту директорию

## Документация:
- [Документация Intel Graphics Performance Analyzers](https://software.intel.com/content/www/us/en/develop/tools/graphics-performance-analyzers/documentation.html)
- [Intel GPA User Guide](https://software.intel.com/content/www/us/en/develop/articles/intel-graphics-performance-analyzers-user-guide.html)

## Примечания:
- Для работы Intel GPA требуется поддерживаемый процессор Intel с графикой
- Библиотека работает только с интегрированной графикой Intel
- Может потребоваться регистрация на сайте Intel для скачивания инструментов
- Убедитесь, что используете совместимую версию Intel GPA с вашим оборудованием