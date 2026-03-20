/**
 * @file sha3.cl
 * @brief SHA-3 (Keccak) OpenCL kernel
 * 
 * Параллельное хэширование на GPU.
 * Каждый work-item вычисляет хэш для одного блока данных.
 */

// ============================================================
// КОНСТАНТЫ KECCAK
// ============================================================

constant ulong keccak_rndc[24] = {
    0x0000000000000001UL, 0x0000000000008082UL, 0x800000000000808aUL,
    0x8000000080008000UL, 0x000000000000808bUL, 0x0000000080000001UL,
    0x8000000080008081UL, 0x8000000000008009UL, 0x000000000000008aUL,
    0x0000000000000088UL, 0x0000000080008009UL, 0x000000008000000aUL,
    0x000000008000808bUL, 0x800000000000008bUL, 0x8000000000008089UL,
    0x8000000000008003UL, 0x8000000000008002UL, 0x8000000000000080UL,
    0x000000000000800aUL, 0x800000008000000aUL, 0x8000000080008081UL,
    0x8000000000008080UL, 0x0000000080000001UL, 0x8000000080008008UL
};

#define ROT64(x, n) (((x) << (n)) | ((x) >> (64 - (n))))

// ============================================================
// ФУНКЦИЯ ПЕРЕСТАНОВКИ KECCAK-F[1600]
// ============================================================

/**
 * @brief Permutation Keccak-f[1600] для GPU
 */
void keccak_f1600(__local ulong* state) {
    ulong t, bc[5];
    
    for (int round = 0; round < 24; round++) {
        // Theta
        for (int i = 0; i < 5; i++) {
            bc[i] = state[i] ^ state[i + 5] ^ state[i + 10] ^ state[i + 15] ^ state[i + 20];
        }
        
        for (int i = 0; i < 5; i++) {
            t = bc[(i + 4) % 5] ^ ROT64(bc[(i + 1) % 5], 1);
            state[i] ^= t;
            state[i + 5] ^= t;
            state[i + 10] ^= t;
            state[i + 15] ^= t;
            state[i + 20] ^= t;
        }
        
        // Rho & Pi
        t = state[1];
        state[1] = ROT64(state[6], 44);
        state[6] = ROT64(state[9], 20);
        state[9] = ROT64(state[22], 61);
        state[22] = ROT64(state[14], 39);
        state[14] = ROT64(state[20], 18);
        state[20] = ROT64(state[2], 62);
        state[2] = ROT64(state[12], 43);
        state[12] = ROT64(state[13], 25);
        state[13] = ROT64(state[19], 8);
        state[19] = ROT64(state[23], 56);
        state[23] = ROT64(state[15], 41);
        state[15] = ROT64(state[4], 27);
        state[4] = ROT64(state[24], 14);
        state[24] = ROT64(state[21], 2);
        state[21] = ROT64(state[8], 55);
        state[8] = ROT64(state[16], 45);
        state[16] = ROT64(state[5], 36);
        state[5] = ROT64(state[3], 28);
        state[3] = ROT64(state[18], 21);
        state[18] = ROT64(state[17], 15);
        state[17] = ROT64(state[11], 10);
        state[11] = ROT64(state[7], 6);
        state[7] = ROT64(state[10], 3);
        state[10] = ROT64(t, 1);
        
        // Chi
        for (int j = 0; j < 25; j += 5) {
            ulong local_bc[5];
            for (int i = 0; i < 5; i++) {
                local_bc[i] = state[j + i];
            }
            for (int i = 0; i < 5; i++) {
                state[j + i] ^= (~local_bc[(i + 1) % 5]) & local_bc[(i + 2) % 5];
            }
        }
        
        // Iota
        state[0] ^= keccak_rndc[round];
    }
}

// ============================================================
// KERNEL: SHA3-256
// ============================================================

/**
 * @brief Вычисление SHA3-256 хэша
 * 
 * @param input Входные данные
 * @param input_lens Длины входных данных для каждого элемента
 * @param output Выходные хэши (32 байта на элемент)
 * @param max_len Максимальная длина входных данных
 * @param num_hashes Количество хэшей
 */
__kernel void sha3_256_hash(
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
    
    // Инициализация состояния (SHA3-256: rate=136 байт, capacity=64 байта)
    __local ulong state[25];
    for (int i = 0; i < 25; i++) state[i] = 0;
    
    // Обработка полных блоков (136 байт)
    uint block_size = 136;
    uint num_blocks = len / block_size;
    
    for (uint block = 0; block < num_blocks; block++) {
        // XOR с данными (little-endian)
        for (uint j = 0; j < block_size; j += 8) {
            ulong word = 0;
            for (int k = 0; k < 8; k++) {
                uint pos = block * block_size + j + k;
                if (offset + pos < offset + len) {
                    word |= ((ulong)input[offset + pos]) << (k * 8);
                }
            }
            state[j / 8] ^= word;
        }
        
        keccak_f1600(state);
    }
    
    // Обработка последнего блока с padding
    uint remaining = len % block_size;
    __local uchar buffer[136];
    for (int i = 0; i < 136; i++) buffer[i] = 0;
    
    // Копирование остатка
    for (uint i = 0; i < remaining; i++) {
        buffer[i] = input[offset + num_blocks * block_size + i];
    }
    
    // Padding: 0x06 в конце данных, 0x80 в конце блока
    buffer[remaining] = 0x06;
    buffer[135] |= 0x80;
    
    // XOR с последним блоком
    for (uint j = 0; j < block_size; j += 8) {
        ulong word = 0;
        for (int k = 0; k < 8; k++) {
            word |= ((ulong)buffer[j + k]) << (k * 8);
        }
        state[j / 8] ^= word;
    }
    
    keccak_f1600(state);
    
    // Извлечение результата (32 байта, little-endian)
    for (int i = 0; i < 32; i++) {
        output[gid * 32 + i] = (state[i / 8] >> ((i % 8) * 8)) & 0xFF;
    }
}

// ============================================================
// KERNEL: SHA3-512
// ============================================================

/**
 * @brief Вычисление SHA3-512 хэша
 */
__kernel void sha3_512_hash(
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
    
    // Инициализация состояния (SHA3-512: rate=72 байта)
    __local ulong state[25];
    for (int i = 0; i < 25; i++) state[i] = 0;
    
    uint block_size = 72;
    uint num_blocks = len / block_size;
    
    for (uint block = 0; block < num_blocks; block++) {
        for (uint j = 0; j < block_size; j += 8) {
            ulong word = 0;
            for (int k = 0; k < 8; k++) {
                uint pos = block * block_size + j + k;
                if (offset + pos < offset + len) {
                    word |= ((ulong)input[offset + pos]) << (k * 8);
                }
            }
            state[j / 8] ^= word;
        }
        
        keccak_f1600(state);
    }
    
    // Padding
    uint remaining = len % block_size;
    __local uchar buffer[72];
    for (int i = 0; i < 72; i++) buffer[i] = 0;
    
    for (uint i = 0; i < remaining; i++) {
        buffer[i] = input[offset + num_blocks * block_size + i];
    }
    
    buffer[remaining] = 0x06;
    buffer[71] |= 0x80;
    
    for (uint j = 0; j < block_size; j += 8) {
        ulong word = 0;
        for (int k = 0; k < 8; k++) {
            word |= ((ulong)buffer[j + k]) << (k * 8);
        }
        state[j / 8] ^= word;
    }
    
    keccak_f1600(state);
    
    // Извлечение результата (64 байта)
    for (int i = 0; i < 64; i++) {
        output[gid * 64 + i] = (state[i / 8] >> ((i % 8) * 8)) & 0xFF;
    }
}

// ============================================================
// KERNEL: SHAKE128 (XOF)
// ============================================================

/**
 * @brief SHAKE128 — extendable-output function
 */
__kernel void shake128_hash(
    __global const uchar* input,
    __global const uint* input_lens,
    __global uchar* output,
    const uint max_len,
    const uint output_len,
    const uint num_hashes
) {
    uint gid = get_global_id(0);
    if (gid >= num_hashes) return;
    
    uint offset = gid * max_len;
    uint len = input_lens[gid];
    
    // SHAKE128: rate=168 байт
    __local ulong state[25];
    for (int i = 0; i < 25; i++) state[i] = 0;
    
    uint block_size = 168;
    uint num_blocks = len / block_size;
    
    for (uint block = 0; block < num_blocks; block++) {
        for (uint j = 0; j < block_size; j += 8) {
            ulong word = 0;
            for (int k = 0; k < 8; k++) {
                uint pos = block * block_size + j + k;
                word |= ((ulong)input[offset + pos]) << (k * 8);
            }
            state[j / 8] ^= word;
        }
        keccak_f1600(state);
    }
    
    // Padding для SHAKE: 0x1F
    uint remaining = len % block_size;
    __local uchar buffer[168];
    for (int i = 0; i < 168; i++) buffer[i] = 0;
    
    for (uint i = 0; i < remaining; i++) {
        buffer[i] = input[offset + num_blocks * block_size + i];
    }
    
    buffer[remaining] = 0x1F;
    buffer[167] |= 0x80;
    
    for (uint j = 0; j < block_size; j += 8) {
        ulong word = 0;
        for (int k = 0; k < 8; k++) {
            word |= ((ulong)buffer[j + k]) << (k * 8);
        }
        state[j / 8] ^= word;
    }
    
    keccak_f1600(state);
    
    // Извлечение результата (output_len байт)
    for (uint i = 0; i < output_len; i++) {
        output[gid * output_len + i] = (state[i / 8] >> ((i % 8) * 8)) & 0xFF;
    }
}
