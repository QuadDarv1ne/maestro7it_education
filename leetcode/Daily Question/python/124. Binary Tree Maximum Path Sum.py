"""
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
# class TreeNode(object):
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right

class Solution(object):
    def maxPathSum(self, root):
        """
        :type root: TreeNode
        :rtype: int
        
        Находит максимальную сумму пути в бинарном дереве.
        Путь может начинаться и заканчиваться в любом узле.
        
        Алгоритм:
        1. Рекурсивно обходим дерево
        2. Для каждого узла вычисляем максимальную сумму левой и правой ветвей
        3. Обновляем глобальный максимум суммой через текущий узел
        4. Возвращаем максимальную сумму одной ветви
        
        Пример:
        Вход: [1,2,3] -> 6 (путь 2-1-3)
        Вход: [-10,9,20,null,null,15,7] -> 42 (путь 15-20-7)
        
        Сложность:
        Время: O(n), Память: O(h)
        """
        self.max_sum = float('-inf')
        
        def dfs(node):
            if not node:
                return 0
            
            # Рекурсивно получаем максимальные суммы левой и правой ветвей
            left_sum = max(0, dfs(node.left))
            right_sum = max(0, dfs(node.right))
            
            # Максимальная сумма пути через текущий узел
            path_through_node = node.val + left_sum + right_sum
            
            # Обновляем глобальный максимум
            self.max_sum = max(self.max_sum, path_through_node)
            
            # Возвращаем максимальную сумму одной ветви (для родителя)
            return node.val + max(left_sum, right_sum)
        
        dfs(root)
        return self.max_sum