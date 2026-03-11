/*
 * Общие определения для тестов
 */

#ifndef TEST_COMMON_H
#define TEST_COMMON_H

#include <stdio.h>
#include <stdlib.h>
#include <string.h>

/* Макросы для тестирования */
#define TEST_ASSERT(condition, message) do { \
    if (!(condition)) { \
        fprintf(stderr, "FAILED: %s (line %d): %s\n", __FILE__, __LINE__, message); \
        test_failures++; \
    } else { \
        test_passes++; \
    } \
} while(0)

#define TEST_ASSERT_EQUAL(expected, actual, message) do { \
    if ((expected) != (actual)) { \
        fprintf(stderr, "FAILED: %s (line %d): %s (expected %ld, got %ld)\n", \
                __FILE__, __LINE__, message, (long)(expected), (long)(actual)); \
        test_failures++; \
    } else { \
        test_passes++; \
    } \
} while(0)

#define TEST_ASSERT_STR_EQUAL(expected, actual, message) do { \
    if (strcmp((expected), (actual)) != 0) { \
        fprintf(stderr, "FAILED: %s (line %d): %s (expected '%s', got '%s')\n", \
                __FILE__, __LINE__, message, (expected), (actual)); \
        test_failures++; \
    } else { \
        test_passes++; \
    } \
} while(0)

#define TEST_BEGIN(name) do { \
    printf("Running test: %s...\n", name); \
} while(0)

#define TEST_END() do { \
    printf("  Passed: %d, Failed: %d\n\n", test_passes, test_failures); \
} while(0)

/* Глобальные счётчики */
static int test_passes = 0;
static int test_failures = 0;

/* Функция вывода итогов */
static inline void test_summary(void) {
    printf("\n========================================\n");
    printf("TEST SUMMARY\n");
    printf("========================================\n");
    printf("  Passed:  %d\n", test_passes);
    printf("  Failed:  %d\n", test_failures);
    printf("  Total:   %d\n", test_passes + test_failures);
    printf("========================================\n");
    if (test_failures == 0) {
        printf("ALL TESTS PASSED!\n");
    } else {
        printf("SOME TESTS FAILED!\n");
    }
}

#endif /* TEST_COMMON_H */
