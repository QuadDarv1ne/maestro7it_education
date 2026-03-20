/**
 * @file sha3_main.c
 * @brief Demo программа для SHA-3 (Keccak)
 */

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>

#include "sha3.h"

int main(int argc, char* argv[]) {
    (void)argc;
    (void)argv;
    
    printf("========================================\n");
    printf("  SHA-3 (Keccak) — NIST Стандарт 2015\n");
    printf("========================================\n\n");
    
    // Тестовые данные
    const char* test_strings[] = {
        "",
        "abc",
        "Hello, World!",
        "The quick brown fox jumps over the lazy dog"
    };
    
    int num_tests = sizeof(test_strings) / sizeof(test_strings[0]);
    
    printf("SHA3-256 хэши:\n");
    printf("----------------------------------------\n");
    
    for (int i = 0; i < num_tests; i++) {
        const char* str = test_strings[i];
        uint8_t hash[32];
        char hex[65];
        
        sha3_256(str, strlen(str), hash);
        
        // Конвертация в hex
        for (int j = 0; j < 32; j++) {
            sprintf(hex + j * 2, "%02x", hash[j]);
        }
        hex[64] = '\0';
        
        printf("  \"%s\"\n", str[0] ? str : "(empty)");
        printf("  %s\n\n", hex);
    }
    
    printf("\nSHA3-512 хэши:\n");
    printf("----------------------------------------\n");
    
    for (int i = 0; i < num_tests; i++) {
        const char* str = test_strings[i];
        uint8_t hash[64];
        char hex[129];
        
        sha3_512(str, strlen(str), hash);
        
        // Конвертация в hex
        for (int j = 0; j < 64; j++) {
            sprintf(hex + j * 2, "%02x", hash[j]);
        }
        hex[128] = '\0';
        
        printf("  \"%s\"\n", str[0] ? str : "(empty)");
        printf("  %s\n\n", hex);
    }
    
    // SHAKE128 тест
    printf("\nSHAKE128 (XOF — переменная длина):\n");
    printf("----------------------------------------\n");
    
    const char* shake_input = "SHAKE test";
    uint8_t shake_out[64];
    
    printf("  Вход: \"%s\"\n", shake_input);
    
    shake128(shake_input, strlen(shake_input), shake_out, 32);
    printf("  32 байта: ");
    for (int i = 0; i < 32; i++) {
        printf("%02x", shake_out[i]);
    }
    printf("\n");
    
    shake128(shake_input, strlen(shake_input), shake_out, 64);
    printf("  64 байта: ");
    for (int i = 0; i < 64; i++) {
        printf("%02x", shake_out[i]);
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
    
    // Инициализация данных
    for (size_t i = 0; i < data_size; i++) {
        data[i] = (uint8_t)(i % 256);
    }
    
    uint8_t hash[32];
    
    printf("  Размер данных: %zu MB\n", data_size / (1024 * 1024));
    
    clock_t start = clock();
    sha3_256(data, data_size, hash);
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
