# Руководство для контрибьюторов

Спасибо за интерес к проекту "Вычисления на GPU с OpenCL"

Это руководство поможет вам внести свой вклад в развитие проекта.

## 📋 Содержание

- [Как внести вклад](#как-внести-вклад)
- [Стандарты кода](#стандарты-кода)
- [Процесс разработки](#процесс-разработки)
- [Тестирование](#тестирование)
- [Документирование](#документирование)

---

## 🔧 Как внести вклад

### 1. Сообщение об ошибке

Если вы нашли баг, создайте issue с меткой `bug`:

- **Заголовок**: Краткое описание проблемы
- **Описание**: 
  - Шаги для воспроизведения
  - Ожидаемое поведение
  - Фактическое поведение
  - Версия проекта
  - ОС и оборудование (GPU)
  - Логи ошибок

### 2. Предложение функции

Для новой функции создайте issue с меткой `enhancement`:

- **Заголовок**: Название функции
- **Описание**:
  - Зачем нужна эта функция
  - Примеры использования
  - Возможные проблемы реализации

### 3. Pull Request

#### Перед отправкой PR:

```bash
# 1. Создайте fork и клонируйте
git clone https://github.com/YOUR_USERNAME/gpu-lab.git
cd gpu-lab

# 2. Создайте ветку для изменений
git checkout -b feature/your-feature-name

# 3. Внесите изменения и отформатируйте код
clang-format -i hashing/hash.c sieve/sieve.c src/cl_utils.c

# 4. Запустите тесты
mkdir build && cd build
cmake .. -DBUILD_TESTS=ON
cmake --build .
ctest --verbose

# 5. Запустите бенчмарки (опционально)
../scripts/benchmark.sh all

# 6. Закоммитьте изменения
git add .
git commit -m "feat: описание изменений"

# 7. Отправьте и создайте PR
git push origin feature/your-feature-name
```

---

## 📐 Стандарты кода

### Стиль кода

Проект использует `.clang-format` для автоматического форматирования:

```bash
# Форматирование одного файла
clang-format -i file.c

# Форматирование всех C файлов
find . -name "*.c" -o -name "*.h" | xargs clang-format -i
```

### Основные правила

```c
// 1. Отступы: 4 пробела (не табы)
void function() {
    int x = 5;  // 4 пробела
}

// 2. Максимальная длина строки: 100 символов
// 3. Имена функций: snake_case
void calculate_sha256_hash(...);

// 4. Имена типов: PascalCase
typedef struct { ... } OpenCLContext;

// 5. Константы: UPPER_SNAKE_CASE
#define MAX_BUFFER_SIZE 0x100000

// 6. Макросы с осторожностью
#define SAFE_FREE(ptr) do { if (ptr) { free(ptr); ptr = NULL; } } while(0)

// 7. Проверка ошибок
cl_int err = clCreateBuffer(...);
if (err != CL_SUCCESS) {
    fprintf(stderr, "Ошибка: %s\n", cl_get_error_string(err));
    return -1;
}

// 8. Комментарии к функциям (Doxygen стиль)
/**
 * @brief Краткое описание функции
 * 
 * @param param1 Описание параметра
 * @return Описание возвращаемого значения
 */
int function(int param1);
```

### Обработка ошибок

```c
// ✅ Правильно: использование макросов
CHECK_CL_ERROR_RET(err, "clCreateBuffer", -1);
CHECK_ALLOC_RET(ptr, size, NULL);
SAFE_FREE(ptr);

// ❌ Неправильно: игнорирование ошибок
clCreateBuffer(...);  // Нет проверки!
free(ptr);  // Может быть NULL
```

---

## 🔄 Процесс разработки

### Ветвление

- `main` — основная стабильная ветка
- `develop` — ветка разработки
- `feature/*` — новые функции
- `bugfix/*` — исправления ошибок
- `hotfix/*` — срочные исправления

### Коммиты

Используйте [Conventional Commits](https://www.conventionalcommits.org/):

```
feat: добавлена поддержка SHA-512
fix: исправлена утечка памяти в sieve_gpu
docs: обновлена документация API
refactor: рефакторинг обработки ошибок
test: добавлены интеграционные тесты
chore: обновлены зависимости
```

### Code Review

Все PR проходят code review:

1. Проверка стиля кода (clang-format)
2. Проверка тестов (ctest)
3. Проверка документации
4. Минимум 1 approval от maintainer

---

## 🧪 Тестирование

### Запуск тестов

```bash
# Все тесты
cd build && ctest --verbose

# Конкретный тест
ctest -R SHA256 --verbose

# С выводом результатов
ctest --output-on-failure
```

### Добавление тестов

Новые тесты добавляйте в `tests/`:

```c
/* tests/test_your_feature.c */
#include "test_common.h"

void test_your_feature(void) {
    TEST_BEGIN("Описание теста");
    
    // Arrange
    int value = setup_test_data();
    
    // Act
    int result = your_function(value);
    
    // Assert
    TEST_ASSERT_EQUAL(expected, result, "Описание проверки");
    
    TEST_END();
}

int main(void) {
    test_your_feature();
    test_summary();
    return (test_failures > 0) ? 1 : 0;
}
```

### Покрытие тестами

Целевое покрытие: **>70%** для новых функций.

```bash
# Генерация отчёта о покрытии (gcc)
gcc --coverage -o test test.c
./test
gcov test.c
```

---

## 📚 Документирование

### Doxygen комментарии

```c
/**
 * @file your_file.h
 * @brief Краткое описание файла
 */

/**
 * @brief Краткое описание функции
 * 
 * Подробное описание функции, включая
 * алгоритм работы и ограничения.
 * 
 * @param input Входные данные
 * @param len Длина данных
 * @param output Выходной буфер
 * 
 * @return CL_SUCCESS при успехе
 * @return CL_ERROR при ошибке
 * 
 * @see related_function()
 * 
 * @example
 * uint8_t hash[32];
 * sha256_hash(data, len, hash);
 */
int sha256_hash(const uint8_t* input, size_t len, uint8_t* output);
```

### Генерация документации

```bash
# Установка doxygen
sudo apt install doxygen graphviz

# Генерация
doxygen Doxyfile

# Просмотр
firefox html/index.html
```

---

## 📦 Область contributions

### Приоритетные направления

| Направление | Описание | Сложность |
|-------------|----------|-----------|
| **Оптимизация kernel'ов** | Улучшение производительности GPU kernel'ов | 🔴 Высокая |
| **Новые алгоритмы** | Добавление новых хэш-функций, алгоритмов | 🟡 Средняя |
| **Тестирование** | Написание unit/integration тестов | 🟢 Низкая |
| **Документация** | Улучшение документации, примеры | 🟢 Низкая |
| **CI/CD** | Улучшение workflow, новые проверки | 🟡 Средняя |

### Идеи для contributions

1. **BLAKE2/BLAKE3 kernel** — современные хэш-функции
2. **Argon2 kernel** — password hashing
3. **Segmented Sieve** — для N > 10^9
4. **OpenCL 3.0 features** — использование новых возможностей
5. **Benchmark automation** — автоматические бенчмарки в CI
6. **Cross-platform testing** — тесты на разных GPU

---

## 🤝 Связь

- **Issues**: Для багов и предложений
- **Discussions**: Для вопросов и обсуждений
- **Email**: Для личных вопросов

---

## 📜 Лицензия

Внося изменения, вы соглашаетесь с лицензией проекта.

---

## 🏆 Contributors

Спасибо всем контрибьюторам!

<!-- Список будет обновляться автоматически через GitHub API -->

---

**Спасибо за ваш вклад! 🎉**
