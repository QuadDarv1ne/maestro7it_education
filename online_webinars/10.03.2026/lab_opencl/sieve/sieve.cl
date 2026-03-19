/*
 * OpenCL Kernel: Решето Эратосфена
 * Нахождение всех простых чисел до N
 * Оптимизированная версия
 */

// Инициализация массива: все числа >= 2 помечаются как простые
__kernel void init_array(__global uchar* is_prime, const uint limit) {
    uint gid = get_global_id(0);
    if (gid > limit) return;
    is_prime[gid] = (gid >= 2) ? 1 : 0;
}

// Маркировка кратных простого числа
// Каждый поток обрабатывает одно кратное, начиная с p*p
__kernel void sieve_mark_multiples(
    __global uchar* is_prime, const uint limit, const uint current_prime) {
    uint gid = get_global_id(0);
    uint start = current_prime * current_prime;
    if (start > limit) return;
    
    uint idx = start + current_prime * gid;
    if (idx <= limit) {
        is_prime[idx] = 0;
    }
}

// Альтернативная версия с использованием global_size для распределения нагрузки
__kernel void sieve_mark_cyclic(
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
