/*
 * OpenCL Kernel: Параллельное хэширование
 * Вычисление SHA-256 хэшей для множества данных одновременно
 * 
 * SHA-256 - криптографический алгоритм хэширования
 * Параллелизм: каждый поток вычисляет хэш для своего блока данных
 */

// ============================================================
// КОНСТАНТЫ SHA-256
// ============================================================

// Начальные значения хэша (первые 32 бита дробных частей квадратных корней первых 8 простых чисел)
constant uint SHA256_H[8] = {
    0x6a09e667, 0xbb67ae85, 0x3c6ef372, 0xa54ff53a,
    0x510e527f, 0x9b05688c, 0x1f83d9ab, 0x5be0cd19
};

// Константы раунда (первые 32 бита дробных частей кубических корней первых 64 простых чисел)
constant uint SHA256_K[64] = {
    0x428a2f98, 0x71374491, 0xb5c0fbcf, 0xe9b5dba5, 0x3956c25b, 0x59f111f1, 0x923f82a4, 0xab1c5ed5,
    0xd807aa98, 0x12835b01, 0x243185be, 0x550c7dc3, 0x72be5d74, 0x80deb1fe, 0x9bdc06a7, 0xc19bf174,
    0xe49b69c1, 0xefbe4786, 0x0fc19dc6, 0x240ca1cc, 0x2de92c6f, 0x4a7484aa, 0x5cb0a9dc, 0x76f988da,
    0x983e5152, 0xa831c66d, 0xb00327c8, 0xbf597fc7, 0xc6e00bf3, 0xd5a79147, 0x06ca6351, 0x14292967,
    0x27b70a85, 0x2e1b2138, 0x4d2c6dfc, 0x53380d13, 0x650a7354, 0x766a0abb, 0x81c2c92e, 0x92722c85,
    0xa2bfe8a1, 0xa81a664b, 0xc24b8b70, 0xc76c51a3, 0xd192e819, 0xd6990624, 0xf40e3585, 0x106aa070,
    0x19a4c116, 0x1e376c08, 0x2748774c, 0x34b0bcb5, 0x391c0cb3, 0x4ed8aa4a, 0x5b9cca4f, 0x682e6ff3,
    0x748f82ee, 0x78a5636f, 0x84c87814, 0x8cc70208, 0x90befffa, 0xa4506ceb, 0xbef9a3f7, 0xc67178f2
};

// ============================================================
// ВСПОМОГАТЕЛЬНЫЕ ФУНКЦИИ SHA-256
// ============================================================

// Циклический сдвиг вправо
#define ROTR(x, n) (((x) >> (n)) | ((x) << (32 - (n))))

// Логические функции SHA-256
#define CH(x, y, z)  (((x) & (y)) ^ (~(x) & (z)))
#define MAJ(x, y, z) (((x) & (y)) ^ ((x) & (z)) ^ ((y) & (z)))
#define EP0(x)       (ROTR(x, 2) ^ ROTR(x, 13) ^ ROTR(x, 22))
#define EP1(x)       (ROTR(x, 6) ^ ROTR(x, 11) ^ ROTR(x, 25))
#define SIG0(x)      (ROTR(x, 7) ^ ROTR(x, 18) ^ ((x) >> 3))
#define SIG1(x)      (ROTR(x, 17) ^ ROTR(x, 19) ^ ((x) >> 10))

// ============================================================
// ОСНОВНОЙ KERNEL SHA-256
// ============================================================

/**
 * Вычисление SHA-256 хэша для одного сообщения
 * Корректная обработка padding для сообщений любой длины
 */
__kernel void sha256_hash(
    __global const uchar* input,
    __global const uint* input_lens,
    __global uchar* output,
    const uint max_len
)
{
    uint gid = get_global_id(0);
    uint offset = gid * max_len;
    uint len = input_lens[gid];

    uint w[64];
    uint h[8];
    for (int i = 0; i < 8; i++) h[i] = SHA256_H[i];

    // Количество 512-битных (64-байтных) блоков
    uint num_blocks = (len + 9 + 63) / 64;
    if (num_blocks < 1) num_blocks = 1;

    for (uint block = 0; block < num_blocks; block++) {
        // Обнуление массива слов
        for (int i = 0; i < 64; i++) w[i] = 0;

        // Копирование данных блока (big-endian)
        uint bytes_in_block = 0;
        for (uint i = 0; i < 64; i++) {
            uint pos = block * 64 + i;
            if (pos < len) {
                uint wi = i >> 2;
                uint bi = 3 - (i & 3);
                w[wi] |= ((uint)input[offset + pos]) << (bi << 3);
                bytes_in_block++;
            }
        }

        // Добавление padding
        uint pad_pos = bytes_in_block;
        if (pad_pos < 64) {
            uint wi = pad_pos >> 2;
            uint bi = 3 - (pad_pos & 3);
            w[wi] |= ((uint)0x80) << (bi << 3);
        }

        // Если это последний блок и осталось место для длины
        if (block == num_blocks - 1) {
            // Длина в битах (big-endian)
            w[14] = (len >> 29) & 0x07;
            w[15] = (len << 3) & 0xFFFFFFFF;
        }

        // Расширение слов
        for (int i = 16; i < 64; i++)
            w[i] = SIG1(w[i-2]) + w[i-7] + SIG0(w[i-15]) + w[i-16];

        // Основной цикл сжатия
        uint a = h[0], b = h[1], c = h[2], d = h[3];
        uint e = h[4], f = h[5], g = h[6], hv = h[7];
        for (int i = 0; i < 64; i++) {
            uint t1 = hv + EP1(e) + CH(e, f, g) + SHA256_K[i] + w[i];
            uint t2 = EP0(a) + MAJ(a, b, c);
            hv = g; g = f; f = e; e = d + t1;
            d = c; c = b; b = a; a = t1 + t2;
        }
        h[0] += a; h[1] += b; h[2] += c; h[3] += d;
        h[4] += e; h[5] += f; h[6] += g; h[7] += hv;
    }

    // Запись результата (big-endian)
    for (int i = 0; i < 8; i++) {
        output[gid * 32 + (i << 2) + 0] = (h[i] >> 24) & 0xFF;
        output[gid * 32 + (i << 2) + 1] = (h[i] >> 16) & 0xFF;
        output[gid * 32 + (i << 2) + 2] = (h[i] >> 8) & 0xFF;
        output[gid * 32 + (i << 2) + 3] = h[i] & 0xFF;
    }
}

// ============================================================
// УПРОЩЁННЫЕ ХЭШИ (для сравнения)
// ============================================================

/**
 * DJB2 хэш - простой и быстрый
 * Часто используется для хэш-таблиц
 */
__kernel void djb2_hash(
    __global const uchar* input,
    __global const uint* input_lens,
    __global uint* output,
    const uint max_len
)
{
    uint gid = get_global_id(0);
    uint offset = gid * max_len;
    uint len = input_lens[gid];
    
    uint hash = 5381;
    
    for (uint i = 0; i < len; i++) {
        hash = ((hash << 5) + hash) + input[offset + i];  // hash * 33 + c
    }
    
    output[gid] = hash;
}

/**
 * FNV-1a хэш - хороший для общего использования
 * Лучшее распределение чем DJB2
 */
__kernel void fnv1a_hash(
    __global const uchar* input,
    __global const uint* input_lens,
    __global uint* output,
    const uint max_len
)
{
    uint gid = get_global_id(0);
    uint offset = gid * max_len;
    uint len = input_lens[gid];
    
    // FNV offset basis и prime для 32 бит
    uint hash = 2166136261u;
    
    for (uint i = 0; i < len; i++) {
        hash ^= input[offset + i];
        hash *= 16777619u;
    }
    
    output[gid] = hash;
}

/**
 * Murmur-подобный хэш - быстрый и с хорошим распределением
 */
__kernel void murmur_hash(
    __global const uchar* input,
    __global const uint* input_lens,
    __global uint* output,
    const uint max_len,
    const uint seed
)
{
    uint gid = get_global_id(0);
    uint offset = gid * max_len;
    uint len = input_lens[gid];
    
    uint h = seed;
    uint c1 = 0xcc9e2d51;
    uint c2 = 0x1b873593;
    
    // Обрабатываем по 4 байта
    uint nblocks = len / 4;
    
    for (uint i = 0; i < nblocks; i++) {
        uint k = ((uint)input[offset + i*4 + 0]) |
                 ((uint)input[offset + i*4 + 1] << 8) |
                 ((uint)input[offset + i*4 + 2] << 16) |
                 ((uint)input[offset + i*4 + 3] << 24);
        
        k *= c1;
        k = ROTR(k, 15);
        k *= c2;
        
        h ^= k;
        h = ROTR(h, 13);
        h = h * 5 + 0xe6546b64;
    }
    
    // Обрабатываем оставшиеся байты
    uint tail = 0;
    uint tail_len = len & 3;
    
    for (uint i = 0; i < tail_len; i++) {
        tail |= ((uint)input[offset + nblocks * 4 + i]) << (i * 8);
    }
    
    if (tail_len > 0) {
        tail *= c1;
        tail = ROTR(tail, 15);
        tail *= c2;
        h ^= tail;
    }
    
    h ^= len;
    h ^= h >> 16;
    h *= 0x85ebca6b;
    h ^= h >> 13;
    h *= 0xc2b2ae35;
    h ^= h >> 16;
    
    output[gid] = h;
}

// ============================================================
// ПАРОЛЬНЫЕ ХЭШИ (для демонстрации криптографии)
// ============================================================

/**
 * Множественное хэширование для паролей (аналог PBKDF)
 * Итеративное применение хэша для увеличения времени вычисления
 */
__kernel void password_hash(
    __global const uchar* input,
    __global const uint* input_lens,
    __global uchar* output,
    const uint max_len,
    const uint iterations
)
{
    uint gid = get_global_id(0);
    uint offset = gid * max_len;
    uint len = input_lens[gid];
    
    // Начальное значение
    uint h[8];
    for (int i = 0; i < 8; i++) {
        h[i] = SHA256_H[i];
    }
    
    // Итеративное хэширование
    for (uint iter = 0; iter < iterations; iter++) {
        // Простой вариант: XOR с номером итерации
        uint w[64];
        for (int i = 0; i < 64; i++) w[i] = 0;
        
        // Добавляем данные
        for (uint i = 0; i < len && i < 56; i++) {
            uint word_idx = i / 4;
            uint byte_idx = 3 - (i % 4);
            w[word_idx] |= ((uint)input[offset + i]) << (byte_idx * 8);
        }
        
        // Добавляем номер итерации
        w[14] = iter;
        w[15] = len * 8;
        
        // Расширение
        for (int i = 16; i < 64; i++) {
            w[i] = SIG1(w[i-2]) + w[i-7] + SIG0(w[i-15]) + w[i-16];
        }
        
        // Сжатие
        uint a = h[0], b = h[1], c = h[2], d = h[3];
        uint e = h[4], f = h[5], g = h[6], h_val = h[7];
        
        for (int i = 0; i < 64; i++) {
            uint t1 = h_val + EP1(e) + CH(e, f, g) + SHA256_K[i] + w[i];
            uint t2 = EP0(a) + MAJ(a, b, c);
            h_val = g; g = f; f = e; e = d + t1;
            d = c; c = b; b = a; a = t1 + t2;
        }
        
        h[0] += a; h[1] += b; h[2] += c; h[3] += d;
        h[4] += e; h[5] += f; h[6] += g; h[7] += h_val;
    }
    
    // Записываем результат
    for (int i = 0; i < 8; i++) {
        output[gid * 32 + i * 4 + 0] = (h[i] >> 24) & 0xFF;
        output[gid * 32 + i * 4 + 1] = (h[i] >> 16) & 0xFF;
        output[gid * 32 + i * 4 + 2] = (h[i] >> 8) & 0xFF;
        output[gid * 32 + i * 4 + 3] = h[i] & 0xFF;
    }
}

/**
 * Хэш с "солью" - для защиты от радужных таблиц
 */
__kernel void salted_hash(
    __global const uchar* input,
    __global const uint* input_lens,
    __global const uchar* salts,
    __global uchar* output,
    const uint max_len,
    const uint salt_len
)
{
    uint gid = get_global_id(0);
    uint offset = gid * max_len;
    uint len = input_lens[gid];
    
    uint w[64];
    for (int i = 0; i < 64; i++) w[i] = 0;
    
    uint pos = 0;
    
    // Добавляем соль
    for (uint i = 0; i < salt_len && pos < 56; i++, pos++) {
        uint word_idx = pos / 4;
        uint byte_idx = 3 - (pos % 4);
        w[word_idx] |= ((uint)salts[gid * salt_len + i]) << (byte_idx * 8);
    }
    
    // Добавляем данные
    for (uint i = 0; i < len && pos < 56; i++, pos++) {
        uint word_idx = pos / 4;
        uint byte_idx = 3 - (pos % 4);
        w[word_idx] |= ((uint)input[offset + i]) << (byte_idx * 8);
    }
    
    // Padding
    uint total_len = salt_len + len;
    if (pos < 56) {
        uint word_idx = pos / 4;
        uint byte_idx = 3 - (pos % 4);
        w[word_idx] |= ((uint)0x80) << (byte_idx * 8);
    }
    
    w[14] = 0;
    w[15] = total_len * 8;
    
    // Расширение
    for (int i = 16; i < 64; i++) {
        w[i] = SIG1(w[i-2]) + w[i-7] + SIG0(w[i-15]) + w[i-16];
    }
    
    // Хэширование
    uint h[8];
    for (int i = 0; i < 8; i++) h[i] = SHA256_H[i];
    
    uint a = h[0], b = h[1], c = h[2], d = h[3];
    uint e = h[4], f = h[5], g = h[6], h_val = h[7];
    
    for (int i = 0; i < 64; i++) {
        uint t1 = h_val + EP1(e) + CH(e, f, g) + SHA256_K[i] + w[i];
        uint t2 = EP0(a) + MAJ(a, b, c);
        h_val = g; g = f; f = e; e = d + t1;
        d = c; c = b; b = a; a = t1 + t2;
    }
    
    h[0] += a; h[1] += b; h[2] += c; h[3] += d;
    h[4] += e; h[5] += f; h[6] += g; h[7] += h_val;
    
    for (int i = 0; i < 8; i++) {
        output[gid * 32 + i * 4 + 0] = (h[i] >> 24) & 0xFF;
        output[gid * 32 + i * 4 + 1] = (h[i] >> 16) & 0xFF;
        output[gid * 32 + i * 4 + 2] = (h[i] >> 8) & 0xFF;
        output[gid * 32 + i * 4 + 3] = h[i] & 0xFF;
    }
}
