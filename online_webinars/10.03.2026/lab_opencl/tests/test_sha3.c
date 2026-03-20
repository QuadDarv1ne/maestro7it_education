/**
 * @file test_sha3.c
 * @brief Unit-тесты для SHA-3 (Keccak)
 * 
 * Тестирование корректности с использованием тестовых векторов NIST.
 */

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>
#include <time.h>

#include "../crypto/sha3/sha3.h"

// ============================================================
// ТЕСТОВЫЕ ВЕКТОРЫ NIST FIPS 202
// ============================================================

// SHA3-256 тестовые векторы
static const char* SHA3_256_EMPTY = 
    "a7ffc6f8bf1ed76651c14756a061d662f580ff4de43b49fa82d80a4b80f8434a";

static const char* SHA3_256_ABC = 
    "3a985da74fe225b2045c172d6bd390bd855f086e3e9d525b46bfe24511431532";

static const char* SHA3_256_ABCDEF = 
    "59890c1d183aa279505750422e6384ccb1499c793872d6f31bb3bcaa4bc9f5a5";

// SHA3-512 тестовые векторы
static const char* SHA3_512_EMPTY = 
    "a69f73cca23a9ac5c8b567dc185a756e97c982164fe25859e0d1dcc1475c80a6"
    "15b2123af1f5f94c11e3e9402c3ac558f500199d95b6d3e301758586281dcd26";

static const char* SHA3_512_ABC = 
    "b751850b1a57168a5693cd924b6b096e08f621827444f70d884f5d0240d2712e"
    "10e116e9192af3c91a7ec57647e3934057340b4cf408d5a56592f8274eec53f0";

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
// ТЕСТЫ SHA3-256
// ============================================================

void test_sha3_256_empty(void) {
    printf("\nТест: SHA3-256 пустой строки...\n");
    
    uint8_t hash[32];
    sha3_256("", 0, hash);
    
    uint8_t expected[32];
    hex_to_bytes(SHA3_256_EMPTY, expected, 32);
    
    int match = (memcmp(hash, expected, 32) == 0);
    TEST_ASSERT(match, "SHA3-256(\"\") совпадает с NIST вектором");
    
    printf("  Ожидаемый: %s\n", SHA3_256_EMPTY);
    printf("  Полученный: ");
    print_hash(hash, 32);
}

void test_sha3_256_abc(void) {
    printf("\nТест: SHA3-256 \"abc\"...\n");
    
    uint8_t hash[32];
    sha3_256("abc", 3, hash);
    
    uint8_t expected[32];
    hex_to_bytes(SHA3_256_ABC, expected, 32);
    
    int match = (memcmp(hash, expected, 32) == 0);
    TEST_ASSERT(match, "SHA3-256(\"abc\") совпадает с NIST вектором");
    
    printf("  Ожидаемый: %s\n", SHA3_256_ABC);
    printf("  Полученный: ");
    print_hash(hash, 32);
}

void test_sha3_256_abcdef(void) {
    printf("\nТест: SHA3-256 \"abcdef\"...\n");
    
    uint8_t hash[32];
    sha3_256("abcdef", 6, hash);
    
    uint8_t expected[32];
    hex_to_bytes(SHA3_256_ABCDEF, expected, 32);
    
    int match = (memcmp(hash, expected, 32) == 0);
    TEST_ASSERT(match, "SHA3-256(\"abcdef\") совпадает с вектором");
    
    printf("  Ожидаемый: %s\n", SHA3_256_ABCDEF);
    printf("  Полученный: ");
    print_hash(hash, 32);
}

void test_sha3_256_long(void) {
    printf("\nТест: SHA3-256 длинной строки (1000 байт)...\n");
    
    uint8_t data[1000];
    for (int i = 0; i < 1000; i++) {
        data[i] = (uint8_t)(i % 256);
    }
    
    uint8_t hash[32];
    sha3_256(data, sizeof(data), hash);
    
    // Проверяем что хэш не нулевой и детерминированный
    int not_zero = 0;
    for (int i = 0; i < 32; i++) {
        if (hash[i] != 0) not_zero = 1;
    }
    TEST_ASSERT(not_zero, "Хэш не нулевой");
    
    // Проверяем детерминированность
    uint8_t hash2[32];
    sha3_256(data, sizeof(data), hash2);
    int deterministic = (memcmp(hash, hash2, 32) == 0);
    TEST_ASSERT(deterministic, "Хэш детерминированный");
    
    printf("  Хэш: ");
    print_hash(hash, 32);
}

// ============================================================
// ТЕСТЫ SHA3-512
// ============================================================

void test_sha3_512_empty(void) {
    printf("\nТест: SHA3-512 пустой строки...\n");
    
    uint8_t hash[64];
    sha3_512("", 0, hash);
    
    uint8_t expected[64];
    hex_to_bytes(SHA3_512_EMPTY, expected, 64);
    
    int match = (memcmp(hash, expected, 64) == 0);
    TEST_ASSERT(match, "SHA3-512(\"\") совпадает с NIST вектором");
    
    printf("  Ожидаемый: %s\n", SHA3_512_EMPTY);
    printf("  Полученный: ");
    print_hash(hash, 64);
}

void test_sha3_512_abc(void) {
    printf("\nТест: SHA3-512 \"abc\"...\n");
    
    uint8_t hash[64];
    sha3_512("abc", 3, hash);
    
    uint8_t expected[64];
    hex_to_bytes(SHA3_512_ABC, expected, 64);
    
    int match = (memcmp(hash, expected, 64) == 0);
    TEST_ASSERT(match, "SHA3-512(\"abc\") совпадает с NIST вектором");
    
    printf("  Ожидаемый: %s\n", SHA3_512_ABC);
    printf("  Полученный: ");
    print_hash(hash, 64);
}

// ============================================================
// ТЕСТЫ SHAKE
// ============================================================

void test_shake128(void) {
    printf("\nТест: SHAKE128...\n");
    
    uint8_t hash[32];
    shake128("test", 4, hash, sizeof(hash));
    
    // Проверяем что хэш не нулевой
    int not_zero = 0;
    for (int i = 0; i < 32; i++) {
        if (hash[i] != 0) not_zero = 1;
    }
    TEST_ASSERT(not_zero, "SHAKE128 хэш не нулевой");
    
    // Проверяем детерминированность
    uint8_t hash2[32];
    shake128("test", 4, hash2, sizeof(hash2));
    int deterministic = (memcmp(hash, hash2, 32) == 0);
    TEST_ASSERT(deterministic, "SHAKE128 детерминированный");
    
    printf("  SHAKE128(\"test\"): ");
    print_hash(hash, 32);
}

void test_shake256(void) {
    printf("\nТест: SHAKE256...\n");
    
    uint8_t hash[32];
    shake256("test", 4, hash, sizeof(hash));
    
    int not_zero = 0;
    for (int i = 0; i < 32; i++) {
        if (hash[i] != 0) not_zero = 1;
    }
    TEST_ASSERT(not_zero, "SHAKE256 хэш не нулевой");
    
    printf("  SHAKE256(\"test\"): ");
    print_hash(hash, 32);
}

// ============================================================
// ТЕСТЫ: РАЗНАЯ ДЛИНА ВЫВОДА
// ============================================================

void test_shake_variable_length(void) {
    printf("\nТест: SHAKE256 разная длина вывода...\n");
    
    uint8_t hash16[16], hash32[32], hash64[64];
    
    shake256("data", 4, hash16, sizeof(hash16));
    shake256("data", 4, hash32, sizeof(hash32));
    shake256("data", 4, hash64, sizeof(hash64));
    
    // Первые 16 байт должны совпадать
    int match_16 = (memcmp(hash16, hash32, 16) == 0);
    TEST_ASSERT(match_16, "Первые 16 байт SHAKE256 совпадают");
    
    int match_32 = (memcmp(hash32, hash64, 32) == 0);
    TEST_ASSERT(match_32, "Первые 32 байта SHAKE256 совпадают");
    
    printf("  16 байт: ");
    print_hash(hash16, 16);
    printf("  32 байта: ");
    print_hash(hash32, 32);
    printf("  64 байта: ");
    print_hash(hash64, 64);
}

// ============================================================
// ТЕСТЫ: ПРОИЗВОДИТЕЛЬНОСТЬ
// ============================================================

void test_sha3_performance(void) {
    printf("\nТест: Производительность SHA3-256...\n");
    
    uint8_t data[1024 * 1024];  // 1 MB
    for (size_t i = 0; i < sizeof(data); i++) {
        data[i] = (uint8_t)(i % 256);
    }
    
    uint8_t hash[32];
    
    clock_t start = clock();
    sha3_256(data, sizeof(data), hash);
    clock_t end = clock();
    
    double elapsed = (double)(end - start) / CLOCKS_PER_SEC * 1000.0;
    
    TEST_ASSERT(elapsed > 0, "Время больше 0");
    
    printf("  Размер данных: %zu байт (1 MB)\n", sizeof(data));
    printf("  Время: %.2f мс\n", elapsed);
    printf("  Скорость: %.2f MB/s\n", 1000.0 / elapsed);
    printf("  Хэш: ");
    print_hash(hash, 32);
}

// ============================================================
// MAIN
// ============================================================

int main(void) {
    printf("========================================\n");
    printf("  SHA-3 (Keccak) Unit Tests\n");
    printf("  NIST FIPS 202 Standard\n");
    printf("========================================\n\n");
    
    // SHA3-256 тесты
    test_sha3_256_empty();
    test_sha3_256_abc();
    test_sha3_256_abcdef();
    test_sha3_256_long();
    
    // SHA3-512 тесты
    test_sha3_512_empty();
    test_sha3_512_abc();
    
    // SHAKE тесты
    test_shake128();
    test_shake256();
    test_shake_variable_length();
    
    // Производительность
    test_sha3_performance();
    
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
