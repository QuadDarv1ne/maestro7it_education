'''
https://leetcode.com/problems/maximum-depth-of-binary-tree/description/
'''

# Определение узла дерева
# class TreeNode:
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right

class Solution:
    def maxDepth(self, root):
        """
        Задача: Найти максимальную глубину бинарного дерева.

        Алгоритм:
        1. Если дерево пустое, вернуть 0.
        2. Рекурсивно вычислить глубину левого и правого поддерева.
        3. Результат = 1 + max(глубина_левого, глубина_правого).

        Сложность:
        - Время: O(n), где n — количество узлов.
        - Память: O(h), где h — высота дерева (глубина рекурсии).
        """
        if root is None:
            return 0
        return 1 + max(self.maxDepth(root.left), self.maxDepth(root.right))

''' Полезные ссылки: '''
# 1. 💠Telegram💠❃ Хижина программиста Æ: https://t.me/hut_programmer_07
# 2. 💠Telegram №1💠 @quadd4rv1n7
# 3. 💠Telegram №2💠 @dupley_maxim_1999
# 4. Rutube канал: https://rutube.ru/channel/4218729/
# 5. Plvideo канал: https://plvideo.ru/channel/AUPv_p1r5AQJ
# 6. YouTube канал: https://www.youtube.com/@it-coders
# 7. ВК группа: https://vk.com/science_geeks