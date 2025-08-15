'''
https://leetcode.com/problems/intersection-of-two-linked-lists/description/
'''

class Solution:
    def getIntersectionNode(self, headA, headB):
        """
        Находит узел пересечения двух односвязных списков.
        Если пересечения нет, возвращает None.

        Алгоритм:
        1. Определяем длину обоих списков.
        2. Выравниваем указатели по длине списков.
        3. Двигаем оба указателя одновременно, пока не найдём пересечение или конец списков.

        Время: O(A + B), где A и B — длины списков
        Память: O(1)

        :param headA: ListNode — голова первого списка
        :param headB: ListNode — голова второго списка
        :return: ListNode или None — узел пересечения
        """
        if not headA or not headB:
            return None

        # Определяем длину списков
        lenA = lenB = 0
        currA, currB = headA, headB
        while currA:
            lenA += 1
            currA = currA.next
        while currB:
            lenB += 1
            currB = currB.next

        # Выравниваем списки
        currA, currB = headA, headB
        if lenA > lenB:
            for _ in range(lenA - lenB):
                currA = currA.next
        else:
            for _ in range(lenB - lenA):
                currB = currB.next

        # Ищем пересечение
        while currA and currB:
            if currA == currB:
                return currA
            currA = currA.next
            currB = currB.next

        return None

''' Полезные ссылки: '''
# 1. 💠Telegram💠❃ Хижина программиста Æ: https://t.me/hut_programmer_07
# 2. 💠Telegram №1💠 @quadd4rv1n7
# 3. 💠Telegram №2💠 @dupley_maxim_1999
# 4. Rutube канал: https://rutube.ru/channel/4218729/
# 5. Plvideo канал: https://plvideo.ru/channel/AUPv_p1r5AQJ
# 6. YouTube канал: https://www.youtube.com/@it-coders
# 7. ВК группа: https://vk.com/science_geeks