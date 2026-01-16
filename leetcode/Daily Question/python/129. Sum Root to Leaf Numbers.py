"""
Решение задачи LeetCode №129: "Sum Root to Leaf Numbers"
Ссылка на задачу: https://leetcode.com/problems/sum-root-to-leaf-numbers/
Описание: Дано бинарное дерево, где каждый узел содержит цифру от 0 до 9.
Каждое корневое-листовое число образуется путем соединения цифр от корня до листа.
Требуется найти сумму всех корневых-листовых чисел.

Автор: Дуплей Максим Игоревич - AGLA
ORCID: https://orcid.org/0009-0007-7605-539X
GitHub: https://github.com/QuadDarv1ne/

Полезные ссылки:
1. Telegram ❃ Хижина программиста Æ: https://t.me/hut_programmer_07
2. Telegram №1 @quadd4rv1n7
3. Telegram №2 @dupley_maxim_1999
4. Rutube канал: https://rutube.ru/channel/4218729/
5. Plvideo канал: https://plvideo.ru/channel/AUPv_p1r5AQJ
6. YouTube канал: https://www.youtube.com/@it-coders
7. ВК группа: https://vk.com/science_geeks
"""

# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right

class Solution:
    def sumNumbers(self, root):
        """
        Вычисляет сумму всех чисел, образованных путями от корня к листьям.
        
        Алгоритм:
        1. Рекурсивный обход дерева с накоплением текущего значения
        2. При достижении листа добавляем значение к сумме
        
        Сложность: O(n) время, O(h) память
        
        Пример:
        Вход: [1,2,3] -> 25 (12 + 13)
        Вход: [4,9,0,5,1] -> 1026 (495 + 491 + 40)
        """
        
        def dfs(node, current_sum):
            if not node:
                return 0
            
            # Обновляем текущее значение
            current_sum = current_sum * 10 + node.val
            
            # Если это лист, возвращаем текущее значение
            if not node.left and not node.right:
                return current_sum
            
            # Рекурсивно обходим потомков
            left_sum = dfs(node.left, current_sum)
            right_sum = dfs(node.right, current_sum)
            
            return left_sum + right_sum
        
        return dfs(root, 0)