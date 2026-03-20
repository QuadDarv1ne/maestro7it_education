/**
 * @file aes.h
 * @brief AES-256-GCM — стандарт симметричного шифрования
 * 
 * AES (Advanced Encryption Standard) — стандарт шифрования США (FIPS 197).
 * GCM (Galois/Counter Mode) — режим с аутентификацией (AEAD).
 * 
 * @see FIPS 197 — Advanced Encryption Standard (AES)
 * @see NIST SP 800-38D — Recommendation for GCM Mode
 */

#ifndef AES_H
#define AES_H

#include <stdint.h>
#include <stddef.h>

#ifdef __cplusplus
extern "C" {
#endif

// ============================================================
// КОНСТАНТЫ
// ============================================================

/** Размер ключа AES-256 (байт) */
#define AES_256_KEY_LEN 32

/** Размер блока AES (байт) */
#define AES_BLOCK_LEN 16

/** Размер IV/nonce для GCM (байт) */
#define AES_GCM_IV_LEN 12

/** Размер тега аутентификации (байт) */
#define AES_GCM_TAG_LEN 16

/** Максимальный размер данных для шифрования */
#define AES_MAX_DATA_LEN (1024 * 1024 * 1024)  // 1 GB

// ============================================================
// СТРУКТУРЫ
// ============================================================

/**
 * @brief Контекст AES-256
 */
typedef struct {
    uint32_t rk[60];  /**< Раундовые ключи (60 для AES-256) */
    int rounds;       /**< Количество раундов (14 для AES-256) */
} aes256_ctx_t;

/**
 * @brief Контекст AES-256-GCM
 */
typedef struct {
    aes256_ctx_t aes;
    uint8_t h[AES_BLOCK_LEN];  /**< H = AES_K(0) для GHASH */
    uint8_t j0[AES_BLOCK_LEN]; /**< J0 для GCM */
} aes256_gcm_ctx_t;

// ============================================================
// AES-256 ФУНКЦИИ
// ============================================================

/**
 * @brief Инициализация AES-256
 * @param ctx Контекст AES
 * @param key Ключ (32 байта)
 * @return 0 при успехе
 */
int aes256_init(aes256_ctx_t* ctx, const uint8_t key[AES_256_KEY_LEN]);

/**
 * @brief Шифрование одного блока (16 байт)
 */
void aes256_encrypt_block(const aes256_ctx_t* ctx, 
                          const uint8_t in[AES_BLOCK_LEN],
                          uint8_t out[AES_BLOCK_LEN]);

/**
 * @brief Дешифрование одного блока
 */
void aes256_decrypt_block(const aes256_ctx_t* ctx, 
                          const uint8_t in[AES_BLOCK_LEN],
                          uint8_t out[AES_BLOCK_LEN]);

// ============================================================
// AES-256-GCM ФУНКЦИИ
// ============================================================

/**
 * @brief Инициализация AES-256-GCM
 */
int aes256_gcm_init(aes256_gcm_ctx_t* ctx, const uint8_t key[AES_256_KEY_LEN]);

/**
 * @brief Шифрование в режиме GCM
 * @param ctx Контекст GCM
 * @param iv Вектор инициализации (12 байт)
 * @param aad Дополнительные аутентифицируемые данные (может быть NULL)
 * @param aad_len Длина AAD
 * @param in Входные данные
 * @param in_len Длина входных данных
 * @param out Выходные данные (шифротекст)
 * @param tag Тег аутентификации (16 байт)
 * @return 0 при успехе
 */
int aes256_gcm_encrypt(aes256_gcm_ctx_t* ctx,
                       const uint8_t iv[AES_GCM_IV_LEN],
                       const uint8_t* aad, size_t aad_len,
                       const uint8_t* in, size_t in_len,
                       uint8_t* out, uint8_t tag[AES_GCM_TAG_LEN]);

/**
 * @brief Дешифрование в режиме GCM
 * @return 0 если тег верный, -1 если неверный
 */
int aes256_gcm_decrypt(aes256_gcm_ctx_t* ctx,
                       const uint8_t iv[AES_GCM_IV_LEN],
                       const uint8_t* aad, size_t aad_len,
                       const uint8_t* in, size_t in_len,
                       const uint8_t tag[AES_GCM_TAG_LEN],
                       uint8_t* out);

/**
 * @brief Шифрование за один вызов
 */
int aes256_gcm(const uint8_t key[AES_256_KEY_LEN],
               const uint8_t iv[AES_GCM_IV_LEN],
               const uint8_t* aad, size_t aad_len,
               const uint8_t* in, size_t in_len,
               uint8_t* out, uint8_t tag[AES_GCM_TAG_LEN]);

#ifdef __cplusplus
}
#endif

#endif /* AES_H */
