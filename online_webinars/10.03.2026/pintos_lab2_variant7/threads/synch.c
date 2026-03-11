#include "threads/synch.h"
#include <stdio.h>
#include <string.h>
#include "threads/interrupt.h"
#include "threads/thread.h"

/* Вспомогательная структура для условных переменных */
struct semaphore_elem
  {
    struct semaphore semaphore;
    struct list_elem elem;
  };

/* Поиск элемента с максимальным приоритетом */
static struct list_elem *
list_find_max(struct list *list, list_less_func *less, void *aux)
{
  struct list_elem *e, *max = NULL;

  ASSERT(list != NULL);

  if (list_empty(list))
    return NULL;

  for (e = list_begin(list); e != list_end(list); e = list_next(e))
    if (max == NULL || less(max, e, aux))
      max = e;

  return max;
}

void sema_init(struct semaphore *sema, unsigned value)
{
  ASSERT(sema != NULL);

  sema->value = value;
  list_init(&sema->waiters);
}

bool semaphore_waiter_priority_less(const struct list_elem *a,
                                     const struct list_elem *b,
                                     void *aux UNUSED)
{
  struct thread *ta = list_entry(a, struct thread, elem);
  struct thread *tb = list_entry(b, struct thread, elem);
  return ta->effective_priority < tb->effective_priority;
}

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

void sema_up_priority(struct semaphore *sema)
{
  enum intr_level old_level;

  ASSERT(sema != NULL);

  old_level = intr_disable();

  if (!list_empty(&sema->waiters))
    {
      /* Выбор процесса с наивысшим приоритетом из ожидающих */
      struct thread *t = list_entry(list_find_max(&sema->waiters, semaphore_waiter_priority_less, NULL),
                                    struct thread, elem);
      list_remove(&t->elem);
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
  /* Используем приоритетное ожидание по умолчанию */
  sema_down_priority(sema);
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
  /* Используем приоритетное пробуждение по умолчанию */
  sema_up_priority(sema);
}

/* Инициализация замка */
void lock_init(struct lock *lock)
{
  ASSERT(lock != NULL);

  lock->holder = NULL;
  sema_init(&lock->semaphore, 1);
}

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

  /* Захват замка */
  lock->holder = cur;
  cur->waiting_lock = NULL;

  /* Обновление приоритета после захвата */
  thread_update_effective_priority(cur);

  /* Проверка: замок должен быть захвачен текущим процессом */
  ASSERT(lock->holder == cur);
}

/* Попытка захвата замка без блокировки */
bool lock_try_acquire(struct lock *lock)
{
  struct thread *cur = thread_current();
  bool success;

  ASSERT(lock != NULL);
  ASSERT(!lock_held_by_current_thread(lock));

  /* Priority donation: если замок занят, передать приоритет владельцу */
  if (lock->holder != NULL)
    {
      cur->waiting_lock = lock;
      donate_priority(cur, lock->holder, lock);
    }

  success = sema_try_down(&lock->semaphore);
  if (success)
    {
      lock->holder = cur;
      cur->waiting_lock = NULL;
      thread_update_effective_priority(cur);
    }
  else
    {
      /* Очистка waiting_lock при неудаче */
      cur->waiting_lock = NULL;
    }

  return success;
}

void lock_release(struct lock *lock)
{
  struct thread *cur = thread_current();
  struct thread *next_holder;

  ASSERT(lock != NULL);
  ASSERT(lock_held_by_current_thread(lock));

  /* Удаление donations для этого замка */
  remove_donation(cur, lock);
  thread_update_effective_priority(cur);

  /* Проверка: есть ли ожидающие процессы */
  enum intr_level old_level = intr_disable();
  if (!list_empty(&lock->semaphore.waiters))
    {
      /* Новый владелец будет процесс с наивысшим приоритетом */
      next_holder = list_entry(list_find_max(&lock->semaphore.waiters,
                                              semaphore_waiter_priority_less, NULL),
                               struct thread, elem);
    }
  else
    {
      next_holder = NULL;
    }
  intr_set_level(old_level);

  /* Освобождение замка */
  lock->holder = NULL;
  sema_up(&lock->semaphore);

  /* Вытеснение если новый владелец имеет более высокий приоритет */
  if (next_holder != NULL &&
      next_holder->effective_priority > cur->effective_priority)
    thread_yield();
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
      struct semaphore_elem *waiter = list_entry(
          list_find_max(&cond->waiters, semaphore_waiter_priority_less, NULL),
          struct semaphore_elem, elem);
      list_remove(&waiter->elem);
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

  /* Пробуждение всех процессов в порядке приоритета */
  while (!list_empty(&cond->waiters))
    {
      struct semaphore_elem *waiter = list_entry(
          list_find_max(&cond->waiters, semaphore_waiter_priority_less, NULL),
          struct semaphore_elem, elem);
      list_remove(&waiter->elem);
      sema_up(&waiter->semaphore);
    }
}
