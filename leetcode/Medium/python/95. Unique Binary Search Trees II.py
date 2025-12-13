'''
https://leetcode.com/problems/unique-binary-search-trees-ii/description/

Автор: Дуплей Максим Игоревич
ORCID: https://orcid.org/0009-0007-7605-539X
GitHub: https://github.com/QuadDarv1ne/
'''

# Definition for a binary tree node.
# class TreeNode(object):
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right

class Solution(object):
    def generateTrees(self, n):
        """
        Решение задачи "Unique Binary Search Trees II" (LeetCode 95).

        Вариант без lru_cache.

        Идея:
        - Рекурсивно строим все BST для диапазона [start..end].
        - Для каждого числа i выбираем его как корень,
          рекурсивно строим левое и правое поддерево.
        """
        if n == 0:
            return []

        def build(start, end):
            trees = []
            if start > end:
                trees.append(None)
                return trees

            for i in range(start, end+1):
                left_trees = build(start, i-1)
                right_trees = build(i+1, end)
                for l in left_trees:
                    for r in right_trees:
                        root = TreeNode(i)
                        root.left = l
                        root.right = r
                        trees.append(root)
            return trees

        return build(1, n)
