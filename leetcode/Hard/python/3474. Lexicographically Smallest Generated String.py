"""
https://leetcode.com/problems/lexicographically-smallest-generated-string/description/
Автор: Дуплей Максим Игоревич - AGLA
ORCID: https://orcid.org/0009-0007-7605-539X
GitHub: https://github.com/QuadDarv1ne/

Решение задачи "3474. Lexicographically Smallest Generated String" на Python

Полезные ссылки:
1. Telegram ❃ Хижина программиста Æ: https://t.me/hut_programmer_07
2. Telegram №1 @quadd4rv1n7
3. Telegram №2 @dupley_maxim_1999
4. Rutube канал: https://rutube.ru/channel/4218729/
5. Plvideo канал: https://plvideo.ru/channel/AUPv_p1r5AQJ
6. YouTube канал: https://www.youtube.com/@it-coders
7. ВК группа: https://vk.com/science_geeks
"""

import bisect

class Solution(object):
    def generateString(self, str1, str2):
        """
        :type str1: str
        :type str2: str
        :rtype: str
        """
        n, m = len(str1), len(str2)
        L = n + m - 1
        word = [-1] * L
        
        # Шаг 1: Фиксируем символы из T-условий
        for i in range(n):
            if str1[i] == 'T':
                for k in range(m):
                    pos = i + k
                    if pos >= L: return ""
                    if word[pos] != -1 and word[pos] != ord(str2[k]): return ""
                    word[pos] = ord(str2[k])
                    
        def would_match_if_a(i):
            for k in range(m):
                pos = i + k
                if pos >= L: return False
                if word[pos] == -1:
                    if str2[k] != 'a': return False
                else:
                    if word[pos] != ord(str2[k]): return False
            return True
            
        def get_rightmost_undef(i):
            r = -1
            for k in range(m):
                pos = i + k
                if pos < L and word[pos] == -1: r = pos
            return r
            
        # Шаг 2: Собираем конфликтующие F-условия
        violated = []
        for i in range(n):
            if str1[i] == 'F' and would_match_if_a(i):
                r = get_rightmost_undef(i)
                if r == -1: return ""
                violated.append((i, r))
                
        # Шаг 3: Жадное исправление
        violated.sort(key=lambda x: x[1])
        active = []
        
        for i, r in violated:
            idx = bisect.bisect_left(active, i)
            if idx == len(active) or active[idx] > i + m - 1:
                bisect.insort(active, r)
                word[r] = ord('b')
                
        # Шаг 4: Сборка финальной строки
        return "".join(chr(c) if c != -1 else 'a' for c in word)