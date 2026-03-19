/*
 * Интеграционные тесты: Сравнение CPU vs GPU для хэширования
 *
 * Компиляция:
 *   gcc -o test_hash_correctness test_hash_correctness.c \
 *       -I.. -I../hashing -I../include ../hashing/hash.c ../src/cl_utils.c \
 *       -lOpenCL -lm
 *
 * Запуск:
 *   ./test_hash_correctness
 */

#include "test_common.h"
#include <stdint.h>

/* Внешние функции из hash.c */
extern void sha256_cpu(const uint8_t* data, size_t len, uint8_t* hash);
extern void hash_all_cpu(const uint8_t* data, const uint32_t* lens,
                         uint8_t* hashes, uint32_t num_hashes, uint32_t max_len);

extern int hash_gpu(const uint8_t* data, const uint32_t* lens, uint8_t* hashes,
                    uint32_t num_hashes, uint32_t max_len, size_t local_size,
                    int print_info, double* kernel_time_ms);

/* Вспомогательная функция для сравнения хэшей */
static int hash_equal(const uint8_t* a, const uint8_t* b, size_t len) {
    for (size_t i = 0; i < len; i++) {
        if (a[i] != b[i]) return 0;
    }
    return 1;
}

/* Вспомогательная функция для вывода хэша */
static void print_hash_hex(const uint8_t* hash, size_t len) {
    for (size_t i = 0; i < len; i++) {
        printf("%02x", hash[i]);
    }
}

/* Тест: Сравнение CPU и GPU для одного хэша */
void test_hash_single_cpu_gpu(void) {
    TEST_BEGIN("Single hash CPU vs GPU");

    const char* input = "Hello, OpenCL!";
    size_t len = strlen(input);
    
    uint8_t hash_cpu[32];
    uint8_t hash_gpu[32];
    
    /* CPU версия */
    sha256_cpu((const uint8_t*)input, len, hash_cpu);
    
    /* GPU версия */
    uint32_t data_len = (uint32_t)len;
    double kernel_time = 0;
    int result = hash_gpu(
        (const uint8_t*)input,
        &data_len,
        hash_gpu,
        1,
        (uint32_t)len,
        64,
        0,  /* не выводить информацию об устройстве */
        &kernel_time
    );
    
    TEST_ASSERT(result == 0, "GPU хэширование выполнено успешно");
    TEST_ASSERT(hash_equal(hash_cpu, hash_gpu, 32), 
                "Результаты CPU и GPU совпадают");
    
    if (!test_failures) {
        printf("    CPU: ");
        print_hash_hex(hash_cpu, 32);
        printf("\n    GPU: ");
        print_hash_hex(hash_gpu, 32);
        printf("\n    Время GPU: %.3f мс\n", kernel_time);
    }
    
    TEST_END();
}

/* Тест: Сравнение CPU и GPU для множества хэшей */
void test_hash_multiple_cpu_gpu(void) {
    TEST_BEGIN("Multiple hashes CPU vs GPU");

    const uint32_t num_hashes = 1000;
    const uint32_t max_len = 64;
    
    /* Выделение памяти */
    uint8_t* data = (uint8_t*)calloc(num_hashes * max_len, sizeof(uint8_t));
    uint32_t* lens = (uint32_t*)calloc(num_hashes, sizeof(uint32_t));
    uint8_t* hashes_cpu = (uint8_t*)calloc(num_hashes * 32, sizeof(uint8_t));
    uint8_t* hashes_gpu = (uint8_t*)calloc(num_hashes * 32, sizeof(uint8_t));
    
    TEST_ASSERT(data != NULL, "Выделена память для data");
    TEST_ASSERT(lens != NULL, "Выделена память для lens");
    TEST_ASSERT(hashes_cpu != NULL, "Выделена память для hashes_cpu");
    TEST_ASSERT(hashes_gpu != NULL, "Выделена память для hashes_gpu");
    
    if (!data || !lens || !hashes_cpu || !hashes_gpu) {
        SAFE_FREE(data);
        SAFE_FREE(lens);
        SAFE_FREE(hashes_cpu);
        SAFE_FREE(hashes_gpu);
        return;
    }
    
    /* Генерация тестовых данных */
    srand(42);
    for (uint32_t i = 0; i < num_hashes; i++) {
        lens[i] = 8 + (rand() % (max_len - 7));
        for (uint32_t j = 0; j < lens[i]; j++) {
            data[i * max_len + j] = (uint8_t)(rand() % 256);
        }
    }
    
    /* CPU версия */
    hash_all_cpu(data, lens, hashes_cpu, num_hashes, max_len);
    
    /* GPU версия */
    double kernel_time = 0;
    int result = hash_gpu(data, lens, hashes_gpu, num_hashes, max_len, 
                          256, 0, &kernel_time);
    
    TEST_ASSERT(result == 0, "GPU хэширование выполнено успешно");
    
    /* Сравнение результатов */
    int all_match = 1;
    uint32_t first_error = 0;
    
    for (uint32_t i = 0; i < num_hashes; i++) {
        if (!hash_equal(hashes_cpu + i * 32, hashes_gpu + i * 32, 32)) {
            all_match = 0;
            first_error = i;
            break;
        }
    }
    
    TEST_ASSERT(all_match, "Все хэши CPU и GPU совпадают");
    
    if (!all_match) {
        printf("    Первое несовпадение на индексе %u:\n", first_error);
        printf("    CPU: ");
        print_hash_hex(hashes_cpu + first_error * 32, 32);
        printf("\n    GPU: ");
        print_hash_hex(hashes_gpu + first_error * 32, 32);
        printf("\n");
    }
    
    /* Освобождение памяти */
    SAFE_FREE(data);
    SAFE_FREE(lens);
    SAFE_FREE(hashes_cpu);
    SAFE_FREE(hashes_gpu);
    
    TEST_END();
}

/* Тест: Пустая строка CPU vs GPU */
void test_hash_empty_cpu_gpu(void) {
    TEST_BEGIN("Empty string CPU vs GPU");

    const char* input = "";
    
    uint8_t hash_cpu[32];
    uint8_t hash_gpu[32];
    uint32_t data_len = 0;
    
    /* Ожидаемый хэш для пустой строки */
    const uint8_t expected[32] = {
        0xe3, 0xb0, 0xc4, 0x42, 0x98, 0xfc, 0x1c, 0x14,
        0x9a, 0xfb, 0xf4, 0xc8, 0x99, 0x6f, 0xb9, 0x24,
        0x27, 0xae, 0x41, 0xe4, 0x64, 0x9b, 0x93, 0x4c,
        0xa4, 0x95, 0x99, 0x1b, 0x78, 0x52, 0xb8, 0x55
    };
    
    sha256_cpu((const uint8_t*)input, 0, hash_cpu);
    
    double kernel_time = 0;
    int result = hash_gpu((const uint8_t*)input, &data_len, hash_gpu, 
                          1, 0, 64, 0, &kernel_time);
    
    TEST_ASSERT(result == 0, "GPU хэширование выполнено успешно");
    TEST_ASSERT(hash_equal(hash_cpu, expected, 32), "CPU хэш совпадает с ожидаемым");
    TEST_ASSERT(hash_equal(hash_gpu, expected, 32), "GPU хэш совпадает с ожидаемым");
    TEST_ASSERT(hash_equal(hash_cpu, hash_gpu, 32), "CPU и GPU хэши совпадают");
    
    TEST_END();
}

/* Тест: Длинные данные (множественные блоки) CPU vs GPU */
void test_hash_long_cpu_gpu(void) {
    TEST_BEGIN("Long data (multiple blocks) CPU vs GPU");

    const size_t data_len = 1000;
    uint8_t* data = (uint8_t*)calloc(data_len, sizeof(uint8_t));
    
    TEST_ASSERT(data != NULL, "Выделена память для данных");
    if (!data) return;
    
    /* Заполняем данными */
    memset(data, 'a', data_len);
    
    uint32_t len = (uint32_t)data_len;
    uint8_t hash_cpu[32];
    uint8_t hash_gpu[32];
    
    /* Ожидаемый хэш для 1000 'a' */
    const uint8_t expected[32] = {
        0x29, 0x69, 0x5e, 0xed, 0x0c, 0xf8, 0x6f, 0x89,
        0x5e, 0x0d, 0x6d, 0x1a, 0x29, 0x34, 0xcd, 0x3d,
        0x22, 0x83, 0x1b, 0x94, 0x4f, 0xa7, 0x5a, 0x2d,
        0x4e, 0x15, 0xb7, 0xd5, 0x95, 0x1b, 0x93, 0x3e
    };
    
    sha256_cpu(data, data_len, hash_cpu);
    
    double kernel_time = 0;
    int result = hash_gpu(data, &len, hash_gpu, 1, len, 64, 0, &kernel_time);
    
    TEST_ASSERT(result == 0, "GPU хэширование выполнено успешно");
    TEST_ASSERT(hash_equal(hash_cpu, expected, 32), "CPU хэш совпадает с ожидаемым");
    TEST_ASSERT(hash_equal(hash_gpu, expected, 32), "GPU хэш совпадает с ожидаемым");
    TEST_ASSERT(hash_equal(hash_cpu, hash_gpu, 32), "CPU и GPU хэши совпадают");
    
    SAFE_FREE(data);
    TEST_END();
}

/* Тест: Производительность CPU vs GPU */
void test_hash_performance_cpu_gpu(void) {
    TEST_BEGIN("Performance comparison CPU vs GPU");

    const uint32_t num_hashes = 100000;
    const uint32_t max_len = 64;
    
    /* Выделение памяти */
    uint8_t* data = (uint8_t*)calloc(num_hashes * max_len, sizeof(uint8_t));
    uint32_t* lens = (uint32_t*)calloc(num_hashes, sizeof(uint32_t));
    uint8_t* hashes_cpu = (uint8_t*)calloc(num_hashes * 32, sizeof(uint8_t));
    uint8_t* hashes_gpu = (uint8_t*)calloc(num_hashes * 32, sizeof(uint8_t));
    
    TEST_ASSERT(data != NULL, "Выделена память для data");
    TEST_ASSERT(lens != NULL, "Выделена память для lens");
    TEST_ASSERT(hashes_cpu != NULL, "Выделена память для hashes_cpu");
    TEST_ASSERT(hashes_gpu != NULL, "Выделена память для hashes_gpu");
    
    if (!data || !lens || !hashes_cpu || !hashes_gpu) {
        SAFE_FREE(data);
        SAFE_FREE(lens);
        SAFE_FREE(hashes_cpu);
        SAFE_FREE(hashes_gpu);
        return;
    }
    
    /* Генерация тестовых данных */
    srand(42);
    for (uint32_t i = 0; i < num_hashes; i++) {
        lens[i] = 8 + (rand() % (max_len - 7));
        for (uint32_t j = 0; j < lens[i]; j++) {
            data[i * max_len + j] = (uint8_t)(rand() % 256);
        }
    }
    
    /* CPU версия */
    clock_t cpu_start = clock();
    hash_all_cpu(data, lens, hashes_cpu, num_hashes, max_len);
    clock_t cpu_end = clock();
    double cpu_time_ms = ((double)(cpu_end - cpu_start)) / CLOCKS_PER_SEC * 1000.0;
    
    /* GPU версия */
    double gpu_kernel_time = 0;
    int result = hash_gpu(data, lens, hashes_gpu, num_hashes, max_len, 
                          256, 0, &gpu_kernel_time);
    
    TEST_ASSERT(result == 0, "GPU хэширование выполнено успешно");
    
    /* Сравнение результатов */
    int all_match = 1;
    for (uint32_t i = 0; i < num_hashes && all_match; i++) {
        if (!hash_equal(hashes_cpu + i * 32, hashes_gpu + i * 32, 32)) {
            all_match = 0;
        }
    }
    
    TEST_ASSERT(all_match, "Все хэши совпадают");
    
    double speedup = gpu_kernel_time > 0 ? cpu_time_ms / gpu_kernel_time : 0;
    
    printf("    CPU время:        %.3f мс\n", cpu_time_ms);
    printf("    GPU время (kernel): %.3f мс\n", gpu_kernel_time);
    printf("    Ускорение:        %.2fx\n", speedup);
    
    /* Освобождение памяти */
    SAFE_FREE(data);
    SAFE_FREE(lens);
    SAFE_FREE(hashes_cpu);
    SAFE_FREE(hashes_gpu);
    
    TEST_END();
}

/* Тест: Разные размеры work-group */
void test_hash_different_work_groups(void) {
    TEST_BEGIN("Different work-group sizes");

    const uint32_t num_hashes = 10000;
    const uint32_t max_len = 64;
    
    uint8_t* data = (uint8_t*)calloc(num_hashes * max_len, sizeof(uint8_t));
    uint32_t* lens = (uint32_t*)calloc(num_hashes, sizeof(uint32_t));
    uint8_t* hashes_cpu = (uint8_t*)calloc(num_hashes * 32, sizeof(uint8_t));
    uint8_t* hashes_gpu_32 = (uint8_t*)calloc(num_hashes * 32, sizeof(uint8_t));
    uint8_t* hashes_gpu_256 = (uint8_t*)calloc(num_hashes * 32, sizeof(uint8_t));
    
    TEST_ASSERT(data != NULL, "Выделена память для data");
    TEST_ASSERT(lens != NULL, "Выделена память для lens");
    TEST_ASSERT(hashes_cpu != NULL, "Выделена память для hashes_cpu");
    TEST_ASSERT(hashes_gpu_32 != NULL, "Выделена память для hashes_gpu_32");
    TEST_ASSERT(hashes_gpu_256 != NULL, "Выделена память для hashes_gpu_256");
    
    if (!data || !lens || !hashes_cpu || !hashes_gpu_32 || !hashes_gpu_256) {
        SAFE_FREE(data);
        SAFE_FREE(lens);
        SAFE_FREE(hashes_cpu);
        SAFE_FREE(hashes_gpu_32);
        SAFE_FREE(hashes_gpu_256);
        return;
    }
    
    /* Генерация данных */
    srand(42);
    for (uint32_t i = 0; i < num_hashes; i++) {
        lens[i] = 8 + (rand() % (max_len - 7));
        for (uint32_t j = 0; j < lens[i]; j++) {
            data[i * max_len + j] = (uint8_t)(rand() % 256);
        }
    }
    
    /* CPU версия */
    hash_all_cpu(data, lens, hashes_cpu, num_hashes, max_len);
    
    /* GPU с work-group = 32 */
    double time_32 = 0;
    int r1 = hash_gpu(data, lens, hashes_gpu_32, num_hashes, max_len, 32, 0, &time_32);
    
    /* GPU с work-group = 256 */
    double time_256 = 0;
    int r2 = hash_gpu(data, lens, hashes_gpu_256, num_hashes, max_len, 256, 0, &time_256);
    
    TEST_ASSERT(r1 == 0, "GPU (wg=32) хэширование выполнено успешно");
    TEST_ASSERT(r2 == 0, "GPU (wg=256) хэширование выполнено успешно");
    
    /* Сравнение */
    int match_32 = 1, match_256 = 1;
    for (uint32_t i = 0; i < num_hashes; i++) {
        if (!hash_equal(hashes_cpu + i * 32, hashes_gpu_32 + i * 32, 32))
            match_32 = 0;
        if (!hash_equal(hashes_cpu + i * 32, hashes_gpu_256 + i * 32, 32))
            match_256 = 0;
    }
    
    TEST_ASSERT(match_32, "WG=32: результаты совпадают с CPU");
    TEST_ASSERT(match_256, "WG=256: результаты совпадают с CPU");
    
    printf("    WG=32:  %.3f мс\n", time_32);
    printf("    WG=256: %.3f мс\n", time_256);
    
    SAFE_FREE(data);
    SAFE_FREE(lens);
    SAFE_FREE(hashes_cpu);
    SAFE_FREE(hashes_gpu_32);
    SAFE_FREE(hashes_gpu_256);
    
    TEST_END();
}

/* =============================================================================
 * Главная функция
 * ============================================================================= */

int main(void) {
    printf("========================================\n");
    printf("Интеграционные тесты: CPU vs GPU (Hash)\n");
    printf("========================================\n\n");

    test_hash_single_cpu_gpu();
    test_hash_empty_cpu_gpu();
    test_hash_long_cpu_gpu();
    test_hash_multiple_cpu_gpu();
    test_hash_different_work_groups();
    test_hash_performance_cpu_gpu();

    printf("\n========================================\n");
    test_summary();
    printf("========================================\n");

    return (test_failures > 0) ? 1 : 0;
}
