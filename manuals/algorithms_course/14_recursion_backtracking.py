"""
РЕКУРСИЯ И ОБРАТНЫЙ ПРОХОД (RECURSION AND BACKTRACKING)

Рекурсия — это метод программирования, при котором функция вызывает сама себя.
Backtracking (обратный проход) — это метод перебора всех возможных вариантов
решения с возможностью вернуться назад при неудаче.

Основные концепции рекурсии:
1. Базовый случай — условие выхода из рекурсии
2. Рекурсивный случай — сведение задачи к более простой
3. Глубина рекурсии — количество вложенных вызовов

Backtracking применяется для:
- Генерации всех перестановок и сочетаний
- Решения судоку и других головоломок
- Задачи о ферзях (N-Queens)
- Поиска пути в лабиринте
- Подмножеств и разбиений

Временная сложность обычно O(n!) или O(2^n) — полный перебор.
Важно: правильно определять базовый случай и условия отсечения!
"""

from typing import List


# ===== БАЗОВАЯ РЕКУРСИЯ =====

def factorial(n: int) -> int:
    """
    Вычисление факториала рекурсивно.
    
    Классический пример рекурсии.
    n! = n × (n-1)!
    0! = 1 (базовый случай)
    
    Аргументы:
        n: неотрицательное целое число
    
    Возвращает:
        int: n!
    
    Сложность: O(n) по времени, O(n) по памяти (стек вызовов)
    
    Пример:
        >>> factorial(5)
        120
    """
    # Базовый случай
    if n <= 1:
        return 1
    # Рекурсивный случай
    return n * factorial(n - 1)


def fibonacci(n: int) -> int:
    """
    Числа Фибоначчи через рекурсию.
    
    ВНИМАНИЕ: Экспоненциальная сложность!
    Показывает проблему повторных вычислений.
    Для практики используйте мемоизацию или итеративный подход.
    
    F(n) = F(n-1) + F(n-2)
    F(0) = 0, F(1) = 1
    
    Сложность: O(2^n) — катастрофически медленно
    """
    if n <= 1:
        return n
    return fibonacci(n - 1) + fibonacci(n - 2)


def fibonacci_memo(n: int, memo: dict = None) -> int:
    """
    Числа Фибоначчи с мемоизацией.
    
    Кэширование результатов устраняет повторные вычисления.
    
    Сложность: O(n) по времени, O(n) по памяти
    
    Пример:
        >>> fibonacci_memo(50)
        12586269025
    """
    if memo is None:
        memo = {}
    
    if n in memo:
        return memo[n]
    
    if n <= 1:
        return n
    
    memo[n] = fibonacci_memo(n - 1, memo) + fibonacci_memo(n - 2, memo)
    return memo[n]


def sum_array(arr: List[int]) -> int:
    """
    Сумма элементов массива рекурсивно.
    
    Демонстрирует рекурсивную обработку списков.
    
    Аргументы:
        arr: список чисел
    
    Возвращает:
        int: сумма всех элементов
    
    Сложность: O(n)
    
    Пример:
        >>> sum_array([1, 2, 3, 4, 5])
        15
    """
    # Базовый случай: пустой список
    if not arr:
        return 0
    # Рекурсивный случай: первый элемент + сумма остальных
    return arr[0] + sum_array(arr[1:])


def reverse_string(s: str) -> str:
    """
    Разворот строки рекурсивно.
    
    Аргументы:
        s: строка
    
    Возвращает:
        str: перевёрнутая строка
    
    Сложность: O(n²) из-за конкатенации строк
    
    Пример:
        >>> reverse_string("hello")
        'olleh'
    """
    if len(s) <= 1:
        return s
    return reverse_string(s[1:]) + s[0]


# ===== BACKTRACKING: ГЕНЕРАЦИЯ КОМБИНАЦИЙ =====

def generate_permutations(nums: List[int]) -> List[List[int]]:
    """
    Генерация всех перестановок массива.
    
    Backtracking: для каждой позиции пробуем все неиспользованные элементы.
    
    Аргументы:
        nums: список уникальных элементов
    
    Возвращает:
        list: все перестановки
    
    Сложность: O(n! × n) — n! перестановок, каждая длины n
    
    Пример:
        >>> generate_permutations([1, 2, 3])
        [[1, 2, 3], [1, 3, 2], [2, 1, 3], [2, 3, 1], [3, 1, 2], [3, 2, 1]]
    """
    result = []
    
    def backtrack(current: List[int], remaining: List[int]):
        """
        Рекурсивная функция построения перестановок.
        
        Аргументы:
            current: текущая строящаяся перестановка
            remaining: ещё не использованные элементы
        """
        # Базовый случай: все элементы использованы
        if not remaining:
            result.append(current[:])  # Копируем!
            return
        
        # Пробуем каждый оставшийся элемент
        for i in range(len(remaining)):
            # Добавляем элемент к текущей перестановке
            current.append(remaining[i])
            # Рекурсивно строим дальше
            backtrack(current, remaining[:i] + remaining[i+1:])
            # BACKTRACK: убираем элемент, пробуем следующий
            current.pop()
    
    backtrack([], nums)
    return result


def generate_permutations_swap(nums: List[int]) -> List[List[int]]:
    """
    Генерация перестановок обменом элементов.
    
    Оптимизированная версия без создания новых списков.
    Меняем элементы местами in-place.
    
    Сложность: O(n! × n)
    """
    result = []
    n = len(nums)
    
    def backtrack(start: int):
        """
        Генерация перестановок начиная с позиции start.
        """
        # Базовый случай: достигли конца массива
        if start == n:
            result.append(nums[:])  # Копируем текущее состояние
            return
        
        # Пробуем каждый элемент на позиции start
        for i in range(start, n):
            # Ставим элемент i на позицию start
            nums[start], nums[i] = nums[i], nums[start]
            # Рекурсивно генерируем перестановки для остальных позиций
            backtrack(start + 1)
            # BACKTRACK: возвращаем элементы на места
            nums[start], nums[i] = nums[i], nums[start]
    
    backtrack(0)
    return result


def generate_combinations(nums: List[int], k: int) -> List[List[int]]:
    """
    Генерация всех сочетаний из n элементов по k.
    
    Порядок элементов в сочетании не важен.
    C(n, k) = n! / (k! × (n-k)!)
    
    Аргументы:
        nums: список элементов
        k: размер каждого сочетания
    
    Возвращает:
        list: все сочетания размера k
    
    Сложность: O(C(n, k) × k)
    
    Пример:
        >>> generate_combinations([1, 2, 3, 4], 2)
        [[1, 2], [1, 3], [1, 4], [2, 3], [2, 4], [3, 4]]
    """
    result = []
    n = len(nums)
    
    def backtrack(start: int, current: List[int]):
        """
        Построение сочетаний.
        
        Аргументы:
            start: индекс, с которого начинать выбор
            current: текущее сочетание
        """
        # Базовый случай: набрали нужное количество
        if len(current) == k:
            result.append(current[:])
            return
        
        # Пробуем каждый элемент от start до конца
        for i in range(start, n):
            current.append(nums[i])
            # Рекурсивно выбираем следующие элементы
            backtrack(i + 1, current)
            # BACKTRACK
            current.pop()
    
    backtrack(0, [])
    return result


def generate_subsets(nums: List[int]) -> List[List[int]]:
    """
    Генерация всех подмножеств (power set).
    
    Каждое подмножество — это уникальная комбинация элементов.
    Всего 2^n подмножеств.
    
    Аргументы:
        nums: список элементов
    
    Возвращает:
        list: все подмножества
    
    Сложность: O(2^n × n)
    
    Пример:
        >>> generate_subsets([1, 2, 3])
        [[], [1], [1, 2], [1, 2, 3], [1, 3], [2], [2, 3], [3]]
    """
    result = []
    n = len(nums)
    
    def backtrack(start: int, current: List[int]):
        """
        Построение подмножеств.
        """
        # Добавляем текущее подмножество
        result.append(current[:])
        
        # Пробуем добавить каждый следующий элемент
        for i in range(start, n):
            current.append(nums[i])
            backtrack(i + 1, current)
            # BACKTRACK
            current.pop()
    
    backtrack(0, [])
    return result


# ===== ЗАДАЧА О ФЕРЗЯХ =====

def solve_n_queens(n: int) -> List[List[str]]:
    """
    Задача о N ферзях.
    
    Расставить N ферзей на доске N×N так, чтобы они не били друг друга.
    Ферзь бьёт по горизонтали, вертикали и диагоналям.
    
    Аргументы:
        n: размер доски и количество ферзей
    
    Возвращает:
        list: все возможные расстановки (каждая — список строк)
    
    Сложность: O(N!) в худшем случае
    
    Пример:
        >>> solve_n_queens(4)
        [['.Q..', '...Q', 'Q...', '..Q.'],
         ['..Q.', 'Q...', '...Q', '.Q..']]
    """
    result = []
    
    def is_safe(board: List[int], row: int, col: int) -> bool:
        """
        Проверка, можно ли поставить ферзя в (row, col).
        
        Аргументы:
            board: board[i] = колонка ферзя в строке i
            row: строка для проверки
            col: колонка для проверки
        
        Возвращает:
            bool: True если позиция безопасна
        """
        for prev_row in range(row):
            prev_col = board[prev_row]
            
            # Проверка вертикали
            if prev_col == col:
                return False
            
            # Проверка диагоналей
            # Разница строк == разнице колонок -> одна диагональ
            if abs(prev_row - row) == abs(prev_col - col):
                return False
        
        return True
    
    def backtrack(row: int, board: List[int]):
        """
        Расстановка ферзей по строкам.
        
        Аргументы:
            row: текущая строка
            board: текущая расстановка
        """
        # Базовый случай: все ферзи расставлены
        if row == n:
            # Формируем визуализацию доски
            solution = []
            for col in board:
                row_str = '.' * col + 'Q' + '.' * (n - col - 1)
                solution.append(row_str)
            result.append(solution)
            return
        
        # Пробуем поставить ферзя в каждую колонку
        for col in range(n):
            if is_safe(board, row, col):
                board[row] = col
                backtrack(row + 1, board)
                # BACKTRACK: board[row] перезапишется в следующей итерации
    
    backtrack(0, [0] * n)
    return result


def total_n_queens(n: int) -> int:
    """
    Подсчёт количества решений задачи о N ферзях.
    
    Оптимизированная версия с битовым представлением.
    
    Аргументы:
        n: размер доски
    
    Возвращает:
        int: количество решений
    
    Сложность: O(N!)
    """
    count = 0
    
    def backtrack(row: int, cols: int, diag1: int, diag2: int):
        """
        Рекурсивная расстановка с битовыми масками.
        
        Аргументы:
            row: текущая строка
            cols: биты занятых колонок
            diag1: биты занятых диагоналей (row - col)
            diag2: биты занятых диагоналей (row + col)
        """
        nonlocal count
        
        if row == n:
            count += 1
            return
        
        # Доступные позиции: не заняты колонки и диагонали
        available = ((1 << n) - 1) & ~(cols | diag1 | diag2)
        
        while available:
            # Берём правую доступную позицию
            pos = available & -available
            available -= pos
            
            # Рекурсивно идём дальше
            # diag1 сдвигается вправо, diag2 — влево
            backtrack(row + 1, cols | pos, (diag1 | pos) >> 1, (diag2 | pos) << 1)
    
    backtrack(0, 0, 0, 0)
    return count


# ===== СУДОКУ =====

def solve_sudoku(board: List[List[str]]) -> bool:
    """
    Решение судоку методом backtracking.
    
    Доска 9×9, клетки могут содержать цифры 1-9 или быть пустыми ('.').
    Правила: каждая строка, столбец и блок 3×3 содержат все цифры 1-9.
    
    Аргументы:
        board: матрица 9×9 (изменяется in-place)
    
    Возвращает:
        bool: True если решение найдено
    
    Сложность: O(9^(n*n)) в худшем случае, но на практике быстрее
    """
    def is_valid(row: int, col: int, num: str) -> bool:
        """
        Проверка возможности поставить num в (row, col).
        """
        # Проверка строки
        if num in board[row]:
            return False
        
        # Проверка столбца
        for r in range(9):
            if board[r][col] == num:
                return False
        
        # Проверка блока 3×3
        block_row, block_col = 3 * (row // 3), 3 * (col // 3)
        for r in range(block_row, block_row + 3):
            for c in range(block_col, block_col + 3):
                if board[r][c] == num:
                    return False
        
        return True
    
    def find_empty() -> tuple:
        """Найти пустую клетку."""
        for r in range(9):
            for c in range(9):
                if board[r][c] == '.':
                    return (r, c)
        return None
    
    def solve() -> bool:
        """
        Рекурсивное решение судоку.
        """
        empty = find_empty()
        
        # Базовый случай: нет пустых клеток — решено
        if empty is None:
            return True
        
        row, col = empty
        
        # Пробуем каждую цифру
        for num in '123456789':
            if is_valid(row, col, num):
                board[row][col] = num
                
                if solve():
                    return True
                
                # BACKTRACK
                board[row][col] = '.'
        
        return False
    
    return solve()


# ===== ПОИСК ПУТИ В ЛАБИРИНТЕ =====

def find_path_maze(maze: List[List[int]], start: tuple, end: tuple) -> List[tuple]:
    """
    Поиск пути в лабиринте методом backtracking.
    
    Лабиринт — матрица, где 0 = свободно, 1 = стена.
    
    Аргументы:
        maze: матрица лабиринта
        start: начальная позиция (row, col)
        end: конечная позиция (row, col)
    
    Возвращает:
        list: путь от start до end или пустой список
    
    Сложность: O(4^(n×m)) в худшем случае
    """
    if not maze or not maze[0]:
        return []
    
    rows, cols = len(maze), len(maze[0])
    path = []
    visited = set()
    
    # Направления: вверх, вниз, влево, вправо
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    
    def is_valid(row: int, col: int) -> bool:
        """Проверка корректности позиции."""
        return (0 <= row < rows and 
                0 <= col < cols and 
                maze[row][col] == 0 and 
                (row, col) not in visited)
    
    def backtrack(row: int, col: int) -> bool:
        """
        Поиск пути из текущей позиции.
        
        Возвращает:
            bool: True если путь найден
        """
        # Базовый случай: достигли цели
        if (row, col) == end:
            path.append((row, col))
            return True
        
        # Проверяем возможность нахождения здесь
        if not is_valid(row, col):
            return False
        
        # Отмечаем посещение
        visited.add((row, col))
        path.append((row, col))
        
        # Пробуем все направления
        for dr, dc in directions:
            new_row, new_col = row + dr, col + dc
            if backtrack(new_row, new_col):
                return True
        
        # BACKTRACK: возвращаемся назад
        path.pop()
        visited.remove((row, col))
        return False
    
    if backtrack(start[0], start[1]):
        return path
    return []


# ===== РАЗБИЕНИЕ СТРОКИ =====

def partition_palindrome(s: str) -> List[List[str]]:
    """
    Разбиение строки на палиндромы.
    
    Найти все возможные разбиения строки, где каждая часть — палиндром.
    
    Аргументы:
        s: строка
    
    Возвращает:
        list: все разбиения на палиндромы
    
    Сложность: O(n × 2^n)
    
    Пример:
        >>> partition_palindrome("aab")
        [['a', 'a', 'b'], ['aa', 'b']]
    """
    result = []
    n = len(s)
    
    def is_palindrome(sub: str) -> bool:
        """Проверка палиндрома."""
        return sub == sub[::-1]
    
    def backtrack(start: int, current: List[str]):
        """
        Построение разбиений.
        
        Аргументы:
            start: индекс начала текущего куска
            current: текущее разбиение
        """
        # Базовый случай: дошли до конца строки
        if start == n:
            result.append(current[:])
            return
        
        # Пробуем все возможные концы текущего куска
        for end in range(start + 1, n + 1):
            substring = s[start:end]
            
            if is_palindrome(substring):
                current.append(substring)
                backtrack(end, current)
                # BACKTRACK
                current.pop()
    
    backtrack(0, [])
    return result


# ===== СУММА ПОДМНОЖЕСТВ =====

def combination_sum(candidates: List[int], target: int) -> List[List[int]]:
    """
    Найти все комбинации чисел, дающие заданную сумму.
    
    Каждое число можно использовать неограниченное количество раз.
    
    Аргументы:
        candidates: список положительных чисел
        target: целевая сумма
    
    Возвращает:
        list: все комбинации, дающие target
    
    Сложность: O(2^(target/min)) в худшем случае
    
    Пример:
        >>> combination_sum([2, 3, 6, 7], 7)
        [[2, 2, 3], [7]]
    """
    result = []
    n = len(candidates)
    
    def backtrack(start: int, remaining: int, current: List[int]):
        """
        Построение комбинаций.
        
        Аргументы:
            start: индекс, с которого можно брать числа (избегаем дубликатов)
            remaining: оставшаяся сумма
            current: текущая комбинация
        """
        # Базовый случай: сумма набрана
        if remaining == 0:
            result.append(current[:])
            return
        
        # Превысили сумму — отсечение
        if remaining < 0:
            return
        
        # Пробуем каждое число от start
        for i in range(start, n):
            num = candidates[i]
            current.append(num)
            # Можно использовать то же число снова
            backtrack(i, remaining - num, current)
            # BACKTRACK
            current.pop()
    
    backtrack(0, target, [])
    return result


def combination_sum_2(candidates: List[int], target: int) -> List[List[int]]:
    """
    Найти комбинации чисел, дающие сумму.
    
    Каждое число можно использовать только один раз.
    Могут быть дубликаты в candidates, но результат должен быть уникальным.
    
    Сложность: O(2^n)
    
    Пример:
        >>> combination_sum_2([10, 1, 2, 7, 6, 1, 5], 8)
        [[1, 1, 6], [1, 2, 5], [1, 7], [2, 6]]
    """
    result = []
    candidates.sort()  # Сортировка для обработки дубликатов
    n = len(candidates)
    
    def backtrack(start: int, remaining: int, current: List[int]):
        if remaining == 0:
            result.append(current[:])
            return
        
        if remaining < 0:
            return
        
        for i in range(start, n):
            # Пропускаем дубликаты
            if i > start and candidates[i] == candidates[i - 1]:
                continue
            
            current.append(candidates[i])
            # i + 1 — каждое число используется один раз
            backtrack(i + 1, remaining - candidates[i], current)
            current.pop()
    
    backtrack(0, target, [])
    return result


# ===== ГЕНЕРАЦИЯ СКОБОК =====

def generate_parentheses(n: int) -> List[str]:
    """
    Генерация всех правильных скобочных последовательностей.
    
    Дано n пар скобок. Сгенерировать все правильные комбинации.
    Правильная: каждой открывающей соответствует закрывающая.
    
    Аргументы:
        n: количество пар скобок
    
    Возвращает:
        list: все правильные последовательности
    
    Сложность: O(4^n / sqrt(n)) — каталаново число
    
    Пример:
        >>> generate_parentheses(3)
        ['((()))', '(()())', '(())()', '()(())', '()()()']
    """
    result = []
    
    def backtrack(current: str, open_count: int, close_count: int):
        """
        Построение последовательности.
        
        Аргументы:
            current: текущая строка
            open_count: использовано открывающих скобок
            close_count: использовано закрывающих скобок
        """
        # Базовый случай: все скобки использованы
        if open_count == n and close_count == n:
            result.append(current)
            return
        
        # Можно добавить открывающую, если ещё есть
        if open_count < n:
            backtrack(current + '(', open_count + 1, close_count)
        
        # Можно добавить закрывающую, если открывающих больше
        if close_count < open_count:
            backtrack(current + ')', open_count, close_count + 1)
    
    backtrack('', 0, 0)
    return result


# ===== ВОССТАНОВЛЕНИЕ IP-АДРЕСА =====

def restore_ip_addresses(s: str) -> List[str]:
    """
    Восстановление IP-адресов из строки.
    
    Строка состоит только из цифр. Разбить на 4 части (октеты).
    Каждый октет: 0-255, без ведущих нулей (кроме самого 0).
    
    Аргументы:
        s: строка цифр
    
    Возвращает:
        list: все возможные IP-адреса
    
    Сложность: O(1) — максимум 3^3 вариантов
    
    Пример:
        >>> restore_ip_addresses("25525511135")
        ['255.255.11.135', '255.255.111.35']
    """
    result = []
    n = len(s)
    
    # IP-адрес: от 4 до 12 цифр
    if n < 4 or n > 12:
        return result
    
    def is_valid_octet(octet: str) -> bool:
        """Проверка корректности октета."""
        if not octet:
            return False
        # Ведущий ноль разрешён только для "0"
        if len(octet) > 1 and octet[0] == '0':
            return False
        # Значение 0-255
        return 0 <= int(octet) <= 255
    
    def backtrack(start: int, parts: List[str]):
        """
        Построение IP-адреса.
        
        Аргументы:
            start: текущая позиция в строке
            parts: уже сформированные октеты
        """
        # Базовый случай: 4 части и вся строка использована
        if len(parts) == 4:
            if start == n:
                result.append('.'.join(parts))
            return
        
        # Пробуем октеты длины 1, 2, 3
        for length in range(1, 4):
            if start + length > n:
                break
            
            octet = s[start:start + length]
            
            if is_valid_octet(octet):
                parts.append(octet)
                backtrack(start + length, parts)
                parts.pop()
    
    backtrack(0, [])
    return result


# ===== TELEGRAM: БУКВЫ ТЕЛЕФОННОЙ КЛАВИАТУРЫ =====

def letter_combinations(digits: str) -> List[str]:
    """
    Генерация комбинаций букв телефонной клавиатуры.
    
    2 -> abc, 3 -> def, 4 -> ghi, 5 -> jkl,
    6 -> mno, 7 -> pqrs, 8 -> tuv, 9 -> wxyz
    
    Аргументы:
        digits: строка цифр от 2 до 9
    
    Возвращает:
        list: все возможные комбинации букв
    
    Сложность: O(4^n) — максимум 4 буквы на цифру
    
    Пример:
        >>> letter_combinations("23")
        ['ad', 'ae', 'af', 'bd', 'be', 'bf', 'cd', 'ce', 'cf']
    """
    if not digits:
        return []
    
    mapping = {
        '2': 'abc', '3': 'def', '4': 'ghi', '5': 'jkl',
        '6': 'mno', '7': 'pqrs', '8': 'tuv', '9': 'wxyz'
    }
    
    result = []
    
    def backtrack(index: int, current: str):
        """
        Построение комбинаций.
        
        Аргументы:
            index: текущая позиция в digits
            current: текущая строка
        """
        # Базовый случай: обработали все цифры
        if index == len(digits):
            result.append(current)
            return
        
        # Пробуем каждую букву для текущей цифры
        for letter in mapping[digits[index]]:
            backtrack(index + 1, current + letter)
    
    backtrack(0, '')
    return result


if __name__ == "__main__":
    print(__doc__)
    print("\n" + "="*60)
    
    # Базовая рекурсия
    print("Базовая рекурсия:")
    print(f"  factorial(5) = {factorial(5)}")
    print(f"  fibonacci_memo(40) = {fibonacci_memo(40)}")
    print(f"  sum_array([1,2,3,4,5]) = {sum_array([1,2,3,4,5])}")
    
    # Перестановки и сочетания
    print("\nПерестановки [1, 2, 3]:")
    perms = generate_permutations([1, 2, 3])
    print(f"  Количество: {len(perms)}")
    print(f"  {perms}")
    
    print("\nСочетания [1,2,3,4] по 2:")
    print(f"  {generate_combinations([1, 2, 3, 4], 2)}")
    
    print("\nПодмножества [1, 2]:")
    print(f"  {generate_subsets([1, 2])}")
    
    # N ферзей
    print("\nЗадача о 4 ферзях:")
    solutions = solve_n_queens(4)
    print(f"  Количество решений: {len(solutions)}")
    for sol in solutions[:2]:
        print(f"  {sol}")
    
    print(f"\nКоличество решений для 8 ферзей: {total_n_queens(8)}")
    
    # Скобки
    print("\nПравильные скобки для n=3:")
    print(f"  {generate_parentheses(3)}")
    
    # Телефонная клавиатура
    print("\nБуквы для '23':")
    print(f"  {letter_combinations('23')}")
    
    # Разбиение на палиндромы
    print("\nРазбиение 'aab' на палиндромы:")
    print(f"  {partition_palindrome('aab')}")
    
    # Сумма комбинаций
    print("\nКомбинации суммы 7 из [2,3,6,7]:")
    print(f"  {combination_sum([2, 3, 6, 7], 7)}")
