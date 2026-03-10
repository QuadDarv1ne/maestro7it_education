#include "threads/synch.h"
#include <stdio.h>
#include <string.h>
#include "threads/interrupt.h"
#include "threads/thread.h"

/* Инициализация семафора */
void sema_init(struct semaphore *sema, unsigned value)
{
  ASSERT(sema != NULL);

  sema->value = value;
  list_init(&sema->waiters);
}

/* Функция сравнения ожидающих процессов по приоритету */
bool semaphore_waiter_priority_less(const struct list_elem *a, 
                                     const struct list_elem *b, 
                                     void *aux UNUSED)
{
  struct thread *ta = list_entry(a, struct thread, elem);
  struct thread *tb = list_entry(b, struct thread, elem);
  return ta->effective_priority < tb->effective_priority;
}

/* Операция Down (P) на семафоре с приоритетом */
void sema_down_priority(struct semaphore *sema)
{
  enum intr_level old_level;

  ASSERT(sema != NULL);
  ASSERT(!intr_context());

  old_level = intr_disable();
  
  while (sema->value == 0)
    {
      /* Добавление в список ожидающих с учётом приоритета */
      list_insert_ordered(&sema->waiters, &thread_current()->elem,
                          thread_priority_less, NULL);
      thread_block();
    }
  
  sema->value--;
  intr_set_level(old_level);
}

/* Операция Up (V) на семафоре с приоритетом */
void sema_up_priority(struct semaphore *sema)
{
  enum intr_level old_level;

  ASSERT(sema != NULL);

  old_level = intr_disable();
  
  if (!list_empty(&sema->waiters))
    {
      /* Выбор процесса с наивысшим приоритетом из ожидающих */
      list_sort(&sema->waiters, semaphore_waiter_priority_less, NULL);
      struct thread *t = list_entry(list_pop_front(&sema->waiters),
                                    struct thread, elem);
      thread_unblock(t);
      
      /* Если разблокированный процесс имеет более высокий приоритет, вытеснить */
      if (t->effective_priority > thread_current()->effective_priority)
        thread_yield();
    }
  
  sema->value++;
  intr_set_level(old_level);
}

/* Стандартная операция Down (P) */
void sema_down(struct semaphore *sema)
{
  enum intr_level old_level;

  ASSERT(sema != NULL);
  ASSERT(!intr_context());

  old_level = intr_disable();
  
  while (sema->value == 0)
    {
      list_push_back(&sema->waiters, &thread_current()->elem);
      thread_block();
    }
  
  sema->value--;
  intr_set_level(old_level);
}

/* Попытка операции Down (P) без блокировки */
bool sema_try_down(struct semaphore *sema)
{
  enum intr_level old_level;
  bool success;

  ASSERT(sema != NULL);

  old_level = intr_disable();
  
  if (sema->value > 0)
    {
      sema->value--;
      success = true;
    }
  else
    success = false;
  
  intr_set_level(old_level);

  return success;
}

/* Стандартная операция Up (V) */
void sema_up(struct semaphore *sema)
{
  enum intr_level old_level;

  ASSERT(sema != NULL);

  old_level = intr_disable();
  
  if (!list_empty(&sema->waiters))
    {
      /* Используем приоритетное пробуждение */
      list_sort(&sema->waiters, semaphore_waiter_priority_less, NULL);
      struct thread *t = list_entry(list_pop_front(&sema->waiters),
                                    struct thread, elem);
      thread_unblock(t);
    }
  
  sema->value++;
  intr_set_level(old_level);
}

/* Инициализация замка */
void lock_init(struct lock *lock)
{
  ASSERT(lock != NULL);

  lock->holder = NULL;
  sema_init(&lock->semaphore, 1);
}

/* Захват замка с priority donation */
void lock_acquire(struct lock *lock)
{
  struct thread *cur = thread_current();
  
  ASSERT(lock != NULL);
  ASSERT(!intr_context());
  ASSERT(!lock_held_by_current_thread(lock));

  /* Priority donation: если замок занят, передать приоритет владельцу */
  if (lock->holder != NULL)
    {
      cur->waiting_lock = lock;
      donate_priority(cur, lock->holder, lock);
    }

  sema_down(&lock->semaphore);
  
  lock->holder = cur;
  cur->waiting_lock = NULL;
}

/* Попытка захвата замка без блокировки */
bool lock_try_acquire(struct lock *lock)
{
  bool success;

  ASSERT(lock != NULL);
  ASSERT(!lock_held_by_current_thread(lock));

  success = sema_try_down(&lock->semaphore);
  if (success)
    lock->holder = thread_current();
  
  return success;
}

/* Освобождение замка с отменой donation */
void lock_release(struct lock *lock)
{
  struct thread *cur = thread_current();
  
  ASSERT(lock != NULL);
  ASSERT(lock_held_by_current_thread(lock));

  /* Удаление всех donations, связанных с этим замком */
  remove_donation(cur, lock);
  thread_update_effective_priority(cur);
  
  lock->holder = NULL;
  sema_up(&lock->semaphore);
}

/* Проверка, принадлежит ли замок текущему процессу */
bool lock_held_by_current_thread(const struct lock *lock)
{
  ASSERT(lock != NULL);

  return lock->holder == thread_current();
}

/* Инициализация условной переменной */
void cond_init(struct condition *cond)
{
  ASSERT(cond != NULL);

  list_init(&cond->waiters);
}

/* Ожидание условия */
void cond_wait(struct condition *cond, struct lock *lock)
{
  struct semaphore_elem waiter;

  ASSERT(cond != NULL);
  ASSERT(lock != NULL);
  ASSERT(!intr_context());
  ASSERT(lock_held_by_current_thread(lock));

  sema_init(&waiter.semaphore, 0);
  
  /* Добавление в список ожидающих с учётом приоритета */
  list_insert_ordered(&cond->waiters, &waiter.elem,
                      semaphore_waiter_priority_less, NULL);
  
  lock_release(lock);
  sema_down(&waiter.semaphore);
  lock_acquire(lock);
}

/* Сигнал одному ожидающему */
void cond_signal(struct condition *cond, struct lock *lock UNUSED)
{
  ASSERT(cond != NULL);
  ASSERT(lock != NULL);
  ASSERT(!intr_context());
  ASSERT(lock_held_by_current_thread(lock));

  if (!list_empty(&cond->waiters))
    {
      /* Выбор процесса с наивысшим приоритетом */
      list_sort(&cond->waiters, semaphore_waiter_priority_less, NULL);
      struct semaphore_elem *waiter = list_entry(list_pop_front(&cond->waiters),
                                                  struct semaphore_elem, elem);
      sema_up(&waiter->semaphore);
    }
}

/* Сигнал всем ожидающим */
void cond_broadcast(struct condition *cond, struct lock *lock UNUSED)
{
  ASSERT(cond != NULL);
  ASSERT(lock != NULL);
  ASSERT(!intr_context());
  ASSERT(lock_held_by_current_thread(lock));

  while (!list_empty(&cond->waiters))
    cond_signal(cond, lock);
}

/* Вспомогательная структура для условных переменных */
struct semaphore_elem
  {
    struct semaphore semaphore;       /* Семафор для ожидания */
    struct list_elem elem;            /* Элемент списка */
  };
