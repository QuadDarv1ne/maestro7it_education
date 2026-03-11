#ifndef THREADS_THREAD_H
#define THREADS_THREAD_H

#include <debug.h>
#include <list.h>
#include <stdint.h>

/**
 * @file thread.h
 * @brief Управление потоками и планирование в Pintos
 * 
 * Этот файл содержит определения и объявления функций для:
 * - Создания и управления потоками
 * - Приоритетного планирования
 * - Priority donation (передачи приоритета)
 * 
 * @author Студент
 * @version 1.0
 * @date 2024
 */

/**
 * @brief Статусы процессов
 * 
 * Определяет возможные состояния потока в системе планирования.
 */
enum thread_status
  {
    THREAD_RUNNING,     /**< Выполняется в данный момент */
    THREAD_READY,       /**< Готов к выполнению, ожидает в очереди */
    THREAD_BLOCKED,     /**< Заблокирован (ожидает ресурса) */
    THREAD_DYING        /**< Завершается, будет удалён */
  };

/**
 * @name Приоритеты процессов
 * @brief Диапазон приоритетов: от 0 (минимальный) до 63 (максимальный)
 * @{
 */
#define PRI_MIN 0                       /**< Минимальный приоритет */
#define PRI_MAX 63                      /**< Максимальный приоритет */
#define PRI_DEFAULT 31                  /**< Приоритет по умолчанию */
/** @} */

/**
 * @brief Структура для отслеживания доноров приоритета
 * 
 * Используется для реализации priority donation:
 * когда поток с высоким приоритетом ожидает замок,
 * его приоритет передаётся владельцу замка.
 */
struct donation
  {
    int priority;                       /**< Приоритет донора */
    struct thread *donor;               /**< Указатель на поток-донор */
    struct lock *lock;                  /**< Замок, на котором основана donation */
    struct list_elem elem;              /**< Элемент списка */
  };

/**
 * @brief Структура процесса (thread)
 * 
 * Содержит всю информацию о потоке: состояние, приоритет,
 * стек, списки для планирования и priority donation.
 */
struct thread
  {
    /* Владелец ядра */
    tid_t tid;                          /**< Идентификатор процесса */
    enum thread_status status;          /**< Статус процесса */
    char name[16];                      /**< Имя процесса (для отладки) */
    uint8_t *stack;                     /**< Указатель на стек */
    
    /**
     * @name Приоритеты
     * @{
     */
    int priority;                       /**< Базовый приоритет */
    int effective_priority;             /**< Эффективный приоритет (с учётом donation) */
    /** @} */
    
    /**
     * @name Priority donation
     * @{
     */
    struct list donation_list;          /**< Список полученных donations */
    struct lock *waiting_lock;          /**< Замок, который ожидает процесс */
    /** @} */
    
    /* Общие поля */
    struct list_elem allelem;           /**< Элемент списка всех процессов */
    struct list_elem elem;              /**< Элемент списка ready/других списков */

#ifdef USERPROG
    /* Владелец пользовательской программы */
    struct process *process;            /**< Родительский процесс */
    struct list children;               /**< Список дочерних процессов */
    struct list_elem childelem;         /**< Элемент списка дочерних процессов */
#endif

    /**
     * @name Планирование
     * @{
     */
    int64_t sleep_ticks;                /**< Тики до пробуждения (для timer_sleep) */
    struct list_elem sleep_elem;        /**< Элемент списка спящих процессов */
    int cpu_burst;                      /**< Оставшееся время CPU burst (для теста) */
    /** @} */
    
#ifdef FILESYS
    unsigned magic;                     /**< Магическое число для обнаружения повреждения стека */
#endif
  };

/**
 * @name Функции работы с процессами
 * @{
 */

/**
 * @brief Инициализация системы процессов
 * 
 * Должна быть вызвана один раз при запуске системы.
 * Инициализирует списки потоков и создаёт начальный поток.
 */
void thread_init (void);

/**
 * @brief Запуск планировщика
 * 
 * Создаёт idle поток и включает прерывания.
 */
void thread_start (void);

/**
 * @brief Обработка тика таймера
 * 
 * Вызывается при каждом прерывании таймера.
 * Обновляет статистику и проверяет спящие потоки.
 */
void thread_tick (void);

/**
 * @brief Вывод статистики потоков
 */
void thread_print_stats (void);
/** @} */

/**
 * @name Создание и управление процессами
 * @{
 */

/**
 * @brief Тип функции потока
 */
typedef void thread_func (void *aux);

/**
 * @brief Создание нового потока
 * 
 * @param name Имя потока (для отладки)
 * @param priority Приоритет потока (PRI_MIN..PRI_MAX)
 * @param function Функция, которую будет выполнять поток
 * @param aux Аргумент для функции
 * @return ID потока или TID_ERROR при ошибке
 */
tid_t thread_create (const char *name, int priority, thread_func *, void *);

/**
 * @brief Блокировка текущего потока
 */
void thread_block (void);

/**
 * @brief Разблокировка потока
 * 
 * @param t Поток для разблокировки
 */
void thread_unblock (struct thread *);

/**
 * @brief Получение текущего потока
 * @return Указатель на текущий поток
 */
struct thread *thread_current (void);

/**
 * @brief Получение ID текущего потока
 * @return ID текущего потока
 */
tid_t thread_tid (void);

/**
 * @brief Получение имени текущего потока
 * @return Имя текущего потока
 */
const char *thread_name (void);

/**
 * @brief Завершение текущего потока
 */
void thread_exit (void) NO_RETURN;

/**
 * @brief Освобождение процессора текущим потоком
 */
void thread_yield (void);
/** @} */

/**
 * @name Функции работы с приоритетом
 * @{
 */

/**
 * @brief Получение базового приоритета текущего потока
 * @return Базовый приоритет
 */
int thread_get_priority (void);

/**
 * @brief Установка базового приоритета текущего потока
 * 
 * @param new_priority Новый приоритет (PRI_MIN..PRI_MAX)
 * 
 * Может вызвать вытеснение, если приоритет понизился
 * и есть готовые потоки с более высоким приоритетом.
 */
void thread_set_priority (int);

/**
 * @brief Получение эффективного приоритета потока
 * 
 * @param t Поток
 * @return Эффективный приоритет (максимум из базового и donations)
 */
int thread_get_effective_priority (struct thread *);

/**
 * @brief Обновление эффективного приоритета потока
 * 
 * @param t Поток для обновления
 * 
 * Пересчитывает эффективный приоритет на основе
 * базового приоритета и полученных donations.
 */
void thread_update_effective_priority (struct thread *);
/** @} */

/**
 * @name Функции для priority donation
 * @{
 */

/**
 * @brief Передача приоритета от донора получателю
 * 
 * @param donor Поток, передающий приоритет
 * @param recipient Поток-получатель
 * @param lock Замок, вызвавший donation
 * 
 * Реализует механизм priority donation для предотвращения
 * инверсии приоритетов. Если поток с высоким приоритетом
 * ожидает замок, его приоритет передаётся владельцу замка.
 */
void donate_priority (struct thread *donor, struct thread *recipient, struct lock *lock);

/**
 * @brief Удаление donation для указанного замка
 * 
 * @param t Поток-получатель
 * @param lock Замок, для которого удаляется donation
 */
void remove_donation (struct thread *t, struct lock *lock);

/**
 * @brief Удаление всех donations для потока
 * 
 * @param t Поток, для которого удаляются donations
 * 
 * Вызывается при завершении потока.
 */
void remove_all_donations (struct thread *t);
/** @} */

/**
 * @name Сравнение процессов по приоритету
 * @{
 */

/**
 * @brief Сравнение потоков по приоритету (меньше)
 * 
 * @param a Первый элемент списка
 * @param b Второй элемент списка
 * @param aux Не используется
 * @return true, если a < b по приоритету
 */
bool thread_priority_less (const struct list_elem *a, const struct list_elem *b, void *aux);

/**
 * @brief Сравнение потоков по приоритету (больше)
 * 
 * @param a Первый элемент списка
 * @param b Второй элемент списка
 * @param aux Не используется
 * @return true, если a > b по приоритету
 */
bool thread_priority_greater (const struct list_elem *a, const struct list_elem *b, void *aux);
/** @} */

/**
 * @name Функции для CPU burst
 * @{
 */

/**
 * @brief Установка CPU burst для текущего потока
 * @param burst Значение CPU burst
 */
void thread_set_cpu_burst (int burst);

/**
 * @brief Получение CPU burst текущего потока
 * @return Значение CPU burst
 */
int thread_get_cpu_burst (void);
/** @} */

/**
 * @name Алгоритмы планирования
 * @{
 */

/** Переменная для выбора алгоритма планирования */
extern int scheduler_algorithm;

#define SCHED_RR    0    /**< Round Robin (по умолчанию) */
#define SCHED_FCFS  1    /**< First Come First Served */
#define SCHED_SJF   2    /**< Shortest Job First */
#define SCHED_PRIORITY 3 /**< Приоритетное планирование */

/**
 * @brief Установка алгоритма планирования
 * @param algorithm Алгоритм (SCHED_RR, SCHED_FCFS, SCHED_SJF, SCHED_PRIORITY)
 */
void thread_set_scheduler (int algorithm);

/**
 * @brief Получение текущего алгоритма планирования
 * @return Текущий алгоритм
 */
int thread_get_scheduler (void);
/** @} */

#endif /* threads/thread.h */
