/**
 * @file argon2_main.c
 * @brief Demo программа для Argon2
 */

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>

#include "argon2.h"

int main(int argc, char* argv[]) {
    printf("========================================\n");
    printf("  Argon2 — Memory-Hard Хэширование\n");
    printf("  (PHC Winner 2015)\n");
    printf("========================================\n\n");
    
    const char* password = "MySecurePassword123!";
    uint8_t salt[ARGON2_SALT_LEN];
    uint8_t hash[32];
    
    // Генерация соли
    if (argon2_generate_salt(salt, sizeof(salt)) != 0) {
        fprintf(stderr, "Ошибка генерации соли\n");
        return 1;
    }
    
    printf("Пароль: %s\n", password);
    printf("Соль: ");
    for (size_t i = 0; i < sizeof(salt); i++) {
        printf("%02x", salt[i]);
    }
    printf("\n\n");
    
    // Параметры по умолчанию (Argon2id)
    argon2_params_t params = {
        .type = ARGON2_ID,
        .time_cost = 3,
        .memory_cost = 65536,  // 64 MB
        .lanes = 4,
        .hash_len = 32
    };
    
    printf("Параметры:\n");
    printf("  Тип: %s\n", argon2_type_name(params.type));
    printf("  Итерации: %u\n", params.time_cost);
    printf("  Память: %u KB (%u MB)\n", params.memory_cost, params.memory_cost / 1024);
    printf("  Параллельность: %u lanes\n", params.lanes);
    printf("  Длина хэша: %u байт\n\n", params.hash_len);
    
    // Хэширование
    printf(">>> Хэширование...\n");
    clock_t start = clock();
    
    int result = argon2_hash(
        (const void*)password, strlen(password),
        salt, sizeof(salt),
        hash, sizeof(hash),
        &params
    );
    
    clock_t end = clock();
    double elapsed = (double)(end - start) / CLOCKS_PER_SEC * 1000.0;
    
    if (result != 0) {
        fprintf(stderr, "Ошибка хэширования\n");
        return 1;
    }
    
    printf("  Время: %.2f мс\n", elapsed);
    printf("  Хэш: ");
    for (size_t i = 0; i < sizeof(hash); i++) {
        printf("%02x", hash[i]);
    }
    printf("\n\n");
    
    // Проверка пароля
    printf(">>> Проверка правильного пароля...\n");
    int verify_result = argon2_verify(
        (const void*)password, strlen(password),
        salt, sizeof(salt),
        hash, sizeof(hash),
        &params
    );
    
    if (verify_result == 0) {
        printf("  ✓ Пароль подтверждён\n\n");
    } else {
        printf("  ✗ Пароль НЕ подтверждён (ошибка!)\n\n");
        return 1;
    }
    
    // Проверка неправильного пароля
    printf(">>> Проверка неправильного пароля...\n");
    int wrong_result = argon2_verify(
        (const void*)"WrongPassword", 13,
        salt, sizeof(salt),
        hash, sizeof(hash),
        &params
    );
    
    if (wrong_result != 0) {
        printf("  ✓ Неправильный пароль отклонён\n\n");
    } else {
        printf("  ✗ Неправильный пароль принят (ошибка!)\n\n");
        return 1;
    }
    
    printf("========================================\n");
    printf("  ВСЕ ПРОВЕРКИ ПРОЙДЕНЫ!\n");
    printf("========================================\n\n");
    
    return 0;
}
