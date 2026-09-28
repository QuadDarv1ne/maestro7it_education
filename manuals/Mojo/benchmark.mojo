# benchmark.mojo — Бенчмарк вычислительной производительности
# Демонстрирует: time, циклы, Float64, списки

from std.time import perf_counter_ns


# ── Задача 1: Сумма квадратов (простая арифметика) ──
def sum_of_squares(n: Int) -> Float64:
    """Сумма квадратов чисел от 1 до n."""
    var total: Float64 = 0.0
    for i in range(1, n + 1):
        let x = Float64(i)
        total += x * x
    return total


# ── Задача 2: Числа Фибоначчи (итеративно) ──
def fibonacci(n: Int) -> Int:
    """n-е число Фибоначчи (итеративно)."""
    if n <= 1:
        return n
    var a: Int = 0
    var b: Int = 1
    for _ in range(2, n + 1):
        let temp = a + b
        a = b
        b = temp
    return b


# ── Задача 3: Проверка простых чисел (наивная) ──
def count_primes(limit: Int) -> Int:
    """Подсчёт простых чисел до limit (наивный алгоритм)."""
    var count: Int = 0
    for n in range(2, limit):
        var is_prime = True
        var d: Int = 2
        while d * d <= n:
            if n % d == 0:
                is_prime = False
                break
            d += 1
        if is_prime:
            count += 1
    return count


# ── Задача 4: Скалярное произведение (SIMD-подобная) ──
def dot_product(a: List[Float64], b: List[Float64]) -> Float64:
    """Скалярное произведение двух векторов."""
    var result: Float64 = 0.0
    for i in range(len(a)):
        result += a[i] * b[i]
    return result


# ── Вспомогательная функция: запуск и замер ──
def run_benchmark(name: String, func: fn () -> String, iterations: Int) -> String:
    """Запускает функцию iterations раз, возвращает форматированный результат."""
    # Прогрев (чтобы JIT не влиял на первый замер)
    _ = func()

    let start = perf_counter_ns()
    var result: String = ""
    for _ in range(iterations):
        result = func()
    let end = perf_counter_ns()

    let total_ns = end - start
    let avg_ms = Float64(total_ns) / Float64(iterations) / 1_000_000.0

    return t"  {name.ljust(35)} {avg_ms:>8.3f} мс   {result}"


# ── Точка входа ──
def main():
    print()
    print("╔" + "═" * 65 + "╗")
    print("║" + "  БЕНЧМАРК ПРОИЗВОДИТЕЛЬНОСТИ MOJO".ljust(64) + "║")
    print("╚" + "═" * 65 + "╝")
    print()
    print(t"  Запуск: 10 итераций на каждый тест")
    print("─" * 67)
    print(t"  {'Тест'.ljust(35)} {'Среднее'.rjust(10)}   {'Результат'}")
    print("─" * 67)

    # ── Тест 1: Сумма квадратов ──
    let r1 = run_benchmark(
        "Сумма квадратов (n=1 000 000)",
        fn () -> String:
            let s = sum_of_squares(1_000_000)
            return t"{s:.2e}",
        10
    )
    print(r1)

    # ── Тест 2: Фибоначчи ──
    let r2 = run_benchmark(
        "Фибоначчи (n=100 000)",
        fn () -> String:
            let f = fibonacci(100_000)
            return t"{f % 1_000_000}",
        10
    )
    print(r2)

    # ── Тест 3: Простые числа ──
    let r3 = run_benchmark(
        "Простые числа до 100 000",
        fn () -> String:
            let p = count_primes(100_000)
            return t"{p}",
        10
    )
    print(r3)

    # ── Тест 4: Скалярное произведение ──
    let r4 = run_benchmark(
        "Скалярное произведение (1M элементов)",
        fn () -> String:
            var a: List[Float64] = []
            var b: List[Float64] = []
            for i in range(1_000_000):
                a.append(Float64(i) * 0.5)
                b.append(Float64(i) * 0.3)
            let dp = dot_product(a, b)
            return t"{dp:.2e}",
        10
    )
    print(r4)

    print("─" * 67)
    print()
    print("  Готово. Сравните с аналогичными тестами на Python/C++.")
    print()


if __name__ == "__main__":
    main()
