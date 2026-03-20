/**
 * @file chacha20_main.c
 * @brief Demo программа для ChaCha20-Poly1305
 */

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>

#include "chacha20.h"

int main(int argc, char* argv[]) {
    (void)argc;
    (void)argv;
    
    printf("========================================\n");
    printf("  ChaCha20-Poly1305 — AEAD Шифрование\n");
    printf("========================================\n\n");
    
    // Ключ (32 байта)
    uint8_t key[32] = {
        0x00, 0x01, 0x02, 0x03, 0x04, 0x05, 0x06, 0x07,
        0x08, 0x09, 0x0a, 0x0b, 0x0c, 0x0d, 0x0e, 0x0f,
        0x10, 0x11, 0x12, 0x13, 0x14, 0x15, 0x16, 0x17,
        0x18, 0x19, 0x1a, 0x1b, 0x1c, 0x1d, 0x1e, 0x1f
    };
    
    // Nonce (12 байт)
    uint8_t nonce[12] = {
        0x00, 0x01, 0x02, 0x03, 0x04, 0x05,
        0x06, 0x07, 0x08, 0x09, 0x0a, 0x0b
    };
    
    // Данные
    const char* plaintext = "Hello, ChaCha20-Poly1305! Secret message here.";
    size_t pt_len = strlen(plaintext);
    
    printf("Исходные данные:\n");
    printf("  Текст: \"%s\"\n", plaintext);
    printf("  Длина: %zu байт\n\n", pt_len);
    
    // Выделение памяти
    uint8_t* ciphertext = (uint8_t*)malloc(pt_len);
    uint8_t* decrypted = (uint8_t*)malloc(pt_len);
    uint8_t tag[16];
    
    if (!ciphertext || !decrypted) {
        fprintf(stderr, "Ошибка выделения памяти\n");
        return 1;
    }
    
    // Шифрование
    printf("Шифрование...\n");
    int ret = chacha20_poly1305_encrypt(
        key, nonce,
        NULL, 0,  // Без AAD
        (const uint8_t*)plaintext, pt_len,
        ciphertext, tag
    );
    
    if (ret != 0) {
        fprintf(stderr, "Ошибка шифрования\n");
        return 1;
    }
    
    printf("  Шифротекст: ");
    for (size_t i = 0; i < pt_len; i++) {
        printf("%02x", ciphertext[i]);
    }
    printf("\n");
    
    printf("  Тег: ");
    for (int i = 0; i < 16; i++) {
        printf("%02x", tag[i]);
    }
    printf("\n\n");
    
    // Дешифрование
    printf("Дешифрование...\n");
    ret = chacha20_poly1305_decrypt(
        key, nonce,
        NULL, 0,
        ciphertext, pt_len,
        tag, decrypted
    );
    
    if (ret == 0) {
        printf("  Расшифровано: %.*s\n", (int)pt_len, decrypted);
    } else {
        printf("  ✗ Ошибка проверки тега!\n");
    }
    printf("\n");
    
    // Производительность
    printf("========================================\n");
    printf("  Тест производительности\n");
    printf("========================================\n");
    
    size_t data_size = 10 * 1024 * 1024;  // 10 MB
    uint8_t* data = (uint8_t*)malloc(data_size);
    uint8_t* enc_data = (uint8_t*)malloc(data_size);
    
    if (!data || !enc_data) {
        fprintf(stderr, "Ошибка выделения памяти\n");
        free(ciphertext);
        free(decrypted);
        return 1;
    }
    
    for (size_t i = 0; i < data_size; i++) {
        data[i] = (uint8_t)(i % 256);
    }
    
    uint8_t perf_tag[16];
    
    printf("  Размер данных: %zu MB\n", data_size / (1024 * 1024));
    
    clock_t start = clock();
    chacha20_poly1305_encrypt(key, nonce, NULL, 0, data, data_size, enc_data, perf_tag);
    clock_t end = clock();
    
    double elapsed = (double)(end - start) / CLOCKS_PER_SEC * 1000.0;
    double throughput = (data_size / (1024.0 * 1024.0)) / (elapsed / 1000.0);
    
    printf("  Время: %.2f мс\n", elapsed);
    printf("  Пропускная способность: %.2f MB/s\n", throughput);
    
    free(data);
    free(enc_data);
    free(ciphertext);
    free(decrypted);
    
    printf("\n========================================\n");
    printf("  ВСЕ ОПЕРАЦИИ ВЫПОЛНЕНЫ!\n");
    printf("========================================\n\n");
    
    return 0;
}
