# Библиотека управления NVIDIA (NVML)

Эта директория должна содержать файлы NVIDIA Management Library (NVML) для мониторинга графических процессоров NVIDIA.

## Необходимые файлы:
- `nvml.h` - Заголовочный файл для NVML API
- `nvml.lib` - Статическая библиотека для линковки (Windows)
- `nvml.dll` - Динамическая библиотека (Windows)

## Установка:
1. Скачайте драйверы NVIDIA GPU или CUDA Toolkit с официального сайта NVIDIA
2. Извлеките файлы NVML в эту директорию
3. Включите поддержку NVML в CMake с помощью флага `-DENABLE_NVML=ON`

## Подробная инструкция:
1. Перейдите на сайт разработчика NVIDIA: https://developer.nvidia.com/cuda-toolkit
2. Скачайте CUDA Toolkit (в состав входит NVML)
3. После установки найдите файлы библиотеки:
   - Заголовочные файлы обычно находятся в: `C:\Program Files\NVIDIA GPU Computing Toolkit\CUDA\v[версия]\include\nvml.h`
   - Библиотеки обычно находятся в: `C:\Program Files\NVIDIA GPU Computing Toolkit\CUDA\v[версия]\lib\x64\`
4. Скопируйте файлы в эту директорию

## Документация:
- [Документация NVIDIA Management Library](https://docs.nvidia.com/deploy/nvml-api/)
- [CUDA Toolkit Documentation](https://docs.nvidia.com/cuda/)

## Примечания:
- Убедитесь, что у вас установлены последние драйверы NVIDIA
- Для работы NVML требуется поддерживаемая видеокарта NVIDIA
- Библиотека работает только на устройствах NVIDIA