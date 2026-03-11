/*
 * OpenCL Kernel: Решето Эратосфена
 * Нахождение всех простых чисел до N
 */

__kernel void init_array(__global uchar* is_prime, const ulong limit) {
    ulong gid = get_global_id(0);
    if (gid <= limit) {
        is_prime[gid] = (gid >= 2) ? 1 : 0;
    }
}

__kernel void sieve_mark_multiples(
    __global uchar* is_prime, const ulong limit, const ulong current_prime) {
    ulong gid = get_global_id(0);
    ulong start = current_prime * current_prime;
    ulong global_size = get_global_size(0);
    ulong multiple = start + current_prime * gid;
    while (multiple <= limit) {
        is_prime[multiple] = 0;
        multiple += current_prime * global_size;
    }
}

__kernel void count_primes(
    __global const uchar* is_prime, const ulong limit,
    __global uint* count) {
    ulong gid = get_global_id(0);
    ulong global_size = get_global_size(0);
    uint local_sum = 0;
    for (ulong i = gid; i <= limit; i += global_size) {
        if (is_prime[i]) local_sum++;
    }
    if (local_sum > 0) {
        atomic_add(count, local_sum);
    }
}
