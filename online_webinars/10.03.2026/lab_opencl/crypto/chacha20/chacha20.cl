/**
 * @file chacha20.cl
 * @brief ChaCha20-Poly1305 OpenCL kernel
 * 
 * Параллельное шифрование на GPU.
 */

// ============================================================
// КОНСТАНТЫ
// ============================================================

#define CHACHA20_BLOCK_LEN 64

// ============================================================
// CHACHA20 QUARTER ROUND
// ============================================================

uint rotl32(uint v, uint n) {
    return (v << n) | (v >> (32 - n));
}

void quarter_round(uint* x, uint a, uint b, uint c, uint d) {
    x[a] += x[b]; x[d] = rotl32(x[d] ^ x[a], 16);
    x[c] += x[d]; x[b] = rotl32(x[b] ^ x[c], 12);
    x[a] += x[b]; x[d] = rotl32(x[d] ^ x[a], 8);
    x[c] += x[d]; x[b] = rotl32(x[b] ^ x[c], 7);
}

// ============================================================
// CHACHA20 BLOCK
// ============================================================

void chacha20_block(const uint state[16], uchar out[64]) {
    uint x[16];
    for (int i = 0; i < 16; i++) x[i] = state[i];
    
    // 20 раундов
    for (int i = 0; i < 10; i++) {
        // Column
        quarter_round(x, 0, 4, 8, 12);
        quarter_round(x, 1, 5, 9, 13);
        quarter_round(x, 2, 6, 10, 14);
        quarter_round(x, 3, 7, 11, 15);
        // Diagonal
        quarter_round(x, 0, 5, 10, 15);
        quarter_round(x, 1, 6, 11, 12);
        quarter_round(x, 2, 7, 8, 13);
        quarter_round(x, 3, 4, 9, 14);
    }
    
    // Add state
    for (int i = 0; i < 16; i++) x[i] += state[i];
    
    // Little-endian output
    for (int i = 0; i < 16; i++) {
        out[i*4 + 0] = x[i] & 0xFF;
        out[i*4 + 1] = (x[i] >> 8) & 0xFF;
        out[i*4 + 2] = (x[i] >> 16) & 0xFF;
        out[i*4 + 3] = (x[i] >> 24) & 0xFF;
    }
}

// ============================================================
// KERNEL: CHACHA20 ENCRYPT
// ============================================================

/**
 * @brief ChaCha20 шифрование
 * Каждый work-item шифрует один блок (64 байта)
 */
__kernel void chacha20_encrypt(
    __global const uchar* key,
    __global const uchar* nonce,
    __global const uchar* in,
    __global uchar* out,
    size_t data_len,
    uint start_counter
) {
    size_t gid = get_global_id(0);
    size_t num_blocks = (data_len + 63) / 64;
    
    if (gid >= num_blocks) return;
    
    // Инициализация состояния
    uint state[16];
    
    // Constants "expand 32-byte k"
    state[0] = 0x61707865;
    state[1] = 0x3320646e;
    state[2] = 0x79622d32;
    state[3] = 0x6b206574;
    
    // Key
    for (int i = 0; i < 8; i++) {
        state[4 + i] = ((uint)key[i*4 + 0]) |
                       ((uint)key[i*4 + 1] << 8) |
                       ((uint)key[i*4 + 2] << 16) |
                       ((uint)key[i*4 + 3] << 24);
    }
    
    // Counter
    state[12] = start_counter + (uint)gid;
    
    // Nonce
    for (int i = 0; i < 3; i++) {
        state[13 + i] = ((uint)nonce[i*4 + 0]) |
                        ((uint)nonce[i*4 + 1] << 8) |
                        ((uint)nonce[i*4 + 2] << 16) |
                        ((uint)nonce[i*4 + 3] << 24);
    }
    
    // Генерация keystream
    uchar keystream[64];
    chacha20_block(state, keystream);
    
    // XOR с данными
    size_t offset = gid * 64;
    size_t remaining = data_len - offset;
    size_t copy_len = (remaining < 64) ? remaining : 64;
    
    for (size_t i = 0; i < copy_len; i++) {
        out[offset + i] = in[offset + i] ^ keystream[i];
    }
}
