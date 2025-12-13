'''
https://leetcode.com/problems/partition-list/description/

Автор: Дуплей Максим Игоревич
ORCID: https://orcid.org/0009-0007-7605-539X
GitHub: https://github.com/QuadDarv1ne/
'''

# Definition for singly-linked list.
class ListNode(object):
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

class Solution(object):
    def partition(self, head, x):
        """
        Решение задачи "Partition List" (LeetCode 86).

        Задача:
        - Дан связный список head и число x.
        - Перестроить список так, чтобы все узлы < x
          были перед узлами ≥ x.
        - Относительный порядок узлов внутри групп
          должен сохраниться.

        Идея:
        - Используем 2 фиктивных списка:
          one  — для значений < x
          two  — для значений ≥ x
        - На каждом узле добавляем его в соответстующий
          список, затем склеиваем.

        Сложность:
        - Время: O(n)
        - Память: O(1)
        """
        before_head = ListNode(0)
        after_head = ListNode(0)
        before = before_head
        after = after_head

        curr = head
        while curr:
            if curr.val < x:
                before.next = curr
                before = before.next
            else:
                after.next = curr
                after = after.next
            curr = curr.next

        after.next = None
        before.next = after_head.next

        return before_head.next
