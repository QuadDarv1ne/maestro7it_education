/**
 * @file blake3.cl
 * @brief BLAKE3 OpenCL kernel
 * 
 * Параллельное хэширование на GPU.
 */

// ============================================================
// КОНСТАНТЫ
// ============================================================

constant uint BLAKE3_IV[8] = {
    0x6A09E667, 0xBB67AE85, 0x3C6EF372, 0xA54FF53A,
    0x510E527F, 0x9B05688C, 0x1F83D9AB, 0x5BE0CD19
};

#define CHUNK_START 1
#define CHUNK_END 2
#define ROOT 4

// ============================================================
// ВСПОМОГАТЕЛЬНЫЕ МАКРОСЫ
// ============================================================

#define ROTR32(x, n) (((x) >> (n)) | ((x) << (32 - (n))))

// ============================================================
// ФУНКЦИЯ СЖАТИЯ
// ============================================================

/** Mixing function G */
void blake3_mix_g(uint* v, uint a, uint b, uint c, uint d, uint x, uint y) {
    v[a] = v[a] + v[b] + x;
    v[d] = ROTR32(v[d] ^ v[a], 16);
    v[c] = v[c] + v[d];
    v[b] = ROTR32(v[b] ^ v[c], 12);
    v[a] = v[a] + v[b] + y;
    v[d] = ROTR32(v[d] ^ v[a], 8);
    v[c] = v[c] + v[d];
    v[b] = ROTR32(v[b] ^ v[c], 7);
}

/** Функция сжатия BLAKE3 */
void blake3_compress(uint cv[8], __local const uchar* block,
                     ulong counter, uint flags) {
    uint v[16];
    uint m[16];
    
    // Инициализация v
    for (int i = 0; i < 8; i++) {
        v[i] = cv[i];
        v[i + 8] = BLAKE3_IV[i];
    }
    
    v[12] ^= (uint)counter;
    v[13] ^= (uint)(counter >> 32);
    v[14] ^= flags;
    
    // Парсинг сообщения (little-endian)
    for (int i = 0; i < 16; i++) {
        m[i] = ((uint)block[i * 4 + 0]) |
               ((uint)block[i * 4 + 1] << 8) |
               ((uint)block[i * 4 + 2] << 16) |
               ((uint)block[i * 4 + 3] << 24);
    }
    
    // Permutation σ
    constant uint8_t sigma[10][16] = {
        {0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15},
        {2, 6, 3, 10, 7, 0, 4, 13, 1, 11, 12, 5, 9, 14, 15, 8},
        {3, 4, 10, 12, 13, 2, 7, 14, 6, 5, 9, 0, 11, 15, 8, 1},
        {10, 7, 12, 9, 14, 3, 13, 15, 0, 4, 11, 2, 5, 8, 1, 6},
        {12, 13, 9, 11, 15, 10, 14, 8, 2, 7, 5, 3, 4, 1, 6, 0},
        {9, 14, 11, 5, 8, 12, 15, 1, 3, 4, 0, 10, 7, 6, 14, 13},
        {11, 15, 5, 0, 1, 9, 8, 2, 10, 7, 3, 12, 13, 6, 4, 14},
        {5, 8, 0, 3, 2, 11, 1, 4, 12, 13, 10, 7, 6, 14, 15, 9},
        {0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15},
        {2, 6, 3, 10, 7, 0, 4, 13, 1, 11, 12, 5, 9, 14, 15, 8}
    };
    
    // 7 раундов
    for (int r = 0; r < 7; r++) {
        blake3_mix_g(v, 0, 4, 8, 12, m[sigma[r][0]], m[sigma[r][1]]);
        blake3_mix_g(v, 1, 5, 9, 13, m[sigma[r][2]], m[sigma[r][3]]);
        blake3_mix_g(v, 2, 6, 10, 14, m[sigma[r][4]], m[sigma[r][5]]);
        blake3_mix_g(v, 3, 7, 11, 15, m[sigma[r][6]], m[sigma[r][7]]);
        blake3_mix_g(v, 0, 5, 10, 15, m[sigma[r][8]], m[sigma[r][9]]);
        blake3_mix_g(v, 1, 6, 11, 12, m[sigma[r][10]], m[sigma[r][11]]);
        blake3_mix_g(v, 2, 7, 8, 13, m[sigma[r][12]], m[sigma[r][13]]);
        blake3_mix_g(v, 3, 4, 9, 14, m[sigma[r][14]], m[sigma[r][15]]);
    }
    
    // XOR с CV
    for (int i = 0; i < 8; i++) {
        cv[i] ^= v[i] ^ v[i + 8];
    }
}

// ============================================================
// KERNEL: BLAKE3
// ============================================================

/**
 * @brief Вычисление BLAKE3 хэша
 */
__kernel void blake3_hash(
    __global const uchar* input,
    __global const uint* input_lens,
    __global uchar* output,
    const uint max_len,
    const uint num_hashes
) {
    uint gid = get_global_id(0);
    if (gid >= num_hashes) return;
    
    uint offset = gid * max_len;
    uint len = input_lens[gid];
    
    // Инициализация CV
    uint cv[8];
    for (int i = 0; i < 8; i++) cv[i] = BLAKE3_IV[i];
    
    // Обработка полных блоков (64 байта)
    uint num_blocks = len / 64;
    ulong counter = 0;
    
    for (uint block = 0; block < num_blocks; block++) {
        counter += 64;
        uint flags = CHUNK_START;
        if (block == num_blocks - 1) flags |= CHUNK_END;
        
        __local uchar block_data[64];
        for (int i = 0; i < 64; i++) {
            block_data[i] = input[offset + block * 64 + i];
        }
        
        blake3_compress(cv, block_data, counter, flags);
    }
    
    // Обработка последнего блока с padding
    uint remaining = len % 64;
    __local uchar last_block[64];
    for (int i = 0; i < 64; i++) last_block[i] = 0;
    
    for (uint i = 0; i < remaining; i++) {
        last_block[i] = input[offset + num_blocks * 64 + i];
    }
    
    uint flags = CHUNK_END | ROOT;
    if (num_blocks == 0) flags |= CHUNK_START;
    
    blake3_compress(cv, last_block, counter + remaining, flags);
    
    // Вывод (32 байта, little-endian)
    for (int i = 0; i < 32; i++) {
        output[gid * 32 + i] = (cv[i / 4] >> ((i % 4) * 8)) & 0xFF;
    }
}
