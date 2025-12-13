'''
https://leetcode.com/problems/binary-tree-inorder-traversal/description/

Автор: Дуплей Максим Игоревич
ORCID: https://orcid.org/0009-0007-7605-539X
GitHub: https://github.com/QuadDarv1ne/
'''

# Definition for a binary tree node.
class TreeNode(object):
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

class Solution(object):
    def inorderTraversal(self, root):
        """
        Решение задачи "Binary Tree Inorder Traversal" (LeetCode 94).

        Задача:
        - Обойти бинарное дерево в порядке Inorder: левое -> корень -> правое.

        Идея:
        - Используем стек для итеративного обхода.
        - Сохраняем значения в список.

        Сложность:
        - Время: O(n)
        - Память: O(n)
        """
        res = []
        stack = []
        curr = root

        # Итеративный обход
        while curr or stack:
            while curr:
                stack.append(curr)
                curr = curr.left
            curr = stack.pop()
            res.append(curr.val)
            curr = curr.right

        return res
