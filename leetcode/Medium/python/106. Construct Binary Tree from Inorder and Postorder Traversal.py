'''
https://leetcode.com/problems/construct-binary-tree-from-inorder-and-postorder-traversal/description/

Автор: Дуплей Максим Игоревич
ORCID: https://orcid.org/0009-0007-7605-539X
GitHub: https://github.com/QuadDarv1ne/
'''

# Definition for a binary tree node.

class Solution:
    def buildTree(self, inorder, postorder):
        """
        Решение задачи "Construct Binary Tree from Inorder and Postorder Traversal" (LeetCode 106).

        Идея:
        - Последний элемент postorder — корень.
        - Находим его индекс в inorder → левое/правое поддерево.
        - Рекурсивно строим правое и левое поддеревья.
        """
        if not inorder or not postorder:
            return None

        root_val = postorder[-1]
        root = TreeNode(root_val)

        idx = inorder.index(root_val)
        root.left = self.buildTree(inorder[:idx], postorder[:idx])
        root.right = self.buildTree(inorder[idx+1:], postorder[idx:-1])

        return root
