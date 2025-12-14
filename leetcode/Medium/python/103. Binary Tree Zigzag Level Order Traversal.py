'''
https://leetcode.com/problems/binary-tree-zigzag-level-order-traversal/description/

Автор: Дуплей Максим Игоревич
ORCID: https://orcid.org/0009-0007-7605-539X
GitHub: https://github.com/QuadDarv1ne/
'''

# Definition for a binary tree node.
# LeetCode Python уже предоставляет TreeNode — повторно объявлять не нужно.

class Solution:
    def zigzagLevelOrder(self, root):
        """
        Решение задачи "Binary Tree Zigzag Level Order Traversal" (LeetCode 103).

        Идея:
        - BFS по уровням.
        - Переменная flip чередует порядок.
        """
        if not root:
            return []

        results = []
        level_nodes = [root]
        flip = False

        while level_nodes:
            vals = []
            next_level = []
            for node in level_nodes:
                vals.append(node.val)
                if node.left:
                    next_level.append(node.left)
                if node.right:
                    next_level.append(node.right)
            if flip:
                vals.reverse()
            results.append(vals)

            level_nodes = next_level
            flip = not flip

        return results
