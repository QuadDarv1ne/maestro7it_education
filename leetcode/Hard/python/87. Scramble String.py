'''
https://leetcode.com/problems/scramble-string/description/

Автор: Дуплей Максим Игоревич
ORCID: https://orcid.org/0009-0007-7605-539X
GitHub: https://github.com/QuadDarv1ne/
'''

from collections import Counter

class Solution(object):
    def isScramble(self, s1, s2):
        """
        Решение задачи "Scramble String" (LeetCode 87).

        Идея:
        - Используем рекурсивный поиск.
        - Результаты подзадач сохраняем в словаре memo.
        - Ключ: (i1, i2, length).
        - Без использования lru_cache.

        Сложность:
        - Время: O(n^4)
        - Память: O(n^3)
        """
        if len(s1) != len(s2):
            return False

        if Counter(s1) != Counter(s2):
            return False

        memo = {}

        def dfs(i1, i2, length):
            if (i1, i2, length) in memo:
                return memo[(i1, i2, length)]

            if length == 1:
                return s1[i1] == s2[i2]

            for k in range(1, length):
                # Без обмена
                if dfs(i1, i2, k) and dfs(i1 + k, i2 + k, length - k):
                    memo[(i1, i2, length)] = True
                    return True
                # С обменом
                if dfs(i1, i2 + length - k, k) and dfs(i1 + k, i2, length - k):
                    memo[(i1, i2, length)] = True
                    return True

            memo[(i1, i2, length)] = False
            return False

        return dfs(0, 0, len(s1))
