/*
 * OpenCL Kernel: Решето Эратосфена
 * Нахождение всех простых чисел до N
 * 
 * Объединенный kernel - делает инициализацию и решето за один проход
 */

// Инициализация массива
__kernel void init_array(__global uchar* is_prime, const uint limit) {
    uint gid = get_global_id(0);
    if (gid < 2) { is_prime[gid] = 0; return; }
    if (gid <= limit) is_prime[gid] = 1;
}

// Маркировка кратных (используется в цикле на CPU)
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

// Объединенный kernel: инициализация + решето
// Работает для small N, где весь массив помещается в global work size
__kernel void sieve_full(__global uchar* is_prime, const uint limit) {
    uint gid = get_global_id(0);
    
    // Фаза 1: инициализация
    if (gid < 2) {
        is_prime[gid] = 0;
    } else if (gid <= limit) {
        is_prime[gid] = 1;
    }
    
    // Синхронизация (work-group barrier)
    barrier(CLK_GLOBAL_MEM_FENCE);
    
    // Фаза 2: решето Эратосфена
    // Каждый поток проверяет одно число и маркует его кратные
    if (gid >= 2 && gid <= limit && is_prime[gid]) {
        uint start = gid * gid;
        if (start <= limit) {
            for (uint multiple = start; multiple <= limit; multiple += gid) {
                is_prime[multiple] = 0;
            }
        }
    }
}
