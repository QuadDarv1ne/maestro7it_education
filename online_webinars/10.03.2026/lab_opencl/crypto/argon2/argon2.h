/**
 * @file argon2.h
 * @brief Argon2 — memory-hard функция хэширования (победитель PHC 2015)
 * 
 * Argon2 — самая защищённая функция для хэширования паролей.
 * Устойчива к GPU/ASIC/FPGA атакам благодаря требованию большого объёма памяти.
 * 
 * Варианты:
 * - Argon2d — быстрая, уязвима к side-channel (для криптовалют)
 * - Argon2i — устойчива к side-channel (для паролей)
 * - Argon2id — гибрид (рекомендуется по умолчанию)
 * 
 * @see RFC 9106 — Argon2 Memory-Hard Function for Password Hashing
 * @see https://github.com/P-H-C/phc-winner-argon2
 */

#ifndef ARGON2_H
#define ARGON2_H

#include <stdint.h>
#include <stddef.h>

#ifdef __cplusplus
extern "C" {
#endif

// ============================================================
// КОНСТАНТЫ
// ============================================================

/** Минимальная длина соли (байт) */
#define ARGON2_MIN_SALT_LEN 8

/** Рекомендуемая длина соли (байт) */
#define ARGON2_SALT_LEN 16

/** Минимальная длина хэша (байт) */
#define ARGON2_MIN_HASH_LEN 4

/** Максимальная длина хэша (байт) */
#define ARGON2_MAX_HASH_LEN 64

/** Минимальное время (итерации) */
#define ARGON2_MIN_TIME 1

/** Рекомендуемое время (итерации) */
#define ARGON2_DEFAULT_TIME 3

/** Минимальная память (KB) */
#define ARGON2_MIN_MEMORY 8

/** Рекомендуемая память (KB) */
#define ARGON2_DEFAULT_MEMORY 65536  // 64 MB

/** Минимальная параллельность */
#define ARGON2_MIN_LANES 1

/** Рекомендуемая параллельность */
#define ARGON2_DEFAULT_LANES 4

// ============================================================
// ТИПЫ ДАННЫХ
// ============================================================

/**
 * @brief Типы варианта Argon2
 */
typedef enum {
    ARGON2_D = 0,    /**< Data-dependent (быстрый, для криптовалют) */
    ARGON2_I = 1,    /**< Data-independent (устойчивый к side-channel) */
    ARGON2_ID = 2    /**< Гибрид (рекомендуется для паролей) */
} argon2_type_t;

/**
 * @brief Параметры Argon2
 */
typedef struct {
    argon2_type_t type;      /**< Тип варианта */
    uint32_t time_cost;      /**< Количество итераций */
    uint32_t memory_cost;    /**< Объём памяти в KB */
    uint32_t lanes;          /**< Параллельность (threads) */
    uint32_t hash_len;       /**< Длина вывода (байт) */
} argon2_params_t;

// ============================================================
// ФУНКЦИИ
// ============================================================

/**
 * @brief Хэширование с Argon2
 * 
 * @param password Пароль для хэширования
 * @param password_len Длина пароля
 * @param salt Соль (минимум 8 байт, рекомендуется 16)
 * @param salt_len Длина соли
 * @param hash Буфер для хэша
 * @param hash_len Длина хэша (4-64 байта)
 * @param params Параметры Argon2 (или NULL для значений по умолчанию)
 * @return 0 при успехе, -1 при ошибке
 */
int argon2_hash(const void* password, size_t password_len,
                const void* salt, size_t salt_len,
                void* hash, size_t hash_len,
                const argon2_params_t* params);

/**
 * @brief Хэширование Argon2id (рекомендуемый вариант)
 * 
 * @param password Пароль
 * @param password_len Длина пароля
 * @param salt Соль (16 байт)
 * @param hash Буфер для хэша (32 байта)
 * @return 0 при успехе, -1 при ошибке
 */
int argon2id_hash(const void* password, size_t password_len,
                  const void* salt, void* hash);

/**
 * @brief Проверка пароля против хэша
 * 
 * @param password Пароль для проверки
 * @param password_len Длина пароля
 * @param salt Соль
 * @param salt_len Длина соли
 * @param expected_hash Ожидаемый хэш
 * @param hash_len Длина хэша
 * @param params Параметры Argon2
 * @return 0 если пароль верный, -1 если неверный
 */
int argon2_verify(const void* password, size_t password_len,
                  const void* salt, size_t salt_len,
                  const void* expected_hash, size_t hash_len,
                  const argon2_params_t* params);

/**
 * @brief Генерация безопасной соли
 * 
 * @param salt Буфер для соли (минимум 8 байт)
 * @param salt_len Длина соли
 * @return 0 при успехе, -1 при ошибке
 */
int argon2_generate_salt(void* salt, size_t salt_len);

/**
 * @brief Получение строкового названия типа Argon2
 */
const char* argon2_type_name(argon2_type_t type);

#ifdef __cplusplus
}
#endif

#endif /* ARGON2_H */
