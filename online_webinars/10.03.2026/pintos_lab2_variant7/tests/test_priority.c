/*
 * Unit-тесты для приоритетного планирования Pintos
 * 
 * Эти тесты проверяют логику приоритетного планирования
 * без необходимости запуска полной системы Pintos.
 * 
 * Компиляция:
 *   gcc -o test_priority test_priority.c -I..
 * 
 * Запуск:
 *   ./test_priority
 */

#include "test_common.h"
#include <stdint.h>

/* Заглушки для типов Pintos */

/* Приоритеты */
#define PRI_MIN 0
#define PRI_MAX 63
#define PRI_DEFAULT 31

/* Структура процесса */
struct thread {
    int priority;
    int effective_priority;
    int cpu_burst;
    char name[16];
};

/* Структура для donation */
struct donation {
    int priority;
    struct thread *donor;
    void *lock;
};

/* Структура замка */
struct lock {
    struct thread *holder;
};

/* Структура элемента списка */
struct list_elem {
    struct list_elem *prev;
    struct list_elem *next;
};

/* Структура списка */
struct list {
    struct list_elem head;
    struct list_elem tail;
};

/* ============================================================
 * Тестируемые функции (копии из thread.c)
 * ============================================================ */

/* Сравнение процессов по приоритету (для сортировки по убыванию) */
bool thread_priority_less(const struct thread *a, const struct thread *b) {
    return a->effective_priority < b->effective_priority;
}

/* Обновление эффективного приоритета */
void thread_update_effective_priority(struct thread *t, struct donation *donations, int num_donations) {
    int max_priority = t->priority;
    
    for (int i = 0; i < num_donations; i++) {
        if (donations[i].priority > max_priority) {
            max_priority = donations[i].priority;
        }
    }
    
    t->effective_priority = max_priority;
}

/* Проверка: должен ли поток A вытеснить поток B */
bool should_preempt(struct thread *a, struct thread *b) {
    return a->effective_priority > b->effective_priority;
}

/* ============================================================
 * Тесты
 * ============================================================ */

/* Тест: Сравнение приоритетов */
void test_priority_comparison(void) {
    TEST_BEGIN("Priority comparison");
    
    struct thread t1 = {.priority = 10, .effective_priority = 10};
    struct thread t2 = {.priority = 20, .effective_priority = 20};
    struct thread t3 = {.priority = 10, .effective_priority = 10};
    
    TEST_ASSERT(thread_priority_less(&t1, &t2), "Lower priority should be 'less'");
    TEST_ASSERT(!thread_priority_less(&t2, &t1), "Higher priority should not be 'less'");
    TEST_ASSERT(!thread_priority_less(&t1, &t3), "Same priority should not be 'less'");
    
    TEST_END();
}

/* Тест: Эффективный приоритет без donation */
void test_effective_priority_no_donation(void) {
    TEST_BEGIN("Effective priority without donation");
    
    struct thread t = {.priority = 25, .effective_priority = 0};
    struct donation donations[1] = {0};
    
    thread_update_effective_priority(&t, donations, 0);
    
    TEST_ASSERT_EQUAL(25, t.effective_priority, 
                      "Effective priority should equal base priority without donations");
    
    TEST_END();
}

/* Тест: Эффективный приоритет с donation */
void test_effective_priority_with_donation(void) {
    TEST_BEGIN("Effective priority with donation");
    
    struct thread t = {.priority = 10, .effective_priority = 0};
    struct donation donations[2] = {
        {.priority = 20},
        {.priority = 15}
    };
    
    thread_update_effective_priority(&t, donations, 2);
    
    TEST_ASSERT_EQUAL(20, t.effective_priority, 
                      "Effective priority should be max of base and donations");
    
    TEST_END();
}

/* Тест: Эффективный приоритет с несколькими donations */
void test_effective_priority_multiple_donations(void) {
    TEST_BEGIN("Effective priority with multiple donations");
    
    struct thread t = {.priority = 10, .effective_priority = 0};
    struct donation donations[4] = {
        {.priority = 15},
        {.priority = 25},
        {.priority = 20},
        {.priority = 18}
    };
    
    thread_update_effective_priority(&t, donations, 4);
    
    TEST_ASSERT_EQUAL(25, t.effective_priority, 
                      "Effective priority should be max of all donations");
    
    TEST_END();
}

/* Тест: Эффективный приоритет с donation ниже базового */
void test_effective_priority_donation_lower(void) {
    TEST_BEGIN("Effective priority with lower donation");
    
    struct thread t = {.priority = 30, .effective_priority = 0};
    struct donation donations[1] = {
        {.priority = 20}
    };
    
    thread_update_effective_priority(&t, donations, 1);
    
    TEST_ASSERT_EQUAL(30, t.effective_priority, 
                      "Effective priority should not be lowered by donation");
    
    TEST_END();
}

/* Тест: Вытеснение */
void test_preemption(void) {
    TEST_BEGIN("Preemption");
    
    struct thread low = {.priority = 10, .effective_priority = 10};
    struct thread high = {.priority = 50, .effective_priority = 50};
    struct thread same = {.priority = 10, .effective_priority = 10};
    
    TEST_ASSERT(should_preempt(&high, &low), "High priority should preempt low");
    TEST_ASSERT(!should_preempt(&low, &high), "Low priority should not preempt high");
    TEST_ASSERT(!should_preempt(&same, &low), "Same priority should not preempt");
    
    TEST_END();
}

/* Тест: Вытеснение с donation */
void test_preemption_with_donation(void) {
    TEST_BEGIN("Preemption with donation");
    
    struct thread t1 = {.priority = 10, .effective_priority = 40};  /* Получил donation */
    struct thread t2 = {.priority = 30, .effective_priority = 30};
    
    TEST_ASSERT(should_preempt(&t1, &t2), 
                "Thread with donated priority should preempt higher base priority");
    
    TEST_END();
}

/* Тест: Граничные значения приоритетов */
void test_priority_boundaries(void) {
    TEST_BEGIN("Priority boundaries");
    
    struct thread min = {.priority = PRI_MIN, .effective_priority = PRI_MIN};
    struct thread max = {.priority = PRI_MAX, .effective_priority = PRI_MAX};
    struct thread def = {.priority = PRI_DEFAULT, .effective_priority = PRI_DEFAULT};
    
    TEST_ASSERT_EQUAL(0, PRI_MIN, "PRI_MIN should be 0");
    TEST_ASSERT_EQUAL(63, PRI_MAX, "PRI_MAX should be 63");
    TEST_ASSERT_EQUAL(31, PRI_DEFAULT, "PRI_DEFAULT should be 31");
    
    TEST_ASSERT(thread_priority_less(&min, &max), "PRI_MIN < PRI_MAX");
    TEST_ASSERT(thread_priority_less(&def, &max), "PRI_DEFAULT < PRI_MAX");
    TEST_ASSERT(thread_priority_less(&min, &def), "PRI_MIN < PRI_DEFAULT");
    
    TEST_END();
}

/* Тест: Порядок выполнения процессов по варианту 7 */
void test_variant7_order(void) {
    TEST_BEGIN("Variant 7 execution order");
    
    /* Процессы из варианта 7 */
    struct thread proc0 = {.priority = 27, .effective_priority = 27, .cpu_burst = 3};
    struct thread proc1 = {.priority = 7, .effective_priority = 7, .cpu_burst = 8};
    struct thread proc2 = {.priority = 8, .effective_priority = 8, .cpu_burst = 20};
    struct thread proc3 = {.priority = 18, .effective_priority = 18, .cpu_burst = 1};
    
    /* Ожидаемый порядок: Proc0 -> Proc3 -> Proc2 -> Proc1 */
    /* (по убыванию приоритета) */
    
    struct thread *procs[] = {&proc0, &proc1, &proc2, &proc3};
    int n = 4;
    
    /* Сортировка по приоритету (пузырьковая для простоты) */
    for (int i = 0; i < n - 1; i++) {
        for (int j = 0; j < n - i - 1; j++) {
            if (thread_priority_less(procs[j], procs[j+1])) {
                struct thread *tmp = procs[j];
                procs[j] = procs[j+1];
                procs[j+1] = tmp;
            }
        }
    }
    
    /* Проверка порядка */
    TEST_ASSERT_EQUAL(27, procs[0]->priority, "First should be Proc0 (priority 27)");
    TEST_ASSERT_EQUAL(18, procs[1]->priority, "Second should be Proc3 (priority 18)");
    TEST_ASSERT_EQUAL(8, procs[2]->priority, "Third should be Proc2 (priority 8)");
    TEST_ASSERT_EQUAL(7, procs[3]->priority, "Fourth should be Proc1 (priority 7)");
    
    TEST_END();
}

/* Тест: Цепочное donation */
void test_chain_donation(void) {
    TEST_BEGIN("Chain donation");
    
    /* Три потока: A (prio=10) -> B (prio=20) -> C (prio=30) */
    /* A ждёт замок B, B ждёт замок C */
    /* После chain donation: C должен получить приоритет A */
    
    struct thread thread_a = {.priority = 10, .effective_priority = 10};
    struct thread thread_b = {.priority = 20, .effective_priority = 20};
    struct thread thread_c = {.priority = 30, .effective_priority = 30};
    
    /* B получает donation от A */
    struct donation donations_b[1] = {{.priority = 10}};
    thread_update_effective_priority(&thread_b, donations_b, 1);
    /* B.effective = max(20, 10) = 20 (базовый выше) */
    
    /* C получает donation от B */
    struct donation donations_c[1] = {{.priority = 20}};
    thread_update_effective_priority(&thread_c, donations_c, 1);
    /* C.effective = max(30, 20) = 30 (базовый выше) */
    
    /* Если бы B получил donation выше своего приоритета: */
    struct donation donations_b2[1] = {{.priority = 50}};
    thread_update_effective_priority(&thread_b, donations_b2, 1);
    TEST_ASSERT_EQUAL(50, thread_b.effective_priority, 
                      "B should have effective priority from donation");
    
    /* И тогда C тоже должен получить этот приоритет через chain */
    struct donation donations_c2[1] = {{.priority = 50}};
    thread_update_effective_priority(&thread_c, donations_c2, 1);
    TEST_ASSERT_EQUAL(50, thread_c.effective_priority, 
                      "C should inherit priority through chain");
    
    TEST_END();
}

int main(void) {
    printf("========================================\n");
    printf("Pintos Priority Scheduling Unit Tests\n");
    printf("========================================\n\n");
    
    test_priority_comparison();
    test_effective_priority_no_donation();
    test_effective_priority_with_donation();
    test_effective_priority_multiple_donations();
    test_effective_priority_donation_lower();
    test_preemption();
    test_preemption_with_donation();
    test_priority_boundaries();
    test_variant7_order();
    test_chain_donation();
    
    test_summary();
    
    return (test_failures > 0) ? 1 : 0;
}
