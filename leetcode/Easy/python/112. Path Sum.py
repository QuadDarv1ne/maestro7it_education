'''
https://leetcode.com/problems/path-sum/description/

Автор: Дуплей Максим Игоревич
ORCID: https://orcid.org/0009-0007-7605-539X
GitHub: https://github.com/QuadDarv1ne/
'''

# from typing import Optional

# Определение структуры узла бинарного дерева
# class TreeNode:
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right

class Solution:
    # def hasPathSum(self, root: Optional[TreeNode], targetSum: int) -> bool:
    def hasPathSum(self, root, targetSum):
        """
        Проверяет, существует ли путь от корня до листа, сумма значений которого равна targetSum.

        :param root: корень бинарного дерева
        :param targetSum: целевая сумма
        :return: True, если такой путь существует, иначе False
        """
        if not root:
            return False

        if not root.left and not root.right:
            return root.val == targetSum

        return (self.hasPathSum(root.left, targetSum - root.val) or
                self.hasPathSum(root.right, targetSum - root.val))

''' Полезные ссылки: '''
# 1. 💠Telegram💠❃ Хижина программиста Æ: https://t.me/hut_programmer_07
# 2. 💠Telegram №1💠 @quadd4rv1n7
# 3. 💠Telegram №2💠 @dupley_maxim_1999
# 4. Rutube канал: https://rutube.ru/channel/4218729/
# 5. Plvideo канал: https://plvideo.ru/channel/AUPv_p1r5AQJ
# 6. YouTube канал: https://www.youtube.com/@it-coders
# 7. ВК группа: https://vk.com/science_geeks