'''
https://leetcode.com/problems/reverse-nodes-in-k-group/description/
'''

class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

class Solution:
    # def reverseKGroup(self, head: ListNode, k: int) -> ListNode:
    def reverseKGroup(self, head, k):
        """
        Разворачивает элементы связанного списка группами по k элементов.
        """
        # Проверка на наличие k элементов
        node = head
        count = 0
        while node and count < k:
            node = node.next
            count += 1
        if count < k:
            return head  # меньше k элементов, возвращаем оригинальный список

        # Разворот текущей группы
        prev, curr = None, head
        for _ in range(k):
            next_node = curr.next
            curr.next = prev
            prev = curr
            curr = next_node

        # Рекурсивный вызов для оставшейся части списка
        head.next = self.reverseKGroup(curr, k)
        return prev

''' Полезные ссылки: '''
# 1. 💠Telegram💠❃ Хижина программиста Æ: https://t.me/hut_programmer_07
# 2. 💠Telegram №1💠 @quadd4rv1n7
# 3. 💠Telegram №2💠 @dupley_maxim_1999
# 4. Rutube канал: https://rutube.ru/channel/4218729/
# 5. Plvideo канал: https://plvideo.ru/channel/AUPv_p1r5AQJ
# 6. YouTube канал: https://www.youtube.com/@it-coders
# 7. ВК группа: https://vk.com/science_geeks