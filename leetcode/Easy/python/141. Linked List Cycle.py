'''
https://leetcode.com/problems/linked-list-cycle/description/

Автор: Дуплей Максим Игоревич
ORCID: https://orcid.org/0009-0007-7605-539X
GitHub: https://github.com/QuadDarv1ne/
'''

class Solution:
    def hasCycle(self, head):
        """
        Определяет, содержит ли односвязный список цикл.

        Алгоритм:
        - Используем метод "медленного и быстрого указателей" (Floyd’s Cycle Detection)
        - slow двигается на 1 шаг, fast двигается на 2 шага
        - Если slow == fast — цикл найден
        - Если fast или fast.next == None — цикла нет

        Время: O(n)
        Память: O(1)

        :param head: ListNode — голова односвязного списка
        :return: bool — True, если есть цикл; False, если цикла нет
        """
        if not head or not head.next:
            return False

        slow, fast = head, head.next
        while fast and fast.next:
            if slow == fast:
                return True
            slow = slow.next
            fast = fast.next.next
        return False

''' Полезные ссылки: '''
# 1. 💠Telegram💠❃ Хижина программиста Æ: https://t.me/hut_programmer_07
# 2. 💠Telegram №1💠 @quadd4rv1n7
# 3. 💠Telegram №2💠 @dupley_maxim_1999
# 4. Rutube канал: https://rutube.ru/channel/4218729/
# 5. Plvideo канал: https://plvideo.ru/channel/AUPv_p1r5AQJ
# 6. YouTube канал: https://www.youtube.com/@it-coders
# 7. ВК группа: https://vk.com/science_geeks