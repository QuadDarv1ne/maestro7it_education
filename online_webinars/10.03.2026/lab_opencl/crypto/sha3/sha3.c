/**
 * @file sha3.c
 * @brief SHA-3 (Keccak) — полноценная реализация
 * 
 * Реализация основана на спецификации FIPS 202.
 * Использует перестановку Keccak-f[1600].
 */

#include "sha3.h"
#include <stdio.h>
#include <string.h>

// ============================================================
// КОНСТАНТЫ KECCAK
// ============================================================

/** Константы для раундов (Keccak round constants) */
static const uint64_t keccak_rndc[24] = {
    0x0000000000000001ULL, 0x0000000000008082ULL, 0x800000000000808aULL,
    0x8000000080008000ULL, 0x000000000000808bULL, 0x0000000080000001ULL,
    0x8000000080008081ULL, 0x8000000000008009ULL, 0x000000000000008aULL,
    0x0000000000000088ULL, 0x0000000080008009ULL, 0x000000008000000aULL,
    0x000000008000808bULL, 0x800000000000008bULL, 0x8000000000008089ULL,
    0x8000000000008003ULL, 0x8000000000008002ULL, 0x8000000000000080ULL,
    0x000000000000800aULL, 0x800000008000000aULL, 0x8000000080008081ULL,
    0x8000000000008080ULL, 0x0000000080000001ULL, 0x8000000080008008ULL
};

// ============================================================
// ВСПОМОГАТЕЛЬНЫЕ МАКРОСЫ
// ============================================================

#define ROT64(x, n) (((x) << (n)) | ((x) >> (64 - (n))))
#define MIN(a, b) ((a) < (b) ? (a) : (b))

// ============================================================
// ФУНКЦИЯ ПЕРЕСТАНОВКИ KECCAK-F[1600]
// ============================================================

/**
 * @brief Permutation Keccak-f[1600] — 24 раунда
 */
static void keccak_f1600(uint64_t state[25]) {
    uint64_t t, bc[5];
    
    for (int round = 0; round < 24; round++) {
        // === Theta ===
        for (int i = 0; i < 5; i++) {
            bc[i] = state[i] ^ state[i + 5] ^ state[i + 10] ^ state[i + 15] ^ state[i + 20];
        }
        
        for (int i = 0; i < 5; i++) {
            t = bc[(i + 4) % 5] ^ ROT64(bc[(i + 1) % 5], 1);
            state[i] ^= t;
            state[i + 5] ^= t;
            state[i + 10] ^= t;
            state[i + 15] ^= t;
            state[i + 20] ^= t;
        }
        
        // === Rho & Pi ===
        t = state[1];
        state[1] = ROT64(state[6], 44);
        state[6] = ROT64(state[9], 20);
        state[9] = ROT64(state[22], 61);
        state[22] = ROT64(state[14], 39);
        state[14] = ROT64(state[20], 18);
        state[20] = ROT64(state[2], 62);
        state[2] = ROT64(state[12], 43);
        state[12] = ROT64(state[13], 25);
        state[13] = ROT64(state[19], 8);
        state[19] = ROT64(state[23], 56);
        state[23] = ROT64(state[15], 41);
        state[15] = ROT64(state[4], 27);
        state[4] = ROT64(state[24], 14);
        state[24] = ROT64(state[21], 2);
        state[21] = ROT64(state[8], 55);
        state[8] = ROT64(state[16], 45);
        state[16] = ROT64(state[5], 36);
        state[5] = ROT64(state[3], 28);
        state[3] = ROT64(state[18], 21);
        state[18] = ROT64(state[17], 15);
        state[17] = ROT64(state[11], 10);
        state[11] = ROT64(state[7], 6);
        state[7] = ROT64(state[10], 3);
        state[10] = ROT64(t, 1);
        
        // === Chi ===
        for (int j = 0; j < 25; j += 5) {
            for (int i = 0; i < 5; i++) {
                bc[i] = state[j + i];
            }
            for (int i = 0; i < 5; i++) {
                state[j + i] ^= (~bc[(i + 1) % 5]) & bc[(i + 2) % 5];
            }
        }
        
        // === Iota ===
        state[0] ^= keccak_rndc[round];
    }
}

// ============================================================
// ФУНКЦИИ ИНИЦИАЛИЗАЦИИ
// ============================================================

void sha3_256_init(sha3_ctx_t* ctx) {
    if (!ctx) return;
    memset(ctx, 0, sizeof(sha3_ctx_t));
    ctx->block_size = SHA3_256_BLOCK_SIZE;  // 136 байт
    ctx->hash_len = SHA3_256_HASH_LEN;       // 32 байта
    ctx->delim = 0x06;                       // Domain separation for SHA3
}

void sha3_512_init(sha3_ctx_t* ctx) {
    if (!ctx) return;
    memset(ctx, 0, sizeof(sha3_ctx_t));
    ctx->block_size = SHA3_512_BLOCK_SIZE;  // 72 байта
    ctx->hash_len = SHA3_512_HASH_LEN;       // 64 байта
    ctx->delim = 0x06;
}

void shake128_init(sha3_ctx_t* ctx) {
    if (!ctx) return;
    memset(ctx, 0, sizeof(sha3_ctx_t));
    ctx->block_size = SHAKE128_BLOCK_SIZE;  // 168 байт
    ctx->hash_len = 0;                       // XOF — длина задаётся при финализации
    ctx->delim = 0x1F;                       // Domain separation for SHAKE
}

void shake256_init(sha3_ctx_t* ctx) {
    if (!ctx) return;
    memset(ctx, 0, sizeof(sha3_ctx_t));
    ctx->block_size = SHAKE256_BLOCK_SIZE;  // 136 байт
    ctx->hash_len = 0;
    ctx->delim = 0x1F;
}

// ============================================================
// UPDATE ФУНКЦИЯ
// ============================================================

void sha3_update(sha3_ctx_t* ctx, const void* data, size_t len) {
    if (!ctx || !data || len == 0) return;
    
    const uint8_t* input = (const uint8_t*)data;
    size_t i = 0;
    
    // Обработка данных, оставшихся в буфере
    if (ctx->buffer_len > 0) {
        size_t to_fill = ctx->block_size - ctx->buffer_len;
        size_t to_copy = MIN(len - i, to_fill);
        
        memcpy(ctx->buffer + ctx->buffer_len, input + i, to_copy);
        ctx->buffer_len += to_copy;
        i += to_copy;
        
        if (ctx->buffer_len < ctx->block_size) {
            return;  // Буфер ещё не заполнен
        }
        
        // Буфер заполнен — обрабатываем
        for (size_t j = 0; j < ctx->block_size; j += 8) {
            uint64_t word = 0;
            for (size_t k = 0; k < 8; k++) {
                word |= (uint64_t)ctx->buffer[j + k] << (k * 8);
            }
            ctx->state[j / 8] ^= word;
        }

        keccak_f1600(ctx->state);
        ctx->buffer_len = 0;
    }

    // Обработка полных блоков
    while (i + ctx->block_size <= len) {
        for (size_t j = 0; j < ctx->block_size; j += 8) {
            uint64_t word = 0;
            for (size_t k = 0; k < 8; k++) {
                word |= (uint64_t)input[i + j + k] << (k * 8);
            }
            ctx->state[j / 8] ^= word;
        }

        keccak_f1600(ctx->state);
        i += ctx->block_size;
    }
    
    // Остаток в буфере
    size_t remaining = len - i;
    if (remaining > 0) {
        memcpy(ctx->buffer, input + i, remaining);
        ctx->buffer_len = remaining;
    }
}

// ============================================================
// FINAL ФУНКЦИЯ
// ============================================================

void sha3_final(sha3_ctx_t* ctx, void* hash) {
    if (!ctx || !hash) return;
    
    // Добавление padding
    memset(ctx->buffer + ctx->buffer_len, 0, ctx->block_size - ctx->buffer_len);
    ctx->buffer[ctx->buffer_len] = ctx->delim;
    ctx->buffer[ctx->block_size - 1] |= 0x80;
    
    // Обработка последнего блока
    for (size_t j = 0; j < ctx->block_size; j += 8) {
        uint64_t word = 0;
        for (size_t k = 0; k < 8; k++) {
            word |= (uint64_t)ctx->buffer[j + k] << (k * 8);
        }
        ctx->state[j / 8] ^= word;
    }

    keccak_f1600(ctx->state);

    // Извлечение результата (little-endian)
    size_t output_len = (ctx->hash_len > 0) ? ctx->hash_len : ctx->block_size;
    uint8_t* output = (uint8_t*)hash;

    for (size_t j = 0; j < output_len; j += 8) {
        size_t to_copy = MIN(8, output_len - j);
        for (size_t k = 0; k < to_copy; k++) {
            output[j + k] = (ctx->state[j / 8] >> (k * 8)) & 0xFF;
        }
    }
}

// ============================================================
// УДОБНЫЕ ФУНКЦИИ
// ============================================================

void sha3_256(const void* data, size_t len, void* hash) {
    sha3_ctx_t ctx;
    sha3_256_init(&ctx);
    sha3_update(&ctx, data, len);
    sha3_final(&ctx, hash);
}

void sha3_512(const void* data, size_t len, void* hash) {
    sha3_ctx_t ctx;
    sha3_512_init(&ctx);
    sha3_update(&ctx, data, len);
    sha3_final(&ctx, hash);
}

void shake128(const void* data, size_t len, void* output, size_t output_len) {
    sha3_ctx_t ctx;
    shake128_init(&ctx);
    ctx.hash_len = output_len;
    sha3_update(&ctx, data, len);
    sha3_final(&ctx, output);
}

void shake256(const void* data, size_t len, void* output, size_t output_len) {
    sha3_ctx_t ctx;
    shake256_init(&ctx);
    ctx.hash_len = output_len;
    sha3_update(&ctx, data, len);
    sha3_final(&ctx, output);
}

void sha3_256_string(const char* str, char* hex_output) {
    if (!str || !hex_output) return;
    
    uint8_t hash[SHA3_256_HASH_LEN];
    sha3_256(str, strlen(str), hash);
    
    for (int i = 0; i < SHA3_256_HASH_LEN; i++) {
        sprintf(hex_output + i * 2, "%02x", hash[i]);
    }
    hex_output[SHA3_256_HASH_LEN * 2] = '\0';
}
