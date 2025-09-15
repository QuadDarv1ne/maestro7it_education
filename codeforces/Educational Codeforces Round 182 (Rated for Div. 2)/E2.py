'''
https://codeforces.com/contest/2144/problem/E2
'''

MOD = 998244353

def get_LR_positions(a):
    """
    Определяет позиции левых и правых максимумов в последовательности.
    
    Args:
        a: список целых чисел - исходная последовательность
        
    Returns:
        L: список кортежей (значение, позиция) для левых максимумов
        R: список кортежей (значение, позиция) для правых максимумов
    """
    n = len(a)
    L = []  # список (value, index) для левых максимумов
    cur_max = -1
    for i in range(n):
        if a[i] > cur_max:
            cur_max = a[i]
            L.append((a[i], i))
    
    R = []  # список (value, index) для правых максимумов
    cur_max = -1
    for i in range(n-1, -1, -1):
        if a[i] > cur_max:
            cur_max = a[i]
            R.append((a[i], i))
    R.reverse()  # разворачиваем, чтобы порядок был слева направо
    
    return L, R

def count_left_ways(a, L, pos_max, MOD):
    """
    Подсчитывает количество допустимых подпоследовательностей для левой части.
    
    Args:
        a: исходная последовательность
        L: список левых максимумов с позициями
        pos_max: позиция текущего максимального элемента
        MOD: модуль для вычислений
        
    Returns:
        Количество допустимых подпоследовательностей для левой части
    """
    # Формируем L_left - все левые максимумы до pos_max
    L_left = []
    for val, idx in L:
        if idx < pos_max:
            L_left.append((val, idx))
        else:
            break
    
    m = len(L_left)
    if m == 0:
        return 1
    
    # Для каждого элемента в L_left находим допустимые позиции
    positions = []
    for i in range(m):
        val, orig_idx = L_left[i]
        # Определяем границы поиска
        left_bound = -1
        if i > 0:
            left_bound = L_left[i-1][1]
        right_bound = pos_max
        if i < m-1:
            right_bound = L_left[i+1][1]
        
        # Собираем все позиции в заданном диапазоне с нужным значением
        pos_list = []
        for p in range(left_bound+1, right_bound):
            if a[p] == val:
                pos_list.append(p)
        positions.append(pos_list)
    
    # Если для какого-то элемента нет допустимых позиций, возвращаем 0
    for pos_list in positions:
        if len(pos_list) == 0:
            return 0
    
    # Динамическое программирование для подсчета количества способов
    dp = []
    
    # Инициализация для первого элемента L_left
    next_pos = pos_max
    if m > 1:
        next_pos = L_left[1][1]
    dp0 = []
    for p in positions[0]:
        count = next_pos - p - 1
        ways = pow(2, count, MOD)
        dp0.append(ways)
    dp.append(dp0)
    
    # Обработка остальных элементов L_left
    for i in range(1, m):
        next_pos = pos_max
        if i < m-1:
            next_pos = L_left[i+1][1]
        
        dpi = [0] * len(positions[i])
        for j in range(len(positions[i])):
            p_j = positions[i][j]
            for k in range(len(positions[i-1])):
                p_k = positions[i-1][k]
                if p_k < p_j:
                    count = p_j - p_k - 1
                    ways = pow(2, count, MOD)
                    dpi[j] = (dpi[j] + dp[i-1][k] * ways) % MOD
        dp.append(dpi)
    
    return sum(dp[-1]) % MOD

def count_right_ways(a, R, pos_max, MOD):
    """
    Подсчитывает количество допустимых подпоследовательностей для правой части.
    
    Args:
        a: исходная последовательность
        R: список правых максимумов с позициями
        pos_max: позиция текущего максимального элемента
        MOD: модуль для вычислений
        
    Returns:
        Количество допустимых подпоследовательностей для правой части
    """
    # Формируем R_right - все правые максимумы после pos_max
    R_right = []
    for val, idx in R:
        if idx > pos_max:
            R_right.append((val, idx))
        else:
            break
    
    m = len(R_right)
    if m == 0:
        return 1
    
    # Для каждого элемента в R_right находим допустимые позиции
    positions = []
    for i in range(m):
        val, orig_idx = R_right[i]
        # Определяем границы поиска
        left_bound = pos_max
        if i > 0:
            left_bound = R_right[i-1][1]
        right_bound = len(a)
        if i < m-1:
            right_bound = R_right[i+1][1]
        
        # Собираем все позиции в заданном диапазоне с нужным значением
        pos_list = []
        for p in range(left_bound+1, right_bound):
            if a[p] == val:
                pos_list.append(p)
        positions.append(pos_list)
    
    # Если для какого-то элемента нет допустимых позиций, возвращаем 0
    for pos_list in positions:
        if len(pos_list) == 0:
            return 0
    
    # Динамическое программирование для подсчета количества способов
    dp = []
    
    # Инициализация для первого элемента R_right
    dp0 = []
    for p in positions[0]:
        count = p - pos_max - 1
        ways = pow(2, count, MOD)
        dp0.append(ways)
    dp.append(dp0)
    
    # Обработка остальных элементов R_right
    for i in range(1, m):
        dpi = [0] * len(positions[i])
        for j in range(len(positions[i])):
            p_j = positions[i][j]
            for k in range(len(positions[i-1])):
                p_k = positions[i-1][k]
                if p_k < p_j:
                    count = p_j - p_k - 1
                    ways = pow(2, count, MOD)
                    dpi[j] = (dpi[j] + dp[i-1][k] * ways) % MOD
        dp.append(dpi)
    
    return sum(dp[-1]) % MOD

def solve():
    """
    Решение задачи E2: Смотрим на башни (сложная версия)
    
    Задача:
    Эта задача идентична E1, но с более строгими ограничениями:
    - 1 ≤ t ≤ 500
    - 1 ≤ n ≤ 10^5
    - Сумма n по всем тестам ≤ 10^5
    
    Решение использует оптимизированный алгоритм с предподсчетом
    и более эффективной обработкой данных.
    
    Входные данные и выходные данные аналогичны E1.
    """
    n = int(input().strip())
    a = list(map(int, input().split()))
    
    # Получаем левые и правые максимумы с позициями
    L, R = get_LR_positions(a)
    
    # Находим максимальное значение и все его позиции
    max_val = L[-1][0]
    max_positions = [idx for val, idx in L if val == max_val]
    
    total = 0
    for pos_max in max_positions:
        left_ways = count_left_ways(a, L, pos_max, MOD)
        right_ways = count_right_ways(a, R, pos_max, MOD)
        total = (total + left_ways * right_ways) % MOD
    
    print(total)

t = int(input().strip())
for _ in range(t):
    solve()

''' Полезные ссылки: '''
# 1. Telegram ❃ Хижина программиста Æ: https://t.me/hut_programmer_07
# 2. Telegram №1 @quadd4rv1n7
# 3. Telegram №2 @dupley_maxim_1999
# 4. Rutube канал: https://rutube.ru/channel/4218729/
# 5. Plvideo канал: https://plvideo.ru/channel/AUPv_p1r5AQJ
# 6. YouTube канал: https://www.youtube.com/@it-coders
# 7. ВК группа: https://vk.com/science_geeks