/**
 * @file test_chacha20.c
 * @brief Unit-тесты для ChaCha20-Poly1305
 */

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>
#include <time.h>

#include "../crypto/chacha20/chacha20.h"

// ============================================================
// ТЕСТОВЫЕ ДАННЫЕ
// ============================================================

static const uint8_t TEST_KEY[32] = {
    0x00, 0x01, 0x02, 0x03, 0x04, 0x05, 0x06, 0x07,
    0x08, 0x09, 0x0a, 0x0b, 0x0c, 0x0d, 0x0e, 0x0f,
    0x10, 0x11, 0x12, 0x13, 0x14, 0x15, 0x16, 0x17,
    0x18, 0x19, 0x1a, 0x1b, 0x1c, 0x1d, 0x1e, 0x1f
};

static const uint8_t TEST_NONCE[12] = {
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

void test_chacha20_encrypt(void) {
    printf("\nТест: ChaCha20 шифрование...\n");
    
    const char* plaintext = "Test message for ChaCha20!";
    size_t pt_len = strlen(plaintext);
    
    uint8_t* ciphertext = (uint8_t*)malloc(pt_len);
    uint8_t tag[16];
    
    int ret = chacha20_poly1305_encrypt(
        TEST_KEY, TEST_NONCE,
        NULL, 0,
        (const uint8_t*)plaintext, pt_len,
        ciphertext, tag
    );
    
    TEST_ASSERT(ret == 0, "Шифрование успешно");
    TEST_ASSERT(tag[0] != 0 || tag[15] != 0, "Тег не нулевой");
    
    printf("  Plaintext:  %s\n", plaintext);
    printf("  Ciphertext: ");
    print_hex(ciphertext, pt_len);
    printf("  Tag:        ");
    print_hex(tag, 16);
    
    free(ciphertext);
}

void test_chacha20_with_aad(void) {
    printf("\nТест: ChaCha20-Poly1305 с AAD...\n");
    
    const char* plaintext = "Message with AAD";
    const char* aad = "Additional Authenticated Data";
    size_t pt_len = strlen(plaintext);
    size_t aad_len = strlen(aad);
    
    uint8_t* ciphertext = (uint8_t*)malloc(pt_len);
    uint8_t tag[16];
    
    int ret = chacha20_poly1305_encrypt(
        TEST_KEY, TEST_NONCE,
        (const uint8_t*)aad, aad_len,
        (const uint8_t*)plaintext, pt_len,
        ciphertext, tag
    );
    
    TEST_ASSERT(ret == 0, "Шифрование с AAD успешно");
    
    printf("  AAD:        %s\n", aad);
    printf("  Plaintext:  %s\n", plaintext);
    printf("  Ciphertext: ");
    print_hex(ciphertext, pt_len);
    printf("  Tag:        ");
    print_hex(tag, 16);
    
    free(ciphertext);
}

void test_chacha20_deterministic(void) {
    printf("\nТест: ChaCha20 детерминированность...\n");
    
    const char* plaintext = "Deterministic test";
    size_t pt_len = strlen(plaintext);
    
    uint8_t* ct1 = (uint8_t*)malloc(pt_len);
    uint8_t* ct2 = (uint8_t*)malloc(pt_len);
    uint8_t tag1[16], tag2[16];
    
    chacha20_poly1305_encrypt(TEST_KEY, TEST_NONCE, NULL, 0,
                              (const uint8_t*)plaintext, pt_len, ct1, tag1);
    chacha20_poly1305_encrypt(TEST_KEY, TEST_NONCE, NULL, 0,
                              (const uint8_t*)plaintext, pt_len, ct2, tag2);
    
    int same_ct = (memcmp(ct1, ct2, pt_len) == 0);
    int same_tag = (memcmp(tag1, tag2, 16) == 0);
    
    TEST_ASSERT(same_ct, "Шифротекст детерминированный");
    TEST_ASSERT(same_tag, "Тег детерминированный");
    
    free(ct1);
    free(ct2);
}

void test_chacha20_different_nonce(void) {
    printf("\nТест: ChaCha20 разный nonce...\n");
    
    const char* plaintext = "Same plaintext, different nonce";
    size_t pt_len = strlen(plaintext);
    
    uint8_t nonce1[12] = {0};
    uint8_t nonce2[12] = {0};
    nonce2[0] = 0x01;
    
    uint8_t* ct1 = (uint8_t*)malloc(pt_len);
    uint8_t* ct2 = (uint8_t*)malloc(pt_len);
    uint8_t tag1[16], tag2[16];
    
    chacha20_poly1305_encrypt(TEST_KEY, nonce1, NULL, 0, (const uint8_t*)plaintext, pt_len, ct1, tag1);
    chacha20_poly1305_encrypt(TEST_KEY, nonce2, NULL, 0, (const uint8_t*)plaintext, pt_len, ct2, tag2);
    
    int different_ct = (memcmp(ct1, ct2, pt_len) != 0);
    int different_tag = (memcmp(tag1, tag2, 16) != 0);
    
    TEST_ASSERT(different_ct, "Разный nonce даёт разный шифротекст");
    TEST_ASSERT(different_tag, "Разный nonce даёт разный тег");
    
    free(ct1);
    free(ct2);
}

void test_chacha20_decrypt(void) {
    printf("\nТест: ChaCha20 дешифрование...\n");
    
    const char* plaintext = "Test decryption";
    size_t pt_len = strlen(plaintext);
    
    uint8_t* ciphertext = (uint8_t*)malloc(pt_len);
    uint8_t* decrypted = (uint8_t*)malloc(pt_len);
    uint8_t tag[16];
    
    chacha20_poly1305_encrypt(TEST_KEY, TEST_NONCE, NULL, 0,
                              (const uint8_t*)plaintext, pt_len, ciphertext, tag);
    
    int ret = chacha20_poly1305_decrypt(TEST_KEY, TEST_NONCE, NULL, 0,
                                        ciphertext, pt_len, tag, decrypted);
    
    TEST_ASSERT(ret == 0, "Дешифрование успешно");
    
    printf("  Plaintext:   %s\n", plaintext);
    printf("  Decrypted:   %.*s\n", (int)pt_len, decrypted);
    
    free(ciphertext);
    free(decrypted);
}

void test_chacha20_performance(void) {
    printf("\nТест: Производительность ChaCha20...\n");
    
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
    
    uint8_t tag[16];
    
    printf("  Размер данных: %zu MB\n", data_size / (1024 * 1024));
    
    clock_t start = clock();
    chacha20_poly1305_encrypt(TEST_KEY, TEST_NONCE, NULL, 0, data, data_size, enc_data, tag);
    clock_t end = clock();
    
    double elapsed = (double)(end - start) / CLOCKS_PER_SEC * 1000.0;
    double throughput = (data_size / (1024.0 * 1024.0)) / (elapsed / 1000.0);
    
    TEST_ASSERT(elapsed > 0, "Время больше 0");
    
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
    printf("  ChaCha20-Poly1305 Unit Tests\n");
    printf("  AEAD Шифрование (RFC 8439)\n");
    printf("========================================\n\n");
    
    test_chacha20_encrypt();
    test_chacha20_with_aad();
    test_chacha20_deterministic();
    test_chacha20_different_nonce();
    test_chacha20_decrypt();
    test_chacha20_performance();
    
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
