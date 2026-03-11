# Makefile для тестов Pintos
# Unit-тесты для приоритетного планирования

CC = gcc
CFLAGS = -O2 -Wall -Wextra -std=c99 -I..
LDFLAGS = 

TESTS = test_priority

all: $(TESTS)

test_priority: test_priority.c
	$(CC) $(CFLAGS) -o $@ test_priority.c $(LDFLAGS)

run: $(TESTS)
	@echo "========================================="
	@echo "Running Pintos priority tests..."
	@echo "========================================="
	@for test in $(TESTS); do \
		echo ""; \
		echo ">>> Running $$test..."; \
		./$$test || exit 1; \
	done
	@echo ""
	@echo "All tests passed!"

clean:
	rm -f $(TESTS) *.o

.PHONY: all run clean
