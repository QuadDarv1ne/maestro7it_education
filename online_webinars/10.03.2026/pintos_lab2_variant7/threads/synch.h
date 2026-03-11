#ifndef THREADS_SYNCH_H
#define THREADS_SYNCH_H

#include <list.h>
#include <stdbool.h>

/* Семафор */
struct semaphore
  {
    unsigned value;             /* Текущее значение */
    struct list waiters;        /* Список ожидающих процессов */
  };

void sema_init (struct semaphore *, unsigned value);
void sema_down (struct semaphore *);
bool sema_try_down (struct semaphore *);
void sema_up (struct semaphore *);

void sema_down_priority (struct semaphore *);
void sema_up_priority (struct semaphore *);

/* Замок (lock) */
struct lock
  {
    struct thread *holder;      /* Владелец замка */
    struct semaphore semaphore; /* Семафор для реализации замка */
  };

void lock_init (struct lock *);
void lock_acquire (struct lock *);
bool lock_try_acquire (struct lock *);
void lock_release (struct lock *);
bool lock_held_by_current_thread (const struct lock *);

/* Условная переменная */
struct condition
  {
    struct list waiters;        /* Список ожидающих процессов */
  };

void cond_init (struct condition *);
void cond_wait (struct condition *, struct lock *);
void cond_signal (struct condition *, struct lock *);
void cond_broadcast (struct condition *, struct lock *);

/* Вспомогательные функции */
bool semaphore_waiter_priority_less (const struct list_elem *a, 
                                      const struct list_elem *b, 
                                      void *aux UNUSED);

#endif /* threads/synch.h */
