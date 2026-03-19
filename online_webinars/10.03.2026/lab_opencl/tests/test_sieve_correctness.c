/*
 * Интеграционные тесты: Сравнение CPU vs GPU для Решета Эратосфена
 *
 * Компиляция:
 *   gcc -o test_sieve_correctness test_sieve_correctness.c \
 *       -I.. -I../sieve -I../include ../sieve/sieve.c ../src/cl_utils.c \
 *       -lOpenCL -lm
 *
 * Запуск:
 *   ./test_sieve_correctness
 */

#include "test_common.h"
#include <stdint.h>
#include <math.h>

/* Внешние функции из sieve.c */
extern unsigned long sieve_cpu(unsigned char* is_prime, unsigned long limit);

/* Объявление функции sieve_gpu (необходимо адаптировать для тестов) */
typedef enum {
    DEVICE_AUTO,
    DEVICE_GPU,
    DEVICE_CPU
} DeviceType;

extern unsigned int sieve_gpu(unsigned char* is_prime, unsigned long limit,
                              size_t local_size, int print_info, 
                              double* gpu_time_ms, DeviceType device_type);

/* Вспомогательная функция для сравнения массивов is_prime */
static int arrays_equal(const unsigned char* a, const unsigned char* b, 
                        unsigned long size) {
    for (unsigned long i = 0; i < size; i++) {
        if (a[i] != b[i]) return 0;
    }
    return 1;
}

/* Вспомогательная функция для подсчёта простых чисел */
static unsigned long count_primes(const unsigned char* is_prime, 
                                   unsigned long limit) {
    unsigned long count = 0;
    for (unsigned long i = 2; i <= limit; i++) {
        if (is_prime[i]) count++;
    }
    return count;
}

/* Тест: Сравнение CPU и GPU для малого N */
void test_sieve_cpu_gpu_small(void) {
    TEST_BEGIN("Sieve CPU vs GPU small (N=1000)");

    unsigned long limit = 1000;
    unsigned char* is_prime_cpu = (unsigned char*)calloc(limit + 1, sizeof(unsigned char));
    unsigned char* is_prime_gpu = (unsigned char*)calloc(limit + 1, sizeof(unsigned char));
    
    TEST_ASSERT(is_prime_cpu != NULL, "Выделена память для CPU массива");
    TEST_ASSERT(is_prime_gpu != NULL, "Выделена память для GPU массива");
    
    if (!is_prime_cpu || !is_prime_gpu) {
        SAFE_FREE(is_prime_cpu);
        SAFE_FREE(is_prime_gpu);
        return;
    }

    /* CPU версия */
    unsigned long count_cpu = sieve_cpu(is_prime_cpu, limit);
    
    /* GPU версия */
    double gpu_time = 0;
    unsigned long count_gpu = sieve_gpu(is_prime_gpu, limit, 128, 0, &gpu_time, DEVICE_GPU);
    
    /* Сравнение количества */
    TEST_ASSERT_EQUAL(count_cpu, count_gpu, "Количество простых чисел должно совпадать");
    
    /* Сравнение массивов */
    TEST_ASSERT(arrays_equal(is_prime_cpu, is_prime_gpu, limit + 1),
                "Массивы CPU и GPU должны совпадать");
    
    printf("    Найдено простых: %lu\n", count_cpu);
    printf("    Время GPU: %.3f мс\n", gpu_time);
    
    SAFE_FREE(is_prime_cpu);
    SAFE_FREE(is_prime_gpu);
    TEST_END();
}

/* Тест: Сравнение CPU и GPU для среднего N */
void test_sieve_cpu_gpu_medium(void) {
    TEST_BEGIN("Sieve CPU vs GPU medium (N=100000)");

    unsigned long limit = 100000;
    unsigned char* is_prime_cpu = (unsigned char*)calloc(limit + 1, sizeof(unsigned char));
    unsigned char* is_prime_gpu = (unsigned char*)calloc(limit + 1, sizeof(unsigned char));
    
    TEST_ASSERT(is_prime_cpu != NULL, "Выделена память для CPU массива");
    TEST_ASSERT(is_prime_gpu != NULL, "Выделена память для GPU массива");
    
    if (!is_prime_cpu || !is_prime_gpu) {
        SAFE_FREE(is_prime_cpu);
        SAFE_FREE(is_prime_gpu);
        return;
    }

    /* CPU версия */
    clock_t cpu_start = clock();
    unsigned long count_cpu = sieve_cpu(is_prime_cpu, limit);
    clock_t cpu_end = clock();
    double cpu_time_ms = ((double)(cpu_end - cpu_start)) / CLOCKS_PER_SEC * 1000.0;
    
    /* GPU версия */
    double gpu_time = 0;
    unsigned long count_gpu = sieve_gpu(is_prime_gpu, limit, 256, 0, &gpu_time, DEVICE_GPU);
    
    /* Сравнение количества */
    TEST_ASSERT_EQUAL(count_cpu, count_gpu, "Количество простых чисел должно совпадать");
    
    /* Сравнение массивов */
    TEST_ASSERT(arrays_equal(is_prime_cpu, is_prime_gpu, limit + 1),
                "Массивы CPU и GPU должны совпадать");
    
    double speedup = gpu_time > 0 ? cpu_time_ms / gpu_time : 0;
    printf("    Найдено простых: %lu\n", count_cpu);
    printf("    CPU время: %.3f мс\n", cpu_time_ms);
    printf("    GPU время: %.3f мс\n", gpu_time);
    printf("    Ускорение: %.2fx\n", speedup);
    
    SAFE_FREE(is_prime_cpu);
    SAFE_FREE(is_prime_gpu);
    TEST_END();
}

/* Тест: Сравнение CPU и GPU для большого N */
void test_sieve_cpu_gpu_large(void) {
    TEST_BEGIN("Sieve CPU vs GPU large (N=1000000)");

    unsigned long limit = 1000000;
    unsigned char* is_prime_cpu = (unsigned char*)calloc(limit + 1, sizeof(unsigned char));
    unsigned char* is_prime_gpu = (unsigned char*)calloc(limit + 1, sizeof(unsigned char));
    
    TEST_ASSERT(is_prime_cpu != NULL, "Выделена память для CPU массива");
    TEST_ASSERT(is_prime_gpu != NULL, "Выделена память для GPU массива");
    
    if (!is_prime_cpu || !is_prime_gpu) {
        SAFE_FREE(is_prime_cpu);
        SAFE_FREE(is_prime_gpu);
        return;
    }

    /* CPU версия */
    clock_t cpu_start = clock();
    unsigned long count_cpu = sieve_cpu(is_prime_cpu, limit);
    clock_t cpu_end = clock();
    double cpu_time_ms = ((double)(cpu_end - cpu_start)) / CLOCKS_PER_SEC * 1000.0;
    
    /* GPU версия */
    double gpu_time = 0;
    unsigned long count_gpu = sieve_gpu(is_prime_gpu, limit, 256, 0, &gpu_time, DEVICE_GPU);
    
    /* Сравнение количества */
    TEST_ASSERT_EQUAL(count_cpu, count_gpu, "Количество простых чисел должно совпадать");
    
    /* Сравнение массивов (выборочно для производительности) */
    TEST_ASSERT(arrays_equal(is_prime_cpu, is_prime_gpu, limit + 1),
                "Массивы CPU и GPU должны совпадать");
    
    double speedup = gpu_time > 0 ? cpu_time_ms / gpu_time : 0;
    printf("    Найдено простых: %lu\n", count_cpu);
    printf("    CPU время: %.3f мс\n", cpu_time_ms);
    printf("    GPU время: %.3f мс\n", gpu_time);
    printf("    Ускорение: %.2fx\n", speedup);
    
    SAFE_FREE(is_prime_cpu);
    SAFE_FREE(is_prime_gpu);
    TEST_END();
}

/* Тест: Проверка первых простых чисел (CPU vs GPU) */
void test_sieve_first_primes_cpu_gpu(void) {
    TEST_BEGIN("Sieve first primes CPU vs GPU");

    unsigned long limit = 100;
    unsigned char* is_prime_cpu = (unsigned char*)calloc(limit + 1, sizeof(unsigned char));
    unsigned char* is_prime_gpu = (unsigned char*)calloc(limit + 1, sizeof(unsigned char));
    
    TEST_ASSERT(is_prime_cpu != NULL, "Выделена память для CPU массива");
    TEST_ASSERT(is_prime_gpu != NULL, "Выделена память для GPU массива");
    
    if (!is_prime_cpu || !is_prime_gpu) {
        SAFE_FREE(is_prime_cpu);
        SAFE_FREE(is_prime_gpu);
        return;
    }

    /* CPU версия */
    sieve_cpu(is_prime_cpu, limit);
    
    /* GPU версия */
    sieve_gpu(is_prime_gpu, limit, 64, 0, NULL, DEVICE_GPU);
    
    /* Проверка первых 10 простых чисел */
    int expected_primes[] = {2, 3, 5, 7, 11, 13, 17, 19, 23, 29};
    
    for (int i = 0; i < 10; i++) {
        int p = expected_primes[i];
        TEST_ASSERT(is_prime_cpu[p] == is_prime_gpu[p],
                    "Статус простого числа должен совпадать");
    }
    
    /* Проверка составных чисел */
    int expected_composite[] = {0, 1, 4, 6, 8, 9, 10, 12, 14, 15};
    for (int i = 0; i < 10; i++) {
        int c = expected_composite[i];
        TEST_ASSERT(is_prime_cpu[c] == is_prime_gpu[c],
                    "Статус составного числа должен совпадать");
    }
    
    SAFE_FREE(is_prime_cpu);
    SAFE_FREE(is_prime_gpu);
    TEST_END();
}

/* Тест: Разные размеры work-group */
void test_sieve_different_work_groups(void) {
    TEST_BEGIN("Sieve different work-group sizes");

    unsigned long limit = 500000;
    unsigned char* is_prime_cpu = (unsigned char*)calloc(limit + 1, sizeof(unsigned char));
    unsigned char* is_prime_gpu_64 = (unsigned char*)calloc(limit + 1, sizeof(unsigned char));
    unsigned char* is_prime_gpu_256 = (unsigned char*)calloc(limit + 1, sizeof(unsigned char));
    
    TEST_ASSERT(is_prime_cpu != NULL, "Выделена память для CPU массива");
    TEST_ASSERT(is_prime_gpu_64 != NULL, "Выделена память для GPU массива (wg=64)");
    TEST_ASSERT(is_prime_gpu_256 != NULL, "Выделена память для GPU массива (wg=256)");
    
    if (!is_prime_cpu || !is_prime_gpu_64 || !is_prime_gpu_256) {
        SAFE_FREE(is_prime_cpu);
        SAFE_FREE(is_prime_gpu_64);
        SAFE_FREE(is_prime_gpu_256);
        return;
    }

    /* CPU версия */
    unsigned long count_cpu = sieve_cpu(is_prime_cpu, limit);
    
    /* GPU с work-group = 64 */
    double time_64 = 0;
    unsigned long count_64 = sieve_gpu(is_prime_gpu_64, limit, 64, 0, &time_64, DEVICE_GPU);
    
    /* GPU с work-group = 256 */
    double time_256 = 0;
    unsigned long count_256 = sieve_gpu(is_prime_gpu_256, limit, 256, 0, &time_256, DEVICE_GPU);
    
    /* Сравнение количества */
    TEST_ASSERT_EQUAL(count_cpu, count_64, "WG=64: количество должно совпадать");
    TEST_ASSERT_EQUAL(count_cpu, count_256, "WG=256: количество должно совпадать");
    
    /* Сравнение массивов */
    TEST_ASSERT(arrays_equal(is_prime_cpu, is_prime_gpu_64, limit + 1),
                "WG=64: массивы должны совпадать");
    TEST_ASSERT(arrays_equal(is_prime_cpu, is_prime_gpu_256, limit + 1),
                "WG=256: массивы должны совпадать");
    
    printf("    Найдено простых: %lu\n", count_cpu);
    printf("    WG=64:  %.3f мс\n", time_64);
    printf("    WG=256: %.3f мс\n", time_256);
    
    SAFE_FREE(is_prime_cpu);
    SAFE_FREE(is_prime_gpu_64);
    SAFE_FREE(is_prime_gpu_256);
    TEST_END();
}

/* Тест: Производительность CPU vs GPU */
void test_sieve_performance_cpu_gpu(void) {
    TEST_BEGIN("Sieve performance CPU vs GPU");

    unsigned long limit = 10000000;  /* 10 миллионов */
    unsigned char* is_prime_cpu = (unsigned char*)calloc(limit + 1, sizeof(unsigned char));
    unsigned char* is_prime_gpu = (unsigned char*)calloc(limit + 1, sizeof(unsigned char));
    
    TEST_ASSERT(is_prime_cpu != NULL, "Выделена память для CPU массива");
    TEST_ASSERT(is_prime_gpu != NULL, "Выделена память для GPU массива");
    
    if (!is_prime_cpu || !is_prime_gpu) {
        SAFE_FREE(is_prime_cpu);
        SAFE_FREE(is_prime_gpu);
        return;
    }

    /* CPU версия */
    clock_t cpu_start = clock();
    unsigned long count_cpu = sieve_cpu(is_prime_cpu, limit);
    clock_t cpu_end = clock();
    double cpu_time_ms = ((double)(cpu_end - cpu_start)) / CLOCKS_PER_SEC * 1000.0;
    
    /* GPU версия */
    double gpu_time = 0;
    unsigned long count_gpu = sieve_gpu(is_prime_gpu, limit, 256, 0, &gpu_time, DEVICE_GPU);
    
    /* Сравнение количества */
    TEST_ASSERT_EQUAL(count_cpu, count_gpu, "Количество должно совпадать");
    
    /* Сравнение массивов (выборочно для больших N) */
    TEST_ASSERT(arrays_equal(is_prime_cpu, is_prime_gpu, limit + 1),
                "Массивы должны совпадать");
    
    double speedup = gpu_time > 0 ? cpu_time_ms / gpu_time : 0;
    
    /* Теоретическое приближение */
    double approx = (double)limit / log((double)limit);
    double error = fabs((double)count_cpu - approx) / approx * 100.0;
    
    printf("    Найдено простых: %lu\n", count_cpu);
    printf("    Теор. ожидание:  %.0f\n", approx);
    printf("    Отклонение:      %.2f%%\n", error);
    printf("    CPU время:       %.3f мс\n", cpu_time_ms);
    printf("    GPU время:       %.3f мс\n", gpu_time);
    printf("    Ускорение:       %.2fx\n", speedup);
    
    SAFE_FREE(is_prime_cpu);
    SAFE_FREE(is_prime_gpu);
    TEST_END();
}

/* =============================================================================
 * Главная функция
 * ============================================================================= */

int main(void) {
    printf("========================================\n");
    printf("Интеграционные тесты: CPU vs GPU (Sieve)\n");
    printf("========================================\n\n");

    test_sieve_first_primes_cpu_gpu();
    test_sieve_cpu_gpu_small();
    test_sieve_cpu_gpu_medium();
    test_sieve_cpu_gpu_large();
    test_sieve_different_work_groups();
    test_sieve_performance_cpu_gpu();

    printf("\n========================================\n");
    test_summary();
    printf("========================================\n");

    return (test_failures > 0) ? 1 : 0;
}
