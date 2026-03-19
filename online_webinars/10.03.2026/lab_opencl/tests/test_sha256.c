/*
 * Unit-тесты для SHA-256
 * 
 * Компиляция:
 *   gcc -o test_sha256 test_sha256.c -I.. -I../hashing -lm
 * 
 * Запуск:
 *   ./test_sha256
 */

#include "test_common.h"
#include <stdint.h>

/* Внешние функции из hash.c */
extern void sha256_cpu(const uint8_t* data, size_t len, uint8_t* hash);

/* Вспомогательная функция для сравнения хэшей */
static int hash_equal(const uint8_t* a, const uint8_t* b) {
    for (int i = 0; i < 32; i++) {
        if (a[i] != b[i]) return 0;
    }
    return 1;
}

/* Вспомогательная функция для вывода хэша */
static void print_hash(const uint8_t* hash) {
    for (int i = 0; i < 32; i++) {
        printf("%02x", hash[i]);
    }
    printf("\n");
}

/* Тест: SHA-256 пустой строки */
void test_sha256_empty(void) {
    TEST_BEGIN("SHA-256 empty string");
    
    /* Ожидаемый хэш для пустой строки */
    const uint8_t expected[32] = {
        0xe3, 0xb0, 0xc4, 0x42, 0x98, 0xfc, 0x1c, 0x14,
        0x9a, 0xfb, 0xf4, 0xc8, 0x99, 0x6f, 0xb9, 0x24,
        0x27, 0xae, 0x41, 0xe4, 0x64, 0x9b, 0x93, 0x4c,
        0xa4, 0x95, 0x99, 0x1b, 0x78, 0x52, 0xb8, 0x55
    };
    
    uint8_t hash[32];
    sha256_cpu((const uint8_t*)"", 0, hash);
    
    TEST_ASSERT(hash_equal(hash, expected), "Empty string hash should match");
    TEST_END();
}

/* Тест: SHA-256 "abc" */
void test_sha256_abc(void) {
    TEST_BEGIN("SHA-256 'abc'");
    
    /* Ожидаемый хэш для "abc" */
    const uint8_t expected[32] = {
        0xba, 0x78, 0x16, 0xbf, 0x8f, 0x01, 0xcf, 0xea,
        0x41, 0x41, 0x40, 0xde, 0x5d, 0xae, 0x22, 0x23,
        0xb0, 0x03, 0x61, 0xa3, 0x96, 0x17, 0x7a, 0x9c,
        0xb4, 0x10, 0xff, 0x61, 0xf2, 0x00, 0x15, 0xad
    };
    
    uint8_t hash[32];
    sha256_cpu((const uint8_t*)"abc", 3, hash);
    
    TEST_ASSERT(hash_equal(hash, expected), "'abc' hash should match");
    TEST_END();
}

/* Тест: SHA-256 длинной строки */
void test_sha256_long(void) {
    TEST_BEGIN("SHA-256 long string");
    
    /* "abcdbcdecdefdefgefghfghighijhijkijkljklmklmnlmnomnopnopq" */
    const char* input = "abcdbcdecdefdefgefghfghighijhijkijkljklmklmnlmnomnopnopq";
    
    const uint8_t expected[32] = {
        0x24, 0x8d, 0x6a, 0x61, 0xd2, 0x06, 0x38, 0xb8,
        0xe5, 0xc0, 0x26, 0x93, 0x0c, 0x3e, 0x60, 0x39,
        0xa3, 0x3c, 0xe4, 0x59, 0x64, 0xff, 0x21, 0x67,
        0xf6, 0xec, 0xed, 0xd4, 0x19, 0xdb, 0x06, 0xc1
    };
    
    uint8_t hash[32];
    sha256_cpu((const uint8_t*)input, strlen(input), hash);
    
    TEST_ASSERT(hash_equal(hash, expected), "Long string hash should match");
    TEST_END();
}

/* Тест: SHA-256 очень длинной строки (множественные блоки) */
void test_sha256_very_long(void) {
    TEST_BEGIN("SHA-256 very long string (multiple blocks)");

    /* Строка из 1000 'a' */
    char input[1001];
    memset(input, 'a', 1000);
    input[1000] = '\0';

    /* Ожидаемый хэш для 1000 'a' (проверено через Python hashlib) */
    const uint8_t expected[32] = {
        0x41, 0xed, 0xec, 0xe4, 0x2d, 0x63, 0xe8, 0xd9,
        0xbf, 0x51, 0x5a, 0x9b, 0xa6, 0x93, 0x2e, 0x1c,
        0x20, 0xcb, 0xc9, 0xf5, 0xa5, 0xd1, 0x34, 0x64,
        0x5a, 0xdb, 0x5d, 0xb1, 0xb9, 0x73, 0x7e, 0xa3
    };

    uint8_t hash[32];
    sha256_cpu((const uint8_t*)input, 1000, hash);

    TEST_ASSERT(hash_equal(hash, expected), "1000 'a' hash should match");
    TEST_END();
}

/* Тест: SHA-256 детерминированность */
void test_sha256_deterministic(void) {
    TEST_BEGIN("SHA-256 deterministic");
    
    const char* input = "test string";
    uint8_t hash1[32], hash2[32];
    
    sha256_cpu((const uint8_t*)input, strlen(input), hash1);
    sha256_cpu((const uint8_t*)input, strlen(input), hash2);
    
    TEST_ASSERT(hash_equal(hash1, hash2), "Same input should produce same hash");
    TEST_END();
}

/* Тест: SHA-256 лавинный эффект */
void test_sha256_avalanche(void) {
    TEST_BEGIN("SHA-256 avalanche effect");
    
    const char* input1 = "test";
    const char* input2 = "tEst";  /* Одна буква изменена */
    
    uint8_t hash1[32], hash2[32];
    sha256_cpu((const uint8_t*)input1, strlen(input1), hash1);
    sha256_cpu((const uint8_t*)input2, strlen(input2), hash2);
    
    /* Подсчёт отличающихся битов */
    int diff_bits = 0;
    for (int i = 0; i < 32; i++) {
        uint8_t diff = hash1[i] ^ hash2[i];
        while (diff) {
            diff_bits += diff & 1;
            diff >>= 1;
        }
    }
    
    /* Ожидаем примерно 50% отличающихся битов (128 из 256) */
    /* Допускаем диапазон 64-192 (25%-75%) */
    TEST_ASSERT(diff_bits >= 64 && diff_bits <= 192, 
                "Small input change should cause significant hash change");
    TEST_END();
}

int main(void) {
    printf("========================================\n");
    printf("SHA-256 Unit Tests\n");
    printf("========================================\n\n");

    test_sha256_empty();
    test_sha256_abc();
    test_sha256_long();
    test_sha256_very_long();
    test_sha256_deterministic();
    test_sha256_avalanche();

    test_summary();

    return (test_failures > 0) ? 1 : 0;
}
