'''
https://codeforces.com/contest/2144/problem/F
'''

MOD = 998244353

def is_valid_subsequence(s):
    """
    Проверяет, может ли скобочная последовательность быть подпоследовательностью
    некоторой правильной скобочной последовательности.
    
    Args:
        s: строка - скобочная последовательность
        
    Returns:
        True, если последовательность может быть подпоследовательностью правильной, иначе False
    """
    open_count = 0
    for char in s:
        if char == '(':
            open_count += 1
        else:  # char == ')'
            if open_count == 0:
                return False
            open_count -= 1
    return True

def can_be_in_same_group(s1, s2, m):
    """
    Проверяет, могут ли две скобочные последовательности быть в одной группе.
    
    Args:
        s1, s2: строки - скобочные последовательности
        m: длина последовательностей
        
    Returns:
        True, если последовательности могут быть в одной группе, иначе False
    """
    # Проверяем, что обе последовательности могут быть подпоследовательностями
    # некоторой правильной скобочной последовательности
    if not is_valid_subsequence(s1) or not is_valid_subsequence(s2):
        return False
    
    # Проверяем совместимость: для каждой позиции i, если s1[i] и s2[i] разные,
    # то одна из них должна быть '(' а другая ')'
    for i in range(m):
        if s1[i] != s2[i] and not (s1[i] == '(' and s2[i] == ')'):
            return False
    
    return True

def build_rbs_for_group(sequences, m):
    """
    Строит правильную скобочную последовательность для группы.
    
    Args:
        sequences: список строк - скобочные последовательности в группе
        m: длина последовательностей
        
    Returns:
        Строка - правильная скобочная последовательность для группы,
        или None, если построить невозможно
    """
    # Для каждой позиции определяем, какая скобка должна быть
    result = [''] * m
    
    for i in range(m):
        has_open = False
        has_close = False
        
        for s in sequences:
            if s[i] == '(':
                has_open = True
            else:  # s[i] == ')'
                has_close = True
        
        # Если в этой позиции есть и открывающие, и закрывающие скобки,
        # то мы должны поставить открывающую скобку, чтобы последовательность была правильной
        if has_open and has_close:
            result[i] = '('
        elif has_open:
            result[i] = '('
        elif has_close:
            result[i] = ')'
    
    rbs = ''.join(result)
    
    # Проверяем, является ли построенная последовательность правильной
    if not is_valid_subsequence(rbs):
        return None
    
    # Проверяем, что ни одна из последовательностей не является подстрокой rbs
    for s in sequences:
        if s in rbs:
            return None
    
    return rbs

def solve():
    """
    Решение задачи F: Regular Bracket Sequence
    
    Задача:
    Даны n скобочных последовательностей одинаковой длины m.
    Нужно разделить их на минимальное количество групп, таких что:
    1. Для каждой группы можно построить правильную скобочную последовательность длины m.
    2. Каждая скобочная последовательность из группы должна быть подпоследовательностью
       построенной правильной скобочной последовательности.
    3. Ни одна из данных скобочных последовательностей не должна быть подстрокой
       построенной правильной скобочной последовательности.
    
    Входные данные:
    - Первая строка: два целых числа n и m
    - Следующие n строк: скобочные последовательности
    
    Выходные данные:
    - Если невозможно разделить последовательности на группы, выводит -1
    - Иначе выводит минимальное количество групп k
      Затем для каждой группы:
        * количество последовательностей в группе
        * правильную скобочную последовательность для группы
        * номера последовательностей в группе (1-индексированные)
    
    Пример:
    Ввод:
        3 6
        )))(((
        ((()))
        ()()()
    
    Вывод:
        1
        3 (()()) 1 2 3
    
    Ввод:
        4 6
        (()()(
        ())((
        ()()()
        ((((((
    
    Вывод:
        2
        2 (())() 1 2
        2 ()()() 3 4
    
    Ввод:
        2 6
        ())()(
        ()))()
    
    Вывод:
        -1
    """
    import sys
    data = sys.stdin.read().splitlines()
    
    if not data:
        return
    
    n, m = map(int, data[0].split())
    sequences = [line.strip() for line in data[1:1+n]]
    
    # Проверяем каждую последовательность
    for s in sequences:
        if len(s) != m or not is_valid_subsequence(s):
            print(-1)
            return
    
    # Строим граф совместимости
    graph = [[False] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            graph[i][j] = can_be_in_same_group(sequences[i], sequences[j], m)
    
    # Используем жадный алгоритм для поиска минимального покрытия кликами
    groups = []
    used = [False] * n
    
    for i in range(n):
        if used[i]:
            continue
        
        # Начинаем новую группу с i-й последовательности
        group = [i]
        used[i] = True
        
        # Добавляем в группу все совместимые последовательности
        for j in range(i+1, n):
            if not used[j] and all(graph[j][k] for k in group):
                group.append(j)
                used[j] = True
        
        # Строим правильную скобочную последовательность для группы
        rbs = build_rbs_for_group([sequences[idx] for idx in group], m)
        if rbs is None:
            print(-1)
            return
        
        groups.append((group, rbs))
    
    # Выводим результат
    print(len(groups))
    for group, rbs in groups:
        indices = [idx + 1 for idx in sorted(group)]  # 1-индексированные номера
        print(f"{len(group)} {rbs} {' '.join(map(str, indices))}")

# Для тестирования
if __name__ == "__main__":
    solve()

''' Полезные ссылки: '''
# 1. Telegram ❃ Хижина программиста Æ: https://t.me/hut_programmer_07
# 2. Telegram №1 @quadd4rv1n7
# 3. Telegram №2 @dupley_maxim_1999
# 4. Rutube канал: https://rutube.ru/channel/4218729/
# 5. Plvideo канал: https://plvideo.ru/channel/AUPv_p1r5AQJ
# 6. YouTube канал: https://www.youtube.com/@it-coders
# 7. ВК группа: https://vk.com/science_geeks