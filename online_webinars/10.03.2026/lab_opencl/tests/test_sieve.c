/*
 * Unit-тесты для Решета Эратосфена
 * 
 * Компиляция:
 *   gcc -o test_sieve test_sieve.c -I.. -I../sieve -lm
 * 
 * Запуск:
 *   ./test_sieve
 */

#include "test_common.h"
#include <stdint.h>
#include <math.h>

/* Внешние функции из sieve.c */
extern unsigned long sieve_cpu(unsigned char* is_prime, unsigned long limit);

/* Тест: Количество простых чисел до 10 */
void test_sieve_small(void) {
    TEST_BEGIN("Sieve small (N=10)");
    
    unsigned char is_prime[11];
    unsigned long count = sieve_cpu(is_prime, 10);
    
    /* Простые числа до 10: 2, 3, 5, 7 */
    TEST_ASSERT_EQUAL(4, count, "Should find 4 primes up to 10");
    
    /* Проверка конкретных чисел */
    TEST_ASSERT(is_prime[2], "2 should be prime");
    TEST_ASSERT(is_prime[3], "3 should be prime");
    TEST_ASSERT(is_prime[5], "5 should be prime");
    TEST_ASSERT(is_prime[7], "7 should be prime");
    
    /* Составные числа */
    TEST_ASSERT(!is_prime[0], "0 should not be prime");
    TEST_ASSERT(!is_prime[1], "1 should not be prime");
    TEST_ASSERT(!is_prime[4], "4 should not be prime");
    TEST_ASSERT(!is_prime[6], "6 should not be prime");
    TEST_ASSERT(!is_prime[8], "8 should not be prime");
    TEST_ASSERT(!is_prime[9], "9 should not be prime");
    TEST_ASSERT(!is_prime[10], "10 should not be prime");
    
    TEST_END();
}

/* Тест: Количество простых чисел до 100 */
void test_sieve_100(void) {
    TEST_BEGIN("Sieve N=100");
    
    unsigned char is_prime[101];
    unsigned long count = sieve_cpu(is_prime, 100);
    
    /* Количество простых чисел до 100 = 25 */
    TEST_ASSERT_EQUAL(25, count, "Should find 25 primes up to 100");
    
    /* Проверка некоторых простых */
    TEST_ASSERT(is_prime[97], "97 should be prime");
    TEST_ASSERT(is_prime[89], "89 should be prime");
    
    /* Проверка некоторых составных */
    TEST_ASSERT(!is_prime[99], "99 should not be prime");
    TEST_ASSERT(!is_prime[77], "77 should not be prime");
    
    TEST_END();
}

/* Тест: Количество простых чисел до 1000 */
void test_sieve_1000(void) {
    TEST_BEGIN("Sieve N=1000");
    
    unsigned char* is_prime = (unsigned char*)malloc(1001);
    unsigned long count = sieve_cpu(is_prime, 1000);
    
    /* Количество простых чисел до 1000 = 168 */
    TEST_ASSERT_EQUAL(168, count, "Should find 168 primes up to 1000");
    
    /* Проверка некоторых простых */
    TEST_ASSERT(is_prime[997], "997 should be prime");
    TEST_ASSERT(is_prime[499], "499 should be prime");
    
    free(is_prime);
    TEST_END();
}

/* Тест: Количество простых чисел до 10000 */
void test_sieve_10000(void) {
    TEST_BEGIN("Sieve N=10000");
    
    unsigned char* is_prime = (unsigned char*)malloc(10001);
    unsigned long count = sieve_cpu(is_prime, 10000);
    
    /* Количество простых чисел до 10000 = 1229 */
    TEST_ASSERT_EQUAL(1229, count, "Should find 1229 primes up to 10000");
    
    free(is_prime);
    TEST_END();
}

/* Тест: Количество простых чисел до 100000 */
void test_sieve_100000(void) {
    TEST_BEGIN("Sieve N=100000");
    
    unsigned char* is_prime = (unsigned char*)malloc(100001);
    unsigned long count = sieve_cpu(is_prime, 100000);
    
    /* Количество простых чисел до 100000 = 9592 */
    TEST_ASSERT_EQUAL(9592, count, "Should find 9592 primes up to 100000");
    
    free(is_prime);
    TEST_END();
}

/* Тест: Проверка теоремы о распределении простых чисел */
void test_sieve_distribution(void) {
    TEST_BEGIN("Sieve prime distribution (Pi(x) ~ x/ln(x))");
    
    unsigned long n = 1000000;
    unsigned char* is_prime = (unsigned char*)malloc(n + 1);
    unsigned long count = sieve_cpu(is_prime, n);
    
    /* Теоретическое приближение: n / ln(n) */
    double approx = (double)n / log((double)n);
    
    /* Допускаем отклонение 10% */
    double error_percent = fabs((double)count - approx) / approx * 100.0;
    
    printf("    Actual count: %lu\n", count);
    printf("    Approximation: %.0f\n", approx);
    printf("    Error: %.2f%%\n", error_percent);
    
    TEST_ASSERT(error_percent < 10.0, "Error should be less than 10%");
    
    free(is_prime);
    TEST_END();
}

/* Тест: Первые несколько простых чисел */
void test_sieve_first_primes(void) {
    TEST_BEGIN("Sieve first primes");
    
    unsigned char is_prime[31];
    sieve_cpu(is_prime, 30);
    
    /* Первые 10 простых чисел */
    int expected_primes[] = {2, 3, 5, 7, 11, 13, 17, 19, 23, 29};
    
    for (int i = 0; i < 10; i++) {
        TEST_ASSERT(is_prime[expected_primes[i]], 
                    "Expected prime should be found");
    }
    
    TEST_END();
}

/* Тест: Квадраты простых чисел - составные */
void test_sieve_prime_squares(void) {
    TEST_BEGIN("Sieve prime squares are composite");
    
    unsigned char is_prime[101];
    sieve_cpu(is_prime, 100);
    
    /* Квадраты простых чисел должны быть составными */
    int primes[] = {2, 3, 5, 7};
    for (int i = 0; i < 4; i++) {
        int square = primes[i] * primes[i];
        if (square <= 100) {
            TEST_ASSERT(!is_prime[square], 
                        "Square of prime should be composite");
        }
    }
    
    TEST_END();
}

int main(void) {
    printf("========================================\n");
    printf("Sieve of Eratosthenes Unit Tests\n");
    printf("========================================\n\n");
    
    test_sieve_small();
    test_sieve_100();
    test_sieve_1000();
    test_sieve_10000();
    test_sieve_100000();
    test_sieve_distribution();
    test_sieve_first_primes();
    test_sieve_prime_squares();
    
    test_summary();
    
    return (test_failures > 0) ? 1 : 0;
}
