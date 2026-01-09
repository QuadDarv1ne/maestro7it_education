"""
Python (Рекурсивный DFS)

Находит наименьшее поддерево, содержащее все самые глубокие узлы

@param root: Корень бинарного дерева
@return: Корень наименьшего поддерева со всеми самыми глубокими узлами

Сложность: Время O(n), Память O(h), где n - количество узлов, h - высота дерева

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

class Solution:
    def subtreeWithAllDeepest(self, root):
        def dfs(node):
            """Рекурсивная функция, возвращающая (узел, глубина)"""
            if not node:
                return (None, 0)
            
            # Рекурсивно обходим левое и правое поддеревья
            left_node, left_depth = dfs(node.left)
            right_node, right_depth = dfs(node.right)
            
            # Сравниваем глубины поддеревьев
            if left_depth > right_depth:
                # Самые глубокие узлы в левом поддереве
                return (left_node, left_depth + 1)
            elif right_depth > left_depth:
                # Самые глубокие узлы в правом поддереве
                return (right_node, right_depth + 1)
            else:
                # Глубины равны - текущий узел является общим предком
                return (node, left_depth + 1)
        
        return dfs(root)[0]