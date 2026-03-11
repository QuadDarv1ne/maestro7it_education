#include "tests/threads/tests.h"
#include "threads/init.h"
#include "threads/thread.h"
#include "devices/timer.h"
#include "lib/kernel/list.h"
#include <stdio.h>
#include <debug.h>

/* Вариант 7: Round Robin с приоритетным планированием */

/* Данные процессов по варианту:
 * Proc0: CPU burst = 3, приоритет = 27
 * Proc1: CPU burst = 8, приоритет = 7
 * Proc2: CPU burst = 20, приоритет = 8
 * Proc3: CPU burst = 1, приоритет = 18
 */

/* Семафор для ожидания завершения всех процессов */
static struct semaphore finish_sema;
static int finished_count = 0;
static int total_processes = 4;

/* Структура для передачи параметров процессу */
struct process_args
{
  int cpu_burst;
  int priority;
  char name[16];
};

/* Функция выполнения процесса */
static void
process_func(void *aux_)
{
  struct process_args *args = aux_;
  struct thread *cur = thread_current();
  int remaining = args->cpu_burst;
  int ticks_worked = 0;
  int64_t start_tick = timer_ticks();

  printf("[%s] Запущен (приоритет=%d, burst=%d)\n",
         args->name, args->priority, args->cpu_burst);

  while (remaining > 0)
    {
      int64_t current_tick = timer_ticks();
      
      /* Ждём 1 тик таймера */
      while (timer_ticks() == current_tick)
        thread_yield();
      
      ticks_worked++;
      remaining--;

      /* Вывод диагностической информации */
      printf("[%s] отработал %d тиков, осталось %d (всего тиков: %ld)\n",
             args->name, ticks_worked, remaining, (long)(timer_ticks() - start_tick));

      /* Для Round Robin: добровольная уступка процессора после каждого тика */
      /* Это позволяет другим процессам с таким же приоритетом выполняться */
      thread_yield();
    }

  /* Сигнал о завершении */
  finished_count++;
  printf("[%s] ЗАВЕРШЁН (всего отработано %d тиков)\n",
         args->name, ticks_worked);
  sema_up(&finish_sema);
}

void
test_new_alg(void)
{
  int64_t start_tick, end_tick;
  int actual_ticks;

  printf("\n");
  printf("========================================\n");
  printf("ТЕСТ: Приоритетное планирование с Round Robin\n");
  printf("Вариант 7\n");
  printf("========================================\n\n");

  /* Увеличиваем приоритет главного процесса до максимального */
  /* Это предотвращает вытеснение во время создания процессов */
  thread_set_priority(PRI_MAX);
  printf("[MAIN] Приоритет установлен на максимум (%d)\n\n", PRI_MAX);

  /* Инициализация семафора */
  sema_init(&finish_sema, 0);

  /* Определение процессов по варианту 7 */
  struct process_args procs[4] = {
    {3, 27, "Proc0"},   /* CPU burst = 3, приоритет = 27 (наивысший) */
    {8, 7, "Proc1"},    /* CPU burst = 8, приоритет = 7 (наинизший) */
    {20, 8, "Proc2"},   /* CPU burst = 20, приоритет = 8 */
    {1, 18, "Proc3"}    /* CPU burst = 1, приоритет = 18 */
  };

  /* Создание процессов */
  printf("Создание процессов:\n");
  printf("-------------------\n");

  for (int i = 0; i < 4; i++)
    {
      tid_t tid = thread_create(procs[i].name, procs[i].priority,
                                process_func, &procs[i]);
      if (tid == TID_ERROR)
        printf("[ERROR] Не удалось создать процесс %s\n", procs[i].name);
      else
        printf("[MAIN] Создан %s (tid=%d, приоритет=%d, burst=%d)\n",
               procs[i].name, tid, procs[i].priority, procs[i].cpu_burst);
    }

  /* Запоминание начального тика */
  start_tick = timer_ticks();

  printf("\n========================================\n");
  printf("Начало выполнения процессов\n");
  printf("Ожидаемый порядок: Proc0 -> Proc3 -> Proc2 -> Proc1\n");
  printf("(по убыванию приоритета)\n");
  printf("========================================\n\n");

  /* Понижение приоритета главного процесса */
  /* Это позволяет созданным процессам начать выполнение */
  thread_set_priority(PRI_MIN);

  /* Ожидание завершения всех процессов */
  for (int i = 0; i < total_processes; i++)
    sema_down(&finish_sema);

  /* Запоминание конечного тика */
  end_tick = timer_ticks();
  actual_ticks = (int)(end_tick - start_tick);

  printf("\n========================================\n");
  printf("РЕЗУЛЬТАТЫ ТЕСТА\n");
  printf("========================================\n");
  printf("Все процессы завершены: %d/%d\n", finished_count, total_processes);
  printf("Реальное время выполнения: %d тиков\n", actual_ticks);
  printf("Теоретическое (сумма burst): %d тиков\n",
         3 + 8 + 20 + 1);
  printf("Алгоритм: Round Robin с приоритетным планированием\n");
  printf("========================================\n\n");

  /* Восстановление приоритета */
  thread_set_priority(PRI_DEFAULT);
}
