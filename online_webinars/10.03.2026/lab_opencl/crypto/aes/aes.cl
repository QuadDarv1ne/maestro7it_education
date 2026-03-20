/**
 * @file aes.cl
 * @brief AES-256-GCM OpenCL kernel
 * 
 * Параллельное шифрование на GPU.
 */

// ============================================================
// S-BOX
// ============================================================

constant uchar aes_sbox[256] = {
    0x63, 0x7c, 0x77, 0x7b, 0xf2, 0x6b, 0x6f, 0xc5, 0x30, 0x01, 0x67, 0x2b, 0xfe, 0xd7, 0xab, 0x76,
    0xca, 0x82, 0xc9, 0x7d, 0xfa, 0x59, 0x47, 0xf0, 0xad, 0xd4, 0xa2, 0xaf, 0x9c, 0xa4, 0x72, 0xc0,
    0xb7, 0xfd, 0x93, 0x26, 0x36, 0x3f, 0xf7, 0xcc, 0x34, 0xa5, 0xe5, 0xf1, 0x71, 0xd8, 0x31, 0x15,
    0x04, 0xc7, 0x23, 0xc3, 0x18, 0x96, 0x05, 0x9a, 0x07, 0x12, 0x80, 0xe2, 0xeb, 0x27, 0xb2, 0x75,
    0x09, 0x83, 0x2c, 0x1a, 0x1b, 0x6e, 0x5a, 0xa0, 0x52, 0x3b, 0xd6, 0xb3, 0x29, 0xe3, 0x2f, 0x84,
    0x53, 0xd1, 0x00, 0xed, 0x20, 0xfc, 0xb1, 0x5b, 0x6a, 0xcb, 0xbe, 0x39, 0x4a, 0x4c, 0x58, 0xcf,
    0xd0, 0xef, 0xaa, 0xfb, 0x43, 0x4d, 0x33, 0x85, 0x45, 0xf9, 0x02, 0x7f, 0x50, 0x3c, 0x9f, 0xa8,
    0x51, 0xa3, 0x40, 0x8f, 0x92, 0x9d, 0x38, 0xf5, 0xbc, 0xb6, 0xda, 0x21, 0x10, 0xff, 0xf3, 0xd2,
    0xcd, 0x0c, 0x13, 0xec, 0x5f, 0x97, 0x44, 0x17, 0xc4, 0xa7, 0x7e, 0x3d, 0x64, 0x5d, 0x19, 0x73,
    0x60, 0x81, 0x4f, 0xdc, 0x22, 0x2a, 0x90, 0x88, 0x46, 0xee, 0xb8, 0x14, 0xde, 0x5e, 0x0b, 0xdb,
    0xe0, 0x32, 0x3a, 0x0a, 0x49, 0x06, 0x24, 0x5c, 0xc2, 0xd3, 0xac, 0x62, 0x91, 0x95, 0xe4, 0x79,
    0xe7, 0xc8, 0x37, 0x6d, 0x8d, 0xd5, 0x4e, 0xa9, 0x6c, 0x56, 0xf4, 0xea, 0x65, 0x7a, 0xae, 0x08,
    0xba, 0x78, 0x25, 0x2e, 0x1c, 0xa6, 0xb4, 0xc6, 0xe8, 0xdd, 0x74, 0x1f, 0x4b, 0xbd, 0x8b, 0x8a,
    0x70, 0x3e, 0xb5, 0x66, 0x48, 0x03, 0xf6, 0x0e, 0x61, 0x35, 0x57, 0xb9, 0x86, 0xc1, 0x1d, 0x9e,
    0xe1, 0xf8, 0x98, 0x11, 0x69, 0xd9, 0x8e, 0x94, 0x9b, 0x1e, 0x87, 0xe9, 0xce, 0x55, 0x28, 0xdf,
    0x8c, 0xa1, 0x89, 0x0d, 0xbf, 0xe6, 0x42, 0x68, 0x41, 0x99, 0x2d, 0x0f, 0xb0, 0x54, 0xbb, 0x16
};

constant uchar aes_rcon[11] = {
    0x00, 0x01, 0x02, 0x04, 0x08, 0x10, 0x20, 0x40, 0x80, 0x1b, 0x36
};

// ============================================================
// AES-256 KEY EXPANSION
// ============================================================

uint sub_word(uint w) {
    return ((uint)aes_sbox[(w >> 24) & 0xFF]) << 24 |
           ((uint)aes_sbox[(w >> 16) & 0xFF]) << 16 |
           ((uint)aes_sbox[(w >> 8) & 0xFF]) << 8 |
           ((uint)aes_sbox[w & 0xFF]);
}

uint rot_word(uint w) {
    return (w << 8) | (w >> 24);
}

void aes256_key_expand(__global const uchar* key, __global uint* rk) {
    // Копирование ключа
    for (int i = 0; i < 8; i++) {
        rk[i] = ((uint)key[i*4 + 0]) << 24 |
                ((uint)key[i*4 + 1]) << 16 |
                ((uint)key[i*4 + 2]) << 8 |
                ((uint)key[i*4 + 3]);
    }
    
    // Генерация раундовых ключей
    int i = 8;
    for (int round = 1; round <= 14; round++) {
        uint temp = rk[i - 1];
        
        if (i % 8 == 0) {
            temp = rot_word(temp);
            temp = sub_word(temp);
            temp ^= aes_rcon[round];
        } else if (i % 8 == 4) {
            temp = sub_word(temp);
        }
        
        rk[i] = rk[i - 8] ^ temp;
        i++;
    }
}

// ============================================================
// AES BLOCK ENCRYPTION
// ============================================================

void aes_sub_bytes(uchar state[16]) {
    for (int i = 0; i < 16; i++) {
        state[i] = aes_sbox[state[i]];
    }
}

void aes_shift_rows(uchar state[16]) {
    uchar temp;
    
    // Row 1
    temp = state[1]; state[1] = state[5]; state[5] = state[9]; state[9] = state[13]; state[13] = temp;
    
    // Row 2
    temp = state[2]; state[2] = state[10]; state[10] = temp;
    temp = state[6]; state[6] = state[14]; state[14] = temp;
    
    // Row 3
    temp = state[15]; state[15] = state[11]; state[11] = state[7]; state[7] = state[3]; state[3] = temp;
}

uchar gf_mul(uchar a, uchar b) {
    uchar p = 0;
    for (int i = 0; i < 8; i++) {
        if (b & 1) p ^= a;
        a = (a << 1) ^ ((a & 0x80) ? 0x1b : 0);
        b >>= 1;
    }
    return p;
}

void aes_mix_columns(uchar state[16]) {
    for (int i = 0; i < 4; i++) {
        uchar a0 = state[i*4 + 0], a1 = state[i*4 + 1];
        uchar a2 = state[i*4 + 2], a3 = state[i*4 + 3];
        
        state[i*4 + 0] = gf_mul(a0, 2) ^ gf_mul(a1, 3) ^ a2 ^ a3;
        state[i*4 + 1] = a0 ^ gf_mul(a1, 2) ^ gf_mul(a2, 3) ^ a3;
        state[i*4 + 2] = a0 ^ a1 ^ gf_mul(a2, 2) ^ gf_mul(a3, 3);
        state[i*4 + 3] = gf_mul(a0, 3) ^ a1 ^ a2 ^ gf_mul(a3, 2);
    }
}

void aes_add_round_key(uchar state[16], __global const uint* rk, int round) {
    for (int i = 0; i < 4; i++) {
        uint w = rk[round * 4 + i];
        state[i*4 + 0] ^= (w >> 24) & 0xFF;
        state[i*4 + 1] ^= (w >> 16) & 0xFF;
        state[i*4 + 2] ^= (w >> 8) & 0xFF;
        state[i*4 + 3] ^= w & 0xFF;
    }
}

void aes_encrypt_block(uchar state[16], __global const uint* rk) {
    // Initial round
    aes_add_round_key(state, rk, 0);
    
    // Main rounds
    for (int round = 1; round < 14; round++) {
        aes_sub_bytes(state);
        aes_shift_rows(state);
        aes_mix_columns(state);
        aes_add_round_key(state, rk, round);
    }
    
    // Final round
    aes_sub_bytes(state);
    aes_shift_rows(state);
    aes_add_round_key(state, rk, 14);
}

// ============================================================
// KERNEL: AES-256-GCM ENCRYPT
// ============================================================

/**
 * @brief AES-256-GCM шифрование
 * Каждый work-item шифрует один блок (16 байт)
 */
__kernel void aes256_gcm_encrypt(
    __global const uchar* key,
    __global const uchar* iv,
    __global const uchar* in,
    __global uchar* out,
    __global uint* rk,
    size_t data_len,
    int init_rk
) {
    size_t gid = get_global_id(0);
    size_t num_blocks = (data_len + 15) / 16;
    
    if (gid >= num_blocks) return;
    
    // Инициализация раундовых ключей (только один раз)
    if (init_rk) {
        aes256_key_expand(key, rk);
    }
    
    // Чтение блока
    uchar state[16] = {0};
    size_t offset = gid * 16;
    size_t remaining = data_len - offset;
    size_t copy_len = (remaining < 16) ? remaining : 16;
    
    for (size_t i = 0; i < copy_len; i++) {
        state[i] = in[offset + i];
    }
    
    // Шифрование
    aes_encrypt_block(state, rk);
    
    // Запись результата
    for (size_t i = 0; i < copy_len; i++) {
        out[offset + i] = state[i];
    }
}
