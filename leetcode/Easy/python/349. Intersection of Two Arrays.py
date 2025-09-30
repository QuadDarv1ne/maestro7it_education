'''
https://leetcode.com/problems/intersection-of-two-arrays/description/

Автор: Дуплей Максим Игоревич
ORCID: https://orcid.org/0009-0007-7605-539X
GitHub: https://github.com/QuadDarv1ne/
'''

class Solution:
    def intersection(self, nums1, nums2):
        """
        Функция ищет пересечение двух массивов.
        Каждый элемент результата уникален.

        :param nums1: List[int] - первый массив чисел
        :param nums2: List[int] - второй массив чисел
        :return: List[int] - список уникальных элементов, встречающихся в обоих массивах
        """
        return list(set(nums1) & set(nums2))

''' Полезные ссылки: '''
# 1. 💠Telegram💠❃ Хижина программиста Æ: https://t.me/hut_programmer_07
# 2. 💠Telegram №1💠 @quadd4rv1n7
# 3. 💠Telegram №2💠 @dupley_maxim_1999
# 4. Rutube канал: https://rutube.ru/channel/4218729/
# 5. Plvideo канал: https://plvideo.ru/channel/AUPv_p1r5AQJ
# 6. YouTube канал: https://www.youtube.com/@it-coders
# 7. ВК группа: https://vk.com/science_geeks