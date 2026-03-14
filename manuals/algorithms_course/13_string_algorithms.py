"""
СТРОКОВЫЕ АЛГОРИТМЫ (STRING ALGORITHMS)

Строки — одна из важнейших структур данных.
Работа со строками требует понимания их особенностей и эффективных методов.

Основные темы:
1. Поиск подстроки
2. Палиндромы
3. Анаграммы
4. Самая длинная подстрока
5. Проблемы с кодировкой и символами
6. Сравнение строк

Сложность операций со строками:
- Длина строки: O(1) в Python (len)
- Конкатенация: O(n + m)
- Срез s[i:j]: O(j - i)
- Поиск подстроки: O(n × m) наивный, O(n + m) KMP

Важно:
В Python строки неизменяемы! Любая модификация создаёт новую строку.
Для множественных изменений используйте list и ''.join().
"""


# ===== ПАЛИНДРОМЫ =====

def is_palindrome(s):
    """
    Проверка, является ли строка палиндромом.
    
    Палиндром — строка, читающаяся одинаково слева направо и справа налево.
    
    Аргументы:
        s: строка
    
    Возвращает:
        bool: True если палиндром
    
    Сложность: O(n) по времени, O(1) по памяти
    
    Пример:
        >>> is_palindrome("racecar")
        True
        >>> is_palindrome("hello")
        False
    """
    left, right = 0, len(s) - 1
    while left < right:
        if s[left] != s[right]:
            return False
        left += 1
        right -= 1
    return True


def is_palindrome_alphanumeric(s):
    """
    Проверка палиндрома с учётом только буквенно-цифровых символов.
    
    Игнорирует регистр и не-буквенно-цифровые символы.
    
    Аргументы:
        s: строка
    
    Возвращает:
        bool: True если палиндром
    
    Пример:
        >>> is_palindrome_alphanumeric("A man, a plan, a canal: Panama")
        True
    """
    left, right = 0, len(s) - 1
    
    while left < right:
        while left < right and not s[left].isalnum():
            left += 1
        while left < right and not s[right].isalnum():
            right -= 1
        
        if s[left].lower() != s[right].lower():
            return False
        
        left += 1
        right -= 1
    
    return True


def longest_palindrome_substring(s):
    """
    Найти самый длинный палиндром-подстроку.
    
    Расширяем от центра. Каждый символ — потенциальный центр.
    Учитываем палиндромы чётной и нечётной длины.
    
    Аргументы:
        s: строка
    
    Возвращает:
        str: самый длинный палиндром
    
    Сложность: O(n²) по времени, O(1) по памяти
    
    Пример:
        >>> longest_palindrome_substring("babad")
        'bab'  # или 'aba'
    """
    if not s:
        return ""
    
    def expand_around_center(left, right):
        while left >= 0 and right < len(s) and s[left] == s[right]:
            left -= 1
            right += 1
        return s[left + 1:right]
    
    longest = s[0]
    
    for i in range(len(s)):
        # Нечётная длина (центр — один символ)
        odd = expand_around_center(i, i)
        if len(odd) > len(longest):
            longest = odd
        
        # Чётная длина (центр — между символами)
        even = expand_around_center(i, i + 1)
        if len(even) > len(longest):
            longest = even
    
    return longest


def count_palindromic_substrings(s):
    """
    Подсчитать количество палиндромных подстрок.
    
    Аргументы:
        s: строка
    
    Возвращает:
        int: количество палиндромных подстрок
    
    Сложность: O(n²)
    
    Пример:
        >>> count_palindromic_substrings("aaa")
        6  # 'a', 'a', 'a', 'aa', 'aa', 'aaa'
    """
    count = 0
    
    def expand(left, right):
        nonlocal count
        while left >= 0 and right < len(s) and s[left] == s[right]:
            count += 1
            left -= 1
            right += 1
    
    for i in range(len(s)):
        expand(i, i)      # Нечётная длина
        expand(i, i + 1)  # Чётная длина
    
    return count


# ===== АНАГРАММЫ =====

def is_anagram(s1, s2):
    """
    Проверка, являются ли строки анаграммами.
    
    Анаграммы — строки с одинаковым набором символов.
    
    Аргументы:
        s1, s2: строки
    
    Возвращает:
        bool: True если анаграммы
    
    Сложность: O(n) по времени, O(k) по памяти (k — размер алфавита)
    
    Пример:
        >>> is_anagram("listen", "silent")
        True
    """
    from collections import Counter
    return Counter(s1) == Counter(s2)


def group_anagrams(strs):
    """
    Сгруппировать строки по анаграммам.
    
    Аргументы:
        strs: список строк
    
    Возвращает:
        list: список групп анаграмм
    
    Сложность: O(n × k log k), где k — средняя длина строки
    
    Пример:
        >>> group_anagrams(["eat", "tea", "tan", "ate", "nat", "bat"])
        [['eat', 'tea', 'ate'], ['tan', 'nat'], ['bat']]
    """
    from collections import defaultdict
    
    groups = defaultdict(list)
    
    for s in strs:
        # Сортировка как ключ
        key = ''.join(sorted(s))
        groups[key].append(s)
    
    return list(groups.values())


# ===== ПОИСК ПОДСТРОКИ =====

def find_all_occurrences(text, pattern):
    """
    Найти все вхождения подстроки (наивный алгоритм).
    
    Аргументы:
        text: текст для поиска
        pattern: искомый образец
    
    Возвращает:
        list: индексы всех вхождений
    
    Сложность: O(n × m)
    
    Пример:
        >>> find_all_occurrences("ababa", "aba")
        [0, 2]
    """
    n, m = len(text), len(pattern)
    result = []
    
    for i in range(n - m + 1):
        if text[i:i + m] == pattern:
            result.append(i)
    
    return result


def kmp_search(text, pattern):
    """
    Поиск подстроки алгоритмом Кнута-Морриса-Пратта.
    
    Строит таблицу частичных совпадений (lps),
    что позволяет избежать повторных сравнений.
    
    Аргументы:
        text: текст для поиска
        pattern: искомый образец
    
    Возвращает:
        list: индексы всех вхождений
    
    Сложность: O(n + m)
    
    Пример:
        >>> kmp_search("ababa", "aba")
        [0, 2]
    """
    def build_lps(p):
        """Построение таблицы lps (longest proper prefix which is suffix)."""
        m = len(p)
        lps = [0] * m
        length = 0
        i = 1
        
        while i < m:
            if p[i] == p[length]:
                length += 1
                lps[i] = length
                i += 1
            elif length != 0:
                length = lps[length - 1]
            else:
                lps[i] = 0
                i += 1
        
        return lps
    
    n, m = len(text), len(pattern)
    
    if m == 0:
        return []
    
    lps = build_lps(pattern)
    result = []
    
    i = j = 0  # i — индекс в text, j — индекс в pattern
    
    while i < n:
        if text[i] == pattern[j]:
            i += 1
            j += 1
            
            if j == m:
                result.append(i - m)
                j = lps[j - 1]
        else:
            if j != 0:
                j = lps[j - 1]
            else:
                i += 1
    
    return result


# ===== САМАЯ ДЛИННАЯ ОБЩАЯ ПОДСТРОКА =====

def longest_common_prefix(strs):
    """
    Самый длинный общий префикс массива строк.
    
    Аргументы:
        strs: список строк
    
    Возвращает:
        str: общий префикс
    
    Сложность: O(S), где S — сумма длин всех строк
    
    Пример:
        >>> longest_common_prefix(["flower", "flow", "flight"])
        'fl'
    """
    if not strs:
        return ""
    
    # Находим минимальную и максимальную строку
    min_str = min(strs)
    max_str = max(strs)
    
    i = 0
    while i < len(min_str) and min_str[i] == max_str[i]:
        i += 1
    
    return min_str[:i]


def longest_common_substring(s1, s2):
    """
    Самая длинная общая подстрока двух строк.
    
    Динамическое программирование.
    dp[i][j] = длина общей подстроки, заканчивающейся в s1[i-1] и s2[j-1].
    
    Аргументы:
        s1, s2: строки
    
    Возвращает:
        str: самая длинная общая подстрока
    
    Сложность: O(n × m) по времени и памяти
    
    Пример:
        >>> longest_common_substring("abcdef", "zcdemf")
        'cde'
    """
    m, n = len(s1), len(s2)
    dp = [[0] * (n + 1) for _ in range(m + 1)]
    max_len = 0
    end_pos = 0
    
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if s1[i - 1] == s2[j - 1]:
                dp[i][j] = dp[i - 1][j - 1] + 1
                if dp[i][j] > max_len:
                    max_len = dp[i][j]
                    end_pos = i
    
    return s1[end_pos - max_len:end_pos]


# ===== РЕДАКЦИОННОЕ РАССТОЯНИЕ =====

def edit_distance(s1, s2):
    """
    Редакционное расстояние (расстояние Левенштейна).
    
    Минимальное количество операций (вставка, удаление, замена)
    для превращения одной строки в другую.
    
    Аргументы:
        s1, s2: строки
    
    Возвращает:
        int: редакционное расстояние
    
    Сложность: O(n × m)
    
    Пример:
        >>> edit_distance("horse", "ros")
        3
    """
    m, n = len(s1), len(s2)
    dp = [[0] * (n + 1) for _ in range(m + 1)]
    
    # Базовые случаи
    for i in range(m + 1):
        dp[i][0] = i
    for j in range(n + 1):
        dp[0][j] = j
    
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if s1[i - 1] == s2[j - 1]:
                dp[i][j] = dp[i - 1][j - 1]
            else:
                dp[i][j] = 1 + min(
                    dp[i - 1][j],      # Удаление
                    dp[i][j - 1],      # Вставка
                    dp[i - 1][j - 1]   # Замена
                )
    
    return dp[m][n]


# ===== ПРЕОБРАЗОВАНИЯ СТРОК =====

def reverse_string(s):
    """
    Разворот строки.
    
    Сложность: O(n)
    """
    return s[::-1]


def reverse_words(s):
    """
    Разворот порядка слов в строке.
    
    Аргументы:
        s: строка со словами
    
    Возвращает:
        str: строка с развёрнутым порядком слов
    
    Пример:
        >>> reverse_words("the sky is blue")
        'blue is sky the'
    """
    words = s.split()
    return ' '.join(reversed(words))


def reverse_words_in_place(s):
    """
    Разворот слов в строке без лишних пробелов.
    
    Пример:
        >>> reverse_words_in_place("  hello   world  ")
        'world hello'
    """
    words = s.split()
    return ' '.join(reversed(words))


# ===== КОДИРОВКАRun-length =====

def run_length_encode(s):
    """
    Кодирование длин серий (Run-Length Encoding).
    
    Аргументы:
        s: строка
    
    Возвращает:
        str: закодированная строка
    
    Пример:
        >>> run_length_encode("AAABBBCCDAA")
        'A3B3C2D1A2'
    """
    if not s:
        return ""
    
    result = []
    count = 1
    
    for i in range(1, len(s)):
        if s[i] == s[i - 1]:
            count += 1
        else:
            result.append(s[i - 1] + str(count))
            count = 1
    
    result.append(s[-1] + str(count))
    return ''.join(result)


def run_length_decode(s):
    """
    Декодирование длин серий.
    
    Пример:
        >>> run_length_decode("A3B3C2D1A2")
        'AAABBBCCDAA'
    """
    result = []
    i = 0
    
    while i < len(s):
        char = s[i]
        i += 1
        count_str = ""
        while i < len(s) and s[i].isdigit():
            count_str += s[i]
            i += 1
        result.append(char * int(count_str))
    
    return ''.join(result)


# ===== УНИКАЛЬНЫЕ СИМВОЛЫ =====

def first_unique_char(s):
    """
    Найти первый неповторяющийся символ.
    
    Аргументы:
        s: строка
    
    Возвращает:
        int: индекс первого уникального символа или -1
    
    Сложность: O(n)
    
    Пример:
        >>> first_unique_char("leetcode")
        0
        >>> first_unique_char("loveleetcode")
        2
    """
    from collections import Counter
    
    count = Counter(s)
    
    for i, char in enumerate(s):
        if count[char] == 1:
            return i
    
    return -1


def first_repeating_char(s):
    """
    Найти первый повторяющийся символ.
    
    Возвращает:
        str: первый символ, который встречается более одного раза
             или None, если все уникальны
    """
    seen = set()
    
    for char in s:
        if char in seen:
            return char
        seen.add(char)
    
    return None


# ===== РАЗБИЕНИЕ СТРОКИ =====

def word_break(s, word_dict):
    """
    Проверка возможности разбить строку на слова из словаря.
    
    Аргументы:
        s: строка
        word_dict: множество допустимых слов
    
    Возвращает:
        bool: True если разбиение возможно
    
    Сложность: O(n² × m), где m — средняя длина слова
    
    Пример:
        >>> word_break("leetcode", ["leet", "code"])
        True
    """
    word_set = set(word_dict)
    n = len(s)
    dp = [False] * (n + 1)
    dp[0] = True
    
    for i in range(1, n + 1):
        for j in range(i):
            if dp[j] and s[j:i] in word_set:
                dp[i] = True
                break
    
    return dp[n]


if __name__ == "__main__":
    print(__doc__)
    print("\n" + "="*60)
    
    # Палиндромы
    print("Палиндромы:")
    print(f"  'racecar' -> {is_palindrome('racecar')}")
    print(f"  'A man, a plan, a canal: Panama' -> {is_palindrome_alphanumeric('A man, a plan, a canal: Panama')}")
    print(f"  Самый длинный в 'babad': '{longest_palindrome_substring('babad')}'")
    
    # Анаграммы
    print("\nАнаграммы:")
    print(f"  'listen' vs 'silent': {is_anagram('listen', 'silent')}")
    print(f"  Группы: {group_anagrams(['eat', 'tea', 'tan', 'ate', 'nat', 'bat'])}")
    
    # Поиск
    print("\nПоиск подстроки:")
    print(f"  KMP 'ababa' в 'aba': {kmp_search('ababa', 'aba')}")
    
    # LCS
    print("\nОбщая подстрока:")
    print(f"  'abcdef' & 'zcdemf': '{longest_common_substring('abcdef', 'zcdemf')}'")
    
    # Редакционное расстояние
    print("\nРедакционное расстояние:")
    print(f"  'horse' -> 'ros': {edit_distance('horse', 'ros')}")
    
    # Уникальный символ
    print("\nПервый уникальный символ:")
    print(f"  'leetcode': индекс {first_unique_char('leetcode')}")
    print(f"  'loveleetcode': индекс {first_unique_char('loveleetcode')}")
