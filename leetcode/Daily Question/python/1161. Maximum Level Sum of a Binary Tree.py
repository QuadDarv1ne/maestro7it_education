"""
Максимальная сумма уровня в бинарном дереве

@param root Корень бинарного дерева
@return Наименьший уровень с максимальной суммой значений узлов

Сложность: Время O(n), Память O(w), где n - количество узлов, w - максимальная ширина дерева

Автор: Дуплей Максим Игоревич
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

from collections import deque

class Solution:
    def maxLevelSum(self, root):
        if not root:
            return 0
        
        # Инициализация переменных для отслеживания максимума
        max_sum = float('-inf')
        max_level = 1
        current_level = 1
        
        # Очередь для обхода в ширину (BFS)
        queue = deque([root])
        
        while queue:
            level_sum = 0
            level_size = len(queue)
            
            # Обработка всех узлов текущего уровня
            for _ in range(level_size):
                node = queue.popleft()
                level_sum += node.val
                
                # Добавление дочерних узлов в очередь
                if node.left:
                    queue.append(node.left)
                if node.right:
                    queue.append(node.right)
            
            # Обновление максимума (только если строго больше)
            if level_sum > max_sum:
                max_sum = level_sum
                max_level = current_level
            
            current_level += 1
        
        return max_level