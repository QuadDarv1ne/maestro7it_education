'''
https://leetcode.com/problems/balanced-binary-tree/description/

Автор: Дуплей Максим Игоревич
ORCID: https://orcid.org/0009-0007-7605-539X
GitHub: https://github.com/QuadDarv1ne/
'''

# from typing import Optional

# class TreeNode:
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right

class Solution:
    def isBalanced(self, root):
        """
        Определяет, является ли бинарное дерево сбалансированным.

        Дерево считается сбалансированным, если для каждого узла разница высот
        его левого и правого поддеревьев не превышает 1 по абсолютному значению.

        Алгоритм использует пост-обход (bottom-up): 
        возвращает высоту поддерева, а при обнаружении несбалансированности
        сразу возвращает -1, которое распространяется вверх.

        Args:
            root: Корень бинарного дерева (может быть None)

        Returns:
            bool: True если дерево сбалансировано, иначе False

        Сложность:
            Время: O(n)
            Память: O(h) — в худшем случае O(n), в среднем O(log n)
        """
        def check_height(node):
            if not node:
                return 0
            
            left = check_height(node.left)
            if left == -1:
                return -1
                
            right = check_height(node.right)
            if right == -1:
                return -1
            
            if abs(left - right) > 1:
                return -1
                
            return max(left, right) + 1

        return check_height(root) != -1

''' Полезные ссылки: '''
# 1. Telegram ❃ Хижина программиста Æ: https://t.me/hut_programmer_07
# 2. Telegram №1 @quadd4rv1n7
# 3. Telegram №2 @dupley_maxim_1999
# 4. Rutube канал: https://rutube.ru/channel/4218729/
# 5. Plvideo канал: https://plvideo.ru/channel/AUPv_p1r5AQJ
# 6. YouTube канал: https://www.youtube.com/@it-coders
# 7. ВК группа: https://vk.com/science_geeks