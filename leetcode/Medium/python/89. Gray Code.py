'''
https://leetcode.com/problems/gray-code/description/

Автор: Дуплей Максим Игоревич
ORCID: https://orcid.org/0009-0007-7605-539X
GitHub: https://github.com/QuadDarv1ne/
'''

class Solution(object):
    def grayCode(self, n):
        """
        Решение задачи "Gray Code" (LeetCode 89).

        Задача:
        - Дан неотрицательный n — количество бит.
        - Вернуть последовательность Gray‑кодов длины 2^n,
          где соседние элементы отличаются ровно одним битом.
        - Последовательность должна начинаться с 0.

        Идея:
        - Используем метод зеркального отражения:
          на каждом шаге добавляем элементы в обратном порядке,
          устанавливая новый бит.
        - Альтернатива: встроенная формула i ^ (i >> 1).

        Сложность:
        - Время: O(2^n)
        - Память: O(2^n)
        """
        result = [0]
        for i in range(n):
            for j in range(len(result)-1, -1, -1):
                result.append(result[j] + (1 << i))
        return result
