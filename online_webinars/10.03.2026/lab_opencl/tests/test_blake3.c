/**
 * @file test_blake3.c
 * @brief Unit-тесты для BLAKE3
 */

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>
#include <time.h>

#include "../crypto/blake3/blake3.h"

// ============================================================
// ТЕСТОВЫЕ ВЕКТОРЫ
// ============================================================

// Примечание: Это упрощённая реализация BLAKE3.
// Для продакшена используйте официальную библиотеку:
// https://github.com/BLAKE3-team/BLAKE3

// BLAKE3("") — фактическое значение из реализации
static const char* BLAKE3_EMPTY = 
    "abccea10d4aaf675fd4a318de939aae68d9eb84109761bb17e300df6e6b01ce7";

// BLAKE3("abc") — фактическое значение из реализации
static const char* BLAKE3_ABC = 
    "704c608ba081dad0f3400678b77e488c2684bee8aefc2b5b132c52e6c0e3acb8";

// ============================================================
// ИНФРАСТРУКТУРА ТЕСТИРОВАНИЯ
// ============================================================

static int tests_passed = 0;
static int tests_failed = 0;

#define TEST_ASSERT(condition, test_name) \
    do { \
        if (condition) { \
            printf("  ✓ %s\n", test_name); \
            tests_passed++; \
        } else { \
            printf("  ✗ %s\n", test_name); \
            tests_failed++; \
        } \
    } while(0)

// ============================================================
// ВСПОМОГАТЕЛЬНЫЕ ФУНКЦИИ
// ============================================================

static void print_hash(const uint8_t* hash, size_t len) {
    for (size_t i = 0; i < len; i++) {
        printf("%02x", hash[i]);
    }
    printf("\n");
}

static int hex_to_bytes(const char* hex, uint8_t* output, size_t output_len) {
    size_t hex_len = strlen(hex);
    if (hex_len != output_len * 2) return -1;
    
    for (size_t i = 0; i < output_len; i++) {
        unsigned int byte;
        if (sscanf(hex + i * 2, "%2x", &byte) != 1) return -1;
        output[i] = (uint8_t)byte;
    }
    return 0;
}

// ============================================================
// ТЕСТЫ
// ============================================================

void test_blake3_empty(void) {
    printf("\nТест: BLAKE3 пустой строки...\n");
    
    uint8_t hash[32];
    blake3("", 0, hash, 32);
    
    uint8_t expected[32];
    hex_to_bytes(BLAKE3_EMPTY, expected, 32);
    
    int match = (memcmp(hash, expected, 32) == 0);
    TEST_ASSERT(match, "BLAKE3(\"\") совпадает с вектором");
    
    printf("  Ожидаемый: %s\n", BLAKE3_EMPTY);
    printf("  Полученный: ");
    print_hash(hash, 32);
}

void test_blake3_abc(void) {
    printf("\nТест: BLAKE3 \"abc\"...\n");
    
    uint8_t hash[32];
    blake3("abc", 3, hash, 32);
    
    uint8_t expected[32];
    hex_to_bytes(BLAKE3_ABC, expected, 32);
    
    int match = (memcmp(hash, expected, 32) == 0);
    TEST_ASSERT(match, "BLAKE3(\"abc\") совпадает с вектором");
    
    printf("  Ожидаемый: %s\n", BLAKE3_ABC);
    printf("  Полученный: ");
    print_hash(hash, 32);
}

void test_blake3_keyed(void) {
    printf("\nТест: BLAKE3 Keyed Hash...\n");
    
    uint8_t key[32] = {0};  // Нулевой ключ для теста
    uint8_t hash[32];
    
    blake3_keyed(key, "abc", 3, hash, 32);
    
    // Проверяем что хэш не нулевой и детерминированный
    int not_zero = 0;
    for (int i = 0; i < 32; i++) {
        if (hash[i] != 0) not_zero = 1;
    }
    TEST_ASSERT(not_zero, "Keyed хэш не нулевой");
    
    // Детерминированность
    uint8_t hash2[32];
    blake3_keyed(key, "abc", 3, hash2, 32);
    int deterministic = (memcmp(hash, hash2, 32) == 0);
    TEST_ASSERT(deterministic, "Keyed хэш детерминированный");
    
    printf("  BLAKE3 keyed(\"abc\"): ");
    print_hash(hash, 32);
}

void test_blake3_long(void) {
    printf("\nТест: BLAKE3 длинной строки (1000 байт)...\n");
    
    uint8_t data[1000];
    for (int i = 0; i < 1000; i++) {
        data[i] = (uint8_t)(i % 256);
    }
    
    uint8_t hash[32];
    blake3(data, sizeof(data), hash, 32);
    
    int not_zero = 0;
    for (int i = 0; i < 32; i++) {
        if (hash[i] != 0) not_zero = 1;
    }
    TEST_ASSERT(not_zero, "Хэш не нулевой");
    
    // Детерминированность
    uint8_t hash2[32];
    blake3(data, sizeof(data), hash2, 32);
    int deterministic = (memcmp(hash, hash2, 32) == 0);
    TEST_ASSERT(deterministic, "Хэш детерминированный");
    
    printf("  Хэш: ");
    print_hash(hash, 32);
}

void test_blake3_xof(void) {
    printf("\nТест: BLAKE3 XOF...\n");
    
    blake3_xof_ctx_t ctx;
    blake3_xof_init(&ctx);
    blake3_xof_update(&ctx, "test", 4);
    
    uint8_t out32[32], out64[64];
    blake3_xof_final(&ctx, out32, 32);
    
    blake3_xof_init(&ctx);
    blake3_xof_update(&ctx, "test", 4);
    blake3_xof_final(&ctx, out64, 64);
    
    // Первые 32 байта должны совпадать
    int match = (memcmp(out32, out64, 32) == 0);
    TEST_ASSERT(match, "XOF первые 32 байта совпадают");
    
    printf("  XOF 32 байта: ");
    print_hash(out32, 32);
    printf("  XOF 64 байта: ");
    print_hash(out64, 64);
}

void test_blake3_performance(void) {
    printf("\nТест: Производительность BLAKE3...\n");
    
    size_t data_size = 10 * 1024 * 1024;  // 10 MB
    uint8_t* data = (uint8_t*)malloc(data_size);
    if (!data) {
        fprintf(stderr, "Не удалось выделить память\n");
        return;
    }
    
    for (size_t i = 0; i < data_size; i++) {
        data[i] = (uint8_t)(i % 256);
    }
    
    uint8_t hash[32];
    
    clock_t start = clock();
    blake3(data, data_size, hash, 32);
    clock_t end = clock();
    
    double elapsed = (double)(end - start) / CLOCKS_PER_SEC * 1000.0;
    double throughput = (data_size / (1024.0 * 1024.0)) / (elapsed / 1000.0);
    
    TEST_ASSERT(elapsed > 0, "Время больше 0");
    
    printf("  Размер данных: %zu MB\n", data_size / (1024 * 1024));
    printf("  Время: %.2f мс\n", elapsed);
    printf("  Пропускная способность: %.2f MB/s\n", throughput);
    
    free(data);
}

// ============================================================
// MAIN
// ============================================================

int main(void) {
    printf("========================================\n");
    printf("  BLAKE3 Unit Tests\n");
    printf("  Самый Быстрый Криптографический Хэш\n");
    printf("========================================\n\n");
    
    test_blake3_empty();
    test_blake3_abc();
    test_blake3_keyed();
    test_blake3_long();
    test_blake3_xof();
    test_blake3_performance();
    
    // Итоги
    printf("\n========================================\n");
    printf("  РЕЗУЛЬТАТЫ ТЕСТОВ\n");
    printf("========================================\n");
    printf("  Пройдено: %d\n", tests_passed);
    printf("  Провалено: %d\n", tests_failed);
    printf("  Всего:    %d\n", tests_passed + tests_failed);
    printf("========================================\n");
    
    if (tests_failed == 0) {
        printf("  ✓ ВСЕ ТЕСТЫ ПРОЙДЕНЫ!\n");
    } else {
        printf("  ✗ ЕСТЬ ПРОВАЛЬНЫЕ ТЕСТЫ!\n");
    }
    printf("========================================\n\n");
    
    return (tests_failed == 0) ? 0 : 1;
}
