'''
https://leetcode.com/problems/construct-binary-tree-from-preorder-and-inorder-traversal/description/

Автор: Дуплей Максим Игоревич
ORCID: https://orcid.org/0009-0007-7605-539X
GitHub: https://github.com/QuadDarv1ne/
'''

# Definition for a binary tree node.
# На LeetCode Python класс TreeNode уже определён.

class Solution:
    def buildTree(self, preorder, inorder):
        """
        Решение задачи "Construct Binary Tree from Preorder and Inorder Traversal" (LeetCode 105).

        Идея:
        - Первый элемент preorder — корень дерева.
        - Находим индекс корня в inorder → левое/правое поддерево.
        - Рекурсивно строим левое и правое поддеревья.
        """
        if not preorder or not inorder:
            return None

        root_val = preorder[0]
        root = TreeNode(root_val)

        idx = inorder.index(root_val)
        root.left = self.buildTree(preorder[1:1+idx], inorder[:idx])
        root.right = self.buildTree(preorder[1+idx:], inorder[idx+1:])

        return root
