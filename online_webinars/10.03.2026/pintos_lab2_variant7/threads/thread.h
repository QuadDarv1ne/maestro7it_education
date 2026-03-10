#ifndef THREADS_THREAD_H
#define THREADS_THREAD_H

#include <debug.h>
#include <list.h>
#include <stdint.h>

/* Статусы процессов */
enum thread_status
  {
    THREAD_RUNNING,     /* Выполняется */
    THREAD_READY,       /* Готов к выполнению */
    THREAD_BLOCKED,     /* Заблокирован */
    THREAD_DYING        /* Завершается */
  };

/* Приоритеты процессов: от 0 (минимальный) до 63 (максимальный) */
#define PRI_MIN 0                       /* Минимальный приоритет */
#define PRI_MAX 63                      /* Максимальный приоритет */
#define PRI_DEFAULT 31                  /* Приоритет по умолчанию */

/* Структура для отслеживания доноров приоритета */
struct donation
  {
    int priority;                       /* Приоритет донора */
    struct thread *donor;               /* Указатель на поток-донор */
    struct lock *lock;                  /* Замок, на котором основана donation */
    struct list_elem elem;              /* Элемент списка */
  };

/* Структура процесса (thread) */
struct thread
  {
    /* Владелец ядра */
    tid_t tid;                          /* Идентификатор процесса */
    enum thread_status status;          /* Статус процесса */
    char name[16];                      /* Имя процесса (для отладки) */
    uint8_t *stack;                     /* Указатель на стек */
    int priority;                       /* Базовый приоритет */
    int effective_priority;             /* Эффективный приоритет (с учётом donation) */
    
    /* Поля для priority donation */
    struct list donation_list;          /* Список полученных donations */
    struct lock *waiting_lock;          /* Замок, который ожидает процесс */
    
    /* Общие поля */
    struct list_elem allelem;           /* Элемент списка всех процессов */
    struct list_elem elem;              /* Элемент списка ready/других списков */

#ifdef USERPROG
    /* Владелец пользовательской программы */
    struct process *process;            /* Родительский процесс */
    struct list children;               /* Список дочерних процессов */
    struct list_elem childelem;         /* Элемент списка дочерних процессов */
#endif

    /* Поля для планирования */
    int64_t sleep_ticks;                /* Тики до пробуждения (для timer_sleep) */
    struct list_elem sleep_elem;        /* Элемент списка спящих процессов */
    int cpu_burst;                      /* Оставшееся время CPU burst (для теста) */
    
#ifdef FILESYS
    unsigned magic;                     /* Магическое число для обнаружения повреждения стека */
#endif
  };

/* Функции работы с процессами */
void thread_init (void);
void thread_start (void);

void thread_tick (void);
void thread_print_stats (void);

/* Создание и управление процессами */
typedef void thread_func (void *aux);
tid_t thread_create (const char *name, int priority, thread_func *, void *);
void thread_block (void);
void thread_unblock (struct thread *);
struct thread *thread_current (void);
tid_t thread_tid (void);
const char *thread_name (void);

void thread_exit (void) NO_RETURN;
void thread_yield (void);

/* Функции работы с приоритетом */
int thread_get_priority (void);
void thread_set_priority (int);
int thread_get_effective_priority (struct thread *);
void thread_update_effective_priority (struct thread *);

/* Функции для priority donation */
void donate_priority (struct thread *donor, struct thread *recipient, struct lock *lock);
void remove_donation (struct thread *t, struct lock *lock);
void remove_all_donations (struct thread *t);

/* Сравнение процессов по приоритету */
bool thread_priority_less (const struct list_elem *a, const struct list_elem *b, void *aux);
bool thread_priority_greater (const struct list_elem *a, const struct list_elem *b, void *aux);

/* Функции для CPU burst (для теста test-new-alg) */
void thread_set_cpu_burst (int burst);
int thread_get_cpu_burst (void);

/* Переменная для выбора алгоритма планирования */
extern int scheduler_algorithm;
#define SCHED_RR    0    /* Round Robin (по умолчанию) */
#define SCHED_FCFS  1    /* First Come First Served */
#define SCHED_SJF   2    /* Shortest Job First */
#define SCHED_PRIORITY 3 /* Приоритетное планирование */

void thread_set_scheduler (int algorithm);
int thread_get_scheduler (void);

#endif /* threads/thread.h */
