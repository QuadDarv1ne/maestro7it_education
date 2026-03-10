/*
 * OpenCL Kernel: Решето Эратосфена
 * Нахождение всех простых чисел до N
 * 
 * Алгоритм: Каждый поток обрабатывает несколько чисел,
 * проверяя делимость на уже найденные простые числа
 */

// Вариант 1: Прямое решето - каждый поток отмечает кратные своего числа
__kernel void sieve_mark_multiples(
    __global uchar* is_prime,  // Массив флагов (0 = составное, 1 = простое)
    const uint limit,          // Верхняя граница N
    const uint current_prime   // Текущее простое число для обработки
)
{
    // Получаем глобальный ID потока
    uint gid = get_global_id(0);
    
    // Вычисляем начальное кратное (первое кратное >= current_prime^2)
    uint start = current_prime * current_prime;
    
    // Каждый поток обрабатывает числа с шагом current_prime * global_size
    // Это позволяет распределить работу между потоками
    uint global_size = get_global_size(0);
    
    // Начальная позиция для этого потока
    // кратные current_prime: current_prime^2, current_prime^2 + current_prime, ...
    // Распределяем их между потоками
    
    uint multiple = start + current_prime * gid;
    
    // Отмечаем все кратные для этого потока
    while (multiple <= limit) {
        is_prime[multiple] = 0;  // Отмечаем как составное
        multiple += current_prime * global_size;
    }
}

// Вариант 2: Оптимизированное решето с локальной памятью
__kernel void sieve_optimized(
    __global uchar* is_prime,
    const uint limit,
    const uint sqrt_limit,
    __local uint* local_primes,  // Локальная память для простых чисел
    const uint num_primes        // Количество простых до sqrt(limit)
)
{
    uint gid = get_global_id(0);
    uint lid = get_local_id(0);
    uint group_size = get_local_size(0);
    
    // Загружаем простые числа в локальную память (коалесцентный доступ)
    // Только первые num_primes потоков в группе загружают данные
    if (gid < num_primes) {
        // Простые числа передаются через локальную память
        // Это улучшает производительность за счёт кэширования
    }
    
    barrier(CLK_LOCAL_MEM_FENCE);
    
    // Каждый поток проверяет свой диапазон чисел
    // Используем сегментированный подход для лучшего использования кэша
    uint chunk_size = (limit - sqrt_limit) / get_global_size(0);
    uint start = sqrt_limit + 1 + gid * chunk_size;
    uint end = (gid == get_global_size(0) - 1) ? limit : start + chunk_size - 1;
    
    // Проверяем каждое число в диапазоне
    for (uint num = start; num <= end; num++) {
        uint is_num_prime = 1;
        
        // Проверяем делимость на все простые до sqrt(num)
        for (uint i = 0; i < num_primes; i++) {
            uint p = local_primes[i];
            if (p * p > num) break;
            if (num % p == 0) {
                is_num_prime = 0;
                break;
            }
        }
        
        if (is_num_prime) {
            is_prime[num] = 1;
        }
    }
}

// Вариант 3: Сегментированное решето - лучше для больших N
// Каждый work-group обрабатывает сегмент массива
__kernel void sieve_segmented(
    __global uchar* is_prime,
    const uint segment_low,
    const uint segment_high,
    __global const uint* primes,    // Простые числа до sqrt(N)
    const uint num_primes
)
{
    uint gid = get_global_id(0);
    uint global_size = get_global_size(0);
    
    // Каждый поток обрабатывает несколько сегментов
    // (для лучшего распределения работы при большом количестве простых)
    
    for (uint i = 0; i < num_primes; i++) {
        uint p = primes[i];
        
        // Находим первое кратное p в сегменте
        uint first_multiple = (segment_low / p) * p;
        if (first_multiple < p * p) {
            first_multiple = p * p;
        }
        if (first_multiple < segment_low) {
            first_multiple += p;
        }
        
        // Распределяем кратные между потоками
        uint idx = first_multiple + p * gid;
        
        while (idx <= segment_high) {
            is_prime[idx - segment_low] = 0;
            idx += p * global_size;
        }
    }
}

// Ядро для подсчёта количества простых чисел
__kernel void count_primes(
    __global const uchar* is_prime,
    const uint limit,
    __global uint* count,
    __local uint* local_count
)
{
    uint gid = get_global_id(0);
    uint lid = get_local_id(0);
    uint group_size = get_local_size(0);
    uint global_size = get_global_size(0);
    
    // Инициализация локального счётчика
    if (lid == 0) {
        local_count[0] = 0;
    }
    barrier(CLK_LOCAL_MEM_FENCE);
    
    // Каждый поток считает простые в своём диапазоне
    uint local_sum = 0;
    for (uint i = gid; i <= limit; i += global_size) {
        if (is_prime[i]) {
            local_sum++;
        }
    }
    
    // Атомарное сложение в локальную память
    atomic_add(local_count, local_sum);
    barrier(CLK_LOCAL_MEM_FENCE);
    
    // Только первый поток в группе записывает результат
    if (lid == 0) {
        atomic_add(count, local_count[0]);
    }
}

// Ядро для инициализации массива
__kernel void init_array(
    __global uchar* is_prime,
    const uint limit
)
{
    uint gid = get_global_id(0);
    
    if (gid <= limit) {
        // Изначально все числа считаем простыми (кроме 0 и 1)
        is_prime[gid] = (gid >= 2) ? 1 : 0;
    }
}
