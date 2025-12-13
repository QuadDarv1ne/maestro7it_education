'''
https://leetcode.com/problems/remove-duplicates-from-sorted-list/description/

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
        Решение задачи "Remove Duplicates from Sorted List" (LeetCode 83).

        Задача:
        - Дан отсортированный связный список.
        - Удалить *повторяющиеся узлы*, оставив **по одному**
из каждого значения.

        Идея:
        - Проходим по списку один раз.
        - Если значение следующего узла такое же, как текущего,
          пропускаем его.
        - В итоге оставляем только уникальные элементы.

        Сложность:
        - Время: O(n)
        - Память: O(1)
        """
        curr = head

        while curr and curr.next:
            if curr.val == curr.next.val:
                # Пропускаем узел с дубликатом
                curr.next = curr.next.next
            else:
                curr = curr.next

        return head


''' Полезные ссылки: '''
# 1. Telegram ❃ Хижина программиста Æ: https://t.me/hut_programmer_07  
# 2. Telegram №1 @quadd4rv1n7
# 3. Telegram №2 @dupley_maxim_1999
# 4. Rutube канал: https://rutube.ru/channel/4218729/  
# 5. Plvideo канал: https://plvideo.ru/channel/AUPv_p1r5AQJ  
# 6. YouTube канал: https://www.youtube.com/@it-coders  
# 7. ВК группа: https://vk.com/science_geeks
