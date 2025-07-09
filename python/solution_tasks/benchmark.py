import time
import math
import threading
import multiprocessing
from functools import partial
import platform
import sys
import io
import locale
from typing import Callable, Dict, Tuple, List
from tqdm import tqdm

def configure_environment():
    """Инициализация окружения и настройка кодировки."""
    if sys.version_info < (3, 7):
        print("Требуется Python 3.7 или выше")
        sys.exit(1)

    if sys.platform == 'win32':
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
        sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')
        try:
            import win32api, win32process
            win32process.SetPriorityClass(win32api.GetCurrentProcess(),
                                        win32process.HIGH_PRIORITY_CLASS)
        except ImportError:
            pass
    else:
        locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')

configure_environment()

def fibonacci(n: int, progress=False) -> int:
    """Вычисление чисел Фибоначчи с индикатором прогресса."""
    cache = {0: 0, 1: 1}

    def fib(n):
        if n not in cache:
            cache[n] = fib(n-1) + fib(n-2)
        return cache[n]

    if progress:
        for i in tqdm(range(n), desc='Фибоначчи'):
            fib(i)
    else:
        fib(n)

    return fib(n)

def matrix_multiply(size: int, progress=False) -> List[List[float]]:
    """Умножение матриц с индикатором прогресса."""
    a = [[float(i+j) for j in range(size)] for i in range(size)]
    b = [[float(i-j) for j in range(size)] for i in range(size)]
    result = [[0.0 for _ in range(size)] for _ in range(size)]

    if progress:
        with tqdm(total=size*size, desc='Матрицы') as pbar:
            for i in range(size):
                for j in range(size):
                    result[i][j] = sum(a[i][k] * b[k][j] for k in range(size))
                    pbar.update(1)
    else:
        for i in range(size):
            for j in range(size):
                result[i][j] = sum(a[i][k] * b[k][j] for k in range(size))

    return result

def prime_sieve(n: int) -> List[int]:
    """Решето Эратосфена для нахождения простых чисел до n."""
    sieve = [True] * (n+1)
    sieve[0] = sieve[1] = False
    for i in tqdm(range(2, int(math.sqrt(n)) + 1), desc='Решето Эратосфена'):
        if sieve[i]:
            sieve[i*i :: i] = [False] * len(sieve[i*i :: i])
    return [i for i, is_prime in enumerate(sieve) if is_prime]

def heavy_compute(n: int) -> float:
    """Интенсивные вычисления с плавающей точкой."""
    result = 0.0
    for i in tqdm(range(n), desc='Вычисления'):
        result += math.sin(i) * math.cos(i) * math.sqrt(i + 1)
        result -= math.log(i + 1) if i > 0 else 0
    return result

def time_execution(task: Callable, task_name: str, warmup: int = 1, repeats: int = 2) -> Tuple[float, float]:
    """
    Точный замер времени выполнения с индикацией прогресса.
    """
    print(f"\nЗапуск теста: {task_name}")

    # Прогрев
    for i in range(warmup):
        print(f"Прогрев {i+1}/{warmup}", end='\r')
        task()

    # Основные замеры
    times = []
    for i in tqdm(range(repeats), desc='Тестирование'):
        start = time.perf_counter()
        task()
        times.append(time.perf_counter() - start)

    avg = sum(times) / repeats
    std_dev = math.sqrt(sum((t - avg)**2 for t in times) / repeats)
    return avg, std_dev

def task_runner(task):
    """Функция для выполнения задачи в многопоточном или многопроцессном режиме."""
    return task()

def run_benchmarks():
    """Основная функция выполнения тестов."""
    test_config = {
        "small": {
            "fib": 30,
            "matrix": 40,
            "sieve": 10**5,
            "compute": 10**6
        },
        "medium": {
            "fib": 35,
            "matrix": 60,
            "sieve": 10**6,
            "compute": 10**7
        }
    }

    config = test_config["medium"]

    tasks = {
        "Фибоначчи": (partial(fibonacci, config["fib"], True), True),
        "Умножение матриц": (partial(matrix_multiply, config["matrix"], True), True),
        "Решето Эратосфена": (partial(prime_sieve, config["sieve"]), True),
        "Вычисления": (partial(heavy_compute, config["compute"]), True),
    }

    print(f"\nТестирование на {platform.python_implementation()} {platform.python_version()}")
    print(f"Система: {platform.system()} {platform.release()} {platform.processor()}")
    print("=" * 60)

    # Запуск тестов в разных режимах
    for mode_name, mode_func in [
        ("Однопоточный", lambda t: t()),
        ("Многопоточный (4)", lambda t: [threading.Thread(target=task_runner, args=(t,)).start() for _ in range(4)]),
        ("Многопроцессный (4)", lambda t: [multiprocessing.Process(target=task_runner, args=(t,)).start() for _ in range(4)])
    ]:
        print(f"\n=== РЕЖИМ: {mode_name.upper()} ===")

        for name, (task, can_run) in tasks.items():
            if not can_run and "процесс" in mode_name.lower():
                print(f"{name:<20} {'N/A':>10}")
                continue

            try:
                if "поток" in mode_name.lower() or "процесс" in mode_name.lower():
                    if hasattr(task, 'func') and 'progress' in task.func.keywords:
                        task.func.keywords['progress'] = False

                if "поток" in mode_name.lower():
                    threads = [threading.Thread(target=task_runner, args=(task,)) for _ in range(4)]
                    for thread in threads:
                        thread.start()
                    for thread in threads:
                        thread.join()
                elif "процесс" in mode_name.lower():
                    processes = [multiprocessing.Process(target=task_runner, args=(task,)) for _ in range(4)]
                    for process in processes:
                        process.start()
                    for process in processes:
                        process.join()
                else:
                    avg, std = time_execution(task, name)
                    print(f"{name:<20} {avg:>8.3f}s ± {std:.3f}s")
            except Exception as e:
                print(f"{name:<20} {'Ошибка:':>10} {str(e)}")

if __name__ == "__main__":
    multiprocessing.freeze_support()
    try:
        run_benchmarks()
    except KeyboardInterrupt:
        print("\nТестирование прервано пользователем")
    except Exception as e:
        print(f"\nОшибка: {str(e)}", file=sys.stderr)
    finally:
        input("\nНажмите Enter для выхода...")
