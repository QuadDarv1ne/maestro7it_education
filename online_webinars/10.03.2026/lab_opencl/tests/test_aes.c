/**
 * @file test_aes.c
 * @brief Unit-тесты для AES-256-GCM
 */

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>
#include <time.h>

#include "../crypto/aes/aes.h"

// ============================================================
// ТЕСТОВЫЕ ДАННЫЕ
// ============================================================

static const uint8_t TEST_KEY[32] = {
    0x00, 0x01, 0x02, 0x03, 0x04, 0x05, 0x06, 0x07,
    0x08, 0x09, 0x0a, 0x0b, 0x0c, 0x0d, 0x0e, 0x0f,
    0x10, 0x11, 0x12, 0x13, 0x14, 0x15, 0x16, 0x17,
    0x18, 0x19, 0x1a, 0x1b, 0x1c, 0x1d, 0x1e, 0x1f
};

static const uint8_t TEST_IV[12] = {
    0x00, 0x01, 0x02, 0x03, 0x04, 0x05,
    0x06, 0x07, 0x08, 0x09, 0x0a, 0x0b
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

// ============================================================
// ВСПОМОГАТЕЛЬНЫЕ ФУНКЦИИ
// ============================================================

static void print_hex(const uint8_t* data, size_t len) {
    for (size_t i = 0; i < len; i++) {
        printf("%02x", data[i]);
    }
    printf("\n");
}

// ============================================================
// ТЕСТЫ
// ============================================================

void test_aes256_init(void) {
    printf("\nТест: Инициализация AES-256...\n");
    
    aes256_ctx_t ctx;
    int ret = aes256_init(&ctx, TEST_KEY);
    
    TEST_ASSERT(ret == 0, "aes256_init вернул успех");
    TEST_ASSERT(ctx.rounds == 14, "Количество раундов = 14 для AES-256");
    
    printf("  Раундов: %d\n", ctx.rounds);
}

void test_aes256_block_encrypt(void) {
    printf("\nТест: Шифрование блока AES-256...\n");
    
    aes256_ctx_t ctx;
    aes256_init(&ctx, TEST_KEY);
    
    uint8_t plaintext[16] = "Hello AES-256!";
    uint8_t ciphertext[16];
    uint8_t decrypted[16];
    
    aes256_encrypt_block(&ctx, plaintext, ciphertext);
    // aes256_decrypt_block(&ctx, ciphertext, decrypted);  // Заглушка
    
    // Проверяем что шифротекст отличается от открытого текста
    int different = (memcmp(plaintext, ciphertext, 16) != 0);
    TEST_ASSERT(different, "Шифротекст отличается от plaintext");
    
    printf("  Plaintext:  ");
    print_hex(plaintext, 16);
    printf("  Ciphertext: ");
    print_hex(ciphertext, 16);
}

void test_aes256_gcm_encrypt(void) {
    printf("\nТест: AES-256-GCM шифрование...\n");
    
    const char* plaintext = "Secret message for AES-256-GCM!";
    size_t pt_len = strlen(plaintext);
    
    uint8_t* ciphertext = (uint8_t*)malloc(pt_len);
    uint8_t tag[16];
    
    int ret = aes256_gcm(
        TEST_KEY, TEST_IV,
        NULL, 0,
        (const uint8_t*)plaintext, pt_len,
        ciphertext, tag
    );
    
    TEST_ASSERT(ret == 0, "GCM шифрование успешно");
    TEST_ASSERT(tag[0] != 0 || tag[15] != 0, "Тег не нулевой");
    
    printf("  Plaintext:  %s\n", plaintext);
    printf("  Ciphertext: ");
    print_hex(ciphertext, pt_len);
    printf("  Tag:        ");
    print_hex(tag, 16);
    
    free(ciphertext);
}

void test_aes256_gcm_with_aad(void) {
    printf("\nТест: AES-256-GCM с AAD...\n");
    
    const char* plaintext = "Message with AAD";
    const char* aad = "Additional Authenticated Data";
    size_t pt_len = strlen(plaintext);
    size_t aad_len = strlen(aad);
    
    uint8_t* ciphertext = (uint8_t*)malloc(pt_len);
    uint8_t tag[16];
    
    int ret = aes256_gcm(
        TEST_KEY, TEST_IV,
        (const uint8_t*)aad, aad_len,
        (const uint8_t*)plaintext, pt_len,
        ciphertext, tag
    );
    
    TEST_ASSERT(ret == 0, "GCM с AAD успешно");
    
    printf("  AAD:        %s\n", aad);
    printf("  Plaintext:  %s\n", plaintext);
    printf("  Ciphertext: ");
    print_hex(ciphertext, pt_len);
    printf("  Tag:        ");
    print_hex(tag, 16);
    
    free(ciphertext);
}

void test_aes256_gcm_deterministic(void) {
    printf("\nТест: AES-256-GCM детерминированность...\n");
    
    const char* plaintext = "Deterministic test";
    size_t pt_len = strlen(plaintext);
    
    uint8_t* ct1 = (uint8_t*)malloc(pt_len);
    uint8_t* ct2 = (uint8_t*)malloc(pt_len);
    uint8_t tag1[16], tag2[16];
    
    aes256_gcm(TEST_KEY, TEST_IV, NULL, 0,
               (const uint8_t*)plaintext, pt_len, ct1, tag1);
    aes256_gcm(TEST_KEY, TEST_IV, NULL, 0,
               (const uint8_t*)plaintext, pt_len, ct2, tag2);
    
    int same_ct = (memcmp(ct1, ct2, pt_len) == 0);
    int same_tag = (memcmp(tag1, tag2, 16) == 0);
    
    TEST_ASSERT(same_ct, "Шифротекст детерминированный");
    TEST_ASSERT(same_tag, "Тег детерминированный");
    
    free(ct1);
    free(ct2);
}

void test_aes256_gcm_different_iv(void) {
    printf("\nТест: AES-256-GCM разный IV...\n");
    
    const char* plaintext = "Same plaintext, different IV";
    size_t pt_len = strlen(plaintext);
    
    uint8_t iv1[12] = {0};
    uint8_t iv2[12] = {0};
    iv2[0] = 0x01;  // Разный IV
    
    uint8_t* ct1 = (uint8_t*)malloc(pt_len);
    uint8_t* ct2 = (uint8_t*)malloc(pt_len);
    uint8_t tag1[16], tag2[16];
    
    aes256_gcm(TEST_KEY, iv1, NULL, 0, (const uint8_t*)plaintext, pt_len, ct1, tag1);
    aes256_gcm(TEST_KEY, iv2, NULL, 0, (const uint8_t*)plaintext, pt_len, ct2, tag2);
    
    int different_ct = (memcmp(ct1, ct2, pt_len) != 0);
    int different_tag = (memcmp(tag1, tag2, 16) != 0);
    
    TEST_ASSERT(different_ct, "Разный IV даёт разный шифротекст");
    TEST_ASSERT(different_tag, "Разный IV даёт разный тег");
    
    free(ct1);
    free(ct2);
}

void test_aes256_gcm_performance(void) {
    printf("\nТест: Производительность AES-256-GCM...\n");
    
    size_t data_size = 10 * 1024 * 1024;  // 10 MB
    uint8_t* data = (uint8_t*)malloc(data_size);
    uint8_t* enc_data = (uint8_t*)malloc(data_size);
    
    if (!data || !enc_data) {
        fprintf(stderr, "Ошибка выделения памяти\n");
        return;
    }
    
    for (size_t i = 0; i < data_size; i++) {
        data[i] = (uint8_t)(i % 256);
    }
    
    aes256_gcm_ctx_t ctx;
    aes256_gcm_init(&ctx, TEST_KEY);
    
    uint8_t tag[16];
    
    clock_t start = clock();
    aes256_gcm_encrypt(&ctx, TEST_IV, NULL, 0, data, data_size, enc_data, tag);
    clock_t end = clock();
    
    double elapsed = (double)(end - start) / CLOCKS_PER_SEC * 1000.0;
    double throughput = (data_size / (1024.0 * 1024.0)) / (elapsed / 1000.0);
    
    TEST_ASSERT(elapsed > 0, "Время больше 0");
    
    printf("  Размер данных: %zu MB\n", data_size / (1024 * 1024));
    printf("  Время: %.2f мс\n", elapsed);
    printf("  Пропускная способность: %.2f MB/s\n", throughput);
    
    free(data);
    free(enc_data);
}

// ============================================================
// MAIN
// ============================================================

int main(void) {
    printf("========================================\n");
    printf("  AES-256-GCM Unit Tests\n");
    printf("  Стандарт Симметричного Шифрования\n");
    printf("========================================\n\n");
    
    test_aes256_init();
    test_aes256_block_encrypt();
    test_aes256_gcm_encrypt();
    test_aes256_gcm_with_aad();
    test_aes256_gcm_deterministic();
    test_aes256_gcm_different_iv();
    test_aes256_gcm_performance();
    
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
