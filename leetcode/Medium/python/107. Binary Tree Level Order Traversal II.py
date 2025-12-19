'''
https://leetcode.com/problems/binary-tree-level-order-traversal-ii/description/

Автор: Дуплей Максим Игоревич - AGLA
ORCID: https://orcid.org/0009-0007-7605-539X
GitHub: https://github.com/QuadDarv1ne/

Решение задачи "Binary Tree Level Order Traversal II".
'''

# Definition for a binary tree node.
# На LeetCode Python класс TreeNode уже определён.

class Solution(object):
    def levelOrderBottom(self, root):
        """
        :type root: TreeNode
        :rtype: List[List[int]]
        """
        if not root:
            return []

        from collections import deque
        q = deque([root])
        result = []

        while q:
            level = []
            for _ in range(len(q)):
                node = q.popleft()
                level.append(node.val)
                if node.left:
                    q.append(node.left)
                if node.right:
                    q.append(node.right)
            result.append(level)

        # Меняем порядок на обратный
        return result[::-1]
