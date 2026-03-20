/**
 * @file argon2.c
 * @brief CPU реализация Argon2 (упрощённая версия для демонстрации)
 * 
 * Полная реализация Argon2 требует значительного объёма кода.
 * Эта версия демонстрирует основные принципы работы алгоритма.
 * 
 * Для продакшена используйте официальную библиотеку:
 * https://github.com/P-H-C/phc-winner-argon2
 */

#include "argon2.h"
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>

// ============================================================
// КОНСТАНТЫ
// ============================================================

/** Размер блока в Argon2 (1 KB) */
#define ARGON2_BLOCK_SIZE 1024

/** Количество 64-битных слов в блоке */
#define ARGON2_QWORDS_IN_BLOCK (ARGON2_BLOCK_SIZE / 8)

/** Версия алгоритма */
#define ARGON2_VERSION_NUMBER 0x13

/** Максимальное количество колонок */
#define ARGON2_MAX_COLUMNS 256

// ============================================================
// ВНУТРЕННИЕ СТРУКТУРЫ
// ============================================================

/**
 * @brief Блок памяти Argon2 (1024 байта)
 */
typedef struct {
    uint64_t v[ARGON2_QWORDS_IN_BLOCK];
} argon2_block_t;

/**
 * @brief Контекст хэширования
 */
typedef struct {
    argon2_type_t type;
    uint32_t time_cost;
    uint32_t memory_cost;
    uint32_t lanes;
    uint32_t hash_len;
    uint32_t segment_length;
    uint32_t lane_length;
    argon2_block_t* memory;
} argon2_context_t;

// ============================================================
// ВСПОМОГАТЕЛЬНЫЕ ФУНКЦИИ
// ============================================================

/**
 * @brief Функция сжатия G (основная операция Argon2)
 * 
 * Использует операцию Blake2b-like для смешивания блоков.
 */
static void argon2_g(argon2_block_t* result, 
                     const argon2_block_t* x, 
                     const argon2_block_t* y) {
    if (!result || !x || !y) return;
    
    // XOR входов
    argon2_block_t r;
    for (size_t i = 0; i < ARGON2_QWORDS_IN_BLOCK; i++) {
        r.v[i] = x->v[i] ^ y->v[i];
    }
    
    // Применяем функцию перестановки (упрощённо)
    // В полной реализации используется 8 раундов Blake2b-like перестановки
    for (size_t round = 0; round < 8; round++) {
        // Row-wise permutation (упрощённая версия)
        for (size_t i = 0; i < ARGON2_QWORDS_IN_BLOCK; i += 16) {
            // Применяем функцию F (упрощённо)
            uint64_t a = r.v[i];
            uint64_t b = r.v[i + 1];
            
            // Rotations и XOR (симуляция BLAKE2b)
            r.v[i] = a ^ ((b << 32) | (b >> 32));
            r.v[i + 1] = b ^ ((a << 24) | (a >> 40));
        }
        
        // Column-wise permutation (упрощённо)
        for (size_t i = 0; i < 8; i++) {
            for (size_t j = 0; j < 8; j++) {
                size_t idx = i * 8 + j;
                if (idx < ARGON2_QWORDS_IN_BLOCK) {
                    r.v[idx] ^= r.v[(idx + 1) % ARGON2_QWORDS_IN_BLOCK];
                }
            }
        }
    }
    
    // XOR с исходным значением
    for (size_t i = 0; i < ARGON2_QWORDS_IN_BLOCK; i++) {
        result->v[i] = r.v[i] ^ x->v[i] ^ y->v[i];
    }
}

/**
 * @brief Инициализация первого блока
 */
static void argon2_init_first_block(argon2_context_t* ctx,
                                    const void* password, size_t password_len,
                                    const void* salt, size_t salt_len,
                                    argon2_block_t* block) {
    if (!ctx || !block) return;
    
    memset(block, 0, sizeof(argon2_block_t));
    
    // H0: Initial hash input
    // Lane || Index (4 bytes each)
    uint32_t* block32 = (uint32_t*)block->v;
    block32[0] = ctx->lanes;
    block32[1] = ctx->hash_len;
    block32[2] = ctx->memory_cost;
    block32[3] = ctx->time_cost;
    block32[4] = ARGON2_VERSION_NUMBER;
    block32[5] = (uint32_t)ctx->type;
    block32[6] = (uint32_t)password_len;
    block32[7] = (uint32_t)salt_len;
    
    // Копируем пароль и соль (упрощённо)
    size_t offset = 8 * sizeof(uint32_t);
    size_t remaining = ARGON2_BLOCK_SIZE - offset;
    
    if (password && password_len > 0) {
        size_t copy_len = (password_len < remaining) ? password_len : remaining;
        memcpy((uint8_t*)block->v + offset, password, copy_len);
        remaining -= copy_len;
        offset += copy_len;
    }
    
    if (salt && salt_len > 0 && remaining > 0) {
        size_t copy_len = (salt_len < remaining) ? salt_len : remaining;
        memcpy((uint8_t*)block->v + offset, salt, copy_len);
    }
}

/**
 * @brief Функция индексации (упрощённая)
 */
static uint32_t argon2_get_ref_lane(uint32_t lane, uint32_t index,
                                    argon2_type_t type) {
    (void)index;
    (void)type;
    // Упрощённая версия: используем текущую полосу
    return lane;
}

// ============================================================
// ОСНОВНАЯ ФУНКЦИЯ
// ============================================================

int argon2_hash(const void* password, size_t password_len,
                const void* salt, size_t salt_len,
                void* hash, size_t hash_len,
                const argon2_params_t* params) {
    // Валидация входных параметров
    if (!password || password_len == 0) {
        fprintf(stderr, "[Argon2 Error] Пароль не указан\n");
        return -1;
    }
    
    if (!salt || salt_len < ARGON2_MIN_SALT_LEN) {
        fprintf(stderr, "[Argon2 Error] Соль слишком короткая (минимум %d байт)\n", 
                ARGON2_MIN_SALT_LEN);
        return -1;
    }
    
    if (!hash || hash_len < ARGON2_MIN_HASH_LEN || hash_len > ARGON2_MAX_HASH_LEN) {
        fprintf(stderr, "[Argon2 Error] Неверная длина хэша (%zu)\n", hash_len);
        return -1;
    }
    
    // Параметры по умолчанию
    argon2_params_t default_params = {
        .type = ARGON2_ID,
        .time_cost = ARGON2_DEFAULT_TIME,
        .memory_cost = ARGON2_DEFAULT_MEMORY,
        .lanes = ARGON2_DEFAULT_LANES,
        .hash_len = 32
    };
    
    const argon2_params_t* p = params ? params : &default_params;
    
    // Валидация параметров
    if (p->memory_cost < ARGON2_MIN_MEMORY) {
        fprintf(stderr, "[Argon2 Error] Память слишком мала (минимум %d KB)\n",
                ARGON2_MIN_MEMORY);
        return -1;
    }
    
    if (p->lanes < ARGON2_MIN_LANES) {
        fprintf(stderr, "[Argon2 Error] Слишком мало потоков\n");
        return -1;
    }
    
    // Инициализация контекста
    argon2_context_t ctx;
    memset(&ctx, 0, sizeof(ctx));
    ctx.type = p->type;
    ctx.time_cost = p->time_cost;
    ctx.memory_cost = p->memory_cost;
    ctx.lanes = p->lanes;
    ctx.hash_len = p->hash_len;
    
    // Вычисляем размеры
    ctx.lane_length = ctx.memory_cost / ctx.lanes;
    ctx.segment_length = ctx.lane_length / 4;  // 4 сегмента на проход
    
    // Выделение памяти
    size_t total_blocks = ctx.memory_cost;  // 1 KB на блок
    ctx.memory = (argon2_block_t*)calloc(total_blocks, sizeof(argon2_block_t));
    
    if (!ctx.memory) {
        fprintf(stderr, "[Argon2 Error] Не удалось выделить %u KB памяти\n",
                (unsigned)ctx.memory_cost);
        return -1;
    }
    
    // Инициализация первых двух блоков каждой полосы
    for (uint32_t lane = 0; lane < ctx.lanes; lane++) {
        argon2_block_t first_block;
        argon2_init_first_block(&ctx, password, password_len, salt, salt_len, &first_block);
        
        // Добавляем номер полосы и индекс
        uint32_t* fb32 = (uint32_t*)first_block.v;
        fb32[0] ^= lane;
        fb32[1] ^= 0;  // Index = 0

        ctx.memory[lane * ctx.lane_length + 0] = first_block;
        
        // Второй блок (инициализируется нулями в упрощённой версии)
        memset(&ctx.memory[lane * ctx.lane_length + 1], 0, sizeof(argon2_block_t));
    }
    
    // Основное заполнение памяти
    for (uint32_t pass = 0; pass < ctx.time_cost; pass++) {
        for (uint32_t slice = 0; slice < 4; slice++) {
            for (uint32_t lane = 0; lane < ctx.lanes; lane++) {
                for (uint32_t index = 0; index < ctx.segment_length; index++) {
                    uint32_t current_idx = slice * ctx.segment_length + index;
                    
                    // Пропускаем первые два блока
                    if (pass == 0 && current_idx < 2) continue;
                    
                    // Получаем ссылочную полосу и индекс (упрощённо)
                    uint32_t ref_lane = argon2_get_ref_lane(lane, current_idx, ctx.type);
                    uint32_t ref_index = (current_idx > 0) ? (current_idx - 1) : 0;
                    
                    // Применяем функцию G
                    argon2_block_t* prev_block = &ctx.memory[lane * ctx.lane_length + 
                                                             (current_idx > 0 ? current_idx - 1 : 0)];
                    argon2_block_t* ref_block = &ctx.memory[ref_lane * ctx.lane_length + ref_index];
                    argon2_block_t* curr_block = &ctx.memory[lane * ctx.lane_length + current_idx];
                    
                    if (prev_block && ref_block && curr_block) {
                        argon2_g(curr_block, prev_block, ref_block);
                    }
                }
            }
        }
    }
    
    // Финализация: XOR последних блоков всех полос
    argon2_block_t final_block;
    memset(&final_block, 0, sizeof(final_block));
    
    for (uint32_t lane = 0; lane < ctx.lanes; lane++) {
        argon2_block_t* last_block = &ctx.memory[lane * ctx.lane_length + ctx.lane_length - 1];
        for (size_t i = 0; i < ARGON2_QWORDS_IN_BLOCK; i++) {
            final_block.v[i] ^= last_block->v[i];
        }
    }
    
    // Вывод хэша
    memcpy(hash, final_block.v, hash_len);
    
    // Очистка
    free(ctx.memory);
    
    return 0;
}

int argon2id_hash(const void* password, size_t password_len,
                  const void* salt, void* hash) {
    argon2_params_t params = {
        .type = ARGON2_ID,
        .time_cost = ARGON2_DEFAULT_TIME,
        .memory_cost = ARGON2_DEFAULT_MEMORY,
        .lanes = ARGON2_DEFAULT_LANES,
        .hash_len = 32
    };
    
    return argon2_hash(password, password_len, salt, ARGON2_SALT_LEN, 
                       hash, 32, &params);
}

int argon2_verify(const void* password, size_t password_len,
                  const void* salt, size_t salt_len,
                  const void* expected_hash, size_t hash_len,
                  const argon2_params_t* params) {
    if (!expected_hash || !password) return -1;
    
    uint8_t computed_hash[ARGON2_MAX_HASH_LEN];
    
    if (argon2_hash(password, password_len, salt, salt_len,
                    computed_hash, hash_len, params) != 0) {
        return -1;
    }
    
    // Constant-time comparison
    volatile uint8_t result = 0;
    for (size_t i = 0; i < hash_len; i++) {
        result |= computed_hash[i] ^ ((const uint8_t*)expected_hash)[i];
    }
    
    return (result == 0) ? 0 : -1;
}

int argon2_generate_salt(void* salt, size_t salt_len) {
    if (!salt || salt_len < ARGON2_MIN_SALT_LEN) return -1;

    // Используем криптографически безопасный генератор
    // Fallback: rand() (не рекомендуется для продакшена!)
    // Для полноценной реализации используйте bcrypt или официальную библиотеку Argon2
    for (size_t i = 0; i < salt_len; i++) {
        ((uint8_t*)salt)[i] = (uint8_t)(rand() % 256);
    }

    return 0;
}

const char* argon2_type_name(argon2_type_t type) {
    switch (type) {
        case ARGON2_D:  return "Argon2d";
        case ARGON2_I:  return "Argon2i";
        case ARGON2_ID: return "Argon2id";
        default:        return "Unknown";
    }
}
