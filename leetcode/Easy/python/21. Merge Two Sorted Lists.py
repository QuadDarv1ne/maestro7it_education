'''
https://leetcode.com/problems/merge-two-sorted-lists/description/
'''

class Solution:
    def mergeTwoLists(self, l1, l2):
        """
        Объединяет два отсортированных односвязных списка в один отсортированный.

        Args:
            l1 (ListNode): голова первого списка.
            l2 (ListNode): голова второго списка.

        Returns:
            ListNode: голова нового объединённого отсортированного списка.

        Алгоритм:
        - Используется фиктивная голова dummy и tail для отслеживания конца списка.
        - Проходим по обоим спискам, соединяя меньший элемент.
        - После основного цикла присоединяем остаток.

        Сложности:
        - Время: O(m + n), где m, n — длины списков.
        - Память: O(1), используются только указатели.
        """
        dummy = tail = ListNode(0)
        while l1 and l2:
            if l1.val <= l2.val:
                tail.next = l1
                l1 = l1.next
            else:
                tail.next = l2
                l2 = l2.next
            tail = tail.next
        tail.next = l1 if l1 else l2
        return dummy.next

''' Полезные ссылки: '''
# 1. 💠Telegram💠❃ Хижина программиста Æ: https://t.me/hut_programmer_07
# 2. 💠Telegram №1💠 @quadd4rv1n7
# 3. 💠Telegram №2💠 @dupley_maxim_1999
# 4. Rutube канал: https://rutube.ru/channel/4218729/
# 5. Plvideo канал: https://plvideo.ru/channel/AUPv_p1r5AQJ
# 6. YouTube канал: https://www.youtube.com/@it-coders
# 7. ВК группа: https://vk.com/science_geeks