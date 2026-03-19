/*
 * OpenCL Kernel: Решето Эратосфена
 * Нахождение всех простых чисел до N
 */

// Инициализация массива (байтовый массив)
__kernel void init_array(__global uchar* is_prime, const uint limit) {
    uint gid = get_global_id(0);
    if (gid > limit) return;
    if (gid < 2) { 
        is_prime[gid] = 0; 
        return; 
    }
    is_prime[gid] = 1;
}

// Маркировка кратных - упрощённая версия
__kernel void sieve_mark_multiples(
    __global uchar* is_prime, const uint limit, const uint current_prime) {
    uint gid = get_global_id(0);
    uint start = current_prime * current_prime;
    if (start > limit) return;
    
    // Каждый поток обрабатывает одно кратное
    uint multiple = start + current_prime * gid;
    if (multiple <= limit) {
        is_prime[multiple] = 0;
    }
}

