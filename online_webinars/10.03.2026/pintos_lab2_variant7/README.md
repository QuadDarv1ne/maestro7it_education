# Лабораторная работа №2: Планирование процессов в Pintos

## Вариант №7: Round Robin с приоритетным планированием

---

## Содержимое архива

```
pintos_lab2_variant7/
├── threads/
│   ├── thread.h          # Изменённый заголовочный файл (поддержка приоритетов)
│   ├── thread.c          # Реализация приоритетного планирования
│   ├── synch.h           # Заголовочный файл синхронизации
│   └── synch.c           # Реализация priority donation
├── tests/threads/
│   ├── test-new-alg.c    # Основной тест для варианта 7
│   ├── new-alg.c         # Заглушка для системы тестов
│   └── tests-integration.c  # Инструкции по интеграции
├── report/
│   └── Лабораторная_работа_2_Отчёт.docx
├── diagrams/
│   ├── gantt_original.png   # Диаграмма исходного алгоритма
│   ├── gantt_priority.png   # Диаграмма приоритетного планирования
│   ├── comparison_chart.png # Сравнение времени ожидания
│   └── flowchart.png        # Блок-схема алгоритма
└── README.md             # Этот файл
```

---

## Исходные данные варианта №7

| Процесс | CPU Burst | Приоритет |
|---------|-----------|-----------|
| Proc0   | 3         | 27        |
| Proc1   | 8         | 7         |
| Proc2   | 20        | 8         |
| Proc3   | 1         | 18        |

**Алгоритм**: Round Robin с приоритетным планированием

---

## Установка

### Шаг №1: Резервное копирование оригинальных файлов

```bash
cd /path/to/pintos/src/threads
cp thread.h thread.h.orig
cp thread.c thread.c.orig
cp synch.h synch.h.orig
cp synch.c synch.c.orig
```

### Шаг №2: Копирование новых файлов

```bash
# Копирование файлов планировщика
cp /path/to/pintos_lab2_variant7/threads/thread.h .
cp /path/to/pintos_lab2_variant7/threads/thread.c .
cp /path/to/pintos_lab2_variant7/threads/synch.h .
cp /path/to/pintos_lab2_variant7/threads/synch.c .

# Копирование теста
cp /path/to/pintos_lab2_variant7/tests/threads/test-new-alg.c tests/threads/
cp /path/to/pintos_lab2_variant7/tests/threads/new-alg.c tests/threads/
```

### Шаг №3: Интеграция теста в систему

Добавьте в файл `tests/threads/tests.h`:
```c
extern void test_new_alg(void);
```

Добавьте в файл `tests/threads/tests.c` в массив `tests[]`:
```c
{"new-alg", test_new_alg},
```

---

## Запуск тестов

### Тесты приоритетного планирования

```bash
cd /path/to/pintos/src/threads
make tests/threads/alarm-priority.result
make tests/threads/priority-change.result
make tests/threads/priority-fifo.result
make tests/threads/priority-preempt.result
make tests/threads/priority-sema.result
make tests/threads/priority-condvar.result
```

### Тесты priority donation

```bash
make tests/threads/priority-donate-one.result
make tests/threads/priority-donate-lower.result
make tests/threads/priority-donate-multiple.result
make tests/threads/priority-donate-multiple2.result
make tests/threads/priority-donate-sema.result
make tests/threads/priority-donate-nest.result
make tests/threads/priority-donate-chain.result
```

### Запуск теста test-new-alg

```bash
make tests/threads/new-alg.result
```

### Запуск всех тестов

```bash
make check
```

---

## Ожидаемые результаты

### Порядок выполнения процессов (по убыванию приоритета):

1. **Proc0** (приоритет 27) — выполняется первым, 3 тика
2. **Proc3** (приоритет 18) — выполняется вторым, 1 тик
3. **Proc2** (приоритет 8) — выполняется третьим, 20 тиков
4. **Proc1** (приоритет 7) — выполняется последним, 8 тиков

### Общее время выполнения: 32 тика

---

## Ключевые изменения в коде

### thread.h

- Добавлено поле `effective_priority` — эффективный приоритет с учётом donation
- Добавлено поле `donation_list` — список полученных donations
- Добавлено поле `waiting_lock` — замок, который ожидает процесс
- Добавлена структура `struct donation` для отслеживания доноров

### thread.c

- Реализована функция `thread_priority_less()` для сортировки по приоритету
- Модифицирована функция `thread_yield()` для упорядоченной вставки в очередь
- Реализованы функции `donate_priority()`, `remove_donation()`, `remove_all_donations()`
- Модифицирована функция `next_thread_to_run()` для выбора по приоритету

### synch.c

- Модифицирована функция `lock_acquire()` для реализации priority donation
- Модифицирована функция `lock_release()` для отмены donation
- Реализовано приоритетное пробуждение на семафорах и условных переменных

---

## Структура отчёта

1. **Диаграммы исполнения процессов**
   - Для исходного алгоритма Pintos (FIFO)
   - Для приоритетного планирования

2. **Сравнительный анализ диаграмм**
   - Время ожидания процессов
   - Среднее время ожидания
   - Выводы

3. **Блок-схема нового алгоритма планирования**

4. **Описание функций планирования**
   - Таблица с аргументами, возвращаемыми значениями, связями

5. **Исходные коды с комментариями**
   - thread.c, thread.h
   - synch.c, synch.h

6. **Описание тестовых задач**
   - Результаты запуска тестов
   - Анализ результатов

7. **Описание теста test-new-alg**
   - Исходный код
   - Полученный вывод
   - Анализ

---

## Контакты

При возникновении вопросов обращайтесь к преподавателю или в методический кабинет.
