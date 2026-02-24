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
# class TreeNode:
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right

class Solution:
    def sumRootToLeaf(self, root):
        """
        Вычисляет сумму всех двоичных чисел, образованных путями от корня до листьев.
        Использует DFS с накоплением текущего значения.
        """
        def dfs(node, current):
            if not node:
                return 0
            # Формируем новое число: сдвигаем текущее влево и добавляем значение узла
            current = (current << 1) | node.val
            # Если это лист, возвращаем полученное число
            if not node.left and not node.right:
                return current
            # Иначе продолжаем обход потомков
            return dfs(node.left, current) + dfs(node.right, current)

        return dfs(root, 0)