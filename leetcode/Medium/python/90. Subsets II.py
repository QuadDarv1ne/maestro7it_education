'''
https://leetcode.com/problems/subsets-ii/description/

Автор: Дуплей Максим Игоревич
ORCID: https://orcid.org/0009-0007-7605-539X
GitHub: https://github.com/QuadDarv1ne/
'''

class Solution(object):
    def subsetsWithDup(self, nums):
        """
        Решение задачи "Subsets II" (LeetCode 90).

        Задача:
        - Дан массив nums, возможно с дубликатами.
        - Вернуть все уникальные подмножества.

        Идея:
        - Сортируем массив, чтобы дубликаты шли подряд.
        - Используем backtracking:
          на каждом уровне выбираем элемент либо пропускаем.
        - Пропускаем повторные элементы на одном уровне рекурсии,
          чтобы избежать одинаковых подмножеств.

        Сложность:
        - Время: O(2^n * n)
        - Память: O(2^n * n)
        """
        nums.sort()
        res = []

        def backtrack(start, path):
            res.append(path[:])
            for i in range(start, len(nums)):
                if i > start and nums[i] == nums[i-1]:
                    continue
                path.append(nums[i])
                backtrack(i+1, path)
                path.pop()

        backtrack(0, [])
        return res
