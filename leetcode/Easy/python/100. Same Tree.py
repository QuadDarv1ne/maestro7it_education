'''
https://leetcode.com/problems/same-tree/description/

Автор: Дуплей Максим Игоревич
ORCID: https://orcid.org/0009-0007-7605-539X
GitHub: https://github.com/QuadDarv1ne/
'''

# Definition for a binary tree node.
# На LeetCode Python класс TreeNode уже определён — повторно объявлять не нужно.

class Solution:
    def isSameTree(self, p, q):
        """
        Решение задачи "Same Tree" (LeetCode 100).

        Идея:
        - Рекурсивно сравниваем узлы.
        - Если оба узла None — одинаковы.
        - Если один None и другой нет — не одинаковы.
        - Иначе значения должны быть равны, и левое/правое поддеревья тоже.
        """
        if not p and not q:
            return True
        if not p or not q:
            return False
        if p.val != q.val:
            return False
        return self.isSameTree(p.left, q.left) and self.isSameTree(p.right, q.right)
