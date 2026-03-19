/*
 * OpenCL Kernel: Параллельное хэширование
 * Вычисление SHA-256 хэшей для множества данных одновременно
 *
 * SHA-256 - криптографический алгоритм хэширования
 * Параллелизм: каждый поток вычисляет хэш для своего блока данных
 *
 * ОПТИМИЗАЦИИ (версия 1.1):
 * - Использование локальной памяти для констант
 * - Loop unrolling для 64 раундов
 * - Оптимизированный доступ к глобальной памяти
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
// OPTIMIZED: Вспомогательная функция для загрузки данных
// ============================================================

/**
 * Быстрая загрузка 4 байт в слово (little-endian для OpenCL)
 */
inline uint load_word_be(__global const uchar* data, uint offset) {
    return ((uint)data[offset + 0] << 24) |
           ((uint)data[offset + 1] << 16) |
           ((uint)data[offset + 2] << 8) |
           ((uint)data[offset + 3]);
}

// ============================================================
// OPTIMIZED: ОСНОВНОЙ KERNEL SHA-256 С LOCAL MEMORY
// ============================================================

/**
 * Вычисление SHA-256 хэша для одного сообщения
 * Оптимизации:
 * - Загрузка констант в локальную память (shared между потоками work-group)
 * - Loop unrolling для 64 раундов
 * - Минимизация доступа к глобальной памяти
 */
__kernel void sha256_hash_optimized(
    __global const uchar* input,
    __global const uint* input_lens,
    __global uchar* output,
    const uint max_len,
    __local uint* local_k  // Локальная память для констант K (64 * 4 = 256 байт)
) {
    uint gid = get_global_id(0);
    uint lid = get_local_id(0);
    uint group_size = get_local_size(0);
    
    uint offset = gid * max_len;
    uint len = input_lens[gid];

    // Загрузка констант K в локальную память (кооперативно)
    // Каждый поток загружает несколько констант
    for (uint i = lid; i < 64; i += group_size) {
        local_k[i] = SHA256_K[i];
    }
    barrier(CLK_LOCAL_MEM_FENCE);

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

        // Если это последний блок - добавляем длину
        if (block == num_blocks - 1) {
            w[14] = (len >> 29) & 0x07;
            w[15] = (len << 3) & 0xFFFFFFFF;
        }

        // Расширение слов (unrolled для производительности)
        #pragma unroll
        for (int i = 16; i < 64; i++) {
            w[i] = SIG1(w[i-2]) + w[i-7] + SIG0(w[i-15]) + w[i-16];
        }

        // Основной цикл сжатия (полностью развернут для производительности)
        uint a = h[0], b = h[1], c = h[2], d = h[3];
        uint e = h[4], f = h[5], g = h[6], hv = h[7];

        // Раунды 0-15: используем w[i] напрямую
        #define ROUND(i) \
            do { \
                uint t1 = hv + EP1(e) + CH(e, f, g) + local_k[i] + w[i]; \
                uint t2 = EP0(a) + MAJ(a, b, c); \
                hv = g; g = f; f = e; e = d + t1; \
                d = c; c = b; b = a; a = t1 + t2; \
            } while(0)

        ROUND(0);  ROUND(1);  ROUND(2);  ROUND(3);
        ROUND(4);  ROUND(5);  ROUND(6);  ROUND(7);
        ROUND(8);  ROUND(9);  ROUND(10); ROUND(11);
        ROUND(12); ROUND(13); ROUND(14); ROUND(15);

        // Раунды 16-63: используем расширенные w[i]
        ROUND(16); ROUND(17); ROUND(18); ROUND(19);
        ROUND(20); ROUND(21); ROUND(22); ROUND(23);
        ROUND(24); ROUND(25); ROUND(26); ROUND(27);
        ROUND(28); ROUND(29); ROUND(30); ROUND(31);
        ROUND(32); ROUND(33); ROUND(34); ROUND(35);
        ROUND(36); ROUND(37); ROUND(38); ROUND(39);
        ROUND(40); ROUND(41); ROUND(42); ROUND(43);
        ROUND(44); ROUND(45); ROUND(46); ROUND(47);
        ROUND(48); ROUND(49); ROUND(50); ROUND(51);
        ROUND(52); ROUND(53); ROUND(54); ROUND(55);
        ROUND(56); ROUND(57); ROUND(58); ROUND(59);
        ROUND(60); ROUND(61); ROUND(62); ROUND(63);

        #undef ROUND

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
// ОСНОВНОЙ KERNEL SHA-256 (оригинальная версия)
// ============================================================

/**
 * Вычисление SHA-256 хэша для одного сообщения
 * Корректная обработка padding для сообщений любой длины
 */
__kernel void sha256_hash(
    __global const uchar* input,
    __global const uint* input_lens,
    __global uchar* output,
    const uint max_len,
    const uint num_hashes
)
{
    uint gid = get_global_id(0);
    if (gid >= num_hashes) return;
    
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

        // Добавление padding (только в последний блок, если хватит места для длины)
        if (block == num_blocks - 1) {
            uint pad_pos = bytes_in_block;
            // Нужно место для 0x80 (1 байт) + длина (8 байт) = 9 байт
            // 64 - 9 = 55, поэтому добавляем если < 56
            if (pad_pos < 56) {
                uint wi = pad_pos >> 2;
                uint bi = 3 - (pad_pos & 3);
                w[wi] |= ((uint)0x80) << (bi << 3);
            }
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

// ============================================================
// SHA-512 KERNEL (НОВЫЙ)
// ============================================================

/**
 * SHA-512 Constants
 * Начальные значения (первые 64 бита дробных частей квадратных корней первых 8 простых чисел)
 * Константы раунда (первые 64 бита дробных частей кубических корней первых 80 простых чисел)
 */
constant ulong SHA512_H[8] = {
    0x6a09e667f3bcc908ULL, 0xbb67ae8584caa73bULL, 0x3c6ef372fe94f82bULL, 0xa54ff53a5f1d36f1ULL,
    0x510e527fade682d1ULL, 0x9b05688c2b3e6c1fULL, 0x1f83d9abfb41bd6bULL, 0x5be0cd19137e2179ULL
};

constant ulong SHA512_K[80] = {
    0x428a2f98d728ae22ULL, 0x7137449123ef65cdULL, 0xb5c0fbcfec4d3b2fULL, 0xe9b5dba58189dbbcULL,
    0x3956c25bf348b538ULL, 0x59f111f1b605d019ULL, 0x923f82a4af194f9bULL, 0xab1c5ed5da6d8118ULL,
    0xd807aa98a3030242ULL, 0x12835b0145706fbeULL, 0x243185be4ee4b28cULL, 0x550c7dc3d5ffb4e2ULL,
    0x72be5d74f27b896fULL, 0x80deb1fe3b1696b1ULL, 0x9bdc06a725c71235ULL, 0xc19bf174cf692694ULL,
    0xe49b69c19ef14ad2ULL, 0xefbe4786384f25e3ULL, 0x0fc19dc68b8cd5b5ULL, 0x240ca1cc77ac9c65ULL,
    0x2de92c6f592b0275ULL, 0x4a7484aa6ea6e483ULL, 0x5cb0a9dcbd41fbd4ULL, 0x76f988da831153b5ULL,
    0x983e5152ee66dfabULL, 0xa831c66d2db43210ULL, 0xb00327c898fb213fULL, 0xbf597fc7beef0ee4ULL,
    0xc6e00bf33da88fc2ULL, 0xd5a79147930aa725ULL, 0x06ca6351e003826fULL, 0x142929670a0e6e70ULL,
    0x27b70a8546d22ffcULL, 0x2e1b21385c26c926ULL, 0x4d2c6dfc5ac42aedULL, 0x53380d139d95b3dfULL,
    0x650a73548baf63deULL, 0x766a0abb3c77b2a8ULL, 0x81c2c92e47edaee6ULL, 0x92722c851482353bULL,
    0xa2bfe8a14cf10364ULL, 0xa81a664bbc423001ULL, 0xc24b8b70d0f89791ULL, 0xc76c51a30654be30ULL,
    0xd192e819d6ef5218ULL, 0xd69906245565a910ULL, 0xf40e35855771202aULL, 0x106aa07032bbd1b8ULL,
    0x19a4c116b8d2d0c8ULL, 0x1e376c085141ab53ULL, 0x2748774cdf8eeb99ULL, 0x34b0bcb5e19b48a8ULL,
    0x391c0cb3c5c95a63ULL, 0x4ed8aa4ae3418acbULL, 0x5b9cca4f7763e373ULL, 0x682e6ff3d6b2b8a3ULL,
    0x748f82ee5defb2fcULL, 0x78a5636f43172f60ULL, 0x84c87814a1f0ab72ULL, 0x8cc702081a6439ecULL,
    0x90befffa23631e28ULL, 0xa4506cebde82bde9ULL, 0xbef9a3f7b2c67915ULL, 0xc67178f2e372532bULL,
    0xca273eceea26619cULL, 0xd186b8c721c0c207ULL, 0xeada7dd6cde0eb1eULL, 0xf57d4f7fee6ed178ULL,
    0x06f067aa72176fbaULL, 0x0a637dc5a2c898a6ULL, 0x113f9804bef90daeULL, 0x1b710b35131c471bULL,
    0x28db77f523047d84ULL, 0x32caab7b40c72493ULL, 0x3c9ebe0a15c9bebcULL, 0x431d67c49c100d4cULL,
    0x4cc5d4becb3e42b6ULL, 0x597f299cfc657e2aULL, 0x5fcb6fab3ad6faecULL, 0x6c44198c4a475817ULL
};

// Макросы для SHA-512
#define ROTR64(x, n) (((x) >> (n)) | ((x) << (64 - (n))))
#define CH64(x, y, z)  (((x) & (y)) ^ (~(x) & (z)))
#define MAJ64(x, y, z) (((x) & (y)) ^ ((x) & (z)) ^ ((y) & (z)))
#define EP0_512(x)     (ROTR64(x, 28) ^ ROTR64(x, 34) ^ ROTR64(x, 39))
#define EP1_512(x)     (ROTR64(x, 14) ^ ROTR64(x, 18) ^ ROTR64(x, 41))
#define SIG0_512(x)    (ROTR64(x, 1) ^ ROTR64(x, 8) ^ ((x) >> 7))
#define SIG1_512(x)    (ROTR64(x, 19) ^ ROTR64(x, 61) ^ ((x) >> 6))

/**
 * SHA-512 хэш для одного сообщения
 * Выход: 512 бит (64 байта)
 * Размер блока: 1024 бита (128 байт)
 * Количество раундов: 80
 */
__kernel void sha512_hash(
    __global const uchar* input,
    __global const uint* input_lens,
    __global uchar* output,
    const uint max_len
) {
    uint gid = get_global_id(0);
    uint offset = gid * max_len;
    uint len = input_lens[gid];

    ulong w[80];
    ulong h[8];
    for (int i = 0; i < 8; i++) h[i] = SHA512_H[i];

    // Количество 1024-битных (128-байтных) блоков
    uint num_blocks = (len + 17 + 127) / 128;
    if (num_blocks < 1) num_blocks = 1;

    for (uint block = 0; block < num_blocks; block++) {
        // Обнуление массива слов
        for (int i = 0; i < 80; i++) w[i] = 0;

        // Копирование данных блока (big-endian)
        uint bytes_in_block = 0;
        for (uint i = 0; i < 128; i++) {
            uint pos = block * 128 + i;
            if (pos < len) {
                uint wi = i >> 3;
                uint bi = 7 - (i & 7);
                w[wi] |= ((ulong)input[offset + pos]) << (bi << 3);
                bytes_in_block++;
            }
        }

        // Добавление padding
        uint pad_pos = bytes_in_block;
        if (pad_pos < 128) {
            uint wi = pad_pos >> 3;
            uint bi = 7 - (pad_pos & 7);
            w[wi] |= ((ulong)0x80) << (bi << 3);
        }

        // Если это последний блок - добавляем длину
        if (block == num_blocks - 1) {
            // Длина в битах (big-endian, 128 бит)
            w[14] = 0;
            w[15] = ((ulong)len) << 3;
        }

        // Расширение слов
        for (int i = 16; i < 80; i++) {
            w[i] = SIG1_512(w[i-2]) + w[i-7] + SIG0_512(w[i-15]) + w[i-16];
        }

        // Основной цикл сжатия (80 раундов)
        ulong a = h[0], b = h[1], c = h[2], d = h[3];
        ulong e = h[4], f = h[5], g = h[6], hv = h[7];

        for (int i = 0; i < 80; i++) {
            ulong t1 = hv + EP1_512(e) + CH64(e, f, g) + SHA512_K[i] + w[i];
            ulong t2 = EP0_512(a) + MAJ64(a, b, c);
            hv = g; g = f; f = e; e = d + t1;
            d = c; c = b; b = a; a = t1 + t2;
        }

        h[0] += a; h[1] += b; h[2] += c; h[3] += d;
        h[4] += e; h[5] += f; h[6] += g; h[7] += hv;
    }

    // Запись результата (big-endian, 64 байта)
    for (int i = 0; i < 8; i++) {
        output[gid * 64 + (i << 3) + 0] = (h[i] >> 56) & 0xFF;
        output[gid * 64 + (i << 3) + 1] = (h[i] >> 48) & 0xFF;
        output[gid * 64 + (i << 3) + 2] = (h[i] >> 40) & 0xFF;
        output[gid * 64 + (i << 3) + 3] = (h[i] >> 32) & 0xFF;
        output[gid * 64 + (i << 3) + 4] = (h[i] >> 24) & 0xFF;
        output[gid * 64 + (i << 3) + 5] = (h[i] >> 16) & 0xFF;
        output[gid * 64 + (i << 3) + 6] = (h[i] >> 8) & 0xFF;
        output[gid * 64 + (i << 3) + 7] = h[i] & 0xFF;
    }
}

/**
 * SHA-384 хэш (усечённая версия SHA-512)
 * Выход: 384 бита (48 байт)
 * Использует другие начальные значения H
 */
constant ulong SHA384_H[8] = {
    0xcbbb9d5dc1059ed8ULL, 0x629a292a367cd507ULL, 0x9159015a3070dd17ULL, 0x152fecd8f70e5939ULL,
    0x67332667ffc00b31ULL, 0x8eb44a8768581511ULL, 0xdb0c2e0d64f98fa7ULL, 0x47b5481dbefa4fa4ULL
};

__kernel void sha384_hash(
    __global const uchar* input,
    __global const uint* input_lens,
    __global uchar* output,
    const uint max_len
) {
    uint gid = get_global_id(0);
    uint offset = gid * max_len;
    uint len = input_lens[gid];

    ulong w[80];
    ulong h[8];
    for (int i = 0; i < 8; i++) h[i] = SHA384_H[i];

    uint num_blocks = (len + 17 + 127) / 128;
    if (num_blocks < 1) num_blocks = 1;

    for (uint block = 0; block < num_blocks; block++) {
        for (int i = 0; i < 80; i++) w[i] = 0;

        uint bytes_in_block = 0;
        for (uint i = 0; i < 128; i++) {
            uint pos = block * 128 + i;
            if (pos < len) {
                uint wi = i >> 3;
                uint bi = 7 - (i & 7);
                w[wi] |= ((ulong)input[offset + pos]) << (bi << 3);
                bytes_in_block++;
            }
        }

        uint pad_pos = bytes_in_block;
        if (pad_pos < 128) {
            uint wi = pad_pos >> 3;
            uint bi = 7 - (pad_pos & 7);
            w[wi] |= ((ulong)0x80) << (bi << 3);
        }

        if (block == num_blocks - 1) {
            w[14] = 0;
            w[15] = ((ulong)len) << 3;
        }

        for (int i = 16; i < 80; i++) {
            w[i] = SIG1_512(w[i-2]) + w[i-7] + SIG0_512(w[i-15]) + w[i-16];
        }

        ulong a = h[0], b = h[1], c = h[2], d = h[3];
        ulong e = h[4], f = h[5], g = h[6], hv = h[7];

        for (int i = 0; i < 80; i++) {
            ulong t1 = hv + EP1_512(e) + CH64(e, f, g) + SHA512_K[i] + w[i];
            ulong t2 = EP0_512(a) + MAJ64(a, b, c);
            hv = g; g = f; f = e; e = d + t1;
            d = c; c = b; b = a; a = t1 + t2;
        }

        h[0] += a; h[1] += b; h[2] += c; h[3] += d;
        h[4] += e; h[5] += f; h[6] += g; h[7] += hv;
    }

    // Запись результата (48 байт, первые 6 слов)
    for (int i = 0; i < 6; i++) {
        output[gid * 48 + (i << 3) + 0] = (h[i] >> 56) & 0xFF;
        output[gid * 48 + (i << 3) + 1] = (h[i] >> 48) & 0xFF;
        output[gid * 48 + (i << 3) + 2] = (h[i] >> 40) & 0xFF;
        output[gid * 48 + (i << 3) + 3] = (h[i] >> 32) & 0xFF;
        output[gid * 48 + (i << 3) + 4] = (h[i] >> 24) & 0xFF;
        output[gid * 48 + (i << 3) + 5] = (h[i] >> 16) & 0xFF;
        output[gid * 48 + (i << 3) + 6] = (h[i] >> 8) & 0xFF;
        output[gid * 48 + (i << 3) + 7] = h[i] & 0xFF;
    }
}
