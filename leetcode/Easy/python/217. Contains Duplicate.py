'''
https://leetcode.com/problems/contains-duplicate/description/
'''

class Solution:
    def containsDuplicate(self, nums):
        """
        Проверяет, есть ли в списке дубли (повторяющиеся элементы).

        Используется набор (set) для отслеживания уже встреченных чисел.
        Время: O(n) — прохождение списка один раз.
        Память: O(n) — набор в худшем случае хранит все элементы.

        :param nums: list[int] — исходный список целых чисел
        :return: bool — True, если есть повторяющийся элемент, иначе False
        """
        seen = set()
        for num in nums:
            if num in seen:
                return True
            seen.add(num)
        return False

''' Полезные ссылки: '''
# 1. 💠Telegram💠❃ Хижина программиста Æ: https://t.me/hut_programmer_07
# 2. 💠Telegram №1💠 @quadd4rv1n7
# 3. 💠Telegram №2💠 @dupley_maxim_1999
# 4. Rutube канал: https://rutube.ru/channel/4218729/
# 5. Plvideo канал: https://plvideo.ru/channel/AUPv_p1r5AQJ
# 6. YouTube канал: https://www.youtube.com/@it-coders
# 7. ВК группа: https://vk.com/science_geeks