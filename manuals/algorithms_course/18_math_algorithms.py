"""
МАТЕМАТИЧЕСКИЕ АЛГОРИТМЫ (MATHEMATICAL ALGORITHMS)

Математические алгоритмы — это фундаментальный класс алгоритмов, используемых
для решения вычислительных задач. Они часто встречаются в программировании
и требуют понимания математических основ.

Основные темы:
1. Теория чисел (простые числа, НОД, НОК)
2. Модульная арифметика
3. Комбинаторика
4. Геометрия
5. Работа с большими числами
6. Вероятностные алгоритмы

Важно:
- Многие алгоритмы требуют работы с большими числами
- Понимание математики критично для оптимизации
- Python поддерживает произвольную точность целых чисел
"""

from typing import List, Tuple, Optional, Set
import random


# ===== ПРОСТЫЕ ЧИСЛА =====

def is_prime_naive(n: int) -> bool:
    """
    Проверка простоты числа (наивный алгоритм).
    
    Проверяем все числа от 2 до n-1.
    
    Аргументы:
        n: число для проверки
    
    Возвращает:
        bool: True если n простое
    
    Сложность: O(n)
    """
    if n < 2:
        return False
    
    for i in range(2, n):
        if n % i == 0:
            return False
    
    return True


def is_prime_optimized(n: int) -> bool:
    """
    Оптимизированная проверка простоты.
    
    Проверяем только до √n и только нечётные делители.
    
    Сложность: O(√n)
    """
    if n < 2:
        return False
    if n == 2:
        return True
    if n % 2 == 0:
        return False
    
    i = 3
    while i * i <= n:
        if n % i == 0:
            return False
        i += 2
    
    return True


def is_prime_miller_rabin(n: int, k: int = 5) -> bool:
    """
    Тест Миллера-Рабина на простоту.
    
    Вероятностный алгоритм. Даёт правильный ответ с высокой вероятностью.
    Для n < 3,317,044,064,679,887,385,961,981 достаточно k=12 для точного ответа.
    
    Аргументы:
        n: число для проверки
        k: количество раундов тестирования
    
    Возвращает:
        bool: True если n вероятно простое
    
    Сложность: O(k × log³n)
    """
    if n < 2:
        return False
    if n == 2 or n == 3:
        return True
    if n % 2 == 0:
        return False
    
    # Представляем n-1 как 2^r × d
    r, d = 0, n - 1
    while d % 2 == 0:
        r += 1
        d //= 2
    
    # k раундов тестирования
    for _ in range(k):
        a = random.randrange(2, n - 1)
        x = pow(a, d, n)
        
        if x == 1 or x == n - 1:
            continue
        
        for _ in range(r - 1):
            x = pow(x, 2, n)
            if x == n - 1:
                break
        else:
            return False
    
    return True


def sieve_of_eratosthenes(n: int) -> List[int]:
    """
    Решето Эратосфена — нахождение всех простых чисел до n.
    
    Аргументы:
        n: верхняя граница
    
    Возвращает:
        list: все простые числа от 2 до n
    
    Сложность: O(n log log n)
    
    Пример:
        >>> sieve_of_eratosthenes(30)
        [2, 3, 5, 7, 11, 13, 17, 19, 23, 29]
    """
    if n < 2:
        return []
    
    # Создаём массив, где is_prime[i] = True значит i простое
    is_prime = [True] * (n + 1)
    is_prime[0] = is_prime[1] = False
    
    p = 2
    while p * p <= n:
        if is_prime[p]:
            # Отмечаем все кратные p как составные
            for i in range(p * p, n + 1, p):
                is_prime[i] = False
        p += 1
    
    return [i for i in range(2, n + 1) if is_prime[i]]


def sieve_linear(n: int) -> List[int]:
    """
    Линейное решето — находит все простые за O(n).
    
    Каждое составное число помечается ровно один раз.
    """
    if n < 2:
        return []
    
    is_prime = [True] * (n + 1)
    primes = []
    
    for i in range(2, n + 1):
        if is_prime[i]:
            primes.append(i)
        
        for p in primes:
            if p * i > n:
                break
            is_prime[p * i] = False
            if i % p == 0:
                break
    
    return primes


# ===== НОД И НОК =====

def gcd_euclidean(a: int, b: int) -> int:
    """
    Наибольший общий делитель (алгоритм Евклида).
    
    НОД(a, b) = НОД(b, a mod b)
    НОД(a, 0) = a
    
    Аргументы:
        a, b: целые числа
    
    Возвращает:
        int: НОД(a, b)
    
    Сложность: O(log(min(a, b)))
    
    Пример:
        >>> gcd_euclidean(48, 18)
        6
    """
    while b:
        a, b = b, a % b
    return abs(a)


def gcd_recursive(a: int, b: int) -> int:
    """Рекурсивная версия алгоритма Евклида."""
    if b == 0:
        return abs(a)
    return gcd_recursive(b, a % b)


def lcm(a: int, b: int) -> int:
    """
    Наименьшее общее кратное.
    
    НОК(a, b) = |a × b| / НОД(a, b)
    
    Аргументы:
        a, b: целые числа
    
    Возвращает:
        int: НОК(a, b)
    
    Сложность: O(log(min(a, b)))
    """
    if a == 0 or b == 0:
        return 0
    return abs(a * b) // gcd_euclidean(a, b)


def extended_gcd(a: int, b: int) -> Tuple[int, int, int]:
    """
    Расширенный алгоритм Евклида.
    
    Находит x и y такие, что a×x + b×y = НОД(a, b).
    
    Аргументы:
        a, b: целые числа
    
    Возвращает:
        tuple: (НОД, x, y)
    
    Сложность: O(log(min(a, b)))
    
    Применение:
    - Решение диофантовых уравнений
    - Нахождение обратного по модулю
    """
    if b == 0:
        return a, 1, 0
    
    g, x1, y1 = extended_gcd(b, a % b)
    x = y1
    y = x1 - (a // b) * y1
    
    return g, x, y


def mod_inverse(a: int, m: int) -> Optional[int]:
    """
    Мультипликативная обратная по модулю.
    
    Находит x такой, что (a × x) mod m = 1.
    Существует только если НОД(a, m) = 1.
    
    Аргументы:
        a: число
        m: модуль
    
    Возвращает:
        int: обратное число или None
    
    Сложность: O(log m)
    
    Пример:
        >>> mod_inverse(3, 7)  # 3 × 5 = 15 ≡ 1 (mod 7)
        5
    """
    g, x, _ = extended_gcd(a % m, m)
    
    if g != 1:
        return None  # Обратного не существует
    
    return x % m


# ===== РАЗЛОЖЕНИЕ НА МНОЖИТЕЛИ =====

def prime_factors(n: int) -> List[Tuple[int, int]]:
    """
    Разложение числа на простые множители.
    
    Возвращает список пар (простое число, степень).
    
    Аргументы:
        n: число для разложения
    
    Возвращает:
        list: [(p1, e1), (p2, e2), ...]
    
    Сложность: O(√n)
    
    Пример:
        >>> prime_factors(360)
        [(2, 3), (3, 2), (5, 1)]  # 360 = 2³ × 3² × 5
    """
    if n < 2:
        return []
    
    factors = []
    
    # Проверяем делимость на 2
    count = 0
    while n % 2 == 0:
        count += 1
        n //= 2
    if count > 0:
        factors.append((2, count))
    
    # Проверяем нечётные делители
    i = 3
    while i * i <= n:
        count = 0
        while n % i == 0:
            count += 1
            n //= i
        if count > 0:
            factors.append((i, count))
        i += 2
    
    # Если осталось число > 1, оно простое
    if n > 1:
        factors.append((n, 1))
    
    return factors


def count_divisors(n: int) -> int:
    """
    Количество делителей числа.
    
    Если n = p1^e1 × p2^e2 × ..., то количество делителей = (e1+1)×(e2+1)×...
    
    Аргументы:
        n: число
    
    Возвращает:
        int: количество положительных делителей
    
    Сложность: O(√n)
    """
    if n < 1:
        return 0
    if n == 1:
        return 1
    
    count = 1
    for _, exp in prime_factors(n):
        count *= (exp + 1)
    
    return count


def sum_divisors(n: int) -> int:
    """
    Сумма всех делителей числа.
    
    Для n = p1^e1 × p2^e2 × ...:
    Сумма = (p1^(e1+1) - 1)/(p1-1) × (p2^(e2+1) - 1)/(p2-1) × ...
    """
    if n < 1:
        return 0
    if n == 1:
        return 1
    
    total = 1
    for p, e in prime_factors(n):
        total *= (p**(e + 1) - 1) // (p - 1)
    
    return total


def euler_phi(n: int) -> int:
    """
    Функция Эйлера φ(n).
    
    Количество чисел от 1 до n, взаимно простых с n.
    
    Формула: φ(n) = n × ∏(1 - 1/p) для всех простых p|n
    
    Аргументы:
        n: число
    
    Возвращает:
        int: φ(n)
    
    Сложность: O(√n)
    
    Пример:
        >>> euler_phi(12)  # 1, 5, 7, 11
        4
    """
    if n < 1:
        return 0
    if n == 1:
        return 1
    
    result = n
    for p, _ in prime_factors(n):
        result = result // p * (p - 1)
    
    return result


# ===== БЫСТРОЕ ВОЗВЕДЕНИЕ В СТЕПЕНЬ =====

def power_naive(base: int, exp: int) -> int:
    """
    Возведение в степень наивным методом.
    
    Сложность: O(exp)
    """
    result = 1
    for _ in range(exp):
        result *= base
    return result


def power_binary(base: int, exp: int) -> int:
    """
    Быстрое возведение в степень (бинарное).
    
    Использует представление степени в двоичном виде.
    
    Аргументы:
        base: основание
        exp: показатель степени
    
    Возвращает:
        int: base^exp
    
    Сложность: O(log exp)
    
    Пример:
        >>> power_binary(2, 10)
        1024
    """
    result = 1
    b = base
    
    while exp > 0:
        if exp % 2 == 1:
            result *= b
        b *= b
        exp //= 2
    
    return result


def power_mod(base: int, exp: int, mod: int) -> int:
    """
    Быстрое возведение в степень по модулю.
    
    Аргументы:
        base: основание
        exp: показатель степени
        mod: модуль
    
    Возвращает:
        int: (base^exp) mod mod
    
    Сложность: O(log exp)
    """
    result = 1
    base = base % mod
    
    while exp > 0:
        if exp % 2 == 1:
            result = (result * base) % mod
        exp //= 2
        base = (base * base) % mod
    
    return result


# ===== КОМБИНАТОРИКА =====

def factorial(n: int) -> int:
    """
    Вычисление факториала.
    
    n! = 1 × 2 × ... × n
    
    Сложность: O(n)
    """
    if n < 0:
        raise ValueError("Факториал не определён для отрицательных чисел")
    
    result = 1
    for i in range(2, n + 1):
        result *= i
    
    return result


def factorial_mod(n: int, mod: int) -> int:
    """Факториал по модулю."""
    result = 1
    for i in range(2, n + 1):
        result = (result * i) % mod
    return result


def binomial_coefficient(n: int, k: int) -> int:
    """
    Биномиальный коэффициент C(n, k).
    
    C(n, k) = n! / (k! × (n-k)!)
    
    Количество способов выбрать k элементов из n.
    
    Аргументы:
        n: общее количество
        k: количество для выбора
    
    Возвращает:
        int: C(n, k)
    
    Сложность: O(k)
    
    Пример:
        >>> binomial_coefficient(5, 2)
        10
    """
    if k < 0 or k > n:
        return 0
    if k == 0 or k == n:
        return 1
    
    # Оптимизация: C(n, k) = C(n, n-k)
    k = min(k, n - k)
    
    result = 1
    for i in range(k):
        result = result * (n - i) // (i + 1)
    
    return result


def pascals_triangle(n: int) -> List[List[int]]:
    """
    Треугольник Паскаля.
    
    Каждый элемент равен сумме двух элементов над ним.
    
    Аргументы:
        n: количество строк
    
    Возвращает:
        list: треугольник Паскаля
    
    Сложность: O(n²)
    """
    triangle = []
    
    for i in range(n):
        row = [1] * (i + 1)
        
        for j in range(1, i):
            row[j] = triangle[i - 1][j - 1] + triangle[i - 1][j]
        
        triangle.append(row)
    
    return triangle


def permutations_count(n: int, k: int) -> int:
    """
    Количество размещений A(n, k).
    
    A(n, k) = n! / (n-k)!
    
    Количество способов выбрать и упорядочить k элементов из n.
    """
    if k < 0 or k > n:
        return 0
    
    result = 1
    for i in range(n, n - k, -1):
        result *= i
    
    return result


def catalan_number(n: int) -> int:
    """
    Число Каталана.
    
    Cn = (1/(n+1)) × C(2n, n)
    
    Применения:
    - Количество правильных скобочных последовательностей
    - Количество бинарных деревьев с n узлами
    - Количество путей в сетке, не пересекающих диагональ
    
    Сложность: O(n)
    """
    return binomial_coefficient(2 * n, n) // (n + 1)


# ===== МАТРИЦЫ =====

def matrix_multiply(A: List[List[int]], B: List[List[int]]) -> List[List[int]]:
    """
    Умножение матриц.
    
    Аргументы:
        A: матрица m×n
        B: матрица n×p
    
    Возвращает:
        list: матрица m×p
    
    Сложность: O(m × n × p)
    """
    m, n = len(A), len(A[0])
    n2, p = len(B), len(B[0])
    
    if n != n2:
        raise ValueError("Несовместимые размеры матриц")
    
    result = [[0] * p for _ in range(m)]
    
    for i in range(m):
        for j in range(p):
            for k in range(n):
                result[i][j] += A[i][k] * B[k][j]
    
    return result


def matrix_power(matrix: List[List[int]], exp: int) -> List[List[int]]:
    """
    Быстрое возведение матрицы в степень.
    
    Сложность: O(n³ × log exp)
    """
    n = len(matrix)
    result = [[1 if i == j else 0 for j in range(n)] for i in range(n)]
    
    while exp > 0:
        if exp % 2 == 1:
            result = matrix_multiply(result, matrix)
        matrix = matrix_multiply(matrix, matrix)
        exp //= 2
    
    return result


def fibonacci_matrix(n: int) -> int:
    """
    Числа Фибоначчи через матричное возведение в степень.
    
    [[F(n+1), F(n)  ],     [[1, 1]]^n
     [F(n),   F(n-1)]]  =  
    
    Сложность: O(log n)
    """
    if n <= 1:
        return n
    
    matrix = [[1, 1], [1, 0]]
    result = matrix_power(matrix, n)
    
    return result[0][1]


# ===== ГЕОМЕТРИЯ =====

def gcd_of_coordinates(x: int, y: int) -> int:
    """НОД координат (для задач на решётку)."""
    return gcd_euclidean(abs(x), abs(y))


def lattice_points_on_segment(x1: int, y1: int, x2: int, y2: int) -> int:
    """
    Количество целочисленных точек на отрезке.
    
    Формула: НОД(|x2-x1|, |y2-y1|) + 1
    
    Аргументы:
        x1, y1: координаты первой точки
        x2, y2: координаты второй точки
    
    Возвращает:
        int: количество точек с целыми координатами
    """
    if x1 == x2 and y1 == y2:
        return 1
    
    dx = abs(x2 - x1)
    dy = abs(y2 - y1)
    
    return gcd_euclidean(dx, dy) + 1


def polygon_area(points: List[Tuple[int, int]]) -> int:
    """
    Площадь многоугольника (формула шнурования).
    
    Аргументы:
        points: список координат вершин
    
    Возвращает:
        int: удвоенная площадь (для целых координат)
    
    Сложность: O(n)
    """
    n = len(points)
    area = 0
    
    for i in range(n):
        j = (i + 1) % n
        area += points[i][0] * points[j][1]
        area -= points[j][0] * points[i][1]
    
    return abs(area)


def pick_theorem(area_doubled: int, boundary: int) -> int:
    """
    Теорема Пика.
    
    Для многоугольника с вершинами в целых точках:
    S = I + B/2 - 1
    
    где I — внутренние точки, B — граничные точки.
    
    Аргументы:
        area_doubled: удвоенная площадь
        boundary: количество граничных точек
    
    Возвращает:
        int: количество внутренних точек
    """
    # I = S - B/2 + 1
    # 2I = 2S - B + 2
    return (area_doubled - boundary + 2) // 2


# ===== РАЗНЫЕ АЛГОРИТМЫ =====

def josephus(n: int, k: int) -> int:
    """
    Задача Иосифа Флавия.
    
    n человек стоят в круге, каждый k-й выбывает.
    Определить, кто останется последним.
    
    Аргументы:
        n: количество людей
        k: шаг выбывания
    
    Возвращает:
        int: номер последнего оставшегося (0-indexed)
    
    Сложность: O(n)
    
    Рекуррентная формула:
    J(1, k) = 0
    J(n, k) = (J(n-1, k) + k) mod n
    """
    result = 0
    for i in range(2, n + 1):
        result = (result + k) % i
    return result


def josephus_recursive(n: int, k: int) -> int:
    """Рекурсивная версия."""
    if n == 1:
        return 0
    return (josephus_recursive(n - 1, k) + k) % n


def josephus_power_of_two(n: int) -> int:
    """
    Задача Иосифа для k=2.
    
    Для k=2 есть формула: J(n, 2) = 2L, где L = n - 2^⌊log₂n⌋
    
    Сложность: O(log n)
    """
    # Находим старший бит
    highest_power = 1
    while highest_power * 2 <= n:
        highest_power *= 2
    
    return 2 * (n - highest_power)


def gray_code(n: int) -> List[int]:
    """
    Генерация кода Грея.
    
    Код Грея — последовательность, где соседние числа отличаются одним битом.
    
    Аргументы:
        n: количество бит
    
    Возвращает:
        list: коды Грея от 0 до 2^n - 1
    
    Рекуррентная формула:
    G(n) = G(n-1) + reverse(G(n-1)) с добавленным старшим битом
    
    Пример:
        >>> gray_code(2)
        [0, 1, 3, 2]  # 00, 01, 11, 10
    """
    if n == 0:
        return [0]
    
    result = [0, 1]
    
    for i in range(1, n):
        # Добавляем старший бит к перевёрнутой части
        result = result + [x + (1 << i) for x in reversed(result)]
    
    return result


def gray_code_to_binary(gray: int) -> int:
    """Преобразование кода Грея в двоичное число."""
    binary = gray
    mask = gray >> 1
    
    while mask:
        binary ^= mask
        mask >>= 1
    
    return binary


def binary_to_gray(binary: int) -> int:
    """Преобразование двоичного числа в код Грея."""
    return binary ^ (binary >> 1)


def trailing_zeros(n: int) -> int:
    """
    Количество нулей в конце n!.
    
    Каждый ноль появляется от множителя 10 = 2 × 5.
    Поскольку двоек больше, считаем пятёрки.
    
    Формула: sum(⌊n/5^i⌋) для i = 1, 2, ...
    
    Аргументы:
        n: число
    
    Возвращает:
        int: количество нулей в конце n!
    
    Сложность: O(log n)
    """
    count = 0
    power = 5
    
    while power <= n:
        count += n // power
        power *= 5
    
    return count


def count_digits(n: int) -> int:
    """Количество цифр в числе."""
    if n == 0:
        return 1
    count = 0
    n = abs(n)
    while n:
        count += 1
        n //= 10
    return count


def sum_of_digits(n: int) -> int:
    """Сумма цифр числа."""
    total = 0
    n = abs(n)
    while n:
        total += n % 10
        n //= 10
    return total


def reverse_number(n: int) -> int:
    """Разворот числа."""
    result = 0
    sign = 1 if n >= 0 else -1
    n = abs(n)
    
    while n:
        result = result * 10 + n % 10
        n //= 10
    
    return result * sign


def is_armstrong(n: int) -> bool:
    """
    Проверка числа Армстронга.
    
    Число равно сумме своих цифр, возведённых в степень количества цифр.
    """
    if n < 0:
        return False
    
    digits = []
    temp = n
    while temp:
        digits.append(temp % 10)
        temp //= 10
    
    k = len(digits)
    return sum(d ** k for d in digits) == n


def is_perfect(n: int) -> bool:
    """
    Проверка совершенного числа.
    
    Совершенное число равно сумме своих делителей (кроме себя).
    """
    if n < 2:
        return False
    
    return sum_divisors(n) - n == n


def collatz_steps(n: int) -> int:
    """
    Количество шагов до 1 в последовательности Коллатца.
    
    Правила:
    - Если n чётное: n = n / 2
    - Если n нечётное: n = 3n + 1
    
    Гипотеза: для любого n последовательность достигнет 1.
    """
    steps = 0
    
    while n != 1:
        if n % 2 == 0:
            n //= 2
        else:
            n = 3 * n + 1
        steps += 1
    
    return steps


# ===== МОДУЛЬНАЯ АРИФМЕТИКА =====

def chinese_remainder_theorem(remainders: List[int], moduli: List[int]) -> int:
    """
    Китайская теорема об остатках.
    
    Находит x такое, что:
    x ≡ r1 (mod m1)
    x ≡ r2 (mod m2)
    ...
    
    Требуется, чтобы все mi были попарно взаимно просты.
    
    Аргументы:
        remainders: остатки [r1, r2, ...]
        moduli: модули [m1, m2, ...]
    
    Возвращает:
        int: наименьшее положительное решение
    
    Сложность: O(n × log M), M = ∏mi
    """
    # Произведение всех модулей
    M = 1
    for m in moduli:
        M *= m
    
    result = 0
    
    for ri, mi in zip(remainders, moduli):
        Mi = M // mi
        yi = mod_inverse(Mi, mi)
        result += ri * Mi * yi
    
    return result % M


if __name__ == "__main__":
    print(__doc__)
    print("\n" + "="*60)
    
    # Простые числа
    print("Простые числа:")
    print(f"  is_prime(17): {is_prime_optimized(17)}")
    print(f"  is_prime(18): {is_prime_optimized(18)}")
    print(f"  Простые до 30: {sieve_of_eratosthenes(30)}")
    
    # НОД и НОК
    print("\nНОД и НОК:")
    print(f"  НОД(48, 18): {gcd_euclidean(48, 18)}")
    print(f"  НОК(12, 18): {lcm(12, 18)}")
    
    # Расширенный Евклид
    g, x, y = extended_gcd(35, 15)
    print(f"  35×{x} + 15×{y} = {g}")
    
    # Обратное по модулю
    print(f"  Обратное к 3 mod 7: {mod_inverse(3, 7)}")
    
    # Разложение на множители
    print("\nРазложение на множители:")
    print(f"  360 = {prime_factors(360)}")
    print(f"  Количество делителей 360: {count_divisors(360)}")
    print(f"  φ(12) = {euler_phi(12)}")
    
    # Быстрое возведение в степень
    print("\nБыстрое возведение в степень:")
    print(f"  2^10 = {power_binary(2, 10)}")
    print(f"  2^100 mod 1000 = {power_mod(2, 100, 1000)}")
    
    # Комбинаторика
    print("\nКомбинаторика:")
    print(f"  C(5, 2) = {binomial_coefficient(5, 2)}")
    print(f"  5! = {factorial(5)}")
    print(f"  Число Каталана C4 = {catalan_number(4)}")
    
    # Фибоначчи матрицей
    print("\nФибоначчи матрицей:")
    print(f"  F(50) = {fibonacci_matrix(50)}")
    
    # Задача Иосифа
    print("\nЗадача Иосифа:")
    print(f"  n=7, k=3: последний = {josephus(7, 3)}")
    
    # Код Грея
    print("\nКод Грея для 3 бит:")
    print(f"  {gray_code(3)}")
    
    # Нули в конце факториала
    print("\nНули в конце 100!:")
    print(f"  {trailing_zeros(100)}")
    
    # Китайская теорема
    print("\nКитайская теорема об остатках:")
    print(f"  x ≡ 2 (mod 3), x ≡ 3 (mod 5), x ≡ 2 (mod 7)")
    print(f"  x = {chinese_remainder_theorem([2, 3, 2], [3, 5, 7])}")
