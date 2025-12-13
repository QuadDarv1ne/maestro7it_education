'''
https://leetcode.com/problems/reverse-linked-list-ii/description/

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
    def reverseBetween(self, head, left, right):
        """
        Решение задачи "Reverse Linked List II" (LeetCode 92).

        Задача:
        - Дан связный список head.
        - Поменять порядок узлов между позициями left и right включительно.
        - Остальные части списка сохранить.

        Идея:
        - Используем фиктивный узел (dummy) перед head.
        - Доходим до узла перед left.
        - Переворачиваем участок [left, right] с помощью вставки узлов
          в начало подсписка.
        - Возвращаем dummy.next.

        Сложность:
        - Время: O(n)
        - Память: O(1)
        """
        dummy = ListNode(0, head)
        prev = dummy

        # Доходим до узла перед left
        for _ in range(left - 1):
            prev = prev.next

        # Начинаем переворот
        curr = prev.next
        for _ in range(right - left):
            temp = curr.next
            curr.next = temp.next
            temp.next = prev.next
            prev.next = temp

        return dummy.next
