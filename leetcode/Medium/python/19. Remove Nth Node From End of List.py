'''
https://leetcode.com/problems/remove-nth-node-from-end-of-list/description/
'''

class Solution:
    def removeNthFromEnd(self, head, n):
        """
        Удаляет n-й узел с конца односвязного списка.

        Алгоритм:
        - Используем фиктивную голову dummy для упрощения удаления
        - Используем два указателя: fast и slow
        - Передвигаем fast на n+1 шаг вперёд
        - Двигаем оба указателя на один шаг, пока fast не достигнет конца
        - slow.next — узел, который нужно удалить
        - Присваиваем slow.next = slow.next.next

        Время: O(L), L — длина списка
        Память: O(1)

        :param head: ListNode — голова списка
        :param n: int — номер узла с конца, который нужно удалить
        :return: ListNode — голова обновлённого списка
        """
        dummy = ListNode(0)
        dummy.next = head
        fast = slow = dummy

        for _ in range(n + 1):
            fast = fast.next

        while fast:
            fast = fast.next
            slow = slow.next

        slow.next = slow.next.next
        return dummy.next

''' Полезные ссылки: '''
# 1. 💠Telegram💠❃ Хижина программиста Æ: https://t.me/hut_programmer_07
# 2. 💠Telegram №1💠 @quadd4rv1n7
# 3. 💠Telegram №2💠 @dupley_maxim_1999
# 4. Rutube канал: https://rutube.ru/channel/4218729/
# 5. Plvideo канал: https://plvideo.ru/channel/AUPv_p1r5AQJ
# 6. YouTube канал: https://www.youtube.com/@it-coders
# 7. ВК группа: https://vk.com/science_geeks