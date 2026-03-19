/**
 * @file sha256.h
 * @brief CPU реализация SHA-256
 *
 * Стандартная реализация криптографической хэш-функции SHA-256
 * Выход: 256 бит (32 байта)
 * Размер блока: 512 бит (64 байта)
 * Количество раундов: 64
 */

#ifndef SHA256_H
#define SHA256_H

#include <stdint.h>
#include <stddef.h>

#ifdef __cplusplus
extern "C" {
#endif

/**
 * @brief Вычисление SHA-256 хэша для одного сообщения
 * @param data Входные данные
 * @param len Длина данных в байтах
 * @param hash Буфер для результата (32 байта)
 */
void sha256_cpu(const uint8_t* data, size_t len, uint8_t* hash);

/**
 * @brief Вычисление SHA-256 хэша для строки
 * @param str Входная строка (null-terminated)
 * @param hash Буфер для результата (32 байта)
 */
void sha256_string(const char* str, uint8_t* hash);

/**
 * @brief Вычисление SHA-256 хэша для массива данных
 * @param data Массив данных
 * @param num_elements Количество элементов
 * @param element_size Размер одного элемента в байтах
 * @param hashes Буфер для результатов (num_elements * 32 байта)
 */
void sha256_hash_all(const uint8_t* data, uint32_t num_elements,
                     uint32_t element_size, uint8_t* hashes);

#ifdef __cplusplus
}
#endif

#endif /* SHA256_H */
