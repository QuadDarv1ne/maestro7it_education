/**
 * @file sha3.h
 * @brief SHA-3 (Keccak) — NIST стандарт хэширования (2015)
 * 
 * SHA-3 отличается от SHA-2 конструкцией (губка вместо Merkle-Damgård).
 * Устойчив к атакам, применимым к SHA-2.
 * 
 * @see FIPS 202 — SHA-3 Standard: Permutation-Based Hash and Extendable-Output Functions
 * @see https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.202.pdf
 */

#ifndef SHA3_H
#define SHA3_H

#include <stdint.h>
#include <stddef.h>

#ifdef __cplusplus
extern "C" {
#endif

// ============================================================
// КОНСТАНТЫ
// ============================================================

/** Размер состояния Keccak (байт) */
#define SHA3_STATE_SIZE 200

/** Размер блока для SHA3-256 (байт) */
#define SHA3_256_BLOCK_SIZE 136

/** Размер блока для SHA3-512 (байт) */
#define SHA3_512_BLOCK_SIZE 72

/** Размер блока для SHAKE128 (байт) */
#define SHAKE128_BLOCK_SIZE 168

/** Размер блока для SHAKE256 (байт) */
#define SHAKE256_BLOCK_SIZE 136

/** Длина хэша SHA3-256 (байт) */
#define SHA3_256_HASH_LEN 32

/** Длина хэша SHA3-512 (байт) */
#define SHA3_512_HASH_LEN 64

// ============================================================
// СТРУКТУРЫ
// ============================================================

/**
 * @brief Контекст хэширования SHA-3
 */
typedef struct {
    uint64_t state[25];    /**< Состояние (5x5x64 бита) */
    uint8_t buffer[SHA3_STATE_SIZE]; /**< Буфер для входных данных */
    size_t buffer_len;     /**< Количество байт в буфере */
    size_t block_size;     /**< Размер блока (зависит от варианта) */
    size_t hash_len;       /**< Желаемая длина хэша */
    uint8_t delim;         /**< Разделитель (0x06 для SHA3, 0x1F для SHAKE) */
} sha3_ctx_t;

// ============================================================
// ФУНКЦИИ
// ============================================================

/**
 * @brief Инициализация контекста SHA3-256
 */
void sha3_256_init(sha3_ctx_t* ctx);

/**
 * @brief Инициализация контекста SHA3-512
 */
void sha3_512_init(sha3_ctx_t* ctx);

/**
 * @brief Инициализация контекста SHAKE128
 */
void shake128_init(sha3_ctx_t* ctx);

/**
 * @brief Инициализация контекста SHAKE256
 */
void shake256_init(sha3_ctx_t* ctx);

/**
 * @brief Добавление данных для хэширования
 */
void sha3_update(sha3_ctx_t* ctx, const void* data, size_t len);

/**
 * @brief Завершение хэширования и получение результата
 */
void sha3_final(sha3_ctx_t* ctx, void* hash);

/**
 * @brief Вычисление SHA3-256 хэша за один вызов
 */
void sha3_256(const void* data, size_t len, void* hash);

/**
 * @brief Вычисление SHA3-512 хэша за один вызов
 */
void sha3_512(const void* data, size_t len, void* hash);

/**
 * @brief Вычисление SHAKE128 XOF (extendable-output function)
 */
void shake128(const void* data, size_t len, void* output, size_t output_len);

/**
 * @brief Вычисление SHAKE256 XOF
 */
void shake256(const void* data, size_t len, void* output, size_t output_len);

/**
 * @brief Вычисление SHA3-256 для строки (hex вывод)
 */
void sha3_256_string(const char* str, char* hex_output);

#ifdef __cplusplus
}
#endif

#endif /* SHA3_H */
