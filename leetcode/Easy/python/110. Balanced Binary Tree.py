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
    # def isBalanced(self, root: Optional[TreeNode]) -> bool:
    def isBalanced(self, root):
        """
        Проверяет, является ли бинарное дерево высотно сбалансированным.
        Возвращает True, если для каждого узла разница высот его поддеревьев ≤ 1.
        """
        # def height(node: Optional[TreeNode]) -> int:
        def height(node):
            if not node:
                return 0
            lh = height(node.left)
            if lh == -1:
                return -1
            rh = height(node.right)
            if rh == -1:
                return -1
            if abs(lh - rh) > 1:
                return -1
            return 1 + max(lh, rh)

        return height(root) != -1

''' Полезные ссылки: '''
# 1. 💠Telegram💠❃ Хижина программиста Æ: https://t.me/hut_programmer_07
# 2. 💠Telegram №1💠 @quadd4rv1n7
# 3. 💠Telegram №2💠 @dupley_maxim_1999
# 4. Rutube канал: https://rutube.ru/channel/4218729/
# 5. Plvideo канал: https://plvideo.ru/channel/AUPv_p1r5AQJ
# 6. YouTube канал: https://www.youtube.com/@it-coders
# 7. ВК группа: https://vk.com/science_geeks