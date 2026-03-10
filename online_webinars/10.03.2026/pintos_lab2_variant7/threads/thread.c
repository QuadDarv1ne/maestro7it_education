#include "threads/thread.h"
#include <debug.h>
#include <random.h>
#include <stddef.h>
#include <stdio.h>
#include <string.h>
#include "threads/flags.h"
#include "threads/interrupt.h"
#include "threads/intr-stubs.h"
#include "threads/palloc.h"
#include "threads/switch.h"
#include "threads/vaddr.h"
#ifdef USERPROG
#include "userprog/process.h"
#endif

/* Переменная для выбора алгоритма планирования */
int scheduler_algorithm = SCHED_RR;

/* Магическое число для обнаружения повреждения стека */
#ifdef USERPROG
#define THREAD_MAGIC 0xcd6abf4b
#endif

/* Статистика процессов */
static struct list all_list;
static struct list ready_list;
static struct list sleep_list;

static struct thread *idle_thread;
static struct thread *initial_thread;
static struct lock sleep_lock;

static int64_t idle_ticks;
static int64_t kernel_ticks;
static int64_t total_ticks;

static struct kernel_thread_frame *get_kernel_frame(struct thread *t);
static bool is_kernel_thread(struct thread *t);
static void schedule(void);
static void thread_schedule_tail(struct thread *prev);
static tid_t allocate_tid(void);

/* Инициализация системы процессов */
void thread_init(void)
{
  ASSERT(intr_get_level() == INTR_OFF);

  list_init(&all_list);
  list_init(&ready_list);
  list_init(&sleep_list);
  lock_init(&sleep_lock);

  idle_ticks = 0;
  kernel_ticks = 0;
  total_ticks = 0;

  initial_thread = running_thread();
  initial_thread->status = THREAD_RUNNING;
  initial_thread->tid = allocate_tid();
  initial_thread->priority = PRI_DEFAULT;
  initial_thread->effective_priority = PRI_DEFAULT;
  list_init(&initial_thread->donation_list);
  initial_thread->waiting_lock = NULL;
  initial_thread->cpu_burst = 0;
}

/* Запуск планировщика */
void thread_start(void)
{
  struct semaphore idle_started;
  sema_init(&idle_started, 0);
  thread_create("idle", PRI_MIN, idle, &idle_started);

  intr_enable();
  sema_down(&idle_started);
}

/* Тик таймера */
void thread_tick(void)
{
  struct thread *t = thread_current();
  total_ticks++;

  if (is_kernel_thread(t))
    kernel_ticks++;
  else if (t == idle_thread)
    idle_ticks++;
  else
    {
      /* Уменьшаем CPU burst если установлен */
      if (t->cpu_burst > 0)
        t->cpu_burst--;
    }

  /* Проверка спящих процессов */
  enum intr_level old_level = intr_disable();
  lock_acquire(&sleep_lock);
  
  if (!list_empty(&sleep_list))
    {
      struct list_elem *e = list_begin(&sleep_list);
      while (e != list_end(&sleep_list))
        {
          struct thread *sleeper = list_entry(e, struct thread, sleep_elem);
          if (sleeper->sleep_ticks > 0)
            sleeper->sleep_ticks--;
          
          if (sleeper->sleep_ticks == 0)
            {
              e = list_remove(e);
              thread_unblock(sleeper);
            }
          else
            e = list_next(e);
        }
    }
  
  lock_release(&sleep_lock);
  intr_set_level(old_level);
}

/* Вывод статистики */
void thread_print_stats(void)
{
  printf("Thread: %lld idle ticks, %lld kernel ticks, %lld total ticks\n",
         idle_ticks, kernel_ticks, total_ticks);
}

/* Функция сравнения процессов по приоритету (для сортировки по убыванию) */
bool thread_priority_less(const struct list_elem *a, const struct list_elem *b, void *aux UNUSED)
{
  struct thread *ta = list_entry(a, struct thread, elem);
  struct thread *tb = list_entry(b, struct thread, elem);
  return ta->effective_priority < tb->effective_priority;
}

/* Функция сравнения процессов по приоритету (для сортировки по возрастанию) */
bool thread_priority_greater(const struct list_elem *a, const struct list_elem *b, void *aux UNUSED)
{
  struct thread *ta = list_entry(a, struct thread, elem);
  struct thread *tb = list_entry(b, struct thread, elem);
  return ta->effective_priority > tb->effective_priority;
}

/* Создание нового процесса */
tid_t thread_create(const char *name, int priority,
                    thread_func *function, void *aux)
{
  struct thread *t;
  struct kernel_thread_frame *kf;
  struct switch_entry_frame *ef;
  struct switch_threads_frame *sf;
  tid_t tid;

  ASSERT(function != NULL);

  /* Выделение памяти под структуру процесса */
  t = palloc_get_page(PAL_ZERO);
  if (t == NULL)
    return TID_ERROR;

  /* Инициализация структуры процесса */
  t->tid = allocate_tid();
  strlcpy(t->name, name, sizeof t->name);
  t->stack = (uint8_t *)t + PGSIZE;
  t->priority = priority;
  t->effective_priority = priority;
  list_init(&t->donation_list);
  t->waiting_lock = NULL;
  t->cpu_burst = 0;

  /* Настройка стека для первого переключения контекста */
  kf = get_kernel_frame(t);
  kf->eip = (void (*) (void)) kernel_thread;
  kf->function = function;
  kf->aux = aux;

  ef = (struct switch_entry_frame *) t->stack - 1;
  ef->eip = (void (*) (void)) kernel_thread;
  t->stack = (uint8_t *) ef;

  sf = (struct switch_threads_frame *) t->stack - 1;
  sf->eip = switch_entry;
  t->stack = (uint8_t *) sf;

  /* Добавление в списки */
  enum intr_level old_level = intr_disable();
  list_push_back(&all_list, &t->allelem);
  
  /* Добавление в очередь готовых с учётом приоритета */
  list_insert_ordered(&ready_list, &t->elem, thread_priority_less, NULL);
  
  intr_set_level(old_level);

  /* Если приоритет нового процесса выше текущего, вытеснить текущий */
  if (t->effective_priority > thread_current()->effective_priority)
    thread_yield();

  return t->tid;
}

/* Блокировка текущего процесса */
void thread_block(void)
{
  ASSERT(!intr_context());
  ASSERT(intr_get_level() == INTR_OFF);

  thread_current()->status = THREAD_BLOCKED;
  schedule();
}

/* Разблокировка процесса */
void thread_unblock(struct thread *t)
{
  enum intr_level old_level;

  ASSERT(is_thread(t));

  old_level = intr_disable();
  ASSERT(t->status == THREAD_BLOCKED);
  
  /* Добавление в очередь готовых с учётом приоритета */
  list_insert_ordered(&ready_list, &t->elem, thread_priority_less, NULL);
  t->status = THREAD_READY;
  
  intr_set_level(old_level);
}

/* Получение текущего процесса */
struct thread *thread_current(void)
{
  struct thread *t = running_thread();
  ASSERT(is_thread(t));
  ASSERT(t->status == THREAD_RUNNING);
  return t;
}

/* Получение ID текущего процесса */
tid_t thread_tid(void)
{
  return thread_current()->tid;
}

/* Получение имени текущего процесса */
const char *thread_name(void)
{
  return thread_current()->name;
}

/* Завершение текущего процесса */
void thread_exit(void)
{
  ASSERT(!intr_context());

#ifdef USERPROG
  process_exit();
#endif

  /* Удаление из списка всех процессов */
  enum intr_level old_level = intr_disable();
  list_remove(&thread_current()->allelem);
  
  /* Удаление всех donations */
  remove_all_donations(thread_current());
  
  thread_current()->status = THREAD_DYING;
  schedule();
  NOT_REACHED();
}

/* Освобождение процессора текущим процессом */
void thread_yield(void)
{
  struct thread *cur = thread_current();
  enum intr_level old_level;

  ASSERT(!intr_context());

  old_level = intr_disable();
  
  if (cur != idle_thread)
    {
      /* Добавление в очередь готовых с учётом приоритета */
      list_insert_ordered(&ready_list, &cur->elem, thread_priority_less, NULL);
    }
  
  cur->status = THREAD_READY;
  schedule();
  intr_set_level(old_level);
}

/* Получение приоритета текущего процесса */
int thread_get_priority(void)
{
  return thread_current()->priority;
}

/* Установка приоритета текущего процесса */
void thread_set_priority(int new_priority)
{
  struct thread *cur = thread_current();
  int old_effective = cur->effective_priority;
  
  cur->priority = new_priority;
  
  /* Пересчёт эффективного приоритета */
  thread_update_effective_priority(cur);
  
  /* Если эффективный приоритет понизился, возможно вытеснение */
  if (cur->effective_priority < old_effective)
    thread_yield();
}

/* Получение эффективного приоритета процесса */
int thread_get_effective_priority(struct thread *t)
{
  return t->effective_priority;
}

/* Обновление эффективного приоритета процесса */
void thread_update_effective_priority(struct thread *t)
{
  int max_priority = t->priority;
  
  /* Проверка всех полученных donations */
  if (!list_empty(&t->donation_list))
    {
      struct list_elem *e;
      for (e = list_begin(&t->donation_list); 
           e != list_end(&t->donation_list); 
           e = list_next(e))
        {
          struct donation *d = list_entry(e, struct donation, elem);
          if (d->priority > max_priority)
            max_priority = d->priority;
        }
    }
  
  t->effective_priority = max_priority;
  
  /* Если процесс ожидает замок, обновить приоритет владельца */
  if (t->waiting_lock != NULL && t->waiting_lock->holder != NULL)
    {
      thread_update_effective_priority(t->waiting_lock->holder);
    }
}

/* Передача приоритета (priority donation) */
void donate_priority(struct thread *donor, struct thread *recipient, struct lock *lock)
{
  struct donation *d = malloc(sizeof(struct donation));
  if (d == NULL)
    return;
  
  d->priority = donor->effective_priority;
  d->donor = donor;
  d->lock = lock;
  
  list_push_back(&recipient->donation_list, &d->elem);
  thread_update_effective_priority(recipient);
  
  /* Цепочное donation: если получатель тоже ждёт замок */
  if (recipient->waiting_lock != NULL && recipient->waiting_lock->holder != NULL)
    {
      donate_priority(recipient, recipient->waiting_lock->holder, recipient->waiting_lock);
    }
}

/* Удаление donation для конкретного замка */
void remove_donation(struct thread *t, struct lock *lock)
{
  if (list_empty(&t->donation_list))
    return;
  
  struct list_elem *e = list_begin(&t->donation_list);
  while (e != list_end(&t->donation_list))
    {
      struct donation *d = list_entry(e, struct donation, elem);
      if (d->lock == lock)
        {
          e = list_remove(e);
          free(d);
        }
      else
        e = list_next(e);
    }
  
  thread_update_effective_priority(t);
}

/* Удаление всех donations процесса */
void remove_all_donations(struct thread *t)
{
  if (list_empty(&t->donation_list))
    return;
  
  struct list_elem *e;
  while (!list_empty(&t->donation_list))
    {
      e = list_pop_front(&t->donation_list);
      struct donation *d = list_entry(e, struct donation, elem);
      free(d);
    }
}

/* Установка CPU burst */
void thread_set_cpu_burst(int burst)
{
  thread_current()->cpu_burst = burst;
}

/* Получение CPU burst */
int thread_get_cpu_burst(void)
{
  return thread_current()->cpu_burst;
}

/* Установка алгоритма планирования */
void thread_set_scheduler(int algorithm)
{
  scheduler_algorithm = algorithm;
}

/* Получение текущего алгоритма планирования */
int thread_get_scheduler(void)
{
  return scheduler_algorithm;
}

/* Выбор следующего процесса для выполнения */
static struct thread *next_thread_to_run(void)
{
  if (list_empty(&ready_list))
    return idle_thread;
  
  /* Приоритетное планирование: процесс с наивысшим приоритетом */
  return list_entry(list_pop_front(&ready_list), struct thread, elem);
}

/* Планирование процессов */
static void schedule(void)
{
  struct thread *cur = running_thread();
  struct thread *next = next_thread_to_run();
  struct thread *prev = NULL;

  ASSERT(intr_get_level() == INTR_OFF);
  ASSERT(cur->status != THREAD_RUNNING);
  ASSERT(is_thread(next));

  if (cur != next)
    prev = switch_threads(cur, next);
  
  thread_schedule_tail(prev);
}

/* Завершение планирования */
static void thread_schedule_tail(struct thread *prev)
{
  struct thread *cur = running_thread();

  ASSERT(intr_get_level() == INTR_OFF);

  /* Установка статуса RUNNING */
  cur->status = THREAD_RUNNING;

  /* Освобождение памяти завершённого процесса */
  if (prev != NULL && prev->status == THREAD_DYING && prev != initial_thread)
    {
      ASSERT(prev != cur);
      palloc_free_page(prev);
    }
}

/* Выделение TID */
static tid_t allocate_tid(void)
{
  static tid_t next_tid = 1;
  return next_tid++;
}

/* Idle процесс */
static void idle(void *idle_started_)
{
  struct semaphore *idle_started = idle_started_;

  idle_thread = thread_current();
  sema_up(idle_started);

  for (;;)
    {
      intr_disable();
      thread_block();
      asm volatile ("sti; hlt" : : : "memory");
    }
}

/* Точка входа в поток ядра */
static void kernel_thread(thread_func *function, void *aux)
{
  ASSERT(function != NULL);

  intr_enable();
  function(aux);
  thread_exit();
}

/* Проверка, является ли процесс потоком ядра */
static bool is_kernel_thread(struct thread *t)
{
  return t->pagedir == NULL;
}

/* Получение фрейма ядра */
static struct kernel_thread_frame *get_kernel_frame(struct thread *t)
{
  return (struct kernel_thread_frame *) ((uint8_t *) t + PGSIZE - sizeof(struct kernel_thread_frame));
}

/* Проверка валидности процесса */
bool is_thread(struct thread *t)
{
  return t != NULL && t->magic == THREAD_MAGIC;
}

/* Получение выполняющегося процесса */
struct thread *running_thread(void)
{
  uint32_t *esp;

  asm ("mov %%esp, %0" : "=g" (esp));
  return pg_round_down(esp);
}
