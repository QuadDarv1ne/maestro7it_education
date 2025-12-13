'''
https://leetcode.com/problems/remove-duplicates-from-sorted-list-ii/description/

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
    def deleteDuplicates(self, head):
        """
        Решение задачи "Remove Duplicates from Sorted List II" (LeetCode 82).

        Задача:
        - Дан отсортированный связный список.
        - Необходимо удалить все узлы, значения которых повторяются,
          оставив только уникальные элементы.

        Идея:
        - Используем фиктивный (dummy) узел перед головой списка.
        - prev указывает на последний подтверждённый уникальный узел.
        - curr используется для обхода списка.
        - Если обнаружена группа дубликатов, пропускаем все узлы
          с этим значением.
        - В конце возвращаем dummy.next.

        Сложность:
        - Время: O(n)
        - Память: O(1)
        """
        dummy = ListNode(0, head)
        prev = dummy
        curr = head

        while curr and curr.next:
            # Обнаружены дубликаты
            if curr.val == curr.next.val:
                dup_val = curr.val
                # Пропускаем все узлы с этим значением
                while curr and curr.val == dup_val:
                    curr = curr.next
                prev.next = curr
            else:
                prev = curr
                curr = curr.next

        return dummy.next


''' Полезные ссылки: '''
# 1. Telegram ❃ Хижина программиста Æ: https://t.me/hut_programmer_07  
# 2. Telegram №1 @quadd4rv1n7
# 3. Telegram №2 @dupley_maxim_1999
# 4. Rutube канал: https://rutube.ru/channel/4218729/  
# 5. Plvideo канал: https://plvideo.ru/channel/AUPv_p1r5AQJ  
# 6. YouTube канал: https://www.youtube.com/@it-coders  
# 7. ВК группа: https://vk.com/science_geeks
