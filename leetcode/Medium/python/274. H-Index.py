'''
https://leetcode.com/problems/h-index/description/?envType=study-plan-v2&envId=top-interview-150
'''

class Solution:
    def hIndex(self, citations):
        """
        Вычисляет h-индекс исследователя.

        Параметры:
        ----------
        citations : List[int]
            Массив количества цитирований каждой работы.

        Возвращает:
        -----------
        int
            Максимальный h-индекс: количество работ, у которых не менее h цитирований.

        Алгоритм:
        ---------
        1. Сортируем массив по убыванию.
        2. Ищем максимальное h, для которого citations[h-1] >= h.
        """
        citations.sort(reverse=True)
        h = 0
        for i, c in enumerate(citations, 1):
            if c >= i:
                h = i
            else:
                break
        return h

''' Полезные ссылки: '''
# 1. 💠Telegram💠❃ Хижина программиста Æ: https://t.me/hut_programmer_07
# 2. 💠Telegram №1💠 @quadd4rv1n7
# 3. 💠Telegram №2💠 @dupley_maxim_1999
# 4. Rutube канал: https://rutube.ru/channel/4218729/
# 5. Plvideo канал: https://plvideo.ru/channel/AUPv_p1r5AQJ
# 6. YouTube канал: https://www.youtube.com/@it-coders
# 7. ВК группа: https://vk.com/science_geeks