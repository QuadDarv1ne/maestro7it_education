# План работ по проекту GPU Lab

## ✅ Выполнено (v1.1.0)

### Исправления
- [x] Исправлена загрузка kernel из файлов (hash.cl, sieve.cl)
  - Добавлена функция `open_kernel_file()` с поиском в нескольких путях
  - Копирование .cl файлов в build директорию через CMake
- [x] Устранено предупреждение deprecated `clCreateCommandQueue`
  - Замена на `clCreateCommandQueueWithProperties` во всех файлах
- [x] Починены unit-тесты
  - Созданы `hashing/sha256.c` и `sieve/sieve_cpu.c` без main()
  - Все 4 теста проходят (100%)
- [x] Добавлены поля в `OpenCLContext` (kernel_sha256, kernel_djb2, kernel_fnv1a)

### Сборка и тесты
- [x] CMake сборка работает (sieve, hash, test_sha256, test_sieve)
- [x] Интеграционные тесты через CTest
- [x] Kernel файлы загружаются из файлов, а не встроенные

---

## 🔧 В работе (dev)

### Критические проблемы
- [ ] **SHA-256 для множественных блоков**
  - Проблема: неправильный хэш для сообщений > 512 бит
  - Тест `test_sha256_very_long()` отключен (#if 0)
  - Требуется: исправить логику обработки множественных блоков в `sha256_cpu()`
  - Файлы: `hashing/sha256.c`, `hashing/hash.c`

### Предупреждения компиляции
- [ ] `cl_version.h: CL_TARGET_OPENCL_VERSION is not defined`
  - Решение: добавить `#define CL_TARGET_OPENCL_VERSION 300` перед включением CL/cl.h
  - Файлы: все .c файлы с OpenCL
- [ ] `snprintf output may be truncated` в `cl_utils.c`
  - Функция `open_kernel_file()`, строки 403, 408
  - Решение: увеличить буфер или использовать динамическое выделение
- [ ] `unused variable 'g_is_prime'` в `sieve.c:519`
  - Удалить неиспользуемую переменную
- [ ] `pointer 'h_primes' may be used after 'free'` в `sieve.c:418`
  - Переместить free() после использования

---

## 📋 Запланировано

### Оптимизации
- [ ] Исправить `sha256_hash_optimized()` в `hash.cl`
  - Настройка размера локальной памяти
  - Тестирование производительности с разными work-group sizes
- [ ] Добавить бенчмарки для сравнения оптимизированного и обычного kernel
- [ ] Профилирование GPU kernel для выявления узких мест

### Тесты
- [ ] Включить тест `test_sha256_very_long()` после исправления
- [ ] Добавить тесты для DJB2, FNV-1a, MurmurHash
- [ ] Интеграционные тесты в CI/CD (GitHub Actions)
- [ ] Тесты на утечки памяти (valgrind, AddressSanitizer)

### Документация
- [ ] Обновить README с инструкциями по сборке через CMake
- [ ] Добавить раздел "Известные проблемы" в README
- [ ] Документировать API общих функций (cl_common.h)

### Рефакторинг
- [ ] Вынести функции из hash.c для тестов (hash_all_cpu, etc.)
- [ ] Создать отдельный модуль для SHA-256 (sha256.h + sha256.c)
- [ ] Убрать дублирование кода между hash.c и sha256.c

---

## 🚀 Долгосрочные цели

### Производительность
- [ ] Поддержка OpenCL 3.0 features
- [ ] Асинхронные вычисления (multiple command queues)
- [ ] Zero-copy память между CPU и GPU
- [ ] Групповая обработка данных (batch processing)

### Функциональность
- [ ] Дополнительные алгоритмы:
  - [ ] Сортировка на GPU
  - [ ] Поиск в ширину/глубину
  - [ ] Матричные операции
- [ ] Поддержка нескольких GPU одновременно
- [ ] Динамический выбор устройства (CPU/GPU) на основе размера задачи

### Инфраструктура
- [ ] Docker образ для сборки и тестирования
- [ ] Pre-built бинарники для Windows/Linux/macOS
- [ ] Пакетный менеджер (vcpkg, conan)
- [ ] Непрерывная интеграция с тестами на GPU (self-hosted runners)

---

## 📊 Статистика

| Категория | Выполнено | В работе | Запланировано |
|-----------|-----------|----------|---------------|
| Критические баги | 3 | 1 | 0 |
| Предупреждения | 1 | 4 | 0 |
| Тесты | 4 | 0 | 3 |
| Оптимизации | 0 | 0 | 3 |
| Документация | 1 | 0 | 3 |

**Всего:** 9 ✅ | 5 🔧 | 9 📋

---

## 📝 Заметки

### Сборка через CMake (рекомендуется)
```bash
mkdir build && cd build
cmake .. -DOpenCL_INCLUDE_DIR=/path/to/opencl/include \
         -DOpenCL_LIBRARY=/path/to/opencl/lib
cmake --build .
ctest --verbose
```

### Сборка через Makefile
```bash
# Hash
cd hashing && make && ./hash

# Sieve
cd sieve && make && ./sieve

# Tests
cd tests && make run
```

### Запуск тестов
```bash
cd build
ctest --verbose
# или
ctest -R SHA256  # конкретный тест
```

### Известные ограничения
- SHA-256 для сообщений > 512 бит требует исправления
- В CI/CD тесты выполняются только на CPU (нет GPU)
- Windows: требуется shlwapi.lib для PathRemoveFileSpecA

---

**Последнее обновление:** 2026-03-19
**Версия:** 1.1.0
**Статус:** v1.1.0 готов к merge в main
