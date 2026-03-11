# Makefile для тестов
# Лабораторная работа по GPU вычислениям

CC = gcc
CFLAGS = -O2 -Wall -Wextra -std=c99 -I..
LDFLAGS = -lm

# Для тестов с OpenCL
OPENCL_FLAGS = -lOpenCL

# Тесты
TESTS = test_sha256 test_sieve

# Все тесты
all: $(TESTS)

# Тест SHA-256
test_sha256: test_sha256.c test_common.h
	$(CC) $(CFLAGS) -o $@ test_sha256.c ../hashing/hash.c $(LDFLAGS) $(OPENCL_FLAGS)

# Тест Решета Эратосфена
test_sieve: test_sieve.c test_common.h
	$(CC) $(CFLAGS) -o $@ test_sieve.c ../sieve/sieve.c $(LDFLAGS)

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
