/**
 * @file blake3_main.c
 * @brief Demo программа для BLAKE3
 */

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>

#include "blake3.h"

int main(int argc, char* argv[]) {
    (void)argc;
    (void)argv;
    
    printf("========================================\n");
    printf("  BLAKE3 — Самый Быстрый Хэш\n");
    printf("========================================\n\n");
    
    // Тестовые данные
    const char* test_strings[] = {
        "",
        "abc",
        "Hello, World!",
        "The quick brown fox jumps over the lazy dog"
    };
    
    int num_tests = sizeof(test_strings) / sizeof(test_strings[0]);
    
    printf("BLAKE3 хэши (32 байта):\n");
    printf("----------------------------------------\n");
    
    for (int i = 0; i < num_tests; i++) {
        const char* str = test_strings[i];
        uint8_t hash[32];
        char hex[65];
        
        blake3(str, strlen(str), hash, 32);
        
        // Конвертация в hex
        for (int j = 0; j < 32; j++) {
            sprintf(hex + j * 2, "%02x", hash[j]);
        }
        hex[64] = '\0';
        
        printf("  \"%s\"\n", str[0] ? str : "(empty)");
        printf("  %s\n\n", hex);
    }
    
    // Keyed hash
    printf("\nBLAKE3 Keyed Hash:\n");
    printf("----------------------------------------\n");
    
    uint8_t key[32] = {
        0x00, 0x01, 0x02, 0x03, 0x04, 0x05, 0x06, 0x07,
        0x08, 0x09, 0x0a, 0x0b, 0x0c, 0x0d, 0x0e, 0x0f,
        0x10, 0x11, 0x12, 0x13, 0x14, 0x15, 0x16, 0x17,
        0x18, 0x19, 0x1a, 0x1b, 0x1c, 0x1d, 0x1e, 0x1f
    };
    
    const char* keyed_input = "BLAKE3 keyed hash test";
    uint8_t keyed_hash[32];
    
    blake3_keyed(key, keyed_input, strlen(keyed_input), keyed_hash, 32);
    
    printf("  Input: \"%s\"\n", keyed_input);
    printf("  Keyed: ");
    for (int i = 0; i < 32; i++) {
        printf("%02x", keyed_hash[i]);
    }
    printf("\n");
    
    // XOF
    printf("\nBLAKE3 XOF (variable length):\n");
    printf("----------------------------------------\n");
    
    blake3_xof_ctx_t xof_ctx;
    blake3_xof_init(&xof_ctx);
    blake3_xof_update(&xof_ctx, "XOF test", 8);
    
    uint8_t xof_out[64];
    blake3_xof_final(&xof_ctx, xof_out, sizeof(xof_out));
    
    printf("  Input: \"XOF test\"\n");
    printf("  32 байта: ");
    for (int i = 0; i < 32; i++) {
        printf("%02x", xof_out[i]);
    }
    printf("\n");
    
    // Производительность
    printf("\n========================================\n");
    printf("  Тест производительности\n");
    printf("========================================\n");
    
    size_t data_size = 10 * 1024 * 1024;  // 10 MB
    uint8_t* data = (uint8_t*)malloc(data_size);
    if (!data) {
        fprintf(stderr, "Не удалось выделить память\n");
        return 1;
    }
    
    for (size_t i = 0; i < data_size; i++) {
        data[i] = (uint8_t)(i % 256);
    }
    
    uint8_t hash[32];
    
    printf("  Размер данных: %zu MB\n", data_size / (1024 * 1024));
    
    clock_t start = clock();
    blake3(data, data_size, hash, 32);
    clock_t end = clock();
    
    double elapsed = (double)(end - start) / CLOCKS_PER_SEC * 1000.0;
    double throughput = (data_size / (1024.0 * 1024.0)) / (elapsed / 1000.0);
    
    printf("  Время: %.2f мс\n", elapsed);
    printf("  Пропускная способность: %.2f MB/s\n", throughput);
    printf("  Хэш: ");
    for (int i = 0; i < 32; i++) {
        printf("%02x", hash[i]);
    }
    printf("\n");
    
    free(data);
    
    printf("\n========================================\n");
    printf("  ВСЕ ОПЕРАЦИИ ВЫПОЛНЕНЫ!\n");
    printf("========================================\n\n");
    
    return 0;
}
