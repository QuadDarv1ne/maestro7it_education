# Makefile для тестов
# Лабораторная работа по GPU вычислениям

CC = gcc
CFLAGS = -O2 -Wall -Wextra -std=c99 -I.. -I../include
LDFLAGS = -lm

# Для тестов с OpenCL
OPENCL_FLAGS = -lOpenCL

# Путь к общим исходникам
COMMON_SRC = ../src/cl_utils.c

# Тесты
TESTS = test_sha256 test_sieve test_hash_correctness test_sieve_correctness

# Все тесты
all: $(TESTS)

# Тест SHA-256
test_sha256: test_sha256.c test_common.h
	$(CC) $(CFLAGS) -o $@ test_sha256.c ../hashing/hash.c $(COMMON_SRC) $(LDFLAGS) $(OPENCL_FLAGS)

# Тест Решета Эратосфена
test_sieve: test_sieve.c test_common.h
	$(CC) $(CFLAGS) -o $@ test_sieve.c ../sieve/sieve.c $(COMMON_SRC) $(LDFLAGS) $(OPENCL_FLAGS)

# Тест корректности хэширования (CPU vs GPU)
test_hash_correctness: test_hash_correctness.c test_common.h
	$(CC) $(CFLAGS) -o $@ test_hash_correctness.c ../hashing/hash.c $(COMMON_SRC) $(LDFLAGS) $(OPENCL_FLAGS)

# Тест корректности решета (CPU vs GPU)
test_sieve_correctness: test_sieve_correctness.c test_common.h
	$(CC) $(CFLAGS) -o $@ test_sieve_correctness.c ../sieve/sieve.c $(COMMON_SRC) $(LDFLAGS) $(OPENCL_FLAGS)

# Запуск всех тестов
run: $(TESTS)
	@echo "========================================="
	@echo "Running all tests..."
	@echo "========================================="
	@for test in $(TESTS); do \
		echo ""; \
		echo ">>> Running $$test..."; \
		./$$test || exit 1; \
	done
	@echo ""
	@echo "========================================="
	@echo "All tests completed successfully!"
	@echo "========================================="

# Очистка
clean:
	rm -f $(TESTS) *.o

.PHONY: all run clean
