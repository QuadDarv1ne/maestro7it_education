# Скрипты сборки PCMetrics

## Автоматическая сборка

Проект включает два скрипта для автоматической сборки:

### Windows (PowerShell)

```powershell
.\build_project.bat
```

Этот скрипт:
1. Создает директорию build (если не существует)
2. Генерирует файлы проекта с помощью CMake
3. Компилирует проект
4. Выводит результаты сборки

### Linux/macOS (Bash)

```bash
chmod +x build_project.sh
./build_project.sh
```

## Ручная сборка

Если вы предпочитаете ручную сборку:

```powershell
# Создать директорию build
mkdir build
cd build

# Генерация проекта
cmake ..

# Сборка
cmake --build .

# Запуск
.\bin\pcmetrics.exe
```

## Опции сборки

### Release сборка

```powershell
cmake -DCMAKE_BUILD_TYPE=Release ..
cmake --build . --config Release
```

### Debug сборка (по умолчанию)

```powershell
cmake -DCMAKE_BUILD_TYPE=Debug ..
cmake --build . --config Debug
```

### С поддержкой NVIDIA GPU

```powershell
cmake -DENABLE_NVML=ON ..
```

### С поддержкой AMD GPU

```powershell
cmake -DENABLE_ADL=ON ..
```

### С поддержкой Intel GPU

```powershell
cmake -DENABLE_INTEL_GPA=ON ..
```

## Очистка сборки

Для полной очистки и пересборки:

```powershell
# Удалить директорию build
Remove-Item -Recurse -Force build

# Пересобрать
mkdir build
cd build
cmake ..
cmake --build .
```

## Решение проблем

### Ошибка: CMake не найден

Установите CMake с [официального сайта](https://cmake.org/download/)

### Ошибка: Компилятор не найден

- **Windows**: Установите Visual Studio или MinGW
- **Linux**: Установите GCC (`sudo apt install build-essential`)
- **macOS**: Установите Xcode Command Line Tools

### Ошибка: PDH библиотека не найдена

PDH входит в Windows SDK. Убедитесь, что установлен Windows SDK.

### Предупреждения о кодировке

Это нормально, проект использует UTF-8 для русских символов.

## Дополнительная информация

Для более подробной информации см.:
- [BUILD_GUIDE.md](docs/BUILD_GUIDE.md) - Полное руководство по сборке (русский)
- [BUILD_GUIDE_EN.md](docs/BUILD_GUIDE_EN.md) - Build Guide (English)
- [CONTRIBUTING.md](CONTRIBUTING.md) - Руководство для разработчиков
