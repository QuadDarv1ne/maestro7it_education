'''
https://leetcode.com/problems/summary-ranges/description/?envType=study-plan-v2&envId=top-interview-150

Автор: Дуплей Максим Игоревич
ORCID: https://orcid.org/0009-0007-7605-539X
GitHub: https://github.com/QuadDarv1ne/
'''

class Solution:
    def summaryRanges(self, nums):
        """
        Функция принимает отсортированный список уникальных целых чисел и возвращает список строк,
        представляющих минимальные диапазоны последовательных чисел.

        :param nums: List[int] - отсортированный список уникальных чисел
        :return: List[str] - список диапазонов в формате "start->end" или "start" если диапазон из одного числа
        """
        ranges = []
        i = 0
        while i < len(nums):
            start = nums[i]
            while i + 1 < len(nums) and nums[i + 1] == nums[i] + 1:
                i += 1
            if start == nums[i]:
                ranges.append(str(start))
            else:
                ranges.append(str(start) + "->" + str(nums[i]))
            i += 1
        return ranges

''' Полезные ссылки: '''
# 1. 💠Telegram💠❃ Хижина программиста Æ: https://t.me/hut_programmer_07
# 2. 💠Telegram №1💠 @quadd4rv1n7
# 3. 💠Telegram №2💠 @dupley_maxim_1999
# 4. Rutube канал: https://rutube.ru/channel/4218729/
# 5. Plvideo канал: https://plvideo.ru/channel/AUPv_p1r5AQJ
# 6. YouTube канал: https://www.youtube.com/@it-coders
# 7. ВК группа: https://vk.com/science_geeks