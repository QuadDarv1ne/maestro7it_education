/*
 * OpenCL Kernel: Решето Эратосфена
 * Нахождение всех простых чисел до N
 */

// Инициализация массива (байтовый массив)
__kernel void init_array(__global uchar* is_prime, const uint limit) {
    uint gid = get_global_id(0);
    if (gid < 2) { is_prime[gid] = 0; return; }
    if (gid <= limit) is_prime[gid] = 1;
}

// Маркировка кратных
__kernel void sieve_mark_multiples(
    __global uchar* is_prime, const uint limit, const uint current_prime) {
    uint gid = get_global_id(0);
    uint start = current_prime * current_prime;
    if (start > limit) return;
    uint global_size = get_global_size(0);
    uint multiple = start + current_prime * gid;
    while (multiple <= limit) {
        is_prime[multiple] = 0;
        multiple += current_prime * global_size;
    }
}

