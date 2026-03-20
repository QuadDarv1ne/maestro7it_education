/**
 * @file blake3.c
 * @brief BLAKE3 — реализация
 * 
 * Упрощённая реализация для демонстрации.
 * Для продакшена используйте официальную библиотеку.
 */

#include "blake3.h"
#include <stdio.h>
#include <string.h>

// ============================================================
// КОНСТАНТЫ
// ============================================================

/** Начальные значения (fractional parts of square roots of first 8 primes) */
static const uint32_t BLAKE3_IV[8] = {
    0x6A09E667, 0xBB67AE85, 0x3C6EF372, 0xA54FF53A,
    0x510E527F, 0x9B05688C, 0x1F83D9AB, 0x5BE0CD19
};

/** Флаги */
enum {
    CHUNK_START = 1 << 0,
    CHUNK_END = 1 << 1,
    PARENT = 1 << 2,
    ROOT = 1 << 3,
    KEYED_HASH = 1 << 4,
    DERIVE_KEY = 1 << 5,
    DERIVE_KEY_MATERIAL = 1 << 6
};

// ============================================================
// ВСПОМОГАТЕЛЬНЫЕ ФУНКЦИИ
// ============================================================

#define ROTR32(x, n) (((x) >> (n)) | ((x) << (32 - (n))))

/** Mixing function G */
static void blake3_mix_g(uint32_t* v, size_t a, size_t b, size_t c, size_t d,
                         uint32_t x, uint32_t y) {
    v[a] = v[a] + v[b] + x;
    v[d] = ROTR32(v[d] ^ v[a], 16);
    v[c] = v[c] + v[d];
    v[b] = ROTR32(v[b] ^ v[c], 12);
    v[a] = v[a] + v[b] + y;
    v[d] = ROTR32(v[d] ^ v[a], 8);
    v[c] = v[c] + v[d];
    v[b] = ROTR32(v[b] ^ v[c], 7);
}

/** Функция сжатия (compression function) */
static void blake3_compress(uint32_t cv[8], const uint8_t block[64],
                            uint64_t counter, uint8_t flags) {
    uint32_t v[16];
    uint32_t m[16];
    
    // Инициализация v
    for (int i = 0; i < 8; i++) {
        v[i] = cv[i];
        v[i + 8] = BLAKE3_IV[i];
    }
    
    v[12] ^= (uint32_t)counter;
    v[13] ^= (uint32_t)(counter >> 32);
    v[14] ^= flags;
    
    // Парсинг сообщения (little-endian)
    for (int i = 0; i < 16; i++) {
        m[i] = ((uint32_t)block[i * 4 + 0]) |
               ((uint32_t)block[i * 4 + 1] << 8) |
               ((uint32_t)block[i * 4 + 2] << 16) |
               ((uint32_t)block[i * 4 + 3] << 24);
    }
    
    // Перестановка σ для BLAKE3
    static const uint8_t SIGMA[10][16] = {
        {0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15},
        {2, 6, 3, 10, 7, 0, 4, 13, 1, 11, 12, 5, 9, 14, 15, 8},
        {3, 4, 10, 12, 13, 2, 7, 14, 6, 5, 9, 0, 11, 15, 8, 1},
        {10, 7, 12, 9, 14, 3, 13, 15, 0, 4, 11, 2, 5, 8, 1, 6},
        {12, 13, 9, 11, 15, 10, 14, 8, 2, 7, 5, 3, 4, 1, 6, 0},
        {9, 14, 11, 5, 8, 12, 15, 1, 3, 4, 0, 10, 7, 6, 2, 13},
        {11, 15, 5, 0, 1, 9, 8, 2, 10, 7, 3, 12, 13, 6, 4, 14},
        {5, 8, 0, 3, 2, 11, 1, 4, 12, 13, 10, 7, 6, 14, 15, 9},
        {0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15},
        {2, 6, 3, 10, 7, 0, 4, 13, 1, 11, 12, 5, 9, 14, 15, 8}
    };
    
    // 7 раундов
    for (int r = 0; r < 7; r++) {
        // Column step
        blake3_mix_g(v, 0, 4, 8, 12, m[SIGMA[r][0]], m[SIGMA[r][1]]);
        blake3_mix_g(v, 1, 5, 9, 13, m[SIGMA[r][2]], m[SIGMA[r][3]]);
        blake3_mix_g(v, 2, 6, 10, 14, m[SIGMA[r][4]], m[SIGMA[r][5]]);
        blake3_mix_g(v, 3, 7, 11, 15, m[SIGMA[r][6]], m[SIGMA[r][7]]);
        // Diagonal step
        blake3_mix_g(v, 0, 5, 10, 15, m[SIGMA[r][8]], m[SIGMA[r][9]]);
        blake3_mix_g(v, 1, 6, 11, 12, m[SIGMA[r][10]], m[SIGMA[r][11]]);
        blake3_mix_g(v, 2, 7, 8, 13, m[SIGMA[r][12]], m[SIGMA[r][13]]);
        blake3_mix_g(v, 3, 4, 9, 14, m[SIGMA[r][14]], m[SIGMA[r][15]]);
    }
    
    // XOR с CV
    for (int i = 0; i < 8; i++) {
        cv[i] ^= v[i] ^ v[i + 8];
    }
}

// ============================================================
// ОСНОВНЫЕ ФУНКЦИИ
// ============================================================

void blake3_init(blake3_ctx_t* ctx) {
    if (!ctx) return;
    
    memset(ctx, 0, sizeof(blake3_ctx_t));
    
    // Инициализация CV
    for (int i = 0; i < 8; i++) {
        ctx->cv[i] = BLAKE3_IV[i];
    }
    
    ctx->flags = CHUNK_START;
}

void blake3_init_key(blake3_ctx_t* ctx, const uint8_t key[BLAKE3_KEY_LEN]) {
    if (!ctx || !key) return;
    
    blake3_init(ctx);
    
    // XOR с ключом
    for (int i = 0; i < 8; i++) {
        uint32_t word = ((uint32_t)key[i * 4 + 0]) |
                        ((uint32_t)key[i * 4 + 1] << 8) |
                        ((uint32_t)key[i * 4 + 2] << 16) |
                        ((uint32_t)key[i * 4 + 3] << 24);
        ctx->cv[i] ^= word;
    }
    
    ctx->flags = CHUNK_START | KEYED_HASH;
}

void blake3_update(blake3_ctx_t* ctx, const void* data, size_t len) {
    if (!ctx || !data || len == 0) return;
    
    const uint8_t* input = (const uint8_t*)data;
    size_t i = 0;
    
    // Обработка буфера
    if (ctx->block_len > 0) {
        size_t to_fill = 64 - ctx->block_len;
        size_t to_copy = (len - i < to_fill) ? (len - i) : to_fill;
        
        memcpy(ctx->block + ctx->block_len, input + i, to_copy);
        ctx->block_len += (uint8_t)to_copy;
        i += to_copy;
        
        if (ctx->block_len < 64) {
            return;
        }
        
        // Сжатие
        ctx->counter += 64;
        uint8_t flags = ctx->flags;
        if (ctx->counter == 64) flags |= CHUNK_START;
        blake3_compress(ctx->cv, ctx->block, ctx->counter, flags);
        ctx->block_len = 0;
    }
    
    // Обработка полных блоков
    while (i + 64 <= len) {
        ctx->counter += 64;
        uint8_t flags = ctx->flags;
        if (ctx->counter == 64) flags |= CHUNK_START;
        blake3_compress(ctx->cv, input + i, ctx->counter, flags);
        i += 64;
    }
    
    // Остаток
    size_t remaining = len - i;
    if (remaining > 0) {
        memcpy(ctx->block, input + i, remaining);
        ctx->block_len = (uint8_t)remaining;
    }
}

void blake3_final(blake3_ctx_t* ctx, void* out) {
    if (!ctx || !out) return;
    
    // Padding
    memset(ctx->block + ctx->block_len, 0, 64 - ctx->block_len);
    
    // Флаги для последнего блока
    uint8_t flags = ctx->flags | CHUNK_END | ROOT;
    if (ctx->counter == 0) flags |= CHUNK_START;
    
    // Финальное сжатие
    uint32_t cv[8];
    memcpy(cv, ctx->cv, sizeof(cv));
    blake3_compress(cv, ctx->block, ctx->counter + ctx->block_len, flags);
    
    // Вывод (little-endian)
    uint8_t* output = (uint8_t*)out;
    for (int i = 0; i < 8; i++) {
        output[i * 4 + 0] = cv[i] & 0xFF;
        output[i * 4 + 1] = (cv[i] >> 8) & 0xFF;
        output[i * 4 + 2] = (cv[i] >> 16) & 0xFF;
        output[i * 4 + 3] = (cv[i] >> 24) & 0xFF;
    }
}

void blake3(const void* input, size_t input_len, void* out, size_t out_len) {
    blake3_ctx_t ctx;
    blake3_init(&ctx);
    blake3_update(&ctx, input, input_len);
    blake3_final(&ctx, out);
    
    // Для вывода > 32 байт нужно XOF расширение
    (void)out_len;
}

void blake3_keyed(const uint8_t key[BLAKE3_KEY_LEN], 
                  const void* input, size_t input_len, 
                  void* out, size_t out_len) {
    blake3_ctx_t ctx;
    blake3_init_key(&ctx, key);
    blake3_update(&ctx, input, input_len);
    blake3_final(&ctx, out);
    (void)out_len;
}

// ============================================================
// XOF ФУНКЦИИ
// ============================================================

void blake3_xof_init(blake3_xof_ctx_t* ctx) {
    if (!ctx) return;
    blake3_init(&ctx->core);
    ctx->cv_done = 0;
}

void blake3_xof_update(blake3_xof_ctx_t* ctx, const void* data, size_t len) {
    if (!ctx) return;
    blake3_update(&ctx->core, data, len);
}

void blake3_xof_final(blake3_xof_ctx_t* ctx, void* out, size_t out_len) {
    if (!ctx || !out) return;
    
    // Сначала получаем 32-байтный хэш
    blake3_final(&ctx->core, ctx->cv);
    ctx->cv_done = 1;
    
    // Для простоты копируем первые out_len байт
    size_t copy_len = (out_len < 32) ? out_len : 32;
    memcpy(out, ctx->cv, copy_len);
    
    // Для out_len > 32 нужно дополнительное расширение
    if (out_len > 32) {
        memset((uint8_t*)out + 32, 0, out_len - 32);
    }
}

void blake3_string(const char* str, char* hex_output) {
    if (!str || !hex_output) return;
    
    uint8_t hash[BLAKE3_OUT_LEN];
    blake3(str, strlen(str), hash, BLAKE3_OUT_LEN);
    
    for (int i = 0; i < BLAKE3_OUT_LEN; i++) {
        sprintf(hex_output + i * 2, "%02x", hash[i]);
    }
    hex_output[BLAKE3_OUT_LEN * 2] = '\0';
}
