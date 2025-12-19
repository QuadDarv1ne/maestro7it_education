'''
https://leetcode.com/problems/convert-sorted-list-to-binary-search-tree/

Автор: Дуплей Максим Игоревич - AGLA
ORCID: https://orcid.org/0009-0007-7605-539X
GitHub: https://github.com/QuadDarv1ne/

Решение задачи "Convert Sorted List to Binary Search Tree".
'''

# Definition for singly-linked list.
# LeetCode уже предоставляет ListNode и TreeNode

class Solution(object):
    def sortedListToBST(self, head):
        """
        :type head: ListNode
        :rtype: TreeNode
        """
        # 1) Посчитать длину списка
        size = 0
        node = head
        while node:
            size += 1
            node = node.next

        # Вспомогательная переменная — указатель по списку
        self.curr = head

        def build(l, r):
            if l > r:
                return None
            mid = (l + r) // 2

            # Сначала строим левое поддерево
            left = build(l, mid - 1)

            # Текущий ListNode становится корнем
            root = TreeNode(self.curr.val)
            root.left = left

            # Сдвигаем глобальный указатель
            self.curr = self.curr.next

            # Построим правое поддерево
            root.right = build(mid + 1, r)
            return root

        return build(0, size - 1)
