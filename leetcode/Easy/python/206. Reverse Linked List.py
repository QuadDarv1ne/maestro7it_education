'''
https://leetcode.com/problems/reverse-linked-list/

Автор: Дуплей Максим Игоревич
ORCID: https://orcid.org/0009-0007-7605-539X
GitHub: https://github.com/QuadDarv1ne/
'''

# class ListNode:
#     def __init__(self, val=0, next=None):
#         self.val = val
#         self.next = next

class Solution:
    # def reverseList(self, head: ListNode) -> ListNode:
    def reverseList(self, head):
        """
        Переворачивает односвязный список.

        Алгоритм:
        1. prev = None (новая голова списка)
        2. Идём по списку с current
        3. next_node = current.next
        4. current.next = prev
        5. prev = current, current = next_node
        6. Возвращаем prev как новую голову

        Время: O(n) — один проход по списку
        Память: O(1) — без доп. структур
        """
        prev = None
        current = head
        while current:
            next_node = current.next
            current.next = prev
            prev = current
            current = next_node
        return prev

''' Полезные ссылки: '''
# 1. 💠Telegram💠❃ Хижина программиста Æ: https://t.me/hut_programmer_07
# 2. 💠Telegram №1💠 @quadd4rv1n7
# 3. 💠Telegram №2💠 @dupley_maxim_1999
# 4. Rutube канал: https://rutube.ru/channel/4218729/
# 5. Plvideo канал: https://plvideo.ru/channel/AUPv_p1r5AQJ
# 6. YouTube канал: https://www.youtube.com/@it-coders
# 7. ВК группа: https://vk.com/science_geeks