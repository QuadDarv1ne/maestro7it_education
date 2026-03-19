/**
 * @file sha256.c
 * @brief CPU реализация SHA-256 для unit-тестов
 *
 * Этот файл содержит только функцию sha256_cpu без зависимостей от OpenCL
 * Исправленная версия с правильной обработкой множественных блоков
 */

#include "sha256.h"
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>

// ============================================================
// КОНСТАНТЫ SHA-256
// ============================================================

static const uint32_t sha256_k[64] = {
    0x428a2f98, 0x71374491, 0xb5c0fbcf, 0xe9b5dba5,
    0x3956c25b, 0x59f111f1, 0x923f82a4, 0xab1c5ed5,
    0xd807aa98, 0x12835b01, 0x243185be, 0x550c7dc3,
    0x72be5d74, 0x80deb1fe, 0x9bdc06a7, 0xc19bf174,
    0xe49b69c1, 0xefbe4786, 0x0fc19dc6, 0x240ca1cc,
    0x2de92c6f, 0x4a7484aa, 0x5cb0a9dc, 0x76f988da,
    0x983e5152, 0xa831c66d, 0xb00327c8, 0xbf597fc7,
    0xc6e00bf3, 0xd5a79147, 0x06ca6351, 0x14292967,
    0x27b70a85, 0x2e1b2138, 0x4d2c6dfc, 0x53380d13,
    0x650a7354, 0x766a0abb, 0x81c2c92e, 0x92722c85,
    0xa2bfe8a1, 0xa81a664b, 0xc24b8b70, 0xc76c51a3,
    0xd192e819, 0xd6990624, 0xf40e3585, 0x106aa070,
    0x19a4c116, 0x1e376c08, 0x2748774c, 0x34b0bcb5,
    0x391c0cb3, 0x4ed8aa4a, 0x5b9cca4f, 0x682e6ff3,
    0x748f82ee, 0x78a5636f, 0x84c87814, 0x8cc70208,
    0x90befffa, 0xa4506ceb, 0xbef9a3f7, 0xc67178f2
};

static const uint32_t sha256_h_init[8] = {
    0x6a09e667, 0xbb67ae85, 0x3c6ef372, 0xa54ff53a,
    0x510e527f, 0x9b05688c, 0x1f83d9ab, 0x5be0cd19
};

// ============================================================
// МАКРОСЫ
// ============================================================

#define ROTR(x, n) (((x) >> (n)) | ((x) << (32 - (n))))
#define CH(x, y, z) (((x) & (y)) ^ (~(x) & (z)))
#define MAJ(x, y, z) (((x) & (y)) ^ ((x) & (z)) ^ ((y) & (z)))
#define EP0(x) (ROTR((x), 2) ^ ROTR((x), 13) ^ ROTR((x), 22))
#define EP1(x) (ROTR((x), 6) ^ ROTR((x), 11) ^ ROTR((x), 25))
#define SIG0(x) (ROTR((x), 7) ^ ROTR((x), 18) ^ ((x) >> 3))
#define SIG1(x) (ROTR((x), 17) ^ ROTR((x), 19) ^ ((x) >> 10))

// ============================================================
// ВСПОМОГАТЕЛЬНЫЕ ФУНКЦИИ
// ============================================================

/**
 * @brief Обработка одного 64-байтного блока
 */
static void sha256_transform(uint32_t h[8], const uint8_t block[64]) {
    uint32_t w[64];
    
    // Первые 16 слов из блока (big-endian)
    for (int i = 0; i < 16; i++) {
        w[i] = ((uint32_t)block[i*4 + 0] << 24) |
               ((uint32_t)block[i*4 + 1] << 16) |
               ((uint32_t)block[i*4 + 2] << 8) |
               ((uint32_t)block[i*4 + 3]);
    }
    
    // Расширение до 64 слов
    for (int i = 16; i < 64; i++) {
        w[i] = SIG1(w[i-2]) + w[i-7] + SIG0(w[i-15]) + w[i-16];
    }
    
    // Основной цикл
    uint32_t a = h[0], b = h[1], c = h[2], d = h[3];
    uint32_t e = h[4], f = h[5], g = h[6], hh = h[7];
    
    for (int i = 0; i < 64; i++) {
        uint32_t t1 = hh + EP1(e) + CH(e, f, g) + sha256_k[i] + w[i];
        uint32_t t2 = EP0(a) + MAJ(a, b, c);
        hh = g; g = f; f = e; e = d + t1;
        d = c; c = b; b = a; a = t1 + t2;
    }
    
    h[0] += a; h[1] += b; h[2] += c; h[3] += d;
    h[4] += e; h[5] += f; h[6] += g; h[7] += hh;
}

// ============================================================
// ОСНОВНАЯ ФУНКЦИЯ
// ============================================================

/**
 * Вычисление SHA-256 хэша для одного сообщения (CPU)
 * Правильная обработка множественных блоков
 */
void sha256_cpu(const uint8_t* data, size_t len, uint8_t* hash) {
    uint32_t h[8];
    memcpy(h, sha256_h_init, sizeof(h));

    // Вычисляем размер с padding
    // Сообщение + 0x80 (1 байт) + нули + длина (8 байт) = len + 9 минимум
    // Padding добавляется до кратности 64
    size_t min_len = len + 9;  // Минимальный размер с padding
    size_t padded_len = ((min_len + 63) / 64) * 64;  // Округление вверх до кратного 64
    if (padded_len < 64) padded_len = 64;

    uint8_t* padded = (uint8_t*)calloc(padded_len, 1);
    if (!padded) return;

    // Копируем данные
    memcpy(padded, data, len);

    // Ставим 0x80 после данных
    padded[len] = 0x80;

    // Длина в битах в последних 8 байтах (big-endian)
    uint64_t bit_len = (uint64_t)len * 8;
    padded[padded_len - 8] = (bit_len >> 56) & 0xFF;
    padded[padded_len - 7] = (bit_len >> 48) & 0xFF;
    padded[padded_len - 6] = (bit_len >> 40) & 0xFF;
    padded[padded_len - 5] = (bit_len >> 32) & 0xFF;
    padded[padded_len - 4] = (bit_len >> 24) & 0xFF;
    padded[padded_len - 3] = (bit_len >> 16) & 0xFF;
    padded[padded_len - 2] = (bit_len >> 8) & 0xFF;
    padded[padded_len - 1] = bit_len & 0xFF;

    // Обрабатываем каждый блок
    size_t num_blocks = padded_len / 64;
    for (size_t block = 0; block < num_blocks; block++) {
        sha256_transform(h, padded + block * 64);
    }

    free(padded);

    // Запись результата (big-endian)
    for (int i = 0; i < 8; i++) {
        hash[i*4 + 0] = (h[i] >> 24) & 0xFF;
        hash[i*4 + 1] = (h[i] >> 16) & 0xFF;
        hash[i*4 + 2] = (h[i] >> 8) & 0xFF;
        hash[i*4 + 3] = h[i] & 0xFF;
    }
}

/**
 * @brief Вычисление SHA-256 хэша для строки
 */
void sha256_string(const char* str, uint8_t* hash) {
    if (str == NULL || hash == NULL) return;
    sha256_cpu((const uint8_t*)str, strlen(str), hash);
}

/**
 * @brief Вычисление SHA-256 хэшей для массива данных фиксированного размера
 */
void sha256_hash_all(const uint8_t* data, uint32_t num_elements,
                     uint32_t element_size, uint8_t* hashes) {
    if (data == NULL || hashes == NULL || num_elements == 0) return;
    
    for (uint32_t i = 0; i < num_elements; i++) {
        sha256_cpu(data + i * element_size, element_size, hashes + i * 32);
    }
}
