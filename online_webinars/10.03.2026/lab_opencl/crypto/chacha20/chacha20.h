/**
 * @file chacha20.h
 * @brief ChaCha20-Poly1305 — современное AEAD шифрование
 * 
 * ChaCha20 — потоковый шифр (альтернатива AES).
 * Poly1305 — MAC для аутентификации.
 * 
 * @see RFC 8439 — ChaCha20 and Poly1305 for IETF Protocols
 * @see https://cr.yp.to/chacha.html
 */

#ifndef CHACHA20_H
#define CHACHA20_H

#include <stdint.h>
#include <stddef.h>

#ifdef __cplusplus
extern "C" {
#endif

// ============================================================
// КОНСТАНТЫ
// ============================================================

/** Размер ключа ChaCha20 (байт) */
#define CHACHA20_KEY_LEN 32

/** Размер nonce (байт) */
#define CHACHA20_NONCE_LEN 12

/** Размер тега Poly1305 (байт) */
#define POLY1305_TAG_LEN 16

/** Размер блока ChaCha20 (байт) */
#define CHACHA20_BLOCK_LEN 64

// ============================================================
// СТРУКТУРЫ
// ============================================================

/**
 * @brief Контекст ChaCha20
 */
typedef struct {
    uint32_t state[16];  /**< Состояние (16 x 32 бита) */
} chacha20_ctx_t;

/**
 * @brief Контекст Poly1305
 */
typedef struct {
    uint32_t r[4];       /**< R (clamp) */
    uint32_t s[4];       /**< S (ключ) */
    uint8_t buf[16];     /**< Буфер */
    size_t buf_len;      /**< Длина буфера */
    uint8_t pad;         /**< Паддинг */
} poly1305_ctx_t;

/**
 * @brief Контекст ChaCha20-Poly1305
 */
typedef struct {
    chacha20_ctx_t chacha;
    poly1305_ctx_t poly;
} chacha20_poly1305_ctx_t;

// ============================================================
// CHACHA20 ФУНКЦИИ
// ============================================================

/**
 * @brief Инициализация ChaCha20
 */
int chacha20_init(chacha20_ctx_t* ctx, const uint8_t key[CHACHA20_KEY_LEN],
                  const uint8_t nonce[CHACHA20_NONCE_LEN], uint32_t counter);

/**
 * @brief Шифрование/дешифрование (XOR)
 */
void chacha20_encrypt(chacha20_ctx_t* ctx, const uint8_t* in, uint8_t* out, size_t len);

/**
 * @brief Дешифрование (то же что шифрование)
 */
#define chacha20_decrypt chacha20_encrypt

// ============================================================
// POLY1305 ФУНКЦИИ
// ============================================================

/**
 * @brief Инициализация Poly1305
 */
void poly1305_init(poly1305_ctx_t* ctx, const uint8_t key[32]);

/**
 * @brief Добавление данных в MAC
 */
void poly1305_update(poly1305_ctx_t* ctx, const uint8_t* in, size_t len);

/**
 * @brief Завершение и получение тега
 */
void poly1305_final(poly1305_ctx_t* ctx, uint8_t tag[POLY1305_TAG_LEN]);

/**
 * @brief Вычисление MAC за один вызов
 */
void poly1305(const uint8_t key[32], const uint8_t* in, size_t len, uint8_t tag[16]);

// ============================================================
// CHACHA20-POLY1305 ФУНКЦИИ
// ============================================================

/**
 * @brief Шифрование с аутентификацией
 */
int chacha20_poly1305_encrypt(const uint8_t key[32], const uint8_t nonce[12],
                              const uint8_t* aad, size_t aad_len,
                              const uint8_t* in, size_t in_len,
                              uint8_t* out, uint8_t tag[16]);

/**
 * @brief Дешифрование с проверкой тега
 * @return 0 если тег верный, -1 если неверный
 */
int chacha20_poly1305_decrypt(const uint8_t key[32], const uint8_t nonce[12],
                              const uint8_t* aad, size_t aad_len,
                              const uint8_t* in, size_t in_len,
                              const uint8_t tag[16], uint8_t* out);

#ifdef __cplusplus
}
#endif

#endif /* CHACHA20_H */
