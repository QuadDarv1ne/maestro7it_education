'''
https://leetcode.com/problems/recover-binary-search-tree/description/

Автор: Дуплей Максим Игоревич
ORCID: https://orcid.org/0009-0007-7605-539X
GitHub: https://github.com/QuadDarv1ne/
'''

class Solution:
    def recoverTree(self, root):
        """
        Решение задачи "Recover Binary Search Tree" (LeetCode 99).

        Идея:
        - In-order обход BST должен быть отсортирован.
        - Если два узла перепутаны, возникают нарушения порядка.
        - Находим два таких узла и меняем их значения местами.

        Сложность:
        - Время: O(n)
        - Память: O(h), h — высота дерева
        """
        self.first = None
        self.second = None
        self.prev = None

        self._inorder(root)

        # Меняем значения местами
        self.first.val, self.second.val = self.second.val, self.first.val

    def _inorder(self, node):
        if not node:
            return

        self._inorder(node.left)

        if self.prev and self.prev.val > node.val:
            if not self.first:
                self.first = self.prev
            self.second = node

        self.prev = node

        self._inorder(node.right)
