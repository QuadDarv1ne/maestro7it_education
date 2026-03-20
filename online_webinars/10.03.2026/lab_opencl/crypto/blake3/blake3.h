/**
 * @file blake3.h
 * @brief BLAKE3 — самый быстрый современный криптографический хэш
 * 
 * BLAKE3 быстрее MD5, SHA-1, SHA-2 и SHA-3.
 * Поддерживает параллелизм на уровне алгоритма.
 * 
 * @see https://github.com/BLAKE3-team/BLAKE3
 * @see https://blake3.io/
 */

#ifndef BLAKE3_H
#define BLAKE3_H

#include <stdint.h>
#include <stddef.h>

#ifdef __cplusplus
extern "C" {
#endif

// ============================================================
// КОНСТАНТЫ
// ============================================================

/** Размер хэша BLAKE3 по умолчанию (байт) */
#define BLAKE3_OUT_LEN 32

/** Размер ключа BLAKE3 (байт) */
#define BLAKE3_KEY_LEN 32

/** Размер чанка BLAKE3 (байт) */
#define BLAKE3_CHUNK_LEN 1024

/** Максимальная глубина дерева */
#define BLAKE3_MAX_DEPTH 54

/** Максимальная длина вывода для XOF (байт) */
#define BLAKE3_MAX_XOF_LEN 0xFFFFFFFF

// ============================================================
// СТРУКТУРЫ
// ============================================================

/**
 * @brief Контекст хэширования BLAKE3
 */
typedef struct {
    uint32_t cv[8];        /**< chaining value */
    uint64_t counter;      /**< счётчик байт */
    uint8_t block[64];     /**< буфер блока */
    uint8_t block_len;     /**< длина заполненной части блока */
    uint8_t compress_len;  /**< длина для сжатия */
    uint8_t flags;         /**< флаги */
    uint8_t pad[2];        /**< выравнивание */
} blake3_ctx_t;

/**
 * @brief Контекст для поточного хэширования (XOF)
 */
typedef struct {
    blake3_ctx_t core;
    uint8_t cv[32];        /**< сжатый cv для XOF */
    uint8_t cv_done;       /**< флаг готовности cv */
} blake3_xof_ctx_t;

// ============================================================
// ФУНКЦИИ
// ============================================================

/**
 * @brief Инициализация контекста BLAKE3
 */
void blake3_init(blake3_ctx_t* ctx);

/**
 * @brief Инициализация с ключом (keyed hash)
 */
void blake3_init_key(blake3_ctx_t* ctx, const uint8_t key[BLAKE3_KEY_LEN]);

/**
 * @brief Инициализация для деривации ключа (KDF)
 */
void blake3_init_derive(blake3_ctx_t* ctx, const uint8_t* material, 
                        size_t material_len, const char* context);

/**
 * @brief Добавление данных
 */
void blake3_update(blake3_ctx_t* ctx, const void* data, size_t len);

/**
 * @brief Завершение и получение хэша (32 байта)
 */
void blake3_final(blake3_ctx_t* ctx, void* out);

/**
 * @brief Вычисление хэша за один вызов
 */
void blake3(const void* input, size_t input_len, void* out, size_t out_len);

/**
 * @brief Вычисление хэша с ключом
 */
void blake3_keyed(const uint8_t key[BLAKE3_KEY_LEN], 
                  const void* input, size_t input_len, 
                  void* out, size_t out_len);

/**
 * @brief XOF — extendable output function
 */
void blake3_xof_init(blake3_xof_ctx_t* ctx);
void blake3_xof_update(blake3_xof_ctx_t* ctx, const void* data, size_t len);
void blake3_xof_final(blake3_xof_ctx_t* ctx, void* out, size_t out_len);

/**
 * @brief Convenience функция для строки
 */
void blake3_string(const char* str, char* hex_output);

#ifdef __cplusplus
}
#endif

#endif /* BLAKE3_H */
