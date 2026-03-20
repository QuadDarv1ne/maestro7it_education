/**
 * @file test_argon2.c
 * @brief Unit-тесты для Argon2
 * 
 * Тестирование корректности и производительности Argon2.
 */

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>
#include <time.h>

#include "../crypto/argon2/argon2.h"

// ============================================================
// ТЕСТОВЫЕ ДАННЫЕ
// ============================================================

static const char* TEST_PASSWORD = "MySecurePassword123!";
static const uint8_t TEST_SALT[16] = {
    0x01, 0x23, 0x45, 0x67, 0x89, 0xAB, 0xCD, 0xEF,
    0xFE, 0xDC, 0xBA, 0x98, 0x76, 0x54, 0x32, 0x10
};

// Ожидаемые результаты для Argon2id (сгенерированы референсной реализацией)
// Примечание: это примерные значения для демонстрации
static const uint8_t EXPECTED_HASH_SMALL[32] = {
    0x00
};

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

#define TEST_ASSERT_EQUAL(expected, actual, test_name) \
    TEST_ASSERT((expected) == (actual), test_name)

// ============================================================
// ФУНКЦИИ ПЕЧАТИ
// ============================================================

static void print_hash(const uint8_t* hash, size_t len) {
    for (size_t i = 0; i < len; i++) {
        printf("%02x", hash[i]);
    }
    printf("\n");
}

static void print_hex(const void* data, size_t len, const char* label) {
    printf("%s: ", label);
    const uint8_t* bytes = (const uint8_t*)data;
    for (size_t i = 0; i < len; i++) {
        printf("%02x", bytes[i]);
    }
    printf("\n");
}

// ============================================================
// ТЕСТЫ
// ============================================================

/**
 * Тест 1: Базовое хэширование
 */
void test_argon2_basic(void) {
    printf("\nТест: Базовое хэширование Argon2id...\n");
    
    uint8_t hash[32];
    int result = argon2id_hash(TEST_PASSWORD, strlen(TEST_PASSWORD),
                               TEST_SALT, hash);
    
    TEST_ASSERT_EQUAL(0, result, "argon2id_hash вернул успех");
    TEST_ASSERT(hash[0] != 0 || hash[31] != 0, "Хэш не нулевой");
    
    printf("  Хэш: ");
    print_hash(hash, 32);
}

/**
 * Тест 2: Разные параметры
 */
void test_argon2_params(void) {
    printf("\nТест: Разные параметры Argon2...\n");
    
    uint8_t hash1[32], hash2[32];
    
    argon2_params_t params1 = {
        .type = ARGON2_ID,
        .time_cost = 1,
        .memory_cost = 8192,  // 8 MB
        .lanes = 1,
        .hash_len = 32
    };
    
    argon2_params_t params2 = {
        .type = ARGON2_ID,
        .time_cost = 2,
        .memory_cost = 16384,  // 16 MB
        .lanes = 2,
        .hash_len = 32
    };
    
    int r1 = argon2_hash(TEST_PASSWORD, strlen(TEST_PASSWORD),
                         TEST_SALT, sizeof(TEST_SALT),
                         hash1, 32, &params1);
    
    int r2 = argon2_hash(TEST_PASSWORD, strlen(TEST_PASSWORD),
                         TEST_SALT, sizeof(TEST_SALT),
                         hash2, 32, &params2);
    
    TEST_ASSERT_EQUAL(0, r1, "Хэширование с params1 успешно");
    TEST_ASSERT_EQUAL(0, r2, "Хэширование с params2 успешно");
    
    // Разные параметры должны давать разные хэши
    int different = (memcmp(hash1, hash2, 32) != 0);
    TEST_ASSERT(different, "Разные параметры дают разные хэши");
    
    printf("  Params 1 (1 pass, 8MB, 1 lane):  "); print_hash(hash1, 32);
    printf("  Params 2 (2 pass, 16MB, 2 lanes): "); print_hash(hash2, 32);
}

/**
 * Тест 3: Проверка пароля (verify)
 */
void test_argon2_verify(void) {
    printf("\nТест: Проверка пароля (verify)...\n");
    
    uint8_t hash[32];
    argon2_params_t params = {
        .type = ARGON2_ID,
        .time_cost = 1,
        .memory_cost = 8192,
        .lanes = 1,
        .hash_len = 32
    };
    
    // Создаём хэш
    int r1 = argon2_hash(TEST_PASSWORD, strlen(TEST_PASSWORD),
                         TEST_SALT, sizeof(TEST_SALT),
                         hash, 32, &params);
    TEST_ASSERT_EQUAL(0, r1, "Создание хэша успешно");
    
    // Проверяем правильный пароль
    int r2 = argon2_verify(TEST_PASSWORD, strlen(TEST_PASSWORD),
                           TEST_SALT, sizeof(TEST_SALT),
                           hash, 32, &params);
    TEST_ASSERT_EQUAL(0, r2, "Правильный пароль принят");
    
    // Проверяем неправильный пароль
    int r3 = argon2_verify("WrongPassword", 13,
                           TEST_SALT, sizeof(TEST_SALT),
                           hash, 32, &params);
    TEST_ASSERT_EQUAL(-1, r3, "Неправильный пароль отклонён");
    
    // Проверяем с неправильной солью
    uint8_t wrong_salt[16] = {0};
    int r4 = argon2_verify(TEST_PASSWORD, strlen(TEST_PASSWORD),
                           wrong_salt, sizeof(wrong_salt),
                           hash, 32, &params);
    TEST_ASSERT_EQUAL(-1, r4, "Неправильная соль отклонена");
}

/**
 * Тест 4: Разные типы Argon2
 */
void test_argon2_types(void) {
    printf("\nТест: Разные типы Argon2...\n");
    
    uint8_t hash_d[32], hash_i[32], hash_id[32];
    
    argon2_params_t params_d = { .type = ARGON2_D, .time_cost = 1, .memory_cost = 8192, .lanes = 1, .hash_len = 32 };
    argon2_params_t params_i = { .type = ARGON2_I, .time_cost = 1, .memory_cost = 8192, .lanes = 1, .hash_len = 32 };
    argon2_params_t params_id = { .type = ARGON2_ID, .time_cost = 1, .memory_cost = 8192, .lanes = 1, .hash_len = 32 };
    
    argon2_hash(TEST_PASSWORD, strlen(TEST_PASSWORD), TEST_SALT, sizeof(TEST_SALT), hash_d, 32, &params_d);
    argon2_hash(TEST_PASSWORD, strlen(TEST_PASSWORD), TEST_SALT, sizeof(TEST_SALT), hash_i, 32, &params_i);
    argon2_hash(TEST_PASSWORD, strlen(TEST_PASSWORD), TEST_SALT, sizeof(TEST_SALT), hash_id, 32, &params_id);
    
    printf("  Argon2d:  "); print_hash(hash_d, 32);
    printf("  Argon2i:  "); print_hash(hash_i, 32);
    printf("  Argon2id: "); print_hash(hash_id, 32);
    
    // Все три типа должны давать разные хэши
    TEST_ASSERT(memcmp(hash_d, hash_i, 32) != 0, "Argon2d != Argon2i");
    TEST_ASSERT(memcmp(hash_i, hash_id, 32) != 0, "Argon2i != Argon2id");
    TEST_ASSERT(memcmp(hash_d, hash_id, 32) != 0, "Argon2d != Argon2id");
    
    // Названия типов
    TEST_ASSERT(strcmp(argon2_type_name(ARGON2_D), "Argon2d") == 0, "Название Argon2d");
    TEST_ASSERT(strcmp(argon2_type_name(ARGON2_I), "Argon2i") == 0, "Название Argon2i");
    TEST_ASSERT(strcmp(argon2_type_name(ARGON2_ID), "Argon2id") == 0, "Название Argon2id");
}

/**
 * Тест 5: Генерация соли
 */
void test_argon2_salt(void) {
    printf("\nТест: Генерация соли...\n");
    
    uint8_t salt1[16], salt2[16];
    
    int r1 = argon2_generate_salt(salt1, sizeof(salt1));
    int r2 = argon2_generate_salt(salt2, sizeof(salt2));
    
    TEST_ASSERT_EQUAL(0, r1, "Генерация соли 1 успешна");
    TEST_ASSERT_EQUAL(0, r2, "Генерация соли 2 успешна");
    
    // Две соли должны быть разными
    int different = (memcmp(salt1, salt2, sizeof(salt1)) != 0);
    TEST_ASSERT(different, "Случайные соли различаются");
    
    printf("  Salt 1: "); print_hex(salt1, sizeof(salt1), "");
    printf("  Salt 2: "); print_hex(salt2, sizeof(salt2), "");
}

/**
 * Тест 6: Разная длина хэша
 */
void test_argon2_hash_lengths(void) {
    printf("\nТест: Разная длина хэша...\n");
    
    uint8_t hash16[16], hash32[32], hash64[64];
    
    argon2_params_t params16 = { .type = ARGON2_ID, .time_cost = 1, .memory_cost = 8192, .lanes = 1, .hash_len = 16 };
    argon2_params_t params32 = { .type = ARGON2_ID, .time_cost = 1, .memory_cost = 8192, .lanes = 1, .hash_len = 32 };
    argon2_params_t params64 = { .type = ARGON2_ID, .time_cost = 1, .memory_cost = 8192, .lanes = 1, .hash_len = 64 };
    
    int r1 = argon2_hash(TEST_PASSWORD, strlen(TEST_PASSWORD), TEST_SALT, sizeof(TEST_SALT), hash16, 16, &params16);
    int r2 = argon2_hash(TEST_PASSWORD, strlen(TEST_PASSWORD), TEST_SALT, sizeof(TEST_SALT), hash32, 32, &params32);
    int r3 = argon2_hash(TEST_PASSWORD, strlen(TEST_PASSWORD), TEST_SALT, sizeof(TEST_SALT), hash64, 64, &params64);
    
    TEST_ASSERT_EQUAL(0, r1, "Хэш 16 байт создан");
    TEST_ASSERT_EQUAL(0, r2, "Хэш 32 байта создан");
    TEST_ASSERT_EQUAL(0, r3, "Хэш 64 байта создан");
    
    printf("  16 байт: "); print_hash(hash16, 16);
    printf("  32 байта: "); print_hash(hash32, 32);
    printf("  64 байта: "); print_hash(hash64, 64);
}

/**
 * Тест 7: Ошибки валидации
 */
void test_argon2_errors(void) {
    printf("\nТест: Обработка ошибок...\n");
    
    uint8_t hash[32];
    
    // Пустой пароль
    int r1 = argon2_hash(NULL, 0, TEST_SALT, sizeof(TEST_SALT), hash, 32, NULL);
    TEST_ASSERT_EQUAL(-1, r1, "Пустой пароль отклонён");
    
    // Слишком короткая соль
    uint8_t short_salt[4] = {0};
    int r2 = argon2_hash(TEST_PASSWORD, strlen(TEST_PASSWORD), short_salt, 4, hash, 32, NULL);
    TEST_ASSERT_EQUAL(-1, r2, "Короткая соль отклонена");
    
    // Неправильная длина хэша
    uint8_t bad_hash[100];
    int r3 = argon2_hash(TEST_PASSWORD, strlen(TEST_PASSWORD), TEST_SALT, sizeof(TEST_SALT), bad_hash, 100, NULL);
    TEST_ASSERT_EQUAL(-1, r3, "Слишком длинный хэш отклонён");
    
    // Слишком мало памяти
    argon2_params_t low_mem = { .type = ARGON2_ID, .time_cost = 1, .memory_cost = 4, .lanes = 1, .hash_len = 32 };
    int r4 = argon2_hash(TEST_PASSWORD, strlen(TEST_PASSWORD), TEST_SALT, sizeof(TEST_SALT), hash, 32, &low_mem);
    TEST_ASSERT_EQUAL(-1, r4, "Мало памяти отклонено");
}

/**
 * Тест 8: Производительность
 */
void test_argon2_performance(void) {
    printf("\nТест: Производительность...\n");
    
    uint8_t hash[32];
    
    argon2_params_t params = {
        .type = ARGON2_ID,
        .time_cost = 3,
        .memory_cost = 65536,  // 64 MB
        .lanes = 4,
        .hash_len = 32
    };
    
    clock_t start = clock();
    int result = argon2_hash(TEST_PASSWORD, strlen(TEST_PASSWORD),
                             TEST_SALT, sizeof(TEST_SALT),
                             hash, 32, &params);
    clock_t end = clock();
    
    double elapsed = (double)(end - start) / CLOCKS_PER_SEC * 1000.0;
    
    TEST_ASSERT_EQUAL(0, result, "Хэширование завершено успешно");
    TEST_ASSERT(elapsed > 0, "Время больше 0");
    
    printf("  Время выполнения: %.2f мс\n", elapsed);
    printf("  Использование памяти: %d MB\n", params.memory_cost / 1024);
    printf("  Итерации: %d\n", params.time_cost);
    printf("  Параллельность: %d lanes\n", params.lanes);
}

/**
 * Тест 9: Длинные пароли
 */
void test_argon2_long_passwords(void) {
    printf("\nТест: Длинные пароли...\n");
    
    // Создаём длинный пароль (128 символов)
    char long_password[129];
    memset(long_password, 'A', sizeof(long_password) - 1);
    long_password[sizeof(long_password) - 1] = '\0';
    
    uint8_t hash1[32], hash2[32];
    
    int r1 = argon2id_hash("A", 1, TEST_SALT, hash1);
    int r2 = argon2id_hash(long_password, 128, TEST_SALT, hash2);
    
    TEST_ASSERT_EQUAL(0, r1, "Короткий пароль хэширован");
    TEST_ASSERT_EQUAL(0, r2, "Длинный пароль хэширован");
    
    // Должны быть разными
    TEST_ASSERT(memcmp(hash1, hash2, 32) != 0, "Разные пароли дают разные хэши");
    
    printf("  Пароль 1 символ:  "); print_hash(hash1, 32);
    printf("  Пароль 128 симв: "); print_hash(hash2, 32);
}

// ============================================================
// MAIN
// ============================================================

int main(void) {
    printf("========================================\n");
    printf("  Argon2 Unit Tests\n");
    printf("  Memory-Hard Function (PHC Winner 2015)\n");
    printf("========================================\n\n");
    
    // Запуск тестов
    test_argon2_basic();
    test_argon2_params();
    test_argon2_verify();
    test_argon2_types();
    test_argon2_salt();
    test_argon2_hash_lengths();
    test_argon2_errors();
    test_argon2_performance();
    test_argon2_long_passwords();
    
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
